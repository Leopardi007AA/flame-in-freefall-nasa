"""ui/tabs/real_data.py - scheda Dati reali: esploratore generico delle tabelle sperimentali.

Interfaccia concordata con il ruolo A: render(tables: dict[str, DataFrame]).
Se tables è vuoto prova a scoprire i file in data/raw/; i file di esempio (nome con
«sample» o «esempio») NON vengono mai mostrati come dati reali.
"""
import html
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from ui.components import badge, glass_card
from ui.plotly_theme import style_fig

RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
NONE_LABEL = "(nessuno)"
MAX_TEXT_FILTER = 30


def discover_tables(raw_dir: Path = RAW_DIR) -> dict:
    """Legge i CSV/TSV in data/raw/<progetto>/, saltando i file di esempio."""
    tables = {}
    if not raw_dir.exists():
        return tables
    for f in sorted(raw_dir.glob("*/*")):
        if f.suffix.lower() not in (".csv", ".tsv", ".txt"):
            continue
        if any(w in f.stem.lower() for w in ("sample", "esempio")):
            continue
        try:
            tables[f"{f.parent.name} / {f.name}"] = pd.read_csv(f, sep=None, engine="python")
        except Exception:
            continue
    return tables


def apply_filters(df: pd.DataFrame, key: str) -> pd.DataFrame:
    out = df
    with st.expander("Filtri"):
        for c in df.columns:
            s = df[c].dropna()
            if s.empty:
                continue
            if pd.api.types.is_numeric_dtype(s):
                lo, hi = float(s.min()), float(s.max())
                if lo < hi:
                    a, b = st.slider(str(c), lo, hi, (lo, hi), key=f"{key}_f_{c}")
                    out = out[out[c].isna() | ((out[c] >= a) & (out[c] <= b))]
            elif s.nunique() <= MAX_TEXT_FILTER:
                opts = sorted(s.astype(str).unique())
                pick = st.multiselect(str(c), opts, key=f"{key}_f_{c}")
                if pick:
                    out = out[out[c].astype(str).isin(pick)]
    return out


def render(tables: dict | None = None) -> None:
    tables = tables or discover_tables()
    if not tables:
        glass_card("Tabelle originali NASA non ancora caricate",
                   badge("NESSUN DATO", "nodata") + "<p>In <code>data/raw/</code> ci sono solo file di esempio, "
                   "che non mostriamo come dati reali. Appena i download originali da NASA PSI "
                   "saranno al loro posto, qui compare l'esploratore.</p>")
        return
    name = st.selectbox("Tabella", list(tables))
    df = tables[name]
    st.markdown(badge("REALE", "real") + f" file di origine: <code>{html.escape(str(name))}</code>",
                unsafe_allow_html=True)
    empty = [c for c in df.columns if df[c].isna().all()]
    usable = [c for c in df.columns if c not in empty]
    numeric = [c for c in usable if pd.api.types.is_numeric_dtype(df[c])]
    if empty:
        st.caption("Non disponibile in questa tabella: " + ", ".join(map(str, empty)))
    if len(usable) < 2 or not numeric:
        st.dataframe(df, hide_index=True)
        return
    k = f"rd_{name}"
    c1, c2, c3 = st.columns(3)
    x = c1.selectbox("Asse x", usable, key=f"{k}_x")
    y = c2.selectbox("Asse y", numeric, index=min(1, len(numeric) - 1), key=f"{k}_y")
    color = c3.selectbox("Colore", [NONE_LABEL] + usable, key=f"{k}_c")
    flt = apply_filters(df, k)
    fig = px.scatter(flt, x=x, y=y, color=None if color == NONE_LABEL else color)
    st.plotly_chart(style_fig(fig), config={"displayModeBar": False})
    st.caption(f"{len(flt)} righe su {len(df)} dopo i filtri.")
    st.dataframe(flt, hide_index=True)
    st.download_button("Scarica il CSV filtrato", flt.to_csv(index=False).encode("utf-8"),
                       file_name="dati_filtrati.csv", mime="text/csv")
    if len(flt):
        idx = st.selectbox("Ispeziona una riga", list(flt.index), key=f"{k}_row")
        rec = flt.loc[idx]
        st.table(pd.DataFrame({"valore": rec.map(lambda v: "Non disponibile" if pd.isna(v) else str(v))}))
        st.caption(f"Riga {idx} del file {name}.")
