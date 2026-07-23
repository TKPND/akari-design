import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync, readFileSync, statSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import test from "node:test";
import { chromium } from "playwright";
import { pages } from "./document.mjs";
import { renderHtml, writeHtml } from "./render-html.mjs";
import { theme } from "./theme.mjs";

const expectedLayouts = [
  [1, "cover-key-visual", "cover"],
  [2, "d65-color-palette", "palette"],
  [3, "character-summary-proportion", "proportion"],
  [4, "front-back", "front-back"],
  [5, "angle-turnaround", "turnaround"],
  [6, "expressions", "expression-grid"],
  [7, "hair-face-details", "detail-board"],
  [8, "outfit-rules", "outfit-rules"],
  [9, "footwear-sock-board", "detail-board-large"],
  [10, "sneaker-construction", "detail-board-large"],
  [11, "bag-detail-board", "detail-board-large"],
  [12, "bag-on-body-scale", "detail-board-large"],
  [13, "do-dont", "do-dont"],
  [14, "production-notes-source-manifest", "manifest"],
];

const supportedBlockTypes = new Set([
  "image",
  "palette-grid",
  "guide-lines",
  "expression-labels",
  "note-list",
  "manifest-summary",
]);

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function cssVariable(css, name) {
  const match = new RegExp(`--${name}:\\s*([^;]+);`).exec(css);
  assert.ok(match, `missing CSS variable --${name}`);
  return match[1].trim();
}

function printRootBlock(css) {
  const match = /@media print\s*\{\s*:root\s*\{([\s\S]*?)\n\s*\}\s*\n\}/.exec(css);
  assert.ok(match, "missing @media print :root block");
  return match[1];
}

function cssVariableInBlock(block, name) {
  const match = new RegExp(`--${name}:\\s*([^;]+);`).exec(block);
  assert.ok(match, `missing CSS variable --${name}`);
  return match[1].trim();
}

function lengthInInches(value) {
  const match = /^([0-9]+(?:\.[0-9]+)?)(in|px)$/.exec(value);
  assert.ok(match, `unsupported CSS length: ${value}`);
  const amount = Number.parseFloat(match[1]);
  return match[2] === "in" ? amount : amount / 288;
}

async function waitForImages(page) {
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
            () => reject(new Error(`failed to load ${image.currentSrc}`)),
            { once: true },
          );
        });
      }),
    );
  });
}

async function imageFitIssues(page) {
  return page.evaluate(() => {
    const tolerance = 0.5;
    return [...document.querySelectorAll(".visual-slot")]
      .map((slot) => {
        const image = slot.querySelector("img");
        const slotBox = slot.getBoundingClientRect();
        const imageBox = image.getBoundingClientRect();
        const overflows =
          imageBox.left < slotBox.left - tolerance ||
          imageBox.top < slotBox.top - tolerance ||
          imageBox.right > slotBox.right + tolerance ||
          imageBox.bottom > slotBox.bottom + tolerance;

        if (!overflows) {
          return undefined;
        }

        return {
          page: slot.closest(".sheet")?.dataset.page,
          source: slot.dataset.source,
          slot: {
            width: Math.round(slotBox.width),
            height: Math.round(slotBox.height),
          },
          image: {
            width: Math.round(imageBox.width),
            height: Math.round(imageBox.height),
          },
        };
      })
      .filter(Boolean);
  });
}

async function objectFitIssues(page) {
  return page.evaluate(() =>
    [...document.querySelectorAll(".visual-slot img")]
      .map((image) => getComputedStyle(image).objectFit)
      .filter((objectFit) => objectFit !== "contain"),
  );
}

async function containedImageMetrics(page, selector) {
  return page.evaluate((slotSelector) => {
    return [...document.querySelectorAll(slotSelector)].map((slot) => {
      const image = slot.querySelector("img");
      const box = slot.getBoundingClientRect();
      const slotRatio = box.width / box.height;
      const naturalRatio = image.naturalWidth / image.naturalHeight;
      let drawnWidth = box.width;
      let drawnHeight = box.height;

      if (naturalRatio > slotRatio) {
        drawnHeight = box.width / naturalRatio;
      } else {
        drawnWidth = box.height * naturalRatio;
      }

      return {
        page: slot.closest(".sheet")?.dataset.page,
        source: slot.dataset.source,
        fillHeightRatio: drawnHeight / box.height,
        fillAreaRatio: (drawnWidth * drawnHeight) / (box.width * box.height),
      };
    });
  }, selector);
}

test("document has exactly 14 numbered pages", () => {
  assert.equal(pages.length, 14);
  assert.deepEqual(
    pages.map((page) => page.page),
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
  );
});

test("all pages have source inputs and English titles", () => {
  for (const page of pages) {
    assert.ok(page.id);
    assert.ok(page.title);
    assert.ok(page.sourceInputs.length > 0);
    assert.equal(/[ぁ-んァ-ン一-龯]/.test(page.title), false);
  }
});

test("pages use structured layouts and supported blocks instead of sections", () => {
  for (const page of pages) {
    assert.equal(Object.hasOwn(page, "sections"), false, `${page.id} still has sections`);
    assert.ok(page.layout, `${page.id} is missing a layout`);
    assert.ok(Array.isArray(page.blocks), `${page.id} blocks must be an array`);
    assert.ok(page.blocks.length > 0, `${page.id} must have at least one block`);
    for (const block of page.blocks) {
      assert.ok(
        supportedBlockTypes.has(block.type),
        `${page.id} has unsupported block type ${block.type}`,
      );
    }
  }
});

test("pages have the required layout sequence by number and id", () => {
  assert.deepEqual(
    pages.map(({ page, id, layout }) => [page, id, layout]),
    expectedLayouts,
  );
});

test("theme matches 16:9 preview contract", () => {
  assert.equal(theme.preview.width, 3840);
  assert.equal(theme.preview.height, 2160);
  assert.equal(theme.page.aspect, "16:9");
});

test("CSS page and preview constants match theme", () => {
  const css = readFileSync(resolve("tools/pdf/styles.css"), "utf-8");

  assert.match(
    css,
    new RegExp(`size:\\s*${theme.page.widthIn}in\\s+${theme.page.heightIn}in;`),
  );
  assert.equal(cssVariable(css, "page-width"), `${theme.preview.width}px`);
  assert.equal(cssVariable(css, "page-height"), `${theme.preview.height}px`);
  assert.equal(cssVariable(css, "page-padding"), `${theme.preview.safeMargin}px`);
  assert.ok(parseFloat(cssVariable(css, "body-size")) >= theme.preview.minBodyPx);
  assert.ok(parseFloat(cssVariable(css, "caption-size")) >= theme.preview.minCaptionPx);
  assert.ok(parseFloat(cssVariable(css, "small-size")) >= theme.preview.minCaptionPx);
  assert.equal(cssVariable(css, "font-title"), theme.fonts.title);
  assert.equal(cssVariable(css, "font-body"), theme.fonts.body);
  for (const [name, value] of Object.entries(theme.colors)) {
    assert.equal(cssVariable(css, `color-${name}`), value);
  }
});

test("PDF CSS loads project-local Inter font assets", () => {
  const css = readFileSync(resolve("tools/pdf/styles.css"), "utf-8");
  const interFont = resolve("source/fonts/inter/Inter-Variable.ttf");
  const interLicense = resolve("source/fonts/inter/OFL.txt");

  assert.ok(existsSync(interFont), "missing vendored Inter variable font");
  assert.ok(statSync(interFont).size > 100_000, "Inter font file is unexpectedly small");
  assert.ok(existsSync(interLicense), "missing Inter OFL license");
  assert.match(css, /@font-face\s*\{[\s\S]*font-family:\s*"Inter";/);
  assert.match(css, /url\("\.\.\/\.\.\/source\/fonts\/inter\/Inter-Variable\.ttf"\)/);
  assert.match(css, /font-weight:\s*100 900;/);
});

test("print CSS keeps safe margins, readable text sizes, and non-negative tracking", () => {
  const css = readFileSync(resolve("tools/pdf/styles.css"), "utf-8");
  const printRoot = printRootBlock(css);

  assert.ok(lengthInInches(cssVariableInBlock(printRoot, "page-padding")) >= 0.5);
  assert.ok(lengthInInches(cssVariableInBlock(printRoot, "body-size")) >= 0.105);
  assert.ok(lengthInInches(cssVariableInBlock(printRoot, "caption-size")) >= 0.085);
  assert.ok(lengthInInches(cssVariableInBlock(printRoot, "small-size")) >= 0.085);
  assert.equal(/letter-spacing:\s*-/i.test(css), false);
});

test("document mirrors page manifest identifiers and source inputs", () => {
  const manifest = JSON.parse(
    readFileSync(resolve("source/manifests/page-manifest.json"), "utf-8"),
  );
  assert.deepEqual(
    pages.map(({ page, id, title, layout, blocks = [], sourceInputs }) => ({
      page,
      id,
      title,
      layout,
      blocks: blocks.map((block) => block.type),
      source_inputs: sourceInputs,
    })),
    manifest.pages.map(({ page, id, title, layout, blocks = [], source_inputs }) => ({
      page,
      id,
      title,
      layout,
      blocks: blocks.map((block) => block.type),
      source_inputs,
    })),
  );
});

test("source image path mapping covers every document source input", async () => {
  const { sourceImagePath } = await import("./render-html.mjs");
  const sourceManifest = JSON.parse(
    readFileSync(resolve("source/manifests/source-assets.json"), "utf-8"),
  );
  const assetManifest = JSON.parse(
    readFileSync(resolve("source/manifests/asset-manifest.json"), "utf-8"),
  );
  const pathsById = new Map(
    sourceManifest.assets.map((asset) => [asset.id, asset.source_path]),
  );
  for (const asset of assetManifest.assets) {
    if (asset.model_or_tool === "image_generation") {
      pathsById.set(asset.id, asset.candidate_path);
    }
  }
  const sourceInputs = [...new Set(pages.flatMap((page) => page.sourceInputs))];

  for (const sourceInput of sourceInputs) {
    assert.equal(sourceImagePath(sourceInput), pathsById.get(sourceInput));
  }
});

test("accepted generated assets are routed to their target PDF pages", () => {
  const pagesById = new Map(pages.map((page) => [page.id, page]));

  assert.deepEqual(pagesById.get("cover-key-visual").sourceInputs, [
    "cover-key-visual-16x9",
  ]);
  assert.deepEqual(pagesById.get("character-summary-proportion").sourceInputs, [
    "hoodie-front-proportion-corrected",
    "body-proportion-lock",
  ]);
  assert.deepEqual(pagesById.get("hair-face-details").sourceInputs, [
    "hair-face-detail-board",
  ]);
  assert.deepEqual(pagesById.get("bag-detail-board").sourceInputs, [
    "bag-board",
  ]);
  assert.deepEqual(pagesById.get("bag-on-body-scale").sourceInputs, [
    "bag-on-body-scale",
  ]);
});

test("image pages render every declared source input", () => {
  for (const page of pages) {
    const imageSources = page.blocks
      .filter((block) => block.type === "image")
      .flatMap((block) => block.images.map((image) => image.source));
    if (imageSources.length === 0) {
      continue;
    }

    assert.deepEqual(
      [...new Set(imageSources)].sort(),
      [...page.sourceInputs].sort(),
      `${page.id} image sources must match footer source chips`,
    );
  }
});

test("rendered HTML contains 14 sheets", () => {
  const html = renderHtml();
  const count = html.match(/class="sheet layout-/g)?.length ?? 0;
  assert.equal(count, 14);
  assert.match(html, /Akari v1\.1/);
  assert.match(html, /D65 Color Palette/);
});

test("rendered HTML uses dynamic total page count in headers", () => {
  const html = renderHtml();

  assert.match(html, /14 \/ 14/);
  assert.doesNotMatch(html, /\/ 12</);
});

test("renderer output contains layout classes and representative block content", () => {
  const html = renderHtml();

  assert.match(html, /class="sheet layout-cover"/);
  assert.match(html, /class="sheet layout-expression-grid"/);
  assert.match(html, /class="sheet layout-manifest"/);
  assert.match(html, /data-block-type="image"/);
  assert.match(html, /data-block-type="guide-lines"/);
  assert.match(html, /Head \/ torso \/ leg landmarks/);
  assert.match(html, /Neutral/);
  assert.match(html, /Soft Smile/);
  assert.match(html, /Avoid color drift/);
});

test("dense detail pages recreate source-board labels as PDF-native text", () => {
  const html = renderHtml();
  const requiredTerms = [
    "Footwear Sock Board",
    "Stable mid-calf height",
    "Sock Height Guide",
    "Stripe Placement",
    "Tongue Visibility",
    "Toe Shape",
    "Blue Gray Outsole",
    "Sneaker Construction",
    "Two thin pale blue stripes",
    "Tongue sits slightly above sock line",
    "Rounded toe",
    "Sculpted Sole",
    "White Laces",
    "Bag Detail Board",
    "Color & Material",
    "Can Fit",
    "W 16cm x H 20cm x D 5cm",
    "Smartphone / A6 notebook / earbuds",
    "Portable Battery",
    "Canvas-like ivory body",
    "Adjustable Strap",
    "Bag-on-body scale",
    "Compact against hoodie",
  ];

  for (const term of requiredTerms) {
    assert.ok(html.includes(escapeHtml(term)), `missing PDF-native detail term: ${term}`);
  }
});

test("palette grid renders roles from the D65 palette source", () => {
  const palette = JSON.parse(
    readFileSync(resolve("source/palette/akari-v1.1-palette.json"), "utf-8"),
  );
  const html = renderHtml();

  assert.match(html, /data-block-type="palette-grid"/);
  assert.match(html, new RegExp(escapeHtml(palette.palette_version)));
  for (const role of palette.roles) {
    assert.ok(html.includes(`data-palette-role="${escapeHtml(role.name)}"`));
    assert.ok(html.includes(escapeHtml(role.hex)));
    assert.ok(html.includes(escapeHtml(role.usage)));
  }
});

test("manifest summary reflects palette and accepted final PDF assets", () => {
  const sourceManifest = JSON.parse(
    readFileSync(resolve("source/manifests/source-assets.json"), "utf-8"),
  );
  const assetManifest = JSON.parse(
    readFileSync(resolve("source/manifests/asset-manifest.json"), "utf-8"),
  );
  const palette = JSON.parse(
    readFileSync(resolve("source/palette/akari-v1.1-palette.json"), "utf-8"),
  );
  const html = renderHtml();
  const sourceAssetsById = new Map(sourceManifest.assets.map((asset) => [asset.id, asset]));

  assert.match(html, /data-block-type="manifest-summary"/);
  assert.ok(html.includes(escapeHtml(palette.palette_version)));
  assert.ok(html.includes(escapeHtml(palette.white_point)));
  for (const asset of assetManifest.assets.filter(
    (asset) => asset.status === "accepted" && asset.used_in_final_pdf,
  )) {
    const filename = sourceAssetsById.get(asset.id)?.original_filename ?? asset.candidate_path;
    assert.ok(html.includes(`data-accepted-asset="${escapeHtml(asset.id)}"`));
    assert.ok(html.includes(escapeHtml(filename)));
  }
});

test("renderer exports preview and PDF commands", async () => {
  const renderer = await import("./render.mjs");

  assert.equal(typeof renderer.renderPreviews, "function");
  assert.equal(typeof renderer.exportPdf, "function");
});

test("renderer CLI rejects missing flags", async () => {
  const { parseRenderArgs } = await import("./render.mjs");

  assert.throws(() => parseRenderArgs([]), /Usage: node tools\/pdf\/render\.mjs/);
});

test("renderer CLI rejects unknown flags", async () => {
  const { parseRenderArgs } = await import("./render.mjs");

  assert.throws(
    () => parseRenderArgs(["--bogus"]),
    /Unknown option: --bogus/,
  );
});

test("renderer CLI accepts both flags in deterministic order", async () => {
  const { parseRenderArgs } = await import("./render.mjs");

  assert.deepEqual(parseRenderArgs(["--pdf", "--previews"]), {
    documentName: "settings",
    commands: ["previews", "pdf"],
  });
});

test("renderer CLI rejects duplicate document flags", async () => {
  const { parseRenderArgs } = await import("./render.mjs");

  assert.throws(
    () => parseRenderArgs(["--document", "settings", "--document", "daybook", "--pdf"]),
    /Duplicate document option/,
  );
});

test("renderer CLI fails fast for missing and unknown flags", () => {
  const renderScript = resolve("tools/pdf/render.mjs");
  const noFlags = spawnSync(process.execPath, [renderScript], {
    encoding: "utf-8",
  });
  const bogus = spawnSync(process.execPath, [renderScript, "--bogus"], {
    encoding: "utf-8",
  });

  assert.notEqual(noFlags.status, 0);
  assert.match(noFlags.stderr, /Usage: node tools\/pdf\/render\.mjs/);
  assert.notEqual(bogus.status, 0);
  assert.match(bogus.stderr, /Unknown option: --bogus/);
  assert.match(bogus.stderr, /Usage: node tools\/pdf\/render\.mjs/);
});

test("importing renderer ignores parent process CLI flags", () => {
  const renderUrl = pathToFileURL(resolve("tools/pdf/render.mjs")).href;
  const script = `
    process.argv.push("--pdf");
    const renderer = await import(${JSON.stringify(`${renderUrl}?import-side-effect`)});
    console.log(typeof renderer.exportPdf);
  `;
  const result = spawnSync(process.execPath, ["--input-type=module", "--eval", script], {
    encoding: "utf-8",
    timeout: 30_000,
  });

  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, "");
  assert.equal(result.stdout, "function\n");
});

test("settings renderer import does not load daybook document", () => {
  const renderUrl = pathToFileURL(resolve("tools/pdf/render.mjs")).href;
  const loaderSource = `
    export async function resolve(specifier, context, nextResolve) {
      if (specifier === "./daybook-document.mjs" || specifier.endsWith("/daybook-document.mjs")) {
        throw new Error("daybook document import blocked");
      }
      return nextResolve(specifier, context);
    }
  `;
  const loaderUrl = `data:text/javascript,${encodeURIComponent(loaderSource)}`;
  const script = `
    const renderer = await import(${JSON.stringify(renderUrl)});
    console.log(JSON.stringify(renderer.parseRenderArgs(["--pdf"])));
  `;
  const result = spawnSync(
    process.execPath,
    ["--experimental-loader", loaderUrl, "--input-type=module", "--eval", script],
    {
      encoding: "utf-8",
      timeout: 30_000,
    },
  );

  assert.equal(result.status, 0, result.stderr);
  assert.equal(
    result.stdout.trim(),
    JSON.stringify({ documentName: "settings", commands: ["pdf"] }),
  );
});

test("preview filenames match the expected page images", async () => {
  const { previewFilenames } = await import("./render.mjs");

  assert.deepEqual(
    previewFilenames(),
    pages.map((page) => `${String(page.page).padStart(2, "0")}-${page.id}.png`),
  );
});

test("renderHtml includes all sheets and escaped source chips", async () => {
  const html = renderHtml();

  assert.ok(html.startsWith("<!doctype html>"));
  assert.ok(html.includes("<style>"));
  for (const page of pages) {
    assert.ok(
      html.includes(
        `class="sheet layout-${escapeHtml(page.layout)}" data-page="${page.page}" id="${page.id}"`,
      ),
    );
    assert.ok(html.includes(`<h1>${escapeHtml(page.title)}</h1>`));
    for (const sourceInput of page.sourceInputs) {
      assert.ok(
        html.includes(`<span class="source-chip">${escapeHtml(sourceInput)}</span>`),
      );
    }
  }
});

test("rendered source images fit visual slots in screen and print media", async (t) => {
  const target = writeHtml();
  const browser = await chromium.launch({
    channel: "chrome",
    headless: true,
  });
  t.after(async () => {
    await browser.close();
  });

  const page = await browser.newPage({
    viewport: {
      width: theme.preview.width,
      height: theme.preview.height,
    },
  });
  await page.goto(pathToFileURL(target).href, { waitUntil: "domcontentloaded" });
  await waitForImages(page);
  assert.deepEqual(await objectFitIssues(page), []);
  assert.deepEqual(await imageFitIssues(page), []);

  await page.emulateMedia({ media: "print" });
  assert.deepEqual(await objectFitIssues(page), []);
  assert.deepEqual(await imageFitIssues(page), []);
});

test("dense source boards use readable slot proportions", async (t) => {
  const target = writeHtml();
  const browser = await chromium.launch({
    channel: "chrome",
    headless: true,
  });
  t.after(async () => {
    await browser.close();
  });

  const page = await browser.newPage({
    viewport: {
      width: theme.preview.width,
      height: theme.preview.height,
    },
  });
  await page.goto(pathToFileURL(target).href, { waitUntil: "domcontentloaded" });
  await waitForImages(page);

  const metrics = await containedImageMetrics(
    page,
    [
      '.sheet[data-page="9"] .visual-slot[data-source="footwear-board"]',
      '.sheet[data-page="10"] .visual-slot[data-source="shoe-board"]',
      '.sheet[data-page="11"] .visual-slot[data-source="bag-board"]',
    ].join(","),
  );

  assert.equal(metrics.length, 3);
  for (const metric of metrics) {
    assert.ok(
      metric.fillHeightRatio >= 0.85,
      `${metric.source} only fills ${Math.round(metric.fillHeightRatio * 100)}% of slot height`,
    );
    assert.ok(
      metric.fillAreaRatio >= 0.75,
      `${metric.source} only fills ${Math.round(metric.fillAreaRatio * 100)}% of slot area`,
    );
  }
});
