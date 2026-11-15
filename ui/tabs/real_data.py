import html
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from ui.components import badge
from ui import mock_data
from ui.plotly_theme import style_fig

NESSUNO = "(none)"
RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"

# File names containing one of these words are sample files and are never shown as real data.
# ("esempio" is kept so that sample files named in Italian are still skipped.)
SAMPLE_WORDS = ("sample", "example", "esempio")


def discover_tables(raw_dir: Path = RAW_DIR) -> dict:
    """Reads the CSV/TSV files in data/raw/<project>/, skipping the sample files."""
    tables = {}
    if not raw_dir.exists():
        return tables
    for f in sorted(raw_dir.glob("*/*")):
        if f.suffix.lower() not in (".csv", ".tsv", ".txt"):
            continue
        if any(w in f.stem.lower() for w in SAMPLE_WORDS):
            continue
        try:
            df = pd.read_csv(f, sep=None, engine="python")
        except Exception:
            continue
        df.attrs["file"] = f"data/raw/{f.parent.name}/{f.name}"
        tables[f"{f.parent.name} / {f.name}"] = df
    return tables


def render(tables: dict | None = None) -> None:
    mock_data.show_mock_banner()

    if not tables:
        tables = discover_tables()   # app.py passes {}: we look for them ourselves in data/raw/

    if not tables:
        st.markdown(
            "### Original NASA tables not loaded yet\n"
            + badge("NO DATA", "nodata")
            + " There are no original tables in <code>data/raw/</code> yet; we do not show sample files as real data.",
            unsafe_allow_html=True,
        )
        return

    # 1) Table choice + badge + source file
    nome = st.selectbox("Table", list(tables.keys()))
    df = tables[nome]
    origine = html.escape(str(df.attrs.get("file", nome)))
    etichetta = badge("ILLUSTRATIVE", "illustrative") if mock_data.IS_MOCK else badge("REAL", "real")
    st.markdown(f"{etichetta} &nbsp; Source file: <code>{origine}</code>", unsafe_allow_html=True)

    # Which columns have at least one value?
    con_dati = [c for c in df.columns if df[c].notna().any()]
    senza_dati = [c for c in df.columns if c not in con_dati]
    numeriche = [c for c in con_dati if pd.api.types.is_numeric_dtype(df[c])]

    # 6) Empty columns are declared, not hidden
    if senza_dati:
        elenco = html.escape(", ".join(str(c) for c in senza_dati))
        st.markdown(
            f"Not available in this table: {elenco} " + badge("NO DATA", "nodata"),
            unsafe_allow_html=True,
        )

    if not con_dati:
        return

    # 2) Chart menus
    base = numeriche if numeriche else con_dati
    y_iniziale = base[1] if len(base) > 1 else base[0]
    c1, c2, c3 = st.columns(3)
    with c1:
        x = st.selectbox("X axis", con_dati, index=con_dati.index(base[0]))
    with c2:
        y = st.selectbox("Y axis", con_dati, index=con_dati.index(y_iniziale))
    with c3:
        colore = st.selectbox("Color", [NESSUNO] + con_dati)

    # 3) Filters: choose the columns to filter
    filtrate = df
    scelte = st.multiselect("Filter by columns", con_dati)
    for c in scelte:
        if c in numeriche:
            minimo, massimo = float(df[c].min()), float(df[c].max())
            if minimo == massimo:
                st.write(f"{c}: single value ({minimo:g}), no filter possible")
                continue
            da, a = st.slider(str(c), minimo, massimo, (minimo, massimo))
            filtrate = filtrate[filtrate[c].between(da, a)]
        else:
            valori = sorted(df[c].dropna().astype(str).unique())
            scelti = st.multiselect(str(c), valori)
            if scelti:
                filtrate = filtrate[filtrate[c].astype(str).isin(scelti)]

    st.markdown(
        f'<span class="mono-label">{len(filtrate)} rows out of {len(df)}. '
        "Rows with no value in a filtered column are excluded.</span>",
        unsafe_allow_html=True,
    )

    # Scatter plot
    dati = filtrate.dropna(subset=list({x, y}))
    senza_xy = len(filtrate) - len(dati)
    if dati.empty:
        st.write("No row has values for both the x axis and the y axis.")
    else:
        fig = px.scatter(dati, x=x, y=y, color=None if colore == NESSUNO else colore)
        fig.update_traces(marker=dict(size=9))
        style_fig(fig, height=400)
        st.plotly_chart(fig, config={"displayModeBar": False})
    if senza_xy:
        st.markdown(
            f'<span class="mono-label">Rows without a value for x or y (not in the chart): {senza_xy}</span>',
            unsafe_allow_html=True,
        )

    # 4) Filtered table and download
    st.dataframe(filtrate)
    st.download_button(
        "Download filtered CSV",
        filtrate.to_csv(index=False).encode("utf-8"),
        file_name=f"{nome}_filtered.csv".replace(" ", "_"),
        mime="text/csv",
    )

    # 5) Record inspector
    if filtrate.empty:
        return
    indice = st.selectbox("Inspect a row", list(filtrate.index), format_func=lambda i: f"Row {i}")
    riga = filtrate.loc[indice]
    valori_riga = pd.DataFrame({
        "Column": [str(c) for c in df.columns],
        "Value": ["— (NO DATA)" if pd.isna(riga[c]) else str(riga[c]) for c in df.columns],
    })
    st.dataframe(valori_riga, hide_index=True)
    st.markdown(f"Source file: <code>{origine}</code>", unsafe_allow_html=True)
