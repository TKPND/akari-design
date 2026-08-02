# Akari v1.7 V17-03 Hairpin-Side 45-Degree Promotion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote the explicitly selected V17-03 r02 C PNG byte-for-byte into
the minimal tracked v1.7 checkpoint, prove the merged result, and remove only
the two completed V17-03 worktrees and branches after every cleanup
precondition passes.

**Architecture:** Reuse the existing r02 worktree that contains the ignored,
hash-pinned selection source. Fast-forward it to this committed plan, create
one atomic three-file promotion commit, independently review that commit,
fast-forward local `main`, verify the merged bytes and history, and then run
the separately gated cleanup. The authoritative generated C source stays
outside the removable worktrees.

**Tech Stack:** Bash, `cp`, `cmp`, `sha256sum`, `xxd`, ImageMagick
`identify`, Codex `view_image`, Markdown lint, and Git.

## Global Constraints

- Follow
  `docs/superpowers/specs/2026-08-02-akari-v1-7-hairpin-45-promotion-design.md`.
- Execute the promotion only in
  `/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02`
  after fast-forwarding its expected branch to the committed plan on local
  `main`.
- Selected ignored source:
  `build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png`.
- Authoritative generated source:
  `/home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png`.
- Source and destination must all have SHA-256
  `bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954`.
- Destination:
  `akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png`.
- Refuse to copy if the destination already exists; never overwrite or
  reconcile it inside this plan.
- Change exactly the destination PNG, `akari-v1.7/README.md`, and
  `akari-v1.7/selection.md` in the promotion commit.
- Preserve V17-01 as the sole front-view authority, V17-02 as the accepted
  character-left hairpin-side 30-degree authority, and V17-03 as the accepted
  character-left hairpin-side 45-degree authority for its selected fixed
  moment.
- Preserve the two inherited r01 A Minor image findings; do not turn the final
  task/process review's zero-finding result into a global flawlessness claim.
- Use the committed promotion design as the durable selection fact source.
  The ignored r02 build directory has no local text selection ledger.
- Do not track or stage r01/r02 candidates, comparisons, crops, reports,
  ledgers, rollout extracts, or any other generated review artifact.
- Do not modify another version, the root README, a manifest, validator,
  renderer, audit, release artifact, or PDF.
- Do not run Node tests, Python tests, package validation, PDF builds, OCR,
  integration gates, or release gates.
- Independent review must report zero Critical and zero Important findings
  before integration.
- Keep both V17-03 worktrees and branches if a cleanup precondition or merged
  verification fails.
- Cleanup may remove only the exact r01/r02 worktree paths and expected
  branches named in Task 4. Use `git worktree remove --force` only for those
  exact paths and `git branch -d` only; never use `git branch -D`.
- Do not push or otherwise synchronize a remote.

---

### Task 1: Create the atomic V17-03 promotion commit in the r02 worktree

**Files:**

- Read:
  `docs/superpowers/specs/2026-08-02-akari-v1-7-hairpin-45-promotion-design.md`
- Read:
  `docs/superpowers/plans/2026-08-02-akari-v1-7-hairpin-45-promotion.md`
- Read source:
  `build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png`
- Read source:
  `/home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png`
- Create:
  `akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png`
- Modify: `akari-v1.7/README.md`
- Modify: `akari-v1.7/selection.md`

**Interfaces:**

- Consumes: the committed approved promotion design, this committed plan, and
  one ignored review PNG proven byte-identical to its authoritative generated
  source.
- Produces: one commit whose changed path set is exactly one accepted PNG and
  two package Markdown files.

- [ ] **Step 1: Verify both checkouts and fast-forward only the r02 branch**

Run from `/home/takahiro/workspace/akari-design`:

```bash
set -euo pipefail
test "$(pwd -P)" = \
  "/home/takahiro/workspace/akari-design"
test "$(git branch --show-current)" = "main"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
test -f \
  docs/superpowers/specs/2026-08-02-akari-v1-7-hairpin-45-promotion-design.md
test -f \
  docs/superpowers/plans/2026-08-02-akari-v1-7-hairpin-45-promotion.md
git cat-file -e \
  HEAD:docs/superpowers/specs/2026-08-02-akari-v1-7-hairpin-45-promotion-design.md
git cat-file -e \
  HEAD:docs/superpowers/plans/2026-08-02-akari-v1-7-hairpin-45-promotion.md
test "$(git -C \
  /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02 \
  branch --show-current)" = \
  "codex/akari-v1-7-hairpin-45-continuity-r02"
test -z "$(git -C \
  /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02 \
  status --porcelain=v1 --untracked-files=all)"
git merge-base --is-ancestor \
  codex/akari-v1-7-hairpin-45-continuity-r02 main
test ! -e \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
test ! -e \
  /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02/akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
git -C \
  /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02 \
  merge --ff-only main
test "$(git -C \
  /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02 \
  rev-parse HEAD)" = "$(git rev-parse main)"
```

Expected: local `main` remains clean, both promotion documents exist in its
`HEAD`, the r02 branch is a clean ancestor of `main`, neither checkout has the
destination, and the r02 branch fast-forwards exactly to the plan commit.
Stop before the merge if any assertion fails.

- [ ] **Step 2: Verify selection-source provenance and image invariants**

Change to the r02 worktree and run:

```bash
set -euo pipefail
cd \
  /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02
test "$(pwd -P)" = \
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02"
test "$(git branch --show-current)" = \
  "codex/akari-v1-7-hairpin-45-continuity-r02"
test -f \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png
test -f \
  /home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png
test -f \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-comparison.png
cmp --silent \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png \
  /home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png
printf '%s  %s\n' \
  bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954 \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png \
  | sha256sum -c -
printf '%s  %s\n' \
  bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954 \
  /home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png \
  | sha256sum -c -
printf '%s  %s\n' \
  92856c88e45541bc9f4e6e776e8d8bf936202faa298e4e4a50ba7901ccfe8095 \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-comparison.png \
  | sha256sum -c -
test "$(xxd -p -l 8 \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png)" = \
  "89504e470d0a1a0a"
test "$(identify -format '%m %wx%h' \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png)" = \
  "PNG 1024x1536"
test ! -e \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
git diff --quiet
git diff --cached --quiet
```

Expected: both C sources exist, are byte-identical, have the pinned digest,
PNG signature, and exact dimensions; the comparison has its pinned digest;
the destination is still absent; and tracked and staged state is clean. Do not
attempt payload recovery or image generation because the authoritative PNG is
present and verified.

- [ ] **Step 3: Copy the selected PNG without transformation or clobbering**

Run immediately after the absence check:

```bash
set -euo pipefail
test ! -e \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
cp --update=none-fail -- \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
cmp --silent \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
```

Expected: the new destination exists and `cmp` exits zero. Do not resize,
recompress, composite, color-convert, normalize metadata, or remove either
source.

- [ ] **Step 4: Replace the v1.7 README with the contract-complete text**

Use `apply_patch` to replace `akari-v1.7/README.md` with exactly:

```markdown
# Akari v1.7 Intimate Baseline and Hairpin-Side Checkpoints

Status: V17-01 front baseline, V17-02 hairpin-side 30-degree checkpoint, and
V17-03 hairpin-side 45-degree checkpoint promoted.

Date: 2026-08-02.

Akari v1.7 restarts from the accepted v1.5 B3 body balance and restores the
intimate childhood-friend appeal through a restrained expression change. The
user-selected `V17-01 B / Slightly Happy` image is the sole current v1.7
front-view authority. The user-selected
`V17-02 r02 A / hairpin-side 30-degree continuity` image is the accepted
character-left hairpin-side 30-degree continuity authority. The user-selected
`V17-03 r02 C / hairpin-side 45-degree continuity` image is the accepted
character-left hairpin-side 45-degree continuity authority for its selected
fixed moment.

## Accepted Checkpoints

- `accepted/base/akari-v1.7-v17-01-intimate-front.png` — promoted V17-01
  front image, copied byte-for-byte from the selected review output.
- `accepted/base/akari-v1.7-v17-02-hairpin-side-30.png` — promoted V17-02
  hairpin-side 30-degree image, copied byte-for-byte from the selected review
  output.
- `accepted/base/akari-v1.7-v17-03-hairpin-side-45.png` — promoted V17-03
  hairpin-side 45-degree image, copied byte-for-byte from the selected review
  output.
- `selection.md` — shared selection history, lineage, review results, hashes,
  and promotion verification.

The baseline preserves Akari's adult age-25 identity, short airy chestnut bob,
amber eyes, pale-blue crossed ornament, v1.5 B3 body balance, white T-shirt,
pale-blue lounge shorts, warm apartment light, and hand-painted finish. Its
small closed-mouth smile reads as quiet happiness after noticing the familiar
viewer.

The 30-degree checkpoint preserves the accepted identity, adult age,
expression, hair, ornament, body volume, neutral stance, roomwear, and
presentation while adding only the character-left hairpin-side 30-degree
continuity view.

The 45-degree checkpoint preserves the selected age-25 identity, quiet
expression, fixed 45-degree moment, corrected chest-to-waist volume, relaxed
T-shirt drape, neutral stance, hair, ornament, room, light, and finish.

These remain character-design checkpoints, not a paired opposite-side set,
complete turnaround, release package, manifest-backed workflow, wardrobe
redesign, or PDF. No v1.6 image or design element has positive inheritance
authority in v1.7.
```

Expected: the heading is plural, the top-level date is 2026-08-02, all three
accepted checkpoints and their distinct authority roles are present, the
obsolete lack-of-45-degree statement is gone, and the non-goal and v1.6
boundaries remain explicit.

- [ ] **Step 5: Extend the shared selection history without rewriting earlier events**

Use `apply_patch` on `akari-v1.7/selection.md` to replace only the opening
date line:

```diff
-Date: 2026-07-31.
+Original selection-history date: 2026-07-31.
+
+Updated: 2026-08-02.
```

Append exactly this section after the existing V17-02 promotion verification:

```markdown

## V17-03 Hairpin-Side 45-Degree Selection

Selection date: 2026-08-01.

### V17-03 Promoted Result

**r02 C / hairpin-side 45-degree continuity is the explicit user choice.**

The user explicitly selected r02 C. Candidates A and C passed all seven hard
gates. Candidate B failed Gate 3 because it did not complete the mandatory
body correction. Among the passing candidates, the quality order was C then
A.

C gives the strongest balance of complete localized correction, natural adult
volume, same-person read, and finished image quality. It corrected the rounder
near-side bust projection, newly stronger under-bust definition, narrowed
waist, and tight T-shirt fall while preserving the fixed 45-degree view and
every out-of-scope attribute.

### V17-03 Authority and Provenance

- Accepted destination:
  `accepted/base/akari-v1.7-v17-03-hairpin-side-45.png`.
- Ignored review source:
  `/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02/build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png`.
- Authoritative generated source:
  `/home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png`.
- Outer request ID: `call_rd98V3j0ikTsdm1c3h04392x`.
- Completed generation ID:
  `exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4`.
- Immutable prompt SHA-256:
  `19459cdff592ecb59a32dbce7f082f233e96e66e5a74a1383ef678773e9c572c`.
- Review comparison SHA-256:
  `92856c88e45541bc9f4e6e776e8d8bf936202faa298e4e4a50ba7901ccfe8095`.

V17-01 remains the sole accepted front-view authority. V17-02 remains the
accepted character-left hairpin-side 30-degree continuity authority. V17-03
is the accepted character-left hairpin-side 45-degree continuity authority
for this selected fixed moment; it does not supersede either earlier asset.

### V17-03 Review Result

C is not recorded as globally flawless. Its slightly stronger eye polish and
compressed cord are the two known r01 A Minor findings; both remain materially
unchanged in C and are not new r02 findings.

The final task and process review returned zero Critical, Important, and Minor
findings, with no eligibility disagreement or tie-break. Candidate B's Gate 3
failure was an expected candidate-level result, not an implementation or
process defect. No repair, composite, r03 generation, or further image edit
followed the selection.

### V17-03 File Hashes

| Role | SHA-256 |
| --- | --- |
| V17-03 selected review source | `bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954` |
| V17-03 authoritative generated source | `bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954` |
| V17-03 accepted destination | `bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954` |

### V17-03 Promotion Verification

The accepted destination was copied without transformation and verified
byte-identical to both the ignored review source and authoritative generated
source. Its PNG signature is `89504e470d0a1a0a`, its dimensions are
`1024 x 1536`, and its SHA-256 is the recorded digest above. Original-detail
inspection confirmed the complete figure, face, torso correction, ornament,
hands, feet, room, and finish remained intact. Both targeted and repository
Markdown lint passed, and bounded precommit Git-scope assertions confirmed
that only the accepted PNG, this selection history, and the v1.7 README
comprise the tracked promotion.
```

Expected: every V17-01 and V17-02 event statement remains unchanged; only the
top metadata distinguishes the original and updated dates. V17-03 records the
2026-08-01 selection, full provenance, gate results, passing quality order,
localized correction, two inherited Minor findings, zero-finding task/process
review, no follow-up edit, and bounded promotion checks.

- [ ] **Step 6: Verify the complete unstaged three-file promotion**

Run:

```bash
set -euo pipefail
cmp --silent \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
cmp --silent \
  /home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
printf '%s  %s\n' \
  bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954 \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png \
  | sha256sum -c -
test "$(xxd -p -l 8 \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png)" = \
  "89504e470d0a1a0a"
test "$(identify -format '%m %wx%h' \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png)" = \
  "PNG 1024x1536"
/home/takahiro/workspace/akari-design/node_modules/.bin/markdownlint-cli2 \
  --no-globs akari-v1.7/README.md akari-v1.7/selection.md
bash -lc \
  'cd /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02 && PATH="/home/takahiro/workspace/akari-design/node_modules/.bin:$PATH" npm run lint:md'
git diff --check
test -z "$(git diff --cached --name-only)"
promotion_unstaged_scope="$(
  {
    git diff --name-only
    git ls-files --others --exclude-standard
  } | sort
)"
promotion_expected_scope="$(
  printf '%s\n' \
    akari-v1.7/README.md \
    akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png \
    akari-v1.7/selection.md \
    | sort
)"
test "$promotion_unstaged_scope" = "$promotion_expected_scope"
test -z "$(git ls-files -- \
  build/v1.7-hairpin-45-continuity-r02)"
git status --short
```

Expected complete changed scope before staging is exactly:

```text
akari-v1.7/README.md
akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
akari-v1.7/selection.md
```

Both lint commands, byte/hash/signature/dimension checks, `git diff --check`,
and the exact string-equality scope assertion must pass. No file under the
ignored review build directory may be tracked.

- [ ] **Step 7: Inspect the accepted destination at original detail**

Use `view_image` with `detail: original` on:

`/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02/akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png`

Confirm all of the following against the already selected C review result:

- the complete figure is present from hair through both feet;
- face, age-25 identity, quiet expression, hair, and crossed ornament remain
  intact;
- the corrected near-side bust, under-bust, waist, and T-shirt fall are intact;
- hands, neutral stance, room, light, and hand-painted finish contain no copy
  artifact or truncation.

Expected: no visual difference from selected C and no damage introduced by
the byte copy. A failed visual check blocks staging and integration.

- [ ] **Step 8: Stage and commit exactly the three-file promotion**

Run:

```bash
set -euo pipefail
git add \
  akari-v1.7/README.md \
  akari-v1.7/selection.md \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
git diff --cached --check
promotion_staged_scope="$(git diff --cached --name-only | sort)"
promotion_expected_scope="$(
  printf '%s\n' \
    akari-v1.7/README.md \
    akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png \
    akari-v1.7/selection.md \
    | sort
)"
test "$promotion_staged_scope" = "$promotion_expected_scope"
test -z "$(git ls-files -- \
  build/v1.7-hairpin-45-continuity-r02)"
test -z "$(git diff --name-only)"
test -z "$(git ls-files --others --exclude-standard)"
git diff --cached --stat
git diff --cached -- \
  akari-v1.7/README.md akari-v1.7/selection.md
git commit -m "feat: promote v1.7 hairpin 45-degree view"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
promotion_commit_scope="$(
  git diff-tree --no-commit-id --name-only -r HEAD | sort
)"
test "$promotion_commit_scope" = "$promotion_expected_scope"
git status --short --branch
```

Expected: the staged and committed path sets are exactly the three paths, the
commit message is `feat: promote v1.7 hairpin 45-degree view`, and the tracked,
staged, and non-ignored untracked state is clean. Report the full commit hash
without pushing, merging, or removing a worktree.

---

### Task 2: Independently review the promotion commit

**Files:**

- Read:
  `docs/superpowers/specs/2026-08-02-akari-v1-7-hairpin-45-promotion-design.md`
- Read:
  `docs/superpowers/plans/2026-08-02-akari-v1-7-hairpin-45-promotion.md`
- Review: `akari-v1.7/README.md`
- Review: `akari-v1.7/selection.md`
- Review:
  `akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png`

**Interfaces:**

- Consumes: the completed r02 promotion commit and its two pinned sources.
- Produces: an untracked reviewer verdict with severity counts, an explicit
  integrate-or-block decision, and `v17_reviewed_commit`, the exact
  40-character commit SHA from the Ready verdict. The controller retains that
  value without recomputing it from a branch; review produces no repository
  mutation.

- [ ] **Step 1: Reproduce the mechanical promotion checks read-only**

Run in the r02 worktree:

```bash
set -euo pipefail
test "$(git branch --show-current)" = \
  "codex/akari-v1-7-hairpin-45-continuity-r02"
test "$(git log -1 --format=%s)" = \
  "feat: promote v1.7 hairpin 45-degree view"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
review_target_commit="$(git rev-parse HEAD)"
[[ "$review_target_commit" =~ ^[0-9a-f]{40}$ ]]
printf 'Review target commit: %s\n' "$review_target_commit"
review_expected_scope="$(
  printf '%s\n' \
    akari-v1.7/README.md \
    akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png \
    akari-v1.7/selection.md \
    | sort
)"
review_commit_scope="$(
  git diff-tree --no-commit-id --name-only -r \
    "$review_target_commit" \
    | sort
)"
test "$review_commit_scope" = "$review_expected_scope"
cmp --silent \
  build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
cmp --silent \
  /home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
printf '%s  %s\n' \
  bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954 \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png \
  | sha256sum -c -
test "$(xxd -p -l 8 \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png)" = \
  "89504e470d0a1a0a"
test "$(identify -format '%m %wx%h' \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png)" = \
  "PNG 1024x1536"
```

Expected: the branch and commit identity are exact, the checkout is clean, the
command prints one full 40-character review-target SHA, the commit changes
exactly three paths, and the accepted image remains the pinned source bytes.

- [ ] **Step 2: Review provenance, document truth, and original-detail image quality**

Read the complete design, plan, README, and selection history. Use
`view_image` with `detail: original` on the accepted destination. Confirm:

- request ID, generation ID, prompt hash, comparison hash, source paths, and
  all three image hashes match the approved design;
- V17-01, V17-02, and V17-03 retain distinct authority roles;
- A/C passing status, B's candidate-level Gate 3 failure, C-first quality
  order, correction rationale, two inherited Minor image findings, and final
  task/process zero-finding result are all stated without contradiction;
- no text claims a paired set, complete turnaround, manifest-backed release,
  wardrobe redesign, PDF, global flawlessness, remote synchronization, merged
  verification, or completed cleanup;
- the whole figure and all original-detail regions named in Task 1 remain
  intact.

The reviewer must begin the report with `Reviewed commit SHA:` followed by the
exact 40-character value printed as `Review target commit` in Step 1. The
remaining report format is:

```text
Critical: 0
Important: 0
Minor: 0
Scope: exact three-file promotion
Provenance: verified
Byte identity: verified
Verdict: Ready for fast-forward integration
```

Use `Minor: 0` when no Minor finding exists; otherwise report the observed
non-negative integer on that line. Do not write or track the report in the
repository.

- [ ] **Step 3: Resolve any blocking review finding before integration**

If Critical or Important is nonzero, do not integrate. If the finding concerns
README or selection wording, change only those allowed Markdown files with
`apply_patch`, then rerun the two lint commands,
`git diff --check`, the byte/hash/signature/dimension checks, and the
original-detail inspection. Stage only the changed allowed Markdown files and
run:

```bash
set -euo pipefail
git add akari-v1.7/README.md akari-v1.7/selection.md
test -z "$(git diff --name-only)"
test -z "$(git ls-files --others --exclude-standard)"
test -n "$(git diff --cached --name-only)"
test -z "$(git diff --cached --name-only | sed \
  -e '/^akari-v1\.7\/README\.md$/d' \
  -e '/^akari-v1\.7\/selection\.md$/d')"
git commit --amend --no-edit
test -z "$(git status --porcelain=v1 --untracked-files=all)"
amended_expected_scope="$(
  printf '%s\n' \
    akari-v1.7/README.md \
    akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png \
    akari-v1.7/selection.md \
    | sort
)"
amended_commit_scope="$(
  git diff-tree --no-commit-id --name-only -r HEAD | sort
)"
test "$amended_commit_scope" = "$amended_expected_scope"
```

Then repeat the independent review from Step 1 against the amended commit.
Proceed only when Critical and Important are both zero. A Minor must be
reported accurately and must not contradict the approved promotion contract.
Replace the controller's retained `v17_reviewed_commit` with the new full SHA
from the repeated Ready verdict; an earlier SHA is no longer eligible for
integration.

If the finding concerns image bytes, source provenance, or an unexpected path,
stop without overwriting, regenerating, amending, integrating, or cleaning up;
reconcile that state separately.

---

### Task 3: Fast-forward local main and verify the merged result

**Files:**

- Verify:
  `akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png`
- Verify: `akari-v1.7/README.md`
- Verify: `akari-v1.7/selection.md`
- Verify: all six V17-03 design and plan documents listed in Step 3

**Interfaces:**

- Consumes: a clean reviewed r02 branch with zero Critical and zero Important
  findings, the exact reviewer-reported `v17_reviewed_commit` value, and a
  clean local `main` still at that commit's parent.
- Produces: local `main` fast-forwarded to the exact reviewed commit, with
  merged byte, document, scope, and history verification. It does not push.

For every Task 3 shell block, the controller must inject the exact
reviewer-reported 40-character SHA as the `v17_reviewed_commit` environment
variable. Never derive or replace this value from the mutable r02 branch after
review.

- [ ] **Step 1: Prove a fast-forward-only integration is still possible**

Run from `/home/takahiro/workspace/akari-design`:

```bash
set -euo pipefail
: "${v17_reviewed_commit:?supply the reviewer-reported full commit SHA}"
[[ "$v17_reviewed_commit" =~ ^[0-9a-f]{40}$ ]]
test "$(pwd -P)" = \
  "/home/takahiro/workspace/akari-design"
test "$(git branch --show-current)" = "main"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
test -z "$(git -C \
  /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02 \
  status --porcelain=v1 --untracked-files=all)"
test "$(git rev-parse \
  codex/akari-v1-7-hairpin-45-continuity-r02)" = \
  "$v17_reviewed_commit"
v17_promotion_parent="$(git rev-parse "${v17_reviewed_commit}^")"
test "$(git rev-parse main)" = "$v17_promotion_parent"
git merge-base --is-ancestor main "$v17_reviewed_commit"
```

Expected: both checkouts are clean, local `main` is exactly the promotion
commit's parent, and Git proves the reviewed tip is a descendant. Any mismatch
blocks integration and cleanup.

- [ ] **Step 2: Fast-forward local main to the reviewed promotion commit**

Run:

```bash
set -euo pipefail
: "${v17_reviewed_commit:?supply the reviewer-reported full commit SHA}"
[[ "$v17_reviewed_commit" =~ ^[0-9a-f]{40}$ ]]
test "$(git rev-parse \
  codex/akari-v1-7-hairpin-45-continuity-r02)" = \
  "$v17_reviewed_commit"
git merge --ff-only "$v17_reviewed_commit"
test "$(git rev-parse HEAD)" = "$v17_reviewed_commit"
test "$(git log -1 --format=%s)" = \
  "feat: promote v1.7 hairpin 45-degree view"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

Expected: `main` moves by fast-forward only to the exact reviewed commit and
remains clean. Do not pull, push, rebase, squash, or create a merge commit.

- [ ] **Step 3: Prove every V17-03 design, plan, and promotion commit is on main**

Run:

```bash
set -euo pipefail
: "${v17_reviewed_commit:?supply the reviewer-reported full commit SHA}"
[[ "$v17_reviewed_commit" =~ ^[0-9a-f]{40}$ ]]
for v17_history_path in \
  docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-45-continuity-design.md \
  docs/superpowers/plans/2026-07-31-akari-v1-7-hairpin-45-continuity.md \
  docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-45-continuity-r02-design.md \
  docs/superpowers/plans/2026-07-31-akari-v1-7-hairpin-45-continuity-r02.md \
  docs/superpowers/specs/2026-08-02-akari-v1-7-hairpin-45-promotion-design.md \
  docs/superpowers/plans/2026-08-02-akari-v1-7-hairpin-45-promotion.md
do
  test -f "$v17_history_path"
  v17_history_commit="$(git log -1 --format=%H -- "$v17_history_path")"
  test -n "$v17_history_commit"
  git merge-base --is-ancestor "$v17_history_commit" main
done
test "$(git rev-parse \
  codex/akari-v1-7-hairpin-45-continuity-r02)" = \
  "$v17_reviewed_commit"
git merge-base --is-ancestor "$v17_reviewed_commit" main
test "$(git rev-parse main)" = "$v17_reviewed_commit"
```

Expected: each V17-03 design/plan file exists, the commit that introduced or
last changed it is an ancestor of `main`, and the reviewed promotion commit is
the current `main` tip.

- [ ] **Step 4: Re-run byte, image, Markdown, and commit-scope checks from main**

Run:

```bash
set -euo pipefail
: "${v17_reviewed_commit:?supply the reviewer-reported full commit SHA}"
[[ "$v17_reviewed_commit" =~ ^[0-9a-f]{40}$ ]]
test "$(git branch --show-current)" = "main"
test "$(git rev-parse HEAD)" = "$v17_reviewed_commit"
test "$(git rev-parse \
  codex/akari-v1-7-hairpin-45-continuity-r02)" = \
  "$v17_reviewed_commit"
cmp --silent \
  /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02/build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
cmp --silent \
  /home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
printf '%s  %s\n' \
  bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954 \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png \
  | sha256sum -c -
test "$(xxd -p -l 8 \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png)" = \
  "89504e470d0a1a0a"
test "$(identify -format '%m %wx%h' \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png)" = \
  "PNG 1024x1536"
/home/takahiro/workspace/akari-design/node_modules/.bin/markdownlint-cli2 \
  --no-globs akari-v1.7/README.md akari-v1.7/selection.md
bash -lc \
  'cd /home/takahiro/workspace/akari-design && npm run lint:md'
git diff --check
test -z "$(git status --porcelain=v1 --untracked-files=all)"
merged_expected_scope="$(
  printf '%s\n' \
    akari-v1.7/README.md \
    akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png \
    akari-v1.7/selection.md \
    | sort
)"
merged_promotion_scope="$(
  git diff-tree --no-commit-id --name-only -r \
    "$v17_reviewed_commit" \
    | sort
)"
test "$merged_promotion_scope" = "$merged_expected_scope"
test -z "$(git ls-files -- \
  build/v1.7-hairpin-45-continuity-r02)"
```

Expected: the merged accepted destination is byte-identical to both surviving
sources, all image invariants and both Markdown lint commands pass, the merged
checkout is clean, and the promotion commit contains exactly the three
approved paths.

- [ ] **Step 5: Inspect the merged destination at original detail**

Use `view_image` with `detail: original` on:

`/home/takahiro/workspace/akari-design/akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png`

Repeat the complete-figure, face, torso correction, ornament, hands, feet,
room, light, and finish inspection from Task 1. Expected: the merged main image
is visually identical to selected C. A failed inspection blocks cleanup.

---

### Task 4: Remove only the completed V17-03 worktrees and branches

**Files:**

- Preserve:
  `/home/takahiro/workspace/akari-design/akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png`
- Preserve:
  `/home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png`
- Remove exact worktree:
  `/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity`
- Remove exact worktree:
  `/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02`

**Interfaces:**

- Consumes: verified local `main`, two clean named worktrees, two branch tips
  proven ancestors of `main`, and surviving accepted/generated C bytes outside
  the removable worktrees.
- Produces: the same verified local `main` with only the two named worktree
  registrations/directories and their safely merged local branches removed.

- [ ] **Step 1: Run every cleanup precondition before any removal**

Run the entire block from `/home/takahiro/workspace/akari-design`:

```bash
set -euo pipefail
test "$(pwd -P)" = \
  "/home/takahiro/workspace/akari-design"
test "$(git branch --show-current)" = "main"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
test -f \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
test -f \
  /home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png
cmp --silent \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png \
  /home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png
printf '%s  %s\n' \
  bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954 \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png \
  | sha256sum -c -
test "$(git worktree list --porcelain | awk '
  $1 == "worktree" { worktree_path = $2 }
  $1 == "branch" && worktree_path == \
    "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity" {
    print $2
  }
')" = "refs/heads/codex/akari-v1-7-hairpin-45-continuity"
test "$(git worktree list --porcelain | awk '
  $1 == "worktree" { worktree_path = $2 }
  $1 == "branch" && worktree_path == \
    "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02" {
    print $2
  }
')" = "refs/heads/codex/akari-v1-7-hairpin-45-continuity-r02"
test -z "$(git -C \
  /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity \
  status --porcelain=v1 --untracked-files=all)"
test -z "$(git -C \
  /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02 \
  status --porcelain=v1 --untracked-files=all)"
git merge-base --is-ancestor \
  codex/akari-v1-7-hairpin-45-continuity main
git merge-base --is-ancestor \
  codex/akari-v1-7-hairpin-45-continuity-r02 main
test "$(git rev-parse main)" = \
  "$(git rev-parse codex/akari-v1-7-hairpin-45-continuity-r02)"
```

Expected: the accepted and authoritative generated files survive outside both
worktrees and remain byte-identical with the required digest; porcelain maps
both exact paths to both expected branches; tracked, staged, and non-ignored
untracked state is clean in all three checkouts; both branch tips are
ancestors of verified local `main`; and the r02 tip equals `main`. If any
command fails, stop with both worktrees and branches intact.

- [ ] **Step 2: Snapshot unrelated worktrees, remove the exact targets, and safely delete their branches**

Only after Step 1 passes, run this entire block without substituting variables
into any destructive target:

```bash
set -euo pipefail
v17_unrelated_worktrees_before="$(git worktree list --porcelain | awk \
  -v RS='' -v ORS='\n\n' '
    $0 !~ /worktree \/home\/takahiro\/workspace\/akari-design\/\.worktrees\/akari-v1-7-hairpin-45-continuity(\n|$)/ &&
    $0 !~ /worktree \/home\/takahiro\/workspace\/akari-design\/\.worktrees\/akari-v1-7-hairpin-45-continuity-r02(\n|$)/ {
      print
    }
  ')"
git worktree remove --force \
  /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity
git worktree remove --force \
  /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02
git branch -d codex/akari-v1-7-hairpin-45-continuity
git branch -d codex/akari-v1-7-hairpin-45-continuity-r02
v17_unrelated_worktrees_after="$(git worktree list --porcelain | awk \
  -v RS='' -v ORS='\n\n' '
    $0 !~ /worktree \/home\/takahiro\/workspace\/akari-design\/\.worktrees\/akari-v1-7-hairpin-45-continuity(\n|$)/ &&
    $0 !~ /worktree \/home\/takahiro\/workspace\/akari-design\/\.worktrees\/akari-v1-7-hairpin-45-continuity-r02(\n|$)/ {
      print
    }
  ')"
test "$v17_unrelated_worktrees_after" = \
  "$v17_unrelated_worktrees_before"
```

Expected: only the exact r01/r02 worktree directories and registrations are
removed. Their known ignored candidate, comparison, crop, and local SDD scratch
files are intentionally deleted. Both local branches delete through safe
merged-branch checks, and the unrelated worktree snapshot is byte-for-byte
unchanged. If a removal command unexpectedly fails after cleanup starts, stop
and report the exact partial state; do not broaden or repeat cleanup with a
different target.

- [ ] **Step 3: Verify final repository state and source survival**

Run:

```bash
set -euo pipefail
test ! -e \
  /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity
test ! -e \
  /home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02
test -z "$(git branch --list \
  codex/akari-v1-7-hairpin-45-continuity)"
test -z "$(git branch --list \
  codex/akari-v1-7-hairpin-45-continuity-r02)"
test -f \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png
test -f \
  /home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png
cmp --silent \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png \
  /home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png
printf '%s  %s\n' \
  bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954 \
  akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png \
  | sha256sum -c -
test "$(git branch --show-current)" = "main"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
git status --short --branch
git worktree list --porcelain
```

Expected: both target worktrees and branches are gone, accepted C and the
authoritative generated source remain byte-identical with the pinned digest,
local `main` is clean at the verified promotion commit, and every unrelated
worktree is still registered. Report the promotion commit, review verdict,
merged verification, removed exact targets, final `main` status, and that no
push occurred.
