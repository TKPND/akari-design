import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.build_v1_2_overhead_room_contact_sheet import (
    build_batch_contact_sheet,
    build_final_contact_sheet,
    select_active_requests,
)
from scripts.v1_2_overhead_room_common import POSE_SLOTS


def make_image(path: Path, *, mode: str = "RGB", size=(1024, 1536)) -> str:
    Image.new(mode, size, "white").save(path)
    return path.as_posix()


class AkariV12OverheadRoomContactSheetTest(unittest.TestCase):
    def test_selects_two_requests_from_only_the_active_batch(self):
        manifest = {
            "active_batches": {"supine-direct-gaze": "r2"},
            "requests": [
                {
                    "pose": "supine-direct-gaze",
                    "batch_id": batch,
                    "revision": int(batch[-1]),
                    "candidate_number": number,
                    "target_path": f"{batch}-{number}.png",
                }
                for batch in ("r1", "r2")
                for number in (1, 2)
            ],
        }
        selected = select_active_requests(manifest, "supine-direct-gaze")
        self.assertEqual([1, 2], [item["candidate_number"] for item in selected])
        self.assertEqual({"r2"}, {item["batch_id"] for item in selected})

    def test_batch_sheet_requires_two_rgb_candidates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests = [
                {
                    "id": f"r-{number}",
                    "pose": "supine-direct-gaze",
                    "batch_id": "r1",
                    "revision": 1,
                    "candidate_number": number,
                    "target_path": make_image(root / f"c{number}.png"),
                }
                for number in (1, 2)
            ]
            output = root / "batch.webp"
            self.assertEqual(
                output,
                build_batch_contact_sheet(requests, {}, root, output),
            )
            with Image.open(output) as sheet:
                self.assertEqual((774, 638), sheet.size)

    def test_batch_sheet_rejects_invalid_source_before_replacing_output(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = root / "batch.webp"
            output.write_bytes(b"keep-me")
            requests = [
                {
                    "id": f"r-{number}",
                    "pose": "supine-direct-gaze",
                    "batch_id": "r1",
                    "revision": 1,
                    "candidate_number": number,
                    "target_path": make_image(
                        root / f"c{number}.png",
                        mode="RGBA" if number == 2 else "RGB",
                    ),
                }
                for number in (1, 2)
            ]
            with self.assertRaisesRegex(ValueError, "RGB 1024x1536"):
                build_batch_contact_sheet(requests, {}, root, output)
            self.assertEqual(b"keep-me", output.read_bytes())

    def test_final_sheet_requires_ten_canonical_accepted_works(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            records = [
                {
                    "pose": pose,
                    "pose_order": order,
                    "finished_path": make_image(root / f"pose-{order}.webp"),
                }
                for order, pose in enumerate(POSE_SLOTS, start=1)
            ]
            output = root / "final.webp"
            self.assertEqual(
                output,
                build_final_contact_sheet(records, root, output),
            )
            with Image.open(output) as sheet:
                self.assertEqual((1364, 866), sheet.size)
            with self.assertRaisesRegex(ValueError, "ten accepted works"):
                build_final_contact_sheet(records[:9], root, root / "bad.webp")

            wrong = [dict(record) for record in records]
            wrong[-1]["pose"] = wrong[0]["pose"]
            with self.assertRaisesRegex(ValueError, "canonical pose"):
                build_final_contact_sheet(wrong, root, root / "wrong.webp")
