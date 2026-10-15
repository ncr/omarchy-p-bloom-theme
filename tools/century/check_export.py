"""Blender regression: a wire emerges from behind a box in its last interval."""
import sys,tempfile,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/hardware3d')]
import family_core as g
from century.exporter import export

g.reset()
folder=Path(tempfile.mkdtemp(prefix='century-clip-'))
g.OUT=folder;g.STUDY=folder
g.box('occluder',(0,-1,0),(2,1,2))
g.wire('test seam',[(-1.5,0,0),(1.5,0,0)],.01,'detail')
export('last-interval',0,0)
paths=[p for p in json.loads((folder/'last-interval.json').read_text())['paths'] if p['name']=='test seam']
assert len(paths)==2,paths
spans=sorted((min(p[0] for p in q['points']),max(p[0] for p in q['points'])) for q in paths)
assert abs(spans[0][0]+1.5)<.001 and abs(spans[0][1]+1)<.01,spans
assert abs(spans[1][0]-1)<.01 and abs(spans[1][1]-1.5)<.001,spans
print('PASS: both visible ends survive; central occluded interval stays hidden.',flush=True)
os._exit(0)
