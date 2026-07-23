import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";
import test from "node:test";
import { chromium } from "playwright";
import { pages, naturalFormDocument } from "./natural-form-document.mjs";
import { renderHtml, sourceImagePath, writeHtml } from "./render-html.mjs";

const expectedPages = [
  [1, "cover-natural-form", "Cover / Natural Form"],
  [2, "inheritance", "v1.1 to v1.2 Inheritance"],
  [3, "identity-lock", "Identity Lock"],
  [4, "natural-front-stance", "Natural Front Stance"],
  [5, "back-and-45-views", "Back and 45-degree Views"],
  [6, "weight-and-joints", "Weight and Joint Guidelines"],
  [7, "floor-sitting-master", "Floor Sitting Master"],
  [8, "floor-sitting-anatomy", "Floor Sitting Anatomy Notes"],
  [9, "indoor-sock-feet", "Indoor Sock Feet"],
  [10, "morning-bed-hair", "Morning Bed Hair"],
  [11, "expression-gradient", "Sleepy-to-Soft-Smile Expressions"],
  [12, "d01-morning-validation", "D01 Morning Validation"],
  [13, "do-dont", "Do / Don't"],
  [14, "source-review-status", "Source Manifest and Review Status"],
];

const expectedAcceptedPaths = [
  "akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png",
  "akari-v1.2/accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png",
  "akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png",
  "akari-v1.2/accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_r02.png",
  "akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png",
  "akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png",
  "akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-1_sleepy-neutral_r01.png",
  "akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-2_sleepy-secure_r01.png",
  "akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-3_loosened-mouth_r01.png",
  "akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-4_soft-smile_r01.png",
  "akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-standing_r01.png",
  "akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-seated_r01.png",
  "akari-v1.2/accepted/daily-validation/akari-v1.2_d01_morning-bedside_r01.png",
];

test("Natural Form document exposes the v1.2 release paths", () => {
  assert.equal(naturalFormDocument.id, "akari-v1.2-natural-form-core");
  assert.equal(naturalFormDocument.title, "Akari v1.2.0 Natural Form Core Settings");
  assert.equal(
    naturalFormDocument.outputPdf,
    "akari-v1.2/release/akari-v1.2-core-settings.pdf",
  );
  assert.equal(naturalFormDocument.previewDir, "build/akari-v1.2-page-previews");
  assert.equal(naturalFormDocument.siteHtml, "build/akari-v1.2-site/index.html");
});

test("Natural Form document follows the approved 14-page sequence", () => {
  assert.deepEqual(
    pages.map(({ page, id, title }) => [page, id, title]),
    expectedPages,
  );
});

test("Natural Form asset map contains only the 13 accepted package PNGs", () => {
  const paths = Object.values(naturalFormDocument.assetPaths);
  assert.deepEqual(paths.toSorted(), expectedAcceptedPaths.toSorted());
  assert.equal(paths.some((path) => path.includes("source/candidates/")), false);
  assert.equal(paths.some((path) => path.includes("comparisons/")), false);
});

test("Natural Form pages use supported blocks and mapped image sources", () => {
  const supported = new Set(["image", "guide-lines", "note-list"]);
  const imageSources = [];

  for (const page of pages) {
    assert.ok(page.sourceInputs.length > 0, `${page.id} has no source inputs`);
    for (const block of page.blocks) {
      assert.ok(supported.has(block.type), `${page.id} uses ${block.type}`);
      if (block.type === "image") {
        for (const image of block.images) {
          imageSources.push(image.source);
          assert.equal(
            sourceImagePath(image.source, naturalFormDocument),
            naturalFormDocument.assetPaths[image.source],
          );
        }
      }
    }
  }

  assert.deepEqual(
    [...new Set(imageSources)].toSorted(),
    Object.keys(naturalFormDocument.assetPaths).toSorted(),
  );
});

test("Natural Form HTML contains all release-native text", () => {
  const html = renderHtml(naturalFormDocument);
  for (const [, id, title] of expectedPages) {
    assert.match(html, new RegExp(`id="${id}"`));
    assert.ok(html.includes(`<h1>${title}</h1>`));
  }
  for (const term of [
    "v1.2.0",
    "C01",
    "C02",
    "C03",
    "C04",
    "C05",
    "C06",
    "C07",
    "D01",
    "Gate 4",
    "release",
  ]) {
    assert.ok(html.includes(term), `missing native text: ${term}`);
  }
});

test("renderer accepts the natural-form document name", async () => {
  const renderer = await import("./render.mjs");
  assert.deepEqual(
    renderer.parseRenderArgs(["--document", "natural-form", "--previews", "--pdf"]),
    { documentName: "natural-form", commands: ["previews", "pdf"] },
  );
  assert.equal((await renderer.resolveDocument("natural-form")).id, naturalFormDocument.id);
});

test("Natural Form pages contain loaded images and page content", async (t) => {
  const target = writeHtml(undefined, naturalFormDocument);
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  t.after(async () => browser.close());

  const browserPage = await browser.newPage({
    viewport: { width: 3840, height: 2160 },
  });
  await browserPage.goto(pathToFileURL(target).href, { waitUntil: "load" });
  await browserPage.evaluate(async () => {
    await Promise.all(
      [...document.images].map((image) => {
        if (image.complete && image.naturalWidth > 0) return undefined;
        return new Promise((resolve, reject) => {
          image.addEventListener("load", resolve, { once: true });
          image.addEventListener("error", reject, { once: true });
        });
      }),
    );
    await document.fonts.ready;
  });

  const issues = await browserPage.evaluate(() =>
    [...document.querySelectorAll(".sheet")]
      .map((sheet) => {
        const images = [...sheet.querySelectorAll("img")];
        return {
          page: sheet.dataset.page,
          overflowX: sheet.scrollWidth - sheet.clientWidth,
          overflowY: sheet.scrollHeight - sheet.clientHeight,
          brokenImages: images.filter((image) => image.naturalWidth === 0).length,
          badObjectFit: images.filter((image) => getComputedStyle(image).objectFit !== "contain")
            .length,
        };
      })
      .filter(
        (issue) =>
          issue.overflowX > 1 ||
          issue.overflowY > 1 ||
          issue.brokenImages > 0 ||
          issue.badObjectFit > 0,
      ),
  );

  assert.deepEqual(issues, []);
});
