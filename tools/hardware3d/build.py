"""Authored cryostat illustration: actual 3-D parts, hidden-line vector export."""
import bpy, math, json, os, sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'tools/assets/hardware3d';STUDY=ROOT/'concepts/hardware-study'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
parts=[];wires=[];anchors={};tau=math.tau

def mesh(name,v,f,role='structure'):
 m=bpy.data.meshes.new(name);m.from_pydata(v,[],f);m.update();o=bpy.data.objects.new(name,m);bpy.context.collection.objects.link(o);parts.append((o,role));return o

def box(name,center,size,role='detail'):
 x,y,z=center;a,b,c=[v/2 for v in size]
 v=[(x+i*a,y+j*b,z+k*c) for k in (-1,1) for j in (-1,1) for i in (-1,1)]
 return mesh(name,v,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],role)

def cyl(name,x,y,z,r,h,role='structure',n=48):
 v=[(x+r*math.cos(tau*i/n),y+r*math.sin(tau*i/n),z+zz) for zz in (0,h) for i in range(n)]
 f=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,v,f,role)

def shell(name,r,z0,z1,a0,a1,role='shell'):
 n=64;angles=[math.radians(a0+(a1-a0)*i/n) for i in range(n+1)];v=[(rr*math.cos(a),rr*math.sin(a),z) for z in (z0,z1) for rr in (r-4,r) for a in angles];m=n+1
 f=[]
 for i in range(n):
  f.extend([(i,i+1,2*m+i+1,2*m+i),(m+i,3*m+i,3*m+i+1,m+i+1),(i,m+i,m+i+1,i+1),(2*m+i,2*m+i+1,3*m+i+1,3*m+i)])
 f.extend([(0,2*m,3*m,m),(n,m+n,3*m+n,2*m+n)])
 return mesh(name,v,f,role)

def wire(name,pts,r=1.2,role='cable'):
 # Tubes occlude one another physically; export their centreline at controlled weight.
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=1;c.resolution_u=1
 sp=c.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,co in zip(sp.points,pts):p.co=(*co,1)
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);parts.append((o,'tube'));wires.append((o.name,[Vector(p) for p in pts],role))

levels=[(690,202,'300 K'),(596,180,'50 K'),(496,158,'4 K'),(400,137,'800 mK'),(310,118,'100 mK'),(220,104,'8 mK')]
# Rear cutaway sectors expose a physically nested assembly.
shell('vacuum jacket',223,26,702,32,166)
shell('radiation shield 50K',190,50,586,37,159)
shell('radiation shield 4K',166,76,486,43,153)
for i,(z,r,label) in enumerate(levels):
 cyl('cold plate '+label,0,0,z,r,9,'plate',96)
 for a in range(0,360,30):
  x,y=(r-12)*math.cos(math.radians(a)),(r-12)*math.sin(math.radians(a))
  cyl('plate fastener',x,y,z+9,3.4,3,'detail',6)
  cyl('washer',x,y,z+9,5,.8,'detail',24)
 if i<len(levels)-1:
  low=levels[i+1][0]+9;rr=levels[i+1][1]-18
  for a in (20,140,260):
   x,y=rr*math.cos(math.radians(a)),rr*math.sin(math.radians(a))
   cyl('suspension rod',x,y,low,3.5,z-low)
   for zz in (low,low+9,z-12):cyl('rod collar',x,y,zz,6,5,'detail',12)
# Vacuum closure and floor pedestal.
cyl('lower flange',0,0,20,224,12,'plate',96)
for x,y in [(-170,100),(170,100),(0,-186)]:
 cyl('support foot',x,y,-20,16,40);cyl('foot pad',x,y,-25,25,5)
# Feedthrough blocks with coax sockets.
for x in (-110,-45,25):
 box('feedthrough',(x,-30,725),(48,42,40),'structure')
 for j in range(4):cyl('feedthrough socket',x-16+j*10,-30,745,3,10,'detail',12)
# Pulse tube head and stepped cold finger.
cyl('pulse tube motor',108,64,710,39,62)
for z in range(716,770,7):cyl('cooling fin',108,64,z,44,2,'detail',64)
for x in (97,120):cyl('cold finger',x,64,507,8,203)
anchors['PULSE-TUBE COOLER']=(108,64,758)
# Coax looms drape and anchor to each stage, with intentional routing corridors.
for bundle in range(3):
 for j in range(5):
  x=-120+bundle*55+j*4.5;y=-64-bundle*9
  pts=[]
  for stage in range(5):
   hi=levels[stage][0];lo=levels[stage+1][0]+11
   for k in range(25):
    t=k/24;factor=1-.055*(stage+t);pts.append(((x+12*math.sin(t*math.pi))*factor,(y-12*math.sin(t*math.pi))*factor,hi+(lo-hi)*t))
   box('thermal anchor',(x*(1-.055*(stage+1)),y*(1-.055*(stage+1)),lo),(5,10,5),'detail')
  wire('coax loom',pts,.9)
anchors['CONTROL LINES']=(-95,-78,550)
# Controller module on the 4 K stage.
box('control carrier',(65,-58,510),(63,52,5),'accent')
for x in (45,64,83):
 box('controller package',(x,-58,516),(13,19,8),'accent')
 for k in range(5):box('controller pin',(x-7,-65+k*3,513),(3,1,1),'detail')
anchors['CONTROL CHIPS']=(65,-58,520)
# Braided service loops and coil exchanger to the right.
for j in range(3):
 pts=[(91+16*math.cos(tau*k/20),-36+16*math.sin(tau*k/20),340+k*.7+j*4) for k in range(150)]
 wire('heat exchanger coil',pts,1.7,'detail')
anchors['HEAT EXCHANGER']=(108,-36,374)
cyl('mixing chamber',72,-18,168,23,45,'structure');cyl('mixing flange',72,-18,208,29,7,'detail')
for k in range(8):
 a=tau*k/8;cyl('mixing bolt',72+25*math.cos(a),-18+25*math.sin(a),215,2,3,'detail',6)
anchors['MIXING CHAMBER']=(90,-18,187)
for j in range(4):
 pts=[(42+j*4,-103,665-440*k/50) for k in range(51)]+[(42+j*4-50*k/20,-103+26*k/20,225-33*k/20) for k in range(1,21)]
 wire('optical fibre',pts,.9,'accent')
anchors['OPTICAL LINK']=(47,-103,435)
# KiCad layout drives the actual six-board module inside an open magnetic cage.
carrier=json.loads((OUT/'carrier.json').read_text())
for idx in range(6):
 z=55+idx*23
 box('carrier PCB',(0,-25,z),(96,68,2),'accent')
 for p in carrier['parts']:box(p['kind'],(p['x'],p['y']-25,z+1+p['height']/2),(p['w'],p['h'],p['height']),'detail')
 for x,y,w,h in carrier['pads']:box('solder pad',(x,y-25,z+1.2),(w,h,.4),'detail')
 for line in carrier['tracks']:wire('copper trace',[(x,y-25,z+1.5) for x,y in line],.18,'fine')
for x in (-55,55):
 for y in (-64,16):cyl('module standoff',x,y,42,3,157,'detail',12)
box('shield back',(0,23,121),(122,3,171),'structure')
box('shield side',(-62,-24,121),(3,96,171),'structure')
box('shield lid',(0,-24,208),(130,104,6),'structure')
anchors['PROCESSOR STACK']=(4,-61,120);anchors['MAGNETIC SHIELD']=(-62,-24,121)

# Extract sharp and silhouette edges from evaluated geometry, with ray-tested occlusion.
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();vertices=[];faces=[];owners=[];meshes=[]
for o,role in parts:
 eo=o.evaluated_get(deps);m=eo.to_mesh();v=[o.matrix_world@p.co for p in m.vertices];f=[list(p.vertices) for p in m.polygons];off=len(vertices)
 vertices.extend(v);faces.extend([tuple(off+i for i in face) for face in f]);owners.extend([o.name]*len(f));meshes.append((o.name,role,v,f));eo.to_mesh_clear()
bvh=BVHTree.FromPolygons(vertices,faces,all_triangles=False)
az=math.radians(24);el=math.radians(13);right=Vector((math.cos(az),math.sin(az),0));toward=Vector((math.sin(az)*math.cos(el),-math.cos(az)*math.cos(el),math.sin(el)));up=toward.cross(right)
def export(view):
 global right,toward,up
 if view=='plate':right=Vector((1,0,0));toward=Vector((0,0,1));up=Vector((0,1,0))
 def xy(p):return [round(p.dot(right),4),round(-p.dot(up),4)]
 paths=[]
 def visible(p,owner):
  hit=bvh.ray_cast(p+toward*2000,-toward,2002)
  return hit[0] is None or owners[hit[2]]==owner or (hit[0]-p).length<.4
 def line(name,pts,role):
  chain=[]
  def flush():
   if len(chain)>1:paths.append(dict(name=name,points=chain.copy(),role=role))
  for a,b in zip(pts,pts[1:]):
   n=max(1,math.ceil((a-b).length/1.2))
   for k in range(n):
    p=a.lerp(b,k/n)
    if visible(p,name):chain.append(xy(p))
    else:flush();chain=[]
  if visible(pts[-1],name):chain.append(xy(pts[-1]))
  flush()
 for name,role,v,f in meshes:
  if role=='tube':continue
  if view=='plate':continue
  edges={}
  for poly in f:
   normal=(v[poly[1]]-v[poly[0]]).cross(v[poly[2]]-v[poly[0]]).normalized()
   for a,b in zip(poly,poly[1:]+poly[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append(normal)
  for (a,b),norms in edges.items():
   front=[n.dot(toward)>1e-6 for n in norms]
   silhouette=len(norms)==1 or any(front)!=all(front)
   sharp=len(norms)>1 and norms[0].dot(norms[1])<.75
   if silhouette or (sharp and any(front)):line(name,[v[a],v[b]],role)
 if view=='main':
  for name,pts,role in wires:line(name,pts,role)
 data=dict(paths=paths,anchors={name:xy(Vector(p)) for name,p in anchors.items()},levels=[dict(z=z,r=r,label=label,anchor=xy(Vector((-r,0,z)))) for z,r,label in levels])
 (OUT/(view+'.json')).write_text(json.dumps(data,separators=(',',':'))+'\n')
 print(view,len(paths),'visible paths',flush=True)
export('main')
bpy.ops.object.camera_add(location=toward*1800+Vector((0,0,360)));cam=bpy.context.object;cam.rotation_euler=(-toward).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1050;bpy.context.scene.camera=cam
bpy.ops.wm.save_as_mainfile(filepath=str(STUDY/'quantum-assembly.blend'))
sys.stdout.flush();os._exit(0)
