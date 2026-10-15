# Century: 100 nowych tapet — produkcja nocna

- Zlecenie: samodzielnie stworzyć 100 nowych tapet, bez pytań do użytkownika.
- Start: 2026-09-24 23:42 Europe/Warsaw (21:42 UTC).
- Bezwzględny koniec: **2026-09-25 08:00 Europe/Warsaw (06:00 UTC)**.
- Zatrzymać wcześniej, gdy 100 nowych tapet jest kompletnych i sprawdzonych.
- Aktywny cel w tym zadaniu obejmuje pełną produkcję, nie tylko listę pomysłów.
- Wzorce: 14 istniejących tapet i docs/WALLPAPER-PRODUCTION-GUIDE.pl.md.
- Technika: autorskie modele Blender, ukrywanie linii BVH, Cairo, Nimbus Sans i oryginalne logo.
- Zakaz korzystania z katalogu imagen; bez modeli generujących bitmapy/upscalingu.
- Nowa kolekcja jest osobnym zestawem 001–100. Nie zastępuje 14 istniejących tapet.
- Bez commit/push; użytkownik nie zlecił publikacji tej partii.
- Kod: tools/century/. Rejestr: docs/century/catalog.json.
- Rendery: concepts/century/wide/ i concepts/century/16-9/.
- Podglądy i raporty: concepts/century/previews/ oraz concepts/century/qa/.
- Nie utożsamiać weryfikacji technicznej z akceptacją artystyczną użytkownika.

## Stan

**UKOŃCZONE — 2026-09-25 01:47 Europe/Warsaw. Zatrzymano po 100 tapetach przed 08:00.**

- 100 unikalnych koncepcji i autorskich modeli, 300 widoków wektorowych.
- 200 finalnych plików: 100 × 5120×2160 i 100 × 5120×2880; bez upscalingu.
- 200/200 audytów układu PASS; wszystkie obrazy zdekodowane i aktualne wobec geometrii.
- package.py: PASS, 1,13 GB natywnych obrazów; manifest.json zapisany.
- Wszystkie kompozycje obejrzane, szczegóły kontrolowane na próbkach 1:1.
- Galeria lokalna: concepts/century/index.html; przeglądarka desktopowa: `python3 tools/view_wallpapers.py --dir concepts/century/finalized/wide`.
- Poradnik produkcji i katalog opisów uzupełnione.
- Pozostaje wyłącznie ocena artystyczna użytkownika; nie wznawiać automatycznie produkcji.

Poniżej zachowano historyczny dziennik pracy. Jego wcześniejsze stany pending
zostały zamknięte powyższą kontrolą końcową.

## Dziennik historyczny

Sprawdź zegar i aktualny cel. Przeczytaj ten plik oraz catalog.json, jeśli istnieje.
Kontynuuj najbliższą nieukończoną partię. Aktualizuj ten dziennik po każdej partii.
Nie czekaj na użytkownika. Nie zatrzymuj się po samej infrastrukturze lub liście pomysłów.
Po 08:00 nie zaczynaj kolejnych renderów. Zapisz faktyczną liczbę gotowych plików.

Rejestr kompletny: `docs/century/catalog.json` i czytelne `CONCEPTS.md` zawierają
100 unikalnych koncepcji w 10 dziedzinach. Każda ma indywidualny opis spekulacji,
własne A/B/C i paletę. Rozpoczęta budowa infrastruktury oraz pierwszych modeli.

2026-09-25 00:15 — 40 autorskich modeli gotowych (orbit, energy, water, biology).
Każdy ma trzy projekcje ze wspólnej geometrii. Natywne rendery i audyty trwają partiami.
Pierwsze 20 modeli przeszło audyt A/B/C, geometrii i tekstu w obu formatach.
Pierwsze 10 obejrzane na kontakcie; korekta C z nadmiernie bocznego kąta do czytelnego 3/4
jest w kit.py i wymaga przebudowy wcześniejszych 30 modeli przed finałem.
Light Sail: przebudowane wnętrze reefingu oraz rzeczywisty zawias zamiast długiej belki C.
Registry ma blokadę pliku, więc niezależne renderowanie/audyt nie nadpisują metadanych.

2026-09-25 00:45 — **100/100 autorskich modeli** zbudowane. Natywne warianty
renderują się partiami; wszystkie pierwsze audyty dotychczas przeszły bez kolizji.
NIE oznaczać jeszcze celu jako kompletnego: trwa przegląd wizualny i korekty.

Ważne poprawki globalne już w kodzie, wymagają finałowego `build --force` i `render --force`:
- Kołnierze miały zbyt wąski pierścień w stosunku do rozstawu śrub. Teraz śruby
  mieszczą się w materiale, a małe przeguby mają proporcjonalną głębokość i śruby.
- C ma kamerę az+8 zamiast az+48; mechanizmy lepiej widać.
- Kabiny mają uszczelki wyliczane na powierzchni loftu, bez pływających okręgów.
- Dune Skimmer: identyczne lamele i piasty wszystkich czterech kół.
- Rescue Fan: podpory wszystkich czterech silników zgodne.
- Ice Mule: usunięto zdublowane środkowe koła przez unique xspan w kit.wheels.
- Ring Tender: uzupełniono dysze drugiego zbiornika.
- Spring Pack / Elastic Cartridge / Balance Spring: prawdziwe helisy, osłony
  zdejmowane tylko w widoku serwisowym C (kit.uncover).
- Sleep Cocoon: poprawione położenie siedziska, podłokietniki i fizyczne mocowanie
  równoległoboku fotela. Potrzebna ponowna kontrola obrazka.

Podglądy `concepts/century/qa/{domain}-pages.jpg` i `-heroes.jpg` buduje review.py.
Pierwsze rendery nie uwzględniają jeszcze powyższych zmian. Finalne przegenerowanie
całej setki ma nastąpić dopiero po przeglądzie. Status artystyczny: do oceny użytkownika.

2026-09-25 01:22 — Przegląd kompozycji ukończony dla 100 szerokich i 100 kompaktowych
plansz. Ostatni długi proces eksportu został przerwany sygnałem TERM przez środowisko;
wznowiono tylko brakujące pliki krótszymi partiami. Trzeba też sprawdzić dekodowanie
plików zapisanych w chwili przerwania. /tmp/century-resume-render.py obsługuje wznowienie.
Audyty 001–035 finalne PASS; reszta biegnie czterema krótszymi partiami.
Galeria: naprawiony rzeczywisty fullscreen (kontener wewnątrz dialogu), filtry, strzałki
i Esc sprawdzone. Serwer lokalny na 8192, karta przeglądarki 4.

2026-09-25 01:25 — Wszystkie 200 FINALNYCH audytów układu PASS.
Krótka pierwsza partia wznowienia (32 pliki) ukończona. Teraz używać
repozytoryjnego tools/century/batch.py --limit 32; sprawdza również dekodowanie.
visual-review.json ma już zakres faktycznego przeglądu, ale last_export_review
pozostaje pending do odświeżenia finalnych arkuszy po zakończeniu eksportu.

2026-09-25 01:36 — Nowy exporter: test regresji PASS, 200/200 nowych audytów PASS.
Natywne pliki 001–032 już finalne; trwa partia 033–064. Kolejne: batch.py --limit 64,
a potem pozostała końcówka. Geometria zamknięta do wydania, nie zmieniać bez nowego błędu.

## Późniejsza korekta: wybrana dziesiątka

Na nowe zlecenie użytkownika dopracowano 001, 010, 030, 031, 044, 056, 060,
087, 099, 100: dodatkowe części 3D, indywidualne panele danych, faktoidy i humor.
20 natywnych renderów i 20 audytów PASS; kontrola całego pakietu PASS.
180 pozostałych obrazów zachowuje poprzednie SHA-256. Przed/po zapisane,
przełącznik B oraz oba formaty sprawdzone w przeglądarce.
Galeria: http://127.0.0.1:8192/refined-ten/.
Zmiany opisano w REFINED-TEN.pl.md. Bez instalacji na pulpicie i publikacji Git.


## Druga selekcja i dopracowanie — 25 września 2026

- Zachowane 20: pierwsza dziesiątka zaakceptowana, druga do opinii użytkownika.
- Pozostałe 80 odrzucone; indywidualne uzasadnienia w CURATION.pl.md oraz katalogu. Pliki zachowane jako archiwum.
- Druga partia: 2, 6, 17, 18, 25, 38, 42, 65, 70, 80; części modeli 1338 → 2067.
- 20 plików natywnych w dwóch formatach, 20 audytów składu PASS.
- 180 pozostałych plików natywnych identycznych SHA-256 względem stanu przed pracą.
- Galeria refined-next-ten: przełącznik B, oba formaty; domyślny filtr galerii głównej to zachowane 20.
- 10 nowych briefów 101–110 w NEXT-TEN-IDEAS.pl.md, na razie bez generacji.
