from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from scripts import create_akari_review_demo as demo
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

    def _snapshot_batch(self, batch: Path) -> dict[str, str]:
        return {
            path.relative_to(batch).as_posix(): hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
            for path in batch.rglob("*")
            if path.is_file()
        }

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

    def test_unchanged_refresh_preserves_existing_media_and_reviews(self):
        batch = create_demo_batch(self.data_root)
        reviews_path = batch / "reviews.json"
        reviews = json.loads(reviews_path.read_text(encoding="utf-8"))
        reviews["reviews"]["B000-001"] = {
            "status": "favorite",
            "reasons": [],
            "note": "preserve this review",
            "revision": 1,
            "updatedAt": "2026-07-30T00:00:00.000Z",
        }
        reviews_path.write_text(
            json.dumps(reviews, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        watched = (
            batch / "manifest.json",
            batch / "images/demo-001.png",
            batch / "thumbs/demo-001.webp",
            reviews_path,
        )
        fixed_time = 1_000_000_000
        for path in watched:
            os.utime(path, ns=(fixed_time, fixed_time))

        create_demo_batch(self.data_root)

        self.assertTrue(
            all(path.stat().st_mtime_ns == fixed_time for path in watched)
        )
        self.assertEqual(
            "preserve this review",
            json.loads(reviews_path.read_text(encoding="utf-8"))["reviews"][
                "B000-001"
            ]["note"],
        )

    def test_changed_demo_content_requires_reset_without_mutation(self):
        batch = create_demo_batch(self.data_root)
        reviews_path = batch / "reviews.json"
        reviews = json.loads(reviews_path.read_text(encoding="utf-8"))
        reviews["reviews"]["B000-001"]["status"] = "keep"
        reviews["reviews"]["B000-001"]["revision"] = 1
        reviews_path.write_text(
            json.dumps(reviews, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        before = self._snapshot_batch(batch)
        changed_colors = ("#101010", *demo.COLORS[1:])

        with (
            patch.object(demo, "COLORS", changed_colors),
            self.assertRaisesRegex(ValueError, "reset B000 reviews"),
        ):
            create_demo_batch(self.data_root)

        self.assertEqual(before, self._snapshot_batch(batch))

    def test_successful_refresh_removes_stale_demo_media(self):
        batch = create_demo_batch(self.data_root)
        stale_image = batch / "images/stale.png"
        stale_thumb = batch / "thumbs/stale.webp"
        stale_image.write_bytes(b"stale image")
        stale_thumb.write_bytes(b"stale thumbnail")

        create_demo_batch(self.data_root)

        self.assertFalse(stale_image.exists())
        self.assertFalse(stale_thumb.exists())
        self.assertEqual(50, len(list((batch / "images").glob("*.png"))))
        self.assertEqual(50, len(list((batch / "thumbs").glob("*.webp"))))

    def test_failed_refresh_does_not_mutate_the_current_batch(self):
        batch = create_demo_batch(self.data_root)
        before = self._snapshot_batch(batch)
        changed_colors = ("#202020", *demo.COLORS[1:])
        real_build_thumbnail = demo.build_thumbnail

        def fail_on_second_thumbnail(source: Path, output: Path) -> Path:
            if source.name == "demo-002.png":
                raise RuntimeError("simulated thumbnail failure")
            return real_build_thumbnail(source, output)

        with (
            patch.object(demo, "COLORS", changed_colors),
            patch.object(
                demo,
                "build_thumbnail",
                side_effect=fail_on_second_thumbnail,
            ),
            self.assertRaisesRegex(RuntimeError, "simulated thumbnail failure"),
        ):
            create_demo_batch(self.data_root)

        self.assertEqual(before, self._snapshot_batch(batch))
