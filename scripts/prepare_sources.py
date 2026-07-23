#!/usr/bin/env python3
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

from akari_assets import ROOT, SOURCE_ASSETS


ORIGINALS_DIR = ROOT / "source/originals"
MANIFEST_DIR = ROOT / "source/manifests"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_image_dirs() -> list[Path]:
    dirs = []
    configured = os.environ.get("AKARI_SOURCE_IMAGE_DIR")
    if configured:
        dirs.append(Path(configured).expanduser())
    dirs.append(ORIGINALS_DIR)
    dirs.append(ROOT)
    return dirs


def find_source(filename: str) -> Path:
    checked = []
    for directory in source_image_dirs():
        candidate = directory / filename
        checked.append(candidate)
        if candidate.exists():
            return candidate
    locations = ", ".join(str(path) for path in checked)
    raise FileNotFoundError(f"source asset not found: {filename} (checked: {locations})")


def image_metadata(path: Path) -> dict:
    result = subprocess.run(
        ["identify", "-format", "%w %h %[colorspace]", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    width, height, colorspace = result.stdout.strip().split()
    return {
        "width": int(width),
        "height": int(height),
        "colorspace": colorspace,
    }


def main() -> int:
    ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    manifest_assets = []
    for asset in SOURCE_ASSETS:
        source = find_source(asset["filename"])
        target = ORIGINALS_DIR / asset["filename"]
        if not target.exists() or sha256(source) != sha256(target):
            shutil.copy2(source, target)
        metadata = image_metadata(target)
        manifest_assets.append(
            {
                "id": asset["id"],
                "original_filename": asset["filename"],
                "source_path": target.relative_to(ROOT).as_posix(),
                "sha256": sha256(target),
                "width": metadata["width"],
                "height": metadata["height"],
                "colorspace": metadata["colorspace"],
                "role": asset["role"],
                "orientation_state": asset["orientation_state"],
            }
        )

    payload = {
        "schema_version": 1,
        "asset_count": len(manifest_assets),
        "assets": manifest_assets,
    }
    (MANIFEST_DIR / "source-assets.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"source assets prepared: {len(manifest_assets)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
