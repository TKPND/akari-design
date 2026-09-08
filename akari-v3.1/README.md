# Akari v3.1 — シルバー細ピンとグレー靴下

黒髪ボブ版v3.0を土台に、S1の明るいシルバー細ピンと、
G2のミディアムグレー靴下を採用した作業用デザイン。

- [S1：ヘアアクセ参照](references/S1-silver-slim-pin.png)
- [G2：現在の全身ベース](references/G2-silver-pin-gray-socks-full-body.png)

## 作業を再開する

まず [design-state.json](design-state.json) を読む。
このパッケージは、同じリポジトリ内の `akari-v3.0/` と一緒に使う。
現在の参照パスは `akari-v3.1/` からの相対パスで、画像は原寸PNG。

| 役割 | 基準 |
| --- | --- |
| 顔・黒髪ボブ・描き方 | [P1](../akari-v3.0/references/P1-user-pro-portrait.png) |
| 普段の閉じ口の微笑み | [P2](../akari-v3.0/references/P2-quiet-smile.png) |
| 全身・制服・靴下の色 | [G2](references/G2-silver-pin-gray-socks-full-body.png) |
| 細ピンの形・色・位置 | [S1](references/S1-silver-slim-pin.png) |
| 継承した体型・衣装構造 | [P6](../akari-v3.0/references/P6-relaxed-full-body.png) |

生成前に、修正対象と必要な参照原本を開き、画像ごとの役割を指定する。
G2の全身に描かれた小さい顔で、P1・P2の顔の基準を置き換えない。

細ピンは明るいシルバーの細い直線形を1本、本人の左側・耳の少し上に付ける。
S1とG2では画面右側に見える。靴下はG2のミディアムグレー、膝下丈、
不透明なリブ編みを基準とする。P6の紺色は履歴上の色として扱う。

## 選択と来歴

ユーザーの「S1がいいね。」「G2にしよう」を
[selection.json](selection.json) に記録した。

- [細ピンの生成記録](history/S1-generation.json)：青い細ピンAからS1への色変更
- [全身の生成記録](history/G2-generation.json)：P6への細ピン追加とG2への靴下色変更
- [画像一覧とSHA-256](asset-inventory.json)
- [検証記録](validation.json)

`history/` 内の青い細ピンと紺色靴下の画像は、選択画像へ至る中間素材。
現在の色はS1・G2を参照する。必要な中間画像とプロンプトは同梱している。
S1の生成記録に残る `build/` のパスは元の探索場所を示す履歴情報で、
現在の生成入力には使わない。

内蔵image_genで生成し、選択画像は再加工せず保存した。
生成モデル名はツール応答に公開されていないため、不明として記録している。
