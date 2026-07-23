# Akari v1.2 Natural Form

Version: v1.2.0.

Status: Natural Form Core Release.

This is the canonical Akari v1.2 package. It preserves the v1.1 identity lock
and adds natural posture, weight balance, relaxed body state, morning state,
and daily micro-expressions.

Production order:

1. Phase 1: C01, C02, and both C03 views.
2. Phase 2: C04 and both C07 variants.
3. Phase 3: C05 and C06-1 through C06-4.
4. Phase 4: D01 validation.

The default settings release is:

- `akari-v1.2/release/akari-v1.2-core-settings.pdf`
- `akari-v1.2/release/checksums.txt`

Build and verify the complete release from the repository root:

```sh
npm run release:v1-2
```

Individual commands are also available:

```sh
npm run validate:v1-2
npm run build:v1-2:previews
npm run build:v1-2:pdf
npm run audit:v1-2:pdf
```

The previous face-hair, eight-view turnaround, motion, and overhead-room work
lives under `legacy/akari-v1.2-pre-natural-form/`. It is reference history,
not automatically accepted Natural Form material.

The previous settings PDF remains at `dist/akari-v1.1-settings.pdf` for
inheritance, comparison, history, and recovery.
