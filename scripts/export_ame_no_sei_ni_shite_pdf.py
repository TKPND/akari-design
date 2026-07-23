#!/usr/bin/env python3
from pathlib import Path
import subprocess

from audit_ame_no_sei_ni_shite_pdf import PDF, write_checksum


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    subprocess.run(
        [
            "node",
            "tools/pdf/render.mjs",
            "--document",
            "ame-no-sei-ni-shite",
            "--pdf",
        ],
        cwd=ROOT,
        check=True,
    )
    write_checksum(PDF)
    print("rain-day artbook pdf exported with checksum")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
