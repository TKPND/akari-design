#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PALETTE = ROOT / "source/palette/akari-v1.1-palette.json"
COLOR_REVIEW = ROOT / "source/manifests/color-review.json"
PAGE_MANIFEST = ROOT / "source/manifests/page-manifest.json"

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
EXPECTED_ROLE_NAMES = {
    "hair",
    "skin",
    "eyes",
    "hoodie_white",
    "hoodie_shadow",
    "skirt_gray",
    "sock_white",
    "sock_stripe_blue",
    "sneaker_white",
    "sneaker_accent_blue",
    "bag_body",
    "bag_strap",
    "metal",
}
REQUIRED_RAMP_KEYS = ("base", "shadow", "highlight")
REQUIRED_TEXT_FIELDS = ("usage", "sample_area", "exception_policy")


def hex_to_rgb(value: str) -> list[int]:
    return [int(value[index : index + 2], 16) for index in (1, 3, 5)]


def main() -> int:
    data = json.loads(PALETTE.read_text(encoding="utf-8"))
    errors = []

    if data.get("white_point") != "D65":
        errors.append("palette white_point must be D65")
    if data.get("color_space") != "sRGB":
        errors.append("palette color_space must be sRGB")
    palette_version = data.get("palette_version")
    if not isinstance(palette_version, str) or not palette_version.strip():
        errors.append("palette palette_version must be a non-empty string")

    roles = data.get("roles", [])
    if not isinstance(roles, list):
        errors.append("palette roles must be a list")
        roles = []

    role_names = [role.get("name", "") for role in roles if isinstance(role, dict)]
    if len(role_names) != len(EXPECTED_ROLE_NAMES) or set(role_names) != EXPECTED_ROLE_NAMES:
        errors.append("palette roles must exactly match the canonical 13 role names")

    names = set()
    for role in roles:
        if not isinstance(role, dict):
            errors.append("palette roles must be objects")
            continue

        name = role.get("name", "")
        if name in names:
            errors.append(f"duplicate role: {name}")
        names.add(name)

        hex_value = role.get("hex", "")
        hex_ok = isinstance(hex_value, str) and HEX_RE.match(hex_value)
        if not hex_ok:
            errors.append(f"bad hex for role: {name}")
        elif role.get("rgb") != hex_to_rgb(hex_value):
            errors.append(f"rgb does not match hex for role: {name}")

        ramp = role.get("ramp")
        if not isinstance(ramp, dict):
            errors.append(f"missing ramp for role: {name}")
        else:
            for key in REQUIRED_RAMP_KEYS:
                ramp_value = ramp.get(key)
                if not isinstance(ramp_value, str) or not HEX_RE.match(ramp_value):
                    errors.append(f"bad ramp {key} for role: {name}")
            if hex_ok and ramp.get("base") != hex_value:
                errors.append(f"ramp base does not match hex for role: {name}")

        tolerance = role.get("tolerance", {})
        if not isinstance(tolerance, dict) or "median_rgb_delta" not in tolerance:
            errors.append(f"missing tolerance for role: {name}")
        else:
            median_rgb_delta = tolerance["median_rgb_delta"]
            if (
                not isinstance(median_rgb_delta, (int, float))
                or isinstance(median_rgb_delta, bool)
                or median_rgb_delta <= 0
            ):
                errors.append(f"bad median_rgb_delta for role: {name}")

        for field in REQUIRED_TEXT_FIELDS:
            value = role.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"missing {field} for role: {name}")

    if COLOR_REVIEW.exists():
        color_review = json.loads(COLOR_REVIEW.read_text(encoding="utf-8"))
        color_review_version = color_review.get("palette_version")
        if not isinstance(color_review_version, str) or not color_review_version.strip():
            errors.append("color-review palette_version must be a non-empty string")
        elif color_review_version != palette_version:
            errors.append("color-review palette_version must match palette palette_version")
    else:
        errors.append("color-review manifest missing")

    if PAGE_MANIFEST.exists():
        pages = json.loads(PAGE_MANIFEST.read_text(encoding="utf-8"))
        palette_pages = [
            page for page in pages.get("pages", []) if page.get("role") == "palette"
        ]
        if len(palette_pages) != 1:
            errors.append("page-manifest must define exactly one palette page")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"palette audit: ok ({len(names)} roles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
