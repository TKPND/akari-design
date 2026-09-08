"""Validate the selected native assets, edit lineage, hashes and local links."""
from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import argparse
import hashlib
import json
import re
import struct
import zlib

parser = argparse.ArgumentParser()
parser.add_argument("--write-report", action="store_true",
                    help="Refresh inventory and validation report after reviewing changes.")
args = parser.parse_args()
root = Path(__file__).resolve().parent
base = root.parents[1]
repo = base.parent
cache = {}
checks = {"hashes": 0, "pngs": 0, "links": 0}

def resolve(value):
    path = Path(value)
    assert not path.is_absolute(), f"Absolute package path: {value}"
    result = (base / path).resolve()
    assert result.is_relative_to(repo), f"Path outside repository: {value}"
    assert result.is_file(), f"Missing file: {value}"
    return result

def inspect(path):
    path = path.resolve()
    if path in cache:
        return cache[path]
    data = path.read_bytes()
    result = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    if path.suffix.lower() == ".png":
        assert data[:8] == bytes.fromhex("89504e470d0a1a0a"), path
        pos, compressed, ended = 8, [], False
        while pos < len(data):
            size = struct.unpack(">I", data[pos:pos + 4])[0]
            kind = data[pos + 4:pos + 8]
            payload = data[pos + 8:pos + 8 + size]
            crc = struct.unpack(">I", data[pos + 8 + size:pos + 12 + size])[0]
            assert len(payload) == size
            assert (zlib.crc32(kind + payload) & 0xffffffff) == crc, path
            if kind == b"IHDR":
                result["width"], result["height"] = struct.unpack(">II", payload[:8])
            if kind == b"IDAT":
                compressed.append(payload)
            pos += size + 12
            if kind == b"IEND":
                ended = True
                break
        assert ended and pos == len(data) and zlib.decompress(b"".join(compressed)), path
        checks["pngs"] += 1
    cache[path] = result
    return result

def check_asset(asset):
    info = inspect(resolve(asset["path"]))
    for key in ("sha256", "bytes", "width", "height"):
        if key in asset:
            assert asset[key] == info[key], f"{asset['path']}: {key} mismatch"
    checks["hashes"] += 1

manifest = json.loads((root / "manifest.json").read_text())
selection = json.loads((root / "selection.json").read_text())
references = json.loads(resolve(manifest["references"]).read_text())["references"]
entries = manifest["entries"]
expected = [f"{theme}{number:02}" for theme, numbers in (
    ("A", (4, 8, 9, 13, 15, 16)), ("B", (1, 3, 7, 9, 14, 16)),
    ("C", (2, 4, 11, 12, 13, 15))) for number in numbers]
assert manifest["selected_ids"] == selection["selected_ids"] == expected
assert [entry["id"] for entry in entries] == expected
assert manifest["selected_count"] == len(entries) == 18
assert len(list((root / "images").glob("*.png"))) == 18
assert selection["A04"]["revision"] == "A04-r4"
assert len({ref["id"] for ref in references}) == len(references) == 6
for ref in references:
    check_asset(ref)
for entry in entries:
    check_asset(entry["output"])
    check_asset(entry["prompt"])
    assert entry["visual_review"]["verdict"] == "pass", entry["id"]
    assert entry["face_authority_promoted"] is False
    record = json.loads(resolve(entry["record"]).read_text())
    assert record["output"] == entry["output"] and record["prompt"] == entry["prompt"]
for value in manifest["generation_records"]:
    record = json.loads(resolve(value).read_text())
    assert record["tool_mode"] == "built-in-imagegen" and record["model"] is None
    assert [item["id"] for item in record["inputs"]] == record["input_ids"]
    assert len(record["inputs"]) == 5
    check_asset(record["output"])
    check_asset(record["prompt"])
    for asset in record["inputs"]:
        check_asset(asset)
history = json.loads(resolve(manifest["A04_correction"]).read_text())
assert [item["id"] for item in history["history"]] == ["A04", "A04-r2", "A04-r3", "A04-r4"]
assert history["selected_revision"] == "A04-r4"
for item in history["history"]:
    check_asset(item["output"])
    check_asset(item["prompt"])
    resolve(item["record"])
assert history["history"][-1]["review"]["verdict"] == "pass"
assert entries[0]["output"] == history["history"][-1]["output"]

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.images = [], [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.links.extend(value for key, value in attrs.items()
                          if key in ("href", "src") and value)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "img":
            self.images.append(attrs.get("src"))

page = root / "index.html"
links = Links()
links.feed(page.read_text())
assert set(links.ids) == set(expected)
assert len(links.images) == 18
for value in links.links:
    parsed = urlsplit(value)
    assert not parsed.scheme and not parsed.netloc and not parsed.path.startswith("/")
    if parsed.path:
        assert (page.parent / unquote(parsed.path)).resolve().is_file(), value
    if parsed.fragment:
        assert parsed.fragment in links.ids, value
    checks["links"] += 1
for value in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", (root / "README.md").read_text()):
    parsed = urlsplit(value)
    if parsed.scheme:
        continue
    target = (root / unquote(parsed.path)).resolve()
    if args.write_report and target.name in ("validation.json", "asset-inventory.json"):
        continue
    assert target.is_file(), value
    checks["links"] += 1

inventory_path = root / "asset-inventory.json"
excluded = {"asset-inventory.json", "validation.json"}
files = sorted(path for path in root.rglob("*") if path.is_file() and path.name not in excluded)
items = [{"path": path.relative_to(base).as_posix(), **inspect(path)} for path in files]
if args.write_report:
    inventory_path.write_text(json.dumps({"path_base": "akari-v3.1", "files": items},
                                        ensure_ascii=False, indent=2) + "\n")
else:
    saved = json.loads(inventory_path.read_text())["files"]
    assert saved == items, "Package differs from the recorded inventory"
report = {
    "status": "pass", "checked_at": datetime.now(timezone.utc).isoformat(),
    "selected_count": 18, "generation_records": len(manifest["generation_records"]),
    "package_file_count_excluding_reports": len(items),
    "checks": checks, "A04_selected_revision": "A04-r4",
    "native_png_validation": "signature, dimensions, CRC, zlib and SHA-256 passed",
    "references_and_edit_inputs": "All current and historical inputs resolve within the repository and match their recorded hashes.",
    "visual_review": "18 selected scenes reviewed; A04-r4 additionally inspected in a footwork enlargement.",
    "browser_render_check": "Not performed: no browser backend was available.",
    "preview_check": "Static thumbnails/contact sheets and their source links checked.",
    "approval_scope": "User selected 18 scene IDs; assistant verified A04 correction."
}
if args.write_report:
    (root / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(report, ensure_ascii=False, indent=2))
