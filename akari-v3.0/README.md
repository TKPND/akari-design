# Akari v3.0 — 作業用デザインとシチュエーション集

2026年9月7日の黒髪ボブ版v3.0を、別環境でも続けられる形で保存した作業パッケージ。
採用済み参照13枚、P16とS01〜S24のシチュ絵25枚、生成プロンプト、選択記録を含む。
正式設定リリース前の作業用資料である。

## 作業を再開する

このディレクトリを含むcommitを取得し、まず [design-state.json](design-state.json) を読む。
現在の作業用manifestのパスは、すべてこの `akari-v3.0/` ディレクトリからの相対パス。
画像、HTML、PDFの閲覧にビルドや外部サービスは不要。

- [設定資料HTML](working-reference/akari-v3.0-working-reference.html)：画像を押すと拡大できる4ページの参照集
- [設定資料PDF](working-reference/akari-v3.0-working-reference.pdf)：同じ参照集の保存済みPDF
- [シチュ絵24枚の一覧](situations/index.html)
- [お気に入り5枚の一覧](situations/favorites.html)
- [P16：放課後の帰り道、隣で思わず笑う](situations/P16-walk-home-laugh.png)

## 参照の優先順位

| 役割 | 基準 | 扱い |
| --- | --- | --- |
| 顔・髪・描き方 | [P1](references/P1-user-pro-portrait.png) | 本人性の原本。黒髪の丸いボブ、丸みのあるグレーのタレ目、ふっくらした頬、短めの下顔面、頬の斜線 |
| 普段の表情 | [P2](references/P2-quiet-smile.png) | 選択済みの小さな閉じ口の微笑み |
| 全身・服 | [P6](references/P6-relaxed-full-body.png) | 自然な肩幅、健康的な脚、白い半袖開襟シャツと青灰色の縁取り・プリーツスカート、紺の膝下ソックス、白いスニーカー |

P4・P5は角度、P8・P9は日常場面、P10-2・P11・P14・P15は表情、P12・P13は仕草の補助。
各画像の役割、採用時の発言、SHA-256は [参照manifest](references/manifest.json) に記録している。

生成前に、修正対象と必要な参照原本を開いて確認し、入力画像ごとの役割をプロンプトに明記する。
全身画像の小さく省略された顔でP1を置き換えない。
シチュ絵を気に入っても、顔・表情・体型の基準は自動的に変わらない。
以前のv1・v2や、8月のスタイル研究で使った別デザインは今回の生成参照に混ぜない。

## お気に入り

ユーザーが今回添付した5枚を記録した。添付と保存済み原寸PNGのSHA-256は一致。
順番は画像番号順で、好みの順位を表すものではない。

| ID | 場面 |
| --- | --- |
| S01 | [朝の曲がり角でおはよう](situations/S01-morning-greeting.png) |
| S09 | [バス待ちで、ちょっと拗ねる](situations/S09-missed-bus.png) |
| S18 | [踏切待ちの照れ隠し](situations/S18-sunset-crossing.png) |
| S21 | [海沿いで、声が弾む](situations/S21-seaside-laugh.png) |
| S24 | [別れ際の、ありがと](situations/S24-doorway-thanks.png) |

選択記録は [favorites.json](favorites.json)、各場面の参照画像・プロンプト・生成ID・所要時間は
[シチュ絵manifest](situations/manifest.json) にある。ほかの場面は保存済み候補のまま。
S05は余分な指を直した `S05-cold-drink-r2.png` を現行画像にしている。

## 保存範囲と来歴

原寸画像とPDFは元ファイルから無変更で保存した。
HTMLは既存レイアウトを使い、同梱画像へ相対パスでアクセスする。
画像とPDFのサイズ・SHA-256は [asset-inventory.json](asset-inventory.json) で確認できる。
生成モデル名は内蔵image_genの応答に公開されていないため、不明として記録している。
P1はユーザー提供画像で、生成プロンプトは提供されていない。

[history](history/) は当時の作業状態・生成記録・プロンプトの保存先。
この中のローカル絶対パスは来歴情報であり、現在の入力ファイルを探すためのパスではない。
以前の不採用候補すべては同梱していない。体型の経緯を示すB7と、S05の修正前画像は保存した。
現在の作業は、このREADMEと `design-state.json`、2つの作業用manifestを入口にする。

8月の [スタイル研究メモ](docs/akari-v3.0-style-research-checkpoint.md) は別デザインの履歴資料。
現在の黒髪ボブ版の仕様として使わない。
