import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import test from "node:test";
import { tonariNoAkariDocument, pages } from "./tonari-no-akari-document.mjs";

test("tonari document has 24 A4 portrait artwork pages", () => {
  assert.equal(tonariNoAkariDocument.id, "akari-v1.1-tonari-no-akari");
  assert.equal(tonariNoAkariDocument.title, "となりのあかり");
  assert.equal(tonariNoAkariDocument.outputPdf, "dist/akari-v1.1-tonari-no-akari.pdf");
  assert.equal(tonariNoAkariDocument.previewDir, "build/tonari-no-akari-page-previews");
  assert.equal(tonariNoAkariDocument.siteHtml, "build/tonari-no-akari-site/index.html");
  assert.deepEqual(tonariNoAkariDocument.pageSize, {
    widthIn: 8.27,
    heightIn: 11.69,
    previewWidth: 2480,
    previewHeight: 3508,
  });
  assert.equal(pages.length, 24);
  assert.deepEqual(
    pages.map(({ page, id, layout }) => [page, id, layout]),
    [
      [1, "morning-glance", "tonari-portrait"],
      [2, "window-breath", "tonari-portrait"],
      [3, "turn-back-smile", "tonari-portrait"],
      [4, "near-eye-contact", "tonari-portrait"],
      [5, "light-cardigan", "tonari-portrait"],
      [6, "afternoon-stretch", "tonari-portrait"],
      [7, "seated-distance", "tonari-portrait"],
      [8, "shy-half-smile", "tonari-portrait"],
      [9, "roomwear-morning", "tonari-portrait"],
      [10, "walking-beside", "tonari-portrait"],
      [11, "profile-light", "tonari-portrait"],
      [12, "small-peace", "tonari-portrait"],
      [13, "looking-up", "tonari-portrait"],
      [14, "chair-pause", "tonari-portrait"],
      [15, "special-outing", "tonari-portrait"],
      [16, "small-run", "tonari-portrait"],
      [17, "sleepy-afternoon", "tonari-portrait"],
      [18, "almost-touching", "tonari-portrait"],
      [19, "straight-stance", "tonari-portrait"],
      [20, "crouching-gesture", "tonari-portrait"],
      [21, "evening-cardigan", "tonari-portrait"],
      [22, "over-shoulder-voice", "tonari-portrait"],
      [23, "skirt-in-breeze", "tonari-portrait"],
      [24, "homeward-smile", "tonari-portrait"],
    ],
  );
});

test("tonari pages mirror the page manifest as portrait plates", () => {
  const manifest = JSON.parse(
    readFileSync(resolve("source/manifests/tonari-no-akari/page-manifest.json"), "utf-8"),
  );
  assert.deepEqual(
    pages.map(({ page, id, title, displayLine, layout, internalRange, sourceInputs, blocks }) => ({
      page,
      id,
      title,
      display_line: displayLine,
      layout,
      internal_range: internalRange,
      source_inputs: sourceInputs,
      blocks: blocks.map((block) => ({ type: block.type })),
    })),
    manifest.pages.map(({ page, id, title, display_line, layout, internal_range, source_inputs, blocks }) => ({
      page,
      id,
      title,
      display_line,
      layout,
      internal_range,
      source_inputs,
      blocks,
    })),
  );
});

test("tonari renders PDF-native Japanese portrait text", async () => {
  const { renderHtml, sourceImagePath } = await import("./render-html.mjs");
  const html = renderHtml(tonariNoAkariDocument);
  assert.match(html, /<title>となりのあかり<\/title>/);
  assert.match(html, /class="sheet layout-tonari-portrait"/);
  assert.match(html, /朝の合図/);
  assert.match(html, /目が合うだけで、今日が少し近くなる。/);
  assert.match(html, /@page\s*\{\s*size:\s*8\.27in 11\.69in;/);
  assert.equal(
    sourceImagePath("tonari-morning-glance", tonariNoAkariDocument),
    "source/finished/tonari-no-akari/20260701_morning-glance_v1_finish_h05_v1.png",
  );
});

test("tonari uses accepted finish-pass image paths for reviewed pages", async () => {
  const { sourceImagePath } = await import("./render-html.mjs");
  assert.equal(
    sourceImagePath("tonari-morning-glance", tonariNoAkariDocument),
    "source/finished/tonari-no-akari/20260701_morning-glance_v1_finish_h05_v1.png",
  );
  assert.equal(
    sourceImagePath("tonari-window-breath", tonariNoAkariDocument),
    "source/finished/tonari-no-akari/20260701_window-breath_v1_finish_h05_v1.webp",
  );
  assert.equal(
    sourceImagePath("tonari-seated-distance", tonariNoAkariDocument),
    "source/finished/tonari-no-akari/20260701_seated-distance_v1_correction_socks_v1.webp",
  );
});

test("renderer exposes the tonari document", async () => {
  const renderer = await import("./render.mjs");
  assert.deepEqual(
    renderer.parseRenderArgs(["--document", "tonari-no-akari", "--previews", "--pdf"]),
    { documentName: "tonari-no-akari", commands: ["previews", "pdf"] },
  );
  assert.deepEqual(
    renderer.previewFilenames(tonariNoAkariDocument).slice(0, 2),
    ["01-morning-glance.png", "02-window-breath.png"],
  );
});
