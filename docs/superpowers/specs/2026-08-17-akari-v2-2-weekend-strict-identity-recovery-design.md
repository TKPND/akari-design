# Akari V2.2 Weekend Strict Identity Recovery Design

Date: 2026-08-17
Status: approved for implementation

## Decision

Add a series-scoped recovery overlay to the active 24-shot Akari V2.2 Weekend
Happenings handoff. Treat its completed shot state as frozen historical
evidence. Do not rewrite its 23 accepted decisions, the rejected S06 decision,
accepted image bytes, shot manifest, status table, or decision log.

The recovery overlay applies a `strict_identity_recovery` profile only to this
series. It does not change the installed global Akari V2.2 generation skill or
the reference policy for unrelated V2.2 work.

No image generation, image editing, crop, mask, composite, or face-free plate
creation is part of this implementation.

## Location and Source Boundary

Apply the overlay inside the ignored active handoff at:

`tmp/handoffs/akari-v2.2-weekend-happenings-24shot-handoff-2026-08-17/`

Only `00-START-HERE.md` and `tracking/README.md` are edited, so the normal
resume path cannot bypass recovery mode. New recovery policy, data, ledger, and
validation files live under the existing `runbook/`, `tracking/`, and `scripts/`
directories.

The overlay records the verified GPT Pro attachment SHA-256
`05846f006c461b80659378316e1725ad57ad36590b8703df5614b5bf0fedf9c1`
and binds the current historical `DECISION-LOG.md`, `tracking/shot-status.csv`,
and `tracking/shot-manifest.json` by SHA-256. Its validator fails when a bound
historical source changes. Repository canonical Akari V2.2 authorities remain
under `akari-v2.2/accepted/base/` and are verified by active path and hash.

## Recovery Pack Components

### Recovery entrypoint and policy

`00-START-HERE.md` remains the entrypoint and dispatches to recovery mode before
the historical production runbook. It states that image generation still
requires a separate explicit request and that the series profile narrows only
reference eligibility and audit workflow for future recovery calls.

`runbook/STRICT-IDENTITY-RECOVERY.md` defines:

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

`tracking/shot-status.post-audit.csv` contains exactly one row for each S01-S24. It
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

`tracking/strict-identity-recovery.json` is the machine-readable policy. Its
default reference decision is deny. Its face-bearing allowlist contains only
the canonical portrait and three approved canonical angle helpers with active
repository paths and SHA-256 values. The canonical full-body image is recorded
as inventory-only for strict recovery generation calls; it may later be the
source of a deterministic head-masked body plate.

`tracking/recovery-input-ledger.jsonl` starts with a schema record and stores
future actual calls. Each attempt record includes:

- `call_id`
- `shot_id`
- `operation`
- `output_path`
- `inputs`, preserving input order and each input's `path`, `sha256`,
  `source_class`, `contains_face`, and `role`
- `authorization`
- `outfit_observation`
- `identity_review`
- `user_gate`

Before a future image-generation call, every planned input must be written to
the ledger and validated. A face-bearing row passes only when its path and hash
match an enabled canonical face authority. A face-free plate row passes only
when its source class is `deterministic_face_free_plate` and its complete source
and transform provenance is present in that ledger record. The ledger contains
no attempt records initially.

The existing generated candidates, rejected S06 controls, P00/T00/T01/E01-E06
lineage images, and derived comparison/contact-sheet assets are denied by class,
not by an incomplete path-only quarantine list.

### Reviewer-recorded continuity gate

`tracking/shot-status.post-audit.csv` contains the expected `outfit_key` for
each shot and separates it from reviewer-recorded observations:

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

`tracking/strict-identity-recovery.json` preserves the audited shot sets and
corrects the dependency ambiguity:

- S11 follows clean S09 and S10.
- S17-S19 follow a clean Sunday gate and S16.
- S22 follows clean S21.
- S23 follows clean S22, not merely clean S21.
- S24 uses the canonical portrait as its only face-bearing input.

The plan retains S06 as rejected for anatomy and does not schedule a retry
without a separate explicit generation request.

## Validation

Implement `scripts/validate_strict_identity_recovery.py` with Python's standard
library and add `unittest` coverage under `scripts/tests/`. The validator checks:
The validator checks:

- historical source paths and hashes;
- exact S01-S24 ID coverage with no duplicates;
- immutability of historical statuses against the source tracking CSV;
- the five expected audit counts;
- corrected rebuild dependencies;
- reference-authority hashes against live repository files;
- all actual-input ledger rows against strict face-bearing and face-free rules;
- reviewer-recorded outfit mismatches before an acceptance-ready state;
- `generation_permission=false` and an empty initial actual-input ledger;
- every future recovery output path is under `outputs/recovery/`;
- no image file was created by this implementation.

Tests include a passing fixture plus failures for a generated face-bearing
input, an unregistered face-free plate, a changed historical status, an S09
outfit mismatch marked as passing, and the old S23-after-S21 dependency.

Run the validator, its unit tests, and repository Markdown lint. Create a
recovery-specific checksum file for the new overlay files without rewriting the
handoff's original snapshot `SHA256SUMS`.

## Manual Re-gate Boundary

The recovery overlay records S03, S04, S07, S13, and S14 as awaiting the user's
strict identity verdict. Existing audit evidence may be presented for review,
but this implementation does not create new image artifacts or convert the
five rows to pass or fail without the user's verdict.

A user pass may change only `manual_regate_status` and the human verdict. It
does not make the historical generated image reference-eligible. A user fail
keeps history intact and confirms the rebuild action.

## Out of Scope

- Editing the installed global `generating-akari-v2-2-images` skill.
- Modifying repository canonical authorities or accepted scene images.
- Modifying `DECISION-LOG.md`, `tracking/shot-status.csv`,
  `tracking/shot-manifest.json`, prompt cards, the historical production
  runbook, or the original handoff checksums.
- Generating or regenerating any Akari image.
- Creating crops, masks, comparisons, composites, or face-free plates.
- Automatically deciding Akari identity on the user's behalf.
- Committing ignored handoff files or unrelated working-tree changes.
