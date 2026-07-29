import { LANES } from "./manifest.mjs";

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
