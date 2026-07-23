#!/usr/bin/env python3
import hashlib
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
RELEASE_PINS = {
    "akari-v1.2/release/akari-v1.2-core-settings.pdf": (
        "a3904369ed20875e4d18e7a28eb2cce81e7f2da4e8cfb846cae7395bbab0e673"
    ),
    "akari-v1.2/release/checksums.txt": (
        "e8ead253ec1dbdf19e7c179c4f848f4c2839038a7704a373c6754ba38a28dd17"
    ),
}


class PinError(Exception):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_release_pins(root: Path, pins: dict[str, str]) -> None:
    errors = []
    for relative_path, expected in pins.items():
        path = root / relative_path
        if not path.is_file():
            errors.append(f"release pin missing: {relative_path}")
            continue
        actual = sha256_file(path)
        if actual != expected:
            errors.append(
                f"release pin mismatch: {relative_path}: "
                f"expected {expected}, got {actual}"
            )
    if errors:
        raise PinError("\n".join(errors))


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: verify_v1_2_release_pins.py", file=sys.stderr)
        return 2
    try:
        verify_release_pins(ROOT, RELEASE_PINS)
    except PinError as error:
        print(f"v1.2 release pins: failed:\n{error}", file=sys.stderr)
        return 1
    print("v1.2 release pins: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
