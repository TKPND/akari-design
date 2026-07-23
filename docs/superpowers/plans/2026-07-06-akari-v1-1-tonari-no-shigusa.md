# Akari v1.1 Tonari No Shigusa Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first image-first `となりのしぐさ` workflow: a 36-slot gesture map, generated request manifest for the first promising batch, and a contact-sheet path for reviewing motion.

**Architecture:** Keep `gesture-slots.json` as the source of truth. A small Python builder derives `generation-requests.json` from `priority == "promising"` slots, and a separate Pillow contact-sheet script reviews generated image files without adding PDF or booklet rendering.

**Tech Stack:** Python 3.11, `unittest`, JSON manifests, Pillow, `uv run python`, existing npm scripts.

---

## Scope Check

The approved design covers one subsystem: image-first gesture exploration. This plan does not add PDF rendering, gallery output, image finishing automation, or public publishing.

## File Structure

- Create `tests/test_tonari_no_shigusa_contract.py`
  - Contract tests for slot metadata, generated requests, package scripts, identity locks, text bans, and Motion Gate fields.
- Create `source/manifests/tonari-no-shigusa/gesture-slots.json`
  - Source-of-truth 36-slot idea map.
- Create `scripts/build_tonari_no_shigusa_generation_requests.py`
  - Deterministically derives generation requests for `promising` slots.
- Create `source/manifests/tonari-no-shigusa/generation-requests.json`
  - Derived first-batch request manifest.
- Create `tests/test_tonari_no_shigusa_contact_sheet.py`
  - Unit tests for contact-sheet generation using temporary images.
- Create `scripts/build_tonari_no_shigusa_contact_sheet.py`
  - Builds a labeled sheet from existing generated images.
- Modify `package.json`
  - Add `build:shigusa:requests` and `build:shigusa:contact-sheet`.

## Task 1: Add The Failing Shigusa Contract Test

**Files:**

- Create: `tests/test_tonari_no_shigusa_contract.py`

- [ ] **Step 1: Write the failing contract test**

Create `tests/test_tonari_no_shigusa_contract.py`:

```python
import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/tonari-no-shigusa"
SLOT_MANIFEST = MANIFEST_DIR / "gesture-slots.json"
GENERATION_REQUESTS = MANIFEST_DIR / "generation-requests.json"
COLLECTION_ID = "akari-v1.1-tonari-no-shigusa"
TITLE = "となりのしぐさ"
REFERENCE_PACK_VERSION = "tonari-no-akari-identity-v1"
PROMPT_TEMPLATE_VERSION = "tonari_shigusa_motion_lock_v1"
REFERENCE_PACK_INPUTS = [
    "source/references/tonari-no-akari/identity-face-hair.webp",
    "source/references/tonari-no-akari/identity-body-base.webp",
    "source/references/tonari-no-akari/identity-basic-outfit.webp",
    "source/references/tonari-no-akari/identity-side-view.webp",
]
DISTANCE_COUNTS = {
    "beside": 6,
    "across": 6,
    "diagonal": 6,
    "over_shoulder": 6,
    "one_step_close": 6,
    "relaxed": 6,
}
PRIORITY_COUNTS = {
    "promising": 18,
    "seed": 13,
    "hold": 5,
}
ALLOWED_POSITIVE_TONES = {
    "reassurance",
    "shyness",
    "closeness",
    "small_dependence",
    "joy",
    "relaxation",
}
ALLOWED_GESTURE_FOCUS = {
    "sleeve",
    "hand",
    "shoulder",
    "back",
    "knee",
    "hair",
    "posture",
    "feet",
}
ALLOWED_SCENES = {"room", "desk", "sofa", "entrance", "window", "walk_home"}
ALLOWED_COMPOSITIONS = {"upper_body", "half_body", "knee_up", "wider_body"}
MOTION_VERBS = {"pull", "reach", "lean", "twist", "fix", "release", "bounce"}
JAPANESE_TEXT = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
IDENTITY_LOCK_PHRASES = [
    "adult 25-year-old japanese woman",
    "naturally cute adult",
    "not glamorous",
    "not model-like",
    "not pin-up",
    "not childlike",
    "short fluffy light-brown bob",
    "warm amber eyes",
    "pale-blue crossed hairpins",
    "white hoodie",
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
BANNED_PROMPT_FRAGMENTS = {
    "school uniform",
    "teenage",
    "little girl",
    "young child",
    "child body",
    "childlike body",
    "pinup",
    "pin-up pose",
    "glamour model",
}


def load_json(path):
    with path.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


class TonariNoShigusaContractTest(unittest.TestCase):
    def test_package_scripts_expose_shigusa_helpers(self):
        package_json = load_json(ROOT / "package.json")
        scripts = package_json["scripts"]

        self.assertEqual(
            "uv run python scripts/build_tonari_no_shigusa_generation_requests.py",
            scripts["build:shigusa:requests"],
        )
        self.assertEqual(
            "uv run python scripts/build_tonari_no_shigusa_contact_sheet.py",
            scripts["build:shigusa:contact-sheet"],
        )

    def test_slot_manifest_exists_and_records_strategy(self):
        self.assertTrue(SLOT_MANIFEST.is_file(), f"missing manifest: {SLOT_MANIFEST}")
        manifest = load_json(SLOT_MANIFEST)

        self.assertEqual(1, manifest["schema_version"])
        self.assertEqual(COLLECTION_ID, manifest["collection_id"])
        self.assertEqual(TITLE, manifest["title"])
        self.assertEqual(REFERENCE_PACK_VERSION, manifest["reference_pack_version"])
        self.assertEqual(
            "distance_map_first_positive_body_language_second",
            manifest["strategy"]["organizing_model"],
        )
        self.assertEqual("white_hoodie_primary", manifest["strategy"]["outfit_direction"])
        self.assertEqual("half_body_to_knee_up", manifest["strategy"]["composition_center"])
        self.assertEqual("motion_gate_required", manifest["strategy"]["acceptance_center"])

    def test_slot_map_has_36_balanced_motion_slots(self):
        manifest = load_json(SLOT_MANIFEST)
        slots = manifest["slots"]

        self.assertEqual(36, len(slots))
        self.assertEqual(DISTANCE_COUNTS, dict(Counter(slot["distance"] for slot in slots)))
        self.assertEqual(PRIORITY_COUNTS, dict(Counter(slot["priority"] for slot in slots)))
        self.assertEqual(len(slots), len({slot["slug"] for slot in slots}))

        for index, slot in enumerate(slots, start=1):
            with self.subTest(slot=slot["slug"]):
                self.assertEqual(index, slot["slot_order"])
                self.assertRegex(slot["slug"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertTrue(JAPANESE_TEXT.search(slot["japanese_title"]))
                self.assertIn(slot["distance"], DISTANCE_COUNTS)
                self.assertIn(slot["positive_tone"], ALLOWED_POSITIVE_TONES)
                self.assertIn(slot["gesture_focus"], ALLOWED_GESTURE_FOCUS)
                self.assertIn(slot["scene"], ALLOWED_SCENES)
                self.assertIn(slot["composition"], ALLOWED_COMPOSITIONS)
                self.assertIn(slot["motion"]["verb"], MOTION_VERBS)
                self.assertTrue(slot["motion"]["body_part"])
                self.assertTrue(slot["motion"]["readable_change"])
                self.assertTrue(slot["prompt_note"])
                self.assertTrue(slot["avoid_note"])
                self.assertNotIn("static portrait", slot["prompt_note"].lower())
                self.assertNotIn("face close-up", slot["prompt_note"].lower())

    def test_promising_slots_cover_every_distance_and_motion_family(self):
        slots = load_json(SLOT_MANIFEST)["slots"]
        promising = [slot for slot in slots if slot["priority"] == "promising"]

        self.assertEqual(18, len(promising))
        self.assertEqual(set(DISTANCE_COUNTS), {slot["distance"] for slot in promising})

        motion_verbs = {slot["motion"]["verb"] for slot in promising}
        for required in ("pull", "reach", "lean", "twist", "fix", "release"):
            self.assertIn(required, motion_verbs)

    def test_generation_requests_match_promising_slots(self):
        slots = load_json(SLOT_MANIFEST)["slots"]
        promising_slots = [slot for slot in slots if slot["priority"] == "promising"]
        generation_requests = load_json(GENERATION_REQUESTS)
        requests = generation_requests["requests"]

        self.assertEqual(COLLECTION_ID, generation_requests["collection_id"])
        self.assertEqual(TITLE, generation_requests["title"])
        self.assertEqual(REFERENCE_PACK_VERSION, generation_requests["reference_pack_version"])
        self.assertEqual(PROMPT_TEMPLATE_VERSION, generation_requests["prompt_template_version"])
        self.assertEqual("promising_slots_only", generation_requests["batch_policy"]["request_source"])
        self.assertEqual("contact_sheet_before_finishing", generation_requests["batch_policy"]["review_order"])
        self.assertEqual([slot["slug"] for slot in promising_slots], [request["slot"] for request in requests])

        for request, slot in zip(requests, promising_slots, strict=True):
            with self.subTest(slot=slot["slug"]):
                self.assertEqual(f"request:tonari-shigusa-{slot['slug']}", request["id"])
                self.assertEqual(slot["slot_order"], request["slot_order"])
                self.assertEqual(slot["japanese_title"], request["japanese_title"])
                self.assertEqual(slot["distance"], request["distance"])
                self.assertEqual(slot["positive_tone"], request["positive_tone"])
                self.assertEqual(slot["gesture_focus"], request["gesture_focus"])
                self.assertEqual(slot["scene"], request["scene"])
                self.assertEqual(slot["composition"], request["composition"])
                self.assertEqual(slot["motion"], request["motion"])
                self.assertEqual(REFERENCE_PACK_INPUTS, request["reference_pack_inputs"])
                self.assertEqual(
                    f"source/generated/tonari-no-shigusa/20260706_{slot['slug']}_v1.webp",
                    request["target_path"],
                )

    def test_generation_prompts_lock_identity_motion_and_text_bans(self):
        generation_requests = load_json(GENERATION_REQUESTS)

        for request in generation_requests["requests"]:
            with self.subTest(slot=request["slot"]):
                prompt = request["prompt"].lower()
                acceptance = request["acceptance"].lower()
                combined = f"{prompt} {acceptance}"

                self.assertIn(request["japanese_title"].lower(), request["prompt"].lower())
                self.assertIn(request["motion"]["verb"], prompt)
                self.assertIn(request["motion"]["body_part"], prompt)
                self.assertIn(request["motion"]["readable_change"].lower(), prompt)
                self.assertIn("motion gate", acceptance)
                self.assertIn("not another facial-expression sheet", acceptance)

                for phrase in IDENTITY_LOCK_PHRASES:
                    self.assertIn(phrase, prompt)
                for phrase in IMAGE_TEXT_BANS:
                    self.assertIn(phrase, combined)
                for fragment in BANNED_PROMPT_FRAGMENTS:
                    self.assertNotIn(fragment, prompt)

    def test_request_risk_profiles_and_review_plan_are_explicit(self):
        generation_requests = load_json(GENERATION_REQUESTS)

        for request in generation_requests["requests"]:
            with self.subTest(slot=request["slot"]):
                risk_profile = request["risk_profile"]
                self.assertEqual("high", risk_profile["identity_risk"])
                self.assertIn(risk_profile["hand_risk"], {"medium", "high"})
                self.assertIn(risk_profile["motion_readability_risk"], {"medium", "high"})
                self.assertEqual("medium", risk_profile["text_logo_watermark_risk"])

                review_plan = request["review_plan"]
                self.assertEqual("draft_candidate", review_plan["initial_status"])
                self.assertIn("contact sheet", review_plan["first_pass"])
                self.assertIn("Motion Gate", review_plan["motion_gate"])
                self.assertIn("akari-v1-1-image-review", review_plan["strict_review"])
                self.assertIn("Correction Pass", review_plan["correction"])
                self.assertIn("Humanization Pass", review_plan["humanization"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and confirm it fails on missing files/scripts**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_shigusa_contract
```

Expected: `FAILED` with a missing `build:shigusa:requests` key or missing `gesture-slots.json`, depending on assertion order.

- [ ] **Step 3: Commit the failing test**

```bash
git add tests/test_tonari_no_shigusa_contract.py
git commit -m "test: add tonari no shigusa contract"
```

## Task 2: Add The 36-Slot Gesture Map

**Files:**

- Create: `source/manifests/tonari-no-shigusa/gesture-slots.json`
- Test: `tests/test_tonari_no_shigusa_contract.py`

- [ ] **Step 1: Create the slot manifest**

Create `source/manifests/tonari-no-shigusa/gesture-slots.json`:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.1-tonari-no-shigusa",
  "title": "となりのしぐさ",
  "reference_pack_version": "tonari-no-akari-identity-v1",
  "strategy": {
    "organizing_model": "distance_map_first_positive_body_language_second",
    "outfit_direction": "white_hoodie_primary",
    "scene_range": ["room", "desk", "sofa", "entrance", "window", "walk_home"],
    "composition_center": "half_body_to_knee_up",
    "acceptance_center": "motion_gate_required"
  },
  "distance_map": [
    {"id": "beside", "japanese_label": "隣にいる"},
    {"id": "across", "japanese_label": "向かいにいる"},
    {"id": "diagonal", "japanese_label": "斜め前にいる"},
    {"id": "over_shoulder", "japanese_label": "背中越し・振り返り"},
    {"id": "one_step_close", "japanese_label": "一歩近い"},
    {"id": "relaxed", "japanese_label": "くつろぎの距離"}
  ],
  "slots": [
    {
      "slot_order": 1,
      "slug": "sleeve-near-bench",
      "japanese_title": "隣で袖をそっと寄せる",
      "distance": "beside",
      "positive_tone": "closeness",
      "gesture_focus": "sleeve",
      "scene": "walk_home",
      "composition": "knee_up",
      "motion": {"verb": "pull", "body_part": "sleeve and elbow", "readable_change": "one sleeve shifts closer while her elbow draws inward"},
      "prompt_note": "Akari sits or stands beside the viewer in a white hoodie, gently pulling one sleeve closer while keeping a happy near-distance mood.",
      "avoid_note": "Do not make this a face-led close-up; keep the sleeve and elbow movement visible.",
      "priority": "promising"
    },
    {
      "slot_order": 2,
      "slug": "shoulder-soft-sofa",
      "japanese_title": "ソファで肩の力が抜ける",
      "distance": "beside",
      "positive_tone": "reassurance",
      "gesture_focus": "shoulder",
      "scene": "sofa",
      "composition": "half_body",
      "motion": {"verb": "release", "body_part": "shoulders", "readable_change": "both shoulders drop into a relaxed beside-you posture"},
      "prompt_note": "Akari relaxes beside the viewer on a sofa, shoulders lowering in visible comfort, white hoodie folds soft around the arms.",
      "avoid_note": "Avoid sleepy collapse or gloomy fatigue; this is comfortable happiness.",
      "priority": "promising"
    },
    {
      "slot_order": 3,
      "slug": "knee-angle-floor",
      "japanese_title": "床で膝だけこちらに向く",
      "distance": "beside",
      "positive_tone": "relaxation",
      "gesture_focus": "knee",
      "scene": "room",
      "composition": "knee_up",
      "motion": {"verb": "lean", "body_part": "knees and torso", "readable_change": "knees angle toward the viewer while the torso follows softly"},
      "prompt_note": "Akari sits on the floor in a white hoodie, knees angled toward the viewer as she settles into the shared space.",
      "avoid_note": "Keep the pose modest and adult; avoid childlike curled-up proportions.",
      "priority": "seed"
    },
    {
      "slot_order": 4,
      "slug": "shared-cup-beside",
      "japanese_title": "隣でカップを両手に持つ",
      "distance": "beside",
      "positive_tone": "reassurance",
      "gesture_focus": "hand",
      "scene": "sofa",
      "composition": "half_body",
      "motion": {"verb": "reach", "body_part": "hands and cup", "readable_change": "the cup shifts slightly toward the viewer while both hands stay simple"},
      "prompt_note": "Akari holds a plain cup with both hands beside the viewer, subtly offering or sharing warmth without readable text on the cup.",
      "avoid_note": "Use a plain unbranded cup; avoid complex interlocked fingers.",
      "priority": "seed"
    },
    {
      "slot_order": 5,
      "slug": "almost-lean-hoodie",
      "japanese_title": "寄りかかりそうで止まる",
      "distance": "beside",
      "positive_tone": "small_dependence",
      "gesture_focus": "posture",
      "scene": "sofa",
      "composition": "knee_up",
      "motion": {"verb": "lean", "body_part": "torso and shoulder", "readable_change": "her torso tilts closer but stops before fully leaning"},
      "prompt_note": "Akari in a white hoodie almost leans on the viewer from beside, pausing with a shy happy posture.",
      "avoid_note": "Keep the gesture gentle and healthy; avoid romantic overstatement or pin-up framing.",
      "priority": "promising"
    },
    {
      "slot_order": 6,
      "slug": "walk-beside-sleeve",
      "japanese_title": "帰り道で袖が揺れる",
      "distance": "beside",
      "positive_tone": "joy",
      "gesture_focus": "sleeve",
      "scene": "walk_home",
      "composition": "wider_body",
      "motion": {"verb": "bounce", "body_part": "sleeves and step", "readable_change": "a light step makes the hoodie sleeve swing beside the viewer"},
      "prompt_note": "Akari walks beside the viewer in a white hoodie, one small happy step making the sleeve swing naturally.",
      "avoid_note": "Avoid running action; this should be a small everyday step.",
      "priority": "seed"
    },
    {
      "slot_order": 7,
      "slug": "desk-lean-forward",
      "japanese_title": "机越しに少し身を乗り出す",
      "distance": "across",
      "positive_tone": "joy",
      "gesture_focus": "posture",
      "scene": "desk",
      "composition": "half_body",
      "motion": {"verb": "reach", "body_part": "torso and shoulders", "readable_change": "her upper body moves forward across the desk"},
      "prompt_note": "Akari leans forward across a simple desk in a white hoodie, curious and happy, with hands kept simple on the desk edge.",
      "avoid_note": "Avoid face-only framing; show the desk edge and forward body motion.",
      "priority": "promising"
    },
    {
      "slot_order": 8,
      "slug": "chin-hand-smile",
      "japanese_title": "頬杖で小さく笑う",
      "distance": "across",
      "positive_tone": "reassurance",
      "gesture_focus": "hand",
      "scene": "desk",
      "composition": "upper_body",
      "motion": {"verb": "release", "body_part": "wrist and shoulder", "readable_change": "her wrist takes the cheek weight while the shoulder relaxes"},
      "prompt_note": "Akari rests her cheek lightly on one hand across the desk, white hoodie sleeve visible, small happy smile secondary to the hand pose.",
      "avoid_note": "Do not crop out the elbow and sleeve support; avoid making only the face expressive.",
      "priority": "seed"
    },
    {
      "slot_order": 9,
      "slug": "cup-both-hands",
      "japanese_title": "カップを両手で包む",
      "distance": "across",
      "positive_tone": "relaxation",
      "gesture_focus": "hand",
      "scene": "desk",
      "composition": "half_body",
      "motion": {"verb": "release", "body_part": "hands and shoulders", "readable_change": "both hands settle around a cup while shoulders soften"},
      "prompt_note": "Akari across a desk wraps both hands around a plain cup, shoulders relaxed, white hoodie sleeves bunching softly.",
      "avoid_note": "Cup must be unbranded and textless; fingers should remain simple and separated.",
      "priority": "promising"
    },
    {
      "slot_order": 10,
      "slug": "sleeve-mouth-table",
      "japanese_title": "袖口で口元を隠す",
      "distance": "across",
      "positive_tone": "shyness",
      "gesture_focus": "sleeve",
      "scene": "desk",
      "composition": "upper_body",
      "motion": {"verb": "pull", "body_part": "sleeve and hand", "readable_change": "the sleeve lifts toward the mouth while the shoulder turns shyly"},
      "prompt_note": "Akari sits across the desk and raises a white hoodie sleeve near her mouth, shy but happy, with the hand and shoulder motion visible.",
      "avoid_note": "Do not cover her identity; keep eyes, hair, and hairpins readable.",
      "priority": "promising"
    },
    {
      "slot_order": 11,
      "slug": "notebook-peek",
      "japanese_title": "ノートの向こうから覗く",
      "distance": "across",
      "positive_tone": "joy",
      "gesture_focus": "posture",
      "scene": "desk",
      "composition": "half_body",
      "motion": {"verb": "reach", "body_part": "head and shoulders", "readable_change": "she peeks over a low notebook while shoulders shift forward"},
      "prompt_note": "Akari peeks over a plain textless notebook across the desk, white hoodie visible, happy curiosity in the forward motion.",
      "avoid_note": "Notebook must have no readable writing or logo marks.",
      "priority": "seed"
    },
    {
      "slot_order": 12,
      "slug": "reaching-across-desk",
      "japanese_title": "机越しに手を伸ばしかける",
      "distance": "across",
      "positive_tone": "closeness",
      "gesture_focus": "hand",
      "scene": "desk",
      "composition": "half_body",
      "motion": {"verb": "reach", "body_part": "hand and forearm", "readable_change": "one hand extends across the desk but stops before touching"},
      "prompt_note": "Akari reaches one simple hand across the desk from a white hoodie sleeve, stopping just short with warm closeness.",
      "avoid_note": "Avoid distorted foreground fingers; keep the hand simple and not too close to the lens.",
      "priority": "promising"
    },
    {
      "slot_order": 13,
      "slug": "hair-tuck-diagonal",
      "japanese_title": "斜め前で髪を耳にかける",
      "distance": "diagonal",
      "positive_tone": "shyness",
      "gesture_focus": "hair",
      "scene": "window",
      "composition": "half_body",
      "motion": {"verb": "fix", "body_part": "hair and hand", "readable_change": "one hand moves hair near the ear while the shoulders stay diagonal"},
      "prompt_note": "Akari stands diagonally near a window in a white hoodie, one hand tucking hair near the ear with a shy happy body angle.",
      "avoid_note": "Keep the pale-blue hairpins consistent and do not hide them behind the hand.",
      "priority": "promising"
    },
    {
      "slot_order": 14,
      "slug": "shoulder-turn-window",
      "japanese_title": "肩だけこちらに向ける",
      "distance": "diagonal",
      "positive_tone": "closeness",
      "gesture_focus": "shoulder",
      "scene": "window",
      "composition": "half_body",
      "motion": {"verb": "twist", "body_part": "shoulders and neck", "readable_change": "only the shoulders rotate toward the viewer from a diagonal stance"},
      "prompt_note": "Akari near a window turns only her shoulders toward the viewer, white hoodie folds showing the twist.",
      "avoid_note": "Avoid full frontal portrait; keep the diagonal body read.",
      "priority": "seed"
    },
    {
      "slot_order": 15,
      "slug": "averted-happy-sleeve",
      "japanese_title": "嬉しくて袖を握りながら目を逸らす",
      "distance": "diagonal",
      "positive_tone": "shyness",
      "gesture_focus": "sleeve",
      "scene": "room",
      "composition": "half_body",
      "motion": {"verb": "pull", "body_part": "sleeve and shoulders", "readable_change": "fingers grip the sleeve while shoulders turn slightly away"},
      "prompt_note": "Akari in a white hoodie looks diagonally away while gripping a sleeve, visibly happy but shy through the shoulder and hand motion.",
      "avoid_note": "The gesture must not become only a blush expression; show the sleeve grip clearly.",
      "priority": "promising"
    },
    {
      "slot_order": 16,
      "slug": "hoodie-cuff-fix",
      "japanese_title": "パーカー袖を直す",
      "distance": "diagonal",
      "positive_tone": "relaxation",
      "gesture_focus": "sleeve",
      "scene": "room",
      "composition": "half_body",
      "motion": {"verb": "fix", "body_part": "hoodie cuff", "readable_change": "one hand adjusts the opposite hoodie cuff"},
      "prompt_note": "Akari diagonally adjusts one white hoodie cuff with the other hand in a relaxed everyday moment.",
      "avoid_note": "Avoid merged hands at the cuffs; keep both wrists readable.",
      "priority": "seed"
    },
    {
      "slot_order": 17,
      "slug": "side-step-smile",
      "japanese_title": "横に一歩ずれて笑う",
      "distance": "diagonal",
      "positive_tone": "joy",
      "gesture_focus": "feet",
      "scene": "walk_home",
      "composition": "wider_body",
      "motion": {"verb": "bounce", "body_part": "feet and sleeves", "readable_change": "a small side step shifts her weight and sleeve swing"},
      "prompt_note": "Akari takes a small sideways step on a walk home, smiling lightly, white hoodie sleeves moving with the step.",
      "avoid_note": "Keep the motion small and everyday; avoid dance-like exaggeration.",
      "priority": "hold"
    },
    {
      "slot_order": 18,
      "slug": "listening-side-angle",
      "japanese_title": "斜めに聞きながら首を傾ける",
      "distance": "diagonal",
      "positive_tone": "reassurance",
      "gesture_focus": "posture",
      "scene": "room",
      "composition": "upper_body",
      "motion": {"verb": "twist", "body_part": "neck and shoulder", "readable_change": "her head tilts while one shoulder remains angled toward the viewer"},
      "prompt_note": "Akari listens from a diagonal angle, head slightly tilted and shoulder still turned toward the viewer in a white hoodie.",
      "avoid_note": "Avoid making this a face-only listening expression; include shoulder line.",
      "priority": "seed"
    },
    {
      "slot_order": 19,
      "slug": "doorway-hand-pause",
      "japanese_title": "ドアの前で手だけ止まる",
      "distance": "over_shoulder",
      "positive_tone": "closeness",
      "gesture_focus": "hand",
      "scene": "entrance",
      "composition": "knee_up",
      "motion": {"verb": "twist", "body_part": "hand and shoulders", "readable_change": "her hand pauses near the door while shoulders twist back"},
      "prompt_note": "Akari at an entrance in a white hoodie pauses with one hand near a plain door, turning back warmly over her shoulder.",
      "avoid_note": "Door must be plain with no signs or readable labels; keep hand anatomy simple.",
      "priority": "promising"
    },
    {
      "slot_order": 20,
      "slug": "walk-back-turn",
      "japanese_title": "一歩先で振り返る",
      "distance": "over_shoulder",
      "positive_tone": "joy",
      "gesture_focus": "back",
      "scene": "walk_home",
      "composition": "wider_body",
      "motion": {"verb": "twist", "body_part": "back and neck", "readable_change": "her body keeps walking forward while the neck and shoulders turn back"},
      "prompt_note": "Akari walks one step ahead in a white hoodie and turns back with light happiness, showing back, shoulder, and neck motion.",
      "avoid_note": "Face should be readable enough for identity but the back-turn gesture stays primary.",
      "priority": "promising"
    },
    {
      "slot_order": 21,
      "slug": "hoodie-back-glance",
      "japanese_title": "フード越しに少し振り向く",
      "distance": "over_shoulder",
      "positive_tone": "reassurance",
      "gesture_focus": "back",
      "scene": "window",
      "composition": "half_body",
      "motion": {"verb": "twist", "body_part": "hoodie back and head", "readable_change": "hoodie back faces the viewer while the head turns slightly"},
      "prompt_note": "Akari near a window shows the back of the white hoodie while glancing back softly.",
      "avoid_note": "Avoid hiding identity completely; show enough face profile and hairpin context when possible.",
      "priority": "seed"
    },
    {
      "slot_order": 22,
      "slug": "window-shoulder-look",
      "japanese_title": "窓辺で肩越しに見る",
      "distance": "over_shoulder",
      "positive_tone": "relaxation",
      "gesture_focus": "shoulder",
      "scene": "window",
      "composition": "half_body",
      "motion": {"verb": "twist", "body_part": "shoulder and neck", "readable_change": "one shoulder stays toward the window while her gaze returns to the viewer"},
      "prompt_note": "Akari turns from a window in a white hoodie, shoulder still angled away while her attention returns warmly.",
      "avoid_note": "Keep the window background simple and unbranded.",
      "priority": "seed"
    },
    {
      "slot_order": 23,
      "slug": "entrance-sleeve-stop",
      "japanese_title": "玄関で袖を握って止まる",
      "distance": "over_shoulder",
      "positive_tone": "small_dependence",
      "gesture_focus": "sleeve",
      "scene": "entrance",
      "composition": "knee_up",
      "motion": {"verb": "pull", "body_part": "sleeve and torso", "readable_change": "she grips a sleeve and stops mid-turn at the entrance"},
      "prompt_note": "Akari pauses at the entrance in a white hoodie, gripping one sleeve while half-turned back with warm hesitation.",
      "avoid_note": "Do not make this sad or abandoned; the pause is affectionate and positive.",
      "priority": "promising"
    },
    {
      "slot_order": 24,
      "slug": "hallway-half-turn",
      "japanese_title": "廊下で半分だけ振り返る",
      "distance": "over_shoulder",
      "positive_tone": "closeness",
      "gesture_focus": "posture",
      "scene": "entrance",
      "composition": "wider_body",
      "motion": {"verb": "twist", "body_part": "torso and feet", "readable_change": "feet face away while the torso turns halfway back"},
      "prompt_note": "Akari in a simple hallway half-turns back, feet still pointing away, white hoodie showing the body twist.",
      "avoid_note": "Avoid empty melancholy hallway mood; keep the lighting warm and familiar.",
      "priority": "hold"
    },
    {
      "slot_order": 25,
      "slug": "sleeve-tug-near",
      "japanese_title": "近くで袖をちょっと引く",
      "distance": "one_step_close",
      "positive_tone": "small_dependence",
      "gesture_focus": "sleeve",
      "scene": "room",
      "composition": "half_body",
      "motion": {"verb": "pull", "body_part": "sleeve and hand", "readable_change": "one hand tugs the hoodie sleeve close to the viewer"},
      "prompt_note": "Akari stands one step close in a white hoodie, gently tugging a sleeve as if to get attention, shy and happy.",
      "avoid_note": "Keep the tug visible without making the hand oversized or distorted.",
      "priority": "promising"
    },
    {
      "slot_order": 26,
      "slug": "peek-in-close",
      "japanese_title": "近くから覗き込む",
      "distance": "one_step_close",
      "positive_tone": "reassurance",
      "gesture_focus": "posture",
      "scene": "desk",
      "composition": "half_body",
      "motion": {"verb": "reach", "body_part": "torso and shoulders", "readable_change": "her torso leans into the viewer's space while shoulders follow"},
      "prompt_note": "Akari peeks in from one step close beside a desk, white hoodie shoulders leaning forward to check in warmly.",
      "avoid_note": "Avoid extreme perspective; the body lean should be readable and natural.",
      "priority": "promising"
    },
    {
      "slot_order": 27,
      "slug": "almost-says-step",
      "japanese_title": "言いかけて一歩近づく",
      "distance": "one_step_close",
      "positive_tone": "shyness",
      "gesture_focus": "posture",
      "scene": "room",
      "composition": "knee_up",
      "motion": {"verb": "lean", "body_part": "feet and torso", "readable_change": "one foot steps closer while the torso follows before speaking"},
      "prompt_note": "Akari in a white hoodie takes one small step closer before saying something, shy happiness carried by feet and torso.",
      "avoid_note": "Do not make the moment dramatic; keep it ordinary and close.",
      "priority": "promising"
    },
    {
      "slot_order": 28,
      "slug": "hand-foreground-smile",
      "japanese_title": "手元だけ少し手前に来る",
      "distance": "one_step_close",
      "positive_tone": "closeness",
      "gesture_focus": "hand",
      "scene": "room",
      "composition": "half_body",
      "motion": {"verb": "reach", "body_part": "hand and sleeve", "readable_change": "one hand enters the foreground while the sleeve remains connected"},
      "prompt_note": "Akari reaches one simple hand slightly toward the viewer from a white hoodie sleeve, close and happy.",
      "avoid_note": "High hand-risk slot; avoid large lens-distorted fingers and merged joints.",
      "priority": "seed"
    },
    {
      "slot_order": 29,
      "slug": "close-small-laugh",
      "japanese_title": "近くで小さく笑って肩が揺れる",
      "distance": "one_step_close",
      "positive_tone": "joy",
      "gesture_focus": "shoulder",
      "scene": "room",
      "composition": "upper_body",
      "motion": {"verb": "bounce", "body_part": "shoulders", "readable_change": "a small laugh lifts one shoulder and sleeve"},
      "prompt_note": "Akari laughs quietly from one step close, shoulder and sleeve lifting with the small motion.",
      "avoid_note": "This can collapse into expression-only; require visible shoulder movement.",
      "priority": "hold"
    },
    {
      "slot_order": 30,
      "slug": "step-back-bashful",
      "japanese_title": "照れて半歩だけ戻る",
      "distance": "one_step_close",
      "positive_tone": "shyness",
      "gesture_focus": "feet",
      "scene": "room",
      "composition": "knee_up",
      "motion": {"verb": "pull", "body_part": "feet and torso", "readable_change": "one foot and the torso pull back slightly while she remains happy"},
      "prompt_note": "Akari shyly pulls back half a step in a white hoodie, still warm and happy, with knees and torso showing the retreat.",
      "avoid_note": "Avoid making the retreat fearful or negative.",
      "priority": "seed"
    },
    {
      "slot_order": 31,
      "slug": "knees-hug-soft",
      "japanese_title": "膝を抱えて安心する",
      "distance": "relaxed",
      "positive_tone": "relaxation",
      "gesture_focus": "knee",
      "scene": "sofa",
      "composition": "knee_up",
      "motion": {"verb": "release", "body_part": "knees and arms", "readable_change": "arms gather around the knees as her posture settles"},
      "prompt_note": "Akari sits relaxed on a sofa in a white hoodie, arms around her knees with a safe happy feeling.",
      "avoid_note": "Keep the age impression adult and proportions healthy; avoid childish smallness.",
      "priority": "promising"
    },
    {
      "slot_order": 32,
      "slug": "sleepy-head-tilt",
      "japanese_title": "眠くて頭が少し傾く",
      "distance": "relaxed",
      "positive_tone": "relaxation",
      "gesture_focus": "posture",
      "scene": "sofa",
      "composition": "half_body",
      "motion": {"verb": "release", "body_part": "head and shoulders", "readable_change": "her head tilts as the shoulders loosen with sleepiness"},
      "prompt_note": "Akari grows sleepy on a sofa in a white hoodie, head tilting and shoulders soft, content rather than sad.",
      "avoid_note": "Avoid childish drowsiness; keep it gentle adult tiredness.",
      "priority": "promising"
    },
    {
      "slot_order": 33,
      "slug": "desk-nap-sleeve",
      "japanese_title": "机に伏せて袖に頬を乗せる",
      "distance": "relaxed",
      "positive_tone": "relaxation",
      "gesture_focus": "sleeve",
      "scene": "desk",
      "composition": "half_body",
      "motion": {"verb": "release", "body_part": "head and sleeves", "readable_change": "her cheek settles onto folded sleeves on the desk"},
      "prompt_note": "Akari rests her cheek on folded white hoodie sleeves at a desk, content and sleepy, with the settling motion visible.",
      "avoid_note": "Desk must stay textless; do not crop into a face-only sleepy expression.",
      "priority": "promising"
    },
    {
      "slot_order": 34,
      "slug": "sofa-feet-tucked",
      "japanese_title": "ソファで足を寄せる",
      "distance": "relaxed",
      "positive_tone": "relaxation",
      "gesture_focus": "feet",
      "scene": "sofa",
      "composition": "wider_body",
      "motion": {"verb": "pull", "body_part": "feet and knees", "readable_change": "feet tuck closer while knees angle comfortably"},
      "prompt_note": "Akari tucks her feet closer on a sofa, white hoodie relaxed, comfortable and happy.",
      "avoid_note": "Keep legs modest and anatomy clear; avoid awkward foreshortening.",
      "priority": "seed"
    },
    {
      "slot_order": 35,
      "slug": "sleeve-grip-relief",
      "japanese_title": "安心して袖を握る",
      "distance": "relaxed",
      "positive_tone": "reassurance",
      "gesture_focus": "sleeve",
      "scene": "room",
      "composition": "half_body",
      "motion": {"verb": "release", "body_part": "hand and shoulders", "readable_change": "the hand grips the sleeve while shoulders visibly settle"},
      "prompt_note": "Akari grips one white hoodie sleeve as relief settles into her shoulders, warm and safe.",
      "avoid_note": "Avoid worry-heavy expression; this is relief after comfort arrives.",
      "priority": "seed"
    },
    {
      "slot_order": 36,
      "slug": "chair-curl-smile",
      "japanese_title": "椅子の上で小さくくつろぐ",
      "distance": "relaxed",
      "positive_tone": "relaxation",
      "gesture_focus": "posture",
      "scene": "room",
      "composition": "knee_up",
      "motion": {"verb": "release", "body_part": "torso and knees", "readable_change": "torso and knees settle into a compact chair posture"},
      "prompt_note": "Akari sits compactly on a chair in a white hoodie, relaxed and happy, with torso and knees showing the settling posture.",
      "avoid_note": "Avoid making her look childlike or too small in the chair.",
      "priority": "hold"
    }
  ]
}
```

- [ ] **Step 2: Validate JSON syntax**

Run:

```bash
python -m json.tool source/manifests/tonari-no-shigusa/gesture-slots.json >/tmp/tonari-no-shigusa-slots.json
```

Expected: exit `0` and no stderr.

- [ ] **Step 3: Run the contract test and confirm the slot assertions pass while request/script assertions still fail**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_shigusa_contract
```

Expected: `FAILED` because `generation-requests.json` and package scripts are still missing; no failures should mention invalid slot count, distance count, priority count, or slot field names.

- [ ] **Step 4: Commit the slot manifest**

```bash
git add source/manifests/tonari-no-shigusa/gesture-slots.json
git commit -m "feat: add tonari no shigusa gesture slots"
```

## Task 3: Add Generation Request Builder And Package Script

**Files:**

- Create: `scripts/build_tonari_no_shigusa_generation_requests.py`
- Create: `source/manifests/tonari-no-shigusa/generation-requests.json`
- Modify: `package.json`
- Test: `tests/test_tonari_no_shigusa_contract.py`

- [ ] **Step 1: Add the package script entries**

Modify `package.json` scripts by adding these two entries near the other build scripts:

```json
"build:shigusa:requests": "uv run python scripts/build_tonari_no_shigusa_generation_requests.py",
"build:shigusa:contact-sheet": "uv run python scripts/build_tonari_no_shigusa_contact_sheet.py",
```

- [ ] **Step 2: Write the request builder**

Create `scripts/build_tonari_no_shigusa_generation_requests.py`:

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/tonari-no-shigusa"
SLOT_MANIFEST = MANIFEST_DIR / "gesture-slots.json"
OUTPUT = MANIFEST_DIR / "generation-requests.json"
DEFAULT_DATE = "20260706"
COLLECTION_ID = "akari-v1.1-tonari-no-shigusa"
TITLE = "となりのしぐさ"
REFERENCE_PACK_VERSION = "tonari-no-akari-identity-v1"
PROMPT_TEMPLATE_VERSION = "tonari_shigusa_motion_lock_v1"
REFERENCE_PACK_INPUTS = [
    "source/references/tonari-no-akari/identity-face-hair.webp",
    "source/references/tonari-no-akari/identity-body-base.webp",
    "source/references/tonari-no-akari/identity-basic-outfit.webp",
    "source/references/tonari-no-akari/identity-side-view.webp",
]
IDENTITY_LOCK = (
    "Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, "
    "not glamorous, not model-like, not pin-up, not childlike; short fluffy "
    "light-brown bob with airy uneven ends and soft side bangs; warm amber eyes, "
    "rounded cheeks, compact rounded chin, small subtle nose and mouth; pale-blue "
    "crossed hairpins/ribbon-like clips on character-left side when visible; "
    "petite/slender healthy adult proportions; white hoodie as the primary outfit anchor."
)
TEXT_BAN = (
    "No image-internal readable text, no logos, no watermarks, no frame, no border, "
    "no panel layout."
)
ACCEPTANCE = (
    "Must preserve Akari identity, adult age impression, white hoodie continuity, "
    "clean anatomy, happy positive tone, and Motion Gate readability; must be "
    "not another facial-expression sheet. No image-internal readable text, no logos, "
    "no watermarks, no frame, no border, no panel layout."
)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as source_file:
        return json.load(source_file)


def dump_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def risk_profile(slot: dict) -> dict:
    hand_risk = "high" if slot["gesture_focus"] == "hand" else "medium"
    motion_risk = "high" if slot["composition"] == "upper_body" else "medium"
    return {
        "identity_risk": "high",
        "hand_risk": hand_risk,
        "motion_readability_risk": motion_risk,
        "text_logo_watermark_risk": "medium",
    }


def build_prompt(slot: dict) -> str:
    motion = slot["motion"]
    return (
        f"Create one A4 portrait draft for Tonari no Shigusa / {slot['japanese_title']}: "
        f"{slot['prompt_note']} Motion Gate: show a clear {motion['verb']} motion through "
        f"{motion['body_part']}; the readable body change is that {motion['readable_change']}. "
        f"Distance category: {slot['distance']}. Positive tone: {slot['positive_tone']}. "
        f"Gesture focus: {slot['gesture_focus']}. Scene: {slot['scene']}. "
        f"Composition: {slot['composition']}; favor half-body to knee-up body readability "
        f"over a face close-up. Avoid: {slot['avoid_note']} {IDENTITY_LOCK} "
        f"Keep the gesture readable from the body first, not only the face. {TEXT_BAN}"
    )


def build_request(slot: dict, date_prefix: str) -> dict:
    slug = slot["slug"]
    return {
        "id": f"request:tonari-shigusa-{slug}",
        "slot_order": slot["slot_order"],
        "slot": slug,
        "japanese_title": slot["japanese_title"],
        "distance": slot["distance"],
        "positive_tone": slot["positive_tone"],
        "gesture_focus": slot["gesture_focus"],
        "scene": slot["scene"],
        "composition": slot["composition"],
        "motion": slot["motion"],
        "target_path": f"source/generated/tonari-no-shigusa/{date_prefix}_{slug}_v1.webp",
        "reference_pack_inputs": REFERENCE_PACK_INPUTS,
        "prompt_template_version": PROMPT_TEMPLATE_VERSION,
        "reference_pack_version": REFERENCE_PACK_VERSION,
        "prompt": build_prompt(slot),
        "acceptance": ACCEPTANCE,
        "risk_profile": risk_profile(slot),
        "review_plan": {
            "initial_status": "draft_candidate",
            "first_pass": "Place in a Tonari no Shigusa contact sheet before any finishing pass.",
            "motion_gate": "Reject or regenerate if the gesture reads as a static portrait instead of body motion.",
            "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
            "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, or anatomy defects.",
            "humanization": "Use Humanization Pass only after the gesture and anatomy are structurally valid.",
        },
    }


def build_manifest(slot_manifest: dict, date_prefix: str) -> dict:
    promising = [
        slot
        for slot in slot_manifest["slots"]
        if slot["priority"] == "promising"
    ]
    return {
        "schema_version": 1,
        "collection_id": COLLECTION_ID,
        "title": TITLE,
        "reference_pack_version": REFERENCE_PACK_VERSION,
        "prompt_template_version": PROMPT_TEMPLATE_VERSION,
        "source_slots_manifest": "source/manifests/tonari-no-shigusa/gesture-slots.json",
        "batch_policy": {
            "request_source": "promising_slots_only",
            "review_order": "contact_sheet_before_finishing",
            "heavy_pdf_or_ocr_audit": "not_applicable_until_pdf_exists",
        },
        "requests": [
            build_request(slot, date_prefix)
            for slot in promising
        ],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slot-manifest", type=Path, default=SLOT_MANIFEST)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--date-prefix", default=DEFAULT_DATE)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    slot_manifest = load_json(args.slot_manifest)
    manifest = build_manifest(slot_manifest, args.date_prefix)
    dump_json(args.output, manifest)
    print(f"tonari no shigusa requests written: {len(manifest['requests'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 3: Generate the request manifest**

Run:

```bash
npm run build:shigusa:requests
```

Expected:

```text
tonari no shigusa requests written: 18
```

- [ ] **Step 4: Validate JSON syntax**

Run:

```bash
python -m json.tool source/manifests/tonari-no-shigusa/generation-requests.json >/tmp/tonari-no-shigusa-requests.json
```

Expected: exit `0` and no stderr.

- [ ] **Step 5: Run the shigusa contract test**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_shigusa_contract
```

Expected: `OK`.

- [ ] **Step 6: Commit the builder and request manifest**

```bash
git add package.json scripts/build_tonari_no_shigusa_generation_requests.py source/manifests/tonari-no-shigusa/generation-requests.json
git commit -m "feat: add tonari no shigusa generation requests"
```

## Task 4: Add Contact Sheet Script

**Files:**

- Create: `tests/test_tonari_no_shigusa_contact_sheet.py`
- Create: `scripts/build_tonari_no_shigusa_contact_sheet.py`
- Test: `tests/test_tonari_no_shigusa_contact_sheet.py`

- [ ] **Step 1: Write the failing contact-sheet test**

Create `tests/test_tonari_no_shigusa_contact_sheet.py`:

```python
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build_tonari_no_shigusa_contact_sheet.py"


def load_script():
    spec = importlib.util.spec_from_file_location("build_tonari_no_shigusa_contact_sheet", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TonariNoShigusaContactSheetTest(unittest.TestCase):
    def setUp(self):
        self.script = load_script()

    def test_contact_sheet_is_created_from_generated_images(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image_dir = root / "source/generated/tonari-no-shigusa"
            image_dir.mkdir(parents=True)
            image_a = image_dir / "20260706_sleeve-near-bench_v1.webp"
            image_b = image_dir / "20260706_desk-lean-forward_v1.webp"
            Image.new("RGB", (640, 960), (240, 230, 220)).save(image_a)
            Image.new("RGB", (640, 960), (220, 235, 240)).save(image_b)

            manifest = {
                "requests": [
                    {
                        "slot_order": 1,
                        "slot": "sleeve-near-bench",
                        "japanese_title": "隣で袖をそっと寄せる",
                        "distance": "beside",
                        "motion": {"verb": "pull"},
                        "target_path": "source/generated/tonari-no-shigusa/20260706_sleeve-near-bench_v1.webp",
                    },
                    {
                        "slot_order": 7,
                        "slot": "desk-lean-forward",
                        "japanese_title": "机越しに少し身を乗り出す",
                        "distance": "across",
                        "motion": {"verb": "reach"},
                        "target_path": "source/generated/tonari-no-shigusa/20260706_desk-lean-forward_v1.webp",
                    },
                ]
            }
            manifest_path = root / "source/manifests/tonari-no-shigusa/generation-requests.json"
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            output = root / "evidence/tonari-no-shigusa/contact-sheets/test.webp"

            result = self.script.main(
                [
                    "--root",
                    str(root),
                    "--manifest",
                    str(manifest_path),
                    "--output",
                    str(output),
                    "--columns",
                    "2",
                    "--thumb-width",
                    "180",
                ]
            )

            self.assertEqual(0, result)
            self.assertTrue(output.is_file())
            with Image.open(output) as sheet:
                self.assertGreater(sheet.width, 300)
                self.assertGreater(sheet.height, 250)

    def test_missing_images_fail_with_clear_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = {
                "requests": [
                    {
                        "slot_order": 1,
                        "slot": "missing-slot",
                        "japanese_title": "足りない画像",
                        "distance": "beside",
                        "motion": {"verb": "pull"},
                        "target_path": "source/generated/tonari-no-shigusa/missing.webp",
                    }
                ]
            }
            manifest_path = root / "requests.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaises(SystemExit) as raised:
                self.script.main(
                    [
                        "--root",
                        str(root),
                        "--manifest",
                        str(manifest_path),
                        "--output",
                        str(root / "sheet.webp"),
                    ]
                )

            self.assertEqual(1, raised.exception.code)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the contact-sheet test and confirm it fails on missing script**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_shigusa_contact_sheet
```

Expected: `FAILED` because `scripts/build_tonari_no_shigusa_contact_sheet.py` does not exist.

- [ ] **Step 3: Implement the contact-sheet script**

Create `scripts/build_tonari_no_shigusa_contact_sheet.py`:

```python
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "source/manifests/tonari-no-shigusa/generation-requests.json"
DEFAULT_OUTPUT = ROOT / "evidence/tonari-no-shigusa/contact-sheets/20260706_first-promising-batch.webp"
BACKGROUND = (248, 247, 243)
CARD_BACKGROUND = (255, 255, 255)
TEXT = (30, 30, 30)
MUTED = (92, 92, 92)
GAP = 18
LABEL_HEIGHT = 74


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as source_file:
        return json.load(source_file)


def font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except OSError:
        return ImageFont.load_default()


def fit_image(image: Image.Image, thumb_width: int) -> Image.Image:
    ratio = thumb_width / image.width
    thumb_height = round(image.height * ratio)
    return image.convert("RGB").resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)


def draw_label(draw: ImageDraw.ImageDraw, x: int, y: int, request: dict) -> None:
    title_font = font(18)
    meta_font = font(14)
    order = f"{request['slot_order']:02d}"
    draw.text((x, y), f"{order} {request['slot']}", fill=TEXT, font=title_font)
    draw.text((x, y + 24), request["japanese_title"], fill=TEXT, font=meta_font)
    motion = request.get("motion", {}).get("verb", "")
    draw.text((x, y + 46), f"{request['distance']} / {motion}", fill=MUTED, font=meta_font)


def load_entries(root: Path, manifest_path: Path, thumb_width: int) -> list[tuple[dict, Image.Image]]:
    manifest = load_json(manifest_path)
    entries = []
    missing = []
    for request in manifest["requests"]:
        image_path = root / request["target_path"]
        if not image_path.is_file():
            missing.append(str(image_path))
            continue
        with Image.open(image_path) as image:
            entries.append((request, fit_image(image, thumb_width)))
    if missing:
        for path in missing:
            print(f"missing generated image: {path}")
        raise SystemExit(1)
    return entries


def build_sheet(entries: list[tuple[dict, Image.Image]], columns: int) -> Image.Image:
    if not entries:
        raise SystemExit("no entries to render")
    thumb_width = entries[0][1].width
    thumb_height = max(image.height for _request, image in entries)
    rows = math.ceil(len(entries) / columns)
    card_width = thumb_width
    card_height = thumb_height + LABEL_HEIGHT
    width = columns * card_width + (columns + 1) * GAP
    height = rows * card_height + (rows + 1) * GAP
    sheet = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(sheet)

    for index, (request, image) in enumerate(entries):
        row = index // columns
        column = index % columns
        x = GAP + column * (card_width + GAP)
        y = GAP + row * (card_height + GAP)
        draw.rectangle((x, y, x + card_width, y + card_height), fill=CARD_BACKGROUND)
        sheet.paste(image, (x, y))
        draw_label(draw, x + 8, y + thumb_height + 8, request)

    return sheet


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--columns", type=int, default=6)
    parser.add_argument("--thumb-width", type=int, default=260)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    entries = load_entries(args.root, args.manifest, args.thumb_width)
    sheet = build_sheet(entries, args.columns)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output, quality=92, method=6)
    print(f"tonari no shigusa contact sheet written: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the contact-sheet test and confirm it passes**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_shigusa_contact_sheet
```

Expected: `OK`.

- [ ] **Step 5: Commit the contact-sheet script**

```bash
git add tests/test_tonari_no_shigusa_contact_sheet.py scripts/build_tonari_no_shigusa_contact_sheet.py
git commit -m "feat: add tonari no shigusa contact sheet builder"
```

## Task 5: Verify The Whole Lightweight Workflow

**Files:**

- Modify only if verification reveals a real defect in files from Tasks 1 through 4.

- [ ] **Step 1: Regenerate request manifest**

Run:

```bash
npm run build:shigusa:requests
```

Expected:

```text
tonari no shigusa requests written: 18
```

- [ ] **Step 2: Validate JSON files**

Run:

```bash
python -m json.tool source/manifests/tonari-no-shigusa/gesture-slots.json >/tmp/tonari-no-shigusa-slots.json
python -m json.tool source/manifests/tonari-no-shigusa/generation-requests.json >/tmp/tonari-no-shigusa-requests.json
```

Expected: both commands exit `0` and print no stderr.

- [ ] **Step 3: Run targeted Python tests**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_shigusa_contract tests.test_tonari_no_shigusa_contact_sheet
```

Expected: `OK`.

- [ ] **Step 4: Run all Python tests**

Run:

```bash
npm run test:python
```

Expected: unittest summary with no failures or errors.

- [ ] **Step 5: Run Markdown lint**

Run:

```bash
npm run lint:md
```

Expected: `Summary: 0 error(s)`.

- [ ] **Step 6: Commit any verification fixes**

If files changed during verification:

```bash
git add package.json scripts/build_tonari_no_shigusa_generation_requests.py scripts/build_tonari_no_shigusa_contact_sheet.py source/manifests/tonari-no-shigusa tests/test_tonari_no_shigusa_contract.py tests/test_tonari_no_shigusa_contact_sheet.py
git commit -m "test: verify tonari no shigusa workflow"
```

If no files changed, do not create an empty commit.

## Task 6: First Image Batch Execution Handoff

**Files:**

- Read: `source/manifests/tonari-no-shigusa/generation-requests.json`
- Create through image generation: `source/generated/tonari-no-shigusa/20260706_<slot>_v1.webp`
- Create through contact sheet script after images exist: `evidence/tonari-no-shigusa/contact-sheets/20260706_first-promising-batch.webp`

- [ ] **Step 1: Read the generated request manifest**

Run:

```bash
jq -r '.requests[] | [.slot_order, .slot, .japanese_title, .target_path] | @tsv' source/manifests/tonari-no-shigusa/generation-requests.json
```

Expected: 18 tab-separated rows, beginning with `1 sleeve-near-bench`.

- [ ] **Step 2: Generate one image per request**

For each request, submit the exact `prompt` field to the image generation tool and save the resulting image to its `target_path`. Generate the first batch in request order so contact-sheet labels match the manifest order.

Use this command to inspect a prompt without printing the whole manifest:

```bash
jq -r '.requests[] | select(.slot == "sleeve-near-bench") | .prompt' source/manifests/tonari-no-shigusa/generation-requests.json
```

Expected: prompt text includes `Motion Gate`, the `pull` motion, Akari identity lock, `white hoodie`, and the text/logo/watermark bans.

- [ ] **Step 3: Build the first contact sheet**

Run after all 18 target images exist:

```bash
npm run build:shigusa:contact-sheet
```

Expected:

```text
tonari no shigusa contact sheet written: /path/to/akari-design/evidence/tonari-no-shigusa/contact-sheets/20260706_first-promising-batch.webp
```

- [ ] **Step 4: Review against Motion Gate**

Open `evidence/tonari-no-shigusa/contact-sheets/20260706_first-promising-batch.webp` and classify each slot as one of:

- `keep`: body motion reads before the title.
- `regenerate`: identity is close, but motion is weak or hand/limb anatomy failed.
- `hold`: good-looking image, but it duplicates `となりの表情` or lacks usable body motion.
- `reject`: hard identity, anatomy, age impression, tone, text/logo, or policy failure.

- [ ] **Step 5: Record first-batch notes**

Create `evidence/tonari-no-shigusa/reviews/20260706_first-batch-motion-review.md` with this structure:

```markdown
# Tonari No Shigusa First Batch Motion Review

## Summary

- Batch: `20260706_first-promising-batch`
- Requests: 18
- Contact sheet: `evidence/tonari-no-shigusa/contact-sheets/20260706_first-promising-batch.webp`

## Decisions

| Slot | Decision | Motion Read | Notes |
| --- | --- | --- | --- |
| sleeve-near-bench | keep | sleeve and elbow movement reads | The sleeve shifts toward the viewer and the elbow draws inward; identity remains stable. |
```

- [ ] **Step 6: Commit generated review artifacts only if the user asks to preserve them**

Generated intermediates normally stay out of git. If the user explicitly asks to keep this first batch in the repository, commit the selected generated images, the contact sheet, and the review note:

```bash
git add source/generated/tonari-no-shigusa evidence/tonari-no-shigusa/contact-sheets evidence/tonari-no-shigusa/reviews
git commit -m "feat: add tonari no shigusa first image batch"
```

## Final Verification Checklist

- `python -m json.tool source/manifests/tonari-no-shigusa/gesture-slots.json`
- `python -m json.tool source/manifests/tonari-no-shigusa/generation-requests.json`
- `npm run build:shigusa:requests`
- `uv run python -m unittest tests.test_tonari_no_shigusa_contract tests.test_tonari_no_shigusa_contact_sheet`
- `npm run test:python`
- `npm run lint:md`

Do not run PDF audits for this phase because no PDF artifact is added.
