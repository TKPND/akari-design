# Akari v1.7 Baseline Promotion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote the selected V17-01 B PNG byte-for-byte into a minimal,
tracked Akari v1.7 front-baseline package.

**Architecture:** Treat the ignored selected PNG as an immutable promotion
source, copy it once into `akari-v1.7/accepted/base/`, and record the decision
and lineage in two focused Markdown files. Reconcile the completed outcome in
the earlier design document, then prove byte identity, hashes, image validity,
and Markdown quality without running unrelated test or release suites.

**Tech Stack:** POSIX shell, `cp`, `cmp`, `xxd`, ImageMagick `identify`,
SHA-256, Markdown, markdownlint-cli2, Git, and local `view_image`.

## Global Constraints

- Follow
  `docs/superpowers/specs/2026-07-31-akari-v1-7-baseline-promotion-design.md`.
- The exact source is
  `build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png`.
- The selected source and promoted destination must both have SHA-256
  `64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8`.
- The v1.5 B3 lineage source must retain SHA-256
  `e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734`.
- Copy the selected PNG byte-for-byte. Do not resize, re-encode, optimize,
  recolor, crop, or process it through an image editor.
- Create only the minimal `README.md`, accepted PNG, and `selection.md` under
  `akari-v1.7/`, plus the required status reconciliation in the earlier v1.7
  design document.
- Do not promote A, C, or the comparison image. Do not create a manifest,
  release package, PDF, turnaround, or angle asset.
- Do not generate images or run Python tests, Node tests, PDF builds, OCR, or
  release gates.
- Do not delete or modify ignored review output, v1.6 material, or existing
  worktrees.
- Do not push, merge, clean up branches, or synchronize remotes.

---

### Task 1: Promote and verify the V17-01 front baseline

**Files:**

- Read:
  `docs/superpowers/specs/2026-07-31-akari-v1-7-baseline-promotion-design.md`
- Read:
  `build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png`
- Read:
  `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`
- Create: `akari-v1.7/README.md`
- Create:
  `akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`
- Create: `akari-v1.7/selection.md`
- Modify:
  `docs/superpowers/specs/2026-07-31-akari-v1-7-intimate-baseline-design.md`

**Interfaces:**

- Consumes: one selected `1024 x 1536` PNG, its recorded user selection and
  final review, and the accepted v1.5 B3 lineage file.
- Produces: one byte-identical tracked front authority plus durable package
  and selection metadata for later v1.7 angle designs.

- [ ] **Step 1: Verify immutable preconditions**

Run:

```bash
test "$(sha256sum \
  build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png \
  | cut -d ' ' -f 1)" = \
  "64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8"
test "$(sha256sum \
  akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png \
  | cut -d ' ' -f 1)" = \
  "e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734"
test "$(xxd -p -l 8 \
  build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png)" = \
  "89504e470d0a1a0a"
identify -format '%m %wx%h\n' \
  build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png
git status --short --branch
```

Expected:

- both `test` commands exit zero;
- the selected source has the PNG signature;
- `identify` prints `PNG 1024x1536`;
- the tracked worktree is clean before promotion.

- [ ] **Step 2: Copy the selected PNG without transformation**

Run:

```bash
mkdir -p akari-v1.7/accepted/base
cp -- \
  build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png
```

Expected: the destination exists as a regular PNG file. Do not open and save
it through an image editor.

- [ ] **Step 3: Add the package README**

Create `akari-v1.7/README.md` with exactly:

```markdown
# Akari v1.7 Intimate Baseline

Status: V17-01 front baseline promoted.

Date: 2026-07-31.

Akari v1.7 restarts from the accepted v1.5 B3 body balance and restores the
intimate childhood-friend appeal through a restrained expression change. The
user-selected `V17-01 B / Slightly Happy` image is the sole current v1.7
front-view authority.

## Accepted Baseline

- `accepted/base/akari-v1.7-v17-01-intimate-front.png` — promoted V17-01
  front image, copied byte-for-byte from the selected review output.
- `selection.md` — selection, lineage, review result, hashes, and promotion
  verification.

The baseline preserves Akari's adult age-25 identity, short airy chestnut bob,
amber eyes, pale-blue crossed ornament, v1.5 B3 body balance, white T-shirt,
pale-blue lounge shorts, warm apartment light, and hand-painted finish. Its
small closed-mouth smile reads as quiet happiness after noticing the familiar
viewer.

This is a character-design checkpoint, not a release package, manifest-backed
turnaround, wardrobe redesign, or PDF. No v1.6 image or design element has
positive inheritance authority in v1.7.
```

- [ ] **Step 4: Add the durable selection record**

Create `akari-v1.7/selection.md` with exactly:

```markdown
# Akari v1.7 — V17-01 Intimate Front Selection

Date: 2026-07-31.

## Promoted Result

**B / Slightly Happy is the accepted V17-01 front baseline.**

The user explicitly selected B after reviewing v1.5 B3 and V17-01 candidates
A, B, and C at equal scale. B gives the clearest restrained improvement toward
the approved intimate-childhood-friend direction while preserving the same
adult identity, hair, ornament, body balance, outfit, apartment, and
hand-painted finish.

Candidate C was not selected because its intended one-corner mouth response
was not reliably distinguishable from B at full-body scale. The planned
no-correction boundary remained in force, so no follow-up candidate generation
was performed.

## Authority and Lineage

- Current front authority:
  `accepted/base/akari-v1.7-v17-01-intimate-front.png`.
- Promotion source:
  `build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png`.
- Upstream body-balance lineage:
  `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`.
- No v1.6 asset, prompt, proportion, accessory, outfit, palette, or manifest
  has positive inheritance authority.

## Review Result

The final independent review returned `READY` with zero Critical and zero
Important findings. Incidental whole-frame stroke and texture rerendering was
classified as a Minor difference allowed by the approved V17-01 design.

## File Hashes

| Role | SHA-256 |
| --- | --- |
| v1.7 V17-01 accepted front | `64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8` |
| v1.5 B3 lineage source | `e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734` |

## Promotion Verification

The accepted PNG was copied without transformation. Its PNG signature,
`1024 x 1536` dimensions, SHA-256, and byte identity against the selected
review source were verified during promotion.
```

- [ ] **Step 5: Reconcile the completed outcome in the earlier design**

In
`docs/superpowers/specs/2026-07-31-akari-v1-7-intimate-baseline-design.md`,
replace:

```markdown
Status: approved design, awaiting written-spec review.
```

with:

```markdown
Status: complete.
```

Then insert this section immediately after `Date: 2026-07-31.`:

```markdown
## Outcome

- The design was approved and candidate B / Slightly Happy was explicitly
  selected as the V17-01 working baseline.
- The final independent review returned `READY` with zero Critical and zero
  Important findings.
- The selected PNG was promoted byte-for-byte to
  `akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png`.
```

Do not change the historical candidate matrix, generation boundaries,
acceptance rules, or non-goals elsewhere in that document.

- [ ] **Step 6: Prove image validity and byte identity**

Run:

```bash
test "$(xxd -p -l 8 \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png)" = \
  "89504e470d0a1a0a"
identify -format '%m %wx%h\n' \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png
cmp -- \
  build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png
sha256sum \
  build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
  akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png
```

Expected:

- the destination signature check and `cmp` exit zero;
- `identify` prints `PNG 1024x1536`;
- source and destination both print the selected v1.7 digest;
- B3 prints the recorded lineage digest.

Open
`akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png` with
`view_image` at original detail. Confirm that it is the selected quietly
pleased B image with complete face, hair ornament, hands, legs, and bare feet,
and that it has no text, border, watermark, or visible corruption.

- [ ] **Step 7: Validate Markdown and the exact tracked scope**

Run:

```bash
./node_modules/.bin/markdownlint-cli2 \
  akari-v1.7/README.md \
  akari-v1.7/selection.md \
  docs/superpowers/specs/2026-07-31-akari-v1-7-intimate-baseline-design.md
npm run lint:md
git diff --check
git status --short
```

Expected:

- both Markdown lint commands report zero issues;
- `git diff --check` reports no whitespace errors;
- status shows only the new `akari-v1.7/` package and the intended earlier
  design status update.

Do not substitute Python, Node test, PDF, OCR, or release commands for this
bounded verification.

- [ ] **Step 8: Stage, inspect, and commit the promotion**

Run:

```bash
git add \
  akari-v1.7/README.md \
  akari-v1.7/accepted/base/akari-v1.7-v17-01-intimate-front.png \
  akari-v1.7/selection.md \
  docs/superpowers/specs/2026-07-31-akari-v1-7-intimate-baseline-design.md
git diff --cached --check
git diff --cached --stat
git status --short
git commit -m "Promote Akari v1.7 V17-01 baseline"
```

Expected:

- the staged diff contains exactly three new package files and one status
  update;
- the commit succeeds with no unrelated files;
- the ignored `build/` source remains present and unchanged.
