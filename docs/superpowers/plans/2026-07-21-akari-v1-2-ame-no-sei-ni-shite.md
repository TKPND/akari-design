# あかり v1.2 画集『雨のせいにして』実装計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** 恋人になった後のあかりとたかひろが、雨で予定を変えた一日を
完全 POV の 12 場面で描く、A4 横 18 ページの独立画集 PDF を制作する。

**Architecture:** Core と Daily を変更せず、
`akari-v1.2/artbooks/ame-no-sei-ni-shite/` に manifest、候補レビュー、採用画像、
比較シート、PDF、checksum を閉じ込める。Python の専用ライフサイクル検証と
比較シート生成、既存 Node/Playwright PDF renderer の専用 document model、
Python の専用 release audit を順に追加する。画像は Scene 01 と Scene 08 を
衣装 anchor として先に承認し、残りを場面順に生成・選定する。

**Tech Stack:** Python 3、PyYAML、Pillow、Node ESM、Playwright/Chrome、
Poppler、qpdf、既存 npm gate、OpenAI image generation。

## Global Constraints

- 用紙は A4 横、本文画像は 3:2 横長、最低寸法は 1536 x 1024 px とする。
- 本文画像は 12 枚、総ページ数は 18 ページとする。
- 画像内に台詞、題名、ロゴ、ページ番号、透かしを生成しない。
- 台詞は PDF レイアウトで 1 場面につき 0 行または 1 行だけ配置する。
- 全場面をたかひろの実在可能な完全 POV とし、Scene 12 の袖端以外は
  たかひろの顔、身体、手、反射、影を描かない。
- あかりは全場面で同じ 25 歳の成人女性、短い暖色ブラウンのボブ、
  character-left の平行ピンと淡いブルーの小リボン、健康的でしっかりした脚、
  コンパクトなアニメ等身を維持する。
- Scene 01-07 は承認済み Scene 01 を屋外衣装 anchor、Scene 08-12 は承認済み
  Scene 08 を室内衣装 anchor とし、どちらも Core identity 参照と併用する。
- Scene N を Scene N+1 の唯一の参照にせず、世代ごとの identity 漂流を防ぐ。
- 初回は各場面 2 候補を生成し、2 ラウンド連続で Blocker が残った時だけ
  構図または動作を簡略化する。identity 条件は弱めない。
- `akari-v1.2/release/akari-v1.2-core-settings.pdf`、Core accepted 画像、
  Daily accepted 画像のバイト列を変更しない。
- `source/candidates/` と生成 contact sheet は git 管理外とし、最終成果物の
  commit 範囲はユーザー承認後に決める。
- 既存の無関係な untracked ディレクトリは変更、削除、stage しない。
- Chromium、PDF build、Poppler、OCR 相当の重い処理は直列に実行する。

---

## 承認済み入力

- 設計書:
  `docs/superpowers/specs/2026-07-21-akari-v1-2-ame-no-sei-ni-shite-design.md`
- 画集 ID: `akari-v1.2-ame-no-sei-ni-shite`
- package root: `akari-v1.2/artbooks/ame-no-sei-ni-shite/`
- release PDF:
  `akari-v1.2/artbooks/ame-no-sei-ni-shite/release/akari-v1.2-ame-no-sei-ni-shite.pdf`
- Scene 01-07 屋外衣装: 白トップス、淡いベージュまたはライトグレーの
  カーディガン、グレーのプリーツスカート、白地に淡いブルー二本線の靴下、
  白いチャンキースニーカー、小さな淡色ショルダーバッグ。
- Scene 08-12 室内衣装: ゆるい白い半袖 T シャツ、グレーのルームショーツ、
  白地に淡いブルー二本線の靴下、靴なし。

## 固定する Core 参照

| role | path | SHA-256 |
| --- | --- | --- |
| `core-standing-body` | `akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png` | `a977f2798d15f3da9ef0d7720d6f9fc41bd2f84f54f4c8a69908a482596a75c5` |
| `core-hairpin-side` | `akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png` | `19c8c96113bcbc47f7d1e4cc1d58af466d3a573f0dae40cfcdf9bf456b1a0a9b` |
| `core-seated-body` | `akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png` | `7289ca0d9cbc74b4f1becb949dcf174fdd691af08d19f185de47d7657c1d7c64` |
| `core-front-hair` | `akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png` | `4aae292203b389b7ab1f1a44171ec5cf45498843705d7dbefbc47f4452ac8ffa` |
| `core-soft-smile` | `akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-4_soft-smile_r01.png` | `7db1ea102a95d45d16e66a7390642d1ceb958ef631af072c40af87b2ee0b71d6` |
| `core-standing-feet` | `akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-standing_r01.png` | `57b6d32d00ef10222abcca3664addeb72d514ec1cb772eb9fcae6c657ce7cca4` |
| `core-seated-feet` | `akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-seated_r01.png` | `46c812d0f10e2c9df0a7904687ec38939645b4636037dfd537437d1232967d27` |

## 対象ファイル構成

```text
akari-v1.2/artbooks/ame-no-sei-ni-shite/
├── README.md
├── manifest/
│   ├── book.yaml
│   ├── continuity.yaml
│   └── scenes/index.yaml
├── source/candidates/<scene-id>/<revision>/*.png
├── accepted/scene-01.png ... scene-12.png
├── evidence/
│   ├── reviews/scene-01.yaml ... scene-12.yaml
│   ├── reviews/act-1.yaml ... act-4.yaml
│   ├── reviews/full-continuity.yaml
│   └── contact-sheets/
│       ├── act-1.webp ... act-4.webp
│       └── full-continuity.webp
└── release/
    ├── akari-v1.2-ame-no-sei-ni-shite.pdf
    └── checksums.txt
scripts/akari_v1_2_ame_no_sei_ni_shite.py
scripts/build_ame_no_sei_ni_shite_contact_sheet.py
scripts/export_ame_no_sei_ni_shite_pdf.py
scripts/audit_ame_no_sei_ni_shite_pdf.py
tests/test_ame_no_sei_ni_shite_contract.py
tests/test_build_ame_no_sei_ni_shite_contact_sheet.py
tests/test_ame_no_sei_ni_shite_pdf_audit.py
tools/pdf/ame-no-sei-ni-shite-document.mjs
tools/pdf/ame-no-sei-ni-shite-document.test.mjs
```

## 共通ライフサイクル interface

全画像タスクは Task 1 と Task 2 が作る次の CLI を使う。

```text
python scripts/akari_v1_2_ame_no_sei_ni_shite.py validate
python scripts/akari_v1_2_ame_no_sei_ni_shite.py prompt --scene scene-01
python scripts/akari_v1_2_ame_no_sei_ni_shite.py promote \
  --scene scene-01 --revision r01 --variant a \
  --review evidence/reviews/scene-01.yaml
python scripts/akari_v1_2_ame_no_sei_ni_shite.py approve-act \
  --act 1 --review evidence/reviews/act-1.yaml
python scripts/akari_v1_2_ame_no_sei_ni_shite.py validate-act --act 1
python scripts/akari_v1_2_ame_no_sei_ni_shite.py approve-full \
  --review evidence/reviews/full-continuity.yaml
python scripts/build_ame_no_sei_ni_shite_contact_sheet.py \
  --scope candidates --scene scene-01
python scripts/build_ame_no_sei_ni_shite_contact_sheet.py \
  --scope act --act 1
python scripts/build_ame_no_sei_ni_shite_contact_sheet.py \
  --scope all-acts
python scripts/build_ame_no_sei_ni_shite_contact_sheet.py \
  --scope full
```

`prompt` は標準出力へ完成 prompt と参照 path/role を出す。`promote` は review が
`accepted`、Blocker/Major が 0 件、選択候補が 3:2 かつ最低 1536 x 1024 の時だけ
`accepted/scene-NN.png` へ byte copy し、scene manifest の lifecycle と SHA-256 を
更新する。

### Task 1: 画集 package contract と軽量 edit gate

**Files:**

- Create: `akari-v1.2/artbooks/ame-no-sei-ni-shite/README.md`
- Create: `akari-v1.2/artbooks/ame-no-sei-ni-shite/manifest/book.yaml`
- Create: `akari-v1.2/artbooks/ame-no-sei-ni-shite/manifest/continuity.yaml`
- Create: `akari-v1.2/artbooks/ame-no-sei-ni-shite/manifest/scenes/index.yaml`
- Create: `scripts/akari_v1_2_ame_no_sei_ni_shite.py`
- Create: `tests/test_ame_no_sei_ni_shite_contract.py`
- Modify: `.gitignore`
- Modify: `package.json`

**Interfaces:**

- Consumes: 承認済み設計書と固定 Core 参照。
- Produces: `load_contract(root: Path) -> dict`、
  `validate_contract(root: Path, require_release: bool = False) -> None`、
  `render_scene_prompt(contract: dict, scene_id: str) -> str`、
  `sha256_file(path: Path) -> str`。

- [ ] **Step 1: package contract の failing test を書く**

`tests/test_ame_no_sei_ni_shite_contract.py` に、次の契約を実装する。

```python
class AmeNoSeiNiShiteContractTest(unittest.TestCase):
    def test_book_contract(self):
        contract = load_contract(ROOT)
        self.assertEqual("akari-v1.2-ame-no-sei-ni-shite", contract["book"]["book_id"])
        self.assertEqual(18, contract["book"]["page_count"])
        self.assertEqual({"width": 1536, "height": 1024}, contract["book"]["minimum_image"])
        self.assertEqual(list(range(1, 19)), [p["page"] for p in contract["book"]["pages"]])

    def test_scene_order_and_dialogue_limit(self):
        scenes = load_contract(ROOT)["scenes"]
        self.assertEqual([f"scene-{n:02d}" for n in range(1, 13)], [s["id"] for s in scenes])
        self.assertTrue(all(len(s["dialogue"]) <= 1 for s in scenes))

    def test_planned_scene_paths_are_canonical(self):
        for scene in load_contract(ROOT)["scenes"]:
            self.assertEqual(
                [
                    f"source/candidates/{scene['id']}/r01/{scene['id']}-r01-a.png",
                    f"source/candidates/{scene['id']}/r01/{scene['id']}-r01-b.png",
                ],
                [item["path"] for item in scene["candidates"]],
            )

    def test_core_reference_hashes_are_pinned(self):
        contract = load_contract(ROOT)
        for ref in contract["continuity"]["core_references"]:
            self.assertEqual(ref["sha256"], sha256_file(ROOT / ref["path"]))

    def test_scene_prompt_contains_global_pov_and_production_bans(self):
        prompt = render_scene_prompt(load_contract(ROOT), "scene-12").lower()
        for phrase in (
            "25-year-old adult akari",
            "physically possible first-person point of view",
            "no viewer face, body, hand, reflection, or shadow",
            "only the edge of viewer's sleeve",
            "no readable text, logo, watermark, collage, or grid",
        ):
            self.assertIn(phrase, prompt)
```

- [ ] **Step 2: focused test が missing module で失敗することを確認する**

Run:

```bash
uv run python -m unittest tests.test_ame_no_sei_ni_shite_contract -v
```

Expected: `ModuleNotFoundError` または package manifest missing で FAIL。

- [ ] **Step 3: book、continuity、scene contract を作る**

`book.yaml` は次の固定値を持たせる。

```yaml
schema_version: 1
book_id: akari-v1.2-ame-no-sei-ni-shite
title: 雨のせいにして
version: 1.0.0
page_size: {name: A4-landscape, width_in: 11.69, height_in: 8.27}
preview_size: {width: 3508, height: 2480}
minimum_image: {width: 1536, height: 1024}
page_count: 18
release_pdf: release/akari-v1.2-ame-no-sei-ni-shite.pdf
pages:
  - {page: 1, id: cover, layout: artbook-cover, source: scene-06, crop: cover}
  - {page: 2, id: first-rain-detail, layout: artbook-detail, source: scene-03, crop: rain-detail}
  - {page: 3, id: title, layout: artbook-title, source: null, crop: null}
  - {page: 4, id: scene-01, layout: artbook-scene, source: scene-01, crop: full}
  - {page: 5, id: scene-02, layout: artbook-scene, source: scene-02, crop: full}
  - {page: 6, id: scene-03, layout: artbook-scene, source: scene-03, crop: full}
  - {page: 7, id: scene-04, layout: artbook-scene, source: scene-04, crop: full}
  - {page: 8, id: scene-05, layout: artbook-scene, source: scene-05, crop: full}
  - {page: 9, id: scene-06, layout: artbook-scene, source: scene-06, crop: full}
  - {page: 10, id: scene-07, layout: artbook-scene, source: scene-07, crop: full}
  - {page: 11, id: scene-08, layout: artbook-scene, source: scene-08, crop: full}
  - {page: 12, id: scene-09, layout: artbook-scene, source: scene-09, crop: full}
  - {page: 13, id: scene-10, layout: artbook-scene, source: scene-10, crop: full}
  - {page: 14, id: scene-11, layout: artbook-scene, source: scene-11, crop: full}
  - {page: 15, id: scene-12, layout: artbook-scene, source: scene-12, crop: full}
  - {page: 16, id: afterimage, layout: artbook-afterimage, source: scene-12, crop: afterimage}
  - {page: 17, id: colophon, layout: artbook-colophon, source: null, crop: null}
  - {page: 18, id: back-cover, layout: artbook-back, source: null, crop: null}
```

`continuity.yaml` は固定 Core 参照表、完全 POV 契約、屋外/室内衣装、Scene ごとの
濡れ方、Act ごとの光、review 順序、Blocker 一覧を設計書の順序どおり収録する。
Core 参照の path と SHA-256 は本計画の「固定する Core 参照」表をそのまま使う。
衣装は prompt composer が直接使える次の値にする。

```yaml
outfits:
  outdoor:
    scenes: [scene-01, scene-02, scene-03, scene-04, scene-05, scene-06, scene-07]
    prompt: "white top, pale beige or light-gray cardigan, gray pleated skirt, warm-white mid-calf socks with exactly two thin pale-blue stripes, white chunky sneakers, and one small pale shoulder bag"
  indoor:
    scenes: [scene-08, scene-09, scene-10, scene-11, scene-12]
    prompt: "loose opaque white short-sleeve T-shirt, simple opaque gray room shorts, warm-white mid-calf socks with exactly two thin pale-blue stripes, and no shoes or slippers"
```

さらに、生成時に manifest から参照役割を再現できるよう、次の exact mapping を
`reference_sets` として収録する。`outdoor-look-anchor` と
`indoor-look-anchor` の SHA-256 は、それぞれ Scene 01 と Scene 08 の accepted
lifecycle から解決する。

```yaml
reference_sets:
  scene-01: [core-standing-body, core-hairpin-side, core-soft-smile]
  scene-02: [outdoor-look-anchor, core-standing-body, core-hairpin-side]
  scene-03: [outdoor-look-anchor, core-standing-body, core-hairpin-side, core-front-hair, core-soft-smile]
  scene-04: [outdoor-look-anchor, core-standing-body, core-hairpin-side]
  scene-05: [outdoor-look-anchor, core-hairpin-side, core-front-hair, core-soft-smile]
  scene-06: [outdoor-look-anchor, core-hairpin-side, core-front-hair, core-soft-smile]
  scene-07: [outdoor-look-anchor, core-standing-body, core-hairpin-side, core-standing-feet]
  scene-08: [core-standing-body, core-hairpin-side, core-front-hair, core-soft-smile, core-standing-feet]
  scene-09: [indoor-look-anchor, core-hairpin-side, core-front-hair, core-soft-smile, core-standing-feet]
  scene-10: [indoor-look-anchor, core-seated-body, core-hairpin-side, core-front-hair, core-soft-smile, core-seated-feet]
  scene-11: [indoor-look-anchor, core-standing-body, core-hairpin-side, core-soft-smile]
  scene-12: [indoor-look-anchor, core-standing-body, core-hairpin-side, core-front-hair, core-soft-smile, core-standing-feet]
```

`manifest/scenes/index.yaml` の `scenes` は次の exact scene rows を持たせる。

```yaml
schema_version: 1
scenes:
  - {id: scene-01, act: 1, time: "10:02", slug: invitation-at-door, action: "open door; Akari waits beyond it and invites the viewer out", composition: "physically possible standing POV; knee-up Akari beyond the open door", emotion: "expectation she cannot fully hide", wetness: dry, lighting: bright-warm-overcast, dialogue: ["遅い。ほら、行こ"]}
  - {id: scene-02, act: 1, time: "10:24", slug: half-step-ahead, action: "Akari walks half a step ahead and looks back", composition: "walking eye-level POV; near-full-body middle distance", emotion: "easy anticipation", wetness: dry, lighting: bright-warm-overcast, dialogue: []}
  - {id: scene-03, act: 1, time: "10:41", slug: first-raindrops, action: "Akari turns one palm upward, checks the sky, then looks back", composition: "eye-level POV; raised palm readable without hiding her face", emotion: "small shared surprise", wetness: first-drops, lighting: overcast-shifting-blue-gray, dialogue: ["うそ。降るって言ってた？"]}
  - {id: scene-04, act: 2, time: "10:46", slug: reach-and-run, action: "Akari reaches toward the camera and starts running for shelter", composition: "reaching hand in foreground; moving body in middle distance; hand does not touch lens", emotion: "urgent but playful first contact", wetness: light-rain, lighting: blue-gray-rain, dialogue: ["たかひろ、こっち！"]}
  - {id: scene-05, act: 2, time: "10:52", slug: one-umbrella, action: "under the eaves Akari wipes damp hair and finds one folding umbrella in her bag", composition: "eye-level close middle shot; umbrella, bag, wet hair and face all readable", emotion: "laughing together at the changed plan", wetness: clearly-wet, lighting: sheltered-blue-gray-rain, dialogue: ["一本しかないけど、まあいっか"]}
  - {id: scene-06, act: 2, time: "11:06", slug: shared-umbrella, action: "Akari walks beside the viewer under one small umbrella and looks slightly up", composition: "very close physically possible shared-umbrella POV; shoulders almost touching", emotion: "comfortable closeness created by rain", wetness: damp-stable, lighting: soft-blue-gray-under-umbrella, dialogue: []}
  - {id: scene-07, act: 2, time: "11:28", slug: returned-entryway, action: "inside the viewer's entryway Akari turns back beside wet shoes and the closed umbrella", composition: "slightly lowered entryway POV; full footwear and umbrella remain readable", emotion: "amused acceptance that they came back", wetness: damp-entryway, lighting: cool-entry-warm-interior, dialogue: ["……帰ってきちゃったね"]}
  - {id: scene-08, act: 3, time: "12:03", slug: roomwear-and-two-mugs, action: "after changing next door Akari returns through the door holding two mugs", composition: "standing eye-level POV; knee-up Akari, both mugs and dry roomwear readable", emotion: "quiet decision to spend the day together", wetness: towel-dried-ends, lighting: cool-window-warm-room, dialogue: ["今日はもう、ここでいいでしょ"]}
  - {id: scene-09, act: 3, time: "13:17", slug: rain-window, action: "Akari rests beside two drinks and watches rain at the window", composition: "seated or standing eye-level POV; broad negative space around profile and rain window", emotion: "silence already feels safe", wetness: drying-soft-bob, lighting: cool-window-warm-room, dialogue: []}
  - {id: scene-10, act: 3, time: "15:42", slug: sleepy-movie, action: "during a movie Akari hides her sleepiness and looks toward the viewer", composition: "closest physical POV of the book from adjacent sofa or floor seating; no screen content", emotion: "sleepy trust with a small defensive glance", wetness: dry, lighting: dim-cool-window-warm-room, dialogue: ["……見てるってば"]}
  - {id: scene-11, act: 4, time: "18:31", slug: rain-cleared, action: "Akari looks at the cleared sky, then turns toward the viewer", composition: "eye-level POV with window and rain-cleared dusk both readable", emotion: "she notices the day is ending", wetness: dry, lighting: rain-cleared-soft-sunset, dialogue: ["雨、やんだね"]}
  - {id: scene-12, act: 4, time: "21:08", slug: sleeve-at-door, action: "at the night doorway Akari catches only the edge of the viewer's sleeve and looks up", composition: "physically possible standing POV; doorway, corridor, her hand, expression, and tiny sleeve edge readable", emotion: "emotional closest point; honest reluctance to part", wetness: dry, lighting: warm-night-corridor, dialogue: ["……もう少しだけ、ここにいていい？"]}
```

各 row に実装時に次の lifecycle fields を追加する。

```yaml
revision: r01
status: planned
candidates:
  - {variant: a, path: source/candidates/scene-NN/r01/scene-NN-r01-a.png}
  - {variant: b, path: source/candidates/scene-NN/r01/scene-NN-r01-b.png}
accepted_path: null
accepted_sha256: null
review_path: null
```

`scene-NN` は各 row 自身の `id` を使い、生成された index.yaml にはリテラルの
`scene-NN` を残さない。

- [ ] **Step 4: validator と prompt composer の最小実装を書く**

`scripts/akari_v1_2_ame_no_sei_ni_shite.py` は次の規則を実装する。

```python
PACKAGE = Path("akari-v1.2/artbooks/ame-no-sei-ni-shite")
SCENE_RE = re.compile(r"^scene-(0[1-9]|1[0-2])$")
VALID_STATUSES = {"planned", "candidate", "review", "accepted", "rejected", "superseded"}
REVIEW_ORDER = ("identity", "hair", "pov", "continuity", "body", "emotion", "rendering", "production")

def render_scene_prompt(contract: dict, scene_id: str) -> str:
    scene = next(item for item in contract["scenes"] if item["id"] == scene_id)
    outfit_key = "outdoor" if scene["act"] <= 2 else "indoor"
    outfit = contract["continuity"]["outfits"][outfit_key]
    sleeve = (
        "Only the edge of the viewer's sleeve may appear at the bottom of the frame. "
        if scene_id == "scene-12" else ""
    )
    return " ".join((
        "Create one 3:2 landscape illustration at 1536 by 1024 or larger.",
        "Show the same naturally cute 25-year-old adult Akari from the pinned Core references.",
        "Keep her warm-brown short bob, character-left parallel pins and pale-blue small ribbon, round face, warm-brown eyes, compact anime proportions, and healthy substantial legs.",
        f"Scene action: {scene['action']}.",
        f"Composition: {scene['composition']}.",
        f"Emotion: {scene['emotion']}.",
        f"Wetness state: {scene['wetness']}. Lighting: {scene['lighting']}.",
        f"Outfit: {outfit['prompt']}.",
        "Use a physically possible first-person point of view belonging to the viewer.",
        sleeve,
        "No viewer face, body, hand, reflection, or shadow.",
        "No readable text, logo, watermark, collage, or grid. One scene, one time, one outfit.",
    ))
```

CLI の `prompt` は完成 prompt に続けて `reference_sets[scene_id]` の role、path、
SHA-256 を出力する。validator は top-level key、12 scene 順、
Act 1=`01-03`、Act 2=`04-07`、
Act 3=`08-10`、Act 4=`11-12`、dialogue 長、candidate canonical path、参照 SHA、
accepted lifecycle、PNG format、3:2、最低寸法を検査する。`planned` の時だけ
accepted/review が null でよく、`accepted` の時は両 path と accepted SHA を必須にする。

- [ ] **Step 5: ignore と npm scripts を追加する**

`.gitignore` に次を追加する。

```gitignore
akari-v1.2/artbooks/ame-no-sei-ni-shite/source/candidates/
akari-v1.2/artbooks/ame-no-sei-ni-shite/evidence/contact-sheets/
```

`package.json` に次を追加する。

```json
"test:python:ame-no-sei-ni-shite": "uv run python -m unittest tests.test_ame_no_sei_ni_shite_contract -v",
"validate:ame-no-sei-ni-shite": "uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py validate",
"gate:edit:ame-no-sei-ni-shite": "npm run test:python:ame-no-sei-ni-shite && npm run validate:ame-no-sei-ni-shite && npm run verify:v1-2:release-pins"
```

- [ ] **Step 6: 軽量 gate を通す**

Run:

```bash
npm run gate:edit:ame-no-sei-ni-shite
```

Expected: artbook tests、contract validation、既存 v1.2 release pins がすべて PASS。

- [ ] **Step 7: package contract を commit する**

```bash
git add .gitignore package.json \
  akari-v1.2/artbooks/ame-no-sei-ni-shite/README.md \
  akari-v1.2/artbooks/ame-no-sei-ni-shite/manifest \
  scripts/akari_v1_2_ame_no_sei_ni_shite.py \
  tests/test_ame_no_sei_ni_shite_contract.py
git commit -m "feat: add rain-day artbook contract"
```

### Task 2: 候補比較、review、promotion tooling

**Files:**

- Modify: `scripts/akari_v1_2_ame_no_sei_ni_shite.py`
- Create: `scripts/build_ame_no_sei_ni_shite_contact_sheet.py`
- Create: `tests/test_build_ame_no_sei_ni_shite_contact_sheet.py`
- Modify: `tests/test_ame_no_sei_ni_shite_contract.py`
- Modify: `package.json`

**Interfaces:**

- Consumes: Task 1 の scene lifecycle と `render_scene_prompt()`。
- Produces: `promote_scene(...) -> Path`、`build_candidate_sheet(...) -> Path`、
  `build_act_sheet(...) -> Path`、`build_full_sheet(...) -> Path`、
  `approve_act(...) -> Path`、`validate_act(...) -> None`、
  `approve_full(...) -> Path`。

- [ ] **Step 1: promotion と sheet の failing tests を書く**

```python
def test_promotion_requires_accepted_review(self):
    with self.assertRaisesRegex(ValidationError, "review status must be accepted"):
        promote_scene(self.root, "scene-01", "r01", "a", self.review_path)

def test_candidate_sheet_uses_declared_a_b_order(self):
    output = build_candidate_sheet(self.root, "scene-01")
    self.assertTrue(output.is_file())
    self.assertEqual("scene-01-r01-candidates.webp", output.name)

def test_full_sheet_requires_twelve_accepted_scenes(self):
    with self.assertRaisesRegex(ValueError, "12 accepted scenes required"):
        build_full_sheet(self.root)

def test_act_approval_pins_contact_sheet_hash(self):
    review = approve_act(self.root, 1, self.review_path)
    data = yaml.safe_load(review.read_text(encoding="utf-8"))
    self.assertRegex(data["contact_sheet_sha256"], r"^[0-9a-f]{64}$")
```

- [ ] **Step 2: tests が missing functions で失敗することを確認する**

Run:

```bash
uv run python -m unittest \
  tests.test_ame_no_sei_ni_shite_contract \
  tests.test_build_ame_no_sei_ni_shite_contact_sheet -v
```

Expected: `promote_scene` または sheet builder が未定義で FAIL。

- [ ] **Step 3: review schema と promotion を実装する**

review YAML の exact contract は次とする。

```yaml
schema_version: 1
scene_id: scene-01
revision: r01
status: accepted
selected_variant: a
findings: []
selection_reason: "Candidate A best preserves adult identity, POV, continuity, anatomy, emotion, and rendering."
reference_roles_confirmed: [core-standing-body, core-hairpin-side, core-soft-smile]
```

`findings` item は
`{severity: blocker|major|minor, category: identity|hair|pov|continuity|body|emotion|rendering|production, note: string}`
だけを許可する。`accepted` は blocker/major 0 件、`accepted-with-notes` は minor のみ、
`rejected` は blocker または major を 1 件以上必須とする。

promotion は候補を Pillow で検証して byte copy し、manifest の status、
accepted path、SHA-256、review path を更新し、final review YAML へ実行時の
RFC 3339 timestamp を `reviewed_at` として書き込む。既存 accepted がある場合は
`--replace` なしで拒否し、暗黙上書きをしない。

Act review draft は次の contract とする。ユーザー承認後に実行する `approve-act` が
status を `accepted` へ変え、deterministic contact sheet の SHA-256 と実行時の
RFC 3339 timestamp を追加する。全 check が `pass`、Blocker/Major が 0 件の時だけ
確定する。

```yaml
schema_version: 1
scope: act-1
status: review
checks:
  accepted_scene_count: pass
  outfit_and_ornament: pass
  wetness_order: pass
  light_order: pass
  core_bytes_unchanged: pass
findings: []
```

`validate-act --act N` は該当 Act の accepted 数、accepted/review link、衣装 key、
wetness と light の宣言順、contact sheet の再計算 SHA、Act review、Core pins を検査する。

- [ ] **Step 4: candidate、Act、full sheet builder を実装する**

Pillow で次の固定グリッドを作る。`--scope all-acts` は Act 1、2、3、4 を
順番に生成する shortcut とし、並列実行しない。

```python
SCOPE_LAYOUTS = {
    "candidates": {"columns": 2, "thumb": (768, 512)},
    "act-1": {"columns": 3, "thumb": (576, 384)},
    "act-2": {"columns": 2, "thumb": (672, 448)},
    "act-3": {"columns": 3, "thumb": (576, 384)},
    "act-4": {"columns": 2, "thumb": (768, 512)},
    "full": {"columns": 3, "thumb": (512, 341)},
}
```

各 tile 下へ scene id、時刻、wetness、lighting、accepted SHA 先頭 12 文字を描く。
候補 sheet は A/B の declared order、Act/full は scene id の時系列順を強制する。

- [ ] **Step 5: sheet scripts を package.json に追加する**

```json
"build:ame-no-sei-ni-shite:contact-sheet": "uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py",
"test:python:ame-no-sei-ni-shite": "uv run python -m unittest tests.test_ame_no_sei_ni_shite_contract tests.test_build_ame_no_sei_ni_shite_contact_sheet -v"
```

- [ ] **Step 6: tooling tests と edit gate を通す**

Run:

```bash
npm run gate:edit:ame-no-sei-ni-shite
```

Expected: PASS。候補画像がまだない状態でも `validate` は planned lifecycle を許可する。

- [ ] **Step 7: tooling を commit する**

```bash
git add package.json scripts/akari_v1_2_ame_no_sei_ni_shite.py \
  scripts/build_ame_no_sei_ni_shite_contact_sheet.py \
  tests/test_ame_no_sei_ni_shite_contract.py \
  tests/test_build_ame_no_sei_ni_shite_contact_sheet.py
git commit -m "feat: add rain-day artbook review tooling"
```

### Task 3: Scene 01 屋外 look anchor

**Files:**

- Create ignored: `akari-v1.2/artbooks/ame-no-sei-ni-shite/source/candidates/scene-01/r01/scene-01-r01-a.png`
- Create ignored: `akari-v1.2/artbooks/ame-no-sei-ni-shite/source/candidates/scene-01/r01/scene-01-r01-b.png`
- Create: `akari-v1.2/artbooks/ame-no-sei-ni-shite/evidence/reviews/scene-01.yaml`
- Create: `akari-v1.2/artbooks/ame-no-sei-ni-shite/accepted/scene-01.png`
- Modify: `akari-v1.2/artbooks/ame-no-sei-ni-shite/manifest/scenes/index.yaml`

**Interfaces:**

- Consumes: `core-standing-body`、`core-hairpin-side`、`core-soft-smile`。
- Produces: Scene 02-07 が Core と併用する `outdoor-look-anchor`。

- [ ] **Step 1: 3 枚の参照を `view_image` で開く**

役割は C01=成人体型、C03=髪飾り側と 45 度 identity、C06-4=顔と自然な期待感。
参照を開かずに text-only 生成へ進まない。

- [ ] **Step 2: 完成 prompt を取得して A/B を独立生成する**

Run:

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py prompt --scene scene-01
```

画像生成では 3 枚を同時参照し、同じ prompt から候補 A と B を独立生成する。
出力は declared candidate path へ PNG で保存する。B に A を参照させない。

- [ ] **Step 3: candidate sheet を作り、順序どおり review する**

Run:

```bash
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py \
  --scope candidates --scene scene-01
```

identity、hair、POV、continuity、body、emotion、rendering、production の順で確認し、
屋外衣装、乾いた髪、開いた扉、膝上、期待の表情が最も強い候補を選ぶ。

- [ ] **Step 4: review を記録し promotion する**

Run with the selected literal variant `a` or `b`:

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py promote \
  --scene scene-01 --revision r01 --variant a \
  --review evidence/reviews/scene-01.yaml
npm run gate:edit:ame-no-sei-ni-shite
```

Expected: `accepted/scene-01.png` が存在し、scene-01 lifecycle が `accepted`。

- [ ] **Step 5: ユーザー承認 checkpoint を取る**

Scene 01 と候補比較を提示し、屋外 look anchor として明示承認を受ける。
承認前に Scene 02-07 を最終承認しない。

### Task 4: Scene 08 室内 look anchor

**Files:**

- Create ignored: `akari-v1.2/artbooks/ame-no-sei-ni-shite/source/candidates/scene-08/r01/scene-08-r01-a.png`
- Create ignored: `akari-v1.2/artbooks/ame-no-sei-ni-shite/source/candidates/scene-08/r01/scene-08-r01-b.png`
- Create: `akari-v1.2/artbooks/ame-no-sei-ni-shite/evidence/reviews/scene-08.yaml`
- Create: `akari-v1.2/artbooks/ame-no-sei-ni-shite/accepted/scene-08.png`
- Modify: `akari-v1.2/artbooks/ame-no-sei-ni-shite/manifest/scenes/index.yaml`

**Interfaces:**

- Consumes: `core-standing-body`、`core-hairpin-side`、`core-soft-smile`、
  `core-standing-feet`。
- Produces: Scene 09-12 が Core と併用する `indoor-look-anchor`。

- [ ] **Step 1: 5 枚の参照を `view_image` で開く**

C01=体型、C03=髪飾り側、C05=正面寄りの顔と髪の構造、C06-4=自然な顔、
C07 standing=二本線靴下と靴なし足元。C05 は顔と髪の構造だけを参照し、
寝ぐせ状態は Scene 08 へ持ち込まない。

- [ ] **Step 2: A/B を独立生成する**

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py prompt --scene scene-08
```

室内衣装が乾いていること、毛先だけ少し湿っていること、髪飾りを付け直していること、
二つのマグを自然に持つこと、扉越しの完全 POV を prompt output と目視で確認する。

- [ ] **Step 3: 比較、review、promotion を行う**

```bash
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py \
  --scope candidates --scene scene-08
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py promote \
  --scene scene-08 --revision r01 --variant a \
  --review evidence/reviews/scene-08.yaml
npm run gate:edit:ame-no-sei-ni-shite
```

Expected: `accepted/scene-08.png` が存在し、濡れた室内衣装、靴、片方だけのマグ、
余分な手指、左右反転した髪飾りがない。

- [ ] **Step 4: ユーザー承認 checkpoint を取る**

Scene 08 と候補比較を提示し、室内 look anchor として明示承認を受ける。

### Task 5: Act 1 の Scene 02-03 と連続性 review

**Files:**

- Create ignored: Scene 02-03 の r01 A/B candidates。
- Create: `evidence/reviews/scene-02.yaml`、`evidence/reviews/scene-03.yaml`
  （package root 基準）。
- Create: `accepted/scene-02.png`、`accepted/scene-03.png`
  （package root 基準）。
- Create ignored: `evidence/contact-sheets/act-1.webp`（package root 基準）。
- Modify: `manifest/scenes/index.yaml`（package root 基準）。

**Interfaces:**

- Consumes: Core refs と Scene 01 `outdoor-look-anchor`。
- Produces: 乾いた朝から最初の雨粒までの承認済み Act 1。

- [ ] **Step 1: Scene 02 の参照を開き、A/B を生成・選定・promotion する**

参照は Scene 01、C01、C03。半歩先の歩行、振り返り、乾いた衣装、明るい曇りを確認する。

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py prompt --scene scene-02
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope candidates --scene scene-02
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py promote --scene scene-02 --revision r01 --variant a --review evidence/reviews/scene-02.yaml
```

- [ ] **Step 2: Scene 03 の参照を開き、A/B を生成・選定・promotion する**

参照は Scene 01、C01、C03、C05、C06-4。C05 は正面寄りの顔と髪の構造だけに使い、
寝ぐせは持ち込まない。手のひら、最初の雨粒、顔、髪、肩のごく軽い濡れを確認する。

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py prompt --scene scene-03
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope candidates --scene scene-03
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py promote --scene scene-03 --revision r01 --variant a --review evidence/reviews/scene-03.yaml
```

- [ ] **Step 3: Act 1 sheet を作り、乾きと光の順序を確認する**

```bash
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope act --act 1
```

Expected: Scene 01-02 は乾燥、Scene 03 だけ最初の雨粒。衣装と髪飾り側が一致する。

- [ ] **Step 4: ユーザーに Act 1 の時系列を提示し、承認後に Act review を確定する**

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py approve-act \
  --act 1 --review evidence/reviews/act-1.yaml
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py validate-act --act 1
npm run gate:edit:ame-no-sei-ni-shite
```

### Task 6: Act 2 の Scene 04-07 と連続性 review

**Files:**

- Create ignored: Scene 04-07 の r01 A/B candidates。
- Create: Scene 04-07 の review YAML と accepted PNG。
- Create ignored: `evidence/contact-sheets/act-2.webp`（package root 基準）。
- Modify: `manifest/scenes/index.yaml`（package root 基準）。

**Interfaces:**

- Consumes: Core refs、Scene 01 anchor、承認済み Scene 03。
- Produces: 雨量、傘、バッグ、帰宅まで連続した Act 2。

- [ ] **Step 1: Scene 04 を生成・選定・promotion する**

参照は Scene 01、C01、C03。伸ばした手の全指、走り出す身体、実在可能 POV、
前髪・肩・袖・裾の軽い雨を確認する。

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py prompt --scene scene-04
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope candidates --scene scene-04
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py promote --scene scene-04 --revision r01 --variant a --review evidence/reviews/scene-04.yaml
```

- [ ] **Step 2: Scene 05 を生成・選定・promotion する**

参照は Scene 01、C03、C05、C06-4。濡れた前髪と毛先、一つの折りたたみ傘、
一つのバッグ、軒下の青灰色光、共有する笑いを確認する。

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py prompt --scene scene-05
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope candidates --scene scene-05
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py promote --scene scene-05 --revision r01 --variant a --review evidence/reviews/scene-05.yaml
```

- [ ] **Step 3: Scene 06 を生成・選定・promotion する**

参照は Scene 01、C03、C05、C06-4。一つの小さな傘、見上げる自然な顔、肩が触れそうな距離、
たかひろの身体や手が見えないこと、濡れが Scene 05 から増えていないことを確認する。

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py prompt --scene scene-06
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope candidates --scene scene-06
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py promote --scene scene-06 --revision r01 --variant a --review evidence/reviews/scene-06.yaml
```

- [ ] **Step 4: Scene 07 を生成・選定・promotion する**

参照は Scene 01、C01、C03、C07 standing。濡れた白スニーカー、閉じた傘、湿った髪と裾、
玄関の低めだが実在可能な POV、靴を脱ぐ前の状態を確認する。

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py prompt --scene scene-07
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope candidates --scene scene-07
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py promote --scene scene-07 --revision r01 --variant a --review evidence/reviews/scene-07.yaml
```

- [ ] **Step 5: Act 2 sheet を作ってユーザーへ提示し、承認後に review を確定する**

```bash
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope act --act 2
```

Expected: 濡れ方は 04 < 05 = 06 = 07、傘とバッグは増殖・消失せず、完全 POV が続く。
ユーザーの明示承認後に実行する。

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py approve-act \
  --act 2 --review evidence/reviews/act-2.yaml
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py validate-act --act 2
npm run gate:edit:ame-no-sei-ni-shite
```

### Task 7: Act 3 の Scene 09-10 と連続性 review

**Files:**

- Create ignored: Scene 09-10 の r01 A/B candidates。
- Create: Scene 09-10 の review YAML と accepted PNG。
- Create ignored: `evidence/contact-sheets/act-3.webp`（package root 基準）。
- Modify: `manifest/scenes/index.yaml`（package root 基準）。

**Interfaces:**

- Consumes: Core refs と Scene 08 `indoor-look-anchor`。
- Produces: 静かな午後と物理的最接近が連続した Act 3。

- [ ] **Step 1: Scene 09 を生成・選定・promotion する**

参照は Scene 08、C03、C05、C06-4、C07 standing。二人分の飲み物、雨窓、
広い余白、乾きつつある柔らかいボブ、安心した横顔を確認する。

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py prompt --scene scene-09
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope candidates --scene scene-09
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py promote --scene scene-09 --revision r01 --variant a --review evidence/reviews/scene-09.yaml
```

- [ ] **Step 2: Scene 10 を生成・選定・promotion する**

参照は Scene 08、C04、C03、C05、C06-4、C07 seated。隣接座位の実在可能 POV、完全な手足、
眠そうだが成人で健康な表情、画面内容なし、性的でない近距離を確認する。

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py prompt --scene scene-10
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope candidates --scene scene-10
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py promote --scene scene-10 --revision r01 --variant a --review evidence/reviews/scene-10.yaml
```

- [ ] **Step 3: Act 3 sheet を作ってユーザーへ提示し、承認後に review を確定する**

```bash
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope act --act 3
```

Expected: Scene 08 の毛先だけ湿り、09 で乾き、10 で乾燥。室内衣装、靴下、髪飾りが一致する。
ユーザーの明示承認後に実行する。

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py approve-act \
  --act 3 --review evidence/reviews/act-3.yaml
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py validate-act --act 3
npm run gate:edit:ame-no-sei-ni-shite
```

### Task 8: Act 4 の Scene 11-12 と連続性 review

**Files:**

- Create ignored: Scene 11-12 の r01 A/B candidates。
- Create: Scene 11-12 の review YAML と accepted PNG。
- Create ignored: `evidence/contact-sheets/act-4.webp`（package root 基準）。
- Modify: `manifest/scenes/index.yaml`（package root 基準）。

**Interfaces:**

- Consumes: Core refs と Scene 08 anchor。
- Produces: 雨上がりから袖をつかむ余韻までの Act 4。

- [ ] **Step 1: Scene 11 を生成・選定・promotion する**

参照は Scene 08、C01、C03、C06-4。雨上がりの窓、薄い夕焼け、乾いた髪と衣装、
終わりに気づく控えめな表情、こちらへ振り返る完全 POV を確認する。

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py prompt --scene scene-11
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope candidates --scene scene-11
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py promote --scene scene-11 --revision r01 --variant a --review evidence/reviews/scene-11.yaml
```

- [ ] **Step 2: Scene 12 を生成・選定・promotion する**

参照は Scene 08、C01、C03、C05、C06-4、C07 standing。夜の扉と廊下、見上げる表情、
自然な五指、画面下端の小さな袖端だけを確認する。たかひろの手、腕、顔、反射、影、
大きすぎる袖、性的な見下ろし構図は Blocker とする。

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py prompt --scene scene-12
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope candidates --scene scene-12
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py promote --scene scene-12 --revision r01 --variant a --review evidence/reviews/scene-12.yaml
```

- [ ] **Step 3: Act 4 sheet を作ってユーザーへ提示し、承認後に review を確定する**

```bash
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope act --act 4
```

Expected: Scene 11 の雨上がり夕景から Scene 12 の暖かい夜廊下へ進み、Scene 12 が
感情的最接近として読める。ユーザーの明示承認後に実行する。

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py approve-act \
  --act 4 --review evidence/reviews/act-4.yaml
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py validate-act --act 4
npm run gate:edit:ame-no-sei-ni-shite
```

### Task 9: 全 12 場面 continuity review

**Files:**

- Create ignored: `akari-v1.2/artbooks/ame-no-sei-ni-shite/evidence/contact-sheets/full-continuity.webp`
- Create: `akari-v1.2/artbooks/ame-no-sei-ni-shite/evidence/reviews/full-continuity.yaml`

**Interfaces:**

- Consumes: 12 accepted PNG と 12 scene review。
- Produces: PDF build の prerequisite となる full continuity approval。

- [ ] **Step 1: full sheet を生成する**

```bash
uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope full
```

Expected: 3 列 x 4 行、Scene 01-12 の時系列順、各 tile に時刻、濡れ方、光、SHA 表示。

- [ ] **Step 2: full continuity review を記録する**

```yaml
schema_version: 1
scope: full-continuity
status: review
checks:
  identity_and_adult_age: pass
  character_left_ornament: pass
  pov_and_viewer_visibility: pass
  outdoor_outfit: pass
  indoor_outfit: pass
  wetness_progression: pass
  light_progression: pass
  prop_continuity: pass
  emotion_arc_without_dialogue: pass
findings: []
```

full sheet review を確定する CLI は実行時の RFC 3339 timestamp を
`reviewed_at` と deterministic sheet の SHA-256 を
`contact_sheet_sha256` として追加する。

- [ ] **Step 3: ユーザーへ full sheet を提示して最終画像承認を得る**

12 枚を台詞なしで順番に見せ、朝から夜、距離の変化、最後の甘さが読めるか確認する。
ここで Blocker/Major が出たら原則として後から制作した場面を再生成する。

- [ ] **Step 4: ユーザー承認後に status を accepted へ変え、full review を確定する**

```bash
uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py approve-full \
  --review evidence/reviews/full-continuity.yaml
npm run gate:edit:ame-no-sei-ni-shite
```

Expected: 12 scene lifecycle と full review が accepted。

### Task 10: A4 横 18 ページ PDF document model

**Files:**

- Create: `tools/pdf/ame-no-sei-ni-shite-document.mjs`
- Create: `tools/pdf/ame-no-sei-ni-shite-document.test.mjs`
- Modify: `tools/pdf/render-html.mjs`
- Modify: `tools/pdf/render.mjs`
- Modify: `tools/pdf/styles.css`
- Create: `scripts/export_ame_no_sei_ni_shite_pdf.py`
- Modify: `package.json`

**Interfaces:**

- Consumes: 固定済み book/page contract、12 accepted PNG、full continuity approval。
- Produces: `ameNoSeiNiShiteDocument` と release PDF。

- [ ] **Step 1: document model の failing Node tests を書く**

```javascript
test("rain-day artbook has 18 A4 landscape pages", () => {
  assert.equal(ameNoSeiNiShiteDocument.id, "akari-v1.2-ame-no-sei-ni-shite");
  assert.deepEqual(ameNoSeiNiShiteDocument.pageSize, {
    widthIn: 11.69,
    heightIn: 8.27,
    previewWidth: 3508,
    previewHeight: 2480,
  });
  assert.equal(pages.length, 18);
  assert.deepEqual(pages.map((p) => p.page), Array.from({length: 18}, (_, i) => i + 1));
});

test("scene pages use one accepted image and at most one dialogue", () => {
  for (const page of pages.filter((p) => p.sceneId)) {
    assert.equal(page.sourceInputs.length, 1);
    assert.ok(page.dialogue.length <= 1);
    assert.match(page.sourceInputs[0], /^scene-(0[1-9]|1[0-2])$/);
  }
});

test("derived pages reuse scene 03, 06, and 12", () => {
  assert.equal(pages[0].sourceInputs[0], "scene-06");
  assert.equal(pages[1].sourceInputs[0], "scene-03");
  assert.equal(pages[15].sourceInputs[0], "scene-12");
});
```

- [ ] **Step 2: Node test が missing document で失敗することを確認する**

```bash
node --test tools/pdf/ame-no-sei-ni-shite-document.test.mjs
```

Expected: module not found で FAIL。

- [ ] **Step 3: document model と専用 block renderer を実装する**

document は次の固定 book contract、scene row、page builder、accepted path map を使う。

```javascript
const book = {
  book_id: "akari-v1.2-ame-no-sei-ni-shite",
  title: "雨のせいにして",
  release_pdf: "release/akari-v1.2-ame-no-sei-ni-shite.pdf",
};
const sceneRows = [
  ["scene-01", "10:02", "遅い。ほら、行こ"],
  ["scene-02", "10:24", ""],
  ["scene-03", "10:41", "うそ。降るって言ってた？"],
  ["scene-04", "10:46", "たかひろ、こっち！"],
  ["scene-05", "10:52", "一本しかないけど、まあいっか"],
  ["scene-06", "11:06", ""],
  ["scene-07", "11:28", "……帰ってきちゃったね"],
  ["scene-08", "12:03", "今日はもう、ここでいいでしょ"],
  ["scene-09", "13:17", ""],
  ["scene-10", "15:42", "……見てるってば"],
  ["scene-11", "18:31", "雨、やんだね"],
  ["scene-12", "21:08", "……もう少しだけ、ここにいていい？"],
];
const sceneIds = Array.from({ length: 12 }, (_, index) => `scene-${String(index + 1).padStart(2, "0")}`);
const assetPaths = Object.fromEntries(sceneIds.map((sceneId) => [
  sceneId,
  `akari-v1.2/artbooks/ame-no-sei-ni-shite/accepted/${sceneId}.png`,
]));
const plate = (page, id, source, time, dialogue, layout = "artbook-scene", crop = "full") => ({
  page,
  id,
  sceneId: id.startsWith("scene-") ? id : undefined,
  title: id,
  eyebrow: "",
  layout,
  crop,
  dialogue: dialogue ? [dialogue] : [],
  sourceInputs: [source],
  blocks: [{ type: "artbook-plate", source, time, dialogue, crop }],
});
const copy = (page, id, layout, title, lines) => ({
  page, id, title, eyebrow: "", layout, dialogue: [], sourceInputs: [],
  blocks: [{ type: "artbook-copy", title, lines }],
});

export const pages = [
  plate(1, "cover", "scene-06", "", "雨のせいにして", "artbook-cover", "cover"),
  plate(2, "first-rain-detail", "scene-03", "", "", "artbook-detail", "rain-detail"),
  copy(3, "title", "artbook-title", "雨のせいにして", ["出かけるはずだった休日は、雨にほどかれていった。", "予定がなくなった部屋で、二人の時間だけが残る。"]),
  ...sceneRows.map(([id, time, dialogue], index) => plate(index + 4, id, id, time, dialogue)),
  plate(16, "afterimage", "scene-12", "", "雨は、もうやんでいた。", "artbook-afterimage", "afterimage"),
  copy(17, "colophon", "artbook-colophon", "制作ノート", ["Akari v1.2", "Ame no sei ni shite", "Version 1.0.0", "2026-07-21"]),
  copy(18, "back-cover", "artbook-back", "雨のせいにして", ["akari-v1.2-ame-no-sei-ni-shite", "checksums.txt"]),
];

export const ameNoSeiNiShiteDocument = {
  id: book.book_id,
  title: book.title,
  pages,
  assetPaths,
  outputPdf: `akari-v1.2/artbooks/ame-no-sei-ni-shite/${book.release_pdf}`,
  previewDir: "build/ame-no-sei-ni-shite-page-previews",
  siteHtml: "build/ame-no-sei-ni-shite-site/index.html",
  pageSize: { widthIn: 11.69, heightIn: 8.27, previewWidth: 3508, previewHeight: 2480 },
};
```

`render-html.mjs` に `artbook-plate` と `artbook-copy` を追加する。
`artbook-plate` は accepted 画像、時刻、0-1 行の台詞、crop class を描画し、
`artbook-copy` は title、intro、colophon、back-cover の PDF-native text を描画する。
画像へ文字を焼き込まない。

```javascript
function renderArtbookPlate(block, page, document) {
  const source = block.source ?? page.sourceInputs[0];
  const imagePath = sourceImagePath(source, document);
  const dialogue = block.dialogue
    ? `<p class="artbook-dialogue">${escapeHtml(block.dialogue)}</p>` : "";
  const time = block.time
    ? `<time class="artbook-time">${escapeHtml(block.time)}</time>` : "";
  return `<section class="block block-artbook-plate crop-${escapeHtml(block.crop)}">
    <figure class="artbook-frame"><img src="../../${escapeHtml(imagePath)}" alt="${escapeHtml(page.title)}"></figure>
    ${time}${dialogue}
  </section>`;
}

function renderArtbookCopy(block) {
  const lines = block.lines.map((line) => `<p>${escapeHtml(line)}</p>`).join("");
  return `<section class="block block-artbook-copy"><h1>${escapeHtml(block.title)}</h1>${lines}</section>`;
}
```

`renderBlock()` の switch へ `artbook-plate` と `artbook-copy` を追加し、上の関数へ
委譲する。

page copy は次で固定する。

```text
Page 1: 雨のせいにして
Page 3 title: 雨のせいにして
Page 3 intro: 出かけるはずだった休日は、雨にほどかれていった。予定がなくなった部屋で、二人の時間だけが残る。
Page 16: 雨は、もうやんでいた。
Page 17: Akari v1.2 / Ame no sei ni shite / Version 1.0.0 / 2026-07-21
Page 18: 雨のせいにして / akari-v1.2-ame-no-sei-ni-shite / checksums.txt
```

- [ ] **Step 4: A4 landscape CSS を追加する**

```css
.layout-artbook-cover,
.layout-artbook-detail,
.layout-artbook-title,
.layout-artbook-scene,
.layout-artbook-afterimage,
.layout-artbook-colophon,
.layout-artbook-back {
  grid-template-rows: minmax(0, 1fr);
  gap: 0;
  padding: 0;
  background: #f7f3ec;
}

.layout-artbook-cover .page-header,
.layout-artbook-detail .page-header,
.layout-artbook-title .page-header,
.layout-artbook-scene .page-header,
.layout-artbook-afterimage .page-header,
.layout-artbook-colophon .page-header,
.layout-artbook-back .page-header,
.layout-artbook-cover .source-list,
.layout-artbook-detail .source-list,
.layout-artbook-title .source-list,
.layout-artbook-scene .source-list,
.layout-artbook-afterimage .source-list,
.layout-artbook-colophon .source-list,
.layout-artbook-back .source-list { display: none; }

.artbook-frame img { width: 100%; height: 100%; object-fit: contain; }
.layout-artbook-cover .artbook-frame img { object-fit: cover; object-position: 52% 44%; }
.layout-artbook-detail .artbook-frame img { object-fit: cover; object-position: 58% 28%; }
.layout-artbook-afterimage .artbook-frame img { object-fit: cover; object-position: 70% 62%; }
```

scene page は上下余白を確保し、3:2 画像を切らずに `object-fit: contain` で置く。
台詞は下余白に一行、時刻は小さく左上へ置く。

- [ ] **Step 5: renderer loader と export wrapper を追加する**

`render.mjs` の loader に次を追加する。

```javascript
"ame-no-sei-ni-shite": async () => {
  const { ameNoSeiNiShiteDocument } = await import("./ame-no-sei-ni-shite-document.mjs");
  return ameNoSeiNiShiteDocument;
},
```

同時に usage の document 候補へ `ame-no-sei-ni-shite` を追加する。

`scripts/export_ame_no_sei_ni_shite_pdf.py` は次を実行する薄い wrapper とする。

```python
subprocess.run(
    ["node", "tools/pdf/render.mjs", "--document", "ame-no-sei-ni-shite", "--pdf"],
    cwd=ROOT,
    check=True,
)
```

`package.json` に次を追加する。

```json
"build:ame-no-sei-ni-shite:previews": "node tools/pdf/render.mjs --document ame-no-sei-ni-shite --previews",
"build:ame-no-sei-ni-shite:pdf": "uv run python scripts/export_ame_no_sei_ni_shite_pdf.py"
```

- [ ] **Step 6: Node tests と previews を直列実行する**

```bash
npm run test:node
npm run build:ame-no-sei-ni-shite:previews
```

Expected: Node tests PASS、`build/ame-no-sei-ni-shite-page-previews/` に 18 PNG。
全 preview を contact sheet または個別画像で目視し、切れ、重なり、空白ページがないことを確認する。

- [ ] **Step 7: shared renderer 変更の integration gate を通す**

```bash
npm run gate:integration:v1-2
```

Expected: PASS。既存 Core PDF と release pins は不変。

### Task 11: 専用 release audit、checksum、最終 handoff

**Files:**

- Create: `scripts/audit_ame_no_sei_ni_shite_pdf.py`
- Create: `tests/test_ame_no_sei_ni_shite_pdf_audit.py`
- Modify: `package.json`
- Create: `akari-v1.2/artbooks/ame-no-sei-ni-shite/release/akari-v1.2-ame-no-sei-ni-shite.pdf`
- Create: `akari-v1.2/artbooks/ame-no-sei-ni-shite/release/checksums.txt`

**Interfaces:**

- Consumes: Task 10 の PDF、12 accepted PNG、full continuity review。
- Produces: 18-page audited PDF、一致する checksum、専用 release gate。

- [ ] **Step 1: audit helper の failing tests を書く**

```python
def test_pdfinfo_requires_eighteen_a4_landscape_pages(self):
    output = "Pages: 18\nPage size: 841.68 x 595.44 pts\n"
    self.audit.require_pdfinfo_contract(output)

def test_pdfinfo_rejects_wrong_page_count(self):
    with self.assertRaisesRegex(AuditError, "18 pages"):
        self.audit.require_pdfinfo_contract("Pages: 17\nPage size: 841.68 x 595.44 pts\n")

def test_checksum_line_uses_pdf_sha(self):
    line = self.audit.checksum_line(Path("book.pdf"), "a" * 64)
    self.assertEqual(f"{'a' * 64}  book.pdf", line)
```

- [ ] **Step 2: focused test が missing audit module で失敗することを確認する**

```bash
uv run python -m unittest tests.test_ame_no_sei_ni_shite_pdf_audit -v
```

Expected: module not found で FAIL。

- [ ] **Step 3: structure/full audit を実装する**

CLI は `--level structure|full` を受ける。structure は qpdf、pdfinfo、pdffonts、
18 page、A4 landscape ratio、embedded Unicode font、manifest lifecycle、Core release pins を確認する。
full は追加で 288 dpi raster、18 PNG、各ページの非空白率、PDF text extraction、
必須文言、preview と同じ cropping、checksum 一致を確認する。

必須文言は次とする。

```python
REQUIRED_TEXT = (
    "雨のせいにして",
    "10:02", "10:24", "10:41", "10:46", "10:52", "11:06",
    "11:28", "12:03", "13:17", "15:42", "18:31", "21:08",
    "遅い。ほら、行こ",
    "……もう少しだけ、ここにいていい？",
    "akari-v1.2-ame-no-sei-ni-shite",
    "Version 1.0.0",
)
```

- [ ] **Step 4: release scripts を package.json に追加する**

```json
"audit:ame-no-sei-ni-shite:pdf:structure": "uv run python scripts/audit_ame_no_sei_ni_shite_pdf.py --level structure",
"audit:ame-no-sei-ni-shite:pdf": "uv run python scripts/audit_ame_no_sei_ni_shite_pdf.py --level full",
"test:python:ame-no-sei-ni-shite": "uv run python -m unittest tests.test_ame_no_sei_ni_shite_contract tests.test_build_ame_no_sei_ni_shite_contact_sheet tests.test_ame_no_sei_ni_shite_pdf_audit -v",
"gate:release:ame-no-sei-ni-shite": "npm run gate:edit:ame-no-sei-ni-shite && uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope all-acts && uv run python scripts/akari_v1_2_ame_no_sei_ni_shite.py validate-act --act all && uv run python scripts/build_ame_no_sei_ni_shite_contact_sheet.py --scope full && npm run build:ame-no-sei-ni-shite:pdf && npm run audit:ame-no-sei-ni-shite:pdf && npm run gate:integration:v1-2"
```

- [ ] **Step 5: PDF を build し checksum を作る**

```bash
npm run build:ame-no-sei-ni-shite:pdf
sha256sum \
  akari-v1.2/artbooks/ame-no-sei-ni-shite/release/akari-v1.2-ame-no-sei-ni-shite.pdf
```

sha256sum の 64 文字 digest と basename を
`akari-v1.2/artbooks/ame-no-sei-ni-shite/release/checksums.txt` に一行で記録する。

- [ ] **Step 6: formal release gate を直列実行する**

```bash
npm run gate:release:ame-no-sei-ni-shite
```

Expected: 12 accepted scenes、full continuity approval、18-page PDF、raster、text、
checksum、Core/Daily 非変更、既存 v1.2 integration がすべて PASS。

- [ ] **Step 7: release artifact を目視する**

18 raster pages を順番に確認し、表紙と派生 crop が新規第 13 場面に見えないこと、
Scene 01-12 が一日として読めること、台詞が画像や裁ち落としへ重ならないこと、
最後の袖と表情が見切れていないことを確認する。

- [ ] **Step 8: commit 範囲をユーザーに確認する**

候補画像と contact sheet は gitignored のまま残す。manifest、accepted PNG、review evidence、
renderer、tests、release PDF、checksum のうち、ユーザーが保存を承認した範囲だけを stage する。
無関係な untracked ディレクトリは stage しない。

- [ ] **Step 9: 承認された release を commit する**

ユーザーが全成果物の保存を承認した場合の exact command:

```bash
git add package.json \
  akari-v1.2/artbooks/ame-no-sei-ni-shite/README.md \
  akari-v1.2/artbooks/ame-no-sei-ni-shite/manifest \
  akari-v1.2/artbooks/ame-no-sei-ni-shite/accepted \
  akari-v1.2/artbooks/ame-no-sei-ni-shite/evidence/reviews \
  akari-v1.2/artbooks/ame-no-sei-ni-shite/release \
  scripts/akari_v1_2_ame_no_sei_ni_shite.py \
  scripts/build_ame_no_sei_ni_shite_contact_sheet.py \
  scripts/export_ame_no_sei_ni_shite_pdf.py \
  scripts/audit_ame_no_sei_ni_shite_pdf.py \
  tests/test_ame_no_sei_ni_shite_contract.py \
  tests/test_build_ame_no_sei_ni_shite_contact_sheet.py \
  tests/test_ame_no_sei_ni_shite_pdf_audit.py \
  tools/pdf/ame-no-sei-ni-shite-document.mjs \
  tools/pdf/ame-no-sei-ni-shite-document.test.mjs \
  tools/pdf/render-html.mjs tools/pdf/render.mjs tools/pdf/styles.css
git commit -m "feat: release rain-day POV artbook"
```

## 実行時の再試行ルール

- 1 round は A/B の 2 候補。
- 一方だけに局所 Major がある場合は、良い候補を選ぶか、その局所原因だけを変えて r02 を作る。
- 両方に同じ identity/hair 問題がある場合は Core 参照の role と向きを再確認する。
- 2 round 連続で Blocker が残ったら、手の動き、傘、マグ、座位など問題の構図を一段簡略化する。
- Scene 04 の手、Scene 05-06 の傘、Scene 08 の二つのマグ、Scene 10 の近距離座位、
  Scene 12 の袖で破綻した時は、低差分合成で切断を隠さず、広い再生成領域か再生成を使う。
- 前後矛盾は後から制作した場面を直す。先行場面に Blocker がある時だけ先行場面を戻す。

## 完了判定

- Scene 01-12 に accepted PNG と accepted review が各 1 件ある。
- Scene 01 と Scene 08 が固定 look anchor として承認済み。
- Act 1-4 と full continuity review が accepted。
- 18 ページ A4 横 PDF と一致する checksum がある。
- `npm run gate:release:ame-no-sei-ni-shite` が成功する。
- default Core PDF、Core accepted、Daily accepted が不変。
- 台詞を隠しても、一日の時系列、雨、距離、最後の別れ惜しさが読める。
