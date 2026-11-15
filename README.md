# Flame in Freefall

Dashboard for the **Flame in Freefall** challenge of the NASA Space Apps Challenge 2026: it summarizes, ranks and
explains NASA combustion experiments in microgravity, for fire safety on the Moon and Mars.

The user picks a scenario (gravity, oxygen, pressure, airflow); an **AI Copilot** drives the dashboard, but
**cannot invent data**: every answer is validated by the code (existing ids, numbers present in the cited
sources) and where the data do not exist it says so.

> Independent project, not affiliated with or endorsed by NASA. The flames are an illustrative rendering,
> not a physical simulation.

Live app: [<URL>](https://flame-in-freefall-nasa-clean-fxsi2n57qbyr5txlrtqpnv.streamlit.app/)

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Gemini key (only for the Copilot): the `GEMINI_API_KEY` environment variable, or
`.streamlit/secrets.toml` with `GEMINI_API_KEY = "..."`, or the field in the sidebar.
**Never commit the key** (`.streamlit/secrets.toml` is in `.gitignore`).

## Tests

```bash
python -m unittest discover -s tests -v
```

The tests require neither Streamlit nor Gemini (they use a fake Streamlit). They do not check the visual appearance.

## Structure and responsibilities

| Folder / file | Role | Content |
|---|---|---|
| `app.py`, `src/`, `ui/flame_lab.py` | A | app shell, AI, scores, animated flame |
| `ui/theme.py`, `ui/components.py`, `ui/plotly_theme.py`, `ui/tabs/` | C | theme, components, Compare / Gaps / Real data tabs |
| `data/`, `scripts/fetch_ntrs.py` | B | `investigations.csv`, `papers.json`, `raw/`, `SOURCES.md` |
| `dev/investigations_mock.csv` | A | **fake** development data, used only if `data/investigations.csv` is missing |

Contracts between the roles: CSV schema (columns frozen at v1, checked by
`python scripts/validate_csv.py`), `rank(df, scenario)`, `compare.render(df, scenario, highlight_ids)`,
`gaps.render(df, scenario, highlight_ids)`, `real_data.render(tables)`.

## Data rules

- Empty cell = unknown data. Never 0, never estimates.
- Every number shown has a source or a provenance label (REAL, MODEL, ILLUSTRATIVE, NO DATA).
- The relevance score is a **model** with weights declared in `src/scoring.py`.
- The column names and the categorical values of `data/investigations.csv` (for example `gravita`,
  `microgravita`, `solido`, `prevenzione`) are the stable data contract used by the code, so they keep their
  original Italian identifiers. The dashboard always shows English labels for them.

## AI use and resources

The in-app Copilot uses Google's Gemini model (`google-genai` API); every answer is validated
in code (record ids and numbers must appear in the cited records). The code in this repository (app, tests,
scripts, Flame Lab) was written with the assistance of Claude (Anthropic) and reviewed by the team. Data
summaries may contain AI-generated or AI-summarised text and must be checked against the sources listed in
`data/SOURCES.md`. The flame is rendered by CSS code, not by an image-generation model. The NASA Space Apps Challenge logo is shown in the top-right corner only to identify the event (`static/space_apps_logo_light.png`, light-on-dark variant of the official logo); no other NASA logo or
design element is used.

External resources: Streamlit, pandas, plotly, pydantic, google-genai, requests (see `requirements.txt`);
NASA Physical Sciences Informatics (psi.nasa.gov) and NASA NTRS (ntrs.nasa.gov) as data sources.
