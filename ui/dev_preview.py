import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
import plotly.graph_objects as go
from ui.theme import apply_theme
from ui.components import glass_card, stat_tile, badge

apply_theme()

st.title("Anteprima interfaccia")

# --- Passo 4: prova dei componenti ---
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

# --- Schede e grafico del Passo 1 ---
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