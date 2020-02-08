#NVDA Remote Access
Versione 2.2

Ecco il componente aggiuntivo NVDA Remote Access, che consente di connettervi ad un altro computer che esegue lo screen reader  NVDA. Non importa se si è dall'altra parte della stanza o del mondo. Connettersi è semplice, e ci sono solo pochi comandi da ricordare. È possibile collegarsi al computer di un'altra persona, o permettere ad una persona di fiducia di connettersi al proprio dispositivo per eseguire operazioni di manutenzione di routine, diagnosticare problemi, o per attività didattica.

## Requisiti

È necessario installare NVDA     eil componente aggiuntivo NVDA Remote Access su entrambi i computer.

L'installazione del componente aggiuntivo e dello screen reader si esegue in modo abituale, vedere il manuale utente dello screen reader NVDA per maggiori informazioni.

## Aggiornamenti:

Quando si aggiorna il componente aggiuntivo, se hai installato NVDA Remoto sul desktop sicuro, si consiglia di aggiornare anche la copia sul desktop sicuro.

Per fare ciò, aggiornare innanzi tutto il componente aggiuntivo,   quindi aprire il menu  NVDA, preferenze, impostazioni Generali, selezionare la casella di controllo "Utilizza NVDA nella finestra di logon (richiede privilegi di amministratore)".

## Avvio di una sessione remota tramite un server esterno
### Computer controllato
1. Aprire il menu di NVDA, Strumenti, Accesso Remoto, Connetti.
2. Scegliere client nel primo gruppo di pulsanti radio.
3. Scegliere Consenti il controllo remoto di questo PC nel secondo gruppo di pulsanti radio.
4. Nel campo host, immettere l'host del server a cui ci si connette, per esempio nvdaremote.com. Se il server in uso usa una porta alternativa, si può inserire l'Host con la sintassi &lt;host&gt;:&lt;port&gt; (per esempio nvdaremote.com:1234).
5. Inserire una  chiave d'accesso nel campo di editazione apposito, oppure premere il pulsante genera chiave d'accesso. La chiave d'accesso servirà alla persona che  deve accedere in remoto  al tuo dispositivo. Il dispositivo  controllato e tutti i suoi client devono utilizzare la stessa chiave d'accesso.
6. Premere il pulsante OK, , un beep e ed un avviso vocale vi informerà della avvenuta connessione.

### Controllare un altro computer
1. Aprire il menu NVDA, Strumenti, Accesso Remoto, Connetti.
2. Scegliere client nel primo gruppo di pulsanti radio.
3. Scegliere Controlla un altro PC nel secondo gruppo di pulsanti radio.
4. Nel campo host, immettere l'host del server a cui ci si connette, per esempio nvdaremote.com. Se il server in uso usa una porta alternativa, si può inserire l'Host con la sintassi &lt;host&gt;:&lt;port&gt; (per esempio nvdaremote.com:1234).
5. Inserire una chiave d'accesso nel campo di editazione apposito, oppure premere il pulsante genera chiave d'accesso. Il dispositivo  controllato e tutti i suoi client devono utilizzare la stessa chiave d'accesso.
6. Premere il pulsante OK, , un beep e ed un avviso vocale vi informerà della avvenuta connessione.

## Connessioni dirette
L'opzione server nella finestra di dialogo connessione consente di impostare una connessione diretta.
Una volta selezionata tale opzione, seleziona la modalità della tua connessione, se controllare un Pc o essere controllato.
Viceversa, l'altra persona si connetterà selezionando la modalità inversa.

Una volta selezionata la modalità, è possibile utilizzare il pulsante Ottieni Ip esterno per ottenere il vostro indirizzo IP esterno.
Assicurarsi che la porta sia aperta correttamente.

Se viene rilevato che la porta (6837) non è raggiungibile, viene visualizzato un messaggio di avviso.
Aprire la porta e riprovare.

Nota: Il processo di apertura delle porte va oltre lo scopo di questa guida. Consultare le informazioni fornite con il router per ulteriori istruzioni.

Immettere una chiave d'accesso, oppure premere il pulsante genera Chiave d'accesso. L'altra persona avrà bisogno del vostro IP esterno oltre alla chiave d'accesso per connettersi. Se è stata inserita una porta differente da quella di default (6837) nel campo di editazione Porta, assicurarsi che l'altra persona aggiunga la porta alternativa per l'indirizzo host con la sintassi &lt;external ip&gt;:&lt;port&gt;.

Una volta premuto OK, sarete connessi.
Quando l'altra persona si connette, è possibile utilizzare NVDA remote normalmente.

## Controllo del dispositivo remoto

Una volta stabilita la connessione, l'utente del dispositivo di controllo può premere   F11 per iniziare il controllo del dispositivo remoto (per esempio, eseguire comandi da tastiera o imput per il braille).
Quando NVDA annuncia  Controllo remoto, i comandi eseguiti dal dispositivo di controllo   andranno ad interagire  sul dispositivo remoto. Premere nuovamente F11 per interrompere l'inoltro dei comandi e tornare alla macchina di controllo.
Per una migliore compatibilità, assicurarsi che i layout tastiera corrispondano su entrambe le macchine.

## Condividere una sessione.

Per condividere un collegamento, in modo che un'altra persona può facilmente unirsi alla vostra sessione REMOTA, selezionare  "Copia link" dal menu.

Se vi siete connessi come dispositivo di controllo, questo link permetterà di controllare il dispositivo della persona a cui inviate il link.

Se invece avete dato il consenso per controllare il vostro dispositivo da un altro, il link servirà per permettere il controllo del vostro dispositivo alla persona a cui inviate il link.

Molte applicazioni consentono di attivare questo link automaticamente, ma se non è possibile  eseguirlo dall'applicazione specifica, può essere copiato negli appunti ed eseguito da la finestra di dialogo Esegui.

## Inoltro di Ctrl + Alt + Canc
Durante l'inoltro dei tasti, non è possibile inviare la combinazione Ctrl+Alt+Canc normalmente.
Se è necessario utilizzare questo comando, e il sistema remoto si trova su desktop sicuro, utilizzare la apposita voce dal menu.

## Controllare da  remoto un computer in modo automatico

In certi casi  può risultare indispensabile controllare il  vostro computer da remoto. Ciò è particolarmente utile se si viaggia e si desidera controllare il vostro PC di casa dal proprio laptop, o un computer in una stanza della casa, mentre si è seduti fuori, usando un altro PC. Con semplici passaggi è possibile impostare il controllo remoto in automatico.

1. Accedere al menu NVDA, scegliere Strumenti, quindi Accesso Remoto. Infine, premere Invio su Opzioni.
2. Selezionare la casella di controllo: "Connetti automaticamente al server di controllo all'avvio".
3. Selezionare se si vuole usare un server o un Host locale.
4. Selezionare il pulsante radio Consenti il controllo remoto di questo PC.
5. Se si sceglie di usare un server proprio, assicurarsi che la porta inserita sia aperta nel dispositivo controllato, e che il dispositivo che controlla ne abbia accesso. Di default la porta è 6837.
6. Se si usa un server remoto, inserire i dati nei campi Host e chiave d'accesso, premere invio sul pulsante OK. L'opzione Genera chiave non è disponibile in questa situazione. La cosa migliore è trovare una chiave che poi verrà ricordata in modo da poterla facilmente utilizzare da qualsiasi postazione remota.

Per un uso avanzato, è possibile anche configurare NVDA Remoto per connettersi a un server locale o remoto in modalità controller. Per far ciò, selezionare l'opzione Controlla un altro PC.

Nota: le opzioni relative alla connessione automatica all'avvio nella finestra di dialogo opzioni non avranno effetto fino al riavvio di NVDA.

## Silenziare la sintesi sul computer remoto
Se non si desidera ascoltare la sintesi del computer remoto, è sufficiente accedere al menu NVDA, Strumenti, Accesso Remoto. Usare la Freccia  giù fino a Silenzia il sintetizzatore del PC remoto, e premere Invio. Tener presente che questa opzione non disattiva l'output braille inviato dal dispositivo di controllo al dispositivo controllato.

## Terminare una sessione remota

Per terminare una sessione remota, effettuare le seguenti operazioni:

1. Sul Pc di controllo, premere F11 per interrompere il controllo remoto. Dovreste sentire il messaggio: "Controllo locale" Se invece si sente il messaggio Controllo remoto, premere nuovamente F11.
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
* Matthew McCubbin
* Jason Meddaugh
* ABDULAZIZ ALSHMASI.
* Tyler W Kavanaugh
* Casey Mathews
* Babbage B.V.
* Leonard de Ruijter

## Change Log

### Version 2.2

* IPv6 Support
* Support for new NVDA 2018.3 as well as older versions
* Support for model-specific Braille display gestures


### Version 2.1

* Fixed connection not saving when allowing this machine to be controlled
* Added a script to push the clipboard with ctrl+shift+NVDA+c
* Braille input now works in browse mode
* Support model specific braille display gestures
* The beeps generated by NVDA Remote no longer block NVDA

### Version 2.0

* Support for remote Braille
* Support for nvdaremote:// links
* Centered Dialogs to conform with the rest of NVDA
* Fixed portcheck to point at a domain we control, portcheck.nvdaremote.com
* Support automatically connecting to a control server in master mode
* Fixed rendering error in documentation
* Update to protocol version 2, which includes an origin field in every remote message
* Significant code cleanup allowing easier modifications in future


