import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import scripts.v1_2_motion_common as motion_common
from scripts.v1_2_motion_common import dump_json, load_json, validate_handoff


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "source/manifests/v1-2-motion/phase-2-handoff.json"


class AkariV12MotionCommonTest(unittest.TestCase):
    def test_dump_json_preserves_existing_file_when_replace_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "manifest.json"
            original = '{"state":"old"}\n'
            path.write_text(original, encoding="utf-8")

            def fail_replace(_source, _destination):
                raise OSError("injected replace failure")

            with patch.object(
                motion_common,
                "os",
                SimpleNamespace(
                    O_RDONLY=os.O_RDONLY,
                    close=os.close,
                    fsync=os.fsync,
                    open=os.open,
                    replace=fail_replace,
                ),
                create=True,
            ):
                with self.assertRaisesRegex(OSError, "injected replace failure"):
                    dump_json(path, {"state": "new"})

            self.assertEqual(original, path.read_text(encoding="utf-8"))
            self.assertEqual([], list(path.parent.glob(f".{path.name}-*.tmp")))

    def test_repository_handoff_is_valid(self):
        validate_handoff(load_json(HANDOFF), ROOT)

    def test_manifest_hash_drift_is_rejected(self):
        handoff = copy.deepcopy(load_json(HANDOFF))
        handoff["source_turnaround_manifest_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "manifest hash drift"):
            validate_handoff(handoff, ROOT)

    def test_asset_hash_drift_is_rejected(self):
        handoff = copy.deepcopy(load_json(HANDOFF))
        handoff["turnaround_inputs"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "asset hash drift"):
            validate_handoff(handoff, ROOT)

    def test_all_eight_canonical_slots_are_required(self):
        handoff = copy.deepcopy(load_json(HANDOFF))
        handoff["turnaround_inputs"].pop()
        with self.assertRaisesRegex(ValueError, "eight canonical turnaround inputs"):
            validate_handoff(handoff, ROOT)

    def test_final_review_must_still_be_approved(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            rejected = Path(temp_dir) / "rejected-review.json"
            rejected.write_text(
                json.dumps({"decision": "rejected", "user_decision": "approved"}),
                encoding="utf-8",
            )
            handoff = copy.deepcopy(load_json(HANDOFF))
            handoff["source_final_review"] = rejected.as_posix()
            with self.assertRaisesRegex(ValueError, "final Phase 1 review"):
                validate_handoff(handoff, ROOT)

    def test_final_review_must_reference_handoff_manifest(self):
        handoff, final_review = self._handoff_with_temporary_final_review()
        final_review["source_manifest"] = "source/manifests/other.json"
        self._write_final_review(handoff, final_review)
        with self.assertRaisesRegex(ValueError, "final Phase 1 review"):
            validate_handoff(handoff, ROOT)

    def test_final_review_must_reference_handoff_manifest_hash(self):
        handoff, final_review = self._handoff_with_temporary_final_review()
        final_review["source_manifest_sha256"] = "0" * 64
        self._write_final_review(handoff, final_review)
        with self.assertRaisesRegex(ValueError, "final Phase 1 review"):
            validate_handoff(handoff, ROOT)

    def test_final_review_must_accept_all_eight_canonical_slots(self):
        handoff, final_review = self._handoff_with_temporary_final_review()
        final_review["accepted_slots"].pop()
        self._write_final_review(handoff, final_review)
        with self.assertRaisesRegex(ValueError, "final Phase 1 review"):
            validate_handoff(handoff, ROOT)

    def test_every_final_review_gate_must_pass(self):
        handoff, final_review = self._handoff_with_temporary_final_review()
        final_review["gate_summary"]["quality"] = "fail"
        self._write_final_review(handoff, final_review)
        with self.assertRaisesRegex(ValueError, "final Phase 1 review"):
            validate_handoff(handoff, ROOT)

    def _handoff_with_temporary_final_review(self):
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        handoff = copy.deepcopy(load_json(HANDOFF))
        handoff["source_final_review"] = (
            Path(temporary_directory.name) / "final-review.json"
        ).as_posix()
        source_review = ROOT / load_json(HANDOFF)["source_final_review"]
        return handoff, copy.deepcopy(load_json(source_review))

    @staticmethod
    def _write_final_review(handoff, final_review):
        Path(handoff["source_final_review"]).write_text(
            json.dumps(final_review), encoding="utf-8"
        )
