"""Streamlit finto per il test di fumo: permette di eseguire app.py senza installare Streamlit.
Controlla solo errori di battitura e di importazione, NON l'aspetto ne' il comportamento reale."""
import sys
from types import ModuleType
from unittest.mock import MagicMock


class FakeState(dict):
    def pop(self, key, default=None):
        return super().pop(key, default)


def install(chat_question=None):
    st = MagicMock(name="streamlit")
    st.session_state = FakeState()
    st.secrets = {}
    st.cache_data = lambda f=None, **k: f if f else (lambda g: g)
    st.columns = lambda spec, **k: [MagicMock() for _ in range(spec if isinstance(spec, int) else len(spec))]
    st.tabs = lambda labels: [MagicMock() for _ in labels]
    st.text_input = lambda *a, **k: ""
    st.chat_input = lambda *a, **k: chat_question
    st.rerun = MagicMock(side_effect=SystemExit("rerun"))
    st.column_config = MagicMock()
    # i moduli di C importano streamlit all'avvio: li si scarta, cosi' si reimportano col Streamlit finto
    for name in [k for k in sys.modules if k in ("ui.theme", "ui.components") or k.startswith("ui.tabs")]:
        del sys.modules[name]
    sys.modules["streamlit"] = st
    comp = ModuleType("streamlit.components")
    v1 = ModuleType("streamlit.components.v1")
    v1.html = MagicMock()
    comp.v1 = v1
    sys.modules["streamlit.components"] = comp
    sys.modules["streamlit.components.v1"] = v1
    st.components = comp
    return st
