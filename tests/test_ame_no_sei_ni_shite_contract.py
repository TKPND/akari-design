from __future__ import annotations

import unittest
import tempfile
from pathlib import Path
from shutil import copytree, ignore_patterns

import yaml
from PIL import Image

from scripts.akari_v1_2_ame_no_sei_ni_shite import (
    ValidationError,
    load_contract,
    promote_scene,
    render_scene_prompt,
    sha256_file,
)


ROOT = Path(__file__).resolve().parents[1]


class AmeNoSeiNiShiteContractTest(unittest.TestCase):
    def test_book_contract(self):
        contract = load_contract(ROOT)
        self.assertEqual(
            "akari-v1.2-ame-no-sei-ni-shite",
            contract["book"]["book_id"],
        )
        self.assertEqual(18, contract["book"]["page_count"])
        self.assertEqual(
            {"width": 1536, "height": 1024},
            contract["book"]["minimum_image"],
        )
        self.assertEqual(
            list(range(1, 19)),
            [page["page"] for page in contract["book"]["pages"]],
        )

    def test_scene_order_and_dialogue_limit(self):
        scenes = load_contract(ROOT)["scenes"]
        self.assertEqual(
            [f"scene-{number:02d}" for number in range(1, 13)],
            [scene["id"] for scene in scenes],
        )
        self.assertTrue(all(len(scene["dialogue"]) <= 1 for scene in scenes))

    def test_planned_scene_paths_are_canonical(self):
        for scene in load_contract(ROOT)["scenes"]:
            self.assertEqual(
                [
                    f"source/candidates/{scene['id']}/r01/"
                    f"{scene['id']}-r01-a.png",
                    f"source/candidates/{scene['id']}/r01/"
                    f"{scene['id']}-r01-b.png",
                ],
                [item["path"] for item in scene["candidates"]],
            )

    def test_accepted_scene_paths_are_webp(self):
        for scene in load_contract(ROOT)["scenes"]:
            self.assertEqual(
                f"accepted/{scene['id']}.webp",
                scene["accepted_path"],
            )

    def test_core_reference_hashes_are_pinned(self):
        contract = load_contract(ROOT)
        for reference in contract["continuity"]["core_references"]:
            self.assertEqual(
                reference["sha256"],
                sha256_file(ROOT / reference["path"]),
            )

    def test_scene_prompt_contains_global_pov_and_production_bans(self):
        prompt = render_scene_prompt(load_contract(ROOT), "scene-12").lower()
        for phrase in (
            "25-year-old adult akari",
            "physically possible first-person point of view",
            "no viewer face, body, hand, reflection, or shadow",
            "only the edge of the viewer's sleeve",
            "no readable text, logo, watermark, collage, or grid",
        ):
            self.assertIn(phrase, prompt)


class AmeNoSeiNiShitePromotionTest(unittest.TestCase):
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
        candidate = (
            self.package
            / "source/candidates/scene-01/r01/scene-01-r01-a.png"
        )
        candidate.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (1536, 1024), "#d8cfbf").save(candidate)
        self.review_path = self.package / "evidence/reviews/scene-01.yaml"
        self.review_path.parent.mkdir(parents=True)
        self.review_path.write_text(
            yaml.safe_dump(
                {
                    "schema_version": 1,
                    "scene_id": "scene-01",
                    "revision": "r01",
                    "status": "rejected",
                    "selected_variant": "a",
                    "findings": [
                        {
                            "severity": "major",
                            "category": "pov",
                            "note": "not accepted",
                        }
                    ],
                    "selection_reason": "Rejected fixture.",
                    "reference_roles_confirmed": [],
                },
                allow_unicode=True,
                sort_keys=False,
            ),
            encoding="utf-8",
        )

    def test_promotion_requires_accepted_review(self):
        with self.assertRaisesRegex(
            ValidationError,
            "review status must be accepted",
        ):
            promote_scene(
                self.root,
                "scene-01",
                "r01",
                "a",
                self.review_path,
            )

    def test_promotion_encodes_accepted_image_as_webp(self):
        review = yaml.safe_load(self.review_path.read_text(encoding="utf-8"))
        review.update(
            {
                "status": "accepted",
                "findings": [],
                "selection_reason": "Accepted fixture.",
            }
        )
        self.review_path.write_text(
            yaml.safe_dump(review, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )

        destination = promote_scene(
            self.root,
            "scene-01",
            "r01",
            "a",
            self.review_path,
        )

        self.assertEqual("scene-01.webp", destination.name)
        with Image.open(destination) as image:
            self.assertEqual("WEBP", image.format)
            self.assertEqual((1536, 1024), image.size)
        scene = load_contract(self.root)["scenes"][0]
        self.assertEqual("accepted/scene-01.webp", scene["accepted_path"])
        self.assertEqual(sha256_file(destination), scene["accepted_sha256"])


if __name__ == "__main__":
    unittest.main()
