#!/usr/bin/env python3
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "akari-v1.2/release/akari-v1.2-core-settings.pdf"
CHECKSUM = ROOT / "akari-v1.2/release/checksums.txt"
RENDER_DIR = ROOT / "build/akari-v1.2-pdf-rendered-pages"
TEXT_DIR = ROOT / "build/akari-v1.2-pdf-text"
TEXT_OUTPUT = TEXT_DIR / "document.txt"
EXPECTED_PAGE_COUNT = 14
EXPECTED_RENDER_SIZE = (3840, 2160)
AUDIT_LEVELS = {"structure", "raster", "full"}
CONTENT_SAMPLE_SIZE = (192, 108)
MIN_CONTENT_RATIO = 0.003
REQUIRED_TEXT = (
    "Akari v1.2.0 Natural Form Core Settings",
    "Cover / Natural Form",
    "v1.1 to v1.2 Inheritance",
    "Identity Lock",
    "Natural Front Stance",
    "Back and 45-degree Views",
    "Weight and Joint Guidelines",
    "Floor Sitting Master",
    "Floor Sitting Anatomy Notes",
    "Indoor Sock Feet",
    "Morning Bed Hair",
    "Sleepy-to-Soft-Smile Expressions",
    "D01 Morning Validation",
    "Do / Don't",
    "Source Manifest and Review Status",
    "C01",
    "C02",
    "C03",
    "C04",
    "C05",
    "C06",
    "C07",
    "D01",
    "Gate 4",
    "release",
)
PAGES_RE = re.compile(r"^Pages:\s+([0-9]+)\s*$", re.MULTILINE)
PAGE_SIZE_RE = re.compile(
    r"^Page size:\s+([0-9]+(?:\.[0-9]+)?) x ([0-9]+(?:\.[0-9]+)?) pts",
    re.MULTILINE,
)
RENDERED_PAGE_RE = re.compile(r"^page-([0-9]+)\.png$")
CHECKSUM_RE = re.compile(
    r"^([0-9a-f]{64})  akari-v1\.2-core-settings\.pdf\n$"
)


class AuditError(Exception):
    pass


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

    size_match = PAGE_SIZE_RE.search(pdfinfo_output)
    if not size_match:
        raise AuditError("pdfinfo must report page size in points")
    width = float(size_match.group(1))
    height = float(size_match.group(2))
    if height == 0 or abs((width / height) - (16 / 9)) > 0.001:
        raise AuditError(
            f"pdf pages must use 16:9 aspect ratio, got {width:g} x {height:g} pts"
        )


def require_font_table(pdffonts_output: str) -> None:
    lines = [line for line in pdffonts_output.splitlines() if line.strip()]
    if len(lines) < 3 or not lines[0].lower().startswith("name"):
        raise AuditError("pdffonts must report at least one font table row")
    bad_rows = []
    for row in lines[2:]:
        tokens = row.split()
        if len(tokens) < 7 or tokens[-5].lower() != "yes" or tokens[-3].lower() != "yes":
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
                raise AuditError(
                    f"{page.name} must be {EXPECTED_RENDER_SIZE[0]}x"
                    f"{EXPECTED_RENDER_SIZE[1]}, got {image.width}x{image.height}"
                )


def rendered_content_ratio(page: Path) -> float:
    with Image.open(page) as image:
        sample = image.convert("RGB").resize(CONTENT_SAMPLE_SIZE)
    background = sample.getpixel((0, 0))
    pixels = list(sample.get_flattened_data())
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


def normalize_searchable_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().lower()


def require_searchable_text(text: str) -> None:
    normalized = normalize_searchable_text(text)
    missing = [
        term
        for term in REQUIRED_TEXT
        if normalize_searchable_text(term) not in normalized
    ]
    if missing:
        raise AuditError(f"searchable text missing: {', '.join(missing)}")


def extract_text(pdf: Path) -> str:
    clear_directory(TEXT_DIR)
    run_command(["pdftotext", str(pdf), str(TEXT_OUTPUT)], "pdftotext")
    return TEXT_OUTPUT.read_text(encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_checksum_contract(pdf: Path, checksum: Path) -> None:
    value = checksum.read_text(encoding="utf-8")
    match = CHECKSUM_RE.fullmatch(value)
    if not match:
        raise AuditError("checksum must contain the exact one-line release contract")
    expected = match.group(1)
    actual = sha256_file(pdf)
    if expected != actual:
        raise AuditError(f"PDF SHA-256 mismatch: expected {expected}, got {actual}")


def audit_pdf_structure(pdf: Path) -> None:
    run_command(["qpdf", "--check", str(pdf)], "qpdf check")
    pdfinfo = run_command(["pdfinfo", str(pdf)], "pdfinfo")
    require_pdfinfo_contract(pdfinfo.stdout)
    fonts = run_command(["pdffonts", str(pdf)], "pdffonts")
    require_font_table(fonts.stdout)
    require_searchable_text(extract_text(pdf))


def audit_pdf_raster(pdf: Path) -> None:
    pages = render_pages(pdf)
    require_rendered_page_sizes(pages)
    require_rendered_page_content(pages)


def audit_release(pdf: Path, checksum: Path, level: str = "full") -> None:
    if level not in AUDIT_LEVELS:
        raise AuditError(
            f"audit level must be one of {sorted(AUDIT_LEVELS)}, got {level}"
        )
    if not pdf.exists():
        raise AuditError(f"PDF missing: {pdf}")
    if not pdf.is_file():
        raise AuditError(f"PDF path is not a file: {pdf}")
    if not checksum.exists():
        raise AuditError(f"checksum missing: {checksum}")
    if not checksum.is_file():
        raise AuditError(f"checksum path is not a file: {checksum}")

    require_checksum_contract(pdf, checksum)
    if level in {"structure", "full"}:
        audit_pdf_structure(pdf)
    if level in {"raster", "full"}:
        audit_pdf_raster(pdf)


def main(argv: list[str]) -> int:
    if len(argv) == 1:
        level = "full"
    elif len(argv) == 3 and argv[1] == "--level":
        level = argv[2]
    else:
        print(
            "usage: audit_akari_v1_2_pdf.py "
            "[--level structure|raster|full]",
            file=sys.stderr,
        )
        return 2
    try:
        audit_release(PDF, CHECKSUM, level=level)
    except AuditError as error:
        print(f"Natural Form pdf audit: failed: {error}", file=sys.stderr)
        return 1
    print("Natural Form pdf audit: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
