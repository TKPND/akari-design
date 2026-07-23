#!/usr/bin/env python3
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RENDER_DIR = ROOT / "build/pdf-rendered-pages"
TEXT_DIR = ROOT / "dist/akari-v1.1-settings-pages"
TEXT_OUTPUT = TEXT_DIR / "document.txt"
EXPECTED_PAGE_COUNT = 14
EXPECTED_RENDER_SIZE = (3840, 2160)
AUDIT_LEVELS = {"structure", "raster", "full"}
OCR_PAGE_SIZE = (1440, 810)
CONTENT_SAMPLE_SIZE = (192, 108)
MIN_CONTENT_RATIO = 0.003
REQUIRED_TEXT = (
    "Akari v1.1",
    "D65 Color Palette",
    "Production Notes",
    "Stable mid-calf height",
    "Sock Height Guide",
    "Stripe Placement",
    "Tongue Visibility",
    "Toe Shape",
    "Blue Gray Outsole",
    "Sneaker Construction",
    "Tongue sits slightly above sock line",
    "Rounded toe",
    "Sculpted Sole",
    "Bag Detail Board",
    "Color & Material",
    "Can Fit",
    "W 16cm x H 20cm x D 5cm",
    "Smartphone / A6 notebook",
    "earbuds",
    "Portable Battery",
    "Canvas-like ivory body",
    "Adjustable Strap",
    "Bag-on-body scale",
    "Compact against hoodie",
)
OCR_REQUIRED_TERMS_BY_PAGE = {
    9: (
        "Footwear Sock Board",
        "Sock Height Guide",
        "Stripe Placement",
        "Tongue Visibility",
        "Toe Shape",
        "Design Notes",
        "Blue Gray Outsole",
    ),
    10: (
        "Sneaker Construction",
        "Front View",
        "Back View",
        "Outer Side View",
        "Inner Side View",
        "Top View",
        "Sole",
        "White Laces",
        "Sculpted Sole",
    ),
    11: (
        "Bag Detail Board",
        "Color Material",
        "Smartphone",
        "Small Notebook",
        "Earbuds",
        "Portable Battery",
        "Adjustable Strap",
        "W 16cm x H 20cm",
        "Canvas Like Fabric",
    ),
    12: (
        "Bag On Body Scale",
        "Compact Against Hoodie",
        "Strap Drop",
        "Cross Body Fit",
        "Mini Shoulder Bag",
    ),
}
PAGES_RE = re.compile(r"^Pages:\s+([0-9]+)\s*$", re.MULTILINE)
PAGE_SIZE_RE = re.compile(
    r"^Page size:\s+([0-9]+(?:\.[0-9]+)?) x ([0-9]+(?:\.[0-9]+)?) pts",
    re.MULTILINE,
)


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
        raise AuditError(f"pdf pages must use 16:9 aspect ratio, got {width:g} x {height:g} pts")


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


def render_pages(pdf: Path) -> list[Path]:
    clear_directory(RENDER_DIR)
    prefix = RENDER_DIR / "page"
    run_command(
        ["pdftoppm", "-png", "-r", "288", str(pdf), str(prefix)],
        "pdftoppm render",
    )
    pages = sorted(RENDER_DIR.glob("page-*.png"))
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


def require_searchable_text(text: str) -> None:
    normalized_text = normalize_searchable_text(text)
    missing = [
        needle
        for needle in REQUIRED_TEXT
        if normalize_searchable_text(needle) not in normalized_text
    ]
    if missing:
        raise AuditError(f"searchable text missing: {', '.join(missing)}")


def normalize_searchable_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_ocr_text(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.lower())).strip()


def require_ocr_readability(pages: list[Path]) -> None:
    if shutil.which("tesseract") is None:
        raise AuditError("tesseract is required for 1440px OCR readability audit")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        for page_number, required_terms in OCR_REQUIRED_TERMS_BY_PAGE.items():
            page_path = pages[page_number - 1]
            resized = temp_path / f"{page_path.stem}-1440.png"
            with Image.open(page_path) as image:
                image.convert("RGB").resize(OCR_PAGE_SIZE, Image.Resampling.LANCZOS).save(
                    resized
                )

            ocr = run_command(
                ["tesseract", str(resized), "stdout", "--psm", "6"],
                f"tesseract OCR page {page_number}",
            )
            text = normalize_ocr_text(ocr.stdout)
            missing = [
                term
                for term in required_terms
                if normalize_ocr_text(term) not in text
            ]
            if missing:
                raise AuditError(
                    f"page {page_number} OCR missing required terms at 1440px: "
                    + ", ".join(missing)
                )


def audit_pdf_structure(pdf: Path) -> None:
    run_command(["qpdf", "--check", str(pdf)], "qpdf check")
    pdfinfo = run_command(["pdfinfo", str(pdf)], "pdfinfo")
    require_pdfinfo_contract(pdfinfo.stdout)

    pdffonts = run_command(["pdffonts", str(pdf)], "pdffonts")
    require_font_table(pdffonts.stdout)

    text = extract_text(pdf)
    require_searchable_text(text)


def audit_pdf_raster(pdf: Path) -> None:
    pages = render_pages(pdf)
    require_rendered_page_sizes(pages)
    require_rendered_page_content(pages)
    require_ocr_readability(pages)


def audit_pdf(pdf: Path, level: str = "full") -> None:
    if level not in AUDIT_LEVELS:
        raise AuditError(
            f"audit level must be one of {sorted(AUDIT_LEVELS)}, got {level}"
        )
    if not pdf.exists():
        raise AuditError(f"PDF missing: {pdf}")
    if not pdf.is_file():
        raise AuditError(f"PDF path is not a file: {pdf}")

    if level in {"structure", "full"}:
        audit_pdf_structure(pdf)
    if level in {"raster", "full"}:
        audit_pdf_raster(pdf)


def main(argv: list[str]) -> int:
    if len(argv) == 2:
        level = "full"
        pdf_arg = argv[1]
    elif len(argv) == 4 and argv[1] == "--level":
        level = argv[2]
        pdf_arg = argv[3]
    else:
        print(
            "usage: audit_pdf.py [--level structure|raster|full] "
            "dist/akari-v1.1-settings.pdf",
            file=sys.stderr,
        )
        return 2

    try:
        audit_pdf(project_path(pdf_arg), level=level)
    except AuditError as error:
        print(f"pdf audit: failed: {error}", file=sys.stderr)
        return 1

    print("pdf audit: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
