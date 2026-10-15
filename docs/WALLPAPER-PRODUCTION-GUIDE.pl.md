# Futurystyczne blueprinty — poradnik produkcji

Zapis ustaleń projektu z 24 września 2026. Dla kolejnych sesji i autorów,
którzy mają stworzyć większą kolekcję, docelowo około 100 tapet tej klasy.
To specyfikacja kierunku i kontrola jakości, nie tylko prompt stylistyczny.
Bieżące polecenie użytkownika ma pierwszeństwo.

## 1. Efekt, do którego dążymy

Dokumentacja urządzeń z przyszłości, oglądana jak autentyczny materiał
techniczny. Inspiracja: hierarchia i subtelność loading screenów Destiny,
estetyka rysunków technicznych NASA oraz elegancki retrofuturyzm Fallout.
Własne urządzenia, nazwy i historie; bez kopiowania znaków i maszyn tych marek.

„Artefakt z przeszłości” oznacza tutaj dokument z przyszłości, który dla jeszcze
późniejszego obserwatora będzie historyczny. Nie oznacza westernu, sepii,
rdzawego pergaminu, RDR2 ani sceny sfotografowanej na starym biurku.
Wrażenie materialności dają dyskretne ziarno, halacja i zróżnicowanie tuszu.
Geometria i liternictwo pozostają precyzyjne.

Tapeta musi działać najpierw jako piękna kompozycja i czytelna sylweta,
potem jako urządzenie, na końcu jako zbiór detali do odkrywania z bliska.
Liczba kresek sama w sobie nie jest jakością. Puste miejsce jest częścią projektu.

## 2. Co obejrzeć przed rozpoczęciem

Lokalny [arkusz wzorców](references/contact-sheet.jpg) pokazuje stan kolekcji
w momencie pisania poradnika. [Manifest](references/manifest.json) podaje
pliki źródłowe, ich SHA-256, rozdzielczości i statusy. Podglądy są pomniejszone;
ocenę linii w skali 1:1 wykonuj na pełnych renderach wskazanych w manifeście.
Hash pozwala wykryć późniejszą zmianę źródła; sama ścieżka nie jest archiwum.

| Przykład | Czego się uczyć | Granica użycia |
|---|---|---|
| Fusion Transport | Atrakcyjna sylweta, segmentacja, kratownica, radiatory, różne skale detalu | Parametry podróży są treścią fikcyjnego projektu, nie symulacją orbity |
| Sky Racer, główny i lewy rysunek | Wspólny model kadłuba i rzeczywisty przekrój kokpitu, baterii i fotela | Nowy prawy tor jest studium, jeszcze bez osobnej akceptacji |
| Tether Climber | Przestrzenne wyposażenie i powiększenia materiału o różnym poziomie skali | Warstwy taśmy to koncepcja; skala grubości jest wyolbrzymiona |
| Truth Lamp | Techniczna postać przy stole, humor w dokumentacji, czytelne dane | Nie przywracać fotorealistycznej sceny jako głównej ilustracji |
| Air Refinery | Rozdzielenie strumieni materiału i energii, przestrzenne symbole aparatury | Enzymatyczna droga pozostaje spekulacją |
| Bounder | Człowiek rzeczywiście używa sprzętu; osprzęt jest osadzony na tym samym rigu | Pozy nadal podlegają ocenie, nie są przechwyconym ruchem |
| Proxy, poprawiona poza | Wspólne długości kończyn, przeciwstawny wymach, poprawiony kierunek kolana | Ostatnia korekta oczekuje opinii użytkownika, nie jest wzorcem certyfikowanej biomechaniki |
| Organ Foundry, prawy panel | Zorganizowany przekrój zamiast losowych kółek w obrysie | Nowe studium, uproszczona koncepcja druku, nie atlas anatomiczny |

Szczególnie obejrzyj [Proxy przed i po](references/proxy-gait-before-after.jpg).
Starsze rysunki w `backgrounds/`, `previews/` oraz katalogach `concepts/`
mogą pochodzić sprzed poprawek. Najświeższy zestaw roboczy jest w
`concepts/development/`; obecność tam nie oznacza akceptacji każdego elementu.

Nie kopiuj bez sprawdzenia: losowej macierzy receptorów Aroma Organ, dowolnych
wykresów wydajności ani historycznych uproszczeń sylwetek. Zamrożone podglądy
w `references/` pochodzą sprzed ujednolicenia oznaczenia A; jego aktualną postać
wyznacza wspólna funkcja `Sheet.end_main()`, a nie starsze obrazki referencyjne.
Aktualne oznaczenia wszystkich 14 plansz pokazuje
[osobny arkusz A](references/all-A-labels.jpg).

## 3. Każda tapeta zaczyna się od urządzenia i historii

Najpierw zapisz: co urządzenie robi, dla kogo, dlaczego istnieje, co jest wejściem
i wyjściem, jakie ma główne podzespoły oraz czego jeszcze nie umiemy zbudować.
Dopiero potem projektuj jego kształt. Udany redesign zaczynał się od treści
plakatu, a nie od ozdabiania dotychczasowego schematu.

W kolekcji przeplatają się urządzenia poważne, rekreacyjne i satyryczne.
Humor wynika z potrzeb człowieka: Proxy biega za właściciela, Greener wygrywa
z sąsiadem, Truth Lamp psuje kolacje. Dokumentacja traktuje je serio.
Nowa tapeta potrzebuje własnego pomysłu, nie kolejnej obudowy tej samej maszyny.

Przy zmianie istniejącej tapety zachowuj jej funkcję, nazwy, cytaty, liczby,
datę, sens żartu i legendę, chyba że użytkownik zlecił zmianę treści albo
usuwasz rozpoznany błąd. Zmianę znaczenia opisz w wyniku. Nie podmieniaj
oryginalnych zdań na podobne tylko dlatego, że łatwiej mieszczą się w układzie.

W nowych projektach oddziel realną podstawę od postulowanego przełomu.
Źródła techniczne zapisuj obok koncepcji. Parametry fikcyjne mogą być konkretne,
ale muszą być spójne jednostkowo i nie mogą udawać wyników obliczeń.

## 4. Obowiązujący sposób wykonania

1. Oryginalny model w Blenderze, z nazwanymi elementami i sensowną konstrukcją.
2. Dla postaci wspólny model i rig; dla sprzętu wspólna geometria wszystkich widoków.
3. Projekcja ortograficzna oraz usuwanie niewidocznych linii testami BVH.
4. Zapis widocznych ścieżek i punktów mocowania odnośników w JSON.
5. Kompozycja wektorowa w Cairo, tekst z fontu, logo z oryginalnego SVG.
6. Rasteryzacja bezpośrednio do docelowej rozdzielczości i kontrolowany postprocessing.

To nie jest bitmapowy tracing. Obrys wynika z geometrii 3D. Zdjęcia, lokalne
modele obrazowe, OpenPose lub zgrubne maski mogą pomagać w referencji i ocenie
pozy, ale nie zastępują poprawnej budowy końcowego rysunku. Nie korzystaj
z katalogu `imagen`. Nie wracaj domyślnie do generowania gotowych tapet
modelem obrazowym ani do upscalingu niskiej rozdzielczości: to podejście zostało
odrzucone z powodu artefaktów, utraty detalu, stylu i stabilności napisów.

KiCad przydaje się do rzeczywistych kształtów płytki i rozmieszczenia komponentów.
Ilustracyjna płytka nie jest automatycznie działającym, sprawdzonym elektrycznie PCB.

## 5. Sprzęt: forma, konstrukcja, hierarchia

- Projektuj sylwetę: proporcje, zwężenia, podcięcia, przestrzenie między modułami,
  podpory, pokrywy i czytelny kierunek przepływu lub ruchu.
- Retroprzyszłość ma kształtowane odlewy, kołnierze, żebra, osłony i sensownie
  prowadzone przewody. Sama skrzynka z setką śrub nadal jest skrzynką.
- Główna bryła, mechanizm i detale serwisowe mają różne grubości oraz jasności linii.
  Obrys prowadzi wzrok; śruby i faktury nie konkurują z nim.
- Detal musi należeć do części i mieć sens: łożysko, uszczelnienie, uchwyt,
  szyna, kanał, radiator, złącze. Nie dodawaj losowego technicznego ornamentu.
- Asymetria wynika z funkcji: dostęp serwisowy, dopływ, sterowanie, zawias.
  Powtarzalne części nadal muszą być identyczne tam, gdzie wymaga tego konstrukcja.
- Przekrój pokazuje wnętrze tej samej maszyny. Nie jest drugim, niezależnym gadżetem.
- Unikaj wielkich pustych owali i okręgów stosowanych jako uniwersalny wypełniacz.
  Ramka kołowa jest uzasadniona powiększeniem, przyrządem lub osią, nie przyzwyczajeniem.
- Delikatne, kolorowe pola nie mogą być ostrzejsze i bardziej dominujące niż sprzęt.
  Przykładem błędu był agresywny niebieski kształt w Volumetric Stage.
- Obiekty organiczne również muszą być czytelne: trawa, gnomy, tkanka i włókna
  potrzebują dobrego konturu oraz skali, a nie jedynie większej liczby kreskowań.

## 6. Postacie i biomechanika — obowiązkowa kontrola

Konwencja: manekin techniczny inspirowany crash dummy i Optimusem. Gładkie,
uproszczone głowy, smukłe osłony, czytelne przeguby, dyskretne znaczniki pomiarowe.
Bez fotorealistycznych ludzi na głównym blueprincie, ekspresyjnych twarzy,
włosów, rysowania mięśni oraz sylwetek z kilku nachodzących na siebie prymitywów.

Nie używaj mocnych czarnych wypełnień wizjera, barków i szyi. Zostaw cienką
linię i delikatny jasny ton. Połączenie barki–szyja ma być zwarte i ciągłe.
Dłonie są zwartymi technicznymi bryłami z klinem kciuka, bez wachlarza palców.
Stopy i dłonie mają płaszczyzny i delikatne zaokrąglenia, nie kształt baloników.

Jeżeli taki manekin oznacza człowieka, umieść czytelną, pasującą do humoru
adnotację: np. HUMAN OWNER albo HUMAN INSIDE. Nie zmieniaj w ten sposób
fabularnego człowieka w robota. Proxy rzeczywiście jest robotem bez głowy;
zachowaj NONE FITTED i jednoznaczny symbol braku zamiast przypadkowej elipsy.

Kontrola każdej pozy:

1. Lewe i prawe udo, łydka, ramię, przedramię, dłoń i stopa pochodzą z tych
   samych definicji. Perspektywa może zmienić wygląd, nie długość modelu.
2. Przeguby łączą się fizycznie; sprawdź szyję, bark, nadgarstek, biodro i kostkę.
3. Zgięcie kolana ma poprawny znak. Sama zgodność długości w IK tego nie gwarantuje.
4. Przy biegu sprawdź jedną konkretną fazę: nogę prowadzącą, odzyskującą,
   moment kontaktu albo lotu. Nie składaj kończyn z różnych faz cyklu.
5. Wymach ramion jest przeciwstawny do nóg. Sprawdź go po stronach rigu,
   nie tylko według tego, co znajduje się z lewej strony obrazka.
6. Łydka ma wybrzuszenie z tyłu, piszczel z przodu. Lokalna rama segmentu
   skierowanego w dół może odwrócić profil — taki błąd już wystąpił w Proxy.
7. Stopa wynika z orientacji podudzia i fazy ruchu. Nie trzymaj obu butów
   poziomo, kiedy jedna pięta wraca pod pośladek.
   Sprawdź też stronę podeszwy: prostopadłość stopy do podudzia dopuszcza
   dwie orientacje różniące się o 180°. W Bounderze tylna stopa i sprężyna
   były odwrócone ku piszczeli, mimo że miały wspólną macierz obrotu.
   Normalna podeszwy musi wskazywać od podudzia, a sprężyna pozostawać po
   podeszwowej stronie buta. Wspólna transformacja sama nie dowodzi poprawności.
8. Postać siedząca ma oparcie, kontakt z siedziskiem i sensowne położenie stóp.
   Stojąca opiera podeszwy o właściwą powierzchnię. Bieg w fazie lotu jest wyjątkiem.
9. Kciuki w neutralnym frontalnym widoku są skierowane na zewnątrz, zgodnie
   z wybraną konwencją użytkownika. W innych pozach kontroluj rotację całej dłoni.
10. Model i nakładany zegarek, sprzęt, linie wymiarowe oraz odnośniki korzystają
    z tych samych współrzędnych. Nie utrzymuj drugiej, rozjeżdżającej się pozy 2D.

Aktualne źródło pozy Proxy: `tools/mannequin3d/proxy_pose.py`; wspólne bryły:
`tools/mannequin3d/build.py`. To autorskie pozy ilustracyjne, nie zwalidowana
biomechanika. Obejrzenie całej sylwetki i detali wciąż jest konieczne po testach.

## 7. Boczne ilustracje i podstawa naukowa

Jakość dotyczy całej planszy. Przestrzenna główna maszyna z płaskim starym
insetem obok to nieukończona aktualizacja. Lewy i prawy panel mają wyjaśniać
inną rzecz: wnętrze, użycie, system, materiał albo dane. Nie powtarzać tej samej bryły.

Nie rysuj losowych kratek jako danych receptorowych, dowolnych krzywych jako
wyników pomiaru ani dekoracyjnych połączeń jako naukowego mechanizmu.
Weryfikuj źródło lub jasno przedstaw koncepcję. Rozróżniaj uproszczenie
topologii, wyolbrzymienie skali i fikcyjne parametry urządzenia.

Przykłady dobrego kierunku: kod powierzchniowy z poprawnymi relacjami stabilizatorów,
rzeczywisty przekrój kokpitu, oddzielne CO₂/wodór/energia, wiązki CNT zamiast
przypadkowej siatki heksagonów, tkanka z rozdzielonym układem naczyń i odpływu.
Nie twierdź na podstawie wyglądu, że urządzenie, organ lub materiał da się wyprodukować.

## 8. Napisy, oznaczenia i odnośniki

Oryginalny `tools/omarchy-logo.svg` jest jedynym źródłem logotypu. Nimbus Sans
i wspólne funkcje `Sheet` odpowiadają za tekst. Bez generowania napisów modelem,
przerysowywania znaku „podobną czcionką” oraz indywidualnego skalowania liter.

Zachowaj wspólną geometrię nagłówków, legendy, numeru planszy i emblematu dla
danego formatu. Nie przenoś ich do rastra głównej ilustracji. Dłuższy tekst
dopasuj składem; nie łam krótkich cytatów bez potrzeby — to już poprawialiśmy
w zestawieniu Truth Lamp.

Każdy podpis ma leżeć obok części. Sprawdź tytuł i pełen podtytuł, obie proporcje,
inne podpisy oraz geometrię rysowaną później. Punkt odnośnika zostaje na części;
przesuwaj załamanie i blok tekstu. Unikaj prowadzenia linii przez inne części.
Nie maskuj kolizji prostokątem tła i nie dopisuj wyjątku do audytu tylko po to,
żeby test przeszedł. Numer umieszczony celowo na własnym symbolu to inny przypadek.

Wszystkie plansze: A = główny widok, B = lewy, C = prawy, jeżeli te widoki
występują. Wspólna funkcja `Sheet.end_main()` dodaje A w takiej samej ramce
i typografii jak B/C. Nie dodawaj kolejnego A w indywidualnym rendererze.
Audyt wymaga dokładnie jednego A, B i C na każdej aktualnej planszy, w obu
formatach. Sprawdza również pojedyncze litery rysowane przez `text_mid()`.
Nazwa przy A musi być unikalna i opisywać konkretny obiekt lub scenę, np.
DUCTED-FAN RACER, AUTOLOGOUS KIDNEY PRINTER albo DELEGATED MORNING RUN.
Nie stosuj ogólników typu ASSEMBLY, UNIT, MAIN VIEW lub CONFIGURATION,
nawet z innym rzeczownikiem przed nimi. To podpis urządzenia, nie nazwa
techniki renderowania. Ta zasada dotyczy również przyszłych partii kolekcji.

## 9. Linie, rozdzielczość i wykończenie

Rysuj od razu w rozdzielczości docelowej. Zaakceptowane mastery to 5120×2160
oraz 5120×2880; pozostałe formaty macierzy wydań składa `tools/aspect_layout.py`
(sekcja 28). Dla innego monitora przelicz kompozycję; nie rozciągaj ilustracji.
PNG i aktualny eksport WebP są bezstratne. JPEG służy wyłącznie do lekkich podglądów.

Kontur zamkniętej bryły ma być ciągły. Przerwa jest uzasadniona rzeczywistym
zasłonięciem lub przekrojem. Małe luki po próbkowaniu nie są „analogowym charakterem”.
Poprawiaj granicę widoczności i łączenie ścieżek u źródła; nie domykaj wszystkich
końców bezmyślnie, bo połączysz różne części. Zachowuj ostre czubki, płaskie
podeszwy i wspólne styki po uproszczeniu ścieżek.

Widoczność liczy jeden moduł, `tools/hardware3d/hidden_line.py`, wspólny dla
eksportera Century/p(bloom) (`century/exporter.py`), rodziny sprzętu
(`family_core.export`) i symulatora kwantowego (`radial.py`). Punkt linii jest
widoczny, gdy żadna ściana (także tej samej bryły) nie leży przed nim dalej niż
0,03 jednostki; pomijane są tylko ściany wokół jego własnej krawędzi i ściany
tej samej powierzchni trafione stycznie. Próbki co 1/3200 rozpiętości widoku,
każda zmiana widoczności wyszukiwana bisekcją, więc linia kończy się dokładnie
tam, gdzie coś ją zasłania. Wierzchołki bryły są zespawane (szew pierścienia
lub osłony nie rysuje się w poprzek części), ściany mają spójny obieg i bryły
zamknięte patrzą na zewnątrz, a obrzeże płaskiego denka (n-kąta) rysuje się
w całości albo wcale. Kontur gładkiej powierzchni to krawędzie między ścianą
przednią i tylną, łańcuchowane w ciągłe linie; to dokładny obrys fasetowanej
bryły, więc kadr i położenie odnośników się nie zmieniają. Nie wracaj do
tolerancji „ta sama bryła = widoczne” ani 0,35 jednostki: rysowały ukryte
krawędzie (kreska przy wkręcie w Resonance Tailor, szwy i wewnętrzne obręcze
pierścieni, pozorne linie przez półkule First Light).

Eksportery zapisują widoczne krawędzie jako krótkie ścieżki. Każdy loader
widoków (`century/render.py`, `century/bloom/render.py`, `hardware3d/*_drawing.py`)
czyta je przez `tools/path_cleanup.load()`: łączy krawędzie jednej roli w ciągłe
linie (bez nakładek alfa i wcięć na stykach), scala współliniowe duplikaty,
dociąga końce do linii, której nie dosięgły lub którą przestrzeliły, i usuwa
bardzo krótkie luźne okruchy (kreski przerywane i kreskowanie zostają). Progi są
w jednostkach modelu, poniżej tolerancji eksportera; punkty otoczki wypukłej
się nie ruszają, więc kadr widoku jest identyczny. `PBLOOM_RAW_PATHS=1`
odtwarza surowe ścieżki. Kontrola: `tools/stroke_audit.py` (liczby przed/po
i wycinki), `tools/stroke_cleanup_review.py` (miejsca zmian na masterach).

Ziarno i delikatna halacja działają na końcu. Nie wyginają napisów ani geometrii,
nie mają udawać brakujących detali i nie mogą zjadać cienkich linii.
Porównuj podgląd całej tapety z cropem 1:1, szczególnie na docelowym ekranie.
Nie zużywaj wspólnego `s.rng` w nowej dekoracji: zmieni to dane/wykresy generowane
później. Użyj odrębnego, stałego ziarna. Powtarzalność wymaga tych samych źródeł,
fontów, ustawień i wersji środowiska; nie obiecuj identycznych bajtów między systemami.

## 10. Produkcja serii około 100 sztuk

Zbuduj rejestr pomysłów przed renderowaniem setki. Dla każdego wpisu zapisz:

```yaml
id: stable-slug
title: Nazwa urządzenia
category: serious | playful | satire
purpose: Jedno konkretne zastosowanie
narrative: Potrzeba człowieka lub sedno żartu
real_basis: Źródła i znane zasady działania
required_breakthroughs: Co pozostaje fikcją
main_silhouette: Forma i podzespoły
view_A: Główna ilustracja
view_B: Co wyjaśnia lewy panel
view_C: Co wyjaśnia prawy panel
human_role: none | operator | wearer | owner
palette: Zdefiniowana paleta, odróżniająca od sąsiadów
parameters: Wartości, jednostki i założenia
source_files: Modele, kod, fonty i zasoby
seed: Stałe ziarno
status: idea | built | qa_passed | reviewed | approved | installed
review_notes: Decyzje i rzeczy jeszcze do poprawienia
```

Zróżnicuj dziedziny, skalę i sylwetki: infrastruktura, medycyna, transport,
materiały, energia, komunikacja, dom, rekreacja i absurdalne potrzeby społeczne.
Nie produkuj stu wariantów cylindrycznej komory lub tego samego robota.

Najpierw kilka reprezentatywnych urządzeń o różnych kształtach, potem małe
partie, np. po 5–10. To praktyka kontroli jakości, nie nowy obowiązek proszenia
o zgodę na każdy krok. Wykonuj już zlecony zakres autonomicznie i stosuj
zaakceptowane poprawki globalnie tam, gdzie dotyczą wspólnego generatora.

Każda partia dostaje: pełne rendery, arkusz miniatur, powiększenia problematycznych
fragmentów, raport układu i krótką notatkę zmian. W rejestrze zapisuj faktyczny
status; wygenerowane nie znaczy sprawdzone, a sprawdzone nie znaczy zaakceptowane.
Do kolekcji pulpitu trafia wskazany zestaw, nie wszystkie eksperymenty z `concepts/`.

Numerację i nazwę pliku generuj z jednego rejestru. Przy 100 sztukach użyj
trzech cyfr (`001`…`100`) — sortowanie po nazwie musi odpowiadać kolejności.
Przeplataj palety i rodzaje ilustracji. Nie wprowadzaj ręcznych duplikatów numerów.

## 11. Procedura sprawdzenia i publikacji wyniku

1. Obejrzyj aktualny wzorzec i sprawdź stan plików; nie nadpisuj cudzych zmian.
2. Zapisz wersję „przed” z faktycznie oglądanego renderu, zwykle z development.
3. Zmień model lub generator u źródła, nie pojedynczą wyeksportowaną bitmapę.
4. Przebuduj właściwy model i renderuj do nowego katalogu przeglądu.
5. Obejrzyj sylwetę, przekroje, pozy, ręce/stopy, domknięcia i czytelność cropów.
6. Sprawdź długości par kończyn, kierunki zgięć, zgodność punktów 3D z adnotacjami
   i kontakt z podłożem tam, gdzie dotyczy to zmiany.
7. Uruchom audyt napisów dla obu formatów; usuń rzeczywiste kolizje.
8. Zapisz porównanie i decyzje; podmień atomowo właściwe pliki development.
9. Instalacja, commit i push następują w zakresie zleconym przez użytkownika.
   Sam render nie instaluje tapety i nie przełącza motywu.

Pułapka wykryta po korekcie Proxy: poprawiona poza była w development, ale
użytkownik nadal widział stary plik z aktywnego motywu. Przy dostarczaniu zmian
na pulpit porównaj sumy plików w development, `backgrounds/`, zainstalowanym
motywie i `~/.local/state/omarchy/current/theme/backgrounds/`. Samo podmienienie
pliku pod tą samą nazwą może nie odświeżyć obrazu: renderer Omarchy buforuje
go w pamięci. Zweryfikuj aktywną ścieżkę i rzeczywisty reload po instalacji.
W podsumowaniu rozróżniaj „w przeglądarce” od „na pulpicie”.

Przykład dla Proxy, z katalogu głównego repozytorium:

```sh
MANNEQUIN_ONLY=proxy blender -b --factory-startup -t 4 --python tools/mannequin3d/build.py
/usr/bin/python tools/make_wallpapers.py --only 13 --out concepts/new-review
/usr/bin/python tools/make_wallpapers.py --only 13 --size 5120x2880 --out concepts/new-review/16-9
/usr/bin/python tools/verify_wallpaper_layout.py --out concepts/new-review/layout.json
/usr/bin/python tools/verify_wallpaper_layout.py --size 5120x2880 --out concepts/new-review/layout-16-9.json
git diff --check
python3 tools/view_wallpapers.py --dir concepts/new-review 13
```

Audyt analizuje cały obecny zestaw. Jest kontrolą kolizji, nie oceną anatomii,
estetyki lub prawdziwości danych. Nie zastępuje obejrzenia wyniku.
Przeglądarka: strzałki zmieniają tapety, Esc zamyka, F przełącza fullscreen.
Lokalny Super+O pozwala przejść do pływającego okna.

Mapa kodu: `tools/sheet.py` — skład i eksport; `tools/starmap*.py` — styl linii;
`tools/hardware3d/` — modele sprzętu; `tools/mannequin3d/` — postacie;
`tools/projected_dummy.py` — ich rysowanie; `tools/right_aux_panels.py` — nowe
prawe panele; `tools/right_panel_studies.py` — Truth Lamp i Air Refinery;
`tools/order.py` — kolejność i palety. Szczegóły przebudowy poszczególnych
urządzeń znajdują się w `tools/FIDELITY.md`.

## 12. Rotacja w Omarchy

Sprawdzone w lokalnie zainstalowanym kodzie 24 września 2026:
`omarchy theme bg next` przechodzi do następnego pliku, sortuje ścieżki i po
ostatnim wraca do pierwszego. Nie jest to losowanie. Łączy tapety aktywnego
motywu z dodatkowymi z `~/.config/omarchy/backgrounds/<theme-name>/`.
Dla tego motywu miejscem dodatkowej kolekcji jest zwykle podkatalog `destiny/`.

W obecnym pluginie `omarchy.background` nie ma ustawienia automatycznego
interwału. Rotację okresową można dodać timerem użytkownika wywołującym
właściwe polecenie w sesji graficznej. Przed instalacją sprawdź środowisko
usługi, IPC Omarchy, aktywny motyw i istniejące timery, żeby nie uruchomić
drugiej rotacji. Interwał, zakres kolekcji i ewentualne losowanie ustala użytkownik.
Przy losowaniu warto zachować tasowaną kolejkę bez powtórek aż do jej wyczerpania.

Ten poradnik nie instaluje ani nie włącza timera. Sama rotacja pulpitu powinna
działać lokalnie, bez wywoływania modelu AI przy każdej zmianie obrazu.

## 13. Krótka instrukcja do następnego zadania

> Rozwijasz futurystyczne tapety w `omarchy-destiny-theme`. Przeczytaj ten
> poradnik, manifest i obejrzyj wzorce. Zaprojektuj urządzenie od jego funkcji
> i treści. Użyj autorskiej geometrii 3D, widocznych ścieżek wektorowych i
> wspólnego składu Cairo. Zachowaj logo, typografię i hierarchię. Wszystkie
> widoki muszą mieć ten sam poziom jakości. Postacie wymagają kontroli pozy,
> proporcji, kciuków, połączeń i kontaktu z podłożem. Odróżniaj podstawę naukową
> od fikcji. Sprawdź oba formaty, podpisy oraz detale 1:1. Dostarcz rendery,
> porównania i notatkę zmian; zapisuj nowe uwagi tak, aby następna partia nie
> powtórzyła tych samych błędów.

## 14. Wnioski z produkcji Century / 100

- Opis i geometria muszą pozostać zgodne po zmianie pomysłu. Zmiana transportowca
  orbitalnego w łazik wymaga zmiany funkcji, podpisów oraz źródeł, nie tylko tytułu.
  Aktualny rejestr jest nadrzędny wobec skryptu początkowego brainstormingu.
- Kołnierz ma materiał między otworem a krawędzią. Rozstaw i średnicę śrub
  wyznaczaj z tej szerokości; śruby nie mogą wisieć wewnątrz otworu.
- Szwy i opaski dopasowuj do przekroju odlewu. Okrąg na obudowie o przekroju
  zaokrąglonego prostokąta znika wewnątrz powierzchni i tworzy pozorne luki linii.
- Stałe odległości przy profilach naczyń zawodzą na małych częściach. Poziomy
  przejść powinny być proporcjonalne do wysokości, z zachowaniem kolejności.
- Ostatni punkt każdej ścieżki musi przejść tę samą kontrolę zmiany widoczności
  co próbki wewnętrzne. Dopisanie go dopiero po pętli gubi krótki odcinek,
  który właśnie wychodzi zza przeszkody. Century ma osobny exporter i regresję
  `check_export.py`; nie domyka konturów przez rzeczywiste zasłonięcia.
- Otwarty widok serwisowy korzysta z istniejącego modelu po zdjęciu pokrywy.
  Wnętrze trzeba rzeczywiście zbudować; podpis COVER REMOVED musi odpowiadać
  eksportowi. Kąt od spodu bywa potrzebny dla rolek, sond i powierzchni roboczych.
- Powtarzalność sprawdzaj na wszystkich kołach, napędach i zawiasach. Jedna
  dopracowana część obok uproszczonych odpowiedników wygląda jak błąd montażu.
- Zmniejszona miniatura wystarcza do oceny sylwety i hierarchii, ale nie cienkich
  żeber ani napisów. Audyt Century pracuje na obu natywnych rozdzielczościach,
  a przegląd wizualny łączy arkusze kontaktowe z wybranymi zbliżeniami 1:1.
- Galeria HTML i źródła trafiają do tej samej lokalnej paczki. Pełny ekran należy
  testować obrazem: poprawne zdarzenie API nie gwarantuje poprawnej kolejności
  warstw. Pełnoekranowy kontener wewnątrz dialogu utrzymuje tapetę i sterowanie razem.

Katalog, kod i ścieżki nowej serii opisuje [instrukcja Century](century/README.pl.md).

## 15. Dodatkowa warstwa narracji — uwagi po obejrzeniu setki

Użytkownik zaakceptował bazę Century, ale wskazał niedostatek detali, wykresów,
faktoidów i ostrzejszego humoru względem pierwotnych wzorców. Sama szczegółowa
maszyna z dwoma widokami podzespołów nie kończy kompozycji.

- Dodaj dopasowany do konkretnego urządzenia diagram: fizyczną zależność,
  sekwencję operacji, schemat procesu albo fikcyjny dziennik serwisowy.
- Krzywa ma wynikać z jawnego równania lub opisanych danych. Jednostki,
  normalizację i założenia umieść obok; fikcyjne liczby oznacz na samej tapecie.
- Faktoid nie musi być liczbą. Może wyjaśniać, co sensor naprawdę mierzy,
  jak działa mechanizm albo gdzie kończy się obietnica marketingowa.
- Humor powinien mieć konkretny cel: ludzkie wymówki, biurokracja, zebrania,
  brak cierpliwości. Krótka uwaga serwisowa bywa lepsza od długiej zabawnej legendy.
- Drobne elementy 3D muszą być widoczne: dobierz kąt lub zdejmij rzeczywistą
  osłonę w widoku serwisowym. Nie dodawaj śrub ukrytych pod pełną bryłą.
- Bogatszy panel nie usprawiedliwia kolizji. Kompaktowy format potrzebuje
  własnego miejsca na diagramy; nie ściskaj szerokiej kompozycji mechanicznie.

Pierwsza [dopracowana dziesiątka](century/REFINED-TEN.pl.md) zachowuje przed/po,
źródła i granice interpretacji danych. Obie partie zostały później zaakceptowane; dalszy próg jakości pozostaje osobną decyzją użytkownika.


## 16. Selekcja Century po przeglądzie stu pomysłów

Czytaj `docs/century/CURATION.pl.md` i pola `curation` w `catalog.json`. Z oryginalnej setki zachowujemy 20; pozostałe 80 odrzucono na prośbę użytkownika i pozostawiono wyłącznie jako archiwum. Nie proponuj ich ponownie pod inną nazwą ani nie uruchamiaj dla nich automatycznego dopracowywania bez wyraźnej prośby. Status techniczny pliku (np. ready-for-review) nie unieważnia decyzji kuratorskiej. Obie dopracowane dziesiątki są zaakceptowane. Wspólny rejestr 34 gotowych plansz i 10 kolejnych pomysłów to `docs/collection/catalog.json`; próg jakości w `docs/collection/quality-ranking.json` jest propozycją i nie zmienia przynależności do kolekcji bez akceptacji użytkownika. Kolejne pomysły mają wnosić nową funkcję, sylwetkę i historię, a nie sam wzrost liczby detali.

## 17. Redesign po wspólnym rankingu jakości

[Przegląd dwunastu zmian](collection/QUALITY-REDESIGN.md) rozwija 12 plansz poniżej
proponowanego progu. Użytkownik zlecił redesign; nie oznacza to automatycznej
akceptacji nowych wersji ani usunięcia ich z kolekcji. Ranking opisuje wersje
sprzed zmian i trzeba to wyraźnie pokazać, gdy galeria otwiera aktualne mastery.

- Najpierw zmieniaj architekturę urządzenia: sylwetę, podparcie, mechanizm,
  dostęp serwisowy i punkt zainteresowania. Nakładka ze śrubami nie naprawia
  ogólnej bryły. Boczne widoki muszą pokazywać rzeczywiste części tej bryły.
- W kit `tube()` zapisuje środkową linię przewodu, nawet gdy przekrój 3D jest
  gruby. Zakrzywione podpory konstrukcyjne potrzebują siatki z konturem,
  inaczej na planszy znowu wyglądają jak przewody.
- Wysokość osłony nad manekinem wyznaczaj z obwiedni głowy po transformacji,
  nie z przybliżonego Z. Audyt napisów nie wykryje kolizji głowy z osłoną.
- Widok serwisowy warto pokazać od strony działania i zdjąć rzeczywistą
  osłonę. Kamera patrząca na plecy bogatego mechanizmu daje nadal pusty panel.
- Gdy wyjaśniasz ruch, diagram ma używać tych samych współrzędnych i stanów
  co model. Sprawdzone stany krańcowe nie oznaczają pełnej walidacji ruchu.
- Nie zamieniaj błędnych danych w inne wymyślone dane. Aroma Organ pokazuje
  teraz program zaworów i tor dozowania, jawnie ilustracyjne, zamiast macierzy
  rzekomej odpowiedzi receptorów na nazwany zapach.

## 18. Wspólny skład kolekcji 34 plansz

Wszystkie zachowane plansze korzystają z `tools/collection_layout.py`:
Field Notes są obowiązkowe także na czternastu pierwotnych projektach.
Ich dawne parametry przeniesiono bez zmian do `original_field_notes.json`;
notatka wyjaśnia urządzenie, a trzy podpisane etapy porządkują jego działanie.
Krótki żart pozostaje osobną linią, nie częścią danych pomiarowych.

- Aktualna korekta „triptych” zastępuje wcześniejsze pomijanie B/C w 16:9.
  **Każda plansza, w obu formatach, ma pełne trzy kolumny.** Lewa: detal B,
  diagram lub wykres, metryczka. Środek: podpis A nad dominującym rysunkiem,
  dyskretna puenta na dole. Prawa: NCR w rogu, detal C, diagram lub wykres,
  Field Notes i osobna, mniejsza sygnatura Omarchy.
- W obu formatach szerokość logiczna to 2560 jednostek; wysokość 1080 lub
  1440. Nie rozciągaj geometrii. Dodatkowa wysokość rozsuwa sekcje pionowo,
  zachowując rozmiary typografii. `tools/triptych.py` określa pola i diagramy.
- Field Notes: `W−670, H−264`, szerokość 430. Emblemat ma osobne pole:
  środek `W−133, H−158`, promień 78. Nie przywracaj ogromnego pierścienia
  obok małej tabelki ani notatek wiszących między rysunkiem a znakiem.
- Unikalny podpis A: `W/2, 88`, poza transformacją głównego rysunku.
  Puenta: dokładnie `W/2, H−84`, neutralna biel, alfa 0.40, rozmiar 6.3,
  niewielki tracking. To Easter egg, nie kolejny nagłówek ani złoty akcent.
- B/C mają wspólną typografię; wysokość podpisu wynika z obrysu konkretnego
  rysunku (sekcja 26), a nie ze wspólnej linii pod pustą obwiednią.
  Wykresy są osobnymi sekcjami pod detalami. Nowe diagramy opisują konkretny
  przepływ energii, materiału, sygnału lub decyzji; nie dodawaj losowych
  przebiegów udających pomiary. Podpisy nie mogą leżeć na przewodach.
- Legenda pozostaje przy dolnej lewej krawędzi. Jej wysokość wynika z treści;
  wspólna dolna linia jest ważniejsza od wymuszania identycznej wysokości bloków.
- Wspólna siatka nie wymusza identycznej skali sylwetek. A dominuje, B/C
  objaśniają konkretne części lub zjawiska, a stopka ma spokojniejszy kontrast.
- Audyt sprawdza dokładnie jeden A/B/C, dwa diagramy, jeden blok Field Notes,
  jedną puentę na osi, odległość notatek od logo, tekst względem geometrii
  oraz oba formaty. Przegląd całości i cropów
  jest nadal konieczny. Stare porównania pozostają zamrożone; aktualizacja
  masterów nie powinna przepisywać historii wcześniejszych redesignów.

### Automatyczna aktualizacja Destiny Wallpapers

Użytkownik zlecił, aby po ukończeniu kolejnych poprawek od razu aktualizować
kolekcję dostępną w Destiny Wallpapers. Po audycie podmieniaj właściwe mastery
i sprawdzaj linki pełnej kolekcji. Skrót aplikacji uruchamia companion app `destiny-wallpapers`, która czyta
wspólny rejestr wszystkich 34 zachowanych tapet. Instalator znajduje się
w `companion/install.py`; po zmianach kodu aplikacji uruchom go ponownie.
Same rendery są czytane bezpośrednio z katalogu projektu. Nie kończ na osobnym katalogu podglądów.
To upoważnienie dotyczy przeglądarki tapet; nie oznacza przełączania aktywnego
motywu ani automatycznego commitu/pusha.


## 19. Unikalna grafika zamiast powtarzalnego schematu

Po korekcie triptych użytkownik odrzucił powtarzany blok dwóch wejść i dwóch
wyjść. Różne podpisy nie czynią z tego różnych ilustracji. Wspólne mogą być
siatka, położenie sekcji, typografia i metryczka; geometria diagramu musi wynikać
z konkretnego urządzenia i wyjaśniać coś innego niż sąsiedni detal lub wykres.

- Każdy panel projektuj osobno: przekrój spoiny, droga optyczna, próbkowanie,
  kontakt z podłożem, mechanizm zapadki, geometria sterowania lub zapis zdarzeń.
- Nie zastępuj jednego szablonu kilkoma losowo przydzielanymi wariantami.
  Po ukryciu napisów i koloru rysunki nadal powinny być rozróżnialne.
- Wspólne helpery mogą rysować strzałki i kreski, ale nie całą topologię panelu.
  `tools/subject_diagrams.py` ma 35 osobnych rysunków dla 34 tapet; Tether ma dwa.
- Nowe przekroje pomocnicze są koncepcyjne, nie zwalidowaną dokumentacją
  produkcyjną. Sekwencje demonstracyjne i fikcyjne rekordy oznaczaj na planszy.
- Obejrzyj osobny arkusz samych fragmentów, następnie pełne tapety w obu
  formatach. Poprawne testy napisów nie wykrywają monotonii wizualnej.

## 20. Schemat też ma język retrofuturyzmu

Po obejrzeniu indywidualnych diagramów użytkownik zaakceptował ich schematyczną,
nieprzestrzenną konwencję, ale odrzucił nadmiar kantów. Dla tych pomocniczych
miniatur świadomie projektowana grafika 2D jest dopuszczona. Nie oznacza to
powrotu do płaskich uproszczeń głównych maszyn i bocznych widoków sprzętu.

- Obudowy i odlewy mają promienie, miękkie barki, ranty i kołnierze. Przewody
  prowadź łukami o ciągłych stycznych. Cienka druga krawędź może pokazać rant;
  nie dokładaj tej samej ramki wszystkim ilustracjom.
- Sprężyna mechaniczna ma zwoje, nie zygzak rezystora. W sekwencji zachowaj
  liczbę zwojów, średnicę i punkty mocowania; zmienia się skok sprężyny.
- Miękkie materiały potrzebują odpowiednich konturów: poduszki, skarpety,
  korzenie, fragment korala. Płat nośny powinien mieć płynny profil, a linki
  muszą kończyć się na jego obróconej powierzchni.
- Nie zaokrąglaj automatycznie wszystkich linii. Promienie optyczne, płaszczyzny,
  próbki sygnału, zęby zapadek, rowek spoiny i powierzchnie styku zachowują
  geometrię potrzebną do wyjaśnienia działania. Retro nie unieważnia mechaniki.
- Używaj jawnie wybranych promieni konkretnych części, nie globalnego filtra
  wygładzającego bitmapę. Zachowaj napisy, treść, punkty połączeń i odrębność
  kompozycji. Obejrzyj miniatury i pełne rendery w obu formatach.

Źródło tej korekty: `tools/subject_diagrams.py`, `RETRO_REFINED`. Przegląd
`concepts/century/retro-diagrams/` porównuje nowe fragmenty z poprzednią
indywidualną wersją. Starsze porównanie `individual-diagrams/` jest zamrożone.

## 21. Jedna konwencja podpisów i daty wejścia do służby

Użytkownik wskazał niespójność między oryginalną czternastką i dwudziestką
Century: osobny wyśrodkowany tekst `OBLIQUE`, `SAME HARDWARE` lub `SERVICE VIEW`
wyglądał jak przeoczenie. Wzorzec to podpis **B / HALL PLAN** z informacją
`12 000 SEATS / EVERY ONE SEES DEPTH` bezpośrednio pod nazwą.

- Wszystkie podpisy B/C korzystają z `Sheet.view_label` wraz z argumentem
  `scale`, który jest również miejscem na treściwy opis części lub jej funkcji.
  Podtytuł zaczyna się pod nazwą, nie pod literą, i ma bazę 14 jednostek niżej.
  Nie składaj drugiego, niezależnie wyśrodkowanego bloku pod widokiem.
- Century przechowuje autorskie `view_B_note` i `view_C_note` w rejestrze.
  Każda z 40 notatek musi odpowiadać pokazanym częściom modelu. Nie zastępuj
  ich domyślnym opisem kąta kamery lub zapewnieniem, że to ten sam sprzęt.
- Gdy pominięto element dla czytelności, nazwij go: np. `SADDLE OMITTED`
  albo `BOGIE OMITTED`, po czym wskaż odsłonięty mechanizm. Nie każda pominięta
  część jest pokrywą; sprawdź metadane eksportu.
- Przy `PROJECTED FIRST SERVICE` pozostaje oryginalny rok. Dopisek
  `/ SPECULATIVE` występował tylko w generatorze Century i został usunięty
  dla spójności. Nie oznaczał różnicy w dojrzałości projektów; cała kolekcja
  nadal przedstawia fikcyjne urządzenia i przewidywane daty.
- Audyt Century wymaga dwóch autorskich podtytułów, ich wyrównania z nazwami,
  wspólnego odstępu oraz braku dawnych ogólnych podpisów i dopisku do roku.
  Obowiązuje to w obu formatach, zanim mastery trafią do Destiny Wallpapers.

## 22. Jedna nazwa każdego bocznego widoku

Po ujednoliceniu podpisów użytkownik wskazał kolejny duplikat: nagłówek nad
ilustracją i podpis B/C pod nią. W Greener `NEIGHBOURHOOD / YEAR 06` powtarzało
`THE STREET, YEAR SIX`; Century powtarzało pełną nazwę urządzenia nad prawym
detalem oraz w metryczce, z dodatkowym wierszem programu badawczego.

- Nazwa bocznej ilustracji należy do podpisu B/C pod nią. Nie dodawaj kolejnego
  tytułu nad rysunkiem, również innymi słowami, w innym języku lub skrócie.
- Pełny tytuł tapety występuje raz, w dolnej lewej metryczce. Osobne nazwy A/B/C
  opisują konkretne widoki. Audyt wspólnego składu kontroluje pojedynczy tytuł.
- Numery posesji, oznaczenia części, nazwy strumieni, osie i nagłówki zbiorów
  danych zostają, gdy niosą potrzebną informację. To nie są dodatkowe tytuły
  całej ilustracji. Oceniaj znaczenie, nie usuwaj automatycznie każdego tekstu
  nad dowolną geometrią.
- Korekta usunęła nagłówki z dwudziestu Century oraz siedmiu paneli oryginalnych:
  Greener C, Sky Racer C, Cortical Mesh B/C, Truth Lamp B, Organ Foundry C,
  Proxy C. Nie skalowano rysunków w celu zapełnienia odzyskanego whitespace.

## 23. Czytelność po skalowaniu i widok od strony mechanizmu

Użytkownik wskazał zbyt małe napisy, niedopracowane schematy oraz prawą listwę
Quiet Stair oglądaną od pustej strony. Korekta obejmuje całą kolekcję 34 tapet:

- Minimalny podstawowy stopień tekstu to **7 jednostek planszy, czyli 14 pikseli
  w pliku 5120 px**. Licz go po wszystkich transformacjach, również dopasowaniu
  bocznego panelu. Indeksy dolne/górne zachowują proporcję względem liter.
  `Sheet.readable_size` jest wspólne dla rysowania, pomiaru, łamania i audytu.
- Alfa tekstu co najmniej 0.60; hierarchię tworzą rozmiar, pozycja, treść i odstępy.
  Nie uzyskuj dyskrecji przez nieczytelnie małą czcionkę. Ta korekta zastępuje
  wcześniejsze niższe wartości puenty i podpisów z sekcji 18.
- Nie pomniejszaj fontu, aby naprawić kolizję. Przesuń etykietę, odnośnik,
  oznaczenie osi albo popraw łamanie. Audyt musi mierzyć faktycznie narysowaną
  czcionkę, nie dawny rozmiar sprzed ograniczenia. Raport przechowuje `font_px`.
- Więcej detali wymaga odpowiedniej kamery: Quiet Stair C pokazuje stronę
  styków, z rzeczywiście pominiętą elastomerową osłoną tego samego modelu.
  Obrót w płaszczyźnie prezentuje długą listwę po przekątnej. Widoczne są
  styki, podatne listki, mocowania, przewód powrotny i uszczelnione wyjście.
- Fusion Transport C dostał większy widok osiowy pierścienia załogi, zamiast
  małego obiektu w rozległym pustym polu. Skala zależy od widocznej geometrii,
  a nie starej obwiedni wspólnej dla wszystkich widoków.
- Schematy Seam Surgeon, Plant Alibi, Quiet Stair i Volumetric Stage mają
  własne opracowane części: stopkę sondy, warstwy donicy, korpus zapadki,
  podstawę przyrządu. Nie zaokrąglaj kierunków wiązek ani płaszczyzn adresowania.
- Puenta Quiet Stair celowo odnosi się do claudyzmu „load-bearing”:
  `CLAUDE CALLED THIS LABEL LOAD-BEARING. THE LATCH DISAGREES.`
  To żart o podpisie, nie parametry obciążenia ani certyfikacja mechanizmu.

Przegląd `concepts/century/readable-retro/` zachowuje rzeczywiste wcześniejsze
mastery, sześć porównań fragmentów oraz przykłady typografii w skali natywnej.

## 24. Jedna puenta pod główną ilustracją

Luźne adnotacje na dole środkowej kolumny konkurowały z właściwą puentą.
W Truth Lamp były to dwie linie o ludzkiej rodzinie; podobne dopiski zostały
w Proxy i Quantum Simulator, a wszystkie 20 Century miały tam kod modelu
z nazwą dziedziny.

- Środkowa stopka zawiera wyłącznie wspólną puentę. Nie dodawaj nad nią
  swobodnego opisu sceny, kodu modelu, wariantu widoku ani drugiego żartu.
- Takie informacje należą do Field Notes: pod tabelą parametrów, oddzielone
  delikatną linią, wyrównane do lewej. Zachowuj ich treść i czytelny rozmiar.
- `collection_layout.MAIN_CONTEXT` przechowuje przeniesione adnotacje
  pierwotnych plansz. Century pobiera kod modelu i dziedzinę ze swojego wpisu.
  `field_notes` składa je wspólnie; audyt wymaga pojedynczego wystąpienia
  we właściwej prawej kolumnie, w obu formatach.
- Nie przenoś opisów konkretnych części połączonych odnośnikiem z maszyną,
  wymiarów i oznaczeń na samym sprzęcie. To inna funkcja niż podpis sceny.
- Przejrzano wszystkie 34 plansze; przesunięcia dotyczą 23. Porównanie
  `concepts/century/quiet-footer/` zachowuje poprzedni stan. Słowa i wartości
  pozostają te same; rysunki urządzeń nie zmieniły geometrii.

## 25. Pionowa hierarchia bocznych kolumn

Podpis B/C musi być odczytywany razem z ilustracją, nie jako wstęp do wykresu
poniżej. Użytkownik wskazał ten problem na Quiet Stair; poprawka jest wspólna
dla wszystkich 34 plansz i obu formatów.

- Boczne ilustracje przesunięto o 44 jednostki w górę, zachowując skalę.
  B/C mają bazę `411 + extra*0.35`; podtytuł nadal należy do tego samego podpisu.
  Odstęp ilustracja–podpis jest o 8 jednostek krótszy od poprzedniego układu.
- Linia podziału wprowadza następną sekcję: znajduje się **nad** nagłówkiem
  wykresu, a nie pomiędzy nagłówkiem i jego grafiką. Nie dodawaj kolejnych
  ozdobnych linii lub ogólnych etykiet, aby symulować strukturę.
- `triptych.diagram_y` wyznacza lewy diagram na podstawie faktycznej wysokości
  metryczki. Zostawia co najmniej 40 jednostek przed jej górną linią. Długie
  legendy potrzebują wcześniej położonego diagramu; krótkie mogą dać mu
  więcej miejsca w środku kolumny. Nie zmniejszaj przez to czcionek lub rysunków.
- Prawy diagram zachowuje osobny margines przed Field Notes. Starsze wykresy
  dostają własną linię wprowadzającą, poza ich istniejącymi nagłówkami.
- `register_section` zapisuje krawędzie sekcji. Audyt obu formatów wymaga
  co najmniej 30 jednostek od końca podpisu B/C do kolejnego podziału oraz
  co najmniej 38 jednostek między diagramem a metryczką / Field Notes.
  Margines nominalny 40 dopuszcza drobne różnice zasięgu glifów.
- W Century metryczka jest składana przed diagramami, aby jej rzeczywista
  wysokość była znana. Nie szacuj jej z liczby znaków lub ogólnej liczby wierszy.

Przegląd `concepts/century/vertical-rhythm/` zachowuje poprzednie mastery,
porównania bocznych kolumn i pomiary wszystkich 136 bocznych kolumn w 68 plikach.

## 26. Podpis należy do rzeczywistego obrysu, nie do pola

Poprawka pionowych odstępów z sekcji 25 nie wystarczyła. Presence Rig B miał
krótką kasetę rolek wysoko w polu, a podpis nadal na wspólnej, odległej bazie.
Audyt przechodził, bo mierzył odstęp do następnej sekcji, lecz nie do rysunku.

- Zastępuj stały poziom B/C pomiarem faktycznego tuszu wektorowego.
  `measured_illustration` zapisuje obrys Cairo wraz z adnotacjami części;
  nie liczy pustego pola docelowego jako ilustracji.
- Górna krawędź ramki B/C jest 19 jednostek poniżej obrysu (baza +30).
  Zachowaj rozmiar i położenie rysunku. Krótszy rysunek ma wyżej swój podpis.
- Następny blok musi być co najmniej dwukrotnie dalej od końca podpisu
  niż podpis od własnego obrysu. Pomiar obejmuje każdą ze 136 kolumn
  w obu formatach, nie tylko planszę wskazaną przez użytkownika.
- Jawny pomiar glifów działa również w audycie renderowanym bez tekstu.
  Sprawdź, czy render i raport używają tych samych współrzędnych.
- Linie osiowe i bazy konstrukcyjne też należą do pomiaru. Nie pozwalaj,
  aby wychodziły daleko poza sprzęt i odsuwały podpis: Fusion C i Aroma B
  mają teraz zasięg wyznaczony przez `fitted_size` geometrii + 8 jednostek.
- Obejrzyj arkusze wszystkich bocznych grup i większe zbliżenia odstających
  przykładów. Samo PASS kontroli kolizji nie jest oceną hierarchii wizualnej.

Porównanie `concepts/century/attached-captions/` zachowuje poprzednią korektę
`vertical-rhythm` jako wersję przed; nie przepisuj jej archiwum.

## 27. Rozszerzenie do 42 i kontrola połączeń

Osiem nowych urządzeń opisano w `docs/collection/EXTENSION-42.pl.md`.
Nie wracaj do 80 odrzuconych koncepcji. Numery katalogowe zachowują historię,
a o członkostwie i liczbie 42 decyduje `docs/collection/catalog.json`.

- Liczba części modelu nie świadczy o widocznym detalu: osłona może zasłonić
  całą sprężynę. Obejrzyj B/C od strony mechanizmu i otwórz korpus świadomie.
- Sprawdź wszystkie punkty mocowania: koniec podpory musi dochodzić do odlewu,
  napinacz do wspornika, trunnion do jarzma. Nie uznawaj pozornego styku
  w projekcji za połączenie w modelu.
- Grupa podzespołu powinna obejmować transformację części **i przewodów**.
  `group()` wewnątrz `at()` może zachować stare współrzędne przewodu, ponieważ
  transformacja wymienia jego zapis. Obejmij `at()` zewnętrzną grupą.
- Przewód należący do całej maszyny nie powinien wydłużać obwiedni odłączonej
  kasety serwisowej. Rozdziel pigtail kasety i dalszą wiązkę głównej sceny.
- Zestaw dostarczany w Git i aplikacja mają mieć tę samą liczbę pozycji.
  Użyj `release_collection.py`; sprawdź też aplikację na świeżym klonie bez
  katalogu `concepts/`, a nie tylko na stanowisku autora.

## 28. Macierz formatów i czytelność na każdym ekranie

Ustalenia z 27 września 2026. Każda z 42 plansz ma osobny, skomponowany zestaw
dla każdego popularnego ekranu poziomego: 16:9, 16:10, 3:2, 4:3, 21:9 (64:27
oraz 43:18/12:5) i 32:9, od klasy 1080p do 5K/8K. Pion jest poza zakresem.
Lista, rozmiary i sumy kontrolne: `docs/collection/profiles.json`.

- **Próg czcionki**: najmniejszy tekst w pliku natywnym ma co najmniej
  `max(11, 14 × wysokość / 2880)` pikseli. 11 px to najmniejszy standardowy
  tekst interfejsu przy 96 DPI (8 pt); wersaliki Nimbus Sans mają wtedy około
  8 px wysokości, czyli jeszcze odrębne kreski bez hintingu. Drugi człon
  utrzymuje fizyczną (kątową) wielkość zaakceptowanego mastera 5K na ekranach
  o podobnej gęstości. Audyt mierzy faktycznie narysowany rozmiar.
- **Mniejszy ekran = zwięźlejsza kompozycja, nie mniejszy tekst.** Rysunki są
  rasteryzowane raz, w docelowej skali; `Sheet.readable_size` powiększa tekst
  już przy łamaniu i pomiarze. Kolejność ustępowania: diagramy, potem C,
  potem Field Notes; legenda traci najpierw zdania ENABLED BY, w ostateczności
  całą sekcję. A, legenda, puenta, emblemat i numer arkusza zostają zawsze.
- Szablony: `triptych` (trzy kolumny mastera, przeliczone na inną wysokość),
  `duo` (ekrany ~1920 px: rysunek w prawo, lewa kolumna z B i legendą),
  `stacked` (4:3: rysunek u góry, pas dossier pod nim), `panorama` (32:9:
  pięć kolumn). Bloki przesuwa się tylko o całe piksele; ich tusz nie może
  się stykać (maska kolizji), a słabe linie konstrukcyjne widoku A kończą się
  przed innymi blokami i ramką. B i C pochodzą z drugiego, wyższego przebiegu,
  aby przy większym tekście pozostały większe od swoich podpisów.
- Poprawki typograficzne dla powiększonego tekstu są warunkowe (`layer_mode`,
  `Sheet.type_growth`): nie zmieniają ani jednego bajtu masterów 5K, co
  `tools/render_wallpaper_sets.py` sprawdza względem
  `docs/collection/native-masters.json`.
- Kontrola: każdy plik przechodzi audyt w pikselach końcowych (tekst na
  geometrii, tekst na tekście, obcięte etykiety, jeden A/B/C na pokazany
  widok, próg czcionki). Arkusze przeglądowe i wycinki 1:1 najmniejszego
  tekstu: `tools/aspect_matrix_review.py` → `concepts/aspect-matrix/`.
- Dostarczanie (decyzje właściciela z 27 września): w repozytorium jest tylko
  zestaw zaakceptowanych masterów 16:9 5120×2880 w `backgrounds/`; pozostałe
  zestawy to archiwa GitHub Release (`tools/package_wallpaper_profiles.py`,
  tag w `tools/wallpaper_profiles.py`). Wysyłane pliki (ten zestaw i archiwa)
  to stratny WebP q90, method 6 — dla szybkiej instalacji. Renderujemy
  i audytujemy bezstratnie; bezstratny master musi być identyczny bajtowo,
  przekodowana jest dopiero kopia wysyłkowa. Przy zbliżeniu 3× tekst i cienkie
  linie są bez zmian, ziarno jest delikatnie gładsze. Ta decyzja zastępuje
  regułę „tylko bezstratnie” z sekcji 9 dla plików dostarczanych, nie dla
  masterów.   companion pobiera właściwy i weryfikuje SHA-256.

## 29. Wymiana ośmiu plansz i nowa historia Proxy (27 września 2026)

Na prośbę właściciela z kolekcji wyszły Compliment Mill, Advice Filter,
Meeting Buoy, Queue Garden, Plant Alibi, Sock Oracle, Truth Lamp i Greener.
Weszło osiem plansz p(bloom): Reef Nursery, Clear Sight, Stellarator Hearth,
Green Forge, Sun Still, First Light, Crater Ear i Wind Freighter (pliki
`bNN-slug.webp`, renderer `tools/century/bloom/render.py`, rodzina `bloom`
w `aspect_layout.collection()`). Kolekcja nadal liczy 42; o składzie decyduje
`docs/collection/catalog.json`, a wycofane numery NCR nie wracają.
Greener i Truth Lamp zostają w `order.ORDER`, żeby pozostałe oryginały nie
zmieniły pozycji, id ani nazw plików.

- (Nieaktualne od sekcji 30: dziesięć teł.) Tła rozłożono równo: każde z 13 ma 3 albo 4 plansze. Sąsiedzi w kolejności,
  także ostatnia i pierwsza plansza (rotacja się zawija), nie dzielą tła ani
  sąsiedniego odcienia; grafit sąsiaduje tylko z tłami nasyconymi. Zmieniono
  tylko dwie istniejące plansze: Presence Rig (grafit → umber) i Spin Table
  (umber → moss).
- Proxy nie jest już żartem. To przewodnik dla niewidomych i słabowidzących
  biegaczy: biegnie obok na krótkiej linie, podaje tempo, ostrzega przed
  krawężnikami i zakrętami. Rysunek się nie zmienił; zmieniły się legenda,
  odnośniki, podpisy B/C, oba diagramy, Field Notes i puenta. Liczby są
  spójne: 10 km w około 60 min, 3 s wyprzedzenia to około 8 m przy
  6 min/km, czujniki widzą 20 m. Ton jak w `BLOOM-TEN.md`: prosto, konkretnie,
  bez żartów. Brak głowy nadal oznacza NONE FITTED.
- Po takiej zmianie wydane archiwa macierzy formatów zawierają stary zestaw.
  Manifest `profiles.json` publikuje wtedy tylko zestaw dołączony do motywu
  (`release.pending` wymienia wycofane profile), dopóki macierz nie zostanie
  przerenderowana i spakowana.

## 30. Trzy poziomy tła: Muted / Default / Vivid (27 września 2026)

Każda plansza istnieje w trzech intensywnościach tła. Zmienia się wyłącznie
tło (gradient, centralna poświata, winieta); linie, tekst i akcenty są
identyczne. Default to projekt i musi pozostać bajtowo identyczny.

- Dziesięć teł (decyzja właściciela 27 września): crimson, copper, saffron,
  emerald, teal, cobalt, ink, violet, berry, graphite. Każde jest zdefiniowane
  zmierzonym, wyrenderowanym tłem w OKLCH (`palettes.json` → `targets_oklch`,
  mediana tła planszy 1080p) i rozwiązane do parametrów HLS z dokładnością
  ΔE ≤ 1 (×100). Najbliższa para crimson–berry 6,4, pozostałe ≥ 7,6. Usunięte
  nazwy mają aliasy w `old_to_new`. Na plansze: 4–5 na tło (saffron 4),
  sąsiedzi (także 42 → 1) nie mają tła bliższego niż ΔE 10.
- Poziomy: dla każdego tła Muted i Vivid są w tej samej odległości d od
  Default (ΔE OKLab na wyrenderowanym tle). d wynika z koloru tła: Muted to
  połowa chromy przy tej samej jasności; Vivid dodaje chromę (jasność tylko
  w razie potrzeby) do tego samego d. Grafit robi krok 0,02 głównie jasnością
  i zostaje szary. Dzięki temu tła nasycone zmieniają się bardziej, spokojne
  mniej, a każde zachowuje tożsamość na każdym poziomie. Wspólny krok dla
  wszystkich (5,5) odrzucono: Muted szarzał, a Vivid zamieniał grafit w granat.
- Krok nie może kosztować czytelności: biały tekst (alfa 0,60) i akcenty
  zachowują 4,5:1 / 3:1, a gdzie Default jest poniżej, nie tracą kontrastu.
  Tylko na saffron właściciel zwolnił limit białego tekstu; akcenty nadal
  3:1. Teal jest ciemny (L 0,232, C 0,040), bo jaśniejszy morski nie daje
  4,5:1 dla białego tekstu, a wciąż musi być ≥ ΔE 6 od grafitu i ink; ma też
  cichszą poświatę (`default_glow`: 0,10 / 0,28). Gdy limit zatrzymuje Vivid
  przed d, Muted robi ten sam krótszy krok.
- Saffron ma jasne akcenty bright_cyan / bright_green: większość akcentowych
  podpisów leży na ciemniejszych, winietowanych brzegach, gdzie ciemny tusz
  ma około 1,5:1. Nie dodawaj podkładów ani cieni pod białym tekstem.
- Audyt (`aspect_layout.audit`, `verify_wallpaper_layout.py --level`) mierzy
  każdy podpis na końcowych pikselach: jego kolor i alfę na każdym pikselu
  tła pod nim (liczy się najgorszy), i porównuje z tym samym podpisem na tle Default.
- Przegląd: `render_wallpaper_sets.py --profile 16x9-1080p --level muted
  --level default --level vivid --out concepts/ground-levels/sets`, potem
  `tools/ground_level_review.py`. Pełna macierz: `render_wallpaper_sets.py
  --level muted --level default --level vivid`, potem pakowanie.
