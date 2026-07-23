from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps
import yaml

if __package__:
    from scripts.build_v1_2_candidate_comparison import (
        BACKGROUND,
        CARD_BACKGROUND,
        CARD_SIZE,
        GAP,
        LABEL_HEIGHT,
        TEXT,
        load_font,
    )
else:
    from build_v1_2_candidate_comparison import (
        BACKGROUND,
        CARD_BACKGROUND,
        CARD_SIZE,
        GAP,
        LABEL_HEIGHT,
        TEXT,
        load_font,
    )


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"
VIEW_ORDER = ("hairpin-side-45", "non-hairpin-side-45")


def render_grid(rows: list[list[tuple[str, Path]]], output_path: Path) -> Path:
    column_count = len(rows[0])
    row_height = CARD_SIZE[1] + LABEL_HEIGHT
    width = GAP * (column_count + 1) + CARD_SIZE[0] * column_count
    height = GAP * (len(rows) + 1) + row_height * len(rows)
    sheet = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    font = load_font(16)
    for row_index, row in enumerate(rows):
        for column_index, (label, source) in enumerate(row):
            if not source.is_file():
                raise ValueError(f"missing {source.name}")
            x = GAP + column_index * (CARD_SIZE[0] + GAP)
            y = GAP + row_index * (row_height + GAP)
            draw.rectangle(
                (x, y, x + CARD_SIZE[0], y + row_height),
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
            draw.text(
                (x + 10, y + CARD_SIZE[1] + 13),
                label,
                fill=TEXT,
                font=font,
            )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=94)
    return output_path


def build_c03_comparison(
    request_path: Path,
    package_root: Path,
    output_path: Path,
    alignment: bool = False,
) -> Path:
    request = yaml.safe_load(request_path.read_text(encoding="utf-8"))
    candidates = request["candidates"]
    if [candidate.get("variant") for candidate in candidates] != ["a", "b", "c"]:
        raise ValueError("expected candidates a, b, c")

    pair_rows: list[list[tuple[str, Path]]] = []
    for candidate in candidates:
        outputs = candidate.get("outputs")
        if not isinstance(outputs, list) or [
            output.get("view") for output in outputs
        ] != list(VIEW_ORDER):
            raise ValueError("expected paired view order")
        pair_rows.append(
            [
                (
                    f"{candidate['variant'].upper()}  {output['view']}",
                    package_root / output["target_path"],
                )
                for output in outputs
            ]
        )

    if not alignment:
        return render_grid(pair_rows, output_path)

    anchors = request.get("comparison_anchors")
    if not isinstance(anchors, list) or len(anchors) != 2:
        raise ValueError("expected C01 and C02 comparison anchors")
    c01_anchor, c02_anchor = (package_root / path for path in anchors)
    rows = [
        [
            ("C01  accepted front", c01_anchor),
            pair_row[0],
            ("C02  accepted back", c02_anchor),
            pair_row[1],
        ]
        for pair_row in pair_rows
    ]
    return render_grid(rows, output_path)


def resolve_from(base: Path, value: Path) -> Path:
    return value if value.is_absolute() else base / value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--alignment", action="store_true")
    args = parser.parse_args()
    request = resolve_from(ROOT, args.request)
    output = resolve_from(ROOT, args.output)
    result = build_c03_comparison(
        request,
        PACKAGE_ROOT,
        output,
        alignment=args.alignment,
    )
    print(result.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
