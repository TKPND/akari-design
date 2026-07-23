import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image, ImageColor
import yaml

from scripts import build_v1_2_c03_comparisons as comparisons


PAIR_COLORS = (
    ("red", "green"),
    ("blue", "yellow"),
    ("magenta", "cyan"),
)


def make_request(root: Path) -> Path:
    anchors = root / "anchors"
    anchors.mkdir(parents=True)
    Image.new("RGB", (300, 480), "black").save(anchors / "c01.png")
    Image.new("RGB", (300, 480), "white").save(anchors / "c02.png")
    candidates = []
    for variant, colors in zip(("a", "b", "c"), PAIR_COLORS):
        outputs = []
        for view, color in zip(
            ("hairpin-side-45", "non-hairpin-side-45"), colors
        ):
            target = Path("candidates") / f"{variant}-{view}.png"
            path = root / target
            path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (300, 480), color).save(path)
            outputs.append({"view": view, "target_path": target.as_posix()})
        candidates.append(
            {
                "variant": variant,
                "title": f"paired-attempt-{variant}",
                "outputs": outputs,
            }
        )
    request = root / "request.yaml"
    request.write_text(
        yaml.safe_dump(
            {
                "candidates": candidates,
                "comparison_anchors": ["anchors/c01.png", "anchors/c02.png"],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return request


def assert_color_close(testcase, actual, expected_name):
    expected = ImageColor.getrgb(expected_name)
    testcase.assertTrue(
        all(abs(left - right) <= 20 for left, right in zip(actual, expected)),
        (actual, expected),
    )


def get_builder(testcase):
    builder = getattr(comparisons, "build_c03_comparison", None)
    testcase.assertIsNotNone(builder)
    return builder


class C03ComparisonModuleTests(unittest.TestCase):
    def test_c03_comparison_module_exists(self):
        self.assertIsNotNone(
            importlib.util.find_spec("scripts.build_v1_2_c03_comparisons")
        )

    def test_pair_grid_is_three_rows_by_two_columns(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "pair.webp"
            get_builder(self)(make_request(root), root, output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (660, 1658))
                expected = (
                    ((170, 260), "red"),
                    ((490, 260), "green"),
                    ((170, 806), "blue"),
                    ((490, 806), "yellow"),
                    ((170, 1352), "magenta"),
                    ((490, 1352), "cyan"),
                )
                for point, color in expected:
                    assert_color_close(self, image.getpixel(point), color)

    def test_alignment_grid_repeats_c01_pair_c02_pair_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "alignment.webp"
            get_builder(self)(make_request(root), root, output, alignment=True)
            with Image.open(output) as image:
                self.assertEqual(image.size, (1300, 1658))
                expected = ("black", "red", "white", "green")
                for x, color in zip((170, 490, 810, 1130), expected):
                    assert_color_close(self, image.getpixel((x, 260)), color)

    def test_rejects_a_missing_paired_output(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            (root / "candidates/b-non-hairpin-side-45.png").unlink()
            with self.assertRaisesRegex(
                ValueError, "missing b-non-hairpin-side-45.png"
            ):
                get_builder(self)(request, root, root / "pair.webp")

    def test_rejects_a_missing_alignment_anchor(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            (root / "anchors/c02.png").unlink()
            with self.assertRaisesRegex(ValueError, "missing c02.png"):
                get_builder(self)(
                    request, root, root / "alignment.webp", alignment=True
                )

    def test_rejects_reordered_candidate_variants(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            data["candidates"].reverse()
            request.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "expected candidates a, b, c"):
                get_builder(self)(request, root, root / "pair.webp")

    def test_rejects_reordered_view_names(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            data["candidates"][0]["outputs"].reverse()
            request.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "expected paired view order"):
                get_builder(self)(request, root, root / "pair.webp")


if __name__ == "__main__":
    unittest.main()
