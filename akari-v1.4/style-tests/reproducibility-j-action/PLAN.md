# Akari v1.4 J Action Reproducibility Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:dispatching-parallel-agents` for the three independent image
> generations, then review all outputs together in the parent session.

**Goal:** Produce and evaluate three independent v1.4 illustrations of Akari
peeling one mandarin at a dining table.

**Architecture:** One byte-identical shared prompt and one fixed ordered
three-image reference set feed three separate built-in image-generation calls.
No output is used as a reference for another output. The parent session
validates files, creates a controlled comparison sheet, and records a
gate-by-gate result.

**Tech Stack:** Built-in image generation, PNG, ImageMagick or Pillow for
deterministic comparison assembly, shell tools for hashes and dimensions.

## Global Constraints

- Output canvas is exact 1024 × 1536 portrait PNG.
- Reference order is G2, I-2, canonical ornament-side v1.1 reference.
- All three calls use byte-identical `PROMPT.md`.
- Each generation gets one call and no artistic retry before comparison.
- No J output becomes an input to another J output.
- The formal pass threshold is at least two of three samples passing every
  controlling gate in `DESIGN.md`.

---

### Task 1: Freeze the shared generation inputs

**Files:**

- Create: `akari-v1.4/style-tests/reproducibility-j-action/DESIGN.md`
- Create: `akari-v1.4/style-tests/reproducibility-j-action/PROMPT.md`
- Create: `akari-v1.4/style-tests/reproducibility-j-action/PLAN.md`

- [x] Record the approved action, reference authority, and rejection gates.
- [x] Calculate and retain the SHA-256 of `PROMPT.md`.
- [x] Verify that every referenced source image exists before generation.

### Task 2: Generate J-1, J-2, and J-3 independently

**Files:**

- Create: `akari-v1.4/style-tests/reproducibility-j-action/akari-v14-j1-mandarin-action-repro.png`
- Create: `akari-v1.4/style-tests/reproducibility-j-action/akari-v14-j2-mandarin-action-repro.png`
- Create: `akari-v1.4/style-tests/reproducibility-j-action/akari-v14-j3-mandarin-action-repro.png`

- [x] Dispatch three isolated generation workers concurrently.
- [x] Give every worker the same prompt path, reference paths, and reference
  order.
- [x] Give each worker a unique final output path.
- [x] Make one built-in image-generation call per worker without retry.

### Task 3: Validate production properties and visual gates

**Files:**

- Create: `akari-v1.4/style-tests/reproducibility-j-action/akari-v14-j-action-comparison.png`
- Create: `akari-v1.4/style-tests/reproducibility-j-action/README.md`

- [x] Verify each output is a readable 1024 × 1536 true-color PNG.
- [x] Review identity, age, face, ornament, roomwear, body, and clean finish.
- [x] Review the two-hand peel action, wrist visibility, fingers, rind contact,
  gaze, dish count, and forbidden props.
- [x] Assemble one comparison containing full frames plus equal-scale face,
  hand-action, and lower-body crops.
- [x] Record the gate table, rankings, failures, pass count, prompt hash,
  reference paths, and generation method in `README.md`.

### Task 4: Persist the deliverables

**Files:**

- Save every file created by Tasks 1–3 as one artifact set.

- [x] Save the three originals, comparison image, design, prompt, plan, and
  README together.
- [x] Present the comparison and links to all three original images.
