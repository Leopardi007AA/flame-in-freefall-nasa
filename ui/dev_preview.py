import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
import plotly.graph_objects as go
from ui.theme import apply_theme

apply_theme()

st.title("Anteprima interfaccia")

st.markdown(
    '<div class="glass"><h3>Card di vetro</h3><p>Testo di prova dentro la card.</p></div>',
    unsafe_allow_html=True,
)

tab_confronto, tab_dati, tab_lacune = st.tabs(["Confronto", "Dati reali", "Lacune"])

with tab_confronto:
    st.write("Scheda Confronto (vuota)")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=["A", "B", "C"], y=[3, 7, 5]))
    fig.update_layout(title="Grafico di prova")
    st.plotly_chart(fig, config={"displayModeBar": False})

with tab_dati:
    st.write("Scheda Dati reali (vuota)")

with tab_lacune:
    st.write("Scheda Lacune (vuota)")