# Akari v1.2 Daily.2 D06 Evening Entryway Floor Sit Implementation Plan

> Execute autonomously under the user's delegated A/B selection authority.

**Goal:** Build, select, promote, verify, and integrate the first Wave 2
evening scene.

**Architecture:** Extend the registry-driven Daily validator with D06 while
keeping Core and D01-D05 frozen. Generate local independent A/B candidates
from five accepted Core references and promote one byte-for-byte.

## Task 1: Register D06

1. Write failing tests for the asset, request, ordered references,
   dependencies, generation counts, comparison command, edit gate, and review
   controller policy.
2. Add D06 candidate r00, the exact r01 generation request, and frozen prompt
   and scene-contract pins.
3. Add `build:v1-2:d06-comparison` and `gate:edit:d06`.
4. Run focused tests, validator, Markdown lint, and `git diff --check`; commit.

## Task 2: Generate and Select

1. Open accepted C04, C01, C03 hairpin-side, C06-2, and C07 seated in their
   declared roles immediately before each generation.
2. Generate independent A and B with the frozen prompt; never use another D06
   candidate as a reference.
3. Verify PNG signature, dimensions, SHA-256, and build the comparison.
4. Inspect originals and comparison; Akari selects the strongest eligible
   candidate and uses C only when the declared retry policy requires it.

## Task 3: Promote and Integrate

1. Add failing live-linkage, clean-clone, and selected-hash tests.
2. Append ordered reviews, promote the selected source without processing,
   and set D06 to accepted r01.
3. Run `npm run gate:edit:d06`, Markdown lint, and the v1.2 integration gate.
4. Commit durable files only, preserve local evidence in the primary checkout,
   fast-forward main, reverify main, remove the worktree and branch, and
   continue directly to D07.
