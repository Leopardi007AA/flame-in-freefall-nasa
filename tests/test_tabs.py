"""Test delle schede Confronto e Lacune (funzioni pure) e dell'esploratore Dati reali."""
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.data_loader import load_investigations  # noqa: E402
from ui import mock_data  # noqa: E402
from ui.tabs import compare, gaps, real_data  # noqa: E402

NAN = float("nan")


def make_df():
    base = dict(nome="x", gravita="microgravita", o2_min=NAN, o2_max=NAN, url_psi="https://x",
                pressione_min_psia=NAN, pressione_max_psia=NAN, flusso_min_cm_s=NAN, flusso_max_cm_s=NAN,
                stato_combustibile=None, combustibili=None, sensori=None, area_sicurezza=None, dati_grezzi=None)
    rows = [dict(base, id="A", nome="A", o2_min=14, o2_max=21),
            dict(base, id="B", nome="B", gravita="1g", o2_min=21, o2_max=40),
            dict(base, id="C", nome="C"),                                   # senza ossigeno
            dict(base, id="D", nome="D", gravita="mista", o2_min=21, o2_max=21)]
    return pd.DataFrame(rows)


class TestGaps(unittest.TestCase):
    def test_coverage(self):
        cov = gaps.coverage(make_df())
        self.assertEqual(cov["celle"][("microgravita", 21)], ["A"])
        self.assertEqual(cov["celle"][("1g", 30)], ["B"])
        self.assertEqual(cov["senza_ossigeno"], 1)    # C
        self.assertEqual(cov["senza_colonna"], 1)     # D: gravita "mista"

    def test_mars_and_moon_stay_empty(self):
        celle = gaps.coverage(make_df())["celle"]
        for (colonna, _), nomi in celle.items():
            if colonna in ("marte", "luna"):
                self.assertEqual(nomi, [])

    def test_scenario_column_uses_app_keys(self):
        # app.py passa {"gravity": "mars"|"moon"|"earth"|"iss", "o2": ...}
        self.assertEqual(gaps.colonna_scenario({"gravity": "mars", "o2": 30}), "marte")
        self.assertEqual(gaps.colonna_scenario({"gravity": "moon", "o2": 27}), "luna")
        self.assertEqual(gaps.colonna_scenario({"gravity": "earth", "o2": 21}), "1g")
        self.assertEqual(gaps.colonna_scenario({"gravity": "iss", "o2": 21}), "microgravita")
        self.assertEqual(gaps.ossigeno_scenario({"gravity": "moon", "o2": 27}), 27.0)

    def test_real_csv_coverage_builds(self):
        cov = gaps.coverage(load_investigations())
        self.assertEqual(len(cov["celle"]), 20)       # 4 gravita' x 5 ossigeni

    def test_zero_is_data_not_missing(self):
        self.assertFalse(gaps.manca(0))
        self.assertTrue(gaps.manca(NAN))
        self.assertTrue(gaps.manca("  "))


class TestCompare(unittest.TestCase):
    def test_intervallo(self):
        self.assertIsNone(compare.intervallo(NAN, NAN, "%"))
        self.assertEqual(compare.intervallo(14, 21, "%"), "14–21 %")
        self.assertEqual(compare.intervallo(20, 20, "cm/s"), "20 cm/s")
        self.assertEqual(compare.intervallo(NAN, 40, "cm/s"), "max 40 cm/s")
        self.assertEqual(compare.intervallo(21, NAN, "%"), "min 21 %")
        self.assertEqual(compare.intervallo(26.5, 30, "%"), "26.5–30 %")

    def test_missing_is_none_never_zero(self):
        riga = make_df().iloc[2]
        for etichetta, valore in compare.attributi(riga).items():
            self.assertIsNone(valore, etichetta)
        self.assertEqual(compare.cella(None), compare.NESSUN_DATO)

    def test_zero_is_a_real_value(self):
        self.assertEqual(compare.intervallo(0, 0, "cm/s"), "0 cm/s")

    def test_list_columns_are_readable(self):
        self.assertEqual(compare.testo("PMMA|cotone", elenco=True), "PMMA, cotone")
        self.assertEqual(compare.numero(26.0), "26")


class TestRealData(unittest.TestCase):
    def test_sample_files_are_never_shown(self):
        names = real_data.discover_tables().keys()
        self.assertFalse(any("sample" in n.lower() for n in names))

    def test_discover_skips_samples_and_reads_real_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "BASS-II"
            d.mkdir()
            (d / "bass_ii_sample_data.csv").write_text("a,b\n1,2\n")
            (d / "bass_ii_real.csv").write_text("a,b\n1,2\n3,4\n")
            tabelle = real_data.discover_tables(Path(tmp))
            self.assertEqual(list(tabelle), ["BASS-II / bass_ii_real.csv"])
            self.assertIn("bass_ii_real.csv", tabelle["BASS-II / bass_ii_real.csv"].attrs["file"])


class TestMockBanner(unittest.TestCase):
    def test_banner_is_off_for_the_real_dashboard(self):
        # i dati veri non devono mai essere etichettati "DATI DI PROVA"
        self.assertFalse(mock_data.IS_MOCK)

    def test_mock_rows_start_with_MOCK(self):
        df = mock_data.get_mock_data()
        self.assertTrue(df["nome"].str.startswith("MOCK").all())
        self.assertEqual(list(df.columns), mock_data.COLONNE)


if __name__ == "__main__":
    unittest.main()
