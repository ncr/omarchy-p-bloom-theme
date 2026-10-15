#!/usr/bin/env python3
"""Compose the promo from real production sheets; never redraw their content."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'previews/wallpaper-collage.webp'
W, H = 2400, 1430
TILT_DEGREES = 5
FONT = Path('/usr/share/fonts/gsfonts')
def font(size, face='NimbusSans-Regular.otf'):
    return ImageFont.truetype(str(FONT / face), size)

canvas = Image.new('RGBA', (W, H), '#090f1b')
draw = ImageDraw.Draw(canvas)
# Quiet engineering-paper registration marks behind the real prints.
for x in range(60, W, 120):
    for y in range(40, H, 120):
        draw.line((x-3,y,x+3,y), fill='#172332')
        draw.line((x,y-3,x,y+3), fill='#172332')
draw.text((94, 51), 'p(bloom)    /    omarchy', font=font(27), fill='#98b2c3')
draw.text((1780, 51), 'A FIELD GUIDE TO TOMORROW', font=font(23), fill='#98b2c3')

# Original bitmap sheets on a slightly skewed print wall.
names = [
    '01-quantum-simulator', '03-fusion-transport', 'b18-stellarator-hearth', '02-sky-racer',
    '065-seam-surgeon', '12-volumetric-stage', '09-tether-climber', '11-organ-foundry',
    '006-manta-foil', '101-velvet-hammer', '025-fibre-braid', '110-spin-table',
]
tw, th, gap = 726, 408, 28
wall = Image.new('RGBA', (4*(tw+gap)+60, 3*(th+gap)+60))
for i, name in enumerate(names):
    x = 30 + (i % 4)*(tw+gap)
    y = 30 + (i // 4)*(th+gap)
    sheet = Image.open(ROOT / 'dist/wallpaper-release/16x9-2880p' / (name+'.webp')).convert('RGBA')
    sheet = sheet.resize((tw, th), Image.Resampling.LANCZOS)
    shadow = Image.new('RGBA', (tw+40, th+40))
    ImageDraw.Draw(shadow).rectangle((20,20,tw+20,th+20), fill=(0,0,0,180))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    wall.alpha_composite(shadow, (x-12,y-8))
    wall.alpha_composite(sheet, (x,y))
    ImageDraw.Draw(wall).rectangle((x,y,x+tw-1,y+th-1), outline='#485261',width=1)
wall = wall.rotate(TILT_DEGREES, resample=Image.Resampling.BICUBIC, expand=True)
canvas.alpha_composite(wall, (-360, 435))

# Typography stays deterministic; only its light has a restrained bloom.
headline = Image.new('RGBA', (1600, 355))
hd = ImageDraw.Draw(headline)
hd.text((10, 0), 'A FUTURE', font=font(145,'NimbusSans-BoldItalic.otf'), fill='#eff5ea')
hd.text((0, 145), 'WORTH BUILDING.', font=font(155,'NimbusSans-BoldItalic.otf'), fill='#b1e2e8')
headline = headline.rotate(TILT_DEGREES, resample=Image.Resampling.BICUBIC, expand=True)
glow = headline.filter(ImageFilter.GaussianBlur(15))
glow.putalpha(glow.getchannel('A').point(lambda a: int(a*.20)))
canvas.alpha_composite(glow,(83,107))
canvas.alpha_composite(headline,(83,107))

draw = ImageDraw.Draw(canvas)
draw.text((1770, 107), '42', font=font(191,'NimbusSans-BoldItalic.otf'), fill='#eff5ea')
draw.text((1778, 312), 'p(bloom)', font=font(30,'NimbusSans-Bold.otf'), fill='#d9e7e7')
draw.text((1778, 358), 'WALLPAPERS', font=font(30,'NimbusSans-Bold.otf'), fill='#9bb1c3')
# Footer darkens the cropped edge, leaving the invitation and images dominant.
fade = Image.new('RGBA',(W,100))
fd = ImageDraw.Draw(fade)
for y in range(100):
    fd.line((0,y,W,y),fill=(9,15,27,int(245*y/99)))
canvas.alpha_composite(fade,(0,H-100))
canvas.convert('RGB').save(OUT, quality=94, method=6)
print(OUT)
