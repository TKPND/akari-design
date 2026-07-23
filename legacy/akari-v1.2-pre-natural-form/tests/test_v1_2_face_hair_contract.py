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
REFERENCE_PROMPT_PREFIX = (
    "Use the visible reference images as identity references. Reference image 1 "
    "is the primary Akari v1.1 face identity; reference images 2 and 3 are "
    "auxiliary face consistency checks. Preserve the same character identity, "
    "face proportions, warm brown eye color, short brown bob mass, small mouth "
    "scale, and pale blue character-left hair ornament before making any v1.2 "
    "refinement."
)
REFERENCE_PILOT_TARGET = (
    "source/generated/v1-2-face-hair/reference-pilot/"
    "20260708_soft-horizontal-eyes_ref-v1.png"
)
STRONG_REFERENCE_PILOT_TARGET = (
    "source/generated/v1-2-face-hair/reference-pilot/"
    "20260708_soft-horizontal-eyes_ref-v2.png"
)
REFERENCE_PACK_INPUTS = [
    "source/originals/v1_1_front_3.webp",
    "source/originals/v1_1_front_1.webp",
    "source/originals/v1_1_front_2.webp",
    "source/references/tonari-no-akari/identity-face-hair.webp",
]
STRONG_REFERENCE_INPUTS = [
    "source/originals/v1_1_front_3.webp",
    "source/originals/v1_1_髪飾り側_45deg.webp",
    "source/originals/v1_1_front_1.webp",
]
HYOUJOU_REFERENCE_INPUTS = [
    "source/generated/tonari-no-hyoujou/20260703_called-turn_v2.webp",
    "source/generated/tonari-no-hyoujou/20260703_eye-contact-pause_v1.webp",
    "source/generated/tonari-no-hyoujou/20260706_extra-02_prank-smug_v5.webp",
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

    def test_manifest_records_selected_young_base05_direction(self):
        selection = load_json(MANIFEST)["selection_notes"]

        self.assertEqual("hold_as_v1_2_standard_face_axis", selection["decision"])
        self.assertEqual(
            (
                "source/generated/v1-2-face-hair/free-reference-batch/"
                "20260708_free-ref-05.png"
            ),
            selection["selected_source_axis_path"],
        )
        self.assertEqual(
            (
                "source/generated/v1-2-face-hair/"
                "free-reference-batch-younger-base05/"
                "20260708_base05-younger-01.png"
            ),
            selection["selected_candidate_path"],
        )
        self.assertEqual(
            (
                "evidence/v1-2-face-hair/contact-sheets/"
                "akari-v1-2-face-hair-base05-younger-variants.webp"
            ),
            selection["selected_contact_sheet_path"],
        )
        self.assertIn("early-20s university-age young adult", selection["age_impression"])
        self.assertIn("less older-sister-like", selection["age_impression"])
        self.assertIn("still not underage", selection["age_impression"])
        self.assertIn("younger-01 adjustment", selection["rationale"])

    def test_reference_pack_inputs_exist(self):
        for reference_path in REFERENCE_PACK_INPUTS:
            with self.subTest(reference_path=reference_path):
                self.assertTrue((ROOT / reference_path).is_file())
        for reference_path in STRONG_REFERENCE_INPUTS + HYOUJOU_REFERENCE_INPUTS:
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
                self.assertEqual(
                    f"request:v1-2-face-hair-{expected['slot']}",
                    request["id"],
                )
                self.assertEqual(expected["title"], request["japanese_title"])
                self.assertTrue(JAPANESE_TEXT.search(request["japanese_title"]))
                self.assertEqual(expected["eye_variation"], request["eye_variation"])
                self.assertEqual(expected["hair_variation"], request["hair_variation"])
                self.assertEqual(REFERENCE_PACK_INPUTS, request["reference_pack_inputs"])
                self.assertEqual(
                    (
                        "source/generated/v1-2-face-hair/"
                        f"{DATE_PREFIX}_{expected['slot']}_v1.png"
                    ),
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
                self.assertIn("do not make her underage", prompt)
                self.assertIn("no readable text", prompt)
                self.assertIn("no logos", prompt)
                self.assertIn("no watermarks", prompt)

                for banned in BANNED_PROMPT_FRAGMENTS:
                    self.assertNotIn(banned, prompt_lower)

    def test_first_request_records_reference_locked_pilot(self):
        request = load_json(MANIFEST)["requests"][0]

        self.assertEqual("soft-horizontal-eyes", request["slot"])
        self.assertEqual(
            REFERENCE_PILOT_TARGET,
            request["reference_pilot_target_path"],
        )
        self.assertTrue(request["prompt"].startswith(REFERENCE_PROMPT_PREFIX))
        self.assertIn(
            "Image 1: primary Akari v1.1 face identity reference.",
            request["prompt"],
        )
        self.assertIn(
            "Image 2: auxiliary v1.1 face and softness reference.",
            request["prompt"],
        )
        self.assertIn(
            "Image 3: auxiliary v1.1 face and hair-balance reference.",
            request["prompt"],
        )

    def test_first_request_records_stronger_reference_retry(self):
        request = load_json(MANIFEST)["requests"][0]

        self.assertEqual(STRONG_REFERENCE_INPUTS, request["strong_reference_inputs"])
        self.assertEqual(
            STRONG_REFERENCE_PILOT_TARGET,
            request["strong_reference_pilot_target_path"],
        )
        strong_prompt = request["strong_reference_prompt"]
        self.assertIn("source/originals/v1_1_髪飾り側_45deg.webp", strong_prompt)
        self.assertIn("pale-blue crossed hairpins", strong_prompt)
        self.assertIn("not a flower accessory", strong_prompt)
        self.assertIn("lighter copper-brown v1.1 hair", strong_prompt)
        self.assertIn("rounder v1.1 cheeks", strong_prompt)
        self.assertIn("small restrained mouth", strong_prompt)

    def test_first_request_records_hyoujou_reference_pilot(self):
        request = load_json(MANIFEST)["requests"][0]

        self.assertEqual(HYOUJOU_REFERENCE_INPUTS, request["hyoujou_reference_inputs"])
        self.assertEqual(
            "source/generated/v1-2-face-hair/reference-pilot/"
            "20260708_soft-horizontal-eyes_hyoujou-v1.png",
            request["hyoujou_reference_pilot_target_path"],
        )
        hyoujou_prompt = request["hyoujou_reference_prompt"]
        self.assertIn("20260703_called-turn_v2.webp", hyoujou_prompt)
        self.assertIn("main standard-face reference", hyoujou_prompt)
        self.assertIn("20260703_eye-contact-pause_v1.webp", hyoujou_prompt)
        self.assertIn("innocence reference", hyoujou_prompt)
        self.assertIn("20260706_extra-02_prank-smug_v5.webp", hyoujou_prompt)
        self.assertIn("appeal reference", hyoujou_prompt)
        self.assertIn("do not invent a new face family", hyoujou_prompt)

    def test_acceptance_and_review_gates_are_explicit(self):
        for request in load_json(MANIFEST)["requests"]:
            with self.subTest(slot=request["slot"]):
                acceptance = request["acceptance"]
                for phrase in REQUIRED_ACCEPTANCE_PHRASES:
                    self.assertIn(phrase, acceptance)

                self.assertEqual(
                    {
                        "appeal": (
                            "soft close memorable eyes, warm expression, "
                            "immediate character charm"
                        ),
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
