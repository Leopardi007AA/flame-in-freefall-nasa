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
* **Valori numerici da articoli NASA NTRS** (ogni riga cita la frase della fonte in `fonte_note`):
  * PSI-69 (FLEX): ossigeno 12-30%, pressione 0.7 e 1 atm (= 10.3 e 14.7 psia) da NTRS 20130014061 (da verificare che il paper coincida con FLEX).
  * PSI-25 (BASS-II): ossigeno 14-21% da NTRS 20150019858 (da verificare); flusso fino a 40 cm/s dalla scheda PSI.
  * PSI-98 (Saffire-I): flusso 20 cm/s, confermato da NTRS 20170008805.
* **DOI:** non verificati, colonna lasciata vuota. Da compilare solo dopo controllo su doi.org o sulla scheda PSI.
* Cella vuota = dato sconosciuto. Mai 0, mai stime.

## Articoli (`data/papers.json`)
Elenco curato di articoli NTRS; il campo `da_controllare` resta `true` finché titolo, autori e anno non sono controllati.

## Licenza / condizioni d'uso
Da copiare dal sito PSI (non verificata).
