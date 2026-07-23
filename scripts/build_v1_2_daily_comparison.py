from __future__ import annotations

import argparse
from pathlib import Path
import re

import yaml

if __package__:
    from scripts.build_v1_2_c03_comparisons import render_grid
else:
    from build_v1_2_c03_comparisons import render_grid


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"


def build_daily_comparison(
    request_path: Path,
    package_root: Path,
    output_path: Path,
    expected_asset_id: str | None = None,
) -> Path:
    request = yaml.safe_load(request_path.read_text(encoding="utf-8"))
    asset_id = request.get("asset_id")
    revision = request.get("revision")
    if (
        not isinstance(asset_id, str)
        or re.fullmatch(r"D\d{2}", asset_id) is None
        or not isinstance(revision, str)
        or re.fullmatch(r"r\d{2}", revision) is None
        or (
            expected_asset_id is not None
            and asset_id != expected_asset_id
        )
    ):
        raise ValueError("expected declared Daily revision request")
    candidates = request.get("candidates")
    variants = [item.get("variant") for item in candidates or []]
    if variants not in (["a", "b"], ["a", "b", "c"]):
        raise ValueError("expected Daily A/B or A/B/C candidates")

    asset_manifest = yaml.safe_load(
        (package_root / "manifest/assets.yaml").read_text(encoding="utf-8")
    )
    assets = (
        asset_manifest.get("assets")
        if isinstance(asset_manifest, dict)
        else None
    )
    declared_assets = [
        item
        for item in assets or []
        if isinstance(item, dict) and item.get("asset_id") == asset_id
    ]
    if (
        len(declared_assets) != 1
        or not isinstance(declared_assets[0].get("descriptor"), str)
    ):
        raise ValueError("expected declared Daily asset contract")
    descriptor = declared_assets[0]["descriptor"]

    lower_id = asset_id.lower()
    source_directory = Path(f"source/candidates/{lower_id}/{revision}")
    canonical_directory = package_root.resolve(strict=False) / source_directory
    actual_directory = (package_root / source_directory).resolve(strict=False)
    if actual_directory != canonical_directory:
        raise ValueError("Daily candidate sources must remain canonical")

    pattern = re.compile(
        rf"^source/candidates/{lower_id}/{revision}/"
        rf"akari-v1\.2_{lower_id}_([a-z0-9-]+)_{revision}-([abc])\.png$"
    )
    row = []
    for candidate, variant in zip(candidates, variants):
        raw_source = candidate.get("target_path", "")
        if not isinstance(raw_source, str):
            raise ValueError("Daily candidate sources must remain canonical")
        source = Path(raw_source)
        match = pattern.fullmatch(source.as_posix())
        resolved = (package_root / source).resolve(strict=False)
        if (
            source.is_absolute()
            or raw_source != source.as_posix()
            or match is None
            or match.group(2) != variant
            or resolved.parent != canonical_directory
        ):
            raise ValueError("Daily candidate sources must remain canonical")
        current_descriptor = match.group(1)
        if current_descriptor != descriptor:
            raise ValueError("Daily candidate descriptor mismatch")
        if not (package_root / source).is_file():
            raise ValueError(f"missing {source.name}")
        row.append(
            (
                f"{variant.upper()}  {asset_id} "
                f"{current_descriptor.replace('-', ' ')}",
                package_root / source,
            )
        )
    return render_grid([row], output_path)


def resolve_from(base: Path, value: Path) -> Path:
    return value if value.is_absolute() else base / value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--asset-id", required=True)
    args = parser.parse_args()
    result = build_daily_comparison(
        resolve_from(ROOT, args.request),
        PACKAGE_ROOT,
        resolve_from(ROOT, args.output),
        expected_asset_id=args.asset_id,
    )
    print(result.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
