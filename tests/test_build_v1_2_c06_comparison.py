from pathlib import Path
from tempfile import TemporaryDirectory
import copy
import unittest

from PIL import Image, ImageColor
import yaml

from scripts.build_v1_2_c06_comparison import build_c06_comparison


STAGES = (
    ("c06-1", "sleepy-neutral"),
    ("c06-2", "sleepy-secure"),
    ("c06-3", "loosened-mouth"),
    ("c06-4", "soft-smile"),
)
COLORS = {
    "a": ("red", "green", "blue", "yellow"),
    "b": ("magenta", "cyan", "orange", "purple"),
    "c": ("brown", "pink", "lime", "navy"),
}


def source_path(variant: str, stage_index: int) -> Path:
    stage, descriptor = STAGES[stage_index]
    return Path("source/candidates/c06/r01") / (
        f"akari-v1.2_{stage}_{descriptor}_r01-{variant}.png"
    )


def make_request(root: Path) -> Path:
    for variant, colors in COLORS.items():
        for index, color in enumerate(colors):
            path = root / source_path(variant, index)
            path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (300, 480), color).save(path)
    request = root / "request.yaml"
    request.write_text(
        yaml.safe_dump(
            {
                "stages": [
                    {
                        "stage": stage,
                        "descriptor": descriptor,
                        "prompt_delta": f"{stage} prompt",
                    }
                    for stage, descriptor in STAGES
                ],
                "review_sets": [
                    {
                        "candidate_id": f"c06-r01-{variant}",
                        "source_paths": [
                            source_path(variant, index).as_posix()
                            for index in range(4)
                        ],
                    }
                    for variant in ("a", "b")
                ],
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


class C06ComparisonTests(unittest.TestCase):
    def test_builds_initial_two_by_four_board_in_review_set_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "comparison.webp"
            build_c06_comparison(make_request(root), root, output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (1300, 1112))
                for row, variant in enumerate(("a", "b")):
                    for column, color in enumerate(COLORS[variant]):
                        assert_color_close(
                            self,
                            image.getpixel(
                                (170 + column * 320, 260 + row * 546)
                            ),
                            color,
                        )

    def test_builds_literal_targeted_repair_row(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            sources = copy.deepcopy(data["review_sets"][0]["source_paths"])
            sources[2] = source_path("c", 2).as_posix()
            data["review_sets"].append(
                {
                    "candidate_id": "c06-r01-a-repair-c06-3",
                    "source_paths": sources,
                }
            )
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            output = root / "repair.webp"
            build_c06_comparison(request, root, output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (1300, 1658))
                expected = ("red", "green", "lime", "yellow")
                for column, color in enumerate(expected):
                    assert_color_close(
                        self,
                        image.getpixel((170 + column * 320, 1352)),
                        color,
                    )

    def test_rejects_a_row_populated_with_b_sources(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            data["review_sets"][0]["source_paths"] = copy.deepcopy(
                data["review_sets"][1]["source_paths"]
            )
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "review set sources must match C06 stage order"
            ):
                build_c06_comparison(request, root, root / "swapped.webp")

    def test_rejects_targeted_repair_c_at_the_wrong_stage(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            sources = copy.deepcopy(data["review_sets"][0]["source_paths"])
            sources[1] = source_path("c", 1).as_posix()
            data["review_sets"].append(
                {
                    "candidate_id": "c06-r01-a-repair-c06-3",
                    "source_paths": sources,
                }
            )
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "review set sources must match C06 stage order"
            ):
                build_c06_comparison(
                    request, root, root / "wrong-repair-stage.webp"
                )

    def test_rejects_targeted_repair_c_at_more_than_one_stage(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            sources = copy.deepcopy(data["review_sets"][0]["source_paths"])
            sources[1] = source_path("c", 1).as_posix()
            sources[2] = source_path("c", 2).as_posix()
            data["review_sets"].append(
                {
                    "candidate_id": "c06-r01-a-repair-c06-3",
                    "source_paths": sources,
                }
            )
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "review set sources must match C06 stage order"
            ):
                build_c06_comparison(
                    request, root, root / "multiple-repair-stages.webp"
                )

    def test_builds_complete_c_family_row(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            data["review_sets"].append(
                {
                    "candidate_id": "c06-r01-c",
                    "source_paths": [
                        source_path("c", index).as_posix()
                        for index in range(4)
                    ],
                }
            )
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            output = root / "complete-c.webp"
            build_c06_comparison(request, root, output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (1300, 1658))
                for column, color in enumerate(COLORS["c"]):
                    assert_color_close(
                        self,
                        image.getpixel((170 + column * 320, 1352)),
                        color,
                    )

    def test_rejects_duplicate_complete_ab_third_row(self):
        for index, variant in enumerate(("a", "b")):
            with self.subTest(variant=variant), TemporaryDirectory() as directory:
                root = Path(directory)
                request = make_request(root)
                data = yaml.safe_load(request.read_text(encoding="utf-8"))
                data["review_sets"].append(
                    copy.deepcopy(data["review_sets"][index])
                )
                request.write_text(
                    yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "expected C06 C or targeted repair review set third",
                ):
                    build_c06_comparison(
                        request, root, root / f"duplicate-{variant}.webp"
                    )

    def test_rejects_reordered_stages(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            data["stages"].reverse()
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "expected C06 stage order"):
                build_c06_comparison(request, root, root / "out.webp")

    def test_rejects_reordered_or_incomplete_review_sets(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))

            reordered = copy.deepcopy(data)
            reordered["review_sets"].reverse()
            request.write_text(
                yaml.safe_dump(reordered, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "expected C06 A and B review sets first"
            ):
                build_c06_comparison(request, root, root / "reordered.webp")

            incomplete = copy.deepcopy(data)
            incomplete["review_sets"][0]["source_paths"].pop()
            request.write_text(
                yaml.safe_dump(incomplete, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "expected four ordered C06 sources"
            ):
                build_c06_comparison(request, root, root / "incomplete.webp")

    def test_rejects_source_path_traversal(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            escaped = (
                Path("source/candidates/c06/r01/../escaped")
                / source_path("a", 0).name
            )
            escaped_target = (root / escaped).resolve()
            escaped_target.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (300, 480), "red").save(escaped_target)
            data["review_sets"][0]["source_paths"][0] = escaped.as_posix()
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "review set sources must match C06 stage order"
            ):
                build_c06_comparison(request, root, root / "traversal.webp")

    def test_rejects_canonical_source_directory_symlink_outside_package(self):
        with TemporaryDirectory() as directory:
            workspace = Path(directory)
            root = workspace / "package"
            request = make_request(root)
            canonical = root / "source/candidates/c06/r01"
            outside = workspace / "outside-r01"
            canonical.rename(outside)
            canonical.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(
                ValueError, "review set sources must match C06 stage order"
            ):
                build_c06_comparison(
                    request, root, root / "directory-symlink.webp"
                )

    def test_rejects_candidate_file_symlink_outside_canonical_directory(self):
        with TemporaryDirectory() as directory:
            workspace = Path(directory)
            root = workspace / "package"
            request = make_request(root)
            canonical = root / source_path("a", 0)
            outside = workspace / canonical.name
            canonical.rename(outside)
            canonical.symlink_to(outside)
            with self.assertRaisesRegex(
                ValueError, "review set sources must match C06 stage order"
            ):
                build_c06_comparison(
                    request, root, root / "file-symlink.webp"
                )

    def test_rejects_a_missing_source(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            (root / source_path("b", 1)).unlink()
            with self.assertRaisesRegex(ValueError, "missing"):
                build_c06_comparison(request, root, root / "missing.webp")


if __name__ == "__main__":
    unittest.main()
