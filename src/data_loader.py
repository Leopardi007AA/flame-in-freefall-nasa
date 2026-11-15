"""src/data_loader.py - loads and normalizes the experiments table.

If data/investigations.csv (delivered by role B) does not exist yet, it uses the FAKE
development data in dev/investigations_mock.csv: the fake rows have a name that starts with MOCK
and the app shows a banner as long as there are any.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
MOCK_PATH = ROOT / "dev" / "investigations_mock.csv"

NUM_COLS = ["o2_min", "o2_max", "pressione_min_psia", "pressione_max_psia",
            "flusso_min_cm_s", "flusso_max_cm_s"]


def load_investigations(path: Path | None = None) -> pd.DataFrame:
    """One row per experiment. Empty cells = NaN (never 0). `path` is for the tests."""
    path = path or DATA_DIR / "investigations.csv"
    if not path.exists():
        path = MOCK_PATH
    df = pd.read_csv(path, encoding="utf-8")
    for c in NUM_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in df.columns.difference(NUM_COLS):
        df[c] = df[c].astype("string").str.strip()
    return df


def is_mock(df: pd.DataFrame) -> bool:
    """True if the table has at least one test row (name that starts with MOCK)."""
    return bool(df["nome"].fillna("").str.upper().str.startswith("MOCK").any())


def load_papers() -> list[dict]:
    """NTRS papers curated by B (data/papers.json). Empty list if the file does not exist yet."""
    import json
    path = DATA_DIR / "papers.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))
