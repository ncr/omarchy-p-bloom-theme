"""p(bloom) Wallpapers: the gallery.

GTK 4 with python-gobject (both in Omarchy's base), drawn like the sheets themselves: the image fills the screen,
and a 30-unit strip along the bottom edge (units of 1/1080 of the screen height) carries the position and the keys,
set in Nimbus Sans with the sheets' tracking and their boxed letters. The strip fades out after three seconds without
input and comes back on any key or pointer movement.

Keys: Left/Right browse (wrapping), Home/End, Enter makes the wallpaper the desktop background, S opens the settings
menu over the dimmed wallpaper (a menu object from the caller, drawn in this window) and reloads the set when they are
saved, I hides or shows the strip, F toggles fullscreen, Esc or Q closes.
The file on screen is re-read when it changes on disk, so the development viewers see new renders live.
"""
import sys
import threading
import time
from pathlib import Path

import cairo
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gdk, GdkPixbuf, GLib, Gtk  # noqa: E402

NAVY = (9/255, 13/255, 22/255)
ICE = (217/255, 232/255, 1.0)
MUTED = (140/255, 160/255, 192/255)
POLLEN = (245/255, 201/255, 69/255)
BOX = (150/255, 170/255, 200/255)
FACE = 'Nimbus Sans'
CAP = 0.729              # Nimbus Sans cap height, in em
KEYS = ((('←', '→'), 'BROWSE'), (('↑', '↓'), 'INTENSITY'), (('↵',), 'SET AS DESKTOP'), (('S',), 'SETTINGS'), (('I',), 'HIDE'),
        (('F',), 'FULLSCREEN'), (('ESC',), 'CLOSE'))
LEVELS = ('muted', 'default', 'vivid')
IDLE = 3.0               # seconds before the strip fades
FADE = 0.22              # seconds of the fade


def _face(cr, size, bold=False):
    cr.select_font_face(FACE, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)


def _tracked(cr, x, baseline, text, track, draw=True):
    """Set text letter by letter with tracking (em); returns the advance."""
    size = cr.get_font_matrix().xx
    x0 = x
    for i, ch in enumerate(text):
        if draw:
            cr.move_to(x, baseline)
            cr.show_text(ch)
        x += cr.text_extents(ch).x_advance + (track*size if i < len(text)-1 else 0)
    return x - x0


def _arrow(cr, x, cy, length, direction):
    """Path of a horizontal arrow (the face has none): shaft and a 45° head."""
    head = length*0.42
    x0, x1 = (x, x + length) if direction > 0 else (x + length, x)
    cr.move_to(x0, cy)
    cr.line_to(x1, cy)
    cr.move_to(x1 - direction*head, cy - head)
    cr.line_to(x1, cy)
    cr.line_to(x1 - direction*head, cy + head)


def _varrow(cr, cx, y, length, direction):
    """Path of a vertical arrow: shaft and a 45° head (direction 1 = down)."""
    head = length*0.42
    y0, y1 = (y, y + length) if direction > 0 else (y + length, y)
    cr.move_to(cx, y0)
    cr.line_to(cx, y1)
    cr.move_to(cx - head, y1 - direction*head)
    cr.line_to(cx, y1)
    cr.line_to(cx + head, y1 - direction*head)


def keycap_metrics(cr, u, box_band=None):
    """Sizes of the boxed keys at unit u: (font size, box height, inner margin, stroke)."""
    size = 11*u
    _face(cr, size, bold=True)
    cap = cr.text_extents('H').height
    box = round(cap + 2*round(5.5*u))
    if box_band is not None and (box_band - box) % 2:
        box += 1                                           # equal space above and below inside the band
    return size, box, (box - cap)/2, max(1.0, 0.13*size)


def keycap(cr, x, top, key, metrics, draw=True):
    """One boxed key with its top-left corner at (x, top); returns its width. Letters are centred by ink; arrows are
    strokes with the caps' stem weight, centred by their stroke extents (miter tips included)."""
    size, box, pad, stroke = metrics
    _face(cr, size, bold=True)
    drawn = key in ('←', '→', '↑', '↓', '↵')
    ext = None if drawn else cr.text_extents(key)
    w = box if drawn else max(box, round(ext.width + 2*pad))
    if not draw:
        return w
    mid = top + box/2
    cr.set_source_rgba(*BOX, 0.95)
    cr.set_line_width(1)
    cr.rectangle(x + 0.5, top + 0.5, w - 1, box - 1)
    cr.stroke()
    cr.set_source_rgb(*ICE)
    if drawn:
        cr.set_line_width(stroke)
        cr.set_line_cap(cairo.LINE_CAP_BUTT)
        cr.set_line_join(cairo.LINE_JOIN_MITER)
        length = box - 2*pad

        def shape(dx=0.0, dy=0.0):
            cr.new_path()
            if key == '↵':
                _return(cr, x + pad + dx, mid + dy, length)
            elif key in ('↑', '↓'):
                _varrow(cr, x + w/2 + dx, top + pad + dy, length, 1 if key == '↓' else -1)
            else:
                _arrow(cr, x + pad + dx, mid + dy, length, 1 if key == '→' else -1)
        shape()
        x0, y0, x1, y1 = cr.stroke_extents()
        shape((x + w/2) - (x0 + x1)/2, mid - (y0 + y1)/2)
        cr.stroke()
    else:
        cr.move_to(x + (w - ext.width)/2 - ext.x_bearing, round(mid - ext.y_bearing - ext.height/2))
        cr.show_text(key)
    return w


def key_hints(cr, x, top, band_mid, keys, metrics, u, draw=True):
    """A row of key groups: boxes, then the action in tracked caps; returns the row's width."""
    x0 = x
    gap_key, gap_label, gap_group = round(4*u), round(7*u), round(28*u)
    for caps, label in keys:
        for key in caps:
            x = round(x)
            x += keycap(cr, x, top, key, metrics, draw) + gap_key
        x = round(x + gap_label - gap_key)
        _face(cr, 10*u)
        cr.set_source_rgb(*MUTED)
        ext = cr.text_extents(label)
        x += _tracked(cr, x, round(band_mid - (ext.y_bearing + ext.height/2)), label, 0.2, draw) + gap_group
    return x - gap_group - x0


def _return(cr, x, cy, length):
    """Path of the return key's arrow: down the right side, then left, with a 45° head."""
    rise, head = length*0.55, length*0.36
    right, bottom = x + length, cy + rise/2
    cr.move_to(right, cy - rise/2)
    cr.line_to(right, bottom)
    cr.line_to(x, bottom)
    cr.move_to(x + head, bottom - head)
    cr.line_to(x, bottom)
    cr.line_to(x + head, bottom + head)


def draw_strip(cr, width, height, index, count, keys=KEYS, status=None, level=None):
    """The strip, `width` x `height` device pixels, drawn with its top-left corner at the origin.

    Units are height/30. The one-pixel hairline is the top edge; everything else is centred by ink in the band below
    it. A key box keeps the same inner margin on every side: the space between the caps and the box's top and bottom
    is also its left and right padding, so S, I and ESC sit alike; arrow boxes are square, their strokes as long as
    the caps are tall, with the caps' stem weight. Gaps follow one scale: box to box, box to label, group to group."""
    u = height/30
    snap = round
    centre = (1 + height)/2

    def baseline(text):
        ext = cr.text_extents(text)
        return snap(centre - (ext.y_bearing + ext.height/2))

    options = cairo.FontOptions()
    options.set_hint_style(cairo.HINT_STYLE_NONE)
    options.set_hint_metrics(cairo.HINT_METRICS_OFF)
    options.set_antialias(cairo.ANTIALIAS_GRAY)
    cr.set_font_options(options)
    cr.set_source_rgba(*NAVY, 0.93)
    cr.rectangle(0, 0, width, height)
    cr.fill()
    cr.set_source_rgba(1, 1, 1, 0.14)
    cr.rectangle(0, 0, width, 1)
    cr.fill()
    margin = snap(24*u)
    # position: 09 / 42, one size, one cap line
    _face(cr, 12*u, bold=True)
    base = baseline(f'{index:02d}{count}')
    cr.set_source_rgb(*POLLEN)
    x = margin + _tracked(cr, margin, base, f'{index:02d}', 0.08)
    _face(cr, 12*u)
    cr.set_source_rgb(*MUTED)
    x += snap(7*u)
    x += _tracked(cr, x, base, '/', 0)
    x += snap(7*u)
    x += _tracked(cr, x, base, str(count), 0.08)
    if level and not status:                              # the background level ↑ ↓ change, after the position
        _face(cr, 10*u)
        cr.set_source_rgb(*MUTED)
        _tracked(cr, x + snap(28*u), baseline(level), level, 0.24)
    # keys, right-aligned
    metrics = keycap_metrics(cr, u, height - 1)
    top = 1 + (height - 1 - metrics[1])//2
    total = key_hints(cr, 0, top, centre, keys, metrics, u, draw=False)
    left = round(width - margin - total)
    key_hints(cr, left, top, centre, keys, metrics, u)
    if status:                                            # e.g. a set being downloaded: Pollen, before the keys
        _face(cr, 10*u, bold=True)
        cr.set_source_rgb(*POLLEN)
        _tracked(cr, left - snap(28*u) - snap(_tracked(cr, 0, 0, status, 0.24, draw=False)), baseline(status),
                 status, 0.24)


class Gallery:
    def __init__(self, files, first, set_desktop=None, settings=None, level=None, change_level=None):
        # the strip lists only the keys this gallery answers (the development viewers have no desktop or settings)
        self.keys = tuple(k for k in KEYS if (k[1] != 'SET AS DESKTOP' or set_desktop) and (k[1] != 'SETTINGS' or settings)
                          and (k[1] != 'INTENSITY' or change_level))
        # the background level: the one shown, and the one asked for with ↑ ↓ (ahead of it while a set is fetched)
        self.level = self.level_wanted = level
        self.change_level = change_level
        self.progress, self.progress_alpha, self.progress_frame = None, 0.0, 0
        self.files = [Path(f) for f in files]
        self.index = self.files.index(Path(first)) if Path(first) in self.files else 0
        self.set_desktop, self.settings = set_desktop, settings
        self.cache, self.mtimes, self.lock = {}, {}, threading.Lock()
        self.size, self.status = None, None
        self.resize_to, self.resize_since = None, 0.0
        self.menu, self.menu_done, self.menu_key, self.menu_alpha = None, None, None, 0.0
        self.strip_on, self.alpha, self.last_input = True, 1.0, time.monotonic()
        self.loop = GLib.MainLoop()
        GLib.set_prgname('p-bloom-wallpapers')               # the window class Omarchy's Super+O rule matches
        GLib.set_application_name('p(bloom) Wallpapers')
        Gtk.Window.set_default_icon_name('p-bloom-wallpapers')
        win = self.window = Gtk.Window(title='p(bloom) Wallpapers')
        win.set_decorated(False)
        win.set_default_size(1600, 900)                       # a window, as Hyprland tiles it; F for fullscreen
        provider = Gtk.CssProvider()
        provider.load_from_string('window { background: #000; } .pb-dim { background: rgba(4, 6, 11, 0.72); }')
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), provider,
                                                  Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        overlay = Gtk.Overlay()
        self.picture = Gtk.Picture(content_fit=Gtk.ContentFit.CONTAIN, can_shrink=True)
        overlay.set_child(self.picture)
        # the strip is rendered into a texture at the screen's own pixels (fractional scales included), so every
        # hairline and gap lands on a device pixel; fading is the widget's opacity
        self.strip = Gtk.Picture(valign=Gtk.Align.END, halign=Gtk.Align.FILL, can_target=False, can_shrink=True,
                                 content_fit=Gtk.ContentFit.FILL)
        overlay.add_overlay(self.strip)
        # the settings menu: the whole window, dimmed, with the panel in its centre; rendered like the strip
        self.menu_picture = Gtk.Picture(can_target=False, can_shrink=True, content_fit=Gtk.ContentFit.FILL)
        self.menu_picture.set_opacity(0)
        overlay.add_overlay(self.menu_picture)
        # a download: the window dimmed, the sheets' emblem turning in its middle as the progress
        self.dim = Gtk.Box(can_target=False, hexpand=True, vexpand=True)
        self.dim.add_css_class('pb-dim')
        self.dim.set_opacity(0)
        overlay.add_overlay(self.dim)
        self.progress_picture = Gtk.Picture(can_target=False, can_shrink=False, halign=Gtk.Align.CENTER,
                                            valign=Gtk.Align.CENTER, content_fit=Gtk.ContentFit.FILL)
        self.progress_picture.set_opacity(0)
        overlay.add_overlay(self.progress_picture)
        self.strip_key = None
        win.set_child(overlay)
        keys = Gtk.EventControllerKey()
        keys.connect('key-pressed', self._key)
        win.add_controller(keys)
        motion = Gtk.EventControllerMotion()
        motion.connect('motion', lambda *_: self._wake())
        win.add_controller(motion)
        win.connect('close-request', lambda *_: self.loop.quit() or False)
        win.present()
        GLib.timeout_add(16, self._tick)
        GLib.timeout_add(1000, self._watch)

    # images: scaled once to the window on a worker thread, neighbours prepared ahead
    def _scale(self):
        surface = self.window.get_surface()
        return (surface.get_scale() if surface and hasattr(surface, 'get_scale') else self.window.get_scale_factor()) or 1

    def _target(self):
        w, h = self.window.get_width(), self.window.get_height()
        scale = self._scale()
        return (max(1, round(w*scale)), max(1, round(h*scale))) if w and h else None

    def _load(self, path, size):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(str(path))
        k = min(size[0]/pixbuf.get_width(), size[1]/pixbuf.get_height())
        if k < 1:
            pixbuf = pixbuf.scale_simple(max(1, round(pixbuf.get_width()*k)), max(1, round(pixbuf.get_height()*k)),
                                         GdkPixbuf.InterpType.HYPER)
        return Gdk.Texture.new_for_pixbuf(pixbuf)

    def _prepare(self, i, size):
        files = self.files
        path = files[i % len(files)]
        key = (path, size, path.stat().st_mtime_ns)
        with self.lock:
            if key in self.cache:
                return self.cache[key]
        texture = self._load(path, size)
        with self.lock:
            self.cache[key] = texture
            # keep the shown sheet and its two neighbours at the current size
            near = {files[(self.index + d) % len(files)] for d in (-1, 0, 1)}
            for old in [k for k in self.cache if k[1] != size or k[0] not in near]:
                self.cache.pop(old, None)
        return texture

    def _show(self):
        size = self._target()
        if not size:
            return
        self.size = size
        self._render_strip()
        self.picture.set_paintable(self._prepare(self.index, size))
        self.window.set_title(f'p(bloom) Wallpapers — {self.index + 1}/{len(self.files)} — {self.files[self.index].name}')
        for step in (1, -1):
            threading.Thread(target=self._prepare, args=(self.index + step, size), daemon=True).start()

    def _resized(self):
        """F, a new tile, a monitor change: the image is scaled again for the window's new size once it has held
        still for a moment (Hyprland animates resizes; until then GTK stretches the previous scaling)."""
        target, now = self._target(), time.monotonic()
        if not target or target == self.size:
            self.resize_to = None
        elif target != self.resize_to:
            self.resize_to, self.resize_since = target, now
        elif now - self.resize_since > 0.15:
            self.resize_to = None
            self._show()

    def _watch(self):
        path = self.files[self.index]
        try:
            mtime = path.stat().st_mtime_ns
        except OSError:
            return True
        if self.mtimes.get(path, mtime) != mtime:
            self._show()
        self.mtimes[path] = mtime
        return True

    # the strip: drawn in cairo, faded by alpha
    def _render_strip(self):
        width, height, scale = self.window.get_width(), self.window.get_height(), self._scale()
        if not width or not height:
            return
        # 30/1080 of the window, in logical pixels that are whole device pixels too
        want = max(24, min(height*30/1080, width*30/1150))      # a narrow window: the keys and a status still fit
        logical = min(range(int(want) - 4, int(want) + 5), key=lambda h: (abs(h*scale - round(h*scale)) > 1e-6, abs(h - want)))
        device_w, device_h = round(width*scale), round(logical*scale)
        key = (self.index, len(self.files), device_w, device_h, self.status, self.level_wanted)
        if key == self.strip_key:
            return
        self.strip_key = key
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, device_w, device_h)
        draw_strip(cairo.Context(surface), device_w, device_h, self.index + 1, len(self.files), self.keys,
                   self.status, (self.level_wanted or '').upper() or None)
        surface.flush()
        texture = Gdk.MemoryTexture.new(device_w, device_h, Gdk.MemoryFormat.B8G8R8A8_PREMULTIPLIED,
                                        GLib.Bytes.new(bytes(surface.get_data())), surface.get_stride())
        self.strip.set_size_request(-1, logical)
        self.strip.set_paintable(texture)

    def _wake(self):
        self.last_input = time.monotonic()

    def _tick(self):
        if self.size is None:
            self._show()
        else:
            self._resized()
            self._render_strip()                           # a no-op unless what the strip shows has changed
            self._render_menu()
        idle = time.monotonic() - self.last_input
        want = 0.0 if self.menu or self.progress else 1.0 if self.status or (self.strip_on and idle < IDLE) else 0.0
        step = 0.016/FADE
        if want != self.alpha:
            self.alpha = min(want, self.alpha + step) if want > self.alpha else max(want, self.alpha - step)
            self.strip.set_opacity(self.alpha)
        want = 1.0 if self.menu else 0.0
        if want != self.menu_alpha:
            self.menu_alpha = min(want, self.menu_alpha + step) if want > self.menu_alpha else max(want, self.menu_alpha - step)
            self.menu_picture.set_opacity(self.menu_alpha)
        want = 1.0 if self.progress else 0.0
        if want != self.progress_alpha:
            self.progress_alpha = min(want, self.progress_alpha + step) if want > self.progress_alpha else max(want, self.progress_alpha - step)
            self.dim.set_opacity(self.progress_alpha)
            self.progress_picture.set_opacity(self.progress_alpha)
        self.progress_frame += 1
        if self.progress and self.progress_frame % 2 == 0:  # the emblem turns at 30 frames a second
            self._render_progress()
        return True

    def _render_progress(self):
        from settings_ui import PROGRESS_SIZE, draw_progress
        width, height, scale = self.window.get_width(), self.window.get_height(), self._scale()
        if not width or not height:
            return
        u = min(height/1080, width/1000)                    # logical pixels per unit, as in the settings menu
        w, h = round(PROGRESS_SIZE[0]*u), round(PROGRESS_SIZE[1]*u)
        device_w, device_h = round(w*scale), round(h*scale)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, device_w, device_h)
        draw_progress(cairo.Context(surface), u*device_w/w, (time.monotonic()/9) % 1.0, self.progress)
        surface.flush()
        self.progress_picture.set_size_request(w, h)
        self.progress_picture.set_paintable(Gdk.MemoryTexture.new(device_w, device_h, Gdk.MemoryFormat.B8G8R8A8_PREMULTIPLIED,
                                                                  GLib.Bytes.new(bytes(surface.get_data())),
                                                                  surface.get_stride()))

    def show_progress(self, info):
        """A download or install under way (see settings_ui.draw_progress), or None when it is over."""
        self.progress = info
        if info:
            self._render_progress()

    def _render_menu(self):
        if not self.menu:
            return
        width, height, scale = self.window.get_width(), self.window.get_height(), self._scale()
        if not width or not height:
            return
        device_w, device_h = round(width*scale), round(height*scale)
        key = (device_w, device_h, self.menu.state())
        if key == self.menu_key:
            return
        self.menu_key = key
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, device_w, device_h)
        self.menu.draw(cairo.Context(surface), device_w, device_h)
        surface.flush()
        self.menu_picture.set_paintable(Gdk.MemoryTexture.new(device_w, device_h, Gdk.MemoryFormat.B8G8R8A8_PREMULTIPLIED,
                                                              GLib.Bytes.new(bytes(surface.get_data())),
                                                              surface.get_stride()))

    def show_menu(self, menu, done):
        """Open a menu over the wallpaper; done(result) is called once with what its key() returned."""
        self.menu, self.menu_done, self.menu_key = menu, done, None
        self._render_menu()

    def _menu_key(self, name):
        result = self.menu.key(name)
        if result is None:
            self._render_menu()
            return
        done = self.menu_done
        self.menu, self.menu_done = None, None
        self._wake()
        done(result[1] if result[0] == 'save' else None)

    def _key(self, controller, keyval, keycode, state):
        self._wake()
        name = Gdk.keyval_name(keyval) or ''
        if self.menu and name.lower() != 'f':              # the menu has the keys while it is open; F still works
            self._menu_key(name)
        elif name in ('Right', 'Left'):
            self.index = (self.index + (1 if name == 'Right' else -1)) % len(self.files)
            self._show()
        elif name in ('Home', 'End'):
            self.index = 0 if name == 'Home' else len(self.files) - 1
            self._show()
        elif name in ('Up', 'Down') and self.change_level and self.level_wanted in LEVELS:
            i = LEVELS.index(self.level_wanted) + (1 if name == 'Up' else -1)   # up is towards Vivid
            if 0 <= i < len(LEVELS):
                self.level_wanted = LEVELS[i]
                self.change_level(self, LEVELS[i])
        elif name in ('Return', 'KP_Enter') and self.set_desktop:
            self.set_desktop(self, self.files[self.index])  # the caller runs it off the main thread
        elif name.lower() == 's' and self.settings:
            self.settings(self)
        elif name.lower() == 'i':
            self.strip_on = not self.strip_on
        elif name.lower() == 'f':
            if self.window.is_fullscreen():
                self.window.unfullscreen()
            else:
                self.window.fullscreen()
        elif name in ('Escape',) or name.lower() == 'q':
            self.loop.quit()
        return True

    def set_status(self, text):
        """A line in the strip that stays until it is cleared (None)."""
        self.status = text

    def replace(self, files, level=None):
        """A new set after settings were saved: same wallpaper, new files."""
        if level:
            self.level = level
        name = self.files[self.index].name
        self.files = [Path(f) for f in files]
        self.index = next((i for i, f in enumerate(self.files) if f.name == name), 0)
        with self.lock:
            self.cache.clear()
        self._show()

    def run(self):
        self.loop.run()


def run(files, first, set_desktop=None, settings=None, open_settings=False, level=None, change_level=None):
    """open_settings: start with the settings menu open (the app menu's Wallpaper settings, --configure).
    level and change_level(view, level): the background level shown, and what ↑ ↓ call to change it."""
    view = Gallery(files, first, set_desktop, settings, level, change_level)
    view.saved_level = level
    if open_settings and settings:
        GLib.idle_add(settings, view)
    view.run()


if __name__ == '__main__':
    files = sorted(Path(sys.argv[1]).glob('*.webp'))
    run(files, files[0])
