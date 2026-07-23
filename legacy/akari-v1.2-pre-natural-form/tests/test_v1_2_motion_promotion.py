import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

import scripts.promote_v1_2_motion_candidate as promotion_module
from scripts.promote_v1_2_motion_candidate import (
    promote_review,
    validate_review_artifact_path,
)
from scripts.v1_2_motion_common import CANONICAL_SLOTS, sha256_file


GATES = {
    "identity",
    "age",
    "anatomy_pose",
    "body_proportion",
    "outfit",
    "footwear",
    "ornament_side",
    "framing",
    "artifacts_quality",
    "motion_naturalness",
}
def handoff_for(root: Path) -> dict:
    turnaround_dir = root / "turnaround"
    turnaround_dir.mkdir(parents=True, exist_ok=True)
    accepted_angles = []
    inputs = []
    for slot in CANONICAL_SLOTS:
        asset = turnaround_dir / f"{slot}.webp"
        asset.write_bytes(f"asset:{slot}\n".encode())
        digest = sha256_file(asset)
        accepted_angles.append(
            {"slot": slot, "accepted_path": asset.as_posix(), "sha256": digest}
        )
        inputs.append(
            {"slot": slot, "accepted_path": asset.as_posix(), "sha256": digest}
        )

    manifest = root / "accepted-angles.json"
    manifest.write_text(
        json.dumps({"accepted_angles": accepted_angles}, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest_hash = sha256_file(manifest)
    final_review = root / "final-review.json"
    final_review.write_text(
        json.dumps(
            {
                "decision": "accepted",
                "user_decision": "approved",
                "source_manifest": manifest.as_posix(),
                "source_manifest_sha256": manifest_hash,
                "accepted_slots": list(CANONICAL_SLOTS),
                "gate_summary": {"quality": "pass"},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "source_turnaround_manifest": manifest.as_posix(),
        "source_turnaround_manifest_sha256": manifest_hash,
        "source_final_review": final_review.as_posix(),
        "turnaround_inputs": inputs,
        "motion_slots": [
            {
                "slug": motion,
                "candidate_count": 3,
                "deliverable_count": 1,
                "required_turnaround_slots": list(CANONICAL_SLOTS),
            }
            for motion in ("walking", "seated", "turning")
        ],
    }


def request_manifest_for(
    root: Path, motion: str = "walking"
) -> tuple[dict, list[str]]:
    pack_hash = handoff_for(root)["source_turnaround_manifest_sha256"]
    paths = []
    requests = []
    for number in range(1, 4):
        path = root / f"{motion}-c{number}.png"
        Image.new("RGB", (1024, 1536), "white").save(path)
        paths.append(path.as_posix())
        requests.append(
            {
                "id": f"{motion}-r1-c{number}",
                "batch_id": f"{motion}-r1",
                "motion": motion,
                "revision": 1,
                "candidate_number": number,
                "target_path": path.as_posix(),
                "source_pack_sha256": pack_hash,
            }
        )
    return {
        "active_batches": {motion: f"{motion}-r1"},
        "requests": requests,
    }, paths


def review_for(requests: dict, paths: list[str]) -> dict:
    decisions = ("accept", "hold", "reject")
    motion, batch_id = next(iter(requests["active_batches"].items()))
    return {
        "review_id": f"{motion}-r1-review",
        "review_path": f"evidence/v1-2-motion/reviews/{motion}-r1-review.json",
        "motion": motion,
        "batch_id": batch_id,
        "user_decision": "approved",
        "candidates": [
            {
                "request_id": request["id"],
                "candidate_path": path,
                "decision": decision,
                "gates": {gate: "pass" for gate in GATES},
                "observations": {
                    gate: f"{gate} checked" for gate in GATES
                },
                "rejection_reason": (
                    "malformed hand" if decision == "reject" else ""
                ),
            }
            for request, path, decision in zip(
                requests["requests"], paths, decisions
            )
        ],
    }


def empty_selection() -> dict:
    return {
        "schema_version": 1,
        "collection_id": "akari-v1.2-representative-motion-poses",
        "accepted_motions": [],
    }


def accepted_record_for(motion: str) -> dict:
    order = {"walking": 1, "seated": 2, "turning": 3}[motion]
    digest = str(order) * 64
    return {
        "motion": motion,
        "motion_order": order,
        "finished_path": f"source/finished/v1-2-motion/{motion}.webp",
        "source_candidate_path": f"source/generated/v1-2-motion/{motion}.png",
        "request_id": f"{motion}-r1-c1",
        "batch_id": f"{motion}-r1",
        "revision": 1,
        "candidate_number": 1,
        "review_id": f"{motion}-r1-review",
        "review_path": f"evidence/v1-2-motion/reviews/{motion}-r1-review.json",
        "source_pack_sha256": digest,
        "source_sha256": digest,
        "finished_sha256": digest,
    }


class AkariV12MotionPromotionTest(unittest.TestCase):
    def test_transaction_rolls_back_webp_when_manifest_replace_fails(self):
        self.assertTrue(
            hasattr(promotion_module, "commit_promotion_transaction"),
            "transactional promotion installer is missing",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = root / "source/finished/v1-2-motion/walking.webp"
            accepted_path = root / "accepted-selection.json"
            output.parent.mkdir(parents=True)
            Image.new("RGB", (1024, 1536), "blue").save(output, "WEBP")
            accepted_path.write_text('{"state":"old"}\n', encoding="utf-8")
            old_output = output.read_bytes()
            old_manifest = accepted_path.read_bytes()

            staged = root / "staged.webp"
            Image.new("RGB", (1024, 1536), "green").save(staged, "WEBP")
            real_replace = os.replace
            failed = False

            def fail_manifest_once(source, destination):
                nonlocal failed
                if Path(destination) == accepted_path and not failed:
                    failed = True
                    raise OSError("injected manifest replace failure")
                real_replace(source, destination)

            with patch.object(
                promotion_module.os, "replace", side_effect=fail_manifest_once
            ):
                with self.assertRaisesRegex(
                    OSError, "injected manifest replace failure"
                ):
                    promotion_module.commit_promotion_transaction(
                        staged,
                        output,
                        accepted_path,
                        {"state": "new"},
                    )

            self.assertEqual(old_output, output.read_bytes())
            self.assertEqual(old_manifest, accepted_path.read_bytes())
            self.assertFalse(
                promotion_module.promotion_journal_path(accepted_path).exists()
            )

    def test_recovers_interrupted_promotion_transaction(self):
        self.assertTrue(
            hasattr(promotion_module, "commit_promotion_transaction"),
            "transactional promotion installer is missing",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = root / "source/finished/v1-2-motion/walking.webp"
            accepted_path = root / "accepted-selection.json"
            output.parent.mkdir(parents=True)
            Image.new("RGB", (1024, 1536), "blue").save(output, "WEBP")
            accepted_path.write_text('{"state":"old"}\n', encoding="utf-8")
            old_output = output.read_bytes()
            old_manifest = accepted_path.read_bytes()

            staged = root / "staged.webp"
            Image.new("RGB", (1024, 1536), "green").save(staged, "WEBP")
            real_replace = os.replace

            def interrupt_manifest_replace(source, destination):
                if Path(destination) == accepted_path:
                    raise SystemExit("simulated process stop")
                real_replace(source, destination)

            with patch.object(
                promotion_module.os,
                "replace",
                side_effect=interrupt_manifest_replace,
            ):
                with self.assertRaisesRegex(SystemExit, "simulated process stop"):
                    promotion_module.commit_promotion_transaction(
                        staged,
                        output,
                        accepted_path,
                        {"state": "new"},
                    )

            journal = promotion_module.promotion_journal_path(accepted_path)
            self.assertTrue(journal.is_file())
            self.assertNotEqual(old_output, output.read_bytes())

            promotion_module.recover_promotion_transaction(accepted_path)

            self.assertEqual(old_output, output.read_bytes())
            self.assertEqual(old_manifest, accepted_path.read_bytes())
            self.assertFalse(journal.exists())

    def test_recovery_converges_after_interruption_between_restores(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = root / "finished.webp"
            accepted_path = root / "accepted-selection.json"
            Image.new("RGB", (1024, 1536), "blue").save(output, "WEBP")
            accepted_path.write_text('{"state":"old"}\n', encoding="utf-8")
            old_output = output.read_bytes()
            old_manifest = accepted_path.read_bytes()
            staged = root / "staged.webp"
            Image.new("RGB", (1024, 1536), "green").save(staged, "WEBP")
            real_replace = os.replace

            def stop_commit(source, destination):
                if Path(destination) == accepted_path:
                    raise SystemExit("stop during commit")
                real_replace(source, destination)

            with patch.object(
                promotion_module.os, "replace", side_effect=stop_commit
            ):
                with self.assertRaises(SystemExit):
                    promotion_module.commit_promotion_transaction(
                        staged, output, accepted_path, {"state": "new"}
                    )

            def stop_before_manifest_restore(source, destination):
                if Path(destination) == accepted_path:
                    raise SystemExit("stop during recovery")
                real_replace(source, destination)

            with patch.object(
                promotion_module.os,
                "replace",
                side_effect=stop_before_manifest_restore,
            ):
                with self.assertRaisesRegex(SystemExit, "stop during recovery"):
                    promotion_module.recover_promotion_transaction(accepted_path)

            promotion_module.recover_promotion_transaction(accepted_path)
            self.assertEqual(old_output, output.read_bytes())
            self.assertEqual(old_manifest, accepted_path.read_bytes())
            self.assertFalse(
                promotion_module.promotion_journal_path(accepted_path).exists()
            )

    def test_recovery_converges_after_cleanup_interruption(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = root / "finished.webp"
            accepted_path = root / "accepted-selection.json"
            Image.new("RGB", (1024, 1536), "blue").save(output, "WEBP")
            accepted_path.write_text('{"state":"old"}\n', encoding="utf-8")
            old_output = output.read_bytes()
            old_manifest = accepted_path.read_bytes()
            staged = root / "staged.webp"
            Image.new("RGB", (1024, 1536), "green").save(staged, "WEBP")
            real_replace = os.replace

            def stop_commit(source, destination):
                if Path(destination) == accepted_path:
                    raise SystemExit("stop during commit")
                real_replace(source, destination)

            with patch.object(
                promotion_module.os, "replace", side_effect=stop_commit
            ):
                with self.assertRaises(SystemExit):
                    promotion_module.commit_promotion_transaction(
                        staged, output, accepted_path, {"state": "new"}
                    )

            journal_path = promotion_module.promotion_journal_path(accepted_path)
            journal = promotion_module.load_json(journal_path)
            interrupt_path = Path(journal["accepted_backup"])
            real_unlink = Path.unlink

            def stop_cleanup(path, *args, **kwargs):
                if path == interrupt_path:
                    raise SystemExit("stop during cleanup")
                return real_unlink(path, *args, **kwargs)

            with patch.object(Path, "unlink", stop_cleanup):
                with self.assertRaisesRegex(SystemExit, "stop during cleanup"):
                    promotion_module.recover_promotion_transaction(accepted_path)

            promotion_module.recover_promotion_transaction(accepted_path)
            self.assertEqual(old_output, output.read_bytes())
            self.assertEqual(old_manifest, accepted_path.read_bytes())
            self.assertFalse(journal_path.exists())

    def test_transaction_cleans_prepared_files_when_backup_creation_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = root / "finished.webp"
            accepted_path = root / "accepted-selection.json"
            Image.new("RGB", (1024, 1536), "blue").save(output, "WEBP")
            accepted_path.write_text('{"state":"old"}\n', encoding="utf-8")
            staged = root / "staged.webp"
            Image.new("RGB", (1024, 1536), "green").save(staged, "WEBP")
            real_backup = promotion_module._backup_file
            calls = 0

            def fail_second_backup(path, label):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected backup failure")
                return real_backup(path, label)

            with patch.object(
                promotion_module,
                "_backup_file",
                side_effect=fail_second_backup,
            ):
                with self.assertRaisesRegex(OSError, "injected backup failure"):
                    promotion_module.commit_promotion_transaction(
                        staged, output, accepted_path, {"state": "new"}
                    )

            self.assertFalse(staged.exists())
            self.assertFalse(
                promotion_module.promotion_journal_path(accepted_path).exists()
            )
            self.assertEqual([], list(root.glob(".*-previous-*.backup")))
            self.assertEqual([], list(root.glob(".*-promotion-*.tmp")))

    def test_backup_helper_cleans_partial_file_on_copy_failure(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.webp"
            source.write_bytes(b"source bytes")

            def partial_copy(_source, destination):
                destination.write(b"partial")
                raise OSError("injected copy failure")

            with patch.object(
                promotion_module.shutil,
                "copyfileobj",
                side_effect=partial_copy,
            ):
                with self.assertRaisesRegex(OSError, "injected copy failure"):
                    promotion_module._backup_file(source, "previous")

            self.assertEqual([], list(root.glob(".*-previous-*.backup")))

    def test_transaction_persists_resources_before_prepared_journal(self):
        self.assertTrue(
            hasattr(promotion_module, "_fsync_file"),
            "staged WebP file fsync helper is missing",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            stage_dir = root / "stage"
            output_dir = root / "finished"
            manifest_dir = root / "manifests"
            for directory in (stage_dir, output_dir, manifest_dir):
                directory.mkdir()
            staged = stage_dir / "staged.webp"
            output = output_dir / "walking.webp"
            accepted_path = manifest_dir / "accepted-selection.json"
            Image.new("RGB", (1024, 1536), "green").save(staged, "WEBP")
            Image.new("RGB", (1024, 1536), "blue").save(output, "WEBP")
            accepted_path.write_text('{"state":"old"}\n', encoding="utf-8")

            events = []
            real_fsync_file = promotion_module._fsync_file
            real_fsync_directory = promotion_module.fsync_directory
            real_dump_json = promotion_module.dump_json
            real_replace = promotion_module.os.replace
            journal_path = promotion_module.promotion_journal_path(accepted_path)

            def record_file(path):
                events.append(("file", Path(path)))
                return real_fsync_file(path)

            def record_directory(path):
                events.append(("dir", Path(path)))
                return real_fsync_directory(path)

            def record_json(path, data):
                if Path(path) == journal_path and data.get("state") == "prepared":
                    events.append(("journal", "prepared"))
                return real_dump_json(path, data)

            def record_replace(source, destination):
                if Path(destination) == output:
                    events.append(("replace", "output"))
                return real_replace(source, destination)

            with (
                patch.object(
                    promotion_module, "_fsync_file", side_effect=record_file
                ),
                patch.object(
                    promotion_module,
                    "fsync_directory",
                    side_effect=record_directory,
                ),
                patch.object(
                    promotion_module, "dump_json", side_effect=record_json
                ),
                patch.object(
                    promotion_module.os, "replace", side_effect=record_replace
                ),
            ):
                promotion_module.commit_promotion_transaction(
                    staged, output, accepted_path, {"state": "new"}
                )

            prepared = events.index(("journal", "prepared"))
            replaced = events.index(("replace", "output"))
            self.assertLess(events.index(("file", staged)), prepared)
            for directory in (stage_dir, output_dir, manifest_dir):
                before = [
                    index
                    for index, event in enumerate(events[:prepared])
                    if event == ("dir", directory)
                ]
                self.assertTrue(before, f"missing durable directory: {directory}")
                after = [
                    index
                    for index, event in enumerate(events[replaced + 1 :], replaced + 1)
                    if event == ("dir", directory)
                ]
                self.assertTrue(after, f"missing cleanup directory fsync: {directory}")
            self.assertLess(prepared, replaced)

    def test_promotes_only_the_single_accepted_active_candidate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, paths = request_manifest_for(root)
            review = review_for(requests, paths)
            result = promote_review(
                review, requests, handoff_for(root), empty_selection(), root
            )
            record = result["accepted_motions"][0]
            output = root / record["finished_path"]
            self.assertEqual("walking", record["motion"])
            self.assertTrue(output.is_file())
            self.assertEqual(sha256_file(output), record["finished_sha256"])
            self.assertEqual(
                sha256_file(Path(paths[0])), record["source_sha256"]
            )

    def test_revalidates_phase_1_handoff_before_promotion(self):
        mutations = {
            "manifest": lambda handoff: Path(
                handoff["source_turnaround_manifest"]
            ).write_text("{}\n", encoding="utf-8"),
            "asset": lambda handoff: Path(
                handoff["turnaround_inputs"][0]["accepted_path"]
            ).write_bytes(b"drifted\n"),
            "final review": lambda handoff: Path(
                handoff["source_final_review"]
            ).write_text(
                json.dumps({"decision": "rejected"}) + "\n",
                encoding="utf-8",
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                requests, paths = request_manifest_for(root)
                handoff = handoff_for(root)
                mutate(handoff)
                output = root / "source/finished/v1-2-motion/walking.webp"
                with self.assertRaisesRegex(
                    ValueError,
                    "manifest hash drift|asset hash drift|final Phase 1 review",
                ):
                    promote_review(
                        review_for(requests, paths),
                        requests,
                        handoff,
                        empty_selection(),
                        root,
                    )
                self.assertFalse(output.exists())

    def test_rejects_missing_or_multiple_accepts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, paths = request_manifest_for(root)
            for states in (
                ("hold", "hold", "reject"),
                ("accept", "accept", "reject"),
            ):
                changed = review_for(requests, paths)
                for candidate, state in zip(changed["candidates"], states):
                    candidate["decision"] = state
                with self.assertRaisesRegex(
                    ValueError, "exactly one accepted candidate"
                ):
                    promote_review(
                        changed,
                        requests,
                        handoff_for(root),
                        empty_selection(),
                        root,
                    )

    def test_rejects_failed_or_missing_gate_and_request_mismatch(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, paths = request_manifest_for(root)
            review = review_for(requests, paths)
            failed = copy.deepcopy(review)
            failed["candidates"][0]["gates"]["footwear"] = "fail"
            with self.assertRaisesRegex(ValueError, "all acceptance gates"):
                promote_review(
                    failed,
                    requests,
                    handoff_for(root),
                    empty_selection(),
                    root,
                )
            mismatched = copy.deepcopy(review)
            mismatched["candidates"][0]["candidate_path"] = "wrong.png"
            with self.assertRaisesRegex(ValueError, "request target"):
                promote_review(
                    mismatched,
                    requests,
                    handoff_for(root),
                    empty_selection(),
                    root,
                )

    def test_rejects_source_pack_drift_and_implicit_replacement(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, paths = request_manifest_for(root)
            review = review_for(requests, paths)
            stale_requests = copy.deepcopy(requests)
            stale_requests["requests"][0]["source_pack_sha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "source pack"):
                promote_review(
                    review,
                    stale_requests,
                    handoff_for(root),
                    empty_selection(),
                    root,
                )
            existing = empty_selection()
            existing["accepted_motions"] = [accepted_record_for("walking")]
            with self.assertRaisesRegex(ValueError, "already accepted"):
                promote_review(
                    review, requests, handoff_for(root), existing, root
                )

    def test_invalid_existing_selection_writes_no_finished_asset(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, paths = request_manifest_for(root)
            existing = empty_selection()
            existing["accepted_motions"] = [{"motion": "seated"}]
            output = root / "source/finished/v1-2-motion/walking.webp"
            with self.assertRaisesRegex(ValueError, "accepted selection"):
                promote_review(
                    review_for(requests, paths),
                    requests,
                    handoff_for(root),
                    existing,
                    root,
                )
            self.assertFalse(output.exists())

    def test_enforces_motion_order_and_explicit_replacement(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            seated_requests, seated_paths = request_manifest_for(root, "seated")
            seated_output = root / "source/finished/v1-2-motion/seated.webp"
            with self.assertRaisesRegex(ValueError, "preceding motion"):
                promote_review(
                    review_for(seated_requests, seated_paths),
                    seated_requests,
                    handoff_for(root),
                    empty_selection(),
                    root,
                )
            self.assertFalse(seated_output.exists())

            turning_requests, turning_paths = request_manifest_for(root, "turning")
            walking_only = empty_selection()
            walking_only["accepted_motions"] = [accepted_record_for("walking")]
            with self.assertRaisesRegex(ValueError, "preceding motion"):
                promote_review(
                    review_for(turning_requests, turning_paths),
                    turning_requests,
                    handoff_for(root),
                    walking_only,
                    root,
                )

            walking_requests, walking_paths = request_manifest_for(root)
            with self.assertRaisesRegex(ValueError, "cannot replace unaccepted"):
                promote_review(
                    review_for(walking_requests, walking_paths),
                    walking_requests,
                    handoff_for(root),
                    empty_selection(),
                    root,
                    replace=True,
                )

    def test_rejects_bad_selection_schema_collection_and_partial_record(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, paths = request_manifest_for(root)
            output = root / "source/finished/v1-2-motion/walking.webp"
            cases = (
                ({**empty_selection(), "schema_version": 2}, "schema_version"),
                ({**empty_selection(), "collection_id": "wrong"}, "collection_id"),
                (
                    {
                        **empty_selection(),
                        "accepted_motions": [{"motion": "seated"}],
                    },
                    "complete traceability",
                ),
            )
            for selection, message in cases:
                with self.subTest(message=message):
                    with self.assertRaisesRegex(ValueError, message):
                        promote_review(
                            review_for(requests, paths),
                            requests,
                            handoff_for(root),
                            selection,
                            root,
                        )
                    self.assertFalse(output.exists())

    def test_rejects_blank_review_traceability_fields(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, paths = request_manifest_for(root)
            for field in ("review_id", "review_path"):
                review = review_for(requests, paths)
                review[field] = "  "
                with self.subTest(field=field):
                    with self.assertRaisesRegex(ValueError, field):
                        promote_review(
                            review,
                            requests,
                            handoff_for(root),
                            empty_selection(),
                            root,
                        )

    def test_rejected_candidate_requires_string_reason(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, paths = request_manifest_for(root)
            for reason in (None, 123, ""):
                review = review_for(requests, paths)
                review["candidates"][2]["rejection_reason"] = reason
                with self.subTest(reason=reason):
                    with self.assertRaisesRegex(
                        ValueError, "rejection_reason"
                    ):
                        promote_review(
                            review,
                            requests,
                            handoff_for(root),
                            empty_selection(),
                            root,
                        )

    def test_review_artifact_path_must_identify_cli_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            artifact = root / "evidence/v1-2-motion/reviews/walking.json"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("{}\n", encoding="utf-8")
            review = {
                "review_path": (
                    "evidence/v1-2-motion/reviews/../reviews/walking.json"
                )
            }
            validate_review_artifact_path(review, artifact, root)

            review["review_path"] = artifact.as_posix()
            validate_review_artifact_path(review, artifact, root)

            review["review_path"] = (
                "evidence/v1-2-motion/reviews/different.json"
            )
            with self.assertRaisesRegex(ValueError, "--review artifact"):
                validate_review_artifact_path(review, artifact, root)

    def test_invalid_active_request_numbers_write_no_finished_asset(self):
        cases = (
            ("revision", 0),
            ("candidate_number", 0),
            ("candidate_number", 4),
        )
        for field, value in cases:
            with self.subTest(field=field, value=value):
                with tempfile.TemporaryDirectory() as temp_dir:
                    root = Path(temp_dir)
                    requests, paths = request_manifest_for(root)
                    requests["requests"][0][field] = value
                    output = root / "source/finished/v1-2-motion/walking.webp"
                    with self.assertRaisesRegex(
                        ValueError, f"active request {field}"
                    ):
                        promote_review(
                            review_for(requests, paths),
                            requests,
                            handoff_for(root),
                            empty_selection(),
                            root,
                        )
                    self.assertFalse(output.exists())

    def test_failed_replacement_preserves_existing_finished_asset(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = root / "source/finished/v1-2-motion/walking.webp"
            output.parent.mkdir(parents=True)
            Image.new("RGB", (1024, 1536), "blue").save(
                output, "WEBP", quality=94, method=6
            )
            original_sha256 = sha256_file(output)

            existing = empty_selection()
            record = accepted_record_for("walking")
            record["finished_sha256"] = original_sha256
            existing["accepted_motions"] = [record]
            requests, paths = request_manifest_for(root)
            requests["requests"][0]["revision"] = 0

            with self.assertRaisesRegex(ValueError, "active request revision"):
                promote_review(
                    review_for(requests, paths),
                    requests,
                    handoff_for(root),
                    existing,
                    root,
                    replace=True,
                )
            self.assertEqual(original_sha256, sha256_file(output))
