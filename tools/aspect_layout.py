"""Readable compositions for screens other than the two accepted 5K masters.

The accepted masters (5120x2880 and 5120x2160) keep the direct renderer and
must stay byte-identical. Every other profile is composed in two steps:

1. The unchanged sheet renderer draws the usual three-column triptych into a
   transparent *virtual* layer, 2560 design units wide, at `g` pixels per unit.
   The main view and its callouts get their own layer. Type never falls below
   `floor_px` native pixels: `Sheet.readable_size` enlarges it at draw time,
   so every wrap, legend height and caption offset is computed at that size.
2. The layer is cut into measured blocks (main view, B, C, the two diagrams,
   legend, Field Notes, emblem, Easter egg). A template for the profile's
   proportion places whole blocks by integer pixel translation on a new canvas
   that has its own background, grid, frame and sheet number. Blocks are never
   resampled: vectors are rasterised once, at the final pixel scale.

Smaller screens keep fewer secondary blocks rather than shrinking type.
"""
from dataclasses import dataclass, field
import copy
import json
import math
from pathlib import Path

import cairo
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DESIGN_W = 2560


# ---------------------------------------------------------------------------
# collection registry: the 42 retained sheets, in release order
# ---------------------------------------------------------------------------

def collection():
    """Return [{id, title, filename, family, render(size) -> Sheet}] for all 42."""
    import sys
    sys.path.insert(0, str(ROOT/'tools'))
    cat = json.loads((ROOT/'docs/collection/catalog.json').read_text())
    import devices, foibles, leisure
    from order import ORDER
    from starmap import install
    install()
    drawn = dict(devices.SHEETS + leisure.SHEETS + foibles.SHEETS)
    numbered = {f'o{i:02d}': (name, drawn[name]) for i, (name, _) in enumerate(ORDER, 1)}
    entries = {e['number']: e for e in json.loads((ROOT/'docs/century/catalog.json').read_text())}
    from century import bloom
    blooms = {e['id']: e for e in bloom.entries()}
    items = []
    for e in cat['finalized']:
        filename = Path(e['source']).name
        if e['id'].startswith('o'):
            name, fn = numbered[e['id']]
            items.append(dict(id=e['id'], title=e['title'], filename=filename, family='original',
                              render=fn, glow=.28, grain=1.6))
        elif e['id'].startswith('b'):
            # p(bloom) series (tools/century/bloom); same export as its own renderer.
            def render(size, entry=blooms[e['id']]):
                from century.bloom.render import compose
                return compose(entry, size)
            items.append(dict(id=e['id'], title=e['title'], filename=filename, family='bloom',
                              render=render, glow=.15, grain=1.8))
        else:
            entry = entries[int(e['id'][1:])]
            def render(size, entry=entry):
                from century.render import compose
                return compose(entry, size)
            items.append(dict(id=e['id'], title=e['title'], filename=filename, family='century',
                              render=render, glow=.15, grain=1.8))
    assert len(items) == 42
    return items


# ---------------------------------------------------------------------------
# virtual render and block extraction
# ---------------------------------------------------------------------------

@dataclass
class Composition:
    """How one profile renders: virtual scale, type floor and block template."""
    size: tuple            # final pixels
    g: float               # pixels per design unit in the virtual layer and blocks
    virtual_h: float       # virtual layer height in design units (>= 1080)
    floor_px: float        # smallest native type size
    template: str          # key in TEMPLATES
    options: dict = field(default_factory=dict)
    aux_h: float = 0       # virtual height of a second pass supplying larger B/C views

    @property
    def virtual_px(self):
        return (round(DESIGN_W*self.g), round(self.virtual_h*self.g))


def render_virtual(item, comp):
    from sheet import Sheet
    Sheet.composition = comp
    try:
        s = item['render'](comp.virtual_px)
    finally:
        Sheet.composition = None
    s.surface.flush()
    s.main_layer.flush()
    return s


def _alpha(surface):
    w, h = surface.get_width(), surface.get_height()
    stride = surface.get_stride()
    return np.frombuffer(surface.get_data(), np.uint8).reshape(h, stride//4, 4)[:, :w, 3]


def _bbox(alpha, zone):
    """Tight pixel bbox of ink inside zone (x0, y0, x1, y1), or None."""
    h, w = alpha.shape
    x0, y0, x1, y1 = (max(0, math.floor(zone[0])), max(0, math.floor(zone[1])),
                      min(w, math.ceil(zone[2])), min(h, math.ceil(zone[3])))
    if x1 <= x0 or y1 <= y0:
        return None
    sub = alpha[y0:y1, x0:x1] > 0
    if not sub.any():
        return None
    ys = np.flatnonzero(sub.any(axis=1))
    xs = np.flatnonzero(sub.any(axis=0))
    return (x0 + int(xs[0]), y0 + int(ys[0]), x0 + int(xs[-1]) + 1, y0 + int(ys[-1]) + 1)


@dataclass
class Block:
    name: str
    surface: object
    rect: tuple            # layer pixels x0, y0, x1, y1 (tight ink box)
    zone: tuple            # layer pixels the block was searched in

    @property
    def w(self):
        return self.rect[2]-self.rect[0]

    @property
    def h(self):
        return self.rect[3]-self.rect[1]


def extract(s):
    """Cut the virtual layers into blocks. Zones follow the triptych metadata."""
    k = s.s
    W, H = s.W, s.H
    side = _alpha(s.surface)
    main = _alpha(s.main_layer)
    left_div = s.section_layout['left']['divider']
    right_div = s.section_layout['right']['divider']
    fx0, fy0, fx1, fy1 = s.field_notes_bounds
    from collection_layout import signature_box
    ex, ey, er = signature_box(s)
    LEFT, RIGHT = 780, W-780
    zones = {
        'B': (0, 0, LEFT, left_div-4),
        'left_diagram': (0, left_div-4, LEFT, s.legend_top-14),
        'legend': (0, s.legend_top-14, LEFT, H),
        'C': (RIGHT, 0, W, right_div-4),
        'right_diagram': (RIGHT, right_div-4, W, fy0-4),
        'notes': (RIGHT, fy0-4, ex-er-12, H),
        'emblem': (ex-er-12, fy0-4, W, H),
        'punchline': (LEFT, H-110, RIGHT, H),
    }
    blocks = {}
    for name, z in zones.items():
        zp = tuple(v*k for v in z)
        box = _bbox(side, zp)
        if box:
            blocks[name] = Block(name, s.surface, box, zp)
    box = _bbox(main, (0, 0, main.shape[1], main.shape[0]))
    blocks['main'] = Block('main', s.main_layer, box, (0, 0, main.shape[1], main.shape[0]))
    # Anything outside the zones would be silently lost: report it.
    covered = np.zeros_like(side, dtype=bool)
    for b in blocks.values():
        if b.surface is s.surface:
            x0, y0, x1, y1 = b.rect
            covered[y0:y1, x0:x1] = True
    orphan = (side > 0) & ~covered
    s.orphan_pixels = int(orphan.sum())
    if s.orphan_pixels:
        ys, xs = np.nonzero(orphan)
        s.orphan_box = (int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1)
    return blocks


# ---------------------------------------------------------------------------
# final canvas
# ---------------------------------------------------------------------------

def _native(s, size, unit):
    """Switch the sheet to the final canvas: background, grid and frame."""
    s.layer_mode = False
    w, h = size
    s.px = size
    s.s = unit
    s.W, s.H = w/unit, h/unit
    s.cx = s.W/2
    s.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    s.c = cairo.Context(s.surface)
    s.c.scale(unit, unit)
    s.c.set_line_cap(cairo.LINE_CAP_BUTT)
    s.c.set_line_join(cairo.LINE_JOIN_MITER)
    for key in ('_bg', '_bg_surface', '_lines'):
        s.__dict__.pop(key, None)


def compose(item, comp, fixed=None):
    """See _compose; retries with a compact legend if the main view cannot fit."""
    if fixed is None and not comp.options:
        from dataclasses import replace
        for level in (None, 'compact', 'minimal'):
            try:
                s = _compose(item, replace(comp, options={'legend': level} if level else {}))
                s.fallback = level and f'{level} legend'
                return s
            except LayoutError:
                if level == 'minimal':
                    raise
    return _compose(item, comp, fixed)


def _compose(item, comp, fixed=None):
    """Render one sheet for a composed profile; returns the finished sheet.

    fixed: {block: (tx, ty)} pixel translations from an earlier render. The
    geometry-only audit uses it so that both renders share one placement.
    """
    s = render_virtual(item, comp)
    blocks = extract(s)
    for t in s.text_boxes:
        t['surface'] = s.main_layer if t['layer'] == 'main' else s.surface
    layer_boxes = s.text_boxes
    if comp.aux_h and comp.aux_h != comp.virtual_h:
        # B and C from a taller virtual sheet: the same drawings, larger,
        # so their enlarged labels keep clear of the geometry.
        from dataclasses import replace
        s2 = render_virtual(item, replace(comp, virtual_h=comp.aux_h))
        tall = extract(s2)
        for name in ('B', 'C'):
            blocks.pop(name, None)
            if name in tall:
                blocks[name] = tall[name]
        for t in s2.text_boxes:
            if t['layer'] == 'side':
                t['surface'] = s2.surface
                layer_boxes.append(t)
        s.aux_sheet = s2
    virtual = dict(W=s.W, H=s.H, s=s.s)
    sheet_no, total, code, rng = s.frame_call
    unit = comp.g
    if fixed is None:
        # Frame furniture first, on its own layer: blocks must clear it.
        _native(s, comp.size, unit)
        s.text_floor = comp.floor_px/unit
        s.text_boxes = None
        s.rng = copy.deepcopy(rng)
        s.inset = 0
        type(s).frame(s, sheet_no, total, code)
        s.surface.flush()
        frame_alpha = _alpha(s.surface).copy()
        placer, native = TEMPLATES[comp.template](s, blocks, comp, frame_alpha)
        shift = {n: (dx-blocks[n].rect[0], dy-blocks[n].rect[1], blocks[n].rect) for n, (dx, dy) in placer.place.items()}
        dropped = placer.dropped
        holes = (placer.holes(), placer.q)
    else:
        shift, native, dropped, holes = fixed['shift'], fixed['native'], fixed['dropped'], fixed['holes']
    _native(s, comp.size, unit)
    s.text_floor = comp.floor_px/unit
    s.cy = native.get('cy', s.H/2)
    s.background()
    s.begin_lines()
    s.grid()
    s.rng = copy.deepcopy(rng)
    s.inset = 0
    s.text_boxes = []
    type(s).frame(s, sheet_no, total, code)
    s.surface.flush()
    s.base = np.frombuffer(s.surface.get_data(), np.uint8).reshape(comp.size[1], -1, 4)[:, :comp.size[0], :3].copy()
    c = s.c
    for name, (tx, ty, rect) in shift.items():
        if name not in blocks:
            continue  # e.g. a text-only block in the geometry-only audit
        b = blocks[name]
        x0, y0, x1, y1 = rect
        c.save()
        c.identity_matrix()
        c.rectangle(x0+tx, y0+ty, x1-x0, y1-y0)
        c.clip()
        c.set_source_surface(b.surface, tx, ty)
        if name == 'main':
            c.mask_surface(_keep_mask(holes, comp.size), 0, 0)
        else:
            c.paint()
        c.restore()
    s.surface.flush()
    s.shift, s.native, s.dropped, s.blocks, s.holes = shift, native, dropped, blocks, holes
    s.virtual = virtual
    s.comp = comp
    s.fallback = None
    s.layer_boxes = layer_boxes
    s.canvas_boxes = s.text_boxes
    s.end_lines()
    return s


def _keep_mask(holes, size):
    """A8 mask: opaque everywhere except the hole cells."""
    grid, q = holes
    w, h = size
    keep = np.repeat(np.repeat(~grid, q, axis=0), q, axis=1)[:h, :w]
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_A8, w)
    buf = np.zeros((h, stride), np.uint8)
    buf[:, :w] = keep*255
    return cairo.ImageSurface.create_for_data(buf, cairo.FORMAT_A8, w, h, stride)


# Identifiers deliberately printed on their own filled symbols (as in
# verify_wallpaper_layout.py); nothing else may touch drawn geometry.
INSIDE_OWN_SYMBOL = {
    'air-refinery': {'AIR', 'CONTACTOR', 'WATER', 'ELECTROLYSER', 'SUNLIGHT', 'RECEIVER',
                     'ENZYME BEDS', 'CATALYST BEDS', 'JET FUEL'},
    'truth-lamp': {'14', '9', '0', '22', '17', '11'},
    'organ-foundry': {'1', '2', '3', '4', '5', '6'},
    'proxy': {'114', 'CITY 10K'},
}


def canvas_texts(s):
    """Every label of a composed sheet in final canvas pixels, and clipping issues."""
    issues = []
    texts = []
    for t in s.layer_boxes:
        x0, y0, x1, y1 = t['box']
        cx, cy = (x0+x1)/2, (y0+y1)/2
        owner = None
        for name, (tx, ty, _) in s.shift.items():
            b = s.blocks[name]
            if b.surface is not t['surface']:
                continue
            r = b.rect
            if r[0] <= cx <= r[2] and r[1] <= cy <= r[3]:
                owner = name
                over = max(r[0]-x0, r[1]-y0, x1-r[2], y1-r[3])
                if over > 1.5:
                    issues.append(f'clipped text in {name} by {over:.1f}px: {t["text"]}')
                texts.append(dict(t, block=name, box=[x0+tx, y0+ty, x1+tx, y1+ty]))
                break
    texts += [dict(t, block='frame') for t in s.canvas_boxes]
    return texts, issues


def audit(item, comp, s=None):
    """Collision/readability report for one composed sheet (final pixels)."""
    from sheet import Sheet
    import ground_levels
    s = s or compose(item, comp)
    w, h = comp.size
    boxes = []
    texts, issues = canvas_texts(s)
    level = Sheet.ground_level
    contrast = ground_levels.text_contrast(
        texts, ground_levels.bgra_rgb(s._bg, w, h),
        None if level == 'default' else ground_levels.reference_ground(s))
    issues += ground_levels.contrast_issues(contrast, getattr(s, 'ground', None))
    # Geometry without type, same placement.
    Sheet.draw_text = False
    try:
        g = _compose(item, getattr(s, 'comp', comp), fixed=dict(shift=s.shift, native=s.native, dropped=s.dropped, holes=s.holes))
    finally:
        Sheet.draw_text = True
    arr = np.frombuffer(g.surface.get_data(), np.uint8).reshape(h, -1, 4)[:, :w, :3]
    mask = np.abs(arr.astype(np.int16)-g.base.astype(np.int16)).max(axis=2) > 5
    # the top strip stays plain paper so Omarchy's see-through bar is readable over every set
    # (visible ink only: faint construction lines a few levels above the ground do not hurt the bar)
    strip = math.ceil(.03*h)
    ink = np.abs(arr[:strip].astype(np.int16)-g.base[:strip].astype(np.int16)).max(axis=2) > 24
    if ink.sum() > 20:
        ys, xs = np.nonzero(ink)
        issues.append(f'ink in the top bar strip ({len(xs)}px, x {xs.min()}-{xs.max()}, y {ys.min()}-{ys.max()})')
    for t in texts:
        if t['box'][1] < strip:
            issues.append(f'text in the top bar strip: {t["text"]}')
    small = [t for t in texts if t['font_px'] < comp.floor_px-.01]
    for t in small:
        issues.append(f'type below floor: {t["text"]} {t["font_px"]:.1f}px')
    own = INSIDE_OWN_SYMBOL.get(getattr(s, 'subject', ''), set())
    grid, q = s.holes
    for t in texts:
        if t['block'] == 'main':
            x0, y0, x1, y1 = t['box']
            if grid[max(0, int(y0//q)):math.ceil(y1/q), max(0, int(x0//q)):math.ceil(x1/q)].any():
                issues.append(f'main-view text cut by a construction-line gap: {t["text"]}')
    for t in texts:
        x0, y0, x1, y1 = t['box']
        if x0 < 0 or y0 < 0 or x1 > w or y1 > h:
            issues.append(f'outside canvas: {t["text"]}')
            continue
        hits = int(mask[math.floor(y0):math.ceil(y1), math.floor(x0):math.ceil(x1)].sum())
        if hits and t['text'] not in own:
            issues.append(f'text on geometry ({hits}px) in {t["block"]}: {t["text"]}')
            boxes.append(t['box'])
    for i, a in enumerate(texts):
        for b in texts[i+1:]:
            if a['box'][0] < b['box'][2] and a['box'][2] > b['box'][0] and a['box'][1] < b['box'][3] and a['box'][3] > b['box'][1]:
                issues.append(f'text overlap: {a["text"]} / {b["text"]}')
                boxes.append(a['box'])
    letters = {k: sum(t['text'] == k for t in texts) for k in 'ABC'}
    want = {'A': 1, 'B': int('B' in s.shift), 'C': int('C' in s.shift)}
    for k in 'ABC':
        if letters[k] != want[k]:
            issues.append(f'view letter {k}: {letters[k]} (expected {want[k]})')
    for need in ('main', 'legend', 'punchline'):
        if need not in s.shift:
            issues.append(f'missing {need}')
    if s.orphan_pixels:
        issues.append(f'unassigned ink {s.orphan_pixels}px at {s.orphan_box}')
    return dict(id=item['id'], size=list(comp.size), template=comp.template,
                blocks=sorted(s.shift), dropped=s.dropped, fallback=s.fallback,
                min_text_px=round(min(t['font_px'] for t in texts), 2), issues=issues,
                ground=getattr(s, 'ground', None), level=level,
                contrast=ground_levels.summary(contrast),
                issue_boxes=[[round(v) for v in b] for b in boxes]), s


# ---------------------------------------------------------------------------
# placement: whole blocks, integer pixels, no overlap of inked areas
# ---------------------------------------------------------------------------

class Placer:
    """Greedy block placement on a coarse occupancy grid of the final canvas.

    A block is accepted where its own inked cells (dilated by `gap` units)
    miss everything already placed and it stays inside the safe area.
    """

    def __init__(self, comp, blocks, unit):
        self.comp, self.blocks, self.unit = comp, blocks, unit
        w, h = comp.size
        self.q = max(2, round(4*unit))          # pixels per cell, about 4 units
        self.shape = (math.ceil(h/self.q)+1, math.ceil(w/self.q)+1)
        self.occ = np.zeros(self.shape, bool)
        self.W, self.H = w/unit, h/unit
        self.place = {}
        self.frame_occ = np.zeros(self.shape, bool)
        self.dropped = []
        self._masks = {}

    def reserve_top(self, frac=.035):
        """Keep the top strip plain paper: Omarchy's see-through bar sits there."""
        self.reserve(0, 0, self.W, self.H*frac)

    def reserve_mask(self, alpha, gap=8):
        """Frame furniture (already drawn natively) that blocks must clear."""
        q = self.q
        h, w = alpha.shape
        hh, ww = self.shape
        pad = np.zeros((hh*q, ww*q), bool)
        pad[:h, :w] = alpha > 12
        cells = pad.reshape(hh, q, ww, q).any(axis=(1, 3))
        d = max(1, round(gap*self.unit/q))
        out = cells.copy()
        for dy in range(-d, d+1):
            for dx in range(-d, d+1):
                out |= np.roll(np.roll(cells, dy, 0), dx, 1)
        self.frame_occ = out

    def reserve(self, x0, y0, x1, y1):
        q, u = self.q, self.unit
        self.occ[max(0, int(y0*u//q)):max(0, math.ceil(y1*u/q)), max(0, int(x0*u//q)):max(0, math.ceil(x1*u/q))] = True

    def mask(self, name, gap):
        key = (name, gap)
        if key not in self._masks:
            b = self.blocks[name]
            x0, y0, x1, y1 = b.rect
            # The main view's faint registration and datum lines do not block
            # other blocks; they are cut back around them instead (holes()).
            a = _alpha(b.surface)[y0:y1, x0:x1] > (64 if name == 'main' else 3)
            q = self.q
            hh, ww = math.ceil(a.shape[0]/q), math.ceil(a.shape[1]/q)
            pad = np.zeros((hh*q, ww*q), bool)
            pad[:a.shape[0], :a.shape[1]] = a
            cells = pad.reshape(hh, q, ww, q).any(axis=(1, 3))
            d = max(0, round(gap*self.unit/q))
            out = np.zeros((hh+2*d, ww+2*d), bool)
            for dy in range(-d, d+1):
                for dx in range(-d, d+1):
                    if dx*dx+dy*dy <= d*d+d:
                        out[d+dy:d+dy+hh, d+dx:d+dx+ww] |= cells
            self._masks[key] = (out, d)
        return self._masks[key]

    def free(self, name, x, y, gap):
        """x, y: top-left of the block's rect in canvas units."""
        b = self.blocks[name]
        u, q = self.unit, self.q
        if x < 0 or y < 0 or (x*u+b.w) > self.comp.size[0] or (y*u+b.h) > self.comp.size[1]:
            return False
        m, d = self.mask(name, gap)
        cx, cy = round(x*u/q)-d, round(y*u/q)-d
        H, W = self.shape
        y0, x0 = max(0, cy), max(0, cx)
        y1, x1 = min(H, cy+m.shape[0]), min(W, cx+m.shape[1])
        if y1 <= y0 or x1 <= x0:
            return False
        if (self.occ[y0:y1, x0:x1] & m[y0-cy:y1-cy, x0-cx:x1-cx]).any():
            return False
        m0, d0 = self.mask(name, 0)
        cx, cy = cx+d-d0, cy+d-d0
        y0, x0 = max(0, cy), max(0, cx)
        y1, x1 = min(H, cy+m0.shape[0]), min(W, cx+m0.shape[1])
        return not (self.frame_occ[y0:y1, x0:x1] & m0[y0-cy:y1-cy, x0-cx:x1-cx]).any()

    def commit(self, name, x, y):
        b = self.blocks[name]
        u, q = self.unit, self.q
        m, d = self.mask(name, 0)
        cx, cy = round(x*u/q), round(y*u/q)
        H, W = self.shape
        y1, x1 = min(H, cy+m.shape[0]), min(W, cx+m.shape[1])
        self.occ[cy:y1, cx:x1] |= m[:y1-cy, :x1-cx]
        self.place[name] = (round(x*u), round(y*u))

    def put(self, name, candidates, gap=22, required=False, slide=(), step=6, reach=400, force=False):
        """Try candidate top-left positions (units), each also slid along axes."""
        if name not in self.blocks:
            return None
        if force:
            self.commit(name, *candidates[0])
            return candidates[0]
        tries = []
        for x, y in candidates:
            tries.append((x, y))
            for k in range(1, int(reach/step)+1):
                for axis, sign in slide:
                    off = sign*k*step
                    tries.append((x+off, y) if axis == 'x' else (x, y+off))
        for x, y in tries:
            if self.free(name, x, y, gap):
                self.commit(name, x, y)
                return (x, y)
        if required:
            raise LayoutError(f'{name} does not fit')
        self.dropped.append(name)
        return None

    def holes(self, gap=6):
        """Cells where faint main-view construction lines must not continue:
        around every other placed block and the frame furniture.

        gap must stay below the main view's placement gap, so that only faint
        lines (never its strong ink or type) can fall inside a hole."""
        u, q = self.unit, self.q
        H, W = self.shape
        out = self.frame_occ.copy()
        for name, (px, py) in self.place.items():
            if name == 'main':
                continue
            m, d = self.mask(name, gap)
            cx, cy = round(px/q)-d, round(py/q)-d
            y0, x0 = max(0, cy), max(0, cx)
            y1, x1 = min(H, cy+m.shape[0]), min(W, cx+m.shape[1])
            out[y0:y1, x0:x1] |= m[y0-cy:y1-cy, x0-cx:x1-cx]
        return out

    def size(self, name):
        b = self.blocks[name]
        return b.w/self.unit, b.h/self.unit

    def virtual(self, name):
        b = self.blocks[name]
        return b.rect[0]/self.unit, b.rect[1]/self.unit


class LayoutError(Exception):
    pass


def triptych_template(s, blocks, comp, frame_alpha):
    """The master's three columns, re-flowed for another width and height."""
    P = Placer(comp, blocks, comp.g)
    P.reserve_mask(frame_alpha)
    P.reserve_top()
    W, H = P.W, P.H
    dx = (W-DESIGN_W)
    Hv = s.H if False else comp.virtual_h
    dy = H-Hv
    def at(name, shift_x=0.0, shift_y=0.0):
        x, y = P.virtual(name)
        return (x+shift_x, y+shift_y)
    P.put('legend', [at('legend', 0, dy)], required=True)
    P.put('main', [at('main', dx/2)], required=True, gap=12,
          slide=[('x', 1), ('y', -1), ('x', -1)], step=4, reach=200)
    P.put('punchline', [at('punchline', dx/2, dy)], required=True, gap=14, slide=[('x', 1), ('x', -1)])
    P.put('emblem', [at('emblem', dx, dy)], slide=[('y', -1)])
    P.put('notes', [at('notes', dx, dy)], slide=[('x', -1), ('y', -1)])
    P.put('B', [at('B')], slide=[('y', -1), ('y', 1), ('x', -1)])
    P.put('C', [at('C', dx)], slide=[('y', -1), ('y', 1), ('x', 1)])
    P.put('left_diagram', [at('left_diagram', 0, dy/2)], slide=[('y', 1), ('y', -1)])
    P.put('right_diagram', [at('right_diagram', dx, dy/2)], slide=[('y', 1), ('y', -1)])
    return P, dict(cy=(P.place['main'][1]+blocks['main'].h/2)/comp.g)


def _common(s, blocks, comp, frame_alpha):
    P = Placer(comp, blocks, comp.g)
    P.reserve_mask(frame_alpha)
    P.reserve_top()
    dx, dy = P.W-DESIGN_W, P.H-comp.virtual_h
    def at(name, shift_x=0.0, shift_y=0.0):
        x, y = P.virtual(name)
        return (x+shift_x, y+shift_y)
    return P, dx, dy, at


def _finish(P, blocks, comp):
    x, y = P.place['main']
    return P, dict(cy=(y+blocks['main'].h/2)/comp.g)


def _under_main(P, name, dy_virtual):
    """Easter egg on the physical bottom axis of the main view."""
    mx = P.place['main'][0]/P.unit + P.size('main')[0]/2
    x, y = P.virtual(name)
    return (mx-P.size(name)[0]/2, y+dy_virtual)


ANY = [('y', -1), ('y', 1), ('x', -1), ('x', 1)]


def duo_template(s, blocks, comp, frame_alpha):
    """1080p-class landscape: the main view with the left column's dossier.

    The main view moves right; B, its diagram and the legend keep the left
    column. Right-column blocks appear only where they genuinely fit.
    """
    P, dx, dy, at = _common(s, blocks, comp, frame_alpha)
    W, H = P.W, P.H
    P.put('legend', [at('legend', 0, dy)], required=True)
    mw = P.size('main')[0]
    x0 = at('main')[0]
    P.put('main', [(W-58-mw, at('main')[1]+dy*.35)], required=True, gap=12,
          slide=[('x', -1), ('y', -1), ('y', 1)], step=4, reach=260)
    P.put('punchline', [_under_main(P, 'punchline', dy)], required=True, gap=14,
          slide=[('x', -1), ('x', 1)])
    P.put('emblem', [at('emblem', dx, dy)], slide=[('y', -1), ('x', -1)])
    P.put('B', [at('B')], slide=[('y', 1), ('x', -1)])
    P.put('notes', [at('notes', dx, dy)], slide=[('x', -1), ('y', -1)])
    P.put('left_diagram', [at('left_diagram', 0, dy/2)], slide=[('y', 1), ('y', -1)])
    P.put('C', [at('C', dx)], slide=[('y', 1), ('x', 1)])
    P.put('right_diagram', [at('right_diagram', dx, dy/2)], slide=[('y', 1), ('y', -1)])
    return _finish(P, blocks, comp)


def stacked_template(s, blocks, comp, frame_alpha):
    """4:3 and squarer: main view above, dossier band below it."""
    P, dx, dy, at = _common(s, blocks, comp, frame_alpha)
    W, H = P.W, P.H
    mw, mh = P.size('main')
    P.put('legend', [at('legend', 0, dy)], required=True)
    P.put('main', [((W-mw)/2, at('main')[1]+max(0, dy)*.12)], required=True, gap=12,
          slide=[('x', 1), ('y', -1), ('x', -1)], step=4, reach=200)
    P.put('punchline', [at('punchline', dx/2, dy)], required=True, gap=14,
          slide=[('x', 1), ('x', -1)])
    P.put('emblem', [at('emblem', dx, dy)], slide=[('y', -1), ('x', -1)])
    P.put('notes', [at('notes', dx, dy)], slide=[('y', -1), ('x', -1)])
    lx1 = P.place['legend'][0]/P.unit+P.size('legend')[0]
    rx0 = (P.place['notes'][0]/P.unit) if 'notes' in P.place else W-260
    band = lambda name: ((lx1+rx0)/2-P.size(name)[0]/2, H-96-P.size(name)[1])
    P.put('B', [at('B'), band('B')], slide=[('y', 1), ('x', 1), ('y', -1)])
    P.put('C', [at('C', dx), band('C')], slide=[('y', 1), ('x', -1), ('y', -1)])
    P.put('left_diagram', [at('left_diagram', 0, dy/2), band('left_diagram')], slide=[('y', 1), ('y', -1)])
    P.put('right_diagram', [at('right_diagram', dx, dy/2), band('right_diagram')], slide=[('y', 1), ('y', -1)])
    return _finish(P, blocks, comp)


def panorama_template(s, blocks, comp, frame_alpha):
    """32:9: five columns. Diagrams over the dossiers, B and C beside A."""
    P, dx, dy, at = _common(s, blocks, comp, frame_alpha)
    W, H = P.W, P.H
    mw, mh = P.size('main')
    P.put('legend', [at('legend', 0, dy)], required=True)
    P.put('main', [((W-mw)/2, at('main')[1]+dy*.35)], required=True, gap=12,
          slide=[('x', 1), ('y', -1), ('x', -1)], step=4, reach=200)
    P.put('punchline', [at('punchline', dx/2, dy)], required=True, gap=14, slide=[('x', 1), ('x', -1)])
    P.put('emblem', [at('emblem', dx, dy)], slide=[('y', -1)])
    P.put('notes', [at('notes', dx, dy)], slide=[('x', -1), ('y', -1)])
    top = 108
    P.put('left_diagram', [(at('left_diagram')[0], top)], slide=[('y', 1)])
    P.put('right_diagram', [(at('right_diagram', dx)[0], top)], slide=[('y', 1)])
    main_x0 = P.place['main'][0]/P.unit
    main_x1 = main_x0+mw
    outer_l = max(P.place['legend'][0]/P.unit+P.size('legend')[0],
                  at('left_diagram')[0]+P.size('left_diagram')[0])
    outer_r = min(at('right_diagram', dx)[0], at('notes', dx)[0])
    bw, bh = P.size('B')
    cw, ch = P.size('C')
    P.put('B', [((outer_l+main_x0)/2-bw/2, (H-bh)/2-40)], slide=ANY)
    P.put('C', [((main_x1+outer_r)/2-cw/2, (H-ch)/2-40)], slide=ANY)
    return _finish(P, blocks, comp)


TEMPLATES = {'triptych': triptych_template, 'duo': duo_template,
             'stacked': stacked_template, 'panorama': panorama_template}


def floor_px(w, h):
    """Smallest native type: 11 px, or the 5K master's 14 px per 2880 rows."""
    return max(11.0, round(14*h/2880, 2))


# id, aspect family, size, template, px per design unit, canvas height in units
MATRIX = [
    ('16x9-1080p', '16:9', (1920, 1080), 'duo', 1.0),
    ('16x9-1440p', '16:9', (2560, 1440), 'triptych', 1.0),
    ('16x9-2160p', '16:9', (3840, 2160), 'triptych', 1.5),
    ('16x10-1200p', '16:10', (1920, 1200), 'duo', 1.0),
    ('16x10-1600p', '16:10', (2560, 1600), 'triptych', 1.0),
    ('16x10-2400p', '16:10', (3840, 2400), 'triptych', 1.5),
    ('3x2-1504p', '3:2', (2256, 1504), 'duo', 1.0),
    ('3x2-1920p', '3:2', (2880, 1920), 'triptych', 1.125),
    ('4x3-1200p', '4:3', (1600, 1200), 'stacked', 1.0),
    ('4x3-1536p', '4:3', (2048, 1536), 'stacked', 1.1),
    ('64x27-1080p', '21:9', (2560, 1080), 'triptych', 1.0),
    ('43x18-1440p', '21:9', (3440, 1440), 'triptych', 1.344),
    ('12x5-1600p', '21:9', (3840, 1600), 'triptych', 1.5),
    ('32x9-1080p', '32:9', (3840, 1080), 'panorama', 1.0),
    ('32x9-1440p', '32:9', (5120, 1440), 'panorama', 4/3),
    ('32x9-2160p', '32:9', (7680, 2160), 'panorama', 2.0),
]
# The accepted native masters: direct renderer, byte-identical, not composed.
MASTERS = [
    ('16x9-2880p', '16:9', (5120, 2880)),
    ('64x27-2160p', '21:9', (5120, 2160)),
]


def composition(profile_id):
    for pid, family, size, template, g in MATRIX:
        if pid == profile_id:
            h_units = size[1]/g
            vh = 1080 if template in ('duo', 'stacked', 'panorama') else max(1080, h_units)
            # B and C come from a taller virtual sheet (larger drawings).
            aux = 1800 if template == 'panorama' else max(vh+160, 1440)
            return Composition(size, g, vh, floor_px(*size), template, aux_h=aux)
    raise KeyError(profile_id)
