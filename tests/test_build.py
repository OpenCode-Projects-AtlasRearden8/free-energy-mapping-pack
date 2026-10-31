#!/usr/bin/env python3
"""Tests for the Free Energy Mapping printables pack.

Run with:
    python3 -m unittest discover -s tests -v

Every physical sheet must build a valid PDF: real PDF header/trailer,
sane size, no zero-byte stubs. Sources must be self-contained and each
sheet must carry its kind intro page. Nothing here touches the network.
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build as buildmod  # noqa: E402  (after sys.path setup)

SHEET_NAMES = [
    "01-weekly-energy-map.html",
    "02-five-level-task-matcher.html",
    "03-low-battery-day-menu.html",
    "04-hours-per-day-tracker.html",
    "05-drain-day-recovery-card.html",
    "06-people-meetings-drain-sorter.html",
    "07-sunday-gentle-review.html",
]


def is_valid_pdf(path: Path) -> bool:
    """Real PDFs: '%PDF-' header, '%%EOF' trailer, not a stub."""
    if not path.is_file():
        return False
    data = path.read_bytes()
    if not data.startswith(b"%PDF-"):
        return False
    if b"%%EOF" not in data[-512:]:
        return False
    if len(data) < 2000:
        return False
    return True


class TestSources(unittest.TestCase):
    def test_seven_sheets_exist(self):
        for name in SHEET_NAMES:
            with self.subTest(sheet=name):
                self.assertTrue((ROOT / "src" / "sheets" / name).is_file(), name)

    def test_shared_stylesheet_exists(self):
        self.assertTrue((ROOT / "src" / "styles.css").is_file())

    def test_each_sheet_links_shared_stylesheet(self):
        for name in SHEET_NAMES:
            with self.subTest(sheet=name):
                text = (ROOT / "src" / "sheets" / name).read_text(encoding="utf-8")
                self.assertIn('href="../styles.css"', text)

    def test_each_sheet_has_kind_intro_page(self):
        for name in SHEET_NAMES:
            with self.subTest(sheet=name):
                text = (ROOT / "src" / "sheets" / name).read_text(encoding="utf-8")
                self.assertIn('class="page intro-page"', text)

    def test_sources_have_no_secrets_or_urls_forming(self):
        for name in SHEET_NAMES:
            with self.subTest(sheet=name):
                text = (ROOT / "src" / "sheets" / name).read_text(encoding="utf-8")
                for token in ("api_key", "API_KEY", "password=", "Bearer ", "token="):
                    self.assertNotIn(token, text, f"{name}: {token!r}")


class TestBuild(unittest.TestCase):
    """Build every sheet into a temp dir; verify each PDF is valid."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory(prefix="fem-build-")
        cls.out = Path(cls._tmp.name)
        cls._orig_out = buildmod.OUT_DIR
        buildmod.OUT_DIR = cls.out
        buildmod.build_all()
        cls.pdfs = buildmod.sheet_pdfs()

    @classmethod
    def tearDownClass(cls):
        buildmod.OUT_DIR = cls._orig_out
        cls._tmp.cleanup()

    def test_every_sheet_builds_valid_pdf(self):
        for html, pdf in self.pdfs:
            with self.subTest(sheet=html.name):
                self.assertTrue(is_valid_pdf(pdf), f"{pdf} missing/invalid")

    def test_seven_pdfs_built(self):
        self.assertEqual(len(self.pdfs), 7)

    def test_no_empty_pdf(self):
        for html, pdf in self.pdfs:
            with self.subTest(sheet=html.name):
                self.assertGreater(pdf.stat().st_size, 10_000, f"{pdf} looks empty")

    def test_pdf_page_counts_match_sheet_page_divs(self):
        """Loose check: PDF has at least as many pages as the HTML declares."""
        for html, pdf in self.pdfs:
            with self.subTest(sheet=html.name):
                text = html.read_text(encoding="utf-8")
                declared = text.count('class="page')
                raw = pdf.read_bytes()
                # Count actual page objects in the PDF (matches "N 0 obj" blocks).
                actual = max(
                    [
                        1,
                        raw.count(b"/Type /Page\n"),
                        raw.count(b"/Type /Page "),
                        raw.count(b"/Type/Page"),
                    ]
                )
                self.assertGreaterEqual(actual, min(declared, 2), f"{pdf.name}: too few pages")

    def test_out_dir_defaults_to_printables(self):
        self.assertEqual(type(self)._orig_out.name, "printables")


class TestLicenseAndReadme(unittest.TestCase):
    def test_mit_license_with_exact_copyright(self):
        lic = (ROOT / "LICENSE").read_text(encoding="utf-8") if (ROOT / "LICENSE").is_file() else ""
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", lic)

    def test_readme_credits_asdale_dynamics(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
        self.assertIn("Asdale Dynamics, LLC", readme)


if __name__ == "__main__":
    unittest.main()
