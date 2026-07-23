from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path

from PIL import Image


class ValidationError(ValueError):
    pass


DAILY_TOP_LEVEL_KEYS = {
    "schema_version", "request_id", "asset_id", "revision",
    "variation_axis", "references", "shared_prompt", "scene_contract",
    "production_requirements", "candidate_policy", "candidates",
    "comparison_anchors", "acceptance_gates", "hard_rejects",
}


@dataclass(frozen=True)
class DailyReviewPolicy:
    controllers: frozenset[str]
    scene_controller: str
    optional_c_finding_severities: frozenset[str]
    optional_c_allows_distinct_candidate_local: bool


DAILY_REVIEW_POLICIES = {
    "D01": DailyReviewPolicy(
        frozenset({"C04", "C05", "C06", "C07", "D01-scene"}),
        "D01-scene",
        frozenset({"blocker", "major", "minor"}),
        False,
    ),
    "D02": DailyReviewPolicy(
        frozenset({"D01", "C04", "C05", "C06", "C07", "D02-scene"}),
        "D02-scene",
        frozenset({"blocker", "major"}),
        False,
    ),
    "D03": DailyReviewPolicy(
        frozenset(
            {"D02", "C01", "C03", "C05", "C06", "C07", "D03-scene"}
        ),
        "D03-scene",
        frozenset({"blocker", "major"}),
        False,
    ),
    "D04": DailyReviewPolicy(
        frozenset(
            {"D03", "C01", "C03", "C05", "C06", "C07", "D04-scene"}
        ),
        "D04-scene",
        frozenset({"blocker", "major"}),
        True,
    ),
    "D05": DailyReviewPolicy(
        frozenset(
            {"D04", "C02", "C03", "C05", "C06", "C07", "D05-scene"}
        ),
        "D05-scene",
        frozenset({"blocker", "major"}),
        True,
    ),
    "D06": DailyReviewPolicy(
        frozenset({"C01", "C03", "C04", "C06", "C07", "D06-scene"}),
        "D06-scene",
        frozenset({"blocker", "major"}),
        True,
    ),
    "D07": DailyReviewPolicy(
        frozenset({"D06", "C03", "C04", "C06", "C07", "D07-scene"}),
        "D07-scene",
        frozenset({"blocker", "major"}),
        True,
    ),
    "D08": DailyReviewPolicy(
        frozenset({"D07", "C03", "C04", "C06", "C07", "D08-scene"}),
        "D08-scene",
        frozenset({"blocker", "major"}),
        True,
    ),
    "D09": DailyReviewPolicy(
        frozenset({"D08", "C03", "C04", "C06", "C07", "D09-scene"}),
        "D09-scene",
        frozenset({"blocker", "major"}),
        True,
    ),
    "D10": DailyReviewPolicy(
        frozenset({"D09", "D02", "C03", "C06", "C07", "D10-scene"}),
        "D10-scene",
        frozenset({"blocker", "major"}),
        True,
    ),
    "D11": DailyReviewPolicy(
        frozenset({"D10", "D02", "C03", "C04", "C07", "D11-scene"}),
        "D11-scene",
        frozenset({"blocker", "major"}),
        True,
    ),
    "D12": DailyReviewPolicy(
        frozenset({"D11", "D04", "C03", "C01", "C07", "D12-scene"}),
        "D12-scene",
        frozenset({"blocker", "major"}),
        True,
    ),
    "D13": DailyReviewPolicy(
        frozenset({"D12", "D04", "C03", "C01", "C07", "D13-scene"}),
        "D13-scene",
        frozenset({"blocker", "major"}),
        True,
    ),
    "D14": DailyReviewPolicy(
        frozenset({"D13", "D11", "D06", "C03", "C07", "D14-scene"}),
        "D14-scene",
        frozenset({"blocker", "major"}),
        True,
    ),
    "D15": DailyReviewPolicy(
        frozenset({"D14", "D13", "D11", "C03", "C07", "D15-scene"}),
        "D15-scene",
        frozenset({"blocker", "major"}),
        True,
    ),
}
DAILY_FINDING_FIELDS = {
    "severity",
    "category",
    "note",
    "resolved",
    "controlling_source_asset",
    "recommended_next_action",
}


def daily_review_policy(asset_id: str) -> DailyReviewPolicy:
    try:
        return DAILY_REVIEW_POLICIES[asset_id]
    except KeyError as error:
        raise ValidationError(
            f"{asset_id}: Daily review policy required"
        ) from error


def validate_daily_finding(asset_id: str, finding: dict) -> None:
    policy = daily_review_policy(asset_id)
    if (
        set(finding) != DAILY_FINDING_FIELDS
        or finding.get("controlling_source_asset")
        not in policy.controllers
        or not isinstance(finding.get("recommended_next_action"), str)
        or not finding["recommended_next_action"].strip()
    ):
        raise ValidationError(f"{asset_id}: exact finding provenance required")


def validate_daily_review_status(
    asset_id: str,
    status: str,
    findings: list[dict],
) -> None:
    policy = daily_review_policy(asset_id)
    unresolved = [item for item in findings if not item["resolved"]]
    if status == "accepted" and unresolved:
        raise ValidationError(
            f"{asset_id}: accepted requires no unresolved finding"
        )
    if status == "accepted-with-notes" and (
        not unresolved
        or any(
            item["severity"] != "minor"
            or item["controlling_source_asset"]
            != policy.scene_controller
            for item in unresolved
        )
    ):
        raise ValidationError(
            f"{asset_id}: accepted-with-notes requires "
            f"{policy.scene_controller} Minor only"
        )


def _ordered_value(value):
    if isinstance(value, dict):
        return tuple(
            (key, _ordered_value(item)) for key, item in value.items()
        )
    if isinstance(value, list):
        return tuple(_ordered_value(item) for item in value)
    return value


def daily_candidate_path(
    asset_id: str, revision: str, descriptor: str, variant: str
) -> str:
    lower_id = asset_id.lower()
    return (
        f"source/candidates/{lower_id}/{revision}/"
        f"akari-v1.2_{lower_id}_{descriptor}_{revision}-{variant}.png"
    )


def validate_daily_generation_request(data: dict, contract: dict) -> None:
    asset_id = data["asset_id"]
    if set(data) != DAILY_TOP_LEVEL_KEYS:
        raise ValidationError(f"{asset_id} exact top-level contract required")
    if any(set(item) != {"role", "path"} for item in data["references"]):
        raise ValidationError(f"{asset_id} exact reference contract required")
    candidates = data.get("candidates")
    variants = [item.get("variant") for item in candidates or []]
    if variants not in (["a", "b"], ["a", "b", "c"]):
        raise ValidationError(f"{asset_id} candidate contract mismatch")
    expected = [
        {
            "variant": variant,
            "title": f"independent-scene-{variant}",
            "target_path": daily_candidate_path(
                asset_id, data["revision"], contract["descriptor"], variant
            ),
        }
        for variant in variants
    ]
    if candidates != expected:
        raise ValidationError(f"{asset_id} candidate contract mismatch")
    if _ordered_value(data.get("scene_contract")) != _ordered_value(
        contract["scene_contract"]
    ):
        raise ValidationError(f"{asset_id} scene_contract mismatch")
    for key in ("production_requirements", "candidate_policy"):
        if data.get(key) != contract[key]:
            raise ValidationError(f"{asset_id} {key} mismatch")
    if data.get("comparison_anchors") != []:
        raise ValidationError(f"{asset_id} comparison anchors mismatch")
    prompt = data.get("shared_prompt")
    if not isinstance(prompt, str):
        raise ValidationError(f"{asset_id} shared prompt required")
    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    if digest != contract["shared_prompt_sha256"]:
        raise ValidationError(f"{asset_id} exact shared prompt contract mismatch")
    if data.get("acceptance_gates") != list(contract["acceptance_gates"]):
        raise ValidationError(f"{asset_id} acceptance gates mismatch")
    if data.get("hard_rejects") != list(contract["hard_rejects"]):
        raise ValidationError(f"{asset_id} exact hard rejects required")


def validate_daily_png_dimensions(
    source: Path, asset_id: str, revision: str, requirements: dict
) -> None:
    try:
        with Image.open(source) as image:
            image_format = image.format
            width, height = image.size
            image.verify()
    except (OSError, SyntaxError) as error:
        raise ValidationError(
            f"{asset_id} {revision}: unreadable candidate PNG"
        ) from error
    if image_format != "PNG":
        raise ValidationError(f"{asset_id} {revision}: candidate must be PNG")
    width_gate = requirements["accepted_width"]
    height_gate = requirements["accepted_height"]
    if not (
        width_gate["minimum"] <= width <= width_gate["maximum"]
        and height_gate["minimum"] <= height <= height_gate["maximum"]
    ):
        raise ValidationError(
            f"{asset_id} {revision}: candidate dimensions outside "
            f"{width_gate['minimum']}-{width_gate['maximum']} x "
            f"{height_gate['minimum']}-{height_gate['maximum']}"
        )


def validate_daily_candidate_dimensions(request: dict, package_root: Path) -> None:
    for candidate in request["candidates"]:
        source = package_root / candidate["target_path"]
        if source.is_file():
            validate_daily_png_dimensions(
                source,
                request["asset_id"],
                request["revision"],
                request["production_requirements"],
            )
