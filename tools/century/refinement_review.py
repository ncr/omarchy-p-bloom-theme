#!/usr/bin/env python3
"""Publish the selected ten with native before/after switching and review sheets."""
import json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from century.editorial import DATA
OUT=ROOT/'concepts/century';REVIEW=OUT/'refined-ten'


def main():
    import argparse
    global REVIEW
    parser=argparse.ArgumentParser();parser.add_argument('--batch',type=int,choices=(1,2),default=1);args=parser.parse_args()
    selected=DATA
    if args.batch==2:
        from century.editorial_second import DATA as selected
        REVIEW=OUT/'refined-next-ten'
    entries=[e for e in json.loads((ROOT/'docs/century/catalog.json').read_text()) if e['number'] in selected]
    template=(ROOT/'tools/century/gallery.html').read_text()
    template=template.replace('Century — 100 nowych blueprintów','Century — dopracowana dziesiątka')
    template=template.replace('CENTURY / 100','CENTURY / SELECTED TEN')
    template=template.replace('Nowe urządzenia, historie i rysunki techniczne.', '10 dopracowanych tapet. W podglądzie B przełącza PRZED / PO; geometria i skala obrazu pozostają porównywalne.')
    template=template.replace('100 autorskich koncepcji. 300 projekcji z modeli 3D.', '10 wybranych projektów z kolekcji Century. Porównanie obejmuje oba natywne formaty.')
    template=template.replace("shown.length+' / 100'", "shown.length+' / 10'")
    template=template.replace('<button id="info"', '<button id="compare" aria-pressed="false">Pokaż PRZED · B</button><button id="info"')
    template=template.replace('let shown=catalog.slice()', 'let before=false;\nlet shown=catalog.slice()')
    template=template.replace("const native=e=>$('format').value+'/'", "const native=e=>(before?'before/':'../')+$('format').value+'/'")
    template=template.replace("const preview=e=>'previews/'", "const preview=e=>'../previews/'")
    template=template.replace("+' / '+e.title;", "+' / '+e.title+(before?' / PRZED':' / PO');")
    template=template.replace("$('close').onclick=close;", "function compare(){before=!before;$('compare').textContent=before?'Pokaż PO · B':'Pokaż PRZED · B';$('compare').setAttribute('aria-pressed',String(before));display()}\n$('compare').onclick=compare;\n$('close').onclick=close;")
    template=template.replace("else if(e.key.toLowerCase()==='i')", "else if(e.key.toLowerCase()==='b'){e.preventDefault();compare()}else if(e.key.toLowerCase()==='i')")
    if args.batch==2:
        template=template.replace('Century — dopracowana dziesiątka','Century — druga dopracowana dziesiątka').replace('CENTURY / SELECTED TEN','CENTURY / SECOND TEN')
    public=[{k:e[k] for k in ('number','slug','title','domain','purpose','narrative','real_basis','required_breakthroughs')} for e in entries]
    (REVIEW/'index.html').write_text(template.replace('/*CATALOG*/',json.dumps(public,ensure_ascii=False).replace('</','<\\/')))
    font=ImageFont.truetype('/usr/share/fonts/gsfonts/NimbusSans-Regular.otf',22)
    for fmt in ('wide','16-9'):
        hh=338 if fmt=='wide' else 450
        sheet=Image.new('RGB',(1600,(hh+35)*5),(9,14,21));draw=ImageDraw.Draw(sheet)
        for i,e in enumerate(entries):
            stem=f"{e['number']:03d}-{e['slug']}";path=OUT/fmt/(stem+'.webp')
            with Image.open(path) as im:
                im.thumbnail((790,hh));sheet.paste(im,((i%2)*800,(i//2)*(hh+35)))
            draw.text(((i%2)*800+8,(i//2)*(hh+35)+hh+4),f"{e['number']:03d}  {e['title']}",font=font,fill=(200,218,230))
            ch=675 if fmt=='wide' else 900
            comparison=Image.new('RGB',(1600,ch*2+65),(9,14,21));dc=ImageDraw.Draw(comparison)
            for j,p in enumerate((REVIEW/'before'/fmt/(stem+'.webp'),path)):
                with Image.open(p) as im:
                    im.thumbnail((1600,ch));comparison.paste(im,((1600-im.width)//2,j*(ch+30)+25))
                dc.text((14,j*(ch+30)+3),'PRZED' if j==0 else 'PO',font=font,fill=(200,218,230))
            comparison.save(REVIEW/(stem+'-'+fmt+'-compare.jpg'),quality=95)
        sheet.save(REVIEW/('contact-'+fmt+'.jpg'),quality=95)
    print('Ten-entry before/after gallery, 20 comparisons and two contact sheets ready.')

if __name__=='__main__':main()
