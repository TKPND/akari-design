#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from scripts.build_v1_2_turnaround_contact_sheet import (
    validate_landmark_ratios,
)
from scripts.v1_2_turnaround_common import (
    dump_json,
    load_json,
    normalize_landmarks,
    resolve_path,
    sha256_file,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/v1-2-turnaround"
SLOT_MANIFEST_PATH = MANIFEST_DIR / "angle-slots.json"
REQUESTS_PATH = MANIFEST_DIR / "generation-requests.json"
ACCEPTED_PATH = MANIFEST_DIR / "accepted-angles.json"
REQUIRED_GATES = {"identity", "geometry", "outfit", "quality"}
ALLOWED_STATES = {"accept", "hold", "reject"}


def validate_review(
    review: dict,
    slot_manifest: dict,
    request_manifest: dict,
    accepted_manifest: dict,
) -> None:
    if review.get("user_decision") != "approved":
        raise ValueError("review is not user-approved")
    slots = {slot["slug"]: slot for slot in slot_manifest["slots"]}
    requests = {
        request["id"]: request for request in request_manifest["requests"]
    }
    accepted_slots = {
        record["slot"] for record in accepted_manifest["accepted_angles"]
    }
    reviewed_slots = set(review["slots"])
    candidate_slots = {
        candidate["slot"] for candidate in review["candidates"]
    }
    if candidate_slots != reviewed_slots:
        raise ValueError("review slots do not match candidate slots")
    request_batches = review.get("request_batches", {})
    if set(request_batches) != reviewed_slots:
        raise ValueError("review must name one active request batch per slot")
    for slot_name, batch_id in request_batches.items():
        if request_manifest.get("active_batches", {}).get(slot_name) != batch_id:
            raise ValueError(f"review does not use the active batch for {slot_name}")
    expected_request_ids = {
        request["id"]
        for request in request_manifest["requests"]
        if request["slot"] in reviewed_slots
        and request["batch_id"] == request_batches[request["slot"]]
    }
    reviewed_request_ids = [
        candidate["request_id"] for candidate in review["candidates"]
    ]
    if (
        len(reviewed_request_ids) != len(expected_request_ids)
        or set(reviewed_request_ids) != expected_request_ids
    ):
        raise ValueError(
            "review must cover every materialized candidate in the stage"
        )
    for candidate in review["candidates"]:
        if candidate["state"] not in ALLOWED_STATES:
            raise ValueError(f"invalid candidate state: {candidate['state']}")
        if candidate["request_id"] not in requests:
            raise ValueError(f"unknown request id: {candidate['request_id']}")
        request = requests[candidate["request_id"]]
        if request["slot"] != candidate["slot"]:
            raise ValueError("review slot does not match request slot")
        if request["batch_id"] != request_batches[candidate["slot"]]:
            raise ValueError(
                "review candidate does not belong to the active batch"
            )
        if request["target_path"] != candidate["candidate_path"]:
            raise ValueError("review candidate path does not match request target")
        if (
            candidate["state"] == "reject"
            and not candidate["rejection_reason"].strip()
        ):
            raise ValueError("rejected candidate requires rejection_reason")
        if not candidate["notes"].strip():
            raise ValueError("candidate notes must be concrete and non-empty")
    for slot_name in reviewed_slots:
        if slot_name not in slots:
            raise ValueError(f"unknown reviewed slot: {slot_name}")
        accepted_candidates = [
            candidate
            for candidate in review["candidates"]
            if candidate["slot"] == slot_name
            and candidate["state"] == "accept"
        ]
        if len(accepted_candidates) != 1:
            raise ValueError(
                f"exactly one accepted candidate for {slot_name} is required"
            )
        candidate = accepted_candidates[0]
        if set(candidate["gates"]) != REQUIRED_GATES:
            raise ValueError(f"gate keys are incomplete for {slot_name}")
        if set(candidate["gates"].values()) != {"pass"}:
            raise ValueError(f"all gates must pass for {slot_name}")
        normalized = normalize_landmarks(candidate["landmark_y_px"])
        if normalized != candidate["normalized_landmarks"]:
            raise ValueError(
                f"normalized landmarks do not match pixels for {slot_name}"
            )
        for upstream_slot in slots[slot_name]["upstream_slots"]:
            if upstream_slot not in accepted_slots:
                raise ValueError(
                    f"{slot_name} requires accepted slot {upstream_slot}"
                )


def promote_review(
    review: dict,
    slot_manifest: dict,
    request_manifest: dict,
    accepted_manifest: dict,
    project_root: Path,
) -> dict:
    validate_review(
        review,
        slot_manifest,
        request_manifest,
        accepted_manifest,
    )
    slots = {slot["slug"]: slot for slot in slot_manifest["slots"]}
    requests = {
        request["id"]: request for request in request_manifest["requests"]
    }
    current = {
        record["slot"]: record
        for record in accepted_manifest["accepted_angles"]
    }
    proposed = {}
    reviewed_slots = {
        candidate["slot"] for candidate in review["candidates"]
    }
    for slot_name in reviewed_slots:
        if slot_name in current:
            raise ValueError(f"slot already accepted: {slot_name}")
        candidate = next(
            candidate
            for candidate in review["candidates"]
            if candidate["slot"] == slot_name
            and candidate["state"] == "accept"
        )
        source = resolve_path(project_root, candidate["candidate_path"])
        if not source.is_file():
            raise ValueError(f"missing accepted candidate: {source}")
        with Image.open(source) as image:
            if image.size != (1024, 1536):
                raise ValueError(
                    f"candidate canvas must be 1024x1536: {source}"
                )
        relative_output = (
            Path("source/finished/v1-2-turnaround") / f"{slot_name}.webp"
        )
        slot = slots[slot_name]
        request = requests[candidate["request_id"]]
        proposed[slot_name] = {
            "slot": slot_name,
            "angle_order": slot["angle_order"],
            "japanese_title": slot["japanese_title"],
            "accepted_path": relative_output.as_posix(),
            "source_candidate_path": candidate["candidate_path"],
            "request_id": candidate["request_id"],
            "batch_id": request["batch_id"],
            "revision": request["revision"],
            "candidate_number": request["candidate_number"],
            "review_id": review["review_id"],
            "review_path": review["review_path"],
            "landmark_y_px": candidate["landmark_y_px"],
            "normalized_landmarks": candidate["normalized_landmarks"],
        }
    hypothetical = list(current.values()) + list(proposed.values())
    errors = validate_landmark_ratios(hypothetical)
    if errors:
        raise ValueError("landmark validation failed: " + "; ".join(errors))
    for slot_name, record in proposed.items():
        source = resolve_path(project_root, record["source_candidate_path"])
        output = resolve_path(project_root, record["accepted_path"])
        output.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source) as image:
            image.convert("RGB").save(
                output,
                "WEBP",
                quality=94,
                method=6,
            )
        record["sha256"] = sha256_file(output)
        current[slot_name] = record
    updated = dict(accepted_manifest)
    updated["accepted_angles"] = sorted(
        current.values(),
        key=lambda record: record["angle_order"],
    )
    remaining_queue = [
        slot_name
        for slot_name in accepted_manifest.get("regeneration_queue", [])
        if slot_name not in proposed
    ]
    if remaining_queue:
        updated["regeneration_queue"] = remaining_queue
    else:
        updated.pop("regeneration_queue", None)
    return updated


def reopen_slots(
    review: dict,
    slot_manifest: dict,
    accepted_manifest: dict,
    project_root: Path,
) -> dict:
    if review.get("user_decision") != "reopen":
        raise ValueError("reopen review is not user-approved")
    if not review.get("reason", "").strip():
        raise ValueError("reopen review requires a concrete reason")
    current = {
        record["slot"]: record
        for record in accepted_manifest["accepted_angles"]
    }
    slots = {slot["slug"]: slot for slot in slot_manifest["slots"]}
    requested = set(review["slots"])
    unknown = requested - set(slots)
    if unknown:
        raise ValueError(f"unknown reopen slots: {sorted(unknown)}")
    unaccepted = requested - set(current)
    if unaccepted:
        raise ValueError(f"cannot reopen unaccepted slots: {sorted(unaccepted)}")
    reopened = set(requested)
    changed = True
    while changed:
        changed = False
        for slot_name in current:
            if slot_name in reopened:
                continue
            if any(
                upstream in reopened
                for upstream in slots[slot_name]["upstream_slots"]
            ):
                reopened.add(slot_name)
                changed = True
    expected_root = project_root / "source/finished/v1-2-turnaround"
    removals = []
    for slot_name in reopened:
        record = current[slot_name]
        finished = resolve_path(project_root, record["accepted_path"])
        if finished.parent != expected_root:
            raise ValueError(f"refusing to remove unexpected path: {finished}")
        removals.append((slot_name, finished))
    for slot_name, finished in removals:
        current.pop(slot_name)
        finished.unlink(missing_ok=True)
    remaining = set(reopened)
    regeneration_queue = []
    while remaining:
        ready = sorted(
            (
                slot_name
                for slot_name in remaining
                if not (
                    set(slots[slot_name]["upstream_slots"]) & remaining
                )
            ),
            key=lambda slot_name: slots[slot_name]["angle_order"],
        )
        if not ready:
            raise ValueError("turnaround dependency graph contains a cycle")
        regeneration_queue.extend(ready)
        remaining.difference_update(ready)
    updated = dict(accepted_manifest)
    updated["accepted_angles"] = sorted(
        current.values(),
        key=lambda record: record["angle_order"],
    )
    updated["regeneration_queue"] = regeneration_queue
    return updated


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Promote reviewed Akari v1.2 turnaround candidates."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--review", type=Path)
    mode.add_argument("--reopen-review", type=Path)
    parser.add_argument("--slots", type=Path, default=SLOT_MANIFEST_PATH)
    parser.add_argument("--requests", type=Path, default=REQUESTS_PATH)
    parser.add_argument("--accepted", type=Path, default=ACCEPTED_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    review_arg = args.review or args.reopen_review
    review_path = review_arg if review_arg.is_absolute() else ROOT / review_arg
    if args.review:
        updated = promote_review(
            load_json(review_path),
            load_json(args.slots),
            load_json(args.requests),
            load_json(args.accepted),
            ROOT,
        )
    else:
        updated = reopen_slots(
            load_json(review_path),
            load_json(args.slots),
            load_json(args.accepted),
            ROOT,
        )
    dump_json(args.accepted, updated)
    print(f"accepted turnaround angles: {len(updated['accepted_angles'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
