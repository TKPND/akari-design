#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.v1_2_motion_common import (
    dump_json,
    load_json,
    validate_handoff,
)


ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = ROOT / "source/manifests/v1-2-motion/phase-2-handoff.json"
OUTPUT_PATH = ROOT / "source/manifests/v1-2-motion/generation-requests.json"
PROMPT_TEMPLATE_VERSION = "akari_v1_2_representative_motion_v1"
MOTION_ORDER = {"walking": 1, "seated": 2, "turning": 3}
POSE_VARIATIONS = {
    "walking": (
        "heel-strike with modest stride and opposite arm swing",
        "mid-stance with compact stride and relaxed arms",
        "toe-off with restrained garment and hair follow-through",
    ),
    "seated": (
        "knees offset left, hands near knees, upright torso",
        "feet offset right, hands beside body, slight forward inclination",
        "asymmetric feet, one hand near knee and one beside body",
    ),
    "turning": (
        "early mid-turn with gaze leading shoulders",
        "over-shoulder moment with hips lagging",
        "later turn with restrained hair and hoodie follow-through",
    ),
}

MOTION_SPECIFICATIONS = {
    "walking": (
        "Walking specification: show a readable mid-step with one leg forward "
        "and the other behind. Keep both feet and their relationship to the "
        "ground understandable, with modest arm swing and restrained hoodie, "
        "skirt, and hair follow-through. Keep thighs, knees, calves, socks, and "
        "sneakers traceable and unobscured by skirt or crop."
    ),
    "seated": (
        "Seated specification: show a natural seated reference pose on an "
        "implied, invisible support plane without rendering a chair, backrest, "
        "or prop. Balance pelvis, torso, and feet as though a stable seat is "
        "present; offset knees and feet for leg readability; place hands "
        "naturally near the knees or beside the body; preserve believable folds, "
        "skirt placement, hand anatomy, socks, and complete footwear."
    ),
    "turning": (
        "Turning specification: show a natural over-shoulder or mid-turn moment "
        "derived from standing or walking. Use a believable difference between "
        "face, shoulder, and hip rotation without an extreme spinal twist. "
        "Connect the accepted front, profile, rear-three-quarter, and back "
        "construction without mirroring the character-left hair ornament."
    ),
}

ACCEPTANCE_GATES = [
    "Identity matches the accepted v1.2 face and hair lock.",
    "Age impression remains consistent with the accepted character reference.",
    "Anatomy and pose are coherent and immediately readable.",
    "Body proportion remains consistent with the accepted turnaround.",
    "Hoodie, skirt, socks, and sneakers retain their construction and palette.",
    "The pale-blue ornament remains on the character-left side.",
    "The entire figure is framed cleanly without clipped hair, hands, or shoes.",
    (
        "No extra limbs, merged anatomy, malformed hands or feet, text, or image "
        "artifacts are present."
    ),
    (
        "Weight, balance, garment response, and hair response make the named "
        "motion feel natural."
    ),
    (
        "The candidate is strong enough to serve as a reusable character "
        "reference, not merely the safest surviving image."
    ),
]


def build_prompt(
    motion: str, variation: str, revision: int, failure_observations: list[str]
) -> str:
    lines = [
        f"Create one clean full-body Akari v1.2 {motion} motion candidate.",
        (
            "Use all eight attached reference images as mandatory identity, age, "
            "body, outfit, footwear, hair, and construction sources; do not omit "
            "or replace any reference and do not generate from prompt text alone."
        ),
        (
            "Identity and age lock: preserve the accepted adult Akari v1.2 "
            "identity and age impression, face, warm-brown bob and eyes, body "
            "proportions, and the pale-blue hair ornament on character-left."
        ),
        (
            "Outfit and footwear lock: standard white oversized hoodie, gray "
            "pleated skirt, striped crew socks, and chunky white-and-blue sneakers."
        ),
        (
            "Canvas and framing lock: full body including all hair, both hands, "
            "and both shoes inside a 1024x1536 RGB portrait; plain light "
            "background; restrained perspective; no dramatic foreshortening or "
            "camera tilt."
        ),
        (
            "Exclusions: no props, other characters, scenery, text, logos, "
            "watermarks, labels, borders, frames, or panel layouts."
        ),
        f"Candidate variation: {variation}.",
        MOTION_SPECIFICATIONS[motion],
    ]
    if revision > 1:
        lines.append(
            "Regeneration failure observations to correct: "
            + "; ".join(failure_observations)
            + "."
        )
    return "\n".join(lines)


def build_ready_batch(
    handoff: dict,
    motion: str,
    date_prefix: str,
    revision: int,
    failure_observations: list[str],
) -> dict:
    if revision < 1:
        raise ValueError("revision must be a positive integer")
    if motion not in MOTION_ORDER:
        raise ValueError(f"unknown motion: {motion}")
    failure_observations = [
        observation.strip() for observation in failure_observations
    ]
    if revision > 1 and (
        not failure_observations or any(not item for item in failure_observations)
    ):
        raise ValueError("regeneration requires failure observations")

    slots = {slot["slug"]: slot for slot in handoff["motion_slots"]}
    if motion not in slots:
        raise ValueError(f"motion is missing from handoff: {motion}")
    slot = slots[motion]
    variations = POSE_VARIATIONS[motion]
    if slot["candidate_count"] != len(variations):
        raise ValueError(f"invalid candidate contract: {motion}")

    batch_id = f"batch:v1-2-motion:{date_prefix}:{motion}:r{revision}"
    references = [item["accepted_path"] for item in handoff["turnaround_inputs"]]
    requests = []
    for candidate_number, variation in enumerate(variations, start=1):
        requests.append(
            {
                "id": (
                    f"request:v1-2-motion:{date_prefix}:{motion}:"
                    f"r{revision}:c{candidate_number}"
                ),
                "batch_id": batch_id,
                "motion_order": MOTION_ORDER[motion],
                "motion": motion,
                "revision": revision,
                "candidate_number": candidate_number,
                "variation": variation,
                "reference_pack_inputs": references,
                "source_pack_sha256": handoff[
                    "source_turnaround_manifest_sha256"
                ],
                "target_path": (
                    "source/generated/v1-2-motion/"
                    f"{date_prefix}_{motion}_r{revision}_c{candidate_number}.png"
                ),
                "prompt_template_version": PROMPT_TEMPLATE_VERSION,
                "prompt": build_prompt(
                    motion, variation, revision, failure_observations
                ),
                "acceptance_gates": list(ACCEPTANCE_GATES),
                "review_plan": {
                    "initial_status": "draft_candidate",
                    "first_pass": (
                        "compare all three candidates on one motion contact sheet"
                    ),
                    "outcomes": ["accept", "hold", "reject"],
                },
            }
        )
    return {
        "schema_version": 1,
        "collection_id": handoff["collection_id"],
        "prompt_template_version": PROMPT_TEMPLATE_VERSION,
        "active_batches": {motion: batch_id},
        "requests": requests,
    }


def merge_request_history(existing: dict, batch: dict) -> dict:
    existing_motions = {
        request["motion"] for request in existing["requests"]
    }
    by_id = {request["id"]: request for request in existing["requests"]}
    for request in batch["requests"]:
        current = by_id.get(request["id"])
        if current is not None and current != request:
            raise ValueError(f"conflicting request id: {request['id']}")
        by_id[request["id"]] = request

    for motion in batch["active_batches"]:
        if motion in existing_motions:
            continue
        preceding = {
            name
            for name, order in MOTION_ORDER.items()
            if order < MOTION_ORDER[motion]
        }
        missing = sorted(preceding - existing_motions, key=MOTION_ORDER.get)
        if missing:
            raise ValueError(
                f"cannot activate {motion} before preceding motion: "
                + ", ".join(missing)
            )

    merged = dict(existing)
    merged["requests"] = sorted(
        by_id.values(),
        key=lambda item: (
            item["motion_order"],
            item["revision"],
            item["candidate_number"],
            item["id"],
        ),
    )
    active_batches = dict(existing.get("active_batches", {}))
    revisions_by_batch = {
        request["batch_id"]: request["revision"] for request in by_id.values()
    }
    for motion, batch_id in batch["active_batches"].items():
        current_batch = active_batches.get(motion)
        if (
            current_batch is not None
            and revisions_by_batch[current_batch] > revisions_by_batch[batch_id]
        ):
            raise ValueError(f"cannot reactivate older revision for {motion}")
    active_batches.update(batch["active_batches"])
    merged["active_batches"] = active_batches
    return merged


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build append-only Akari v1.2 motion generation requests."
    )
    parser.add_argument("--motion", choices=tuple(MOTION_ORDER), required=True)
    parser.add_argument("--date-prefix", default="20260713")
    parser.add_argument("--revision", type=int, default=1)
    parser.add_argument("--failure-observation", action="append", default=[])
    parser.add_argument("--handoff", type=Path, default=HANDOFF_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    handoff = load_json(args.handoff)
    validate_handoff(handoff, ROOT)
    batch = build_ready_batch(
        handoff,
        args.motion,
        args.date_prefix,
        args.revision,
        args.failure_observation,
    )
    existing = load_json(args.output)
    merged = merge_request_history(existing, batch)
    dump_json(args.output, merged)
    print(f"motion requests written: {len(batch['requests'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
