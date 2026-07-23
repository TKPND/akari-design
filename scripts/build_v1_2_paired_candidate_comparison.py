from __future__ import annotations

import argparse
from pathlib import Path

import yaml

if __package__:
    from scripts.build_v1_2_c03_comparisons import render_grid
else:
    from build_v1_2_c03_comparisons import render_grid


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"


def build_paired_comparison(
    request_path: Path,
    package_root: Path,
    output_path: Path,
) -> Path:
    request = yaml.safe_load(request_path.read_text(encoding="utf-8"))
    candidates = request["candidates"]
    variants = [candidate.get("variant") for candidate in candidates]
    if variants not in (["a", "b"], ["a", "b", "c"]):
        raise ValueError("expected candidates a, b or a, b, c")
    view_order = list(request.get("view_prompts", {}))
    if len(view_order) != 2:
        raise ValueError("expected exactly two paired views")
    rows = []
    for candidate in candidates:
        outputs = candidate.get("outputs")
        if not isinstance(outputs, list) or [
            output.get("view") for output in outputs
        ] != view_order:
            raise ValueError("expected paired view order")
        rows.append(
            [
                (
                    f"{candidate['variant'].upper()}  {output['view']}",
                    package_root / output["target_path"],
                )
                for output in outputs
            ]
        )
    return render_grid(rows, output_path)


def resolve_from(base: Path, value: Path) -> Path:
    return value if value.is_absolute() else base / value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_paired_comparison(
        resolve_from(ROOT, args.request),
        PACKAGE_ROOT,
        resolve_from(ROOT, args.output),
    )
    print(result.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
