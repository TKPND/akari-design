import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
AUDIT_TONARI_PDF = ROOT / "scripts/audit_tonari_no_akari_pdf.py"


def load_audit_tonari_pdf():
    spec = importlib.util.spec_from_file_location(
        "audit_tonari_no_akari_pdf", AUDIT_TONARI_PDF
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TonariNoAkariPdfAuditTest(unittest.TestCase):
    def setUp(self):
        self.audit_tonari_pdf = load_audit_tonari_pdf()

    def test_rendered_page_sort_key_orders_numeric_suffixes(self):
        pages = [
            Path("page-1.png"),
            Path("page-10.png"),
            Path("page-2.png"),
        ]

        sorted_pages = sorted(
            pages, key=self.audit_tonari_pdf.rendered_page_sort_key
        )

        self.assertEqual(
            [Path("page-1.png"), Path("page-2.png"), Path("page-10.png")],
            sorted_pages,
        )

    def test_searchable_text_normalization_removes_japanese_spacing(self):
        self.assertIn(
            "となりのあかり",
            self.audit_tonari_pdf.normalize_searchable_text("と な り の あ か り"),
        )
        self.assertIn(
            "目が合うだけで、今日が少し近くなる。",
            self.audit_tonari_pdf.normalize_searchable_text(
                "目が合うだけで、\n今日が少し近くなる。"
            ),
        )

    def test_load_required_text_from_manifest_includes_all_page_text(self):
        required_text = self.audit_tonari_pdf.load_required_text_from_manifest(
            ROOT / "source/manifests/tonari-no-akari/page-manifest.json"
        )

        self.assertEqual(48, len(required_text))
        self.assertNotIn("となりのあかり", required_text)
        self.assertIn("朝の合図", required_text)
        self.assertIn("帰り道の笑顔", required_text)
        self.assertIn("目が合うだけで、今日が少し近くなる。", required_text)
        self.assertIn("また明日、と言う前の表情を残しておく。", required_text)

    def test_pdfinfo_contract_accepts_24_page_a4_portrait_with_title(self):
        self.audit_tonari_pdf.require_pdfinfo_contract(
            """
Title:           となりのあかり
Pages:           24
Page size:       595.28 x 841.89 pts (A4)
"""
        )

    def test_pdfinfo_contract_rejects_wrong_title(self):
        with self.assertRaisesRegex(
            self.audit_tonari_pdf.AuditError,
            "title",
        ):
            self.audit_tonari_pdf.require_pdfinfo_contract(
                """
Title:           となりじゃない
Pages:           24
Page size:       595.28 x 841.89 pts (A4)
"""
            )

    def test_pdfinfo_contract_rejects_wrong_page_count(self):
        with self.assertRaisesRegex(
            self.audit_tonari_pdf.AuditError,
            "24 pages, got 23",
        ):
            self.audit_tonari_pdf.require_pdfinfo_contract(
                """
Title:           となりのあかり
Pages:           23
Page size:       595.28 x 841.89 pts (A4)
"""
            )

    def test_pdfinfo_contract_rejects_landscape_pages(self):
        with self.assertRaisesRegex(
            self.audit_tonari_pdf.AuditError,
            "A4 portrait",
        ):
            self.audit_tonari_pdf.require_pdfinfo_contract(
                """
Title:           となりのあかり
Pages:           24
Page size:       841.89 x 595.28 pts (A4)
"""
            )

    def test_expected_render_size_is_derived_from_pdf_points(self):
        self.assertEqual(
            (2381, 3368),
            self.audit_tonari_pdf.expected_render_size_from_points(
                595.28, 841.89, dpi=288
            ),
        )


if __name__ == "__main__":
    unittest.main()
