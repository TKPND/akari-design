# Akari V2.2 GPT Pro Face-Angle Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify a manual-upload GPT Pro package that starts the
three-image Akari V2.2 face-angle workflow with F00 only.

**Architecture:** Keep all working files under one ignored `tmp/` package.
Include exactly one canonical image input, three short gate-specific prompts,
and a decision ledger. Finalize a sanitized timestamped archive under
`Documents/GPT Pro Analysis/`, then stop before any image-generation call.

**Tech Stack:** Markdown and text prompts, shell file inspection, ImageMagick,
SHA-256, tar/gzip, the `gpt-pro-review` finalization script, Markdown lint.

## Global Constraints

- Do not call Codex `image_gen` or any other image-generation tool.
- F00 receives exactly one image input: the accepted canonical V2.2 portrait.
- Do not include the canonical full-body image, rejected or pending candidates,
  old-version angle references, scene images, or the R02 eye-calibration image.
- F01 and F02 remain blocked prompt templates; GPT Pro must generate only F00
  during the first gate.
- Keep prompts short and avoid numerical face redesign.
- Do not promote, edit, or commit generated images or accepted assets.
- The user alone approves identity and pack-local anchor use.
- Do not modify unrelated tracked or untracked workspace changes.

---

### Task 1: Assemble the ignored working package

**Files:**

- Create: `tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/PROMPT.md`
- Create:
  `tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/DECISIONS.md`
- Create:
  `tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/prompts/F00.txt`
- Create:
  `tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/prompts/F01.txt`
- Create:
  `tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/prompts/F02.txt`
- Copy:
  `akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp`
  to
  `tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/reference/01-canonical-portrait.webp`
- Copy:
  `docs/superpowers/specs/2026-08-13-akari-v2-2-gpt-pro-face-angle-pack-design.md`
  to
  `tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/docs/design.md`
- Create: `tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/tree.txt`
- Create: `tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/git-log.txt`
- Create:
  `tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/SHA256SUMS.txt`

**Interfaces:**

- Consumes: the approved design and canonical portrait.
- Produces: a self-contained package directory whose active first gate is F00.

- [ ] **Step 1: Confirm the package destination is ignored and absent**

Run:

```bash
git check-ignore -v \
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/.ignore-probe
test ! -e tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13
```

Expected: `git check-ignore` identifies the repository's `tmp/` rule and the
second command exits zero. If the directory already exists, inspect it and stop
instead of overwriting it.

- [ ] **Step 2: Create the package directories**

Create only these directories:

```text
tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/
  docs/
  prompts/
  reference/
```

Run:

```bash
mkdir -p \
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/docs \
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/prompts \
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/reference
```

- [ ] **Step 3: Write the active GPT Pro map**

Create `PROMPT.md` with this exact content:

```markdown
# Akari V2.2 F00 Close-Face Reference

## Your Role

You are creating one identity-sensitive face reference for the fictional anime
character Akari V2.2.

## Current Gate

Generate F00 only. Do not generate F01, F02, a contact sheet, alternatives, or
extra panels. Stop after one finished image.

## Image Input

Use `reference/01-canonical-portrait.webp` as the only image reference and the
sole authority for Akari's face, eyes, hair, and rendering.

## Task

Use the exact F00 request in `prompts/F00.txt`. Keep the result as one close
head-and-shoulders portrait on a plain background.

## Review Boundary

The output is a candidate only. The user alone decides whether it is Akari and
whether it may become a pack-local relay anchor. A visually polished image is
not automatically approved.

## Exclusions

Do not infer or request any other reference image. Do not redesign the face,
make the eye openings taller, mirror the hair, add a second hairpin, add hands
or props, or include text, labels, borders, and inset panels.

## Output

Return exactly one finished F00 image and no additional variants.
```

- [ ] **Step 4: Write the F00 prompt**

Create `prompts/F00.txt` with this exact content:

```text
Image A is the only reference. Make a close head-and-shoulders reference of the same Akari. Keep Image A's head angle, face, eye proportions, bangs, low side ponytail, and exactly one blue hairpin.

Give her a small closed-mouth smile, a plain white T-shirt, and a warm off-white background. Keep her face large, with no hand or prop.

Generate one finished image only. Do not redesign her face, make her eye openings taller, mirror her hair, or add text or extra panels.
```

- [ ] **Step 5: Write the blocked F01 prompt template**

Create `prompts/F01.txt` with this exact content:

```text
BLOCKED: Do not use this prompt until the user approves F00 identity and explicitly approves F00 as the pack-local relay anchor.

Image A is the canonical Akari portrait. Image B is the user-approved F00 neutral face anchor. Draw the same Akari as a close head-and-shoulders reference, rotating her head about 30 degrees so the blue-hairpin side is the nearer, more visible side.

Keep F00's small closed-mouth smile, plain white T-shirt, warm off-white background, and large face. Use exactly one blue hairpin in its canonical location, with no hand or prop.

Generate one finished image only. Do not redesign her face, make her eye openings taller, mirror her hair, or add text or extra panels.
```

- [ ] **Step 6: Write the blocked F02 prompt template**

Create `prompts/F02.txt` with this exact content:

```text
BLOCKED: Do not use this prompt until the user approves F00 as the pack-local relay anchor and approves F01 identity.

Image A is the canonical Akari portrait. Image B is the user-approved F00 neutral face anchor. Draw the same Akari as a close head-and-shoulders reference, rotating her head about 30 degrees so the side without the blue hairpin is the nearer, more visible side.

Keep F00's small closed-mouth smile, plain white T-shirt, warm off-white background, and large face. The hairpin may be naturally partly hidden, but it must not move, mirror, or duplicate. Include no hand or prop.

Generate one finished image only. Do not redesign her face, make her eye openings taller, or add text or extra panels.
```

- [ ] **Step 7: Write the decision ledger**

Create `DECISIONS.md` with this exact initial state:

```markdown
# Face-Angle Pack Decisions

Date: 2026-08-13

## State

- F00 generation: `ready_for_manual_gpt_pro_call`
- F00 identity: `not_generated`
- F00 relay-anchor use: `blocked_by_identity`
- F01 generation: `blocked_by_F00_identity_and_anchor_approval`
- F02 generation: `blocked_by_F01_identity_approval`
- Repository preservation: `not_requested`
- Global skill update: `not_requested`
- School-day S03 resume: `paused`

## Input Contract

- F00 input: `reference/01-canonical-portrait.webp` only.
- F01/F02 inputs after their gates: canonical portrait plus approved F00 only.
- F01 is never an F02 input.
- Rejected and pending images are never reused.

## User Decisions

No generated face decision has been recorded yet.
```

- [ ] **Step 8: Copy only the approved source files**

Copy the canonical portrait and approved design to their exact package paths.
Do not copy any other image or document.

Run:

```bash
cp -- \
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp \
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/reference/01-canonical-portrait.webp
cp -- \
  docs/superpowers/specs/2026-08-13-akari-v2-2-gpt-pro-face-angle-pack-design.md \
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/docs/design.md
```

- [ ] **Step 9: Generate package metadata**

Write the package tree, the latest ten Git commits, and a SHA-256 entry for the
packaged canonical copy. Keep the hash path relative to the package root so the
archive remains self-verifying after transfer.

Run:

```bash
FACE_PACK_DIR=tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13
git log --oneline -n 10 > "$FACE_PACK_DIR/git-log.txt"
(
  cd "$FACE_PACK_DIR"
  sha256sum reference/01-canonical-portrait.webp > SHA256SUMS.txt
  tree -a -I tree.txt . > tree.txt
)
```

Expected image hash for both canonical paths:

```text
b076afd95be49c4ed9c5a4ddfb4083c9ead8328313b4d5fa0555a374dd10543c
```

Do not commit the ignored working package.

---

### Task 2: Verify content, reference isolation, and safety

**Files:**

- Verify: `tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/`

**Interfaces:**

- Consumes: the Task 1 package directory.
- Produces: a verified package directory safe to pass to the finalizer.

- [ ] **Step 1: Verify the reference count and type**

Run:

```bash
FACE_PACK_REFERENCE_DIR=tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/reference
test "$(find "$FACE_PACK_REFERENCE_DIR" -type f | wc -l)" -eq 1
find "$FACE_PACK_REFERENCE_DIR" -type f -print
identify -format '%f %wx%h %[colorspace]\n' \
  "$FACE_PACK_REFERENCE_DIR/01-canonical-portrait.webp"
```

Expected: exactly one file named `01-canonical-portrait.webp`, reported as
`1888x3344 sRGB`.

- [ ] **Step 2: Verify the canonical copy byte-for-byte**

Run:

```bash
cmp \
  akari-v2.2/accepted/base/akari-v2.2-single-hairpin-portrait.webp \
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/reference/01-canonical-portrait.webp
(
  cd tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13
  sha256sum -c SHA256SUMS.txt
)
```

Expected: `cmp` exits zero and the packaged SHA-256 check reports `OK`.

- [ ] **Step 3: Verify the gate language**

Run fixed-string checks confirming:

- `PROMPT.md` says `Generate F00 only`;
- `F01.txt` begins with `BLOCKED` and requires both F00 identity and anchor
  approval;
- `F02.txt` begins with `BLOCKED` and requires F01 identity approval;
- `DECISIONS.md` keeps F01 and F02 blocked;
- all three prompt files request one finished image only.

Run:

```bash
FACE_PACK_DIR=tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13
rg -F -n 'Generate F00 only' "$FACE_PACK_DIR/PROMPT.md"
rg -F -n \
  'BLOCKED: Do not use this prompt until the user approves F00 identity and explicitly approves F00 as the pack-local relay anchor.' \
  "$FACE_PACK_DIR/prompts/F01.txt"
rg -F -n \
  'BLOCKED: Do not use this prompt until the user approves F00 as the pack-local relay anchor and approves F01 identity.' \
  "$FACE_PACK_DIR/prompts/F02.txt"
rg -F -n \
  'F01 generation: `blocked_by_F00_identity_and_anchor_approval`' \
  "$FACE_PACK_DIR/DECISIONS.md"
rg -F -n \
  'F02 generation: `blocked_by_F01_identity_approval`' \
  "$FACE_PACK_DIR/DECISIONS.md"
test "$(rg -F -l 'Generate one finished image only.' \
  "$FACE_PACK_DIR/prompts/F00.txt" \
  "$FACE_PACK_DIR/prompts/F01.txt" \
  "$FACE_PACK_DIR/prompts/F02.txt" | wc -l)" -eq 3
```

Expected: every required string has exactly the intended file hit.

- [ ] **Step 4: Verify excluded images are absent**

Run:

```bash
find tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13 \
  -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \
  -o -iname '*.webp' \) -print
```

Expected: the canonical portrait is the only image.

- [ ] **Step 5: Scan for secrets and private paths**

Run:

```bash
if rg -n -i \
  'PRIVATE KEY|API_KEY|PASSWORD|SECRET|AUTH_TOKEN|ACCESS_KEY|CREDENTIAL|MNEMONIC|SEED_PHRASE|token[[:space:]]*=' \
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13; then
  echo 'secret-like content detected' >&2
  exit 1
fi
if rg -n '/home/|/Users/|desktop:' \
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13; then
  echo 'private path detected' >&2
  exit 1
fi
```

Expected: both searches have no hits. If either has a hit, inspect and remove
the unsafe content before continuing.

- [ ] **Step 6: Check Markdown and package shape**

Run:

```bash
bash -lc 'npx markdownlint-cli2 \
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/PROMPT.md \
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/DECISIONS.md \
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/docs/design.md'
find tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13 \
  ! -type f ! -type d -print
```

Expected: Markdown lint reports zero issues and no special files are printed.

---

### Task 3: Finalize and verify the manual-upload archive

**Files:**

- Consume: `tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/`
- Create under: `/home/takahiro/Documents/GPT Pro Analysis/`

**Interfaces:**

- Consumes: the verified working package.
- Produces: a timestamped package directory, top-level `PROMPT.md`, and `.tar.gz`
  archive for manual upload.

- [ ] **Step 1: Run the package finalizer**

Run:

```bash
FACE_PACK_FINALIZE_LOG=tmp/gpt-pro-akari-v22-face-angle-pack-finalize-2026-08-13.txt
/home/takahiro/.codex/skills/gpt-pro-review/scripts/finalize_gpt_pro_package.sh \
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13 \
  akari-v22-face-angle-pack | tee "$FACE_PACK_FINALIZE_LOG"
```

Expected: the log contains one value each for `PACKAGE_DIR`, `PROMPT_PATH`,
`ARCHIVE_PATH`, and `SCP_COMMAND`.

- [ ] **Step 2: Inspect the archive listing**

```bash
FACE_PACK_FINALIZE_LOG=tmp/gpt-pro-akari-v22-face-angle-pack-finalize-2026-08-13.txt
FACE_PACK_ARCHIVE=$(sed -n 's/^ARCHIVE_PATH=//p' "$FACE_PACK_FINALIZE_LOG")
test -n "$FACE_PACK_ARCHIVE"
test -f "$FACE_PACK_ARCHIVE"
tar tvzf "$FACE_PACK_ARCHIVE"
```

Expected:

- one timestamped top-level directory;
- one canonical image under `reference/`;
- all three prompts, with F01 and F02 still blocked;
- no rejected candidate or extra image;
- no symlink or special-file entry.

- [ ] **Step 3: Extract and compare the archive**

Extract the archive to a uniquely named temporary directory and compare it with
the staged package copied by the finalizer:

```bash
FACE_PACK_FINALIZE_LOG=tmp/gpt-pro-akari-v22-face-angle-pack-finalize-2026-08-13.txt
FACE_PACK_PACKAGE_DIR=$(sed -n 's/^PACKAGE_DIR=//p' "$FACE_PACK_FINALIZE_LOG")
FACE_PACK_ARCHIVE=$(sed -n 's/^ARCHIVE_PATH=//p' "$FACE_PACK_FINALIZE_LOG")
FACE_PACK_RUN_DIR=$(basename "$FACE_PACK_ARCHIVE" .tar.gz)
FACE_PACK_STAGED_DIR="$FACE_PACK_PACKAGE_DIR/$FACE_PACK_RUN_DIR"
FACE_PACK_COMPARE_DIR=$(mktemp -d)
tar xzf "$FACE_PACK_ARCHIVE" -C "$FACE_PACK_COMPARE_DIR"
diff -qr \
  "$FACE_PACK_STAGED_DIR" \
  "$FACE_PACK_COMPARE_DIR/$FACE_PACK_RUN_DIR"
rm -r -- "$FACE_PACK_COMPARE_DIR"
```

Expected: no differences.

- [ ] **Step 4: Re-run safety scans on extracted content**

Extract a fresh copy, scan it, and then remove only that explicit temporary
directory:

```bash
FACE_PACK_FINALIZE_LOG=tmp/gpt-pro-akari-v22-face-angle-pack-finalize-2026-08-13.txt
FACE_PACK_ARCHIVE=$(sed -n 's/^ARCHIVE_PATH=//p' "$FACE_PACK_FINALIZE_LOG")
FACE_PACK_RUN_DIR=$(basename "$FACE_PACK_ARCHIVE" .tar.gz)
FACE_PACK_SCAN_DIR=$(mktemp -d)
tar xzf "$FACE_PACK_ARCHIVE" -C "$FACE_PACK_SCAN_DIR"
if rg -n -i \
  'PRIVATE KEY|API_KEY|PASSWORD|SECRET|AUTH_TOKEN|ACCESS_KEY|CREDENTIAL|MNEMONIC|SEED_PHRASE|token[[:space:]]*=' \
  "$FACE_PACK_SCAN_DIR/$FACE_PACK_RUN_DIR"; then
  echo 'secret-like content detected' >&2
  exit 1
fi
if rg -n '/home/|/Users/|desktop:' \
  "$FACE_PACK_SCAN_DIR/$FACE_PACK_RUN_DIR"; then
  echo 'private path detected' >&2
  exit 1
fi
find "$FACE_PACK_SCAN_DIR/$FACE_PACK_RUN_DIR" \
  -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \
  -o -iname '*.webp' \) -print
find "$FACE_PACK_SCAN_DIR/$FACE_PACK_RUN_DIR" \
  ! -type f ! -type d -print
rm -r -- "$FACE_PACK_SCAN_DIR"
```

Expected: no secret or private-path hits, exactly one canonical image, and no
special files.

- [ ] **Step 5: Verify repository isolation**

Run:

```bash
git status --short
git check-ignore -v \
  tmp/gpt-pro-akari-v22-face-angle-pack-2026-08-13/.ignore-probe
```

Expected: the pre-existing workspace changes remain unchanged and the working
package does not appear as a new Git change.

- [ ] **Step 6: Handoff only the F00 gate**

Report:

- `PACKAGE_DIR`;
- `PROMPT_PATH`;
- `ARCHIVE_PATH`;
- `SCP_COMMAND`;
- the packaged canonical image dimensions and hash;
- that F01/F02 are present only as blocked templates;
- that no image was generated.

Tell the user to upload the archive or the canonical portrait plus `PROMPT.md`
to GPT Pro, request F00 only, and bring the resulting image back for the
identity comparison. Do not ask for F01 or F02 yet.

No implementation commit is required because all package outputs are ignored
local review artifacts or external transfer copies.
