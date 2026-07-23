from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from scripts.v1_2_motion_common import (
    dump_json,
    load_json,
    resolve_path,
    sha256_file,
)


COLLECTION_ID = "akari-v1.2-overhead-room-portraits"
POSE_SLOTS = (
    "supine-direct-gaze",
    "supine-bent-knees",
    "supine-overhead-stretch",
    "side-curled-gaze",
    "side-reaching-hand",
    "prone-chin-on-arms",
    "floor-seated-look-up",
    "close-face-hair-spread",
    "close-upper-body-hands",
    "close-sleeved-reaching-hand",
)
FULL_SLOTS = POSE_SLOTS[:7]
CLOSE_SLOTS = POSE_SLOTS[7:]
REFERENCE_ROLES = (
    "identity_face",
    "turnaround",
    "motion",
    "composition_mood_only",
)
REFERENCE_COUNTS = {
    "identity_face": 1,
    "turnaround": 8,
    "motion": 3,
    "composition_mood_only": 1,
}


def reference_pack_fingerprint(pack: dict) -> str:
    payload = {key: value for key, value in pack.items() if key != "pack_sha256"}
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_pose_slots(manifest: dict) -> None:
    if (
        type(manifest.get("schema_version")) is not int
        or manifest["schema_version"] != 1
        or manifest.get("collection_id") != COLLECTION_ID
    ):
        raise ValueError("invalid overhead room pose manifest identity")

    poses = manifest.get("poses")
    if (
        not isinstance(poses, list)
        or tuple(item.get("slug") for item in poses) != POSE_SLOTS
    ):
        raise ValueError("overhead room poses must match the ten canonical slots")

    for order, pose in enumerate(poses, 1):
        expected_framing = "full" if pose["slug"] in FULL_SLOTS else "close"
        expected_range = [80, 90] if expected_framing == "full" else [65, 80]
        if (
            type(pose.get("pose_order")) is not int
            or pose["pose_order"] != order
            or not isinstance(pose.get("title"), str)
            or not pose["title"].strip()
            or pose.get("framing") != expected_framing
            or pose.get("angle_degrees") != expected_range
            or type(pose.get("candidate_count")) is not int
            or pose["candidate_count"] != 2
            or type(pose.get("deliverable_count")) is not int
            or pose["deliverable_count"] != 1
            or pose.get("outfit")
            not in {"oversized-hoodie-shorts", "loose-tshirt-shorts"}
            or pose.get("feet")
            not in {"striped-socks", "barefoot", "not-visible"}
            or (
                expected_framing == "full"
                and pose.get("feet") == "not-visible"
            )
            or pose.get("background")
            not in {"ivory-rug", "pale-bedding", "gray-blanket"}
            or type(pose.get("prop_count")) is not int
            or not 0 <= pose["prop_count"] <= 3
        ):
            raise ValueError(f"invalid pose contract: {pose.get('slug')}")

    full_poses = poses[:7]
    if sum(pose["feet"] == "striped-socks" for pose in full_poses) != 4:
        raise ValueError("full poses must include four striped-socks works")
    if sum(pose["feet"] == "barefoot" for pose in full_poses) != 3:
        raise ValueError("full poses must include three barefoot works")
    if any(pose["feet"] != "not-visible" for pose in poses[7:]):
        raise ValueError("close poses must not force feet into frame")
    if sum(pose["outfit"] == "oversized-hoodie-shorts" for pose in poses) != 5:
        raise ValueError("pose set must include five hoodie works")
    if sum(pose["outfit"] == "loose-tshirt-shorts" for pose in poses) != 5:
        raise ValueError("pose set must include five T-shirt works")


def _validate_hash(value: object, label: str) -> None:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise ValueError(f"invalid SHA-256: {label}")


def validate_reference_pack(pack: dict, project_root: Path) -> None:
    if (
        type(pack.get("schema_version")) is not int
        or pack["schema_version"] != 1
        or pack.get("collection_id") != COLLECTION_ID
    ):
        raise ValueError("invalid overhead room reference pack identity")
    _validate_hash(pack.get("pack_sha256"), "reference pack")

    source_manifests = pack.get("source_manifests")
    if (
        not isinstance(source_manifests, list)
        or tuple(item.get("role") for item in source_manifests)
        != REFERENCE_ROLES[:3]
    ):
        raise ValueError("source manifest roles are incomplete")
    for record in source_manifests:
        _validate_hash(record.get("sha256"), record.get("role", "manifest"))
        path = resolve_path(project_root, record["path"])
        if not path.is_file() or sha256_file(path) != record["sha256"]:
            raise ValueError(f"source manifest hash drift: {record['role']}")

    references = pack.get("reference_inputs")
    if (
        not isinstance(references, list)
        or tuple(item.get("role") for item in references) != REFERENCE_ROLES
    ):
        raise ValueError("reference pack roles are incomplete")
    for record in references:
        assets = record.get("assets")
        if (
            not isinstance(assets, list)
            or len(assets) != REFERENCE_COUNTS[record["role"]]
        ):
            raise ValueError(f"invalid reference count: {record['role']}")
        for asset in assets:
            _validate_hash(asset.get("sha256"), asset.get("path", "asset"))
            path = resolve_path(project_root, asset["path"])
            if not path.is_file() or sha256_file(path) != asset["sha256"]:
                raise ValueError(f"reference asset hash drift: {asset['path']}")
        if record["role"] == "composition_mood_only":
            if record.get("identity_source") is not False:
                raise ValueError(
                    "composition reference must not be an identity source"
                )
        elif record.get("identity_source") is not True:
            raise ValueError(f"formal reference must lock identity: {record['role']}")

    if pack["pack_sha256"] != reference_pack_fingerprint(pack):
        raise ValueError("reference pack fingerprint drift")


__all__ = [
    "CLOSE_SLOTS",
    "COLLECTION_ID",
    "FULL_SLOTS",
    "POSE_SLOTS",
    "dump_json",
    "load_json",
    "reference_pack_fingerprint",
    "resolve_path",
    "sha256_file",
    "validate_pose_slots",
    "validate_reference_pack",
]
