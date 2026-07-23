import copy
import unittest
from pathlib import Path

from scripts.build_v1_2_turnaround_generation_requests import (
    build_ready_batch,
    merge_request_history,
    validate_identity_lock,
)
from scripts.v1_2_turnaround_common import load_json


ROOT = Path(__file__).resolve().parents[1]
IDENTITY_LOCK_PATH = (
    ROOT / "source/manifests/v1-2-turnaround/identity-lock.json"
)

IDENTITY_LOCK = {
    "schema_version": 1,
    "collection_id": "akari-v1.2-canonical-turnaround",
    "outfit_lock": {
        "top": "white oversized hoodie",
        "bottom": "gray pleated skirt",
        "socks": "white crew socks with two pale-blue stripes",
        "shoes": "chunky white sneakers with pale-blue accents",
        "hair_ornament": "two-part pale-blue character-left hair ornament",
        "excluded_accessories": ["shoulder bag"],
    },
    "reference_inputs": [
        {"role": "face_hair", "path": "refs/face.webp"},
        {"role": "body_proportion", "path": "refs/body.webp"},
        {"role": "standard_outfit_front", "path": "refs/front.webp"},
        {"role": "footwear_sock", "path": "refs/footwear.webp"},
        {"role": "sneaker_construction", "path": "refs/sneaker.webp"},
        {"role": "hairpin_side_front_45", "path": "refs/left45.webp"},
    ],
}

SLOT_MANIFEST = {
    "schema_version": 1,
    "collection_id": "akari-v1.2-canonical-turnaround",
    "slots": [
        {
            "angle_order": 1,
            "slug": "front",
            "japanese_title": "正面",
            "side": "center",
            "azimuth_degrees": 0,
            "view_family": "front",
            "hair_ornament_visibility": "visible",
            "upstream_slots": [],
            "legacy_reference_roles": [
                "standard_outfit_front",
                "body_proportion",
            ],
            "candidate_count": 3,
            "pose": "neutral_standing",
        },
        {
            "angle_order": 2,
            "slug": "character-left-front-three-quarter",
            "japanese_title": "キャラクター左・前45度",
            "side": "character_left",
            "azimuth_degrees": 45,
            "view_family": "front_three_quarter",
            "hair_ornament_visibility": "prominent",
            "upstream_slots": ["front"],
            "legacy_reference_roles": ["hairpin_side_front_45"],
            "candidate_count": 3,
            "pose": "neutral_standing",
        },
    ],
}


class AkariV12TurnaroundGenerationRequestsTest(unittest.TestCase):
    def test_identity_lock_matches_the_accepted_selection_and_asset(self):
        validate_identity_lock(load_json(IDENTITY_LOCK_PATH), ROOT)

    def test_identity_lock_rejects_rule_drift(self):
        identity_lock = copy.deepcopy(load_json(IDENTITY_LOCK_PATH))
        identity_lock["identity_rules"]["hair_ornament"]["lower"] = "missing"
        with self.assertRaisesRegex(ValueError, "identity rules"):
            validate_identity_lock(identity_lock, ROOT)

    def test_front_is_ready_without_upstream_acceptance(self):
        batch = build_ready_batch(
            SLOT_MANIFEST,
            IDENTITY_LOCK,
            {"accepted_angles": []},
            ["front"],
            "20260710",
            1,
        )
        self.assertEqual(3, len(batch["requests"]))
        self.assertEqual(
            [
                "source/generated/v1-2-turnaround/20260710_front_r1_c1.png",
                "source/generated/v1-2-turnaround/20260710_front_r1_c2.png",
                "source/generated/v1-2-turnaround/20260710_front_r1_c3.png",
            ],
            [request["target_path"] for request in batch["requests"]],
        )
        self.assertEqual(
            {"front": "batch:v1-2-turnaround:20260710:front:r1"},
            batch["active_batches"],
        )
        for request in batch["requests"]:
            self.assertIn("crossed X-shaped hairpins", request["prompt"])
            self.assertIn("compact ribbon-like loop", request["prompt"])
            self.assertIn("exactly two thin trailing strands", request["prompt"])

    def test_dependent_angle_is_blocked_until_front_is_accepted(self):
        with self.assertRaisesRegex(
            ValueError,
            "character-left-front-three-quarter requires accepted slot front",
        ):
            build_ready_batch(
                SLOT_MANIFEST,
                IDENTITY_LOCK,
                {"accepted_angles": []},
                ["character-left-front-three-quarter"],
                "20260710",
                1,
            )

    def test_dependent_angle_includes_the_accepted_neighbor(self):
        accepted = {
            "accepted_angles": [
                {
                    "slot": "front",
                    "accepted_path": (
                        "source/finished/v1-2-turnaround/front.webp"
                    ),
                }
            ]
        }
        batch = build_ready_batch(
            SLOT_MANIFEST,
            IDENTITY_LOCK,
            accepted,
            ["character-left-front-three-quarter"],
            "20260710",
            1,
        )
        for request in batch["requests"]:
            self.assertIn(
                "source/finished/v1-2-turnaround/front.webp",
                request["reference_pack_inputs"],
            )
            self.assertIn("refs/left45.webp", request["reference_pack_inputs"])
            self.assertLessEqual(len(request["reference_pack_inputs"]), 5)
            self.assertNotIn("refs/body.webp", request["reference_pack_inputs"])
            self.assertNotIn("refs/front.webp", request["reference_pack_inputs"])

    def test_request_history_is_append_only_and_idempotent(self):
        existing = {
            "schema_version": 1,
            "collection_id": "akari-v1.2-canonical-turnaround",
            "prompt_template_version": (
                "akari_v1_2_turnaround_adjacent_angle_v1"
            ),
            "active_batches": {},
            "requests": [],
        }
        first_batch = build_ready_batch(
            SLOT_MANIFEST,
            IDENTITY_LOCK,
            {"accepted_angles": []},
            ["front"],
            "20260710",
            1,
        )
        with_history = merge_request_history(existing, first_batch)
        second_batch = build_ready_batch(
            SLOT_MANIFEST,
            IDENTITY_LOCK,
            {"accepted_angles": []},
            ["front"],
            "20260710",
            2,
        )
        revised = merge_request_history(with_history, second_batch)
        idempotent = merge_request_history(revised, second_batch)
        self.assertEqual(6, len(revised["requests"]))
        self.assertEqual(
            "batch:v1-2-turnaround:20260710:front:r2",
            revised["active_batches"]["front"],
        )
        self.assertEqual(revised, idempotent)
        with self.assertRaisesRegex(ValueError, "cannot reactivate older revision"):
            merge_request_history(revised, first_batch)
