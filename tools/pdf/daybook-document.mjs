import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const documentId = "akari-v1.1-situation-daybook";
const documentTitle = "Akari v1.1 Situation Daybook";
const pageCount = 10;
const manifest = JSON.parse(
  readFileSync(resolve(root, "source/manifests/daybook/page-manifest.json"), "utf-8"),
);

function validateManifest(sourceManifest) {
  if (sourceManifest.document_id !== documentId) {
    throw new Error(`Unexpected daybook document id "${sourceManifest.document_id}"`);
  }
  if (sourceManifest.page_count !== pageCount) {
    throw new Error(`Unexpected daybook page count "${sourceManifest.page_count}"`);
  }
  if (!Array.isArray(sourceManifest.pages) || sourceManifest.pages.length !== pageCount) {
    throw new Error("Daybook page count must match manifest pages");
  }

  for (const entry of sourceManifest.pages) {
    if (!Array.isArray(entry.source_inputs) || entry.source_inputs.length !== 1) {
      throw new Error(`Daybook page "${entry.id}" must include exactly one source input`);
    }
    if (!Array.isArray(entry.atmosphere_notes) || !Array.isArray(entry.generation_notes)) {
      throw new Error(`Daybook page "${entry.id}" must include atmosphere and generation notes`);
    }
  }
}

function imageBlock(source, label) {
  return {
    type: "image",
    images: [{ source, label }],
  };
}

function notes(title, items, variant) {
  return {
    type: "note-list",
    title,
    variant,
    items,
  };
}

validateManifest(manifest);

export const pages = manifest.pages.map((entry) => {
  const [source] = entry.source_inputs;
  const eyebrow = entry.role === "cover"
    ? `${documentTitle} / Mood Standard`
    : `${documentTitle} / Light Notes`;

  return {
    page: entry.page,
    id: entry.id,
    title: entry.title,
    eyebrow,
    layout: entry.layout,
    sourceInputs: entry.source_inputs,
    blocks: [
      imageBlock(source, entry.title),
      notes("Atmosphere", entry.atmosphere_notes, "plain"),
      notes("Generation Notes", entry.generation_notes, "cards"),
    ],
  };
});

export const daybookDocument = {
  id: documentId,
  title: documentTitle,
  pages,
  sourceManifestPath: "source/manifests/daybook/source-assets.json",
  assetManifestPath: "source/manifests/daybook/asset-manifest.json",
  outputPdf: "dist/akari-v1.1-situation-daybook.pdf",
  previewDir: "build/daybook-page-previews",
  siteHtml: "build/daybook-site/index.html",
};
