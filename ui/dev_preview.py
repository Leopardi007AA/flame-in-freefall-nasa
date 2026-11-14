"""ui/dev_preview.py - pagina di prova per lavorare alle schede con dati finti.
Uso: streamlit run ui/dev_preview.py
Qui i dati sono SEMPRE finti (MOCK): il banner e' ben visibile. L'app vera usa i dati di data/."""
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st  # noqa: E402

from ui.mock_data import get_mock_data, show_mock_banner  # noqa: E402
from ui.tabs import compare, gaps, real_data  # noqa: E402
from ui.theme import apply_theme  # noqa: E402

st.set_page_config(page_title="Anteprima interfaccia", layout="wide")
apply_theme()
st.title("Anteprima interfaccia")

df = get_mock_data()
scenario = {
    "gravity": st.selectbox("Gravità", ["earth", "mars", "moon", "iss"], index=1),
    "o2": st.slider("Ossigeno %", 21.0, 85.0, 30.0, step=0.5),
    "pressure": 10.2,
    "flow": 5.0,
}

tab_confronto, tab_lacune, tab_dati = st.tabs(["Confronto", "Lacune", "Dati reali"])
with tab_confronto:
    show_mock_banner()
    compare.render(df, scenario, [])
with tab_lacune:
    show_mock_banner()
    gaps.render(df, scenario, [])
with tab_dati:
    show_mock_banner()
    real_data.render({})
