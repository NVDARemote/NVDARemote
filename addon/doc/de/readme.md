#Fernsteuerung für NVDA
Version 1.2

Willkommen zur Fernsteuerung für NVDA. Diese Erweiterung ermöglicht es Ihnen, eine Verbindung zu einem anderen Computer aufzubauen,sofern auf diesem der freie Screenreader NVDA läuft. Es macht keinen Unterschied, ob sich die Computer im Raum gegenüber oder in verschiedenen Kontinenten befinden. Eine Verbindung herzustellen ist einfach und es gibt nur sehr wenige Befehle, die Sie sich merken müssen. Sie können auf den Computer eines anderen Menschen zugreifen oder einer vertrauenswürdigen Person den Zugriff auf Ihren Computer gewähren, sodass diese Wartungsarbeiten, Problemdiagnosen oder Schulungen durchführen kann.

##bevor sie beginnen

Auf beiden Rechnern müssen sowohl NVDA als auch die Erweiterung Fernsteuerung für NVDA  installiert sein. 
Beide Installationsprozesse sind Standardverfahren. Wenn Sie weitere Informationen benötigen, finden Sie diese im NVDA-Benutzerhandbuch.

##Starten einer Sitzung unter Zuhilfenahme einer Vermittlungsstelle
###ferngesteuerter Rechner
1. Öffnen Sie das NVDA-Menü, wählen sie dort extras, Fernsteuerung, verbinden.
2. Wählen Sie im ersten Auswahlschalter den Eintrag "client" aus.
3. Wählen Sie im zweiten Auswahlschalter den Eintrag "Zulassen, dass dieser Computer gesteuert wird" aus.
4. Tragen Sie in das Eingabefeld "Rechner" die Adrese einer Vermittlungsstelle ein, über die die Verbindung abgewickelt werden soll (z.B. nvdaremote.com)
5. Tragen Sie in das Eingabefeld "Schlüssel" ein beliebiges Passwort ein oder drücken Sie den Schalter "Schlüssel erzeugen", um eines zu generieren.
der Schlüssel wird verwendet, um den Rechner fernzusteuern.
alle Clients, die die selbe Verbindung nutzen wollen, müssen denselben Schlüssel verwenden.
6. Drücken Sie den Schalter OK. Sobald die Verbindung(en) hergestellt wurde, werden Sie eine Tonfolge hören und die Meldung "Verbindung hergestellt" wird angezeigt.

###fernsteuernder Rechner
1. Öffnen Sie das NVDA-Menü, wählen sie dort extras, Fernsteuerung, verbinden.
2. Wählen Sie im ersten Auswahlschalter den Eintrag "client" aus.
3. Wählen Sie im zweiten Auswahlschalter den eintrag "einen anderen Computer steuern" aus.
4. Tragen Sie in das Eingabefeld "Rechner" die Adresse einer Vermittlungsstelle ein (z.B. nvdaremote.com)
5. Tragen Sie in das Eingabefeld "Schlüssel" ein beliebiges Passwort ein oder drücken Sie den Schalter "Schlüssel erzeugen", um eines zu generieren.
der ferngesteuerte Rechner und alle Clients müssen denselben Schlüsel verwenden.
6. Drücken Sie den Schalter OK. Sobald die Verbindung(en) hergestellt wurden, werden Sie eine Tonfolge hören und die Meldung "Verbindung hergestellt" wird ausgegeben.

##Direktverbindungen
Die Option "Server" im Dialog "Verbinden" erlaubt eine direkte Verbindung zwischen zwei Rechnern ohne eine Vermittlungsstelle.
Wählen sie den Modus aus, in dem ihr Rechner während der Verbindung betrieben werden soll.
Ihr Kommunikationspartner muss den jeweils gegenteiligen Modus auswählen.

Sobald Sie den Modus ausgewählt haben, können Sie den Schalter "externe IP ermitteln" verwenden, um ihre externe (öffentliche) Ip-Adresse herauszufinden und
prüfen, ob der erforderliche Tcp_ip-Anschluss korrekt an Ihren Rechner weitergeleitet wird.
Fällt die Prüfung negativ aus, wird wahrscheinlich der erforderliche Anschluss /6837) nicht an Ihren Rechner weitergeleitet. In diesem Fall wird eine Warnung angezeigt.
Sorgen Sie für eine korrekte Weiterleitung des Tcp-Ip-Anschlusses und versuchen Sie es erneut.
Anmerkung: Das weiterleiten von TCp-Ip-Anschlüssen sprengt den Rahmen dieser Dokumentation. Sehen Sie im Benutzerhandbuch Ihres Routers in Kapiteln wie "Port-Weiterleitung" für weitere informationen nach.

Geben Sie in das Feld "Schlüssel" ein Passwort ein oder drücken Sie den Schalter "Schlüssel erzeugen" um eines zu generieren. Ihr Kommunikationspartner wird zum Herstellen einer Verbindung Ihre externe Ip-Adresse und das Passwort benötigen.

Sobald Sie OK drücken, wird die Verbindung hergestellt.
Sobald Ihr Kommunikationspartner die Verbindung hergestellt hat, können Sie Fernsteuerung für NVDA  normal verwenden.

##senden von Tastenanschlägen
Sobald die Verbindung hergestellt wurde, können Sie F11 drücken, um alle Tastenanschläge an den anderen Rechner zu übertragen.
Um zu Ihrem Rechner zurückzuschalten, drücken Sie ein weiteres Mal F11.
Es wird empfohlen, auf beiden Rechnern dasselbe Tastaturschema einzustellen.

##senden von strg+alt+entf
Wenn die Übertragung von Tastenanschlägen aktiviert ist, können Sie die Tastenkombination strg+alt+entf nicht übertragen.
Falls Sie strg+alt+entf an den entfernten Rechner übertragen (und dessen sicheren Desktop steuern) müssen, verwenden Sie den entsprechenden Befehl.

##Fernsteuerung eines unbeaufsichtigten Rechners

Manchmal möchten Sie vielleicht einen Ihrer eigenen Computer aus der Ferne steuern. Dies ist besonders hilfreich, wenn Sie unterwegs sind und Ihren Heim-PC von Ihrem Laptop steuern möchten. Oder möchten Sie vielleicht einen Computer in einem Raum Ihres Hauses steuern, während Sie mit einem anderen PC draußen sitzen. Ein wenig Vorbereitung macht dies bequem möglich.
 
1. Öffnen Sie das NVDA-Menü und  wählen Sie Extras, Fernsteuerung und zuletzt Optionen.
2. Hier Aktivieren Sie das Kontrollkästchen "beim Start automatisch mit Server verbinden".
3. Nun Füllen Sie die Felder Rechner und Schlüssel aus und bestätigen mit Eingabe.
4. Bitte beachten Sie, dass die Option "Schlüssel erzeugen" hier nicht zur Verfügung steht. Es ist das beste, wenn Sie einen Schlüssel verwenden, an welchen Sie sich jederzeit erinnern können.
 
##Stummschalten der Sprache auf einem ferngesteuerten Rechner
Wenn Sie die Sprache auf dem ferngesteuerten Rechner stummschalten wollen, wählen Sie im NVDA-Manü den Befehl Extras --> Fernsteuerung --> entfernte Sprache stummschalten aus


##Beenden einer Fernsteuerungssitzung

Wenn Sie eine Verbindung mit einem ferngesteuerten Rechner beenden wollen, gehen Sie folgendermaßen vor:

1. Drücken Sie auf dem fernsteuernden Rechner so oft F11, bis das Senden von Tastenanschlägen aktiviert ist.

2. Wählen Sie den Befehl extras --> Fernsteuerung --> Verbindung trennen aus dem NVDA-Menü aus.

##Übertragen der Zwischenablage
Wenn Sie diese Option im Menü extras --> Fernsteuerung im NVDA-Menü aktivieren, werden jegliche Daten, die Sie in die Zwischenablage kopieren, an den ferngesteuerten Rechner übertragen, sofern eine Verbindung besteht.


##Einrichten der Fernsteuerung auf sicheren Desktops

Damit NVDA über eine NVDARemote-Verbindung hinweg auch auf sicheren Desktops funktioniert, muss die Erweiterung in NVDA-Instanzen installiert werden, die auf sicheren Desktops ausgeführt werden. Gehen Sie folgendermaßen vor, um NVDA auf sicheren Desktops einzurichten:

1. Öffnen Sie die allgemeinen einstellungen

2. Drücken Sie den Schalter "Aktuell gespeicherte Einstellungen im Anmeldebildschirm und bei Sicherheitsmeldungen verwenden (erfordert Administrationsberechtigungen)".

3. Beantworten Sie die Nachfrage zum Kopieren der Einstellungen sowie die Nachfrage der Benutzerkontensteuerung mit "ja".
4. Schließen Sie das Dialogfeld mit OK.

Von nun an wird NVDA auch in Sicheren Desktops funktionieren, wenn eine Remoteverbindung besteht.


##UnterstützerInnen
We would like to acknowledge the following contributors, among others, who helped make the NVDA Remote project a reality.

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
