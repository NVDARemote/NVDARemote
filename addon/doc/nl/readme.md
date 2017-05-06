#NVDA Externe Toegang
Versie 2.0

Welkom bij de NVDA Externe Toegang add-on, die u in staat stelt om verbinding te maken met een andere computer die gebruikt maakt van de gratis NVDA schermlezer. Het maakt hierbij geen verschil of u zich aan de andere kant van één en de zelfde ruimte, of aan de andere kant van de wereld bevindt. Verbinding maken is eenvoudig en er zijn slechts een aantal commando's om te onthouden. U kunt verbinding maken met de computer van een andere persoon, of een vertrouwd persoon toestaan om verbinding te maken met uw systeem voor het uitvoeren van routine-onderhoud, het vaststellen van een probleem of het geven van training.

##Voordat u begint

Het is nodig dat u NVDA geïnstalleerd hebt op beide computers, waarbij u tevens de NVDA Externe Toegang add-on dient te installeren. De installatie van zowel NVDA als de Externe Toegang add-on verlopen via de normale weg. Wanneer u hierover meer informatie zoekt, kunt u deze vinden in de gebruikershandleiding van NVDA.

##Updaten

Wanneer u de add-on update en deze ook op het beveiligd bureaublad gebruikt, wordt het aanbevolen om ook de kopie voor het beveiligd bureaublad te updaten.
Om dit te doen update u eerst de bestaande add-on. Ga daarna naar het NVDA-menu, Opties, Algemeen en activeer de knop "Huidige instellingen van NVDA gebruiken bij windows-aanmelding (administrative rechten vereist)".

##Het starten van een externe sessie via een relay server
###De te beheren computer
1. Open het NVDA-menu, Extra's, Externe toegang, Verbinden.
2. Kies voor client bij de eerste reeks met keuzerondjes.
3. In de tweede reeks keuzerondjes kiest u voor de optie Laat deze machine beheerd worden.
4. In het veld Adres vult u het adres van de server in waarnaar u gaat verbinden, bijvoorbeeld nvdaremote.com. Wanneer de betreffende server een alternatieve poort gebruikt, voert u het adres in in de vorm &lt;host&gt;:&lt;port&gt;, bijvoorbeeld nvdaremote.com:1234.
5. Vul in het veld sleutel een toegangssleutel in, of kies voor de knop Sleutel genereren.
Deze toegangssleutel wordt door anderen gebruikt om uw computer te beheren.
De machine die beheert wordt en de bijbehorende clients dienen gebruik te maken van de zelfde sleutel.
6. Druk op Ok. Wanneer de verbinding tot stand gebracht is hoort u twee pieptonen, evenals de melding Verbonden.

###De beherende computer
1. Open het NVDA-menu, Extra's, Externe toegang, Verbinden.
2. Kies voor client bij de eerste reeks met keuzerondjes.
3. In de tweede reeks keuzerondjes kiest u voor de optie Beheer een andere machine.
4. In het veld Adres vult u het adres van de server in waarnaar u gaat verbinden, bijvoorbeeld nvdaremote.com. Wanneer de betreffende server een alternatieve poort gebruikt, voert u het adres in in de vorm &lt;host&gt;:&lt;port&gt;, bijvoorbeeld nvdaremote.com:1234.
5. Vul in het veld sleutel een toegangssleutel in, of kies voor de knop Sleutel genereren.
De machine die beheert wordt en de bijbehorende clients dienen gebruik te maken van de zelfde sleutel.
6. Druk op Ok. Wanneer de verbinding tot stand gebracht is hoort u een toon, evenals de melding Verbonden.

##Directe verbindingen
De optie Server in het dialoogvenster Verbinden stelt u in staat om een directe verbinding te maken.
Wanneer u deze optie selecteert, dient u ook te selecteren in welke modus u uw kant van de verbinding dient te gebruiken.
De andere persoon zal met u verbinden via de tegenovergestelde modus.

Waneer u de juiste modus geselecteerd hebt, kunt u de knop Extern IP opvragen gebruiken om uw externe IP-adres te verkrijgen en er zeker van te zijn dat de in het invoerveld ingevoerde poort op de juiste wijze geopend is.
Wanneer portcheck detecteert dat uw poort (standaard 6837) niet bereikbaar is, zal er hierover een waarschuwing verschijnen.
Open in dat geval uw poort in uw router of firewall en probeer het nogmaals.
Let op: Het proces van het openen van poorten valt buiten het bestek van dit document. Raadpleeg de informatie bij uw router voor verdere instructies.

Voer in het veld Sleutel een toegangssleutel in, of laat een sleutel genereren. De andere persoon heeft zowel uw externe IP als de toegangssleutel nodig om verbinding te maken. Wanneer u in het poort invoerveld een poort hebt ingevoerd die afwijkt van de standaard (6837), dient u er zeker van te zijn dat de andere persoon de alternatieve poort toevoegt aan het serveradres in de vorm &lt;extern ip&gt;:&lt;poort&gt;.

Zodra er voor Ok gekozen wordt, zal de verbinding met uw eigen server tot stand worden gebracht. Zodra de andere persoon verbinding maakt, kunt u NVDA Externe Toegang op de normale manier gebruiken.

##De externe machine beheren

Zodra de sessie verbonden is, kan er vanaf de beherende machine op F11 gedrukt worden om de externe machine te beheren (bijv. door het doorsturen van toetsen op het toetsenbord of een brailleleesregel).
Zodra NVDA de melding Externe machine wordt beheert geeft, zullen de toetsen die u indrukt doorgestuurd worden naar de externe machine. Daarnaast zal, wanneer de beherende machine beschikt over een brailleleesregel, informatie van de externe machine worden weergegeven op de leesregel. Druk opnieuw op F11 om het doorsturen van toetsen te stoppen en terug te schakelen naar de beherende machine.
zorg ervoor dat de toetsenbordindelingen op beide machines overeenkomen voor de beste compatibiliteit.

##Het delen van een sessie

Om een link te delen zodat iemand anders eenvoudig kan deelnemen aan uw NVDA externe toegang sessie, selecteert u link kopiëren in het menu Externe toegang.
Wanneer u verbonden bent als de beherende computer, zal deze link de ander in staat stellen om te verbinden en beheert te worden.
Wanneer u in plaats daarvan uw computer hebt ingesteld om beheerd te worden, zal de link de ander in staat stellen om uw machine te heberen.
Veel applicaties zullen gebruikers in staat stellen om deze link automatisch te activeren. Mocht het zo zijn dat de link vanuit een specifieke applicatie niet uitgevoerd wordt, is het mogelijk deze naar het klembord te kopiëren en uit te voeren vanuit het dialoogvenster uitvoeren.

##Ctrl+Alt+Del sturen
Tijdens het doorsturen van toetsen is het niet mogelijk om de toetscombinatie Ctrl+Alt+Del via de normale weg door te sturen. 
Gebruik daarvoor dit commando.

##Het beheren van een onbeheerde Computer

Het zou kunnen zijn dat u soms de wens hebt om één van uw eigen computers extern te beheren. Dit is vooral handig wanneer u op reis bent en u uw thuis-PC wilt bedienen vanaf uw laptop. Of, mogelijk wilt u een computer beheren die zich in een kamer van uw huis bevindt, terwijl u zelf buiten zit met een andere PC. Een vrij eenvoudige voorbereiding maakt dit mogelijk.

1. Open het NVDA-menu en kies voor Extra's, waarna u kiest voor Externe toegang. Kies vervolgens voor Opties en druk op enter.
2. Plaats een aankruisvakje bij de optie met het opschrift: "Automatisch met beheerserver verbinden bij opstarten".
3. Maak een keuze voor een externe server, of kies ervoor om de server lokaal, op de zelfde computer, te hosten.
4. In de tweede reeks keuzerondjes kiest u voor de optie Laat deze machine beheerd worden.
5. Wanneer u de server zelf host, dient u er zeker van te zijn dat de poort zoals ingevoerd in het invoerveld poort (standaard 6837) op de te beheren machine bereikbaar is vanaf de beherende machines.
6. Wanneer u een externe server wilt gebruiken, vul de velden Adres en Sleutel in, tab naar Ok en druk op enter. De optie Sleutel genereren is niet beschikbaar in deze situatie. Het is hierbij het beste om te kiezen voor een sleutel die u kunt onthouden, zodat u deze sleutel vanaf iedere willekeurige locatie kunt gebruiken.

Voor geavanceerd gebruik kunt u NVDA Remote zo instellen dat er automatisch verbinding wordt gemaakt met een lokale of externe server in beheermodus. Wanneer u dit wilt, kiest u voor de optie Beheer een andere machine in de tweede reeks keuzerondjes.

Let op: De opties rondom het automatisch verbinden in het dialoogvenster opties zijn pas van kracht na het opnieuw opstarten van NVDA.


##Spraak dempen op de externe computer
Wanneer u de spraak van de externe computer niet wenst te horen, opent u het NVDA-menu en kiest u voor Extra's, waarna u kiest voor Externe toegang. Navigeer naar Externe spraak dempen en druk op enter.


##Een externe sessie beëindigen

Voor het beëindigen van een externe sessie doet u het volgende.

1. Op de beherende computer drukt u op F11 om het doorsturen van toetsen te stoppen. U krijgt de boodschap "Toetsen niet doorsturen" te horen. Wanneer u in plaats daarvan het bericht hoort dat de toetsen wel doorgestuurd worden, drukt u nogmaals op F11.

2. Open het NVDA-menu en kies voor Extra's, waarna u kiest voor Externe toegang. Druk vervolgens op enter bij de optie Verbinding verbreken.

##Klembord doorsturen
De optie Klembord doorsturen in het menu Externe toegang stelt u in staat om tekst vanaf uw klembord door te sturen naar de externe computer.
Wanneer deze optie geactiveerd wordt, wordt de tekst op het klembord verstuurd naar de externe machine.

##NVDA Externe Toegang confugireren voor een Beveiligd Bureaublad

Om externe toegang met NVDA te laten functioneren op het beveiligd bureaublad dient de add-on geïnstalleerd te worden in het NVDA-gebruikersprofiel dat gebruikt wordt bij het beveiligd bureaublad.

1. Kies vanuit het NVDA-menu voor Opties, en vervolgens voor Algemeen.

2. Tab naar de knop NVDA gebruiken bij windows-aanmelding (administrator rechten vereist), en druk op enter.

3. Beantwoord de vragen over het kopieren van instellingen en add-ons, en reageer eveneens op het eventuele bericht van Gebruikersaccountbeheer.
4. Zodra de instellingen gekopieerd zijn, drukt u op Enter op de knop OK. Tab vervolgens naar OK en druk nogmaals op Enter om het dialoogvenster te sluiten.

Zodra NVDA Externe Toegang geïnstalleerd is voor het beveiligd bureaublad en uw PC beheert wordt in een externe sessie, wordt ook het beveiligd bureaublad voorgelezen.

##bijdragen
Deze add-on is vertaald door [Babbage](http://www.babbage.com/), leverancier van elektronische hulpmiddelen voor blinden en slechtzienden. Babbage levert hulpmiddelen, biedt [trainingen](http://www.babbage.com/?page_id=198) aan binnen werk en studie situaties en verzorgt [softwarematige aanpassingen](http://www.babbage.com/?page_id=202) van werkplekken voor personen met een visuele beperking. Daarnaast verstrekt Babbage advies aan zowel organisaties, werknemers en scholieren/studenten over mogelijke technische oplossingen en benodigde persoonlijke trainingen. 

Babbage draagt de ontwikkeling van NVDA een warm hart toe en levert dan ook ondersteuning voor NVDA. Tevens is Babbage aanbieder van cursussen om met NVDA te leren werken. Daarnaast kunnen gebruikers met een serviceovereenkomst terecht bij de Babbage helpdesk met vragen of problemen rondom het gebruik van NVDA.

Verder hebben onderstaande personen hun bijdrage geleverd aan het project NVDA Externe Toegang, evenals anderen.

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
* Leonard de Ruijter

##Wijzigingen

### Versie 2.0

* Ondersteuning voor braille
* Ondersteuning voor nvdaremote:// links
* Dialoogvensters zijn nu gecentreerd in overeenkomst met de rest van NVDA
* Portcheck verwijst nu naar een domein in eigen beheer, portcheck.nvdaremote.com
* Ondersteuning voor automatisch verbinden met een beheerserver in beherende (master) modus
* Fout in het renderen van documentatie opgelost
* Update naar protocol versie 2, dat een origin veld bevat in ieder bericht
* Significante opruiming van code die gemakkelijkere modificaties mogelijk maakt in de toekomst
