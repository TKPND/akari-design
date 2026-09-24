"""Prepare shared region guides or assemble reviewed PNG regions. Python 3 + ImageMagick 7."""
import argparse
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path


def magick(*args, capture=False):
    result = subprocess.run(
        ["magick", "-limit", "thread", "2", "-limit", "memory", "256MiB",
         "-limit", "map", "512MiB", *map(str, args)], check=True,
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL)
    return result.stdout


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def info(path, png=True):
    if png:
        with path.open("rb") as stream:
            if stream.read(8) != bytes.fromhex("89504e470d0a1a0a"):
                raise ValueError(f"Expected PNG: {path}")
    # This reads the image pixels, rather than only trusting a dimensions header.
    size = magick(path, "-format", "%w %h", "info:", capture=True).decode().split()
    if len(size) != 2:
        raise ValueError(f"Expected one image: {path}")
    magick(path, "null:")
    return list(map(int, size))


def positive_ints(values, count):
    return (isinstance(values, list) and len(values) == count
            and all(type(n) is int and n > 0 for n in values))


def rect_ok(rect, canvas):
    return (isinstance(rect, list) and len(rect) == 4
            and all(type(n) is int for n in rect)
            and min(rect[:2]) >= 0 and min(rect[2:]) > 0
            and rect[0] + rect[2] <= canvas[0] and rect[1] + rect[3] <= canvas[1])


def source(root, relative):
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise ValueError("Input image paths must be relative to the layout manifest")
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f"Missing input or path outside run: {relative}")
    return path


def placement(native, target):
    scale = max(target[0] / native[0], target[1] / native[1])
    return {"native_size": native, "uniform_scale": scale,
            "aspect_relative_difference": abs((native[0] / native[1]) / (target[0] / target[1]) - 1),
            "ideal_cover_crop_total_xy": [native[i] * scale - target[i] for i in range(2)]}


def preflight(layout_path, mode):
    root = layout_path.parent
    layout = json.loads(layout_path.read_text())
    canvas = layout["canvas"]
    if not positive_ints(canvas, 2):
        raise ValueError("canvas must contain two positive integer dimensions")
    master = source(root, layout["master"])
    master_info = placement(info(master), canvas)
    regions = layout["regions"]
    if not isinstance(regions, list) or not regions:
        raise ValueError("regions must be a nonempty list")
    ids = []
    for region in regions + layout.get("qa", []):
        if not re.fullmatch(r"[A-Za-z0-9_-]+", region["id"]):
            raise ValueError(f"Invalid ID: {region['id']}")
        if not rect_ok(region["rect"], canvas):
            raise ValueError(f"Out-of-canvas rectangle: {region['id']}")
    ids = [r["id"] for r in regions]
    qa_ids = [r["id"] for r in layout.get("qa", [])]
    if len(set(ids)) != len(ids) or len(set(qa_ids)) != len(qa_ids):
        raise ValueError("Duplicate region or QA ID")
    selected = layout.get("selected_region_ids", ids)
    if (not isinstance(selected, list) or not selected
            or not all(isinstance(x, str) for x in selected)
            or len(set(selected)) != len(selected) or not set(selected) <= set(ids)):
        raise ValueError("selected_region_ids must contain distinct known IDs")
    records = []
    if mode == "assemble":
        limit = layout["max_aspect_drift"]
        if type(limit) not in (int, float) or not math.isfinite(limit) or not 0 <= limit < 1:
            raise ValueError("max_aspect_drift must be a finite fraction in [0, 1)")
        for region in regions:
            if region["id"] not in selected:
                continue
            native = source(root, region["native"])
            w, h = region["rect"][2:]
            record = {"id": region["id"], "rect": region["rect"], "source": region["native"],
                      "sha256": digest(native), **placement(info(native), [w, h])}
            if record["aspect_relative_difference"] > limit:
                raise ValueError(f"Aspect mismatch for {region['id']}: {record['aspect_relative_difference']:.2%}")
            if "mask" in region and "feather" in region:
                raise ValueError("Choose an external mask or edge feather, not both")
            if "mask" in region:
                mask = source(root, region["mask"])
                if info(mask, png=False) != [w, h]:
                    raise ValueError(f"Mask dimensions must match placed region: {region['id']}")
                record["mask_source"] = region["mask"]
                record["mask_sha256"] = digest(mask)
            feather = region.get("feather", {})
            if not isinstance(feather, dict):
                raise ValueError("feather must be a mapping of edges to local distance pairs")
            for edge, pair in feather.items():
                dimension = w if edge in ("left", "right") else h
                if (edge not in ("left", "right", "top", "bottom")
                        or not isinstance(pair, list) or len(pair) != 2
                        or not all(type(x) in (int, float) and math.isfinite(x) for x in pair)
                        or not 0 <= pair[0] < pair[1] <= dimension - 1):
                    raise ValueError(f"Invalid feather: {region['id']} {edge}")
            record["feather"] = feather
            records.append(record)
    return layout, master, master_info, records


def cover(src, size, dst):
    geometry = f"{size[0]}x{size[1]}"
    magick(src, "-filter", "Lanczos", "-resize", geometry + "^",
           "-gravity", "center", "-extent", geometry, "+repage",
           "-colorspace", "sRGB", "-alpha", "off", "-depth", "8", "PNG24:" + str(dst))


def crop(src, rect, dst):
    x, y, w, h = rect
    magick(src, "-gravity", "NorthWest", "-crop", f"{w}x{h}+{x}+{y}", "+repage", dst)


def smooth(value):
    value = max(0., min(1., value))
    return value * value * (3 - 2 * value)


def feather_mask(size, feather, dst):
    w, h = size
    def axis_factor(position, length, low, high):
        factor = 1.
        for edge, distance in ((low, position), (high, length - 1 - position)):
            if edge in feather:
                a, b = feather[edge]
                factor *= smooth((distance - a) / (b - a))
        return factor
    horizontal = [axis_factor(x, w, "left", "right") for x in range(w)]
    with dst.open("wb") as stream:
        stream.write(f"P5\n{w} {h}\n255\n".encode())
        for y in range(h):
            vertical = axis_factor(y, h, "top", "bottom")
            stream.write(bytes(round(255 * factor * vertical) for factor in horizontal))


def execute(mode, layout_path, output):
    layout_path, output = layout_path.resolve(), output.resolve()
    if output.exists():
        raise ValueError("Output already exists; choose a fresh revision directory")
    layout, master, master_info, records = preflight(layout_path, mode)
    root = layout_path.parent
    output.mkdir(parents=True)
    canvas = layout["canvas"]
    baseline = output / "baseline.png"
    cover(master, canvas, baseline)
    if mode == "prepare":
        (output / "guides").mkdir()
        for region in layout["regions"]:
            crop(baseline, region["rect"], output / "guides" / (region["id"] + ".png"))
        records = [{"id": r["id"], "rect": r["rect"], "guide": f"guides/{r['id']}.png"}
                   for r in layout["regions"]]
    else:
        (output / "layers").mkdir()
        work = baseline
        by_id = {r["id"]: r for r in layout["regions"]}
        for n, record in enumerate(records):
            region = by_id[record["id"]]
            prefix = output / "layers" / record["id"]
            placed = prefix.with_name(prefix.name + "-placed.png")
            cover(source(root, region["native"]), region["rect"][2:], placed)
            mask = prefix.with_name(prefix.name + "-mask.pgm")
            if "mask" in region:
                magick(source(root, region["mask"]), "-alpha", "off", "-colorspace", "Gray", "-depth", "8", mask)
            else:
                feather_mask(region["rect"][2:], region.get("feather", {}), mask)
            layer = prefix.with_name(prefix.name + "-layer.png")
            magick(placed, mask, "-alpha", "off", "-compose", "CopyOpacity", "-composite", layer)
            stage = output / "layers" / f"stage-{n:02d}.png"
            x, y = region["rect"][:2]
            magick(work, layer, "-gravity", "NorthWest", "-geometry", f"+{x}+{y}",
                   "-compose", "Over", "-composite", stage)
            work = stage
            record["applied_mask"] = str(mask.relative_to(output))
        magick(work, "-colorspace", "sRGB", "-alpha", "off", "-depth", "8",
               "PNG24:" + str(output / "composite.png"))
        (output / "qa").mkdir()
        for region in layout.get("qa", []):
            crops = []
            for kind in ("baseline", "composite"):
                dst = output / "qa" / f"{region['id']}-{kind}.png"
                crop(output / f"{kind}.png", region["rect"], dst)
                crops.append(dst)
            magick(*crops, "+append", output / "qa" / f"{region['id']}-compare.png")
    all_ids = [r["id"] for r in layout["regions"]]
    outputs = [p for p in output.rglob("*.png") if "layers" not in p.relative_to(output).parts]
    checked = [{"path": str(p.relative_to(output)), "size": info(p), "sha256": digest(p)}
               for p in sorted(outputs)]
    report = {"mode": mode, "canvas": canvas, "layout_sha256": digest(layout_path),
              "input_path_base": "input layout manifest directory",
              "master": {"source": layout["master"], "sha256": digest(master), **master_info},
              "baseline_method": "uniform Lanczos cover resize and centered extent; sRGB RGB8",
              "regions": records, "excluded_region_ids": [x for x in all_ids if x not in layout.get("selected_region_ids", all_ids)],
              "qa": layout.get("qa", []), "outputs": checked,
              "geometric_warping": False, "generative_postprocessing": False,
              "visual_review": "required; not established by this script"}
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(output), "mode": mode, "canvas": canvas,
                      "decoded_outputs": len(checked)}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["prepare", "assemble"])
    parser.add_argument("layout", type=Path, help="Run-local JSON manifest; see references/assembly.md")
    parser.add_argument("output", type=Path, help="New directory; existing paths are never overwritten")
    args = parser.parse_args()
    try:
        execute(args.mode, args.layout, args.output)
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Error: {error}\n")
