"""src/ai_engine.py - Copilota AI vincolato ("l'AI propone, il codice decide").

Flusso: domanda + scenario + record del CSV -> Gemini (solo JSON) -> validate_reply() ->
se valida si applica alla dashboard; se no un nuovo tentativo; se ancora no, risposta di riserva.

NOTA: la chiamata a Gemini (ask) NON e' stata provata con una chiave reale. Verifica
nomi dei parametri e del modello con la documentazione di google-genai.
"""
import json
import os
import re
import time
from pathlib import Path

from src.ai_validation import AiReply, validate_reply

ROOT = Path(__file__).resolve().parent.parent
SYSTEM_PROMPT_PATH = ROOT / "src" / "system_prompt.txt"
DEMO_ANSWERS_PATH = ROOT / "src" / "demo_answers.json"
DEFAULT_MODEL = "gemini-2.5-flash"   # verifica con client.models.list() quali modelli hai


def get_api_key(sidebar_value: str = "") -> str:
    """Ordine: st.secrets (online) -> variabile d'ambiente -> valore inserito nella sidebar."""
    try:
        import streamlit as st
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key:
            return str(key)
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY", "") or sidebar_value or ""


def _records_json(df) -> str:
    cols = [c for c in df.columns if c != "note"]
    return df[cols].to_json(orient="records", force_ascii=False)


def ask(question: str, df, scenario: dict, api_key: str, model: str = DEFAULT_MODEL):
    """Interroga Gemini. Restituisce (AiReply validata | None, lista di problemi)."""
    from google import genai            # import tardivo: i test non richiedono la libreria
    from google.genai import types

    system = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    client = genai.Client(api_key=api_key)
    prompt = (f"SCENARIO: {json.dumps(scenario)}\nRECORD:\n{_records_json(df)}\n"
              f"DOMANDA: {question}")
    problems: list[str] = []
    for _ in range(2):
        resp = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system,
                temperature=0.1,
                response_mime_type="application/json",
                response_schema=AiReply,
            ),
        )
        reply, problems = validate_reply(AiReply.model_validate_json(resp.text), df, scenario)
        if reply:
            return reply, []
        prompt += f"\nERRORI DA CORREGGERE: {problems}"
    return None, problems


# ---------------- risposte di riserva ----------------

def normalize_question(q: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", q.lower().replace("'", " ")).strip()


def load_demo_answers(path: Path = DEMO_ANSWERS_PATH) -> dict:
    """Chiave = domanda normalizzata, valore = AiReply come dizionario."""
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {normalize_question(k): v for k, v in raw.items()}


def fallback_answer(question: str, df, scenario: dict, answers: dict | None = None):
    """Risposta di riserva gia' salvata, ri-validata sui dati correnti."""
    answers = load_demo_answers() if answers is None else answers
    entry = answers.get(normalize_question(question))
    if not entry:
        return None
    reply, _ = validate_reply(AiReply(**entry), df, scenario)
    return reply


# ---------------- limite d'uso ----------------

class RateLimiter:
    """Massimo `max_calls` richieste per sessione e `min_interval` secondi tra due richieste."""

    def __init__(self, max_calls: int = 20, min_interval: float = 3.0):
        self.max_calls, self.min_interval = max_calls, min_interval
        self.calls, self.last = 0, 0.0

    def allow(self, now: float | None = None) -> tuple[bool, str]:
        now = time.monotonic() if now is None else now
        if self.calls >= self.max_calls:
            return False, "Limite di richieste per questa sessione raggiunto."
        if self.calls and now - self.last < self.min_interval:
            return False, "Attendi qualche secondo prima della prossima domanda."
        self.calls += 1
        self.last = now
        return True, ""


def answer_question(question: str, df, scenario: dict, api_key: str, model: str = DEFAULT_MODEL) -> dict:
    """Punto d'ingresso per l'app. Restituisce {"source": ai|fallback|error, "reply", "problems"}."""
    problems: list[str] = []
    if api_key:
        try:
            reply, problems = ask(question, df, scenario, api_key, model)
            if reply:
                return {"source": "ai", "reply": reply, "problems": []}
        except Exception as e:  # rete, quota, chiave errata...
            problems = [f"chiamata AI non riuscita ({type(e).__name__}: {str(e)[:200]})"]
    else:
        problems = ["nessuna chiave API configurata"]
    fb = fallback_answer(question, df, scenario)
    if fb:
        return {"source": "fallback", "reply": fb, "problems": problems}
    return {"source": "error", "reply": None, "problems": problems}
