#Zdalne NVDA / NVDA Remote Access
Wersja 1.0

Dodatek Zdalne NVDA (oryginalnie NVDA Remote Access) pozwala po³¹czyæ siê z innym komputerem, na którym uruchomiony jest czytnik ekranu NVDA. Nie ma znaczenia, czy znajdujesz siê po drugiej stronie pokoju, czy po drugiej stronie œwiata. Po³¹czenie jest proste i jest tylko kilka poleceñ do zapamiêtania. Mo¿esz pod³¹czyæ siê do komputera innej osoby, lub pozwoliæ komuœ zaufanemu pod³¹czyæ siê do twojego systemu dla wykonania rutynowej konserwacji, diagnostyki problemu, albo przeprowadzenia szkolenia.

##Zanim zaczniesz

Musisz zainstalowaæ NVDA na obu komputerach, oraz pobraæ dodatek Zdalne NVDA.
Instalacja NVDA i tego dodatku s¹ standardowe. Jeœli potrzebujesz wiêcej informacji, mo¿esz je znaleŸæ w podrêczniku NVDA.

##Rozpoczynanie zdalnej sesji przez serwer poœrednicz¹cy
###Kontrolowany	 komputer
1. Otwórz menu NVDA, Narzêdzia, Zdalne, Po³¹cz.
2. Wybierz klient w pierwszej grupie  przycisków opcji.
3. Wybierz Zezwól na kontrolê tego komputera w drugiej grupie przycisków opcji.
4. W polu Host, wprowadŸ adres serwera, do którego siê ³¹czysz, np. nvdaremote.com.
5. WprowadŸ klucz w polu klucza, albo u¿yj przycisku Generuj klucz.
Klucz jest niezbêdny osobie, która bêdzie kontrolowaæ twój komputer.
Kontrolowana maszyna i inne do niej pod³¹czone, musz¹ u¿ywaæ tego samego klucza.
6. Naciœnij OK. Us³yszysz dŸwiêk i po³¹czone.

###Komputer kontroluj¹cy
1. Otwórz menu NVDA, Narzêdzia, Zdalne, Po³¹cz.
2. Wybierz klient w pierwszej grupie  przycisków opcji.
3. Wybierz Kontroluj inny komputer w drugiej grupie przycisków opcji.
4. W polu Host, wprowadŸ adres serwera, do którego siê ³¹czysz, np. nvdaremote.com.
5. WprowadŸ klucz w polu klucza, albo u¿yj przycisku Generuj klucz.
Klucz jest niezbêdny osobie, która bêdzie kontrolowaæ twój komputer.
Kontrolowana maszyna i inne do niej pod³¹czone, musz¹ u¿ywaæ tego samego klucza.
6. Naciœnij OK. Us³yszysz dŸwiêk i po³¹czone.


##Bezpoœrednie po³¹czenia
Opcja Serwer w oknie po³¹czenia pozwala ustanowiæ bezpoœrednie po³¹czenie.
Po wybraniu tego, okreœl, jak¹ rolê bêdzie pe³ni³ twój komputer.
Inna osoba po³¹czy siê z tob¹ u¿ywaj¹c roli przeciwnej.

Po wybraniu roli, mo¿esz uzyskaæ adres IP przyciskiem Pobierz zewnêtrzne IP, oraz upewniæ siê, ¿e port jest prawid³owo przekazywany.
Jeœli sprawdzenie wykryje, ¿e twój port (6837) jest nieosi¹galny, pojawi siê okienko powiadomienia.
W³¹cz przekazywanie portów i spróbuj ponownie.
Uwaga: proces ustawiania przekazywania portów wykracza poza zakres tego dokumentu. SprawdŸ instrukcjê obs³ugi swojego routera.

WprowadŸ klucz w polu klucza, lub wybierz przycisk Generuj. Inna osoba bêdzie potrzebowaæ twojego zewnêtrznego IP oraz klucza, aby siê po³¹czyæ.

Po naciœniêciu przycisku OK, zostaniesz po³¹czony.
Gdy pod³¹czy siê druga osoba, mo¿na bêdzie normalnie u¿ywaæ zdalnego NVDA.

##Wysy³anie klawiszy
Po ustanowieniu po³¹czenia, na maszynie kontroluj¹cej mo¿na nacisn¹æ f11 aby rozpocz¹æ przesy³anie klawiszy.
Gdy NVDA wypowie Klawisze wysy³ane, naciskane klawisze bêd¹ trafiaæ do kontrolowanego komputera. Naciœnij f11 aby zakoñczyæ wysy³anie klawiszy i powróciæ do kontroluj¹cej maszyny.
Dla najlepszej kompatybilnoœci proszê siê upewniæ, ¿e uk³ad klawiatury jest taki sam na obu maszynach.

##Wyœlij Ctrl+Alt+Del
Podczas wysy³ania klawiszy, nie jest mo¿liwe wys³anie kombinacji CTRL+Alt+del w zwyk³y sposób.
Jeœli musisz wys³aæ CTRL+Alt+del, a zdalny komputer jest w trybie bezpiecznego pulpitu, u¿yj tego polecenia.

##Zdalna kontrola nienadzorowanego komputera

Czasem mo¿esz chcieæ kontrolowaæ zdalnie jakiœ w³asny komputer. Jest to szczególnie przydatne jeœli podró¿ujesz i chcesz kontrolowaæ swój domowy PC z laptopa. Podobnie, dla kontroli komputera znajduj¹cego siê w innym pokoju. Drobne przygotowania czyni¹ to wygodne i mo¿liwe.

1. WejdŸ do menu NVDA, Narzêdzia, Zdalne, Opcje.
2. Zaznacz pole wyboru , "£¹cz automatycznie z serwerem kontroli przy starcie".
3. Wype³nij pola Host i klucz i naciœnij OK.
4. Opcja generowania klucza nie jest dostêpna w tej sytuacji. Najlepiej jest u¿yæ klucza, który ³atwo zapamiêtasz i bêdziesz móg³ go u¿yæ ze zdalnej lokalizacji .

##Wyciszanie mowy na zdalnym komputerze
Jeœli nie chcesz s³yszeæ mowy zdalnego komputera, uruchom menu NVDA, Narzêdzia, Zdalne. PrzejdŸ do polecenia "Wycisz zdaln¹ mowê" i naciœnij Enter.


##Koñczenie sesji zdalnej

Aby zakoñczyæ zdaln¹ sesjê, wykonaj nastêpuj¹ce dzia³ania:

1. Na kontroluj¹cym komputerze, naciœnij F11 aby zakoñczyæ wysy³anie klawiszy. Powinieneœ us³yszeæ komunikat: "Klawisze nie wysy³ane." Jeœli zamiast tego us³yszysz, ¿e klawisze wysy³ane,  naciœnij F11 jeszcze raz.

2. Otwórz menu NVDA, Narzêdzia, Zdalne, i naciœnij Enter na poleceniu Roz³¹cz.

##Wyœlij schowek
Opcja Wyœlij schowek w menu Zdalne, pozwala przes³aæ tekst z twojego schowka.
Po jej aktywowaniu tekst w schowku zostanie przes³any do schowka innych maszyn.

##Konfigurowanie zdalnego NVDA do pracy na bezpiecznym pulpicie

Aby Zdalne NVDA mog³o pracowaæ na bezpiecznym pulpicie, dodatek musi byæ zainstalowany w NVDA dzia³aj¹cym na bezpiecznym pulpicie.

1. Z menu NVDA wybierz Ustawienia, Ogólne.

2. PrzejdŸ klawiszem Tab do przycisku U¿ywaj zapisanych ustawieñ NVDA na ekranie logowania i innych zabezpieczonych ekranach (wymaga uprawnieñ administratora) i naciœnij Enter.

3. Odpowiedz twierdz¹co na pytania dotycz¹ce kopiowania twoich ustawieñ i kopiowania dodatków, ewentualnie potwierdŸ komunikat kontroli konta u¿ytkownika, który siê mo¿e pojawiæ.
4. Po skopiowaniu ustawieñ zamknij powiadomienie przyciskiem OK. PrzejdŸ klawiszem Tab do OK i naciœnij Enter, aby opuœciæ okno ustawieñ.

Gdy Zdalne NVDA jest zainstalowane na bezpiecznym pulpicie, jeœli aktualnie jesteœ kontrolowany w zdalnej sesji,
bezpieczny pulpit bêdzie odczytywany, jeœli siê pojawi.

##Wspó³praca
Chcielibyœmy podziêkowaæ m.in. nastêpuj¹cym osobom, które pomog³y urzeczywistniæ projekt Zdalnego NVDA.

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
