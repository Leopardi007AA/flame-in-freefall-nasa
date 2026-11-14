# Submission sheet (English) — Flame in Freefall

Field names follow the 2026 Project Submission form. Copy each block into the Project tab (My Team → Project → Edit). Click **Save Progress** often. Submission closes Sunday 15 November, 11:59 PM local time of the team's event.

## Project Name
Flame in Freefall

## High-Level Project Summary
Flame in Freefall is a dashboard of NASA microgravity combustion experiments for fire safety on the Moon and Mars. The user picks a scenario (gravity, oxygen, pressure, airflow); the app ranks the NASA PSI investigations by relevance, animates an illustrative flame, and shows what is NOT known. An AI Copilot (Google Gemini) answers questions and drives the dashboard, but it is not allowed to invent data: every record id and number in an answer is checked by code against the source records, and where no data exists the app says "no data". It matters because Moon (0.16 g) and Mars (0.38 g) habitats depend on flame behaviour in a gravity range that no investigation in our table covers.

## Link to Project Demo
<ADD LINK — public video ≤ 30 s with English subtitles, or ≤ 7 slides; no password>

## Link to Final Project
Live app: https://flame-in-freefall-nasa-fzgfghjn5vfzmfhukvnt58.streamlit.app/
Code: https://github.com/Leopardi007AA/flame-in-freefall-nasa

## Detailed Project Description
**What it does**
- **Flame Lab:** an illustrative animated flame (not a physical simulation) that reacts to gravity, oxygen, pressure and airflow.
- **Experiment ranking:** a transparent relevance score (our own model, with declared weights: gravity 30, oxygen 25, pressure 15, airflow 10, raw data 10, safety areas 10; missing data scores 0) for each of the 19 NASA PSI investigations in our table.
- **AI Copilot:** natural-language answers that can also set the scenario ("Show me Mars with 30% oxygen"). The AI proposes, the code decides: ids and numbers are validated, rejected answers are retried and then replaced by pre-validated fallback answers.
- **Gap analysis:** shows what is *not* known. All 19 investigations are in microgravity: none covers gravity between 0 g and 1 g. Oxygen, pressure and airflow values are declared for only part of them; the rest are left empty, never estimated.
- **Real data tab:** shows original NASA tables only when they are real; sample files are never presented as data.

**How it works.** Python and Streamlit app. Data lives in `data/investigations.csv` (one row per PSI investigation, schema validated by `scripts/validate_csv.py`; an empty cell means unknown). Scoring in `src/scoring.py`; Copilot and validation in `src/ai_engine.py` and `src/ai_validation.py`.

**Tools.** Python, Streamlit, pandas, Plotly, pydantic, google-genai, requests; hosted on Streamlit Community Cloud.

## Use of Super Intelligence (SI)
- Google Gemini (`google-genai` API) powers the in-app Copilot; its output is validated by code before it is shown.
- The code of this repository and parts of the data summaries were written with the assistance of an AI assistant (Claude, Anthropic) and reviewed by the team. Code and data files state this in `README.md` and `data/SOURCES.md` (column `verificato_da`).
- The flame is drawn by CSS code, not by an image-generation model. No SI-generated images, video or audio are used. No NASA logo or branding is used.
- <TEAM: confirm that the idea of the project came from the team, not from SI, before submitting.>

## NASA Data
- NASA Physical Sciences Informatics (PSI) investigation pages: https://psi.nasa.gov/ — DOIs (prefix 10.60555), platforms and test conditions for PSI-10, 20, 21, 22, 23, 25, 26, 39, 47, 68, 69, 98, 99, 100, 101, 102, 106, 107, 159.
- NASA Technical Reports Server (NTRS): https://ntrs.nasa.gov/ — papers used for oxygen, pressure and airflow values (e.g. 20210011385, 20130014061, 20150023456, 20170001636, 20200000557, 20150011070). The exact source sentence is quoted in the `fonte_note` column of `data/investigations.csv`.

## Space Agency Partner Data and Other References
- Streamlit (Apache-2.0), pandas (BSD-3-Clause), Plotly (MIT), pydantic (MIT), google-genai (Apache-2.0), requests (Apache-2.0).
- Google Gemini API (model used for the Copilot).
- Our original code and text are released under the Apache-2.0 license (the Space Apps default); see `data/CREDITS.md` for the full list.
- No Space Agency Partner data was used.

## Disclaimer
Independent project for the NASA Space Apps Challenge; not affiliated with or endorsed by NASA.
