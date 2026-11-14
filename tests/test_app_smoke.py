"""Test di fumo: app.py si importa ed esegue fino in fondo con Streamlit finto,
e il flusso di una domanda all'AI (con risposta simulata) applica l'azione alla dashboard."""
import runpy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fake_streamlit  # noqa: E402
from src.ai_validation import AiReply  # noqa: E402
from ui import flame_lab  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class TestSmoke(unittest.TestCase):
    def test_app_runs_with_defaults(self):
        st = fake_streamlit.install()
        runpy.run_path(str(ROOT / "app.py"))
        self.assertEqual(st.session_state["gravity"], "mars")
        st.set_page_config.assert_called_once()

    def test_question_sets_pending_action(self):
        st = fake_streamlit.install(chat_question="Mostrami la Luna")
        fake_reply = AiReply(gravity="moon", o2=26.5, answer="Nessun dato a 0,16 g.")
        with patch("src.ai_engine.answer_question",
                   return_value={"source": "ai", "reply": fake_reply, "problems": []}):
            with self.assertRaises(SystemExit):          # st.rerun() finto
                runpy.run_path(str(ROOT / "app.py"))
        self.assertEqual(st.session_state["pending_action"]["gravity"], "moon")
        self.assertEqual(st.session_state["chat"][-1]["role"], "assistant")

    def test_pending_action_is_applied_on_next_run(self):
        st = fake_streamlit.install()
        st.session_state["pending_action"] = {"gravity": "moon", "o2": 26.5, "pressure": None,
                                              "flow": None, "highlight_ids": ["MOCK-1"]}
        runpy.run_path(str(ROOT / "app.py"))
        self.assertEqual(st.session_state["gravity"], "moon")
        self.assertEqual(st.session_state["o2"], 26.5)
        self.assertEqual(st.session_state["pressure"], 10.2)      # invariato
        self.assertEqual(st.session_state["highlight_ids"], ["MOCK-1"])
        self.assertNotIn("pending_action", st.session_state)


class TestFlameLab(unittest.TestCase):
    def test_all_gravities_build(self):
        for g in flame_lab.GRAVITY:
            html = flame_lab.build_html(g, 30, 10.2, 5)
            self.assertIn("Resa illustrativa", html)
            self.assertNotIn("__", html)                  # nessun segnaposto rimasto

    def test_more_oxygen_means_bigger_flame(self):
        low = flame_lab.flame_params("mars", 21, 0)
        high = flame_lab.flame_params("mars", 60, 0)
        self.assertGreater(high["h"], low["h"])

    def test_flow_leans_flame(self):
        self.assertGreater(flame_lab.flame_params("iss", 21, 20)["lean_deg"],
                           flame_lab.flame_params("iss", 21, 0)["lean_deg"])

    def test_unknown_gravity(self):
        with self.assertRaises(ValueError):
            flame_lab.build_html("venere", 21, 14.7, 0)


if __name__ == "__main__":
    unittest.main()
