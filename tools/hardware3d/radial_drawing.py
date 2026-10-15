"""Independent poster-content interpretation: serviceable radial quantum engine."""
import json
from pathlib import Path
from functools import lru_cache
from sheet import WHITE,ARC,GOLD
from path_cleanup import trace
@lru_cache(None)
def data(view):
 from path_cleanup import load
 return load(Path(__file__).resolve().parents[1]/'assets/radial-quantum'/f'{view}.json')

def paths(s,d,tx,ty,scale):
 c=s.c;c.save();c.translate(tx,ty);c.scale(scale,scale)
 styles={'shell':(.44,.5,WHITE),'plate':(.88,1.05,WHITE),'structure':(.87,.85,WHITE),'detail':(.5,.4,WHITE),'accent':(.88,.62,ARC),'cable':(.62,.43,GOLD),'fine':(.42,.28,ARC)}
 for p in d['paths']:
  trace(c,p)
  a,w,col=styles[p['role']];s._stroke(a,w,None,col)
 c.restore()

def main(s,mx,my):
 d=data('main');sc=1.03;dy=273
 paths(s,d,mx-22,my+dy,sc)
 labels={'PULSE-TUBE COOLERS':'CLOSED-CYCLE / NO LIQUID HELIUM','4 K CONTROLLERS':'LOCAL CONTROL / SHORT COLD LINKS','OPTICAL INTERCONNECT':None,'COMPUTE CASSETTES':'6 × 1 700 LOGICAL QUBITS','BASE-STAGE MANIFOLD':'COMMON COLD CORE','NESTED THERMAL SHIELDS':'50 K / 4 K / 100 mK','VACUUM ENCLOSURE':'ROOM-TEMPERATURE OUTER WALL','SERVICE CARRIAGE':'WITHDRAW COMPLETE COLD ASSEMBLY'}
 # The manifold's anchor keeps its exported key; the label leaves 8 mK to the field notes.
 anchor={'BASE-STAGE MANIFOLD':'8 mK MANIFOLD'}
 positions={}
 for name in labels:
  x,y=d['anchors'][anchor.get(name,name)];dx_,dy_=SHIFTS.get(name,(0,0))
  positions[name]=(x*sc-22+dx_,y*sc+dy+dy_)
 from hardware3d.family_drawing import callouts
 callouts(s,positions,labels,mx,my)


# Anchor dots that land on a neighbouring part (main-view units): the dot moves onto the part it names.
SHIFTS={'VACUUM ENCLOSURE':(-79,15),   # off an inner shield ring, onto the bolted outer flange of the vessel
        'COMPUTE CASSETTES':(-4,60)}   # off the arm the 4 K controller sits on, onto the lower right cassette

def detail(s,qx,qy):
 d=data('detail');ps=[p for path in d['paths'] for p in path['points']];cx=(min(x for x,y in ps)+max(x for x,y in ps))/2;cy=(min(y for x,y in ps)+max(y for x,y in ps))/2
 sc=2.7;paths(s,d,qx-cx*sc,qy-cy*sc,sc)
 s.view_label(qx,qy+183,'C','COMPUTE CASSETTE','COLD TILE + OPTICAL TERMINATION')
