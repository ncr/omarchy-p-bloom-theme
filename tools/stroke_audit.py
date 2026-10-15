#!/usr/bin/env python3
"""Detect line artefacts in the exported drawing paths of every sheet.

    python3 tools/stroke_audit.py                 # counts per sheet and view, before/after
    python3 tools/stroke_audit.py --evidence 24   # plus zoomed before/after crops
    python3 tools/stroke_audit.py --refresh-map   # re-discover which views each sheet loads

Works on the vector paths in tools/assets/ (model units), not on pixels.
For every view of every sheet (main view A and its B/C or auxiliary views) it
counts, on the raw export and after tools/path_cleanup.clean():

* strays       short open fragments touching nothing within the snap radius
               (closed loops, cables and accents are never strays);
* near misses  free path ends within the snap radius of other geometry:
               gap, overshoot, node or sideways touch;
* duplicates   collinear segments drawn on top of each other (count and
               overlapping length);
* split joins  places where two separate strokes of one role meet end to end
               (butt caps: notch outside, doubled alpha inside).

Pixel sizes use the approximate 5K master scale of the view (A ~1360 px,
side views ~750 px across) and only rank the evidence.
Output: concepts/stroke-cleanup/report.json, report.md and evidence-*.png.
"""
import argparse
import json
import math
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
OUT = ROOT/'concepts/stroke-cleanup'
ASSETS = ROOT/'tools/assets'
# Hand-authored rig lines with per-path widths; reported, not cleaned.
NOT_CLEANED = ('mannequin3d/',)


def discover():
    """Sheet id -> views it loads, found by rendering each sheet small."""
    import gc
    import pathlib
    import path_cleanup
    orig = pathlib.Path.read_text
    log = []

    def read_text(self, *a, **k):
        p = str(self.resolve())
        if '/tools/assets/' in p:
            log.append(p.split('/tools/assets/')[1])
        return orig(self, *a, **k)
    pathlib.Path.read_text = read_text
    import aspect_layout as A
    out = {}
    for it in A.collection():
        for name in ('hardware3d.family_drawing', 'hardware3d.radial_drawing', 'projected_dummy'):
            m = sys.modules.get(name)
            for fn in vars(m).values() if m else ():
                if hasattr(fn, 'cache_clear'):
                    fn.cache_clear()
        path_cleanup._CACHE.clear()
        log.clear()
        it['render']((1280, 720))
        views = sorted({v for v in log if v.endswith('.json') and not v.endswith('-meta.json')
                        and not v.endswith('labels.json')})
        out[it['id']] = dict(filename=it['filename'], family=it['family'], views=views)
        print(it['id'], len(views), 'views', flush=True)
        gc.collect()
    pathlib.Path.read_text = orig
    return out


def px_scale(view, extent):
    main = view.endswith('-A.json') or view.split('/')[-1] in MAIN_VIEWS
    return (1360 if main else 750)/extent


MAIN_VIEWS = {'air-refinery.json', 'aroma-organ.json', 'bounder.json', 'cortical-mesh.json',
              'fusion-transport.json', 'organ-foundry.json', 'sky-racer.json', 'tether-climber.json',
              'proxy-main-scene.json', 'main.json'}


def audit_view(view):
    import path_cleanup as pc
    data = json.loads((ASSETS/view).read_text())
    paths = data['paths']
    k = None
    before = pc.analyse(paths)
    k = px_scale(view, before['extent'])
    cleaned = paths if view.startswith(NOT_CLEANED) else pc.clean(paths)
    after = pc.analyse(cleaned)

    def summary(a):
        return dict(paths=a['paths'], split_joins=a['split_joins'],
                    strays=len(a['strays']), near_miss=len(a['near_miss']),
                    near_miss_kinds={kind: sum(1 for x in a['near_miss'] if x[0] == kind)
                                     for kind in ('gap', 'overshoot', 'node', 'touch')},
                    duplicates=len(a['duplicates']),
                    duplicate_px=round(sum(x[0] for x in a['duplicates'])*k, 1))
    cases = ([dict(kind='stray', px=l*k, at=p, detail=f'{n} seg') for l, p, n in before['strays']]
             + [dict(kind='near-miss', px=d*k, at=p, detail=kind) for kind, d, p in before['near_miss']]
             + [dict(kind='duplicate', px=l*k, at=p, detail='/'.join(r)) for l, p, r in before['duplicates']])
    return view, dict(thresholds={a: round(b, 4) for a, b in before['thresholds'].items()},
                      extent=round(before['extent'], 2), px_per_unit=round(k, 3),
                      cleaned=not view.startswith(NOT_CLEANED),
                      before=summary(before), after=summary(after)), cases


def evidence(cases, per_kind, out):
    """Before/after crops around the worst cases of each kind."""
    import cairo
    from PIL import Image, ImageDraw
    import path_cleanup as pc
    loaded = {}

    def view_paths(view):
        if view not in loaded:
            raw = json.loads((ASSETS/view).read_text())['paths']
            loaded[view] = (raw, raw if view.startswith(NOT_CLEANED) else pc.clean(raw))
        return loaded[view]
    styles = {'structure': (.89, .85), 'plate': (.87, 1), 'figure': (.9, .8), 'outline': (.75, .8),
              'detail': (.69, .47), 'shell': (.48, .36), 'accent': (.86, .62), 'cable': (.64, .47)}
    colours = {'accent': (.45, .86, .92), 'cable': (.95, .76, .38), 'fine': (.45, .86, .92)}
    zoom, half = 4, 36          # 72 master px shown at 4x

    def draw(paths, k, cx, cy, mark):
        size = 2*half*zoom
        surf = cairo.ImageSurface(cairo.FORMAT_RGB24, size, size)
        c = cairo.Context(surf)
        c.set_source_rgb(41/255, 19/255, 69/255); c.paint()
        c.scale(zoom, zoom); c.translate(half, half)
        c.set_line_cap(cairo.LINE_CAP_BUTT); c.set_line_join(cairo.LINE_JOIN_MITER)
        for p in paths:
            role = p.get('role', p.get('kind'))
            a, w = styles.get(role, (.56, .45))
            pts, closed = pc.points(p)
            c.new_path()
            c.move_to((pts[0][0]-cx)*k, (pts[0][1]-cy)*k)
            for q in pts[1:]:
                c.line_to((q[0]-cx)*k, (q[1]-cy)*k)
            if closed:
                c.close_path()
            c.set_source_rgba(*colours.get(role, (1, 1, 1)), a)
            c.set_line_width(w*2)       # design units at 2 px each
            c.stroke()
        if mark:
            c.new_path(); c.arc(0, 0, 9, 0, 2*math.pi)
            c.set_source_rgba(1, .45, .2, .9); c.set_line_width(.6); c.stroke()
        buf = surf.get_data()
        return Image.frombuffer('RGBA', (size, size), bytes(buf), 'raw', 'BGRA', 0, 1).convert('RGB')
    written = []
    for kind in ('stray', 'near-miss', 'duplicate'):
        top = sorted((c for c in cases if c['kind'] == kind), key=lambda c: -c['px'])[:per_kind]
        if not top:
            continue
        tile = 2*half*zoom
        cols = 4
        rows = math.ceil(len(top)/cols)
        sheet = Image.new('RGB', (cols*(2*tile+18), rows*(tile+34)), (14, 12, 20))
        d = ImageDraw.Draw(sheet)
        for i, case in enumerate(top):
            raw, cleaned = view_paths(case['view'])
            k = case['k']
            x, y = (i % cols)*(2*tile+18), (i//cols)*(tile+34)
            sheet.paste(draw(raw, k, *case['at'], True), (x, y+30))
            sheet.paste(draw(cleaned, k, *case['at'], False), (x+tile+4, y+30))
            d.text((x+4, y+4), f"{case['sheet']} {case['view'].split('/')[-1][:-5]}  {case['detail']}"
                               f"  {case['px']:.1f}px   before | after", fill=(230, 222, 240))
        path = out/f'evidence-{kind}.png'
        sheet.save(path)
        written.append(path)
    return written


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--refresh-map', action='store_true')
    ap.add_argument('--jobs', type=int, default=3)
    ap.add_argument('--evidence', type=int, default=0, help='worst cases per kind to render')
    ap.add_argument('--only', help='comma-separated sheet ids')
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    mapping = OUT/'views.json'
    if args.refresh_map or not mapping.is_file():
        mapping.write_text(json.dumps(discover(), indent=1)+'\n')
    sheets = json.loads(mapping.read_text())
    if args.only:
        sheets = {i: s for i, s in sheets.items() if i in args.only.split(',')}
    for s in sheets.values():
        s['views'] = [v for v in s['views'] if not v.endswith(('-meta.json', 'labels.json'))]
    views = sorted({v for s in sheets.values() for v in s['views']})
    results, cases = {}, []
    owners = {}
    for i, s in sheets.items():
        for v in s['views']:
            owners.setdefault(v, []).append(i)
    with ProcessPoolExecutor(args.jobs) as pool:
        for view, r, cs in pool.map(audit_view, views):
            results[view] = r
            for c in cs:
                c.update(view=view, sheet=owners[view][0], k=r['px_per_unit'])
            cases += cs
            b, a = r['before'], r['after']
            print(f"{view:48} strays {b['strays']:4}->{a['strays']:<4} near {b['near_miss']:5}->{a['near_miss']:<5}"
                  f" dup {b['duplicates']:5}->{a['duplicates']:<5} joins {b['split_joins']:6}->{a['split_joins']}",
                  flush=True)
    keys = ('strays', 'near_miss', 'duplicates', 'duplicate_px', 'split_joins')
    per_sheet = {}
    for i, s in sheets.items():
        tot = {w: {k: 0 for k in keys} for w in ('before', 'after')}
        for v in s['views']:
            for w in tot:
                for k in keys:
                    tot[w][k] += results[v][w][k]
        per_sheet[i] = dict(filename=s['filename'], family=s['family'], views=s['views'], **tot)
    (OUT/'report.json').write_text(json.dumps(dict(sheets=per_sheet, views=results), indent=1)+'\n')
    lines = ['| sheet | strays | near misses | duplicates (px) | split joins |', '|---|---|---|---|---|']
    for i, r in per_sheet.items():
        b, a = r['before'], r['after']
        lines.append(f"| {i} {r['filename'][:-5]} | {b['strays']} → {a['strays']} | {b['near_miss']} → {a['near_miss']}"
                     f" | {b['duplicates']} ({b['duplicate_px']:.0f}) → {a['duplicates']} ({a['duplicate_px']:.0f})"
                     f" | {b['split_joins']} → {a['split_joins']} |")
    (OUT/'report.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))
    if args.evidence:
        for p in evidence(cases, args.evidence, OUT):
            print('wrote', p.relative_to(ROOT))


if __name__ == '__main__':
    main()
