# Akari v2.1 Stability Probe r03 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and approve one deterministic neutral 30-degree structural
guide, then use it with Candidate C in exactly one noncanonical r03 generation
call and audit whether the selected eye language and level axes survive.

**Architecture:** Keep all guide tooling, measurements, prompt, provenance,
and generated evidence under the ignored `stability-r03` run. A small
dependency-free Node module projects a fixed 3D landmark scaffold with weak
perspective and emits separate clean and annotated SVGs; `rsvg-convert`
rasterizes them deterministically. Execution has a hard user checkpoint after
guide review: only the exact approved clean PNG may join Candidate C as the two
generation inputs, after which one call is preserved and reviewed without a
retry.

**Tech Stack:** Node.js ESM and `node:test`, SVG, `rsvg-convert`, ImageMagick,
built-in `image_gen`, local `view_image`, JSON measurement records, SHA-256,
`cmp`, Git ignore checks, and markdownlint-cli2.

## Global Constraints

- Follow
  `docs/superpowers/specs/2026-08-05-akari-v2-1-stability-probe-r03-design.md`.
- Execute in `/home/takahiro/workspace/akari-design`; do not create or switch
  to another worktree.
- The user's `OK承認` on 2026-08-05 approves the written r03 specification and
  this planning transition only. It is not approval of a guide that has not
  yet been shown.
- Candidate C at
  `tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png`, SHA-256
  `fadba782fcf2309063f86a992fdeaacece9a1d1f063adaf681343d60ce959c73`,
  is the sole identity and rendering authority.
- The clean guide at
  `tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.png`
  is the sole projection and placement authority only after the user approves
  that exact PNG and its SHA-256 is pinned.
- The guide uses a neutral parametric scaffold with yaw `30.0` degrees, roll
  `0.0` degrees, pitch `0.0` degrees, weak-perspective projection, and exact
  `1024x1536` PNG output.
- The clean guide contains only neutral-gray geometry on a plain light field.
  It contains no text, labels, measurements, color coding, hair, hairpin,
  ponytail, clothing detail, skin treatment, texture, shading, catchlights,
  decorative lashes, or recognizable character styling.
- Candidate C controls identity-bearing lid, nose, cheek, jaw, chin,
  expression, hair, palette, linework, and finish. The guide controls only
  yaw, axis direction, projected placement, near/far scale, occlusion, nose and
  jaw projection, neck, and shoulder placement.
- Candidate C's observed approximately `7`-to-`8`-degree facial incline is
  normalized rather than inherited. The guide and output target clean level
  axes for this bounded test.
- If the output cannot preserve both Candidate C's identity-bearing morphology
  and the guide's spatial construction, the affected gate fails; neither
  authority may silently override the other.
- Accepted v2.0 images are review-only. Rejected r01 and r02 probes are
  negative review evidence only. None of those four images may be passed to
  `image_gen` for r03.
- The accepted output yaw band is approximately `25` to `35` degrees. Near
  front, `45` degrees or deeper, profile, or incoherent face/neck/shoulder
  perspective fails Gate 3.
- Each output eye-center, brow-center, and mouth axis must differ from its
  corresponding approved-guide axis by no more than `3.0` degrees. There is no
  gray zone above that boundary; disputed evidence fails.
- Shoulder angle is qualitative corroboration only, not a numeric hard gate.
  Do not derive a separate numeric output head-axis gate from the facial axes or
  from the yaw-shifted nose-to-chin line.
- Record `W_far / W_near` and `H_far / H_near` only as diagnostics. The
  neighborhoods `0.75` to `0.88` and `0.85` to `1.00` never determine PASS or
  FAIL by themselves.
- Measure iris apparent diameter `D`, visible span `V`, and normalized exposure
  `E = V / D` separately. The farther iris must be no larger and no more
  exposed than the nearer iris.
- Record canvas coordinates and derived angles to one decimal degree. If stroke
  thickness, occlusion, crop, or independent placement disagreement can move a
  hard result across its boundary, fail the controlling gate.
- Define the outer canthus independently from any continuation. A connected
  soft Candidate-C-relative taper is allowed; a separate spur, hook, lash
  cluster, or eyeliner point fails.
- Build and revise the deterministic guide without `image_gen`. Stop after
  showing the exact clean and annotated guide PNGs. Do not continue until the
  user explicitly approves the exact guide.
- After guide approval, make exactly one built-in `image_gen` call with exactly
  Candidate C and the approved clean guide. Omit recent-conversation image
  injection and do not make a second call.
- Preserve the first returned PNG byte-for-byte. Do not retry, retouch, crop,
  resize, recompress, composite, or silently replace it.
- Keep every r03 runtime artifact under ignored
  `tmp/akari-v2.1-redesign/stability-r03/`; do not stage or commit it. The
  tracked plan and approved-spec status are the only durable changes from this
  planning checkpoint.
- Keep the existing r01/r02 plans, prompts, images, run ledgers, reviews, and
  `FAIL` verdicts byte-for-byte unchanged. Record new authorization only in the
  r03 ledger. The pinned combined digest of all files under `r01`,
  `stability-r01`, and `stability-r02` is
  `cae2a164d86c4c0e3b85e65c5e36911cc651a3bdf60c5e6e6cbd469508b9255b`.
- Preserve `tmp/akari-v2-uniform-batch/` byte-for-byte. Its pinned digest is
  `4ac76bd19c478edaf11cf122ed41a35e0658fdf796731d49dcddb323b11382cc`.
- Do not create r04, Stage 2 work, promotion, canonical assets, package,
  manifest, release, PDF, or v2.0 uniform-batch changes.

---

### Task 1: Pin the r03 authorization and preflight boundary

**Files:**

- Read:
  `docs/superpowers/specs/2026-08-05-akari-v2-1-stability-probe-r03-design.md`
- Read:
  `docs/superpowers/plans/2026-08-05-akari-v2-1-stability-probe-r03.md`
- Create: `tmp/akari-v2.1-redesign/stability-r03/RUN.md`

**Interfaces:**

- Consumes: the approved r03 design, the user's `OK承認`, immutable Candidate
  C, the historical r01/r02 failures, and the paused v2.0 batch digest.
- Produces: one r03 ledger whose state is `guide construction; generation
  blocked pending exact-guide approval`, consumed by Task 2.

- [ ] **Step 1: Verify the checkout, historical evidence, and immutable state**

Run serially:

```bash
test "$(pwd -P)" = "/home/takahiro/workspace/akari-design"
test -f \
  docs/superpowers/specs/2026-08-05-akari-v2-1-stability-probe-r03-design.md
test -f \
  docs/superpowers/plans/2026-08-05-akari-v2-1-stability-probe-r03.md
sha256sum \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png \
  tmp/akari-v2.1-redesign/stability-r01/images/akari-v2.1-stability-30-r01.png \
  tmp/akari-v2.1-redesign/stability-r02/images/akari-v2.1-stability-30-r02.png \
  tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png \
  tmp/akari-v2.1-redesign/stability-r01/images/akari-v2.1-stability-30-r01.png \
  tmp/akari-v2.1-redesign/stability-r02/images/akari-v2.1-stability-30-r02.png
find \
  tmp/akari-v2.1-redesign/r01 \
  tmp/akari-v2.1-redesign/stability-r01 \
  tmp/akari-v2.1-redesign/stability-r02 \
  -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum
find tmp/akari-v2-uniform-batch -type f -print0 | sort -z | \
  xargs -0 sha256sum | sha256sum
command -v rsvg-convert
rsvg-convert --version
command -v magick
command -v identify
command -v sha256sum
command -v xxd
command -v cmp
command -v jq
bash -lc 'command -v node; node --version; command -v npm; npm --version'
git status --short --branch
git diff --quiet
git diff --cached --quiet
```

Expected: Candidate C matches the pinned hash; the combined historical digest
is `cae2a164d86c4c0e3b85e65c5e36911cc651a3bdf60c5e6e6cbd469508b9255b`;
all three PNGs are readable; the batch digest is the pinned digest; every tool
resolves; tracked and staged trees are clean after this plan commit; and the
pre-existing user-owned untracked v2.0 uniform-batch plan remains untouched.

- [ ] **Step 2: Preserve r01/r02 history and record the new boundary in r03**

Do not edit the existing r01/r02 plans, prompts, images, ledgers, or reviews.
Carry all of these facts into the new r03 ledger created in Step 3:

- r01 and r02 retain their historical `FAIL` verdicts; r02 failed Gates 2 and
  3;
- the user approved the new written r03 specification with `OK承認` on
  2026-08-05;
- r03 changes the generation architecture to Candidate C plus one separately
  approved neutral guide;
- v2.0 images move to review-only roles, while r01/r02 remain negative evidence
  only;
- guide construction is authorized, but image generation remains blocked until
  the exact clean guide PNG is shown and explicitly approved;
- no r04, Stage 2, promotion, package, manifest, release, or PDF is authorized.

- [ ] **Step 3: Create the r03 directory and preflight ledger**

Run:

```bash
mkdir -p \
  tmp/akari-v2.1-redesign/stability-r03/guides \
  tmp/akari-v2.1-redesign/stability-r03/measurements \
  tmp/akari-v2.1-redesign/stability-r03/approvals \
  tmp/akari-v2.1-redesign/stability-r03/prompts \
  tmp/akari-v2.1-redesign/stability-r03/images
```

Use `apply_patch` to create `RUN.md` with:

- status `guide construction; generation blocked pending exact-guide approval`;
- approved design and implementation-plan paths;
- literal user approval `OK承認` and date `2026-08-05`;
- Candidate C path, sole identity/rendering role, dimensions, and hash;
- clean guide target path and sole projection/placement role;
- all four review-only image paths and their restricted roles;
- yaw, roll, pitch, projection type, canvas size, and near-side convention;
- guide-review checkpoint, one-call limit, and every non-goal;
- preserved v2.0 batch digest;
- pinned combined r01/r02 historical digest;
- recovery-helper path and preflight hash; a later recovery may use only those
  unchanged helper bytes.

- [ ] **Step 4: Validate the preflight records**

Run:

```bash
bash -lc './node_modules/.bin/markdownlint-cli2 \
  :tmp/akari-v2.1-redesign/stability-r03/RUN.md \
  --no-globs'
git check-ignore -v \
  tmp/akari-v2.1-redesign/stability-r03/RUN.md \
  tmp/akari-v2.1-redesign/stability-r03/guides \
  tmp/akari-v2.1-redesign/stability-r03/measurements
```

Expected: the r03 ledger lints with zero issues and all r03 working paths are
ignored. Recorded preflight hashes confirm that no r01/r02 file changed.

### Task 2: Construct, audit, and show the neutral structural guide

**Files:**

- Create:
  `tmp/akari-v2.1-redesign/stability-r03/guides/build-structure-guide.test.mjs`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/guides/build-structure-guide.mjs`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.svg`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure-review.svg`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-landmarks.json`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.png`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure-review.png`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/measurements/measure-landmarks.test.mjs`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/measurements/measure-landmarks.mjs`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/measurements/candidate-c-lid-placement-1.json`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/measurements/candidate-c-lid-placement-2.json`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/measurements/candidate-c-lid-summary.json`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/measurements/guide-placement-1.json`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/measurements/guide-placement-2.json`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/measurements/guide-summary.json`
- Modify: `tmp/akari-v2.1-redesign/stability-r03/RUN.md`

**Interfaces:**

- Consumes: the Task 1 ledger, Candidate C's approved lid-language contract,
  and the deterministic projection constants below.
- Produces: one exact clean guide PNG, one annotated review PNG, source SVGs,
  projected coordinates, measurements, hashes, and a user-facing guide review.
  Task 3 may consume them only after explicit user approval.

- [ ] **Step 1: Write the failing guide-contract tests**

Use `apply_patch` to create `build-structure-guide.test.mjs` with these tests:

```javascript
import assert from "node:assert/strict";
import test from "node:test";
import {
  CONTRACT,
  buildArtifacts,
  projectPoint,
  rotatePoint,
} from "./build-structure-guide.mjs";

test("pins the approved weak-perspective pose and canvas", () => {
  assert.deepEqual(CONTRACT.canvas, { width: 1024, height: 1536 });
  assert.deepEqual(CONTRACT.rotationDeg, { yaw: 30, roll: 0, pitch: 0 });
  assert.equal(CONTRACT.projection, "weak-perspective");
  assert.equal(CONTRACT.nearSide, "character-left / canvas-right");
});

test("projects the head axis vertically and facial axes horizontally", () => {
  const { record } = buildArtifacts();
  assert.ok(Math.abs(Math.abs(record.metrics.axisAnglesDeg.head) - 90) < 1e-9);
  for (const name of ["eyes", "brows", "mouth"]) {
    assert.ok(Math.abs(record.metrics.axisAnglesDeg[name]) < 1e-9, name);
  }
});

test("puts the character-left near side on canvas-right", () => {
  const { record } = buildArtifacts();
  assert.ok(
    record.projected.nearEyeOuter.x > record.projected.farEyeOuter.x,
  );
  assert.ok(record.projected.visibleEar.x > record.projected.noseTip.x);
});

test("constructs the far eye as narrower with no larger iris exposure", () => {
  const { record } = buildArtifacts();
  assert.ok(record.metrics.eyeWidthPx.far < record.metrics.eyeWidthPx.near);
  assert.ok(record.metrics.eyeHeightPx.far <= record.metrics.eyeHeightPx.near);
  assert.ok(record.metrics.irisDiameterPx.far <= record.metrics.irisDiameterPx.near);
  assert.ok(record.metrics.irisExposure.far <= record.metrics.irisExposure.near);
  assert.equal(record.metrics.nearContinuationPx, 0);
});

test("keeps the generation guide neutral and annotation-free", () => {
  const { cleanSvg, reviewSvg } = buildArtifacts();
  assert.equal(cleanSvg.includes("<text"), false);
  assert.equal(cleanSvg.includes("#2563eb"), false);
  assert.equal(cleanSvg.includes("#dc2626"), false);
  assert.equal(cleanSvg.includes("<image"), false);
  assert.equal(cleanSvg.includes("<foreignObject"), false);
  assert.equal(cleanSvg.includes("<script"), false);
  assert.equal(cleanSvg.includes("href="), false);
  assert.equal(cleanSvg.includes("hair"), false);
  assert.equal(cleanSvg.includes("catchlight"), false);
  assert.equal(reviewSvg.includes("<text"), true);
});

test("projects a source point without roll, pitch, or perspective scaling", () => {
  assert.deepEqual(rotatePoint([0, 0, 0], CONTRACT.rotationDeg), [0, 0, 0]);
  assert.deepEqual(
    projectPoint([0, 0, 0], CONTRACT),
    { x: 512, y: 610 },
  );
});
```

- [ ] **Step 2: Run the guide tests to verify RED**

Run:

```bash
bash -lc 'node --test \
  tmp/akari-v2.1-redesign/stability-r03/guides/build-structure-guide.test.mjs'
```

Expected: FAIL with `ERR_MODULE_NOT_FOUND` for
`build-structure-guide.mjs`.

- [ ] **Step 3: Implement the fixed projection model and SVG emitters**

Use `apply_patch` to create `build-structure-guide.mjs`. Export exactly
`CONTRACT`, `MODEL`, `rotatePoint`, `projectPoint`, `buildArtifacts`, and
`writeArtifacts`. Use these constants and source landmarks:

```javascript
export const CONTRACT = Object.freeze({
  canvas: { width: 1024, height: 1536 },
  origin: { x: 512, y: 610 },
  scale: 500,
  rotationDeg: { yaw: 30, roll: 0, pitch: 0 },
  projection: "weak-perspective",
  nearSide: "character-left / canvas-right",
});

export const MODEL = Object.freeze({
  landmarks: {
    crown: [0.00, 0.92, 0.14],
    headAxisTop: [0.00, 0.82, 0.14],
    headAxisBottom: [0.00, -0.70, 0.14],
    farTemple: [-0.78, 0.45, 0.14],
    farCheek: [-0.64, -0.08, 0.23],
    farJaw: [-0.43, -0.57, 0.27],
    chin: [0.00, -0.82, 0.27],
    nearJaw: [0.50, -0.54, 0.25],
    nearCheek: [0.70, -0.06, 0.19],
    nearTemple: [0.78, 0.45, 0.14],
    farEyeOuter: [-0.55, 0.17, 0.33],
    farEyeInner: [-0.18, 0.17, 0.40],
    nearEyeInner: [0.18, 0.17, 0.40],
    nearEyeOuter: [0.55, 0.17, 0.33],
    farBrowCenter: [-0.36, 0.39, 0.36],
    nearBrowCenter: [0.36, 0.39, 0.36],
    noseBridge: [0.00, 0.22, 0.43],
    noseTip: [0.00, -0.08, 0.55],
    farMouthCorner: [-0.22, -0.33, 0.43],
    nearMouthCorner: [0.22, -0.33, 0.43],
    visibleEar: [0.78, 0.03, 0.08],
    farNeck: [-0.25, -0.90, 0.12],
    nearNeck: [0.30, -0.90, 0.12],
    farAcromion: [-0.74, -1.18, 0.05],
    nearAcromion: [0.82, -1.18, 0.05],
  },
  eyes: {
    far: { upperRise: 0.045, lowerDrop: 0.045, irisDiameter: 0.108,
      visibleSpan: 0.084 },
    near: { upperRise: 0.052, lowerDrop: 0.052, irisDiameter: 0.120,
      visibleSpan: 0.104 },
  },
});

export function rotatePoint([x, y, z], rotationDeg) {
  const yaw = rotationDeg.yaw * Math.PI / 180;
  const pitch = rotationDeg.pitch * Math.PI / 180;
  const roll = rotationDeg.roll * Math.PI / 180;
  const x1 = x * Math.cos(yaw) - z * Math.sin(yaw);
  const z1 = x * Math.sin(yaw) + z * Math.cos(yaw);
  const y2 = y * Math.cos(pitch) - z1 * Math.sin(pitch);
  const z2 = y * Math.sin(pitch) + z1 * Math.cos(pitch);
  const x3 = x1 * Math.cos(roll) - y2 * Math.sin(roll);
  const y3 = x1 * Math.sin(roll) + y2 * Math.cos(roll);
  return [x3, y3, z2];
}

export function projectPoint(point, contract = CONTRACT) {
  const [x, y] = rotatePoint(point, contract.rotationDeg);
  return {
    x: contract.origin.x + contract.scale * x,
    y: contract.origin.y - contract.scale * y,
  };
}
```

Implement the remaining exports with these exact responsibilities:

- `buildArtifacts()` projects every source landmark and returns
  `{ cleanSvg, reviewSvg, record }` without writing files;
- `record` contains `schemaVersion: 1`, the complete source model, projection
  formula and rotation order `yaw -> pitch -> roll`, projected pixel
  coordinates, and all derived metrics;
- compute widths as Euclidean canthus distance, heights perpendicular to each
  canthus chord, centers as chord midpoints, axes with `atan2`, iris exposure
  as `V / D`, and diagnostic ratios from the projected values;
- compute each height by sampling its upper and lower cubic at the same chord
  parameter in `0.01` increments and taking the maximum perpendicular
  upper-to-lower separation; never subtract unrelated global extrema;
- keep the head axis vertical by joining the projected `headAxisTop` and
  `headAxisBottom`; keep eye, brow, mouth, and shoulder endpoint pairs at their
  shared model `y` values;
- draw the head and jaw as one neutral outline through crown, temples, cheeks,
  jaws, and chin; add only the face centerline, nose, visible ear, neck,
  shoulders, brows, mouth, eye apertures, clipped iris ellipses, canthus dots,
  and construction axes;
- use a low cubic upper lid and quiet cubic lower lid for each eye; both paths
  end exactly at the anatomical canthi, so the guide continuation length is
  `0`;
- use only `#f7f7f4`, `#5f6368`, `#8a8f94`, and `#c9cccf` in `cleanSvg`, with
  no `<text>`, `<image>`, `<foreignObject>`, `<script>`, external resource,
  metadata label, or character feature;
- make `reviewSvg` a separate annotated derivative with projected landmark
  dots, axes, yaw/roll/pitch, coordinates, axis angles, width/height ratios,
  iris diameter/exposure, and canthus-continuation metrics. Review-only colors
  `#2563eb` and `#dc2626` are allowed there;
- `writeArtifacts(outputDirectory)` writes the two SVGs and landmark JSON with
  the exact filenames in the Files block, using a stable trailing newline and
  two-space JSON indentation;
- the main entry point accepts one output-directory argument and refuses to
  overwrite a non-identical existing file by default;
- an explicit `--replace-unapproved --archive-id guide-rNN` mode may replace
  Task 2 artifacts only when `approvals/guide-approval.json` does not exist and
  `RUN.md` records that the displayed guide was rejected. Before changing a
  byte, copy the existing clean/review SVGs, clean/review PNGs, and landmark JSON
  with no-clobber semantics into `guides/rejected/<archive-id>/`, then write a
  stable JSON hash manifest there. Refuse an existing archive ID or incomplete
  archive. Once approval exists, no generator mode may alter canonical guide
  bytes.

Use a sampled cubic helper for the upper-lid central-50-percent rise metric.
The sampler must inspect `t = 0.25` through `t = 0.75` in increments of `0.01`
and measure perpendicular distance from the canthus chord, rather than treating
the control-point height as the observed rise.

- [ ] **Step 4: Run the guide tests to verify GREEN**

Run:

```bash
bash -lc 'node --test \
  tmp/akari-v2.1-redesign/stability-r03/guides/build-structure-guide.test.mjs'
```

Expected: six tests pass and zero fail.

- [ ] **Step 5: Write and test the independent-measurement helper**

Use `apply_patch` to create `measure-landmarks.test.mjs` first. Test exact
horizontal, axial wraparound (`89` versus `-89` is `2` degrees), inclusive
`3.000`-degree PASS and `3.001`-degree FAIL fixtures, Euclidean width,
same-parameter interpolated perpendicular eye height, `E = V / D`, tangent-
projected continuation length, continuation uncertainty, and the rule that two
placements straddling the hard boundary produce `disputed: true`. Add one
fixture whose width and height ratios fall outside the diagnostic neighborhoods
while all hard predicates remain unchanged. Run it once and expect
`ERR_MODULE_NOT_FOUND`.

Then create `measure-landmarks.mjs` with these exports and core calculations:

```javascript
import { spawnSync } from "node:child_process";

export function distance(a, b) {
  return Math.hypot(b[0] - a[0], b[1] - a[1]);
}

export function axisAngleDeg(a, b) {
  return Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI;
}

export function axialAngleDeltaDeg(aDeg, bDeg) {
  const wrapped = ((aDeg - bDeg + 90) % 180 + 180) % 180 - 90;
  return Math.abs(wrapped);
}

export function perpendicularAperture(
  canthusA,
  canthusB,
  upperLidSamples,
  lowerLidSamples,
) {
  const width = distance(canthusA, canthusB);
  const tangent = [
    (canthusB[0] - canthusA[0]) / width,
    (canthusB[1] - canthusA[1]) / width,
  ];
  const normal = [
    -tangent[1],
    tangent[0],
  ];
  const project = (points) => points.map(([x, y]) => ({
    t: ((x - canthusA[0]) * tangent[0] +
      (y - canthusA[1]) * tangent[1]) / width,
    v: (x - canthusA[0]) * normal[0] +
      (y - canthusA[1]) * normal[1],
  })).sort((a, b) => a.t - b.t);
  const interpolate = (samples, t) => {
    const rightIndex = samples.findIndex((sample) => sample.t >= t);
    if (rightIndex === -1) return samples.at(-1).v;
    if (rightIndex === 0) return samples[0].v;
    const left = samples[rightIndex - 1];
    const right = samples[rightIndex];
    const mix = (t - left.t) / (right.t - left.t);
    return left.v + (right.v - left.v) * mix;
  };
  const upper = project(upperLidSamples);
  const lower = project(lowerLidSamples);
  let maximum = 0;
  for (let index = 0; index <= 100; index += 1) {
    const t = index / 100;
    maximum = Math.max(
      maximum,
      Math.abs(interpolate(upper, t) - interpolate(lower, t)),
    );
  }
  return maximum;
}

export function continuationLength(eye) {
  const anchor = eye.outerTangentAnchor;
  const canthus = eye.outerCanthus;
  const end = eye.continuationEnd;
  const tangentLength = distance(anchor, canthus);
  const tangent = [
    (canthus[0] - anchor[0]) / tangentLength,
    (canthus[1] - anchor[1]) / tangentLength,
  ];
  return Math.max(
    0,
    (end[0] - canthus[0]) * tangent[0] +
      (end[1] - canthus[1]) * tangent[1],
  );
}

export function continuationUncertainty(candidate, subject) {
  return Math.max(
    2 / Math.min(...candidate.widthsNear, ...subject.widthsNear),
    Math.abs(candidate.ratios[0] - candidate.ratios[1]),
    Math.abs(subject.ratios[0] - subject.ratios[1]),
  );
}

export function normalizedTransform(subjectPlacement, guidePlacement) {
  const subjectDerived = subjectPlacement.derived ??
    summarizePlacement(subjectPlacement);
  const guideDerived = guidePlacement.derived ??
    summarizePlacement(guidePlacement);
  const sourceHeight = distance(
    subjectPlacement.landmarks.crown,
    subjectPlacement.landmarks.chin,
  );
  const guideHeight = distance(
    guidePlacement.landmarks.crown,
    guidePlacement.landmarks.chin,
  );
  const midpoint = (left, right) => [
    (left[0] + right[0]) / 2,
    (left[1] + right[1]) / 2,
  ];
  const sourceEyes = midpoint(
    subjectDerived.eyeCenters.far,
    subjectDerived.eyeCenters.near,
  );
  const guideEyes = midpoint(
    guideDerived.eyeCenters.far,
    guideDerived.eyeCenters.near,
  );
  const scale = guideHeight / sourceHeight;
  return {
    scale,
    translateX: guideEyes[0] - sourceEyes[0] * scale,
    translateY: guideEyes[1] - sourceEyes[1] * scale,
  };
}

export function renderNormalizedOverlay(options) {
  const transform = normalizedTransform(options.subject, options.guide);
  const percent = `${(transform.scale * 100).toFixed(6)}%`;
  const rasterX = Math.round(transform.translateX);
  const rasterY = Math.round(transform.translateY);
  const geometry = `${rasterX >= 0 ? "+" : ""}${rasterX}${
    rasterY >= 0 ? "+" : ""}${rasterY}`;
  const args = [
    "-size", "1024x1536", "canvas:none",
    "(", options.sourcePath, "-resize", percent, ")",
    "-geometry", geometry, "-composite",
    "(", options.guideReviewPath, "-alpha", "set", "-channel", "A",
    "-evaluate", "multiply", "0.55", "+channel", ")",
    "-composite", options.outputPath,
  ];
  const result = spawnSync("magick", args, { encoding: "utf8" });
  if (result.status !== 0) throw new Error(result.stderr || "magick failed");
  return { ...transform, rasterX, rasterY, args };
}
```

Use this normative JSON shape for every placement file. `Point2` values are
finite canvas-pixel numbers. Candidate C uses `scope: "lid-baseline"` and may
set full-review-only fields to `null`; guide and output use `scope: "full"` and
must supply every review field except for the output-only `headAxis` exception
defined below:

```typescript
type Point2 = [number, number];
type EyeLandmarks = {
  innerCanthus: Point2;
  outerCanthus: Point2;
  upperLidPolyline: Point2[];
  lowerLidPolyline: Point2[];
  irisEllipse: {
    center: Point2;
    rx: number;
    ry: number;
    rotationDeg: number;
  };
  irisVisibleTop: Point2;
  irisVisibleBottom: Point2;
  outerTangentAnchor: Point2;
  continuationEnd: Point2;
};
type MeasurementPass = {
  schemaVersion: 1;
  subject: "candidate-c" | "guide" | "output";
  scope: "lid-baseline" | "full";
  pass: 1 | 2;
  image: {
    path: string;
    sha256: string;
    width: number;
    height: number;
  };
  independence: {
    firstAnnotationsHidden: boolean;
  };
  landmarks: {
    crown: Point2 | null;
    chin: Point2 | null;
    headAxis: { top: Point2; bottom: Point2 } | null;
    eyes: { near: EyeLandmarks; far: EyeLandmarks | null };
    brows: { nearArc: Point2[]; farArc: Point2[] } | null;
    mouthCorners: { near: Point2; far: Point2 } | null;
    acromia: { near: Point2; far: Point2 } | null;
    noseTip: Point2 | null;
    earCenter: Point2 | null;
    cheekAnchors: { near: Point2; far: Point2 } | null;
    pitch: {
      crownPlane: [Point2, Point2];
      nostrilVisibility: "none" | "slight" | "clear";
      underChinVisibility: "none" | "slight" | "clear";
    } | null;
  };
};
```

Export `validatePlacement(value)`. It rejects non-finite or off-canvas points,
hashes other than 64 lowercase hexadecimal characters, polyline arrays shorter
than four points, nonpositive iris radii, a pass-2 record without
`firstAnnotationsHidden: true`, a Candidate C record outside
`scope: "lid-baseline"`, coincident inner/outer canthi, or a coincident
`outerTangentAnchor`/outer-canthus pair. A guide record with `scope: "full"`
must supply `headAxis`; an output record with `scope: "full"` must set
`headAxis: null` because r03 has no numeric output head-axis gate. Every other
field required by `scope: "full"` must be non-null. Both upper and lower lid
polylines must begin and end at the same two anatomical canthi. Determine each
outer canthus from the fitted upper/lower centerline junction before placing
`outerTangentAnchor` or `continuationEnd`.
Enforce the complete subject/scope mapping: `candidate-c` requires
`lid-baseline`; `guide` requires `full` with a non-null `headAxis`; and `output`
requires `full` with `headAxis: null`. No subject may use another subject's
scope or head-axis convention.
Add negative tests for coincident canthi and for a zero-length
outer-tangent-anchor/canthus vector, every invalid subject/scope/head-axis
combination, reversed or duplicate pass order, mismatched pair subjects, and
mismatched pair image path/hash/dimensions so none can reach the measurement
math.

Add `polylineArcMidpoint(points)` using cumulative Euclidean arc length, then
complete `summarizePlacement(placement)`,
`comparePlacements(first, second, referencePlacements, candidateBaseline)`, and
`candidateContinuationBaseline(first, second)` from the exact landmark schema
used in Steps 7 and 8. `summarizePlacement` returns eye centers, arc-length brow
centers, eye/brow/mouth/shoulder axes, `W`, perpendicular `H`, central-50-percent
lid rise, fitted iris vertical diameter `D`, visible `V` projected onto the
fitted ellipse's apparent vertical-axis unit vector, `E = V / D`, tangent-
projected continuation `L`, and `L / W_near`. `comparePlacements` evaluates
every subject/reference combination and returns the structure below.

`comparePlacements` must return both raw summaries plus:

```typescript
{
  axisBoundaryDeg: 3.0,
  axisDeltasDeg: {
    eyes: number[][],
    brows: number[][],
    mouth: number[][],
  },
  allAxesWithinBoundary: boolean,
  straddlesBoundary: boolean,
  disputed: boolean,
  diagnosticRanges: {
    widthRatio: [number, number],
    heightRatio: [number, number],
  },
  continuation: {
    candidateBaselineMean: number,
    subjectMean: number,
    uncertainty: number,
    withinCandidateBoundary: boolean,
  },
}
```

Treat line axes modulo `180` degrees. Do not average two placements into a PASS.
Both eye, brow, and mouth deltas must independently remain within `3.0` degrees,
and any boundary straddle sets `disputed: true`. Define continuation uncertainty
as the greatest of `2 / minimum observed W_near`, the Candidate C placement
spread, and the guide or output placement spread. Diagnostic width and height
ratios must never be read by a hard PASS/FAIL predicate.

For a two-placement subject and two-placement guide, each axis matrix row is one
subject pass and each column is one guide pass. Preserve all four raw deltas to
one decimal degree; do not collapse them into only a maximum or boolean.

`normalizedTransform` returns only `scale`, `translateX`, and `translateY`, with
no rotation, skew, or warp field. `renderNormalizedOverlay` must invoke
ImageMagick with an argument array rather than a shell string: uniformly resize
the subject by `scale`, place it on a transparent `1024x1536` canvas at the
computed translation, then composite the annotated guide at `55` percent
opacity. Add tests that fail if the argument array contains `-rotate`,
`-distort`, `-affine`, `-shear`, or nonuniform resize.
Also assert that raster translation rounds each computed offset by no more than
`0.5` canvas pixel and record both floating and raster offsets.

The CLI entry point supports these exact subcommands and refuses to overwrite
an existing output:

```text
candidate-baseline --first PATH --second PATH --output PATH
compare --first PATH --second PATH (--reference PATH --reference PATH --guide-approval PATH | --reference-record PATH) --candidate-baseline PATH --output PATH
overlay --placement PATH --guide-placement PATH --source PATH --guide-review PATH --output PATH
```

`candidate-baseline` validates both input placements and writes the two widths,
two tangent-projected lengths, two ratios, spread, two-pixel term, and baseline
uncertainty. `compare` validates both subject placements and one or two
references, writes both raw summaries and the complete result structure above,
uses the Candidate C baseline to record continuation uncertainty and comparison,
and never reads diagnostic ratios in a hard predicate. `--reference-record`
adapts the deterministic generator's projected coordinates and derived metrics
to one reference summary; it is mutually exclusive with `--reference`.
Every `--first`/`--second` pair must be pass `1` then pass `2`, use the same
subject, and identify the same inspected image by path, SHA-256, width, and
height. A two-file `--reference` pair must additionally be `guide`/`full`, use
pass `1` then pass `2`, and identify the same approved-guide image.
`--guide-approval` is required with two-file `--reference` mode and forbidden
with `--reference-record`; validate each reference's image path, SHA-256,
width, and height against `approval.guide` in that exact approval JSON. Add a
negative test where both reference placements match each other but do not
match the approved guide. Reject a single `--reference`, more than two
references, a missing/misplaced approval option, or any pair invariant failure.

Run:

```bash
bash -lc 'node --test \
  tmp/akari-v2.1-redesign/stability-r03/measurements/measure-landmarks.test.mjs'
```

Expected: all measurement-helper tests pass and zero fail.

- [ ] **Step 6: Build and rasterize the guide twice**

Run:

```bash
bash -lc 'node \
  tmp/akari-v2.1-redesign/stability-r03/guides/build-structure-guide.mjs \
  tmp/akari-v2.1-redesign/stability-r03/guides'
rsvg-convert --format=png --width=1024 --height=1536 \
  --output=tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.png \
  tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.svg
rsvg-convert --format=png --width=1024 --height=1536 \
  --output=tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure-review.png \
  tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure-review.svg
r03_check_dir="$(mktemp -d /tmp/akari-r03-guide-check.XXXXXX)"
bash -lc "node \
  tmp/akari-v2.1-redesign/stability-r03/guides/build-structure-guide.mjs \
  '$r03_check_dir'"
rsvg-convert --format=png --width=1024 --height=1536 \
  --output="$r03_check_dir/akari-v2.1-stability-30-r03-structure.png" \
  "$r03_check_dir/akari-v2.1-stability-30-r03-structure.svg"
rsvg-convert --format=png --width=1024 --height=1536 \
  --output="$r03_check_dir/akari-v2.1-stability-30-r03-structure-review.png" \
  "$r03_check_dir/akari-v2.1-stability-30-r03-structure-review.svg"
cmp --silent \
  tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.svg \
  "$r03_check_dir/akari-v2.1-stability-30-r03-structure.svg"
cmp --silent \
  tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-landmarks.json \
  "$r03_check_dir/akari-v2.1-stability-30-r03-landmarks.json"
cmp --silent \
  tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.png \
  "$r03_check_dir/akari-v2.1-stability-30-r03-structure.png"
cmp --silent \
  tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure-review.png \
  "$r03_check_dir/akari-v2.1-stability-30-r03-structure-review.png"
```

Expected: both builds are byte-identical. Leave the temporary comparison
directory in `/tmp`; do not use a destructive cleanup command.

- [ ] **Step 7: Measure Candidate C's connected outer-lid taper twice**

Open Candidate C at original detail. In the first pass, place the near eye's
inner canthus, anatomical outer canthus, upper/lower lid samples, fitted iris,
outer tangent anchor, and continuation endpoint using stroke centers. Save a
valid `MeasurementPass` with `subject: "candidate-c"`,
`scope: "lid-baseline"`, and `pass: 1` as
`candidate-c-lid-placement-1.json`.

Hide the first annotations and do not read the first coordinate file during
the second pass. Repeat from the clean Candidate C image and save
`candidate-c-lid-placement-2.json`. A fresh reviewer agent may perform the
second placement. Run the measurement helper to write
`candidate-c-lid-summary.json`, containing both `W_near`, both `L`, both
`L / W_near`, their spread, `2 / W_near`, and the controlling uncertainty.

Run:

```bash
bash -lc 'node \
  tmp/akari-v2.1-redesign/stability-r03/measurements/measure-landmarks.mjs \
  candidate-baseline \
  --first tmp/akari-v2.1-redesign/stability-r03/measurements/candidate-c-lid-placement-1.json \
  --second tmp/akari-v2.1-redesign/stability-r03/measurements/candidate-c-lid-placement-2.json \
  --output tmp/akari-v2.1-redesign/stability-r03/measurements/candidate-c-lid-summary.json'
```

Compute `L` as
`max(0, dot(continuationEnd - outerCanthus,
unit(outerCanthus - outerTangentAnchor)))`. Do not substitute Euclidean stroke
length or include the anatomical lid segment before the canthus.

Expected: the guide's `L / W_near = 0` does not exceed Candidate C's baseline
plus uncertainty. If the anatomical outer canthus cannot be placed independently
from the decorative continuation in either pass, the guide evidence is
disputed and this task stops before user approval.

- [ ] **Step 8: Measure the clean guide twice independently**

Using the clean PNG rather than the annotated review view, record two complete
guide placements with the same stroke-center landmark schema later required for
the output: head-axis endpoints, four canthi, lid samples, brow arcs, mouth
corners, acromia, crown, chin, nose, ear, cheeks, iris ellipse and visible span,
and near continuation endpoint. Finish placement 1, hide it, and do not inspect
its annotations, coordinate file, or the generator landmark JSON while making
placement 2. The two files must use `subject: "guide"`, `scope: "full"`, and
`pass: 1` or `pass: 2` respectively, with a non-null `headAxis`.

Run `comparePlacements` against the generator landmark record and write
`guide-summary.json`. For eye, brow, and mouth axes, evaluate every human
placement against the projected guide axis with axial angle differences modulo
`180` degrees. Both passes must satisfy the inclusive `3.0`-degree tolerance;
any boundary straddle or landmark dispute fails the guide audit. Record the
width/height ratios as diagnostics only, and confirm both passes independently
measure the farther iris as no larger and no more exposed than the nearer iris.

Run:

```bash
bash -lc 'node \
  tmp/akari-v2.1-redesign/stability-r03/measurements/measure-landmarks.mjs \
  compare \
  --first tmp/akari-v2.1-redesign/stability-r03/measurements/guide-placement-1.json \
  --second tmp/akari-v2.1-redesign/stability-r03/measurements/guide-placement-2.json \
  --reference-record tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-landmarks.json \
  --candidate-baseline tmp/akari-v2.1-redesign/stability-r03/measurements/candidate-c-lid-summary.json \
  --output tmp/akari-v2.1-redesign/stability-r03/measurements/guide-summary.json'
```

- [ ] **Step 9: Audit the guide and record its exact evidence**

Use `view_image(detail=original)` on Candidate C, the clean guide, and the
annotated review PNG. Open the v2.0 face and full-body images only as review
cross-checks; do not treat them as guide sources. Confirm and record:

1. vertical head axis and level eye, brow, and mouth axes;
2. low central farther upper lid rather than a dome;
3. farther iris no larger and no more exposed than the nearer iris;
4. near upper lid ends softly at the anatomical outer canthus with no separate
   extension;
5. compact soft jaw and chin;
6. unambiguous 30-degree character-left orientation with near side on
   canvas-right;
7. neutral appearance with no identity, hair, outfit, color, text, or style
   leakage in the clean PNG.

Run:

```bash
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.png \
  tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure-review.png
xxd -p -l 8 \
  tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.png
sha256sum \
  tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.svg \
  tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.png \
  tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure-review.png \
  tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-landmarks.json
```

Expected: both PNGs are exactly `1024x1536`, the clean PNG signature is
`89504e470d0a1a0a`, and every hash is recorded in `RUN.md` with the source
method, coordinates, metrics, two Candidate C placements, two clean-guide
placements, their uncertainty, and seven checks.

- [ ] **Step 10: Show both guide views and enforce the approval checkpoint**

Show these exact files to the user:

```text
/home/takahiro/workspace/akari-design/tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.png
/home/takahiro/workspace/akari-design/tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure-review.png
```

Report the clean-guide SHA-256, dimensions, hard-check results, diagnostic
ratios, Candidate C continuation baseline, and any residual concern. Ask for
approval of that exact clean PNG and stop. Do not create the prompt, read the
`imagegen` skill, open a pre-generation reference set, or call `image_gen` in
the same checkpoint. If the guide is rejected, revise only Task 2 artifacts,
record `guide rejected; revision allowed` in `RUN.md`, invoke the generator with
`--replace-unapproved --archive-id guide-r01` for the first rejected guide
(`guide-r02`, then `guide-r03` for later rejections), verify the archived hash
manifest, rerasterize both canonical PNGs, rerun all Task 2 tests and hashes,
show the new bytes, and request approval again. Never delete a rejected archive.

For the first rejection, run:

```bash
bash -lc 'node \
  tmp/akari-v2.1-redesign/stability-r03/guides/build-structure-guide.mjs \
  tmp/akari-v2.1-redesign/stability-r03/guides \
  --replace-unapproved --archive-id guide-r01'
```

### Task 3: Freeze the approved guide and pin the r03 prompt

**Files:**

- Modify: `tmp/akari-v2.1-redesign/stability-r03/RUN.md`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/approvals/guide-approval.json`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/approvals/assert-generation-ready.test.mjs`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/approvals/assert-generation-ready.mjs`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/prompts/akari-v2.1-stability-30-r03.md`

**Interfaces:**

- Consumes: an explicit user message approving the exact Task 2 clean guide
  PNG, its unchanged hash, Candidate C, and the guide landmark record.
- Produces: a recorded guide approval, one complete prompt no longer than
  `3500` Unicode characters, and a two-input generation preflight for Task 4.

- [ ] **Step 1: Reverify that the approved guide bytes did not change**

Run the clean-guide `sha256sum`, `identify`, and PNG-signature commands from
Task 2 and compare them with the values shown to the user. Also rerun both Node
test files and the v2.0 batch digest.

Expected: every value is unchanged, all tests pass, and the batch digest still
matches the Global Constraints. Any guide change invalidates approval and
returns execution to Task 2 before prompt creation or generation.

- [ ] **Step 2: Record the exact guide approval**

Use `apply_patch` to add the user's literal approval message, approval date,
clean-guide path, dimensions, SHA-256, source SVG hash, landmark-record hash,
and status `guide approved and pinned; generation not yet called` to `RUN.md`.
State that approval applies only to those exact bytes. Create
`guide-approval.json` with `schemaVersion: 1`, `decision: "approved"`,
`approvedBy: "user"`, the literal approval text and timestamp with timezone,
and path/hash/dimensions records named `guide`, `reviewImage`, and `landmarks`
for the clean guide, annotated review PNG, and landmark JSON respectively. The
`guide` object must contain numeric `width: 1024` and `height: 1536`. This file
must not exist before the user approval arrives.

- [ ] **Step 3: Write and test the generation-readiness guard**

Use `apply_patch` to create `assert-generation-ready.test.mjs` first. Build
isolated fixture directories and prove that readiness fails for each of these
conditions: missing approval, non-`approved` decision, stale guide bytes,
stale review or landmark hashes, wrong Candidate C hash, three references,
reversed references, any v2.0/r01/r02 reference, `3501` Unicode code points,
an altered in-limit prompt hash, changed batch digest, or an already-existing
output. Also fail empty approval text, an invalid or timezone-free approval
timestamp, and approval dimensions other than `1024x1536`. Prove that the
pinned prompt and exactly the ordered Candidate-C/guide pair pass. Run once and
expect `ERR_MODULE_NOT_FOUND`.

Then create `assert-generation-ready.mjs` with:

```javascript
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

export const EXPECTED_CANDIDATE_SHA256 =
  "fadba782fcf2309063f86a992fdeaacece9a1d1f063adaf681343d60ce959c73";
export const EXPECTED_BATCH_DIGEST =
  "4ac76bd19c478edaf11cf122ed41a35e0658fdf796731d49dcddb323b11382cc";
export const EXPECTED_PROMPT_SHA256 =
  "5b8c7975ebbc0a672df363bbf39e6a26522d2bc9227d2b08016dda643452f2d0";

export function unicodeLength(text) {
  return Array.from(text).length;
}

export function hashFile(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

export function hashTreeLikeSha256sum(root) {
  const files = [];
  const visit = (directory) => {
    for (const name of readdirSync(directory).sort()) {
      const path = join(directory, name);
      if (statSync(path).isDirectory()) visit(path);
      else files.push(path);
    }
  };
  visit(root);
  const listing = files.sort().map((path) =>
    `${hashFile(path)}  ${path}\n`).join("");
  return createHash("sha256").update(listing).digest("hex");
}

function pngDimensions(path) {
  const bytes = readFileSync(path);
  assert.equal(bytes.subarray(0, 8).toString("hex"), "89504e470d0a1a0a");
  return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
}

export function assertGenerationReady(config, expected = {
  candidateSha256: EXPECTED_CANDIDATE_SHA256,
  batchDigest: EXPECTED_BATCH_DIGEST,
  promptSha256: EXPECTED_PROMPT_SHA256,
}) {
  assert.equal(existsSync(config.approvalPath), true, "approval missing");
  const approval = JSON.parse(readFileSync(config.approvalPath, "utf8"));
  assert.equal(approval.schemaVersion, 1);
  assert.equal(approval.decision, "approved");
  assert.equal(approval.approvedBy, "user");
  assert.ok(approval.approvalText.trim().length > 0);
  assert.match(approval.approvedAt, /(?:Z|[+-]\d{2}:\d{2})$/);
  assert.equal(Number.isNaN(Date.parse(approval.approvedAt)), false);
  assert.equal(approval.guide.path, config.guidePath);
  assert.equal(approval.reviewImage.path, config.reviewPath);
  assert.equal(approval.landmarks.path, config.landmarkPath);
  assert.equal(hashFile(config.guidePath), approval.guide.sha256);
  assert.equal(hashFile(config.reviewPath), approval.reviewImage.sha256);
  assert.equal(hashFile(config.landmarkPath), approval.landmarks.sha256);
  assert.deepEqual(
    { width: approval.guide.width, height: approval.guide.height },
    { width: 1024, height: 1536 },
  );
  assert.deepEqual(pngDimensions(config.guidePath), {
    width: 1024,
    height: 1536,
  });
  assert.equal(hashFile(config.candidatePath), expected.candidateSha256);
  assert.deepEqual(config.referencePaths, [
    config.candidatePath,
    config.guidePath,
  ]);
  for (const path of config.referencePaths) {
    assert.equal(/akari-v2\.0|stability-r0[12]/.test(path), false);
  }
  const prompt = readFileSync(config.promptPath, "utf8");
  assert.ok(unicodeLength(prompt) <= 3500);
  assert.equal(hashFile(config.promptPath), expected.promptSha256);
  assert.equal(hashTreeLikeSha256sum(config.batchRoot), expected.batchDigest);
  assert.equal(existsSync(config.outputPath), false, "output already exists");
  return {
    ready: true,
    references: config.referencePaths,
    guideSha256: approval.guide.sha256,
    promptSha256: expected.promptSha256,
  };
}
```

The CLI entry point calls `assertGenerationReady` with this exact configuration
and prints the returned object as two-space JSON:

```javascript
{
  approvalPath: "tmp/akari-v2.1-redesign/stability-r03/approvals/guide-approval.json",
  candidatePath: "tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png",
  guidePath: "tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.png",
  reviewPath: "tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure-review.png",
  landmarkPath: "tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-landmarks.json",
  promptPath: "tmp/akari-v2.1-redesign/stability-r03/prompts/akari-v2.1-stability-30-r03.md",
  referencePaths: [
    "tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png",
    "tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.png",
  ],
  batchRoot: "tmp/akari-v2-uniform-batch",
  outputPath: "tmp/akari-v2.1-redesign/stability-r03/images/akari-v2.1-stability-30-r03.png",
}
```

The guard must require the
approval's current clean-guide, review-PNG, and landmark-JSON hashes; require
exact `1024x1536` approved guide dimensions; verify Candidate C and batch
digests; require an ordered two-item reference list of Candidate C then guide;
reject every review-only path; enforce `Array.from(prompt).length <= 3500`;
require the exact pinned prompt hash; refuse an existing output; and print a
JSON readiness record without calling image generation or writing any image.

Run:

```bash
bash -lc 'node --test \
  tmp/akari-v2.1-redesign/stability-r03/approvals/assert-generation-ready.test.mjs'
```

Expected: all readiness-guard tests pass and zero fail.

- [ ] **Step 4: Create the complete r03 prompt exactly**

Use `apply_patch` to create the prompt file with this complete content:

```text
# Akari v2.1 30-Degree Stability Probe Prompt — r03

Use case: stylized-concept.
Asset: one noncanonical Akari v2.1 guide-assisted stability probe.

Reference roles:
Image 1 is the SOLE identity and rendering authority: selected Candidate C.
Preserve this exact same approachable 18-year-old Akari, small open friendly
smile, familiar camera-directed gaze, selected low horizontally emphasized eye
language, facial character, compact softly rounded lower face, warm chestnut
hair, off-center V bangs, pale muted-blue crossed hairpin, one connected low
character-left ponytail, warm off-white field, white crew-neck top, palette,
soft linework, and restrained cel finish.

Image 2 is the SOLE projection and placement authority: a neutral structural
guide. Follow only its approximately 30-degree character-left yaw, near side on
canvas-right, vertical head axis, level facial axes, four canthus positions,
near/far foreshortening, iris occlusion, face centerline, nose and jaw
projection, neck, quiet shoulders, crop, and scale. Do not copy identity,
proportions, age, expression, color, texture, or style from the guide.

Primary request:
Create one tight head-and-shoulders portrait near 1024 x 1536. Keep chin-to-
crown head height around 55 to 65 percent of the canvas. Realize Candidate C's
identity-bearing shapes at the guide's placement: a coherent modest three-
quarter camera view toward Akari's own left hairpin side, not an independently
turned head. Keep the complete hair silhouette and compact chin inside
comfortable margins.

Eye construction:
Project Candidate C's low almond construction into both guide apertures. Keep a
low, gently sloped central upper-lid segment and quiet lower lid. The farther
eye is naturally narrower; keep its upper lid low rather than domed, its iris
no larger or more exposed than the nearer iris, and allow nasal-side and upper-
lid occlusion. A complete circular iris or catchlight is unnecessary. End the
nearer upper lid at its anatomical outer canthus in one connected soft taper,
without an independently readable extension. Preserve honey-amber irises,
restrained pupils and highlights, and compatible binocular gaze.

Identity and presentation:
Preserve Candidate C's brow placement, eye spacing, small natural nose, soft
cheeks, compact rounded jaw and chin, friendly smile, and fresh non-glamorous
18-year-old read in correct perspective. Keep warm chestnut hair, the complete
crossed hairpin and attached low ponytail on character-left near canvas-right,
the white crew-neck shoulder crop, warm off-white background, restrained shine,
and coherent anatomy.

Avoid only these test-breaking failures: head or camera roll; a dome-shaped
farther upper lid; increased farther-eye iris size or exposure; a separate
nearer-eye outer spur, hook, lash cluster, or eyeliner point; a narrow V-shaped
chin; mirrored laterality; near-front, 45-degree, or profile substitution;
malformed or duplicated anatomy; accidental crop; text; logo; watermark.
```

- [ ] **Step 5: Enforce prompt length, hash, and two-input preflight**

Run:

```bash
bash -lc 'node -e '\''const fs=require("node:fs"); const p="tmp/akari-v2.1-redesign/stability-r03/prompts/akari-v2.1-stability-30-r03.md"; const s=fs.readFileSync(p,"utf8"); const n=[...s].length; console.log(n); if(n>3500) process.exit(1)'\'''
sha256sum \
  tmp/akari-v2.1-redesign/stability-r03/prompts/akari-v2.1-stability-30-r03.md
sha256sum \
  tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png \
  tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.png
bash -lc 'node \
  tmp/akari-v2.1-redesign/stability-r03/approvals/assert-generation-ready.mjs'
bash -lc './node_modules/.bin/markdownlint-cli2 \
  :tmp/akari-v2.1-redesign/stability-r03/RUN.md \
  :tmp/akari-v2.1-redesign/stability-r03/prompts/akari-v2.1-stability-30-r03.md \
  --no-globs'
git check-ignore -v \
  tmp/akari-v2.1-redesign/stability-r03/RUN.md \
  tmp/akari-v2.1-redesign/stability-r03/prompts/akari-v2.1-stability-30-r03.md
```

Expected: the complete file is exactly `2995` Unicode code points including its
final newline, its SHA-256 is
`5b8c7975ebbc0a672df363bbf39e6a26522d2bc9227d2b08016dda643452f2d0`,
Candidate C and guide hashes match, the readiness guard exits zero and prints
exactly two ordered references, both Markdown files lint, and both are ignored.
Record the readiness result and exactly two planned inputs in `RUN.md`; record
v2.0, r01, and r02 paths in a separate review-only table.

### Task 4: Generate and preserve the single r03 probe

**Files:**

- Read:
  `tmp/akari-v2.1-redesign/stability-r03/prompts/akari-v2.1-stability-30-r03.md`
- Read:
  `tmp/akari-v2.1-redesign/r01/recover-image-payload.mjs`
- Read:
  `tmp/akari-v2.1-redesign/stability-r03/approvals/assert-generation-ready.mjs`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/images/akari-v2.1-stability-30-r03.png`
- Modify: `tmp/akari-v2.1-redesign/stability-r03/RUN.md`

**Interfaces:**

- Consumes: one exact prompt, Candidate C, and the exact approved clean guide.
- Produces: one exact first-call PNG plus request IDs, source provenance,
  dimensions, signature, hash, and byte-comparison evidence for Task 5.

- [ ] **Step 1: Read the current image-generation instructions**

Read the current `imagegen` skill completely before any generation action.
Recheck `RUN.md` for a literal exact-guide approval and exactly two reference
paths. Run `assert-generation-ready.mjs` again immediately before opening the
references and record its exact JSON result in `RUN.md`. If the guard fails or
either ledger condition is absent, stop without calling the tool.

- [ ] **Step 2: Open exactly the two generation authorities at original detail**

Reverify both hashes, then use `view_image(detail=original)` on Candidate C and
the exact approved clean guide. State immediately before generation:

1. Candidate C is the sole identity and rendering authority and controls every
   identity-bearing shape, expression, hair, color, line, and finish.
2. The neutral guide is the sole projection and placement authority and
   controls only view geometry, axes, canthi, near/far scale, occlusion, nose,
   jaw, neck, shoulders, crop, and scale.

Do not open v2.0, r01, or r02 images in the immediate pre-generation reference
set. Keep the two approved inputs visible in the conversation context.

- [ ] **Step 3: Make exactly one built-in image-generation call**

Call built-in `image_gen` once with the complete Task 3 prompt and exactly these
`referenced_image_paths`:

```text
/home/takahiro/workspace/akari-design/tmp/akari-v2.1-redesign/r01/images/akari-v2.1-face-r01-c.png
/home/takahiro/workspace/akari-design/tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure.png
```

Omit `num_last_images_to_include`. Record the outer request ID, completed call
or generation ID, tool-provided source path, completed-event status, and any
tool-returned revised prompt. Never make a second generation call in this run.

- [ ] **Step 4: Preserve the exact returned PNG without transformation**

Copy the readable tool-provided source with `cp --no-clobber` to the target
image path and run `cmp --silent` between the literal source and destination.
Do not move or delete the generated source.

If and only if the image is displayed but no readable source PNG exists, run
the existing recovery helper through `bash -lc` with the literal completed call
ID, exact destination, and actual Asia/Tokyo session day. It must structurally
match one current-day `image_generation_call`, require one unique `iVBOR`
payload, verify signature `89504e470d0a1a0a`, and refuse overwrite. If recovery
fails, record `technical failure` and stop without another generation call.

- [ ] **Step 5: Verify, inspect, and record the saved output**

Run:

```bash
file \
  tmp/akari-v2.1-redesign/stability-r03/images/akari-v2.1-stability-30-r03.png
identify -format '%f %wx%h %[channels]\n' \
  tmp/akari-v2.1-redesign/stability-r03/images/akari-v2.1-stability-30-r03.png
xxd -p -l 8 \
  tmp/akari-v2.1-redesign/stability-r03/images/akari-v2.1-stability-30-r03.png
sha256sum \
  tmp/akari-v2.1-redesign/stability-r03/images/akari-v2.1-stability-30-r03.png
```

Expected: one readable non-empty RGB portrait PNG near `1024x1536`, signature
`89504e470d0a1a0a`, and one recorded hash. Use `view_image(detail=original)` on
the saved output and Candidate C. Record call count `1`, request and call IDs,
source path, save or recovery method, dimensions, channels, signature, hash,
`cmp` result, prompt/revised-prompt hashes, and status
`generated once; preserved; awaiting six-gate review` in `RUN.md`.

If the completed event contains a revised prompt, structurally select the
unique event by completed call ID, emit only that field with `jq -j`, hash it,
and run `cmp --silent` against the pinned prompt. Record byte identity or the
exact difference; a revised prompt mismatch does not authorize a retry.

### Task 5: Measure, review, and stop at the r03 result gate

**Files:**

- Create:
  `tmp/akari-v2.1-redesign/stability-r03/measurements/output-placement-1.json`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/measurements/output-placement-2.json`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/measurements/output-summary.json`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/measurements/output-vs-guide-placement-1.png`
- Create:
  `tmp/akari-v2.1-redesign/stability-r03/measurements/output-vs-guide-placement-2.png`
- Create: `tmp/akari-v2.1-redesign/stability-r03/REVIEW.md`
- Modify: `tmp/akari-v2.1-redesign/stability-r03/RUN.md`

**Interfaces:**

- Consumes: the exact one-call r03 output, Candidate C, approved clean guide and
  landmark record, accepted v2.0 review authorities, and r01/r02 negative
  evidence.
- Produces: two independent measurement placements, two unrotated normalized
  overlays, six evidence-backed gates, one final verdict, and an explicit stop
  for user direction.

- [ ] **Step 1: Open the complete review set at original detail**

Use `view_image(detail=original)` on:

1. Candidate C as the positive identity and eye-morphology authority;
2. the exact r03 probe as the sole review target;
3. the exact approved clean guide as projection/placement authority;
4. the annotated guide as review explanation only;
5. the v2.0 face for lineage, warmth, and age only;
6. the v2.0 full body for laterality and rendering family only;
7. rejected r01 and r02 as negative evidence for eye drift, spur, chin, and
   roll only.

Do not treat v2.0, r01, or r02 as positive generation targets.

- [ ] **Step 2: Record two independent output landmark placements**

For each placement JSON, record canvas-pixel stroke-center coordinates for:

- crown and chin;
- four canthi;
- sampled upper and lower lid centerlines for both eyes;
- two brow visible arcs;
- both mouth corners;
- both visible acromion landmarks;
- nose tip, visible ear center, and near/far cheek contour anchors;
- fitted iris center, radii, rotation, vertical diameter `D`, and visible
  vertical span `V` along the fitted ellipse's apparent vertical axis for both
  eyes;
- near anatomical outer canthus, outer tangent anchor, and continuation
  endpoint;
- crown-plane endpoints and qualitative nostril/under-chin visibility for the
  pitch record.

Finish placement 1, hide its annotations, and do not inspect its coordinate
record while making placement 2 from the clean output. Run
`comparePlacements` to create `output-summary.json`. Record each placement's
eye, brow, and mouth axis delta against the guide to one decimal degree; do not
average across placements. Record width and height ratios, upper-lid central
rise, iris `D`, `V`, and `E`, and `L / W_near` as diagnostics and morphology
evidence. The two files must use `subject: "output"`, `scope: "full"`, and
`pass: 1` or `pass: 2` respectively, with `headAxis: null` in both files.

Evaluate all four combinations of the two output placements and two approved
guide placements for every facial axis. Every combination must remain within
the inclusive `3.0`-degree axial difference. For continuation uncertainty, use
the greatest of `2 / minimum observed W_near`, Candidate C placement spread,
and output placement spread.

Run:

```bash
bash -lc 'node \
  tmp/akari-v2.1-redesign/stability-r03/measurements/measure-landmarks.mjs \
  compare \
  --first tmp/akari-v2.1-redesign/stability-r03/measurements/output-placement-1.json \
  --second tmp/akari-v2.1-redesign/stability-r03/measurements/output-placement-2.json \
  --reference tmp/akari-v2.1-redesign/stability-r03/measurements/guide-placement-1.json \
  --reference tmp/akari-v2.1-redesign/stability-r03/measurements/guide-placement-2.json \
  --guide-approval tmp/akari-v2.1-redesign/stability-r03/approvals/guide-approval.json \
  --candidate-baseline tmp/akari-v2.1-redesign/stability-r03/measurements/candidate-c-lid-summary.json \
  --output tmp/akari-v2.1-redesign/stability-r03/measurements/output-summary.json'
```

The summary must preserve three `2x2` `axisDeltasDeg` matrices for eyes, brows,
and mouth in `[output pass][guide pass]` order, plus both raw subject summaries
and both raw guide summaries.

Expected hard logic: both placements keep all three facial-axis deltas within
`3.0` degrees; no boundary straddle exists; farther iris diameter and exposure
do not exceed the nearer values; and near continuation does not exceed the
Candidate C baseline plus uncertainty. A disputed landmark or threshold fails
the controlling gate.

- [ ] **Step 3: Create two scale-and-translation-only overlays**

For each placement, compute uniform scale as:

```text
approved guide chin-to-crown height / output chin-to-crown height
```

Then translate the scaled output so its two-eye-center midpoint equals the
guide eye midpoint. Run:

```bash
bash -lc 'node \
  tmp/akari-v2.1-redesign/stability-r03/measurements/measure-landmarks.mjs \
  overlay \
  --placement tmp/akari-v2.1-redesign/stability-r03/measurements/output-placement-1.json \
  --guide-placement tmp/akari-v2.1-redesign/stability-r03/measurements/guide-placement-1.json \
  --source tmp/akari-v2.1-redesign/stability-r03/images/akari-v2.1-stability-30-r03.png \
  --guide-review tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure-review.png \
  --output tmp/akari-v2.1-redesign/stability-r03/measurements/output-vs-guide-placement-1.png'
bash -lc 'node \
  tmp/akari-v2.1-redesign/stability-r03/measurements/measure-landmarks.mjs \
  overlay \
  --placement tmp/akari-v2.1-redesign/stability-r03/measurements/output-placement-2.json \
  --guide-placement tmp/akari-v2.1-redesign/stability-r03/measurements/guide-placement-2.json \
  --source tmp/akari-v2.1-redesign/stability-r03/images/akari-v2.1-stability-30-r03.png \
  --guide-review tmp/akari-v2.1-redesign/stability-r03/guides/akari-v2.1-stability-30-r03-structure-review.png \
  --output tmp/akari-v2.1-redesign/stability-r03/measurements/output-vs-guide-placement-2.png'
```

The helper uses ImageMagick to place the uniformly scaled output on a
`1024x1536` transparent canvas and composite the annotated guide at `55`
percent opacity. Do not rotate, skew, distort, or warp either image.

Inspect both overlays for agreement among the face centerline, nose tip, four
canthi, cheeks, chin, and visible ear. Use the whole construction to judge the
`25`-to-`35`-degree band. Compare crown plane, brow, nose, ear, mouth, chin,
nostril, and under-chin relations for qualitative pitch. If yaw or pitch remains
reasonably disputed, Gate 3 fails.

- [ ] **Step 4: Apply all six r03 gates**

Create `REVIEW.md` and record one `Pass` or `Fail` with concrete evidence for:

1. same-person Candidate C identity, expression, warmth, and selected v2.1
   rendering;
2. selected eye morphology, including low farther upper lid, no extra farther
   iris scale or exposure, Candidate-C-relative connected near taper, restrained
   highlights, and compatible gaze;
3. coherent approximately 30-degree character-left view, all three axis deltas
   within `3.0` degrees in both placements, quiet shoulders without compensating
   lean, and qualitative pitch match;
4. coherent hairline, V bangs, complete crossed hairpin, visible ear, attached
   low ponytail, and character-left near side on canvas-right;
5. approachable 18-year-old read, soft cheeks, compact rounded chin, and
   non-glamorous presentation;
6. no malformed geometry, disconnection, duplication, seam, border, accidental
   crop, text, logo, watermark, or material-rendering artifact.

The final verdict is `PASS` only if all six gates pass. Diagnostic ratios never
override lid curvature, iris occlusion, canthus termination, axes, yaw/pitch,
or direct Candidate C comparison. Record every residual Minor on PASS and every
failed gate and stop reason on FAIL.

- [ ] **Step 5: Record result meaning and the exact stop route**

Update both ledgers with the final verdict and state that r03 remains ignored,
noncanonical evidence. On PASS, record only one successful guide-assisted
realization with these exact inputs; do not claim statistical reproducibility
or Candidate-C-alone rotation stability.

On repeated Gate 2 farther-eye dome/exposure or near spur, or repeated Gate 3
roll despite the guide, record that the prompt-guided 30-degree track ends and
ask the user to choose between front-master redesign and Candidate C as a
front-only constraint. If failure is confined to identity, age, lower face,
laterality, crop, anatomy, or material artifact, stop for separate diagnosis
without claiming the eye/axis hypothesis failed. Never start r04 automatically.

- [ ] **Step 6: Run final verification and show the result**

Run serially:

```bash
bash -lc 'node --test \
  tmp/akari-v2.1-redesign/stability-r03/guides/build-structure-guide.test.mjs \
  tmp/akari-v2.1-redesign/stability-r03/measurements/measure-landmarks.test.mjs \
  tmp/akari-v2.1-redesign/stability-r03/approvals/assert-generation-ready.test.mjs'
bash -lc './node_modules/.bin/markdownlint-cli2 \
  :tmp/akari-v2.1-redesign/stability-r03/RUN.md \
  :tmp/akari-v2.1-redesign/stability-r03/REVIEW.md \
  :tmp/akari-v2.1-redesign/stability-r03/prompts/akari-v2.1-stability-30-r03.md \
  --no-globs'
bash -lc 'npm run lint:md'
find tmp/akari-v2-uniform-batch -type f -print0 | sort -z | \
  xargs -0 sha256sum | sha256sum
find \
  tmp/akari-v2.1-redesign/r01 \
  tmp/akari-v2.1-redesign/stability-r01 \
  tmp/akari-v2.1-redesign/stability-r02 \
  -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum
xxd -p -l 8 \
  tmp/akari-v2.1-redesign/stability-r03/images/akari-v2.1-stability-30-r03.png
git check-ignore -v \
  tmp/akari-v2.1-redesign/stability-r03/RUN.md \
  tmp/akari-v2.1-redesign/stability-r03/REVIEW.md \
  tmp/akari-v2.1-redesign/stability-r03/images/akari-v2.1-stability-30-r03.png
git status --short -- tmp/akari-v2.1-redesign
git diff --check
git diff --quiet
git diff --cached --quiet
git status --short --branch
```

Expected: all three Node suites pass; local and tracked Markdown lint pass; the
batch digest, combined historical digest, and PNG signature remain pinned;
every r03 artifact is ignored; tracked and staged trees remain clean after this
plan commit; and the pre-existing user-owned untracked v2.0 plan remains
untouched.

Before reporting completion, rerun `cmp --silent` with the literal generated
source path recorded in `RUN.md` as the first argument and the saved r03 PNG as
the second. If payload recovery was used, compare the recovered payload bytes
to the saved PNG and record that recovery-specific identity instead.

Show the exact r03 probe and report all six gates, measurement uncertainty, and
the applicable stop route. Stop for explicit user direction. Do not infer
approval from a PASS verdict and do not continue to Stage 2, promotion, r04,
package, manifest, release, or PDF work.
