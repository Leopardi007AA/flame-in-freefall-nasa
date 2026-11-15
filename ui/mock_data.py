import pandas as pd
import streamlit as st

# If True, every tab shows the "Test data" banner.
# Before the final delivery it must be set to False (Step 10).
IS_MOCK = False  # True only in ui/dev_preview.py: the real dashboard must never show the banner

# The columns of the "data contract": do not change them.
COLONNE = [
    "id", "nome", "progetto", "piattaforma", "gravita", "stato_combustibile",
    "combustibili", "o2_min", "o2_max", "pressione_min_psia", "pressione_max_psia",
    "flusso_min_cm_s", "flusso_max_cm_s", "area_sicurezza", "sensori", "sintesi",
    "risultato_chiave", "url_psi", "doi", "dati_grezzi", "fonte_note",
    "verificato_da", "note",
]


def get_mock_data() -> pd.DataFrame:
    # A cell that you do not write stays empty (unknown value).
    righe = [
        {
            "id": "MOCK-1", "nome": "MOCK-1", "progetto": "BASS", "piattaforma": "ISS",
            "gravita": "microgravita", "stato_combustibile": "solido",
            "combustibili": "PMMA|cotton", "o2_min": 21, "o2_max": 30,
            "pressione_min_psia": 14.7, "pressione_max_psia": 14.7,
            "flusso_min_cm_s": 5, "flusso_max_cm_s": 20,
            "area_sicurezza": "prevenzione|rilevazione", "sensori": "camera|thermocouples",
            "sintesi": "Fake test experiment.", "risultato_chiave": "Test data",
            "url_psi": "https://example.com/mock-1", "dati_grezzi": "si",
        },
        {
            "id": "MOCK-2", "nome": "MOCK-2", "progetto": "FLEX", "piattaforma": "ISS",
            "gravita": "microgravita", "stato_combustibile": "liquido",
            "combustibili": "heptane", "o2_min": 21, "o2_max": 40,
            "pressione_min_psia": 10.2, "pressione_max_psia": 14.7,
            "area_sicurezza": "soppressione", "sensori": "camera",
            "sintesi": "Fake test experiment.",
            "url_psi": "https://example.com/mock-2", "dati_grezzi": "parziale",
        },
        {
            "id": "MOCK-3", "nome": "MOCK-3", "progetto": "ACME", "piattaforma": "Cygnus",
            "gravita": "microgravita", "stato_combustibile": "gassoso",
            "combustibili": "methane", "o2_min": 26.5, "o2_max": 26.5,
            "flusso_min_cm_s": 10, "flusso_max_cm_s": 10,
            "area_sicurezza": "prevenzione", "sintesi": "Fake test experiment.",
            "risultato_chiave": "Test data", "dati_grezzi": "no",
        },
        {
            "id": "MOCK-4", "nome": "MOCK-4", "progetto": "Saffire", "piattaforma": "Cygnus",
            "gravita": "microgravita", "stato_combustibile": "misto",
            "combustibili": "cotton|PMMA", "pressione_min_psia": 14.7,
            "pressione_max_psia": 14.7, "flusso_min_cm_s": 0, "flusso_max_cm_s": 25,
            "area_sicurezza": "prevenzione|soppressione", "sensori": "thermocouples",
            "sintesi": "Fake experiment: oxygen is missing.",
            "url_psi": "https://example.com/mock-4", "dati_grezzi": "si",
        },
        {
            "id": "MOCK-5", "nome": "MOCK-5", "progetto": "other", "piattaforma": "drop tower",
            "gravita": "1g", "stato_combustibile": "solido",
            "combustibili": "PMMA", "o2_min": 21, "o2_max": 60,
            "pressione_min_psia": 14.7, "pressione_max_psia": 14.7,
            "area_sicurezza": "rilevazione", "sensori": "camera|thermocouples",
            "sintesi": "Fake experiment at Earth gravity.",
            "url_psi": "https://example.com/mock-5", "dati_grezzi": "si",
        },
        {
            "id": "MOCK-6", "nome": "MOCK-6", "progetto": "SAME", "piattaforma": "parabolic flight",
            "gravita": "mista", "stato_combustibile": "fumo",
            "o2_min": 21, "o2_max": 21, "sensori": "camera",
            "sintesi": "Fake experiment: fuels and airflow are missing.",
            "dati_grezzi": "no",
        },
    ]
    return pd.DataFrame(righe, columns=COLONNE)


def show_mock_banner() -> None:
    if IS_MOCK:
        st.markdown(
            '<div style="border:1px solid #ff8a4c; background:rgba(255,138,76,.15); border-radius:16px; padding:12px 16px; color:#ffb347; font-weight:600;">⚠ TEST DATA, NOT REAL</div>',
            unsafe_allow_html=True,
        )


def get_mock_tables() -> dict:
    """Two fake tables to try the explorer. One column is empty on purpose."""
    bass = pd.DataFrame({
        "time_s": [0, 5, 10, 15, 20, 25, 30, 35],
        "o2_percent": [21, 21, 30, 30, 40, 40, 50, 50],
        "speed_mm_s": [1.2, 1.5, 2.1, None, 3.0, 3.4, None, 4.2],
        "fuel": ["PMMA", "PMMA", "cotton", "cotton", "PMMA", "cotton", "PMMA", "cotton"],
        "empty_column": [None] * 8,
    })
    bass.attrs["file"] = "MOCK_bass2.csv"

    flex = pd.DataFrame({
        "pressure_psia": [10.2, 10.2, 12.0, 12.0, 14.7, 14.7],
        "flow_cm_s": [5, 10, 5, 10, 5, 10],
        "flame_height_mm": [12.5, 14.0, None, 15.2, 18.1, 19.3],
        "outcome": ["flame", "flame", "extinguished", "flame", "flame", "flame"],
    })
    flex.attrs["file"] = "MOCK_flex.csv"

    return {"MOCK BASS-II": bass, "MOCK FLEX": flex}
