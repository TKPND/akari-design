# Akari V2.2 Weekend Strict Identity Recovery Design

Date: 2026-08-17
Status: approved for implementation

## Decision

Create a series-scoped recovery control pack for the 24-shot Akari V2.2
Weekend Happenings handoff. Treat the completed handoff as frozen historical
evidence. Do not rewrite its 23 accepted decisions, the rejected S06 decision,
accepted image bytes, or decision log.

The recovery pack applies a `strict_identity_recovery` profile only to this
series. It does not change the installed global Akari V2.2 generation skill or
the reference policy for unrelated V2.2 work.

No image generation, image editing, crop, mask, composite, or face-free plate
creation is part of this implementation.

## Location and Source Boundary

Create the ignored local control pack at:

`tmp/handoffs/akari-v2.2-weekend-happenings-24shot-recovery-2026-08-17/`

The pack references these immutable inputs:

- Source handoff:
  `tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/`
- A minimal copied audit snapshot under `data/audit-source/`, taken from the
  verified GPT Pro attachment whose SHA-256 is
  `05846f006c461b80659378316e1725ad57ad36590b8703df5614b5bf0fedf9c1`
- Repository canonical Akari V2.2 authorities under
  `akari-v2.2/accepted/base/`

The copied audit snapshot contains the JSON audit, overlay CSV, corrected
rebuild source, and source metadata needed for reproducible validation; it does
not copy evidence images. The recovery pack stores paths and SHA-256 values for
source binding. Its validator fails when a bound source is absent or its
expected hash changes.

## Recovery Pack Components

### Recovery entrypoint and policy

`00-START-HERE.md` is the only recovery entrypoint. It states that the original
handoff is historical, image generation still requires a separate explicit
request, and the series profile overrides only reference eligibility and audit
workflow for future recovery calls.

`STRICT-IDENTITY-RECOVERY.md` defines:

- generated face-bearing images are deliverables, never identity inputs;
- a user-approved deliverable remains historically accepted but is not thereby
  reference-eligible;
- canonical portrait is the primary face authority;
- at most one matching canonical angle helper may accompany it;
- a third input may be a deterministic face-free plate created later under
  explicit authorization;
- canonical full-body is not supplied directly to a close or identity-sensitive
  recovery call because its small rendered face competes with the portrait;
- identity review is separate from anatomy, scene, outfit, and continuity
  review;
- previous accepted shots may appear in a separate continuity comparison, but
  never in the primary identity panel or generation inputs.

### Historical status overlay

`data/post-audit-status.csv` contains exactly one row for each S01-S24. It
copies the historical status fields without changing them and adds:

- `deliverable_status`
- `human_identity_verdict`
- `audit_identity_status`
- `audit_severity`
- `audit_confidence`
- `identity_reviewability`
- `audit_reason`
- `recommended_action`
- `reference_eligible`
- `reference_quarantined`
- `manual_regate_status`

Historical `accepted`, `identity_approved`, and `rejected_anatomy` values remain
verbatim. Every historical generated image has `reference_eligible=false` and
`reference_quarantined=true`, including S01. The five yellow shots start with
`manual_regate_status=awaiting_user_verdict`; this implementation does not
silently replace the user's earlier identity decisions.

Expected audit counts are fixed at:

- `keep_final_only`: 1
- `manual_regate`: 5
- `rebuild_priority`: 11
- `rebuild_after_anchor`: 6
- `keep_rejected`: 1

### Reference policy and actual-input ledger

`data/reference-authorities.tsv` is an allowlist for face-bearing inputs. It
contains only the canonical portrait, canonical full-body inventory record,
and the three approved canonical angle helpers with active repository paths and
SHA-256 values. The policy marks the full-body image as inventory-only for
strict recovery generation calls; it may later be the source of a deterministic
head-masked body plate.

`data/actual-input-ledger.csv` records future calls, one input per row, with:

- `call_id`
- `shot_id`
- `input_order`
- `path`
- `sha256`
- `source_class`
- `contains_face`
- `role`
- `authorization`

Before a future image-generation call, every planned input must be written to
the ledger and validated. A face-bearing row passes only when its path and hash
match an enabled canonical face authority. A face-free plate row passes only
when its source class is `deterministic_face_free_plate` and its provenance is
present in `data/face-free-plates.csv`. The plate ledger is initially header-only.

The existing generated candidates, rejected S06 controls, P00/T00/T01/E01-E06
lineage images, and derived comparison/contact-sheet assets are denied by class,
not by an incomplete path-only quarantine list.

### Reviewer-recorded continuity gate

`data/review-observations.csv` contains one S01-S24 row with the expected
`outfit_key` copied from `shots.yaml`. It separates expected values from
reviewer-recorded observations:

- `expected_outfit_key`
- `observed_outfit_key`
- `outfit_review_status`
- `outfit_verdict`
- `observed_bottom_category`
- `observed_bottom_color`
- `continuity_notes`

The validator does not pretend to recognize clothes automatically. A reviewer
records observations first; the validator then rejects an acceptance-ready row
when the recorded category differs from the expected category. S09 is seeded as
a hard mismatch because its dusty-blue below-knee flared skirt became beige or
khaki shorts. Unreviewed rows remain explicitly `not_reviewed`.

### Rebuild dependencies

`data/rebuild-plan.json` preserves the audited shot sets and corrects the
dependency ambiguity:

- S11 follows clean S09 and S10.
- S17-S19 follow a clean Sunday gate and S16.
- S22 follows clean S21.
- S23 follows clean S22, not merely clean S21.
- S24 uses the canonical portrait as its only face-bearing input.

The plan retains S06 as rejected for anatomy and does not schedule a retry
without a separate explicit generation request.

## Validation

Implement a standard-library-only Python validator and `unittest` coverage.
The validator checks:

- source paths and hashes;
- exact S01-S24 ID coverage with no duplicates;
- immutability of historical statuses against the source tracking CSV;
- the five expected audit counts;
- corrected rebuild dependencies;
- reference-authority hashes against live repository files;
- all actual-input ledger rows against strict face-bearing and face-free rules;
- reviewer-recorded outfit mismatches before an acceptance-ready state;
- `generation_permission=false` and an empty initial actual-input ledger;
- no image files exist in the recovery control pack.

Tests include a passing fixture plus failures for a generated face-bearing
input, an unregistered face-free plate, a changed historical status, an S09
outfit mismatch marked as passing, and the old S23-after-S21 dependency.

Run the validator, its unit tests, and repository Markdown lint. Generate a
fresh `SHA256SUMS` for the recovery pack after all files are final, then verify
it from the pack root.

## Manual Re-gate Boundary

The recovery pack records S03, S04, S07, S13, and S14 as awaiting the user's
strict identity verdict. Existing audit evidence may be presented for review,
but this implementation does not create new image artifacts or convert the
five rows to pass or fail without the user's verdict.

A user pass may change only `manual_regate_status` and the human verdict. It
does not make the historical generated image reference-eligible. A user fail
keeps history intact and confirms the rebuild action.

## Out of Scope

- Editing the installed global `generating-akari-v2-2-images` skill.
- Modifying repository canonical authorities or accepted scene images.
- Modifying the frozen source handoff or its checksums.
- Generating or regenerating any Akari image.
- Creating crops, masks, comparisons, composites, or face-free plates.
- Automatically deciding Akari identity on the user's behalf.
- Committing ignored recovery outputs or unrelated working-tree changes.
