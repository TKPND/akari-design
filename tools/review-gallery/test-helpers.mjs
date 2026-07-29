import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { LANES } from "./manifest.mjs";

const ONE_PIXEL_PNG = Buffer.from(
  "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
  "base64",
);
const ONE_PIXEL_WEBP = Buffer.from(
  "UklGRiIAAABXRUJQVlA4IBYAAAAwAQCdASoBAAEAAUAmJQBOgCHwAP7+3gAA",
  "base64",
);

export function makeValidManifest(overrides = {}) {
  const entries = LANES.flatMap((lane, laneIndex) =>
    Array.from({ length: 5 }, (_, offset) => {
      const ordinal = laneIndex * 5 + offset + 1;
      return {
        id: `B001-${String(ordinal).padStart(3, "0")}`,
        lane,
        cuteBeat: `beat-${laneIndex}-${offset}`,
        wardrobeFamily: `wardrobe-${laneIndex}-${offset}`,
        setting: `setting-${laneIndex}-${offset}`,
        action: `action-${laneIndex}-${offset}`,
        sceneMode: ordinal <= 40 ? "action-reaction" : "quiet-posed",
        composition: `composition-${laneIndex}-${offset}`,
        camera: `camera-${laneIndex}-${offset}`,
        lighting: `lighting-${laneIndex}-${offset}`,
        cast: ordinal <= 35 ? "solo" : ordinal <= 45 ? "viewer-pov" : "group",
        dominantColor: `color-${laneIndex}-${offset}`,
        textureFocus: ordinal <= 10,
        textureType: ordinal <= 10 ? `texture-${ordinal}` : "none",
        subculture: lane === "subculture-wildcard",
        prompt: `Independent Akari request ${ordinal}`,
        references: [
          {
            path: "references/akari-v1.5-b3-body-balance.png",
            role: "v1.5 identity and body balance",
            exclusions: ["outfit", "pose", "background"],
            sha256: "a".repeat(64),
          },
          {
            path: "references/akari-v1.4-g2-balanced-lines.png",
            role: "rendering and skin authority",
            exclusions: ["body balance", "pose", "background"],
            sha256: "b".repeat(64),
          },
        ],
        generation: {
          toolMode: "built-in-imagegen",
          generationId: null,
          requestId: null,
          sourcePath: null,
          technicalStatus: "pending",
          failureReason: null,
        },
        artifact: {
          imagePath: `batches/B001/images/image-${ordinal}.png`,
          thumbnailPath: `batches/B001/thumbs/image-${ordinal}.webp`,
          sha256: null,
          width: null,
          height: null,
        },
      };
    }),
  );
  return {
    schemaVersion: 1,
    batchType: "production",
    batchId: "B001",
    title: "Akari v1.5 Kawaii 1000 B001",
    entries,
    ...overrides,
  };
}

export async function createDemoFixture(
  dataRoot,
  { batchId = "B001" } = {},
) {
  const manifest = makeValidManifest();
  const batchDir = join(dataRoot, "batches", batchId);
  const referencePaths = [
    "references/akari-v1.5-b3-body-balance.png",
    "references/akari-v1.4-g2-balanced-lines.png",
  ];
  const referenceHash = createHash("sha256")
    .update(ONE_PIXEL_PNG)
    .digest("hex");

  manifest.batchId = batchId;
  manifest.title = `Akari v1.5 Kawaii 1000 ${batchId}`;
  for (const [index, entry] of manifest.entries.entries()) {
    const ordinal = index + 1;
    entry.id = `${batchId}-${String(ordinal).padStart(3, "0")}`;
    entry.artifact.imagePath =
      `batches/${batchId}/images/image-${ordinal}.png`;
    entry.artifact.thumbnailPath =
      `batches/${batchId}/thumbs/image-${ordinal}.webp`;
    if (batchId === "B000") entry.generation.toolMode = "demo";
    for (const reference of entry.references) {
      reference.sha256 = referenceHash;
    }
  }

  await mkdir(join(batchDir, "images"), { recursive: true });
  await mkdir(join(batchDir, "thumbs"), { recursive: true });
  await mkdir(join(dataRoot, "references"), { recursive: true });
  await Promise.all([
    ...referencePaths.map((path) =>
      writeFile(join(dataRoot, path), ONE_PIXEL_PNG)
    ),
    ...manifest.entries.flatMap((entry) => [
      writeFile(join(dataRoot, entry.artifact.imagePath), ONE_PIXEL_PNG),
      writeFile(join(dataRoot, entry.artifact.thumbnailPath), ONE_PIXEL_WEBP),
    ]),
  ]);
  await writeFile(
    join(batchDir, "manifest.json"),
    `${JSON.stringify(manifest, null, 2)}\n`,
    "utf8",
  );
  return { manifest, batchDir };
}
