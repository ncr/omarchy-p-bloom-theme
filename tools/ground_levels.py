#!/usr/bin/env python3
"""Ground levels (Muted / Default / Vivid) and the type-contrast audit.

Every wallpaper exists at three background intensities. Only the ground
changes (the gradient, the central glow and the vignette drawn by
Sheet.background); lines, type and accents are identical at every level.
Default is the design itself. The Muted and Vivid ground of each palette is
stored in docs/collection/palettes.json (`levels`) as HLS saturation and
lightness, the same parameters as the design, so a render needs no colour
science. This tool derives those values and checks them:

    python3 tools/ground_levels.py            # table: OKLab step and contrast per ground x level
    python3 tools/ground_levels.py --write    # re-derive and store `levels` in palettes.json

The rule (see MUTED_CHROMA and the comment above it) works in OKLab on the
whole rendered ground, glow and vignette included, because that is what the
eye averages:

* each ground's two steps are the same perceptual distance d (Delta E from
  Default); d follows the ground's own colour (Muted = half its chroma), so
  saturated grounds move more than quiet ones and every ground keeps its
  identity; graphite steps mostly in lightness and stays grey;
* a step may never cost legibility: white type (alpha 0.60) and the
  palette's accents keep CONTRAST_FLOOR, or where Default is below it, their
  Default contrast (RELAX_TEXT grounds: accents only). Where the caps stop
  Vivid short, Muted takes the same shorter step.

The contrast audit (text_contrast / contrast_issues) runs on final pixels in
tools/aspect_layout.audit, i.e. in tools/render_wallpaper_sets.py and
tools/verify_wallpaper_layout.py --profile, for every composed sheet at every
level. It measures each label's actual ink (colour and alpha) over every
ground pixel inside its box (the worst one counts), before grain and bloom.
"""
import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from sheet import GLOW, Sheet, ground_tone  # noqa: E402
PALETTES_JSON = ROOT/'docs/collection/palettes.json'
LEVELS = ('muted', 'default', 'vivid')

# WCAG 2 contrast ratio floors, measured per label against every ground
# pixel under it, with the label's own alpha. Body type is white at alpha
# >= 0.60 (production guide, section 23). Accent type (ARC / GOLD) marks small
# indices and highlights and follows the WCAG non-text / large-text floor.
# A label passes at a level when it reaches the floor, or - where the accepted
# Default design is itself below the floor - when it is at least as legible
# as the same label on the Default ground. Default therefore always passes;
# its own shortfalls are reported (`below_floor`), not failed.
CONTRAST_FLOOR = {'text': 4.5, 'accent': 3.0}

# Per-ground symmetric steps (owner, 2026-09-27): for each ground, Muted and
# Vivid are the same perceptual distance d from Default (Delta E, OKLab, mean
# of the rendered ground), and d follows the ground's own colour: Muted is
# Default with half its chroma at the same lightness, which defines d; Vivid
# adds chroma (lightness only as needed) until it is d away too. Quiet grounds
# (near-neutral, chroma below 0.015) step by QUIET_STEP mostly in lightness, so graphite
# stays grey. Where the contrast caps stop Vivid short of d, Muted takes the
# same shorter step, so both steps of a ground stay equal.
MUTED_CHROMA = 0.5
QUIET_STEP = 0.020
STEP_TOLERANCE = 0.002
RULE = {'muted': {}, 'vivid': {}}
# The owner relaxed the white-text 4.5:1 cap for saffron only. On 2026-10-01 he also kept saffron's full
# Muted/Vivid step (Delta E ~3) over full accent protection (which would shrink it to ~1.4): accents on
# saffron must keep ACCENT_FLOOR_RELAXED instead of 3:1 (the composed 4:3, 3:2 and 16:10 layouts move a few
# faint diagram callouts of Proxy and Sun Still onto the brighter part of the Vivid ground).
RELAX_TEXT = {'saffron'}
ACCENT_FLOOR_RELAXED = 2.4
KEEP_GROUND = set()  # grounds that stay at their Default tone at every level


# -- colour -----------------------------------------------------------------

def linear(c):
    c = np.asarray(c, float)
    return np.where(c <= 0.04045, c/12.92, ((c+0.055)/1.055)**2.4)


def luminance(rgb):
    """WCAG relative luminance of sRGB values in 0..1 (last axis RGB)."""
    return linear(rgb) @ np.array([0.2126, 0.7152, 0.0722])


def ratio(y1, y2):
    hi, lo = np.maximum(y1, y2), np.minimum(y1, y2)
    return (hi+0.05)/(lo+0.05)


def oklab(rgb):
    lms = np.cbrt(linear(rgb) @ np.array([
        [0.4122214708, 0.5363325363, 0.0514459929],
        [0.2119034982, 0.6806995451, 0.1073969566],
        [0.0883024619, 0.2817188376, 0.6299787005]]).T)
    return lms @ np.array([
        [0.2104542553, 0.7936177850, -0.0040720468],
        [1.9779984951, -2.4285922050, 0.4505937099],
        [0.0259040371, 0.7827717662, -0.8086757660]]).T


def bgra_rgb(buf, w, h):
    """A Cairo ARGB32 snapshot (numpy, BGRA bytes) as float RGB 0..1."""
    return np.asarray(buf)[:h, :w, [2, 1, 0]].astype(np.float32)/255


# -- contrast audit -----------------------------------------------------------

def role(ink):
    """'text' for the neutral white type, 'accent' for any coloured ink."""
    r, g, b = ink[:3]
    return 'text' if min(r, g, b) > 0.9 else 'accent'


def reference_ground(s, level='default'):
    """The ground of a finished sheet redrawn alone at another level (RGB 0..1).

    Same canvas, glow centre and palette; used to compare a label with the
    same label on the Default ground.
    """
    import cairo
    w, h = s.px
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(surface)
    c.scale(s.s, s.s)
    hue, sat, light, *glow = ground_tone(s.ground, level)
    Sheet.background(SimpleNamespace(layer_mode=False, c=c, bg=(hue, sat, light), bg_glow=glow,
                                     W=s.W, H=s.H, cx=s.cx, cy=s.cy))
    surface.flush()
    buf = np.frombuffer(surface.get_data(), np.uint8).reshape(h, -1, 4)
    return bgra_rgb(buf, w, h)


def _label_ratio(t, rgb, y):
    h, w = rgb.shape[:2]
    x0, y0, x1, y1 = t['box']
    x0, y0 = max(0, math.floor(x0)), max(0, math.floor(y0))
    x1, y1 = min(w, math.ceil(x1)), min(h, math.ceil(y1))
    if x1 <= x0 or y1 <= y0:
        return None
    # Every ground pixel under the label: the lightest is the worst case for
    # light ink, the darkest for dark ink.
    ground = rgb[y0:y1, x0:x1].reshape(-1, 3)
    ink = t['ink']
    seen = ink[3]*np.array(ink[:3]) + (1-ink[3])*ground
    return float(ratio(luminance(seen), luminance(ground)).min())


def text_contrast(texts, rgb, reference=None):
    """[{text, role, ratio, need, font_px}] for every label that recorded its ink.

    rgb: the ground the labels sit on; reference: the Default ground of the
    same canvas (None when rgb is the Default ground).
    """
    y = luminance(rgb)
    y_ref = y if reference is None else luminance(reference)
    reference = rgb if reference is None else reference
    out = []
    for t in texts:
        if not t.get('ink'):
            continue
        r = _label_ratio(t, rgb, y)
        if r is None:
            continue
        kind = role(t['ink'])
        need = min(CONTRAST_FLOOR[kind], _label_ratio(t, reference, y_ref))
        out.append(dict(text=t['text'], role=kind, font_px=t['font_px'],
                        ratio=round(r, 2), need=round(need, 2)))
    return out


def summary(contrast):
    """Lowest ratio per role, the label that has it, and how many are below the floor."""
    out = {}
    for c in contrast:
        row = out.setdefault(c['role'], dict(ratio=math.inf, text=None, below_floor=0))
        if c['ratio'] < row['ratio']:
            row.update(ratio=c['ratio'], text=c['text'])
        row['below_floor'] += c['ratio'] < CONTRAST_FLOOR[c['role']]
    return out


def contrast_issues(contrast, ground=None):
    """Labels below what they must keep. On RELAX_TEXT grounds white type is
    reported (summary) but not failed; accents always count."""
    relaxed = {'text'} if ground in RELAX_TEXT else set()
    def need(c):
        return min(c['need'], ACCENT_FLOOR_RELAXED) if ground in RELAX_TEXT and c['role'] == 'accent' else c['need']
    # Rounded values; 0.01 absorbs the rounding of both numbers.
    return [f"{c['role']} contrast {c['ratio']:.2f}:1 < {need(c):.2f}:1: {c['text']}"
            for c in contrast if c['ratio'] < need(c) - 0.01 and c['role'] not in relaxed]


# -- grounds ------------------------------------------------------------------

# Probe canvases for the derivation: 16:9, 4:3 and 32:9, with the glow at the
# middle and raised (the stacked 4:3 and duo layouts move it with the main
# drawing). The gradient, glow and vignette are defined in design units, so
# small probes give the same statistics as full-size files.
PROBES = [((320, 180), None), ((240, 180), None), ((640, 180), None), ((320, 180), 0.36), ((240, 180), 0.36)]
# The inks the contrast constraint protects: white type at its lowest alpha,
# and both accents of the palette at the alpha accent type uses (0.90; the
# per-label audit on final pixels checks every actual alpha).
TEXT_ALPHA, ACCENT_ALPHA = 0.60, 0.90
# Lower accent alphas that the per-label audit found on a ground's sheets
# (teal: Quantum Simulator's Z_L callout at 0.70).
ACCENT_ALPHA_BY_GROUND = {'teal': 0.70}
WHITE = (0.95, 0.965, 0.98)


def palettes():
    return json.loads(PALETTES_JSON.read_text())


@lru_cache(maxsize=4096)
def ground_image(name, tone, size=(320, 180), cy=None):
    """Render only the ground of `name` with tone (hue 0-1, sat, light, glow, glow lightness).

    Cached; treat the returned array as read-only.
    """
    tone = tuple(float(v) for v in tone)
    s = Sheet(*size)
    s.set_palette(name)
    s.bg, s.bg_glow = tone[:3], tone[3:5]
    if cy is not None:
        s.cy = cy*s.H
    s.background()
    s.surface.flush()
    buf = np.frombuffer(s.surface.get_data(), np.uint8).reshape(size[1], -1, 4)
    return bgra_rgb(buf, *size)


def mean_lab(img):
    """Typical OKLab colour (L, a, b) of a ground image: the median over the
    image without a 4 % margin, the same measure the review uses on
    rendered 1080p sheets (where the median ignores the line work)."""
    h, w = img.shape[:2]
    mh, mw = max(1, round(h*.04)), max(1, round(w*.04))
    return np.median(oklab(img[mh:h-mh:2, mw:w-mw:2].reshape(-1, 3)), axis=0)


def delta_e(img, ref):
    """OKLab Delta E between the mean colours of two ground images."""
    return float(np.linalg.norm(mean_lab(img) - mean_lab(ref)))


def stats(img):
    """Mean OKLab lightness and chroma (of the mean colour) of a ground image,
    and how much the centre (the glow, around the main drawing) stands out."""
    h, w = img.shape[:2]
    lab = oklab(img.reshape(-1, 3))
    L = lab[:, 0].reshape(h, w)
    yy, xx = np.mgrid[0:h, 0:w]
    centre = (xx-w/2)**2 + (yy-h*0.46)**2 < (0.12*w)**2
    a, b = lab[:, 1].mean(), lab[:, 2].mean()
    return float(L.mean()), float(np.hypot(a, b)), float(L[centre].mean()-L.mean())


def inks(name, data):
    colours = data['theme_colours']
    def rgb(key):
        h = colours[key].lstrip('#')
        return np.array([int(h[i:i+2], 16)/255 for i in (0, 2, 4)])
    a, b = data['palettes'][name][3:5]
    alpha = ACCENT_ALPHA_BY_GROUND.get(name, ACCENT_ALPHA)
    return [('text', np.array(WHITE), TEXT_ALPHA), ('accent', rgb(a), alpha), ('accent', rgb(b), alpha)]


def pixel_contrast(img, ink, alpha):
    rgb = img.reshape(-1, 3)
    return ratio(luminance(alpha*ink + (1-alpha)*rgb), luminance(rgb))


# The main drawing covers the heart of the central glow; labels sit around
# it, not on its brightest core. The derivation protects every pixel outside
# this radius (design units from the glow centre); the per-label audit on
# final pixels then checks the real positions, core included.
CORE = 200


@lru_cache(maxsize=64)
def type_area(size, cy=None):
    """Flat mask of probe pixels where type can sit (outside the glow core)."""
    w, h = size
    s = h/1080
    W = w/s
    yy, xx = np.mgrid[0:h, 0:w]
    gx, gy = W/2*s, (cy if cy is not None else 0.5)*1080*0.92*s
    return (((xx+0.5-gx)**2 + (yy+0.5-gy)**2) >= (CORE*s)**2).reshape(-1)


def shortfall(name, tone, default, data, margin=0.05):
    """How far a tone falls below the contrast it must keep, on any probe.

    Every pixel where type can sit must keep the WCAG floor (plus `margin`)
    for each ink or, where the Default design is already below that floor,
    at least the Default's own contrast at that pixel: a level never makes
    weak places weaker. Positive means the tone fails.
    """
    worst = -math.inf
    for size, cy in PROBES:
        img, ref = ground_image(name, tone, size, cy), ground_image(name, default, size, cy)
        area = type_area(size, cy)
        for role, ink, alpha in inks(name, data):
            if role == 'text' and name in RELAX_TEXT:
                continue
            # On relaxed grounds the accents are protected over the glow core too:
            # they are what still has to read there.
            keep = slice(None) if name in RELAX_TEXT else area
            before = pixel_contrast(ref, ink, alpha)[keep]
            need = np.where(before >= CONTRAST_FLOOR[role], CONTRAST_FLOOR[role] + margin, before)
            worst = max(worst, float((need - pixel_contrast(img, ink, alpha)[keep]).max()))
    return worst


def worst_contrast(name, tone, data):
    """Lowest contrast of white type and of the accents where type can sit (all probes)."""
    out = {'text': math.inf, 'accent': math.inf}
    for size, cy in PROBES:
        img = ground_image(name, tone, size, cy)
        area = type_area(size, cy)
        for role, ink, alpha in inks(name, data):
            out[role] = min(out[role], float(pixel_contrast(img, ink, alpha)[area].min()))
    return out


def search(name, default, cost, data):
    """Coarse-to-fine grid search of (sat, light, glow, glow light) minimising
    cost(img, L, C, P); tones that break the contrast caps are skipped."""
    hue, sat, light, glow, glow_light = default
    bounds = ((0.0, 1.0), (0.02, 0.6), (0.04, 0.30), (0.20, 0.70))
    x0, span, best = (sat, light, glow, glow_light), (0.5, 0.15, 0.10, 0.20), None
    for _ in range(5):
        axes = [np.linspace(max(lo, x-d), min(hi, x+d), n)
                for x, d, (lo, hi), n in zip(x0, span, bounds, (9, 9, 5, 5))]
        for x in np.stack(np.meshgrid(*axes, indexing='ij'), -1).reshape(-1, 4):
            img = ground_image(name, (hue, *x))
            c = cost(img, *stats(img))
            if best is not None and c >= best[0]:
                continue
            # The contrast check is the expensive part; only for improvements.
            if shortfall(name, (hue, *x), default, data) > 0:
                continue
            best = (c, *x)
        x0 = best[1:]
        span = tuple(v/3 for v in span)
    return tuple(round(float(v), 3) for v in best[1:])


def settle(name, default, x, toward, data):
    """Round-trip safety: step lightness toward Default until the stored values pass."""
    hue = default[0]
    s, l, g, gl = x
    while shortfall(name, (hue, s, l, g, gl), default, data, margin=0.0) > 0:
        l = round(l + (0.001 if toward > l else -0.001), 3)
    return {'sat': s, 'light': l, 'glow': g, 'glow_light': gl}


def solve_to(name, default, target, data, weights=(4, 4, 0.5)):
    """Tone nearest to a mean OKLab (L, C) and centre prominence P."""
    tl, tc, tp = target
    wc, wl, wp = weights
    x = search(name, default, lambda img, L, C, P: wc*(C-tc)**2 + wl*(L-tl)**2 + wp*(P-tp)**2, data)
    return settle(name, default, x, default[2], data)


def solve_step(name, default, level, step, data):
    """Tone `step` (Delta E) from Default: chroma first, lightness only as
    needed; chroma falls for Muted and rises for Vivid."""
    ref = ground_image(name, default)
    L0, C0, P0 = stats(ref)
    sign = 1 if level == 'vivid' else -1

    def cost(img, L, C, P):
        return (40*(delta_e(img, ref) - step)**2 + 2*(L - L0)**2 + 0.5*(P - P0)**2
                + 100*max(0.0, sign*(C0 - C))**2 + 100*max(0.0, sign*(L0 - L))**2)
    return settle(name, default, search(name, default, cost, data), default[2], data)


def tone_of(name, entry, hue):
    return (hue, entry['sat'], entry['light'], entry['glow'], entry['glow_light'])


def _derive_one(task):
    """Both levels of one ground with equal steps d (see MUTED_CHROMA)."""
    name, data = task
    hue_deg, sat, light = data['palettes'][name][:3]
    hue = hue_deg/360
    default = ground_tone(name, 'default')
    if name in KEEP_GROUND:
        same = {'sat': sat, 'light': light, 'glow': default[3], 'glow_light': default[4]}
        return name, {'muted': same, 'vivid': dict(same)}
    ref = ground_image(name, default)
    L0, C0, P0 = stats(ref)
    de = lambda tone: delta_e(ground_image(name, tone_of(name, tone, hue)), ref)
    muted = solve_to(name, default, (L0, C0*MUTED_CHROMA, P0), data)
    d = de(muted)
    if C0 < 0.015:  # near-neutral (graphite): step by lightness
        # Quiet ground: the step is mostly lightness, chroma follows proportionally.
        dl = math.sqrt(max(0.0, QUIET_STEP**2 - (C0*(1 - MUTED_CHROMA))**2))
        muted = solve_to(name, default, (L0 - dl, C0*MUTED_CHROMA, P0), data, weights=(4, 8, 0.5))
        vivid = solve_to(name, default, (L0 + dl, C0*(2 - MUTED_CHROMA), P0), data, weights=(4, 8, 0.5))
    else:
        vivid = solve_step(name, default, 'vivid', d, data)
        dv = de(vivid)
        if dv < d - STEP_TOLERANCE:
            # Vivid is capped: Muted takes the same shorter step.
            muted = solve_to(name, default, (L0, max(0.0, C0 - dv), P0), data)
    return name, {'muted': muted, 'vivid': vivid}


def derive(data, names=None, jobs=8):
    """Per-ground Muted and Vivid tones: equal steps per ground within the contrast caps."""
    from concurrent.futures import ProcessPoolExecutor
    out = {level: dict(data.get('levels', {}).get(level, {})) for level in RULE}
    tasks = [(name, data) for name in data['palettes'] if not names or name in names]
    with ProcessPoolExecutor(jobs) as pool:
        for name, tones in pool.map(_derive_one, tasks):
            for level, tone in tones.items():
                out[level][name] = tone
            print(f'{name:10} {tones}', flush=True)
    # Palette order, not completion order.
    return {level: {n: out[level][n] for n in data['palettes'] if n in out[level]} for level in RULE}


def table(data):
    """Delta E of each step, mean OKLab change and lowest contrast, per ground x level."""
    rows = []
    for name, (hue_deg, sat, light, *_) in data['palettes'].items():
        hue = hue_deg/360
        default = ground_tone(name, 'default')
        ref = ground_image(name, default)
        L0, C0, _ = stats(ref)
        cells = []
        for level in LEVELS:
            tone = default if level == 'default' else tone_of(name, data['levels'][level][name], hue)
            img = ground_image(name, tone)
            L, C, _ = stats(img)
            w = worst_contrast(name, tone, data)
            cells.append(f'{level[:3]} dE {100*delta_e(img, ref):4.1f} dL {100*(L-L0):+4.1f} dC {100*(C-C0):+4.1f} '
                         f'text {w["text"]:.2f} acc {w["accent"]:.2f}')
        rows.append(f'{name:10} ' + ' | '.join(cells))
    print('\n'.join(rows))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--write', action='store_true', help='re-derive the levels and store them in palettes.json')
    ap.add_argument('--only', help='comma-separated grounds to re-derive (with --write)')
    ap.add_argument('--jobs', type=int, default=8)
    args = ap.parse_args()
    data = palettes()
    if args.write:
        levels = derive(data, set(args.only.split(',')) if args.only else None, args.jobs)
        data['levels'] = dict(data.get('levels', {}), **levels)
        PALETTES_JSON.write_text(json.dumps(data, indent=1, ensure_ascii=False)+'\n')
    table(data)


if __name__ == '__main__':
    main()
