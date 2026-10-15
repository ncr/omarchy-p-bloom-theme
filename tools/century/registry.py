"""Small locked status updates allow independent build/render/QA workers."""
import fcntl,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];CAT=ROOT/'docs/century/catalog.json'
def update(number,patch):
    def merge(dst,src):
        for k,v in src.items():
            if isinstance(v,dict) and isinstance(dst.get(k),dict):merge(dst[k],v)
            else:dst[k]=v
    with open(CAT.with_suffix('.lock'),'a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX);entries=json.loads(CAT.read_text())
        e=next(e for e in entries if e['number']==number);merge(e,patch)
        tmp=CAT.with_suffix(f'.{os.getpid()}.tmp');tmp.write_text(json.dumps(entries,indent=2,ensure_ascii=False)+'\n');tmp.replace(CAT)
