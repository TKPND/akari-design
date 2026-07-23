const book = {
  bookId: "akari-v1.2-ame-no-sei-ni-shite",
  title: "雨のせいにして",
  releasePdf: "release/akari-v1.2-ame-no-sei-ni-shite.pdf",
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

const sceneIds = sceneRows.map(([sceneId]) => sceneId);
const assetPaths = Object.fromEntries(
  sceneIds.map((sceneId) => [
    sceneId,
    `akari-v1.2/artbooks/ame-no-sei-ni-shite/accepted/${sceneId}.webp`,
  ]),
);

function plate(
  page,
  id,
  source,
  time,
  dialogue,
  layout = "artbook-scene",
  crop = "full",
) {
  return {
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
  };
}

function copy(page, id, layout, title, lines) {
  return {
    page,
    id,
    title,
    eyebrow: "",
    layout,
    dialogue: [],
    sourceInputs: [],
    blocks: [{ type: "artbook-copy", title, lines }],
  };
}

export const pages = [
  plate(1, "cover", "scene-06", "", "雨のせいにして", "artbook-cover", "cover"),
  plate(2, "first-rain-detail", "scene-03", "", "", "artbook-detail", "rain-detail"),
  copy(3, "title", "artbook-title", "雨のせいにして", [
    "出かけるはずだった休日は、雨にほどかれていった。",
    "予定がなくなった部屋で、二人の時間だけが残る。",
  ]),
  ...sceneRows.map(([id, time, dialogue], index) =>
    plate(index + 4, id, id, time, dialogue),
  ),
  plate(
    16,
    "afterimage",
    "scene-12",
    "",
    "雨は、もうやんでいた。",
    "artbook-afterimage",
    "afterimage",
  ),
  copy(17, "colophon", "artbook-colophon", "制作ノート", [
    "Akari v1.2",
    "Ame no sei ni shite",
    "Version 1.0.0",
    "2026-07-21",
  ]),
  copy(18, "back-cover", "artbook-back", "雨のせいにして", [
    "akari-v1.2-ame-no-sei-ni-shite",
    "checksums.txt",
  ]),
];

export const ameNoSeiNiShiteDocument = {
  id: book.bookId,
  title: book.title,
  pages,
  assetPaths,
  outputPdf: `akari-v1.2/artbooks/ame-no-sei-ni-shite/${book.releasePdf}`,
  previewDir: "build/ame-no-sei-ni-shite-page-previews",
  siteHtml: "build/ame-no-sei-ni-shite-site/index.html",
  pageSize: {
    widthIn: 11.69,
    heightIn: 8.27,
    previewWidth: 3508,
    previewHeight: 2480,
  },
};
