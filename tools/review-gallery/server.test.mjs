import assert from "node:assert/strict";
import {
  mkdtemp,
  mkdir,
  readFile,
  rm,
  writeFile,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import {
  assertSafeBindHost,
  startGalleryServer,
} from "./server.mjs";
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

test("missing thumbnail is rebuilt once", async (t) => {
  let repairs = 0;
  let validWebp;
  const { fixture, running } = await startFixture(t, {
    thumbnailBuilder: async (source, output) => {
      repairs += 1;
      assert.equal(source, join(fixture.batchDir, "images/image-1.png"));
      assert.equal(output, join(fixture.batchDir, "thumbs/image-1.webp"));
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
