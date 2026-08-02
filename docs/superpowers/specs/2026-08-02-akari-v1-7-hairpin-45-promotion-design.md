# Akari v1.7 V17-03 Hairpin-Side 45-Degree Promotion Design

Status: approved design.

Date: 2026-08-02.

## Goal

Promote the explicitly selected V17-03 r02 C image into the minimal durable
Akari v1.7 character-design checkpoint without changing the reviewed pixels or
expanding v1.7 into a manifest-backed turnaround, release, or PDF workflow.

V17-01 remains the sole accepted front-view authority. V17-02 remains the
accepted character-left hairpin-side 30-degree continuity authority. V17-03
becomes the accepted character-left hairpin-side 45-degree continuity
authority.

## Approved Promotion Approach

Use the existing V17-03 r02 worktree because it contains the verified ignored
selection source. After this design and its implementation plan are committed,
fast-forward that worktree to the planning commit, perform the byte-identical
promotion there, review the exact three-file change, and fast-forward the
approved promotion commit onto local `main`.

Do not promote directly in `main` or create another promotion worktree. Keeping
the source, promotion, review, and commit in the existing r02 worktree gives the
clearest provenance without copying the candidate into another temporary
checkout.

## Source, Provenance, and Destination

Selected ignored source:

`/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02/build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png`

Required SHA-256:

`bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954`

Authoritative generated source:

`/home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png`

Generation provenance:

- outer request ID: `call_rd98V3j0ikTsdm1c3h04392x`;
- completed generation ID: `exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4`;
- immutable prompt SHA-256:
  `19459cdff592ecb59a32dbce7f082f233e96e66e5a74a1383ef678773e9c572c`;
- comparison SHA-256:
  `92856c88e45541bc9f4e6e776e8d8bf936202faa298e4e4a50ba7901ccfe8095`.

Tracked destination:

`akari-v1.7/accepted/base/akari-v1.7-v17-03-hairpin-side-45.png`

The semantic accepted filename drops the review-stage `r02-c` suffix. Copy the
selected source without resizing, recompression, compositing, color conversion,
metadata normalization, or any other transformation.

## Exact Tracked Scope

Promotion changes exactly three tracked files:

1. add the byte-identical accepted PNG at the destination above;
2. update `akari-v1.7/README.md`;
3. update `akari-v1.7/selection.md`.

Do not track r01 or r02 inputs, candidates, comparisons, review crops, reports,
ledgers, or rollout extracts. Do not modify another version package, the root
README, a manifest, validator, renderer, audit, release artifact, or PDF.

## Accepted-Authority Contract

The three accepted v1.7 checkpoints have distinct roles:

- V17-01 is the sole accepted front-view authority for identity, adult age,
  underlying body balance, restrained expression, roomwear, palette, and
  finish;
- V17-02 is the accepted hairpin-side 30-degree continuity authority for the
  same-side camera orbit and intermediate view;
- V17-03 is the accepted hairpin-side 45-degree continuity authority for the
  selected fixed moment at that angle.

V17-03 does not supersede the front or 30-degree assets. Future work must use
the strongest applicable accepted authority for the attribute or view being
designed rather than treating the newest file as universal authority.

## README Contract

Update the v1.7 package summary so that it:

- retitles the package heading for the plural promoted hairpin-side
  checkpoints and updates its top-level date to 2026-08-02;
- records V17-01, V17-02, and V17-03 as promoted checkpoints;
- preserves each checkpoint's distinct authority role;
- lists all three accepted PNGs and the shared selection record;
- states that V17-03 preserves the selected age-25 identity, quiet expression,
  fixed 45-degree moment, corrected chest-to-waist volume, relaxed T-shirt
  drape, neutral stance, hair, ornament, room, light, and finish;
- replaces the now-obsolete claim that v1.7 lacks a 45-degree reference;
- preserves the boundary that this is not a paired opposite-side set, complete
  turnaround, manifest-backed release, wardrobe redesign, or PDF;
- preserves the exclusion of v1.6 material from positive inheritance
  authority.

## Selection Record Contract

Extend the existing `akari-v1.7/selection.md` without rewriting the V17-01 or
V17-02 history. Add a V17-03 section that records:

- the original selection-history date, an updated date of 2026-08-02, and the
  V17-03 selection date of 2026-08-01 without rewriting earlier event dates;
- the user's explicit selection of r02 C;
- the ignored review source, authoritative generated source, and semantic
  accepted destination;
- the source and destination SHA-256;
- the request ID, completed generation ID, immutable prompt hash, and
  comparison hash;
- that A and C passed all seven hard gates, B failed Gate 3 because it did not
  complete the mandatory body correction, and the passing quality order was
  C then A;
- that C gave the strongest balance of complete localized correction, natural
  adult volume, same-person read, and finished image quality;
- that C corrected the near-side bust projection, under-bust definition,
  narrowed waist, and tight T-shirt fall while preserving the fixed 45-degree
  view and every out-of-scope attribute;
- that the slightly stronger eye polish and compressed cord are the two known
  r01 A Minor findings, remain materially unchanged in C, and are not new r02
  findings;
- that the final task and process review returned zero Critical, Important,
  and Minor findings, with no eligibility disagreement or tie-break;
- that no repair, composite, r03 generation, or further image edit followed
  the selection;
- byte identity, PNG signature, dimensions, original-detail inspection,
  Markdown lint, and bounded precommit Git-scope verification.

Do not describe C as globally flawless or erase the two inherited Minor
findings. Do not describe B's expected candidate-level Gate 3 failure as an
implementation or process defect.

## Verification

Before copying, verify that the tracked destination does not exist. If it does,
stop without overwriting it and reconcile that unexpected state separately.
Verify that both the ignored source and authoritative generated source exist
and are byte-identical. Verify their required SHA-256, PNG signature
`89504e470d0a1a0a`, format, and exact dimensions `PNG 1024x1536`.

After copying:

- use `cmp --silent` to prove source and destination byte identity;
- prove matching SHA-256 values and the required destination digest;
- assert the destination PNG signature and exact dimensions;
- open the accepted destination at original detail and inspect the complete
  figure, face, torso correction, ornament, hands, feet, room, and finish;
- run direct Markdown lint on the two changed package Markdown files;
- run the repository Markdown lint required after Markdown changes;
- run `git diff --check` and assert the exact three-file tracked scope;
- confirm that no review-stage file is staged or tracked.

Do not run Node tests, Python tests, package validation, PDF builds, OCR,
integration gates, or release gates. The bounded image-and-document checks own
this promotion.

## Review, Integration, and Cleanup

An independent reviewer must confirm the source provenance, byte identity,
document accuracy, exact tracked scope, and absence of Critical or Important
findings before integration.

After review approval:

1. fast-forward local `main` to the promotion commit;
2. rerun byte, hash, signature, dimension, original-detail, and Markdown
   verification from the merged `main` checkout;
3. inspect the promotion commit itself and prove that its changed path set is
   exactly the accepted PNG, package README, and shared selection history;
4. prove that `main` contains every V17-03 design, plan, and promotion commit;
5. prove that the accepted destination and authoritative generated C source
   still exist outside the worktrees and remain byte-identical with the
   required digest;
6. resolve both V17-03 worktrees from `git worktree list --porcelain`, require
   their exact absolute paths and expected branches, and verify that neither
   contains an uncommitted tracked, staged, or non-ignored untracked file;
7. prove that both V17-03 branch tips are ancestors of the verified local
   `main` tip;
8. remove only these two named worktrees and their branches:
   - `.worktrees/akari-v1-7-hairpin-45-continuity` and
     `codex/akari-v1-7-hairpin-45-continuity`;
   - `.worktrees/akari-v1-7-hairpin-45-continuity-r02` and
     `codex/akari-v1-7-hairpin-45-continuity-r02`.

The cleanup intentionally removes ignored r01/r02 candidates, comparisons,
review crops, and local SDD scratch after the accepted C bytes and durable
selection history are proven on `main`. The authoritative generated C source
and rollout provenance remain outside those worktrees. Do not remove or modify
any unrelated worktree or branch. Worktree removal may use the exact named
paths with `--force` only because the approved cleanup intentionally deletes
their verified ignored review output. Delete each branch with safe `-d` only
after its ancestor check passes; never use `-D`.

If any precondition or merged verification fails, keep both V17-03 worktrees
and branches intact and stop. Do not force integration, cleanup, source
replacement, regeneration, or scope expansion.

Do not push unless the user explicitly asks.

## Non-Goals

- no image generation, repair, compositing, rerendering, or color adjustment;
- no change to V17-01 or V17-02 accepted bytes;
- no opposite-side view, rear view, paired set, or complete turnaround;
- no manifest, validator, renderer, audit, release package, or PDF;
- no modification of v1.6 material or its inheritance status;
- no remote synchronization.
