import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
from ui.theme import apply_theme
from ui.mock_data import get_mock_data, get_mock_tables
from ui.tabs import compare, gaps, real_data

apply_theme()

st.title("Anteprima interfaccia")

df = get_mock_data()
scenario = {"gravita": "microgravita", "o2": 21}
highlight_ids = ["MOCK-1", "MOCK-2", "MOCK-4"]

tab_confronto, tab_dati, tab_lacune = st.tabs(["Confronto", "Dati reali", "Lacune"])

with tab_confronto:
    compare.render(df, scenario, highlight_ids)

with tab_dati:
    real_data.render(get_mock_tables())

with tab_lacune:
    gaps.render(df, scenario, highlight_ids)