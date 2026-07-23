# Akari v1.1 Tonari No Coordinate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first image-first `となりのコーデ` workflow: a 36-slot coordinate map, a generated request manifest for the first 12 promising outfits, and a contact-sheet path for outfit-balance review.

**Architecture:** Keep `coordinate-slots.json` as the source of truth for season, scene, outfit family, mint accent, and priority. A small Python builder derives `generation-requests.json` from `priority == "promising"` slots, and a separate Pillow contact-sheet script reviews generated candidate image files without adding PDF or booklet rendering.

**Tech Stack:** Python 3.11, `unittest`, JSON manifests, Pillow, `uv run python`, existing npm scripts.

---

## Scope Check

The approved design covers one subsystem: image-first coordinate exploration.
This plan does not add PDF rendering, gallery output, image finishing automation,
or public publishing. Generated image files stay out of git unless the user
explicitly asks to preserve final deliverables.

## Current Context

- Approved design spec:
  `docs/superpowers/specs/2026-07-06-akari-v1-1-tonari-no-coordinate-design.md`
- Existing identity references to reuse:
  `source/references/tonari-no-akari/identity-face-hair.webp`,
  `source/references/tonari-no-akari/identity-body-base.webp`,
  `source/references/tonari-no-akari/identity-basic-outfit.webp`, and
  `source/references/tonari-no-akari/identity-side-view.webp`
- New manifest directory:
  `source/manifests/tonari-no-coordinate/`
- New generated draft image directory named in manifests and scripts:
  `source/generated/tonari-no-coordinate/`
- New evidence output directory for contact sheets:
  `evidence/tonari-no-coordinate/contact-sheets/`
- This plan intentionally stops before actual image generation.

## File Structure

- Create `tests/test_tonari_no_coordinate_contract.py`
  - Contract tests for slot metadata, generated requests, package scripts,
    identity locks, coordinate gates, text bans, and outfit-family balance.
- Create `source/manifests/tonari-no-coordinate/coordinate-slots.json`
  - Source-of-truth 36-slot coordinate map.
- Create `scripts/build_tonari_no_coordinate_generation_requests.py`
  - Deterministically derives generation requests for `promising` slots.
- Create `source/manifests/tonari-no-coordinate/generation-requests.json`
  - Derived first-batch request manifest.
- Create `tests/test_tonari_no_coordinate_contact_sheet.py`
  - Unit tests for contact-sheet generation using temporary images.
- Create `scripts/build_tonari_no_coordinate_contact_sheet.py`
  - Builds a labeled sheet from existing generated candidate images.
- Modify `package.json`
  - Add `build:coordinate:requests` and `build:coordinate:contact-sheet`.

## Task 1: Add The Failing Coordinate Contract Test

**Files:**

- Create: `tests/test_tonari_no_coordinate_contract.py`

- [ ] **Step 1: Write the failing contract test**

Create `tests/test_tonari_no_coordinate_contract.py`:

```python
import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/tonari-no-coordinate"
SLOT_MANIFEST = MANIFEST_DIR / "coordinate-slots.json"
GENERATION_REQUESTS = MANIFEST_DIR / "generation-requests.json"
COLLECTION_ID = "akari-v1.1-tonari-no-coordinate"
TITLE = "となりのコーデ"
REFERENCE_PACK_VERSION = "tonari-no-akari-identity-v1"
PROMPT_TEMPLATE_VERSION = "tonari_coordinate_identity_lock_v1"
REFERENCE_PACK_INPUTS = [
    "source/references/tonari-no-akari/identity-face-hair.webp",
    "source/references/tonari-no-akari/identity-body-base.webp",
    "source/references/tonari-no-akari/identity-basic-outfit.webp",
    "source/references/tonari-no-akari/identity-side-view.webp",
]
EXPECTED_FAMILY_COUNTS = {
    "layering": 10,
    "one_piece_skirt": 9,
    "knit_soft": 6,
    "roomwear_relaxed": 5,
    "shirt_blouse_pants": 4,
    "hoodie_baseline": 2,
}
EXPECTED_PROMISING_COUNTS = {
    "layering": 4,
    "one_piece_skirt": 3,
    "knit_soft": 2,
    "roomwear_relaxed": 1,
    "shirt_blouse_pants": 1,
    "hoodie_baseline": 1,
}
EXPECTED_PRIORITY_COUNTS = {
    "promising": 12,
    "seed": 18,
    "hold": 6,
}
ALLOWED_SEASONS = {"spring", "summer", "autumn", "winter", "rain", "night", "all_season"}
ALLOWED_SCENES = {
    "room",
    "window",
    "sofa",
    "desk",
    "walk_home",
    "cafe",
    "station",
    "riverside",
    "doorway",
    "shopping_street",
    "kitchen",
    "veranda",
}
ALLOWED_COMPOSITIONS = {"close", "upper_body", "half_body", "knee_up", "full_body"}
ALLOWED_TONES = {
    "everyday_cute",
    "relaxed",
    "lightly_dressed_up",
    "quiet",
    "warm",
    "fresh",
}
JAPANESE_TEXT = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
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
BANNED_PROMPT_FRAGMENTS = {
    "school uniform",
    "teenage",
    "little girl",
    "young child",
    "child body",
    "childlike body",
    "pinup",
    "glamour model",
    "brand logo",
}


def load_json(path):
    with path.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


class TonariNoCoordinateContractTest(unittest.TestCase):
    def test_package_scripts_expose_coordinate_helpers(self):
        package_json = load_json(ROOT / "package.json")
        scripts = package_json["scripts"]

        self.assertEqual(
            "uv run python scripts/build_tonari_no_coordinate_generation_requests.py",
            scripts["build:coordinate:requests"],
        )
        self.assertEqual(
            "uv run python scripts/build_tonari_no_coordinate_contact_sheet.py",
            scripts["build:coordinate:contact-sheet"],
        )

    def test_slot_manifest_exists_and_records_strategy(self):
        self.assertTrue(SLOT_MANIFEST.is_file(), f"missing manifest: {SLOT_MANIFEST}")
        manifest = load_json(SLOT_MANIFEST)

        self.assertEqual(1, manifest["schema_version"])
        self.assertEqual(COLLECTION_ID, manifest["collection_id"])
        self.assertEqual(TITLE, manifest["title"])
        self.assertEqual(REFERENCE_PACK_VERSION, manifest["reference_pack_version"])
        self.assertEqual(
            "season_scene_outfit_family",
            manifest["strategy"]["organizing_model"],
        )
        self.assertEqual("daily_plus_lightly_special", manifest["strategy"]["outfit_direction"])
        self.assertEqual("mint_or_pale_blue_every_slot", manifest["strategy"]["identity_accent"])
        self.assertEqual("contact_sheet_before_finishing", manifest["strategy"]["review_order"])
        self.assertEqual("not_in_first_phase", manifest["strategy"]["pdf_policy"])

    def test_slot_map_has_36_balanced_coordinate_slots(self):
        manifest = load_json(SLOT_MANIFEST)
        slots = manifest["slots"]

        self.assertEqual(36, len(slots))
        self.assertEqual(EXPECTED_FAMILY_COUNTS, dict(Counter(slot["outfit_family"] for slot in slots)))
        self.assertEqual(EXPECTED_PRIORITY_COUNTS, dict(Counter(slot["priority"] for slot in slots)))
        self.assertEqual(len(slots), len({slot["slug"] for slot in slots}))

        seasons = {slot["season"] for slot in slots}
        for required_season in ("spring", "summer", "autumn", "winter", "rain", "night"):
            self.assertIn(required_season, seasons)

        for index, slot in enumerate(slots, start=1):
            with self.subTest(slot=slot["slug"]):
                self.assertEqual(index, slot["slot_order"])
                self.assertRegex(slot["slug"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertTrue(JAPANESE_TEXT.search(slot["japanese_title"]))
                self.assertIn(slot["season"], ALLOWED_SEASONS)
                self.assertIn(slot["scene"], ALLOWED_SCENES)
                self.assertIn(slot["outfit_family"], EXPECTED_FAMILY_COUNTS)
                self.assertIn(slot["composition"], ALLOWED_COMPOSITIONS)
                self.assertIn(slot["tone"], ALLOWED_TONES)
                self.assertIn(slot["priority"], EXPECTED_PRIORITY_COUNTS)
                self.assertTrue(slot["outfit_notes"])
                self.assertTrue(slot["mint_accent"])
                self.assertTrue(slot["risk_note"])
                self.assertNotIn("logo", slot["outfit_notes"].lower())
                self.assertNotIn("school uniform", slot["outfit_notes"].lower())
                self.assertNotIn("swimwear", slot["outfit_notes"].lower())

    def test_promising_slots_match_first_batch_distribution(self):
        slots = load_json(SLOT_MANIFEST)["slots"]
        promising = [slot for slot in slots if slot["priority"] == "promising"]

        self.assertEqual(12, len(promising))
        self.assertEqual(
            EXPECTED_PROMISING_COUNTS,
            dict(Counter(slot["outfit_family"] for slot in promising)),
        )
        self.assertEqual(
            [slot["slug"] for slot in promising],
            [
                "spring-cardigan-walk",
                "linen-shirt-window",
                "autumn-short-jacket",
                "rain-light-coat",
                "day-off-one-piece",
                "long-skirt-soft-top",
                "summer-airy-blouse-skirt",
                "winter-warm-knit",
                "ribbed-top-relaxed-skirt",
                "morning-soft-roomwear",
                "clean-blouse-simple-pants",
                "updated-hoodie-cardigan",
            ],
        )

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
        self.assertEqual(12, generation_requests["batch_policy"]["candidate_count"])
        self.assertEqual("contact_sheet_before_finishing", generation_requests["batch_policy"]["review_order"])
        self.assertEqual("not_in_first_phase", generation_requests["batch_policy"]["pdf_policy"])
        self.assertEqual([slot["slug"] for slot in promising_slots], [request["slot"] for request in requests])

        for request, slot in zip(requests, promising_slots, strict=True):
            with self.subTest(slot=slot["slug"]):
                self.assertEqual(f"request:tonari-coordinate-{slot['slug']}", request["id"])
                self.assertEqual(slot["slot_order"], request["coordinate_order"])
                self.assertEqual(slot["japanese_title"], request["japanese_title"])
                self.assertEqual(slot["season"], request["season"])
                self.assertEqual(slot["scene"], request["scene"])
                self.assertEqual(slot["outfit_family"], request["outfit_family"])
                self.assertEqual(slot["outfit_notes"], request["outfit_notes"])
                self.assertEqual(slot["mint_accent"], request["mint_accent"])
                self.assertEqual(slot["composition"], request["composition"])
                self.assertEqual(slot["tone"], request["tone"])
                self.assertEqual(slot["risk_note"], request["risk_note"])
                self.assertEqual(REFERENCE_PACK_INPUTS, request["reference_pack_inputs"])
                self.assertEqual(
                    f"source/generated/tonari-no-coordinate/20260706_{slot['slug']}_v1.webp",
                    request["target_path"],
                )

    def test_generation_prompts_lock_identity_coordinate_and_text_bans(self):
        generation_requests = load_json(GENERATION_REQUESTS)

        for request in generation_requests["requests"]:
            with self.subTest(slot=request["slot"]):
                prompt = request["prompt"].lower()
                acceptance = request["acceptance"].lower()
                combined = f"{prompt} {acceptance}"

                self.assertIn(request["japanese_title"].lower(), request["prompt"].lower())
                self.assertIn(request["season"].replace("_", " "), prompt)
                self.assertIn(request["scene"].replace("_", " "), prompt)
                self.assertIn(request["outfit_notes"].lower(), prompt)
                self.assertIn(request["mint_accent"].lower(), prompt)
                self.assertIn("coordinate gate", acceptance)
                self.assertIn("not a fashion-model sheet", acceptance)

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
                self.assertIn(risk_profile["outfit_drift_risk"], {"medium", "high"})
                self.assertIn(risk_profile["age_impression_risk"], {"medium", "high"})
                self.assertIn(risk_profile["hand_risk"], {"low", "medium", "high"})
                self.assertEqual("medium", risk_profile["text_logo_watermark_risk"])

                review_plan = request["review_plan"]
                self.assertEqual("draft_candidate", review_plan["initial_status"])
                self.assertIn("contact sheet", review_plan["first_pass"])
                self.assertIn("Coordinate Gate", review_plan["coordinate_gate"])
                self.assertIn("akari-v1-1-image-review", review_plan["strict_review"])
                self.assertIn("Correction Pass", review_plan["correction"])
                self.assertIn("Humanization Pass", review_plan["humanization"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and confirm it fails on missing files/scripts**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_coordinate_contract
```

Expected: `FAILED` with a missing `build:coordinate:requests` key or missing
`coordinate-slots.json`, depending on assertion order.

- [ ] **Step 3: Commit the failing test**

```bash
git add tests/test_tonari_no_coordinate_contract.py
git commit -m "test: add tonari no coordinate contract"
```

## Task 2: Add The 36-Slot Coordinate Map

**Files:**

- Create: `source/manifests/tonari-no-coordinate/coordinate-slots.json`
- Test: `tests/test_tonari_no_coordinate_contract.py`

- [ ] **Step 1: Create the slot manifest**

Create `source/manifests/tonari-no-coordinate/coordinate-slots.json`:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.1-tonari-no-coordinate",
  "title": "となりのコーデ",
  "reference_pack_version": "tonari-no-akari-identity-v1",
  "strategy": {
    "organizing_model": "season_scene_outfit_family",
    "outfit_direction": "daily_plus_lightly_special",
    "identity_accent": "mint_or_pale_blue_every_slot",
    "review_order": "contact_sheet_before_finishing",
    "pdf_policy": "not_in_first_phase"
  },
  "slots": [
    {
      "slot_order": 1,
      "slug": "spring-cardigan-walk",
      "japanese_title": "春のカーディガン",
      "season": "spring",
      "scene": "walk_home",
      "outfit_family": "layering",
      "outfit_notes": "Light oatmeal cardigan over a simple ivory top and soft navy skirt.",
      "mint_accent": "Pale-blue crossed hairpins plus a tiny mint bag charm.",
      "composition": "half_body",
      "tone": "everyday_cute",
      "priority": "promising",
      "risk_note": "Keep the cardigan adult and relaxed; avoid student styling."
    },
    {
      "slot_order": 2,
      "slug": "linen-shirt-window",
      "japanese_title": "窓辺のリネンシャツ",
      "season": "summer",
      "scene": "window",
      "outfit_family": "layering",
      "outfit_notes": "Loose pale linen shirt layer over a muted sage camisole-style inner top and ankle skirt.",
      "mint_accent": "Hairpins and a mint glass cup near the window.",
      "composition": "upper_body",
      "tone": "fresh",
      "priority": "promising",
      "risk_note": "Keep the inner top modest and non-glamorous."
    },
    {
      "slot_order": 3,
      "slug": "autumn-short-jacket",
      "japanese_title": "秋の短いジャケット",
      "season": "autumn",
      "scene": "walk_home",
      "outfit_family": "layering",
      "outfit_notes": "Cropped brown short jacket over a cream knit and dark green long skirt.",
      "mint_accent": "Pale-blue crossed hairpins and a mint zipper pull.",
      "composition": "knee_up",
      "tone": "warm",
      "priority": "promising",
      "risk_note": "Avoid hard fashion-model posing; keep the walk-home mood."
    },
    {
      "slot_order": 4,
      "slug": "rain-light-coat",
      "japanese_title": "雨の日の薄いコート",
      "season": "rain",
      "scene": "doorway",
      "outfit_family": "layering",
      "outfit_notes": "Soft beige light coat over a simple top and charcoal skirt.",
      "mint_accent": "Hairpins plus a mint umbrella handle.",
      "composition": "half_body",
      "tone": "quiet",
      "priority": "promising",
      "risk_note": "Umbrella should not hide the hair ornament or face."
    },
    {
      "slot_order": 5,
      "slug": "evening-cardigan",
      "japanese_title": "夕方の羽織り",
      "season": "night",
      "scene": "station",
      "outfit_family": "layering",
      "outfit_notes": "Long charcoal cardigan over a pale top with a muted lavender skirt.",
      "mint_accent": "Pale-blue crossed hairpins and a mint pass-case strap.",
      "composition": "half_body",
      "tone": "quiet",
      "priority": "seed",
      "risk_note": "Station background must stay unbranded and text-free."
    },
    {
      "slot_order": 6,
      "slug": "winter-duffle-soft",
      "japanese_title": "冬のやわらかダッフル",
      "season": "winter",
      "scene": "walk_home",
      "outfit_family": "layering",
      "outfit_notes": "Soft camel duffle-style coat over a warm knit and long skirt.",
      "mint_accent": "Hairpins plus pale mint mitten trim.",
      "composition": "knee_up",
      "tone": "warm",
      "priority": "seed",
      "risk_note": "Keep the coat simple and adult; avoid school-coat impression."
    },
    {
      "slot_order": 7,
      "slug": "veranda-shirt-cardigan",
      "japanese_title": "ベランダのシャツカーデ",
      "season": "spring",
      "scene": "veranda",
      "outfit_family": "layering",
      "outfit_notes": "Thin sky-grey shirt cardigan over a white ribbed top and beige skirt.",
      "mint_accent": "Hairpins and pale mint nail color.",
      "composition": "upper_body",
      "tone": "fresh",
      "priority": "seed",
      "risk_note": "Do not let the white top repeat the default hoodie silhouette."
    },
    {
      "slot_order": 8,
      "slug": "cafe-soft-blazer",
      "japanese_title": "カフェの柔らかブレザー",
      "season": "all_season",
      "scene": "cafe",
      "outfit_family": "layering",
      "outfit_notes": "Unstructured soft navy blazer over a pale knit and relaxed skirt.",
      "mint_accent": "Pale-blue crossed hairpins and a mint spoon rest.",
      "composition": "half_body",
      "tone": "lightly_dressed_up",
      "priority": "seed",
      "risk_note": "Work-adjacent is fine, but avoid occupation-uniform feeling."
    },
    {
      "slot_order": 9,
      "slug": "shopping-denim-jacket",
      "japanese_title": "買い物帰りのデニムジャケット",
      "season": "autumn",
      "scene": "shopping_street",
      "outfit_family": "layering",
      "outfit_notes": "Dark denim jacket over a soft cream top and rust-colored skirt.",
      "mint_accent": "Hairpins plus a small mint key charm on a plain tote.",
      "composition": "knee_up",
      "tone": "everyday_cute",
      "priority": "seed",
      "risk_note": "Background signs must be blurred or absent with no readable text."
    },
    {
      "slot_order": 10,
      "slug": "riverside-thin-coat",
      "japanese_title": "川沿いの薄いコート",
      "season": "spring",
      "scene": "riverside",
      "outfit_family": "layering",
      "outfit_notes": "Light grey spring coat over a soft blue-grey knit and pleated skirt.",
      "mint_accent": "Pale-blue crossed hairpins and mint scarf edging.",
      "composition": "full_body",
      "tone": "fresh",
      "priority": "hold",
      "risk_note": "Full body raises footwear and proportion risk."
    },
    {
      "slot_order": 11,
      "slug": "day-off-one-piece",
      "japanese_title": "休日のワンピース",
      "season": "spring",
      "scene": "cafe",
      "outfit_family": "one_piece_skirt",
      "outfit_notes": "Soft moss-green one-piece dress with a small cream cardigan.",
      "mint_accent": "Hairpins plus a pale mint ribbon detail on a simple bag.",
      "composition": "knee_up",
      "tone": "lightly_dressed_up",
      "priority": "promising",
      "risk_note": "Keep it day-off casual, not formal datewear."
    },
    {
      "slot_order": 12,
      "slug": "long-skirt-soft-top",
      "japanese_title": "ロングスカートと柔らかトップス",
      "season": "all_season",
      "scene": "room",
      "outfit_family": "one_piece_skirt",
      "outfit_notes": "Soft taupe top tucked lightly into a deep teal long skirt.",
      "mint_accent": "Pale-blue crossed hairpins and mint socks peeking out.",
      "composition": "half_body",
      "tone": "relaxed",
      "priority": "promising",
      "risk_note": "Avoid repeating the existing grey-skirt structure."
    },
    {
      "slot_order": 13,
      "slug": "summer-airy-blouse-skirt",
      "japanese_title": "夏の軽いブラウス",
      "season": "summer",
      "scene": "window",
      "outfit_family": "one_piece_skirt",
      "outfit_notes": "Airy pale yellow blouse with a navy midi skirt.",
      "mint_accent": "Hairpins and a thin mint bracelet.",
      "composition": "upper_body",
      "tone": "fresh",
      "priority": "promising",
      "risk_note": "Blouse should not become sheer or glamorous."
    },
    {
      "slot_order": 14,
      "slug": "pleated-skirt-cardigan",
      "japanese_title": "大人めプリーツ",
      "season": "autumn",
      "scene": "station",
      "outfit_family": "one_piece_skirt",
      "outfit_notes": "Muted wine pleated skirt with a grown-up beige cardigan and simple top.",
      "mint_accent": "Pale-blue crossed hairpins and mint pass-case edge.",
      "composition": "knee_up",
      "tone": "lightly_dressed_up",
      "priority": "seed",
      "risk_note": "Avoid school-uniform silhouette."
    },
    {
      "slot_order": 15,
      "slug": "shopping-street-skirt",
      "japanese_title": "商店街のスカート",
      "season": "all_season",
      "scene": "shopping_street",
      "outfit_family": "one_piece_skirt",
      "outfit_notes": "Soft black skirt with a warm beige top and plain canvas tote.",
      "mint_accent": "Hairpins and a mint tote charm.",
      "composition": "knee_up",
      "tone": "everyday_cute",
      "priority": "seed",
      "risk_note": "No readable storefront signs or printed tote graphics."
    },
    {
      "slot_order": 16,
      "slug": "night-knit-skirt",
      "japanese_title": "夜のニットスカート",
      "season": "night",
      "scene": "walk_home",
      "outfit_family": "one_piece_skirt",
      "outfit_notes": "Dark knit skirt with a soft cream top and short warm cardigan.",
      "mint_accent": "Pale-blue crossed hairpins and mint reflective bag charm.",
      "composition": "half_body",
      "tone": "quiet",
      "priority": "seed",
      "risk_note": "Night lighting must keep face and hair identity readable."
    },
    {
      "slot_order": 17,
      "slug": "room-soft-indoor-skirt",
      "japanese_title": "部屋のやわらかスカート",
      "season": "all_season",
      "scene": "sofa",
      "outfit_family": "one_piece_skirt",
      "outfit_notes": "Soft indoor jersey skirt with a relaxed oatmeal pullover.",
      "mint_accent": "Hairpins and pale mint room socks.",
      "composition": "knee_up",
      "tone": "relaxed",
      "priority": "seed",
      "risk_note": "Keep roomwear healthy and non-underwear-like."
    },
    {
      "slot_order": 18,
      "slug": "rain-midi-skirt",
      "japanese_title": "雨上がりのミディスカート",
      "season": "rain",
      "scene": "doorway",
      "outfit_family": "one_piece_skirt",
      "outfit_notes": "Navy midi skirt with a pale knit top and light waterproof jacket.",
      "mint_accent": "Hairpins and a mint umbrella strap.",
      "composition": "full_body",
      "tone": "fresh",
      "priority": "hold",
      "risk_note": "Full-body rain props can obscure outfit continuity."
    },
    {
      "slot_order": 19,
      "slug": "winter-simple-dress",
      "japanese_title": "冬のシンプルワンピ",
      "season": "winter",
      "scene": "room",
      "outfit_family": "one_piece_skirt",
      "outfit_notes": "Simple charcoal knit one-piece dress layered with a cream inner collar.",
      "mint_accent": "Pale-blue crossed hairpins and a small mint pendant.",
      "composition": "half_body",
      "tone": "warm",
      "priority": "hold",
      "risk_note": "Avoid bodycon styling; keep the silhouette soft."
    },
    {
      "slot_order": 20,
      "slug": "winter-warm-knit",
      "japanese_title": "冬のあったかニット",
      "season": "winter",
      "scene": "room",
      "outfit_family": "knit_soft",
      "outfit_notes": "Warm ivory cable knit with a muted blue-grey skirt.",
      "mint_accent": "Hairpins plus a mint mug held low.",
      "composition": "upper_body",
      "tone": "warm",
      "priority": "promising",
      "risk_note": "Hands around the mug must remain simple and readable."
    },
    {
      "slot_order": 21,
      "slug": "ribbed-top-relaxed-skirt",
      "japanese_title": "リブトップの休日",
      "season": "all_season",
      "scene": "desk",
      "outfit_family": "knit_soft",
      "outfit_notes": "Muted clay ribbed top with a relaxed dark skirt.",
      "mint_accent": "Pale-blue crossed hairpins and mint pen cap on the desk.",
      "composition": "half_body",
      "tone": "relaxed",
      "priority": "promising",
      "risk_note": "Ribbed fabric should not read as tight glamour styling."
    },
    {
      "slot_order": 22,
      "slug": "soft-sweater-desk",
      "japanese_title": "机のやわらかセーター",
      "season": "autumn",
      "scene": "desk",
      "outfit_family": "knit_soft",
      "outfit_notes": "Soft heather-grey sweater with a dark teal indoor skirt.",
      "mint_accent": "Hairpins and a mint sticky-note pad with no readable writing.",
      "composition": "upper_body",
      "tone": "quiet",
      "priority": "seed",
      "risk_note": "Desk items must not contain readable text."
    },
    {
      "slot_order": 23,
      "slug": "mint-scarf-knit",
      "japanese_title": "ミント縁のマフラー",
      "season": "winter",
      "scene": "walk_home",
      "outfit_family": "knit_soft",
      "outfit_notes": "Warm brown knit with a soft scarf and simple skirt.",
      "mint_accent": "Pale-blue crossed hairpins and mint scarf edging.",
      "composition": "half_body",
      "tone": "warm",
      "priority": "seed",
      "risk_note": "Scarf must not hide jawline or hair shape."
    },
    {
      "slot_order": 24,
      "slug": "summer-thin-knit",
      "japanese_title": "夏の薄手ニット",
      "season": "summer",
      "scene": "cafe",
      "outfit_family": "knit_soft",
      "outfit_notes": "Thin short-sleeve knit in muted coral with a navy skirt.",
      "mint_accent": "Hairpins and a mint straw charm on a cold drink.",
      "composition": "upper_body",
      "tone": "fresh",
      "priority": "seed",
      "risk_note": "No readable cafe labels, cup logos, or straw wrapper text."
    },
    {
      "slot_order": 25,
      "slug": "rain-soft-knit-layer",
      "japanese_title": "雨のニット重ね",
      "season": "rain",
      "scene": "window",
      "outfit_family": "knit_soft",
      "outfit_notes": "Soft blue-grey knit vest over a cream long-sleeve top and dark skirt.",
      "mint_accent": "Pale-blue crossed hairpins and mint curtain tie.",
      "composition": "half_body",
      "tone": "quiet",
      "priority": "hold",
      "risk_note": "Layered vest should not become a school-uniform cue."
    },
    {
      "slot_order": 26,
      "slug": "morning-soft-roomwear",
      "japanese_title": "朝のやわらか部屋着",
      "season": "all_season",
      "scene": "room",
      "outfit_family": "roomwear_relaxed",
      "outfit_notes": "Soft long-sleeve room top with relaxed ankle pants.",
      "mint_accent": "Hairpins and pale mint room socks.",
      "composition": "half_body",
      "tone": "relaxed",
      "priority": "promising",
      "risk_note": "Keep it healthy and everyday; avoid sleepwear exposure."
    },
    {
      "slot_order": 27,
      "slug": "evening-lounge-cardigan",
      "japanese_title": "夜のラウンジカーデ",
      "season": "night",
      "scene": "sofa",
      "outfit_family": "roomwear_relaxed",
      "outfit_notes": "Long soft cardigan over a modest lounge top and relaxed pants.",
      "mint_accent": "Pale-blue crossed hairpins and a mint blanket edge.",
      "composition": "knee_up",
      "tone": "quiet",
      "priority": "seed",
      "risk_note": "Sofa pose should not become pin-up or glamour."
    },
    {
      "slot_order": 28,
      "slug": "sofa-cardigan-pants",
      "japanese_title": "ソファのカーデとパンツ",
      "season": "all_season",
      "scene": "sofa",
      "outfit_family": "roomwear_relaxed",
      "outfit_notes": "Soft beige cardigan with loose charcoal pants.",
      "mint_accent": "Hairpins and mint cushion piping.",
      "composition": "knee_up",
      "tone": "relaxed",
      "priority": "seed",
      "risk_note": "Hands, knees, and cardigan edges must stay clean."
    },
    {
      "slot_order": 29,
      "slug": "kitchen-apron-relaxed",
      "japanese_title": "キッチンのゆるいエプロン",
      "season": "all_season",
      "scene": "kitchen",
      "outfit_family": "roomwear_relaxed",
      "outfit_notes": "Plain home apron over a soft top and relaxed skirt.",
      "mint_accent": "Pale-blue crossed hairpins and a mint apron tie.",
      "composition": "half_body",
      "tone": "warm",
      "priority": "seed",
      "risk_note": "Apron must read as homewear, not job uniform."
    },
    {
      "slot_order": 30,
      "slug": "winter-room-pants",
      "japanese_title": "冬の部屋パンツ",
      "season": "winter",
      "scene": "room",
      "outfit_family": "roomwear_relaxed",
      "outfit_notes": "Warm fleece-like pullover with loose dark room pants.",
      "mint_accent": "Hairpins and a mint blanket folded nearby.",
      "composition": "full_body",
      "tone": "warm",
      "priority": "hold",
      "risk_note": "Full-body indoor pose can make proportions childlike."
    },
    {
      "slot_order": 31,
      "slug": "clean-blouse-simple-pants",
      "japanese_title": "きれいめブラウスとパンツ",
      "season": "all_season",
      "scene": "cafe",
      "outfit_family": "shirt_blouse_pants",
      "outfit_notes": "Clean ivory blouse with simple navy tapered pants.",
      "mint_accent": "Pale-blue crossed hairpins and a mint bracelet.",
      "composition": "half_body",
      "tone": "lightly_dressed_up",
      "priority": "promising",
      "risk_note": "Adult but not office-uniform or overly formal."
    },
    {
      "slot_order": 32,
      "slug": "casual-work-shirt",
      "japanese_title": "カジュアルなシャツの日",
      "season": "all_season",
      "scene": "desk",
      "outfit_family": "shirt_blouse_pants",
      "outfit_notes": "Soft striped shirt with relaxed dark pants.",
      "mint_accent": "Hairpins and a mint pen clip with no readable label.",
      "composition": "upper_body",
      "tone": "everyday_cute",
      "priority": "seed",
      "risk_note": "Stripes must stay simple and not become readable graphics."
    },
    {
      "slot_order": 33,
      "slug": "summer-shirt-cropped-pants",
      "japanese_title": "夏シャツとクロップドパンツ",
      "season": "summer",
      "scene": "riverside",
      "outfit_family": "shirt_blouse_pants",
      "outfit_notes": "Short-sleeve pale blue shirt with beige cropped pants.",
      "mint_accent": "Pale-blue crossed hairpins and mint sandal detail if feet appear.",
      "composition": "full_body",
      "tone": "fresh",
      "priority": "hold",
      "risk_note": "Full-body footwear and leg proportions need stricter review."
    },
    {
      "slot_order": 34,
      "slug": "station-blouse-cardigan-pants",
      "japanese_title": "駅前のブラウスパンツ",
      "season": "autumn",
      "scene": "station",
      "outfit_family": "shirt_blouse_pants",
      "outfit_notes": "Muted lavender blouse with soft grey cardigan and navy pants.",
      "mint_accent": "Hairpins plus a mint pass-case strap.",
      "composition": "knee_up",
      "tone": "lightly_dressed_up",
      "priority": "seed",
      "risk_note": "Station signs must have no readable text."
    },
    {
      "slot_order": 35,
      "slug": "updated-hoodie-cardigan",
      "japanese_title": "少し更新したパーカー",
      "season": "all_season",
      "scene": "room",
      "outfit_family": "hoodie_baseline",
      "outfit_notes": "Soft pale hoodie under a thin colored cardigan with a dark teal skirt.",
      "mint_accent": "Pale-blue crossed hairpins and mint drawstring tips.",
      "composition": "half_body",
      "tone": "everyday_cute",
      "priority": "promising",
      "risk_note": "This is a baseline, so avoid returning to the old white-top grey-skirt default."
    },
    {
      "slot_order": 36,
      "slug": "hoodie-nondefault-bottom",
      "japanese_title": "パーカーと違うボトム",
      "season": "all_season",
      "scene": "walk_home",
      "outfit_family": "hoodie_baseline",
      "outfit_notes": "Familiar pale hoodie with relaxed dark pants and a small shoulder bag.",
      "mint_accent": "Hairpins and a mint bag strap detail.",
      "composition": "knee_up",
      "tone": "relaxed",
      "priority": "seed",
      "risk_note": "Keep hoodie count visibly minor in the set."
    }
  ]
}
```

- [ ] **Step 2: Run the contract test and confirm the manifest assertions pass up to missing requests/scripts**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_coordinate_contract
```

Expected: `FAILED` because package scripts and `generation-requests.json` do not
exist yet. The slot count, family count, priority count, and promising slot
distribution assertions should pass if run individually.

- [ ] **Step 3: Validate JSON syntax**

Run:

```bash
python -m json.tool source/manifests/tonari-no-coordinate/coordinate-slots.json >/dev/null
```

Expected: command exits `0` with no output.

- [ ] **Step 4: Commit the coordinate slot map**

```bash
git add source/manifests/tonari-no-coordinate/coordinate-slots.json
git commit -m "feat: add tonari no coordinate slots"
```

## Task 3: Add The Generation Request Builder And Package Script

**Files:**

- Create: `scripts/build_tonari_no_coordinate_generation_requests.py`
- Modify: `package.json`
- Test: `tests/test_tonari_no_coordinate_contract.py`

- [ ] **Step 1: Create the builder script**

Create `scripts/build_tonari_no_coordinate_generation_requests.py`:

```python
#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/tonari-no-coordinate"
SLOTS_PATH = MANIFEST_DIR / "coordinate-slots.json"
OUTPUT_PATH = MANIFEST_DIR / "generation-requests.json"
COLLECTION_ID = "akari-v1.1-tonari-no-coordinate"
TITLE = "となりのコーデ"
REFERENCE_PACK_VERSION = "tonari-no-akari-identity-v1"
PROMPT_TEMPLATE_VERSION = "tonari_coordinate_identity_lock_v1"
REFERENCE_PACK_INPUTS = [
    "source/references/tonari-no-akari/identity-face-hair.webp",
    "source/references/tonari-no-akari/identity-body-base.webp",
    "source/references/tonari-no-akari/identity-basic-outfit.webp",
    "source/references/tonari-no-akari/identity-side-view.webp",
]
DATE_PREFIX = "20260706"
SCENE_LABELS = {
    "room": "room",
    "window": "window",
    "sofa": "sofa",
    "desk": "desk",
    "walk_home": "walk home",
    "cafe": "cafe",
    "station": "station",
    "riverside": "riverside",
    "doorway": "doorway",
    "shopping_street": "shopping street",
    "kitchen": "kitchen",
    "veranda": "veranda",
}
SEASON_LABELS = {
    "spring": "spring",
    "summer": "summer",
    "autumn": "autumn",
    "winter": "winter",
    "rain": "rain",
    "night": "night",
    "all_season": "all season",
}
COMPOSITION_LABELS = {
    "close": "close portrait",
    "upper_body": "upper-body portrait",
    "half_body": "half-body portrait",
    "knee_up": "knee-up portrait",
    "full_body": "full-body portrait",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def hand_risk_for(slot: dict) -> str:
    if slot["composition"] == "full_body":
        return "high"
    if slot["composition"] in {"knee_up", "half_body"}:
        return "medium"
    return "low"


def outfit_drift_risk_for(slot: dict) -> str:
    if slot["outfit_family"] in {"one_piece_skirt", "hoodie_baseline"}:
        return "high"
    return "medium"


def age_impression_risk_for(slot: dict) -> str:
    if slot["outfit_family"] in {"hoodie_baseline", "roomwear_relaxed"}:
        return "high"
    return "medium"


def build_prompt(slot: dict) -> str:
    season = SEASON_LABELS[slot["season"]]
    scene = SCENE_LABELS[slot["scene"]]
    composition = COMPOSITION_LABELS[slot["composition"]]
    return (
        f"Create one A4 portrait draft for Tonari no Coordinate: "
        f"{slot['japanese_title']}. Season and scene: {season}, {scene}. "
        f"Composition: {composition}, close everyday Akari mood, outfit clearly visible. "
        f"Coordinate: {slot['outfit_notes']} "
        f"Identity accent: {slot['mint_accent']} "
        "Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, "
        "not glamorous, not model-like, not pin-up, not childlike; "
        "short fluffy light-brown bob with airy uneven ends and soft side bangs; "
        "warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; "
        "pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; "
        "petite/slender healthy adult proportions. "
        "Styling boundary: daily wear or lightly dressed-up day-off wear; "
        "no student-uniform styling, no character-costume styling, no job-uniform styling, "
        "no revealing swim styling, no underwear-like styling, no readable text prints. "
        "No image-internal readable text, no logos, no watermarks, no frame, no border, "
        "no panel layout."
    )


def build_acceptance(slot: dict) -> str:
    return (
        "Coordinate Gate: must preserve Akari identity, 25-year-old adult age impression, "
        "face/hair/hairpin consistency, natural body proportions, visible mint or pale-blue "
        "identity accent, daily or lightly special outfit readability, and clean clothing "
        "continuity. It must be not a fashion-model sheet, not a costume sheet, and not a "
        "return to hoodie-heavy sameness. Must contain no image-internal readable text, "
        "no logos, no watermarks, no frame, no border, no panel layout. "
        f"Known slot risk: {slot['risk_note']}"
    )


def build_request(slot: dict) -> dict:
    return {
        "id": f"request:tonari-coordinate-{slot['slug']}",
        "coordinate_order": slot["slot_order"],
        "slot": slot["slug"],
        "japanese_title": slot["japanese_title"],
        "season": slot["season"],
        "scene": slot["scene"],
        "outfit_family": slot["outfit_family"],
        "outfit_notes": slot["outfit_notes"],
        "mint_accent": slot["mint_accent"],
        "composition": slot["composition"],
        "tone": slot["tone"],
        "risk_note": slot["risk_note"],
        "target_path": f"source/generated/tonari-no-coordinate/{DATE_PREFIX}_{slot['slug']}_v1.webp",
        "reference_pack_inputs": REFERENCE_PACK_INPUTS,
        "prompt": build_prompt(slot),
        "acceptance": build_acceptance(slot),
        "risk_profile": {
            "identity_risk": "high",
            "outfit_drift_risk": outfit_drift_risk_for(slot),
            "age_impression_risk": age_impression_risk_for(slot),
            "hand_risk": hand_risk_for(slot),
            "text_logo_watermark_risk": "medium",
        },
        "review_plan": {
            "initial_status": "draft_candidate",
            "first_pass": "Place in the 12-image coordinate contact sheet before finishing.",
            "coordinate_gate": "Run the Coordinate Gate for outfit variety, Akari identity, age impression, mint accent, and no text/logo/frame issues.",
            "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
            "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, anatomy, or artifact defects.",
            "humanization": "Use Humanization Pass only after the image is structurally valid.",
        },
    }


def build_manifest(slot_manifest: dict) -> dict:
    promising_slots = [
        slot for slot in slot_manifest["slots"] if slot["priority"] == "promising"
    ]
    return {
        "schema_version": 1,
        "collection_id": COLLECTION_ID,
        "title": TITLE,
        "reference_pack_version": REFERENCE_PACK_VERSION,
        "prompt_template_version": PROMPT_TEMPLATE_VERSION,
        "batch_policy": {
            "request_source": "promising_slots_only",
            "candidate_count": len(promising_slots),
            "review_order": "contact_sheet_before_finishing",
            "pdf_policy": "not_in_first_phase",
        },
        "requests": [build_request(slot) for slot in promising_slots],
    }


def main() -> None:
    slot_manifest = load_json(SLOTS_PATH)
    dump_json(OUTPUT_PATH, build_manifest(slot_manifest))
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Add package scripts**

Modify the `scripts` object in `package.json` to include:

```json
"build:coordinate:requests": "uv run python scripts/build_tonari_no_coordinate_generation_requests.py",
"build:coordinate:contact-sheet": "uv run python scripts/build_tonari_no_coordinate_contact_sheet.py"
```

Place them near the existing `build:tonari:*` scripts so collection helpers stay
grouped.

- [ ] **Step 3: Run the builder**

Run:

```bash
npm run build:coordinate:requests
```

Expected:

```text
Wrote source/manifests/tonari-no-coordinate/generation-requests.json
```

- [ ] **Step 4: Validate generated JSON syntax**

Run:

```bash
python -m json.tool source/manifests/tonari-no-coordinate/generation-requests.json >/dev/null
```

Expected: command exits `0` with no output.

- [ ] **Step 5: Run the contract test**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_coordinate_contract
```

Expected: `OK`.

- [ ] **Step 6: Commit the builder and generated request manifest**

```bash
git add package.json scripts/build_tonari_no_coordinate_generation_requests.py source/manifests/tonari-no-coordinate/generation-requests.json
git commit -m "feat: add tonari no coordinate generation requests"
```

## Task 4: Add Contact Sheet Tests

**Files:**

- Create: `tests/test_tonari_no_coordinate_contact_sheet.py`
- Target implementation: `scripts/build_tonari_no_coordinate_contact_sheet.py`

- [ ] **Step 1: Write the failing contact-sheet test**

Create `tests/test_tonari_no_coordinate_contact_sheet.py`:

```python
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.build_tonari_no_coordinate_contact_sheet import build_contact_sheet


class TonariNoCoordinateContactSheetTest(unittest.TestCase):
    def test_build_contact_sheet_uses_existing_images_and_writes_sheet(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            generated_dir = temp_path / "generated"
            output_path = temp_path / "sheet.webp"
            generated_dir.mkdir()

            first_image = generated_dir / "20260706_first_v1.webp"
            second_image = generated_dir / "20260706_second_v1.webp"
            Image.new("RGB", (320, 480), "#d9eee9").save(first_image)
            Image.new("RGB", (320, 480), "#f0dfd1").save(second_image)

            requests = [
                {
                    "slot": "first",
                    "japanese_title": "一枚目",
                    "outfit_family": "layering",
                    "target_path": first_image.as_posix(),
                },
                {
                    "slot": "second",
                    "japanese_title": "二枚目",
                    "outfit_family": "knit_soft",
                    "target_path": second_image.as_posix(),
                },
                {
                    "slot": "missing",
                    "japanese_title": "未生成",
                    "outfit_family": "roomwear_relaxed",
                    "target_path": (generated_dir / "missing.webp").as_posix(),
                },
            ]

            result = build_contact_sheet(
                requests=requests,
                project_root=temp_path,
                output_path=output_path,
                columns=2,
                thumb_width=160,
                label_height=48,
                gap=12,
            )

            self.assertEqual(output_path, result)
            self.assertTrue(output_path.is_file())
            with Image.open(output_path) as sheet:
                self.assertEqual((356, 312), sheet.size)

    def test_build_contact_sheet_fails_when_no_images_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            with self.assertRaisesRegex(ValueError, "No generated coordinate images found"):
                build_contact_sheet(
                    requests=[
                        {
                            "slot": "missing",
                            "japanese_title": "未生成",
                            "outfit_family": "roomwear_relaxed",
                            "target_path": "source/generated/tonari-no-coordinate/missing.webp",
                        }
                    ],
                    project_root=temp_path,
                    output_path=temp_path / "sheet.webp",
                    columns=2,
                    thumb_width=160,
                    label_height=48,
                    gap=12,
                )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the contact-sheet test and confirm it fails on missing module**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_coordinate_contact_sheet
```

Expected: `FAILED` or `ERROR` because
`scripts/build_tonari_no_coordinate_contact_sheet.py` does not exist yet.

- [ ] **Step 3: Commit the failing contact-sheet test**

```bash
git add tests/test_tonari_no_coordinate_contact_sheet.py
git commit -m "test: add tonari no coordinate contact sheet coverage"
```

## Task 5: Add The Contact Sheet Builder

**Files:**

- Create: `scripts/build_tonari_no_coordinate_contact_sheet.py`
- Test: `tests/test_tonari_no_coordinate_contact_sheet.py`

- [ ] **Step 1: Create the contact-sheet script**

Create `scripts/build_tonari_no_coordinate_contact_sheet.py`:

```python
#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REQUESTS_PATH = ROOT / "source/manifests/tonari-no-coordinate/generation-requests.json"
DEFAULT_OUTPUT = ROOT / "evidence/tonari-no-coordinate/contact-sheets/tonari-no-coordinate-first-batch.webp"
BACKGROUND = "#f7f3ee"
CARD_BACKGROUND = "#ffffff"
TEXT = "#2b2b2b"
SUBTEXT = "#666666"


def load_requests(path: Path) -> list[dict]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    return manifest["requests"]


def resolve_candidate_path(project_root: Path, target_path: str) -> Path:
    path = Path(target_path)
    if path.is_absolute():
        return path
    return project_root / path


def load_font(size: int) -> ImageFont.ImageFont:
    for font_path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ):
        candidate = Path(font_path)
        if candidate.is_file():
            return ImageFont.truetype(candidate.as_posix(), size=size)
    return ImageFont.load_default()


def fit_image(image: Image.Image, thumb_width: int) -> Image.Image:
    image = image.convert("RGB")
    ratio = thumb_width / image.width
    thumb_height = int(round(image.height * ratio))
    return image.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)


def draw_label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], request: dict, font: ImageFont.ImageFont, small_font: ImageFont.ImageFont) -> None:
    x, y = xy
    title = f"{request['japanese_title']} / {request['slot']}"
    family = request["outfit_family"].replace("_", " ")
    draw.text((x, y), title, fill=TEXT, font=font)
    draw.text((x, y + 22), family, fill=SUBTEXT, font=small_font)


def existing_request_images(requests: list[dict], project_root: Path) -> list[tuple[dict, Path]]:
    found = []
    for request in requests:
        image_path = resolve_candidate_path(project_root, request["target_path"])
        if image_path.is_file():
            found.append((request, image_path))
    return found


def build_contact_sheet(
    requests: list[dict],
    project_root: Path,
    output_path: Path,
    columns: int = 4,
    thumb_width: int = 280,
    label_height: int = 56,
    gap: int = 20,
) -> Path:
    found = existing_request_images(requests, project_root)
    if not found:
        raise ValueError("No generated coordinate images found")

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
    small_font = load_font(13)

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
        draw_label(draw, (x + 8, y + thumb_height + 6), request, font, small_font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=92)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a contact sheet for Tonari no Coordinate candidates.")
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
    print(f"Wrote {result.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the contact-sheet unit test**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_coordinate_contact_sheet
```

Expected: `OK`.

- [ ] **Step 3: Run the contact-sheet script before images exist and confirm the error is clear**

Run:

```bash
npm run build:coordinate:contact-sheet
```

Expected: command exits non-zero with:

```text
ValueError: No generated coordinate images found
```

This is acceptable before candidate images are generated.

- [ ] **Step 4: Commit the contact-sheet builder**

```bash
git add scripts/build_tonari_no_coordinate_contact_sheet.py
git commit -m "feat: add tonari no coordinate contact sheet builder"
```

## Task 6: Final Verification And Documentation Check

**Files:**

- Read: `docs/superpowers/specs/2026-07-06-akari-v1-1-tonari-no-coordinate-design.md`
- Read: `docs/superpowers/plans/2026-07-06-akari-v1-1-tonari-no-coordinate.md`

- [ ] **Step 1: Rebuild generation requests**

Run:

```bash
npm run build:coordinate:requests
```

Expected:

```text
Wrote source/manifests/tonari-no-coordinate/generation-requests.json
```

- [ ] **Step 2: Validate JSON manifests**

Run:

```bash
python -m json.tool source/manifests/tonari-no-coordinate/coordinate-slots.json >/dev/null
python -m json.tool source/manifests/tonari-no-coordinate/generation-requests.json >/dev/null
```

Expected: both commands exit `0` with no output.

- [ ] **Step 3: Run focused Python tests**

Run:

```bash
uv run python -m unittest tests.test_tonari_no_coordinate_contract tests.test_tonari_no_coordinate_contact_sheet
```

Expected: `OK`.

- [ ] **Step 4: Run the full Python test suite**

Run:

```bash
npm run test:python
```

Expected: `OK`.

- [ ] **Step 5: Run Markdown lint**

Run:

```bash
npm run lint:md
```

Expected: `Summary: 0 error(s)`.

- [ ] **Step 6: Confirm no generated image files were accidentally staged**

Run:

```bash
git status --short
```

Expected: only intended source, test, script, package, and manifest files are
present. No files under `source/generated/tonari-no-coordinate/` or
`evidence/tonari-no-coordinate/contact-sheets/` should be staged unless the user
explicitly requested final deliverables.

- [ ] **Step 7: Commit final verification adjustments if needed**

If verification required small fixes, commit only those fixes:

```bash
git add package.json scripts/build_tonari_no_coordinate_generation_requests.py scripts/build_tonari_no_coordinate_contact_sheet.py tests/test_tonari_no_coordinate_contract.py tests/test_tonari_no_coordinate_contact_sheet.py source/manifests/tonari-no-coordinate/coordinate-slots.json source/manifests/tonari-no-coordinate/generation-requests.json
git commit -m "chore: verify tonari no coordinate workflow"
```

If there are no final fixes after Task 5, skip this commit.

## Implementation Notes

- Use `bash -lc 'npm ...'` if `npm` or `node` is not visible in the Codex shell.
- Keep `coordinate-slots.json` hand-reviewed. Do not edit
  `generation-requests.json` by hand after the builder exists; regenerate it.
- The first real image-generation batch should use only the 12 requests in
  `generation-requests.json`.
- The contact sheet is intentionally tolerant of missing images so partial
  generation batches can still be reviewed.
- If a candidate passes the set-level contact-sheet review, run
  `akari-v1-1-image-review` on that single image before treating it as a likely
  accept.
