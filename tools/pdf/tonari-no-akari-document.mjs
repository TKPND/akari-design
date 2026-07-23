import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const documentId = "akari-v1.1-tonari-no-akari";
const documentTitle = "となりのあかり";
const pageCount = 24;
const manifest = JSON.parse(
  readFileSync(resolve(root, "source/manifests/tonari-no-akari/page-manifest.json"), "utf-8"),
);

function validateManifest(sourceManifest) {
  if (sourceManifest.document_id !== documentId) {
    throw new Error(`Unexpected tonari document id "${sourceManifest.document_id}"`);
  }
  if (sourceManifest.title !== documentTitle) {
    throw new Error(`Unexpected tonari document title "${sourceManifest.title}"`);
  }
  if (sourceManifest.page_count !== pageCount) {
    throw new Error(`Unexpected tonari page count "${sourceManifest.page_count}"`);
  }
  if (!Array.isArray(sourceManifest.pages) || sourceManifest.pages.length !== pageCount) {
    throw new Error("Tonari page count must match manifest pages");
  }

  for (const entry of sourceManifest.pages) {
    if (entry.role !== "artwork") {
      throw new Error(`Tonari page "${entry.id}" must use artwork role`);
    }
    if (entry.layout !== "tonari-portrait") {
      throw new Error(`Tonari page "${entry.id}" must use tonari-portrait layout`);
    }
    if (!Array.isArray(entry.source_inputs) || entry.source_inputs.length !== 1) {
      throw new Error(`Tonari page "${entry.id}" must include exactly one source input`);
    }
    if (!entry.display_line) {
      throw new Error(`Tonari page "${entry.id}" must include a display line`);
    }
    if (
      !Array.isArray(entry.blocks) ||
      entry.blocks.length !== 1 ||
      entry.blocks[0]?.type !== "portrait-plate"
    ) {
      throw new Error(`Tonari page "${entry.id}" must include exactly one portrait-plate block`);
    }
  }
}

validateManifest(manifest);

export const pages = manifest.pages.map((entry) => {
  const [source] = entry.source_inputs;

  return {
    page: entry.page,
    id: entry.id,
    title: entry.title,
    displayLine: entry.display_line,
    internalRange: entry.internal_range,
    eyebrow: "となりのあかり",
    layout: entry.layout,
    sourceInputs: entry.source_inputs,
    blocks: [
      {
        type: "portrait-plate",
        source,
        line: entry.display_line,
      },
    ],
  };
});

export const tonariNoAkariDocument = {
  id: documentId,
  title: documentTitle,
  pages,
  sourceManifestPath: "source/manifests/tonari-no-akari/source-assets.json",
  assetManifestPath: "source/manifests/tonari-no-akari/asset-manifest.json",
  outputPdf: "dist/akari-v1.1-tonari-no-akari.pdf",
  previewDir: "build/tonari-no-akari-page-previews",
  siteHtml: "build/tonari-no-akari-site/index.html",
  pageSize: {
    widthIn: 8.27,
    heightIn: 11.69,
    previewWidth: 2480,
    previewHeight: 3508,
  },
};
