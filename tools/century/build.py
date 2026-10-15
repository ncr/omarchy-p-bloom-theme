"""Blender batch runner; reproducible models and line exports, no network."""
import sys,os,json,importlib,time,traceback
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from century import kit
from century.registry import update
CAT=ROOT/'docs/century/catalog.json'

def main():
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--ids',default='');p.add_argument('--domain');p.add_argument('--force',action='store_true');p.add_argument('--maintenance',action='store_true',help='Explicit later revision; bypass the one-night production deadline')
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    entries=json.loads(CAT.read_text());ids={int(x) for x in args.ids.split(',') if x}
    for entry in entries:
        if not ids and entry.get('curation',{}).get('status')=='rejected':continue
        if ids and entry['number'] not in ids:continue
        if args.domain and entry['domain']!=args.domain:continue
        if entry.get('built') and not args.force:continue
        if not args.maintenance and datetime.now(timezone.utc)>=datetime(2026,9,25,6,tzinfo=timezone.utc):
            print('DEADLINE: stopping before next model',flush=True);break
        t=time.time();print('BUILD',entry['number'],entry['slug'],flush=True)
        from century.quality_geometry import BUILDERS as quality_builders
        from century.extension_geometry import BUILDERS as extension_builders
        kit.reset(entry)
        if entry['number'] in extension_builders:
            az,el=extension_builders[entry['number']]()
        elif entry['number'] in quality_builders:
            az,el=quality_builders[entry['number']]()
        else:
            mod=importlib.import_module('century.'+entry['domain'])
            az,el=getattr(mod,entry['recipe'])()
            from century.refinement_geometry import enrich
            enrich(entry)
            from century.refinement_second_geometry import enrich as enrich_second
            enrich_second(entry)
        meta=kit.save(entry,az,el)
        entry['built']={'at':datetime.now(timezone.utc).isoformat(),'seconds':round(time.time()-t,2),'parts':meta['parts'],'views':meta['views']}
        entry['status']='built'
        update(entry['number'],{'built':entry['built'],'status':'built'})
        print('BUILT',entry['slug'],entry['built']['seconds'],flush=True)
    sys.stdout.flush();os._exit(0)
if __name__=='__main__':main()
