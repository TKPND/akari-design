import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.build_v1_2_turnaround_contact_sheet import (
    build_final_contact_sheet,
    build_stage_contact_sheet,
    select_active_requests,
    validate_landmark_ratios,
)
from scripts.v1_2_turnaround_common import normalize_landmarks


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


def accepted_record(slot: str, path: str, drift_px: int = 0) -> dict:
    landmark_y_px = dict(LANDMARK_Y_PX)
    for name in (
        "chin",
        "shoulder",
        "hoodie_hem",
        "skirt_hem",
        "knee",
        "ankle",
    ):
        landmark_y_px[name] += drift_px
    return {
        "slot": slot,
        "angle_order": 1,
        "japanese_title": slot,
        "accepted_path": path,
        "candidate_number": 1,
        "revision": 1,
        "batch_id": f"{slot}-r1",
        "landmark_y_px": landmark_y_px,
        "normalized_landmarks": normalize_landmarks(landmark_y_px),
    }


class AkariV12TurnaroundContactSheetTest(unittest.TestCase):
    def test_active_request_selection_excludes_historical_revisions(self):
        manifest = {
            "active_batches": {"front": "front-r2"},
            "requests": [
                {"slot": "front", "batch_id": "front-r1", "id": "old"},
                {"slot": "front", "batch_id": "front-r2", "id": "new"},
            ],
        }
        selected = select_active_requests(manifest, ["front"], None)
        self.assertEqual(["new"], [request["id"] for request in selected])

    def test_stage_sheet_uses_every_requested_candidate_image(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            image_one = root / "one.png"
            image_two = root / "two.png"
            output = root / "stage.webp"
            Image.new("RGB", (1024, 1536), "#d9eee9").save(image_one)
            Image.new("RGB", (1024, 1536), "#f0dfd1").save(image_two)
            requests = [
                {
                    "slot": "front",
                    "batch_id": "front-r1",
                    "revision": 1,
                    "candidate_number": 1,
                    "japanese_title": "正面",
                    "target_path": image_one.as_posix(),
                },
                {
                    "slot": "front",
                    "batch_id": "front-r1",
                    "revision": 1,
                    "candidate_number": 2,
                    "japanese_title": "正面",
                    "target_path": image_two.as_posix(),
                },
            ]
            result = build_stage_contact_sheet(requests, root, output, columns=2)
            self.assertEqual(output, result)
            with Image.open(output) as sheet:
                self.assertEqual("RGB", sheet.mode)
                self.assertEqual((774, 638), sheet.size)

    def test_stage_sheet_rejects_a_missing_requested_candidate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            existing = root / "one.png"
            Image.new("RGB", (1024, 1536), "white").save(existing)
            requests = [
                {
                    "slot": "front",
                    "batch_id": "front-r1",
                    "revision": 1,
                    "candidate_number": candidate_number,
                    "japanese_title": "正面",
                    "target_path": path.as_posix(),
                }
                for candidate_number, path in (
                    (1, existing),
                    (2, root / "missing.png"),
                )
            ]
            with self.assertRaisesRegex(ValueError, "missing requested candidate"):
                build_stage_contact_sheet(requests, root, root / "stage.webp")

    def test_landmark_validator_accepts_small_counterpart_drift(self):
        records = [
            accepted_record("character-left-profile", "left.webp"),
            accepted_record("character-right-profile", "right.webp", 7),
        ]
        self.assertEqual([], validate_landmark_ratios(records))

    def test_landmark_validator_reports_pair_and_set_drift(self):
        records = [
            accepted_record("character-left-profile", "left.webp"),
            accepted_record("character-right-profile", "right.webp", 55),
        ]
        errors = validate_landmark_ratios(records)
        self.assertTrue(any("counterpart" in error for error in errors))
        self.assertTrue(any("full-set" in error for error in errors))

    def test_final_sheet_rejects_landmark_drift(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            left = root / "left.webp"
            right = root / "right.webp"
            Image.new("RGB", (1024, 1536), "white").save(left)
            Image.new("RGB", (1024, 1536), "white").save(right)
            records = [
                accepted_record("character-left-profile", left.as_posix()),
                accepted_record(
                    "character-right-profile",
                    right.as_posix(),
                    55,
                ),
            ]
            with self.assertRaisesRegex(ValueError, "landmark validation failed"):
                build_final_contact_sheet(records, root, root / "final.webp")

    def test_final_sheet_renders_all_accepted_records(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            records = []
            for angle_order, slot in enumerate(("front", "back"), start=1):
                path = root / f"{slot}.webp"
                Image.new("RGB", (1024, 1536), "white").save(path)
                record = accepted_record(slot, path.as_posix())
                record["angle_order"] = angle_order
                records.append(record)
            output = root / "final.webp"
            self.assertEqual(
                output,
                build_final_contact_sheet(records, root, output),
            )
            self.assertTrue(output.is_file())
