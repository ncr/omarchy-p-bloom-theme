#!/usr/bin/env python3
"""README comparison: the same corner of Fusion Transport on a 1920x1080 monitor,
once as the 5K master scaled down, once from the set composed for that screen.
Both crops are real screen pixels, drawn at 2x with nearest-neighbour so a
retina browser shows them exactly and a 1x browser shows them at true size."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'previews/resolution.webp'
MASTER = ROOT / 'backgrounds/03-fusion-transport.webp'
# The composed 1080p file comes from the release archive (dist/ after packaging).
NATIVE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'dist/wallpaper-release/16x9-1080p/03-fusion-transport.webp'
FONT = Path('/usr/share/fonts/gsfonts')
def font(size, face='NimbusSans-Regular.otf'):
    return ImageFont.truetype(str(FONT / face), size)

SCREEN = (1920, 1080)
CW, CH, K = 450, 250, 2           # crop in screen pixels, zoom
old = Image.open(MASTER).convert('RGB').resize(SCREEN, Image.LANCZOS)   # a high-quality downscale
new = Image.open(NATIVE).convert('RGB')
assert new.size == SCREEN, new.size
# Top-left of the title block in each layout.
crops = [old.crop((62, 815, 62 + CW, 815 + CH)), new.crop((82, 690, 82 + CW, 690 + CH))]

pad, gap, top = 36, 36, 150
W = pad * 2 + CW * K * 2 + gap
H = top + CH * K + 34
canvas = Image.new('RGB', (W, H), '#090d16')
d = ImageDraw.Draw(canvas)
labels = [('ONE IMAGE FOR EVERY SCREEN', '5120 × 2880 master, scaled down to 1920 × 1080', '#8a93a6'),
          ('p(bloom): COMPOSED FOR THIS SCREEN', 'the 1920 × 1080 set, text never below 11 px', '#4cc9ff')]
for i, (crop, (head, sub, col)) in enumerate(zip(crops, labels)):
    x = pad + i * (CW * K + gap)
    d.text((x, 40), head, font=font(38, 'NimbusSans-Bold.otf'), fill=col)
    d.text((x, 92), sub, font=font(30), fill='#b7c4d9')
    canvas.paste(crop.resize((CW * K, CH * K), Image.NEAREST), (x, top))
    d.rectangle((x - 1, top - 1, x + CW * K, top + CH * K), outline=col, width=2)
canvas.save(OUT, quality=92, method=6)
print(OUT, canvas.size)
