"""Test dei moduli puri (senza Streamlit ne' Gemini). Esegui dalla radice del progetto:
    python -m unittest discover -s tests -v
"""
import subprocess
import sys
import unittest
from pathlib import Path

import pandas as pd

from src import data_loader, scoring
from src.ai_engine import RateLimiter, fallback_answer, normalize_question
from src.ai_validation import AiReply, validate_reply

ROOT = Path(__file__).resolve().parent.parent
MARS = {"gravity": "mars", "o2": 30, "pressure": 10.2, "flow": 5}
ISS = {"gravity": "iss", "o2": 21, "pressure": 14.7, "flow": 10}


class TestLoader(unittest.TestCase):
    def test_real_csv_loads_ranks_and_is_not_mock(self):
        df = data_loader.load_investigations()
        self.assertFalse(data_loader.is_mock(df))
        self.assertGreaterEqual(len(df), 10)
        r = scoring.rank(df, {"gravity": "moon", "o2": 30.0, "pressure": 10.2, "flow": 5.0})
        self.assertEqual(len(r), len(df))
        self.assertFalse((df["o2_min"] == 0).any())

    def test_mock_fallback_and_flag(self):
        df = data_loader.load_investigations(data_loader.MOCK_PATH)
        self.assertEqual(len(df), 6)
        self.assertTrue(data_loader.is_mock(df))
        self.assertTrue(df["o2_min"].isna().any())          # celle vuote = NaN, mai 0
        self.assertFalse((df["o2_min"] == 0).any())

    def test_papers_missing_is_empty_list(self):
        if not (ROOT / "data" / "papers.json").exists():
            self.assertEqual(data_loader.load_papers(), [])


class TestValidateCsv(unittest.TestCase):
    def run_script(self, path):
        return subprocess.run([sys.executable, "scripts/validate_csv.py", str(path)],
                              cwd=ROOT, capture_output=True, text=True)

    def test_mock_passes(self):
        r = self.run_script("dev/investigations_mock.csv")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_bad_values_fail(self):
        df = pd.read_csv(ROOT / "dev" / "investigations_mock.csv")
        df.loc[0, "o2_min"] = 50          # min > max
        df.loc[1, "gravita"] = "marte"     # valore non ammesso
        df.loc[2, "id"] = "MOCK-1"         # id duplicato
        out = ROOT / "tests" / "_bad.csv"
        df.to_csv(out, index=False)
        try:
            r = self.run_script("tests/_bad.csv")
        finally:
            out.unlink()
        self.assertEqual(r.returncode, 1)
        self.assertIn("min > max", r.stdout)
        self.assertIn("non ammesso", r.stdout)
        self.assertIn("duplicati", r.stdout)


class TestScoring(unittest.TestCase):
    def setUp(self):
        self.df = data_loader.load_investigations(data_loader.MOCK_PATH)

    def test_range_and_order(self):
        r = scoring.rank(self.df, ISS)
        self.assertTrue(r["score"].between(0, 100).all())
        self.assertTrue(r["score"].is_monotonic_decreasing)

    def test_missing_data_gets_zero_points(self):
        r = scoring.rank(self.df, ISS).set_index("id")
        self.assertIn("nessun dato", " ".join(r.loc["MOCK-5", "why"]))

    def test_microgravity_matches_iss_better_than_earth_experiment(self):
        r = scoring.rank(self.df, ISS).set_index("id")
        self.assertGreater(r.loc["MOCK-1", "score"], r.loc["MOCK-6", "score"])

    def test_mars_prefers_microgravity_over_1g_for_same_conditions(self):
        row_micro = self.df[self.df["id"] == "MOCK-1"].iloc[0]
        row_1g = row_micro.copy()
        row_1g["gravita"] = "1g"
        self.assertGreater(scoring.score_row(row_micro, MARS)[0], scoring.score_row(row_1g, MARS)[0])


class TestAiValidation(unittest.TestCase):
    def setUp(self):
        self.df = data_loader.load_investigations(data_loader.MOCK_PATH)

    def test_valid_reply_passes(self):
        r = AiReply(answer="MOCK-1 copre O2 da 21 a 35.", citations=["MOCK-1"], highlight_ids=["MOCK-1"])
        reply, problems = validate_reply(r, self.df, MARS)
        self.assertEqual(problems, [])
        self.assertIsNotNone(reply)

    def test_invented_number_rejected(self):
        r = AiReply(answer="La propagazione e' 7,3 cm/s.", citations=["MOCK-1"])
        reply, problems = validate_reply(r, self.df, MARS)
        self.assertIsNone(reply)
        self.assertIn("7.3", " ".join(problems))

    def test_unknown_id_rejected(self):
        reply, problems = validate_reply(AiReply(answer="ok", citations=["ZZZ"]), self.df, MARS)
        self.assertIsNone(reply)

    def test_no_data_statement_passes(self):
        reply, _ = validate_reply(AiReply(answer="Nessun dato a 0,38 g."), self.df, MARS)
        self.assertIsNotNone(reply)

    def test_numbers_without_citations_rejected(self):
        reply, problems = validate_reply(AiReply(answer="Vale 30 percento."), self.df, MARS)
        self.assertIsNone(reply)

    def test_schema_bounds(self):
        with self.assertRaises(Exception):
            AiReply(answer="x", o2=200)


class TestFallbackAndLimiter(unittest.TestCase):
    def test_fallback_is_revalidated(self):
        df = data_loader.load_investigations(data_loader.MOCK_PATH)
        answers = {normalize_question("Che cosa copre MOCK-1?"):
                   {"answer": "MOCK-1 copre O2 da 21 a 35.", "citations": ["MOCK-1"]}}
        self.assertIsNotNone(fallback_answer("che cosa copre mock-1", df, MARS, answers))
        bad = {normalize_question("domanda"): {"answer": "Vale 99.", "citations": ["MOCK-1"]}}
        self.assertIsNone(fallback_answer("domanda", df, MARS, bad))
        self.assertIsNone(fallback_answer("sconosciuta", df, MARS, answers))

    def test_rate_limiter(self):
        rl = RateLimiter(max_calls=2, min_interval=3.0)
        self.assertTrue(rl.allow(now=0.0)[0])
        self.assertFalse(rl.allow(now=1.0)[0])      # troppo presto
        self.assertTrue(rl.allow(now=5.0)[0])
        self.assertFalse(rl.allow(now=20.0)[0])     # limite di sessione


if __name__ == "__main__":
    unittest.main()
