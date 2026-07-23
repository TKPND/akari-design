from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

if __package__:
    from scripts.build_v1_2_c03_comparisons import render_grid
else:
    from build_v1_2_c03_comparisons import render_grid


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"
STAGE_ORDER = (
    ("c06-1", "sleepy-neutral"),
    ("c06-2", "sleepy-secure"),
    ("c06-3", "loosened-mouth"),
    ("c06-4", "soft-smile"),
)


def review_set_label(candidate_id: str) -> str:
    complete = {
        "c06-r01-a": "A",
        "c06-r01-b": "B",
        "c06-r01-c": "C",
    }
    if candidate_id in complete:
        return complete[candidate_id]
    match = re.fullmatch(
        r"c06-r01-([ab])-repair-c06-([1-4])", candidate_id
    )
    if match:
        return f"{match.group(1).upper()}+C{match.group(2)}"
    raise ValueError("invalid C06 review set ID")


def expected_source_variants(candidate_id: str) -> tuple[str, ...]:
    complete = re.fullmatch(r"c06-r01-([abc])", candidate_id)
    if complete:
        return (complete.group(1),) * len(STAGE_ORDER)
    repair = re.fullmatch(
        r"c06-r01-([ab])-repair-c06-([1-4])", candidate_id
    )
    if repair:
        variants = [repair.group(1)] * len(STAGE_ORDER)
        variants[int(repair.group(2)) - 1] = "c"
        return tuple(variants)
    raise ValueError("invalid C06 review set ID")


def build_c06_comparison(
    request_path: Path,
    package_root: Path,
    output_path: Path,
) -> Path:
    request = yaml.safe_load(request_path.read_text(encoding="utf-8"))
    actual_stages = [
        (item.get("stage"), item.get("descriptor"))
        for item in request.get("stages", [])
    ]
    if actual_stages != list(STAGE_ORDER):
        raise ValueError("expected C06 stage order")

    review_sets = request.get("review_sets")
    if not isinstance(review_sets, list) or len(review_sets) not in (2, 3):
        raise ValueError("expected two or three C06 review sets")
    candidate_ids = [item.get("candidate_id") for item in review_sets]
    if candidate_ids[:2] != ["c06-r01-a", "c06-r01-b"]:
        raise ValueError("expected C06 A and B review sets first")
    if len(candidate_ids) == 3 and review_set_label(candidate_ids[2]) in {
        "A",
        "B",
    }:
        raise ValueError("expected C06 C or targeted repair review set third")

    rows = []
    source_directory = Path("source/candidates/c06/r01")
    anchored_source_directory = package_root.resolve(
        strict=False
    ) / source_directory
    resolved_source_directory = (package_root / source_directory).resolve(
        strict=False
    )
    if resolved_source_directory != anchored_source_directory:
        raise ValueError("review set sources must match C06 stage order")
    for review_set in review_sets:
        label = review_set_label(review_set["candidate_id"])
        expected_variants = expected_source_variants(
            review_set["candidate_id"]
        )
        source_paths = review_set.get("source_paths")
        if not isinstance(source_paths, list) or len(source_paths) != 4:
            raise ValueError("expected four ordered C06 sources")
        row = []
        for (stage, descriptor), expected_variant, source_value in zip(
            STAGE_ORDER, expected_variants, source_paths
        ):
            source = Path(source_value)
            resolved_source = (package_root / source).resolve(strict=False)
            expected_name = (
                f"akari-v1.2_{stage}_{descriptor}_r01-{expected_variant}.png"
            )
            if (
                source.is_absolute()
                or source.parent != source_directory
                or resolved_source.parent != anchored_source_directory
                or source.name != expected_name
            ):
                raise ValueError(
                    "review set sources must match C06 stage order"
                )
            row.append(
                (
                    f"{label}  {stage.upper()}  {descriptor}",
                    package_root / source,
                )
            )
        rows.append(row)
    return render_grid(rows, output_path)


def resolve_from(base: Path, value: Path) -> Path:
    return value if value.is_absolute() else base / value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_c06_comparison(
        resolve_from(ROOT, args.request),
        PACKAGE_ROOT,
        resolve_from(ROOT, args.output),
    )
    print(result.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
