import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { constants, realpathSync } from "node:fs";
import {
  lstat,
  mkdtemp,
  open,
  readdir,
  realpath,
  rename,
  rm,
} from "node:fs/promises";
import { createServer } from "node:http";
import { networkInterfaces } from "node:os";
import {
  basename,
  dirname,
  isAbsolute,
  join,
  relative,
  resolve,
} from "node:path";
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
const BODY_READ_TIMEOUT_MS = 10_000;
const DEFAULT_THUMBNAIL_REPAIR_TIMEOUT_MS = 15_000;
const STDERR_LIMIT = 64 * 1024;
const PNG_SIGNATURE = Buffer.from("89504e470d0a1a0a", "hex");

class BatchNotFoundError extends Error {}
class BatchValidationError extends Error {}
class UnsafeDataPathError extends Error {}
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

function isContained(root, path) {
  const fromRoot = relative(root, path);
  return fromRoot === "" ||
    (fromRoot !== ".." &&
      !fromRoot.startsWith(`..${"/"}`) &&
      !fromRoot.startsWith(`..${"\\"}`) &&
      !isAbsolute(fromRoot));
}

function requireContained(root, path) {
  if (!isContained(root, path)) {
    throw new UnsafeDataPathError("path escapes dataRoot");
  }
  return path;
}

async function canonicalExistingPath(root, path) {
  const lexicalPath = requireContained(root, resolve(path));
  const canonicalPath = await realpath(lexicalPath);
  return requireContained(root, canonicalPath);
}

async function safeReadFile(root, path, encoding) {
  const canonicalPath = await canonicalExistingPath(root, path);
  const handle = await open(
    canonicalPath,
    constants.O_RDONLY | constants.O_NOFOLLOW,
  );
  try {
    return {
      contents: await handle.readFile(encoding),
      path: canonicalPath,
    };
  } finally {
    await handle.close();
  }
}

async function safeWritablePath(root, path) {
  const lexicalPath = requireContained(root, resolve(path));
  const canonicalParent = requireContained(
    root,
    await realpath(dirname(lexicalPath)),
  );
  const canonicalPath = join(canonicalParent, basename(lexicalPath));
  try {
    const metadata = await lstat(canonicalPath);
    if (metadata.isSymbolicLink()) {
      let symlinkTarget;
      try {
        symlinkTarget = await realpath(canonicalPath);
      } catch (error) {
        if (error.code === "ENOENT") {
          throw new UnsafeDataPathError("dangling symlink is unsafe");
        }
        throw error;
      }
      requireContained(root, symlinkTarget);
    } else {
      requireContained(root, await realpath(canonicalPath));
    }
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
  return canonicalPath;
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

async function readManifest(dataRoot, batchId) {
  if (!/^B\d{3}$/.test(batchId)) throw new BatchNotFoundError();
  let text;
  try {
    ({ contents: text } = await safeReadFile(
      dataRoot,
      join(dataRoot, "batches", batchId, "manifest.json"),
      "utf8",
    ));
  } catch (error) {
    if (error.code === "ENOENT" || error.code === "ENOTDIR") {
      throw new BatchNotFoundError();
    }
    if (error instanceof UnsafeDataPathError) {
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
        ({ contents } = await safeReadFile(
          dataRoot,
          resolve(dataRoot, reference.path),
        ));
      } catch (error) {
        if (error.code === "ENOENT" || error.code === "ENOTDIR") {
          throw new BatchValidationError("declared reference missing");
        }
        if (error instanceof UnsafeDataPathError) {
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

async function readMediaFile(dataRoot, path) {
  try {
    return await safeReadFile(dataRoot, path);
  } catch (error) {
    if (
      error instanceof UnsafeDataPathError ||
      error.code === "ENOENT" ||
      error.code === "ENOTDIR"
    ) {
      return null;
    }
    throw error;
  }
}

async function validPng(dataRoot, path, expectedSha256 = null) {
  const media = await readMediaFile(dataRoot, path);
  const contents = media?.contents;
  if (
    contents === undefined ||
    contents.length < PNG_SIGNATURE.length ||
    !contents.subarray(0, PNG_SIGNATURE.length).equals(PNG_SIGNATURE) ||
    (expectedSha256 !== null && sha256(contents) !== expectedSha256)
  ) {
    return null;
  }
  return media;
}

function hasWebpHeader(media) {
  const contents = media?.contents;
  return contents !== undefined &&
    contents.length >= 12 &&
    contents.subarray(0, 4).toString("ascii") === "RIFF" &&
    contents.subarray(8, 12).toString("ascii") === "WEBP";
}

async function validWebp(dataRoot, path) {
  const media = await readMediaFile(dataRoot, path);
  return hasWebpHeader(media) ? media : null;
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
      let settled = false;
      let forceKillTimer;
      const rejectOnce = (error) => {
        if (settled) return;
        settled = true;
        rejectRun(error);
      };
      const onAbort = () => {
        rejectOnce(new Error("thumbnail builder aborted"));
        child.kill("SIGTERM");
        forceKillTimer = setTimeout(() => child.kill("SIGKILL"), 250);
        forceKillTimer.unref();
      };
      signal?.addEventListener("abort", onAbort, { once: true });
      child.stderr.on("data", (chunk) =>
        appendBounded(stderr, chunk, stderrState)
      );
      child.once("error", rejectOnce);
      child.once("close", (code, terminationSignal) => {
        clearTimeout(forceKillTimer);
        signal?.removeEventListener?.("abort", onAbort);
        if (settled) return;
        settled = true;
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
    ready: reviewed === manifest.entries.length,
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
  const canonicalDataRoot = realpathSync(dataRoot);
  const repairTimeoutMs = thumbnailTimeout(thumbnailRepairTimeoutMs);
  const reviewStore = createReviewStore({ dataRoot: canonicalDataRoot });
  const thumbnailRepairs = new Map();

  async function assertReviewPathsSafe(batchId) {
    const batchDirectory = await canonicalExistingPath(
      canonicalDataRoot,
      join(canonicalDataRoot, "batches", batchId),
    );
    await safeWritablePath(
      canonicalDataRoot,
      join(batchDirectory, "reviews.json"),
    );
    await safeWritablePath(
      canonicalDataRoot,
      join(batchDirectory, "reviews.json.bak"),
    );
  }

  async function repairThumbnail(source, output) {
    const safeOutput = await safeWritablePath(canonicalDataRoot, output);
    const existing = thumbnailRepairs.get(safeOutput);
    if (existing) return existing;
    const repair = (async () => {
      const alreadyValid = await validWebp(canonicalDataRoot, safeOutput);
      if (alreadyValid) return alreadyValid;
      const temporaryDirectory = await mkdtemp(
        join(dirname(safeOutput), ".akari-thumb-"),
      );
      const temporarySource = join(temporaryDirectory, "source.png");
      const temporaryOutput = join(temporaryDirectory, "thumbnail.webp");
      const controller = new AbortController();
      let timer;
      try {
        const sourceHandle = await open(
          temporarySource,
          constants.O_WRONLY |
            constants.O_CREAT |
            constants.O_EXCL,
          0o600,
        );
        try {
          await sourceHandle.writeFile(source.contents);
        } finally {
          await sourceHandle.close();
        }
        const build = Promise.resolve().then(() =>
          thumbnailBuilder(temporarySource, temporaryOutput, {
            signal: controller.signal,
          })
        );
        const timeout = new Promise((_, rejectTimeout) => {
          timer = setTimeout(() => {
            rejectTimeout(new Error("thumbnail repair timed out"));
            controller.abort();
          }, repairTimeoutMs);
          timer.unref();
        });
        await Promise.race([build, timeout]);
        const rebuilt = await validWebp(
          canonicalDataRoot,
          temporaryOutput,
        );
        if (!rebuilt) {
          throw new Error("thumbnail builder produced invalid WebP");
        }
        const checkedOutput = await safeWritablePath(
          canonicalDataRoot,
          safeOutput,
        );
        await rename(temporaryOutput, checkedOutput);
        const installed = await validWebp(
          canonicalDataRoot,
          checkedOutput,
        );
        if (!installed) {
          throw new Error("installed thumbnail is invalid");
        }
        return installed;
      } finally {
        clearTimeout(timer);
        await rm(temporaryDirectory, { recursive: true, force: true });
      }
    })();
    thumbnailRepairs.set(safeOutput, repair);
    try {
      return await repair;
    } finally {
      if (thumbnailRepairs.get(safeOutput) === repair) {
        thumbnailRepairs.delete(safeOutput);
      }
    }
  }

  async function listBatches(response) {
    let entries;
    try {
      const batchesDirectory = await canonicalExistingPath(
        canonicalDataRoot,
        join(canonicalDataRoot, "batches"),
      );
      entries = await readdir(batchesDirectory, {
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
        const manifest = await readManifest(canonicalDataRoot, batchId);
        await assertReviewPathsSafe(batchId);
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
      return await readManifest(canonicalDataRoot, batchId);
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
      manifest = await readManifest(canonicalDataRoot, batchId);
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
    const mediaPath = resolve(canonicalDataRoot, declaredPath);
    if (kind === "image") {
      const media = await validPng(
        canonicalDataRoot,
        mediaPath,
        entry.artifact.sha256,
      );
      if (!media) {
        mediaUnavailable(response);
        return;
      }
      sendMedia(response, media.contents, "image/png");
      return;
    }

    const thumbnail = await validWebp(canonicalDataRoot, mediaPath);
    if (thumbnail) {
      sendMedia(response, thumbnail.contents, "image/webp");
      return;
    }
    const sourcePath = resolve(
      canonicalDataRoot,
      entry.artifact.imagePath,
    );
    const source = await validPng(
      canonicalDataRoot,
      sourcePath,
      entry.artifact.sha256,
    );
    if (!source) {
      mediaUnavailable(response);
      return;
    }
    try {
      const repaired = await repairThumbnail(source, mediaPath);
      sendMedia(response, repaired.contents, "image/webp");
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
        await assertReviewPathsSafe(batchId);
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
        await assertReviewPathsSafe(batchId);
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
