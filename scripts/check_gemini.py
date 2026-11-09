"""Controlla la chiave Gemini e il modello, senza avviare l'app.

Uso (dalla cartella del progetto, con l'ambiente attivo):
    python scripts/check_gemini.py [nome-modello]

La chiave si legge da GEMINI_API_KEY (variabile d'ambiente) oppure da .streamlit/secrets.toml.
Lo script non stampa mai la chiave.
"""
import os
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def read_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "")
    if key:
        return key
    secrets = ROOT / ".streamlit" / "secrets.toml"
    if secrets.exists():
        return str(tomllib.loads(secrets.read_text(encoding="utf-8")).get("GEMINI_API_KEY", ""))
    return ""


def main() -> int:
    from src.ai_engine import DEFAULT_MODEL
    from src.ai_validation import AiReply

    key = read_key()
    if not key:
        print("ERRORE: nessuna chiave trovata (GEMINI_API_KEY o .streamlit/secrets.toml).")
        return 1
    model = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL
    print(f"Chiave trovata ({len(key)} caratteri). Modello in prova: {model}")

    from google import genai
    from google.genai import types
    client = genai.Client(api_key=key)

    print("\n1) Modelli disponibili con questa chiave:")
    try:
        names = []
        for m in client.models.list():
            actions = getattr(m, "supported_actions", None) or []
            if not actions or "generateContent" in actions:
                names.append(m.name)
        for n in names:
            print("  -", n)
    except Exception as e:
        print(f"  ERRORE ({type(e).__name__}): {str(e)[:300]}")

    print("\n2) Richiesta semplice:")
    try:
        r = client.models.generate_content(model=model, contents="Rispondi solo con la parola: ok")
        print("  risposta:", (r.text or "").strip()[:100])
    except Exception as e:
        print(f"  ERRORE ({type(e).__name__}): {str(e)[:300]}")
        return 1

    print("\n3) Risposta strutturata (la stessa modalita' usata dall'app):")
    try:
        r = client.models.generate_content(
            model=model,
            contents="Scenario: Marte. Rispondi con answer='prova' e gravity='mars'.",
            config=types.GenerateContentConfig(response_mime_type="application/json",
                                               response_schema=AiReply))
        print("  JSON ricevuto:", (r.text or "").strip()[:300])
        print("  validazione schema:", AiReply.model_validate_json(r.text))
    except Exception as e:
        print(f"  ERRORE ({type(e).__name__}): {str(e)[:300]}")
        return 1

    print("\nTutto in ordine: l'app puo' usare questa chiave e questo modello.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
