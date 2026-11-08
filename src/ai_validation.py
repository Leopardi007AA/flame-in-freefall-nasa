"""src/ai_validation.py - l'AI propone, il codice decide."""
import re
from typing import Literal
import pandas as pd
from pydantic import BaseModel, Field


class AiReply(BaseModel):
    """Schema JSON che Gemini deve rispettare."""
    gravity: Literal["earth", "mars", "moon", "iss"] | None = None
    o2: float | None = Field(default=None, ge=21, le=85)
    pressure: float | None = Field(default=None, ge=8, le=20)
    flow: float | None = Field(default=None, ge=0, le=30)
    highlight_ids: list[str] = []
    answer: str
    citations: list[str] = []


NUM = re.compile(r"(?<![A-Za-z])\d+(?:[.,]\d+)?")   # ignora il 2 di "O2"


def _nums(text: str) -> set[float]:
    return {float(n.replace(",", ".")) for n in NUM.findall(str(text))}


def validate_reply(reply: AiReply, df: pd.DataFrame, scenario: dict):
    """Controlla una risposta dell'AI. Restituisce (risposta pulita o None, problemi)."""
    problems = []
    ids = set(df["id"].astype(str))

    bad = [i for i in reply.citations + reply.highlight_ids if i not in ids]
    if bad:
        problems.append(f"id inesistenti: {bad}")
    reply.citations = [i for i in reply.citations if i in ids]
    reply.highlight_ids = [i for i in reply.highlight_ids if i in ids]

    # ogni numero nel testo deve venire da un record citato o dallo scenario
    allowed = {0.0}
    for k in ("o2", "pressure", "flow"):
        allowed |= _nums(scenario.get(k, ""))
        allowed |= _nums(getattr(reply, k) or "")
    allowed |= {0.16, 0.38, 1.0}
    for _, r in df[df["id"].astype(str).isin(reply.citations)].iterrows():
        for v in r.values:
            allowed |= _nums(v) if not pd.isna(v) else set()
    unknown = sorted(n for n in _nums(reply.answer) if n not in allowed)
    if unknown:
        problems.append(f"numeri non presenti nelle fonti citate: {unknown}")

    no_data = "nessun dato" in reply.answer.lower()
    if not reply.citations and re.search(r"\d", reply.answer) and not no_data:
        problems.append("risposta con numeri ma senza citazioni")

    return (None if problems else reply), problems
