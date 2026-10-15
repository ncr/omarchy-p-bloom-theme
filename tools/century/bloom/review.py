#!/usr/bin/env python3
"""Contact sheets and native crops for visual review of p(bloom).

python tools/century/bloom/review.py [--tag pass1] [--ids b01,b02]

Writes concepts/bloom-ten/review/<tag>/:
  contact-16x9.jpg, contact-21x9.jpg  all rendered sheets, labelled
  <stem>-<fmt>-{A,B,C,left,right,notes}.jpg  crops at native 1:1 pixels
"""
import sys, argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
from century import bloom
OUT = ROOT / 'concepts/bloom-ten'


def crops(im, fmt):
    W, H = im.size
    k = W / 2560
    ex = (H / k - 1080)
    boxes = {
        'A': (700 * k, 110 * k, 1860 * k, (900 + ex * .5) * k),
        'B': (150 * k, 70 * k, 650 * k, (470 + ex * .45) * k),
        'C': (1910 * k, 70 * k, 2440 * k, (470 + ex * .45) * k),
        'left': (120 * k, (520 + ex * .55) * k, 620 * k, (760 + ex * .7) * k),
        'right': (1890 * k, (520 + ex * .55) * k, 2420 * k, (760 + ex * .75) * k),
        'notes': (1880 * k, H - 300 * k, 2520 * k, H - 60 * k),
    }
    return {n: tuple(int(v) for v in b) for n, b in boxes.items()}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--tag', default='latest'); ap.add_argument('--ids', default='')
    ap.add_argument('--no-crops', action='store_true')
    a = ap.parse_args()
    ids = [x for x in a.ids.split(',') if x]
    dest = OUT / 'review' / a.tag; dest.mkdir(parents=True, exist_ok=True)
    try:
        font = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf', 22)
    except OSError:
        font = ImageFont.load_default()
    for fmt in ('16x9', '21x9'):
        files = [(e, OUT / fmt / f'{bloom.stem(e)}.webp') for e in bloom.entries(ids or None)]
        files = [(e, f) for e, f in files if f.exists()]
        if not files:
            continue
        tw = 1200; th = int(tw * (2880 if fmt == '16x9' else 2160) / 5120)
        cols = 2; rows = (len(files) + 1) // 2
        sheet = Image.new('RGB', (cols * tw + (cols + 1) * 12, rows * (th + 40) + 12), (12, 14, 18))
        d = ImageDraw.Draw(sheet)
        for i, (e, f) in enumerate(files):
            im = Image.open(f).convert('RGB')
            if not a.no_crops:
                for name, box in crops(im, fmt).items():
                    im.crop(box).save(dest / f'{bloom.stem(e)}-{fmt}-{name}.jpg', quality=92)
            t = im.copy(); t.thumbnail((tw, th))
            x = 12 + (i % cols) * (tw + 12); y = 12 + (i // cols) * (th + 40)
            sheet.paste(t, (x, y + 30)); d.text((x, y), f"{e['series']}  {e['title']}", fill=(220, 225, 235), font=font)
        sheet.save(dest / f'contact-{fmt}.jpg', quality=90)
        print(dest / f'contact-{fmt}.jpg')


if __name__ == '__main__':
    main()
