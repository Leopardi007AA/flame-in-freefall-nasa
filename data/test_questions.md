# Test questions for the Copilot

The expected answers are computed from the current CSV. If the CSV changes, regenerate the expected ids.

| # | Type | Question | Correct Copilot answer | Expected ids |
|---|---|---|---|---|
| 1 | Answer in the data | Which experiments studied liquid fuels? | Lists the right rows with cited ids | PSI-69, PSI-39 |
| 2 | Answer in the data | Which experiments use gaseous fuels? | Lists the right rows with cited ids | PSI-20, PSI-10, PSI-106 |
| 3 | Answer in the data | Which experiments use solid fuels? | Lists the right rows with cited ids | PSI-25, PSI-98, PSI-99, PSI-100 |
| 4 | Answer in the data | Which experiments were run on Cygnus? | Lists the right rows with cited ids | PSI-98, PSI-99, PSI-100 |
| 5 | Answer in the data | Which experiments belong to the Saffire family? | Lists the right rows with cited ids | PSI-98, PSI-99, PSI-100 |
| 6 | Answer in the data | Which experiments belong to the ACME family? | Lists the right rows with cited ids | PSI-20, PSI-10 |
| 7 | Answer in the data | For which experiments is there an oxygen range in the data? | Only the experiments indicated (BASS-II 14-21%, FLEX 12-30%, Saffire-I 21% expected); for the others “no data” | PSI-25, PSI-69, PSI-98 |
| 8 | Answer in the data | Which experiments have an airflow in the data? | The experiments indicated with their values in cm/s | PSI-25, PSI-98, PSI-99, PSI-100, PSI-106 |
| 9 | Answer in the data | At what airflow was Saffire-I run? | 20 cm/s, citing PSI-98 | PSI-98 |
| 10 | Answer in the data | What is the maximum airflow of BASS-II? | 40 cm/s (value from the PSI page), citing PSI-25 | PSI-25 |
| 11 | Comparison | Compare BASS-II and Saffire-I on airflow. | Table consistent with the CSV | PSI-25, PSI-98 |
| 12 | Comparison | Compare FLEX and Cool Flames by fuel type. | Table consistent with the CSV | PSI-69, PSI-39 |
| 13 | Comparison | Compare ACME BRE and ACME Flame Design by fuels. | Table consistent with the CSV | PSI-20, PSI-10 |
| 14 | Comparison | Compare Saffire-I and Saffire-II on airflow. | Both 20 cm/s | PSI-98, PSI-99 |
| 15 | Comparison | Compare BASS-II and FLEX on oxygen. | BASS-II 14-21% and FLEX 12-30%, both with a range | PSI-25, PSI-69 |
| 16 | Gap | What do we know about fire at 0.38 g (Mars)? | “No data at this gravity” + closest evidence | (none) |
| 17 | Gap | What do we know about fire at 0.16 g (Moon)? | “No data at this gravity” + closest evidence | (none) |
| 18 | Gap | Which experiments have pressure data? | FLEX (10.3-14.7 psia) and Saffire-II (14.5 psia); for the others “no data” | PSI-69, PSI-99 |
| 19 | Trap | What is the flame propagation speed of Saffire-III at 40% O2? | Refuses: “No data”, does not invent | PSI-100 (do not use for numbers) |
| 20 | Trap | What is the maximum temperature reached in FLEX? | Refuses: no temperature in the data | PSI-69 (do not use for numbers) |
