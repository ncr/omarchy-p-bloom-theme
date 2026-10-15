# Rozszerzenie kolekcji do 42 tapet

Dodano osiem nowych koncepcji do 14 pierwotnych i 20 zachowanych Century.
Wybór, poprawki i kontrolę wykonał agent na wyraźne polecenie użytkownika
samodzielnego ukończenia kolekcji. To nie jest przypisanie użytkownikowi
osobistej akceptacji każdego nowego kadru.

| Nowa plansza | Mechanizm i powód wyboru |
|---|---|
| Velvet Hammer | Otwarty pierścień, krzywki przejmujące obciążenie i rejestrator zwolnienia; wyrazista asymetryczna sylwetka. |
| Bubble Bailiff | Esowaty kanał i kaseta kapilarna; czytelny problem nieważkości i gazu w obiegu cieczy. |
| Key Concord | Dwa równoprawne bębny, wspólne jarzmo i otwarta kaseta rygla; mechaniczny żart o zgodzie. |
| Metric Embassy | Karuzela fizycznych wzorców z głowicą pomiarową; humor wynika z różnicy między pasowaniem i zgodnością. |
| Muon Customs | Otwarta bramka z dwiema parami płaszczyzn śledzących; nauka z naturalnym ograniczeniem czasu zbierania danych. |
| Resonance Tailor | Trzy nierówne gałęzie rezonansowe, przesuwne masy i blokada; rytm części pokazuje funkcję. |
| Suture Loom | Naprzemienne uchwyty igły, szpula i napinacz; precyzyjna mechanika na neutralnej membranie testowej. |
| Spin Table | Okrągła misa w jarzmie, napęd, przeciwwaga i zamykana pokrywa; skala kuchenna zamiast cudownej grawitacji całego pokoju. |

Capillary Salon i Glass Amnesty pozostają w kolejce. Pierwszy wymaga osobnej
pracy nad pozą i ergonomią człowieka, drugi jest bliższy istniejącym urządzeniom
optycznym. Żadna z osiemdziesięciu odrzuconych koncepcji nie została przywrócona.
Numeracja 101–110 to identyfikatory kolejki, z zachowanymi lukami 102 i 109;
liczba dostępnych tapet wynosi 42, a nie 110.

## Rysunek i redakcja

Każde urządzenie ma własny model Blender. B i C są rzeczywistymi podzespołami
tej samej sceny. Eksportuje się widoczne linie z kontrolą zasłaniania; tekst,
logo i grain powstają osobno, deterministycznie. Oba formaty, 5120×2160 oraz
5120×2880, są składane natywnie, bez powiększania mniejszego rastra.

Wszystkie plansze zawierają A/B/C z nazwami konkretnych części, dwa osobne
diagramy tematyczne, metryczkę, Field Notes oraz pojedynczą cichą puentę na
środku dołu. Diagramy obejmują m.in. tablicę logiczną, przekrój membrany,
profil gwintu, śledzenie toru, model oscylatorów, geometrię napinacza i bilans
momentów. Wspólny rytm typografii nie zastępuje treści uniwersalnym flowchartem.

Przegląd pierwszych renderów spowodował poprawki: otwarcie kasety rygla,
uwidocznienie sprężyn, podparcie karuzeli i napinacza, skrócenie przewodu
rozciągającego obwiednię panelu C, odsunięcie skrzyżowanych sprężyn od osłony,
okrągłą misę z połączonymi czopami oraz poprawne połączenie jarzma z nogami.
Zachowano pierwsze wersje lokalnie w `concepts/century/extension-42/before/`.

## Podstawy i granice interpretacji

- **Velvet Hammer:** [NASA, non-pyrotechnic release mechanism](https://ntrs.nasa.gov/api/citations/19970021613/downloads/19970021613.pdf). Brak pirotechniki nie oznacza zerowego udaru; energia naprężenia nadal wymaga przejęcia. Diagram pokazuje stany kontaktów, nie wymyślony wynik pomiaru udaru.
- **Bubble Bailiff:** [NASA, capillary air/liquid separation](https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20100033580.pdf). Zdolność zatrzymania gazu zależy od zwilżania, cieczy, ciśnienia i porów. Krzywa 1/r zakłada stałą chemię powierzchni.
- **Key Concord:** autorska mechaniczna ilustracja logicznego AND. Nie przypisujemy jej klasy odporności zamka ani certyfikacji bezpieczeństwa.
- **Metric Embassy:** [NIST, pitch diameter measurement](https://www.nist.gov/publications/pitch-diameter-measurement-threaded-gages-using-cmm). Pomiar gwintu nie sprawdza polaryzacji ani napięcia. Rejestr 12/8/3 jest jawnie fikcyjny.
- **Muon Customs:** [Los Alamos, tomography with cosmic-ray muons](https://laro.lanl.gov/esploro/outputs/journalArticle/Tomographic-Imaging-with-Cosmic-Ray-Muons/9916364485503761). Pokazany tor jest ilustracją. 1/√N dotyczy idealnej względnej niepewności zliczeń, nie gwarancji jakości tomogramu.
- **Resonance Tailor:** [NASA, Compact Vibration Damper](https://technology.nasa.gov/patent/LAR-TOPS-189). Wykres f∝1/√m opisuje pojedynczą idealną gałąź przy stałej sztywności. Nie obiecuje tłumienia wszystkich częstotliwości.
- **Suture Loom:** [Robotic micro-suturing research](https://arxiv.org/abs/2002.00530). Mechanizm badawczy na neutralnym materiale; nie gotowe narzędzie kliniczne. Wykres opisuje zaplanowane stany chwytów.
- **Spin Table:** [NASA, centrifugal/centripetal motion](https://science.nasa.gov/learn/basics-of-space-flight/chapter3-3/). a=ω²r opisuje misę; równowaga m₁r₁=m₂r₂ jest uproszczeniem statycznym, a rzeczywisty wirnik potrzebuje także wyważenia dynamicznego.

## Powtarzalność i wydanie

```sh
python3 tools/century/extension_catalog.py
blender -b --factory-startup -t 4 --python-exit-code 1 --python tools/century/build.py -- --ids 101,103,104,105,106,107,108,110 --force --maintenance
python3 tools/century/render.py --ids 101,103,104,105,106,107,108,110 --format both --force --maintenance
python3 tools/century/audit.py --ids 101,103,104,105,106,107,108,110
python3 tools/release_collection.py --format wide
```

`release_collection.py` wybiera tylko członków kolekcji. Sprawdza natywny
rozmiar i skróty, pakuje komplet 42 obrazów, tworzy miniatury oraz manifest
`docs/collection/release.json`. Dla gałęzi 16:9 używa się `--format 16-9`.
Companion korzysta z lokalnych masterów, a w świeżym klonie ze wszystkich
42 plików `backgrounds/`. Dawny `century/package.py` dotyczy archiwalnej setki;
nie służy do wydawania obecnej kolekcji.
