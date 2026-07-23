#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps, UnidentifiedImageError

from scripts.v1_2_motion_common import load_json, resolve_path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REQUESTS_PATH = (
    ROOT / "source/manifests/v1-2-motion/generation-requests.json"
)
DEFAULT_ACCEPTED_PATH = (
    ROOT / "source/manifests/v1-2-motion/accepted-selection.json"
)
CARD_WIDTH = 360
IMAGE_HEIGHT = 540
LABEL_HEIGHT = 62
GAP = 18
BACKGROUND = "#f7f3ee"
CARD_BACKGROUND = "#ffffff"
TEXT = "#2b2b2b"
SECONDARY_TEXT = "#666666"
MOTION_ORDER = {"walking": 1, "seated": 2, "turning": 3}
ALLOWED_DECISIONS = {"accept", "hold", "reject"}


def load_font(size: int) -> ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(path).is_file():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def select_active_requests(manifest: dict, motion: str) -> list[dict]:
    active_batch = manifest.get("active_batches", {}).get(motion)
    if not active_batch:
        raise ValueError(f"no active request batch for motion: {motion}")
    selected = [
        request
        for request in manifest.get("requests", [])
        if request.get("motion") == motion
        and request.get("batch_id") == active_batch
    ]
    return sorted(selected, key=lambda request: request["candidate_number"])


def _validate_batch(requests: list[dict]) -> list[dict]:
    ordered = sorted(requests, key=lambda request: request["candidate_number"])
    if len(ordered) != 3:
        raise ValueError("a motion batch must contain exactly three requests")
    if len({request.get("motion") for request in ordered}) != 1:
        raise ValueError("a motion batch must share one motion")
    if len({request.get("batch_id") for request in ordered}) != 1:
        raise ValueError("a motion batch must share one batch")
    if [request.get("candidate_number") for request in ordered] != [1, 2, 3]:
        raise ValueError("candidate numbers must be exactly 1, 2, 3")
    revisions = {request.get("revision") for request in ordered}
    if (
        len(revisions) != 1
        or any(type(revision) is not int for revision in revisions)
        or next(iter(revisions)) < 1
    ):
        raise ValueError(
            "a motion batch must share the same positive integer revision"
        )
    return ordered


def _prepare_images(
    records: list[dict], project_root: Path, path_key: str
) -> list[tuple[dict, Image.Image]]:
    prepared = []
    for record in records:
        path = resolve_path(project_root, record[path_key])
        try:
            with Image.open(path) as image:
                image.load()
                if image.mode != "RGB" or image.size != (1024, 1536):
                    raise ValueError(
                        f"candidate must be RGB 1024x1536: {path}"
                    )
                contained = ImageOps.contain(
                    image,
                    (CARD_WIDTH, IMAGE_HEIGHT),
                    Image.Resampling.LANCZOS,
                )
        except (OSError, UnidentifiedImageError):
            raise ValueError(
                f"missing or unreadable candidate: {path}"
            ) from None
        prepared.append((record, contained))
    return prepared


def _render_sheet(
    cards: list[tuple[dict, Image.Image]],
    labels: list[tuple[str, str]],
    output_path: Path,
) -> Path:
    sheet = Image.new(
        "RGB",
        (
            len(cards) * CARD_WIDTH + (len(cards) + 1) * GAP,
            IMAGE_HEIGHT + LABEL_HEIGHT + 2 * GAP,
        ),
        BACKGROUND,
    )
    draw = ImageDraw.Draw(sheet)
    title_font = load_font(16)
    small_font = load_font(12)
    for index, ((_, image), (title, subtitle)) in enumerate(
        zip(cards, labels, strict=True)
    ):
        x = GAP + index * (CARD_WIDTH + GAP)
        y = GAP
        draw.rectangle(
            (x, y, x + CARD_WIDTH, y + IMAGE_HEIGHT + LABEL_HEIGHT),
            fill=CARD_BACKGROUND,
        )
        sheet.paste(image, (x + (CARD_WIDTH - image.width) // 2, y))
        draw.text(
            (x + 8, y + IMAGE_HEIGHT + 6),
            title,
            fill=TEXT,
            font=title_font,
        )
        draw.text(
            (x + 8, y + IMAGE_HEIGHT + 31),
            subtitle,
            fill=SECONDARY_TEXT,
            font=small_font,
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=92, method=6)
    return output_path


def build_batch_contact_sheet(
    requests: list[dict],
    reviews: dict[str, dict],
    project_root: Path,
    output_path: Path,
) -> Path:
    ordered = _validate_batch(requests)
    cards = _prepare_images(ordered, project_root, "target_path")
    labels = []
    for request in ordered:
        review = reviews.get(request.get("id"), {})
        decision = review.get("decision", "unreviewed")
        if decision not in ALLOWED_DECISIONS | {"unreviewed"}:
            raise ValueError(f"invalid review decision: {decision}")
        labels.append(
            (
                f"{request['motion']} / r{request['revision']} "
                f"/ c{request['candidate_number']}",
                decision,
            )
        )
    return _render_sheet(cards, labels, output_path)


def build_final_contact_sheet(
    accepted_records: list[dict],
    project_root: Path,
    output_path: Path,
) -> Path:
    if len(accepted_records) != 3 or {
        record.get("motion") for record in accepted_records
    } != set(MOTION_ORDER):
        raise ValueError(
            "final sheet requires exactly three accepted motions: "
            "walking, seated, turning"
        )
    if any(
        type(record.get("motion_order")) is not int
        or record["motion_order"] != MOTION_ORDER[record["motion"]]
        for record in accepted_records
    ):
        raise ValueError(
            "accepted records require canonical motion_order mapping: "
            "walking=1, seated=2, turning=3"
        )
    ordered = sorted(
        accepted_records, key=lambda record: record["motion_order"]
    )
    if [record.get("motion") for record in ordered] != list(MOTION_ORDER):
        raise ValueError(
            "accepted motions must order walking, seated, turning"
        )
    cards = _prepare_images(ordered, project_root, "finished_path")
    labels = [(record["motion"], "accepted") for record in ordered]
    return _render_sheet(cards, labels, output_path)


def _load_review_decisions(review_paths: list[Path]) -> dict[str, dict]:
    decisions = {}
    for path in review_paths:
        review = load_json(path)
        for candidate in review.get("candidates", []):
            request_id = candidate.get("request_id")
            if request_id in decisions:
                raise ValueError(f"duplicate review decision: {request_id}")
            decisions[request_id] = candidate
    return decisions


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Akari v1.2 motion contact sheets."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--requests", type=Path)
    source.add_argument("--accepted", type=Path)
    parser.add_argument("--motion", choices=tuple(MOTION_ORDER))
    parser.add_argument("--review", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if args.requests:
        if args.motion is None:
            raise ValueError("--motion is required with --requests")
        request_path = (
            args.requests
            if args.requests.is_absolute()
            else ROOT / args.requests
        )
        review_paths = [
            path if path.is_absolute() else ROOT / path for path in args.review
        ]
        result = build_batch_contact_sheet(
            select_active_requests(load_json(request_path), args.motion),
            _load_review_decisions(review_paths),
            ROOT,
            output,
        )
    else:
        if args.motion is not None or args.review:
            raise ValueError(
                "--motion and --review are only valid with --requests"
            )
        accepted_path = (
            args.accepted
            if args.accepted.is_absolute()
            else ROOT / args.accepted
        )
        result = build_final_contact_sheet(
            load_json(accepted_path)["accepted_motions"], ROOT, output
        )
    try:
        display_path = result.relative_to(ROOT).as_posix()
    except ValueError:
        display_path = result.as_posix()
    print(f"Wrote {display_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
