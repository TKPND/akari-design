import hashlib
import json
import subprocess
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SELECTION = ROOT / "source/manifests/v1-2-face-hair/accepted-selection.json"
HAIR_SELECTION = ROOT / (
    "source/manifests/v1-2-face-hair/hair-symbol-bangs-y1-requests.json"
)
ACCEPTED_ASSET_PATH = (
    "source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp"
)
ACCEPTED_ASSET = ROOT / ACCEPTED_ASSET_PATH
SOURCE_CANDIDATE_PATH = (
    "source/generated/v1-2-face-hair/hair-symbol-bangs-y1/"
    "20260708_balanced-symbol-bangs_v2.png"
)
SOURCE_CANDIDATE_SHA256 = (
    "ad2044cfa407df4ba884c9fa503e0cad7be2a38de77e3865480ccbf2674b2805"
)


def load_json(path):
    if not path.is_file():
        raise AssertionError(f"missing JSON contract: {path}")
    with path.open(encoding="utf-8") as json_file:
        return json.load(json_file)


def sha256(path):
    if not path.is_file():
        raise AssertionError(f"missing asset for hashing: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as asset_file:
        for chunk in iter(lambda: asset_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class AkariV12FaceHairAcceptanceTest(unittest.TestCase):
    def test_acceptance_manifest_and_asset_exist(self):
        self.assertTrue(SELECTION.is_file(), f"missing manifest: {SELECTION}")
        self.assertTrue(
            ACCEPTED_ASSET.is_file(),
            f"missing accepted asset: {ACCEPTED_ASSET}",
        )

    def test_manifest_records_the_user_accepted_blind_selection(self):
        manifest = load_json(SELECTION)

        self.assertEqual(1, manifest["schema_version"])
        self.assertEqual(
            "akari-v1.2-standard-face-v1",
            manifest["identity_version"],
        )
        self.assertEqual("accepted", manifest["decision"])
        self.assertEqual("2026-07-10", manifest["accepted_on"])
        self.assertEqual("balanced-symbol-bangs", manifest["accepted_slot"])
        self.assertEqual(SOURCE_CANDIDATE_PATH, manifest["source_candidate"])
        self.assertEqual(ACCEPTED_ASSET_PATH, manifest["accepted_asset"])
        self.assertEqual(
            SOURCE_CANDIDATE_SHA256,
            manifest["source_candidate_sha256"],
        )
        self.assertEqual("A", manifest["user_review"]["blind_label"])
        self.assertEqual(
            "Aにしよう",
            manifest["user_review"]["decision_text"],
        )
        self.assertEqual(
            "balanced-symbol-bangs",
            manifest["user_review"]["revealed_slot"],
        )
        self.assertTrue(manifest["accepted_reason"].strip())

    def test_manifest_records_durable_identity_and_layout_rules(self):
        rules = load_json(SELECTION)["identity_rules"]
        ornament = rules["hair_ornament"]

        self.assertIn("young adult", rules["age_impression"])
        self.assertIn("not underage", rules["age_impression"])
        self.assertIn("Y1 face direction", rules["face"])
        self.assertIn("warm amber eyes", rules["face"])
        self.assertIn("small restrained mouth", rules["face"])
        self.assertIn("warm brown short bob", rules["hair"])
        self.assertIn("v1.1-like bang grouping", rules["hair"])
        self.assertEqual("character-left", ornament["side"])
        self.assertEqual(
            "small pale-blue crossed X-shaped hairpins",
            ornament["upper"],
        )
        self.assertEqual(
            "compact pale-blue ribbon-like loop immediately below",
            ornament["lower"],
        )
        self.assertEqual(2, ornament["trailing_strand_count"])
        self.assertIn("flower", ornament["hard_rejects"])
        self.assertIn("jewel", ornament["hard_rejects"])
        self.assertIn("missing upper or lower component", ornament["hard_rejects"])
        self.assertEqual(
            [
                "same crop as the accepted source",
                "same pose as the accepted source",
                "same background layout as the accepted source",
                "1024x1536 portrait aspect ratio",
            ],
            rules["layout"],
        )

    def test_accepted_asset_metadata_and_hash_match_file(self):
        manifest = load_json(SELECTION)

        self.assertEqual(sha256(ACCEPTED_ASSET), manifest["accepted_asset_sha256"])
        with Image.open(ACCEPTED_ASSET) as image:
            self.assertEqual("WEBP", image.format)
            self.assertEqual((1024, 1536), image.size)
            self.assertEqual("RGB", image.mode)
        self.assertEqual(
            {
                "tool": "cwebp",
                "version": "1.6.0",
                "quality": 95,
                "method": 6,
                "sharp_yuv": True,
                "metadata": "none",
            },
            manifest["conversion"],
        )

    def test_selected_source_agrees_with_the_hair_direction_record(self):
        selection_notes = load_json(HAIR_SELECTION)["selection_notes"]

        self.assertEqual(1, len(selection_notes))
        self.assertEqual(
            "hold_as_hair_symbol_bangs_y1_direction",
            selection_notes[0]["decision"],
        )
        self.assertEqual("balanced-symbol-bangs", selection_notes[0]["selected_slot"])
        self.assertEqual(
            SOURCE_CANDIDATE_PATH,
            selection_notes[0]["selected_candidate_path"],
        )

    def test_accepted_asset_path_can_be_tracked(self):
        result = subprocess.run(
            ["git", "check-ignore", "-q", ACCEPTED_ASSET_PATH],
            cwd=ROOT,
            check=False,
        )

        self.assertEqual(1, result.returncode)


if __name__ == "__main__":
    unittest.main()
