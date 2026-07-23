# Akari v1.2 Daily.2 D06 Evening Entryway Floor Sit Design

**Date:** 2026-07-16

**Status:** Approved under the user's autonomous-completion delegation

**Scope:** D06 scene contract, independent A/B generation, Akari selection,
accepted-asset linkage, and Wave 2 opening

## 1. Intent

Create the first Daily Wave 2 scene: Akari has just returned home, removed her
shoes, and sat down on the entryway-side floor before doing anything else. The
moment is ordinary end-of-day release, not a fall, illness, despair, or an
exhaustion spectacle.

D06 changes time, lighting, and scene from Wave 1. D05 remains an ordering
dependency only; its morning roomwear, bed hair, and washroom staging do not
control this image.

## 2. Scene Boundary

Use a compact apartment entryway with a closed front door, a shallow lower
threshold, warm interior evening light, and a cooler neutral door seam. Place
one simple soft tote or shoulder bag on the floor within arm's reach and one
neat pair of removed white-and-pale-blue sneakers near the threshold. These
two objects establish the return-home moment without turning the scene into a
product layout.

Do not show an open exterior door, rain entering the room, readable mail,
delivery boxes, keys in hand, a phone, food, alcohol, medication, luggage, or
another person.

## 3. Pose and Camera

Use a room-side front-left three-quarter camera at natural seated height. Keep
Akari's full figure readable against the entryway wall and floor.

The pose is a controlled low floor sit immediately after removing shoes:

- pelvis fully supported on the floor;
- upper back touches the wall lightly without sliding or collapsing;
- one knee is raised modestly with its socked sole fully flat;
- the other leg folds low and outward with a relaxed ankle and visible toe;
- the raised and folded legs remain separately traceable from pelvis to toes;
- one hand rests loosely over the raised knee or nearby thigh;
- the other palm gives light side support on the floor;
- shoulders drop and the spine rounds mildly while the neck remains supported;
- gaze falls toward the nearby floor or removed shoes, never the viewer.

Angle the knees away from the camera and keep the opaque pleated skirt covering
the pelvis and upper thighs. Preserve complete head, ornament, hands, pelvis,
both legs, both striped socks, heels, toes, wall support, and floor contact.

## 4. Identity, State, and Outfit

Preserve the same naturally cute 25-year-old adult Akari with normal short
warm-brown bob, complete character-left pale-blue crossed pins and ribbon
ornament, healthy face and leg volume, and compact adult proportions.

Use the Core standard indoor outfit exactly:

- oversized opaque white hoodie;
- opaque gray pleated skirt;
- warm-white mid-calf socks with exactly two thin pale-blue stripes;
- no footwear on the body.

Her eyes stay open and mildly heavy, brows and cheeks remain relaxed, and the
small closed mouth is almost neutral. The state reads as safe private relief
after arriving home, never sadness, fear, sickness, intoxication, sleep,
dissociation, sensual posing, or viewer performance.

## 5. Humanization

Use exactly two primary Humanization elements:

1. the character-right hoodie cuff is pushed up by about one thumb width;
2. the character-right sock sits slightly lower than the character-left sock
   while retaining both pale-blue stripes.

Do not add a loose hoodie neckline, exposed underlayer, rumpled skirt failure,
wet hair, dropped ornament, or further costume disorder.

## 6. Reference Contract

Use five visible accepted references in this order:

1. Accepted C04 controls grounded floor-sitting anatomy, standard hoodie and
   skirt, pelvis-to-leg support, healthy leg volume, and seated rendering. It
   does not control the exact side-sit pose, plain backdrop, smile, or rug.
2. Accepted C01 controls the adult identity, normal hair, front face, standard
   outfit, palette, and body volume. It does not control shoes, standing pose,
   or white reference backdrop.
3. Accepted C03 hairpin-side three-quarter controls the three-quarter identity,
   complete character-left ornament, cheek contour, and short-bob side
   construction. It does not control standing pose, smile, or shoes.
4. Accepted C06-2 controls only the heavy-open eyelids, relaxed brows and
   cheeks, and safe sleepy-secure expression intensity. C01 and C03 override
   its morning-hair disturbance, crop, and backdrop.
5. Accepted C07 seated controls two-stripe socks, ankle and foot volume,
   relaxed toes, and believable seated contact. It does not control the exact
   C04-derived pose, smile, rug, or plain backdrop.

No Daily image, local candidate, comparison, generated retry, or legacy path
may be a D06 generation reference.

## 7. Asset and Retry Contract

Use asset ID `D06`, revision `r01`, descriptor
`evening-entryway-floor-sit`, phase `9`, and dependencies D05, C01, C03, C04,
C06, and C07.

Durable accepted output:

```text
akari-v1.2/accepted/daily/evening/
akari-v1.2_d06_evening-entryway-floor-sit_r01.png
```

Local review outputs:

```text
akari-v1.2/source/candidates/d06/r01/
akari-v1.2/comparisons/d06-r01/d06-r01-comparison.webp
```

Generate independent A and B from the same frozen prompt and five accepted
references. Akari selects the strongest eligible candidate without pausing.
Generate C only when neither A nor B is eligible and unresolved Blocker or
Major findings are D06-scene-only or distinct candidate-local failures. A
shared C01, C03, C04, C06, or C07 failure reopens that controller.

## 8. Acceptance and Completion

Review Identity, Body, State, Continuity, Rendering, and Production in that
order. Hard reject severe identity or adult-age drift, broken sitting support,
untraceable or fused legs, floating feet, wrong outfit or sock stripes,
mirrored ornament, exposed underwear, distress coding, glamorized or sensual
posing, viewer focus, open exterior staging, crop loss, text, logo, watermark,
grid, collage, or multiple characters.

D06 is complete only when one eligible candidate is promoted byte-for-byte,
every generated candidate has an ordered review, the D06 edit and v1.2
integration gates pass on main, and local A/B evidence remains preserved.
