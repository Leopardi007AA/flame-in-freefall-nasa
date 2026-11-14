"""src/scoring.py - punteggio di rilevanza 0-100 per scenario. Dato mancante = 0 punti."""
import pandas as pd

G_EXP = {"microgravita": 0.0, "1g": 1.0}      # gravita' dell'esperimento (in g)
G_SCEN = {"earth": 1.0, "mars": 0.38, "moon": 0.16, "iss": 0.0}


def _closeness(value, lo, hi, full, scale):
    """full punti se value e' nell'intervallo, poi cala linearmente fino a 0 a distanza `scale`."""
    if pd.isna(lo) and pd.isna(hi):
        return 0.0
    lo = hi if pd.isna(lo) else lo
    hi = lo if pd.isna(hi) else hi
    dist = 0 if lo <= value <= hi else min(abs(value - lo), abs(value - hi))
    return full * max(0.0, 1 - dist / scale)


def score_row(row: pd.Series, sc: dict) -> tuple[int, list[str]]:
    """sc = {"gravity": "mars", "o2": 30, "pressure": 10.2, "flow": 5}"""
    parts, why = [], []

    g = G_EXP.get(row["gravita"])
    if g is None:
        pts = 10.0 if row["gravita"] == "mista" else 0.0
    else:
        pts = 30 * max(0.0, 1 - abs(g - G_SCEN[sc["gravity"]]))
    parts.append(pts)
    why.append(f"gravita {pts:.0f}/30")

    for label, full, scale, a, b, v in (
        ("ossigeno", 25, 15, "o2_min", "o2_max", sc["o2"]),
        ("pressione", 15, 5, "pressione_min_psia", "pressione_max_psia", sc["pressure"]),
        ("flusso", 10, 10, "flusso_min_cm_s", "flusso_max_cm_s", sc["flow"]),
    ):
        pts = _closeness(v, row[a], row[b], full, scale)
        parts.append(pts)
        nodata = pd.isna(row[a]) and pd.isna(row[b])
        why.append(f"{label} 0/{full} (nessun dato)" if nodata else f"{label} {pts:.0f}/{full}")

    raw = {"si": 10, "parziale": 5}.get(row["dati_grezzi"], 0)
    parts.append(raw)
    why.append(f"dati grezzi {raw}/10")

    valid = ("prevenzione", "rilevazione", "soppressione")
    areas = [a for a in str(row["area_sicurezza"]).split("|") if a in valid]
    pts = 10 * len(set(areas)) / 3
    parts.append(pts)
    why.append(f"aree sicurezza {pts:.0f}/10")

    return round(sum(parts)), why


def rank(df: pd.DataFrame, sc: dict) -> pd.DataFrame:
    out = df.copy()
    res = out.apply(lambda r: score_row(r, sc), axis=1)
    out["score"] = [r[0] for r in res]
    out["why"] = [r[1] for r in res]
    return out.sort_values("score", ascending=False).reset_index(drop=True)
