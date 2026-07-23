from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from PIL import Image
import yaml

from scripts import build_v1_2_c01_comparison as comparison
from scripts.build_v1_2_c01_comparison import build_comparison


class C01ComparisonTests(unittest.TestCase):
    def make_request(self, root: Path) -> Path:
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

    def test_builds_three_column_sheet_in_request_order(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "comparison.webp"
            result = build_comparison(self.make_request(root), root, output)
            self.assertEqual(result, output)
            with Image.open(result) as image:
                self.assertEqual(image.size, (980, 566))

    def test_rejects_a_missing_candidate(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            request = self.make_request(root)
            (root / "candidates/candidate-b.png").unlink()
            with self.assertRaisesRegex(ValueError, "missing candidate-b.png"):
                build_comparison(request, root, root / "comparison.webp")

    def test_default_cli_resolves_candidates_from_package_root(self):
        with (
            patch.object(
                comparison,
                "build_comparison",
                return_value=comparison.OUTPUT,
            ) as build,
            patch("sys.argv", ["build_v1_2_c01_comparison.py"]),
            patch("builtins.print"),
        ):
            comparison.main()

        build.assert_called_once_with(
            comparison.REQUEST,
            comparison.ROOT / "akari-v1.2",
            comparison.OUTPUT,
        )

    def test_direct_script_entrypoint_loads_generic_builder(self):
        result = subprocess.run(
            [
                sys.executable,
                comparison.ROOT / "scripts/build_v1_2_c01_comparison.py",
                "--help",
            ],
            cwd=comparison.ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
