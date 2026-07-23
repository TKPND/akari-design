#!/usr/bin/env python3
"""Validate the Akari v1.3 Base Definition package."""

from __future__ import annotations

import argparse
import filecmp
import hashlib
from pathlib import Path, PurePosixPath
import re
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.3"

ASSET_CONTRACT = {
    "V13-01": {
        "descriptor": "corrected-key-visual",
        "variants": ["default"],
        "expected_paths": [
            "accepted/base/key-visual/"
            "akari-v1.3_v13-01_corrected-key-visual_rNN.png"
        ],
        "depends_on": [],
        "controlling_gate": "identity",
        "required_review_gates": {
            "identity",
            "ornament",
            "expression",
            "rendering",
            "preservation",
        },
    },
    "V13-02": {
        "descriptor": "natural-full-body",
        "variants": ["default"],
        "expected_paths": [
            "accepted/base/full-body/"
            "akari-v1.3_v13-02_natural-full-body_rNN.png"
        ],
        "depends_on": ["V13-01"],
        "controlling_gate": "body",
        "required_review_gates": {
            "identity",
            "ornament",
            "body",
            "rendering",
        },
    },
    "V13-03": {
        "descriptor": "expression-pair",
        "variants": ["everyday", "bright-smile"],
        "expected_paths": [
            "accepted/base/expressions/"
            "akari-v1.3_v13-03a_everyday_rNN.png",
            "accepted/base/expressions/"
            "akari-v1.3_v13-03b_bright-smile_rNN.png",
        ],
        "depends_on": ["V13-01", "V13-02"],
        "controlling_gate": "expression",
        "required_review_gates": {
            "identity",
            "ornament",
            "expression",
            "rendering",
            "pair-consistency",
        },
    },
    "V13-04": {
        "descriptor": "wardrobe-pair",
        "variants": ["outdoor", "roomwear"],
        "expected_paths": [
            "accepted/base/wardrobe/"
            "akari-v1.3_v13-04a_outdoor_rNN.png",
            "accepted/base/wardrobe/"
            "akari-v1.3_v13-04b_roomwear_rNN.png",
        ],
        "depends_on": ["V13-01", "V13-02"],
        "controlling_gate": "wardrobe",
        "required_review_gates": {
            "identity",
            "ornament",
            "body",
            "wardrobe",
            "rendering",
            "pair-consistency",
        },
    },
}

ASSET_STATES = {"planned", "candidate", "review", "accepted"}
REVIEW_STATUSES = ["accepted", "rejected", "superseded"]
VERDICTS = ["pass", "minor", "major", "not-applicable"]
REVISION_RE = re.compile(r"^r[0-9]{2}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ValidationError(ValueError):
    """Raised when the Base Definition contract is violated."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def _mapping(value: object, label: str) -> dict:
    _require(isinstance(value, dict), f"{label} must be a mapping")
    return value


def _list(value: object, label: str) -> list:
    _require(isinstance(value, list), f"{label} must be a list")
    return value


def _string_list(value: object, label: str) -> list[str]:
    items = _list(value, label)
    _require(
        all(isinstance(item, str) and item for item in items),
        f"{label} must contain non-empty strings",
    )
    return items


def _relative_path(value: object, label: str) -> PurePosixPath:
    _require(isinstance(value, str) and value, f"{label} must be a path string")
    _require("\\" not in value, f"{label} must use repository-relative POSIX syntax")
    path = PurePosixPath(value)
    _require(
        not path.is_absolute() and ".." not in path.parts and "." not in path.parts,
        f"{label} must be a safe relative path",
    )
    return path


def _resolve_relative(root: Path, value: object, label: str) -> Path:
    relative = _relative_path(value, label)
    return root.joinpath(*relative.parts)


def _sha_list(value: object, label: str, expected_count: int) -> list[str]:
    hashes = _string_list(value, label)
    _require(
        len(hashes) == expected_count,
        f"{label} count: expected {expected_count}, got {len(hashes)}",
    )
    _require(
        all(SHA256_RE.fullmatch(digest) for digest in hashes),
        f"{label} must contain lowercase SHA-256 digests",
    )
    return hashes


def load_yaml(path: Path) -> dict:
    """Load one manifest as a mapping."""

    try:
        with path.open(encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
    except (OSError, yaml.YAMLError) as error:
        raise ValidationError(f"cannot load {path}: {error}") from error
    return _mapping(data, str(path))


def sha256_file(path: Path) -> str:
    """Return a lowercase SHA-256 digest for a file."""

    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as error:
        raise ValidationError(f"cannot hash {path}: {error}") from error
    return digest.hexdigest()


def validate_assets(data: dict, package_root: Path) -> None:
    """Validate the static asset contract and current lifecycle state."""

    _require(data.get("schema_version") == 1, "assets schema_version must be 1")
    _require(
        data.get("collection") == "akari-v1.3-base-definition",
        "assets collection must be akari-v1.3-base-definition",
    )
    _require(data.get("required_image_count") == 6, "required_image_count must be 6")
    assets = _list(data.get("assets"), "assets")
    expected_ids = list(ASSET_CONTRACT)
    actual_ids = [
        _mapping(asset, f"assets[{index}]").get("asset_id")
        for index, asset in enumerate(assets)
    ]
    _require(
        actual_ids == expected_ids,
        f"asset IDs must be ordered as {expected_ids}, got {actual_ids}",
    )

    accepted_paths_seen: set[str] = set()
    status_by_id = {asset["asset_id"]: asset.get("status") for asset in assets}
    for asset in assets:
        asset_id = asset["asset_id"]
        contract = ASSET_CONTRACT[asset_id]
        dependencies = _string_list(asset.get("depends_on"), f"{asset_id} depends_on")
        for dependency in dependencies:
            _require(
                dependency in ASSET_CONTRACT,
                f"{asset_id} has unknown dependency {dependency}",
            )

        for field in (
            "descriptor",
            "variants",
            "expected_paths",
            "depends_on",
            "controlling_gate",
        ):
            _require(
                asset.get(field) == contract[field],
                f"{asset_id} {field} must equal {contract[field]!r}",
            )

        status = asset.get("status")
        _require(status in ASSET_STATES, f"{asset_id} has invalid status {status!r}")
        revision = asset.get("revision")
        accepted_paths = _list(asset.get("accepted_paths"), f"{asset_id} accepted_paths")

        if status != "accepted":
            _require(revision is None, f"{asset_id} non-accepted revision must be null")
            _require(
                accepted_paths == [], f"{asset_id} non-accepted accepted_paths must be empty"
            )
            continue

        _require(
            isinstance(revision, str) and REVISION_RE.fullmatch(revision),
            f"{asset_id} accepted revision must match rNN",
        )
        expected_paths = [
            path.replace("rNN", revision) for path in contract["expected_paths"]
        ]
        _require(
            accepted_paths == expected_paths,
            f"{asset_id} accepted_paths must be {expected_paths}",
        )
        for index, accepted_path in enumerate(accepted_paths):
            _require(
                accepted_path not in accepted_paths_seen,
                f"duplicate accepted path: {accepted_path}",
            )
            accepted_paths_seen.add(accepted_path)
            resolved = _resolve_relative(
                package_root, accepted_path, f"{asset_id} accepted_paths[{index}]"
            )
            _require(resolved.suffix == ".png", f"{asset_id} accepted path must be PNG")
            _require(resolved.is_file(), f"{asset_id} accepted file is missing: {resolved}")

    variant_count = sum(len(asset["variants"]) for asset in assets)
    _require(variant_count == 6, f"variant count: expected 6, got {variant_count}")

    for asset_id, contract in ASSET_CONTRACT.items():
        if status_by_id[asset_id] != "accepted":
            continue
        for dependency in contract["depends_on"]:
            _require(
                status_by_id[dependency] == "accepted",
                f"{asset_id} acceptance requires accepted dependency {dependency}",
            )


def _validate_inheritance_at(
    data: dict, repo_root: Path, package_root: Path
) -> None:
    _require(
        data.get("schema_version") == 1, "inheritance schema_version must be 1"
    )
    _require(
        data.get("collection") == "akari-v1.3-base-definition",
        "inheritance collection must be akari-v1.3-base-definition",
    )
    references = _list(data.get("references"), "inheritance references")
    reference_ids = [
        _mapping(reference, f"references[{index}]").get("reference_id")
        for index, reference in enumerate(references)
    ]
    _require(
        reference_ids == ["style-v04-a", "v1.2-c01-standing"],
        "inheritance must contain exactly style-v04-a and v1.2-c01-standing",
    )

    required_fields = {
        "source_path",
        "copied_path",
        "source_collection",
        "controlling_roles",
        "reuse_rationale",
        "inherited_traits",
        "excluded_traits",
        "sha256",
    }
    for reference in references:
        reference_id = reference["reference_id"]
        missing = sorted(required_fields - reference.keys())
        _require(not missing, f"{reference_id} missing fields: {', '.join(missing)}")
        _relative_path(reference["source_path"], f"{reference_id} source_path")
        copied_relative = _relative_path(
            reference["copied_path"], f"{reference_id} copied_path"
        )
        _require(
            copied_relative.parts[0] == "references",
            f"{reference_id} copied_path must stay under references/",
        )
        _require(
            isinstance(reference["source_collection"], str)
            and reference["source_collection"],
            f"{reference_id} source_collection must be non-empty",
        )
        for field in ("controlling_roles", "inherited_traits", "excluded_traits"):
            _require(
                bool(_string_list(reference[field], f"{reference_id} {field}")),
                f"{reference_id} {field} must not be empty",
            )
        _require(
            isinstance(reference["reuse_rationale"], str)
            and reference["reuse_rationale"].strip(),
            f"{reference_id} reuse_rationale must be non-empty",
        )
        recorded_hash = reference["sha256"]
        _require(
            isinstance(recorded_hash, str) and SHA256_RE.fullmatch(recorded_hash),
            f"{reference_id} SHA-256 must be 64 lowercase hex characters",
        )
        copied_path = package_root.joinpath(*copied_relative.parts)
        _require(copied_path.is_file(), f"{reference_id} copied file is missing")
        _require(
            sha256_file(copied_path) == recorded_hash,
            f"{reference_id} copied SHA-256 mismatch",
        )

    c01 = references[1]
    required_exclusions = {"face", "age", "hair", "ornament", "rendering"}
    missing_exclusions = required_exclusions - set(c01["excluded_traits"])
    _require(
        not missing_exclusions,
        "v1.2-c01-standing must exclude " + ", ".join(sorted(missing_exclusions)),
    )

    del repo_root  # Provenance source paths are recorded, not runtime dependencies.


def validate_inheritance(data: dict, repo_root: Path) -> None:
    """Validate role-limited copied references and their immutable hashes."""

    _validate_inheritance_at(data, repo_root, repo_root / "akari-v1.3")


def _asset_map(assets: dict) -> dict[str, dict]:
    return {
        asset["asset_id"]: asset
        for asset in _list(assets.get("assets"), "assets")
    }


def validate_review_log(
    data: dict,
    assets: dict,
    package_root: Path,
    require_complete: bool,
) -> None:
    """Validate reviews, promotion integrity, and the Base Identity Lock."""

    _require(data.get("schema_version") == 1, "review schema_version must be 1")
    _require(
        data.get("allowed_statuses") == REVIEW_STATUSES,
        f"allowed_statuses must be {REVIEW_STATUSES}",
    )
    _require(
        data.get("allowed_verdicts") == VERDICTS,
        f"allowed_verdicts must be {VERDICTS}",
    )
    reviews = _list(data.get("reviews"), "reviews")
    assets_by_id = _asset_map(assets)
    accepted_reviews: dict[str, list[dict]] = {asset_id: [] for asset_id in ASSET_CONTRACT}
    candidate_ids: set[str] = set()

    for index, raw_review in enumerate(reviews):
        review = _mapping(raw_review, f"reviews[{index}]")
        candidate_id = review.get("candidate_id")
        _require(
            isinstance(candidate_id, str) and candidate_id,
            f"reviews[{index}] candidate_id must be non-empty",
        )
        _require(candidate_id not in candidate_ids, f"duplicate candidate_id {candidate_id}")
        candidate_ids.add(candidate_id)
        asset_id = review.get("asset_id")
        _require(asset_id in ASSET_CONTRACT, f"{candidate_id} has unknown asset_id")
        contract = ASSET_CONTRACT[asset_id]
        variant_count = len(contract["variants"])
        revision = review.get("revision")
        _require(
            isinstance(revision, str) and REVISION_RE.fullmatch(revision),
            f"{candidate_id} revision must match rNN",
        )
        status = review.get("status")
        _require(status in REVIEW_STATUSES, f"{candidate_id} has invalid status")
        overall = review.get("overall_verdict")
        _require(overall in VERDICTS, f"{candidate_id} has invalid overall_verdict")
        user_selected = review.get("user_selected")
        _require(
            isinstance(user_selected, bool), f"{candidate_id} user_selected must be boolean"
        )
        source_paths = _string_list(
            review.get("source_paths"), f"{candidate_id} source_paths"
        )
        _require(
            len(source_paths) == variant_count,
            f"{candidate_id} source path count: expected {variant_count}, got {len(source_paths)}",
        )
        source_hashes = _sha_list(
            review.get("source_sha256"),
            f"{candidate_id} source_sha256",
            variant_count,
        )
        promoted_paths = _list(
            review.get("promoted_paths"), f"{candidate_id} promoted_paths"
        )
        promoted_hashes = _list(
            review.get("promoted_sha256"), f"{candidate_id} promoted_sha256"
        )
        gate_verdicts = _mapping(
            review.get("gate_verdicts"), f"{candidate_id} gate_verdicts"
        )
        _require(
            set(gate_verdicts) == contract["required_review_gates"],
            f"{asset_id} review gates must be {sorted(contract['required_review_gates'])}",
        )
        _require(
            all(verdict in VERDICTS for verdict in gate_verdicts.values()),
            f"{candidate_id} has invalid gate verdict",
        )
        _list(review.get("findings"), f"{candidate_id} findings")
        _require(
            isinstance(review.get("decision"), str) and review["decision"].strip(),
            f"{candidate_id} decision must be non-empty",
        )

        resolved_sources = []
        for source_index, source_path in enumerate(source_paths):
            resolved = _resolve_relative(
                package_root,
                source_path,
                f"{candidate_id} source_paths[{source_index}]",
            )
            resolved_sources.append(resolved)
            if resolved.exists():
                _require(
                    resolved.is_file() and sha256_file(resolved) == source_hashes[source_index],
                    f"{candidate_id} candidate SHA-256 mismatch",
                )

        if status != "accepted":
            _require(not user_selected, f"{candidate_id} non-accepted review cannot be selected")
            _require(
                promoted_paths == [] and promoted_hashes == [],
                f"{candidate_id} non-accepted promotion fields must be empty",
            )
            continue

        accepted_reviews[asset_id].append(review)
        _require(
            overall == "pass", f"{asset_id} accepted review must have overall pass"
        )
        _require(
            user_selected, f"{asset_id} accepted review requires user_selected: true"
        )
        _require(
            all(verdict == "pass" for verdict in gate_verdicts.values()),
            f"{asset_id} accepted review gates must all pass",
        )
        asset = assets_by_id[asset_id]
        _require(
            asset.get("status") == "accepted" and asset.get("revision") == revision,
            f"{asset_id} accepted review must match accepted asset revision",
        )
        _require(
            promoted_paths == asset.get("accepted_paths"),
            f"{asset_id} promoted paths must match accepted paths",
        )
        promoted_paths = _string_list(promoted_paths, f"{candidate_id} promoted_paths")
        promoted_hashes = _sha_list(
            promoted_hashes, f"{candidate_id} promoted_sha256", variant_count
        )
        _require(
            source_hashes == promoted_hashes,
            f"{asset_id} source and promoted hashes must match",
        )
        for promoted_index, promoted_path in enumerate(promoted_paths):
            resolved_promoted = _resolve_relative(
                package_root,
                promoted_path,
                f"{candidate_id} promoted_paths[{promoted_index}]",
            )
            _require(
                resolved_promoted.is_file(),
                f"{asset_id} promoted file is missing: {resolved_promoted}",
            )
            _require(
                sha256_file(resolved_promoted) == promoted_hashes[promoted_index],
                f"{asset_id} promoted SHA-256 mismatch",
            )
            resolved_source = resolved_sources[promoted_index]
            if resolved_source.exists():
                _require(
                    filecmp.cmp(resolved_source, resolved_promoted, shallow=False),
                    f"{asset_id} candidate and promoted bytes differ",
                )

    for asset_id, asset in assets_by_id.items():
        expected_count = 1 if asset.get("status") == "accepted" else 0
        actual_count = len(accepted_reviews[asset_id])
        _require(
            actual_count == expected_count,
            f"{asset_id} accepted review count: expected {expected_count}, got {actual_count}",
        )

    lock = _mapping(data.get("base_identity_lock"), "base_identity_lock")
    lock_passed = (
        lock.get("status") == "accepted"
        and lock.get("same_person_verdict") == "pass"
        and lock.get("user_confirmed") is True
    )
    for asset_id in ("V13-03", "V13-04"):
        if assets_by_id[asset_id].get("status") == "accepted":
            _require(
                lock_passed,
                f"{asset_id} acceptance requires Base Identity Lock",
            )

    if lock.get("status") == "accepted":
        for asset_id, revision_field in (
            ("V13-01", "v13_01_revision"),
            ("V13-02", "v13_02_revision"),
        ):
            asset = assets_by_id[asset_id]
            _require(
                asset.get("status") == "accepted"
                and lock.get(revision_field) == asset.get("revision"),
                f"Base Identity Lock {revision_field} must match {asset_id}",
            )
    else:
        _require(
            lock
            == {
                "status": "pending",
                "v13_01_revision": None,
                "v13_02_revision": None,
                "same_person_verdict": None,
                "user_confirmed": False,
            },
            "pending Base Identity Lock must retain the initial null state",
        )

    accepted_image_count = sum(
        len(asset.get("accepted_paths", []))
        for asset in assets_by_id.values()
        if asset.get("status") == "accepted"
    )
    if require_complete:
        _require(
            accepted_image_count == 6,
            "required accepted image count: "
            f"expected 6, got {accepted_image_count}",
        )


def validate_package(
    package_root: Path = PACKAGE_ROOT,
    repo_root: Path = ROOT,
    require_complete: bool = True,
) -> None:
    """Validate the complete package or its current production-stage state."""

    assets = load_yaml(package_root / "manifest/assets.yaml")
    inheritance = load_yaml(package_root / "manifest/inheritance.yaml")
    review_log = load_yaml(package_root / "manifest/review-log.yaml")
    validate_assets(assets, package_root)
    _validate_inheritance_at(inheritance, repo_root, package_root)
    validate_review_log(review_log, assets, package_root, require_complete)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-incomplete",
        action="store_true",
        help="validate the current production-stage lifecycle without six accepted images",
    )
    args = parser.parse_args(argv)
    try:
        validate_package(require_complete=not args.allow_incomplete)
    except ValidationError as error:
        print(f"akari v1.3 validation failed: {error}", file=sys.stderr)
        return 1
    print("akari v1.3 validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
