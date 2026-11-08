"""src/data_loader.py - carica e normalizza la tabella degli esperimenti.

Se data/investigations.csv (consegnato dal ruolo B) non esiste ancora, usa i dati
FINTI di sviluppo in dev/investigations_mock.csv: le righe finte hanno nome che inizia
con MOCK e l'app mostra un banner finche' ce ne sono.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
MOCK_PATH = ROOT / "dev" / "investigations_mock.csv"

NUM_COLS = ["o2_min", "o2_max", "pressione_min_psia", "pressione_max_psia",
            "flusso_min_cm_s", "flusso_max_cm_s"]


def load_investigations() -> pd.DataFrame:
    """Una riga per esperimento. Celle vuote = NaN (mai 0)."""
    path = DATA_DIR / "investigations.csv"
    if not path.exists():
        path = MOCK_PATH
    df = pd.read_csv(path, encoding="utf-8")
    for c in NUM_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in df.columns.difference(NUM_COLS):
        df[c] = df[c].astype("string").str.strip()
    return df


def is_mock(df: pd.DataFrame) -> bool:
    """Vero se nella tabella c'e' almeno una riga di prova (nome che inizia con MOCK)."""
    return bool(df["nome"].fillna("").str.upper().str.startswith("MOCK").any())


def load_papers() -> list[dict]:
    """Articoli NTRS curati da B (data/papers.json). Lista vuota se il file non c'e' ancora."""
    import json
    path = DATA_DIR / "papers.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))
