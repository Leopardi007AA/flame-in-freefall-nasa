# Credits and sources

Independent project for the NASA Space Apps Challenge 2026 "Flame in Freefall". Not affiliated with or endorsed by NASA.

## Data
- NASA Physical Sciences Informatics (PSI): https://psi.nasa.gov/ — investigation pages PSI-10, 20, 21, 22, 23, 25, 26, 39, 47, 68, 69, 98, 99, 100, 101, 102, 106, 107, 159 (DOI, platform and test tables, 14 Nov 2026).
- NASA Technical Reports Server (NTRS): https://ntrs.nasa.gov/ — papers listed in `data/papers.json` and quoted in `data/investigations.csv` (`fonte_note`).
- PSI database guide: https://science.nasa.gov/wp-content/uploads/2024/11/psi-database-guide.pdf
- Terms of use of PSI data: not copied into this repository; NASA data are cited with their DOI.

## Software (third-party, open source)
| Package | License |
|---|---|
| Streamlit | Apache-2.0 |
| pandas | BSD-3-Clause |
| Plotly | MIT |
| pydantic | MIT |
| google-genai | Apache-2.0 |
| requests | Apache-2.0 |

Google Gemini API is used for the in-app Copilot (service, not redistributed).

## Our own work
Code and text of this repository are released under Apache-2.0 (the Space Apps default for original content).

## Use of SI (AI)
Parts of the code and of the data summaries were produced with the assistance of an AI assistant (Claude, Anthropic) and reviewed by the team. The in-app Copilot uses Google Gemini; its answers are validated by code. See `README.md` and `data/SOURCES.md`.
