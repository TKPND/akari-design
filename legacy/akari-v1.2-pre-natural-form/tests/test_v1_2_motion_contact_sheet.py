import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.build_v1_2_motion_contact_sheet import (
    build_batch_contact_sheet,
    build_final_contact_sheet,
    main,
    select_active_requests,
)


def request(motion: str, batch: str, number: int, path: str) -> dict:
    return {
        "motion": motion,
        "batch_id": batch,
        "revision": int(batch[-1]),
        "candidate_number": number,
        "target_path": path,
    }


def make_image(path: Path, color: str = "white") -> str:
    Image.new("RGB", (1024, 1536), color).save(path)
    return path.as_posix()


def make_custom_image(
    path: Path,
    mode: str,
    size: tuple[int, int],
) -> str:
    Image.new(mode, size, "white").save(path)
    return path.as_posix()


class AkariV12MotionContactSheetTest(unittest.TestCase):
    def test_selects_three_requests_from_only_the_active_batch(self):
        manifest = {
            "active_batches": {"walking": "walking-r2"},
            "requests": [
                request(
                    "walking",
                    batch,
                    number,
                    f"{batch}-c{number}.png",
                )
                for batch in ("walking-r1", "walking-r2")
                for number in range(1, 4)
            ],
        }
        selected = select_active_requests(manifest, "walking")
        self.assertEqual(
            [1, 2, 3],
            [item["candidate_number"] for item in selected],
        )
        self.assertEqual(
            {"walking-r2"},
            {item["batch_id"] for item in selected},
        )

    def test_batch_sheet_orders_by_candidate_number_and_labels_decisions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests = [
                request(
                    "walking",
                    "walking-r1",
                    number,
                    make_image(root / f"c{number}.png"),
                )
                for number in (3, 2, 1)
            ]
            reviews = {
                f"walking-r1-c{number}": {"decision": decision}
                for number, decision in enumerate(
                    ("accept", "hold", "reject"), 1
                )
            }
            for number, item in enumerate(
                sorted(
                    requests,
                    key=lambda value: value["candidate_number"],
                ),
                1,
            ):
                item["id"] = f"walking-r1-c{number}"
            output = root / "batch.webp"
            self.assertEqual(
                output,
                build_batch_contact_sheet(requests, reviews, root, output),
            )
            with Image.open(output) as sheet:
                self.assertEqual("RGB", sheet.mode)
                self.assertEqual((1152, 638), sheet.size)

    def test_batch_sheet_rejects_missing_or_unreadable_images(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests = [
                request(
                    "walking",
                    "walking-r1",
                    number,
                    (root / f"missing-{number}.png").as_posix(),
                )
                for number in range(1, 4)
            ]
            with self.assertRaisesRegex(
                ValueError, "missing or unreadable candidate"
            ):
                build_batch_contact_sheet(
                    requests, {}, root, root / "batch.webp"
                )

    def test_batch_sheet_rejects_noncanonical_sources_without_clobbering(self):
        invalid_sources = (
            ("RGBA", (1024, 1536), "rgba.png"),
            ("L", (1024, 1536), "grayscale.png"),
            ("RGB", (1536, 1024), "landscape.png"),
            ("RGB", (512, 768), "small.png"),
        )
        for mode, size, filename in invalid_sources:
            with self.subTest(mode=mode, size=size):
                with tempfile.TemporaryDirectory() as temp_dir:
                    root = Path(temp_dir)
                    paths = [
                        make_image(root / "c1.png"),
                        make_image(root / "c2.png"),
                        make_custom_image(root / filename, mode, size),
                    ]
                    requests = [
                        request(
                            "walking",
                            "walking-r1",
                            number,
                            path,
                        )
                        for number, path in enumerate(paths, 1)
                    ]
                    output = root / "batch.webp"
                    output.write_bytes(b"existing output")
                    with self.assertRaisesRegex(
                        ValueError,
                        "candidate must be RGB 1024x1536",
                    ):
                        build_batch_contact_sheet(
                            requests, {}, root, output
                        )
                    self.assertEqual(b"existing output", output.read_bytes())

    def test_batch_sheet_rejects_mixed_or_invalid_revisions_without_output(self):
        invalid_revisions = (
            (1, 1, 2),
            (0, 0, 0),
            ("1", "1", "1"),
            (True, True, True),
        )
        for revisions in invalid_revisions:
            with self.subTest(revisions=revisions):
                with tempfile.TemporaryDirectory() as temp_dir:
                    root = Path(temp_dir)
                    requests = [
                        request(
                            "walking",
                            "walking-r1",
                            number,
                            make_image(root / f"c{number}.png"),
                        )
                        for number in range(1, 4)
                    ]
                    for item, revision in zip(requests, revisions, strict=True):
                        item["revision"] = revision
                    output = root / "batch.webp"
                    with self.assertRaisesRegex(
                        ValueError,
                        "same positive integer revision",
                    ):
                        build_batch_contact_sheet(
                            requests, {}, root, output
                        )
                    self.assertFalse(output.exists())

    def test_final_sheet_requires_walking_seated_turning_in_order(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            records = [
                {
                    "motion": motion,
                    "motion_order": order,
                    "finished_path": make_image(root / f"{motion}.webp"),
                }
                for order, motion in enumerate(
                    ("walking", "seated", "turning"), 1
                )
            ]
            with self.assertRaisesRegex(
                ValueError, "exactly three accepted motions"
            ):
                build_final_contact_sheet(
                    records[:2], root, root / "bad.webp"
                )
            output = root / "final.webp"
            self.assertEqual(
                output,
                build_final_contact_sheet(
                    list(reversed(records)), root, output
                ),
            )

    def test_final_sheet_requires_canonical_motion_order_mapping(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            records = [
                {
                    "motion": motion,
                    "motion_order": order + 1,
                    "finished_path": make_image(root / f"{motion}.webp"),
                }
                for order, motion in enumerate(
                    ("walking", "seated", "turning"), 1
                )
            ]
            output = root / "final.webp"
            output.write_bytes(b"existing output")
            with self.assertRaisesRegex(
                ValueError,
                "canonical motion_order",
            ):
                build_final_contact_sheet(records, root, output)
            self.assertEqual(b"existing output", output.read_bytes())

    def test_final_sheet_rejects_noncanonical_source_without_clobbering(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            records = [
                {
                    "motion": motion,
                    "motion_order": order,
                    "finished_path": (
                        make_custom_image(
                            root / f"{motion}.png",
                            "RGBA",
                            (1024, 1536),
                        )
                        if motion == "turning"
                        else make_image(root / f"{motion}.webp")
                    ),
                }
                for order, motion in enumerate(
                    ("walking", "seated", "turning"), 1
                )
            ]
            output = root / "final.webp"
            output.write_bytes(b"existing output")
            with self.assertRaisesRegex(
                ValueError,
                "candidate must be RGB 1024x1536",
            ):
                build_final_contact_sheet(records, root, output)
            self.assertEqual(b"existing output", output.read_bytes())

    def test_cli_supports_absolute_output_outside_project_root(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests = [
                {
                    **request(
                        "walking",
                        "walking-r1",
                        number,
                        make_image(root / f"c{number}.png"),
                    ),
                    "id": f"walking-r1-c{number}",
                }
                for number in range(1, 4)
            ]
            manifest_path = root / "requests.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "active_batches": {"walking": "walking-r1"},
                        "requests": requests,
                    }
                ),
                encoding="utf-8",
            )
            output = root / "absolute-output.webp"
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                self.assertEqual(
                    0,
                    main(
                        [
                            "--requests",
                            manifest_path.as_posix(),
                            "--motion",
                            "walking",
                            "--output",
                            output.as_posix(),
                        ]
                    ),
                )
            self.assertTrue(output.is_file())
            self.assertIn(output.as_posix(), stdout.getvalue())
