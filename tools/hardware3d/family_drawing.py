"""Shared page composition for individually modeled hardware assemblies."""
import os,json
from pathlib import Path
from functools import lru_cache
from sheet import WHITE,ARC,GOLD
ROOT=Path(__file__).resolve().parents[1]/'assets/hardware-family'
SUBJECTS={'greener','sky-racer','organ-foundry','air-refinery','aroma-organ','cortical-mesh','tether-climber','fusion-transport','volumetric-stage','bounder'}
def enabled(name):return name in SUBJECTS and os.environ.get('PBLOOM_HARDWARE_SET','retro')=='retro'
@lru_cache(None)
def data(name):
 from path_cleanup import load
 return load(ROOT/(name+'.json'))
@lru_cache(None)
def labels():return json.loads((ROOT/'labels.json').read_text())
def draw(s,name,mx,my):
 d=data(name);pts=[p for path in d['paths'] for p in path['points']];x0=min(x for x,y in pts);x1=max(x for x,y in pts);y0=min(y for x,y in pts);y1=max(y for x,y in pts)
 scale=min(620/(x1-x0),695/(y1-y0));dx=-(x0+x1)/2*scale;dy=-(y0+y1)/2*scale-25
 c=s.c;c.save();c.translate(mx+dx,my+dy);c.scale(scale,scale)
 styles={'shell':(.39,.47,WHITE),'plate':(.87,1,WHITE),'structure':(.85,.86,WHITE),'detail':(.53,.43,WHITE),'accent':(.88,.65,ARC),'cable':(.57,.42,GOLD),'fine':(.40,.28,ARC),'hologram':(.60,.40,ARC),'figure':(.95,.95,WHITE),'grass':(.76,.60,WHITE),'radiator':(.66,.35,ARC)}
 from path_cleanup import trace
 for p in d['paths']:
  trace(c,p)
  a,w,col=styles[p['role']];s._stroke(a,w/max(.75,scale**.35),None,col)
 c.restore()
 annotation={v[0]:v[1] if len(v)>1 else None for v in labels()[name]}
 # labels.json decides which parts are called out; an exported anchor without a label stays silent
 positions={lab:(x*scale+dx,y*scale+dy) for lab,(x,y) in d['anchors'].items() if lab in annotation}
 for lab,(sx,sy) in ANCHOR_SHIFTS.get(name,{}).items():
  x,y=positions[lab];positions[lab]=(x+sx,y+sy)
 callouts(s,positions,annotation,mx,my)
 return {lab:(mx+x,my+y) for lab,(x,y) in positions.items()}


def callouts(s,positions,annotation,mx,my,column=383,top=-345,bottom=(205,290),sides=None):
 """The callouts of every original sheet's main view. positions are relative to (mx, my).

 Labels stay in two columns but sit as close to the height of the part they name as the spacing
 allows, so leaders run short and nearly level instead of reaching across the drawing to fixed
 slots. The left column stops higher (bottom[0]): the legend sits under it. Labels split into the
 columns by the x of their part, unless sides (label -> -1 or 1) places them."""
 gap=50+2*s.type_growth(6.5)  # name and subtitle of one label, then clear air to the next
 from label_layout import LABEL_OFFSETS,COMPACT_OFFSETS
 def offsets(lab):  # s.leader adds the reviewed offsets back; the layout here is already final
  subject=getattr(s,'subject','')
  ox,oy=LABEL_OFFSETS.get(subject,{}).get(lab,(0,0))
  if not s.wide:
   cx,cy=COMPACT_OFFSETS.get(subject,{}).get(lab,(0,0));ox+=cx;oy+=cy
  return ox,oy
 ordered=sorted(positions,key=lambda lab:positions[lab][0]);split=len(ordered)//2
 if sides:
  columns=([lab for lab in ordered if sides[lab]<0],[lab for lab in ordered if sides[lab]>0])
 else:
  columns=(ordered[:split],ordered[split:])
 for side,group,low in [(-1,columns[0],bottom[0]),(1,columns[1],bottom[1])]:
  group.sort(key=lambda lab:positions[lab][1])
  ys=[min(low,max(top,positions[lab][1])) for lab in group]
  for i in range(1,len(ys)):ys[i]=max(ys[i],ys[i-1]+gap)
  if ys and ys[-1]>low:
   ys[-1]=low
   for i in range(len(ys)-2,-1,-1):ys[i]=min(ys[i],ys[i+1]-gap)
  # A label whose name or subtitle would sit on the framing's horizontal datum moves to the
  # nearest height where it clears it, within the room its neighbours leave.
  datum=getattr(s,'datum_y',None)
  if datum is not None:
   d0=datum-my;g=s.type_growth(7.5);above,below=14+g,14+g
   for i in range(len(ys)):
    if not ys[i]-above<=d0<=ys[i]+below:continue
    lo=ys[i-1]+gap if i else top;hi=ys[i+1]-gap if i+1<len(ys) else low
    for d in sorted(range(-60,61,2),key=abs):
     y=ys[i]+d
     if lo<=y<=hi and not y-above<=d0<=y+below:ys[i]=y;break
  slot=lambda i,lab,side=side,ys=ys:(side*column,ys[i])
  group=uncrossed(group,positions,slot)
  for i,lab in enumerate(group):
   x,y=positions[lab];ex,ey=slot(i,lab);ox,oy=offsets(lab)
   s.leader(mx+x,my+y,ex-x-ox,ey-y-oy,side*95,lab,annotation.get(lab))


# Anchor dots that land on a neighbouring part in the projection (drawing units):
# the dot moves onto the visible part it names.
ANCHOR_SHIFTS={'sky-racer':{'FOLDING ARM':(-20,-4),          # onto the fold hinge where the wing meets the body
                            'LITHIUM-AIR PACK':(-50,48)},   # off the wing, onto the energy cassette under the flank
               'aroma-organ':{'BASE ODORANT':(17,-41),       # off the clearing fan, onto a cartridge
                              'MANIFOLD':(143,-30)},         # away from the mixing chip, onto a capillary branch
               'air-refinery':{'MIRROR FIELD':(-73,58)},     # off the base plate, onto a mirror
               'cortical-mesh':{'RECORDING SITE':(-224,3),     # a node on the mesh's near edge: a short leader
                                'MESH THREAD':(-52,59)},       # off a node, onto the thread between two nodes
               'fusion-transport':{'DROPLET RADIATOR':(-60,-104)},  # off the lower boom, onto the droplet sheet near its top
               'tether-climber':{'POWER BEAM':(0,80),        # off the receiver plate, onto the beam under it
                                 'DEBRIS SHIELD':(70,-57)}}  # off the ribbon's edge, onto the dome


def uncrossed(group,positions,elbow):
 """Label order on one side, top to bottom. Sorting by anchor height can still
 cross two leaders (an anchor far inside sits lower than its neighbour's);
 then the order with no crossing and the least leader length wins."""
 from itertools import permutations
 def cross(a,b,c,d):
  o=lambda p,q,r:(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
  return o(a,b,c)*o(a,b,d)<0 and o(c,d,a)*o(c,d,b)<0
 def crossings(order):
  seg=[(positions[lab],elbow(i,lab)) for i,lab in enumerate(order)]
  return sum(cross(*seg[i],*seg[j]) for i in range(len(seg)) for j in range(i+1,len(seg)))
 if not crossings(group) or len(group)>6:return group
 def length(order):
  return sum(((positions[lab][0]-elbow(i,lab)[0])**2+(positions[lab][1]-elbow(i,lab)[1])**2)**.5 for i,lab in enumerate(order))
 return list(min(permutations(group),key=lambda o:(crossings(o),length(o))))
