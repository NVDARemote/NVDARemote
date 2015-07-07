#NVDA Externe Toegang
Versie 1.0

Welkom bij de NVDA Externe Toegang add-on, die u in staat stelt om verbinding te maken met een andere computer die gebruikt maakt van de gratis NVDA schermlezer. Het maakt hierbij geen verschil of u zich aan de andere kant van één en de zelfde ruimte, of aan de andere kant van de wereld bevindt. Verbinding maken is eenvoudig en er zijn slechts een aantal commando's om te onthouden. U kunt verbinding maken met de computer van een andere persoon, of een vertrouwd persoon toestaan om verbinding te maken met uw systeem voor het uitvoeren van routine-onderhoud, het vaststellen van een probleem of het geven van training.

##Voordat u begint

Het is nodig dat u NVDA geïnstalleerd hebt op beide computers, evenals de NVDA Externe Toegang add-on. De installatie van zowel NVDA als de Externe Toegang add-on verlopen via de normale weg. Wanneer u hierover meer informatie zoekt, kunt u deze vinden in de gebruikershandleiding van NVDA.

##Het starten van een externe sessie via een relay server
###De te beheren computer
1. Open het NVDA-menu, Extra's, Externe toegang, Verbinden.
2. Kies voor client bij de eerste reeks met keuzerondjes.
3. In de tweede reeks keuzerondjes kiest u voor de optie Laat deze machine beheerd worden.
4. In het veld Adres vult u het adres van de server in waarnaar u gaat verbinden, bijvoorbeeld nvdaremote.com.
5. Vul in het veld sleutel een toegangssleutel in, of kies voor de knop Sleutel genereren.
Deze toegangssleutel wordt door anderen gebruikt om uw computer te beheren.
De machine die beheert wordt en de bijbehorende clients dienen gebruik te maken van de zelfde sleutel.
6. Druk op Ok. Wanneer de verbinding tot stand gebracht is hoort u een toon, evenals de melding Verbonden.

###De beherende computer
1. Open het NVDA-menu, Extra's, Externe toegang, Verbinden.
2. Kies voor client bij de eerste reeks met keuzerondjes.
3. In de tweede reeks keuzerondjes kiest u voor de optie Beheer een andere machine.
4. In het veld Adres vult u het adres van de server in waarnaar u gaat verbinden, bijvoorbeeld nvdaremote.com.
5. Vul in het veld sleutel een toegangssleutel in, of kies voor de knop Sleutel genereren.
De machine die beheert wordt en de bijbehorende clients dienen gebruik te maken van de zelfde sleutel.
6. Druk op Ok. Wanneer de verbinding tot stand gebracht is hoort u een toon, evenals de melding Verbonden.

##Directe verbindingen
De optie Server in het dialoogvenster Verbinden stelt u in staat om een directe verbinding te maken.
Wanneer u deze optie selecteert, dient u ook te selecteren in welke modus uw kant van de verbinding dient te gebruiken.
De andere persoon zal met u verbinden via de tegenovergestelde modus.


Waneer u de juiste modus geselecteerd hebt, kunt u de knop Extern IP opvragen gebruiken om uw externe IP-adres te verkrijgen en er zeker van te zijn dat de poort op de juiste wijze geopend is.
Wanneer portcheck detecteert dat uw poort (6837) niet bereikbaar is, zal er hierover een waarschuwing verschijnen.
Open in dat geval uw poort in uw router of firewall en probeer het nogmaals.
Let op: Het proces van het openen van poorten valt buiten het bestek van dit document. Raadpleeg de informatie bij uw router voor verdere instructies.

Voer in het veld Sleutel een toegangssleutel in, of laat een sleutel genereren. De andere persoon heeft zowel uw externe IP als de toegangssleutel nodig om verbinding te maken.

Zodra er voor Ok gekozen wordt, zal de verbinding met uw eigen server tot stand worden gebracht. Zodra de andere persoon verbinding maakt, kunt u NVDA Externe Toegang op de normale manier gebruiken.

##Toetsen doorsturen
Zodra de sessie verbonden is, kan er vanaf de beherende machine op F11 gedrukt worden om toetsen door te sturen.
Zodra NVDA de melding Toetsen doorsturen geeft, zullen de toetsen die u indrukt doorgestuurd worden naar de externe machine. Druk opnieuw op F11 om het doorsturen van toetsen te stoppen en terug te schakelen naar de beherende machine.
zorg ervoor dat de toetsenbordindelingen op beide machines overeenkomen voor de beste compatibiliteit.

##Ctrl+Alt+Del sturen
Tijdens het doorsturen van toetsen is het niet mogelijk om de toetscombinatie Ctrl+Alt+Del via de normale weg door te sturen. 
Gebruik daarvoor dit commando.

##Het beheren van een onbeheerde Computer

Het zou kunnen zijn dat u soms de wens hebt om één van uw eigen computers extern te beheren. Dit is vooral handig wanneer u op reis bent en u uw thuis-PC wilt bedienen vanaf uw laptop. Of, mogelijk wilt u een computer beheren die zich in een kamer van uw huis bevindt, terwijl u zelf buiten zit met een andere PC. Een nauwelijks geavanceerde voorbereiding maakt dit mogelijk.

1. Open het NVDA-menu en kies voor Extra's, waarna u kiest voor Externe toegang. Kies vervolgens voor Opties en druk op enter.
2. Plaats een aankruisvakje bij de optie met het opschrift: "Automatisch met controleserver verbinden bij opstarten".
3. Vul de velden Adres en Sleutel in, tab naar Ok en druk op enter.
4. Let op: de optie Sleutel genereren is niet beschikbaar in deze situatie. Het is hierbij het beste om te kiezen voor een sleutel die u kunt onthouden, zodat u deze sleutel vanaf iedere willekeurige locatie kunt gebruiken.

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
Deze add-on is vertaald door Leonard de Ruijter namens het NVDA Nederlandstalig vertaalteam (nvda-nl@googlegroups.com). Verder hebben onderstaande personen hun bijdrage geleverd aan het project NVDA Externe Toegang, evenals anderen.

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