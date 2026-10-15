"""p(bloom) Wallpapers: the settings menu, drawn over the gallery's wallpaper like a game's pause menu.

Nothing to choose: the wallpapers follow the optimal set for the connected monitors (one for all of them, as Omarchy
shows one wallpaper on every monitor). The menu shows the monitors, the set in use, and that set's packs, one per
intensity, installed or not. Its one action, DOWNLOAD OPTIMAL, fetches the missing packs in the background, with the
progress in the gallery's middle; then the gallery's ↑ ↓ switch intensity at once. Keys are boxed like the gallery's: Enter
downloads, Esc or S closes. Units are 1/1080 of the window's height; everything is drawn at the screen's own pixels and
centred by ink, as in gallery.draw_strip.
"""
import math

import cairo

from gallery import ICE, MUTED, NAVY, POLLEN, _face, _tracked, key_hints, keycap_metrics

LEVELS = ('muted', 'default', 'vivid')
LEVEL_LABELS = {'muted': 'MUTED', 'default': 'DEFAULT', 'vivid': 'VIVID'}
TEXT = (0.82, 0.88, 0.97)


def missing(plan):
    return [k for k in plan.get('packs', []) if not k['local']]


def action(plan):
    """What Enter does: ('download', megabytes) when packs are missing, ('optimal', 0) when a manual set from an
    earlier version is in use, else None."""
    lacking = missing(plan)
    if lacking:
        return 'download', sum(k['bytes'] for k in lacking)/1e6
    if plan.get('setting', 'auto') != 'auto':
        return 'optimal', 0
    return None


def keys(plan):
    what = action(plan)
    if not what:
        return ((('ESC',), 'CLOSE'),)
    label = f'DOWNLOAD OPTIMAL · {what[1]:.0f} MB' if what[0] == 'download' else 'USE OPTIMAL'
    return ((('↵',), label), (('ESC',), 'CLOSE'))


def draw_settings(cr, W, H, plan):
    u = min(H/1080, W/1000)                                    # a portrait screen: the panel fits its width
    snap = round
    options = cairo.FontOptions()
    options.set_hint_style(cairo.HINT_STYLE_NONE)
    options.set_hint_metrics(cairo.HINT_METRICS_OFF)
    options.set_antialias(cairo.ANTIALIAS_GRAY)
    cr.set_font_options(options)
    cr.set_source_rgba(4/255, 6/255, 11/255, 0.70)          # the wallpaper behind stays visible, quieted
    cr.paint()

    def centred(text, mid):
        ext = cr.text_extents(text)
        return snap(mid - (ext.y_bearing + ext.height/2))

    def width_of(text, track):
        return _tracked(cr, 0, 0, text, track, draw=False)

    screens = plan.get('monitors') or []
    packs = plan.get('packs') or []
    in_use = plan.get('label', '')
    optimal = plan.get('profile') == plan.get('optimal', plan.get('profile'))
    # one vertical scale: SECTION above each section's label, LABEL from the label to its rows
    pw, pad, row_h = snap(640*u), snap(44*u), snap(28*u)
    SECTION, LABEL, footer_h = snap(30*u), snap(14*u), snap(76*u)
    title_mid, rule_y = snap(46*u), snap(80*u)
    sections = [('MONITORS', max(1, len(screens))), ('IN USE', 1), ('PACKS', len(packs))]
    room = H - snap(120*u) - pad - rule_y - footer_h - SECTION//2 - sum(SECTION + LABEL for _ in sections)
    row_h = min(row_h, max(snap(18*u), room//max(1, sum(n for _, n in sections))))
    ph = pad + rule_y + sum(SECTION + LABEL + n*row_h for _, n in sections) + SECTION//2 + footer_h
    x0, y0 = snap((W - pw)/2), snap((H - ph)/2)
    inner0, inner1 = x0 + pad, x0 + pw - pad
    # the panel: navy, a hairline border, the sheets' corner marks just outside it
    cr.set_source_rgba(*NAVY, 0.95)
    cr.rectangle(x0, y0, pw, ph)
    cr.fill()
    cr.set_source_rgba(1, 1, 1, 0.14)
    cr.set_line_width(1)
    cr.rectangle(x0 + 0.5, y0 + 0.5, pw - 1, ph - 1)
    cr.stroke()
    mark, off = snap(22*u), snap(10*u)
    cr.set_source_rgba(*ICE, 0.55)
    for cx, cy, sx, sy in ((x0 - off, y0 - off, 1, 1), (x0 + pw + off, y0 - off, -1, 1),
                           (x0 - off, y0 + ph + off, 1, -1), (x0 + pw + off, y0 + ph + off, -1, -1)):
        cr.move_to(cx + 0.5*sx, cy + sy*mark)
        cr.line_to(cx + 0.5*sx, cy + 0.5*sy)
        cr.line_to(cx + sx*mark, cy + 0.5*sy)
    cr.stroke()
    # header
    y = y0 + pad
    _face(cr, 10*u)
    cr.set_source_rgb(*MUTED)
    _tracked(cr, inner0, centred('P', y + snap(6*u)), 'P(BLOOM) WALLPAPERS', 0.28)
    _face(cr, 26*u, bold=True)
    cr.set_source_rgb(*ICE)
    _tracked(cr, inner0, centred('O', y + title_mid), 'OPTIMAL SET', 0.3)
    y += rule_y
    cr.set_source_rgba(1, 1, 1, 0.14)
    cr.rectangle(inner0, y, inner1 - inner0, 1)
    cr.fill()

    def label(text, y, note=None):
        _face(cr, 9*u)
        cr.set_source_rgb(*MUTED)
        _tracked(cr, inner0, centred(text[0], y), text, 0.28)
        if note:
            _tracked(cr, inner1 - snap(width_of(note, 0.28)), centred(note[0], y), note, 0.28)

    def left(text, mid, color=TEXT, bold=False, x=None):
        _face(cr, 12*u, bold=bold)
        cr.set_source_rgb(*color)
        cr.move_to(inner0 if x is None else x, centred('5', mid))
        cr.show_text(text)
        return cr.text_extents(text).x_advance

    def right(text, mid, color, x=None, size=12, track=0.0, bold=False):
        _face(cr, size*u, bold=bold)
        cr.set_source_rgb(*color)
        width = snap(width_of(text, track))
        _tracked(cr, (inner1 if x is None else x) - width, centred('O' if text[:1].isalpha() else '5', mid), text, track)

    # the monitors the optimal set is chosen for
    y += SECTION
    label('MONITORS', y)
    top = y + LABEL
    for n, m in enumerate(screens or [None]):
        mid = top + n*row_h + row_h/2
        if m is None:
            left('None detected', mid, MUTED)
            continue
        left(m['name'], mid, ICE, bold=True)
        right(f"{m['width']} × {m['height']}", mid, TEXT)
    y = top + max(1, len(screens))*row_h
    # the set in use
    y += SECTION
    label('IN USE', y)
    mid = y + LABEL + row_h/2
    left(in_use, mid, ICE, bold=True)
    right('OPTIMAL' if optimal else 'MANUAL', mid, POLLEN if optimal else MUTED, size=9, track=0.24, bold=optimal)
    y += LABEL + row_h
    # the set's packs: one per intensity, its size, installed or not
    y += SECTION
    lacking = missing(plan)
    label('PACKS', y, 'ALL INSTALLED' if packs and not lacking else f'{len(packs) - len(lacking)} OF {len(packs)} INSTALLED')
    top = y + LABEL
    mb_right = inner0 + snap(330*u)
    for n, k in enumerate(packs):
        mid = top + n*row_h + row_h/2
        left(LEVEL_LABELS[k['level']].capitalize(), mid, TEXT if k['local'] else MUTED)
        if k['bytes']:
            right(f"{k['bytes']/1e6:.1f} MB", mid, MUTED, x=mb_right)
        right('INSTALLED' if k['local'] else 'DOWNLOAD', mid, MUTED if k['local'] else POLLEN, size=9, track=0.24,
              bold=not k['local'])
    # footer: the action and the keys, centred
    fy = top + len(packs)*row_h + SECTION//2
    cr.set_source_rgba(1, 1, 1, 0.14)
    cr.rectangle(inner0, fy, inner1 - inner0, 1)
    cr.fill()
    metrics = keycap_metrics(cr, u, footer_h - 1)
    ktop = fy + 1 + (footer_h - 1 - metrics[1])//2
    band = fy + (1 + footer_h)/2
    hints = keys(plan)
    total = key_hints(cr, 0, ktop, band, hints, metrics, u, draw=False)
    key_hints(cr, snap(x0 + (pw - total)/2), ktop, band, hints, metrics, u)


class Menu:
    """The menu's state and keys; the gallery draws it with draw() and passes it the keys while it is open."""

    def __init__(self, plan):
        self.plan = plan
        self.level = plan.get('setting_level', 'default') if plan.get('setting_level') in LEVELS else 'default'

    def state(self):
        return 0

    def draw(self, cr, width, height):
        draw_settings(cr, width, height, self.plan)

    def key(self, name):
        """('save', choice), ('cancel', None), or None when the menu stays open. The intensity is kept; saving makes
        the resolution automatic (the optimal set) and, with packs missing, downloads them."""
        if name in ('Return', 'KP_Enter'):
            what = action(self.plan)
            if not what:
                return None
            choice = {'profile': 'auto', 'level': self.level}
            if what[0] == 'download':
                choice['download'] = 'optimal'
            return 'save', choice
        if name in ('Escape', 's', 'S', 'q', 'Q'):
            return 'cancel', None
        return None

def polar(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r*math.cos(a), cy + r*math.sin(a)


PROGRESS_SIZE = (560, 430)                                    # the box the progress is drawn in, in units


def draw_progress(cr, u, t, info):
    """The sheets' corner emblem as a progress indicator, drawn in a PROGRESS_SIZE box (units of u).

    The rings turn as on the sheets (t is the loop's phase, 0..1); the Pollen arc is the download's progress, with the
    percentage in the middle. Without a byte count (installing, or nothing to count) the arc turns on its own and the
    middle holds the icon's flower. Below: what is happening, the set, and the megabytes."""
    w, h = PROGRESS_SIZE[0]*u, PROGRESS_SIZE[1]*u
    options = cairo.FontOptions()
    options.set_hint_style(cairo.HINT_STYLE_NONE)
    options.set_hint_metrics(cairo.HINT_METRICS_OFF)
    options.set_antialias(cairo.ANTIALIAS_GRAY)
    cr.set_font_options(options)
    phase = info.get('phase', 'download')
    total, done = info.get('total') or 0, info.get('done') or 0
    fraction = min(1.0, done/total) if phase == 'download' and total else None
    x, y, k = w/2, 160*u, 140*u/140
    turn = 360*t

    def ink(a, color=ICE):
        cr.set_source_rgba(*color, a)

    def stroke(a, width, color=ICE, dash=None):
        ink(a, color)
        cr.set_line_width(width*u)
        cr.set_dash([d*u for d in dash] if dash else [])
        cr.stroke()
        cr.set_dash([])

    def circ(r, a, width, dash=None):
        cr.new_sub_path()
        cr.arc(x, y, r, 0, 2*math.pi)
        stroke(a, width, dash=dash)

    def arc(r, a0, a1, a, width, color=ICE):
        cr.new_sub_path()
        cr.arc(x, y, r, math.radians(a0), math.radians(a1))
        stroke(a, width, color)

    circ(140*k, 0.12, 0.5)
    for i in range(4):                                            # diamonds on the outer ring
        px, py = polar(x, y, 140*k, 45 + 90*i)
        d = 3.2*k
        cr.move_to(px, py - d); cr.line_to(px + d, py); cr.line_to(px, py + d); cr.line_to(px - d, py); cr.close_path()
        ink(0.9)
        cr.fill()
    for i in range(2):
        a0 = turn*2 + 180*i + 20
        arc(130*k, a0, a0 + 56, 0.45, 0.7)
    for i in range(8):                                            # the segmented band
        a0 = -turn + 45*i
        cr.new_sub_path()
        cr.arc(x, y, 120*k, math.radians(a0), math.radians(a0 + 34))
        cr.arc_negative(x, y, 113*k, math.radians(a0 + 34), math.radians(a0))
        cr.close_path()
        if i % 2 == 0:
            ink(0.55)
            cr.fill_preserve()
        stroke(0.6, 0.7)
    circ(105*k, 0.3, 0.5, dash=[2, 4])
    # progress: the Pollen arc from the top, clockwise; a faint track under it
    if fraction is not None:
        circ(99*k, 0.12, 1.6)
        a0, a1 = -90, -90 + 360*fraction
    else:
        a0 = turn*1.5 - 90
        a1 = a0 + 78
    if a1 > a0:
        arc(99*k, a0, a1, 0.95, 2.2, POLLEN)
    cr.arc(*polar(x, y, 99*k, a1), 2.6*k, 0, 2*math.pi)
    ink(0.95, POLLEN)
    cr.fill()
    cr.save()
    cr.translate(x, y)
    cr.rotate(math.radians(-turn/2))
    for i in range(72):                                           # ticks, every sixth longer
        length = (7 if i % 6 == 0 else 3.5)*k
        cr.move_to(*polar(0, 0, 90*k, i*5))
        cr.line_to(*polar(0, 0, 90*k + length, i*5))
    stroke(0.45, 0.4)
    cr.restore()
    for i in range(3):
        a0 = turn + 120*i
        arc(82*k, a0, a0 + 96, 0.9, 2.2)
    circ(75*k, 0.35, 0.5)
    for sgn in (-1, 1):
        cr.move_to(x + sgn*66*k, y)
        cr.line_to(x + sgn*72*k, y)
    stroke(0.6, 0.6)
    # the middle: the percentage, or the flower
    if fraction is not None:
        number = f'{int(fraction*100)}'
        _face(cr, 34*u, bold=True)
        ext = cr.text_extents(number)
        _face(cr, 13*u)
        pct = cr.text_extents('%')
        gap = 3*u
        left = x - (ext.x_advance + gap + pct.x_advance)/2
        base = y - (ext.y_bearing + ext.height/2)
        _face(cr, 34*u, bold=True)
        ink(1.0)
        cr.move_to(left, base)
        cr.show_text(number)
        _face(cr, 13*u)
        ink(1.0, MUTED)
        cr.move_to(left + ext.x_advance + gap, base)
        cr.show_text('%')
    else:
        R = 20*k
        for i in range(5):
            a = -90 + i*72 + turn/3
            px, py = polar(x, y, R, a)
            cr.arc(px, py, R*0.74, 0, 2*math.pi)
            cr.close_path()
        ink(0.95, POLLEN)
        cr.fill()
        cr.arc(x, y, R*0.42, 0, 2*math.pi)
        cr.set_source_rgba(*NAVY, 1)
        cr.fill()
    # the words, centred under the emblem
    title = {'download': 'DOWNLOADING', 'install': 'INSTALLING'}.get(phase, 'UPDATING WALLPAPERS')
    level = info.get('level', 'default')
    detail = ' · '.join(p for p in (info.get('label', ''), LEVEL_LABELS.get(level, '') if level != 'default' else '') if p)
    sizes = f'{done/1e6:.1f} / {total/1e6:.1f} MB' if total and phase == 'download' else ''
    if info.get('packs', 1) > 1:                              # DOWNLOAD OPTIMAL: one pack of several
        sizes = ' · '.join(x for x in (f"PACK {info['pack']} OF {info['packs']}", sizes) if x)

    def line(text, size, bold, color, mid, track):
        if not text:
            return
        _face(cr, size*u, bold=bold)
        ink(1.0, color)
        width = _tracked(cr, 0, 0, text, track, draw=False)
        ext = cr.text_extents('H')
        _tracked(cr, round(x - width/2), round(mid - (ext.y_bearing + ext.height/2)), text, track)
    line(title, 13, True, ICE, 340*u, 0.3)
    line(detail.upper(), 10, False, MUTED, 368*u, 0.24)
    line(sizes, 10, False, MUTED, 390*u, 0.08)
