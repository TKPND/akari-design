#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.v1_2_overhead_room_common import (
    COLLECTION_ID,
    dump_json,
    load_json,
    reference_pack_fingerprint,
    resolve_path,
    sha256_file,
    validate_reference_pack,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "source/manifests/v1-2-overhead-room/reference-pack.json"
COMPOSITION_PATH = (
    ROOT
    / "source/references/v1-2-overhead-room/overhead-composition-sample.webp"
)
SOURCE_MANIFESTS = {
    "identity_face": (
        "source/manifests/v1-2-face-hair/accepted-selection.json"
    ),
    "turnaround": "source/manifests/v1-2-turnaround/accepted-angles.json",
    "motion": "source/manifests/v1-2-motion/accepted-selection.json",
}
ALLOWED_COMPOSITION_USES = [
    "camera angle",
    "distance",
    "negative space",
    "soft light",
    "pale palette",
]


def _asset(path: str, sha256: str, **metadata: object) -> dict:
    return {"path": path, "sha256": sha256, **metadata}


def build_reference_pack(
    project_root: Path, composition_path: Path
) -> dict:
    composition_path = resolve_path(project_root, composition_path.as_posix())
    if not composition_path.is_file():
        raise ValueError(f"composition reference is missing: {composition_path}")

    source_manifests = []
    loaded = {}
    for role, relative_path in SOURCE_MANIFESTS.items():
        path = project_root / relative_path
        if not path.is_file():
            raise ValueError(f"source manifest is missing: {relative_path}")
        source_manifests.append(
            {"role": role, "path": relative_path, "sha256": sha256_file(path)}
        )
        loaded[role] = load_json(path)

    face = loaded["identity_face"]
    if face.get("decision") != "accepted":
        raise ValueError("face selection is not accepted")
    face_path = face["accepted_asset"]
    face_sha256 = face["accepted_asset_sha256"]

    turnaround_assets = [
        _asset(
            item["accepted_path"],
            item["sha256"],
            slot=item["slot"],
            order=item["angle_order"],
        )
        for item in loaded["turnaround"]["accepted_angles"]
    ]
    motion_assets = [
        _asset(
            item["finished_path"],
            item["finished_sha256"],
            motion=item["motion"],
            order=item["motion_order"],
        )
        for item in loaded["motion"]["accepted_motions"]
    ]

    try:
        composition_relative = composition_path.relative_to(project_root).as_posix()
    except ValueError:
        composition_relative = composition_path.as_posix()

    pack = {
        "schema_version": 1,
        "collection_id": COLLECTION_ID,
        "source_manifests": source_manifests,
        "reference_inputs": [
            {
                "role": "identity_face",
                "identity_source": True,
                "assets": [_asset(face_path, face_sha256)],
            },
            {
                "role": "turnaround",
                "identity_source": True,
                "assets": turnaround_assets,
            },
            {
                "role": "motion",
                "identity_source": True,
                "assets": motion_assets,
            },
            {
                "role": "composition_mood_only",
                "identity_source": False,
                "allowed_use": list(ALLOWED_COMPOSITION_USES),
                "assets": [
                    _asset(
                        composition_relative,
                        sha256_file(composition_path),
                    )
                ],
            },
        ],
    }
    pack["pack_sha256"] = reference_pack_fingerprint(pack)
    validate_reference_pack(pack, project_root)
    return pack


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the immutable Akari overhead-room reference pack."
    )
    parser.add_argument("--composition", type=Path, default=COMPOSITION_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output = args.output if args.output.is_absolute() else ROOT / args.output
    pack = build_reference_pack(ROOT, args.composition)
    dump_json(output, pack)
    asset_count = sum(
        len(group["assets"]) for group in pack["reference_inputs"]
    )
    print(f"overhead room reference pack written: {asset_count} assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
