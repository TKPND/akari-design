# Akari v1.2 Canonical Turnaround Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and accept an AI-generation-first Akari v1.2 eight-view
canonical turnaround whose finished views are safe to reuse as the source pack
for a separately executed, exactly three-slot motion-pose phase.

**Architecture:** Treat the accepted front view as the root of a dependency
graph. Materialize generation requests only when every upstream angle is
already accepted, promote one reviewed candidate per angle into a tracked
finished WebP, and converge the left and right branches at the back view. Keep
candidate PNGs and contact sheets ignored while committing accepted assets,
review records, hashes, and deterministic tooling.

**Tech Stack:** Python 3.11, `unittest`, JSON manifests, Pillow 10-12,
ImageMagick inspection tools, built-in image generation, `uv run python`, npm
scripts, Git.

## Global Constraints

- Tooling and manifests may be implemented before the face-and-hair gate, but
  front-master request materialization and image generation must hard-stop
  unless `source/manifests/v1-2-face-hair/accepted-selection.json` records
  `decision: accepted`, its exact identity rules, and the SHA-256 of
  `source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp`.
- The gate is now satisfied. The accepted asset SHA-256 is
  `e130b7e00d98d02fc05f139ddc3b01f206e7eabf61987e4ad385ed7870fadb66`;
  Task 1 records the current selection-manifest SHA-256 and copies the complete
  accepted `identity_rules` into the turnaround identity lock.
- Use a 1024-by-1536 RGB portrait canvas, neutral standing pose, matched camera
  height, and shared sole baseline for all eight views.
- Left and right always use the character's perspective.
- Use the standard white oversized hoodie, gray pleated skirt, striped crew
  socks, chunky white-and-blue sneakers, and character-left pale-blue hair
  ornament. Exclude the shoulder bag.
- Generate two or three candidates per angle stage and accept exactly one image
  per angle before unlocking dependent angles.
- Keep corresponding major landmark ratios within 2 percent for left/right
  counterparts and within 3 percent across the eight-view set, measured against
  normalized crown-to-sole height.
- Never use mirrored shortcuts, aggressive warps, or seam-producing partial
  composites.
- Run `$akari-v1-1-image-review` on every likely accept before promotion and
  record the resulting identity, anatomy, and artifact findings in the stage
  review.
- Do not modify or replace `dist/akari-v1.1-settings.pdf`.
- Keep `source/generated/v1-2-turnaround/` and
  `evidence/v1-2-turnaround/contact-sheets/` ignored. Track review JSON and only
  explicitly accepted finished images.
- This is implementation Plan 1 of 2. It completes Phase 1 and writes a tracked
  Phase 2 handoff contract containing exactly the `walking`, `seated`, and
  `turning` motion slots. Creating and accepting those three images remains
  Plan 2 and the full design is not complete until Plan 2 passes.

---

## Scope Check

The approved design contains two sequential phases. Phase 1 is independently
testable: it produces eight accepted finished views, a dependency-aware request
history, review records, and a final alignment gate. Phase 2 consumes those
specific accepted files. This first implementation plan therefore completes
Phase 1 and creates an executable handoff contract with exactly three motion
slots; the second implementation plan generates and accepts the three motion
images. Completion of this plan must not be reported as completion of the full
approved design.

## Current Context

- Approved design:
  `docs/superpowers/specs/2026-07-10-akari-v1-2-turnaround-motion-design.md`
- Accepted v1.2 face-and-hair lock:
  `source/manifests/v1-2-face-hair/accepted-selection.json` and
  `source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp`
- Current accepted proportion lock:
  `source/generated/akari-body-proportion-option-b.webp`
- Current corrected standard-outfit front:
  `source/generated/akari-hoodie-front-proportion-corrected.webp`
- Existing back, profile, and front-three-quarter sources:
  `source/originals/v1_1_back.webp`, `source/originals/v1_1_真横.webp`,
  `source/originals/v1_1_髪飾り側_45deg.webp`, and
  `source/originals/v1_1_非髪飾り側45deg.webp`
- Existing footwear sources:
  `source/originals/v1_1_standard_foot_set.webp` and
  `source/originals/v1_1_shoes.webp`
- Existing patterns to follow:
  `tests/test_v1_2_face_hair_contract.py`,
  `tests/test_tonari_no_coordinate_contact_sheet.py`,
  `scripts/build_v1_2_face_hair_contact_sheet.py`, and
  `scripts/build_tonari_no_coordinate_generation_requests.py`

## File Structure

- Modify `.gitignore`
  - Ignore turnaround candidate images and contact sheets, but not reviews or
    accepted finished images.
- Modify `package.json`
  - Add request, contact-sheet, and promotion commands.
- Create `source/manifests/v1-2-turnaround/identity-lock.json`
  - Exact accepted face prerequisite and v1.1 body/outfit/detail inputs.
- Create `source/manifests/v1-2-turnaround/angle-slots.json`
  - Eight ordered angles and their dependency graph.
- Create `source/manifests/v1-2-turnaround/generation-requests.json`
  - Append-only history of materialized candidate requests.
- Create `source/manifests/v1-2-turnaround/accepted-angles.json`
  - Accepted finished image, SHA-256, source review, and landmark ratios per
    angle.
- Create `tests/test_v1_2_turnaround_contract.py`
  - Prerequisite, identity, slot graph, ignore, and package-script contracts.
- Create `tests/test_v1_2_turnaround_common.py`
  - Shared JSON, path, hash, and crown-to-sole landmark normalization contracts.
- Create `scripts/v1_2_turnaround_common.py`
  - Shared JSON, path, SHA-256, and landmark helpers used by all three tools.
- Create `tests/test_v1_2_turnaround_generation_requests.py`
  - Dependency gating and deterministic request materialization.
- Create `scripts/build_v1_2_turnaround_generation_requests.py`
  - Builds ready candidate requests only for unlocked slots.
- Create `tests/test_v1_2_turnaround_contact_sheet.py`
  - Stage/final sheet rendering and landmark tolerance checks.
- Create `scripts/build_v1_2_turnaround_contact_sheet.py`
  - Builds candidate sheets, final ordered sheet, and alignment guides.
- Create `tests/test_v1_2_turnaround_promotion.py`
  - Review validation, finished WebP conversion, hash recording, and dependency
    enforcement.
- Create `scripts/promote_v1_2_turnaround_candidate.py`
  - Promotes one accepted candidate per slot and updates accepted state.
- Create tracked review files under
  `evidence/v1-2-turnaround/reviews/`
  - One concrete review per generation stage plus one final eight-view review.
- Create tracked finished files under
  `source/finished/v1-2-turnaround/`
  - `front.webp`, paired three-quarter/profile/rear-three-quarter views, and
    `back.webp`.
- Create `dist/akari-v1.2-turnaround-contact-sheet.webp`
  - Final tracked eight-view comparison after all landmark gates pass.
- Create `source/manifests/v1-2-motion/phase-2-handoff.json`
  - Exactly three motion slots and the accepted eight-view paths and hashes
    required by the second implementation plan.
- Create `scripts/build_v1_2_motion_handoff.py`
  - Builds the Phase 2 contract only from the accepted eight-view manifest and
    accepted final review.

## Stable Interfaces

`scripts/v1_2_turnaround_common.py` exposes
`load_json(path: Path) -> dict`, `dump_json(path: Path, data: dict) -> None`,
`resolve_path(project_root: Path, path_text: str) -> Path`,
`sha256_file(path: Path) -> str`, and
`normalize_landmarks(landmark_y_px: dict[str, int | float],
image_height: int = 1536) -> dict[str, float]`.

`scripts/build_v1_2_turnaround_generation_requests.py` exposes
`validate_identity_lock(identity_lock: dict, project_root: Path) -> None`,
`accepted_by_slot(accepted_manifest: dict) -> dict[str, dict]`,
`build_ready_batch(slot_manifest: dict, identity_lock: dict,
accepted_manifest: dict, requested_slots: list[str], date_prefix: str,
revision: int) -> dict`,
and `merge_request_history(existing: dict, batch: dict) -> dict`.

`scripts/build_v1_2_turnaround_contact_sheet.py` exposes
`build_stage_contact_sheet(requests: list[dict], project_root: Path,
output_path: Path, columns: int = 3, enforce_stage_shape: bool = True) -> Path`,
`select_active_requests(manifest: dict, selected_slots: list[str] | None,
selected_batch_ids: list[str] | None) -> list[dict]`,
`validate_landmark_ratios(accepted_records: list[dict], pair_tolerance: float =
0.02, set_tolerance: float = 0.03) -> list[str]`, and
`build_final_contact_sheet(accepted_records: list[dict], project_root: Path,
output_path: Path) -> Path`.

`scripts/promote_v1_2_turnaround_candidate.py` exposes
`validate_review(review: dict, slot_manifest: dict, request_manifest: dict,
accepted_manifest: dict) -> None` and
`promote_review(review: dict, slot_manifest: dict, request_manifest: dict,
accepted_manifest: dict, project_root: Path) -> dict`, plus
`reopen_slots(review: dict, slot_manifest: dict, accepted_manifest: dict,
project_root: Path) -> dict`
for an explicitly user-approved rollback of inconsistent accepted angles.
Promotion computes hypothetical accepted state and runs normalized landmark
tolerance checks before writing any finished WebP or state manifest.

## Task 1: Lock The Accepted v1.2 Identity Prerequisite

**Files:**

- Read:
  `source/manifests/v1-2-face-hair/accepted-selection.json`
- Read:
  `source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp`
- Modify: `.gitignore`
- Create: `tests/test_v1_2_turnaround_contract.py`
- Create: `tests/test_v1_2_turnaround_common.py`
- Create: `scripts/v1_2_turnaround_common.py`
- Create: `source/manifests/v1-2-turnaround/identity-lock.json`
- Create: `source/manifests/v1-2-turnaround/generation-requests.json`
- Create: `source/manifests/v1-2-turnaround/accepted-angles.json`

**Interfaces:**

- Consumes: the accepted face-and-hair handoff described in Global Constraints.
- Produces: shared deterministic helpers, `identity-lock.json`, and empty
  request/acceptance manifests used by every subsequent task.

- [ ] **Step 1: Verify the external prerequisite before changing files**

Run:

```bash
uv run python - <<'PY'
import hashlib
import json
from pathlib import Path

selection_path = Path("source/manifests/v1-2-face-hair/accepted-selection.json")
asset_path = Path("source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp")
if not selection_path.is_file():
    raise SystemExit(f"missing accepted face selection: {selection_path}")
selection = json.loads(selection_path.read_text(encoding="utf-8"))
if selection.get("decision") != "accepted":
    raise SystemExit(f"face selection is not accepted: {selection.get('decision')}")
if selection.get("accepted_asset") != asset_path.as_posix():
    raise SystemExit("accepted face path does not match the canonical handoff")
if not asset_path.is_file():
    raise SystemExit(f"missing accepted face asset: {asset_path}")
digest = hashlib.sha256(asset_path.read_bytes()).hexdigest()
if digest != selection.get("accepted_asset_sha256"):
    raise SystemExit("accepted face SHA-256 does not match its selection manifest")
if not selection.get("identity_rules"):
    raise SystemExit("accepted face selection has no identity rules")
print("v1.2 face-and-hair prerequisite: accepted")
PY
```

Expected: `v1.2 face-and-hair prerequisite: accepted`. If this command fails,
Tasks 1 through 5 may still implement and test tooling with a blocked gate
fixture, but Task 6 request materialization and image generation must not run.

- [ ] **Step 2: Write the failing prerequisite and identity contract**

Create `tests/test_v1_2_turnaround_contract.py`:

```python
import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/v1-2-turnaround"
IDENTITY_LOCK = MANIFEST_DIR / "identity-lock.json"
ANGLE_SLOTS = MANIFEST_DIR / "angle-slots.json"
GENERATION_REQUESTS = MANIFEST_DIR / "generation-requests.json"
ACCEPTED_ANGLES = MANIFEST_DIR / "accepted-angles.json"
SELECTION = ROOT / "source/manifests/v1-2-face-hair/accepted-selection.json"
FACE_ASSET = ROOT / "source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp"
COLLECTION_ID = "akari-v1.2-canonical-turnaround"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class AkariV12TurnaroundContractTest(unittest.TestCase):
    def test_face_hair_prerequisite_is_explicitly_accepted(self):
        self.assertTrue(SELECTION.is_file())
        selection = load_json(SELECTION)
        self.assertEqual("accepted", selection["decision"])
        self.assertEqual(
            "source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp",
            selection["accepted_asset"],
        )
        self.assertTrue(FACE_ASSET.is_file())
        self.assertEqual(
            selection["accepted_asset_sha256"],
            hashlib.sha256(FACE_ASSET.read_bytes()).hexdigest(),
        )
        self.assertTrue(selection["identity_rules"])

    def test_identity_lock_records_exact_sources(self):
        manifest = load_json(IDENTITY_LOCK)
        self.assertEqual(1, manifest["schema_version"])
        self.assertEqual(COLLECTION_ID, manifest["collection_id"])
        self.assertEqual("accepted", manifest["prerequisite"]["required_status"])
        selection = load_json(SELECTION)
        self.assertEqual(
            hashlib.sha256(SELECTION.read_bytes()).hexdigest(),
            manifest["prerequisite"]["selection_manifest_sha256"],
        )
        self.assertEqual(
            selection["accepted_asset_sha256"],
            manifest["prerequisite"]["accepted_asset_sha256"],
        )
        self.assertEqual(selection["identity_rules"], manifest["identity_rules"])
        self.assertEqual((1024, 1536), tuple(manifest["canvas"][key] for key in ("width", "height")))
        for entry in manifest["reference_inputs"]:
            self.assertTrue((ROOT / entry["path"]).is_file(), entry["path"])

    def test_working_outputs_are_ignored_but_reviews_are_trackable(self):
        ignored = [
            "source/generated/v1-2-turnaround/example.png",
            "evidence/v1-2-turnaround/contact-sheets/example.webp",
        ]
        tracked = "evidence/v1-2-turnaround/reviews/example.json"
        for path in ignored:
            result = subprocess.run(
                ["git", "check-ignore", path],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
        result = subprocess.run(
            ["git", "check-ignore", tracked],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, result.returncode)

    def test_state_manifests_start_empty(self):
        requests = load_json(GENERATION_REQUESTS)
        accepted = load_json(ACCEPTED_ANGLES)
        self.assertEqual(COLLECTION_ID, requests["collection_id"])
        self.assertEqual([], requests["requests"])
        self.assertEqual({}, requests["active_batches"])
        self.assertEqual(COLLECTION_ID, accepted["collection_id"])
        self.assertEqual([], accepted["accepted_angles"])
```

Create `tests/test_v1_2_turnaround_common.py`:

```python
import tempfile
import unittest
from pathlib import Path

from scripts.v1_2_turnaround_common import (
    dump_json,
    load_json,
    normalize_landmarks,
    sha256_file,
)


LANDMARK_Y_PX = {
    "crown": 96,
    "chin": 270,
    "shoulder": 350,
    "hoodie_hem": 720,
    "skirt_hem": 850,
    "knee": 1080,
    "ankle": 1370,
    "sole": 1464,
}


class AkariV12TurnaroundCommonTest(unittest.TestCase):
    def test_json_round_trip_and_sha256_are_deterministic(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "nested/record.json"
            dump_json(path, {"name": "あかり", "value": 1})
            self.assertEqual({"name": "あかり", "value": 1}, load_json(path))
            self.assertEqual(64, len(sha256_file(path)))

    def test_landmarks_normalize_against_crown_to_sole_height(self):
        normalized = normalize_landmarks(LANDMARK_Y_PX)
        self.assertEqual(0.0, normalized["crown"])
        self.assertEqual(1.0, normalized["sole"])
        self.assertAlmostEqual(
            (LANDMARK_Y_PX["knee"] - LANDMARK_Y_PX["crown"])
            / (LANDMARK_Y_PX["sole"] - LANDMARK_Y_PX["crown"]),
            normalized["knee"],
            places=6,
        )

    def test_landmarks_reject_invalid_order_and_canvas_values(self):
        invalid_order = dict(LANDMARK_Y_PX, chin=80)
        with self.assertRaisesRegex(ValueError, "strictly increasing"):
            normalize_landmarks(invalid_order)
        invalid_canvas = dict(LANDMARK_Y_PX, sole=1536)
        with self.assertRaisesRegex(ValueError, "inside the image"):
            normalize_landmarks(invalid_canvas)
```

- [ ] **Step 3: Run the contract and verify it fails**

Run:

```bash
uv run python -m unittest tests.test_v1_2_turnaround_contract -v
```

Expected: FAIL because the shared module, `identity-lock.json`, the ignore
entries, and state manifests do not exist.

- [ ] **Step 4: Implement the shared deterministic helpers**

Create `scripts/v1_2_turnaround_common.py`:

```python
from __future__ import annotations

import hashlib
import json
from pathlib import Path


LANDMARK_NAMES = (
    "crown",
    "chin",
    "shoulder",
    "hoodie_hem",
    "skirt_hem",
    "knee",
    "ankle",
    "sole",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def resolve_path(project_root: Path, path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else project_root / path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_landmarks(
    landmark_y_px: dict[str, int | float],
    image_height: int = 1536,
) -> dict[str, float]:
    if set(landmark_y_px) != set(LANDMARK_NAMES):
        raise ValueError("landmark_y_px must contain the eight canonical landmarks")
    values = [float(landmark_y_px[name]) for name in LANDMARK_NAMES]
    if not all(0 <= value < image_height for value in values):
        raise ValueError("landmark y values must be inside the image")
    if any(first >= second for first, second in zip(values, values[1:])):
        raise ValueError("landmark y values must be strictly increasing")
    crown = float(landmark_y_px["crown"])
    standing_height = float(landmark_y_px["sole"]) - crown
    return {
        name: round((float(landmark_y_px[name]) - crown) / standing_height, 6)
        for name in LANDMARK_NAMES
    }
```

- [ ] **Step 5: Add only the two working-output ignore entries**

Append to `.gitignore`:

```gitignore
source/generated/v1-2-turnaround/
evidence/v1-2-turnaround/contact-sheets/
```

Do not ignore `evidence/v1-2-turnaround/reviews/` or
`source/finished/v1-2-turnaround/`.

- [ ] **Step 6: Create the identity lock**

Create `source/manifests/v1-2-turnaround/identity-lock.json`:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.2-canonical-turnaround",
  "identity_version": "akari-v1.2-standard-face-v1",
  "prerequisite": {
    "selection_manifest": "source/manifests/v1-2-face-hair/accepted-selection.json",
    "selection_manifest_sha256": "f5d552b01b5251c16c93f380e25d4f62f1dc595fa951d586861335c2d98490c0",
    "accepted_asset": "source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp",
    "accepted_asset_sha256": "e130b7e00d98d02fc05f139ddc3b01f206e7eabf61987e4ad385ed7870fadb66",
    "source_candidate_sha256": "ad2044cfa407df4ba884c9fa503e0cad7be2a38de77e3865480ccbf2674b2805",
    "required_status": "accepted"
  },
  "identity_rules": {
    "age_impression": "early-20s university-age young adult; not underage and not older-sister-like",
    "face": [
      "Y1 face direction",
      "warm amber eyes",
      "small restrained mouth",
      "rounded cheeks and compact rounded chin"
    ],
    "hair": [
      "warm brown short bob",
      "v1.1-like bang grouping",
      "subtle cheek-side face framing",
      "airy natural short-bob tips"
    ],
    "hair_ornament": {
      "side": "character-left",
      "upper": "small pale-blue crossed X-shaped hairpins",
      "lower": "compact pale-blue ribbon-like loop immediately below",
      "trailing_strand_count": 2,
      "hard_rejects": [
        "missing upper or lower component",
        "wrong-side placement",
        "flower",
        "jewel",
        "oversized fashion bow",
        "large dangling ribbon"
      ]
    },
    "outfit_context": "white oversized hoodie",
    "layout": [
      "same crop as the accepted source",
      "same pose as the accepted source",
      "same background layout as the accepted source",
      "1024x1536 portrait aspect ratio"
    ]
  },
  "canvas": {
    "width": 1024,
    "height": 1536,
    "mode": "RGB",
    "camera_height": "matched",
    "pose": "neutral_standing",
    "sole_baseline": "shared"
  },
  "outfit_lock": {
    "top": "white oversized hoodie",
    "bottom": "gray pleated skirt",
    "socks": "white crew socks with two pale-blue stripes",
    "shoes": "chunky white sneakers with pale-blue accents",
    "hair_ornament": "small pale-blue character-left hair ornament",
    "excluded_accessories": ["shoulder bag"]
  },
  "reference_inputs": [
    {
      "role": "face_hair",
      "path": "source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp"
    },
    {
      "role": "body_proportion",
      "path": "source/generated/akari-body-proportion-option-b.webp"
    },
    {
      "role": "standard_outfit_front",
      "path": "source/generated/akari-hoodie-front-proportion-corrected.webp"
    },
    {
      "role": "standard_outfit_back",
      "path": "source/originals/v1_1_back.webp"
    },
    {
      "role": "hairpin_side_front_45",
      "path": "source/originals/v1_1_髪飾り側_45deg.webp"
    },
    {
      "role": "non_hairpin_side_front_45",
      "path": "source/originals/v1_1_非髪飾り側45deg.webp"
    },
    {
      "role": "legacy_profile",
      "path": "source/originals/v1_1_真横.webp"
    },
    {
      "role": "footwear_sock",
      "path": "source/originals/v1_1_standard_foot_set.webp"
    },
    {
      "role": "sneaker_construction",
      "path": "source/originals/v1_1_shoes.webp"
    }
  ]
}
```

- [ ] **Step 7: Create empty request and accepted-angle state**

Create `source/manifests/v1-2-turnaround/generation-requests.json`:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.2-canonical-turnaround",
  "prompt_template_version": "akari_v1_2_turnaround_adjacent_angle_v1",
  "active_batches": {},
  "requests": []
}
```

Create `source/manifests/v1-2-turnaround/accepted-angles.json`:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.2-canonical-turnaround",
  "accepted_angles": []
}
```

- [ ] **Step 8: Run the contract and verify the prerequisite layer passes**

Run:

```bash
uv run python -m unittest \
  tests.test_v1_2_turnaround_common \
  tests.test_v1_2_turnaround_contract -v
```

Expected: PASS for the Task 1 helper and contract tests.

- [ ] **Step 9: Commit the prerequisite contract**

```bash
git add .gitignore scripts/v1_2_turnaround_common.py \
  tests/test_v1_2_turnaround_common.py \
  tests/test_v1_2_turnaround_contract.py \
  source/manifests/v1-2-turnaround
git commit -m "test: lock akari v1.2 turnaround prerequisite"
```

## Task 2: Define The Eight-View Dependency Graph

**Files:**

- Modify: `tests/test_v1_2_turnaround_contract.py`
- Create: `source/manifests/v1-2-turnaround/angle-slots.json`

**Interfaces:**

- Consumes: `identity-lock.json` from Task 1.
- Produces: eight stable slot names and `upstream_slots` consumed by the request
  builder and promotion script.

- [ ] **Step 1: Add the failing slot-graph tests**

Append these methods to `AkariV12TurnaroundContractTest`:

```python
    def test_angle_slots_are_complete_and_canonical(self):
        manifest = load_json(ANGLE_SLOTS)
        slots = manifest["slots"]
        self.assertEqual(COLLECTION_ID, manifest["collection_id"])
        self.assertEqual(
            [
                "front",
                "character-left-front-three-quarter",
                "character-left-profile",
                "character-left-rear-three-quarter",
                "back",
                "character-right-rear-three-quarter",
                "character-right-profile",
                "character-right-front-three-quarter",
            ],
            [slot["slug"] for slot in slots],
        )
        self.assertEqual(list(range(1, 9)), [slot["angle_order"] for slot in slots])
        self.assertEqual(8, len({slot["azimuth_degrees"] for slot in slots}))

    def test_angle_dependencies_form_two_branches_that_converge_at_back(self):
        slots = {slot["slug"]: slot for slot in load_json(ANGLE_SLOTS)["slots"]}
        self.assertEqual([], slots["front"]["upstream_slots"])
        self.assertEqual(
            ["front"],
            slots["character-left-front-three-quarter"]["upstream_slots"],
        )
        self.assertEqual(
            ["front", "character-left-front-three-quarter"],
            slots["character-left-profile"]["upstream_slots"],
        )
        self.assertEqual(
            ["front", "character-left-front-three-quarter", "character-left-profile"],
            slots["character-left-rear-three-quarter"]["upstream_slots"],
        )
        self.assertEqual(
            ["front"],
            slots["character-right-front-three-quarter"]["upstream_slots"],
        )
        self.assertEqual(
            ["front", "character-right-front-three-quarter"],
            slots["character-right-profile"]["upstream_slots"],
        )
        self.assertEqual(
            ["front", "character-right-front-three-quarter", "character-right-profile"],
            slots["character-right-rear-three-quarter"]["upstream_slots"],
        )
        self.assertEqual(
            ["front", "character-left-rear-three-quarter", "character-right-rear-three-quarter"],
            slots["back"]["upstream_slots"],
        )

    def test_slot_orientation_and_hair_ornament_rules_are_explicit(self):
        allowed_sides = {"center", "character_left", "character_right"}
        allowed_visibility = {"prominent", "visible", "partial", "occluded"}
        for slot in load_json(ANGLE_SLOTS)["slots"]:
            with self.subTest(slot=slot["slug"]):
                self.assertIn(slot["side"], allowed_sides)
                self.assertIn(slot["hair_ornament_visibility"], allowed_visibility)
                self.assertEqual(3, slot["candidate_count"])
                self.assertEqual("neutral_standing", slot["pose"])
                self.assertTrue(slot["japanese_title"])
```

- [ ] **Step 2: Run the contract and verify the missing manifest fails**

Run:

```bash
uv run python -m unittest tests.test_v1_2_turnaround_contract -v
```

Expected: FAIL with `FileNotFoundError` for `angle-slots.json`.

- [ ] **Step 3: Create the complete angle-slot manifest**

Create `source/manifests/v1-2-turnaround/angle-slots.json`:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.2-canonical-turnaround",
  "title": "Akari v1.2 Canonical Turnaround",
  "reference_pack_version": "akari-v1.2-turnaround-lock-v1",
  "strategy": {
    "production_order": "front_to_adjacent_angles_then_back_convergence",
    "review_order": "paired_counterparts_before_advancing",
    "candidate_count_per_angle": 3,
    "pdf_policy": "not_in_phase_1"
  },
  "slots": [
    {
      "angle_order": 1,
      "slug": "front",
      "japanese_title": "正面",
      "side": "center",
      "azimuth_degrees": 0,
      "view_family": "front",
      "hair_ornament_visibility": "visible",
      "upstream_slots": [],
      "legacy_reference_roles": ["standard_outfit_front", "body_proportion"],
      "candidate_count": 3,
      "pose": "neutral_standing"
    },
    {
      "angle_order": 2,
      "slug": "character-left-front-three-quarter",
      "japanese_title": "キャラクター左・前45度",
      "side": "character_left",
      "azimuth_degrees": 45,
      "view_family": "front_three_quarter",
      "hair_ornament_visibility": "prominent",
      "upstream_slots": ["front"],
      "legacy_reference_roles": ["hairpin_side_front_45"],
      "candidate_count": 3,
      "pose": "neutral_standing"
    },
    {
      "angle_order": 3,
      "slug": "character-left-profile",
      "japanese_title": "キャラクター左・真横",
      "side": "character_left",
      "azimuth_degrees": 90,
      "view_family": "profile",
      "hair_ornament_visibility": "prominent",
      "upstream_slots": ["front", "character-left-front-three-quarter"],
      "legacy_reference_roles": ["legacy_profile"],
      "candidate_count": 3,
      "pose": "neutral_standing"
    },
    {
      "angle_order": 4,
      "slug": "character-left-rear-three-quarter",
      "japanese_title": "キャラクター左・後45度",
      "side": "character_left",
      "azimuth_degrees": 135,
      "view_family": "rear_three_quarter",
      "hair_ornament_visibility": "partial",
      "upstream_slots": ["front", "character-left-front-three-quarter", "character-left-profile"],
      "legacy_reference_roles": ["standard_outfit_back"],
      "candidate_count": 3,
      "pose": "neutral_standing"
    },
    {
      "angle_order": 5,
      "slug": "back",
      "japanese_title": "背面",
      "side": "center",
      "azimuth_degrees": 180,
      "view_family": "back",
      "hair_ornament_visibility": "partial",
      "upstream_slots": ["front", "character-left-rear-three-quarter", "character-right-rear-three-quarter"],
      "legacy_reference_roles": ["standard_outfit_back"],
      "candidate_count": 3,
      "pose": "neutral_standing"
    },
    {
      "angle_order": 6,
      "slug": "character-right-rear-three-quarter",
      "japanese_title": "キャラクター右・後45度",
      "side": "character_right",
      "azimuth_degrees": 225,
      "view_family": "rear_three_quarter",
      "hair_ornament_visibility": "occluded",
      "upstream_slots": ["front", "character-right-front-three-quarter", "character-right-profile"],
      "legacy_reference_roles": ["standard_outfit_back"],
      "candidate_count": 3,
      "pose": "neutral_standing"
    },
    {
      "angle_order": 7,
      "slug": "character-right-profile",
      "japanese_title": "キャラクター右・真横",
      "side": "character_right",
      "azimuth_degrees": 270,
      "view_family": "profile",
      "hair_ornament_visibility": "occluded",
      "upstream_slots": ["front", "character-right-front-three-quarter"],
      "legacy_reference_roles": ["legacy_profile"],
      "candidate_count": 3,
      "pose": "neutral_standing"
    },
    {
      "angle_order": 8,
      "slug": "character-right-front-three-quarter",
      "japanese_title": "キャラクター右・前45度",
      "side": "character_right",
      "azimuth_degrees": 315,
      "view_family": "front_three_quarter",
      "hair_ornament_visibility": "occluded",
      "upstream_slots": ["front"],
      "legacy_reference_roles": ["non_hairpin_side_front_45"],
      "candidate_count": 3,
      "pose": "neutral_standing"
    }
  ]
}
```

- [ ] **Step 4: Run the contract and verify the graph passes**

Run:

```bash
uv run python -m unittest tests.test_v1_2_turnaround_contract -v
```

Expected: PASS.

- [ ] **Step 5: Commit the angle graph**

```bash
git add tests/test_v1_2_turnaround_contract.py source/manifests/v1-2-turnaround/angle-slots.json
git commit -m "feat: define akari v1.2 turnaround angles"
```

## Task 3: Materialize Only Dependency-Ready Generation Requests

**Files:**

- Create: `tests/test_v1_2_turnaround_generation_requests.py`
- Create: `scripts/build_v1_2_turnaround_generation_requests.py`
- Modify: `package.json`
- Modify: `source/manifests/v1-2-turnaround/generation-requests.json`

**Interfaces:**

- Consumes: `identity-lock.json`, `angle-slots.json`, and
  `accepted-angles.json`.
- Produces: three concrete candidate requests per requested, unlocked slot and
  an append-only request history with exact reference paths.

- [ ] **Step 1: Write failing dependency-gating tests**

Create `tests/test_v1_2_turnaround_generation_requests.py`:

```python
import unittest

from scripts.build_v1_2_turnaround_generation_requests import (
    build_ready_batch,
    merge_request_history,
)


IDENTITY_LOCK = {
    "schema_version": 1,
    "collection_id": "akari-v1.2-canonical-turnaround",
    "outfit_lock": {
        "top": "white oversized hoodie",
        "bottom": "gray pleated skirt",
        "socks": "white crew socks with two pale-blue stripes",
        "shoes": "chunky white sneakers with pale-blue accents",
        "hair_ornament": "small pale-blue character-left hair ornament",
        "excluded_accessories": ["shoulder bag"],
    },
    "reference_inputs": [
        {"role": "face_hair", "path": "refs/face.webp"},
        {"role": "body_proportion", "path": "refs/body.webp"},
        {"role": "standard_outfit_front", "path": "refs/front.webp"},
        {"role": "footwear_sock", "path": "refs/footwear.webp"},
        {"role": "sneaker_construction", "path": "refs/sneaker.webp"},
        {"role": "hairpin_side_front_45", "path": "refs/left45.webp"},
    ],
}

SLOT_MANIFEST = {
    "schema_version": 1,
    "collection_id": "akari-v1.2-canonical-turnaround",
    "slots": [
        {
            "angle_order": 1,
            "slug": "front",
            "japanese_title": "正面",
            "side": "center",
            "azimuth_degrees": 0,
            "view_family": "front",
            "hair_ornament_visibility": "visible",
            "upstream_slots": [],
            "legacy_reference_roles": ["standard_outfit_front", "body_proportion"],
            "candidate_count": 3,
            "pose": "neutral_standing",
        },
        {
            "angle_order": 2,
            "slug": "character-left-front-three-quarter",
            "japanese_title": "キャラクター左・前45度",
            "side": "character_left",
            "azimuth_degrees": 45,
            "view_family": "front_three_quarter",
            "hair_ornament_visibility": "prominent",
            "upstream_slots": ["front"],
            "legacy_reference_roles": ["hairpin_side_front_45"],
            "candidate_count": 3,
            "pose": "neutral_standing",
        },
    ],
}


class AkariV12TurnaroundGenerationRequestsTest(unittest.TestCase):
    def test_front_is_ready_without_upstream_acceptance(self):
        batch = build_ready_batch(
            SLOT_MANIFEST,
            IDENTITY_LOCK,
            {"accepted_angles": []},
            ["front"],
            "20260710",
            1,
        )
        self.assertEqual(3, len(batch["requests"]))
        self.assertEqual(
            [
                "source/generated/v1-2-turnaround/20260710_front_r1_c1.png",
                "source/generated/v1-2-turnaround/20260710_front_r1_c2.png",
                "source/generated/v1-2-turnaround/20260710_front_r1_c3.png",
            ],
            [request["target_path"] for request in batch["requests"]],
        )

    def test_dependent_angle_is_blocked_until_front_is_accepted(self):
        with self.assertRaisesRegex(
            ValueError,
            "character-left-front-three-quarter requires accepted slot front",
        ):
            build_ready_batch(
                SLOT_MANIFEST,
                IDENTITY_LOCK,
                {"accepted_angles": []},
                ["character-left-front-three-quarter"],
                "20260710",
                1,
            )

    def test_dependent_angle_includes_the_accepted_neighbor(self):
        accepted = {
            "accepted_angles": [
                {
                    "slot": "front",
                    "accepted_path": "source/finished/v1-2-turnaround/front.webp",
                }
            ]
        }
        batch = build_ready_batch(
            SLOT_MANIFEST,
            IDENTITY_LOCK,
            accepted,
            ["character-left-front-three-quarter"],
            "20260710",
            1,
        )
        for request in batch["requests"]:
            self.assertIn(
                "source/finished/v1-2-turnaround/front.webp",
                request["reference_pack_inputs"],
            )
            self.assertIn("refs/left45.webp", request["reference_pack_inputs"])

    def test_request_history_is_append_only_and_idempotent(self):
        existing = {
            "schema_version": 1,
            "collection_id": "akari-v1.2-canonical-turnaround",
            "prompt_template_version": "akari_v1_2_turnaround_adjacent_angle_v1",
            "active_batches": {},
            "requests": [],
        }
        first_batch = build_ready_batch(
            SLOT_MANIFEST,
            IDENTITY_LOCK,
            {"accepted_angles": []},
            ["front"],
            "20260710",
            1,
        )
        with_history = merge_request_history(existing, first_batch)
        second_batch = build_ready_batch(
            SLOT_MANIFEST,
            IDENTITY_LOCK,
            {"accepted_angles": []},
            ["front"],
            "20260710",
            2,
        )
        revised = merge_request_history(with_history, second_batch)
        idempotent = merge_request_history(revised, second_batch)
        self.assertEqual(6, len(revised["requests"]))
        self.assertEqual(
            "batch:v1-2-turnaround:20260710:front:r2",
            revised["active_batches"]["front"],
        )
        self.assertEqual(revised, idempotent)
        with self.assertRaisesRegex(ValueError, "cannot reactivate older revision"):
            merge_request_history(revised, first_batch)
```

- [ ] **Step 2: Run the tests and verify the missing module fails**

Run:

```bash
uv run python -m unittest tests.test_v1_2_turnaround_generation_requests -v
```

Expected: FAIL with `ModuleNotFoundError` for
`scripts.build_v1_2_turnaround_generation_requests`.

- [ ] **Step 3: Implement the dependency-aware request builder**

Create `scripts/build_v1_2_turnaround_generation_requests.py`:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.v1_2_turnaround_common import dump_json, load_json, sha256_file


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/v1-2-turnaround"
IDENTITY_LOCK_PATH = MANIFEST_DIR / "identity-lock.json"
SLOT_MANIFEST_PATH = MANIFEST_DIR / "angle-slots.json"
ACCEPTED_ANGLES_PATH = MANIFEST_DIR / "accepted-angles.json"
OUTPUT_PATH = MANIFEST_DIR / "generation-requests.json"
COLLECTION_ID = "akari-v1.2-canonical-turnaround"
PROMPT_TEMPLATE_VERSION = "akari_v1_2_turnaround_adjacent_angle_v1"
FRONT_REFERENCE_ROLES = (
    "face_hair",
    "body_proportion",
    "standard_outfit_front",
    "footwear_sock",
    "sneaker_construction",
)
DEPENDENT_DETAIL_ROLES = (
    "face_hair",
    "footwear_sock",
    "sneaker_construction",
)


def validate_identity_lock(identity_lock: dict, project_root: Path) -> None:
    prerequisite = identity_lock["prerequisite"]
    selection_path = project_root / prerequisite["selection_manifest"]
    selection = load_json(selection_path)
    if sha256_file(selection_path) != prerequisite["selection_manifest_sha256"]:
        raise ValueError("v1.2 face-and-hair selection manifest hash drift")
    if selection.get("decision") != prerequisite["required_status"]:
        raise ValueError("v1.2 face-and-hair selection is not accepted")
    if selection.get("accepted_asset") != prerequisite["accepted_asset"]:
        raise ValueError("accepted face asset does not match identity lock")
    if selection.get("accepted_asset_sha256") != prerequisite["accepted_asset_sha256"]:
        raise ValueError("accepted face SHA-256 does not match identity lock")
    if selection.get("identity_rules") != identity_lock["identity_rules"]:
        raise ValueError("accepted face identity rules do not match identity lock")
    accepted_asset = project_root / prerequisite["accepted_asset"]
    if sha256_file(accepted_asset) != prerequisite["accepted_asset_sha256"]:
        raise ValueError("accepted face asset hash drift")
    for entry in identity_lock["reference_inputs"]:
        path = project_root / entry["path"]
        if not path.is_file():
            raise ValueError(f"missing identity reference: {entry['path']}")


def accepted_by_slot(accepted_manifest: dict) -> dict[str, dict]:
    return {record["slot"]: record for record in accepted_manifest["accepted_angles"]}


def unique_paths(paths: list[str]) -> list[str]:
    return list(dict.fromkeys(paths))


def build_prompt(slot: dict, outfit_lock: dict) -> str:
    return "\n".join(
        [
            f"Create one clean full-body Akari v1.2 canonical turnaround candidate for {slot['japanese_title']}.",
            (
                "Use every attached reference image as a mandatory identity, body, outfit, angle, "
                "and construction source. Do not generate from prompt text alone."
            ),
            (
                "Identity lock: use the accepted Akari v1.2 standard face and hair; warm-brown "
                "eyes; short warm-brown bob; adult early-20s Japanese young woman character "
                "design; on character-left preserve the two-part pale-blue ornament: small "
                "crossed X-shaped hairpins above, compact ribbon-like loop immediately below, "
                "and exactly two thin trailing strands."
            ),
            (
                f"View lock: {slot['view_family']} at {slot['azimuth_degrees']} degrees from the "
                f"character's perspective; expected hair ornament visibility is "
                f"{slot['hair_ornament_visibility']}."
            ),
            (
                f"Outfit lock: {outfit_lock['top']}; {outfit_lock['bottom']}; "
                f"{outfit_lock['socks']}; {outfit_lock['shoes']}; no shoulder bag."
            ),
            (
                "Canvas and pose lock: 1024x1536 RGB portrait, neutral standing pose, matched "
                "camera height, shared sole baseline, full body visible, plain neutral background."
            ),
            (
                "Consistency lock: preserve head-to-body ratio, healthy thigh and calf volume, "
                "shoulder width, hoodie hem, skirt hem, knee height, ankle shape, and sneaker mass."
            ),
            (
                "No readable text, no logos, no watermarks, no border, no frame, no panel "
                "layout, no mirrored shortcut, no photorealistic live-action person."
            ),
        ]
    )


def build_acceptance(slot: dict) -> str:
    return " ".join(
        [
            "Identity Gate: must match the accepted Akari v1.2 face, hair, adult age impression, and character-left ornament.",
            "Geometry Gate: must preserve matched crown, chin, shoulder, hoodie hem, skirt hem, knee, ankle, and sole relationships.",
            "Outfit Gate: must preserve the standard hoodie, pleated skirt, striped socks, and sneaker construction.",
            f"Orientation Gate: must read as {slot['japanese_title']} without mirroring or side-label ambiguity.",
            "Quality Gate: clean anatomy and clothing continuity; no text, logo, watermark, frame, border, or panel layout.",
        ]
    )


def build_ready_batch(
    slot_manifest: dict,
    identity_lock: dict,
    accepted_manifest: dict,
    requested_slots: list[str],
    date_prefix: str,
    revision: int,
) -> dict:
    if revision < 1:
        raise ValueError("revision must be a positive integer")
    slots = {slot["slug"]: slot for slot in slot_manifest["slots"]}
    accepted = accepted_by_slot(accepted_manifest)
    role_paths = {entry["role"]: entry["path"] for entry in identity_lock["reference_inputs"]}
    requests = []
    active_batches = {}
    for requested_slot in requested_slots:
        if requested_slot not in slots:
            raise ValueError(f"unknown turnaround slot: {requested_slot}")
        slot = slots[requested_slot]
        upstream_paths = []
        for upstream_slot in slot["upstream_slots"]:
            if upstream_slot not in accepted:
                raise ValueError(f"{requested_slot} requires accepted slot {upstream_slot}")
            upstream_paths.append(accepted[upstream_slot]["accepted_path"])
        legacy_paths = [role_paths[role] for role in slot["legacy_reference_roles"]]
        if slot["upstream_slots"]:
            reference_paths = unique_paths(
                [role_paths["face_hair"]] + upstream_paths + legacy_paths
            )
            for role in DEPENDENT_DETAIL_ROLES:
                path = role_paths[role]
                if path not in reference_paths and len(reference_paths) < 5:
                    reference_paths.append(path)
        else:
            reference_paths = unique_paths(
                [role_paths[role] for role in FRONT_REFERENCE_ROLES]
                + legacy_paths
            )
        if len(reference_paths) > 5:
            raise ValueError(
                f"{requested_slot} exceeds the five-image generation reference limit"
            )
        batch_id = (
            f"batch:v1-2-turnaround:{date_prefix}:{requested_slot}:r{revision}"
        )
        active_batches[requested_slot] = batch_id
        for candidate_number in range(1, slot["candidate_count"] + 1):
            requests.append(
                {
                    "id": (
                        f"request:v1-2-turnaround:{date_prefix}:{requested_slot}:"
                        f"r{revision}:c{candidate_number}"
                    ),
                    "batch_id": batch_id,
                    "revision": revision,
                    "slot": requested_slot,
                    "angle_order": slot["angle_order"],
                    "candidate_number": candidate_number,
                    "japanese_title": slot["japanese_title"],
                    "side": slot["side"],
                    "azimuth_degrees": slot["azimuth_degrees"],
                    "view_family": slot["view_family"],
                    "required_upstream_slots": slot["upstream_slots"],
                    "reference_pack_inputs": reference_paths,
                    "target_path": (
                        "source/generated/v1-2-turnaround/"
                        f"{date_prefix}_{requested_slot}_r{revision}_c{candidate_number}.png"
                    ),
                    "prompt_template_version": PROMPT_TEMPLATE_VERSION,
                    "prompt": build_prompt(slot, identity_lock["outfit_lock"]),
                    "acceptance": build_acceptance(slot),
                    "review_plan": {
                        "initial_status": "draft_candidate",
                        "first_pass": "compare all three candidates on one stage contact sheet",
                        "outcomes": ["accept", "hold", "reject"],
                    },
                }
            )
    return {
        "schema_version": 1,
        "collection_id": COLLECTION_ID,
        "prompt_template_version": PROMPT_TEMPLATE_VERSION,
        "active_batches": active_batches,
        "requests": requests,
    }


def merge_request_history(existing: dict, batch: dict) -> dict:
    by_id = {request["id"]: request for request in existing["requests"]}
    for request in batch["requests"]:
        current = by_id.get(request["id"])
        if current is not None and current != request:
            raise ValueError(f"conflicting request id: {request['id']}")
        by_id[request["id"]] = request
    merged = dict(existing)
    merged["requests"] = sorted(
        by_id.values(),
        key=lambda item: (
            item["angle_order"],
            item["revision"],
            item["candidate_number"],
            item["id"],
        ),
    )
    active_batches = dict(existing.get("active_batches", {}))
    revisions_by_batch = {
        request["batch_id"]: request["revision"] for request in by_id.values()
    }
    for slot_name, batch_id in batch["active_batches"].items():
        current_batch = active_batches.get(slot_name)
        if (
            current_batch is not None
            and revisions_by_batch[current_batch] > revisions_by_batch[batch_id]
        ):
            raise ValueError(f"cannot reactivate older revision for {slot_name}")
    active_batches.update(batch["active_batches"])
    merged["active_batches"] = active_batches
    return merged


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build dependency-ready Akari v1.2 turnaround requests.")
    parser.add_argument("--slot", action="append", required=True)
    parser.add_argument("--date-prefix", default="20260710")
    parser.add_argument("--revision", type=int, default=1)
    parser.add_argument("--identity-lock", type=Path, default=IDENTITY_LOCK_PATH)
    parser.add_argument("--slots", type=Path, default=SLOT_MANIFEST_PATH)
    parser.add_argument("--accepted", type=Path, default=ACCEPTED_ANGLES_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    identity_lock = load_json(args.identity_lock)
    validate_identity_lock(identity_lock, ROOT)
    batch = build_ready_batch(
        load_json(args.slots),
        identity_lock,
        load_json(args.accepted),
        args.slot,
        args.date_prefix,
        args.revision,
    )
    existing = load_json(args.output)
    merged = merge_request_history(existing, batch)
    dump_json(args.output, merged)
    print(f"turnaround requests written: {len(batch['requests'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Add the package command**

Add this entry to `package.json` under `scripts`:

```json
"build:v1-2-turnaround:requests": "uv run python -m scripts.build_v1_2_turnaround_generation_requests"
```

Add this method to `AkariV12TurnaroundContractTest`:

```python
    def test_package_scripts_expose_turnaround_request_builder(self):
        scripts = load_json(ROOT / "package.json")["scripts"]
        self.assertEqual(
            "uv run python -m scripts.build_v1_2_turnaround_generation_requests",
            scripts["build:v1-2-turnaround:requests"],
        )
```

- [ ] **Step 5: Run targeted tests**

Run:

```bash
uv run python -m unittest \
  tests.test_v1_2_turnaround_contract \
  tests.test_v1_2_turnaround_generation_requests -v
```

Expected: PASS.

- [ ] **Step 6: Commit request materialization**

```bash
git add package.json scripts/build_v1_2_turnaround_generation_requests.py tests/test_v1_2_turnaround_contract.py tests/test_v1_2_turnaround_generation_requests.py
git commit -m "feat: gate akari v1.2 turnaround requests"
```

## Task 4: Build Stage Sheets And Validate Final Landmarks

**Files:**

- Create: `tests/test_v1_2_turnaround_contact_sheet.py`
- Create: `scripts/build_v1_2_turnaround_contact_sheet.py`
- Modify: `tests/test_v1_2_turnaround_contract.py`
- Modify: `package.json`

**Interfaces:**

- Consumes: materialized requests for stage sheets or accepted-angle records
  for the final sheet.
- Produces: ignored contact sheets and a deterministic list of landmark
  tolerance failures.

- [ ] **Step 1: Write failing rendering and landmark tests**

Create `tests/test_v1_2_turnaround_contact_sheet.py`:

```python
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.v1_2_turnaround_common import normalize_landmarks
from scripts.build_v1_2_turnaround_contact_sheet import (
    build_final_contact_sheet,
    build_stage_contact_sheet,
    validate_landmark_ratios,
)


LANDMARK_Y_PX = {
    "crown": 96,
    "chin": 270,
    "shoulder": 350,
    "hoodie_hem": 720,
    "skirt_hem": 850,
    "knee": 1080,
    "ankle": 1370,
    "sole": 1464,
}


def accepted_record(slot: str, path: str, drift_px: int = 0) -> dict:
    landmark_y_px = dict(LANDMARK_Y_PX)
    for name in ("chin", "shoulder", "hoodie_hem", "skirt_hem", "knee", "ankle"):
        landmark_y_px[name] += drift_px
    return {
        "slot": slot,
        "angle_order": 1,
        "accepted_path": path,
        "landmark_y_px": landmark_y_px,
        "normalized_landmarks": normalize_landmarks(landmark_y_px),
    }


class AkariV12TurnaroundContactSheetTest(unittest.TestCase):
    def test_stage_sheet_uses_existing_candidate_images(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            image_one = root / "one.png"
            image_two = root / "two.png"
            output = root / "stage.webp"
            Image.new("RGB", (1024, 1536), "#d9eee9").save(image_one)
            Image.new("RGB", (1024, 1536), "#f0dfd1").save(image_two)
            requests = [
                {
                    "slot": "front",
                    "batch_id": "batch:v1-2-turnaround:20260710:front:r1",
                    "revision": 1,
                    "candidate_number": 1,
                    "japanese_title": "正面",
                    "target_path": image_one.as_posix(),
                },
                {
                    "slot": "front",
                    "batch_id": "batch:v1-2-turnaround:20260710:front:r1",
                    "revision": 1,
                    "candidate_number": 2,
                    "japanese_title": "正面",
                    "target_path": image_two.as_posix(),
                },
            ]
            result = build_stage_contact_sheet(requests, root, output, columns=2)
            self.assertEqual(output, result)
            with Image.open(output) as sheet:
                self.assertEqual("RGB", sheet.mode)
                self.assertEqual((774, 638), sheet.size)

    def test_stage_sheet_rejects_a_missing_requested_candidate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            existing = root / "one.png"
            Image.new("RGB", (1024, 1536), "white").save(existing)
            requests = [
                {
                    "slot": "front",
                    "batch_id": "batch:v1-2-turnaround:20260710:front:r1",
                    "revision": 1,
                    "candidate_number": candidate_number,
                    "japanese_title": "正面",
                    "target_path": path.as_posix(),
                }
                for candidate_number, path in (
                    (1, existing),
                    (2, root / "missing.png"),
                )
            ]
            with self.assertRaisesRegex(ValueError, "missing requested candidate"):
                build_stage_contact_sheet(requests, root, root / "stage.webp")

    def test_landmark_validator_accepts_small_counterpart_drift(self):
        records = [
            accepted_record("character-left-profile", "left.webp"),
            accepted_record("character-right-profile", "right.webp", 7),
        ]
        self.assertEqual([], validate_landmark_ratios(records))

    def test_landmark_validator_reports_pair_and_set_drift(self):
        records = [
            accepted_record("character-left-profile", "left.webp"),
            accepted_record("character-right-profile", "right.webp", 55),
        ]
        errors = validate_landmark_ratios(records)
        self.assertTrue(any("counterpart" in error for error in errors))
        self.assertTrue(any("full-set" in error for error in errors))

    def test_final_sheet_rejects_landmark_drift(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            left = root / "left.webp"
            right = root / "right.webp"
            Image.new("RGB", (1024, 1536), "white").save(left)
            Image.new("RGB", (1024, 1536), "white").save(right)
            records = [
                accepted_record("character-left-profile", left.as_posix()),
                accepted_record("character-right-profile", right.as_posix(), 55),
            ]
            with self.assertRaisesRegex(ValueError, "landmark validation failed"):
                build_final_contact_sheet(records, root, root / "final.webp")
```

- [ ] **Step 2: Run the tests and verify the missing module fails**

Run:

```bash
uv run python -m unittest tests.test_v1_2_turnaround_contact_sheet -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement contact-sheet and landmark validation**

Create `scripts/build_v1_2_turnaround_contact_sheet.py`:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import statistics
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

from scripts.v1_2_turnaround_common import load_json, resolve_path


ROOT = Path(__file__).resolve().parents[1]
REQUESTS_PATH = ROOT / "source/manifests/v1-2-turnaround/generation-requests.json"
ACCEPTED_PATH = ROOT / "source/manifests/v1-2-turnaround/accepted-angles.json"
DEFAULT_OUTPUT = ROOT / "evidence/v1-2-turnaround/contact-sheets/turnaround.webp"
BACKGROUND = "#f7f3ee"
CARD_BACKGROUND = "#ffffff"
TEXT = "#2b2b2b"
GUIDE = "#4e9d92"
LANDMARK_NAMES = (
    "crown",
    "chin",
    "shoulder",
    "hoodie_hem",
    "skirt_hem",
    "knee",
    "ankle",
    "sole",
)
COUNTERPART_PAIRS = (
    ("character-left-front-three-quarter", "character-right-front-three-quarter"),
    ("character-left-profile", "character-right-profile"),
    ("character-left-rear-three-quarter", "character-right-rear-three-quarter"),
)


def load_font(size: int) -> ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(path).is_file():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def prepared_image(path: Path, size: tuple[int, int] = (360, 540)) -> Image.Image:
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        return ImageOps.contain(rgb, size, Image.Resampling.LANCZOS)


def build_stage_contact_sheet(
    requests: list[dict],
    project_root: Path,
    output_path: Path,
    columns: int = 3,
    enforce_stage_shape: bool = True,
) -> Path:
    if columns < 1:
        raise ValueError("columns must be at least 1")
    if not requests:
        raise ValueError("No active v1.2 turnaround requests selected")
    grouped = {}
    for request in requests:
        grouped.setdefault(request["slot"], []).append(request)
    if enforce_stage_shape:
        if len(grouped) not in {1, 2}:
            raise ValueError("a stage sheet must contain one slot or one counterpart pair")
        for slot, slot_requests in grouped.items():
            if len(slot_requests) not in {2, 3}:
                raise ValueError(f"{slot} must contain exactly two or three candidates")
            if len({request["batch_id"] for request in slot_requests}) != 1:
                raise ValueError(f"{slot} mixes request batches")
    found = []
    missing = []
    for request in requests:
        path = resolve_path(project_root, request["target_path"])
        if path.is_file():
            found.append((request, path))
        else:
            missing.append(request["target_path"])
    if missing:
        raise ValueError("missing requested candidate: " + ", ".join(missing))
    card_width, image_height, label_height, gap = 360, 540, 62, 18
    rows = math.ceil(len(found) / columns)
    sheet = Image.new(
        "RGB",
        (
            columns * card_width + (columns + 1) * gap,
            rows * (image_height + label_height) + (rows + 1) * gap,
        ),
        BACKGROUND,
    )
    draw = ImageDraw.Draw(sheet)
    title_font = load_font(16)
    small_font = load_font(12)
    for index, (request, path) in enumerate(found):
        row, column = divmod(index, columns)
        x = gap + column * (card_width + gap)
        y = gap + row * (image_height + label_height + gap)
        draw.rectangle((x, y, x + card_width, y + image_height + label_height), fill=CARD_BACKGROUND)
        image = prepared_image(path, (card_width, image_height))
        sheet.paste(image, (x + (card_width - image.width) // 2, y))
        draw.text(
            (x + 8, y + image_height + 6),
            (
                f"{request['japanese_title']} / r{request['revision']} "
                f"/ c{request['candidate_number']}"
            ),
            fill=TEXT,
            font=title_font,
        )
        draw.text((x + 8, y + image_height + 31), request["slot"], fill="#666666", font=small_font)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=92, method=6)
    return output_path


def validate_landmark_ratios(
    accepted_records: list[dict],
    pair_tolerance: float = 0.02,
    set_tolerance: float = 0.03,
) -> list[str]:
    errors = []
    by_slot = {record["slot"]: record for record in accepted_records}
    for left_slot, right_slot in COUNTERPART_PAIRS:
        if left_slot not in by_slot or right_slot not in by_slot:
            continue
        for landmark in LANDMARK_NAMES:
            delta = abs(
                by_slot[left_slot]["normalized_landmarks"][landmark]
                - by_slot[right_slot]["normalized_landmarks"][landmark]
            )
            if delta > pair_tolerance:
                errors.append(
                    f"counterpart {landmark} drift {left_slot} vs {right_slot}: {delta:.4f}"
                )
    for landmark in LANDMARK_NAMES:
        values = [record["normalized_landmarks"][landmark] for record in accepted_records]
        if values and max(values) - min(values) > set_tolerance:
            errors.append(f"full-set {landmark} drift: {max(values) - min(values):.4f}")
    return errors


def select_active_requests(
    manifest: dict,
    selected_slots: list[str] | None,
    selected_batch_ids: list[str] | None,
) -> list[dict]:
    slots = selected_slots or list(manifest["active_batches"])
    batches = set(
        selected_batch_ids
        or [manifest["active_batches"][slot] for slot in slots]
    )
    return [
        request
        for request in manifest["requests"]
        if request["slot"] in slots and request["batch_id"] in batches
    ]


def build_final_contact_sheet(
    accepted_records: list[dict],
    project_root: Path,
    output_path: Path,
) -> Path:
    errors = validate_landmark_ratios(accepted_records)
    if errors:
        raise ValueError("landmark validation failed: " + "; ".join(errors))
    ordered = sorted(accepted_records, key=lambda record: record["angle_order"])
    requests = [
        {
            "slot": record["slot"],
            "candidate_number": record["candidate_number"],
            "revision": record["revision"],
            "batch_id": record["batch_id"],
            "japanese_title": record["japanese_title"],
            "target_path": record["accepted_path"],
        }
        for record in ordered
    ]
    result = build_stage_contact_sheet(
        requests,
        project_root,
        output_path,
        columns=4,
        enforce_stage_shape=False,
    )
    with Image.open(result) as opened:
        sheet = opened.convert("RGB")
    draw = ImageDraw.Draw(sheet)
    if ordered:
        top_margin = 18
        card_height = 540 + 62
        for row in range(math.ceil(len(ordered) / 4)):
            row_y = top_margin + row * (card_height + 18)
            row_records = ordered[row * 4 : (row + 1) * 4]
            for landmark in LANDMARK_NAMES:
                canvas_positions = []
                for record in row_records:
                    crown = record["landmark_y_px"]["crown"]
                    sole = record["landmark_y_px"]["sole"]
                    normalized = record["normalized_landmarks"][landmark]
                    canvas_positions.append(crown + normalized * (sole - crown))
                y = row_y + round(statistics.median(canvas_positions) / 1536 * 540)
                draw.line((0, y, sheet.width, y), fill=GUIDE, width=1)
    sheet.save(result, quality=92, method=6)
    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Akari v1.2 turnaround contact sheets.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--requests", type=Path)
    source.add_argument("--accepted", type=Path)
    parser.add_argument("--slot", action="append")
    parser.add_argument("--batch-id", action="append")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--columns", type=int, default=3)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if args.requests:
        manifest = load_json(args.requests)
        requests = select_active_requests(manifest, args.slot, args.batch_id)
        result = build_stage_contact_sheet(requests, ROOT, output, args.columns)
    else:
        result = build_final_contact_sheet(
            load_json(args.accepted)["accepted_angles"],
            ROOT,
            output,
        )
    print(f"Wrote {result.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Add the package command and contract assertion**

Add to `package.json`:

```json
"build:v1-2-turnaround:contact-sheet": "uv run python -m scripts.build_v1_2_turnaround_contact_sheet"
```

Add to `AkariV12TurnaroundContractTest`:

```python
    def test_package_scripts_expose_turnaround_contact_sheet_builder(self):
        scripts = load_json(ROOT / "package.json")["scripts"]
        self.assertEqual(
            "uv run python -m scripts.build_v1_2_turnaround_contact_sheet",
            scripts["build:v1-2-turnaround:contact-sheet"],
        )
```

- [ ] **Step 5: Run targeted tests**

Run:

```bash
uv run python -m unittest \
  tests.test_v1_2_turnaround_contract \
  tests.test_v1_2_turnaround_contact_sheet -v
```

Expected: PASS.

- [ ] **Step 6: Commit contact-sheet tooling**

```bash
git add package.json scripts/build_v1_2_turnaround_contact_sheet.py tests/test_v1_2_turnaround_contract.py tests/test_v1_2_turnaround_contact_sheet.py
git commit -m "feat: add akari v1.2 turnaround review sheets"
```

## Task 5: Promote Only User-Approved Candidates

**Files:**

- Create: `tests/test_v1_2_turnaround_promotion.py`
- Create: `scripts/promote_v1_2_turnaround_candidate.py`
- Modify: `tests/test_v1_2_turnaround_contract.py`
- Modify: `package.json`

**Interfaces:**

- Consumes: one tracked stage review, the slot graph, request history, and
  current accepted-angle state.
- Produces: one 94-quality RGB WebP per accepted slot plus sorted records in
  `accepted-angles.json` containing SHA-256 and landmark ratios.

The exact review shape is:

```json
{
  "schema_version": 1,
  "review_id": "akari-v1.2-turnaround-front-20260710",
  "review_path": "evidence/v1-2-turnaround/reviews/front-review.json",
  "stage": "front",
  "slots": ["front"],
  "request_batches": {
    "front": "batch:v1-2-turnaround:20260710:front:r1"
  },
  "user_decision": "approved",
  "candidates": [
    {
      "request_id": "request:v1-2-turnaround:20260710:front:r1:c1",
      "slot": "front",
      "candidate_path": "source/generated/v1-2-turnaround/20260710_front_r1_c1.png",
      "state": "accept",
      "gates": {
        "identity": "pass",
        "geometry": "pass",
        "outfit": "pass",
        "quality": "pass"
      },
      "landmark_y_px": {
        "crown": 96,
        "chin": 270,
        "shoulder": 350,
        "hoodie_hem": 720,
        "skirt_hem": 850,
        "knee": 1080,
        "ankle": 1370,
        "sole": 1464
      },
      "normalized_landmarks": {
        "crown": 0.0,
        "chin": 0.127193,
        "shoulder": 0.185673,
        "hoodie_hem": 0.45614,
        "skirt_hem": 0.55117,
        "knee": 0.719298,
        "ankle": 0.931287,
        "sole": 1.0
      },
      "notes": "Concrete observed identity, proportion, outfit, and artifact notes.",
      "rejection_reason": ""
    }
  ]
}
```

Every candidate in each named active request batch appears once. Historical
batches remain append-only but are not re-reviewed. Rejected candidates have
non-empty `rejection_reason`; held candidates have concrete next-action notes.

- [ ] **Step 1: Write failing promotion tests**

Create `tests/test_v1_2_turnaround_promotion.py`:

```python
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.v1_2_turnaround_common import normalize_landmarks, sha256_file
from scripts.promote_v1_2_turnaround_candidate import promote_review


SLOTS = {
    "slots": [
        {
            "angle_order": 1,
            "slug": "front",
            "japanese_title": "正面",
            "upstream_slots": [],
        },
        {
            "angle_order": 2,
            "slug": "character-left-front-three-quarter",
            "japanese_title": "キャラクター左・前45度",
            "upstream_slots": ["front"],
        },
    ]
}

LANDMARK_Y_PX = {
    "crown": 96,
    "chin": 270,
    "shoulder": 350,
    "hoodie_hem": 720,
    "skirt_hem": 850,
    "knee": 1080,
    "ankle": 1370,
    "sole": 1464,
}


def review_for(request: dict) -> dict:
    return {
        "schema_version": 1,
        "review_id": "front-review",
        "review_path": "evidence/v1-2-turnaround/reviews/front-review.json",
        "stage": "front",
        "slots": [request["slot"]],
        "request_batches": {request["slot"]: request["batch_id"]},
        "user_decision": "approved",
        "candidates": [
            {
                "request_id": request["id"],
                "slot": request["slot"],
                "candidate_path": request["target_path"],
                "state": "accept",
                "gates": {
                    "identity": "pass",
                    "geometry": "pass",
                    "outfit": "pass",
                    "quality": "pass",
                },
                "landmark_y_px": LANDMARK_Y_PX,
                "normalized_landmarks": normalize_landmarks(LANDMARK_Y_PX),
                "notes": "same Akari, coherent body, standard outfit, clean image",
                "rejection_reason": "",
            }
        ],
    }


class AkariV12TurnaroundPromotionTest(unittest.TestCase):
    def test_promote_review_writes_webp_hash_and_acceptance_record(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            candidate = root / "source/generated/v1-2-turnaround/front.png"
            candidate.parent.mkdir(parents=True)
            Image.new("RGB", (1024, 1536), "#f4eee8").save(candidate)
            request = {
                "id": "request:v1-2-turnaround:20260710:front:r1:c1",
                "batch_id": "batch:v1-2-turnaround:20260710:front:r1",
                "revision": 1,
                "candidate_number": 1,
                "slot": "front",
                "target_path": candidate.relative_to(root).as_posix(),
            }
            result = promote_review(
                review_for(request),
                SLOTS,
                {"active_batches": {"front": request["batch_id"]}, "requests": [request]},
                {"schema_version": 1, "collection_id": "akari-v1.2-canonical-turnaround", "accepted_angles": []},
                root,
            )
            record = result["accepted_angles"][0]
            self.assertEqual("front", record["slot"])
            output = root / record["accepted_path"]
            self.assertTrue(output.is_file())
            self.assertEqual(sha256_file(output), record["sha256"])
            self.assertEqual(LANDMARK_Y_PX, record["landmark_y_px"])
            self.assertEqual(
                normalize_landmarks(LANDMARK_Y_PX),
                record["normalized_landmarks"],
            )
            with Image.open(output) as image:
                self.assertEqual((1024, 1536), image.size)
                self.assertEqual("RGB", image.mode)

    def test_promote_review_rejects_locked_dependency(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            candidate = root / "left.png"
            Image.new("RGB", (1024, 1536), "white").save(candidate)
            request = {
                "id": "left-request",
                "batch_id": "left-r1",
                "revision": 1,
                "candidate_number": 1,
                "slot": "character-left-front-three-quarter",
                "target_path": candidate.as_posix(),
            }
            review = review_for(request)
            review["candidates"][0]["slot"] = "character-left-front-three-quarter"
            with self.assertRaisesRegex(ValueError, "requires accepted slot front"):
                promote_review(
                    review,
                    SLOTS,
                    {
                        "active_batches": {
                            "character-left-front-three-quarter": "left-r1"
                        },
                        "requests": [request],
                    },
                    {"schema_version": 1, "collection_id": "akari-v1.2-canonical-turnaround", "accepted_angles": []},
                    root,
                )

    def test_promote_review_requires_exactly_one_accept_per_slot(self):
        request = {
            "id": "front-request",
            "batch_id": "front-r1",
            "revision": 1,
            "candidate_number": 1,
            "slot": "front",
            "target_path": "front.png",
        }
        review = review_for(request)
        review["candidates"][0]["state"] = "hold"
        with self.assertRaisesRegex(ValueError, "exactly one accepted candidate for front"):
            promote_review(
                review,
                SLOTS,
                {"active_batches": {"front": "front-r1"}, "requests": [request]},
                {"schema_version": 1, "collection_id": "akari-v1.2-canonical-turnaround", "accepted_angles": []},
                Path("."),
            )

    def test_promote_review_requires_every_materialized_candidate(self):
        first = {
            "id": "front-r2-c1",
            "batch_id": "front-r2",
            "revision": 2,
            "candidate_number": 1,
            "slot": "front",
            "target_path": "front-r2-c1.png",
        }
        second = dict(
            first,
            id="front-r2-c2",
            candidate_number=2,
            target_path="front-r2-c2.png",
        )
        historical = dict(
            first,
            id="front-r1-c1",
            batch_id="front-r1",
            revision=1,
            target_path="front-r1-c1.png",
        )
        review = review_for(first)
        with self.assertRaisesRegex(ValueError, "review must cover every materialized candidate"):
            promote_review(
                review,
                SLOTS,
                {
                    "active_batches": {"front": "front-r2"},
                    "requests": [historical, first, second],
                },
                {"schema_version": 1, "collection_id": "akari-v1.2-canonical-turnaround", "accepted_angles": []},
                Path("."),
            )

    def test_reopen_review_removes_the_record_and_finished_file(self):
        from scripts.promote_v1_2_turnaround_candidate import reopen_slots

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            front = root / "source/finished/v1-2-turnaround/front.webp"
            left = root / "source/finished/v1-2-turnaround/character-left-front-three-quarter.webp"
            front.parent.mkdir(parents=True)
            Image.new("RGB", (1024, 1536), "white").save(front)
            Image.new("RGB", (1024, 1536), "white").save(left)
            accepted = {
                "schema_version": 1,
                "collection_id": "akari-v1.2-canonical-turnaround",
                "accepted_angles": [
                    {
                        "slot": "front",
                        "angle_order": 1,
                        "accepted_path": front.relative_to(root).as_posix(),
                    },
                    {
                        "slot": "character-left-front-three-quarter",
                        "angle_order": 2,
                        "accepted_path": left.relative_to(root).as_posix(),
                    }
                ],
            }
            result = reopen_slots(
                {
                    "user_decision": "reopen",
                    "slots": ["front"],
                    "reason": "user approved correction after convergence review",
                },
                SLOTS,
                accepted,
                root,
            )
            self.assertEqual([], result["accepted_angles"])
            self.assertEqual(
                ["front", "character-left-front-three-quarter"],
                result["regeneration_queue"],
            )
            self.assertFalse(front.exists())
            self.assertFalse(left.exists())

    def test_tolerance_failure_writes_no_finished_asset(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            candidate = root / "left.png"
            Image.new("RGB", (1024, 1536), "white").save(candidate)
            request = {
                "id": "left-request",
                "batch_id": "left-r1",
                "revision": 1,
                "candidate_number": 1,
                "slot": "character-left-front-three-quarter",
                "target_path": candidate.as_posix(),
            }
            review = review_for(request)
            drifted = dict(LANDMARK_Y_PX)
            drifted["knee"] += 70
            review["candidates"][0]["landmark_y_px"] = drifted
            review["candidates"][0]["normalized_landmarks"] = normalize_landmarks(
                drifted
            )
            accepted = {
                "schema_version": 1,
                "collection_id": "akari-v1.2-canonical-turnaround",
                "accepted_angles": [
                    {
                        "slot": "front",
                        "angle_order": 1,
                        "accepted_path": "source/finished/v1-2-turnaround/front.webp",
                        "landmark_y_px": LANDMARK_Y_PX,
                        "normalized_landmarks": normalize_landmarks(LANDMARK_Y_PX),
                    }
                ],
            }
            with self.assertRaisesRegex(ValueError, "landmark validation failed"):
                promote_review(
                    review,
                    SLOTS,
                    {
                        "active_batches": {
                            "character-left-front-three-quarter": "left-r1"
                        },
                        "requests": [request],
                    },
                    accepted,
                    root,
                )
            self.assertFalse(
                (root / "source/finished/v1-2-turnaround/character-left-front-three-quarter.webp").exists()
            )
```

- [ ] **Step 2: Run the tests and verify the missing module fails**

Run:

```bash
uv run python -m unittest tests.test_v1_2_turnaround_promotion -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement validated promotion**

Create `scripts/promote_v1_2_turnaround_candidate.py`:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from scripts.build_v1_2_turnaround_contact_sheet import validate_landmark_ratios
from scripts.v1_2_turnaround_common import (
    LANDMARK_NAMES,
    dump_json,
    load_json,
    normalize_landmarks,
    resolve_path,
    sha256_file,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/v1-2-turnaround"
SLOT_MANIFEST_PATH = MANIFEST_DIR / "angle-slots.json"
REQUESTS_PATH = MANIFEST_DIR / "generation-requests.json"
ACCEPTED_PATH = MANIFEST_DIR / "accepted-angles.json"
FINISHED_DIR = ROOT / "source/finished/v1-2-turnaround"
REQUIRED_GATES = {"identity", "geometry", "outfit", "quality"}
ALLOWED_STATES = {"accept", "hold", "reject"}


def validate_review(
    review: dict,
    slot_manifest: dict,
    request_manifest: dict,
    accepted_manifest: dict,
) -> None:
    if review.get("user_decision") != "approved":
        raise ValueError("review is not user-approved")
    slots = {slot["slug"]: slot for slot in slot_manifest["slots"]}
    requests = {request["id"]: request for request in request_manifest["requests"]}
    accepted_slots = {record["slot"] for record in accepted_manifest["accepted_angles"]}
    reviewed_slots = set(review["slots"])
    candidate_slots = {candidate["slot"] for candidate in review["candidates"]}
    if candidate_slots != reviewed_slots:
        raise ValueError("review slots do not match candidate slots")
    request_batches = review.get("request_batches", {})
    if set(request_batches) != reviewed_slots:
        raise ValueError("review must name one active request batch per slot")
    for slot_name, batch_id in request_batches.items():
        if request_manifest.get("active_batches", {}).get(slot_name) != batch_id:
            raise ValueError(f"review does not use the active batch for {slot_name}")
    expected_request_ids = {
        request["id"]
        for request in request_manifest["requests"]
        if request["slot"] in reviewed_slots
        and request["batch_id"] == request_batches[request["slot"]]
    }
    reviewed_request_ids = [candidate["request_id"] for candidate in review["candidates"]]
    if len(reviewed_request_ids) != len(expected_request_ids) or set(reviewed_request_ids) != expected_request_ids:
        raise ValueError("review must cover every materialized candidate in the stage")
    for candidate in review["candidates"]:
        if candidate["state"] not in ALLOWED_STATES:
            raise ValueError(f"invalid candidate state: {candidate['state']}")
        if candidate["request_id"] not in requests:
            raise ValueError(f"unknown request id: {candidate['request_id']}")
        request = requests[candidate["request_id"]]
        if request["slot"] != candidate["slot"]:
            raise ValueError("review slot does not match request slot")
        if request["batch_id"] != request_batches[candidate["slot"]]:
            raise ValueError("review candidate does not belong to the active batch")
        if request["target_path"] != candidate["candidate_path"]:
            raise ValueError("review candidate path does not match request target")
        if candidate["state"] == "reject" and not candidate["rejection_reason"].strip():
            raise ValueError("rejected candidate requires rejection_reason")
        if not candidate["notes"].strip():
            raise ValueError("candidate notes must be concrete and non-empty")
    for slot_name in reviewed_slots:
        if slot_name not in slots:
            raise ValueError(f"unknown reviewed slot: {slot_name}")
        accepted_candidates = [
            candidate
            for candidate in review["candidates"]
            if candidate["slot"] == slot_name and candidate["state"] == "accept"
        ]
        if len(accepted_candidates) != 1:
            raise ValueError(f"exactly one accepted candidate for {slot_name} is required")
        candidate = accepted_candidates[0]
        if set(candidate["gates"]) != REQUIRED_GATES:
            raise ValueError(f"gate keys are incomplete for {slot_name}")
        if set(candidate["gates"].values()) != {"pass"}:
            raise ValueError(f"all gates must pass for {slot_name}")
        normalized = normalize_landmarks(candidate["landmark_y_px"])
        if normalized != candidate["normalized_landmarks"]:
            raise ValueError(f"normalized landmarks do not match pixels for {slot_name}")
        for upstream_slot in slots[slot_name]["upstream_slots"]:
            if upstream_slot not in accepted_slots:
                raise ValueError(f"{slot_name} requires accepted slot {upstream_slot}")


def promote_review(
    review: dict,
    slot_manifest: dict,
    request_manifest: dict,
    accepted_manifest: dict,
    project_root: Path,
) -> dict:
    validate_review(review, slot_manifest, request_manifest, accepted_manifest)
    slots = {slot["slug"]: slot for slot in slot_manifest["slots"]}
    requests = {request["id"]: request for request in request_manifest["requests"]}
    current = {record["slot"]: record for record in accepted_manifest["accepted_angles"]}
    proposed = {}
    for slot_name in {candidate["slot"] for candidate in review["candidates"]}:
        if slot_name in current:
            raise ValueError(f"slot already accepted: {slot_name}")
        candidate = next(
            candidate
            for candidate in review["candidates"]
            if candidate["slot"] == slot_name and candidate["state"] == "accept"
        )
        source = resolve_path(project_root, candidate["candidate_path"])
        if not source.is_file():
            raise ValueError(f"missing accepted candidate: {source}")
        with Image.open(source) as image:
            if image.size != (1024, 1536):
                raise ValueError(f"candidate canvas must be 1024x1536: {source}")
        relative_output = Path("source/finished/v1-2-turnaround") / f"{slot_name}.webp"
        slot = slots[slot_name]
        request = requests[candidate["request_id"]]
        proposed[slot_name] = {
            "slot": slot_name,
            "angle_order": slot["angle_order"],
            "japanese_title": slot["japanese_title"],
            "accepted_path": relative_output.as_posix(),
            "source_candidate_path": candidate["candidate_path"],
            "request_id": candidate["request_id"],
            "batch_id": request["batch_id"],
            "revision": request["revision"],
            "candidate_number": request["candidate_number"],
            "review_id": review["review_id"],
            "review_path": review["review_path"],
            "landmark_y_px": candidate["landmark_y_px"],
            "normalized_landmarks": candidate["normalized_landmarks"],
        }
    hypothetical = list(current.values()) + list(proposed.values())
    errors = validate_landmark_ratios(hypothetical)
    if errors:
        raise ValueError("landmark validation failed: " + "; ".join(errors))
    for slot_name, record in proposed.items():
        source = resolve_path(project_root, record["source_candidate_path"])
        output = resolve_path(project_root, record["accepted_path"])
        output.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source) as image:
            image.convert("RGB").save(output, "WEBP", quality=94, method=6)
        record["sha256"] = sha256_file(output)
        current[slot_name] = record
    updated = dict(accepted_manifest)
    updated["accepted_angles"] = sorted(current.values(), key=lambda record: record["angle_order"])
    remaining_queue = [
        slot_name
        for slot_name in accepted_manifest.get("regeneration_queue", [])
        if slot_name not in proposed
    ]
    if remaining_queue:
        updated["regeneration_queue"] = remaining_queue
    else:
        updated.pop("regeneration_queue", None)
    return updated


def reopen_slots(
    review: dict,
    slot_manifest: dict,
    accepted_manifest: dict,
    project_root: Path,
) -> dict:
    if review.get("user_decision") != "reopen":
        raise ValueError("reopen review is not user-approved")
    if not review.get("reason", "").strip():
        raise ValueError("reopen review requires a concrete reason")
    current = {record["slot"]: record for record in accepted_manifest["accepted_angles"]}
    slots = {slot["slug"]: slot for slot in slot_manifest["slots"]}
    requested = set(review["slots"])
    unknown = requested - set(slots)
    if unknown:
        raise ValueError(f"unknown reopen slots: {sorted(unknown)}")
    unaccepted = requested - set(current)
    if unaccepted:
        raise ValueError(f"cannot reopen unaccepted slots: {sorted(unaccepted)}")
    reopened = set(requested)
    changed = True
    while changed:
        changed = False
        for slot_name in current:
            if slot_name in reopened:
                continue
            if any(upstream in reopened for upstream in slots[slot_name]["upstream_slots"]):
                reopened.add(slot_name)
                changed = True
    expected_root = project_root / "source/finished/v1-2-turnaround"
    removals = []
    for slot_name in reopened:
        record = current[slot_name]
        finished = resolve_path(project_root, record["accepted_path"])
        if finished.parent != expected_root:
            raise ValueError(f"refusing to remove unexpected path: {finished}")
        removals.append((slot_name, finished))
    for slot_name, finished in removals:
        current.pop(slot_name)
        finished.unlink(missing_ok=True)
    updated = dict(accepted_manifest)
    updated["accepted_angles"] = sorted(current.values(), key=lambda record: record["angle_order"])
    remaining = set(reopened)
    regeneration_queue = []
    while remaining:
        ready = sorted(
            (
                slot_name
                for slot_name in remaining
                if not (set(slots[slot_name]["upstream_slots"]) & remaining)
            ),
            key=lambda slot_name: slots[slot_name]["angle_order"],
        )
        if not ready:
            raise ValueError("turnaround dependency graph contains a cycle")
        regeneration_queue.extend(ready)
        remaining.difference_update(ready)
    updated["regeneration_queue"] = regeneration_queue
    return updated


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Promote reviewed Akari v1.2 turnaround candidates.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--review", type=Path)
    mode.add_argument("--reopen-review", type=Path)
    parser.add_argument("--slots", type=Path, default=SLOT_MANIFEST_PATH)
    parser.add_argument("--requests", type=Path, default=REQUESTS_PATH)
    parser.add_argument("--accepted", type=Path, default=ACCEPTED_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    review_arg = args.review or args.reopen_review
    review_path = review_arg if review_arg.is_absolute() else ROOT / review_arg
    if args.review:
        updated = promote_review(
            load_json(review_path),
            load_json(args.slots),
            load_json(args.requests),
            load_json(args.accepted),
            ROOT,
        )
    else:
        updated = reopen_slots(
            load_json(review_path),
            load_json(args.slots),
            load_json(args.accepted),
            ROOT,
        )
    dump_json(args.accepted, updated)
    print(f"accepted turnaround angles: {len(updated['accepted_angles'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Add the package command and contract assertion**

Add to `package.json`:

```json
"promote:v1-2-turnaround": "uv run python -m scripts.promote_v1_2_turnaround_candidate"
```

Add to `AkariV12TurnaroundContractTest`:

```python
    def test_package_scripts_expose_turnaround_promotion(self):
        scripts = load_json(ROOT / "package.json")["scripts"]
        self.assertEqual(
            "uv run python -m scripts.promote_v1_2_turnaround_candidate",
            scripts["promote:v1-2-turnaround"],
        )
```

- [ ] **Step 5: Run targeted tests**

Run:

```bash
uv run python -m unittest \
  tests.test_v1_2_turnaround_contract \
  tests.test_v1_2_turnaround_promotion -v
```

Expected: PASS.

- [ ] **Step 6: Commit promotion tooling**

```bash
git add package.json scripts/promote_v1_2_turnaround_candidate.py tests/test_v1_2_turnaround_contract.py tests/test_v1_2_turnaround_promotion.py
git commit -m "feat: promote reviewed akari turnaround assets"
```

## Task 6: Generate And Accept The Front Master

**Files:**

- Modify: `source/manifests/v1-2-turnaround/generation-requests.json`
- Create working files:
  `source/generated/v1-2-turnaround/20260710_front_r1_c1.png`,
  `source/generated/v1-2-turnaround/20260710_front_r1_c2.png`, and
  `source/generated/v1-2-turnaround/20260710_front_r1_c3.png`
- Create working file:
  `evidence/v1-2-turnaround/contact-sheets/front-candidates.webp`
- Create tracked file:
  `evidence/v1-2-turnaround/reviews/front-review.json`
- Modify: `source/manifests/v1-2-turnaround/accepted-angles.json`
- Create tracked file: `source/finished/v1-2-turnaround/front.webp`

**Interfaces:**

- Consumes: accepted face-and-hair lock and static v1.1 body/outfit references.
- Produces: accepted slot `front`, which unlocks both front-three-quarter slots.

- [ ] **Step 1: Materialize the three front requests**

Run:

```bash
uv run python scripts/verify_environment.py
npm run build:v1-2-turnaround:requests -- \
  --slot front \
  --date-prefix 20260710 \
  --revision 1
```

Expected: `environment: ok`, followed by `turnaround requests written: 3`.

- [ ] **Step 2: Print and verify the exact front request inputs**

Run:

```bash
jq -r '.active_batches.front as $batch | .requests[] | select(.batch_id == $batch) | [.id, .target_path, (.reference_pack_inputs | join(" | ")), .prompt] | @tsv' \
  source/manifests/v1-2-turnaround/generation-requests.json
```

Expected: three rows targeting `20260710_front_r1_c1.png` through
`20260710_front_r1_c3.png`; every row includes the accepted v1.2 face, corrected
body, corrected hoodie front, footwear, and sneaker sources.

- [ ] **Step 3: Generate all three front candidates**

Before each front request, open the accepted face plus every applicable body,
outfit, footwear, and ornament path from `reference_pack_inputs` with
`view_image`; record each reference's role in the image-generation prompt.
Then use the `$imagegen` skill with every path attached and the exact materialized
`prompt` value. Save the returned image to the request's exact `target_path`.

If the UI shows an image but no PNG appears, recover the current rollout payload
as documented in `AGENTS.md` and verify the PNG signature
`89504e470d0a1a0a` before saving it.

- [ ] **Step 4: Verify image dimensions and color mode**

Run:

```bash
uv run python - <<'PY'
import json
from pathlib import Path
from PIL import Image

manifest = json.loads(
    Path("source/manifests/v1-2-turnaround/generation-requests.json").read_text(
        encoding="utf-8"
    )
)
active_batch = manifest["active_batches"]["front"]
requests = [
    request for request in manifest["requests"]
    if request["slot"] == "front" and request["batch_id"] == active_batch
]
for request in requests:
    path = Path(request["target_path"])
    if not path.is_file():
        raise SystemExit(f"missing front candidate: {path}")
    with Image.open(path) as image:
        if image.size != (1024, 1536):
            raise SystemExit(f"wrong front canvas: {path} {image.size}")
        if image.mode not in {"RGB", "RGBA"}:
            raise SystemExit(f"wrong front mode: {path} {image.mode}")
        print(path.as_posix(), image.size, image.mode)
PY
```

Expected: three valid image rows.

- [ ] **Step 5: Build and inspect the front candidate sheet**

Run:

```bash
npm run build:v1-2-turnaround:contact-sheet -- \
  --requests source/manifests/v1-2-turnaround/generation-requests.json \
  --slot front \
  --output evidence/v1-2-turnaround/contact-sheets/front-candidates.webp \
  --columns 3
```

Expected:
`Wrote evidence/v1-2-turnaround/contact-sheets/front-candidates.webp`.

Open the sheet and compare all three candidates against the Identity, Geometry,
Outfit, and Quality Gates. Measure crown, chin, shoulder, hoodie hem, skirt hem,
knee, ankle, and sole y positions as image pixels. Compute each normalized
landmark with `(y_px - crown_y_px) / (sole_y_px - crown_y_px)`; crown must be
`0.0` and sole must be `1.0`. Never divide landmark y directly by 1536.

- [ ] **Step 6: Present the sheet and wait for the user's front-master choice**

Show the contact sheet and report concrete differences in face continuity,
head-to-body ratio, healthy leg volume, hoodie/skirt construction, footwear, and
artifacts. Do not create an approved review until the user selects one candidate
or requests a regeneration.

- [ ] **Step 7: Write and validate the concrete front review**

Create `evidence/v1-2-turnaround/reviews/front-review.json` using the exact
review schema in Task 5. Include the active batch ID, all three active request
IDs in candidate order, exactly one `accept`, concrete notes for every
candidate, raw pixel landmarks plus crown-to-sole normalized landmarks for the
accepted candidate, and `user_decision: approved`.

Run:

```bash
npm run promote:v1-2-turnaround -- \
  --review evidence/v1-2-turnaround/reviews/front-review.json
```

Expected: `accepted turnaround angles: 1` and
`source/finished/v1-2-turnaround/front.webp` exists.

- [ ] **Step 8: Verify and commit the front master**

Run:

```bash
jq -e '.accepted_angles | length == 1 and .[0].slot == "front"' \
  source/manifests/v1-2-turnaround/accepted-angles.json
git status --short --ignored source/generated/v1-2-turnaround evidence/v1-2-turnaround/contact-sheets
```

Expected: `jq` exits 0; candidates and contact sheet have `!!` prefixes.

Commit:

```bash
git add source/manifests/v1-2-turnaround/generation-requests.json \
  source/manifests/v1-2-turnaround/accepted-angles.json \
  source/finished/v1-2-turnaround/front.webp \
  evidence/v1-2-turnaround/reviews/front-review.json
git commit -m "feat: accept akari v1.2 front master"
```

## Task 7: Generate And Accept Both Front-Three-Quarter Views

**Files:**

- Modify: `source/manifests/v1-2-turnaround/generation-requests.json`
- Create working candidates for:
  `character-left-front-three-quarter` and
  `character-right-front-three-quarter`, versions 1 through 3
- Create working file:
  `evidence/v1-2-turnaround/contact-sheets/front-three-quarter-candidates.webp`
- Create tracked file:
  `evidence/v1-2-turnaround/reviews/front-three-quarter-review.json`
- Modify: `source/manifests/v1-2-turnaround/accepted-angles.json`
- Create tracked files:
  `source/finished/v1-2-turnaround/character-left-front-three-quarter.webp` and
  `source/finished/v1-2-turnaround/character-right-front-three-quarter.webp`

**Interfaces:**

- Consumes: accepted `front` plus the legacy hairpin-side and non-hairpin-side
  45-degree references.
- Produces: accepted paired front-three-quarter slots that unlock both profiles.

- [ ] **Step 1: Materialize the paired requests**

Run:

```bash
npm run build:v1-2-turnaround:requests -- \
  --slot character-left-front-three-quarter \
  --slot character-right-front-three-quarter \
  --date-prefix 20260710 \
  --revision 1
```

Expected: `turnaround requests written: 6`. Every request includes
`source/finished/v1-2-turnaround/front.webp`.

- [ ] **Step 2: Generate all six candidates from their exact requests**

Use `$imagegen` with each request's exact prompt and all listed references. Save
to these paths:

```text
source/generated/v1-2-turnaround/20260710_character-left-front-three-quarter_r1_c1.png
source/generated/v1-2-turnaround/20260710_character-left-front-three-quarter_r1_c2.png
source/generated/v1-2-turnaround/20260710_character-left-front-three-quarter_r1_c3.png
source/generated/v1-2-turnaround/20260710_character-right-front-three-quarter_r1_c1.png
source/generated/v1-2-turnaround/20260710_character-right-front-three-quarter_r1_c2.png
source/generated/v1-2-turnaround/20260710_character-right-front-three-quarter_r1_c3.png
```

- [ ] **Step 3: Build the paired sheet**

Run:

```bash
npm run build:v1-2-turnaround:contact-sheet -- \
  --requests source/manifests/v1-2-turnaround/generation-requests.json \
  --slot character-left-front-three-quarter \
  --slot character-right-front-three-quarter \
  --output evidence/v1-2-turnaround/contact-sheets/front-three-quarter-candidates.webp \
  --columns 3
```

Expected: a six-card sheet with the character-left candidates first and the
character-right candidates second.

- [ ] **Step 4: Review the counterpart pair with the user**

Report which left and right candidates best preserve the accepted front master,
the correct ornament side, head width, shoulder width, hoodie hem, skirt hem,
leg volume, and sneaker mass. Reject any pair that succeeds only through a
mirrored shortcut. Wait for one user-approved candidate per side.

- [ ] **Step 5: Record, promote, and validate both accepted views**

Create
`evidence/v1-2-turnaround/reviews/front-three-quarter-review.json` with all six
candidates, exactly one accept per slot, concrete notes, and measured landmark
pixel positions plus crown-to-sole normalized ratios. Promotion must reject the
hypothetical three-angle state before writing either WebP when any 2 or 3
percent tolerance fails. Run:

```bash
npm run promote:v1-2-turnaround -- \
  --review evidence/v1-2-turnaround/reviews/front-three-quarter-review.json
npm run build:v1-2-turnaround:contact-sheet -- \
  --accepted source/manifests/v1-2-turnaround/accepted-angles.json \
  --output evidence/v1-2-turnaround/contact-sheets/front-three-quarter-alignment.webp
```

Expected: three accepted angles total and no landmark validation failure.

- [ ] **Step 6: Commit the accepted pair**

```bash
git add source/manifests/v1-2-turnaround/generation-requests.json \
  source/manifests/v1-2-turnaround/accepted-angles.json \
  source/finished/v1-2-turnaround/character-left-front-three-quarter.webp \
  source/finished/v1-2-turnaround/character-right-front-three-quarter.webp \
  evidence/v1-2-turnaround/reviews/front-three-quarter-review.json
git commit -m "feat: accept akari v1.2 front three-quarter views"
```

## Task 8: Generate And Accept Both True Profiles

**Files:**

- Modify: `source/manifests/v1-2-turnaround/generation-requests.json`
- Create working candidates for `character-left-profile` and
  `character-right-profile`, versions 1 through 3
- Create working file:
  `evidence/v1-2-turnaround/contact-sheets/profile-candidates.webp`
- Create tracked file:
  `evidence/v1-2-turnaround/reviews/profile-review.json`
- Modify: `source/manifests/v1-2-turnaround/accepted-angles.json`
- Create tracked files:
  `source/finished/v1-2-turnaround/character-left-profile.webp` and
  `source/finished/v1-2-turnaround/character-right-profile.webp`

**Interfaces:**

- Consumes: accepted front and corresponding accepted front-three-quarter view
  for each side, plus the legacy profile as a volume reference.
- Produces: accepted paired profiles that unlock both rear-three-quarter views.

- [ ] **Step 1: Materialize and verify the profile dependencies**

Run:

```bash
npm run build:v1-2-turnaround:requests -- \
  --slot character-left-profile \
  --slot character-right-profile \
  --date-prefix 20260710 \
  --revision 1
jq -e '
  .active_batches as $active
  | [.requests[] | select(
      .slot == "character-left-profile"
      or .slot == "character-right-profile"
    ) | select(.batch_id == $active[.slot])]
  | length == 6
' \
  source/manifests/v1-2-turnaround/generation-requests.json
```

Expected: six profile requests, each containing the accepted front and its
same-side accepted front-three-quarter path.

- [ ] **Step 2: Generate all six profile candidates**

Use `$imagegen` with each exact materialized request. Verify each output is
1024x1536 RGB or RGBA and save it to the request target path.

- [ ] **Step 3: Build and inspect the profile sheet**

Run:

```bash
npm run build:v1-2-turnaround:contact-sheet -- \
  --requests source/manifests/v1-2-turnaround/generation-requests.json \
  --slot character-left-profile \
  --slot character-right-profile \
  --output evidence/v1-2-turnaround/contact-sheets/profile-candidates.webp \
  --columns 3
```

Compare forehead, nose, mouth, chin, back-of-head volume, hood depth, chest and
back thickness, skirt projection, knee, calf, sock, and sneaker profile. Wait
for the user to approve one candidate per side.

- [ ] **Step 4: Record and promote the profile pair**

Create `evidence/v1-2-turnaround/reviews/profile-review.json` with all six
candidates from the two active batches, exact request IDs, concrete
observations, one accept per side, and raw plus normalized landmarks. Promotion
must validate the hypothetical five-angle state before writing either WebP.
Run:

```bash
npm run promote:v1-2-turnaround -- \
  --review evidence/v1-2-turnaround/reviews/profile-review.json
npm run build:v1-2-turnaround:contact-sheet -- \
  --accepted source/manifests/v1-2-turnaround/accepted-angles.json \
  --output evidence/v1-2-turnaround/contact-sheets/profile-alignment.webp
```

Expected: five accepted angles total and no tolerance failure.

- [ ] **Step 5: Commit the accepted profiles**

```bash
git add source/manifests/v1-2-turnaround/generation-requests.json \
  source/manifests/v1-2-turnaround/accepted-angles.json \
  source/finished/v1-2-turnaround/character-left-profile.webp \
  source/finished/v1-2-turnaround/character-right-profile.webp \
  evidence/v1-2-turnaround/reviews/profile-review.json
git commit -m "feat: accept akari v1.2 profile views"
```

## Task 9: Generate And Accept Both Rear-Three-Quarter Views

**Files:**

- Modify: `source/manifests/v1-2-turnaround/generation-requests.json`
- Create working candidates for `character-left-rear-three-quarter` and
  `character-right-rear-three-quarter`, versions 1 through 3
- Create working file:
  `evidence/v1-2-turnaround/contact-sheets/rear-three-quarter-candidates.webp`
- Create tracked file:
  `evidence/v1-2-turnaround/reviews/rear-three-quarter-review.json`
- Modify: `source/manifests/v1-2-turnaround/accepted-angles.json`
- Create tracked files:
  `source/finished/v1-2-turnaround/character-left-rear-three-quarter.webp` and
  `source/finished/v1-2-turnaround/character-right-rear-three-quarter.webp`

**Interfaces:**

- Consumes: accepted front, same-side front-three-quarter, and same-side profile
  views plus the legacy back source.
- Produces: two accepted rear-three-quarter views that jointly unlock `back`.

- [ ] **Step 1: Materialize both rear-three-quarter request sets**

Run:

```bash
npm run build:v1-2-turnaround:requests -- \
  --slot character-left-rear-three-quarter \
  --slot character-right-rear-three-quarter \
  --date-prefix 20260710 \
  --revision 1
```

Expected: `turnaround requests written: 6`. Each request contains the front,
same-side front-three-quarter, same-side profile, and legacy back reference.

- [ ] **Step 2: Generate all six rear-three-quarter candidates**

Use `$imagegen` with the exact prompt and every listed reference. Save to each
request target path and verify every image is a readable 1024x1536 RGB or RGBA
PNG.

- [ ] **Step 3: Build the paired sheet and review back construction**

Run:

```bash
npm run build:v1-2-turnaround:contact-sheet -- \
  --requests source/manifests/v1-2-turnaround/generation-requests.json \
  --slot character-left-rear-three-quarter \
  --slot character-right-rear-three-quarter \
  --output evidence/v1-2-turnaround/contact-sheets/rear-three-quarter-candidates.webp \
  --columns 3
```

Compare bob back volume, ornament occlusion, hood depth, shoulder slope, sleeve
width, hoodie back hem, skirt reveal, calf transition, sock stripes, and sneaker
heel construction. Run `$akari-v1-1-image-review` on the likely accept for each
side, then present the sheet and findings to the user. Wait for one approved
candidate per side.

- [ ] **Step 4: Record, promote, and validate the rear pair**

Create `evidence/v1-2-turnaround/reviews/rear-three-quarter-review.json` with
all six candidates, one accepted candidate per side, concrete review notes,
gate results, and raw plus normalized landmarks. Promotion must validate the
hypothetical seven-angle state before writing either WebP. Run:

```bash
npm run promote:v1-2-turnaround -- \
  --review evidence/v1-2-turnaround/reviews/rear-three-quarter-review.json
npm run build:v1-2-turnaround:contact-sheet -- \
  --accepted source/manifests/v1-2-turnaround/accepted-angles.json \
  --output evidence/v1-2-turnaround/contact-sheets/rear-three-quarter-alignment.webp
```

Expected: seven accepted angles and no tolerance failure.

- [ ] **Step 5: Commit the accepted rear pair**

```bash
git add source/manifests/v1-2-turnaround/generation-requests.json \
  source/manifests/v1-2-turnaround/accepted-angles.json \
  source/finished/v1-2-turnaround/character-left-rear-three-quarter.webp \
  source/finished/v1-2-turnaround/character-right-rear-three-quarter.webp \
  evidence/v1-2-turnaround/reviews/rear-three-quarter-review.json
git commit -m "feat: accept akari v1.2 rear three-quarter views"
```

## Task 10: Converge Both Branches At The Back View

**Files:**

- Modify: `source/manifests/v1-2-turnaround/generation-requests.json`
- Create working files:
  `source/generated/v1-2-turnaround/20260710_back_r1_c1.png`,
  `source/generated/v1-2-turnaround/20260710_back_r1_c2.png`, and
  `source/generated/v1-2-turnaround/20260710_back_r1_c3.png`
- Create working file:
  `evidence/v1-2-turnaround/contact-sheets/back-candidates.webp`
- Create tracked file:
  `evidence/v1-2-turnaround/reviews/back-review.json`
- Modify: `source/manifests/v1-2-turnaround/accepted-angles.json`
- Create tracked file: `source/finished/v1-2-turnaround/back.webp`

**Interfaces:**

- Consumes: accepted front plus both accepted rear-three-quarter views and the
  legacy back reference.
- Produces: the eighth accepted angle and proves that the two branches converge.

- [ ] **Step 1: Materialize the back requests and verify convergence inputs**

Run:

```bash
npm run build:v1-2-turnaround:requests -- \
  --slot back \
  --date-prefix 20260710 \
  --revision 1
jq -e '
  .active_batches.back as $batch
  | [.requests[] | select(.slot == "back" and .batch_id == $batch)][-1].reference_pack_inputs
  | index("source/finished/v1-2-turnaround/character-left-rear-three-quarter.webp") != null
    and index("source/finished/v1-2-turnaround/character-right-rear-three-quarter.webp") != null
' source/manifests/v1-2-turnaround/generation-requests.json
```

Expected: three requests and `jq` exits 0.

- [ ] **Step 2: Generate and verify all three back candidates**

Use `$imagegen` with each exact back request. Save to the three target paths and
verify 1024x1536 RGB or RGBA images.

- [ ] **Step 3: Build and inspect the back convergence sheet**

Run:

```bash
npm run build:v1-2-turnaround:contact-sheet -- \
  --requests source/manifests/v1-2-turnaround/generation-requests.json \
  --slot back \
  --output evidence/v1-2-turnaround/contact-sheets/back-candidates.webp \
  --columns 3
```

Compare the candidate against both rear-three-quarter views. If neither
candidate can connect both branches without averaging away a contradiction,
identify the earliest inconsistent rear-three-quarter or profile slot and ask
the user to approve reopening it. Record that decision at the fixed path
`evidence/v1-2-turnaround/reviews/back-convergence-reopen-review.json` with
`user_decision: reopen`, a `slots` array containing the exact inconsistent
slots, and a concrete `reason`. Run:

```bash
npm run promote:v1-2-turnaround -- \
  --reopen-review evidence/v1-2-turnaround/reviews/back-convergence-reopen-review.json
git add evidence/v1-2-turnaround/reviews/back-convergence-reopen-review.json \
  source/manifests/v1-2-turnaround/accepted-angles.json \
  source/finished/v1-2-turnaround
git commit -m "fix: reopen inconsistent akari turnaround branch"
```

Use the returned `regeneration_queue` in ascending dependency order. When a
profile is reopened, rerun Task 8 for that exact profile, Task 9 for its
invalidated same-side rear-three-quarter, and Task 10 for back. When only a rear
three-quarter is reopened, rerun that exact Task 9 slot and then Task 10. Keep
`--date-prefix 20260710` and materialize the first correction with
`--revision 2`; increment the revision only after another user-approved reopen.
Historical requests remain in the manifest while `active_batches` moves to the
new batch.
Run `$akari-v1-1-image-review` on the likely back accept and wait for user
approval.

- [ ] **Step 4: Record and promote the accepted back**

Create `evidence/v1-2-turnaround/reviews/back-review.json` with all three
candidates, one accepted back, concrete branch-convergence notes, gate results,
and raw plus normalized landmarks. Promotion must validate the complete
hypothetical eight-angle state before writing `back.webp`. Run:

```bash
npm run promote:v1-2-turnaround -- \
  --review evidence/v1-2-turnaround/reviews/back-review.json
jq -e '.accepted_angles | length == 8' \
  source/manifests/v1-2-turnaround/accepted-angles.json
```

Expected: `accepted turnaround angles: 8` and `jq` exits 0.

- [ ] **Step 5: Commit the accepted back**

```bash
git add source/manifests/v1-2-turnaround/generation-requests.json \
  source/manifests/v1-2-turnaround/accepted-angles.json \
  source/finished/v1-2-turnaround/back.webp \
  evidence/v1-2-turnaround/reviews/back-review.json
git commit -m "feat: converge akari v1.2 turnaround at back view"
```

## Task 11: Run The Final Eight-View Gate And Handoff

**Files:**

- Create tracked file: `dist/akari-v1.2-turnaround-contact-sheet.webp`
- Create tracked file:
  `evidence/v1-2-turnaround/reviews/final-eight-view-review.json`
- Create tracked file:
  `source/manifests/v1-2-motion/phase-2-handoff.json`
- Create: `scripts/build_v1_2_motion_handoff.py`
- Modify: `tests/test_v1_2_turnaround_contract.py`
- Read: every Phase 1 manifest, review, and finished image

**Interfaces:**

- Consumes: all eight accepted records and finished WebPs.
- Produces: the final visual comparison, a user-approved Phase 1 gate, and a
  machine-checked three-slot input contract for the separate motion-pose plan.

- [ ] **Step 1: Build the final tracked contact sheet**

Run:

```bash
npm run build:v1-2-turnaround:contact-sheet -- \
  --accepted source/manifests/v1-2-turnaround/accepted-angles.json \
  --output dist/akari-v1.2-turnaround-contact-sheet.webp
```

Expected: `Wrote dist/akari-v1.2-turnaround-contact-sheet.webp` with eight views
in canonical order and no landmark tolerance failure.

- [ ] **Step 2: Verify hashes, dimensions, and canonical order**

Run:

```bash
uv run python - <<'PY'
import hashlib
import json
from pathlib import Path
from PIL import Image

manifest = json.loads(
    Path("source/manifests/v1-2-turnaround/accepted-angles.json").read_text(
        encoding="utf-8"
    )
)
expected = [
    "front",
    "character-left-front-three-quarter",
    "character-left-profile",
    "character-left-rear-three-quarter",
    "back",
    "character-right-rear-three-quarter",
    "character-right-profile",
    "character-right-front-three-quarter",
]
records = manifest["accepted_angles"]
if [record["slot"] for record in records] != expected:
    raise SystemExit("accepted angle order is not canonical")
for record in records:
    path = Path(record["accepted_path"])
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != record["sha256"]:
        raise SystemExit(f"hash mismatch: {path}")
    with Image.open(path) as image:
        if image.size != (1024, 1536) or image.mode != "RGB":
            raise SystemExit(f"invalid finished asset: {path} {image.size} {image.mode}")
    print(record["slot"], path.as_posix(), digest)
PY
```

Expected: eight rows and exit 0.

- [ ] **Step 3: Present the final sheet and wait for user acceptance**

Show `dist/akari-v1.2-turnaround-contact-sheet.webp`. Summarize the final
Identity, Geometry, Outfit, Quality, left/right counterpart, hair-ornament, and
back-convergence results. Do not mark Phase 1 accepted until the user approves
the complete set. If the user rejects the set, create
`evidence/v1-2-turnaround/reviews/final-eight-view-reopen-review.json` with
`user_decision: reopen`, the earliest inconsistent accepted slots, and a
concrete reason. Run the `--reopen-review` command from Task 10 and follow its
entire `regeneration_queue` in order: Task 6 for front, Task 7 for a front
three-quarter, Task 8 for a profile, Task 9 for a rear three-quarter, and Task
10 for back, skipping slots not present in the queue. Rebuild and present the
final sheet again. Do not create an accepted final review or Phase 2 handoff on
a rejected set.

- [ ] **Step 4: Write the final review and its failing contract**

After user approval, create
`evidence/v1-2-turnaround/reviews/final-eight-view-review.json`:

```json
{
  "schema_version": 1,
  "review_id": "akari-v1.2-turnaround-final-eight-view-20260710",
  "source_manifest": "source/manifests/v1-2-turnaround/accepted-angles.json",
  "contact_sheet": "dist/akari-v1.2-turnaround-contact-sheet.webp",
  "decision": "accepted",
  "accepted_slots": [
    "front",
    "character-left-front-three-quarter",
    "character-left-profile",
    "character-left-rear-three-quarter",
    "back",
    "character-right-rear-three-quarter",
    "character-right-profile",
    "character-right-front-three-quarter"
  ],
  "gate_summary": {
    "identity": "pass",
    "geometry": "pass",
    "outfit": "pass",
    "quality": "pass",
    "counterpart_tolerance": "pass",
    "back_convergence": "pass"
  },
  "motion_phase_handoff": {
    "status": "ready_for_contract_build",
    "target": "source/manifests/v1-2-motion/phase-2-handoff.json"
  }
}
```

Create `scripts/build_v1_2_motion_handoff.py`:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.v1_2_turnaround_common import dump_json, load_json, sha256_file


ROOT = Path(__file__).resolve().parents[1]
ACCEPTED = ROOT / "source/manifests/v1-2-turnaround/accepted-angles.json"
FINAL_REVIEW = ROOT / "evidence/v1-2-turnaround/reviews/final-eight-view-review.json"
OUTPUT = ROOT / "source/manifests/v1-2-motion/phase-2-handoff.json"
CANONICAL_SLOTS = [
    "front",
    "character-left-front-three-quarter",
    "character-left-profile",
    "character-left-rear-three-quarter",
    "back",
    "character-right-rear-three-quarter",
    "character-right-profile",
    "character-right-front-three-quarter",
]
MOTION_SLOTS = [
    {
        "slug": "walking",
        "description": "readable mid-step with traceable leg, clothing, hair, sock, and sneaker motion",
    },
    {
        "slug": "seated",
        "description": "natural seated pose with believable proportion, folds, hands, socks, and footwear",
    },
    {
        "slug": "turning",
        "description": "over-shoulder or mid-turn pose without flipping the character-left ornament",
    },
]


def build_handoff(
    accepted: dict,
    final_review: dict,
    accepted_manifest_sha256: str,
) -> dict:
    records = accepted["accepted_angles"]
    if [record["slot"] for record in records] != CANONICAL_SLOTS:
        raise ValueError("Phase 2 requires all eight accepted slots in canonical order")
    if final_review.get("decision") != "accepted":
        raise ValueError("Phase 2 requires an accepted final eight-view review")
    inputs = [
        {
            "slot": record["slot"],
            "accepted_path": record["accepted_path"],
            "sha256": record["sha256"],
        }
        for record in records
    ]
    return {
        "schema_version": 1,
        "collection_id": "akari-v1.2-representative-motion-poses",
        "source_turnaround_manifest": (
            "source/manifests/v1-2-turnaround/accepted-angles.json"
        ),
        "source_turnaround_manifest_sha256": accepted_manifest_sha256,
        "source_final_review": (
            "evidence/v1-2-turnaround/reviews/final-eight-view-review.json"
        ),
        "turnaround_inputs": inputs,
        "motion_slots": [
            {
                **motion,
                "requires_complete_turnaround": True,
                "required_turnaround_slots": CANONICAL_SLOTS,
                "candidate_count": 3,
                "deliverable_count": 1,
            }
            for motion in MOTION_SLOTS
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Akari v1.2 motion handoff")
    parser.add_argument("--accepted", type=Path, default=ACCEPTED)
    parser.add_argument("--final-review", type=Path, default=FINAL_REVIEW)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args(argv)
    handoff = build_handoff(
        load_json(args.accepted),
        load_json(args.final_review),
        sha256_file(args.accepted),
    )
    dump_json(args.output, handoff)
    print(f"motion handoff written: {len(handoff['motion_slots'])} slots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Add this constant and method to `tests/test_v1_2_turnaround_contract.py`:

```python
FINAL_REVIEW = ROOT / "evidence/v1-2-turnaround/reviews/final-eight-view-review.json"
PHASE_2_HANDOFF = ROOT / "source/manifests/v1-2-motion/phase-2-handoff.json"

    def test_final_review_accepts_all_eight_canonical_slots(self):
        review = load_json(FINAL_REVIEW)
        slots = load_json(ANGLE_SLOTS)["slots"]
        self.assertEqual("accepted", review["decision"])
        self.assertEqual([slot["slug"] for slot in slots], review["accepted_slots"])
        self.assertEqual(
            {"pass"},
            set(review["gate_summary"].values()),
        )
        self.assertEqual(
            "ready_for_contract_build",
            review["motion_phase_handoff"]["status"],
        )

    def test_phase_2_handoff_has_exactly_three_turnaround_dependent_slots(self):
        accepted = load_json(ACCEPTED_ANGLES)["accepted_angles"]
        handoff = load_json(PHASE_2_HANDOFF)
        self.assertEqual(
            ["walking", "seated", "turning"],
            [slot["slug"] for slot in handoff["motion_slots"]],
        )
        expected_slots = [record["slot"] for record in accepted]
        expected_inputs = [
            {
                "slot": record["slot"],
                "accepted_path": record["accepted_path"],
                "sha256": record["sha256"],
            }
            for record in accepted
        ]
        self.assertEqual(expected_inputs, handoff["turnaround_inputs"])
        self.assertEqual(
            hashlib.sha256(ACCEPTED_ANGLES.read_bytes()).hexdigest(),
            handoff["source_turnaround_manifest_sha256"],
        )
        for slot in handoff["motion_slots"]:
            self.assertTrue(slot["requires_complete_turnaround"])
            self.assertEqual(expected_slots, slot["required_turnaround_slots"])
            self.assertEqual(1, slot["deliverable_count"])
```

Run the tests once before creating the final review and handoff to verify they
fail with missing files. After the user's approval, create the final review,
then run:

```bash
uv run python -m scripts.build_v1_2_motion_handoff
uv run python -m unittest tests.test_v1_2_turnaround_contract -v
```

Expected: `motion handoff written: 3 slots` and PASS.

- [ ] **Step 5: Run full Phase 1 verification**

Run:

```bash
uv run python -m unittest \
  tests.test_v1_2_turnaround_contract \
  tests.test_v1_2_turnaround_common \
  tests.test_v1_2_turnaround_generation_requests \
  tests.test_v1_2_turnaround_contact_sheet \
  tests.test_v1_2_turnaround_promotion -v
npm run test:node
npm run test:python
npm run audit
uv run python -m json.tool source/manifests/v1-2-turnaround/angle-slots.json >/dev/null
uv run python -m json.tool source/manifests/v1-2-turnaround/generation-requests.json >/dev/null
uv run python -m json.tool source/manifests/v1-2-turnaround/accepted-angles.json >/dev/null
uv run python -m json.tool source/manifests/v1-2-motion/phase-2-handoff.json >/dev/null
git diff --check
```

Expected: targeted Python, Node, full Python, and existing v1.1 regression
audits PASS; JSON parsing exits 0; `git diff --check` produces no output.

Run the repository Markdown command and record its result:

```bash
npm run lint:md
```

If it fails only because `.worktrees/*/node_modules` is included by the global
glob, run this targeted verification:

```bash
./node_modules/.bin/markdownlint-cli2 \
  docs/superpowers/specs/2026-07-10-akari-v1-2-turnaround-motion-design.md \
  docs/superpowers/plans/2026-07-10-akari-v1-2-canonical-turnaround.md
```

Expected targeted result: `Summary: 0 error(s)`.

- [ ] **Step 6: Commit the final Phase 1 gate**

```bash
git add dist/akari-v1.2-turnaround-contact-sheet.webp \
  evidence/v1-2-turnaround/reviews/final-eight-view-review.json \
  scripts/build_v1_2_motion_handoff.py \
  source/manifests/v1-2-motion/phase-2-handoff.json \
  tests/test_v1_2_turnaround_contract.py
git commit -m "feat: finalize akari v1.2 canonical turnaround"
```

- [ ] **Step 7: Report the Phase 2 handoff**

Report these exact inputs to the next planning session:

```text
source/manifests/v1-2-turnaround/accepted-angles.json
source/manifests/v1-2-turnaround/identity-lock.json
source/manifests/v1-2-motion/phase-2-handoff.json
dist/akari-v1.2-turnaround-contact-sheet.webp
evidence/v1-2-turnaround/reviews/final-eight-view-review.json
source/finished/v1-2-turnaround/front.webp
source/finished/v1-2-turnaround/character-left-front-three-quarter.webp
source/finished/v1-2-turnaround/character-left-profile.webp
source/finished/v1-2-turnaround/character-left-rear-three-quarter.webp
source/finished/v1-2-turnaround/back.webp
source/finished/v1-2-turnaround/character-right-rear-three-quarter.webp
source/finished/v1-2-turnaround/character-right-profile.webp
source/finished/v1-2-turnaround/character-right-front-three-quarter.webp
```

The next plan implements exactly three representative key poses: walking,
seated, and turning. It does not reopen the eight-view selection.

## Plan Self-Review

### Spec Coverage

- Tasks 1 through 5 may define tooling before the external face gate, while
  Task 6 hard-stops request materialization and generation unless the accepted
  selection path, identity rules, selection hash, and asset hash all match.
- The eight canonical views, character-perspective labels, standard outfit,
  canvas, and dependency graph are exact in Task 2.
- Front-rooted adjacent-angle production and back convergence are enforced by
  Tasks 3 and 6 through 10.
- Two or three candidates per angle, contact-sheet review, user approval, and
  `accept`/`hold`/`reject` records are covered by Tasks 3 through 10.
- Crown-to-sole landmark normalization, counterpart and set tolerances are
  executable in Tasks 1 and 4 and are enforced before any promotion output is
  written in Task 5.
- Accepted-only tracking, WebP promotion, hashes, and provenance are covered by
  Task 5.
- The final individual images, manifest, review records, and tracked contact
  sheet are completed in Task 11.
- Task 11 creates an exact three-slot walking, seated, and turning contract from
  the accepted eight-view paths and hashes. Image production is explicitly
  deferred to implementation Plan 2, so this plan does not claim the full
  two-phase design is complete.
- The v1.1 PDF remains untouched and no v1.2 PDF is added in this phase.

### Minimality

The plan adds five focused Python modules with one responsibility each: shared
deterministic helpers, request materialization, review visualization/landmark
checking, promotion/reopening, and Phase 2 handoff construction. It does not add
a 3D pipeline, PDF renderer, animation system, alternate outfits, or unrelated
refactoring.

### Existing Pattern Fit

Tests use `unittest`; manifests use JSON; contact sheets use Pillow; package
commands call `uv run python`; working generated assets remain ignored; and
accepted visual work uses contact-sheet-first review before promotion.

### Edge Verification

Tests and stage gates cover a missing or held face prerequisite, identity-rule
or hash drift, unknown slots, locked dependencies, conflicting request IDs,
append-only revisions with active batch selection, missing requested images,
invalid candidate states, multiple accepts, failed gates, missing notes, raw
landmark order, normalized landmark mismatch, incorrect canvas size, exact
output hash drift, pre-write left/right and full-set tolerance failure, mirrored
ornament risk, back-branch contradiction, transitive reopening with a complete
regeneration queue, final-set rejection recovery, and exactly three Phase 2
motion slots dependent on the accepted eight-view set.
