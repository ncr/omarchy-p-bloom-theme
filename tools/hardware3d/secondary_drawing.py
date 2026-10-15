"""Uniform-scale auxiliary views exported from the same solids as the primary drawing."""
from hardware3d.family_drawing import data
from path_cleanup import trace
from sheet import WHITE,ARC,GOLD

def fitted_size(name,width,height):
 pts=[p for path in data(name)['paths'] for p in path['points']]
 w=max(p[0] for p in pts)-min(p[0] for p in pts)
 h=max(p[1] for p in pts)-min(p[1] for p in pts)
 k=min(width/w,height/h)
 return w*k,h*k

def view(s,name,cx,cy,width,height,angle=0):
 d=data(name);pts=[p for path in d['paths'] for p in path['points']]
 x0=min(x for x,y in pts);x1=max(x for x,y in pts);y0=min(y for x,y in pts);y1=max(y for x,y in pts)
 scale=min(width/(x1-x0),height/(y1-y0))
 c=s.c;c.save();c.translate(cx,cy);c.rotate(angle);c.scale(scale,scale);c.translate(-(x0+x1)/2,-(y0+y1)/2)
 for path in d['paths']:
  role=path['role']
  a,w,color=(.88,.85,WHITE) if role in ('structure','plate') else (.66,.5,WHITE)
  if role in ('accent','hologram','fine'):a,w,color=.64,.45,ARC
  elif role=='cable':a,w,color=.64,.45,GOLD
  elif role=='shell':a,w=.44,.45
  trace(c,path)
  s._stroke(a,w/scale,None,color)
 c.restore()
 return {name:(cx+(px-(x0+x1)/2)*scale,cy+(py-(y0+y1)/2)*scale) for name,(px,py) in d.get("anchors",{}).items()}
