#NVDA-etäkäyttö
Versio 1.2

Tervetuloa NVDA-etäkäyttö-lisäosaan, jonka avulla voit yhdistää toiseen ilmaista NVDA-ruudunlukuohjelmaa käyttävään tietokoneeseen. On yhdentekevää, oletko  samassa huoneessa tai toisella puolen maailmaa. Yhdistäminen on yksinkertaista, ja muistettavia komentojakin on vain muutama. Voit yhdistää toisen henkilön tietokoneeseen tai sallia luotetun henkilön yhdistää järjestelmääsi ylläpitorutiinien suorittamista, ongelman diagnosointia tai opetuksen tarjoamista varten.

##Ennen kuin aloitat

NVDA ja NVDA-etäkäyttö-lisäosa on oltava asennettuna molemmissa tietokoneissa.
Molempien asennusvaiheet ovat standardinmukaisia. Katso lisätietoja NVDA:n käyttöoppaasta, mikäli tarvitset apua.

##Etäistunnon aloittaminen välittäjäpalvelimen kautta
###Hallittava tietokone
1. Avaa NVDA-valikko ja valitse Työkalut -> Etäkäyttö -> Yhdistä.
2. Valitse ensimmäisestä valintapainikeryhmästä Asiakas-vaihtoehto.
3. Valitse toisesta valintapainikeryhmästä Salli tämän tietokoneen hallinta -vaihtoehto.
4. Kirjoita Isäntä-muokkauskenttään sen palvelimen osoite, johon olet yhdistämässä, esimerkiksi nvdaremote.com.
5. Kirjoita Avain-muokkauskenttään haluamasi avain tai paina Luo avain -painiketta.
Avainta käytetään tietokoneesi hallitsemiseen.
Hallittavan koneen ja kaikkien siihen yhdistävien asiakaskoneiden on käytettävä samaa avainta.
6. Paina OK. Kun yhteys on muodostettu, kuulet äänimerkin ja "Yhdistetty"-ilmoituksen.

###Hallitseva tietokone
1. Avaa NVDA-valikko ja valitse Työkalut -> Etäkäyttö -> Yhdistä.
2. Valitse ensimmäisestä valintapainikeryhmästä Asiakas-vaihtoehto.
3. Valitse toisesta valintapainikeryhmästä Hallitse toista konetta -vaihtoehto.
4. Kirjoita Isäntä-muokkauskenttään sen palvelimen osoite, johon olet yhdistämässä, esimerkiksi nvdaremote.com.
5. Kirjoita Avain-kenttään haluamasi avain tai paina Luo avain -painiketta.
Hallittavan koneen ja kaikkien siihen yhdistävien asiakaskoneiden on käytettävä samaa avainta.
6. Paina OK. Kun yhteys on muodostettu, kuulet äänimerkin ja "Yhdistetty"-ilmoituksen.

##Suorat yhteydet
Yhdistä-valintaikkunan Palvelin-vaihtoehdolla voit muodostaa suoran yhteyden.
Kun se on valittuna, sinun on myös valittava, missä tilassa yhteytesi tulee olemaan.
Toinen henkilö yhdistää koneeseesi päinvastaista vaihtoehtoa käyttäen.

Kun tila on valittu, voit käyttää Hae ulkoinen IP -painiketta noutaaksesi ulkoisen IP-osoitteesi ja varmistaaksesi, että portti on uudelleenohjattu asianmukaisesti.
Jos portcheck-palvelu havaitsee, ettei porttiin 6837 saada yhteyttä, näkyviin tulee varoitus asiasta.
Sinun on tällöin uudelleenohjattava porttisi ja yritettävä sitten uudelleen.
Huom: Porttien uudelleenohjausta ei käsitellä tässä asiakirjassa. Katso lisätietoja reitittimesi mukana toimitetuista ohjeista.

Kirjoita haluamasi avain Avain-muokkauskenttään tai paina Luo avain -painiketta. Toinen henkilö tarvitsee yhdistämiseen ulkoisen IP-osoitteesi lisäksi tämän avaimen.

Yhteys muodostetaan painettuasi OK-painiketta.
Kun toinen henkilö yhdistää koneeseesi, voit käyttää NVDA-etäkäyttöä tavalliseen tapaan.

##Näppäinpainallusten lähettäminen
Kun yhteys on muodostettu, hallitsevassa koneessa voidaan painaa F11, joka aloittaa näppäinpainallusten lähettämisen.
Kun NVDA sanoo "näppäimet lähetetään", kaikki näppäinpainalluksesi suoritetaan etäkoneessa. Paina uudestaan F11 lopettaaksesi näppäinpainallusten lähettämisen ja vaihtaaksesi takaisin hallitsevalle koneelle.
Varmista parhaan yhteensopivuuden takaamiseksi, että molemmissa koneissa on käytössä sama näppäimistöasettelu.

##Lähetä Ctrl+Alt+Del
Ctrl+Alt+Del-näppäinyhdistelmän lähettäminen ei ole mahdollista näppäinpainalluksia lähetettäessä.
Käytä tätä komentoa, mikäli sinun on lähetettävä Ctrl+Alt+Del etäjärjestelmälle, jossa suojattu työpöytä on aktiivisena.

##Valvomattoman tietokoneen etähallinta
Saatat joskus haluta etähallita omaa konettasi. Tämä on erityisen hyödyllistä, mikäli olet matkoilla ja haluat hallita kotikonetta kannettavallasi, tai kotona sisällä talossa olevaa konetta ollessasi itse ulkona toisen koneen kanssa. Tämä on mahdollista pienellä valmistelulla.

1. Avaa NVDA-valikko ja valitse Työkalut ja sitten Etäkäyttö. Paina lopuksi Enter Asetukset-vaihtoehdon kohdalla.
2. Valitse valintaruutu "Yhdistä hallintapalvelimeen automaattisesti käynnistyksen yhteydessä".
3. Täytä Isäntä- ja Avain-muokkauskentät, siirry Sarkaimella OK-painikkeen kohdalle ja paina Enter.
4. Huomaa, että Luo avain -vaihtoehto ei ole käytettävissä. Parasta on keksiä avain, jonka muistat, jotta voit helposti käyttää sitä mistä tahansa etäsijainnista.

##Etätietokoneen puheen mykistäminen
Mikäli et halua kuulla etäkoneen puhetta, avaa NVDA-valikko ja valitse Työkalut -> Etäkäyttö. Siirry lopuksi alanuolella kohtaan Mykistä etäpuhe ja paina Enter.

##Etäistunnon lopettaminen
Lopeta etäistunto seuraavasti:

1. Paina hallitsevassa tietokoneessa F11 lopettaaksesi näppäinpainallusten lähettämisen. NVDA:n pitäisi nyt sanoa "Näppäimiä ei lähetetä". Jos sen sijaan kuulet ilmoituksen näppäinten lähettämisestä, paina vielä kerran F11.
2. Avaa NVDA-valikko, valitse Työkalut -> Etäkäyttö ja paina Enter Katkaise yhteys -kohdassa.

##Leikepöydän lähettäminen
Etäkäyttö-valikon Lähetä leikepöytä -vaihtoehdolla voit lähettää leikepöydällä olevan tekstin.
Kun toiminto on otettu käyttöön, kaikki leikepöydällä oleva teksti lähetetään toisille koneille.

##NVDA-etäkäytön määrittäminen toimimaan suojatulla työpöydällä
Jotta NVDA-etäkäyttö-lisäosa toimisi suojatulla työpöydällä, se on asennettava suojatulla työpöydällä käynnissä olevaan NVDA:han.

1. Valitse NVDA-valikosta Asetukset -> Yleiset.
2. Siirry Sarkaimella Käytä tallennettuja asetuksia kirjautumis- ja muissa suojatuissa ruuduissa (edellyttää järjestelmänvalvojan oikeuksia) -painikkeen kohdalle ja paina Enter.
3. Vastaa Kyllä kehotteisiin asetustesi ja lisäosien kopioinnista sekä mahdollisesti näkyviin tulevaan Käyttäjätilien valvonnan kehotteeseen.
4. Kun asetukset on kopioitu, paina Enter sulkeaksesi siitä kertovan ilmoituksen. Siirry sitten sarkaimella OK-painikkeen kohdalle ja paina vielä kerran Enter sulkeaksesi valintaikkunan.

Kun NVDA-etäkäyttö on asennettu suojatulle työpöydälle ja konettasi hallitaan etäistunnossa, suojattu työpöytä luetaan siihen siirryttäessä.

##Avustajat
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
