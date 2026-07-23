import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { daybookDocument, pages } from "./daybook-document.mjs";

test("daybook document has ten 16:9 scene pages", () => {
  assert.equal(daybookDocument.id, "akari-v1.1-situation-daybook");
  assert.equal(daybookDocument.title, "Akari v1.1 Situation Daybook");
  assert.equal(daybookDocument.outputPdf, "dist/akari-v1.1-situation-daybook.pdf");
  assert.equal(daybookDocument.previewDir, "build/daybook-page-previews");
  assert.equal(daybookDocument.siteHtml, "build/daybook-site/index.html");
  assert.equal(pages.length, 10);
  assert.deepEqual(
    pages.map(({ page, id, layout }) => [page, id, layout]),
    [
      [1, "lakeside-bench", "daybook-cover"],
      [2, "footbridge-breeze", "daybook-scene"],
      [3, "convenience-walk", "daybook-scene"],
      [4, "dock-edge", "daybook-scene"],
      [5, "park-steps", "daybook-scene"],
      [6, "window-seat", "daybook-scene"],
      [7, "rain-cooled-street", "daybook-scene"],
      [8, "station-after-sun", "daybook-scene"],
      [9, "vending-machine-night", "daybook-scene"],
      [10, "golden-hour-return", "daybook-scene"],
    ],
  );
  assert.equal(pages[0].eyebrow, "Akari v1.1 Situation Daybook / Mood Standard");
  for (const page of pages.slice(1)) {
    assert.equal(page.eyebrow, "Akari v1.1 Situation Daybook / Light Notes");
  }
});

test("daybook pages mirror the daybook page manifest", () => {
  const manifest = JSON.parse(
    readFileSync(resolve("source/manifests/daybook/page-manifest.json"), "utf-8"),
  );
  assert.deepEqual(
    pages.map(({ page, id, title, layout, sourceInputs, blocks }) => ({
      page,
      id,
      title,
      layout,
      source_inputs: sourceInputs,
      blocks: blocks.map((block) => ({ type: block.type })),
    })),
    manifest.pages.map(({ page, id, title, layout, source_inputs, blocks }) => ({
      page,
      id,
      title,
      layout,
      source_inputs,
      blocks,
    })),
  );
});

test("every daybook scene has native text notes", () => {
  for (const page of pages) {
    const noteBlocks = page.blocks.filter((block) => block.type === "note-list");
    assert.equal(noteBlocks.length, 2, page.id);
    assert.equal(noteBlocks[0].title, "Atmosphere");
    assert.equal(noteBlocks[0].items.length, 1, page.id);
    assert.equal(noteBlocks[1].title, "Generation Notes");
    assert.equal(noteBlocks[1].items.length, 3, page.id);
  }
});

test("daybook document can be imported from the tools/pdf cwd", () => {
  const result = spawnSync(
    process.execPath,
    [
      "--input-type=module",
      "--eval",
      "import { daybookDocument, pages } from './daybook-document.mjs'; console.log(`${daybookDocument.id}:${pages.length}`);",
    ],
    { cwd: resolve("tools/pdf"), encoding: "utf-8" },
  );

  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.trim(), "akari-v1.1-situation-daybook:10");
});

test("daybook renders PDF-native page text without changing settings render", async () => {
  const { renderHtml, sourceImagePath } = await import("./render-html.mjs");
  const html = renderHtml(daybookDocument);
  assert.match(html, /<title>Akari v1\.1 Situation Daybook<\/title>/);
  assert.match(html, /class="sheet layout-daybook-cover"/);
  assert.match(html, /Lakeside Bench/);
  assert.match(html, /Generation Notes/);
  assert.match(html, /writing/i);
  assert.match(
    html,
    /\.\.\/\.\.\/source\/originals\/situation-daybook-lakeside-bench-cover\.webp/,
  );
  assert.equal(
    sourceImagePath("situation-daybook-lakeside-bench-cover", daybookDocument),
    "source/originals/situation-daybook-lakeside-bench-cover.webp",
  );
});

test("daybook writeHtml default target uses the daybook site path", async () => {
  const { writeHtml } = await import("./render-html.mjs");
  const htmlPath = writeHtml(undefined, daybookDocument);

  assert.match(htmlPath, /build\/daybook-site\/index\.html$/);
  assert.match(readFileSync(htmlPath, "utf-8"), /Akari v1\.1 Situation Daybook/);
});

test("renderer exposes settings and daybook documents", async () => {
  const renderer = await import("./render.mjs");
  assert.deepEqual(
    renderer.parseRenderArgs(["--document", "daybook", "--previews", "--pdf"]),
    { documentName: "daybook", commands: ["previews", "pdf"] },
  );
  assert.deepEqual(
    renderer.previewFilenames(daybookDocument),
    pages.map((page) => `${String(page.page).padStart(2, "0")}-${page.id}.png`),
  );
});

test("renderer CLI rejects unknown documents", async () => {
  const { parseRenderArgs } = await import("./render.mjs");

  assert.throws(
    () => parseRenderArgs(["--document", "bogus", "--pdf"]),
    /Unknown document: bogus/,
  );
});

test("daybook images render inside visual slots", async (t) => {
  const { chromium } = await import("playwright");
  const { pathToFileURL } = await import("node:url");
  const { writeHtml } = await import("./render-html.mjs");
  const { theme } = await import("./theme.mjs");
  const target = writeHtml(undefined, daybookDocument);
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  t.after(async () => {
    await browser.close();
  });
  const page = await browser.newPage({
    viewport: { width: theme.preview.width, height: theme.preview.height },
  });
  await page.goto(pathToFileURL(target).href, { waitUntil: "domcontentloaded" });
  await page.evaluate(async () => {
    await Promise.all(
      [...document.images].map((image) => {
        if (image.complete && image.naturalWidth > 0) {
          return undefined;
        }
        return new Promise((resolve, reject) => {
          image.addEventListener("load", resolve, { once: true });
          image.addEventListener(
            "error",
            () => reject(new Error(`failed to load ${image.src}`)),
            { once: true },
          );
        });
      }),
    );
  });
  const issues = await page.evaluate(() => {
    return [
      ...document.querySelectorAll(
        ".layout-daybook-cover .visual-slot, .layout-daybook-scene .visual-slot",
      ),
    ]
      .map((slot) => {
        const image = slot.querySelector("img");
        return getComputedStyle(image).objectFit === "contain" ? undefined : slot.dataset.source;
      })
      .filter(Boolean);
  });
  assert.deepEqual(issues, []);

  const columnCounts = await page.evaluate(() => {
    return [
      ...document.querySelectorAll(
        ".layout-daybook-cover .page-body, .layout-daybook-scene .page-body",
      ),
    ].map((body) => getComputedStyle(body).gridTemplateColumns.split(" ").length);
  });
  assert.deepEqual([...new Set(columnCounts)], [2]);

  const misplacedNotes = await page.evaluate(() => {
    const tolerance = 2;
    return [
      ...document.querySelectorAll(".layout-daybook-cover, .layout-daybook-scene"),
    ].flatMap((sheet) => {
      const imageBlock = sheet.querySelector(".block-image");
      const noteBlocks = [...sheet.querySelectorAll(".block-note-list")];
      const imageRect = imageBlock.getBoundingClientRect();
      return noteBlocks
        .map((noteBlock) => {
          const noteRect = noteBlock.getBoundingClientRect();
          if (noteRect.left >= imageRect.right - tolerance) {
            return undefined;
          }
          return {
            page: sheet.id,
            title: noteBlock.querySelector("h2")?.textContent,
            imageRight: Math.round(imageRect.right),
            noteLeft: Math.round(noteRect.left),
          };
        })
        .filter(Boolean);
    });
  });
  assert.deepEqual(misplacedNotes, []);

  const unspacedGenerationNotes = await page.evaluate(() => {
    return [
      ...document.querySelectorAll(
        ".layout-daybook-cover .note-list-cards, .layout-daybook-scene .note-list-cards",
      ),
    ]
      .map((noteBlock) => {
        const marginTop = Number.parseFloat(getComputedStyle(noteBlock).marginTop);
        if (marginTop > 0) {
          return undefined;
        }
        return {
          page: noteBlock.closest(".sheet")?.id,
          marginTop,
        };
      })
      .filter(Boolean);
  });
  assert.deepEqual(unspacedGenerationNotes, []);

  await page.emulateMedia({ media: "print" });
  await page.evaluate(async () => {
    await new Promise((resolve) => requestAnimationFrame(() => resolve()));
  });

  const printLayoutIssues = await page.evaluate(() => {
    const tolerance = 2;
    return [
      ...document.querySelectorAll(".layout-daybook-cover, .layout-daybook-scene"),
    ].flatMap((sheet) => {
      const imageBlock = sheet.querySelector(".block-image");
      const visualSlot = sheet.querySelector(".visual-slot");
      const noteBlocks = [...sheet.querySelectorAll(".block-note-list")];
      const image = visualSlot.querySelector("img");
      const imageRect = imageBlock.getBoundingClientRect();
      const slotRect = visualSlot.getBoundingClientRect();
      const noteRects = noteBlocks.map((noteBlock) => ({
        title: noteBlock.querySelector("h2")?.textContent,
        rect: noteBlock.getBoundingClientRect(),
      }));
      const noteLeft = Math.min(...noteRects.map(({ rect }) => rect.left));
      const issues = [];

      if (getComputedStyle(image).objectFit !== "contain") {
        issues.push({
          page: sheet.id,
          issue: "object-fit",
          value: getComputedStyle(image).objectFit,
        });
      }
      if (slotRect.right > imageRect.right + tolerance || slotRect.right > noteLeft - tolerance) {
        issues.push({
          page: sheet.id,
          issue: "visual-slot-overlap",
          imageRight: Math.round(imageRect.right),
          noteLeft: Math.round(noteLeft),
          slotRight: Math.round(slotRect.right),
        });
      }
      for (const { title, rect } of noteRects) {
        if (rect.left < imageRect.right - tolerance) {
          issues.push({
            page: sheet.id,
            issue: "note-column",
            title,
            imageRight: Math.round(imageRect.right),
            noteLeft: Math.round(rect.left),
          });
        }
      }

      return issues;
    });
  });
  assert.deepEqual(printLayoutIssues, []);
});
