#!/usr/bin/env python3
"""The p(bloom) Wallpapers app icon, rendered natively at every size the icon theme uses.

    python3 tools/make_icon.py        # writes companion/icons/p-bloom-wallpapers-<size>.png

A tile in the magenta of the sheets' grounds, with their faint grid. On it the name as on the music video's card,
p( ) in Jost Light with a Pollen flower between the parentheses, framed by the sheets' corner marks. The marks keep
one gap to the monogram's ink on all four sides (38/512 of the tile), and the monogram is sized so the frame's sides
sit 16 % in from the tile, where they are on a sheet.
"""
import math
from pathlib import Path
import urllib.request

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'companion/icons'
SIZES = (16, 24, 32, 48, 64, 128, 256, 512)
FONT = Path.home()/'.cache/p-bloom/jost-300.ttf'
ICE = (217, 232, 255)
POLLEN = (245, 201, 69)
GROUND_TOP, GROUND = (120, 24, 64), (70, 12, 40)
GAP, SIDE = 38/512, 0.16


def jost():
    if not FONT.is_file():
        css = urllib.request.urlopen('https://fonts.googleapis.com/css2?family=Jost:wght@300', timeout=30).read().decode()
        FONT.parent.mkdir(parents=True, exist_ok=True)
        FONT.write_bytes(urllib.request.urlopen(css.split('url(')[1].split(')')[0], timeout=30).read())
    return str(FONT)


def tile(cr, S):
    r, m = S*0.22, S*0.04
    cr.new_path()
    cr.arc(m+r, m+r, r, math.pi, 1.5*math.pi)
    cr.arc(S-m-r, m+r, r, 1.5*math.pi, 0)
    cr.arc(S-m-r, S-m-r, r, 0, .5*math.pi)
    cr.arc(m+r, S-m-r, r, .5*math.pi, math.pi)
    cr.close_path()
    g = cairo.LinearGradient(0, m, 0, S-m)
    g.add_color_stop_rgb(0, *(c/255 for c in GROUND_TOP))
    g.add_color_stop_rgb(1, *(c/255 for c in GROUND))
    cr.set_source(g)
    cr.fill_preserve()
    cr.set_source_rgba(1, 1, 1, .10)
    cr.set_line_width(max(1, S/128))
    cr.stroke()
    if S >= 48:                                          # the grid only where it can be seen
        cr.set_source_rgba(*(c/255 for c in ICE), .05)
        cr.set_line_width(max(1, S/512))
        step, a = S/16, S*.1
        for k in range(17):
            v = a + k*step
            if v <= S-a+1:
                cr.move_to(v, a); cr.line_to(v, S-a)
                cr.move_to(a, v); cr.line_to(S-a, v)
        cr.stroke()


def monogram(S, size):
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(jost(), max(4, int(S*size)))
    wp, wr = f.getlength('p('), f.getlength(')')
    g = S*size*.42
    x = (S - (wp + g + wr))/2
    bb = f.getbbox('p()')
    y = (S - (bb[3] - bb[1]))/2 - bb[1]
    d.text((x, y), 'p(', font=f, fill=ICE)
    d.text((x + wp + g, y), ')', font=f, fill=ICE)
    cap = f.getbbox('(')
    cx, cy, R = x + wp + g/2, y + (cap[1] + cap[3])/2, S*size*.115
    for k in range(5):
        a = -math.pi/2 + k*2*math.pi/5
        px, py, r = cx + math.cos(a)*R, cy + math.sin(a)*R, R*.74
        d.ellipse((px-r, py-r, px+r, py+r), fill=POLLEN)
    d.ellipse((cx-R*.42, cy-R*.42, cx+R*.42, cy+R*.42), fill=GROUND_TOP)
    alpha = np.asarray(im)[..., 3]
    ys, xs = np.nonzero(alpha > 20)
    return im, (xs.min(), ys.min(), xs.max()+1, ys.max()+1)


def icon(S):
    # the monogram's size puts the frame's sides at SIDE from the tile's edges, with GAP to the ink;
    # at 24 px and below the corner marks would be noise, so they go and the monogram takes their room
    framed = S > 24
    side, gap = (SIDE, GAP) if framed else (0.12, 0.0)
    lo, hi = .2, .6
    for _ in range(25):
        mid = (lo+hi)/2
        _, (a, _, c, _) = monogram(512, mid)
        lo, hi = (lo, mid) if (512-(c-a))/2 - gap*512 < side*512 else (mid, hi)
    layer, (x0, y0, x1, y1) = monogram(S, lo)
    dx, dy = round(S/2 - (x0+x1)/2), round(S/2 - (y0+y1)/2)
    x0, x1, y0, y1 = x0+dx, x1+dx, y0+dy, y1+dy
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, S, S)
    cr = cairo.Context(surface)
    tile(cr, S)
    g, lw, mark = GAP*S, max(1.0, S/256*3), S*.085
    fx0, fy0, fx1, fy1 = x0-g-lw/2, y0-g-lw/2, x1+g+lw/2, y1+g+lw/2
    if framed:
        cr.set_source_rgba(*(c/255 for c in ICE), .62)
        cr.set_line_width(lw)
        for x, y, sx, sy in ((fx0, fy0, 1, 1), (fx1, fy0, -1, 1), (fx0, fy1, 1, -1), (fx1, fy1, -1, -1)):
            cr.move_to(x, y + sy*mark); cr.line_to(x, y); cr.line_to(x + sx*mark, y)
        cr.stroke()
    surface.flush()
    a = np.ndarray((S, S, 4), np.uint8, surface.get_data()).copy()
    rgba = a[..., [2, 1, 0, 3]].astype(float)
    alpha = rgba[..., 3:4]/255
    rgba[..., :3] = np.where(alpha > 0, rgba[..., :3]/np.maximum(alpha, 1e-6), 0)   # un-premultiply
    im = Image.fromarray(rgba.clip(0, 255).astype(np.uint8), 'RGBA')
    im.alpha_composite(layer, (dx, dy))
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for S in SIZES:
        icon(S).save(OUT/f'p-bloom-wallpapers-{S}.png', optimize=True)
    print(OUT, SIZES)


if __name__ == '__main__':
    main()
