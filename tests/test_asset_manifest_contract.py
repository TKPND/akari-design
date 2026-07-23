import copy
import json
import sys
from pathlib import Path
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "source/manifests/source-assets.json"
ASSET_MANIFEST = ROOT / "source/manifests/asset-manifest.json"
PAGE_MANIFEST = ROOT / "source/manifests/page-manifest.json"
GENERATION_REQUESTS = ROOT / "source/manifests/generation-requests.json"
SOURCE_PALETTE = ROOT / "source/palette"
SCRIPTS_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import audit_assets


class AssetManifestContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_manifests = {
            "source": json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8")),
            "asset": json.loads(ASSET_MANIFEST.read_text(encoding="utf-8")),
            "page": json.loads(PAGE_MANIFEST.read_text(encoding="utf-8")),
            "generation": json.loads(
                GENERATION_REQUESTS.read_text(encoding="utf-8")
            ),
            "palette": json.loads(
                (SOURCE_PALETTE / "akari-v1.1-palette.json").read_text(
                    encoding="utf-8"
                )
            ),
        }

    def test_logical_audit_never_calls_physical_readers(self):
        manifests = copy.deepcopy(self.base_manifests)

        def unexpected_reader(_path):
            self.fail("logical audit called a physical reader")

        with mock.patch.object(
            audit_assets, "sha256", side_effect=unexpected_reader
        ), mock.patch.object(
            audit_assets, "image_metadata", side_effect=unexpected_reader
        ):
            errors = audit_assets.audit_manifest_data(
                manifests["source"],
                manifests["asset"],
                manifests["page"],
                manifests["generation"],
                manifests["palette"],
                ROOT,
            )
        self.assertEqual([], errors)

    def _audit_with_mutated_manifests(self, mutate):
        result, _stdout, _stderr = self._audit_with_mutated_manifests_and_output(mutate)
        return result

    def _audit_with_mutated_manifests_and_output(self, mutate):
        manifests = copy.deepcopy(self.base_manifests)
        mutate(manifests)
        return self._audit_manifests_and_output(manifests)

    def _audit_manifests_and_output(self, manifests):
        errors = audit_assets.audit_manifest_data(
            manifests["source"],
            manifests["asset"],
            manifests["page"],
            manifests["generation"],
            manifests["palette"],
            ROOT,
        )
        result = 1 if errors else 0
        stdout = "" if errors else "asset audit: ok\n"
        stderr = "\n".join(errors)
        return result, stdout, stderr

    def _add_cover_generated_candidate(self, manifests, **overrides):
        manifests["asset"]["assets"] = [
            asset
            for asset in manifests["asset"]["assets"]
            if asset.get("id") != "cover-key-visual-16x9"
        ]
        generated = dict(manifests["asset"]["assets"][0])
        generated.update(
            {
                "id": "cover-key-visual-16x9",
                "status": "needs_review",
                "source_inputs": [
                    "hoodie-front",
                    "expression-sheet",
                    "footwear-board",
                    "shoe-board",
                ],
                "prompt_summary": "Generated cover key visual candidate for review.",
                "model_or_tool": "image_generation",
                "seed_or_generation_id": "request:cover-key-visual-16x9",
                "palette_version": "akari-v1.1-d65-srgb-1",
                "orientation_state": "front_view_character_left_is_viewer_right",
                "identity_check": "User copied candidate pending final acceptance.",
                "color_check": "Candidate requires visual palette review before acceptance.",
                "layout_check": "16:9 candidate saved for cover review.",
                "reviewer": "user copied candidate; Codex intake pending final acceptance",
                "accepted_reason": "",
                "candidate_path": "source/generated/cover-key-visual-16x9.webp",
                "used_in_final_pdf": False,
            }
        )
        generated.update(overrides)
        manifests["asset"]["assets"].append(generated)
        return generated

    def test_source_manifest_has_ten_assets(self):
        data = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(10, len(data["assets"]))

    def test_asset_entries_have_required_fields(self):
        data = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
        required = {
            "id",
            "original_filename",
            "source_path",
            "sha256",
            "width",
            "height",
            "colorspace",
            "role",
            "orientation_state",
        }
        for asset in data["assets"]:
            self.assertTrue(required.issubset(asset))
            self.assertEqual(64, len(asset["sha256"]))

    def test_audit_rejects_manifest_metadata_drift_when_hash_is_current(self):
        source = copy.deepcopy(self.base_manifests["source"])
        expected_by_path = {
            ROOT / asset["source_path"]: asset
            for asset in self.base_manifests["source"]["assets"]
        }
        asset = source["assets"][0]
        asset["width"] += 1
        asset["height"] += 1
        asset["colorspace"] = "RGB"

        errors = []
        audit_assets.verify_source_files(
            source,
            ROOT,
            errors,
            file_exists=lambda _path: True,
            hash_reader=lambda path: expected_by_path[path]["sha256"],
            metadata_reader=lambda path: {
                field: expected_by_path[path][field]
                for field in ("width", "height", "colorspace")
            },
        )

        self.assertTrue(any("metadata mismatch" in error for error in errors))
        self.assertFalse(any("sha256 mismatch" in error for error in errors))

    def test_audit_rejects_catalog_role_or_orientation_drift(self):
        cases = {
            "role": "unexpected_role",
            "orientation_state": "unexpected_orientation",
        }
        for field, value in cases.items():
            with self.subTest(field=field):
                def mutate(data):
                    data["assets"][0][field] = value

                manifests = copy.deepcopy(self.base_manifests)
                mutate(manifests["source"])
                errors = audit_assets.audit_manifest_data(
                    manifests["source"],
                    manifests["asset"],
                    manifests["page"],
                    manifests["generation"],
                    manifests["palette"],
                    ROOT,
                )

                self.assertTrue(
                    any("source catalog mismatch" in error for error in errors)
                )

    def test_audit_rejects_source_paths_outside_originals_location(self):
        def root_level_path(data):
            asset = data["assets"][0]
            filename = asset["original_filename"]
            asset["source_path"] = filename

        def escaping_path(data):
            asset = data["assets"][0]
            filename = asset["original_filename"]
            asset["source_path"] = f"../outside/{filename}"

        cases = {
            "root-level": root_level_path,
            "escaping": escaping_path,
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                manifests = copy.deepcopy(self.base_manifests)
                mutate(manifests["source"])
                errors = audit_assets.audit_manifest_data(
                    manifests["source"],
                    manifests["asset"],
                    manifests["page"],
                    manifests["generation"],
                    manifests["palette"],
                    ROOT,
                )

                self.assertTrue(
                    any("source_path" in error for error in errors), errors
                )

    def test_audit_rejects_noncanonical_source_path_strings(self):
        def mutate(data):
            asset = data["assets"][0]
            asset["source_path"] = f"./{asset['source_path']}"

        manifests = copy.deepcopy(self.base_manifests)
        mutate(manifests["source"])
        errors = audit_assets.audit_manifest_data(
            manifests["source"],
            manifests["asset"],
            manifests["page"],
            manifests["generation"],
            manifests["palette"],
            ROOT,
        )

        self.assertTrue(any("source_path mismatch" in error for error in errors))

    def test_final_pages_have_accepted_asset_inputs(self):
        asset_manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
        page_manifest = json.loads(PAGE_MANIFEST.read_text(encoding="utf-8"))
        accepted = {
            asset["id"]
            for asset in asset_manifest["assets"]
            if asset["status"] == "accepted"
        }
        self.assertEqual(14, len(page_manifest["pages"]))
        for page in page_manifest["pages"]:
            self.assertTrue(page["source_inputs"])
            for asset_id in page["source_inputs"]:
                self.assertIn(asset_id, accepted)

    def test_audit_rejects_asset_manifest_source_input_outside_source_catalog(self):
        def mutate(manifests):
            manifests["asset"]["assets"][0]["source_inputs"] = ["unknown-source-asset"]

        result = self._audit_with_mutated_manifests(mutate)

        self.assertNotEqual(0, result)

    def test_audit_rejects_asset_manifest_palette_version_drift(self):
        def mutate(manifests):
            manifests["asset"]["palette_version"] = "stale-palette-version"

        result = self._audit_with_mutated_manifests(mutate)

        self.assertNotEqual(0, result)

    def test_audit_rejects_page_source_input_without_accepted_asset(self):
        def mutate(manifests):
            manifests["asset"]["assets"][0]["status"] = "needs_review"
            manifests["asset"]["assets"][0]["used_in_final_pdf"] = False

        result = self._audit_with_mutated_manifests(mutate)

        self.assertNotEqual(0, result)

    def test_audit_rejects_page_count_or_number_drift(self):
        cases = {
            "page_count": lambda manifests: manifests["page"].update({"page_count": 13}),
            "page_numbers": lambda manifests: manifests["page"]["pages"][1].update({"page": 7}),
            "bool_page_number": lambda manifests: manifests["page"]["pages"][0].update(
                {"page": True}
            ),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                result = self._audit_with_mutated_manifests(mutate)

                self.assertNotEqual(0, result)

    def test_audit_rejects_generation_request_target_outside_page_manifest(self):
        def mutate(manifests):
            manifests["generation"]["requests"][0]["target_page"] = 99

        result = self._audit_with_mutated_manifests(mutate)

        self.assertNotEqual(0, result)

    def test_audit_allows_generated_needs_review_request_with_existing_candidate(self):
        def mutate(manifests):
            manifests["generation"]["requests"][0]["status"] = "needs_review"
            manifests["page"]["pages"][0]["source_inputs"] = [
                "hoodie-front",
                "expression-sheet",
            ]
            self._add_cover_generated_candidate(manifests)

        result, _stdout, stderr = self._audit_with_mutated_manifests_and_output(mutate)

        self.assertEqual(0, result, stderr)

    def test_audit_rejects_needs_review_request_without_generated_asset(self):
        def mutate(manifests):
            manifests["generation"]["requests"][0]["status"] = "needs_review"
            manifests["asset"]["assets"] = [
                asset
                for asset in manifests["asset"]["assets"]
                if asset.get("id") != "cover-key-visual-16x9"
            ]

        result, _stdout, stderr = self._audit_with_mutated_manifests_and_output(mutate)

        self.assertNotEqual(0, result)
        self.assertIn("needs_review generation request must have generated asset", stderr)

    def test_audit_rejects_generated_asset_without_existing_request_reference(self):
        cases = {
            "missing": "",
            "unknown": "request:not-a-generation-request",
            "bare": "cover-key-visual-16x9",
        }
        for name, seed_or_generation_id in cases.items():
            with self.subTest(name=name):
                def mutate(manifests):
                    self._add_cover_generated_candidate(
                        manifests,
                        seed_or_generation_id=seed_or_generation_id,
                        candidate_path="",
                    )

                result, _stdout, stderr = self._audit_with_mutated_manifests_and_output(
                    mutate
                )

                self.assertNotEqual(0, result)
                self.assertIn("generated asset seed_or_generation_id", stderr)

    def test_audit_rejects_needs_review_generated_asset_without_candidate_path(self):
        def mutate(manifests):
            manifests["generation"]["requests"][0]["status"] = "needs_review"
            generated = self._add_cover_generated_candidate(manifests)
            del generated["candidate_path"]

        result, _stdout, stderr = self._audit_with_mutated_manifests_and_output(mutate)

        self.assertNotEqual(0, result)
        self.assertIn("needs_review generated asset candidate_path", stderr)

    def test_audit_rejects_generated_asset_for_queued_request(self):
        def mutate(manifests):
            manifests["generation"]["requests"][0]["status"] = "queued"
            self._add_cover_generated_candidate(manifests)

        result, _stdout, stderr = self._audit_with_mutated_manifests_and_output(mutate)

        self.assertNotEqual(0, result)
        self.assertIn("generated asset must not reference queued generation request", stderr)

    def test_audit_rejects_generated_candidate_path_contract_violations(self):
        cases = {
            "absolute": (
                "/tmp/cover-key-visual-16x9.webp",
                "candidate_path must be relative",
            ),
            "outside_generated_dir": (
                "source/originals/v1_1_front_1.webp",
                "candidate_path must be under source/generated",
            ),
        }
        for name, (candidate_path, expected_error) in cases.items():
            with self.subTest(name=name):
                def mutate(manifests):
                    self._add_cover_generated_candidate(
                        manifests,
                        candidate_path=candidate_path,
                    )

                result, _stdout, stderr = self._audit_with_mutated_manifests_and_output(
                    mutate
                )

                self.assertNotEqual(0, result)
                self.assertIn(expected_error, stderr)

    def test_verify_generated_files_rejects_missing_candidate(self):
        manifests = copy.deepcopy(self.base_manifests)
        generated = self._add_cover_generated_candidate(
            manifests,
            candidate_path="source/generated/missing-cover-key-visual-16x9.webp",
        )
        errors = []
        audit_assets.verify_generated_files(
            {"assets": [generated]},
            audit_assets.generation_requests_by_id(manifests["generation"]),
            ROOT,
            errors,
            file_exists=lambda _path: False,
            metadata_reader=lambda _path: self.fail(
                "missing candidate reached metadata reader"
            ),
        )

        self.assertEqual(
            [
                "generated candidate missing: "
                "source/generated/missing-cover-key-visual-16x9.webp"
            ],
            errors,
        )

    def test_audit_rejects_generated_candidate_metadata_mismatches(self):
        cases = {
            "aspect ratio": (
                {"width": 100, "height": 100, "colorspace": "sRGB"},
                "aspect ratio",
            ),
            "colorspace": (
                {"width": 160, "height": 90, "colorspace": "CMYK"},
                "colorspace",
            ),
            "tiny bad ratio": (
                {"width": 16, "height": 8, "colorspace": "sRGB"},
                "minimum dimensions",
            ),
        }
        for name, (metadata, expected_error) in cases.items():
            with self.subTest(name=name):
                manifests = copy.deepcopy(self.base_manifests)
                generated = self._add_cover_generated_candidate(
                    manifests,
                    candidate_path="source/generated/test-candidate.webp",
                )
                errors = []
                audit_assets.verify_generated_files(
                    {"assets": [generated]},
                    audit_assets.generation_requests_by_id(
                        manifests["generation"]
                    ),
                    ROOT,
                    errors,
                    file_exists=lambda _path: True,
                    metadata_reader=lambda _path, value=metadata: value,
                )

                self.assertTrue(
                    any(expected_error in error for error in errors), errors
                )

    def test_aspect_ratio_match_rejects_tiny_bad_ratio(self):
        self.assertFalse(audit_assets.aspect_ratio_matches(16, 8, (16, 9)))

    def test_audit_rejects_page_id_and_title_contract_violations(self):
        cases = {
            "duplicate_id": lambda manifests: manifests["page"]["pages"][1].update(
                {"id": manifests["page"]["pages"][0]["id"]}
            ),
            "blank_id": lambda manifests: manifests["page"]["pages"][0].update({"id": ""}),
            "non_string_id": lambda manifests: manifests["page"]["pages"][0].update(
                {"id": []}
            ),
            "blank_title": lambda manifests: manifests["page"]["pages"][0].update(
                {"title": ""}
            ),
            "non_string_title": lambda manifests: manifests["page"]["pages"][0].update(
                {"title": []}
            ),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                result, _stdout, stderr = self._audit_with_mutated_manifests_and_output(
                    mutate
                )

                self.assertNotEqual(0, result)
                self.assertIn("page", stderr)

    def test_audit_rejects_japanese_characters_in_page_titles(self):
        def mutate(manifests):
            manifests["page"]["pages"][6]["title"] = "髪 / Face Details"

        result, _stdout, stderr = self._audit_with_mutated_manifests_and_output(mutate)

        self.assertNotEqual(0, result)
        self.assertIn("Japanese", stderr)

    def test_audit_rejects_unhashable_page_source_input_without_raising(self):
        def mutate(manifests):
            manifests["page"]["pages"][0]["source_inputs"] = [["hoodie-front"]]

        try:
            result, _stdout, stderr = self._audit_with_mutated_manifests_and_output(mutate)
        except TypeError as error:
            self.fail(f"audit raised TypeError instead of reporting errors: {error}")

        self.assertNotEqual(0, result)
        self.assertIn("page source_input", stderr)

    def test_audit_rejects_duplicate_generation_request_ids(self):
        def mutate(manifests):
            manifests["generation"]["requests"][1]["id"] = manifests["generation"][
                "requests"
            ][0]["id"]

        result, _stdout, stderr = self._audit_with_mutated_manifests_and_output(mutate)

        self.assertNotEqual(0, result)
        self.assertIn("duplicate generation request id", stderr)

    def test_audit_rejects_generation_request_id_or_aspect_ratio_shape(self):
        cases = {
            "blank_id": lambda manifests: manifests["generation"]["requests"][0].update(
                {"id": ""}
            ),
            "non_string_id": lambda manifests: manifests["generation"]["requests"][
                0
            ].update({"id": []}),
            "blank_aspect_ratio": lambda manifests: manifests["generation"]["requests"][
                0
            ].update({"aspect_ratio": ""}),
            "non_string_aspect_ratio": lambda manifests: manifests["generation"][
                "requests"
            ][0].update({"aspect_ratio": []}),
            "malformed_aspect_ratio": lambda manifests: manifests["generation"][
                "requests"
            ][0].update({"aspect_ratio": "not-a-ratio"}),
            "zero_aspect_ratio": lambda manifests: manifests["generation"][
                "requests"
            ][0].update({"aspect_ratio": "16:0"}),
            "newline_aspect_ratio": lambda manifests: manifests["generation"][
                "requests"
            ][0].update({"aspect_ratio": "16:9\n"}),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                result, _stdout, stderr = self._audit_with_mutated_manifests_and_output(
                    mutate
                )

                self.assertNotEqual(0, result)
                self.assertIn("generation request", stderr)

    def test_audit_rejects_unhashable_asset_id_or_source_input_without_raising(self):
        cases = {
            "asset_id": lambda manifests: manifests["asset"]["assets"][0].update(
                {"id": []}
            ),
            "source_input": lambda manifests: manifests["asset"]["assets"][0].update(
                {"source_inputs": [[]]}
            ),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                try:
                    result, _stdout, stderr = (
                        self._audit_with_mutated_manifests_and_output(mutate)
                    )
                except TypeError as error:
                    self.fail(
                        f"audit raised TypeError instead of reporting errors: {error}"
                    )

                self.assertNotEqual(0, result)
                self.assertIn("asset", stderr)

    def test_generation_requests_target_existing_pages(self):
        generation_requests = json.loads(GENERATION_REQUESTS.read_text(encoding="utf-8"))
        asset_manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
        page_manifest = json.loads(PAGE_MANIFEST.read_text(encoding="utf-8"))
        page_numbers = {page["page"] for page in page_manifest["pages"]}
        generated_assets_by_request = {
            asset["seed_or_generation_id"].removeprefix("request:"): asset
            for asset in asset_manifest["assets"]
            if asset.get("model_or_tool") == "image_generation"
            and isinstance(asset.get("seed_or_generation_id"), str)
            and asset["seed_or_generation_id"].startswith("request:")
        }

        self.assertEqual(5, len(generation_requests["requests"]))
        requests_by_id = {
            request["id"]: request
            for request in generation_requests["requests"]
        }
        self.assertEqual("accepted", requests_by_id["cover-key-visual-16x9"]["status"])
        self.assertEqual("accepted", requests_by_id["hair-face-detail-board"]["status"])
        self.assertEqual("accepted", requests_by_id["body-proportion-lock"]["status"])
        self.assertEqual(
            "accepted",
            requests_by_id["hoodie-front-proportion-corrected"]["status"],
        )
        self.assertEqual("accepted", requests_by_id["bag-on-body-scale"]["status"])
        for request in generation_requests["requests"]:
            self.assertIn(request["status"], {"queued", "needs_review", "accepted"})
            self.assertIn(request["target_page"], page_numbers)
            self.assertTrue(request["prompt"].strip())
            self.assertTrue(request["acceptance"].strip())
            if request["status"] in {"needs_review", "accepted"}:
                self.assertIn(request["id"], generated_assets_by_request)

    def test_asset_manifest_records_cover_generated_candidate_for_review(self):
        asset_manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
        generated = {
            asset["id"]: asset
            for asset in asset_manifest["assets"]
            if asset.get("model_or_tool") == "image_generation"
        }
        cover = generated["cover-key-visual-16x9"]

        self.assertEqual("accepted", cover["status"])
        self.assertEqual(
            [
                "hoodie-front",
                "expression-sheet",
                "footwear-board",
                "shoe-board",
            ],
            cover["source_inputs"],
        )
        self.assertEqual("request:cover-key-visual-16x9", cover["seed_or_generation_id"])
        self.assertEqual("akari-v1.1-d65-srgb-1", cover["palette_version"])
        self.assertEqual(
            "front_view_character_left_is_viewer_right",
            cover["orientation_state"],
        )
        self.assertEqual(
            "source/generated/cover-key-visual-16x9.webp",
            cover["candidate_path"],
        )
        self.assertTrue(cover["used_in_final_pdf"])
        self.assertIn("user accepted candidate", cover["reviewer"])
        self.assertIn("user accepted", cover["identity_check"])
        self.assertTrue(cover["accepted_reason"].strip())

    def test_asset_manifest_records_hair_face_detail_generated_candidate_for_review(self):
        asset_manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
        generated = {
            asset["id"]: asset
            for asset in asset_manifest["assets"]
            if asset.get("model_or_tool") == "image_generation"
        }
        hair_face = generated["hair-face-detail-board"]

        self.assertEqual("accepted", hair_face["status"])
        self.assertEqual(
            [
                "expression-sheet",
                "hairpin-side-45",
                "non-hairpin-side-45",
                "side-view",
            ],
            hair_face["source_inputs"],
        )
        self.assertEqual(
            "request:hair-face-detail-board",
            hair_face["seed_or_generation_id"],
        )
        self.assertEqual("akari-v1.1-d65-srgb-1", hair_face["palette_version"])
        self.assertEqual(
            "hair_face_detail_board_unmirrored",
            hair_face["orientation_state"],
        )
        self.assertEqual(
            "source/generated/hair-face-detail-board.webp",
            hair_face["candidate_path"],
        )
        self.assertTrue(hair_face["used_in_final_pdf"])
        self.assertIn("user accepted candidate", hair_face["reviewer"])
        self.assertIn("user accepted", hair_face["identity_check"])
        self.assertTrue(hair_face["accepted_reason"].strip())

    def test_asset_manifest_records_body_proportion_generated_candidate_for_review(self):
        asset_manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
        generated = {
            asset["id"]: asset
            for asset in asset_manifest["assets"]
            if asset.get("model_or_tool") == "image_generation"
        }
        body_proportion = generated["body-proportion-lock"]

        self.assertEqual("accepted", body_proportion["status"])
        self.assertEqual(
            [
                "hoodie-front",
                "base-front",
                "expression-sheet",
            ],
            body_proportion["source_inputs"],
        )
        self.assertEqual(
            "request:body-proportion-lock",
            body_proportion["seed_or_generation_id"],
        )
        self.assertEqual("akari-v1.1-d65-srgb-1", body_proportion["palette_version"])
        self.assertEqual(
            "front_view_character_left_is_viewer_right",
            body_proportion["orientation_state"],
        )
        self.assertEqual(
            "source/generated/akari-body-proportion-option-b.webp",
            body_proportion["candidate_path"],
        )
        self.assertTrue(body_proportion["used_in_final_pdf"])
        self.assertIn("user accepted option B", body_proportion["reviewer"])
        self.assertIn("user accepted option B", body_proportion["identity_check"])
        self.assertTrue(body_proportion["accepted_reason"].strip())

    def test_asset_manifest_records_hoodie_front_proportion_corrected_candidate(self):
        asset_manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
        generated = {
            asset["id"]: asset
            for asset in asset_manifest["assets"]
            if asset.get("model_or_tool") == "image_generation"
        }
        corrected = generated["hoodie-front-proportion-corrected"]

        self.assertEqual("accepted", corrected["status"])
        self.assertEqual(
            [
                "hoodie-front",
                "base-front",
                "expression-sheet",
            ],
            corrected["source_inputs"],
        )
        self.assertEqual(
            "request:hoodie-front-proportion-corrected",
            corrected["seed_or_generation_id"],
        )
        self.assertEqual("akari-v1.1-d65-srgb-1", corrected["palette_version"])
        self.assertEqual(
            "front_view_character_left_is_viewer_right",
            corrected["orientation_state"],
        )
        self.assertEqual(
            "source/generated/akari-hoodie-front-proportion-corrected.webp",
            corrected["candidate_path"],
        )
        self.assertTrue(corrected["used_in_final_pdf"])
        self.assertIn("Codex visual review", corrected["reviewer"])
        self.assertIn("correcting thigh and calf thickness", corrected["identity_check"])
        self.assertTrue(corrected["accepted_reason"].strip())

    def test_asset_manifest_records_bag_on_body_generated_candidate_for_review(self):
        asset_manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
        generated = {
            asset["id"]: asset
            for asset in asset_manifest["assets"]
            if asset.get("model_or_tool") == "image_generation"
        }
        bag_scale = generated["bag-on-body-scale"]

        self.assertEqual("accepted", bag_scale["status"])
        self.assertEqual(
            [
                "hoodie-front",
                "bag-board",
                "footwear-board",
                "shoe-board",
                "expression-sheet",
            ],
            bag_scale["source_inputs"],
        )
        self.assertEqual(
            "request:bag-on-body-scale",
            bag_scale["seed_or_generation_id"],
        )
        self.assertEqual("akari-v1.1-d65-srgb-1", bag_scale["palette_version"])
        self.assertEqual(
            "front_view_character_left_is_viewer_right",
            bag_scale["orientation_state"],
        )
        self.assertEqual(
            "source/generated/bag-on-body-scale.webp",
            bag_scale["candidate_path"],
        )
        self.assertTrue(bag_scale["used_in_final_pdf"])
        self.assertIn("user accepted candidate", bag_scale["reviewer"])
        self.assertIn("user accepted", bag_scale["identity_check"])
        self.assertTrue(bag_scale["accepted_reason"].strip())


if __name__ == "__main__":
    unittest.main()
