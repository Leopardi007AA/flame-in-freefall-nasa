import html

import pandas as pd
import plotly.express as px
import streamlit as st

from ui.components import badge
from ui.mock_data import IS_MOCK, show_mock_banner
from ui.plotly_theme import style_fig

NESSUNO = "(nessuno)"


def render(tables: dict) -> None:
    show_mock_banner()

    if not tables:
        st.write("Nessuna tabella disponibile.")
        return

    # 1) Scelta della tabella + badge + file di origine
    nome = st.selectbox("Tabella", list(tables.keys()))
    df = tables[nome]
    origine = html.escape(str(df.attrs.get("file", nome)))
    etichetta = badge("ILLUSTRATIVO", "illustrative") if IS_MOCK else badge("REALE", "real")
    st.markdown(f"{etichetta} &nbsp; File di origine: <code>{origine}</code>", unsafe_allow_html=True)

    # Quali colonne hanno almeno un dato?
    con_dati = [c for c in df.columns if df[c].notna().any()]
    senza_dati = [c for c in df.columns if c not in con_dati]
    numeriche = [c for c in con_dati if pd.api.types.is_numeric_dtype(df[c])]

    # 6) Le colonne vuote si dichiarano, non si nascondono
    if senza_dati:
        elenco = html.escape(", ".join(str(c) for c in senza_dati))
        st.markdown(
            f"Non disponibile in questa tabella: {elenco} " + badge("NESSUN DATO", "nodata"),
            unsafe_allow_html=True,
        )

    if not con_dati:
        return

    # 2) Menu per il grafico
    base = numeriche if numeriche else con_dati
    y_iniziale = base[1] if len(base) > 1 else base[0]
    c1, c2, c3 = st.columns(3)
    with c1:
        x = st.selectbox("Asse x", con_dati, index=con_dati.index(base[0]))
    with c2:
        y = st.selectbox("Asse y", con_dati, index=con_dati.index(y_iniziale))
    with c3:
        colore = st.selectbox("Colore", [NESSUNO] + con_dati)

    # 3) Filtri: scegli le colonne da filtrare
    filtrate = df
    scelte = st.multiselect("Filtra per colonne", con_dati)
    for c in scelte:
        if c in numeriche:
            minimo, massimo = float(df[c].min()), float(df[c].max())
            if minimo == massimo:
                st.write(f"{c}: valore unico ({minimo:g}), nessun filtro possibile")
                continue
            da, a = st.slider(str(c), minimo, massimo, (minimo, massimo))
            filtrate = filtrate[filtrate[c].between(da, a)]
        else:
            valori = sorted(df[c].dropna().astype(str).unique())
            scelti = st.multiselect(str(c), valori)
            if scelti:
                filtrate = filtrate[filtrate[c].astype(str).isin(scelti)]

    st.markdown(
        f'<span class="mono-label">{len(filtrate)} righe su {len(df)}. '
        "Le righe senza valore in una colonna filtrata vengono escluse.</span>",
        unsafe_allow_html=True,
    )

    # Grafico a dispersione
    dati = filtrate.dropna(subset=list({x, y}))
    senza_xy = len(filtrate) - len(dati)
    if dati.empty:
        st.write("Nessuna riga con valori per l'asse x e l'asse y.")
    else:
        fig = px.scatter(dati, x=x, y=y, color=None if colore == NESSUNO else colore)
        fig.update_traces(marker=dict(size=9))
        style_fig(fig, height=400)
        st.plotly_chart(fig, config={"displayModeBar": False})
    if senza_xy:
        st.markdown(
            f'<span class="mono-label">Righe senza valore per x o y (non nel grafico): {senza_xy}</span>',
            unsafe_allow_html=True,
        )

    # 4) Tabella filtrata e download
    st.dataframe(filtrate)
    st.download_button(
        "Scarica CSV filtrato",
        filtrate.to_csv(index=False).encode("utf-8"),
        file_name=f"{nome}_filtrato.csv".replace(" ", "_"),
        mime="text/csv",
    )

    # 5) Ispettore del record
    if filtrate.empty:
        return
    indice = st.selectbox("Ispeziona una riga", list(filtrate.index), format_func=lambda i: f"Riga {i}")
    riga = filtrate.loc[indice]
    valori_riga = pd.DataFrame({
        "Colonna": [str(c) for c in df.columns],
        "Valore": ["— (NESSUN DATO)" if pd.isna(riga[c]) else str(riga[c]) for c in df.columns],
    })
    st.dataframe(valori_riga, hide_index=True)
    st.markdown(f"File di origine: <code>{origine}</code>", unsafe_allow_html=True)