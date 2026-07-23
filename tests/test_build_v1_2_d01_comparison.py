from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image
import yaml

from scripts.build_v1_2_d01_comparison import build_d01_comparison


def candidate_path(
    variant: str, descriptor: str = "morning-bedside"
) -> Path:
    return Path("source/candidates/d01/r01") / (
        f"akari-v1.2_d01_{descriptor}_r01-{variant}.png"
    )


def make_request(root: Path, variants=("a", "b")) -> Path:
    manifest = root / "manifest/assets.yaml"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        yaml.safe_dump(
            {
                "assets": [
                    {"asset_id": "D01", "descriptor": "morning-bedside"}
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    request = root / "request.yaml"
    request.write_text(
        yaml.safe_dump(
            {
                "asset_id": "D01",
                "revision": "r01",
                "candidates": [
                    {
                        "variant": variant,
                        "title": f"independent-scene-{variant}",
                        "target_path": candidate_path(variant).as_posix(),
                    }
                    for variant in variants
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return request


class D01ComparisonTests(unittest.TestCase):
    def test_builds_ab_in_declared_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for variant, color in (("a", "red"), ("b", "blue")):
                path = root / candidate_path(variant)
                path.parent.mkdir(parents=True, exist_ok=True)
                Image.new("RGB", (300, 480), color).save(path)
            output = root / "comparison.webp"
            build_d01_comparison(make_request(root), root, output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (660, 566))
                self.assertGreater(image.getpixel((170, 260))[0], 180)
                self.assertGreater(image.getpixel((490, 260))[2], 120)

    def test_builds_abc_in_declared_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for variant, color in (
                ("a", "red"),
                ("b", "blue"),
                ("c", "green"),
            ):
                path = root / candidate_path(variant)
                path.parent.mkdir(parents=True, exist_ok=True)
                Image.new("RGB", (300, 480), color).save(path)
            output = root / "comparison.webp"
            build_d01_comparison(
                make_request(root, ("a", "b", "c")), root, output
            )
            with Image.open(output) as image:
                self.assertEqual(image.size, (980, 566))

    def test_rejects_variant_order_and_suffix_mismatch(self):
        for variants in (("b", "a"), ("a", "c")):
            with (
                self.subTest(variants=variants),
                TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                request = make_request(root, variants)
                with self.assertRaisesRegex(
                    ValueError, "expected Daily A/B or A/B/C candidates"
                ):
                    build_d01_comparison(request, root, root / "out.webp")

    def test_rejects_absolute_parent_and_noncanonical_sources(self):
        canonical = candidate_path("a").as_posix()
        replacements = (
            "/tmp/d01.png",
            "source/candidates/d01/r01/../d01.png",
            f"./{canonical}",
            canonical.replace("source/", "source//", 1),
            f"{canonical}/",
            "source/candidates/d01/other/akari-v1.2_d01_morning-bedside_r01-a.png",
            "source/candidates/d01/r01/akari-v1.2_d01_morning-bedside_r01-b.png",
        )
        for replacement in replacements:
            with (
                self.subTest(replacement=replacement),
                TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                for variant in ("a", "b"):
                    path = root / candidate_path(variant)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    Image.new("RGB", (300, 480), "gray").save(path)
                request = make_request(root)
                data = yaml.safe_load(request.read_text(encoding="utf-8"))
                data["candidates"][0]["target_path"] = replacement
                request.write_text(
                    yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "Daily candidate sources must remain canonical",
                ):
                    build_d01_comparison(request, root, root / "out.webp")

    def test_rejects_same_wrong_descriptor_for_every_candidate(self):
        wrong_descriptor = "morning-window-daze"
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for variant, color in (("a", "red"), ("b", "blue")):
                path = root / candidate_path(variant, wrong_descriptor)
                path.parent.mkdir(parents=True, exist_ok=True)
                Image.new("RGB", (300, 480), color).save(path)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            for candidate in data["candidates"]:
                candidate["target_path"] = candidate_path(
                    candidate["variant"], wrong_descriptor
                ).as_posix()
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )

            with self.assertRaisesRegex(
                ValueError, "Daily candidate descriptor mismatch"
            ):
                build_d01_comparison(request, root, root / "out.webp")

    def test_rejects_missing_source(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            with self.assertRaisesRegex(ValueError, "missing .*r01-a.png"):
                build_d01_comparison(request, root, root / "out.webp")

    def test_rejects_candidate_directory_symlink_escape(self):
        with TemporaryDirectory() as directory, TemporaryDirectory() as outside:
            root = Path(directory)
            candidate_dir = root / "source/candidates/d01/r01"
            candidate_dir.parent.mkdir(parents=True)
            candidate_dir.symlink_to(Path(outside), target_is_directory=True)
            request = make_request(root)
            with self.assertRaisesRegex(
                ValueError, "Daily candidate sources must remain canonical"
            ):
                build_d01_comparison(request, root, root / "out.webp")

    def test_rejects_candidate_file_symlink_escape(self):
        with TemporaryDirectory() as directory, TemporaryDirectory() as outside:
            root = Path(directory)
            candidate_dir = root / "source/candidates/d01/r01"
            candidate_dir.mkdir(parents=True)
            escaped = Path(outside) / "escaped.png"
            Image.new("RGB", (300, 480), "red").save(escaped)
            (root / candidate_path("a")).symlink_to(escaped)
            Image.new("RGB", (300, 480), "blue").save(
                root / candidate_path("b")
            )
            request = make_request(root)
            with self.assertRaisesRegex(
                ValueError, "Daily candidate sources must remain canonical"
            ):
                build_d01_comparison(request, root, root / "out.webp")


if __name__ == "__main__":
    unittest.main()
