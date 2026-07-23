from __future__ import annotations

import tempfile
import unittest
import subprocess
import sys
from pathlib import Path
from shutil import copytree, ignore_patterns

import yaml
from PIL import Image

from scripts.akari_v1_2_ame_no_sei_ni_shite import approve_act
from scripts.build_ame_no_sei_ni_shite_contact_sheet import (
    build_act_sheet,
    build_candidate_sheet,
    build_first_pass_sheet,
    build_full_sheet,
)


ROOT = Path(__file__).resolve().parents[1]


class AmeNoSeiNiShiteContactSheetTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        source = ROOT / "akari-v1.2/artbooks/ame-no-sei-ni-shite"
        copytree(
            source,
            self.root / "akari-v1.2/artbooks/ame-no-sei-ni-shite",
            ignore=ignore_patterns("accepted", "evidence", "release", "source"),
        )
        self.package = self.root / "akari-v1.2/artbooks/ame-no-sei-ni-shite"
        index_path = self.package / "manifest/scenes/index.yaml"
        data = yaml.safe_load(index_path.read_text(encoding="utf-8"))
        for scene in data["scenes"]:
            scene.update(
                {
                    "status": "planned",
                    "accepted_path": None,
                    "accepted_sha256": None,
                    "review_path": None,
                }
            )
        index_path.write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )

    def _image(self, path: Path, color: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (1536, 1024), color).save(path)

    def _accept_act_one_fixtures(self) -> None:
        index_path = self.package / "manifest/scenes/index.yaml"
        data = yaml.safe_load(index_path.read_text(encoding="utf-8"))
        for offset, scene in enumerate(data["scenes"][:3], start=1):
            scene_id = scene["id"]
            accepted = self.package / f"accepted/{scene_id}.webp"
            self._image(accepted, f"#{offset}{offset}{offset}{offset}{offset}{offset}")
            review = self.package / f"evidence/reviews/{scene_id}.yaml"
            review.parent.mkdir(parents=True, exist_ok=True)
            review.write_text("status: accepted\n", encoding="utf-8")
            scene.update(
                {
                    "revision": "r01",
                    "status": "accepted",
                    "candidates": [
                        {
                            "variant": variant,
                            "path": (
                                f"source/candidates/{scene_id}/r01/"
                                f"{scene_id}-r01-{variant}.png"
                            ),
                        }
                        for variant in ("a", "b")
                    ],
                    "accepted_path": f"accepted/{scene_id}.webp",
                    "accepted_sha256": "0" * 64,
                    "review_path": f"evidence/reviews/{scene_id}.yaml",
                }
            )
        index_path.write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )

    def test_candidate_sheet_uses_declared_a_b_order(self):
        candidate_root = self.package / "source/candidates/scene-01/r01"
        self._image(candidate_root / "scene-01-r01-a.png", "#d8cfbf")
        self._image(candidate_root / "scene-01-r01-b.png", "#aeb9c5")
        output = build_candidate_sheet(self.root, "scene-01")
        self.assertTrue(output.is_file())
        self.assertEqual("scene-01-r01-candidates.webp", output.name)

    def test_full_sheet_requires_twelve_accepted_scenes(self):
        with self.assertRaisesRegex(ValueError, "12 accepted scenes required"):
            build_full_sheet(self.root)

    def test_first_pass_sheet_uses_scene_a_candidates_without_acceptance(self):
        for offset in range(1, 13):
            scene_id = f"scene-{offset:02d}"
            candidate = (
                self.package
                / f"source/candidates/{scene_id}/r01/{scene_id}-r01-a.png"
            )
            self._image(candidate, f"#{offset:02x}{offset:02x}{offset:02x}")

        output = build_first_pass_sheet(self.root)

        self.assertTrue(output.is_file())
        self.assertEqual("first-pass-continuity.webp", output.name)

    def test_act_approval_pins_contact_sheet_hash(self):
        self._accept_act_one_fixtures()
        build_act_sheet(self.root, 1)
        review_path = self.package / "evidence/reviews/act-1.yaml"
        review_path.write_text(
            yaml.safe_dump(
                {
                    "schema_version": 1,
                    "scope": "act-1",
                    "status": "review",
                    "checks": {
                        "accepted_scene_count": "pass",
                        "outfit_and_ornament": "pass",
                        "wetness_order": "pass",
                        "light_order": "pass",
                        "core_bytes_unchanged": "pass",
                    },
                    "findings": [],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        review = approve_act(self.root, 1, review_path)
        data = yaml.safe_load(review.read_text(encoding="utf-8"))
        self.assertRegex(data["contact_sheet_sha256"], r"^[0-9a-f]{64}$")

    def test_contact_sheet_script_supports_direct_cli_execution(self):
        result = subprocess.run(
            [
                sys.executable,
                "scripts/build_ame_no_sei_ni_shite_contact_sheet.py",
                "--help",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("--scope", result.stdout)


if __name__ == "__main__":
    unittest.main()
