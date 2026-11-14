import html

import pandas as pd
import streamlit as st

from ui.components import badge
from ui.mock_data import show_mock_banner

# Chiavi che A usa dentro "scenario".
# DA CONFERMARE CON A: se le chiama in un altro modo, cambia solo queste due righe.
CHIAVE_GRAVITA = "gravita"
CHIAVE_O2 = "o2"

# Colonne della griglia: (nome interno, etichetta mostrata)
COLONNE = [
    ("1g", "1 g"),
    ("marte", "0,38 g (Marte)"),
    ("luna", "0,16 g (Luna)"),
    ("microgravita", "0 g (microgravità)"),
]

# Righe della griglia: ossigeno in % di volume
OSSIGENO = [21, 26.5, 30, 40, 60]

# Valore della colonna "gravita" nei dati -> colonna della griglia.
# Marte e Luna non ci sono: restano vuote finché nessun dato le giustifica.
GRAVITA_A_COLONNA = {"1g": "1g", "microgravita": "microgravita"}

# Gravità numerica dello scenario (in g) -> colonna della griglia
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
# PARTE 1: il calcolo (nessun disegno). A può riusare coverage(df).
# ======================================================================

def manca(valore) -> bool:
    """Vero se la cella è vuota. Lo zero NON è vuoto: è un dato vero."""
    return pd.isna(valore) or str(valore).strip() == ""


def coverage(df: pd.DataFrame) -> dict:
    """Calcola quali celle della griglia sono testate.

    Restituisce un dizionario con tre voci:
      "celle": {(colonna, ossigeno): [nomi degli esperimenti]}
               la lista è vuota se la cella non ha dati
      "senza_ossigeno": quanti esperimenti sono esclusi perché mancano i numeri di ossigeno
      "senza_colonna": quanti esperimenti non finiscono in nessuna colonna di gravità
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
# PARTE 2: lo scenario (quale cella evidenziare)
# ======================================================================

def ossigeno_scenario(scenario):
    try:
        return float((scenario or {}).get(CHIAVE_O2))
    except (TypeError, ValueError):
        return None


def colonna_scenario(scenario):
    """Trasforma la gravità dello scenario in una colonna. None se non la riconosce."""
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
# PARTE 3: il disegno
# ======================================================================

def disegna_griglia(risultato: dict, scenario: dict) -> bool:
    """Disegna la griglia. Restituisce True se ha evidenziato la cella dello scenario."""
    celle = risultato["celle"]
    colonna_ora = colonna_scenario(scenario)
    o2_ora = ossigeno_scenario(scenario)
    ultima = COLONNE[-1][0]
    evidenziata = False

    # Prima riga: intestazioni delle colonne
    out = '<div class="gap-grid"><div></div>'
    for _, etichetta in COLONNE:
        out += f'<div class="gap-head">{etichetta}</div>'

    # Una riga per ogni valore di ossigeno
    for o2 in OSSIGENO:
        out += f'<div class="gap-head">{str(o2).replace(".", ",")} % O₂</div>'

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
                    elenco += f"<br>… e altri {len(nomi) - 8}"
                corpo = (
                    '<div class="gap-main">● TESTATO</div>'
                    f'<div class="gap-tip">Esperimenti:<br>{elenco}</div>'
                )
                extra = ' tabindex="0"'
            else:
                corpo = '<div class="gap-main">—</div>' + badge("NESSUN DATO", "nodata")
                extra = ""

            if adesso:
                corpo += '<div class="gap-tag">◎ SCENARIO</div>'

            out += f'<div class="{classi}"{extra}>{corpo}</div>'

    out += "</div>"
    st.markdown(out, unsafe_allow_html=True)
    return evidenziata


def disegna_note(risultato: dict, scenario: dict, evidenziata: bool) -> None:
    righe = [
        "● TESTATO = almeno un esperimento copre quella gravità e quell'ossigeno. — = nessun dato.",
        "Le colonne Marte e Luna restano vuote finché nessun dato le giustifica.",
    ]
    if risultato["senza_ossigeno"]:
        righe.append(
            "Esperimenti esclusi per dati incompleti (ossigeno non indicato): "
            f"{risultato['senza_ossigeno']}"
        )
    if risultato["senza_colonna"]:
        righe.append(
            "Esperimenti con gravità mista o non indicata, non assegnati a nessuna colonna: "
            f"{risultato['senza_colonna']}"
        )
    if scenario and not evidenziata:
        righe.append(
            "La cella dello scenario non è evidenziata: gravità o ossigeno dello scenario "
            "non corrispondono a nessuna cella della griglia."
        )

    st.markdown(
        "".join(f'<p class="gap-note">{r}</p>' for r in righe),
        unsafe_allow_html=True,
    )


# ======================================================================
# La funzione che chiama A
# ======================================================================

def render(df: pd.DataFrame, scenario: dict, highlight_ids: list) -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    show_mock_banner()

    st.subheader("Dove abbiamo dati, e dove no")

    risultato = coverage(df)
    evidenziata = disegna_griglia(risultato, scenario)
    disegna_note(risultato, scenario, evidenziata)