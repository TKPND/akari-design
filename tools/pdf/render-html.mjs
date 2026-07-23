import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { pages as settingsPages } from "./document.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");

export const settingsDocument = {
  id: "akari-v1.1-settings",
  title: "Akari v1.1 Settings",
  pages: settingsPages,
  sourceManifestPath: "source/manifests/source-assets.json",
  assetManifestPath: "source/manifests/asset-manifest.json",
  outputPdf: "dist/akari-v1.1-settings.pdf",
  previewDir: "build/page-previews",
  siteHtml: "build/site/index.html",
};

function loadJson(relativePath) {
  return JSON.parse(readFileSync(resolve(root, relativePath), "utf-8"));
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function blockClass(block) {
  return `block block-${escapeHtml(block.type)}`;
}

function safeHexColor(value) {
  return /^#[0-9a-fA-F]{6}$/.test(value) ? value : "#000000";
}

function renderSourceChips(page) {
  return page.sourceInputs
    .map((input) => `<span class="source-chip">${escapeHtml(input)}</span>`)
    .join("");
}

function renderImageBlock(block, document) {
  const images = block.images ?? [];
  if (!Array.isArray(images) || images.length === 0) {
    throw new Error("image block must include at least one image");
  }

  const imageItems = images
    .map((image) => {
      const source = image.source;
      const label = image.label ?? source;
      return `
        <figure class="image-card">
          <div class="visual-slot" data-source="${escapeHtml(source)}">
            <img src="../../${escapeHtml(sourceImagePath(source, document))}" alt="${escapeHtml(label)}">
          </div>
          <figcaption>${escapeHtml(label)}</figcaption>
        </figure>`;
    })
    .join("");

  return `<section class="${blockClass(block)}" data-block-type="image">${imageItems}</section>`;
}

function renderPortraitPlate(block, page, document) {
  const source = block.source ?? page.sourceInputs?.[0];
  const line = block.line ?? page.displayLine;

  if (!source) {
    throw new Error(`portrait-plate block on page "${page.id}" must include a source`);
  }
  if (!line) {
    throw new Error(`portrait-plate block on page "${page.id}" must include a display line`);
  }

  return `
    <section class="${blockClass(block)}" data-block-type="portrait-plate">
      <figure class="portrait-plate">
        <div class="portrait-frame visual-slot" data-source="${escapeHtml(source)}">
          <img src="../../${escapeHtml(sourceImagePath(source, document))}" alt="${escapeHtml(page.title)}">
        </div>
        <figcaption class="portrait-caption">
          <strong>${escapeHtml(page.title)}</strong>
          <span>${escapeHtml(line)}</span>
        </figcaption>
      </figure>
    </section>`;
}

function renderArtbookPlate(block, page, document) {
  const source = block.source ?? page.sourceInputs?.[0];
  if (!source) {
    throw new Error(`artbook-plate block on page "${page.id}" must include a source`);
  }
  const dialogue = block.dialogue
    ? `<p class="artbook-dialogue">${escapeHtml(block.dialogue)}</p>`
    : "";
  const time = block.time
    ? `<time class="artbook-time">${escapeHtml(block.time)}</time>`
    : "";
  const crop = block.crop ?? "full";
  return `
    <section class="${blockClass(block)} crop-${escapeHtml(crop)}" data-block-type="artbook-plate">
      <figure class="artbook-frame visual-slot" data-source="${escapeHtml(source)}">
        <img src="../../${escapeHtml(sourceImagePath(source, document))}" alt="${escapeHtml(page.title)}">
      </figure>
      ${time}${dialogue}
    </section>`;
}

function renderArtbookCopy(block) {
  const lines = block.lines ?? [];
  if (!Array.isArray(lines)) {
    throw new Error("artbook-copy block lines must be an array");
  }
  const lineMarkup = lines.map((line) => `<p>${escapeHtml(line)}</p>`).join("");
  return `
    <section class="${blockClass(block)}" data-block-type="artbook-copy">
      <h1>${escapeHtml(block.title)}</h1>
      <div>${lineMarkup}</div>
    </section>`;
}

function renderPaletteGrid(block) {
  const palette = loadJson("source/palette/akari-v1.1-palette.json");
  const swatches = palette.roles
    .map(
      (role) => `
        <article class="palette-card" data-palette-role="${escapeHtml(role.name)}">
          <span class="swatch" style="--swatch-color: ${safeHexColor(role.hex)}"></span>
          <div>
            <h2>${escapeHtml(role.name)}</h2>
            <p class="hex">${escapeHtml(role.hex)}</p>
            <p>${escapeHtml(role.usage)}</p>
          </div>
        </article>`,
    )
    .join("");

  return `
    <section class="${blockClass(block)}" data-block-type="palette-grid">
      <div class="palette-meta">
        <strong>${escapeHtml(palette.palette_version)}</strong>
        <span>${escapeHtml(palette.white_point)} / ${escapeHtml(palette.color_space)}</span>
      </div>
      <div class="palette-cards">${swatches}</div>
    </section>`;
}

function renderGuideLines(block) {
  const rows = block.rows ?? [];
  if (!Array.isArray(rows) || rows.length === 0) {
    throw new Error("guide-lines block must include rows");
  }

  const rowItems = rows
    .map(
      (row) => `
        <li>
          <strong>${escapeHtml(row.name)}</strong>
          <span>${escapeHtml(row.note)}</span>
        </li>`,
    )
    .join("");

  return `
    <section class="${blockClass(block)}" data-block-type="guide-lines">
      <h2>${escapeHtml(block.title)}</h2>
      <ol>${rowItems}</ol>
    </section>`;
}

function renderExpressionLabels(block) {
  const labels = block.labels ?? [];
  if (!Array.isArray(labels) || labels.length !== 9) {
    throw new Error("expression-labels block must include nine labels");
  }

  const labelItems = labels
    .map((label, index) => `<li><span>${index + 1}</span>${escapeHtml(label)}</li>`)
    .join("");

  return `
    <section class="${blockClass(block)}" data-block-type="expression-labels">
      <ol>${labelItems}</ol>
    </section>`;
}

function renderNoteList(block) {
  const items = block.items ?? [];
  if (!Array.isArray(items) || items.length === 0) {
    throw new Error("note-list block must include notes");
  }

  const itemMarkup = items.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
  return `
    <section class="${blockClass(block)} note-list-${escapeHtml(block.variant ?? "plain")}" data-block-type="note-list">
      <h2>${escapeHtml(block.title)}</h2>
      <ul>${itemMarkup}</ul>
    </section>`;
}

function renderManifestSummary(block) {
  const pageManifest = loadJson("source/manifests/page-manifest.json");
  const sourceManifest = loadJson("source/manifests/source-assets.json");
  const assetManifest = loadJson("source/manifests/asset-manifest.json");
  const palette = loadJson("source/palette/akari-v1.1-palette.json");
  const sourceAssetsById = new Map(sourceManifest.assets.map((asset) => [asset.id, asset]));
  const acceptedIds = new Set(
    assetManifest.assets
      .filter((asset) => asset.status === "accepted" && asset.used_in_final_pdf)
      .map((asset) => asset.id),
  );
  const acceptedRows = assetManifest.assets
    .filter((asset) => acceptedIds.has(asset.id))
    .map(
      (asset) => {
        const sourceAsset = sourceAssetsById.get(asset.id);
        const filename = sourceAsset?.original_filename ?? asset.candidate_path;
        const role = sourceAsset?.role ?? "generated_accepted_asset";
        return `
        <tr data-accepted-asset="${escapeHtml(asset.id)}">
          <th>${escapeHtml(asset.id)}</th>
          <td>${escapeHtml(filename)}</td>
          <td>${escapeHtml(role)}</td>
        </tr>`;
      },
    )
    .join("");

  return `
    <section class="${blockClass(block)}" data-block-type="manifest-summary">
      <div class="manifest-kpis">
        <p><strong>Document</strong><span>${escapeHtml(pageManifest.document_id)}</span></p>
        <p><strong>Schema Version</strong><span>${escapeHtml(pageManifest.schema_version)}</span></p>
        <p><strong>Palette</strong><span>${escapeHtml(palette.palette_version)}</span></p>
        <p><strong>White Point</strong><span>${escapeHtml(palette.white_point)}</span></p>
        <p><strong>Accepted Assets</strong><span>${acceptedIds.size}</span></p>
      </div>
      <table class="manifest-table">
        <thead>
          <tr><th>Asset ID</th><th>Filename</th><th>Role</th></tr>
        </thead>
        <tbody>${acceptedRows}</tbody>
      </table>
    </section>`;
}

export function renderBlock(block, page, document = settingsDocument) {
  switch (block.type) {
    case "image":
      return renderImageBlock(block, document);
    case "portrait-plate":
      return renderPortraitPlate(block, page, document);
    case "artbook-plate":
      return renderArtbookPlate(block, page, document);
    case "artbook-copy":
      return renderArtbookCopy(block);
    case "palette-grid":
      return renderPaletteGrid(block);
    case "guide-lines":
      return renderGuideLines(block);
    case "expression-labels":
      return renderExpressionLabels(block);
    case "note-list":
      return renderNoteList(block);
    case "manifest-summary":
      return renderManifestSummary(block);
    default:
      throw new Error(`Unsupported block type "${block.type}" on page "${page.id}"`);
  }
}

function renderPage(page, totalPages, document) {
  const blockItems = page.blocks.map((block) => renderBlock(block, page, document)).join("");

  return `
    <section class="sheet layout-${escapeHtml(page.layout)}" data-page="${page.page}" id="${escapeHtml(page.id)}">
      <header class="page-header">
        <p>${escapeHtml(page.eyebrow)}</p>
        <h1>${escapeHtml(page.title)}</h1>
        <span>${String(page.page).padStart(2, "0")} / ${totalPages}</span>
      </header>
      <main class="page-body">${blockItems}</main>
      <footer class="source-list">${renderSourceChips(page)}</footer>
    </section>`;
}

export function sourceImagePath(assetId, document = settingsDocument) {
  if (document.assetPaths) {
    if (!Object.hasOwn(document.assetPaths, assetId)) {
      throw new Error(`Unknown source asset id: ${assetId}`);
    }
    return document.assetPaths[assetId];
  }

  const sourceManifest = loadJson(document.sourceManifestPath);
  const assetManifest = loadJson(document.assetManifestPath);
  const paths = Object.fromEntries(
    sourceManifest.assets.map((asset) => [asset.id, asset.source_path]),
  );

  for (const asset of assetManifest.assets) {
    if (asset.model_or_tool === "image_generation" && asset.candidate_path) {
      const finishPassStatus = asset.finish_pass?.status;
      const acceptedFinishPath =
        finishPassStatus === "accepted" || finishPassStatus === "accepted_correction_only"
          ? asset.finish_pass?.output
          : undefined;
      paths[asset.id] = acceptedFinishPath ?? asset.candidate_path;
    }
  }

  if (!Object.hasOwn(paths, assetId)) {
    throw new Error(`Unknown source asset id: ${assetId}`);
  }
  return paths[assetId];
}

export function sourceFilename(assetId, document = settingsDocument) {
  return sourceImagePath(assetId, document).split("/").at(-1);
}

function renderDocumentCss(document) {
  if (!document.pageSize) {
    return "";
  }

  const { widthIn, heightIn, previewWidth, previewHeight } = document.pageSize;
  return `
@page {
  size: ${widthIn}in ${heightIn}in;
}

:root {
  --page-width: ${previewWidth}px;
  --page-height: ${previewHeight}px;
}

@media print {
  :root {
    --page-width: ${widthIn}in;
    --page-height: ${heightIn}in;
  }
}`;
}

export function renderHtml(document = settingsDocument) {
  const css = readFileSync(resolve(root, "tools/pdf/styles.css"), "utf-8");
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escapeHtml(document.title)}</title>
  <style>${css}${renderDocumentCss(document)}</style>
</head>
<body>
${document.pages.map((page) => renderPage(page, document.pages.length, document)).join("\n")}
</body>
</html>`;
}

export function writeHtml(target, document = settingsDocument) {
  const htmlTarget = target ?? resolve(root, document.siteHtml);
  mkdirSync(dirname(htmlTarget), { recursive: true });
  writeFileSync(htmlTarget, renderHtml(document), "utf-8");
  return htmlTarget;
}
