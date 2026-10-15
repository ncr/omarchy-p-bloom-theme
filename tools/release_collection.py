#!/usr/bin/env python3
"""Package the retained registry, using native masters for one branch format.

Never scans rejected concepts. --source-root can point to the development
checkout while --root points to a separate release worktree. Existing images
outside the retained filename set cause an error rather than being deleted.
"""
import argparse,hashlib,json,shutil
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--format',choices=['wide','16-9'],required=True)
 p.add_argument('--root',type=Path,default=ROOT)
 p.add_argument('--source-root',type=Path,default=ROOT)
 a=p.parse_args();root=a.root.resolve();src=a.source_root.resolve()
 # Superseded: backgrounds/ now holds the light default set of the release
 # matrix. Render with render_wallpaper_sets.py, package with
 # package_wallpaper_profiles.py; this tool would overwrite it with 5K masters.
 if json.loads((root/'docs/collection/profiles.json').read_text()).get('version',1)>=2:
  p.error('superseded by tools/render_wallpaper_sets.py and tools/package_wallpaper_profiles.py')
 cat=json.loads((src/'docs/collection/catalog.json').read_text())
 assert cat['finalized_count']==len(cat['finalized'])==42
 records=[];size=(5120,2160) if a.format=='wide' else (5120,2880)
 for e in cat['finalized']:
  source=src/e['source']
  if a.format=='16-9':source=(source.parent/'16-9'/source.name) if e['id'].startswith('o') else source.parent.parent/'16-9'/source.name
  assert source.is_relative_to(src) and source.is_file(),source
  with Image.open(source) as im:assert im.size==size and im.format=='WEBP';im.verify()
  records.append(dict(id=e['id'],title=e['title'],source=source,filename=source.name,sha256=digest(source)))
 assert len({r['filename'] for r in records})==42
 out=root/'backgrounds';out.mkdir(exist_ok=True)
 unknown={f.name for f in out.glob('*.webp')}-{r['filename'] for r in records}
 assert not unknown,('Unexpected background files; resolve explicitly',unknown)
 previews=root/'previews';previews.mkdir(exist_ok=True)
 cols=3;cw=600;ch=round(cw*size[1]/size[0]);label=27
 contact=Image.new('RGB',(cols*cw,14*(ch+label)),(10,12,16));draw=ImageDraw.Draw(contact)
 for i,r in enumerate(records):
  dest=out/r['filename'];shutil.copy2(r['source'],dest);assert digest(dest)==r['sha256']
  with Image.open(dest) as im:
   thumb=im.convert('RGB');thumb.thumbnail((1600,1000));thumb.save(previews/r['filename'],quality=87,method=6)
   thumb=im.resize((cw,ch),Image.Resampling.LANCZOS);x=(i%cols)*cw;y=(i//cols)*(ch+label)
   contact.paste(thumb,(x,y));draw.text((x+10,y+ch+6),r['title'],fill=(208,217,233))
  r['source']=str(r['source'].relative_to(src));r['path']='backgrounds/'+r['filename']
 contact.save(previews/'wallpapers.webp',quality=87,method=6)
 report={'count':42,'format':a.format,'native_size':list(size),'wallpapers':records}
 (root/'docs/collection/release.json').write_text(json.dumps(report,indent=2)+'\n')
 print(f'RELEASE PASS: 42 {a.format} native masters; hashes verified')
if __name__=='__main__':main()
