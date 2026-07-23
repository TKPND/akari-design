#!/usr/bin/env python3
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RENDER_DIR = ROOT / "build/daybook-pdf-rendered-pages"
TEXT_DIR = ROOT / "dist/akari-v1.1-situation-daybook-pages"
TEXT_OUTPUT = TEXT_DIR / "document.txt"
EXPECTED_PAGE_COUNT = 10
EXPECTED_RENDER_SIZE = (3840, 2160)
CONTENT_SAMPLE_SIZE = (192, 108)
MIN_CONTENT_RATIO = 0.003
REQUIRED_TEXT = (
    "Akari v1.1 Situation Daybook",
    "Lakeside Bench",
    "Footbridge Breeze",
    "Convenience Walk",
    "Dock Edge",
    "Park Steps",
    "Window Seat",
    "Rain-Cooled Street",
    "Station After Sun",
    "Vending Machine Night",
    "Golden Hour Return",
    "Generation Notes",
    "writing",
)
PAGES_RE = re.compile(r"^Pages:\s+([0-9]+)\s*$", re.MULTILINE)
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


def require_pdfinfo_contract(pdfinfo_output: str) -> None:
    pages_match = PAGES_RE.search(pdfinfo_output)
    if not pages_match:
        raise AuditError("pdfinfo must report page count")
    page_count = int(pages_match.group(1))
    if page_count != EXPECTED_PAGE_COUNT:
        raise AuditError(
            f"pdfinfo must report {EXPECTED_PAGE_COUNT} pages, got {page_count}"
        )

    match = PAGE_SIZE_RE.search(pdfinfo_output)
    if not match:
        raise AuditError("pdfinfo must report page size in points")

    width = float(match.group(1))
    height = float(match.group(2))
    if height == 0 or abs((width / height) - (16 / 9)) > 0.001:
        raise AuditError(
            f"pdf pages must use 16:9 aspect ratio, got {width:g} x {height:g} pts"
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
        ["pdftoppm", "-png", "-r", "288", str(pdf), str(prefix)],
        "pdftoppm render",
    )
    pages = sorted(RENDER_DIR.glob("page-*.png"), key=rendered_page_sort_key)
    if len(pages) != EXPECTED_PAGE_COUNT:
        raise AuditError(
            f"expected {EXPECTED_PAGE_COUNT} rendered PNG pages, got {len(pages)}"
        )
    return pages


def require_rendered_page_sizes(pages: list[Path]) -> None:
    for page in pages:
        with Image.open(page) as image:
            if image.size != EXPECTED_RENDER_SIZE:
                width, height = image.size
                raise AuditError(
                    f"{page.name} must be {EXPECTED_RENDER_SIZE[0]}x{EXPECTED_RENDER_SIZE[1]}, "
                    f"got {width}x{height}"
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
    return re.sub(r"\s+", " ", value).strip().lower()


def require_searchable_text(text: str) -> None:
    normalized_text = normalize_searchable_text(text)
    missing = [
        needle
        for needle in REQUIRED_TEXT
        if normalize_searchable_text(needle) not in normalized_text
    ]
    if missing:
        raise AuditError(f"searchable text missing: {', '.join(missing)}")


def audit_daybook_pdf(pdf: Path) -> None:
    if not pdf.exists():
        raise AuditError(f"PDF missing: {pdf}")
    if not pdf.is_file():
        raise AuditError(f"PDF path is not a file: {pdf}")

    run_command(["qpdf", "--check", str(pdf)], "qpdf check")
    pdfinfo = run_command(["pdfinfo", str(pdf)], "pdfinfo")
    require_pdfinfo_contract(pdfinfo.stdout)

    pdffonts = run_command(["pdffonts", str(pdf)], "pdffonts")
    require_font_table(pdffonts.stdout)

    pages = render_pages(pdf)
    require_rendered_page_sizes(pages)
    require_rendered_page_content(pages)

    text = extract_text(pdf)
    require_searchable_text(text)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            "usage: audit_daybook_pdf.py dist/akari-v1.1-situation-daybook.pdf",
            file=sys.stderr,
        )
        return 2

    try:
        audit_daybook_pdf(project_path(argv[1]))
    except AuditError as error:
        print(f"daybook pdf audit: failed: {error}", file=sys.stderr)
        return 1

    print("daybook pdf audit: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
