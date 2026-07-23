# Akari v1.2 Representative Motion Poses Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and run a traceable Phase 2 workflow that produces one accepted full-body walking, seated, and turning reference pose from the immutable Akari v1.2 eight-view turnaround.

**Architecture:** Add a small motion-specific Python workflow beside the existing turnaround tools. A shared contract module validates the Phase 1 handoff; separate request, contact-sheet, and promotion modules consume append-only JSON records, while generated candidates and contact sheets remain ignored working artifacts.

**Tech Stack:** Python 3.12, standard-library `unittest`, Pillow, JSON manifests, npm command aliases, Codex `view_image` and image generation.

## Global Constraints

- The accepted Phase 1 eight-view turnaround is immutable input and every request must carry all eight source references.
- Process motions sequentially in this exact order: `walking`, `seated`, `turning`.
- Create exactly three candidates per active motion batch and promote exactly one accepted candidate per motion.
- Use a 1024 by 1536 RGB portrait canvas, full-body framing, and a plain light background.
- Preserve the standard white oversized hoodie, gray pleated skirt, striped crew socks, chunky white-and-blue sneakers, and character-left pale-blue ornament.
- A seated pose uses an implied invisible support plane; no chair, backrest, or prop may appear.
- Keep `source/generated/v1-2-motion/` and `evidence/v1-2-motion/contact-sheets/` out of git.
- Do not modify `dist/akari-v1.1-settings.pdf` or add the Phase 2 images to a PDF.
- Before each identity-sensitive generation, open the current candidate when one exists and the strongest applicable accepted turnaround references with `view_image`, then state each reference's role.

---

### Task 1: Validate the Immutable Phase 1 Handoff

**Files:**

- Create: `scripts/v1_2_motion_common.py`
- Create: `tests/test_v1_2_motion_common.py`

**Interfaces:**

- Consumes: `phase-2-handoff.json`, its referenced accepted manifest, final review, and eight assets.
- Produces: `load_json(path: Path) -> dict`, `dump_json(path: Path, data: dict) -> None`, `sha256_file(path: Path) -> str`, `resolve_path(project_root: Path, path_text: str) -> Path`, and `validate_handoff(handoff: dict, project_root: Path) -> None`.

- [ ] **Step 1: Write failing handoff contract tests**

```python
# tests/test_v1_2_motion_common.py
import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.v1_2_motion_common import load_json, validate_handoff

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "source/manifests/v1-2-motion/phase-2-handoff.json"


class AkariV12MotionCommonTest(unittest.TestCase):
    def test_repository_handoff_is_valid(self):
        validate_handoff(load_json(HANDOFF), ROOT)

    def test_manifest_hash_drift_is_rejected(self):
        handoff = copy.deepcopy(load_json(HANDOFF))
        handoff["source_turnaround_manifest_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "manifest hash drift"):
            validate_handoff(handoff, ROOT)

    def test_asset_hash_drift_is_rejected(self):
        handoff = copy.deepcopy(load_json(HANDOFF))
        handoff["turnaround_inputs"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "asset hash drift"):
            validate_handoff(handoff, ROOT)

    def test_all_eight_canonical_slots_are_required(self):
        handoff = copy.deepcopy(load_json(HANDOFF))
        handoff["turnaround_inputs"].pop()
        with self.assertRaisesRegex(ValueError, "eight canonical turnaround inputs"):
            validate_handoff(handoff, ROOT)

    def test_final_review_must_still_be_approved(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            rejected = Path(temp_dir) / "rejected-review.json"
            rejected.write_text(json.dumps({"decision": "rejected", "user_decision": "approved"}), encoding="utf-8")
            handoff = copy.deepcopy(load_json(HANDOFF))
            handoff["source_final_review"] = rejected.as_posix()
            with self.assertRaisesRegex(ValueError, "final Phase 1 review"):
                validate_handoff(handoff, ROOT)
```

- [ ] **Step 2: Run the test and verify the missing module failure**

Run: `uv run python -m unittest tests.test_v1_2_motion_common -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.v1_2_motion_common'`.

- [ ] **Step 3: Implement the shared validator**

```python
# scripts/v1_2_motion_common.py
from __future__ import annotations

import hashlib
import json
from pathlib import Path

CANONICAL_SLOTS = (
    "front",
    "character-left-front-three-quarter",
    "character-left-profile",
    "character-left-rear-three-quarter",
    "back",
    "character-right-rear-three-quarter",
    "character-right-profile",
    "character-right-front-three-quarter",
)
MOTION_SLOTS = ("walking", "seated", "turning")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_path(project_root: Path, path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else project_root / path


def validate_handoff(handoff: dict, project_root: Path) -> None:
    source_manifest = resolve_path(project_root, handoff["source_turnaround_manifest"])
    if not source_manifest.is_file() or sha256_file(source_manifest) != handoff["source_turnaround_manifest_sha256"]:
        raise ValueError("source turnaround manifest hash drift")
    final_review_path = resolve_path(project_root, handoff["source_final_review"])
    if not final_review_path.is_file():
        raise ValueError("final Phase 1 review is missing")
    final_review = load_json(final_review_path)
    if final_review.get("decision") != "accepted" or final_review.get("user_decision") != "approved":
        raise ValueError("final Phase 1 review is not approved")
    inputs = handoff["turnaround_inputs"]
    if tuple(item["slot"] for item in inputs) != CANONICAL_SLOTS:
        raise ValueError("Phase 2 requires eight canonical turnaround inputs")
    accepted = {item["slot"]: item for item in load_json(source_manifest)["accepted_angles"]}
    for item in inputs:
        path = resolve_path(project_root, item["accepted_path"])
        if not path.is_file() or sha256_file(path) != item["sha256"]:
            raise ValueError(f"turnaround asset hash drift: {item['slot']}")
        if accepted[item["slot"]]["accepted_path"] != item["accepted_path"] or accepted[item["slot"]]["sha256"] != item["sha256"]:
            raise ValueError(f"handoff input disagrees with accepted manifest: {item['slot']}")
    slots = handoff["motion_slots"]
    if tuple(slot["slug"] for slot in slots) != MOTION_SLOTS:
        raise ValueError("motion slots must be walking, seated, turning")
    for slot in slots:
        if slot["candidate_count"] != 3 or slot["deliverable_count"] != 1:
            raise ValueError(f"invalid candidate contract: {slot['slug']}")
        if tuple(slot["required_turnaround_slots"]) != CANONICAL_SLOTS:
            raise ValueError(f"incomplete turnaround contract: {slot['slug']}")
```

- [ ] **Step 4: Run the focused tests**

Run: `uv run python -m unittest tests.test_v1_2_motion_common -v`

Expected: all five tests PASS.

- [ ] **Step 5: Commit the handoff validator**

```bash
git add scripts/v1_2_motion_common.py tests/test_v1_2_motion_common.py
git commit -m "feat: validate akari motion handoff"
```

### Task 2: Build Append-Only Motion Generation Requests

**Files:**

- Create: `scripts/build_v1_2_motion_generation_requests.py`
- Create: `tests/test_v1_2_motion_generation_requests.py`
- Create: `source/manifests/v1-2-motion/generation-requests.json`
- Modify: `package.json`

**Interfaces:**

- Consumes: `validate_handoff()`, Phase 2 handoff, motion slug, date prefix, revision, and optional failure observations.
- Produces: `build_ready_batch(handoff: dict, motion: str, date_prefix: str, revision: int, failure_observations: list[str]) -> dict`, `merge_request_history(existing: dict, batch: dict) -> dict`, and npm command `build:v1-2-motion:requests`.

- [ ] **Step 1: Write failing request builder tests**

```python
# tests/test_v1_2_motion_generation_requests.py
import unittest

from scripts.build_v1_2_motion_generation_requests import build_ready_batch, merge_request_history

HANDOFF = {
    "collection_id": "akari-v1.2-representative-motion-poses",
    "source_turnaround_manifest_sha256": "abc123",
    "turnaround_inputs": [{"slot": f"s{i}", "accepted_path": f"refs/{i}.webp", "sha256": str(i)} for i in range(8)],
    "motion_slots": [
        {"slug": slug, "candidate_count": 3, "deliverable_count": 1}
        for slug in ("walking", "seated", "turning")
    ],
}


class AkariV12MotionGenerationRequestsTest(unittest.TestCase):
    def test_walking_batch_has_three_distinct_requests_and_all_references(self):
        batch = build_ready_batch(HANDOFF, "walking", "20260713", 1, [])
        self.assertEqual(3, len(batch["requests"]))
        self.assertEqual(8, len(batch["requests"][0]["reference_pack_inputs"]))
        self.assertEqual([1, 2, 3], [item["candidate_number"] for item in batch["requests"]])
        self.assertEqual("batch:v1-2-motion:20260713:walking:r1", batch["active_batches"]["walking"])

    def test_motion_prompts_include_shared_and_pose_specific_locks(self):
        expected = {
            "walking": "readable mid-step",
            "seated": "invisible support plane",
            "turning": "face, shoulder, and hip rotation",
        }
        for motion, phrase in expected.items():
            request = build_ready_batch(HANDOFF, motion, "20260713", 1, [])["requests"][0]
            self.assertIn(phrase, request["prompt"])
            self.assertIn("character-left", request["prompt"])
            self.assertIn("1024x1536", request["prompt"])

    def test_regeneration_requires_failure_observations(self):
        with self.assertRaisesRegex(ValueError, "failure observations"):
            build_ready_batch(HANDOFF, "walking", "20260713", 2, [])

    def test_history_is_idempotent_and_rejects_older_reactivation(self):
        empty = {"schema_version": 1, "collection_id": HANDOFF["collection_id"], "active_batches": {}, "requests": []}
        first = build_ready_batch(HANDOFF, "walking", "20260713", 1, [])
        current = merge_request_history(empty, first)
        second = build_ready_batch(HANDOFF, "walking", "20260713", 2, ["all candidates had malformed feet"])
        revised = merge_request_history(current, second)
        self.assertEqual(revised, merge_request_history(revised, second))
        with self.assertRaisesRegex(ValueError, "older revision"):
            merge_request_history(revised, first)
```

- [ ] **Step 2: Run the tests and verify the missing module failure**

Run: `uv run python -m unittest tests.test_v1_2_motion_generation_requests -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement request construction and history merging**

Create `scripts/build_v1_2_motion_generation_requests.py` with these exact public constants and record fields:

```python
ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = ROOT / "source/manifests/v1-2-motion/phase-2-handoff.json"
OUTPUT_PATH = ROOT / "source/manifests/v1-2-motion/generation-requests.json"
PROMPT_TEMPLATE_VERSION = "akari_v1_2_representative_motion_v1"
MOTION_ORDER = {"walking": 1, "seated": 2, "turning": 3}
POSE_VARIATIONS = {
    "walking": ("heel-strike with modest stride and opposite arm swing", "mid-stance with compact stride and relaxed arms", "toe-off with restrained garment and hair follow-through"),
    "seated": ("knees offset left, hands near knees, upright torso", "feet offset right, hands beside body, slight forward inclination", "asymmetric feet, one hand near knee and one beside body"),
    "turning": ("early mid-turn with gaze leading shoulders", "over-shoulder moment with hips lagging", "later turn with restrained hair and hoodie follow-through"),
}
```

Each request must contain `id`, `batch_id`, `motion_order`, `motion`, `revision`, `candidate_number`, `variation`, `reference_pack_inputs`, `source_pack_sha256`, `target_path`, `prompt_template_version`, `prompt`, `acceptance_gates`, and `review_plan`. Build IDs and paths as:

```python
batch_id = f"batch:v1-2-motion:{date_prefix}:{motion}:r{revision}"
request_id = f"request:v1-2-motion:{date_prefix}:{motion}:r{revision}:c{candidate_number}"
target_path = f"source/generated/v1-2-motion/{date_prefix}_{motion}_r{revision}_c{candidate_number}.png"
```

The shared prompt text must explicitly require all eight attached references, adult identity and age impression, standard outfit and footwear, character-left ornament, full body, 1024x1536 RGB portrait, plain light background, restrained perspective, and no props/text/logos/watermarks. Append the exact pose requirement selected from `POSE_VARIATIONS`, the motion-specific specification from the approved design, and joined `failure_observations` for revisions above one. Copy the ten acceptance gates from the approved design into `acceptance_gates` as an ordered list.

Implement `merge_request_history()` with the same append-only/conflicting-ID/older-revision behavior as `scripts/build_v1_2_turnaround_generation_requests.py`, sorting by `motion_order`, `revision`, and `candidate_number`. The CLI must require `--motion`, accept `--date-prefix`, `--revision`, repeatable `--failure-observation`, `--handoff`, and `--output`; it must call `validate_handoff()` before writing.

- [ ] **Step 4: Add the initial empty manifest and npm entry**

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.2-representative-motion-poses",
  "prompt_template_version": "akari_v1_2_representative_motion_v1",
  "active_batches": {},
  "requests": []
}
```

Add to `package.json`:

```json
"build:v1-2-motion:requests": "uv run python -m scripts.build_v1_2_motion_generation_requests"
```

- [ ] **Step 5: Run unit and CLI contract tests**

Run: `uv run python -m unittest tests.test_v1_2_motion_generation_requests -v && bash -lc 'npm run build:v1-2-motion:requests -- --help'`

Expected: all tests PASS and help lists `--motion`, `--revision`, and `--failure-observation`.

- [ ] **Step 6: Commit the request builder**

```bash
git add scripts/build_v1_2_motion_generation_requests.py tests/test_v1_2_motion_generation_requests.py source/manifests/v1-2-motion/generation-requests.json package.json
git commit -m "feat: build akari motion generation requests"
```

### Task 3: Validate Reviews and Promote Accepted Motion Poses

**Files:**

- Create: `scripts/promote_v1_2_motion_candidate.py`
- Create: `tests/test_v1_2_motion_promotion.py`
- Create: `source/manifests/v1-2-motion/accepted-selection.json`
- Modify: `package.json`

**Interfaces:**

- Consumes: Phase 2 handoff, request manifest, one tracked review JSON, current accepted-selection manifest, and candidate PNGs.
- Produces: `validate_review(review: dict, request_manifest: dict, handoff: dict) -> dict`, `promote_review(review: dict, request_manifest: dict, handoff: dict, accepted: dict, project_root: Path, replace: bool = False) -> dict`, three WebPs, and npm command `promote:v1-2-motion`.

- [ ] **Step 1: Write failing review and promotion tests**

```python
# tests/test_v1_2_motion_promotion.py
import copy
import tempfile
import unittest
from pathlib import Path
from PIL import Image

from scripts.promote_v1_2_motion_candidate import promote_review
from scripts.v1_2_motion_common import sha256_file

GATES = {
    "identity", "age", "anatomy_pose", "body_proportion", "outfit",
    "footwear", "ornament_side", "framing", "artifacts_quality",
    "motion_naturalness",
}


def handoff_for() -> dict:
    return {"source_turnaround_manifest_sha256": "pack-hash"}


def request_manifest_for(root: Path) -> tuple[dict, list[str]]:
    paths = []
    requests = []
    for number in range(1, 4):
        path = root / f"walking-c{number}.png"
        Image.new("RGB", (1024, 1536), "white").save(path)
        paths.append(path.as_posix())
        requests.append({
            "id": f"walking-r1-c{number}", "batch_id": "walking-r1",
            "motion": "walking", "revision": 1,
            "candidate_number": number, "target_path": path.as_posix(),
            "source_pack_sha256": "pack-hash",
        })
    return {"active_batches": {"walking": "walking-r1"}, "requests": requests}, paths


def review_for(requests: dict, paths: list[str]) -> dict:
    decisions = ("accept", "hold", "reject")
    return {
        "review_id": "walking-r1-review",
        "review_path": "evidence/v1-2-motion/reviews/walking-r1-review.json",
        "motion": "walking", "batch_id": "walking-r1",
        "user_decision": "approved",
        "candidates": [{
            "request_id": request["id"], "candidate_path": path,
            "decision": decision,
            "gates": {gate: "pass" for gate in GATES},
            "observations": {gate: f"{gate} checked" for gate in GATES},
            "rejection_reason": "malformed hand" if decision == "reject" else "",
        } for request, path, decision in zip(requests["requests"], paths, decisions)],
    }


def empty_selection() -> dict:
    return {"schema_version": 1, "collection_id": "akari-v1.2-representative-motion-poses", "accepted_motions": []}


class AkariV12MotionPromotionTest(unittest.TestCase):
    def test_promotes_only_the_single_accepted_active_candidate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, paths = request_manifest_for(root)
            review = review_for(requests, paths)
            result = promote_review(review, requests, handoff_for(), empty_selection(), root)
            record = result["accepted_motions"][0]
            output = root / record["finished_path"]
            self.assertEqual("walking", record["motion"])
            self.assertTrue(output.is_file())
            self.assertEqual(sha256_file(output), record["finished_sha256"])
            self.assertEqual(sha256_file(Path(paths[0])), record["source_sha256"])

    def test_rejects_missing_or_multiple_accepts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, paths = request_manifest_for(root)
            for states in (("hold", "hold", "reject"), ("accept", "accept", "reject")):
                changed = review_for(requests, paths)
                for candidate, state in zip(changed["candidates"], states):
                    candidate["decision"] = state
                with self.assertRaisesRegex(ValueError, "exactly one accepted candidate"):
                    promote_review(changed, requests, handoff_for(), empty_selection(), root)

    def test_rejects_failed_or_missing_gate_and_request_mismatch(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, paths = request_manifest_for(root)
            review = review_for(requests, paths)
            failed = copy.deepcopy(review)
            failed["candidates"][0]["gates"]["footwear"] = "fail"
            with self.assertRaisesRegex(ValueError, "all acceptance gates"):
                promote_review(failed, requests, handoff_for(), empty_selection(), root)
            mismatched = copy.deepcopy(review)
            mismatched["candidates"][0]["candidate_path"] = "wrong.png"
            with self.assertRaisesRegex(ValueError, "request target"):
                promote_review(mismatched, requests, handoff_for(), empty_selection(), root)

    def test_rejects_source_pack_drift_and_implicit_replacement(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, paths = request_manifest_for(root)
            review = review_for(requests, paths)
            stale = {"source_turnaround_manifest_sha256": "stale"}
            with self.assertRaisesRegex(ValueError, "source pack"):
                promote_review(review, requests, stale, empty_selection(), root)
            existing = empty_selection()
            existing["accepted_motions"] = [{"motion": "walking"}]
            with self.assertRaisesRegex(ValueError, "already accepted"):
                promote_review(review, requests, handoff_for(), existing, root)
```

- [ ] **Step 2: Run the tests and verify the missing module failure**

Run: `uv run python -m unittest tests.test_v1_2_motion_promotion -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement review validation and atomic promotion**

Define these exact gates and states:

```python
REQUIRED_GATES = {
    "identity", "age", "anatomy_pose", "body_proportion", "outfit",
    "footwear", "ornament_side", "framing", "artifacts_quality",
    "motion_naturalness",
}
ALLOWED_DECISIONS = {"accept", "hold", "reject"}
MOTION_ORDER = {"walking": 1, "seated": 2, "turning": 3}
```

`validate_review()` must require `user_decision == "approved"`, one active batch, coverage of all three active requests, exact request ID/path matches, a non-empty observation for every gate, rejection reasons for rejected candidates, exactly one `accept`, and `pass` for every gate on the accepted candidate. It must return the accepted `(candidate, request)` pair.

`promote_review()` must compare every request's `source_pack_sha256` with the handoff hash, call `validate_review()`, reject an existing motion unless `replace=True`, verify the accepted image is exactly 1024x1536, then write `source/finished/v1-2-motion/<motion>.webp` with RGB, quality 94, and method 6. Build the record as:

```python
record = {
    "motion": motion,
    "motion_order": MOTION_ORDER[motion],
    "finished_path": f"source/finished/v1-2-motion/{motion}.webp",
    "source_candidate_path": candidate["candidate_path"],
    "request_id": request["id"],
    "batch_id": request["batch_id"],
    "revision": request["revision"],
    "candidate_number": request["candidate_number"],
    "review_id": review["review_id"],
    "review_path": review["review_path"],
    "source_pack_sha256": request["source_pack_sha256"],
    "source_sha256": sha256_file(source_path),
    "finished_sha256": sha256_file(output_path),
}
```

Write output only after every validation succeeds. The CLI accepts `--review`, `--requests`, `--handoff`, `--accepted`, and explicit `--replace`.

- [ ] **Step 4: Add the initial selection manifest and npm entry**

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.2-representative-motion-poses",
  "accepted_motions": []
}
```

Add to `package.json`:

```json
"promote:v1-2-motion": "uv run python -m scripts.promote_v1_2_motion_candidate"
```

- [ ] **Step 5: Run promotion tests and CLI help**

Run: `uv run python -m unittest tests.test_v1_2_motion_promotion -v && bash -lc 'npm run promote:v1-2-motion -- --help'`

Expected: all tests PASS and help includes `--review` and `--replace`.

- [ ] **Step 6: Commit the promotion workflow**

```bash
git add scripts/promote_v1_2_motion_candidate.py tests/test_v1_2_motion_promotion.py source/manifests/v1-2-motion/accepted-selection.json package.json
git commit -m "feat: promote reviewed akari motion poses"
```

### Task 4: Build Motion Batch and Final Contact Sheets

**Files:**

- Create: `scripts/build_v1_2_motion_contact_sheet.py`
- Create: `tests/test_v1_2_motion_contact_sheet.py`
- Modify: `package.json`
- Modify: `.gitignore`

**Interfaces:**

- Consumes: active request metadata for batch sheets, review decisions when present, and accepted-selection metadata for the final sheet.
- Produces: `select_active_requests(manifest: dict, motion: str) -> list[dict]`, `build_batch_contact_sheet(requests: list[dict], reviews: dict[str, dict], project_root: Path, output_path: Path) -> Path`, `build_final_contact_sheet(accepted_records: list[dict], project_root: Path, output_path: Path) -> Path`, and npm command `build:v1-2-motion:contact-sheet`.

- [ ] **Step 1: Write failing contact-sheet tests**

```python
# tests/test_v1_2_motion_contact_sheet.py
import tempfile
import unittest
from pathlib import Path
from PIL import Image

from scripts.build_v1_2_motion_contact_sheet import build_batch_contact_sheet, build_final_contact_sheet, select_active_requests


def request(motion: str, batch: str, number: int, path: str) -> dict:
    return {"motion": motion, "batch_id": batch, "revision": int(batch[-1]), "candidate_number": number, "target_path": path}


def make_image(path: Path, color: str = "white") -> str:
    Image.new("RGB", (1024, 1536), color).save(path)
    return path.as_posix()


class AkariV12MotionContactSheetTest(unittest.TestCase):
    def test_selects_three_requests_from_only_the_active_batch(self):
        manifest = {"active_batches": {"walking": "walking-r2"}, "requests": [
            request("walking", batch, number, f"{batch}-c{number}.png")
            for batch in ("walking-r1", "walking-r2") for number in range(1, 4)
        ]}
        selected = select_active_requests(manifest, "walking")
        self.assertEqual([1, 2, 3], [item["candidate_number"] for item in selected])
        self.assertEqual({"walking-r2"}, {item["batch_id"] for item in selected})

    def test_batch_sheet_orders_by_candidate_number_and_labels_decisions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests = [request("walking", "walking-r1", number, make_image(root / f"c{number}.png")) for number in (3, 2, 1)]
            reviews = {f"walking-r1-c{number}": {"decision": decision} for number, decision in enumerate(("accept", "hold", "reject"), 1)}
            for number, item in enumerate(sorted(requests, key=lambda value: value["candidate_number"]), 1):
                item["id"] = f"walking-r1-c{number}"
            output = root / "batch.webp"
            self.assertEqual(output, build_batch_contact_sheet(requests, reviews, root, output))
            with Image.open(output) as sheet:
                self.assertEqual("RGB", sheet.mode)
                self.assertEqual((1152, 638), sheet.size)

    def test_batch_sheet_rejects_missing_or_unreadable_images(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests = [request("walking", "walking-r1", number, (root / f"missing-{number}.png").as_posix()) for number in range(1, 4)]
            with self.assertRaisesRegex(ValueError, "missing or unreadable candidate"):
                build_batch_contact_sheet(requests, {}, root, root / "batch.webp")

    def test_final_sheet_requires_walking_seated_turning_in_order(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            records = [{"motion": motion, "motion_order": order, "finished_path": make_image(root / f"{motion}.webp")} for order, motion in enumerate(("walking", "seated", "turning"), 1)]
            with self.assertRaisesRegex(ValueError, "exactly three accepted motions"):
                build_final_contact_sheet(records[:2], root, root / "bad.webp")
            output = root / "final.webp"
            self.assertEqual(output, build_final_contact_sheet(list(reversed(records)), root, output))
```

- [ ] **Step 2: Run the tests and verify the missing module failure**

Run: `uv run python -m unittest tests.test_v1_2_motion_contact_sheet -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement deterministic batch and final sheets**

Reuse the Pillow layout and font fallback pattern from `scripts/build_v1_2_turnaround_contact_sheet.py`. Use 360x540 contained images, a 62-pixel label area, and an 18-pixel gap. Batch sheets must sort by `candidate_number`, require exactly three records sharing one motion and batch, and label each card `<motion> / r<revision> / c<candidate_number>` plus `accept`, `hold`, `reject`, or `unreviewed` outside the image. Final sheets must require exactly `walking`, `seated`, `turning`, sort by `motion_order`, and use each record's `finished_path`.

The CLI uses mutually exclusive `--requests` and `--accepted`, accepts `--motion`, repeatable `--review`, and `--output`, and fails before writing when any source image is missing or unreadable.

- [ ] **Step 4: Add the npm entry and ignore only working outputs**

Add to `package.json`:

```json
"build:v1-2-motion:contact-sheet": "uv run python -m scripts.build_v1_2_motion_contact_sheet"
```

Append to `.gitignore`:

```gitignore
source/generated/v1-2-motion/
evidence/v1-2-motion/contact-sheets/
```

Do not ignore `evidence/v1-2-motion/reviews/`; review records must remain trackable.

- [ ] **Step 5: Run contact-sheet and ignore-contract checks**

Run: `uv run python -m unittest tests.test_v1_2_motion_contact_sheet -v && git check-ignore source/generated/v1-2-motion/example.png evidence/v1-2-motion/contact-sheets/example.webp && ! git check-ignore evidence/v1-2-motion/reviews/example.json`

Expected: all tests PASS; both working paths are printed as ignored; the review path is not ignored.

- [ ] **Step 6: Commit the contact-sheet workflow**

```bash
git add scripts/build_v1_2_motion_contact_sheet.py tests/test_v1_2_motion_contact_sheet.py package.json .gitignore
git commit -m "feat: build akari motion contact sheets"
```

### Task 5: Run the Sequential Three-Pose Production Workflow

**Files:**

- Modify: `source/manifests/v1-2-motion/generation-requests.json`
- Modify: `source/manifests/v1-2-motion/accepted-selection.json`
- Create: `evidence/v1-2-motion/reviews/<motion>-r<revision>-review.json`
- Create locally, ignored: `source/generated/v1-2-motion/*.png`
- Create locally, ignored: `evidence/v1-2-motion/contact-sheets/*.webp`
- Create: `source/finished/v1-2-motion/walking.webp`
- Create: `source/finished/v1-2-motion/seated.webp`
- Create: `source/finished/v1-2-motion/turning.webp`

**Interfaces:**

- Consumes: all tools from Tasks 1-4 plus user visual approval.
- Produces: three accepted WebPs, three tracked review records, populated request/selection manifests, three batch sheets, and one final sheet.

- [ ] **Step 1: Build the walking request batch**

Run: `bash -lc 'npm run build:v1-2-motion:requests -- --motion walking --date-prefix 20260713 --revision 1'`

Expected: `motion requests written: 3`, with exactly one active walking batch and three new request records.

- [ ] **Step 2: Inspect references and generate walking candidates**

Open the accepted front, both front-three-quarter, both profile, both rear-three-quarter, and back images with `view_image`. State that front/front-three-quarter views lock face, body, and outfit; profiles lock gait silhouette and footwear; rear-three-quarter/back views lock hair, hoodie, skirt construction, and ornament continuity. Generate each walking request with all eight references present in the request contract and save the returned image to its exact `target_path`. Open every saved candidate with `view_image` before judging it.

- [ ] **Step 3: Build, inspect, and record the walking review**

Run:

```bash
bash -lc 'npm run build:v1-2-motion:contact-sheet -- --requests source/manifests/v1-2-motion/generation-requests.json --motion walking --output evidence/v1-2-motion/contact-sheets/walking-r1.webp'
```

Open the batch sheet and each candidate. Write `evidence/v1-2-motion/reviews/walking-r1-review.json` with `review_id`, its own `review_path`, `motion`, `batch_id`, `user_decision`, and all three candidates. Each candidate contains `request_id`, `candidate_path`, `decision`, the ten named gate results, ten non-empty gate observations, and `rejection_reason`; exactly one decision is `accept`.

- [ ] **Step 4: Promote walking or create only a walking revision**

If one candidate passes and the user approves it, run:

```bash
bash -lc 'npm run promote:v1-2-motion -- --review evidence/v1-2-motion/reviews/walking-r1-review.json'
```

If all three fail, keep the rejection review and run revision 2 with one repeatable flag per concrete failure:

```bash
bash -lc 'npm run build:v1-2-motion:requests -- --motion walking --date-prefix 20260713 --revision 2 --failure-observation "feet lost ground contact and sneaker construction" --failure-observation "arm swing became too energetic for a reference pose"'
```

Repeat Steps 2-4 for walking only; do not regenerate another motion.

- [ ] **Step 5: Repeat the same gated loop for seated**

Run the request builder for `seated`. Before generation, reopen the full accepted turnaround and the accepted walking image, explaining that walking is a cross-pose identity/finish check rather than a replacement for the eight mandatory sources. Enforce invisible support, believable pelvis balance, readable offset legs, complete shoes, natural hands, and no visible chair/backrest/prop. Build `seated-r1.webp`, record the three-candidate review, obtain user approval, and promote exactly one seated image; revise seated alone if all three fail.

- [ ] **Step 6: Repeat the same gated loop for turning**

Run the request builder for `turning`. Before generation, reopen front, profiles, rear-three-quarters, back, and the accepted walking/seated images. Explain that profiles and rear/back views govern face-shoulder-hip rotation and ornament side, while prior motions check identity and finish consistency. Enforce a believable staggered rotation without an extreme spinal twist or mirrored ornament. Build `turning-r1.webp`, record the review, obtain user approval, and promote exactly one turning image; revise turning alone if all three fail.

- [ ] **Step 7: Build and visually approve the final three-pose sheet**

Run:

```bash
bash -lc 'npm run build:v1-2-motion:contact-sheet -- --accepted source/manifests/v1-2-motion/accepted-selection.json --output evidence/v1-2-motion/contact-sheets/final-three-pose.webp'
```

Open all three finished WebPs individually and the final sheet with `view_image`. Confirm identity, adult age impression, anatomy, body proportion, outfit, footwear, character-left ornament, full framing, artifact quality, and natural motion across the set. Do not declare Phase 2 complete until the user approves the final sheet.

- [ ] **Step 8: Run focused and repository-wide verification**

Run:

```bash
uv run python -m unittest \
  tests.test_v1_2_motion_common \
  tests.test_v1_2_motion_generation_requests \
  tests.test_v1_2_motion_promotion \
  tests.test_v1_2_motion_contact_sheet -v
bash -lc 'npm run test:node && npm run test:python && npm run audit'
bash -lc 'npm run lint:md'
git diff --check
```

Expected: focused tests, Node tests, Python tests, and audits PASS; `git diff --check` reports nothing. If Markdown lint still traverses `.worktrees/*/node_modules`, record that pre-existing glob failure separately and also run `./node_modules/.bin/markdownlint-cli2 docs/superpowers/plans/2026-07-13-akari-v1-2-representative-motion-poses.md` to prove the new plan is clean.

- [ ] **Step 9: Commit the approved Phase 2 deliverables**

```bash
git add \
  source/manifests/v1-2-motion/generation-requests.json \
  source/manifests/v1-2-motion/accepted-selection.json \
  evidence/v1-2-motion/reviews \
  source/finished/v1-2-motion
git commit -m "feat: finalize akari v1.2 motion poses"
```

Verify `git status --short` contains no generated candidates or contact sheets. Generated folders remain uncommitted unless the user explicitly asks to preserve them.
