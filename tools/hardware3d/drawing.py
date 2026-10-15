"""Opt-in Quantum Simulator assembly study; typography stays in the sheet engine."""
import json
from pathlib import Path
from functools import lru_cache
from sheet import WHITE,ARC,GOLD
@lru_cache(None)
def data():return json.loads((Path(__file__).resolve().parents[1]/'assets/hardware3d/main.json').read_text())

def main(s,mx,my):
 d=data();scale=1.06;dy=354
 c=s.c;c.save();c.translate(mx,my+dy);c.scale(scale,scale)
 styles={'shell':(.48,.6,WHITE),'plate':(.88,1.05,WHITE),'structure':(.8,.85,WHITE),'detail':(.51,.42,WHITE),'accent':(.85,.7,ARC),'cable':(.54,.48,GOLD),'fine':(.38,.28,ARC)}
 for p in d['paths']:
  pts=p['points'];c.new_path();c.move_to(*pts[0])
  for point in pts[1:]:c.line_to(*point)
  a,w,col=styles[p['role']];s._stroke(a,w,None,col)
 c.restore()
 # Fixed label rails keep the assembly readable in both page formats.
 labels=[('PULSE-TUBE COOLER',None,350,-436),('CONTROL CHIPS','AT 4 K, BESIDE THE WIRING',355,-288),('OPTICAL LINK','TO NEIGHBOUR CRYOSTATS',355,-173),('HEAT EXCHANGER',None,355,-60),('MIXING CHAMBER','HELIUM-3 IN HELIUM-4',355,67),('MAGNETIC SHIELD',None,355,180),('PROCESSOR STACK','6 TILES × 1 700 LOGICAL QUBITS',-345,274),('CONTROL LINES',None,-345,-260)]
 from label_layout import LABEL_OFFSETS
 for name,sub,ex,ey in labels:
  x,y=d['anchors'][name];x*=scale;y=y*scale+dy
  ox,oy=LABEL_OFFSETS.get('quantum-simulator',{}).get(name,(0,0))
  s.leader(mx+x,my+y,ex-x-ox,ey-y-oy,100 if ex>0 else -100,name,sub)
 sx=mx-490
 s.text('THERMAL STAGES',sx,my-417,6.5,a=.6,align='r')
 s.ln(sx+10,my-397,sx+10,my+140,.4,.5)
 for stage in d['levels']:
  x,y=stage['anchor'];y=y*scale+dy
  s.text(stage['label'],sx,my+y+3,7.5,a=.8,align='r')
  s.ln(sx+10,my+y,sx+20,my+y,.65,.6)
 s.text('A / AXONOMETRIC CUTAWAY',mx-180,my+461,7,a=.65)
 s.text('VACUUM JACKET AND SHIELDS PARTLY REMOVED',mx-180,my+477,6,a=.4)

def detail(s,qx,qy):
 # Enlarged board drawing from the same KiCad carrier layout used by Blender.
 d=json.loads((Path(__file__).resolve().parents[1]/'assets/hardware3d/carrier.json').read_text())
 c=s.c;c.save();c.translate(qx,qy);c.scale(2.7,2.7)
 s.rect(-48,-34,96,68,.85,.55)
 for p in d['parts']:s.rect(p['x']-p['w']/2,p['y']-p['h']/2,p['w'],p['h'],.7,.24,fill=.04,color=ARC if p['kind']=='package' else WHITE)
 for x,y,w,h in d['pads']:s.rect(x-w/2,y-h/2,w,h,.5,.16,color=GOLD)
 for line in d['tracks']:s.poly(line,.5,.16,close=False,color=ARC)
 for x in (-43,43):
  for y in (-29,29):s.circ(x,y,1.8,.7,.3)
 c.restore()
 s.view_label(qx,qy+164,'C','PROCESSOR CARRIER','ENLARGED / ONE OF SIX BOARDS')
