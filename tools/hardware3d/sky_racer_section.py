"""Longitudinal service cutaway of SR-1; outboard drives omitted explicitly."""
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import family_core as g
from sky_racer import build
from mathutils import Matrix,Vector
import bmesh

def build_section():
 g.reset();build()
 keep=('monocoque','canopy','glazing','shell longitudinal','canted tail','rudder','landing')
 g.parts[:]=[(o,r) for o,r in g.parts if o.name.startswith(keep)]
 g.wires[:]=[(n,p,r) for n,p,r in g.wires if n.startswith(keep)]
 # The longitudinal plane removes the near half of the hull and glazing.
 g.bpy.context.view_layer.update();deps=g.bpy.context.evaluated_depsgraph_get()
 for index,(o,role) in enumerate(g.parts):
  mesh=g.bpy.data.meshes.new_from_object(o.evaluated_get(deps))
  bm=bmesh.new();bm.from_mesh(mesh);bm.transform(o.matrix_world)
  bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),plane_co=(0,0,0),plane_no=(1,0,0),clear_outer=True,dist=.0001)
  bm.to_mesh(mesh);bm.free()
  if o.type!='MESH':
   name=o.name;g.bpy.data.objects.remove(o,do_unlink=True);o=g.bpy.data.objects.new(name,mesh);g.bpy.context.collection.objects.link(o);g.parts[index]=(o,role)
  else:o.modifiers.clear();o.data=mesh
  o.matrix_world=Matrix.Identity(4)
 # Discard decorative wire paths on the removed half.
 g.wires[:]=[(n,p,r) for n,p,r in g.wires if all(v.x<=.01 for v in p)]
 # A continuous cabin floor and longitudinal load members.
 g.softbox('cabin floor',(-4,-49,49),(37,177,6),2,'structure')
 for x in (-15,3):
  g.beam('floor longeron',(x,-157,44),(x,117,55),2.5,'detail')
 # Structural bulkheads are genuine elliptical frames behind the cut plane.
 for y,w,lo,hi in [(-181,29,45,86),(-141,39,38,95),(39,40,39,96),(104,28,46,87),(163,20,55,82)]:
  pts=[(-w*abs(math.cos(math.pi*k/40)),y,(hi+lo)/2+(hi-lo)/2*math.sin(-math.pi/2+math.pi*k/40)) for k in range(41)]
  # Back-wall reinforcement follows the upper and lower body envelope.
  pts=[(-w*math.sin(math.pi*k/40),y,(hi+lo)/2-(hi-lo)/2*math.cos(math.pi*k/40)) for k in range(41)]
  g.wire('bulkhead frame',pts,1.4,'structure')
 # Reclined crash seat; front is negative Y, seat back rises towards the tail.
 g.softbox('seat cushion',(-2,-51,65),(35,43,10),4,'structure')
 o=g.softbox('seat back',(-2,-12,95),(36,10,60),4,'structure');o.matrix_world=Matrix.Translation((-2,-12,95))@Matrix.Rotation(math.radians(-22),4,'X')@Matrix.Translation((2,12,-95))
 g.softbox('head restraint',(-2,-1,127),(27,12,14),4,'detail')
 for yy in (-62,-41):g.beam('seat crush mount',(-2,yy,51),(-2,yy,60),3,'detail')
 # A visible harness loop and buckle, in the open half of the cockpit.
 for x in (-10,9):
  g.wire('shoulder harness',[(x,-3,121),(x,-21,104),(x,-30,83),(x,-49,73)],1,'cable')
 g.softbox('harness buckle',(9,-48,73),(4,8,6),1,'accent')
 # Pedals, stick, and sloped instrument panel.
 for x in (-10,9):
  g.beam('pedal support',(x,-133,51),(x,-142,68),2,'detail')
  o=g.softbox('pedal',(x,-143,69),(12,5,16),2,'detail');o.matrix_world=Matrix.Translation((x,-143,69))@Matrix.Rotation(.3,4,'X')@Matrix.Translation((-x,143,-69))
 g.beam('control stick',(11,-77,59),(11,-86,83),1.8,'detail')
 g.ball('stick grip',(11,-86,85),(3,3,6),'structure')
 o=g.softbox('instrument console',(-2,-113,97),(39,9,27),4,'structure');o.matrix_world=Matrix.Translation((-2,-113,97))@Matrix.Rotation(-.4,4,'X')@Matrix.Translation((2,113,-97))
 g.softbox('display face',(18,-114,99),(2,7,19),1,'accent')
 # Accessible aft cell bay, visibly separate from avionics in the nose.
 g.softbox('cell bay floor',(-3,78,55),(31,82,4),2,'structure')
 for y in (48,62,76,90,104):
  g.softbox('cell module',(-3,y,67),(28,11,19),2,'detail')
  g.softbox('cell bus tab',(12,y,77),(2,7,3),.8,'accent')
 g.wire('power bus',[(13,47,79),(13,108,79),(13,124,67)],1,'cable')
 g.softbox('flight computer',(-3,-185,67),(25,30,16),3,'detail')
 for yy in (-196,-189,-182,-175):g.wire('avionics fin',[(10,yy,61),(10,yy,73)],.6,'detail')
 g.wire('floor cable duct',[(8,-193,53),(8,-151,43),(8,-54,39),(8,27,43),(8,113,51)],1.3,'cable')
 g.anchors.clear()
 for label,p in [('FLIGHT COMPUTER',(12,-185,67)),('CRASH CELL',(16,-34,78)),('CELL BAY',(13,78,73))]:g.mark(label,p)
 return (87,7)

if __name__=='__main__':
 import sys,os
 az,el=build_section();g.export('sky-racer-cutaway',az,el)
 sys.stdout.flush();os._exit(0)
