#!/usr/bin/env python3
"""The p(bloom) unlock screen: the logo Plymouth shows above the password field, and its preview.

    python3 tools/make_unlock.py [variant]     # writes unlock.png and preview-unlock.png in the theme root

The logo is the app icon without its tile: p( ) in Jost Light with a Pollen flower between the parentheses, framed by
the sheets' corner marks at the icon's proportions (the marks keep one gap to the monogram's ink on every side). Plymouth
draws it at its own pixel size, centred on the theme's background with the password field below, so it is made about
as large as Omarchy's own logos. The preview is Omarchy's own (`omarchy plymouth preview`) with the theme's colours.

Variants for comparison: wordmark (p(bloom) as in the video), monogram (no frame), framed (the default).
"""
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_icon import GAP, POLLEN, SIDE, jost  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
COLORS = tomllib.loads((ROOT/'colors.toml').read_text())
INK = tuple(int(COLORS['foreground'][i:i + 2], 16) for i in (1, 3, 5))     # the unlock screen's text colour


def flower(draw, cx, cy, R, hole=True):
    """Five overlapping Pollen petals; the centre is cut out to show what is behind."""
    for k in range(5):
        a = -math.pi/2 + k*2*math.pi/5
        px, py, r = cx + math.cos(a)*R, cy + math.sin(a)*R, R*.74
        draw.ellipse((px - r, py - r, px + r, py + r), fill=POLLEN + (255,))
    if hole:
        draw.ellipse((cx - R*.42, cy - R*.42, cx + R*.42, cy + R*.42), fill=(0, 0, 0, 0))


def ink_box(im):
    ys, xs = np.nonzero(np.asarray(im)[..., 3] > 20)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def trim(im, margin):
    x0, y0, x1, y1 = ink_box(im)
    return im.crop((x0 - margin, y0 - margin, x1 + margin, y1 + margin))


def monogram(size):
    """p( ❀ ) at a font size, on a transparent canvas larger than it."""
    S = int(size*4)
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(jost(), int(size))
    wp, wr = f.getlength('p('), f.getlength(')')
    g = size*.42
    x = (S - (wp + g + wr))/2
    bb = f.getbbox('p()')
    y = (S - (bb[3] - bb[1]))/2 - bb[1]
    d.text((x, y), 'p(', font=f, fill=INK + (255,))
    d.text((x + wp + g, y), ')', font=f, fill=INK + (255,))
    cap = f.getbbox('(')
    flower(d, x + wp + g/2, y + (cap[1] + cap[3])/2, size*.115)
    return im


def wordmark(size):
    S = (int(size*6), int(size*2))
    im = Image.new('RGBA', S, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(jost(), int(size))
    x, y = size*.3, size*.3
    for part, colour in (('p(', INK), ('bloom', POLLEN), (')', INK)):
        d.text((x, y), part, font=f, fill=colour + (255,))
        x += f.getlength(part)
    return trim(im, 4)


def framed(size):
    """The monogram inside the sheets' corner marks, at the icon's proportions: one gap to the ink on every side."""
    mono = monogram(size)
    x0, y0, x1, y1 = ink_box(mono)
    # the icon's tile width that gives this monogram: its ink plus a gap and half a stroke on each side spans the
    # tile minus SIDE on each side (make_icon.icon)
    lw = 3.0
    unit = (x1 - x0 + 2*lw)/(1 - 2*SIDE - 2*GAP)
    gap, mark = GAP*unit, unit*.085
    pad = int(gap + lw + 4)
    W, H = int(x1 - x0 + 2*pad), int(y1 - y0 + 2*pad)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surface)
    fx0, fy0, fx1, fy1 = pad - gap - lw/2, pad - gap - lw/2, W - pad + gap + lw/2, H - pad + gap + lw/2
    cr.set_source_rgba(*(c/255 for c in INK), .62)
    cr.set_line_width(lw)
    for x, y, sx, sy in ((fx0, fy0, 1, 1), (fx1, fy0, -1, 1), (fx0, fy1, 1, -1), (fx1, fy1, -1, -1)):
        cr.move_to(x, y + sy*mark)
        cr.line_to(x, y)
        cr.line_to(x + sx*mark, y)
    cr.stroke()
    surface.flush()
    a = np.ndarray((H, W, 4), np.uint8, surface.get_data()).copy()
    rgba = a[..., [2, 1, 0, 3]].astype(float)
    alpha = rgba[..., 3:4]/255
    rgba[..., :3] = np.where(alpha > 0, rgba[..., :3]/np.maximum(alpha, 1e-6), 0)
    im = Image.fromarray(rgba.clip(0, 255).astype(np.uint8), 'RGBA')
    im.alpha_composite(mono.crop((x0 - pad, y0 - pad, x1 + pad, y1 + pad)))
    return im


VARIANTS = {'framed': lambda: framed(300), 'monogram': lambda: trim(monogram(320), 4), 'wordmark': lambda: wordmark(200)}


def preview(logo, out):
    """Omarchy's own preview of the boot screen, with its image viewer stubbed out so nothing opens."""
    with tempfile.TemporaryDirectory() as d:
        stub = Path(d)/'imv'
        stub.write_text('#!/bin/sh\nexit 0\n')
        stub.chmod(0o755)
        env = {**os.environ, 'PATH': f"{d}:{os.environ['PATH']}",
               'OMARCHY_PATH': os.environ.get('OMARCHY_PATH', str(Path.home()/'.local/share/omarchy'))}
        subprocess.run(['omarchy-plymouth-preview', COLORS['background'], COLORS['foreground'], str(logo), str(out)],
                       check=True, env=env)


def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else 'framed'
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT
    logo = VARIANTS[variant]()
    logo.save(out/'unlock.png', optimize=True)
    preview(out/'unlock.png', out/'preview-unlock.png')
    print(out/'unlock.png', logo.size)


if __name__ == '__main__':
    main()
