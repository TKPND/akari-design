"""Reproduce the selected M2 montage in a new output directory.

Requires Python 3 and ImageMagick's magick command. The fixed crop coordinates
and clothing transitions are specific to the selected U1/L1 standing pose.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


RECIPE_DIR = Path(__file__).resolve().parent
PACKAGE = RECIPE_DIR.parents[1]
LAYOUT = json.loads((RECIPE_DIR / "layout.json").read_text())
PARAMETERS = LAYOUT["assembly_parameters"]
SCALE = PARAMETERS["scale"]
SIZE = LAYOUT["intended_montage_size"]
SEAM = PARAMETERS["waist_transition_y"]
OUTER_SEAM = PARAMETERS["outer_transition_y"]


def magick(*args):
    subprocess.run(["magick", *map(str, args)], check=True)


def ramp(value):
    t = max(0.0, min(1.0, value))
    return t * t * (3.0 - 2.0 * t)


def alpha_mask(output_dir, name, width, height, origin_x, origin_y, upper):
    edges = PARAMETERS["edge_fade_in_output_pixels"]
    horizontal = [
        min(ramp(x / edges["horizontal"]),
            ramp((width - 1 - x) / edges["horizontal"]))
        for x in range(width)
    ]
    left, right = PARAMETERS["center_x_in_source"]
    center_width = PARAMETERS["center_ramp_width_in_source"]
    seams = []
    for x in range(width):
        source_x = (origin_x + x) / SCALE
        center = min(ramp((source_x - left) / center_width),
                     ramp((right - source_x) / center_width))
        seams.append(tuple(outer + (inner - outer) * center
                           for inner, outer in zip(SEAM, OUTER_SEAM)))
    pixels = bytearray(width * height)
    for y in range(height):
        vertical = min(ramp(y / edges["top"]),
                       ramp((height - 1 - y) / edges["bottom"]))
        if upper:
            row = bytes(round(255 * min(h, vertical) *
                              (1 - ramp((origin_y + y - start) / (end - start))))
                        for h, (start, end) in zip(horizontal, seams))
        else:
            row = bytes(round(255 * min(h, vertical)) for h in horizontal)
        pixels[y * width:(y + 1) * width] = row
    target = output_dir / name
    target.write_bytes(f"P5\n{width} {height}\n255\n".encode() + pixels)
    return target


def layer(output_dir, candidate, guide, upper):
    x, y, w, h = LAYOUT["guides"][guide]["crop_xywh"]
    x, y, w, h = (n * SCALE for n in (x, y, w, h))
    resized = output_dir / (candidate + "-placed-size.png")
    source = PACKAGE / LAYOUT["candidates"][candidate]["path"]
    magick(source, "-filter", "Lanczos", "-resize", f"{w}x{h}", resized)
    mask = alpha_mask(output_dir, candidate + "-assembly-mask.pgm",
                      w, h, x, y, upper)
    transparent = output_dir / (candidate + "-assembly-layer.png")
    magick(resized, mask, "-alpha", "off", "-compose", "CopyOpacity",
           "-composite", transparent)
    return transparent, x, y


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="New directory outside the preserved v3.1 package")
    args = parser.parse_args()
    output_dir = args.output_dir.resolve()
    if output_dir == PACKAGE or PACKAGE in output_dir.parents:
        parser.error("Choose an output directory outside the preserved package.")
    if output_dir.exists():
        parser.error("The output directory already exists; choose a new one.")
    inputs = [
        {"path": LAYOUT["source"], "sha256": LAYOUT["source_sha256"]},
        *LAYOUT["candidates"].values(),
    ]
    for source in inputs:
        actual = hashlib.sha256((PACKAGE / source["path"]).read_bytes()).hexdigest()
        if actual != source["sha256"]:
            parser.error(f"Input hash changed: {source['path']}")
    output_dir.mkdir(parents=True)

    base = output_dir / "assembly-background.png"
    magick(PACKAGE / LAYOUT["source"], "-filter", "Lanczos", "-resize",
           f"{SIZE[0]}x{SIZE[1]}", base)
    lower, lx, ly = layer(output_dir, "L1", "L-guide", False)
    upper, ux, uy = layer(output_dir, "U1", "U-guide", True)
    target = output_dir / "M2-full-body-montage.png"
    magick(base, lower, "-geometry", f"+{lx}+{ly}", "-compose", "Over", "-composite",
           upper, "-geometry", f"+{ux}+{uy}", "-compose", "Over", "-composite", target)
    magick(target, "-resize", "1024x1536", output_dir / "M2-full-body-preview.png")
    magick(target, "-crop", "860x500+600+900", "+repage",
           output_dir / "M2-waist-inspection.png")
    magick(target, "-crop", "880x730+590+1080", "+repage",
           output_dir / "M2-hands-skirt-inspection.png")
    result = {
        "output": target.name,
        "output_path_base": "This output directory.",
        "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "canvas": SIZE,
        "input_path_base": "The akari-v3.1 package directory.",
        "inputs": inputs,
        "waist_transition_y": SEAM,
        "outer_transition_y": OUTER_SEAM,
        "generative_postprocessing": False,
        "geometric_warping": False,
        "original_reference_files_overwritten": False,
        "status": "reproduction_output_not_a_new_selection",
    }
    (output_dir / "assembly.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
