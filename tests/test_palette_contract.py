from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from io import StringIO
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
PALETTE = ROOT / "source/palette/akari-v1.1-palette.json"
COLOR_REVIEW = ROOT / "source/manifests/color-review.json"
SCRIPTS_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import audit_palette


class PaletteContractTest(unittest.TestCase):
    def _audit_with_mutated_palette(
        self, mutate, page_manifest=None, color_review=None
    ):
        with tempfile.TemporaryDirectory() as directory:
            temp_root = Path(directory)
            temp_palette = temp_root / "akari-v1.1-palette.json"
            temp_page_manifest = temp_root / "page-manifest.json"
            temp_color_review = temp_root / "color-review.json"

            data = json.loads(PALETTE.read_text(encoding="utf-8"))
            mutate(data)
            temp_palette.write_text(
                json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            color_review_data = json.loads(COLOR_REVIEW.read_text(encoding="utf-8"))
            if color_review is not None:
                color_review_data = color_review
            temp_color_review.write_text(
                json.dumps(color_review_data, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            if page_manifest is not None:
                temp_page_manifest.write_text(
                    json.dumps(page_manifest, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

            stdout = StringIO()
            with mock.patch.object(
                audit_palette, "PALETTE", temp_palette
            ), mock.patch.object(
                audit_palette, "PAGE_MANIFEST", temp_page_manifest
            ), mock.patch.object(
                audit_palette, "COLOR_REVIEW", temp_color_review, create=True
            ), redirect_stdout(
                stdout
            ), redirect_stderr(
                StringIO()
            ):
                return audit_palette.main(), stdout.getvalue()

    def test_palette_roles_are_complete(self):
        data = json.loads(PALETTE.read_text(encoding="utf-8"))
        roles = {role["name"] for role in data["roles"]}
        expected = {
            "hair",
            "skin",
            "eyes",
            "hoodie_white",
            "hoodie_shadow",
            "skirt_gray",
            "sock_white",
            "sock_stripe_blue",
            "sneaker_white",
            "sneaker_accent_blue",
            "bag_body",
            "bag_strap",
            "metal",
        }
        self.assertEqual(expected, roles)

    def test_each_role_has_hex_rgb_usage_and_tolerance(self):
        data = json.loads(PALETTE.read_text(encoding="utf-8"))
        for role in data["roles"]:
            self.assertRegex(role["hex"], r"^#[0-9A-Fa-f]{6}$")
            self.assertEqual(3, len(role["rgb"]))
            self.assertTrue(role["usage"])
            self.assertIn("median_rgb_delta", role["tolerance"])

    def test_audit_reports_success_with_role_count(self):
        result, output = self._audit_with_mutated_palette(lambda _data: None)

        self.assertEqual(0, result)
        self.assertEqual("palette audit: ok (13 roles)\n", output)

    def test_audit_rejects_palette_contract_drift(self):
        cases = {
            "white_point": lambda data: data.__setitem__("white_point", "D50"),
            "color_space": lambda data: data.__setitem__("color_space", "Adobe RGB"),
            "duplicate_role": lambda data: data["roles"].append(
                deepcopy(data["roles"][0])
            ),
            "empty_roles": lambda data: data.__setitem__("roles", []),
            "renamed_role": lambda data: data["roles"][0].__setitem__(
                "name", "hair_alt"
            ),
            "bad_hex": lambda data: data["roles"][0].__setitem__("hex", "#XYZ123"),
            "rgb_mismatch": lambda data: data["roles"][0].__setitem__(
                "rgb", [0, 0, 0]
            ),
            "missing_tolerance": lambda data: data["roles"][0]["tolerance"].pop(
                "median_rgb_delta"
            ),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                result, _output = self._audit_with_mutated_palette(mutate)

                self.assertNotEqual(0, result)

    def test_audit_rejects_invalid_role_ramp(self):
        cases = {
            "missing_ramp": lambda data: data["roles"][0].pop("ramp"),
            "missing_ramp_key": lambda data: data["roles"][0]["ramp"].pop("shadow"),
            "bad_ramp_hex": lambda data: data["roles"][0]["ramp"].__setitem__(
                "shadow", "#NOPE00"
            ),
            "base_hex_drift": lambda data: data["roles"][0]["ramp"].__setitem__(
                "base", "#000000"
            ),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                result, _output = self._audit_with_mutated_palette(mutate)

                self.assertNotEqual(0, result)

    def test_audit_rejects_invalid_median_rgb_delta(self):
        cases = {
            "string_delta": lambda data: data["roles"][0]["tolerance"].__setitem__(
                "median_rgb_delta", "12"
            ),
            "zero_delta": lambda data: data["roles"][0]["tolerance"].__setitem__(
                "median_rgb_delta", 0
            ),
            "negative_delta": lambda data: data["roles"][0]["tolerance"].__setitem__(
                "median_rgb_delta", -1
            ),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                result, _output = self._audit_with_mutated_palette(mutate)

                self.assertNotEqual(0, result)

    def test_audit_rejects_empty_role_metadata(self):
        cases = {
            "empty_usage": lambda data: data["roles"][0].__setitem__("usage", ""),
            "empty_sample_area": lambda data: data["roles"][0].__setitem__(
                "sample_area", ""
            ),
            "empty_exception_policy": lambda data: data["roles"][0].__setitem__(
                "exception_policy", ""
            ),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                result, _output = self._audit_with_mutated_palette(mutate)

                self.assertNotEqual(0, result)

    def test_audit_rejects_color_review_palette_version_drift(self):
        color_review = json.loads(COLOR_REVIEW.read_text(encoding="utf-8"))
        color_review["palette_version"] = "not-the-palette-version"

        result, _output = self._audit_with_mutated_palette(
            lambda _data: None,
            color_review=color_review,
        )

        self.assertNotEqual(0, result)

    def test_audit_rejects_missing_palette_version(self):
        color_review = json.loads(COLOR_REVIEW.read_text(encoding="utf-8"))
        color_review.pop("palette_version")

        def mutate(data):
            data.pop("palette_version")

        result, _output = self._audit_with_mutated_palette(
            mutate,
            color_review=color_review,
        )

        self.assertNotEqual(0, result)

    def test_audit_rejects_wrong_palette_page_count_when_manifest_exists(self):
        cases = {
            "no_palette_page": {"pages": [{"role": "cover"}]},
            "two_palette_pages": {"pages": [{"role": "palette"}, {"role": "palette"}]},
        }
        for name, page_manifest in cases.items():
            with self.subTest(name=name):
                result, _output = self._audit_with_mutated_palette(
                    lambda _data: None,
                    page_manifest,
                )

                self.assertNotEqual(0, result)


if __name__ == "__main__":
    unittest.main()
