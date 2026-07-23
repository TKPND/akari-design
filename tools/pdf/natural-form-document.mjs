function imageBlock(images) {
  return { type: "image", images };
}

function notes(title, items, variant = "plain") {
  return { type: "note-list", title, variant, items };
}

function guides(title, rows) {
  return { type: "guide-lines", title, rows };
}

const assetPaths = {
  C01: "akari-v1.2/accepted/core/standing/akari-v1.2_c01_front-natural-stance_r01.png",
  C02: "akari-v1.2/accepted/core/standing/akari-v1.2_c02_back-natural-stance_r01.png",
  "C03-hairpin":
    "akari-v1.2/accepted/core/standing/akari-v1.2_c03_hairpin-side-45_r02.png",
  "C03-non-hairpin":
    "akari-v1.2/accepted/core/standing/akari-v1.2_c03_non-hairpin-side-45_r02.png",
  C04: "akari-v1.2/accepted/core/sitting/akari-v1.2_c04_floor-sitting_r01.png",
  C05: "akari-v1.2/accepted/core/face-hair/akari-v1.2_c05_morning-bedhair_r01.png",
  "C06-1":
    "akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-1_sleepy-neutral_r01.png",
  "C06-2":
    "akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-2_sleepy-secure_r01.png",
  "C06-3":
    "akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-3_loosened-mouth_r01.png",
  "C06-4":
    "akari-v1.2/accepted/core/face-hair/akari-v1.2_c06-4_soft-smile_r01.png",
  "C07-standing":
    "akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-standing_r01.png",
  "C07-seated":
    "akari-v1.2/accepted/core/indoor-feet/akari-v1.2_c07_indoor-socks-seated_r01.png",
  D01: "akari-v1.2/accepted/daily-validation/akari-v1.2_d01_morning-bedside_r01.png",
};

export const pages = [
  {
    page: 1,
    id: "cover-natural-form",
    title: "Cover / Natural Form",
    eyebrow: "Akari v1.2.0 Natural Form Core Settings",
    layout: "natural-form-cover",
    sourceInputs: ["C01"],
    blocks: [
      imageBlock([{ source: "C01", label: "C01 accepted natural front stance" }]),
      notes("Release Lock", [
        "Natural Form Core Release",
        "C01 through C07 accepted",
        "D01 accepted / Gate 4 release",
      ], "cards"),
    ],
  },
  {
    page: 2,
    id: "inheritance",
    title: "v1.1 to v1.2 Inheritance",
    eyebrow: "Inherited Identity / Extended Natural State",
    layout: "natural-form-standard",
    sourceInputs: ["C01", "C05"],
    blocks: [
      imageBlock([
        { source: "C01", label: "Inherited identity in natural standing" },
        { source: "C05", label: "Extended morning hair state" },
      ]),
      notes("Inheritance", [
        "Face, hair, ornament side, palette, body type, and base outfit remain locked",
        "Natural posture, floor sitting, indoor socks, morning hair, and micro-expression are extended",
        "v1.1 remains the fallback for shoes, bag, and any element not redefined here",
      ]),
    ],
  },
  {
    page: 3,
    id: "identity-lock",
    title: "Identity Lock",
    eyebrow: "Same Akari / More Natural Presence",
    layout: "natural-form-standard",
    sourceInputs: ["C01", "C05", "C06-4"],
    blocks: [
      imageBlock([
        { source: "C01", label: "Core identity and proportion" },
        { source: "C05", label: "Morning hair identity" },
        { source: "C06-4", label: "Soft smile identity" },
      ]),
      notes("No-drift Rules", [
        "Warm brown eyes and short dark-brown bob",
        "Hair ornament stays on character-left",
        "Healthy youthful proportions and leg volume",
        "Expression changes state, not identity",
      ], "cards"),
    ],
  },
  {
    page: 4,
    id: "natural-front-stance",
    title: "Natural Front Stance",
    eyebrow: "C01 / Primary Posture Standard",
    layout: "natural-form-guided",
    sourceInputs: ["C01"],
    blocks: [
      imageBlock([{ source: "C01", label: "C01 front natural stance r01" }]),
      guides("Posture Read", [
        { name: "Head", note: "Small relaxed offset without presentation-pose stiffness" },
        { name: "Shoulders", note: "Uneven but quiet, with hoodie volume preserved" },
        { name: "Pelvis", note: "Weight settles into one supporting leg" },
        { name: "Feet", note: "Both shoes remain grounded and traceable" },
      ]),
      notes("Use", ["Primary Natural Form front reference", "Supersedes the v1.1 front posture standard"]),
    ],
  },
  {
    page: 5,
    id: "back-and-45-views",
    title: "Back and 45-degree Views",
    eyebrow: "C02 + C03 / Weight Continuity",
    layout: "natural-form-standard",
    sourceInputs: ["C02", "C03-hairpin", "C03-non-hairpin"],
    blocks: [
      imageBlock([
        { source: "C02", label: "C02 back natural stance r01" },
        { source: "C03-hairpin", label: "C03 hairpin-side 45 r02" },
        { source: "C03-non-hairpin", label: "C03 non-hairpin-side 45 r02" },
      ]),
      notes("Continuity", [
        "Back and angled views keep the same supporting-leg logic",
        "Hairpin side is never mirrored",
        "Hoodie, skirt, knees, ankles, and shoe baselines remain coherent",
      ]),
    ],
  },
  {
    page: 6,
    id: "weight-and-joints",
    title: "Weight and Joint Guidelines",
    eyebrow: "Natural Form Body Logic",
    layout: "natural-form-guided",
    sourceInputs: ["C01", "C02"],
    blocks: [
      imageBlock([
        { source: "C01", label: "Front weight path" },
        { source: "C02", label: "Back weight path" },
      ]),
      guides("Joint Chain", [
        { name: "Spine", note: "A quiet curve follows the relaxed head and shoulder offset" },
        { name: "Pelvis", note: "Pelvic tilt follows the loaded leg instead of a model pose" },
        { name: "Knees", note: "Knees remain anatomically traceable under the skirt" },
        { name: "Ankles", note: "Ankles resolve into grounded feet without disconnects" },
      ]),
    ],
  },
  {
    page: 7,
    id: "floor-sitting-master",
    title: "Floor Sitting Master",
    eyebrow: "C04 / Relaxed Seated Weight",
    layout: "natural-form-standard",
    sourceInputs: ["C04"],
    blocks: [
      imageBlock([{ source: "C04", label: "C04 floor sitting r01" }]),
      notes("Master Read", [
        "Pelvis visibly carries the seated weight",
        "Supporting hand contacts the floor without wrist collapse",
        "Both legs read as relaxed rather than arranged for display",
        "No sneakers in the indoor floor-sitting standard",
      ], "cards"),
    ],
  },
  {
    page: 8,
    id: "floor-sitting-anatomy",
    title: "Floor Sitting Anatomy Notes",
    eyebrow: "C04 / Trace Every Limb",
    layout: "natural-form-guided",
    sourceInputs: ["C04"],
    blocks: [
      imageBlock([{ source: "C04", label: "C04 anatomy trace reference" }]),
      guides("Traceability", [
        { name: "Near leg", note: "Thigh, knee, shin, ankle, heel, and toes form one readable chain" },
        { name: "Far leg", note: "Occlusion never creates a detached socked foot" },
        { name: "Pelvis", note: "Fold direction starts from a believable hip position" },
        { name: "Hand", note: "Palm contact supports weight while all fingers stay coherent" },
      ]),
      notes("Hard Reject", ["Disconnected foot", "Untraceable lower leg", "Collapsed supporting hand"], "cards"),
    ],
  },
  {
    page: 9,
    id: "indoor-sock-feet",
    title: "Indoor Sock Feet",
    eyebrow: "C07 / Standing + Seated",
    layout: "natural-form-standard",
    sourceInputs: ["C07-standing", "C07-seated"],
    blocks: [
      imageBlock([
        { source: "C07-standing", label: "C07 standing indoor socks r01" },
        { source: "C07-seated", label: "C07 seated indoor socks r01" },
      ]),
      notes("Sock-foot Rules", [
        "Two pale-blue lines remain stable around each sock",
        "Heel, arch, ball, and toe direction stay readable",
        "Standing feet carry weight; seated feet relax without flattening",
        "No sneaker shape remains under indoor socks",
      ], "cards"),
    ],
  },
  {
    page: 10,
    id: "morning-bed-hair",
    title: "Morning Bed Hair",
    eyebrow: "C05 / Controlled Morning State",
    layout: "natural-form-standard",
    sourceInputs: ["C05"],
    blocks: [
      imageBlock([{ source: "C05", label: "C05 morning bed hair r01" }]),
      notes("State Rules", [
        "Crown and side tufts loosen without changing the bob silhouette",
        "Hair ornament remains visible on character-left",
        "Sleepiness reads through lids, mouth, and posture",
        "Morning variation is controlled asymmetry, not damage or neglect",
      ], "cards"),
    ],
  },
  {
    page: 11,
    id: "expression-gradient",
    title: "Sleepy-to-Soft-Smile Expressions",
    eyebrow: "C06 / Daily Micro-expression Continuity",
    layout: "natural-form-expression",
    sourceInputs: ["C06-1", "C06-2", "C06-3", "C06-4"],
    blocks: [
      imageBlock([
        { source: "C06-1", label: "C06-1 Sleepy Neutral" },
        { source: "C06-2", label: "C06-2 Sleepy Secure" },
        { source: "C06-3", label: "C06-3 Loosened Mouth" },
        { source: "C06-4", label: "C06-4 Soft Smile" },
      ]),
      notes("Gradient", [
        "01 Sleepy Neutral",
        "02 Sleepy Secure",
        "03 Loosened Mouth",
        "04 Soft Smile",
        "Keep eye, cheek, mouth, and head-angle changes small and continuous",
      ], "cards"),
    ],
  },
  {
    page: 12,
    id: "d01-morning-validation",
    title: "D01 Morning Validation",
    eyebrow: "Daily Scene / Gate 4",
    layout: "natural-form-standard",
    sourceInputs: ["D01"],
    blocks: [
      imageBlock([{ source: "D01", label: "D01 morning bedside r01" }]),
      notes("Validation Result", [
        "C04 floor-sitting weight remains believable",
        "C05 morning hair remains identifiable",
        "C06-2 sleepy-secure state remains readable",
        "C07 indoor sock feet remain anatomically traceable",
        "Gate 4 outcome: release",
      ], "cards"),
    ],
  },
  {
    page: 13,
    id: "do-dont",
    title: "Do / Don't",
    eyebrow: "Production Guardrails",
    layout: "natural-form-do-dont",
    sourceInputs: ["C01", "C04"],
    blocks: [
      notes("Do", [
        "Preserve identity and ornament side",
        "Show believable weight and traceable joints",
        "Keep socks, feet, hair, and clothing continuous",
        "Use canonical accepted assets as controlling references",
      ], "cards"),
      notes("Don't", [
        "Do not stage a presentation pose",
        "Do not accept broken anatomy or disconnected feet",
        "Do not mirror the hairpin side",
        "Do not use candidate or comparison paths as release inputs",
      ], "cards"),
      imageBlock([
        { source: "C01", label: "Standing standard" },
        { source: "C04", label: "Sitting standard" },
      ]),
    ],
  },
  {
    page: 14,
    id: "source-review-status",
    title: "Source Manifest and Review Status",
    eyebrow: "v1.2.0 Release Record",
    layout: "natural-form-status",
    sourceInputs: ["manifest/assets.yaml", "manifest/review-log.yaml"],
    blocks: [
      guides("Accepted Assets", [
        { name: "C01", note: "accepted / front natural stance r01" },
        { name: "C02", note: "accepted / back natural stance r01" },
        { name: "C03", note: "accepted / paired 45-degree views r02" },
        { name: "C04", note: "accepted / floor sitting r01" },
        { name: "C05", note: "accepted / morning bed hair r01" },
        { name: "C06", note: "accepted / four-expression gradient r01" },
        { name: "C07", note: "accepted / standing and seated indoor socks r01" },
        { name: "D01", note: "accepted / morning bedside r01" },
      ]),
      notes("Release", [
        "Version v1.2.0",
        "Natural Form Core Release",
        "Gate 4 outcome: release",
        "No unresolved Blocker or Major finding",
        "Daily Wave 1 is unblocked",
      ], "cards"),
    ],
  },
];

export const naturalFormDocument = {
  id: "akari-v1.2-natural-form-core",
  title: "Akari v1.2.0 Natural Form Core Settings",
  pages,
  assetPaths,
  outputPdf: "akari-v1.2/release/akari-v1.2-core-settings.pdf",
  previewDir: "build/akari-v1.2-page-previews",
  siteHtml: "build/akari-v1.2-site/index.html",
};
