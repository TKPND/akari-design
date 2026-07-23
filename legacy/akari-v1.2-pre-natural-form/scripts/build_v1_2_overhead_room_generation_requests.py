#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from scripts.v1_2_overhead_room_common import (
    COLLECTION_ID,
    POSE_SLOTS,
    dump_json,
    load_json,
    validate_pose_slots,
    validate_reference_pack,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/v1-2-overhead-room"
REFERENCE_PACK_PATH = MANIFEST_DIR / "reference-pack.json"
POSE_MANIFEST_PATH = MANIFEST_DIR / "pose-slots.json"
ACCEPTED_PATH = MANIFEST_DIR / "accepted-selection.json"
OUTPUT_PATH = MANIFEST_DIR / "generation-requests.json"
PROMPT_TEMPLATE_VERSION = "akari_v1_2_overhead_room_v1"
ANCHOR_POSE = POSE_SLOTS[0]

POSE_VARIATIONS = {
    "supine-direct-gaze": (
        "body nearly vertical with one hand over chest",
        "body on a slight diagonal with both hands relaxed near torso",
    ),
    "supine-bent-knees": (
        "both knees raised with a gentle offset",
        "one knee higher with ankles softly crossed",
    ),
    "supine-overhead-stretch": (
        "one arm extended above the head",
        "both arms loosely stretched with asymmetric sleeves",
    ),
    "side-curled-gaze": (
        "knees softly tucked and cheek on a cushion",
        "looser side curl with one hand near the face",
    ),
    "side-reaching-hand": (
        "open hand reaching gently toward camera",
        "sleeved fingers reaching without hiding the face",
    ),
    "prone-chin-on-arms": (
        "chin on crossed forearms with legs extended",
        "chin on stacked hands with lower legs softly offset",
    ),
    "floor-seated-look-up": (
        "relaxed cross-legged seat",
        "soft side-seated pose with one supporting hand",
    ),
    "close-face-hair-spread": (
        "direct gaze with hair fanned evenly",
        "slightly turned face with asymmetric hair spread",
    ),
    "close-upper-body-hands": (
        "phone held loosely against chest with blank screen",
        "closed book held near torso with blank cover",
    ),
    "close-sleeved-reaching-hand": (
        "open sleeved hand near camera",
        "relaxed fingers emerging from oversized cuff",
    ),
}

POSE_SPECIFICATIONS = {
    "supine-direct-gaze": (
        "Lie naturally on the back and return a calm direct gaze. Keep the "
        "complete figure readable from hair to socks, with hands close to the "
        "torso and no suggestive emphasis."
    ),
    "supine-bent-knees": (
        "Lie on the back with both knees bent and gently offset. Preserve clear "
        "pelvis, thigh, knee, calf, and bare-foot connections, and keep the "
        "shorts construction fully readable."
    ),
    "supine-overhead-stretch": (
        "Show a slow natural stretch with believable shoulder rotation, long "
        "sleeve flow, connected arms and hands, and the complete body inside "
        "the frame."
    ),
    "side-curled-gaze": (
        "Use a relaxed side curl with a soft returned gaze. Keep neck, torso, "
        "pelvis, tucked knees, bare feet, and cheek-on-cushion contact coherent."
    ),
    "side-reaching-hand": (
        "Reach one hand gently toward the camera without oversized perspective "
        "or hiding the face. Keep the side-lying body, shorts, legs, and socks "
        "connected."
    ),
    "prone-chin-on-arms": (
        "Rest the chin naturally on the forearms or hands. Preserve shoulders, "
        "elbows, fingers, torso, pelvis, shorts, extended legs, and bare feet "
        "without compression artifacts."
    ),
    "floor-seated-look-up": (
        "Sit naturally on the floor and look straight up. Keep the seated "
        "weight grounded, the torso-to-leg relationship readable, and hands, "
        "shorts, knees, socks, and complete limbs coherent."
    ),
    "close-face-hair-spread": (
        "Frame the face and upper hair from above. Show warm amber eyes, the "
        "complete two-part character-left ornament, natural hair spread, and "
        "a subtle shy expression; do not force feet into frame."
    ),
    "close-upper-body-hands": (
        "Frame the face, upper torso, and both hands. Keep the single prop "
        "secondary, blank, unbranded, and anatomically separated from fingers."
    ),
    "close-sleeved-reaching-hand": (
        "Frame the face, oversized cuff, and gently offered hand. Keep hand "
        "scale restrained, all five fingers coherent, and the face unobscured."
    ),
}

ACCEPTANCE_GATES = [
    "Identity matches the accepted Akari v1.2 face and hair references.",
    "The adult 25-year-old age impression remains consistent.",
    "The requested overhead angle reads clearly.",
    "Face, hands, feet, and body connections are anatomically coherent.",
    "The two-part pale-blue ornament remains on character-left.",
    "The requested roomwear, shorts, and feet treatment are constructed clearly.",
    "Intimacy comes from gaze, expression, and hand distance while staying healthy.",
    "The person remains dominant and the background stays restrained.",
    "No readable text, logos, watermarks, extra digits, or generated artifacts appear.",
    "The image has a distinct and useful role in the ten-work collection.",
]

REFERENCE_SELECTIONS = {
    "supine-direct-gaze": (
        ("identity_face", "identity_face", None, None),
        ("body_front", "turnaround", "slot", "front"),
        (
            "ornament_three_quarter",
            "turnaround",
            "slot",
            "character-left-front-three-quarter",
        ),
        ("pose_structure", "motion", "motion", "seated"),
        ("composition_mood_only", "composition_mood_only", None, None),
    ),
    "supine-bent-knees": (
        ("identity_face", "identity_face", None, None),
        ("body_front", "turnaround", "slot", "front"),
        ("pose_structure", "motion", "motion", "seated"),
        ("composition_mood_only", "composition_mood_only", None, None),
    ),
    "supine-overhead-stretch": (
        ("identity_face", "identity_face", None, None),
        ("body_front", "turnaround", "slot", "front"),
        ("pose_structure", "motion", "motion", "walking"),
        ("composition_mood_only", "composition_mood_only", None, None),
    ),
    "side-curled-gaze": (
        ("identity_face", "identity_face", None, None),
        ("left_profile", "turnaround", "slot", "character-left-profile"),
        ("right_profile", "turnaround", "slot", "character-right-profile"),
        ("pose_structure", "motion", "motion", "seated"),
        ("composition_mood_only", "composition_mood_only", None, None),
    ),
    "side-reaching-hand": (
        ("identity_face", "identity_face", None, None),
        ("left_profile", "turnaround", "slot", "character-left-profile"),
        ("composition_mood_only", "composition_mood_only", None, None),
    ),
    "prone-chin-on-arms": (
        ("identity_face", "identity_face", None, None),
        (
            "left_three_quarter",
            "turnaround",
            "slot",
            "character-left-front-three-quarter",
        ),
        (
            "right_three_quarter",
            "turnaround",
            "slot",
            "character-right-front-three-quarter",
        ),
        ("pose_structure", "motion", "motion", "seated"),
    ),
    "floor-seated-look-up": (
        ("identity_face", "identity_face", None, None),
        ("body_front", "turnaround", "slot", "front"),
        ("pose_structure", "motion", "motion", "seated"),
        ("composition_mood_only", "composition_mood_only", None, None),
    ),
    "close-face-hair-spread": (
        ("identity_face", "identity_face", None, None),
        (
            "left_three_quarter",
            "turnaround",
            "slot",
            "character-left-front-three-quarter",
        ),
        (
            "right_three_quarter",
            "turnaround",
            "slot",
            "character-right-front-three-quarter",
        ),
        ("composition_mood_only", "composition_mood_only", None, None),
    ),
    "close-upper-body-hands": (
        ("identity_face", "identity_face", None, None),
        ("body_front", "turnaround", "slot", "front"),
        ("pose_structure", "motion", "motion", "seated"),
    ),
    "close-sleeved-reaching-hand": (
        ("identity_face", "identity_face", None, None),
        (
            "left_three_quarter",
            "turnaround",
            "slot",
            "character-left-front-three-quarter",
        ),
    ),
}


def _group(reference_pack: dict, role: str) -> dict:
    try:
        return next(
            item
            for item in reference_pack["reference_inputs"]
            if item["role"] == role
        )
    except StopIteration:
        raise ValueError(f"missing reference role: {role}") from None


def _select_asset(
    reference_pack: dict,
    group_role: str,
    selector_key: str | None,
    selector_value: str | None,
) -> dict:
    assets = _group(reference_pack, group_role)["assets"]
    if selector_key is None:
        return assets[0]
    try:
        return next(
            item for item in assets if item.get(selector_key) == selector_value
        )
    except StopIteration:
        if len(assets) == 1:
            return assets[0]
        raise ValueError(
            f"missing {group_role} reference: {selector_key}={selector_value}"
        ) from None


def build_reference_roles(reference_pack: dict, pose: str) -> list[dict]:
    roles = []
    for role, group_role, selector_key, selector_value in REFERENCE_SELECTIONS[pose]:
        asset = _select_asset(
            reference_pack, group_role, selector_key, selector_value
        )
        roles.append(
            {
                "role": role,
                "path": asset["path"],
                "sha256": asset["sha256"],
            }
        )
    return roles


def build_prompt(
    pose: dict,
    variation: str,
    revision: int,
    failure_observations: list[str],
) -> str:
    angle_min, angle_max = pose["angle_degrees"]
    lines = [
        f"Create one finished Akari v1.2 {pose['slug']} portrait.",
        (
            "Identity lock: depict the accepted adult 25-year-old Akari v1.2 "
            "identity with warm amber eyes, a warm-brown short bob, and the "
            "complete two-part pale-blue hair ornament on character-left."
        ),
        (
            "Reference rule: formal face, turnaround, and motion images control "
            "identity, age, anatomy, hair, and construction. The composition "
            "sample is not an identity or wardrobe source."
        ),
        (
            f"Canvas and camera lock: 1024x1536 RGB portrait, directly overhead "
            f"at {angle_min} to {angle_max} degrees, {pose['framing']} framing."
        ),
        (
            f"Wardrobe lock: {pose['outfit']}, feet treatment {pose['feet']}. "
            "The shorts must remain visibly constructed and must not read as "
            "underwear."
        ),
        (
            f"Room lock: {pose['background']}, exactly {pose['prop_count']} "
            "or fewer simple secondary props, person occupying roughly 60 to "
            "80 percent of the composition."
        ),
        (
            "Palette and intimacy lock: white, ivory, pale blue, soft gray, and "
            "warm brown; intimacy comes from gaze, expression, and hand distance, "
            "not sexualized exposure or body emphasis."
        ),
        (
            "No readable text, numbers, clock display, logos, branding, packaging "
            "copy, watermark, border, panel layout, extra limbs, or other characters."
        ),
        f"Candidate variation: {variation}.",
        POSE_SPECIFICATIONS[pose["slug"]],
    ]
    if revision > 1:
        lines.append(
            "Regeneration failure observations to correct: "
            + "; ".join(failure_observations)
            + "."
        )
    return "\n".join(lines)


def build_ready_batch(
    reference_pack: dict,
    pose_manifest: dict,
    pose: str,
    date_prefix: str,
    revision: int,
    failure_observations: list[str],
    collection_anchor: dict | None,
) -> dict:
    if pose not in POSE_VARIATIONS:
        raise ValueError(f"unknown overhead room pose: {pose}")
    if type(revision) is not int or revision < 1:
        raise ValueError("revision must be a positive integer")
    if re.fullmatch(r"[0-9]{8}", date_prefix) is None:
        raise ValueError("date prefix must use YYYYMMDD")
    failure_observations = [item.strip() for item in failure_observations]
    if revision > 1 and (
        not failure_observations or any(not item for item in failure_observations)
    ):
        raise ValueError("regeneration requires failure observations")

    try:
        pose_record = next(
            item for item in pose_manifest["poses"] if item["slug"] == pose
        )
    except StopIteration:
        raise ValueError(f"pose is missing from manifest: {pose}") from None

    if pose != ANCHOR_POSE:
        if (
            not isinstance(collection_anchor, dict)
            or collection_anchor.get("pose") != ANCHOR_POSE
            or not collection_anchor.get("finished_path")
            or not collection_anchor.get("finished_sha256")
        ):
            raise ValueError("non-anchor pose requires the accepted collection anchor")
    else:
        collection_anchor = None

    batch_id = f"batch:v1-2-overhead-room:{date_prefix}:{pose}:r{revision}"
    base_roles = build_reference_roles(reference_pack, pose)
    if collection_anchor is not None:
        base_roles.append(
            {
                "role": "collection_anchor",
                "path": collection_anchor["finished_path"],
                "sha256": collection_anchor["finished_sha256"],
            }
        )

    requests = []
    for candidate_number, variation in enumerate(
        POSE_VARIATIONS[pose], start=1
    ):
        request = {
            "id": (
                f"request:v1-2-overhead-room:{date_prefix}:{pose}:"
                f"r{revision}:c{candidate_number}"
            ),
            "batch_id": batch_id,
            "pose": pose,
            "pose_order": pose_record["pose_order"],
            "framing": pose_record["framing"],
            "angle_degrees": list(pose_record["angle_degrees"]),
            "outfit": pose_record["outfit"],
            "feet": pose_record["feet"],
            "background": pose_record["background"],
            "prop_count": pose_record["prop_count"],
            "revision": revision,
            "candidate_number": candidate_number,
            "variation": variation,
            "reference_roles": [dict(item) for item in base_roles],
            "source_pack_sha256": reference_pack["pack_sha256"],
            "target_path": (
                "source/generated/v1-2-overhead-room/"
                f"{date_prefix}_{pose}_r{revision}_c{candidate_number}.png"
            ),
            "prompt_template_version": PROMPT_TEMPLATE_VERSION,
            "prompt": build_prompt(
                pose_record, variation, revision, failure_observations
            ),
            "acceptance_gates": list(ACCEPTANCE_GATES),
            "review_plan": {
                "initial_status": "draft_candidate",
                "first_pass": "compare both candidates on one pose contact sheet",
                "outcomes": ["accept", "hold", "reject"],
            },
        }
        if collection_anchor is not None:
            request["collection_anchor"] = dict(collection_anchor)
        requests.append(request)

    return {
        "schema_version": 1,
        "collection_id": COLLECTION_ID,
        "prompt_template_version": PROMPT_TEMPLATE_VERSION,
        "active_batches": {pose: batch_id},
        "requests": requests,
    }


def merge_request_history(existing: dict, batch: dict) -> dict:
    if (
        existing.get("schema_version") != 1
        or existing.get("collection_id") != COLLECTION_ID
    ):
        raise ValueError("existing request manifest identity is invalid")
    if batch.get("collection_id") != COLLECTION_ID:
        raise ValueError("request batch collection id is invalid")

    by_id = {item["id"]: item for item in existing.get("requests", [])}
    for request in batch["requests"]:
        current = by_id.get(request["id"])
        if current is not None and current != request:
            raise ValueError(f"conflicting request id: {request['id']}")
        by_id[request["id"]] = request

    active_batches = dict(existing.get("active_batches", {}))
    revisions = {item["batch_id"]: item["revision"] for item in by_id.values()}
    for pose, batch_id in batch["active_batches"].items():
        current_batch = active_batches.get(pose)
        if current_batch is not None and revisions[current_batch] > revisions[batch_id]:
            raise ValueError(f"cannot reactivate older revision for {pose}")
        active_batches[pose] = batch_id

    merged = dict(existing)
    merged["prompt_template_version"] = PROMPT_TEMPLATE_VERSION
    merged["active_batches"] = active_batches
    merged["requests"] = sorted(
        by_id.values(),
        key=lambda item: (
            item["pose_order"],
            item["revision"],
            item["candidate_number"],
            item["id"],
        ),
    )
    return merged


def _collection_anchor(accepted: dict) -> dict | None:
    for record in accepted.get("accepted_works", []):
        if record.get("pose") == ANCHOR_POSE:
            return {
                "pose": record["pose"],
                "finished_path": record["finished_path"],
                "finished_sha256": record["finished_sha256"],
            }
    return None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build append-only Akari overhead-room generation requests."
    )
    parser.add_argument("--pose", choices=POSE_SLOTS, required=True)
    parser.add_argument("--date-prefix", default="20260713")
    parser.add_argument("--revision", type=int, default=1)
    parser.add_argument("--failure-observation", action="append", default=[])
    parser.add_argument("--reference-pack", type=Path, default=REFERENCE_PACK_PATH)
    parser.add_argument("--pose-manifest", type=Path, default=POSE_MANIFEST_PATH)
    parser.add_argument("--accepted", type=Path, default=ACCEPTED_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    return parser.parse_args(argv)


def _rooted(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    reference_pack = load_json(_rooted(args.reference_pack))
    pose_manifest = load_json(_rooted(args.pose_manifest))
    validate_reference_pack(reference_pack, ROOT)
    validate_pose_slots(pose_manifest)

    accepted_path = _rooted(args.accepted)
    accepted = (
        load_json(accepted_path)
        if accepted_path.is_file()
        else {"schema_version": 1, "collection_id": COLLECTION_ID, "accepted_works": []}
    )
    batch = build_ready_batch(
        reference_pack,
        pose_manifest,
        args.pose,
        args.date_prefix,
        args.revision,
        args.failure_observation,
        _collection_anchor(accepted),
    )
    output_path = _rooted(args.output)
    existing = load_json(output_path)
    merged = merge_request_history(existing, batch)
    dump_json(output_path, merged)
    print(f"overhead room requests written: {len(batch['requests'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
