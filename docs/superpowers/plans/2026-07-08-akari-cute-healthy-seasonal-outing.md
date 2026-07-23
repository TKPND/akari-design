# Akari Cute Healthy Seasonal Outing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reference-backed eight-image `cute_healthy` seasonal outing request batch for `となりのコーデ`, then generate and review only through a reference-image-capable workflow.

**Architecture:** Keep the new batch as a separate request manifest under the existing `tonari-no-coordinate` manifest directory. Reuse the existing coordinate contact-sheet builder by passing the new request manifest path, and keep generated images plus evidence under already ignored working directories. The manifest must make reference image usage explicit so no worker can accidentally run prompt-only generation.

**Tech Stack:** Python 3.11, `unittest`, JSON manifests, Pillow contact-sheet tooling, `uv run python`, existing npm scripts, a reference-image-capable image generation route.

---

## Scope Check

The approved spec covers one subsystem: an eight-image seasonal outing
extension batch for the existing `cute_healthy` coordinate direction. This plan
does not update PDFs, replace existing coordinate images, redesign Akari's base
body, or broaden the batch beyond eight candidates.

Reference images are mandatory during generation. If the active image
generation route cannot attach image references, do not generate images with
prompt text alone. Stop after the committed request manifest and report that a
reference-capable route is required.

## Current Context

- Approved design spec:
  `docs/superpowers/specs/2026-07-08-akari-cute-healthy-seasonal-outing-design.md`
- Existing coordinate request manifest:
  `source/manifests/tonari-no-coordinate/generation-requests.json`
- Existing coordinate slot map:
  `source/manifests/tonari-no-coordinate/coordinate-slots.json`
- Existing coordinate contact-sheet script:
  `scripts/build_tonari_no_coordinate_contact_sheet.py`
- Existing generated coordinate directory, already ignored:
  `source/generated/tonari-no-coordinate/`
- Existing evidence directory, already ignored:
  `evidence/tonari-no-coordinate/`
- Required reference image pack:
  `source/references/tonari-no-akari/identity-face-hair.webp`,
  `source/references/tonari-no-akari/identity-body-base.webp`,
  `source/references/tonari-no-akari/identity-basic-outfit.webp`,
  `source/references/tonari-no-akari/identity-side-view.webp`,
  `source/originals/v1_1_front_1.webp`

## File Structure

- Create `tests/test_tonari_no_coordinate_cute_healthy_seasonal_contract.py`
  - Contract tests for the new standalone request manifest, including exact
    candidate slots, seasonal balance, outfit distribution, reference pack,
    reference usage instructions, prompt boundaries, and ignored generated
    output paths.
- Create
  `source/manifests/tonari-no-coordinate/cute-healthy-seasonal-outing-requests.json`
  - Source-of-truth generation request manifest for the eight candidates.
- Modify `tests/test_tonari_no_coordinate_contact_sheet.py`
  - Add coverage that the existing contact-sheet label fitting works with the
    new request manifest.
- Working-only generated outputs:
  - `source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_<slot>_v1.webp`
  - `evidence/tonari-no-coordinate/contact-sheets/cute-healthy-seasonal-outing-first-pass.webp`

## Data Model

Use this manifest shape:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.1-tonari-no-coordinate-cute-healthy-seasonal-outing",
  "title": "となりのコーデ cute healthy seasonal outing",
  "reference_pack_version": "tonari-no-akari-identity-plus-v1-1-leg-reference-v1",
  "prompt_template_version": "tonari_coordinate_cute_healthy_seasonal_reference_v1",
  "batch_policy": {
    "candidate_count": 8,
    "seasonal_balance": {
      "spring": 2,
      "summer": 2,
      "autumn": 2,
      "winter": 2
    },
    "composition": "knee_up_default",
    "outfit_distribution": {
      "skirt_dress_jumper_skirt": 6,
      "shorts_culotte": 2
    },
    "background_policy": "quiet_seasonal_support_only",
    "reference_policy": "image_references_required_no_prompt_only_generation",
    "pdf_policy": "not_in_this_phase"
  },
  "requests": []
}
```

Every request must include:

- `id`
- `coordinate_order`
- `slot`
- `japanese_title`
- `season`
- `scene`
- `outfit_family`
- `outfit_notes`
- `charm_notes`
- `leg_quality_notes`
- `composition`
- `tone`
- `risk_note`
- `target_path`
- `reference_pack_inputs`
- `reference_usage`
- `prompt`
- `acceptance`
- `risk_profile`
- `review_plan`

## Task 1: Add The Failing Seasonal Contract Test

**Files:**

- Create: `tests/test_tonari_no_coordinate_cute_healthy_seasonal_contract.py`

- [ ] **Step 1: Write the failing contract test**

Create
`tests/test_tonari_no_coordinate_cute_healthy_seasonal_contract.py`:

```python
import json
import re
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT
    / "source/manifests/tonari-no-coordinate/cute-healthy-seasonal-outing-requests.json"
)
COLLECTION_ID = "akari-v1.1-tonari-no-coordinate-cute-healthy-seasonal-outing"
TITLE = "となりのコーデ cute healthy seasonal outing"
REFERENCE_PACK_VERSION = "tonari-no-akari-identity-plus-v1-1-leg-reference-v1"
PROMPT_TEMPLATE_VERSION = "tonari_coordinate_cute_healthy_seasonal_reference_v1"
DATE_PREFIX = "20260708"
REFERENCE_PACK_INPUTS = [
    "source/references/tonari-no-akari/identity-face-hair.webp",
    "source/references/tonari-no-akari/identity-body-base.webp",
    "source/references/tonari-no-akari/identity-basic-outfit.webp",
    "source/references/tonari-no-akari/identity-side-view.webp",
    "source/originals/v1_1_front_1.webp",
]
REFERENCE_USAGE_KEYS = {
    "face_hair_identity",
    "body_balance",
    "default_outfit_context",
    "side_view_identity",
    "leg_quality_reference",
}
EXPECTED_CANDIDATES = [
    {
        "slot": "spring-light-cardigan-flare-dress",
        "title": "春の薄カーデワンピ",
        "season": "spring",
        "outfit_family": "skirt_dress_jumper_skirt",
    },
    {
        "slot": "spring-denim-short-jacket-skirt",
        "title": "春のデニム短ジャケット",
        "season": "spring",
        "outfit_family": "skirt_dress_jumper_skirt",
    },
    {
        "slot": "summer-puff-sleeve-blouse-skirt",
        "title": "夏のパフ袖ブラウス",
        "season": "summer",
        "outfit_family": "skirt_dress_jumper_skirt",
    },
    {
        "slot": "summer-collar-blouse-culotte",
        "title": "夏襟ブラウスとキュロット",
        "season": "summer",
        "outfit_family": "shorts_culotte",
    },
    {
        "slot": "autumn-short-knit-check-skirt",
        "title": "秋の短めニット",
        "season": "autumn",
        "outfit_family": "skirt_dress_jumper_skirt",
    },
    {
        "slot": "autumn-jumper-skirt-thin-turtleneck",
        "title": "秋のジャンスカ",
        "season": "autumn",
        "outfit_family": "skirt_dress_jumper_skirt",
    },
    {
        "slot": "winter-knit-onepiece-short-coat",
        "title": "冬のニットワンピ",
        "season": "winter",
        "outfit_family": "skirt_dress_jumper_skirt",
    },
    {
        "slot": "winter-short-duffle-culotte",
        "title": "冬の短めダッフル",
        "season": "winter",
        "outfit_family": "shorts_culotte",
    },
]
IDENTITY_LOCK_PHRASES = [
    "adult 25-year-old japanese woman",
    "akari identity",
    "short warm-brown bob",
    "warm amber eyes",
    "pale blue hair ornament",
    "cute adult private outing clothes",
]
REFERENCE_PHRASES = [
    "use the attached reference images",
    "do not generate from prompt text alone",
    "identity-face-hair",
    "identity-body-base",
    "identity-basic-outfit",
    "identity-side-view",
    "v1_1_front_1",
]
LEG_QUALITY_PHRASES = [
    "soft thigh volume",
    "natural knee shape",
    "calf transition",
    "healthy leg line",
]
IMAGE_TEXT_BANS = [
    "no readable image text",
    "no logos",
    "no watermarks",
    "no frame",
    "no panel layout",
]
BANNED_PROMPT_FRAGMENTS = {
    "school uniform",
    "teenage",
    "little girl",
    "child body",
    "explicit nude",
    "pin-up pose",
    "glamour model",
    "brand logo",
}
OVERBROAD_NEGATIVE_FRAGMENTS = {
    "no skin",
    "fully covered",
    "ultra conservative",
    "extremely modest",
    "no attraction",
}
JAPANESE_TEXT = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")


def load_json(path):
    with path.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


class TonariNoCoordinateCuteHealthySeasonalContractTest(unittest.TestCase):
    def test_generated_working_paths_are_ignored_by_git(self):
        ignored_paths = [
            "source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_example_v1.webp",
            "evidence/tonari-no-coordinate/contact-sheets/cute-healthy-seasonal-outing-first-pass.webp",
        ]

        for path in ignored_paths:
            with self.subTest(path=path):
                result = subprocess.run(
                    ["git", "check-ignore", path],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )

                self.assertEqual(0, result.returncode, result.stderr)

    def test_manifest_exists_and_records_reference_backed_batch_policy(self):
        self.assertTrue(MANIFEST.is_file(), f"missing manifest: {MANIFEST}")
        manifest = load_json(MANIFEST)

        self.assertEqual(1, manifest["schema_version"])
        self.assertEqual(COLLECTION_ID, manifest["collection_id"])
        self.assertEqual(TITLE, manifest["title"])
        self.assertEqual(REFERENCE_PACK_VERSION, manifest["reference_pack_version"])
        self.assertEqual(PROMPT_TEMPLATE_VERSION, manifest["prompt_template_version"])
        self.assertEqual(8, manifest["batch_policy"]["candidate_count"])
        self.assertEqual(
            {"spring": 2, "summer": 2, "autumn": 2, "winter": 2},
            manifest["batch_policy"]["seasonal_balance"],
        )
        self.assertEqual("knee_up_default", manifest["batch_policy"]["composition"])
        self.assertEqual(
            {"skirt_dress_jumper_skirt": 6, "shorts_culotte": 2},
            manifest["batch_policy"]["outfit_distribution"],
        )
        self.assertEqual(
            "quiet_seasonal_support_only",
            manifest["batch_policy"]["background_policy"],
        )
        self.assertEqual(
            "image_references_required_no_prompt_only_generation",
            manifest["batch_policy"]["reference_policy"],
        )
        self.assertEqual("not_in_this_phase", manifest["batch_policy"]["pdf_policy"])

    def test_reference_pack_inputs_exist(self):
        for reference_path in REFERENCE_PACK_INPUTS:
            with self.subTest(reference_path=reference_path):
                self.assertTrue((ROOT / reference_path).is_file())

    def test_manifest_has_exactly_eight_ordered_candidates(self):
        requests = load_json(MANIFEST)["requests"]

        self.assertEqual(8, len(requests))
        self.assertEqual(
            [candidate["slot"] for candidate in EXPECTED_CANDIDATES],
            [request["slot"] for request in requests],
        )
        self.assertEqual(list(range(1, 9)), [request["coordinate_order"] for request in requests])
        self.assertEqual(
            {"spring": 2, "summer": 2, "autumn": 2, "winter": 2},
            dict(Counter(request["season"] for request in requests)),
        )
        self.assertEqual(
            {"skirt_dress_jumper_skirt": 6, "shorts_culotte": 2},
            dict(Counter(request["outfit_family"] for request in requests)),
        )

    def test_requests_match_candidate_contract(self):
        requests = load_json(MANIFEST)["requests"]

        for request, expected in zip(requests, EXPECTED_CANDIDATES, strict=True):
            with self.subTest(slot=expected["slot"]):
                self.assertEqual(
                    f"request:tonari-coordinate-cute-healthy-seasonal-{expected['slot']}",
                    request["id"],
                )
                self.assertEqual(expected["slot"], request["slot"])
                self.assertEqual(expected["title"], request["japanese_title"])
                self.assertTrue(JAPANESE_TEXT.search(request["japanese_title"]))
                self.assertEqual(expected["season"], request["season"])
                self.assertEqual(expected["outfit_family"], request["outfit_family"])
                self.assertEqual("knee_up", request["composition"])
                self.assertTrue(request["outfit_notes"])
                self.assertTrue(request["charm_notes"])
                self.assertTrue(request["leg_quality_notes"])
                self.assertTrue(request["risk_note"])
                self.assertEqual(REFERENCE_PACK_INPUTS, request["reference_pack_inputs"])
                self.assertEqual(
                    f"source/generated/tonari-no-coordinate/{DATE_PREFIX}_cute-healthy-seasonal_{expected['slot']}_v1.webp",
                    request["target_path"],
                )

    def test_reference_usage_is_explicit_and_generation_ready(self):
        requests = load_json(MANIFEST)["requests"]

        for request in requests:
            with self.subTest(slot=request["slot"]):
                usage = request["reference_usage"]
                self.assertEqual(REFERENCE_USAGE_KEYS, set(usage))
                self.assertEqual(
                    "source/references/tonari-no-akari/identity-face-hair.webp",
                    usage["face_hair_identity"]["path"],
                )
                self.assertEqual(
                    "source/references/tonari-no-akari/identity-body-base.webp",
                    usage["body_balance"]["path"],
                )
                self.assertEqual(
                    "source/references/tonari-no-akari/identity-basic-outfit.webp",
                    usage["default_outfit_context"]["path"],
                )
                self.assertEqual(
                    "source/references/tonari-no-akari/identity-side-view.webp",
                    usage["side_view_identity"]["path"],
                )
                self.assertEqual(
                    "source/originals/v1_1_front_1.webp",
                    usage["leg_quality_reference"]["path"],
                )
                self.assertIn("mandatory", usage["leg_quality_reference"]["instruction"].lower())
                self.assertIn("leg", usage["leg_quality_reference"]["instruction"].lower())

    def test_prompts_lock_identity_references_leg_quality_and_background_restraint(self):
        requests = load_json(MANIFEST)["requests"]

        for request in requests:
            with self.subTest(slot=request["slot"]):
                prompt = request["prompt"].lower()
                acceptance = request["acceptance"].lower()
                combined = f"{prompt} {acceptance}"

                self.assertIn(request["japanese_title"].lower(), prompt)
                self.assertIn(request["outfit_notes"].lower(), prompt)
                self.assertIn(request["charm_notes"].lower(), prompt)
                self.assertIn(request["leg_quality_notes"].lower(), prompt)
                self.assertIn("quiet seasonal background", combined)
                self.assertIn("person, outfit, and legs stay primary", combined)
                self.assertIn("natural outfit-appropriate skin visibility", combined)

                for phrase in IDENTITY_LOCK_PHRASES:
                    self.assertIn(phrase, prompt)
                for phrase in REFERENCE_PHRASES:
                    self.assertIn(phrase, prompt)
                for phrase in LEG_QUALITY_PHRASES:
                    self.assertIn(phrase, combined)
                for phrase in IMAGE_TEXT_BANS:
                    self.assertIn(phrase, combined)
                for fragment in BANNED_PROMPT_FRAGMENTS:
                    self.assertNotIn(fragment, prompt)
                for fragment in OVERBROAD_NEGATIVE_FRAGMENTS:
                    self.assertNotIn(fragment, prompt)

    def test_risk_profile_and_review_plan_are_explicit(self):
        requests = load_json(MANIFEST)["requests"]

        for request in requests:
            with self.subTest(slot=request["slot"]):
                risk_profile = request["risk_profile"]
                self.assertEqual("high", risk_profile["identity_risk"])
                self.assertEqual("high", risk_profile["reference_drift_risk"])
                self.assertIn(risk_profile["leg_quality_risk"], {"medium", "high"})
                self.assertIn(risk_profile["outfit_drift_risk"], {"medium", "high"})
                self.assertIn(risk_profile["background_distraction_risk"], {"low", "medium"})
                self.assertEqual("medium", risk_profile["text_logo_watermark_risk"])

                review_plan = request["review_plan"]
                self.assertEqual("draft_candidate", review_plan["initial_status"])
                self.assertIn("reference images", review_plan["generation_gate"])
                self.assertIn("contact sheet", review_plan["first_pass"])
                self.assertIn("Leg Quality Gate", review_plan["leg_quality_gate"])
                self.assertIn("accept", review_plan["outcomes"])
                self.assertIn("hold", review_plan["outcomes"])
                self.assertIn("reject", review_plan["outcomes"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_coordinate_cute_healthy_seasonal_contract
```

Expected: FAIL with an assertion containing
`missing manifest: /path/to/akari-design/source/manifests/tonari-no-coordinate/cute-healthy-seasonal-outing-requests.json`.

- [ ] **Step 3: Commit the failing test**

```bash
git add tests/test_tonari_no_coordinate_cute_healthy_seasonal_contract.py
git commit -m "test: add cute healthy seasonal contract"
```

## Task 2: Add The Reference-Backed Seasonal Request Manifest

**Files:**

- Create:
  `source/manifests/tonari-no-coordinate/cute-healthy-seasonal-outing-requests.json`

- [ ] **Step 1: Create the manifest**

Create
`source/manifests/tonari-no-coordinate/cute-healthy-seasonal-outing-requests.json`:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.1-tonari-no-coordinate-cute-healthy-seasonal-outing",
  "title": "となりのコーデ cute healthy seasonal outing",
  "reference_pack_version": "tonari-no-akari-identity-plus-v1-1-leg-reference-v1",
  "prompt_template_version": "tonari_coordinate_cute_healthy_seasonal_reference_v1",
  "batch_policy": {
    "candidate_count": 8,
    "seasonal_balance": {
      "spring": 2,
      "summer": 2,
      "autumn": 2,
      "winter": 2
    },
    "composition": "knee_up_default",
    "outfit_distribution": {
      "skirt_dress_jumper_skirt": 6,
      "shorts_culotte": 2
    },
    "background_policy": "quiet_seasonal_support_only",
    "reference_policy": "image_references_required_no_prompt_only_generation",
    "pdf_policy": "not_in_this_phase"
  },
  "requests": [
    {
      "id": "request:tonari-coordinate-cute-healthy-seasonal-spring-light-cardigan-flare-dress",
      "coordinate_order": 1,
      "slot": "spring-light-cardigan-flare-dress",
      "japanese_title": "春の薄カーデワンピ",
      "season": "spring",
      "scene": "spring_street",
      "outfit_family": "skirt_dress_jumper_skirt",
      "outfit_notes": "Cream light cardigan over a pale mint flare dress with a softly moving knee-up hem.",
      "charm_notes": "Soft spring outing baseline, adult-cute and relaxed, with a little warm private-clothes charm.",
      "leg_quality_notes": "Show soft thigh volume, natural knee shape, calf transition, and a healthy leg line inspired by the v1_1_front_1 reference.",
      "composition": "knee_up",
      "tone": "fresh",
      "risk_note": "Avoid making the dress too plain or hiding the leg line.",
      "target_path": "source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_spring-light-cardigan-flare-dress_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp",
        "source/originals/v1_1_front_1.webp"
      ],
      "reference_usage": {
        "face_hair_identity": {
          "path": "source/references/tonari-no-akari/identity-face-hair.webp",
          "instruction": "Mandatory face, hair, eye, and hair ornament identity reference."
        },
        "body_balance": {
          "path": "source/references/tonari-no-akari/identity-body-base.webp",
          "instruction": "Mandatory body balance and adult petite proportion reference."
        },
        "default_outfit_context": {
          "path": "source/references/tonari-no-akari/identity-basic-outfit.webp",
          "instruction": "Mandatory baseline clothing-volume context; do not copy the outfit directly."
        },
        "side_view_identity": {
          "path": "source/references/tonari-no-akari/identity-side-view.webp",
          "instruction": "Mandatory side silhouette and hair-volume reference."
        },
        "leg_quality_reference": {
          "path": "source/originals/v1_1_front_1.webp",
          "instruction": "Mandatory leg-quality reference for soft thigh volume, natural knees, calf transition, and healthy leg line."
        }
      },
      "prompt": "Create one A4 portrait draft for Tonari no Coordinate: 春の薄カーデワンピ. Use the attached reference images as mandatory visual anchors; do not generate from prompt text alone. Reference roles: identity-face-hair, identity-body-base, identity-basic-outfit, identity-side-view, and v1_1_front_1 leg-quality reference. Akari identity lock: adult 25-year-old Japanese woman, Akari identity, short warm-brown bob, warm amber eyes, pale blue hair ornament on character-left side, cute adult private outing clothes. Outfit: Cream light cardigan over a pale mint flare dress with a softly moving knee-up hem. Charm: Soft spring outing baseline, adult-cute and relaxed, with a little warm private-clothes charm. Leg quality: Show soft thigh volume, natural knee shape, calf transition, and a healthy leg line inspired by the v1_1_front_1 reference. Composition: knee-up portrait; the person, outfit, and legs stay primary. Background: quiet seasonal background with light spring air only, no detailed storefront focus. Natural outfit-appropriate skin visibility is allowed. No readable image text, no logos, no watermarks, no frame, no panel layout.",
      "acceptance": "Coordinate Gate: must preserve Akari identity, adult age impression, face/hair/hairpin consistency, and reference-image continuity. Leg Quality Gate: soft thigh volume, natural knee shape, believable calf transition, and healthy leg line must remain attractive and coherent. Outfit Gate: cream cardigan and pale mint flare dress must read clearly as cute spring outing clothes. Background must stay quiet seasonal support only so the person, outfit, and legs stay primary. Reject for missing reference influence, prompt-only drift, school styling, explicit sexual framing, broken anatomy, readable text, logos, watermarks, frame, or panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "reference_drift_risk": "high",
        "leg_quality_risk": "medium",
        "outfit_drift_risk": "medium",
        "background_distraction_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "generation_gate": "Generate only with the listed reference images attached; do not use prompt-only generation.",
        "first_pass": "Place in the eight-image cute healthy seasonal outing contact sheet before finishing.",
        "leg_quality_gate": "Run the Leg Quality Gate against v1_1_front_1 softness and continuity.",
        "outcomes": "accept, hold, or reject"
      }
    },
    {
      "id": "request:tonari-coordinate-cute-healthy-seasonal-spring-denim-short-jacket-skirt",
      "coordinate_order": 2,
      "slot": "spring-denim-short-jacket-skirt",
      "japanese_title": "春のデニム短ジャケット",
      "season": "spring",
      "scene": "spring_walk",
      "outfit_family": "skirt_dress_jumper_skirt",
      "outfit_notes": "Short soft denim jacket over an ivory top and a light A-line skirt.",
      "charm_notes": "Casual spring outing with a little structure, more cute private clothes than streetwear.",
      "leg_quality_notes": "Keep thighs softly dimensional under the skirt hem, with natural knees and a coherent calf line.",
      "composition": "knee_up",
      "tone": "everyday_cute",
      "risk_note": "Avoid drifting into youth-casual streetwear.",
      "target_path": "source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_spring-denim-short-jacket-skirt_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp",
        "source/originals/v1_1_front_1.webp"
      ],
      "reference_usage": {
        "face_hair_identity": {
          "path": "source/references/tonari-no-akari/identity-face-hair.webp",
          "instruction": "Mandatory face, hair, eye, and hair ornament identity reference."
        },
        "body_balance": {
          "path": "source/references/tonari-no-akari/identity-body-base.webp",
          "instruction": "Mandatory body balance and adult petite proportion reference."
        },
        "default_outfit_context": {
          "path": "source/references/tonari-no-akari/identity-basic-outfit.webp",
          "instruction": "Mandatory baseline clothing-volume context; do not copy the outfit directly."
        },
        "side_view_identity": {
          "path": "source/references/tonari-no-akari/identity-side-view.webp",
          "instruction": "Mandatory side silhouette and hair-volume reference."
        },
        "leg_quality_reference": {
          "path": "source/originals/v1_1_front_1.webp",
          "instruction": "Mandatory leg-quality reference for soft thigh volume, natural knees, calf transition, and healthy leg line."
        }
      },
      "prompt": "Create one A4 portrait draft for Tonari no Coordinate: 春のデニム短ジャケット. Use the attached reference images as mandatory visual anchors; do not generate from prompt text alone. Reference roles: identity-face-hair, identity-body-base, identity-basic-outfit, identity-side-view, and v1_1_front_1 leg-quality reference. Akari identity lock: adult 25-year-old Japanese woman, Akari identity, short warm-brown bob, warm amber eyes, pale blue hair ornament on character-left side, cute adult private outing clothes. Outfit: Short soft denim jacket over an ivory top and a light A-line skirt. Charm: Casual spring outing with a little structure, more cute private clothes than streetwear. Leg quality: Keep thighs softly dimensional under the skirt hem, with natural knees and a coherent calf line. Composition: knee-up portrait; the person, outfit, and legs stay primary. Background: quiet seasonal background with spring walk atmosphere only. Natural outfit-appropriate skin visibility is allowed. No readable image text, no logos, no watermarks, no frame, no panel layout.",
      "acceptance": "Coordinate Gate: must preserve Akari identity, adult age impression, face/hair/hairpin consistency, and reference-image continuity. Leg Quality Gate: thighs must keep soft volume and connect naturally through knees and calves. Outfit Gate: denim jacket, ivory top, and A-line skirt must read as cute spring outing clothes rather than streetwear. Background must stay quiet seasonal support only so the person, outfit, and legs stay primary. Reject for missing reference influence, prompt-only drift, school styling, explicit sexual framing, broken anatomy, readable text, logos, watermarks, frame, or panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "reference_drift_risk": "high",
        "leg_quality_risk": "medium",
        "outfit_drift_risk": "medium",
        "background_distraction_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "generation_gate": "Generate only with the listed reference images attached; do not use prompt-only generation.",
        "first_pass": "Place in the eight-image cute healthy seasonal outing contact sheet before finishing.",
        "leg_quality_gate": "Run the Leg Quality Gate against v1_1_front_1 softness and continuity.",
        "outcomes": "accept, hold, or reject"
      }
    },
    {
      "id": "request:tonari-coordinate-cute-healthy-seasonal-summer-puff-sleeve-blouse-skirt",
      "coordinate_order": 3,
      "slot": "summer-puff-sleeve-blouse-skirt",
      "japanese_title": "夏のパフ袖ブラウス",
      "season": "summer",
      "scene": "summer_daylight",
      "outfit_family": "skirt_dress_jumper_skirt",
      "outfit_notes": "Light puff-sleeve blouse with a pale mint trapeze skirt.",
      "charm_notes": "Clear summer clothing signal, airy and cute without leaning on scenery.",
      "leg_quality_notes": "Keep the visible legs softly sunlit, with thigh-knee-calf continuity and no mannequin stiffness.",
      "composition": "knee_up",
      "tone": "fresh",
      "risk_note": "Keep fabric light but not awkwardly transparent.",
      "target_path": "source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_summer-puff-sleeve-blouse-skirt_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp",
        "source/originals/v1_1_front_1.webp"
      ],
      "reference_usage": {
        "face_hair_identity": {
          "path": "source/references/tonari-no-akari/identity-face-hair.webp",
          "instruction": "Mandatory face, hair, eye, and hair ornament identity reference."
        },
        "body_balance": {
          "path": "source/references/tonari-no-akari/identity-body-base.webp",
          "instruction": "Mandatory body balance and adult petite proportion reference."
        },
        "default_outfit_context": {
          "path": "source/references/tonari-no-akari/identity-basic-outfit.webp",
          "instruction": "Mandatory baseline clothing-volume context; do not copy the outfit directly."
        },
        "side_view_identity": {
          "path": "source/references/tonari-no-akari/identity-side-view.webp",
          "instruction": "Mandatory side silhouette and hair-volume reference."
        },
        "leg_quality_reference": {
          "path": "source/originals/v1_1_front_1.webp",
          "instruction": "Mandatory leg-quality reference for soft thigh volume, natural knees, calf transition, and healthy leg line."
        }
      },
      "prompt": "Create one A4 portrait draft for Tonari no Coordinate: 夏のパフ袖ブラウス. Use the attached reference images as mandatory visual anchors; do not generate from prompt text alone. Reference roles: identity-face-hair, identity-body-base, identity-basic-outfit, identity-side-view, and v1_1_front_1 leg-quality reference. Akari identity lock: adult 25-year-old Japanese woman, Akari identity, short warm-brown bob, warm amber eyes, pale blue hair ornament on character-left side, cute adult private outing clothes. Outfit: Light puff-sleeve blouse with a pale mint trapeze skirt. Charm: Clear summer clothing signal, airy and cute without leaning on scenery. Leg quality: Keep the visible legs softly sunlit, with thigh-knee-calf continuity and no mannequin stiffness. Composition: knee-up portrait; the person, outfit, and legs stay primary. Background: quiet seasonal background with summer daylight only. Natural outfit-appropriate skin visibility is allowed. No readable image text, no logos, no watermarks, no frame, no panel layout.",
      "acceptance": "Coordinate Gate: must preserve Akari identity, adult age impression, face/hair/hairpin consistency, and reference-image continuity. Leg Quality Gate: visible legs must preserve soft thigh volume, natural knee shape, calf transition, and healthy leg line. Outfit Gate: puff-sleeve blouse and pale mint trapeze skirt must read as summer private outing clothes. Background must stay quiet seasonal support only so the person, outfit, and legs stay primary. Reject for missing reference influence, prompt-only drift, awkward transparency, explicit sexual framing, broken anatomy, readable text, logos, watermarks, frame, or panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "reference_drift_risk": "high",
        "leg_quality_risk": "medium",
        "outfit_drift_risk": "medium",
        "background_distraction_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "generation_gate": "Generate only with the listed reference images attached; do not use prompt-only generation.",
        "first_pass": "Place in the eight-image cute healthy seasonal outing contact sheet before finishing.",
        "leg_quality_gate": "Run the Leg Quality Gate against v1_1_front_1 softness and continuity.",
        "outcomes": "accept, hold, or reject"
      }
    },
    {
      "id": "request:tonari-coordinate-cute-healthy-seasonal-summer-collar-blouse-culotte",
      "coordinate_order": 4,
      "slot": "summer-collar-blouse-culotte",
      "japanese_title": "夏襟ブラウスとキュロット",
      "season": "summer",
      "scene": "summer_outing",
      "outfit_family": "shorts_culotte",
      "outfit_notes": "Rounded-collar summer blouse with soft culottes.",
      "charm_notes": "One of the two culotte checks, fresh and playful while staying adult.",
      "leg_quality_notes": "Culotte hem should reveal soft thigh volume and natural knees without flattening the legs.",
      "composition": "knee_up",
      "tone": "fresh",
      "risk_note": "Avoid school-uniform cues.",
      "target_path": "source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_summer-collar-blouse-culotte_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp",
        "source/originals/v1_1_front_1.webp"
      ],
      "reference_usage": {
        "face_hair_identity": {
          "path": "source/references/tonari-no-akari/identity-face-hair.webp",
          "instruction": "Mandatory face, hair, eye, and hair ornament identity reference."
        },
        "body_balance": {
          "path": "source/references/tonari-no-akari/identity-body-base.webp",
          "instruction": "Mandatory body balance and adult petite proportion reference."
        },
        "default_outfit_context": {
          "path": "source/references/tonari-no-akari/identity-basic-outfit.webp",
          "instruction": "Mandatory baseline clothing-volume context; do not copy the outfit directly."
        },
        "side_view_identity": {
          "path": "source/references/tonari-no-akari/identity-side-view.webp",
          "instruction": "Mandatory side silhouette and hair-volume reference."
        },
        "leg_quality_reference": {
          "path": "source/originals/v1_1_front_1.webp",
          "instruction": "Mandatory leg-quality reference for soft thigh volume, natural knees, calf transition, and healthy leg line."
        }
      },
      "prompt": "Create one A4 portrait draft for Tonari no Coordinate: 夏襟ブラウスとキュロット. Use the attached reference images as mandatory visual anchors; do not generate from prompt text alone. Reference roles: identity-face-hair, identity-body-base, identity-basic-outfit, identity-side-view, and v1_1_front_1 leg-quality reference. Akari identity lock: adult 25-year-old Japanese woman, Akari identity, short warm-brown bob, warm amber eyes, pale blue hair ornament on character-left side, cute adult private outing clothes. Outfit: Rounded-collar summer blouse with soft culottes. Charm: One of the two culotte checks, fresh and playful while staying adult. Leg quality: Culotte hem should reveal soft thigh volume and natural knees without flattening the legs. Composition: knee-up portrait; the person, outfit, and legs stay primary. Background: quiet seasonal background with summer outing air only. Natural outfit-appropriate skin visibility is allowed. No readable image text, no logos, no watermarks, no frame, no panel layout.",
      "acceptance": "Coordinate Gate: must preserve Akari identity, adult age impression, face/hair/hairpin consistency, and reference-image continuity. Leg Quality Gate: culotte hem must keep soft thigh volume, natural knee shape, calf transition, and healthy leg line readable. Outfit Gate: rounded-collar blouse and culottes must read as adult summer outing clothes and not as a uniform. Background must stay quiet seasonal support only so the person, outfit, and legs stay primary. Reject for missing reference influence, prompt-only drift, school styling, explicit sexual framing, broken anatomy, readable text, logos, watermarks, frame, or panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "reference_drift_risk": "high",
        "leg_quality_risk": "high",
        "outfit_drift_risk": "high",
        "background_distraction_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "generation_gate": "Generate only with the listed reference images attached; do not use prompt-only generation.",
        "first_pass": "Place in the eight-image cute healthy seasonal outing contact sheet before finishing.",
        "leg_quality_gate": "Run the Leg Quality Gate against v1_1_front_1 softness and continuity.",
        "outcomes": "accept, hold, or reject"
      }
    },
    {
      "id": "request:tonari-coordinate-cute-healthy-seasonal-autumn-short-knit-check-skirt",
      "coordinate_order": 5,
      "slot": "autumn-short-knit-check-skirt",
      "japanese_title": "秋の短めニット",
      "season": "autumn",
      "scene": "autumn_walk",
      "outfit_family": "skirt_dress_jumper_skirt",
      "outfit_notes": "Short soft knit with a muted check A-line skirt.",
      "charm_notes": "Autumn color and texture while keeping the silhouette cute and easygoing.",
      "leg_quality_notes": "Skirt length should keep thigh softness and knee placement visible enough to judge.",
      "composition": "knee_up",
      "tone": "warm",
      "risk_note": "Avoid making the knit tight glamour styling.",
      "target_path": "source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_autumn-short-knit-check-skirt_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp",
        "source/originals/v1_1_front_1.webp"
      ],
      "reference_usage": {
        "face_hair_identity": {
          "path": "source/references/tonari-no-akari/identity-face-hair.webp",
          "instruction": "Mandatory face, hair, eye, and hair ornament identity reference."
        },
        "body_balance": {
          "path": "source/references/tonari-no-akari/identity-body-base.webp",
          "instruction": "Mandatory body balance and adult petite proportion reference."
        },
        "default_outfit_context": {
          "path": "source/references/tonari-no-akari/identity-basic-outfit.webp",
          "instruction": "Mandatory baseline clothing-volume context; do not copy the outfit directly."
        },
        "side_view_identity": {
          "path": "source/references/tonari-no-akari/identity-side-view.webp",
          "instruction": "Mandatory side silhouette and hair-volume reference."
        },
        "leg_quality_reference": {
          "path": "source/originals/v1_1_front_1.webp",
          "instruction": "Mandatory leg-quality reference for soft thigh volume, natural knees, calf transition, and healthy leg line."
        }
      },
      "prompt": "Create one A4 portrait draft for Tonari no Coordinate: 秋の短めニット. Use the attached reference images as mandatory visual anchors; do not generate from prompt text alone. Reference roles: identity-face-hair, identity-body-base, identity-basic-outfit, identity-side-view, and v1_1_front_1 leg-quality reference. Akari identity lock: adult 25-year-old Japanese woman, Akari identity, short warm-brown bob, warm amber eyes, pale blue hair ornament on character-left side, cute adult private outing clothes. Outfit: Short soft knit with a muted check A-line skirt. Charm: Autumn color and texture while keeping the silhouette cute and easygoing. Leg quality: Skirt length should keep thigh softness and knee placement visible enough to judge. Composition: knee-up portrait; the person, outfit, and legs stay primary. Background: quiet seasonal background with autumn walk atmosphere only. Natural outfit-appropriate skin visibility is allowed. No readable image text, no logos, no watermarks, no frame, no panel layout.",
      "acceptance": "Coordinate Gate: must preserve Akari identity, adult age impression, face/hair/hairpin consistency, and reference-image continuity. Leg Quality Gate: skirt hem must leave thigh volume, natural knee shape, calf transition, and healthy leg line readable. Outfit Gate: short knit and muted check skirt must read as autumn private outing clothes, not tight glamour styling. Background must stay quiet seasonal support only so the person, outfit, and legs stay primary. Reject for missing reference influence, prompt-only drift, explicit sexual framing, broken anatomy, readable text, logos, watermarks, frame, or panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "reference_drift_risk": "high",
        "leg_quality_risk": "medium",
        "outfit_drift_risk": "medium",
        "background_distraction_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "generation_gate": "Generate only with the listed reference images attached; do not use prompt-only generation.",
        "first_pass": "Place in the eight-image cute healthy seasonal outing contact sheet before finishing.",
        "leg_quality_gate": "Run the Leg Quality Gate against v1_1_front_1 softness and continuity.",
        "outcomes": "accept, hold, or reject"
      }
    },
    {
      "id": "request:tonari-coordinate-cute-healthy-seasonal-autumn-jumper-skirt-thin-turtleneck",
      "coordinate_order": 6,
      "slot": "autumn-jumper-skirt-thin-turtleneck",
      "japanese_title": "秋のジャンスカ",
      "season": "autumn",
      "scene": "autumn_cafe_walk",
      "outfit_family": "skirt_dress_jumper_skirt",
      "outfit_notes": "Brown jumper skirt over a thin soft turtleneck.",
      "charm_notes": "Adult cute autumn jumper-skirt look with a calm day-off feeling.",
      "leg_quality_notes": "Keep the jumper-skirt hem from hiding the soft thigh volume and natural knee rhythm.",
      "composition": "knee_up",
      "tone": "warm",
      "risk_note": "Avoid childlike proportions or school styling.",
      "target_path": "source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_autumn-jumper-skirt-thin-turtleneck_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp",
        "source/originals/v1_1_front_1.webp"
      ],
      "reference_usage": {
        "face_hair_identity": {
          "path": "source/references/tonari-no-akari/identity-face-hair.webp",
          "instruction": "Mandatory face, hair, eye, and hair ornament identity reference."
        },
        "body_balance": {
          "path": "source/references/tonari-no-akari/identity-body-base.webp",
          "instruction": "Mandatory body balance and adult petite proportion reference."
        },
        "default_outfit_context": {
          "path": "source/references/tonari-no-akari/identity-basic-outfit.webp",
          "instruction": "Mandatory baseline clothing-volume context; do not copy the outfit directly."
        },
        "side_view_identity": {
          "path": "source/references/tonari-no-akari/identity-side-view.webp",
          "instruction": "Mandatory side silhouette and hair-volume reference."
        },
        "leg_quality_reference": {
          "path": "source/originals/v1_1_front_1.webp",
          "instruction": "Mandatory leg-quality reference for soft thigh volume, natural knees, calf transition, and healthy leg line."
        }
      },
      "prompt": "Create one A4 portrait draft for Tonari no Coordinate: 秋のジャンスカ. Use the attached reference images as mandatory visual anchors; do not generate from prompt text alone. Reference roles: identity-face-hair, identity-body-base, identity-basic-outfit, identity-side-view, and v1_1_front_1 leg-quality reference. Akari identity lock: adult 25-year-old Japanese woman, Akari identity, short warm-brown bob, warm amber eyes, pale blue hair ornament on character-left side, cute adult private outing clothes. Outfit: Brown jumper skirt over a thin soft turtleneck. Charm: Adult cute autumn jumper-skirt look with a calm day-off feeling. Leg quality: Keep the jumper-skirt hem from hiding the soft thigh volume and natural knee rhythm. Composition: knee-up portrait; the person, outfit, and legs stay primary. Background: quiet seasonal background with autumn cafe-walk atmosphere only. Natural outfit-appropriate skin visibility is allowed. No readable image text, no logos, no watermarks, no frame, no panel layout.",
      "acceptance": "Coordinate Gate: must preserve Akari identity, adult age impression, face/hair/hairpin consistency, and reference-image continuity. Leg Quality Gate: jumper-skirt length must preserve soft thigh volume, natural knee shape, calf transition, and healthy leg line readability. Outfit Gate: jumper skirt and thin turtleneck must read as adult cute autumn clothes, not childlike or school styling. Background must stay quiet seasonal support only so the person, outfit, and legs stay primary. Reject for missing reference influence, prompt-only drift, school styling, childlike proportions, explicit sexual framing, broken anatomy, readable text, logos, watermarks, frame, or panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "reference_drift_risk": "high",
        "leg_quality_risk": "medium",
        "outfit_drift_risk": "high",
        "background_distraction_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "generation_gate": "Generate only with the listed reference images attached; do not use prompt-only generation.",
        "first_pass": "Place in the eight-image cute healthy seasonal outing contact sheet before finishing.",
        "leg_quality_gate": "Run the Leg Quality Gate against v1_1_front_1 softness and continuity.",
        "outcomes": "accept, hold, or reject"
      }
    },
    {
      "id": "request:tonari-coordinate-cute-healthy-seasonal-winter-knit-onepiece-short-coat",
      "coordinate_order": 7,
      "slot": "winter-knit-onepiece-short-coat",
      "japanese_title": "冬のニットワンピ",
      "season": "winter",
      "scene": "winter_street",
      "outfit_family": "skirt_dress_jumper_skirt",
      "outfit_notes": "Soft knit one-piece with a short winter coat.",
      "charm_notes": "Winter warmth without hiding the legs completely, adult cute and softly dressed.",
      "leg_quality_notes": "Visible legs should keep soft volume and natural knee-to-calf continuity despite winter styling.",
      "composition": "knee_up",
      "tone": "warm",
      "risk_note": "Avoid bodycon styling and avoid long-coat leg concealment.",
      "target_path": "source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_winter-knit-onepiece-short-coat_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp",
        "source/originals/v1_1_front_1.webp"
      ],
      "reference_usage": {
        "face_hair_identity": {
          "path": "source/references/tonari-no-akari/identity-face-hair.webp",
          "instruction": "Mandatory face, hair, eye, and hair ornament identity reference."
        },
        "body_balance": {
          "path": "source/references/tonari-no-akari/identity-body-base.webp",
          "instruction": "Mandatory body balance and adult petite proportion reference."
        },
        "default_outfit_context": {
          "path": "source/references/tonari-no-akari/identity-basic-outfit.webp",
          "instruction": "Mandatory baseline clothing-volume context; do not copy the outfit directly."
        },
        "side_view_identity": {
          "path": "source/references/tonari-no-akari/identity-side-view.webp",
          "instruction": "Mandatory side silhouette and hair-volume reference."
        },
        "leg_quality_reference": {
          "path": "source/originals/v1_1_front_1.webp",
          "instruction": "Mandatory leg-quality reference for soft thigh volume, natural knees, calf transition, and healthy leg line."
        }
      },
      "prompt": "Create one A4 portrait draft for Tonari no Coordinate: 冬のニットワンピ. Use the attached reference images as mandatory visual anchors; do not generate from prompt text alone. Reference roles: identity-face-hair, identity-body-base, identity-basic-outfit, identity-side-view, and v1_1_front_1 leg-quality reference. Akari identity lock: adult 25-year-old Japanese woman, Akari identity, short warm-brown bob, warm amber eyes, pale blue hair ornament on character-left side, cute adult private outing clothes. Outfit: Soft knit one-piece with a short winter coat. Charm: Winter warmth without hiding the legs completely, adult cute and softly dressed. Leg quality: Visible legs should keep soft volume and natural knee-to-calf continuity despite winter styling. Composition: knee-up portrait; the person, outfit, and legs stay primary. Background: quiet seasonal background with winter street air only. Natural outfit-appropriate skin visibility is allowed. No readable image text, no logos, no watermarks, no frame, no panel layout.",
      "acceptance": "Coordinate Gate: must preserve Akari identity, adult age impression, face/hair/hairpin consistency, and reference-image continuity. Leg Quality Gate: visible legs must keep soft thigh volume, natural knee shape, calf transition, and healthy leg line despite winter clothing. Outfit Gate: knit one-piece and short winter coat must read as winter outing clothes without bodycon styling or long-coat concealment. Background must stay quiet seasonal support only so the person, outfit, and legs stay primary. Reject for missing reference influence, prompt-only drift, explicit sexual framing, broken anatomy, readable text, logos, watermarks, frame, or panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "reference_drift_risk": "high",
        "leg_quality_risk": "high",
        "outfit_drift_risk": "medium",
        "background_distraction_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "generation_gate": "Generate only with the listed reference images attached; do not use prompt-only generation.",
        "first_pass": "Place in the eight-image cute healthy seasonal outing contact sheet before finishing.",
        "leg_quality_gate": "Run the Leg Quality Gate against v1_1_front_1 softness and continuity.",
        "outcomes": "accept, hold, or reject"
      }
    },
    {
      "id": "request:tonari-coordinate-cute-healthy-seasonal-winter-short-duffle-culotte",
      "coordinate_order": 8,
      "slot": "winter-short-duffle-culotte",
      "japanese_title": "冬の短めダッフル",
      "season": "winter",
      "scene": "winter_walk",
      "outfit_family": "shorts_culotte",
      "outfit_notes": "Adult-cute short duffle or cape-like coat with warm culottes.",
      "charm_notes": "Second culotte check, winter version, cute but not school-coat coded.",
      "leg_quality_notes": "Winter culotte styling should still reveal coherent thighs, knees, calves, and healthy leg line.",
      "composition": "knee_up",
      "tone": "warm",
      "risk_note": "Avoid school-coat impression.",
      "target_path": "source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_winter-short-duffle-culotte_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp",
        "source/originals/v1_1_front_1.webp"
      ],
      "reference_usage": {
        "face_hair_identity": {
          "path": "source/references/tonari-no-akari/identity-face-hair.webp",
          "instruction": "Mandatory face, hair, eye, and hair ornament identity reference."
        },
        "body_balance": {
          "path": "source/references/tonari-no-akari/identity-body-base.webp",
          "instruction": "Mandatory body balance and adult petite proportion reference."
        },
        "default_outfit_context": {
          "path": "source/references/tonari-no-akari/identity-basic-outfit.webp",
          "instruction": "Mandatory baseline clothing-volume context; do not copy the outfit directly."
        },
        "side_view_identity": {
          "path": "source/references/tonari-no-akari/identity-side-view.webp",
          "instruction": "Mandatory side silhouette and hair-volume reference."
        },
        "leg_quality_reference": {
          "path": "source/originals/v1_1_front_1.webp",
          "instruction": "Mandatory leg-quality reference for soft thigh volume, natural knees, calf transition, and healthy leg line."
        }
      },
      "prompt": "Create one A4 portrait draft for Tonari no Coordinate: 冬の短めダッフル. Use the attached reference images as mandatory visual anchors; do not generate from prompt text alone. Reference roles: identity-face-hair, identity-body-base, identity-basic-outfit, identity-side-view, and v1_1_front_1 leg-quality reference. Akari identity lock: adult 25-year-old Japanese woman, Akari identity, short warm-brown bob, warm amber eyes, pale blue hair ornament on character-left side, cute adult private outing clothes. Outfit: Adult-cute short duffle or cape-like coat with warm culottes. Charm: Second culotte check, winter version, cute but not school-coat coded. Leg quality: Winter culotte styling should still reveal coherent thighs, knees, calves, and healthy leg line. Composition: knee-up portrait; the person, outfit, and legs stay primary. Background: quiet seasonal background with winter walk air only. Natural outfit-appropriate skin visibility is allowed. No readable image text, no logos, no watermarks, no frame, no panel layout.",
      "acceptance": "Coordinate Gate: must preserve Akari identity, adult age impression, face/hair/hairpin consistency, and reference-image continuity. Leg Quality Gate: culotte styling must preserve soft thigh volume, natural knee shape, calf transition, and healthy leg line. Outfit Gate: short duffle or cape-like coat and culottes must read as adult cute winter outing clothes, not school-coat styling. Background must stay quiet seasonal support only so the person, outfit, and legs stay primary. Reject for missing reference influence, prompt-only drift, school styling, explicit sexual framing, broken anatomy, readable text, logos, watermarks, frame, or panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "reference_drift_risk": "high",
        "leg_quality_risk": "high",
        "outfit_drift_risk": "high",
        "background_distraction_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "generation_gate": "Generate only with the listed reference images attached; do not use prompt-only generation.",
        "first_pass": "Place in the eight-image cute healthy seasonal outing contact sheet before finishing.",
        "leg_quality_gate": "Run the Leg Quality Gate against v1_1_front_1 softness and continuity.",
        "outcomes": "accept, hold, or reject"
      }
    }
  ]
}
```

- [ ] **Step 2: Run the contract test**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_coordinate_cute_healthy_seasonal_contract
```

Expected: PASS.

- [ ] **Step 3: Confirm generated paths remain ignored**

Run:

```bash
git check-ignore source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_spring-light-cardigan-flare-dress_v1.webp
git check-ignore evidence/tonari-no-coordinate/contact-sheets/cute-healthy-seasonal-outing-first-pass.webp
```

Expected: both commands print the checked path and exit 0.

- [ ] **Step 4: Commit the manifest**

```bash
git add source/manifests/tonari-no-coordinate/cute-healthy-seasonal-outing-requests.json
git commit -m "feat: add cute healthy seasonal requests"
```

## Task 3: Add Contact-Sheet Coverage For The New Manifest

**Files:**

- Modify: `tests/test_tonari_no_coordinate_contact_sheet.py`

- [ ] **Step 1: Add a label-fitting test for the seasonal manifest**

Add this method to `TonariNoCoordinateContactSheetTest` in
`tests/test_tonari_no_coordinate_contact_sheet.py`, immediately after
`test_real_contact_sheet_labels_fit_default_card_width`:

```python
    def test_real_cute_healthy_seasonal_labels_fit_default_card_width(self):
        requests_path = (
            ROOT
            / "source/manifests/tonari-no-coordinate/cute-healthy-seasonal-outing-requests.json"
        )
        with requests_path.open(encoding="utf-8") as requests_file:
            requests = json.load(requests_file)["requests"]
        font = load_font(16)
        small_font = load_font(13)
        max_width = 264

        for request in requests:
            with self.subTest(slot=request["slot"]):
                title_line, detail_line = label_lines_for(request, font, small_font, max_width)

                self.assertLessEqual(text_width(title_line, font), max_width)
                self.assertLessEqual(text_width(detail_line, small_font), max_width)
```

- [ ] **Step 2: Run the contact-sheet tests**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_coordinate_contact_sheet
```

Expected: PASS.

- [ ] **Step 3: Run the seasonal contract test again**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_coordinate_cute_healthy_seasonal_contract
```

Expected: PASS.

- [ ] **Step 4: Commit the contact-sheet test**

```bash
git add tests/test_tonari_no_coordinate_contact_sheet.py
git commit -m "test: cover seasonal coordinate contact labels"
```

## Task 4: Run Full Python Verification

**Files:**

- No file changes.

- [ ] **Step 1: Run all Python tests**

Run:

```bash
npm run test:python
```

Expected: PASS.

- [ ] **Step 2: Confirm the working tree only has intended changes**

Run:

```bash
git status --short
```

Expected: clean, unless generated working artifacts have already been created.

## Task 5: Generate Working Candidates With Reference Images

**Files:**

- Create working-only images under:
  `source/generated/tonari-no-coordinate/`
- Create working-only contact sheet under:
  `evidence/tonari-no-coordinate/contact-sheets/`

- [ ] **Step 1: Confirm the generation route supports attached references**

Before generating any image, confirm the tool or workflow can attach the five
paths in `reference_pack_inputs` for each request:

```text
source/references/tonari-no-akari/identity-face-hair.webp
source/references/tonari-no-akari/identity-body-base.webp
source/references/tonari-no-akari/identity-basic-outfit.webp
source/references/tonari-no-akari/identity-side-view.webp
source/originals/v1_1_front_1.webp
```

Expected: a reference-capable route is available. If not, stop here and report:
`Blocked: this generation route cannot attach the required Akari reference images, so prompt-only generation was not run.`

- [ ] **Step 2: Generate each request with its attached reference pack**

For each request in
`source/manifests/tonari-no-coordinate/cute-healthy-seasonal-outing-requests.json`:

1. Attach all five files in `reference_pack_inputs`.
2. Use `reference_usage` role labels if the tool supports role labels.
3. Use the request's `prompt` exactly.
4. Save the generated image to the request's `target_path`.
5. Do not commit generated images.

Expected generated paths:

```text
source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_spring-light-cardigan-flare-dress_v1.webp
source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_spring-denim-short-jacket-skirt_v1.webp
source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_summer-puff-sleeve-blouse-skirt_v1.webp
source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_summer-collar-blouse-culotte_v1.webp
source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_autumn-short-knit-check-skirt_v1.webp
source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_autumn-jumper-skirt-thin-turtleneck_v1.webp
source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_winter-knit-onepiece-short-coat_v1.webp
source/generated/tonari-no-coordinate/20260708_cute-healthy-seasonal_winter-short-duffle-culotte_v1.webp
```

- [ ] **Step 3: Verify all generated files exist and are readable**

Run:

```bash
uv run python - <<'PY'
import json
from pathlib import Path
from PIL import Image

root = Path.cwd()
manifest = root / "source/manifests/tonari-no-coordinate/cute-healthy-seasonal-outing-requests.json"
requests = json.loads(manifest.read_text(encoding="utf-8"))["requests"]
missing = []
for request in requests:
    path = root / request["target_path"]
    if not path.is_file():
        missing.append(request["target_path"])
        continue
    with Image.open(path) as image:
        print(f"{request['slot']}: {image.width}x{image.height} {image.mode}")
if missing:
    raise SystemExit("missing generated files: " + ", ".join(missing))
PY
```

Expected: eight lines of image metadata and no `missing generated files` error.

- [ ] **Step 4: Build the first-pass contact sheet**

Run:

```bash
npm run build:coordinate:contact-sheet -- \
  --requests source/manifests/tonari-no-coordinate/cute-healthy-seasonal-outing-requests.json \
  --output evidence/tonari-no-coordinate/contact-sheets/cute-healthy-seasonal-outing-first-pass.webp
```

Expected:
`Wrote evidence/tonari-no-coordinate/contact-sheets/cute-healthy-seasonal-outing-first-pass.webp`.

- [ ] **Step 5: Confirm generated artifacts remain ignored**

Run:

```bash
git status --short --ignored source/generated/tonari-no-coordinate evidence/tonari-no-coordinate
```

Expected: generated images and contact sheet appear as ignored files with `!!`
prefixes. They should not appear as staged or tracked files.

## Task 6: Final Verification And Handoff

**Files:**

- No required file changes.

- [ ] **Step 1: Run targeted tests**

Run:

```bash
uv run python -m unittest \
  tests.test_tonari_no_coordinate_cute_healthy_seasonal_contract \
  tests.test_tonari_no_coordinate_contact_sheet
```

Expected: PASS.

- [ ] **Step 2: Run all Python tests**

Run:

```bash
npm run test:python
```

Expected: PASS.

- [ ] **Step 3: Check final git status**

Run:

```bash
git status --short
```

Expected: clean for tracked files. Ignored generated images may exist under
`source/generated/tonari-no-coordinate/` and `evidence/tonari-no-coordinate/`.

- [ ] **Step 4: Report the generation status**

If images were generated, report:

```text
Generated 8 reference-backed cute healthy seasonal outing candidates.
Contact sheet: evidence/tonari-no-coordinate/contact-sheets/cute-healthy-seasonal-outing-first-pass.webp
Tracked changes: tests and request manifest only.
Generated images remain ignored working artifacts.
```

If image generation was blocked because references could not be attached,
report:

```text
Request manifest and tests are complete, but image generation was not run because the available route could not attach the required Akari reference images. Prompt-only generation was intentionally skipped.
```

## Self-Review

- Spec coverage: This plan covers the eight-image batch, two-per-season
  balance, six skirt/dress/jumper-skirt and two shorts/culotte distribution,
  knee-up framing, quiet backgrounds, leg-quality gate, reference image
  requirement, prompt boundary, contact-sheet review, and ignored generated
  artifacts.
- Placeholder scan: No `TBD`, `TODO`, `implement later`, or "similar to" steps
  are used.
- Type consistency: The manifest keys in Task 2 match the contract test in
  Task 1 and the contact-sheet expectations in Task 3.
