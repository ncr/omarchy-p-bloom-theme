#!/usr/bin/env python3
"""Native p(bloom) sheets: 16:9 5120x2880 and 21:9 5120x2160.

python tools/century/bloom/render.py --ids b01,b02 [--format 16x9|21x9|both]

Composition reuses the Century sheet (same frame, typography, A/B/C view
labels, callouts, legend, field notes, punch line) with the series' own
dossier module per machine. Shared layout code is imported, never edited.
"""
import sys, json, time, argparse, os
from pathlib import Path
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
from sheet import Sheet
from starmap_study import StudySheet
from PIL import Image
from century.render import CenturySheet, callouts
from century import bloom
OUT = ROOT / 'concepts/bloom-ten'
FORMATS = {'16x9': (5120, 2880), '21x9': (5120, 2160)}


# Heavier hierarchy than Century: the outline carries the silhouette at
# desktop distance; detail and shell stay clearly secondary.
STYLES = {
    'A': {'structure': (.94, 1.18), 'detail': (.72, .58), 'shell': (.52, .42),
          'accent': (.92, .78), 'cable': (.74, .58), 'figure': (.90, .85)},
    'side': {'structure': (.92, .98), 'detail': (.72, .54), 'shell': (.50, .40),
             'accent': (.90, .70), 'cable': (.70, .52), 'figure': (.90, .80)},
}
A_FIT = (730, 700)

# New owner-approved grounds (docs/collection/palettes.json). Until the
# shared Sheet knows a name, render with its nearest old alias and say so.
NEAREST_OLD = {'moss': 'olive', 'saffron': 'sand', 'berry': 'wine', 'crimson': 'rust',
               'emerald': 'grass', 'periwinkle': 'indigo', 'sage': 'grass'}


def ground(name):
    from sheet import PALETTES
    if name in PALETTES:
        return name
    old = NEAREST_OLD[name]
    print(f'NOTE: ground {name!r} not yet in sheet.PALETTES; rendering with alias {old!r}', flush=True)
    return old


def draw_view(s, entry, key, cx, cy, width, height):
    import math
    from sheet import WHITE, ARC, GOLD
    from path_cleanup import load, points
    d = load(ROOT / 'tools/assets/century' / (entry['slug'] + '-' + key + '.json'))
    roll = math.radians(entry.get('view_' + key + '_roll', 0))
    if roll:
        def turn(v): return [v[0] * math.cos(roll) - v[1] * math.sin(roll), v[0] * math.sin(roll) + v[1] * math.cos(roll)]
        for path in d['paths']:
            path['points'] = [turn(v) for v in path['points']]
        d['anchors'] = {k: turn(v) for k, v in d.get('anchors', {}).items()}
    pts = [p for path in d['paths'] for p in path['points']]
    x0 = min(x for x, y in pts); x1 = max(x for x, y in pts); y0 = min(y for x, y in pts); y1 = max(y for x, y in pts)
    k = min(width / (x1 - x0), height / (y1 - y0)); ox = (x0 + x1) / 2; oy = (y0 + y1) / 2

    def p(v): return (cx + (v[0] - ox) * k, cy + (v[1] - oy) * k)
    colours = {'accent': ARC, 'cable': GOLD}
    table = STYLES['A' if key == 'A' else 'side']
    # Secondary lines first so the outline is never overdrawn by detail.
    order = {'shell': 0, 'detail': 1, 'cable': 2, 'figure': 3, 'accent': 4, 'structure': 5}
    drawn = []
    for path in sorted(d['paths'], key=lambda q: order.get(q['role'], 1)):
        a, w = table.get(path['role'], (.56, .45))
        pts, closed = points(path)
        s.poly([p(v) for v in pts], a, w, close=closed, color=colours.get(path['role'], WHITE))
        drawn.append([p(v) for v in pts] + ([p(pts[0])] if closed else []))
    if key == 'A':
        # what century.render.callouts needs to keep labels off the drawing
        s._view_A_paths, s._view_A_centre = drawn, cy
    # per-sheet corrections where an exported anchor misses the part it names (century/anchor_shifts.py)
    from century.anchor_shifts import SHIFTS
    shift = SHIFTS.get((entry['slug'], key), {})
    return {name: (lambda q, d=shift.get(name, (0, 0)): (q[0] + d[0] * k, q[1] + d[1] * k))(p(v))
            for name, v in d.get('anchors', {}).items()}


class BloomSheet(CenturySheet):
    def frame(self, sheet_no, total=10, code='NCR'):
        # Same physical frame. The stamp is the permanent NCR id from the
        # registry (three digits, as on Century sheets); no series total,
        # because totals change and NCR numbers never do.
        old = self.text
        ncr = self.entry['ncr']

        def number_text(t, *a, **kw):
            if t == f'{code}-{sheet_no:02d}':
                t = f'{code}-{ncr:03d}'
            if t == f'SHEET {sheet_no:02d} / {total:02d}':
                t = f'SHEET {ncr:03d}'
            return old(t, *a, **kw)
        self.text = number_text
        try:
            StudySheet.frame(self, sheet_no, total, code)
        finally:
            self.text = old


def dossier(s, entry):
    from century.editorial import header, tx
    from collection_layout import field_notes
    from triptych import diagram_y, register_section, punchline
    mod = bloom.module(entry['module'])
    d = mod.DOSSIER
    with s.layer('section'):
        for side, x in (('left', 140), ('right', s.W - 650)):
            y = diagram_y(s, side, 187)
            title, scope, foot = d[side]
            header(s, dict(title=title, scope=scope), x, y, 440)
            mod.figure(s, side, x, y + 39, 440)
            tx(s, foot, x, y + 184, 7, .67)
            register_section(s, side, y - 16, y + 187)
        s.diagram_slots = {'left', 'right'}
        field_notes(s, d)
        punchline(s, d['note'])


def compose(entry, size=(5120, 2160), audit_hook=None):
    Sheet.side_inset = 150 if size[0] / size[1] < 2 else 0
    s = BloomSheet(*size, seed=entry['seed'])
    s.entry = entry
    s.subject = entry['slug']
    s.set_palette(ground(entry['palette']))
    s.background(); s.begin_lines(); s.grid(); s.frame(entry['ncr'], 10)
    if audit_hook:
        audit_hook(s)
    # 16:9 has 360 more design units of height: the A view and its callout
    # columns move down together and tall machines may use the extra height.
    ex = max(0, s.H - 1080)
    mx, my = s.cx - 70, 505 + ex * .28
    s.begin_main(mx, my)
    fw, fh = entry.get('view_A_fit', A_FIT)
    anchors = draw_view(s, entry, 'A', mx, my - 15, fw, fh + ex * .42)
    callouts(s, entry, anchors, mx, my)
    s.end_main()
    if s.wide:
        from triptych import extra, caption_y, measured_illustration
        ex = extra(s); lx = 390; rx = s.W - 405
        with measured_illustration(s, 'left'):
            draw_view(s, entry, 'B', lx, 241 + ex * .225, 370, 290 + ex * .25)
        s.view_label(lx, caption_y(s, 'left'), 'B', entry['view_B'], entry.get('view_B_note'))
        with measured_illustration(s, 'right'):
            draw_view(s, entry, 'C', rx, 241 + ex * .225, 370, 290 + ex * .25)
        s.view_label(rx, caption_y(s, 'right'), 'C', entry['view_C'], entry.get('view_C_note'))
    enabled = [tuple(x) for x in entry['enabled_by']] + [('STILL NEEDED', entry['required_breakthroughs'])]
    for tag, _ in enabled:
        # The legend sets tags at +20 in a 160-unit label column. Composed
        # profiles enlarge the type and Sheet.legend widens that column itself.
        width = 20 + s.measure(tag, 6.5)
        assert s.layer_mode or width < 152, (entry['id'], 'legend tag too long for its column', tag, round(width, 1))
    s.legend(entry['title'], entry['purpose'], entry['narrative'], enabled, entry['service_year'])
    dossier(s, entry)
    s.end_lines()
    return s


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--ids', default='')
    p.add_argument('--format', choices=['16x9', '21x9', 'both'], default='both')
    p.add_argument('--out', default=str(OUT))
    a = p.parse_args()
    ids = [x for x in a.ids.split(',') if x]
    out = Path(a.out)
    for entry in bloom.entries(ids or None):
        assets = ROOT / 'tools/assets/century' / (entry['slug'] + '-meta.json')
        if not assets.exists():
            print('SKIP (not built)', entry['id'], flush=True)
            continue
        for fmt, size in FORMATS.items():
            if a.format not in (fmt, 'both'):
                continue
            t = time.time()
            s = compose(entry, size)
            file = out / fmt / f"{bloom.stem(entry)}.webp"
            file.parent.mkdir(parents=True, exist_ok=True)
            tmp = file.with_name('.' + file.stem + f'.{os.getpid()}.webp')
            s.save(tmp, glow=.15, grain=1.8)
            tmp.replace(file)
            prev = out / 'review' / 'previews'
            prev.mkdir(parents=True, exist_ok=True)
            im = Image.open(file); im.thumbnail((2400, 1400))
            im.convert('RGB').save(prev / f"{bloom.stem(entry)}-{fmt}.jpg", quality=90)
            print('RENDERED', entry['id'], fmt, round(time.time() - t, 2), file.relative_to(ROOT), flush=True)


if __name__ == '__main__':
    main()
