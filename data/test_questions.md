# Domande di prova per il Copilota

Le risposte attese sono calcolate dal CSV attuale. Se il CSV cambia, rigenerare gli id attesi.

| # | Tipo | Domanda | Risposta corretta del Copilota | Id attesi |
|---|---|---|---|---|
| 1 | Risposta nei dati | Quali esperimenti hanno studiato combustibili liquidi? | Elenca le righe giuste con id citati | PSI-69, PSI-142 |
| 2 | Risposta nei dati | Quali esperimenti usano combustibili gassosi? | Elenca le righe giuste con id citati | PSI-20, PSI-10, PSI-106 |
| 3 | Risposta nei dati | Quali esperimenti usano combustibili solidi? | Elenca le righe giuste con id citati | PSI-25, PSI-98, PSI-99, PSI-100 |
| 4 | Risposta nei dati | Quali esperimenti sono stati eseguiti su Cygnus? | Elenca le righe giuste con id citati | PSI-98, PSI-99, PSI-100 |
| 5 | Risposta nei dati | Quali esperimenti appartengono alla famiglia Saffire? | Elenca le righe giuste con id citati | PSI-98, PSI-99, PSI-100 |
| 6 | Risposta nei dati | Quali esperimenti appartengono alla famiglia ACME? | Elenca le righe giuste con id citati | PSI-20, PSI-10 |
| 7 | Risposta nei dati | Per quali esperimenti c'è un intervallo di ossigeno nei dati? | Solo gli esperimenti indicati (BASS-II 14-21%, FLEX 12-30%); per gli altri «nessun dato» | PSI-25, PSI-69 |
| 8 | Risposta nei dati | Quali esperimenti hanno un flusso d'aria nei dati? | Gli esperimenti indicati con i loro valori in cm/s | PSI-25, PSI-98 |
| 9 | Risposta nei dati | A che flusso d'aria è stato condotto Saffire-I? | 20 cm/s, citando PSI-98 | PSI-98 |
| 10 | Risposta nei dati | Qual è il flusso d'aria massimo di BASS-II? | 40 cm/s (valore della scheda PSI), citando PSI-25 | PSI-25 |
| 11 | Confronto | Confronta BASS-II e Saffire-I per flusso d'aria. | Tabella coerente con il CSV | PSI-25, PSI-98 |
| 12 | Confronto | Confronta FLEX e Cool Flames per tipo di combustibile. | Tabella coerente con il CSV | PSI-69, PSI-142 |
| 13 | Confronto | Confronta ACME BRE e ACME Flame Design per combustibili. | Tabella coerente con il CSV | PSI-20, PSI-10 |
| 14 | Confronto | Confronta Saffire-I e Saffire-II per flusso d'aria. | Saffire-I 20 cm/s; Saffire-II «nessun dato» | PSI-98, PSI-99 |
| 15 | Confronto | Confronta BASS-II e FLEX per ossigeno. | BASS-II 14-21% e FLEX 12-30%, entrambi con intervallo | PSI-25, PSI-69 |
| 16 | Lacuna | Cosa sappiamo sul fuoco a 0,38 g (Marte)? | «Nessun dato a questa gravità» + prove più vicine | (nessuno) |
| 17 | Lacuna | Cosa sappiamo sul fuoco a 0,16 g (Luna)? | «Nessun dato a questa gravità» + prove più vicine | (nessuno) |
| 18 | Lacuna | Quali esperimenti hanno dati di pressione? | Solo FLEX (10.3-14.7 psia); per gli altri «nessun dato» | PSI-69 |
| 19 | Trabocchetto | Qual è la velocità di propagazione della fiamma di Saffire-III a 40% di O2? | Rifiuta: «Nessun dato», non inventa | PSI-100 (da non usare per numeri) |
| 20 | Trabocchetto | Qual è la temperatura massima raggiunta in FLEX? | Rifiuta: nessuna temperatura nei dati | PSI-69 (da non usare per numeri) |
