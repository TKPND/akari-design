const expressionLabels = [
  "Neutral",
  "Soft Smile",
  "Open Smile",
  "Laughing",
  "Surprised",
  "Anxious",
  "Pout",
  "Sleepy",
  "Wink",
];

const proportionGuides = [
  { name: "Head", note: "Large anime head, short bob volume, eyes held warm brown." },
  { name: "Torso", note: "Compact body under an oversized hoodie silhouette." },
  { name: "Hands", note: "Small hands sit inside long, soft hoodie sleeves." },
  { name: "Skirt", note: "Gray pleated skirt starts high and stays visible below the hem." },
  { name: "Legs", note: "Sturdy youthful legs with fuller thighs, soft calves, crew socks, and chunky white sneakers." },
];

const turnaroundGuides = [
  { name: "Crown", note: "Match head height across front, back, and angled views." },
  { name: "Shoulder", note: "Keep hoodie shoulder drop and sleeve width consistent." },
  { name: "Hem", note: "Hoodie hem and skirt reveal align across the set." },
  { name: "Sole", note: "Sneaker sole baseline stays level and unmirrored." },
];

function imageBlock(images) {
  return {
    type: "image",
    images,
  };
}

function notes(title, items, variant = "plain") {
  return {
    type: "note-list",
    title,
    variant,
    items,
  };
}

export const pages = [
  {
    page: 1,
    id: "cover-key-visual",
    title: "Akari v1.1",
    eyebrow: "Palette-Anchored Master Reference",
    layout: "cover",
    sourceInputs: ["cover-key-visual-16x9"],
    blocks: [
      imageBlock([
        { source: "cover-key-visual-16x9", label: "Accepted cover key visual" },
      ]),
      notes("Reference Lock", [
        "D65 / sRGB target",
        "14-page production reference",
        "Accepted generated cover candidate",
      ]),
    ],
  },
  {
    page: 2,
    id: "d65-color-palette",
    title: "D65 Color Palette",
    eyebrow: "Source Of Truth",
    layout: "palette",
    sourceInputs: ["hoodie-front", "expression-sheet", "bag-board", "shoe-board"],
    blocks: [
      { type: "palette-grid" },
      notes("Palette Rules", [
        "Named roles are the PDF source of truth",
        "Base / shadow / highlight ramps remain D65 balanced",
        "Audit tolerances define acceptable drift",
      ]),
    ],
  },
  {
    page: 3,
    id: "character-summary-proportion",
    title: "Character Summary + Proportion",
    eyebrow: "Identity Lock",
    layout: "proportion",
    sourceInputs: ["hoodie-front-proportion-corrected", "body-proportion-lock"],
    blocks: [
      imageBlock([
        { source: "hoodie-front-proportion-corrected", label: "Corrected hoodie silhouette" },
        { source: "body-proportion-lock", label: "Accepted body proportion lock" },
      ]),
      { type: "guide-lines", title: "Head / torso / leg landmarks", rows: proportionGuides },
      notes("Proportion Notes", [
        "Youthful anime proportion",
        "Sturdy healthy leg volume",
        "Fuller thighs with soft calves",
        "Short bob silhouette",
        "Oversized hoodie volume",
      ]),
    ],
  },
  {
    page: 4,
    id: "front-back",
    title: "Front / Back",
    eyebrow: "Production Turnaround",
    layout: "front-back",
    sourceInputs: ["hoodie-front", "hoodie-back"],
    blocks: [
      imageBlock([
        { source: "hoodie-front", label: "Front view" },
        { source: "hoodie-back", label: "Back view" },
      ]),
      { type: "guide-lines", title: "Shared turnaround guide lines", rows: turnaroundGuides },
      notes("Turnaround Rules", [
        "Matched scale",
        "Shared guide lines",
        "No mirrored shortcuts",
      ]),
    ],
  },
  {
    page: 5,
    id: "angle-turnaround",
    title: "Angle Turnaround",
    eyebrow: "Side And 45 Degree Views",
    layout: "turnaround",
    sourceInputs: ["side-view", "hairpin-side-45", "non-hairpin-side-45"],
    blocks: [
      imageBlock([
        { source: "side-view", label: "Side view" },
        { source: "hairpin-side-45", label: "Hairpin-side 45 degree view" },
        { source: "non-hairpin-side-45", label: "Non-hairpin-side 45 degree view" },
      ]),
      notes("Angle Notes", [
        "Hairpin-side label",
        "Non-hairpin-side label",
        "Hair and hoodie volume",
      ]),
    ],
  },
  {
    page: 6,
    id: "expressions",
    title: "Expressions",
    eyebrow: "Face / Hair Identity Master",
    layout: "expression-grid",
    sourceInputs: ["expression-sheet"],
    blocks: [
      imageBlock([{ source: "expression-sheet", label: "Nine-expression source sheet" }]),
      { type: "expression-labels", labels: expressionLabels },
      notes("Expression Rules", [
        "Keep eye shape and warm brown iris color consistent",
        "Keep short bob volume consistent across expressions",
        "Use the labels as English PDF text, not image-only text",
      ]),
    ],
  },
  {
    page: 7,
    id: "hair-face-details",
    title: "Hair / Face Details",
    eyebrow: "No-Drift Rules",
    layout: "detail-board",
    sourceInputs: ["hair-face-detail-board"],
    blocks: [
      imageBlock([
        { source: "hair-face-detail-board", label: "Accepted hair and face detail board" },
      ]),
      notes("Detail Cards", [
        "Warm brown eyes",
        "Short bob volume",
        "Character-left hair pins",
        "Soft cheek and mouth shapes stay readable",
      ], "cards"),
    ],
  },
  {
    page: 8,
    id: "outfit-rules",
    title: "Outfit Rules",
    eyebrow: "Layer And Silhouette Guide",
    layout: "outfit-rules",
    sourceInputs: ["hoodie-front", "base-front", "hoodie-back"],
    blocks: [
      imageBlock([
        { source: "hoodie-front", label: "Oversized hoodie front" },
        { source: "base-front", label: "Base outfit construction" },
        { source: "hoodie-back", label: "Back hoodie volume" },
      ]),
      notes("Outfit Rules", [
        "Oversized hoodie",
        "Gray pleated skirt",
        "Base outfit construction",
        "Sleeves remain long and soft, with neutral hoodie shadows",
      ]),
    ],
  },
  {
    page: 9,
    id: "footwear-sock-board",
    title: "Footwear Sock Board",
    eyebrow: "Large Sock And Footwear Source",
    layout: "detail-board-large",
    sourceInputs: ["footwear-board"],
    blocks: [
      imageBlock([
        { source: "footwear-board", label: "Official footwear and sock board" },
      ]),
      notes("Footwear Rules", [
        "Sock Height Guide",
        "Stable mid-calf height",
        "Stripe Placement",
        "Two thin pale blue stripes",
        "Design Notes",
        "Blue Gray Outsole",
        "Tongue Visibility",
        "Tongue sits slightly above sock line",
        "Toe Shape",
        "Rounded toe",
        "No logo-like marks",
        "Blue accents stay in the sock stripe hue family",
      ], "cards"),
    ],
  },
  {
    page: 10,
    id: "sneaker-construction",
    title: "Sneaker Construction",
    eyebrow: "Large Sneaker Source",
    layout: "detail-board-large",
    sourceInputs: ["shoe-board"],
    blocks: [
      imageBlock([
        { source: "shoe-board", label: "Official sneaker construction board" },
      ]),
      notes("Sculpted Sole Rules", [
        "Front View",
        "Outer Side View",
        "Inner Side View",
        "Back View",
        "Top View",
        "Sole",
        "White Laces",
        "Sculpted Sole",
        "Rounded toe",
        "Pale blue and blue-gray accents",
        "Soft chunky silhouette",
        "No logo-like marks",
      ], "cards"),
    ],
  },
  {
    page: 11,
    id: "bag-detail-board",
    title: "Bag Detail Board",
    eyebrow: "Large Accessory Source",
    layout: "detail-board-large",
    sourceInputs: ["bag-board"],
    blocks: [
      imageBlock([
        { source: "bag-board", label: "Official mini shoulder bag board" },
      ]),
      notes("Bag Specs W 16cm H 20cm D 5cm", [
        "Bag Detail Board",
        "Portable Battery",
        "Color & Material",
        "Canvas-like ivory body",
        "Canvas Like Fabric",
        "Pale blue-gray webbing strap",
        "Subtle silver hardware",
        "Can Fit",
        "Small Notebook",
        "W 16cm x H 20cm x D 5cm",
        "Smartphone / A6 notebook / earbuds",
        "Adjustable Strap",
      ], "cards"),
    ],
  },
  {
    page: 12,
    id: "bag-on-body-scale",
    title: "Bag-on-body scale",
    eyebrow: "Scale And Wear Reference",
    layout: "detail-board-large",
    sourceInputs: ["bag-on-body-scale"],
    blocks: [
      imageBlock([
        { source: "bag-on-body-scale", label: "Accepted bag-on-body scale reference" },
      ]),
      notes("Scale Rules", [
        "Bag-on-body scale",
        "Mini Shoulder Bag",
        "Compact against hoodie",
        "Strap Drop",
        "Cross Body Fit",
        "Bag rests at upper hip",
        "Scale stays compact against oversized hoodie",
        "Pale neutral body stays smaller than the hoodie pocket",
      ], "cards"),
    ],
  },
  {
    page: 13,
    id: "do-dont",
    title: "Do / Don't",
    eyebrow: "Production Rules",
    layout: "do-dont",
    sourceInputs: ["hoodie-front", "expression-sheet", "shoe-board", "bag-board"],
    blocks: [
      notes("Do", [
        "Preserve identity",
        "Keep the character-left hair pins on the correct side",
        "Use D65 palette roles for fabric, hair, skin, eyes, shoes, and bag",
      ], "cards"),
      notes("Don't", [
        "Avoid side flips",
        "Avoid color drift",
        "Avoid logo-like marks",
      ], "cards"),
      imageBlock([
        { source: "hoodie-front", label: "Identity reference" },
        { source: "expression-sheet", label: "Expression reference" },
        { source: "shoe-board", label: "Footwear reference" },
        { source: "bag-board", label: "Accessory reference" },
      ]),
    ],
  },
  {
    page: 14,
    id: "production-notes-source-manifest",
    title: "Production Notes / Source Manifest",
    eyebrow: "Traceability",
    layout: "manifest",
    sourceInputs: ["hoodie-front", "expression-sheet", "bag-board", "shoe-board"],
    blocks: [
      { type: "manifest-summary" },
      notes("Review Notes", [
        "Version",
        "Palette",
        "Accepted assets",
        "Review notes",
      ]),
    ],
  },
];
