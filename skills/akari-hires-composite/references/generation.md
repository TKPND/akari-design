# 生成・参照・構図

## 参照を決める

現在のリポジトリと依頼された版を確認する。版のREADME、design-state.json、reference-set.jsonを優先し、履歴の数値や旧版の顔で上書きしない。
生成前に原寸参照と編集対象をview_imageで開く。画像生成ツールの実際に公開された入力形式に従う。
内蔵image_genが使える環境ではそれを使い、寸法指定を増やすためだけに別APIやCLIへ切り替えない。

V4.0の現在の役割は次のとおり。将来の変更はリポジトリの選択状態で確認する。

| 入力 | 役割 |
| --- | --- |
| `akari-v4.0/references/V11-novelai-v5-curated.png` | 顔、グレーの目、黒いボブ、一本の銀ピン、軽い線と淡いセル塗り |
| `akari-v4.0/references/B06-full-body.png` | 体格、四肢の長さと柔らかい量感。小さい顔は顔の基準にしない |
| 依頼に合う場面例 | 明示した衣装・小物・雰囲気のみ |
| 全体原画 | 今回の構図・ポーズ・カメラ・照明 |
| 全体原画からの領域ガイド | 今回の領域の正確な画角と切り取り位置 |

B06の比較用衣装は固定制服ではない。数値年齢やadult-woman指定を追加しない。
V11の銀ピンは本人の左側で、正面なら画面右。ポーズに応じて見え方が変わる。
靴下の見える布は柔らかく不透明、浅く控えめなしわを保つ。靴で隠れたつま先を描かせない。
顔中心の構図ではV11を主に使い、B06は体格が見える範囲の補助とする。

アルバムが接続されている場合、各生成の前に最新reviewsを一度読み、image_idをcatalogへ対応させる。
該当するお気に入り・next_reference・keep/changeを原画と合わせて確認する。
直前に取得した同じ生成工程のスナップショットは使える。取得日時と使用した評価を保存する。
取得できなければその事実を短く伝え、手元の履歴を最新取得済みとは扱わない。
評価は好みの入力であり、顔や体格の基準の変更、採用、commit、公開の許可ではない。

## 画面と人物の大きさ

ポートレートには「縦向きの画面」と「人物中心の画角」という別の意味がある。
依頼の用途から、比率と画角をそれぞれ決める。既出条件で決められない場合だけ、結果に影響する不足情報を確認する。

| 用途の例 | キャンバスの例 | 分割の考え方 |
| --- | --- | --- |
| 人物と背景を楽しむ壁紙 | 3840×2160、16:9 | 背景の重なり領域と、頭・胴・脚の意味に沿った領域 |
| 縦長壁紙 | 2160×3840、9:16 | 頭と肩、胴と手、下半身の連続性を先に考える |
| 顔・上半身のポートレート | 用途に応じ3:4や4:5など | 顔全体・髪・ピンを一つの領域に収め、肩・衣装・背景を分ける |

縦長を作るとき、横長原画を中央で切り落として済ませない。縦構図の全体原画から始める。
顔の横の手には前腕・肘・肩とのつながりが必要。腰を横切る腕は広い重なりを使う。
顔を左右に割らず、膝・手首を接合線に置かない。
人物全体の関係が崩れる場合は、その接続を含む大きな領域を作る。
細部密度を上げるためだけに人体を細切れにしない。

全体原画の顔・手・シルエット・靴先の切れを確認してから分割する。
見切れが意図に反するならこの段階で構図を修正する。比較する両側では同じ画角を保つ。
最初の領域は10〜20%程度の重なりを出発点にしてよいが、必要な文脈と接合位置で調整する。
縦長2×3、横長3×2などの固定グリッドは下書きであり、完成の分割規則ではない。

## 領域生成の入力例

実在する入力を開き、以下の役割を今回の画像に合わせて指定する。
ガイドのぼやけは配置情報として扱い、顔の原寸参照で描き方と形を補う。
全体原画からガイドへ渡す役割を明確にし、前の生成領域を次の顔基準にしない。

```text
Create one high-detail region for a larger assembled illustration.
Input 1 is the exact region guide: preserve its crop, pose, camera and object positions.
Input 2 is the full composition for lighting and spatial context only. Output only Input 1's region.
Input 3 is native V11: the authority for Akari's face, grey eyes, black bob, single slim silver pin,
light linework and pastel cel rendering. Do not copy the guide's blurred facial detail.
Input 4 is native B06: body balance and soft limb volume only, not its wardrobe or small face.
Keep the complete head and raised hand with their visible connecting arm inside this region.
Match the existing clothing, lighting and scene. Draw clean intentional details at native output
resolution, with no extra border, caption, panel layout or artificial sharpening halos.
```

背景だけの領域なら顔・体格の指示と不要な入力を省く。
実在しないInput番号を残さず、入力順と参照の役割を記録する。
toolが返す実寸を測る。プロンプトに「4K」と書いても原寸4Kの保証にはならない。
出力が大きく構図を変えた場合は無理なワープで押し込まず、領域・ガイド・生成を見直す。

## 保存と失敗の扱い

run内で `references/`, `native/`, `prompts/`, `records/` を分け、原寸PNGを再圧縮せず保存する。
各生成にID、入力順、入力の役割とSHA-256、プロンプト、実寸、生成IDまたは取得可能な来歴、成否を持たせる。
成功数、失敗数、合成対象IDをそれぞれ記録する。

| 状況 | 処理 |
| --- | --- |
| 画像は表示されたがローカルファイルがない | toolの保存先を探す。見つからなければ当該rolloutを構造的にparseし、該当生成のPNG payloadを署名確認して復元する。base64を端末へ大量出力しない |
| 通信・保存処理が失敗 | 生成済みかを先に調べる。重複生成を避け、必要な範囲で復旧する |
| 出力が拒否された | 拒否を記録し、回避目的の言い換えや繰り返しをしない。既存の成功領域だけで成立するか評価する |
| 領域が欠けても合成できる | selected_region_idsから明示的に除外し、他領域の被覆と通常拡大が残る範囲を記録する |
| 顔・腕など重要部分が成立しない | 未完成を完成扱いにせず、具体的な不足を伝える |

合成手順は[assembly.md](assembly.md)を読む。
