import { spawn } from "node:child_process";
import { createHash, randomUUID } from "node:crypto";
import { readFile } from "node:fs/promises";
import { createServer } from "node:http";
import { networkInterfaces } from "node:os";
import {
  isAbsolute,
  join,
} from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";
import {
  ManifestValidationError,
  declaredMedia,
  isReviewableEntry,
  validateBatchManifest,
} from "./manifest.mjs";
import { createPinnedRoot } from "./pinned-fs.mjs";
import {
  ReviewConflictError,
  ReviewValidationError,
  createReviewStore,
} from "./review-store.mjs";

const BODY_LIMIT = 64 * 1024;
const BODY_READ_TIMEOUT_MS = 10_000;
const DEFAULT_THUMBNAIL_REPAIR_TIMEOUT_MS = 15_000;
const STDERR_LIMIT = 64 * 1024;
const PNG_SIGNATURE = Buffer.from("89504e470d0a1a0a", "hex");
const disposePinnedRoot = Symbol("disposePinnedRoot");
const staticAssets = new Map([
  ["/", {
    path: new URL("./public/index.html", import.meta.url),
    contentType: "text/html; charset=utf-8",
  }],
  ["/styles.css", {
    path: new URL("./public/styles.css", import.meta.url),
    contentType: "text/css; charset=utf-8",
  }],
  ["/app.js", {
    path: new URL("./public/app.js", import.meta.url),
    contentType: "text/javascript; charset=utf-8",
  }],
]);

export function parseGalleryOptions(argv, env) {
  const { values } = parseArgs({
    args: argv,
    options: {
      "repo-root": { type: "string" },
      "data-root": { type: "string" },
      host: { type: "string" },
      port: { type: "string" },
      python: { type: "string" },
    },
    strict: true,
  });
  const options = {
    repoRoot: values["repo-root"] ?? env.AKARI_GALLERY_REPO_ROOT,
    dataRoot: values["data-root"] ?? env.AKARI_GALLERY_DATA_ROOT,
    host: values.host ?? env.AKARI_GALLERY_HOST,
    port: Number(values.port ?? env.AKARI_GALLERY_PORT),
    pythonExecutable: values.python ?? env.AKARI_GALLERY_PYTHON,
  };
  for (const [name, value] of [
    ["repo root", options.repoRoot],
    ["data root", options.dataRoot],
    ["host", options.host],
    ["python executable", options.pythonExecutable],
  ]) {
    if (typeof value !== "string" || value.length === 0) {
      throw new Error(`${name} required`);
    }
  }
  for (const [name, value] of [
    ["repo root", options.repoRoot],
    ["data root", options.dataRoot],
    ["python executable", options.pythonExecutable],
  ]) {
    if (!isAbsolute(value)) {
      throw new Error(`${name} must be an absolute path`);
    }
  }
  if (!Number.isInteger(options.port) || options.port < 1 || options.port > 65_535) {
    throw new Error("invalid gallery port");
  }
  return options;
}

class BatchNotFoundError extends Error {}
class BatchValidationError extends Error {}
class RequestBodyError extends Error {
  constructor(message, { status = 422, code = "invalid_review" } = {}) {
    super(message);
    this.status = status;
    this.code = code;
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

async function serveStaticAsset(pathname, response) {
  const asset = staticAssets.get(pathname);
  if (asset === undefined) return false;
  const contents = await readFile(asset.path);
  response.writeHead(200, {
    "cache-control": "no-store",
    "content-length": contents.length,
    "content-type": asset.contentType,
  });
  response.end(contents);
  return true;
}

function decodeRoute(pathname) {
  try {
    return pathname.split("/").map((segment) => decodeURIComponent(segment));
  } catch {
    return null;
  }
}

async function readJsonBody(request) {
  const declaredLength = request.headers["content-length"];
  if (
    typeof declaredLength === "string" &&
    /^\d+$/.test(declaredLength) &&
    BigInt(declaredLength) > BigInt(BODY_LIMIT)
  ) {
    throw new RequestBodyError("request body exceeds 65536 bytes", {
      status: 413,
      code: "request_too_large",
    });
  }

  const contents = await new Promise((resolveBody, rejectBody) => {
    const chunks = [];
    let size = 0;
    let timer;
    const cleanup = () => {
      clearTimeout(timer);
      request.off("data", onData);
      request.off("end", onEnd);
      request.off("error", onError);
      request.off("aborted", onAborted);
    };
    const reject = (error) => {
      cleanup();
      request.pause();
      rejectBody(error);
    };
    const onData = (chunk) => {
      size += chunk.length;
      if (size > BODY_LIMIT) {
        reject(new RequestBodyError("request body exceeds 65536 bytes", {
          status: 413,
          code: "request_too_large",
        }));
        return;
      }
      chunks.push(chunk);
    };
    const onEnd = () => {
      cleanup();
      resolveBody(Buffer.concat(chunks));
    };
    const onError = (error) => reject(error);
    const onAborted = () => reject(new RequestBodyError(
      "request body aborted",
    ));
    request.on("data", onData);
    request.once("end", onEnd);
    request.once("error", onError);
    request.once("aborted", onAborted);
    timer = setTimeout(() => {
      reject(new RequestBodyError("request body timeout", {
        status: 408,
        code: "request_timeout",
      }));
    }, BODY_READ_TIMEOUT_MS);
    timer.unref();
  });

  try {
    return JSON.parse(contents.toString("utf8"));
  } catch {
    throw new RequestBodyError("invalid JSON body");
  }
}

function closeRequestAfterResponse(request, response) {
  response.shouldKeepAlive = false;
  response.setHeader("connection", "close");
  response.once("finish", () => request.destroy());
}

function appendBounded(chunks, chunk, state) {
  if (state.bytes >= STDERR_LIMIT) return;
  const remaining = STDERR_LIMIT - state.bytes;
  const bounded = chunk.length > remaining ? chunk.subarray(0, remaining) : chunk;
  chunks.push(bounded);
  state.bytes += bounded.length;
}

function thumbnailTimeout(value) {
  if (Number.isFinite(value) && value > 0) return value;
  return DEFAULT_THUMBNAIL_REPAIR_TIMEOUT_MS;
}

function sha256(contents) {
  return createHash("sha256").update(contents).digest("hex");
}

function unsafeFileSystemError(error) {
  return error.code === "EACCES" || error.code === "ELOOP";
}

async function readManifest(pinnedRoot, batchId) {
  if (!/^B\d{3}$/.test(batchId)) throw new BatchNotFoundError();
  let text;
  try {
    text = await pinnedRoot.fileSystem.readFile(
      `batches/${batchId}/manifest.json`,
      "utf8",
    );
  } catch (error) {
    if (error.code === "ENOENT" || error.code === "ENOTDIR") {
      throw new BatchNotFoundError();
    }
    if (unsafeFileSystemError(error)) {
      throw new BatchValidationError("unsafe data path");
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
      dataRoot: pinnedRoot.canonicalRoot,
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
        contents = await pinnedRoot.fileSystem.readFile(reference.path);
      } catch (error) {
        if (error.code === "ENOENT" || error.code === "ENOTDIR") {
          throw new BatchValidationError("declared reference missing");
        }
        if (unsafeFileSystemError(error)) {
          throw new BatchValidationError("unsafe data path");
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

async function readMediaFile(pinnedRoot, path) {
  try {
    return await pinnedRoot.fileSystem.readFile(path);
  } catch (error) {
    if (
      unsafeFileSystemError(error) ||
      error.code === "ENOENT" ||
      error.code === "ENOTDIR"
    ) {
      return null;
    }
    throw error;
  }
}

async function validPng(pinnedRoot, path, expectedSha256 = null) {
  const contents = await readMediaFile(pinnedRoot, path);
  if (
    contents == null ||
    contents.length < PNG_SIGNATURE.length ||
    !contents.subarray(0, PNG_SIGNATURE.length).equals(PNG_SIGNATURE) ||
    (expectedSha256 !== null && sha256(contents) !== expectedSha256)
  ) {
    return null;
  }
  return contents;
}

function hasWebpHeader(contents) {
  return contents != null &&
    contents.length >= 12 &&
    contents.subarray(0, 4).toString("ascii") === "RIFF" &&
    contents.subarray(8, 12).toString("ascii") === "WEBP";
}

async function validWebp(pinnedRoot, path) {
  const contents = await readMediaFile(pinnedRoot, path);
  return hasWebpHeader(contents) ? contents : null;
}

async function validWebpAt(directory, name) {
  let contents;
  try {
    contents = await directory.readFile(name);
  } catch (error) {
    if (error.code === "ENOENT" || error.code === "ENOTDIR") return null;
    throw error;
  }
  return hasWebpHeader(contents) ? contents : null;
}

function productionThumbnailBuilder({
  repoRoot,
  pythonExecutable,
}) {
  return async (source, output, { signal } = {}) => {
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
      const stderrState = { bytes: 0 };
      let aborted = false;
      let spawned = false;
      let postSpawnError;
      let settled = false;
      let forceKillTimer;
      const onSpawn = () => {
        spawned = true;
      };
      const cleanup = () => {
        clearTimeout(forceKillTimer);
        signal?.removeEventListener?.("abort", onAbort);
        child.off("error", onError);
        child.off("spawn", onSpawn);
      };
      const rejectOnce = (error) => {
        if (settled) return;
        settled = true;
        cleanup();
        rejectRun(error);
      };
      const onError = (error) => {
        if (!spawned) {
          rejectOnce(error);
          return;
        }
        postSpawnError ??= error;
      };
      const onAbort = () => {
        if (settled) return;
        aborted = true;
        child.kill("SIGTERM");
        forceKillTimer = setTimeout(() => child.kill("SIGKILL"), 250);
        forceKillTimer.unref();
      };
      signal?.addEventListener("abort", onAbort, { once: true });
      child.stderr.on("data", (chunk) =>
        appendBounded(stderr, chunk, stderrState)
      );
      child.once("spawn", onSpawn);
      child.on("error", onError);
      child.once("close", (code, terminationSignal) => {
        if (settled) return;
        settled = true;
        cleanup();
        if (postSpawnError) {
          rejectRun(postSpawnError);
          return;
        }
        if (aborted) {
          rejectRun(new Error("thumbnail builder aborted"));
          return;
        }
        if (code === 0) {
          resolveRun();
          return;
        }
        const detail = Buffer.concat(stderr).toString("utf8").trim();
        rejectRun(new Error(
          `thumbnail builder failed (${terminationSignal ?? code})${detail ? `: ${detail}` : ""}`,
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
    ready: manifest.entries.every(isReviewableEntry) &&
      reviewed === manifest.entries.length,
  };
}

export function createGalleryServer({
  dataRoot,
  repoRoot,
  pythonExecutable,
  thumbnailRepairTimeoutMs,
  thumbnailBuilder = productionThumbnailBuilder({
    repoRoot,
    pythonExecutable,
  }),
}) {
  const pinnedRoot = createPinnedRoot(dataRoot);
  const repairTimeoutMs = thumbnailTimeout(thumbnailRepairTimeoutMs);
  const reviewStore = createReviewStore({
    dataRoot: pinnedRoot.canonicalRoot,
    fileSystem: pinnedRoot.fileSystem,
  });
  const thumbnailRepairs = new Map();

  async function repairThumbnail(source, output) {
    const existing = thumbnailRepairs.get(output);
    if (existing) return existing.result;
    let resultSettled = false;
    let rejectResult;
    let resolveResult;
    const result = new Promise((resolve, reject) => {
      resolveResult = (value) => {
        if (resultSettled) return;
        resultSettled = true;
        resolve(value);
      };
      rejectResult = (error) => {
        if (resultSettled) return;
        resultSettled = true;
        reject(error);
      };
    });
    const entry = { result };
    thumbnailRepairs.set(output, entry);
    const lease = pinnedRoot.withParent(
      output,
      async (outputDirectory, outputName) => {
        const alreadyValid = await validWebpAt(
          outputDirectory,
          outputName,
        );
        if (alreadyValid) return alreadyValid;
        const temporaryName = `.akari-thumb-${randomUUID()}`;
        await outputDirectory.mkdir(temporaryName, { mode: 0o700 });
        try {
          return await outputDirectory.withDirectory(
            temporaryName,
            async (temporaryDirectory) => {
              await temporaryDirectory.writeFile("source.png", source);
              const controller = new AbortController();
              const build = Promise.resolve().then(() =>
                thumbnailBuilder(
                  temporaryDirectory.path("source.png"),
                  temporaryDirectory.path("thumbnail.webp"),
                  { signal: controller.signal },
                )
              );
              let timedOut = false;
              const timer = setTimeout(() => {
                timedOut = true;
                rejectResult(new Error("thumbnail repair timed out"));
                controller.abort();
              }, repairTimeoutMs);
              timer.unref();
              try {
                await build;
              } catch (error) {
                if (!timedOut) throw error;
              } finally {
                clearTimeout(timer);
              }
              if (timedOut) return undefined;
              const rebuilt = await validWebpAt(
                temporaryDirectory,
                "thumbnail.webp",
              );
              if (!rebuilt) {
                throw new Error(
                  "thumbnail builder produced invalid WebP",
                );
              }
              await temporaryDirectory.renameTo(
                "thumbnail.webp",
                outputDirectory,
                outputName,
              );
              const installed = await validWebpAt(
                outputDirectory,
                outputName,
              );
              if (!installed) {
                throw new Error("installed thumbnail is invalid");
              }
              return installed;
            },
          );
        } finally {
          await outputDirectory.remove(temporaryName, {
            recursive: true,
            force: true,
          });
        }
      },
    );
    lease.then(resolveResult, rejectResult).finally(() => {
      if (thumbnailRepairs.get(output) === entry) {
        thumbnailRepairs.delete(output);
      }
    });
    return result;
  }

  async function listBatches(response) {
    let entries;
    try {
      entries = await pinnedRoot.readdir("batches", {
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
        const manifest = await readManifest(pinnedRoot, batchId);
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
      return await readManifest(pinnedRoot, batchId);
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
      manifest = await readManifest(pinnedRoot, batchId);
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
    if (!isReviewableEntry(entry)) {
      mediaUnavailable(response);
      return;
    }
    if (kind === "image") {
      const media = await validPng(
        pinnedRoot,
        declaredPath,
        entry.artifact.sha256,
      );
      if (!media) {
        mediaUnavailable(response);
        return;
      }
      sendMedia(response, media, "image/png");
      return;
    }

    const thumbnail = await validWebp(pinnedRoot, declaredPath);
    if (thumbnail) {
      sendMedia(response, thumbnail, "image/webp");
      return;
    }
    const source = await validPng(
      pinnedRoot,
      entry.artifact.imagePath,
      entry.artifact.sha256,
    );
    if (!source) {
      mediaUnavailable(response);
      return;
    }
    try {
      const repaired = await repairThumbnail(source, declaredPath);
      sendMedia(response, repaired, "image/webp");
    } catch {
      mediaUnavailable(response);
    }
  }

  async function handle(request, response) {
    const requestTarget = request.url;
    let url;
    try {
      url = new URL(requestTarget, "http://localhost");
    } catch {
      notFound(response);
      return;
    }
    const queryIndex = requestTarget.indexOf("?");
    const rawPathname = queryIndex === -1
      ? requestTarget
      : requestTarget.slice(0, queryIndex);
    if (rawPathname !== url.pathname) {
      notFound(response);
      return;
    }
    if (
      request.method === "GET" &&
      await serveStaticAsset(url.pathname, response)
    ) {
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
      const entry = manifest.entries.find(({ id }) => id === imageId);
      if (!isReviewableEntry(entry)) {
        failure(
          response,
          409,
          "non_reviewable",
          "image is not technically valid for review",
        );
        return;
      }
      let body;
      try {
        body = await readJsonBody(request);
      } catch (error) {
        if (error instanceof RequestBodyError) {
          if (error.status === 413 || error.status === 408) {
            closeRequestAfterResponse(request, response);
          }
          failure(
            response,
            error.status,
            error.code,
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

  const server = createServer((request, response) => {
    pinnedRoot.withLease(() => handle(request, response)).catch(() => {
      if (!response.headersSent) {
        failure(response, 500, "internal_error", "internal server error");
      } else {
        response.destroy();
      }
    });
  });
  let pinnedRootClosed = false;
  const closePinnedRoot = () => {
    if (pinnedRootClosed) return;
    pinnedRootClosed = true;
    pinnedRoot.close();
  };
  server[disposePinnedRoot] = closePinnedRoot;
  server.once("close", closePinnedRoot);
  return server;
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
      server[disposePinnedRoot]?.();
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

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  Promise.resolve()
    .then(() => startGalleryServer(
      parseGalleryOptions(process.argv.slice(2), process.env),
    ))
    .then(({ url }) => {
      console.log(`Akari review gallery listening on ${url}`);
    })
    .catch((error) => {
      console.error(error.message);
      process.exitCode = 1;
    });
}
