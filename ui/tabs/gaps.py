"""ui/tabs/gaps.py - scheda Lacune: dove esistono dati e dove no.

Interfaccia concordata con il ruolo A: render(df, scenario, highlight_ids).
coverage(df) è separata dal disegno, così A può riusarla.
"""
import html

import pandas as pd
import streamlit as st

from ui.components import badge

# (chiave, etichetta, valore di gravita' nel CSV, scenario di A)
GRAVITY_COLS = [
    ("1g", "1 g (Terra)", "1g", "earth"),
    ("mars", "0,38 g (Marte)", None, "mars"),
    ("moon", "0,16 g (Luna)", None, "moon"),
    ("0g", "0 g (microgravità)", "microgravita", "iss"),
]
O2_ROWS = [21, 26.5, 30, 40, 60]


def coverage(df: pd.DataFrame) -> dict:
    """{'cells': {(colonna, o2): [id, ...]}, 'excluded_o2': [id], 'excluded_gravity': [id]}.
    Una cella è testata se esiste un esperimento con quella gravità e o2_min <= valore <= o2_max.
    Luna e Marte restano vuote finché nessun dato le giustifica."""
    col_of = {g: key for key, _, g, _ in GRAVITY_COLS if g}
    cells = {(key, o2): [] for key, *_ in GRAVITY_COLS for o2 in O2_ROWS}
    ex_o2, ex_g = [], []
    for _, r in df.iterrows():
        eid = str(r["id"])
        if pd.isna(r["o2_min"]) or pd.isna(r["o2_max"]):
            ex_o2.append(eid)
            continue
        key = col_of.get(r["gravita"]) if not pd.isna(r["gravita"]) else None
        if key is None:
            ex_g.append(eid)
            continue
        for o2 in O2_ROWS:
            if r["o2_min"] <= o2 <= r["o2_max"]:
                cells[(key, o2)].append(eid)
    return {"cells": cells, "excluded_o2": ex_o2, "excluded_gravity": ex_g}


def scenario_cell(scenario: dict):
    """(colonna, riga o2 più vicina) dello scenario attuale."""
    col = next(k for k, _, _, s in GRAVITY_COLS if s == scenario["gravity"])
    row = min(O2_ROWS, key=lambda v: abs(v - float(scenario["o2"])))
    return col, row


def grid_html(cov: dict, names: dict, scenario: dict, highlight_ids: list) -> str:
    sc = scenario_cell(scenario)
    head = "".join(f'<th style="padding:8px 10px;text-align:center;">{html.escape(lab)}</th>'
                   for _, lab, _, _ in GRAVITY_COLS)
    rows = []
    for o2 in O2_ROWS:
        tds = []
        for key, *_ in GRAVITY_COLS:
            ids = cov["cells"][(key, o2)]
            outline = "outline:2px solid #ff7a3d;outline-offset:-2px;" if (key, o2) == sc else ""
            if ids:
                star = " ★" if any(i in (highlight_ids or []) for i in ids) else ""
                tip = html.escape(", ".join(f"{i} · {names.get(i, '')}" for i in ids))
                tds.append(f'<td title="{tip}" style="padding:10px;text-align:center;border-radius:10px;'
                           f'background:rgba(92,225,230,.28);border:1px solid #5ce1e6;{outline}">'
                           f"◆ {len(ids)} esp.{star}</td>")
            else:
                tds.append('<td style="padding:10px;text-align:center;border-radius:10px;'
                           f'border:1px dashed rgba(255,255,255,.28);color:rgba(255,255,255,.72);{outline}">'
                           "○ nessun dato</td>")
        rows.append(f'<tr><th class="mono-label" style="padding:8px 10px;text-align:left;">O₂ {o2:g}%</th>'
                    f'{"".join(tds)}</tr>')
    return ('<div style="overflow-x:auto;"><table style="width:100%;border-collapse:separate;border-spacing:6px;">'
            f'<thead><tr><th></th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def render(df: pd.DataFrame, scenario: dict, highlight_ids: list) -> None:
    cov = coverage(df)
    names = dict(zip(df["id"].astype(str), df["nome"].astype(str)))
    tested = sum(1 for v in cov["cells"].values() if v)
    st.markdown(badge("REALE", "real") + f" {tested} celle su {len(cov['cells'])} hanno almeno un esperimento. "
                "Il resto è una lacuna: non esistono dati nelle nostre fonti.", unsafe_allow_html=True)
    st.markdown(grid_html(cov, names, scenario, highlight_ids), unsafe_allow_html=True)
    st.caption("◆ cella testata (passa il mouse per vedere quali esperimenti) · ○ nessun dato · "
               "bordo arancio = scenario attuale (riga di ossigeno più vicina).")
    if cov["excluded_o2"]:
        st.caption(f"{len(cov['excluded_o2'])} esperimenti esclusi per dati di ossigeno incompleti.")
    if cov["excluded_gravity"]:
        st.caption(f"{len(cov['excluded_gravity'])} esperimenti con gravità «mista» o non indicata, "
                   "non assegnabili a una colonna.")
