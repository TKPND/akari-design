# Akari v1.2 Daily.2 D08 Evening Bed-Edge Sock Adjust Implementation Plan

> Execute autonomously under the user's delegated A/B selection authority.

**Goal:** Build, select, promote, verify, and integrate D08.

**Architecture:** Extend the Daily registry and validator without changing
accepted D01-D07 or Core bytes. Generate local A/B from accepted D07 and four
Core controllers, then promote one byte-for-byte.

## Task 1: Register

1. Add failing tests for D08 asset, request, references, dependencies, counts,
   commands, and controller policy.
2. Add candidate r00, exact r01 request, prompt hash, scene pins, comparison
   command, and edit gate.
3. Run the D08 gate, Markdown lint, and `git diff --check`; commit.

## Task 2: Generate and Select

1. Open D07, C04, C03, C06-2, and C07 seated immediately before each call.
2. Generate independent A/B from the frozen prompt and verify PNG, dimensions,
   SHA-256, and comparison output.
3. Inspect originals and comparison. Akari selects the strongest eligible
   candidate; use C only when policy requires it.

## Task 3: Promote and Integrate

1. Add failing selected-hash, linkage, and clean-clone tests.
2. Record ordered reviews, promote byte-for-byte, and set D08 accepted r01.
3. Run the D08 edit and v1.2 integration gates, commit durable files only,
   preserve local evidence in the primary checkout, fast-forward main,
   reverify, clean the worktree, and continue to D09.
