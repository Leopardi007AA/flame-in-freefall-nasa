# Test Questions for AI Assistant & Judges

Verification questions designed to validate the NASA microgravity data architecture and RAG system.

## Category A: Operational & Flame Behavior
1. How does oxygen concentration affect the flame extinction time for solid PMMA in the BASS-II experiment?
2. What are the key differences in burning rates between heptane and methanol droplets observed during FLEX?
3. What airflow threshold is required to sustain combustion in low-gravity environments according to Saffire data?

## Category B: Data Integrity & NTRS Bibliographic Sources
4. Which NASA NTRS paper details the operations of BASS-II on the International Space Station? (Expected DOI: 10.1016/j.proci.2016.06.031)
5. What investigation ID corresponds to the Cool Flames Investigation (CFI)? (Expected: PSI-39)
6. How many total microgravity combustion investigations are indexed in `data/papers.json`?

## Category C: Edge Cases & Safety Limits
7. Can a flame self-extinguish in microgravity without forced convection?
8. What role do cool flames play in high-pressure droplet combustion limits?