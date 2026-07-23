from contextlib import redirect_stdout
import importlib.util
from io import StringIO
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
PREPARE_SOURCES = ROOT / "scripts/prepare_sources.py"
SOURCE_ORIGINALS = ROOT / "source/originals"
sys.path.insert(0, str(ROOT / "scripts"))


def load_prepare_sources():
    spec = importlib.util.spec_from_file_location(
        "prepare_sources", PREPARE_SOURCES
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PrepareSourcesTest(unittest.TestCase):
    def setUp(self):
        self.prepare_sources = load_prepare_sources()

    def test_main_uses_tracked_originals_when_raw_root_images_are_absent(self):
        with tempfile.TemporaryDirectory() as directory:
            temp_root = Path(directory)
            temp_originals = temp_root / "source/originals"
            temp_manifests = temp_root / "source/manifests"
            shutil.copytree(SOURCE_ORIGINALS, temp_originals)

            with mock.patch.dict(os.environ, {}, clear=False):
                os.environ.pop("AKARI_SOURCE_IMAGE_DIR", None)
                with mock.patch.object(
                    self.prepare_sources, "ROOT", temp_root
                ), mock.patch.object(
                    self.prepare_sources, "ORIGINALS_DIR", temp_originals
                ), mock.patch.object(
                    self.prepare_sources, "MANIFEST_DIR", temp_manifests
                ), redirect_stdout(StringIO()):
                    result = self.prepare_sources.main()

            manifest = json.loads(
                (temp_manifests / "source-assets.json").read_text(encoding="utf-8")
            )
            self.assertEqual(0, result)
            self.assertEqual(10, manifest["asset_count"])
            self.assertEqual(10, len(manifest["assets"]))
            for asset in manifest["assets"]:
                self.assertTrue(asset["source_path"].startswith("source/originals/"))


if __name__ == "__main__":
    unittest.main()
