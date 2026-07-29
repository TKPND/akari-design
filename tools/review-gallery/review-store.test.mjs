import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import {
  ReviewConflictError,
  ReviewValidationError,
  createReviewStore,
} from "./review-store.mjs";
import { makeValidManifest } from "./test-helpers.mjs";

test("review update persists status reasons and monotonic revision", async () => {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-review-"));
  await mkdir(join(dataRoot, "batches", "B001"), { recursive: true });
  const manifest = makeValidManifest();
  const store = createReviewStore({
    dataRoot,
    clock: () => "2026-07-29T12:00:00.000Z",
  });
  const updated = await store.update(
    "B001",
    manifest,
    "B001-001",
    0,
    { status: "reject", reasons: ["skin-flat"], note: "" },
  );
  assert.equal(updated.revision, 1);
  assert.equal(updated.status, "reject");
  const saved = JSON.parse(
    await readFile(join(dataRoot, "batches/B001/reviews.json"), "utf8"),
  );
  assert.equal(saved.reviews["B001-001"].revision, 1);
});

test("stale revision is rejected", async () => {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-review-"));
  await mkdir(join(dataRoot, "batches", "B001"), { recursive: true });
  const manifest = makeValidManifest();
  const store = createReviewStore({ dataRoot });
  await store.update(
    "B001",
    manifest,
    "B001-001",
    0,
    { status: "keep", reasons: [], note: "" },
  );
  await assert.rejects(
    store.update(
      "B001",
      manifest,
      "B001-001",
      0,
      { status: "favorite", reasons: [], note: "" },
    ),
    ReviewConflictError,
  );
  const loaded = await store.load("B001", manifest);
  assert.equal(loaded.reviews["B001-001"].status, "keep");
  assert.equal(loaded.reviews["B001-001"].revision, 1);
});

test("different image updates are serialized without loss", async () => {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-review-"));
  await mkdir(join(dataRoot, "batches", "B001"), { recursive: true });
  const manifest = makeValidManifest();
  const store = createReviewStore({ dataRoot });
  await Promise.all([
    store.update("B001", manifest, "B001-001", 0, {
      status: "keep", reasons: [], note: "",
    }),
    store.update("B001", manifest, "B001-002", 0, {
      status: "favorite", reasons: [], note: "",
    }),
  ]);
  const saved = await store.load("B001", manifest);
  assert.equal(saved.reviews["B001-001"].status, "keep");
  assert.equal(saved.reviews["B001-002"].status, "favorite");
});

test("corrupt primary is restored from valid backup", async () => {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-review-"));
  const batchDir = join(dataRoot, "batches", "B001");
  await mkdir(batchDir, { recursive: true });
  const manifest = makeValidManifest();
  const store = createReviewStore({ dataRoot });
  await store.update("B001", manifest, "B001-001", 0, {
    status: "keep", reasons: [], note: "",
  });
  await store.update("B001", manifest, "B001-001", 1, {
    status: "favorite", reasons: [], note: "",
  });
  await writeFile(join(batchDir, "reviews.json"), "{broken", "utf8");
  const recovered = await store.load("B001", manifest);
  assert.equal(recovered.reviews["B001-001"].status, "keep");
  const restoredText = await readFile(
    join(batchDir, "reviews.json"),
    "utf8",
  );
  assert.doesNotThrow(() => JSON.parse(restoredText));
});

test("review reasons are allowed only for reject", async () => {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-review-"));
  await mkdir(join(dataRoot, "batches", "B001"), { recursive: true });
  const store = createReviewStore({ dataRoot });
  await assert.rejects(
    store.update("B001", makeValidManifest(), "B001-001", 0, {
      status: "keep",
      reasons: ["skin-flat"],
      note: "",
    }),
    ReviewValidationError,
  );
});

test("note is trimmed and capped at 1,000 Unicode code points", async () => {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-review-"));
  const store = createReviewStore({ dataRoot });
  const updated = await store.update(
    "B001",
    makeValidManifest(),
    "B001-001",
    0,
    { status: "keep", reasons: [], note: `  ${"😀".repeat(1_001)}  ` },
  );
  assert.equal(Array.from(updated.note).length, 1_000);
  assert.equal(updated.note, "😀".repeat(1_000));
});

test("a failed queued update does not block a later update", async () => {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-review-"));
  const store = createReviewStore({ dataRoot });
  const manifest = makeValidManifest();
  await assert.rejects(
    store.update("B001", manifest, "B001-001", 0, {
      status: "keep", reasons: ["skin-flat"], note: "",
    }),
    ReviewValidationError,
  );
  const updated = await store.update("B001", manifest, "B001-001", 0, {
    status: "keep", reasons: [], note: "",
  });
  assert.equal(updated.revision, 1);
});

test("load rejects stored documents with IDs outside the manifest", async () => {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-review-"));
  const batchDir = join(dataRoot, "batches", "B001");
  await mkdir(batchDir, { recursive: true });
  const manifest = makeValidManifest();
  const reviews = Object.fromEntries(manifest.entries.map(({ id }) => [id, {
    status: "unreviewed",
    reasons: [],
    note: "",
    revision: 0,
    updatedAt: null,
  }]));
  reviews["B001-999"] = { ...reviews["B001-001"] };
  await writeFile(
    join(batchDir, "reviews.json"),
    JSON.stringify({ schemaVersion: 1, batchId: "B001", reviews }),
    "utf8",
  );
  const loaded = await createReviewStore({ dataRoot }).load("B001", manifest);
  assert.equal(loaded.reviews["B001-999"], undefined);
  assert.equal(loaded.reviews["B001-001"].status, "unreviewed");
});
