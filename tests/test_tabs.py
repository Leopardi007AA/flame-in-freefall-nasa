"""Test delle schede Confronto e Lacune (funzioni pure) e dell'esploratore Dati reali."""
import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.data_loader import load_investigations  # noqa: E402
from ui.tabs import compare, gaps, real_data  # noqa: E402

NAN = float("nan")


def make_df():
    base = dict(nome="x", gravita="microgravita", o2_min=NAN, o2_max=NAN, url_psi="https://x",
                pressione_min_psia=NAN, pressione_max_psia=NAN, flusso_min_cm_s=NAN, flusso_max_cm_s=NAN,
                stato_combustibile=None, combustibili=None, sensori=None, area_sicurezza=None, dati_grezzi=None)
    rows = [dict(base, id="A", o2_min=14, o2_max=21),
            dict(base, id="B", gravita="1g", o2_min=21, o2_max=40),
            dict(base, id="C"),                                   # senza ossigeno
            dict(base, id="D", gravita="mista", o2_min=21, o2_max=21)]
    return pd.DataFrame(rows)


class TestGaps(unittest.TestCase):
    def test_coverage(self):
        cov = gaps.coverage(make_df())
        self.assertEqual(cov["cells"][("0g", 21)], ["A"])
        self.assertEqual(sorted(cov["cells"][("1g", 21)] + cov["cells"][("1g", 30)]), ["B", "B"])
        self.assertEqual(cov["excluded_o2"], ["C"])
        self.assertEqual(cov["excluded_gravity"], ["D"])

    def test_mars_and_moon_stay_empty(self):
        cells = gaps.coverage(make_df())["cells"]
        self.assertFalse(any(v for (k, _), v in cells.items() if k in ("mars", "moon")))

    def test_scenario_cell(self):
        self.assertEqual(gaps.scenario_cell({"gravity": "moon", "o2": 27}), ("moon", 26.5))

    def test_real_csv_grid_builds(self):
        df = load_investigations()
        html = gaps.grid_html(gaps.coverage(df), {}, {"gravity": "mars", "o2": 30}, [])
        self.assertIn("nessun dato", html)


class TestCompare(unittest.TestCase):
    def test_missing_is_dash_not_zero(self):
        sel = make_df().iloc[[2]]
        html = compare.table_html(sel)
        self.assertIn("NESSUN DATO", html)
        self.assertNotIn(" 0 ", html)

    def test_fmt_range(self):
        self.assertIsNone(compare.fmt_range(NAN, NAN))
        self.assertEqual(compare.fmt_range(14, 21), "14–21")
        self.assertEqual(compare.fmt_range(20, 20), "20")
        self.assertEqual(compare.fmt_range(NAN, 40), "≤ 40")

    def test_rows_that_differ(self):
        rows = compare.build_rows(make_df().iloc[[0, 1]])
        o2 = next(r for r in rows if r[0] == "Ossigeno")
        self.assertTrue(o2[3])

    def test_o2_figure_none_without_data(self):
        self.assertIsNone(compare.o2_figure(make_df().iloc[[2]], 30))


class TestRealData(unittest.TestCase):
    def test_sample_files_are_never_shown(self):
        names = real_data.discover_tables().keys()
        self.assertFalse(any("sample" in n.lower() for n in names))


if __name__ == "__main__":
    unittest.main()
