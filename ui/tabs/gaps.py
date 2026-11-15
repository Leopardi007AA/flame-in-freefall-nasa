import html

import pandas as pd
import streamlit as st

from ui.components import badge
from ui.mock_data import show_mock_banner

# Keys that A uses inside "scenario".
# TO CONFIRM WITH A: if A names them differently, change only these two lines.
CHIAVE_GRAVITA = "gravita"
CHIAVE_O2 = "o2"

# Grid columns: (internal name, displayed label)
COLONNE = [
    ("1g", "1 g"),
    ("marte", "0.38 g (Mars)"),
    ("luna", "0.16 g (Moon)"),
    ("microgravita", "0 g (microgravity)"),
]

# Grid rows: oxygen in % by volume
OSSIGENO = [21, 26.5, 30, 40, 60]

# Value of the "gravita" column in the data -> grid column.
# Mars and Moon are not there: they stay empty until some data justify them.
GRAVITA_A_COLONNA = {"1g": "1g", "microgravita": "microgravita"}

# Numeric gravity of the scenario (in g) -> grid column
GRAVITA_NUMERICA = {"1g": 1.0, "marte": 0.38, "luna": 0.16, "microgravita": 0.0}

CSS = """
<style>
.gap-grid {
    display: grid;
    grid-template-columns: 110px repeat(4, minmax(0, 1fr));
    gap: 10px;
}
.gap-head {
    display: flex;
    align-items: center;
    padding: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: rgba(255,255,255,.72);
}
.gap-cell {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 6px;
    min-height: 72px;
    padding: 12px;
    border-radius: 16px;
    color: rgba(255,255,255,.92);
}
.gap-cell .badge { align-self: flex-start; }
.gap-tested {
    background: rgba(92,225,230,.18);
    border: 1px solid #5ce1e6;
    box-shadow: 0 0 22px rgba(92,225,230,.25);
}
.gap-empty {
    background: rgba(255,255,255,.03);
    border: 1px dashed rgba(255,255,255,.3);
}
.gap-now {
    border-color: #ff8a4c !important;
    border-width: 2px !important;
}
.gap-main {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
}
.gap-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: .06em;
    color: #ffb347;
}
.gap-tip {
    display: none;
    position: absolute;
    z-index: 20;
    left: 0;
    top: calc(100% + 6px);
    min-width: 200px;
    max-width: 280px;
    padding: 10px 12px;
    border-radius: 12px;
    background: #12182b;
    border: 1px solid rgba(255,255,255,.25);
    font-size: 13px;
    line-height: 1.4;
}
.gap-last .gap-tip { left: auto; right: 0; }
.gap-cell:hover .gap-tip,
.gap-cell:focus .gap-tip { display: block; }
.gap-note {
    margin: 4px 0;
    font-size: 13px;
    color: rgba(255,255,255,.72);
}
</style>
"""


# ======================================================================
# PART 1: the computation (no drawing). A can reuse coverage(df).
# ======================================================================

def manca(valore) -> bool:
    """True if the cell is empty. Zero is NOT empty: it is a real value."""
    return pd.isna(valore) or str(valore).strip() == ""


def coverage(df: pd.DataFrame) -> dict:
    """Computes which grid cells are tested.

    Returns a dictionary with three entries:
      "celle": {(column, oxygen): [experiment names]}
               the list is empty if the cell has no data
      "senza_ossigeno": how many experiments are excluded because the oxygen numbers are missing
      "senza_colonna": how many experiments do not fall in any gravity column
    """
    celle = {(chiave, o2): [] for chiave, _ in COLONNE for o2 in OSSIGENO}
    senza_ossigeno = 0
    senza_colonna = 0

    for _, riga in df.iterrows():
        if manca(riga["o2_min"]) or manca(riga["o2_max"]):
            senza_ossigeno += 1
            continue

        colonna = GRAVITA_A_COLONNA.get(str(riga["gravita"]).strip())
        if colonna is None:
            senza_colonna += 1
            continue

        for o2 in OSSIGENO:
            if float(riga["o2_min"]) <= o2 <= float(riga["o2_max"]):
                celle[(colonna, o2)].append(str(riga["nome"]))

    return {
        "celle": celle,
        "senza_ossigeno": senza_ossigeno,
        "senza_colonna": senza_colonna,
    }


# ======================================================================
# PART 2: the scenario (which cell to highlight)
# ======================================================================

def ossigeno_scenario(scenario):
    try:
        return float((scenario or {}).get(CHIAVE_O2))
    except (TypeError, ValueError):
        return None


def colonna_scenario(scenario):
    """Turns the scenario's gravity into a column. None if it does not recognize it."""
    app = {"earth": "1g", "mars": "marte", "moon": "luna", "iss": "microgravita"}
    if (scenario or {}).get("gravity") in app:      # key used by app.py
        return app[scenario["gravity"]]
    valore = (scenario or {}).get(CHIAVE_GRAVITA)
    try:
        g = float(valore)
    except (TypeError, ValueError):
        return GRAVITA_A_COLONNA.get(str(valore).strip())
    for chiave, valore_g in GRAVITA_NUMERICA.items():
        if abs(g - valore_g) < 0.01:
            return chiave
    return None


# ======================================================================
# PART 3: the drawing
# ======================================================================

def disegna_griglia(risultato: dict, scenario: dict) -> bool:
    """Draws the grid. Returns True if it highlighted the scenario's cell."""
    celle = risultato["celle"]
    colonna_ora = colonna_scenario(scenario)
    o2_ora = ossigeno_scenario(scenario)
    ultima = COLONNE[-1][0]
    evidenziata = False

    # First row: column headers
    out = '<div class="gap-grid"><div></div>'
    for _, etichetta in COLONNE:
        out += f'<div class="gap-head">{etichetta}</div>'

    # One row for each oxygen value
    for o2 in OSSIGENO:
        out += f'<div class="gap-head">{o2} % O₂</div>'

        for chiave, _ in COLONNE:
            nomi = celle[(chiave, o2)]
            adesso = chiave == colonna_ora and o2_ora is not None and abs(o2 - o2_ora) < 0.05

            classi = "gap-cell gap-tested" if nomi else "gap-cell gap-empty"
            if adesso:
                classi += " gap-now"
                evidenziata = True
            if chiave == ultima:
                classi += " gap-last"

            if nomi:
                elenco = "<br>".join(html.escape(n) for n in nomi[:8])
                if len(nomi) > 8:
                    elenco += f"<br>… and {len(nomi) - 8} more"
                corpo = (
                    f'<div class="gap-main">● TESTED · {len(nomi)}</div>'
                    f'<div class="gap-tip">Experiments:<br>{elenco}</div>'
                )
                extra = ' tabindex="0"'
            else:
                # Only one label for the scenario cell; the other empty cells show just “—”
                # (the legend below explains the symbol).
                corpo = '<div class="gap-main">—</div>'
                if adesso:
                    corpo += badge("NO DATA", "nodata")
                extra = ""

            if adesso:
                corpo += '<div class="gap-tag">◎ SCENARIO</div>'

            out += f'<div class="{classi}"{extra}>{corpo}</div>'

    out += "</div>"
    st.markdown(out, unsafe_allow_html=True)
    return evidenziata


def disegna_note(risultato: dict, scenario: dict, evidenziata: bool) -> None:
    righe = [
        "● TESTED · n = n experiments cover that gravity and that oxygen level (hover over the cell for the names). — = no data in our sources.",
        "The Mars and Moon columns stay empty until some data justify them.",
    ]
    if risultato["senza_ossigeno"]:
        righe.append(
            "Experiments excluded for incomplete data (oxygen not given): "
            f"{risultato['senza_ossigeno']}"
        )
    if risultato["senza_colonna"]:
        righe.append(
            "Experiments with mixed or unspecified gravity, not assigned to any column: "
            f"{risultato['senza_colonna']}"
        )
    if scenario and not evidenziata:
        righe.append(
            "The scenario cell is not highlighted: the scenario's gravity or oxygen "
            "does not match any cell in the grid."
        )

    st.markdown(
        "".join(f'<p class="gap-note">{r}</p>' for r in righe),
        unsafe_allow_html=True,
    )


# ======================================================================
# The function that A calls
# ======================================================================

def render(df: pd.DataFrame, scenario: dict, highlight_ids: list) -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    show_mock_banner()

    st.subheader("Where we have data, and where we don't")

    risultato = coverage(df)
    evidenziata = disegna_griglia(risultato, scenario)
    disegna_note(risultato, scenario, evidenziata)
