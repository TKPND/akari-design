import json
import re
import subprocess
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

    def test_phase_generated_outputs_are_ignored_by_git(self):
        ignored_paths = [
            "source/generated/tonari-no-coordinate/example.webp",
            "evidence/tonari-no-coordinate/contact-sheets/example.webp",
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
        self.assertEqual(
            EXPECTED_FAMILY_COUNTS,
            dict(Counter(slot["outfit_family"] for slot in slots)),
        )
        self.assertEqual(
            EXPECTED_PRIORITY_COUNTS,
            dict(Counter(slot["priority"] for slot in slots)),
        )
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
