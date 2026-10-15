#!/usr/bin/env python3
"""Typography eval for the side diagrams of every wallpaper (deterministic layer).

    python3 tools/eval_wallpapers.py                     # all 42 sheets, 16:9 2160p layout
    python3 tools/eval_wallpapers.py --only b03,c065     # some sheets
    python3 tools/eval_wallpapers.py --cases             # score against docs/collection/eval-cases.json
    python3 tools/eval_wallpapers.py --json out.json     # findings as JSON

It renders each sheet once (virtual layers, as the composed profiles do), takes the text and
rectangle boxes the renderer records, and checks what the layout audit cannot see:

  box-centre     text inside a frame is optically off-centre (pushed right, or high/low)
  box-index      a small label floats just above a frame's corner instead of belonging to it
  near-align     sibling labels almost share a left edge, right edge or baseline (a 0.4-3 unit miss)
  schema         heading / subtitle / caption missing, or not on the diagram's common left edge
  caption-gap    other ink crowds the caption line
  detached       a short value sits far across the block from the label on its line
  edge           a label is flush against the column boundary next to the main drawing

and, across the whole sheet (zone "sheet"):

  widow          a wrapped paragraph ends on one word
  glyph          "4 x 4" for ×, a hyphen for a minus, H2 / P0 / OMEGA0 without sub/superscripts, US -ize spelling
  repeat         the same three-word phrase in two different blocks (a note that repeats a callout, a caption
                 that repeats the subtitle)

Units are design units (1080 per sheet height). Findings are advice for a human eye, not a gate:
the judge layer (a model with the owner's taste rubric) looks at what geometry alone cannot.
The eval is scored on labelled cases from real reviews (docs/collection/eval-cases.json): every
case must be found on the version it was written for, and must be gone once fixed.
"""
import argparse
import json
from pathlib import Path
import re
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
CASES = ROOT/'docs/collection/eval-cases.json'
ZONES = ('left_diagram', 'right_diagram')


def inside(t, r, tol=0.5):
    return t[0] >= r[0]-tol and t[1] >= r[1]-tol and t[2] <= r[2]+tol and t[3] <= r[3]+tol


def centre(b):
    return ((b[0]+b[2])/2, (b[1]+b[3])/2)


STOP = set('A AN THE OF AND TO IN ON FOR IS ARE WITH PER AT BY FROM AS OR IT ITS INTO ONE TWO'.split())
GLYPHS = [
    (r'\d\s?x\s?\d', 'an x between numbers; use ×'),
    (r'(^|[\s(=])-\d', 'a hyphen as a minus sign; use −'),
    (r'\b(?:[A-Za-z]|OMEGA|omega)0\b', 'a zero written inline; use a subscript (P₀)'),
    (r'\b(?:H2O?|O2|CO2|N2|CH4|NH3|Fe2O3|SO2)\b', 'a chemical formula without subscripts'),
    (r'\b(?:OMEGA(?! CENTAURI)|omega|PI|SQUARED)\b|\b(?:ROOT|root)\(', 'a symbol spelled out (ω, π, ², √)'),
    (r'(?i)\b(?!(?:size|sized|sizes|prize|seize|seized|capsize|resize|oversize|downsize)\b)[a-z]{3,}iz(?:e|ed|es|er|ers|ing|ation|ations)\b',
     'US -ize spelling; the collection is British (-ise)'),
]


def whole_sheet(item, s, blocks, wraps):
    """Checks across every block of one sheet: widows, glyph lint, phrases repeated between blocks."""
    out = []
    add = lambda code, msg, text=None: out.append(dict(id=item['id'], zone='sheet', code=code, msg=msg, text=text))
    for lines in wraps:
        if len(lines) > 1 and ' ' not in lines[-1].strip():
            add('widow', f'paragraph ends on one word: "… {lines[-2][-30:]} / {lines[-1]}"', lines[-1])
    texts = [t for t in (s.text_boxes or []) if t.get('text')]
    seen = set()
    for t in texts:
        for pat, why in GLYPHS:
            m = re.search(pat, t['text'])
            if m and (t['text'], why) not in seen:
                seen.add((t['text'], why))
                add('glyph', f'{why}: "{t["text"]}"', t['text'])
    # which block each line of text belongs to (the main view's callouts are on their own layer)
    def block_of(t):
        if t.get('layer') == 'main':
            return 'main'
        c = centre(t['box'])
        for name, b in blocks.items():
            z = getattr(b, 'zone', None) or b.rect
            if name != 'main' and z[0] <= c[0] <= z[2] and z[1] <= c[1] <= z[3]:
                return name
        return None
    phrases = {}
    for t in texts:
        name = block_of(t)
        if not name or name == 'emblem':
            continue
        words = [w for w in re.findall(r"[A-Za-z0-9°²³₀-₉%.'’-]+", t['text'].upper()) if w not in STOP and w.strip('.-')]
        for i in range(len(words)-2):
            phrases.setdefault(' '.join(words[i:i+3]).rstrip('.'), set()).add(name)
    reported = set()
    for ph, names in sorted(phrases.items()):
        if len(names) > 1:
            key = tuple(sorted(names))
            if (key, ph[:12]) in reported:
                continue
            reported.add((key, ph[:12]))
            add('repeat', f'"{ph}" in {" and ".join(key)}', ph)
    return out


def sheet_findings(item, comp):
    import aspect_layout as A
    import numpy as np
    from sheet import Sheet
    wraps, wrap = [], Sheet.wrap
    def logged(self, *a, **kw):
        lines = wrap(self, *a, **kw)
        wraps.append(lines)
        return lines
    Sheet.wrap = logged
    try:
        s = A.render_virtual(item, comp)
    finally:
        Sheet.wrap = wrap
    blocks = A.extract(s)
    k = s.s                                   # layer pixels per design unit
    u = lambda v: v/k
    alpha = A._alpha(s.surface)
    texts = [t for t in (s.text_boxes or []) if t.get('layer') == 'side']
    shapes = [r for r in (getattr(s, 'shape_boxes', None) or []) if r['layer'] == 'side']
    out = whole_sheet(item, s, blocks, wraps)
    for zone_name in ZONES:
        if zone_name not in blocks:
            continue
        z = blocks[zone_name].zone
        zt = sorted([t for t in texts if z[0] <= centre(t['box'])[0] <= z[2] and z[1] <= centre(t['box'])[1] <= z[3]],
                    key=lambda t: (t['box'][1], t['box'][0]))
        zs = [r for r in shapes if z[0] <= centre(r['box'])[0] <= z[2] and z[1] <= centre(r['box'])[1] <= z[3]]
        side = zone_name.split('_')[0]
        def add(code, msg, t=None):
            out.append(dict(id=item['id'], zone=side, code=code, msg=msg, text=t['text'] if t else None))
        if not zt:
            add('schema', 'no text in the diagram')
            continue
        # -- schema: heading, subtitle under it, caption last, one left edge
        head = zt[0]
        cap = max(zt, key=lambda t: t['box'][3])
        sub = next((t for t in zt[1:] if t is not cap and abs(u(t['box'][0]-head['box'][0])) < 2), None)
        for t in zt:
            if u(head['box'][0]-t['box'][0]) > 1:
                add('schema', f'"{t["text"]}" sticks out {u(head["box"][0]-t["box"][0]):.1f}u left of the heading\'s edge', t)
        if not sub or u(sub['box'][1]-head['box'][3]) > 14:
            add('schema', 'no subtitle under the heading', head)
        if not re.search(r'[a-z]', cap['text']) or len(cap['text']) < 25:
            add('schema', 'no sentence caption at the bottom', cap)
        elif abs(u(cap['box'][0]-head['box'][0])) > 1.5:
            add('schema', f'caption not on the heading\'s left edge ({u(cap["box"][0]-head["box"][0]):+.1f}u)', cap)
        out_rows = {'heading_x': u(head['box'][0]-z[0]), 'zone': side}
        # -- caption gap: no other ink in the band just above the caption
        if cap is not head:
            y0 = int(cap['box'][1]); band = int(5*k)
            x0, x1 = int(max(z[0], cap['box'][0]-2*k)), int(min(z[2], z[0]+(z[2]-z[0])))
            strip = alpha[max(0, y0-band):max(0, y0-1), x0:x1] > 40
            if strip.any():
                rows = np.nonzero(strip.any(axis=1))[0]
                gap = u(band-rows.max())
                add('caption-gap', f'ink {gap:.1f}u above the caption (want ≥ 5u)', cap)
        body = [t for t in zt if t is not head and t is not sub and t is not cap]
        # -- text in frames
        for r in zs:
            b = r['box']
            if u(b[2]-b[0]) < 10 or u(b[3]-b[1]) < 7:
                continue
            ins = [t for t in body if inside(t['box'], b)]
            # a small index just above the frame's top-left corner
            for t in body:
                tb = t['box']
                if 0 <= u(b[1]-tb[3]) <= 4 and -10 <= u(tb[0]-b[0]) <= .35*u(b[2]-b[0]) and len(t['text']) <= 3:
                    add('box-index', f'"{t["text"]}" floats above a frame corner', t)
            if not ins:
                continue
            tx0, ty0 = min(t['box'][0] for t in ins), min(t['box'][1] for t in ins)
            tx1, ty1 = max(t['box'][2] for t in ins), max(t['box'][3] for t in ins)
            l, rr, tp, bt = u(tx0-b[0]), u(b[2]-tx1), u(ty0-b[1]), u(b[3]-ty1)
            if l - rr > max(1.5, .15*(l+rr)):
                add('box-centre', f'text pushed right in its frame (left {l:.1f}u, right {rr:.1f}u)', ins[0])
            if abs(tp-bt) > max(1.2, .25*(tp+bt)) and len({round(u(t['box'][1])) for t in ins}) == 1:
                add('box-centre', f'text not vertically centred in its frame (top {tp:.1f}u, bottom {bt:.1f}u)', ins[0])
        # -- near-alignment between siblings, by the anchors the code placed them with (not by glyph ink)
        for i, a in enumerate(body):
            for c in body[i+1:]:
                if a.get('rot') or c.get('rot') or 'anchor' not in a or 'anchor' not in c:
                    continue
                ab, cb = a['box'], c['box']
                stacked = cb[1] > ab[3] and u(cb[1]-ab[3]) < 30
                side_by = not (cb[1] > ab[3] or ab[1] > cb[3])
                if stacked and a['align'] == c['align']:
                    d = abs(u(a['anchor'][0]-c['anchor'][0]))
                    if .4 < d < 3:
                        edge = {'l': 'left', 'r': 'right', 'c': 'centre'}[a['align']]
                        add('near-align', f'{edge} anchors of "{a["text"]}" and "{c["text"]}" miss by {d:.1f}u', a)
                elif (side_by and abs(u(a['font_px']-c['font_px'])) < .3 and u(max(cb[0]-ab[2], ab[0]-cb[2])) < 80
                      and not any(re.fullmatch(r'[\d.,\s/+-]+', t['text']) for t in (a, c))):
                    d = abs(u(a['anchor'][1]-c['anchor'][1]))
                    if .4 < d < 3:
                        add('near-align', f'baselines of "{a["text"]}" and "{c["text"]}" miss by {d:.1f}u', a)
        # -- a short value far across the block from the label on its line
        width = z[2]-z[0]
        for i, a in enumerate(body):
            for c in body:
                if c is a or c['box'][0] <= a['box'][2]:
                    continue
                if abs(centre(a['box'])[1]-centre(c['box'])[1]) > 1.5*k:
                    continue
                if (re.fullmatch(r'[\d.,%]+', c['text']) and len(a['text']) >= 4 and not re.fullmatch(r'[\d.,\s/+-]+', a['text'])
                        and u(c['box'][0]-a['box'][2]) > 120):
                    between = [t for t in body if t is not a and t is not c and a['box'][2] < centre(t['box'])[0] < c['box'][0]
                               and abs(centre(t['box'])[1]-centre(a['box'])[1]) < 1.5*k]
                    if not between:
                        add('detached', f'"{c["text"]}" is {u(c["box"][0]-a["box"][2]):.0f}u from "{a["text"]}"', c)
        # -- flush against the column boundary next to the main drawing
        for t in zt:
            if side == 'left' and u(z[2]-t['box'][2]) < 4:
                add('edge', f'"{t["text"]}" ends {u(z[2]-t["box"][2]):.1f}u from the column boundary', t)
            if side == 'right' and u(t['box'][0]-z[0]) < 4:
                add('edge', f'"{t["text"]}" starts {u(t["box"][0]-z[0]):.1f}u from the column boundary', t)
        out.append(dict(id=item['id'], zone=side, code='_heading_x', msg=f'{out_rows["heading_x"]:.1f}'))
    return out


def crops(out, ids=None, profile='16x9-2160p'):
    """Crops of every block for the judge layer: <out>/<id>-<block>.png on the sheet's ground, plus
    <id>-sheet.png (the whole virtual sheet, side and main layers). See docs/collection/eval-judge.md."""
    import aspect_layout as A
    import numpy as np
    from PIL import Image
    out.mkdir(parents=True, exist_ok=True)
    comp = A.composition(profile)
    def rgba(surface):
        h, w = surface.get_height(), surface.get_width()
        a = np.frombuffer(surface.get_data(), np.uint8).reshape(h, -1, 4)[:, :w].astype(float)
        return a[..., [2, 1, 0]], a[..., 3:4]/255
    for item in A.collection():
        if ids and item['id'] not in ids:
            continue
        s = A.render_virtual(item, comp)
        blocks = A.extract(s)
        ground = np.array([24, 30, 40.])
        side_rgb, side_a = rgba(s.surface)
        main_rgb, main_a = rgba(s.main_layer)
        whole = ground*(1-side_a)+side_rgb
        whole = whole*(1-main_a)+main_rgb
        Image.fromarray(whole.clip(0, 255).astype(np.uint8)).save(out/f'{item["id"]}-sheet.png')
        for name, b in blocks.items():
            rgb, a = (main_rgb, main_a) if name == 'main' else (side_rgb, side_a)
            x0, y0, x1, y1 = b.rect
            # blocks are tight ink boxes; a margin shows what sits around them (and keeps one-line blocks legible)
            x0, y0 = max(0, x0-32), max(0, y0-32)
            x1, y1 = min(whole.shape[1], x1+32), min(whole.shape[0], y1+32)
            img = (ground*(1-a[y0:y1, x0:x1])+rgb[y0:y1, x0:x1]).clip(0, 255).astype(np.uint8)
            Image.fromarray(img).save(out/f'{item["id"]}-{name}.png')
        print(item['id'], file=sys.stderr, flush=True)


def run(ids=None, profile='16x9-2160p'):
    import aspect_layout as A
    comp = A.composition(profile)
    found = []
    for item in A.collection():
        if ids and item['id'] not in ids:
            continue
        found += sheet_findings(item, comp)
        print(item['id'], file=sys.stderr, flush=True)
    # the common left edge: headings that sit away from the median of their side
    for side in ('left', 'right'):
        xs = [float(f['msg']) for f in found if f['code'] == '_heading_x' and f['zone'] == side]
        if len(xs) >= 5:
            med = statistics.median(xs)
            for f in found:
                if f['code'] == '_heading_x' and f['zone'] == side and abs(float(f['msg'])-med) > 2:
                    found.append(dict(id=f['id'], zone=side, code='schema', msg=f'heading {float(f["msg"])-med:+.1f}u off the common left edge', text=None))
    return [f for f in found if not f['code'].startswith('_')]


def score(found, ids=None):
    cases = json.loads(CASES.read_text())
    cases['cases'] = [c for c in cases['cases'] if c.get('layer', 'geometry') == 'geometry' and (not ids or c['id'] in ids)]
    hit = 0
    for c in cases['cases']:
        ok = any(f['id'] == c['id'] and f['zone'] == c['zone'] and f['code'] == c['code'] for f in found)
        hit += ok
        print(f"{'FOUND ' if ok else 'MISSED'} {c['id']}-{c['zone']} {c['code']:12s} {c['note']}")
    print(f'recall {hit}/{len(cases["cases"])}')
    return hit, len(cases['cases'])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--only')
    ap.add_argument('--profile', default='16x9-2160p')
    ap.add_argument('--json', type=Path)
    ap.add_argument('--cases', action='store_true', help='score recall on the labelled cases')
    ap.add_argument('--crops', type=Path, help='write block crops for the judge layer to this folder and stop')
    args = ap.parse_args()
    ids = set(args.only.split(',')) if args.only else None
    if args.crops:
        crops(args.crops, ids, args.profile)
        return
    found = run(ids, args.profile)
    for f in found:
        print(f"{f['id']}-{f['zone']:5s} {f['code']:12s} {f['msg']}")
    by = {}
    for f in found:
        by[f['code']] = by.get(f['code'], 0)+1
    print('findings', len(found), by)
    if args.json:
        args.json.write_text(json.dumps(found, indent=1, ensure_ascii=False)+'\n')
    if args.cases:
        score(found, ids)


if __name__ == '__main__':
    main()
