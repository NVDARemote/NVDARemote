#Zdalne NVDA / NVDA Remote Access
Wersja 1.0

Dodatek Zdalne NVDA (oryginalnie NVDA Remote Access) pozwala połączyć się z innym komputerem, na którym uruchomiony jest czytnik ekranu NVDA. Nie ma znaczenia, czy znajdujesz się po drugiej stronie pokoju, czy po drugiej stronie świata. Połączenie jest proste i jest tylko kilka poleceń do zapamiętania. Możesz podłączyć się do komputera innej osoby, lub pozwolić komuś zaufanemu podłączyć się do twojego systemu dla wykonania rutynowej konserwacji, diagnostyki problemu, albo przeprowadzenia szkolenia.

##Zanim zaczniesz

Musisz zainstalować NVDA na obu komputerach, oraz pobrać dodatek Zdalne NVDA.
Instalacja NVDA i tego dodatku są standardowe. Jeśli potrzebujesz więcej informacji, możesz je znaleźć w podręczniku NVDA.

##Rozpoczynanie zdalnej sesji przez serwer pośredniczący
###Kontrolowany	 komputer
1. Otwórz menu NVDA, Narzędzia, Zdalne, Połącz.
2. Wybierz klient w pierwszej grupie  przycisków opcji.
3. Wybierz Zezwól na kontrolę tego komputera w drugiej grupie przycisków opcji.
4. W polu Host, wprowadź adres serwera, do którego się łączysz, np. nvdaremote.com.
5. Wprowadź klucz w polu klucza, albo użyj przycisku Generuj klucz.
Klucz jest niezbędny osobie, która będzie kontrolować twój komputer.
Kontrolowana maszyna i inne do niej podłączone, muszą używać tego samego klucza.
6. Naciśnij OK. Usłyszysz dźwięk i połączone.

###Komputer kontrolujący
1. Otwórz menu NVDA, Narzędzia, Zdalne, Połącz.
2. Wybierz klient w pierwszej grupie  przycisków opcji.
3. Wybierz Kontroluj inny komputer w drugiej grupie przycisków opcji.
4. W polu Host, wprowadź adres serwera, do którego się łączysz, np. nvdaremote.com.
5. Wprowadź klucz w polu klucza, albo użyj przycisku Generuj klucz.
Klucz jest niezbędny osobie, która będzie kontrolować twój komputer.
Kontrolowana maszyna i inne do niej podłączone, muszą używać tego samego klucza.
6. Naciśnij OK. Usłyszysz dźwięk i połączone.


##Bezpośrednie połączenia
Opcja Serwer w oknie połączenia pozwala ustanowić bezpośrednie połączenie.
Po wybraniu tego, określ, jaką rolę będzie pełnił twój komputer.
Inna osoba połączy się z tobą używając roli przeciwnej.

Po wybraniu roli, możesz uzyskać adres IP przyciskiem Pobierz zewnętrzne IP, oraz upewnić się, że port jest prawidłowo przekazywany.
Jeśli sprawdzenie wykryje, że twój port (6837) jest nieosiągalny, pojawi się okienko powiadomienia.
Włącz przekazywanie portów i spróbuj ponownie.
Uwaga: proces ustawiania przekazywania portów wykracza poza zakres tego dokumentu. Sprawdź instrukcję obsługi swojego routera.

Wprowadź klucz w polu klucza, lub wybierz przycisk Generuj. Inna osoba będzie potrzebować twojego zewnętrznego IP oraz klucza, aby się połączyć.

Po naciśnięciu przycisku OK, zostaniesz połączony.
Gdy podłączy się druga osoba, można będzie normalnie używać zdalnego NVDA.

##Wysyłanie klawiszy
Po ustanowieniu połączenia, na maszynie kontrolującej można nacisnąć f11 aby rozpocząć przesyłanie klawiszy.
Gdy NVDA wypowie Klawisze wysyłane, naciskane klawisze będą trafiać do kontrolowanego komputera. Naciśnij f11 aby zakończyć wysyłanie klawiszy i powrócić do kontrolującej maszyny.
Dla najlepszej kompatybilności proszę się upewnić, że układ klawiatury jest taki sam na obu maszynach.

##Wyślij Ctrl+Alt+Del
Podczas wysyłania klawiszy, nie jest możliwe wysłanie kombinacji CTRL+Alt+del w zwykły sposób.
Jeśli musisz wysłać CTRL+Alt+del, a zdalny komputer jest w trybie bezpiecznego pulpitu, użyj tego polecenia.

##Zdalna kontrola nienadzorowanego komputera

Czasem możesz chcieć kontrolować zdalnie jakiś własny komputer. Jest to szczególnie przydatne jeśli podróżujesz i chcesz kontrolować swój domowy PC z laptopa. Podobnie, dla kontroli komputera znajdującego się w innym pokoju. Drobne przygotowania czynią to wygodne i możliwe.

1. Wejdź do menu NVDA, Narzędzia, Zdalne, Opcje.
2. Zaznacz pole wyboru , "Łącz automatycznie z serwerem kontroli przy starcie".
3. Wypełnij pola Host i klucz i naciśnij OK.
4. Opcja generowania klucza nie jest dostępna w tej sytuacji. Najlepiej jest użyć klucza, który łatwo zapamiętasz i będziesz mógł go użyć ze zdalnej lokalizacji .

##Wyciszanie mowy na zdalnym komputerze
Jeśli nie chcesz słyszeć mowy zdalnego komputera, uruchom menu NVDA, Narzędzia, Zdalne. Przejdź do polecenia "Wycisz zdalną mowę" i naciśnij Enter.


##Kończenie sesji zdalnej

Aby zakończyć zdalną sesję, wykonaj następujące działania:

1. Na kontrolującym komputerze, naciśnij F11 aby zakończyć wysyłanie klawiszy. Powinieneś usłyszeć komunikat: "Klawisze nie wysyłane." Jeśli zamiast tego usłyszysz, że klawisze wysyłane,  naciśnij F11 jeszcze raz.

2. Otwórz menu NVDA, Narzędzia, Zdalne, i naciśnij Enter na poleceniu Rozłącz.

##Wyślij schowek
Opcja Wyślij schowek w menu Zdalne, pozwala przesłać tekst z twojego schowka.
Po jej aktywowaniu tekst w schowku zostanie przesłany do schowka innych maszyn.

##Konfigurowanie zdalnego NVDA do pracy na bezpiecznym pulpicie

Aby Zdalne NVDA mogło pracować na bezpiecznym pulpicie, dodatek musi być zainstalowany w NVDA działającym na bezpiecznym pulpicie.

1. Z menu NVDA wybierz Ustawienia, Ogólne.

2. Przejdź klawiszem Tab do przycisku Używaj zapisanych ustawień NVDA na ekranie logowania i innych zabezpieczonych ekranach (wymaga uprawnień administratora) i naciśnij Enter.

3. Odpowiedz twierdząco na pytania dotyczące kopiowania twoich ustawień i kopiowania dodatków, ewentualnie potwierdź komunikat kontroli konta użytkownika, który się może pojawić.
4. Po skopiowaniu ustawień zamknij powiadomienie przyciskiem OK. Przejdź klawiszem Tab do OK i naciśnij Enter, aby opuścić okno ustawień.

Gdy Zdalne NVDA jest zainstalowane na bezpiecznym pulpicie, jeśli aktualnie jesteś kontrolowany w zdalnej sesji,
bezpieczny pulpit będzie odczytywany, jeśli się pojawi.

##Współpraca
Chcielibyśmy podziękować m.in. następującym osobom, które pomogły urzeczywistnić projekt Zdalnego NVDA.

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
