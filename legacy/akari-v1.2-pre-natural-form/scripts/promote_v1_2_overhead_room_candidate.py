#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import tempfile
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from scripts.promote_v1_2_motion_candidate import (
    commit_promotion_transaction,
)
from scripts.v1_2_overhead_room_common import (
    COLLECTION_ID,
    POSE_SLOTS,
    load_json,
    resolve_path,
    sha256_file,
    validate_reference_pack,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/v1-2-overhead-room"
REFERENCE_PACK_PATH = MANIFEST_DIR / "reference-pack.json"
REQUESTS_PATH = MANIFEST_DIR / "generation-requests.json"
ACCEPTED_PATH = MANIFEST_DIR / "accepted-selection.json"
REQUIRED_GATES = {
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
ALLOWED_DECISIONS = {"accept", "hold", "reject"}
TRACEABILITY_FIELDS = {
    "finished_path",
    "source_candidate_path",
    "request_id",
    "batch_id",
    "review_id",
    "review_path",
}
HASH_FIELDS = {
    "source_pack_sha256",
    "source_sha256",
    "finished_sha256",
}


def _non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_accepted_selection(accepted: dict) -> dict[str, dict]:
    if (
        type(accepted.get("schema_version")) is not int
        or accepted["schema_version"] != 1
        or accepted.get("collection_id") != COLLECTION_ID
        or not isinstance(accepted.get("accepted_works"), list)
    ):
        raise ValueError("accepted selection identity is invalid")

    works = accepted["accepted_works"]
    poses = []
    for record in works:
        pose = record.get("pose")
        if (
            pose not in POSE_SLOTS
            or type(record.get("pose_order")) is not int
            or record["pose_order"] != POSE_SLOTS.index(pose) + 1
            or type(record.get("revision")) is not int
            or record["revision"] < 1
            or type(record.get("candidate_number")) is not int
            or record["candidate_number"] not in {1, 2}
            or any(
                not _non_empty_string(record.get(field))
                for field in TRACEABILITY_FIELDS
            )
            or any(
                not isinstance(record.get(field), str)
                or re.fullmatch(r"[0-9a-f]{64}", record[field]) is None
                for field in HASH_FIELDS
            )
        ):
            raise ValueError("accepted selection requires complete traceability")
        poses.append(pose)

    if len(set(poses)) != len(poses):
        raise ValueError("accepted selection contains duplicate poses")
    if poses != list(POSE_SLOTS[: len(poses)]):
        raise ValueError("accepted selection must be a canonical pose prefix")
    return {record["pose"]: record for record in works}


def _active_requests(request_manifest: dict, pose: str, batch_id: str) -> list[dict]:
    if request_manifest.get("active_batches", {}).get(pose) != batch_id:
        raise ValueError("review does not target the active pose batch")
    requests = sorted(
        [
            request
            for request in request_manifest.get("requests", [])
            if request.get("pose") == pose
            and request.get("batch_id") == batch_id
        ],
        key=lambda item: item.get("candidate_number", 0),
    )
    if (
        len(requests) != 2
        or [item.get("candidate_number") for item in requests] != [1, 2]
    ):
        raise ValueError("active pose batch must contain exactly two candidates")
    return requests


def validate_review(
    review: dict, request_manifest: dict, reference_pack: dict
) -> tuple[dict, dict]:
    if review.get("review_status") != "approved":
        raise ValueError("review status must be approved")
    pose = review.get("pose")
    batch_id = review.get("batch_id")
    if pose not in POSE_SLOTS or not _non_empty_string(batch_id):
        raise ValueError("review pose or batch is invalid")
    if not _non_empty_string(review.get("review_id")) or not _non_empty_string(
        review.get("review_path")
    ):
        raise ValueError("review traceability is incomplete")

    requests = _active_requests(request_manifest, pose, batch_id)
    requests_by_id = {item["id"]: item for item in requests}
    if any(
        request.get("source_pack_sha256") != reference_pack.get("pack_sha256")
        for request in requests
    ):
        raise ValueError("request source pack does not match current reference pack")

    candidates = review.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != 2:
        raise ValueError("review must cover exactly two candidates")
    reviewed_ids = [item.get("request_id") for item in candidates]
    if set(reviewed_ids) != set(requests_by_id) or len(set(reviewed_ids)) != 2:
        raise ValueError("review must cover every active request exactly once")

    accepted_pairs = []
    for candidate in candidates:
        request = requests_by_id[candidate["request_id"]]
        if candidate.get("candidate_path") != request.get("target_path"):
            raise ValueError("review candidate path does not match request target")
        decision = candidate.get("decision")
        if decision not in ALLOWED_DECISIONS:
            raise ValueError(f"invalid review decision: {decision}")
        if set(candidate.get("gates", {})) != REQUIRED_GATES:
            raise ValueError("review must include every acceptance gate")
        observations = candidate.get("observations")
        if (
            not isinstance(observations, dict)
            or set(observations) != REQUIRED_GATES
            or any(not _non_empty_string(value) for value in observations.values())
        ):
            raise ValueError("review must include every gate observation")
        if not _non_empty_string(candidate.get("decision_reason")):
            raise ValueError("review candidates require a decision reason")
        if decision == "accept":
            accepted_pairs.append((candidate, request))

    if len(accepted_pairs) != 1:
        raise ValueError("review must contain exactly one accepted candidate")
    candidate, request = accepted_pairs[0]
    if any(candidate["gates"][gate] != "pass" for gate in REQUIRED_GATES):
        raise ValueError("accepted candidate must pass all acceptance gates")
    return candidate, request


def _stage_webp(source_path: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        with Image.open(source_path) as image:
            image.load()
            if image.mode != "RGB" or image.size != (1024, 1536):
                raise ValueError(
                    f"accepted candidate must be RGB 1024x1536: {source_path}"
                )
            with tempfile.NamedTemporaryFile(
                prefix=".overhead-room-promotion-",
                suffix=".webp",
                dir=output_dir,
                delete=False,
            ) as temporary:
                staged = Path(temporary.name)
            image.save(staged, "WEBP", quality=95, method=6)
    except (OSError, UnidentifiedImageError):
        raise ValueError(
            f"accepted candidate is missing or unreadable: {source_path}"
        ) from None
    return staged


def promote_review(
    review: dict,
    request_manifest: dict,
    reference_pack: dict,
    accepted: dict,
    project_root: Path,
    replace: bool = False,
    accepted_path: Path | None = None,
) -> dict:
    current = validate_accepted_selection(accepted)
    candidate, request = validate_review(
        review, request_manifest, reference_pack
    )
    pose = request["pose"]

    if pose in current and not replace:
        raise ValueError(f"pose is already accepted: {pose}")
    if pose not in current:
        next_index = len(current)
        if next_index >= len(POSE_SLOTS) or POSE_SLOTS[next_index] != pose:
            raise ValueError(
                f"new promotion must target the next canonical pose: {POSE_SLOTS[next_index]}"
            )

    source_path = resolve_path(project_root, candidate["candidate_path"])
    output_relative = f"source/finished/v1-2-overhead-room/{pose}.webp"
    output_path = project_root / output_relative
    staged_webp = _stage_webp(source_path, output_path.parent)
    try:
        record = {
            "pose": pose,
            "pose_order": request["pose_order"],
            "finished_path": output_relative,
            "source_candidate_path": candidate["candidate_path"],
            "request_id": request["id"],
            "batch_id": request["batch_id"],
            "revision": request["revision"],
            "candidate_number": request["candidate_number"],
            "review_id": review["review_id"],
            "review_path": review["review_path"],
            "source_pack_sha256": request["source_pack_sha256"],
            "source_sha256": sha256_file(source_path),
            "finished_sha256": sha256_file(staged_webp),
        }

        works = [dict(item) for item in accepted["accepted_works"]]
        if pose in current:
            works[POSE_SLOTS.index(pose)] = record
        else:
            works.append(record)
        updated = {
            "schema_version": 1,
            "collection_id": COLLECTION_ID,
            "accepted_works": works,
        }
        validate_accepted_selection(updated)

        selection_path = accepted_path or (
            project_root
            / "source/manifests/v1-2-overhead-room/accepted-selection.json"
        )
        commit_promotion_transaction(
            staged_webp,
            output_path,
            selection_path,
            updated,
        )
        staged_webp = None
        return updated
    finally:
        if staged_webp is not None:
            staged_webp.unlink(missing_ok=True)


def _rooted(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Promote one approved Akari overhead-room candidate."
    )
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--requests", type=Path, default=REQUESTS_PATH)
    parser.add_argument("--reference-pack", type=Path, default=REFERENCE_PACK_PATH)
    parser.add_argument("--accepted", type=Path, default=ACCEPTED_PATH)
    parser.add_argument("--replace", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    review_path = _rooted(args.review)
    requests_path = _rooted(args.requests)
    reference_pack_path = _rooted(args.reference_pack)
    accepted_path = _rooted(args.accepted)

    review = load_json(review_path)
    try:
        expected_review_path = review_path.relative_to(ROOT).as_posix()
    except ValueError:
        expected_review_path = review_path.as_posix()
    if review.get("review_path") != expected_review_path:
        raise ValueError("review_path does not match the review artifact")

    reference_pack = load_json(reference_pack_path)
    validate_reference_pack(reference_pack, ROOT)
    accepted = load_json(accepted_path)
    updated = promote_review(
        review,
        load_json(requests_path),
        reference_pack,
        accepted,
        ROOT,
        replace=args.replace,
        accepted_path=accepted_path,
    )
    print(f"overhead room accepted works: {len(updated['accepted_works'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
