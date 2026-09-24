# 合成・等倍比較・再現

## 補助スクリプト

Python 3とImageMagick 7の`magick`を使う。追加のPythonライブラリは不要。
`scripts/compose.py`は画像生成を呼ばず、ユーザーが依頼した分割合成の配置と比較を再現する。
意味のある領域選択、マスクの目視判断、顔や人体の検証は自動化していない。

runのルートにlayout.jsonを置く。画像パスはそのJSONがあるディレクトリからの相対パス。
元画像のコピーをrun内に保存して使う。入力画像は書き換えない。
出力は新しいディレクトリを指定する。既存ディレクトリは上書きせずエラーにする。

以下は上半身が中央付近にある縦長画像の**形式例**で、配置済みの構図を保証しない。
実際の原画を見て、特に顔と腕が収まる座標へ変更する。

```json
{
  "canvas": [2160, 3840],
  "master": "native/master.png",
  "max_aspect_drift": 0.02,
  "regions": [
    {
      "id": "head-arm",
      "purpose": "complete head, raised hand and connected arm",
      "rect": [160, 180, 1840, 1640],
      "native": "native/head-arm.png",
      "feather": {"left": [0, 64], "right": [0, 64], "top": [0, 64], "bottom": [0, 96]}
    },
    {
      "id": "torso-hand",
      "purpose": "crossing hand, entire sleeve and waist",
      "rect": [160, 1500, 1840, 1700],
      "native": "native/torso-hand.png",
      "mask": "masks/torso-hand.pgm"
    }
  ],
  "selected_region_ids": ["head-arm", "torso-hand"],
  "qa": [
    {"id": "face", "rect": [740, 320, 700, 700]},
    {"id": "join", "rect": [800, 1450, 700, 500]}
  ]
}
```

この例は人物の一部を描き直し、残りに通常拡大を使う構成。
背景や下半身も高密度にする場合は、必要な領域を追加する。
全キャンバスを再描画したと表現するには、全域の被覆を確認する。

| フィールド | 意味 |
| --- | --- |
| canvas | 最終サイズの幅・高さ。縦横を入れ替えるだけでは構図は変わらない |
| rect | 左上原点の整数x, y, width, height。領域とQAの両方で同じ座標系 |
| max_aspect_drift | 各領域の原寸と配置の比率差を許す上限。masterには適用しない。0.02は試作で使った値で普遍的基準ではない |
| regionsの順序 | 実際の合成順。selected_region_idsの並びは順序指定ではない |
| selected_region_ids | 合成する領域。省略時はすべて。欠けた原画を暗黙に飛ばさない |
| feather | 各端から内側への距離[透明の終わり, 不透明の始まり]、単位px。smoothstepで接続 |
| mask | 配置後の領域と同寸のグレースケール画像。黒は下地、白は新しい領域。featherと排他 |
| マスク指定なし | 領域全体が不透明。境界は目視で確認する |
| qa | 同じ座標・寸法で比較する箇所。合成の両側を同じ倍率にする |

```sh
# 実際に読み込んだスキルの場所を使う。生成原画はまだ不要。
python3 /path/to/akari-hires-composite/scripts/compose.py prepare /path/to/run/layout.json /path/to/run/prepared-r1

# 生成原画と選択したマスクがそろってから実行。
python3 /path/to/akari-hires-composite/scripts/compose.py assemble /path/to/run/layout.json /path/to/run/assembled-r1
```

prepareはbaseline.png、guides/、report.jsonを出す。
assembleは同じ方式のbaseline.png、composite.png、layers/、qa/、report.jsonを出す。
QAのcompare.pngは左が通常拡大、右が合成。切り出した画素数のまま横に連結し、縮小しない。
どちらも基準画像をLanczosで等方的にcover拡大し、中心で必要な端だけを切る。
報告のideal_cover_crop_total_xyは丸め前の理想的な切り落とし総量で、整数の実クロップ座標ではない。
顔・手・靴の端が失われる場合は、原画の構図やキャンバスの比率を先に見直す。
masterの比率差はreport.jsonへ記録するが、自動拒否の閾値は設けていない。prepare後のbaselineと切り落とし量を目視で確認してから領域生成へ進む。
アルファはマスクから作り、完成PNGはsRGB、RGB8。原寸入力は変更しない。

## 細部密度と縦横比

```text
s_master = max(canvas_width / master_width, canvas_height / master_height)
s_region = max(region_width / native_width, region_height / native_height)
relative_sampling_gain = s_master / s_region
aspect_drift = abs((native_width / native_height) / (region_width / region_height) - 1)
```

配置倍率が1に近いほど、原寸の情報を大きく引き伸ばさずに使える。
relative_sampling_gainは画素サンプリングの比で、知覚的画質や正確な復元を保証しない。
返された画像で実測する。想定のネイティブ寸法で成功扱いにしない。
微小な比率差は等方coverと微小クロップで吸収し、大きな比率差は再配置・ガイド・生成を見直す。
エラーを消すためだけにmax_aspect_driftを緩めない。変更する場合は切り落とし範囲を確認して記録する。

## 接合を直す

目・顔輪郭・髪先・銀ピン・手指・袖の輪郭などは、一つの原画の不透明な領域に収める。
二重線に幅広いぼかしを重ねると輪郭が幽霊状に残る。
まず位置と形を比較し、継ぎ目を背景や同じ色の布面へ移す。
必要なら大きい連続領域を作り直す。四肢を引き延ばすワープで一致を強制しない。

重なりの候補帯で見た目が近い箇所を探す場合は、次の最小差分経路が補助になる。
両画像をすでに同じ座標へ置いてから、RGB色差と強い輪郭への罰点を足し、動的計画法で連続する線を選ぶ。
縦継ぎ目なら行ごとのx、横継ぎ目なら列ごとのyを求める。
候補帯は人物の輪郭を避けて目視で設定する。低い色差だけで人体の正しさを判断しない。

```text
cost(x,y) = RGB absolute difference + edge penalty
D(y,x) = cost(x,y) + min(D(y-1,x-1), D(y-1,x), D(y-1,x+1))
```

経路を逆追跡して領域ローカルのグレースケールmaskへ変換する。
初期の狭いフェザー幅は完成サイズで数px〜十数px程度から目視調整する。
8pxが横長試作では有効だったが、どの絵にも固定しない。
経路、候補帯、幅、合成順、マスクのハッシュを保存し、maskフィールドで適用する。
マスクだけを変えた合成は新しい出力ディレクトリへ作り、前の候補と比較する。

## 仕上がりの確認

1. fit表示で全体の視線、体格、色、背景と人物の描き込みの釣り合いを確認する。
2. 同じ座標の100%切り出しで、瞳、髪とピン、両手、袖、腰、脚、靴下、すべての接合部を見る。
3. 輪郭の二重化、腕の切断、手指の増減、衣装の線の途切れ、急な塗りの変化を記録する。
4. 改善した線と、顔の輪郭・表情・服のしわ・背景など変化した内容を分けて伝える。
5. 最終寸法、PNG全デコード、原寸と参照のハッシュ、実際の合成対象IDを確認する。

スクリプトのreport.jsonは寸法、全デコード、入力・出力のSHA-256、原寸と倍率を記録する。
原寸と参照のハッシュは保存直後の生成記録とも照合する。
ファイル検証は目視QAを代行しない。各QAの良否と残る変化はrecords/visual-review.jsonなどへ別に保存する。
基準は非生成のLanczos拡大と明記し、未比較の学習型アップスケーラーとの優劣に広げない。
100%表示は画像1pxをCSS 1pxとして表示する場合、端末の物理pxとの違いも区別する。
比較ページを作った場合は画像寸法とリンク、スライダー両端、100%表示、モバイルの表示を確認する。
ZIPを渡す場合はCRCと各ファイルのハッシュを確認する。

## 実例を参照するとき

同じリポジトリにある場合、横長試作は`tmp/akari-v4.0/2026-09-24-4k-split-pilot/`。
records/layout.json、assembly.json、T06-seam.json、visual-review.jsonが設計根拠になる。
試作のassemble.pyはその座標専用。別構図ではこの補助スクリプトへ新しいlayout.jsonとマスクを渡す。
ローカル試作がなくてもこのスキル単体で実行できる。
