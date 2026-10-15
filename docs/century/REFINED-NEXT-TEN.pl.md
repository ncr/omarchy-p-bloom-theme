# Century — druga dopracowana dziesiątka

Wybrane: **002, 006, 017, 018, 025, 038, 042, 065, 070, 080**.
Pierwsza zaakceptowana dziesiątka pozostaje osobną partią. Wszystkie pozostałe
80 koncepcji ma trwały status odrzuconych w katalogu i [rejestrze decyzji](CURATION.pl.md).

[Galeria przed/po](../../concepts/century/refined-next-ten/index.html): B przełącza
wersję, strzałki zmieniają planszę, F pełny ekran, Esc zamyka. Oba formaty natywne.
W `concepts/century/refined-next-ten/before/` zachowano oryginalne 20 obrazów i
projekcje wektorowe; katalog sprzed zmian jest obok.

| Projekt | Rozwinięcie geometrii | Panel i ton opowieści |
|---|---|---|
| 002 Tidal Loom | Zgodny osprzęt obu turbin: wymienne wargi osłon, anody, uszczelnienia wałów, czujniki i przyłącza | Strumień dostępnej energii ∝ moduł prędkości³. Księżyc odmówił podpisania SLA |
| 006 Manta Foil | Mocowania osi, inspekcyjne szwy płatów, obsługa dyszy, podziały kabiny, poręcze i knagi | Siła nośna ∝ prędkość² przy stałym CL. Choroba morska nie zaakceptowała poprawki |
| 017 Memory Kiln | Skale i enkoder ogniskowania, pierścienie regulacji, fiducjale płyt, indeks karuzeli i uchwyt instrukcji | Symboliczna mapa orientacji z kluczem odczytu. README w zestawie, cywilizacja osobno |
| 018 Lunar Porch | Drugie uszczelnienie, porty testowe, dźwignie zamków, uszczelka szuflady i przyłącza serwisowe | Wyraźna granica brudnego skafandra i kabiny. Proszę wytrzeć planetę przed wejściem |
| 025 Fibre Braid | Napinacze i ceramiczne oczka wszystkich szpul; zastąpienie starego splotu rodzinami o przeciwnych kierunkach | Kąt włókna względem osi a prędkość odbioru. Włókna, w przeciwieństwie do komisji, mają kierunek |
| 038 Quiet Stair | Zgodny osprzęt stopni i przegubów, łożyska wału, listwa kontaktowa, noski i ręczne zwolnienie | Kolejność: wolny pomost → ruch → blokada. Dostępność nie jest zadaniem pobocznym |
| 042 Wind Kite | Prowadnica równomiernego nawijania, śruba, hamulec, mocowania żeber i uzdy, ucha kotwienia | Pętla siła–długość liny: powrót też kosztuje energię. Ze sztormem się nie negocjuje |
| 065 Seam Surgeon | Podziałka kołnierza, podawanie drutu, śledzenie łuku, sprężyny sondy i przewód sprzęgający | Fikcyjna mapa 12 sektorów: 9 przyjętych, 2 wstrzymane, 1 do poprawy. Termin nie jest parametrem spawania |
| 070 Queue Garden | Mechaniczne zatrzaski liści, indeksator łodygi, pierścienie rolek i elementy czytnika | Schodkowy dziennik 6 obsłużonych pozycji. Pięć minut — od zeszłego wtorku |
| 080 Compliment Mill | Kalibracja tacy, pierścienie i synchronizacja optyki, napinacze papieru i detal wydruku | Fikcyjna selekcja: 3 konkretne pochwały, 7 ogólników, 2 bez dowodów. „Amazing” nie przeszło inspekcji |

## Granice wykresów i źródła

- Tidal Loom: strumień energii kinetycznej przez stałe pole to ½ρA|v|³,
  wynik masowego przepływu ρA|v| i energii na jednostkę masy ½v². To obliczenie
  geometryczno-fizyczne, nie charakterystyka sprawności naszej turbiny.
- Manta Foil: [równanie siły nośnej NASA](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/lift-equation/).
  Na wykresie stałe są gęstość, powierzchnia i współczynnik CL. Nie modelujemy
  kawitacji, powierzchni swobodnej ani regulatora wysokości.
- Memory Kiln: [Microsoft Research, Project Silica](https://www.microsoft.com/en-us/research/project/project-silica/).
  Istnieją badania zapisu struktur laserem femtosekundowym i odczytu optycznego;
  nasza mapa czterech orientacji jest symbolem, nie rzeczywistym kodekiem ani
  twierdzeniem o pojemności lub trwałości urządzenia.
- Lunar Porch: [NASA, suitport](https://techport.nasa.gov/projects/10728) i
  [ograniczenia metod wejścia/wyjścia](https://www.nasa.gov/wp-content/uploads/2017/02/2018-_eva_airlocks_and_alternate_ingressegress_methods_document.pdf).
  Skafander pozostaje na zewnątrz; projekt nadal potrzebuje kontroli szczelności,
  obsługi pyłu i osobnej drogi awaryjnej. Schemat nie obiecuje idealnej izolacji.
- Fibre Braid: autorska konstrukcja geometryczna helisy: tan α = vt/vz,
  stała prędkość styczna i zmienna osiowa. Nie prognozuje wytrzymałości kompozytu.
- Quiet Stair: autorski schemat kolejności blokad. Nie jest dowodem kinematycznej
  wykonalności transformacji ani certyfikacją dostępności lub bezpieczeństwa.
- Wind Kite: [AWESCO, sterowanie cyklem pompowym](https://www.awesco.eu/publication/licitra-2019-a/licitra-2019-a.pdf).
  Pętla używa ilustracyjnych znormalizowanych sił, pomija przejścia i straty.
  Pole pętli opisuje pracę mechaniczną; energię elektryczną należałoby pomniejszyć o straty.
- Seam Surgeon, Queue Garden i Compliment Mill: wszystkie liczby są jawnie
  fikcyjnymi dziennikami, nie wynikami pomiarów ani benchmarkami.

Typografia i znak Omarchy pozostają w deterministycznej warstwie Cairo/SVG.
Detale B/C są wybranymi częściami tego samego modelu A. Żaden obraz nie jest
wynikiem upscalingu lub modelu generowania obrazu.
