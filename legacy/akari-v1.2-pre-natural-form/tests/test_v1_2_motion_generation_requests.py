import unittest

from scripts.build_v1_2_motion_generation_requests import build_ready_batch, merge_request_history

HANDOFF = {
    "collection_id": "akari-v1.2-representative-motion-poses",
    "source_turnaround_manifest_sha256": "abc123",
    "turnaround_inputs": [{"slot": f"s{i}", "accepted_path": f"refs/{i}.webp", "sha256": str(i)} for i in range(8)],
    "motion_slots": [
        {"slug": slug, "candidate_count": 3, "deliverable_count": 1}
        for slug in ("walking", "seated", "turning")
    ],
}


class AkariV12MotionGenerationRequestsTest(unittest.TestCase):
    def test_walking_batch_has_three_distinct_requests_and_all_references(self):
        batch = build_ready_batch(HANDOFF, "walking", "20260713", 1, [])
        self.assertEqual(3, len(batch["requests"]))
        self.assertEqual(8, len(batch["requests"][0]["reference_pack_inputs"]))
        self.assertEqual([1, 2, 3], [item["candidate_number"] for item in batch["requests"]])
        self.assertEqual("batch:v1-2-motion:20260713:walking:r1", batch["active_batches"]["walking"])

    def test_motion_prompts_include_shared_and_pose_specific_locks(self):
        expected = {
            "walking": "readable mid-step",
            "seated": "invisible support plane",
            "turning": "face, shoulder, and hip rotation",
        }
        for motion, phrase in expected.items():
            request = build_ready_batch(HANDOFF, motion, "20260713", 1, [])["requests"][0]
            self.assertIn(phrase, request["prompt"])
            self.assertIn("character-left", request["prompt"])
            self.assertIn("1024x1536", request["prompt"])

    def test_regeneration_requires_failure_observations(self):
        with self.assertRaisesRegex(ValueError, "failure observations"):
            build_ready_batch(HANDOFF, "walking", "20260713", 2, [])

    def test_regeneration_rejects_blank_observations_and_trims_content(self):
        with self.assertRaisesRegex(ValueError, "failure observations"):
            build_ready_batch(HANDOFF, "walking", "20260713", 2, ["   "])
        request = build_ready_batch(
            HANDOFF,
            "walking",
            "20260713",
            2,
            ["  malformed feet  "],
        )["requests"][0]
        self.assertIn(
            "Regeneration failure observations to correct: malformed feet.",
            request["prompt"],
        )
        self.assertNotIn("  malformed feet  ", request["prompt"])

    def test_motion_history_requires_predecessors_but_allows_earlier_revisions(self):
        empty = {
            "schema_version": 1,
            "collection_id": HANDOFF["collection_id"],
            "active_batches": {},
            "requests": [],
        }
        seated = build_ready_batch(HANDOFF, "seated", "20260713", 1, [])
        with self.assertRaisesRegex(ValueError, "preceding motion"):
            merge_request_history(empty, seated)

        walking = build_ready_batch(HANDOFF, "walking", "20260713", 1, [])
        walking_history = merge_request_history(empty, walking)
        turning = build_ready_batch(HANDOFF, "turning", "20260713", 1, [])
        with self.assertRaisesRegex(ValueError, "preceding motion"):
            merge_request_history(walking_history, turning)

        sequential = merge_request_history(walking_history, seated)
        complete = merge_request_history(sequential, turning)
        walking_revision = build_ready_batch(
            HANDOFF,
            "walking",
            "20260713",
            2,
            ["malformed feet"],
        )
        revised = merge_request_history(complete, walking_revision)
        self.assertEqual(
            "batch:v1-2-motion:20260713:walking:r2",
            revised["active_batches"]["walking"],
        )

    def test_history_is_idempotent_and_rejects_older_reactivation(self):
        empty = {"schema_version": 1, "collection_id": HANDOFF["collection_id"], "active_batches": {}, "requests": []}
        first = build_ready_batch(HANDOFF, "walking", "20260713", 1, [])
        current = merge_request_history(empty, first)
        second = build_ready_batch(HANDOFF, "walking", "20260713", 2, ["all candidates had malformed feet"])
        revised = merge_request_history(current, second)
        self.assertEqual(revised, merge_request_history(revised, second))
        with self.assertRaisesRegex(ValueError, "older revision"):
            merge_request_history(revised, first)
