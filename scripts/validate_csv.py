"""scripts/validate_csv.py - controlla data/investigations.csv
Uso: python scripts/validate_csv.py"""
import sys
from pathlib import Path
import pandas as pd

PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/investigations.csv")
COLS = ["id", "nome", "progetto", "piattaforma", "gravita", "stato_combustibile",
        "combustibili", "o2_min", "o2_max", "pressione_min_psia", "pressione_max_psia",
        "flusso_min_cm_s", "flusso_max_cm_s", "area_sicurezza", "sensori", "sintesi",
        "risultato_chiave", "url_psi", "doi", "dati_grezzi", "fonte_note",
        "verificato_da", "note"]
ALLOWED = {"gravita": {"microgravita", "1g", "mista"},
           "stato_combustibile": {"solido", "liquido", "gassoso", "misto", "fumo"},
           "dati_grezzi": {"si", "no", "parziale"}}
RANGES = {"o2": ("o2_min", "o2_max", 0, 100),
          "pressione": ("pressione_min_psia", "pressione_max_psia", 0, 30),
          "flusso": ("flusso_min_cm_s", "flusso_max_cm_s", 0, 100)}
errors = []

df = pd.read_csv(PATH, encoding="utf-8")
if list(df.columns) != COLS:
    errors.append(f"Colonne diverse dallo schema v1. Attese: {COLS}")
else:
    if df["id"].duplicated().any():
        dup = df.loc[df["id"].duplicated(), "id"].astype(str)
        errors.append("id duplicati: " + ", ".join(dup))
    for i, r in df.iterrows():
        row = f"riga {i + 2} ({r['id']})"
        for col in ("id", "nome", "url_psi", "fonte_note", "verificato_da"):
            if pd.isna(r[col]):
                errors.append(f"{row}: manca {col}")
        for col, ok in ALLOWED.items():
            if not pd.isna(r[col]) and r[col] not in ok:
                errors.append(f"{row}: {col}='{r[col]}' non ammesso {sorted(ok)}")
        for key, (cmin, cmax, lo, hi) in RANGES.items():
            mn = pd.to_numeric(r[cmin], errors="coerce")
            mx = pd.to_numeric(r[cmax], errors="coerce")
            for val in (mn, mx):
                if not pd.isna(val) and not lo <= val <= hi:
                    errors.append(f"{row}: valore {key} fuori scala ({val})")
            if not pd.isna(mn) and not pd.isna(mx) and mn > mx:
                errors.append(f"{row}: {key} min > max")
        if not pd.isna(r["sintesi"]) and len(str(r["sintesi"])) > 280:
            errors.append(f"{row}: sintesi oltre 280 caratteri")
        if not pd.isna(r["url_psi"]) and not str(r["url_psi"]).startswith("https://"):
            errors.append(f"{row}: url_psi deve iniziare con https://")

print(f"{len(df)} righe controllate.")
if errors:
    print("PROBLEMI TROVATI:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("Tutto in ordine.")
