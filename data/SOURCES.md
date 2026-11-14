# Fonti dei dati

## Stato dei dati grezzi
`data/raw/` è **vuota di proposito**: i file di esempio che c'erano non erano download originali NASA e sono stati rimossi.
La scheda «Dati reali» dell'app mostra «Nessun dato» finché non ci sono tabelle originali scaricate da NASA PSI.

## Tabella degli esperimenti (`data/investigations.csv`)
* **Nomi:** controllati sull'elenco ufficiale «PSI investigations by research area» (sezione Combustion Science):
  https://www.nasa.gov/physical-sciences-informatics-psi/psi-investigations-by-research-area/
* **Righe 11-19 (bozza, `verificato_da = Claude-bozza`):** nome dall'elenco ufficiale, id da tabelle di archivi pubblici di altri team
  (github.com/OSAMABASAM/NASA_flame_in_freefall, github.com/YoussefHegazy74/flame-in-freefall); nessun valore numerico. Due voci (ACME CLD, ACME CFI-G)
  non sono nell'elenco ufficiale. Cool Flames: id corretto da PSI-142 a PSI-39 (stesse fonti). **Id, nome e DOI poi confermati dalle schede PSI (vedi sotto).**
* **Id PSI e testi delle schede (righe 1-10):** presi dalle schede `https://psi.nasa.gov/physci/repo/data/investigations/PSI-<numero>`.
  L'elenco ufficiale non riporta gli id: **gli id vanno riverificati a mano sul sito PSI**.
* **Valori numerici da articoli NASA NTRS** (letti sul PDF tramite `scripts/verify_ntrs.py`; ogni riga cita la frase della fonte in `fonte_note`):
  * PSI-25 (BASS-II): O2 14-21% (NTRS 20210011385, titolo coincidente); flusso fino a 40 cm/s dalla scheda PSI (il report dice ~55 cm/s: annotato).
  * PSI-69 (FLEX): O2 12-30% e 0.7-1 atm (10.3-14.7 psia), condizioni della maggior parte dei test (NTRS 20130014061 e 20150023456). Intervallo completo 0.70-3.05 atm fuori schema.
  * PSI-98 (Saffire-I): flusso 20 cm/s e O2 ~21% PREVISTI nei paper pre-volo (NTRS 20170001636, 20170000230).
  * PSI-99 (Saffire-II): 100 kPa (14.5 psia) e 200 mm/s (20 cm/s) (NTRS 20200000557).
  * PSI-100 (Saffire-III): flusso 30 cm/s PREVISTO (NTRS 20170001636).
  * PSI-106 (SLICE): coflusso d'aria 18-71 cm/s (NTRS 20150011070).
* Cella vuota = dato sconosciuto. Mai 0, mai stime.

## Schede PSI ufficiali (14 nov 2026)
* **DOI, piattaforma e id di tutte le 19 righe** sono presi dal testo delle schede del sito PSI (copiato da un membro del team). I DOI sono quelli del dataset PSI (prefisso 10.60555).
* **Valori dalle tabelle di dati delle schede** (`verificato_da = Claude-PSI` sulle righe che prima erano bozza): PSI-98 e PSI-99 (O2 21.5 e 21.5-22.1%, flusso 20 cm/s), PSI-39 (1 atm, O2 21%), PSI-10 (O2 20.4-20.7%, 1.012-1.018 atm), PSI-68 (O2 17%, 0.5 atm, 0.1 cm/s), PSI-102 (5-10 cm/s), PSI-101 (8.1 cm/s), PSI-159 (O2 38-39.4%), PSI-107 (36.39-57.08 cm/s). atm convertiti in psia (x14.696).
* **Da ricontrollare:** PSI-98 e PSI-100 risultano su ISS nella scheda; la pubblicazione li descrive su Cygnus. Il flusso di PSI-68 (0.1 cm/s) è quello della tabella: unità non confermata.
* Le righe senza valori numerici (PSI-20, 47, 26, 22, 23, 21) non hanno colonne O2/pressione/flusso nelle schede incollate: restano vuote.

## Articoli (`data/papers.json`)
Elenco curato di articoli NTRS; il campo `da_controllare` resta `true` finché titolo, autori e anno non sono controllati.

## Licenza / condizioni d'uso
Da copiare dal sito PSI (non verificata).
