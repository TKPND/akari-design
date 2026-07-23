import { mkdirSync, readdirSync, rmSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright";
import { pages as settingsPages } from "./document.mjs";
import { settingsDocument, writeHtml } from "./render-html.mjs";
import { theme } from "./theme.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const settingsRenderDocument = { ...settingsDocument, pages: settingsPages };
const documentLoaders = {
  settings: async () => settingsRenderDocument,
  daybook: async () => {
    const { daybookDocument } = await import("./daybook-document.mjs");
    return daybookDocument;
  },
  "tonari-no-akari": async () => {
    const { tonariNoAkariDocument } = await import("./tonari-no-akari-document.mjs");
    return tonariNoAkariDocument;
  },
  "natural-form": async () => {
    const { naturalFormDocument } = await import("./natural-form-document.mjs");
    return naturalFormDocument;
  },
  "ame-no-sei-ni-shite": async () => {
    const { ameNoSeiNiShiteDocument } = await import(
      "./ame-no-sei-ni-shite-document.mjs"
    );
    return ameNoSeiNiShiteDocument;
  },
};
const usage =
  "Usage: node tools/pdf/render.mjs [--document settings|daybook|tonari-no-akari|natural-form|ame-no-sei-ni-shite] [--previews] [--pdf]";

export function parseRenderArgs(args) {
  const selected = new Set();
  let documentName = "settings";
  let hasDocumentOption = false;

  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === "--document") {
      if (hasDocumentOption) {
        throw new Error(`Duplicate document option\n${usage}`);
      }
      hasDocumentOption = true;

      const value = args[index + 1];
      if (!value || value.startsWith("--")) {
        throw new Error(`Missing document name\n${usage}`);
      }
      if (!Object.hasOwn(documentLoaders, value)) {
        throw new Error(`Unknown document: ${value}\n${usage}`);
      }
      documentName = value;
      index += 1;
      continue;
    }

    if (arg === "--previews" || arg === "--pdf") {
      selected.add(arg);
      continue;
    }

    throw new Error(`Unknown option: ${arg}\n${usage}`);
  }

  if (selected.size === 0) {
    throw new Error(usage);
  }

  const commands = [];
  if (selected.has("--previews")) {
    commands.push("previews");
  }
  if (selected.has("--pdf")) {
    commands.push("pdf");
  }
  return { documentName, commands };
}

export async function resolveDocument(documentName) {
  const loadDocument = documentLoaders[documentName];
  if (!loadDocument) {
    throw new Error(`Unknown document: ${documentName}\n${usage}`);
  }
  return loadDocument();
}

export function previewFilenames(document = settingsRenderDocument) {
  return document.pages.map((entry) => `${String(entry.page).padStart(2, "0")}-${entry.id}.png`);
}

function viewportFor(document) {
  return {
    width: document.pageSize?.previewWidth ?? theme.preview.width,
    height: document.pageSize?.previewHeight ?? theme.preview.height,
  };
}

function pdfSizeFor(document) {
  return {
    widthIn: document.pageSize?.widthIn ?? theme.page.widthIn,
    heightIn: document.pageSize?.heightIn ?? theme.page.heightIn,
  };
}

function isMainModule(metaUrl) {
  if (!process.argv[1]) {
    return false;
  }
  return resolve(process.argv[1]) === resolve(fileURLToPath(metaUrl));
}

async function waitForDocumentAssets(page) {
  await page.evaluate(async () => {
    await Promise.all(
      [...document.images].map((image) => {
        if (image.complete && image.naturalWidth > 0) {
          return undefined;
        }

        if (image.complete && image.naturalWidth === 0) {
          throw new Error(`failed to load ${image.currentSrc || image.src}`);
        }

        return new Promise((resolve, reject) => {
          image.addEventListener("load", resolve, { once: true });
          image.addEventListener(
            "error",
            () => reject(new Error(`failed to load ${image.currentSrc || image.src}`)),
            { once: true },
          );
        });
      }),
    );

    if (document.fonts) {
      await document.fonts.ready;
    }
  });
}

async function openDocument(document) {
  const htmlPath = writeHtml(resolve(root, document.siteHtml), document);
  const browser = await chromium.launch({
    channel: "chrome",
    headless: true,
  });

  try {
    const page = await browser.newPage({
      viewport: viewportFor(document),
      deviceScaleFactor: 1,
    });

    await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "load" });
    await page.emulateMedia({ media: "screen" });
    await waitForDocumentAssets(page);

    return { browser, page };
  } catch (error) {
    await browser.close();
    throw error;
  }
}

function removePreviewPngs(targetDir) {
  mkdirSync(targetDir, { recursive: true });
  for (const entry of readdirSync(targetDir, { withFileTypes: true })) {
    if (entry.isFile() && entry.name.endsWith(".png")) {
      rmSync(resolve(targetDir, entry.name));
    }
  }
}

function validatePreviewFiles(targetDir, document) {
  const expected = previewFilenames(document).toSorted();
  const actual = readdirSync(targetDir, { withFileTypes: true })
    .filter((entry) => entry.isFile() && entry.name.endsWith(".png"))
    .map((entry) => entry.name)
    .toSorted();

  if (
    actual.length !== expected.length ||
    actual.some((filename, index) => filename !== expected[index])
  ) {
    throw new Error(
      [
        "Preview output mismatch.",
        `Expected: ${expected.join(", ")}`,
        `Actual: ${actual.join(", ")}`,
      ].join("\n"),
    );
  }
}

export async function renderPreviews(document = settingsRenderDocument) {
  const targetDir = resolve(root, document.previewDir);
  removePreviewPngs(targetDir);

  const { browser, page } = await openDocument(document);
  try {
    for (const entry of document.pages) {
      const locator = page.locator(`.sheet[data-page="${entry.page}"]`);
      await locator.screenshot({
        path: resolve(targetDir, `${String(entry.page).padStart(2, "0")}-${entry.id}.png`),
      });
    }
    validatePreviewFiles(targetDir, document);
  } finally {
    await browser.close();
  }
}

export async function exportPdf(document = settingsRenderDocument) {
  const pdfPath = resolve(root, document.outputPdf);
  mkdirSync(dirname(pdfPath), { recursive: true });

  const { browser, page } = await openDocument(document);
  try {
    const pdfSize = pdfSizeFor(document);
    await page.emulateMedia({ media: "print" });
    await waitForDocumentAssets(page);
    await page.pdf({
      path: pdfPath,
      width: `${pdfSize.widthIn}in`,
      height: `${pdfSize.heightIn}in`,
      printBackground: true,
      preferCSSPageSize: true,
      margin: { top: "0", right: "0", bottom: "0", left: "0" },
    });
  } finally {
    await browser.close();
  }
}

export async function runCli(args = process.argv.slice(2)) {
  const { documentName, commands } = parseRenderArgs(args);
  const document = await resolveDocument(documentName);
  for (const command of commands) {
    if (command === "previews") {
      await renderPreviews(document);
      console.log(`${documentName} page previews rendered`);
    }

    if (command === "pdf") {
      await exportPdf(document);
      console.log(`${documentName} pdf exported`);
    }
  }
}

if (isMainModule(import.meta.url)) {
  try {
    await runCli();
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
