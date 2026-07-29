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
from scripts.create_akari_review_demo import (
    SystemdUserServiceGuard,
    create_demo_batch,
)


ROOT = Path(__file__).resolve().parents[1]


class FakeServiceGuard:
    def __init__(
        self,
        *,
        originally_active: bool = False,
        enter_error: Exception | None = None,
        reactivate_on_check: int | None = None,
    ):
        self.originally_active = originally_active
        self.enter_error = enter_error
        self.reactivate_on_check = reactivate_on_check
        self.events: list[str] = []
        self.checks = 0

    def __enter__(self):
        self.events.append(
            "state:active" if self.originally_active else "state:inactive"
        )
        if self.enter_error is not None:
            raise self.enter_error
        if self.originally_active:
            self.events.extend(("stop", "state:inactive"))
        return self

    def assert_inactive(self) -> None:
        self.checks += 1
        self.events.append("assert-inactive")
        if self.reactivate_on_check == self.checks:
            raise RuntimeError("gallery service became active during refresh")

    def __exit__(self, exc_type, exc, traceback):
        self.events.append("maintenance-finished")
        if self.originally_active:
            self.events.extend(("start", "state:active"))
        return False


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

    def _create(
        self,
        data_root: Path | None = None,
        *,
        guard: FakeServiceGuard | None = None,
    ) -> Path:
        return create_demo_batch(
            data_root or self.data_root,
            service_guard=guard or FakeServiceGuard(),
        )

    def test_demo_has_fifty_non_counting_entries_and_thumbnails(self):
        batch = self._create()
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
        fake_bin = self.data_root / "fake-bin"
        fake_bin.mkdir()
        fake_systemctl = fake_bin / "systemctl"
        fake_systemctl.write_text(
            "#!/bin/sh\n"
            "if [ \"$2\" = \"is-active\" ]; then\n"
            "  printf 'inactive\\n'\n"
            "  exit 3\n"
            "fi\n"
            "exit 0\n",
            encoding="utf-8",
        )
        fake_systemctl.chmod(0o755)
        environment = dict(os.environ)
        environment["PATH"] = f"{fake_bin}:{environment['PATH']}"
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
            env=environment,
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            f"{self.data_root.resolve() / 'batches/B000'}\n",
            result.stdout,
        )

    def test_unchanged_refresh_preserves_existing_media_and_reviews(self):
        batch = self._create()
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

        self._create()

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
        batch = self._create()
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
            self._create()

        self.assertEqual(before, self._snapshot_batch(batch))

    def test_successful_refresh_removes_stale_demo_media(self):
        batch = self._create()
        stale_image = batch / "images/stale.png"
        stale_thumb = batch / "thumbs/stale.webp"
        stale_image.write_bytes(b"stale image")
        stale_thumb.write_bytes(b"stale thumbnail")

        self._create()

        self.assertFalse(stale_image.exists())
        self.assertFalse(stale_thumb.exists())
        self.assertEqual(50, len(list((batch / "images").glob("*.png"))))
        self.assertEqual(50, len(list((batch / "thumbs").glob("*.webp"))))

    def test_failed_refresh_does_not_mutate_the_current_batch(self):
        batch = self._create()
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
            self._create()

        self.assertEqual(before, self._snapshot_batch(batch))

    def test_changed_manifest_entry_requires_reset_without_mutation(self):
        batch = self._create()
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
            self._create()

        self.assertEqual(before, self._snapshot_batch(batch))

    def test_changed_thumbnail_bytes_require_reset_without_mutation(self):
        batch = self._create()
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
            self._create()

        self.assertEqual(before, self._snapshot_batch(batch))

    def test_interrupted_swap_restores_deterministic_previous_batch(self):
        batch = self._create()
        self._review_first(batch, "survives interrupted swap")
        previous = batch.parent / ".B000.previous"
        os.replace(batch, previous)

        restored = self._create()

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
        batch = self._create()
        self._review_first(batch, "current review wins")
        previous = batch.parent / ".B000.previous"
        shutil.copytree(batch, previous)
        self._review_first(previous, "stale previous review")

        result = self._create()

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
        batch = self._create()
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
            result = self._create()

        previous = batch.parent / ".B000.previous"
        self.assertEqual(batch, result)
        self.assertTrue(previous.is_dir())
        self.assertFalse((batch / "images/stale.png").exists())
        recovered = self._create()
        self.assertEqual(batch, recovered)
        self.assertFalse(previous.exists())

    def test_systemd_guard_stops_active_service_and_restores_it(self):
        state = "active"
        commands: list[str] = []

        def runner(command, **_kwargs):
            nonlocal state
            operation = command[2]
            commands.append(operation)
            if operation == "is-active":
                return subprocess.CompletedProcess(
                    command,
                    0 if state == "active" else 3,
                    stdout=f"{state}\n",
                    stderr="",
                )
            if operation == "stop":
                state = "inactive"
            elif operation == "start":
                state = "active"
            return subprocess.CompletedProcess(
                command,
                0,
                stdout="",
                stderr="",
            )

        with SystemdUserServiceGuard(runner=runner) as guard:
            self.assertEqual("inactive", state)
            guard.assert_inactive()

        self.assertEqual("active", state)
        self.assertEqual(
            [
                "is-active",
                "stop",
                "is-active",
                "is-active",
                "start",
                "is-active",
            ],
            commands,
        )

    def test_systemd_guard_fails_closed_on_unknown_state(self):
        def runner(command, **_kwargs):
            return subprocess.CompletedProcess(
                command,
                3,
                stdout="activating\n",
                stderr="",
            )

        with self.assertRaisesRegex(
            RuntimeError,
            "unable to establish inactive gallery service",
        ):
            with SystemdUserServiceGuard(runner=runner):
                self.fail("unknown service state entered maintenance")

    def test_systemd_guard_rejects_inactive_text_with_unexpected_status(self):
        def runner(command, **_kwargs):
            return subprocess.CompletedProcess(
                command,
                1,
                stdout="inactive\n",
                stderr="systemctl query failed",
            )

        with self.assertRaisesRegex(
            RuntimeError,
            "unable to establish inactive gallery service",
        ):
            with SystemdUserServiceGuard(runner=runner):
                self.fail("failed service query entered maintenance")

    def test_systemd_guard_treats_an_uninstalled_unit_as_inactive(self):
        commands: list[str] = []

        def runner(command, **_kwargs):
            commands.append(command[2])
            return subprocess.CompletedProcess(
                command,
                4,
                stdout="inactive\n",
                stderr="Unit akari-review-gallery.service could not be found.",
            )

        with SystemdUserServiceGuard(runner=runner) as guard:
            guard.assert_inactive()

        self.assertEqual(["is-active", "is-active"], commands)

    def test_active_refresh_orders_stop_build_swap_then_restart(self):
        guard = FakeServiceGuard(originally_active=True)
        real_build = demo._build_staged_batch
        real_replace = demo._replace_batch

        def record_build(*args, **kwargs):
            guard.events.append("build")
            return real_build(*args, **kwargs)

        def record_replace(*args, **kwargs):
            guard.events.append("swap")
            return real_replace(*args, **kwargs)

        with (
            patch.object(
                demo,
                "_build_staged_batch",
                side_effect=record_build,
            ),
            patch.object(
                demo,
                "_replace_batch",
                side_effect=record_replace,
            ),
        ):
            self._create(guard=guard)

        self.assertLess(guard.events.index("stop"), guard.events.index("build"))
        self.assertLess(
            guard.events.index("assert-inactive"),
            guard.events.index("swap"),
        )
        self.assertLess(guard.events.index("swap"), guard.events.index("start"))

    def test_guard_entry_failure_leaves_existing_tree_unchanged(self):
        batch = self._create()
        before = self._snapshot_batch(batch)
        for message in (
            "failed to stop gallery service",
            "unable to establish inactive gallery service",
        ):
            with self.subTest(message=message):
                guard = FakeServiceGuard(enter_error=RuntimeError(message))
                with self.assertRaisesRegex(RuntimeError, message):
                    self._create(guard=guard)
                self.assertEqual(before, self._snapshot_batch(batch))

    def test_refresh_failure_restarts_only_a_previously_active_service(self):
        batch = self._create()
        before = self._snapshot_batch(batch)
        active_guard = FakeServiceGuard(originally_active=True)
        with (
            patch.object(
                demo,
                "_build_staged_batch",
                side_effect=RuntimeError("staged build failed"),
            ),
            self.assertRaisesRegex(RuntimeError, "staged build failed"),
        ):
            self._create(guard=active_guard)
        self.assertEqual(
            ["maintenance-finished", "start", "state:active"],
            active_guard.events[-3:],
        )
        self.assertEqual(before, self._snapshot_batch(batch))

        inactive_guard = FakeServiceGuard()
        with (
            patch.object(
                demo,
                "_build_staged_batch",
                side_effect=RuntimeError("staged build failed"),
            ),
            self.assertRaisesRegex(RuntimeError, "staged build failed"),
        ):
            self._create(guard=inactive_guard)
        self.assertNotIn("start", inactive_guard.events)

    def test_service_reactivation_before_swap_rejects_without_mutation(self):
        batch = self._create()
        (batch / "images/stale.png").write_bytes(b"stale")
        before = self._snapshot_batch(batch)
        guard = FakeServiceGuard(reactivate_on_check=2)

        with self.assertRaisesRegex(
            RuntimeError,
            "became active during refresh",
        ):
            self._create(guard=guard)

        self.assertEqual(2, guard.checks)
        self.assertEqual(before, self._snapshot_batch(batch))

    def test_symlinked_demo_paths_are_rejected_without_external_writes(self):
        baseline = self._create()
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
                    self._create(case_root)

                self.assertEqual(external_before, self._snapshot_batch(external))
