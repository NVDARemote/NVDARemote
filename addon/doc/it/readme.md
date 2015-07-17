#NVDA Remote Access
Versione 1.0

Benvenuti nell'addon NVDA Remote Access, che consente di connettervi ad un altro computer che esegue lo screen reader gratuito NVDA. Non fa alcuna differenza se si è dall'altra parte della stanza o del mondo. Connettersi è semplice, e ci sono solo pochi comandi da ricordare. È possibile collegarsi al computer di un'altra persona, o permettere ad una persona di fiducia di connettersi al proprio sistema per eseguire operazioni di manutenzione di routine, diagnosticare un problema, o insegnare qualcosa.

## Requisiti

È necessario installare NVDA     e l'addon NVDA Remote Access su entrambi i computer.
L'installazione di entrambe le cose, NVDA e l'addon per l'accesso remoto, si esegue in maniera standard. Se sono necessarie ulteriori informazioni, si possono trovare nel manuale di NVDA.

## Avvio di una sessione remota tramite un server esterno
### Computer controllato
1. Aprire il menu di NVDA, Strumenti, Accesso Remoto, Connetti.
2. Scegliere client nel primo gruppo di pulsanti radio.
3. Scegliere Consenti il controllo remoto di questo PC nel secondo gruppo di pulsanti radio.
4. Nel campo host, immettere l'host del server a cui ci si connette, per esempio nvdaremote.com.
5. Inserire una chiave nel campo chiave, oppure premere il pulsante genera chiave d'accesso.
La chiave è ciò che gli altri utilizzeranno per controllare il computer.
La macchina controllata e tutti i suoi client devono utilizzare la stessa chiave.
6. Premere OK. Una volta fatto, si sentirà un beep e la parola connesso.

### Controllare un altro computer
1. Aprire il menu NVDA, Strumenti, Accesso Remoto, Connetti.
2. Scegliere client nel primo gruppo di pulsanti radio.
3. Scegliere Controlla un altro PC nel secondo gruppo di pulsanti radio.
4. Nel campo host, immettere l'host del server a cui ci si connette, per esempio nvdaremote.com.
5. Inserire una chiave nel campo chiave, oppure premere il pulsante genera chiave d'accesso.
La chiave è ciò che gli altri utilizzeranno per controllare il computer.
La macchina controllata e tutti i suoi client devono utilizzare la stessa chiave.
6. Premere OK. Una volta fatto, si sentirà un beep e la parola connesso.

## Connessioni dirette
L'opzione server nella finestra di dialogo connessione consente di impostare una connessione diretta.
Una volta selezionata tale opzione, seleziona la modalità della tua connessione, se controllare un Pc o essere controllato.
L'altra persona si connetterà utilizzando il metodo opposto.

Una volta selezionata la modalità, è possibile utilizzare il pulsante Ottieni Ip esterno per ottenere il vostro indirizzo IP esterno.
Assicurarsi che la porta sia aperta correttamente.
Se viene rilevato che la porta (6837) non è raggiungibile, viene visualizzato un messaggio di avviso.
Aprire la porta e riprovare.
Nota: Il processo di apertura delle porte va oltre lo scopo di questa guida. Consultare le informazioni fornite con il router per ulteriori istruzioni.

Immettere una chiave nel campo chiave, oppure premere il pulsante genera. L'altra persona avrà bisogno del vostro IP esterno oltre alla chiave per la connessione.

Una volta premuto OK, sarete connessi.
Quando l'altra persona si connette, è possibile utilizzare NVDA remote normalmente.

## Inoltro tasti
Una volta che la sessione è iniziata, il Pc che ha il controllo sarà in grado di premere F11 per iniziare ad inoltrare i tasti.
Quando NVDA dice inoltro tasti, i tasti premuti avranno effetto sulla macchina remota. Premere di nuovo F11 per interrompere l'inoltro dei tasti e tornare alla macchina di controllo.
Per una migliore compatibilità, assicurarsi che i layout tastiera corrispondano su entrambe le macchine.

## Inoltro di Ctrl + Alt + Canc
Durante l'inoltro dei tasti, non è possibile inviare la combinazione Ctrl+Alt+Canc normalmente.
Se è necessario inviare Ctrl+Alt+Canc, e il sistema remoto si trova su desktop sicuro, utilizzare questo comando.

## Controllare da  remoto un computer in maniera automatica

A volte, si potrebbe desiderare di controllare uno dei vostri computer da remoto. Ciò è particolarmente utile se si viaggia e si desidera controllare il vostro PC di casa dal proprio laptop. oppure, si potrebbe voler controllare un computer in una stanza della casa, mentre si è seduti fuori, usando un altro PC. Un po di preparazione iniziale rende questa cosa conveniente e possibile.

1. Accedere al menu NVDA, scegliere Strumenti, quindi Accesso Remoto. Infine, premere Invio su Opzioni.
2. Selezionare la casella che dice: "Connetti automaticamente al server di controllo all'avvio".
3. Inserire i dati nei campi Host e chiave, usare il tab fino al pulsante OK e premere Invio.
4. Nota: l'opzione Genera chiave non è disponibile in questa situazione. La cosa migliore è trovare una chiave che poi verrà ricordata in modo da poterla facilmente utilizzare da qualsiasi postazione remota.

## Silenziare la sintesi sul computer remoto
Se non si desidera ascoltare la sintesi del computer remoto, è sufficiente accedere al menu NVDA, Strumenti, Accesso Remoto. Usare la Freccia  giù fino a Silenzia il sintetizzatore del PC remoto, e premere Invio.

## Terminare una sessione remota

Per terminare una sessione remota, effettuare le seguenti operazioni:

1. Sul Pc di controllo, premere F11 per interrompere l'inoltro tasti. Dovreste sentire il messaggio: "Inoltro tasti disattivato." Se invece si sente il messaggio Inoltro tasti, premere F11 ancora una volta.
2. Accedere al menu NVDA, poi Strumenti, Accesso Remoto e premere Invio su Disconnetti.

## Inviare gli appunti
L'opzione Invia appunti nel menu remote permette di inviare del testo dagli appunti.
quando attivata, qualsiasi testo negli appunti sarà inviato agli altri Pc.

## Configurazione di NVDA remote per consentirne l'accesso  al desktop sicuro e finestra di logon

Affinché NVDA Remote funzioni sul desktop sicuro e finestra di logon, l'addon deve essere installato in una versione di NVDA che ha l'accesso al desktop sicuro e finestra di logon.

1. Dal menu NVDA, selezionare Preferenze, quindi Impostazioni generali.

2. Tab fino al pulsante Utilizza le impostazioni di configurazione salvate nella finestra di logon (richiede privilegi di amministratore), e premere Invio.

3. Rispondere Sì alle domande riguardanti la copia delle impostazioni e sul copiare i plugin, e rispondere al prompt del Controllo account utente che può apparire.

4. Quando le impostazioni sono state copiate, premere Invio per confermare. Tab fino ad OK e premere invio ancora una volta per uscire dalla finestra.

Una volta che NVDA remoto viene installato sul desktop sicuro, se si viene controllati in una sessione remota, sarà possibile controllare anche la finestra di logon e Desktop Sicuro quando vi si accede.

## Contributi
Vorremmo inoltre ringraziare i seguenti collaboratori che hanno contribuito a rendere il progetto NVDA Remote una realtà.

* Hai Nguyen Ly
* Chris Westbrook
* Thomas Huebner
* John F Crosotn III
* Darrell Shandrow
* D Williams
* Mattew McCubbin
* Jason Meddaugh
* ABDULAZIZ ALSHMASI.
* Tyler W Kavanaugh
* Casey Mathews 