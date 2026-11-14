import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
import plotly.graph_objects as go
from ui.theme import apply_theme
from ui.components import glass_card, stat_tile, badge
from ui.plotly_theme import style_fig

apply_theme()

st.title("Anteprima interfaccia")

st.subheader("Etichette di provenienza")
st.markdown(
    badge("REALE", "real") + " &nbsp; "
    + badge("MODELLO", "model") + " &nbsp; "
    + badge("ILLUSTRATIVO", "illustrative") + " &nbsp; "
    + badge("NESSUN DATO", "nodata"),
    unsafe_allow_html=True,
)

st.subheader("Tile")
c1, c2, c3, c4 = st.columns(4)
with c1:
    stat_tile("Ossigeno", "21%", badge("REALE", "real"), tone="cool")
with c2:
    stat_tile("Punteggio", "78", badge("MODELLO", "model"), tone="warm")
with c3:
    stat_tile("Flusso", "—", badge("NESSUN DATO", "nodata"))
with c4:
    stat_tile("Rischio", "Alto", badge("ILLUSTRATIVO", "illustrative"), tone="alert")

st.subheader("Card")
glass_card(
    "Card di prova",
    "Testo dentro la card. Valore: 21% " + badge("REALE", "real"),
    accent="#ff8a4c",
)

tab_confronto, tab_dati, tab_lacune = st.tabs(["Confronto", "Dati reali", "Lacune"])

with tab_confronto:
    st.write("Scheda Confronto (vuota)")

    fig = go.Figure()
    fig.add_trace(go.Bar(x=["A", "B", "C"], y=[3, 7, 5], name="Serie 1"))
    fig.add_trace(go.Bar(x=["A", "B", "C"], y=[4, 2, 6], name="Serie 2"))
    fig.update_layout(title="Grafico di prova")
    style_fig(fig)
    st.plotly_chart(fig, config={"displayModeBar": False})

with tab_dati:
    st.write("Scheda Dati reali (vuota)")

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[3, 5, 4, 7], mode="markers", name="Punti"))
    fig3.update_layout(title="Dispersione di prova")
    style_fig(fig3)
    st.plotly_chart(fig3, config={"displayModeBar": False})

with tab_lacune:
    st.write("Scheda Lacune (vuota)")

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(y=["Esp. 1", "Esp. 2"], x=[21, 30], orientation="h", name="O2 max"))
    fig2.update_layout(title="Barre orizzontali di prova")
    style_fig(fig2, height=240)
    st.plotly_chart(fig2, config={"displayModeBar": False})