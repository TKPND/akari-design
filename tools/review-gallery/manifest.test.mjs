import assert from "node:assert/strict";
import test from "node:test";
import {
  LANES,
  ManifestValidationError,
  noveltyKey,
  validateBatchManifest,
} from "./manifest.mjs";
import { makeValidManifest } from "./test-helpers.mjs";

test("production manifest has fifty entries and five per lane", () => {
  const manifest = validateBatchManifest(makeValidManifest());
  assert.equal(manifest.entries.length, 50);
  for (const lane of LANES) {
    assert.equal(
      manifest.entries.filter((entry) => entry.lane === lane).length,
      5,
      lane,
    );
  }
});

test("production manifest requires ten texture slots", () => {
  const invalid = makeValidManifest();
  invalid.entries[0].textureFocus = false;
  assert.throws(
    () => validateBatchManifest(invalid),
    (error) =>
      error instanceof ManifestValidationError &&
      /exactly 10 texture-focus entries/.test(error.message),
  );
});

test("novelty key changes when a primary axis changes", () => {
  const [entry] = makeValidManifest().entries;
  const changed = structuredClone(entry);
  changed.camera = "ground-level three-quarter";
  assert.notEqual(noveltyKey(entry), noveltyKey(changed));
});

const cases = [
  ["duplicate image id", (m) => { m.entries[1].id = m.entries[0].id; }],
  ["duplicate novelty combination", (m) => {
    const id = m.entries[1].id;
    const artifact = m.entries[1].artifact;
    m.entries[1] = structuredClone(m.entries[0]);
    m.entries[1].id = id;
    m.entries[1].artifact = artifact;
  }],
  ["fewer than two references", (m) => { m.entries[0].references.length = 1; }],
  ["more than four references", (m) => {
    m.entries[0].references.push(
      structuredClone(m.entries[0].references[0]),
      structuredClone(m.entries[0].references[1]),
      structuredClone(m.entries[0].references[0]),
    );
  }],
  ["absolute media path", (m) => {
    m.entries[0].artifact.imagePath = "/etc/passwd";
  }],
  ["path traversal", (m) => {
    m.entries[0].artifact.thumbnailPath = "../outside.webp";
  }],
];

for (const [name, mutate] of cases) {
  test(name, () => {
    const invalid = makeValidManifest();
    mutate(invalid);
    assert.throws(
      () => validateBatchManifest(invalid),
      ManifestValidationError,
    );
  });
}

test("valid generation metadata is required", () => {
  const invalid = makeValidManifest();
  invalid.entries[0].generation.technicalStatus = "finished";
  assert.throws(
    () => validateBatchManifest(invalid),
    /invalid generation metadata/,
  );
});
