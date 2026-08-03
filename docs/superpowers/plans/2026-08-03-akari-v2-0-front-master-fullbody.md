# Akari v2.0 Front Master Full-Body Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce one GPT Pro front full-body image from the approved FRONT MASTER and promote the face master plus approved full-body result as the minimal Akari v2.0 canonical package.

**Architecture:** Treat the existing FRONT MASTER as immutable primary identity input and the existing white-T full-body image as a secondary lower-body guide only. Package those inputs with a strict GPT Pro prompt, pause for the returned PNG and explicit visual approval, then copy the two accepted images byte-for-byte into a new `akari-v2.0/` package with concise provenance records.

**Tech Stack:** PNG assets, GPT Pro manual image generation, ImageMagick `identify`, `sha256sum`, `cmp`, Git, Markdown.

## Global Constraints

- The FRONT MASTER is the sole face, eye, hair, skin, and expression authority.
- Akari reads as an 18-year-old young adult with a cute, approachable childhood-friend presence.
- The canonical full-body view is strict front, neutral standing, white T-shirt, navy A-line mid-thigh shorts, white socks, and generic blue-and-white sneakers.
- The organizer is on character-left/canvas-right in the front view.
- The shorts have exactly two short drawcord ends and no bow.
- Only the face master and one user-approved front full-body PNG become canonical v2.0 images.
- Oblique, rear, pose, jacket, contact-sheet, and comparison images remain untracked.
- Do not run PDF audits or Python tests.
- Do not transform accepted PNGs during promotion.

---

### Task 1: Build the GPT Pro generation package

**Files:**

- Create: `tmp/gpt-pro-akari-v2-front-fullbody/PROMPT.md`
- Create: `tmp/gpt-pro-akari-v2-front-fullbody/tree.txt`
- Create: `tmp/gpt-pro-akari-v2-front-fullbody/git-log.txt`
- Create: `tmp/gpt-pro-akari-v2-front-fullbody/reference/01-front-master-primary.png`
- Create: `tmp/gpt-pro-akari-v2-front-fullbody/reference/02-white-t-fullbody-secondary.png`
- Create: `tmp/gpt-pro-akari-v2-front-fullbody/docs/2026-08-03-akari-v2-0-front-master-fullbody-design.md`

**Interfaces:**

- Consumes primary source:
  `/home/takahiro/.codex/generated_images/019fc632-26c5-7bf3-8c52-5bccf7607363/exec-cc663046-4420-4290-a975-1a7d7bf09a59.png`
- Consumes secondary source:
  `/home/takahiro/.codex/generated_images/019fc632-26c5-7bf3-8c52-5bccf7607363/exec-6d12b732-1b82-43d9-93e3-685ddd89e3b8.png`
- Produces: one sanitized `.tar.gz` package and a standalone `PROMPT.md` for manual GPT Pro upload.

- [ ] **Step 1: Verify immutable source identities**

Run:

```bash
identify -format '%f %wx%h\n' \
  /home/takahiro/.codex/generated_images/019fc632-26c5-7bf3-8c52-5bccf7607363/exec-cc663046-4420-4290-a975-1a7d7bf09a59.png \
  /home/takahiro/.codex/generated_images/019fc632-26c5-7bf3-8c52-5bccf7607363/exec-6d12b732-1b82-43d9-93e3-685ddd89e3b8.png
sha256sum \
  /home/takahiro/.codex/generated_images/019fc632-26c5-7bf3-8c52-5bccf7607363/exec-cc663046-4420-4290-a975-1a7d7bf09a59.png \
  /home/takahiro/.codex/generated_images/019fc632-26c5-7bf3-8c52-5bccf7607363/exec-6d12b732-1b82-43d9-93e3-685ddd89e3b8.png
```

Expected:

```text
exec-cc663046-4420-4290-a975-1a7d7bf09a59.png 1023x1537
exec-6d12b732-1b82-43d9-93e3-685ddd89e3b8.png 916x1717
34aab9fb8c5db9d49667106a3fc4158b1a28b2bd6633a1ce6073b57d4dde1cbe  /home/takahiro/.codex/generated_images/019fc632-26c5-7bf3-8c52-5bccf7607363/exec-cc663046-4420-4290-a975-1a7d7bf09a59.png
736c769e1dd7fda7fb38210700a14a3dbb4ea44d2a5ab5fc45e86ad35263aeb8  /home/takahiro/.codex/generated_images/019fc632-26c5-7bf3-8c52-5bccf7607363/exec-6d12b732-1b82-43d9-93e3-685ddd89e3b8.png
```

- [ ] **Step 2: Assemble the ignored working package**

Create the directories, copy the two PNGs without transformation, copy the
approved design document, and write `tree.txt` plus `git-log.txt`. Name and
role the images exactly as listed in the Files section so GPT Pro cannot mistake
the secondary full-body face for an identity authority.

- [ ] **Step 3: Write the exact generation prompt**

`PROMPT.md` must instruct GPT Pro to:

1. Start from `reference/01-front-master-primary.png` and preserve its visible
   face, eyes, irises, cheeks, chin, smile, hair, neck, shoulders, and white
   T-shirt as closely as possible.
2. Extend downward into one strict-front complete figure.
3. Use `reference/02-white-t-fullbody-secondary.png` only for body balance,
   shorts, organizer, socks, and shoes; never copy or average its face.
4. Follow every Full-Body Image Contract and Acceptance Gate in the included
   design document.
5. Return one clean vertical PNG only, without variants, labels, text, borders,
   watermarks, props, jacket, or decorative background.

- [ ] **Step 4: Run security and package finalization**

Run:

```bash
grep -RInE 'PRIVATE KEY|API_KEY|PASSWORD|SECRET|AUTH_TOKEN|ACCESS_KEY|CREDENTIAL|MNEMONIC|SEED_PHRASE|token[[:space:]]*=' \
  tmp/gpt-pro-akari-v2-front-fullbody | head -20
/home/takahiro/.codex/skills/gpt-pro-review/scripts/finalize_gpt_pro_package.sh \
  tmp/gpt-pro-akari-v2-front-fullbody \
  akari-v2-front-master-fullbody
```

Expected: no secret-bearing input and printed `PACKAGE_DIR`, `PROMPT_PATH`,
`ARCHIVE_PATH`, and `SCP_COMMAND` values.

### Task 2: Review the GPT Pro return

**Files:**

- Receive: one user-attached GPT Pro PNG.
- Create locally only when useful: face and full-body comparison images under
  `tmp/akari-v2-review/`.
- Create after explicit approval: `tmp/akari-v2-review/approved-source.txt`.

**Interfaces:**

- Consumes: one GPT Pro PNG returned from Task 1.
- Produces: `approved-source.txt` containing the exact absolute path of the
  explicitly user-approved candidate, plus its dimensions and SHA-256.

- [ ] **Step 1: Verify the returned file**

Set `AKARI_V2_RETURNED_SOURCE` to the exact attachment path reported by Codex,
then run `identify`, `file`, and `sha256sum` against it. Confirm a valid PNG, a
complete vertical figure, and no truncation before judging design details.

- [ ] **Step 2: Inspect identity at original detail**

Open the returned PNG, the primary FRONT MASTER, and enlarged face crops. Reject
the candidate if the eye shapes, iris sizes, cheek width, chin, mouth, hairline,
ponytail side, or ornament side materially differ from the FRONT MASTER.

- [ ] **Step 3: Inspect body, outfit, and presentation**

Check the compact healthy body, neutral strict-front pose, complete anatomy,
white T-shirt, navy shorts, exactly two drawcord ends, organizer on
character-left/canvas-right, socks, shoes, warm off-white background, and lack
of seams or artifacts.

- [ ] **Step 4: Obtain the selection gate**

Show the candidate and concise findings to the user. Do not promote, retouch, or
regenerate until the user explicitly accepts that exact PNG. After acceptance,
write `realpath "$AKARI_V2_RETURNED_SOURCE"` as the sole line of
`tmp/akari-v2-review/approved-source.txt`.

### Task 3: Promote the approved v2.0 baseline

**Files:**

- Create: `akari-v2.0/accepted/base/akari-v2.0-front-face-master.png`
- Create: `akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png`
- Create: `akari-v2.0/README.md`
- Create: `akari-v2.0/selection.md`

**Interfaces:**

- Consumes: immutable FRONT MASTER and the exact user-approved GPT Pro PNG.
- Produces: a minimal tracked Akari v2.0 package and one promotion commit.

- [ ] **Step 1: Copy accepted binaries without transformation**

Copy the FRONT MASTER to the face-master destination and the accepted GPT Pro
PNG to the full-body destination. Do not resize, recompress, crop, color-adjust,
or rename either source before the copy.

- [ ] **Step 2: Record the package contract and provenance**

Write `README.md` with the two authority roles, identity and outfit locks, and
explicit non-goals. Write `selection.md` with the user decision, source paths,
dimensions, SHA-256 hashes, byte-identity verification, and known accepted
minor differences if any.

- [ ] **Step 3: Verify binaries and Markdown**

Run:

```bash
AKARI_V2_APPROVED_SOURCE=$(<tmp/akari-v2-review/approved-source.txt)
test -f "$AKARI_V2_APPROVED_SOURCE"
cmp --silent \
  /home/takahiro/.codex/generated_images/019fc632-26c5-7bf3-8c52-5bccf7607363/exec-cc663046-4420-4290-a975-1a7d7bf09a59.png \
  akari-v2.0/accepted/base/akari-v2.0-front-face-master.png
cmp --silent "$AKARI_V2_APPROVED_SOURCE" \
  akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png
identify -format '%f %wx%h\n' akari-v2.0/accepted/base/*.png
sha256sum akari-v2.0/accepted/base/*.png
./node_modules/.bin/markdownlint-cli2 \
  ':akari-v2.0/README.md' ':akari-v2.0/selection.md'
git diff --check
```

Expected: both `cmp` checks exit zero, both files are valid PNGs, recorded
hashes and dimensions match command output, Markdown lint exits zero, and the
diff has no whitespace errors.

- [ ] **Step 4: Enforce commit scope**

Run `git status --short` and confirm the promotion diff contains only the two
canonical PNGs, `akari-v2.0/README.md`, and `akari-v2.0/selection.md`. Do not add
`tmp/`, comparisons, GPT Pro packages, oblique views, rear views, or candidates.

- [ ] **Step 5: Commit the v2.0 promotion**

Run:

```bash
git add -- \
  akari-v2.0/accepted/base/akari-v2.0-front-face-master.png \
  akari-v2.0/accepted/base/akari-v2.0-front-fullbody.png \
  akari-v2.0/README.md \
  akari-v2.0/selection.md
git diff --cached --check
git commit -m 'feat: promote Akari v2.0 front baseline'
```

- [ ] **Step 6: Verify the recorded commit**

Run `git show --stat --oneline --summary HEAD`, `git status --short --branch`,
and repeat both `cmp` checks against the committed files. Report the commit hash,
the two canonical SHA-256 values, and whether the branch remains ahead of its
remote. Do not push unless the user separately requests it.
