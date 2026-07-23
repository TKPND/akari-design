from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

if __package__:
    from scripts.akari_v1_2_ame_no_sei_ni_shite import load_contract, sha256_file
else:
    from akari_v1_2_ame_no_sei_ni_shite import load_contract, sha256_file


SCOPE_LAYOUTS = {
    "candidates": {"columns": 2, "thumb": (768, 512)},
    "first-pass": {"columns": 3, "thumb": (512, 341)},
    "act-1": {"columns": 3, "thumb": (576, 384)},
    "act-2": {"columns": 2, "thumb": (672, 448)},
    "act-3": {"columns": 3, "thumb": (576, 384)},
    "act-4": {"columns": 2, "thumb": (768, 512)},
    "full": {"columns": 3, "thumb": (512, 341)},
}


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ):
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _sheet(
    entries: list[tuple[Path, list[str]]],
    output: Path,
    layout: dict,
) -> Path:
    columns = layout["columns"]
    thumb_width, thumb_height = layout["thumb"]
    label_height = 112
    gutter = 24
    rows = (len(entries) + columns - 1) // columns
    width = gutter + columns * (thumb_width + gutter)
    height = gutter + rows * (thumb_height + label_height + gutter)
    canvas = Image.new("RGB", (width, height), "#f3efe8")
    draw = ImageDraw.Draw(canvas)
    title_font = _font(26)
    detail_font = _font(18)
    for index, (path, labels) in enumerate(entries):
        column = index % columns
        row = index // columns
        x = gutter + column * (thumb_width + gutter)
        y = gutter + row * (thumb_height + label_height + gutter)
        with Image.open(path) as source:
            tile = ImageOps.fit(
                source.convert("RGB"),
                (thumb_width, thumb_height),
                method=Image.Resampling.LANCZOS,
            )
        canvas.paste(tile, (x, y))
        for line_index, label in enumerate(labels):
            font = title_font if line_index == 0 else detail_font
            draw.text(
                (x, y + thumb_height + 10 + line_index * 28),
                label,
                fill="#292722",
                font=font,
            )
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, "WEBP", quality=90, method=6)
    return output


def build_candidate_sheet(root: Path, scene_id: str) -> Path:
    contract = load_contract(root)
    scene = next(item for item in contract["scenes"] if item["id"] == scene_id)
    entries = []
    for candidate in scene["candidates"]:
        path = contract["package"] / candidate["path"]
        if not path.is_file():
            raise FileNotFoundError(path)
        entries.append(
            (
                path,
                [
                    f"{scene_id} / {candidate['variant'].upper()}",
                    f"{scene['time']}  {scene['wetness']}",
                    scene["lighting"],
                ],
            )
        )
    output = (
        contract["package"]
        / f"evidence/contact-sheets/{scene_id}-r01-candidates.webp"
    )
    return _sheet(entries, output, SCOPE_LAYOUTS["candidates"])


def build_first_pass_sheet(root: Path) -> Path:
    contract = load_contract(root)
    entries = []
    for scene in contract["scenes"]:
        candidate = next(
            item for item in scene["candidates"] if item["variant"] == "a"
        )
        path = contract["package"] / candidate["path"]
        if not path.is_file():
            raise FileNotFoundError(path)
        entries.append(
            (
                path,
                [
                    f"{scene['id']} / {scene['time']} / A",
                    f"{scene['wetness']}  {scene['lighting']}",
                    sha256_file(path)[:12],
                ],
            )
        )
    output = (
        contract["package"]
        / "evidence/contact-sheets/first-pass-continuity.webp"
    )
    return _sheet(entries, output, SCOPE_LAYOUTS["first-pass"])


def _accepted_entries(contract: dict, scenes: list[dict]) -> list[tuple[Path, list[str]]]:
    entries = []
    for scene in scenes:
        if scene["status"] != "accepted":
            raise ValueError(f"accepted scene required: {scene['id']}")
        path = contract["package"] / scene["accepted_path"]
        if not path.is_file():
            raise FileNotFoundError(path)
        entries.append(
            (
                path,
                [
                    f"{scene['id']} / {scene['time']}",
                    f"{scene['wetness']}  {scene['lighting']}",
                    sha256_file(path)[:12],
                ],
            )
        )
    return entries


def build_act_sheet(root: Path, act: int) -> Path:
    contract = load_contract(root)
    scenes = [scene for scene in contract["scenes"] if scene["act"] == act]
    if not scenes:
        raise ValueError(f"unknown act: {act}")
    output = contract["package"] / f"evidence/contact-sheets/act-{act}.webp"
    return _sheet(
        _accepted_entries(contract, scenes),
        output,
        SCOPE_LAYOUTS[f"act-{act}"],
    )


def build_full_sheet(root: Path) -> Path:
    contract = load_contract(root)
    accepted = [
        scene for scene in contract["scenes"] if scene["status"] == "accepted"
    ]
    if len(accepted) != 12:
        raise ValueError("12 accepted scenes required")
    output = contract["package"] / "evidence/contact-sheets/full-continuity.webp"
    return _sheet(
        _accepted_entries(contract, accepted),
        output,
        SCOPE_LAYOUTS["full"],
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scope",
        choices=("candidates", "first-pass", "act", "all-acts", "full"),
        required=True,
    )
    parser.add_argument("--scene")
    parser.add_argument("--act", type=int)
    args = parser.parse_args()
    root = Path.cwd()
    if args.scope == "candidates":
        if not args.scene:
            parser.error("--scene is required for candidates")
        print(build_candidate_sheet(root, args.scene))
    elif args.scope == "first-pass":
        print(build_first_pass_sheet(root))
    elif args.scope == "act":
        if not args.act:
            parser.error("--act is required for act")
        print(build_act_sheet(root, args.act))
    elif args.scope == "all-acts":
        for act in range(1, 5):
            print(build_act_sheet(root, act))
    else:
        print(build_full_sheet(root))


if __name__ == "__main__":
    main()
