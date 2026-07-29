#!/usr/bin/env python3
"""Create the non-counting B000 review-gallery demo batch."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw

if __package__:
    from scripts.build_akari_review_thumbnail import (
        build_thumbnail,
        inspect_png,
    )
else:
    from build_akari_review_thumbnail import (
        build_thumbnail,
        inspect_png,
    )


LANES = (
    "classic-school-uniform",
    "professional-service-uniform",
    "sports-ceremony-fictional-uniform",
    "everyday-girly",
    "outings-special-days",
    "hobbies-making",
    "travel-walking",
    "retro-storybook",
    "magic-fantasy-sf",
    "subculture-wildcard",
)
COLORS = (
    "#f2d8d5",
    "#ead8ca",
    "#d9e4ef",
    "#efe2c6",
    "#dce7d6",
    "#e5daf0",
    "#f0d9e3",
    "#d7e8e6",
    "#e8dfd5",
    "#d9d8e9",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json_atomic(path: Path, value: object) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _reference(data_root: Path, name: str, role: str) -> dict[str, object]:
    path = data_root / "references" / name
    if not path.is_file():
        raise FileNotFoundError(path)
    return {
        "path": f"references/{name}",
        "role": role,
        "exclusions": ["outfit", "pose", "background"],
        "sha256": _sha256(path),
    }


def create_demo_batch(data_root: Path) -> Path:
    """Create or refresh the demo-only B000 batch."""

    data_root = data_root.resolve()
    batch = data_root / "batches/B000"
    manifest_path = batch / "manifest.json"
    if manifest_path.exists():
        current = json.loads(manifest_path.read_text(encoding="utf-8"))
        if current.get("batchType") != "demo":
            raise ValueError("refusing to overwrite non-demo B000")
    images = batch / "images"
    thumbs = batch / "thumbs"
    images.mkdir(parents=True, exist_ok=True)
    thumbs.mkdir(parents=True, exist_ok=True)
    authorities = (
        _reference(
            data_root,
            "akari-v1.5-b3-body-balance.png",
            "v1.5 identity and body balance",
        ),
        _reference(
            data_root,
            "akari-v1.4-g2-balanced-lines.png",
            "rendering and skin authority",
        ),
    )
    entries = []
    for lane_index, lane in enumerate(LANES):
        for offset in range(5):
            ordinal = lane_index * 5 + offset + 1
            image_id = f"B000-{ordinal:03d}"
            stem = f"demo-{ordinal:03d}"
            image_path = images / f"{stem}.png"
            thumb_path = thumbs / f"{stem}.webp"
            canvas = Image.new("RGB", (768, 1152), COLORS[lane_index])
            draw = ImageDraw.Draw(canvas)
            draw.text((64, 80), image_id, fill="#352f32")
            draw.text((64, 150), lane, fill="#352f32")
            draw.text(
                (64, 240),
                "1 Reject   2 Keep   3 Favorite",
                fill="#554b50",
            )
            canvas.save(image_path, "PNG")
            build_thumbnail(image_path, thumb_path)
            technical = inspect_png(image_path)
            entries.append(
                {
                    "id": image_id,
                    "lane": lane,
                    "cuteBeat": f"demo-beat-{ordinal}",
                    "wardrobeFamily": f"demo-wardrobe-{ordinal}",
                    "setting": f"demo-setting-{ordinal}",
                    "action": f"demo-action-{ordinal}",
                    "sceneMode": (
                        "action-reaction" if ordinal <= 40 else "quiet-posed"
                    ),
                    "composition": f"demo-composition-{ordinal}",
                    "camera": f"demo-camera-{ordinal}",
                    "lighting": f"demo-lighting-{ordinal}",
                    "cast": (
                        "solo"
                        if ordinal <= 35
                        else "viewer-pov"
                        if ordinal <= 45
                        else "group"
                    ),
                    "dominantColor": COLORS[lane_index],
                    "textureFocus": ordinal <= 10,
                    "textureType": (
                        f"demo-texture-{ordinal}"
                        if ordinal <= 10
                        else "none"
                    ),
                    "subculture": lane == "subculture-wildcard",
                    "prompt": f"Demo card only; no image generation; {image_id}",
                    "references": [dict(item) for item in authorities],
                    "generation": {
                        "toolMode": "demo",
                        "generationId": None,
                        "requestId": None,
                        "sourcePath": None,
                        "technicalStatus": "valid",
                        "failureReason": None,
                    },
                    "artifact": {
                        "imagePath": f"batches/B000/images/{stem}.png",
                        "thumbnailPath": f"batches/B000/thumbs/{stem}.webp",
                        "sha256": technical["sha256"],
                        "width": technical["width"],
                        "height": technical["height"],
                    },
                }
            )
    manifest = {
        "schemaVersion": 1,
        "batchType": "demo",
        "batchId": "B000",
        "title": "Akari Kawaii 1000 Review Demo",
        "entries": entries,
    }
    reviews = {
        "schemaVersion": 1,
        "batchId": "B000",
        "reviews": {
            entry["id"]: {
                "status": "unreviewed",
                "reasons": [],
                "note": "",
                "revision": 0,
                "updatedAt": None,
            }
            for entry in entries
        },
    }
    _write_json_atomic(manifest_path, manifest)
    reviews_path = batch / "reviews.json"
    if not reviews_path.exists():
        _write_json_atomic(reviews_path, reviews)
    return batch


def _absolute_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        raise argparse.ArgumentTypeError("must be an absolute path")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the non-counting B000 review-gallery demo batch."
    )
    parser.add_argument("--data-root", required=True, type=_absolute_path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(create_demo_batch(args.data_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
