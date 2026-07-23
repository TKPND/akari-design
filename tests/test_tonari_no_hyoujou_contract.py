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
    "young child",
    "child body",
    "childlike body",
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
