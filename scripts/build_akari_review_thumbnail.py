from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from PIL import Image


PNG_SIGNATURE = bytes.fromhex("89504e470d0a1a0a")


def inspect_png(source: Path) -> dict[str, object]:
    contents = source.read_bytes()
    if contents[:8] != PNG_SIGNATURE:
        raise ValueError(f"invalid PNG signature: {source}")
    with Image.open(source) as image:
        image.verify()
    with Image.open(source) as image:
        width, height = image.size
        mode = image.mode
    return {
        "width": width,
        "height": height,
        "mode": mode,
        "sha256": hashlib.sha256(contents).hexdigest(),
    }


def build_thumbnail(source: Path, output: Path, max_edge: int = 512) -> Path:
    if source.resolve() == output.resolve():
        raise ValueError("output path must differ from source")
    inspect_png(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        converted = image.convert("RGB")
        converted.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
        converted.save(output, "WEBP", quality=82, method=6)
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a bounded WebP review thumbnail from a PNG source."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-edge", default=512, type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(build_thumbnail(args.input, args.output, args.max_edge))


if __name__ == "__main__":
    main()
