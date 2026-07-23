#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.v1_2_turnaround_common import dump_json, load_json, sha256_file


ROOT = Path(__file__).resolve().parents[1]
ACCEPTED = ROOT / "source/manifests/v1-2-turnaround/accepted-angles.json"
FINAL_REVIEW = (
    ROOT / "evidence/v1-2-turnaround/reviews/final-eight-view-review.json"
)
OUTPUT = ROOT / "source/manifests/v1-2-motion/phase-2-handoff.json"
ACCEPTED_SOURCE = "source/manifests/v1-2-turnaround/accepted-angles.json"
FINAL_REVIEW_SOURCE = (
    "evidence/v1-2-turnaround/reviews/final-eight-view-review.json"
)
CANONICAL_SLOTS = [
    "front",
    "character-left-front-three-quarter",
    "character-left-profile",
    "character-left-rear-three-quarter",
    "back",
    "character-right-rear-three-quarter",
    "character-right-profile",
    "character-right-front-three-quarter",
]
MOTION_SLOTS = [
    {
        "slug": "walking",
        "description": (
            "readable mid-step with traceable leg, clothing, hair, sock, "
            "and sneaker motion"
        ),
    },
    {
        "slug": "seated",
        "description": (
            "natural seated pose with believable proportion, folds, "
            "hands, socks, and footwear"
        ),
    },
    {
        "slug": "turning",
        "description": (
            "over-shoulder or mid-turn pose without flipping the "
            "character-left ornament"
        ),
    },
]


def build_handoff(
    accepted: dict,
    final_review: dict,
    accepted_manifest_sha256: str,
    project_root: Path = ROOT,
    source_turnaround_manifest: str = ACCEPTED_SOURCE,
    source_final_review: str = FINAL_REVIEW_SOURCE,
) -> dict:
    records = accepted["accepted_angles"]
    if [record["slot"] for record in records] != CANONICAL_SLOTS:
        raise ValueError(
            "Phase 2 requires all eight accepted slots in canonical order"
        )
    if final_review.get("decision") != "accepted":
        raise ValueError("Phase 2 requires an accepted final eight-view review")
    if final_review.get("user_decision") != "approved":
        raise ValueError("Phase 2 requires explicit user approval")
    if final_review.get("accepted_slots") != CANONICAL_SLOTS:
        raise ValueError("final review accepted slots do not match Phase 1")
    expected_gates = {
        "identity",
        "geometry",
        "outfit",
        "quality",
        "counterpart_tolerance",
        "back_convergence",
    }
    gate_summary = final_review.get("gate_summary", {})
    if set(gate_summary) != expected_gates or set(gate_summary.values()) != {
        "pass"
    }:
        raise ValueError("Phase 2 requires every final eight-view gate to pass")
    if (
        final_review.get("motion_phase_handoff", {}).get("status")
        != "ready_for_contract_build"
    ):
        raise ValueError("final review is not ready for Phase 2 handoff")
    if final_review.get("source_manifest") != source_turnaround_manifest:
        raise ValueError("final review source manifest does not match input")
    if final_review.get("source_manifest_sha256") != accepted_manifest_sha256:
        raise ValueError("final review is stale for the accepted manifest")
    for record in records:
        expected_path = (
            f"source/finished/v1-2-turnaround/{record['slot']}.webp"
        )
        if record.get("accepted_path") != expected_path:
            raise ValueError(
                f"unexpected accepted path for {record['slot']}: "
                f"{record.get('accepted_path')}"
            )
        asset_path = project_root / expected_path
        if not asset_path.is_file():
            raise ValueError(f"missing accepted asset: {expected_path}")
        if sha256_file(asset_path) != record.get("sha256"):
            raise ValueError(f"accepted asset hash mismatch: {expected_path}")
    inputs = [
        {
            "slot": record["slot"],
            "accepted_path": record["accepted_path"],
            "sha256": record["sha256"],
        }
        for record in records
    ]
    return {
        "schema_version": 1,
        "collection_id": "akari-v1.2-representative-motion-poses",
        "source_turnaround_manifest": source_turnaround_manifest,
        "source_turnaround_manifest_sha256": accepted_manifest_sha256,
        "source_final_review": source_final_review,
        "turnaround_inputs": inputs,
        "motion_slots": [
            {
                **motion,
                "requires_complete_turnaround": True,
                "required_turnaround_slots": CANONICAL_SLOTS,
                "candidate_count": 3,
                "deliverable_count": 1,
            }
            for motion in MOTION_SLOTS
        ],
    }


def source_label(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build Akari v1.2 motion handoff"
    )
    parser.add_argument("--accepted", type=Path, default=ACCEPTED)
    parser.add_argument("--final-review", type=Path, default=FINAL_REVIEW)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args(argv)
    handoff = build_handoff(
        load_json(args.accepted),
        load_json(args.final_review),
        sha256_file(args.accepted),
        project_root=ROOT,
        source_turnaround_manifest=source_label(args.accepted),
        source_final_review=source_label(args.final_review),
    )
    dump_json(args.output, handoff)
    print(f"motion handoff written: {len(handoff['motion_slots'])} slots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
