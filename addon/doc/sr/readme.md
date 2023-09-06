# NVDA daljinski pristup
Verzija 2.6

Dobrodošli u dodatak NVDA daljinski pristup, koji će vam dozvoliti da se povežete na drugi računar na kojem je pokrenut besplatni NVDA čitač ekrana. Nije bitno da li ste u istoj sobi ili na različitim krajevima sveta. Povezivanje je jednostavno, i nema puno komandi koje treba zapamtiti. Možete se povezati na računar neke druge osobe, ili dozvoliti osobi kojoj verujete da se poveže na vaš računar kako bi izvršila rutinska održavanja, rešila problem, ili vam pružila podršku.

## Pre nego što počnete

Morate da imate instaliran NVDA na oba računara, i da preuzmete NVDA dodatak daljinskog pristupa.
Instalacije programa NVDA kao i dodatka su standardne. Ako vam trebaju dodatne informacije, mogu se pronaći u NVDA korisničkom uputstvu.

## Ažuriranje

Nakon što ažurirate dodatak, ako ste instalirali dodatak na bezbednoj radnoj površini, preporučuje se da takođe ažurirate kopiju na bezbednoj radnoj površini.
Da biste ovo uradili, prvo ažurirajte vaš postojeći dodatak. Zatim otvorite NVDA meni, opcije, podešavanja, i u panelu opštih podešavanja pritisnite dugme koje se zove "Koristi trenutno sačuvana podešavanja u toku prijave i drugim bezbednosnim ekranima (zahteva administratorske privilegije )".

## Početak daljinske sesije kroz udaljeni server
### Na računaru koji će biti kontrolisan
1. Otvorite NVDA meni, alati, Remote, poveži se.
2. U prvom radio dugmetu izaberite klijent.
3. U drugom skupu radio dugmića izaberite dozvoli da ovaj računar bude kontrolisan.
4. U polju za unos servera, upišite adresu servera na koji se povezujete, na primer nvdaremote.com. Kada server koristi neki drugi port, možete upisati adresu u obliku &lt;adresa&gt;:&lt;port&gt;, na primer nvdaremote.com:1234.
5. Upišite šifru u polje šifre, ili pritisnite dugme napravi šifru.
Šifra je ono što će drugi koristiti da kontrolišu vaš računar.
Računar koji će biti kontrolisan i svi njegovi klijenti moraju da koriste istu šifru.
6. Pritisnite u redu. Nakon što to uradite, čućete zvučni signal i poruku koja kaže  povezan.

### Na računaru koji će kontrolisati drugi računar
1. Otvorite NVDA meni, alati, Remote, poveži se. Alternativno, možete da pritisnete NVDA+alt+page up da otvorite dijalog za povezivanje.
2. U prvom radio dugmetu izaberite klijent.
3. U drugom skupu radio dugmića izaberite kontroliši drugi računar.
4. U polju za unos servera, upišite adresu servera na koji se povezujete, na primer nvdaremote.com. Kada server koristi neki drugi port, možete upisati adresu u obliku &lt;adresa&gt;:&lt;port&gt;, na primer nvdaremote.com:1234.
5. Upišite šifru u polje šifre, ili pritisnite dugme napravi šifru.
Računar koji će biti kontrolisan i svi njegovi klijenti moraju da koriste istu šifru.
6. Pritisnite u redu. Nakon što to uradite, čućete zvučni signal i poruku koja kaže  povezan.

### Upozorenje o bezbednosti veze
Ako se povežete na server bez ispravnog SSL sertifikata, dobićete upozorenje o bezbednosti veze.
Ovo može da znači da vaša veza nije bezbedna. Ako verujete otisku ovog servera, možete da pritisnete dugme "Poveži se" da se povežete jednom, ili "Poveži se i ne pitaj ponovo za ovaj server" da se povežete i sačuvate otisak.

## Direktne veze
Opcija za server u dijalogu povezivanja vam dozvoljava da podesite direktnu vezu.
Nakon što ovo izaberete, izaberite režim u kojem će biti vaša strana veze.
Druga osoba će se sa vama povezati u suprotnom režimu.

Nakon što se izabere režim, možete da koristite dugme saznajte IP adresu da dobijete vašu eksternu IP adresu i
uverite se da je port koji ste upisali u polje porta ispravno preusmeren.
Ako provera porta otkrije da se vašem portu (podrazumevani je 6837 ) ne može pristupiti, pojaviće se upozorenje.
Preusmerite vaš port i pokušajte ponovo.
Napomena: proces preusmeravanja porta je van okvira za ovaj dokument. Molimo pogledajte informacije koje dolaze uz vaš ruter za dodatna uputstva.

Upišite šifru u polje šifre, ili pritisnite dugme za pravljenje. Drugoj osobi će biti neophodna vaša eksterna IP adresa uz šifru za povezivanje. Ako upišete port koji nije podrazumevani (6837) u polje porta, uverite se da druga osoba doda port u polje za unos adrese u obliku &lt;Eksterna IP adresa&gt;:&lt;port&gt;.

Nakon što se pritisne u redu, bićete povezani.
Kada se druga osoba poveže, možete normalno koristiti NVDA remote.

## Kontrolisanje drugog računara

Nakon što se veza uspostavi, korisnik lokalnog računara može da pritisne f11 kako bi započeo kontrolisanje drugog računara (na primer slanjem tastera na tastaturi ili brajevog unosa).
Kada NVDA remote kaže kontrolisanje drugog računara, tasteri na tastaturi i brajevom redu koje pritisnete biće poslati drugom računaru. Takođe, kada računar koji kontroliše koristi brajev red, informacije sa drugog računara biće prikazane na njemu. Pritisnite F11 ponovo da se vratite na lokalni računar i prestanete da šaljete tastere.
Za najbolju kompatibilnost, molimo uverite se da se rasporedi tastature na oba računara podudaraju.

## Deljenje vaše veze

Da biste podelili link kako bi bilo ko mogao da se pridruži vašoj NVDA remote vezi, iz NVDA remote menija izaberite kopiraj link.
Ako ste povezani kao računar koji kontroliše, ovaj link će dozvoliti drugoj osobi da se poveže i bude kontrolisana.
Ako ste umesto toga podesili vezu tako da vaš računar bude kontrolisan, link će dozvoliti ljudima sa kojima ga podelite da kontrolišu vaš računar.
Mnoge aplikacije će dozvoliti automatsku aktivaciju ovog linka, ali ako se ne pokrene iz određene aplikacije, može se kopirati u privremenu memoriju i otvoriti iz dijaloga za pokretanje.


## Pošalji Ctrl+Alt+taster za brisanje
Dok šaljete tastere, nije moguće na standardni način poslati prečicu ctrl+alt+taster za brisanje.
Ako morate da pošaljete ovu prečicu, i Remote dodatak je na bezbednoj radnoj površini, koristite ovu komandu.

## Daljinsko kontrolisanje računara bez nadzora

Ponekad, možda ćete želeti daljinski da kontrolišete sopstvene računare. Ovo je posebno korisno ako putujete, i želite da kontrolišete vaš kućni računar sa vašeg laptopa. Ili, možda ćete želeti da kontrolišete računar koji je u jednoj sobi vaše kuće dok sedite napolju sa drugim računarom. Malo prethodne pripreme će učiniti da ovo bude jednostavno i moguće.

1. Uđite u NVDA meni, i izaberite alati, a zatim remote. Na kraju, pritisnite enter na podešavanja.
2. Označite izborno polje koje kaže, "Automatsko povezivanje na server za kontrolisanje".
3. Izaberite da li želite da koristite udaljeni server ili da napravite lokalnu vezu. 
4. U drugom skupu radio dugmića izaberite dozvoli da ovaj računar bude kontrolisan.
5. Ako sami pravite vezu, morate da se uverite da se portu koji je upisan u polje porta (podrazumevano 6837) na kontrolnom računaru može pristupiti sa računara koji će ga kontrolisati.
6. Ako želite da koristite udaljeni server, popunite polja adrese i šifre, krećite se tabom do tastera u redu, i pritisnite enter. Pravljenje šifre nije dostupno u ovoj situaciji. Najbolje je da smislite šifru koju ćete lako zapamtiti kako biste mogli da je koristite iz bilo koje udaljene lokacije.

Za napredno korišćenje, možete takođe da podesite NVDA remote da se poveže na lokalni ili udaljeni server u režimu kontrolisanja. Ako ovo želite, u drugom skupu radio dugmića izaberite kontroliši drugi računar.

Napomena: Opcije automatskog povezivanja u dijalogu podešavanja se ne primenjuju dok se NVDA ne pokrene ponovo.


## Isključivanje govora daljinskog računara
Ako ne želite da čujete govor daljinskog računara ili NVDA zvukove, pristupite NVDA meniju, alatima, i meniju remote. Krećite se strelicom dole do opcije Isključi zvuk daljinskog računara, i pritisnite enter. Molimo imajte na umu da ova opcija neće onemogućiti daljinski brajev izlaz sa kontrolnog brajevog reda kada mašina koja kontroliše šalje tastere.


## Prekidanje daljinske veze

Da prekinete daljinsku vezu, uradite sledeće:

1. Na računaru koji kontroliše, pritisnite F11 da prestanete da kontrolišete daljinski računar. Trebalo bi da čujete ili pročitate sledeću poruku: "Kontrolisanje lokalnog računara." Ako umesto toga čujete ili pročitate poruku koja kaže da kontrolišete drugi računar, ponovo pritisnite F11.
2. Pristupite NVDA meniju, zatim alatima, Remote, i pritisnite enter na opciju prekini vezu. Alternativno, možete da pritisnete NVDA+alt+page down da odmah prekinete daljinsku vezu.

## Prebacivanje privremene memorije
Opcija prebaci privremenu memoriju u remote meniju vam dozvoljava da prebacite tekst iz vaše privremene memorije.
Kada se aktivira, bilo koji tekst iz privremene memorije biće prebačen drugim računarima.

## Podešavanje dodatka NVDA remote za rad na bezbednoj radnoj površini

Kako bi NVDA remote radio na bezbednoj radnoj površini, dodatak mora biti instaliran u kopiju programa NVDA koja je pokrenuta na bezbednoj radnoj površini.

1. Iz NVDA menija, izaberite opcije, a zatim podešavanja.
2. U panelu opštih podešavanja, krećite se tabom do dugmeta Koristi trenutno sačuvana podešavanja u toku prijave i drugim bezbednosnim ekranima (zahteva administratorske privilegije ), i pritisnite enter.
3. Odgovorite potvrdno na pitanje o kopiranju vaših podešavanja i dodataka, i odgovorite na upozorenje kontrole korisničkog naloga koje će se možda pojaviti.
4. Nakon što se podešavanja kopiraju, pritisnite enter na dugme u redu da zatvorite dijalog. Krećite se tasterom tab do dugmeta u redu i pritisnite enter da zatvorite dijalog sa podešavanjima.

Nakon što je NVDA instaliran na bezbednoj radnoj površini, ako je vaš računar trenutno kontrolisan u daljinskoj vezi,
imaćete govornu i brajevu podršku na bezbednoj radnoj površini kada se prebacite na nju.

## Brisanje otisaka SSL sertifikata
Ako više ne želite da verujete otiscima servera kojima ste prethodno verovali, možete da obrišete sve otiske kojima verujete tako što ćete pritisnuti dugme "Obriši sve dozvoljene sertifikate" u dialogu sa podešavanjima.

## Saradnici
Želimo da se zahvalimo sledećim saradnicima, između ostalih, koji su pomogli da NVDA remote projekat postane stvarnost.

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
* NV Access
* Reef Turner

## Promene

### Verzija 2.6

* NVDA 2023.1 podrška
* Dodata prečica za otvaranje dijaloga za povezivanje
* Ažurirani prevodi za Ukrajinski i Italijanski
* Novi zvukovi za privremenu memoriju

### Verzija 2.5

* Ispravljena stabilnost SSL veze
* Ispravljena podrška za bezbedne radne površine
* Ispravljen prvobitan fokus u dijalogu za povezivanje
* Podrška za pauziranje daljinskog govora
* Zamenjeno polje za unos adrese izbornim okvirom koji se može urediti, kako bi postojala istorija unetih podataka
* Automatsko uklanjanje oštećenih podešavanja

### Verzija 2.4

* Dodati zvukovi
* Ažuriranja za NVDA 2021.1
* Potvrda SSL sertifikata za servere na koje se dodatak povezuje

### Verzija 2.3

* Prebačen na Python 3
* Uklonjena Python 2 podrška
* Ažuriranja kako bi se podržao promenjen API za NVDA 2019.3, uključujući:

    * Redizajn  govora
    * Promene za brajeve redove

### Verzija 2.2

* IPv6 podrška
* Podrška za novi NVDA 2018.3 kao i starije verzije
* Podrška za komande brajevih redova koje zavise od modela

### Verzija 2.1

* Ispravljena greška sa čuvanjem veze kada se dozvoli kontrolisanje računara
* Dodata prečica za prebacivanje privremene memorije ctrl+šift+NVDA+c
* Brajev unos sada radi u režimu pretraživanja
* Podrška za prečice brajevog reda koje zavise od modela
* Pištanja koja generiše NVDA remote više ne blokiraju NVDA

### Verzija 2.0

* Podrška za daljinski brajev izlaz
* Podrška za nvdaremote:// linkove
* Centrirani dijalozi kako bi bili usklađeni sa ostatkom programa NVDA
* Ispravljena provera porta kako bi radila na domenu koji je pod našom kontrolom, portcheck.nvdaremote.com
* Podrška za automatsko povezivanje na server za kontrolisanje kao računar koji kontroliše
* Ispravljena greška obrade u dokumentaciji
* Ažuriran protokol na verziju 2, koja uključuje polje porekla u svakoj poruci
* Značajno čišćenje koda koje će dozvoliti bitne promene u budućnosti

## Menjanje NVDA remote dodatka

Možete klonirati ovaj projekat kako biste menjali NVDA remote.

### Dodaci trećih strana

Mogu se instalirati uz pip:

* Markdown
* scons
* python-gettext

### Kako biste spakovali dodatak za deljenje:

1. Otvorite komandnu liniju, dođite do glavnog foldera ovog projekta
2. Pokrenite **scons** komandu. Napravljen dodatak, ako nije bilo grešaka, biće u trenutnom folderu.

