# Akari v1.7 Selection History

Date: 2026-07-31.

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
