import copy
import unittest
from pathlib import Path

from scripts.v1_2_overhead_room_common import (
    POSE_SLOTS,
    load_json,
    validate_pose_slots,
    validate_reference_pack,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/v1-2-overhead-room"


class AkariV12OverheadRoomCommonTest(unittest.TestCase):
    def test_repository_reference_pack_is_current(self):
        validate_reference_pack(
            load_json(MANIFEST_DIR / "reference-pack.json"), ROOT
        )

    def test_repository_pose_contract_has_ten_ordered_slots(self):
        manifest = load_json(MANIFEST_DIR / "pose-slots.json")
        validate_pose_slots(manifest)
        self.assertEqual(
            POSE_SLOTS, tuple(item["slug"] for item in manifest["poses"])
        )
        self.assertEqual(
            7, sum(item["framing"] == "full" for item in manifest["poses"])
        )
        self.assertEqual(
            3, sum(item["framing"] == "close" for item in manifest["poses"])
        )
        self.assertTrue(
            all(item["candidate_count"] == 2 for item in manifest["poses"])
        )

    def test_reference_manifest_hash_drift_is_rejected(self):
        pack = copy.deepcopy(load_json(MANIFEST_DIR / "reference-pack.json"))
        pack["source_manifests"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "manifest hash drift"):
            validate_reference_pack(pack, ROOT)

    def test_reference_asset_hash_drift_is_rejected(self):
        pack = copy.deepcopy(load_json(MANIFEST_DIR / "reference-pack.json"))
        pack["reference_inputs"][0]["assets"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "reference asset hash drift"):
            validate_reference_pack(pack, ROOT)

    def test_composition_reference_cannot_be_an_identity_source(self):
        pack = copy.deepcopy(load_json(MANIFEST_DIR / "reference-pack.json"))
        composition = next(
            item
            for item in pack["reference_inputs"]
            if item["role"] == "composition_mood_only"
        )
        composition["identity_source"] = True
        with self.assertRaisesRegex(ValueError, "composition reference"):
            validate_reference_pack(pack, ROOT)
