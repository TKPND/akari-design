# Akari v1.7 Selection History

Original selection-history date: 2026-07-31.

Updated: 2026-08-02.

## V17-01 Intimate Front Selection

### Promoted Result

**B / Slightly Happy is the accepted V17-01 front baseline.**

The user explicitly selected B after reviewing v1.5 B3 and V17-01 candidates
A, B, and C at equal scale. B gives the clearest restrained improvement toward
the approved intimate-childhood-friend direction while preserving the same
adult identity, hair, ornament, body balance, outfit, apartment, and
hand-painted finish.

Candidate C was not selected because its intended one-corner mouth response
was not reliably distinguishable from B at full-body scale. The planned
no-correction boundary remained in force, so no follow-up candidate generation
was performed.

### Authority and Lineage

- Current front authority:
  `accepted/base/akari-v1.7-v17-01-intimate-front.png`.
- Promotion source:
  `build/v1.7-intimate-baseline/akari-v1.7-v17-01-intimate-b1.png`.
- Upstream body-balance lineage:
  `akari-v1.5/accepted/base/akari-v1.5-b3-body-balance.png`.
- No v1.6 asset, prompt, proportion, accessory, outfit, palette, or manifest
  has positive inheritance authority.

### Review Result

The final independent review returned `READY` with zero Critical and zero
Important findings. Incidental whole-frame stroke and texture rerendering was
classified as a Minor difference allowed by the approved V17-01 design.

### File Hashes

| Role | SHA-256 |
| --- | --- |
| v1.7 V17-01 accepted front | `64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8` |
| v1.5 B3 lineage source | `e0cd9a7e9abfcbe5997df156f1e6ecb246ca91fe91ba0b1d84d7947050c66734` |

### Promotion Verification

The accepted PNG was copied without transformation. Its PNG signature,
`1024 x 1536` dimensions, SHA-256, and byte identity against the selected
review source were verified during promotion.

## V17-02 Hairpin-Side 30-Degree Selection

### V17-02 Promoted Result

**r02 A / hairpin-side 30-degree continuity is the explicit user choice.**

The user explicitly selected r02 A after reviewing the accepted front and
r02 A/B/C at equal display scale. It is promoted as the character-left
hairpin-side 30-degree continuity authority; V17-01 remains the sole accepted
front-view authority.

### V17-02 Authority and Lineage

- Accepted destination:
  `accepted/base/akari-v1.7-v17-02-hairpin-side-30.png`.
- Ignored promotion source:
  `build/v1.7-hairpin-30-continuity/akari-v1.7-v17-02-hairpin-30-r02-a.png`.
- Sole accepted-front generation authority:
  `accepted/base/akari-v1.7-v17-01-intimate-front.png`.
- Accepted-front authority SHA-256:
  `64385d2c63cd2e56fdee2d367b199e7339406de324f0e8add00e5432b54108e8`.
- Candidate A generation artifact ID:
  `exec-28dc8843-3811-4d27-b334-4bbeaf034196`.
- Review comparison SHA-256:
  `8f3a68abc4694363d8abe904698a53c168d3c9750e6799288848acb34b1fa826`.

### V17-02 Review Result

The generation implementer's initial visual adjudication classified all three
candidates as failing. That over-strict verdict remains part of the review
history; it was superseded by a full independent artifact review and a second
blind A-only tie-break. Both later reviews classified A as the sole hard-gate
pass and safe for user selection.

The superseding reviews found that A preserves one coherent camera orbit near
30 degrees through the face, collar, shoulders, ribcage, waistband, pelvis,
knees, and feet. Its foot depth offset reads as perspective parallax rather
than a changed one-leg pose: shoulders and pelvis remain level, both feet stay
planted, and neither leg reads as the sole weight-bearing leg.

A retains two Minor findings and is not recorded as flawless:

- slight near-side bust and waist perspective/rendering emphasis;
- slightly stronger eye and facial polish than the accepted front.

Neither finding crosses the locked body, stance, identity, adult-age, or
glamour boundary. Candidate B was rejected because its chest modeling and
bust-to-waist contrast exceeded modest perspective change. Candidate C was
rejected because its head and upper torso turned farther than its lower-body
chain; its bust, waist, hip, weight-shift, neutral-stance, and coherent-view
drift recurred; and its diagonal floor and baseboard introduced camera-roll
presentation drift.

No automatic repair, correction, or r03 generation followed the selection.

### V17-02 File Hashes

| Role | SHA-256 |
| --- | --- |
| V17-02 selected review source | `22aee4f2bcd9863b2c22c0e58b191cf767521576c0ffb11ed11208f3bd917749` |
| V17-02 accepted destination | `22aee4f2bcd9863b2c22c0e58b191cf767521576c0ffb11ed11208f3bd917749` |

### V17-02 Promotion Verification

The accepted destination was copied without transformation and verified
byte-identical to the ignored promotion source. Its PNG signature is
`89504e470d0a1a0a`, its dimensions are `1024 x 1536`, and its SHA-256 is the
recorded digest above. Original-detail inspection confirmed the whole figure,
face, ornament, hands, feet, background, and finish remained intact. Both
targeted and repository Markdown lint passed, and bounded Git-scope assertions
confirmed that only the accepted PNG, this selection history, and the v1.7
README comprise the tracked promotion.

## V17-03 Hairpin-Side 45-Degree Selection

Selection date: 2026-08-01.

### V17-03 Promoted Result

**r02 C / hairpin-side 45-degree continuity is the explicit user choice.**

The user explicitly selected r02 C. Candidates A and C passed all seven hard
gates. Candidate B failed Gate 3 because it did not complete the mandatory
body correction. Among the passing candidates, the quality order was C then
A.

C gives the strongest balance of complete localized correction, natural adult
volume, same-person read, and finished image quality. It corrected the rounder
near-side bust projection, newly stronger under-bust definition, narrowed
waist, and tight T-shirt fall while preserving the fixed 45-degree view and
every out-of-scope attribute.

### V17-03 Authority and Provenance

- Accepted destination:
  `accepted/base/akari-v1.7-v17-03-hairpin-side-45.png`.
- Ignored review source:
  `/home/takahiro/workspace/akari-design/.worktrees/akari-v1-7-hairpin-45-continuity-r02/build/v1.7-hairpin-45-continuity-r02/akari-v1.7-v17-03-hairpin-45-r02-c.png`.
- Authoritative generated source:
  `/home/takahiro/.codex/generated_images/019fb8fe-27cc-73b0-a506-039a2a0afc77/exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4.png`.
- Outer request ID: `call_rd98V3j0ikTsdm1c3h04392x`.
- Completed generation ID:
  `exec-4fa1ac22-7b22-413e-a85a-02bcdef3c6c4`.
- Immutable prompt SHA-256:
  `19459cdff592ecb59a32dbce7f082f233e96e66e5a74a1383ef678773e9c572c`.
- Review comparison SHA-256:
  `92856c88e45541bc9f4e6e776e8d8bf936202faa298e4e4a50ba7901ccfe8095`.

V17-01 remains the sole accepted front-view authority. V17-02 remains the
accepted character-left hairpin-side 30-degree continuity authority. V17-03
is the accepted character-left hairpin-side 45-degree continuity authority
for this selected fixed moment; it does not supersede either earlier asset.

### V17-03 Review Result

C is not recorded as globally flawless. Its slightly stronger eye polish and
compressed cord are the two known r01 A Minor findings; both remain materially
unchanged in C and are not new r02 findings.

The final task and process review returned zero Critical, Important, and Minor
findings, with no eligibility disagreement or tie-break. Candidate B's Gate 3
failure was an expected candidate-level result, not an implementation or
process defect. No repair, composite, r03 generation, or further image edit
followed the selection.

### V17-03 File Hashes

| Role | SHA-256 |
| --- | --- |
| V17-03 selected review source | `bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954` |
| V17-03 authoritative generated source | `bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954` |
| V17-03 accepted destination | `bffe8e124a6cfed9319d903baa9e109d2dd0016d7d2cd7a13538f460e8992954` |

### V17-03 Promotion Verification

The accepted destination was copied without transformation and verified
byte-identical to both the ignored review source and authoritative generated
source. Its PNG signature is `89504e470d0a1a0a`, its dimensions are
`1024 x 1536`, and its SHA-256 is the recorded digest above. Original-detail
inspection confirmed the complete figure, face, torso correction, ornament,
hands, feet, room, and finish remained intact. Both targeted and repository
Markdown lint passed, and bounded precommit Git-scope assertions confirmed
that only the accepted PNG, this selection history, and the v1.7 README
comprise the tracked promotion.
