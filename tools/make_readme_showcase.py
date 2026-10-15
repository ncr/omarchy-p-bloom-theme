#!/usr/bin/env python3
"""Compose the README's full-sheet/detail card from unchanged production pixels."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'previews/wallpaper-detail.webp'
W,H=2400,1050
BG='#090d16'
TEXT='#d9e8ff'
MUTED='#94a6bf'
BORDER='#273044'
source=Image.open(ROOT/'backgrounds/03-fusion-transport.webp').convert('RGB')
canvas=Image.new('RGB',(W,H),BG)
draw=ImageDraw.Draw(canvas)
font=ImageFont.truetype('/usr/share/fonts/gsfonts/NimbusSans-Regular.otf',25)
bold=ImageFont.truetype('/usr/share/fonts/gsfonts/NimbusSans-Bold.otf',36)

def label(text,xy):
    x,y=xy
    for char in text:
        draw.text((x,y),char,font=font,fill=MUTED)
        x+=draw.textlength(char,font=font)+3

# One full 16:9 sheet and an actual native-resolution crop, aligned on a grid.
full_box=(40,102,1560,957)
detail_box=(1600,102,2360,957)
canvas.paste(source.resize((1520,855),Image.Resampling.LANCZOS),full_box[:2])
crop=source.crop((2210,640,3110,1652))
canvas.paste(crop.resize((760,855),Image.Resampling.LANCZOS),detail_box[:2])
for box in (full_box,detail_box):draw.rectangle(box,outline=BORDER,width=2)
label('FULL WALLPAPER', (40,48))
label('PROPULSION DETAIL', (1600,48))
draw.text((40,984),'FUSION TRANSPORT',font=bold,fill=TEXT)
draw.text((1600,990),'Original linework · enlarged from the 5K render',font=font,fill=MUTED)
canvas.save(OUT,quality=94,method=6)
print(OUT)
