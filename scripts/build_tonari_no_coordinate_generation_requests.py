#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/tonari-no-coordinate"
SLOTS_PATH = MANIFEST_DIR / "coordinate-slots.json"
OUTPUT_PATH = MANIFEST_DIR / "generation-requests.json"
COLLECTION_ID = "akari-v1.1-tonari-no-coordinate"
TITLE = "となりのコーデ"
REFERENCE_PACK_VERSION = "tonari-no-akari-identity-v1"
PROMPT_TEMPLATE_VERSION = "tonari_coordinate_identity_lock_v1"
REFERENCE_PACK_INPUTS = [
    "source/references/tonari-no-akari/identity-face-hair.webp",
    "source/references/tonari-no-akari/identity-body-base.webp",
    "source/references/tonari-no-akari/identity-basic-outfit.webp",
    "source/references/tonari-no-akari/identity-side-view.webp",
]
DATE_PREFIX = "20260706"
SCENE_LABELS = {
    "room": "room",
    "window": "window",
    "sofa": "sofa",
    "desk": "desk",
    "walk_home": "walk home",
    "cafe": "cafe",
    "station": "station",
    "riverside": "riverside",
    "doorway": "doorway",
    "shopping_street": "shopping street",
    "kitchen": "kitchen",
    "veranda": "veranda",
}
SEASON_LABELS = {
    "spring": "spring",
    "summer": "summer",
    "autumn": "autumn",
    "winter": "winter",
    "rain": "rain",
    "night": "night",
    "all_season": "all season",
}
COMPOSITION_LABELS = {
    "close": "close portrait",
    "upper_body": "upper-body portrait",
    "half_body": "half-body portrait",
    "knee_up": "knee-up portrait",
    "full_body": "full-body portrait",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def hand_risk_for(slot: dict) -> str:
    if slot["composition"] == "full_body":
        return "high"
    if slot["composition"] in {"knee_up", "half_body"}:
        return "medium"
    return "low"


def outfit_drift_risk_for(slot: dict) -> str:
    if slot["outfit_family"] in {"one_piece_skirt", "hoodie_baseline"}:
        return "high"
    return "medium"


def age_impression_risk_for(slot: dict) -> str:
    if slot["outfit_family"] in {"hoodie_baseline", "roomwear_relaxed"}:
        return "high"
    return "medium"


def build_prompt(slot: dict) -> str:
    season = SEASON_LABELS[slot["season"]]
    scene = SCENE_LABELS[slot["scene"]]
    composition = COMPOSITION_LABELS[slot["composition"]]
    return (
        f"Create one A4 portrait draft for Tonari no Coordinate: "
        f"{slot['japanese_title']}. Season and scene: {season}, {scene}. "
        f"Composition: {composition}, close everyday Akari mood, outfit clearly visible. "
        f"Coordinate: {slot['outfit_notes']} "
        f"Identity accent: {slot['mint_accent']} "
        "Akari identity lock: adult 25-year-old Japanese woman; naturally cute adult, "
        "not glamorous, not model-like, not pin-up, not childlike; "
        "short fluffy light-brown bob with airy uneven ends and soft side bangs; "
        "warm amber eyes, rounded cheeks, compact rounded chin, small subtle nose and mouth; "
        "pale-blue crossed hairpins/ribbon-like clips on character-left side when visible; "
        "petite/slender healthy adult proportions. "
        "Styling boundary: daily wear or lightly dressed-up day-off wear; "
        "no student-uniform styling, no character-costume styling, no job-uniform styling, "
        "no revealing swim styling, no underwear-like styling, no readable text prints. "
        "No image-internal readable text, no logos, no watermarks, no frame, no border, "
        "no panel layout."
    )


def build_acceptance(slot: dict) -> str:
    return (
        "Coordinate Gate: must preserve Akari identity, 25-year-old adult age impression, "
        "face/hair/hairpin consistency, natural body proportions, visible mint or pale-blue "
        "identity accent, daily or lightly special outfit readability, and clean clothing "
        "continuity. It must be not a fashion-model sheet, not a costume sheet, and not a "
        "return to hoodie-heavy sameness. Must contain no image-internal readable text, "
        "no logos, no watermarks, no frame, no border, no panel layout. "
        f"Known slot risk: {slot['risk_note']}"
    )


def build_request(slot: dict) -> dict:
    return {
        "id": f"request:tonari-coordinate-{slot['slug']}",
        "coordinate_order": slot["slot_order"],
        "slot": slot["slug"],
        "japanese_title": slot["japanese_title"],
        "season": slot["season"],
        "scene": slot["scene"],
        "outfit_family": slot["outfit_family"],
        "outfit_notes": slot["outfit_notes"],
        "mint_accent": slot["mint_accent"],
        "composition": slot["composition"],
        "tone": slot["tone"],
        "risk_note": slot["risk_note"],
        "target_path": f"source/generated/tonari-no-coordinate/{DATE_PREFIX}_{slot['slug']}_v1.webp",
        "reference_pack_inputs": REFERENCE_PACK_INPUTS,
        "prompt": build_prompt(slot),
        "acceptance": build_acceptance(slot),
        "risk_profile": {
            "identity_risk": "high",
            "outfit_drift_risk": outfit_drift_risk_for(slot),
            "age_impression_risk": age_impression_risk_for(slot),
            "hand_risk": hand_risk_for(slot),
            "text_logo_watermark_risk": "medium",
        },
        "review_plan": {
            "initial_status": "draft_candidate",
            "first_pass": "Place in the 12-image coordinate contact sheet before finishing.",
            "coordinate_gate": "Run the Coordinate Gate for outfit variety, Akari identity, age impression, mint accent, and no text/logo/frame issues.",
            "strict_review": "If selected, run akari-v1-1-image-review on this single image.",
            "correction": "Use Correction Pass for concrete face, hairpin, hand, outfit, anatomy, or artifact defects.",
            "humanization": "Use Humanization Pass only after the image is structurally valid.",
        },
    }


def build_manifest(slot_manifest: dict) -> dict:
    promising_slots = [
        slot for slot in slot_manifest["slots"] if slot["priority"] == "promising"
    ]
    return {
        "schema_version": 1,
        "collection_id": COLLECTION_ID,
        "title": TITLE,
        "reference_pack_version": REFERENCE_PACK_VERSION,
        "prompt_template_version": PROMPT_TEMPLATE_VERSION,
        "batch_policy": {
            "request_source": "promising_slots_only",
            "candidate_count": len(promising_slots),
            "review_order": "contact_sheet_before_finishing",
            "pdf_policy": "not_in_first_phase",
        },
        "requests": [build_request(slot) for slot in promising_slots],
    }


def main() -> None:
    slot_manifest = load_json(SLOTS_PATH)
    dump_json(OUTPUT_PATH, build_manifest(slot_manifest))
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
