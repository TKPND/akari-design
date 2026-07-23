#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import statistics
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

from scripts.v1_2_turnaround_common import load_json, resolve_path


ROOT = Path(__file__).resolve().parents[1]
REQUESTS_PATH = (
    ROOT / "source/manifests/v1-2-turnaround/generation-requests.json"
)
ACCEPTED_PATH = ROOT / "source/manifests/v1-2-turnaround/accepted-angles.json"
DEFAULT_OUTPUT = (
    ROOT / "evidence/v1-2-turnaround/contact-sheets/turnaround.webp"
)
BACKGROUND = "#f7f3ee"
CARD_BACKGROUND = "#ffffff"
TEXT = "#2b2b2b"
GUIDE = "#4e9d92"
LANDMARK_NAMES = (
    "crown",
    "chin",
    "shoulder",
    "hoodie_hem",
    "skirt_hem",
    "knee",
    "ankle",
    "sole",
)
COUNTERPART_PAIRS = (
    (
        "character-left-front-three-quarter",
        "character-right-front-three-quarter",
    ),
    ("character-left-profile", "character-right-profile"),
    (
        "character-left-rear-three-quarter",
        "character-right-rear-three-quarter",
    ),
)


def load_font(size: int) -> ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(path).is_file():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def prepared_image(
    path: Path,
    size: tuple[int, int] = (360, 540),
) -> Image.Image:
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        return ImageOps.contain(rgb, size, Image.Resampling.LANCZOS)


def build_stage_contact_sheet(
    requests: list[dict],
    project_root: Path,
    output_path: Path,
    columns: int = 3,
    enforce_stage_shape: bool = True,
) -> Path:
    if columns < 1:
        raise ValueError("columns must be at least 1")
    if not requests:
        raise ValueError("No active v1.2 turnaround requests selected")
    grouped: dict[str, list[dict]] = {}
    for request in requests:
        grouped.setdefault(request["slot"], []).append(request)
    if enforce_stage_shape:
        if len(grouped) not in {1, 2}:
            raise ValueError(
                "a stage sheet must contain one slot or one counterpart pair"
            )
        for slot, slot_requests in grouped.items():
            if len(slot_requests) not in {2, 3}:
                raise ValueError(
                    f"{slot} must contain exactly two or three candidates"
                )
            if len({request["batch_id"] for request in slot_requests}) != 1:
                raise ValueError(f"{slot} mixes request batches")
    found = []
    missing = []
    for request in requests:
        path = resolve_path(project_root, request["target_path"])
        if path.is_file():
            found.append((request, path))
        else:
            missing.append(request["target_path"])
    if missing:
        raise ValueError("missing requested candidate: " + ", ".join(missing))
    card_width, image_height, label_height, gap = 360, 540, 62, 18
    rows = math.ceil(len(found) / columns)
    sheet = Image.new(
        "RGB",
        (
            columns * card_width + (columns + 1) * gap,
            rows * (image_height + label_height) + (rows + 1) * gap,
        ),
        BACKGROUND,
    )
    draw = ImageDraw.Draw(sheet)
    title_font = load_font(16)
    small_font = load_font(12)
    for index, (request, path) in enumerate(found):
        row, column = divmod(index, columns)
        x = gap + column * (card_width + gap)
        y = gap + row * (image_height + label_height + gap)
        draw.rectangle(
            (x, y, x + card_width, y + image_height + label_height),
            fill=CARD_BACKGROUND,
        )
        image = prepared_image(path, (card_width, image_height))
        sheet.paste(image, (x + (card_width - image.width) // 2, y))
        draw.text(
            (x + 8, y + image_height + 6),
            (
                f"{request['japanese_title']} / r{request['revision']} "
                f"/ c{request['candidate_number']}"
            ),
            fill=TEXT,
            font=title_font,
        )
        draw.text(
            (x + 8, y + image_height + 31),
            request["slot"],
            fill="#666666",
            font=small_font,
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=92, method=6)
    return output_path


def validate_landmark_ratios(
    accepted_records: list[dict],
    pair_tolerance: float = 0.02,
    set_tolerance: float = 0.03,
) -> list[str]:
    errors = []
    by_slot = {record["slot"]: record for record in accepted_records}
    for left_slot, right_slot in COUNTERPART_PAIRS:
        if left_slot not in by_slot or right_slot not in by_slot:
            continue
        for landmark in LANDMARK_NAMES:
            delta = abs(
                by_slot[left_slot]["normalized_landmarks"][landmark]
                - by_slot[right_slot]["normalized_landmarks"][landmark]
            )
            if delta > pair_tolerance:
                errors.append(
                    f"counterpart {landmark} drift {left_slot} vs "
                    f"{right_slot}: {delta:.4f}"
                )
    for landmark in LANDMARK_NAMES:
        values = [
            record["normalized_landmarks"][landmark]
            for record in accepted_records
        ]
        if values and max(values) - min(values) > set_tolerance:
            errors.append(
                f"full-set {landmark} drift: {max(values) - min(values):.4f}"
            )
    return errors


def select_active_requests(
    manifest: dict,
    selected_slots: list[str] | None,
    selected_batch_ids: list[str] | None,
) -> list[dict]:
    slots = selected_slots or list(manifest["active_batches"])
    batches = set(
        selected_batch_ids
        or [manifest["active_batches"][slot] for slot in slots]
    )
    return [
        request
        for request in manifest["requests"]
        if request["slot"] in slots and request["batch_id"] in batches
    ]


def build_final_contact_sheet(
    accepted_records: list[dict],
    project_root: Path,
    output_path: Path,
) -> Path:
    errors = validate_landmark_ratios(accepted_records)
    if errors:
        raise ValueError("landmark validation failed: " + "; ".join(errors))
    ordered = sorted(accepted_records, key=lambda record: record["angle_order"])
    requests = [
        {
            "slot": record["slot"],
            "candidate_number": record["candidate_number"],
            "revision": record["revision"],
            "batch_id": record["batch_id"],
            "japanese_title": record["japanese_title"],
            "target_path": record["accepted_path"],
        }
        for record in ordered
    ]
    result = build_stage_contact_sheet(
        requests,
        project_root,
        output_path,
        columns=4,
        enforce_stage_shape=False,
    )
    with Image.open(result) as opened:
        sheet = opened.convert("RGB")
    draw = ImageDraw.Draw(sheet)
    if ordered:
        top_margin = 18
        card_height = 540 + 62
        for row in range(math.ceil(len(ordered) / 4)):
            row_y = top_margin + row * (card_height + 18)
            row_records = ordered[row * 4 : (row + 1) * 4]
            for landmark in LANDMARK_NAMES:
                canvas_positions = []
                for record in row_records:
                    crown = record["landmark_y_px"]["crown"]
                    sole = record["landmark_y_px"]["sole"]
                    normalized = record["normalized_landmarks"][landmark]
                    canvas_positions.append(
                        crown + normalized * (sole - crown)
                    )
                y = row_y + round(
                    statistics.median(canvas_positions) / 1536 * 540
                )
                draw.line((0, y, sheet.width, y), fill=GUIDE, width=1)
    sheet.save(result, quality=92, method=6)
    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Akari v1.2 turnaround contact sheets."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--requests", type=Path)
    source.add_argument("--accepted", type=Path)
    parser.add_argument("--slot", action="append")
    parser.add_argument("--batch-id", action="append")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--columns", type=int, default=3)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if args.requests:
        manifest = load_json(args.requests)
        requests = select_active_requests(manifest, args.slot, args.batch_id)
        result = build_stage_contact_sheet(
            requests,
            ROOT,
            output,
            args.columns,
        )
    else:
        result = build_final_contact_sheet(
            load_json(args.accepted)["accepted_angles"],
            ROOT,
            output,
        )
    print(f"Wrote {result.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
