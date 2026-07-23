from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path


CANONICAL_SLOTS = (
    "front",
    "character-left-front-three-quarter",
    "character-left-profile",
    "character-left-rear-three-quarter",
    "back",
    "character-right-rear-three-quarter",
    "character-right-profile",
    "character-right-front-three-quarter",
)
MOTION_SLOTS = ("walking", "seated", "turning")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=f".{path.name}-",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
        fsync_directory(path.parent)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_path(project_root: Path, path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else project_root / path


def validate_handoff(handoff: dict, project_root: Path) -> None:
    source_manifest = resolve_path(
        project_root, handoff["source_turnaround_manifest"]
    )
    if (
        not source_manifest.is_file()
        or sha256_file(source_manifest)
        != handoff["source_turnaround_manifest_sha256"]
    ):
        raise ValueError("source turnaround manifest hash drift")

    final_review_path = resolve_path(project_root, handoff["source_final_review"])
    if not final_review_path.is_file():
        raise ValueError("final Phase 1 review is missing")
    final_review = load_json(final_review_path)
    if (
        final_review.get("decision") != "accepted"
        or final_review.get("user_decision") != "approved"
        or final_review.get("source_manifest")
        != handoff["source_turnaround_manifest"]
        or final_review.get("source_manifest_sha256")
        != handoff["source_turnaround_manifest_sha256"]
        or tuple(final_review.get("accepted_slots", ())) != CANONICAL_SLOTS
        or not final_review.get("gate_summary")
        or any(
            result != "pass"
            for result in final_review.get("gate_summary", {}).values()
        )
    ):
        raise ValueError("final Phase 1 review is not current and approved")

    inputs = handoff["turnaround_inputs"]
    if tuple(item["slot"] for item in inputs) != CANONICAL_SLOTS:
        raise ValueError("Phase 2 requires eight canonical turnaround inputs")
    accepted = {
        item["slot"]: item for item in load_json(source_manifest)["accepted_angles"]
    }
    for item in inputs:
        path = resolve_path(project_root, item["accepted_path"])
        if not path.is_file() or sha256_file(path) != item["sha256"]:
            raise ValueError(f"turnaround asset hash drift: {item['slot']}")
        if (
            accepted[item["slot"]]["accepted_path"] != item["accepted_path"]
            or accepted[item["slot"]]["sha256"] != item["sha256"]
        ):
            raise ValueError(
                f"handoff input disagrees with accepted manifest: {item['slot']}"
            )

    slots = handoff["motion_slots"]
    if tuple(slot["slug"] for slot in slots) != MOTION_SLOTS:
        raise ValueError("motion slots must be walking, seated, turning")
    for slot in slots:
        if slot["candidate_count"] != 3 or slot["deliverable_count"] != 1:
            raise ValueError(f"invalid candidate contract: {slot['slug']}")
        if tuple(slot["required_turnaround_slots"]) != CANONICAL_SLOTS:
            raise ValueError(f"incomplete turnaround contract: {slot['slug']}")
