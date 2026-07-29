import assert from "node:assert/strict";
import childProcess from "node:child_process";
import { EventEmitter } from "node:events";
import {
  chmod,
  copyFile,
  mkdtemp,
  mkdir,
  open,
  readFile,
  readdir,
  readlink,
  rename,
  rm,
  symlink,
  writeFile,
} from "node:fs/promises";
import { syncBuiltinESMExports } from "node:module";
import { connect } from "node:net";
import { tmpdir } from "node:os";
import { basename, dirname, join } from "node:path";
import { PassThrough } from "node:stream";
import test from "node:test";
import {
  assertSafeBindHost,
  startGalleryServer,
} from "./server.mjs";
import { createPinnedRoot } from "./pinned-fs.mjs";
import { createDemoFixture } from "./test-helpers.mjs";

test("public wildcard hosts are always rejected", () => {
  for (const host of ["0.0.0.0", "::"]) {
    assert.throws(
      () => assertSafeBindHost(host, {
        allowLoopback: true,
        interfaceAddresses: [host],
      }),
      /public bind forbidden/,
    );
  }
});

test("non-Tailscale IPv4 is rejected", () => {
  assert.throws(
    () => assertSafeBindHost("192.168.1.20"),
    /Tailscale IPv4 required/,
  );
});

test("loopback requires its explicit test-only override", () => {
  assert.throws(
    () => assertSafeBindHost("127.0.0.1"),
    /loopback bind forbidden/,
  );
  assert.equal(
    assertSafeBindHost("127.0.0.1", { allowLoopback: true }),
    "127.0.0.1",
  );
});

test("Tailscale range boundaries require exact local interface membership", () => {
  for (const host of ["100.64.0.0", "100.127.255.255"]) {
    assert.equal(
      assertSafeBindHost(host, { interfaceAddresses: [host] }),
      host,
    );
  }
  assert.throws(
    () => assertSafeBindHost("100.128.0.0", {
      interfaceAddresses: ["100.128.0.0"],
    }),
    /Tailscale IPv4 required/,
  );
  assert.throws(
    () => assertSafeBindHost("100.100.20.30", { interfaceAddresses: [] }),
    /host not present on a local interface/,
  );
});

test("IPv4 parser rejects non-canonical or out-of-range octets", () => {
  for (const host of [
    "100.064.0.1",
    "100.64.0",
    "100.64.0.1.2",
    "100.64.0.-1",
    "100.64.0.256",
    "tailscale.local",
  ]) {
    assert.throws(
      () => assertSafeBindHost(host, { interfaceAddresses: [host] }),
      /Tailscale IPv4 required/,
      host,
    );
  }
});

async function startFixture(t, options = {}) {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-server-"));
  const fixture = await createDemoFixture(dataRoot);
  const running = await startGalleryServer({
    dataRoot,
    host: "127.0.0.1",
    port: 0,
    allowLoopback: true,
    ...options,
  });
  t.after(() => running.close());
  return { dataRoot, fixture, running };
}

async function descriptorForPath(path) {
  const descriptorDirectory = `/proc/${process.pid}/fd`;
  for (const name of await readdir(descriptorDirectory)) {
    try {
      if (await readlink(join(descriptorDirectory, name)) === path) {
        return Number(name);
      }
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
  }
  throw new Error(`no open descriptor for ${path}`);
}

async function waitForJson(path, timeoutMs = 500) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      return JSON.parse(await readFile(path, "utf8"));
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
    await new Promise((resolve) => setTimeout(resolve, 5));
  }
  throw new Error(`timed out waiting for ${path}`);
}

async function waitForProcessExit(pid, timeoutMs = 1_000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      process.kill(pid, 0);
    } catch (error) {
      if (error.code === "ESRCH") return;
      throw error;
    }
    await new Promise((resolve) => setTimeout(resolve, 10));
  }
  throw new Error(`process ${pid} did not exit`);
}

test("pinned root close defers descriptor reuse until active work settles", async () => {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-pinned-root-"));
  await writeFile(join(dataRoot, "probe.txt"), "inside", "utf8");
  const outside = await mkdtemp(join(tmpdir(), "akari-outside-"));
  const pinnedRoot = createPinnedRoot(dataRoot);
  let enterWork;
  const workEntered = new Promise((resolve) => {
    enterWork = resolve;
  });
  let releaseWork;
  const workBlocked = new Promise((resolve) => {
    releaseWork = resolve;
  });
  const activeWork = pinnedRoot.withLease(async () => {
    enterWork();
    await workBlocked;
    assert.equal(
      await pinnedRoot.fileSystem.readFile("probe.txt", "utf8"),
      "inside",
    );
  });
  await workEntered;
  const rootFd = await descriptorForPath(dataRoot);
  pinnedRoot.close();

  const outsideHandles = [];
  let rootFdWasReused = false;
  try {
    for (let index = 0; index < 64; index += 1) {
      const handle = await open(outside, "r");
      outsideHandles.push(handle);
      if (handle.fd === rootFd) rootFdWasReused = true;
    }
    assert.equal(rootFdWasReused, false);
  } finally {
    releaseWork();
    await activeWork;
    await Promise.all(outsideHandles.map((handle) => handle.close()));
    pinnedRoot.close();
    await rm(dataRoot, { recursive: true, force: true });
    await rm(outside, { recursive: true, force: true });
  }
});

test("API returns a validated batch and review progress", async (t) => {
  const { running } = await startFixture(t);
  const response = await fetch(`${running.url}/api/batches/B001`);
  assert.equal(response.status, 200);
  const payload = await response.json();
  assert.equal(payload.ok, true);
  assert.equal(payload.data.entries.length, 50);

  const reviewsResponse = await fetch(
    `${running.url}/api/batches/B001/reviews`,
  );
  assert.equal(reviewsResponse.status, 200);
  const reviewsPayload = await reviewsResponse.json();
  assert.equal(Object.keys(reviewsPayload.data.reviews).length, 50);
  assert.equal(reviewsPayload.data.reviews["B001-001"].revision, 0);
});

test("batch listing isolates malformed manifests", async (t) => {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-server-"));
  await createDemoFixture(dataRoot);
  const invalid = await createDemoFixture(dataRoot, { batchId: "B002" });
  invalid.manifest.entries.pop();
  await writeFile(
    join(invalid.batchDir, "manifest.json"),
    JSON.stringify(invalid.manifest),
    "utf8",
  );
  const running = await startGalleryServer({
    dataRoot,
    host: "127.0.0.1",
    port: 0,
    allowLoopback: true,
  });
  t.after(() => running.close());

  const response = await fetch(`${running.url}/api/batches`);
  assert.equal(response.status, 200);
  const payload = await response.json();
  const valid = payload.data.batches.find(({ batchId }) => batchId === "B001");
  const malformed =
    payload.data.batches.find(({ batchId }) => batchId === "B002");
  assert.equal(valid.disabled, false);
  assert.equal(malformed.disabled, true);
  assert.match(malformed.validationMessage, /exactly 50 entries/);
});

test("reference hashes are checked whenever a batch is loaded", async (t) => {
  const { dataRoot, running } = await startFixture(t);
  await writeFile(
    join(dataRoot, "references/akari-v1.5-b3-body-balance.png"),
    Buffer.from("changed"),
  );
  const response = await fetch(`${running.url}/api/batches/B001`);
  assert.equal(response.status, 422);
  const payload = await response.json();
  assert.equal(payload.ok, false);
  assert.match(payload.error.message, /invalid reference sha256/);
});

test("batch manifests cannot be read through a symlink outside dataRoot", async (t) => {
  const { fixture, running } = await startFixture(t);
  const outside = await mkdtemp(join(tmpdir(), "akari-outside-"));
  const manifestPath = join(fixture.batchDir, "manifest.json");
  const outsideManifest = join(outside, "manifest.json");
  await copyFile(manifestPath, outsideManifest);
  await rm(manifestPath);
  await symlink(outsideManifest, manifestPath);

  const response = await fetch(`${running.url}/api/batches/B001`);
  assert.equal(response.status, 422);
  assert.equal((await response.json()).error.code, "invalid_batch");
});

test("reference snapshots cannot be read through a symlink outside dataRoot", async (t) => {
  const { dataRoot, running } = await startFixture(t);
  const outside = await mkdtemp(join(tmpdir(), "akari-outside-"));
  const referencePath = join(
    dataRoot,
    "references/akari-v1.5-b3-body-balance.png",
  );
  const outsideReference = join(outside, "reference.png");
  await copyFile(referencePath, outsideReference);
  await rm(referencePath);
  await symlink(outsideReference, referencePath);

  const response = await fetch(`${running.url}/api/batches/B001`);
  assert.equal(response.status, 422);
  assert.equal((await response.json()).error.code, "invalid_batch");
});

test("review state cannot be read through a symlink outside dataRoot", async (t) => {
  const { fixture, running } = await startFixture(t);
  const reviews = await fetch(
    `${running.url}/api/batches/B001/reviews`,
  ).then((response) => response.json());
  const outside = await mkdtemp(join(tmpdir(), "akari-outside-"));
  const outsideReviews = join(outside, "reviews.json");
  await writeFile(outsideReviews, JSON.stringify(reviews.data), "utf8");
  await symlink(outsideReviews, join(fixture.batchDir, "reviews.json"));

  const response = await fetch(
    `${running.url}/api/batches/B001/reviews`,
  );
  assert.equal(response.status, 500);
  assert.equal((await response.json()).error.code, "review_load_failed");
});

test("review backup cannot overwrite a symlink target outside dataRoot", async (t) => {
  const { fixture, running } = await startFixture(t);
  const update = (expectedRevision, status) =>
    fetch(`${running.url}/api/batches/B001/reviews/B001-001`, {
      method: "PUT",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        expectedRevision,
        status,
        reasons: [],
        note: "",
      }),
    });
  assert.equal((await update(0, "keep")).status, 200);
  const outside = await mkdtemp(join(tmpdir(), "akari-outside-"));
  const outsideBackup = join(outside, "reviews.json.bak");
  await writeFile(outsideBackup, "outside sentinel", "utf8");
  await symlink(
    outsideBackup,
    join(fixture.batchDir, "reviews.json.bak"),
  );

  const response = await update(1, "favorite");
  assert.equal(response.status, 500);
  assert.equal((await response.json()).error.code, "durable_write_failed");
  assert.equal(await readFile(outsideBackup, "utf8"), "outside sentinel");
});

test("dangling review backup symlink cannot create a file outside dataRoot", async (t) => {
  const { fixture, running } = await startFixture(t);
  const update = (expectedRevision, status) =>
    fetch(`${running.url}/api/batches/B001/reviews/B001-001`, {
      method: "PUT",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        expectedRevision,
        status,
        reasons: [],
        note: "",
      }),
    });
  assert.equal((await update(0, "keep")).status, 200);
  const outside = await mkdtemp(join(tmpdir(), "akari-outside-"));
  const missingOutsideBackup = join(outside, "missing-backup.json");
  await symlink(
    missingOutsideBackup,
    join(fixture.batchDir, "reviews.json.bak"),
  );

  const response = await update(1, "favorite");
  assert.equal(response.status, 500);
  await assert.rejects(readFile(missingOutsideBackup), { code: "ENOENT" });
});

test("unknown batches and malformed paths use stable JSON 404 responses", async (t) => {
  const { running } = await startFixture(t);
  for (const path of [
    "/api/batches/B999",
    "/api/batches/%E0%A4%A",
    "/api/batches/B001/unknown",
  ]) {
    const response = await fetch(`${running.url}${path}`);
    assert.equal(response.status, 404, path);
    const payload = await response.json();
    assert.deepEqual(payload, {
      ok: false,
      error: {
        code: "not_found",
        message: "resource not found",
      },
    });
  }
});

test("invalid review input is rejected without changing state", async (t) => {
  const { running } = await startFixture(t);
  const response = await fetch(
    `${running.url}/api/batches/B001/reviews/B001-001`,
    {
      method: "PUT",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        expectedRevision: 0,
        status: "keep",
        reasons: ["skin-flat"],
        note: "",
      }),
    },
  );
  assert.equal(response.status, 422);
  const payload = await response.json();
  assert.equal(payload.ok, false);
  assert.equal(payload.error.code, "invalid_review");

  const reviews = await fetch(
    `${running.url}/api/batches/B001/reviews`,
  ).then((result) => result.json());
  assert.equal(reviews.data.reviews["B001-001"].revision, 0);
});

test("JSON request bodies are capped at 64 KiB", async (t) => {
  const { running } = await startFixture(t);
  const response = await fetch(
    `${running.url}/api/batches/B001/reviews/B001-001`,
    {
      method: "PUT",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        expectedRevision: 0,
        status: "keep",
        reasons: [],
        note: "x".repeat(65_536),
      }),
    },
  );
  assert.equal(response.status, 413);
  const payload = await response.json();
  assert.equal(payload.error.code, "request_too_large");
});

test("oversized chunked body returns 413 without waiting for EOF", async (t) => {
  const { running } = await startFixture(t);
  const socket = connect(running.port, running.host);
  t.after(() => socket.destroy());
  await new Promise((resolve, reject) => {
    socket.once("connect", resolve);
    socket.once("error", reject);
  });
  const response = new Promise((resolve, reject) => {
    socket.once("data", (chunk) => resolve(chunk.toString("utf8")));
    socket.once("error", reject);
  });
  socket.write([
    "PUT /api/batches/B001/reviews/B001-001 HTTP/1.1",
    `Host: ${running.host}:${running.port}`,
    "Content-Type: application/json",
    "Transfer-Encoding: chunked",
    "",
    `${(65_537).toString(16)}`,
    "x".repeat(65_537),
    "",
  ].join("\r\n"));

  let firstChunk;
  try {
    firstChunk = await Promise.race([
      response,
      new Promise((_, reject) => setTimeout(
        () => reject(new Error("server waited for request EOF")),
        500,
      )),
    ]);
  } finally {
    socket.destroy();
  }
  assert.match(firstChunk, /^HTTP\/1\.1 413 Payload Too Large/m);
});

test("media route rejects traversal and undeclared ids", async (t) => {
  const { running } = await startFixture(t);
  for (const path of [
    "/media/B001/%2e%2e%2fetc%2fpasswd/image",
    "/media/B001/B001-999/image",
    "/media/B001/B001-001/%2e%2e%2fimage",
  ]) {
    const response = await fetch(`${running.url}${path}`);
    assert.equal(response.status, 404, path);
  }
});

test("missing original disables only that media response", async (t) => {
  const { fixture, running } = await startFixture(t);
  await rm(join(fixture.batchDir, "images/image-1.png"));
  const missing = await fetch(
    `${running.url}/media/B001/B001-001/image`,
  );
  const available = await fetch(
    `${running.url}/media/B001/B001-002/image`,
  );
  assert.equal(missing.status, 404);
  assert.equal(available.status, 200);
});

test("original media cannot be read through a symlink outside dataRoot", async (t) => {
  const { fixture, running } = await startFixture(t);
  const outside = await mkdtemp(join(tmpdir(), "akari-outside-"));
  const imagePath = join(fixture.batchDir, "images/image-1.png");
  const outsideImage = join(outside, "image.png");
  await copyFile(imagePath, outsideImage);
  await rm(imagePath);
  await symlink(outsideImage, imagePath);

  const response = await fetch(
    `${running.url}/media/B001/B001-001/image`,
  );
  assert.equal(response.status, 404);
  assert.equal((await response.json()).error.code, "media_unavailable");
});

test("original media requires a valid PNG signature", async (t) => {
  const { fixture, running } = await startFixture(t);
  await writeFile(
    join(fixture.batchDir, "images/image-1.png"),
    Buffer.from("not a png"),
  );
  const response = await fetch(
    `${running.url}/media/B001/B001-001/image`,
  );
  assert.equal(response.status, 404);
  assert.equal((await response.json()).error.code, "media_unavailable");
});

test("declared PNG hash is checked before serving media", async (t) => {
  const { fixture, running } = await startFixture(t);
  const manifestPath = join(fixture.batchDir, "manifest.json");
  const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
  const image = await readFile(join(fixture.batchDir, "images/image-1.png"));
  manifest.entries[0].artifact.sha256 =
    "abf4de8d2a57f7e3c7ddce453f941e74fe3cc1d591b4ff36962b4196c02c88d4";
  manifest.entries[0].artifact.width = 1;
  manifest.entries[0].artifact.height = 1;
  manifest.entries[0].generation.technicalStatus = "valid";
  await writeFile(manifestPath, JSON.stringify(manifest), "utf8");
  assert.notEqual(image.length, 0);

  const response = await fetch(
    `${running.url}/media/B001/B001-001/image`,
  );
  assert.equal(response.status, 404);
});

test("valid original media has PNG headers", async (t) => {
  const { running } = await startFixture(t);
  const response = await fetch(
    `${running.url}/media/B001/B001-001/image`,
  );
  assert.equal(response.status, 200);
  assert.equal(response.headers.get("content-type"), "image/png");
  const bytes = Buffer.from(await response.arrayBuffer());
  assert.equal(bytes.subarray(0, 8).toString("hex"), "89504e470d0a1a0a");
});

test("thumbnail media cannot be read through a symlink outside dataRoot", async (t) => {
  const { fixture, running } = await startFixture(t);
  const outside = await mkdtemp(join(tmpdir(), "akari-outside-"));
  const thumbnailPath = join(fixture.batchDir, "thumbs/image-1.webp");
  const outsideThumbnail = join(outside, "image.webp");
  await copyFile(thumbnailPath, outsideThumbnail);
  await rm(thumbnailPath);
  await symlink(outsideThumbnail, thumbnailPath);

  const response = await fetch(
    `${running.url}/media/B001/B001-001/thumb`,
  );
  assert.equal(response.status, 404);
  assert.equal((await response.json()).error.code, "media_unavailable");
});

test("thumbnail repair cannot overwrite a symlink target outside dataRoot", async (t) => {
  let repairs = 0;
  const outside = await mkdtemp(join(tmpdir(), "akari-outside-"));
  const outsideTarget = join(outside, "target.webp");
  await writeFile(outsideTarget, Buffer.from("outside sentinel"));
  const { fixture, running } = await startFixture(t, {
    thumbnailBuilder: async () => {
      repairs += 1;
    },
  });
  const thumbnailPath = join(fixture.batchDir, "thumbs/image-1.webp");
  await rm(thumbnailPath);
  await symlink(outsideTarget, thumbnailPath);

  const response = await fetch(
    `${running.url}/media/B001/B001-001/thumb`,
  );
  assert.equal(response.status, 404);
  assert.equal(repairs, 0);
  assert.equal(await readFile(outsideTarget, "utf8"), "outside sentinel");
});

test("thumbnail repair reads a private copy of the validated PNG", async (t) => {
  let observedSource;
  let validWebp;
  const outside = await mkdtemp(join(tmpdir(), "akari-outside-"));
  const outsideSource = join(outside, "outside.png");
  await writeFile(outsideSource, Buffer.from("outside sentinel"));
  const { fixture, running } = await startFixture(t, {
    thumbnailBuilder: async (source, output) => {
      const declaredSource = join(fixture.batchDir, "images/image-1.png");
      await rm(declaredSource);
      await symlink(outsideSource, declaredSource);
      observedSource = await readFile(source);
      await writeFile(output, validWebp);
    },
  });
  validWebp = await readFile(join(fixture.batchDir, "thumbs/image-2.webp"));
  await rm(join(fixture.batchDir, "thumbs/image-1.webp"));

  const response = await fetch(
    `${running.url}/media/B001/B001-001/thumb`,
  );
  assert.equal(response.status, 200);
  assert.equal(
    observedSource.subarray(0, 8).toString("hex"),
    "89504e470d0a1a0a",
  );
});

test("parent replacement cannot redirect thumbnail install or cleanup", async (t) => {
  let outsideCleanupSentinel;
  let outsideInstallSentinel;
  let pinnedThumbs;
  let validWebp;
  const outside = await mkdtemp(join(tmpdir(), "akari-outside-"));
  const { fixture, running } = await startFixture(t, {
    thumbnailBuilder: async (_source, output) => {
      await writeFile(output, validWebp);
      const thumbs = join(fixture.batchDir, "thumbs");
      pinnedThumbs = `${thumbs}-pinned`;
      await rename(thumbs, pinnedThumbs);
      const redirectedTemporary = join(
        outside,
        basename(dirname(output)),
      );
      await mkdir(redirectedTemporary);
      outsideCleanupSentinel = join(
        redirectedTemporary,
        "cleanup-sentinel.txt",
      );
      outsideInstallSentinel = join(outside, "image-1.webp");
      await writeFile(
        outsideCleanupSentinel,
        "outside cleanup sentinel",
        "utf8",
      );
      await writeFile(
        outsideInstallSentinel,
        "outside install sentinel",
        "utf8",
      );
      await symlink(outside, thumbs);
    },
  });
  validWebp = await readFile(join(fixture.batchDir, "thumbs/image-2.webp"));
  await rm(join(fixture.batchDir, "thumbs/image-1.webp"));

  const response = await fetch(
    `${running.url}/media/B001/B001-001/thumb`,
  );
  assert.equal(
    await readFile(outsideCleanupSentinel, "utf8"),
    "outside cleanup sentinel",
  );
  assert.equal(
    await readFile(outsideInstallSentinel, "utf8"),
    "outside install sentinel",
  );
  assert.equal(response.status, 200);
  assert.equal(
    (await readFile(join(pinnedThumbs, "image-1.webp")))
      .subarray(0, 4)
      .toString("ascii"),
    "RIFF",
  );
});

test("timed-out builder cannot access a reused directory descriptor", async (t) => {
  let builderOutput;
  let finishBuilder;
  let validWebp;
  const builderBlocked = new Promise((resolve) => {
    finishBuilder = resolve;
  });
  let markBuilderFinished;
  const builderFinished = new Promise((resolve) => {
    markBuilderFinished = resolve;
  });
  const outside = await mkdtemp(join(tmpdir(), "akari-reused-fd-"));
  t.after(() => rm(outside, { recursive: true, force: true }));
  const { fixture, running } = await startFixture(t, {
    thumbnailRepairTimeoutMs: 40,
    thumbnailBuilder: async (_source, output) => {
      builderOutput = output;
      await builderBlocked;
      try {
        await writeFile(output, validWebp);
      } finally {
        markBuilderFinished();
      }
    },
  });
  validWebp = await readFile(join(fixture.batchDir, "thumbs/image-2.webp"));
  await rm(join(fixture.batchDir, "thumbs/image-1.webp"));

  const response = await Promise.race([
    fetch(`${running.url}/media/B001/B001-001/thumb`),
    new Promise((_, reject) => setTimeout(
      () => reject(new Error("thumbnail response exceeded its timeout bound")),
      500,
    )),
  ]);
  assert.equal(response.status, 404);
  const descriptor = Number(
    builderOutput.match(/^\/proc\/\d+\/fd\/(\d+)\//)?.[1],
  );
  assert.equal(Number.isInteger(descriptor), true);

  const outsideHandles = [];
  try {
    for (let index = 0; index < 64; index += 1) {
      outsideHandles.push(await open(outside, "r"));
    }
    finishBuilder();
    await builderFinished;
    await new Promise((resolve) => setImmediate(resolve));
    await assert.rejects(
      readFile(join(outside, "thumbnail.webp")),
      { code: "ENOENT" },
    );
  } finally {
    finishBuilder();
    await Promise.all(outsideHandles.map((handle) => handle.close()));
  }
});

test("production builder keeps its descriptor lease until child exit", async (t) => {
  const builderDirectory = await mkdtemp(
    join(tmpdir(), "akari-thumbnail-builder-"),
  );
  const executable = join(builderDirectory, "fake-python");
  const builderScript = join(builderDirectory, "fake-builder.cjs");
  const marker = join(builderDirectory, "started.json");
  t.after(() => rm(builderDirectory, { recursive: true, force: true }));
  await writeFile(
    builderScript,
    `
const { writeFileSync } = require("node:fs");
const { join } = require("node:path");
const outputIndex = process.argv.indexOf("--output");
const output = process.argv[outputIndex + 1];
process.on("SIGTERM", () => {});
writeFileSync(join(__dirname, "started.json"), JSON.stringify({
  pid: process.pid,
  output,
}));
setTimeout(() => {
  writeFileSync(
    output,
    Buffer.from(
      "UklGRiIAAABXRUJQVlA4IBYAAAAwAQCdASoBAAEAAUAmJQBOgCHwAP7+3gAA",
      "base64",
    ),
  );
}, 250);
setInterval(() => {}, 1_000);
`,
    "utf8",
  );
  await writeFile(
    executable,
    `#!/bin/sh
unset NODE_TEST_CONTEXT
exec ${process.execPath} ${builderScript} "$@"
`,
    "utf8",
  );
  await chmod(executable, 0o700);
  const outside = await mkdtemp(join(tmpdir(), "akari-child-reused-fd-"));
  t.after(() => rm(outside, { recursive: true, force: true }));
  const { fixture, running } = await startFixture(t, {
    repoRoot: process.cwd(),
    pythonExecutable: executable,
    thumbnailRepairTimeoutMs: 150,
  });
  await rm(join(fixture.batchDir, "thumbs/image-1.webp"));

  const request = fetch(
    `${running.url}/media/B001/B001-001/thumb`,
  );
  const started = await waitForJson(marker);
  const response = await Promise.race([
    request,
    new Promise((_, reject) => setTimeout(
      () => reject(new Error("thumbnail response exceeded its timeout bound")),
      700,
    )),
  ]);
  assert.equal(response.status, 404);
  const descriptor = Number(
    started.output.match(/^\/proc\/\d+\/fd\/(\d+)\//)?.[1],
  );
  assert.equal(Number.isInteger(descriptor), true);

  const outsideHandles = [];
  try {
    for (let index = 0; index < 64; index += 1) {
      outsideHandles.push(await open(outside, "r"));
    }
    await waitForProcessExit(started.pid);
    await assert.rejects(
      readFile(join(outside, "thumbnail.webp")),
      { code: "ENOENT" },
    );
  } finally {
    await Promise.all(outsideHandles.map((handle) => handle.close()));
  }
});

test("post-spawn kill error retains production repair leases until close", async (t) => {
  const originalSpawn = childProcess.spawn;
  const children = [];
  const closedChildren = new WeakSet();
  const closeChild = (child, code = 1) => {
    if (closedChildren.has(child)) return;
    closedChildren.add(child);
    child.emit("close", code, null);
  };
  let resolveFirstSpawn;
  const firstSpawn = new Promise((resolve) => {
    resolveFirstSpawn = resolve;
  });
  const postSpawnError = new Error("simulated post-spawn kill failure");
  childProcess.spawn = (_executable, argumentsList) => {
    const child = new EventEmitter();
    child.pid = 43_210 + children.length;
    child.stderr = new PassThrough();
    child.kill = () => {
      child.emit("error", postSpawnError);
      return false;
    };
    children.push(child);
    queueMicrotask(() => {
      child.emit("spawn");
      if (children.length === 1) {
        resolveFirstSpawn({ argumentsList, child });
      } else {
        closeChild(child);
      }
    });
    return child;
  };
  syncBuiltinESMExports();
  t.after(() => {
    childProcess.spawn = originalSpawn;
    syncBuiltinESMExports();
  });
  t.after(() => {
    for (const child of children) closeChild(child);
  });

  const outside = await mkdtemp(join(tmpdir(), "akari-post-spawn-error-"));
  t.after(() => rm(outside, { recursive: true, force: true }));
  const { fixture, running } = await startFixture(t, {
    repoRoot: process.cwd(),
    pythonExecutable: process.execPath,
    thumbnailRepairTimeoutMs: 10_000,
  });
  const validWebp = await readFile(
    join(fixture.batchDir, "thumbs/image-2.webp"),
  );
  await rm(join(fixture.batchDir, "thumbs/image-1.webp"));

  const firstRequest = fetch(
    `${running.url}/media/B001/B001-001/thumb`,
  );
  const started = await firstSpawn;
  const outputIndex = started.argumentsList.indexOf("--output");
  const output = started.argumentsList[outputIndex + 1];
  const descriptor = Number(
    output.match(/^\/proc\/\d+\/fd\/(\d+)\//)?.[1],
  );
  assert.equal(Number.isInteger(descriptor), true);
  await writeFile(output, validWebp);

  let firstSettled = false;
  const observedFirstRequest = firstRequest.then((response) => {
    firstSettled = true;
    return response;
  });
  started.child.kill("SIGTERM");
  await new Promise((resolve) => setTimeout(resolve, 50));
  const firstSettledBeforeClose = firstSettled;

  let secondSettled = false;
  const observedSecondRequest = fetch(
    `${running.url}/media/B001/B001-001/thumb`,
  ).then((response) => {
    secondSettled = true;
    return response;
  });
  await new Promise((resolve) => setTimeout(resolve, 50));
  const secondSettledBeforeClose = secondSettled;
  const spawnCountBeforeClose = children.length;

  const outsideHandles = [];
  let descriptorReusedBeforeClose = false;
  try {
    for (let index = 0; index < 64; index += 1) {
      const handle = await open(outside, "r");
      outsideHandles.push(handle);
      if (handle.fd === descriptor) descriptorReusedBeforeClose = true;
    }
  } finally {
    closeChild(started.child, 0);
  }
  let responses;
  try {
    responses = await Promise.all([
      observedFirstRequest,
      observedSecondRequest,
    ]);
  } finally {
    await Promise.all(outsideHandles.map((handle) => handle.close()));
  }

  assert.equal(firstSettledBeforeClose, false);
  assert.equal(secondSettledBeforeClose, false);
  assert.equal(spawnCountBeforeClose, 1);
  assert.equal(descriptorReusedBeforeClose, false);
  assert.deepEqual(responses.map(({ status }) => status), [404, 404]);
});

test("missing thumbnail is rebuilt once", async (t) => {
  let repairs = 0;
  let validWebp;
  const { fixture, running } = await startFixture(t, {
    thumbnailBuilder: async (_source, output) => {
      repairs += 1;
      await writeFile(output, validWebp);
    },
  });
  validWebp = await readFile(join(fixture.batchDir, "thumbs/image-2.webp"));
  await rm(join(fixture.batchDir, "thumbs/image-1.webp"));
  const responses = await Promise.all([
    fetch(`${running.url}/media/B001/B001-001/thumb`),
    fetch(`${running.url}/media/B001/B001-001/thumb`),
  ]);
  assert.deepEqual(responses.map((response) => response.status), [200, 200]);
  assert.equal(repairs, 1);
  assert.equal(responses[0].headers.get("content-type"), "image/webp");
});

test("corrupt thumbnail is rebuilt", async (t) => {
  let repairs = 0;
  let validWebp;
  const { fixture, running } = await startFixture(t, {
    thumbnailBuilder: async (_source, output) => {
      repairs += 1;
      await writeFile(output, validWebp);
    },
  });
  validWebp = await readFile(join(fixture.batchDir, "thumbs/image-2.webp"));
  await writeFile(
    join(fixture.batchDir, "thumbs/image-1.webp"),
    Buffer.from("broken"),
  );
  const response = await fetch(
    `${running.url}/media/B001/B001-001/thumb`,
  );
  assert.equal(response.status, 200);
  assert.equal(repairs, 1);
});

test("thumbnail repair failure returns disabled media", async (t) => {
  let repairs = 0;
  const { fixture, running } = await startFixture(t, {
    thumbnailBuilder: async () => {
      repairs += 1;
      throw new Error("thumbnail stderr");
    },
  });
  await rm(join(fixture.batchDir, "thumbs/image-1.webp"));
  const response = await fetch(
    `${running.url}/media/B001/B001-001/thumb`,
  );
  assert.equal(response.status, 404);
  assert.equal((await response.json()).error.code, "media_unavailable");
  assert.equal(repairs, 1);
});

test("invalid immutable PNG prevents thumbnail repair", async (t) => {
  let repairs = 0;
  const { fixture, running } = await startFixture(t, {
    thumbnailBuilder: async () => {
      repairs += 1;
    },
  });
  await rm(join(fixture.batchDir, "thumbs/image-1.webp"));
  await writeFile(
    join(fixture.batchDir, "images/image-1.png"),
    Buffer.from("broken"),
  );
  const response = await fetch(
    `${running.url}/media/B001/B001-001/thumb`,
  );
  assert.equal(response.status, 404);
  assert.equal(repairs, 0);
});

test("hung thumbnail repair times out and removes its partial output", async (t) => {
  let partialOutput;
  let releaseBuilder;
  const { fixture, running } = await startFixture(t, {
    thumbnailRepairTimeoutMs: 40,
    thumbnailBuilder: async (_source, output, { signal } = {}) => {
      partialOutput = output;
      await writeFile(output, Buffer.from("partial"));
      await new Promise((resolve) => {
        releaseBuilder = resolve;
        signal?.addEventListener("abort", resolve, { once: true });
      });
    },
  });
  const finalOutput = join(fixture.batchDir, "thumbs/image-1.webp");
  await rm(finalOutput);

  const request = fetch(
    `${running.url}/media/B001/B001-001/thumb`,
  );
  let response;
  try {
    response = await Promise.race([
      request,
      new Promise((_, reject) => setTimeout(
        () => reject(new Error("thumbnail repair did not time out")),
        500,
      )),
    ]);
  } finally {
    releaseBuilder?.();
    await request.catch(() => undefined);
  }
  assert.equal(response.status, 404);
  assert.equal((await response.json()).error.code, "media_unavailable");
  await assert.rejects(readFile(partialOutput), { code: "ENOENT" });
  await assert.rejects(readFile(finalOutput), { code: "ENOENT" });
});

test("concurrent clients persist different image reviews", async (t) => {
  const { running } = await startFixture(t);
  const update = (id, status) =>
    fetch(`${running.url}/api/batches/B001/reviews/${id}`, {
      method: "PUT",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        expectedRevision: 0,
        status,
        reasons: [],
        note: "",
      }),
    });
  const responses = await Promise.all([
    update("B001-001", "keep"),
    update("B001-002", "favorite"),
  ]);
  assert.deepEqual(responses.map((response) => response.status), [200, 200]);
  const stale = await update("B001-001", "reject");
  assert.equal(stale.status, 409);
  assert.deepEqual(await stale.json(), {
    ok: false,
    error: {
      code: "review_conflict",
      message: "review revision changed; reload this image",
    },
  });
});

test("unknown review image IDs return 404", async (t) => {
  const { running } = await startFixture(t);
  const response = await fetch(
    `${running.url}/api/batches/B001/reviews/B001-999`,
    {
      method: "PUT",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        expectedRevision: 0,
        status: "keep",
        reasons: [],
        note: "",
      }),
    },
  );
  assert.equal(response.status, 404);
});

test("durable review write failures return 500", async (t) => {
  const { fixture, running } = await startFixture(t);
  await mkdir(join(fixture.batchDir, "reviews.json"));
  const response = await fetch(
    `${running.url}/api/batches/B001/reviews/B001-001`,
    {
      method: "PUT",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        expectedRevision: 0,
        status: "keep",
        reasons: [],
        note: "",
      }),
    },
  );
  assert.equal(response.status, 500);
  assert.equal((await response.json()).error.code, "durable_write_failed");
});

test("busy port error names the configured listener", async (t) => {
  const { dataRoot, running } = await startFixture(t);
  const port = Number(new URL(running.url).port);
  await assert.rejects(
    startGalleryServer({
      dataRoot,
      host: "127.0.0.1",
      port,
      allowLoopback: true,
    }),
    new RegExp(`127\\.0\\.0\\.1:${port}`),
  );
});
