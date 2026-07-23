from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image, ImageColor
import yaml

from scripts.build_v1_2_paired_candidate_comparison import (
    build_paired_comparison,
)


PAIR_COLORS = (
    ("red", "green"),
    ("blue", "yellow"),
    ("magenta", "cyan"),
)


def make_request(root: Path) -> Path:
    candidates = []
    for variant, colors in zip(("a", "b", "c"), PAIR_COLORS):
        outputs = []
        for view, color in zip(("standing", "seated"), colors):
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
                "view_prompts": {
                    "standing": "Standing view.",
                    "seated": "Seated view.",
                },
                "candidates": candidates,
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


class PairedCandidateComparisonTests(unittest.TestCase):
    def test_builds_two_pair_rows_when_request_closes_after_b(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            data["candidates"] = data["candidates"][:2]
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            output = root / "pair.webp"
            build_paired_comparison(request, root, output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (660, 1112))
                expected = (
                    ((170, 260), "red"),
                    ((490, 260), "green"),
                    ((170, 806), "blue"),
                    ((490, 806), "yellow"),
                )
                for point, color in expected:
                    assert_color_close(self, image.getpixel(point), color)

    def test_builds_three_pair_rows_in_request_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            output = root / "pair.webp"
            build_paired_comparison(request, root, output)
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

    def test_rejects_reordered_pair_views(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            data["candidates"][0]["outputs"].reverse()
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "expected paired view order"):
                build_paired_comparison(request, root, root / "pair.webp")

    def test_rejects_missing_pair_member(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            (root / "candidates/b-seated.png").unlink()
            with self.assertRaisesRegex(ValueError, "missing b-seated.png"):
                build_paired_comparison(request, root, root / "pair.webp")


if __name__ == "__main__":
    unittest.main()
