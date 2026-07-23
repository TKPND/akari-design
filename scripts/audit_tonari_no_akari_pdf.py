#!/usr/bin/env python3
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAGE_MANIFEST = ROOT / "source/manifests/tonari-no-akari/page-manifest.json"
RENDER_DIR = ROOT / "build/tonari-no-akari-pdf-rendered-pages"
TEXT_DIR = ROOT / "dist/akari-v1.1-tonari-no-akari-pages"
TEXT_OUTPUT = TEXT_DIR / "document.txt"
EXPECTED_PAGE_COUNT = 24
EXPECTED_DOCUMENT_TITLE = "となりのあかり"
EXPECTED_A4_SIZE_PT = (595.28, 841.89)
A4_SIZE_TOLERANCE_PT = 3.0
A4_RATIO_TOLERANCE = 0.01
RENDER_DPI = 288
RENDER_SIZE_TOLERANCE_PX = 2
CONTENT_SAMPLE_SIZE = (108, 152)
MIN_CONTENT_RATIO = 0.003
PAGES_RE = re.compile(r"^Pages:\s+([0-9]+)\s*$", re.MULTILINE)
TITLE_RE = re.compile(r"^Title:\s+(.+?)\s*$", re.MULTILINE)
PAGE_SIZE_RE = re.compile(
    r"^Page size:\s+([0-9]+(?:\.[0-9]+)?) x ([0-9]+(?:\.[0-9]+)?) pts",
    re.MULTILINE,
)
RENDERED_PAGE_RE = re.compile(r"^page-([0-9]+)\.png$")


class AuditError(Exception):
    pass


def project_path(path_arg: str) -> Path:
    path = Path(path_arg)
    if path.is_absolute():
        return path
    return ROOT / path


def run_command(command: list[str], label: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:
        raise AuditError(f"{label} failed: command not found: {command[0]}") from error
    except subprocess.CalledProcessError as error:
        details = "\n".join(
            part.strip()
            for part in (error.stdout, error.stderr)
            if part and part.strip()
        )
        message = f"{label} failed"
        if details:
            message = f"{message}:\n{details}"
        raise AuditError(message) from error


def pdfinfo_page_size(pdfinfo_output: str) -> tuple[float, float]:
    match = PAGE_SIZE_RE.search(pdfinfo_output)
    if not match:
        raise AuditError("pdfinfo must report page size in points")
    return float(match.group(1)), float(match.group(2))


def require_pdfinfo_contract(pdfinfo_output: str) -> None:
    title_match = TITLE_RE.search(pdfinfo_output)
    if not title_match:
        raise AuditError("pdfinfo must report document title")
    title = title_match.group(1)
    if title != EXPECTED_DOCUMENT_TITLE:
        raise AuditError(
            f"pdfinfo must report title {EXPECTED_DOCUMENT_TITLE}, got {title}"
        )

    pages_match = PAGES_RE.search(pdfinfo_output)
    if not pages_match:
        raise AuditError("pdfinfo must report page count")
    page_count = int(pages_match.group(1))
    if page_count != EXPECTED_PAGE_COUNT:
        raise AuditError(
            f"pdfinfo must report {EXPECTED_PAGE_COUNT} pages, got {page_count}"
        )

    width, height = pdfinfo_page_size(pdfinfo_output)
    expected_width, expected_height = EXPECTED_A4_SIZE_PT
    ratio = width / height if height else 0
    expected_ratio = expected_width / expected_height
    is_a4_size = (
        abs(width - expected_width) <= A4_SIZE_TOLERANCE_PT
        and abs(height - expected_height) <= A4_SIZE_TOLERANCE_PT
    )
    is_a4_ratio = abs(ratio - expected_ratio) <= A4_RATIO_TOLERANCE
    if width >= height or not is_a4_size or not is_a4_ratio:
        raise AuditError(
            f"pdf pages must use A4 portrait size, got {width:g} x {height:g} pts"
        )


def require_font_table(pdffonts_output: str) -> None:
    lines = [line for line in pdffonts_output.splitlines() if line.strip()]
    if len(lines) < 3 or not lines[0].lower().startswith("name"):
        raise AuditError("pdffonts must report at least one font table row")
    font_rows = lines[2:]
    bad_rows = []
    for row in font_rows:
        tokens = row.split()
        if len(tokens) < 7:
            bad_rows.append(row)
            continue
        emb = tokens[-5]
        uni = tokens[-3]
        if emb.lower() != "yes" or uni.lower() != "yes":
            bad_rows.append(row)
    if bad_rows:
        raise AuditError(
            "pdffonts must report embedded Unicode fonts; failing rows: "
            + "; ".join(bad_rows)
        )


def clear_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def rendered_page_sort_key(path: Path) -> int:
    match = RENDERED_PAGE_RE.match(path.name)
    if not match:
        raise AuditError(f"rendered page file has unexpected name: {path.name}")
    return int(match.group(1))


def render_pages(pdf: Path) -> list[Path]:
    clear_directory(RENDER_DIR)
    prefix = RENDER_DIR / "page"
    run_command(
        ["pdftoppm", "-png", "-r", str(RENDER_DPI), str(pdf), str(prefix)],
        "pdftoppm render",
    )
    pages = sorted(RENDER_DIR.glob("page-*.png"), key=rendered_page_sort_key)
    if len(pages) != EXPECTED_PAGE_COUNT:
        raise AuditError(
            f"expected {EXPECTED_PAGE_COUNT} rendered PNG pages, got {len(pages)}"
        )
    return pages


def expected_render_size_from_points(
    width_pt: float, height_pt: float, dpi: int = RENDER_DPI
) -> tuple[int, int]:
    return round(width_pt / 72 * dpi), round(height_pt / 72 * dpi)


def require_rendered_page_sizes(
    pages: list[Path], expected_size: tuple[int, int]
) -> None:
    expected_width, expected_height = expected_size
    for page in pages:
        with Image.open(page) as image:
            width, height = image.size
        width_delta = abs(width - expected_width)
        height_delta = abs(height - expected_height)
        if (
            width >= height
            or width_delta > RENDER_SIZE_TOLERANCE_PX
            or height_delta > RENDER_SIZE_TOLERANCE_PX
        ):
            raise AuditError(
                f"{page.name} must be A4 portrait near "
                f"{expected_width}x{expected_height}, got {width}x{height}"
            )


def rendered_content_ratio(page: Path) -> float:
    with Image.open(page) as image:
        sample = image.convert("RGB").resize(CONTENT_SAMPLE_SIZE)
    background = sample.getpixel((0, 0))
    if hasattr(sample, "get_flattened_data"):
        pixels = list(sample.get_flattened_data())
    else:
        pixels = list(sample.getdata())
    changed = 0
    for pixel in pixels:
        delta = sum(abs(channel - base) for channel, base in zip(pixel, background))
        if delta > 24:
            changed += 1
    return changed / len(pixels)


def require_rendered_page_content(pages: list[Path]) -> None:
    for page in pages:
        ratio = rendered_content_ratio(page)
        if ratio < MIN_CONTENT_RATIO:
            raise AuditError(
                f"{page.name} appears blank or near-blank: content ratio {ratio:.4f}"
            )


def extract_text(pdf: Path) -> str:
    clear_directory(TEXT_DIR)
    run_command(["pdftotext", str(pdf), str(TEXT_OUTPUT)], "pdftotext")
    return TEXT_OUTPUT.read_text(encoding="utf-8")


def normalize_searchable_text(value: str) -> str:
    return re.sub(r"\s+", "", value).strip().casefold()


def load_required_text_from_manifest(manifest_path: Path = PAGE_MANIFEST) -> tuple[str, ...]:
    with manifest_path.open(encoding="utf-8") as manifest_file:
        manifest = json.load(manifest_file)

    if manifest.get("title") != "となりのあかり":
        raise AuditError("Tonari page manifest must use title: となりのあかり")
    if manifest.get("page_count") != EXPECTED_PAGE_COUNT:
        raise AuditError(
            f"Tonari page manifest must declare {EXPECTED_PAGE_COUNT} pages"
        )

    pages = manifest.get("pages")
    if not isinstance(pages, list) or len(pages) != EXPECTED_PAGE_COUNT:
        raise AuditError(
            f"Tonari page manifest must include {EXPECTED_PAGE_COUNT} page entries"
        )

    titles = []
    display_lines = []
    for expected_page, page in enumerate(pages, start=1):
        if page.get("page") != expected_page:
            raise AuditError(
                "Tonari page manifest pages must be ordered from 1 to "
                f"{EXPECTED_PAGE_COUNT}"
            )
        title = page.get("title")
        display_line = page.get("display_line")
        if not title or not display_line:
            raise AuditError(
                f"Tonari page {expected_page} must include title and display_line"
            )
        titles.append(title)
        display_lines.append(display_line)

    return (*titles, *display_lines)


def require_searchable_text(text: str) -> None:
    normalized_text = normalize_searchable_text(text)
    missing = [
        needle
        for needle in load_required_text_from_manifest()
        if normalize_searchable_text(needle) not in normalized_text
    ]
    if missing:
        raise AuditError(f"searchable text missing: {', '.join(missing)}")


def audit_tonari_no_akari_pdf(pdf: Path) -> None:
    if not pdf.exists():
        raise AuditError(f"PDF missing: {pdf}")
    if not pdf.is_file():
        raise AuditError(f"PDF path is not a file: {pdf}")

    run_command(["qpdf", "--check", str(pdf)], "qpdf check")
    pdfinfo = run_command(["pdfinfo", str(pdf)], "pdfinfo")
    require_pdfinfo_contract(pdfinfo.stdout)
    pdf_page_size = pdfinfo_page_size(pdfinfo.stdout)

    pdffonts = run_command(["pdffonts", str(pdf)], "pdffonts")
    require_font_table(pdffonts.stdout)

    pages = render_pages(pdf)
    require_rendered_page_sizes(
        pages, expected_render_size_from_points(*pdf_page_size)
    )
    require_rendered_page_content(pages)

    text = extract_text(pdf)
    require_searchable_text(text)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            "usage: audit_tonari_no_akari_pdf.py "
            "dist/akari-v1.1-tonari-no-akari.pdf",
            file=sys.stderr,
        )
        return 2

    try:
        audit_tonari_no_akari_pdf(project_path(argv[1]))
    except AuditError as error:
        print(f"tonari no akari pdf audit: failed: {error}", file=sys.stderr)
        return 1

    print("tonari no akari pdf audit: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
