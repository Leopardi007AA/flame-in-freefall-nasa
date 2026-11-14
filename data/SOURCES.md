# Fonti dei dati

## Stato dei dati grezzi
`data/raw/` è **vuota di proposito**: i file di esempio che c'erano non erano download originali NASA e sono stati rimossi.
La scheda «Dati reali» dell'app mostra «Nessun dato» finché non ci sono tabelle originali scaricate da NASA PSI.

## Tabella degli esperimenti (`data/investigations.csv`)
* **Nomi:** controllati sull'elenco ufficiale «PSI investigations by research area» (sezione Combustion Science):
  https://www.nasa.gov/physical-sciences-informatics-psi/psi-investigations-by-research-area/
* **Righe 11-19 (bozza, `verificato_da = Claude-bozza`):** nome dall'elenco ufficiale, id da tabelle di archivi pubblici di altri team
  (github.com/OSAMABASAM/NASA_flame_in_freefall, github.com/YoussefHegazy74/flame-in-freefall); nessun valore numerico. Due voci (ACME CLD, ACME CFI-G)
  non sono nell'elenco ufficiale. Cool Flames: id corretto da PSI-142 a PSI-39 (stesse fonti). **Tutti da verificare sul sito PSI.**
* **Id PSI e testi delle schede (righe 1-10):** presi dalle schede `https://psi.nasa.gov/physci/repo/data/investigations/PSI-<numero>`.
  L'elenco ufficiale non riporta gli id: **gli id vanno riverificati a mano sul sito PSI**.
* **Valori numerici da articoli NASA NTRS** (letti sul PDF tramite `scripts/verify_ntrs.py`; ogni riga cita la frase della fonte in `fonte_note`):
  * PSI-25 (BASS-II): O2 14-21% (NTRS 20210011385, titolo coincidente); flusso fino a 40 cm/s dalla scheda PSI (il report dice ~55 cm/s: annotato).
  * PSI-69 (FLEX): O2 12-30% e 0.7-1 atm (10.3-14.7 psia), condizioni della maggior parte dei test (NTRS 20130014061 e 20150023456). Intervallo completo 0.70-3.05 atm fuori schema.
  * PSI-98 (Saffire-I): flusso 20 cm/s e O2 ~21% PREVISTI nei paper pre-volo (NTRS 20170001636, 20170000230).
  * PSI-99 (Saffire-II): 100 kPa (14.5 psia) e 200 mm/s (20 cm/s) (NTRS 20200000557).
  * PSI-100 (Saffire-III): flusso 30 cm/s PREVISTO (NTRS 20170001636).
  * PSI-106 (SLICE): coflusso d'aria 18-71 cm/s (NTRS 20150011070).
* **DOI:** l'API NTRS riporta un DOI solo per l'articolo 20200000557 (PSI-99); quello di FLEX (10.60555/mbq8-0451) viene da un archivio di terzi. Gli altri restano vuoti.
* Cella vuota = dato sconosciuto. Mai 0, mai stime.

## Articoli (`data/papers.json`)
Elenco curato di articoli NTRS; il campo `da_controllare` resta `true` finché titolo, autori e anno non sono controllati.

## Licenza / condizioni d'uso
Da copiare dal sito PSI (non verificata).
