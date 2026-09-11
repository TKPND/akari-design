"""Verify the preserved package without requiring tmp or the image tool cache."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib


BASE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local(value):
    assert not Path(value).is_absolute(), value
    path = (BASE / value).resolve()
    assert path.is_relative_to(BASE) and path.is_file(), value
    return path


def decode_png(path):
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", path
    offset, compressed, dimensions = 8, bytearray(), None
    while offset < len(data):
        length = struct.unpack_from(">I", data, offset)[0]
        kind = data[offset + 4:offset + 8]
        body = data[offset + 8:offset + 8 + length]
        crc = struct.unpack_from(">I", data, offset + 8 + length)[0]
        assert zlib.crc32(kind + body) & 0xFFFFFFFF == crc, path
        if kind == b"IHDR":
            width, height, depth, color, compression, filtering, interlace = struct.unpack(">IIBBBBB", body)
            assert compression == filtering == interlace == 0, path
            dimensions = (width, height)
            channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[color]
            row_bytes = (width * depth * channels + 7) // 8
        elif kind == b"IDAT":
            compressed.extend(body)
        offset += length + 12
        if kind == b"IEND":
            assert offset == len(data), path
            break
    assert kind == b"IEND" and dimensions, path
    decoder = zlib.decompressobj()
    pixels = decoder.decompress(compressed) + decoder.flush()
    assert decoder.eof and not decoder.unused_data, path
    assert len(pixels) == height * (row_bytes + 1), path
    assert all(pixels[y * (row_bytes + 1)] <= 4 for y in range(height)), path
    return dimensions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-sources", type=Path, help="Optional original workspace root")
    args = parser.parse_args()
    manifest = json.loads((BASE / "manifest.json").read_text())
    inventory = {entry["path"]: entry for entry in manifest["files"]}
    assert len(inventory) == len(manifest["files"])
    assert manifest["preservation_only"] and not manifest["authority_promoted"]
    images, source_checks = {}, 0
    for entry in inventory.values():
        path = local(entry["path"])
        assert path.stat().st_size == entry["bytes"], path
        assert digest(path) == entry["sha256"], path
        if path.suffix == ".json":
            json.loads(path.read_text())
        if path.suffix == ".png":
            images[entry["path"]] = decode_png(path)
        if args.verify_sources:
            # tmp sources remain immutable; authority-document snapshots may predate README updates.
            origin = entry["source_path_at_preservation"]
            if origin.startswith("tmp/"):
                assert digest(args.verify_sources / origin) == entry["sha256"], origin
                source_checks += 1

    def asset(entry):
        stored = inventory[entry["path"]]
        assert entry["sha256"] == stored["sha256"]
        assert entry["bytes"] == stored["bytes"]

    expected = {"N16", "N20", "N21", "N22", "N24", "N27", "N28", "N30",
                "SU03", "SU05", "SU06", "SU08", "SU11", "SU14"}
    expected.update(f"AF{i:02}" for i in range(1, 12))
    assert {scene["id"] for scene in manifest["scenes"]} == expected
    assert len(manifest["scenes"]) == 25
    calls = 0
    for scene in manifest["scenes"]:
        assert not scene["authority_promoted"]
        asset(scene["final_image"])
        album = scene["album_entry_at_preservation"]
        assert scene["final_image"]["sha256"] == album["sha256"]
        assert images[scene["final_image"]["path"]] == (album["width"], album["height"])
        local(scene["generation_record"])
        for call in scene["calls"]:
            asset(call["prompt"])
            asset(call["output"])
            for reference in call["inputs"]:
                assert reference["role"]
                asset(reference)
            calls += 1
        assert any(call["output"]["sha256"] == scene["final_image"]["sha256"] for call in scene["calls"])

    entries = json.loads((BASE / "path-resolutions.json").read_text())["entries"]
    for entry in entries:
        assert entry["path"] in inventory
        value = json.loads(local(entry["record"]).read_text())
        for token in entry["json_pointer"].split("/")[1:]:
            key = token.replace("~1", "/").replace("~0", "~")
            value = value[int(key)] if isinstance(value, list) else value[key]
        assert value == entry["original_value"]
        local(entry["path"])
    for value in manifest["selection_and_feedback_evidence"]:
        local(value)
    links = re.findall(r"\]\(([^)]+)\)", (BASE / "README.md").read_text())
    for value in links:
        local(value)
    print(json.dumps({"status": "pass", "scenes": 25, "files": len(inventory),
                      "png_crc_and_pixel_stream_checks": len(images), "generation_records_or_calls": calls,
                      "resolved_references": len(entries), "readme_links": len(links),
                      "original_tmp_files_compared": source_checks}, indent=2))


if __name__ == "__main__":
    main()
