# Data sources

## Status of the raw data
`data/raw/` is **empty on purpose**: the sample files that were there were not original NASA downloads and have been removed.
The app's “Real data” tab shows “No data” until there are original tables downloaded from NASA PSI.

## Experiments table (`data/investigations.csv`)
* **Names:** checked against the official list “PSI investigations by research area” (Combustion Science section):
  https://www.nasa.gov/physical-sciences-informatics-psi/psi-investigations-by-research-area/
* **Rows 11-19 (draft, `verificato_da = Claude-bozza`):** name from the official list, id from tables in other teams' public repositories
  (github.com/OSAMABASAM/NASA_flame_in_freefall, github.com/YoussefHegazy74/flame-in-freefall); no numerical values. Two entries (ACME CLD, ACME CFI-G)
  are not in the official list. Cool Flames: id corrected from PSI-142 to PSI-39 (same sources). **Id, name and DOI were later confirmed by the PSI pages (see below).**
* **PSI ids and page texts (rows 1-10):** taken from the pages `https://psi.nasa.gov/physci/repo/data/investigations/PSI-<number>`.
  The official list does not give the ids: **the ids must be re-verified by hand on the PSI site**.
* **Numerical values from NASA NTRS papers** (read from the PDF with `scripts/verify_ntrs.py`; each row cites the source sentence in `fonte_note`):
  * PSI-25 (BASS-II): O2 14-21% (NTRS 20210011385, matching title); airflow up to 40 cm/s from the PSI page (the report says ~55 cm/s: noted).
  * PSI-69 (FLEX): O2 12-30% and 0.7-1 atm (10.3-14.7 psia), conditions of most tests (NTRS 20130014061 and 20150023456). The full range 0.70-3.05 atm is outside the schema.
  * PSI-98 (Saffire-I): airflow 20 cm/s and O2 ~21% EXPECTED in the pre-flight papers (NTRS 20170001636, 20170000230).
  * PSI-99 (Saffire-II): 100 kPa (14.5 psia) and 200 mm/s (20 cm/s) (NTRS 20200000557).
  * PSI-100 (Saffire-III): airflow 30 cm/s EXPECTED (NTRS 20170001636).
  * PSI-106 (SLICE): air coflow 18-71 cm/s (NTRS 20150011070).
* Empty cell = unknown data. Never 0, never estimates.

## Official PSI pages (14 Nov 2026)
* **DOI, platform and id of all 19 rows** are taken from the text of the PSI site pages (copied by a team member). The DOIs are those of the PSI dataset (prefix 10.60555).
* **Values from the data tables of the pages** (`verificato_da = Claude-PSI` on the rows that used to be drafts): PSI-98 and PSI-99 (O2 21.5 and 21.5-22.1%, airflow 20 cm/s), PSI-39 (1 atm, O2 21%), PSI-10 (O2 20.4-20.7%, 1.012-1.018 atm), PSI-68 (O2 17%, 0.5 atm, 0.1 cm/s), PSI-102 (5-10 cm/s), PSI-101 (8.1 cm/s), PSI-159 (O2 38-39.4%), PSI-107 (36.39-57.08 cm/s). atm converted to psia (x14.696).
* **Check of 14 Nov (page texts):** PSI-98 and PSI-100: the “Flight Platform” field says ISS, but the page text says the experiment was run on Cygnus after it deberthed from the ISS: platform = Cygnus. PSI-68: the header confirms cm/s; the table gives O2 17-30%, 0.5-3.0 atm, 0.1-5 cm/s (pressure limited to 0.5-1.0 atm because of the schema limit). PSI-25: O2 22.2% added from the table (14-22.2). PSI-159: pressure ~13.7 psia (0.944 bar).
* The rows without numerical values (PSI-20, 47, 26, 22, 23, 21) have no O2/pressure/airflow columns in the pasted pages: they stay empty.

## Papers (`data/papers.json`)
Curated list of NTRS papers; the `da_controllare` field stays `true` until title, authors and year have been checked.

## License / terms of use
To be copied from the PSI site (not verified).
