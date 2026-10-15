"""Resolution-independent visible lines projected from the authored Blender rig."""
import json, math
from functools import lru_cache
from pathlib import Path
from sheet import WHITE,GOLD,ARC

@lru_cache(None)
def geometry(pose):
 return json.loads((Path(__file__).parent/'assets/mannequin3d'/f'{pose}.json').read_text())

def draw(s,pose,x,y,scale=1,facing=1,stroke_scale=1):
 data=geometry(pose);c=s.c;c.save();c.translate(x,y);c.scale(scale*facing,scale)
 # Union of full projected shells clears construction lines underneath.
 for pts in data['fills']:
  c.new_path();c.move_to(*pts[0])
  for p in pts[1:]:c.line_to(*p)
  c.close_path();s.knockout()
 # Combine visible mechanical faces in one fill to avoid antialiased mesh seams.
 c.new_path()
 for pts in data.get('dark_faces',[]):
  c.move_to(*pts[0])
  for p in pts[1:]:c.line_to(*p)
  c.close_path()
 s._ink(.035,WHITE);c.fill()
 for pts in data.get('panels',[]):
  c.new_path();c.move_to(*pts[0])
  for p in pts[1:]:c.line_to(*p)
  c.close_path();s._ink(.07,WHITE);c.fill()
 for path in data['paths']:
  pts=path['points'];c.new_path();c.move_to(*pts[0])
  for p in pts[1:]:c.line_to(*p)
  target=path['kind']=='target'
  if target and len(pts)>35 and math.dist(pts[0],pts[-1])<1.5:
   x0=min(p[0] for p in pts);x1=max(p[0] for p in pts);y0=min(p[1] for p in pts);y1=max(p[1] for p in pts)
   if x1-x0>2 and y1-y0>2:
    c.save();c.translate((x0+x1)/2,(y0+y1)/2);c.scale((x1-x0)/2,(y1-y0)/2)
    for k in (0,2):
     c.new_path();c.move_to(0,0);c.arc(0,0,.87,k*math.pi/2,(k+1)*math.pi/2);c.close_path();s._ink(.72,GOLD);c.fill()
    c.restore();c.new_path();c.move_to(*pts[0])
    for p in pts[1:]:c.line_to(*p)
  hardware=path['name'].startswith('B4 ')
  s._stroke(.88 if hardware else (.75 if path['kind']=='outline' else .49),path['width']*stroke_scale,None,GOLD if target else (ARC if hardware else WHITE))
 c.restore()
