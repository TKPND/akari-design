# Akari v1.7 V17-02 Hairpin-Side 30-Degree Promotion Design

Status: approved design.

Date: 2026-07-31.

## Goal

Promote the user-selected V17-02 r02 A image into the small durable Akari
v1.7 checkpoint package without expanding v1.7 into a manifest-backed
turnaround, release, or PDF workflow.

The promoted PNG remains byte-identical to the reviewed source. V17-01 remains
the sole current front-view authority. V17-02 becomes the accepted
hairpin-side 30-degree continuity authority.

## Source and Destination

Promotion source:

`/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-30-continuity/build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png`

Required source SHA-256:

`22aee4f2bcd9863b2c22c0e58b191cf767521576c0ffb11ed11208f3bd917749`

Tracked destination:

`akari-v1.7/accepted/base/akari-v1.7-v17-02-hairpin-side-30.png`

The semantic accepted filename drops the review-stage `r02-a` suffix. The
asset stays under the existing `accepted/base/` checkpoint structure instead
of creating a new angle hierarchy that would imply a broader package model.

## Exact Tracked Scope

Promotion changes exactly three tracked files:

1. add the byte-identical accepted PNG at the destination above;
2. update `akari-v1.7/README.md`;
3. update `akari-v1.7/selection.md`.

Do not track the r01 or r02 candidate directories, comparison images, local
selection note, task reports, or reviewer scratch. Do not modify the root
README, another version package, a manifest, validator, renderer, audit,
release artifact, or PDF.

## README Contract

Update the v1.7 package summary so that it:

- records V17-01 and V17-02 as promoted checkpoints;
- preserves V17-01 as the sole front-view authority;
- records V17-02 as the accepted character-left hairpin-side 30-degree
  continuity authority;
- lists both accepted PNGs and the shared selection record;
- preserves the character-design-checkpoint boundary and v1.6 exclusion;
- does not imply a complete 45-degree reference, paired views, turnaround,
  release package, manifest, or PDF.

## Selection Record Contract

Extend the existing `akari-v1.7/selection.md` rather than creating a second
tracked selection file. Preserve all V17-01 history, then add V17-02 sections
that record:

- the explicit user selection of r02 A;
- accepted destination and review source;
- source and destination SHA-256;
- the sole accepted-front generation authority and its SHA-256;
- the independent artifact review and blind tie-break that classified A as
  the sole passing candidate;
- why B and C were rejected;
- A's two Minor findings: slight near-side bust/waist rendering emphasis and
  slightly stronger eye/facial polish;
- the absence of automatic correction or r03 generation;
- byte identity, PNG signature, dimensions, original-detail inspection,
  Markdown lint, and bounded Git-scope verification.

The record must not rewrite A as flawless or erase the implementer's initial
over-strict verdict from review history. It may state that the independent
review and blind tie-break superseded that initial visual adjudication.

## Verification

Before copying, verify the source exists, has PNG signature
`89504e470d0a1a0a`, exact dimensions `1024x1536`, and the required SHA-256.

After copying:

- use `cmp --silent` to prove source and destination byte identity;
- prove matching SHA-256 values and the required destination digest;
- assert destination PNG signature and exact dimensions;
- open the destination at original detail;
- run Markdown lint on the two tracked Markdown files;
- run `git diff --check` and inspect exact tracked scope;
- confirm no review-stage file was added.

Do not run Node tests, Python tests, package validation, PDF builds, OCR,
integration gates, or release gates. The bounded asset-and-document checks own
this promotion.

## Completion Boundary

The task is complete only after an independent review finds no Critical or
Important issue, the three-file commit is fast-forwarded onto local `main`,
the merged result passes the same byte, image, Markdown, and scope checks, and
the promotion worktree and branch are cleaned up without deleting unrelated
worktrees.

Do not push unless the user explicitly asks.
