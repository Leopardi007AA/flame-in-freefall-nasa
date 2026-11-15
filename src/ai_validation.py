"""src/ai_validation.py - the AI proposes, the code decides."""
import re
from typing import Literal
import pandas as pd
from pydantic import BaseModel, Field


class AiReply(BaseModel):
    """JSON schema that Gemini must follow."""
    gravity: Literal["earth", "mars", "moon", "iss"] | None = None
    o2: float | None = Field(default=None, ge=21, le=85)
    pressure: float | None = Field(default=None, ge=8, le=20)
    flow: float | None = Field(default=None, ge=0, le=30)
    highlight_ids: list[str] = []
    answer: str
    citations: list[str] = []


NUM = re.compile(r"(?<![A-Za-z])\d+(?:[.,]\d+)?")   # ignores the 2 in "O2"

# An answer that says there is no data may contain numbers without citations.
# The system prompt asks for "No data"; the Italian phrase is also accepted so that an
# answer written in Italian (e.g. by the model, or an old saved one) is not wrongly rejected.
NO_DATA = re.compile(r"\bno data\b|\bnessun dato\b", re.IGNORECASE)


def _nums(text: str) -> set[float]:
    return {float(n.replace(",", ".")) for n in NUM.findall(str(text))}


def validate_reply(reply: AiReply, df: pd.DataFrame, scenario: dict):
    """Checks an AI reply. Returns (clean reply or None, problems)."""
    problems = []
    ids = set(df["id"].astype(str))

    bad = [i for i in reply.citations + reply.highlight_ids if i not in ids]
    if bad:
        problems.append(f"nonexistent ids: {bad}")
    reply.citations = [i for i in reply.citations if i in ids]
    reply.highlight_ids = [i for i in reply.highlight_ids if i in ids]

    # every number in the text must come from a cited record or from the scenario
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
        problems.append(f"numbers not present in the cited sources: {unknown}")

    no_data = bool(NO_DATA.search(reply.answer))
    if not reply.citations and re.search(r"\d", reply.answer) and not no_data:
        problems.append("answer with numbers but no citations")

    return (None if problems else reply), problems
