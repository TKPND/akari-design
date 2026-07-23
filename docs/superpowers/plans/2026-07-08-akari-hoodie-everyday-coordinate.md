# Akari Hoodie Everyday Coordinate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reference-backed eight-image `hoodie_everyday` corrective
coordinate batch that returns Akari's outfits to the original hoodie image's
casual "her own clothes" feeling.

**Architecture:** Keep this as a separate request manifest under the existing
`tonari-no-coordinate` manifest directory, with a focused contract test that
prevents the previous dress-up/catalog drift from re-entering the prompt set.
Reuse the existing contact-sheet builder and keep generated WebP images plus
contact sheets as ignored working artifacts.

**Tech Stack:** Python 3.11, `unittest`, JSON manifests, Pillow contact-sheet
tooling, `uv run python`, existing npm scripts, Codex visible reference image
workflow, `image_gen`, `cwebp`.

---

## Scope Check

The approved spec covers one corrective image batch. This plan does not update
the PDF, replace the broader `となりのコーデ` design, commit generated images, or
expand beyond eight candidates. The generated first pass is review evidence
only.

Reference images are mandatory. If the active generation route cannot use the
visible in-thread reference workflow, stop after the manifest and report that
generation is blocked. Do not generate from prompt text alone.

## Current Context

- Approved design spec:
  `docs/superpowers/specs/2026-07-08-akari-hoodie-everyday-coordinate-design.md`
- Previous seasonal manifest:
  `source/manifests/tonari-no-coordinate/cute-healthy-seasonal-outing-requests.json`
- Previous seasonal contract test:
  `tests/test_tonari_no_coordinate_cute_healthy_seasonal_contract.py`
- Contact-sheet script:
  `scripts/build_tonari_no_coordinate_contact_sheet.py`
- Contact-sheet tests:
  `tests/test_tonari_no_coordinate_contact_sheet.py`
- Generated image directory, already ignored:
  `source/generated/tonari-no-coordinate/`
- Evidence directory, already ignored:
  `evidence/tonari-no-coordinate/`

## File Structure

- Create `tests/test_tonari_no_coordinate_hoodie_everyday_contract.py`
  - Contract test for top-level manifest metadata, exact candidate order,
    reference requirements, prompt identity locks, casual hoodie-family locks,
    anti-catalog boundaries, leg-quality terms, and ignored output paths.
- Create
  `source/manifests/tonari-no-coordinate/hoodie-everyday-coordinate-requests.json`
  - Static source-of-truth request manifest for the eight candidates.
- Modify `tests/test_tonari_no_coordinate_contact_sheet.py`
  - Add label-fitting coverage for the new manifest.
- Working-only generated outputs:
  - `source/generated/tonari-no-coordinate/20260708_hoodie-everyday_<slot>_v1.webp`
  - `evidence/tonari-no-coordinate/contact-sheets/hoodie-everyday-first-pass.webp`

## Candidate Data

| Order | Slot | Title | Season | Family |
| --- | --- | --- | --- | --- |
| 1 | `spring-zip-hoodie-pleated-mini` | `春のジップパーカー` | `spring` | `hoodie_sweatshirt` |
| 2 | `spring-long-tee-denim-layer-shorts` | `春のロンTデニム羽織り` | `spring` | `long_tee_outerwear` |
| 3 | `summer-oversized-tee-culotte` | `夏の大きめTシャツ` | `summer` | `long_tee_outerwear` |
| 4 | `summer-thin-hoodie-shorts` | `夏の薄手フーディ` | `summer` | `hoodie_sweatshirt` |
| 5 | `autumn-sweatshirt-check-skirt` | `秋のスウェット` | `autumn` | `hoodie_sweatshirt` |
| 6 | `autumn-coach-jacket-hoodie-mini` | `秋のコーチジャケット` | `autumn` | `casual_outerwear` |
| 7 | `winter-boa-hoodie-pleated-skirt` | `冬のボアパーカー` | `winter` | `hoodie_sweatshirt` |
| 8 | `winter-short-puffer-sweat-culotte` | `冬の短め中綿ジャケット` | `winter` | `casual_outerwear` |

## Task 1: Add The Failing Hoodie Everyday Contract Test

**Files:**

- Create:
  `tests/test_tonari_no_coordinate_hoodie_everyday_contract.py`

- [ ] **Step 1: Write the failing contract test**

Create
`tests/test_tonari_no_coordinate_hoodie_everyday_contract.py`:

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
    / "source/manifests/tonari-no-coordinate/hoodie-everyday-coordinate-requests.json"
)
COLLECTION_ID = "akari-v1.1-tonari-no-coordinate-hoodie-everyday"
TITLE = "となりのコーデ hoodie everyday"
REFERENCE_PACK_VERSION = "tonari-no-akari-identity-plus-v1-1-hoodie-leg-reference-v1"
PROMPT_TEMPLATE_VERSION = "tonari_coordinate_hoodie_everyday_reference_v1"
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
    "default_hoodie_outfit_context",
    "side_view_identity",
    "leg_quality_reference",
}
EXPECTED_CANDIDATES = [
    {
        "slot": "spring-zip-hoodie-pleated-mini",
        "title": "春のジップパーカー",
        "season": "spring",
        "outfit_family": "hoodie_sweatshirt",
    },
    {
        "slot": "spring-long-tee-denim-layer-shorts",
        "title": "春のロンTデニム羽織り",
        "season": "spring",
        "outfit_family": "long_tee_outerwear",
    },
    {
        "slot": "summer-oversized-tee-culotte",
        "title": "夏の大きめTシャツ",
        "season": "summer",
        "outfit_family": "long_tee_outerwear",
    },
    {
        "slot": "summer-thin-hoodie-shorts",
        "title": "夏の薄手フーディ",
        "season": "summer",
        "outfit_family": "hoodie_sweatshirt",
    },
    {
        "slot": "autumn-sweatshirt-check-skirt",
        "title": "秋のスウェット",
        "season": "autumn",
        "outfit_family": "hoodie_sweatshirt",
    },
    {
        "slot": "autumn-coach-jacket-hoodie-mini",
        "title": "秋のコーチジャケット",
        "season": "autumn",
        "outfit_family": "casual_outerwear",
    },
    {
        "slot": "winter-boa-hoodie-pleated-skirt",
        "title": "冬のボアパーカー",
        "season": "winter",
        "outfit_family": "hoodie_sweatshirt",
    },
    {
        "slot": "winter-short-puffer-sweat-culotte",
        "title": "冬の短め中綿ジャケット",
        "season": "winter",
        "outfit_family": "casual_outerwear",
    },
]
IDENTITY_LOCK_PHRASES = [
    "adult 25-year-old japanese woman",
    "akari identity",
    "short warm-brown bob",
    "warm amber eyes",
    "pale blue hair ornament",
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
CASUAL_PHRASES = [
    "akari's own clothes",
    "slightly oversized casual top",
    "lived-in everyday outing mood",
    "socks and sneakers",
]
LEG_QUALITY_PHRASES = [
    "soft thigh volume",
    "natural knee placement",
    "calf transition",
    "ankle shape",
    "healthy leg line",
]
ANTI_CATALOG_PHRASES = [
    "not a fashion catalog model",
    "not a generic background character",
    "clothes must not overpower akari",
]
IMAGE_TEXT_BANS = [
    "no readable image text",
    "no logos",
    "no watermarks",
    "no frame",
    "no panel layout",
]
BANNED_PROMPT_FRAGMENTS = {
    "one-piece",
    "onepiece",
    "elegant blouse",
    "jumper skirt",
    "formal coat",
    "fashion catalog",
    "fashion photography",
    "glamour model",
    "pin-up",
    "school uniform",
    "teenage",
    "little girl",
    "child body",
    "brand logo",
}
JAPANESE_TEXT = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")


def load_json(path):
    if not path.is_file():
        raise AssertionError(f"missing manifest: {path}")
    with path.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


class TonariNoCoordinateHoodieEverydayContractTest(unittest.TestCase):
    def test_generated_working_paths_are_ignored_by_git(self):
        ignored_paths = [
            "source/generated/tonari-no-coordinate/20260708_hoodie-everyday_example_v1.webp",
            "evidence/tonari-no-coordinate/contact-sheets/hoodie-everyday-first-pass.webp",
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
        self.assertEqual(
            "standing_full_body_or_near_full_body",
            manifest["batch_policy"]["composition"],
        )
        self.assertEqual(
            {"hoodie_sweatshirt": 4, "long_tee_outerwear": 2, "casual_outerwear": 2},
            manifest["batch_policy"]["outfit_distribution"],
        )
        self.assertEqual(
            "plain_or_lightly_seasonal_person_first",
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
        self.assertEqual(
            list(range(1, 9)),
            [request["coordinate_order"] for request in requests],
        )
        self.assertEqual(
            {"spring": 2, "summer": 2, "autumn": 2, "winter": 2},
            dict(Counter(request["season"] for request in requests)),
        )
        self.assertEqual(
            {"hoodie_sweatshirt": 4, "long_tee_outerwear": 2, "casual_outerwear": 2},
            dict(Counter(request["outfit_family"] for request in requests)),
        )

    def test_requests_match_candidate_contract(self):
        requests = load_json(MANIFEST)["requests"]

        for request, expected in zip(requests, EXPECTED_CANDIDATES, strict=True):
            with self.subTest(slot=expected["slot"]):
                self.assertEqual(
                    f"request:tonari-coordinate-hoodie-everyday-{expected['slot']}",
                    request["id"],
                )
                self.assertEqual(expected["slot"], request["slot"])
                self.assertEqual(expected["title"], request["japanese_title"])
                self.assertTrue(JAPANESE_TEXT.search(request["japanese_title"]))
                self.assertEqual(expected["season"], request["season"])
                self.assertEqual(expected["outfit_family"], request["outfit_family"])
                self.assertEqual("standing_full_body", request["composition"])
                self.assertTrue(request["outfit_notes"])
                self.assertTrue(request["casual_identity_notes"])
                self.assertTrue(request["leg_quality_notes"])
                self.assertTrue(request["risk_note"])
                self.assertEqual(REFERENCE_PACK_INPUTS, request["reference_pack_inputs"])
                self.assertEqual(
                    f"source/generated/tonari-no-coordinate/{DATE_PREFIX}_hoodie-everyday_{expected['slot']}_v1.webp",
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
                    usage["default_hoodie_outfit_context"]["path"],
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
                self.assertIn("hoodie", usage["default_hoodie_outfit_context"]["instruction"].lower())

    def test_prompts_lock_identity_casualness_leg_quality_and_anti_catalog_rules(self):
        requests = load_json(MANIFEST)["requests"]

        for request in requests:
            with self.subTest(slot=request["slot"]):
                prompt = request["prompt"].lower()
                acceptance = request["acceptance"].lower()
                combined = f"{prompt} {acceptance}"

                self.assertIn(request["japanese_title"].lower(), prompt)
                self.assertIn(request["outfit_notes"].lower(), prompt)
                self.assertIn(request["casual_identity_notes"].lower(), prompt)
                self.assertIn(request["leg_quality_notes"].lower(), prompt)
                self.assertIn("plain or lightly seasonal background", combined)
                self.assertIn("person and outfit stay dominant", combined)

                for phrase in IDENTITY_LOCK_PHRASES:
                    self.assertIn(phrase, prompt)
                for phrase in REFERENCE_PHRASES:
                    self.assertIn(phrase, prompt)
                for phrase in CASUAL_PHRASES:
                    self.assertIn(phrase, combined)
                for phrase in LEG_QUALITY_PHRASES:
                    self.assertIn(phrase, combined)
                for phrase in ANTI_CATALOG_PHRASES:
                    self.assertIn(phrase, combined)
                for phrase in IMAGE_TEXT_BANS:
                    self.assertIn(phrase, combined)
                for fragment in BANNED_PROMPT_FRAGMENTS:
                    self.assertNotIn(fragment, prompt)

    def test_risk_profile_and_review_plan_are_explicit(self):
        requests = load_json(MANIFEST)["requests"]

        for request in requests:
            with self.subTest(slot=request["slot"]):
                risk_profile = request["risk_profile"]
                self.assertEqual("high", risk_profile["identity_risk"])
                self.assertEqual("high", risk_profile["reference_drift_risk"])
                self.assertIn(risk_profile["leg_quality_risk"], {"medium", "high"})
                self.assertIn(risk_profile["catalog_drift_risk"], {"medium", "high"})
                self.assertIn(
                    risk_profile["clothes_overpowering_akari_risk"],
                    {"medium", "high"},
                )
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
uv run python -m unittest tests.test_tonari_no_coordinate_hoodie_everyday_contract
```

Expected: `FAILED` with `missing manifest:
/path/to/akari-design/source/manifests/tonari-no-coordinate/hoodie-everyday-coordinate-requests.json`.

- [ ] **Step 3: Commit the failing test**

Run:

```bash
git add tests/test_tonari_no_coordinate_hoodie_everyday_contract.py
git commit -m "test: add hoodie everyday coordinate contract"
```

## Task 2: Add The Hoodie Everyday Request Manifest

**Files:**

- Create:
  `source/manifests/tonari-no-coordinate/hoodie-everyday-coordinate-requests.json`
- Test:
  `tests/test_tonari_no_coordinate_hoodie_everyday_contract.py`

- [ ] **Step 1: Create the manifest**

Create a static JSON manifest with this exact top-level shape and eight request
objects matching the Candidate Data table:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.1-tonari-no-coordinate-hoodie-everyday",
  "title": "となりのコーデ hoodie everyday",
  "reference_pack_version": "tonari-no-akari-identity-plus-v1-1-hoodie-leg-reference-v1",
  "prompt_template_version": "tonari_coordinate_hoodie_everyday_reference_v1",
  "batch_policy": {
    "candidate_count": 8,
    "seasonal_balance": {
      "spring": 2,
      "summer": 2,
      "autumn": 2,
      "winter": 2
    },
    "composition": "standing_full_body_or_near_full_body",
    "outfit_distribution": {
      "hoodie_sweatshirt": 4,
      "long_tee_outerwear": 2,
      "casual_outerwear": 2
    },
    "background_policy": "plain_or_lightly_seasonal_person_first",
    "reference_policy": "image_references_required_no_prompt_only_generation",
    "pdf_policy": "not_in_this_phase"
  },
  "requests": []
}
```

Each request object must include these fields:

```text
id
coordinate_order
slot
japanese_title
season
scene
outfit_family
outfit_notes
casual_identity_notes
leg_quality_notes
composition
tone
risk_note
target_path
reference_pack_inputs
reference_usage
prompt
acceptance
risk_profile
review_plan
```

Use these exact request-specific values:

```text
1 spring-zip-hoodie-pleated-mini
  title: 春のジップパーカー
  scene: spring_walk
  outfit_family: hoodie_sweatshirt
  outfit_notes: Light zip hoodie over a simple inner top, short pleated skirt, pale socks, and sneakers.
  casual_identity_notes: Closest spring extension of the original hoodie; Akari's own clothes, relaxed and repeat-wearable.
  leg_quality_notes: Keep soft thigh volume visible below the skirt, with natural knee placement, calf transition, ankle shape, and a healthy leg line into socks and sneakers.
  tone: everyday_cute
  risk_note: Avoid school-uniform cues and avoid simply duplicating the original hoodie image.

2 spring-long-tee-denim-layer-shorts
  title: 春のロンTデニム羽織り
  scene: spring_errand
  outfit_family: long_tee_outerwear
  outfit_notes: Oversized long-sleeve T-shirt with a light denim shirt or jacket layer, soft shorts, pale socks, and sneakers.
  casual_identity_notes: Casual spring errand clothes with an easy lived-in mood, not a styled denim catalog look.
  leg_quality_notes: Shorts should show soft thigh volume and natural knee placement without flattening the calf transition or ankle shape.
  tone: casual_fresh
  risk_note: Avoid the denim layer overpowering Akari's face, body balance, or original hoodie warmth.

3 summer-oversized-tee-culotte
  title: 夏の大きめTシャツ
  scene: summer_day_off
  outfit_family: long_tee_outerwear
  outfit_notes: Oversized summer T-shirt, light culotte, short socks, and sneakers with a small pale blue or mint accent.
  casual_identity_notes: Breathable summer everyday clothes; slightly oversized casual top first, cute outfit second.
  leg_quality_notes: Culotte hem should reveal enough thigh and knee read for soft volume, calf transition, ankle shape, and healthy leg line.
  tone: fresh
  risk_note: Avoid logo or text graphics and avoid turning the top into a shapeless blank sack.

4 summer-thin-hoodie-shorts
  title: 夏の薄手フーディ
  scene: summer_walk
  outfit_family: hoodie_sweatshirt
  outfit_notes: Thin light hoodie or rash-guard-like hoodie over a simple top, soft shorts, ankle socks, and sneakers.
  casual_identity_notes: Summer hoodie adaptation that still feels like Akari's own clothes and not beach styling.
  leg_quality_notes: Shorts should keep the thighs softly dimensional, knees natural, calves coherent, ankles clean, and stance relaxed.
  tone: light_casual
  risk_note: Avoid swimwear framing, sporty beach cues, and glamour pose drift.

5 autumn-sweatshirt-check-skirt
  title: 秋のスウェット
  scene: autumn_walk
  outfit_family: hoodie_sweatshirt
  outfit_notes: Soft sweatshirt with a muted check short skirt, ribbed socks, and sneakers.
  casual_identity_notes: Autumn comfort closest to hoodie warmth; lived-in everyday outing mood with soft sleeve volume.
  leg_quality_notes: Check skirt should not hide the thigh-to-knee read; preserve natural knee placement, calf transition, ankle shape, and healthy leg line.
  tone: warm_everyday
  risk_note: Avoid school-uniform cues from the checked skirt and avoid fashion catalog pose.

6 autumn-coach-jacket-hoodie-mini
  title: 秋のコーチジャケット
  scene: autumn_station_meetup
  outfit_family: casual_outerwear
  outfit_notes: Casual coach jacket over a hoodie, short skirt, pale socks, and sneakers.
  casual_identity_notes: Light outerwear variation while preserving hoodie identity and Akari's own clothes feeling.
  leg_quality_notes: Short skirt and socks should leave legs readable from soft thighs through natural knees, calves, ankles, and sneakers.
  tone: casual_warm
  risk_note: Avoid streetwear model styling, brand-like logos, and outfit overpowering Akari.

7 winter-boa-hoodie-pleated-skirt
  title: 冬のボアパーカー
  scene: winter_day_off
  outfit_family: hoodie_sweatshirt
  outfit_notes: Warm boa or fleece hoodie, short pleated skirt or soft skirt, thicker socks, and sneakers.
  casual_identity_notes: Winter warmth without long-coat concealment; soft, approachable, and still visibly Akari first.
  leg_quality_notes: Thicker socks should connect cleanly to calves and ankles while preserving soft thigh volume, natural knees, and healthy leg line.
  tone: soft_winter
  risk_note: Avoid bulky upper body swallowing Akari's proportions.

8 winter-short-puffer-sweat-culotte
  title: 冬の短め中綿ジャケット
  scene: winter_errand
  outfit_family: casual_outerwear
  outfit_notes: Short puffer or padded jacket over a sweatshirt, culotte or shorts, warm socks, and sneakers.
  casual_identity_notes: Practical winter casual outerwear that feels worn by Akari rather than styled on a model.
  leg_quality_notes: Keep legs readable below the culotte or shorts, with coherent thigh volume, knee placement, calf transition, ankle shape, and warm socks.
  tone: practical_cute
  risk_note: Avoid formal coat, long coat, fashion-editorial styling, and clothes overpowering Akari.
```

For every request, set:

```json
"composition": "standing_full_body",
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
  "default_hoodie_outfit_context": {
    "path": "source/references/tonari-no-akari/identity-basic-outfit.webp",
    "instruction": "Mandatory hoodie clothing-volume context; do not copy the outfit directly."
  },
  "side_view_identity": {
    "path": "source/references/tonari-no-akari/identity-side-view.webp",
    "instruction": "Mandatory side silhouette and hair-volume reference."
  },
  "leg_quality_reference": {
    "path": "source/originals/v1_1_front_1.webp",
    "instruction": "Mandatory leg-quality reference for soft thigh volume, natural knee placement, calf transition, ankle shape, and healthy leg line."
  }
}
```

Build each prompt with this exact structure, replacing bracketed values with
the request values:

```text
Create one A4 portrait draft for Tonari no Coordinate: [japanese_title]. Use the attached reference images as mandatory visual anchors; do not generate from prompt text alone. Reference roles: identity-face-hair, identity-body-base, identity-basic-outfit, identity-side-view, and v1_1_front_1 leg-quality reference. Akari identity lock: adult 25-year-old Japanese woman, Akari identity, short warm-brown bob, warm amber eyes, pale blue hair ornament on character-left side. Outfit: [outfit_notes] Casual identity: [casual_identity_notes] Leg quality: [leg_quality_notes] Composition: standing full-body or near full-body coordinate-sheet framing; person and outfit stay dominant. Silhouette: slightly oversized casual top, short skirt/culotte/shorts as support, socks and sneakers, Akari's own clothes, lived-in everyday outing mood. Background: plain or lightly seasonal background only. Not a fashion catalog model, not a generic background character; clothes must not overpower Akari. No readable image text, no logos, no watermarks, no frame, no panel layout.
```

Build each acceptance string with this exact structure:

```text
Coordinate Gate: must preserve Akari identity, adult age impression, face/hair/hairpin consistency, and reference-image continuity. Casual Fit Gate: outfit must feel like Akari's own clothes, with a slightly oversized casual top, socks and sneakers, lived-in everyday outing mood, and no fashion catalog model read. Leg Quality Gate: soft thigh volume, natural knee placement, calf transition, ankle shape, and healthy leg line must remain attractive and coherent. Outfit Gate: [outfit_notes] must read clearly without the clothes overpowering Akari. Background must stay plain or lightly seasonal background support only so person and outfit stay dominant. Reject for missing reference influence, prompt-only drift, generic background character read, broken anatomy, readable text, logos, watermarks, frame, or panel layout.
```

Use this risk profile for every request:

```json
{
  "identity_risk": "high",
  "reference_drift_risk": "high",
  "leg_quality_risk": "high",
  "catalog_drift_risk": "high",
  "clothes_overpowering_akari_risk": "high",
  "text_logo_watermark_risk": "medium"
}
```

Use this review plan for every request:

```json
{
  "initial_status": "draft_candidate",
  "generation_gate": "Generate only with the listed reference images attached or visible in-thread; do not use prompt-only generation.",
  "first_pass": "Place in the eight-image hoodie everyday contact sheet before finishing.",
  "leg_quality_gate": "Run the Leg Quality Gate against v1_1_front_1 softness and continuity.",
  "outcomes": "accept, hold, or reject"
}
```

- [ ] **Step 2: Run the contract test**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_coordinate_hoodie_everyday_contract
```

Expected: `Ran 8 tests` and `OK`.

- [ ] **Step 3: Verify ignored output paths**

Run:

```bash
git check-ignore source/generated/tonari-no-coordinate/20260708_hoodie-everyday_example_v1.webp
git check-ignore evidence/tonari-no-coordinate/contact-sheets/hoodie-everyday-first-pass.webp
```

Expected: both commands print the path and exit `0`.

- [ ] **Step 4: Commit the manifest**

Run:

```bash
git add source/manifests/tonari-no-coordinate/hoodie-everyday-coordinate-requests.json
git commit -m "feat: add hoodie everyday coordinate requests"
```

## Task 3: Cover Contact-Sheet Labels For The New Manifest

**Files:**

- Modify:
  `tests/test_tonari_no_coordinate_contact_sheet.py`
- Test:
  `tests/test_tonari_no_coordinate_contact_sheet.py`

- [ ] **Step 1: Add the label-fitting test**

Add this test method after
`test_real_cute_healthy_seasonal_labels_fit_default_card_width`:

```python
    def test_real_hoodie_everyday_labels_fit_default_card_width(self):
        requests_path = (
            ROOT
            / "source/manifests/tonari-no-coordinate/hoodie-everyday-coordinate-requests.json"
        )
        with requests_path.open(encoding="utf-8") as requests_file:
            requests = json.load(requests_file)["requests"]
        font = load_font(16)
        small_font = load_font(13)
        max_width = 264

        for request in requests:
            with self.subTest(slot=request["slot"]):
                title_line, detail_line = label_lines_for(
                    request,
                    font,
                    small_font,
                    max_width,
                )

                self.assertLessEqual(text_width(title_line, font), max_width)
                self.assertLessEqual(text_width(detail_line, small_font), max_width)
```

- [ ] **Step 2: Run the contact-sheet test file**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_coordinate_contact_sheet
```

Expected: all tests pass.

- [ ] **Step 3: Run both targeted test files**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_coordinate_hoodie_everyday_contract tests.test_tonari_no_coordinate_contact_sheet
```

Expected: both test modules pass.

- [ ] **Step 4: Commit the contact-sheet coverage**

Run:

```bash
git add tests/test_tonari_no_coordinate_contact_sheet.py
git commit -m "test: cover hoodie everyday contact labels"
```

## Task 4: Generate The Eight Reference-Backed Candidates

**Files:**

- Working output:
  `source/generated/tonari-no-coordinate/20260708_hoodie-everyday_<slot>_v1.webp`
- Working evidence:
  `evidence/tonari-no-coordinate/contact-sheets/hoodie-everyday-first-pass.webp`

- [ ] **Step 1: Display the mandatory references in-thread**

Use the image viewer for each mandatory reference before calling `image_gen`:

```text
/path/to/akari-design/source/references/tonari-no-akari/identity-face-hair.webp
/path/to/akari-design/source/references/tonari-no-akari/identity-body-base.webp
/path/to/akari-design/source/references/tonari-no-akari/identity-basic-outfit.webp
/path/to/akari-design/source/references/tonari-no-akari/identity-side-view.webp
/path/to/akari-design/source/originals/v1_1_front_1.webp
```

Also display these successful style anchors if they exist:

```text
/path/to/akari-design/source/generated/tonari-no-coordinate/20260706_cute-healthy_cardigan-mini-onepiece_v1.webp
/path/to/akari-design/source/generated/tonari-no-coordinate/20260706_cute-healthy_summer-blouse-shorts_v1.webp
/path/to/akari-design/source/generated/tonari-no-coordinate/20260706_cute-healthy_short-knit-a-line-skirt_v1.webp
/path/to/akari-design/source/generated/tonari-no-coordinate/20260706_cute-healthy_cafe-jumper-skirt_v1.webp
```

Do not use the rejected seasonal outing contact sheet as a positive style
reference.

- [ ] **Step 2: Create a marker before generation**

Run:

```bash
mkdir -p tmp
touch tmp/hoodie_everyday_generation.marker
```

Expected: marker file exists at `tmp/hoodie_everyday_generation.marker`.

- [ ] **Step 3: Generate one image per manifest request**

For each request, call `image_gen` with the manifest prompt plus this prefix:

```text
Use the visible Akari reference pack and visible successful casual coordinate style references from this thread as visual references. Ignore previous rejected seasonal outing results. Preserve anime illustration finish and standing full-body coordinate-sheet composition. Keep Akari first and the outfit second. Avoid live-action, fashion photography, seated pose, reclining pose, cropped legs, glamour pose, pin-up framing, readable text, logos, and busy scenery.
```

Reject immediately and regenerate when a candidate is live-action, photoreal,
seated, reclining, cropped above the knees, catalog-like, dress-like,
one-piece-like, blouse-led, or missing the reference identity.

- [ ] **Step 4: Convert the accepted PNGs to WebP**

Find PNGs newer than the marker:

```bash
find "$CODEX_HOME/generated_images" -type f -name '*.png' -newer tmp/hoodie_everyday_generation.marker | sort
```

Expected: exactly eight final accepted PNGs, in generation order.

Convert each accepted PNG to its manifest `target_path` with high-quality WebP:

```bash
mapfile -t pngs < <(find "$CODEX_HOME/generated_images" -type f -name '*.png' -newer tmp/hoodie_everyday_generation.marker | sort)
test "${#pngs[@]}" -eq 8
targets=(
  source/generated/tonari-no-coordinate/20260708_hoodie-everyday_spring-zip-hoodie-pleated-mini_v1.webp
  source/generated/tonari-no-coordinate/20260708_hoodie-everyday_spring-long-tee-denim-layer-shorts_v1.webp
  source/generated/tonari-no-coordinate/20260708_hoodie-everyday_summer-oversized-tee-culotte_v1.webp
  source/generated/tonari-no-coordinate/20260708_hoodie-everyday_summer-thin-hoodie-shorts_v1.webp
  source/generated/tonari-no-coordinate/20260708_hoodie-everyday_autumn-sweatshirt-check-skirt_v1.webp
  source/generated/tonari-no-coordinate/20260708_hoodie-everyday_autumn-coach-jacket-hoodie-mini_v1.webp
  source/generated/tonari-no-coordinate/20260708_hoodie-everyday_winter-boa-hoodie-pleated-skirt_v1.webp
  source/generated/tonari-no-coordinate/20260708_hoodie-everyday_winter-short-puffer-sweat-culotte_v1.webp
)
for index in "${!targets[@]}"; do
  cwebp -quiet -q 95 "${pngs[$index]}" -o "${targets[$index]}"
done
```

- [ ] **Step 5: Verify image count and dimensions**

Run:

```bash
uv run python - <<'PY'
from pathlib import Path
from PIL import Image

paths = sorted(Path("source/generated/tonari-no-coordinate").glob("20260708_hoodie-everyday_*_v1.webp"))
print(len(paths))
for path in paths:
    with Image.open(path) as image:
        print(path.as_posix(), image.size, image.mode)
PY
```

Expected: first line is `8`; every image is readable and has an RGB-like mode.

## Task 5: Build And Review The Hoodie Everyday Contact Sheet

**Files:**

- Working evidence:
  `evidence/tonari-no-coordinate/contact-sheets/hoodie-everyday-first-pass.webp`

- [ ] **Step 1: Build the contact sheet**

Run:

```bash
npm run build:coordinate:contact-sheet -- --requests source/manifests/tonari-no-coordinate/hoodie-everyday-coordinate-requests.json --output evidence/tonari-no-coordinate/contact-sheets/hoodie-everyday-first-pass.webp
```

Expected: output includes:

```text
Wrote evidence/tonari-no-coordinate/contact-sheets/hoodie-everyday-first-pass.webp
```

- [ ] **Step 2: Inspect the contact sheet visually**

Open:

```text
/path/to/akari-design/evidence/tonari-no-coordinate/contact-sheets/hoodie-everyday-first-pass.webp
```

Review each candidate for:

```text
Akari identity first
clothes feel personally owned
original hoodie warmth preserved
season visible without costume feel
standing full-body or near full-body framing
socks, sneakers, and legs coherent
no fashion catalog model read
no generic background character read
no dress/one-piece/elegant-blouse drift
```

- [ ] **Step 3: Keep or regenerate weak candidates**

Regenerate any candidate marked reject by the visual review before presenting
the contact sheet. Regeneration must use the same visible references and the
same no-prompt-only gate.

## Task 6: Final Verification And Handoff

**Files:**

- Test:
  `tests/test_tonari_no_coordinate_hoodie_everyday_contract.py`
  `tests/test_tonari_no_coordinate_contact_sheet.py`
- Generated working artifacts:
  `source/generated/tonari-no-coordinate/20260708_hoodie-everyday_*_v1.webp`
  `evidence/tonari-no-coordinate/contact-sheets/hoodie-everyday-first-pass.webp`

- [ ] **Step 1: Run targeted tests**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_coordinate_hoodie_everyday_contract tests.test_tonari_no_coordinate_contact_sheet
```

Expected: all targeted tests pass.

- [ ] **Step 2: Run the default Python suite**

Run:

```bash
npm run test:python
```

Expected: all Python tests pass.

- [ ] **Step 3: Check generated artifacts remain ignored**

Run:

```bash
git status --short --ignored source/generated/tonari-no-coordinate evidence/tonari-no-coordinate
```

Expected: generated image and evidence directories appear only under `!!`.

- [ ] **Step 4: Confirm tracked status**

Run:

```bash
git status --short
```

Expected: no tracked modifications remain after the committed tests and
manifest. Ignored generated artifacts may remain unlisted in this command.

- [ ] **Step 5: Present the contact sheet**

Show the image in the final response:

```markdown
![hoodie everyday contact sheet](/path/to/akari-design/evidence/tonari-no-coordinate/contact-sheets/hoodie-everyday-first-pass.webp)
```

Summarize accepted, hold, and reject observations. Mention any candidates that
were regenerated and why.

## Plan Review

- Difference minimization: this plan adds one new manifest, one new contract
  test, one contact-sheet label test, and ignored generated evidence only.
- Existing pattern fit: it mirrors the existing seasonal coordinate manifest,
  unittest contract style, target path layout, and contact-sheet builder.
- Edge-case verification: tests cover reference-pack requirements, exact
  candidate order, no prompt-only generation, anti-catalog prompt boundaries,
  ignored artifact paths, label fitting, and full-suite regression.
