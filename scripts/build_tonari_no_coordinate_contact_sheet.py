#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REQUESTS_PATH = ROOT / "source/manifests/tonari-no-coordinate/generation-requests.json"
DEFAULT_OUTPUT = (
    ROOT
    / "evidence/tonari-no-coordinate/contact-sheets/tonari-no-coordinate-first-batch.webp"
)
BACKGROUND = "#f7f3ee"
CARD_BACKGROUND = "#ffffff"
TEXT = "#2b2b2b"
SUBTEXT = "#666666"
CJK_FONT_PATHS = (
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
)
LATIN_FALLBACK_FONT_PATHS = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
)


def mask_signature(font: ImageFont.ImageFont, text: str) -> tuple[tuple[int, int], bytes]:
    mask = font.getmask(text)
    return mask.size, bytes(mask)


def supports_coordinate_label_text(font: ImageFont.ImageFont) -> bool:
    return (
        mask_signature(font, "spring") != mask_signature(font, "□□□□□□")
        and mask_signature(font, "春") != mask_signature(font, "□")
    )


def load_requests(path: Path) -> list[dict]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    return manifest["requests"]


def resolve_candidate_path(project_root: Path, target_path: str) -> Path:
    path = Path(target_path)
    if path.is_absolute():
        return path
    return project_root / path


def load_font(size: int) -> ImageFont.ImageFont:
    first_available = None
    for font_path in CJK_FONT_PATHS + LATIN_FALLBACK_FONT_PATHS:
        candidate = Path(font_path)
        if candidate.is_file():
            font = ImageFont.truetype(candidate.as_posix(), size=size)
            if first_available is None:
                first_available = font
            if supports_coordinate_label_text(font):
                return font
    if first_available is not None:
        return first_available
    return ImageFont.load_default()


def fit_image(image: Image.Image, thumb_width: int) -> Image.Image:
    image = image.convert("RGB")
    ratio = thumb_width / image.width
    thumb_height = int(round(image.height * ratio))
    return image.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)


def text_width(text: str, font: ImageFont.ImageFont) -> int:
    if hasattr(font, "getlength"):
        return math.ceil(font.getlength(text))
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]


def fit_text_to_width(text: str, font: ImageFont.ImageFont, max_width: int) -> str:
    if max_width <= 0:
        return ""
    if text_width(text, font) <= max_width:
        return text

    ellipsis = "..."
    if text_width(ellipsis, font) > max_width:
        return ""

    low = 0
    high = len(text)
    best = ellipsis
    while low <= high:
        midpoint = (low + high) // 2
        candidate = f"{text[:midpoint].rstrip()}{ellipsis}"
        if text_width(candidate, font) <= max_width:
            best = candidate
            low = midpoint + 1
        else:
            high = midpoint - 1
    return best


def label_lines_for(
    request: dict,
    font: ImageFont.ImageFont,
    small_font: ImageFont.ImageFont,
    max_width: int,
) -> tuple[str, str]:
    family = request["outfit_family"].replace("_", " ")
    return (
        fit_text_to_width(request["japanese_title"], font, max_width),
        fit_text_to_width(f"{request['slot']} / {family}", small_font, max_width),
    )


def draw_label(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    request: dict,
    font: ImageFont.ImageFont,
    small_font: ImageFont.ImageFont,
    max_width: int,
) -> None:
    x, y = xy
    title, detail = label_lines_for(request, font, small_font, max_width)
    draw.text((x, y), title, fill=TEXT, font=font)
    draw.text((x, y + 22), detail, fill=SUBTEXT, font=small_font)


def existing_request_images(requests: list[dict], project_root: Path) -> list[tuple[dict, Path]]:
    found = []
    for request in requests:
        image_path = resolve_candidate_path(project_root, request["target_path"])
        if image_path.is_file():
            found.append((request, image_path))
    return found


def display_output_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def build_contact_sheet(
    requests: list[dict],
    project_root: Path,
    output_path: Path,
    columns: int = 4,
    thumb_width: int = 280,
    label_height: int = 56,
    gap: int = 20,
) -> Path:
    if columns < 1:
        raise ValueError("columns must be at least 1")

    found = existing_request_images(requests, project_root)
    if not found:
        raise ValueError("No generated coordinate images found")

    prepared = []
    for request, image_path in found:
        with Image.open(image_path) as image:
            thumbnail = fit_image(image, thumb_width)
        prepared.append((request, thumbnail))

    thumb_height = max(thumbnail.height for _, thumbnail in prepared)
    card_width = thumb_width
    card_height = thumb_height + label_height
    rows = math.ceil(len(prepared) / columns)
    sheet_width = columns * card_width + (columns + 1) * gap
    sheet_height = rows * card_height + (rows + 1) * gap
    sheet = Image.new("RGB", (sheet_width, sheet_height), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    font = load_font(16)
    small_font = load_font(13)
    label_text_width = card_width - 16

    for index, (request, thumbnail) in enumerate(prepared):
        row = index // columns
        column = index % columns
        x = gap + column * (card_width + gap)
        y = gap + row * (card_height + gap)
        draw.rectangle((x, y, x + card_width, y + card_height), fill=CARD_BACKGROUND)
        image_y = y
        if thumbnail.height < thumb_height:
            image_y += (thumb_height - thumbnail.height) // 2
        sheet.paste(thumbnail, (x, image_y))
        draw_label(
            draw,
            (x + 8, y + thumb_height + 6),
            request,
            font,
            small_font,
            label_text_width,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=92)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a contact sheet for Tonari no Coordinate candidates."
    )
    parser.add_argument("--requests", type=Path, default=REQUESTS_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--columns", type=int, default=4)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requests = load_requests(args.requests)
    output_path = args.output
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    result = build_contact_sheet(
        requests=requests,
        project_root=ROOT,
        output_path=output_path,
        columns=args.columns,
    )
    print(f"Wrote {display_output_path(result)}")


if __name__ == "__main__":
    main()
