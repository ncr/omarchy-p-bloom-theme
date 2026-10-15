#!/usr/bin/env python3
"""Fast geometry preview: A, B, C exported paths on one dark canvas.

python tools/century/bloom/preview.py canopy-seeder [--out file.png] [--size 1400]
Role colours follow the sheet (structure bright, detail/shell dimmer,
accent cyan, cable gold). Anchors drawn as red dots with their key.
"""
import sys, json, argparse
from pathlib import Path
import cairo
ROOT = Path(__file__).resolve().parents[3]
ASSETS = ROOT / 'tools/assets/century'
STY = {'structure': (.9, .9, .95, 1.0), 'detail': (.75, .78, .85, .65), 'shell': (.6, .65, .7, .5),
       'accent': (.35, .8, 1, .9), 'cable': (.95, .78, .3, .8), 'figure': (.9, .9, .95, .9)}


def draw(ctx, d, x0, y0, W, H, label):
    pts = [p for path in d['paths'] for p in path['points']]
    if not pts:
        return
    xa = min(p[0] for p in pts); xb = max(p[0] for p in pts); ya = min(p[1] for p in pts); yb = max(p[1] for p in pts)
    k = min((W - 40) / max(1e-6, xb - xa), (H - 60) / max(1e-6, yb - ya))
    ox = x0 + W / 2 - (xa + xb) / 2 * k; oy = y0 + H / 2 - (ya + yb) / 2 * k
    for path in d['paths']:
        r, g, b, a = STY.get(path['role'], (.7, .7, .7, .6))
        ctx.set_source_rgba(r, g, b, a); ctx.set_line_width(1.1 if path['role'] == 'structure' else .8)
        p0 = path['points']
        ctx.move_to(ox + p0[0][0] * k, oy + p0[0][1] * k)
        for p in p0[1:]:
            ctx.line_to(ox + p[0] * k, oy + p[1] * k)
        ctx.stroke()
    ctx.set_font_size(12)
    for name, p in d.get('anchors', {}).items():
        ctx.set_source_rgba(1, .3, .3, 1); ctx.arc(ox + p[0] * k, oy + p[1] * k, 4, 0, 6.3); ctx.fill()
        ctx.move_to(ox + p[0] * k + 6, oy + p[1] * k - 6); ctx.show_text(name)
    ctx.set_source_rgba(1, 1, 1, .8); ctx.set_font_size(16); ctx.move_to(x0 + 12, y0 + 22); ctx.show_text(label)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('slug'); ap.add_argument('--out'); ap.add_argument('--size', type=int, default=1300)
    ap.add_argument('--only', default='ABC')
    ap.add_argument('--keys', default='', help='comma list of view suffixes, e.g. probe0,probe1')
    a = ap.parse_args()
    keys = a.keys.split(',') if a.keys else list(a.only)
    n = len(keys); S = a.size
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, S * n if n > 1 else S, S)
    ctx = cairo.Context(surf); ctx.set_source_rgb(.07, .09, .12); ctx.paint()
    for i, key in enumerate(keys):
        src = (Path('/tmp/bloom/probes') if key.startswith('probe') else ASSETS) / f'{a.slug}-{key}.json'
        d = json.loads(src.read_text())
        draw(ctx, d, i * S, 0, S, S, f'{a.slug} {key}')
    out = a.out or f"/tmp/bloom/{a.slug}-{''.join(keys)}.png"
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    surf.write_to_png(out); print(out)


if __name__ == '__main__':
    main()
