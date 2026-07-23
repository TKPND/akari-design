import assert from "node:assert/strict";
import test from "node:test";

import {
  ameNoSeiNiShiteDocument,
  pages,
} from "./ame-no-sei-ni-shite-document.mjs";

test("rain-day artbook has 18 A4 landscape pages", () => {
  assert.equal(ameNoSeiNiShiteDocument.id, "akari-v1.2-ame-no-sei-ni-shite");
  assert.deepEqual(ameNoSeiNiShiteDocument.pageSize, {
    widthIn: 11.69,
    heightIn: 8.27,
    previewWidth: 3508,
    previewHeight: 2480,
  });
  assert.equal(pages.length, 18);
  assert.deepEqual(
    pages.map((page) => page.page),
    Array.from({ length: 18 }, (_, index) => index + 1),
  );
});

test("scene pages use one accepted image and at most one dialogue", () => {
  const scenePages = pages.filter((page) => page.sceneId);
  assert.equal(scenePages.length, 12);
  for (const page of scenePages) {
    assert.equal(page.sourceInputs.length, 1);
    assert.ok(page.dialogue.length <= 1);
    assert.match(page.sourceInputs[0], /^scene-(0[1-9]|1[0-2])$/);
  }
});

test("derived pages reuse scene 03, 06, and 12", () => {
  assert.equal(pages[0].sourceInputs[0], "scene-06");
  assert.equal(pages[1].sourceInputs[0], "scene-03");
  assert.equal(pages[15].sourceInputs[0], "scene-12");
});

test("accepted asset paths and release targets stay inside the artbook package", () => {
  for (const [sceneId, path] of Object.entries(ameNoSeiNiShiteDocument.assetPaths)) {
    assert.match(sceneId, /^scene-(0[1-9]|1[0-2])$/);
    assert.equal(
      path,
      `akari-v1.2/artbooks/ame-no-sei-ni-shite/accepted/${sceneId}.webp`,
    );
  }
  assert.equal(
    ameNoSeiNiShiteDocument.outputPdf,
    "akari-v1.2/artbooks/ame-no-sei-ni-shite/release/akari-v1.2-ame-no-sei-ni-shite.pdf",
  );
  assert.equal(
    ameNoSeiNiShiteDocument.previewDir,
    "build/ame-no-sei-ni-shite-page-previews",
  );
});

test("artbook renderer emits native dialogue and copy text", async () => {
  const { renderHtml } = await import("./render-html.mjs");
  const html = renderHtml(ameNoSeiNiShiteDocument);
  assert.match(html, /class="sheet layout-artbook-cover"/);
  assert.match(html, /data-block-type="artbook-plate"/);
  assert.match(html, /data-block-type="artbook-copy"/);
  assert.match(html, /一本しかないけど、まあいっか/);
  assert.match(html, /雨は、もうやんでいた。/);
  assert.match(html, /accepted\/scene-12\.webp/);
});

test("renderer exposes the rain-day artbook document", async () => {
  const renderer = await import("./render.mjs");
  assert.deepEqual(
    renderer.parseRenderArgs([
      "--document",
      "ame-no-sei-ni-shite",
      "--previews",
      "--pdf",
    ]),
    { documentName: "ame-no-sei-ni-shite", commands: ["previews", "pdf"] },
  );
  assert.equal(
    (await renderer.resolveDocument("ame-no-sei-ni-shite")).id,
    ameNoSeiNiShiteDocument.id,
  );
});
