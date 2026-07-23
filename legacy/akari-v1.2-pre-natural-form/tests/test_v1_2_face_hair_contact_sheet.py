import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.build_v1_2_face_hair_contact_sheet import (
    ROOT,
    build_contact_sheet,
    display_output_path,
    fit_text_to_width,
    label_lines_for,
    load_font,
    text_width,
)


class AkariV12FaceHairContactSheetTest(unittest.TestCase):
    def assertRgbClose(self, actual, expected, tolerance=5):
        for actual_channel, expected_channel in zip(actual[:3], expected):
            self.assertLessEqual(
                abs(actual_channel - expected_channel),
                tolerance,
                f"{actual[:3]} is not within {tolerance} of {expected}",
            )

    def test_build_contact_sheet_uses_existing_images_and_writes_sheet(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            generated_dir = temp_path / "source/generated/v1-2-face-hair"
            output_path = temp_path / "evidence/v1-2-face-hair/contact-sheets/sheet.webp"
            generated_dir.mkdir(parents=True)

            first_image = generated_dir / "20260708_soft-horizontal-eyes_v1.png"
            second_image = generated_dir / "20260708_round-innocent-eyes_v1.png"
            Image.new("RGB", (320, 320), "#d9eee9").save(first_image)
            Image.new("RGB", (320, 320), "#f0dfd1").save(second_image)

            requests = [
                {
                    "candidate_order": 1,
                    "slot": "soft-horizontal-eyes",
                    "japanese_title": "柔らかい水平寄りの目",
                    "eye_variation": "soft horizontal eyes with calm direct gaze",
                    "hair_variation": "baseline organized short bob",
                    "target_path": first_image.as_posix(),
                },
                {
                    "candidate_order": 2,
                    "slot": "round-innocent-eyes",
                    "japanese_title": "少し丸くあどけない目",
                    "eye_variation": "slightly rounder eyes with strong innocence",
                    "hair_variation": "soft rounded bangs",
                    "target_path": second_image.as_posix(),
                },
                {
                    "candidate_order": 3,
                    "slot": "missing",
                    "japanese_title": "未生成",
                    "eye_variation": "missing image",
                    "hair_variation": "missing image",
                    "target_path": (generated_dir / "missing.png").as_posix(),
                },
            ]

            result = build_contact_sheet(
                requests=requests,
                project_root=temp_path,
                output_path=output_path,
                columns=2,
                thumb_width=160,
                label_height=66,
                gap=12,
            )

            self.assertEqual(output_path, result)
            self.assertTrue(output_path.is_file())
            with Image.open(output_path) as sheet:
                self.assertEqual((356, 250), sheet.size)
                self.assertRgbClose(sheet.getpixel((20, 20)), (217, 238, 233))
                self.assertRgbClose(sheet.getpixel((192, 20)), (240, 223, 209))

    def test_build_contact_sheet_fails_when_no_images_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            with self.assertRaisesRegex(
                ValueError,
                "No generated v1.2 face/hair images found",
            ):
                build_contact_sheet(
                    requests=[
                        {
                            "candidate_order": 1,
                            "slot": "missing",
                            "japanese_title": "未生成",
                            "eye_variation": "missing image",
                            "hair_variation": "missing image",
                            "target_path": "source/generated/v1-2-face-hair/missing.png",
                        }
                    ],
                    project_root=temp_path,
                    output_path=temp_path / "sheet.webp",
                    columns=2,
                    thumb_width=160,
                    label_height=66,
                    gap=12,
                )

    def test_build_contact_sheet_rejects_zero_columns(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            generated_dir = temp_path / "source/generated/v1-2-face-hair"
            generated_dir.mkdir(parents=True)
            image_path = generated_dir / "20260708_soft-horizontal-eyes_v1.png"
            Image.new("RGB", (320, 320), "#d9eee9").save(image_path)

            with self.assertRaisesRegex(ValueError, "columns must be at least 1"):
                build_contact_sheet(
                    requests=[
                        {
                            "candidate_order": 1,
                            "slot": "soft-horizontal-eyes",
                            "japanese_title": "柔らかい水平寄りの目",
                            "eye_variation": "soft horizontal eyes with calm direct gaze",
                            "hair_variation": "baseline organized short bob",
                            "target_path": image_path.as_posix(),
                        }
                    ],
                    project_root=temp_path,
                    output_path=temp_path / "sheet.webp",
                    columns=0,
                    thumb_width=160,
                    label_height=66,
                    gap=12,
                )

    def test_fit_text_to_width_truncates_long_text_with_ascii_ellipsis(self):
        font = load_font(16)
        max_width = 120
        text = "balanced hybrid candidate based on strongest prior traits"

        fitted = fit_text_to_width(text, font, max_width)

        self.assertNotEqual(text, fitted)
        self.assertTrue(fitted.endswith("..."))
        self.assertLessEqual(text_width(fitted, font), max_width)

    def test_load_font_renders_japanese_glyphs_distinctly(self):
        font = load_font(16)

        soft_mask = font.getmask("柔")
        eye_mask = font.getmask("目")

        self.assertNotEqual(
            (soft_mask.size, bytes(soft_mask)),
            (eye_mask.size, bytes(eye_mask)),
        )

    def test_real_contact_sheet_labels_fit_default_card_width(self):
        requests_path = ROOT / "source/manifests/v1-2-face-hair/generation-requests.json"
        with requests_path.open(encoding="utf-8") as requests_file:
            requests = json.load(requests_file)["requests"]
        font = load_font(16)
        small_font = load_font(12)
        max_width = 284

        for request in requests:
            with self.subTest(slot=request["slot"]):
                title_line, eye_line, hair_line = label_lines_for(
                    request,
                    font,
                    small_font,
                    max_width,
                )

                self.assertLessEqual(text_width(title_line, font), max_width)
                self.assertLessEqual(text_width(eye_line, small_font), max_width)
                self.assertLessEqual(text_width(hair_line, small_font), max_width)

    def test_display_output_path_prefers_repo_relative_path(self):
        path = ROOT / "evidence/v1-2-face-hair/contact-sheets/sheet.webp"

        self.assertEqual(
            "evidence/v1-2-face-hair/contact-sheets/sheet.webp",
            display_output_path(path),
        )

    def test_display_output_path_supports_external_absolute_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sheet.webp"

            self.assertEqual(path.as_posix(), display_output_path(path))

    def test_package_json_exposes_contact_sheet_script(self):
        package_json = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))

        self.assertEqual(
            "uv run python scripts/build_v1_2_face_hair_contact_sheet.py",
            package_json["scripts"]["build:v1-2-face-hair:contact-sheet"],
        )


if __name__ == "__main__":
    unittest.main()
