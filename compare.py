"""ui/tabs/compare.py - scheda Confronto: fino a 3 esperimenti affiancati.

Interfaccia concordata con il ruolo A: render(df, scenario, highlight_ids).
Regola n. 1: una cella senza dato mostra «—» con l'etichetta NESSUN DATO, mai 0.
"""
import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ui.components import badge
from ui.plotly_theme import style_fig

MAX_SELECTED = 3
HILITE = "background:rgba(255,138,76,.14);"

# (etichetta, colonna testo | (colonna min, colonna max), unità se numerico)
ROWS = [
    ("Stato del combustibile", "stato_combustibile", None),
    ("Combustibili", "combustibili", None),
    ("Ossigeno", ("o2_min", "o2_max"), "%"),
    ("Pressione", ("pressione_min_psia", "pressione_max_psia"), "psia"),
    ("Flusso d'aria", ("flusso_min_cm_s", "flusso_max_cm_s"), "cm/s"),
    ("Sensori", "sensori", None),
    ("Aree di sicurezza", "area_sicurezza", None),
    ("Dati grezzi", "dati_grezzi", None),
]


def fmt_range(lo, hi):
    """Testo di un intervallo, oppure None se mancano entrambi i valori."""
    lo_ok, hi_ok = not pd.isna(lo), not pd.isna(hi)
    if not lo_ok and not hi_ok:
        return None
    if lo_ok and hi_ok:
        return f"{lo:g}" if lo == hi else f"{lo:g}–{hi:g}"
    return f"≥ {lo:g}" if lo_ok else f"≤ {hi:g}"


def fmt_text(value):
    """Testo di una cella, oppure None se vuota."""
    if value is None or pd.isna(value) or str(value).strip() == "":
        return None
    return str(value).replace("|", ", ")


def build_rows(sel: pd.DataFrame):
    """Una riga per attributo: (etichetta, unità, [valori o None], differisce?)."""
    out = []
    for label, col, unit in ROWS:
        if isinstance(col, tuple):
            vals = [fmt_range(r[col[0]], r[col[1]]) for _, r in sel.iterrows()]
        else:
            vals = [fmt_text(r[col]) for _, r in sel.iterrows()]
        out.append((label, unit, vals, len(set(vals)) > 1))
    return out


def _cell(value, unit):
    if value is None:
        return "— " + badge("NESSUN DATO", "nodata")
    if unit:
        return f"{html.escape(value)} {unit} " + badge("REALE", "real")
    return html.escape(value)


def table_html(sel: pd.DataFrame) -> str:
    th = "".join(f'<th style="text-align:left;padding:8px 10px;">{html.escape(str(n))}</th>'
                 for n in sel["nome"])
    body = []
    for label, unit, vals, differs in build_rows(sel):
        style = HILITE if differs else ""
        tds = "".join(f'<td style="padding:8px 10px;vertical-align:top;">{_cell(v, unit)}</td>'
                      for v in vals)
        body.append(f'<tr style="{style}"><td class="mono-label" style="padding:8px 10px;">'
                    f'{html.escape(label)}</td>{tds}</tr>')
    return ('<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;">'
            f'<thead><tr><th></th>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>')


def o2_figure(sel: pd.DataFrame, o2_scenario: float):
    """Barre orizzontali degli intervalli di ossigeno + linea dello scenario. None se nessun dato."""
    have = sel.dropna(subset=["o2_min", "o2_max"])
    if have.empty:
        return None
    fig = go.Figure()
    for _, r in have.iterrows():
        fig.add_trace(go.Bar(y=[r["nome"]], x=[max(r["o2_max"] - r["o2_min"], 0.3)], base=[r["o2_min"]],
                             orientation="h", name=str(r["id"]),
                             hovertemplate=f"{r['o2_min']:g}–{r['o2_max']:g} %<extra>{r['id']}</extra>"))
    fig.add_vline(x=o2_scenario, line_dash="dash", line_color="#ff7a3d",
                  annotation_text=f"Scenario {o2_scenario:g}%", annotation_font_color="#ff7a3d")
    fig.update_xaxes(title="Ossigeno (% in volume)", range=[0, 100])
    fig.update_layout(showlegend=False, barmode="overlay")
    return style_fig(fig, height=120 + 60 * len(have))


def render(df: pd.DataFrame, scenario: dict, highlight_ids: list) -> None:
    ids = df["id"].astype(str).tolist()
    names = dict(zip(ids, df["nome"].astype(str)))
    default = [i for i in (highlight_ids or []) if i in ids][:MAX_SELECTED]
    chosen = list(st.multiselect(
        f"Scegli fino a {MAX_SELECTED} esperimenti", ids, default=default,
        format_func=lambda i: f"{i} · {names[i]}", max_selections=MAX_SELECTED,
        key="cmp_sel_" + "_".join(default)))
    if not chosen:
        st.info("Seleziona almeno un esperimento per vedere il confronto.")
        return
    sel = df.set_index(df["id"].astype(str), drop=False).loc[chosen].reset_index(drop=True)
    st.markdown(table_html(sel), unsafe_allow_html=True)
    st.caption("Le righe su sfondo arancio sono quelle in cui gli esperimenti differiscono. "
               "«—» = nessun dato nelle fonti (non è zero).")
    fig = o2_figure(sel, float(scenario["o2"]))
    if fig is None:
        st.info("Nessuno degli esperimenti scelti ha un intervallo di ossigeno nei dati.")
    else:
        st.plotly_chart(fig, config={"displayModeBar": False})
        missing = sel[sel[["o2_min", "o2_max"]].isna().any(axis=1)]["nome"].tolist()
        if missing:
            st.caption("Senza dati di ossigeno (non disegnati): " + ", ".join(missing))
    cols = st.columns(len(chosen))
    for col, (_, r) in zip(cols, sel.iterrows()):
        with col:
            url = fmt_text(r["url_psi"])
            if url and url.startswith("https://"):
                st.link_button(f"Apri la scheda PSI · {r['id']}", url)
            else:
                st.caption(f"{r['id']}: scheda PSI non disponibile")
