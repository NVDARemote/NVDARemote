# NVDA-etäkäyttö
Versio 2.1

Tervetuloa NVDA-etäkäyttö-lisäosaan, jonka avulla voit yhdistää toiseen ilmaista NVDA-ruudunlukuohjelmaa käyttävään tietokoneeseen. On yhdentekevää, oletko  samassa huoneessa tai toisella puolen maailmaa. Yhdistäminen on yksinkertaista, ja muistettavia komentojakin on vain muutama. Voit yhdistää toisen henkilön tietokoneeseen tai sallia luotetun henkilön yhdistää järjestelmääsi ylläpitorutiinien suorittamista, ongelman diagnosointia tai koulutuksen tarjoamista varten.

## Ennen kuin aloitat
NVDA ja tämä etäkäyttölisäosa on oltava asennettuna molemmissa tietokoneissa.
Molempien asennusvaiheet ovat standardinmukaisia. Katso lisätietoja NVDA:n käyttöoppaasta, mikäli tarvitset apua.

## Päivittäminen
Mikäli olet asentanut NVDA-etäkäytön suojatulle työpöydälle,  lisäosaa päivitettäessä on suositeltavaa, että päivität myös sen version.
Tämä tehdään päivittämällä ensin olemassa oleva lisäosa ja valitsemalla sitten NVDA-valikosta Asetukset -> Yleiset ja painamalla "Käytä tallennettuja asetuksia kirjautumisikkunassa ja muissa suojatuissa ruuduissa (edellyttää järjestelmänvalvojan oikeuksia)" -painiketta.

## Etäistunnon aloittaminen välittäjäpalvelimen kautta
### Hallittavassa tietokoneessa
1. Avaa NVDA-valikko ja valitse Työkalut -> Etäkäyttö -> Yhdistä.
2. Valitse ensimmäisestä valintapainikeryhmästä Asiakas.
3. Valitse toisesta valintapainikeryhmästä Salli tämän tietokoneen hallinta.
4. Kirjoita Isäntä-muokkauskenttään sen palvelimen osoite, johon olet yhdistämässä, esimerkiksi nvdaremote.com. Jos palvelin käyttää vaihtoehtoista porttia, voit kirjoittaa isäntäkoneen muodossa &lt;isäntä&gt;:&lt;portti&gt;, esim. nvdaremote.com:1234.
5. Kirjoita Avain-muokkauskenttään haluamasi avain tai paina Luo avain -painiketta.
Avainta käytetään tietokoneesi hallitsemiseen.
Hallittavan koneen ja kaikkien siihen yhdistävien asiakaskoneiden on käytettävä samaa avainta.
6. Paina OK. Kun yhteys on muodostettu, kuulet äänimerkin ja "Yhdistetty"-ilmoituksen.

### Hallitsevassa tietokoneessa
1. Avaa NVDA-valikko ja valitse Työkalut -> Etäkäyttö -> Yhdistä.
2. Valitse ensimmäisestä valintapainikeryhmästä Asiakas.
3. Valitse toisesta valintapainikeryhmästä Hallitse toista konetta.
4. Kirjoita Isäntä-muokkauskenttään sen palvelimen osoite, johon olet yhdistämässä, esimerkiksi nvdaremote.com. Jos palvelin käyttää vaihtoehtoista porttia, voit kirjoittaa isäntäkoneen muodossa &lt;isäntä&gt;:&lt;portti&gt;, esim. nvdaremote.com:1234.
5. Kirjoita Avain-kenttään haluamasi avain tai paina Luo avain -painiketta.
Hallittavan koneen ja kaikkien siihen yhdistävien asiakaskoneiden on käytettävä samaa avainta.
6. Paina OK. Kun yhteys on muodostettu, kuulet äänimerkin ja "Yhdistetty"-ilmoituksen.

## Suorat yhteydet
Yhdistä-valintaikkunan Palvelin-vaihtoehdolla voit muodostaa suoran yhteyden.
Kun se on valittuna, sinun on myös valittava, missä tilassa yhteytesi tulee olemaan.
Toinen osapuoli yhdistää koneeseesi päinvastaista vaihtoehtoa käyttäen.

Kun tila on valittu, voit käyttää Hae ulkoinen IP -painiketta noutaaksesi ulkoisen IP-osoitteesi ja varmistaaksesi, että Portti-muokkauskenttään syötetty portti on uudelleenohjattu asianmukaisesti.
Jos portintarkistus havaitsee, ettei porttiin (oletusarvoisesti 6837) saada yhteyttä, näkyviin tulee siitä kertova varoitus.
Sinun on tällöin uudelleenohjattava porttisi ja yritettävä sitten uudelleen.
Huom: Porttien uudelleenohjausta ei käsitellä tässä dokumentissa. Katso lisätietoja reitittimesi mukana toimitetuista ohjeista.

Kirjoita haluamasi avain Avain-muokkauskenttään tai paina Luo avain -painiketta. Toinen osapuoli tarvitsee yhdistämiseen ulkoisen IP-osoitteesi lisäksi tämän avaimen. Mikäli syötit Portti-muokkauskenttään muun kuin oletusportin (6837), varmista, että toinen osapuoli lisää isäntäkoneen osoitteeseen vaihtoehtoisen portin muodossa &lt;ulkoinen IP&gt;:&lt;portti&gt;.

Yhteys muodostetaan painettuasi OK-painiketta.
Kun toinen osapuoli yhdistää koneeseesi, voit käyttää NVDA-etäkäyttöä normaalisti.

## Etäkoneen hallinta
Kun yhteys on muodostettu, etäkoneen hallinta (esim. näppäinpainallusten tai pistekirjoitussyötteen lähettäminen) voidaan aloittaa painamalla hallitsevassa koneessa F11.
Kun NVDA sanoo Hallitaan etäkonetta, painamasi näppäimistön ja pistenäytön näppäimet suoritetaan etäkoneessa. Lisäksi, jos hallitsevassa tietokoneessa käytetään pistenäyttöä, kaikki etäkoneen palaute näytetään siinä. Lopeta näppäinpainallusten lähettäminen ja vaihda takaisin hallitsevaan koneeseen painamalla uudestaan F11.
Varmista parhaan yhteensopivuuden takaamiseksi, että molemmissa koneissa on käytössä sama näppäinasettelu.

## Istunnon jakaminen
Jotta muut voivat helposti liittyä NVDA-etäkäyttöistuntoosi, valitse Etäkäyttö-valikosta Kopioi linkki -vaihtoehto.
Mikäli olet yhteydessä hallitsevana tietokoneena, tämä linkki sallii jonkun muun henkilön yhdistää tietokoneeseesi sekä hänen koneensa hallitsemisen.
Jos sen sijaan olet määrittänyt tietokoneesi hallittavaksi, linkki sallii henkilöiden, joille sen jaat, hallita konettasi.
Useat sovellukset mahdollistavat linkin automaattisen avaamisen, mutta mikäli se ei onnistu jossain määrätyssä sovelluksessa, se voidaan kopioida leikepöydälle ja avata Suorita-valintaikkunasta.

## Lähetä Ctrl+Alt+Del
Ctrl+Alt+Del-näppäinyhdistelmän lähettäminen ei ole mahdollista näppäinpainalluksia lähetettäessä.
Käytä tätä komentoa, mikäli sinun on lähetettävä Ctrl+Alt+Del etäjärjestelmälle, jossa suojattu työpöytä on aktiivisena.

## Valvomattoman tietokoneen etähallinta
Saatat joskus haluta etähallita omaa konettasi. Tämä on erityisen hyödyllistä matkoilla ollessasi ja halutessasi hallita kotikonetta kannettavallasi, tai kotona sisällä talossa olevaa konetta ollessasi itse ulkona toisen koneen kanssa. Tämä on mahdollista pienellä valmistelulla.

1. Avaa NVDA-valikko ja valitse Työkalut ja sitten Etäkäyttö. Paina lopuksi Enter Asetukset-vaihtoehdon kohdalla.
2. Valitse valintaruutu "Yhdistä hallintapalvelimeen automaattisesti käynnistyksen yhteydessä".
3. Valitse, käytetäänkö etävälittäjäpalvelinta vai isännöidäänkö yhteyttä paikallisesti. 
4. Valitse toisena olevasta valintapainikeryhmästä Salli tämän koneen hallinta.
5. Mikäli isännöit yhteyttä itse, sinun on varmistettava, että  hallitsevista koneista saadaan yhteys hallitsevassa koneessa Portti-muokkauskenttään syötettyyn porttiin (oletusarvoisesti 6837).
6. Jos haluat käyttää välittäjäpalvelinta, täytä sekä Isäntä- että Avain-muokkauskentät, siirry Sarkaimella OK-painikkeen kohdalle ja paina Enter. Luo avain -vaihtoehto ei ole käytettävissä, joten parasta on keksiä helposti muistettava avain, jotta voit käyttää sitä mistä tahansa etäsijainnista.
Voit  määrittää NVDA-etäkäytön yhdistämään edistynyttä käyttöä varten myös automaattisesti paikalliseen tai etävälittäjäpalvelimeen hallintatilassa. Tämä tehdään valitsemalla Hallitse toista konetta toisena olevasta valintapainikeryhmästä.

Huom: Asetukset-valintaikkunan automaattiseen käynnistyksen yhteydessä yhdistämiseen liittyvillä vaihtoehdoilla ei ole vaikutusta ennen NVDA:n uudelleenkäynnistystä.

## Puheen mykistäminen etätietokoneessa
Jos et halua kuulla etäkoneen puhetta tai NVDA:n äänimerkkejä, avaa NVDA-valikko ja valitse Työkalut -> Etäkäyttö. Siirry lopuksi Nuoli alas -näppäimellä kohtaan Mykistä etäkone ja paina Enter. Huom: Tämä asetus ei poista käytöstä hallitsevan koneen pistenäytölle tuotettavaa etäpistekirjoituspalautetta, mikäli hallitsevan koneen näppäinpainallusten lähettäminen on käytössä.

## Etäistunnon lopettaminen
Lopeta etäistunto seuraavasti:

1. Lopeta etäkoneen hallinta painamalla hallitsevassa koneessa F11. NVDA:n pitäisi nyt sanoa tai pistenäytöllä lukea "Hallitaan paikallista konetta". Jos sen sijaan kuulet tai näet pistenäytöllä ilmoituksen etäkoneen hallitsemisesta, paina vielä kerran F11.
2. Avaa NVDA-valikko, valitse Työkalut -> Etäkäyttö ja paina Enter Katkaise yhteys -vaihtoehdon kohdalla.

## Leikepöydän lähettäminen
Etäkäyttö-valikon Lähetä leikepöytä -vaihtoehdolla voit lähettää leikepöydällä olevan tekstin.
Kun toiminto on otettu käyttöön, kaikki leikepöydällä oleva teksti lähetetään toisille koneille.

## NVDA-etäkäytön määrittäminen toimimaan suojatulla työpöydällä
Jotta NVDA-etäkäyttö-lisäosa toimisi suojatulla työpöydällä, se on asennettava suojatulla työpöydällä käynnissä olevaan NVDA:han.

1. Valitse NVDA-valikosta Asetukset -> Yleiset.
2. Siirry Sarkaimella Käytä tallennettuja asetuksia kirjautumis- ja muissa suojatuissa ruuduissa (edellyttää järjestelmänvalvojan oikeuksia) -painikkeen kohdalle ja paina Enter.
3. Vastaa Kyllä kysymyksiin asetustesi ja lisäosien kopioinnista sekä mahdollisesti näkyviin tulevaan Käyttäjätilien valvonnan kehotteeseen.
4. Kun asetukset on kopioitu, paina Enter sulkeaksesi siitä kertovan ilmoituksen. Siirry sitten sarkaimella OK-painikkeen kohdalle ja paina vielä kerran Enter sulkeaksesi valintaikkunan.

Kun NVDA-etäkäyttö on asennettu suojatulle työpöydälle ja konettasi hallitaan etäistunnossa, puhe ja pistenäyttö ovat käytettävissä suojatulle työpöydälle siirryttäessä.

## Avustajat
Haluamme kiittää muiden muassa seuraavia henkilöitä, jotka auttoivat tekemään NVDA Remote -projektista todellisuutta.

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

## Muutosloki

### Versio 2.1
* Korjattu tallentumaton yhteys, kun tietokoneen hallinta sallitaan.
* Lisätty skripti leikepöydän lähettämiseen näppäinkomennolla Ctrl+Shift+NVDA+C.
* Pistekirjoituksen syöttö toimii nyt selaustilassa.
* Tuki pistenäyttöjen mallikohtaisille komennoille
* NVDA-etäkäytön tuottamat äänimerkit eivät enää estä NVDA:ta.

### Versio 2.0
* Tuki etäpistekirjoitukselle
* Tuki nvdaremote://-linkeille
* Valintaikkunat keskitetty vastaamaan NVDA:n muita ikkunoita
* Portintarkistus korjattu viittaamaan  hallinnoimaamme portcheck.nvdaremote.com-domainiin
* Tuki automaattiselle hallintapalvelimeen yhdistämiselle hallintatilassa
* Korjattu dokumentaation hahmonnusvirhe
* Protokolla päivitetty versioon 2, jonka jokaiseen etäviestiin sisältyy origin-kenttä
* Koodia siivottu huomattavasti, mikä mahdollistaa tulevaisuudessa helpommat muokkaukset
