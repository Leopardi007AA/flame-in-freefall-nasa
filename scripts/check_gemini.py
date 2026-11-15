"""Checks the Gemini key and the model, without starting the app.

Usage (from the project folder, with the environment active):
    python scripts/check_gemini.py [model-name]

The key is read from GEMINI_API_KEY (environment variable) or from .streamlit/secrets.toml.
The script never prints the key.
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
        print("ERROR: no key found (GEMINI_API_KEY or .streamlit/secrets.toml).")
        return 1
    model = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL
    print(f"Key found ({len(key)} characters). Model under test: {model}")

    from google import genai
    from google.genai import types
    client = genai.Client(api_key=key)

    print("\n1) Models available with this key:")
    try:
        names = []
        for m in client.models.list():
            actions = getattr(m, "supported_actions", None) or []
            if not actions or "generateContent" in actions:
                names.append(m.name)
        for n in names:
            print("  -", n)
    except Exception as e:
        print(f"  ERROR ({type(e).__name__}): {str(e)[:300]}")

    print("\n2) Simple request:")
    try:
        r = client.models.generate_content(model=model, contents="Reply with only the word: ok")
        print("  reply:", (r.text or "").strip()[:100])
    except Exception as e:
        print(f"  ERROR ({type(e).__name__}): {str(e)[:300]}")
        return 1

    print("\n3) Structured reply (the same mode used by the app):")
    try:
        r = client.models.generate_content(
            model=model,
            contents="Scenario: Mars. Reply with answer='test' and gravity='mars'.",
            config=types.GenerateContentConfig(response_mime_type="application/json",
                                               response_schema=AiReply))
        print("  JSON received:", (r.text or "").strip()[:300])
        print("  schema validation:", AiReply.model_validate_json(r.text))
    except Exception as e:
        print(f"  ERROR ({type(e).__name__}): {str(e)[:300]}")
        return 1

    print("\nAll good: the app can use this key and this model.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
