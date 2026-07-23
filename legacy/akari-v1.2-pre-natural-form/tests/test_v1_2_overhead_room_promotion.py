import copy
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.promote_v1_2_overhead_room_candidate import promote_review


GATES = {
    "identity",
    "age",
    "overhead_read",
    "anatomy",
    "ornament_side",
    "outfit",
    "intimacy",
    "composition",
    "artifacts",
    "collection_role",
}
PACK_SHA256 = "a" * 64


def fixtures(root: Path, pose: str = "supine-direct-gaze", order: int = 1):
    requests = []
    candidates = []
    for number in (1, 2):
        path = root / f"candidate-{number}.png"
        Image.new("RGB", (1024, 1536), "white").save(path)
        candidates.append(path)
        requests.append(
            {
                "id": f"request-{number}",
                "batch_id": "batch-r1",
                "pose": pose,
                "pose_order": order,
                "revision": 1,
                "candidate_number": number,
                "target_path": path.as_posix(),
                "source_pack_sha256": PACK_SHA256,
            }
        )
    manifest = {
        "active_batches": {pose: "batch-r1"},
        "requests": requests,
    }
    review = {
        "review_id": "review-r1",
        "review_path": "evidence/review-r1.json",
        "pose": pose,
        "batch_id": "batch-r1",
        "review_status": "approved",
        "candidates": [
            {
                "request_id": request["id"],
                "candidate_path": path.as_posix(),
                "decision": decision,
                "gates": {gate: "pass" for gate in GATES},
                "observations": {
                    gate: f"{gate} checked" for gate in GATES
                },
                "decision_reason": (
                    "strongest finished image"
                    if decision == "accept"
                    else "weaker expression"
                ),
            }
            for request, path, decision in zip(
                requests,
                candidates,
                ("accept", "hold"),
                strict=True,
            )
        ],
    }
    return manifest, review


def empty_selection() -> dict:
    return {
        "schema_version": 1,
        "collection_id": "akari-v1.2-overhead-room-portraits",
        "accepted_works": [],
    }


class AkariV12OverheadRoomPromotionTest(unittest.TestCase):
    def test_promotes_exactly_one_active_candidate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, review = fixtures(root)
            result = promote_review(
                review,
                requests,
                {"pack_sha256": PACK_SHA256},
                empty_selection(),
                root,
            )
            record = result["accepted_works"][0]
            self.assertEqual("supine-direct-gaze", record["pose"])
            self.assertTrue((root / record["finished_path"]).is_file())
            self.assertEqual(64, len(record["source_sha256"]))
            self.assertEqual(64, len(record["finished_sha256"]))

    def test_rejects_multiple_accepts_and_failed_gates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, review = fixtures(root)
            multiple = copy.deepcopy(review)
            multiple["candidates"][1]["decision"] = "accept"
            with self.assertRaisesRegex(
                ValueError, "exactly one accepted candidate"
            ):
                promote_review(
                    multiple,
                    requests,
                    {"pack_sha256": PACK_SHA256},
                    empty_selection(),
                    root,
                )

            failed = copy.deepcopy(review)
            failed["candidates"][0]["gates"]["anatomy"] = "fail"
            with self.assertRaisesRegex(ValueError, "all acceptance gates"):
                promote_review(
                    failed,
                    requests,
                    {"pack_sha256": PACK_SHA256},
                    empty_selection(),
                    root,
                )

    def test_rejects_wrong_dimensions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, review = fixtures(root)
            Image.new("RGB", (512, 768), "white").save(
                review["candidates"][0]["candidate_path"]
            )
            with self.assertRaisesRegex(ValueError, "RGB 1024x1536"):
                promote_review(
                    review,
                    requests,
                    {"pack_sha256": PACK_SHA256},
                    empty_selection(),
                    root,
                )

    def test_rejects_out_of_order_and_implicit_replacement(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, review = fixtures(root, "supine-bent-knees", 2)
            with self.assertRaisesRegex(ValueError, "next canonical pose"):
                promote_review(
                    review,
                    requests,
                    {"pack_sha256": PACK_SHA256},
                    empty_selection(),
                    root,
                )

            anchor_requests, anchor_review = fixtures(root)
            accepted = promote_review(
                anchor_review,
                anchor_requests,
                {"pack_sha256": PACK_SHA256},
                empty_selection(),
                root,
            )
            with self.assertRaisesRegex(ValueError, "already accepted"):
                promote_review(
                    anchor_review,
                    anchor_requests,
                    {"pack_sha256": PACK_SHA256},
                    accepted,
                    root,
                )

    def test_rejects_review_path_and_request_mismatch(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, review = fixtures(root)
            review["candidates"][0]["candidate_path"] = "wrong.png"
            with self.assertRaisesRegex(ValueError, "request target"):
                promote_review(
                    review,
                    requests,
                    {"pack_sha256": PACK_SHA256},
                    empty_selection(),
                    root,
                )
