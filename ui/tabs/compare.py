import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ui.components import badge
from ui.mock_data import show_mock_banner
from ui.plotly_theme import style_fig

# Name of the oxygen key inside "scenario".
# TO CONFIRM WITH A: if A names it differently, change only this line.
CHIAVE_O2 = "o2"

NESSUN_DATO = "— " + badge("NO DATA", "nodata")

# The CSV keeps its Italian values (they are the data contract used by the code);
# these maps only change what the dashboard SHOWS. A value that is not in a map is shown as is.
ETICHETTE_STATO = {"solido": "Solid", "liquido": "Liquid", "gassoso": "Gas",
                   "misto": "Mixed", "fumo": "Smoke"}
ETICHETTE_AREA = {"prevenzione": "Prevention", "rilevazione": "Detection",
                  "soppressione": "Suppression"}
ETICHETTE_DATI_GREZZI = {"si": "Yes", "no": "No", "parziale": "Partial"}

CSS = """
<style>
.cmp-wrap { overflow-x: auto; }
.cmp-table { width: 100%; border-collapse: collapse; }
.cmp-table th, .cmp-table td {
    text-align: left;
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255,255,255,.14);
    vertical-align: top;
    color: rgba(255,255,255,.92);
}
.cmp-table th {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: rgba(255,255,255,.72);
}
.cmp-table tr.diff td, .cmp-table tr.diff th {
    background: rgba(255,138,76,.14);
}
</style>
"""


# ---------- small helper functions ----------

def manca(valore) -> bool:
    """True if the cell is empty. Zero is NOT empty: it is a real value."""
    return pd.isna(valore) or str(valore).strip() == ""


def numero(x) -> str:
    """26.0 becomes '26', 26.5 stays '26.5'."""
    return f"{float(x):g}"


def testo(valore, elenco=False, etichette=None):
    """Returns the text of the cell, or None if it is missing.

    elenco: the cell holds a list separated by "|" and it is shown separated by commas.
    etichette: optional map {data value: displayed label}.
    """
    if manca(valore):
        return None
    t = str(valore).strip()
    parti = [p.strip() for p in t.split("|")] if elenco else [t]
    if etichette:
        parti = [etichette.get(p, p) for p in parti]
    return ", ".join(parti)


def intervallo(minimo, massimo, unita):
    """Returns '21–30 %', '21 %', 'min 21 %'... or None if both are missing."""
    if manca(minimo) and manca(massimo):
        return None
    if manca(minimo):
        return f"max {numero(massimo)} {unita}"
    if manca(massimo):
        return f"min {numero(minimo)} {unita}"
    if float(minimo) == float(massimo):
        return f"{numero(minimo)} {unita}"
    return f"{numero(minimo)}–{numero(massimo)} {unita}"


def ossigeno_scenario(scenario):
    """Reads the scenario's oxygen. Returns None if there is none."""
    try:
        return float((scenario or {}).get(CHIAVE_O2))
    except (TypeError, ValueError):
        return None


def attributi(riga) -> dict:
    """The table rows for ONE experiment."""
    return {
        "Fuel state": testo(riga["stato_combustibile"], etichette=ETICHETTE_STATO),
        "Fuels": testo(riga["combustibili"], elenco=True),
        "Oxygen": intervallo(riga["o2_min"], riga["o2_max"], "%"),
        "Pressure": intervallo(riga["pressione_min_psia"], riga["pressione_max_psia"], "psia"),
        "Airflow": intervallo(riga["flusso_min_cm_s"], riga["flusso_max_cm_s"], "cm/s"),
        "Sensors": testo(riga["sensori"], elenco=True),
        "Safety area": testo(riga["area_sicurezza"], elenco=True, etichette=ETICHETTE_AREA),
        "Raw data": testo(riga["dati_grezzi"], etichette=ETICHETTE_DATI_GREZZI),
    }


def cella(valore) -> str:
    if valore is None:
        return NESSUN_DATO
    return html.escape(valore)


# ---------- the three parts of the tab ----------

def tabella(scelti: pd.DataFrame) -> None:
    colonne = [attributi(riga) for _, riga in scelti.iterrows()]

    intestazione = '<tr><th scope="col">Attribute</th>'
    for nome in scelti["nome"]:
        intestazione += f'<th scope="col">{html.escape(str(nome))}</th>'
    intestazione += "</tr>"

    righe = ""
    for etichetta in colonne[0]:
        valori = [c[etichetta] for c in colonne]
        classe = ' class="diff"' if len(set(valori)) > 1 else ""
        righe += f'<tr{classe}><th scope="row">{etichetta}</th>'
        righe += "".join(f"<td>{cella(v)}</td>" for v in valori)
        righe += "</tr>"

    st.markdown(
        f'<div class="cmp-wrap"><table class="cmp-table">{intestazione}{righe}</table></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<span class="mono-label">Orange background = the experiments differ on this row</span>',
        unsafe_allow_html=True,
    )


def grafico_ossigeno(scelti: pd.DataFrame, scenario: dict) -> None:
    fig = go.Figure()
    esclusi = 0

    for _, riga in scelti.iterrows():
        if manca(riga["o2_min"]) or manca(riga["o2_max"]):
            esclusi += 1
            continue
        minimo = float(riga["o2_min"])
        massimo = float(riga["o2_max"])
        fig.add_trace(
            go.Bar(
                y=[riga["nome"]],
                x=[max(massimo - minimo, 0.3)],  # at least 0.3 so that a single value is visible
                base=[minimo],
                orientation="h",
                name=str(riga["nome"]),
                hovertext=[intervallo(minimo, massimo, "%")],
                hoverinfo="text",
            )
        )

    if not fig.data:
        st.markdown(
            "None of the selected experiments has oxygen values. " + badge("NO DATA", "nodata"),
            unsafe_allow_html=True,
        )
        return

    o2 = ossigeno_scenario(scenario)
    if o2 is not None:
        fig.add_vline(
            x=o2,
            line_dash="dash",
            line_color="#ffb347",
            annotation_text=f"Scenario {numero(o2)}%",
            annotation_position="top right",
            annotation_font_color="#ffb347",
        )

    style_fig(fig, height=140 + 60 * len(fig.data))
    fig.update_layout(
        title="Oxygen ranges (% by volume)",
        barmode="overlay",
        showlegend=False,
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, config={"displayModeBar": False})

    if esclusi:
        st.markdown(
            f'<span class="mono-label">Experiments without oxygen data (not shown in the chart): {esclusi}</span>',
            unsafe_allow_html=True,
        )


def bottoni_psi(scelti: pd.DataFrame) -> None:
    colonne = st.columns(len(scelti))
    for col, (_, riga) in zip(colonne, scelti.iterrows()):
        with col:
            if manca(riga["url_psi"]):
                st.markdown(
                    f'{html.escape(str(riga["nome"]))}: PSI page not available '
                    + badge("NO DATA", "nodata"),
                    unsafe_allow_html=True,
                )
            else:
                st.link_button(f'Open the PSI page · {riga["nome"]}', riga["url_psi"])


# ---------- the function that A calls ----------

def render(df: pd.DataFrame, scenario: dict, highlight_ids: list) -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    show_mock_banner()

    nomi = dict(zip(df["id"], df["nome"]))
    preselezionati = [i for i in (highlight_ids or []) if i in nomi][:3]

    selezione = st.multiselect(
        "Choose up to 3 experiments to compare",
        options=df["id"].tolist(),
        default=preselezionati,
        max_selections=3,
        format_func=lambda i: str(nomi[i]),
    )

    if not selezione:
        st.write("Choose at least one experiment to see the comparison.")
        return

    scelti = df.set_index("id").loc[selezione].reset_index()

    tabella(scelti)
    grafico_ossigeno(scelti, scenario)
    bottoni_psi(scelti)
