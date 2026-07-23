import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COVER = ROOT / "source/originals/situation-daybook-lakeside-bench-cover.webp"
DAYBOOK_MANIFEST_DIR = ROOT / "source/manifests/daybook"
SOURCE_ASSETS = DAYBOOK_MANIFEST_DIR / "source-assets.json"
ASSET_MANIFEST = DAYBOOK_MANIFEST_DIR / "asset-manifest.json"
PAGE_MANIFEST = DAYBOOK_MANIFEST_DIR / "page-manifest.json"
GENERATION_REQUESTS = DAYBOOK_MANIFEST_DIR / "generation-requests.json"
DAYBOOK_MANIFESTS = [
    SOURCE_ASSETS,
    ASSET_MANIFEST,
    PAGE_MANIFEST,
    GENERATION_REQUESTS,
]
JAPANESE_TEXT = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")


def load_json(path):
    with path.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


def identify(path):
    result = subprocess.run(
        ["identify", "-format", "%w %h %[colorspace]", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    width, height, colorspace = result.stdout.strip().split()
    return int(width), int(height), colorspace


class DaybookContractTest(unittest.TestCase):
    def test_cover_anchor_exists_with_expected_dimensions(self):
        self.assertTrue(COVER.is_file(), f"missing cover image: {COVER}")
        self.assertEqual((1280, 720, "sRGB"), identify(COVER))

    def test_daybook_manifests_exist(self):
        for manifest_path in DAYBOOK_MANIFESTS:
            with self.subTest(manifest=manifest_path.name):
                self.assertTrue(
                    manifest_path.is_file(),
                    f"missing daybook manifest: {manifest_path}",
                )

    def test_daybook_page_contract(self):
        page_manifest = load_json(PAGE_MANIFEST)

        self.assertEqual("akari-v1.1-situation-daybook", page_manifest["document_id"])
        self.assertEqual(10, page_manifest["page_count"])

        pages = page_manifest["pages"]
        self.assertEqual(list(range(1, 11)), [page["page"] for page in pages])
        self.assertEqual(
            [
                "Lakeside Bench",
                "Footbridge Breeze",
                "Convenience Walk",
                "Dock Edge",
                "Park Steps",
                "Window Seat",
                "Rain-Cooled Street",
                "Station After Sun",
                "Vending Machine Night",
                "Golden Hour Return",
            ],
            [page["title"] for page in pages],
        )

        for page in pages:
            with self.subTest(page=page["page"]):
                self.assertIsNone(JAPANESE_TEXT.search(page["title"]))
                self.assertEqual(1, len(page["source_inputs"]))
                self.assertEqual(
                    ["image", "note-list", "note-list"],
                    [block["type"] for block in page["blocks"]],
                )
                self.assertEqual(1, len(page["atmosphere_notes"]))
                self.assertEqual(3, len(page["generation_notes"]))

    def test_daybook_assets_are_accepted_and_16x9(self):
        asset_manifest = load_json(ASSET_MANIFEST)
        source_assets = load_json(SOURCE_ASSETS)
        source_path_by_id = {
            asset["id"]: asset["source_path"] for asset in source_assets["assets"]
        }

        assets = asset_manifest["assets"]
        self.assertEqual(10, len(assets))

        for asset in assets:
            with self.subTest(asset=asset["id"]):
                self.assertEqual("accepted", asset["status"])
                self.assertTrue(asset["used_in_daybook_pdf"])

                image_path = source_path_by_id.get(asset["id"]) or asset.get(
                    "candidate_path"
                )
                self.assertIsNotNone(image_path)
                resolved_path = ROOT / image_path
                self.assertTrue(
                    resolved_path.is_file(),
                    f"missing daybook image for {asset['id']}: {resolved_path}",
                )

                width, height, colorspace = identify(resolved_path)
                self.assertEqual(width * 9, height * 16)
                self.assertIn(colorspace, {"sRGB", "RGB"})
                self.assertNotIn("readable text", asset["layout_check"].lower())

    def test_generation_prompts_ban_text_in_image(self):
        generation_requests = load_json(GENERATION_REQUESTS)

        requests = generation_requests["requests"]
        self.assertEqual(9, len(requests))

        for request in requests:
            with self.subTest(request=request["id"]):
                prompt = request["prompt"].lower()
                acceptance = request["acceptance"].lower()
                self.assertIn("no readable text", prompt)
                self.assertIn("no logos", prompt)
                self.assertIn("no watermark", prompt)
                self.assertIn("text-in-image", acceptance)


if __name__ == "__main__":
    unittest.main()
