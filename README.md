# Flame in Freefall

Dashboard per la sfida **Flame in Freefall** del NASA Space Apps Challenge 2026: riassume, ordina e
spiega gli esperimenti NASA sulla combustione in microgravità, per la sicurezza antincendio su Luna e Marte.

L'utente sceglie uno scenario (gravità, ossigeno, pressione, flusso d'aria); un **Copilota AI** comanda
la dashboard, ma **non può inventare dati**: ogni risposta viene validata dal codice (id esistenti, numeri
presenti nelle fonti citate) e dove i dati non esistono lo dichiara.

> Progetto indipendente, non affiliato né approvato dalla NASA. Le fiamme sono una resa illustrativa,
> non una simulazione fisica.

## Avvio

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Chiave Gemini (solo per il Copilota): variabile d'ambiente `GEMINI_API_KEY`, oppure
`.streamlit/secrets.toml` con `GEMINI_API_KEY = "..."`, oppure il campo nella sidebar.
**Non committare mai la chiave** (`.streamlit/secrets.toml` è nel `.gitignore`).

## Test

```bash
python -m unittest discover -s tests -v
```

I test non richiedono Streamlit né Gemini (usano un Streamlit finto). Non verificano l'aspetto grafico.

## Struttura e responsabilità

| Cartella / file | Ruolo | Contenuto |
|---|---|---|
| `app.py`, `src/`, `ui/flame_lab.py` | A | guscio dell'app, AI, punteggi, fiamma animata |
| `ui/theme.py`, `ui/components.py`, `ui/plotly_theme.py`, `ui/tabs/` | C | tema, componenti, schede Confronto / Lacune / Dati reali |
| `data/`, `scripts/fetch_ntrs.py` | B | `investigations.csv`, `papers.json`, `raw/`, `SOURCES.md` |
| `dev/investigations_mock.csv` | A | dati **finti** di sviluppo, usati solo se manca `data/investigations.csv` |

Contratti tra i ruoli: schema del CSV (colonne congelate v1, controllate da
`python scripts/validate_csv.py`), `rank(df, scenario)`, `compare.render(df, scenario, highlight_ids)`,
`gaps.render(df, scenario, highlight_ids)`, `real_data.render(tables)`.

## Regole sui dati

- Cella vuota = dato sconosciuto. Mai 0, mai stime.
- Ogni numero mostrato ha una fonte o un'etichetta di provenienza (REALE, MODELLO, ILLUSTRATIVO, NESSUN DATO).
- Il punteggio di rilevanza è un **modello** con pesi dichiarati in `src/scoring.py`.

## Uso dell'AI e risorse / AI use and resources

**Italiano.** Il Copilota dell'app usa il modello Gemini di Google (API `google-genai`); le sue risposte
sono validate dal codice (id e numeri devono comparire nei record citati). Il codice di questo repository
(app, test, script, Flame Lab) è stato scritto con l'assistenza di Claude (Anthropic) e rivisto dal team.
Le descrizioni e le sintesi dei dati possono contenere testo generato o riassunto con AI e vanno
verificate sulle fonti indicate in `data/SOURCES.md`. Le immagini della fiamma sono generate da codice
(CSS), non da modelli di immagini. Nessun logo o elemento grafico NASA è utilizzato.

**English.** The in-app Copilot uses Google's Gemini model (`google-genai` API); every answer is validated
in code (record ids and numbers must appear in the cited records). The code in this repository (app, tests,
scripts, Flame Lab) was written with the assistance of Claude (Anthropic) and reviewed by the team. Data
summaries may contain AI-generated or AI-summarised text and must be checked against the sources listed in
`data/SOURCES.md`. The flame is rendered by CSS code, not by an image-generation model. No NASA logo or
design element is used.

External resources: Streamlit, pandas, plotly, pydantic, google-genai, requests (see `requirements.txt`);
NASA Physical Sciences Informatics (psi.nasa.gov) and NASA NTRS (ntrs.nasa.gov) as data sources.
