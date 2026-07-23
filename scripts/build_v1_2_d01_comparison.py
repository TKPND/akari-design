from __future__ import annotations

import argparse
from pathlib import Path

if __package__:
    from scripts.build_v1_2_daily_comparison import build_daily_comparison
else:
    from build_v1_2_daily_comparison import build_daily_comparison


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"


def build_d01_comparison(
    request_path: Path,
    package_root: Path,
    output_path: Path,
) -> Path:
    return build_daily_comparison(
        request_path,
        package_root,
        output_path,
        expected_asset_id="D01",
    )


def resolve_from(base: Path, value: Path) -> Path:
    return value if value.is_absolute() else base / value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_d01_comparison(
        resolve_from(ROOT, args.request),
        PACKAGE_ROOT,
        resolve_from(ROOT, args.output),
    )
    print(result.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
