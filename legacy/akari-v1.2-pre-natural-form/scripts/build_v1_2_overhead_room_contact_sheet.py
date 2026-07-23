#!/usr/bin/env python3
from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps, UnidentifiedImageError

from scripts.v1_2_overhead_room_common import POSE_SLOTS, load_json, resolve_path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_DECISIONS = {"accept", "hold", "reject", "unreviewed"}
BACKGROUND = "#f7f3ee"
CARD_BACKGROUND = "#ffffff"
TEXT = "#2b2b2b"
SECONDARY_TEXT = "#666666"
BATCH_CARD_WIDTH, BATCH_IMAGE_HEIGHT = 360, 540
BATCH_LABEL_HEIGHT, BATCH_GAP = 62, 18
FINAL_CARD_WIDTH, FINAL_IMAGE_HEIGHT = 256, 384
FINAL_LABEL_HEIGHT, FINAL_GAP, FINAL_COLUMNS = 28, 14, 5


def load_font(size: int) -> ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(path).is_file():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def select_active_requests(manifest: dict, pose: str) -> list[dict]:
    active_batch = manifest.get("active_batches", {}).get(pose)
    if not active_batch:
        raise ValueError(f"no active request batch for pose: {pose}")
    selected = [
        request
        for request in manifest.get("requests", [])
        if request.get("pose") == pose
        and request.get("batch_id") == active_batch
    ]
    return _validate_batch(selected)


def _validate_batch(requests: list[dict]) -> list[dict]:
    ordered = sorted(requests, key=lambda item: item.get("candidate_number", 0))
    if len(ordered) != 2:
        raise ValueError("a pose batch must contain exactly two requests")
    if len({item.get("pose") for item in ordered}) != 1:
        raise ValueError("a pose batch must share one pose")
    if len({item.get("batch_id") for item in ordered}) != 1:
        raise ValueError("a pose batch must share one batch")
    if [item.get("candidate_number") for item in ordered] != [1, 2]:
        raise ValueError("candidate numbers must be exactly 1, 2")
    revisions = {item.get("revision") for item in ordered}
    if (
        len(revisions) != 1
        or any(type(revision) is not int for revision in revisions)
        or next(iter(revisions)) < 1
    ):
        raise ValueError("a pose batch must share one positive integer revision")
    return ordered


def _prepare_images(
    records: list[dict],
    project_root: Path,
    path_key: str,
    card_size: tuple[int, int],
) -> list[tuple[dict, Image.Image]]:
    prepared = []
    for record in records:
        if not isinstance(record.get(path_key), str):
            raise ValueError(f"record requires {path_key}")
        path = resolve_path(project_root, record[path_key])
        try:
            with Image.open(path) as image:
                image.load()
                if image.mode != "RGB" or image.size != (1024, 1536):
                    raise ValueError(f"candidate must be RGB 1024x1536: {path}")
                contained = ImageOps.contain(
                    image, card_size, Image.Resampling.LANCZOS
                ).copy()
        except (OSError, UnidentifiedImageError):
            raise ValueError(f"missing or unreadable candidate: {path}") from None
        prepared.append((record, contained))
    return prepared


def _save_atomic(sheet: Image.Image, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=f".{output_path.stem}-",
            suffix=output_path.suffix or ".webp",
            dir=output_path.parent,
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
        sheet.save(temporary_path, "WEBP", quality=92, method=6)
        temporary_path.replace(output_path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return output_path


def build_batch_contact_sheet(
    requests: list[dict],
    reviews: dict[str, dict],
    project_root: Path,
    output_path: Path,
) -> Path:
    ordered = _validate_batch(requests)
    cards = _prepare_images(
        ordered,
        project_root,
        "target_path",
        (BATCH_CARD_WIDTH, BATCH_IMAGE_HEIGHT),
    )
    sheet = Image.new(
        "RGB",
        (
            2 * BATCH_CARD_WIDTH + 3 * BATCH_GAP,
            BATCH_IMAGE_HEIGHT + BATCH_LABEL_HEIGHT + 2 * BATCH_GAP,
        ),
        BACKGROUND,
    )
    draw = ImageDraw.Draw(sheet)
    title_font, small_font = load_font(16), load_font(12)
    for index, (request, image) in enumerate(cards):
        decision = reviews.get(request.get("id"), {}).get("decision", "unreviewed")
        if decision not in ALLOWED_DECISIONS:
            raise ValueError(f"invalid review decision: {decision}")
        x, y = BATCH_GAP + index * (BATCH_CARD_WIDTH + BATCH_GAP), BATCH_GAP
        draw.rectangle(
            (x, y, x + BATCH_CARD_WIDTH, y + BATCH_IMAGE_HEIGHT + BATCH_LABEL_HEIGHT),
            fill=CARD_BACKGROUND,
        )
        sheet.paste(image, (x + (BATCH_CARD_WIDTH - image.width) // 2, y))
        draw.text(
            (x + 8, y + BATCH_IMAGE_HEIGHT + 6),
            f"{request['pose']} / r{request['revision']} / c{request['candidate_number']}",
            fill=TEXT,
            font=title_font,
        )
        draw.text(
            (x + 8, y + BATCH_IMAGE_HEIGHT + 33),
            decision,
            fill=SECONDARY_TEXT,
            font=small_font,
        )
    return _save_atomic(sheet, output_path)


def _validate_final_records(accepted_records: list[dict]) -> list[dict]:
    if len(accepted_records) != 10:
        raise ValueError("final sheet requires exactly ten accepted works")
    poses = [record.get("pose") for record in accepted_records]
    if len(set(poses)) != 10 or set(poses) != set(POSE_SLOTS):
        raise ValueError("final sheet requires every canonical pose exactly once")
    if any(
        type(record.get("pose_order")) is not int
        or record["pose_order"] != POSE_SLOTS.index(record["pose"]) + 1
        for record in accepted_records
    ):
        raise ValueError("accepted works require canonical pose order")
    return sorted(accepted_records, key=lambda record: record["pose_order"])


def build_final_contact_sheet(
    accepted_records: list[dict],
    project_root: Path,
    output_path: Path,
) -> Path:
    ordered = _validate_final_records(accepted_records)
    cards = _prepare_images(
        ordered,
        project_root,
        "finished_path",
        (FINAL_CARD_WIDTH, FINAL_IMAGE_HEIGHT),
    )
    rows = 2
    width = FINAL_COLUMNS * FINAL_CARD_WIDTH + (FINAL_COLUMNS + 1) * FINAL_GAP
    height = rows * (FINAL_IMAGE_HEIGHT + FINAL_LABEL_HEIGHT) + (rows + 1) * FINAL_GAP
    sheet = Image.new("RGB", (width, height), BACKGROUND)
    draw, font = ImageDraw.Draw(sheet), load_font(12)
    for index, (record, image) in enumerate(cards):
        column, row = index % FINAL_COLUMNS, index // FINAL_COLUMNS
        x = FINAL_GAP + column * (FINAL_CARD_WIDTH + FINAL_GAP)
        y = FINAL_GAP + row * (FINAL_IMAGE_HEIGHT + FINAL_LABEL_HEIGHT + FINAL_GAP)
        draw.rectangle(
            (x, y, x + FINAL_CARD_WIDTH, y + FINAL_IMAGE_HEIGHT + FINAL_LABEL_HEIGHT),
            fill=CARD_BACKGROUND,
        )
        sheet.paste(image, (x + (FINAL_CARD_WIDTH - image.width) // 2, y))
        draw.text(
            (x + 6, y + FINAL_IMAGE_HEIGHT + 6),
            f"{record['pose_order']:02d}  {record['pose']}",
            fill=TEXT,
            font=font,
        )
    return _save_atomic(sheet, output_path)


def _load_review_decisions(review_paths: list[Path]) -> dict[str, dict]:
    decisions = {}
    for path in review_paths:
        for candidate in load_json(path).get("candidates", []):
            request_id = candidate.get("request_id")
            if not request_id or request_id in decisions:
                raise ValueError(f"duplicate or missing review decision: {request_id}")
            decisions[request_id] = candidate
    return decisions


def _rooted(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Akari v1.2 overhead-room contact sheets."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--requests", type=Path)
    source.add_argument("--accepted", type=Path)
    parser.add_argument("--pose", choices=POSE_SLOTS)
    parser.add_argument("--review", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output = _rooted(args.output)
    if args.requests:
        if args.pose is None:
            raise ValueError("--pose is required with --requests")
        result = build_batch_contact_sheet(
            select_active_requests(load_json(_rooted(args.requests)), args.pose),
            _load_review_decisions([_rooted(path) for path in args.review]),
            ROOT,
            output,
        )
    else:
        if args.pose is not None or args.review:
            raise ValueError("--pose and --review are only valid with --requests")
        result = build_final_contact_sheet(
            load_json(_rooted(args.accepted))["accepted_works"], ROOT, output
        )
    try:
        display_path = result.relative_to(ROOT).as_posix()
    except ValueError:
        display_path = result.as_posix()
    print(f"Wrote {display_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
