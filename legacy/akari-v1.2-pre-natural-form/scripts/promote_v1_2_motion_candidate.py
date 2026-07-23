#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shutil
import tempfile
from pathlib import Path

from PIL import Image

from scripts.v1_2_motion_common import (
    dump_json,
    fsync_directory,
    load_json,
    resolve_path,
    sha256_file,
    validate_handoff,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/v1-2-motion"
HANDOFF_PATH = MANIFEST_DIR / "phase-2-handoff.json"
REQUESTS_PATH = MANIFEST_DIR / "generation-requests.json"
ACCEPTED_PATH = MANIFEST_DIR / "accepted-selection.json"
REQUIRED_GATES = {
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
ALLOWED_DECISIONS = {"accept", "hold", "reject"}
MOTION_ORDER = {"walking": 1, "seated": 2, "turning": 3}
COLLECTION_ID = "akari-v1.2-representative-motion-poses"
TRACEABILITY_STRING_FIELDS = {
    "finished_path",
    "source_candidate_path",
    "request_id",
    "batch_id",
    "review_id",
    "review_path",
}
TRACEABILITY_HASH_FIELDS = {
    "source_pack_sha256",
    "source_sha256",
    "finished_sha256",
}


def promotion_journal_path(accepted_path: Path) -> Path:
    return accepted_path.parent / f".{accepted_path.name}.promotion-transaction.json"


def _backup_file(path: Path, label: str) -> Path | None:
    if not path.exists():
        return None
    backup: Path | None = None
    completed = False
    try:
        with tempfile.NamedTemporaryFile(
            prefix=f".{path.name}-{label}-",
            suffix=".backup",
            dir=path.parent,
            delete=False,
        ) as temporary:
            backup = Path(temporary.name)
            with path.open("rb") as source:
                shutil.copyfileobj(source, temporary)
            temporary.flush()
            os.fsync(temporary.fileno())
        completed = True
        return backup
    finally:
        if not completed and backup is not None:
            backup.unlink(missing_ok=True)


def _fsync_file(path: Path) -> None:
    with path.open("rb") as file_handle:
        os.fsync(file_handle.fileno())


def _stage_json(path: Path, data: dict) -> Path:
    with tempfile.NamedTemporaryFile(
        prefix=f".{path.name}-promotion-",
        suffix=".tmp",
        dir=path.parent,
        delete=False,
    ) as temporary:
        staged = Path(temporary.name)
    try:
        dump_json(staged, data)
    except BaseException:
        staged.unlink(missing_ok=True)
        raise
    return staged


def _restore_transaction_path(
    destination: Path, backup: Path | None, existed: bool
) -> None:
    if existed:
        if backup is None or not backup.is_file():
            raise RuntimeError(f"promotion backup is missing: {destination}")
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                prefix=f".{destination.name}-restore-",
                suffix=".tmp",
                dir=destination.parent,
                delete=False,
            ) as temporary:
                temporary_path = Path(temporary.name)
                with backup.open("rb") as source:
                    shutil.copyfileobj(source, temporary)
                temporary.flush()
                os.fsync(temporary.fileno())
            os.replace(temporary_path, destination)
            temporary_path = None
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
    else:
        destination.unlink(missing_ok=True)


def recover_promotion_transaction(accepted_path: Path) -> None:
    journal_path = promotion_journal_path(accepted_path)
    if not journal_path.is_file():
        return
    journal = load_json(journal_path)
    output_path = Path(journal["output_path"])
    recorded_accepted = Path(journal["accepted_path"])
    if recorded_accepted.resolve() != accepted_path.resolve():
        raise RuntimeError("promotion journal targets a different accepted manifest")

    output_backup = (
        Path(journal["output_backup"]) if journal.get("output_backup") else None
    )
    accepted_backup = (
        Path(journal["accepted_backup"])
        if journal.get("accepted_backup")
        else None
    )
    state = journal.get("state")
    if state == "prepared":
        _restore_transaction_path(
            output_path, output_backup, bool(journal["output_existed"])
        )
        _restore_transaction_path(
            accepted_path, accepted_backup, bool(journal["accepted_existed"])
        )
        fsync_directory(output_path.parent)
        if accepted_path.parent != output_path.parent:
            fsync_directory(accepted_path.parent)
        journal["state"] = "rolled_back"
        dump_json(journal_path, journal)
    elif state not in {"committed", "rolled_back"}:
        raise RuntimeError("promotion journal has an invalid state")

    resource_directories = {output_path.parent, accepted_path.parent}
    for field in (
        "output_backup",
        "accepted_backup",
        "staged_webp",
        "staged_manifest",
    ):
        if journal.get(field):
            resource = Path(journal[field])
            resource_directories.add(resource.parent)
            resource.unlink(missing_ok=True)
    journal_path.unlink(missing_ok=True)
    resource_directories.add(journal_path.parent)
    for directory in sorted(resource_directories, key=lambda path: path.as_posix()):
        fsync_directory(directory)


def commit_promotion_transaction(
    staged_webp: Path,
    output_path: Path,
    accepted_path: Path,
    updated_selection: dict,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    accepted_path.parent.mkdir(parents=True, exist_ok=True)
    recover_promotion_transaction(accepted_path)

    journal_path = promotion_journal_path(accepted_path)
    staged_manifest: Path | None = None
    output_backup: Path | None = None
    accepted_backup: Path | None = None
    try:
        staged_manifest = _stage_json(accepted_path, updated_selection)
        output_backup = _backup_file(output_path, "previous")
        accepted_backup = _backup_file(accepted_path, "previous")
        _fsync_file(staged_webp)
        resource_directories = {
            staged_webp.parent,
            staged_manifest.parent,
            output_path.parent,
            accepted_path.parent,
        }
        if output_backup is not None:
            resource_directories.add(output_backup.parent)
        if accepted_backup is not None:
            resource_directories.add(accepted_backup.parent)
        for directory in sorted(
            resource_directories, key=lambda path: path.as_posix()
        ):
            fsync_directory(directory)
    except BaseException:
        for path in (
            staged_webp,
            staged_manifest,
            output_backup,
            accepted_backup,
        ):
            if path is not None:
                path.unlink(missing_ok=True)
        raise

    journal = {
        "state": "prepared",
        "output_path": output_path.resolve().as_posix(),
        "accepted_path": accepted_path.resolve().as_posix(),
        "output_existed": output_path.exists(),
        "accepted_existed": accepted_path.exists(),
        "output_backup": output_backup.as_posix() if output_backup else None,
        "accepted_backup": accepted_backup.as_posix() if accepted_backup else None,
        "staged_webp": staged_webp.as_posix(),
        "staged_manifest": staged_manifest.as_posix(),
    }
    try:
        dump_json(journal_path, journal)
        os.replace(staged_webp, output_path)
        fsync_directory(output_path.parent)
        os.replace(staged_manifest, accepted_path)
        fsync_directory(accepted_path.parent)
        journal["state"] = "committed"
        dump_json(journal_path, journal)
    except Exception:
        if journal_path.is_file():
            recover_promotion_transaction(accepted_path)
        else:
            for path in (
                staged_webp,
                staged_manifest,
                output_backup,
                accepted_backup,
            ):
                if path is not None:
                    path.unlink(missing_ok=True)
        raise
    recover_promotion_transaction(accepted_path)


def _is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_accepted_selection(accepted: dict) -> dict[str, dict]:
    if type(accepted.get("schema_version")) is not int or accepted.get(
        "schema_version"
    ) != 1:
        raise ValueError("accepted selection schema_version must be 1")
    if accepted.get("collection_id") != COLLECTION_ID:
        raise ValueError("accepted selection collection_id is invalid")
    accepted_motions = accepted.get("accepted_motions")
    if not isinstance(accepted_motions, list):
        raise ValueError("accepted selection accepted_motions must be a list")

    for record in accepted_motions:
        if not isinstance(record, dict):
            raise ValueError("accepted selection requires complete traceability")
        motion = record.get("motion")
        if (
            motion not in MOTION_ORDER
            or type(record.get("motion_order")) is not int
            or record.get("motion_order") != MOTION_ORDER[motion]
            or any(
                not _is_non_empty_string(record.get(field))
                for field in TRACEABILITY_STRING_FIELDS
            )
            or type(record.get("revision")) is not int
            or record["revision"] < 1
            or type(record.get("candidate_number")) is not int
            or record["candidate_number"] < 1
            or any(
                not isinstance(record.get(field), str)
                or re.fullmatch(r"[0-9a-f]{64}", record[field]) is None
                for field in TRACEABILITY_HASH_FIELDS
            )
        ):
            raise ValueError("accepted selection requires complete traceability")

    current = {record["motion"]: record for record in accepted_motions}
    if len(current) != len(accepted_motions):
        raise ValueError("accepted selection contains duplicate motions")
    motions = [record["motion"] for record in accepted_motions]
    expected_prefix = list(MOTION_ORDER)[: len(motions)]
    if motions != expected_prefix:
        raise ValueError("accepted selection violates motion order prerequisites")
    return current


def validate_review(
    review: dict, request_manifest: dict, handoff: dict
) -> dict:
    if review.get("user_decision") != "approved":
        raise ValueError("review is not user-approved")
    for field in ("review_id", "review_path"):
        if not _is_non_empty_string(review.get(field)):
            raise ValueError(f"review {field} must be a non-empty string")

    motion = review.get("motion")
    if motion not in MOTION_ORDER:
        raise ValueError(f"unknown review motion: {motion}")
    active_batch = request_manifest.get("active_batches", {}).get(motion)
    if not _is_non_empty_string(active_batch) or review.get(
        "batch_id"
    ) != active_batch:
        raise ValueError("review must name the active batch for its motion")

    active_requests = [
        request
        for request in request_manifest.get("requests", [])
        if isinstance(request, dict) and request.get("batch_id") == active_batch
    ]
    if len(active_requests) != 3:
        raise ValueError("active motion batch must contain exactly three requests")
    for request in active_requests:
        for field in ("id", "batch_id", "target_path", "source_pack_sha256"):
            if not _is_non_empty_string(request.get(field)):
                raise ValueError(
                    f"active request {field} must be a non-empty string"
                )
        if request.get("motion") != motion or motion not in MOTION_ORDER:
            raise ValueError("active request motion does not match review motion")
        if "motion_order" in request and (
            type(request["motion_order"]) is not int
            or request["motion_order"] != MOTION_ORDER[motion]
        ):
            raise ValueError("active request motion_order is invalid")
        if (
            type(request.get("revision")) is not int
            or request["revision"] < 1
        ):
            raise ValueError("active request revision must be at least 1")
        if (
            type(request.get("candidate_number")) is not int
            or not 1 <= request["candidate_number"] <= 3
        ):
            raise ValueError("active request candidate_number must be 1..3")
    if {request["candidate_number"] for request in active_requests} != {1, 2, 3}:
        raise ValueError("active request candidate_number values must be 1, 2, 3")
    requests_by_id = {request.get("id"): request for request in active_requests}
    if None in requests_by_id or len(requests_by_id) != len(active_requests):
        raise ValueError("active motion requests must have unique IDs")

    candidates = review.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError("review candidates must be a list")
    reviewed_ids = [candidate.get("request_id") for candidate in candidates]
    if (
        len(reviewed_ids) != len(active_requests)
        or set(reviewed_ids) != set(requests_by_id)
    ):
        raise ValueError("review must cover all three active requests")

    accepted = []
    for candidate in candidates:
        request = requests_by_id[candidate["request_id"]]
        if candidate.get("candidate_path") != request.get("target_path"):
            raise ValueError("candidate path does not match request target")
        decision = candidate.get("decision")
        if decision not in ALLOWED_DECISIONS:
            raise ValueError(f"invalid candidate decision: {decision}")

        gates = candidate.get("gates")
        observations = candidate.get("observations")
        if not isinstance(gates, dict) or set(gates) != REQUIRED_GATES:
            raise ValueError("candidate must include all acceptance gates")
        if not isinstance(observations, dict) or set(observations) != REQUIRED_GATES:
            raise ValueError("candidate must include all gate observations")
        if any(
            not isinstance(observations[gate], str)
            or not observations[gate].strip()
            for gate in REQUIRED_GATES
        ):
            raise ValueError("every acceptance gate requires an observation")
        if decision == "reject" and not _is_non_empty_string(
            candidate.get("rejection_reason")
        ):
            raise ValueError(
                "rejected candidate requires string rejection_reason"
            )
        if decision == "accept":
            accepted.append((candidate, request))

    if len(accepted) != 1:
        raise ValueError("exactly one accepted candidate is required")
    candidate, request = accepted[0]
    if any(candidate["gates"][gate] != "pass" for gate in REQUIRED_GATES):
        raise ValueError("all acceptance gates must pass")
    return {"candidate": candidate, "request": request}


def validate_review_artifact_path(
    review: dict, review_file: Path, project_root: Path
) -> None:
    review_path = review.get("review_path")
    if not _is_non_empty_string(review_path):
        raise ValueError("review review_path must be a non-empty string")
    declared = Path(review_path)
    if not declared.is_absolute():
        declared = project_root / declared
    if declared.resolve() != review_file.resolve(strict=True):
        raise ValueError("review_path does not identify the --review artifact")


def promote_review(
    review: dict,
    request_manifest: dict,
    handoff: dict,
    accepted: dict,
    project_root: Path,
    replace: bool = False,
    accepted_path: Path | None = None,
) -> dict:
    validate_handoff(handoff, project_root)
    source_pack_sha256 = handoff.get("source_turnaround_manifest_sha256")
    if not source_pack_sha256 or any(
        request.get("source_pack_sha256") != source_pack_sha256
        for request in request_manifest.get("requests", [])
    ):
        raise ValueError("request source pack does not match Phase 2 handoff")

    validated = validate_review(review, request_manifest, handoff)
    candidate = validated["candidate"]
    request = validated["request"]
    motion = review["motion"]

    current = validate_accepted_selection(accepted)
    if motion in current:
        if not replace:
            raise ValueError(f"motion already accepted: {motion}")
    elif replace:
        raise ValueError(f"cannot replace unaccepted motion: {motion}")
    else:
        preceding = {
            name
            for name, order in MOTION_ORDER.items()
            if order < MOTION_ORDER[motion]
        }
        missing = sorted(preceding - set(current), key=MOTION_ORDER.get)
        if missing:
            raise ValueError(
                "cannot promote before preceding motion: " + ", ".join(missing)
            )

    source_path = resolve_path(project_root, candidate["candidate_path"])
    if not source_path.is_file():
        raise ValueError(f"missing accepted candidate: {source_path}")
    with Image.open(source_path) as image:
        if image.size != (1024, 1536):
            raise ValueError(f"candidate canvas must be 1024x1536: {source_path}")
        image.load()

    relative_output = Path("source/finished/v1-2-motion") / f"{motion}.webp"
    output_path = resolve_path(project_root, relative_output.as_posix())
    if output_path.exists() and motion not in current and not replace:
        raise ValueError(f"finished output already exists: {output_path}")

    record = {
        "motion": motion,
        "motion_order": MOTION_ORDER[motion],
        "finished_path": relative_output.as_posix(),
        "source_candidate_path": candidate["candidate_path"],
        "request_id": request["id"],
        "batch_id": request["batch_id"],
        "revision": request["revision"],
        "candidate_number": request["candidate_number"],
        "review_id": review["review_id"],
        "review_path": review["review_path"],
        "source_pack_sha256": request["source_pack_sha256"],
        "source_sha256": sha256_file(source_path),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=f".{motion}-",
            suffix=".webp",
            dir=output_path.parent,
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
        with Image.open(source_path) as image:
            image.convert("RGB").save(
                temporary_path,
                "WEBP",
                quality=94,
                method=6,
            )
        record["finished_sha256"] = sha256_file(temporary_path)
        prospective = dict(current)
        prospective[motion] = record
        updated = dict(accepted)
        updated["accepted_motions"] = sorted(
            prospective.values(), key=lambda item: item["motion_order"]
        )
        validate_accepted_selection(updated)
        if accepted_path is None:
            os.replace(temporary_path, output_path)
            fsync_directory(output_path.parent)
        else:
            commit_promotion_transaction(
                temporary_path,
                output_path,
                accepted_path,
                updated,
            )
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return updated


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Promote one reviewed Akari v1.2 motion candidate."
    )
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--requests", type=Path, default=REQUESTS_PATH)
    parser.add_argument("--handoff", type=Path, default=HANDOFF_PATH)
    parser.add_argument("--accepted", type=Path, default=ACCEPTED_PATH)
    parser.add_argument("--replace", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    review_path = args.review if args.review.is_absolute() else ROOT / args.review
    accepted_path = (
        args.accepted if args.accepted.is_absolute() else ROOT / args.accepted
    )
    recover_promotion_transaction(accepted_path)
    review = load_json(review_path)
    validate_review_artifact_path(review, review_path, ROOT)
    updated = promote_review(
        review,
        load_json(args.requests),
        load_json(args.handoff),
        load_json(accepted_path),
        ROOT,
        replace=args.replace,
        accepted_path=accepted_path,
    )
    print(f"accepted motion poses: {len(updated['accepted_motions'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
