from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"
CARD_SIZE = (300, 480)
GAP = 20
LABEL_HEIGHT = 46
BACKGROUND = "#f3f0ec"
CARD_BACKGROUND = "#ffffff"
TEXT = "#2b2927"


def load_font(size: int) -> ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def build_comparison(
    request_path: Path,
    package_root: Path,
    output_path: Path,
    anchor_path: Path | None = None,
) -> Path:
    request = yaml.safe_load(request_path.read_text(encoding="utf-8"))
    candidates = request["candidates"]
    if [item["variant"] for item in candidates] != ["a", "b", "c"]:
        raise ValueError("expected candidates a, b, c")
    cards: list[tuple[str, Path]] = []
    if anchor_path is not None:
        if not anchor_path.is_file():
            raise ValueError(f"missing {anchor_path.name}")
        cards.append(("C01  accepted anchor", anchor_path))
    for candidate in candidates:
        source = package_root / candidate["target_path"]
        if not source.is_file():
            raise ValueError(f"missing {source.name}")
        cards.append(
            (f"{candidate['variant'].upper()}  {candidate['title']}", source)
        )
    width = GAP * (len(cards) + 1) + CARD_SIZE[0] * len(cards)
    height = GAP * 2 + CARD_SIZE[1] + LABEL_HEIGHT
    sheet = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    font = load_font(16)
    for index, (label, source) in enumerate(cards):
        x = GAP + index * (CARD_SIZE[0] + GAP)
        y = GAP
        draw.rectangle(
            (x, y, x + CARD_SIZE[0], y + CARD_SIZE[1] + LABEL_HEIGHT),
            fill=CARD_BACKGROUND,
        )
        with Image.open(source) as image:
            fitted = ImageOps.contain(image.convert("RGB"), CARD_SIZE)
        sheet.paste(
            fitted,
            (
                x + (CARD_SIZE[0] - fitted.width) // 2,
                y + (CARD_SIZE[1] - fitted.height) // 2,
            ),
        )
        draw.text((x + 10, y + CARD_SIZE[1] + 13), label, fill=TEXT, font=font)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=94)
    return output_path


def resolve_from(base: Path, value: Path) -> Path:
    return value if value.is_absolute() else base / value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--anchor", type=Path)
    args = parser.parse_args()
    request = resolve_from(ROOT, args.request)
    output = resolve_from(ROOT, args.output)
    anchor = (
        resolve_from(PACKAGE_ROOT, args.anchor)
        if args.anchor is not None
        else None
    )
    result = build_comparison(request, PACKAGE_ROOT, output, anchor)
    print(result.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
