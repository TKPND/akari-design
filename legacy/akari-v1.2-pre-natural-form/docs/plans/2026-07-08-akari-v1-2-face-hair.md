# Akari v1.2 Face And Hair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a narrow v1.2 face-and-hair exploration workflow that produces eight matched bust-up Akari candidates, a comparison contact sheet, and first-pass selection material.

**Architecture:** Keep v1.2 exploration separate from v1.1 production PDFs. Commit only the reusable request manifest, validation tests, and contact-sheet tooling; keep generated candidate images and comparison evidence in ignored working directories unless the user explicitly chooses a final deliverable. The request manifest locks shared identity, composition, and rejection gates so the eight images vary mainly in eyes.

**Tech Stack:** Python 3.11, `unittest`, JSON manifests, Pillow, built-in image generation, `uv run python`, existing npm scripts.

---

## Scope Check

The approved spec covers one subsystem: Akari v1.2 face-and-hair visual
exploration. This plan does not update the v1.1 settings PDF, redesign the
full body, add outfit variants, or create a v1.2 PDF product.

Generated exploration images and contact sheets are working artifacts. They
stay out of git unless the user explicitly asks to preserve a selected final
direction.

## Current Context

- Approved design spec:
  `docs/superpowers/specs/2026-07-08-akari-v1-2-face-hair-design.md`
- Primary v1.1 face identity references:
  `source/originals/v1_1_front_3.webp`,
  `source/originals/v1_1_front_1.webp`, and
  `source/originals/v1_1_front_2.webp`
- Existing packaged face reference:
  `source/references/tonari-no-akari/identity-face-hair.webp`
- Mid-run finding:
  the first text-only eight-candidate batch did not preserve Akari's v1.1
  identity and is rejected as selection material.
- Reference pilot finding:
  the first reference-locked pilot still drifted into a darker-haired, more
  mature alternate character with flower-like hair accessory drift.
- Hyoujou reference decision:
  if original v1.1 references keep producing generic faces, use
  `tonari-no-hyoujou` bust-up images as the face family reference, with
  `20260703_called-turn_v2.webp` as the main anchor.
- New manifest directory:
  `source/manifests/v1-2-face-hair/`
- New generated draft image directory:
  `source/generated/v1-2-face-hair/`
- New evidence directory:
  `evidence/v1-2-face-hair/`

## File Structure

- Modify `.gitignore`
  - Ignore `source/generated/v1-2-face-hair/` and
    `evidence/v1-2-face-hair/`.
- Create `tests/test_v1_2_face_hair_contract.py`
  - Contract tests for the request manifest, identity locks, candidate count,
    target paths, text bans, and ignored working folders.
- Create `source/manifests/v1-2-face-hair/generation-requests.json`
  - Source-of-truth prompt and review contract for the eight candidates.
- Create `tests/test_v1_2_face_hair_contact_sheet.py`
  - Unit tests for contact-sheet construction from generated candidate files.
- Create `scripts/build_v1_2_face_hair_contact_sheet.py`
  - Builds a labeled 4x2 comparison sheet from generated images already saved
    under `source/generated/v1-2-face-hair/`.
- Modify `package.json`
  - Add `build:v1-2-face-hair:contact-sheet`.
- Modify `source/manifests/v1-2-face-hair/generation-requests.json`
  - Add reference-locked prompt language before any further generation.
- Working-only output paths:
  - `source/generated/v1-2-face-hair/20260708_<slot>_v1.png`
  - `source/generated/v1-2-face-hair/reference-pilot/20260708_soft-horizontal-eyes_ref-v1.png`
  - `source/generated/v1-2-face-hair/reference-pilot/20260708_soft-horizontal-eyes_ref-v2.png`
  - `source/generated/v1-2-face-hair/reference-pilot/20260708_soft-horizontal-eyes_hyoujou-v1.png`
  - `evidence/v1-2-face-hair/contact-sheets/akari-v1-2-face-hair-first-pass.webp`
  - `evidence/v1-2-face-hair/reviews/20260708-first-pass-review.json`

## Data Model

Use this request manifest shape:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.2-face-hair",
  "title": "Akari v1.2 Face And Hair",
  "reference_pack_version": "akari-v1.1-face-hair-identity-v1",
  "prompt_template_version": "akari_v1_2_face_hair_eye_axis_v1",
  "batch_policy": {
    "candidate_count": 8,
    "composition": "matched_bust_up",
    "primary_variation_axis": "eyes",
    "secondary_variation_axis": "organized_v1_1_short_bob",
    "hair_ornament_policy": "keep_character_left_pale_blue_pin",
    "pdf_policy": "not_in_this_phase"
  },
  "requests": []
}
```

Each request must include:

- `id`
- `candidate_order`
- `slot`
- `japanese_title`
- `eye_variation`
- `hair_variation`
- `target_path`
- `reference_pack_inputs`
- `prompt`
- `acceptance`
- `selection_gates`
- `risk_profile`

## Task 1: Add The Failing Face/Hair Contract Test

**Files:**

- Modify: `.gitignore`
- Create: `tests/test_v1_2_face_hair_contract.py`

- [ ] **Step 1: Write the failing contract test**

Create `tests/test_v1_2_face_hair_contract.py`:

```python
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "source/manifests/v1-2-face-hair/generation-requests.json"
COLLECTION_ID = "akari-v1.2-face-hair"
TITLE = "Akari v1.2 Face And Hair"
REFERENCE_PACK_VERSION = "akari-v1.1-face-hair-identity-v1"
PROMPT_TEMPLATE_VERSION = "akari_v1_2_face_hair_eye_axis_v1"
DATE_PREFIX = "20260708"
REFERENCE_PACK_INPUTS = [
    "source/originals/v1_1_front_3.webp",
    "source/originals/v1_1_front_1.webp",
    "source/originals/v1_1_front_2.webp",
    "source/references/tonari-no-akari/identity-face-hair.webp",
]
EXPECTED_CANDIDATES = [
    {
        "slot": "soft-horizontal-eyes",
        "title": "柔らかい水平寄りの目",
        "eye_variation": "soft horizontal eyes with calm direct gaze",
        "hair_variation": "baseline organized short bob",
    },
    {
        "slot": "round-innocent-eyes",
        "title": "少し丸くあどけない目",
        "eye_variation": "slightly rounder eyes with strong innocence",
        "hair_variation": "soft rounded bangs",
    },
    {
        "slot": "lowered-lid-gentle",
        "title": "まぶたに重みのある優しい目",
        "eye_variation": "gentle eyes with lowered eyelid weight",
        "hair_variation": "clean side hair framing",
    },
    {
        "slot": "bright-catchlights",
        "title": "光の入った温かい目",
        "eye_variation": "warm eyes with brighter catchlights",
        "hair_variation": "light bang grouping",
    },
    {
        "slot": "stable-narrower-eyes",
        "title": "少し細めで落ち着いた目",
        "eye_variation": "mildly narrower eyes with stable expression",
        "hair_variation": "organized bob volume",
    },
    {
        "slot": "shy-soft-gaze",
        "title": "少し照れた柔らかい目線",
        "eye_variation": "soft eyes with slightly shy gaze",
        "hair_variation": "gentle hair-tip movement",
    },
    {
        "slot": "v1-1-cleaner-eyes",
        "title": "v1.1に近い整理された目",
        "eye_variation": "v1.1-near eyes with cleaner rendering",
        "hair_variation": "v1.1-near bob cleanup",
    },
    {
        "slot": "balanced-hybrid",
        "title": "強い要素を混ぜたバランス案",
        "eye_variation": "balanced hybrid candidate based on strongest prior traits",
        "hair_variation": "balanced organized short bob",
    },
]
IDENTITY_LOCK_PHRASES = [
    "Akari v1.1 evolving into v1.2",
    "adult early-20s Japanese young woman as character design, not realism",
    "soft approachable innocence",
    "warm brown eyes",
    "warm brown short bob",
    "soft bangs",
    "pale blue hair ornament on Akari's character-left side",
    "white oversized hoodie context",
]
REQUIRED_ACCEPTANCE_PHRASES = [
    "Appeal Gate",
    "Identity Gate",
    "matched bust-up",
    "no readable text",
    "no logos",
    "no watermarks",
    "no frame",
    "no panel layout",
]
BANNED_PROMPT_FRAGMENTS = [
    "school uniform",
    "teenage",
    "little girl",
    "child body",
    "pin-up",
    "glamour model",
    "brand logo",
]
JAPANESE_TEXT = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")


def load_json(path):
    with path.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


class AkariV12FaceHairContractTest(unittest.TestCase):
    def test_generated_working_directories_are_ignored(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()

        self.assertIn("source/generated/v1-2-face-hair/", gitignore)
        self.assertIn("evidence/v1-2-face-hair/", gitignore)

    def test_manifest_exists_and_records_batch_policy(self):
        self.assertTrue(MANIFEST.is_file(), f"missing manifest: {MANIFEST}")
        manifest = load_json(MANIFEST)

        self.assertEqual(1, manifest["schema_version"])
        self.assertEqual(COLLECTION_ID, manifest["collection_id"])
        self.assertEqual(TITLE, manifest["title"])
        self.assertEqual(REFERENCE_PACK_VERSION, manifest["reference_pack_version"])
        self.assertEqual(PROMPT_TEMPLATE_VERSION, manifest["prompt_template_version"])
        self.assertEqual(
            {
                "candidate_count": 8,
                "composition": "matched_bust_up",
                "primary_variation_axis": "eyes",
                "secondary_variation_axis": "organized_v1_1_short_bob",
                "hair_ornament_policy": "keep_character_left_pale_blue_pin",
                "pdf_policy": "not_in_this_phase",
            },
            manifest["batch_policy"],
        )

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
            [request["candidate_order"] for request in requests],
        )
        self.assertEqual(len(requests), len({request["id"] for request in requests}))

        for request, expected in zip(requests, EXPECTED_CANDIDATES, strict=True):
            with self.subTest(slot=request["slot"]):
                self.assertEqual(f"request:v1-2-face-hair-{expected['slot']}", request["id"])
                self.assertEqual(expected["title"], request["japanese_title"])
                self.assertTrue(JAPANESE_TEXT.search(request["japanese_title"]))
                self.assertEqual(expected["eye_variation"], request["eye_variation"])
                self.assertEqual(expected["hair_variation"], request["hair_variation"])
                self.assertEqual(REFERENCE_PACK_INPUTS, request["reference_pack_inputs"])
                self.assertEqual(
                    f"source/generated/v1-2-face-hair/{DATE_PREFIX}_{expected['slot']}_v1.png",
                    request["target_path"],
                )

    def test_prompts_lock_identity_and_keep_variation_narrow(self):
        for request in load_json(MANIFEST)["requests"]:
            prompt = request["prompt"]
            prompt_lower = prompt.lower()

            with self.subTest(slot=request["slot"]):
                for phrase in IDENTITY_LOCK_PHRASES:
                    self.assertIn(phrase, prompt)
                self.assertIn(request["eye_variation"], prompt)
                self.assertIn(request["hair_variation"], prompt)
                self.assertIn("same bust-up composition", prompt)
                self.assertIn("eyes are the primary design variable", prompt)
                self.assertIn("do not redesign the outfit", prompt)
                self.assertIn("do not make her photorealistic", prompt)
                self.assertIn("no readable text", prompt)
                self.assertIn("no logos", prompt)
                self.assertIn("no watermarks", prompt)

                for banned in BANNED_PROMPT_FRAGMENTS:
                    self.assertNotIn(banned, prompt_lower)

    def test_acceptance_and_review_gates_are_explicit(self):
        for request in load_json(MANIFEST)["requests"]:
            with self.subTest(slot=request["slot"]):
                acceptance = request["acceptance"]
                for phrase in REQUIRED_ACCEPTANCE_PHRASES:
                    self.assertIn(phrase, acceptance)

                self.assertEqual(
                    {
                        "appeal": "soft close memorable eyes, warm expression, immediate character charm",
                        "identity": "still reads as Akari v1.1 evolving into v1.2",
                        "hard_rejects": [
                            "long-hair drift",
                            "missing or flipped hair ornament",
                            "eye color drift",
                            "sharp cold generic eyes",
                            "extreme roundness that reads too young",
                            "photorealistic rendering",
                            "large mouth style change",
                            "pin-up expression",
                            "background or lighting hiding the face decision",
                        ],
                    },
                    request["selection_gates"],
                )
                self.assertEqual(
                    {
                        "identity_risk": "high",
                        "eye_drift_risk": "high",
                        "hair_drift_risk": "medium",
                        "age_impression_risk": "medium",
                        "text_logo_watermark_risk": "medium",
                    },
                    request["risk_profile"],
                )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
uv run python -m unittest tests.test_v1_2_face_hair_contract -v
```

Expected: FAIL because `.gitignore` lacks the new ignored working paths and
`source/manifests/v1-2-face-hair/generation-requests.json` does not exist.

- [ ] **Step 3: Add ignored generated and evidence paths**

Append these lines to `.gitignore`:

```gitignore
source/generated/v1-2-face-hair/
evidence/v1-2-face-hair/
```

- [ ] **Step 4: Run the test again to confirm only the manifest is missing**

Run:

```bash
uv run python -m unittest tests.test_v1_2_face_hair_contract -v
```

Expected: FAIL with a message containing:

```text
missing manifest:
```

## Task 2: Add The v1.2 Face/Hair Request Manifest

**Files:**

- Create: `source/manifests/v1-2-face-hair/generation-requests.json`
- Test: `tests/test_v1_2_face_hair_contract.py`

- [ ] **Step 1: Create the manifest**

Create `source/manifests/v1-2-face-hair/generation-requests.json`:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.2-face-hair",
  "title": "Akari v1.2 Face And Hair",
  "reference_pack_version": "akari-v1.1-face-hair-identity-v1",
  "prompt_template_version": "akari_v1_2_face_hair_eye_axis_v1",
  "batch_policy": {
    "candidate_count": 8,
    "composition": "matched_bust_up",
    "primary_variation_axis": "eyes",
    "secondary_variation_axis": "organized_v1_1_short_bob",
    "hair_ornament_policy": "keep_character_left_pale_blue_pin",
    "pdf_policy": "not_in_this_phase"
  },
  "requests": [
    {
      "id": "request:v1-2-face-hair-soft-horizontal-eyes",
      "candidate_order": 1,
      "slot": "soft-horizontal-eyes",
      "japanese_title": "柔らかい水平寄りの目",
      "eye_variation": "soft horizontal eyes with calm direct gaze",
      "hair_variation": "baseline organized short bob",
      "target_path": "source/generated/v1-2-face-hair/20260708_soft-horizontal-eyes_v1.png",
      "reference_pack_inputs": [
        "source/originals/v1_1_front_3.webp",
        "source/originals/v1_1_front_1.webp",
        "source/originals/v1_1_front_2.webp",
        "source/references/tonari-no-akari/identity-face-hair.webp"
      ],
      "prompt": "Create one clean bust-up Akari v1.2 face-and-hair design candidate. Akari v1.1 evolving into v1.2; adult early-20s Japanese young woman as character design, not realism; soft approachable innocence; warm brown eyes; warm brown short bob; soft bangs; pale blue hair ornament on Akari's character-left side; white oversized hoodie context. Use the same bust-up composition, neutral simple background, gentle front three-quarter feeling, and matched lighting across the whole set. For this candidate, the eyes are the primary design variable: soft horizontal eyes with calm direct gaze. Hair variation: baseline organized short bob. Keep the v1.1 short bob, clean bang groups, rounded side volume, and natural hair tips. Keep mouth small and restrained. Do not redesign the outfit, do not change eye color, do not make her photorealistic, do not make her sharper or colder, and do not make her underage or older-sister-like. No readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Appeal Gate: the eyes feel soft, close, memorable, and warm. Identity Gate: the image still reads as Akari v1.1 evolving into v1.2. Must be a matched bust-up candidate focused on face and hair. Must preserve warm brown eyes and hair, short bob, pale blue character-left hair ornament, small mouth, soft innocence, and white hoodie context. Must contain no readable text, no logos, no watermarks, no frame, and no panel layout.",
      "selection_gates": {
        "appeal": "soft close memorable eyes, warm expression, immediate character charm",
        "identity": "still reads as Akari v1.1 evolving into v1.2",
        "hard_rejects": [
          "long-hair drift",
          "missing or flipped hair ornament",
          "eye color drift",
          "sharp cold generic eyes",
          "extreme roundness that reads too young",
          "photorealistic rendering",
          "large mouth style change",
          "pin-up expression",
          "background or lighting hiding the face decision"
        ]
      },
      "risk_profile": {
        "identity_risk": "high",
        "eye_drift_risk": "high",
        "hair_drift_risk": "medium",
        "age_impression_risk": "medium",
        "text_logo_watermark_risk": "medium"
      }
    },
    {
      "id": "request:v1-2-face-hair-round-innocent-eyes",
      "candidate_order": 2,
      "slot": "round-innocent-eyes",
      "japanese_title": "少し丸くあどけない目",
      "eye_variation": "slightly rounder eyes with strong innocence",
      "hair_variation": "soft rounded bangs",
      "target_path": "source/generated/v1-2-face-hair/20260708_round-innocent-eyes_v1.png",
      "reference_pack_inputs": [
        "source/originals/v1_1_front_3.webp",
        "source/originals/v1_1_front_1.webp",
        "source/originals/v1_1_front_2.webp",
        "source/references/tonari-no-akari/identity-face-hair.webp"
      ],
      "prompt": "Create one clean bust-up Akari v1.2 face-and-hair design candidate. Akari v1.1 evolving into v1.2; adult early-20s Japanese young woman as character design, not realism; soft approachable innocence; warm brown eyes; warm brown short bob; soft bangs; pale blue hair ornament on Akari's character-left side; white oversized hoodie context. Use the same bust-up composition, neutral simple background, gentle front three-quarter feeling, and matched lighting across the whole set. For this candidate, the eyes are the primary design variable: slightly rounder eyes with strong innocence. Hair variation: soft rounded bangs. Keep the v1.1 short bob, clean bang groups, rounded side volume, and natural hair tips. Keep mouth small and restrained. Do not redesign the outfit, do not change eye color, do not make her photorealistic, do not make her sharper or colder, and do not make her underage or older-sister-like. No readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Appeal Gate: the eyes feel soft, close, memorable, and warm. Identity Gate: the image still reads as Akari v1.1 evolving into v1.2. Must be a matched bust-up candidate focused on face and hair. Must preserve warm brown eyes and hair, short bob, pale blue character-left hair ornament, small mouth, soft innocence, and white hoodie context. Must contain no readable text, no logos, no watermarks, no frame, and no panel layout.",
      "selection_gates": {
        "appeal": "soft close memorable eyes, warm expression, immediate character charm",
        "identity": "still reads as Akari v1.1 evolving into v1.2",
        "hard_rejects": [
          "long-hair drift",
          "missing or flipped hair ornament",
          "eye color drift",
          "sharp cold generic eyes",
          "extreme roundness that reads too young",
          "photorealistic rendering",
          "large mouth style change",
          "pin-up expression",
          "background or lighting hiding the face decision"
        ]
      },
      "risk_profile": {
        "identity_risk": "high",
        "eye_drift_risk": "high",
        "hair_drift_risk": "medium",
        "age_impression_risk": "medium",
        "text_logo_watermark_risk": "medium"
      }
    },
    {
      "id": "request:v1-2-face-hair-lowered-lid-gentle",
      "candidate_order": 3,
      "slot": "lowered-lid-gentle",
      "japanese_title": "まぶたに重みのある優しい目",
      "eye_variation": "gentle eyes with lowered eyelid weight",
      "hair_variation": "clean side hair framing",
      "target_path": "source/generated/v1-2-face-hair/20260708_lowered-lid-gentle_v1.png",
      "reference_pack_inputs": [
        "source/originals/v1_1_front_3.webp",
        "source/originals/v1_1_front_1.webp",
        "source/originals/v1_1_front_2.webp",
        "source/references/tonari-no-akari/identity-face-hair.webp"
      ],
      "prompt": "Create one clean bust-up Akari v1.2 face-and-hair design candidate. Akari v1.1 evolving into v1.2; adult early-20s Japanese young woman as character design, not realism; soft approachable innocence; warm brown eyes; warm brown short bob; soft bangs; pale blue hair ornament on Akari's character-left side; white oversized hoodie context. Use the same bust-up composition, neutral simple background, gentle front three-quarter feeling, and matched lighting across the whole set. For this candidate, the eyes are the primary design variable: gentle eyes with lowered eyelid weight. Hair variation: clean side hair framing. Keep the v1.1 short bob, clean bang groups, rounded side volume, and natural hair tips. Keep mouth small and restrained. Do not redesign the outfit, do not change eye color, do not make her photorealistic, do not make her sharper or colder, and do not make her underage or older-sister-like. No readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Appeal Gate: the eyes feel soft, close, memorable, and warm. Identity Gate: the image still reads as Akari v1.1 evolving into v1.2. Must be a matched bust-up candidate focused on face and hair. Must preserve warm brown eyes and hair, short bob, pale blue character-left hair ornament, small mouth, soft innocence, and white hoodie context. Must contain no readable text, no logos, no watermarks, no frame, and no panel layout.",
      "selection_gates": {
        "appeal": "soft close memorable eyes, warm expression, immediate character charm",
        "identity": "still reads as Akari v1.1 evolving into v1.2",
        "hard_rejects": [
          "long-hair drift",
          "missing or flipped hair ornament",
          "eye color drift",
          "sharp cold generic eyes",
          "extreme roundness that reads too young",
          "photorealistic rendering",
          "large mouth style change",
          "pin-up expression",
          "background or lighting hiding the face decision"
        ]
      },
      "risk_profile": {
        "identity_risk": "high",
        "eye_drift_risk": "high",
        "hair_drift_risk": "medium",
        "age_impression_risk": "medium",
        "text_logo_watermark_risk": "medium"
      }
    },
    {
      "id": "request:v1-2-face-hair-bright-catchlights",
      "candidate_order": 4,
      "slot": "bright-catchlights",
      "japanese_title": "光の入った温かい目",
      "eye_variation": "warm eyes with brighter catchlights",
      "hair_variation": "light bang grouping",
      "target_path": "source/generated/v1-2-face-hair/20260708_bright-catchlights_v1.png",
      "reference_pack_inputs": [
        "source/originals/v1_1_front_3.webp",
        "source/originals/v1_1_front_1.webp",
        "source/originals/v1_1_front_2.webp",
        "source/references/tonari-no-akari/identity-face-hair.webp"
      ],
      "prompt": "Create one clean bust-up Akari v1.2 face-and-hair design candidate. Akari v1.1 evolving into v1.2; adult early-20s Japanese young woman as character design, not realism; soft approachable innocence; warm brown eyes; warm brown short bob; soft bangs; pale blue hair ornament on Akari's character-left side; white oversized hoodie context. Use the same bust-up composition, neutral simple background, gentle front three-quarter feeling, and matched lighting across the whole set. For this candidate, the eyes are the primary design variable: warm eyes with brighter catchlights. Hair variation: light bang grouping. Keep the v1.1 short bob, clean bang groups, rounded side volume, and natural hair tips. Keep mouth small and restrained. Do not redesign the outfit, do not change eye color, do not make her photorealistic, do not make her sharper or colder, and do not make her underage or older-sister-like. No readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Appeal Gate: the eyes feel soft, close, memorable, and warm. Identity Gate: the image still reads as Akari v1.1 evolving into v1.2. Must be a matched bust-up candidate focused on face and hair. Must preserve warm brown eyes and hair, short bob, pale blue character-left hair ornament, small mouth, soft innocence, and white hoodie context. Must contain no readable text, no logos, no watermarks, no frame, and no panel layout.",
      "selection_gates": {
        "appeal": "soft close memorable eyes, warm expression, immediate character charm",
        "identity": "still reads as Akari v1.1 evolving into v1.2",
        "hard_rejects": [
          "long-hair drift",
          "missing or flipped hair ornament",
          "eye color drift",
          "sharp cold generic eyes",
          "extreme roundness that reads too young",
          "photorealistic rendering",
          "large mouth style change",
          "pin-up expression",
          "background or lighting hiding the face decision"
        ]
      },
      "risk_profile": {
        "identity_risk": "high",
        "eye_drift_risk": "high",
        "hair_drift_risk": "medium",
        "age_impression_risk": "medium",
        "text_logo_watermark_risk": "medium"
      }
    },
    {
      "id": "request:v1-2-face-hair-stable-narrower-eyes",
      "candidate_order": 5,
      "slot": "stable-narrower-eyes",
      "japanese_title": "少し細めで落ち着いた目",
      "eye_variation": "mildly narrower eyes with stable expression",
      "hair_variation": "organized bob volume",
      "target_path": "source/generated/v1-2-face-hair/20260708_stable-narrower-eyes_v1.png",
      "reference_pack_inputs": [
        "source/originals/v1_1_front_3.webp",
        "source/originals/v1_1_front_1.webp",
        "source/originals/v1_1_front_2.webp",
        "source/references/tonari-no-akari/identity-face-hair.webp"
      ],
      "prompt": "Create one clean bust-up Akari v1.2 face-and-hair design candidate. Akari v1.1 evolving into v1.2; adult early-20s Japanese young woman as character design, not realism; soft approachable innocence; warm brown eyes; warm brown short bob; soft bangs; pale blue hair ornament on Akari's character-left side; white oversized hoodie context. Use the same bust-up composition, neutral simple background, gentle front three-quarter feeling, and matched lighting across the whole set. For this candidate, the eyes are the primary design variable: mildly narrower eyes with stable expression. Hair variation: organized bob volume. Keep the v1.1 short bob, clean bang groups, rounded side volume, and natural hair tips. Keep mouth small and restrained. Do not redesign the outfit, do not change eye color, do not make her photorealistic, do not make her sharper or colder, and do not make her underage or older-sister-like. No readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Appeal Gate: the eyes feel soft, close, memorable, and warm. Identity Gate: the image still reads as Akari v1.1 evolving into v1.2. Must be a matched bust-up candidate focused on face and hair. Must preserve warm brown eyes and hair, short bob, pale blue character-left hair ornament, small mouth, soft innocence, and white hoodie context. Must contain no readable text, no logos, no watermarks, no frame, and no panel layout.",
      "selection_gates": {
        "appeal": "soft close memorable eyes, warm expression, immediate character charm",
        "identity": "still reads as Akari v1.1 evolving into v1.2",
        "hard_rejects": [
          "long-hair drift",
          "missing or flipped hair ornament",
          "eye color drift",
          "sharp cold generic eyes",
          "extreme roundness that reads too young",
          "photorealistic rendering",
          "large mouth style change",
          "pin-up expression",
          "background or lighting hiding the face decision"
        ]
      },
      "risk_profile": {
        "identity_risk": "high",
        "eye_drift_risk": "high",
        "hair_drift_risk": "medium",
        "age_impression_risk": "medium",
        "text_logo_watermark_risk": "medium"
      }
    },
    {
      "id": "request:v1-2-face-hair-shy-soft-gaze",
      "candidate_order": 6,
      "slot": "shy-soft-gaze",
      "japanese_title": "少し照れた柔らかい目線",
      "eye_variation": "soft eyes with slightly shy gaze",
      "hair_variation": "gentle hair-tip movement",
      "target_path": "source/generated/v1-2-face-hair/20260708_shy-soft-gaze_v1.png",
      "reference_pack_inputs": [
        "source/originals/v1_1_front_3.webp",
        "source/originals/v1_1_front_1.webp",
        "source/originals/v1_1_front_2.webp",
        "source/references/tonari-no-akari/identity-face-hair.webp"
      ],
      "prompt": "Create one clean bust-up Akari v1.2 face-and-hair design candidate. Akari v1.1 evolving into v1.2; adult early-20s Japanese young woman as character design, not realism; soft approachable innocence; warm brown eyes; warm brown short bob; soft bangs; pale blue hair ornament on Akari's character-left side; white oversized hoodie context. Use the same bust-up composition, neutral simple background, gentle front three-quarter feeling, and matched lighting across the whole set. For this candidate, the eyes are the primary design variable: soft eyes with slightly shy gaze. Hair variation: gentle hair-tip movement. Keep the v1.1 short bob, clean bang groups, rounded side volume, and natural hair tips. Keep mouth small and restrained. Do not redesign the outfit, do not change eye color, do not make her photorealistic, do not make her sharper or colder, and do not make her underage or older-sister-like. No readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Appeal Gate: the eyes feel soft, close, memorable, and warm. Identity Gate: the image still reads as Akari v1.1 evolving into v1.2. Must be a matched bust-up candidate focused on face and hair. Must preserve warm brown eyes and hair, short bob, pale blue character-left hair ornament, small mouth, soft innocence, and white hoodie context. Must contain no readable text, no logos, no watermarks, no frame, and no panel layout.",
      "selection_gates": {
        "appeal": "soft close memorable eyes, warm expression, immediate character charm",
        "identity": "still reads as Akari v1.1 evolving into v1.2",
        "hard_rejects": [
          "long-hair drift",
          "missing or flipped hair ornament",
          "eye color drift",
          "sharp cold generic eyes",
          "extreme roundness that reads too young",
          "photorealistic rendering",
          "large mouth style change",
          "pin-up expression",
          "background or lighting hiding the face decision"
        ]
      },
      "risk_profile": {
        "identity_risk": "high",
        "eye_drift_risk": "high",
        "hair_drift_risk": "medium",
        "age_impression_risk": "medium",
        "text_logo_watermark_risk": "medium"
      }
    },
    {
      "id": "request:v1-2-face-hair-v1-1-cleaner-eyes",
      "candidate_order": 7,
      "slot": "v1-1-cleaner-eyes",
      "japanese_title": "v1.1に近い整理された目",
      "eye_variation": "v1.1-near eyes with cleaner rendering",
      "hair_variation": "v1.1-near bob cleanup",
      "target_path": "source/generated/v1-2-face-hair/20260708_v1-1-cleaner-eyes_v1.png",
      "reference_pack_inputs": [
        "source/originals/v1_1_front_3.webp",
        "source/originals/v1_1_front_1.webp",
        "source/originals/v1_1_front_2.webp",
        "source/references/tonari-no-akari/identity-face-hair.webp"
      ],
      "prompt": "Create one clean bust-up Akari v1.2 face-and-hair design candidate. Akari v1.1 evolving into v1.2; adult early-20s Japanese young woman as character design, not realism; soft approachable innocence; warm brown eyes; warm brown short bob; soft bangs; pale blue hair ornament on Akari's character-left side; white oversized hoodie context. Use the same bust-up composition, neutral simple background, gentle front three-quarter feeling, and matched lighting across the whole set. For this candidate, the eyes are the primary design variable: v1.1-near eyes with cleaner rendering. Hair variation: v1.1-near bob cleanup. Keep the v1.1 short bob, clean bang groups, rounded side volume, and natural hair tips. Keep mouth small and restrained. Do not redesign the outfit, do not change eye color, do not make her photorealistic, do not make her sharper or colder, and do not make her underage or older-sister-like. No readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Appeal Gate: the eyes feel soft, close, memorable, and warm. Identity Gate: the image still reads as Akari v1.1 evolving into v1.2. Must be a matched bust-up candidate focused on face and hair. Must preserve warm brown eyes and hair, short bob, pale blue character-left hair ornament, small mouth, soft innocence, and white hoodie context. Must contain no readable text, no logos, no watermarks, no frame, and no panel layout.",
      "selection_gates": {
        "appeal": "soft close memorable eyes, warm expression, immediate character charm",
        "identity": "still reads as Akari v1.1 evolving into v1.2",
        "hard_rejects": [
          "long-hair drift",
          "missing or flipped hair ornament",
          "eye color drift",
          "sharp cold generic eyes",
          "extreme roundness that reads too young",
          "photorealistic rendering",
          "large mouth style change",
          "pin-up expression",
          "background or lighting hiding the face decision"
        ]
      },
      "risk_profile": {
        "identity_risk": "high",
        "eye_drift_risk": "high",
        "hair_drift_risk": "medium",
        "age_impression_risk": "medium",
        "text_logo_watermark_risk": "medium"
      }
    },
    {
      "id": "request:v1-2-face-hair-balanced-hybrid",
      "candidate_order": 8,
      "slot": "balanced-hybrid",
      "japanese_title": "強い要素を混ぜたバランス案",
      "eye_variation": "balanced hybrid candidate based on strongest prior traits",
      "hair_variation": "balanced organized short bob",
      "target_path": "source/generated/v1-2-face-hair/20260708_balanced-hybrid_v1.png",
      "reference_pack_inputs": [
        "source/originals/v1_1_front_3.webp",
        "source/originals/v1_1_front_1.webp",
        "source/originals/v1_1_front_2.webp",
        "source/references/tonari-no-akari/identity-face-hair.webp"
      ],
      "prompt": "Create one clean bust-up Akari v1.2 face-and-hair design candidate. Akari v1.1 evolving into v1.2; adult early-20s Japanese young woman as character design, not realism; soft approachable innocence; warm brown eyes; warm brown short bob; soft bangs; pale blue hair ornament on Akari's character-left side; white oversized hoodie context. Use the same bust-up composition, neutral simple background, gentle front three-quarter feeling, and matched lighting across the whole set. For this candidate, the eyes are the primary design variable: balanced hybrid candidate based on strongest prior traits. Hair variation: balanced organized short bob. Keep the v1.1 short bob, clean bang groups, rounded side volume, and natural hair tips. Keep mouth small and restrained. Do not redesign the outfit, do not change eye color, do not make her photorealistic, do not make her sharper or colder, and do not make her underage or older-sister-like. No readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Appeal Gate: the eyes feel soft, close, memorable, and warm. Identity Gate: the image still reads as Akari v1.1 evolving into v1.2. Must be a matched bust-up candidate focused on face and hair. Must preserve warm brown eyes and hair, short bob, pale blue character-left hair ornament, small mouth, soft innocence, and white hoodie context. Must contain no readable text, no logos, no watermarks, no frame, and no panel layout.",
      "selection_gates": {
        "appeal": "soft close memorable eyes, warm expression, immediate character charm",
        "identity": "still reads as Akari v1.1 evolving into v1.2",
        "hard_rejects": [
          "long-hair drift",
          "missing or flipped hair ornament",
          "eye color drift",
          "sharp cold generic eyes",
          "extreme roundness that reads too young",
          "photorealistic rendering",
          "large mouth style change",
          "pin-up expression",
          "background or lighting hiding the face decision"
        ]
      },
      "risk_profile": {
        "identity_risk": "high",
        "eye_drift_risk": "high",
        "hair_drift_risk": "medium",
        "age_impression_risk": "medium",
        "text_logo_watermark_risk": "medium"
      }
    }
  ]
}
```

- [ ] **Step 2: Run the contract test**

Run:

```bash
uv run python -m unittest tests.test_v1_2_face_hair_contract -v
```

Expected: PASS.

- [ ] **Step 3: Commit the request contract**

Run:

```bash
git add .gitignore tests/test_v1_2_face_hair_contract.py source/manifests/v1-2-face-hair/generation-requests.json
git commit -m "feat: add akari v1.2 face hair requests"
```

## Task 3: Add The v1.2 Contact Sheet Builder

**Files:**

- Create: `tests/test_v1_2_face_hair_contact_sheet.py`
- Create: `scripts/build_v1_2_face_hair_contact_sheet.py`
- Modify: `package.json`
- Test: `tests/test_v1_2_face_hair_contact_sheet.py`

- [ ] **Step 1: Write the failing contact sheet tests**

Create `tests/test_v1_2_face_hair_contact_sheet.py`:

```python
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.build_v1_2_face_hair_contact_sheet import (
    ROOT,
    build_contact_sheet,
    display_output_path,
    fit_text_to_width,
    label_lines_for,
    load_font,
    text_width,
)


class AkariV12FaceHairContactSheetTest(unittest.TestCase):
    def assertRgbClose(self, actual, expected, tolerance=5):
        for actual_channel, expected_channel in zip(actual[:3], expected):
            self.assertLessEqual(
                abs(actual_channel - expected_channel),
                tolerance,
                f"{actual[:3]} is not within {tolerance} of {expected}",
            )

    def test_build_contact_sheet_uses_existing_images_and_writes_sheet(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            generated_dir = temp_path / "source/generated/v1-2-face-hair"
            output_path = temp_path / "evidence/v1-2-face-hair/contact-sheets/sheet.webp"
            generated_dir.mkdir(parents=True)

            first_image = generated_dir / "20260708_soft-horizontal-eyes_v1.png"
            second_image = generated_dir / "20260708_round-innocent-eyes_v1.png"
            Image.new("RGB", (320, 320), "#d9eee9").save(first_image)
            Image.new("RGB", (320, 320), "#f0dfd1").save(second_image)

            requests = [
                {
                    "candidate_order": 1,
                    "slot": "soft-horizontal-eyes",
                    "japanese_title": "柔らかい水平寄りの目",
                    "eye_variation": "soft horizontal eyes with calm direct gaze",
                    "hair_variation": "baseline organized short bob",
                    "target_path": first_image.as_posix(),
                },
                {
                    "candidate_order": 2,
                    "slot": "round-innocent-eyes",
                    "japanese_title": "少し丸くあどけない目",
                    "eye_variation": "slightly rounder eyes with strong innocence",
                    "hair_variation": "soft rounded bangs",
                    "target_path": second_image.as_posix(),
                },
                {
                    "candidate_order": 3,
                    "slot": "missing",
                    "japanese_title": "未生成",
                    "eye_variation": "missing image",
                    "hair_variation": "missing image",
                    "target_path": (generated_dir / "missing.png").as_posix(),
                },
            ]

            result = build_contact_sheet(
                requests=requests,
                project_root=temp_path,
                output_path=output_path,
                columns=2,
                thumb_width=160,
                label_height=66,
                gap=12,
            )

            self.assertEqual(output_path, result)
            self.assertTrue(output_path.is_file())
            with Image.open(output_path) as sheet:
                self.assertEqual((356, 346), sheet.size)
                self.assertRgbClose(sheet.getpixel((20, 20)), (217, 238, 233))
                self.assertRgbClose(sheet.getpixel((192, 20)), (240, 223, 209))

    def test_build_contact_sheet_fails_when_no_images_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            with self.assertRaisesRegex(ValueError, "No generated v1.2 face/hair images found"):
                build_contact_sheet(
                    requests=[
                        {
                            "candidate_order": 1,
                            "slot": "missing",
                            "japanese_title": "未生成",
                            "eye_variation": "missing image",
                            "hair_variation": "missing image",
                            "target_path": "source/generated/v1-2-face-hair/missing.png",
                        }
                    ],
                    project_root=temp_path,
                    output_path=temp_path / "sheet.webp",
                    columns=2,
                    thumb_width=160,
                    label_height=66,
                    gap=12,
                )

    def test_build_contact_sheet_rejects_zero_columns(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            generated_dir = temp_path / "source/generated/v1-2-face-hair"
            generated_dir.mkdir(parents=True)
            image_path = generated_dir / "20260708_soft-horizontal-eyes_v1.png"
            Image.new("RGB", (320, 320), "#d9eee9").save(image_path)

            with self.assertRaisesRegex(ValueError, "columns must be at least 1"):
                build_contact_sheet(
                    requests=[
                        {
                            "candidate_order": 1,
                            "slot": "soft-horizontal-eyes",
                            "japanese_title": "柔らかい水平寄りの目",
                            "eye_variation": "soft horizontal eyes with calm direct gaze",
                            "hair_variation": "baseline organized short bob",
                            "target_path": image_path.as_posix(),
                        }
                    ],
                    project_root=temp_path,
                    output_path=temp_path / "sheet.webp",
                    columns=0,
                    thumb_width=160,
                    label_height=66,
                    gap=12,
                )

    def test_fit_text_to_width_truncates_long_text_with_ascii_ellipsis(self):
        font = load_font(16)
        max_width = 120
        text = "balanced hybrid candidate based on strongest prior traits"

        fitted = fit_text_to_width(text, font, max_width)

        self.assertNotEqual(text, fitted)
        self.assertTrue(fitted.endswith("..."))
        self.assertLessEqual(text_width(fitted, font), max_width)

    def test_load_font_renders_japanese_glyphs_distinctly(self):
        font = load_font(16)

        soft_mask = font.getmask("柔")
        eye_mask = font.getmask("目")

        self.assertNotEqual(
            (soft_mask.size, bytes(soft_mask)),
            (eye_mask.size, bytes(eye_mask)),
        )

    def test_real_contact_sheet_labels_fit_default_card_width(self):
        requests_path = ROOT / "source/manifests/v1-2-face-hair/generation-requests.json"
        with requests_path.open(encoding="utf-8") as requests_file:
            requests = json.load(requests_file)["requests"]
        font = load_font(16)
        small_font = load_font(12)
        max_width = 284

        for request in requests:
            with self.subTest(slot=request["slot"]):
                title_line, eye_line, hair_line = label_lines_for(
                    request,
                    font,
                    small_font,
                    max_width,
                )

                self.assertLessEqual(text_width(title_line, font), max_width)
                self.assertLessEqual(text_width(eye_line, small_font), max_width)
                self.assertLessEqual(text_width(hair_line, small_font), max_width)

    def test_display_output_path_prefers_repo_relative_path(self):
        path = ROOT / "evidence/v1-2-face-hair/contact-sheets/sheet.webp"

        self.assertEqual(
            "evidence/v1-2-face-hair/contact-sheets/sheet.webp",
            display_output_path(path),
        )

    def test_display_output_path_supports_external_absolute_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sheet.webp"

            self.assertEqual(path.as_posix(), display_output_path(path))

    def test_package_json_exposes_contact_sheet_script(self):
        package_json = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))

        self.assertEqual(
            "uv run python scripts/build_v1_2_face_hair_contact_sheet.py",
            package_json["scripts"]["build:v1-2-face-hair:contact-sheet"],
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
uv run python -m unittest tests.test_v1_2_face_hair_contact_sheet -v
```

Expected: FAIL with an import error for
`scripts.build_v1_2_face_hair_contact_sheet`.

- [ ] **Step 3: Add the contact sheet builder**

Create `scripts/build_v1_2_face_hair_contact_sheet.py`:

```python
#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REQUESTS_PATH = ROOT / "source/manifests/v1-2-face-hair/generation-requests.json"
DEFAULT_OUTPUT = (
    ROOT
    / "evidence/v1-2-face-hair/contact-sheets/akari-v1-2-face-hair-first-pass.webp"
)
BACKGROUND = "#f7f3ee"
CARD_BACKGROUND = "#ffffff"
TEXT = "#2b2b2b"
SUBTEXT = "#666666"
CJK_FONT_PATHS = (
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
)
LATIN_FALLBACK_FONT_PATHS = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
)


def load_requests(path: Path) -> list[dict]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    return manifest["requests"]


def resolve_candidate_path(project_root: Path, target_path: str) -> Path:
    path = Path(target_path)
    if path.is_absolute():
        return path
    return project_root / path


def load_font(size: int) -> ImageFont.ImageFont:
    for font_path in CJK_FONT_PATHS + LATIN_FALLBACK_FONT_PATHS:
        candidate = Path(font_path)
        if candidate.is_file():
            return ImageFont.truetype(candidate.as_posix(), size=size)
    return ImageFont.load_default()


def fit_image(image: Image.Image, thumb_width: int) -> Image.Image:
    image = image.convert("RGB")
    ratio = thumb_width / image.width
    thumb_height = int(round(image.height * ratio))
    return image.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)


def text_width(text: str, font: ImageFont.ImageFont) -> int:
    if hasattr(font, "getlength"):
        return math.ceil(font.getlength(text))
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]


def fit_text_to_width(text: str, font: ImageFont.ImageFont, max_width: int) -> str:
    if max_width <= 0:
        return ""
    if text_width(text, font) <= max_width:
        return text

    ellipsis = "..."
    if text_width(ellipsis, font) > max_width:
        return ""

    low = 0
    high = len(text)
    best = ellipsis
    while low <= high:
        midpoint = (low + high) // 2
        candidate = f"{text[:midpoint].rstrip()}{ellipsis}"
        if text_width(candidate, font) <= max_width:
            best = candidate
            low = midpoint + 1
        else:
            high = midpoint - 1
    return best


def label_lines_for(
    request: dict,
    font: ImageFont.ImageFont,
    small_font: ImageFont.ImageFont,
    max_width: int,
) -> tuple[str, str, str]:
    title = f"{request['candidate_order']}. {request['japanese_title']}"
    eye = f"eye: {request['eye_variation']}"
    hair = f"hair: {request['hair_variation']}"
    return (
        fit_text_to_width(title, font, max_width),
        fit_text_to_width(eye, small_font, max_width),
        fit_text_to_width(hair, small_font, max_width),
    )


def draw_label(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    request: dict,
    font: ImageFont.ImageFont,
    small_font: ImageFont.ImageFont,
    max_width: int,
) -> None:
    x, y = xy
    title, eye, hair = label_lines_for(request, font, small_font, max_width)
    draw.text((x, y), title, fill=TEXT, font=font)
    draw.text((x, y + 22), eye, fill=SUBTEXT, font=small_font)
    draw.text((x, y + 40), hair, fill=SUBTEXT, font=small_font)


def existing_request_images(requests: list[dict], project_root: Path) -> list[tuple[dict, Path]]:
    found = []
    for request in requests:
        image_path = resolve_candidate_path(project_root, request["target_path"])
        if image_path.is_file():
            found.append((request, image_path))
    return found


def display_output_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def build_contact_sheet(
    requests: list[dict],
    project_root: Path,
    output_path: Path,
    columns: int = 4,
    thumb_width: int = 300,
    label_height: int = 78,
    gap: int = 20,
) -> Path:
    if columns < 1:
        raise ValueError("columns must be at least 1")

    found = existing_request_images(requests, project_root)
    if not found:
        raise ValueError("No generated v1.2 face/hair images found")

    prepared = []
    for request, image_path in found:
        with Image.open(image_path) as image:
            thumbnail = fit_image(image, thumb_width)
        prepared.append((request, thumbnail))

    thumb_height = max(thumbnail.height for _, thumbnail in prepared)
    card_width = thumb_width
    card_height = thumb_height + label_height
    rows = math.ceil(len(prepared) / columns)
    sheet_width = columns * card_width + (columns + 1) * gap
    sheet_height = rows * card_height + (rows + 1) * gap
    sheet = Image.new("RGB", (sheet_width, sheet_height), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    font = load_font(16)
    small_font = load_font(12)
    label_text_width = card_width - 16

    for index, (request, thumbnail) in enumerate(prepared):
        row = index // columns
        column = index % columns
        x = gap + column * (card_width + gap)
        y = gap + row * (card_height + gap)
        draw.rectangle((x, y, x + card_width, y + card_height), fill=CARD_BACKGROUND)
        image_y = y
        if thumbnail.height < thumb_height:
            image_y += (thumb_height - thumbnail.height) // 2
        sheet.paste(thumbnail, (x, image_y))
        draw_label(
            draw,
            (x + 8, y + thumb_height + 6),
            request,
            font,
            small_font,
            label_text_width,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=92)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a contact sheet for Akari v1.2 face/hair candidates."
    )
    parser.add_argument("--requests", type=Path, default=REQUESTS_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--columns", type=int, default=4)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requests = load_requests(args.requests)
    output_path = args.output
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    result = build_contact_sheet(
        requests=requests,
        project_root=ROOT,
        output_path=output_path,
        columns=args.columns,
    )
    print(f"Wrote {display_output_path(result)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Add the package script**

Modify `package.json` and add this entry under `scripts` after
`build:coordinate:contact-sheet`:

```json
"build:v1-2-face-hair:contact-sheet": "uv run python scripts/build_v1_2_face_hair_contact_sheet.py"
```

- [ ] **Step 5: Run contact sheet tests**

Run:

```bash
uv run python -m unittest tests.test_v1_2_face_hair_contact_sheet -v
```

Expected: PASS.

- [ ] **Step 6: Run both v1.2 Python tests**

Run:

```bash
uv run python -m unittest tests.test_v1_2_face_hair_contract tests.test_v1_2_face_hair_contact_sheet -v
```

Expected: PASS.

- [ ] **Step 7: Commit the contact sheet tooling**

Run:

```bash
git add package.json tests/test_v1_2_face_hair_contact_sheet.py scripts/build_v1_2_face_hair_contact_sheet.py
git commit -m "feat: add akari v1.2 face hair contact sheet"
```

## Task 4: Generate The Eight Matched Bust-Up Candidates

**Files:**

- Read: `source/manifests/v1-2-face-hair/generation-requests.json`
- Create working files:
  `source/generated/v1-2-face-hair/20260708_<slot>_v1.png`
- Create working file:
  `evidence/v1-2-face-hair/contact-sheets/akari-v1-2-face-hair-first-pass.webp`

- [ ] **Step 1: Prepare ignored working directories**

Run:

```bash
mkdir -p source/generated/v1-2-face-hair evidence/v1-2-face-hair/contact-sheets
```

Expected: command exits 0.

- [ ] **Step 2: Print the eight generation prompts**

Run:

```bash
uv run python - <<'PY'
import json
from pathlib import Path

manifest = json.loads(
    Path("source/manifests/v1-2-face-hair/generation-requests.json").read_text(
        encoding="utf-8"
    )
)
for request in manifest["requests"]:
    print("=" * 72)
    print(request["slot"])
    print(request["target_path"])
    print(request["prompt"])
PY
```

Expected: eight sections print, one per slot, with target paths under
`source/generated/v1-2-face-hair/`.

- [ ] **Step 3: Generate each candidate**

For each request printed in Step 2, call the built-in `image_gen` tool with
the exact `prompt` value from the manifest. Save each returned image to that
request's `target_path`.

Use these save paths:

```text
source/generated/v1-2-face-hair/20260708_soft-horizontal-eyes_v1.png
source/generated/v1-2-face-hair/20260708_round-innocent-eyes_v1.png
source/generated/v1-2-face-hair/20260708_lowered-lid-gentle_v1.png
source/generated/v1-2-face-hair/20260708_bright-catchlights_v1.png
source/generated/v1-2-face-hair/20260708_stable-narrower-eyes_v1.png
source/generated/v1-2-face-hair/20260708_shy-soft-gaze_v1.png
source/generated/v1-2-face-hair/20260708_v1-1-cleaner-eyes_v1.png
source/generated/v1-2-face-hair/20260708_balanced-hybrid_v1.png
```

If the UI displays images but no PNG files appear, recover the payload from
the current Codex session as described in `AGENTS.md`. Confirm each recovered
PNG starts with this signature:

```text
89504e470d0a1a0a
```

- [ ] **Step 4: Verify all eight generated files exist and are readable**

Run:

```bash
uv run python - <<'PY'
import json
from pathlib import Path
from PIL import Image

manifest = json.loads(
    Path("source/manifests/v1-2-face-hair/generation-requests.json").read_text(
        encoding="utf-8"
    )
)
missing = []
for request in manifest["requests"]:
    path = Path(request["target_path"])
    if not path.is_file():
        missing.append(path.as_posix())
        continue
    with Image.open(path) as image:
        print(f"{path.as_posix()} {image.size[0]}x{image.size[1]} {image.mode}")

if missing:
    raise SystemExit("missing generated files: " + ", ".join(missing))
PY
```

Expected: eight image lines print and the command exits 0.

- [ ] **Step 5: Build the contact sheet**

Run:

```bash
npm run build:v1-2-face-hair:contact-sheet
```

Expected:

```text
Wrote evidence/v1-2-face-hair/contact-sheets/akari-v1-2-face-hair-first-pass.webp
```

- [ ] **Step 6: Confirm generated artifacts remain untracked**

Run:

```bash
git status --short --ignored source/generated/v1-2-face-hair evidence/v1-2-face-hair
```

Expected: generated images and contact sheets appear as ignored files, with
`!!` prefixes.

## Task 4R: Add A Reference-Locked Pilot Before Review

**Files:**

- Modify: `source/manifests/v1-2-face-hair/generation-requests.json`
- Create working file:
  `source/generated/v1-2-face-hair/reference-pilot/20260708_soft-horizontal-eyes_ref-v1.png`

- [ ] **Step 1: Record the text-only batch as rejected exploration evidence**

Keep the existing text-only images and first-pass contact sheet under ignored
paths. Do not use them as selection candidates because the user found them too
dissimilar to Akari v1.1.

- [ ] **Step 2: Tighten the first request prompt for reference use**

Update the `soft-horizontal-eyes` request prompt so it starts with this
reference instruction:

```text
Use the visible reference images as identity references. Reference image 1 is the primary Akari v1.1 face identity; reference images 2 and 3 are auxiliary face consistency checks. Preserve the same character identity, face proportions, warm brown eye color, short brown bob mass, small mouth scale, and pale blue character-left hair ornament before making any v1.2 refinement.
```

Keep the existing eye variation:

```text
soft horizontal eyes with calm direct gaze
```

- [ ] **Step 3: Load the reference images into context**

Open these images with `view_image` before calling `image_gen`:

```text
source/originals/v1_1_front_3.webp
source/originals/v1_1_front_1.webp
source/originals/v1_1_front_2.webp
```

Label their roles in the prompt:

```text
Image 1: primary Akari v1.1 face identity reference.
Image 2: auxiliary v1.1 face and softness reference.
Image 3: auxiliary v1.1 face and hair-balance reference.
```

- [ ] **Step 4: Generate one pilot only**

Call built-in `image_gen` once with the tightened `soft-horizontal-eyes`
prompt. Save the result to:

```text
source/generated/v1-2-face-hair/reference-pilot/20260708_soft-horizontal-eyes_ref-v1.png
```

- [ ] **Step 5: Verify the pilot file**

Run:

```bash
uv run python - <<'PY'
from pathlib import Path
from PIL import Image

path = Path(
    "source/generated/v1-2-face-hair/reference-pilot/"
    "20260708_soft-horizontal-eyes_ref-v1.png"
)
if not path.is_file():
    raise SystemExit(f"missing pilot: {path}")
with Image.open(path) as image:
    print(f"{path.as_posix()} {image.size[0]}x{image.size[1]} {image.mode}")
PY
```

Expected: one image line prints and the command exits 0.

- [ ] **Step 6: Present the pilot for identity review**

Show the pilot image to the user and ask whether it is close enough to Akari
v1.1 to regenerate the full eight-image batch using the same reference-locked
method. Do not regenerate the full set until the user approves the pilot.

- [ ] **Step 7: If the first pilot is rejected, run a stronger v2 pilot**

If the first reference pilot is still too dissimilar, add
`source/originals/v1_1_髪飾り側_45deg.webp` as the strict hair-ornament and
side-hair reference. Use a stronger prompt that hard-bans flower accessory
drift, darker generic bob hair, sharper mature face proportions, and large
glossy mouth rendering. Save only one v2 pilot to:

```text
source/generated/v1-2-face-hair/reference-pilot/20260708_soft-horizontal-eyes_ref-v2.png
```

Show the v2 pilot to the user before regenerating any eight-image batch.

- [ ] **Step 8: If original references still drift, run a Hyoujou v1 pilot**

Use these existing bust-up expression images as the face-family references:

```text
source/generated/tonari-no-hyoujou/20260703_called-turn_v2.webp
source/generated/tonari-no-hyoujou/20260703_eye-contact-pause_v1.webp
source/generated/tonari-no-hyoujou/20260706_extra-02_prank-smug_v5.webp
```

Generate only one pilot and save it to:

```text
source/generated/v1-2-face-hair/reference-pilot/20260708_soft-horizontal-eyes_hyoujou-v1.png
```

Show this pilot to the user before regenerating any eight-image batch.

## Task 5: Run The First-Pass Selection Review

**Files:**

- Read:
  `evidence/v1-2-face-hair/contact-sheets/akari-v1-2-face-hair-first-pass.webp`
- Create working file:
  `evidence/v1-2-face-hair/reviews/20260708-first-pass-review.json`

- [ ] **Step 1: Inspect the contact sheet**

Open:

```text
evidence/v1-2-face-hair/contact-sheets/akari-v1-2-face-hair-first-pass.webp
```

Review all eight candidates against these gates:

```text
Appeal: immediate character charm; soft, close, memorable eyes; warm expression.
Identity: reads as Akari v1.1 evolving into v1.2; warm brown eyes and hair; short bob; character-left pale blue hair ornament.
Hard rejects: long hair, missing or flipped ornament, eye-color drift, cold generic eyes, too-young roundness, photorealism, large mouth style shift, pin-up expression, distracting background or lighting.
```

- [ ] **Step 2: Write the review JSON**

Create `evidence/v1-2-face-hair/reviews/20260708-first-pass-review.json`
after inspection. Use these exact top-level keys and write concrete observed
notes for every candidate:

```text
review_id: akari-v1.2-face-hair-first-pass-20260708
source_manifest: source/manifests/v1-2-face-hair/generation-requests.json
contact_sheet: evidence/v1-2-face-hair/contact-sheets/akari-v1-2-face-hair-first-pass.webp
review_mode: appeal_and_identity_first_pass
states: ["accept", "hold", "reject"]
candidates: one object per manifest slot, in manifest order
overall_recommendation: lead candidate, secondary candidates, reusable traits, and next prompt adjustment
```

Each candidate object must contain:

```text
slot: the manifest slot
state: accept, hold, or reject
appeal_notes: non-empty visual observation about eye charm and warmth
identity_notes: non-empty visual observation about Akari continuity
rejection_reason: non-empty only when state is reject
reusable_traits: array of concrete eye or hair traits worth carrying forward
```

`overall_recommendation.lead_candidate` must be one manifest slot or `none`.
`overall_recommendation.secondary_candidates` must contain only manifest slots.
`overall_recommendation.combine_traits` must name concrete visual ingredients.
`overall_recommendation.next_prompt_adjustment` must be a non-empty sentence.

- [ ] **Step 3: Validate the review JSON shape**

Run:

```bash
uv run python - <<'PY'
import json
from pathlib import Path

manifest = json.loads(
    Path("source/manifests/v1-2-face-hair/generation-requests.json").read_text(
        encoding="utf-8"
    )
)
review = json.loads(
    Path("evidence/v1-2-face-hair/reviews/20260708-first-pass-review.json").read_text(
        encoding="utf-8"
    )
)
slots = [request["slot"] for request in manifest["requests"]]
review_slots = [candidate["slot"] for candidate in review["candidates"]]
if review_slots != slots:
    raise SystemExit(f"review slots do not match manifest: {review_slots}")
for candidate in review["candidates"]:
    if candidate["state"] not in review["states"]:
        raise SystemExit(f"invalid state for {candidate['slot']}: {candidate['state']}")
    if not candidate["appeal_notes"].strip():
        raise SystemExit(f"missing appeal notes for {candidate['slot']}")
    if not candidate["identity_notes"].strip():
        raise SystemExit(f"missing identity notes for {candidate['slot']}")
    if candidate["state"] == "reject" and not candidate["rejection_reason"]:
        raise SystemExit(f"missing rejection reason for {candidate['slot']}")
    if not isinstance(candidate["reusable_traits"], list):
        raise SystemExit(f"reusable traits must be a list for {candidate['slot']}")
recommendation = review["overall_recommendation"]
lead_candidate = recommendation["lead_candidate"]
if lead_candidate != "none" and lead_candidate not in slots:
    raise SystemExit(f"invalid lead candidate: {lead_candidate}")
invalid_secondary = [
    slot for slot in recommendation["secondary_candidates"] if slot not in slots
]
if invalid_secondary:
    raise SystemExit(f"invalid secondary candidates: {invalid_secondary}")
if not recommendation["next_prompt_adjustment"].strip():
    raise SystemExit("missing next prompt adjustment")
print("review JSON ok")
PY
```

Expected:

```text
review JSON ok
```

- [ ] **Step 4: Present the contact sheet and review to the user**

Show the user the contact sheet and summarize:

- strongest candidate by appeal
- strongest candidate by v1.1 identity continuity
- any hard rejects
- reusable eye traits
- reusable hair traits
- recommended next prompt adjustment

Ask the user to choose one of these:

```text
1. Pick a lead candidate and extract v1.2 face/hair rules.
2. Regenerate a second eight-candidate batch using the strongest traits.
3. Narrow to two or three candidates and generate close variants.
```

## Task 6: Final Verification For Committed Tooling

**Files:**

- Read: all files changed in Tasks 1 through 3

- [ ] **Step 1: Run targeted Python tests**

Run:

```bash
uv run python -m unittest tests.test_v1_2_face_hair_contract tests.test_v1_2_face_hair_contact_sheet -v
```

Expected: PASS.

- [ ] **Step 2: Run the full Python test suite**

Run:

```bash
npm run test:python
```

Expected: PASS.

- [ ] **Step 3: Run Markdown lint**

Run:

```bash
npm run lint:md
```

Expected: PASS, or a failure caused only by pre-existing ignored worktree
content. If it fails, rerun this targeted command and record both outputs:

```bash
npx markdownlint-cli2 docs/superpowers/plans/2026-07-08-akari-v1-2-face-hair.md docs/superpowers/specs/2026-07-08-akari-v1-2-face-hair-design.md
```

Expected targeted result: 0 errors.

- [ ] **Step 4: Check for whitespace errors**

Run:

```bash
git diff --check
```

Expected: no output and exit 0.

- [ ] **Step 5: Check git status**

Run:

```bash
git status --short
```

Expected: only committed tooling changes are clean; generated v1.2 images and
evidence are ignored.

## Plan Self-Review

Spec coverage:

- Face/hair-only scope is covered by the request manifest and ignored v1.2
  working paths.
- Eight matched bust-up candidates are covered by the manifest contract and
  Task 4 generation list.
- Reference-locked recovery after text-only identity drift is covered by
  Task 4R's one-image pilot gate.
- Eyes as the primary axis are covered by per-request `eye_variation` values
  and prompt contract assertions.
- Organized v1.1 short bob and pale blue character-left ornament are covered
  by prompt and acceptance assertions.
- Appeal plus identity selection is covered by the `selection_gates` contract
  and Task 5 review flow.
- No PDF update is covered by `pdf_policy: not_in_this_phase` and the absence
  of PDF renderer changes.

Three local-rule checks:

- Minimality: the committed surface is limited to `.gitignore`, one manifest,
  two tests, one contact-sheet script, and one package script.
- Existing pattern fit: tests use `unittest`; scripts follow the existing
  `build_tonari_no_coordinate_contact_sheet.py` Pillow pattern.
- Edge verification: contract tests catch prompt drift, path drift, missing
  reference inputs, missing ignore entries, label overflow, unreadable images,
  and review JSON shape errors.
