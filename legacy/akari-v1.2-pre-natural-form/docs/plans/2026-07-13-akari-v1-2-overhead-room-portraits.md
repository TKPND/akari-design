# Akari v1.2 Overhead Room Portraits Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 正式な Akari v1.2 参照から、室内の真上俯瞰を中心とする採用画像 10 点、高解像度個別画像、レビュー証跡、採用確定後の縦型閲覧用 PDF を制作する。

**Architecture:** 既存の v1.2 モーション制作と同じく、Python で参照契約、追記型生成リクエスト、レビュー済み候補の採用、候補・最終コンタクトシートを分離する。基準カットを最初に採用し、残り 9 点は正式資料と基準カットを併用して制作する。10 点の最終レビューが承認されるまで PDF 用 manifest とレンダリングを開始しない。

**Tech Stack:** Python 3.12、標準ライブラリ `unittest`、Pillow、JSON manifest、Node.js、Playwright、HTML/CSS、Poppler/QPDF、npm scripts、Codex `view_image` と画像生成。

## Global Constraints

- コア採用数は 10 点とし、全身またはほぼ全身 7 点、寄り 3 点を厳守する。
- 追加 11〜12 点は必須ではない。本計画は品質優先で 10 点を完成条件とし、点数合わせの追加生成をしない。
- キャンバスは 1024x1536、RGB、縦 2:3 とする。
- 全身カットの俯瞰角度は 80〜90 度、寄りは 65〜80 度とする。
- 舞台は室内のみ。背景面はアイボリーのラグ、淡い青または白の寝具、グレーのブランケットを中心にする。
- 小物は 0〜3 個に限定し、読める文字、数字、時計表示、ロゴ、透かしを画像内に入れない。
- 衣装は大きめパーカー＋ショートパンツと、ゆるい T シャツ＋ショートパンツの 2 系統に限定する。
- 足元は全身 7 点のうち縞ソックス 4 点、素足 3 点とし、寄りでは足を無理に画面へ入れない。
- 基調色は白、アイボリー、淡い青、柔らかいグレー、髪の暖色ブラウンに限定する。
- ショートパンツの構造を明確にし、下着のように見える構図や、肌へ不自然に視線を誘導する構図を採用しない。
- 正式な顔、髪、身体比率、髪飾りの左右は Akari v1.2 採用資料を不変入力とする。
- ユーザー提供サンプルは構図、距離、淡い色、柔らかな光だけの参考とし、顔、衣装、文字、小物を継承しない。
- 各生成前に、現在の基準候補と最も関係する正式参照を `view_image` で開き、各参照の役割を明示する。
- `source/generated/v1-2-overhead-room/` と候補比較シートは Git に追加しない。
- 全 10 点の最終コンタクトシートがユーザー承認されるまで PDF manifest、プレビュー、PDF を生成しない。
- PDF は 8x12 インチ、プレビュー 1024x1536、一作品一ページを基本とする。
- 既存の settings PDF、daybook、tonari-no-akari の契約を変更しない。

---

## File Structure

### Production contracts and tools

- `source/references/v1-2-overhead-room/overhead-composition-sample.webp`: ユーザー提供サンプルの構図用派生画像。
- `source/manifests/v1-2-overhead-room/reference-pack.json`: 顔、8 方向、3 モーション、構図参考のパスとハッシュ。
- `source/manifests/v1-2-overhead-room/pose-slots.json`: 10 ポーズの順序、分類、角度、衣装、背景、小物契約。
- `source/manifests/v1-2-overhead-room/generation-requests.json`: 全ラウンドを保持する追記型生成リクエスト。
- `source/manifests/v1-2-overhead-room/accepted-selection.json`: 1 ポーズ 1 採用の追跡情報。
- `scripts/v1_2_overhead_room_common.py`: JSON、ハッシュ、パス解決、参照・ポーズ契約検証。
- `scripts/build_v1_2_overhead_room_reference_pack.py`: 現行採用資料から固定参照 pack を作る。
- `scripts/build_v1_2_overhead_room_generation_requests.py`: 1 ポーズ 2 候補のリクエストと再生成履歴を作る。
- `scripts/promote_v1_2_overhead_room_candidate.py`: レビュー済み候補を WebP へ原子的に採用する。
- `scripts/build_v1_2_overhead_room_contact_sheet.py`: 2 候補比較と最終 10 点比較を作る。
- `scripts/audit_v1_2_overhead_room_collection.py`: PDF 前の 10 点完成契約を検証する。

### Review evidence and accepted assets

- `evidence/v1-2-overhead-room/reviews/`: ポーズごとの追跡可能なレビュー JSON。
- `evidence/v1-2-overhead-room/final-review.json`: 10 点の最終ユーザー承認。
- `evidence/v1-2-overhead-room/contact-sheets/final-overhead-room.webp`: 追跡対象の最終比較シート。
- `source/finished/v1-2-overhead-room/`: 採用済み 1024x1536 WebP 10 点。

### PDF pipeline

- `scripts/build_v1_2_overhead_room_pdf_manifests.py`: 採用 selection と最終 review から PDF manifest 3 種を作る。
- `source/manifests/v1-2-overhead-room/source-assets.json`: PDF 用 asset ID と完成画像パス。
- `source/manifests/v1-2-overhead-room/asset-manifest.json`: PDF 掲載対象と追跡情報。
- `source/manifests/v1-2-overhead-room/page-manifest.json`: 表紙、作品 10 ページ、奥付の 12 ページ構成。
- `tools/pdf/overhead-room-document.mjs`: manifest を検証し既存 renderer 用ページモデルへ変換する。
- `tools/pdf/overhead-room-document.test.mjs`: ページ順、比率、source、最小テキストの Node 契約。
- `scripts/render_overhead_room_previews.py`: 12 ページのプレビュー生成 wrapper。
- `scripts/export_overhead_room_pdf.py`: 最終 PDF 生成 wrapper。
- `scripts/audit_overhead_room_pdf.py`: 2:3、12 ページ、画像、文字、フォント監査。
- `tests/test_overhead_room_pdf_audit.py`: PDF 監査関数の単体テスト。

---

### Task 1: Lock the Reference Pack and Ten Pose Contracts

**Files:**

- Create: `source/references/v1-2-overhead-room/overhead-composition-sample.webp`
- Create: `source/manifests/v1-2-overhead-room/reference-pack.json`
- Create: `source/manifests/v1-2-overhead-room/pose-slots.json`
- Create: `scripts/v1_2_overhead_room_common.py`
- Create: `scripts/build_v1_2_overhead_room_reference_pack.py`
- Create: `tests/test_v1_2_overhead_room_common.py`

**Interfaces:**

- Consumes: 採用済み face、turnaround、motion manifest とユーザー提供サンプル派生画像。
- Produces: `load_json(path: Path) -> dict`、`dump_json(path: Path, data: dict) -> None`、`sha256_file(path: Path) -> str`、`resolve_path(project_root: Path, path_text: str) -> Path`、`reference_pack_fingerprint(pack: dict) -> str`、`build_reference_pack(project_root: Path, composition_path: Path) -> dict`、`validate_reference_pack(pack: dict, project_root: Path) -> None`、`validate_pose_slots(manifest: dict) -> None`。

- [ ] **Step 1: Write the failing reference and pose contract tests**

```python
# tests/test_v1_2_overhead_room_common.py
import copy
import unittest
from pathlib import Path

from scripts.v1_2_overhead_room_common import (
    POSE_SLOTS,
    load_json,
    validate_pose_slots,
    validate_reference_pack,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/v1-2-overhead-room"


class AkariV12OverheadRoomCommonTest(unittest.TestCase):
    def test_repository_reference_pack_is_current(self):
        validate_reference_pack(load_json(MANIFEST_DIR / "reference-pack.json"), ROOT)

    def test_repository_pose_contract_has_ten_ordered_slots(self):
        manifest = load_json(MANIFEST_DIR / "pose-slots.json")
        validate_pose_slots(manifest)
        self.assertEqual(POSE_SLOTS, tuple(item["slug"] for item in manifest["poses"]))
        self.assertEqual(7, sum(item["framing"] == "full" for item in manifest["poses"]))
        self.assertEqual(3, sum(item["framing"] == "close" for item in manifest["poses"]))
        self.assertTrue(all(item["candidate_count"] == 2 for item in manifest["poses"]))

    def test_reference_manifest_hash_drift_is_rejected(self):
        pack = copy.deepcopy(load_json(MANIFEST_DIR / "reference-pack.json"))
        pack["source_manifests"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "manifest hash drift"):
            validate_reference_pack(pack, ROOT)

    def test_reference_asset_hash_drift_is_rejected(self):
        pack = copy.deepcopy(load_json(MANIFEST_DIR / "reference-pack.json"))
        pack["reference_inputs"][0]["assets"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "reference asset hash drift"):
            validate_reference_pack(pack, ROOT)

    def test_composition_reference_cannot_be_an_identity_source(self):
        pack = copy.deepcopy(load_json(MANIFEST_DIR / "reference-pack.json"))
        composition = next(item for item in pack["reference_inputs"] if item["role"] == "composition_mood_only")
        composition["identity_source"] = True
        with self.assertRaisesRegex(ValueError, "composition reference"):
            validate_reference_pack(pack, ROOT)
```

- [ ] **Step 2: Run the test and verify the missing module failure**

Run: `uv run python -m unittest tests.test_v1_2_overhead_room_common -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.v1_2_overhead_room_common'`.

- [ ] **Step 3: Implement the common contract module**

```python
# scripts/v1_2_overhead_room_common.py
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from scripts.v1_2_motion_common import dump_json, load_json, resolve_path, sha256_file

COLLECTION_ID = "akari-v1.2-overhead-room-portraits"
POSE_SLOTS = (
    "supine-direct-gaze",
    "supine-bent-knees",
    "supine-overhead-stretch",
    "side-curled-gaze",
    "side-reaching-hand",
    "prone-chin-on-arms",
    "floor-seated-look-up",
    "close-face-hair-spread",
    "close-upper-body-hands",
    "close-sleeved-reaching-hand",
)
FULL_SLOTS = POSE_SLOTS[:7]
CLOSE_SLOTS = POSE_SLOTS[7:]


def reference_pack_fingerprint(pack: dict) -> str:
    payload = {key: value for key, value in pack.items() if key != "pack_sha256"}
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_pose_slots(manifest: dict) -> None:
    if manifest.get("schema_version") != 1 or manifest.get("collection_id") != COLLECTION_ID:
        raise ValueError("invalid overhead room pose manifest identity")
    poses = manifest.get("poses")
    if not isinstance(poses, list) or tuple(item.get("slug") for item in poses) != POSE_SLOTS:
        raise ValueError("overhead room poses must match the ten canonical slots")
    for order, pose in enumerate(poses, 1):
        expected_framing = "full" if pose["slug"] in FULL_SLOTS else "close"
        expected_range = [80, 90] if expected_framing == "full" else [65, 80]
        if (
            pose.get("pose_order") != order
            or pose.get("framing") != expected_framing
            or pose.get("angle_degrees") != expected_range
            or pose.get("candidate_count") != 2
            or pose.get("deliverable_count") != 1
            or pose.get("outfit") not in {"oversized-hoodie-shorts", "loose-tshirt-shorts"}
            or pose.get("feet") not in {"striped-socks", "barefoot", "not-visible"}
            or (expected_framing == "full" and pose.get("feet") == "not-visible")
            or pose.get("background") not in {"ivory-rug", "pale-bedding", "gray-blanket"}
            or not 0 <= pose.get("prop_count", -1) <= 3
        ):
            raise ValueError(f"invalid pose contract: {pose.get('slug')}")


def validate_reference_pack(pack: dict, project_root: Path) -> None:
    if pack.get("schema_version") != 1 or pack.get("collection_id") != COLLECTION_ID:
        raise ValueError("invalid overhead room reference pack identity")
    if pack.get("pack_sha256") != reference_pack_fingerprint(pack):
        raise ValueError("reference pack fingerprint drift")
    for record in pack.get("source_manifests", []):
        path = resolve_path(project_root, record["path"])
        if not path.is_file() or sha256_file(path) != record["sha256"]:
            raise ValueError(f"source manifest hash drift: {record['role']}")
    references = pack.get("reference_inputs", [])
    required_roles = {"identity_face", "turnaround", "motion", "composition_mood_only"}
    if {item.get("role") for item in references} != required_roles:
        raise ValueError("reference pack roles are incomplete")
    for record in references:
        for asset in record["assets"]:
            path = resolve_path(project_root, asset["path"])
            if not path.is_file() or sha256_file(path) != asset["sha256"]:
                raise ValueError(f"reference asset hash drift: {asset['path']}")
        if record["role"] == "composition_mood_only" and record.get("identity_source") is not False:
            raise ValueError("composition reference must not be an identity source")
```

Reuse the atomic `dump_json()` from `scripts.v1_2_motion_common.py`; do not duplicate its temporary-file and fsync logic.

- [ ] **Step 4: Create the exact ten-pose manifest**

Write `source/manifests/v1-2-overhead-room/pose-slots.json` with ten ordered records using this exact compact data:

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.2-overhead-room-portraits",
  "poses": [
    {"slug":"supine-direct-gaze","pose_order":1,"title":"Direct Gaze","framing":"full","angle_degrees":[80,90],"candidate_count":2,"deliverable_count":1,"outfit":"oversized-hoodie-shorts","feet":"striped-socks","background":"ivory-rug","prop_count":1},
    {"slug":"supine-bent-knees","pose_order":2,"title":"Bent Knees","framing":"full","angle_degrees":[80,90],"candidate_count":2,"deliverable_count":1,"outfit":"loose-tshirt-shorts","feet":"barefoot","background":"pale-bedding","prop_count":0},
    {"slug":"supine-overhead-stretch","pose_order":3,"title":"Slow Stretch","framing":"full","angle_degrees":[80,90],"candidate_count":2,"deliverable_count":1,"outfit":"oversized-hoodie-shorts","feet":"striped-socks","background":"ivory-rug","prop_count":0},
    {"slug":"side-curled-gaze","pose_order":4,"title":"Curled Close","framing":"full","angle_degrees":[80,90],"candidate_count":2,"deliverable_count":1,"outfit":"loose-tshirt-shorts","feet":"barefoot","background":"gray-blanket","prop_count":1},
    {"slug":"side-reaching-hand","pose_order":5,"title":"Reach","framing":"full","angle_degrees":[80,90],"candidate_count":2,"deliverable_count":1,"outfit":"oversized-hoodie-shorts","feet":"striped-socks","background":"pale-bedding","prop_count":0},
    {"slug":"prone-chin-on-arms","pose_order":6,"title":"Quiet Look","framing":"full","angle_degrees":[80,90],"candidate_count":2,"deliverable_count":1,"outfit":"loose-tshirt-shorts","feet":"barefoot","background":"gray-blanket","prop_count":1},
    {"slug":"floor-seated-look-up","pose_order":7,"title":"Look Up","framing":"full","angle_degrees":[80,90],"candidate_count":2,"deliverable_count":1,"outfit":"oversized-hoodie-shorts","feet":"striped-socks","background":"ivory-rug","prop_count":0},
    {"slug":"close-face-hair-spread","pose_order":8,"title":"Hair and Eyes","framing":"close","angle_degrees":[65,80],"candidate_count":2,"deliverable_count":1,"outfit":"loose-tshirt-shorts","feet":"not-visible","background":"pale-bedding","prop_count":0},
    {"slug":"close-upper-body-hands","pose_order":9,"title":"At Hand","framing":"close","angle_degrees":[65,80],"candidate_count":2,"deliverable_count":1,"outfit":"loose-tshirt-shorts","feet":"not-visible","background":"ivory-rug","prop_count":1},
    {"slug":"close-sleeved-reaching-hand","pose_order":10,"title":"Sleeved Reach","framing":"close","angle_degrees":[65,80],"candidate_count":2,"deliverable_count":1,"outfit":"oversized-hoodie-shorts","feet":"not-visible","background":"gray-blanket","prop_count":0}
  ]
}
```

- [ ] **Step 5: Build the composition derivative and reference pack**

Run:

```bash
mkdir -p source/references/v1-2-overhead-room
cwebp -quiet -q 95 -m 6 -sharp_yuv -metadata none \
  '/path/to/input/ChatGPT Image 2026年7月13日 14_14_03.png' \
  -o source/references/v1-2-overhead-room/overhead-composition-sample.webp
```

Implement `build_reference_pack()` from these exact source manifests:

```python
SOURCE_MANIFESTS = {
    "identity_face": "source/manifests/v1-2-face-hair/accepted-selection.json",
    "turnaround": "source/manifests/v1-2-turnaround/accepted-angles.json",
    "motion": "source/manifests/v1-2-motion/accepted-selection.json",
}
COMPOSITION_PATH = "source/references/v1-2-overhead-room/overhead-composition-sample.webp"
```

The face group contains one accepted face; turnaround contains all eight accepted angles in manifest order; motion contains walking, seated, turning in order; composition has `identity_source: false` and allowed use limited to camera angle, distance, negative space, soft light, and pale palette. After assembling the record, set `pack_sha256 = reference_pack_fingerprint(pack)` and then validate it. The CLI accepts `--composition` and `--output`, validates before writing, and prints `overhead room reference pack written: 13 assets`.

Run:

```bash
uv run python -m scripts.build_v1_2_overhead_room_reference_pack \
  --composition source/references/v1-2-overhead-room/overhead-composition-sample.webp \
  --output source/manifests/v1-2-overhead-room/reference-pack.json
uv run python -m unittest tests.test_v1_2_overhead_room_common -v
```

Expected: 13 assets reported and all five tests PASS.

- [ ] **Step 6: Commit the immutable inputs and contract**

```bash
git add \
  source/references/v1-2-overhead-room/overhead-composition-sample.webp \
  source/manifests/v1-2-overhead-room/reference-pack.json \
  source/manifests/v1-2-overhead-room/pose-slots.json \
  scripts/v1_2_overhead_room_common.py \
  scripts/build_v1_2_overhead_room_reference_pack.py \
  tests/test_v1_2_overhead_room_common.py
git commit -m "feat: lock overhead room reference contract"
```

### Task 2: Build Append-Only Two-Candidate Generation Requests

**Files:**

- Create: `scripts/build_v1_2_overhead_room_generation_requests.py`
- Create: `tests/test_v1_2_overhead_room_generation_requests.py`
- Create: `source/manifests/v1-2-overhead-room/generation-requests.json`
- Modify: `package.json`

**Interfaces:**

- Consumes: validated reference pack, ten-pose manifest, current accepted selection, pose slug, date prefix, revision, failure observations.
- Produces: `build_ready_batch(reference_pack: dict, pose_manifest: dict, pose: str, date_prefix: str, revision: int, failure_observations: list[str], collection_anchor: dict | None) -> dict`、`merge_request_history(existing: dict, batch: dict) -> dict`、npm command `build:v1-2-overhead-room:requests`。

- [ ] **Step 1: Write failing request builder tests**

```python
# tests/test_v1_2_overhead_room_generation_requests.py
import unittest

from scripts.build_v1_2_overhead_room_generation_requests import (
    build_ready_batch,
    merge_request_history,
)

PACK = {
    "collection_id": "akari-v1.2-overhead-room-portraits",
    "pack_sha256": "pack-hash",
    "reference_inputs": [
        {"role": "identity_face", "assets": [{"path": "face.webp", "sha256": "f"}]},
        {"role": "turnaround", "assets": [{"path": "front.webp", "sha256": "t"}]},
        {"role": "motion", "assets": [{"path": "seated.webp", "sha256": "m"}]},
        {"role": "composition_mood_only", "identity_source": False, "assets": [{"path": "sample.webp", "sha256": "c"}]},
    ],
}
POSES = {"poses": [{
    "slug": "supine-direct-gaze", "pose_order": 1, "framing": "full",
    "angle_degrees": [80, 90], "candidate_count": 2,
        "outfit": "oversized-hoodie-shorts", "feet": "striped-socks", "background": "ivory-rug",
    "prop_count": 1,
}]}


class AkariV12OverheadRoomGenerationRequestsTest(unittest.TestCase):
    def test_anchor_batch_has_two_requests_and_no_collection_anchor(self):
        batch = build_ready_batch(PACK, POSES, "supine-direct-gaze", "20260713", 1, [], None)
        self.assertEqual(2, len(batch["requests"]))
        self.assertEqual([1, 2], [item["candidate_number"] for item in batch["requests"]])
        self.assertTrue(all("collection_anchor" not in item for item in batch["requests"]))

    def test_non_anchor_pose_requires_accepted_collection_anchor(self):
        poses = {"poses": [dict(POSES["poses"][0], slug="supine-bent-knees", pose_order=2)]}
        with self.assertRaisesRegex(ValueError, "collection anchor"):
            build_ready_batch(PACK, poses, "supine-bent-knees", "20260713", 1, [], None)

    def test_regeneration_requires_non_blank_failure_observations(self):
        with self.assertRaisesRegex(ValueError, "failure observations"):
            build_ready_batch(PACK, POSES, "supine-direct-gaze", "20260713", 2, [], None)

    def test_history_is_idempotent_and_rejects_older_reactivation(self):
        empty = {"schema_version": 1, "collection_id": PACK["collection_id"], "active_batches": {}, "requests": []}
        first = build_ready_batch(PACK, POSES, "supine-direct-gaze", "20260713", 1, [], None)
        current = merge_request_history(empty, first)
        second = build_ready_batch(PACK, POSES, "supine-direct-gaze", "20260713", 2, ["hand anatomy failed"], None)
        revised = merge_request_history(current, second)
        self.assertEqual(revised, merge_request_history(revised, second))
        with self.assertRaisesRegex(ValueError, "older revision"):
            merge_request_history(revised, first)
```

- [ ] **Step 2: Run the test and verify the missing module failure**

Run: `uv run python -m unittest tests.test_v1_2_overhead_room_generation_requests -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement prompt and request construction**

Use exact IDs and paths:

```python
PROMPT_TEMPLATE_VERSION = "akari_v1_2_overhead_room_v1"
batch_id = f"batch:v1-2-overhead-room:{date_prefix}:{pose}:r{revision}"
request_id = f"request:v1-2-overhead-room:{date_prefix}:{pose}:r{revision}:c{candidate_number}"
target_path = f"source/generated/v1-2-overhead-room/{date_prefix}_{pose}_r{revision}_c{candidate_number}.png"
```

Every request contains `id`, `batch_id`, `pose`, `pose_order`, `framing`, `angle_degrees`, `outfit`, `feet`, `background`, `prop_count`, `revision`, `candidate_number`, `variation`, `reference_roles`, `source_pack_sha256`, optional `collection_anchor`, `target_path`, `prompt_template_version`, `prompt`, `acceptance_gates`, and `review_plan`.

```python
POSE_VARIATIONS = {
    "supine-direct-gaze": ("body nearly vertical with one hand over chest", "body on a slight diagonal with both hands relaxed near torso"),
    "supine-bent-knees": ("both knees raised with a gentle offset", "one knee higher with ankles softly crossed"),
    "supine-overhead-stretch": ("one arm extended above the head", "both arms loosely stretched with asymmetric sleeves"),
    "side-curled-gaze": ("knees softly tucked and cheek on a cushion", "looser side curl with one hand near the face"),
    "side-reaching-hand": ("open hand reaching gently toward camera", "sleeved fingers reaching without hiding the face"),
    "prone-chin-on-arms": ("chin on crossed forearms with legs extended", "chin on stacked hands with lower legs softly offset"),
    "floor-seated-look-up": ("relaxed cross-legged seat", "soft side-seated pose with one supporting hand"),
    "close-face-hair-spread": ("direct gaze with hair fanned evenly", "slightly turned face with asymmetric hair spread"),
    "close-upper-body-hands": ("phone held loosely against chest with blank screen", "closed book held near torso with blank cover"),
    "close-sleeved-reaching-hand": ("open sleeved hand near camera", "relaxed fingers emerging from oversized cuff"),
}
```

The shared prompt must lock adult 25-year-old Akari identity consistent with accepted v1.2 references, warm brown bob, amber eyes, two-part character-left ornament, 1024x1536 RGB, requested angle/outfit/background/prop count, connected anatomy, and intimate but healthy directness. Exclude skirt, unnecessary shoes, text, logos, clock displays, packaging, watermark, borders, panels, and other characters. State that the composition sample is not an identity or wardrobe source.

Pose 1 selects face, front turnaround, seated motion, and composition mood. Poses 2〜10 require role-appropriate official references plus the accepted `supine-direct-gaze` finished image as `collection_anchor`. Revisions above one append trimmed failure observations.

- [ ] **Step 4: Add the empty request manifest and npm command**

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.2-overhead-room-portraits",
  "prompt_template_version": "akari_v1_2_overhead_room_v1",
  "active_batches": {},
  "requests": []
}
```

Add:

```json
"build:v1-2-overhead-room:requests": "uv run python -m scripts.build_v1_2_overhead_room_generation_requests"
```

- [ ] **Step 5: Run focused tests and CLI help**

```bash
uv run python -m unittest tests.test_v1_2_overhead_room_generation_requests -v
bash -lc 'npm run build:v1-2-overhead-room:requests -- --help'
```

Expected: all tests PASS; help lists `--pose`, `--date-prefix`, `--revision`, `--failure-observation`, `--reference-pack`, `--pose-manifest`, `--accepted`, and `--output`.

- [ ] **Step 6: Commit the request builder**

```bash
git add \
  scripts/build_v1_2_overhead_room_generation_requests.py \
  tests/test_v1_2_overhead_room_generation_requests.py \
  source/manifests/v1-2-overhead-room/generation-requests.json \
  package.json
git commit -m "feat: build overhead room generation requests"
```

### Task 3: Validate Reviews and Promote One Candidate per Pose

**Files:**

- Create: `scripts/promote_v1_2_overhead_room_candidate.py`
- Create: `tests/test_v1_2_overhead_room_promotion.py`
- Create: `source/manifests/v1-2-overhead-room/accepted-selection.json`
- Modify: `package.json`

**Interfaces:**

- Consumes: reference pack, request manifest, one review JSON, current selection, candidate PNGs.
- Produces: `validate_review(review: dict, request_manifest: dict, reference_pack: dict) -> tuple[dict, dict]`、`promote_review(review: dict, request_manifest: dict, reference_pack: dict, accepted: dict, project_root: Path, replace: bool = False) -> dict`、npm command `promote:v1-2-overhead-room`。

- [ ] **Step 1: Write failing promotion tests**

```python
# tests/test_v1_2_overhead_room_promotion.py
import copy
import tempfile
import unittest
from pathlib import Path
from PIL import Image

from scripts.promote_v1_2_overhead_room_candidate import promote_review

GATES = {
    "identity", "age", "overhead_read", "anatomy", "ornament_side",
    "outfit", "intimacy", "composition", "artifacts", "collection_role",
}


def fixtures(root: Path):
    requests = []
    candidates = []
    for number in (1, 2):
        path = root / f"candidate-{number}.png"
        Image.new("RGB", (1024, 1536), "white").save(path)
        candidates.append(path)
        requests.append({
            "id": f"request-{number}", "batch_id": "batch-r1",
            "pose": "supine-direct-gaze", "pose_order": 1,
            "revision": 1, "candidate_number": number,
            "target_path": path.as_posix(), "source_pack_sha256": "pack-hash",
        })
    manifest = {"active_batches": {"supine-direct-gaze": "batch-r1"}, "requests": requests}
    review = {
        "review_id": "review-r1", "review_path": "evidence/review-r1.json",
        "pose": "supine-direct-gaze", "batch_id": "batch-r1",
        "review_status": "approved",
        "candidates": [
            {
                "request_id": request["id"],
                "candidate_path": path.as_posix(),
                "decision": decision,
                "gates": {gate: "pass" for gate in GATES},
                "observations": {gate: f"{gate} checked" for gate in GATES},
                "decision_reason": "strongest finished image" if decision == "accept" else "weaker expression",
            }
            for request, path, decision in zip(requests, candidates, ("accept", "hold"), strict=True)
        ],
    }
    return manifest, review


class AkariV12OverheadRoomPromotionTest(unittest.TestCase):
    def test_promotes_exactly_one_active_candidate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, review = fixtures(root)
            accepted = {"schema_version": 1, "collection_id": "akari-v1.2-overhead-room-portraits", "accepted_works": []}
            result = promote_review(review, requests, {"pack_sha256": "pack-hash"}, accepted, root)
            self.assertEqual("supine-direct-gaze", result["accepted_works"][0]["pose"])
            self.assertTrue((root / result["accepted_works"][0]["finished_path"]).is_file())

    def test_rejects_multiple_accepts_and_failed_gates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, review = fixtures(root)
            accepted = {"schema_version": 1, "collection_id": "akari-v1.2-overhead-room-portraits", "accepted_works": []}
            multiple = copy.deepcopy(review)
            multiple["candidates"][1]["decision"] = "accept"
            with self.assertRaisesRegex(ValueError, "exactly one accepted candidate"):
                promote_review(multiple, requests, {"pack_sha256": "pack-hash"}, accepted, root)
            failed = copy.deepcopy(review)
            failed["candidates"][0]["gates"]["anatomy"] = "fail"
            with self.assertRaisesRegex(ValueError, "all acceptance gates"):
                promote_review(failed, requests, {"pack_sha256": "pack-hash"}, accepted, root)

    def test_rejects_wrong_dimensions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests, review = fixtures(root)
            Image.new("RGB", (512, 768), "white").save(review["candidates"][0]["candidate_path"])
            accepted = {"schema_version": 1, "collection_id": "akari-v1.2-overhead-room-portraits", "accepted_works": []}
            with self.assertRaisesRegex(ValueError, "RGB 1024x1536"):
                promote_review(review, requests, {"pack_sha256": "pack-hash"}, accepted, root)
```

- [ ] **Step 2: Run the test and verify the missing module failure**

Run: `uv run python -m unittest tests.test_v1_2_overhead_room_promotion -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement strict review validation and transactional promotion**

Use:

```python
REQUIRED_GATES = {
    "identity", "age", "overhead_read", "anatomy", "ornament_side",
    "outfit", "intimacy", "composition", "artifacts", "collection_role",
}
ALLOWED_DECISIONS = {"accept", "hold", "reject"}
```

`validate_review()` requires one active batch, exactly two reviewed active requests, exact ID/path matches, all gate observations, a non-empty decision reason for each candidate, exactly one `accept`, all accepted gates `pass`, and `review_status == "approved"`.

Validate the current selection before promotion: accepted poses must be a unique canonical prefix of `POSE_SLOTS`. A new promotion must be the next canonical pose; only explicit `--replace` may target an already accepted pose, and replacement must preserve its `pose_order`.

The CLI loads and revalidates the repository reference pack before calling `promote_review()`. The function compares `source_pack_sha256`, rejects implicit replacement and out-of-order promotion, verifies RGB 1024x1536, stages quality-95 method-6 WebP, and reuses `commit_promotion_transaction()` from `scripts.promote_v1_2_motion_candidate` so image and manifest commit or roll back together. Unit tests may pass the already-validated synthetic pack shown above.

```python
record = {
    "pose": request["pose"],
    "pose_order": request["pose_order"],
    "finished_path": f"source/finished/v1-2-overhead-room/{request['pose']}.webp",
    "source_candidate_path": candidate["candidate_path"],
    "request_id": request["id"],
    "batch_id": request["batch_id"],
    "revision": request["revision"],
    "candidate_number": request["candidate_number"],
    "review_id": review["review_id"],
    "review_path": review["review_path"],
    "source_pack_sha256": request["source_pack_sha256"],
    "source_sha256": sha256_file(source_path),
    "finished_sha256": sha256_file(staged_webp),
}
```

The CLI accepts `--review`, `--requests`, `--reference-pack`, `--accepted`, and explicit `--replace`. No output is written before all validation passes.

- [ ] **Step 4: Add the empty selection manifest and npm command**

```json
{
  "schema_version": 1,
  "collection_id": "akari-v1.2-overhead-room-portraits",
  "accepted_works": []
}
```

Add:

```json
"promote:v1-2-overhead-room": "uv run python -m scripts.promote_v1_2_overhead_room_candidate"
```

- [ ] **Step 5: Run promotion tests and CLI help**

```bash
uv run python -m unittest tests.test_v1_2_overhead_room_promotion -v
bash -lc 'npm run promote:v1-2-overhead-room -- --help'
```

Expected: all tests PASS and help includes all five arguments.

- [ ] **Step 6: Commit the promotion workflow**

```bash
git add \
  scripts/promote_v1_2_overhead_room_candidate.py \
  tests/test_v1_2_overhead_room_promotion.py \
  source/manifests/v1-2-overhead-room/accepted-selection.json \
  package.json
git commit -m "feat: promote overhead room portraits"
```

### Task 4: Build Two-Candidate and Final Contact Sheets

**Files:**

- Create: `scripts/build_v1_2_overhead_room_contact_sheet.py`
- Create: `tests/test_v1_2_overhead_room_contact_sheet.py`
- Modify: `package.json`
- Modify: `.gitignore`

**Interfaces:**

- Consumes: active request batch, optional review decisions, accepted selection.
- Produces: `select_active_requests(manifest: dict, pose: str) -> list[dict]`、`build_batch_contact_sheet(requests: list[dict], reviews: dict[str, dict], project_root: Path, output_path: Path) -> Path`、`build_final_contact_sheet(accepted_records: list[dict], project_root: Path, output_path: Path) -> Path`、npm command `build:v1-2-overhead-room:contact-sheet`。

- [ ] **Step 1: Write failing contact-sheet tests**

```python
# tests/test_v1_2_overhead_room_contact_sheet.py
import tempfile
import unittest
from pathlib import Path
from PIL import Image

from scripts.build_v1_2_overhead_room_contact_sheet import (
    build_batch_contact_sheet,
    build_final_contact_sheet,
    select_active_requests,
)


def make_image(path: Path) -> str:
    Image.new("RGB", (1024, 1536), "white").save(path)
    return path.as_posix()


class AkariV12OverheadRoomContactSheetTest(unittest.TestCase):
    def test_selects_two_requests_from_only_the_active_batch(self):
        manifest = {"active_batches": {"supine-direct-gaze": "r2"}, "requests": [
            {"pose": "supine-direct-gaze", "batch_id": batch, "revision": int(batch[-1]),
             "candidate_number": number, "target_path": f"{batch}-{number}.png"}
            for batch in ("r1", "r2") for number in (1, 2)
        ]}
        selected = select_active_requests(manifest, "supine-direct-gaze")
        self.assertEqual([1, 2], [item["candidate_number"] for item in selected])
        self.assertEqual({"r2"}, {item["batch_id"] for item in selected})

    def test_batch_sheet_requires_two_rgb_candidates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            requests = [
                {"id": f"r-{number}", "pose": "supine-direct-gaze", "batch_id": "r1",
                 "revision": 1, "candidate_number": number,
                 "target_path": make_image(root / f"c{number}.png")}
                for number in (1, 2)
            ]
            output = root / "batch.webp"
            self.assertEqual(output, build_batch_contact_sheet(requests, {}, root, output))

    def test_final_sheet_requires_ten_accepted_works(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            records = [
                {"pose": f"pose-{order}", "pose_order": order,
                 "finished_path": make_image(root / f"pose-{order}.webp")}
                for order in range(1, 11)
            ]
            self.assertEqual(root / "final.webp", build_final_contact_sheet(records, root, root / "final.webp"))
            with self.assertRaisesRegex(ValueError, "ten accepted works"):
                build_final_contact_sheet(records[:9], root, root / "bad.webp")
```

- [ ] **Step 2: Run the test and verify the missing module failure**

Run: `uv run python -m unittest tests.test_v1_2_overhead_room_contact_sheet -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement deterministic sheets**

Use the font fallback and contained-image loading pattern from `scripts/build_v1_2_motion_contact_sheet.py`. Candidate sheets use two 360x540 image cards and external labels for pose, revision, candidate, and decision. Reject missing, unreadable, non-RGB, or non-1024x1536 sources before replacing output.

The final sheet sorts by `pose_order`, requires exactly ten unique core poses, and lays them out five columns by two rows. Each 256x384 card has an external order/title label. The CLI uses mutually exclusive `--requests` and `--accepted`; batch mode requires `--pose` and accepts repeatable `--review`; both modes require `--output`.

- [ ] **Step 4: Add npm command and narrow ignore rules**

```json
"build:v1-2-overhead-room:contact-sheet": "uv run python -m scripts.build_v1_2_overhead_room_contact_sheet"
```

Append:

```gitignore
source/generated/v1-2-overhead-room/
evidence/v1-2-overhead-room/contact-sheets/batches/
```

Do not ignore reviews, final review, or final contact sheet.

- [ ] **Step 5: Run tests and ignore checks**

```bash
uv run python -m unittest tests.test_v1_2_overhead_room_contact_sheet -v
git check-ignore \
  source/generated/v1-2-overhead-room/example.png \
  evidence/v1-2-overhead-room/contact-sheets/batches/example.webp
! git check-ignore evidence/v1-2-overhead-room/reviews/example.json
```

Expected: tests PASS, two working paths are ignored, review JSON is not ignored.

- [ ] **Step 6: Commit the contact-sheet workflow**

```bash
git add \
  scripts/build_v1_2_overhead_room_contact_sheet.py \
  tests/test_v1_2_overhead_room_contact_sheet.py \
  package.json .gitignore
git commit -m "feat: build overhead room contact sheets"
```

### Task 5: Generate and Approve the Collection Anchor

**Files:**

- Modify: `source/manifests/v1-2-overhead-room/generation-requests.json`
- Modify: `source/manifests/v1-2-overhead-room/accepted-selection.json`
- Create: `evidence/v1-2-overhead-room/reviews/supine-direct-gaze-r1-review.json`
- Create: `source/finished/v1-2-overhead-room/supine-direct-gaze.webp`
- Create locally, ignored: two exact anchor candidate PNGs and one batch sheet.

**Interfaces:**

- Consumes: Tasks 1〜4, official references, composition-only sample, user approval.
- Produces: accepted collection anchor used by every later pose.

- [ ] **Step 1: Build the anchor request batch**

```bash
bash -lc 'npm run build:v1-2-overhead-room:requests -- --pose supine-direct-gaze --date-prefix 20260713 --revision 1'
```

Expected: `overhead room requests written: 2`; no request has `collection_anchor`.

- [ ] **Step 2: Open exact references and state their roles**

Open with `view_image`:

- `source/finished/v1-2-face-hair/akari-v1-2-standard-face.webp`: face, adult age, eyes, bangs, ornament.
- `source/finished/v1-2-turnaround/front.webp`: proportion and hoodie construction.
- `source/finished/v1-2-turnaround/character-left-front-three-quarter.webp`: cheek-side hair and ornament continuity.
- `source/finished/v1-2-motion/seated.webp`: bent limbs and fabric compression.
- `source/references/v1-2-overhead-room/overhead-composition-sample.webp`: overhead angle, close gaze, negative space, pale room palette only.

- [ ] **Step 3: Generate both anchor candidates**

Call image generation once per request with the five opened references, request prompt verbatim, and exact target path. If no PNG lands locally, structurally parse the current-day rollout JSONL, select the `image_generation_call` result beginning `iVBOR`, verify decoded PNG signature `89504e470d0a1a0a`, and write it to the target. Record generation IDs in the review. Open both PNGs at original detail.

- [ ] **Step 4: Build and inspect the anchor sheet**

```bash
bash -lc 'npm run build:v1-2-overhead-room:contact-sheet -- --requests source/manifests/v1-2-overhead-room/generation-requests.json --pose supine-direct-gaze --output evidence/v1-2-overhead-room/contact-sheets/batches/supine-direct-gaze-r1.webp'
```

Inspect identity, adult age, overhead read, anatomy, ornament, hoodie/shorts, direct gaze, restrained background, artifacts, and collection-anchor quality.

- [ ] **Step 5: Record one accepted review and obtain user approval**

Write the exact review JSON with review identity, batch, generation IDs, two candidates, decisions, ten gates, ten observations, and decision reasons. Set `review_status: "approved"` only after user acceptance. If neither passes, retain the rejection record and build a new revision with concrete `--failure-observation` flags.

- [ ] **Step 6: Promote and verify the anchor**

```bash
bash -lc 'npm run promote:v1-2-overhead-room -- --review evidence/v1-2-overhead-room/reviews/supine-direct-gaze-r1-review.json'
identify source/finished/v1-2-overhead-room/supine-direct-gaze.webp
```

Expected: one accepted work and `WEBP 1024x1536`, `sRGB`.

- [ ] **Step 7: Commit without generated candidates**

```bash
git add \
  source/manifests/v1-2-overhead-room/generation-requests.json \
  source/manifests/v1-2-overhead-room/accepted-selection.json \
  evidence/v1-2-overhead-room/reviews/supine-direct-gaze-r1-review.json \
  source/finished/v1-2-overhead-room/supine-direct-gaze.webp
git commit -m "feat: establish overhead room collection anchor"
```

Verify generated candidates and batch sheet are absent from `git status --short`.

### Task 6: Produce the Remaining Six Full-Body Poses

**Files:**

- Modify: `source/manifests/v1-2-overhead-room/generation-requests.json`
- Modify: `source/manifests/v1-2-overhead-room/accepted-selection.json`
- Create: six exact first-round review JSONs under `evidence/v1-2-overhead-room/reviews/`
- Create: six matching WebPs under `source/finished/v1-2-overhead-room/`
- Create locally, ignored: twelve candidate PNGs and six batch sheets.

**Interfaces:**

- Consumes: accepted anchor plus role-appropriate official references.
- Produces: accepted works 2〜7 and a complete seven-image full-body set.

- [ ] **Step 1: Build six first-round request batches**

```bash
for pose in \
  supine-bent-knees \
  supine-overhead-stretch \
  side-curled-gaze \
  side-reaching-hand \
  prone-chin-on-arms \
  floor-seated-look-up
do
  bash -lc "npm run build:v1-2-overhead-room:requests -- --pose $pose --date-prefix 20260713 --revision 1"
done
```

Expected: six successful two-request messages; every request records the exact finished anchor path and hash.

- [ ] **Step 2: Generate poses 2〜4 with role-specific references**

Before each generation, open the accepted anchor, standard face, composition sample, and:

- `supine-bent-knees`: front turnaround and seated motion for knees, pelvis, and shorts coverage.
- `supine-overhead-stretch`: front turnaround and walking motion for shoulders, arms, torso, and fabric flow.
- `side-curled-gaze`: both profile turnarounds and seated motion for head/torso silhouette and tucked legs.

State each role. Generate two candidates per pose from the exact requests, save all six target paths, and open each original. Never use the sample for face, body, or wardrobe.

- [ ] **Step 3: Review, approve, and promote poses 2〜4**

Build three batch sheets, inspect originals, and write:

- `evidence/v1-2-overhead-room/reviews/supine-bent-knees-r1-review.json`
- `evidence/v1-2-overhead-room/reviews/supine-overhead-stretch-r1-review.json`
- `evidence/v1-2-overhead-room/reviews/side-curled-gaze-r1-review.json`

Require one accepted candidate and ten gate observations per pose. Regenerate only a failed pose. Present the three selections together and, after user approval, promote each in pose order with its active review path.

- [ ] **Step 4: Generate poses 5〜7 with role-specific references**

Reopen the anchor and the strongest current selected work plus:

- `side-reaching-hand`: standard face, character-left profile, composition sample; the hand must not hide the face.
- `prone-chin-on-arms`: standard face, both front-three-quarter turnarounds, seated motion; preserve shoulders, forearms, pelvis, legs.
- `floor-seated-look-up`: standard face, front turnaround, seated motion, composition sample; keep the seat grounded under a true overhead camera.

Generate two candidates per pose, save targets, and inspect all six originals.

- [ ] **Step 5: Review, approve, and promote poses 5〜7**

Build the three batch sheets and write exact reviews:

- `evidence/v1-2-overhead-room/reviews/side-reaching-hand-r1-review.json`
- `evidence/v1-2-overhead-room/reviews/prone-chin-on-arms-r1-review.json`
- `evidence/v1-2-overhead-room/reviews/floor-seated-look-up-r1-review.json`

Regenerate only failed poses. Present selected works together. After approval, promote in order and confirm the manifest and finished directory contain seven works.

- [ ] **Step 6: Run focused tests**

```bash
uv run python -m unittest \
  tests.test_v1_2_overhead_room_common \
  tests.test_v1_2_overhead_room_generation_requests \
  tests.test_v1_2_overhead_room_promotion \
  tests.test_v1_2_overhead_room_contact_sheet -v
git diff --check
```

Expected: all tests PASS and no whitespace errors.

- [ ] **Step 7: Commit the full-body wave**

```bash
git add \
  source/manifests/v1-2-overhead-room/generation-requests.json \
  source/manifests/v1-2-overhead-room/accepted-selection.json \
  evidence/v1-2-overhead-room/reviews \
  source/finished/v1-2-overhead-room
git commit -m "feat: complete overhead room full-body set"
```

### Task 7: Produce the Three Close Portraits

**Files:**

- Modify: `source/manifests/v1-2-overhead-room/generation-requests.json`
- Modify: `source/manifests/v1-2-overhead-room/accepted-selection.json`
- Create: three close-portrait review JSONs under `evidence/v1-2-overhead-room/reviews/`
- Create: three matching WebPs under `source/finished/v1-2-overhead-room/`
- Create locally, ignored: six candidate PNGs and three batch sheets.

**Interfaces:**

- Consumes: seven accepted full-body works, anchor, face and angle references.
- Produces: accepted works 8〜10 and the complete ten-work selection.

- [ ] **Step 1: Build all three close-up batches**

```bash
for pose in close-face-hair-spread close-upper-body-hands close-sleeved-reaching-hand
do
  bash -lc "npm run build:v1-2-overhead-room:requests -- --pose $pose --date-prefix 20260713 --revision 1"
done
```

Expected: six requests total, 65〜80 degree contracts, and collection anchor on every request.

- [ ] **Step 2: Generate the face-and-hair close portrait**

Open standard face, both front-three-quarter turnarounds, anchor, and composition sample. Face/three-quarter references lock identity and ornament; anchor locks finish; sample contributes only hair-on-surface composition. Generate two, inspect originals, build sheet, write `close-face-hair-spread-r1-review.json`, and revise only if neither passes.

- [ ] **Step 3: Generate the upper-body-and-hands close portrait**

Open standard face, front turnaround, anchor, and the best accepted hand rendering. Generate the blank-screen phone and blank-cover book variants. Reject readable content, extra fingers, merged prop anatomy, or prop dominance. Build sheet and write `close-upper-body-hands-r1-review.json`.

- [ ] **Step 4: Generate the sleeved reaching-hand close portrait**

Open standard face, character-left front-three-quarter, anchor, and accepted `side-reaching-hand`. The earlier reach locks hand scale; face reference prevents identity distortion. Generate two, inspect, build sheet, and write `close-sleeved-reaching-hand-r1-review.json`.

- [ ] **Step 5: Approve and promote all three close portraits**

Present the three selections with seven full-body thumbnails. Confirm new face, hand, sleeve, and texture information without composition repetition. After user approval, promote in order and verify exactly ten accepted works.

- [ ] **Step 6: Commit the close portrait wave**

```bash
git add \
  source/manifests/v1-2-overhead-room/generation-requests.json \
  source/manifests/v1-2-overhead-room/accepted-selection.json \
  evidence/v1-2-overhead-room/reviews \
  source/finished/v1-2-overhead-room
git commit -m "feat: complete overhead room close portraits"
```

### Task 8: Audit and Approve the Final Ten-Work Collection

**Files:**

- Create: `scripts/audit_v1_2_overhead_room_collection.py`
- Create: `tests/test_v1_2_overhead_room_collection_audit.py`
- Create: `evidence/v1-2-overhead-room/contact-sheets/final-overhead-room.webp`
- Create: `evidence/v1-2-overhead-room/final-review.json`
- Modify: `package.json`

**Interfaces:**

- Consumes: reference pack, pose slots, selection, ten finished WebPs, final user review.
- Produces: `validate_collection(reference_pack: dict, pose_manifest: dict, accepted: dict, final_review: dict, project_root: Path) -> None`、npm command `audit:v1-2-overhead-room`、PDF eligibility gate。

- [ ] **Step 1: Write failing collection audit tests**

```python
# tests/test_v1_2_overhead_room_collection_audit.py
import copy
import unittest
from pathlib import Path

from scripts.audit_v1_2_overhead_room_collection import validate_collection
from scripts.v1_2_overhead_room_common import load_json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "source/manifests/v1-2-overhead-room"
FINAL_REVIEW = ROOT / "evidence/v1-2-overhead-room/final-review.json"


class AkariV12OverheadRoomCollectionAuditTest(unittest.TestCase):
    def test_repository_collection_is_pdf_ready(self):
        validate_collection(
            load_json(BASE / "reference-pack.json"),
            load_json(BASE / "pose-slots.json"),
            load_json(BASE / "accepted-selection.json"),
            load_json(FINAL_REVIEW),
            ROOT,
        )

    def test_missing_pose_is_rejected(self):
        accepted = copy.deepcopy(load_json(BASE / "accepted-selection.json"))
        accepted["accepted_works"].pop()
        with self.assertRaisesRegex(ValueError, "ten accepted works"):
            validate_collection(
                load_json(BASE / "reference-pack.json"),
                load_json(BASE / "pose-slots.json"),
                accepted,
                load_json(FINAL_REVIEW),
                ROOT,
            )

    def test_unapproved_final_review_is_rejected(self):
        review = copy.deepcopy(load_json(FINAL_REVIEW))
        review["user_decision"] = "changes_requested"
        with self.assertRaisesRegex(ValueError, "final user approval"):
            validate_collection(
                load_json(BASE / "reference-pack.json"),
                load_json(BASE / "pose-slots.json"),
                load_json(BASE / "accepted-selection.json"),
                review,
                ROOT,
            )
```

- [ ] **Step 2: Run the test and verify the missing module failure**

Run: `uv run python -m unittest tests.test_v1_2_overhead_room_collection_audit -v`

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement the PDF eligibility audit**

Revalidate reference and pose contracts. Require ten canonical poses in order; unique request/review/source/finished paths; exact hashes; RGB 1024x1536 finished assets; 7 full and 3 close roles; final review with exact selection path/hash, final-sheet path/hash, ten poses, `decision: "accepted"`, `user_decision: "approved"`, and all gates:

```python
FINAL_GATES = {
    "identity_consistency",
    "adult_age_consistency",
    "overhead_angle_range",
    "anatomy_and_clothing",
    "outfit_balance",
    "lighting_balance",
    "background_restraint",
    "pose_and_expression_uniqueness",
    "artifact_free",
    "overall_finish",
}
```

The CLI prints `overhead room collection audit: ok` only after all checks pass.

- [ ] **Step 4: Build and inspect the final sheet**

```bash
bash -lc 'npm run build:v1-2-overhead-room:contact-sheet -- --accepted source/manifests/v1-2-overhead-room/accepted-selection.json --output evidence/v1-2-overhead-room/contact-sheets/final-overhead-room.webp'
```

Open all ten finished images and the sheet. Check identity, adult age, ornament, 7:3 framing, outfit balance, angle range, lighting/background, unique roles, anatomy, shorts coverage, and finish.

- [ ] **Step 5: Record final user approval**

Present the sheet. If changes are requested, revise only named poses and rebuild. After approval, write `final-review.json` with current selection and sheet hashes, ten ordered poses, accepted/approved decisions, and all ten gates passing with observations.

- [ ] **Step 6: Add command and run audit**

Add:

```json
"audit:v1-2-overhead-room": "uv run python -m scripts.audit_v1_2_overhead_room_collection"
```

Run:

```bash
uv run python -m unittest tests.test_v1_2_overhead_room_collection_audit -v
bash -lc 'npm run audit:v1-2-overhead-room'
```

Expected: tests PASS and audit reports OK.

- [ ] **Step 7: Commit the PDF-ready gate**

```bash
git add \
  scripts/audit_v1_2_overhead_room_collection.py \
  tests/test_v1_2_overhead_room_collection_audit.py \
  evidence/v1-2-overhead-room/contact-sheets/final-overhead-room.webp \
  evidence/v1-2-overhead-room/final-review.json \
  package.json
git commit -m "feat: approve overhead room portrait collection"
```

### Task 9: Build the Portrait PDF Only After Final Approval

**Files:**

- Create: `scripts/build_v1_2_overhead_room_pdf_manifests.py`
- Create: `tests/test_overhead_room_contract.py`
- Create: three PDF JSON manifests under `source/manifests/v1-2-overhead-room/`
- Create: `tools/pdf/overhead-room-document.mjs`
- Create: `tools/pdf/overhead-room-document.test.mjs`
- Create: `scripts/render_overhead_room_previews.py`
- Create: `scripts/export_overhead_room_pdf.py`
- Create: `scripts/audit_overhead_room_pdf.py`
- Create: `tests/test_overhead_room_pdf_audit.py`
- Modify: `tools/pdf/render.mjs`
- Modify: `tools/pdf/styles.css`
- Modify: `package.json`
- Modify: `README.md`
- Create: `dist/akari-v1.2-overhead-room-portraits.pdf`
- Create: `dist/akari-v1.2-overhead-room-portraits-pages/document.txt`

**Interfaces:**

- Consumes: PDF-eligible selection and approved final review.
- Produces: deterministic PDF manifests, `overheadRoomDocument`, 12 previews, final PDF, searchable text, build/audit commands.

- [ ] **Step 1: Write failing PDF contract tests**

```python
# tests/test_overhead_room_contract.py
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "source/manifests/v1-2-overhead-room"


class OverheadRoomContractTest(unittest.TestCase):
    def test_pdf_manifest_has_cover_ten_artworks_and_colophon(self):
        manifest = json.loads((BASE / "page-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("akari-v1.2-overhead-room-portraits", manifest["document_id"])
        self.assertEqual(12, manifest["page_count"])
        self.assertEqual(list(range(1, 13)), [page["page"] for page in manifest["pages"]])
        artworks = [page for page in manifest["pages"] if page["role"] == "artwork"]
        self.assertEqual(10, len(artworks))
        self.assertTrue(all(len(page["source_inputs"]) == 1 for page in artworks))

    def test_source_and_asset_manifests_cover_all_ten_works(self):
        sources = json.loads((BASE / "source-assets.json").read_text(encoding="utf-8"))["assets"]
        assets = json.loads((BASE / "asset-manifest.json").read_text(encoding="utf-8"))["assets"]
        self.assertEqual(10, len(sources))
        self.assertEqual({item["id"] for item in sources}, {item["id"] for item in assets})
        self.assertTrue(all(item["used_in_final_pdf"] for item in assets))
```

```javascript
// tools/pdf/overhead-room-document.test.mjs
import assert from "node:assert/strict";
import test from "node:test";
import { overheadRoomDocument, pages } from "./overhead-room-document.mjs";

test("overhead room document uses twelve portrait pages", () => {
  assert.equal(pages.length, 12);
  assert.deepEqual(pages.map((page) => page.page), [...Array(12)].map((_, index) => index + 1));
  assert.deepEqual(overheadRoomDocument.pageSize, {
    widthIn: 8,
    heightIn: 12,
    previewWidth: 1024,
    previewHeight: 1536,
  });
});

test("ten artwork pages each carry one accepted source", () => {
  const artworks = pages.filter((page) => page.layout === "overhead-room-artwork");
  assert.equal(artworks.length, 10);
  assert.ok(artworks.every((page) => page.sourceInputs.length === 1));
});
```

- [ ] **Step 2: Run tests and verify missing artifacts**

```bash
uv run python -m unittest tests.test_overhead_room_contract -v
bash -lc 'npm run test:node'
```

Expected: Python fails on missing manifest and Node on missing document module.

- [ ] **Step 3: Implement the gated PDF manifest builder**

Call Task 8's collection validator before writing. Atomically build source-assets, asset-manifest, and page-manifest from the ten selections. Exact pages:

- Page 1: cover, `Akari v1.2 Overhead Room Portraits`, no source.
- Pages 2〜11: canonical works, one source each, title from pose manifest.
- Page 12: colophon, `Collection Notes`, no source.

Cover subtitle: `Ten studies from directly above`. Colophon text: `10 portraits / 7 full views / 3 close views`, `Akari v1.2`, `2026`. Do not show prompts, review notes, source IDs, or production metadata.

Run:

```bash
uv run python -m scripts.build_v1_2_overhead_room_pdf_manifests
uv run python -m unittest tests.test_overhead_room_contract -v
```

Expected: three manifests written and tests PASS.

- [ ] **Step 4: Implement the portrait document and renderer registration**

Validate document ID, 12 pages, role sequence, canonical sources, and one source per artwork. Map cover/colophon to existing `note-list`, artworks to existing `image`; do not add a renderer block type.

```javascript
export const overheadRoomDocument = {
  id: "akari-v1.2-overhead-room-portraits",
  title: "Akari v1.2 Overhead Room Portraits",
  pages,
  sourceManifestPath: "source/manifests/v1-2-overhead-room/source-assets.json",
  assetManifestPath: "source/manifests/v1-2-overhead-room/asset-manifest.json",
  outputPdf: "dist/akari-v1.2-overhead-room-portraits.pdf",
  previewDir: "build/overhead-room-page-previews",
  siteHtml: "build/overhead-room-site/index.html",
  pageSize: { widthIn: 8, heightIn: 12, previewWidth: 1024, previewHeight: 1536 },
};
```

Register `overhead-room` in `render.mjs`. Add scoped cover/artwork/colophon CSS. Artwork images use `object-fit: contain`, source chips are hidden, image area consumes at least 88% page height, and title stays outside pixels.

- [ ] **Step 5: Add wrappers and npm scripts**

Create wrappers using `--document overhead-room`. Add:

```json
"build:overhead-room:previews": "uv run python scripts/render_overhead_room_previews.py",
"build:overhead-room:pdf": "uv run python scripts/export_overhead_room_pdf.py",
"audit:overhead-room:pdf": "uv run python scripts/audit_overhead_room_pdf.py dist/akari-v1.2-overhead-room-portraits.pdf"
```

- [ ] **Step 6: Implement portrait PDF audit and tests**

Use:

```python
EXPECTED_PAGE_COUNT = 12
EXPECTED_RENDER_SIZE = (2304, 3456)
CONTENT_SAMPLE_SIZE = (128, 192)
MIN_CONTENT_RATIO = 0.003
REQUIRED_TEXT = (
    "Akari v1.2 Overhead Room Portraits",
    "Ten studies from directly above",
    "Direct Gaze", "Bent Knees", "Slow Stretch", "Curled Close", "Reach",
    "Quiet Look", "Look Up", "Hair and Eyes", "At Hand", "Sleeved Reach",
    "Collection Notes",
)
```

Require 2:3 page ratio, embedded Unicode fonts, `qpdf --check`, 12 non-blank 2304x3456 renders from `pdftoppm -r 288`, and searchable text saved to the specified dist text path. Tests cover numeric sorting, case-insensitive text, rejection of 16:9, and blank portrait rejection.

- [ ] **Step 7: Build, inspect, export, and audit**

```bash
bash -lc 'npm run build:overhead-room:previews'
bash -lc 'npm run build:overhead-room:pdf'
bash -lc 'npm run audit:overhead-room:pdf'
```

Expected: 12 exact previews, final PDF, extracted text, and `overhead room pdf audit: ok`. Open all previews and rendered pages; reject crop, stretch, source IDs, prompts, review text, blank pages, or title overlap.

- [ ] **Step 8: Update README and run complete verification**

Add the new PDF to README deliverables, then run:

```bash
bash -lc 'npm run test:node && npm run test:python && npm run audit'
bash -lc 'npm run audit:v1-2-overhead-room && npm run audit:overhead-room:pdf'
bash -lc 'npm run lint:md'
git diff --check
git status --short
```

Expected: all suites and audits PASS, Markdown lint has 0 errors, no whitespace errors, candidates/batch sheets remain ignored.

- [ ] **Step 9: Commit the final pipeline and deliverable**

```bash
git add \
  scripts/build_v1_2_overhead_room_pdf_manifests.py \
  scripts/render_overhead_room_previews.py \
  scripts/export_overhead_room_pdf.py \
  scripts/audit_overhead_room_pdf.py \
  tests/test_overhead_room_contract.py \
  tests/test_overhead_room_pdf_audit.py \
  tools/pdf/overhead-room-document.mjs \
  tools/pdf/overhead-room-document.test.mjs \
  tools/pdf/render.mjs tools/pdf/styles.css \
  source/manifests/v1-2-overhead-room/source-assets.json \
  source/manifests/v1-2-overhead-room/asset-manifest.json \
  source/manifests/v1-2-overhead-room/page-manifest.json \
  dist/akari-v1.2-overhead-room-portraits.pdf \
  dist/akari-v1.2-overhead-room-portraits-pages/document.txt \
  package.json README.md
git commit -m "feat: publish overhead room portrait book"
```

Run `git status --short` again. Do not claim completion if a tracked change is unexplained or an audit was skipped.
