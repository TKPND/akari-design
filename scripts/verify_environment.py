#!/usr/bin/env python3
import shutil
import subprocess
import sys


REQUIRED_TOOLS = [
    "python3",
    "uv",
    "node",
    "npm",
    "google-chrome",
    "identify",
    "compare",
    "pdfinfo",
    "pdffonts",
    "pdftoppm",
    "pdftotext",
    "qpdf",
    "exiftool",
]


def command_text(command) -> str:
    if isinstance(command, (list, tuple)):
        return " ".join(str(part) for part in command)
    return str(command)


def clean_output(output) -> str:
    if output is None:
        return ""
    if isinstance(output, bytes):
        output = output.decode(errors="replace")
    return str(output).strip()


def main() -> int:
    missing = [tool for tool in REQUIRED_TOOLS if shutil.which(tool) is None]
    if missing:
        print("Missing required tools: " + ", ".join(missing), file=sys.stderr)
        return 1

    for command in (["qpdf", "--version"], ["exiftool", "-ver"]):
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as error:
            print(
                "Version probe failed: "
                f"{command_text(error.cmd)} (exit {error.returncode})",
                file=sys.stderr,
            )
            for label, output in (
                ("stdout", clean_output(error.stdout)),
                ("stderr", clean_output(error.stderr)),
            ):
                if output:
                    print(f"{label}: {output}", file=sys.stderr)
            return 1

    print("environment: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
