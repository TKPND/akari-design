# Akari v1.1 Tonari No Akari Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a separate A4 portrait PDF art book titled `となりのあかり` with about 24 generated Akari portrait pages.

**Architecture:** Add a Tonari No Akari document beside the existing settings PDF and situation daybook, sharing the renderer while giving Tonari its own manifests, portrait plate block, A4 page metrics, wrappers, and final audit. Keep candidate image review lightweight during generation, then run full document-level tests and PDF/OCR-style checks only after the selected 24-page draft exists.

**Tech Stack:** Node ESM, Playwright/Chrome, CSS print layout, Python 3 standard library, Pillow, ImageMagick `identify`, Poppler tools, qpdf, markdownlint-cli2, existing npm scripts.

---

## Current Context

- Approved spec:
  `docs/superpowers/specs/2026-07-01-akari-v1-1-tonari-no-akari-design.md`
- Existing renderer:
  `tools/pdf/render.mjs`
- Existing HTML renderer:
  `tools/pdf/render-html.mjs`
- Existing 16:9 settings document:
  `tools/pdf/document.mjs`
- Existing daybook document pattern:
  `tools/pdf/daybook-document.mjs`
- New document id:
  `akari-v1.1-tonari-no-akari`
- New PDF output:
  `dist/akari-v1.1-tonari-no-akari.pdf`

## Scope Check

This plan covers one subsystem: the Tonari No Akari art book. It includes the data model, rendering support, generation workflow, wrappers, final audit, and verification. It does not change the settings PDF or situation daybook content, except for shared renderer additions that are covered by regression tests.

## Page Catalogue

Use this exact 24-page catalogue for the first version. Titles and lines are PDF-native text; generated image pixels must not include text.

| Page | ID | Range | Title | Line | Output image |
| --- | --- | --- | --- | --- | --- |
| 1 | `morning-glance` | `いつもの距離` | `朝の合図` | `目が合うだけで、今日が少し近くなる。` | `source/generated/tonari-no-akari/20260701_morning-glance_v1.webp` |
| 2 | `window-breath` | `静かな余韻` | `窓辺の息` | `光の中で、言葉がゆっくりほどけていく。` | `source/generated/tonari-no-akari/20260701_window-breath_v1.webp` |
| 3 | `turn-back-smile` | `いつもの距離` | `ふりむき笑顔` | `呼ばれた気がして、少しだけ足を止めた。` | `source/generated/tonari-no-akari/20260701_turn-back-smile_v1.webp` |
| 4 | `near-eye-contact` | `少し甘め` | `近くのまなざし` | `照れた声より先に、まなざしが届く。` | `source/generated/tonari-no-akari/20260701_near-eye-contact_v1.webp` |
| 5 | `light-cardigan` | `服で魅せる` | `薄手の羽織り` | `いつもの服に、やわらかな風を重ねて。` | `source/generated/tonari-no-akari/20260701_light-cardigan_v1.webp` |
| 6 | `afternoon-stretch` | `元気な一瞬` | `背伸びの午後` | `伸ばした指先まで、夏の光が跳ねる。` | `source/generated/tonari-no-akari/20260701_afternoon-stretch_v1.webp` |
| 7 | `seated-distance` | `全身ポーズ` | `腰かける距離` | `隣に座る余白まで、ちゃんと残して。` | `source/generated/tonari-no-akari/20260701_seated-distance_v1.webp` |
| 8 | `shy-half-smile` | `少し甘め` | `照れ笑い` | `言いかけた言葉を、笑顔がそっと隠す。` | `source/generated/tonari-no-akari/20260701_shy-half-smile_v1.webp` |
| 9 | `roomwear-morning` | `服で魅せる` | `部屋着の朝` | `気を抜いた時間にも、あかりらしさがある。` | `source/generated/tonari-no-akari/20260701_roomwear-morning_v1.webp` |
| 10 | `walking-beside` | `いつもの距離` | `となりを歩く` | `歩幅がそろうと、景色までやさしくなる。` | `source/generated/tonari-no-akari/20260701_walking-beside_v1.webp` |
| 11 | `profile-light` | `静かな余韻` | `横顔の光` | `静けさの中で、輪郭だけが少し大人びる。` | `source/generated/tonari-no-akari/20260701_profile-light_v1.webp` |
| 12 | `small-peace` | `元気な一瞬` | `小さなピース` | `はしゃぎすぎない合図が、いちばん似合う。` | `source/generated/tonari-no-akari/20260701_small-peace_v1.webp` |
| 13 | `looking-up` | `少し甘め` | `見上げる距離` | `近すぎないのに、声だけはすぐそばにある。` | `source/generated/tonari-no-akari/20260701_looking-up_v1.webp` |
| 14 | `chair-pause` | `全身ポーズ` | `椅子の上で` | `足元まで自然に、ひと休みの形。` | `source/generated/tonari-no-akari/20260701_chair-pause_v1.webp` |
| 15 | `special-outing` | `服で魅せる` | `少しだけ特別` | `特別すぎない服で、いつもの道が変わる。` | `source/generated/tonari-no-akari/20260701_special-outing_v1.webp` |
| 16 | `small-run` | `元気な一瞬` | `小走りの影` | `振り返る前から、楽しそうな気配がする。` | `source/generated/tonari-no-akari/20260701_small-run_v1.webp` |
| 17 | `sleepy-afternoon` | `静かな余韻` | `眠たげな午後` | `まぶたの重さも、今日はやさしい表情になる。` | `source/generated/tonari-no-akari/20260701_sleepy-afternoon_v1.webp` |
| 18 | `almost-touching` | `少し甘め` | `指先の間` | `触れそうで触れないくらいが、ちょうどいい。` | `source/generated/tonari-no-akari/20260701_almost-touching_v1.webp` |
| 19 | `straight-stance` | `全身ポーズ` | `まっすぐ立つ` | `全身のバランスに、あかりの芯が見える。` | `source/generated/tonari-no-akari/20260701_straight-stance_v1.webp` |
| 20 | `crouching-gesture` | `全身ポーズ` | `しゃがむ仕草` | `何気ない姿勢ほど、らしさが出る。` | `source/generated/tonari-no-akari/20260701_crouching-gesture_v1.webp` |
| 21 | `evening-cardigan` | `静かな余韻` | `夕方の羽織り` | `一日の終わりに、少しだけ声がやわらぐ。` | `source/generated/tonari-no-akari/20260701_evening-cardigan_v1.webp` |
| 22 | `over-shoulder-voice` | `いつもの距離` | `肩越しの声` | `先に行きすぎないように、振り返ってくれる。` | `source/generated/tonari-no-akari/20260701_over-shoulder-voice_v1.webp` |
| 23 | `skirt-in-breeze` | `元気な一瞬` | `スカートの風` | `軽く揺れる裾に、元気な気配だけ残る。` | `source/generated/tonari-no-akari/20260701_skirt-in-breeze_v1.webp` |
| 24 | `homeward-smile` | `いつもの距離` | `帰り道の笑顔` | `また明日、と言う前の表情を残しておく。` | `source/generated/tonari-no-akari/20260701_homeward-smile_v1.webp` |

## Target File Structure

```text
source/references/tonari-no-akari/identity-face-hair.webp
source/references/tonari-no-akari/identity-body-base.webp
source/references/tonari-no-akari/identity-basic-outfit.webp
source/references/tonari-no-akari/identity-side-view.webp
source/manifests/tonari-no-akari/source-assets.json
source/manifests/tonari-no-akari/asset-manifest.json
source/manifests/tonari-no-akari/page-manifest.json
source/manifests/tonari-no-akari/generation-requests.json
source/generated/tonari-no-akari/*.png
tools/pdf/tonari-no-akari-document.mjs
tools/pdf/tonari-no-akari-document.test.mjs
tools/pdf/render-html.mjs
tools/pdf/render.mjs
tools/pdf/styles.css
scripts/render_tonari_no_akari_previews.py
scripts/export_tonari_no_akari_pdf.py
scripts/audit_tonari_no_akari_pdf.py
tests/test_tonari_no_akari_contract.py
tests/test_tonari_no_akari_pdf_audit.py
build/tonari-no-akari-site/index.html
build/tonari-no-akari-page-previews/*.png
build/tonari-no-akari-pdf-rendered-pages/*.png
dist/akari-v1.1-tonari-no-akari.pdf
dist/akari-v1.1-tonari-no-akari-pages/document.txt
```

## Task 1: Manifest And Reference Pack Contract

**Files:**

- Create: `tests/test_tonari_no_akari_contract.py`
- Create: `source/references/tonari-no-akari/identity-face-hair.webp`
- Create: `source/references/tonari-no-akari/identity-body-base.webp`
- Create: `source/references/tonari-no-akari/identity-basic-outfit.webp`
- Create: `source/references/tonari-no-akari/identity-side-view.webp`
- Create: `source/manifests/tonari-no-akari/source-assets.json`
- Create: `source/manifests/tonari-no-akari/page-manifest.json`
- Create: `source/manifests/tonari-no-akari/asset-manifest.json`
- Create: `source/manifests/tonari-no-akari/generation-requests.json`

- [ ] **Step 1: Write the failing Tonari manifest contract test**

Create `tests/test_tonari_no_akari_contract.py`:

```python
import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/tonari-no-akari"
REFERENCE_DIR = ROOT / "source/references/tonari-no-akari"
SOURCE_ASSETS = MANIFEST_DIR / "source-assets.json"
ASSET_MANIFEST = MANIFEST_DIR / "asset-manifest.json"
PAGE_MANIFEST = MANIFEST_DIR / "page-manifest.json"
GENERATION_REQUESTS = MANIFEST_DIR / "generation-requests.json"
DOCUMENT_ID = "akari-v1.1-tonari-no-akari"
JAPANESE_TEXT = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
EXPECTED_RANGES = {
    "いつもの距離",
    "少し甘め",
    "元気な一瞬",
    "静かな余韻",
    "服で魅せる",
    "全身ポーズ",
}
EXPECTED_REFERENCE_COPIES = {
    "identity-face-hair.webp": "source/originals/v1_1_front_3.webp",
    "identity-body-base.webp": "source/originals/v1_1_front_2.webp",
    "identity-basic-outfit.webp": "source/originals/v1_1_front_1.webp",
    "identity-side-view.webp": "source/originals/v1_1_真横.webp",
}
EXPECTED_PAGE_IDS = [
    "morning-glance",
    "window-breath",
    "turn-back-smile",
    "near-eye-contact",
    "light-cardigan",
    "afternoon-stretch",
    "seated-distance",
    "shy-half-smile",
    "roomwear-morning",
    "walking-beside",
    "profile-light",
    "small-peace",
    "looking-up",
    "chair-pause",
    "special-outing",
    "small-run",
    "sleepy-afternoon",
    "almost-touching",
    "straight-stance",
    "crouching-gesture",
    "evening-cardigan",
    "over-shoulder-voice",
    "skirt-in-breeze",
    "homeward-smile",
]


def load_json(path):
    with path.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class TonariNoAkariContractTest(unittest.TestCase):
    def test_tonari_manifests_exist(self):
        for manifest_path in (SOURCE_ASSETS, ASSET_MANIFEST, PAGE_MANIFEST, GENERATION_REQUESTS):
            with self.subTest(manifest=manifest_path.name):
                self.assertTrue(manifest_path.is_file(), f"missing manifest: {manifest_path}")

    def test_reference_pack_copies_minimum_identity_sources(self):
        source_assets = load_json(SOURCE_ASSETS)
        assets_by_filename = {
            Path(asset["source_path"]).name: asset for asset in source_assets["assets"]
        }

        for copy_name, original_relative_path in EXPECTED_REFERENCE_COPIES.items():
            with self.subTest(copy=copy_name):
                copied = REFERENCE_DIR / copy_name
                original = ROOT / original_relative_path
                self.assertTrue(copied.is_file(), f"missing reference copy: {copied}")
                self.assertTrue(original.is_file(), f"missing original source: {original}")
                self.assertEqual(sha256(original), sha256(copied))
                self.assertIn(copy_name, assets_by_filename)
                self.assertEqual(original_relative_path, assets_by_filename[copy_name]["original_source_path"])
                self.assertEqual(sha256(original), assets_by_filename[copy_name]["original_sha256"])

    def test_page_manifest_has_24_portrait_artwork_pages(self):
        page_manifest = load_json(PAGE_MANIFEST)
        self.assertEqual(DOCUMENT_ID, page_manifest["document_id"])
        self.assertEqual("となりのあかり", page_manifest["title"])
        self.assertEqual(24, page_manifest["page_count"])

        pages = page_manifest["pages"]
        self.assertEqual(list(range(1, 25)), [page["page"] for page in pages])
        self.assertEqual(EXPECTED_PAGE_IDS, [page["id"] for page in pages])

        for page in pages:
            with self.subTest(page=page["id"]):
                self.assertEqual("artwork", page["role"])
                self.assertEqual("tonari-portrait", page["layout"])
                self.assertIn(page["internal_range"], EXPECTED_RANGES)
                self.assertEqual(1, len(page["source_inputs"]))
                self.assertTrue(JAPANESE_TEXT.search(page["title"]), page["title"])
                self.assertTrue(JAPANESE_TEXT.search(page["display_line"]), page["display_line"])
                self.assertEqual([{"type": "portrait-plate"}], page["blocks"])
                self.assertNotIn("cover", page["role"])
                self.assertNotIn("chapter", page["role"])

    def test_asset_manifest_tracks_planned_final_images(self):
        asset_manifest = load_json(ASSET_MANIFEST)
        assets = asset_manifest["assets"]
        self.assertEqual(DOCUMENT_ID, asset_manifest["document_id"])
        self.assertEqual(24, len(assets))
        self.assertEqual(EXPECTED_PAGE_IDS, [asset["id"].removeprefix("tonari-") for asset in assets])

        for asset in assets:
            with self.subTest(asset=asset["id"]):
                self.assertIn(asset["status"], {"planned", "accepted"})
                self.assertEqual("image_generation", asset["model_or_tool"])
                self.assertTrue(asset["candidate_path"].startswith("source/generated/tonari-no-akari/"))
                self.assertTrue(asset["candidate_path"].endswith("_v1.png"))
                self.assertTrue(asset["used_in_tonari_pdf"])
                self.assertIn("no intentional readable text", asset["layout_check"].lower())

    def test_generation_requests_are_lightweight_until_final_pdf(self):
        generation_requests = load_json(GENERATION_REQUESTS)
        self.assertEqual(DOCUMENT_ID, generation_requests["document_id"])
        self.assertEqual(
            "final_pdf_only",
            generation_requests["audit_policy"]["heavy_pdf_or_ocr_audit"],
        )
        self.assertIn("identity", generation_requests["candidate_stage_checks"])
        self.assertIn("image-internal text", generation_requests["candidate_stage_checks"])

        requests = generation_requests["requests"]
        self.assertEqual(24, len(requests))
        self.assertEqual(EXPECTED_PAGE_IDS, [request["page_id"] for request in requests])
        for request in requests:
            with self.subTest(request=request["page_id"]):
                prompt = request["prompt"].lower()
                self.assertIn("no readable text", prompt)
                self.assertIn("no logos", prompt)
                self.assertIn("no watermark", prompt)
                self.assertNotIn("ocr each candidate", prompt)
                self.assertEqual(4, len(request["reference_pack_inputs"]))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused Python test and verify it fails**

Run:

```bash
npm run test:python -- tests.test_tonari_no_akari_contract
```

Expected: FAIL with missing Tonari manifest and reference files.

- [ ] **Step 3: Copy the minimum identity reference pack**

Run:

```bash
mkdir -p source/references/tonari-no-akari
cp source/originals/v1_1_front_3.webp source/references/tonari-no-akari/identity-face-hair.webp
cp source/originals/v1_1_front_2.webp source/references/tonari-no-akari/identity-body-base.webp
cp source/originals/v1_1_front_1.webp source/references/tonari-no-akari/identity-basic-outfit.webp
cp source/originals/v1_1_真横.webp source/references/tonari-no-akari/identity-side-view.webp
```

- [ ] **Step 4: Create the Tonari source manifest**

Create `source/manifests/tonari-no-akari/source-assets.json` with four assets copied from the source originals:

```json
{
  "schema_version": 1,
  "document_id": "akari-v1.1-tonari-no-akari",
  "reference_pack_version": "tonari-no-akari-identity-v1",
  "asset_count": 4,
  "assets": [
    {
      "id": "tonari-reference-face-hair",
      "original_source_id": "expression-sheet",
      "original_source_path": "source/originals/v1_1_front_3.webp",
      "original_sha256": "05cf3ca0fcbfd81d1e27b5e8e5b26eb25072c908d7b8ae75f4b4cb463e36e6db",
      "source_path": "source/references/tonari-no-akari/identity-face-hair.webp",
      "sha256": "05cf3ca0fcbfd81d1e27b5e8e5b26eb25072c908d7b8ae75f4b4cb463e36e6db",
      "width": 1254,
      "height": 1254,
      "colorspace": "sRGB",
      "role": "primary_face_hair_identity_anchor",
      "orientation_state": "expression_grid_unmirrored"
    },
    {
      "id": "tonari-reference-body-base",
      "original_source_id": "base-front",
      "original_source_path": "source/originals/v1_1_front_2.webp",
      "original_sha256": "302cf545880eb554f752b23da434cbff1563799f6e7311da5e14916b02c50434",
      "source_path": "source/references/tonari-no-akari/identity-body-base.webp",
      "sha256": "302cf545880eb554f752b23da434cbff1563799f6e7311da5e14916b02c50434",
      "width": 1024,
      "height": 1536,
      "colorspace": "sRGB",
      "role": "base_body_outfit_anchor",
      "orientation_state": "front_view_character_left_is_viewer_right"
    },
    {
      "id": "tonari-reference-basic-outfit",
      "original_source_id": "hoodie-front",
      "original_source_path": "source/originals/v1_1_front_1.webp",
      "original_sha256": "c22fe4aee39efd2282bf2bc7d858d31a0191707690629c323b3d454000104e59",
      "source_path": "source/references/tonari-no-akari/identity-basic-outfit.webp",
      "sha256": "c22fe4aee39efd2282bf2bc7d858d31a0191707690629c323b3d454000104e59",
      "width": 1024,
      "height": 1536,
      "colorspace": "sRGB",
      "role": "secondary_full_body_outfit_anchor",
      "orientation_state": "front_view_character_left_is_viewer_right"
    },
    {
      "id": "tonari-reference-side-view",
      "original_source_id": "side-view",
      "original_source_path": "source/originals/v1_1_真横.webp",
      "original_sha256": "ba73eff428f79b670b50b65fbc296f373f62a2689b17c7016527cd4a95385490",
      "source_path": "source/references/tonari-no-akari/identity-side-view.webp",
      "sha256": "ba73eff428f79b670b50b65fbc296f373f62a2689b17c7016527cd4a95385490",
      "width": 1055,
      "height": 1491,
      "colorspace": "sRGB",
      "role": "side_turnaround_anchor",
      "orientation_state": "side_view_unmirrored"
    }
  ]
}
```

- [ ] **Step 5: Create the page and asset manifests from the page catalogue**

Create `source/manifests/tonari-no-akari/page-manifest.json` with:

```json
{
  "schema_version": 1,
  "document_id": "akari-v1.1-tonari-no-akari",
  "title": "となりのあかり",
  "page_count": 24,
  "pages": [
    {
      "page": 1,
      "id": "morning-glance",
      "title": "朝の合図",
      "display_line": "目が合うだけで、今日が少し近くなる。",
      "role": "artwork",
      "layout": "tonari-portrait",
      "internal_range": "いつもの距離",
      "secondary_tags": ["close-expression", "everyday-distance"],
      "source_inputs": ["tonari-morning-glance"],
      "blocks": [{"type": "portrait-plate"}]
    }
  ]
}
```

Use the Page Catalogue as the complete source for every page object after `morning-glance`. Each page object must have role `artwork`, layout `tonari-portrait`, one `source_inputs` entry named `tonari-` plus the page id, and one block `{"type":"portrait-plate"}`. Do not add cover pages, chapter pages, or extra blocks.

Create `source/manifests/tonari-no-akari/asset-manifest.json` with 24 assets. The first asset is:

```json
{
  "id": "tonari-morning-glance",
  "status": "planned",
  "source_inputs": [
    "tonari-reference-face-hair",
    "tonari-reference-body-base",
    "tonari-reference-basic-outfit",
    "tonari-reference-side-view"
  ],
  "prompt_summary": "Close morning eye-contact portrait for the everyday-distance range.",
  "model_or_tool": "image_generation",
  "seed_or_generation_id": "request:tonari-morning-glance",
  "reference_pack_version": "tonari-no-akari-identity-v1",
  "orientation_state": "portrait_unmirrored",
  "identity_check": "planned; must preserve Akari face, hair, body impression, and overall identity",
  "color_check": "planned; generated image should remain sRGB/RGB",
  "layout_check": "planned A4 portrait page image with no intentional readable text, labels, logos, captions, or watermarks",
  "reviewer": "pending user and Codex visual review",
  "selection_reason": "planned opening page for close everyday presence",
  "candidate_path": "source/generated/tonari-no-akari/20260701_morning-glance_v1.webp",
  "used_in_tonari_pdf": true
}
```

Create the other 23 assets from the Page Catalogue with this exact mapping:

```text
tonari-window-breath -> request:tonari-window-breath -> source/generated/tonari-no-akari/20260701_window-breath_v1.webp -> quiet window-side portrait for the still-afterglow range
tonari-turn-back-smile -> request:tonari-turn-back-smile -> source/generated/tonari-no-akari/20260701_turn-back-smile_v1.webp -> over-shoulder smile for everyday distance
tonari-near-eye-contact -> request:tonari-near-eye-contact -> source/generated/tonari-no-akari/20260701_near-eye-contact_v1.webp -> close shy eye contact for the slightly sweet range
tonari-light-cardigan -> request:tonari-light-cardigan -> source/generated/tonari-no-akari/20260701_light-cardigan_v1.webp -> light cardigan clothing variation
tonari-afternoon-stretch -> request:tonari-afternoon-stretch -> source/generated/tonari-no-akari/20260701_afternoon-stretch_v1.webp -> lively stretch pose
tonari-seated-distance -> request:tonari-seated-distance -> source/generated/tonari-no-akari/20260701_seated-distance_v1.webp -> seated pose with adjacent space
tonari-shy-half-smile -> request:tonari-shy-half-smile -> source/generated/tonari-no-akari/20260701_shy-half-smile_v1.webp -> shy half-smile portrait
tonari-roomwear-morning -> request:tonari-roomwear-morning -> source/generated/tonari-no-akari/20260701_roomwear-morning_v1.webp -> tasteful roomwear morning clothing variation
tonari-walking-beside -> request:tonari-walking-beside -> source/generated/tonari-no-akari/20260701_walking-beside_v1.webp -> walking beside viewer feeling
tonari-profile-light -> request:tonari-profile-light -> source/generated/tonari-no-akari/20260701_profile-light_v1.webp -> quiet side-profile light portrait
tonari-small-peace -> request:tonari-small-peace -> source/generated/tonari-no-akari/20260701_small-peace_v1.webp -> small peace sign pose
tonari-looking-up -> request:tonari-looking-up -> source/generated/tonari-no-akari/20260701_looking-up_v1.webp -> close looking-up portrait
tonari-chair-pause -> request:tonari-chair-pause -> source/generated/tonari-no-akari/20260701_chair-pause_v1.webp -> seated chair full-body pose
tonari-special-outing -> request:tonari-special-outing -> source/generated/tonari-no-akari/20260701_special-outing_v1.webp -> slightly special outing clothes
tonari-small-run -> request:tonari-small-run -> source/generated/tonari-no-akari/20260701_small-run_v1.webp -> small run or quick-step pose
tonari-sleepy-afternoon -> request:tonari-sleepy-afternoon -> source/generated/tonari-no-akari/20260701_sleepy-afternoon_v1.webp -> sleepy quiet afternoon expression
tonari-almost-touching -> request:tonari-almost-touching -> source/generated/tonari-no-akari/20260701_almost-touching_v1.webp -> near-touching hands with tasteful restraint
tonari-straight-stance -> request:tonari-straight-stance -> source/generated/tonari-no-akari/20260701_straight-stance_v1.webp -> balanced full-body standing pose
tonari-crouching-gesture -> request:tonari-crouching-gesture -> source/generated/tonari-no-akari/20260701_crouching-gesture_v1.webp -> stable crouching or low pose
tonari-evening-cardigan -> request:tonari-evening-cardigan -> source/generated/tonari-no-akari/20260701_evening-cardigan_v1.webp -> evening cardigan quiet portrait
tonari-over-shoulder-voice -> request:tonari-over-shoulder-voice -> source/generated/tonari-no-akari/20260701_over-shoulder-voice_v1.webp -> shoulder-over glance calling back
tonari-skirt-in-breeze -> request:tonari-skirt-in-breeze -> source/generated/tonari-no-akari/20260701_skirt-in-breeze_v1.webp -> tasteful hem movement in breeze
tonari-homeward-smile -> request:tonari-homeward-smile -> source/generated/tonari-no-akari/20260701_homeward-smile_v1.webp -> closing homeward smile
```

For every mapped asset, use the same `source_inputs`, `model_or_tool`, `reference_pack_version`, `orientation_state`, `identity_check`, `color_check`, `layout_check`, `reviewer`, and `used_in_tonari_pdf` fields as the first asset. Keep `status` as `planned` until images pass visual review.

- [ ] **Step 6: Create the generation request manifest**

Create `source/manifests/tonari-no-akari/generation-requests.json` with:

```json
{
  "schema_version": 1,
  "document_id": "akari-v1.1-tonari-no-akari",
  "reference_pack_version": "tonari-no-akari-identity-v1",
  "candidate_stage_checks": [
    "identity",
    "anatomy",
    "tone",
    "image-internal text",
    "logos",
    "watermarks",
    "A4 portrait fit"
  ],
  "audit_policy": {
    "candidate_stage": "lightweight human review plus file existence and dimensions",
    "heavy_pdf_or_ocr_audit": "final_pdf_only"
  },
  "requests": [
    {
      "id": "request:tonari-morning-glance",
      "page_id": "morning-glance",
      "range": "いつもの距離",
      "target_path": "source/generated/tonari-no-akari/20260701_morning-glance_v1.webp",
      "reference_pack_inputs": [
        "source/references/tonari-no-akari/identity-face-hair.webp",
        "source/references/tonari-no-akari/identity-body-base.webp",
        "source/references/tonari-no-akari/identity-basic-outfit.webp",
        "source/references/tonari-no-akari/identity-side-view.webp"
      ],
      "prompt": "Akari v1.1 portrait art book page, preserve Akari identity from the reference pack: warm brown bob hair, warm brown eyes, gentle healthy presence, sturdy natural body proportion, everyday outfit direction with soft pale blue accents. A4 portrait composition, morning close eye-contact portrait, relaxed familiar distance, natural smile just before speaking, soft daylight, quiet background with no readable text, no signs, no labels, no logos, no watermark, complete natural hands and hair continuity.",
      "acceptance": "identity gate passes; image is portrait-oriented; no text-in-image; no logos; no watermark; healthy slightly sweet tone"
    }
  ]
}
```

Create requests for every Page Catalogue row after `morning-glance` using the same reference pack inputs, target paths from the Page Catalogue, and these prompt focuses:

```text
window-breath: quiet window-side half-body portrait, soft side light, thoughtful expression, no posters or written decor.
turn-back-smile: looking back over shoulder while walking, everyday smile, clear hair shape, no street signs or text.
near-eye-contact: close shy eye contact, gentle sweetness, relaxed shoulders, no text or symbols.
light-cardigan: light cardigan variation over everyday outfit, half-body portrait, calm breeze, no labels or logos.
afternoon-stretch: lively stretch pose with hands visible and connected, bright afternoon, no written background.
seated-distance: seated full-body or three-quarter pose with visible grounded feet, empty space beside her, no text.
shy-half-smile: half-smile with slight blush or shy warmth, upper-body portrait, no typographic decoration.
roomwear-morning: tasteful roomwear morning portrait, relaxed but healthy, simple room without posters or text.
walking-beside: full-body walking beside viewer feeling, natural stride, complete feet and hands, no signs.
profile-light: side-profile portrait in soft light, quiet mood, clean silhouette, no written objects.
small-peace: small peace sign, lively but not exaggerated, fingers correct, no text or logos.
looking-up: looking slightly upward from close everyday distance, sweet but tasteful, no labels.
chair-pause: seated on simple chair, full-body pose, natural feet and knees, no visible writing.
special-outing: slightly special outing clothes, portrait fit, not formal or flashy, no brand marks.
small-run: small run or quick step, playful motion, stable anatomy and complete shoes, no signs.
sleepy-afternoon: sleepy relaxed afternoon expression, gentle quiet pose, no written background.
almost-touching: hands near the frame or viewer-side space, touching is implied but not explicit, no text.
straight-stance: full-body standing pose, balanced body proportion, simple background without writing.
crouching-gesture: crouching or low pose, hands and feet stable, no text or logo details.
evening-cardigan: evening cardigan variation, warm low light, quiet expression, no signage.
over-shoulder-voice: shoulder-over glance as if calling back, everyday closeness, no text.
skirt-in-breeze: tasteful skirt or hem movement in breeze, lively posture, no exposure drift, no logos.
homeward-smile: warm homeward closing smile, everyday path or soft background, no signs or text.
```

- [ ] **Step 7: Run the focused Python test and verify it passes**

Run:

```bash
npm run test:python -- tests.test_tonari_no_akari_contract
```

Expected: PASS.

- [ ] **Step 8: Commit the manifest and reference pack scaffold**

Run:

```bash
git add tests/test_tonari_no_akari_contract.py source/references/tonari-no-akari source/manifests/tonari-no-akari
git commit -m "Add Tonari No Akari manifest scaffold"
```

## Task 2: Tonari Document Model And A4 Renderer Support

**Files:**

- Create: `tools/pdf/tonari-no-akari-document.mjs`
- Create: `tools/pdf/tonari-no-akari-document.test.mjs`
- Modify: `tools/pdf/render-html.mjs`
- Modify: `tools/pdf/render.mjs`
- Modify: `tools/pdf/styles.css`

- [ ] **Step 1: Write the failing Node document tests**

Create `tools/pdf/tonari-no-akari-document.test.mjs`:

```javascript
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import test from "node:test";
import { tonariNoAkariDocument, pages } from "./tonari-no-akari-document.mjs";

test("tonari document has 24 A4 portrait artwork pages", () => {
  assert.equal(tonariNoAkariDocument.id, "akari-v1.1-tonari-no-akari");
  assert.equal(tonariNoAkariDocument.title, "となりのあかり");
  assert.equal(tonariNoAkariDocument.outputPdf, "dist/akari-v1.1-tonari-no-akari.pdf");
  assert.equal(tonariNoAkariDocument.previewDir, "build/tonari-no-akari-page-previews");
  assert.equal(tonariNoAkariDocument.siteHtml, "build/tonari-no-akari-site/index.html");
  assert.deepEqual(tonariNoAkariDocument.pageSize, {
    widthIn: 8.27,
    heightIn: 11.69,
    previewWidth: 2480,
    previewHeight: 3508,
  });
  assert.equal(pages.length, 24);
  assert.deepEqual(
    pages.map(({ page, id, layout }) => [page, id, layout]),
    [
      [1, "morning-glance", "tonari-portrait"],
      [2, "window-breath", "tonari-portrait"],
      [3, "turn-back-smile", "tonari-portrait"],
      [4, "near-eye-contact", "tonari-portrait"],
      [5, "light-cardigan", "tonari-portrait"],
      [6, "afternoon-stretch", "tonari-portrait"],
      [7, "seated-distance", "tonari-portrait"],
      [8, "shy-half-smile", "tonari-portrait"],
      [9, "roomwear-morning", "tonari-portrait"],
      [10, "walking-beside", "tonari-portrait"],
      [11, "profile-light", "tonari-portrait"],
      [12, "small-peace", "tonari-portrait"],
      [13, "looking-up", "tonari-portrait"],
      [14, "chair-pause", "tonari-portrait"],
      [15, "special-outing", "tonari-portrait"],
      [16, "small-run", "tonari-portrait"],
      [17, "sleepy-afternoon", "tonari-portrait"],
      [18, "almost-touching", "tonari-portrait"],
      [19, "straight-stance", "tonari-portrait"],
      [20, "crouching-gesture", "tonari-portrait"],
      [21, "evening-cardigan", "tonari-portrait"],
      [22, "over-shoulder-voice", "tonari-portrait"],
      [23, "skirt-in-breeze", "tonari-portrait"],
      [24, "homeward-smile", "tonari-portrait"],
    ],
  );
});

test("tonari pages mirror the page manifest as portrait plates", () => {
  const manifest = JSON.parse(
    readFileSync(resolve("source/manifests/tonari-no-akari/page-manifest.json"), "utf-8"),
  );
  assert.deepEqual(
    pages.map(({ page, id, title, displayLine, layout, internalRange, sourceInputs, blocks }) => ({
      page,
      id,
      title,
      display_line: displayLine,
      layout,
      internal_range: internalRange,
      source_inputs: sourceInputs,
      blocks: blocks.map((block) => ({ type: block.type })),
    })),
    manifest.pages.map(({ page, id, title, display_line, layout, internal_range, source_inputs, blocks }) => ({
      page,
      id,
      title,
      display_line,
      layout,
      internal_range,
      source_inputs,
      blocks,
    })),
  );
});

test("tonari renders PDF-native Japanese portrait text", async () => {
  const { renderHtml, sourceImagePath } = await import("./render-html.mjs");
  const html = renderHtml(tonariNoAkariDocument);
  assert.match(html, /<title>となりのあかり<\/title>/);
  assert.match(html, /class="sheet layout-tonari-portrait"/);
  assert.match(html, /朝の合図/);
  assert.match(html, /目が合うだけで、今日が少し近くなる。/);
  assert.match(html, /@page\s*\{\s*size:\s*8\.27in 11\.69in;/);
  assert.equal(
    sourceImagePath("tonari-morning-glance", tonariNoAkariDocument),
    "source/generated/tonari-no-akari/20260701_morning-glance_v1.webp",
  );
});

test("renderer exposes the tonari document", async () => {
  const renderer = await import("./render.mjs");
  assert.deepEqual(
    renderer.parseRenderArgs(["--document", "tonari-no-akari", "--previews", "--pdf"]),
    { documentName: "tonari-no-akari", commands: ["previews", "pdf"] },
  );
  assert.deepEqual(
    renderer.previewFilenames(tonariNoAkariDocument).slice(0, 2),
    ["01-morning-glance.png", "02-window-breath.png"],
  );
});
```

- [ ] **Step 2: Run the focused Node test and verify it fails**

Run:

```bash
node --test tools/pdf/tonari-no-akari-document.test.mjs
```

Expected: FAIL because `tools/pdf/tonari-no-akari-document.mjs` does not exist yet.

- [ ] **Step 3: Add the Tonari document loader**

Create `tools/pdf/tonari-no-akari-document.mjs`:

```javascript
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const documentId = "akari-v1.1-tonari-no-akari";
const documentTitle = "となりのあかり";
const pageCount = 24;
const manifest = JSON.parse(
  readFileSync(resolve(root, "source/manifests/tonari-no-akari/page-manifest.json"), "utf-8"),
);

function validateManifest(sourceManifest) {
  if (sourceManifest.document_id !== documentId) {
    throw new Error(`Unexpected Tonari No Akari document id "${sourceManifest.document_id}"`);
  }
  if (sourceManifest.title !== documentTitle) {
    throw new Error(`Unexpected Tonari No Akari title "${sourceManifest.title}"`);
  }
  if (sourceManifest.page_count !== pageCount) {
    throw new Error(`Unexpected Tonari No Akari page count "${sourceManifest.page_count}"`);
  }
  if (!Array.isArray(sourceManifest.pages) || sourceManifest.pages.length !== pageCount) {
    throw new Error("Tonari No Akari page count must match manifest pages");
  }

  for (const entry of sourceManifest.pages) {
    if (entry.role !== "artwork") {
      throw new Error(`Tonari No Akari page "${entry.id}" must be an artwork page`);
    }
    if (entry.layout !== "tonari-portrait") {
      throw new Error(`Tonari No Akari page "${entry.id}" must use the portrait layout`);
    }
    if (!Array.isArray(entry.source_inputs) || entry.source_inputs.length !== 1) {
      throw new Error(`Tonari No Akari page "${entry.id}" must include exactly one source input`);
    }
    if (!entry.display_line) {
      throw new Error(`Tonari No Akari page "${entry.id}" must include a display line`);
    }
    if (!Array.isArray(entry.blocks) || entry.blocks.length !== 1 || entry.blocks[0].type !== "portrait-plate") {
      throw new Error(`Tonari No Akari page "${entry.id}" must include one portrait-plate block`);
    }
  }
}

function portraitPlateBlock(source, line) {
  return {
    type: "portrait-plate",
    source,
    line,
  };
}

validateManifest(manifest);

export const pages = manifest.pages.map((entry) => {
  const [source] = entry.source_inputs;
  return {
    page: entry.page,
    id: entry.id,
    title: entry.title,
    displayLine: entry.display_line,
    internalRange: entry.internal_range,
    eyebrow: documentTitle,
    layout: entry.layout,
    sourceInputs: entry.source_inputs,
    blocks: [portraitPlateBlock(source, entry.display_line)],
  };
});

export const tonariNoAkariDocument = {
  id: documentId,
  title: documentTitle,
  pages,
  sourceManifestPath: "source/manifests/tonari-no-akari/source-assets.json",
  assetManifestPath: "source/manifests/tonari-no-akari/asset-manifest.json",
  outputPdf: "dist/akari-v1.1-tonari-no-akari.pdf",
  previewDir: "build/tonari-no-akari-page-previews",
  siteHtml: "build/tonari-no-akari-site/index.html",
  pageSize: {
    widthIn: 8.27,
    heightIn: 11.69,
    previewWidth: 2480,
    previewHeight: 3508,
  },
};
```

- [ ] **Step 4: Add the portrait plate renderer and document page-size override**

Modify `tools/pdf/render-html.mjs`:

```javascript
function renderPortraitPlate(block, page, document) {
  const source = block.source ?? page.sourceInputs?.[0];
  const line = block.line ?? page.displayLine;
  if (!source) {
    throw new Error(`portrait-plate block on page "${page.id}" must include a source`);
  }
  if (!line) {
    throw new Error(`portrait-plate block on page "${page.id}" must include a line`);
  }

  return `
    <section class="${blockClass(block)}" data-block-type="portrait-plate">
      <figure class="portrait-plate">
        <div class="portrait-frame visual-slot" data-source="${escapeHtml(source)}">
          <img src="../../${escapeHtml(sourceImagePath(source, document))}" alt="${escapeHtml(page.title)}">
        </div>
        <figcaption class="portrait-caption">
          <strong>${escapeHtml(page.title)}</strong>
          <span>${escapeHtml(line)}</span>
        </figcaption>
      </figure>
    </section>`;
}

function renderDocumentCss(document) {
  if (!document.pageSize) {
    return "";
  }

  const { widthIn, heightIn, previewWidth, previewHeight } = document.pageSize;
  return `
@page {
  size: ${widthIn}in ${heightIn}in;
}

:root {
  --page-width: ${previewWidth}px;
  --page-height: ${previewHeight}px;
}

@media print {
  :root {
    --page-width: ${widthIn}in;
    --page-height: ${heightIn}in;
  }
}`;
}
```

Add `case "portrait-plate": return renderPortraitPlate(block, page, document);` to `renderBlock()`.

Change `renderHtml()` so the `<style>` tag appends `renderDocumentCss(document)` after the shared CSS:

```javascript
const documentCss = renderDocumentCss(document);
return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escapeHtml(document.title)}</title>
  <style>${css}${documentCss}</style>
</head>
<body>
${document.pages.map((page) => renderPage(page, document.pages.length, document)).join("\n")}
</body>
</html>`;
```

- [ ] **Step 5: Add Tonari to the renderer CLI and use document page metrics**

Modify `tools/pdf/render.mjs`:

```javascript
const documentLoaders = {
  settings: async () => settingsRenderDocument,
  daybook: async () => {
    const { daybookDocument } = await import("./daybook-document.mjs");
    return daybookDocument;
  },
  "tonari-no-akari": async () => {
    const { tonariNoAkariDocument } = await import("./tonari-no-akari-document.mjs");
    return tonariNoAkariDocument;
  },
};
const usage =
  "Usage: node tools/pdf/render.mjs [--document settings|daybook|tonari-no-akari] [--previews] [--pdf]";

function viewportFor(document) {
  return {
    width: document.pageSize?.previewWidth ?? theme.preview.width,
    height: document.pageSize?.previewHeight ?? theme.preview.height,
  };
}

function pdfSizeFor(document) {
  return {
    widthIn: document.pageSize?.widthIn ?? theme.page.widthIn,
    heightIn: document.pageSize?.heightIn ?? theme.page.heightIn,
  };
}
```

Use `viewportFor(document)` inside `openDocument()` and use `pdfSizeFor(document)` inside `exportPdf()`:

```javascript
const page = await browser.newPage({
  viewport: viewportFor(document),
  deviceScaleFactor: 1,
});
```

```javascript
const { widthIn, heightIn } = pdfSizeFor(document);
await page.pdf({
  path: pdfPath,
  width: `${widthIn}in`,
  height: `${heightIn}in`,
  printBackground: true,
  preferCSSPageSize: true,
  margin: { top: "0", right: "0", bottom: "0", left: "0" },
});
```

- [ ] **Step 6: Add Tonari portrait CSS**

Append to `tools/pdf/styles.css`:

```css
.layout-tonari-portrait {
  grid-template-rows: minmax(0, 1fr);
  gap: 0;
  padding: 180px 190px 150px;
}

.layout-tonari-portrait .page-header,
.layout-tonari-portrait .source-list {
  display: none;
}

.layout-tonari-portrait .page-body {
  display: grid;
  grid-template-rows: minmax(0, 1fr);
  gap: 0;
}

.block-portrait-plate,
.portrait-plate {
  display: grid;
  min-width: 0;
  min-height: 0;
}

.portrait-plate {
  grid-template-rows: minmax(0, 1fr) auto;
  gap: 44px;
  margin: 0;
}

.portrait-frame {
  border-radius: 0;
  box-shadow: none;
}

.portrait-caption {
  display: grid;
  gap: 16px;
  color: var(--color-ink);
  text-align: center;
}

.portrait-caption strong,
.portrait-caption span {
  display: block;
  letter-spacing: 0;
}

.portrait-caption strong {
  font-family: var(--font-title);
  font-size: 58px;
  font-weight: 700;
  line-height: 1.1;
}

.portrait-caption span {
  color: var(--color-muted);
  font-size: 31px;
  line-height: 1.45;
}

@media print {
  .layout-tonari-portrait {
    padding: 0.62in 0.66in 0.54in;
  }

  .portrait-plate {
    gap: 0.16in;
  }

  .portrait-caption {
    gap: 0.055in;
  }

  .portrait-caption strong {
    font-size: 0.2in;
  }

  .portrait-caption span {
    font-size: 0.108in;
  }
}
```

- [ ] **Step 7: Run focused Node tests**

Run:

```bash
node --test tools/pdf/tonari-no-akari-document.test.mjs
node --test tools/pdf/document.test.mjs tools/pdf/daybook-document.test.mjs
```

Expected: PASS. If image files do not exist yet, keep tests to HTML string assertions only in this task.

- [ ] **Step 8: Commit renderer support**

Run:

```bash
git add tools/pdf/tonari-no-akari-document.mjs tools/pdf/tonari-no-akari-document.test.mjs tools/pdf/render-html.mjs tools/pdf/render.mjs tools/pdf/styles.css
git commit -m "Add Tonari No Akari renderer support"
```

## Task 3: Build Wrappers And Package Scripts

**Files:**

- Create: `scripts/render_tonari_no_akari_previews.py`
- Create: `scripts/export_tonari_no_akari_pdf.py`
- Modify: `package.json`
- Modify: `tests/test_tonari_no_akari_contract.py`

- [ ] **Step 1: Extend the Python contract test for wrapper scripts**

Add this test to `tests/test_tonari_no_akari_contract.py`:

```python
    def test_package_scripts_expose_tonari_build_and_audit(self):
        package_json = load_json(ROOT / "package.json")
        scripts = package_json["scripts"]
        self.assertEqual(
            "uv run python scripts/render_tonari_no_akari_previews.py",
            scripts["build:tonari:previews"],
        )
        self.assertEqual(
            "uv run python scripts/export_tonari_no_akari_pdf.py",
            scripts["build:tonari:pdf"],
        )
        self.assertEqual(
            "uv run python scripts/audit_tonari_no_akari_pdf.py dist/akari-v1.1-tonari-no-akari.pdf",
            scripts["audit:tonari:pdf"],
        )
```

- [ ] **Step 2: Run the focused Python test and verify it fails**

Run:

```bash
npm run test:python -- tests.test_tonari_no_akari_contract.TonariNoAkariContractTest.test_package_scripts_expose_tonari_build_and_audit
```

Expected: FAIL because the scripts are not in `package.json`.

- [ ] **Step 3: Add wrapper scripts**

Create `scripts/render_tonari_no_akari_previews.py`:

```python
#!/usr/bin/env python3
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    subprocess.run(
        ["node", "tools/pdf/render.mjs", "--document", "tonari-no-akari", "--previews"],
        cwd=ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Create `scripts/export_tonari_no_akari_pdf.py`:

```python
#!/usr/bin/env python3
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    subprocess.run(
        ["node", "tools/pdf/render.mjs", "--document", "tonari-no-akari", "--pdf"],
        cwd=ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Add npm scripts**

Modify `package.json`:

```json
{
  "scripts": {
    "build:tonari:previews": "uv run python scripts/render_tonari_no_akari_previews.py",
    "build:tonari:pdf": "uv run python scripts/export_tonari_no_akari_pdf.py",
    "audit:tonari:pdf": "uv run python scripts/audit_tonari_no_akari_pdf.py dist/akari-v1.1-tonari-no-akari.pdf"
  }
}
```

Insert these keys beside the daybook build and audit scripts. Keep every existing script unchanged.

- [ ] **Step 5: Run script contract tests**

Run:

```bash
npm run test:python -- tests.test_tonari_no_akari_contract.TonariNoAkariContractTest.test_package_scripts_expose_tonari_build_and_audit
npm run test:node
```

Expected: PASS.

- [ ] **Step 6: Commit wrappers and scripts**

Run:

```bash
git add scripts/render_tonari_no_akari_previews.py scripts/export_tonari_no_akari_pdf.py package.json tests/test_tonari_no_akari_contract.py
git commit -m "Add Tonari No Akari build scripts"
```

## Task 4: Generate And Lightly Review The 24 Portrait Images

**Files:**

- Create: `source/generated/tonari-no-akari/*.png`
- Modify: `source/manifests/tonari-no-akari/asset-manifest.json`

This task is visual. Do not run full PDF/OCR audit after each image. For each accepted image, do only lightweight checks: visual identity/anatomy/tone/text review, file existence, `identify` dimensions/colorspace, and occasional preview generation when a layout risk is obvious.

- [ ] **Step 1: Generate range batch `いつもの距離`**

Generate these five pages from `generation-requests.json`:

```text
morning-glance
turn-back-smile
walking-beside
over-shoulder-voice
homeward-smile
```

For each accepted candidate, save to the exact target path, then run:

```bash
identify -format "%w %h %[colorspace]\n" source/generated/tonari-no-akari/20260701_morning-glance_v1.webp
```

Expected: portrait-oriented image, colorspace `sRGB` or `RGB`. Repeat the command with the matching target path for the other four images.

- [ ] **Step 2: Generate range batch `少し甘め`**

Generate these four pages:

```text
near-eye-contact
shy-half-smile
looking-up
almost-touching
```

Reject candidates with exposure drift, awkward intimacy, broken hands, or text-like marks. Save only accepted candidates to the target paths in the Page Catalogue.

- [ ] **Step 3: Generate range batch `元気な一瞬`**

Generate these four pages:

```text
afternoon-stretch
small-peace
small-run
skirt-in-breeze
```

Reject candidates with unstable fingers, disconnected limbs, unreadable action silhouettes, visible text, or logo-like marks.

- [ ] **Step 4: Generate range batch `静かな余韻`**

Generate these four pages:

```text
window-breath
profile-light
sleepy-afternoon
evening-cardigan
```

Reject candidates with accidental posters, signs, package text, or identity drift from the reference pack.

- [ ] **Step 5: Generate range batch `服で魅せる`**

Generate these three pages:

```text
light-cardigan
roomwear-morning
special-outing
```

Reject candidates with brand marks, excessive styling, or clothing that stops reading as Akari.

- [ ] **Step 6: Generate range batch `全身ポーズ`**

Generate these four pages:

```text
seated-distance
chair-pause
straight-stance
crouching-gesture
```

Reject candidates with weak full-body anatomy, broken feet, ungrounded seated poses, or crops that cannot work on A4 portrait pages.

- [ ] **Step 7: Promote accepted image entries in the asset manifest**

For every accepted image in `source/manifests/tonari-no-akari/asset-manifest.json`, change:

```json
{
  "status": "accepted",
  "identity_check": "passes visual review against tonari-no-akari-identity-v1 reference pack",
  "color_check": "identify reports sRGB/RGB portrait candidate",
  "layout_check": "A4 portrait candidate with no intentional readable text, labels, logos, captions, or watermarks",
  "reviewer": "user and Codex visual review",
  "selection_reason": "accepted for the final Tonari No Akari PDF page"
}
```

Keep each page-specific `prompt_summary`, `seed_or_generation_id`, and `candidate_path`.

- [ ] **Step 8: Run lightweight manifest and file checks**

Run:

```bash
npm run test:python -- tests.test_tonari_no_akari_contract
```

Expected: PASS. Do not run `npm run audit:tonari:pdf` yet.

- [ ] **Step 9: Commit selected images and manifest updates**

Run:

```bash
git add source/generated/tonari-no-akari source/manifests/tonari-no-akari/asset-manifest.json
git commit -m "Add Tonari No Akari selected portraits"
```

## Task 5: Final PDF Audit And Image-Backed Layout Tests

**Files:**

- Create: `scripts/audit_tonari_no_akari_pdf.py`
- Create: `tests/test_tonari_no_akari_pdf_audit.py`
- Modify: `tests/test_tonari_no_akari_contract.py`
- Modify: `tools/pdf/tonari-no-akari-document.test.mjs`

- [ ] **Step 1: Add final accepted image checks**

Add this test to `tests/test_tonari_no_akari_contract.py`:

```python
    def test_accepted_tonari_images_exist_and_are_portrait_or_square_safe(self):
        asset_manifest = load_json(ASSET_MANIFEST)
        for asset in asset_manifest["assets"]:
            with self.subTest(asset=asset["id"]):
                self.assertEqual("accepted", asset["status"])
                image_path = ROOT / asset["candidate_path"]
                self.assertTrue(image_path.is_file(), f"missing image: {image_path}")
```

This is intentionally only a final-stage test. Do not add OCR or PDF rendering here.

- [ ] **Step 2: Add final Playwright layout test**

Append to `tools/pdf/tonari-no-akari-document.test.mjs`:

```javascript
test("tonari portrait plates render image above title and line", async (t) => {
  const { chromium } = await import("playwright");
  const { pathToFileURL } = await import("node:url");
  const { writeHtml } = await import("./render-html.mjs");
  const target = writeHtml(undefined, tonariNoAkariDocument);
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  t.after(async () => {
    await browser.close();
  });

  const page = await browser.newPage({
    viewport: {
      width: tonariNoAkariDocument.pageSize.previewWidth,
      height: tonariNoAkariDocument.pageSize.previewHeight,
    },
  });
  await page.goto(pathToFileURL(target).href, { waitUntil: "domcontentloaded" });
  await page.evaluate(async () => {
    await Promise.all(
      [...document.images].map((image) => {
        if (image.complete && image.naturalWidth > 0) {
          return undefined;
        }
        return new Promise((resolve, reject) => {
          image.addEventListener("load", resolve, { once: true });
          image.addEventListener(
            "error",
            () => reject(new Error(`failed to load ${image.src}`)),
            { once: true },
          );
        });
      }),
    );
  });

  const issues = await page.evaluate(() => {
    return [...document.querySelectorAll(".layout-tonari-portrait")].flatMap((sheet) => {
      const image = sheet.querySelector(".portrait-frame img");
      const frame = sheet.querySelector(".portrait-frame");
      const caption = sheet.querySelector(".portrait-caption");
      const frameRect = frame.getBoundingClientRect();
      const captionRect = caption.getBoundingClientRect();
      const issueList = [];
      if (getComputedStyle(image).objectFit !== "contain") {
        issueList.push({ page: sheet.dataset.page, issue: "object-fit" });
      }
      if (captionRect.top <= frameRect.bottom) {
        issueList.push({ page: sheet.dataset.page, issue: "caption-overlap" });
      }
      if (!caption.querySelector("strong")?.textContent.trim()) {
        issueList.push({ page: sheet.dataset.page, issue: "missing-title" });
      }
      if (!caption.querySelector("span")?.textContent.trim()) {
        issueList.push({ page: sheet.dataset.page, issue: "missing-line" });
      }
      return issueList;
    });
  });
  assert.deepEqual(issues, []);
});
```

- [ ] **Step 3: Write audit unit tests before the audit script exists**

Create `tests/test_tonari_no_akari_pdf_audit.py`:

```python
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
AUDIT_SCRIPT = ROOT / "scripts/audit_tonari_no_akari_pdf.py"


def load_audit_script():
    spec = importlib.util.spec_from_file_location(
        "audit_tonari_no_akari_pdf", AUDIT_SCRIPT
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TonariNoAkariPdfAuditTest(unittest.TestCase):
    def setUp(self):
        self.audit = load_audit_script()

    def test_pdfinfo_contract_requires_24_a4_portrait_pages(self):
        good = "Pages:           24\nPage size:       595.44 x 841.68 pts (A4)\n"
        self.audit.require_pdfinfo_contract(good)

        with self.assertRaises(self.audit.AuditError):
            self.audit.require_pdfinfo_contract(
                "Pages:           10\nPage size:       960 x 540 pts\n"
            )

    def test_searchable_text_normalization_finds_japanese_titles(self):
        text = self.audit.normalize_searchable_text("となりのあかり\n朝の合図\n帰り道の笑顔")
        self.assertIn("朝の合図", text)
        self.assertIn("帰り道の笑顔", text)


if __name__ == "__main__":
    unittest.main()
```

Run:

```bash
npm run test:python -- tests.test_tonari_no_akari_pdf_audit
```

Expected: FAIL because `scripts/audit_tonari_no_akari_pdf.py` does not exist yet.

- [ ] **Step 4: Add the Tonari PDF audit script**

Create `scripts/audit_tonari_no_akari_pdf.py` by adapting `scripts/audit_daybook_pdf.py` with these Tonari constants:

```python
RENDER_DIR = ROOT / "build/tonari-no-akari-pdf-rendered-pages"
TEXT_DIR = ROOT / "dist/akari-v1.1-tonari-no-akari-pages"
TEXT_OUTPUT = TEXT_DIR / "document.txt"
EXPECTED_PAGE_COUNT = 24
EXPECTED_RENDER_SIZE = (2480, 3508)
CONTENT_SAMPLE_SIZE = (124, 176)
MIN_CONTENT_RATIO = 0.003
REQUIRED_TEXT = (
    "となりのあかり",
    "朝の合図",
    "窓辺の息",
    "ふりむき笑顔",
    "近くのまなざし",
    "薄手の羽織り",
    "背伸びの午後",
    "腰かける距離",
    "照れ笑い",
    "部屋着の朝",
    "となりを歩く",
    "横顔の光",
    "小さなピース",
    "見上げる距離",
    "椅子の上で",
    "少しだけ特別",
    "小走りの影",
    "眠たげな午後",
    "指先の間",
    "まっすぐ立つ",
    "しゃがむ仕草",
    "夕方の羽織り",
    "肩越しの声",
    "スカートの風",
    "帰り道の笑顔",
)
```

Use this A4 contract in `require_pdfinfo_contract()`:

```python
width = float(match.group(1))
height = float(match.group(2))
if height <= width or abs((width / height) - (595.44 / 841.68)) > 0.01:
    raise AuditError(
        f"pdf pages must use A4 portrait aspect ratio, got {width:g} x {height:g} pts"
    )
```

The `main()` usage string must be:

```python
"usage: audit_tonari_no_akari_pdf.py dist/akari-v1.1-tonari-no-akari.pdf"
```

The success line must be:

```python
print("tonari no akari pdf audit: ok")
```

- [ ] **Step 5: Run final-stage focused tests**

Run:

```bash
npm run test:python -- tests.test_tonari_no_akari_contract tests.test_tonari_no_akari_pdf_audit
node --test tools/pdf/tonari-no-akari-document.test.mjs
```

Expected: PASS.

- [ ] **Step 6: Commit final audit support**

Run:

```bash
git add scripts/audit_tonari_no_akari_pdf.py tests/test_tonari_no_akari_pdf_audit.py tests/test_tonari_no_akari_contract.py tools/pdf/tonari-no-akari-document.test.mjs
git commit -m "Add Tonari No Akari final audit"
```

## Task 6: Build, Audit, And Finalize The Art Book

**Files:**

- Create: `build/tonari-no-akari-page-previews/*.png`
- Create: `build/tonari-no-akari-site/index.html`
- Create: `build/tonari-no-akari-pdf-rendered-pages/*.png`
- Create: `dist/akari-v1.1-tonari-no-akari.pdf`
- Create: `dist/akari-v1.1-tonari-no-akari-pages/document.txt`
- Modify: generated outputs only if final visual review requires replacing selected images.

- [ ] **Step 1: Build Tonari page previews**

Run:

```bash
npm run build:tonari:previews
```

Expected: `build/tonari-no-akari-page-previews/` contains `01-morning-glance.png` through `24-homeward-smile.png`.

- [ ] **Step 2: Visually review preview contact points**

Open representative previews:

```bash
ls build/tonari-no-akari-page-previews
```

Review at least pages 1, 4, 7, 12, 18, 20, and 24 for:

```text
Akari identity stable
no image-internal text/logos/watermarks
hands/feet/hair connected
caption below image
no overlap
healthy slightly sweet tone
range variety still visible
```

If a page fails, replace that image, update `asset-manifest.json`, rerun `npm run build:tonari:previews`, and review again. Do not run OCR/PDF audit for each replacement.

- [ ] **Step 3: Build the final PDF**

Run:

```bash
npm run build:tonari:pdf
```

Expected: `dist/akari-v1.1-tonari-no-akari.pdf` exists.

- [ ] **Step 4: Run final Tonari audit**

Run:

```bash
npm run audit:tonari:pdf
```

Expected: `tonari no akari pdf audit: ok`.

- [ ] **Step 5: Run full regression verification**

Run:

```bash
npm run test:node
npm run test:python
npm run audit:daybook:pdf
npm run audit:pdf
npm run audit:tonari:pdf
npm run lint:md
git diff --check
```

Expected: all commands pass. `npm run audit` does not include Tonari unless package policy is changed in a separate deliberate edit.

- [ ] **Step 6: Commit the final PDF deliverable**

Run:

```bash
git add dist/akari-v1.1-tonari-no-akari.pdf dist/akari-v1.1-tonari-no-akari-pages source/manifests/tonari-no-akari source/generated/tonari-no-akari
git commit -m "Build Tonari No Akari art book"
```

Do not commit `build/` outputs because they are ignored working artifacts.

## Self-Review Checklist

- Spec coverage: the plan includes A4 portrait output, 24 artwork pages, one generated image per page, Japanese PDF-native title and line, no generated text, range-balanced selection, minimum identity reference pack, lightweight candidate checks, and final document-level audit.
- Placeholder scan: before execution, search this plan for unfinished marker words and SHA placeholder strings.
- Type consistency: document id is always `akari-v1.1-tonari-no-akari`; renderer CLI name is always `tonari-no-akari`; page layout is always `tonari-portrait`; the new block type is always `portrait-plate`; final image asset ids are always `tonari-<page id>`.
