# Akari v1.7 V17-02 Hairpin-Side 30-Degree Promotion Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote the user-selected V17-02 r02 A PNG byte-for-byte into the
minimal tracked v1.7 checkpoint and record its authority, review, hashes, and
known Minor findings.

**Architecture:** Work in the existing isolated V17-02 worktree that contains
the ignored reviewed source. Add one semantic accepted PNG under the existing
`accepted/base/` structure, extend the package README and shared selection
history, run bounded asset/document verification, and commit exactly those
three package files.

**Tech Stack:** POSIX shell, `cp`, `cmp`, `sha256sum`, `xxd`, ImageMagick
`identify`, `view_image`, Markdown lint, and Git.

## Global Constraints

- Follow
  `docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-30-promotion-design.md`.
- Execute only in
  `/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-30-continuity`
  after the controller fast-forwards it to the committed promotion design and
  plan.
- Promotion source:
  `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png`.
- Source and destination must both have SHA-256
  `22aee4f2bcd9863b2c22c0e58b191cf767521576c0ffb11ed11208f3bd917749`.
- Destination:
  `akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png`.
- Change exactly the destination PNG, `akari-v1.7/README.md`, and
  `akari-v1.7/selection.md`.
- Preserve V17-01 as sole front-view authority and V17-02 as hairpin-side
  30-degree authority.
- Preserve A's two Minor findings in the durable selection history.
- Do not add review candidates, comparisons, local selection notes, task
  reports, manifests, validators, PDFs, release files, or other versions.
- Do not run Node tests, Python tests, package validation, PDF builds, OCR,
  integration gates, or release gates.
- Do not push. The controller owns final review, local fast-forward merge,
  merged-result verification, and worktree/branch cleanup.

---

### Task 1: Promote V17-02 r02 A into the v1.7 checkpoint

**Files:**

- Read:
  `docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-30-promotion-design.md`
- Read:
  `build/v1.7-hairpin-30-continuity/V17-02-R02-SELECTION.md`
- Read source:
  `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png`
- Create:
  `akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png`
- Modify: `akari-v1.7/README.md`
- Modify: `akari-v1.7/selection.md`

**Interfaces:**

- Consumes: one ignored, hash-pinned, user-selected review PNG plus its local
  selection evidence.
- Produces: one tracked accepted PNG and two tracked documentation updates in
  one atomic commit.

- [ ] **Step 1: Verify checkout, source evidence, and clean tracked state**

Run:

```bash
test "$(pwd -P)" = \
  "/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-30-continuity"
test -f \
  docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-30-promotion-design.md
test -f \
  docs/superpowers/plans/2026-07-31-akari-v1-7-hairpin-30-promotion.md
git cat-file -e \
  HEAD:docs/superpowers/specs/2026-07-31-akari-v1-7-hairpin-30-promotion-design.md
git cat-file -e \
  HEAD:docs/superpowers/plans/2026-07-31-akari-v1-7-hairpin-30-promotion.md
test -f build/v1.7-hairpin-30-continuity/V17-02-R02-SELECTION.md
test "$(xxd -p -l 8 \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png)" = \
  "89504e470d0a1a0a"
test "$(identify -format '%m %wx%h' \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png)" = \
  "PNG 1024x1536"
printf '%s  %s\n' \
  22aee4f2bcd9863b2c22c0e58b191cf767521576c0ffb11ed11208f3bd917749 \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png \
  | sha256sum -c -
git diff --quiet
git diff --cached --quiet
git status --short --branch
```

Expected: both promotion documents exist in `HEAD`, the local selection record
exists, source signature, exact dimensions, and hash pass, and tracked and
staged diffs are empty.

- [ ] **Step 2: Copy the selected PNG without transformation**

Run:

```bash
mkdir -p akari-v1.7/accepted/base
cp \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png
cmp --silent \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png
```

Expected: destination exists and `cmp` exits zero. Do not resize, recompress,
rename through an image converter, composite, or remove the ignored source.

- [ ] **Step 3: Update the v1.7 README**

Use `apply_patch` on `akari-v1.7/README.md` so it:

- changes status from V17-01-only promotion to V17-01 and V17-02 promoted;
- retains the intimate-baseline explanation and V17-01 sole front authority;
- adds V17-02 as accepted character-left hairpin-side 30-degree continuity
  authority;
- lists the semantic V17-02 accepted path beside the V17-01 path;
- states the angle checkpoint preserves accepted identity, age, expression,
  hair, ornament, body volume, neutral stance, roomwear, and presentation;
- keeps the checkpoint/not-turnaround/not-release/not-PDF and v1.6-exclusion
  boundaries.

Do not claim that v1.7 now contains a 45-degree view, paired views, a complete
turnaround, or a manifest-backed release.

- [ ] **Step 4: Extend the shared selection history**

Use `apply_patch` on `akari-v1.7/selection.md`. Preserve every existing V17-01
statement, retitle the V17-01-only H1 as a shared Akari v1.7 selection-history
title, and add a clearly separated V17-02 section containing:

- `r02 A / hairpin-side 30-degree continuity` as the explicit user choice;
- accepted destination and exact ignored promotion source;
- accepted-front generation authority and its SHA-256
  `64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8`;
- selected and destination SHA-256
  `22aee4f2bcd9863b2c22c0e58b191cf767521576c0ffb11ed11208f3bd917749`;
- candidate A generation artifact ID
  `exec-28dc8843-3811-4d27-b334-4bbeaf034196`;
- comparison SHA-256
  `8f3a68abc4694363d8abe904698a53c168d3c9750e6799288848acb34b1fa826`;
- the independent review plus blind tie-break and their coherent-camera-orbit
  rationale;
- the two Minor findings from the design;
- B's body-volume rejection and C's view/body/stance/camera-roll rejection;
- the generation implementer's initial all-fail visual adjudication, followed
  by the independent review and blind tie-break that superseded it;
- no automatic repair or r03 generation;
- bounded promotion verification.

The durable record must preserve that initial over-strict adjudication and its
supersession explicitly. Do not describe A as flawless.

- [ ] **Step 5: Verify the complete three-file promotion**

Run:

```bash
cmp --silent \
  build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png
printf '%s  %s\n' \
  22aee4f2bcd9863b2c22c0e58b191cf767521576c0ffb11ed11208f3bd917749 \
  akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png \
  | sha256sum -c -
test "$(xxd -p -l 8 \
  akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png)" = \
  "89504e470d0a1a0a"
test "$(identify -format '%m %wx%h' \
  akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png)" = \
  "PNG 1024x1536"
/home/takahiro/workspace/akari-design/node_modules/.bin/markdownlint-cli2 \
  --no-globs akari-v1.7/README.md akari-v1.7/selection.md
PATH="/home/takahiro/workspace/akari-design/node_modules/.bin:$PATH" \
  npm run lint:md
git diff --check
git diff --name-only
git status --short
promotion_unstaged_scope="$(
  {
    git diff --name-only
    git ls-files --others --exclude-standard -- akari-v1.7
  } | sort
)"
promotion_expected_scope="$(
  printf '%s\n' \
    akari-v1.7/README.md \
    akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png \
    akari-v1.7/selection.md \
    | sort
)"
test "$promotion_unstaged_scope" = "$promotion_expected_scope"
```

Expected complete changed scope before staging is exactly:

```text
akari-v1.7/README.md
akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png
akari-v1.7/selection.md
```

The string-equality assertion must pass. Open the accepted destination with
`view_image` at original detail and confirm the whole figure, face, ornament,
hands, feet, background, and finish are intact.

- [ ] **Step 6: Stage and commit exactly the promotion scope**

Run:

```bash
git add \
  akari-v1.7/README.md \
  akari-v1.7/selection.md \
  akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png
git diff --cached --check
git diff --cached --name-only
promotion_staged_scope="$(git diff --cached --name-only | sort)"
promotion_expected_scope="$(
  printf '%s\n' \
    akari-v1.7/README.md \
    akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png \
    akari-v1.7/selection.md \
    | sort
)"
test "$promotion_staged_scope" = "$promotion_expected_scope"
git commit -m "feat: promote v1.7 hairpin 30-degree view"
git status --short --branch
```

Expected staged scope before commit is exactly:

```text
akari-v1.7/README.md
akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png
akari-v1.7/selection.md
```

Expected after commit: the tracked worktree is clean. Report the commit hash,
all verification results, and any concern. Do not push, merge, or remove the
worktree or branch.
