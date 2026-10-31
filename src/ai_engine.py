import json
from google import genai
from google.genai import types

def genera_modifica_dashboard(prompt_utente: str, stato_attuale: dict) -> dict:
    """
    Invia il contesto attuale dell'applicazione e le richieste dell'utente a Gemini.
    Restituisce un dizionario contenente le modifiche da applicare.
    """
    client = genai.Client()
    
    system_instruction = """
    Sei un assistente specializzato nello sviluppo di dashboard per la NASA Space Apps Challenge.
    Il tuo compito è analizzare la richiesta dell'utente e lo stato attuale dei dati/grafici
    e restituire un JSON valido con le modifiche da applicare alla dashboard.
    
    Formato risposta JSON richiesto:
    {
        "spiegazione": "Descrizione sintetica delle modifiche apportate",
        "tipo_grafico": "bar | line | scatter | pie",
        "titolo_grafico": "Titolo del grafico",
        "codice_aggiornato": "Codice Python/Streamlit generato"
    }
    """
    
    prompt = f"""
    Stato attuale della dashboard: {json.dumps(stato_attuale)}
    Richiesta dell'utente: {prompt_utente}
    """
    
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
            response_mime_type="application/json"
        ),
    )
    
    return json.loads(response.text)