"""Browser regression tests for Bagian 3 (pill options) on phone and desktop widths.

Run against a LOCAL dev server only (never the deployed app):
    .venv\\Scripts\\python.exe -m unittest discover -s tests -v

The tests only toggle unsaved pill selections; a submission is performed once in a
controlled case and the dev-only CSV artifact is removed afterwards.
"""

import ast
import os
import unittest
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

APP_URL = os.environ.get("TEST_APP_URL", "http://127.0.0.1:8501")
REPO = Path(__file__).resolve().parent.parent
DATA_FILE = REPO / "data_kuesioner_fgd.csv"

CATEGORIES = {
    "Hambatan Utama Instansi": "HAMBATAN_OPTIONS",
    "Bentuk Komitmen Dukungan Riil": "DUKUNGAN_OPTIONS",
    "Prioritas Utama Program": "PRIORITAS_OPTIONS",
}

CHOICES = {
    node.targets[0].id: ast.literal_eval(node.value)
    for node in ast.parse(
        (REPO / "fgd-interactive-instrument-v3.py").read_text(encoding="utf-8")
    ).body
    if isinstance(node, ast.Assign)
    and isinstance(node.targets[0], ast.Name)
    and node.targets[0].id in CATEGORIES.values()
}

# Check real text geometry, not just the presence of a wrapping CSS declaration.
TEXT_BOUNDS = """element => {
    const box = element.getBoundingClientRect();
    const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
    const failures = [];
    let node;
    while (node = walker.nextNode()) {
        if (!node.textContent.trim()) continue;
        const parent = node.parentElement;
        const css = getComputedStyle(parent);
        if (css.display === 'none' || css.visibility === 'hidden') continue;
        const range = document.createRange();
        range.selectNodeContents(node);
        const outside = [...range.getClientRects()].some(r =>
            r.left < box.left - 1 || r.right > box.right + 1 ||
            r.top < box.top - 1 || r.bottom > box.bottom + 1);
        const clipped = parent.clientWidth > 0 &&
            parent.scrollWidth > parent.clientWidth + 1 &&
            css.overflowX === 'hidden';
        if (outside || clipped) failures.push({
            text: node.textContent, tag: parent.tagName,
            whiteSpace: css.whiteSpace, overflow: css.overflow,
            textOverflow: css.textOverflow,
            width: parent.clientWidth, scrollWidth: parent.scrollWidth,
            outside, clipped
        });
    }
    return failures;
}"""


class Bagian3PillsMobileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if urlparse(APP_URL).hostname not in {"localhost", "127.0.0.1"}:
            raise RuntimeError("Browser tests must target a local server.")
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(
            channel=os.environ.get("TEST_BROWSER_CHANNEL", "msedge"), headless=True
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        if DATA_FILE.exists():
            DATA_FILE.unlink()

    def open_form(self, width):
        page = self.browser.new_page(viewport={"width": width, "height": 900})
        page.set_default_timeout(10000)
        page.goto(APP_URL)
        page.locator('[data-testid="stSidebar"] label').filter(
            has_text="Input Kuesioner OPD"
        ).click()
        page.get_by_text("Bagian 3: Pilihan Terpandu", exact=False).wait_for()
        collapse = page.get_by_test_id("stSidebarCollapseButton").locator("button")
        if collapse.count() and collapse.is_visible():
            collapse.click()
        return page

    def assert_text_fits(self, element):
        errors = element.evaluate(TEXT_BOUNDS)
        self.assertFalse(errors, str(errors) + "\n" + element.evaluate("e => e.outerHTML"))

    def test_every_pill_option_wraps_inside_viewport(self):
        for width in (320, 375, 430, 1280):
            with self.subTest(width=width):
                page = self.open_form(width)
                try:
                    for cat_index, source in enumerate(CATEGORIES.values()):
                        for option in CHOICES[source]:
                            matches = page.get_by_role("button", name=option)
                            # "Lainnya (Tulis pada Catatan Bebas)" exists in every
                            # category; DOM order equals category order.
                            pill = matches.nth(cat_index) if matches.count() > 1 else matches.first
                            pill.scroll_into_view_if_needed()
                            self.assert_text_fits(pill)
                            box = pill.bounding_box()
                            self.assertLessEqual(box["x"] + box["width"], width)
                    main = page.get_by_test_id("stMain")
                    self.assertTrue(main.evaluate("e => e.scrollWidth <= e.clientWidth + 1"))
                finally:
                    page.close()

    def test_fourth_pick_is_dropped_live_and_submission_saves(self):
        page = self.open_form(375)
        try:
            choices = CHOICES["HAMBATAN_OPTIONS"]
            for option in choices[:3]:
                page.get_by_role("button", name=option).click()
            page.get_by_role("button", name=choices[3]).click()
            page.get_by_text("otomatis dilepas", exact=False).wait_for()
            for option in choices[:3]:
                self.assertEqual(
                    page.get_by_role("button", name=option).get_attribute("aria-pressed"),
                    "true",
                )
            self.assertNotEqual(
                page.get_by_role("button", name=choices[3]).get_attribute("aria-pressed"),
                "true",
            )
            page.get_by_label("Nama Lengkap Responden *").fill("Uji Coba")
            page.get_by_label("Jabatan Responden *").fill("Penguji")
            page.get_by_role("button", name="Kirim Jawaban Kuesioner OPD").click()
            page.get_by_text("Terima kasih", exact=False).wait_for()
            rows = DATA_FILE.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(rows), 2)
            self.assertIn(choices[0], rows[1])
            self.assertNotIn(choices[3], rows[1])
        finally:
            page.close()


if __name__ == "__main__":
    unittest.main()
