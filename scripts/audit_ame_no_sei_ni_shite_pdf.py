#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
from pathlib import Path

import yaml
from PIL import Image, ImageChops, ImageStat

try:
    from scripts.akari_v1_2_ame_no_sei_ni_shite import (
        sha256_file,
        validate_act,
        validate_contract,
    )
except ModuleNotFoundError:
    from akari_v1_2_ame_no_sei_ni_shite import (
        sha256_file,
        validate_act,
        validate_contract,
    )


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "akari-v1.2/artbooks/ame-no-sei-ni-shite"
PDF = PACKAGE / "release/akari-v1.2-ame-no-sei-ni-shite.pdf"
CHECKSUM = PACKAGE / "release/checksums.txt"
RENDER_DIR = ROOT / "build/ame-no-sei-ni-shite-pdf-rendered-pages"
TEXT_DIR = ROOT / "build/ame-no-sei-ni-shite-pdf-text"
TEXT_OUTPUT = TEXT_DIR / "document.txt"
PREVIEW_DIR = ROOT / "build/ame-no-sei-ni-shite-page-previews"
EXPECTED_PAGE_COUNT = 18
EXPECTED_A4_POINTS = (841.92, 594.96)
EXPECTED_RENDER_SIZE = (3368, 2380)
AUDIT_LEVELS = {"structure", "full"}
CONTENT_SAMPLE_SIZE = (192, 136)
MIN_CONTENT_RATIO = 0.001
PREVIEW_COMPARE_SIZE = (192, 136)
MAX_PREVIEW_MEAN_DELTA = 24.0
REQUIRED_TEXT = (
    "雨のせいにして",
    "10:02",
    "10:24",
    "10:41",
    "10:46",
    "10:52",
    "11:06",
    "11:28",
    "12:03",
    "13:17",
    "15:42",
    "18:31",
    "21:08",
    "遅い。ほら、行こ",
    "……もう少しだけ、ここにいていい？",
    "akari-v1.2-ame-no-sei-ni-shite",
    "Version 1.0.0",
)
PAGES_RE = re.compile(r"^Pages:\s+([0-9]+)\s*$", re.MULTILINE)
PAGE_SIZE_RE = re.compile(
    r"^Page size:\s+([0-9]+(?:\.[0-9]+)?) x ([0-9]+(?:\.[0-9]+)?) pts",
    re.MULTILINE,
)
RENDERED_PAGE_RE = re.compile(r"^page-([0-9]+)\.png$")
CHECKSUM_RE = re.compile(
    r"^([0-9a-f]{64})  akari-v1\.2-ame-no-sei-ni-shite\.pdf\n$"
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
        raise AuditError(f"{label} failed" + (f":\n{details}" if details else "")) from error


def require_pdfinfo_contract(pdfinfo_output: str) -> None:
    pages_match = PAGES_RE.search(pdfinfo_output)
    if not pages_match or int(pages_match.group(1)) != EXPECTED_PAGE_COUNT:
        actual = pages_match.group(1) if pages_match else "missing"
        raise AuditError(f"pdfinfo must report 18 pages, got {actual}")
    size_match = PAGE_SIZE_RE.search(pdfinfo_output)
    if not size_match:
        raise AuditError("pdfinfo must report A4 landscape page size")
    actual = (float(size_match.group(1)), float(size_match.group(2)))
    if any(abs(value - expected) > 1.0 for value, expected in zip(actual, EXPECTED_A4_POINTS)):
        raise AuditError(
            "pdf pages must use A4 landscape size, "
            f"got {actual[0]:g} x {actual[1]:g} pts"
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


def checksum_line(pdf: Path, digest: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise AuditError("checksum digest must be 64 lowercase hexadecimal characters")
    return f"{digest}  {pdf.name}"


def write_checksum(pdf: Path = PDF, checksum: Path = CHECKSUM) -> Path:
    checksum.parent.mkdir(parents=True, exist_ok=True)
    checksum.write_text(
        checksum_line(pdf, sha256_file(pdf)) + "\n",
        encoding="utf-8",
    )
    return checksum


def require_checksum_contract(pdf: Path, checksum: Path) -> None:
    value = checksum.read_text(encoding="utf-8")
    match = CHECKSUM_RE.fullmatch(value)
    if not match:
        raise AuditError("checksum must contain the exact one-line release contract")
    actual = sha256_file(pdf)
    if match.group(1) != actual:
        raise AuditError(
            f"PDF SHA-256 mismatch: expected {match.group(1)}, got {actual}"
        )


def normalize_searchable_text(value: str) -> str:
    return re.sub(r"\s+", "", value).lower()


def require_searchable_text(text: str) -> None:
    normalized = normalize_searchable_text(text)
    missing = [
        term
        for term in REQUIRED_TEXT
        if normalize_searchable_text(term) not in normalized
    ]
    if missing:
        raise AuditError(f"searchable text missing: {', '.join(missing)}")


def _clear_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def extract_text(pdf: Path) -> str:
    _clear_directory(TEXT_DIR)
    run_command(["pdftotext", str(pdf), str(TEXT_OUTPUT)], "pdftotext")
    return TEXT_OUTPUT.read_text(encoding="utf-8")


def _rendered_page_sort_key(path: Path) -> int:
    match = RENDERED_PAGE_RE.fullmatch(path.name)
    if not match:
        raise AuditError(f"rendered page file has unexpected name: {path.name}")
    return int(match.group(1))


def render_pages(pdf: Path) -> list[Path]:
    _clear_directory(RENDER_DIR)
    run_command(
        ["pdftoppm", "-png", "-r", "288", str(pdf), str(RENDER_DIR / "page")],
        "pdftoppm render",
    )
    pages = sorted(RENDER_DIR.glob("page-*.png"), key=_rendered_page_sort_key)
    if len(pages) != EXPECTED_PAGE_COUNT:
        raise AuditError(f"expected 18 rendered PNG pages, got {len(pages)}")
    return pages


def require_rendered_page_sizes(pages: list[Path]) -> None:
    for page in pages:
        with Image.open(page) as image:
            width_delta = abs(image.width - EXPECTED_RENDER_SIZE[0])
            height_delta = abs(image.height - EXPECTED_RENDER_SIZE[1])
            if width_delta > 1 or height_delta > 1:
                raise AuditError(
                    f"{page.name} must be approximately "
                    f"{EXPECTED_RENDER_SIZE[0]}x{EXPECTED_RENDER_SIZE[1]}, "
                    f"got {image.width}x{image.height}"
                )


def rendered_content_ratio(page: Path) -> float:
    with Image.open(page) as image:
        sample = image.convert("RGB").resize(CONTENT_SAMPLE_SIZE)
    background = sample.getpixel((0, 0))
    changed = 0
    pixels = list(sample.get_flattened_data())
    for pixel in pixels:
        if sum(abs(channel - base) for channel, base in zip(pixel, background)) > 24:
            changed += 1
    return changed / len(pixels)


def require_rendered_page_content(pages: list[Path]) -> None:
    for page in pages:
        ratio = rendered_content_ratio(page)
        if ratio < MIN_CONTENT_RATIO:
            raise AuditError(
                f"{page.name} appears blank or near-blank: content ratio {ratio:.4f}"
            )


def require_preview_alignment(pages: list[Path]) -> None:
    previews = sorted(PREVIEW_DIR.glob("*.png"))
    if len(previews) != EXPECTED_PAGE_COUNT:
        raise AuditError(
            f"expected 18 preview PNG pages for crop comparison, got {len(previews)}"
        )
    for preview, rendered in zip(previews, pages):
        with Image.open(preview) as preview_image, Image.open(rendered) as rendered_image:
            left = preview_image.convert("RGB").resize(PREVIEW_COMPARE_SIZE)
            right = rendered_image.convert("RGB").resize(PREVIEW_COMPARE_SIZE)
        mean_delta = sum(ImageStat.Stat(ImageChops.difference(left, right)).mean) / 3
        if mean_delta > MAX_PREVIEW_MEAN_DELTA:
            raise AuditError(
                f"preview/PDF crop mismatch on {preview.name}: mean delta {mean_delta:.2f}"
            )


def require_lifecycle_and_full_review() -> None:
    validate_contract(ROOT, require_release=True)
    validate_act(ROOT, 0)
    review_path = PACKAGE / "evidence/reviews/full-continuity.yaml"
    review = yaml.safe_load(review_path.read_text(encoding="utf-8"))
    if review.get("status") != "accepted":
        raise AuditError("full continuity review must be accepted")
    sheet = PACKAGE / "evidence/contact-sheets/full-continuity.webp"
    if review.get("contact_sheet_sha256") != sha256_file(sheet):
        raise AuditError("full continuity contact sheet hash mismatch")


def audit_structure(pdf: Path) -> None:
    require_lifecycle_and_full_review()
    run_command(["qpdf", "--check", str(pdf)], "qpdf check")
    pdfinfo = run_command(["pdfinfo", str(pdf)], "pdfinfo")
    require_pdfinfo_contract(pdfinfo.stdout)
    fonts = run_command(["pdffonts", str(pdf)], "pdffonts")
    require_font_table(fonts.stdout)
    require_searchable_text(extract_text(pdf))
    run_command(
        ["uv", "run", "python", "scripts/verify_v1_2_release_pins.py"],
        "v1.2 release pins",
    )


def audit_release(pdf: Path = PDF, checksum: Path = CHECKSUM, level: str = "full") -> None:
    if level not in AUDIT_LEVELS:
        raise AuditError(f"audit level must be one of {sorted(AUDIT_LEVELS)}, got {level}")
    if not pdf.is_file():
        raise AuditError(f"PDF missing: {pdf}")
    if not checksum.is_file():
        raise AuditError(f"checksum missing: {checksum}")
    require_checksum_contract(pdf, checksum)
    audit_structure(pdf)
    if level == "full":
        pages = render_pages(pdf)
        require_rendered_page_sizes(pages)
        require_rendered_page_content(pages)
        require_preview_alignment(pages)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", choices=sorted(AUDIT_LEVELS), default="full")
    args = parser.parse_args()
    try:
        audit_release(level=args.level)
    except AuditError as error:
        print(f"rain-day artbook pdf audit: failed: {error}")
        return 1
    print("rain-day artbook pdf audit: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
