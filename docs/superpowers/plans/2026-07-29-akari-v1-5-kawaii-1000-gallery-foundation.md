# Akari v1.5 Kawaii 1000 Gallery Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and live-verify the manifest, thumbnail, review, browser, and Tailscale service foundation required before generating Akari v1.5 Kawaii 1000 batch B001.

**Architecture:** A dependency-light Node service validates batch manifests, serves allowlisted thumbnails and PNG files, and atomically persists reviews. Small Python tools initialize the external data root, snapshot references, validate PNGs, build WebP thumbnails, and create a non-counting B000 demo batch. A generated `systemd --user` unit binds the service only to the configured Tailscale IPv4.

**Tech Stack:** Node.js 26 ESM, built-in `node:http` and `node:test`, plain HTML/CSS/JavaScript, Playwright, Python 3.11+, Pillow, `unittest`, `systemd --user`, Tailscale.

## Global Constraints

- The canonical design is `docs/superpowers/specs/2026-07-29-akari-v1-5-kawaii-1000-generation-gallery-design.md`.
- This foundation plan performs no built-in `image_gen` calls and consumes no entries from the 1,000-image count.
- Generated images, demo images, thumbnails, manifests, and reviews stay outside Git under the configured data root.
- The live default data root is `/home/takahiro/workspace/akari_generated/v1.5-1000`.
- The live default bind is `100.125.117.75:8787`; never fall back to `0.0.0.0` or `::`.
- The gallery may read only a configured data root and may serve only manifest-declared media.
- Source PNG files are immutable; the gallery writes review JSON only.
- Browser actions never start image generation, modify prompts, delete images, or promote assets.
- Review states are exactly `unreviewed`, `reject`, `keep`, and `favorite`.
- Every production batch contains exactly fifty entries and exactly five entries from each of the ten lanes.
- Every production batch contains exactly ten texture-focus entries and exactly five `subculture-wildcard` entries.
- Every production batch contains exactly thirty-five solo, ten viewer-POV or
  two-person, and five group entries.
- Every production batch contains exactly forty action/reaction scenes and ten
  quiet posed scenes.
- A request uses at least the two permanent authorities and no more than four references.
- `~/neesocks.jpeg` is snapshotted outside Git and used only for anatomy and pressure principles.
- All Node tests run serially.
- Do not run PDF builds, Poppler, OCR, Tesseract, or release audits for this work.
- Use `bash -lc` for npm commands when shell PATH initialization is required.
- Keep the foundation gate serial on the 3-core, 2 GiB host.

## Scope Boundary

This plan ends with a live, persistent B000 demo gallery and a passing
foundation gate. A follow-up implementation plan will define the exact B001
fifty-request manifest and execute fifty independent built-in `image_gen`
calls. Later batches reuse the same generation runbook after each browser
review.

## File Structure

Create these focused units:

```text
tools/review-gallery/
├── manifest.mjs
├── manifest.test.mjs
├── review-store.mjs
├── review-store.test.mjs
├── server.mjs
├── server.test.mjs
├── browser.test.mjs
├── test-helpers.mjs
└── public/
    ├── index.html
    ├── styles.css
    └── app.js

scripts/
├── init_akari_v1_5_kawaii_1000.py
├── build_akari_review_thumbnail.py
├── create_akari_review_demo.py
└── install_akari_review_gallery_service.py

tests/
├── test_init_akari_v1_5_kawaii_1000.py
├── test_build_akari_review_thumbnail.py
├── test_create_akari_review_demo.py
└── test_install_akari_review_gallery_service.py

docs/
└── akari-v1.5-kawaii-1000-gallery-runbook.md
```

Responsibility boundaries:

- `manifest.mjs` owns manifest constants, structural validation, quotas, media
  allowlisting, and novelty-key calculation.
- `review-store.mjs` owns review validation, revision conflicts, serialized
  writes, atomic replacement, and backup recovery.
- `server.mjs` owns safe binding, HTTP routing, static assets, API responses,
  and manifest-declared media lookup.
- `public/` owns browser interaction and contains no filesystem logic.
- `init_akari_v1_5_kawaii_1000.py` owns external directory creation and
  immutable reference snapshots.
- `build_akari_review_thumbnail.py` owns technical PNG validation and thumbnail
  derivation.
- `create_akari_review_demo.py` owns disposable B000 demo data only.
- `install_akari_review_gallery_service.py` owns systemd unit rendering and
  installation; no local absolute path is committed in a unit template.

---

### Task 1: Batch Manifest Contract

**Files:**

- Create: `tools/review-gallery/manifest.mjs`
- Create: `tools/review-gallery/manifest.test.mjs`
- Create: `tools/review-gallery/test-helpers.mjs`

**Interfaces:**

- Consumes: JSON-compatible manifest objects.
- Produces: `LANES`, `validateBatchManifest(manifest, options)`,
  `noveltyKey(entry)`, `declaredMedia(manifest)`, and
  `makeValidManifest(overrides)` for tests.
- `validateBatchManifest` returns a frozen normalized manifest and throws
  `ManifestValidationError` with a stable message on the first violation.

- [ ] **Step 1: Write the valid-manifest and quota tests**

Create `tools/review-gallery/manifest.test.mjs` with these first tests:

```js
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
node --test --test-concurrency=1 tools/review-gallery/manifest.test.mjs
```

Expected: FAIL with `ERR_MODULE_NOT_FOUND` for `manifest.mjs`.

- [ ] **Step 3: Implement constants and core validation**

Create `tools/review-gallery/manifest.mjs` with these exported values and
signatures:

```js
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { isAbsolute, relative, resolve } from "node:path";

export const LANES = Object.freeze([
  "classic-school-uniform",
  "professional-service-uniform",
  "sports-ceremony-fictional-uniform",
  "everyday-girly",
  "outings-special-days",
  "hobbies-making",
  "travel-walking",
  "retro-storybook",
  "magic-fantasy-sf",
  "subculture-wildcard",
]);

export const REVIEW_STATUSES = Object.freeze([
  "unreviewed",
  "reject",
  "keep",
  "favorite",
]);

export class ManifestValidationError extends Error {}

const noveltyFields = Object.freeze([
  "lane",
  "wardrobeFamily",
  "setting",
  "action",
  "sceneMode",
  "composition",
  "camera",
  "lighting",
  "cuteBeat",
  "cast",
  "dominantColor",
  "textureType",
]);

export function noveltyKey(entry) {
  return noveltyFields.map((field) => String(entry[field] ?? "")).join("\u241f");
}
```

Implement `validateBatchManifest(manifest, { dataRoot, checkFiles = false } =
{})` as an ordered validator. Clone before validation, reject non-objects, and
apply these exact rules and stable message fragments:

| Rule | Stable message fragment |
| --- | --- |
| `schemaVersion === 1` | `schemaVersion must be 1` |
| `batchType` is `production` or `demo` | `invalid batchType` |
| `batchId` matches `/^B\d{3}$/` | `invalid batchId` |
| `entries` contains exactly 50 objects | `exactly 50 entries` |
| each ID matches `${batchId}-NNN` and is unique | `invalid image id` / `duplicate image id` |
| each lane is in `LANES` and appears exactly five times | `exactly 5 entries per lane` |
| ten entries have `textureFocus === true` | `exactly 10 texture-focus entries` |
| five entries have `subculture === true`, all in the wildcard lane | `exactly 5 subculture entries` |
| cast values contain 35 solo, 10 viewer-POV/two-person, and 5 group entries | `invalid cast quota` |
| scene mode contains 40 `action-reaction` and 10 `quiet-posed` entries | `invalid scene mode quota` |
| prompt and all novelty fields are non-empty strings | `missing prompt or novelty field` |
| each entry has two through four references | `two to four references` |
| reference path and role are non-empty; exclusions is a string array | `invalid reference metadata` |
| each reference SHA-256 matches `/^[a-f0-9]{64}$/` | `invalid reference sha256` |
| image path ends in `.png`; thumbnail path ends in `.webp` | `invalid artifact extension` |
| media paths are relative and remain below `dataRoot` after `resolve` | `unsafe artifact path` |
| every novelty key is unique | `duplicate novelty combination` |
| generation metadata has a known mode and technical status | `invalid generation metadata` |

Require `dataRoot` when `checkFiles` is true. In that mode, call `existsSync`
for every resolved reference, image, and thumbnail path and fail with
`declared file missing`. Hash each reference with
`createHash("sha256").update(readFileSync(path)).digest("hex")` and compare it
with the declared value. When the artifact SHA-256 is non-null, hash the PNG
and compare that value too. Use `relative(dataRoot, resolvedPath)` for the
containment check and reject a result that is `..`, starts with `../`, or is
absolute. When no data root is supplied, reject absolute paths, empty segments,
`.` segments, and `..` segments lexically. Freeze the cloned manifest, every
entry, each reference array, each generation object, and each artifact object
before returning it.

Each entry has this generation shape from the dry run onward:

```json
{
  "generation": {
    "toolMode": "built-in-imagegen",
    "generationId": null,
    "requestId": null,
    "sourcePath": null,
    "technicalStatus": "pending",
    "failureReason": null
  }
}
```

For B000, `toolMode` is `demo`; otherwise it is
`built-in-imagegen`. `technicalStatus` is one of `pending`, `valid`, or
`failed`. IDs and paths are null until exposed or saved. A `valid` entry
requires non-null artifact SHA-256, width, and height. This leaves recovery and
counting metadata ready for the separate B001 implementation plan without
performing generation in this plan.

Implement `declaredMedia(manifest)` by validating the manifest and returning a
map with exactly two keys per entry:

```js
return new Map(
  normalized.entries.flatMap((entry) => [
    [`${entry.id}:image`, entry.artifact.imagePath],
    [`${entry.id}:thumb`, entry.artifact.thumbnailPath],
  ]),
);
```

Both production and demo batches obey the fifty-entry, lane, texture, and
subculture rules. Only `batchType: "production"` is eligible for the project
count; the validator does not itself increment any count.

- [ ] **Step 4: Implement the deterministic test factory**

Create `tools/review-gallery/test-helpers.mjs`:

```js
import { LANES } from "./manifest.mjs";

export function makeValidManifest(overrides = {}) {
  const entries = LANES.flatMap((lane, laneIndex) =>
    Array.from({ length: 5 }, (_, offset) => {
      const ordinal = laneIndex * 5 + offset + 1;
      return {
        id: `B001-${String(ordinal).padStart(3, "0")}`,
        lane,
        cuteBeat: `beat-${laneIndex}-${offset}`,
        wardrobeFamily: `wardrobe-${laneIndex}-${offset}`,
        setting: `setting-${laneIndex}-${offset}`,
        action: `action-${laneIndex}-${offset}`,
        sceneMode: ordinal <= 40 ? "action-reaction" : "quiet-posed",
        composition: `composition-${laneIndex}-${offset}`,
        camera: `camera-${laneIndex}-${offset}`,
        lighting: `lighting-${laneIndex}-${offset}`,
        cast: ordinal <= 35
          ? "solo"
          : ordinal <= 45
            ? "viewer-pov"
            : "group",
        dominantColor: `color-${laneIndex}-${offset}`,
        textureFocus: ordinal <= 10,
        textureType: ordinal <= 10 ? `texture-${ordinal}` : "none",
        subculture: lane === "subculture-wildcard",
        prompt: `Independent Akari request ${ordinal}`,
        references: [
          {
            path: "references/akari-v1.5-b3-body-balance.png",
            role: "v1.5 identity and body balance",
            exclusions: ["outfit", "pose", "background"],
            sha256: "a".repeat(64),
          },
          {
            path: "references/akari-v1.4-g2-balanced-lines.png",
            role: "rendering and skin authority",
            exclusions: ["body balance", "pose", "background"],
            sha256: "b".repeat(64),
          },
        ],
        generation: {
          toolMode: "built-in-imagegen",
          generationId: null,
          requestId: null,
          sourcePath: null,
          technicalStatus: "pending",
          failureReason: null,
        },
        artifact: {
          imagePath: `batches/B001/images/image-${ordinal}.png`,
          thumbnailPath: `batches/B001/thumbs/image-${ordinal}.webp`,
          sha256: null,
          width: null,
          height: null,
        },
      };
    }),
  );
  return {
    schemaVersion: 1,
    batchType: "production",
    batchId: "B001",
    title: "Akari v1.5 Kawaii 1000 B001",
    entries,
    ...overrides,
  };
}
```

- [ ] **Step 5: Add failure tests for every contract boundary**

Add table-driven tests that mutate one valid manifest at a time and assert
stable failure messages for:

```js
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
```

- [ ] **Step 6: Run the manifest tests**

Run:

```bash
node --test --test-concurrency=1 tools/review-gallery/manifest.test.mjs
```

Expected: all manifest tests PASS.

- [ ] **Step 7: Commit the manifest contract**

```bash
git add tools/review-gallery/manifest.mjs \
  tools/review-gallery/manifest.test.mjs \
  tools/review-gallery/test-helpers.mjs
git commit -m "Add Akari review manifest contract"
```

### Task 2: External Data Root and Reference Snapshot

**Files:**

- Create: `scripts/init_akari_v1_5_kawaii_1000.py`
- Create: `tests/test_init_akari_v1_5_kawaii_1000.py`

**Interfaces:**

- Consumes: repository root, external data root, and texture reference path.
- Produces: `initialize_data_root(repo_root, data_root, texture_reference) ->
  Path`, immutable copied references, `references/manifest.json`, and
  `state/novelty-ledger.json`.

- [ ] **Step 1: Write the initialization tests**

Create `tests/test_init_akari_v1_5_kawaii_1000.py`:

```python
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.init_akari_v1_5_kawaii_1000 import initialize_data_root


class InitializeAkariKawaii1000Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.data = self.root / "data"
        self._image(
            self.repo
            / "akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png",
            "#d6c0aa",
        )
        self._image(
            self.repo
            / "akari-v1.4/style-tests/line-refinement/"
            "akari-v14-g2-balanced-lines.png",
            "#c59d80",
        )
        self._image(
            self.repo
            / "akari-v1.4/style-tests/reproducibility-i-seated/"
            "akari-v14-i2-chair-seated-repro.png",
            "#b9a38f",
        )
        self._image(
            self.repo
            / "akari-v1.4/style-tests/reproducibility-j-action/"
            "akari-v14-j1-mandarin-action-repro.png",
            "#d8a45a",
        )
        self.texture = self.root / "neesocks.jpeg"
        Image.new("RGB", (16, 16), "#dddddd").save(self.texture, "JPEG")

    def _image(self, path: Path, color: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (16, 24), color).save(path, "PNG")

    def test_initialization_copies_references_and_records_hashes(self):
        result = initialize_data_root(self.repo, self.data, self.texture)
        manifest = json.loads(
            (result / "references/manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(5, len(manifest["references"]))
        self.assertTrue(
            all(len(item["sha256"]) == 64 for item in manifest["references"])
        )
        self.assertTrue((result / "state/novelty-ledger.json").is_file())

    def test_initialization_refuses_changed_existing_reference(self):
        initialize_data_root(self.repo, self.data, self.texture)
        copied = self.data / "references/akari-v1.5-b3-body-balance.png"
        copied.write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "reference snapshot mismatch"):
            initialize_data_root(self.repo, self.data, self.texture)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
uv run python -m unittest \
  tests.test_init_akari_v1_5_kawaii_1000 -v
```

Expected: FAIL with an import error for the missing script.

- [ ] **Step 3: Implement initialization**

Create `scripts/init_akari_v1_5_kawaii_1000.py` with:

```python
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path


REFERENCE_SOURCES = (
    (
        "v1.5-body-balance",
        Path("akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png"),
        "akari-v1.5-b3-body-balance.png",
    ),
    (
        "v1.4-rendering",
        Path(
            "akari-v1.4/style-tests/line-refinement/"
            "akari-v14-g2-balanced-lines.png"
        ),
        "akari-v1.4-g2-balanced-lines.png",
    ),
    (
        "v1.4-seated",
        Path(
            "akari-v1.4/style-tests/reproducibility-i-seated/"
            "akari-v14-i2-chair-seated-repro.png"
        ),
        "akari-v1.4-i2-seated.png",
    ),
    (
        "v1.4-action",
        Path(
            "akari-v1.4/style-tests/reproducibility-j-action/"
            "akari-v14-j1-mandarin-action-repro.png"
        ),
        "akari-v1.4-j1-action.png",
    ),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
```

Implement `initialize_data_root(repo_root, data_root, texture_reference) ->
Path` with this exact sequence:

1. Resolve all three paths and require the four repository sources plus the
   texture reference to be regular files.
2. Create `references/`, `state/`, and `batches/` below `data_root`.
3. For each source, calculate SHA-256 before copying. Copy to its fixed
   destination only when absent. When present, compare hashes and raise
   `ValueError("reference snapshot mismatch: <destination>")` on any change.
4. Write `references/manifest.json` atomically as schema version 1 with source
   role, original path, snapshot-relative path, SHA-256, and exclusions.
5. Create `state/novelty-ledger.json` only when absent with:

   ```json
   {
     "schemaVersion": 1,
     "acceptedProductionImages": 0,
     "technicalFailures": 0,
     "entries": []
   }
   ```

6. Return the resolved data-root path. Never rewrite an existing novelty
   ledger.

The reference manifest uses this exact shape:

```json
{
  "schemaVersion": 1,
  "references": [
    {
      "id": "v1.5-body-balance",
      "role": "v1.5 identity and body balance",
      "sourcePath": "/absolute/source.png",
      "snapshotPath": "references/akari-v1.5-b3-body-balance.png",
      "sha256": "64 lowercase hex characters",
      "exclusions": ["outfit", "pose", "background"]
    }
  ]
}
```

Complete the initializer with:

```python
REFERENCE_METADATA = {
    "v1.5-body-balance": (
        "v1.5 identity and body balance",
        ["outfit", "pose", "background"],
    ),
    "v1.4-rendering": (
        "rendering and skin authority",
        ["body balance", "pose", "background"],
    ),
    "v1.4-seated": (
        "seated anatomy and weight distribution",
        ["identity", "outfit", "background"],
    ),
    "v1.4-action": (
        "hands and action continuity",
        ["identity", "outfit", "background"],
    ),
    "neesocks-pressure-study": (
        "anatomy and hosiery pressure only",
        ["identity", "composition", "underwear", "outfit", "color"],
    ),
}


def _atomic_json(path: Path, value: object) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _snapshot(source: Path, destination: Path) -> str:
    source_hash = sha256_file(source)
    if destination.exists():
        if sha256_file(destination) != source_hash:
            raise ValueError(f"reference snapshot mismatch: {destination}")
        return source_hash
    temporary = destination.with_name(
        f".{destination.name}.{os.getpid()}.tmp"
    )
    shutil.copyfile(source, temporary)
    os.replace(temporary, destination)
    return source_hash


def initialize_data_root(
    repo_root: Path,
    data_root: Path,
    texture_reference: Path,
) -> Path:
    repo_root = repo_root.resolve()
    data_root = data_root.resolve()
    texture_reference = texture_reference.resolve()
    references_dir = data_root / "references"
    references_dir.mkdir(parents=True, exist_ok=True)
    (data_root / "state").mkdir(exist_ok=True)
    (data_root / "batches").mkdir(exist_ok=True)
    sources = [
        (item_id, repo_root / relative_source, destination_name)
        for item_id, relative_source, destination_name in REFERENCE_SOURCES
    ]
    sources.append(
        (
            "neesocks-pressure-study",
            texture_reference,
            "neesocks-pressure-study.jpeg",
        )
    )
    records = []
    for item_id, source, destination_name in sources:
        if not source.is_file():
            raise FileNotFoundError(source)
        destination = references_dir / destination_name
        digest = _snapshot(source, destination)
        role, exclusions = REFERENCE_METADATA[item_id]
        records.append({
            "id": item_id,
            "role": role,
            "sourcePath": str(source),
            "snapshotPath": f"references/{destination_name}",
            "sha256": digest,
            "exclusions": exclusions,
        })
    _atomic_json(
        references_dir / "manifest.json",
        {"schemaVersion": 1, "references": records},
    )
    ledger = data_root / "state/novelty-ledger.json"
    if not ledger.exists():
        _atomic_json(
            ledger,
            {
                "schemaVersion": 1,
                "acceptedProductionImages": 0,
                "technicalFailures": 0,
                "entries": [],
            },
        )
    return data_root
```

The reference manifest must label the texture copy
`neesocks-pressure-study.jpeg` with role
`anatomy and hosiery pressure only` and exclusions
`identity`, `composition`, `underwear`, `outfit`, and `color`.

Add a CLI:

```bash
uv run python scripts/init_akari_v1_5_kawaii_1000.py \
  --repo-root /home/takahiro/workspace/akari-design \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --texture-reference /home/takahiro/neesocks.jpeg
```

- [ ] **Step 4: Run the unit tests**

Run:

```bash
uv run python -m unittest \
  tests.test_init_akari_v1_5_kawaii_1000 -v
```

Expected: both tests PASS.

- [ ] **Step 5: Initialize the real external data root**

Run the exact CLI above. Then verify:

```bash
find /home/takahiro/workspace/akari_generated/v1.5-1000 \
  -maxdepth 2 -type f -print | sort
```

Expected: five reference copies, `references/manifest.json`, and
`state/novelty-ledger.json`. No file appears in `git status --short`.

- [ ] **Step 6: Commit the initializer**

```bash
git add scripts/init_akari_v1_5_kawaii_1000.py \
  tests/test_init_akari_v1_5_kawaii_1000.py
git commit -m "Add Akari Kawaii 1000 data initializer"
```

### Task 3: PNG Validation and Thumbnail Derivation

**Files:**

- Create: `scripts/build_akari_review_thumbnail.py`
- Create: `tests/test_build_akari_review_thumbnail.py`

**Interfaces:**

- Consumes: one PNG path and one WebP output path.
- Produces: `inspect_png(source) -> dict[str, object]` and
  `build_thumbnail(source, output, max_edge=512) -> Path`.

- [ ] **Step 1: Write technical validation tests**

Create `tests/test_build_akari_review_thumbnail.py`:

```python
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.build_akari_review_thumbnail import (
    PNG_SIGNATURE,
    build_thumbnail,
    inspect_png,
)


class ReviewThumbnailTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_thumbnail_preserves_ratio_and_limits_long_edge(self):
        source = self.root / "source.png"
        Image.new("RGB", (1024, 1536), "#d9b6a0").save(source)
        output = build_thumbnail(source, self.root / "thumb.webp")
        with Image.open(output) as image:
            self.assertEqual((341, 512), image.size)
            self.assertEqual("WEBP", image.format)

    def test_inspect_png_rejects_non_png_signature(self):
        source = self.root / "fake.png"
        source.write_bytes(b"not a png")
        with self.assertRaisesRegex(ValueError, "invalid PNG signature"):
            inspect_png(source)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
uv run python -m unittest \
  tests.test_build_akari_review_thumbnail -v
```

Expected: FAIL with a missing module import.

- [ ] **Step 3: Implement inspection and thumbnail generation**

Create `scripts/build_akari_review_thumbnail.py`:

```python
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from PIL import Image


PNG_SIGNATURE = bytes.fromhex("89504e470d0a1a0a")


def inspect_png(source: Path) -> dict[str, object]:
    if source.read_bytes()[:8] != PNG_SIGNATURE:
        raise ValueError(f"invalid PNG signature: {source}")
    with Image.open(source) as image:
        image.verify()
    with Image.open(source) as image:
        width, height = image.size
        mode = image.mode
    return {
        "width": width,
        "height": height,
        "mode": mode,
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    }


def build_thumbnail(source: Path, output: Path, max_edge: int = 512) -> Path:
    inspect_png(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        converted = image.convert("RGB")
        converted.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
        converted.save(output, "WEBP", quality=82, method=6)
    return output
```

Add a CLI accepting `--input`, `--output`, and `--max-edge`.

- [ ] **Step 4: Add damaged-image and alpha-image tests**

Add:

```python
def test_inspect_png_rejects_truncated_png(self):
    source = self.root / "truncated.png"
    source.write_bytes(PNG_SIGNATURE + b"broken")
    with self.assertRaises((OSError, SyntaxError, ValueError)):
        inspect_png(source)

def test_rgba_source_builds_rgb_webp_without_source_change(self):
    source = self.root / "alpha.png"
    Image.new("RGBA", (40, 60), (220, 180, 160, 128)).save(source)
    before = source.read_bytes()
    output = build_thumbnail(source, self.root / "alpha.webp")
    self.assertEqual(before, source.read_bytes())
    with Image.open(output) as image:
        self.assertEqual("RGB", image.mode)
        self.assertEqual("WEBP", image.format)
```

- [ ] **Step 5: Run the tests**

Run:

```bash
uv run python -m unittest \
  tests.test_build_akari_review_thumbnail -v
```

Expected: all thumbnail tests PASS.

- [ ] **Step 6: Commit technical image validation**

```bash
git add scripts/build_akari_review_thumbnail.py \
  tests/test_build_akari_review_thumbnail.py
git commit -m "Add review thumbnail validation"
```

### Task 4: Atomic Review Store

**Files:**

- Create: `tools/review-gallery/review-store.mjs`
- Create: `tools/review-gallery/review-store.test.mjs`

**Interfaces:**

- Consumes: data root, validated manifest, image ID, expected revision, and a
  review patch.
- Produces: `createReviewStore({ dataRoot, clock })` with
  `load(batchId, manifest)` and
  `update(batchId, manifest, imageId, expectedRevision, patch)`.
- Throws `ReviewConflictError` on stale revisions and `ReviewValidationError`
  on invalid states or reasons.

- [ ] **Step 1: Write persistence and revision tests**

Create `tools/review-gallery/review-store.test.mjs`:

```js
import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile } from "node:fs/promises";
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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
node --test --test-concurrency=1 \
  tools/review-gallery/review-store.test.mjs
```

Expected: FAIL with a missing module import.

- [ ] **Step 3: Implement review validation and atomic writes**

Create `tools/review-gallery/review-store.mjs` with:

```js
import { copyFile, mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { randomUUID } from "node:crypto";
import { join } from "node:path";
import { REVIEW_STATUSES } from "./manifest.mjs";

export const REJECT_REASONS = Object.freeze([
  "identity-drift",
  "age-drift",
  "not-cute",
  "duplicate",
  "anatomy",
  "hands",
  "composition",
  "garment",
  "artifact",
  "skin-flat",
  "skin-plastic",
  "compression-missing",
  "compression-excessive",
  "sock-painted-on",
  "tissue-anatomy",
  "fabric-texture-weak",
]);

export class ReviewConflictError extends Error {}
export class ReviewValidationError extends Error {}
```

Implement `createReviewStore({ dataRoot, clock = () => new
Date().toISOString() })` with a `Map` of per-batch promise tails. `load` returns
this exact document when neither a valid primary nor valid backup exists:

```json
{
  "schemaVersion": 1,
  "batchId": "B001",
  "reviews": {
    "B001-001": {
      "status": "unreviewed",
      "reasons": [],
      "note": "",
      "revision": 0,
      "updatedAt": null
    }
  }
}
```

Create one entry for every manifest ID. A stored document is valid only when
its schema and batch ID match, it contains exactly the manifest IDs, all
statuses are in `REVIEW_STATUSES`, revisions are non-negative integers,
reasons are in `REJECT_REASONS`, and timestamps are null or strings.

`update` must append its work to the batch promise tail, then:

1. load the latest valid document;
2. reject an unknown image ID;
3. require `expectedRevision` to equal the stored revision;
4. validate status, reasons, and note;
5. reject reasons unless status is `reject`;
6. trim the note and cap it at 1,000 Unicode code points;
7. replace the selected record with revision plus one and `clock()` time;
8. copy a valid primary file to `reviews.json.bak` when it exists;
9. write formatted JSON to
   `reviews.json.<process.pid>.<randomUUID()>.tmp`;
10. atomically rename the temporary file to `reviews.json`;
11. return the updated record.

If the primary file is malformed and `.bak` is valid, restore the primary from
the backup before returning. Never accept unknown manifest IDs. Ensure a
failed queued operation cannot poison the next operation by storing a tail
that catches its predecessor before running.

- [ ] **Step 4: Add serialization and backup tests**

Add `writeFile` to the `node:fs/promises` test import, then add:

```js
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
```

- [ ] **Step 5: Run review-store tests**

Run:

```bash
node --test --test-concurrency=1 \
  tools/review-gallery/review-store.test.mjs
```

Expected: all review-store tests PASS.

- [ ] **Step 6: Commit the review store**

```bash
git add tools/review-gallery/review-store.mjs \
  tools/review-gallery/review-store.test.mjs
git commit -m "Add atomic Akari review storage"
```

### Task 5: Tailscale-Safe HTTP API and Media Allowlist

**Files:**

- Create: `tools/review-gallery/server.mjs`
- Create: `tools/review-gallery/server.test.mjs`
- Modify: `tools/review-gallery/test-helpers.mjs`

**Interfaces:**

- Consumes: `dataRoot`, `host`, `port`, `repoRoot`, `pythonExecutable`, and
  optional test-only `allowLoopback` and `thumbnailBuilder`.
- Produces: `assertSafeBindHost(host, options)`,
  `createGalleryServer(options)`, and `startGalleryServer(options)`.
- HTTP API:
  - `GET /api/batches`
  - `GET /api/batches/:batchId`
  - `GET /api/batches/:batchId/reviews`
  - `PUT /api/batches/:batchId/reviews/:imageId`
  - `GET /media/:batchId/:imageId/image`
  - `GET /media/:batchId/:imageId/thumb`

- [ ] **Step 1: Write safe-bind and API tests**

Create `tools/review-gallery/server.test.mjs`:

```js
import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import {
  assertSafeBindHost,
  startGalleryServer,
} from "./server.mjs";
import { createDemoFixture } from "./test-helpers.mjs";

test("public wildcard hosts are always rejected", () => {
  assert.throws(() => assertSafeBindHost("0.0.0.0"), /public bind forbidden/);
  assert.throws(() => assertSafeBindHost("::"), /public bind forbidden/);
});

test("non-Tailscale IPv4 is rejected", () => {
  assert.throws(
    () => assertSafeBindHost("192.168.1.20"),
    /Tailscale IPv4 required/,
  );
});

test("API returns a validated batch and review progress", async (t) => {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-server-"));
  await createDemoFixture(dataRoot);
  const running = await startGalleryServer({
    dataRoot,
    host: "127.0.0.1",
    port: 0,
    allowLoopback: true,
  });
  t.after(() => running.close());
  const response = await fetch(`${running.url}/api/batches/B001`);
  assert.equal(response.status, 200);
  const payload = await response.json();
  assert.equal(payload.ok, true);
  assert.equal(payload.data.entries.length, 50);
});
```

Extend `test-helpers.mjs` with
`createDemoFixture(dataRoot, { batchId = "B001" } = {})`. It must call
`makeValidManifest`, replace every entry ID and artifact path when `batchId`
differs, create `batches/<batchId>/{images,thumbs}`, write the manifest, and
write valid one-pixel PNG and WebP fixture bytes for all fifty declared media
paths. It must also create the two declared reference files and replace their
factory SHA-256 values with the real fixture hashes. Do not import Pillow or
invoke a subprocess from Node tests. Return `{ manifest, batchDir }`.

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
node --test --test-concurrency=1 tools/review-gallery/server.test.mjs
```

Expected: FAIL with a missing module import.

- [ ] **Step 3: Implement bind validation**

In `server.mjs`, convert IPv4 octets to a 32-bit integer and accept production
hosts only in `100.64.0.0/10`. Also require the host to appear in
`os.networkInterfaces()` unless the test-only `interfaceAddresses` option is
supplied. Always reject wildcard hosts before test overrides.

Use the signature `assertSafeBindHost(host, { allowLoopback = false,
interfaceAddresses = localInterfaceAddresses() } = {})` and return the
normalized host only after all checks pass.

The implementation order is: reject `0.0.0.0` and `::`; accept
`127.0.0.1` only when `allowLoopback` is true; parse exactly four decimal
octets in the range 0–255; require `(ipv4 & 0xffc00000) === 0x64400000`; then
require exact membership in `interfaceAddresses`. Stable errors are
`public bind forbidden`, `loopback bind forbidden`, `Tailscale IPv4 required`,
and `host not present on a local interface`.

Implement it as:

```js
import { networkInterfaces } from "node:os";

function localInterfaceAddresses() {
  return Object.values(networkInterfaces())
    .flat()
    .filter(Boolean)
    .map((address) => address.address);
}

function ipv4Number(host) {
  const parts = host.split(".");
  if (
    parts.length !== 4 ||
    parts.some((part) => !/^(0|[1-9]\d{0,2})$/.test(part))
  ) {
    throw new Error("Tailscale IPv4 required");
  }
  const octets = parts.map(Number);
  if (octets.some((octet) => octet > 255)) {
    throw new Error("Tailscale IPv4 required");
  }
  return (
    (
      (octets[0] << 24) |
      (octets[1] << 16) |
      (octets[2] << 8) |
      octets[3]
    ) >>> 0
  );
}

export function assertSafeBindHost(
  host,
  {
    allowLoopback = false,
    interfaceAddresses = localInterfaceAddresses(),
  } = {},
) {
  if (host === "0.0.0.0" || host === "::") {
    throw new Error("public bind forbidden");
  }
  if (host === "127.0.0.1") {
    if (!allowLoopback) throw new Error("loopback bind forbidden");
    return host;
  }
  const address = ipv4Number(host);
  if ((address & 0xffc00000) !== 0x64400000) {
    throw new Error("Tailscale IPv4 required");
  }
  if (!new Set(interfaceAddresses).has(host)) {
    throw new Error("host not present on a local interface");
  }
  return host;
}
```

- [ ] **Step 4: Implement the API and media allowlist**

Use built-in `node:http`. Parse JSON bodies with a 64 KiB maximum. Load and
validate `batches/<batchId>/manifest.json` with
`validateBatchManifest(manifest, { dataRoot, checkFiles: false })` before every
batch lookup. Reference hashes are verified separately while loading the batch;
image and thumbnail existence is deferred to each media request so a missing
card does not block the other forty-nine. Resolve media through
`declaredMedia(manifest)` using image ID and media kind; never accept a
filesystem path from the URL.

Before serving an original, require the PNG signature
`89504e470d0a1a0a` and, when declared, its SHA-256 match. Before serving a
thumbnail, require a `RIFF....WEBP` header. If a thumbnail is absent or corrupt
but its immutable PNG passes validation, call the injected
`thumbnailBuilder(source, output)` once through a per-output promise queue and
validate the resulting WebP before responding. The production builder runs:

```text
<absolute-python> <absolute-repo>/scripts/build_akari_review_thumbnail.py --input <png> --output <webp> --max-edge 512
```

Capture stderr and return a disabled-media `404` response when repair fails.
Do not attempt repair when the source PNG is invalid.

Responses use:

```js
{
  "ok": true,
  "data": {}
}
```

Errors use a stable status and:

```js
{
  "ok": false,
  "error": {
    "code": "review_conflict",
    "message": "review revision changed; reload this image"
  }
}
```

Return `409` for revision conflicts, `422` for invalid review input, `404` for
unknown IDs or missing media, and `500` for failed durable writes.
`GET /api/batches` validates each batch independently and returns invalid
batches as disabled summaries with their validation message, so one malformed
manifest cannot hide the other batches.

- [ ] **Step 5: Add traversal, missing-media, and concurrent-client tests**

Test URL-encoded traversal strings, undeclared image IDs, missing declared
originals, invalid PNG signatures, valid PNG media headers, missing and corrupt
thumbnail repair through an injected builder, two reviews sent concurrently,
and a stale revision HTTP `409`. Also assert `EADDRINUSE` becomes a startup
error containing the configured host and port.

Extend the filesystem import with `readFile` and `rm`, then use this concrete
fixture and assertions:

```js
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

test("media route rejects traversal and undeclared ids", async (t) => {
  const { running } = await startFixture(t);
  for (const path of [
    "/media/B001/%2e%2e%2fetc%2fpasswd/image",
    "/media/B001/B001-999/image",
  ]) {
    const response = await fetch(`${running.url}${path}`);
    assert.equal(response.status, 404);
  }
});

test("missing original disables only that media response", async (t) => {
  const { fixture, running } = await startFixture(t);
  await rm(join(fixture.batchDir, "images/image-1.png"));
  const response = await fetch(
    `${running.url}/media/B001/B001-001/image`,
  );
  assert.equal(response.status, 404);
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
});
```

Add the corrupt-thumbnail and busy-port cases:

```js
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
```

- [ ] **Step 6: Run server tests**

Run:

```bash
node --test --test-concurrency=1 tools/review-gallery/server.test.mjs
```

Expected: all server tests PASS.

- [ ] **Step 7: Commit the HTTP API**

```bash
git add tools/review-gallery/server.mjs \
  tools/review-gallery/server.test.mjs \
  tools/review-gallery/test-helpers.mjs
git commit -m "Add Tailscale-safe Akari review API"
```

### Task 6: Responsive Review Browser

**Files:**

- Create: `tools/review-gallery/public/index.html`
- Create: `tools/review-gallery/public/styles.css`
- Create: `tools/review-gallery/public/app.js`
- Create: `tools/review-gallery/browser.test.mjs`
- Modify: `tools/review-gallery/server.mjs`
- Modify: `tools/review-gallery/server.test.mjs`

**Interfaces:**

- Consumes: the Task 5 API.
- Produces: fifty-card grid, detail dialog, batch, lane, status, texture, and
  reason filters, progress, keyboard rating, mobile navigation, reason tags,
  notes, missing-media cards, and visible save errors.

- [ ] **Step 1: Write the browser behavior test**

Create `tools/review-gallery/browser.test.mjs`:

```js
import assert from "node:assert/strict";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { chromium } from "playwright";
import { createDemoFixture } from "./test-helpers.mjs";
import { startGalleryServer } from "./server.mjs";

test("desktop grid supports keyboard review and persisted progress", async (t) => {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-browser-"));
  await createDemoFixture(dataRoot);
  const running = await startGalleryServer({
    dataRoot,
    host: "127.0.0.1",
    port: 0,
    allowLoopback: true,
  });
  t.after(() => running.close());
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  t.after(() => browser.close());
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(running.url);
  await page.locator("[data-image-id]").first().click();
  await page.keyboard.press("3");
  await assert.doesNotReject(() =>
    page.waitForSelector('[data-review-status="favorite"]'),
  );
  assert.match(await page.locator("[data-progress]").textContent(), /1\s*\/\s*50/);
});
```

Add a mobile test with a `390 x 844` viewport that opens the detail view,
advances to the next image with the visible button, assigns `reject`, opens the
reason sheet, chooses `skin-flat`, and observes a saved state.

Add browser tests that select a lane, texture-focus, status, and reject-reason
filter and assert the visible card IDs. Abort one review request and assert the
save error stays visible while the prior revision remains. Fulfill one image
request with `404` and assert only its card becomes `Media unavailable`.
Finally rate all fifty fixture entries and assert `Ready for next batch`
appears only after the last successful save.

Use these concrete mobile and completion tests; factor their repeated
server/browser setup into a local helper returning `{ page, running }`:

```js
async function openBrowserFixture(t, viewport) {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-browser-"));
  await createDemoFixture(dataRoot);
  const running = await startGalleryServer({
    dataRoot,
    host: "127.0.0.1",
    port: 0,
    allowLoopback: true,
  });
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  const page = await browser.newPage({ viewport });
  t.after(async () => {
    await browser.close();
    await running.close();
  });
  await page.goto(running.url);
  return { page, running };
}

test("mobile detail saves reject reason and advances", async (t) => {
  const { page } = await openBrowserFixture(t, { width: 390, height: 844 });
  await page.locator("[data-image-id]").first().click();
  await page.locator("[data-review-status-button='reject']").click();
  await page.locator("[data-reason='skin-flat']").click();
  await page.locator("[data-save-review]").click();
  await page.waitForSelector(
    '[data-review-status="reject"][data-review-reasons~="skin-flat"]',
  );
  const firstId = await page.locator("[data-detail-dialog]").getAttribute(
    "data-active-image-id",
  );
  await page.locator("[data-next]").click();
  const secondId = await page.locator("[data-detail-dialog]").getAttribute(
    "data-active-image-id",
  );
  assert.notEqual(firstId, secondId);
});

test("filters save failures missing media and readiness stay visible", async (t) => {
  const { page } = await openBrowserFixture(t, { width: 1280, height: 800 });
  await page.locator("[data-lane-filter]").selectOption("everyday-girly");
  assert.equal(await page.locator("[data-image-id]:visible").count(), 5);
  await page.locator("[data-texture-filter]").selectOption("texture");
  await page.locator("[data-status-filter]").selectOption("unreviewed");

  await page.locator("[data-image-id]").first().click();
  await page.route("**/reviews/**", (route) => route.abort());
  await page.keyboard.press("2");
  await page.waitForSelector("[data-save-error]:not(:empty)");
  await page.unroute("**/reviews/**");

  await page.route("**/media/B001/B001-001/thumb", (route) =>
    route.fulfill({ status: 404, body: "missing" }),
  );
  await page.reload();
  await page.waitForSelector(
    '[data-image-id="B001-001"][data-media-unavailable="true"]',
  );

  await page.evaluate(async () => {
    const batch = await fetch("/api/batches/B001").then((r) => r.json());
    const reviews = await fetch(
      "/api/batches/B001/reviews",
    ).then((r) => r.json());
    await Promise.all(batch.data.entries.map((entry) =>
      fetch(`/api/batches/B001/reviews/${entry.id}`, {
        method: "PUT",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          expectedRevision: reviews.data.reviews[entry.id].revision,
          status: "keep",
          reasons: [],
          note: "",
        }),
      }),
    ));
  });
  await page.reload();
  await page.waitForSelector("text=Ready for next batch");
});
```

Add this reason-filter assertion to the same test before the bulk completion:

```js
await page.locator("[data-image-id='B001-002']").click();
await page.locator("[data-review-status-button='reject']").click();
await page.locator("[data-reason='skin-flat']").click();
await page.locator("[data-save-review]").click();
await page.locator("[data-reason-filter]").selectOption("skin-flat");
assert.deepEqual(
  await page.locator("[data-image-id]:visible").evaluateAll(
    (cards) => cards.map((card) => card.dataset.imageId),
  ),
  ["B001-002"],
);
```

- [ ] **Step 2: Run the browser test to verify it fails**

Run:

```bash
node --test --test-concurrency=1 tools/review-gallery/browser.test.mjs
```

Expected: FAIL because the public application is absent.

- [ ] **Step 3: Create the semantic HTML shell**

`public/index.html` must contain:

```html
<header class="app-header">
  <h1>Akari Kawaii 1000 Review</h1>
  <div data-progress aria-live="polite">0 / 0</div>
</header>
<nav aria-label="Review filters">
  <select data-batch-filter aria-label="Batch"></select>
  <select data-lane-filter aria-label="Lane"></select>
  <select data-status-filter aria-label="Status"></select>
  <select data-texture-filter aria-label="Texture focus"></select>
  <select data-reason-filter aria-label="Reject reason"></select>
</nav>
<main>
  <div class="review-grid" data-review-grid></div>
</main>
<dialog data-detail-dialog>
  <button type="button" data-close aria-label="Close">×</button>
  <button type="button" data-previous>Previous</button>
  <figure>
    <img data-detail-image alt="">
    <figcaption data-detail-caption></figcaption>
  </figure>
  <button type="button" data-next>Next</button>
  <div data-review-controls></div>
  <div data-reason-controls hidden></div>
  <label>Note <textarea data-review-note maxlength="1000"></textarea></label>
  <p data-save-error role="alert"></p>
</dialog>
<script type="module" src="/app.js"></script>
```

- [ ] **Step 4: Implement responsive presentation**

In `styles.css`, use a responsive grid with minimum 170 px cards on desktop and
two columns below 600 px. Use `object-fit: contain`, a neutral dark review
background, obvious status borders, 44 px minimum touch targets, a scroll-safe
dialog, and `prefers-reduced-motion`.

Start from:

```css
:root {
  color-scheme: dark;
  font-family: system-ui, sans-serif;
  background: #171619;
  color: #f7f2f3;
}

body {
  margin: 0;
  min-height: 100vh;
}

.app-header,
nav {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
  padding: 0.75rem 1rem;
}

.review-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 0.75rem;
  padding: 1rem;
}

[data-image-id] {
  min-width: 0;
  border: 3px solid #464147;
  background: #242126;
}

[data-review-status="reject"] { border-color: #d96b71; }
[data-review-status="keep"] { border-color: #75a9d6; }
[data-review-status="favorite"] { border-color: #efb74e; }

[data-image-id] img,
[data-detail-image] {
  display: block;
  width: 100%;
  object-fit: contain;
}

button,
select,
textarea {
  min-height: 44px;
  font: inherit;
}

dialog {
  width: min(96vw, 1100px);
  max-height: 94vh;
  overflow: auto;
  background: #211e23;
  color: inherit;
}

@media (max-width: 599px) {
  .review-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.5rem;
    padding: 0.5rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
  }
}
```

- [ ] **Step 5: Implement application state and rating**

In `app.js`, keep one state object:

```js
const state = {
  batches: [],
  batch: null,
  reviews: null,
  visibleEntries: [],
  activeIndex: -1,
  saving: false,
};
```

Render thumbnail cards with lazy images. Open the original only in the dialog.
An image `error` event replaces only that card with a disabled
`Media unavailable` state; it must not remove or block other entries. Render
all five filters from manifest and review state. Show reviewed count over fifty
and display `Ready for next batch` only when no record is `unreviewed`.
Send review updates with the current revision:

```js
async function saveReview(status, reasons = [], note = "") {
  const entry = state.visibleEntries[state.activeIndex];
  const current = state.reviews.reviews[entry.id];
  const response = await fetch(
    `/api/batches/${state.batch.batchId}/reviews/${entry.id}`,
    {
      method: "PUT",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        expectedRevision: current.revision,
        status,
        reasons,
        note,
      }),
    },
  );
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error.message);
  state.reviews.reviews[entry.id] = payload.data;
  render();
}
```

Map keys `1`, `2`, and `3` to reject, keep, and favorite only while the dialog
is open and no form control has focus. Arrow keys navigate. A reject reveals
optional reason tags. Send the trimmed note with every rating and preserve it
when moving between images. Save failures remain visible and do not
optimistically change the card.

- [ ] **Step 6: Serve static assets safely**

Modify `server.mjs` to map only `/`, `/styles.css`, and `/app.js` to exact files
inside `public/`. Send explicit content types and `Cache-Control: no-store` for
HTML and API responses.

- [ ] **Step 7: Run desktop, mobile, and API tests**

Run:

```bash
node --test --test-concurrency=1 \
  tools/review-gallery/manifest.test.mjs \
  tools/review-gallery/review-store.test.mjs \
  tools/review-gallery/server.test.mjs \
  tools/review-gallery/browser.test.mjs
```

Expected: all tests PASS.

- [ ] **Step 8: Commit the review browser**

```bash
git add tools/review-gallery/public \
  tools/review-gallery/browser.test.mjs \
  tools/review-gallery/server.mjs \
  tools/review-gallery/server.test.mjs
git commit -m "Add responsive Akari review browser"
```

### Task 7: Repository Scripts and Focused Gate

**Files:**

- Modify: `package.json:6-9`
- Modify: `package.json:90-115`
- Modify: `tests/test_workflow_gate_contract.py:13-74`

**Interfaces:**

- Consumes: Task 1 through Task 6 tests and CLIs.
- Produces: `test:node`, `test:python:review-gallery`,
  `gallery:serve`, and `gate:v1-5:gallery` npm scripts.

- [ ] **Step 1: Extend the workflow contract test first**

Update the expected scripts in `tests/test_workflow_gate_contract.py`:

```python
"test:node": (
    "node --test --test-concurrency=1 "
    "tools/pdf/*.test.mjs tools/review-gallery/*.test.mjs"
),
"test:python:review-gallery": (
    "uv run python -m unittest "
    "tests.test_init_akari_v1_5_kawaii_1000 "
    "tests.test_build_akari_review_thumbnail -v"
),
"gallery:serve": "node tools/review-gallery/server.mjs",
"gate:v1-5:gallery": (
    "npm run test:node && npm run test:python:review-gallery && "
    "npm run lint:md"
),
```

Add a focused-gate test:

```python
def test_v1_5_gallery_gate_excludes_pdf_and_ocr(self):
    command = self.scripts["gate:v1-5:gallery"].lower()
    for forbidden in ("pdf", "ocr", "tesseract", "poppler"):
        with self.subTest(forbidden=forbidden):
            self.assertNotIn(forbidden, command)
```

- [ ] **Step 2: Run the workflow test to verify it fails**

Run:

```bash
uv run python -m unittest tests.test_workflow_gate_contract -v
```

Expected: FAIL because the npm scripts still have their old values.

- [ ] **Step 3: Add package scripts**

Set the exact commands in `package.json`:

```json
{
  "test:node": "node --test --test-concurrency=1 tools/pdf/*.test.mjs tools/review-gallery/*.test.mjs",
  "test:python:review-gallery": "uv run python -m unittest tests.test_init_akari_v1_5_kawaii_1000 tests.test_build_akari_review_thumbnail -v",
  "gallery:serve": "node tools/review-gallery/server.mjs",
  "gate:v1-5:gallery": "npm run test:node && npm run test:python:review-gallery && npm run lint:md"
}
```

The Python command intentionally names modules explicitly and does not discover
untracked files. Tasks 8 and 9 extend this exact list as their test modules are
created, so the gate never names a module that does not yet exist.

- [ ] **Step 4: Add CLI argument handling to `server.mjs`**

When executed directly, accept:

```text
--repo-root <absolute path>
--data-root <absolute path>
--host <Tailscale IPv4>
--port <1-65535>
--python <absolute Python executable>
```

Use `AKARI_GALLERY_REPO_ROOT`, `AKARI_GALLERY_DATA_ROOT`,
`AKARI_GALLERY_HOST`, `AKARI_GALLERY_PORT`, and `AKARI_GALLERY_PYTHON` only as
fallbacks. Refuse to start when repo root, data root, host, or Python executable
is missing. Print exactly one ready line:

```text
Akari review gallery listening on http://100.125.117.75:8787
```

Use `node:util` `parseArgs` and this exact mapping:

```js
const { values } = parseArgs({
  args: argv,
  options: {
    "repo-root": { type: "string" },
    "data-root": { type: "string" },
    host: { type: "string" },
    port: { type: "string" },
    python: { type: "string" },
  },
  strict: true,
});
const options = {
  repoRoot: values["repo-root"] ?? env.AKARI_GALLERY_REPO_ROOT,
  dataRoot: values["data-root"] ?? env.AKARI_GALLERY_DATA_ROOT,
  host: values.host ?? env.AKARI_GALLERY_HOST,
  port: Number(values.port ?? env.AKARI_GALLERY_PORT),
  pythonExecutable: values.python ?? env.AKARI_GALLERY_PYTHON,
};
```

Require absolute repo, data, and Python paths and an integer port before
calling `startGalleryServer(options)`. The exported
`parseGalleryOptions(argv, env)` owns this logic so `server.test.mjs` can test
missing values and environment fallbacks without starting a listener.

- [ ] **Step 5: Run focused tests**

Run:

```bash
uv run python -m unittest tests.test_workflow_gate_contract -v
bash -lc 'npm run test:node'
```

Expected: both commands PASS.

- [ ] **Step 6: Commit scripts and gate**

```bash
git add package.json tests/test_workflow_gate_contract.py \
  tools/review-gallery/server.mjs
git commit -m "Add Akari gallery workflow gate"
```

### Task 8: systemd User Service Installer

**Files:**

- Create: `scripts/install_akari_review_gallery_service.py`
- Create: `tests/test_install_akari_review_gallery_service.py`
- Modify: `package.json`
- Modify: `tests/test_workflow_gate_contract.py`

**Interfaces:**

- Consumes: repository root, data root, Tailscale host, port, resolved Node
  executable, resolved virtual-environment Python executable, and user config
  directory.
- Produces: `render_unit(...) -> str`,
  `install_service(...) -> Path`, and a live
  `akari-review-gallery.service`.

- [ ] **Step 1: Write unit-rendering tests**

Create `tests/test_install_akari_review_gallery_service.py`:

```python
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.install_akari_review_gallery_service import (
    install_service,
    render_unit,
)


class InstallReviewGalleryServiceTests(unittest.TestCase):
    def test_unit_uses_exact_node_repo_data_and_tailscale_host(self):
        unit = render_unit(
            node=Path("/opt/node/bin/node"),
            python=Path("/opt/venv/bin/python"),
            repo_root=Path("/srv/akari-design"),
            data_root=Path("/srv/akari-generated/v1.5-1000"),
            host="100.125.117.75",
            port=8787,
        )
        self.assertIn('ExecStart="/opt/node/bin/node"', unit)
        self.assertIn('--python "/opt/venv/bin/python"', unit)
        self.assertIn('"/srv/akari-design/tools/review-gallery/server.mjs"', unit)
        self.assertIn('--host "100.125.117.75"', unit)
        self.assertNotIn("0.0.0.0", unit)
        self.assertIn("Restart=on-failure", unit)

    def test_unit_rejects_wildcard_host(self):
        with self.assertRaisesRegex(ValueError, "Tailscale IPv4"):
            render_unit(
                node=Path("/opt/node/bin/node"),
                python=Path("/opt/venv/bin/python"),
                repo_root=Path("/srv/akari-design"),
                data_root=Path("/srv/data"),
                host="0.0.0.0",
                port=8787,
            )

    def test_install_writes_unit_and_runs_user_systemd(self):
        with tempfile.TemporaryDirectory() as temporary:
            calls = []

            def runner(command, *, check):
                calls.append((command, check))

            destination = install_service(
                "[Unit]\nDescription=Test\n",
                user_config=Path(temporary),
                runner=runner,
            )
            self.assertEqual(
                "[Unit]\nDescription=Test\n",
                destination.read_text(encoding="utf-8"),
            )
            self.assertEqual(
                [
                    (["systemctl", "--user", "daemon-reload"], True),
                    (
                        [
                            "systemctl",
                            "--user",
                            "enable",
                            "--now",
                            "akari-review-gallery.service",
                        ],
                        True,
                    ),
                ],
                calls,
            )
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run python -m unittest \
  tests.test_install_akari_review_gallery_service -v
```

Expected: FAIL with a missing module import.

- [ ] **Step 3: Implement pure unit rendering**

Create `scripts/install_akari_review_gallery_service.py`. `render_unit`
validates absolute paths, rejects quotes and newlines, validates Tailscale
CGNAT IPv4 and the port range, and remains pure so tests may use synthetic
absolute paths. `install_service` additionally requires existing Node and
Python executables, `server.mjs`, the data root, and its `batches/` directory.

Implement the pure core as:

```python
from __future__ import annotations

import ipaddress
import os
import subprocess
from pathlib import Path


SERVICE_NAME = "akari-review-gallery.service"


def _unit_path(path: Path) -> str:
    value = str(path)
    if not path.is_absolute() or any(char in value for char in ('"', "\n")):
        raise ValueError(f"unsafe absolute path: {value}")
    return value


def render_unit(
    *,
    node: Path,
    python: Path,
    repo_root: Path,
    data_root: Path,
    host: str,
    port: int,
) -> str:
    address = ipaddress.ip_address(host)
    network = ipaddress.ip_network("100.64.0.0/10")
    if address.version != 4 or address not in network:
        raise ValueError("Tailscale IPv4 required")
    if not 1 <= port <= 65535:
        raise ValueError("port must be in 1..65535")
    node_value = _unit_path(node)
    python_value = _unit_path(python)
    repo_value = _unit_path(repo_root)
    data_value = _unit_path(data_root)
    server = _unit_path(repo_root / "tools/review-gallery/server.mjs")
    return f"""[Unit]
Description=Akari review gallery

[Service]
Type=simple
ExecStart="{node_value}" "{server}" --repo-root "{repo_value}" --data-root "{data_value}" --host "{host}" --port "{port}" --python "{python_value}"
Restart=on-failure
RestartSec=5
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ReadOnlyPaths="{repo_value}" "{data_value}"
ReadWritePaths="{data_value}/batches"

[Install]
WantedBy=default.target
"""
```

The resulting unit is:

```ini
[Unit]
Description=Akari review gallery

[Service]
Type=simple
ExecStart="/absolute/node" "/absolute/repo/tools/review-gallery/server.mjs" --repo-root "/absolute/repo" --data-root "/absolute/data" --host "100.125.117.75" --port "8787" --python "/absolute/venv/bin/python"
Restart=on-failure
RestartSec=5
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ReadOnlyPaths="/absolute/repo" "/absolute/data"
ReadWritePaths="/absolute/data/batches"

[Install]
WantedBy=default.target
```

The server must write reviews only below `batches/`; reference and state files
stay read-only to the service.

- [ ] **Step 4: Implement explicit installation**

The CLI requires `--install` before writing. It resolves Node with:

```bash
bash -lc 'command -v node'
```

It resolves the environment Python with:

```bash
uv run python -c 'import sys; print(sys.executable)'
```

It writes to
`~/.config/systemd/user/akari-review-gallery.service`, then runs:

```bash
systemctl --user daemon-reload
systemctl --user enable --now akari-review-gallery.service
```

Without `--install`, print the complete unit and perform no writes. Use this
atomic installation function:

```python
def install_service(
    unit: str,
    *,
    user_config: Path,
    runner=subprocess.run,
) -> Path:
    unit_dir = user_config / "systemd/user"
    unit_dir.mkdir(parents=True, exist_ok=True)
    destination = unit_dir / SERVICE_NAME
    temporary = unit_dir / f".{SERVICE_NAME}.{os.getpid()}.tmp"
    temporary.write_text(unit, encoding="utf-8")
    os.replace(temporary, destination)
    runner(
        ["systemctl", "--user", "daemon-reload"],
        check=True,
    )
    runner(
        ["systemctl", "--user", "enable", "--now", SERVICE_NAME],
        check=True,
    )
    return destination
```

Build the `argparse` CLI with `--repo-root`, `--data-root`, `--host`, `--port`,
and `--install`. Resolve Node and Python with the two commands above, call
`render_unit`, and call `install_service` only when `--install` is present.

- [ ] **Step 5: Add the installer test to the focused Python gate**

First update the expected `test:python:review-gallery` value in
`tests/test_workflow_gate_contract.py`, then make the same change in
`package.json`. The exact command at this point is:

```text
uv run python -m unittest tests.test_init_akari_v1_5_kawaii_1000 tests.test_build_akari_review_thumbnail tests.test_install_akari_review_gallery_service -v
```

- [ ] **Step 6: Run installer and workflow tests**

Run:

```bash
uv run python -m unittest \
  tests.test_install_akari_review_gallery_service -v
uv run python -m unittest tests.test_workflow_gate_contract -v
bash -lc 'npm run test:python:review-gallery'
```

Expected: all three commands PASS.

- [ ] **Step 7: Commit the installer**

```bash
git add scripts/install_akari_review_gallery_service.py \
  tests/test_install_akari_review_gallery_service.py \
  package.json tests/test_workflow_gate_contract.py
git commit -m "Add Akari gallery user service installer"
```

### Task 9: Fifty-Image B000 Demo and Operations Runbook

**Files:**

- Create: `scripts/create_akari_review_demo.py`
- Create: `tests/test_create_akari_review_demo.py`
- Create: `docs/akari-v1.5-kawaii-1000-gallery-runbook.md`
- Modify: `package.json`
- Modify: `tests/test_workflow_gate_contract.py`

**Interfaces:**

- Consumes: initialized external data root.
- Produces: non-counting B000 manifest, fifty simple PNG demo cards, fifty WebP
  thumbnails, empty reviews, and a repeatable operations runbook.

- [ ] **Step 1: Write the demo-batch test**

Create `tests/test_create_akari_review_demo.py`:

```python
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.create_akari_review_demo import create_demo_batch


class CreateReviewDemoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data_root = Path(self.temp.name)
        references = self.data_root / "references"
        references.mkdir()
        for name in (
            "akari-v1.5-b3-body-balance.png",
            "akari-v1.4-g2-balanced-lines.png",
        ):
            Image.new("RGB", (16, 24), "#c7a58d").save(references / name)

    def test_demo_has_fifty_non_counting_entries_and_thumbnails(self):
        batch = create_demo_batch(self.data_root)
        manifest = json.loads(
            (batch / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual("demo", manifest["batchType"])
        self.assertEqual(50, len(manifest["entries"]))
        self.assertEqual(
            50,
            len(list((batch / "thumbs").glob("*.webp"))),
        )
```

- [ ] **Step 2: Run the demo test to verify it fails**

Run:

```bash
uv run python -m unittest tests.test_create_akari_review_demo -v
```

Expected: FAIL with a missing module import.

- [ ] **Step 3: Implement B000 demo creation**

Create 50 numbered `768 x 1152` PNG cards with Pillow. Each card shows its ID,
lane, and review instructions on a distinct but restrained background. Create
five cards per lane, mark ten texture-focus slots, and mark the five
`subculture-wildcard` cards. Use the real reference snapshot hashes in the
manifest. Set `generation.toolMode` to `demo`,
`generation.technicalStatus` to `valid`, and record the PNG SHA-256,
dimensions, and thumbnail path. Build thumbnails with `build_thumbnail`.

Use these constants and core:

```python
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw

from scripts.build_akari_review_thumbnail import (
    build_thumbnail,
    inspect_png,
)


LANES = (
    "classic-school-uniform",
    "professional-service-uniform",
    "sports-ceremony-fictional-uniform",
    "everyday-girly",
    "outings-special-days",
    "hobbies-making",
    "travel-walking",
    "retro-storybook",
    "magic-fantasy-sf",
    "subculture-wildcard",
)
COLORS = (
    "#f2d8d5", "#ead8ca", "#d9e4ef", "#efe2c6", "#dce7d6",
    "#e5daf0", "#f0d9e3", "#d7e8e6", "#e8dfd5", "#d9d8e9",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json_atomic(path: Path, value: object) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _reference(data_root: Path, name: str, role: str) -> dict[str, object]:
    path = data_root / "references" / name
    if not path.is_file():
        raise FileNotFoundError(path)
    return {
        "path": f"references/{name}",
        "role": role,
        "exclusions": ["outfit", "pose", "background"],
        "sha256": _sha256(path),
    }


def create_demo_batch(data_root: Path) -> Path:
    data_root = data_root.resolve()
    batch = data_root / "batches/B000"
    manifest_path = batch / "manifest.json"
    if manifest_path.exists():
        current = json.loads(manifest_path.read_text(encoding="utf-8"))
        if current.get("batchType") != "demo":
            raise ValueError("refusing to overwrite non-demo B000")
    images = batch / "images"
    thumbs = batch / "thumbs"
    images.mkdir(parents=True, exist_ok=True)
    thumbs.mkdir(parents=True, exist_ok=True)
    authorities = (
        _reference(
            data_root,
            "akari-v1.5-b3-body-balance.png",
            "v1.5 identity and body balance",
        ),
        _reference(
            data_root,
            "akari-v1.4-g2-balanced-lines.png",
            "rendering and skin authority",
        ),
    )
    entries = []
    for lane_index, lane in enumerate(LANES):
        for offset in range(5):
            ordinal = lane_index * 5 + offset + 1
            image_id = f"B000-{ordinal:03d}"
            stem = f"demo-{ordinal:03d}"
            image_path = images / f"{stem}.png"
            thumb_path = thumbs / f"{stem}.webp"
            canvas = Image.new("RGB", (768, 1152), COLORS[lane_index])
            draw = ImageDraw.Draw(canvas)
            draw.text((64, 80), image_id, fill="#352f32")
            draw.text((64, 150), lane, fill="#352f32")
            draw.text(
                (64, 240),
                "1 Reject   2 Keep   3 Favorite",
                fill="#554b50",
            )
            canvas.save(image_path, "PNG")
            build_thumbnail(image_path, thumb_path)
            technical = inspect_png(image_path)
            entries.append({
                "id": image_id,
                "lane": lane,
                "cuteBeat": f"demo-beat-{ordinal}",
                "wardrobeFamily": f"demo-wardrobe-{ordinal}",
                "setting": f"demo-setting-{ordinal}",
                "action": f"demo-action-{ordinal}",
                "sceneMode": (
                    "action-reaction" if ordinal <= 40 else "quiet-posed"
                ),
                "composition": f"demo-composition-{ordinal}",
                "camera": f"demo-camera-{ordinal}",
                "lighting": f"demo-lighting-{ordinal}",
                "cast": (
                    "solo" if ordinal <= 35
                    else "viewer-pov" if ordinal <= 45
                    else "group"
                ),
                "dominantColor": COLORS[lane_index],
                "textureFocus": ordinal <= 10,
                "textureType": (
                    f"demo-texture-{ordinal}" if ordinal <= 10 else "none"
                ),
                "subculture": lane == "subculture-wildcard",
                "prompt": f"Demo card only; no image generation; {image_id}",
                "references": [dict(item) for item in authorities],
                "generation": {
                    "toolMode": "demo",
                    "generationId": None,
                    "requestId": None,
                    "sourcePath": None,
                    "technicalStatus": "valid",
                    "failureReason": None,
                },
                "artifact": {
                    "imagePath": f"batches/B000/images/{stem}.png",
                    "thumbnailPath": f"batches/B000/thumbs/{stem}.webp",
                    "sha256": technical["sha256"],
                    "width": technical["width"],
                    "height": technical["height"],
                },
            })
    manifest = {
        "schemaVersion": 1,
        "batchType": "demo",
        "batchId": "B000",
        "title": "Akari Kawaii 1000 Review Demo",
        "entries": entries,
    }
    reviews = {
        "schemaVersion": 1,
        "batchId": "B000",
        "reviews": {
            entry["id"]: {
                "status": "unreviewed",
                "reasons": [],
                "note": "",
                "revision": 0,
                "updatedAt": None,
            }
            for entry in entries
        },
    }
    _write_json_atomic(manifest_path, manifest)
    reviews_path = batch / "reviews.json"
    if not reviews_path.exists():
        _write_json_atomic(reviews_path, reviews)
    return batch
```

The CLI parses one required absolute `--data-root`, calls
`create_demo_batch`, and prints the resulting B000 path.

The CLI is:

```bash
uv run python scripts/create_akari_review_demo.py \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000
```

Refuse to overwrite a non-demo `B000`. Re-running an unchanged demo is
idempotent. B000 has `"batchType": "demo"` and never enters the 1,000 count.

- [ ] **Step 4: Write the operations runbook**

Create `docs/akari-v1.5-kawaii-1000-gallery-runbook.md` with exact sections:

- initialize or verify the external reference snapshot;
- create or refresh B000;
- run the focused gate;
- preview the systemd unit;
- install and start the service;
- inspect logs with
  `journalctl --user -u akari-review-gallery.service`;
- verify the listener with
  `ss -ltnp | rg '100\\.125\\.117\\.75:8787'`;
- open `http://100.125.117.75:8787`;
- rate all B000 cards from PC and a mobile tailnet device;
- restart the service and confirm reviews persist;
- stop, disable, or reinstall the service;
- state explicitly that B000 is demo-only and no image generation occurs.

- [ ] **Step 5: Complete the focused Python gate**

First update the expected `test:python:review-gallery` value in
`tests/test_workflow_gate_contract.py`, then make the same change in
`package.json`. The final exact command is:

```text
uv run python -m unittest tests.test_init_akari_v1_5_kawaii_1000 tests.test_build_akari_review_thumbnail tests.test_install_akari_review_gallery_service tests.test_create_akari_review_demo -v
```

- [ ] **Step 6: Run tests and create the real demo**

Run serially:

```bash
uv run python -m unittest tests.test_create_akari_review_demo -v
uv run python -m unittest tests.test_workflow_gate_contract -v
bash -lc 'npm run test:python:review-gallery'
uv run python scripts/create_akari_review_demo.py \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000
node tools/review-gallery/server.mjs \
  --repo-root /home/takahiro/workspace/akari-design \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --host 100.125.117.75 \
  --port 8787 \
  --python /home/takahiro/workspace/akari-design/.venv/bin/python3
```

Start the server command in a managed background session for this manual check;
do not leave a duplicate process running before systemd installation.

- [ ] **Step 7: Validate B000 in the browser**

Confirm:

- fifty cards appear;
- original cards open without downloads;
- desktop `1`/`2`/`3` shortcuts work;
- mobile controls fit and save;
- reject reasons persist;
- the progress reaches `50 / 50`;
- the batch displays `Ready for next batch`;
- restarting the temporary server preserves reviews.

- [ ] **Step 8: Commit demo tooling and runbook**

```bash
git add scripts/create_akari_review_demo.py \
  tests/test_create_akari_review_demo.py \
  docs/akari-v1.5-kawaii-1000-gallery-runbook.md \
  package.json tests/test_workflow_gate_contract.py
git commit -m "Add Akari gallery demo runbook"
```

### Task 10: Live Service and Final Foundation Gate

**Files:**

- Modify only if verification exposes a defect in files owned by Tasks 1-9.
- External write:
  `~/.config/systemd/user/akari-review-gallery.service`

**Interfaces:**

- Consumes: all previous tasks and the live external data root.
- Produces: one persistent Tailscale-only service, passing gates, and evidence
  that foundation acceptance criteria are met.

- [ ] **Step 1: Run the focused gate**

Run:

```bash
bash -lc 'npm run gate:v1-5:gallery'
```

Expected: Node tests, focused Python tests, and Markdown lint all PASS.

- [ ] **Step 2: Preview the live unit without writing**

Run:

```bash
uv run python scripts/install_akari_review_gallery_service.py \
  --repo-root /home/takahiro/workspace/akari-design \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --host 100.125.117.75 \
  --port 8787
```

Expected: unit text contains the resolved Node path, exact Tailscale host, and
no wildcard bind.

- [ ] **Step 3: Install and start the user service**

Run:

```bash
uv run python scripts/install_akari_review_gallery_service.py \
  --repo-root /home/takahiro/workspace/akari-design \
  --data-root /home/takahiro/workspace/akari_generated/v1.5-1000 \
  --host 100.125.117.75 \
  --port 8787 \
  --install
```

Expected: service becomes active. User lingering was already `yes` at planning
time; recheck it rather than changing it blindly.

- [ ] **Step 4: Verify Tailscale-only reachability**

Run:

```bash
systemctl --user --no-pager --full status akari-review-gallery.service
ss -ltnp | rg '100\.125\.117\.75:8787'
curl --fail --silent http://100.125.117.75:8787/api/batches
```

Expected: exactly one matching listener on `100.125.117.75:8787`, API JSON
containing B000, and no listener on `0.0.0.0:8787` or `[::]:8787`.

- [ ] **Step 5: Restart and verify review persistence**

Rate at least one B000 card, record its revision, then run:

```bash
systemctl --user restart akari-review-gallery.service
curl --fail --silent http://100.125.117.75:8787/api/batches/B000/reviews
```

Expected: the saved state and revision remain.

- [ ] **Step 6: Run the existing broad integration gate serially**

Run only after the focused gate and live service checks finish:

```bash
bash -lc 'npm run gate:integration:all'
```

Expected: PASS. This broad gate performs structural checks but not full PDF
raster or OCR work.

- [ ] **Step 7: Verify the final repository state**

Run:

```bash
git diff --check
git status --short --branch
git log --oneline --decorate -12
```

Expected: no uncommitted foundation files. The external
`akari_generated/v1.5-1000` tree does not appear in Git.

- [ ] **Step 8: Prepare the B001 planning handoff**

Record these live facts for the follow-up B001 plan:

- service URL and active status;
- B000 desktop and mobile review result;
- manifest validator and focused gate result;
- permanent reference snapshot paths and hashes;
- exact ten lane slugs;
- texture and subculture quotas;
- any UI friction discovered during B000 review.

Then invoke `superpowers:writing-plans` to write the separate B001 generation
plan. Do not generate B001 in this foundation task.
