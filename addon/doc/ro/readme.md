# NVDA Remote Access
Versiunea 2.6

Bun venit la suplimentul NVDA Remote Access, Care vă va permite să vă conectați la un alt computer folosind NVDA, cititorul de ecran gratuit. Nu contează că sunteți în camera alăturată sau la capătul lumii. Conectarea e simplă. Sunt doar câteva comenzi pe care trebuie să le țineți minte. Vă puteți conecta la calculatorul unei persoane, sau îi puteți permite uneia de încredere să se conecteze la calculatorul dumneavoastră pentru a efectua mentenanța de rutină, pentru a diagnostica o problemă, sau pentru a oferi antrenament (training).

## Înainte de a începe

Trebuie neapărat să aveți NVDA instalat pe ambele calculatoare și să obțineți suplimentul NVDA Remote Access.
Atât instalarea NVDA, cât și cea a acestui supliment sunt standard. Dacă aveți nevoie de mai multe informații, acestea pot fi găsite în ghidul de utilizare al NVDA.

## Actualizarea

La actualizarea suplimentului, dacă ați instalat NVDA Remote pe spațiul de lucru sigur, vă este recomandată actualizarea copiei de pe acesta.
Pentru a face asta, actualizați mai întâi suplimentul existent, apoi deschideți meniul NVDA, preferințe, setări generale și apăsați butonul etichetat „Folosește preferințele curent salvate asupra ecranului de autentificare și a altor ecrane securizate (cere privilegii de administrator)”.

## Pornirea unei sesiuni la distanță printr-un server de transmisie
### Pe calculatorul pe care doriți să îl  controlați
1. Deschideți meniul NVDA, Instrumente, Remote, Conectare.
2. Selectați „Client” în primul buton rotativ.
3. Selectați „Permiteți ca acest computer să fie controlat” din al doilea set de butoane rotative.
4. În câmpul gazdă, introduceți adresa server-ului la care urmează să vă conectați, de exemplu nvdaremote.com. Atunci când server-ul particular utilizează un port alternativ, puteți introduce adresa gazdă în forma &lt;host&gt;:&lt;port&gt;, de exemplu nvdaremote.com:1234.
5. Introduceți o cheie în câmpul cu același nume sau apăsați butonul generare cheie.
Cheia este cea pe care o vor folosi alții pentru a vă controla calculatorul.
Calculatorul care este controlat și toți clienții săi trebuie să utilizeze aceeași cheie.
6. Apăsați ok. Odată terminată operațiunea veți auzi un semnal sonor, iar în același timp pe NVDA spunând „conectat”.

### Pe calculatorul care controlează
1. Deschideți meniul NVDA, Instrumente, Remote, Conectare.
2. Selectați „Client” în primul buton rotativ.
3. Selectați „Controlați un alt computer” din al doilea set de butoane rotative.
4. În câmpul gazdă, introduceți adresa server-ului la care urmează să vă conectați, de exemplu nvdaremote.com. Atunci când server-ul particular utilizează un port alternativ, puteți introduce adresa gazdă în forma &lt;host&gt;:&lt;port&gt;, de exemplu nvdaremote.com:1234.
5. Introduceți o cheie în câmpul cu același nume sau apăsați butonul generare cheie.
Calculatorul care este controlat și toți clienții săi trebuie să utilizeze aceeași cheie.
6. Apăsați ok. Odată terminată operațiunea veți auzi un semnal sonor, iar în același timp pe NVDA spunând „conectat”.

### Avertizarea de securitate a conexiunii
Dacă vă conectați la un server care nu are un certificat SSL valid, veți primi o avertizare de securitate a conexiunii.
Acest lucru poate însemna că nu este sigură conexiunea. Dacă aveți încredere în server-ul respectiv, puteți apăsa butonul „Conectare” pentru a vă conecta o dată, sau pe butonul „Conectează-te și nu mai întreba din nou pentru acest server” pentru a vă conecta și a marca faptul că aveți încredere în acel server.

## Conexiuni directe
Opțiunea server din dialogul de conectare vă permite să setați o conexiune directă.
Odată selectată, selectați ce mod de conexiune va fi setat.
Cealaltă persoană se va conecta la dumneavoastră folosind modul opus.

Odată ce modul este selectat, puteți folosi butonul Obținere adresă IP externă pentru a vă opține IP-ul extern și pentru a vă asigura că portul care este introdus în câmpul cu același nume este deschis corect.
Dacă portcheck detectează că portul dumneavoastră (6837 în mod implicit ) nu este deschis, va apărea un mesaj de avertisment.
Deschideți-vă portul și încercați din nou.
Notă: procesul pentru deschiderea porturilor nu face obiectul acestei documentații. Vă rugăm să consultați informațiile furnizate la pachet cu router-ul pentru instrucțiuni suplimentare.

Introduceți o cheie în câmpul cu același nume, sau apăsați butonul generare. Cealaltă persoană va avea nevoie de IP-ul dumneavoastră extern împreună cu cheia pentru a se conecta. Dacă ați introdus alt port decât cel implicit (6837) în câmpul port, asigurați-vă că persoana care se conectează la dumneavoastră introduce exact același port împreună cu adresa gazdă în forma &lt;external ip&gt;:&lt;port&gt;.

Odată ce butonul ok este apăsat, veți fi conectat.
Când o altă persoană se conectează, puteți folosi NVDA Remote în mod obișnuit.

## Controlare computer aflat la distanță

Odată ce sesiunea este conectată, utilizatorul al cărui computer controlează poate apăsa f11 pentru a începe să controleze calculatorul aflat la distanță.
Când NVDA spune că se controlează calculatorul aflat la distanță, tastatura și tastele afișajului braille pe care le apăsați îl vor controla. În plus, dacă calculatorul care controlează folosește un afișaj braille, informațiile care vin de la cel controlat vor fi afișate pe el. Apăsați f11 pentru a putea controla din nou calculatorul local.
Pentru cea mai bună compatibilitate, vă rugăm să vă asigurați că aspectele tastaturii pe ambele calculatoare se potrivesc.

## Partajarea sesiunii

Pentru a distribui un link prin care altcineva să se poată alătura sesiunii dumneavoastră, selectați Copiere link din meniul Remote.
Dacă calculatorul dumneavoastră controlează în momentul în care o terță persoană se alătură, link-ul îi va permite acesteia să se conecteze, iar calculatorului pe care îl deține să fie controlat.
În schimb, dacă calculatorul dumneavoastră este controlat, link-ul le va permite celor cu care l-ați partajat să vi-l controleze.
Multe aplicații le vor permite utilizatorilor să activeze acest link automat, dar dacă acesta nu se va deschide într-o aplicație specifică, va fi lipit pe planșetă și deschis din dialogul Executare.


## Trimitere Ctrl+Alt+Del
În timp ce se trimit taste, nu puteți acționa comanda CTRL+Alt+del în mod obișnuit.
Dacă vreți să acționați această comandă, iar sistemul aflat la distanță este pe spațiul de lucru sigur, folosiți-o.

## Controlarea de la distanță a unui computer propriu

Uneori, sunt momente în care doriți să vă controlați calculatoarele proprii de la distanță. Asta vă e de folos în special atunci când călătoriți și vreți să vă controlați PC-ul de acasă folosindu-vă de laptop. Sau, poate vreți să controlați un computer dintr-o cameră a casei cât timp stați afară cu un alt PC. O pregătire avansată a făcut acest lucru posibil.

1. Intrați în meniul NVDA și alegeți instrumente, apoi Remote. După aceea, apăsați Enter pe Opțiuni.
2. Bifați caseta care spune: „autoconectare la server-ul de control la pornire”.
3. Selectați dacă vreți să utilizați un server de transmisie sau dacă vreți să găzduiți local conexiunea.
4. Setați că permiteți ca acest computer să fie controlat din al doilea set de butoane rotative.
5. Dacă găzduiți conexiunea, va trebui să vă asigurați că portul introdus în câmpul său specific (6837 în mod implicit) pe calculatorul controlat, poate fi accesat de pe calculatoarele care controlează.
6. Dacă vreți să utilizați un server de transmisie, completați atât câmpul Gazdă, cât și câmpul Cheie, navigați cu Tab până la OK, apoi apăsați Enter. Opțiunea de generare a cheii nu este disponibilă în această situație. E mai bine să puneți o cheie pe care să o țineți minte, astfel încât să o putteți folosi de la orice computer aflat la distanță.

Pentru o utilizare avansată, puteți, de asemenea, să configurați NVDA Remote să se conecteze automat la un server local sau la unul de transmisie în modul de controlare. Dacă vreți asta, controlați un alt computer bifând această opțiune în al doilea set de butoane rotative.

Notă: Opțiunile relatate ale autoconectării la pornire din dialogul de opțiuni nu se aplică până când NVDA este repornit.


## Punerea vorbirii pe mut pe calculatorul aflat la distanță
Dacă nu doriți să auziți vorbirea care provine de la calculatorul aflat la distanță sau sunetele specifice ale NVDA care provin de la acesta, pur și simplu accesați meniul NVDA, Instrumente, Remote. Mergeți cu săgeată jos la Mute Remote și apăsați Enter. Vă rugăm să rețineți faptul că această opțiune nu va dezactiva transmisia conținutului în braille de la calculatorul  aflat la distanță atunci când cel care controlează trimite taste.

## Terminarea unei sesiuni la distanță

Pentru a termina o sesiune la distanță, faceți în felul următor:

1. Pe calculatorul care controlează, apăsați F11 pentru a opri controlarea computerului aflat la distanță.
2. Accesați meniul NVDA, apoi Instrumente, Remote, apoi apăsați Enter pe Deconectare.

## Trimitere conținut la planșetă
Aceast[ opțiune din meniul Remote vă permite să trimiteți textul de pe planșeta dumneavoastră la cea a computerului pe care îl controlați.
Când e activată, orice text de pe planșetă va fi trimis la cealaltă.

## Configurarea NVDA Remote să lucreze pe un spațiu de lucru sigur

Pentru ca NVDA să lucreze pe spațiul de lucru sigur, suplimentul trebuie să fie instalat în NVDA, care rulează pe acest spațiu de lucru.

1. Din meniul NVDA, selectați Preferințe, apoi Setări Generale.
2. Apăsați Tab până la butonul „Utilizați preferințele curent salvate asupra ecranului de autentificare și a altor ecrane securizate (cere privilegii de administrator)”, apoi apăsați Enter.
3. Confirmați această acțiune prin apăsarea butonului „Da”, apoi mai apăsați-l o dată pentru a scăpa de dialogul de UAC (User Account Control) (Control Cont Utilizator) care ar putea apărea.
4. Când setările sunt copiate, apăsați butonul OK, apoi apăsați-l din nou pentru a închide dialogul setărilor generale.

Odată ce NVDA Remote este instalat pe spațiul de lucru sigur, dacă sunteți controlat într-o sesiune la distanță, veți avea accesul vorbirii și al braille la spațiul de lucru sigur.

## Ștergerea amprentelor pentru certificatele SSL
Dacă nu mai aveți încredere într-un anumit server, îi puteți șterge amprentele pentru certificatul SSL apăsând butonul „Șterge toate amprentele de încredere” din dialogul Opțiuni.

## Contribuții
Dorim să menționăm următorii contributori care, împreună cu alții, au făcut ca proiectul NVDA Remote să fie o realitate.

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

## Jurnal de modificări

### Versiunea 2.6

* Suport pentru NVDA 2023.1
* A fost adăugat un gest care deschide dialogul de conectare
* Actualizări la traducerile pentru limbile italiană și ucraineană
* Indicații noi pentru planșetă

### Versiunea 2.5

* A fost rezolvată stabilitatea SSL
* A fost rezolvat suportul pentru spațiul de lucru sigur
* A fost rezolvată focalizarea inițială din dialogul de conectare
* Suport pentru pauza vorbirii de la distanță
* A fost înlocuită caseta de editare gazdă cu un edit combo pentru istoric
* Fișierele de configurare corupte sunt șterse automat

### Versiunea 2.4

* Au fost adăugate sunete
* Actualizat pentru NVDA 2021.1
* Se face verificarea certificatelor SSL ale serverelor gazdă la care ne conectăm

### Versiunea 2.3

* Am migrat la Python 3
* Am abandonat suportul pentru Python 2
* Am actualizat suplimentul astfel încât să se potrivească cu API-ul modificat în NVDA 2019.3, incluzând:

* Rescrierea vorbirii
* Modificări la afișajele Braille

### Versiunea 2.2

* Suport IPv6
* Suport pentru NVDA 2018.3, dar și pentru versiunile mai vechi
* Suport pentru gesturile modelelor specifice ale afișajelor braille


### Versiunea 2.1

* S-a rezolvat problema nesalvării conexiunii atunci când se permite ca un computer să fie controlat
* S-a adăugat un script pentru trimiterea conținutului la planșetă cu ctrl+shift+NVDA+c
* Acum, intrarea braille funcționează în modul de navigare
* Suport pentru gesturile modelelor specifice ale afișajelor braille
* Bipurile generate de NVDA Remote nu mai blochează NVDA

### Versiunea 2.0

* Suport pentru braille la distanță
* Suport pentru link-urile nvdaremote://
* Centrarea dialogurilor
* S-a reparat portcheck pentru a puncta la un domeniu pe care îl controlăm, portcheck.nvdaremote.com
* Suport pentru conectarea automată la un server de control în modul master
* S-au reparat erori în documentație
* Actualizare la protocol versiunea 2, ce include un câmp de origine în fiecare mesaj la distanță
* Curățare semnificativă de cod, care permite modificări mai facile în viitor
