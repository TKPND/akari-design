import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { isAbsolute, relative, resolve } from "node:path";

export const LANES = Object.freeze([
  "classic-school-uniform",
  "professional-service-uniform",
  "sports-ceremony-fictional-uniform",
  "everyday-girly",
  "outings-special-days",
  "hobbies-making",
  "travel-walking",
  "retro-storybook",
  "magic-fantasy-sf",
  "subculture-wildcard",
]);

export const REVIEW_STATUSES = Object.freeze([
  "unreviewed",
  "reject",
  "keep",
  "favorite",
]);

export class ManifestValidationError extends Error {}

const noveltyFields = Object.freeze([
  "lane",
  "wardrobeFamily",
  "setting",
  "action",
  "sceneMode",
  "composition",
  "camera",
  "lighting",
  "cuteBeat",
  "cast",
  "dominantColor",
  "textureType",
]);

const generationStatuses = new Set(["pending", "valid", "failed"]);
const casts = new Set(["solo", "viewer-pov", "two-person", "group"]);
const sceneModes = new Set(["action-reaction", "quiet-posed"]);
const sha256Pattern = /^[a-f0-9]{64}$/;
const permanentAuthorityPaths = new Set([
  "references/akari-v1.5-b3-body-balance.png",
  "references/akari-v1.4-g2-balanced-lines.png",
]);

export function noveltyKey(entry) {
  return noveltyFields.map((field) => String(entry[field] ?? "")).join("\u241f");
}

function fail(message) {
  throw new ManifestValidationError(message);
}

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function hashFile(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function resolveDeclaredPath(path, dataRoot) {
  if (!isNonEmptyString(path)) fail("unsafe artifact path");
  if (isAbsolute(path) || /^[A-Za-z]:[\\/]/.test(path)) fail("unsafe artifact path");

  if (dataRoot === undefined) {
    if (
      path.split(/[\\/]/).some((segment) => segment === "" || segment === "." || segment === "..")
    ) {
      fail("unsafe artifact path");
    }
    return path;
  }

  const resolvedRoot = resolve(dataRoot);
  const resolvedPath = resolve(resolvedRoot, path);
  const pathFromRoot = relative(resolvedRoot, resolvedPath);
  if (
    pathFromRoot === ".." ||
    pathFromRoot.startsWith(`..${"/"}`) ||
    pathFromRoot.startsWith(`..${"\\"}`) ||
    isAbsolute(pathFromRoot)
  ) {
    fail("unsafe artifact path");
  }
  return resolvedPath;
}

function freezeManifest(manifest) {
  for (const entry of manifest.entries) {
    for (const reference of entry.references) Object.freeze(reference);
    Object.freeze(entry.references);
    Object.freeze(entry.generation);
    Object.freeze(entry.artifact);
    Object.freeze(entry);
  }
  Object.freeze(manifest.entries);
  return Object.freeze(manifest);
}

function validateGeneration(entry, batchId) {
  const { generation, artifact } = entry;
  const expectedMode = batchId === "B000" ? "demo" : "built-in-imagegen";
  if (
    !isObject(generation) ||
    generation.toolMode !== expectedMode ||
    !generationStatuses.has(generation.technicalStatus) ||
    ![null, undefined].includes(generation.generationId) && !isNonEmptyString(generation.generationId) ||
    ![null, undefined].includes(generation.requestId) && !isNonEmptyString(generation.requestId) ||
    ![null, undefined].includes(generation.sourcePath) && !isNonEmptyString(generation.sourcePath) ||
    ![null, undefined].includes(generation.failureReason) && !isNonEmptyString(generation.failureReason)
  ) {
    fail("invalid generation metadata");
  }

  if (
    !isObject(artifact) ||
    (artifact.sha256 !== null && !sha256Pattern.test(artifact.sha256)) ||
    (artifact.width !== null && (!Number.isInteger(artifact.width) || artifact.width <= 0)) ||
    (artifact.height !== null && (!Number.isInteger(artifact.height) || artifact.height <= 0)) ||
    (generation.technicalStatus === "valid" &&
      (artifact.sha256 === null || artifact.width === null || artifact.height === null))
  ) {
    fail("invalid generation metadata");
  }
}

export function validateBatchManifest(manifest, { dataRoot, checkFiles = false } = {}) {
  const normalized = structuredClone(manifest);
  if (!isObject(normalized)) fail("manifest must be an object");
  if (normalized.schemaVersion !== 1) fail("schemaVersion must be 1");
  if (!["production", "demo"].includes(normalized.batchType)) fail("invalid batchType");
  if (typeof normalized.batchId !== "string" || !/^B\d{3}$/.test(normalized.batchId)) {
    fail("invalid batchId");
  }
  if (!Array.isArray(normalized.entries) || normalized.entries.length !== 50 || !normalized.entries.every(isObject)) {
    fail("exactly 50 entries");
  }
  if (checkFiles && dataRoot === undefined) fail("dataRoot is required when checkFiles is true");

  const ids = new Set();
  const noveltyKeys = new Set();
  const laneCounts = new Map(LANES.map((lane) => [lane, 0]));
  let textureCount = 0;
  let subcultureCount = 0;
  let soloCount = 0;
  let pairedCount = 0;
  let groupCount = 0;
  let actionReactionCount = 0;
  let quietPosedCount = 0;

  for (const entry of normalized.entries) {
    if (typeof entry.id !== "string" || !new RegExp(`^${normalized.batchId}-\\d{3}$`).test(entry.id)) {
      fail("invalid image id");
    }
    if (ids.has(entry.id)) fail("duplicate image id");
    ids.add(entry.id);

    if (!LANES.includes(entry.lane)) fail("exactly 5 entries per lane");
    laneCounts.set(entry.lane, laneCounts.get(entry.lane) + 1);
    if (entry.textureFocus === true) textureCount += 1;
    if (entry.subculture === true) {
      if (entry.lane !== "subculture-wildcard") fail("exactly 5 subculture entries");
      subcultureCount += 1;
    }
    if (!casts.has(entry.cast)) fail("invalid cast quota");
    if (entry.cast === "solo") soloCount += 1;
    else if (entry.cast === "group") groupCount += 1;
    else pairedCount += 1;
    if (!sceneModes.has(entry.sceneMode)) fail("invalid scene mode quota");
    if (entry.sceneMode === "action-reaction") actionReactionCount += 1;
    else quietPosedCount += 1;

    if (!isNonEmptyString(entry.prompt) || noveltyFields.some((field) => !isNonEmptyString(entry[field]))) {
      fail("missing prompt or novelty field");
    }
    if (!Array.isArray(entry.references) || entry.references.length < 2 || entry.references.length > 4) {
      fail("two to four references");
    }

    const referencePaths = [];
    for (const reference of entry.references) {
      if (
        !isObject(reference) ||
        !isNonEmptyString(reference.path) ||
        !isNonEmptyString(reference.role) ||
        !Array.isArray(reference.exclusions) ||
        !reference.exclusions.every((exclusion) => typeof exclusion === "string")
      ) {
        fail("invalid reference metadata");
      }
      if (!sha256Pattern.test(reference.sha256)) fail("invalid reference sha256");
      referencePaths.push({ path: resolveDeclaredPath(reference.path, dataRoot), sha256: reference.sha256 });
    }
    if (![...permanentAuthorityPaths].every((path) =>
      entry.references.some((reference) => reference.path === path),
    )) {
      fail("missing permanent authority references");
    }

    if (!isObject(entry.artifact) || !isNonEmptyString(entry.artifact.imagePath) || !entry.artifact.imagePath.endsWith(".png") || !isNonEmptyString(entry.artifact.thumbnailPath) || !entry.artifact.thumbnailPath.endsWith(".webp")) {
      fail("invalid artifact extension");
    }
    const imagePath = resolveDeclaredPath(entry.artifact.imagePath, dataRoot);
    const thumbnailPath = resolveDeclaredPath(entry.artifact.thumbnailPath, dataRoot);
    validateGeneration(entry, normalized.batchId);

    if (checkFiles) {
      for (const reference of referencePaths) {
        if (!existsSync(reference.path)) fail("declared file missing");
        if (hashFile(reference.path) !== reference.sha256) fail("invalid reference sha256");
      }
      if (!existsSync(imagePath) || !existsSync(thumbnailPath)) fail("declared file missing");
      if (entry.artifact.sha256 !== null && hashFile(imagePath) !== entry.artifact.sha256) {
        fail("invalid generation metadata");
      }
    }

    const key = noveltyKey(entry);
    if (noveltyKeys.has(key)) fail("duplicate novelty combination");
    noveltyKeys.add(key);
  }

  if ([...laneCounts.values()].some((count) => count !== 5)) fail("exactly 5 entries per lane");
  if (textureCount !== 10) fail("exactly 10 texture-focus entries");
  if (subcultureCount !== 5) fail("exactly 5 subculture entries");
  if (soloCount !== 35 || pairedCount !== 10 || groupCount !== 5) fail("invalid cast quota");
  if (actionReactionCount !== 40 || quietPosedCount !== 10) fail("invalid scene mode quota");

  return freezeManifest(normalized);
}

export function declaredMedia(manifest) {
  const normalized = validateBatchManifest(manifest);
  return new Map(
    normalized.entries.flatMap((entry) => [
      [`${entry.id}:image`, entry.artifact.imagePath],
      [`${entry.id}:thumb`, entry.artifact.thumbnailPath],
    ]),
  );
}
