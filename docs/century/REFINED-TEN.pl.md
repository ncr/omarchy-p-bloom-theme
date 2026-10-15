# Century — dopracowana dziesiątka

Wybrano 10 projektów o różnych sylwetkach, interesującej mechanice i potencjale
narracyjnym. Korekta rozwija zaakceptowaną serię: dodatkowe części należą do
tego samego modelu, wykresy wyjaśniają mechanizm albo jawnie fikcyjny dziennik,
a humor pozostaje częścią dokumentacji urządzenia.

[Galeria przed/po](../../concepts/century/refined-ten/index.html): B przełącza
wersję, strzałki zmieniają tapetę, F pełny ekran, Esc zamyka. Oba formaty natywne.
Oryginalne 20 obrazów zachowano w `concepts/century/refined-ten/before/`.

| Projekt | Dlaczego i co dopracowano | Nowy panel / żart |
|---|---|---|
| 001 Light Sail | Duża lekka konstrukcja; enkodery napinania, przewody, uszczelnienia i zawleczki rolek | Znormalizowane ciśnienie idealnego lustra cos² kąta; Słońce nie obsługuje przesyłek ekspresowych |
| 010 Sock Oracle | Wdzięczna mechanika prania; perforacja bębna, prowadnice i rolki, prawdziwe zdjęcie osłony w C | 100 fikcyjnych skarpet: 84 sparowane, 9 samotnych, 5 zużytych, 2 sporne. Gwarancja nie obejmuje wszechświatów równoległych |
| 030 Advice Filter | Fizyczna przesłona dla społecznego problemu; korby lamelek, podkładki i sprężyny przycisku | Diagram czasowy bufora, prośby i bramki głośnika. Ekspertyza nie omija przycisku |
| 031 Petal Eye | Segmentowane lustro i delikatne nogi; metrologia obrzeża, żebra, wiązki, przegrody optyczne | Pole apertury rośnie jak kwadrat średnicy. Cyfrowy zoom nie powiększa lustra |
| 044 Coral Cradle | Kontrast aparatury z organizmem; czujniki kontaktu, oznaczane gniazda, perforacja i osłony wentylatorów | Fragment → szkółka → rafa. To nie przycisk cofania zmian w oceanie |
| 056 Dune Skimmer | Charakterystyczna sylweta transportowa; identyczne bieżniki wszystkich kół, uszczelnienia, osprzęt cienia i ładunku | Ciśnienie = obciążenie / powierzchnia styku, przy stałym obciążeniu. Napęd na cztery koła nie daje rozsądku |
| 060 Meeting Buoy | Mechanizm i absurd są czytelne od razu; znaczniki masztu, krańcówki, kapsuły mikrofonowe i magistrala | Fikcyjna godzina: 9 min decyzji, 33 min formatu, 18 min następnego spotkania. Flaga dostała zaproszenie na follow-up |
| 087 Neutrino Bell | Dużo warstw prawdziwej aparatury; elektronika odczytu, dystanse, uszczelnienia i odciążenie kabla | Neutrino → oddziaływanie → cząstka naładowana → światło → sensor. Częste dzwonienie każe sprawdzić prąd ciemny |
| 099 Sleep Cocoon | Relacja człowieka i mechaniki; podkładki łożysk, ograniczniki, wiązki, izolatory i pakiet serwisowy | Sekwencja podparcia, odpoczynku i zwolnienia. Człowiek — nie restartować |
| 100 Plant Alibi | Mocny domowy żart; skala sondy, przewody, ściągi przepływomierza, śruby rejestratora | 7 deklaracji podlewania i 2 fikcyjne zdarzenia przepływu. Paprotka żąda reprezentacji prawnej |

## Dane i faktoidy

- [NASA: siła od odbitych fotonów](https://ntrs.nasa.gov/api/citations/20190030798/downloads/20190030798.pdf)
  oraz [zależność cos² kąta dla idealnego odbicia](https://ntrs.nasa.gov/api/citations/19690019483/downloads/19690019483.pdf).
  Wykres Light Sail dotyczy siły normalnej na stałym żaglu przy stałym oświetleniu,
  nie dowolnej trajektorii rzeczywistego statku.
- [NASA: lustra Webba](https://science.nasa.gov/mission/webb/webbs-mirrors/) —
  zasada wspólnego frontu falowego i zbierania światła. Krzywa Petal Eye to
  obliczona geometria A/A0=(D/D0)² przy stałym kształcie i ułamku przesłonięcia.
- [NOAA: odtwarzanie raf](https://www.fisheries.noaa.gov/national/habitat-conservation/restoring-coral-reefs)
  — szkółki i przesadzanie koralowców. Schemat nie podaje wymyślonej skuteczności.
- [IceCube: zasada detekcji](https://icecube.wisc.edu/science/icecube/) — światło
  Czerenkowa od naładowanych produktów oddziaływania. Rysunek nie jest zapisem zdarzenia.
- Dune Skimmer: elementarna definicja średniego nacisku p=F/A. Nie modelujemy
  zapadania ani przyczepności w piasku. Nie wolno odczytywać wykresu jako takich wyników.
- Sock Oracle, Meeting Buoy i Plant Alibi mają jawne etykiety **FICTIONAL LOG**.
  Liczebności są autorskim żartem, a nie badaniem użytkowników.
- Advice Filter i Sleep Cocoon mają **SCRIPTED EXAMPLE / CYCLE**. Diagramy pokazują
  kolejność operacji, nie zmierzoną jakość rozpoznawania mowy ani wyniki medyczne.

Kod: `editorial.py` (treść i wykresy), `refinement_geometry.py` (części 3D),
`refinement_review.py` (porównania). Reprodukcja:

```sh
blender -b --python-exit-code 1 --python tools/century/build.py -- --ids 1,10,30,31,44,56,60,87,99,100 --force --maintenance
python tools/century/render.py --ids 1,10,30,31,44,56,60,87,99,100 --force --maintenance
python tools/century/audit.py --ids 1,10,30,31,44,56,60,87,99,100
python tools/century/refinement_review.py
```
