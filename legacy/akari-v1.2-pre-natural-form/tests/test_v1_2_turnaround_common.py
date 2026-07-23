import tempfile
import unittest
from pathlib import Path

from scripts.v1_2_turnaround_common import (
    dump_json,
    load_json,
    normalize_landmarks,
    sha256_file,
)


LANDMARK_Y_PX = {
    "crown": 96,
    "chin": 270,
    "shoulder": 350,
    "hoodie_hem": 720,
    "skirt_hem": 850,
    "knee": 1080,
    "ankle": 1370,
    "sole": 1464,
}


class AkariV12TurnaroundCommonTest(unittest.TestCase):
    def test_json_round_trip_and_sha256_are_deterministic(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "nested/record.json"
            dump_json(path, {"name": "あかり", "value": 1})
            self.assertEqual({"name": "あかり", "value": 1}, load_json(path))
            self.assertEqual(64, len(sha256_file(path)))

    def test_landmarks_normalize_against_crown_to_sole_height(self):
        normalized = normalize_landmarks(LANDMARK_Y_PX)
        self.assertEqual(0.0, normalized["crown"])
        self.assertEqual(1.0, normalized["sole"])
        self.assertAlmostEqual(
            (LANDMARK_Y_PX["knee"] - LANDMARK_Y_PX["crown"])
            / (LANDMARK_Y_PX["sole"] - LANDMARK_Y_PX["crown"]),
            normalized["knee"],
            places=6,
        )

    def test_landmarks_reject_invalid_order_and_canvas_values(self):
        invalid_order = dict(LANDMARK_Y_PX, chin=80)
        with self.assertRaisesRegex(ValueError, "strictly increasing"):
            normalize_landmarks(invalid_order)
        invalid_canvas = dict(LANDMARK_Y_PX, sole=1536)
        with self.assertRaisesRegex(ValueError, "inside the image"):
            normalize_landmarks(invalid_canvas)
