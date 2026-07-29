#!/usr/bin/env python3
"""Initialize the external Akari v1.5 Kawaii 1000 data root."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path


REFERENCE_SOURCES = (
    (
        "v1.5-body-balance",
        Path("akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png"),
        "akari-v1.5-b3-body-balance.png",
    ),
    (
        "v1.4-rendering",
        Path(
            "akari-v1.4/style-tests/line-refinement/"
            "akari-v14-g2-balanced-lines.png"
        ),
        "akari-v1.4-g2-balanced-lines.png",
    ),
    (
        "v1.4-seated",
        Path(
            "akari-v1.4/style-tests/reproducibility-i-seated/"
            "akari-v14-i2-chair-seated-repro.png"
        ),
        "akari-v1.4-i2-seated.png",
    ),
    (
        "v1.4-action",
        Path(
            "akari-v1.4/style-tests/reproducibility-j-action/"
            "akari-v14-j1-mandarin-action-repro.png"
        ),
        "akari-v1.4-j1-action.png",
    ),
)

REFERENCE_METADATA = {
    "v1.5-body-balance": (
        "v1.5 identity and body balance",
        ["outfit", "pose", "background"],
    ),
    "v1.4-rendering": (
        "rendering and skin authority",
        ["body balance", "pose", "background"],
    ),
    "v1.4-seated": (
        "seated anatomy and weight distribution",
        ["identity", "outfit", "background"],
    ),
    "v1.4-action": (
        "hands and action continuity",
        ["identity", "outfit", "background"],
    ),
    "neesocks-pressure-study": (
        "anatomy and hosiery pressure only",
        ["identity", "composition", "underwear", "outfit", "color"],
    ),
}


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest for one file."""

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_json(path: Path, value: object) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _snapshot(source: Path, destination: Path) -> str:
    source_hash = sha256_file(source)
    if destination.exists():
        if sha256_file(destination) != source_hash:
            raise ValueError(f"reference snapshot mismatch: {destination}")
        return source_hash
    temporary = destination.with_name(f".{destination.name}.{os.getpid()}.tmp")
    shutil.copyfile(source, temporary)
    os.replace(temporary, destination)
    return source_hash


def initialize_data_root(
    repo_root: Path,
    data_root: Path,
    texture_reference: Path,
) -> Path:
    """Create an immutable local snapshot of the five generation references."""

    repo_root = repo_root.resolve()
    data_root = data_root.resolve()
    texture_reference = texture_reference.resolve()
    sources = [
        (item_id, repo_root / relative_source, destination_name)
        for item_id, relative_source, destination_name in REFERENCE_SOURCES
    ]
    sources.append(
        ("neesocks-pressure-study", texture_reference, "neesocks-pressure-study.jpeg")
    )
    for _, source, _ in sources:
        if not source.is_file():
            raise FileNotFoundError(source)

    references_dir = data_root / "references"
    references_dir.mkdir(parents=True, exist_ok=True)
    (data_root / "state").mkdir(exist_ok=True)
    (data_root / "batches").mkdir(exist_ok=True)

    records = []
    for item_id, source, destination_name in sources:
        destination = references_dir / destination_name
        digest = _snapshot(source, destination)
        role, exclusions = REFERENCE_METADATA[item_id]
        records.append(
            {
                "id": item_id,
                "role": role,
                "sourcePath": str(source),
                "snapshotPath": f"references/{destination_name}",
                "sha256": digest,
                "exclusions": exclusions,
            }
        )
    _atomic_json(
        references_dir / "manifest.json",
        {"schemaVersion": 1, "references": records},
    )

    ledger = data_root / "state/novelty-ledger.json"
    if not ledger.exists():
        _atomic_json(
            ledger,
            {
                "schemaVersion": 1,
                "acceptedProductionImages": 0,
                "technicalFailures": 0,
                "entries": [],
            },
        )
    return data_root


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize the Akari v1.5 Kawaii 1000 external data root."
    )
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--texture-reference", type=Path, required=True)
    args = parser.parse_args()
    data_root = initialize_data_root(
        args.repo_root,
        args.data_root,
        args.texture_reference,
    )
    print(f"initialized data root: {data_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
