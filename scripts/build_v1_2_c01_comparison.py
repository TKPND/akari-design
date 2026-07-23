from __future__ import annotations

import argparse
from pathlib import Path

if __package__:
    from scripts.build_v1_2_candidate_comparison import build_comparison
else:
    from build_v1_2_candidate_comparison import build_comparison


ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "akari-v1.2/manifest/generation-requests/c01-r01.yaml"
OUTPUT = ROOT / "akari-v1.2/comparisons/c01-r01/c01-r01-comparison.webp"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, default=REQUEST)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = build_comparison(args.request, ROOT / "akari-v1.2", args.output)
    print(result.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
