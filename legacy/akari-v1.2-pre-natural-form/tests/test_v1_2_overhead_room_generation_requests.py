import unittest

from scripts.build_v1_2_overhead_room_generation_requests import (
    build_ready_batch,
    merge_request_history,
)


PACK = {
    "collection_id": "akari-v1.2-overhead-room-portraits",
    "pack_sha256": "pack-hash",
    "reference_inputs": [
        {
            "role": "identity_face",
            "assets": [{"path": "face.webp", "sha256": "f"}],
        },
        {
            "role": "turnaround",
            "assets": [
                {
                    "path": "front.webp",
                    "sha256": "t",
                    "slot": "front",
                    "order": 1,
                },
                {
                    "path": "left-front-three-quarter.webp",
                    "sha256": "t3q",
                    "slot": "character-left-front-three-quarter",
                    "order": 2,
                }
            ],
        },
        {
            "role": "motion",
            "assets": [
                {
                    "path": "seated.webp",
                    "sha256": "m",
                    "motion": "seated",
                    "order": 2,
                }
            ],
        },
        {
            "role": "composition_mood_only",
            "identity_source": False,
            "assets": [{"path": "sample.webp", "sha256": "c"}],
        },
    ],
}
POSES = {
    "poses": [
        {
            "slug": "supine-direct-gaze",
            "pose_order": 1,
            "framing": "full",
            "angle_degrees": [80, 90],
            "candidate_count": 2,
            "outfit": "oversized-hoodie-shorts",
            "feet": "striped-socks",
            "background": "ivory-rug",
            "prop_count": 1,
        }
    ]
}


class AkariV12OverheadRoomGenerationRequestsTest(unittest.TestCase):
    def test_anchor_batch_has_two_requests_and_no_collection_anchor(self):
        batch = build_ready_batch(
            PACK,
            POSES,
            "supine-direct-gaze",
            "20260713",
            1,
            [],
            None,
        )
        self.assertEqual(2, len(batch["requests"]))
        self.assertEqual(
            [1, 2],
            [item["candidate_number"] for item in batch["requests"]],
        )
        self.assertTrue(
            all("collection_anchor" not in item for item in batch["requests"])
        )

    def test_anchor_prompt_carries_visual_and_safety_locks(self):
        request = build_ready_batch(
            PACK,
            POSES,
            "supine-direct-gaze",
            "20260713",
            1,
            [],
            None,
        )["requests"][0]
        self.assertIn("1024x1536 RGB", request["prompt"])
        self.assertIn("character-left", request["prompt"])
        self.assertIn("80 to 90 degrees", request["prompt"])
        self.assertIn("not an identity or wardrobe source", request["prompt"])
        self.assertIn("No readable text", request["prompt"])
        self.assertEqual("striped-socks", request["feet"])
        self.assertEqual(5, len(request["reference_roles"]))

    def test_non_anchor_pose_requires_accepted_collection_anchor(self):
        poses = {
            "poses": [
                dict(
                    POSES["poses"][0],
                    slug="supine-bent-knees",
                    pose_order=2,
                    outfit="loose-tshirt-shorts",
                    feet="barefoot",
                    background="pale-bedding",
                    prop_count=0,
                )
            ]
        }
        with self.assertRaisesRegex(ValueError, "collection anchor"):
            build_ready_batch(
                PACK,
                poses,
                "supine-bent-knees",
                "20260713",
                1,
                [],
                None,
            )

        anchor = {
            "pose": "supine-direct-gaze",
            "finished_path": "source/finished/anchor.webp",
            "finished_sha256": "anchor-hash",
        }
        request = build_ready_batch(
            PACK,
            poses,
            "supine-bent-knees",
            "20260713",
            1,
            [],
            anchor,
        )["requests"][0]
        self.assertEqual(anchor, request["collection_anchor"])
        self.assertEqual(
            "source/finished/anchor.webp",
            request["reference_roles"][-1]["path"],
        )

    def test_regeneration_requires_non_blank_failure_observations(self):
        with self.assertRaisesRegex(ValueError, "failure observations"):
            build_ready_batch(
                PACK,
                POSES,
                "supine-direct-gaze",
                "20260713",
                2,
                [],
                None,
            )
        with self.assertRaisesRegex(ValueError, "failure observations"):
            build_ready_batch(
                PACK,
                POSES,
                "supine-direct-gaze",
                "20260713",
                2,
                ["  "],
                None,
            )

    def test_history_is_idempotent_and_rejects_older_reactivation(self):
        empty = {
            "schema_version": 1,
            "collection_id": PACK["collection_id"],
            "active_batches": {},
            "requests": [],
        }
        first = build_ready_batch(
            PACK,
            POSES,
            "supine-direct-gaze",
            "20260713",
            1,
            [],
            None,
        )
        current = merge_request_history(empty, first)
        second = build_ready_batch(
            PACK,
            POSES,
            "supine-direct-gaze",
            "20260713",
            2,
            ["hand anatomy failed"],
            None,
        )
        revised = merge_request_history(current, second)
        self.assertEqual(revised, merge_request_history(revised, second))
        with self.assertRaisesRegex(ValueError, "older revision"):
            merge_request_history(revised, first)
