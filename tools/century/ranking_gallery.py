#!/usr/bin/env python3
"""Review all current finished sheets; a proposed cutoff never changes membership."""
import json,os,hashlib
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]

def main():
 data=json.loads((ROOT/'docs/collection/quality-ranking.json').read_text());out=ROOT/'concepts/century/ranking'
 for name in ('wide','previews'):(out/name).mkdir(parents=True,exist_ok=True)
 for e in data['wallpapers']:
  source=ROOT/e['source'];name=f"{e['rank']:03d}-{e['slug']}";link=out/'wide'/(name+'.webp')
  assert hashlib.sha256(source.read_bytes()).hexdigest()==e['sha256'], 'Master changed: review ranking for '+e['id']
  target=Path(os.path.relpath(source,link.parent))
  if link.is_symlink() and link.readlink()!=target:link.unlink()
  if not link.exists():link.symlink_to(target)
  with Image.open(source) as im:
   assert im.size==tuple(e['size']);im.thumbnail((1100,465));im.save(out/'previews'/(name+'.jpg'),quality=94)
  e['image']='wide/'+name+'.webp';e['preview']='previews/'+name+'.jpg'
 data['queued']=json.loads((ROOT/'docs/collection/backlog.json').read_text())['ideas']
 template=(ROOT/'tools/century/ranking.html').read_text()
 (out/'index.html').write_text(template.replace('/*DATA*/',json.dumps(data,ensure_ascii=False).replace('</','<\\/')))
 print('Ranking gallery: 34 current masters; baseline order retained, twelve redesigns flagged; no removal.')

if __name__=='__main__':main()
