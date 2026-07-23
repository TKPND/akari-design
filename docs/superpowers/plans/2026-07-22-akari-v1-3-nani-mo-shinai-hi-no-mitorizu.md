# Akari v1.3『何もしない日の見取り図』Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, review, and release an 18-page A4 portrait Akari v1.3
artbook from twelve user-selected overhead indoor scenes, with reproducible
provenance, continuity evidence, and a deterministic PDF audit.

**Architecture:** Add one independent artbook package below `akari-v1.3/`.
A focused Python lifecycle module owns the immutable reference snapshots, room
anchor, scene prompts, byte-identical promotion, Act approval, and clean
checkout validation. The existing Node/Playwright PDF renderer is extended
with one portrait document and isolated layout styles; a dedicated Python
exporter and auditor own checksum, raster, text, and OCR verification.

**Tech Stack:** Python 3.11, `unittest`, PyYAML, Pillow, Node ESM,
Playwright/Chrome, ImageMagick, Poppler, qpdf, Tesseract, npm scripts, Codex
`imagegen`, SHA-256, Markdown.

## Global Constraints

- The approved design is
  `docs/superpowers/specs/2026-07-22-akari-v1-3-nani-mo-shinai-hi-no-mitorizu-design.md`.
- The story is a different world line from the novel: Akari is alone all day;
  no viewer, visitor, second place setting, off-screen gaze, reflection, or
  implied companion appears.
- Produce exactly twelve 4:5 portrait PNG scenes at 1024 x 1280 or larger,
  ordered from `08:12` through `23:41`.
- Use exactly seven true-overhead scenes at 75-90 degrees and five high-oblique
  scenes at 45-60 degrees, as fixed in the design.
- The room is one compact 1K with immutable furniture placement. Only books,
  mug, laundry, phone, cushion, blanket, food, cardigan, socks, and ornament
  move during the day.
- The base outfit is an opaque loose white short-sleeve T-shirt and opaque
  pale-blue lounge shorts. Scene 09-11 add a thin cardigan and indoor socks;
  Scene 12 removes them.
- The complete crossed pins and small ribbon remain character-left when worn.
  Scene 01, 08, and 12 remove it but keep the complete ornament visible in the
  scene.
- Every scene generation uses byte-identical snapshots of V13-01, V13-02,
  V13-03A, and V13-04B plus the accepted room anchor. A previous scene may
  control only light and movable-prop continuity, never identity.
- Before every generation, open all role-relevant references with
  `view_image`, state each reference role, and keep the images visible in the
  conversation context.
- Every first round is two independent A/B candidates. Only candidates that
  pass all hard gates are shown for selection. Stop until the user selects.
- Promote only the explicitly selected PNG, without conversion or metadata
  rewrite. Prove source and destination are byte-identical with `cmp` and
  matching SHA-256.
- `source/candidates/` and generated contact sheets remain local and untracked.
  Accepted PNGs, manifests, immutable reference snapshots, YAML review
  evidence, release PDF, and checksum are durable.
- Clean checkout validation must not require ignored candidate PNGs. It uses
  the selected source SHA recorded in review evidence and verifies the
  accepted PNG against that SHA.
- Do not waive a `major` into an accepted room anchor, scene, Act, or full-book
  review.
- Change one primary cause per retry. If the same Major survives two rounds,
  simplify the pose or camera. An overhead/high-oblique assignment may move to
  another not-yet-accepted scene only after user approval and a paired manifest
  change that preserves exactly seven overhead and five high-oblique scenes.
- Do not modify accepted files or manifests under `akari-v1.2/`, the six v1.3
  Base Definition images, or anything below
  `legacy/akari-v1.2-pre-natural-form/`.
- Keep named gates serial on the 3-core, 2 GiB host. Do not overlap image
  generation, Chromium, PDF export, Poppler, or Tesseract.

---

## File Map and Interfaces

Create these durable package paths:

```text
akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/README.md
akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/manifest/book.yaml
akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/manifest/continuity.yaml
akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/manifest/references.yaml
akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/manifest/render.json
akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/manifest/scenes/index.yaml
akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/references/v1.3/*.png
akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/references/room/.gitkeep
akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/accepted/.gitkeep
akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/evidence/reviews/.gitkeep
akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/release/.gitkeep
```

Create these implementation and test files:

```text
scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py
scripts/build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py
scripts/export_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf.py
scripts/audit_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf.py
tests/test_v1_3_nani_mo_shinai_hi_no_mitorizu_contract.py
tests/test_build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py
tests/test_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf_audit.py
tools/pdf/nani-mo-shinai-hi-no-mitorizu-document.mjs
tools/pdf/nani-mo-shinai-hi-no-mitorizu-document.test.mjs
```

Modify `.gitignore`, `package.json`, `tests/test_workflow_gate_contract.py`,
`tools/pdf/render.mjs`, and `tools/pdf/styles.css`.

The lifecycle module exposes `ValidationError(ValueError)`,
`sha256_file(path: Path) -> str`, `load_contract(root: Path) -> dict`,
`validate_contract(root: Path, *, require_complete: bool = False,
require_release: bool = False) -> None`,
`render_room_prompt(contract: dict, variant: str) -> str`,
`render_scene_prompt(contract: dict, scene_id: str, variant: str) -> str`,
`promote_room_anchor(root: Path, revision: str, variant: str,
review_path: Path) -> Path`, `promote_scene(root: Path, scene_id: str,
revision: str, variant: str, review_path: Path) -> Path`,
`approve_act(root: Path, act: int, review_path: Path) -> Path`,
`validate_act(root: Path, act: int) -> None`, and
`approve_full(root: Path, review_path: Path, cover_scene: str) -> Path`.

The contact-sheet module exposes
`build_room_candidate_sheet(root: Path) -> Path`,
`build_candidate_sheet(root: Path, scene_id: str) -> Path`,
`build_act_sheet(root: Path, act: int) -> Path`, and
`build_full_sheet(root: Path) -> Path`.

### Task 1: Create the artbook package and immutable reference boundary

**Files:**

- Create: package docs, manifests, reference snapshots, and `.gitkeep` files
  listed in the File Map.
- Modify: `.gitignore`
- Test: `tests/test_v1_3_nani_mo_shinai_hi_no_mitorizu_contract.py`

**Interfaces:**

- Consumes: the approved spec and four accepted v1.3 Base images.
- Produces: the static contract and canonical paths used by every later task.

- [ ] **Step 1: Write the failing static package tests**

Create the test module with these contract assertions:

```python
from pathlib import Path
import hashlib
import json
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu"


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"expected mapping: {path}")
    return data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class V13HolidayStaticContractTest(unittest.TestCase):
    def test_book_is_eighteen_page_a4_portrait(self):
        book = load_yaml(PACKAGE / "manifest/book.yaml")
        self.assertEqual("akari-v1.3-nani-mo-shinai-hi-no-mitorizu", book["book_id"])
        self.assertEqual(18, book["page_count"])
        self.assertEqual(
            {"name": "A4-portrait", "width_in": 8.27, "height_in": 11.69},
            book["page_size"],
        )
        self.assertEqual({"width": 1024, "height": 1280}, book["minimum_image"])

    def test_scene_order_times_and_camera_count(self):
        scenes = load_yaml(PACKAGE / "manifest/scenes/index.yaml")["scenes"]
        self.assertEqual(
            [f"scene-{number:02d}" for number in range(1, 13)],
            [scene["id"] for scene in scenes],
        )
        self.assertEqual(
            [
                "08:12", "08:36", "09:10", "10:24", "11:48", "13:06",
                "14:32", "15:47", "17:26", "19:04", "21:18", "23:41",
            ],
            [scene["time"] for scene in scenes],
        )
        self.assertEqual(7, sum(scene["camera"] == "overhead" for scene in scenes))
        self.assertEqual(5, sum(scene["camera"] == "high-oblique" for scene in scenes))
        self.assertTrue(all(scene["dialogue"] == [] for scene in scenes))

    def test_render_manifest_starts_without_a_cover_selection(self):
        render = json.loads((PACKAGE / "manifest/render.json").read_text())
        self.assertEqual(
            {
                "cover_scene": None,
                "detail_scene": "scene-04",
                "afterimage_scene": "scene-12",
            },
            render,
        )
```

Add a reference test that compares each copied file to its Base source and to
these literal hashes:

```python
REFERENCE_PINS = {
    "v13-01": "780f6b7b2f104f6d5196f0dd57d65cac921cb5af8e958a4edc46a10d842652cb",
    "v13-02": "0f8ca9df4c617dfcb30ba6f23d4b01647d00c4a9216ef57f335109daac7a3ee3",
    "v13-03a": "b07c2ce0c663f3f958e2e134ebeaac7efa3c5786a421b6f81af8f0e472a7043c",
    "v13-04b": "0f8ca9df4c617dfcb30ba6f23d4b01647d00c4a9216ef57f335109daac7a3ee3",
}
```

- [ ] **Step 2: Run the focused module and verify the package is missing**

```sh
bash -lc 'uv run python -m unittest tests.test_v1_3_nani_mo_shinai_hi_no_mitorizu_contract -v'
```

Expected: failures for missing package manifests and references.

- [ ] **Step 3: Create the package manifests**

Create `manifest/book.yaml` with version `1.0.0`, A4 portrait geometry,
preview size `2480 x 3508`, minimum image `1024 x 1280`, page count 18, release
path `release/akari-v1.3-nani-mo-shinai-hi-no-mitorizu.pdf`, and pages 1-18
matching the approved design. Set page 1 source to `cover-selection`, page 2 to
`scene-04`, page 16 to `scene-12`, and pages 4-15 to ordered scene IDs.

Create `manifest/render.json` exactly as asserted above. It is the only data
read directly by the Node document model for derived-page source selection.

Create `manifest/scenes/index.yaml` with the twelve approved rows:

| Scene | Act | Time | Camera | Angle | Ornament | Layers |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | 1 | 08:12 | overhead | 75-90 | visible-off-pillow | base-barefoot |
| 02 | 1 | 08:36 | high-oblique | 45-60 | putting-on | base-barefoot |
| 03 | 1 | 09:10 | high-oblique | 45-60 | worn | base-barefoot |
| 04 | 2 | 10:24 | overhead | 75-90 | worn | base-barefoot |
| 05 | 2 | 11:48 | high-oblique | 45-60 | worn | base-barefoot |
| 06 | 2 | 13:06 | overhead | 75-90 | worn | base-barefoot |
| 07 | 3 | 14:32 | overhead | 75-90 | worn | base-barefoot |
| 08 | 3 | 15:47 | overhead | 75-90 | visible-off-table | base-barefoot |
| 09 | 3 | 17:26 | high-oblique | 45-60 | worn | cardigan-socks |
| 10 | 4 | 19:04 | overhead | 75-90 | worn | cardigan-socks |
| 11 | 4 | 21:18 | high-oblique | 45-60 | worn | cardigan-socks |
| 12 | 4 | 23:41 | overhead | 75-90 | visible-off-pillow | base-barefoot |

Each scene begins with `revision: null`, `status: planned`, the canonical A/B
candidate paths below `source/candidates/<scene>/r01/`, and null
`accepted_path`, `accepted_sha256`, and `review_path`. Copy the exact action,
composition, light, and movable-prop requirements from section 10 of the
approved spec; keep `dialogue: []` for every row.

Create `manifest/continuity.yaml` with the fixed room map, four light stages,
the wardrobe and ornament state table above, `review_order` equal to
`[identity, hair, camera, body, room, continuity, rendering, production]`,
and all Major conditions from section 13 of the spec.

Create `manifest/references.yaml` with four Base references and one planned
room anchor. Each Base row records source path, copied path, controlling role,
excluded roles, and the literal SHA above. The room row begins with
`status: planned`, `copied_path: references/room/room-anchor-r01.png`, and
`sha256: null`.

- [ ] **Step 4: Copy the immutable Base references byte-for-byte**

Use `install -D -m 0644` for these exact pairs:

```sh
install -D -m 0644 \
  akari-v1.3/accepted/base/key-visual/akari-v1.3_v13-01_corrected-key-visual_r01.png \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/references/v1.3/v13-01.png
install -D -m 0644 \
  akari-v1.3/accepted/base/full-body/akari-v1.3_v13-02_natural-full-body_r01.png \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/references/v1.3/v13-02.png
install -D -m 0644 \
  akari-v1.3/accepted/base/expressions/akari-v1.3_v13-03a_everyday_r01.png \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/references/v1.3/v13-03a.png
install -D -m 0644 \
  akari-v1.3/accepted/base/wardrobe/akari-v1.3_v13-04b_roomwear_r01.png \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/references/v1.3/v13-04b.png
```

Run `cmp --silent` for every pair and verify the four literal hashes with
`sha256sum`.

- [ ] **Step 5: Create README, tracked empty boundaries, and ignore rules**

The README states `Status: production`, the room→pilot→Act 1-4→PDF sequence,
the exact edit/integration/release gate names, and that candidates/contact
sheets remain local.

Add these exact `.gitignore` entries:

```gitignore
akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/source/candidates/
akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/evidence/contact-sheets/
```

Create `.gitkeep` files for empty tracked directories listed in the File Map.

- [ ] **Step 6: Run static tests, lint, and commit**

```sh
bash -lc 'uv run python -m unittest tests.test_v1_3_nani_mo_shinai_hi_no_mitorizu_contract -v'
bash -lc './node_modules/.bin/markdownlint-cli2 akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/README.md'
git add .gitignore tests/test_v1_3_nani_mo_shinai_hi_no_mitorizu_contract.py \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu
git commit -m "feat: scaffold Akari v1.3 overhead holiday artbook"
```

Expected: static tests pass, lint reports `0 error(s)`, and no v1.2 path is
staged.

### Task 2: Implement clean-checkout lifecycle, prompt, and promotion logic

**Files:**

- Create: `scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py`
- Modify: `tests/test_v1_3_nani_mo_shinai_hi_no_mitorizu_contract.py`

**Interfaces:**

- Consumes: the four manifests from Task 1.
- Produces: all lifecycle module interfaces declared in the File Map.

- [ ] **Step 1: Add failing lifecycle tests**

Import every lifecycle interface. In temporary package copies, assert:

```python
validate_contract(ROOT, require_complete=False)

with self.assertRaisesRegex(ValidationError, "room anchor is not accepted"):
    validate_contract(ROOT, require_complete=True)
```

Add fixtures and tests proving:

- the four copied reference hashes are recomputed and pinned;
- only the approved twelve scene IDs, times, Acts, wardrobe states, and
  ornament states are valid;
- camera assignments use only `overhead` or `high-oblique`, their angle ranges
  match 75-90 or 45-60, and the collection always totals seven/five;
- the room anchor cannot be accepted without a user-selected all-pass review;
- a scene cannot be accepted before the room anchor;
- Scene 06 can be accepted first as the pilot, but every other scene requires
  accepted Scene 06;
- accepted scene review keys and gate verdicts are exact;
- `major` and `user_selected: false` prevent promotion;
- a candidate must be PNG, sRGB, exact 4:5, and at least 1024 x 1280;
- promotion copies bytes without conversion and source/promoted hashes match;
- a clean checkout remains valid after deleting ignored candidates;
- if a candidate exists, its computed SHA and bytes must match the accepted
  PNG;
- full validation requires the room anchor, twelve scenes, four accepted Act
  reviews, an accepted full review, and a selected overhead cover scene;
- `approve_full` rejects a cover outside
  `{scene-01, scene-04, scene-06, scene-07, scene-08, scene-10, scene-12}`.

- [ ] **Step 2: Run tests and verify the module is missing**

```sh
bash -lc 'uv run python -m unittest tests.test_v1_3_nani_mo_shinai_hi_no_mitorizu_contract -v'
```

Expected: import failure for the new lifecycle module.

- [ ] **Step 3: Implement the static and lifecycle contract**

Define these exact constants:

```python
PACKAGE = Path("akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu")
SCENE_RE = re.compile(r"^scene-(0[1-9]|1[0-2])$")
REVISION_RE = re.compile(r"^r[0-9]{2}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
VALID_STATUSES = {"planned", "candidate", "review", "accepted", "rejected", "superseded"}
REVIEW_GATES = {
    "identity", "hair", "camera", "body", "room", "continuity",
    "rendering", "production",
}
REVIEW_SEVERITIES = {"major", "minor"}
OVERHEAD_SCENES = {
    "scene-01", "scene-04", "scene-06", "scene-07", "scene-08",
    "scene-10", "scene-12",
}
ACT_SCENES = {
    1: ["scene-01", "scene-02", "scene-03"],
    2: ["scene-04", "scene-05", "scene-06"],
    3: ["scene-07", "scene-08", "scene-09"],
    4: ["scene-10", "scene-11", "scene-12"],
}
```

Use `yaml.safe_load`, `yaml.safe_dump(data, allow_unicode=True,
sort_keys=False)`, `hashlib.sha256`,
`filecmp.cmp(candidate, destination, shallow=False)`,
`shutil.copyfile`, and Pillow. Safe package-relative paths must reject absolute
paths, backslashes, `.` parts, and `..` parts.

The selected scene review schema is exactly:

```yaml
schema_version: 1
scene_id: scene-06
revision: r01
status: accepted
selected_variant: a
user_selected: true
source_path: source/candidates/scene-06/r01/scene-06-r01-a.png
source_sha256: 64-lowercase-hex
promoted_path: accepted/scene-06.png
promoted_sha256: same-64-lowercase-hex
gate_verdicts:
  identity: pass
  hair: pass
  camera: pass
  body: pass
  room: pass
  continuity: pass
  rendering: pass
  production: pass
findings: []
selection_reason: non-empty-text
reference_roles_confirmed: [v13-01, v13-02, v13-03a, v13-04b, room-anchor]
reviewed_at: RFC3339-UTC
```

Room-anchor reviews use `target_id: room-anchor`, gates `room`, `rendering`,
and `production`, and the same source/promoted SHA contract.

`promote_scene` validates the review and candidate, copies with
`shutil.copyfile`, requires
`filecmp.cmp(candidate, destination, shallow=False)`, computes the
destination SHA, writes the review timestamp, and updates the scene row to
`accepted/<scene-id>.png`. It never opens and re-saves the candidate.

When the selected candidate file is absent, `validate_contract` verifies the
durable review `source_sha256` equals the manifest and accepted file SHA. When
the candidate exists, it additionally recomputes its SHA and compares bytes.

- [ ] **Step 4: Implement prompt and approval commands**

`render_room_prompt` requires variant `a` or `b`, contains the complete fixed
room map, `4:5 portrait`, `no person`, `no readable text`, and explicitly says
the referenced V13-01 image controls only pastel rendering, light softness,
and the white/pale-blue/warm-wood palette.

`render_scene_prompt` joins the fixed identity paragraph, fixed room paragraph,
the selected scene action/composition/light/wardrobe/ornament fields, and these
literal bans:

```text
One scene, one time, one Akari, one compact 1K room. No second person, second
place setting, off-screen companion cue, reflection, readable text, logo,
watermark, collage, grid, dollhouse cutaway, fisheye, voyeuristic framing, or
sexualized emphasis. Keep the opaque T-shirt and opaque lounge shorts fully
covering and ordinary.
```

`approve_act` requires all three Act scenes accepted, a review with exact
scope `act-N`, all checks `pass`, no Major, and the current generated contact
sheet. It stores the sheet SHA in the review.

`approve_full` requires twelve accepted scenes and four accepted Act reviews.
It validates the selected cover is in `OVERHEAD_SCENES`, updates
`manifest/render.json` with the chosen `cover_scene`, and stores the full
contact-sheet SHA in the accepted review.

The CLI subcommands are:

```text
validate [--complete] [--release]
prompt-room --variant a|b
prompt-scene --scene scene-NN --variant a|b
promote-room --revision rNN --variant a|b --review PATH
promote-scene --scene scene-NN --revision rNN --variant a|b --review PATH
approve-act --act 1|2|3|4 --review PATH
validate-act --act 1|2|3|4|all
approve-full --review PATH --cover-scene scene-NN
validate-full
```

- [ ] **Step 5: Run focused tests and incomplete CLI validation**

```sh
bash -lc 'uv run python -m unittest tests.test_v1_3_nani_mo_shinai_hi_no_mitorizu_contract -v'
bash -lc 'uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py validate'
```

Expected: tests pass and CLI prints
`Akari v1.3 holiday artbook contract: ok`.

- [ ] **Step 6: Commit**

```sh
git add scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py \
  tests/test_v1_3_nani_mo_shinai_hi_no_mitorizu_contract.py
git commit -m "feat: validate Akari v1.3 holiday artbook lifecycle"
```

### Task 3: Add portrait candidate and continuity contact sheets

**Files:**

- Create: `scripts/build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py`
- Create: `tests/test_build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py`

**Interfaces:**

- Consumes: `load_contract(root)` and `sha256_file(path)` from Task 2.
- Produces: the four contact-sheet functions declared in the File Map.

- [ ] **Step 1: Write failing tests for all sheet scopes**

Use temporary package copies and `Image.new("RGB", (1024, 1280), color)`.
Assert:

```python
sheet = build_room_candidate_sheet(self.root)
self.assertEqual("room-anchor-r01-candidates.webp", sheet.name)

sheet = build_candidate_sheet(self.root, "scene-06")
self.assertEqual("scene-06-r01-candidates.webp", sheet.name)

with self.assertRaisesRegex(ValueError, "12 accepted scenes required"):
    build_full_sheet(self.root)
```

Add a test that Act 2 contains exactly scene 04, 05, and 06 in chronological
order, and a direct CLI `--help` test.

- [ ] **Step 2: Verify the missing-module failure**

```sh
bash -lc 'uv run python -m unittest tests.test_build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet -v'
```

- [ ] **Step 3: Implement the complete contact-sheet module**

Use `ImageOps.contain` rather than `ImageOps.fit` so 4:5 portrait images are
never cropped. Use a two-column `640 x 800` thumbnail layout for A/B sheets,
a three-column `480 x 600` layout for each Act, and a three-column `384 x 480`
layout for the full 12-scene sheet. Each tile label contains scene ID, time,
camera, ornament state, wardrobe state, and the first twelve SHA characters.

The CLI is exact:

```text
--scope room-candidates
--scope candidates --scene scene-NN
--scope act --act N
--scope all-acts
--scope full
```

Write outputs below ignored `evidence/contact-sheets/` as deterministic WEBP
with quality 90 and method 6.

- [ ] **Step 4: Verify and commit**

```sh
bash -lc 'uv run python -m unittest tests.test_build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet -v'
git add scripts/build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py \
  tests/test_build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py
git commit -m "feat: add Akari v1.3 holiday continuity sheets"
```

### Task 4: Add explicit edit and integration workflow gates

**Files:**

- Modify: `package.json`
- Modify: `tests/test_workflow_gate_contract.py`

**Interfaces:**

- Consumes: Tasks 2 and 3.
- Produces: focused production commands that do not run PDF or OCR.

- [ ] **Step 1: Add failing exact-string assertions**

Assert these script values:

```python
"test:python:v1-3:nani-mo-shinai-hi-no-mitorizu": (
    "uv run python -m unittest "
    "tests.test_v1_3_nani_mo_shinai_hi_no_mitorizu_contract "
    "tests.test_build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet "
    "tests.test_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf_audit -v"
),
"validate:v1-3:nani-mo-shinai-hi-no-mitorizu": (
    "uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py validate"
),
"gate:edit:v1-3:nani-mo-shinai-hi-no-mitorizu": (
    "npm run test:python:v1-3:nani-mo-shinai-hi-no-mitorizu && "
    "npm run validate:v1-3:nani-mo-shinai-hi-no-mitorizu && "
    "npm run validate:v1-3"
),
```

The focused test command may reference the PDF audit module before Task 13;
create `tests/test_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf_audit.py` with an
empty `unittest.TestCase` so the named gate stays stable from this task onward.

Assert the edit gate contains none of `pdf`, `ocr`, `tesseract`, `chromium`,
`pdftoppm`, or `qpdf`.

- [ ] **Step 2: Run the workflow test and verify missing scripts**

```sh
bash -lc 'uv run python -m unittest tests.test_workflow_gate_contract -v'
```

- [ ] **Step 3: Add package scripts and ignore-safe behavior**

Add the three exact commands above and:

```json
"build:v1-3:nani-mo-shinai-hi-no-mitorizu:contact-sheet": "uv run python scripts/build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py",
"gate:integration:v1-3:nani-mo-shinai-hi-no-mitorizu": "npm run gate:edit:v1-3:nani-mo-shinai-hi-no-mitorizu && uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py validate-act --act all && uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py validate-full && npm run gate:integration:v1-3"
```

The integration gate is expected to remain red until all four Acts and the full
review are approved. During production, use the edit gate plus the focused
`validate-act --act N` command for completed Acts.

- [ ] **Step 4: Verify and commit**

```sh
bash -lc 'uv run python -m unittest tests.test_workflow_gate_contract -v'
bash -lc 'npm run gate:edit:v1-3:nani-mo-shinai-hi-no-mitorizu'
git add package.json tests/test_workflow_gate_contract.py \
  tests/test_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf_audit.py
git commit -m "build: add Akari v1.3 holiday artbook gates"
```

### Task 5: Generate, review, and accept the room anchor

**Files:**

- Create locally:
  `akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/source/candidates/room-anchor/r01/room-anchor-r01-{a,b}.png`
- Create after selection:
  `akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/references/room/room-anchor-r01.png`
- Create:
  `akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/evidence/reviews/room-anchor.yaml`
- Modify:
  `akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/manifest/references.yaml`

**Interfaces:**

- Consumes: V13-01 only as palette and rendering direction.
- Produces: the immutable spatial authority required by every scene.

- [ ] **Step 1: Open the palette/style reference and state its limited role**

Open `references/v1.3/v13-01.png` with `view_image` at original detail. State
that it controls only pastel line/paint finish, soft light, off-white,
pale-blue, warm-wood palette, and overall polish. It does not authorize a
person in the room anchor.

- [ ] **Step 2: Render exact independent A/B prompts**

Run:

```sh
bash -lc 'uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py prompt-room --variant a'
bash -lc 'uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py prompt-room --variant b'
```

Use each stdout verbatim in a separate `imagegen` call with only
`references/v1.3/v13-01.png` attached. Save the two PNG results to the
canonical A/B candidate paths. Do not make a collage and do not generate B as
an edit of A.

- [ ] **Step 3: Build and inspect the room candidate sheet**

```sh
bash -lc 'uv run python scripts/build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py --scope room-candidates'
```

Open A, B, and the sheet. Review fixed orientation, window/bed/rug/table/
kitchen/shelf placement, livable scale, 4:5 composition, warm-wood and
pale-blue palette, absence of people and text, and non-dollhouse rendering.

- [ ] **Step 4: Request explicit room selection and stop**

Present only all-pass candidates. Ask the user for `A` or `B`. Do not create an
accepted room anchor or change its manifest row before the reply. If neither
passes, record both as rejected, increment to `r02`, and change only the shared
Major cause in the next prompt.

- [ ] **Step 5: Write the selected room review and promote**

Write `evidence/reviews/room-anchor.yaml` with `status: accepted`,
`user_selected: true`, the selected source path/SHA, promoted path/SHA, all
three gates `room`, `rendering`, and `production` set to `pass`, no Major, and
the selection reason.

Run:

```sh
bash -lc 'uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py promote-room --revision r01 --variant a --review evidence/reviews/room-anchor.yaml'
```

Use `--variant b` when B was selected. Then run `cmp --silent` and
`sha256sum` against the selected candidate and
`references/room/room-anchor-r01.png`.

- [ ] **Step 6: Verify and commit the selected room only**

```sh
bash -lc 'npm run gate:edit:v1-3:nani-mo-shinai-hi-no-mitorizu'
git add \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/references/room/room-anchor-r01.png \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/manifest/references.yaml \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/evidence/reviews/room-anchor.yaml
git commit -m "feat: accept Akari v1.3 holiday room anchor"
```

Candidate PNGs and the candidate sheet must remain untracked.

### Task 6: Generate and lock Scene 06 as the overhead pilot

**Files:**

- Create locally:
  `source/candidates/scene-06/r01/scene-06-r01-{a,b}.png` below the package.
- Create after selection: `accepted/scene-06.png` below the package.
- Create: `evidence/reviews/scene-06.yaml` below the package.
- Modify: `manifest/scenes/index.yaml` below the package.

**Interfaces:**

- Consumes: all four Base snapshots and the accepted room anchor.
- Produces: the overhead visual grammar and pilot lock required by every other
  scene.

- [ ] **Step 1: Open all five authorities and state each role**

Open, in this order:

```text
references/v1.3/v13-01.png  face, amber eyes, airy bob, worn ornament, rendering
references/v1.3/v13-02.png  full body, healthy legs, joints, natural weight
references/v1.3/v13-03a.png everyday relaxed expression
references/v1.3/v13-04b.png opaque white T-shirt and pale-blue room shorts
references/room/room-anchor-r01.png furniture, scale, palette, room orientation
```

State that no previous generated scene controls identity.

- [ ] **Step 2: Render and generate independent Scene 06 A/B**

```sh
bash -lc 'uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py prompt-scene --scene scene-06 --variant a'
bash -lc 'uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py prompt-scene --scene scene-06 --variant b'
```

Use each stdout verbatim in separate `imagegen` calls with the five reference
paths attached. Save returned PNGs to the canonical paths. If a returned image
is not exactly 4:5, do not stretch or crop it into compliance; record the
production Major and regenerate.

- [ ] **Step 3: Review the pilot at original resolution**

Build the candidate sheet:

```sh
bash -lc 'uv run python scripts/build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py --scope candidates --scene scene-06'
```

Review identity, complete worn character-left ornament, 75-90 degree camera,
readable face, believable neck/shoulders/pelvis/legs, phone-holding hands,
room scale and orientation, nonsexual framing, 4:5, sRGB, and absence of text.

- [ ] **Step 4: Request explicit pilot selection and stop**

Show only all-pass candidates and ask for `A` or `B`. No promotion occurs
before the reply.

- [ ] **Step 5: Record and promote the selected pilot**

Write `evidence/reviews/scene-06.yaml` with the complete schema from Task 2,
all eight gate verdicts `pass`, and the selected source SHA. Run:

```sh
bash -lc 'uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py promote-scene --scene scene-06 --revision r01 --variant a --review evidence/reviews/scene-06.yaml'
```

Use B when selected. Prove candidate/accepted byte equality with `cmp` and
matching SHA-256.

- [ ] **Step 6: Verify and commit**

```sh
bash -lc 'npm run gate:edit:v1-3:nani-mo-shinai-hi-no-mitorizu'
git add \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/accepted/scene-06.png \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/manifest/scenes/index.yaml \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/evidence/reviews/scene-06.yaml
git commit -m "feat: lock Akari v1.3 overhead holiday pilot"
```

### Task 7: Produce and approve Act 1 morning

**Files:**

- Create locally: canonical A/B candidates for Scene 01, 02, and 03.
- Create: `accepted/scene-01.png`, `accepted/scene-02.png`,
  `accepted/scene-03.png` below the package.
- Create: `evidence/reviews/scene-01.yaml` through `scene-03.yaml` and
  `evidence/reviews/act-1.yaml`.
- Modify: `manifest/scenes/index.yaml`.

**Interfaces:**

- Consumes: the overhead pilot and five immutable authorities.
- Produces: an approved three-scene morning sequence.

- [ ] **Step 1: Generate and select Scene 01 at 08:12**

Open the five authorities. Scene 01 additionally uses the accepted Scene 06
only for room scale; it does not inherit its face. Render exact A/B prompts
with `prompt-scene --scene scene-01 --variant a|b`, call `imagegen` separately,
and save to canonical A/B paths.

Review the true-overhead bed composition, awake expression, connected body
under ordinary bedding, basic outfit, and the complete ornament visibly placed
at the pillow. Build the Scene 01 candidate sheet, request A/B selection, write
the all-pass selected review, promote byte-for-byte, run the edit gate, and
commit:

```sh
git commit -m "feat: accept Akari v1.3 holiday scene 01"
```

- [ ] **Step 2: Generate and select Scene 02 at 08:36**

Repeat the explicit reference opening. Render Scene 02 A/B prompts. Review the
45-60 degree high-oblique camera, mirror and hand continuity, young-adult face,
and one complete ornament being attached to character-left without a second
ornament on the table or hair. Stop for A/B selection, promote the selected
PNG byte-for-byte, run the edit gate, and commit:

```sh
git commit -m "feat: accept Akari v1.3 holiday scene 02"
```

- [ ] **Step 3: Generate and select Scene 03 at 09:10**

Render Scene 03 A/B prompts with the five authorities. Review the high-oblique
breakfast composition, one-person place setting, worn ornament, relaxed face,
complete hands and lower body, morning light, and absence of any implied second
person. Stop for selection, promote, verify bytes/hashes, run the edit gate,
and commit:

```sh
git commit -m "feat: accept Akari v1.3 holiday scene 03"
```

- [ ] **Step 4: Build and approve the Act 1 contact sheet**

```sh
bash -lc 'uv run python scripts/build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py --scope act --act 1'
```

Open the sheet and verify these exact checks:

```yaml
checks:
  scene_order_and_morning_light: pass
  identity_and_young_adult_read: pass
  fixed_room_and_furniture_scale: pass
  ornament_off_to_on_continuity: pass
  base_outfit_and_bare_feet: pass
  one_person_prop_continuity: pass
```

Write `evidence/reviews/act-1.yaml` with `scope: act-1`, `status: review`, the
checks above, and `findings: []`. Run `approve-act --act 1`, then
`validate-act --act 1`. Commit only the Act review:

```sh
git add akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/evidence/reviews/act-1.yaml
git commit -m "docs: approve Akari v1.3 holiday Act 1"
```

### Task 8: Produce and approve Act 2 midday

**Files:**

- Create locally: canonical A/B candidates for Scene 04 and 05.
- Create: `accepted/scene-04.png`, `accepted/scene-05.png`.
- Create: `evidence/reviews/scene-04.yaml`, `scene-05.yaml`, and
  `act-2.yaml`.
- Modify: `manifest/scenes/index.yaml`.

**Interfaces:**

- Consumes: accepted Scene 06 plus the fixed authorities.
- Produces: the approved Scene 04-06 midday sequence.

- [ ] **Step 1: Generate and select Scene 04 at 10:24**

Render independent A/B prompts after opening the five authorities. Review the
75-90 degree laundry-sorting composition, full worn ornament, connected limbs,
one person's clothing only, stable rug/table/bed locations, and clear daylight.
Stop for selection, promote byte-for-byte, run the edit gate, and commit
`feat: accept Akari v1.3 holiday scene 04`.

- [ ] **Step 2: Generate and select Scene 05 at 11:48**

Render independent A/B prompts after opening the five authorities. Review the
45-60 degree kitchen composition, safe body and hand relationship to utensils,
one-person food quantity, worn ornament, fixed room orientation, and no
readable packaging. Stop for selection, promote, verify, run the edit gate,
and commit `feat: accept Akari v1.3 holiday scene 05`.

- [ ] **Step 3: Build and approve the Act 2 contact sheet**

Build `--scope act --act 2`. Verify exactly:

```yaml
checks:
  scene_order_and_midday_light: pass
  identity_and_overhead_pilot_match: pass
  fixed_room_and_furniture_scale: pass
  worn_ornament_continuity: pass
  base_outfit_and_bare_feet: pass
  laundry_food_phone_prop_progression: pass
```

Write `act-2.yaml`, run `approve-act --act 2`, run `validate-act --act 2`, and
commit `docs: approve Akari v1.3 holiday Act 2`.

### Task 9: Produce and approve Act 3 afternoon to evening

**Files:**

- Create locally: canonical A/B candidates for Scene 07, 08, and 09.
- Create: `accepted/scene-07.png` through `accepted/scene-09.png`.
- Create: scene reviews and `evidence/reviews/act-3.yaml`.
- Modify: `manifest/scenes/index.yaml`.

**Interfaces:**

- Consumes: fixed authorities and completed morning/midday prop state.
- Produces: the approved reading→nap→window transition.

- [ ] **Step 1: Generate and select Scene 07 at 14:32**

Use exact Scene 07 prompts and five authorities. Review the 75-90 degree
prone-reading pose, connected shoulders/pelvis/legs, ordinary nonsexual
framing, worn ornament, book orientation, and stable room. Stop for selection,
promote, verify, run the edit gate, and commit
`feat: accept Akari v1.3 holiday scene 07`.

- [ ] **Step 2: Generate and select Scene 08 at 15:47**

Use exact Scene 08 prompts and references. Review the curled nap anatomy,
open-book continuity, ornament fully visible on the table rather than hair,
true-overhead camera, and unchanged base outfit. Stop for selection, promote,
verify, run the edit gate, and commit
`feat: accept Akari v1.3 holiday scene 08`.

- [ ] **Step 3: Generate and select Scene 09 at 17:26**

Use exact Scene 09 prompts and references. Review the 45-60 degree window
stretch, complete worn ornament, added thin cardigan and indoor socks, natural
shoulder/arm extension, healthy legs, fixed window placement, and amber evening
light. Stop for selection, promote, verify, run the edit gate, and commit
`feat: accept Akari v1.3 holiday scene 09`.

- [ ] **Step 4: Build and approve the Act 3 contact sheet**

Verify exactly:

```yaml
checks:
  scene_order_and_afternoon_to_amber_light: pass
  identity_and_body_continuity: pass
  fixed_room_and_furniture_scale: pass
  ornament_worn_off_worn_continuity: pass
  cardigan_and_socks_added_only_in_scene_09: pass
  book_nap_window_prop_progression: pass
```

Write `act-3.yaml`, approve, validate, and commit
`docs: approve Akari v1.3 holiday Act 3`.

### Task 10: Produce and approve Act 4 night

**Files:**

- Create locally: canonical A/B candidates for Scene 10, 11, and 12.
- Create: `accepted/scene-10.png` through `accepted/scene-12.png`.
- Create: scene reviews and `evidence/reviews/act-4.yaml`.
- Modify: `manifest/scenes/index.yaml`.

**Interfaces:**

- Consumes: all fixed authorities and completed daytime continuity.
- Produces: the approved dinner→stretch→bed ending.

- [ ] **Step 1: Generate and select Scene 10 at 19:04**

Use exact Scene 10 A/B prompts. Review the true-overhead one-person dinner,
cardigan/socks, worn ornament, stable low table, believable hands and food,
warm indoor light with blue-gray window, and accumulated but controlled props.
Stop for selection, promote, verify, run the edit gate, and commit
`feat: accept Akari v1.3 holiday scene 10`.

- [ ] **Step 2: Generate and select Scene 11 at 21:18**

Use exact Scene 11 A/B prompts. Review the 45-60 degree stretch, ordinary
nonsexual framing, natural weight and healthy legs, cardigan/socks, worn
ornament, and unchanged room. Stop for selection, promote, verify, run the edit
gate, and commit `feat: accept Akari v1.3 holiday scene 11`.

- [ ] **Step 3: Generate and select Scene 12 at 23:41**

Use exact Scene 12 A/B prompts. Review the true-overhead bed composition,
connected body under bedding, cardigan/socks removed, complete ornament back at
the pillow, calm pre-sleep expression, and visual echo of Scene 01. Stop for
selection, promote, verify, run the edit gate, and commit
`feat: accept Akari v1.3 holiday scene 12`.

- [ ] **Step 4: Build and approve the Act 4 contact sheet**

Verify exactly:

```yaml
checks:
  scene_order_and_night_light: pass
  identity_and_body_continuity: pass
  fixed_room_and_furniture_scale: pass
  ornament_worn_to_visible_off_pillow: pass
  cardigan_and_socks_removed_only_in_scene_12: pass
  dinner_stretch_bed_prop_progression: pass
```

Write `act-4.yaml`, approve, validate, and commit
`docs: approve Akari v1.3 holiday Act 4`.

### Task 11: Approve full continuity and select the cover source

**Files:**

- Create locally: `evidence/contact-sheets/full-continuity.webp`.
- Create: `evidence/reviews/full-continuity.yaml`.
- Modify: `manifest/render.json`.

**Interfaces:**

- Consumes: twelve accepted scenes and four accepted Act reviews.
- Produces: the final continuity lock and one machine-readable cover source for
  the PDF model.

- [ ] **Step 1: Build and open the full continuity sheet**

```sh
bash -lc 'uv run python scripts/build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py --scope full'
```

Open the full sheet at original resolution. Verify exact chronological order,
one identity, fixed room, seven overhead/five high-oblique views, morning→day→
amber→night light, ornament states, clothing layers, and movable-prop history.

- [ ] **Step 2: Ask the user to select the cover and stop**

Present the strongest all-pass choices from the allowed overhead set only:

```text
scene-01, scene-04, scene-06, scene-07, scene-08, scene-10, scene-12
```

Explain the cover crop trade-off for each finalist. Do not set
`manifest/render.json` before the user explicitly chooses one.

- [ ] **Step 3: Write the full review and approve the chosen cover**

Create this review with every value shown as `pass` and no Major findings:

```yaml
schema_version: 1
scope: full-continuity
status: review
checks:
  identity_and_young_adult_read: pass
  seven_overhead_five_high_oblique: pass
  fixed_room_and_furniture_scale: pass
  light_progression: pass
  outfit_layer_progression: pass
  ornament_wear_and_visible_removal: pass
  one_person_prop_continuity: pass
  nonsexual_everyday_framing: pass
  image_format_ratio_and_text_bans: pass
findings: []
```

Run the command with the user's literal selection:

```sh
bash -lc 'uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py approve-full --review evidence/reviews/full-continuity.yaml --cover-scene scene-06'
```

Replace `scene-06` only with another user-selected allowed scene. The command
sets review status `accepted`, stores the full-sheet SHA, and writes the cover
scene into `manifest/render.json` while leaving detail `scene-04` and
afterimage `scene-12` unchanged.

- [ ] **Step 4: Rebuild, validate, and commit the full lock**

```sh
bash -lc 'uv run python scripts/build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py --scope all-acts'
bash -lc 'uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py validate-act --act all'
bash -lc 'uv run python scripts/build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py --scope full'
bash -lc 'uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py validate-full'
git add \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/manifest/render.json \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/evidence/reviews/full-continuity.yaml
git commit -m "docs: lock Akari v1.3 holiday continuity"
```

### Task 12: Add the A4 portrait document model and renderer styles

**Files:**

- Create: `tools/pdf/nani-mo-shinai-hi-no-mitorizu-document.mjs`
- Create: `tools/pdf/nani-mo-shinai-hi-no-mitorizu-document.test.mjs`
- Modify: `tools/pdf/render.mjs`
- Modify: `tools/pdf/styles.css`

**Interfaces:**

- Consumes: twelve accepted PNGs and `manifest/render.json`.
- Produces: `naniMoShinaiHiNoMitorizuDocument` for the shared renderer.

- [ ] **Step 1: Write the failing Node document tests**

Assert exactly:

```js
assert.equal(
  naniMoShinaiHiNoMitorizuDocument.id,
  "akari-v1.3-nani-mo-shinai-hi-no-mitorizu",
);
assert.deepEqual(naniMoShinaiHiNoMitorizuDocument.pageSize, {
  widthIn: 8.27,
  heightIn: 11.69,
  previewWidth: 2480,
  previewHeight: 3508,
});
assert.equal(pages.length, 18);
assert.deepEqual(
  pages.map((page) => page.page),
  Array.from({ length: 18 }, (_, index) => index + 1),
);
```

Also assert:

- pages 4-15 map in order to scene 01-12;
- their native times are exactly the twelve approved times;
- every scene has one source and no dialogue;
- every asset path is package-local `accepted/scene-NN.png`;
- cover source equals the accepted non-null value in `render.json`;
- page 2 uses scene 04 and page 16 uses scene 12;
- output path is the approved release PDF;
- rendered HTML contains the Japanese title, all twelve times, release ID,
  PNG source path, and no scene action description;
- `render.mjs` resolves document name
  `nani-mo-shinai-hi-no-mitorizu`.

- [ ] **Step 2: Run the Node test and verify the missing-module failure**

```sh
bash -lc 'node --test tools/pdf/nani-mo-shinai-hi-no-mitorizu-document.test.mjs'
```

- [ ] **Step 3: Implement the document model**

Create the module with this exact data boundary:

```js
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const packageRoot = "akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu";
const render = JSON.parse(
  readFileSync(resolve(root, packageRoot, "manifest/render.json"), "utf-8"),
);
const sceneRows = [
  ["scene-01", "08:12"],
  ["scene-02", "08:36"],
  ["scene-03", "09:10"],
  ["scene-04", "10:24"],
  ["scene-05", "11:48"],
  ["scene-06", "13:06"],
  ["scene-07", "14:32"],
  ["scene-08", "15:47"],
  ["scene-09", "17:26"],
  ["scene-10", "19:04"],
  ["scene-11", "21:18"],
  ["scene-12", "23:41"],
];
```

Use the existing `artbook-plate` and `artbook-copy` block types. Do not add a
new renderer block. Create layouts:

```text
v13-holiday-cover
v13-holiday-detail
v13-holiday-title
v13-holiday-scene
v13-holiday-afterimage
v13-holiday-colophon
v13-holiday-back
```

Page 1 uses `render.cover_scene` with title
`何もしない日の見取り図`. Page 2 uses `render.detail_scene` without text.
Page 3 is title only. Pages 4-15 use the scene rows and time only. Page 16 uses
`render.afterimage_scene` without text. Page 17 contains exactly:

```text
Akari v1.3
Nani mo shinai hi no mitorizu
Version 1.0.0
2026-07-22
```

Page 18 contains the title, release ID, and `checksums.txt`.

- [ ] **Step 4: Register the document in the renderer**

Add one lazy loader to `documentLoaders`:

```js
"nani-mo-shinai-hi-no-mitorizu": async () => {
  const { naniMoShinaiHiNoMitorizuDocument } = await import(
    "./nani-mo-shinai-hi-no-mitorizu-document.mjs"
  );
  return naniMoShinaiHiNoMitorizuDocument;
},
```

Add the same name to the usage string. Do not change any existing document
name or default.

- [ ] **Step 5: Add isolated portrait CSS**

Hide headers and source chips only for the seven new layout classes. Give all
new pages `#f7f3ec` background. For scene pages:

```css
.layout-v13-holiday-scene .page-body {
  padding: 120px 180px 92px;
}

.layout-v13-holiday-scene .block-artbook-plate {
  gap: 30px;
}

.layout-v13-holiday-scene .artbook-frame {
  border: 1px solid rgba(63, 54, 46, 0.14);
  background: #ece7df;
}

.layout-v13-holiday-scene .artbook-time {
  position: static;
  justify-self: center;
  padding: 0;
  color: #5f5953;
  background: transparent;
  font-size: 38px;
  letter-spacing: 0.12em;
  backdrop-filter: none;
}
```

Add print equivalents `0.40in 0.60in 0.31in`, `0.10in` gap, and `0.13in`
time size. Cover/detail/afterimage use `object-fit: cover`; scene pages use the
existing `object-fit: contain`. Style the cover title as a native text overlay,
and keep detail/afterimage text-free. Do not modify existing artbook selectors.

- [ ] **Step 6: Run all Node tests and commit**

```sh
bash -lc 'npm run test:node'
git add tools/pdf/nani-mo-shinai-hi-no-mitorizu-document.mjs \
  tools/pdf/nani-mo-shinai-hi-no-mitorizu-document.test.mjs \
  tools/pdf/render.mjs tools/pdf/styles.css
git commit -m "feat: render Akari v1.3 portrait holiday artbook"
```

### Task 13: Add deterministic export, portrait PDF audit, and release gate

**Files:**

- Create: `scripts/export_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf.py`
- Create: `scripts/audit_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf.py`
- Replace placeholder test:
  `tests/test_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf_audit.py`
- Modify: `package.json`
- Modify: `tests/test_workflow_gate_contract.py`

**Interfaces:**

- Consumes: the completed document model and lifecycle lock.
- Produces: preview PNGs, deterministic release PDF, checksum, and full audit.

- [ ] **Step 1: Write failing audit unit tests**

Assert:

```python
audit.require_pdfinfo_contract(
    "Pages: 18\nPage size: 595.44 x 841.68 pts\n"
)
with self.assertRaisesRegex(audit.AuditError, "18 pages"):
    audit.require_pdfinfo_contract(
        "Pages: 17\nPage size: 595.44 x 841.68 pts\n"
    )
with self.assertRaisesRegex(audit.AuditError, "A4 portrait"):
    audit.require_pdfinfo_contract(
        "Pages: 18\nPage size: 841.68 x 595.44 pts\n"
    )
self.assertEqual(
    f"{'a' * 64}  akari-v1.3-nani-mo-shinai-hi-no-mitorizu.pdf",
    audit.checksum_line(audit.PDF, "a" * 64),
)
```

Add tests that searchable text requires the title, twelve times, `Akari v1.3`,
`Version 1.0.0`, and release ID. Add an OCR helper test that requires ASCII
time terms on pages 4-15 and the release ID on page 18.

- [ ] **Step 2: Verify the missing audit module**

```sh
bash -lc 'uv run python -m unittest tests.test_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf_audit -v'
```

- [ ] **Step 3: Implement the portrait audit**

Use these exact constants:

```python
EXPECTED_PAGE_COUNT = 18
EXPECTED_A4_POINTS = (595.44, 841.68)
EXPECTED_RENDER_SIZE = (2380, 3368)
OCR_PAGE_SIZE = (1440, 2036)
REQUIRED_TEXT = (
    "何もしない日の見取り図",
    "08:12", "08:36", "09:10", "10:24", "11:48", "13:06",
    "14:32", "15:47", "17:26", "19:04", "21:18", "23:41",
    "Akari v1.3", "Version 1.0.0",
    "akari-v1.3-nani-mo-shinai-hi-no-mitorizu",
)
OCR_REQUIRED_TERMS_BY_PAGE = {
    4: ("08:12",), 5: ("08:36",), 6: ("09:10",),
    7: ("10:24",), 8: ("11:48",), 9: ("13:06",),
    10: ("14:32",), 11: ("15:47",), 12: ("17:26",),
    13: ("19:04",), 14: ("21:18",), 15: ("23:41",),
    18: ("akari-v1.3-nani-mo-shinai-hi-no-mitorizu",),
}
```

Implement qpdf check, PDF page/size validation, embedded Unicode fonts,
`pdftotext`, checksum validation, 288-DPI raster, exact approximate rendered
size, nonblank content ratio, preview/PDF mean-delta comparison, and Tesseract
OCR at 1440px width. Before PDF structure checks, require
`validate_contract(ROOT, require_complete=True, require_release=True)`, all
Act validations, and accepted full-continuity review/hash.

The audit supports `--level structure|full`. Structure omits raster, preview
comparison, and OCR. Full runs all checks.

- [ ] **Step 4: Implement deterministic export**

The exporter runs exactly:

```python
subprocess.run(
    [
        "node", "tools/pdf/render.mjs", "--document",
        "nani-mo-shinai-hi-no-mitorizu", "--pdf",
    ],
    cwd=ROOT,
    check=True,
)
write_checksum(PDF)
```

It does not rebuild or modify accepted scene PNGs.

- [ ] **Step 5: Add exact build, audit, and release scripts**

Add:

```json
"build:v1-3:nani-mo-shinai-hi-no-mitorizu:previews": "node tools/pdf/render.mjs --document nani-mo-shinai-hi-no-mitorizu --previews",
"build:v1-3:nani-mo-shinai-hi-no-mitorizu:pdf": "uv run python scripts/export_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf.py",
"audit:v1-3:nani-mo-shinai-hi-no-mitorizu:pdf:structure": "uv run python scripts/audit_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf.py --level structure",
"audit:v1-3:nani-mo-shinai-hi-no-mitorizu:pdf": "uv run python scripts/audit_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf.py --level full",
"gate:release:v1-3:nani-mo-shinai-hi-no-mitorizu": "npm run gate:edit:v1-3:nani-mo-shinai-hi-no-mitorizu && uv run python scripts/build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py --scope all-acts && uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py validate-act --act all && uv run python scripts/build_v1_3_nani_mo_shinai_hi_no_mitorizu_contact_sheet.py --scope full && uv run python scripts/akari_v1_3_nani_mo_shinai_hi_no_mitorizu.py validate-full && npm run build:v1-3:nani-mo-shinai-hi-no-mitorizu:previews && npm run build:v1-3:nani-mo-shinai-hi-no-mitorizu:pdf && npm run audit:v1-3:nani-mo-shinai-hi-no-mitorizu:pdf && npm run gate:integration:v1-3"
```

Update the workflow contract with exact-string assertions. Confirm the edit
gate remains free of heavy tools while the release gate contains previews,
PDF, audit, and Base v1.3 integration exactly once.

- [ ] **Step 6: Run unit tests, then the serial release gate**

```sh
bash -lc 'uv run python -m unittest tests.test_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf_audit tests.test_workflow_gate_contract -v'
bash -lc 'npm run gate:release:v1-3:nani-mo-shinai-hi-no-mitorizu'
```

Expected: 18 previews, release PDF and checksum created, qpdf/fonts/text/raster/
OCR/preview comparison pass, then Base v1.3 integration passes.

- [ ] **Step 7: Commit release implementation and artifacts**

```sh
git add scripts/export_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf.py \
  scripts/audit_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf.py \
  tests/test_v1_3_nani_mo_shinai_hi_no_mitorizu_pdf_audit.py \
  tests/test_workflow_gate_contract.py package.json \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/release/akari-v1.3-nani-mo-shinai-hi-no-mitorizu.pdf \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/release/checksums.txt
git commit -m "feat: release Akari v1.3 overhead holiday artbook"
```

### Task 14: Close documentation and prove cross-version regression safety

**Files:**

- Modify: `akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/README.md`
- Modify: `akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/manifest/book.yaml`
- Test: existing named gates.

**Interfaces:**

- Consumes: completed release and all review evidence.
- Produces: a documented, verified, clean branch ready for integration.

- [ ] **Step 1: Write a failing completion-doc assertion**

Add to the artbook contract test:

```python
readme = (PACKAGE / "README.md").read_text(encoding="utf-8")
self.assertIn("Status: complete", readme)
self.assertIn("12 accepted scenes", readme)
self.assertIn("18-page A4 portrait PDF", readme)
self.assertIn("Base continuity: Pass", readme)
```

Run the focused test and confirm it fails while README still says production.

- [ ] **Step 2: Complete README and book metadata**

Record status complete, accepted room anchor, scene 01-12 paths, selected cover
scene, four accepted Act reviews, full continuity Pass, release PDF, checksum,
and exact build/audit commands. Set `manifest/book.yaml` release status to
`complete` without changing its title, page geometry, page count, times, or
release path.

- [ ] **Step 3: Run focused and release verification from committed inputs**

```sh
bash -lc 'npm run gate:release:v1-3:nani-mo-shinai-hi-no-mitorizu'
bash -lc 'npm run gate:integration:v1-2'
git diff --exit-code -- akari-v1.2 legacy/akari-v1.2-pre-natural-form
git diff --check
```

The v1.3 release gate must pass after the docs change, the v1.2 integration
gate must pass serially, and the versioned v1.2/legacy diff command must be
empty. Existing untracked v1.2 candidate/comparison scratch is not selected or
modified.

- [ ] **Step 4: Lint, commit, and re-verify HEAD**

```sh
bash -lc 'npm run lint:md'
git add \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/README.md \
  akari-v1.3/artbooks/nani-mo-shinai-hi-no-mitorizu/manifest/book.yaml \
  tests/test_v1_3_nani_mo_shinai_hi_no_mitorizu_contract.py
git commit -m "docs: complete Akari v1.3 overhead holiday artbook"
bash -lc 'npm run gate:release:v1-3:nani-mo-shinai-hi-no-mitorizu'
git status --short --branch
```

Expected: committed HEAD passes the release gate; only pre-existing untracked
v1.2 scratch remains.

- [ ] **Step 5: Use the branch-completion workflow**

Invoke `superpowers:finishing-a-development-branch`. Present local merge,
push/PR, keep, or discard options. Do not merge, push, or delete the worktree
without the user's explicit choice.
