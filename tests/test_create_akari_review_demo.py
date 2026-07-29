from __future__ import annotations

import hashlib
import json
import os
import shutil
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

    def _review_first(self, batch: Path, note: str) -> None:
        reviews_path = batch / "reviews.json"
        reviews = json.loads(reviews_path.read_text(encoding="utf-8"))
        reviews["reviews"]["B000-001"] = {
            "status": "favorite",
            "reasons": [],
            "note": note,
            "revision": 1,
            "updatedAt": "2026-07-30T00:00:00.000Z",
        }
        reviews_path.write_text(
            json.dumps(reviews, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

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

    def test_changed_manifest_entry_requires_reset_without_mutation(self):
        batch = create_demo_batch(self.data_root)
        self._review_first(batch, "reviewed original semantics")
        manifest_path = batch / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["entries"][0]["references"][0]["role"] = (
            "changed identity authority semantics"
        )
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        before = self._snapshot_batch(batch)

        with self.assertRaisesRegex(ValueError, "reset B000 reviews"):
            create_demo_batch(self.data_root)

        self.assertEqual(before, self._snapshot_batch(batch))

    def test_changed_thumbnail_bytes_require_reset_without_mutation(self):
        batch = create_demo_batch(self.data_root)
        self._review_first(batch, "reviewed original thumbnail")
        before = self._snapshot_batch(batch)

        def build_changed_thumbnail(source: Path, output: Path) -> Path:
            with Image.open(source) as image:
                converted = image.convert("RGB")
                converted.thumbnail((512, 512), Image.Resampling.LANCZOS)
                converted.save(output, "WEBP", quality=40, method=6)
            return output

        with (
            patch.object(
                demo,
                "build_thumbnail",
                side_effect=build_changed_thumbnail,
            ),
            self.assertRaisesRegex(ValueError, "reset B000 reviews"),
        ):
            create_demo_batch(self.data_root)

        self.assertEqual(before, self._snapshot_batch(batch))

    def test_interrupted_swap_restores_deterministic_previous_batch(self):
        batch = create_demo_batch(self.data_root)
        self._review_first(batch, "survives interrupted swap")
        previous = batch.parent / ".B000.previous"
        os.replace(batch, previous)

        restored = create_demo_batch(self.data_root)

        self.assertEqual(batch, restored)
        self.assertFalse(previous.exists())
        reviews = json.loads(
            (restored / "reviews.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            "survives interrupted swap",
            reviews["reviews"]["B000-001"]["note"],
        )

    def test_valid_current_batch_wins_and_cleans_leftover_previous(self):
        batch = create_demo_batch(self.data_root)
        self._review_first(batch, "current review wins")
        previous = batch.parent / ".B000.previous"
        shutil.copytree(batch, previous)
        self._review_first(previous, "stale previous review")

        result = create_demo_batch(self.data_root)

        self.assertEqual(batch, result)
        self.assertFalse(previous.exists())
        reviews = json.loads(
            (result / "reviews.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            "current review wins",
            reviews["reviews"]["B000-001"]["note"],
        )

    def test_post_activation_cleanup_failure_leaves_recoverable_previous(self):
        batch = create_demo_batch(self.data_root)
        self._review_first(batch, "preserved through cleanup failure")
        (batch / "images/stale.png").write_bytes(b"stale")
        real_rmtree = demo.shutil.rmtree

        def fail_previous_cleanup(path: Path, *args, **kwargs) -> None:
            if Path(path).name.endswith(".previous"):
                raise OSError("simulated previous cleanup failure")
            real_rmtree(path, *args, **kwargs)

        with patch.object(
            demo.shutil,
            "rmtree",
            side_effect=fail_previous_cleanup,
        ):
            result = create_demo_batch(self.data_root)

        previous = batch.parent / ".B000.previous"
        self.assertEqual(batch, result)
        self.assertTrue(previous.is_dir())
        self.assertFalse((batch / "images/stale.png").exists())
        recovered = create_demo_batch(self.data_root)
        self.assertEqual(batch, recovered)
        self.assertFalse(previous.exists())

    def test_symlinked_demo_paths_are_rejected_without_external_writes(self):
        baseline = create_demo_batch(self.data_root)
        cases_root = self.data_root / "symlink-cases"
        cases_root.mkdir()
        for label in (
            "batches",
            "B000",
            "images",
            "thumbs",
            "manifest",
            "reviews",
            "backup",
            "media",
        ):
            with self.subTest(label=label):
                case_root = cases_root / label
                shutil.copytree(self.data_root / "references", case_root / "references")
                external = cases_root / f"{label}-external"
                external.mkdir()
                sentinel = external / "sentinel"
                sentinel.write_bytes(b"outside must not change")
                if label == "batches":
                    (case_root / "batches").symlink_to(
                        external,
                        target_is_directory=True,
                    )
                elif label == "B000":
                    shutil.copytree(baseline, external / "B000")
                    (case_root / "batches").mkdir()
                    (case_root / "batches/B000").symlink_to(
                        external / "B000",
                        target_is_directory=True,
                    )
                else:
                    shutil.copytree(baseline, case_root / "batches/B000")
                    case_batch = case_root / "batches/B000"
                    targets = {
                        "images": case_batch / "images",
                        "thumbs": case_batch / "thumbs",
                        "manifest": case_batch / "manifest.json",
                        "reviews": case_batch / "reviews.json",
                        "backup": case_batch / "reviews.json.bak",
                        "media": case_batch / "images/demo-001.png",
                    }
                    target = targets[label]
                    if label == "backup" and not target.exists():
                        target.write_bytes(b"local backup")
                    if target.is_dir():
                        shutil.rmtree(target)
                        target.symlink_to(external, target_is_directory=True)
                    else:
                        target.unlink()
                        outside_file = external / target.name
                        outside_file.write_bytes(b"outside file")
                        target.symlink_to(outside_file)
                external_before = self._snapshot_batch(external)

                with self.assertRaisesRegex(ValueError, "symlink"):
                    create_demo_batch(case_root)

                self.assertEqual(external_before, self._snapshot_batch(external))
