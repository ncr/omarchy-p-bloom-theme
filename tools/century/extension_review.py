#!/usr/bin/env python3
"""Local comparison gallery and native crops for the eight new sheets."""
import json,hashlib,html
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'concepts/century/extension-42'
def main():
 OUT.mkdir(exist_ok=True);entries=[e for e in json.loads((ROOT/'docs/century/catalog.json').read_text()) if e['number']>100]
 cards=[]
 for e in entries:
  stem=f"{e['number']:03d}-{e['slug']}";rows=[]
  for fmt in ('wide','16-9'):
   source=ROOT/'concepts/century'/fmt/(stem+'.webp');im=Image.open(source)
   # Separate native inspection crops avoid mistaking thumbnail legibility for native type.
   for side,bbox in [('B',(180,100,1350,965 if fmt=='wide' else 1160)),('C',(3700,100,4910,965 if fmt=='wide' else 1160)),('notes',(3700,im.height-570,4750,im.height-125))]:
    im.crop(bbox).save(OUT/f'{stem}-{fmt}-{side}.jpg',quality=96)
   thumb=im.copy();thumb.thumbnail((1600,1000));thumb.save(OUT/f'{stem}-{fmt}.jpg',quality=93)
   rows.append(f'<div><h3>{fmt}</h3><a href="../{fmt}/{stem}.webp"><img loading="lazy" src="{stem}-{fmt}.jpg"></a><p><a href="{stem}-{fmt}-B.jpg">B 1:1</a> · <a href="{stem}-{fmt}-C.jpg">C 1:1</a> · <a href="{stem}-{fmt}-notes.jpg">Field Notes 1:1</a> · <a href="before/{fmt}/{stem}.webp">First pass</a></p></div>')
  cards.append(f'<article id="{e["slug"]}"><h2>{html.escape(e["title"])}</h2>'+''.join(rows)+'</article>')
 (OUT/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Destiny — extension to 42</title><style>body{background:#0b111a;color:#d3ddeb;font:16px system-ui;margin:32px}article{margin:48px 0;border-top:1px solid #394452}img{width:100%;max-width:1600px;display:block}a{color:#a2caff}p{line-height:1.8}h2{letter-spacing:.15em}</style><h1>42 wallpapers · eight new machines</h1><p>Native ultrawide and 16:9; first-pass images preserved. Click the full image for its native master.</p>'+''.join(cards))
 print(OUT/'index.html')
if __name__=='__main__':main()
