# V3.0では目の画風と表情を分けてGPT既定顔と半目固定を避ける

Date: 2026-08-19

Status: V2.3 face candidate user-confirmed at 5/6; promising but not fixed or approved as an anchor

## このメモで固定する判断

Akari V3.0のスタイル探索では、既存の正式ポートレートに顔全体の
権限を与えない。既存画像は髪色、低いサイドポニー、青いヘアピン、
本人らしい雰囲気だけを支える。好みの絵から移すのは、虹彩の組み立て、
反射、線、赤み線などの描画方式に限る。目の開き、まぶた、眉、視線、
頭の傾きは表情変数として分離し、スタイルカードの権限へ含めない。

この分離を使ったD1は、ユーザーから
「どストライクというわけではないが、D1まぁまぁええやんw」と評価された。
この時点では有望な研究チェックポイントだったが、口元パイロット後の
「全部違う。眠そうなだけに見える」という判定で採用候補から外れた。
D1は、虹彩と反射の実験結果を残す負の対照であり、正式採用画像、正準画像、
本人性の承認済みアンカーではない。このメモの目的は、成功だけでなく
表情設計の失敗も再現可能な形で残し、次の変更を一項目ずつ検証できるように
することにある。

## 対象と対象外

対象は、V3.0の顔と目から「GPT Image 2で作ったと分かる既定顔」を減らし、
画風と表情を混同しないための参照設計、プロンプト、停止条件である。
今回は年齢を数値で指定しない。

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

## D1は虹彩文法を得たが表情ベースとして失敗した

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

一方、上まぶたを低くして縦の開口を狭めたため、表情は眠そうに見える。
この欠点は口元パイロット後のユーザー判定で確定した。以降、D1を
「有望な顔」や正の表情参照として扱わない。

残る問題は、髪の稲妻形反射、線の太さと密度の均一さ、口元と顔面配置に
残る既定感である。このうちD2では髪の反射形だけを変え、目、顔、構図、色、
ポニーテール、ヘアピン、服、影を固定した。

### D1の完全プロンプト

```text
Edit Image 1 in place. Preserve its composition, head angle, facial identity, hair silhouette and color, ponytail, single blue hairpin, mouth, nose, skin, shirt, cel shadows, background, and crop. Do not redesign the character or redraw the hair.

Change only both eyes and their immediate eyelid lines, using Image 2 as the exact visual grammar reference.

Make both eye openings flatter and more tapered, with the viewer-left eye distinctly narrower and slightly lower. Rebuild each iris from a small set of flat graphic shapes: a deep cocoa upper cap covering about half, one muted rose-brown middle plane, one compact ochre-gold lower facet, and a narrow vertical dark pupil partly lost into the upper cap. Keep the sclera mainly as lower/outer wedges.

Remove every current glossy white catchlight and sparkle. Add exactly one tiny irregular off-white mark per eye, much smaller than the pupil, with visibly different shape, size, and placement in the two eyes. Do not add any second dot, lower sparkle, rim light, radial gradient, glassy shine, or mirrored pattern.

Upper lashes must be tapered dark wedges; lower lids only short warm strokes. Retain the fine coral blush hatching. The result should read as matte flat cel drawing, not glossy rendered anime eyes. No other changes.
```

## D2では髪の稲妻形反射を疎な単線へ変えた

- Generation ID: `exec-908c176d-3437-4875-bfc5-5589b34d549b`
- Edit target: D1
- Supporting input: 髪面だけを拡大したスタイルカード
- Path:
  `/home/takahiro/.codex/generated_images/01a017d1-a2a4-7513-b31f-81ede290da2b/exec-908c176d-3437-4875-bfc5-5589b34d549b.png`
- Dimensions: `1143x1376`
- SHA-256:
  `9a957e6341974f8b2ec181c1e30a3614b2462c25aebf8f13f3253f181a390084`

D2は、D1に並んでいたW字、稲妻形、山形の反射を除き、短い縦楕円と
単線の反射へ置き換えた。反射のない髪面が広くなり、同じ記号の反復も
減った。目の開口、虹彩の上下分割、小さな反射、口、顔向き、髪型、
ヘアピン、服、背景は、目視比較ではD1の方向を維持している。

ただし、これはピクセル単位の局所編集ではない。D1の`1142x1377`に対して
D2は`1143x1376`で、髪色や輪郭にも軽い再描画がある。D2の髪反射テストは
内部評価で狙いどおりだったが、ユーザーは「D1の方がええかも」と評価した。
以降の実験はD1から分岐し、D2を入力やアンカーとして再利用しない。

### D2用の髪面スタイルカード

- Path:
  `/home/takahiro/.codex/visualizations/2026/08/19/01a017d1-a2a4-7513-b31f-81ede290da2b/v3-style-spike/hair-card/v3-hh1-hair-surface-card-v2.png`
- Dimensions: `1024x1024`
- SHA-256:
  `d26f17d715e17a4d4b9665c919dab6e3c06ed29e3dc5de48affcd6217086dfc9`
- 権限: 短い縦楕円、孤立した単線、低い明暗差、広い無反射面
- 権限外: 黒髪、顔、目、前髪形、髪型、髪飾り、参照キャラクター本人

```bash
rtk magick "$V3_STYLE_SRC" -crop 900x560+120+0 +repage \
  -resize '1024x1024^' -gravity center -extent 1024x1024 \
  "$V3_SPIKE_DIR/hair-card/v3-hh1-hair-surface-card-v2.png"
```

D1とD2のローカル比較画像は次にある。左がD1、右がD2である。

- Path:
  `/home/takahiro/.codex/visualizations/2026/08/19/01a017d1-a2a4-7513-b31f-81ede290da2b/v3-style-spike/d1-d2-side-by-side.png`
- Dimensions: `1232x740`
- SHA-256:
  `fd62f1111de13516d98ee3c829b930a5998d5f9935a6a88202a00135f8e3890a`

### D2の完全プロンプト

```text
Use case: precise-object-edit.
Asset type: Akari V3.0 D2 hair-reflection research spike.

Input images:
- Image 1 is the edit target. Preserve its exact character, composition, crop, head angle, facial proportions, D1 eyes and eyelids, pupils and highlights, eyebrows, nose, mouth, blush, skin, hair silhouette and brown color, bang grouping, low side ponytail, blue tie, single blue hairpin, shirt, cel-shadow shapes, linework, and warm off-white background.
- Image 2 is a supporting reference only for sparse hair-surface mark vocabulary. Borrow only its short vertical ovals, isolated tapered dashes, low contrast, and large uninterrupted matte hair planes. Do not copy its black color, face, eyes, bangs, hairstyle, accessories, or character identity. Ignore the kinked central highlight in Image 2.

Primary request:
Change only the small light-colored reflection marks painted inside the brown hair masses of Image 1.

Remove every tan zigzag, W, M, chevron, sawtooth, and lightning-bolt reflection from the crown, bangs, side locks, and ponytail. Replace them with a sparse, uneven set of muted low-contrast marks: short tapered oval dabs and slightly curved single brush dashes that follow each local strand direction. Vary their length, spacing, angle, and grouping. Leave most of every hair plane completely unhighlighted. Use no continuous crown band and no repeating motif.

Constraints:
Do not alter any hair boundary, strand contour, bang tip, ponytail shape, hair color, shadow plane, or internal dark line. Do not change the face or eyes in any visible way. Do not add gloss, bloom, gradients, extra strands, texture noise, text, logo, or watermark. No changes outside the existing hair highlight marks.
```

## D1から口元だけを動かすパッケージ実験を行った

ユーザー提供のGPT Pro引き継ぎパッケージは、展開前検査と内部チェックサム
検証を通過した。

- Archive:
  `/home/takahiro/.codex/attachments/02a1b208-5602-4995-80b2-d15adcda42d9/akari-v22-dechappy-face-research-handoff-20260819.zip`
- Archive SHA-256:
  `fff3fb6ea3221718aae998a4b580d1096c97f5b6faf088dcabcc99c2f8c01e54`
- Verification: `unzip -tq`で異常なし。展開後の`sha256sum -c`は全項目OK
- Entry points: `README.md`、`PROMPT.md`、`docs/00`から`05`
- Included evidence: 外部参照一枚、GPT ProのI2I出力二枚、比較シート、
  顔クロップ、実験ログと結果報告の雛形

パッケージの外部参照は、D0とD1で使った好み画像と視覚的には同じ元絵の
別サイズ版である。パッケージ版は`1381x2048`、SHA-256は
`fe2c9101e6bea5f365b6450a6478ee088058218993f372d279aa5df400f16521`で、
元の添付画像とは寸法とハッシュが異なる。

収録された二枚のI2I出力は、横長の目や丸い下顔面が全身の駅構図でも
ある程度残ることを示している。一方、顔クロップ併用の優位性、文章だけの
再現性、四枚中三枚の合格率は未検証である。パッケージ全体をそのまま
V3.0へ適用せず、D1の残課題に対応する一変数実験へ縮める。

### 実行時に承認されていた四枚パイロット

パイロットでは、小さな閉じ口が既定顔への回帰を促すという仮説と、
顔クロップが表情変更時の文法保持を助けるという仮説を切り分ける。
年齢は数値で指定しない。

- `D1-MOUTH-A1`、`D1-MOUTH-A2`: Image 1のD1だけを編集対象にする
- `D1-MOUTH-B1`、`D1-MOUTH-B2`: Image 1のD1に、Image 2として
  パッケージの`refs/20_ref_face_crop.png`を加える
- Image 2の権限: 単純な開口形、口まわりの低い情報密度、平面的な塗り
- Image 2の権限外: 顔の輪郭、目、虹彩、黒髪、ツインテール、水色の髪飾り、
  衣装、手、背景、参照キャラクター本人
- 唯一の変更: D1の小さな閉じ口を、歯や舌を描き込まない単純な開口笑顔へ
  変える
- 保持対象: D1の目の開口、虹彩の上下分割、瞳孔、反射、白目、眉、鼻、
  頬線、顔幅、顎、髪色、髪型、ポニーテール、青い髪留め、服、影、構図、
  crop、背景

開口と同時に目が丸くなる、虹彩が宝石状になる、顎が細くなる、鼻の光点や
髪の光沢が増える、黒髪やツインテールが混入する、口以外の形が変わる場合は
失敗とする。四枚は研究候補に留め、ユーザー判断なしで顔アンカーへ昇格しない。

## 四枚の口元パイロットでは局所効果と保持性能が分かれた

2026-08-19に、承認済み設計どおりA条件とB条件を二枚ずつ生成した。
A条件はD1だけを入力し、B条件はD1に役割限定の顔クロップを追加した。
各条件内では同じプロンプトを使い、出力のばらつきも観察対象にした。

B条件で使った顔クロップは、パッケージ内の
`refs/20_ref_face_crop.png`である。寸法は`768x768`、SHA-256は
`a8d850cff91a69d799a5c5d86ab8e7b8a6fd0e3fa97f7ee29e4cbff28e583c92`。

### 生成した四枚

#### D1-MOUTH-A1

- Generation ID: `exec-8d8f0485-f0b4-4fef-86fd-6c9ce54725ea`
- Path:
  `/home/takahiro/.codex/generated_images/01a017d1-a2a4-7513-b31f-81ede290da2b/exec-8d8f0485-f0b4-4fef-86fd-6c9ce54725ea.png`
- Dimensions: `1145x1373`
- SHA-256:
  `946a658fe8c5ddd85eee0e7b3e3d3fdf7f16d4ffab975c6833440b27d520187f`

#### D1-MOUTH-A2

- Generation ID: `exec-6d36438f-55be-4f7e-821b-ab20c9ca09b2`
- Path:
  `/home/takahiro/.codex/generated_images/01a017d1-a2a4-7513-b31f-81ede290da2b/exec-6d36438f-55be-4f7e-821b-ab20c9ca09b2.png`
- Dimensions: `1143x1376`
- SHA-256:
  `e07b4c5864134e0711b696b8c7d941be32120bf9a15a6c59cccdef9943628fdb`

#### D1-MOUTH-B1

- Generation ID: `exec-ca57f0df-fff9-4cb6-97d3-ea50be4b6e0d`
- Path:
  `/home/takahiro/.codex/generated_images/01a017d1-a2a4-7513-b31f-81ede290da2b/exec-ca57f0df-fff9-4cb6-97d3-ea50be4b6e0d.png`
- Dimensions: `1144x1375`
- SHA-256:
  `22eaf33c98e55822dcfae1b59ad09ab3bf7c928ce8b12dc216eb9966f9b6ad36`

#### D1-MOUTH-B2

- Generation ID: `exec-7cf3c009-f907-46dc-9df9-f58f055eb0c8`
- Path:
  `/home/takahiro/.codex/generated_images/01a017d1-a2a4-7513-b31f-81ede290da2b/exec-7cf3c009-f907-46dc-9df9-f58f055eb0c8.png`
- Dimensions: `1143x1376`
- SHA-256:
  `47edb1cf0f4f8e8c68ff3e493c990e8c4907c34953100790f99c350833fa70b2`

比較画像は、D1、A1、A2、B1、B2の順に並べた。

- 顔比較:
  `/home/takahiro/.codex/visualizations/2026/08/19/01a017d1-a2a4-7513-b31f-81ede290da2b/v3-style-spike/mouth-pilot/d1-mouth-pilot-face-grid.png`
- 顔比較の寸法: `1940x450`
- 顔比較のSHA-256:
  `7046b95142a6056b9346607a2ee5beb4e6f64220f7f0abd56e04a56313752332`
- 全体比較:
  `/home/takahiro/.codex/visualizations/2026/08/19/01a017d1-a2a4-7513-b31f-81ede290da2b/v3-style-spike/mouth-pilot/d1-mouth-pilot-full-grid.png`
- 全体比較の寸法: `1660x482`
- 全体比較のSHA-256:
  `3c274ffd0f97617e5948f67b464608051d682fcfd65ad4d84c7055bc2b1f2d33`

### 観察結果

四枚とも、D1の平たい目の開口、虹彩の上下分割、小さな非対称反射、
茶髪、低いサイドポニー、一本の青いヘアピンを目視上は維持した。
開口笑顔へ変えても、今回の四枚では目の丸型化や宝石状の虹彩への明確な
回帰は起きなかった。黒髪、ツインテール、水色の髪飾りの混入もない。

A1とA2は、D1からの変化が比較的控えめな小さい開口になった。A2はA1より
口内が暗く、形も少し明瞭である。B1とB2は、パッケージ参照に近い、幅が
広く丸みのある開口になった。顔クロップには口の形を強める局所効果が
見えるが、目、顔幅、顎、髪、ヘアピンを含む顔全体の保持性能を改善したとは
まだ言えない。

目視確認の仮採点は次のとおり。候補選びの補助であり、ユーザーの顔ゲートを
代替しない。

| 候補 | 顔形 /20 | 目 /25 | 既定感の低さ /20 | 口の簡潔さ /10 | D1保持 /15 | 指示遵守 /10 | 合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| D1 | 18 | 22 | 13 | 8 | 15 | 10 | 86 |
| A1 | 18 | 22 | 16 | 8 | 15 | 10 | 89 |
| A2 | 18 | 22 | 16 | 9 | 15 | 10 | 90 |
| B1 | 18 | 22 | 17 | 9 | 15 | 10 | 91 |
| B2 | 18 | 22 | 17 | 9 | 15 | 10 | 91 |

ImageMagickの`compare -metric SSIM`でも、D1との差を補助的に調べた。
各出力をD1の`1142x1377`へリサイズしてから測ったため、寸法補正そのものの
差を含む。この環境の出力値はdistortionであり、小さいほどD1に近い。

| 候補 | 全体 | 上部 | 目領域 |
| --- | ---: | ---: | ---: |
| A1 | 0.0735263 | 0.0737516 | 0.0849889 |
| A2 | 0.0415150 | 0.0401714 | 0.0423226 |
| B1 | 0.0714970 | 0.0733557 | 0.0764293 |
| B2 | 0.0613794 | 0.0646920 | 0.0635377 |
| A平均 | 0.0575207 | 0.0569615 | 0.0636558 |
| B平均 | 0.0664382 | 0.0690239 | 0.0699835 |

この測定では、A条件のほうが平均してD1に近い。A2とB2は元の寸法も同じ
なので比較しやすく、A2のほうが三領域とも差が小さい。したがって、
「Bは口の文法を強くする」と「Bは顔全体をよく保持する」を分けて扱う。
B条件を勝者とは判定しない。

生成直後は、D1を閉じ口の対照、A2を外部クロップなしの控えめな開口候補、
B1とB2を口形が強い候補としてユーザーへ提示した。各条件二枚だけなので、
パッケージが提案する四枚中三枚の合格基準を評価するには足りなかった。

### 最新判定で候補順位と口原因説は失効した

ユーザーの最終判定は「全部違う。眠そうなだけに見える」だった。D1、A1、
A2、B1、B2はすべて不採用とし、正の参照や次工程のアンカーへ使わない。

判定時に添付された次の画像は、D0と寸法、SHA-256、全画素が一致した。
D0も眠そうな読みを調べる負の対照として扱い、採用候補とは解釈しない。

- Attachment:
  `/home/takahiro/.codex/attachments/cd4168f6-7f66-4792-b0be-e4dc35501e2c/codex-clipboard-4361c9d4-a095-48e5-8e5b-5e68acae7386.png`
- Dimensions: `1142x1378`
- SHA-256:
  `1a1f63623a03f1d6114e8928ccb76524a38fe8895748614a2c93e55defe6ad08`
- Pixel comparison against D0: ImageMagick `compare -metric AE`で`0`

眠そうな読みは、D0から口元パイロットまで一貫して与えた指示で説明できる。
モデルが偶発的に変えたとは考えにくい。

1. D0で`relaxed half-lidded feeling`を指定し、片目を狭く低くした。
2. D1で`flatter and more tapered`を追加し、上まぶたの被さりと
   縦の開口不足を強めた。
3. 暗い上部虹彩、上影へ隠れる瞳孔、下外側だけの白目、短い下まぶた線が、
   覚醒感を示す手掛かりを減らした。
4. A条件とB条件では、`eye openings`と`asymmetric eyelids`を
   保持対象にした。口だけを変え、眠そうな上顔面を固定していた。
5. B条件の顔クロップは口の形だけに権限を限定したため、目や眉の表情を
   改善する経路がなかった。

好み画像から移すべきだったのは、線の細さ、平面的な虹彩、上まつ毛の処理、
低い情報密度、暖色の頬線である。半目、視線、眉、頭の傾き、手や姿勢は
その一枚に乗った表情とポーズであり、画風そのものではなかった。
今回の根本原因は、画風と表情を同じスタイルカードの権限へまとめたことにある。

仮採点も候補順位としては無効になった。採点軸に「眠そうに見えないか」と
「表情の魅力」がなく、原因であるD1の目を保持するほど加点していた。
SSIMの数値は再現性記録として残すが、D1への近さは品質の高さではない。
A2は、拒否された眠そうなD1を最もよく保持していた。その結果として差が
小さい。A/Bで観察した口形の差、生成ID、ハッシュは技術記録として有効だが、
候補選択には使わない。

### A条件の完全プロンプト

```text
Use case: precise-object-edit
Asset type: Akari V3.0 D1 mouth-stress research pilot, preview only

Input images:
- Image 1 is the sole edit target and the sole authority for the character, face, eyes, hair, clothing, composition, crop, and rendering.

Primary request:
Edit Image 1 in place. Change only the small closed-mouth smile into a simple, moderately wide open smile. Keep the mouth centered at the same position. Draw the opening as one clean, softly rounded graphic shape with a muted warm rose interior. Show no teeth, tongue, lips, lip gloss, saliva, inner-mouth highlight, or detailed cavity.

Hard invariants:
Preserve Image 1's exact canvas and crop, head angle, face outline, cheek volume, chin, eye openings, asymmetric eyelids, iris size and flat upper/middle/lower color planes, pupils, tiny asymmetric eye reflections, sclera wedges, eyebrows, nose mark, blush hatching, skin color, hair silhouette and warm brown color, bang grouping, low side ponytail, blue tie, single blue hairpin, hair reflections, shirt, line thickness, cel-shadow shapes, warm off-white background, and every non-mouth pixel as closely as the edit system allows.

Failure conditions:
Do not round or enlarge the eyes. Do not enlarge or gloss the irises. Do not add catchlights. Do not narrow the jaw, sharpen the chin, brighten the nose, increase hair gloss, smooth the blush into airbrush, redesign the face, or alter anything outside the mouth. No text, logo, or watermark.
```

### B条件の完全プロンプト

```text
Use case: precise-object-edit
Asset type: Akari V3.0 D1 mouth-stress research pilot with a role-limited face crop, preview only

Input images:
- Image 1 is the sole edit target and the sole authority for the character, face outline, eyes, hair, clothing, composition, crop, and rendering.
- Image 2 is a supporting reference only for the simple toothless open-mouth topology, low information density around the mouth, and flat matte mouth fill. Do not copy Image 2's facial identity, face outline, jaw, chin, eyes, irises, eyebrows, nose, black hair, twin tails, blue scrunchies, skin tone, clothing, hand, pose, background, or character.

Primary request:
Edit Image 1 in place. Change only the small closed-mouth smile into a simple, moderately wide open smile. Keep the mouth centered at the same position. Borrow only Image 2's clean, softly rounded open shape and restrained low-detail treatment. Use one muted warm rose interior. Show no teeth, tongue, lips, lip gloss, saliva, inner-mouth highlight, or detailed cavity.

Hard invariants:
Preserve Image 1's exact canvas and crop, head angle, face outline, cheek volume, chin, eye openings, asymmetric eyelids, iris size and flat upper/middle/lower color planes, pupils, tiny asymmetric eye reflections, sclera wedges, eyebrows, nose mark, blush hatching, skin color, hair silhouette and warm brown color, bang grouping, low side ponytail, blue tie, single blue hairpin, hair reflections, shirt, line thickness, cel-shadow shapes, warm off-white background, and every non-mouth pixel as closely as the edit system allows.

Failure conditions:
Do not round or enlarge the eyes. Do not enlarge or gloss the irises. Do not add catchlights. Do not narrow the jaw, sharpen the chin, brighten the nose, increase hair gloss, smooth the blush into airbrush, copy any identity or accessory from Image 2, redesign the face, or alter anything outside the mouth. No text, logo, or watermark.
```

## 次は一項目ずつ変える

口元パイロットは不合格で終了する。次の生成はまだ承認されていない。
生成する場合も、次の順で一変数ずつ確かめる。

1. 負の対照: D0、D1、A1、A2、B1、B2を採用候補から外す。
2. 縦開口テスト: D1を比較用の編集対象に限り、口、眉、虹彩の部品、
   目の横幅、顔、髪、構図を保ったまま、上まぶたの高さだけを変える。
3. 成功条件: ユーザーがまず「眠そうではない」と判断する。丸い既定目や
   宝石状虹彩へ戻っていないかは、その後に判定する。
4. 失敗条件: 眠そうなまま、丸目化、虹彩の光沢化のいずれかが起きる。
5. 眉と視線: 縦開口だけで足りない場合に限り、別実験で一項目ずつ動かす。
6. 顔ゲート: 表情の失敗を解消し、ユーザーが明示的に承認した候補だけを
   V3.0顔アンカー候補にする。

髪と線を同時に変える、顔と衣装を同時に変える、全身と背景を同時に足す、
といった変更は行わない。失敗した候補を正の参照へ混ぜない。

この縦開口テストは実行していない。別モデルで作られた新しい3枚が
ユーザーの好みに近かったため、D1の修正より新候補の再現性確認を優先する。
D0、D1、A1、A2、B1、B2は引き続き負の対照とし、新候補へ混ぜない。

## 別モデルの3枚はV2.3顔候補として固定試験へ進める

ユーザーは別モデルで作った3枚を「結構好み」と評価し、V3.0まで
大きく変えずV2.3として扱う案を示した。現時点で3枚は同じ人物に見えるが、
顔固定に成功したとはまだ判定しない。同じ駅、同じ制服、近い微笑みが
本人らしさを補っている可能性が残るためである。

3枚の記録と暫定的な役割は次のとおり。

- 顔アンカー候補:
  `/home/takahiro/.codex/attachments/5bfecbee-664a-419b-ab00-c63882fc271f/20260819_219844051.jpeg`
  (`1024x1536`, SHA-256
  `9cdee2f3df4adf99a1d3aeeacbca1e17633ae4f8a99c835a727d68343f758024`)
- 立ち姿のホールドアウト:
  `/home/takahiro/.codex/attachments/e711366f-6c30-4d2f-888d-c96bca614261/ChatGPT Image 2026年8月19日 14_16_51.png`
  (`941x1672`, SHA-256
  `22e5ed7e24a449d3a5459da17f72fdb5ccb881ce2a8c051b71b88168f974cf17`)
- 座り姿と斜め角度のホールドアウト:
  `/home/takahiro/.codex/attachments/3e49e3a5-0bf0-41fd-9450-669c0307107a/ChatGPT Image 2026年8月19日 14_17_03.png`
  (`941x1672`, SHA-256
  `5aa7e1758c16f86f383b5ebeb086b732f850d7fb2a4d1f96268aabdb9a562638`)

顔だけを同じ大きさへ切り出した比較は、次へ保存した。これは評価用であり、
正式資産や生成参照にはしない。

`/home/takahiro/.codex/visualizations/2026/08/19/01a017d1-a2a4-7513-b31f-81ede290da2b/v23-identity-audit/v23-face-comparison.png`

3枚で安定しているのは、丸みのある頬と尖りすぎない小さな顎、
大きいが真円ではない目、暗い上部と蜂蜜色の下部に分かれた虹彩、
小さな鼻、低い位置の短い閉じ口である。茶色のボブ、画面右側の
低いサイドポニー、一本の青いヘアピンもよく揃っている。

まだ揺れているのは、目の縦幅、虹彩の明るさと反射位置、眉の見え方、
口の横幅である。とくに髪型と青いアクセサリーは人物識別を強く助けるため、
顔が少し変わっても同じ人物に見えてしまう。現在の3枚は再現可能性の
強い予備証拠ではあるが、独立した新規生成への固定を証明していない。

### 顔固定は無地背景の6枚で先に判定する

次の生成が承認された場合、入力に使うのは1枚目から作る顔中心のクロップ
だけにする。2枚目と3枚目は結果比較まで見せない。3枚を同時に入力すると、
駅、制服、髪型の一致が顔の判定を助け、循環した評価になる。

第1段階では、同じ簡素な服、無地背景、開いた目、閉じ口の微笑みを固定し、
次の6枚を独立生成する。数値の年齢指定は使わない。

1. 正面の顔アップを2枚作る。
2. 斜め向きのバストアップを2枚作る。
3. 正面の全身を2枚作る。

変えるのは顔の角度と画面内の大きさだけとする。顔輪郭、頬と顎、
目の形と間隔、虹彩構造、鼻と口の位置を、同じ大きさに切り出した顔で判定する。
髪、服、背景、全体の画風は、顔の不一致を救済する材料にしない。

6枚すべてが顔の5項目を満たせば「固定できた」、5枚なら
「有望だが未固定」、4枚以下なら「固定失敗」とする。同じ条件の2枚で
同じ部位が崩れた場合も、その特徴は固定できていない。第1段階を通過した後だけ、
駅の立ち姿2枚と座り姿2枚を作り、ホールドアウトの2枚と比較する。

### 第一段階は5枚合格で「有望だが未固定」になった

ユーザーの`GO`を受け、組み込みの`image_gen`を使って6枚を生成した。
参照に使ったのは、1枚目から顎までを含めて切り出した次の1枚だけである。
立ち姿と座り姿のホールドアウト、D系、V2.2の既存画像は入力していない。

- Anchor crop:
  `/home/takahiro/.codex/visualizations/2026/08/19/01a017d1-a2a4-7513-b31f-81ede290da2b/v23-identity-audit/v23-face-anchor-candidate.png`
- Dimensions: `900x900`
- SHA-256:
  `587311f0b33427764cbe4d41608757c3282aa783da6520cd05f41c9d39e2451e`

全条件で、顔、目、虹彩、眉、鼻、口、髪の核を同じ文章で固定した。
無地の暖色背景、白いTシャツ、紺のパンツ、白いスニーカー、
開いた目と閉じ口の微笑みも共通にした。数値の年齢指定は使っていない。
条件間で変えたのは、次の構図だけである。

- A: 正面の顔アップ
- B: 画面左を向く斜めバストアップ
- C: 正面の全身立ち

各条件は同じ参照から独立に2回生成した。生成結果は研究用の外置きコピーへ
保存し、Gitには追加していない。

`/home/takahiro/.codex/visualizations/2026/08/19/01a017d1-a2a4-7513-b31f-81ede290da2b/v23-identity-audit/`

外置きコピーのファイル名は、`v23-a1-front-close.png`、
`v23-a2-front-close.png`、`v23-b1-three-quarter.png`、
`v23-b2-three-quarter.png`、`v23-c1-fullbody.png`、
`v23-c2-fullbody.png`である。

- A1: `exec-291720e5-69ae-4747-8b03-1f1a7e329631`,
  `1254x1254`, SHA-256
  `e170c3c6b88a6dc8ee957694d9325b16e663ae9b7aaa2bba397113bb5e007b3a`
- A2: `exec-7ba77204-0e84-45ce-99b6-da7e667323bb`,
  `1254x1254`, SHA-256
  `aafd665f68c2d15b07705c9deff0bf7a35f629c7732df22d862e559c878b0a7c`
- B1: `exec-aafc1170-2b80-4bbe-8562-3311ed989098`,
  `1122x1402`, SHA-256
  `e6a72b8e23dbf6293bb311bd18bb1556abe1d4bac30385c8aa6d58ec77332904`
- B2: `exec-608e29a6-c1b3-4afb-84dd-40c6cdb8d98d`,
  `1122x1402`, SHA-256
  `5f8825a2384dfb1a71e6c4f57838979dbbdba38455b1e9e36ae5d617c092c149`
- C1: `exec-91ad7785-25e8-46b2-b2d7-a6b9b49aea32`,
  `887x1774`, SHA-256
  `f3ce5fb727ab88e4db71cbaffc385046c33d3d5b0f5eb9d7d0668d994caf57a6`
- C2: `exec-c116f425-9b3b-447d-a901-c5faf6ba1a93`,
  `1024x1536`, SHA-256
  `176f19007b82fc0c2d549ec3f35311b5478b232edb9f890c79293f5564c32a48`

顔を同程度の大きさへ切り出した比較は、次へ保存した。

`/home/takahiro/.codex/visualizations/2026/08/19/01a017d1-a2a4-7513-b31f-81ede290da2b/v23-identity-audit/v23-six-sample-face-grid.png`

この比較画像のSHA-256は、
`d8e711f8068b9a4a2801664e5a5566a39d6b622da36ea10b081374b82027a432`
である。

顔輪郭、目の形、目の配置、虹彩、鼻と口の5項目を、髪、服、背景で
救済せずに判定した。結果は次のとおり。

| Candidate | Face gate | Composition gate |
| --- | --- | --- |
| A1 | 5項目すべて合格 | 正面アップ合格 |
| A2 | 5項目すべて合格 | 正面アップ合格 |
| B1 | 5項目すべて合格 | 斜め角度が浅く部分合格 |
| B2 | 5項目すべて合格 | ほぼ正面へ戻り部分合格 |
| C1 | 5項目すべて合格 | 全身構図合格 |
| C2 | 虹彩、鼻と口は合格。輪郭、目の開き、目配置は境界 | 全身構図合格 |

A1、A2、B1、B2、C1の5枚は顔ゲートを通った。C2は、下顔面が少し短く、
目が横長かつ小さくなり、汎用顔へ寄ったため境界とした。全身化によって
顔の画素数が減るほど、目の開き、輪郭、虹彩の細部が弱くなる傾向がある。

ユーザーも比較画像を確認し、「C2だけはちょっと違う」と判定した。
これにより、C2は顔不一致で不採用とし、正の参照や後続生成のアンカーには
使わない。A1、A2、B1、B2、C1は、この第一段階における同一人物の
顔合格例とする。ただし、この判定は形式的なアンカー承認ではない。

事前に決めた判定基準へ当てはめると、今回は5/6で
「有望だが未固定」である。顔アンカー候補は機能したが、縮小を含む6/6の
再現性は証明できなかった。B1とB2も顔は一致した一方、明確な斜め角度を
作れていない。1枚目、A群、B群、C群のいずれも正式アンカーへ昇格しない。

次に進む場合は、ユーザーの6枚への顔判定を先に受ける。その後も必要なら、
Bは遠い目と片側の頬が縮む程度まで斜め角度を強め、Cは顔の画素数を確保した
全身構図で再試験する。駅のホールドアウト試験は、この二点が通るまで始めない。

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
