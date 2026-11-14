import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ui.components import badge
from ui.mock_data import show_mock_banner
from ui.plotly_theme import style_fig

# Nome della chiave dell'ossigeno dentro "scenario".
# DA CONFERMARE CON A: se lui la chiama in un altro modo, cambia solo questa riga.
CHIAVE_O2 = "o2"

NESSUN_DATO = "— " + badge("NESSUN DATO", "nodata")

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


# ---------- piccole funzioni di aiuto ----------

def manca(valore) -> bool:
    """Vero se la cella è vuota. Lo zero NON è vuoto: è un dato vero."""
    return pd.isna(valore) or str(valore).strip() == ""


def numero(x) -> str:
    """26.0 diventa '26', 26.5 resta '26.5'."""
    return f"{float(x):g}"


def testo(valore, elenco=False):
    """Restituisce il testo della cella, oppure None se manca."""
    if manca(valore):
        return None
    t = str(valore).strip()
    if elenco:
        t = ", ".join(parte.strip() for parte in t.split("|"))
    return t


def intervallo(minimo, massimo, unita):
    """Restituisce '21–30 %', '21 %', 'min 21 %'... oppure None se mancano entrambi."""
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
    """Legge l'ossigeno dello scenario. Restituisce None se non c'è."""
    try:
        return float((scenario or {}).get(CHIAVE_O2))
    except (TypeError, ValueError):
        return None


def attributi(riga) -> dict:
    """Le righe della tabella per UN esperimento."""
    return {
        "Stato del combustibile": testo(riga["stato_combustibile"]),
        "Combustibili": testo(riga["combustibili"], elenco=True),
        "Ossigeno": intervallo(riga["o2_min"], riga["o2_max"], "%"),
        "Pressione": intervallo(riga["pressione_min_psia"], riga["pressione_max_psia"], "psia"),
        "Flusso": intervallo(riga["flusso_min_cm_s"], riga["flusso_max_cm_s"], "cm/s"),
        "Sensori": testo(riga["sensori"], elenco=True),
        "Area di sicurezza": testo(riga["area_sicurezza"], elenco=True),
        "Dati grezzi": testo(riga["dati_grezzi"]),
    }


def cella(valore) -> str:
    if valore is None:
        return NESSUN_DATO
    return html.escape(valore)


# ---------- le tre parti della scheda ----------

def tabella(scelti: pd.DataFrame) -> None:
    colonne = [attributi(riga) for _, riga in scelti.iterrows()]

    intestazione = '<tr><th scope="col">Attributo</th>'
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
        '<span class="mono-label">Sfondo arancio = gli esperimenti differiscono su questa riga</span>',
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
                x=[max(massimo - minimo, 0.3)],  # almeno 0.3 per vedere un valore singolo
                base=[minimo],
                orientation="h",
                name=str(riga["nome"]),
                hovertext=[intervallo(minimo, massimo, "%")],
                hoverinfo="text",
            )
        )

    if not fig.data:
        st.markdown(
            "Nessun esperimento scelto ha i valori di ossigeno. " + badge("NESSUN DATO", "nodata"),
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
        title="Intervalli di ossigeno (% in volume)",
        barmode="overlay",
        showlegend=False,
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, config={"displayModeBar": False})

    if esclusi:
        st.markdown(
            f'<span class="mono-label">Esperimenti senza dati di ossigeno (non mostrati nel grafico): {esclusi}</span>',
            unsafe_allow_html=True,
        )


def bottoni_psi(scelti: pd.DataFrame) -> None:
    colonne = st.columns(len(scelti))
    for col, (_, riga) in zip(colonne, scelti.iterrows()):
        with col:
            if manca(riga["url_psi"]):
                st.markdown(
                    f'{html.escape(str(riga["nome"]))}: scheda PSI non disponibile '
                    + badge("NESSUN DATO", "nodata"),
                    unsafe_allow_html=True,
                )
            else:
                st.link_button(f'Apri la scheda PSI · {riga["nome"]}', riga["url_psi"])


# ---------- la funzione che chiama A ----------

def render(df: pd.DataFrame, scenario: dict, highlight_ids: list) -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    show_mock_banner()

    nomi = dict(zip(df["id"], df["nome"]))
    preselezionati = [i for i in (highlight_ids or []) if i in nomi][:3]

    selezione = st.multiselect(
        "Scegli fino a 3 esperimenti da confrontare",
        options=df["id"].tolist(),
        default=preselezionati,
        max_selections=3,
        format_func=lambda i: str(nomi[i]),
    )

    if not selezione:
        st.write("Scegli almeno un esperimento per vedere il confronto.")
        return

    scelti = df.set_index("id").loc[selezione].reset_index()

    tabella(scelti)
    grafico_ossigeno(scelti, scenario)
    bottoni_psi(scelti)