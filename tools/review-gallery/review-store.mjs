import { randomUUID } from "node:crypto";
import { copyFile, mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { REVIEW_STATUSES } from "./manifest.mjs";

const nativeFileSystem = Object.freeze({
  copyFile,
  mkdir,
  readFile,
  rename,
  writeFile,
});

export const REJECT_REASONS = Object.freeze([
  "identity-drift",
  "age-drift",
  "not-cute",
  "duplicate",
  "anatomy",
  "hands",
  "composition",
  "garment",
  "artifact",
  "skin-flat",
  "skin-plastic",
  "compression-missing",
  "compression-excessive",
  "sock-painted-on",
  "tissue-anatomy",
  "fabric-texture-weak",
]);

export class ReviewConflictError extends Error {}
export class ReviewValidationError extends Error {}

const reviewStatuses = new Set(REVIEW_STATUSES);
const rejectReasons = new Set(REJECT_REASONS);

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function manifestIds(batchId, manifest) {
  if (
    !/^B\d{3}$/.test(batchId) ||
    !isObject(manifest) ||
    manifest.batchId !== batchId ||
    !Array.isArray(manifest.entries)
  ) {
    throw new ReviewValidationError("invalid batch manifest");
  }
  const ids = manifest.entries.map(({ id }) => id);
  if (ids.length === 0 || ids.some((id) => typeof id !== "string") || new Set(ids).size !== ids.length) {
    throw new ReviewValidationError("invalid batch manifest");
  }
  return ids;
}

function initialDocument(batchId, ids) {
  return {
    schemaVersion: 1,
    batchId,
    reviews: Object.fromEntries(ids.map((id) => [id, {
      status: "unreviewed",
      reasons: [],
      note: "",
      revision: 0,
      updatedAt: null,
    }])),
  };
}

function validReviewRecord(review) {
  return isObject(review) &&
    reviewStatuses.has(review.status) &&
    Array.isArray(review.reasons) &&
    review.reasons.every((reason) => typeof reason === "string" && rejectReasons.has(reason)) &&
    (review.status === "reject" || review.reasons.length === 0) &&
    typeof review.note === "string" &&
    Number.isSafeInteger(review.revision) && review.revision >= 0 &&
    (review.updatedAt === null || typeof review.updatedAt === "string");
}

function validDocument(document, batchId, ids) {
  if (
    !isObject(document) ||
    document.schemaVersion !== 1 ||
    document.batchId !== batchId ||
    !isObject(document.reviews)
  ) {
    return false;
  }
  const storedIds = Object.keys(document.reviews);
  return storedIds.length === ids.length &&
    ids.every((id) => Object.hasOwn(document.reviews, id) && validReviewRecord(document.reviews[id]));
}

function validatePatch(patch) {
  if (!isObject(patch) || !reviewStatuses.has(patch.status)) {
    throw new ReviewValidationError("invalid review status");
  }
  if (!Array.isArray(patch.reasons) || !patch.reasons.every((reason) =>
    typeof reason === "string" && rejectReasons.has(reason)
  )) {
    throw new ReviewValidationError("invalid review reasons");
  }
  if (patch.status !== "reject" && patch.reasons.length > 0) {
    throw new ReviewValidationError("review reasons require reject status");
  }
  if (typeof patch.note !== "string") {
    throw new ReviewValidationError("invalid review note");
  }
  return {
    status: patch.status,
    reasons: [...patch.reasons],
    note: Array.from(patch.note.trim()).slice(0, 1_000).join(""),
  };
}

export function createReviewStore({
  dataRoot,
  clock = () => new Date().toISOString(),
  fileSystem = nativeFileSystem,
}) {
  const tails = new Map();

  function batchDirectory(batchId) {
    return join(dataRoot, "batches", batchId);
  }

  function paths(batchId) {
    const primary = join(batchDirectory(batchId), "reviews.json");
    return { primary, backup: `${primary}.bak` };
  }

  async function readValidDocument(path, batchId, ids) {
    let text;
    try {
      text = await fileSystem.readFile(path, "utf8");
    } catch (error) {
      if (error.code === "ENOENT") return null;
      throw error;
    }
    try {
      const document = JSON.parse(text);
      return validDocument(document, batchId, ids) ? document : null;
    } catch {
      return null;
    }
  }

  async function loadUnlocked(batchId, manifest) {
    const ids = manifestIds(batchId, manifest);
    const { primary, backup } = paths(batchId);
    const primaryDocument = await readValidDocument(primary, batchId, ids);
    if (primaryDocument) return primaryDocument;

    const backupDocument = await readValidDocument(backup, batchId, ids);
    if (backupDocument) {
      await fileSystem.mkdir(batchDirectory(batchId), { recursive: true });
      await fileSystem.copyFile(backup, primary);
      return backupDocument;
    }
    return initialDocument(batchId, ids);
  }

  function enqueue(batchId, work) {
    const predecessor = tails.get(batchId) ?? Promise.resolve();
    const result = predecessor.catch(() => undefined).then(work);
    tails.set(batchId, result.catch(() => undefined));
    return result;
  }

  function load(batchId, manifest) {
    return enqueue(batchId, () => loadUnlocked(batchId, manifest));
  }

  function update(batchId, manifest, imageId, expectedRevision, patch) {
    return enqueue(batchId, async () => {
      const ids = manifestIds(batchId, manifest);
      if (!ids.includes(imageId)) {
        throw new ReviewValidationError("unknown image id");
      }
      const document = await loadUnlocked(batchId, manifest);
      const current = document.reviews[imageId];
      if (expectedRevision !== current.revision) {
        throw new ReviewConflictError("stale review revision");
      }
      if (!Number.isSafeInteger(current.revision + 1)) {
        throw new ReviewValidationError("review revision cannot be incremented safely");
      }
      const reviewPatch = validatePatch(patch);
      const updatedAt = clock();
      if (typeof updatedAt !== "string") {
        throw new ReviewValidationError("invalid review timestamp");
      }
      const updated = {
        ...reviewPatch,
        revision: current.revision + 1,
        updatedAt,
      };
      document.reviews[imageId] = updated;

      const { primary, backup } = paths(batchId);
      await fileSystem.mkdir(batchDirectory(batchId), { recursive: true });
      if (await readValidDocument(primary, batchId, ids)) {
        await fileSystem.copyFile(primary, backup);
      }
      const temporary = `${primary}.${process.pid}.${randomUUID()}.tmp`;
      await fileSystem.writeFile(
        temporary,
        `${JSON.stringify(document, null, 2)}\n`,
        "utf8",
      );
      await fileSystem.rename(temporary, primary);
      return updated;
    });
  }

  return { load, update };
}
