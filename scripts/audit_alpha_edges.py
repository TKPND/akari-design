#!/usr/bin/env python3
import sys
from pathlib import Path

from PIL import Image, UnidentifiedImageError


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIRS = (
    ROOT / "build/assets/generated",
    ROOT / "build/assets/corrected",
)


def has_transparency(path: Path) -> bool:
    with Image.open(path) as image:
        if "transparency" in image.info:
            return True
        if "A" not in image.getbands():
            return False
        alpha = image.getchannel("A")
        return alpha.getextrema()[0] < 255


def raster_paths() -> list[Path]:
    paths = []
    for directory in ASSET_DIRS:
        if directory.exists():
            paths.extend(sorted(directory.rglob("*.png")))
            paths.extend(sorted(directory.rglob("*.webp")))
    return sorted(paths)


def main() -> int:
    checked = 0
    alpha_assets = 0
    errors = []

    for path in raster_paths():
        checked += 1
        try:
            if has_transparency(path):
                alpha_assets += 1
        except (OSError, UnidentifiedImageError) as error:
            errors.append(f"{path.relative_to(ROOT)}: {error}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"alpha edge audit: ok ({alpha_assets} transparent rasters, {checked} rasters checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
