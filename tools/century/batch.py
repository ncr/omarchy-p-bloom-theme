#!/usr/bin/env python3
"""Bounded, resumable native exports. Finished masters are replaced atomically."""
import argparse,json,subprocess,sys
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--limit',type=int,default=32,help='Maximum native files in this invocation')
    p.add_argument('--workers',type=int,default=4)
    p.add_argument('--check',action='store_true')
    p.add_argument('--maintenance',action='store_true')
    a=p.parse_args()
    if a.limit<1 or not 1<=a.workers<=4:p.error('Use a positive limit and 1–4 workers')
    entries=json.loads((ROOT/'docs/century/catalog.json').read_text());jobs=[]
    for e in entries:
        if e.get('curation',{}).get('status')=='rejected':continue
        if not e.get('built'):continue
        stamp=max((ROOT/'tools/assets/century'/(e['slug']+'-'+v+'.json')).stat().st_mtime for v in 'ABC')
        for fmt,size in [('wide',(5120,2160)),('16-9',(5120,2880))]:
            file=ROOT/'concepts/century'/fmt/f"{e['number']:03d}-{e['slug']}.webp"
            stale=not file.exists() or file.stat().st_mtime<stamp
            if not stale:
                try:
                    with Image.open(file) as im:
                        stale=im.size!=size or im.format!='WEBP';im.load()
                except (OSError,ValueError):stale=True
            if stale:jobs.append((e['number'],fmt))
    print(f'Native files to render: {len(jobs)}',flush=True)
    if a.check:return int(bool(jobs))
    def run(job):
        number,fmt=job
        cmd=[sys.executable,str(ROOT/'tools/century/render.py'),'--ids',str(number),'--format',fmt,'--force']
        if a.maintenance:cmd.append('--maintenance')
        result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
        return number,fmt,result
    failed=False
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        for f in as_completed([pool.submit(run,job) for job in jobs[:a.limit]]):
            n,fmt,r=f.result();failed|=bool(r.returncode)
            print(n,fmt,r.returncode,(r.stdout+r.stderr).strip(),flush=True)
    return int(failed)

if __name__=='__main__':sys.exit(main())
