import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.build_tonari_no_coordinate_contact_sheet import (
    ROOT,
    build_contact_sheet,
    display_output_path,
    fit_text_to_width,
    label_lines_for,
    load_font,
    text_width,
)


class TonariNoCoordinateContactSheetTest(unittest.TestCase):
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
            generated_dir = temp_path / "generated"
            output_path = temp_path / "sheet.webp"
            generated_dir.mkdir()

            first_image = generated_dir / "20260706_first_v1.webp"
            second_image = generated_dir / "20260706_second_v1.webp"
            Image.new("RGB", (320, 480), "#d9eee9").save(first_image)
            Image.new("RGB", (320, 480), "#f0dfd1").save(second_image)

            requests = [
                {
                    "slot": "first",
                    "japanese_title": "一枚目",
                    "outfit_family": "layering",
                    "target_path": first_image.as_posix(),
                },
                {
                    "slot": "second",
                    "japanese_title": "二枚目",
                    "outfit_family": "knit_soft",
                    "target_path": second_image.as_posix(),
                },
                {
                    "slot": "missing",
                    "japanese_title": "未生成",
                    "outfit_family": "roomwear_relaxed",
                    "target_path": (generated_dir / "missing.webp").as_posix(),
                },
            ]

            result = build_contact_sheet(
                requests=requests,
                project_root=temp_path,
                output_path=output_path,
                columns=2,
                thumb_width=160,
                label_height=48,
                gap=12,
            )

            self.assertEqual(output_path, result)
            self.assertTrue(output_path.is_file())
            with Image.open(output_path) as sheet:
                self.assertEqual((356, 312), sheet.size)
                self.assertRgbClose(sheet.getpixel((20, 20)), (217, 238, 233))
                self.assertRgbClose(sheet.getpixel((192, 20)), (240, 223, 209))

    def test_build_contact_sheet_fails_when_no_images_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            with self.assertRaisesRegex(ValueError, "No generated coordinate images found"):
                build_contact_sheet(
                    requests=[
                        {
                            "slot": "missing",
                            "japanese_title": "未生成",
                            "outfit_family": "roomwear_relaxed",
                            "target_path": "source/generated/tonari-no-coordinate/missing.webp",
                        }
                    ],
                    project_root=temp_path,
                    output_path=temp_path / "sheet.webp",
                    columns=2,
                    thumb_width=160,
                    label_height=48,
                    gap=12,
                )

    def test_build_contact_sheet_rejects_zero_columns(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            generated_dir = temp_path / "generated"
            generated_dir.mkdir()
            image_path = generated_dir / "20260706_first_v1.webp"
            Image.new("RGB", (320, 480), "#d9eee9").save(image_path)

            with self.assertRaisesRegex(ValueError, "columns must be at least 1"):
                build_contact_sheet(
                    requests=[
                        {
                            "slot": "first",
                            "japanese_title": "一枚目",
                            "outfit_family": "layering",
                            "target_path": image_path.as_posix(),
                        }
                    ],
                    project_root=temp_path,
                    output_path=temp_path / "sheet.webp",
                    columns=0,
                    thumb_width=160,
                    label_height=48,
                    gap=12,
                )

    def test_fit_text_to_width_truncates_long_text_with_ascii_ellipsis(self):
        font = load_font(16)
        max_width = 90
        text = "ロングスカートと柔らかトップス / long-skirt-soft-top"

        fitted = fit_text_to_width(text, font, max_width)

        self.assertNotEqual(text, fitted)
        self.assertTrue(fitted.endswith("..."))
        self.assertLessEqual(text_width(fitted, font), max_width)

    def test_load_font_renders_japanese_glyphs_distinctly(self):
        font = load_font(16)

        spring_mask = font.getmask("春")
        katakana_mask = font.getmask("カ")

        self.assertNotEqual(
            (spring_mask.size, bytes(spring_mask)),
            (katakana_mask.size, bytes(katakana_mask)),
        )

    def test_load_font_renders_latin_glyphs_distinctly(self):
        font = load_font(13)

        latin_mask = font.getmask("spring")
        missing_mask = font.getmask("□□□□□□")

        self.assertNotEqual(
            (latin_mask.size, bytes(latin_mask)),
            (missing_mask.size, bytes(missing_mask)),
        )

    def test_real_contact_sheet_labels_fit_default_card_width(self):
        requests_path = ROOT / "source/manifests/tonari-no-coordinate/generation-requests.json"
        with requests_path.open(encoding="utf-8") as requests_file:
            requests = json.load(requests_file)["requests"]
        font = load_font(16)
        small_font = load_font(13)
        max_width = 264

        for request in requests:
            with self.subTest(slot=request["slot"]):
                title_line, detail_line = label_lines_for(request, font, small_font, max_width)

                self.assertLessEqual(text_width(title_line, font), max_width)
                self.assertLessEqual(text_width(detail_line, small_font), max_width)

    def test_real_cute_healthy_seasonal_labels_fit_default_card_width(self):
        requests_path = (
            ROOT
            / "source/manifests/tonari-no-coordinate/cute-healthy-seasonal-outing-requests.json"
        )
        with requests_path.open(encoding="utf-8") as requests_file:
            requests = json.load(requests_file)["requests"]
        font = load_font(16)
        small_font = load_font(13)
        max_width = 264

        for request in requests:
            with self.subTest(slot=request["slot"]):
                title_line, detail_line = label_lines_for(request, font, small_font, max_width)

                self.assertLessEqual(text_width(title_line, font), max_width)
                self.assertLessEqual(text_width(detail_line, small_font), max_width)

    def test_real_hoodie_everyday_labels_fit_default_card_width(self):
        requests_path = (
            ROOT
            / "source/manifests/tonari-no-coordinate/hoodie-everyday-coordinate-requests.json"
        )
        with requests_path.open(encoding="utf-8") as requests_file:
            requests = json.load(requests_file)["requests"]
        font = load_font(16)
        small_font = load_font(13)
        max_width = 264

        for request in requests:
            with self.subTest(slot=request["slot"]):
                title_line, detail_line = label_lines_for(
                    request,
                    font,
                    small_font,
                    max_width,
                )

                self.assertLessEqual(text_width(title_line, font), max_width)
                self.assertLessEqual(text_width(detail_line, small_font), max_width)

    def test_display_output_path_prefers_repo_relative_path(self):
        path = ROOT / "evidence/tonari-no-coordinate/contact-sheets/sheet.webp"

        self.assertEqual(
            "evidence/tonari-no-coordinate/contact-sheets/sheet.webp",
            display_output_path(path),
        )

    def test_display_output_path_supports_external_absolute_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sheet.webp"

            self.assertEqual(path.as_posix(), display_output_path(path))


if __name__ == "__main__":
    unittest.main()
