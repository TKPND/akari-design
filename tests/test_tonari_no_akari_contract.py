import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "source/manifests/tonari-no-akari"
REFERENCE_DIR = ROOT / "source/references/tonari-no-akari"
SOURCE_ASSETS = MANIFEST_DIR / "source-assets.json"
ASSET_MANIFEST = MANIFEST_DIR / "asset-manifest.json"
PAGE_MANIFEST = MANIFEST_DIR / "page-manifest.json"
GENERATION_REQUESTS = MANIFEST_DIR / "generation-requests.json"
DOCUMENT_ID = "akari-v1.1-tonari-no-akari"
JAPANESE_TEXT = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
EXPECTED_RANGES = {
    "いつもの距離",
    "少し甘め",
    "元気な一瞬",
    "静かな余韻",
    "服で魅せる",
    "全身ポーズ",
}
EXPECTED_REFERENCE_COPIES = {
    "identity-face-hair.webp": "source/originals/v1_1_front_3.webp",
    "identity-body-base.webp": "source/originals/v1_1_front_2.webp",
    "identity-basic-outfit.webp": "source/originals/v1_1_front_1.webp",
    "identity-side-view.webp": "source/originals/v1_1_真横.webp",
}
EXPECTED_CATALOGUE = [
    {
        "page": 1,
        "id": "morning-glance",
        "internal_range": "いつもの距離",
        "title": "朝の合図",
        "display_line": "目が合うだけで、今日が少し近くなる。",
        "target_path": "source/generated/tonari-no-akari/20260701_morning-glance_v1.webp",
    },
    {
        "page": 2,
        "id": "window-breath",
        "internal_range": "静かな余韻",
        "title": "窓辺の息",
        "display_line": "光の中で、言葉がゆっくりほどけていく。",
        "target_path": "source/generated/tonari-no-akari/20260701_window-breath_v1.webp",
    },
    {
        "page": 3,
        "id": "turn-back-smile",
        "internal_range": "いつもの距離",
        "title": "ふりむき笑顔",
        "display_line": "呼ばれた気がして、少しだけ足を止めた。",
        "target_path": "source/generated/tonari-no-akari/20260701_turn-back-smile_v1.webp",
    },
    {
        "page": 4,
        "id": "near-eye-contact",
        "internal_range": "少し甘め",
        "title": "近くのまなざし",
        "display_line": "照れた声より先に、まなざしが届く。",
        "target_path": "source/generated/tonari-no-akari/20260701_near-eye-contact_v1.webp",
    },
    {
        "page": 5,
        "id": "light-cardigan",
        "internal_range": "服で魅せる",
        "title": "薄手の羽織り",
        "display_line": "いつもの服に、やわらかな風を重ねて。",
        "target_path": "source/generated/tonari-no-akari/20260701_light-cardigan_v1.webp",
    },
    {
        "page": 6,
        "id": "afternoon-stretch",
        "internal_range": "元気な一瞬",
        "title": "背伸びの午後",
        "display_line": "伸ばした指先まで、夏の光が跳ねる。",
        "target_path": "source/generated/tonari-no-akari/20260701_afternoon-stretch_v1.webp",
    },
    {
        "page": 7,
        "id": "seated-distance",
        "internal_range": "全身ポーズ",
        "title": "腰かける距離",
        "display_line": "隣に座る余白まで、ちゃんと残して。",
        "target_path": "source/generated/tonari-no-akari/20260701_seated-distance_v1.webp",
    },
    {
        "page": 8,
        "id": "shy-half-smile",
        "internal_range": "少し甘め",
        "title": "照れ笑い",
        "display_line": "言いかけた言葉を、笑顔がそっと隠す。",
        "target_path": "source/generated/tonari-no-akari/20260701_shy-half-smile_v1.webp",
    },
    {
        "page": 9,
        "id": "roomwear-morning",
        "internal_range": "服で魅せる",
        "title": "部屋着の朝",
        "display_line": "気を抜いた時間にも、あかりらしさがある。",
        "target_path": "source/generated/tonari-no-akari/20260701_roomwear-morning_v1.webp",
    },
    {
        "page": 10,
        "id": "walking-beside",
        "internal_range": "いつもの距離",
        "title": "となりを歩く",
        "display_line": "歩幅がそろうと、景色までやさしくなる。",
        "target_path": "source/generated/tonari-no-akari/20260701_walking-beside_v1.webp",
    },
    {
        "page": 11,
        "id": "profile-light",
        "internal_range": "静かな余韻",
        "title": "横顔の光",
        "display_line": "静けさの中で、輪郭だけが少し大人びる。",
        "target_path": "source/generated/tonari-no-akari/20260701_profile-light_v1.webp",
    },
    {
        "page": 12,
        "id": "small-peace",
        "internal_range": "元気な一瞬",
        "title": "小さなピース",
        "display_line": "はしゃぎすぎない合図が、いちばん似合う。",
        "target_path": "source/generated/tonari-no-akari/20260701_small-peace_v1.webp",
    },
    {
        "page": 13,
        "id": "looking-up",
        "internal_range": "少し甘め",
        "title": "見上げる距離",
        "display_line": "近すぎないのに、声だけはすぐそばにある。",
        "target_path": "source/generated/tonari-no-akari/20260701_looking-up_v1.webp",
    },
    {
        "page": 14,
        "id": "chair-pause",
        "internal_range": "全身ポーズ",
        "title": "椅子の上で",
        "display_line": "足元まで自然に、ひと休みの形。",
        "target_path": "source/generated/tonari-no-akari/20260701_chair-pause_v1.webp",
    },
    {
        "page": 15,
        "id": "special-outing",
        "internal_range": "服で魅せる",
        "title": "少しだけ特別",
        "display_line": "特別すぎない服で、いつもの道が変わる。",
        "target_path": "source/generated/tonari-no-akari/20260701_special-outing_v1.webp",
    },
    {
        "page": 16,
        "id": "small-run",
        "internal_range": "元気な一瞬",
        "title": "小走りの影",
        "display_line": "振り返る前から、楽しそうな気配がする。",
        "target_path": "source/generated/tonari-no-akari/20260701_small-run_v1.webp",
    },
    {
        "page": 17,
        "id": "sleepy-afternoon",
        "internal_range": "静かな余韻",
        "title": "眠たげな午後",
        "display_line": "まぶたの重さも、今日はやさしい表情になる。",
        "target_path": "source/generated/tonari-no-akari/20260701_sleepy-afternoon_v1.webp",
    },
    {
        "page": 18,
        "id": "almost-touching",
        "internal_range": "少し甘め",
        "title": "指先の間",
        "display_line": "触れそうで触れないくらいが、ちょうどいい。",
        "target_path": "source/generated/tonari-no-akari/20260701_almost-touching_v1.webp",
    },
    {
        "page": 19,
        "id": "straight-stance",
        "internal_range": "全身ポーズ",
        "title": "まっすぐ立つ",
        "display_line": "全身のバランスに、あかりの芯が見える。",
        "target_path": "source/generated/tonari-no-akari/20260701_straight-stance_v1.webp",
    },
    {
        "page": 20,
        "id": "crouching-gesture",
        "internal_range": "全身ポーズ",
        "title": "しゃがむ仕草",
        "display_line": "何気ない姿勢ほど、らしさが出る。",
        "target_path": "source/generated/tonari-no-akari/20260701_crouching-gesture_v1.webp",
    },
    {
        "page": 21,
        "id": "evening-cardigan",
        "internal_range": "静かな余韻",
        "title": "夕方の羽織り",
        "display_line": "一日の終わりに、少しだけ声がやわらぐ。",
        "target_path": "source/generated/tonari-no-akari/20260701_evening-cardigan_v1.webp",
    },
    {
        "page": 22,
        "id": "over-shoulder-voice",
        "internal_range": "いつもの距離",
        "title": "肩越しの声",
        "display_line": "先に行きすぎないように、振り返ってくれる。",
        "target_path": "source/generated/tonari-no-akari/20260701_over-shoulder-voice_v1.webp",
    },
    {
        "page": 23,
        "id": "skirt-in-breeze",
        "internal_range": "元気な一瞬",
        "title": "スカートの風",
        "display_line": "軽く揺れる裾に、元気な気配だけ残る。",
        "target_path": "source/generated/tonari-no-akari/20260701_skirt-in-breeze_v1.webp",
    },
    {
        "page": 24,
        "id": "homeward-smile",
        "internal_range": "いつもの距離",
        "title": "帰り道の笑顔",
        "display_line": "また明日、と言う前の表情を残しておく。",
        "target_path": "source/generated/tonari-no-akari/20260701_homeward-smile_v1.webp",
    },
]
EXPECTED_PAGE_IDS = [page["id"] for page in EXPECTED_CATALOGUE]
PROMPT_TEMPLATE_VERSION = "tonari_identity_lock_v2"
IDENTITY_LOCK_VERSION = "tonari-no-akari-identity-v1"
IDENTITY_LOCK_PHRASES = [
    "adult 25-year-old japanese woman",
    "naturally cute adult",
    "not glamorous",
    "not model-like",
    "not pin-up",
    "not childlike",
    "short fluffy light-brown bob",
    "airy uneven ends",
    "soft side bangs",
    "warm amber eyes",
    "round cheeks",
    "compact rounded chin",
    "small subtle nose/mouth",
    "pale-blue crossed hairpins/ribbon clips",
    "character-left side when visible",
    "petite/slender healthy adult proportions",
    "no image-internal readable text",
    "no logos",
    "no watermarks",
]
EXISTING_CANDIDATE_PAGE_IDS = set(EXPECTED_PAGE_IDS)
FEET_VISIBLE_BASIC_OUTFIT_PAGE_IDS = {
    "seated-distance",
    "walking-beside",
    "chair-pause",
    "small-run",
    "straight-stance",
    "crouching-gesture",
}
HAND_RISK_PAGE_IDS = {
    "afternoon-stretch",
    "small-peace",
    "almost-touching",
    "crouching-gesture",
}


def load_json(path):
    with path.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class TonariNoAkariContractTest(unittest.TestCase):
    def test_tonari_manifests_exist(self):
        for manifest_path in (SOURCE_ASSETS, ASSET_MANIFEST, PAGE_MANIFEST, GENERATION_REQUESTS):
            with self.subTest(manifest=manifest_path.name):
                self.assertTrue(manifest_path.is_file(), f"missing manifest: {manifest_path}")

    def test_package_scripts_expose_tonari_build_and_audit(self):
        package_json = load_json(ROOT / "package.json")
        scripts = package_json["scripts"]
        self.assertEqual(
            "uv run python scripts/render_tonari_no_akari_previews.py",
            scripts["build:tonari:previews"],
        )
        self.assertEqual(
            "uv run python scripts/export_tonari_no_akari_pdf.py",
            scripts["build:tonari:pdf"],
        )
        self.assertEqual(
            "uv run python scripts/audit_tonari_no_akari_pdf.py dist/akari-v1.1-tonari-no-akari.pdf",
            scripts["audit:tonari:pdf"],
        )

    def test_reference_pack_copies_minimum_identity_sources(self):
        source_assets = load_json(SOURCE_ASSETS)
        assets_by_filename = {
            Path(asset["source_path"]).name: asset for asset in source_assets["assets"]
        }

        for copy_name, original_relative_path in EXPECTED_REFERENCE_COPIES.items():
            with self.subTest(copy=copy_name):
                copied = REFERENCE_DIR / copy_name
                original = ROOT / original_relative_path
                self.assertTrue(copied.is_file(), f"missing reference copy: {copied}")
                self.assertTrue(original.is_file(), f"missing original source: {original}")
                self.assertEqual(sha256(original), sha256(copied))
                self.assertIn(copy_name, assets_by_filename)
                self.assertEqual(original_relative_path, assets_by_filename[copy_name]["original_source_path"])
                self.assertEqual(sha256(original), assets_by_filename[copy_name]["original_sha256"])

    def test_page_manifest_has_24_portrait_artwork_pages(self):
        page_manifest = load_json(PAGE_MANIFEST)
        self.assertEqual(DOCUMENT_ID, page_manifest["document_id"])
        self.assertEqual("となりのあかり", page_manifest["title"])
        self.assertEqual(24, page_manifest["page_count"])

        pages = page_manifest["pages"]
        self.assertEqual(list(range(1, 25)), [page["page"] for page in pages])
        self.assertEqual(EXPECTED_PAGE_IDS, [page["id"] for page in pages])

        for page, expected_page in zip(pages, EXPECTED_CATALOGUE, strict=True):
            with self.subTest(page=page["id"]):
                self.assertEqual(expected_page["page"], page["page"])
                self.assertEqual(expected_page["id"], page["id"])
                self.assertEqual("artwork", page["role"])
                self.assertEqual("tonari-portrait", page["layout"])
                self.assertEqual(expected_page["internal_range"], page["internal_range"])
                self.assertIn(expected_page["internal_range"], EXPECTED_RANGES)
                self.assertEqual(expected_page["title"], page["title"])
                self.assertEqual(expected_page["display_line"], page["display_line"])
                self.assertEqual(expected_page["target_path"], page["target_path"])
                self.assertEqual([f"tonari-{expected_page['id']}"], page["source_inputs"])
                self.assertTrue(JAPANESE_TEXT.search(page["title"]), page["title"])
                self.assertTrue(JAPANESE_TEXT.search(page["display_line"]), page["display_line"])
                self.assertEqual([{"type": "portrait-plate"}], page["blocks"])
                self.assertNotIn("cover", page["role"])
                self.assertNotIn("chapter", page["role"])

    def test_asset_manifest_tracks_planned_final_images(self):
        asset_manifest = load_json(ASSET_MANIFEST)
        assets = asset_manifest["assets"]
        self.assertEqual(DOCUMENT_ID, asset_manifest["document_id"])
        self.assertEqual(24, len(assets))
        self.assertEqual(EXPECTED_PAGE_IDS, [asset["id"].removeprefix("tonari-") for asset in assets])

        for asset in assets:
            with self.subTest(asset=asset["id"]):
                self.assertIn(asset["status"], {"planned", "accepted"})
                self.assertEqual("image_generation", asset["model_or_tool"])
                self.assertTrue(asset["candidate_path"].startswith("source/generated/tonari-no-akari/"))
                self.assertTrue(asset["candidate_path"].endswith("_v1.webp"))
                self.assertTrue(asset["used_in_tonari_pdf"])
                self.assertIn("no intentional readable text", asset["layout_check"].lower())

    def test_asset_manifest_records_visual_review_and_variant_tags(self):
        asset_manifest = load_json(ASSET_MANIFEST)

        for asset in asset_manifest["assets"]:
            page_id = asset["id"].removeprefix("tonari-")
            with self.subTest(asset=asset["id"]):
                visual_review = asset["visual_review"]
                variant_tags = asset["variant_tags"]
                self.assertEqual(IDENTITY_LOCK_VERSION, variant_tags["identity_lock_version"])
                self.assertEqual(PROMPT_TEMPLATE_VERSION, variant_tags["prompt_template_version"])
                self.assertEqual(page_id in EXISTING_CANDIDATE_PAGE_IDS, variant_tags["candidate_exists"])
                self.assertIn("outfit_variant", variant_tags)
                self.assertIn("camera_distance", variant_tags)
                self.assertIn("hand_risk", variant_tags)
                self.assertIn("feet_visible", variant_tags)

                self.assertEqual("accepted", asset["status"])
                self.assertEqual("accepted", visual_review["status"])
                self.assertEqual("accepted", visual_review["decision"])
                self.assertEqual([], visual_review["fail_reasons"])
                self.assertEqual("final_contact_sheet_review", visual_review["review_stage"])
                self.assertTrue(variant_tags["candidate_exists"])

                if page_id == "walking-beside":
                    self.assertIn("prior_footwear_fail", visual_review["history"])
                    self.assertIn("regenerated_with_official_footwear_lock", visual_review["history"])

                if page_id == "seated-distance":
                    self.assertIn("indoor_socks_ok", visual_review["conditions"])

    def test_generation_requests_are_lightweight_until_final_pdf(self):
        generation_requests = load_json(GENERATION_REQUESTS)
        self.assertEqual(DOCUMENT_ID, generation_requests["document_id"])
        self.assertEqual(
            "final_pdf_only",
            generation_requests["audit_policy"]["heavy_pdf_or_ocr_audit"],
        )
        self.assertIn("identity", generation_requests["candidate_stage_checks"])
        self.assertIn("image-internal text", generation_requests["candidate_stage_checks"])

        requests = generation_requests["requests"]
        self.assertEqual(24, len(requests))
        self.assertEqual(EXPECTED_PAGE_IDS, [request["page_id"] for request in requests])
        for request in requests:
            with self.subTest(request=request["page_id"]):
                prompt = request["prompt"].lower()
                self.assertIn("no readable text", prompt)
                self.assertIn("no logos", prompt)
                self.assertIn("no watermark", prompt)
                self.assertNotIn("ocr each candidate", prompt)
                self.assertEqual(4, len(request["reference_pack_inputs"]))

    def test_generation_requests_lock_prompt_identity_template_metadata(self):
        generation_requests = load_json(GENERATION_REQUESTS)

        for request in generation_requests["requests"]:
            page_id = request["page_id"]
            with self.subTest(request=page_id):
                self.assertEqual(PROMPT_TEMPLATE_VERSION, request["prompt_template_version"])
                self.assertEqual(IDENTITY_LOCK_VERSION, request["identity_lock_version"])
                self.assertIsInstance(request["risk_profile"], dict)
                self.assertIsInstance(request["required_invariants"], list)
                self.assertIsInstance(request["conditional_invariants"], dict)
                for field in (
                    "outfit_variant",
                    "camera_distance",
                    "hands_policy",
                    "footwear_policy",
                    "background_policy",
                ):
                    self.assertIn(field, request)

                prompt = request["prompt"].lower()
                invariant_text = " ".join(request["required_invariants"]).lower()
                for phrase in IDENTITY_LOCK_PHRASES:
                    self.assertIn(phrase, prompt)
                    self.assertIn(phrase, invariant_text)

    def test_hand_and_footwear_risk_policies_are_explicit(self):
        generation_requests = load_json(GENERATION_REQUESTS)
        requests_by_page_id = {
            request["page_id"]: request for request in generation_requests["requests"]
        }

        afternoon = requests_by_page_id["afternoon-stretch"]
        afternoon_text = f"{afternoon['prompt']} {afternoon['hands_policy']}".lower()
        self.assertNotIn("hands visible and connected", afternoon_text)
        self.assertNotIn("connected hands", afternoon_text)
        self.assertIn("one-arm stretch", afternoon_text)

        for page_id in HAND_RISK_PAGE_IDS:
            request = requests_by_page_id[page_id]
            with self.subTest(hand_risk_page=page_id):
                hands_policy = request["hands_policy"].lower()
                self.assertNotEqual("low", request["risk_profile"]["hand_risk"])
                self.assertIn("avoid interlocked", hands_policy)
                self.assertIn("overlapping", hands_policy)
                self.assertIn("merged hands", hands_policy)

        for page_id in FEET_VISIBLE_BASIC_OUTFIT_PAGE_IDS:
            request = requests_by_page_id[page_id]
            with self.subTest(feet_visible_basic_outfit=page_id):
                self.assertEqual("basic_outfit", request["outfit_variant"])
                footwear_policy = request["footwear_policy"].lower()
                self.assertIn("feet are visible", footwear_policy)
                self.assertIn("official white crew socks", footwear_policy)
                self.assertIn("two pale blue stripes", footwear_policy)
                self.assertIn("chunky white sneakers", footwear_policy)
                self.assertIn("pale-blue accents", footwear_policy)

    def test_manifests_link_pages_assets_and_generation_requests(self):
        page_manifest = load_json(PAGE_MANIFEST)
        asset_manifest = load_json(ASSET_MANIFEST)
        generation_requests = load_json(GENERATION_REQUESTS)
        assets_by_id = {asset["id"]: asset for asset in asset_manifest["assets"]}
        requests_by_page_id = {
            request["page_id"]: request for request in generation_requests["requests"]
        }

        self.assertEqual(24, len(assets_by_id))
        self.assertEqual(24, len(requests_by_page_id))

        for page, expected_page in zip(page_manifest["pages"], EXPECTED_CATALOGUE, strict=True):
            with self.subTest(page=page["id"]):
                page_id = expected_page["id"]
                asset_id = f"tonari-{page_id}"
                request_id = f"request:{asset_id}"
                self.assertEqual(page_id, page["id"])
                self.assertEqual(asset_id, page["source_inputs"][0])
                self.assertIn(asset_id, assets_by_id)
                self.assertIn(page_id, requests_by_page_id)

                asset = assets_by_id[asset_id]
                request = requests_by_page_id[page_id]
                self.assertEqual(request_id, asset["seed_or_generation_id"])
                self.assertEqual(request_id, request["id"])
                self.assertEqual(expected_page["target_path"], page["target_path"])
                self.assertEqual(page["target_path"], asset["candidate_path"])
                self.assertEqual(asset["candidate_path"], request["target_path"])
                self.assertEqual(page["internal_range"], request["range"])


if __name__ == "__main__":
    unittest.main()
