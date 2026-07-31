# Akari v1.7 Baseline Promotion Design

Status: approved design, awaiting written-spec review.

Date: 2026-07-31.

## Summary

Promote the user-selected `V17-01 B / Slightly Happy` image from ignored
review output into a minimal, durable Akari v1.7 checkpoint. The promotion
preserves the selected PNG byte-for-byte, records its v1.5 B3 lineage and
review result, and makes it the sole current front-view authority for later
v1.7 angle work.

This pass is deliberately smaller than a release package or manifest-backed
turnaround. It secures the approved baseline before any new image generation.

## Source Authority

The exact promotion source is:

`build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png`

Its required SHA-256 is:

`64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8`

The promoted file must be byte-identical to this source. Do not resize,
re-encode, optimize, recolor, crop, rename through an image editor, or apply
metadata-changing image processing.

The upstream lineage source remains:

`akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`

Its required SHA-256 is:

`e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734`

The v1.5 B3 source records the inherited body-balance origin. The selected
v1.7 image replaces it as the current front-view authority because the user
explicitly selected B's restrained, quietly pleased expression.

No v1.6 image, prompt, proportion, accessory, outfit, palette, or manifest is
part of the positive v1.7 lineage.

## Durable Package

Create only this tracked package:

```text
akari-v1.7/
├── README.md
├── accepted/
│   └── base/
│       └── akari-v1.7-v17-01-intimate-front.png
└── selection.md
```

The accepted PNG is the promoted front-view baseline. `README.md` summarizes
the package purpose, status, authority, and boundaries. `selection.md`
records the user decision, source and destination paths, both SHA-256 values,
the final `READY` review result, and the byte-identity verification.

Do not copy candidate A, candidate C, the four-image comparison, or review
scratch into the tracked package. They remain local review evidence under
`build/` or the existing worktree.

## Status Reconciliation

Update the earlier intimate-baseline design document so its status no longer
says that written-spec review is pending. Its final state must distinguish:

- the design was approved;
- candidate B was explicitly selected;
- the independent final review returned `READY` with zero Critical and zero
  Important findings;
- the accepted PNG was promoted byte-for-byte under `akari-v1.7/`.

Do not rewrite the earlier design's historical scope or candidate rules. Only
make its completion status agree with the recorded outcome.

## Verification

Verify the promotion with the smallest checks that own this change:

1. confirm source and destination PNG signatures start with
   `89504e470d0a1a0a`;
2. confirm both files are valid `1024 x 1536` PNG images;
3. run `cmp` and require byte identity;
4. run SHA-256 on the source and destination and require the selected digest;
5. confirm the v1.5 B3 lineage file still matches its recorded digest;
6. inspect the promoted image once at original detail;
7. run `npm run lint:md` after the Markdown changes;
8. inspect `git diff` and `git status` to confirm only the intended tracked
   package, status update, and promotion design or plan files changed.

Do not run Python tests, Node tests, PDF builds, OCR, release gates, or image
generation. This pass changes no rendering, manifest, validator, or audit
behavior.

## Angle-Expansion Handoff

After promotion, later v1.7 angle design must use the accepted file under
`akari-v1.7/accepted/base/` as the sole current front-view authority. The
ignored `build/` copy is provenance evidence, not the future working anchor.

Angle direction, candidate count, auxiliary topology references, review
thresholds, and promotion rules remain separate design decisions. No angle
asset is created or pre-authorized by this promotion.

## Non-Goals

- no full manifest, release package, PDF, or turnaround structure;
- no new expression, pose, outfit, background, angle, or rendering change;
- no promotion of candidate A, candidate C, or comparison artifacts;
- no use or cleanup of v1.6 assets;
- no deletion of ignored review output or existing worktrees;
- no push, merge, branch cleanup, or remote synchronization;
- no automatic start of angle generation after the promotion.
