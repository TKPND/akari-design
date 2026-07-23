from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image
import yaml

from scripts.build_v1_2_daily_comparison import build_daily_comparison


DESCRIPTOR = "morning-rug-daze"


def candidate_path(
    variant: str,
    descriptor: str = DESCRIPTOR,
    revision: str = "r01",
) -> Path:
    return Path(f"source/candidates/d02/{revision}") / (
        f"akari-v1.2_d02_{descriptor}_{revision}-{variant}.png"
    )


def make_request(
    root: Path,
    variants=("a", "b"),
    revision: str = "r01",
) -> Path:
    manifest = root / "manifest/assets.yaml"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        yaml.safe_dump(
            {
                "assets": [
                    {"asset_id": "D02", "descriptor": DESCRIPTOR}
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
                "asset_id": "D02",
                "revision": revision,
                "candidates": [
                    {
                        "variant": variant,
                        "title": f"independent-scene-{variant}",
                        "target_path": candidate_path(
                            variant, revision=revision
                        ).as_posix(),
                    }
                    for variant in variants
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return request


def write_candidates(
    root: Path,
    variants=("a", "b"),
    descriptor: str = DESCRIPTOR,
    revision: str = "r01",
) -> None:
    colors = {"a": "red", "b": "blue", "c": "green"}
    for variant in variants:
        path = root / candidate_path(variant, descriptor, revision)
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (300, 480), colors[variant]).save(path)


class DailyComparisonTests(unittest.TestCase):
    def test_builds_ab_in_declared_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            write_candidates(root)
            output = root / "comparison.webp"

            result = build_daily_comparison(
                make_request(root),
                root,
                output,
                expected_asset_id="D02",
            )

            self.assertEqual(result, output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (660, 566))
                self.assertGreater(image.getpixel((170, 260))[0], 180)
                self.assertGreater(image.getpixel((490, 260))[2], 120)

    def test_builds_abc_in_declared_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            write_candidates(root, ("a", "b", "c"))
            output = root / "comparison.webp"

            build_daily_comparison(
                make_request(root, ("a", "b", "c")),
                root,
                output,
                expected_asset_id="D02",
            )

            with Image.open(output) as image:
                self.assertEqual(image.size, (980, 566))
                self.assertGreater(image.getpixel((170, 260))[0], 180)
                self.assertGreater(image.getpixel((490, 260))[2], 120)
                self.assertGreater(image.getpixel((810, 260))[1], 60)

    def test_builds_r02_ab_from_revision_scoped_paths(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            write_candidates(root, revision="r02")
            output = root / "comparison.webp"

            result = build_daily_comparison(
                make_request(root, revision="r02"),
                root,
                output,
                expected_asset_id="D02",
            )

            self.assertEqual(result, output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (660, 566))

    def test_rejects_reversed_or_skipped_variants(self):
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
                    build_daily_comparison(
                        request,
                        root,
                        root / "out.webp",
                        expected_asset_id="D02",
                    )

    def test_rejects_noncanonical_candidate_paths(self):
        canonical = candidate_path("a").as_posix()
        replacements = (
            "/tmp/d02.png",
            "source/candidates/d02/r01/../d02.png",
            f"./{canonical}",
            canonical.replace("source/", "source//", 1),
            f"{canonical}/",
            "source/candidates/d02/other/"
            "akari-v1.2_d02_morning-rug-daze_r01-a.png",
            "source/candidates/d02/r01/"
            "akari-v1.2_d02_morning-rug-daze_r01-b.png",
        )
        for replacement in replacements:
            with (
                self.subTest(replacement=replacement),
                TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                write_candidates(root)
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
                    build_daily_comparison(
                        request,
                        root,
                        root / "out.webp",
                        expected_asset_id="D02",
                    )

    def test_rejects_same_wrong_descriptor_for_every_candidate(self):
        wrong_descriptor = "morning-window-daze"
        with TemporaryDirectory() as directory:
            root = Path(directory)
            write_candidates(root, descriptor=wrong_descriptor)
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
                build_daily_comparison(
                    request,
                    root,
                    root / "out.webp",
                    expected_asset_id="D02",
                )

    def test_rejects_wrong_descriptor(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            write_candidates(root)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            data["candidates"][1]["target_path"] = candidate_path(
                "b", "morning-window-daze"
            ).as_posix()
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "Daily candidate descriptor mismatch"
            ):
                build_daily_comparison(
                    request,
                    root,
                    root / "out.webp",
                    expected_asset_id="D02",
                )

    def test_rejects_wrong_filename_suffix(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            write_candidates(root)
            request = make_request(root)
            data = yaml.safe_load(request.read_text(encoding="utf-8"))
            data["candidates"][0]["target_path"] = (
                "source/candidates/d02/r01/"
                "akari-v1.2_d02_morning-rug-daze_r01-a.jpg"
            )
            request.write_text(
                yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "Daily candidate sources must remain canonical"
            ):
                build_daily_comparison(
                    request,
                    root,
                    root / "out.webp",
                    expected_asset_id="D02",
                )

    def test_rejects_missing_source(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = make_request(root)
            with self.assertRaisesRegex(ValueError, "missing .*r01-a.png"):
                build_daily_comparison(
                    request,
                    root,
                    root / "out.webp",
                    expected_asset_id="D02",
                )

    def test_rejects_candidate_directory_symlink_escape(self):
        with TemporaryDirectory() as directory, TemporaryDirectory() as outside:
            root = Path(directory)
            candidate_dir = root / "source/candidates/d02/r01"
            candidate_dir.parent.mkdir(parents=True)
            candidate_dir.symlink_to(Path(outside), target_is_directory=True)
            request = make_request(root)
            with self.assertRaisesRegex(
                ValueError, "Daily candidate sources must remain canonical"
            ):
                build_daily_comparison(
                    request,
                    root,
                    root / "out.webp",
                    expected_asset_id="D02",
                )

    def test_rejects_candidate_file_symlink_escape(self):
        with TemporaryDirectory() as directory, TemporaryDirectory() as outside:
            root = Path(directory)
            candidate_dir = root / "source/candidates/d02/r01"
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
                build_daily_comparison(
                    request,
                    root,
                    root / "out.webp",
                    expected_asset_id="D02",
                )


if __name__ == "__main__":
    unittest.main()
