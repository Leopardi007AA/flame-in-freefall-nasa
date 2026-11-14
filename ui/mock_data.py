import pandas as pd
import streamlit as st

# Se True, ogni scheda mostra il banner "Dati di prova".
# Prima della consegna finale va messo a False (Passo 10).
IS_MOCK = False  # True solo in ui/dev_preview.py: la dashboard vera non deve mai mostrare il banner

# Le colonne del "contratto dati": non cambiarle.
COLONNE = [
    "id", "nome", "progetto", "piattaforma", "gravita", "stato_combustibile",
    "combustibili", "o2_min", "o2_max", "pressione_min_psia", "pressione_max_psia",
    "flusso_min_cm_s", "flusso_max_cm_s", "area_sicurezza", "sensori", "sintesi",
    "risultato_chiave", "url_psi", "doi", "dati_grezzi", "fonte_note",
    "verificato_da", "note",
]


def get_mock_data() -> pd.DataFrame:
    # Una cella che non scrivi resta vuota (dato sconosciuto).
    righe = [
        {
            "id": "MOCK-1", "nome": "MOCK-1", "progetto": "BASS", "piattaforma": "ISS",
            "gravita": "microgravita", "stato_combustibile": "solido",
            "combustibili": "PMMA|cotone", "o2_min": 21, "o2_max": 30,
            "pressione_min_psia": 14.7, "pressione_max_psia": 14.7,
            "flusso_min_cm_s": 5, "flusso_max_cm_s": 20,
            "area_sicurezza": "prevenzione|rilevazione", "sensori": "camera|termocoppie",
            "sintesi": "Esperimento finto di prova.", "risultato_chiave": "Dato di prova",
            "url_psi": "https://example.com/mock-1", "dati_grezzi": "si",
        },
        {
            "id": "MOCK-2", "nome": "MOCK-2", "progetto": "FLEX", "piattaforma": "ISS",
            "gravita": "microgravita", "stato_combustibile": "liquido",
            "combustibili": "eptano", "o2_min": 21, "o2_max": 40,
            "pressione_min_psia": 10.2, "pressione_max_psia": 14.7,
            "area_sicurezza": "soppressione", "sensori": "camera",
            "sintesi": "Esperimento finto di prova.",
            "url_psi": "https://example.com/mock-2", "dati_grezzi": "parziale",
        },
        {
            "id": "MOCK-3", "nome": "MOCK-3", "progetto": "ACME", "piattaforma": "Cygnus",
            "gravita": "microgravita", "stato_combustibile": "gassoso",
            "combustibili": "metano", "o2_min": 26.5, "o2_max": 26.5,
            "flusso_min_cm_s": 10, "flusso_max_cm_s": 10,
            "area_sicurezza": "prevenzione", "sintesi": "Esperimento finto di prova.",
            "risultato_chiave": "Dato di prova", "dati_grezzi": "no",
        },
        {
            "id": "MOCK-4", "nome": "MOCK-4", "progetto": "Saffire", "piattaforma": "Cygnus",
            "gravita": "microgravita", "stato_combustibile": "misto",
            "combustibili": "cotone|PMMA", "pressione_min_psia": 14.7,
            "pressione_max_psia": 14.7, "flusso_min_cm_s": 0, "flusso_max_cm_s": 25,
            "area_sicurezza": "prevenzione|soppressione", "sensori": "termocoppie",
            "sintesi": "Esperimento finto: manca l'ossigeno.",
            "url_psi": "https://example.com/mock-4", "dati_grezzi": "si",
        },
        {
            "id": "MOCK-5", "nome": "MOCK-5", "progetto": "altro", "piattaforma": "torre di caduta",
            "gravita": "1g", "stato_combustibile": "solido",
            "combustibili": "PMMA", "o2_min": 21, "o2_max": 60,
            "pressione_min_psia": 14.7, "pressione_max_psia": 14.7,
            "area_sicurezza": "rilevazione", "sensori": "camera|termocoppie",
            "sintesi": "Esperimento finto a gravita terrestre.",
            "url_psi": "https://example.com/mock-5", "dati_grezzi": "si",
        },
        {
            "id": "MOCK-6", "nome": "MOCK-6", "progetto": "SAME", "piattaforma": "volo parabolico",
            "gravita": "mista", "stato_combustibile": "fumo",
            "o2_min": 21, "o2_max": 21, "sensori": "camera",
            "sintesi": "Esperimento finto: mancano combustibili e flusso.",
            "dati_grezzi": "no",
        },
    ]
    return pd.DataFrame(righe, columns=COLONNE)


def show_mock_banner() -> None:
    if IS_MOCK:
        st.markdown(
            '<div style="border:1px solid #ff8a4c; background:rgba(255,138,76,.15); border-radius:16px; padding:12px 16px; color:#ffb347; font-weight:600;">⚠ DATI DI PROVA, NON REALI</div>',
            unsafe_allow_html=True,
        )        
        
            
        
def get_mock_tables() -> dict:
    """Due tabelle finte per provare l'esploratore. Una colonna è vuota apposta."""
    bass = pd.DataFrame({
        "tempo_s": [0, 5, 10, 15, 20, 25, 30, 35],
        "o2_percent": [21, 21, 30, 30, 40, 40, 50, 50],
        "velocita_mm_s": [1.2, 1.5, 2.1, None, 3.0, 3.4, None, 4.2],
        "combustibile": ["PMMA", "PMMA", "cotone", "cotone", "PMMA", "cotone", "PMMA", "cotone"],
        "colonna_vuota": [None] * 8,
    })
    bass.attrs["file"] = "MOCK_bass2.csv"

    flex = pd.DataFrame({
        "pressione_psia": [10.2, 10.2, 12.0, 12.0, 14.7, 14.7],
        "flusso_cm_s": [5, 10, 5, 10, 5, 10],
        "altezza_fiamma_mm": [12.5, 14.0, None, 15.2, 18.1, 19.3],
        "esito": ["fiamma", "fiamma", "spenta", "fiamma", "fiamma", "fiamma"],
    })
    flex.attrs["file"] = "MOCK_flex.csv"

    return {"MOCK BASS-II": bass, "MOCK FLEX": flex}