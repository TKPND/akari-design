# Akari v1.1 Tonari No Hyoujou Generation Requests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a tested 18-slot draft generation request manifest for the approved `となりの表情` expression collection.

**Architecture:** Keep this phase data-only: add one `tonari-no-hyoujou` generation request manifest and one focused Python contract test. Reuse the existing Akari v1.1 identity reference pack paths from `source/references/tonari-no-akari/`, but do not add a PDF renderer, page manifest, asset manifest, generated images, or finished review artifacts in this phase.

**Tech Stack:** Python 3 standard library `unittest` and `json`, repository JSON manifests, markdownlint-cli2 through `npm run lint:md`, existing npm/uv verification scripts.

---

## Current Context

- Approved design spec:
  `docs/superpowers/specs/2026-07-03-akari-v1-1-tonari-no-hyoujou-design.md`
- Existing identity references to reuse:
  `source/references/tonari-no-akari/identity-face-hair.webp`,
  `source/references/tonari-no-akari/identity-body-base.webp`,
  `source/references/tonari-no-akari/identity-basic-outfit.webp`, and
  `source/references/tonari-no-akari/identity-side-view.webp`
- New manifest directory:
  `source/manifests/tonari-no-hyoujou/`
- New generated draft image directory named in manifest only:
  `source/generated/tonari-no-hyoujou/`
- This plan intentionally stops before actual image generation.

## Scope Check

The approved spec has one implementation slice ready now: turn the 18 expression
slots into traceable generation requests. PDF rendering, contact sheet assembly,
actual image generation, and per-image `akari-v1-1-image-review` work are
separate later slices because they depend on generated candidate images.

## Target File Structure

```text
tests/test_tonari_no_hyoujou_contract.py
source/manifests/tonari-no-hyoujou/generation-requests.json
docs/superpowers/plans/2026-07-03-akari-v1-1-tonari-no-hyoujou-generation-requests.md
```

## Data Model

Use this manifest shape:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.1-tonari-no-hyoujou",
  "title": "となりの表情",
  "reference_pack_version": "tonari-no-akari-identity-v1",
  "draft_strategy": {
    "candidate_stage": "draft_all_18_first",
    "strict_review_stage": "likely_accepts_only",
    "heavy_pdf_or_ocr_audit": "not_applicable_until_pdf_exists"
  },
  "review_workflow": {
    "first_pass": "Build the full 18-image expression map before any heavy finishing pass.",
    "selected_candidate_review": "Run akari-v1-1-image-review on one selected image at a time.",
    "correction_rule": "Use Correction Pass only for concrete defects.",
    "humanization_rule": "Use Humanization Pass only after structural validity is confirmed."
  },
  "requests": []
}
```

Each request must include:

- `id`
- `slot`
- `japanese_title`
- `reaction`
- `emotion`
- `distance`
- `target_path`
- `reference_pack_inputs`
- `prompt`
- `acceptance`
- `risk_profile`
- `review_plan`

## Task 1: Add The Failing Tonari No Hyoujou Contract Test

**Files:**

- Create: `tests/test_tonari_no_hyoujou_contract.py`
- Read: `docs/superpowers/specs/2026-07-03-akari-v1-1-tonari-no-hyoujou-design.md`
- Read: `tests/test_tonari_no_akari_contract.py`

- [ ] **Step 1: Write the failing contract test**

Create `tests/test_tonari_no_hyoujou_contract.py`:

```python
import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "source/manifests/tonari-no-hyoujou/generation-requests.json"
COLLECTION_ID = "akari-v1.1-tonari-no-hyoujou"
TITLE = "となりの表情"
REFERENCE_PACK_VERSION = "tonari-no-akari-identity-v1"
REFERENCE_PACK_INPUTS = [
    "source/references/tonari-no-akari/identity-face-hair.webp",
    "source/references/tonari-no-akari/identity-body-base.webp",
    "source/references/tonari-no-akari/identity-basic-outfit.webp",
    "source/references/tonari-no-akari/identity-side-view.webp",
]
JAPANESE_TEXT = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
EXPECTED_DISTANCE_COUNTS = {
    "close_portrait": 10,
    "half_body": 5,
    "full_body_or_wider_gesture": 3,
}
EXPECTED_SLOTS = [
    {
        "slot": "called-turn",
        "title": "呼ばれて振り向く",
        "emotion": "familiar ease",
        "distance": "close_portrait",
    },
    {
        "slot": "eye-contact-pause",
        "title": "目が合って止まる",
        "emotion": "shyness",
        "distance": "close_portrait",
    },
    {
        "slot": "compliment-blush",
        "title": "褒められて照れる",
        "emotion": "shy happiness",
        "distance": "close_portrait",
    },
    {
        "slot": "teased-pout",
        "title": "からかわれてむっとする",
        "emotion": "resistance",
        "distance": "close_portrait",
    },
    {
        "slot": "answer-hesitation",
        "title": "言い返す前",
        "emotion": "hesitation",
        "distance": "half_body",
    },
    {
        "slot": "side-glance-sulk",
        "title": "拗ねた目線",
        "emotion": "sulking",
        "distance": "close_portrait",
    },
    {
        "slot": "failed-straight-face",
        "title": "でも笑ってしまう",
        "emotion": "warmth",
        "distance": "close_portrait",
    },
    {
        "slot": "small-pride",
        "title": "小さく得意げ",
        "emotion": "pride",
        "distance": "half_body",
    },
    {
        "slot": "sudden-surprise",
        "title": "不意に驚く",
        "emotion": "surprise",
        "distance": "half_body",
    },
    {
        "slot": "worried-peek",
        "title": "心配そうに覗く",
        "emotion": "concern",
        "distance": "half_body",
    },
    {
        "slot": "relief-release",
        "title": "安心して力が抜ける",
        "emotion": "relief",
        "distance": "close_portrait",
    },
    {
        "slot": "sleepy-reply",
        "title": "眠たげに返事する",
        "emotion": "softness",
        "distance": "close_portrait",
    },
    {
        "slot": "lonely-quiet",
        "title": "少し寂しそう",
        "emotion": "loneliness",
        "distance": "close_portrait",
    },
    {
        "slot": "brave-okay-face",
        "title": "平気な顔をする",
        "emotion": "brave front",
        "distance": "full_body_or_wider_gesture",
    },
    {
        "slot": "honest-happy",
        "title": "素直に嬉しい顔",
        "emotion": "honest joy",
        "distance": "close_portrait",
    },
    {
        "slot": "near-shy-cover",
        "title": "近距離の照れ隠し",
        "emotion": "fluster",
        "distance": "half_body",
    },
    {
        "slot": "leaving-turn",
        "title": "帰り際に振り向く",
        "emotion": "afterglow",
        "distance": "full_body_or_wider_gesture",
    },
    {
        "slot": "almost-says",
        "title": "何か言いかけて笑う",
        "emotion": "warm restraint",
        "distance": "full_body_or_wider_gesture",
    },
]
IDENTITY_LOCK_PHRASES = [
    "adult 25-year-old japanese woman",
    "naturally cute adult",
    "not glamorous",
    "not model-like",
    "not pin-up",
    "not childlike",
    "short fluffy light-brown bob",
    "airy uneven ends",
    "soft side bangs",
    "warm amber eyes",
    "rounded cheeks",
    "compact rounded chin",
    "small subtle nose and mouth",
    "pale-blue crossed hairpins",
    "healthy adult proportions",
]
IMAGE_TEXT_BANS = [
    "no image-internal readable text",
    "no logos",
    "no watermarks",
    "no frame",
    "no border",
    "no panel layout",
]
BANNED_PROMPT_FRAGMENTS = [
    "school uniform",
    "teenage",
    "little girl",
    "child",
    "pinup",
    "pin-up pose",
    "glamour model",
]


def load_json(path):
    with path.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


class TonariNoHyoujouContractTest(unittest.TestCase):
    def test_generation_request_manifest_exists(self):
        self.assertTrue(MANIFEST.is_file(), f"missing manifest: {MANIFEST}")

    def test_collection_metadata_records_draft_first_strategy(self):
        manifest = load_json(MANIFEST)

        self.assertEqual(1, manifest["schema_version"])
        self.assertEqual(COLLECTION_ID, manifest["collection_id"])
        self.assertEqual(TITLE, manifest["title"])
        self.assertEqual(REFERENCE_PACK_VERSION, manifest["reference_pack_version"])
        self.assertEqual(
            "draft_all_18_first",
            manifest["draft_strategy"]["candidate_stage"],
        )
        self.assertEqual(
            "likely_accepts_only",
            manifest["draft_strategy"]["strict_review_stage"],
        )
        self.assertEqual(
            "not_applicable_until_pdf_exists",
            manifest["draft_strategy"]["heavy_pdf_or_ocr_audit"],
        )

    def test_requests_match_approved_18_slot_map(self):
        manifest = load_json(MANIFEST)
        requests = manifest["requests"]

        self.assertEqual(18, len(requests))
        self.assertEqual(
            [expected["slot"] for expected in EXPECTED_SLOTS],
            [request["slot"] for request in requests],
        )
        self.assertEqual(
            EXPECTED_DISTANCE_COUNTS,
            dict(Counter(request["distance"] for request in requests)),
        )

        for index, (request, expected) in enumerate(
            zip(requests, EXPECTED_SLOTS, strict=True),
            start=1,
        ):
            with self.subTest(slot=request["slot"]):
                self.assertEqual(f"request:tonari-hyoujou-{expected['slot']}", request["id"])
                self.assertEqual(expected["title"], request["japanese_title"])
                self.assertTrue(JAPANESE_TEXT.search(request["japanese_title"]))
                self.assertEqual(expected["emotion"], request["emotion"])
                self.assertEqual(expected["distance"], request["distance"])
                self.assertTrue(request["reaction"])
                self.assertEqual(REFERENCE_PACK_INPUTS, request["reference_pack_inputs"])
                self.assertEqual(
                    f"source/generated/tonari-no-hyoujou/20260703_{expected['slot']}_v1.webp",
                    request["target_path"],
                )
                self.assertEqual(index, request["expression_order"])

    def test_prompts_preserve_identity_and_block_text_artifacts(self):
        manifest = load_json(MANIFEST)

        for request in manifest["requests"]:
            with self.subTest(slot=request["slot"]):
                prompt = request["prompt"].lower()
                acceptance = request["acceptance"].lower()
                combined = f"{prompt} {acceptance}"

                self.assertIn(request["reaction"].lower(), prompt)
                self.assertIn(request["emotion"].lower(), prompt)
                self.assertIn("readable but not theatrical", prompt)
                for phrase in IDENTITY_LOCK_PHRASES:
                    self.assertIn(phrase, prompt)
                for phrase in IMAGE_TEXT_BANS:
                    self.assertIn(phrase, combined)
                for fragment in BANNED_PROMPT_FRAGMENTS:
                    self.assertNotIn(fragment, prompt)

    def test_risk_profiles_and_review_plan_are_explicit(self):
        manifest = load_json(MANIFEST)
        review_workflow_text = " ".join(manifest["review_workflow"].values())

        self.assertIn("18-image expression map", review_workflow_text)
        self.assertIn("akari-v1-1-image-review", review_workflow_text)
        self.assertIn("Correction Pass", review_workflow_text)
        self.assertIn("Humanization Pass", review_workflow_text)

        for request in manifest["requests"]:
            with self.subTest(slot=request["slot"]):
                risk_profile = request["risk_profile"]
                self.assertEqual("high", risk_profile["identity_risk"])
                self.assertIn(risk_profile["face_expression_risk"], {"medium", "high"})
                self.assertIn(risk_profile["hand_risk"], {"low", "medium", "high"})
                self.assertEqual("medium", risk_profile["text_logo_watermark_risk"])

                review_plan = request["review_plan"]
                self.assertEqual("draft_candidate", review_plan["initial_status"])
                self.assertIn("expression map", review_plan["first_pass"])
                self.assertIn("akari-v1-1-image-review", review_plan["strict_review"])
                self.assertIn("Correction Pass", review_plan["correction"])
                self.assertIn("Humanization Pass", review_plan["humanization"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_hyoujou_contract
```

Expected: `FAIL` or `ERROR` because
`source/manifests/tonari-no-hyoujou/generation-requests.json` does not exist.

- [ ] **Step 3: Commit the failing test**

Run:

```bash
git add tests/test_tonari_no_hyoujou_contract.py
git commit -m "test: add Tonari no Hyoujou generation contract"
```

Expected: a commit containing only
`tests/test_tonari_no_hyoujou_contract.py`.

## Task 2: Add The 18 Draft Generation Requests Manifest

**Files:**

- Create: `source/manifests/tonari-no-hyoujou/generation-requests.json`
- Test: `tests/test_tonari_no_hyoujou_contract.py`

- [ ] **Step 1: Create the manifest directory**

Run:

```bash
mkdir -p source/manifests/tonari-no-hyoujou
```

Expected: the directory exists and no tracked files change yet.

- [ ] **Step 2: Write the generation request manifest**

Create `source/manifests/tonari-no-hyoujou/generation-requests.json` with this
content:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.1-tonari-no-hyoujou",
  "title": "となりの表情",
  "reference_pack_version": "tonari-no-akari-identity-v1",
  "draft_strategy": {
    "candidate_stage": "draft_all_18_first",
    "strict_review_stage": "likely_accepts_only",
    "heavy_pdf_or_ocr_audit": "not_applicable_until_pdf_exists"
  },
  "review_workflow": {
    "first_pass": "Build the full 18-image expression map before any heavy finishing pass.",
    "selected_candidate_review": "Run akari-v1-1-image-review on one selected image at a time.",
    "correction_rule": "Use Correction Pass only for concrete defects.",
    "humanization_rule": "Use Humanization Pass only after structural validity is confirmed."
  },
  "requests": [
    {
      "id": "request:tonari-hyoujou-called-turn",
      "expression_order": 1,
      "slot": "called-turn",
      "japanese_title": "呼ばれて振り向く",
      "reaction": "she turns toward the viewer after being called from nearby",
      "emotion": "familiar ease",
      "distance": "close_portrait",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_called-turn_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: she turns toward the viewer after being called from nearby. Emotion: familiar ease. Composition: close portrait, face readable, shoulders relaxed, everyday near-distance mood. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean anatomy, close readable expression, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "medium",
        "hand_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-eye-contact-pause",
      "expression_order": 2,
      "slot": "eye-contact-pause",
      "japanese_title": "目が合って止まる",
      "reaction": "eye contact lands a little too directly and she pauses for one beat",
      "emotion": "shyness",
      "distance": "close_portrait",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_eye-contact-pause_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: eye contact lands a little too directly and she pauses for one beat. Emotion: shyness. Composition: close portrait, quiet direct gaze, tiny hesitation around mouth and eyes, everyday indoor or soft outdoor light. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean anatomy, close readable expression, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "high",
        "hand_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-compliment-blush",
      "expression_order": 3,
      "slot": "compliment-blush",
      "japanese_title": "褒められて照れる",
      "reaction": "she receives a compliment before she can prepare and tries not to show too much happiness",
      "emotion": "shy happiness",
      "distance": "close_portrait",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_compliment-blush_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: she receives a compliment before she can prepare and tries not to show too much happiness. Emotion: shy happiness. Composition: close portrait, small blush, softened eyes, restrained smile, cozy everyday distance. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean anatomy, close readable expression, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "high",
        "hand_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-teased-pout",
      "expression_order": 4,
      "slot": "teased-pout",
      "japanese_title": "からかわれてむっとする",
      "reaction": "a teasing remark makes her push back with a small annoyed face",
      "emotion": "resistance",
      "distance": "close_portrait",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_teased-pout_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: a teasing remark makes her push back with a small annoyed face. Emotion: resistance. Composition: close portrait, slight pout, brows gently knit, still affectionate rather than angry, everyday conversation distance. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean anatomy, close readable expression, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "high",
        "hand_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-answer-hesitation",
      "expression_order": 5,
      "slot": "answer-hesitation",
      "japanese_title": "言い返す前",
      "reaction": "she is about to answer back and hesitates before choosing softer words",
      "emotion": "hesitation",
      "distance": "half_body",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_answer-hesitation_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: she is about to answer back and hesitates before choosing softer words. Emotion: hesitation. Composition: half body, mouth slightly parted, shoulders caught mid-response, simple relaxed hands or hands mostly out of frame. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean anatomy, readable half-body expression, natural shoulders and hands, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "medium",
        "hand_risk": "medium",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-side-glance-sulk",
      "expression_order": 6,
      "slot": "side-glance-sulk",
      "japanese_title": "拗ねた目線",
      "reaction": "she looks aside while still listening, pretending not to care",
      "emotion": "sulking",
      "distance": "close_portrait",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_side-glance-sulk_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: she looks aside while still listening, pretending not to care. Emotion: sulking. Composition: close portrait, side glance, lips lightly pressed, soft everyday light, no harsh drama. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean anatomy, close readable expression, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "high",
        "hand_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-failed-straight-face",
      "expression_order": 7,
      "slot": "failed-straight-face",
      "japanese_title": "でも笑ってしまう",
      "reaction": "her serious face breaks into a smile despite trying to hold it",
      "emotion": "warmth",
      "distance": "close_portrait",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_failed-straight-face_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: her serious face breaks into a smile despite trying to hold it. Emotion: warmth. Composition: close portrait, uneven little smile, eyes softening first, intimate everyday conversation mood. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean anatomy, close readable expression, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "high",
        "hand_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-small-pride",
      "expression_order": 8,
      "slot": "small-pride",
      "japanese_title": "小さく得意げ",
      "reaction": "she accepts a tiny win and looks quietly proud",
      "emotion": "pride",
      "distance": "half_body",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_small-pride_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: she accepts a tiny win and looks quietly proud. Emotion: pride. Composition: half body, small confident smile, chin slightly lifted, relaxed arms, everyday setting without props requiring text. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean anatomy, readable half-body expression, natural hands, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "medium",
        "hand_risk": "medium",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-sudden-surprise",
      "expression_order": 9,
      "slot": "sudden-surprise",
      "japanese_title": "不意に驚く",
      "reaction": "something unexpected catches her off guard in the middle of conversation",
      "emotion": "surprise",
      "distance": "half_body",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_sudden-surprise_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: something unexpected catches her off guard in the middle of conversation. Emotion: surprise. Composition: half body, widened eyes, tiny intake of breath, shoulders lifted slightly, hands simple and separated if visible. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean anatomy, readable half-body expression, simple separated hands if visible, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "high",
        "hand_risk": "medium",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-worried-peek",
      "expression_order": 10,
      "slot": "worried-peek",
      "japanese_title": "心配そうに覗く",
      "reaction": "she leans or peeks in to check on the viewer",
      "emotion": "concern",
      "distance": "half_body",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_worried-peek_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: she leans or peeks in to check on the viewer. Emotion: concern. Composition: half body, slight forward lean, worried but gentle eyes, one simple hand near chest or edge of frame, no medical or emergency props. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean anatomy, readable half-body expression, natural lean and hand, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "medium",
        "hand_risk": "medium",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-relief-release",
      "expression_order": 11,
      "slot": "relief-release",
      "japanese_title": "安心して力が抜ける",
      "reaction": "tension leaves her face and shoulders after hearing everything is okay",
      "emotion": "relief",
      "distance": "close_portrait",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_relief-release_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: tension leaves her face and shoulders after hearing everything is okay. Emotion: relief. Composition: close portrait, softened eyelids, small exhale, shoulders dropping gently, calm everyday light. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean anatomy, close readable expression, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "medium",
        "hand_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-sleepy-reply",
      "expression_order": 12,
      "slot": "sleepy-reply",
      "japanese_title": "眠たげに返事する",
      "reaction": "she answers softly while still sleepy",
      "emotion": "softness",
      "distance": "close_portrait",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_sleepy-reply_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: she answers softly while still sleepy. Emotion: softness. Composition: close portrait, heavy eyelids, quiet morning or afternoon light, relaxed mouth, gentle adult tiredness rather than childish drowsiness. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean anatomy, close readable expression, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "medium",
        "hand_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-lonely-quiet",
      "expression_order": 13,
      "slot": "lonely-quiet",
      "japanese_title": "少し寂しそう",
      "reaction": "her expression goes quiet for a moment after the conversation thins out",
      "emotion": "loneliness",
      "distance": "close_portrait",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_lonely-quiet_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: her expression goes quiet for a moment after the conversation thins out. Emotion: loneliness. Composition: close portrait, lowered gaze or softened side gaze, restrained mouth, quiet light, no melodrama or crying. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean anatomy, close readable expression, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "high",
        "hand_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-brave-okay-face",
      "expression_order": 14,
      "slot": "brave-okay-face",
      "japanese_title": "平気な顔をする",
      "reaction": "she says she is fine before fully meaning it",
      "emotion": "brave front",
      "distance": "full_body_or_wider_gesture",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_brave-okay-face_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: she says she is fine before fully meaning it. Emotion: brave front. Composition: full body or wider gesture, standing with a controlled small smile and slightly tense shoulders, feet grounded, hands simple and separated. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean full-body anatomy, readable expression and posture, official outfit impression if feet are visible, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "medium",
        "hand_risk": "medium",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-honest-happy",
      "expression_order": 15,
      "slot": "honest-happy",
      "japanese_title": "素直に嬉しい顔",
      "reaction": "she lets happiness show plainly without hiding it",
      "emotion": "honest joy",
      "distance": "close_portrait",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_honest-happy_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: she lets happiness show plainly without hiding it. Emotion: honest joy. Composition: close portrait, open gentle smile, warm eyes, simple light, natural adult happiness without exaggerated sparkle effects. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean anatomy, close readable expression, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "high",
        "hand_risk": "low",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-near-shy-cover",
      "expression_order": 16,
      "slot": "near-shy-cover",
      "japanese_title": "近距離の照れ隠し",
      "reaction": "she deflects a close-distance blush with a small cover gesture",
      "emotion": "fluster",
      "distance": "half_body",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_near-shy-cover_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: she deflects a close-distance blush with a small cover gesture. Emotion: fluster. Composition: half body, one hand near cheek or mouth but not covering identity, fingers simple and readable, close everyday distance. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, readable face, natural simple hand, clean half-body anatomy, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "high",
        "hand_risk": "high",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-leaving-turn",
      "expression_order": 17,
      "slot": "leaving-turn",
      "japanese_title": "帰り際に振り向く",
      "reaction": "she turns back just before leaving",
      "emotion": "afterglow",
      "distance": "full_body_or_wider_gesture",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_leaving-turn_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: she turns back just before leaving. Emotion: afterglow. Composition: full body or wider gesture, walking-away posture with face visible enough to read, clean feet and shoes if visible, simple unbranded path or room exit. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean full-body anatomy, readable expression despite distance, official outfit impression if feet are visible, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "medium",
        "hand_risk": "medium",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    },
    {
      "id": "request:tonari-hyoujou-almost-says",
      "expression_order": 18,
      "slot": "almost-says",
      "japanese_title": "何か言いかけて笑う",
      "reaction": "she almost says something important, then smiles instead",
      "emotion": "warm restraint",
      "distance": "full_body_or_wider_gesture",
      "target_path": "source/generated/tonari-no-hyoujou/20260703_almost-says_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Create one A4 portrait draft for Tonari no Hyoujou: she almost says something important, then smiles instead. Emotion: warm restraint. Composition: full body or wider gesture, quiet final image feeling, face readable, posture gentle, hands simple, clean unbranded background. Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, not glamorous, not model-like, not pin-up, not childlike; short fluffy light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; petite/slender healthy adult proportions. Keep the reaction readable but not theatrical. No image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must preserve Akari identity, adult age impression, face/hair/hairpin consistency, clean full-body anatomy, readable expression and posture, and no image-internal readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "risk_profile": {
        "identity_risk": "high",
        "face_expression_risk": "medium",
        "hand_risk": "medium",
        "text_logo_watermark_risk": "medium"
      },
      "review_plan": {
        "initial_status": "draft_candidate",
        "first_pass": "Place in the 18-image expression map before finishing.",
        "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
        "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
        "humanization": "Use Humanization Pass only after the image is structurally valid."
      }
    }
  ]
}
```

- [ ] **Step 3: Validate the JSON syntax**

Run:

```bash
python -m json.tool source/manifests/tonari-no-hyoujou/generation-requests.json >/dev/null
```

Expected: exit code `0`.

- [ ] **Step 4: Run the focused contract test**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_hyoujou_contract
```

Expected: `OK`.

- [ ] **Step 5: Commit the passing manifest**

Run:

```bash
git add source/manifests/tonari-no-hyoujou/generation-requests.json
git commit -m "feat: add Tonari no Hyoujou generation requests"
```

Expected: a commit containing only
`source/manifests/tonari-no-hyoujou/generation-requests.json`.

## Task 3: Run Repository Verification And Commit Any Plan Tracking Updates

**Files:**

- Verify: `tests/test_tonari_no_hyoujou_contract.py`
- Verify: `source/manifests/tonari-no-hyoujou/generation-requests.json`
- Verify: `docs/superpowers/plans/2026-07-03-akari-v1-1-tonari-no-hyoujou-generation-requests.md`

- [ ] **Step 1: Run the relevant Python tests**

Run:

```bash
npm run test:python
```

Expected: `OK` from the Python unittest suite.

- [ ] **Step 2: Run Markdown lint**

Run:

```bash
npm run lint:md
```

Expected: `Summary: 0 error(s)`.

- [ ] **Step 3: Confirm only intended files changed**

Run:

```bash
git status --short
```

Expected after Task 1 and Task 2 commits: either a clean worktree or only this
plan file if it was written during planning.

- [ ] **Step 4: Commit this plan file if it is still unstaged**

Run:

```bash
git add docs/superpowers/plans/2026-07-03-akari-v1-1-tonari-no-hyoujou-generation-requests.md
git commit -m "plan: add Tonari no Hyoujou generation request plan"
```

Expected: the plan file is committed by itself.

## Self-Review

- Spec coverage: covers the approved title, 18 slots, distance mix, medium
  expression range, draft-all-first review strategy, and later
  `akari-v1-1-image-review` gate.
- Completion scan: no implementation step depends on unfinished notes,
  generated values, or unspecified files.
- Type consistency: the test, manifest shape, request field names, target paths,
  collection id, and reference pack paths use the same names throughout.
- Scope control: no PDF renderer, actual image generation, contact sheet, or
  finished image review is included in this slice.
