#!/usr/bin/env python3
"""Before/after contact sheets of every changed spot between two master sets.

    python3 tools/stroke_cleanup_review.py OLD_DIR NEW_DIR [--spots 20]

Compares the lossless 16:9 masters of the path cleanup (tools/path_cleanup.py)
pixel by pixel, groups changed pixels into spots, and writes one contact sheet
per sheet (strongest spots first, 1:1 crops shown at 3x: before | after) plus
summary.json to concepts/stroke-cleanup/masters/.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'concepts/stroke-cleanup/masters'


def spots(diff, n, size):
    """Centres of the n strongest changed areas, at least `size` apart."""
    small = diff.reshape(diff.shape[0]//8, 8, diff.shape[1]//8, 8).sum((1, 3))
    order = np.argsort(small, axis=None)[::-1]
    out = []
    for idx in order:
        y, x = divmod(int(idx), small.shape[1])
        if small[y, x] <= 0 or len(out) >= n:
            break
        cy, cx = y*8+4, x*8+4
        if all(abs(cx-a) > size or abs(cy-b) > size for a, b, _ in out):
            out.append((cx, cy, float(small[y, x])))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('old', type=Path)
    ap.add_argument('new', type=Path)
    ap.add_argument('--spots', type=int, default=20)
    ap.add_argument('--only')
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    summary = {}
    half, zoom, cols = 48, 3, 4
    tile = 2*half*zoom
    for new in sorted(a.new.glob('*.webp')):
        if a.only and not any(new.name.startswith(x) for x in a.only.split(',')):
            continue
        old = a.old/new.name
        A = np.asarray(Image.open(old).convert('RGB')).astype(np.int16)
        B = np.asarray(Image.open(new).convert('RGB')).astype(np.int16)
        d = np.abs(A-B).max(-1)
        mask = d > 10
        ys, xs = np.nonzero(mask)
        found = spots(np.where(mask, d, 0).astype(np.float64), a.spots, half)
        summary[new.name] = dict(changed_px=int(mask.sum()), max_diff=int(d.max()),
                                 bbox=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None,
                                 spots=[[x, y] for x, y, _ in found])
        rows = max(1, -(-len(found)//cols))
        sheet = Image.new('RGB', (cols*(2*tile+16), rows*(tile+24)+30), (12, 10, 18))
        dr = ImageDraw.Draw(sheet)
        dr.text((6, 8), f'{new.name}  changed px {int(mask.sum())}  (1:1 crops at {zoom}x, before | after)', fill=(230, 222, 240))
        for i, (x, y, _) in enumerate(found):
            box = (max(0, x-half), max(0, y-half), max(0, x-half)+2*half, max(0, y-half)+2*half)
            px, py = (i % cols)*(2*tile+16), (i//cols)*(tile+24)+30
            for j, src in enumerate((A, B)):
                crop = Image.fromarray(src[box[1]:box[3], box[0]:box[2]].astype(np.uint8)).resize((tile, tile), Image.NEAREST)
                sheet.paste(crop, (px+j*(tile+4), py+20))
            dr.text((px+4, py+4), f'x {x} y {y}', fill=(200, 190, 220))
        sheet.save(OUT/(new.stem+'.png'))
        print(new.name, summary[new.name]['changed_px'], summary[new.name]['bbox'], flush=True)
    (OUT/'summary.json').write_text(json.dumps(summary, indent=1)+'\n')


if __name__ == '__main__':
    main()
