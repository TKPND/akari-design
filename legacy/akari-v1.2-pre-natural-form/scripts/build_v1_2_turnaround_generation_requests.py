#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.v1_2_turnaround_common import dump_json, load_json, sha256_file


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/v1-2-turnaround"
IDENTITY_LOCK_PATH = MANIFEST_DIR / "identity-lock.json"
SLOT_MANIFEST_PATH = MANIFEST_DIR / "angle-slots.json"
ACCEPTED_ANGLES_PATH = MANIFEST_DIR / "accepted-angles.json"
OUTPUT_PATH = MANIFEST_DIR / "generation-requests.json"
COLLECTION_ID = "akari-v1.2-canonical-turnaround"
PROMPT_TEMPLATE_VERSION = "akari_v1_2_turnaround_adjacent_angle_v1"
FRONT_REFERENCE_ROLES = (
    "face_hair",
    "body_proportion",
    "standard_outfit_front",
    "footwear_sock",
    "sneaker_construction",
)
DEPENDENT_DETAIL_ROLES = (
    "face_hair",
    "footwear_sock",
    "sneaker_construction",
)


def validate_identity_lock(identity_lock: dict, project_root: Path) -> None:
    prerequisite = identity_lock["prerequisite"]
    selection_path = project_root / prerequisite["selection_manifest"]
    if not selection_path.is_file():
        raise ValueError("v1.2 face-and-hair selection manifest is missing")
    selection = load_json(selection_path)
    if sha256_file(selection_path) != prerequisite["selection_manifest_sha256"]:
        raise ValueError("v1.2 face-and-hair selection manifest hash drift")
    if selection.get("decision") != prerequisite["required_status"]:
        raise ValueError("v1.2 face-and-hair selection is not accepted")
    if selection.get("accepted_asset") != prerequisite["accepted_asset"]:
        raise ValueError("accepted face asset does not match identity lock")
    if (
        selection.get("accepted_asset_sha256")
        != prerequisite["accepted_asset_sha256"]
    ):
        raise ValueError("accepted face SHA-256 does not match identity lock")
    if selection.get("identity_rules") != identity_lock["identity_rules"]:
        raise ValueError("accepted face identity rules do not match identity lock")
    accepted_asset = project_root / prerequisite["accepted_asset"]
    if not accepted_asset.is_file():
        raise ValueError("accepted face asset is missing")
    if sha256_file(accepted_asset) != prerequisite["accepted_asset_sha256"]:
        raise ValueError("accepted face asset hash drift")
    for entry in identity_lock["reference_inputs"]:
        path = project_root / entry["path"]
        if not path.is_file():
            raise ValueError(f"missing identity reference: {entry['path']}")


def accepted_by_slot(accepted_manifest: dict) -> dict[str, dict]:
    return {
        record["slot"]: record
        for record in accepted_manifest["accepted_angles"]
    }


def unique_paths(paths: list[str]) -> list[str]:
    return list(dict.fromkeys(paths))


def build_prompt(slot: dict, outfit_lock: dict) -> str:
    return "\n".join(
        [
            (
                "Create one clean full-body Akari v1.2 canonical turnaround "
                f"candidate for {slot['japanese_title']}."
            ),
            (
                "Use every attached reference image as a mandatory identity, body, "
                "outfit, angle, and construction source. Do not generate from prompt "
                "text alone."
            ),
            (
                "Identity lock: use the accepted Akari v1.2 standard face and hair; "
                "warm-brown eyes; short warm-brown bob; adult early-20s Japanese "
                "young woman character design; on character-left preserve the "
                "two-part pale-blue ornament: small crossed X-shaped hairpins above, "
                "compact ribbon-like loop immediately below, and exactly two thin "
                "trailing strands."
            ),
            (
                f"View lock: {slot['view_family']} at {slot['azimuth_degrees']} "
                "degrees from the character's perspective; expected hair ornament "
                f"visibility is {slot['hair_ornament_visibility']}."
            ),
            (
                f"Outfit lock: {outfit_lock['top']}; {outfit_lock['bottom']}; "
                f"{outfit_lock['socks']}; {outfit_lock['shoes']}; no shoulder bag."
            ),
            (
                "Canvas and pose lock: 1024x1536 RGB portrait, neutral standing "
                "pose, matched camera height, shared sole baseline, full body "
                "visible, plain neutral background."
            ),
            (
                "Consistency lock: preserve head-to-body ratio, healthy thigh and "
                "calf volume, shoulder width, hoodie hem, skirt hem, knee height, "
                "ankle shape, and sneaker mass."
            ),
            (
                "No readable text, no logos, no watermarks, no border, no frame, "
                "no panel layout, no mirrored shortcut, no photorealistic "
                "live-action person."
            ),
        ]
    )


def build_acceptance(slot: dict) -> str:
    return " ".join(
        [
            (
                "Identity Gate: must match the accepted Akari v1.2 face, hair, "
                "adult age impression, and character-left ornament."
            ),
            (
                "Geometry Gate: must preserve matched crown, chin, shoulder, "
                "hoodie hem, skirt hem, knee, ankle, and sole relationships."
            ),
            (
                "Outfit Gate: must preserve the standard hoodie, pleated skirt, "
                "striped socks, and sneaker construction."
            ),
            (
                f"Orientation Gate: must read as {slot['japanese_title']} without "
                "mirroring or side-label ambiguity."
            ),
            (
                "Quality Gate: clean anatomy and clothing continuity; no text, "
                "logo, watermark, frame, border, or panel layout."
            ),
        ]
    )


def build_ready_batch(
    slot_manifest: dict,
    identity_lock: dict,
    accepted_manifest: dict,
    requested_slots: list[str],
    date_prefix: str,
    revision: int,
) -> dict:
    if revision < 1:
        raise ValueError("revision must be a positive integer")
    slots = {slot["slug"]: slot for slot in slot_manifest["slots"]}
    accepted = accepted_by_slot(accepted_manifest)
    role_paths = {
        entry["role"]: entry["path"]
        for entry in identity_lock["reference_inputs"]
    }
    requests = []
    active_batches = {}
    for requested_slot in requested_slots:
        if requested_slot not in slots:
            raise ValueError(f"unknown turnaround slot: {requested_slot}")
        slot = slots[requested_slot]
        upstream_paths = []
        for upstream_slot in slot["upstream_slots"]:
            if upstream_slot not in accepted:
                raise ValueError(
                    f"{requested_slot} requires accepted slot {upstream_slot}"
                )
            upstream_paths.append(accepted[upstream_slot]["accepted_path"])
        legacy_paths = [
            role_paths[role] for role in slot["legacy_reference_roles"]
        ]
        if slot["upstream_slots"]:
            reference_paths = unique_paths(
                [role_paths["face_hair"]] + upstream_paths + legacy_paths
            )
            for role in DEPENDENT_DETAIL_ROLES:
                path = role_paths[role]
                if path not in reference_paths and len(reference_paths) < 5:
                    reference_paths.append(path)
        else:
            reference_paths = unique_paths(
                [role_paths[role] for role in FRONT_REFERENCE_ROLES]
                + legacy_paths
            )
        if len(reference_paths) > 5:
            raise ValueError(
                f"{requested_slot} exceeds the five-image generation reference limit"
            )
        batch_id = (
            f"batch:v1-2-turnaround:{date_prefix}:{requested_slot}:r{revision}"
        )
        active_batches[requested_slot] = batch_id
        for candidate_number in range(1, slot["candidate_count"] + 1):
            requests.append(
                {
                    "id": (
                        f"request:v1-2-turnaround:{date_prefix}:{requested_slot}:"
                        f"r{revision}:c{candidate_number}"
                    ),
                    "batch_id": batch_id,
                    "revision": revision,
                    "slot": requested_slot,
                    "angle_order": slot["angle_order"],
                    "candidate_number": candidate_number,
                    "japanese_title": slot["japanese_title"],
                    "side": slot["side"],
                    "azimuth_degrees": slot["azimuth_degrees"],
                    "view_family": slot["view_family"],
                    "required_upstream_slots": slot["upstream_slots"],
                    "reference_pack_inputs": reference_paths,
                    "target_path": (
                        "source/generated/v1-2-turnaround/"
                        f"{date_prefix}_{requested_slot}_r{revision}_"
                        f"c{candidate_number}.png"
                    ),
                    "prompt_template_version": PROMPT_TEMPLATE_VERSION,
                    "prompt": build_prompt(slot, identity_lock["outfit_lock"]),
                    "acceptance": build_acceptance(slot),
                    "review_plan": {
                        "initial_status": "draft_candidate",
                        "first_pass": (
                            "compare all three candidates on one stage contact sheet"
                        ),
                        "outcomes": ["accept", "hold", "reject"],
                    },
                }
            )
    return {
        "schema_version": 1,
        "collection_id": COLLECTION_ID,
        "prompt_template_version": PROMPT_TEMPLATE_VERSION,
        "active_batches": active_batches,
        "requests": requests,
    }


def merge_request_history(existing: dict, batch: dict) -> dict:
    by_id = {request["id"]: request for request in existing["requests"]}
    for request in batch["requests"]:
        current = by_id.get(request["id"])
        if current is not None and current != request:
            raise ValueError(f"conflicting request id: {request['id']}")
        by_id[request["id"]] = request
    merged = dict(existing)
    merged["requests"] = sorted(
        by_id.values(),
        key=lambda item: (
            item["angle_order"],
            item["revision"],
            item["candidate_number"],
            item["id"],
        ),
    )
    active_batches = dict(existing.get("active_batches", {}))
    revisions_by_batch = {
        request["batch_id"]: request["revision"]
        for request in by_id.values()
    }
    for slot_name, batch_id in batch["active_batches"].items():
        current_batch = active_batches.get(slot_name)
        if (
            current_batch is not None
            and revisions_by_batch[current_batch] > revisions_by_batch[batch_id]
        ):
            raise ValueError(f"cannot reactivate older revision for {slot_name}")
    active_batches.update(batch["active_batches"])
    merged["active_batches"] = active_batches
    return merged


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build dependency-ready Akari v1.2 turnaround requests."
    )
    parser.add_argument("--slot", action="append", required=True)
    parser.add_argument("--date-prefix", default="20260710")
    parser.add_argument("--revision", type=int, default=1)
    parser.add_argument("--identity-lock", type=Path, default=IDENTITY_LOCK_PATH)
    parser.add_argument("--slots", type=Path, default=SLOT_MANIFEST_PATH)
    parser.add_argument("--accepted", type=Path, default=ACCEPTED_ANGLES_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    identity_lock = load_json(args.identity_lock)
    validate_identity_lock(identity_lock, ROOT)
    batch = build_ready_batch(
        load_json(args.slots),
        identity_lock,
        load_json(args.accepted),
        args.slot,
        args.date_prefix,
        args.revision,
    )
    existing = load_json(args.output)
    merged = merge_request_history(existing, batch)
    dump_json(args.output, merged)
    print(f"turnaround requests written: {len(batch['requests'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
