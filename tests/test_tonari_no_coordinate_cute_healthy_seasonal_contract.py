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
    if not path.is_file():
        raise AssertionError(f"missing manifest: {path}")
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
        self.assertEqual(
            list(range(1, 9)),
            [request["coordinate_order"] for request in requests],
        )
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
                self.assertIn(
                    risk_profile["background_distraction_risk"],
                    {"low", "medium"},
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
