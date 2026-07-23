import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def load_script_module(name):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


audit_pdf = load_script_module("audit_pdf")
audit_alpha_edges = load_script_module("audit_alpha_edges")


class PdfContractTest(unittest.TestCase):
    def test_pdf_audit_levels_select_expected_owners(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf = Path(temp_dir) / "document.pdf"
            pdf.write_bytes(b"pdf")

            expected_calls = {
                "structure": (1, 0),
                "raster": (0, 1),
                "full": (1, 1),
            }
            for level, (structure_calls, raster_calls) in expected_calls.items():
                with self.subTest(level=level), mock.patch.object(
                    audit_pdf, "audit_pdf_structure"
                ) as structure, mock.patch.object(
                    audit_pdf, "audit_pdf_raster"
                ) as raster:
                    audit_pdf.audit_pdf(pdf, level=level)
                    self.assertEqual(structure_calls, structure.call_count)
                    self.assertEqual(raster_calls, raster.call_count)

    def test_pdf_audit_rejects_unknown_level(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf = Path(temp_dir) / "document.pdf"
            pdf.write_bytes(b"pdf")
            with self.assertRaisesRegex(audit_pdf.AuditError, "audit level"):
                audit_pdf.audit_pdf(pdf, level="quick")

    def test_pdfinfo_contract_accepts_expected_page_count_and_ratio(self):
        audit_pdf.require_pdfinfo_contract(
            "Pages:           14\nPage size:       960 x 540 pts\n"
        )

    def test_pdfinfo_contract_rejects_non_16_by_9_page(self):
        pdfinfo = "Pages:           14\nPage size:       595 x 842 pts\n"
        with self.assertRaisesRegex(audit_pdf.AuditError, "16:9"):
            audit_pdf.require_pdfinfo_contract(pdfinfo)

    def test_searchable_text_contract_requires_every_release_term(self):
        complete = "\n".join(audit_pdf.REQUIRED_TEXT)
        audit_pdf.require_searchable_text(complete)

        missing = complete.replace("Bag Detail Board", "")
        with self.assertRaisesRegex(audit_pdf.AuditError, "Bag Detail Board"):
            audit_pdf.require_searchable_text(missing)

    def test_pdfinfo_contract_rejects_wrong_page_count(self):
        pdfinfo = "Pages:           12\nPage size:       960 x 540 pts\n"
        with self.assertRaises(audit_pdf.AuditError):
            audit_pdf.require_pdfinfo_contract(pdfinfo)

    def test_font_table_requires_embedded_unicode_fonts(self):
        pdffonts = "\n".join(
            [
                "name type encoding emb sub uni object ID",
                "----------------------------------------",
                "Inter Type 3 Custom no yes yes 4 0",
            ]
        )
        with self.assertRaises(audit_pdf.AuditError):
            audit_pdf.require_font_table(pdffonts)

    def test_rendered_page_content_rejects_blank_png(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            blank = Path(temp_dir) / "blank.png"
            Image.new("RGB", (96, 54), (247, 247, 242)).save(blank)
            with self.assertRaises(audit_pdf.AuditError):
                audit_pdf.require_rendered_page_content([blank])

    def test_alpha_edge_audit_detects_transparency(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            transparent = Path(temp_dir) / "transparent.png"
            Image.new("RGBA", (4, 4), (255, 255, 255, 0)).save(transparent)
            self.assertTrue(audit_alpha_edges.has_transparency(transparent))


if __name__ == "__main__":
    unittest.main()
