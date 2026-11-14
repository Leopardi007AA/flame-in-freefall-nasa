import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
from ui.theme import apply_theme
from ui.mock_data import get_mock_data, show_mock_banner

apply_theme()

st.title("Anteprima interfaccia")

df = get_mock_data()

tab_confronto, tab_dati, tab_lacune = st.tabs(["Confronto", "Dati reali", "Lacune"])

with tab_confronto:
    show_mock_banner()
    st.write("Scheda Confronto (da costruire)")
    st.dataframe(df)

with tab_dati:
    show_mock_banner()
    st.write("Scheda Dati reali (da costruire)")

with tab_lacune:
    show_mock_banner()
    st.write("Scheda Lacune (da costruire)")