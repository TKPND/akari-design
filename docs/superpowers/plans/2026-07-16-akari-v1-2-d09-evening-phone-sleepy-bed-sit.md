# Akari v1.2 Daily.2 D09 Implementation Plan

> Execute autonomously under the user's delegated A/B selection authority.

## Task 1: Register the Contract

1. Add failing D09 asset, policy, request, ordering, count, and command tests.
2. Register the D09 asset, dependencies, two-candidate request, prompt hash,
   validator contract, and comparison command.
3. Run the focused pre-generation gate.

## Task 2: Generate and Select

1. Open D08, C04, C03, C06-1, and C07 before each independent call.
2. Generate A/B without cross-candidate references and build the comparison.
3. Review originals, select quality-first, and use C only when policy permits.

## Task 3: Promote and Integrate

1. Add acceptance, hash-linkage, and clean-clone tests.
2. Promote the selected PNG byte-for-byte and record ordered reviews.
3. Run D09 and integration gates, preserve local evidence, fast-forward main,
   reverify, clean the worktree, and continue to D10.
