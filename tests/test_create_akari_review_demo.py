from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.create_akari_review_demo import create_demo_batch


ROOT = Path(__file__).resolve().parents[1]


class CreateReviewDemoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data_root = Path(self.temp.name)
        references = self.data_root / "references"
        references.mkdir()
        for name in (
            "akari-v1.5-b3-body-balance.png",
            "akari-v1.4-g2-balanced-lines.png",
        ):
            Image.new("RGB", (16, 24), "#c7a58d").save(references / name)

    def test_demo_has_fifty_non_counting_entries_and_thumbnails(self):
        batch = create_demo_batch(self.data_root)
        manifest = json.loads(
            (batch / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual("demo", manifest["batchType"])
        self.assertEqual(50, len(manifest["entries"]))
        self.assertEqual(
            50,
            len(list((batch / "thumbs").glob("*.webp"))),
        )

    def test_direct_script_cli_creates_the_demo_batch(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/create_akari_review_demo.py"),
                "--data-root",
                str(self.data_root),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            f"{self.data_root.resolve() / 'batches/B000'}\n",
            result.stdout,
        )
