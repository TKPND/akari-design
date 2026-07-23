# Akari v1.1 Situation Daybook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a separate 10-page 16:9 Akari v1.1 situation daybook PDF from the approved lakeside bench image plus reviewed scene candidates.

**Architecture:** Keep the existing settings PDF stable while adding a separate daybook document model, separate daybook manifests, and daybook-specific npm scripts. Reuse the existing PDF renderer, CSS theme, Playwright preview/PDF export path, and audit style, but parameterize renderer inputs so `settings` and `daybook` do not share page lists or output paths.

**Tech Stack:** Node ESM, Playwright/Chrome, Python 3 standard library, Pillow, ImageMagick `identify`, Poppler tools, qpdf, markdownlint-cli2, existing npm scripts.

---

## Current Context

- Approved spec:
  `docs/superpowers/specs/2026-06-30-akari-v1-1-situation-daybook-design.md`
- Approved anchor image attachment copied into:
  `source/originals/situation-daybook-lakeside-bench-cover.webp`
- Existing settings PDF output:
  `dist/akari-v1.1-settings.pdf`
- New daybook PDF output:
  `dist/akari-v1.1-situation-daybook.pdf`
- Existing renderer entrypoint:
  `tools/pdf/render.mjs`
- Existing settings document model:
  `tools/pdf/document.mjs`

## Target File Structure

```text
source/originals/situation-daybook-lakeside-bench-cover.webp
source/generated/situation-daybook/20260630_shade-break_v1.png
source/generated/situation-daybook/20260630_convenience-walk_v1.webp
source/generated/situation-daybook/20260630_riverside-path_v1.png
source/generated/situation-daybook/20260630_park-steps_v1.webp
source/generated/situation-daybook/20260630_window-seat_v1.webp
source/generated/situation-daybook/20260630_rain-cooled-street_v1.webp
source/generated/situation-daybook/20260630_station-after-sun_v1.webp
source/generated/situation-daybook/20260630_vending-machine-night_v1.webp
source/generated/situation-daybook/20260630_golden-hour-return_v1.webp
source/manifests/daybook/source-assets.json
source/manifests/daybook/asset-manifest.json
source/manifests/daybook/page-manifest.json
source/manifests/daybook/generation-requests.json
tools/pdf/daybook-document.mjs
tools/pdf/document.test.mjs
tools/pdf/daybook-document.test.mjs
tools/pdf/render-html.mjs
tools/pdf/render.mjs
tools/pdf/styles.css
scripts/render_daybook_previews.py
scripts/export_daybook_pdf.py
scripts/audit_daybook_pdf.py
tests/test_daybook_contract.py
package.json
build/daybook-site/index.html
build/daybook-page-previews/*.png
build/daybook-pdf-rendered-pages/*.png
dist/akari-v1.1-situation-daybook.pdf
dist/akari-v1.1-situation-daybook-pages/document.txt
```

## Task 1: Import The Approved Cover Anchor

**Files:**

- Create: `source/originals/situation-daybook-lakeside-bench-cover.webp`
- Test: `tests/test_daybook_contract.py`

- [ ] **Step 1: Write the failing cover import test**

Create `tests/test_daybook_contract.py`:

```python
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COVER = ROOT / "source/originals/situation-daybook-lakeside-bench-cover.webp"


class DaybookContractTest(unittest.TestCase):
    def test_cover_anchor_exists_with_expected_dimensions(self):
        self.assertTrue(COVER.is_file(), f"missing cover image: {COVER}")
        result = subprocess.run(
            ["identify", "-format", "%w %h %[colorspace]", str(COVER)],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual("1280 720 sRGB", result.stdout.strip())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run:

```bash
uv run python -m unittest tests.test_daybook_contract.DaybookContractTest.test_cover_anchor_exists_with_expected_dimensions
```

Expected: failure containing `missing cover image`.

- [ ] **Step 3: Copy the approved attachment into immutable source originals**

Run:

```bash
cp "<local-review-attachment>" \
  source/originals/situation-daybook-lakeside-bench-cover.webp
```

- [ ] **Step 4: Verify the cover import test passes**

Run:

```bash
uv run python -m unittest tests.test_daybook_contract.DaybookContractTest.test_cover_anchor_exists_with_expected_dimensions
```

Expected: `OK`.

- [ ] **Step 5: Commit the imported cover and test**

Run:

```bash
git add source/originals/situation-daybook-lakeside-bench-cover.webp tests/test_daybook_contract.py
git commit -m "Add situation daybook cover anchor"
```

## Task 2: Generate And Review Scene Candidates

**Files:**

- Create: `source/generated/situation-daybook/*.png`

This task is visual and must stop for user review before assets are marked
accepted in manifests. Every generated image must be illustration-only: no
captions, no titles, no readable signs, no logos, no watermarks, and no prompt
text in pixels.

- [ ] **Step 1: Generate `Shade Break`**

Save the accepted candidate to:

```text
source/generated/situation-daybook/20260630_shade-break_v1.png
```

Prompt:

```text
Akari v1.1 summer daybook scene, same identity as the approved lakeside bench cover: short warm-brown bob, warm brown eyes, gentle expression, simple loose white T-shirt, muted gray shorts or skirt, white crew socks with two pale blue stripes, chunky white and pale-blue sneakers, small pale shoulder bag, sitting on a shaded wooden bench near a calm lakeside path, clear summer daylight, leafy tree shadows, bottle in hand or resting nearby, relaxed everyday distance, wide 16:9 landscape composition with breathing room, complete connected limbs and shoes, no readable text, no captions, no logos, no watermark.
```

- [ ] **Step 2: Generate `Convenience Walk`**

Save the accepted candidate to:

```text
source/generated/situation-daybook/20260630_convenience-walk_v1.webp
```

Prompt:

```text
Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, walking back from a small convenience stop on a bright summer pavement path, carrying a plain drink bottle or simple unbranded small bag with no readable package text, pale blue accents in socks and sneakers, calm soft smile, natural daylight, quiet everyday atmosphere, wide 16:9 landscape composition, full body visible with complete feet and hands, no readable text, no store signs, no logos, no watermark.
```

- [ ] **Step 3: Generate `Riverside Path`**

Save the accepted candidate to:

```text
source/generated/situation-daybook/20260630_riverside-path_v1.png
```

Prompt:

```text
Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, pausing or slowly walking on a riverside path with water and railing in the background, blue sky, soft tree shade nearby, wide negative space on viewer-right for PDF layout, relaxed posture, small pale shoulder bag, white socks with two pale blue stripes, chunky white and pale-blue sneakers, complete connected limbs and shoes, no readable text, no signage, no logos, no watermark.
```

- [ ] **Step 4: Generate `Park Steps`**

Save the accepted candidate to:

```text
source/generated/situation-daybook/20260630_park-steps_v1.webp
```

Prompt:

```text
Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, sitting on low park steps or a low stone edge near greenery, calm midday shade, relaxed knees and grounded shoes, simple gray bottom, small pale shoulder bag, bottle nearby, natural shadow under feet, stable seated anatomy, complete connected limbs and shoes, wide 16:9 landscape composition, no readable text, no captions, no logos, no watermark.
```

- [ ] **Step 5: Generate `Window Seat`**

Save the accepted candidate to:

```text
source/generated/situation-daybook/20260630_window-seat_v1.webp
```

Prompt:

```text
Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, sitting by an indoor window in soft summer afternoon light, simple quiet room, pale blue accessory accents, small bag or bottle nearby, calm gentle expression, warm daylight crossing the white T-shirt, wide 16:9 landscape composition, clean readable silhouette, complete hands and visible lower body, no readable text, no posters, no logos, no watermark.
```

- [ ] **Step 6: Generate `Rain-Cooled Street`**

Save the accepted candidate to:

```text
source/generated/situation-daybook/20260630_rain-cooled-street_v1.webp
```

Prompt:

```text
Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, quiet street after summer rain, damp pavement reflections, optional thin light cardigan over the white T-shirt, small pale shoulder bag, calm face, soft overcast light breaking after rain, no umbrella text or shop text, no readable signs, full body or three-quarter body with complete hands and shoes, wide 16:9 landscape composition, no logos, no watermark.
```

- [ ] **Step 7: Generate `Station After Sun`**

Save the accepted candidate to:

```text
source/generated/situation-daybook/20260630_station-after-sun_v1.webp
```

Prompt:

```text
Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, late afternoon near a small quiet station or transit stop, warm rim light, simple thin outer layer allowed, no readable station name or timetable text, relaxed waiting posture, pale blue sock and sneaker accents, small pale shoulder bag, wide 16:9 landscape composition, complete connected limbs and shoes, no logos, no watermark.
```

- [ ] **Step 8: Generate `Vending Machine Night`**

Save the accepted candidate to:

```text
source/generated/situation-daybook/20260630_vending-machine-night_v1.webp
```

Prompt:

```text
Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, quiet evening near a softly glowing vending machine, cool practical light balanced with warm skin tones, vending machine details abstract and unreadable, no product labels, calm gentle expression, small pale shoulder bag, pale blue sock and sneaker accents, wide 16:9 landscape composition, complete hands and feet, no readable text, no logos, no watermark.
```

- [ ] **Step 9: Generate `Golden Hour Return`**

Save the accepted candidate to:

```text
source/generated/situation-daybook/20260630_golden-hour-return_v1.webp
```

Prompt:

```text
Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, walking home on a quiet path at golden hour, warm backlight, long soft shadows, simple gray bottom, small pale shoulder bag, bottle or small prop optional, calm expression, outfit silhouette readable against sunset light, wide 16:9 landscape composition, complete connected limbs and shoes, no readable text, no signage, no logos, no watermark.
```

- [ ] **Step 10: Verify all generated files are 16:9 sRGB/RGB**

Run:

```bash
identify -format "%f %w %h %[colorspace]\n" source/generated/situation-daybook/*.png
```

Expected: nine lines, each with a 16:9 width/height ratio and colorspace
`sRGB` or `RGB`.

- [ ] **Step 11: Create a contact sheet for user review**

Run:

```bash
mkdir -p tmp/daybook-review
montage -label "%t" -geometry 520x292+16+36 -tile 3x3 \
  source/generated/situation-daybook/*.png \
  tmp/daybook-review/daybook-scene-candidates.png
```

Open `tmp/daybook-review/daybook-scene-candidates.png` and ask the user to
accept, reject, or request regeneration for each scene. Do not continue until
the user accepts one candidate for every scene.

- [ ] **Step 12: Commit accepted scene image candidates**

Run:

```bash
git add source/generated/situation-daybook
git commit -m "Add accepted situation daybook scene candidates"
```

## Task 3: Add Daybook Manifests And Contract Tests

**Files:**

- Create: `source/manifests/daybook/source-assets.json`
- Create: `source/manifests/daybook/asset-manifest.json`
- Create: `source/manifests/daybook/page-manifest.json`
- Create: `source/manifests/daybook/generation-requests.json`
- Modify: `tests/test_daybook_contract.py`

- [ ] **Step 1: Extend the failing manifest contract test**

Replace `tests/test_daybook_contract.py` with:

```python
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DAYBOOK_MANIFEST_DIR = ROOT / "source/manifests/daybook"
COVER = ROOT / "source/originals/situation-daybook-lakeside-bench-cover.webp"
SOURCE_ASSETS = DAYBOOK_MANIFEST_DIR / "source-assets.json"
ASSET_MANIFEST = DAYBOOK_MANIFEST_DIR / "asset-manifest.json"
PAGE_MANIFEST = DAYBOOK_MANIFEST_DIR / "page-manifest.json"
GENERATION_REQUESTS = DAYBOOK_MANIFEST_DIR / "generation-requests.json"
JAPANESE_TEXT_RE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def identify(path: Path) -> tuple[int, int, str]:
    result = subprocess.run(
        ["identify", "-format", "%w %h %[colorspace]", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    width, height, colorspace = result.stdout.strip().split()
    return int(width), int(height), colorspace


class DaybookContractTest(unittest.TestCase):
    def test_cover_anchor_exists_with_expected_dimensions(self):
        self.assertTrue(COVER.is_file(), f"missing cover image: {COVER}")
        self.assertEqual((1280, 720, "sRGB"), identify(COVER))

    def test_daybook_manifests_exist(self):
        for path in [SOURCE_ASSETS, ASSET_MANIFEST, PAGE_MANIFEST, GENERATION_REQUESTS]:
            self.assertTrue(path.is_file(), f"missing manifest: {path}")

    def test_daybook_page_contract(self):
        manifest = load_json(PAGE_MANIFEST)
        self.assertEqual("akari-v1.1-situation-daybook", manifest["document_id"])
        self.assertEqual(10, manifest["page_count"])
        self.assertEqual(list(range(1, 11)), [page["page"] for page in manifest["pages"]])
        self.assertEqual("Lakeside Bench", manifest["pages"][0]["title"])
        for page in manifest["pages"]:
            self.assertEqual(False, bool(JAPANESE_TEXT_RE.search(page["title"])))
            self.assertEqual(1, len(page["source_inputs"]))
            self.assertEqual(
                ["image", "note-list", "note-list"],
                [block["type"] for block in page["blocks"]],
            )
            self.assertEqual(1, len(page["atmosphere_notes"]))
            self.assertEqual(3, len(page["generation_notes"]))

    def test_daybook_assets_are_accepted_and_16x9(self):
        asset_manifest = load_json(ASSET_MANIFEST)
        source_manifest = load_json(SOURCE_ASSETS)
        source_paths = {
            asset["id"]: ROOT / asset["source_path"]
            for asset in source_manifest["assets"]
        }
        self.assertEqual(10, len(asset_manifest["assets"]))
        for asset in asset_manifest["assets"]:
            self.assertEqual("accepted", asset["status"])
            self.assertEqual(True, asset["used_in_daybook_pdf"])
            path = source_paths.get(asset["id"])
            if path is None:
                path = ROOT / asset["candidate_path"]
            self.assertTrue(path.is_file(), f"missing image for {asset['id']}: {path}")
            width, height, colorspace = identify(path)
            self.assertEqual(width * 9, height * 16, asset["id"])
            self.assertIn(colorspace, {"sRGB", "RGB"})
            self.assertNotIn("readable text", asset["layout_check"].lower())

    def test_generation_prompts_ban_text_in_image(self):
        requests = load_json(GENERATION_REQUESTS)["requests"]
        self.assertEqual(9, len(requests))
        for request in requests:
            prompt = request["prompt"].lower()
            acceptance = request["acceptance"].lower()
            self.assertIn("no readable text", prompt)
            self.assertIn("no logos", prompt)
            self.assertIn("no watermark", prompt)
            self.assertIn("text-in-image", acceptance)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the manifest test and verify it fails**

Run:

```bash
uv run python -m unittest tests.test_daybook_contract
```

Expected: failure for missing `source/manifests/daybook/*.json`.

- [ ] **Step 3: Create `source-assets.json`**

Create `source/manifests/daybook/source-assets.json`:

```json
{
  "schema_version": 1,
  "asset_count": 1,
  "assets": [
    {
      "id": "situation-daybook-lakeside-bench-cover",
      "original_filename": "situation-daybook-lakeside-bench-cover.webp",
      "source_path": "source/originals/situation-daybook-lakeside-bench-cover.webp",
      "width": 1280,
      "height": 720,
      "colorspace": "sRGB",
      "role": "situation_daybook_cover_anchor",
      "orientation_state": "scene_unmirrored"
    }
  ]
}
```

- [ ] **Step 4: Create `generation-requests.json`**

Create `source/manifests/daybook/generation-requests.json` using the nine prompt
strings from Task 2 and this exact request schema:

```json
{
  "schema_version": 1,
  "requests": [
    {
      "id": "situation-daybook-shade-break",
      "status": "accepted",
      "target_page": 2,
      "aspect_ratio": "16:9",
      "prompt": "Akari v1.1 summer daybook scene, same identity as the approved lakeside bench cover: short warm-brown bob, warm brown eyes, gentle expression, simple loose white T-shirt, muted gray shorts or skirt, white crew socks with two pale blue stripes, chunky white and pale-blue sneakers, small pale shoulder bag, sitting on a shaded wooden bench near a calm lakeside path, clear summer daylight, leafy tree shadows, bottle in hand or resting nearby, relaxed everyday distance, wide 16:9 landscape composition with breathing room, complete connected limbs and shoes, no readable text, no captions, no logos, no watermark.",
      "acceptance": "Must pass Akari identity, complete limb continuity, 16:9 composition, and text-in-image review."
    },
    {
      "id": "situation-daybook-convenience-walk",
      "status": "accepted",
      "target_page": 3,
      "aspect_ratio": "16:9",
      "prompt": "Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, walking back from a small convenience stop on a bright summer pavement path, carrying a plain drink bottle or simple unbranded small bag with no readable package text, pale blue accents in socks and sneakers, calm soft smile, natural daylight, quiet everyday atmosphere, wide 16:9 landscape composition, full body visible with complete feet and hands, no readable text, no store signs, no logos, no watermark.",
      "acceptance": "Must pass Akari identity, complete limb continuity, 16:9 composition, and text-in-image review."
    },
    {
      "id": "situation-daybook-riverside-path",
      "status": "accepted",
      "target_page": 4,
      "aspect_ratio": "16:9",
      "prompt": "Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, pausing or slowly walking on a riverside path with water and railing in the background, blue sky, soft tree shade nearby, wide negative space on viewer-right for PDF layout, relaxed posture, small pale shoulder bag, white socks with two pale blue stripes, chunky white and pale-blue sneakers, complete connected limbs and shoes, no readable text, no signage, no logos, no watermark.",
      "acceptance": "Must pass Akari identity, complete limb continuity, 16:9 composition, and text-in-image review."
    },
    {
      "id": "situation-daybook-park-steps",
      "status": "accepted",
      "target_page": 5,
      "aspect_ratio": "16:9",
      "prompt": "Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, sitting on low park steps or a low stone edge near greenery, calm midday shade, relaxed knees and grounded shoes, simple gray bottom, small pale shoulder bag, bottle nearby, natural shadow under feet, stable seated anatomy, complete connected limbs and shoes, wide 16:9 landscape composition, no readable text, no captions, no logos, no watermark.",
      "acceptance": "Must pass Akari identity, complete limb continuity, 16:9 composition, and text-in-image review."
    },
    {
      "id": "situation-daybook-window-seat",
      "status": "accepted",
      "target_page": 6,
      "aspect_ratio": "16:9",
      "prompt": "Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, sitting by an indoor window in soft summer afternoon light, simple quiet room, pale blue accessory accents, small bag or bottle nearby, calm gentle expression, warm daylight crossing the white T-shirt, wide 16:9 landscape composition, clean readable silhouette, complete hands and visible lower body, no readable text, no posters, no logos, no watermark.",
      "acceptance": "Must pass Akari identity, complete limb continuity, 16:9 composition, and text-in-image review."
    },
    {
      "id": "situation-daybook-rain-cooled-street",
      "status": "accepted",
      "target_page": 7,
      "aspect_ratio": "16:9",
      "prompt": "Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, quiet street after summer rain, damp pavement reflections, optional thin light cardigan over the white T-shirt, small pale shoulder bag, calm face, soft overcast light breaking after rain, no umbrella text or shop text, no readable signs, full body or three-quarter body with complete hands and shoes, wide 16:9 landscape composition, no logos, no watermark.",
      "acceptance": "Must pass Akari identity, complete limb continuity, 16:9 composition, and text-in-image review."
    },
    {
      "id": "situation-daybook-station-after-sun",
      "status": "accepted",
      "target_page": 8,
      "aspect_ratio": "16:9",
      "prompt": "Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, late afternoon near a small quiet station or transit stop, warm rim light, simple thin outer layer allowed, no readable station name or timetable text, relaxed waiting posture, pale blue sock and sneaker accents, small pale shoulder bag, wide 16:9 landscape composition, complete connected limbs and shoes, no logos, no watermark.",
      "acceptance": "Must pass Akari identity, complete limb continuity, 16:9 composition, and text-in-image review."
    },
    {
      "id": "situation-daybook-vending-machine-night",
      "status": "accepted",
      "target_page": 9,
      "aspect_ratio": "16:9",
      "prompt": "Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, quiet evening near a softly glowing vending machine, cool practical light balanced with warm skin tones, vending machine details abstract and unreadable, no product labels, calm gentle expression, small pale shoulder bag, pale blue sock and sneaker accents, wide 16:9 landscape composition, complete hands and feet, no readable text, no logos, no watermark.",
      "acceptance": "Must pass Akari identity, complete limb continuity, 16:9 composition, and text-in-image review."
    },
    {
      "id": "situation-daybook-golden-hour-return",
      "status": "accepted",
      "target_page": 10,
      "aspect_ratio": "16:9",
      "prompt": "Akari v1.1 summer daybook scene, same identity and white T-shirt outfit anchor as the approved lakeside bench cover, walking home on a quiet path at golden hour, warm backlight, long soft shadows, simple gray bottom, small pale shoulder bag, bottle or small prop optional, calm expression, outfit silhouette readable against sunset light, wide 16:9 landscape composition, complete connected limbs and shoes, no readable text, no signage, no logos, no watermark.",
      "acceptance": "Must pass Akari identity, complete limb continuity, 16:9 composition, and text-in-image review."
    }
  ]
}
```

- [ ] **Step 5: Create `asset-manifest.json`**

Create `source/manifests/daybook/asset-manifest.json`:

```json
{
  "schema_version": 1,
  "document_id": "akari-v1.1-situation-daybook",
  "assets": [
    {
      "id": "situation-daybook-lakeside-bench-cover",
      "status": "accepted",
      "source_inputs": ["situation-daybook-lakeside-bench-cover"],
      "prompt_summary": "User-approved lakeside bench anchor image for the situation daybook.",
      "model_or_tool": "source_jpg",
      "seed_or_generation_id": "",
      "orientation_state": "scene_unmirrored",
      "identity_check": "user accepted as the visual mood standard",
      "color_check": "identify reports sRGB 1280x720 source",
      "layout_check": "16:9 cover scene with no intentional readable text",
      "reviewer": "user accepted candidate; Codex promoted asset",
      "accepted_reason": "User described this as today's winning image and approved it as cover.",
      "used_in_daybook_pdf": true
    }
  ]
}
```

Append nine generated asset objects after the cover object. Use this exact
object shape for each generated asset, changing only `id`, `source_inputs`,
`prompt_summary`, `seed_or_generation_id`, `orientation_state`,
`identity_check`, `color_check`, `layout_check`, `accepted_reason`,
`candidate_path`, and keeping `used_in_daybook_pdf` true:

```json
{
  "id": "situation-daybook-shade-break",
  "status": "accepted",
  "source_inputs": ["situation-daybook-lakeside-bench-cover"],
  "prompt_summary": "Generated shade-break summer bench scene for the situation daybook.",
  "model_or_tool": "image_generation",
  "seed_or_generation_id": "request:situation-daybook-shade-break",
  "orientation_state": "scene_unmirrored",
  "identity_check": "user accepted after visual review against the cover anchor",
  "color_check": "identify reports sRGB/RGB candidate",
  "layout_check": "16:9 scene with no intentional readable text and complete limb continuity",
  "reviewer": "user accepted candidate; Codex promoted asset",
  "accepted_reason": "Accepted as the Shade Break scene.",
  "candidate_path": "source/generated/situation-daybook/20260630_shade-break_v1.png",
  "used_in_daybook_pdf": true
}
```

- [ ] **Step 6: Create `page-manifest.json`**

Create `source/manifests/daybook/page-manifest.json`:

```json
{
  "schema_version": 1,
  "document_id": "akari-v1.1-situation-daybook",
  "page_count": 10,
  "pages": [
    {
      "page": 1,
      "id": "lakeside-bench",
      "title": "Lakeside Bench",
      "role": "cover",
      "layout": "daybook-cover",
      "source_inputs": ["situation-daybook-lakeside-bench-cover"],
      "atmosphere_notes": ["The approved summer anchor: calm water, tree shade, white T-shirt, and close everyday distance."],
      "generation_notes": ["Preserve the relaxed seated posture.", "Keep the image free of readable text.", "Use this page as the mood standard for the rest of the booklet."],
      "blocks": [{"type": "image"}, {"type": "note-list"}, {"type": "note-list"}]
    },
    {
      "page": 2,
      "id": "shade-break",
      "title": "Shade Break",
      "role": "scene",
      "layout": "daybook-scene",
      "source_inputs": ["situation-daybook-shade-break"],
      "atmosphere_notes": ["A nearby bench moment that keeps the cover image's quiet summer shade."],
      "generation_notes": ["Leaf shadows should stay soft and readable.", "Hands and bottle scale need visual review.", "Shoes and lower legs must remain connected and complete."],
      "blocks": [{"type": "image"}, {"type": "note-list"}, {"type": "note-list"}]
    },
    {
      "page": 3,
      "id": "convenience-walk",
      "title": "Convenience Walk",
      "role": "scene",
      "layout": "daybook-scene",
      "source_inputs": ["situation-daybook-convenience-walk"],
      "atmosphere_notes": ["A bright summer errand scene that keeps the outfit simple and unbranded."],
      "generation_notes": ["No readable package, sign, or store text.", "Use bright pavement without harsh overexposure.", "Keep the walking pose stable with visible feet."],
      "blocks": [{"type": "image"}, {"type": "note-list"}, {"type": "note-list"}]
    },
    {
      "page": 4,
      "id": "riverside-path",
      "title": "Riverside Path",
      "role": "scene",
      "layout": "daybook-scene",
      "source_inputs": ["situation-daybook-riverside-path"],
      "atmosphere_notes": ["A wider water-side composition with enough air around Akari for the page layout."],
      "generation_notes": ["Keep viewer-right breathing room.", "Use railing and path perspective gently.", "Do not crop hair, hands, or shoes."],
      "blocks": [{"type": "image"}, {"type": "note-list"}, {"type": "note-list"}]
    },
    {
      "page": 5,
      "id": "park-steps",
      "title": "Park Steps",
      "role": "scene",
      "layout": "daybook-scene",
      "source_inputs": ["situation-daybook-park-steps"],
      "atmosphere_notes": ["A seated park variation that tests grounded feet and relaxed knees."],
      "generation_notes": ["Review seated anatomy before acceptance.", "Ground both shoes with a clear shadow.", "Keep the gray bottom and white T-shirt readable."],
      "blocks": [{"type": "image"}, {"type": "note-list"}, {"type": "note-list"}]
    },
    {
      "page": 6,
      "id": "window-seat",
      "title": "Window Seat",
      "role": "scene",
      "layout": "daybook-scene",
      "source_inputs": ["situation-daybook-window-seat"],
      "atmosphere_notes": ["A quiet indoor summer page that changes light without changing the character core."],
      "generation_notes": ["Use soft side light from the window.", "Keep room props simple and text-free.", "White T-shirt remains the outfit anchor."],
      "blocks": [{"type": "image"}, {"type": "note-list"}, {"type": "note-list"}]
    },
    {
      "page": 7,
      "id": "rain-cooled-street",
      "title": "Rain-Cooled Street",
      "role": "scene",
      "layout": "daybook-scene",
      "source_inputs": ["situation-daybook-rain-cooled-street"],
      "atmosphere_notes": ["A damp summer street scene that cools the palette while staying gentle."],
      "generation_notes": ["Keep reflections subtle.", "Avoid readable umbrellas, shop signs, and posters.", "A thin cardigan is allowed only if the white T-shirt still leads."],
      "blocks": [{"type": "image"}, {"type": "note-list"}, {"type": "note-list"}]
    },
    {
      "page": 8,
      "id": "station-after-sun",
      "title": "Station After Sun",
      "role": "scene",
      "layout": "daybook-scene",
      "source_inputs": ["situation-daybook-station-after-sun"],
      "atmosphere_notes": ["A late-afternoon waiting scene with warm rim light and quiet transit context."],
      "generation_notes": ["No station-name or timetable text dependency.", "Keep the waiting pose relaxed.", "Use a thin outer layer only as a light variation."],
      "blocks": [{"type": "image"}, {"type": "note-list"}, {"type": "note-list"}]
    },
    {
      "page": 9,
      "id": "vending-machine-night",
      "title": "Vending Machine Night",
      "role": "scene",
      "layout": "daybook-scene",
      "source_inputs": ["situation-daybook-vending-machine-night"],
      "atmosphere_notes": ["A quiet night page that swaps sunlight for practical cool light."],
      "generation_notes": ["Vending details must remain unreadable.", "Balance cool light with warm skin tones.", "Do not let machine graphics compete with Akari."],
      "blocks": [{"type": "image"}, {"type": "note-list"}, {"type": "note-list"}]
    },
    {
      "page": 10,
      "id": "golden-hour-return",
      "title": "Golden Hour Return",
      "role": "scene",
      "layout": "daybook-scene",
      "source_inputs": ["situation-daybook-golden-hour-return"],
      "atmosphere_notes": ["A closing return-path scene with warm backlight and long shadows."],
      "generation_notes": ["Keep outfit silhouette readable against sunset.", "Use long shadows without hiding shoes.", "Maintain the same calm everyday distance as the cover."],
      "blocks": [{"type": "image"}, {"type": "note-list"}, {"type": "note-list"}]
    }
  ]
}
```

- [ ] **Step 7: Verify manifest tests pass**

Run:

```bash
uv run python -m unittest tests.test_daybook_contract
```

Expected: `OK`.

- [ ] **Step 8: Commit manifests and contract tests**

Run:

```bash
git add source/manifests/daybook tests/test_daybook_contract.py
git commit -m "Add situation daybook manifests"
```

## Task 4: Add The Daybook Document Model

**Files:**

- Create: `tools/pdf/daybook-document.mjs`
- Create: `tools/pdf/daybook-document.test.mjs`

- [ ] **Step 1: Write the failing daybook document test**

Create `tools/pdf/daybook-document.test.mjs`:

```javascript
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import test from "node:test";
import { daybookDocument, pages } from "./daybook-document.mjs";

test("daybook document has ten 16:9 scene pages", () => {
  assert.equal(daybookDocument.id, "akari-v1.1-situation-daybook");
  assert.equal(daybookDocument.title, "Akari v1.1 Situation Daybook");
  assert.equal(daybookDocument.outputPdf, "dist/akari-v1.1-situation-daybook.pdf");
  assert.equal(daybookDocument.previewDir, "build/daybook-page-previews");
  assert.equal(daybookDocument.siteHtml, "build/daybook-site/index.html");
  assert.equal(pages.length, 10);
  assert.deepEqual(
    pages.map(({ page, id, layout }) => [page, id, layout]),
    [
      [1, "lakeside-bench", "daybook-cover"],
      [2, "shade-break", "daybook-scene"],
      [3, "convenience-walk", "daybook-scene"],
      [4, "riverside-path", "daybook-scene"],
      [5, "park-steps", "daybook-scene"],
      [6, "window-seat", "daybook-scene"],
      [7, "rain-cooled-street", "daybook-scene"],
      [8, "station-after-sun", "daybook-scene"],
      [9, "vending-machine-night", "daybook-scene"],
      [10, "golden-hour-return", "daybook-scene"],
    ],
  );
});

test("daybook pages mirror the daybook page manifest", () => {
  const manifest = JSON.parse(
    readFileSync(resolve("source/manifests/daybook/page-manifest.json"), "utf-8"),
  );
  assert.deepEqual(
    pages.map(({ page, id, title, layout, sourceInputs, blocks }) => ({
      page,
      id,
      title,
      layout,
      source_inputs: sourceInputs,
      blocks: blocks.map((block) => ({ type: block.type })),
    })),
    manifest.pages.map(({ page, id, title, layout, source_inputs, blocks }) => ({
      page,
      id,
      title,
      layout,
      source_inputs,
      blocks,
    })),
  );
});

test("every daybook scene has native text notes", () => {
  for (const page of pages) {
    const noteBlocks = page.blocks.filter((block) => block.type === "note-list");
    assert.equal(noteBlocks.length, 2, page.id);
    assert.equal(noteBlocks[0].title, "Atmosphere");
    assert.equal(noteBlocks[0].items.length, 1, page.id);
    assert.equal(noteBlocks[1].title, "Generation Notes");
    assert.equal(noteBlocks[1].items.length, 3, page.id);
  }
});
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```bash
node --test tools/pdf/daybook-document.test.mjs
```

Expected: failure because `tools/pdf/daybook-document.mjs` does not exist.

- [ ] **Step 3: Implement `daybook-document.mjs`**

Create `tools/pdf/daybook-document.mjs`:

```javascript
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

function loadJson(relativePath) {
  return JSON.parse(readFileSync(resolve(relativePath), "utf-8"));
}

function imageBlock(source, label) {
  return {
    type: "image",
    images: [{ source, label }],
  };
}

function notes(title, items, variant = "plain") {
  return {
    type: "note-list",
    title,
    variant,
    items,
  };
}

function pageFromManifest(entry) {
  const [source] = entry.source_inputs;
  return {
    page: entry.page,
    id: entry.id,
    title: entry.title,
    eyebrow: entry.role === "cover" ? "Summer Daybook / Mood Standard" : "Summer Daybook / Light Notes",
    layout: entry.layout,
    sourceInputs: entry.source_inputs,
    blocks: [
      imageBlock(source, entry.title),
      notes("Atmosphere", entry.atmosphere_notes),
      notes("Generation Notes", entry.generation_notes, "cards"),
    ],
  };
}

const manifest = loadJson("source/manifests/daybook/page-manifest.json");

export const pages = manifest.pages.map(pageFromManifest);

export const daybookDocument = {
  id: "akari-v1.1-situation-daybook",
  title: "Akari v1.1 Situation Daybook",
  pages,
  sourceManifestPath: "source/manifests/daybook/source-assets.json",
  assetManifestPath: "source/manifests/daybook/asset-manifest.json",
  outputPdf: "dist/akari-v1.1-situation-daybook.pdf",
  previewDir: "build/daybook-page-previews",
  siteHtml: "build/daybook-site/index.html",
};
```

- [ ] **Step 4: Verify the document model passes**

Run:

```bash
node --test tools/pdf/daybook-document.test.mjs
```

Expected: all tests pass.

- [ ] **Step 5: Commit the daybook document model**

Run:

```bash
git add tools/pdf/daybook-document.mjs tools/pdf/daybook-document.test.mjs
git commit -m "Add situation daybook document model"
```

## Task 5: Parameterize HTML Rendering

**Files:**

- Modify: `tools/pdf/render-html.mjs`
- Modify: `tools/pdf/document.test.mjs`
- Modify: `tools/pdf/daybook-document.test.mjs`

- [ ] **Step 1: Add failing daybook render tests**

Append this test to `tools/pdf/daybook-document.test.mjs`:

```javascript
test("daybook renders PDF-native page text without changing settings render", async () => {
  const { renderHtml, sourceImagePath } = await import("./render-html.mjs");
  const html = renderHtml(daybookDocument);
  assert.match(html, /<title>Akari v1\.1 Situation Daybook<\/title>/);
  assert.match(html, /class="sheet layout-daybook-cover"/);
  assert.match(html, /Lakeside Bench/);
  assert.match(html, /Generation Notes/);
  assert.match(html, /no readable text/i);
  assert.equal(
    sourceImagePath("situation-daybook-lakeside-bench-cover", daybookDocument),
    "source/originals/situation-daybook-lakeside-bench-cover.webp",
  );
});
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```bash
node --test tools/pdf/daybook-document.test.mjs
```

Expected: failure because `renderHtml` and `sourceImagePath` still use settings
manifests only.

- [ ] **Step 3: Modify `render-html.mjs` imports**

Change the import line from:

```javascript
import { pages } from "./document.mjs";
```

to:

```javascript
import { pages as settingsPages } from "./document.mjs";
```

Then add this object after `const root = ...`:

```javascript
export const settingsDocument = {
  id: "akari-v1.1-settings",
  title: "Akari v1.1 Settings",
  pages: settingsPages,
  sourceManifestPath: "source/manifests/source-assets.json",
  assetManifestPath: "source/manifests/asset-manifest.json",
  outputPdf: "dist/akari-v1.1-settings.pdf",
  previewDir: "build/page-previews",
  siteHtml: "build/site/index.html",
};
```

- [ ] **Step 4: Modify source path resolution**

Replace `sourceImagePath` with:

```javascript
export function sourceImagePath(assetId, document = settingsDocument) {
  const sourceManifest = loadJson(document.sourceManifestPath);
  const assetManifest = loadJson(document.assetManifestPath);
  const paths = Object.fromEntries(
    sourceManifest.assets.map((asset) => [asset.id, asset.source_path]),
  );

  for (const asset of assetManifest.assets) {
    if (asset.model_or_tool === "image_generation" && asset.candidate_path) {
      paths[asset.id] = asset.candidate_path;
    }
  }

  if (!Object.hasOwn(paths, assetId)) {
    throw new Error(`Unknown source asset id: ${assetId}`);
  }
  return paths[assetId];
}
```

Change `sourceFilename` to:

```javascript
export function sourceFilename(assetId, document = settingsDocument) {
  return sourceImagePath(assetId, document).split("/").at(-1);
}
```

- [ ] **Step 5: Pass the document into image block rendering**

Change `renderImageBlock(block)` to `renderImageBlock(block, document)` and
change the `<img>` line to:

```javascript
<img src="../../${escapeHtml(sourceImagePath(source, document))}" alt="${escapeHtml(label)}">
```

Change `renderBlock(block, page)` to `renderBlock(block, page, document)` and
the `image` case to:

```javascript
return renderImageBlock(block, document);
```

Change `renderPage(page, totalPages)` to `renderPage(page, totalPages, document)`
and its block mapping to:

```javascript
const blockItems = page.blocks.map((block) => renderBlock(block, page, document)).join("");
```

- [ ] **Step 6: Parameterize `renderHtml` and `writeHtml`**

Replace `renderHtml` and `writeHtml` with:

```javascript
export function renderHtml(document = settingsDocument) {
  const css = readFileSync(resolve(root, "tools/pdf/styles.css"), "utf-8");
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escapeHtml(document.title)}</title>
  <style>${css}</style>
</head>
<body>
${document.pages.map((page) => renderPage(page, document.pages.length, document)).join("\n")}
</body>
</html>`;
}

export function writeHtml(target = resolve(root, settingsDocument.siteHtml), document = settingsDocument) {
  mkdirSync(dirname(target), { recursive: true });
  writeFileSync(target, renderHtml(document), "utf-8");
  return target;
}
```

- [ ] **Step 7: Run settings and daybook render tests**

Run:

```bash
node --test tools/pdf/document.test.mjs tools/pdf/daybook-document.test.mjs
```

Expected: all tests pass.

- [ ] **Step 8: Commit renderer parameterization**

Run:

```bash
git add tools/pdf/render-html.mjs tools/pdf/document.test.mjs tools/pdf/daybook-document.test.mjs
git commit -m "Parameterize PDF HTML rendering"
```

## Task 6: Add Daybook Layout CSS

**Files:**

- Modify: `tools/pdf/styles.css`
- Modify: `tools/pdf/daybook-document.test.mjs`

- [ ] **Step 1: Add failing layout fit test**

Append this test to `tools/pdf/daybook-document.test.mjs`:

```javascript
test("daybook images render inside visual slots", async (t) => {
  const { chromium } = await import("playwright");
  const { pathToFileURL } = await import("node:url");
  const { writeHtml } = await import("./render-html.mjs");
  const { theme } = await import("./theme.mjs");
  const target = writeHtml(undefined, daybookDocument);
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  t.after(async () => {
    await browser.close();
  });
  const page = await browser.newPage({
    viewport: { width: theme.preview.width, height: theme.preview.height },
  });
  await page.goto(pathToFileURL(target).href, { waitUntil: "domcontentloaded" });
  await page.evaluate(async () => {
    await Promise.all([...document.images].map((image) => {
      if (image.complete && image.naturalWidth > 0) {
        return undefined;
      }
      return new Promise((resolve, reject) => {
        image.addEventListener("load", resolve, { once: true });
        image.addEventListener("error", () => reject(new Error(`failed to load ${image.src}`)), { once: true });
      });
    }));
  });
  const issues = await page.evaluate(() => {
    return [...document.querySelectorAll(".layout-daybook-cover .visual-slot, .layout-daybook-scene .visual-slot")]
      .map((slot) => {
        const image = slot.querySelector("img");
        return getComputedStyle(image).objectFit === "contain" ? undefined : slot.dataset.source;
      })
      .filter(Boolean);
  });
  assert.deepEqual(issues, []);
});
```

- [ ] **Step 2: Run the focused test and verify it fails or exposes cramped layout**

Run:

```bash
node --test tools/pdf/daybook-document.test.mjs
```

Expected before CSS: the test may pass on object-fit but screenshots will use
generic layouts. Continue to add explicit daybook layout CSS so the page is
readable and stable.

- [ ] **Step 3: Add daybook CSS**

Append to `tools/pdf/styles.css`:

```css
.layout-daybook-cover .page-body,
.layout-daybook-scene .page-body {
  grid-template-columns: minmax(0, 2.6fr) minmax(760px, 0.8fr);
  align-items: stretch;
}

.layout-daybook-cover .block-image,
.layout-daybook-scene .block-image {
  display: grid;
  min-height: 0;
}

.layout-daybook-cover .image-card,
.layout-daybook-scene .image-card {
  min-height: 0;
}

.layout-daybook-cover .visual-slot,
.layout-daybook-scene .visual-slot {
  aspect-ratio: 16 / 9;
  min-height: 0;
  height: 100%;
}

.layout-daybook-cover .block-note-list,
.layout-daybook-scene .block-note-list {
  align-self: start;
}

.layout-daybook-cover .note-list-cards,
.layout-daybook-scene .note-list-cards {
  margin-top: var(--page-gap);
}
```

- [ ] **Step 4: Run node tests**

Run:

```bash
npm run test:node
```

Expected: all node tests pass.

- [ ] **Step 5: Commit daybook CSS**

Run:

```bash
git add tools/pdf/styles.css tools/pdf/daybook-document.test.mjs
git commit -m "Add situation daybook page layout"
```

## Task 7: Add Daybook Render Scripts

**Files:**

- Modify: `tools/pdf/render.mjs`
- Create: `scripts/render_daybook_previews.py`
- Create: `scripts/export_daybook_pdf.py`
- Modify: `tools/pdf/document.test.mjs`
- Modify: `tools/pdf/daybook-document.test.mjs`
- Modify: `package.json`

- [ ] **Step 1: Add failing renderer CLI tests**

Append this test to `tools/pdf/daybook-document.test.mjs`:

```javascript
test("renderer exposes settings and daybook documents", async () => {
  const renderer = await import("./render.mjs");
  assert.deepEqual(
    renderer.parseRenderArgs(["--document", "daybook", "--previews", "--pdf"]),
    { documentName: "daybook", commands: ["previews", "pdf"] },
  );
  assert.deepEqual(
    renderer.previewFilenames(daybookDocument),
    pages.map((page) => `${String(page.page).padStart(2, "0")}-${page.id}.png`),
  );
});
```

- [ ] **Step 2: Run the renderer tests and verify they fail**

Run:

```bash
node --test tools/pdf/daybook-document.test.mjs
```

Expected: failure because `parseRenderArgs` does not support `--document`.

- [ ] **Step 3: Update `render.mjs` imports and document selection**

Change imports to:

```javascript
import { pages as settingsPages } from "./document.mjs";
import { daybookDocument } from "./daybook-document.mjs";
import { settingsDocument, writeHtml } from "./render-html.mjs";
```

Add:

```javascript
const documents = {
  settings: { ...settingsDocument, pages: settingsPages },
  daybook: daybookDocument,
};
```

- [ ] **Step 4: Replace CLI parsing**

Replace `usage` with:

```javascript
const usage = "Usage: node tools/pdf/render.mjs [--document settings|daybook] [--previews] [--pdf]";
```

Replace `parseRenderArgs` with:

```javascript
export function parseRenderArgs(args) {
  const commands = [];
  let documentName = "settings";

  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === "--document") {
      const value = args[index + 1];
      if (!Object.hasOwn(documents, value)) {
        throw new Error(`Unknown document: ${value ?? ""}\n${usage}`);
      }
      documentName = value;
      index += 1;
      continue;
    }
    if (arg === "--previews") {
      commands.push("previews");
      continue;
    }
    if (arg === "--pdf") {
      commands.push("pdf");
      continue;
    }
    throw new Error(`Unknown option: ${arg}\n${usage}`);
  }

  if (commands.length === 0) {
    throw new Error(usage);
  }

  return { documentName, commands: [...new Set(commands)].sort((a, b) => {
    const order = { previews: 0, pdf: 1 };
    return order[a] - order[b];
  }) };
}
```

- [ ] **Step 5: Parameterize renderer functions**

Change `previewFilenames`, `openDocument`, `renderPreviews`, and `exportPdf`
signatures to accept a document:

```javascript
export function previewFilenames(document = documents.settings) {
  return document.pages.map((entry) => `${String(entry.page).padStart(2, "0")}-${entry.id}.png`);
}
```

In `openDocument(document)`, call:

```javascript
const htmlPath = writeHtml(resolve(root, document.siteHtml), document);
```

In `renderPreviews(document = documents.settings)`, set:

```javascript
const targetDir = resolve(root, document.previewDir);
```

and loop over `document.pages`.

In `exportPdf(document = documents.settings)`, set:

```javascript
path: resolve(root, document.outputPdf),
```

In `runCli`, use:

```javascript
export async function runCli(args = process.argv.slice(2)) {
  const { documentName, commands } = parseRenderArgs(args);
  const document = documents[documentName];
  for (const command of commands) {
    if (command === "previews") {
      await renderPreviews(document);
      console.log(`${documentName} page previews rendered`);
    }
    if (command === "pdf") {
      await exportPdf(document);
      console.log(`${documentName} pdf exported`);
    }
  }
}
```

- [ ] **Step 6: Create Python wrappers**

Create `scripts/render_daybook_previews.py`:

```python
#!/usr/bin/env python3
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    subprocess.run(
        ["node", "tools/pdf/render.mjs", "--document", "daybook", "--previews"],
        cwd=ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Create `scripts/export_daybook_pdf.py`:

```python
#!/usr/bin/env python3
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    subprocess.run(
        ["node", "tools/pdf/render.mjs", "--document", "daybook", "--pdf"],
        cwd=ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 7: Add npm scripts**

In `package.json`, add:

```json
"build:daybook:previews": "uv run python scripts/render_daybook_previews.py",
"build:daybook:pdf": "uv run python scripts/export_daybook_pdf.py",
```

- [ ] **Step 8: Run node tests**

Run:

```bash
npm run test:node
```

Expected: all node tests pass.

- [ ] **Step 9: Commit render scripts**

Run:

```bash
git add tools/pdf/render.mjs tools/pdf/document.test.mjs tools/pdf/daybook-document.test.mjs scripts/render_daybook_previews.py scripts/export_daybook_pdf.py package.json
git commit -m "Add situation daybook render scripts"
```

## Task 8: Add Daybook PDF Audit

**Files:**

- Create: `scripts/audit_daybook_pdf.py`
- Modify: `package.json`

- [ ] **Step 1: Create the daybook PDF audit script**

Create `scripts/audit_daybook_pdf.py`:

```python
#!/usr/bin/env python3
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RENDER_DIR = ROOT / "build/daybook-pdf-rendered-pages"
TEXT_DIR = ROOT / "dist/akari-v1.1-situation-daybook-pages"
TEXT_OUTPUT = TEXT_DIR / "document.txt"
EXPECTED_PAGE_COUNT = 10
EXPECTED_RENDER_SIZE = (3840, 2160)
CONTENT_SAMPLE_SIZE = (192, 108)
MIN_CONTENT_RATIO = 0.003
REQUIRED_TEXT = (
    "Akari v1.1 Situation Daybook",
    "Lakeside Bench",
    "Shade Break",
    "Convenience Walk",
    "Riverside Path",
    "Park Steps",
    "Window Seat",
    "Rain-Cooled Street",
    "Station After Sun",
    "Vending Machine Night",
    "Golden Hour Return",
    "Generation Notes",
    "no readable text",
)
PAGES_RE = re.compile(r"^Pages:\s+([0-9]+)\s*$", re.MULTILINE)
PAGE_SIZE_RE = re.compile(
    r"^Page size:\s+([0-9]+(?:\.[0-9]+)?) x ([0-9]+(?:\.[0-9]+)?) pts",
    re.MULTILINE,
)


class AuditError(Exception):
    pass


def project_path(path_arg: str) -> Path:
    path = Path(path_arg)
    if path.is_absolute():
        return path
    return ROOT / path


def run_command(command: list[str], label: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    except FileNotFoundError as error:
        raise AuditError(f"{label} failed: command not found: {command[0]}") from error
    except subprocess.CalledProcessError as error:
        details = "\n".join(
            part.strip()
            for part in (error.stdout, error.stderr)
            if part and part.strip()
        )
        raise AuditError(f"{label} failed:\n{details}" if details else f"{label} failed") from error


def clear_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def require_pdfinfo_contract(pdfinfo_output: str) -> None:
    pages_match = PAGES_RE.search(pdfinfo_output)
    if not pages_match:
        raise AuditError("pdfinfo must report page count")
    page_count = int(pages_match.group(1))
    if page_count != EXPECTED_PAGE_COUNT:
        raise AuditError(f"pdfinfo must report {EXPECTED_PAGE_COUNT} pages, got {page_count}")
    match = PAGE_SIZE_RE.search(pdfinfo_output)
    if not match:
        raise AuditError("pdfinfo must report page size in points")
    width = float(match.group(1))
    height = float(match.group(2))
    if height == 0 or abs((width / height) - (16 / 9)) > 0.001:
        raise AuditError(f"pdf pages must use 16:9 aspect ratio, got {width:g} x {height:g} pts")


def render_pages(pdf: Path) -> list[Path]:
    clear_directory(RENDER_DIR)
    prefix = RENDER_DIR / "page"
    run_command(["pdftoppm", "-png", "-r", "288", str(pdf), str(prefix)], "pdftoppm render")
    pages = sorted(RENDER_DIR.glob("page-*.png"))
    if len(pages) != EXPECTED_PAGE_COUNT:
        raise AuditError(f"expected {EXPECTED_PAGE_COUNT} rendered PNG pages, got {len(pages)}")
    return pages


def require_rendered_page_sizes(pages: list[Path]) -> None:
    for page in pages:
        with Image.open(page) as image:
            if image.size != EXPECTED_RENDER_SIZE:
                raise AuditError(f"{page.name} must be 3840x2160, got {image.size[0]}x{image.size[1]}")


def rendered_content_ratio(page: Path) -> float:
    with Image.open(page) as image:
        sample = image.convert("RGB").resize(CONTENT_SAMPLE_SIZE)
    background = sample.getpixel((0, 0))
    pixels = list(sample.getdata())
    changed = 0
    for pixel in pixels:
        if sum(abs(channel - base) for channel, base in zip(pixel, background)) > 24:
            changed += 1
    return changed / len(pixels)


def require_rendered_page_content(pages: list[Path]) -> None:
    for page in pages:
        ratio = rendered_content_ratio(page)
        if ratio < MIN_CONTENT_RATIO:
            raise AuditError(f"{page.name} appears blank or near-blank: content ratio {ratio:.4f}")


def require_font_table(pdffonts_output: str) -> None:
    lines = [line for line in pdffonts_output.splitlines() if line.strip()]
    if len(lines) < 3 or not lines[0].lower().startswith("name"):
        raise AuditError("pdffonts must report at least one font table row")


def extract_text(pdf: Path) -> str:
    clear_directory(TEXT_DIR)
    run_command(["pdftotext", str(pdf), str(TEXT_OUTPUT)], "pdftotext")
    return TEXT_OUTPUT.read_text(encoding="utf-8")


def normalize_searchable_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def require_searchable_text(text: str) -> None:
    normalized = normalize_searchable_text(text)
    missing = [term for term in REQUIRED_TEXT if normalize_searchable_text(term) not in normalized]
    if missing:
        raise AuditError(f"searchable text missing: {', '.join(missing)}")


def audit_pdf(pdf: Path) -> None:
    if not pdf.is_file():
        raise AuditError(f"PDF missing: {pdf}")
    run_command(["qpdf", "--check", str(pdf)], "qpdf check")
    require_pdfinfo_contract(run_command(["pdfinfo", str(pdf)], "pdfinfo").stdout)
    require_font_table(run_command(["pdffonts", str(pdf)], "pdffonts").stdout)
    pages = render_pages(pdf)
    require_rendered_page_sizes(pages)
    require_rendered_page_content(pages)
    require_searchable_text(extract_text(pdf))


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: audit_daybook_pdf.py dist/akari-v1.1-situation-daybook.pdf", file=sys.stderr)
        return 2
    try:
        audit_pdf(project_path(argv[1]))
    except AuditError as error:
        print(f"daybook pdf audit: failed: {error}", file=sys.stderr)
        return 1
    print("daybook pdf audit: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

- [ ] **Step 2: Add npm audit script**

In `package.json`, add:

```json
"audit:daybook:pdf": "uv run python scripts/audit_daybook_pdf.py dist/akari-v1.1-situation-daybook.pdf"
```

- [ ] **Step 3: Run python tests**

Run:

```bash
npm run test:python
```

Expected: all Python tests pass.

- [ ] **Step 4: Commit the daybook audit**

Run:

```bash
git add scripts/audit_daybook_pdf.py package.json
git commit -m "Add situation daybook PDF audit"
```

## Task 9: Build, Audit, And Commit The Daybook PDF

**Files:**

- Generated: `build/daybook-page-previews/*.png`
- Generated: `dist/akari-v1.1-situation-daybook.pdf`
- Generated: `dist/akari-v1.1-situation-daybook-pages/document.txt`

- [ ] **Step 1: Run the full verification suite**

Run:

```bash
npm run lint:md
npm run test:node
npm run test:python
```

Expected: all commands exit 0.

- [ ] **Step 2: Build daybook previews**

Run:

```bash
npm run build:daybook:previews
```

Expected output:

```text
daybook page previews rendered
```

Expected files:

```text
build/daybook-page-previews/01-lakeside-bench.png
build/daybook-page-previews/02-shade-break.png
build/daybook-page-previews/03-convenience-walk.png
build/daybook-page-previews/04-riverside-path.png
build/daybook-page-previews/05-park-steps.png
build/daybook-page-previews/06-window-seat.png
build/daybook-page-previews/07-rain-cooled-street.png
build/daybook-page-previews/08-station-after-sun.png
build/daybook-page-previews/09-vending-machine-night.png
build/daybook-page-previews/10-golden-hour-return.png
```

- [ ] **Step 3: Visually review previews**

Open the preview PNGs and verify:

- No generated image contains intentional readable text, titles, captions, logos,
  or watermarks.
- Notes are rendered as PDF text outside the image.
- Akari's limbs, shoes, hands, hair, bag, and bottle are not visually cut off or
  disconnected.
- The cover image remains the mood standard.

- [ ] **Step 4: Build the daybook PDF**

Run:

```bash
npm run build:daybook:pdf
```

Expected output:

```text
daybook pdf exported
```

Expected file:

```text
dist/akari-v1.1-situation-daybook.pdf
```

- [ ] **Step 5: Audit the daybook PDF**

Run:

```bash
npm run audit:daybook:pdf
```

Expected output:

```text
daybook pdf audit: ok
```

- [ ] **Step 6: Verify the settings PDF still builds**

Run:

```bash
npm run test:node
npm run build:pdf
npm run audit:pdf
```

Expected: node tests pass, settings PDF exports, and `pdf audit: ok`.

- [ ] **Step 7: Commit final daybook deliverables**

Run:

```bash
git add source/generated/situation-daybook source/manifests/daybook tools/pdf scripts tests package.json dist/akari-v1.1-situation-daybook.pdf dist/akari-v1.1-situation-daybook-pages
git commit -m "Build Akari situation daybook PDF"
```

Do not add `build/` outputs unless the user explicitly asks to preserve preview
PNGs in git.

## Self-Review

- Spec coverage: The plan imports the approved anchor, creates a separate
  10-page 16:9 daybook PDF, keeps generated images illustration-only, renders
  all titles and notes as PDF-native text, uses separate daybook manifests, and
  adds build/audit scripts without replacing the settings PDF.
- Scope: This plan intentionally builds the 10-page first pass. The optional
  11th generation notes page and 12th contact sheet are left for a later
  extension after the first booklet is visually accepted.
- Type consistency: The document object consistently uses `id`, `title`,
  `pages`, `sourceManifestPath`, `assetManifestPath`, `outputPdf`, `previewDir`,
  and `siteHtml`.
- Verification: The plan includes focused Python tests, focused Node tests,
  full `npm run test:node`, full `npm run test:python`, Markdown lint, daybook
  preview build, daybook PDF build, daybook PDF audit, and settings PDF
  regression audit.
