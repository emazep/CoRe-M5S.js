# CoRe M5S

Controllo Restituzione M5S

## Domande e risposte

```
CoRe M5S nasce come iniziativa privata, spontanea, libera e gratuita dell'autore,
il quale non è affiliato in alcun modo né ha alcun contatto con il Movimento 5 Stelle.
```

### A cosa serve quest'applicazione?

Attraverso il sito <a href="https://www.beppegrillo.it/tirendiconto.it/trasparenza/">Ti rendi conto?!?!?!?</a> è possibile controllare le somme restituite dai parlamentari del Movimento 5 Stelle. Tuttavia tale verifica può essere effettuata soltanto su un singolo mese alla volta, rendendo così disagevole il calcolo dell'importo totale restituito da un parlamentare in un arco di tempo più ampio. L'applicazione CoRe M5S colma questa lacuna, permettendo di controllare facilmente l'importo totale restituito da ogni parlamentare in un intervallo di tempo arbitrario. Inoltre CoRe M5S offre una sintesi dei dati che dovrebbe risultare più chiara e leggibile.


### I dati forniti da CoRe M5S sono attendibili?

Certamente: i dati mostrati da CoRe M5S sono esattamente quelli pubblicati su
<a href="https://www.beppegrillo.it/tirendiconto.it/trasparenza/">Ti rendi conto?!?!?!?</a>,
che vengono prelevati e utilizzati senza alcuna alterazione.

Fanno eccezione soltanto i primi tre mesi della legislatura (marzo, aprile, maggio del 2013) per i quali, limitatamente ad
alcuni parlamentari, sul predetto sito non sono presenti i dati in formato testuale (sono presenti soltanto le copie fotografiche
delle ricevute dei bonifici, peraltro di non chiarissima interpretazione, da cui non è possibile estrarre le informazioni in automatico).
Limitatamente ai soli predetti tre mesi ed ai soli parlamentari che in tale periodo non hanno pubblicato i dati in formato testuale,
sono stati utilizzati i seguenti valori presuntivi:

* stipendio mensile percepito: 5.000 Euro;
* restituzione mensile stipendio: 2.000 Euro;
* rimborsi mensili percepiti: 7.000 Euro;
* restituzione mensile rimborsi: 3.000 Euro;

derivanti da una stima dei valori medi, (largamente) <em>favorevole</em> al parlamentare
(ovvero stipendi e rimborsi sottostimati, restituzioni sovrastimate).
Tutto questo al netto di bug, che nel software sono sempre possibili. Tuttavia non appena segnalati,
gli eventuali bug verranno prontamente corretti.
D'altro canto, essendo il codice sorgente di CoRe M5S aperto, chiunque può controllarne la correttezza.

### L'esportazione dei risultati come immagine non funziona bene!

Risposta breve: lo so. Risposta lunga: non è semplice da fare interamente client-side (in particolar modo su dispositivi touch) come fa quest'applicazione, considerando che si è inteso generare i risultati
in formato testuale, perché ciò permette di il copia e incolla degli stessi. (L'aiuto su questa funzionalità
dell'applicazione, purché fattivo, sarà grandemente apprezzato).
Workaround, in ordine di preferenza: utilizzate un browser recente (preferibilmente Firefox o Chrome),
preferibilmente su un computer e non un dispositivo mobile; in estremo subordine, fate uno screenshot.

### Come si può contribuire al progetto?

Attraverso GitHub. La documentazione disponibile è tuttavia pressoché inesistente,
né è prevedibile che ne venga aggiunta a breve termine (almeno non dall'autore del progetto).
Per contribuire è necessario quindi possedere una buona familiarità con le tecnologie utilizzate nell'applicazione in quanto, per comprenderne il funzionamento, sarà necessario esaminarne il codice sorgente.

Le tecnologie utilizzate nell'applicazione sono:

* HTML5;
* CSS;
* JavaScript;
* jQuery;
* Semantic UI;
* Python (per gli script offline per il prelievo dei dati);

mentre gli strumenti di sviluppo adottati sono:

* Node.js;
* gulp;
* Git.

## Versioning

CoRe M5S usa il [Semantic Versioning](http://semver.org/), con l'aggiunta di un quarto campo dopo il campo PATCH,
che viene aggiornato se e solo se vengono aggiornati i dati delle restituzioni prelevati dal sito
<a href="https://www.beppegrillo.it/tirendiconto.it/trasparenza/">Ti rendi conto?!?!?!?</a>
(il campo predetto contiene la data, in formato AAAA-MM-GG, dell'ultima acquisizione dei dati effettuata).

## Autore

**Emanuele Zeppieri** - [facebook](https://www.facebook.com/emanuele.zeppieri)

## Licenza

Questo progetto è rilasciato sotto la licenza MIT - per i dettagli si guardi il file [LICENSE](LICENSE).
