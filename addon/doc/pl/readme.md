# Dostęp Zdalny NVDA
Wersja 2.1

Witamy w dodatku Dostęp Zdalny NVDA. Umożliwia on połączenie się z innym komputerem obsługiwanym przez darmowy czytnik ekranu NVDA. Nie ważne, czy ten komputer znajduje się na sąsiednim biurku, czy na innym kontynencie. Samo łączenie się jest niezwykle proste, a do obsługi dodatku wystarczy zapamiętać  kilka komend. Można kontrolować inny komputer lub udzielić zaufanej osobie dostępu do systemu operacyjnego własnego komputera,  w celu przeprowadzenia  rutynowej konserwacji, zdjagnozowania problemu, czy przeprowadzenia szkolenia.

## Zanim Zaczniesz Pracę z Dodatkiem

Upewnij się, czy na obydwu komputerach został zainstalowany czytnik ekranu NVDA orazdodatek Dostęp Zdalny NVDA.
Instalacja czytnika ekranu i dodatku przebiega standardowo. Więcej informacji na ten temat można znaleźć w  Podręczniku Użytkownika NVDA.

## Aktualizacja

Jeżeli posiadasz kopię dodatku Dostęp Zdalny NVDA zainstalowaną na bezpiecznym pulpicie, podczas aktualizacji dodatku w systemie zalecane jest uaktualnienie również tej kopii.
Aby to zrobić, najpierw uaktualnij  główną kopię dodatku zainstalowaną w systemie. Następnie otwórz menu NVDA, Ustawienia, Ustawienia ogólne i naciśnij przycisk o nazwie "Używaj zapisanych ustawień NVDA na ekranie logowania i innych zabezpieczonych ekranach (wymaga uprawnień administratora)".

## Rozpoczęcie sesji zdalnej przez serwer pośredniczący
### Na komputerze kontrolowanym
1. Otwórz menu NVDA, Narzędzia, Zdalne, Połącz.
2. W pierwszym przycisku opcji zaznacz "klient".
3. W drugim przycisku opcji zaznacz "Zezwól na kontrolę tego komputera".
4. W polu edycyjnym "host" wpisz adres serwera, z którym chcesz się połączyć, Na przykład nvdaremote.com. Jeżeli dany serwer używa innego portu, można wpisać jego adres jako &lt;host&gt;:&lt;port&gt;, na przykład nvdaremote.com:1234.
5. Wpisz klucz w kolejnym polu edycyjnym, Lub naciśnij przycisk "Generuj klucz".
Tego klucza będą używać uprawnione osoby, aby połączyć się z twoim komputerem.
Komputer kontrolowany i wszyscy jego klienci muszą używać tego samego klucza.
6. Naciśnij przycisk OK. Jeżeli łączenie przebiegnie pomyślnie, usłyszysz odpowiedni dźwięk oraz komunikat "Połączono z serwerem kontrolującym".

### Na komputerze kontrolującym
1. Otwórz menu NVDA, Narzędzia, Zdalne, Połącz.
2. W pierwszym przycisku opcji zaznacz "klient".
3. W drugim przycisku opcji zaznacz "kontroluj inny komputer".
4. W polu edycyjnym "host" wpisz adres serwera, z którym chcesz się połączyć, Na przykład nvdaremote.com. Jeżeli dany serwer używa innego portu, można wpisać jego adres jako &lt;host&gt;:&lt;port&gt;, na przykład nvdaremote.com:1234.
5. Wpisz klucz w kolejnym polu edycyjnym, Lub naciśnij przycisk "Generuj klucz".
Komputer kontrolujący i wszyscy jego klienci muszą używać tego samego klucza.
6. Naciśnij przycisk OK. Jeżeli łączenie przebiegnie pomyślnie, usłyszysz odpowiedni dźwięk oraz komunikat "Połączono z serwerem kontrolującym".

## Połączenia bezpośrednie
Opcja "Serwer" w oknie dialogowym "Połącz" pozwala ustawić połączenie bezpośrednie.
Po zaznaczeniu tej opcji wybierz swoją stronę połączenia.
Druga osoba połączy się z twoim komputerem za pomocą strony przeciwnej.

Po wybraniu strony połączenia możesz użyć przycisku "Pobierz zewnętrzne IP".
Upewnij się, czy  wpisany w polu edycyjnym port jest poprawny.
Jeśli portcheck wykryje, że wpisany port (domyślnie 6837) jest nieosiągalny, pojawi się ostrzeżenie.
Wpisz port jeszcze raz i spróbuj ponownie.
Uwaga! Proces przekierowywania portów Nie jest opisany w tym dokumencie. Potrzebne informacje i wskazówki znajdziesz w instrukcji dołączonej do swojego routera.

Wpisz klucz w polu edycyjnym lub naciśnij przycisk "generuj". Użytkownik, który łączy się z twoim komputerem będzie potrzebować twojego zewnętrznego IP oraz klucza. Jeżeli chcesz użyć innego portu niż domyślny (6837) upewnij się, że osoba, z którą się łączysz dodała ten port do adresu serwera jako &lt;zewnętrzne ip&gt;:&lt;port&gt;.

Po naciśnięciu OK nastąpi połączenie.
Kiedy druga osoba również się połączy, możesz normalnie używać Dostępu Zdalnego NVDA

## Kontrola maszyny zdalnej

Kiedy oba komputery są już połączone i rozpoczyna się sesja zdalna, użytkownik komputera kontrolującego może nacisnąć f11 aby kontrolować maszynę zdalną (np. przez przesyłanie komend klawiszowych lub brajlowskich).
Gdy NVDA powie "kontroluję maszynę zdalną", naciskane klawisze na klawiaturze lub linijce brajlowskiej zostaną przekazane do komputera kontrolowanego. Ponadto, gdy maszyna lokalna, czyli komputer kontrolujący używa linijki brajlowskiej, informacje z maszyny zdalnej są na niej wyświetlane. Aby przestać przesyłać komendy i powrócić do maszyny lokalnej, ponownie naciśnij f11.
Dla uzyskania najlepszej zgodności, upewnij się, że układy klawiatury w obu komputerach są takie same.

## Udostępnianie sesji

Aby udostępnić link umożliwiający kolejnym osobom dołączenie do sesji zdalnej, wybierz Kopiuj link z menu Zdalne.
Jeżeli twój komputer jest w tej sesji maszyną kontrolującą, udostępniony link pozwoli  innym  dołączyć się pod twoją kontrolę.
Jeżeli natomiast twój komputer jest maszyną zdalną, udostępniony link pozwoli tym, z którymi dzielisz sesję kontrolować ten komputer.
Wiele aplikacji pozwala użytkownikom na automatyczne aktywowanie tego linku. Gdy jednak nie aktywuje się on automatycznie z poziomu danej aplikacji, można skopiować go do schowka i aktywować w oknie dialogowym Uruchom.


## Przesyłanie Ctrl+Alt+Del
Podczas przesyłania komend z klawiatury, nie da się przesłać kombinacji CTRL+Alt+del w standardowy sposób.
W razie potrzeby przesłania CTRL+Alt+del, można użyć tej komendy gdy system kontroli zdalnej jest włączony na bezpiecznym pulpicie.

## Kontrola zdalna komputera nienadzorowanego

Możesz też kontrolować zdalnie inny własny komputer. Jest to szczególnie pomocne, kiedy podczas podróży chcesz skontrolować swój domowy PC z laptopa. Tak samo możesz kontrolować komputer znajdujący się w  domu kiedy siedzisz na dworze z innym PC. Dzięki niewielkim uprzednim przygotowaniom, staje się to możliwe i wygodne.

1. Wejdź do meni NVDA. W menu wybierz kolejno Narzędzia i Zdalne. Następnie naciśnij enter na pozycji Opcje.
2. Zaznacz pole wyboru o nazwie "Łącz automatycznie z serwerem kontroli przy starcie".
3. Wybierz, czy chcesz użyć serwera pośredniczącego, czy zwykłego serwera kontroli zdalnej. 
4. Wybierz "Zezwól na kontrolę tego komputera" w kolejnym przycisku opcji.
5. Jeżeli twój komputer jest maszyną kontrolującą, upewnij się, że wpisany w kolejnym polu edycyjnym port (domyślnie 6837) jest osiągalny dla maszyny kontrolowanej, jak i kontrolującej.
6. Jeżeli chcesz użyć serwera pośredniczącego, wypełnij pola Host i Klucz, przejdź tabulatorem do przycisku OK i naciśnij enter. Opcja Generuj Klucz nie jest w tym kontekście dostępna. Najlepiej wymyślić łatwy do zapamiętania klucz, aby móc używać go w przyszłości z dowolnego komputera.

Dla zaawansowanego użytku można również skonfigurować Dostęp Zdalny NVDA tak, aby automatycznie łączył się z lokalnym lub zdalnym serwerem pośredniczącym w trybie maszyny kontrolującej. aby to ustawić, wybierz Kontroluj inny komputer w drugim przycisku opcji.

Uwaga! Automatyczne łączenie z serwerem przy starcie NVDA w oknie dialogowym Opcje zadziała dopiero po restarcie czytnika ekranu.


## Wyciszanie mowy na komputerze kontrolowanym
Jeżeli nie chcesz słyszeć mowy, czy dźwięków NVDA, wejdź do menu NVDA, Narzędzia, Zdalne. Następnie przejdź strzałką w dół do Wycisz wsparcie zdalne i naciśnij enter. Uwaga! ta opcja nie wyłącza zdalnego wyświetlania brajla na linijce brajlowskiej komputera kontrolującegopodczas przesyłania komend.


## Zakończenie sesji zdalnej

Aby zakończyć sesję zdalną, wykonaj następujące kroki:

1. Na komputerze kontrolującym naciśnij F11 aby zatrzymać kontrolę maszyny zdalnej. Najprawdopodobniej pojawi się wiadomość: "Kontroluję maszynę lokalną." Jeżeli zamiast tego usłyszysz lub przeczytasz "Kontroluję maszynę zdalną", ponownie naciśnij F11.

2. przejdź do menu NVDA, Narzędzia, Zdalne, znajdź pozycję Rozłącz i naciśnij enter.

## Wyślij schowek
Opcja Wyślij schowek znajdująca się w menu Zdalne umożliwia przesyłanie tekstu ze schowka.
Kiedy jest aktywna, można przesyłać każdy znajdujący się w schowku tekst do innych maszyn.

## Konfiguracja Dostępu Zdalnego NVDA na bezpiecznym pulpicie

Do pracy z Dostępem Zdalnym NVDA na bezpiecznym pulpicie,należy najpierw zainstalować kopię tego  dodatku w NVDA uruchomionym na bezpiecznym pulpicie.

1. Z menu NVDA wybierz Ustawienia, Ustawienia ogólne.

2. Przejdź tabulatorem do przycisku "Używaj zapisanych ustawień NVDA na ekranie logowania i innych zabezpieczonych ekranach (wymaga uprawnień administratora)", i naciśnij enter.

3. Odpowiedz "Tak" w ostrzeżeniach dotyczących kopiowania twoich ustawień oraz kopiowania  wtyczek. Następnie odpowiedz na ostrzeżenie kontroli konta użytkownika, jeśli się pojawi.
4. Gdy ustawienia skopiują się do końca, zamknij to okno naciskając enter na przycisku OK. Następnie przejdź  tabulatorem do kolejnego przycisku OK, który zamyka okno dialogowe i ponownie naciśnij enter.

Po instalacji dodatku na bezpiecznym pulpicie, jeżeli twój komputer jest kontrolowany podczas danej sesji,
mowa i brajl będą dostępne gdy przełączysz się na bezpieczny pulpit.

## Współautorzy
Chcielibyśmy podziękować chociaż kilku spośród wielu współautorów, bez których projekt Dostęp Zdalny NVDA nie zostałby zrealizowany.

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

## Lista zmian

### Wersja 2.1

* Naprawiono automatyczne łączenie przy ustawianiu automatycznej kontroli komputera
* Dodano skrypt do wysyłania schowka skrótem ctrl+shift+NVDA+c
* Wprowadzanie brajla działa w trybie przeglądania.
* Dźwięki generowane przez dodatek Dostęp Zdalny nie blokują już NVDA.

### Wersja 2.0

* Wsparcie dla zdalnego brajla
* Wsparcie dla linków nvdaremote://
* Wyśrodkowane okna dialogowe zgadzają się z resztą okien dialogowych w NVDA
* Naprawiono portcheck do wskazywania domeny, którą kontrolujemy portcheck.nvdaremote.com
* Wsparcie automatycznego łączenia z serwerem kontroli w trybie master
* Usprawniono poprawki błędów w dokumentacji
* Aktualizacja do  protokołu wersja 2, który zawiera pole origin w każdej wiadomości zdalnej.
* Znaczne oczyszczenie kodu ułatwiające dokonywanie zmian w przyszłości.

