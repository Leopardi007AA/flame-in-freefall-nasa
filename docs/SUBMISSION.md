# Submission sheet (English) — Flame in Freefall

Copy each block into the Project Tab on the team page. Submission closes Sunday 15 November, 11:59 PM local time.

## Project title
Flame in Freefall: an AI-guided dashboard of NASA microgravity combustion experiments

## One-sentence summary
A dashboard that ranks NASA microgravity combustion experiments for a chosen scenario (gravity, oxygen, pressure, airflow) and uses an AI Copilot that is not allowed to invent data: every answer is validated against the source records, and where no data exists the app says so.

## What it does
- **Flame Lab:** an illustrative animated flame (not a physical simulation) that reacts to gravity, oxygen, pressure and airflow.
- **Experiment ranking:** a transparent relevance score (our own model, with declared weights) for each NASA PSI investigation in the table.
- **AI Copilot (Google Gemini):** answers in natural language and can drive the dashboard ("Show me the Moon with 26.5% oxygen"). The AI proposes, the code decides: record ids and every number in an answer are checked against the cited records; rejected answers are retried and then replaced by pre-validated fallback answers.
- **Gap analysis:** shows what is *not* known. In the current table no experiment declares a gravity between 0 g and 1 g, and most oxygen, pressure and airflow values are missing from the sources we could verify.
- **Real data tab:** shows original NASA tables only when they are real; sample files are never presented as data.

## Why it matters
Fire safety for Moon and Mars habitats depends on how flames behave at 0.16 g and 0.38 g, a regime that existing experiments barely cover. The dashboard makes that gap visible instead of hiding it.

## How we used NASA data
NASA Physical Sciences Informatics (https://psi.nasa.gov/) investigation pages and NASA Technical Reports Server (https://ntrs.nasa.gov/) papers. Each row of `data/investigations.csv` records its source; an empty cell means unknown (never zero or an estimate). Values taken from papers are marked "to verify" in the notes.

## AI use disclosure
- Gemini (Google, `google-genai` API) powers the in-app Copilot; its output is validated by code before being shown.
- The code of this repository was written with the assistance of Claude (Anthropic) and reviewed by the team.
- Data summaries may contain AI-generated or AI-summarised text and should be checked against the sources listed in `data/SOURCES.md`.
- The flame is drawn by CSS code, not by an image-generation model. No NASA logo or branding is used.

## Tools and resources
Python, Streamlit, pandas, Plotly, pydantic, google-genai, requests; hosted on Streamlit Community Cloud. Data: NASA PSI and NTRS. Full list: `README.md` and `data/CREDITS.md`.

## Links (fill in before submitting)
- Live app: https://flame-in-freefall-nasa-fzgfghjn5vfzmfhukvnt58.streamlit.app/
- Code: https://github.com/Leopardi007AA/flame-in-freefall-nasa
- Demo (video up to 30 s or slides): <ADD LINK — public, no password>

## Disclaimer
Independent project for the NASA Space Apps Challenge; not affiliated with or endorsed by NASA.
