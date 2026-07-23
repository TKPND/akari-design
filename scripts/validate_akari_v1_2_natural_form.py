from __future__ import annotations

import argparse
import hashlib
import re
from functools import partial
from pathlib import Path, PurePosixPath

import yaml

if __package__:
    from scripts.akari_v1_2_daily import (
        DAILY_REVIEW_POLICIES,
        ValidationError,
        daily_candidate_path,
        daily_review_policy,
        validate_daily_candidate_dimensions,
        validate_daily_finding,
        validate_daily_generation_request,
        validate_daily_png_dimensions,
        validate_daily_review_status,
    )
else:
    from akari_v1_2_daily import (
        DAILY_REVIEW_POLICIES,
        ValidationError,
        daily_candidate_path,
        daily_review_policy,
        validate_daily_candidate_dimensions,
        validate_daily_finding,
        validate_daily_generation_request,
        validate_daily_png_dimensions,
        validate_daily_review_status,
    )


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "akari-v1.2"
ASSET_IDS = (
    "C01",
    "C02",
    "C03",
    "C04",
    "C05",
    "C06",
    "C07",
    "D01",
    "D02",
    "D03",
    "D04",
    "D05",
    "D06",
    "D07",
    "D08",
    "D09",
    "D10",
    "D11",
    "D12",
    "D13",
    "D14",
    "D15",
)
STATUSES = (
    "candidate",
    "review",
    "accepted",
    "accepted-with-notes",
    "rejected",
    "superseded",
)
SEVERITIES = ("blocker", "major", "minor")
GATES = ("identity", "body", "state", "daily")
REVISION_RE = re.compile(r"^r\d{2}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REVIEW_CATEGORIES = (
    "identity",
    "body",
    "state",
    "continuity",
    "rendering",
    "production",
)
C03_R02_FRAMING_CONTRACT = {
    "canvas": {"width": 1024, "height": 1536},
    "measurement": {
        "tool": "imagemagick",
        "fuzz_percent": 6,
        "geometry_format": "%@",
        "head_top_formula": "y",
        "sole_formula": "y_plus_height_minus_1",
    },
    "anchors": [
        {
            "asset_id": "C01",
            "revision": "r01",
            "head_top_y": 65,
            "sole_y": 1450,
        },
        {
            "asset_id": "C02",
            "revision": "r01",
            "head_top_y": 65,
            "sole_y": 1463,
        },
    ],
    "maximum_displacement": {
        "percent_of_canvas_height": 2,
        "integer_pixels": 30,
    },
    "required_intersection": {
        "head_top_y": [35, 95],
        "sole_y": [1433, 1480],
    },
    "prompt_target": {
        "head_top_y": 65,
        "sole_y": 1456,
        "bottom_margin_pixels": 79,
    },
}
C04_R01_FRAMING_GUIDANCE = {
    "canvas": {"width": 1024, "height": 1536},
    "enforcement": "advisory",
    "head_top_y": [70, 160],
    "lowest_toe_y": [1360, 1490],
    "intended_lateral_margin_pixels": 48,
    "reject_on_numeric_miss_alone": False,
    "major_only_when": "crop-or-scale-prevents-structural-review",
}
C05_R01_FRAMING_GUIDANCE = {
    "canvas": {"width": 1024, "height": 1536},
    "enforcement": "advisory",
    "crop": "chest-up-below-hoodie-neckline-and-upper-chest",
    "intended_top_breathing_room_pixels": 70,
    "intended_lateral_hair_margin_pixels": 60,
    "face_placement": "vertical-upper-middle",
    "required_visible_features": [
        "complete-crown-and-outer-hair-silhouette",
        "complete-character-left-ornament",
        "both-eyes-face-outline-cheek-strand-and-lower-bob-ends",
        "shoulders-hoodie-neckline-and-upper-chest",
    ],
    "reject_on_numeric_miss_alone": False,
    "major_only_when": (
        "crop-or-scale-prevents-complete-face-hair-state-review"
    ),
}
C06_STATIC_ASSET_CONTRACT = {
    "descriptor": "daily-smile-gradient",
    "phase": 3,
    "variants": [
        "sleepy-neutral",
        "sleepy-secure",
        "loosened-mouth",
        "soft-smile",
    ],
    "expected_paths": [
        "accepted/core/face-hair/"
        "akari-v1.2_c06-1_sleepy-neutral_rNN.png",
        "accepted/core/face-hair/"
        "akari-v1.2_c06-2_sleepy-secure_rNN.png",
        "accepted/core/face-hair/"
        "akari-v1.2_c06-3_loosened-mouth_rNN.png",
        "accepted/core/face-hair/"
        "akari-v1.2_c06-4_soft-smile_rNN.png",
    ],
    "depends_on": ["C05"],
    "gate": "state",
}
C06_EXPRESSION_REFERENCE_CONTRACT = {
    "role": "v1.1-expression-range",
    "inheritance_class": "reference-only",
    "source_path": "source/originals/v1_1_front_3.webp",
    "copied_path": "akari-v1.2/references/v1.1/expression-grid.webp",
    "source_collection": "v1.1",
    "reuse_rationale": (
        "C06 neutral relaxed-mouth and closed-mouth soft-smile mechanics only; "
        "open-mouth laughing surprised worried pouting yawning and closed-eye "
        "examples are excluded and grant no identity crop rendering hair outfit "
        "or background authority"
    ),
    "sha256": (
        "2b70c639b320275cde6787263bd6fe0f88ad59068154e4c2439ae69502e6f919"
    ),
}
C06_R01_STAGE_PAIRS = (
    ("c06-1", "sleepy-neutral"),
    ("c06-2", "sleepy-secure"),
    ("c06-3", "loosened-mouth"),
    ("c06-4", "soft-smile"),
)
C06_R01_EDIT_POLICY = {
    "source_role": "accepted_c05_edit_source",
    "mode": "direct-from-source-per-stage",
    "chained_c06_outputs": "forbidden",
}
C06_R01_PRODUCTION_REQUIREMENTS = {
    "file_format": "png",
    "canvas": {"width": 1024, "height": 1536},
    "standalone_composition": True,
    "generated_grid": "forbidden",
}
C06_R01_FRAMING_GUIDANCE = {
    "canvas": {"width": 1024, "height": 1536},
    "enforcement": "advisory",
    "crop": "chest-up-below-hoodie-neckline-and-upper-chest",
    "intended_top_breathing_room_pixels": 70,
    "intended_lateral_hair_margin_pixels": 60,
    "face_placement": "vertical-upper-middle",
    "required_visible_features": [
        "complete-crown-and-outer-hair-silhouette",
        "complete-character-left-ornament",
        "both-eyes-face-outline-cheek-strand-and-lower-bob-ends",
        "shoulders-hoodie-neckline-and-upper-chest",
    ],
    "reject_on_numeric_miss_alone": False,
    "major_only_when": (
        "crop-or-scale-prevents-complete-face-hair-sequence-review"
    ),
}
C06_R01_STAGE_REQUIRED_PHRASES = {
    "c06-1": ("closest to accepted C05", "closed lips in a neutral line"),
    "c06-2": ("safe and comfortable rather than blank", "almost neutral"),
    "c06-3": ("lift only minimally", "beginning of warmth"),
    "c06-4": ("small closed-mouth everyday smile", "No teeth, open mouth"),
}
C06_R01_EXACT_PROMPT_SHA256 = {
    "shared": "1d5ede16c4593085ec749f759c0fde8fc721eacc6665e1e1a8c80a2f9dc72fb1",
    "c06-1": "fa7829f275839abd49986d7d0011f66dafede5364144a99915d742eadccd951f",
    "c06-2": "c5c4c8a29038c9a5d98bcafe3512bc6c95f6610545934a0fa5df29cf6d731c29",
    "c06-3": "160b4e1a3cb4299273bf3f1f96a9be1154dd38f50bad203ae20909814d33b282",
    "c06-4": "3498b3310cf0cd2ff48918bbf8b47780107667414ccb78e204a7f001fed0dd12",
}
D01_STATIC_ASSET_CONTRACT = {
    "descriptor": "morning-bedside",
    "phase": 4,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily-validation/"
        "akari-v1.2_d01_morning-bedside_rNN.png"
    ],
    "depends_on": ["C04", "C05", "C06", "C07"],
    "gate": "daily",
}
D01_R01_SIZE_POLICY = {
    "target_canvas": {"width": 1024, "height": 1536},
    "accepted_width": {"minimum": 1020, "maximum": 1028},
    "accepted_height": {"minimum": 1532, "maximum": 1540},
    "force_exact_resize": "forbidden",
}
D01_R01_REFERENCES = (
    (
        "accepted_c04_floor_sitting_body",
        "akari-v1.2/accepted/core/sitting/"
        "akari-v1.2_c04_floor-sitting_r01.png",
    ),
    (
        "accepted_c05_morning_hair",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c05_morning-bedhair_r01.png",
    ),
    (
        "accepted_c06_sleepy_secure_expression",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c06-2_sleepy-secure_r01.png",
    ),
    (
        "accepted_c07_seated_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-seated_r01.png",
    ),
)
D01_R01_SCENE_CONTRACT = {
    "camera": "front-biased-light-three-quarter-at-natural-seated-viewing-height",
    "surface": "low-contrast-rug-beside-restrained-bed-edge",
    "lighting": "soft-curtain-filtered-morning-natural-light",
    "room_density": "medium-lived-in-not-cluttered",
    "gaze": "viewer-directed-with-incomplete-sleepy-focus",
    "outfit": {
        "top": "loose-opaque-white-short-sleeve-t-shirt",
        "bottom": "simple-opaque-gray-shorts-style-roomwear",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-and-ornament",
        "both-hands-including-one-believable-supporting-hand",
        "pelvis-support-and-both-thigh-roots",
        "both-knees-shins-ankles-heels-and-socked-toes",
    ],
    "forbidden_props": [
        "clock",
        "phone",
        "mug",
        "readable-book",
        "explanatory-prop",
    ],
}
D01_R01_PRODUCTION_REQUIREMENTS = {
    "file_format": "png",
    "target_canvas": D01_R01_SIZE_POLICY["target_canvas"],
    "accepted_width": D01_R01_SIZE_POLICY["accepted_width"],
    "accepted_height": D01_R01_SIZE_POLICY["accepted_height"],
    "standalone_composition": True,
    "generated_grid": "forbidden",
    "force_exact_resize": D01_R01_SIZE_POLICY["force_exact_resize"],
}
D01_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d01-scene-staging-background-lighting-or-presentation"
    ),
    "stop_for_shared_core_failure": ["C04", "C05", "C06", "C07"],
    "cross_candidate_references": "forbidden",
}
D01_R01_ACCEPTANCE_GATES = (
    "identity",
    "body",
    "state",
    "rendering",
    "production",
)
D01_R01_HARD_REJECTS = (
    "severe identity age face body-volume or rendering drift",
    "fused missing duplicated disconnected or untraceable limbs or joints",
    "floating pelvis or hand support that contradicts body weight",
    "thin legs twisted ankles pointed ballet toes or contradictory foot contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "non-reversible hair wrong hair length extreme bed head wet hair or wind",
    "closed eyes distress intoxication sensual posing broad smile or open mouth",
    "wrong outfit sheer clothing exposed underwear shoes slippers or bare feet",
    "incorrect sock height stripe count ankle volume toe relaxation or contact",
    "crop or scale that prevents complete body support or feet review",
    "readable text logo watermark border collage grid or multiple character",
)
D01_R01_SHARED_PROMPT_SHA256 = (
    "ad9c1e9f86e18cb912ed32eed624d03bd0e05b9bfd0c09071e344b2076ca5232"
)
D02_STATIC_ASSET_CONTRACT = {
    "descriptor": "morning-rug-daze",
    "phase": 5,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/morning/"
        "akari-v1.2_d02_morning-rug-daze_rNN.png"
    ],
    "depends_on": ["D01", "C04", "C05", "C06", "C07"],
    "gate": "daily",
}
D02_R01_REFERENCES = (
    (
        "accepted_d01_morning_continuity",
        "akari-v1.2/accepted/daily-validation/"
        "akari-v1.2_d01_morning-bedside_r01.png",
    ),
    (
        "accepted_c04_floor_sitting_body",
        "akari-v1.2/accepted/core/sitting/"
        "akari-v1.2_c04_floor-sitting_r01.png",
    ),
    (
        "accepted_c05_morning_hair",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c05_morning-bedhair_r01.png",
    ),
    (
        "accepted_c06_sleepy_neutral_expression",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c06-1_sleepy-neutral_r01.png",
    ),
    (
        "accepted_c07_seated_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-seated_r01.png",
    ),
)
D02_R01_SCENE_CONTRACT = {
    "camera": "front-biased-three-quarter-natural-seated-height-wider-than-d01",
    "surface": "frame-left-window-side-low-contrast-bedroom-rug",
    "continuity": "d01-same-morning-bedroom-outfit-and-hair",
    "lighting": "soft-frame-left-curtain-filtered-morning-light",
    "gaze": "frame-left-window-directed-with-incomplete-focus",
    "pose": "both-legs-forward-one-knee-slightly-bent-one-supporting-hand",
    "humanization": [
        "straighter-leg-sock-light-natural-slouch",
        "slightly-uneven-t-shirt-hem-with-seated-wrinkles",
    ],
    "outfit": {
        "top": "loose-opaque-white-short-sleeve-t-shirt",
        "bottom": "simple-opaque-gray-shorts-style-roomwear",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-and-ornament",
        "both-hands-including-one-believable-supporting-hand",
        "pelvis-support-and-both-thigh-roots",
        "both-knees-shins-ankles-heels-and-socked-toes",
    ],
    "forbidden_props": [
        "phone",
        "mug",
        "clock",
        "readable-book",
        "food",
        "explanatory-prop",
    ],
}
D02_R01_PRODUCTION_REQUIREMENTS = {
    "file_format": "png",
    "target_canvas": {"width": 1024, "height": 1536},
    "accepted_width": {"minimum": 1020, "maximum": 1028},
    "accepted_height": {"minimum": 1532, "maximum": 1540},
    "standalone_composition": True,
    "generated_grid": "forbidden",
    "force_exact_resize": "forbidden",
}
D02_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d02-scene-staging-background-lighting-or-presentation"
    ),
    "stop_for_shared_failure": ["D01", "C04", "C05", "C06", "C07"],
    "cross_candidate_references": "forbidden",
}
D02_R01_ACCEPTANCE_GATES = (
    "identity",
    "body",
    "state",
    "continuity",
    "rendering",
    "production",
)
D02_R01_HARD_REJECTS = (
    "severe identity adult-age face body-volume or rendering drift",
    "fused missing duplicated disconnected or untraceable limbs or joints",
    "floating pelvis contradictory hand support or implausible whole-body weight",
    "thin legs broken knees twisted ankles pointed toes or contradictory foot contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "non-reversible hair wrong hair length extreme bed head wet hair or wind",
    "closed eyes distress intoxication sensual posing viewer-directed focus broad smile or open mouth",
    "repeated d01 side-folded leg pose instead of approved d02 forward-leg pose",
    "wrong outfit exposed underwear shoes slippers bare feet or incorrect sock height or stripes",
    "crop or scale preventing complete support hand leg or foot review",
    "readable text logo watermark border collage grid or multiple character",
)
D02_R01_SHARED_PROMPT_SHA256 = (
    "fe97dbb86b527379a60c5ff4732781adbda0b2501cf3bcedde94ad9ba40e1f38"
)
D03_STATIC_ASSET_CONTRACT = {
    "descriptor": "morning-curtain-pause",
    "phase": 6,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/morning/"
        "akari-v1.2_d03_morning-curtain-pause_rNN.png"
    ],
    "depends_on": ["D02", "C01", "C03", "C05", "C06", "C07"],
    "gate": "daily",
}
D03_R01_REFERENCES = (
    (
        "accepted_d02_morning_continuity",
        "akari-v1.2/accepted/daily/morning/"
        "akari-v1.2_d02_morning-rug-daze_r01.png",
    ),
    (
        "accepted_c01_standing_body",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c01_front-natural-stance_r01.png",
    ),
    (
        "accepted_c03_hairpin_three_quarter",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png",
    ),
    (
        "accepted_c06_morning_hair_sleepy_neutral",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c06-1_sleepy-neutral_r01.png",
    ),
    (
        "accepted_c07_standing_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-standing_r01.png",
    ),
)
D03_R01_SCENE_CONTRACT = {
    "camera": "room-side-front-biased-three-quarter-natural-standing-height",
    "surface": "bedroom-floor-before-frame-left-fully-closed-curtain",
    "continuity": "d02-same-morning-bedroom-outfit-hair-and-window-location",
    "lighting": "soft-diffused-morning-light-through-fully-closed-curtain",
    "gaze": "curtain-edge-directed-with-incomplete-sleepy-focus",
    "pose": "relaxed-standing-low-curtain-touch-weight-away-from-curtain",
    "humanization": [
        "softly-unlocked-leg-sock-light-natural-slouch",
        "low-arm-lift-shoulder-and-t-shirt-hem-asymmetry",
    ],
    "outfit": {
        "top": "loose-opaque-white-short-sleeve-t-shirt",
        "bottom": "simple-opaque-gray-shorts-style-roomwear",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-and-ornament",
        "both-hands-including-low-curtain-side-touch",
        "pelvis-and-complete-bilateral-leg-support",
        "both-ankles-heels-socked-toes-and-floor-contact",
    ],
    "forbidden_props": [
        "mug",
        "phone",
        "clock",
        "readable-book",
        "food",
        "slippers",
        "explanatory-prop",
    ],
}
D03_R01_PRODUCTION_REQUIREMENTS = D02_R01_PRODUCTION_REQUIREMENTS
D03_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d03-scene-staging-curtain-background-lighting-or-presentation"
    ),
    "stop_for_shared_failure": ["D02", "C01", "C03", "C05", "C06", "C07"],
    "cross_candidate_references": "forbidden",
}
D03_R01_ACCEPTANCE_GATES = D02_R01_ACCEPTANCE_GATES
D03_R01_HARD_REJECTS = (
    "severe identity adult-age face body-volume or rendering drift",
    "fused missing duplicated disconnected or untraceable limbs or joints",
    "floating weight broken pelvis-to-leg support twisted ankles pointed toes or contradictory foot contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "non-reversible hair wrong hair length extreme bed head wet hair or wind",
    "closed eyes distress intoxication sensual posing viewer-directed focus broad smile or open mouth",
    "opened curtain bright window gap high reach stretched torso walking stride crossed legs tiptoe or fabric-hanging weight",
    "wrong outfit exposed underwear shoes slippers bare feet or incorrect sock height or stripes",
    "crop preventing complete hand pelvis leg ankle heel toe or floor-contact review",
    "mug phone clock readable book food slippers or explanatory prop",
    "readable text logo watermark border collage grid or multiple character",
)
D03_R01_SHARED_PROMPT_SHA256 = (
    "99285bc78bb11da7585ddd1ac34f070663e1577d59443835dbb9902083728637"
)
D04_STATIC_ASSET_CONTRACT = {
    "descriptor": "morning-drink-fetch",
    "phase": 7,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/morning/"
        "akari-v1.2_d04_morning-drink-fetch_rNN.png"
    ],
    "depends_on": ["D03", "C01", "C03", "C05", "C06", "C07"],
    "gate": "daily",
}
D04_R01_REFERENCES = (
    (
        "accepted_d03_morning_continuity",
        "akari-v1.2/accepted/daily/morning/"
        "akari-v1.2_d03_morning-curtain-pause_r01.png",
    ),
    (
        "accepted_c01_standing_body",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c01_front-natural-stance_r01.png",
    ),
    (
        "accepted_c03_hairpin_three_quarter",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png",
    ),
    (
        "accepted_c06_morning_hair_sleepy_neutral",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c06-1_sleepy-neutral_r01.png",
    ),
    (
        "accepted_c07_standing_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-standing_r01.png",
    ),
)
D04_R01_SCENE_CONTRACT = {
    "camera": "room-side-front-biased-three-quarter-natural-standing-height",
    "surface": "bedroom-threshold-or-short-passage-toward-compact-kitchenette",
    "continuity": "d03-same-morning-outfit-hair-light-and-domestic-palette",
    "lighting": "soft-diffused-morning-light-with-muted-kitchenette-depth",
    "gaze": "kitchenette-directed-with-incomplete-sleepy-focus",
    "pose": "short-slow-step-leading-foot-flat-trailing-heel-lightly-released",
    "humanization": [
        "trailing-leg-sock-slightly-lower-with-light-natural-slouch",
        "walking-counter-swing-t-shirt-hem-and-shoulder-line-shift",
    ],
    "outfit": {
        "top": "loose-opaque-white-short-sleeve-t-shirt",
        "bottom": "simple-opaque-gray-shorts-style-roomwear",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-and-ornament",
        "both-hands-with-small-natural-counter-swing",
        "pelvis-and-complete-bilateral-leg-support",
        "both-ankles-heels-socked-toes-and-relevant-floor-contact",
    ],
    "forbidden_props": [
        "held-drink",
        "mug",
        "glass",
        "bottle",
        "kettle",
        "food",
        "phone",
        "clock",
        "slippers",
        "explanatory-prop",
    ],
}
D04_R01_PRODUCTION_REQUIREMENTS = D02_R01_PRODUCTION_REQUIREMENTS
D04_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d04-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["D03", "C01", "C03", "C05", "C06", "C07"],
    "cross_candidate_references": "forbidden",
}
D04_R01_ACCEPTANCE_GATES = D02_R01_ACCEPTANCE_GATES
D04_R01_HARD_REJECTS = (
    "severe identity adult-age face body-volume or rendering drift",
    "fused missing duplicated disconnected or untraceable limbs or joints",
    "floating weight broken pelvis-to-leg support crossed-leg topology twisted ankles pointed toes or contradictory contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "non-reversible hair wrong hair length extreme bed head wet hair or wind",
    "closed eyes distress intoxication sensual posing viewer-directed focus broad smile or open mouth",
    "wrong outfit exposed underwear shoes slippers bare feet or incorrect sock height or stripes",
    "stationary curtain touching washroom mirror staging open refrigerator held drink long runway stride high reach or running",
    "crop or scale preventing complete head hand pelvis leg ankle heel toe or contact review",
    "readable text logo watermark border collage grid or multiple character",
    "severe mismatch to D03 morning continuity or compact kitchenette threshold intent",
)
D04_R01_SHARED_PROMPT_SHA256 = (
    "d2195a4593426a7a7f4c5b653e6a37f277e3151a04a7e793345ce5b0f4b03cfd"
)
D04_R02_REFERENCES = D04_R01_REFERENCES
D04_R02_SCENE_CONTRACT = {
    "camera": "room-side-profile-biased-three-quarter-moving-frame-right",
    "surface": "bedroom-threshold-or-short-passage-toward-compact-kitchenette",
    "continuity": "d03-same-morning-outfit-hair-light-and-domestic-palette",
    "lighting": "soft-diffused-morning-light-with-muted-kitchenette-depth",
    "gaze": "kitchenette-directed-with-incomplete-sleepy-focus",
    "pose": "short-weight-transfer-on-two-visible-parallel-foot-lanes",
    "humanization": [
        "trailing-leg-sock-slightly-lower-with-light-natural-slouch",
        "weight-transfer-t-shirt-hem-and-shoulder-line-shift",
    ],
    "outfit": {
        "top": "loose-opaque-white-short-sleeve-t-shirt",
        "bottom": "simple-opaque-gray-shorts-style-roomwear",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-and-ornament",
        "both-hands-with-small-natural-counterbalance",
        "pelvis-and-complete-bilateral-leg-support",
        "separate-projected-knee-ankle-and-foot-lanes",
        "both-ankles-heels-socked-toes-and-relevant-floor-contact",
    ],
    "forbidden_props": [
        "held-drink",
        "mug",
        "glass",
        "bottle",
        "kettle",
        "food",
        "phone",
        "clock",
        "slippers",
        "explanatory-prop",
    ],
}
D04_R02_PRODUCTION_REQUIREMENTS = D04_R01_PRODUCTION_REQUIREMENTS
D04_R02_CANDIDATE_POLICY = D04_R01_CANDIDATE_POLICY
D04_R02_ACCEPTANCE_GATES = D04_R01_ACCEPTANCE_GATES
D04_R02_HARD_REJECTS = (
    "severe identity adult-age face body-volume or rendering drift",
    "fused missing duplicated disconnected or untraceable limbs or joints",
    "floating weight broken pelvis-to-leg support crossed or overlapping leg topology twisted ankles pointed toes or contradictory contact",
    "insufficient image-plane gap between projected knees ankles or feet",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "non-reversible hair wrong hair length extreme bed head wet hair or wind",
    "closed eyes distress intoxication sensual posing viewer-directed focus broad smile or open mouth",
    "wrong outfit exposed underwear shoes slippers bare feet or incorrect sock height or stripes",
    "stationary curtain touching washroom mirror staging open refrigerator held drink long runway stride high reach or running",
    "crop or scale preventing complete head hand pelvis leg ankle heel toe or contact review",
    "readable text logo watermark border collage grid or multiple character",
    "severe mismatch to D03 morning continuity or compact kitchenette threshold intent",
)
D04_R02_SHARED_PROMPT_SHA256 = (
    "10c261b7fc7c2ff42a6e7ac28e34b1ba59594011c9e6821db43c4318e502a386"
)
D05_STATIC_ASSET_CONTRACT = {
    "descriptor": "morning-washroom-route",
    "phase": 8,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/morning/"
        "akari-v1.2_d05_morning-washroom-route_rNN.png"
    ],
    "depends_on": ["D04", "C02", "C03", "C05", "C06", "C07"],
    "gate": "daily",
}
D05_R01_REFERENCES = (
    (
        "accepted_d04_morning_continuity",
        "akari-v1.2/accepted/daily/morning/"
        "akari-v1.2_d04_morning-drink-fetch_r02.png",
    ),
    (
        "accepted_c02_rear_body",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c02_back-natural-stance_r01.png",
    ),
    (
        "accepted_c03_hairpin_three_quarter",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png",
    ),
    (
        "accepted_c06_morning_hair_sleepy_neutral",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c06-1_sleepy-neutral_r01.png",
    ),
    (
        "accepted_c07_standing_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-standing_r01.png",
    ),
)
D05_R01_SCENE_CONTRACT = {
    "camera": "hall-side-rear-left-three-quarter-natural-standing-height",
    "destination": "closed-or-barely-ajar-frosted-washroom-door",
    "surface": "short-domestic-hall-with-cool-neutral-threshold",
    "continuity": "d04-same-morning-outfit-hair-light-and-room-palette",
    "lighting": "soft-diffused-morning-light-with-subtle-cool-threshold-depth",
    "gaze": "frosted-door-directed-with-incomplete-sleepy-focus",
    "pose": "momentary-slowdown-on-two-visible-parallel-foot-lanes",
    "humanization": [
        "character-right-short-sleeve-edge-small-accidental-half-fold",
        "back-t-shirt-hem-one-side-higher-with-shallow-diagonal-fold",
    ],
    "outfit": {
        "top": "loose-opaque-white-short-sleeve-t-shirt",
        "bottom": "simple-opaque-gray-shorts-style-roomwear",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-and-character-left-ornament",
        "readable-sleepy-side-three-quarter-face",
        "both-hands-with-small-natural-counterbalance",
        "pelvis-and-complete-bilateral-leg-support",
        "separate-projected-knee-ankle-and-foot-lanes",
        "both-ankles-heels-socked-toes-and-relevant-floor-contact",
    ],
    "forbidden_props": [
        "mirror",
        "sink",
        "toilet",
        "toothbrush",
        "cosmetics",
        "towel-routine",
        "readable-sign",
        "running-water",
        "kitchenette",
        "refrigerator",
        "held-drink",
        "phone",
        "clock",
        "slippers",
        "explanatory-prop",
    ],
}
D05_R01_PRODUCTION_REQUIREMENTS = D02_R01_PRODUCTION_REQUIREMENTS
D05_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d05-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["D04", "C02", "C03", "C05", "C06", "C07"],
    "cross_candidate_references": "forbidden",
}
D05_R01_ACCEPTANCE_GATES = D02_R01_ACCEPTANCE_GATES
D05_R01_HARD_REJECTS = (
    "severe identity adult-age face body-volume continuity or rendering drift",
    "fused missing duplicated disconnected or untraceable limbs or joints",
    "floating weight broken pelvis-to-leg support crossed or overlapping leg topology twisted ankles pointed toes or contradictory contact",
    "insufficient image-plane separation between projected knees ankles or feet",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "non-reversible hair wrong hair length extreme bed head wet hair or wind",
    "closed eyes distress intoxication sensual posing viewer-directed focus broad smile or open mouth",
    "wrong outfit exposed underwear shoes slippers bare feet incorrect sock height stripes or added sock slouch",
    "mirror sink toilet toothbrush cosmetics towel routine running water readable sign or visible washroom routine",
    "kitchenette refrigerator held drink curtain contact long stride high reach or running",
    "crop or scale preventing complete head hand pelvis leg ankle heel toe or contact review",
    "readable text logo watermark border collage grid or multiple character",
)
D05_R01_SHARED_PROMPT_SHA256 = (
    "6d9c74d94f7136913e66900ffe551232277b92a62b06194653c959bef14667bb"
)
D06_STATIC_ASSET_CONTRACT = {
    "descriptor": "evening-entryway-floor-sit",
    "phase": 9,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/evening/"
        "akari-v1.2_d06_evening-entryway-floor-sit_rNN.png"
    ],
    "depends_on": ["D05", "C01", "C03", "C04", "C06", "C07"],
    "gate": "daily",
}
D06_R01_REFERENCES = (
    (
        "accepted_c04_grounded_floor_sitting",
        "akari-v1.2/accepted/core/sitting/"
        "akari-v1.2_c04_floor-sitting_r01.png",
    ),
    (
        "accepted_c01_normal_hair_identity",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c01_front-natural-stance_r01.png",
    ),
    (
        "accepted_c03_hairpin_three_quarter",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png",
    ),
    (
        "accepted_c06_2_safe_relief_expression",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c06-2_sleepy-secure_r01.png",
    ),
    (
        "accepted_c07_seated_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-seated_r01.png",
    ),
)
D06_R01_SCENE_CONTRACT = {
    "camera": "room-side-front-left-three-quarter-natural-seated-height",
    "location": "compact-closed-apartment-entryway",
    "surface": "warm-wood-room-floor-with-shallow-cool-neutral-threshold",
    "continuity": "wave-two-evening-reset-core-standard-outfit-normal-hair",
    "lighting": "warm-soft-evening-interior-with-cool-neutral-door-seam",
    "gaze": "nearby-floor-or-removed-shoes-not-viewer",
    "pose": "controlled-supported-low-floor-sit-after-removing-shoes",
    "humanization": [
        "character-right-hoodie-cuff-pushed-up-one-thumb-width",
        "character-right-sock-slightly-lower-with-both-stripes-complete",
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "return_home_cues": [
        "one-simple-soft-tote-or-shoulder-bag-within-arm-reach",
        "one-neat-pair-removed-white-and-pale-blue-sneakers-at-threshold",
    ],
    "required_visible_features": [
        "complete-head-and-character-left-ornament",
        "open-heavy-lidded-three-quarter-face",
        "both-hands-and-light-floor-support",
        "fully-supported-pelvis-and-light-wall-contact",
        "separately-traceable-raised-and-folded-legs",
        "both-striped-socks-heels-toes-and-floor-contact",
    ],
    "forbidden_props": [
        "open-exterior-door",
        "entering-rain",
        "readable-mail",
        "delivery-boxes",
        "held-keys",
        "phone",
        "food",
        "alcohol",
        "medicine",
        "luggage",
        "multiple-bags",
        "multiple-shoe-pairs",
    ],
}
D06_R01_PRODUCTION_REQUIREMENTS = D02_R01_PRODUCTION_REQUIREMENTS
D06_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d06-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["C01", "C03", "C04", "C06", "C07"],
    "cross_candidate_references": "forbidden",
}
D06_R01_ACCEPTANCE_GATES = D02_R01_ACCEPTANCE_GATES
D06_R01_HARD_REJECTS = (
    "severe identity adult-age face body-volume continuity or rendering drift",
    "fused missing duplicated disconnected crossed or untraceable limbs or joints",
    "floating weight broken sitting or wall support contradictory pelvis leg foot or hand contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "wrong hair length extreme bed head wet hair or wind",
    "closed eyes tears distress despair injury illness intoxication sleep dissociation sensual glamour posing viewer focus broad smile or open mouth",
    "wrong outfit exposed underwear shoes on body bare feet incorrect sock height or stripes",
    "unstable raised knee hidden thigh root fused legs twisted ankles pointed toes or floating feet",
    "open exterior door entering rain readable mail delivery boxes held keys phone food alcohol medicine luggage multiple bags or multiple shoe pairs",
    "crop or scale preventing complete head hand pelvis leg sock heel toe wall support or floor contact review",
    "readable text logo watermark border collage grid or multiple character",
)
D06_R01_SHARED_PROMPT_SHA256 = (
    "232dfa218a312377b7185419bc075b065ba78424bf3616e0069c6f32f2f830ea"
)
D07_STATIC_ASSET_CONTRACT = {
    "descriptor": "evening-shallow-sofa-sit",
    "phase": 10,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/evening/"
        "akari-v1.2_d07_evening-shallow-sofa-sit_rNN.png"
    ],
    "depends_on": ["D06", "C03", "C04", "C06", "C07"],
    "gate": "daily",
}
D07_R01_REFERENCES = (
    (
        "accepted_d06_same_evening_continuity",
        "akari-v1.2/accepted/daily/evening/"
        "akari-v1.2_d06_evening-entryway-floor-sit_r01.png",
    ),
    (
        "accepted_c04_grounded_seated_body",
        "akari-v1.2/accepted/core/sitting/"
        "akari-v1.2_c04_floor-sitting_r01.png",
    ),
    (
        "accepted_c03_hairpin_three_quarter",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png",
    ),
    (
        "accepted_c06_2_safe_relief_expression",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c06-2_sleepy-secure_r01.png",
    ),
    (
        "accepted_c07_seated_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-seated_r01.png",
    ),
)
D07_R01_SCENE_CONTRACT = {
    "camera": "room-side-front-left-three-quarter-natural-seated-height",
    "location": "compact-living-room-corner",
    "seat": "front-third-of-compact-low-backed-neutral-fabric-sofa",
    "continuity": (
        "d06-same-evening-outfit-normal-hair-light-state-and-humanization"
    ),
    "lighting": "warm-diffused-evening-interior",
    "gaze": "blank-low-room-point-not-viewer",
    "pose": "shallow-fully-supported-sofa-edge-sit-with-bilateral-flat-feet",
    "humanization": [
        "character-right-hoodie-cuff-pushed-up-one-thumb-width",
        "character-right-sock-slightly-lower-with-both-stripes-complete",
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-and-character-left-ornament",
        "open-heavy-lidded-three-quarter-face",
        "cushion-side-support-hand-and-thigh-resting-hand",
        "fully-supported-pelvis-and-subtle-cushion-compression",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "both-striped-socks-heels-toes-and-flat-floor-contact",
    ],
    "forbidden_props": [
        "television-content",
        "phone",
        "remote",
        "blanket",
        "mug",
        "food",
        "bag",
        "shoes",
        "entry-door",
        "clock",
        "explanatory-prop",
    ],
}
D07_R01_PRODUCTION_REQUIREMENTS = D02_R01_PRODUCTION_REQUIREMENTS
D07_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d07-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["D06", "C03", "C04", "C06", "C07"],
    "cross_candidate_references": "forbidden",
}
D07_R01_ACCEPTANCE_GATES = D02_R01_ACCEPTANCE_GATES
D07_R01_HARD_REJECTS = (
    "severe identity adult-age face body-volume continuity or rendering drift",
    "fused missing duplicated disconnected crossed hidden or untraceable limbs or joints",
    "floating weight broken sofa cushion pelvis foot or hand support or contradictory contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "wrong hair length extreme bed head wet hair or wind",
    "closed eyes tears distress sadness injury illness intoxication sleep dissociation sensual glamour viewer focus broad smile or open mouth",
    "wrong outfit exposed underwear shoes on body bare feet incorrect sock height or stripes",
    "unstable shallow sit fused legs tiptoe contact twisted ankles pointed toes or floating feet",
    "television content phone remote blanket mug food bag shoes entry door clock or explanatory prop",
    "crop or scale preventing complete head hand pelvis leg sock heel toe cushion edge or floor contact review",
    "readable text logo watermark border collage grid or multiple character",
)
D07_R01_SHARED_PROMPT_SHA256 = (
    "4f35d27ee9941430c4f3a5ff05d409bb035bba946c277fd9d1089acf393e7412"
)
D08_STATIC_ASSET_CONTRACT = {
    "descriptor": "evening-bed-edge-sock-adjust",
    "phase": 11,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/evening/"
        "akari-v1.2_d08_evening-bed-edge-sock-adjust_rNN.png"
    ],
    "depends_on": ["D07", "C03", "C04", "C06", "C07"],
    "gate": "daily",
}
D08_R01_REFERENCES = (
    (
        "accepted_d07_same_evening_continuity",
        "akari-v1.2/accepted/daily/evening/"
        "akari-v1.2_d07_evening-shallow-sofa-sit_r01.png",
    ),
    (
        "accepted_c04_grounded_seated_body",
        "akari-v1.2/accepted/core/sitting/"
        "akari-v1.2_c04_floor-sitting_r01.png",
    ),
    (
        "accepted_c03_hairpin_three_quarter",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png",
    ),
    (
        "accepted_c06_2_safe_relief_expression",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c06-2_sleepy-secure_r01.png",
    ),
    (
        "accepted_c07_seated_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-seated_r01.png",
    ),
)
D08_R01_SCENE_CONTRACT = {
    "camera": "bed-foot-side-front-left-three-quarter-natural-seated-height",
    "location": "compact-bedroom-bedside",
    "seat": "front-band-of-low-neutral-bed-mattress",
    "action": "two-hand-character-right-sock-top-adjustment",
    "continuity": (
        "d07-same-evening-outfit-normal-hair-light-state-and-humanization"
    ),
    "lighting": "warm-diffused-evening-interior",
    "gaze": "working-character-right-sock-not-viewer",
    "pose": "supported-forward-hinge-with-separated-grounded-feet",
    "humanization": [
        "character-right-hoodie-cuff-pushed-up-one-thumb-width",
        (
            "character-right-sock-slightly-lower-mid-adjustment-"
            "with-both-stripes-complete"
        ),
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-and-character-left-ornament",
        "open-heavy-lidded-three-quarter-face",
        "two-separate-hands-on-character-right-sock-top",
        "fully-supported-pelvis-and-subtle-mattress-compression",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "both-striped-socks-heels-toes-and-grounded-floor-contact",
    ],
    "forbidden_props": [
        "phone",
        "clock",
        "mirror",
        "open-drawer",
        "laundry-pile",
        "footwear",
        "bag",
        "food",
        "drink",
        "medicine",
        "television-content",
        "explanatory-prop",
    ],
}
D08_R01_PRODUCTION_REQUIREMENTS = D02_R01_PRODUCTION_REQUIREMENTS
D08_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d08-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["D07", "C03", "C04", "C06", "C07"],
    "cross_candidate_references": "forbidden",
}
D08_R01_ACCEPTANCE_GATES = D02_R01_ACCEPTANCE_GATES
D08_R01_HARD_REJECTS = (
    "severe identity adult-age face body-volume continuity or rendering drift",
    "fused missing duplicated disconnected crossed hidden or untraceable limbs or joints",
    "floating weight broken bed mattress pelvis foot or hand support or contradictory contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "wrong hair length extreme bed head wet hair or wind",
    "closed eyes tears distress sadness pain injury illness intoxication sleep dissociation sensual fetish glamour viewer focus broad smile or open mouth",
    "wrong outfit exposed underwear removed sock bare feet incorrect sock height or stripes",
    "malformed extra or fused fingers unstable forward hinge crossed legs floating heel tiptoe contact twisted ankles or pointed toes",
    "phone clock mirror open drawer laundry pile footwear bag food drink medicine television content or explanatory prop",
    "crop or scale preventing complete head hand pelvis leg sock heel toe mattress edge or floor contact review",
    "readable text logo watermark border collage grid or multiple character",
)
D08_R01_SHARED_PROMPT_SHA256 = (
    "6a7872169740d6edb2fdf4010009f9765bb2c857dbf55c4b323fca4145105882"
)
D08_R02_REFERENCES = D08_R01_REFERENCES
D08_R02_SCENE_CONTRACT = {
    "camera": "bed-foot-side-front-left-three-quarter-natural-seated-height",
    "location": "compact-bedroom-bedside",
    "seat": "front-band-of-low-neutral-bed-mattress",
    "action": "two-hand-character-left-sock-top-smoothing",
    "continuity": (
        "d07-same-evening-outfit-normal-hair-light-state-and-humanization"
    ),
    "lighting": "warm-diffused-evening-interior",
    "gaze": "working-character-left-sock-not-viewer",
    "pose": "supported-forward-hinge-with-separated-grounded-feet",
    "humanization": [
        "character-right-hoodie-cuff-pushed-up-one-thumb-width",
        (
            "untouched-character-right-sock-slightly-lower-"
            "with-both-stripes-complete"
        ),
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-and-character-left-ornament",
        "open-heavy-lidded-three-quarter-face",
        "two-separate-hands-on-character-left-sock-top",
        "fully-supported-pelvis-and-subtle-mattress-compression",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "lower-untouched-character-right-sock-with-both-stripes",
        "both-striped-socks-heels-toes-and-grounded-floor-contact",
    ],
    "forbidden_props": [
        "phone",
        "clock",
        "mirror",
        "open-drawer",
        "laundry-pile",
        "footwear",
        "bag",
        "food",
        "drink",
        "medicine",
        "television-content",
        "explanatory-prop",
    ],
}
D08_R02_PRODUCTION_REQUIREMENTS = D08_R01_PRODUCTION_REQUIREMENTS
D08_R02_CANDIDATE_POLICY = D08_R01_CANDIDATE_POLICY
D08_R02_ACCEPTANCE_GATES = D08_R01_ACCEPTANCE_GATES
D08_R02_HARD_REJECTS = (
    "severe identity adult-age face body-volume continuity or rendering drift",
    "fused missing duplicated disconnected crossed hidden or untraceable limbs or joints",
    "floating weight broken bed mattress pelvis foot or hand support or contradictory contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "wrong hair length extreme bed head wet hair or wind",
    "closed eyes tears distress sadness pain injury illness intoxication sleep dissociation sensual fetish glamour viewer focus broad smile or open mouth",
    "wrong outfit exposed underwear removed sock bare feet incorrect sock height or stripes",
    "malformed extra or fused fingers unstable forward hinge crossed legs floating heel tiptoe contact twisted ankles or pointed toes",
    "hands on character-right sock higher character-right sock or detached sock band strap loop or ribbon",
    "phone clock mirror open drawer laundry pile footwear bag food drink medicine television content or explanatory prop",
    "crop or scale preventing complete head hand pelvis leg sock heel toe mattress edge or floor contact review",
    "readable text logo watermark border collage grid or multiple character",
)
D08_R02_SHARED_PROMPT_SHA256 = (
    "ae2ef17807acbc3377f0b9ff7398e5a7e42a15adb2b2b4a51b1b1539456722ef"
)
D08_R03_REFERENCES = D08_R01_REFERENCES
D08_R03_SCENE_CONTRACT = {
    "camera": (
        "bed-foot-side-front-left-three-quarter-character-left-on-image-right"
    ),
    "location": "compact-bedroom-bedside",
    "seat": "front-band-of-low-neutral-bed-mattress",
    "action": "two-hand-image-right-character-left-sock-top-smoothing",
    "continuity": (
        "d07-same-evening-outfit-normal-hair-light-state-and-humanization"
    ),
    "lighting": "warm-diffused-evening-interior",
    "gaze": "working-image-right-character-left-sock-not-viewer",
    "pose": "supported-forward-hinge-with-separated-grounded-feet",
    "humanization": [
        "character-right-hoodie-cuff-pushed-up-one-thumb-width",
        (
            "image-left-character-right-sock-slightly-lower-"
            "with-both-stripes-complete"
        ),
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-and-image-right-character-left-ornament",
        "open-heavy-lidded-three-quarter-face",
        "two-separate-hands-on-image-right-character-left-sock-top",
        "untouched-lower-image-left-character-right-sock-with-both-stripes",
        "fully-supported-pelvis-and-subtle-mattress-compression",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "both-striped-socks-heels-toes-and-grounded-floor-contact",
    ],
    "forbidden_props": [
        "phone",
        "clock",
        "mirror",
        "open-drawer",
        "laundry-pile",
        "footwear",
        "bag",
        "food",
        "drink",
        "medicine",
        "television-content",
        "explanatory-prop",
    ],
}
D08_R03_PRODUCTION_REQUIREMENTS = D08_R01_PRODUCTION_REQUIREMENTS
D08_R03_CANDIDATE_POLICY = D08_R01_CANDIDATE_POLICY
D08_R03_ACCEPTANCE_GATES = D08_R01_ACCEPTANCE_GATES
D08_R03_HARD_REJECTS = (
    "severe identity adult-age face body-volume continuity or rendering drift",
    "fused missing duplicated disconnected crossed hidden or untraceable limbs or joints",
    "floating weight broken bed mattress pelvis foot or hand support or contradictory contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "wrong hair length extreme bed head wet hair or wind",
    "closed eyes tears distress sadness pain injury illness intoxication sleep dissociation sensual fetish glamour viewer focus broad smile or open mouth",
    "wrong outfit exposed underwear removed sock bare feet incorrect sock height or stripes",
    "malformed extra or fused fingers unstable forward hinge crossed legs floating heel tiptoe contact twisted ankles or pointed toes",
    "hands on image-left character-right sock mirrored working-side relationship higher image-left character-right sock or detached sock band strap loop or ribbon",
    "phone clock mirror open drawer laundry pile footwear bag food drink medicine television content or explanatory prop",
    "crop or scale preventing complete head hand pelvis leg sock heel toe mattress edge or floor contact review",
    "readable text logo watermark border collage grid or multiple character",
)
D08_R03_SHARED_PROMPT_SHA256 = (
    "c7c1b2d82a5c66d2113da17524fb1b42556cc04bf79b2f072b2f787939e58dfc"
)
D09_STATIC_ASSET_CONTRACT = {
    "descriptor": "evening-phone-sleepy-bed-sit",
    "phase": 12,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/evening/"
        "akari-v1.2_d09_evening-phone-sleepy-bed-sit_rNN.png"
    ],
    "depends_on": ["D08", "C03", "C04", "C06", "C07"],
    "gate": "daily",
}
D09_R01_REFERENCES = (
    (
        "accepted_d08_same_evening_bedroom_continuity",
        "akari-v1.2/accepted/daily/evening/"
        "akari-v1.2_d08_evening-bed-edge-sock-adjust_r03.png",
    ),
    (
        "accepted_c04_grounded_seated_body",
        "akari-v1.2/accepted/core/sitting/"
        "akari-v1.2_c04_floor-sitting_r01.png",
    ),
    (
        "accepted_c03_hairpin_three_quarter",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png",
    ),
    (
        "accepted_c06_1_sleepy_awake_expression",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c06-1_sleepy-neutral_r01.png",
    ),
    (
        "accepted_c07_seated_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-seated_r01.png",
    ),
)
D09_R01_SCENE_CONTRACT = {
    "camera": "bed-foot-side-front-left-three-quarter-natural-seated-height",
    "location": "compact-bedroom-deeper-bed-sit",
    "seat": "fully-supported-deeper-low-bed-mattress",
    "action": "two-hand-single-phone-viewing-above-lap",
    "continuity": (
        "d08-same-evening-outfit-normal-hair-room-light-and-humanization"
    ),
    "lighting": "warm-diffused-evening-interior",
    "gaze": "open-heavy-lidded-eyes-on-phone-not-viewer",
    "pose": "lightly-back-supported-relaxed-sit-with-bilateral-flat-feet",
    "humanization": [
        "character-right-hoodie-cuff-pushed-up-one-thumb-width",
        "character-right-sock-slightly-lower-with-both-stripes-complete",
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-and-character-left-ornament",
        "both-eyes-open-heavy-lidded-three-quarter-face",
        "two-separate-hands-holding-one-phone-above-lap",
        "phone-screen-turned-away-and-unreadable",
        "fully-supported-pelvis-and-light-upper-back-support",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "both-striped-socks-heels-toes-and-flat-floor-contact",
    ],
    "forbidden_props": [
        "charger",
        "cable",
        "second-device",
        "clock",
        "mirror",
        "open-drawer",
        "laundry-pile",
        "footwear",
        "bag",
        "food",
        "drink",
        "medicine",
        "television-content",
        "explanatory-prop",
    ],
}
D09_R01_PRODUCTION_REQUIREMENTS = D02_R01_PRODUCTION_REQUIREMENTS
D09_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d09-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["D08", "C03", "C04", "C06", "C07"],
    "cross_candidate_references": "forbidden",
}
D09_R01_ACCEPTANCE_GATES = D02_R01_ACCEPTANCE_GATES
D09_R01_HARD_REJECTS = (
    "severe identity adult-age face body-volume continuity or rendering drift",
    "fused missing duplicated disconnected crossed hidden or untraceable limbs or joints",
    "floating weight broken bed mattress back pelvis foot hand or phone support or contradictory contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "wrong hair length extreme bed head wet hair or wind",
    "closed eyes tears distress sadness pain injury illness intoxication sleep collapse dissociation sensual fetish glamour viewer focus broad smile or open mouth",
    "wrong outfit exposed underwear removed sock bare feet incorrect sock height or stripes",
    "malformed extra or fused fingers broken wrist malformed phone second phone readable screen logo or face-obscuring phone",
    "unstable unsupported slump crossed legs floating heel tiptoe contact twisted ankles or pointed toes",
    "charger cable clock mirror open drawer laundry pile footwear bag food drink medicine television content or explanatory prop",
    "crop or scale preventing complete head hand phone pelvis leg sock heel toe mattress support or floor contact review",
    "readable text logo watermark border collage grid or multiple character",
)
D09_R01_SHARED_PROMPT_SHA256 = (
    "8cf1ea82825d95187f0d172bfefe62224de9f8d1db2815e272801a8de1ca91cf"
)
D10_STATIC_ASSET_CONTRACT = {
    "descriptor": "evening-rug-side-rest",
    "phase": 13,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/evening/akari-v1.2_d10_evening-rug-side-rest_rNN.png"
    ],
    "depends_on": ["D09", "D02", "C03", "C06", "C07"],
    "gate": "daily",
}
D10_R01_REFERENCES = (
    (
        "accepted_d09_same_evening_continuity",
        "akari-v1.2/accepted/daily/evening/"
        "akari-v1.2_d09_evening-phone-sleepy-bed-sit_r01.png",
    ),
    (
        "accepted_d02_plain_rug_contact",
        "akari-v1.2/accepted/daily/morning/"
        "akari-v1.2_d02_morning-rug-daze_r01.png",
    ),
    (
        "accepted_c03_hairpin_three_quarter",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png",
    ),
    (
        "accepted_c06_1_sleepy_awake_expression",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c06-1_sleepy-neutral_r01.png",
    ),
    (
        "accepted_c07_seated_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-seated_r01.png",
    ),
)
D10_R01_SCENE_CONTRACT = {
    "camera": (
        "gently-elevated-front-left-three-quarter-portrait-diagonal-full-body"
    ),
    "location": "same-compact-room-plain-neutral-rug",
    "support": "temple-low-cushion-and-full-body-rug-contact",
    "action": "character-right-side-lying-rest-on-rug",
    "continuity": (
        "d09-same-evening-outfit-normal-hair-light-state-and-humanization"
    ),
    "lighting": "warm-diffused-evening-interior",
    "gaze": "open-heavy-lidded-eyes-down-away-from-viewer",
    "pose": "supported-side-rest-with-separately-traceable-uncrossed-legs",
    "humanization": [
        "character-right-hoodie-cuff-pushed-up-one-thumb-width",
        "character-right-sock-slightly-lower-with-both-stripes-complete",
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-character-left-ornament-and-both-open-eyes",
        "one-low-cushion-under-temple-with-readable-lower-arm",
        "separate-natural-upper-hand-resting-open-on-rug",
        "continuous-ribcage-waist-pelvis-and-rug-support",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "both-striped-socks-heels-and-relaxed-toes",
    ],
    "forbidden_props": [
        "phone",
        "charger",
        "cable",
        "second-cushion",
        "blanket",
        "bed",
        "sofa",
        "clock",
        "mirror",
        "open-drawer",
        "laundry-pile",
        "footwear",
        "bag",
        "food",
        "drink",
        "medicine",
        "television-content",
        "explanatory-prop",
    ],
}
D10_R01_PRODUCTION_REQUIREMENTS = D02_R01_PRODUCTION_REQUIREMENTS
D10_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d10-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["D09", "D02", "C03", "C06", "C07"],
    "cross_candidate_references": "forbidden",
}
D10_R01_ACCEPTANCE_GATES = D02_R01_ACCEPTANCE_GATES
D10_R01_HARD_REJECTS = (
    "severe identity adult-age face body-volume continuity or rendering drift",
    "fused missing duplicated disconnected crossed hidden or untraceable limbs or joints",
    "floating weight broken rug cushion head shoulder ribcage pelvis leg foot or hand support or contradictory contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "wrong hair length extreme bed head wet hair or wind",
    "closed eyes tears distress sadness pain injury illness intoxication sleep collapse dissociation sensual fetish glamour viewer focus broad smile or open mouth",
    "wrong outfit exposed underwear removed sock bare feet incorrect sock height or stripes",
    "malformed extra or fused fingers broken wrist hand trapped under head twisted neck spine shoulder ribcage or pelvis",
    "fused crossed hidden or untraceable legs broken knee or ankle pointed feet or missing heel or toe",
    "phone charger cable second cushion blanket bed sofa clock mirror open drawer laundry pile footwear bag food drink medicine television content or explanatory prop",
    "crop or scale preventing complete head ornament hand torso pelvis leg sock heel toe cushion or rug-contact review",
    "readable text logo watermark border collage grid or multiple character",
)
D10_R01_SHARED_PROMPT_SHA256 = (
    "0aada1d3f1f934b3cb97cf8e145f185a0c19788b3452b168550d9ce77322f918"
)
D11_STATIC_ASSET_CONTRACT = {
    "descriptor": "life-laundry-fold",
    "phase": 14,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/life/akari-v1.2_d11_life-laundry-fold_rNN.png"
    ],
    "depends_on": ["D10", "D07", "D02", "C03", "C07"],
    "gate": "daily",
}
D11_R01_REFERENCES = (
    (
        "accepted_d10_recent_identity_outfit",
        "akari-v1.2/accepted/daily/evening/"
        "akari-v1.2_d10_evening-rug-side-rest_r01.png",
    ),
    (
        "accepted_d02_plain_rug_contact",
        "akari-v1.2/accepted/daily/morning/"
        "akari-v1.2_d02_morning-rug-daze_r01.png",
    ),
    (
        "accepted_c03_hairpin_three_quarter",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png",
    ),
    (
        "accepted_c04_floor_sitting_body",
        "akari-v1.2/accepted/core/sitting/"
        "akari-v1.2_c04_floor-sitting_r01.png",
    ),
    (
        "accepted_c07_seated_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-seated_r01.png",
    ),
)
D11_R01_SCENE_CONTRACT = {
    "camera": "gently-elevated-front-left-three-quarter-portrait-full-body",
    "location": "compact-room-plain-neutral-rug",
    "support": "stable-side-folded-floor-sit-with-rug-contact",
    "action": "two-hand-single-towel-fold-on-rug",
    "continuity": (
        "recent-standard-outfit-normal-hair-and-restrained-room-rendering"
    ),
    "lighting": "soft-diffused-late-afternoon-daylight",
    "gaze": "both-open-eyes-down-at-working-towel",
    "pose": "modest-character-right-side-folded-legs-with-slight-forward-lean",
    "humanization": [
        "character-right-hoodie-cuff-pushed-up-one-thumb-width",
        "one-folded-warm-white-towel-slightly-askew-by-basket",
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-character-left-ornament-and-both-open-eyes",
        "separate-five-finger-hands-on-different-near-towel-corners",
        "one-coherent-pale-blue-rectangular-working-towel",
        "stable-ribcage-pelvis-and-rug-support",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "both-striped-socks-heels-and-relaxed-toes",
        "one-low-basket-and-one-visible-askew-folded-towel",
    ],
    "forbidden_props": [
        "underwear",
        "laundry-socks",
        "shirts",
        "pants",
        "loose-clothing",
        "laundry-machine",
        "detergent",
        "clothesline",
        "phone",
        "charger",
        "cable",
        "bag",
        "drink",
        "food",
        "bed",
        "sofa",
        "mirror",
        "clock",
        "footwear",
        "blanket",
        "second-basket",
        "extra-towel",
        "explanatory-prop",
    ],
}
D11_R01_PRODUCTION_REQUIREMENTS = D02_R01_PRODUCTION_REQUIREMENTS
D11_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d11-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["D10", "D02", "C03", "C04", "C07"],
    "cross_candidate_references": "forbidden",
}
D11_R01_ACCEPTANCE_GATES = D02_R01_ACCEPTANCE_GATES
D11_R01_HARD_REJECTS = (
    "severe identity adult-age face body-volume continuity or rendering drift",
    "fused missing duplicated disconnected hidden or untraceable limbs or joints",
    "floating weight broken rug seated pelvis leg foot hand towel or basket support or contradictory contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "wrong hair length extreme bed head wet hair or wind",
    "closed eyes tears distress sadness pain injury illness intoxication sleep collapse dissociation sensual fetish glamour viewer focus broad smile or open mouth",
    "wrong outfit exposed underwear removed sock bare feet incorrect sock height or stripes",
    "malformed extra or fused fingers broken wrist hidden hand or disconnected arm",
    "fused crossed hidden or untraceable legs broken knee or ankle pointed feet or missing heel or toe",
    "impossible duplicated torn floating or hand-obscuring towel or duplicated malformed floating basket",
    "underwear laundry socks shirts pants loose clothing laundry machine detergent clothesline phone charger cable bag drink food bed sofa mirror clock footwear blanket second basket extra towel or explanatory prop",
    "crop or scale preventing complete head ornament hand towel basket torso pelvis leg sock heel toe or rug-contact review",
    "readable text logo watermark border collage grid or multiple character",
)
D11_R01_SHARED_PROMPT_SHA256 = (
    "905ba4641d561b5e497c3b2bf2f8199b3742e92152858013de9922036795b74f"
)
D11_R02_REFERENCES = (
    (
        "accepted_d10_recent_identity_outfit",
        "akari-v1.2/accepted/daily/evening/"
        "akari-v1.2_d10_evening-rug-side-rest_r01.png",
    ),
    (
        "accepted_d07_shallow_sofa_support",
        "akari-v1.2/accepted/daily/evening/"
        "akari-v1.2_d07_evening-shallow-sofa-sit_r01.png",
    ),
    (
        "accepted_d02_plain_rug_contact",
        "akari-v1.2/accepted/daily/morning/"
        "akari-v1.2_d02_morning-rug-daze_r01.png",
    ),
    (
        "accepted_c03_hairpin_three_quarter",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png",
    ),
    (
        "accepted_c07_seated_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-seated_r01.png",
    ),
)
D11_R02_SCENE_CONTRACT = {
    "camera": "gently-elevated-front-left-three-quarter-portrait-full-body",
    "location": "compact-room-low-neutral-sofa-and-plain-rug",
    "support": "front-sofa-edge-seat-with-bilateral-flat-rug-foot-contact",
    "action": "two-hand-single-towel-fold-across-lap",
    "continuity": (
        "recent-standard-outfit-normal-hair-and-restrained-room-rendering"
    ),
    "lighting": "soft-diffused-late-afternoon-daylight",
    "gaze": "both-open-eyes-down-at-working-towel",
    "pose": "modest-forward-knees-separated-shins-and-flat-feet",
    "humanization": [
        "character-right-hoodie-cuff-pushed-up-one-thumb-width",
        "one-folded-warm-white-towel-slightly-askew-on-sofa",
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-character-left-ornament-and-both-open-eyes",
        "separate-five-finger-hands-on-different-near-towel-corners",
        "one-coherent-pale-blue-rectangular-working-towel-across-lap",
        "stable-ribcage-pelvis-and-sofa-support",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "both-flat-striped-socks-ankles-heels-and-relaxed-toes",
        "one-low-basket-and-one-visible-askew-folded-towel",
    ],
    "forbidden_props": [
        "underwear",
        "laundry-socks",
        "shirts",
        "pants",
        "loose-clothing",
        "washing-machine",
        "detergent",
        "clothesline",
        "phone",
        "charger",
        "cable",
        "bag",
        "drink",
        "food",
        "bed",
        "mirror",
        "clock",
        "footwear",
        "blanket",
        "second-basket",
        "extra-towel",
        "explanatory-prop",
    ],
}
D11_R02_PRODUCTION_REQUIREMENTS = D02_R01_PRODUCTION_REQUIREMENTS
D11_R02_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d11-r02-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["D10", "D07", "D02", "C03", "C07"],
    "cross_candidate_references": "forbidden",
}
D11_R02_ACCEPTANCE_GATES = D02_R01_ACCEPTANCE_GATES
D11_R02_HARD_REJECTS = (
    "severe identity adult-age face body-volume continuity or rendering drift",
    "fused missing duplicated disconnected hidden or untraceable limbs or joints",
    "floating weight broken sofa rug pelvis leg foot hand towel or basket support or contradictory contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "wrong hair length extreme bed head wet hair or wind",
    "closed eyes tears distress sadness pain injury illness intoxication sleep collapse dissociation sensual fetish glamour viewer focus broad smile or open mouth",
    "wrong outfit exposed underwear removed sock bare feet incorrect sock height or stripes",
    "malformed extra or fused fingers broken wrist hidden hand or disconnected arm",
    "fused crossed hidden or untraceable legs one hidden foot broken knee or ankle tiptoe pointed foot or missing heel or toe",
    "impossible duplicated torn floating or hand-obscuring towel or duplicated malformed floating basket",
    "underwear laundry socks shirts pants loose clothing washing machine detergent clothesline phone charger cable bag drink food bed mirror clock footwear blanket second basket extra towel or explanatory prop",
    "crop or scale preventing complete head ornament hand towel basket torso pelvis knee shin sock heel toe sofa or rug-contact review",
    "readable text logo watermark border collage grid or multiple character",
)
D11_R02_SHARED_PROMPT_SHA256 = (
    "23053fd7d904859b74998084b605016399f33c320fb9bdd015c7fbf3ff31aab0"
)
D12_STATIC_ASSET_CONTRACT = {
    "descriptor": "life-fridge-open",
    "phase": 15,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/life/akari-v1.2_d12_life-fridge-open_rNN.png"
    ],
    "depends_on": ["D11", "D04", "C03", "C01", "C07"],
    "gate": "daily",
}
D12_R01_REFERENCES = (
    (
        "accepted_d11_recent_identity_outfit",
        "akari-v1.2/accepted/daily/life/"
        "akari-v1.2_d11_life-laundry-fold_r02.png",
    ),
    (
        "accepted_d04_compact_kitchenette_route",
        "akari-v1.2/accepted/daily/morning/"
        "akari-v1.2_d04_morning-drink-fetch_r02.png",
    ),
    (
        "accepted_c03_hairpin_three_quarter",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png",
    ),
    (
        "accepted_c01_standing_body",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c01_front-natural-stance_r01.png",
    ),
    (
        "accepted_c07_standing_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-standing_r01.png",
    ),
)
D12_R01_SCENE_CONTRACT = {
    "camera": "gently-elevated-front-left-three-quarter-portrait-full-body",
    "location": "compact-plain-kitchenette-with-off-white-refrigerator",
    "support": "upright-standing-with-bilateral-flat-floor-foot-contact",
    "action": "character-right-hand-open-fridge-door",
    "continuity": (
        "recent-standard-outfit-normal-hair-and-restrained-daylight-rendering"
    ),
    "lighting": "soft-diffused-neutral-daytime-light",
    "gaze": "both-open-eyes-into-middle-refrigerator-shelf",
    "pose": "small-body-turn-with-independent-natural-staggered-legs",
    "humanization": [
        "character-right-hoodie-cuff-pushed-up-one-thumb-width",
        "character-right-sock-one-finger-width-lower-with-two-stripes",
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-character-left-ornament-and-both-open-eyes",
        "character-right-five-finger-hand-on-near-vertical-handle",
        "free-character-left-five-finger-hand-beside-hoodie-seam",
        "stable-ribcage-pelvis-and-upright-floor-support",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "both-flat-striped-socks-ankles-heels-and-relaxed-toes",
        "one-coherent-refrigerator-door-hinge-handle-and-shelf-interior",
    ],
    "forbidden_props": [
        "loose-food",
        "recognizable-produce",
        "meat",
        "alcohol",
        "medicine",
        "readable-packaging",
        "magnets",
        "notes",
        "held-item",
        "drink",
        "towel",
        "basket",
        "laundry",
        "phone",
        "charger",
        "cable",
        "bag",
        "clock",
        "mirror",
        "bed",
        "sofa",
        "footwear",
        "explanatory-prop",
    ],
}
D12_R01_PRODUCTION_REQUIREMENTS = D02_R01_PRODUCTION_REQUIREMENTS
D12_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d12-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["D11", "D04", "C03", "C01", "C07"],
    "cross_candidate_references": "forbidden",
}
D12_R01_ACCEPTANCE_GATES = D02_R01_ACCEPTANCE_GATES
D12_R01_HARD_REJECTS = (
    "severe identity adult-age face body-volume continuity or rendering drift",
    "fused missing duplicated disconnected hidden or untraceable limbs or joints",
    "floating weight broken floor pelvis leg foot hand door refrigerator shelf or container support or contradictory contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "wrong hair length extreme bed head wet hair or wind",
    "closed eyes tears distress sadness pain injury illness intoxication sleep collapse dissociation sensual fetish glamour viewer focus broad smile or open mouth",
    "wrong outfit exposed underwear removed sock bare feet incorrect sock height or stripes",
    "malformed extra or fused fingers broken wrist hidden hand disconnected arm or impossible handle grip",
    "fused crossed hidden or untraceable legs one hidden foot broken knee or ankle tiptoe pointed foot or missing heel or toe",
    "impossible duplicated floating or body-obscuring refrigerator door hinge handle shelf or container",
    "loose food recognizable produce meat alcohol medicine readable packaging magnets notes held item drink towel basket laundry phone charger cable bag clock mirror bed sofa footwear or explanatory prop",
    "crop or scale preventing complete head ornament hand handle door torso pelvis knee shin sock heel toe or floor-contact review",
    "readable text logo watermark border collage grid or multiple character",
)
D12_R01_SHARED_PROMPT_SHA256 = (
    "3b6d5958954d1fd3c917250da9b4675bd3c4f85db989411460c5b768911f9a22"
)
D13_STATIC_ASSET_CONTRACT = {
    "descriptor": "life-charger-search",
    "phase": 16,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/life/akari-v1.2_d13_life-charger-search_rNN.png"
    ],
    "depends_on": ["D12", "D04", "C03", "C01", "C07"],
    "gate": "daily",
}
D13_R01_REFERENCES = (
    (
        "accepted_d12_recent_identity_outfit_action",
        "akari-v1.2/accepted/daily/life/"
        "akari-v1.2_d12_life-fridge-open_r01.png",
    ),
    (
        "accepted_d04_compact_room_route",
        "akari-v1.2/accepted/daily/morning/"
        "akari-v1.2_d04_morning-drink-fetch_r02.png",
    ),
    (
        "accepted_c03_hairpin_three_quarter",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png",
    ),
    (
        "accepted_c01_standing_body",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c01_front-natural-stance_r01.png",
    ),
    (
        "accepted_c07_standing_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-standing_r01.png",
    ),
)
D13_R01_SCENE_CONTRACT = {
    "camera": "gently-elevated-front-right-three-quarter-portrait-full-body",
    "location": "compact-plain-room-with-light-wood-desk",
    "support": "upright-standing-with-bilateral-flat-floor-foot-contact",
    "action": "right-hand-open-drawer-left-hand-hover-search",
    "continuity": (
        "recent-standard-outfit-normal-hair-and-restrained-daylight-rendering"
    ),
    "lighting": "soft-diffused-neutral-daytime-light",
    "gaze": "both-open-eyes-down-into-shallow-drawer",
    "pose": "small-forward-hip-lean-with-independent-natural-staggered-legs",
    "humanization": [
        "character-right-hoodie-cuff-pushed-up-one-thumb-width",
        "small-plain-drawer-organizer-slightly-askew",
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-character-left-ornament-and-both-open-eyes",
        "character-right-five-finger-hand-on-centered-drawer-handle",
        "free-character-left-five-finger-hand-hovering-over-contents",
        "stable-ribcage-pelvis-and-upright-floor-support",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "both-flat-striped-socks-ankles-heels-and-relaxed-toes",
        "one-coherent-desk-drawer-organizer-adapter-cable-and-notebook",
    ],
    "forbidden_props": [
        "phone",
        "laptop",
        "tablet",
        "screen",
        "outlet",
        "plugged-cable",
        "extra-cable",
        "power-strip",
        "loose-electronics",
        "readable-labels",
        "held-item",
        "drink",
        "food",
        "towel",
        "basket",
        "laundry",
        "bag",
        "clock",
        "mirror",
        "bed",
        "sofa",
        "refrigerator",
        "footwear",
        "explanatory-prop",
    ],
}
D13_R01_PRODUCTION_REQUIREMENTS = D02_R01_PRODUCTION_REQUIREMENTS
D13_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d13-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["D12", "D04", "C03", "C01", "C07"],
    "cross_candidate_references": "forbidden",
}
D13_R01_ACCEPTANCE_GATES = D02_R01_ACCEPTANCE_GATES
D13_R01_HARD_REJECTS = (
    "severe identity adult-age face body-volume continuity or rendering drift",
    "fused missing duplicated disconnected hidden or untraceable limbs or joints",
    "floating weight broken floor pelvis leg foot hand drawer desk organizer adapter cable or notebook support or contradictory contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "wrong hair length extreme bed head wet hair or wind",
    "closed eyes tears distress sadness pain injury illness intoxication sleep collapse dissociation sensual fetish glamour viewer focus broad smile or open mouth",
    "wrong outfit exposed underwear removed sock bare feet incorrect sock height or stripes",
    "malformed extra or fused fingers broken wrist hidden hand disconnected arm or impossible handle grip",
    "fused crossed hidden or untraceable legs one hidden foot broken knee or ankle tiptoe pointed foot or missing heel or toe",
    "impossible duplicated floating body-obscuring or unsupported drawer desk organizer adapter cable notebook handle or rail",
    "phone laptop tablet screen outlet plugged cable extra cable power strip loose electronics readable labels held item drink food towel basket laundry bag clock mirror bed sofa refrigerator footwear or explanatory prop",
    "crop or scale preventing complete head ornament hand drawer desk torso pelvis knee shin sock heel toe or floor-contact review",
    "readable text logo watermark border collage grid or multiple character",
)
D13_R01_SHARED_PROMPT_SHA256 = (
    "d2aef86cda52955ae40f096b6be78c0a4f8aacfa446173ce36edb3c48817b529"
)
D13_R02_REFERENCES = D13_R01_REFERENCES
D13_R02_SCENE_CONTRACT = {
    "camera": "gently-elevated-front-right-three-quarter-portrait-full-body",
    "location": "compact-plain-room-with-light-wood-desk",
    "support": "upright-standing-with-bilateral-flat-floor-foot-contact",
    "action": "screen-right-hand-open-drawer-screen-left-hand-hover-search",
    "continuity": (
        "recent-standard-outfit-normal-hair-and-restrained-daylight-rendering"
    ),
    "lighting": "soft-diffused-neutral-daytime-light",
    "gaze": "both-open-eyes-down-into-shallow-drawer",
    "pose": "small-forward-hip-lean-with-independent-natural-staggered-legs",
    "humanization": [
        "screen-left-hovering-arm-hoodie-cuff-pushed-up-one-thumb-width",
        "small-plain-drawer-organizer-slightly-askew",
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-character-left-ornament-and-both-open-eyes",
        "screen-right-five-finger-hand-gripping-drawer-front",
        "screen-left-five-finger-hand-hovering-over-contents",
        "stable-ribcage-pelvis-and-upright-floor-support",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "both-flat-striped-socks-ankles-heels-and-relaxed-toes",
        "one-coherent-desk-drawer-organizer-adapter-cable-and-notebook",
    ],
    "forbidden_props": D13_R01_SCENE_CONTRACT["forbidden_props"],
}
D13_R02_PRODUCTION_REQUIREMENTS = D13_R01_PRODUCTION_REQUIREMENTS
D13_R02_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d13-r02-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["D12", "D04", "C03", "C01", "C07"],
    "cross_candidate_references": "forbidden",
}
D13_R02_ACCEPTANCE_GATES = D13_R01_ACCEPTANCE_GATES
D13_R02_HARD_REJECTS = D13_R01_HARD_REJECTS
D13_R02_SHARED_PROMPT_SHA256 = (
    "15bf9b84cb15d2f21b44a665e5cac9821b6a55527f2bc1e37af0a61b8cfc9a65"
)
D14_STATIC_ASSET_CONTRACT = {
    "descriptor": "life-bag-unpack",
    "phase": 17,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/life/akari-v1.2_d14_life-bag-unpack_rNN.png"
    ],
    "depends_on": ["D13", "D11", "D06", "C03", "C07"],
    "gate": "daily",
}
D14_R01_REFERENCES = (
    (
        "accepted_d13_recent_identity_outfit_action",
        "akari-v1.2/accepted/daily/life/"
        "akari-v1.2_d13_life-charger-search_r02.png",
    ),
    (
        "accepted_d11_sofa_edge_support",
        "akari-v1.2/accepted/daily/life/"
        "akari-v1.2_d11_life-laundry-fold_r02.png",
    ),
    (
        "accepted_d06_soft_bag_family",
        "akari-v1.2/accepted/daily/evening/"
        "akari-v1.2_d06_evening-entryway-floor-sit_r01.png",
    ),
    (
        "accepted_c03_hairpin_three_quarter",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png",
    ),
    (
        "accepted_c07_seated_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-seated_r01.png",
    ),
)
D14_R01_SCENE_CONTRACT = {
    "camera": "gently-elevated-front-three-quarter-portrait-full-body",
    "location": "compact-plain-living-room-with-one-sofa",
    "support": "shallow-sofa-edge-sit-with-bilateral-flat-rug-foot-contact",
    "action": (
        "screen-left-hand-hold-bag-open-screen-right-hand-lift-notebook"
    ),
    "continuity": (
        "recent-standard-outfit-normal-hair-and-restrained-daylight-rendering"
    ),
    "lighting": "soft-diffused-neutral-daytime-light",
    "gaze": "both-open-eyes-toward-notebook-and-bag",
    "pose": "small-forward-hip-lean-with-separate-knees-and-shins",
    "humanization": [
        "bag-strap-resting-in-one-loose-curve-on-cushion",
        "one-small-pale-blue-zip-pouch-slightly-askew",
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-character-left-ornament-and-both-open-eyes",
        "screen-left-five-finger-hand-holding-near-bag-rim-open",
        "screen-right-five-finger-hand-lifting-one-notebook-halfway-out",
        "stable-sofa-edge-ribcage-pelvis-and-bilateral-seat-support",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "both-flat-striped-socks-ankles-heels-and-relaxed-toes",
        "one-coherent-open-bag-strap-notebook-pouch-and-handkerchief",
    ],
    "forbidden_props": [
        "phone",
        "wallet",
        "keys",
        "coins",
        "card",
        "charger",
        "cable",
        "adapter",
        "electronics",
        "cosmetics",
        "medicine",
        "food",
        "drink",
        "receipt",
        "ticket",
        "readable-packaging",
        "loose-paper",
        "extra-notebook",
        "extra-pouch",
        "extra-cloth",
        "second-bag",
        "basket",
        "laundry",
        "towel",
        "drawer",
        "desk",
        "refrigerator",
        "footwear",
        "explanatory-prop",
    ],
}
D14_R01_PRODUCTION_REQUIREMENTS = D02_R01_PRODUCTION_REQUIREMENTS
D14_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d14-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["D13", "D11", "D06", "C03", "C07"],
    "cross_candidate_references": "forbidden",
}
D14_R01_ACCEPTANCE_GATES = D02_R01_ACCEPTANCE_GATES
D14_R01_HARD_REJECTS = (
    "severe identity adult-age face body-volume continuity or rendering drift",
    "fused missing duplicated disconnected hidden or untraceable limbs or joints",
    "floating weight broken sofa pelvis leg foot hand bag strap notebook pouch or handkerchief support or contradictory contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "wrong hair length extreme bed head wet hair or wind",
    "closed eyes tears distress sadness pain injury illness intoxication sleep collapse dissociation sensual fetish glamour viewer focus broad smile or open mouth",
    "wrong outfit exposed underwear removed sock bare feet incorrect sock height or stripes",
    "malformed extra or fused fingers broken wrist hidden hand disconnected arm or impossible bag-rim or notebook grip",
    "fused crossed hidden or untraceable legs one hidden foot broken knee or ankle tiptoe pointed foot or missing heel or toe",
    "impossible duplicated floating body-obscuring or unsupported bag mouth rim panel strap zipper notebook pouch handkerchief sofa or cushion",
    "phone wallet keys coins card charger cable adapter electronics cosmetics medicine food drink receipt ticket readable packaging loose paper extra notebook extra pouch extra cloth second bag basket laundry towel drawer desk refrigerator footwear or explanatory prop",
    "crop or scale preventing complete head ornament hand bag notebook sofa torso pelvis knee shin sock heel toe or floor-contact review",
    "readable text logo watermark border collage grid or multiple character",
)
D14_R01_SHARED_PROMPT_SHA256 = (
    "e02cf818a627a59e4646f41a13810563a4dd818446df590c667e4ce0a50df850"
)
D14_R02_REFERENCES = D14_R01_REFERENCES
D14_R02_SCENE_CONTRACT = {
    "camera": "gently-elevated-front-three-quarter-portrait-full-body",
    "location": "compact-plain-living-room-with-one-sofa",
    "support": "shallow-sofa-edge-sit-with-bilateral-flat-rug-foot-contact",
    "action": (
        "one-visible-hand-hold-bag-open-other-visible-hand-lift-notebook"
    ),
    "continuity": (
        "recent-standard-outfit-normal-hair-and-restrained-daylight-rendering"
    ),
    "lighting": "soft-diffused-neutral-daytime-light",
    "gaze": "both-open-eyes-toward-notebook-and-bag",
    "pose": "small-forward-hip-lean-with-separate-knees-and-shins",
    "humanization": [
        "bag-strap-resting-in-one-loose-curve-on-cushion",
        "one-small-pale-blue-zip-pouch-slightly-askew",
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-character-left-ornament-and-both-open-eyes",
        "one-visible-five-finger-hand-holding-near-bag-rim-open",
        "other-visible-five-finger-hand-lifting-one-notebook-halfway-out",
        "stable-sofa-edge-ribcage-pelvis-and-bilateral-seat-support",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "both-flat-striped-socks-ankles-heels-and-relaxed-toes",
        "one-coherent-open-bag-strap-notebook-pouch-and-handkerchief",
    ],
    "forbidden_props": D14_R01_SCENE_CONTRACT["forbidden_props"],
}
D14_R02_PRODUCTION_REQUIREMENTS = D14_R01_PRODUCTION_REQUIREMENTS
D14_R02_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d14-r02-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["D13", "D11", "D06", "C03", "C07"],
    "cross_candidate_references": "forbidden",
}
D14_R02_ACCEPTANCE_GATES = D14_R01_ACCEPTANCE_GATES
D14_R02_HARD_REJECTS = D14_R01_HARD_REJECTS
D14_R02_SHARED_PROMPT_SHA256 = (
    "bb0af84a742a3a3accebdc11907a6d6bb291c2c10545fdbc8aee4c8fa17fdc56"
)
D15_STATIC_ASSET_CONTRACT = {
    "descriptor": "life-pc-posture-break",
    "phase": 18,
    "variants": ["default"],
    "expected_paths": [
        "accepted/daily/life/akari-v1.2_d15_life-pc-posture-break_rNN.png"
    ],
    "depends_on": ["D14", "D13", "D11", "C03", "C07"],
    "gate": "daily",
}
D15_R01_REFERENCES = (
    (
        "accepted_d14_recent_identity_outfit_action",
        "akari-v1.2/accepted/daily/life/"
        "akari-v1.2_d14_life-bag-unpack_r02.png",
    ),
    (
        "accepted_d13_compact_desk_room",
        "akari-v1.2/accepted/daily/life/"
        "akari-v1.2_d13_life-charger-search_r02.png",
    ),
    (
        "accepted_d11_supported_seated_body",
        "akari-v1.2/accepted/daily/life/"
        "akari-v1.2_d11_life-laundry-fold_r02.png",
    ),
    (
        "accepted_c03_hairpin_three_quarter",
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png",
    ),
    (
        "accepted_c07_seated_sock_feet",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-seated_r01.png",
    ),
)
D15_R01_SCENE_CONTRACT = {
    "camera": "gently-elevated-front-three-quarter-portrait-full-body",
    "location": "compact-plain-room-with-light-wood-desk-and-armless-chair",
    "support": (
        "full-chair-seat-lower-back-and-side-rib-support-with-bilateral-flat-feet"
    ),
    "action": "desk-side-elbow-supported-awake-chair-posture-break",
    "continuity": (
        "recent-standard-outfit-normal-hair-and-restrained-daylight-rendering"
    ),
    "lighting": "soft-diffused-neutral-late-afternoon-light",
    "gaze": "both-open-eyes-toward-dark-blank-unreadable-monitor",
    "pose": "mild-supported-sideways-torso-lean-with-relaxed-uneven-shoulders",
    "humanization": [
        "one-small-diagonal-seated-fold-in-front-hoodie-hem",
        "one-plain-compact-keyboard-slightly-askew",
    ],
    "outfit": {
        "top": "oversized-opaque-white-hoodie",
        "bottom": "opaque-gray-pleated-skirt",
        "socks": "warm-white-mid-calf-exactly-two-thin-pale-blue-stripes",
    },
    "required_visible_features": [
        "complete-head-character-left-ornament-and-both-open-eyes",
        "desk-side-five-finger-hand-lightly-supporting-cheek",
        "other-five-finger-hand-open-on-corresponding-thigh",
        "stable-chair-seat-lower-back-ribcage-and-pelvis-support",
        "separately-traceable-bilateral-thigh-knee-shin-lines",
        "both-flat-striped-socks-ankles-heels-and-relaxed-toes",
        "one-coherent-desk-chair-dark-monitor-keyboard-mouse-and-desk-mat",
    ],
    "forbidden_props": [
        "tower",
        "laptop",
        "tablet",
        "phone",
        "second-monitor",
        "second-keyboard",
        "extra-mouse",
        "headset",
        "speaker",
        "webcam",
        "game-controller",
        "charger",
        "cable",
        "adapter",
        "outlet",
        "power-strip",
        "drawer",
        "organizer",
        "notebook",
        "paper",
        "book",
        "pen",
        "clock",
        "mirror",
        "drink",
        "food",
        "medicine",
        "blanket",
        "pillow",
        "bag",
        "laundry",
        "towel",
        "basket",
        "sofa",
        "bed",
        "refrigerator",
        "footwear",
        "explanatory-prop",
    ],
}
D15_R01_PRODUCTION_REQUIREMENTS = D02_R01_PRODUCTION_REQUIREMENTS
D15_R01_CANDIDATE_POLICY = {
    "initial_variants": ["a", "b"],
    "optional_variant": "c",
    "optional_c_only_for": (
        "d15-scene-or-distinct-independent-candidate-local-major-failures"
    ),
    "stop_for_shared_failure": ["D14", "D13", "D11", "C03", "C07"],
    "cross_candidate_references": "forbidden",
}
D15_R01_ACCEPTANCE_GATES = D02_R01_ACCEPTANCE_GATES
D15_R01_HARD_REJECTS = (
    "severe identity adult-age face body-volume state continuity or rendering drift",
    "fused missing duplicated disconnected hidden or untraceable limbs or joints",
    "floating weight broken chair pelvis ribcage leg foot hand elbow desk monitor keyboard or mouse support or contradictory contact",
    "missing mirrored relocated duplicated or materially redesigned ornament",
    "wrong hair length extreme bed head wet hair or wind",
    "closed or half-closed eyes tears distress sadness pain injury illness fever intoxication sleep unconsciousness collapse dissociation sensual fetish glamour viewer focus broad smile or open mouth",
    "wrong outfit exposed underwear removed sock bare feet incorrect sock height or stripes",
    "malformed extra or fused fingers broken wrist hidden hand disconnected arm eye or mouth covered or impossible cheek support",
    "fused crossed hidden or untraceable legs one hidden foot broken knee or ankle tiptoe pointed foot or missing heel or toe",
    "sliding dangling face-down head-on-desk torso-on-desk unsupported-head-drop limp-body or falling-from-chair read",
    "impossible duplicated floating body-obscuring or unsupported chair desk monitor stand keyboard mouse desk mat or floor geometry",
    "monitor interface icon cursor window reflection image glow readable content text or logo",
    "tower laptop tablet phone second monitor second keyboard extra mouse headset speaker webcam game controller charger cable adapter outlet power strip drawer organizer notebook paper book pen clock mirror drink food medicine blanket pillow bag laundry towel basket sofa bed refrigerator footwear or explanatory prop",
    "crop or scale preventing complete head ornament hand chair desk monitor torso pelvis knee shin sock heel toe or floor-contact review",
    "readable text logo watermark border collage grid or multiple character",
)
D15_R01_SHARED_PROMPT_SHA256 = (
    "141a30bec886fd5594bb619623139b9b674d5ccc5f82b109e1ded6a44bd93254"
)
C07_R01_FRAMING_GUIDANCE = {
    "canvas": {"width": 1024, "height": 1536},
    "enforcement": "advisory",
    "views": {
        "standing": {
            "upper_crop": "both-legs-visible-from-at-least-mid-thigh",
            "intended_bottom_margin_pixels": [46, 150],
            "intended_lateral_margin_pixels": 48,
        },
        "seated": {
            "upper_crop": "pelvis-skirt-hem-and-both-thigh-roots-visible",
            "intended_bottom_margin_pixels": [46, 150],
            "intended_lateral_margin_pixels": 48,
        },
    },
    "reject_on_numeric_miss_alone": False,
    "major_only_when": "crop-or-scale-prevents-structural-foot-review",
}


def ordered_value(value):
    if isinstance(value, dict):
        return tuple((key, ordered_value(item)) for key, item in value.items())
    if isinstance(value, list):
        return tuple(ordered_value(item) for item in value)
    return value


GENERATION_REQUEST_CONTRACTS = {
    ("C01", "r01"): {
        "variation_axis": "posture_relaxation",
        "references": (
            ("primary_front_identity", "akari-v1.2/references/v1.1/front.webp"),
            (
                "hairpin_side_identity",
                "akari-v1.2/references/v1.1/hairpin-side-45.webp",
            ),
            (
                "non_hairpin_side_identity",
                "akari-v1.2/references/v1.1/non-hairpin-side-45.webp",
            ),
            ("shoe_construction", "akari-v1.2/references/v1.1/shoes.webp"),
        ),
        "candidate_prefix": "source/candidates/c01/r01/",
        "candidate_stem": "akari-v1.2_c01_front-natural-stance_r01",
        "candidate_detail": "posture_delta",
        "output_specs": None,
        "comparison_anchors": (),
        "framing_contract": None,
        "framing_guidance": None,
        "acceptance_gates": ("identity", "body", "rendering"),
    },
    ("C02", "r01"): {
        "variation_axis": "generation_attempt",
        "references": (
            (
                "accepted_c01_stance",
                "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c01_front-natural-stance_r01.png",
            ),
            ("primary_back_identity", "akari-v1.2/references/v1.1/back.webp"),
            (
                "hairpin_side_identity",
                "akari-v1.2/references/v1.1/hairpin-side-45.webp",
            ),
            (
                "non_hairpin_side_identity",
                "akari-v1.2/references/v1.1/non-hairpin-side-45.webp",
            ),
            ("shoe_construction", "akari-v1.2/references/v1.1/shoes.webp"),
        ),
        "candidate_prefix": "source/candidates/c02/r01/",
        "candidate_stem": "akari-v1.2_c02_back-natural-stance_r01",
        "candidate_detail": None,
        "output_specs": None,
        "comparison_anchors": (
            "accepted/core/standing/"
            "akari-v1.2_c01_front-natural-stance_r01.png",
        ),
        "framing_contract": None,
        "framing_guidance": None,
        "acceptance_gates": ("identity", "body", "rendering"),
    },
    ("C03", "r01"): {
        "variation_axis": "paired_generation_attempt",
        "references": (
            (
                "accepted_c01_front_stance",
                "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c01_front-natural-stance_r01.png",
            ),
            (
                "accepted_c02_back_stance",
                "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c02_back-natural-stance_r01.png",
            ),
            (
                "hairpin_side_identity",
                "akari-v1.2/references/v1.1/hairpin-side-45.webp",
            ),
            (
                "non_hairpin_side_identity",
                "akari-v1.2/references/v1.1/non-hairpin-side-45.webp",
            ),
            ("shoe_construction", "akari-v1.2/references/v1.1/shoes.webp"),
        ),
        "candidate_prefix": "source/candidates/c03/r01/",
        "candidate_detail": None,
        "output_specs": (
            ("hairpin-side-45", "akari-v1.2_c03_hairpin-side-45_r01"),
            (
                "non-hairpin-side-45",
                "akari-v1.2_c03_non-hairpin-side-45_r01",
            ),
        ),
        "comparison_anchors": (
            "accepted/core/standing/"
            "akari-v1.2_c01_front-natural-stance_r01.png",
            "accepted/core/standing/"
            "akari-v1.2_c02_back-natural-stance_r01.png",
        ),
        "pair_generation_policy": {
            "first_view": "hairpin-side-45",
            "second_view": "non-hairpin-side-45",
            "second_view_additional_reference": {
                "role": "paired_candidate_anchor",
                "source_view": "hairpin-side-45",
                "priority": "supporting",
            },
        },
        "view_names": ("hairpin-side-45", "non-hairpin-side-45"),
        "framing_contract": None,
        "framing_guidance": None,
        "acceptance_gates": ("identity", "body", "rendering"),
    },
    ("C03", "r02"): {
        "variation_axis": "paired_generation_attempt",
        "references": (
            (
                "accepted_c01_front_stance",
                "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c01_front-natural-stance_r01.png",
            ),
            (
                "accepted_c02_back_stance",
                "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c02_back-natural-stance_r01.png",
            ),
            (
                "hairpin_side_identity",
                "akari-v1.2/references/v1.1/hairpin-side-45.webp",
            ),
            (
                "non_hairpin_side_identity",
                "akari-v1.2/references/v1.1/non-hairpin-side-45.webp",
            ),
            ("shoe_construction", "akari-v1.2/references/v1.1/shoes.webp"),
        ),
        "candidate_prefix": "source/candidates/c03/r02/",
        "candidate_detail": None,
        "output_specs": (
            ("hairpin-side-45", "akari-v1.2_c03_hairpin-side-45_r02"),
            (
                "non-hairpin-side-45",
                "akari-v1.2_c03_non-hairpin-side-45_r02",
            ),
        ),
        "comparison_anchors": (
            "accepted/core/standing/"
            "akari-v1.2_c01_front-natural-stance_r01.png",
            "accepted/core/standing/"
            "akari-v1.2_c02_back-natural-stance_r01.png",
        ),
        "pair_generation_policy": {
            "first_view": "hairpin-side-45",
            "second_view": "non-hairpin-side-45",
            "second_view_additional_reference": {
                "role": "paired_candidate_anchor",
                "source_view": "hairpin-side-45",
                "priority": "supporting",
            },
        },
        "view_names": ("hairpin-side-45", "non-hairpin-side-45"),
        "framing_contract": C03_R02_FRAMING_CONTRACT,
        "framing_guidance": None,
        "acceptance_gates": ("identity", "body", "rendering"),
    },
    ("C04", "r01"): {
        "variation_axis": "independent_generation_attempt",
        "references": (
            (
                "accepted_c01_front_identity",
                "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c01_front-natural-stance_r01.png",
            ),
            (
                "accepted_c03_hairpin_three_quarter",
                "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c03_hairpin-side-45_r02.png",
            ),
            (
                "v1_1_indoor_foot_construction",
                "akari-v1.2/references/v1.1/standard-foot-set.webp",
            ),
            (
                "legacy_seated_anatomy_warning",
                "akari-v1.2/references/legacy/seated.webp",
            ),
        ),
        "candidate_prefix": "source/candidates/c04/r01/",
        "candidate_stem": "akari-v1.2_c04_floor-sitting_r01",
        "candidate_detail": None,
        "output_specs": None,
        "comparison_anchors": (),
        "framing_contract": None,
        "framing_guidance": C04_R01_FRAMING_GUIDANCE,
        "acceptance_gates": ("identity", "body", "rendering"),
    },
    ("C05", "r01"): {
        "variation_axis": "independent_generation_attempt",
        "references": (
            (
                "accepted_c01_front_identity",
                "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c01_front-natural-stance_r01.png",
            ),
            (
                "accepted_c03_hairpin_three_quarter",
                "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c03_hairpin-side-45_r02.png",
            ),
            (
                "supporting_sleepy_expression",
                "akari-v1.2/references/supporting/sleepy-reply-v3.webp",
            ),
            (
                "supporting_morning_hair",
                "akari-v1.2/references/supporting/morning-glance-h05.png",
            ),
        ),
        "candidate_prefix": "source/candidates/c05/r01/",
        "candidate_stem": "akari-v1.2_c05_morning-bedhair_r01",
        "candidate_detail": None,
        "candidate_fields": ("variant", "title", "target_path"),
        "candidate_titles": (
            "independent-attempt-a",
            "independent-attempt-b",
            "independent-attempt-c",
        ),
        "output_specs": None,
        "comparison_anchors": (),
        "framing_contract": None,
        "framing_guidance": C05_R01_FRAMING_GUIDANCE,
        "acceptance_gates": ("identity", "state", "rendering"),
        "required_prompt_phrases": (
            "C01 controls the 25-year-old adult identity",
            "C03 r02 controls the character-left pale-blue crossed pins",
            "one or two small crown lifts or flyaways",
            "a light asymmetric separation in the bangs",
            "a partial outward nape flick with small lower-bob end irregularity",
            "one soft strand falling toward a cheek",
            "slightly heavy upper eyelids without substantially shrinking the eyes",
            "a viewer-directed gaze that is not fully focused",
            "closed neutral lips with no smile",
            "No hands, props, furniture, bed, window, room scene",
            "Do not add the C06 smile progression or D01 room-scene content",
        ),
        "hard_rejects": (
            "severe identity age face-shape or eye-construction drift",
            "missing mirrored relocated duplicated or materially redesigned ornament",
            "corrupted face eyes hair or hoodie construction",
            "different longer windblown wet or extreme-bed-head hairstyle",
            "sleepiness shown only by closed or substantially shrunken eyes",
            "sultry intoxicated ill distressed childlike or strong-blush drift",
            "smile yawn open-mouth emphasis cheek-rest hand prop or room-scene leak",
            "crop or scale that prevents complete face hair ornament or hoodie review",
            "readable text logo watermark border grid collage or multiple character",
        ),
    },
    ("C06", "r01"): {
        "variation_axis": "expression_gradient_family_attempt",
        "references": (
            (
                "accepted_c05_edit_source",
                "akari-v1.2/accepted/core/face-hair/"
                "akari-v1.2_c05_morning-bedhair_r01.png",
            ),
            (
                "accepted_c01_identity_crosscheck",
                "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c01_front-natural-stance_r01.png",
            ),
            (
                "accepted_c03_hairpin_three_quarter",
                "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c03_hairpin-side-45_r02.png",
            ),
            (
                "v1_1_expression_range",
                "akari-v1.2/references/v1.1/expression-grid.webp",
            ),
        ),
        "comparison_anchors": (),
        "framing_contract": None,
        "framing_guidance": C06_R01_FRAMING_GUIDANCE,
        "acceptance_gates": ("identity", "state", "rendering"),
        "required_prompt_phrases": (
            "Edit Image 1 directly",
            "Image 1 is the controlling accepted C05 edit source",
            "or intentionally reshape the C05 face",
            "non-controlling expression-range reference",
            "Preserve C05 face width",
            "Change only upper-eyelid opening",
            "No hands, props, furniture, bed, window, room scene",
        ),
        "hard_rejects": (
            "severe identity age face-shape chin or base-eye drift",
            "progressively narrower face sharper chin younger age or larger doll-like eyes",
            "corrupted asymmetric duplicated or disconnected facial features",
            "missing mirrored relocated duplicated or redesigned ornament",
            "material crop head-angle hairstyle outfit backdrop lighting palette or rendering drift",
            "indistinguishable reversed or abrupt expression-stage progression",
            "sleepiness shown mainly through closed or substantially shrunken eyes",
            "sadness distress pout intoxication illness sensuality or strong-blush drift",
            "yawn teeth open mouth laughter performative grin or extra pose",
            "wrong dimensions corrupt file or unreadable complete face-and-hair crop",
            "readable text logo watermark border grid collage or multiple character",
        ),
    },
    ("C07", "r01"): {
        "variation_axis": "paired_generation_attempt",
        "candidate_variants": ("a", "b"),
        "references": (
            (
                "accepted_c01_standing_body",
                "akari-v1.2/accepted/core/standing/"
                "akari-v1.2_c01_front-natural-stance_r01.png",
            ),
            (
                "accepted_c04_seated_body",
                "akari-v1.2/accepted/core/sitting/"
                "akari-v1.2_c04_floor-sitting_r01.png",
            ),
            (
                "v1_1_indoor_sock_construction",
                "akari-v1.2/references/v1.1/standard-foot-set.webp",
            ),
        ),
        "candidate_prefix": "source/candidates/c07/r01/",
        "candidate_detail": None,
        "output_specs": (
            ("standing", "akari-v1.2_c07_indoor-socks-standing_r01"),
            ("seated", "akari-v1.2_c07_indoor-socks-seated_r01"),
        ),
        "comparison_anchors": (),
        "pair_generation_policy": {
            "first_view": "standing",
            "second_view": "seated",
            "second_view_additional_reference": {
                "role": "paired_standing_sock_anchor",
                "source_view": "standing",
                "priority": "supporting",
            },
        },
        "view_names": ("standing", "seated"),
        "framing_contract": None,
        "framing_guidance": C07_R01_FRAMING_GUIDANCE,
        "acceptance_gates": ("body", "rendering"),
    },
    ("D01", "r01"): {
        "descriptor": "morning-bedside",
        "variation_axis": "independent_scene_attempt",
        "references": D01_R01_REFERENCES,
        "scene_contract": D01_R01_SCENE_CONTRACT,
        "production_requirements": D01_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D01_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D01_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D01_R01_ACCEPTANCE_GATES,
        "hard_rejects": D01_R01_HARD_REJECTS,
    },
    ("D02", "r01"): {
        "descriptor": "morning-rug-daze",
        "variation_axis": "independent_scene_attempt",
        "references": D02_R01_REFERENCES,
        "scene_contract": D02_R01_SCENE_CONTRACT,
        "production_requirements": D02_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D02_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D02_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D02_R01_ACCEPTANCE_GATES,
        "hard_rejects": D02_R01_HARD_REJECTS,
    },
    ("D03", "r01"): {
        "descriptor": "morning-curtain-pause",
        "variation_axis": "independent_scene_attempt",
        "references": D03_R01_REFERENCES,
        "scene_contract": D03_R01_SCENE_CONTRACT,
        "production_requirements": D03_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D03_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D03_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D03_R01_ACCEPTANCE_GATES,
        "hard_rejects": D03_R01_HARD_REJECTS,
    },
    ("D04", "r01"): {
        "descriptor": "morning-drink-fetch",
        "variation_axis": "independent_scene_attempt",
        "references": D04_R01_REFERENCES,
        "scene_contract": D04_R01_SCENE_CONTRACT,
        "production_requirements": D04_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D04_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D04_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D04_R01_ACCEPTANCE_GATES,
        "hard_rejects": D04_R01_HARD_REJECTS,
    },
    ("D04", "r02"): {
        "descriptor": "morning-drink-fetch",
        "variation_axis": "independent_scene_attempt",
        "references": D04_R02_REFERENCES,
        "scene_contract": D04_R02_SCENE_CONTRACT,
        "production_requirements": D04_R02_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D04_R02_CANDIDATE_POLICY,
        "shared_prompt_sha256": D04_R02_SHARED_PROMPT_SHA256,
        "acceptance_gates": D04_R02_ACCEPTANCE_GATES,
        "hard_rejects": D04_R02_HARD_REJECTS,
    },
    ("D05", "r01"): {
        "descriptor": "morning-washroom-route",
        "variation_axis": "independent_scene_attempt",
        "references": D05_R01_REFERENCES,
        "scene_contract": D05_R01_SCENE_CONTRACT,
        "production_requirements": D05_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D05_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D05_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D05_R01_ACCEPTANCE_GATES,
        "hard_rejects": D05_R01_HARD_REJECTS,
    },
    ("D06", "r01"): {
        "descriptor": "evening-entryway-floor-sit",
        "variation_axis": "independent_scene_attempt",
        "references": D06_R01_REFERENCES,
        "scene_contract": D06_R01_SCENE_CONTRACT,
        "production_requirements": D06_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D06_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D06_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D06_R01_ACCEPTANCE_GATES,
        "hard_rejects": D06_R01_HARD_REJECTS,
    },
    ("D07", "r01"): {
        "descriptor": "evening-shallow-sofa-sit",
        "variation_axis": "independent_scene_attempt",
        "references": D07_R01_REFERENCES,
        "scene_contract": D07_R01_SCENE_CONTRACT,
        "production_requirements": D07_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D07_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D07_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D07_R01_ACCEPTANCE_GATES,
        "hard_rejects": D07_R01_HARD_REJECTS,
    },
    ("D08", "r01"): {
        "descriptor": "evening-bed-edge-sock-adjust",
        "variation_axis": "independent_scene_attempt",
        "references": D08_R01_REFERENCES,
        "scene_contract": D08_R01_SCENE_CONTRACT,
        "production_requirements": D08_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D08_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D08_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D08_R01_ACCEPTANCE_GATES,
        "hard_rejects": D08_R01_HARD_REJECTS,
    },
    ("D08", "r02"): {
        "descriptor": "evening-bed-edge-sock-adjust",
        "variation_axis": "independent_scene_attempt",
        "references": D08_R02_REFERENCES,
        "scene_contract": D08_R02_SCENE_CONTRACT,
        "production_requirements": D08_R02_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D08_R02_CANDIDATE_POLICY,
        "shared_prompt_sha256": D08_R02_SHARED_PROMPT_SHA256,
        "acceptance_gates": D08_R02_ACCEPTANCE_GATES,
        "hard_rejects": D08_R02_HARD_REJECTS,
    },
    ("D08", "r03"): {
        "descriptor": "evening-bed-edge-sock-adjust",
        "variation_axis": "independent_scene_attempt",
        "references": D08_R03_REFERENCES,
        "scene_contract": D08_R03_SCENE_CONTRACT,
        "production_requirements": D08_R03_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D08_R03_CANDIDATE_POLICY,
        "shared_prompt_sha256": D08_R03_SHARED_PROMPT_SHA256,
        "acceptance_gates": D08_R03_ACCEPTANCE_GATES,
        "hard_rejects": D08_R03_HARD_REJECTS,
    },
    ("D09", "r01"): {
        "descriptor": "evening-phone-sleepy-bed-sit",
        "variation_axis": "independent_scene_attempt",
        "references": D09_R01_REFERENCES,
        "scene_contract": D09_R01_SCENE_CONTRACT,
        "production_requirements": D09_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D09_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D09_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D09_R01_ACCEPTANCE_GATES,
        "hard_rejects": D09_R01_HARD_REJECTS,
    },
    ("D10", "r01"): {
        "descriptor": "evening-rug-side-rest",
        "variation_axis": "independent_scene_attempt",
        "references": D10_R01_REFERENCES,
        "scene_contract": D10_R01_SCENE_CONTRACT,
        "production_requirements": D10_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D10_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D10_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D10_R01_ACCEPTANCE_GATES,
        "hard_rejects": D10_R01_HARD_REJECTS,
    },
    ("D11", "r01"): {
        "descriptor": "life-laundry-fold",
        "variation_axis": "independent_scene_attempt",
        "references": D11_R01_REFERENCES,
        "scene_contract": D11_R01_SCENE_CONTRACT,
        "production_requirements": D11_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D11_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D11_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D11_R01_ACCEPTANCE_GATES,
        "hard_rejects": D11_R01_HARD_REJECTS,
    },
    ("D11", "r02"): {
        "descriptor": "life-laundry-fold",
        "variation_axis": "independent_scene_attempt",
        "references": D11_R02_REFERENCES,
        "scene_contract": D11_R02_SCENE_CONTRACT,
        "production_requirements": D11_R02_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D11_R02_CANDIDATE_POLICY,
        "shared_prompt_sha256": D11_R02_SHARED_PROMPT_SHA256,
        "acceptance_gates": D11_R02_ACCEPTANCE_GATES,
        "hard_rejects": D11_R02_HARD_REJECTS,
    },
    ("D12", "r01"): {
        "descriptor": "life-fridge-open",
        "variation_axis": "independent_scene_attempt",
        "references": D12_R01_REFERENCES,
        "scene_contract": D12_R01_SCENE_CONTRACT,
        "production_requirements": D12_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D12_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D12_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D12_R01_ACCEPTANCE_GATES,
        "hard_rejects": D12_R01_HARD_REJECTS,
    },
    ("D13", "r01"): {
        "descriptor": "life-charger-search",
        "variation_axis": "independent_scene_attempt",
        "references": D13_R01_REFERENCES,
        "scene_contract": D13_R01_SCENE_CONTRACT,
        "production_requirements": D13_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D13_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D13_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D13_R01_ACCEPTANCE_GATES,
        "hard_rejects": D13_R01_HARD_REJECTS,
    },
    ("D13", "r02"): {
        "descriptor": "life-charger-search",
        "variation_axis": "independent_scene_attempt",
        "references": D13_R02_REFERENCES,
        "scene_contract": D13_R02_SCENE_CONTRACT,
        "production_requirements": D13_R02_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D13_R02_CANDIDATE_POLICY,
        "shared_prompt_sha256": D13_R02_SHARED_PROMPT_SHA256,
        "acceptance_gates": D13_R02_ACCEPTANCE_GATES,
        "hard_rejects": D13_R02_HARD_REJECTS,
    },
    ("D14", "r01"): {
        "descriptor": "life-bag-unpack",
        "variation_axis": "independent_scene_attempt",
        "references": D14_R01_REFERENCES,
        "scene_contract": D14_R01_SCENE_CONTRACT,
        "production_requirements": D14_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D14_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D14_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D14_R01_ACCEPTANCE_GATES,
        "hard_rejects": D14_R01_HARD_REJECTS,
    },
    ("D14", "r02"): {
        "descriptor": "life-bag-unpack",
        "variation_axis": "independent_scene_attempt",
        "references": D14_R02_REFERENCES,
        "scene_contract": D14_R02_SCENE_CONTRACT,
        "production_requirements": D14_R02_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D14_R02_CANDIDATE_POLICY,
        "shared_prompt_sha256": D14_R02_SHARED_PROMPT_SHA256,
        "acceptance_gates": D14_R02_ACCEPTANCE_GATES,
        "hard_rejects": D14_R02_HARD_REJECTS,
    },
    ("D15", "r01"): {
        "descriptor": "life-pc-posture-break",
        "variation_axis": "independent_scene_attempt",
        "references": D15_R01_REFERENCES,
        "scene_contract": D15_R01_SCENE_CONTRACT,
        "production_requirements": D15_R01_PRODUCTION_REQUIREMENTS,
        "candidate_policy": D15_R01_CANDIDATE_POLICY,
        "shared_prompt_sha256": D15_R01_SHARED_PROMPT_SHA256,
        "acceptance_gates": D15_R01_ACCEPTANCE_GATES,
        "hard_rejects": D15_R01_HARD_REJECTS,
    },
}


validate_d01_png_dimensions = partial(
    validate_daily_png_dimensions,
    asset_id="D01",
    revision="r01",
    requirements=D01_R01_PRODUCTION_REQUIREMENTS,
)
validate_d01_candidate_dimensions = validate_daily_candidate_dimensions


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: expected mapping")
    return data


def load_generation_requests(request_root: Path) -> list[dict]:
    requests = [load_yaml(path) for path in sorted(request_root.glob("*.yaml"))]
    keys = [(item.get("asset_id"), item.get("revision")) for item in requests]
    if len(keys) != len(set(keys)):
        raise ValidationError("generation requests: duplicate asset revision")
    return sorted(requests, key=lambda item: (item["asset_id"], item["revision"]))


def count_generation_work(requests: list[dict]) -> tuple[int, int]:
    candidate_count = sum(len(request["candidates"]) for request in requests)
    output_count = sum(
        len(candidate.get("outputs", [candidate]))
        for request in requests
        for candidate in request["candidates"]
    )
    for request in requests:
        repair = request.get("repair_lane")
        if (
            (request.get("asset_id"), request.get("revision")) == ("C06", "r01")
            and isinstance(repair, dict)
            and repair.get("mode") == "targeted-stage"
        ):
            output_count += 1
    return candidate_count, output_count


def c06_candidate_path(stage: str, descriptor: str, variant: str) -> str:
    return (
        "source/candidates/c06/r01/"
        f"akari-v1.2_{stage}_{descriptor}_r01-{variant}.png"
    )


def validate_c06_generation_request(data: dict, contract: dict) -> None:
    stages = data.get("stages")
    if (
        not isinstance(stages, list)
        or not all(isinstance(item, dict) for item in stages)
        or [
            (item.get("stage"), item.get("descriptor")) for item in stages
        ]
        != list(C06_R01_STAGE_PAIRS)
    ):
        raise ValidationError("C06 stage contract mismatch")
    if any(
        set(item) != {"stage", "descriptor", "prompt_delta"}
        or not isinstance(item["prompt_delta"], str)
        or not all(
            phrase in item["prompt_delta"]
            for phrase in C06_R01_STAGE_REQUIRED_PHRASES[item["stage"]]
        )
        for item in stages
    ):
        raise ValidationError("C06 stage prompt contract mismatch")
    actual_stage_hashes = {
        item["stage"]: hashlib.sha256(
            item["prompt_delta"].encode("utf-8")
        ).hexdigest()
        for item in stages
    }
    if actual_stage_hashes != {
        stage: C06_R01_EXACT_PROMPT_SHA256[stage]
        for stage, _ in C06_R01_STAGE_PAIRS
    }:
        raise ValidationError("C06 exact stage prompt contract mismatch")
    if data.get("edit_policy") != C06_R01_EDIT_POLICY:
        raise ValidationError("C06 edit policy contract mismatch")
    if data.get("production_requirements") != C06_R01_PRODUCTION_REQUIREMENTS:
        raise ValidationError("C06 production contract mismatch")

    repair = data.get("repair_lane")
    if not isinstance(repair, dict):
        raise ValidationError("C06 repair contract mismatch")
    mode = repair.get("mode")
    expected_variants = ["a", "b", "c"] if mode == "full-family" else ["a", "b"]
    candidates = data.get("candidates")
    if (
        not isinstance(candidates, list)
        or not all(isinstance(candidate, dict) for candidate in candidates)
        or [candidate.get("variant") for candidate in candidates]
        != expected_variants
    ):
        raise ValidationError("C06 candidate family contract mismatch")

    expected_sets = []
    sources_by_variant = {}
    for variant, candidate in zip(expected_variants, candidates):
        if set(candidate) != {"variant", "title", "outputs"}:
            raise ValidationError("C06 candidate family contract mismatch")
        if candidate.get("title") != f"complete-family-{variant}":
            raise ValidationError("C06 candidate family contract mismatch")
        expected_outputs = [
            {
                "stage": stage,
                "descriptor": descriptor,
                "edit_source_role": "accepted_c05_edit_source",
                "target_path": c06_candidate_path(stage, descriptor, variant),
            }
            for stage, descriptor in C06_R01_STAGE_PAIRS
        ]
        if candidate.get("outputs") != expected_outputs:
            raise ValidationError("C06 candidate output contract mismatch")
        sources_by_variant[variant] = [
            output["target_path"] for output in expected_outputs
        ]
        if variant in {"a", "b"}:
            expected_sets.append(
                {
                    "candidate_id": f"c06-r01-{variant}",
                    "source_paths": sources_by_variant[variant],
                }
            )

    if mode == "inactive":
        if repair != {"mode": "inactive"}:
            raise ValidationError("C06 inactive repair contract mismatch")
    elif mode == "targeted-stage":
        base = repair.get("base_family")
        stage = repair.get("stage")
        if base not in {"a", "b"} or stage not in {
            item[0] for item in C06_R01_STAGE_PAIRS
        }:
            raise ValidationError("C06 targeted repair contract mismatch")
        stage_index = [item[0] for item in C06_R01_STAGE_PAIRS].index(stage)
        descriptor = C06_R01_STAGE_PAIRS[stage_index][1]
        target = c06_candidate_path(stage, descriptor, "c")
        if repair != {
            "mode": "targeted-stage",
            "base_family": base,
            "stage": stage,
            "target_path": target,
        }:
            raise ValidationError("C06 targeted repair contract mismatch")
        mixed = list(sources_by_variant[base])
        mixed[stage_index] = target
        expected_sets.append(
            {
                "candidate_id": f"c06-r01-{base}-repair-{stage}",
                "source_paths": mixed,
            }
        )
    elif mode == "full-family":
        if repair != {"mode": "full-family"}:
            raise ValidationError("C06 full repair contract mismatch")
        expected_sets.append(
            {
                "candidate_id": "c06-r01-c",
                "source_paths": sources_by_variant["c"],
            }
        )
    else:
        raise ValidationError("C06 repair contract mismatch")

    if data.get("review_sets") != expected_sets:
        raise ValidationError("C06 review set contract mismatch")

    if data.get("comparison_anchors") != []:
        raise ValidationError("C06 comparison anchors mismatch")
    if "framing_contract" in data:
        raise ValidationError("C06 unexpected framing contract")
    if ordered_value(data.get("framing_guidance")) != ordered_value(
        contract["framing_guidance"]
    ):
        raise ValidationError("C06 exact framing guidance required")
    shared_prompt = data.get("shared_prompt")
    if not isinstance(shared_prompt, str) or not shared_prompt.strip():
        raise ValidationError("C06 shared prompt required")
    if any(
        phrase not in shared_prompt
        for phrase in contract["required_prompt_phrases"]
    ):
        raise ValidationError("C06 required prompt phrase missing")
    if hashlib.sha256(shared_prompt.encode("utf-8")).hexdigest() != (
        C06_R01_EXACT_PROMPT_SHA256["shared"]
    ):
        raise ValidationError("C06 exact shared prompt contract mismatch")
    if data.get("acceptance_gates") != list(contract["acceptance_gates"]):
        raise ValidationError("C06 acceptance gates mismatch")
    if data.get("hard_rejects") != list(contract["hard_rejects"]):
        raise ValidationError("C06 exact hard rejects required")


def validate_generation_request(data: dict) -> None:
    if data.get("schema_version") != 1:
        raise ValidationError("generation request: schema_version must be 1")
    key = (data.get("asset_id"), data.get("revision"))
    contract = GENERATION_REQUEST_CONTRACTS.get(key)
    if contract is None:
        raise ValidationError(f"generation request: unsupported request {key}")
    if data.get("request_id") != f"akari-v1.2-{key[0].lower()}-{key[1]}":
        raise ValidationError("generation request: request_id mismatch")
    if data.get("variation_axis") != contract["variation_axis"]:
        raise ValidationError("generation request: invalid variation axis")
    references = data.get("references")
    if (
        not isinstance(references, list)
        or len(references) != len(contract["references"])
        or not all(isinstance(item, dict) for item in references)
    ):
        raise ValidationError("generation request: exact reference contract required")
    actual = tuple((item.get("role"), item.get("path")) for item in references)
    if actual != contract["references"]:
        raise ValidationError("generation request: exact reference contract required")
    if key == ("C06", "r01"):
        validate_c06_generation_request(data, contract)
        return
    if key[0] in DAILY_REVIEW_POLICIES:
        if key == ("D01", "r01"):
            try:
                validate_daily_generation_request(data, contract)
            except ValidationError as error:
                legacy_messages = {
                    "D01 scene_contract mismatch": "D01 scene contract mismatch",
                    "D01 production_requirements mismatch": (
                        "D01 production contract mismatch"
                    ),
                    "D01 candidate_policy mismatch": (
                        "D01 candidate policy mismatch"
                    ),
                    "D01 shared prompt required": (
                        "D01 exact shared prompt contract mismatch"
                    ),
                }
                raise ValidationError(
                    legacy_messages.get(str(error), str(error))
                ) from error
        else:
            validate_daily_generation_request(data, contract)
        return
    candidates = data.get("candidates")
    expected_variants = list(contract.get("candidate_variants", ("a", "b", "c")))
    if not isinstance(candidates, list) or [
        item.get("variant") for item in candidates
    ] != expected_variants:
        raise ValidationError(
            "generation request: expected candidates "
            + ", ".join(expected_variants)
        )
    for candidate in candidates:
        variant = candidate["variant"]
        if not candidate.get("title"):
            raise ValidationError("generation request: candidate title required")
        candidate_fields = contract.get("candidate_fields")
        if candidate_fields is not None and set(candidate) != set(candidate_fields):
            raise ValidationError("generation request: candidate fields mismatch")
        output_specs = contract["output_specs"]
        if output_specs is None:
            expected = (
                f"{contract['candidate_prefix']}"
                f"{contract['candidate_stem']}-{variant}.png"
            )
            if candidate.get("target_path") != expected:
                raise ValidationError(
                    "generation request: invalid candidate target path"
                )
            detail = contract["candidate_detail"]
            if detail is not None and not candidate.get(detail):
                raise ValidationError(f"generation request: {detail} required")
            continue
        outputs = candidate.get("outputs")
        if not isinstance(outputs, list) or [
            output.get("view") for output in outputs
        ] != [view for view, _ in output_specs]:
            raise ValidationError(
                "generation request: ordered paired outputs required"
            )
        for output, (_, stem) in zip(outputs, output_specs):
            expected = f"{contract['candidate_prefix']}{stem}-{variant}.png"
            if output.get("target_path") != expected:
                raise ValidationError(
                    "generation request: invalid paired output path"
                )
    candidate_titles = contract.get("candidate_titles")
    if candidate_titles is not None and tuple(
        candidate["title"] for candidate in candidates
    ) != candidate_titles:
        raise ValidationError("generation request: candidate titles mismatch")
    if data.get("comparison_anchors") != list(contract["comparison_anchors"]):
        raise ValidationError("generation request: comparison anchors mismatch")
    if contract["output_specs"] is not None:
        view_prompts = data.get("view_prompts")
        if not isinstance(view_prompts, dict) or set(view_prompts) != set(
            contract["view_names"]
        ) or not all(
            isinstance(view_prompts[view], str) and view_prompts[view].strip()
            for view in contract["view_names"]
        ):
            raise ValidationError("generation request: view prompts required")
        if data.get("pair_generation_policy") != contract["pair_generation_policy"]:
            raise ValidationError("generation request: pair generation policy mismatch")
    expected_framing = contract["framing_contract"]
    actual_framing = data.get("framing_contract")
    if expected_framing is None:
        if "framing_contract" in data:
            raise ValidationError("generation request: unexpected framing contract")
    elif ordered_value(actual_framing) != ordered_value(expected_framing):
        raise ValidationError("generation request: exact framing contract required")
    expected_guidance = contract["framing_guidance"]
    actual_guidance = data.get("framing_guidance")
    if expected_guidance is None:
        if "framing_guidance" in data:
            raise ValidationError("generation request: unexpected framing guidance")
    elif ordered_value(actual_guidance) != ordered_value(expected_guidance):
        raise ValidationError("generation request: exact framing guidance required")
    shared_prompt = data.get("shared_prompt")
    if not isinstance(shared_prompt, str) or not shared_prompt.strip():
        raise ValidationError("generation request: shared prompt required")
    for phrase in contract.get("required_prompt_phrases", ()):
        if phrase not in shared_prompt:
            raise ValidationError(
                "generation request: required prompt phrase missing"
            )
    if data.get("acceptance_gates") != list(contract["acceptance_gates"]):
        raise ValidationError("generation request: acceptance gates mismatch")
    expected_hard_rejects = contract.get("hard_rejects")
    if expected_hard_rejects is None:
        if not data.get("hard_rejects"):
            raise ValidationError("generation request: hard rejects required")
    elif data.get("hard_rejects") != list(expected_hard_rejects):
        raise ValidationError("generation request: exact hard rejects required")


def validate_generation_dependencies(assets: dict, requests: list[dict]) -> None:
    assets_by_id = {item["asset_id"]: item for item in assets["assets"]}
    c01 = assets_by_id["C01"]
    c02 = assets_by_id["C02"]
    c03 = assets_by_id["C03"]
    c04 = assets_by_id["C04"]
    c05 = assets_by_id["C05"]
    c06 = assets_by_id["C06"]
    c07 = assets_by_id["C07"]
    d01 = assets_by_id["D01"]
    d02 = assets_by_id["D02"]
    d03 = assets_by_id["D03"]
    d04 = assets_by_id["D04"]
    d05 = assets_by_id["D05"]
    d06 = assets_by_id["D06"]
    d07 = assets_by_id["D07"]
    d08 = assets_by_id["D08"]
    d09 = assets_by_id["D09"]
    d10 = assets_by_id["D10"]
    d11 = assets_by_id["D11"]
    d12 = assets_by_id["D12"]
    d13 = assets_by_id["D13"]
    d14 = assets_by_id["D14"]

    c02_requests = [item for item in requests if item["asset_id"] == "C02"]
    for request in c02_requests:
        paths = c01.get("accepted_paths")
        expected = (
            f"akari-v1.2/{paths[0]}"
            if isinstance(paths, list) and len(paths) == 1
            else None
        )
        if (
            c01.get("status") not in {"accepted", "accepted-with-notes"}
            or c01.get("revision") != "r01"
            or request["references"][0]["path"] != expected
        ):
            raise ValidationError(
                "C02 requires accepted C01 r01 at its declared anchor"
            )

    c03_requests = [item for item in requests if item["asset_id"] == "C03"]
    expected_anchors = []
    for asset in (c01, c02):
        paths = asset.get("accepted_paths")
        expected_anchors.append(
            f"akari-v1.2/{paths[0]}"
            if isinstance(paths, list) and len(paths) == 1
            else None
        )
    for request in c03_requests:
        if (
            any(
                asset.get("status") not in {"accepted", "accepted-with-notes"}
                or asset.get("revision") != "r01"
                for asset in (c01, c02)
            )
            or [reference["path"] for reference in request["references"][:2]]
            != expected_anchors
        ):
            raise ValidationError(
                "C03 requires accepted C01 and C02 r01 at its declared anchors"
            )

    c04_requests = [item for item in requests if item["asset_id"] == "C04"]
    expected_c01 = (
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c01_front-natural-stance_r01.png"
    )
    expected_c03 = (
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c03_hairpin-side-45_r02.png"
    )
    for request in c04_requests:
        if (
            (c01["status"], c01["revision"]) != ("accepted", "r01")
            or (c02["status"], c02["revision"]) != ("accepted", "r01")
            or (c03["status"], c03["revision"]) != ("accepted", "r02")
            or request["references"][0]["path"] != expected_c01
            or request["references"][1]["path"] != expected_c03
        ):
            raise ValidationError(
                "C04 requires accepted C01 r01, C02 r01, and C03 r02 "
                "at its declared anchors"
            )

    c05_requests = [item for item in requests if item["asset_id"] == "C05"]
    c01_paths = c01.get("accepted_paths")
    expected_c05_anchor = (
        f"akari-v1.2/{c01_paths[0]}"
        if isinstance(c01_paths, list) and len(c01_paths) == 1
        else None
    )
    for request in c05_requests:
        if (
            c05.get("depends_on") != ["C01"]
            or (c01.get("status"), c01.get("revision"))
            != ("accepted", "r01")
            or request["references"][0]["path"] != expected_c05_anchor
        ):
            raise ValidationError(
                "C05 requires accepted C01 r01 at its declared anchor"
            )
        expected_targets = [
            "source/candidates/c05/r01/"
            f"akari-v1.2_c05_{c05['descriptor']}_r01-{variant}.png"
            for variant in ("a", "b", "c")
        ]
        if [
            candidate["target_path"] for candidate in request["candidates"]
        ] != expected_targets:
            raise ValidationError(
                "C05 candidate paths must use assets descriptor"
            )

    c06_requests = [item for item in requests if item["asset_id"] == "C06"]
    c05_paths = c05.get("accepted_paths")
    expected_c06_source = (
        f"akari-v1.2/{c05_paths[0]}"
        if isinstance(c05_paths, list) and len(c05_paths) == 1
        else None
    )
    for request in c06_requests:
        if (
            c06.get("depends_on") != ["C05"]
            or (c05.get("status"), c05.get("revision"))
            != ("accepted", "r01")
            or request["references"][0]["path"] != expected_c06_source
        ):
            raise ValidationError(
                "C06 requires accepted C05 r01 at its declared edit source"
            )

    c07_requests = [item for item in requests if item["asset_id"] == "C07"]
    expected_c07_anchors = [
        "akari-v1.2/accepted/core/standing/"
        "akari-v1.2_c01_front-natural-stance_r01.png",
        "akari-v1.2/accepted/core/sitting/"
        "akari-v1.2_c04_floor-sitting_r01.png",
    ]
    for request in c07_requests:
        if (
            (c01["status"], c01["revision"]) != ("accepted", "r01")
            or (c04["status"], c04["revision"]) != ("accepted", "r01")
            or [reference["path"] for reference in request["references"][:2]]
            != expected_c07_anchors
        ):
            raise ValidationError(
                "C07 requires accepted C01 r01 and C04 r01 "
                "at its declared anchors"
            )

    d01_requests = [item for item in requests if item["asset_id"] == "D01"]
    expected_d01_paths = [
        "akari-v1.2/accepted/core/sitting/"
        "akari-v1.2_c04_floor-sitting_r01.png",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c05_morning-bedhair_r01.png",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c06-2_sleepy-secure_r01.png",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-seated_r01.png",
    ]
    for request in d01_requests:
        if (
            [
                (asset["status"], asset["revision"])
                for asset in (c04, c05, c06, c07)
            ]
            != [("accepted", "r01")] * 4
            or [item["path"] for item in request["references"]]
            != expected_d01_paths
        ):
            raise ValidationError(
                "D01 requires strict accepted C04 r01, C05 r01, C06 r01 "
                "C06-2, and C07 r01 seated"
            )

    d02_requests = [item for item in requests if item["asset_id"] == "D02"]
    expected_d02_paths = [
        "akari-v1.2/accepted/daily-validation/"
        "akari-v1.2_d01_morning-bedside_r01.png",
        "akari-v1.2/accepted/core/sitting/"
        "akari-v1.2_c04_floor-sitting_r01.png",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c05_morning-bedhair_r01.png",
        "akari-v1.2/accepted/core/face-hair/"
        "akari-v1.2_c06-1_sleepy-neutral_r01.png",
        "akari-v1.2/accepted/core/indoor-feet/"
        "akari-v1.2_c07_indoor-socks-seated_r01.png",
    ]
    for request in d02_requests:
        if (
            [
                (asset["status"], asset["revision"])
                for asset in (d01, c04, c05, c06, c07)
            ]
            != [("accepted", "r01")] * 5
            or [item["path"] for item in request["references"]]
            != expected_d02_paths
        ):
            raise ValidationError(
                "D02 requires strict accepted D01 r01, C04 r01, C05 r01, "
                "C06 r01 C06-1, and C07 r01 seated"
            )

    d03_requests = [item for item in requests if item["asset_id"] == "D03"]
    expected_d03_paths = [path for _, path in D03_R01_REFERENCES]
    for request in d03_requests:
        if (
            [
                (asset["status"], asset["revision"])
                for asset in (d02, c01, c03, c05, c06, c07)
            ]
            != [
                ("accepted", "r01"),
                ("accepted", "r01"),
                ("accepted", "r02"),
                ("accepted", "r01"),
                ("accepted", "r01"),
                ("accepted", "r01"),
            ]
            or [item["path"] for item in request["references"]]
            != expected_d03_paths
        ):
            raise ValidationError(
                "D03 requires strict accepted D02 r01, C01 r01, C03 r02, "
                "C05 r01, C06 r01 C06-1, and C07 r01 standing"
            )

    d04_requests = [item for item in requests if item["asset_id"] == "D04"]
    expected_d04_paths = [path for _, path in D04_R01_REFERENCES]
    for request in d04_requests:
        if (
            [
                (asset["status"], asset["revision"])
                for asset in (d03, c01, c03, c05, c06, c07)
            ]
            != [
                ("accepted", "r01"),
                ("accepted", "r01"),
                ("accepted", "r02"),
                ("accepted", "r01"),
                ("accepted", "r01"),
                ("accepted", "r01"),
            ]
            or [item["path"] for item in request["references"]]
            != expected_d04_paths
        ):
            raise ValidationError(
                "D04 requires strict accepted D03 r01, C01 r01, C03 r02, "
                "C05 r01, C06 r01 C06-1, and C07 r01 standing"
            )

    d05_requests = [item for item in requests if item["asset_id"] == "D05"]
    expected_d05_paths = [path for _, path in D05_R01_REFERENCES]
    for request in d05_requests:
        if (
            [
                (asset["status"], asset["revision"])
                for asset in (d04, c02, c03, c05, c06, c07)
            ]
            != [
                ("accepted", "r02"),
                ("accepted", "r01"),
                ("accepted", "r02"),
                ("accepted", "r01"),
                ("accepted", "r01"),
                ("accepted", "r01"),
            ]
            or [item["path"] for item in request["references"]]
            != expected_d05_paths
        ):
            raise ValidationError(
                "D05 requires strict accepted D04 r02, C02 r01, C03 r02, "
                "C05 r01, C06 r01 C06-1, and C07 r01 standing"
            )

    d06_requests = [item for item in requests if item["asset_id"] == "D06"]
    expected_d06_paths = [path for _, path in D06_R01_REFERENCES]
    for request in d06_requests:
        if (
            [
                (asset["status"], asset["revision"])
                for asset in (d05, c01, c03, c04, c06, c07)
            ]
            != [
                ("accepted", "r01"),
                ("accepted", "r01"),
                ("accepted", "r02"),
                ("accepted", "r01"),
                ("accepted", "r01"),
                ("accepted", "r01"),
            ]
            or [item["path"] for item in request["references"]]
            != expected_d06_paths
        ):
            raise ValidationError(
                "D06 requires strict accepted D05 r01, C01 r01, C03 r02, "
                "C04 r01, C06 r01 C06-2, and C07 r01 seated"
            )

    d07_requests = [item for item in requests if item["asset_id"] == "D07"]
    expected_d07_paths = [path for _, path in D07_R01_REFERENCES]
    for request in d07_requests:
        if (
            [
                (asset["status"], asset["revision"])
                for asset in (d06, c04, c03, c06, c07)
            ]
            != [
                ("accepted", "r01"),
                ("accepted", "r01"),
                ("accepted", "r02"),
                ("accepted", "r01"),
                ("accepted", "r01"),
            ]
            or [item["path"] for item in request["references"]]
            != expected_d07_paths
        ):
            raise ValidationError(
                "D07 requires strict accepted D06 r01, C04 r01, C03 r02, "
                "C06 r01 C06-2, and C07 r01 seated"
            )

    d08_requests = [item for item in requests if item["asset_id"] == "D08"]
    expected_d08_paths = [path for _, path in D08_R01_REFERENCES]
    for request in d08_requests:
        if (
            [
                (asset["status"], asset["revision"])
                for asset in (d07, c04, c03, c06, c07)
            ]
            != [
                ("accepted", "r01"),
                ("accepted", "r01"),
                ("accepted", "r02"),
                ("accepted", "r01"),
                ("accepted", "r01"),
            ]
            or [item["path"] for item in request["references"]]
            != expected_d08_paths
        ):
            raise ValidationError(
                "D08 requires strict accepted D07 r01, C04 r01, C03 r02, "
                "C06 r01 C06-2, and C07 r01 seated"
            )

    d09_requests = [item for item in requests if item["asset_id"] == "D09"]
    expected_d09_paths = [path for _, path in D09_R01_REFERENCES]
    for request in d09_requests:
        if (
            [
                (asset["status"], asset["revision"])
                for asset in (d08, c04, c03, c06, c07)
            ]
            != [
                ("accepted", "r03"),
                ("accepted", "r01"),
                ("accepted", "r02"),
                ("accepted", "r01"),
                ("accepted", "r01"),
            ]
            or [item["path"] for item in request["references"]]
            != expected_d09_paths
        ):
            raise ValidationError(
                "D09 requires strict accepted D08 r03, C04 r01, C03 r02, "
                "C06 r01 C06-1, and C07 r01 seated"
            )

    d10_requests = [item for item in requests if item["asset_id"] == "D10"]
    expected_d10_paths = [path for _, path in D10_R01_REFERENCES]
    for request in d10_requests:
        if (
            [
                (asset["status"], asset["revision"])
                for asset in (d09, d02, c03, c06, c07)
            ]
            != [
                ("accepted", "r01"),
                ("accepted", "r01"),
                ("accepted", "r02"),
                ("accepted", "r01"),
                ("accepted", "r01"),
            ]
            or [item["path"] for item in request["references"]]
            != expected_d10_paths
        ):
            raise ValidationError(
                "D10 requires strict accepted D09 r01, D02 r01, C03 r02, "
                "C06 r01 C06-1, and C07 r01 seated"
            )

    d11_requests = [item for item in requests if item["asset_id"] == "D11"]
    for request in d11_requests:
        if request["revision"] == "r01":
            dependencies = (d10, d02, c03, c04, c07)
            expected_states = [
                ("accepted", "r01"),
                ("accepted", "r01"),
                ("accepted", "r02"),
                ("accepted", "r01"),
                ("accepted", "r01"),
            ]
            expected_paths = [path for _, path in D11_R01_REFERENCES]
        else:
            dependencies = (d10, d07, d02, c03, c07)
            expected_states = [
                ("accepted", "r01"),
                ("accepted", "r01"),
                ("accepted", "r01"),
                ("accepted", "r02"),
                ("accepted", "r01"),
            ]
            expected_paths = [path for _, path in D11_R02_REFERENCES]
        if (
            [(asset["status"], asset["revision"]) for asset in dependencies]
            != expected_states
            or [item["path"] for item in request["references"]] != expected_paths
        ):
            raise ValidationError(
                "D11 requires its exact strict accepted revision references"
            )

    d12_requests = [item for item in requests if item["asset_id"] == "D12"]
    expected_d12_paths = [path for _, path in D12_R01_REFERENCES]
    for request in d12_requests:
        if (
            [
                (asset["status"], asset["revision"])
                for asset in (d11, d04, c03, c01, c07)
            ]
            != [
                ("accepted", "r02"),
                ("accepted", "r02"),
                ("accepted", "r02"),
                ("accepted", "r01"),
                ("accepted", "r01"),
            ]
            or [item["path"] for item in request["references"]]
            != expected_d12_paths
        ):
            raise ValidationError(
                "D12 requires strict accepted D11 r02, D04 r02, C03 r02, "
                "C01 r01, and C07 r01 standing"
            )

    d13_requests = [item for item in requests if item["asset_id"] == "D13"]
    expected_d13_paths = [path for _, path in D13_R01_REFERENCES]
    for request in d13_requests:
        if (
            [
                (asset["status"], asset["revision"])
                for asset in (d12, d04, c03, c01, c07)
            ]
            != [
                ("accepted", "r01"),
                ("accepted", "r02"),
                ("accepted", "r02"),
                ("accepted", "r01"),
                ("accepted", "r01"),
            ]
            or [item["path"] for item in request["references"]]
            != expected_d13_paths
        ):
            raise ValidationError(
                "D13 requires strict accepted D12 r01, D04 r02, C03 r02, "
                "C01 r01, and C07 r01 standing"
            )

    d14_requests = [item for item in requests if item["asset_id"] == "D14"]
    expected_d14_paths = [path for _, path in D14_R01_REFERENCES]
    for request in d14_requests:
        if (
            [
                (asset["status"], asset["revision"])
                for asset in (d13, d11, d06, c03, c07)
            ]
            != [
                ("accepted", "r02"),
                ("accepted", "r02"),
                ("accepted", "r01"),
                ("accepted", "r02"),
                ("accepted", "r01"),
            ]
            or [item["path"] for item in request["references"]]
            != expected_d14_paths
        ):
            raise ValidationError(
                "D14 requires strict accepted D13 r02, D11 r02, D06 r01, "
                "C03 r02, and C07 r01 seated"
            )

    d15_requests = [item for item in requests if item["asset_id"] == "D15"]
    expected_d15_paths = [path for _, path in D15_R01_REFERENCES]
    for request in d15_requests:
        if (
            [
                (asset["status"], asset["revision"])
                for asset in (d14, d13, d11, c03, c07)
            ]
            != [
                ("accepted", "r02"),
                ("accepted", "r02"),
                ("accepted", "r02"),
                ("accepted", "r02"),
                ("accepted", "r01"),
            ]
            or [item["path"] for item in request["references"]]
            != expected_d15_paths
        ):
            raise ValidationError(
                "D15 requires strict accepted D14 r02, D13 r02, D11 r02, "
                "C03 r02, and C07 r01 seated"
            )


def validate_assets(data: dict, package_root: Path | None = None) -> None:
    if data.get("schema_version") != 1:
        raise ValidationError("assets: schema_version must be 1")
    assets = data.get("assets")
    if not isinstance(assets, list):
        raise ValidationError("assets: assets must be a list")
    ids = [item.get("asset_id") for item in assets]
    if ids != list(ASSET_IDS):
        raise ValidationError(f"assets: expected IDs {ASSET_IDS}, got {ids}")
    c06 = next(item for item in assets if item["asset_id"] == "C06")
    c06_static_contract = {
        field: c06.get(field) for field in C06_STATIC_ASSET_CONTRACT
    }
    if c06_static_contract != C06_STATIC_ASSET_CONTRACT:
        raise ValidationError("C06: static asset contract mismatch")
    d01 = next(item for item in assets if item["asset_id"] == "D01")
    d01_static_contract = {
        field: d01.get(field) for field in D01_STATIC_ASSET_CONTRACT
    }
    if d01_static_contract != D01_STATIC_ASSET_CONTRACT:
        raise ValidationError("D01: static asset contract mismatch")
    d02 = next(item for item in assets if item["asset_id"] == "D02")
    d02_static_contract = {
        field: d02.get(field) for field in D02_STATIC_ASSET_CONTRACT
    }
    if d02_static_contract != D02_STATIC_ASSET_CONTRACT:
        raise ValidationError("D02: static asset contract mismatch")
    d03 = next(item for item in assets if item["asset_id"] == "D03")
    d03_static_contract = {
        field: d03.get(field) for field in D03_STATIC_ASSET_CONTRACT
    }
    if d03_static_contract != D03_STATIC_ASSET_CONTRACT:
        raise ValidationError("D03: static asset contract mismatch")
    d04 = next(item for item in assets if item["asset_id"] == "D04")
    d04_static_contract = {
        field: d04.get(field) for field in D04_STATIC_ASSET_CONTRACT
    }
    if d04_static_contract != D04_STATIC_ASSET_CONTRACT:
        raise ValidationError("D04: static asset contract mismatch")
    d05 = next(item for item in assets if item["asset_id"] == "D05")
    d05_static_contract = {
        field: d05.get(field) for field in D05_STATIC_ASSET_CONTRACT
    }
    if d05_static_contract != D05_STATIC_ASSET_CONTRACT:
        raise ValidationError("D05: static asset contract mismatch")
    d06 = next(item for item in assets if item["asset_id"] == "D06")
    d06_static_contract = {
        field: d06.get(field) for field in D06_STATIC_ASSET_CONTRACT
    }
    if d06_static_contract != D06_STATIC_ASSET_CONTRACT:
        raise ValidationError("D06: static asset contract mismatch")
    d07 = next(item for item in assets if item["asset_id"] == "D07")
    d07_static_contract = {
        field: d07.get(field) for field in D07_STATIC_ASSET_CONTRACT
    }
    if d07_static_contract != D07_STATIC_ASSET_CONTRACT:
        raise ValidationError("D07: static asset contract mismatch")
    d08 = next(item for item in assets if item["asset_id"] == "D08")
    d08_static_contract = {
        field: d08.get(field) for field in D08_STATIC_ASSET_CONTRACT
    }
    if d08_static_contract != D08_STATIC_ASSET_CONTRACT:
        raise ValidationError("D08: static asset contract mismatch")
    d09 = next(item for item in assets if item["asset_id"] == "D09")
    d09_static_contract = {
        field: d09.get(field) for field in D09_STATIC_ASSET_CONTRACT
    }
    if d09_static_contract != D09_STATIC_ASSET_CONTRACT:
        raise ValidationError("D09: static asset contract mismatch")
    d10 = next(item for item in assets if item["asset_id"] == "D10")
    d10_static_contract = {
        field: d10.get(field) for field in D10_STATIC_ASSET_CONTRACT
    }
    if d10_static_contract != D10_STATIC_ASSET_CONTRACT:
        raise ValidationError("D10: static asset contract mismatch")
    d11 = next(item for item in assets if item["asset_id"] == "D11")
    d11_static_contract = {
        field: d11.get(field) for field in D11_STATIC_ASSET_CONTRACT
    }
    if d11_static_contract != D11_STATIC_ASSET_CONTRACT:
        raise ValidationError("D11: static asset contract mismatch")
    d12 = next(item for item in assets if item["asset_id"] == "D12")
    d12_static_contract = {
        field: d12.get(field) for field in D12_STATIC_ASSET_CONTRACT
    }
    if d12_static_contract != D12_STATIC_ASSET_CONTRACT:
        raise ValidationError("D12: static asset contract mismatch")
    d13 = next(item for item in assets if item["asset_id"] == "D13")
    d13_static_contract = {
        field: d13.get(field) for field in D13_STATIC_ASSET_CONTRACT
    }
    if d13_static_contract != D13_STATIC_ASSET_CONTRACT:
        raise ValidationError("D13: static asset contract mismatch")
    d14 = next(item for item in assets if item["asset_id"] == "D14")
    d14_static_contract = {
        field: d14.get(field) for field in D14_STATIC_ASSET_CONTRACT
    }
    if d14_static_contract != D14_STATIC_ASSET_CONTRACT:
        raise ValidationError("D14: static asset contract mismatch")
    d15 = next(item for item in assets if item["asset_id"] == "D15")
    d15_static_contract = {
        field: d15.get(field) for field in D15_STATIC_ASSET_CONTRACT
    }
    if d15_static_contract != D15_STATIC_ASSET_CONTRACT:
        raise ValidationError("D15: static asset contract mismatch")
    known = set(ids)
    for item in assets:
        asset_id = item["asset_id"]
        variants = item.get("variants")
        if (
            not isinstance(variants, list)
            or not variants
            or len(variants) != len(set(variants))
        ):
            raise ValidationError(f"{asset_id}: variants must be unique and non-empty")
        expected_paths = item.get("expected_paths")
        if not isinstance(expected_paths, list) or len(expected_paths) != len(variants):
            raise ValidationError(f"{asset_id}: expected_paths must match variants")
        for expected_path in expected_paths:
            parts = PurePosixPath(expected_path).parts
            if not parts or parts[0] != "accepted" or ".." in parts:
                raise ValidationError(f"{asset_id}: invalid expected_paths entry")
        status = item.get("status")
        if status not in STATUSES:
            raise ValidationError(f"{asset_id}: invalid status")
        if asset_id in {"C05", "C06"} and status == "accepted-with-notes":
            raise ValidationError(
                f"{asset_id}: accepted-with-notes is not allowed"
            )
        if item.get("gate") not in GATES:
            raise ValidationError(f"{asset_id}: invalid gate")
        revision = item.get("revision")
        if not isinstance(revision, str) or not REVISION_RE.fullmatch(revision):
            raise ValidationError(f"{asset_id}: invalid revision")
        if revision == "r00" and status in {"accepted", "accepted-with-notes"}:
            raise ValidationError(f"{asset_id}: r00 cannot be accepted")
        dependencies = item.get("depends_on")
        if not isinstance(dependencies, list):
            raise ValidationError(f"{asset_id}: depends_on must be a list")
        unknown = set(dependencies) - known
        if unknown:
            raise ValidationError(f"{asset_id}: unknown dependency {sorted(unknown)}")
        accepted_paths = item.get("accepted_paths")
        if not isinstance(accepted_paths, list) or not all(
            isinstance(path, str) for path in accepted_paths
        ):
            raise ValidationError(f"{asset_id}: accepted_paths must be a list")
        revision_paths = [
            expected_path.replace("rNN", revision)
            for expected_path in expected_paths
        ]
        if status in {"accepted", "accepted-with-notes"}:
            if accepted_paths != revision_paths:
                raise ValidationError(
                    f"{asset_id}: accepted_paths must match variants and revision"
                )
            if package_root is not None:
                for accepted_path in accepted_paths:
                    if not (package_root / accepted_path).is_file():
                        raise ValidationError(f"{asset_id}: accepted file does not exist")
                if asset_id in DAILY_REVIEW_POLICIES:
                    requirements = {
                        "D01": D01_R01_PRODUCTION_REQUIREMENTS,
                        "D02": D02_R01_PRODUCTION_REQUIREMENTS,
                        "D03": D03_R01_PRODUCTION_REQUIREMENTS,
                        "D04": D04_R01_PRODUCTION_REQUIREMENTS,
                        "D05": D05_R01_PRODUCTION_REQUIREMENTS,
                        "D06": D06_R01_PRODUCTION_REQUIREMENTS,
                        "D07": D07_R01_PRODUCTION_REQUIREMENTS,
                        "D08": D08_R01_PRODUCTION_REQUIREMENTS,
                        "D09": D09_R01_PRODUCTION_REQUIREMENTS,
                        "D10": D10_R01_PRODUCTION_REQUIREMENTS,
                        "D11": D11_R01_PRODUCTION_REQUIREMENTS,
                        "D12": D12_R01_PRODUCTION_REQUIREMENTS,
                        "D13": D13_R01_PRODUCTION_REQUIREMENTS,
                        "D14": D14_R01_PRODUCTION_REQUIREMENTS,
                        "D15": D15_R01_PRODUCTION_REQUIREMENTS,
                    }[asset_id]
                    validate_daily_png_dimensions(
                        package_root / accepted_paths[0],
                        asset_id,
                        revision,
                        requirements,
                    )
        elif accepted_paths:
            raise ValidationError(
                f"{asset_id}: candidate accepted_paths must be empty"
            )
    assets_by_id = {item["asset_id"]: item for item in assets}
    if (
        assets_by_id["C06"]["status"] in {"accepted", "accepted-with-notes"}
        and assets_by_id["C05"]["status"] != "accepted"
    ):
        raise ValidationError("C06 acceptance requires accepted C05")
    if (
        assets_by_id["D01"]["status"] in {"accepted", "accepted-with-notes"}
        and assets_by_id["C06"]["status"] != "accepted"
    ):
        raise ValidationError("D01 acceptance requires accepted C06")
    if assets_by_id["D01"]["status"] in {"accepted", "accepted-with-notes"}:
        core_states = [
            (assets_by_id[asset_id]["status"], assets_by_id[asset_id]["revision"])
            for asset_id in ("C04", "C05", "C06", "C07")
        ]
        if core_states != [("accepted", "r01")] * 4:
            raise ValidationError(
                "D01 acceptance requires strict accepted "
                "C04 r01, C05 r01, C06 r01, and C07 r01"
            )


def validate_review_log(data: dict) -> None:
    if data.get("schema_version") != 1:
        raise ValidationError("review-log: schema_version must be 1")
    if tuple(data.get("allowed_statuses", ())) != STATUSES:
        raise ValidationError("review-log: allowed_statuses mismatch")
    if tuple(data.get("allowed_severities", ())) != SEVERITIES:
        raise ValidationError("review-log: allowed_severities mismatch")
    reviews = data.get("reviews")
    if not isinstance(reviews, list):
        raise ValidationError("review-log: reviews must be a list")
    for review in reviews:
        asset_id = review.get("asset_id")
        if asset_id not in ASSET_IDS:
            raise ValidationError("review-log: unknown asset_id")
        revision = review.get("revision")
        if not isinstance(revision, str) or not REVISION_RE.fullmatch(revision):
            raise ValidationError(f"{asset_id}: invalid review revision")
        candidate_id = review.get("candidate_id")
        if not isinstance(candidate_id, str) or not candidate_id:
            raise ValidationError(f"{asset_id}: candidate_id is required")
        source_paths = review.get("source_paths")
        source_sha256s = review.get("source_sha256s")
        if not isinstance(source_paths, list) or not source_paths:
            raise ValidationError(f"{asset_id}: source_paths are required")
        if (
            not isinstance(source_sha256s, list)
            or len(source_sha256s) != len(source_paths)
        ):
            raise ValidationError(f"{asset_id}: source SHA-256 count mismatch")
        for source_path, source_sha256 in zip(source_paths, source_sha256s):
            if not isinstance(source_path, str):
                raise ValidationError(f"{asset_id}: source path must be a string")
            source_parts = PurePosixPath(source_path).parts
            if source_parts[:2] != ("source", "candidates") or ".." in source_parts:
                raise ValidationError(
                    f"{asset_id}: canonical candidate source required"
                )
            if (
                not isinstance(source_sha256, str)
                or not SHA256_RE.fullmatch(source_sha256)
            ):
                raise ValidationError(f"{asset_id}: invalid source SHA-256")
        status = review.get("status")
        if status not in STATUSES:
            raise ValidationError(f"{asset_id}: invalid review status")
        if not isinstance(review.get("decision"), str) or not review["decision"].strip():
            raise ValidationError(f"{asset_id}: decision is required")
        findings = review.get("findings")
        if not isinstance(findings, list):
            raise ValidationError(f"{asset_id}: findings must be a list")
        for finding in findings:
            severity = finding.get("severity")
            category = finding.get("category")
            if severity not in SEVERITIES:
                raise ValidationError(f"{asset_id}: invalid finding severity")
            if category not in REVIEW_CATEGORIES:
                raise ValidationError(f"{asset_id}: invalid finding category")
            if not isinstance(finding.get("note"), str) or not finding["note"].strip():
                raise ValidationError(f"{asset_id}: finding note is required")
            if not isinstance(finding.get("resolved"), bool):
                raise ValidationError(f"{asset_id}: finding resolution must be boolean")
            if asset_id in DAILY_REVIEW_POLICIES:
                validate_daily_finding(asset_id, finding)
            if (
                asset_id not in DAILY_REVIEW_POLICIES
                and status in {"accepted", "accepted-with-notes"}
                and severity in {"blocker", "major"}
                and not finding["resolved"]
            ):
                raise ValidationError(f"{asset_id}: unresolved {severity}")
        if asset_id in DAILY_REVIEW_POLICIES:
            validate_daily_review_status(asset_id, status, findings)


def candidate_source_paths(candidate: dict) -> list[str]:
    if "outputs" in candidate:
        return [output["target_path"] for output in candidate["outputs"]]
    target_path = candidate.get("target_path")
    return [target_path] if isinstance(target_path, str) else []


def declared_review_pairs(request: dict) -> list[tuple[str, list[str]]]:
    if (request["asset_id"], request["revision"]) == ("C06", "r01"):
        return [
            (item["candidate_id"], item["source_paths"])
            for item in request["review_sets"]
        ]
    return [
        (
            f"{request['asset_id'].lower()}-"
            f"{request['revision']}-{candidate['variant']}",
            candidate_source_paths(candidate),
        )
        for candidate in request["candidates"]
    ]


def validate_lifecycle_linkage(
    assets: dict,
    generation_requests: list[dict],
    review_log: dict,
    package_root: Path | None = None,
) -> None:
    accepted_statuses = {"accepted", "accepted-with-notes"}
    requests_by_key = {
        (request["asset_id"], request["revision"]): request
        for request in generation_requests
    }
    accepted_assets = {
        (asset["asset_id"], asset["revision"]): asset
        for asset in assets["assets"]
        if asset["status"] in accepted_statuses
    }
    accepted_reviews = [
        review
        for review in review_log["reviews"]
        if review["status"] in accepted_statuses
    ]

    reviews_by_key: dict[tuple[str, str], list[dict]] = {}
    for review in review_log["reviews"]:
        key = (review["asset_id"], review["revision"])
        reviews_by_key.setdefault(key, []).append(review)

    for key in reviews_by_key:
        if key not in requests_by_key:
            raise ValidationError(
                f"{key[0]} {key[1]}: reviews require a matching "
                "generation request"
            )

    daily_keys = {
        (request["asset_id"], request["revision"])
        for request in generation_requests
        if request["asset_id"] in DAILY_REVIEW_POLICIES
    }
    latest_daily_key_by_asset: dict[str, tuple[str, str]] = {}
    for daily_key in sorted(daily_keys):
        latest_daily_key_by_asset[daily_key[0]] = daily_key
    accepted_daily_asset_ids = {
        asset_id
        for asset_id, _ in accepted_assets
        if asset_id in DAILY_REVIEW_POLICIES
    }
    if package_root is not None:
        for daily_key in sorted(daily_keys & requests_by_key.keys()):
            request = requests_by_key[daily_key]
            generated = [
                (package_root / candidate["target_path"]).is_file()
                for candidate in request["candidates"]
            ]
            generated_count = sum(generated)
            matching = reviews_by_key.get(daily_key, [])
            actual = [
                (review["candidate_id"], review["source_paths"])
                for review in matching
            ]
            declared = declared_review_pairs(request)
            pending = (
                daily_key not in accepted_assets
                and daily_key[0] not in accepted_daily_asset_ids
                and latest_daily_key_by_asset[daily_key[0]] == daily_key
            )
            if (
                generated
                != [True] * generated_count
                + [False] * (len(generated) - generated_count)
                or actual != declared[:len(actual)]
                or (
                    pending
                    and len(actual) > generated_count
                )
            ):
                raise ValidationError(
                    f"{daily_key[0]} {daily_key[1]}: generated candidates "
                    "require ordered reviews"
                )

    for daily_key in sorted(daily_keys & requests_by_key.keys()):
        request = requests_by_key[daily_key]
        declared = declared_review_pairs(request)
        if len(declared) != 3:
            continue
        matching = reviews_by_key.get(daily_key, [])
        historical_revision = (
            daily_key not in accepted_assets
            and daily_key[0] in accepted_daily_asset_ids
        )
        if historical_revision and not matching:
            continue
        prefix = matching[:2]
        policy = daily_review_policy(daily_key[0])
        scene_controller = policy.scene_controller
        allowed_severities = policy.optional_c_finding_severities
        allowed_controllers = (
            policy.controllers
            if policy.optional_c_allows_distinct_candidate_local
            else frozenset({scene_controller})
        )
        unresolved_controllers = [
            {
                finding.get("controlling_source_asset")
                for finding in review["findings"]
                if not finding["resolved"]
            }
            for review in prefix
        ]
        shared_non_scene = (
            set.intersection(*unresolved_controllers) - {scene_controller}
            if len(unresolved_controllers) == 2
            else set()
        )
        if (
            len(prefix) != 2
            or any(review["status"] != "rejected" for review in prefix)
            or any(
                not any(
                    not finding["resolved"]
                    and finding.get("severity") in allowed_severities
                    and finding.get("controlling_source_asset")
                    in allowed_controllers
                    for finding in review["findings"]
                )
                for review in prefix
            )
            or any(
                finding.get("controlling_source_asset") not in allowed_controllers
                for review in prefix
                for finding in review["findings"]
                if not finding["resolved"]
            )
            or bool(shared_non_scene)
        ):
            raise ValidationError(
                f"{daily_key[0]} {daily_key[1]}: optional C requires "
                "rejected scene-only A/B"
            )

    for key, matching in reviews_by_key.items():
        request = requests_by_key[key]
        declared = declared_review_pairs(request)
        actual = [
            (review["candidate_id"], review["source_paths"])
            for review in matching
        ]
        daily_pending = (
            key in daily_keys
            and key not in accepted_assets
            and key[0] not in accepted_daily_asset_ids
        )
        matches_declaration = (
            actual == declared[:len(actual)] if daily_pending else actual == declared
        )
        if not matches_declaration:
            noun = "review sets" if key == ("C06", "r01") else "candidates"
            raise ValidationError(
                f"{key[0]} {key[1]}: reviews must match declared "
                f"{key[0]} {noun} in order before expected exactly one "
                "accepted review"
            )

    for asset_key in accepted_assets:
        asset_id, revision = asset_key
        request = requests_by_key.get(asset_key)
        if request is None:
            raise ValidationError(
                f"{asset_id} accepted review requires a generation request"
            )
        matching = reviews_by_key.get(asset_key, [])
        accepted_matching = [
            review for review in matching if review["status"] in accepted_statuses
        ]
        if len(accepted_matching) != 1:
            raise ValidationError(
                f"{asset_id} {revision}: expected exactly one accepted review"
            )
        accepted_review = accepted_matching[0]
        if accepted_review["status"] != accepted_assets[asset_key]["status"]:
            raise ValidationError(
                f"{asset_id} {revision}: accepted review status must match "
                "asset status"
            )
        if any(
            review is not accepted_review and review["status"] != "rejected"
            for review in matching
        ):
            raise ValidationError(
                f"{asset_id} {revision}: non-selected reviews must be rejected"
            )
        if package_root is not None:
            accepted_paths = accepted_assets[asset_key]["accepted_paths"]
            if len(accepted_paths) != len(accepted_review["source_sha256s"]):
                raise ValidationError(
                    f"{asset_id} {revision}: accepted hash count mismatch"
                )
            if asset_key in daily_keys:
                for source_path, expected_hash in zip(
                    accepted_review["source_paths"],
                    accepted_review["source_sha256s"],
                ):
                    selected_source = package_root / source_path
                    if (
                        selected_source.is_file()
                        and sha256_file(selected_source) != expected_hash
                    ):
                        raise ValidationError(
                            f"{asset_id} {revision}: selected source file "
                            "SHA-256 mismatch"
                        )
            for accepted_path, expected_hash in zip(
                accepted_paths, accepted_review["source_sha256s"]
            ):
                if sha256_file(package_root / accepted_path) != expected_hash:
                    raise ValidationError(
                        f"{asset_id} {revision}: accepted file SHA-256 mismatch"
                    )
    for review in accepted_reviews:
        key = (review["asset_id"], review["revision"])
        if key not in accepted_assets:
            raise ValidationError(
                f"{review['asset_id']} {review['revision']}: "
                "accepted review requires a matching accepted asset"
            )


def validate_gate4(assets: dict, review_log: dict) -> None:
    d01 = next(item for item in assets["assets"] if item["asset_id"] == "D01")
    record = review_log.get("gate_4")
    if record is None:
        if d01["status"] in {"accepted", "accepted-with-notes"}:
            raise ValidationError("Gate 4 record required for accepted D01")
        return
    if set(record) != {
        "asset_id",
        "revision",
        "outcome",
        "selected_candidate_id",
        "controlling_source_asset",
        "decision",
    } or (record["asset_id"], record["revision"]) != ("D01", "r01"):
        raise ValidationError("Gate 4 record contract mismatch")
    matching = [
        review
        for review in review_log["reviews"]
        if (review["asset_id"], review["revision"]) == ("D01", "r01")
        and review["status"] in {"accepted", "accepted-with-notes"}
    ]
    expected = {
        "accepted": "release",
        "accepted-with-notes": "conditional-release",
    }.get(d01["status"], "hold")
    if record["outcome"] != expected:
        raise ValidationError("Gate 4 outcome does not match D01 status")
    expected_id = matching[0]["candidate_id"] if len(matching) == 1 else None
    if record["selected_candidate_id"] != expected_id:
        raise ValidationError("Gate 4 selection does not match D01 review")
    if (
        record["controlling_source_asset"]
        not in {"C04", "C05", "C06", "C07", "D01-scene"}
        or not isinstance(record["decision"], str)
        or not record["decision"].strip()
    ):
        raise ValidationError("Gate 4 decision contract mismatch")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_inheritance(
    data: dict, repository_root: Path, package_root: Path
) -> None:
    if data.get("schema_version") != 1:
        raise ValidationError("inheritance: schema_version must be 1")
    references = data.get("references")
    if not isinstance(references, list) or len(references) != 16:
        raise ValidationError("inheritance: expected 16 references")
    roles: set[str] = set()
    copied_paths: set[str] = set()
    for record in references:
        role = record.get("role")
        if not isinstance(role, str) or role in roles:
            raise ValidationError(f"inheritance: duplicate role {role}")
        roles.add(role)
        if record.get("inheritance_class") not in {"inherited", "reference-only"}:
            raise ValidationError(f"{role}: invalid inheritance_class")
        source_relative = record.get("source_path")
        copied_relative = record.get("copied_path")
        if not isinstance(source_relative, str) or not isinstance(copied_relative, str):
            raise ValidationError(f"{role}: paths must be strings")
        copied_parts = PurePosixPath(copied_relative).parts
        if copied_parts[:2] != ("akari-v1.2", "references") or ".." in copied_parts:
            raise ValidationError(
                f"{role}: copied_path must be a canonical reference snapshot"
            )
        if copied_relative in copied_paths:
            raise ValidationError(f"{role}: duplicate copied_path")
        copied_paths.add(copied_relative)
        source = repository_root / source_relative
        copied = repository_root / copied_relative
        if not source.is_file() or not copied.is_file():
            raise ValidationError(f"{role}: source and copied files must exist")
        expected = record.get("sha256")
        if not isinstance(expected, str) or len(expected) != 64:
            raise ValidationError(f"{role}: invalid SHA-256")
        if sha256_file(source) != expected or sha256_file(copied) != expected:
            raise ValidationError(f"{role}: SHA-256 mismatch")
        if not record.get("reuse_rationale"):
            raise ValidationError(f"{role}: reuse_rationale is required")
    actual_copies = {
        path.relative_to(repository_root).as_posix()
        for path in (package_root / "references").rglob("*")
        if path.is_file()
    }
    if actual_copies != copied_paths:
        raise ValidationError("inheritance: unrecorded or missing copied reference")
    c06_expression_reference = next(
        (
            record
            for record in references
            if record.get("role")
            == C06_EXPRESSION_REFERENCE_CONTRACT["role"]
        ),
        None,
    )
    if c06_expression_reference != C06_EXPRESSION_REFERENCE_CONTRACT:
        raise ValidationError(
            "inheritance: C06 expression reference contract mismatch"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=PACKAGE_ROOT)
    args = parser.parse_args()
    manifest_root = args.package_root / "manifest"
    assets = load_yaml(manifest_root / "assets.yaml")
    inheritance = load_yaml(manifest_root / "inheritance.yaml")
    review_log = load_yaml(manifest_root / "review-log.yaml")
    generation_requests = load_generation_requests(
        manifest_root / "generation-requests"
    )
    validate_assets(assets, args.package_root)
    for request in generation_requests:
        validate_generation_request(request)
        if request["asset_id"] in DAILY_REVIEW_POLICIES:
            validate_daily_candidate_dimensions(request, args.package_root)
    validate_generation_dependencies(assets, generation_requests)
    validate_inheritance(inheritance, ROOT, args.package_root)
    validate_review_log(review_log)
    validate_lifecycle_linkage(
        assets, generation_requests, review_log, args.package_root
    )
    validate_gate4(assets, review_log)
    candidate_count, output_count = count_generation_work(generation_requests)
    print(
        f"validated {len(assets['assets'])} assets, "
        f"{len(inheritance['references'])} references, "
        f"{len(generation_requests)} generation requests with "
        f"{candidate_count} candidate groups and "
        f"{output_count} generated outputs, and "
        f"{len(review_log['reviews'])} reviews"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
