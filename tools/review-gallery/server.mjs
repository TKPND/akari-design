import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { createServer } from "node:http";
import { networkInterfaces } from "node:os";
import { isAbsolute, join, resolve } from "node:path";
import {
  ManifestValidationError,
  declaredMedia,
  validateBatchManifest,
} from "./manifest.mjs";
import {
  ReviewConflictError,
  ReviewValidationError,
  createReviewStore,
} from "./review-store.mjs";

const BODY_LIMIT = 64 * 1024;
const PNG_SIGNATURE = Buffer.from("89504e470d0a1a0a", "hex");

class BatchNotFoundError extends Error {}
class BatchValidationError extends Error {}
class RequestBodyError extends Error {
  constructor(message, { tooLarge = false } = {}) {
    super(message);
    this.tooLarge = tooLarge;
  }
}

function localInterfaceAddresses() {
  return Object.values(networkInterfaces())
    .flat()
    .filter(Boolean)
    .map((address) => address.address);
}

function ipv4Number(host) {
  const parts = host.split(".");
  if (
    parts.length !== 4 ||
    parts.some((part) => !/^(0|[1-9]\d{0,2})$/.test(part))
  ) {
    throw new Error("Tailscale IPv4 required");
  }
  const octets = parts.map(Number);
  if (octets.some((octet) => octet > 255)) {
    throw new Error("Tailscale IPv4 required");
  }
  return (
    (
      (octets[0] << 24) |
      (octets[1] << 16) |
      (octets[2] << 8) |
      octets[3]
    ) >>> 0
  );
}

export function assertSafeBindHost(
  host,
  {
    allowLoopback = false,
    interfaceAddresses = localInterfaceAddresses(),
  } = {},
) {
  if (host === "0.0.0.0" || host === "::") {
    throw new Error("public bind forbidden");
  }
  if (host === "127.0.0.1") {
    if (!allowLoopback) throw new Error("loopback bind forbidden");
    return host;
  }
  const address = ipv4Number(host);
  if ((address & 0xffc00000) !== 0x64400000) {
    throw new Error("Tailscale IPv4 required");
  }
  if (!new Set(interfaceAddresses).has(host)) {
    throw new Error("host not present on a local interface");
  }
  return host;
}

function jsonResponse(response, status, payload) {
  const body = Buffer.from(`${JSON.stringify(payload)}\n`, "utf8");
  response.writeHead(status, {
    "cache-control": "no-store",
    "content-length": body.length,
    "content-type": "application/json; charset=utf-8",
  });
  response.end(body);
}

function success(response, data) {
  jsonResponse(response, 200, { ok: true, data });
}

function failure(response, status, code, message) {
  jsonResponse(response, status, {
    ok: false,
    error: { code, message },
  });
}

function notFound(response) {
  failure(response, 404, "not_found", "resource not found");
}

function decodeRoute(pathname) {
  try {
    return pathname.split("/").map((segment) => decodeURIComponent(segment));
  } catch {
    return null;
  }
}

async function readJsonBody(request) {
  const chunks = [];
  let size = 0;
  let tooLarge = false;
  for await (const chunk of request) {
    size += chunk.length;
    if (size > BODY_LIMIT) {
      tooLarge = true;
    } else {
      chunks.push(chunk);
    }
  }
  if (tooLarge) {
    throw new RequestBodyError("request body exceeds 65536 bytes", {
      tooLarge: true,
    });
  }
  try {
    return JSON.parse(Buffer.concat(chunks).toString("utf8"));
  } catch {
    throw new RequestBodyError("invalid JSON body");
  }
}

function sha256(contents) {
  return createHash("sha256").update(contents).digest("hex");
}

async function readManifest(dataRoot, batchId) {
  if (!/^B\d{3}$/.test(batchId)) throw new BatchNotFoundError();
  let text;
  try {
    text = await readFile(
      join(dataRoot, "batches", batchId, "manifest.json"),
      "utf8",
    );
  } catch (error) {
    if (error.code === "ENOENT" || error.code === "ENOTDIR") {
      throw new BatchNotFoundError();
    }
    throw error;
  }

  let rawManifest;
  try {
    rawManifest = JSON.parse(text);
  } catch {
    throw new BatchValidationError("invalid manifest JSON");
  }

  let manifest;
  try {
    manifest = validateBatchManifest(rawManifest, {
      dataRoot,
      checkFiles: false,
    });
  } catch (error) {
    if (error instanceof ManifestValidationError) {
      throw new BatchValidationError(error.message);
    }
    throw error;
  }
  if (manifest.batchId !== batchId) {
    throw new BatchValidationError("batchId does not match directory");
  }

  const checkedReferences = new Set();
  for (const entry of manifest.entries) {
    for (const reference of entry.references) {
      const key = `${reference.path}\u241f${reference.sha256}`;
      if (checkedReferences.has(key)) continue;
      checkedReferences.add(key);
      let contents;
      try {
        contents = await readFile(resolve(dataRoot, reference.path));
      } catch (error) {
        if (error.code === "ENOENT" || error.code === "ENOTDIR") {
          throw new BatchValidationError("declared reference missing");
        }
        throw error;
      }
      if (sha256(contents) !== reference.sha256) {
        throw new BatchValidationError("invalid reference sha256");
      }
    }
  }
  return manifest;
}

async function readMediaFile(path) {
  try {
    return await readFile(path);
  } catch (error) {
    if (error.code === "ENOENT" || error.code === "ENOTDIR") return null;
    throw error;
  }
}

async function validPng(path, expectedSha256 = null) {
  const contents = await readMediaFile(path);
  if (
    contents === null ||
    contents.length < PNG_SIGNATURE.length ||
    !contents.subarray(0, PNG_SIGNATURE.length).equals(PNG_SIGNATURE) ||
    (expectedSha256 !== null && sha256(contents) !== expectedSha256)
  ) {
    return null;
  }
  return contents;
}

function hasWebpHeader(contents) {
  return contents !== null &&
    contents.length >= 12 &&
    contents.subarray(0, 4).toString("ascii") === "RIFF" &&
    contents.subarray(8, 12).toString("ascii") === "WEBP";
}

async function validWebp(path) {
  const contents = await readMediaFile(path);
  return hasWebpHeader(contents) ? contents : null;
}

function productionThumbnailBuilder({
  repoRoot,
  pythonExecutable,
}) {
  return async (source, output) => {
    if (
      typeof repoRoot !== "string" ||
      !isAbsolute(repoRoot) ||
      typeof pythonExecutable !== "string" ||
      !isAbsolute(pythonExecutable)
    ) {
      throw new Error("absolute repoRoot and pythonExecutable are required");
    }
    const script = join(repoRoot, "scripts", "build_akari_review_thumbnail.py");
    await new Promise((resolveRun, rejectRun) => {
      const child = spawn(pythonExecutable, [
        script,
        "--input",
        source,
        "--output",
        output,
        "--max-edge",
        "512",
      ], {
        stdio: ["ignore", "ignore", "pipe"],
      });
      const stderr = [];
      child.stderr.on("data", (chunk) => stderr.push(chunk));
      child.once("error", rejectRun);
      child.once("close", (code, signal) => {
        if (code === 0) {
          resolveRun();
          return;
        }
        const detail = Buffer.concat(stderr).toString("utf8").trim();
        rejectRun(new Error(
          `thumbnail builder failed (${signal ?? code})${detail ? `: ${detail}` : ""}`,
        ));
      });
    });
  };
}

function sendMedia(response, contents, contentType) {
  response.writeHead(200, {
    "content-length": contents.length,
    "content-type": contentType,
  });
  response.end(contents);
}

function mediaUnavailable(response) {
  failure(response, 404, "media_unavailable", "media unavailable");
}

function progressSummary(manifest, reviews) {
  const reviewed = Object.values(reviews.reviews)
    .filter(({ status }) => status !== "unreviewed")
    .length;
  return {
    batchId: manifest.batchId,
    title: manifest.title,
    disabled: false,
    validationMessage: null,
    reviewed,
    total: manifest.entries.length,
    ready: reviewed === manifest.entries.length,
  };
}

export function createGalleryServer({
  dataRoot,
  repoRoot,
  pythonExecutable,
  thumbnailBuilder = productionThumbnailBuilder({
    repoRoot,
    pythonExecutable,
  }),
}) {
  const reviewStore = createReviewStore({ dataRoot });
  const thumbnailRepairs = new Map();

  async function repairThumbnail(source, output) {
    const existing = thumbnailRepairs.get(output);
    if (existing) return existing;
    const repair = (async () => {
      const alreadyValid = await validWebp(output);
      if (alreadyValid) return alreadyValid;
      await thumbnailBuilder(source, output);
      const rebuilt = await validWebp(output);
      if (!rebuilt) throw new Error("thumbnail builder produced invalid WebP");
      return rebuilt;
    })();
    thumbnailRepairs.set(output, repair);
    try {
      return await repair;
    } finally {
      if (thumbnailRepairs.get(output) === repair) {
        thumbnailRepairs.delete(output);
      }
    }
  }

  async function listBatches(response) {
    let entries;
    try {
      entries = await readdir(join(dataRoot, "batches"), {
        withFileTypes: true,
      });
    } catch (error) {
      if (error.code === "ENOENT") {
        success(response, { batches: [] });
        return;
      }
      throw error;
    }
    const batchIds = entries
      .filter((entry) => entry.isDirectory() && /^B\d{3}$/.test(entry.name))
      .map((entry) => entry.name)
      .sort();
    const batches = [];
    for (const batchId of batchIds) {
      try {
        const manifest = await readManifest(dataRoot, batchId);
        const reviews = await reviewStore.load(batchId, manifest);
        batches.push(progressSummary(manifest, reviews));
      } catch (error) {
        batches.push({
          batchId,
          title: null,
          disabled: true,
          validationMessage: error.message,
          reviewed: 0,
          total: 0,
          ready: false,
        });
      }
    }
    success(response, { batches });
  }

  async function batchForApi(batchId, response) {
    try {
      return await readManifest(dataRoot, batchId);
    } catch (error) {
      if (error instanceof BatchNotFoundError) {
        notFound(response);
        return null;
      }
      if (error instanceof BatchValidationError) {
        failure(response, 422, "invalid_batch", error.message);
        return null;
      }
      throw error;
    }
  }

  async function serveMedia(batchId, imageId, kind, response) {
    let manifest;
    try {
      manifest = await readManifest(dataRoot, batchId);
    } catch {
      mediaUnavailable(response);
      return;
    }
    const media = declaredMedia(manifest);
    const declaredPath = media.get(`${imageId}:${kind}`);
    if (declaredPath === undefined) {
      mediaUnavailable(response);
      return;
    }
    const entry = manifest.entries.find(({ id }) => id === imageId);
    const mediaPath = resolve(dataRoot, declaredPath);
    if (kind === "image") {
      const contents = await validPng(mediaPath, entry.artifact.sha256);
      if (!contents) {
        mediaUnavailable(response);
        return;
      }
      sendMedia(response, contents, "image/png");
      return;
    }

    const thumbnail = await validWebp(mediaPath);
    if (thumbnail) {
      sendMedia(response, thumbnail, "image/webp");
      return;
    }
    const sourcePath = resolve(dataRoot, entry.artifact.imagePath);
    if (!await validPng(sourcePath, entry.artifact.sha256)) {
      mediaUnavailable(response);
      return;
    }
    try {
      const repaired = await repairThumbnail(sourcePath, mediaPath);
      sendMedia(response, repaired, "image/webp");
    } catch {
      mediaUnavailable(response);
    }
  }

  async function handle(request, response) {
    let url;
    try {
      url = new URL(request.url, "http://localhost");
    } catch {
      notFound(response);
      return;
    }
    const segments = decodeRoute(url.pathname);
    if (segments === null) {
      notFound(response);
      return;
    }

    if (
      request.method === "GET" &&
      segments.length === 3 &&
      segments[1] === "api" &&
      segments[2] === "batches"
    ) {
      await listBatches(response);
      return;
    }

    if (
      request.method === "GET" &&
      segments.length === 4 &&
      segments[1] === "api" &&
      segments[2] === "batches"
    ) {
      const manifest = await batchForApi(segments[3], response);
      if (manifest) success(response, manifest);
      return;
    }

    if (
      request.method === "GET" &&
      segments.length === 5 &&
      segments[1] === "api" &&
      segments[2] === "batches" &&
      segments[4] === "reviews"
    ) {
      const batchId = segments[3];
      const manifest = await batchForApi(batchId, response);
      if (!manifest) return;
      try {
        success(response, await reviewStore.load(batchId, manifest));
      } catch {
        failure(response, 500, "review_load_failed", "failed to load reviews");
      }
      return;
    }

    if (
      request.method === "PUT" &&
      segments.length === 6 &&
      segments[1] === "api" &&
      segments[2] === "batches" &&
      segments[4] === "reviews"
    ) {
      const batchId = segments[3];
      const imageId = segments[5];
      const manifest = await batchForApi(batchId, response);
      if (!manifest) return;
      if (!manifest.entries.some(({ id }) => id === imageId)) {
        notFound(response);
        return;
      }
      let body;
      try {
        body = await readJsonBody(request);
      } catch (error) {
        if (error instanceof RequestBodyError) {
          failure(
            response,
            error.tooLarge ? 413 : 422,
            error.tooLarge ? "request_too_large" : "invalid_review",
            error.message,
          );
          return;
        }
        throw error;
      }
      if (
        body === null ||
        typeof body !== "object" ||
        Array.isArray(body) ||
        !Number.isSafeInteger(body.expectedRevision) ||
        body.expectedRevision < 0
      ) {
        failure(
          response,
          422,
          "invalid_review",
          "invalid expected review revision",
        );
        return;
      }
      try {
        const updated = await reviewStore.update(
          batchId,
          manifest,
          imageId,
          body.expectedRevision,
          {
            status: body.status,
            reasons: body.reasons,
            note: body.note,
          },
        );
        success(response, updated);
      } catch (error) {
        if (error instanceof ReviewConflictError) {
          failure(
            response,
            409,
            "review_conflict",
            "review revision changed; reload this image",
          );
        } else if (error instanceof ReviewValidationError) {
          failure(response, 422, "invalid_review", error.message);
        } else {
          failure(
            response,
            500,
            "durable_write_failed",
            "failed to persist review",
          );
        }
      }
      return;
    }

    if (
      request.method === "GET" &&
      segments.length === 5 &&
      segments[1] === "media" &&
      (segments[4] === "image" || segments[4] === "thumb")
    ) {
      await serveMedia(segments[2], segments[3], segments[4], response);
      return;
    }

    notFound(response);
  }

  return createServer((request, response) => {
    handle(request, response).catch(() => {
      if (!response.headersSent) {
        failure(response, 500, "internal_error", "internal server error");
      } else {
        response.destroy();
      }
    });
  });
}

export async function startGalleryServer(options) {
  const {
    host,
    port,
    allowLoopback = false,
  } = options;
  const interfaceOptions = Object.hasOwn(options, "interfaceAddresses")
    ? { interfaceAddresses: options.interfaceAddresses }
    : {};
  const normalizedHost = assertSafeBindHost(host, {
    allowLoopback,
    ...interfaceOptions,
  });
  if (!Number.isInteger(port) || port < 0 || port > 65_535) {
    throw new Error("invalid gallery port");
  }
  const server = createGalleryServer(options);
  await new Promise((resolveListen, rejectListen) => {
    const onError = (error) => {
      server.off("listening", onListening);
      rejectListen(new Error(
        `failed to listen on ${normalizedHost}:${port}: ${error.message}`,
        { cause: error },
      ));
    };
    const onListening = () => {
      server.off("error", onError);
      resolveListen();
    };
    server.once("error", onError);
    server.once("listening", onListening);
    server.listen(port, normalizedHost);
  });
  const address = server.address();
  const actualPort = address.port;
  let closed = false;
  return {
    server,
    host: normalizedHost,
    port: actualPort,
    url: `http://${normalizedHost}:${actualPort}`,
    close() {
      if (closed) return Promise.resolve();
      closed = true;
      return new Promise((resolveClose, rejectClose) => {
        server.close((error) => {
          if (error) rejectClose(error);
          else resolveClose();
        });
      });
    },
  };
}
