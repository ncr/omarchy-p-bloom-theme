#!/usr/bin/env python3
"""Compare the actual diagram fragments, independently of full-page thumbnails."""
import json,html,argparse
from pathlib import Path
from PIL import Image
from subject_diagrams import FIGURES,RETRO_REFINED
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'concepts/century/individual-diagrams'
def main():
 global OUT
 ap=argparse.ArgumentParser();ap.add_argument('--revision',default='individual-diagrams',choices=['individual-diagrams','retro-diagrams']);args=ap.parse_args()
 OUT=ROOT/'concepts/century'/args.revision
 data=json.loads((OUT/'review.json').read_text());cards=[];records=[]
 priority=['proxy','fusion-transport','bounder','manta-foil','advice-filter','seam-surgeon'] if args.revision=='retro-diagrams' else ['seam-surgeon']
 entries=sorted(data['wallpapers'],key=lambda e:(priority.index(e['slug']) if e['slug'] in priority else len(priority),e['id']))
 for e in entries:
  for side in (['left','right'] if e['slug']=='tether-climber' else ['left' if e['id'][0]=='o' else 'right']):
   key='tether-ribbon' if e['slug']=='tether-climber' and side=='right' else e['slug']
   if args.revision=='retro-diagrams' and key not in RETRO_REFINED:continue
   title=FIGURES[key][1];name=e['title']+' / '+side.upper();paths={}
   for fmt in ('wide','16-9'):
    paths[fmt]={};ex=0 if fmt=='wide' else 360
    x=140 if side=='left' else 2560-650;y=(514 if side=='left' else 552)+ex*.63
    box=tuple(round(z*2) for z in (x-10,y-15,x+450,y+210))
    for state in ('before','after'):
     dest=OUT/'fragments'/fmt/(key+'-'+state+'.jpg');dest.parent.mkdir(parents=True,exist_ok=True)
     with Image.open(OUT/e['files'][fmt][state]) as im:im.crop(box).save(dest,quality=97)
     paths[fmt][state]=str(dest.relative_to(OUT))
   records.append(dict(key=key,wallpaper=e['id'],side=side,title=title,files=paths))
   detail='<p>'+html.escape(RETRO_REFINED[key])+'</p>' if args.revision=='retro-diagrams' else ''
   cards.append('<article><h2>'+html.escape(name)+'</h2><p>'+html.escape(title)+'</p>'+detail+'<div class="pair">'+''.join('<figure><figcaption>'+state.upper()+'</figcaption><a href="'+paths['wide'][state]+'"><img loading="lazy" src="'+paths['wide'][state]+'" alt="'+html.escape(name+' '+state)+'"></a></figure>' for state in ('before','after'))+'</div></article>')
 page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>p(bloom) / 35 individual diagrams</title><style>body{margin:0;padding:3vw;background:#0b121a;color:#d7e2e9;font:16px/1.5 system-ui}h1{font-size:26px}h2{font-size:17px;margin:0}p{color:#a6bbc8}a{color:#b8d4df}article{margin:30px 0 60px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}figure{margin:0}figcaption{font-size:11px;color:#b9a374;letter-spacing:.12em}img{width:100%;display:block}@media(max-width:700px){.pair{grid-template-columns:1fr}}</style><h1>35 INDIVIDUAL DIAGRAMS</h1><p>Actual fragments from the previous and current native wallpapers. Every replacement has its own composition.</p><p><a href="./">Full wallpaper comparison / both formats</a> · <a href="fragments.json">Fragment manifest / both formats</a></p>'''+''.join(cards)+'</html>'
 if args.revision=='retro-diagrams':
  page=page.replace('35 individual diagrams','Retro-future diagrams').replace('35 INDIVIDUAL DIAGRAMS','26 RETRO-FUTURE DIAGRAMS').replace('Actual fragments from the previous and current native wallpapers. Every replacement has its own composition.','The individual schematic figures, softened through shaped castings, swept tubes and material contours. Precise optical rays, event traces and ratchet teeth stay sharp where function requires it.')
 (OUT/'fragments.html').write_text(page);(OUT/'fragments.json').write_text(json.dumps(records,indent=2)+'\n')
 print(str(len(records))+' before / after fragment pairs, in both formats')
if __name__=='__main__':main()
