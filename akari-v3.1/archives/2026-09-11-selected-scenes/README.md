# Akari v3.1 — 選択済みシーンとアルバム作品の保存

2026-09-11、ユーザーの「じゃあそれをコミットして。」に基づき、
優先度「高」として提示した25枚と来歴を保存した。
原寸画像・プロンプト・元の生成記録はバイトを変更せず、修正前の画像と評価用クロップも保存している。

## 保存範囲

- N16・N20・N21・N22、N24・N27・N28・N30：ユーザーが選んだ家でのシーン8枚。
- SU03・SU05・SU06、SU08・SU11・SU14：ユーザーが選んだ制服の方向性6枚。
- AF01〜AF11：アルバムに掲載した作品11枚。最終ファイルは保存時のアルバム一覧とSHA-256で照合した。
- 生成に必要な入力画像、各入力の役割、修正履歴、選択記録、生成時の評価スナップショット。

これは作品と来歴の保存であり、顔・表情・衣装・靴下の正式基準を変更するものではない。
P1/P2、原寸U1/L1、F09の既存の役割を維持する。AF09〜AF11の靴下の試作も、新しい質感基準へ昇格させない。
アルバムアプリ本体、残りの候補、ビルド出力、依存パッケージは今回の保存範囲に含まない。

## 保存した画像

| ID | 内容 | 原寸画像 |
| --- | --- | --- |
| AF01 | 隣に座った、そのあと | [PNG](scenes/AF01/AF01-beside-you.png) |
| AF02 | 静かに、隣で | [PNG](scenes/AF02/AF02-quiet-beside-you.png) |
| AF03 | 隣で、肩の力を抜いて | [PNG](scenes/AF03/AF03-relaxed-beside-you.png) |
| AF04 | 話の途中で、うとうと | [PNG](scenes/AF04/AF04-dozing-mid-conversation-r2.png) |
| AF05 | 今日は、ちょっと疲れた | [PNG](scenes/AF05/AF05-a-little-tired-r3.png) |
| AF06 | クッションに頬を預けて | [PNG](scenes/AF06/AF06-cheek-on-cushion.png) |
| AF07 | 少し休んで、目が合う | [PNG](scenes/AF07/AF07-eye-contact-after-rest.png) |
| AF08 | ベッドでひと眠り | [PNG](scenes/AF08/AF08-peaceful-bed-nap.png) |
| AF09 | 横座り、自然な足先 | [PNG](scenes/AF09/AF09-natural-side-sit-feet.png) |
| AF10 | 足を下ろして、ひと息 | [PNG](scenes/AF10/AF10-feet-down-rest-r2.png) |
| AF11 | 少し丸まって、話のつづき | [PNG](scenes/AF11/AF11-cozy-conversation.png) |
| N16 | リボン、結べたよ | [PNG](scenes/N16/image.png) |
| N20 | それ、ちょっとずるい | [PNG](scenes/N20/image.png) |
| N21 | うん、聞いてる | [PNG](scenes/N21/image.png) |
| N22 | まだ起きてるよ | [PNG](scenes/N22/image.png) |
| N24 | これ、しおりにしたよ | [PNG](scenes/N24/image.png) |
| N27 | も、笑わせないで | [PNG](scenes/N27/image.png) |
| N28 | それで、どうなったの？ | [PNG](scenes/N28/image.png) |
| N30 | もう少し、ここにいて | [PNG](scenes/N30/image.png) |
| SU03 | 深緑ベスト × タータン | [PNG](scenes/SU03/image.png) |
| SU05 | グレーボレロ × くすみローズ | [PNG](scenes/SU05/image.png) |
| SU06 | 淡ブルーの夏ワンピース制服 | [PNG](scenes/SU06/image.png) |
| SU08 | アイボリーベスト × 深緑リボン | [PNG](scenes/SU08/image.png) |
| SU11 | グレージュ × ココアチェック | [PNG](scenes/SU11/image.png) |
| SU14 | 白セーラー × 水色チェック | [PNG](scenes/SU14/image.png) |

## 記録の読み方

- [manifest.json](manifest.json)：今回の保存範囲、最終画像、入力の役割、生成呼び出し、全ファイルのハッシュ。
- [path-resolutions.json](path-resolutions.json)：元の生成記録のJSON Pointerから、保存先の相対パスへの対応表。
- `scenes/`：元のシーン別ファイルをそのまま保存。
- `history/`：ユーザーの選択、アルバム掲載、生成当時の評価の記録。
- `dependencies/`：入力画像と、保存作業時点の参照文書のスナップショット。

manifestと対応表の有効パスは、この保存ディレクトリを基準とする相対パス。
元のJSON・プロンプト・文書は履歴なので、当時の`tmp/`パス、絶対パス、
`committed: false`や選択待ちの状態をそのまま保持している。現在の保存状態はmanifestを参照する。
文書スナップショット内のリンクは元文書の配置を前提とした履歴であり、閲覧用の有効リンクではない。
次の探索先など保存範囲外の参照も、履歴の一部として残している。

入力に使ったN29の画像は来歴のために保存しており、今回の25枚には含めない。
評価は生成当時のスナップショットで、今回ライブ取得したものではない。
画像の品質を新たに採点したり、内蔵生成ツールのモデル名を確定したりする作業は行っていない。

## 検証

[validate.py](validate.py)はPython標準ライブラリだけで実行でき、`tmp/`や生成ツールのキャッシュを必要としない。
全保存ファイルのSHA-256とサイズ、PNGのCRC・展開後ピクセルストリーム、
最終画像と保存時のアルバム一覧の一致、入力・プロンプト・出力のハッシュ、相対パスを検証する。

```bash
python3 akari-v3.1/archives/2026-09-11-selected-scenes/validate.py
```

元の作業ディレクトリが残っている場合、`--verify-sources /absolute/path/to/akari-design`を付けると、
保存した`tmp/`由来のファイルが元と同一であることも確認できる。

選択の根拠は以下の記録に保存している。

- [2026-09-09-a2-close-moments/selection-before-uniform-exploration.json](history/2026-09-09-a2-close-moments/selection-before-uniform-exploration.json)
- [2026-09-09-a2-next-eight/continuation-selection.json](history/2026-09-09-a2-next-eight/continuation-selection.json)
- [2026-09-09-school-uniform-expansion/selection.json](history/2026-09-09-school-uniform-expansion/selection.json)
- [2026-09-09-school-uniform-six/continuation-selection.json](history/2026-09-09-school-uniform-six/continuation-selection.json)
- [2026-09-10-album-feedback/batch-AF02-AF05.json](history/2026-09-10-album-feedback/batch-AF02-AF05.json)
- [2026-09-10-album-feedback/feedback-snapshot.json](history/2026-09-10-album-feedback/feedback-snapshot.json)
- [2026-09-11-album-feedback/batch-AF06-AF08.json](history/2026-09-11-album-feedback/batch-AF06-AF08.json)
- [2026-09-11-album-feedback/feedback-snapshot.json](history/2026-09-11-album-feedback/feedback-snapshot.json)
- [2026-09-11-natural-sock-fit/batch-AF09-AF11.json](history/2026-09-11-natural-sock-fit/batch-AF09-AF11.json)
- [2026-09-11-natural-sock-fit/feedback-snapshot.json](history/2026-09-11-natural-sock-fit/feedback-snapshot.json)
