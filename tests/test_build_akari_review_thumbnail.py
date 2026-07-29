from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.build_akari_review_thumbnail import (
    PNG_SIGNATURE,
    build_thumbnail,
    inspect_png,
)


class ReviewThumbnailTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_thumbnail_preserves_ratio_and_limits_long_edge(self):
        source = self.root / "source.png"
        Image.new("RGB", (1024, 1536), "#d9b6a0").save(source)

        output = build_thumbnail(source, self.root / "thumb.webp")

        with Image.open(output) as image:
            self.assertEqual((341, 512), image.size)
            self.assertEqual("WEBP", image.format)

    def test_inspect_png_rejects_non_png_signature(self):
        source = self.root / "fake.png"
        source.write_bytes(b"not a png")

        with self.assertRaisesRegex(ValueError, "invalid PNG signature"):
            inspect_png(source)

    def test_inspect_png_rejects_truncated_png(self):
        source = self.root / "truncated.png"
        source.write_bytes(PNG_SIGNATURE + b"broken")

        with self.assertRaises((OSError, SyntaxError, ValueError)):
            inspect_png(source)

    def test_rgba_source_builds_rgb_webp_without_source_change(self):
        source = self.root / "alpha.png"
        Image.new("RGBA", (40, 60), (220, 180, 160, 128)).save(source)
        before = source.read_bytes()

        output = build_thumbnail(source, self.root / "alpha.webp")

        self.assertEqual(before, source.read_bytes())
        with Image.open(output) as image:
            self.assertEqual("RGB", image.mode)
            self.assertEqual("WEBP", image.format)
