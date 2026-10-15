# Ciche pętle tapet

Warstwa przeglądarkowa do wszystkich 42 tapet z kolekcji f4a51dd. Oryginały
pozostają nieruchome: lokalne światło oddycha na istniejących liniach i powoli
przechodzi wokół detali. Nie obracamy bitmapowych napisów ani całych urządzeń.
Pełna orbita wokół rzeczywistej geometrii to osobne ujęcie filmu na blogu.

`renderer.js` nie zależy od Astro, Three.js, muzyki ani API Omarchy.
`profiles.json` zawiera osobne położenia i fazy dla 42 plansz. Wszystkie cykle
zamykają się dokładnie po 24 sekundach. Render działa w 24 kl./s, korzysta
z maski faktycznego jasnego tuszu, respektuje wyłączanie ruchu i nie animuje tekstu
w stopce. To ozdobne światło, nie symulacja pracy fikcyjnych urządzeń.

Uruchom z katalogu projektu `python3 -m http.server 8765`, potem otwórz
`http://localhost:8765/tools/ambient/?id=o03`. Wybór tapety i pauza są dostępne
po najechaniu na lewy dolny róg lub klawiaturą. Wpis `id` pochodzi z katalogu.
`window.wallpaper.render(seconds)` pozwala deterministycznie eksportować klatki
bez odtwarzacza, napisów, ujęć reżyserskich ani dźwięku.

Status: przygotowana warstwa i podgląd WWW. Nie zainstalowano jej na pulpicie
ani nie założono nieistniejącego formatu przyszłego Omarchy. Adapter lub format
wideo należy dobrać do rzeczywiście dostępnej obsługi animowanych teł.

Kopia tego samego renderera jest używana w galerii bloga. Sekwencja filmu:
powstawanie rysunku → subtelna pętla tapety → wybrane zbliżenie i orbita 3D.

Eksport bezdźwięcznego MP4 (wymaga Python Playwright i ffmpeg):
`python3 tools/ambient/export.py --id o03 --width 1920 --out concepts/animated-wallpapers/fusion-loop.mp4`.
Przykład ma 24 s, 24 kl./s i 1920×810. Można wybrać dowolny identyfikator z profili
oraz szerokość 5120 dla natywnego 21:9. Źródła 16:9 wymagają osobnego składu;
nie rozciągaj eksportu 21:9.

W filmie na blogu `setAudioLevels({active,bass,mids,highs})` przełącza światło
w wizualizer rzeczywistych pasm utworu. Render tapety używany bez muzyki zachowuje
niezależną pętlę; nie potrzebuje dostępu do mikrofonu ani sieci.
