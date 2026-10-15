"""Secondary projections share the primary assemblies, including genuine cut geometry."""
import sys,os,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import family_build as f
import family_core as g
import bmesh
from mathutils import Vector,Matrix

def section_y(preserve=()):
 # Evaluate bevels and cut away the near half of every solid at the same plane.
 g.bpy.context.view_layer.update();deps=g.bpy.context.evaluated_depsgraph_get()
 for index,(obj,role) in enumerate(g.parts):
  if obj.name.startswith(preserve):continue
  eo=obj.evaluated_get(deps);mesh=g.bpy.data.meshes.new_from_object(eo)
  bm=bmesh.new();bm.from_mesh(mesh);bm.transform(obj.matrix_world)
  bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),
    plane_co=(0,0,0),plane_no=(0,1,0),clear_inner=True,dist=.0001)
  bm.to_mesh(mesh);bm.free()
  if obj.type!='MESH':
   name=obj.name;g.bpy.data.objects.remove(obj,do_unlink=True)
   obj=g.bpy.data.objects.new(name,mesh);g.bpy.context.collection.objects.link(obj);g.parts[index]=(obj,role)
  else:obj.modifiers.clear();obj.data=mesh
  obj.matrix_world=Matrix.Identity(4)
 # Wire centerlines must follow the same section plane.
 clipped=[]
 for owner,pts,role in g.wires:
  if owner.startswith(preserve):
   clipped.append((owner,pts,role));continue
  chain=[]
  for a,b in zip(pts,pts[1:]):
   if a.y>=0:chain.append(a)
   if (a.y>=0)!=(b.y>=0):
    p=a.lerp(b,-a.y/(b.y-a.y));chain.append(p)
    if a.y>=0:
     if len(chain)>1:clipped.append((owner,chain,role))
     chain=[]
  if pts[-1].y>=0:chain.append(pts[-1])
  if len(chain)>1:clipped.append((owner,chain,role))
 g.wires[:]=clipped

g.reset();f.sky_racer();g.export('sky-racer-side',90,0)
from sky_racer_section import build_section
az,el=build_section();g.export('sky-racer-cutaway',az,el)
g.reset();f.fusion_transport()
g.parts[:]=[(o,r) for o,r in g.parts if not o.name.startswith('forward dust shield')]
g.export('fusion-transport-front',-90,0)
g.reset();f.volumetric_stage();g.export('volumetric-stage-plan',0,90)
g.reset();f.aroma_organ()
omit=('front instrument panel','dial bezel','dial face','dial needle')
g.parts[:]=[(o,r) for o,r in g.parts if not o.name.startswith(omit)]
g.wires[:]=[(n,p,r) for n,p,r in g.wires if not n.startswith(omit)]
section_y(('mixing chip','capillary manifold','heated outlet','outlet rim','scrubber','vent','rolled fan duct','fan hub','swept rotor blade','duct rivet'))
g.export('aroma-organ-section',0,18)
g.reset();f.cortical_mesh()
# Only the capsule, lip, acoustic stack and electronics belong in the tissue section.
keep=('titanium implant','capsule lip','acoustic transducer layer','decoder die','die bond')
g.parts[:]=[(o,r) for o,r in g.parts if o.name.startswith(keep)]
g.wires[:]=[]
section_y();g.export('cortical-capsule-section',0,12)
sys.stdout.flush();os._exit(0)
