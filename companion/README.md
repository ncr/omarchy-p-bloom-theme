# p(bloom) Wallpapers — companion app

A full-screen browser for the 42 p(bloom) wallpapers that also keeps your desktop on the set made
for your monitors.

The theme installed through Omarchy's menu is data only: it cannot install or
launch this app by itself. Explicitly run the companion installer once:

```sh
python3 companion/install.py
```

The gallery is a small GTK 4 window (python-gobject, GTK 4 and the WebP loader are part of Omarchy).

The installer announces what it installs, adds **p(bloom) Wallpapers** to the
application menu, and opens it automatically in a graphical session. Use
`--no-launch` to install without opening it. A user service keeps desktop renders matched to your monitors. No sudo or
compositor configuration changes are involved.

## Automatic setup

The desktop service automatically selects and applies the optimal wallpaper
set on installation, login and monitor changes, without opening the gallery.
It checks for changes every 10 seconds. Opening the app also opens the gallery. There is no first-run dialog. Selection considers all connected
monitors: avoid enlargement, minimize cropping, then prefer smaller files.

A short notification appears on the first selection or when the chosen set
changes. It states the resolution; clicking it opens settings. Notifications confirm desktop updates only. With another theme active,
the service waits for p(bloom) and leaves that theme unchanged.
Unchanged launches do not repeat the notification.

Settings are available through **Wallpaper settings** in the application's
context menu, the gallery's **S** key, or `p-bloom-wallpapers --configure`.
They are a menu in the middle of the gallery's window, over the dimmed
wallpaper, set like the gallery's strip, with nothing to choose: the
wallpapers follow the **optimal set** for the connected monitors (one set for
all of them, as Omarchy shows one wallpaper on every monitor). The menu shows
the monitors, the set in use and that set's packs, one per **intensity**
(Muted, Default, Vivid: how strong the background colour is), installed or not.
Its one action, **Download optimal** (Enter), fetches the missing packs in the
background; the gallery's ↑ ↓ then switch intensity at once. Escape or S
closes the menu. Downloaded packs of the optimal set are kept when older sets
are cleaned up. (Sets for each monitor on its own will follow when Omarchy can
show a wallpaper per monitor.)

In the gallery, ↑ ↓ show the same wallpapers at another intensity without
changing anything; Enter makes the one on screen the desktop's, at that
intensity, which is then remembered.

When a change needs a set that is not installed yet, the gallery dims and shows
the download in its middle: the emblem from the sheets' corner, turning, its
Pollen ring filling with the download, the percentage inside and the set and
megabytes below; then it switches to the new set at the same wallpaper.

Without a graphical session (over SSH, for example) `--configure` asks the same
questions in the terminal.

`--show-plan` provides detailed read-only diagnostics. Earlier setup policies
migrate to automatic selection. No monitor detection means no desktop change;
the desktop service keeps watching until real monitors are available.

## Wallpaper sets

Every sheet is composed separately for each common landscape screen, not just
scaled: 16:9, 16:10, 3:2, 4:3, both 21:9 families (64:27 and 43:18/12:5) and
32:9, from 1080p-class to 5K/8K-class (the list and per-set sizes are in
`docs/collection/profiles.json`). Type on every set is at least 11 native
pixels (14 px on 5K 16:9); smaller screens show fewer secondary panels instead
of smaller type.

The theme itself ships ten wallpapers in `backgrounds/`, one for each
background colour (`starter` in `profiles.json`), from the 16:9 5120 × 2880
set, so it works right after `omarchy theme install` and its clone stays
small. The companion downloads the set that best matches your monitors, all
42, file by file. Shipped files are WebP quality 90 (the render pipeline
keeps and audits lossless originals). Every published file is stored
once under its own SHA-256 (`objects_base` in `profiles.json`):
`https://media.jacekbecela.com/p-bloom/<sha256>.webp`. These files never
change; a fixed wallpaper is a new file with a new name. Each file is checked
against its SHA-256 and size as it arrives and retried a few times if the
connection drops. Files the set needs that are already on disk (among the
theme's ten or in another downloaded set) are linked instead of downloaded. The set is
assembled in a staging folder and replaces the installed one only when all 42
files are there, so a failed download changes nothing. Only the Python standard
library is used. Sets are stored in `$XDG_DATA_HOME/p-bloom-wallpapers/sets/`
(default `~/.local/share/`); the three most recently used are kept, so docking
back and forth does not download again.

### Background level

Every set exists at three background levels. Only the background changes
(its gradient, central glow and vignette); lines, type and accents are the
same. **Default** is the design and the level of the theme's own ten.
**Muted** is quieter and a little darker; **Vivid** is more colourful. Both
are separate packs: every resolution has exactly three, Muted, Default and
Vivid, listed under `packs` in `profiles.json`, each a group of 42 files. The
companion downloads only the pack you chose, the same way, into
`sets/<set>-<level>/`, and
refreshes the desktop. Levels are designed so that type never becomes less
legible than in the Default design (`tools/ground_levels.py`). If a level is
not published for a set, that set is shown at Default with a notice; if its
download fails, the set already on the desktop stays and the download is
retried, as below. `--list` prints the current set and level on stderr;
`--show-plan` includes `level` and `requested_level`.

Each downloaded set records a digest of the file list it was built from (`.set-sha256`). After a theme
update that changes some wallpapers, an older set on disk no longer counts as installed; updating it
downloads only the changed files and links the rest from the old copy.

The installed app is a copy of the checkout's `tools/` files. After `omarchy theme update` pulls new app
code, the desktop service and the launcher notice that the copy differs from the checkout it was installed
from, copy the changed files and restart into them; rerunning the installer is needed only after moving the
checkout.

Offline, or if a download or a checksum fails, the desktop keeps the installed
set (before the first download, the theme's ten) and the companion retries
after 15 minutes.
With no monitors detected nothing is downloaded. `--list` never downloads.

Selection is unchanged: all connected monitors are considered, enlargement is
avoided on every one of them, then cropping is minimised, then the smaller
download wins. A set counts as a download in the settings list until it is
installed.

Hyprland's synthetic FALLBACK output is not treated as a physical monitor.
Without monitor detection, the app can browse the default but leaves the
desktop unchanged and retries setup when detection works.

If p(bloom) is active, the app copies the chosen set into Omarchy's staged
backgrounds while preserving custom files and the currently selected sheet.
A user-local `theme-set` hook repeats this selection when p(bloom) is reapplied,
including after an update. The hook can initialize the desktop directly; no prior gallery launch is needed.
Other themes are never activated or modified. The background service tracks monitor changes even when the gallery is closed.

Omarchy currently displays one shared wallpaper on all monitors. Selection
considers the whole monitor arrangement, not a separate profile per output. Other aspect
ratios may crop on the desktop; the viewer always fits the complete sheet.

## Controls

A strip along the bottom edge shows the position and the keys, set like the sheets' own labels; it fades after three seconds without input and comes back on any key or pointer movement. I hides it.

| Key | Action |
|---|---|
| Left / Right | Previous / next, wrapping |
| Up / Down | Browse the same wallpapers at another intensity: Up towards Vivid, Down towards Muted (shown next to the position); settings and desktop stay as they are |
| Enter | Make this wallpaper, at the level shown, the desktop background (p(bloom) must be the active theme); another level is saved as the setting |
| S | Settings menu; after saving, the gallery switches to the new set at the same wallpaper |
| I | Hide or show the strip |
| F | Toggle fullscreen |
| Home / End | First / last |
| Esc / Q | Close |

The local Super+O integration recognizes the unchanged `p-bloom-wallpapers`
window class. This app does not install a global keybinding.

```sh
p-bloom-wallpapers tether
p-bloom-wallpapers 3                  # Collection position, not filename number
p-bloom-wallpapers --configure        # The gallery with its settings open (the optimal set)
p-bloom-wallpapers --show-plan        # JSON; no changes or setup dialog
p-bloom-wallpapers --list             # All 42 chosen files; read-only
p-bloom-wallpapers --monitor DP-1     # Prefer its proportions; still avoid upscaling on all screens
p-bloom-wallpapers --dir /path/to/numbered-images
python3 companion/install.py --uninstall           # add --purge to delete the downloads and settings too
```

Installation is user-local: `~/.local/bin/p-bloom-wallpapers`,
`~/.local/share/p-bloom-wallpapers/`, the application-menu entry and
`~/.config/omarchy/hooks/theme-set.d/p-bloom-wallpapers`. The `p-bloom-wallpapers-desktop.service` user service also runs locally.
Preferences
live under `$XDG_STATE_HOME/p-bloom-wallpapers/setup.json` (default
`~/.local/state/`). Omarchy's own staged files follow its fixed state path.

Keep the checkout in place: the theme's ten wallpapers and the manifest are read from
it. Rerun the installer after moving it. New sets are rendered with
`tools/run_matrix.sh` (all sets, or `tools/run_matrix.sh o02,b13` for a few
sheets in every set), packaged with `tools/package_wallpaper_profiles.py`,
which writes the manifest, and published with
`tools/publish_wallpaper_objects.py`, which uploads only the files that are
not online yet and checks them by downloading them; commit the manifest only
after that. The development viewer (`python3 tools/view_wallpapers.py`) reads live renders,
independently of the packaged sets.

Uninstall stops and removes the desktop service, launcher, menu entry, icons, owned hook and runtime files.
It keeps the theme, the downloaded sets and the settings; `--purge` deletes the sets and settings as well.
Removing the theme with Omarchy (Remove > Theme) removes the app too: once the theme's folder has been gone
for a minute, the desktop service purges the app the same way, disables itself and sends a notification. A custom `--prefix /some/path`
is a staging installation: it installs no hooks or service and launches nothing.
