#!/usr/bin/env python3
import hashlib
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "akari-v1.2/release/akari-v1.2-core-settings.pdf"
CHECKSUM = ROOT / "akari-v1.2/release/checksums.txt"
RELEASE_TIMESTAMP = "2026:07:15 00:00:00+09:00"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_checksum(pdf: Path, checksum_path: Path) -> None:
    checksum_path.parent.mkdir(parents=True, exist_ok=True)
    content = f"{sha256_file(pdf)}  {pdf.name}\n"
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=checksum_path.parent,
            prefix=f".{checksum_path.name}.",
            delete=False,
        ) as handle:
            handle.write(content)
            temporary_path = Path(handle.name)
        temporary_path.chmod(0o644)
        temporary_path.replace(checksum_path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def normalize_pdf_metadata(pdf: Path) -> None:
    subprocess.run(
        [
            "exiftool",
            "-overwrite_original",
            f"-CreateDate={RELEASE_TIMESTAMP}",
            f"-ModifyDate={RELEASE_TIMESTAMP}",
            str(pdf),
        ],
        cwd=ROOT,
        check=True,
    )
    normalized = pdf.with_name(f".{pdf.stem}.normalized.pdf")
    normalized.unlink(missing_ok=True)
    try:
        subprocess.run(
            ["qpdf", "--deterministic-id", str(pdf), str(normalized)],
            cwd=ROOT,
            check=True,
        )
        normalized.chmod(0o644)
        normalized.replace(pdf)
    finally:
        normalized.unlink(missing_ok=True)


def main() -> int:
    subprocess.run(
        [
            "node",
            "tools/pdf/render.mjs",
            "--document",
            "natural-form",
            "--pdf",
        ],
        cwd=ROOT,
        check=True,
    )
    normalize_pdf_metadata(PDF)
    write_checksum(PDF, CHECKSUM)
    print("Natural Form pdf exported with checksum")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
