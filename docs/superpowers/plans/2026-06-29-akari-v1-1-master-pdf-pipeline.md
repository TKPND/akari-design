# Akari v1.1 Master PDF Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible pipeline that turns Akari v1.1 source images,
D65/sRGB palette data, reviewed generated assets, and deterministic layouts into
a polished 12-page 16:9 PDF settings document.

**Architecture:** Keep original images immutable under `source/originals/`, keep
review state in JSON manifests, generate page HTML with deterministic text and
CSS, then use Playwright/Chrome for page previews and PDF export. Python audit
scripts validate manifests, palette roles, source hashes, PDF structure,
rendered-page dimensions, searchable text, and alpha-edge risks.

**Tech Stack:** Python 3 standard library plus Pillow, Node ESM, Playwright using
the installed Google Chrome channel, ImageMagick, Poppler tools, qpdf, exiftool,
and markdownlint-cli2.

---

## Current Context

- Spec:
  `docs/superpowers/specs/2026-06-29-akari-v1-1-palette-anchored-master-pdf-design.md`
- Existing source files at repo root:
  `v1_1_front_1.webp`, `v1_1_front_2.webp`, `v1_1_front_3.webp`,
  `v1_1_back.webp`, `v1_1_真横.webp`, `v1_1_髪飾り側_45deg.webp`,
  `v1_1_非髪飾り側45deg.webp`, `v1_1_standard_foot_set.webp`,
  `v1_1_shoes.webp`, and `v1_1_bag.webp`.
- Confirmed local tools:
  `python3`, `node`, `npm`, `google-chrome`, `identify`, `compare`,
  `pdfinfo`, `pdffonts`, `pdftoppm`, `pdftotext`, `qpdf`, and `exiftool`.
- Existing lint config:
  `.markdownlint.json`.

## Target File Structure

```text
package.json
package-lock.json
requirements.txt
.gitignore
source/originals/*.png
source/palette/akari-v1.1-palette.json
source/manifests/source-assets.json
source/manifests/asset-manifest.json
source/manifests/page-manifest.json
source/manifests/generation-requests.json
source/manifests/color-review.json
scripts/akari_assets.py
scripts/prepare_sources.py
scripts/audit_assets.py
scripts/audit_palette.py
scripts/render_page_previews.py
scripts/export_pdf.py
scripts/audit_pdf.py
scripts/audit_alpha_edges.py
tests/test_environment_contract.py
tests/test_asset_manifest_contract.py
tests/test_palette_contract.py
tests/test_pdf_contract.py
tools/pdf/document.mjs
tools/pdf/theme.mjs
tools/pdf/render-html.mjs
tools/pdf/render.mjs
tools/pdf/document.test.mjs
tools/pdf/styles.css
build/assets/generated/
build/assets/corrected/
build/page-previews/
build/pdf-rendered-pages/
dist/akari-v1.1-settings.pdf
dist/akari-v1.1-settings-pages/
```

Generated build folders are allowed to be recreated. Final reviewed assets and
the final PDF are project deliverables; decide at the end whether to commit the
binary outputs after checking size and usefulness.

## Task 1: Toolchain Scaffold And Preflight

**Files:**

- Create: `package.json`
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `scripts/verify_environment.py`
- Create: `tests/test_environment_contract.py`

- [ ] **Step 1: Write the environment contract test**

Create `tests/test_environment_contract.py`:

```python
import shutil
import subprocess
import unittest


REQUIRED_TOOLS = [
    "python3",
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


class EnvironmentContractTest(unittest.TestCase):
    def test_required_tools_are_available(self):
        missing = [tool for tool in REQUIRED_TOOLS if shutil.which(tool) is None]
        self.assertEqual([], missing)

    def test_qpdf_runs(self):
        result = subprocess.run(
            ["qpdf", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("qpdf version", result.stdout)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test before the helper exists**

Run:

```bash
python3 -m unittest tests/test_environment_contract.py
```

Expected: PASS because the user has installed the required system tools.

- [ ] **Step 3: Add project package metadata**

Create `package.json`:

```json
{
  "name": "akari-v1-1-master-pdf",
  "private": true,
  "type": "module",
  "scripts": {
    "lint:md": "markdownlint-cli2 '**/*.md' '#node_modules'",
    "test:node": "node --test tools/pdf/*.test.mjs",
    "test:python": "python3 -m unittest discover -s tests",
    "prepare:sources": "python3 scripts/prepare_sources.py",
    "build:previews": "python3 scripts/render_page_previews.py",
    "build:pdf": "python3 scripts/export_pdf.py",
    "audit:assets": "python3 scripts/audit_assets.py",
    "audit:palette": "python3 scripts/audit_palette.py",
    "audit:pdf": "python3 scripts/audit_pdf.py dist/akari-v1.1-settings.pdf",
    "audit:alpha": "python3 scripts/audit_alpha_edges.py",
    "audit": "npm run audit:assets && npm run audit:palette && npm run audit:pdf && npm run audit:alpha"
  },
  "devDependencies": {
    "markdownlint-cli2": "^0.22.1",
    "playwright": "^1.53.0"
  }
}
```

- [ ] **Step 4: Add Python dependency declaration**

Create `requirements.txt`:

```text
Pillow>=10,<13
```

- [ ] **Step 5: Add generated-cache ignores**

Create `.gitignore`:

```gitignore
node_modules/
.venv/
__pycache__/
*.pyc
.pytest_cache/
build/site/
build/tmp/
```

- [ ] **Step 6: Install Node and Python dependencies**

Run:

```bash
npm install
python3 -m pip install -r requirements.txt
```

Expected: `package-lock.json` is created and Pillow is importable.

- [ ] **Step 7: Add the environment helper**

Create `scripts/verify_environment.py`:

```python
#!/usr/bin/env python3
import shutil
import subprocess
import sys


REQUIRED_TOOLS = [
    "python3",
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


def main() -> int:
    missing = [tool for tool in REQUIRED_TOOLS if shutil.which(tool) is None]
    if missing:
        print("Missing required tools: " + ", ".join(missing), file=sys.stderr)
        return 1

    for command in (["qpdf", "--version"], ["exiftool", "-ver"]):
        subprocess.run(command, check=True, capture_output=True, text=True)

    print("environment: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 8: Verify and commit**

Run:

```bash
python3 scripts/verify_environment.py
python3 -m unittest tests/test_environment_contract.py
npm run lint:md
git diff --check
```

Expected:

- `environment: ok`
- Python test passes.
- Markdown lint reports 0 errors.
- `git diff --check` reports no whitespace errors.

Commit:

```bash
git add package.json package-lock.json requirements.txt .gitignore scripts/verify_environment.py tests/test_environment_contract.py
git commit -m "Add Akari PDF toolchain scaffold"
```

## Task 2: Source Asset Ingestion And Hash Manifest

**Files:**

- Create: `scripts/akari_assets.py`
- Create: `scripts/prepare_sources.py`
- Create: `scripts/audit_assets.py`
- Create: `tests/test_asset_manifest_contract.py`
- Generate: `source/originals/*.png`
- Generate: `source/manifests/source-assets.json`

- [ ] **Step 1: Write the manifest contract test**

Create `tests/test_asset_manifest_contract.py`:

```python
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "source/manifests/source-assets.json"


class AssetManifestContractTest(unittest.TestCase):
    def test_source_manifest_has_ten_assets(self):
        data = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(10, len(data["assets"]))

    def test_asset_entries_have_required_fields(self):
        data = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
        required = {
            "id",
            "original_filename",
            "source_path",
            "sha256",
            "width",
            "height",
            "colorspace",
            "role",
            "orientation_state",
        }
        for asset in data["assets"]:
            self.assertTrue(required.issubset(asset))
            self.assertEqual(64, len(asset["sha256"]))
            self.assertTrue((ROOT / asset["source_path"]).exists())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
python3 -m unittest tests/test_asset_manifest_contract.py
```

Expected: FAIL because `source/manifests/source-assets.json` does not exist.

- [ ] **Step 3: Add the asset catalog**

Create `scripts/akari_assets.py`:

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SOURCE_ASSETS = [
    {
        "id": "hoodie-front",
        "filename": "v1_1_front_1.webp",
        "role": "secondary_full_body_outfit_anchor",
        "orientation_state": "front_view_character_left_is_viewer_right",
    },
    {
        "id": "base-front",
        "filename": "v1_1_front_2.webp",
        "role": "base_body_outfit_anchor",
        "orientation_state": "front_view_character_left_is_viewer_right",
    },
    {
        "id": "expression-sheet",
        "filename": "v1_1_front_3.webp",
        "role": "primary_face_hair_identity_anchor",
        "orientation_state": "expression_grid_unmirrored",
    },
    {
        "id": "hoodie-back",
        "filename": "v1_1_back.webp",
        "role": "back_turnaround_anchor",
        "orientation_state": "back_view_unmirrored",
    },
    {
        "id": "side-view",
        "filename": "v1_1_真横.webp",
        "role": "side_turnaround_anchor",
        "orientation_state": "side_view_unmirrored",
    },
    {
        "id": "hairpin-side-45",
        "filename": "v1_1_髪飾り側_45deg.webp",
        "role": "hairpin_side_turnaround_anchor",
        "orientation_state": "hairpin_side_45_unmirrored",
    },
    {
        "id": "non-hairpin-side-45",
        "filename": "v1_1_非髪飾り側45deg.webp",
        "role": "non_hairpin_side_turnaround_anchor",
        "orientation_state": "non_hairpin_side_45_unmirrored",
    },
    {
        "id": "footwear-board",
        "filename": "v1_1_standard_foot_set.webp",
        "role": "footwear_sock_reference_board",
        "orientation_state": "board_unmirrored",
    },
    {
        "id": "shoe-board",
        "filename": "v1_1_shoes.webp",
        "role": "sneaker_reference_board",
        "orientation_state": "board_unmirrored",
    },
    {
        "id": "bag-board",
        "filename": "v1_1_bag.webp",
        "role": "bag_accessory_reference_board",
        "orientation_state": "board_unmirrored",
    },
]
```

- [ ] **Step 4: Add the source preparation script**

Create `scripts/prepare_sources.py`:

```python
#!/usr/bin/env python3
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from akari_assets import ROOT, SOURCE_ASSETS


ORIGINALS_DIR = ROOT / "source/originals"
MANIFEST_DIR = ROOT / "source/manifests"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_metadata(path: Path) -> dict:
    result = subprocess.run(
        ["identify", "-format", "%w %h %[colorspace]", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    width, height, colorspace = result.stdout.strip().split()
    return {
        "width": int(width),
        "height": int(height),
        "colorspace": colorspace,
    }


def main() -> int:
    ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    manifest_assets = []
    for asset in SOURCE_ASSETS:
        source = ROOT / asset["filename"]
        if not source.exists():
            raise FileNotFoundError(source)
        target = ORIGINALS_DIR / asset["filename"]
        if not target.exists() or sha256(source) != sha256(target):
            shutil.copy2(source, target)
        metadata = image_metadata(target)
        manifest_assets.append(
            {
                "id": asset["id"],
                "original_filename": asset["filename"],
                "source_path": str(target.relative_to(ROOT)),
                "sha256": sha256(target),
                "width": metadata["width"],
                "height": metadata["height"],
                "colorspace": metadata["colorspace"],
                "role": asset["role"],
                "orientation_state": asset["orientation_state"],
            }
        )

    payload = {
        "schema_version": 1,
        "asset_count": len(manifest_assets),
        "assets": manifest_assets,
    }
    (MANIFEST_DIR / "source-assets.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"source assets prepared: {len(manifest_assets)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Add the asset audit script**

Create `scripts/audit_assets.py`:

```python
#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "source/manifests/source-assets.json"
ASSET_MANIFEST = ROOT / "source/manifests/asset-manifest.json"
PAGE_MANIFEST = ROOT / "source/manifests/page-manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors = []
    source = load_json(SOURCE_MANIFEST)
    if source.get("asset_count") != 10:
        errors.append("source asset_count must be 10")

    ids = set()
    for asset in source["assets"]:
        ids.add(asset["id"])
        path = ROOT / asset["source_path"]
        if not path.exists():
            errors.append(f"missing source asset: {asset['source_path']}")
            continue
        actual = sha256(path)
        if actual != asset["sha256"]:
            errors.append(f"sha256 mismatch: {asset['id']}")
        if asset["colorspace"] not in {"sRGB", "RGB"}:
            errors.append(f"unexpected colorspace for {asset['id']}: {asset['colorspace']}")

    if ASSET_MANIFEST.exists():
        data = load_json(ASSET_MANIFEST)
        for asset in data.get("assets", []):
            if asset["status"] not in {"needs_review", "accepted", "rejected", "needs_correction"}:
                errors.append(f"bad asset status: {asset['id']}")
            if asset["status"] != "accepted" and asset.get("used_in_final_pdf", False):
                errors.append(f"unaccepted asset used in final PDF: {asset['id']}")

    if PAGE_MANIFEST.exists():
        pages = load_json(PAGE_MANIFEST)
        if len(pages.get("pages", [])) != 12:
            errors.append("page-manifest must define 12 pages")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("asset audit: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 6: Prepare, test, and commit**

Run:

```bash
python3 scripts/prepare_sources.py
python3 -m unittest tests/test_asset_manifest_contract.py
python3 scripts/audit_assets.py
identify -format '%f %wx%h\n' source/originals/*.png
git diff --check
```

Expected:

- `source assets prepared: 10`
- Python tests pass.
- `asset audit: ok`
- `identify` lists 10 files with the dimensions recorded in the spec.

Commit:

```bash
git add scripts/akari_assets.py scripts/prepare_sources.py scripts/audit_assets.py tests/test_asset_manifest_contract.py source/originals source/manifests/source-assets.json
git commit -m "Add Akari source asset manifest"
```

## Task 3: Palette Manifest And Palette Audit

**Files:**

- Create: `source/palette/akari-v1.1-palette.json`
- Create: `scripts/audit_palette.py`
- Create: `tests/test_palette_contract.py`
- Create: `source/manifests/color-review.json`

- [ ] **Step 1: Write the palette contract test**

Create `tests/test_palette_contract.py`:

```python
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PALETTE = ROOT / "source/palette/akari-v1.1-palette.json"


class PaletteContractTest(unittest.TestCase):
    def test_palette_roles_are_complete(self):
        data = json.loads(PALETTE.read_text(encoding="utf-8"))
        roles = {role["name"] for role in data["roles"]}
        expected = {
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
        self.assertEqual(expected, roles)

    def test_each_role_has_hex_rgb_usage_and_tolerance(self):
        data = json.loads(PALETTE.read_text(encoding="utf-8"))
        for role in data["roles"]:
            self.assertRegex(role["hex"], r"^#[0-9A-Fa-f]{6}$")
            self.assertEqual(3, len(role["rgb"]))
            self.assertTrue(role["usage"])
            self.assertIn("median_rgb_delta", role["tolerance"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
python3 -m unittest tests/test_palette_contract.py
```

Expected: FAIL because the palette JSON does not exist.

- [ ] **Step 3: Add the palette manifest**

Create `source/palette/akari-v1.1-palette.json`:

```json
{
  "schema_version": 1,
  "palette_version": "akari-v1.1-d65-srgb-1",
  "white_point": "D65",
  "color_space": "sRGB",
  "roles": [
    {
      "name": "hair",
      "hex": "#6B4A37",
      "rgb": [107, 74, 55],
      "usage": "Brown bob hair base tone.",
      "ramp": {
        "base": "#6B4A37",
        "shadow": "#4A3126",
        "highlight": "#A47A5D"
      },
      "sample_area": "expression-sheet hair midtone and hoodie-front hair midtone",
      "tolerance": {"median_rgb_delta": 12},
      "exception_policy": "Allow darker strand shadows when hue remains brown."
    },
    {
      "name": "skin",
      "hex": "#F4CBBE",
      "rgb": [244, 203, 190],
      "usage": "Face, hands, and legs.",
      "ramp": {
        "base": "#F4CBBE",
        "shadow": "#E7AFA6",
        "highlight": "#FFE3D8"
      },
      "sample_area": "face cheek-neutral skin zones",
      "tolerance": {"median_rgb_delta": 12},
      "exception_policy": "Blush may exceed tolerance on cheek-only samples."
    },
    {
      "name": "eyes",
      "hex": "#7B5742",
      "rgb": [123, 87, 66],
      "usage": "Warm brown iris color.",
      "ramp": {
        "base": "#7B5742",
        "shadow": "#3E2A24",
        "highlight": "#C38E68"
      },
      "sample_area": "expression-sheet iris midtone",
      "tolerance": {"median_rgb_delta": 14},
      "exception_policy": "Eye highlights use near-white sparkle tones."
    },
    {
      "name": "hoodie_white",
      "hex": "#F5F4EE",
      "rgb": [245, 244, 238],
      "usage": "Hoodie base fabric.",
      "ramp": {
        "base": "#F5F4EE",
        "shadow": "#D9DBD8",
        "highlight": "#FFFFFF"
      },
      "sample_area": "hoodie-front flat chest and sleeve areas",
      "tolerance": {"median_rgb_delta": 10},
      "exception_policy": "Fold shadows may be cooler but must not become blue-gray."
    },
    {
      "name": "hoodie_shadow",
      "hex": "#D9DBD8",
      "rgb": [217, 219, 216],
      "usage": "Hoodie folds, cuffs, pocket shadow, and hem shadow.",
      "ramp": {
        "base": "#D9DBD8",
        "shadow": "#BFC4C3",
        "highlight": "#F5F4EE"
      },
      "sample_area": "hoodie folds and pocket shadow",
      "tolerance": {"median_rgb_delta": 12},
      "exception_policy": "Contact shadows may be darker if neutral."
    },
    {
      "name": "skirt_gray",
      "hex": "#74777D",
      "rgb": [116, 119, 125],
      "usage": "Pleated skirt fabric.",
      "ramp": {
        "base": "#74777D",
        "shadow": "#555960",
        "highlight": "#A2A6AC"
      },
      "sample_area": "skirt front midtone pleats",
      "tolerance": {"median_rgb_delta": 12},
      "exception_policy": "Pleat lines may be darker when still neutral gray."
    },
    {
      "name": "sock_white",
      "hex": "#F7F8F4",
      "rgb": [247, 248, 244],
      "usage": "Crew sock base.",
      "ramp": {
        "base": "#F7F8F4",
        "shadow": "#DDE4E3",
        "highlight": "#FFFFFF"
      },
      "sample_area": "sock calf flat areas",
      "tolerance": {"median_rgb_delta": 10},
      "exception_policy": "Shoe contact shadows may be darker."
    },
    {
      "name": "sock_stripe_blue",
      "hex": "#9BD8E5",
      "rgb": [155, 216, 229],
      "usage": "Two sock stripes near the top.",
      "ramp": {
        "base": "#9BD8E5",
        "shadow": "#6EB8CA",
        "highlight": "#C9F1F6"
      },
      "sample_area": "sock stripe bands",
      "tolerance": {"median_rgb_delta": 12},
      "exception_policy": "Keep stripe count and position more important than tiny shade drift."
    },
    {
      "name": "sneaker_white",
      "hex": "#F4F5EF",
      "rgb": [244, 245, 239],
      "usage": "Chunky sneaker base.",
      "ramp": {
        "base": "#F4F5EF",
        "shadow": "#D7DFE0",
        "highlight": "#FFFFFF"
      },
      "sample_area": "shoe upper and sole broad white zones",
      "tolerance": {"median_rgb_delta": 10},
      "exception_policy": "Outsole contact shadows can be darker but not muddy."
    },
    {
      "name": "sneaker_accent_blue",
      "hex": "#A4DDE8",
      "rgb": [164, 221, 232],
      "usage": "Sneaker accent panels and detail lines.",
      "ramp": {
        "base": "#A4DDE8",
        "shadow": "#75BFD0",
        "highlight": "#D4F5F8"
      },
      "sample_area": "shoe blue accent panels",
      "tolerance": {"median_rgb_delta": 12},
      "exception_policy": "Use same hue family as sock stripe blue."
    },
    {
      "name": "bag_body",
      "hex": "#F1EEE4",
      "rgb": [241, 238, 228],
      "usage": "Mini shoulder bag body.",
      "ramp": {
        "base": "#F1EEE4",
        "shadow": "#D5CEC0",
        "highlight": "#FFFFFF"
      },
      "sample_area": "bag broad body panels",
      "tolerance": {"median_rgb_delta": 12},
      "exception_policy": "Fabric grain can vary within neutral warm range."
    },
    {
      "name": "bag_strap",
      "hex": "#B5A997",
      "rgb": [181, 169, 151],
      "usage": "Bag strap and binding.",
      "ramp": {
        "base": "#B5A997",
        "shadow": "#8E8170",
        "highlight": "#D5CABA"
      },
      "sample_area": "bag strap flat sections",
      "tolerance": {"median_rgb_delta": 12},
      "exception_policy": "Contact shadows may be darker near hardware."
    },
    {
      "name": "metal",
      "hex": "#B7B8B3",
      "rgb": [183, 184, 179],
      "usage": "Zippers, rings, and small metal accents.",
      "ramp": {
        "base": "#B7B8B3",
        "shadow": "#8D918F",
        "highlight": "#E7E8E1"
      },
      "sample_area": "bag hardware and zipper pulls",
      "tolerance": {"median_rgb_delta": 14},
      "exception_policy": "Specular highlights may be near-white."
    }
  ]
}
```

- [ ] **Step 4: Add color review record**

Create `source/manifests/color-review.json`:

```json
{
  "schema_version": 1,
  "palette_version": "akari-v1.1-d65-srgb-1",
  "review_target": "D65/6500K sRGB document consistency",
  "review_status": "initial_palette_ready_for_page_preview_review",
  "review_notes": [
    "Palette values are canonical document targets, not claims of embedded ICC data in the original PNGs.",
    "Flat swatches must render exactly in the PDF preview.",
    "Illustrated shaded regions are judged by hue family, lightness range, and visual review."
  ]
}
```

- [ ] **Step 5: Add the palette audit script**

Create `scripts/audit_palette.py`:

```python
#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PALETTE = ROOT / "source/palette/akari-v1.1-palette.json"
PAGE_MANIFEST = ROOT / "source/manifests/page-manifest.json"

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


def hex_to_rgb(value: str) -> list[int]:
    return [int(value[index:index + 2], 16) for index in (1, 3, 5)]


def main() -> int:
    data = json.loads(PALETTE.read_text(encoding="utf-8"))
    errors = []

    if data.get("white_point") != "D65":
        errors.append("palette white_point must be D65")
    if data.get("color_space") != "sRGB":
        errors.append("palette color_space must be sRGB")

    names = set()
    for role in data.get("roles", []):
        name = role.get("name", "")
        if name in names:
            errors.append(f"duplicate role: {name}")
        names.add(name)
        if not HEX_RE.match(role.get("hex", "")):
            errors.append(f"bad hex for role: {name}")
            continue
        if role.get("rgb") != hex_to_rgb(role["hex"]):
            errors.append(f"rgb does not match hex for role: {name}")
        if "median_rgb_delta" not in role.get("tolerance", {}):
            errors.append(f"missing tolerance for role: {name}")

    if PAGE_MANIFEST.exists():
        pages = json.loads(PAGE_MANIFEST.read_text(encoding="utf-8"))
        palette_pages = [
            page for page in pages.get("pages", [])
            if page.get("role") == "palette"
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
```

- [ ] **Step 6: Verify and commit**

Run:

```bash
python3 -m unittest tests/test_palette_contract.py
python3 scripts/audit_palette.py
git diff --check
```

Expected:

- Python test passes.
- `palette audit: ok (13 roles)`
- No whitespace errors.

Commit:

```bash
git add source/palette/akari-v1.1-palette.json source/manifests/color-review.json scripts/audit_palette.py tests/test_palette_contract.py
git commit -m "Add Akari D65 palette manifest"
```

## Task 4: Accepted Asset And Page Manifests

**Files:**

- Create: `source/manifests/asset-manifest.json`
- Create: `source/manifests/page-manifest.json`
- Create: `source/manifests/generation-requests.json`
- Modify: `scripts/audit_assets.py`
- Modify: `tests/test_asset_manifest_contract.py`

- [ ] **Step 1: Extend manifest tests**

Append these tests to `tests/test_asset_manifest_contract.py`:

```python
    def test_final_pages_have_accepted_asset_inputs(self):
        asset_manifest = json.loads(
            (ROOT / "source/manifests/asset-manifest.json").read_text(encoding="utf-8")
        )
        page_manifest = json.loads(
            (ROOT / "source/manifests/page-manifest.json").read_text(encoding="utf-8")
        )
        accepted = {
            asset["id"]
            for asset in asset_manifest["assets"]
            if asset["status"] == "accepted"
        }
        self.assertEqual(12, len(page_manifest["pages"]))
        for page in page_manifest["pages"]:
            self.assertTrue(page["source_inputs"])
            for asset_id in page["source_inputs"]:
                self.assertIn(asset_id, accepted)
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
python3 -m unittest tests/test_asset_manifest_contract.py
```

Expected: FAIL because `asset-manifest.json` and `page-manifest.json` do not
exist.

- [ ] **Step 3: Add accepted source asset manifest**

Create `source/manifests/asset-manifest.json`:

```json
{
  "schema_version": 1,
  "palette_version": "akari-v1.1-d65-srgb-1",
  "assets": [
    {
      "id": "hoodie-front",
      "status": "accepted",
      "source_inputs": ["hoodie-front"],
      "prompt_summary": "",
      "model_or_tool": "source_png",
      "seed_or_generation_id": "",
      "palette_version": "akari-v1.1-d65-srgb-1",
      "orientation_state": "front_view_character_left_is_viewer_right",
      "identity_check": "passes visual anchor role as secondary full-body/outfit master",
      "color_check": "assumed sRGB source, pending page-level palette comparison",
      "layout_check": "usable as source input, not final page composition",
      "reviewer": "Codex + user visual review",
      "accepted_reason": "Primary hoodie front reference chosen during brainstorming.",
      "used_in_final_pdf": true
    },
    {
      "id": "base-front",
      "status": "accepted",
      "source_inputs": ["base-front"],
      "prompt_summary": "",
      "model_or_tool": "source_png",
      "seed_or_generation_id": "",
      "palette_version": "akari-v1.1-d65-srgb-1",
      "orientation_state": "front_view_character_left_is_viewer_right",
      "identity_check": "passes as base/body construction reference",
      "color_check": "assumed sRGB source, pending page-level palette comparison",
      "layout_check": "usable as source input",
      "reviewer": "Codex + user visual review",
      "accepted_reason": "Official base outfit/body anchor.",
      "used_in_final_pdf": true
    },
    {
      "id": "expression-sheet",
      "status": "accepted",
      "source_inputs": ["expression-sheet"],
      "prompt_summary": "",
      "model_or_tool": "source_png",
      "seed_or_generation_id": "",
      "palette_version": "akari-v1.1-d65-srgb-1",
      "orientation_state": "expression_grid_unmirrored",
      "identity_check": "passes as primary face/hair identity master",
      "color_check": "assumed sRGB source, pending page-level palette comparison",
      "layout_check": "usable with deterministic PDF labels",
      "reviewer": "Codex + user visual review",
      "accepted_reason": "Selected as identity master.",
      "used_in_final_pdf": true
    },
    {
      "id": "hoodie-back",
      "status": "accepted",
      "source_inputs": ["hoodie-back"],
      "prompt_summary": "",
      "model_or_tool": "source_png",
      "seed_or_generation_id": "",
      "palette_version": "akari-v1.1-d65-srgb-1",
      "orientation_state": "back_view_unmirrored",
      "identity_check": "passes as back turnaround source",
      "color_check": "assumed sRGB source, pending page-level palette comparison",
      "layout_check": "usable as source input",
      "reviewer": "Codex + user visual review",
      "accepted_reason": "Official back view source.",
      "used_in_final_pdf": true
    },
    {
      "id": "side-view",
      "status": "accepted",
      "source_inputs": ["side-view"],
      "prompt_summary": "",
      "model_or_tool": "source_png",
      "seed_or_generation_id": "",
      "palette_version": "akari-v1.1-d65-srgb-1",
      "orientation_state": "side_view_unmirrored",
      "identity_check": "passes as side turnaround source",
      "color_check": "assumed sRGB source, pending page-level palette comparison",
      "layout_check": "usable as source input",
      "reviewer": "Codex + user visual review",
      "accepted_reason": "Official side view source.",
      "used_in_final_pdf": true
    },
    {
      "id": "hairpin-side-45",
      "status": "accepted",
      "source_inputs": ["hairpin-side-45"],
      "prompt_summary": "",
      "model_or_tool": "source_png",
      "seed_or_generation_id": "",
      "palette_version": "akari-v1.1-d65-srgb-1",
      "orientation_state": "hairpin_side_45_unmirrored",
      "identity_check": "passes as hairpin-side 45-degree source",
      "color_check": "assumed sRGB source, pending page-level palette comparison",
      "layout_check": "usable as source input",
      "reviewer": "Codex + user visual review",
      "accepted_reason": "Official hairpin-side view source.",
      "used_in_final_pdf": true
    },
    {
      "id": "non-hairpin-side-45",
      "status": "accepted",
      "source_inputs": ["non-hairpin-side-45"],
      "prompt_summary": "",
      "model_or_tool": "source_png",
      "seed_or_generation_id": "",
      "palette_version": "akari-v1.1-d65-srgb-1",
      "orientation_state": "non_hairpin_side_45_unmirrored",
      "identity_check": "passes as non-hairpin-side 45-degree source",
      "color_check": "assumed sRGB source, pending page-level palette comparison",
      "layout_check": "usable as source input",
      "reviewer": "Codex + user visual review",
      "accepted_reason": "Official non-hairpin-side view source.",
      "used_in_final_pdf": true
    },
    {
      "id": "footwear-board",
      "status": "accepted",
      "source_inputs": ["footwear-board"],
      "prompt_summary": "",
      "model_or_tool": "source_png",
      "seed_or_generation_id": "",
      "palette_version": "akari-v1.1-d65-srgb-1",
      "orientation_state": "board_unmirrored",
      "identity_check": "passes as sock and footwear source board",
      "color_check": "assumed sRGB source, pending page-level palette comparison",
      "layout_check": "use visuals only; recreate text as PDF text",
      "reviewer": "Codex + user visual review",
      "accepted_reason": "Official footwear/sock board.",
      "used_in_final_pdf": true
    },
    {
      "id": "shoe-board",
      "status": "accepted",
      "source_inputs": ["shoe-board"],
      "prompt_summary": "",
      "model_or_tool": "source_png",
      "seed_or_generation_id": "",
      "palette_version": "akari-v1.1-d65-srgb-1",
      "orientation_state": "board_unmirrored",
      "identity_check": "passes as sneaker construction source board",
      "color_check": "assumed sRGB source, pending page-level palette comparison",
      "layout_check": "use visuals only; recreate text as PDF text",
      "reviewer": "Codex + user visual review",
      "accepted_reason": "Official sneaker reference board.",
      "used_in_final_pdf": true
    },
    {
      "id": "bag-board",
      "status": "accepted",
      "source_inputs": ["bag-board"],
      "prompt_summary": "",
      "model_or_tool": "source_png",
      "seed_or_generation_id": "",
      "palette_version": "akari-v1.1-d65-srgb-1",
      "orientation_state": "board_unmirrored",
      "identity_check": "passes as bag/accessory source board",
      "color_check": "assumed sRGB source, pending page-level palette comparison",
      "layout_check": "use visuals only; recreate text as PDF text",
      "reviewer": "Codex + user visual review",
      "accepted_reason": "Official bag reference board.",
      "used_in_final_pdf": true
    }
  ]
}
```

- [ ] **Step 4: Add 12-page manifest**

Create `source/manifests/page-manifest.json`:

```json
{
  "schema_version": 1,
  "document_id": "akari-v1.1-settings",
  "page_count": 12,
  "pages": [
    {"page": 1, "id": "cover-key-visual", "title": "Akari v1.1", "role": "cover", "source_inputs": ["hoodie-front", "expression-sheet"]},
    {"page": 2, "id": "d65-color-palette", "title": "D65 Color Palette", "role": "palette", "source_inputs": ["hoodie-front", "expression-sheet", "bag-board", "shoe-board"]},
    {"page": 3, "id": "character-summary-proportion", "title": "Character Summary + Proportion", "role": "identity", "source_inputs": ["hoodie-front", "base-front"]},
    {"page": 4, "id": "front-back", "title": "Front / Back", "role": "turnaround", "source_inputs": ["hoodie-front", "hoodie-back"]},
    {"page": 5, "id": "angle-turnaround", "title": "Angle Turnaround", "role": "turnaround", "source_inputs": ["side-view", "hairpin-side-45", "non-hairpin-side-45"]},
    {"page": 6, "id": "expressions", "title": "Expressions", "role": "identity", "source_inputs": ["expression-sheet"]},
    {"page": 7, "id": "hair-face-details", "title": "Hair / Face Details", "role": "detail", "source_inputs": ["expression-sheet", "hoodie-front", "hairpin-side-45", "side-view"]},
    {"page": 8, "id": "outfit-rules", "title": "Outfit Rules", "role": "detail", "source_inputs": ["hoodie-front", "base-front", "hoodie-back"]},
    {"page": 9, "id": "shoes-socks", "title": "Shoes / Socks", "role": "detail", "source_inputs": ["footwear-board", "shoe-board", "hoodie-front"]},
    {"page": 10, "id": "bag-accessories", "title": "Bag / Accessories", "role": "detail", "source_inputs": ["bag-board", "hoodie-front"]},
    {"page": 11, "id": "do-dont", "title": "Do / Don't", "role": "rules", "source_inputs": ["hoodie-front", "expression-sheet", "shoe-board", "bag-board"]},
    {"page": 12, "id": "production-notes-source-manifest", "title": "Production Notes / Source Manifest", "role": "manifest", "source_inputs": ["hoodie-front", "expression-sheet", "bag-board", "shoe-board"]}
  ]
}
```

- [ ] **Step 5: Add generation request queue**

Create `source/manifests/generation-requests.json`:

```json
{
  "schema_version": 1,
  "requests": [
    {
      "id": "cover-key-visual-16x9",
      "status": "queued",
      "target_page": 1,
      "aspect_ratio": "16:9",
      "prompt": "Akari v1.1 character reference key visual, full body, white oversized hoodie with drawstrings and kangaroo pocket, gray pleated skirt, white crew socks with two pale blue stripes, chunky white sneakers with pale blue accents, short brown bob hair, warm brown eyes, small gentle mouth, subtle cheek blush, thin pale blue hair pins on character-left side, clean sRGB D65 neutral lighting, transparent or non-white plain background, no text, no logos, no extra accessories, polished anime reference art.",
      "acceptance": "Must pass identity checklist, hair ornament side check, and D65 palette visual check before asset-manifest status can become accepted."
    },
    {
      "id": "hair-face-detail-board",
      "status": "queued",
      "target_page": 7,
      "aspect_ratio": "16:9",
      "prompt": "Akari v1.1 hair and face detail reference board, close-up views of bangs, side hair volume, back hair volume, warm brown eyes, subtle blush, small mouth shapes, short brown bob around jaw and neck, thin pale blue pins on character-left side, clean D65 sRGB neutral lighting, no text, no labels, no logos, transparent or non-white plain background.",
      "acceptance": "Must preserve expression-sheet face identity and hair ornament orientation."
    },
    {
      "id": "bag-on-body-scale",
      "status": "queued",
      "target_page": 10,
      "aspect_ratio": "4:5",
      "prompt": "Akari v1.1 wearing the official mini shoulder bag for scale, same white hoodie, gray pleated skirt, white socks with two pale blue stripes, chunky white sneakers with pale blue accents, short brown bob, warm brown eyes, pale neutral mini shoulder bag with strap and small metal accents, clean D65 sRGB neutral lighting, no text, no logos, transparent or non-white plain background.",
      "acceptance": "Bag must match bag-board scale, strap thickness, pale neutral palette, and hardware details."
    }
  ]
}
```

- [ ] **Step 6: Run manifest tests and asset audit**

Run:

```bash
python3 -m unittest tests/test_asset_manifest_contract.py
python3 scripts/audit_assets.py
python3 scripts/audit_palette.py
git diff --check
```

Expected:

- Python tests pass.
- `asset audit: ok`
- `palette audit: ok (13 roles)`

Commit:

```bash
git add source/manifests/asset-manifest.json source/manifests/page-manifest.json source/manifests/generation-requests.json scripts/audit_assets.py tests/test_asset_manifest_contract.py
git commit -m "Add Akari asset acceptance manifests"
```

## Task 5: Deterministic Document Model

**Files:**

- Create: `tools/pdf/theme.mjs`
- Create: `tools/pdf/document.mjs`
- Create: `tools/pdf/render-html.mjs`
- Create: `tools/pdf/styles.css`
- Create: `tools/pdf/document.test.mjs`

- [ ] **Step 1: Write document model tests**

Create `tools/pdf/document.test.mjs`:

```javascript
import assert from "node:assert/strict";
import test from "node:test";
import { pages } from "./document.mjs";
import { theme } from "./theme.mjs";

test("document has exactly 12 numbered pages", () => {
  assert.equal(pages.length, 12);
  assert.deepEqual(
    pages.map((page) => page.page),
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
  );
});

test("all pages have source inputs and English titles", () => {
  for (const page of pages) {
    assert.ok(page.id);
    assert.ok(page.title);
    assert.ok(page.sourceInputs.length > 0);
    assert.equal(/[ぁ-んァ-ン一-龯]/.test(page.title), false);
  }
});

test("theme matches 16:9 preview contract", () => {
  assert.equal(theme.preview.width, 3840);
  assert.equal(theme.preview.height, 2160);
  assert.equal(theme.page.aspect, "16:9");
});
```

- [ ] **Step 2: Run Node tests to verify failure**

Run:

```bash
npm run test:node
```

Expected: FAIL because `document.mjs` and `theme.mjs` do not exist.

- [ ] **Step 3: Add theme constants**

Create `tools/pdf/theme.mjs`:

```javascript
export const theme = {
  page: {
    aspect: "16:9",
    widthIn: 13.333,
    heightIn: 7.5,
  },
  preview: {
    width: 3840,
    height: 2160,
    safeMargin: 160,
    minBodyPx: 30,
    minCaptionPx: 24,
  },
  fonts: {
    title: "Inter, Arial, sans-serif",
    body: "Inter, Arial, sans-serif",
  },
  colors: {
    page: "#F7F7F2",
    ink: "#242424",
    muted: "#6C6F73",
    rule: "#C9CDD2",
    accent: "#72C7D8",
    danger: "#C94A4A",
  },
};
```

- [ ] **Step 4: Add document page data**

Create `tools/pdf/document.mjs`:

```javascript
export const pages = [
  {
    page: 1,
    id: "cover-key-visual",
    title: "Akari v1.1",
    eyebrow: "Palette-Anchored Master Reference",
    sourceInputs: ["hoodie-front", "expression-sheet"],
    sections: [
      "D65 / sRGB target",
      "12-page production reference",
      "Identity anchored to expression sheet",
    ],
  },
  {
    page: 2,
    id: "d65-color-palette",
    title: "D65 Color Palette",
    eyebrow: "Source Of Truth",
    sourceInputs: ["hoodie-front", "expression-sheet", "bag-board", "shoe-board"],
    sections: ["Named roles", "Base / shadow / highlight ramps", "Audit tolerances"],
  },
  {
    page: 3,
    id: "character-summary-proportion",
    title: "Character Summary + Proportion",
    eyebrow: "Identity Lock",
    sourceInputs: ["hoodie-front", "base-front"],
    sections: ["Youthful anime proportion", "Short bob silhouette", "Oversized hoodie volume"],
  },
  {
    page: 4,
    id: "front-back",
    title: "Front / Back",
    eyebrow: "Production Turnaround",
    sourceInputs: ["hoodie-front", "hoodie-back"],
    sections: ["Matched scale", "Shared guide lines", "No mirrored shortcuts"],
  },
  {
    page: 5,
    id: "angle-turnaround",
    title: "Angle Turnaround",
    eyebrow: "Side And 45 Degree Views",
    sourceInputs: ["side-view", "hairpin-side-45", "non-hairpin-side-45"],
    sections: ["Hairpin-side label", "Non-hairpin-side label", "Hair and hoodie volume"],
  },
  {
    page: 6,
    id: "expressions",
    title: "Expressions",
    eyebrow: "Face / Hair Identity Master",
    sourceInputs: ["expression-sheet"],
    sections: ["Neutral", "Soft Smile", "Open Smile", "Laughing", "Surprised", "Anxious", "Pout", "Sleepy", "Wink"],
  },
  {
    page: 7,
    id: "hair-face-details",
    title: "Hair / Face Details",
    eyebrow: "No-Drift Rules",
    sourceInputs: ["expression-sheet", "hoodie-front", "hairpin-side-45", "side-view"],
    sections: ["Warm brown eyes", "Short bob volume", "Character-left hair pins"],
  },
  {
    page: 8,
    id: "outfit-rules",
    title: "Outfit Rules",
    eyebrow: "Layer And Silhouette Guide",
    sourceInputs: ["hoodie-front", "base-front", "hoodie-back"],
    sections: ["Oversized hoodie", "Gray pleated skirt", "Base outfit construction"],
  },
  {
    page: 9,
    id: "shoes-socks",
    title: "Shoes / Socks",
    eyebrow: "Footwear Detail Board",
    sourceInputs: ["footwear-board", "shoe-board", "hoodie-front"],
    sections: ["Two pale blue sock stripes", "Chunky white sneakers", "No logo-like marks"],
  },
  {
    page: 10,
    id: "bag-accessories",
    title: "Bag / Accessories",
    eyebrow: "Scale And Materials",
    sourceInputs: ["bag-board", "hoodie-front"],
    sections: ["Mini shoulder bag", "Pale neutral fabric", "Small metal accents"],
  },
  {
    page: 11,
    id: "do-dont",
    title: "Do / Don't",
    eyebrow: "Production Rules",
    sourceInputs: ["hoodie-front", "expression-sheet", "shoe-board", "bag-board"],
    sections: ["Preserve identity", "Avoid side flips", "Avoid color drift"],
  },
  {
    page: 12,
    id: "production-notes-source-manifest",
    title: "Production Notes / Source Manifest",
    eyebrow: "Traceability",
    sourceInputs: ["hoodie-front", "expression-sheet", "bag-board", "shoe-board"],
    sections: ["Version", "Palette", "Accepted assets", "Review notes"],
  },
];
```

- [ ] **Step 5: Add HTML renderer**

Create `tools/pdf/render-html.mjs`:

```javascript
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { pages } from "./document.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderPage(page) {
  const sourceItems = page.sourceInputs
    .map((input) => `<span class="source-chip">${escapeHtml(input)}</span>`)
    .join("");
  const sectionItems = page.sections
    .map((section) => `<li>${escapeHtml(section)}</li>`)
    .join("");
  return `
    <section class="sheet" data-page="${page.page}" id="${page.id}">
      <header class="page-header">
        <p>${escapeHtml(page.eyebrow)}</p>
        <h1>${escapeHtml(page.title)}</h1>
        <span>${String(page.page).padStart(2, "0")} / 12</span>
      </header>
      <main class="page-grid">
        <div class="visual-slot" data-source="${escapeHtml(page.sourceInputs[0])}">
          <img src="../../source/originals/${escapeHtml(sourceFilename(page.sourceInputs[0]))}" alt="${escapeHtml(page.sourceInputs[0])}">
        </div>
        <aside class="notes">
          <h2>Reference Notes</h2>
          <ul>${sectionItems}</ul>
          <div class="source-list">${sourceItems}</div>
        </aside>
      </main>
    </section>`;
}

function sourceFilename(assetId) {
  const filenames = {
    "hoodie-front": "v1_1_front_1.webp",
    "base-front": "v1_1_front_2.webp",
    "expression-sheet": "v1_1_front_3.webp",
    "hoodie-back": "v1_1_back.webp",
    "side-view": "v1_1_真横.webp",
    "hairpin-side-45": "v1_1_髪飾り側_45deg.webp",
    "non-hairpin-side-45": "v1_1_非髪飾り側45deg.webp",
    "footwear-board": "v1_1_standard_foot_set.webp",
    "shoe-board": "v1_1_shoes.webp",
    "bag-board": "v1_1_bag.webp",
  };
  return filenames[assetId];
}

export function renderHtml() {
  const css = readFileSync(resolve(root, "tools/pdf/styles.css"), "utf-8");
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Akari v1.1 Settings</title>
  <style>${css}</style>
</head>
<body>
${pages.map(renderPage).join("\n")}
</body>
</html>`;
}

export function writeHtml(target = resolve(root, "build/site/index.html")) {
  mkdirSync(dirname(target), { recursive: true });
  writeFileSync(target, renderHtml(), "utf-8");
  return target;
}
```

- [ ] **Step 6: Add first-pass CSS**

Create `tools/pdf/styles.css`:

```css
@page {
  size: 13.333in 7.5in;
  margin: 0;
}

:root {
  --page-width: 3840px;
  --page-height: 2160px;
  --page-padding: 160px;
  --header-height: 230px;
  --page-gap: 110px;
  --title-size: 122px;
  --eyebrow-size: 46px;
  --body-size: 34px;
  --caption-size: 28px;
  --small-size: 24px;
}

@media print {
  :root {
    --page-width: 13.333in;
    --page-height: 7.5in;
    --page-padding: 0.5in;
    --header-height: 0.8in;
    --page-gap: 0.35in;
    --title-size: 0.42in;
    --eyebrow-size: 0.16in;
    --body-size: 0.16in;
    --caption-size: 0.12in;
    --small-size: 0.1in;
  }
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  color: #242424;
  background: #f7f7f2;
  font-family: Inter, Arial, sans-serif;
}

.sheet {
  width: var(--page-width);
  height: var(--page-height);
  page-break-after: always;
  padding: var(--page-padding);
  background: #f7f7f2;
  overflow: hidden;
}

.page-header {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 30px 80px;
  align-items: end;
  min-height: var(--header-height);
  border-bottom: 1px solid #c9cdd2;
}

@media print {
  .page-header {
    gap: 0.1in 0.25in;
  }
}

.page-header p {
  grid-column: 1 / -1;
  margin: 0;
  color: #6c6f73;
  font-size: var(--eyebrow-size);
  text-transform: uppercase;
  letter-spacing: 0;
}

.page-header h1 {
  margin: 0;
  font-size: var(--title-size);
  line-height: 1;
  letter-spacing: 0;
}

.page-header span {
  color: #6c6f73;
  font-size: var(--eyebrow-size);
}

.page-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(860px, 0.65fr);
  gap: var(--page-gap);
  height: calc(var(--page-height) - (var(--page-padding) * 2) - var(--header-height) - 90px);
  padding-top: 90px;
}

@media print {
  .page-grid {
    grid-template-columns: minmax(0, 1.35fr) minmax(3in, 0.65fr);
    height: 5.6in;
    padding-top: 0.3in;
  }
}

.visual-slot {
  display: grid;
  place-items: center;
  min-width: 0;
  min-height: 0;
  border: 1px solid #c9cdd2;
  background: #ffffff;
}

.visual-slot img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.notes {
  display: flex;
  min-width: 0;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.2in;
}

.notes h2 {
  margin: 0;
  font-size: calc(var(--body-size) * 1.35);
  letter-spacing: 0;
}

.notes ul {
  margin: 0;
  padding-left: 1.4em;
  font-size: var(--body-size);
  line-height: 1.35;
}

.source-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

@media print {
  .source-list {
    gap: 0.08in;
  }
}

.source-chip {
  border: 1px solid #c9cdd2;
  padding: 12px 24px;
  font-size: var(--small-size);
  color: #6c6f73;
}

@media print {
  .source-chip {
    padding: 0.04in 0.08in;
  }
}
```

- [ ] **Step 7: Verify and commit**

Run:

```bash
npm run test:node
npm run lint:md
git diff --check
```

Expected:

- Node tests pass.
- Markdown lint reports 0 errors.
- No whitespace errors.

Commit:

```bash
git add tools/pdf/theme.mjs tools/pdf/document.mjs tools/pdf/render-html.mjs tools/pdf/styles.css tools/pdf/document.test.mjs
git commit -m "Add Akari PDF document model"
```

## Task 6: Preview And PDF Export Commands

**Files:**

- Create: `tools/pdf/render.mjs`
- Create: `scripts/render_page_previews.py`
- Create: `scripts/export_pdf.py`
- Modify: `tools/pdf/document.test.mjs`
- Generate: `build/page-previews/*.png`
- Generate: `dist/akari-v1.1-settings.pdf`

- [ ] **Step 1: Extend Node tests for renderer exports**

Append to `tools/pdf/document.test.mjs`:

```javascript
import { renderHtml } from "./render-html.mjs";

test("rendered HTML contains 12 sheets", () => {
  const html = renderHtml();
  const count = html.match(/class="sheet"/g)?.length ?? 0;
  assert.equal(count, 12);
  assert.match(html, /Akari v1\.1/);
  assert.match(html, /D65 Color Palette/);
});
```

- [ ] **Step 2: Run Node tests**

Run:

```bash
npm run test:node
```

Expected: PASS after Task 5, proving `renderHtml()` produces 12 sheets.

- [ ] **Step 3: Add Playwright renderer**

Create `tools/pdf/render.mjs`:

```javascript
import { mkdirSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { chromium } from "playwright";
import { pages } from "./document.mjs";
import { writeHtml } from "./render-html.mjs";
import { theme } from "./theme.mjs";

const root = resolve(new URL("../..", import.meta.url).pathname);

async function openDocument() {
  const htmlPath = writeHtml(resolve(root, "build/site/index.html"));
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  const page = await browser.newPage({
    viewport: {
      width: theme.preview.width,
      height: theme.preview.height,
    },
    deviceScaleFactor: 1,
  });
  await page.goto(pathToFileURL(htmlPath).href);
  await page.emulateMedia({ media: "screen" });
  return { browser, page };
}

export async function renderPreviews() {
  const targetDir = resolve(root, "build/page-previews");
  mkdirSync(targetDir, { recursive: true });
  const { browser, page } = await openDocument();
  try {
    for (const entry of pages) {
      const locator = page.locator(`.sheet[data-page="${entry.page}"]`);
      await locator.screenshot({
        path: resolve(targetDir, `${String(entry.page).padStart(2, "0")}-${entry.id}.png`),
      });
    }
  } finally {
    await browser.close();
  }
}

export async function exportPdf() {
  mkdirSync(resolve(root, "dist"), { recursive: true });
  const { browser, page } = await openDocument();
  try {
    await page.emulateMedia({ media: "print" });
    await page.pdf({
      path: resolve(root, "dist/akari-v1.1-settings.pdf"),
      width: `${theme.page.widthIn}in`,
      height: `${theme.page.heightIn}in`,
      printBackground: true,
      preferCSSPageSize: true,
      margin: { top: "0", right: "0", bottom: "0", left: "0" },
    });
  } finally {
    await browser.close();
  }
}

if (process.argv.includes("--previews")) {
  await renderPreviews();
  console.log("page previews rendered");
}

if (process.argv.includes("--pdf")) {
  await exportPdf();
  console.log("pdf exported");
}
```

- [ ] **Step 4: Add Python command wrappers**

Create `scripts/render_page_previews.py`:

```python
#!/usr/bin/env python3
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    subprocess.run(
        ["node", "tools/pdf/render.mjs", "--previews"],
        cwd=ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Create `scripts/export_pdf.py`:

```python
#!/usr/bin/env python3
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    subprocess.run(
        ["node", "tools/pdf/render.mjs", "--pdf"],
        cwd=ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Render previews and export PDF**

Run:

```bash
python3 scripts/render_page_previews.py
python3 scripts/export_pdf.py
identify -format '%f %wx%h\n' build/page-previews/*.png
pdfinfo dist/akari-v1.1-settings.pdf | sed -n '1,20p'
```

Expected:

- `page previews rendered`
- `pdf exported`
- 12 preview PNGs exist.
- Each preview is `3840x2160`.
- `pdfinfo` reports `Pages: 12`.

- [ ] **Step 6: Verify and commit**

Run:

```bash
npm run test:node
python3 scripts/render_page_previews.py
python3 scripts/export_pdf.py
git diff --check
```

Commit:

```bash
git add tools/pdf/render.mjs scripts/render_page_previews.py scripts/export_pdf.py tools/pdf/document.test.mjs package.json package-lock.json
git commit -m "Add Akari preview and PDF export"
```

## Task 7: PDF And Rendered-Page Audits

**Files:**

- Create: `scripts/audit_pdf.py`
- Create: `scripts/audit_alpha_edges.py`
- Create: `tests/test_pdf_contract.py`
- Generate: `build/pdf-rendered-pages/*.png`
- Generate: `dist/akari-v1.1-settings-pages/*.txt`

- [ ] **Step 1: Write PDF contract tests**

Create `tests/test_pdf_contract.py`:

```python
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "dist/akari-v1.1-settings.pdf"


class PdfContractTest(unittest.TestCase):
    def test_pdf_exists(self):
        self.assertTrue(PDF.exists())

    def test_pdf_has_12_pages(self):
        result = subprocess.run(
            ["pdfinfo", str(PDF)],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("Pages:           12", result.stdout)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test after Task 6**

Run:

```bash
python3 -m unittest tests/test_pdf_contract.py
```

Expected: PASS after Task 6 generated `dist/akari-v1.1-settings.pdf`.

- [ ] **Step 3: Add PDF audit script**

Create `scripts/audit_pdf.py`:

```python
#!/usr/bin/env python3
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RENDER_DIR = ROOT / "build/pdf-rendered-pages"
TEXT_DIR = ROOT / "dist/akari-v1.1-settings-pages"


def run(command: list[str]) -> str:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: audit_pdf.py dist/akari-v1.1-settings.pdf", file=sys.stderr)
        return 2

    pdf = ROOT / sys.argv[1]
    errors = []
    if not pdf.exists():
        print(f"missing PDF: {pdf}", file=sys.stderr)
        return 1

    subprocess.run(["qpdf", "--check", str(pdf)], check=True)
    info = run(["pdfinfo", str(pdf)])
    if "Pages:           12" not in info:
        errors.append("PDF must have 12 pages")

    size_match = re.search(r"Page size:\s+([0-9.]+) x ([0-9.]+) pts", info)
    if not size_match:
        errors.append("PDF page size not found")
    else:
        width = float(size_match.group(1))
        height = float(size_match.group(2))
        ratio = width / height
        if abs(ratio - (16 / 9)) > 0.01:
            errors.append(f"PDF aspect ratio is not 16:9: {ratio:.4f}")

    fonts = run(["pdffonts", str(pdf)])
    if "name" not in fonts.lower():
        errors.append("pdffonts did not report font table")

    if RENDER_DIR.exists():
        shutil.rmtree(RENDER_DIR)
    RENDER_DIR.mkdir(parents=True)
    subprocess.run(
        ["pdftoppm", "-png", "-r", "288", str(pdf), str(RENDER_DIR / "page")],
        check=True,
    )
    rendered = sorted(RENDER_DIR.glob("page-*.png"))
    if len(rendered) != 12:
        errors.append(f"expected 12 rendered pages, got {len(rendered)}")

    for png in rendered:
        dimensions = run(["identify", "-format", "%w %h", str(png)]).strip()
        if dimensions != "3840 2160":
            errors.append(f"bad rendered page size for {png.name}: {dimensions}")

    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    text_path = TEXT_DIR / "document.txt"
    subprocess.run(["pdftotext", str(pdf), str(text_path)], check=True)
    text = text_path.read_text(encoding="utf-8", errors="replace")
    for required in ["Akari v1.1", "D65 Color Palette", "Production Notes"]:
        if required not in text:
            errors.append(f"missing searchable text: {required}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("pdf audit: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Add alpha edge audit script**

Create `scripts/audit_alpha_edges.py`:

```python
#!/usr/bin/env python3
from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CHECK_DIRS = [
    ROOT / "build/assets/generated",
    ROOT / "build/assets/corrected",
]


def image_has_alpha(path: Path) -> bool:
    with Image.open(path) as image:
        return image.mode in {"LA", "RGBA"} or "transparency" in image.info


def main() -> int:
    checked = 0
    alpha_assets = 0
    for directory in CHECK_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.png")):
            checked += 1
            if image_has_alpha(path):
                alpha_assets += 1

    print(f"alpha edge audit: ok ({alpha_assets} transparent PNGs, {checked} PNGs checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run audits**

Run:

```bash
python3 scripts/audit_pdf.py dist/akari-v1.1-settings.pdf
python3 scripts/audit_alpha_edges.py
python3 -m unittest tests/test_pdf_contract.py
```

Expected:

- `pdf audit: ok`
- `alpha edge audit: ok (...)`
- Python tests pass.

Commit:

```bash
git add scripts/audit_pdf.py scripts/audit_alpha_edges.py tests/test_pdf_contract.py
git commit -m "Add Akari PDF audit scripts"
```

## Task 8: Page-Specific Layout Upgrade

**Files:**

- Modify: `tools/pdf/document.mjs`
- Modify: `tools/pdf/render-html.mjs`
- Modify: `tools/pdf/styles.css`
- Modify: `source/manifests/page-manifest.json`

- [ ] **Step 1: Upgrade page data to structured blocks**

Modify every page entry in `tools/pdf/document.mjs` to use this block schema:

```javascript
{
  page: 2,
  id: "d65-color-palette",
  title: "D65 Color Palette",
  eyebrow: "Source Of Truth",
  sourceInputs: ["hoodie-front", "expression-sheet", "bag-board", "shoe-board"],
  layout: "palette",
  blocks: [
    { type: "palette-grid", palettePath: "source/palette/akari-v1.1-palette.json" },
    { type: "note-list", title: "Usage", items: ["Use role names in prompts.", "Keep swatches deterministic.", "Audit shaded areas visually."] }
  ],
}
```

Use these page layouts:

- Page 1: `cover`
- Page 2: `palette`
- Page 3: `proportion`
- Page 4: `front-back`
- Page 5: `turnaround`
- Page 6: `expression-grid`
- Page 7: `detail-board`
- Page 8: `outfit-rules`
- Page 9: `shoes-socks`
- Page 10: `bag-accessories`
- Page 11: `do-dont`
- Page 12: `manifest`

- [ ] **Step 2: Run Node tests**

Run:

```bash
npm run test:node
```

Expected: FAIL if tests still expect `sections`; update tests in the next step.

- [ ] **Step 3: Update renderer and tests for blocks**

Modify `tools/pdf/render-html.mjs` so it renders:

- `image`: deterministic source image placement.
- `palette-grid`: swatches from `source/palette/akari-v1.1-palette.json`.
- `guide-lines`: named proportion guide rows.
- `expression-labels`: nine English labels from the spec.
- `note-list`: deterministic text notes.
- `manifest-summary`: version, palette, and accepted asset IDs.

Modify `tools/pdf/document.test.mjs` to assert:

```javascript
test("pages use supported block types", () => {
  const supported = new Set([
    "image",
    "palette-grid",
    "guide-lines",
    "expression-labels",
    "note-list",
    "manifest-summary",
  ]);
  for (const page of pages) {
    assert.ok(page.blocks.length > 0);
    for (const block of page.blocks) {
      assert.equal(supported.has(block.type), true, `${page.id} uses ${block.type}`);
    }
  }
});
```

- [ ] **Step 4: Update CSS for production pages**

Modify `tools/pdf/styles.css` with layout classes for the 12 page types. Keep:

- Safe margin at least `0.5in`.
- Body text at least `0.105in`.
- Caption/callout text at least `0.085in`.
- No negative letter spacing.
- Page sections unframed except individual repeated detail cards.

- [ ] **Step 5: Render and visually inspect**

Run:

```bash
npm run test:node
python3 scripts/render_page_previews.py
identify -format '%f %wx%h\n' build/page-previews/*.png
```

Expected:

- Node tests pass.
- 12 previews render at `3840x2160`.
- Visual inspection confirms no page is blank and no obvious text overlap exists.

Commit:

```bash
git add tools/pdf/document.mjs tools/pdf/render-html.mjs tools/pdf/styles.css tools/pdf/document.test.mjs source/manifests/page-manifest.json
git commit -m "Lay out Akari PDF pages"
```

## Task 9: Image Generation Intake For Missing Materials

**Files:**

- Modify: `source/manifests/generation-requests.json`
- Modify: `source/manifests/asset-manifest.json`
- Add: `build/assets/generated/*.png`
- Add: `build/assets/corrected/*.png`

- [ ] **Step 1: Use imagegen skill for queued assets**

For each `queued` request in `source/manifests/generation-requests.json`, use
the `imagegen` skill and the exact prompt recorded in the request.

Save results with these paths:

```text
build/assets/generated/cover-key-visual-16x9.webp
build/assets/generated/hair-face-detail-board.webp
build/assets/generated/bag-on-body-scale.webp
```

- [ ] **Step 2: Add generated assets to the manifest**

For each generated PNG, append an entry to `source/manifests/asset-manifest.json`
with status `needs_review`, `used_in_final_pdf: false`, the prompt from
`generation-requests.json`, and the generation identifier if available.

- [ ] **Step 3: Review generated assets against identity checklist**

Open generated images and compare against:

- `source/originals/v1_1_front_3.webp`
- `source/originals/v1_1_front_1.webp`
- `source/originals/v1_1_bag.webp`

Accept only assets that preserve:

- Brown short bob, not shoulder-length.
- Hair pins on Akari's character-left side.
- Warm brown eyes.
- White oversized hoodie and gray pleated skirt.
- Two pale blue sock stripes.
- Chunky white sneakers with pale blue accents.
- No logos or extra accessories.

- [ ] **Step 4: Promote accepted assets**

For every accepted generated asset:

- Change `status` to `accepted`.
- Set `used_in_final_pdf` to `true`.
- Add `accepted_reason`.
- Add `identity_check`, `color_check`, and `layout_check`.
- Update page data in `tools/pdf/document.mjs` to use the accepted generated
  image on its target page.

For rejected generated assets:

- Change `status` to `rejected`.
- Set `used_in_final_pdf` to `false`.
- Add `rejected_reason`.
- Do not use it outside Page 11, and only if clearly labeled rejected.

- [ ] **Step 5: Audit asset use**

Run:

```bash
python3 scripts/audit_assets.py
python3 scripts/render_page_previews.py
```

Expected:

- `asset audit: ok`
- 12 previews render.
- No `needs_review`, `needs_correction`, or `rejected` asset is used in a final
  production page.

Commit accepted and rejected records separately:

```bash
git add source/manifests/generation-requests.json source/manifests/asset-manifest.json tools/pdf/document.mjs build/assets/generated build/assets/corrected
git commit -m "Add reviewed Akari generated assets"
```

## Task 10: Final End-To-End Audit And Deliverables

**Files:**

- Generate: `build/page-previews/*.png`
- Generate: `build/pdf-rendered-pages/*.png`
- Generate: `dist/akari-v1.1-settings.pdf`
- Generate: `dist/akari-v1.1-settings-pages/document.txt`
- Modify as needed: layout, manifests, palette, or accepted assets.

- [ ] **Step 1: Run the full build**

Run:

```bash
npm run test:python
npm run test:node
npm run build:previews
npm run build:pdf
npm run audit
npm run lint:md
git diff --check
```

Expected:

- All Python tests pass.
- All Node tests pass.
- 12 page previews render.
- PDF exports.
- Asset, palette, PDF, and alpha audits pass.
- Markdown lint reports 0 errors.
- No whitespace errors.

- [ ] **Step 2: Inspect rendered previews**

Open these files side by side:

```text
build/page-previews/01-cover-key-visual.png
build/page-previews/02-d65-color-palette.png
build/page-previews/04-front-back.png
build/page-previews/05-angle-turnaround.png
build/page-previews/09-shoes-socks.png
build/page-previews/10-bag-accessories.png
build/pdf-rendered-pages/page-01.png
build/pdf-rendered-pages/page-12.png
```

Check:

- No page is blank.
- No text crosses the safe margin.
- No labels cover face, hair ornament, shoe details, or bag details.
- Page 2 palette swatches match `akari-v1.1-palette.json`.
- Page 4 and Page 5 views are not mirrored incorrectly.
- Dense board pages are readable at normal PDF viewing size.

- [ ] **Step 3: Fix audit failures one category at a time**

Use this order:

1. Broken build or missing files.
2. Manifest/source hash errors.
3. PDF page count, aspect ratio, or text search errors.
4. Layout overlap or unreadable pages.
5. Palette drift.
6. Generated asset identity drift.

After each fix, rerun the smallest failing command first, then rerun the full
command block from Step 1.

- [ ] **Step 4: Decide which binary artifacts to commit**

Commit:

- Source manifests.
- Palette file.
- Scripts and tests.
- Tooling files.
- Accepted generated/corrected assets used in the final PDF.
- Final PDF if it is reasonably sized and useful as the deliverable.

Do not commit:

- `node_modules/`
- `.venv/`
- Temporary `build/site/`
- Broken or rejected generated images unless they are intentionally used as
  labeled rejected examples on Page 11.

- [ ] **Step 5: Final commit**

Run:

```bash
git status --short
git add package.json package-lock.json requirements.txt scripts tests tools source dist build/assets/generated build/assets/corrected
git diff --cached --check
git commit -m "Build Akari v1.1 master PDF"
```

If `build/page-previews` and `build/pdf-rendered-pages` are committed for review,
add them explicitly:

```bash
git add build/page-previews build/pdf-rendered-pages
git commit -m "Add Akari PDF visual QA renders"
```

## Required Final Verification

Before claiming the PDF is complete, run:

```bash
python3 scripts/verify_environment.py
python3 scripts/prepare_sources.py
python3 -m unittest discover -s tests
npm run test:node
npm run build:previews
npm run build:pdf
python3 scripts/audit_assets.py
python3 scripts/audit_palette.py
python3 scripts/audit_pdf.py dist/akari-v1.1-settings.pdf
python3 scripts/audit_alpha_edges.py
npm run lint:md
git diff --check
```

The final report must include:

- PDF path: `dist/akari-v1.1-settings.pdf`
- Preview path: `build/page-previews/`
- PDF render-back path: `build/pdf-rendered-pages/`
- Exact final verification commands and outcomes.
- Any assets still marked `needs_review`, `rejected`, or `needs_correction`.

## Self-Review

Spec coverage:

- D65/sRGB palette: Task 3, Task 8, and final audit.
- Source hash traceability: Task 2 and Task 4.
- Generated asset acceptance: Task 4 and Task 9.
- 12-page 16:9 PDF: Task 5, Task 6, Task 7, Task 8, and Task 10.
- Searchable deterministic text: Task 5 through Task 7.
- Existing board relayout: Task 8.
- Image generation for missing materials: Task 9.
- White-background extraction risk: Task 7 alpha audit and Task 9 prompts.
- Production notes / source manifest page: Task 4, Task 5, and Task 8.

No deferred fields:

- The plan defines exact files, commands, manifest shapes, initial palette
  values, generation prompts, and expected verification output.
- Conditional regeneration is bounded by the manifest queue and acceptance
  checklist instead of being left open-ended.

Type and naming consistency:

- Asset IDs in `scripts/akari_assets.py`, `asset-manifest.json`,
  `page-manifest.json`, and `tools/pdf/document.mjs` use the same kebab-case IDs.
- Default command interfaces match the spec:
  `audit_assets.py`, `audit_palette.py`, `render_page_previews.py`,
  `export_pdf.py`, `audit_pdf.py`, and `audit_alpha_edges.py`.

AGENTS 3-lens review:

1. Minimality: The plan adds only one PDF pipeline, one manifest/audit layer, and
   one HTML/Playwright renderer. It avoids a frontend framework, database, or
   broad asset-management system.
2. Existing-pattern fit: The plan keeps repo paths from the spec, uses
   `.markdownlint.json`, uses the exact default command interfaces, and treats
   original root PNGs as immutable evidence.
3. Edge-case verification: The plan checks missing tools, source hash drift,
   unaccepted asset use, palette schema, 12-page PDF structure, 16:9 aspect,
   searchable text, render-back dimensions, alpha-edge presence, and manual
   preview inspection for overlap and orientation.
