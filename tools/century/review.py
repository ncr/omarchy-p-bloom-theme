#!/usr/bin/env python3
"""Review contact sheets: whole pages plus large main-view crops."""
import json,sys,argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'concepts/century';CAT=ROOT/'docs/century/catalog.json'
FONT=ImageFont.truetype('/usr/share/fonts/gsfonts/NimbusSans-Regular.otf',19)
def main():
 p=argparse.ArgumentParser();p.add_argument('--domain');p.add_argument('--all',action='store_true');a=p.parse_args();c=json.loads(CAT.read_text())
 domains=list(dict.fromkeys(e['domain'] for e in c)) if a.all else [a.domain]
 for domain in domains:
  items=[e for e in c if e['domain']==domain];page=Image.new('RGB',(1600,1800),(9,14,21));hero=Image.new('RGB',(1600,1800),(9,14,21));d=ImageDraw.Draw(page);dh=ImageDraw.Draw(hero)
  for i,e in enumerate(items):
   path=OUT/'wide'/f"{e['number']:03d}-{e['slug']}.webp"
   if not path.exists():continue
   im=Image.open(path);thumb=im.copy();thumb.thumbnail((790,333));x=(i%2)*800;y=(i//2)*360;page.paste(thumb,(x,y));d.text((x+13,y+337),f"{e['number']:03d}  {e['title']}",font=FONT,fill=(220,226,232))
   h=im.crop((1740,295,3100,1710));h.thumbnail((386,402));x=(i%4)*400;y=(i//4)*593;hero.paste(h,(x+7,y+19));dh.text((x+8,y+439),f"{e['number']:03d} {e['title']}",font=FONT,fill=(220,226,232))
   dh.text((x+8,y+468),f"{e.get('built',{}).get('parts','?')} parts",font=FONT,fill=(125,150,165))
  page.save(OUT/'qa'/f'{domain}-pages.jpg',quality=93);hero.save(OUT/'qa'/f'{domain}-heroes.jpg',quality=94)
  compact=Image.new('RGB',(1600,1310),(9,14,21));dc=ImageDraw.Draw(compact)
  for i,e in enumerate(items):
   path=OUT/'16-9'/f"{e['number']:03d}-{e['slug']}.webp"
   if not path.exists():continue
   with Image.open(path) as im:
    im.thumbnail((520,293));x=(i%3)*534;y=(i//3)*327;compact.paste(im,(x,y))
   dc.text((x+10,y+298),f"{e['number']:03d}  {e['title']}",font=FONT,fill=(220,226,232))
  compact.save(OUT/'qa'/f'{domain}-compact.jpg',quality=94)
 if a.all:
  overview=Image.new('RGB',(1600,1160),(9,14,21));do=ImageDraw.Draw(overview)
  do.text((16,16),'CENTURY / 100 — WYBÓR Z KOLEKCJI',font=FONT,fill=(220,226,232))
  for i,n in enumerate((1,31,44,56,87,99)):
   e=next(e for e in c if e['number']==n)
   with Image.open(OUT/'wide'/f"{n:03d}-{e['slug']}.webp") as im:
    im.thumbnail((790,333));x=(i%2)*800;y=56+(i//2)*366;overview.paste(im,(x,y))
   do.text((x+14,y+338),f"{n:03d}  {e['title']}",font=FONT,fill=(186,204,220))
  overview.save(OUT/'overview.jpg',quality=95)
if __name__=='__main__':main()
