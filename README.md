# IntelligenzaArtificiale

Realizzazione di due reti bayesiane e codice sorgente in python per interfacciarsi con esse tramite pysmile, libreria di BayesFusion.

## Prototipo
Un industria manifatturiera deve decidere se andare avanti con la produzione di un nuovo prodotto o fermarla. I profitti futuri dipendono dalla qualita’ del prodotto (standard o alta) e dalla domanda di mercato (bassa o alta). L’industria puo’, prima di decidere sulla produzione, effettuare due altre azioni: migliorare la qualita’ del prodotto sviluppando un prototipo, oppure effettuare ricerche di marketing approfondite per capire la domanda di mercato. Puo’ effettuare anche entrambe le cose (nel qual caso prima effettua la ricerca di marketing). Entrambe queste azioni costano, in particolare le ricerche di mercato $1000 e lo sviluppo del prototipo di qualita’ $5000. Le ricerche di mercato sono affidabili al 90%, mentre lo sviluppo del prototipo ha una probabilita’ di aumentare la qualita’ dell’85%.
Le probabilita’ di profitto (nessuno, basso, alto) sono stimate dall’azienda (introdurle nel modello a piacere, ma con valori sensati; es: la prob. di un profitto alto deve essere piu’ alta se la domanda di mercato e’ alta e la qualita’ del prodotto e’ alta, rispetto ad una situazione in cui c’e’ prodotto scadente e bassa domanda).
Il costo della produzione e’ stimato in $2500, il profitto basso in $10000 ed il profitto alto in $50000.
L’industria non ha conoscenza sull’attuale domanda di mercato.
Modellare un processo decisionale in cui, sulla base dei dati in input, l’azienda scelga la sequenza di azioni migliori.

## Guida autonoma
Un veicolo autonomo deve mantenere il centro di una corsia unsando un sensore di posizione. Le azioni che puo’ eseguire come comandi sono Left, Stay, Right che muovono il veicolo a sx, non cambiano direzione oppure a dx rispettivamente. Ogni azione ha sempre una probabilita’ del 90% di avere successo, mentre nel rimanente 10% dei casi puo’ portare in un’altra direzione (es: il veicolo e’ nel centro, esegue Stay, rimane al centro con prob 0.9, va a sx con prob 0.05 e va a dx con prob 0.05; similmente negli altri casi).
Il sensore di posizione ha invece un accuratezza che dipende da molti fattori. In particolare, puo’ avere 3 livelli di accuratezza: ottima, buona e pessima. Nel primo caso la percentuale di accuratezza e; del 99% (cioe’ nel 99% dei casi segnala la posizione corretta e nel restante 1% una posizione sbagliata in modo uniforme).; nel secondo caso l’accuratezza e’ del 90%, mentre nel terzo caso del 35%.
L’accuratezza del sensore dipende da due fattori principali: le condizioni meterologiche e lo stato del terreno su cui si muove il veicolo.
Il tempo umido causa nel 30% dei casi una pessima accuratezza e nel 15% dei casi una buona (quindi nel 55% dei casi rimane ottima).
Il terreno sconnesso causa nel 60% dei casi una accuratezza pessima e nel 30% dei casi buone (ossia 10% dei casi ottima).
Le influenze dei due fattori sull’acuratezza sono indipendenti.
Entrambi i fattori possono inoltre causare un guasto al sensore, il che implica che la sua accuratezza diventa pessima.
Il fallimento del sensore avviene nel 10% dei casi di tempo umido e nel 50% dei casi di terreno sconnesso (di nuovo in modo indipendente l’uno dall’altro). Non ci sono altre cause immediate rilevanti. C’e pero’ una probabilita’ dello 0.1 che fallisca, per altre cause non modellate, all’istante successivo (degradazione del sensore).
Ricordando che scopo dell’agente automatico sul veicolo e’ mantenere il centro corsia, modellare un processo decisionale in cui, a seguito di un’osservazione del sensore, l’agente invii al veicolo il comando opportuno, modellando il processo per 5 istanti temporali, partendo dal veicolo sistemato in centro corsia.
Si assuma un modello di evoluzione del tempo (da secco a umido e viceversa) a piacere, cosi’ come un modello di evoluzione del terreno.
Il fallimento del sensore e’ permanente.
**NB: Smile lavora sul modello unrolled; causa bug, in Genie occorre riempire a mano sul modello unrolled le utilità degli istanti di tempo superiori a t=0**

## Realizzazione

Il progetto è impostato come segue

-licenze
    -pysmile_license.py
-prototipo
    -classi.py
    -decision_process.py
    -main.py
-reti
    -prototipo.xdsl
    -guida_autonoma_roll.xdsl
    -guida_autonoma_unrolled.xdsl

### Prototipo
Il sorgente *classi.py* contiene la classe ```Nodo``` che è un enumerativo contenente gli id dei nodi della rete, contiene anche la classe ```Outcome``` che è sempre un enumerativo contenente tutti i possibili outcome della rete: yes, no, nothing, low, high, standard. 
Il sorgente *decision_process.py* contiene la logica necessaria per interfacciarsi con la rete: modificare nodi, stampare utilità etc. 
Il sorgente *main.py* si connette alla rete, lancia il metodo ```decision_process()``` e infine stampa l'utilità del nodo *Profitto* dopo tutte le evidenze impostate nella rete.
