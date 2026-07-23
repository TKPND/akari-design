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
    / "docs/plans/2026-07-08-akari-v1-2-hair-symbol-bangs.md"
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
SELECTED_SLOT = "balanced-symbol-bangs"
SELECTED_PATH = (
    "source/generated/v1-2-face-hair/hair-symbol-bangs-y1/"
    "20260708_balanced-symbol-bangs_v2.png"
)
SELECTED_RATIONALE_PHRASE = "best combined Y1 refinement"
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
                self.assertEqual(
                    "locked Y1 face; no eye redesign",
                    request["eye_variation"],
                )
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

    def test_selection_notes_record_user_choice_after_review(self):
        selection_notes = load_json(MANIFEST)["selection_notes"]

        self.assertEqual(1, len(selection_notes))
        selection = selection_notes[0]
        self.assertEqual(
            "hold_as_hair_symbol_bangs_y1_direction",
            selection["decision"],
        )
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
