import os
import glob
from google import genai
from google.genai import types

def load_context_from_data():
    """Legge tutti i file di testo e PDF dalla cartella data/."""
    context = ""
    # Lettura file .txt
    for file_path in glob.glob("data/*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            context += f"\n--- Fonte: {file_path} ---\n" + f.read()
    return context

def ask_nasa_ai(prompt: str, api_key: str) -> str:
    """Interroga Gemini fornendo il contesto sui dati di combustione."""
    if not api_key:
        return "Inserisci la tua API Key di Gemini nella sidebar per attivare l'AI."

    client = genai.Client(api_key=api_key)
    context_data = load_context_from_data()

    system_instruction = (
        "Sei un assistente scientifico della NASA specializzato in combustione in microgravità. "
        "Usa il seguente contesto tecnico estratto dai database e report NASA per rispondere "
        "alle domande dell'utente sulla sicurezza antincendio in habitat spaziali (Luna/Marte). "
        "Sii preciso, sintetico e professionale.\n\n"
        f"CONTESTO DATI NASA:\n{context_data}"
    )

    try:
        response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.2,
    ),
)
        return response.text
    except Exception as e:
        return f"Errore durante la chiamata AI: {str(e)}"