#Fernsteuerung für NVDA
Version 2.1

Willkommen zur Fernsteuerung für NVDA. Diese Erweiterung ermöglicht es Ihnen, eine Verbindung zu einem anderen Computer aufzubauen,sofern auf diesem der freie Screenreader NVDA läuft. Es macht keinen Unterschied, ob sich die Computer im Raum gegenüber oder in verschiedenen Kontinenten befinden. Eine Verbindung herzustellen ist einfach und es gibt nur sehr wenige Befehle, die Sie sich merken müssen. Sie können auf den Computer eines anderen Menschen zugreifen oder einer vertrauenswürdigen Person den Zugriff auf Ihren Computer gewähren, sodass diese Wartungsarbeiten, Problemdiagnosen oder Schulungen durchführen kann.

##bevor sie beginnen
Auf beiden Rechnern müssen sowohl NVDA als auch die Erweiterung Fernsteuerung für NVDA  installiert sein. Beide Installationsprozesse sind Standardverfahren. Wenn Sie weitere Informationen benötigen, finden Sie diese im NVDA-Benutzerhandbuch.

##Aktualisierung
Wenn Sie Fernsteuerung für NVDA für den sicheren Desktop installiert haben, wird empfohlen, die Kopie auch auf dem sicheren Desktop zu aktualisieren. Aktualisieren Sie dazu zunächst Ihr bestehendes Addon. Öffnen Sie dann das NVDA-Menü, Optionen, Einstellungen, Allgemein, und klicken Sie auf die Schaltfläche "Aktuell gespeicherte Einstellungen im Anmeldebildschirm und bei Sicherheitsmeldungen verwenden (erfordert Administrationsberechtigungen)".

##Starten einer Sitzung unter Zuhilfenahme einer Vermittlungsstelle
###ferngesteuerter Rechner
1. Öffnen Sie das NVDA-Menü, wählen sie dort extras, Fernsteuerung, verbinden.
2. Wählen Sie im ersten Auswahlschalter den Eintrag "client" aus.
3. Wählen Sie im zweiten Auswahlschalter den Eintrag "Zulassen, dass dieser Computer gesteuert wird" aus.
4. Tragen Sie in das Eingabefeld "Rechner" die Adresse einer Vermittlungsstelle ein, über die die Verbindung abgewickelt werden soll (z.B. nvdaremote.com). Wenn der jeweilige Server einen alternativen Port verwendet, können Sie den Host in der Form &lt;host&gt;:&lt;port&gt; eingeben, z.B. nvdaremote.com:1234.
5. Tragen Sie in das Eingabefeld "Schlüssel" ein beliebiges Passwort ein oder drücken Sie den Schalter "Schlüssel erzeugen", um eines zu generieren.
der Schlüssel wird verwendet, um den Rechner fernzusteuern.
alle Clients, die die selbe Verbindung nutzen wollen, müssen denselben Schlüssel verwenden.
6. Drücken Sie den Schalter OK. Sobald die Verbindung(en) hergestellt wurde, werden Sie eine Tonfolge hören und die Meldung "Verbindung hergestellt" wird angezeigt.

###fernsteuernder Rechner
1. Öffnen Sie das NVDA-Menü, wählen sie dort extras, Fernsteuerung, verbinden.
2. Wählen Sie im ersten Auswahlschalter den Eintrag "client" aus.
3. Wählen Sie im zweiten Auswahlschalter den eintrag "einen anderen Computer steuern" aus.
4. Tragen Sie in das Eingabefeld "Rechner" die Adresse einer Vermittlungsstelle ein (z.B. nvdaremote.com). Wenn der jeweilige Server einen alternativen Port verwendet, können Sie den Host in der Form &lt;host&gt;:&lt;port&gt; eingeben, z.B. nvdaremote.com:1234.
5. Tragen Sie in das Eingabefeld "Schlüssel" ein beliebiges Passwort ein oder drücken Sie den Schalter "Schlüssel erzeugen", um eines zu generieren.
der ferngesteuerte Rechner und alle Clients müssen denselben Schlüssel verwenden.
6. Drücken Sie den Schalter OK. Sobald die Verbindung(en) hergestellt wurden, werden Sie eine Tonfolge hören und die Meldung "Verbindung hergestellt" wird ausgegeben.

##Direktverbindungen
Die Option "Server" im Dialog "Verbinden" erlaubt eine direkte Verbindung zwischen zwei Rechnern ohne eine Vermittlungsstelle.
Wählen sie den Modus aus, in dem ihr Rechner während der Verbindung betrieben werden soll.
Ihr Kommunikationspartner muss den jeweils gegenteiligen Modus auswählen.
Sobald Sie den Modus ausgewählt haben, können Sie den Schalter "externe IP ermitteln" verwenden, um ihre externe (öffentliche) Ip-Adresse herauszufinden und prüfen, ob der erforderliche Tcp_ip-Anschluss korrekt an Ihren Rechner weitergeleitet wird.
Fällt die Prüfung negativ aus, wird wahrscheinlich der erforderliche Anschluss (6837) nicht an Ihren Rechner weitergeleitet. In diesem Fall wird eine Warnung angezeigt.
Sorgen Sie für eine korrekte Weiterleitung des Tcp-Ip-Anschlusses und versuchen Sie es erneut.
Anmerkung: Das weiterleiten von TCp-Ip-Anschlüssen sprengt den Rahmen dieser Dokumentation. Sehen Sie im Benutzerhandbuch Ihres Routers in Kapiteln wie "Port-Weiterleitung" für weitere informationen nach.
Geben Sie in das Feld "Schlüssel" ein Passwort ein oder drücken Sie den Schalter "Schlüssel erzeugen" um eines zu generieren. Ihr Kommunikationspartner wird zum Herstellen einer Verbindung Ihre externe Ip-Adresse und das Passwort benötigen. Wenn Sie im Feld Port einen anderen Port als den Standardport (6837) eingegeben haben, stellen Sie sicher, dass die andere Person den alternativen Port in der Form &lt;externe IP&gt;:&lt;Port&gt; an die Hostadresse anhängt.
Sobald Sie OK drücken, wird die Verbindung hergestellt.
Sobald Ihr Kommunikationspartner die Verbindung hergestellt hat, können Sie Fernsteuerung für NVDA  normal verwenden.

##Steuern des entfernten Rechners
Sobald die Verbindung hergestellt wurde, können Sie F11 drücken, um den anderen Rechner zu steuern (z.B. durch Senden von Tastenanschlägen oder Braille-Eingabe). Wenn NVDA sagt, dass der ferngesteuerte Rechner gesteuert wird, werden die Tasten der Tastatur und der Braillezeile, die Sie drücken, an den ferngesteuerten Rechner weitergeleitet. Wenn der steuernde Rechner eine Braillezeile verwendet, werden außerdem Informationen vom entfernten Rechner angezeigt. Um zu Ihrem Rechner zurückzuschalten, drücken Sie ein weiteres Mal F11.
Es wird empfohlen, auf beiden Rechnern dasselbe Tastaturschema einzustellen.

##Gemeinsame Nutzung Ihrer Sitzung
Um einen Link freizugeben, so dass jemand anderes Ihrer NVDA REMOTE-Sitzung beitreten kann, wählen Sie "Link kopieren" aus dem Menü "Fernsteuerung". Wenn Sie als steuernder Computer angeschlossen sind, ermöglicht dieser Link, dass sich jemand anderes verbinden und gesteuert werden kann. Wenn Sie stattdessen Ihren Computer so eingerichtet haben, dass er gesteuert werden kann, können die Personen, mit denen Sie ihn teilen, Ihren Computer steuern. Viele Anwendungen erlauben es Benutzern, diesen Link automatisch zu aktivieren, aber wenn er nicht innerhalb einer bestimmten Anwendung ausgeführt wird, kann er in die Zwischenablage kopiert und über den Ausführungsdialog ausgeführt werden.

##senden von strg+alt+entf
Wenn die Übertragung von Tastenanschlägen aktiviert ist, können Sie die Tastenkombination strg+alt+entf nicht übertragen.
Falls Sie strg+alt+entf an den entfernten Rechner übertragen (und dessen sicheren Desktop steuern) müssen, verwenden Sie den entsprechenden Befehl.

##Fernsteuerung eines unbeaufsichtigten Rechners
Manchmal möchten Sie vielleicht einen Ihrer eigenen Computer aus der Ferne steuern. Dies ist besonders hilfreich, wenn Sie unterwegs sind und Ihren Heim-PC von Ihrem Laptop steuern möchten. Oder möchten Sie vielleicht einen Computer in einem Raum Ihres Hauses steuern, während Sie mit einem anderen PC draußen sitzen. Ein wenig Vorbereitung macht dies bequem möglich.
 
1. Öffnen Sie das NVDA-Menü und  wählen Sie Extras, Fernsteuerung und zuletzt Optionen.
2. Hier Aktivieren Sie das Kontrollkästchen "beim Start automatisch mit Server verbinden".
3. Wählen Sie, ob Sie einen entfernten Server verwenden, oder den Server selbst bereit stellen möchten.
4. Wählen Sie "Zulassen, dass dieser Computer gesteuert wird" im zweiten Satz der Auswahlknöpfe.
5. Wenn Sie den Server selbst bereit stellen, müssen Sie sicherstellen, dass der Port, der im Feld Port auf dem ferngesteuerten Rechner eingetragen ist (standardmäßig 6837), von den steuernden Rechnern aus erreichbar ist.
6. Wenn Sie einen entfernten Server verwenden, Füllen Sie die Felder Rechner und Schlüssel aus und bestätigen mit Eingabe. Bitte beachten Sie, dass die Option "Schlüssel erzeugen" hier nicht zur Verfügung steht. Es ist das beste, wenn Sie einen Schlüssel verwenden, an welchen Sie sich jederzeit erinnern können.

Für den erweiterten Einsatz können Sie Fernsteuerung für NVDA auch so konfigurieren, dass eine automatische Verbindung zu einem lokalen oder entfernten Server im Kontrollmodus hergestellt wird. Wenn Sie dies wünschen, wählen Sie im zweiten Satz der Auswahlknöpfe die Option "Einen anderen Computer steuern".
Hinweis: Die Optionen zum automatischen Verbindungsaufbau gelten erst nach einem Neustart von NVDA.

##Stummschalten der Sprache auf einem ferngesteuerten Rechner
Wenn Sie die Sprache des entfernten Computers oder NVDA-spezifische Töne nicht hören möchten, wählen Sie im NVDA-Menü den Befehl Extras, Fernsteuerung entfernte Sprache stumm schalten aus. Bitte beachten Sie, dass dadurch die Brailleausgabe nicht deaktiviert wird, solange der steuernde Rechner Tastenanschläge sendet.

##Beenden einer Fernsteuerungssitzung
Wenn Sie eine Verbindung mit einem ferngesteuerten Rechner beenden wollen, gehen Sie folgendermaßen vor:

1. Drücken Sie auf dem steuernden Computer F11, um die Steuerung des entfernten Rechners zu beenden. Sie sollten die Nachricht hören oder lesen: "Lokalen Rechner steuern". Wenn Sie stattdessen eine Meldung hören oder lesen, dass Sie den entfernten Rechner steuern, drücken Sie erneut F11.
2. Rufen Sie das NVDA-Menü auf, dann Extras, Fernsteuerung, und drücken Sie bei "Verbindung trennen" die Eingabetaste.

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
Wir möchten unter anderem die folgenden Mitwirkenden würdigen, die dazu beigetragen haben, das Projekt "Fernsteuerung für NVDA" Wirklichkeit werden zu lassen.

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

##Änderungsprotokoll
###Version 2.1
* Behoben: Die Verbindung wurde nicht gespeichert, wenn das System gesteuert wird
* Script hinzugefügt, um die Zwischenablage mit Strg+Umschalt+NVDA+c zu übertragen
* Braille-Eingabe funktioniert jetzt im Lesemodus
* Unterstützt modellspezifische Braillezeilengesten
* Die von Fernsteuerung für NVDA erzeugten Pieptöne blockieren NVDA nicht mehr.

###Version 2.0
* Unterstützung für entfernte Braillesteuerung
* Unterstützung für nvdaremote:// Links
* Zentrierte Dialoge zur Anpassung an den Rest von NVDA
* Portcheck auf eine von uns kontrollierte Domain, portcheck.nvdaremote.com, korrigiert.
* Unterstützung der automatischen Verbindung zu einem Steuerungsserver im Master-Modus
* Darstellungsfehler in der Dokumentation behoben
* Update auf Protokollversion 2, die in jeder Remote-Nachricht ein Herkunftsfeld enthält.
* Signifikante Code-Bereinigung, die in Zukunft einfachere Änderungen ermöglicht