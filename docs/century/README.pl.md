# Century — 100 nowych tapet

Osobna kolekcja 001–100, w dziesięciu dziedzinach: kosmos, energia, woda,
biologia, wytwarzanie, transport, instrumenty, schronienia, sprzęt osobisty
i codzienne absurdy. Każda plansza ma własną nazwę, funkcję, opis i podpis A.
Modele powstały od zera z treści koncepcji.

## Oglądanie

[Dopracowana dziesiątka — przed/po](../../concepts/century/refined-ten/index.html)
ma dodatkowe wykresy, faktoidy, detale i humor. B przełącza wersję w podglądzie.
[Lista zmian i źródła](REFINED-TEN.pl.md).

Z katalogu projektu:

```sh
python3 tools/view_wallpapers.py --dir concepts/century/finalized/wide
```

To istniejąca przeglądarka imv z 20 zachowanymi planszami Century; odrzucone 80 jest wyłącznie w archiwum galerii HTML. ← i → zmieniają tapety,
Esc zamyka. Można zacząć od numeru lub nazwy, dopisując go na końcu polecenia (`99`, `light-sail`). Samo `python3 tools/view_wallpapers.py` otwiera zestaw roboczy.

[Galeria HTML](../../concepts/century/index.html) działa też bez serwera,
bez pobierania bibliotek z internetu. Ma wyszukiwanie, dziedziny, oba formaty,
strzałki, Esc, F (pełny ekran) i I (opis). Przy ograniczeniu pełnego ekranu
przez przeglądarkę można użyć F11 lub przeglądarki imv.

Lokalny podgląd podczas sesji: http://127.0.0.1:8192/.
Po restarcie można otworzyć plik HTML albo uruchomić:

```sh
python -m http.server 8192 --bind 127.0.0.1 --directory concepts/century
```

## Pliki i pochodzenie

- `concepts/century/wide/`: 100 plików WebP, **5120×2160**.
- `concepts/century/16-9/`: 100 plików WebP, **5120×2880**.
- `concepts/century/models/`: sceny Blender z nazwanymi częściami.
- `tools/assets/century/`: widoczne ścieżki A/B/C i metadane podzespołów.
- `concepts/century/qa/`: audyty układu, pomiary segmentów rigu i arkusze przeglądowe.
- [Katalog wszystkich pomysłów](CONCEPTS.md).
- [Realne podstawy i granice źródeł](RESEARCH.md).
- [Manifest](manifest.json): rozdzielczości, SHA-256 oraz źródła użyte w produkcji.

Oba formaty są rasteryzowane natywnie z geometrii wektorowej. Nie używają
upscalingu, modeli generujących gotowe bitmapy ani katalogu imagen.
Szeroki format zawiera A/B/C. Kompaktowy 16:9 pokazuje A, zachowując miejsce
na legendę i znak. Logo pochodzi z oryginalnego SVG; litery składa Cairo
z Nimbus Sans. Ziarno i halacja są osobnym końcowym etapem.

## Kontrola i dalsze poprawki

Przewodnikiem pozostaje [poradnik produkcji](../WALLPAPER-PRODUCTION-GUIDE.pl.md).
Audyty obejmują napisy i geometrię w obu natywnych rozdzielczościach, obecność
A/B/C, unikalność nazw, pliki i zgodność długości kończyn. Ocena artystyczna
przez użytkownika pozostaje otwarta. To ilustracje spekulacyjnych maszyn,
a nie dokumentacja do produkcji lub zwalidowane urządzenia medyczne.

Rejestr `catalog.json` jest źródłem aktualnych opisów. `catalog_seed.py`
zachowuje początkowy brainstorming i celowo odmawia nadpisania rejestru.
Przy zmianie koncepcji aktualizuj rejestr przez `registry.update` oraz model.

Przykład przebudowy pojedynczej planszy:

```sh
blender -b --python-exit-code 1 --python tools/century/build.py -- --ids 31 --force --maintenance
python tools/century/render.py --ids 31 --force --maintenance
python tools/century/audit.py --ids 31
python tools/century/gallery.py
python tools/century/document.py
```

Procesy nocne mają ograniczenie czasu do 25 września 2026, 08:00 Europe/Warsaw.
Dla późniejszych, świadomie uruchamianych poprawek służy opcja `--maintenance`.
Nie włącza się automatycznie i nie była użyta w tej nocnej produkcji.

Przy większej przebudowie po `build --force` można uruchamiać krótkie partie:

```sh
python tools/century/batch.py --limit 32 --maintenance
python tools/century/batch.py --check
```

Pierwsze polecenie wybiera maksymalnie 32 brakujące, starsze od geometrii lub
uszkodzone pliki. Powtarzaj je do wyniku `Native files to render: 0`.
Renderer zapisuje plik tymczasowy i dopiero po zakończeniu zastępuje master.
Zmiana samego stylu, fontu lub treści wymaga jawnego `render --force`;
wznowienie porównuje geometrię i sprawdza obrazy, nie interpretuje zmian kodu.


## Aktualna selekcja

Z oryginalnej setki zachowano 20 koncepcji. [Rejestr decyzji](CURATION.pl.md)
zawiera 80 odrzuconych pomysłów z indywidualną argumentacją. Galeria główna
pokazuje domyślnie zachowane 20; archiwum jest dostępne przez filtr. Zwykłe
polecenia batch/build/render pomijają odrzucone projekty; jawne `--ids` pozwala
wrócić do pojedynczego projektu dopiero na prośbę użytkownika.

- [Druga dopracowana dziesiątka](REFINED-NEXT-TEN.pl.md)
- [Porównania przed / po](../../concepts/century/refined-next-ten/index.html)
- [Dziesięć nowych pomysłów 101–110](NEXT-TEN-IDEAS.pl.md)


## Wspólna kolekcja

Obie dopracowane dziesiątki są zaakceptowane. `python3 tools/view_wallpapers.py --collection finalized` otwierało wtedy 34 gotowe plansze (pierwotne 14 + Century 20). [Wspólny rejestr](../collection/README.md) obejmuje również kolejkę 10 nowych pomysłów. [Ranking](../collection/QUALITY-RANKING.md) proponuje próg po pozycji 22. Użytkownik zlecił redesign dwunastu niżej ocenionych; [nowe wersje i porównanie](../../concepts/century/quality-redesign/index.html) oczekują oceny. Kolekcja nadal zawiera wszystkie 34 plansze.
