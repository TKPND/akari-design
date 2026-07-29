import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WorkflowGateContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scripts = json.loads(
            (ROOT / "package.json").read_text(encoding="utf-8")
        )["scripts"]

    def test_lightweight_and_integration_gates_are_explicit(self):
        expected = {
            "test:node": (
                "node --test --test-concurrency=1 "
                "tools/pdf/*.test.mjs tools/review-gallery/*.test.mjs"
            ),
            "test:python:review-gallery": (
                "uv run python -m unittest "
                "tests.test_init_akari_v1_5_kawaii_1000 "
                "tests.test_build_akari_review_thumbnail -v"
            ),
            "gallery:serve": "node tools/review-gallery/server.mjs",
            "gate:v1-5:gallery": (
                "npm run test:node && npm run test:python:review-gallery && "
                "npm run lint:md"
            ),
            "test:python:natural-form": (
                "uv run python -m unittest "
                "tests.test_akari_v1_2_natural_form_package -v"
            ),
            "test:python:v1-3": (
                "uv run python -m unittest "
                "tests.test_akari_v1_3_base_package -v"
            ),
            "validate:v1-3": (
                "uv run python scripts/validate_akari_v1_3_base.py"
            ),
            "verify:v1-2:release-pins": (
                "uv run python scripts/verify_v1_2_release_pins.py"
            ),
            "audit:v1-1:pdf:structure": (
                "uv run python scripts/audit_pdf.py --level structure "
                "dist/akari-v1.1-settings.pdf"
            ),
            "audit:v1-2:pdf:structure": (
                "uv run python scripts/audit_akari_v1_2_pdf.py --level structure"
            ),
            "gate:edit:d02": (
                "npm run test:python:daily && npm run test:python:natural-form "
                "&& npm run validate:v1-2 && npm run verify:v1-2:release-pins"
            ),
            "gate:common:v1-2": (
                "npm run test:python:root && npm run test:node && "
                "npm run validate:v1-2 && npm run audit:assets && "
                "npm run audit:palette && npm run audit:alpha && npm run lint:md"
            ),
            "gate:integration:v1-2": (
                "npm run gate:common:v1-2 && npm run audit:v1-2:pdf:structure "
                "&& npm run verify:v1-2:release-pins"
            ),
            "gate:integration:all": (
                "npm run gate:integration:v1-2 && "
                "npm run test:python:legacy-v1-2 && "
                "npm run audit:v1-1:pdf:structure"
            ),
            "gate:integration:v1-3": (
                "npm run test:python:v1-3 && npm run validate:v1-3 && "
                "npm run lint:md"
            ),
            "gate:release:v1-2": (
                "npm run gate:common:v1-2 && npm run build:v1-2:pdf && "
                "npm run audit:v1-2:pdf && npm run verify:v1-2:release-pins"
            ),
            "gate:release:v1-1": (
                "npm run gate:common:v1-2 && npm run build:v1-1:pdf && "
                "npm run audit:v1-1:pdf"
            ),
        }
        for name, command in expected.items():
            with self.subTest(name=name):
                self.assertEqual(command, self.scripts.get(name))

    def test_v1_3_integration_gate_stays_focused(self):
        command = self.scripts["gate:integration:v1-3"]
        self.assertEqual(
            "npm run test:python:v1-3 && npm run validate:v1-3 && npm run lint:md",
            command,
        )
        lowered = command.lower()
        for forbidden in ("pdf", "ocr", "tesseract", "chromium"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, lowered)

    def test_v1_5_gallery_gate_excludes_pdf_and_ocr(self):
        command = self.scripts["gate:v1-5:gallery"].lower()
        for forbidden in ("pdf", "ocr", "tesseract", "poppler"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, command)

    def test_daily_gate_uses_explicit_existing_modules(self):
        command = self.scripts["test:python:daily"]
        self.assertIn("tests.test_build_v1_2_d01_comparison", command)
        self.assertNotIn("discover", command)

    def test_markdown_lint_targets_tracked_files_only(self):
        self.assertEqual(
            "git ls-files -z -- '*.md' | "
            "xargs -0 --no-run-if-empty markdownlint-cli2",
            self.scripts["lint:md"],
        )
        self.assertNotIn("**/*.md", self.scripts["lint:md"])

    def test_full_pdf_aliases_are_explicit_and_release_is_not_double_audited(self):
        self.assertEqual(
            "uv run python scripts/audit_pdf.py --level full "
            "dist/akari-v1.1-settings.pdf",
            self.scripts["audit:v1-1:pdf"],
        )
        self.assertEqual(
            "uv run python scripts/audit_akari_v1_2_pdf.py --level full",
            self.scripts["audit:v1-2:pdf"],
        )
        self.assertNotIn(
            "audit:v1-2:pdf:structure", self.scripts["gate:release:v1-2"]
        )

    def test_gates_do_not_select_checks_from_untracked_files(self):
        gate_commands = "\n".join(
            command
            for name, command in self.scripts.items()
            if name.startswith("gate:")
        )
        self.assertNotIn("run_changed_checks", gate_commands)
        self.assertNotIn("git ls-files", gate_commands)


if __name__ == "__main__":
    unittest.main()
