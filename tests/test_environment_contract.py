import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import tomllib
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
PACKAGE_JSON = ROOT / "package.json"
REQUIREMENTS = ROOT / "requirements.txt"
VERIFY_ENVIRONMENT = ROOT / "scripts/verify_environment.py"
GITATTRIBUTES = ROOT / ".gitattributes"

EXPECTED_REQUIRED_TOOLS = [
    "python3",
    "uv",
    "node",
    "npm",
    "google-chrome",
    "identify",
    "compare",
    "pdfinfo",
    "pdffonts",
    "pdftoppm",
    "pdftotext",
    "qpdf",
    "exiftool",
]


def load_verify_environment():
    spec = importlib.util.spec_from_file_location(
        "verify_environment", VERIFY_ENVIRONMENT
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EnvironmentContractTest(unittest.TestCase):
    def setUp(self):
        self.verify_environment = load_verify_environment()

    def test_verify_environment_exposes_expected_tool_contract(self):
        self.assertEqual(
            EXPECTED_REQUIRED_TOOLS, self.verify_environment.REQUIRED_TOOLS
        )

    def test_required_tools_are_available(self):
        missing = [
            tool
            for tool in self.verify_environment.REQUIRED_TOOLS
            if shutil.which(tool) is None
        ]
        self.assertEqual([], missing)

    def test_pyproject_declares_pillow_dependency(self):
        self.assertTrue(PYPROJECT.exists())
        data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
        self.assertIn("Pillow>=10,<13", data["project"]["dependencies"])

    def test_requirements_matches_pyproject_dependency(self):
        data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
        requirements = [
            line.strip()
            for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        ]
        self.assertEqual(data["project"]["dependencies"], requirements)

    def test_python_workflow_scripts_use_uv(self):
        package_data = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
        scripts = package_data["scripts"]
        python_scripts = [
            "test:python",
            "prepare:sources",
            "build:v1-1:previews",
            "build:v1-1:pdf",
            "build:v1-2:pdf",
            "build:daybook:previews",
            "build:daybook:pdf",
            "audit:assets",
            "audit:palette",
            "audit:v1-1:pdf",
            "audit:v1-2:pdf",
            "audit:daybook:pdf",
            "audit:alpha",
        ]
        for script_name in python_scripts:
            self.assertTrue(
                scripts[script_name].startswith("uv run python"),
                msg=f"{script_name} must run through uv",
            )

    def test_settings_pdf_commands_preserve_v1_1_and_default_to_v1_2(self):
        scripts = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))["scripts"]
        expected = {
            "build:v1-1:previews": "uv run python scripts/render_page_previews.py",
            "build:v1-1:pdf": "uv run python scripts/export_pdf.py",
            "audit:v1-1:pdf": (
                "uv run python scripts/audit_pdf.py --level full "
                "dist/akari-v1.1-settings.pdf"
            ),
            "build:v1-2:previews": (
                "node tools/pdf/render.mjs --document natural-form --previews"
            ),
            "build:v1-2:pdf": "uv run python scripts/export_akari_v1_2_pdf.py",
            "audit:v1-2:pdf": (
                "uv run python scripts/audit_akari_v1_2_pdf.py --level full"
            ),
            "build:previews": "npm run build:v1-2:previews",
            "build:pdf": "npm run build:v1-2:pdf",
            "audit:pdf": "npm run audit:v1-2:pdf",
            "release:v1-2": (
                "npm run validate:v1-2 && npm run build:v1-2:pdf && "
                "npm run audit:v1-2:pdf"
            ),
        }
        self.assertEqual(expected, {name: scripts.get(name) for name in expected})
        self.assertIn("npm run audit:v1-1:pdf", scripts["audit"])
        self.assertIn("npm run audit:v1-2:pdf", scripts["audit"])

    def test_pdf_files_are_declared_binary_for_git(self):
        self.assertTrue(GITATTRIBUTES.is_file())
        rules = {
            line.strip()
            for line in GITATTRIBUTES.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        self.assertIn("*.pdf binary", rules)

    def test_qpdf_runs(self):
        result = subprocess.run(
            ["qpdf", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("qpdf version", result.stdout)

    def test_version_probe_failure_returns_clean_error(self):
        failure = subprocess.CalledProcessError(
            returncode=2,
            cmd=["qpdf", "--version"],
            output="",
            stderr="broken qpdf",
        )
        stderr = io.StringIO()
        with mock.patch.object(
            self.verify_environment.subprocess, "run", side_effect=failure
        ):
            with contextlib.redirect_stderr(stderr):
                try:
                    result = self.verify_environment.main()
                except subprocess.CalledProcessError as exc:
                    self.fail(f"main raised traceback-prone exception: {exc}")

        self.assertEqual(1, result)
        error_output = stderr.getvalue()
        self.assertIn("Version probe failed", error_output)
        self.assertIn("qpdf --version", error_output)
        self.assertIn("broken qpdf", error_output)
        self.assertNotIn("Traceback", error_output)


if __name__ == "__main__":
    unittest.main()
