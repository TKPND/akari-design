# V3.0では目の視覚文法を独立させてGPT既定顔を避ける

Date: 2026-08-19

Status: D1 direction promising; not accepted as a V3.0 face anchor

## このメモで固定する判断

Akari V3.0のスタイル探索では、既存の正式ポートレートに顔全体の
権限を与えない。既存画像は髪色、低いサイドポニー、青いヘアピン、
本人らしい雰囲気だけを支える。目の形、虹彩の組み立て、反射、線、
赤み線は、好みの絵から切り出したスタイルカードを唯一の権威にする。

この分離を使ったD1は、ユーザーから
「どストライクというわけではないが、D1まぁまぁええやんw」と評価された。
現時点では有望な研究チェックポイントであり、正式採用画像、正準画像、
本人性の承認済みアンカーではない。このメモの目的は、D1までに効いた手順を
再現可能な形で残し、次の変更を一項目ずつ検証できるようにすることにある。

## 対象と対象外

対象は、V3.0の顔と目から「GPT Image 2で作ったと分かる既定顔」を減らす
参照設計、プロンプト、停止条件である。今回は年齢を数値で指定しない。

次は対象外とする。

- D1を正準画像、正式な顔アンカー、本人性の証拠へ昇格すること
- V2.2の既存正準画像や承認済み画像を置き換えること
- 全身、衣装、ポーズ、背景を含む完成スタイルを決定すること
- 生成候補やユーザー提供画像をGitへ追加すること
- A、B、Cや未承認候補を継続アンカーとして再利用すること

## A、B、Cが同じ既定顔へ寄った原因

A、B、Cには、大きく丸い左右対称の目、橙色の滑らかな放射状虹彩、
同じ位置に置かれた白い丸ハイライト、均一な黒いまつ毛、空気ブラシ状の
赤み、中央寄せの美人ポートレートという共通点があった。

生成履歴を確認すると、失敗はモデル能力だけでは説明できない。

1. 一回の生成に四枚の参照を与え、役割が競合していた。
2. 正式ポートレートを「identity and face authority」としたため、
   V3.0で変更したい既存の目の設計まで固定した。
3. `polished`、`luminous`、`premium anime`のような抽象的な品質語が、
   指定されていない目の内部をGPTの既定レンダリングで補わせた。
4. 毎回を新規生成として始め、承認済みのV3.0顔アンカーを再利用して
   いなかった。

OpenAIの公式ガイドは、少数の参照、画像ごとの役割、保持条件の明示、
段階的な修正を勧めている。複数参照から内容とスタイルを分ける難しさは、
GPT Imageに限らない研究課題でもある。今回の手順は、この二点を
Akari向けの実行規則へ落としたものになる。

## D0の入力は二枚に限定した

### Image 1: Akariの限定的な本人参照

- Path:
  `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`
- Dimensions: `1888x3344`
- SHA-256:
  `b076afd95be49c4ed9c5a4ddfb4083c9ead8328313b4d5fa0555a374dd10543c`
- 権限: 温かい茶髪、画面右の低いサイドポニー、顔まわりの後れ毛、
  一本だけの青いヘアピン、琥珀系の目色、本人らしい親しみ
- 権限外: 目の開口形、虹彩構造、反射、顔の描画方式、光沢

### Image 2: 目と線だけのスタイルカード

- Source attachment:
  `/home/takahiro/.codex/attachments/fc14b321-15db-4bfd-803d-0f56addd9b84/HH1CApCakAAW2dl.jpg`
- Source dimensions: `1592x2360`
- Source SHA-256:
  `577a5b9f347d5ee10d69829c80f6c551cb62bd86a7c7a710eb5918ef994ddf89`
- Card path:
  `/home/takahiro/.codex/visualizations/2026/08/19/01a017d1-a2a4-7513-b31f-81ede290da2b/v3-style-spike/v3-hh1-style-card-v2.png`
- Card dimensions: `1024x1024`
- Card SHA-256:
  `71bbb315c59593cbcd425ac3bd7f270c1092f645d5e4321ee9378c67f3d9ce26`
- 権限: まぶたの形、虹彩の上下分割、瞳孔と反射の配置、線の先細り、
  赤み線、短く切れた髪の反射、平面的なセル塗り
- 権限外: 黒髪、ツインテール、青い髪飾り、衣装、ポーズ、手、背景、
  参照キャラクター本人の顔

カードは、全身画像をそのまま参照させず、必要な目の構造を入力面積の
大部分へ置くために作った。cropを大きく見せる効果は公式仕様ではなく、
今回検証中の実務上の仮説である。

```bash
V3_STYLE_SRC=/home/takahiro/.codex/attachments/fc14b321-15db-4bfd-803d-0f56addd9b84/HH1CApCakAAW2dl.jpg
V3_SPIKE_DIR=/home/takahiro/.codex/visualizations/2026/08/19/01a017d1-a2a4-7513-b31f-81ede290da2b/v3-style-spike

rtk magick "$V3_STYLE_SRC" -crop 900x250+160+340 +repage \
  -resize 1024x420 -background '#f4f0ec' -gravity center \
  -extent 1024x420 "$V3_SPIKE_DIR/card-top-eyes.png"

rtk magick "$V3_STYLE_SRC" -crop 380x280+190+325 +repage \
  -resize '512x604^' -gravity center -extent 512x604 \
  "$V3_SPIKE_DIR/card-bottom-eye.png"

rtk magick "$V3_STYLE_SRC" -crop 520x520+390+120 +repage \
  -resize '512x604^' -gravity center -extent 512x604 \
  "$V3_SPIKE_DIR/card-bottom-hair.png"

rtk magick "$V3_SPIKE_DIR/card-bottom-eye.png" \
  "$V3_SPIKE_DIR/card-bottom-hair.png" +append \
  "$V3_SPIKE_DIR/card-bottom-row.png"

rtk magick "$V3_SPIKE_DIR/card-top-eyes.png" \
  "$V3_SPIKE_DIR/card-bottom-row.png" -append \
  "$V3_SPIKE_DIR/v3-hh1-style-card-v2.png"
```

## D0で目の構造は変わったが反射が残った

- Generation ID: `exec-0ce555d0-2b44-412d-9a3b-efc686491360`
- Path:
  `/home/takahiro/.codex/generated_images/01a017d1-a2a4-7513-b31f-81ede290da2b/exec-0ce555d0-2b44-412d-9a3b-efc686491360.png`
- Dimensions: `1142x1378`
- SHA-256:
  `1a1f63623a03f1d6114e8928ccb76524a38fe8895748614a2c93e55defe6ad08`

D0では、半目気味の左右差、暗い上部虹彩、黄土色の下部パーツ、赤み線が
現れた。一方、白い反射はまだ大きく、髪にも稲妻形の短い反射が出た。
このためD0は採用せず、構図を保持した局所修正へ進んだ。

### D0の完全プロンプト

```text
Use case: stylized-concept. Create one preview-only V3 face-style gate, not a finished scene.

Reference roles:
- Image 1 is Akari identity only. Preserve her warm medium-brown hair, asymmetric low side ponytail on the viewer's right, loose face-framing strands, exactly one slim blue hairpin, warm amber-brown eye color, and gentle recognizable presence. Do not preserve Image 1's eye-drawing method or glossy face rendering.
- Image 2 is the sole visual-grammar authority for eyelid geometry, iris construction, pupil and highlight topology, line taper, coral blush hatching, chunky tapered bangs, short broken hair reflections, and matte cel rendering. Do not copy its black hair, twin tails, blue accessories, outfit, pose, facial identity, hand, or background.

Subject and composition:
A tight head-and-shoulders portrait of Akari on a plain warm off-white background. Near-front three-quarter view, slight natural head roll, one eye subtly narrower and lower than the other, a small asymmetric closed-mouth smile, no hands, minimal shoulders.

Critical eye construction:
Shallow tapered almond openings with a relaxed half-lidded feeling. A dark cocoa upper iris cap occupies roughly the upper half; a muted amber-gold lower facet sits below it. The narrow vertical pupil partly disappears into the upper shadow. Each eye has one small irregular cream highlight, with deliberately different size and placement between the two eyes; no mirrored highlight pattern. Sclera reads mostly as a lower and outer wedge. The upper lash is dark and tapered; the lower lid is only a minimal warm line.

Rendering:
Fine coral cheek hatching with unequal density. Flat matte fills. Crisp one- or two-step cool lavender-blue cel-shadow planes. Hair highlights are short, broken, irregular shapes, never a continuous crown band. Clean sparse linework; no overall paper texture, bloom, or airbrush haze.

Hard constraints:
No twin tails, maid outfit, animal ears, hand gesture, text, logo, or watermark. No large mirrored white circular catchlights. No glossy spherical or smooth radial-gradient irises. No broad zigzag crown highlight. No centered generic beauty-poster pose.
```

## D1は目だけを再編集した有望な停止点である

- Generation ID: `exec-7c083c6c-19f6-4cec-9e4b-c9cfdd2776ae`
- Edit target: D0
- Supporting style input: D0と同じ目のスタイルカード
- Path:
  `/home/takahiro/.codex/generated_images/01a017d1-a2a4-7513-b31f-81ede290da2b/exec-7c083c6c-19f6-4cec-9e4b-c9cfdd2776ae.png`
- Dimensions: `1142x1377`
- SHA-256:
  `7336d5098c3161423a7b880ff5660d12d593fd3a58ddcf20acdaac3fc04da195`

D1では、目の開口をさらに平たくし、白い丸反射を小さな非対称の反射へ
縮めた。暗い上部、赤茶の中間、黄土色の下部を平面的な部品として読める。
左右が同じ型ではなくなり、A、B、CよりGPT既定顔から離れた。

残る問題は、髪の稲妻形反射、線の太さと密度の均一さ、口元と顔面配置に
残る既定感である。次のD2では髪の反射形だけを変え、目、顔、構図、色、
ポニーテール、ヘアピン、服、影を固定する。

### D1の完全プロンプト

```text
Edit Image 1 in place. Preserve its composition, head angle, facial identity, hair silhouette and color, ponytail, single blue hairpin, mouth, nose, skin, shirt, cel shadows, background, and crop. Do not redesign the character or redraw the hair.

Change only both eyes and their immediate eyelid lines, using Image 2 as the exact visual grammar reference.

Make both eye openings flatter and more tapered, with the viewer-left eye distinctly narrower and slightly lower. Rebuild each iris from a small set of flat graphic shapes: a deep cocoa upper cap covering about half, one muted rose-brown middle plane, one compact ochre-gold lower facet, and a narrow vertical dark pupil partly lost into the upper cap. Keep the sclera mainly as lower/outer wedges.

Remove every current glossy white catchlight and sparkle. Add exactly one tiny irregular off-white mark per eye, much smaller than the pupil, with visibly different shape, size, and placement in the two eyes. Do not add any second dot, lower sparkle, rim light, radial gradient, glassy shine, or mirrored pattern.

Upper lashes must be tapered dark wedges; lower lids only short warm strokes. Retain the fine coral blush hatching. The result should read as matte flat cel drawing, not glossy rendered anime eyes. No other changes.
```

## 次は一項目ずつ変える

今後は次の順で進める。ただし各候補を自動的にアンカーへ昇格しない。

1. D2: D1を編集対象にし、髪の反射形だけを変更する。
2. D3: D2の方向が有望なら、線の太さと密度だけを調整する。
3. 顔ゲート: ユーザーが明示的に承認した候補だけをV3.0顔アンカー候補にする。
4. バストアップ: 承認済み顔アンカーを主入力にし、構図変更を一段だけ試す。
5. シーン: バストアップまで安定してから、構図参照を一枚だけ追加する。

髪と線を同時に変える、顔と衣装を同時に変える、全身と背景を同時に足す、
といった変更は行わない。失敗した候補を正の参照へ混ぜない。

## 研究から採用したことと保留したこと

採用したのは、少数参照、役割ラベル、明示的な保持条件、顔アンカーの
段階的な作成、一回の修正で一項目だけを変える方法である。

次は有効性を確認できていないため、手順の中核にしない。

- `remember this style`など、会話内で学習したように扱う命令
- 長い品質タグの列挙
- 参照順だけで重みを制御できるという前提
- GPT Image 2でのseed、LoRA、style strength、reference weightの指定
- cropを大きくすれば必ずスタイルが強くなるという断定

GPT-5.6 Proで参照特徴をよく捉えた例があることは、モデルに能力がないという
見立てを否定する材料になる。公式には、ThinkingとProが画像生成前に計画と
調整を行えることは説明されている。一方、通常経路と異なる画像レンダラーを
使うとは明記されていない。この差は、現時点では計画と参照解釈の差という
推定に留める。

## 参照した資料

- [Creating images with ChatGPT](https://openai.com/academy/image-generation/)
- [GPT Image prompting guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)
- [Image generation guide](https://developers.openai.com/api/docs/guides/image-generation)
- [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- [MultiRef benchmark](https://arxiv.org/abs/2508.06905)
- [InstantStyle](https://arxiv.org/abs/2404.02733)
- [StyleDrop](https://arxiv.org/abs/2306.00983)
- [Community sprite-style workflow](https://www.reddit.com/r/aigamedev/comments/1vqdvaq/my_workflow_for_consistent_sprite_styles/)
- [GPT Image 2 issue and workaround collection](https://community.openai.com/t/collection-of-gpt-image-generator-2-0-issues-bugs-and-work-around-tips-check-first-post/1379535)

## 記録の境界

生成画像とスタイルカードは、明示的に昇格するまでローカルの研究出力として
扱う。研究メモの更新、ユーザー判断の記録、正式資産の追加は別commitにする。
正式資産を追加する場合だけ`feat:`を使い、研究中は`docs:`で記録する。

今回のrolloutは次に保存されている。

`/home/takahiro/.codex/sessions/2026/08/19/rollout-2026-08-19T11-20-09-01a017d1-a2a4-7513-b31f-81ede290da2b.jsonl`
