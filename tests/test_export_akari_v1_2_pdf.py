import hashlib
import importlib.util
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts/export_akari_v1_2_pdf.py"


def load_exporter():
    spec = importlib.util.spec_from_file_location("export_akari_v1_2_pdf", EXPORTER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExportAkariV12PdfTests(unittest.TestCase):
    def setUp(self):
        self.exporter = load_exporter()

    def test_sha256_file_hashes_complete_binary(self):
        payload = (b"akari-v1.2.0" * 100_000) + b"final"
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "release.pdf"
            path.write_bytes(payload)

            self.assertEqual(
                hashlib.sha256(payload).hexdigest(),
                self.exporter.sha256_file(path),
            )

    def test_write_checksum_uses_gnu_sha256sum_format(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            release_dir = Path(temp_dir) / "release"
            pdf = release_dir / "akari-v1.2-core-settings.pdf"
            checksum = release_dir / "checksums.txt"
            release_dir.mkdir()
            pdf.write_bytes(b"pdf-payload")

            self.exporter.write_checksum(pdf, checksum)

            digest = hashlib.sha256(b"pdf-payload").hexdigest()
            self.assertEqual(
                f"{digest}  akari-v1.2-core-settings.pdf\n",
                checksum.read_text(encoding="utf-8"),
            )
            self.assertEqual(0o644, stat.S_IMODE(checksum.stat().st_mode))

    def test_main_renders_natural_form_before_writing_checksum(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            release_dir = Path(temp_dir) / "release"
            pdf = release_dir / "akari-v1.2-core-settings.pdf"
            checksum = release_dir / "checksums.txt"

            commands = []

            def render(command, cwd, check):
                commands.append(command)
                self.assertEqual(ROOT, cwd)
                self.assertTrue(check)
                if command[0] == "node":
                    release_dir.mkdir(parents=True, exist_ok=True)
                    pdf.write_bytes(b"rendered-pdf")
                elif command[0] == "qpdf":
                    shutil.copyfile(command[-2], command[-1])
                return subprocess.CompletedProcess(command, 0)

            with (
                mock.patch.object(self.exporter, "PDF", pdf),
                mock.patch.object(self.exporter, "CHECKSUM", checksum),
                mock.patch.object(self.exporter.subprocess, "run", side_effect=render),
            ):
                self.assertEqual(0, self.exporter.main())

            self.assertEqual(
                [
                    [
                        "node",
                        "tools/pdf/render.mjs",
                        "--document",
                        "natural-form",
                        "--pdf",
                    ],
                    [
                        "exiftool",
                        "-overwrite_original",
                        "-CreateDate=2026:07:15 00:00:00+09:00",
                        "-ModifyDate=2026:07:15 00:00:00+09:00",
                        str(pdf),
                    ],
                    [
                        "qpdf",
                        "--deterministic-id",
                        str(pdf),
                        str(release_dir / ".akari-v1.2-core-settings.normalized.pdf"),
                    ],
                ],
                commands,
            )

            digest = hashlib.sha256(b"rendered-pdf").hexdigest()
            self.assertEqual(
                f"{digest}  akari-v1.2-core-settings.pdf\n",
                checksum.read_text(encoding="utf-8"),
            )

    def test_render_failure_preserves_existing_checksum(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            release_dir = Path(temp_dir) / "release"
            release_dir.mkdir()
            pdf = release_dir / "akari-v1.2-core-settings.pdf"
            checksum = release_dir / "checksums.txt"
            checksum.write_text("previous-checksum\n", encoding="utf-8")

            with (
                mock.patch.object(self.exporter, "PDF", pdf),
                mock.patch.object(self.exporter, "CHECKSUM", checksum),
                mock.patch.object(
                    self.exporter.subprocess,
                    "run",
                    side_effect=subprocess.CalledProcessError(1, ["node"]),
                ),
                self.assertRaises(subprocess.CalledProcessError),
            ):
                self.exporter.main()

            self.assertEqual(
                "previous-checksum\n",
                checksum.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
