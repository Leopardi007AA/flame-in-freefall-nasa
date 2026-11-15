# Flame in Freefall

Dashboard for the **Flame in Freefall** challenge of the NASA Space Apps Challenge 2026: it summarizes, ranks and
explains NASA combustion experiments in microgravity, for fire safety on the Moon and Mars.

The user picks a scenario (gravity, oxygen, pressure, airflow); an **AI Copilot** drives the dashboard, but
**cannot invent data**: every answer is validated by the code (existing ids, numbers present in the cited
sources) and where the data do not exist it says so.

> Independent project, not affiliated with or endorsed by NASA. The flames are an illustrative rendering,
> not a physical simulation.

- Live app: https://flame-in-freefall-nasa-clean-fxsi2n57qbyr5txlrtqpnv.streamlit.app/
- Presentation (Google Slides): https://docs.google.com/presentation/d/1iUPAxiVmiNx3HI-IpGE8ZAAgTozwuArUOD9Xil2ZWaY/edit?slide=id.h2458178d6528d7cb_0_368#slide=id.h2458178d6528d7cb_0_368

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

## Structure

| Folder / file | Content |
|---|---|
| `app.py` | the Streamlit app: sidebar, Flame Lab, Copilot, tiles, ranking and tabs |
| `src/` | data loading (`data_loader.py`), relevance score (`scoring.py`), Copilot and its validation (`ai_engine.py`, `ai_validation.py`, `system_prompt.txt`, `demo_answers.json`), NTRS helpers (`ntrs_tools.py`) |
| `ui/` | theme, components, Plotly theme, animated flame (`flame_lab.py`), Compare / Gaps / Real data tabs (`tabs/`) |
| `data/` | `investigations.csv`, `papers.json`, `raw/` (previews of the PSI tables), `SOURCES.md`, `CREDITS.md` |
| `scripts/` | `validate_csv.py`, `fetch_ntrs.py`, `verify_ntrs.py`, `check_gemini.py` |
| `tests/` | unit and smoke tests |
| `docs/` | demo script and submission sheet |
| `dev/` | **fake** development data, used only if `data/investigations.csv` is missing |

Main interfaces: the CSV schema (columns frozen at v1, checked by `python scripts/validate_csv.py`),
`rank(df, scenario)`, `compare.render(df, scenario, highlight_ids)`,
`gaps.render(df, scenario, highlight_ids)` and `real_data.render(tables)`.

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

## License

Apache License 2.0, see [LICENSE](LICENSE). NASA data remain subject to the terms of the NASA sites they come from; sources and credits are in [`data/SOURCES.md`](data/SOURCES.md) and [`data/CREDITS.md`](data/CREDITS.md).
