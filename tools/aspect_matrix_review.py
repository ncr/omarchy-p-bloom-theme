#!/usr/bin/env python3
"""Review sheets for the rendered matrix (written to concepts/aspect-matrix/).

    python3 tools/aspect_matrix_review.py [--sets dist/wallpaper-sets]

- <profile>.jpg: all 42 sheets of one profile, with drops/fallbacks noted.
- across-<id>.jpg: one sheet in every profile, at a common height.
- smallest-<profile>.png: native 1:1 crops around the smallest labels.
"""
import argparse
import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = '/usr/share/fonts/gsfonts/NimbusSans-Regular.otf'


def font(size):
    try:
        return ImageFont.truetype(FONT, size)
    except OSError:
        return ImageFont.load_default()


def contact(profile_dir, out):
    audit = json.loads((profile_dir/'audit.json').read_text())
    sheets = audit['sheets']
    w0, h0 = sheets[0]['size']
    cols = 6
    cw = 560
    ch = round(cw*h0/w0)
    label = 44
    sheet = Image.new('RGB', (cols*cw, ((len(sheets)+cols-1)//cols)*(ch+label)+60), (10, 12, 16))
    d = ImageDraw.Draw(sheet)
    d.text((10, 14), f"{audit['profile']}  {w0}×{h0}  min type {audit['min_text_px']} px  audit findings {audit['issues']}",
           fill=(230, 235, 240), font=font(28))
    for i, r in enumerate(sheets):
        with Image.open(profile_dir/r['file']) as im:
            thumb = im.convert('RGB').resize((cw, ch), Image.Resampling.LANCZOS)
        x, y = (i % cols)*cw, 60+(i//cols)*(ch+label)
        sheet.paste(thumb, (x, y))
        note = r['id']
        if r['dropped']:
            note += '  −' + ','.join(n.replace('_diagram', ' diag') for n in r['dropped'])
        if r.get('fallback'):
            note += f"  [{r['fallback']}]"
        d.text((x+8, y+ch+8), note, fill=(200, 210, 225) if not r['issues'] else (255, 120, 120), font=font(20))
    sheet.save(out, quality=88)


def across(sets, ids, out):
    profiles = sorted(p for p in sets.iterdir() if (p/'audit.json').is_file())
    for sid in ids:
        tiles = []
        for p in profiles:
            audit = json.loads((p/'audit.json').read_text())
            r = next(x for x in audit['sheets'] if x['id'] == sid)
            with Image.open(p/r['file']) as im:
                h = 360
                tiles.append((p.name, im.convert('RGB').resize((round(h*im.width/im.height), h), Image.Resampling.LANCZOS)))
        width = 2600
        rows, row, x = [], [], 0
        for name, t in tiles:
            if x+t.width > width and row:
                rows.append(row)
                row, x = [], 0
            row.append((name, t))
            x += t.width+16
        rows.append(row)
        img = Image.new('RGB', (width, len(rows)*(360+40)), (10, 12, 16))
        d = ImageDraw.Draw(img)
        for j, row in enumerate(rows):
            x = 0
            for name, t in row:
                img.paste(t, (x, j*400+34))
                d.text((x+4, j*400+6), name, fill=(220, 228, 236), font=font(22))
                x += t.width+16
        img.save(out/f'across-{sid}.jpg', quality=88)


def smallest(profile_dir, out, count=12):
    """Native crops: needs the text boxes from a fresh audit (not stored)."""
    sys.path.insert(0, str(ROOT/'tools'))
    import aspect_layout as A
    audit = json.loads((profile_dir/'audit.json').read_text())
    comp = A.composition(audit['profile'])
    items = {i['id']: i for i in A.collection()}
    crops = []
    for r in audit['sheets'][::5]:
        s = A.compose(items[r['id']], comp)
        boxes = []
        for t in s.layer_boxes:
            for name, (tx, ty, rect) in s.shift.items():
                b = s.blocks.get(name)
                if b is None or b.surface is not t['surface']:
                    continue
                x0, y0, x1, y1 = t['box']
                if rect[0] <= (x0+x1)/2 <= rect[2] and rect[1] <= (y0+y1)/2 <= rect[3]:
                    boxes.append((t['font_px'], [x0+tx, y0+ty, x1+tx, y1+ty], t['text']))
        boxes.sort(key=lambda b: (b[0], -(b[1][2]-b[1][0])))
        with Image.open(profile_dir/r['file']) as im:
            for fp, (x0, y0, x1, y1), text in boxes[:2]:
                crops.append((f"{r['id']} {fp:.1f}px: {text[:40]}",
                              im.convert('RGB').crop((int(x0)-40, int(y0)-24, int(x1)+40, int(y1)+24))))
    crops = crops[:count]
    width = max(c.width for _, c in crops)+20
    img = Image.new('RGB', (width, sum(c.height+34 for _, c in crops)), (0, 0, 0))
    d = ImageDraw.Draw(img)
    y = 0
    for name, c in crops:
        d.text((6, y+6), name, fill=(255, 220, 90), font=font(18))
        img.paste(c, (10, y+30))
        y += c.height+34
    img.save(out/f'smallest-{audit["profile"]}.png')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sets', type=Path, default=ROOT/'dist/wallpaper-sets')
    ap.add_argument('--out', type=Path, default=ROOT/'concepts/aspect-matrix')
    ap.add_argument('--across', default='o03,o10,c087,o06,c042,o13')
    ap.add_argument('--smallest', default='16x9-1080p,16x10-1200p,4x3-1200p,64x27-1080p,32x9-1080p,3x2-1504p')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for p in sorted(args.sets.iterdir()):
        if (p/'audit.json').is_file():
            contact(p, args.out/f'{p.name}.jpg')
            print('contact', p.name, flush=True)
    across(args.sets, args.across.split(','), args.out)
    for pid in args.smallest.split(','):
        if (args.sets/pid/'audit.json').is_file():
            smallest(args.sets/pid, args.out)
            print('smallest', pid, flush=True)


if __name__ == '__main__':
    main()
