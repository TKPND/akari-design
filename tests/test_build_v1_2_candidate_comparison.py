from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image, ImageColor
import yaml

from scripts.build_v1_2_candidate_comparison import build_comparison


def make_request(root: Path) -> Path:
    candidates = []
    for variant, color in zip(("a", "b", "c"), ("red", "green", "blue")):
        target = Path("candidates") / f"candidate-{variant}.png"
        path = root / target
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (200, 300), color).save(path)
        candidates.append(
            {
                "variant": variant,
                "title": f"variant-{variant}",
                "target_path": target.as_posix(),
            }
        )
    request = root / "request.yaml"
    request.write_text(
        yaml.safe_dump({"candidates": candidates}, sort_keys=False),
        encoding="utf-8",
    )
    return request


def assert_color_close(testcase, actual, expected_name):
    expected = ImageColor.getrgb(expected_name)
    testcase.assertTrue(
        all(abs(left - right) <= 20 for left, right in zip(actual, expected)),
        (actual, expected),
    )


class CandidateComparisonTests(unittest.TestCase):
    def test_builds_three_cards_in_request_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "selection.webp"
            build_comparison(make_request(root), root, output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (980, 566))
                for x, color in zip((170, 490, 810), ("red", "green", "blue")):
                    assert_color_close(self, image.getpixel((x, 200)), color)

    def test_builds_anchor_then_three_candidates(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            anchor = root / "anchor.png"
            Image.new("RGB", (200, 300), "yellow").save(anchor)
            output = root / "alignment.webp"
            build_comparison(make_request(root), root, output, anchor)
            with Image.open(output) as image:
                self.assertEqual(image.size, (1300, 566))
                expected = ("yellow", "red", "green", "blue")
                for index, color in enumerate(expected):
                    assert_color_close(
                        self, image.getpixel((170 + index * 320, 200)), color
                    )

    def test_rejects_a_missing_candidate(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            (root / "candidates/candidate-b.png").unlink()
            with self.assertRaisesRegex(ValueError, "missing candidate-b.png"):
                build_comparison(request, root, root / "comparison.webp")

    def test_rejects_a_missing_anchor(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "missing anchor.png"):
                build_comparison(
                    make_request(root), root, root / "out.webp", root / "anchor.png"
                )


if __name__ == "__main__":
    unittest.main()
