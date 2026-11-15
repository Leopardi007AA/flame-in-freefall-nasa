"""src/ai_engine.py - constrained AI Copilot ("the AI proposes, the code decides").

Flow: question + scenario + CSV records -> Gemini (JSON only) -> validate_reply() ->
if valid it is applied to the dashboard; if not, a new attempt; if still not, a fallback answer.

NOTE: the Gemini call (ask) has NOT been tried with a real key. Check the parameter
names and the model against the google-genai documentation.
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
DEFAULT_MODEL = "gemini-3.8-flash"   # check with client.models.list() which models you have
FALLBACK_MODELS = ["gemini-3.7-flash", "gemini-3.5-flash-lite"]   # used if the main one is overloaded
RETRY_WAITS = [1.5]                                           # seconds between attempts on 503/429


def get_api_key(sidebar_value: str = "") -> str:
    """Order: st.secrets (online) -> environment variable -> value typed in the sidebar."""
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


def _generate(client, types, model, prompt, system):
    """One call to Gemini; on 503/429 it retries, then tries the fallback models."""
    last = None
    for m in [model] + [x for x in FALLBACK_MODELS if x != model]:
        for wait in [0.0] + RETRY_WAITS:
            if wait:
                time.sleep(wait)
            try:
                return client.models.generate_content(
                    model=m, contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system, temperature=0.1,
                        response_mime_type="application/json", response_schema=AiReply))
            except Exception as e:
                code = getattr(e, "code", None)
                if code not in (429, 500, 503, 504):
                    raise
                last = e
    raise last


def ask(question: str, df, scenario: dict, api_key: str, model: str = DEFAULT_MODEL):
    """Queries Gemini. Returns (validated AiReply | None, list of problems)."""
    from google import genai            # late import: the tests do not require the library
    from google.genai import types

    system = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    client = genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=60000))  # 60 s per call
    prompt = (f"SCENARIO: {json.dumps(scenario)}\nRECORDS:\n{_records_json(df)}\n"
              f"QUESTION: {question}")
    problems: list[str] = []
    for _ in range(2):
        resp = _generate(client, types, model, prompt, system)
        reply, problems = validate_reply(AiReply.model_validate_json(resp.text), df, scenario)
        if reply:
            return reply, []
        prompt += f"\nERRORS TO FIX: {problems}"
    return None, problems


# ---------------- fallback answers ----------------

def normalize_question(q: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", q.lower().replace("'", " ")).strip()


def load_demo_answers(path: Path = DEMO_ANSWERS_PATH) -> dict:
    """Key = normalized question, value = AiReply as a dictionary."""
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {normalize_question(k): v for k, v in raw.items()}


def fallback_answer(question: str, df, scenario: dict, answers: dict | None = None):
    """Already-saved fallback answer, re-validated on the current data."""
    answers = load_demo_answers() if answers is None else answers
    entry = answers.get(normalize_question(question))
    if not entry:
        return None
    reply, _ = validate_reply(AiReply(**entry), df, scenario)
    return reply


# ---------------- usage limit ----------------

class RateLimiter:
    """At most `max_calls` requests per session and `min_interval` seconds between two requests."""

    def __init__(self, max_calls: int = 20, min_interval: float = 3.0):
        self.max_calls, self.min_interval = max_calls, min_interval
        self.calls, self.last = 0, 0.0

    def allow(self, now: float | None = None) -> tuple[bool, str]:
        now = time.monotonic() if now is None else now
        if self.calls >= self.max_calls:
            return False, "Request limit for this session reached."
        if self.calls and now - self.last < self.min_interval:
            return False, "Please wait a few seconds before the next question."
        self.calls += 1
        self.last = now
        return True, ""


def answer_question(question: str, df, scenario: dict, api_key: str, model: str = DEFAULT_MODEL) -> dict:
    """Entry point for the app. Returns {"source": ai|fallback|error, "reply", "problems"}."""
    problems: list[str] = []
    if api_key:
        try:
            reply, problems = ask(question, df, scenario, api_key, model)
            if reply:
                return {"source": "ai", "reply": reply, "problems": []}
        except Exception as e:  # network, quota, wrong key...
            problems = [f"AI call failed ({type(e).__name__}: {str(e)[:200]})"]
    else:
        problems = ["no API key configured"]
    fb = fallback_answer(question, df, scenario)
    if fb:
        return {"source": "fallback", "reply": fb, "problems": problems}
    return {"source": "error", "reply": None, "problems": problems}
