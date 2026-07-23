from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys

import yaml

if __package__:
    from scripts.validate_akari_v1_2_natural_form import (
        C03_R02_FRAMING_CONTRACT,
        ordered_value,
    )
else:
    from validate_akari_v1_2_natural_form import (
        C03_R02_FRAMING_CONTRACT,
        ordered_value,
    )


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"
GEOMETRY_RE = re.compile(
    r"^(?P<width>\d+)x(?P<height>\d+)(?P<x>[+-]\d+)(?P<y>[+-]\d+)$"
)


class AuditError(RuntimeError):
    pass


@dataclass(frozen=True)
class TrimGeometry:
    width: int
    height: int
    x: int
    y: int


@dataclass(frozen=True)
class Measurement:
    canvas_width: int
    canvas_height: int
    trim: TrimGeometry

    @property
    def head_top_y(self) -> int:
        return self.trim.y

    @property
    def sole_y(self) -> int:
        return self.trim.y + self.trim.height - 1


def parse_geometry(value: str) -> TrimGeometry:
    match = GEOMETRY_RE.fullmatch(value.strip())
    if match is None:
        raise AuditError(f"malformed ImageMagick geometry: {value!r}")
    geometry = TrimGeometry(
        **{key: int(item) for key, item in match.groupdict().items()}
    )
    if geometry.width <= 0 or geometry.height <= 0:
        raise AuditError(f"missing foreground in geometry: {value}")
    return geometry


def measure_image(path: Path, fuzz_percent: int) -> Measurement:
    if not path.is_file():
        raise AuditError(f"missing file: {path}")
    command = [
        "magick",
        "identify",
        "-fuzz",
        f"{fuzz_percent}%",
        "-format",
        "%w %h %@",
        str(path),
    ]
    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:
        raise AuditError("ImageMagick 'magick' is unavailable") from error
    except subprocess.CalledProcessError as error:
        detail = error.stderr.strip() or error.stdout.strip() or "identify failed"
        raise AuditError(f"{path}: {detail}") from error
    parts = completed.stdout.strip().split(maxsplit=2)
    if len(parts) != 3:
        raise AuditError(
            f"{path}: malformed identify output {completed.stdout!r}"
        )
    try:
        canvas_width, canvas_height = (int(parts[0]), int(parts[1]))
    except ValueError as error:
        raise AuditError(f"{path}: malformed canvas size {parts[:2]!r}") from error
    return Measurement(
        canvas_width,
        canvas_height,
        parse_geometry(parts[2]),
    )


def resolve_package_path(package_root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] == package_root.name:
        return package_root.parent / path
    return package_root / path


def measurement_errors(
    measurement: Measurement,
    contract: dict,
    anchors: list[dict],
) -> list[str]:
    errors = []
    canvas = contract["canvas"]
    if (measurement.canvas_width, measurement.canvas_height) != (
        canvas["width"],
        canvas["height"],
    ):
        errors.append(
            f"expected {canvas['width']}x{canvas['height']}, got "
            f"{measurement.canvas_width}x{measurement.canvas_height}"
        )
    limit = contract["maximum_displacement"]["integer_pixels"]
    for name, actual, anchor_field in (
        ("head_top_y", measurement.head_top_y, "head_top_y"),
        ("sole_y", measurement.sole_y, "sole_y"),
    ):
        for anchor in anchors:
            delta = abs(actual - anchor[anchor_field])
            if delta > limit:
                errors.append(
                    f"{name}={actual} differs from {anchor['asset_id']} "
                    f"{anchor[anchor_field]} by {delta} px; maximum is "
                    f"{limit} px"
                )
        lower, upper = contract["required_intersection"][name]
        if not lower <= actual <= upper:
            errors.append(
                f"{name}={actual} is outside required intersection "
                f"[{lower}, {upper}]"
            )
    return errors


def describe(measurement: Measurement, anchors: list[dict]) -> str:
    deltas = ", ".join(
        f"{anchor['asset_id']} "
        f"head={abs(measurement.head_top_y - anchor['head_top_y'])} "
        f"sole={abs(measurement.sole_y - anchor['sole_y'])}"
        for anchor in anchors
    )
    return (
        f"canvas={measurement.canvas_width}x{measurement.canvas_height} "
        f"head_top_y={measurement.head_top_y} sole_y={measurement.sole_y}; "
        f"{deltas}"
    )


def audit_request(request_path: Path, package_root: Path) -> list[str]:
    request = yaml.safe_load(request_path.read_text(encoding="utf-8"))
    if not isinstance(request, dict):
        raise AuditError(f"{request_path}: expected mapping")
    contract = request.get("framing_contract")
    if ordered_value(contract) != ordered_value(C03_R02_FRAMING_CONTRACT):
        raise AuditError(
            "request does not contain the exact C03 r02 framing contract"
        )

    references = request.get("references")
    if not isinstance(references, list) or len(references) < 2:
        raise AuditError("request requires C01 and C02 references first")
    anchor_specs = contract["anchors"]
    fuzz_percent = contract["measurement"]["fuzz_percent"]
    anchor_errors = []
    lines = []
    for spec, reference in zip(anchor_specs, references[:2]):
        label = f"anchor {spec['asset_id']} {spec['revision']}"
        if not isinstance(reference, dict) or not isinstance(
            reference.get("path"), str
        ):
            anchor_errors.append(f"FAIL {label}: invalid reference path")
            continue
        path = resolve_package_path(package_root, reference["path"])
        try:
            measurement = measure_image(path, fuzz_percent)
        except AuditError as error:
            anchor_errors.append(f"FAIL {label}: {error}")
            continue
        expected_canvas = contract["canvas"]
        errors = []
        if (measurement.canvas_width, measurement.canvas_height) != (
            expected_canvas["width"],
            expected_canvas["height"],
        ):
            errors.append(
                f"expected {expected_canvas['width']}x"
                f"{expected_canvas['height']}, got "
                f"{measurement.canvas_width}x{measurement.canvas_height}"
            )
        if measurement.head_top_y != spec["head_top_y"]:
            errors.append(
                f"head_top_y expected {spec['head_top_y']}, "
                f"got {measurement.head_top_y}"
            )
        if measurement.sole_y != spec["sole_y"]:
            errors.append(
                f"sole_y expected {spec['sole_y']}, got {measurement.sole_y}"
            )
        if errors:
            anchor_errors.append(f"FAIL {label}: " + "; ".join(errors))
        else:
            lines.append(f"PASS {label}: {describe(measurement, anchor_specs)}")
    if anchor_errors:
        raise AuditError("\n".join(anchor_errors))

    candidates = request.get("candidates")
    if not isinstance(candidates, list) or [
        item.get("variant") for item in candidates if isinstance(item, dict)
    ] != ["a", "b", "c"]:
        raise AuditError("request requires candidates a, b, c in order")
    failures = []
    for candidate in candidates:
        outputs = candidate.get("outputs")
        if not isinstance(outputs, list) or [
            item.get("view") for item in outputs if isinstance(item, dict)
        ] != ["hairpin-side-45", "non-hairpin-side-45"]:
            raise AuditError(
                f"candidate {candidate.get('variant')} has invalid view order"
            )
        for output in outputs:
            relative = output.get("target_path")
            if not isinstance(relative, str):
                failures.append(
                    f"FAIL candidate {candidate['variant']}: missing target path"
                )
                continue
            path = resolve_package_path(package_root, relative)
            try:
                measurement = measure_image(path, fuzz_percent)
                errors = measurement_errors(
                    measurement,
                    contract,
                    anchor_specs,
                )
            except AuditError as error:
                failures.append(f"FAIL {relative}: {error}")
                continue
            if errors:
                failures.append(
                    f"FAIL {relative}: {describe(measurement, anchor_specs)}; "
                    + "; ".join(errors)
                )
            else:
                lines.append(
                    f"PASS {relative}: {describe(measurement, anchor_specs)}"
                )
    if failures:
        raise AuditError("\n".join(failures))
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--package-root", type=Path, default=PACKAGE_ROOT)
    args = parser.parse_args(argv)
    request = args.request if args.request.is_absolute() else ROOT / args.request
    package_root = (
        args.package_root
        if args.package_root.is_absolute()
        else ROOT / args.package_root
    )
    try:
        lines = audit_request(request, package_root)
    except (AuditError, OSError, yaml.YAMLError) as error:
        print(error, file=sys.stderr)
        return 1
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
