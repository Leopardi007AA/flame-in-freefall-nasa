# Data sources

## Raw data (`data/raw/`)
Each `PSI-xx/` folder holds a `*_psi_page_preview.csv`: the first rows of the table shown on the PSI page of that investigation, transcribed on 14 November 2026 without changing any value. They are partial previews, not the full datasets (see `data/raw/README.md`). The full datasets can be downloaded from each PSI page using the DOI in `data/investigations.csv`.

## Experiments table (`data/investigations.csv`)
* **Names:** checked against the official list "PSI investigations by research area" (Combustion Science section):
  https://www.nasa.gov/physical-sciences-informatics-psi/psi-investigations-by-research-area/
* **PSI id, DOI and platform of all 19 rows** come from the text of the PSI pages (`https://psi.nasa.gov/physci/repo/data/investigations/PSI-<number>`), copied by a team member on 14 November 2026. The DOIs are those of the PSI datasets (prefix 10.60555). Two entries (ACME CLD, ACME CFI-G) are not in the official list; their name and id come from the PSI pages.
* **Values taken from the tables on the PSI pages** (`verificato_da = Claude-PSI`): PSI-98 and PSI-99 (O2 21.5-21.7% and 21.5-22.1%, airflow 20 cm/s), PSI-39 (1 atm, O2 21%), PSI-10 (O2 20.4-20.7%, 1.012-1.018 atm), PSI-68 (O2 17-30%, 0.5-3.0 atm, 0.1-5 cm/s), PSI-102 (5-10 cm/s), PSI-101 (8.1 cm/s), PSI-159 (O2 38-39.4%, about 13.7 psia), PSI-107 (36.39-57.08 cm/s). Pressures in atm are converted to psia (x14.696).
* **Values read from NASA NTRS papers** (with `scripts/verify_ntrs.py`; each row cites the source sentence in `fonte_note`):
  * PSI-25 (BASS-II): O2 14-22.2% (NTRS 20210011385 and the PSI table); airflow up to 40 cm/s from the PSI page (the report says about 55 cm/s: noted).
  * PSI-69 (FLEX): O2 12-30% and 0.7-1 atm (10.3-14.7 psia), conditions of most tests (NTRS 20130014061 and 20150023456). The full range 0.70-3.05 atm is outside the schema.
  * PSI-98 (Saffire-I): airflow 20 cm/s (PSI page); O2 expected near 21% in the pre-flight papers (NTRS 20170001636, 20170000230).
  * PSI-99 (Saffire-II): 100 kPa (14.5 psia) and 200 mm/s (20 cm/s) (NTRS 20200000557).
  * PSI-100 (Saffire-III): airflow 30 cm/s expected (NTRS 20170001636).
  * PSI-106 (SLICE): air coflow 18-71 cm/s (NTRS 20150011070).
* **Platform:** for PSI-98 and PSI-100 the "Flight Platform" field says ISS, but the page text says the experiment ran on the Cygnus vehicle after it left the ISS, so the platform is Cygnus.
* **Schema limit:** PSI-68 pressure is limited to 0.5-1.0 atm (7.35-14.7 psia) because its 3.0 atm maximum is above the 30 psia limit of the schema.
* The rows without numerical values (PSI-20, 47, 26, 22, 23, 21) have no oxygen, pressure or airflow columns in the pages we read: those cells stay empty.
* Empty cell = unknown data. Never 0, never an estimate.

## Papers (`data/papers.json`)
Curated list of NTRS papers; the `da_controllare` field stays `true` until title, authors and year have been checked.

## Licence and terms of use
The PSI dataset pages we read state the licence CC0-1.0. Credits for libraries and tools are in `data/CREDITS.md`.
