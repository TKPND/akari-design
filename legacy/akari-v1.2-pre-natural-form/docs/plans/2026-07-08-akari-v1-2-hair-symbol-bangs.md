# Akari v1.2 Hair Symbol And Bangs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a focused four-candidate Y1 follow-up set that adjusts only Akari v1.2's hair ornament, bangs, and subtle face-framing bob softness.

**Architecture:** Keep the selected Y1 face direction locked and model this as a sibling generation manifest, not an expansion of the original eight-candidate face exploration. Reuse the existing v1.2 contact-sheet builder by giving it a separate manifest with the same `requests` shape. Generated images and evidence stay ignored; the corrected contract, manifest, design spec, and this plan are tracked now, while any selection record remains deferred until user review.

**Tech Stack:** Python 3.11, `unittest`, JSON manifests, Pillow contact-sheet tooling, built-in image generation, `uv run python`, existing npm scripts.

---

## Scope Check

The approved spec covers one narrow follow-up: hair-symbol and bang refinement
from the already selected Y1 standard-face hold candidate. This plan does not
reopen face design, age direction, outfit, pose, PDF layout, or broad v1.2
production work.

## Current Context

### 2026-07-10 Two-Part Ornament Correction

The first four `_v1.png` candidates are identity-invalid because the old
contract allowed an X-only ornament. Preserve those files and build
`akari-v1-2-hair-symbol-bangs-y1-failed-v1.webp` from the untouched v1 manifest
before switching active targets. The corrected generation contract requires
small pale-blue crossed X-shaped hairpins above a compact pale-blue ribbon-like
loop with two thin trailing strands. Both parts stay character-left as one
compact v1.1 ornament; active replacements use `_v2.png` paths. Every v2
prompt also preserves the exact same crop, pose, background layout, and aspect
ratio as the Y1 primary source.

- Approved design spec:
  `docs/superpowers/specs/2026-07-08-akari-v1-2-hair-symbol-bangs-design.md`
- Current Y1 face lock:
  `source/generated/v1-2-face-hair/free-reference-batch-younger-base05/20260708_base05-younger-01.png`
- Existing v1.2 face-and-hair manifest:
  `source/manifests/v1-2-face-hair/generation-requests.json`
- Existing v1.2 contact-sheet builder:
  `scripts/build_v1_2_face_hair_contact_sheet.py`
- Strict v1.1 ornament-side reference:
  `source/originals/v1_1_髪飾り側_45deg.webp`
- Face-family support reference:
  `source/generated/tonari-no-hyoujou/20260703_called-turn_v2.webp`

## File Structure

- Create `tests/test_v1_2_hair_symbol_bangs_contract.py`
  - Contract tests for the Y1 follow-up request manifest, locked source image,
    four slot names, reference inputs, prompt bans, acceptance gates, and future
    selection-note schema.
- Create `source/manifests/v1-2-face-hair/hair-symbol-bangs-y1-requests.json`
  - Sibling manifest for the four Y1 hair-symbol/bang variants.
- Use existing `scripts/build_v1_2_face_hair_contact_sheet.py`
  - No source change required. It already accepts `--requests` and can read a
    sibling manifest with a top-level `requests` array.
- Working-only output paths:
  - `source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_ornament-lock_v2.png`
  - `source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_bang-texture_v2.png`
  - `source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_side-frame-softness_v2.png`
  - `source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_balanced-symbol-bangs_v2.png`
  - `evidence/v1-2-face-hair/contact-sheets/akari-v1-2-hair-symbol-bangs-y1-v2.webp`
- Preserved failed-v1 evidence:
  - `source/generated/v1-2-face-hair/hair-symbol-bangs-y1/*_v1.png`
  - `evidence/v1-2-face-hair/contact-sheets/akari-v1-2-hair-symbol-bangs-y1-failed-v1.webp`

## Data Model

Use this sibling manifest shape:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.2-hair-symbol-bangs-y1",
  "title": "Akari v1.2 Hair Symbol And Bangs Y1",
  "source_lock": {
    "source_axis": "source/generated/v1-2-face-hair/free-reference-batch-younger-base05/20260708_base05-younger-01.png",
    "age_impression": "early-20s university-age young adult; still not underage",
    "locked_traits": [
      "Y1 face direction",
      "gentle eye read",
      "small restrained mouth",
      "white hoodie context"
    ]
  },
  "batch_policy": {
    "candidate_count": 4,
    "composition": "matched_bust_up",
    "primary_variation_axis": "hair_symbol_and_bangs",
    "face_policy": "lock_y1_face_direction",
    "pdf_policy": "not_in_this_step"
  },
  "requests": [],
  "selection_notes": []
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
- `reference_inputs`
- `prompt`
- `acceptance`
- `selection_gates`
- `risk_profile`

## Correction Preflight: Preserve The Failed v1 Batch

Before changing any manifest target path, build the ignored failed-v1 sheet
from the original manifest and four existing `_v1.png` files:

```bash
uv run python scripts/build_v1_2_face_hair_contact_sheet.py \
  --requests source/manifests/v1-2-face-hair/hair-symbol-bangs-y1-requests.json \
  --output evidence/v1-2-face-hair/contact-sheets/akari-v1-2-hair-symbol-bangs-y1-failed-v1.webp \
  --columns 4
git status --short --ignored \
  source/generated/v1-2-face-hair/hair-symbol-bangs-y1 \
  evidence/v1-2-face-hair/contact-sheets/akari-v1-2-hair-symbol-bangs-y1-failed-v1.webp
```

Expected: the sheet is written, the four `_v1.png` files remain unchanged,
and both generated locations report as ignored.

## Task 1: Strengthen The Hair-Symbol/Bangs Contract Test

**Files:**

- Modify: `tests/test_v1_2_hair_symbol_bangs_contract.py`

- [ ] **Step 1: Write the failing two-part contract test**

Update `tests/test_v1_2_hair_symbol_bangs_contract.py`:

```python
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / (
    "source/manifests/v1-2-face-hair/"
    "hair-symbol-bangs-y1-requests.json"
)
PLAN = (
    ROOT
    / "docs/superpowers/plans/2026-07-08-akari-v1-2-hair-symbol-bangs.md"
)
Y1_SOURCE = (
    "source/generated/v1-2-face-hair/free-reference-batch-younger-base05/"
    "20260708_base05-younger-01.png"
)
REFERENCE_INPUTS = [
    Y1_SOURCE,
    "source/originals/v1_1_髪飾り側_45deg.webp",
    "source/originals/v1_1_front_3.webp",
    "source/generated/tonari-no-hyoujou/20260703_called-turn_v2.webp",
]
TRACKED_REFERENCE_INPUTS = REFERENCE_INPUTS[1:]
EXPECTED_SLOTS = [
    {
        "slot": "ornament-lock",
        "title": "髪飾り固定",
        "hair_variation": "restore the small pale blue v1.1 hair ornament shape",
    },
    {
        "slot": "bang-texture",
        "title": "前髪の束感",
        "hair_variation": "add v1.1-like soft uneven bang grouping",
    },
    {
        "slot": "side-frame-softness",
        "title": "サイド髪の柔らかさ",
        "hair_variation": "soften cheek-side short bob framing",
    },
    {
        "slot": "balanced-symbol-bangs",
        "title": "髪記号と前髪のバランス",
        "hair_variation": "balance ornament lock, bang texture, and side framing",
    },
]
REQUIRED_PROMPT_PHRASES = [
    "Use the Y1 image as the locked face source",
    "do not change her eyes",
    "do not change her mouth",
    "do not change her age impression",
    "early-20s university-age young adult",
    "Preserve the exact same crop, pose, background layout, and aspect ratio as the Y1 primary source",
    "pale blue character-left hair ornament",
    "small pale-blue crossed X-shaped hairpins",
    "compact pale-blue ribbon-like loop immediately below",
    "two thin trailing strands",
    "both stay on Akari's character-left side as one compact v1.1 identity ornament",
    "missing upper or lower component",
    "wrong-side placement",
    "flower, petal, or flower-center drift",
    "jewel or gemstone drift",
    "oversized fashion bow",
    "large dangling ribbon",
    "v1.1-like bang grouping",
    "matched bust-up composition",
    "no readable text",
    "no logos",
    "no watermarks",
]
BANNED_PROMPT_FRAGMENTS = [
    "school uniform",
    "teenage",
    "little girl",
    "child body",
    "pin-up",
    "glamour model",
    "photorealistic",
    "new outfit",
]
BANNED_CONTRACT_PHRASES = [
    "not a bow",
    "no bows",
    "reject bows",
    "not a ribbon",
    "no ribbons",
    "reject ribbons",
    "ribbon ornament drift",
    "must stay flat and pin-like",
    "small pale blue crossed-pin / two-stroke hairpin symbol",
]
REQUIRED_HARD_REJECTS = [
    "missing upper crossed X-shaped hairpins",
    "missing lower ribbon-like loop or either trailing strand",
    "wrong-side hair ornament",
    "flower, petal, or flower-center ornament drift",
    "jewel or gemstone ornament drift",
    "oversized fashion bow",
    "large dangling ribbon",
]
PLAN_REQUIRED_SNIPPET_PHRASES = [
    "expected_size = y1_image.size",
    "if image.size != expected_size:",
    "does not match Y1 source dimensions",
]


def load_json(path):
    with path.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


class AkariV12HairSymbolBangsContractTest(unittest.TestCase):
    def test_manifest_exists_and_records_y1_source_lock(self):
        self.assertTrue(MANIFEST.is_file(), f"missing manifest: {MANIFEST}")
        manifest = load_json(MANIFEST)

        self.assertEqual(1, manifest["schema_version"])
        self.assertEqual(
            "akari-v1.2-hair-symbol-bangs-y1",
            manifest["collection_id"],
        )
        self.assertEqual("Akari v1.2 Hair Symbol And Bangs Y1", manifest["title"])
        self.assertEqual(Y1_SOURCE, manifest["source_lock"]["source_axis"])
        self.assertIn(
            "early-20s university-age young adult",
            manifest["source_lock"]["age_impression"],
        )
        self.assertIn("still not underage", manifest["source_lock"]["age_impression"])
        self.assertEqual(
            [
                "Y1 face direction",
                "gentle eye read",
                "small restrained mouth",
                "white hoodie context",
            ],
            manifest["source_lock"]["locked_traits"],
        )
        self.assertEqual(
            {
                "candidate_count": 4,
                "composition": "matched_bust_up",
                "primary_variation_axis": "hair_symbol_and_bangs",
                "face_policy": "lock_y1_face_direction",
                "pdf_policy": "not_in_this_step",
            },
            manifest["batch_policy"],
        )

    def test_tracked_reference_inputs_exist(self):
        for reference_path in TRACKED_REFERENCE_INPUTS:
            with self.subTest(reference_path=reference_path):
                self.assertTrue((ROOT / reference_path).is_file())

    def test_y1_source_lock_points_to_ignored_working_image(self):
        manifest = load_json(MANIFEST)

        self.assertEqual(Y1_SOURCE, manifest["source_lock"]["source_axis"])
        self.assertIn(
            "source/generated/v1-2-face-hair/",
            manifest["source_lock"]["source_axis"],
        )

    def test_manifest_has_four_ordered_followup_candidates(self):
        requests = load_json(MANIFEST)["requests"]

        self.assertEqual(4, len(requests))
        self.assertEqual(
            [expected["slot"] for expected in EXPECTED_SLOTS],
            [request["slot"] for request in requests],
        )
        self.assertEqual(
            [1, 2, 3, 4],
            [request["candidate_order"] for request in requests],
        )
        self.assertEqual(len(requests), len({request["id"] for request in requests}))

        for request, expected in zip(requests, EXPECTED_SLOTS, strict=True):
            with self.subTest(slot=request["slot"]):
                self.assertEqual(
                    f"request:v1-2-hair-symbol-bangs-y1-{expected['slot']}",
                    request["id"],
                )
                self.assertEqual(expected["title"], request["japanese_title"])
                self.assertEqual("locked Y1 face; no eye redesign", request["eye_variation"])
                self.assertEqual(expected["hair_variation"], request["hair_variation"])
                self.assertEqual(REFERENCE_INPUTS, request["reference_inputs"])
                self.assertEqual(
                    (
                        "source/generated/v1-2-face-hair/hair-symbol-bangs-y1/"
                        f"20260708_{expected['slot']}_v2.png"
                    ),
                    request["target_path"],
                )

    def test_live_and_documented_prompts_lock_face_and_ban_symbol_drift(self):
        for request in load_json(MANIFEST)["requests"]:
            prompt = request["prompt"]
            prompt_lower = prompt.lower()

            with self.subTest(slot=request["slot"]):
                self.assertIn(request["hair_variation"], prompt)
                for phrase in REQUIRED_PROMPT_PHRASES:
                    self.assertIn(phrase, prompt)
                for banned in BANNED_PROMPT_FRAGMENTS:
                    self.assertNotIn(banned, prompt_lower)
                for banned in BANNED_CONTRACT_PHRASES:
                    self.assertNotIn(banned, prompt_lower)

        plan_text = PLAN.read_text(encoding="utf-8")
        documented_prompts = [
            json.loads(encoded_prompt)
            for encoded_prompt in re.findall(
                r'^\s+"prompt": (".*"),$',
                plan_text,
                flags=re.MULTILINE,
            )
        ]
        self.assertEqual(4, len(documented_prompts))
        for prompt, expected in zip(
            documented_prompts,
            EXPECTED_SLOTS,
            strict=True,
        ):
            prompt_lower = prompt.lower()
            with self.subTest(documented_slot=expected["slot"]):
                self.assertIn(expected["hair_variation"], prompt)
                for phrase in REQUIRED_PROMPT_PHRASES:
                    self.assertIn(phrase, prompt)
                for banned in BANNED_PROMPT_FRAGMENTS:
                    self.assertNotIn(banned, prompt_lower)
                for banned in BANNED_CONTRACT_PHRASES:
                    self.assertNotIn(banned, prompt_lower)

        validation_snippet = plan_text[
            plan_text.rindex("- [ ] **Step 7:") : plan_text.rindex("- [ ] **Step 8:")
        ]
        for phrase in PLAN_REQUIRED_SNIPPET_PHRASES:
            self.assertIn(phrase, validation_snippet)

    def test_acceptance_and_selection_gates_cover_identity_risks(self):
        for request in load_json(MANIFEST)["requests"]:
            with self.subTest(slot=request["slot"]):
                acceptance = request["acceptance"]
                gates = request["selection_gates"]
                hard_rejects = gates["hard_rejects"]

                self.assertIn("Y1 face direction", acceptance)
                self.assertIn("pale blue character-left hair ornament", acceptance)
                self.assertIn("upper crossed X-shaped hairpins", acceptance)
                self.assertIn("lower ribbon-like loop", acceptance)
                self.assertIn("two thin trailing strands", acceptance)
                self.assertIn("one compact v1.1 identity ornament", acceptance)
                self.assertIn("v1.1-compatible bangs", acceptance)
                self.assertIn("early-20s university-age", acceptance)
                self.assertIn("no readable text", acceptance)
                self.assertIn("no logos", acceptance)
                self.assertEqual(
                    "still reads as the selected Y1 standard-face direction",
                    gates["identity"],
                )
                for required_reject in REQUIRED_HARD_REJECTS:
                    self.assertIn(required_reject, hard_rejects)
                self.assertEqual(
                    ["oversized fashion bow"],
                    [reject for reject in hard_rejects if "bow" in reject.lower()],
                )
                self.assertEqual(
                    [
                        "missing lower ribbon-like loop or either trailing strand",
                        "large dangling ribbon",
                    ],
                    [reject for reject in hard_rejects if "ribbon" in reject.lower()],
                )
                self.assertIn("face redesign", hard_rejects)
                self.assertIn("underage drift", hard_rejects)

    def test_selection_notes_start_empty_until_user_review(self):
        manifest = load_json(MANIFEST)

        self.assertEqual([], manifest["selection_notes"])
```

- [ ] **Step 2: Run the test and verify the old manifest fails**

Run:

```bash
uv run python -m unittest tests.test_v1_2_hair_symbol_bangs_contract -v
```

Expected: `FAIL` against the old manifest because it still uses `_v1.png`
targets and omits the required lower loop/strands from prompts and gates.

- [ ] **Step 3: Keep the RED test uncommitted until the correction is GREEN**

Do not create an intermediate test-only commit for the correction.

## Task 2: Correct The Hair-Symbol/Bangs Request Manifest

**Files:**

- Modify:
  `source/manifests/v1-2-face-hair/hair-symbol-bangs-y1-requests.json`
- Test: `tests/test_v1_2_hair_symbol_bangs_contract.py`

- [ ] **Step 1: Correct the manifest**

Update `source/manifests/v1-2-face-hair/hair-symbol-bangs-y1-requests.json`:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.2-hair-symbol-bangs-y1",
  "title": "Akari v1.2 Hair Symbol And Bangs Y1",
  "source_lock": {
    "source_axis": "source/generated/v1-2-face-hair/free-reference-batch-younger-base05/20260708_base05-younger-01.png",
    "age_impression": "early-20s university-age young adult; still not underage",
    "locked_traits": [
      "Y1 face direction",
      "gentle eye read",
      "small restrained mouth",
      "white hoodie context"
    ]
  },
  "batch_policy": {
    "candidate_count": 4,
    "composition": "matched_bust_up",
    "primary_variation_axis": "hair_symbol_and_bangs",
    "face_policy": "lock_y1_face_direction",
    "pdf_policy": "not_in_this_step"
  },
  "requests": [
    {
      "id": "request:v1-2-hair-symbol-bangs-y1-ornament-lock",
      "candidate_order": 1,
      "slot": "ornament-lock",
      "japanese_title": "髪飾り固定",
      "eye_variation": "locked Y1 face; no eye redesign",
      "hair_variation": "restore the small pale blue v1.1 hair ornament shape",
      "target_path": "source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_ornament-lock_v2.png",
      "reference_inputs": [
        "source/generated/v1-2-face-hair/free-reference-batch-younger-base05/20260708_base05-younger-01.png",
        "source/originals/v1_1_髪飾り側_45deg.webp",
        "source/originals/v1_1_front_3.webp",
        "source/generated/tonari-no-hyoujou/20260703_called-turn_v2.webp"
      ],
      "prompt": "Use the Y1 image as the locked face source. Use the v1.1 hair-ornament-side image as the strict symbol reference. Create one matched bust-up composition of Akari v1.2 that preserves the selected Y1 face direction, gentle eyes, small restrained mouth, early-20s university-age young adult impression, white hoodie context, warm brown short bob, and soft approachable mood. Preserve the exact same crop, pose, background layout, and aspect ratio as the Y1 primary source. For this candidate, restore the small pale blue v1.1 hair ornament shape. Preserve both parts of the pale blue character-left hair ornament: upper small pale-blue crossed X-shaped hairpins; lower compact pale-blue ribbon-like loop immediately below, with two thin trailing strands; both stay on Akari's character-left side as one compact v1.1 identity ornament. Reject any result with a missing upper or lower component, wrong-side placement, flower, petal, or flower-center drift, jewel or gemstone drift, an oversized fashion bow, or a large dangling ribbon. Keep v1.1-like bang grouping, natural short-bob tips, and subtle cheek-side softness. do not change her eyes, do not change her mouth, do not change her age impression, do not redesign the face, do not redesign the outfit, do not make her underage, do not make her older-sister-like, no readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must still read as the selected Y1 face direction. Must show a pale blue character-left hair ornament that is v1.1-compatible: upper crossed X-shaped hairpins plus a lower ribbon-like loop immediately below with two thin trailing strands, together as one compact v1.1 identity ornament. Must keep v1.1-compatible bangs, warm brown short bob, early-20s university-age impression, white hoodie context, no readable text, no logos, no watermarks, no frame, and no panel layout.",
      "selection_gates": {
        "appeal": "small Akari identity symbol returns without making the portrait fussy",
        "identity": "still reads as the selected Y1 standard-face direction",
        "hard_rejects": [
          "missing upper crossed X-shaped hairpins",
          "missing lower ribbon-like loop or either trailing strand",
          "wrong-side hair ornament",
          "flower, petal, or flower-center ornament drift",
          "jewel or gemstone ornament drift",
          "oversized fashion bow",
          "large dangling ribbon",
          "face redesign",
          "eye redesign",
          "large mouth drift",
          "underage drift",
          "older-sister drift",
          "new outfit design"
        ]
      },
      "risk_profile": {
        "face_drift_risk": "high",
        "ornament_drift_risk": "high",
        "bang_drift_risk": "medium",
        "age_impression_risk": "medium",
        "text_logo_watermark_risk": "medium"
      }
    },
    {
      "id": "request:v1-2-hair-symbol-bangs-y1-bang-texture",
      "candidate_order": 2,
      "slot": "bang-texture",
      "japanese_title": "前髪の束感",
      "eye_variation": "locked Y1 face; no eye redesign",
      "hair_variation": "add v1.1-like soft uneven bang grouping",
      "target_path": "source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_bang-texture_v2.png",
      "reference_inputs": [
        "source/generated/v1-2-face-hair/free-reference-batch-younger-base05/20260708_base05-younger-01.png",
        "source/originals/v1_1_髪飾り側_45deg.webp",
        "source/originals/v1_1_front_3.webp",
        "source/generated/tonari-no-hyoujou/20260703_called-turn_v2.webp"
      ],
      "prompt": "Use the Y1 image as the locked face source. Use the v1.1 hair-ornament-side image as the strict symbol reference. Create one matched bust-up composition of Akari v1.2 that preserves the selected Y1 face direction, gentle eyes, small restrained mouth, early-20s university-age young adult impression, white hoodie context, warm brown short bob, and soft approachable mood. Preserve the exact same crop, pose, background layout, and aspect ratio as the Y1 primary source. For this candidate, add v1.1-like soft uneven bang grouping. Keep v1.1-like bang grouping readable and natural, slightly less salon-polished than Y1, with soft front pieces that do not hide the eyes. Preserve both parts of the pale blue character-left hair ornament: upper small pale-blue crossed X-shaped hairpins; lower compact pale-blue ribbon-like loop immediately below, with two thin trailing strands; both stay on Akari's character-left side as one compact v1.1 identity ornament. Reject any result with a missing upper or lower component, wrong-side placement, flower, petal, or flower-center drift, jewel or gemstone drift, an oversized fashion bow, or a large dangling ribbon. Keep natural short-bob tips and subtle cheek-side softness. do not change her eyes, do not change her mouth, do not change her age impression, do not redesign the face, do not redesign the outfit, do not make her underage, do not make her older-sister-like, no readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must still read as the selected Y1 face direction. Must show a pale blue character-left hair ornament that is v1.1-compatible: upper crossed X-shaped hairpins plus a lower ribbon-like loop immediately below with two thin trailing strands, together as one compact v1.1 identity ornament. Must keep v1.1-compatible bangs, warm brown short bob, early-20s university-age impression, white hoodie context, no readable text, no logos, no watermarks, no frame, and no panel layout.",
      "selection_gates": {
        "appeal": "bangs feel more Akari-like and less polished while staying clean",
        "identity": "still reads as the selected Y1 standard-face direction",
        "hard_rejects": [
          "missing upper crossed X-shaped hairpins",
          "missing lower ribbon-like loop or either trailing strand",
          "wrong-side hair ornament",
          "flower, petal, or flower-center ornament drift",
          "jewel or gemstone ornament drift",
          "oversized fashion bow",
          "large dangling ribbon",
          "face redesign",
          "eye redesign",
          "large mouth drift",
          "underage drift",
          "older-sister drift",
          "new outfit design"
        ]
      },
      "risk_profile": {
        "face_drift_risk": "high",
        "ornament_drift_risk": "medium",
        "bang_drift_risk": "high",
        "age_impression_risk": "medium",
        "text_logo_watermark_risk": "medium"
      }
    },
    {
      "id": "request:v1-2-hair-symbol-bangs-y1-side-frame-softness",
      "candidate_order": 3,
      "slot": "side-frame-softness",
      "japanese_title": "サイド髪の柔らかさ",
      "eye_variation": "locked Y1 face; no eye redesign",
      "hair_variation": "soften cheek-side short bob framing",
      "target_path": "source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_side-frame-softness_v2.png",
      "reference_inputs": [
        "source/generated/v1-2-face-hair/free-reference-batch-younger-base05/20260708_base05-younger-01.png",
        "source/originals/v1_1_髪飾り側_45deg.webp",
        "source/originals/v1_1_front_3.webp",
        "source/generated/tonari-no-hyoujou/20260703_called-turn_v2.webp"
      ],
      "prompt": "Use the Y1 image as the locked face source. Use the v1.1 hair-ornament-side image as the strict symbol reference. Create one matched bust-up composition of Akari v1.2 that preserves the selected Y1 face direction, gentle eyes, small restrained mouth, early-20s university-age young adult impression, white hoodie context, warm brown short bob, and soft approachable mood. Preserve the exact same crop, pose, background layout, and aspect ratio as the Y1 primary source. For this candidate, soften cheek-side short bob framing. Add a little v1.1-like face-framing softness around the cheeks and jaw while keeping the bob short and warm brown. Keep v1.1-like bang grouping. Preserve both parts of the pale blue character-left hair ornament: upper small pale-blue crossed X-shaped hairpins; lower compact pale-blue ribbon-like loop immediately below, with two thin trailing strands; both stay on Akari's character-left side as one compact v1.1 identity ornament. Reject any result with a missing upper or lower component, wrong-side placement, flower, petal, or flower-center drift, jewel or gemstone drift, an oversized fashion bow, or a large dangling ribbon. do not change her eyes, do not change her mouth, do not change her age impression, do not redesign the face, do not redesign the outfit, do not make her underage, do not make her older-sister-like, no readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must still read as the selected Y1 face direction. Must show a pale blue character-left hair ornament that is v1.1-compatible: upper crossed X-shaped hairpins plus a lower ribbon-like loop immediately below with two thin trailing strands, together as one compact v1.1 identity ornament. Must keep v1.1-compatible bangs, warm brown short bob, early-20s university-age impression, white hoodie context, no readable text, no logos, no watermarks, no frame, and no panel layout.",
      "selection_gates": {
        "appeal": "side hair adds approachable softness without length drift",
        "identity": "still reads as the selected Y1 standard-face direction",
        "hard_rejects": [
          "missing upper crossed X-shaped hairpins",
          "missing lower ribbon-like loop or either trailing strand",
          "wrong-side hair ornament",
          "flower, petal, or flower-center ornament drift",
          "jewel or gemstone ornament drift",
          "oversized fashion bow",
          "large dangling ribbon",
          "face redesign",
          "eye redesign",
          "large mouth drift",
          "underage drift",
          "older-sister drift",
          "new outfit design"
        ]
      },
      "risk_profile": {
        "face_drift_risk": "high",
        "ornament_drift_risk": "medium",
        "bang_drift_risk": "medium",
        "age_impression_risk": "medium",
        "text_logo_watermark_risk": "medium"
      }
    },
    {
      "id": "request:v1-2-hair-symbol-bangs-y1-balanced-symbol-bangs",
      "candidate_order": 4,
      "slot": "balanced-symbol-bangs",
      "japanese_title": "髪記号と前髪のバランス",
      "eye_variation": "locked Y1 face; no eye redesign",
      "hair_variation": "balance ornament lock, bang texture, and side framing",
      "target_path": "source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_balanced-symbol-bangs_v2.png",
      "reference_inputs": [
        "source/generated/v1-2-face-hair/free-reference-batch-younger-base05/20260708_base05-younger-01.png",
        "source/originals/v1_1_髪飾り側_45deg.webp",
        "source/originals/v1_1_front_3.webp",
        "source/generated/tonari-no-hyoujou/20260703_called-turn_v2.webp"
      ],
      "prompt": "Use the Y1 image as the locked face source. Use the v1.1 hair-ornament-side image as the strict symbol reference. Create one matched bust-up composition of Akari v1.2 that preserves the selected Y1 face direction, gentle eyes, small restrained mouth, early-20s university-age young adult impression, white hoodie context, warm brown short bob, and soft approachable mood. Preserve the exact same crop, pose, background layout, and aspect ratio as the Y1 primary source. For this candidate, balance ornament lock, bang texture, and side framing. Add v1.1-like bang grouping and keep subtle cheek-side short-bob softness. The result should look like Y1 with stronger Akari v1.1 hair identity, not a new portrait. Preserve both parts of the pale blue character-left hair ornament: upper small pale-blue crossed X-shaped hairpins; lower compact pale-blue ribbon-like loop immediately below, with two thin trailing strands; both stay on Akari's character-left side as one compact v1.1 identity ornament. Reject any result with a missing upper or lower component, wrong-side placement, flower, petal, or flower-center drift, jewel or gemstone drift, an oversized fashion bow, or a large dangling ribbon. do not change her eyes, do not change her mouth, do not change her age impression, do not redesign the face, do not redesign the outfit, do not make her underage, do not make her older-sister-like, no readable text, no logos, no watermarks, no frame, no border, no panel layout.",
      "acceptance": "Must still read as the selected Y1 face direction. Must show a pale blue character-left hair ornament that is v1.1-compatible: upper crossed X-shaped hairpins plus a lower ribbon-like loop immediately below with two thin trailing strands, together as one compact v1.1 identity ornament. Must keep v1.1-compatible bangs, warm brown short bob, early-20s university-age impression, white hoodie context, no readable text, no logos, no watermarks, no frame, and no panel layout.",
      "selection_gates": {
        "appeal": "best combined Y1 refinement without a new face family",
        "identity": "still reads as the selected Y1 standard-face direction",
        "hard_rejects": [
          "missing upper crossed X-shaped hairpins",
          "missing lower ribbon-like loop or either trailing strand",
          "wrong-side hair ornament",
          "flower, petal, or flower-center ornament drift",
          "jewel or gemstone ornament drift",
          "oversized fashion bow",
          "large dangling ribbon",
          "face redesign",
          "eye redesign",
          "large mouth drift",
          "underage drift",
          "older-sister drift",
          "new outfit design"
        ]
      },
      "risk_profile": {
        "face_drift_risk": "high",
        "ornament_drift_risk": "high",
        "bang_drift_risk": "high",
        "age_impression_risk": "medium",
        "text_logo_watermark_risk": "medium"
      }
    }
  ],
  "selection_notes": []
}
```

- [ ] **Step 2: Run the contract test and JSON parser**

Run:

```bash
python -m json.tool source/manifests/v1-2-face-hair/hair-symbol-bangs-y1-requests.json >/tmp/akari-v12-hair-symbol-bangs-v2.json
uv run python -m unittest tests.test_v1_2_hair_symbol_bangs_contract -v
```

Expected: JSON parser succeeds and all 7 focused tests pass.

- [ ] **Step 3: Run the existing v1.2 contract tests**

Run:

```bash
uv run python -m unittest tests.test_v1_2_face_hair_contract tests.test_v1_2_hair_symbol_bangs_contract -v
```

Expected: all existing face/hair tests plus the new hair-symbol/bangs tests
pass.

- [ ] **Step 4: Update both Markdown contracts before committing**

Correct the design spec and this plan, run the complete verification set, then
commit the four tracked files together as
`fix: preserve akari two-part hair ornament`.

## Task 3: Generate Four Corrected Y1 Hair-Symbol/Bangs Candidates

**Files:**

- Read:
  `source/manifests/v1-2-face-hair/hair-symbol-bangs-y1-requests.json`
- Write ignored:
  `source/generated/v1-2-face-hair/hair-symbol-bangs-y1/*.png`
- Write ignored:
  `evidence/v1-2-face-hair/contact-sheets/akari-v1-2-hair-symbol-bangs-y1-v2.webp`

The four failed `_v1.png` files and
`akari-v1-2-hair-symbol-bangs-y1-failed-v1.webp` are immutable evidence. Do not
delete or overwrite them while generating the corrected `_v2.png` batch.

- [ ] **Step 1: Open the reference images for visual grounding**

Use `view_image` on these files before calling image generation:

```text
/path/to/akari-design/.worktrees/akari-v1-2-face-hair/source/generated/v1-2-face-hair/free-reference-batch-younger-base05/20260708_base05-younger-01.png
/path/to/akari-design/.worktrees/akari-v1-2-face-hair/source/originals/v1_1_髪飾り側_45deg.webp
/path/to/akari-design/.worktrees/akari-v1-2-face-hair/source/originals/v1_1_front_3.webp
/path/to/akari-design/.worktrees/akari-v1-2-face-hair/source/generated/tonari-no-hyoujou/20260703_called-turn_v2.webp
```

Expected: Y1, the strict ornament reference, the v1.1 expression-board face,
and the accepted Hyoujou face family are visible in context before generation.
Confirm visually that the strict ornament reference contains both the crossed
upper pins and the compact lower ribbon-like loop with two strands.

- [ ] **Step 2: Record the generation baseline timestamp**

Run:

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

Expected: save the timestamp in the working notes for selecting only the four
newly generated images from `$CODEX_HOME/generated_images`.

Before each generation call, confirm the request prompt explicitly requires
both ornament parts and rejects a missing upper or lower component, wrong-side
placement, flower/petal/flower-center drift, jewel/gemstone drift, an oversized
fashion bow, and a large dangling ribbon. A compact lower ribbon-like loop is
required and is not a generic bow rejection. Also confirm that the prompt locks
the exact Y1 crop, pose, background layout, and aspect ratio.

- [ ] **Step 3: Generate `ornament-lock`**

Use the first request's `prompt` from
`source/manifests/v1-2-face-hair/hair-symbol-bangs-y1-requests.json` with the
four reference images visible in the conversation. After generation, copy the
new PNG to:

```text
source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_ornament-lock_v2.png
```

Expected: one PNG exists at that target path.

- [ ] **Step 4: Generate `bang-texture`**

Use the second request's `prompt` from the manifest with the same four
reference images. Copy the new PNG to:

```text
source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_bang-texture_v2.png
```

Expected: one PNG exists at that target path.

- [ ] **Step 5: Generate `side-frame-softness`**

Use the third request's `prompt` from the manifest with the same four reference
images. Copy the new PNG to:

```text
source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_side-frame-softness_v2.png
```

Expected: one PNG exists at that target path.

- [ ] **Step 6: Generate `balanced-symbol-bangs`**

Use the fourth request's `prompt` from the manifest with the same four
reference images. Copy the new PNG to:

```text
source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_balanced-symbol-bangs_v2.png
```

Expected: one PNG exists at that target path.

- [ ] **Step 7: Validate generated files as readable PNG images**

Run:

```bash
uv run python - <<'PY'
from pathlib import Path
from PIL import Image

root = Path("/path/to/akari-design/.worktrees/akari-v1-2-face-hair")
y1_path = (
    root
    / "source/generated/v1-2-face-hair/free-reference-batch-younger-base05/20260708_base05-younger-01.png"
)
paths = [
    root / "source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_ornament-lock_v2.png",
    root / "source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_bang-texture_v2.png",
    root / "source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_side-frame-softness_v2.png",
    root / "source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_balanced-symbol-bangs_v2.png",
]
with Image.open(y1_path) as y1_image:
    expected_size = y1_image.size

for path in paths:
    with path.open("rb") as image_file:
        signature = image_file.read(8).hex()
    if signature != "89504e470d0a1a0a":
        raise SystemExit(f"{path} is not a PNG: {signature}")
    with Image.open(path) as image:
        if image.size != expected_size:
            raise SystemExit(
                f"{path} size {image.size} does not match Y1 source dimensions "
                f"{expected_size}"
            )
        print(f"{path.relative_to(root)} {image.size} {image.mode}")
PY
```

Expected: four lines print image sizes and modes, and every size matches the Y1
source. A non-PNG file or any dimension mismatch raises `SystemExit`.

- [ ] **Step 8: Build the four-image contact sheet**

Run:

```bash
uv run python scripts/build_v1_2_face_hair_contact_sheet.py \
  --requests source/manifests/v1-2-face-hair/hair-symbol-bangs-y1-requests.json \
  --output evidence/v1-2-face-hair/contact-sheets/akari-v1-2-hair-symbol-bangs-y1-v2.webp \
  --columns 4
```

Expected:

```text
Wrote evidence/v1-2-face-hair/contact-sheets/akari-v1-2-hair-symbol-bangs-y1-v2.webp
```

- [ ] **Step 9: Confirm generated outputs are ignored**

Run:

```bash
git status --short --ignored source/generated/v1-2-face-hair/hair-symbol-bangs-y1 evidence/v1-2-face-hair/contact-sheets/akari-v1-2-hair-symbol-bangs-y1-v2.webp
```

Expected: output starts with `!!` for generated images and the contact sheet.
No `??` entries for those generated outputs.

- [ ] **Step 10: Present the contact sheet for user selection**

Use `view_image` on:

```text
/path/to/akari-design/.worktrees/akari-v1-2-face-hair/evidence/v1-2-face-hair/contact-sheets/akari-v1-2-hair-symbol-bangs-y1-v2.webp
```

Ask the user to choose one of:

```text
ornament-lock
bang-texture
side-frame-softness
balanced-symbol-bangs
reject all
```

Expected: stop before writing selection notes until the user chooses.

## Task 4: Record The User's Hair-Symbol/Bangs Selection

**Files:**

- Modify:
  `source/manifests/v1-2-face-hair/hair-symbol-bangs-y1-requests.json`
- Modify: `tests/test_v1_2_hair_symbol_bangs_contract.py`

Use this task only after the user selects one of the four slots. If the user
selects `reject all`, do not run this task; instead write a new spec amendment
for the next adjustment strategy.

- [ ] **Step 1: Add the selected slot expectation to the contract test**

Add this constant near `EXPECTED_SLOTS` in
`tests/test_v1_2_hair_symbol_bangs_contract.py`, replacing the values with the
chosen slot's row from the table below:

```python
SELECTED_SLOT = "balanced-symbol-bangs"
SELECTED_PATH = (
    "source/generated/v1-2-face-hair/hair-symbol-bangs-y1/"
    "20260708_balanced-symbol-bangs_v2.png"
)
SELECTED_RATIONALE_PHRASE = "best combined Y1 refinement"
```

Allowed selected-slot rows:

```text
ornament-lock | source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_ornament-lock_v2.png | complete two-part Akari identity ornament returns
bang-texture | source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_bang-texture_v2.png | bangs feel more Akari-like
side-frame-softness | source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_side-frame-softness_v2.png | side hair adds approachable softness
balanced-symbol-bangs | source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_balanced-symbol-bangs_v2.png | best combined Y1 refinement
```

Replace the existing `test_selection_notes_start_empty_until_user_review`
method with:

```python
    def test_selection_notes_record_user_choice_after_review(self):
        selection_notes = load_json(MANIFEST)["selection_notes"]

        self.assertEqual(1, len(selection_notes))
        selection = selection_notes[0]
        self.assertEqual("hold_as_hair_symbol_bangs_y1_direction", selection["decision"])
        self.assertEqual(SELECTED_SLOT, selection["selected_slot"])
        self.assertEqual(SELECTED_PATH, selection["selected_candidate_path"])
        self.assertEqual(
            (
                "evidence/v1-2-face-hair/contact-sheets/"
                "akari-v1-2-hair-symbol-bangs-y1-v2.webp"
            ),
            selection["selected_contact_sheet_path"],
        )
        self.assertIn("Y1 face direction remains locked", selection["rationale"])
        self.assertIn(SELECTED_RATIONALE_PHRASE, selection["rationale"])
```

- [ ] **Step 2: Run the test and verify it fails before manifest update**

Run:

```bash
uv run python -m unittest tests.test_v1_2_hair_symbol_bangs_contract -v
```

Expected: one failure in
`test_selection_notes_record_user_choice_after_review` because
`selection_notes` is still empty.

- [ ] **Step 3: Add the selection note to the manifest**

In `source/manifests/v1-2-face-hair/hair-symbol-bangs-y1-requests.json`,
replace:

```json
  "selection_notes": []
```

with this block, using the chosen slot's exact `selected_slot`,
`selected_candidate_path`, and rationale phrase from Step 1:

```json
  "selection_notes": [
    {
      "decision": "hold_as_hair_symbol_bangs_y1_direction",
      "selected_slot": "balanced-symbol-bangs",
      "selected_candidate_path": "source/generated/v1-2-face-hair/hair-symbol-bangs-y1/20260708_balanced-symbol-bangs_v2.png",
      "selected_contact_sheet_path": "evidence/v1-2-face-hair/contact-sheets/akari-v1-2-hair-symbol-bangs-y1-v2.webp",
      "rationale": "Y1 face direction remains locked; best combined Y1 refinement was selected as the follow-up hair-symbol and bangs direction."
    }
  ]
```

- [ ] **Step 4: Verify JSON, tests, and Markdown**

Run:

```bash
python -m json.tool source/manifests/v1-2-face-hair/hair-symbol-bangs-y1-requests.json >/tmp/akari-v12-hair-symbol-bangs-selected.json
uv run python -m unittest tests.test_v1_2_face_hair_contract tests.test_v1_2_hair_symbol_bangs_contract tests.test_v1_2_face_hair_contact_sheet -v
npm run lint:md
git diff --check
```

Expected: JSON parser succeeds, all listed tests pass, Markdown lint reports
`0 error(s)`, and `git diff --check` prints no output.

- [ ] **Step 5: Commit the selection record**

Run:

```bash
git add source/manifests/v1-2-face-hair/hair-symbol-bangs-y1-requests.json tests/test_v1_2_hair_symbol_bangs_contract.py
git commit -m "docs: record akari v1.2 hair symbol bangs direction"
```

## Final Verification

Run:

```bash
python -m json.tool source/manifests/v1-2-face-hair/hair-symbol-bangs-y1-requests.json >/tmp/akari-v12-hair-symbol-bangs-v2.json
uv run python -m unittest tests.test_v1_2_face_hair_contract tests.test_v1_2_hair_symbol_bangs_contract tests.test_v1_2_face_hair_contact_sheet -v
npm run lint:md
git diff --check
git status --short --ignored source/generated/v1-2-face-hair/hair-symbol-bangs-y1 evidence/v1-2-face-hair/contact-sheets/akari-v1-2-hair-symbol-bangs-y1-failed-v1.webp
```

Expected:

- JSON parsing succeeds and all 26 targeted Python tests pass.
- Markdown lint reports `0 error(s)`.
- `git diff --check` prints no output.
- The failed `_v1.png` files and failed-v1 contact sheet remain ignored and
  unchanged; any corrected `_v2.png` files and the v2 contact sheet also remain
  ignored.

## Handoff Notes

- If image generation ignores the Y1 face lock, stop after the first bad
  candidate and ask whether to switch from free generation to a stricter image
  edit workflow.
- Reject any candidate that changes the Y1 crop, pose, background layout, or
  aspect ratio; dimension mismatches must fail before contact-sheet review.
- Reject any candidate missing the upper crossed pins or lower loop/strands, or
  showing wrong-side placement, flower/petal/flower-center drift,
  jewel/gemstone drift, an oversized fashion bow, or a large dangling ribbon.
  Preserve failed contact sheets as ignored evidence before tightening prompts.
- If the user rejects all four candidates, do not force a selection note. Add a
  short spec amendment for the new strategy, then write a new plan for that
  strategy.
