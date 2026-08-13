# Akari V2.2 Face-Angle Preservation and Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve the three user-approved Akari V2.2 face-angle PNGs and make
the global generation skill select exactly one angle-matched support image per
identity-sensitive call.

**Architecture:** The repository remains the formal source of truth: the
canonical portrait and full-body authorities stay unchanged, while a new
`accepted/base/face-angles/` directory holds exact-byte supporting authorities.
The global skill adds a small routing contract over those repository paths and
keeps its existing three-reference ceiling, identity gates, and retry stops.

**Tech Stack:** Git-tracked PNG assets, Markdown authority records, shell
contract checks, `markdownlint-cli2`, Skill `quick_validate.py`, and read-only
fresh-agent behavior checks.

## Global Constraints

- Preserve F00, F01-r02, and F02 without resizing, cropping, recompression,
  color conversion, or retouching.
- Keep the canonical portrait as the primary face authority and the canonical
  full-body image as the body and baseline-outfit authority.
- Pass no more than one face-angle support image in one generation call.
- Keep the total reference-image limit at three.
- Never promote or reference F01-r01, rejected images, comparison artifacts, or
  temporary GPT Pro package files.
- Do not generate S03 or any other new image in this implementation.
- Preserve unrelated worktree changes and do not include them in task commits.

---

### Task 1: Establish the Current-Skill Baseline

**Files:**

- Read:
  `/home/takahiro/.agents/skills/generating-akari-v2-2-images/SKILL.md`
- Read: `akari-v2.2/accepted/base/`
- Do not modify files in this task.

**Interfaces:**

- Consumes: the currently deployed global skill and the current accepted V2.2
  authority tree.
- Produces: three verbatim read-only behavior results showing how the current
  skill chooses references for near-front, hairpin-side, and opposite-side
  scene briefs.

- [ ] **Step 1: Define three realistic routing scenarios**

  Use one scenario for each intended direction:

  1. near-front closed-mouth chest-up scene;
  2. approximately 30-degree turn toward Akari's hairpin side;
  3. approximately 30-degree turn away from the hairpin in a knee-up scene that
     also needs body balance.

  Each scenario asks only for a reference list and role explanation. It must
  explicitly forbid image generation.

- [ ] **Step 2: Run the scenarios against the current skill**

  Run fresh read-only agent contexts in parallel. Restrict each context to the
  current deployed `SKILL.md` and existing accepted authority paths so the
  follow-up design and temporary package cannot reveal the intended answer.

- [ ] **Step 3: Verify the baseline exposes the missing behavior**

  Expected baseline failure: the current skill has no explicit F00/F01-r02/F02
  path resolution or deterministic angle-selection rule. Record the selected
  paths and the exact explanation from each result. If the baseline already
  implements all three routes, stop and reduce the skill edit to documentation
  clarification only.

---

### Task 2: Preserve the Accepted Repository Pack

**Files:**

- Create:
  `akari-v2.2/accepted/base/face-angles/akari-v2.2-face-near-front-f00.png`
- Create:
  `akari-v2.2/accepted/base/face-angles/akari-v2.2-face-hairpin-side-f01-r02.png`
- Create:
  `akari-v2.2/accepted/base/face-angles/akari-v2.2-face-opposite-side-f02.png`
- Modify: `akari-v2.2/README.md`
- Modify: `akari-v2.2/selection.md`

**Interfaces:**

- Consumes: the three approved working copies and hashes in the design spec.
- Produces: stable repository paths used by the global skill's angle router.

- [ ] **Step 1: Run the pre-preservation contract**

  Run:

  ```bash
  test -f akari-v2.2/accepted/base/face-angles/akari-v2.2-face-near-front-f00.png
  ```

  Expected: FAIL because the accepted face-angle directory does not exist yet.

- [ ] **Step 2: Copy the three approved byte streams**

  Copy these exact sources to the corresponding accepted destinations:

  ```text
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/reference/02-approved-f00.png
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/selected/F01-hairpin-side-r02.png
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/selected/F02-opposite-side.png
  ```

  Set normal tracked-file permissions without altering file contents.

- [ ] **Step 3: Verify exact bytes and dimensions**

  Run `sha256sum` and `file` on all three accepted paths. Expected hashes, in
  F00/F01-r02/F02 order:

  ```text
  8ff5e5369b9877225b2c2bbc87ea92b6cb0e60309e846cb9250fc2a366cae957
  a8d1574fd1edb071be5ddf111768aa1e5c8fa38a02d5f7aac76b5023823e6902
  338568d22fc150b5b965b259a731de1d30d33c41d0d1238e3c28c044cb7734ad
  ```

  Expected dimensions: `1086x1448`, `1086x1448`, and `1024x1536`.

- [ ] **Step 4: Update the repository authority documentation**

  Add a `Face-Angle Supporting Authorities` section to
  `akari-v2.2/README.md` containing:

  - the three exact accepted paths;
  - the canonical portrait's precedence over base face identity;
  - the F00/F01-r02/F02 routing table from the approved design;
  - the one-angle-only and three-total-reference limits;
  - the unsupported strict-profile, rear, overhead, and extreme-foreshortening
    boundary.

  Add a `Face-Angle Pack F00 / F01-r02 / F02` entry to
  `akari-v2.2/selection.md` containing the approval date, dimensions, hashes,
  angle roles, exact-byte preservation statement, and F01-r01 exclusion.

- [ ] **Step 5: Lint the repository Markdown**

  Run:

  ```bash
  bash -lc 'npm run lint:md'
  npx markdownlint-cli2 \
    docs/superpowers/specs/2026-08-13-akari-v2-2-face-angle-preservation-routing-design.md \
    docs/superpowers/plans/2026-08-13-akari-v2-2-face-angle-preservation-routing.md
  ```

  Expected: both commands report zero issues.

- [ ] **Step 6: Commit only the accepted pack and its documentation hunks**

  Stage the three new PNGs and only the new face-angle hunks from the already
  modified `README.md` and `selection.md`. Inspect `git diff --cached` and
  confirm D38/D39 or other pre-existing worktree changes are absent. Commit:

  ```bash
  git commit -m "feat: preserve v2.2 face-angle authorities"
  ```

---

### Task 3: Add the Global Skill Angle Router with Behavior Tests

**Files:**

- Stage from:
  `/home/takahiro/.agents/skills/generating-akari-v2-2-images/SKILL.md`
- Modify and deploy:
  `/home/takahiro/.agents/skills/generating-akari-v2-2-images/SKILL.md`
- Do not add bundled image copies; the repository accepted paths are the formal
  source, and the existing canonical fallback remains valid outside this repo.

**Interfaces:**

- Consumes: the three stable accepted paths from Task 2.
- Produces: a deterministic `near-front -> F00`, `hairpin-side -> F01-r02`,
  `opposite-side -> F02` selection contract that fits inside the existing
  three-reference input schema.

- [ ] **Step 1: Create a writable staged copy of the current skill**

  Copy the skill folder under `tmp/` and edit only the staged `SKILL.md` until
  validation and GREEN behavior checks pass.

- [ ] **Step 2: Add the minimal path-resolution and routing guidance**

  In `正典と本人性ロック`, add the three repository paths as
  user-approved angle-support authorities available only when all three are
  readable. If the pack is incomplete, report the missing angle support when
  the requested direction needs it; do not silently substitute a different
  angle.

  In `参照設計`, add a compact routing table:

  ```text
  near-front or shallow three-quarter -> F00
  about 30 degrees toward the hairpin side -> F01-r02
  about 30 degrees toward the opposite side -> F02
  ```

  Require the canonical portrait in every new identity-sensitive scene, add no
  more than one matching angle image, and use the remaining slot for the
  full-body or another essential approved reference. State that character
  anatomy determines the side before any canvas flip.

  In the transition-gate section, require the first downstream use of each
  angle support in a changed environment or workflow to be generated alone,
  compared at the same face scale, and approved by the user before more outputs
  use that angle support.

- [ ] **Step 3: Run the same three scenarios against the staged skill**

  Use fresh read-only agent contexts with the staged `SKILL.md`. Expected GREEN
  results:

  - near-front scenario selects canonical portrait plus F00;
  - hairpin-side scenario selects canonical portrait plus F01-r02;
  - opposite-side knee-up scenario selects canonical portrait, F02, and the
    canonical full-body image;
  - no scenario selects multiple face-angle images or F01-r01;
  - every result stops before image generation.

- [ ] **Step 4: Self-review the skill edit**

  Confirm the change does not weaken:

  - explicit-generation authorization;
  - user-only identity approval;
  - the three-reference ceiling;
  - existing retry and stop conditions;
  - the prohibition on using rejected or unapproved images.

- [ ] **Step 5: Validate the staged skill**

  Run:

  ```bash
  uv run --isolated --no-project --with pyyaml python3 \
    /home/takahiro/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
    tmp/generating-akari-v2-2-images-face-angle-routing-test
  npx markdownlint-cli2 \
    tmp/generating-akari-v2-2-images-face-angle-routing-test/SKILL.md
  ```

  Expected: skill validation succeeds and Markdown reports zero issues.

- [ ] **Step 6: Deploy the validated SKILL.md**

  Copy the validated staged file over the global `SKILL.md` with user-approved
  elevated write access. Re-run both validation commands against the deployed
  skill and verify the deployed bytes match the staged bytes.

---

### Task 4: Close the Preservation State and Run Final Contracts

**Files:**

- Modify (ignored working record):
  `tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/DECISIONS.md`
- Read: repository and global skill changes from Tasks 2 and 3.

**Interfaces:**

- Consumes: the verified repository pack and deployed skill.
- Produces: an auditable completed preservation state and a clear next gate for
  later S03 generation.

- [ ] **Step 1: Update the local decision state**

  Set:

  ```text
  Repository preservation: completed
  Global skill update: completed
  School-day S03 resume: paused_pending_explicit_generation_request
  ```

  Add the three accepted paths and state that generation was not performed in
  this task.

- [ ] **Step 2: Run final repository and skill scans**

  Verify:

  - all three accepted files exist and match the approved hashes;
  - README, selection history, and the deployed skill name all three paths;
  - `F01-r01` appears only as an excluded comparison-history label;
  - no file under `tmp/` or `review/` is staged;
  - `git diff --cached` is empty after the task commit;
  - `git status --short` still shows unrelated pre-existing changes only.

- [ ] **Step 3: Report the next explicit gate**

  Report that formal preservation and routing are complete. The next action is
  an explicit Akari V2.2 generation request; because the skill changed, that
  later session begins with its canonical-portrait-only environment preflight,
  followed by one routed downstream transfer candidate and user identity
  confirmation.
