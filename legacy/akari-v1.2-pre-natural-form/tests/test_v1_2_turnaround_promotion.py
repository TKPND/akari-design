import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.promote_v1_2_turnaround_candidate import (
    promote_review,
    reopen_slots,
)
from scripts.v1_2_turnaround_common import (
    normalize_landmarks,
    sha256_file,
)


SLOTS = {
    "slots": [
        {
            "angle_order": 1,
            "slug": "front",
            "japanese_title": "正面",
            "upstream_slots": [],
        },
        {
            "angle_order": 2,
            "slug": "character-left-front-three-quarter",
            "japanese_title": "キャラクター左・前45度",
            "upstream_slots": ["front"],
        },
    ]
}

LANDMARK_Y_PX = {
    "crown": 96,
    "chin": 270,
    "shoulder": 350,
    "hoodie_hem": 720,
    "skirt_hem": 850,
    "knee": 1080,
    "ankle": 1370,
    "sole": 1464,
}


def request_for(
    candidate_path: str,
    slot: str = "front",
    request_id: str = "front-r1-c1",
    batch_id: str = "front-r1",
    revision: int = 1,
    candidate_number: int = 1,
) -> dict:
    return {
        "id": request_id,
        "batch_id": batch_id,
        "revision": revision,
        "candidate_number": candidate_number,
        "slot": slot,
        "target_path": candidate_path,
    }


def review_for(request: dict) -> dict:
    return {
        "schema_version": 1,
        "review_id": f"{request['slot']}-review",
        "review_path": (
            f"evidence/v1-2-turnaround/reviews/{request['slot']}-review.json"
        ),
        "stage": request["slot"],
        "slots": [request["slot"]],
        "request_batches": {request["slot"]: request["batch_id"]},
        "user_decision": "approved",
        "candidates": [
            {
                "request_id": request["id"],
                "slot": request["slot"],
                "candidate_path": request["target_path"],
                "state": "accept",
                "gates": {
                    "identity": "pass",
                    "geometry": "pass",
                    "outfit": "pass",
                    "quality": "pass",
                },
                "landmark_y_px": LANDMARK_Y_PX,
                "normalized_landmarks": normalize_landmarks(LANDMARK_Y_PX),
                "notes": (
                    "same Akari, coherent body, standard outfit, clean image"
                ),
                "rejection_reason": "",
            }
        ],
    }


def empty_accepted() -> dict:
    return {
        "schema_version": 1,
        "collection_id": "akari-v1.2-canonical-turnaround",
        "accepted_angles": [],
    }


class AkariV12TurnaroundPromotionTest(unittest.TestCase):
    def test_promote_review_writes_webp_hash_and_acceptance_record(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            candidate = root / "source/generated/v1-2-turnaround/front.png"
            candidate.parent.mkdir(parents=True)
            Image.new("RGB", (1024, 1536), "#f4eee8").save(candidate)
            request = request_for(candidate.relative_to(root).as_posix())
            result = promote_review(
                review_for(request),
                SLOTS,
                {
                    "active_batches": {"front": request["batch_id"]},
                    "requests": [request],
                },
                empty_accepted(),
                root,
            )
            record = result["accepted_angles"][0]
            self.assertEqual("front", record["slot"])
            output = root / record["accepted_path"]
            self.assertTrue(output.is_file())
            self.assertEqual(sha256_file(output), record["sha256"])
            self.assertEqual(LANDMARK_Y_PX, record["landmark_y_px"])
            self.assertEqual(
                normalize_landmarks(LANDMARK_Y_PX),
                record["normalized_landmarks"],
            )
            with Image.open(output) as image:
                self.assertEqual((1024, 1536), image.size)
                self.assertEqual("RGB", image.mode)

    def test_historical_batch_does_not_expand_the_active_review(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            candidate = root / "front-r2.png"
            Image.new("RGB", (1024, 1536), "white").save(candidate)
            active = request_for(
                candidate.as_posix(),
                request_id="front-r2-c1",
                batch_id="front-r2",
                revision=2,
            )
            historical = request_for(
                "front-r1.png",
                request_id="front-r1-c1",
                batch_id="front-r1",
            )
            result = promote_review(
                review_for(active),
                SLOTS,
                {
                    "active_batches": {"front": "front-r2"},
                    "requests": [historical, active],
                },
                empty_accepted(),
                root,
            )
            self.assertEqual("front-r2", result["accepted_angles"][0]["batch_id"])

    def test_promote_review_rejects_locked_dependency(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            candidate = root / "left.png"
            Image.new("RGB", (1024, 1536), "white").save(candidate)
            request = request_for(
                candidate.as_posix(),
                slot="character-left-front-three-quarter",
                request_id="left-request",
                batch_id="left-r1",
            )
            with self.assertRaisesRegex(ValueError, "requires accepted slot front"):
                promote_review(
                    review_for(request),
                    SLOTS,
                    {
                        "active_batches": {
                            "character-left-front-three-quarter": "left-r1"
                        },
                        "requests": [request],
                    },
                    empty_accepted(),
                    root,
                )

    def test_promote_review_requires_exactly_one_accept_per_slot(self):
        request = request_for("front.png")
        review = review_for(request)
        review["candidates"][0]["state"] = "hold"
        with self.assertRaisesRegex(
            ValueError,
            "exactly one accepted candidate for front",
        ):
            promote_review(
                review,
                SLOTS,
                {
                    "active_batches": {"front": "front-r1"},
                    "requests": [request],
                },
                empty_accepted(),
                Path("."),
            )

    def test_promote_review_requires_every_active_candidate(self):
        first = request_for("front-r2-c1.png", batch_id="front-r2", revision=2)
        second = request_for(
            "front-r2-c2.png",
            request_id="front-r2-c2",
            batch_id="front-r2",
            revision=2,
            candidate_number=2,
        )
        historical = request_for("front-r1-c1.png")
        review = review_for(first)
        with self.assertRaisesRegex(
            ValueError,
            "review must cover every materialized candidate",
        ):
            promote_review(
                review,
                SLOTS,
                {
                    "active_batches": {"front": "front-r2"},
                    "requests": [historical, first, second],
                },
                empty_accepted(),
                Path("."),
            )

    def test_promote_review_rejects_mismatched_normalization(self):
        request = request_for("front.png")
        review = review_for(request)
        review["candidates"][0]["normalized_landmarks"]["knee"] += 0.01
        with self.assertRaisesRegex(
            ValueError,
            "normalized landmarks do not match pixels",
        ):
            promote_review(
                review,
                SLOTS,
                {
                    "active_batches": {"front": "front-r1"},
                    "requests": [request],
                },
                empty_accepted(),
                Path("."),
            )

    def test_tolerance_failure_writes_no_finished_asset(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            candidate = root / "left.png"
            Image.new("RGB", (1024, 1536), "white").save(candidate)
            request = request_for(
                candidate.as_posix(),
                slot="character-left-front-three-quarter",
                request_id="left-request",
                batch_id="left-r1",
            )
            review = review_for(request)
            drifted = dict(LANDMARK_Y_PX)
            drifted["knee"] += 70
            review["candidates"][0]["landmark_y_px"] = drifted
            review["candidates"][0]["normalized_landmarks"] = (
                normalize_landmarks(drifted)
            )
            accepted = empty_accepted()
            accepted["accepted_angles"] = [
                {
                    "slot": "front",
                    "angle_order": 1,
                    "accepted_path": (
                        "source/finished/v1-2-turnaround/front.webp"
                    ),
                    "landmark_y_px": LANDMARK_Y_PX,
                    "normalized_landmarks": normalize_landmarks(LANDMARK_Y_PX),
                }
            ]
            with self.assertRaisesRegex(ValueError, "landmark validation failed"):
                promote_review(
                    review,
                    SLOTS,
                    {
                        "active_batches": {
                            "character-left-front-three-quarter": "left-r1"
                        },
                        "requests": [request],
                    },
                    accepted,
                    root,
                )
            self.assertFalse(
                (
                    root
                    / "source/finished/v1-2-turnaround/"
                    "character-left-front-three-quarter.webp"
                ).exists()
            )

    def test_reopen_review_removes_transitive_dependents_in_dependency_order(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            finished_dir = root / "source/finished/v1-2-turnaround"
            finished_dir.mkdir(parents=True)
            accepted_records = []
            for angle_order, slot in enumerate(
                ("front", "character-left-front-three-quarter"),
                start=1,
            ):
                path = finished_dir / f"{slot}.webp"
                Image.new("RGB", (1024, 1536), "white").save(path)
                accepted_records.append(
                    {
                        "slot": slot,
                        "angle_order": angle_order,
                        "accepted_path": path.relative_to(root).as_posix(),
                    }
                )
            accepted = empty_accepted()
            accepted["accepted_angles"] = accepted_records
            result = reopen_slots(
                {
                    "user_decision": "reopen",
                    "slots": ["front"],
                    "reason": "user approved correction after convergence review",
                },
                SLOTS,
                accepted,
                root,
            )
            self.assertEqual([], result["accepted_angles"])
            self.assertEqual(
                ["front", "character-left-front-three-quarter"],
                result["regeneration_queue"],
            )
            self.assertEqual([], list(finished_dir.glob("*.webp")))
