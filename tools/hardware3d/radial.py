"""Authored cryostat illustration: actual 3-D parts, hidden-line vector export."""
import bpy, math, json, os, sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'tools/assets/radial-quantum';STUDY=ROOT/'concepts/radial-quantum'
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

# Entirely new device arrangement from the poster narrative: a radial cold engine.
from mathutils import Matrix
C=350

def annulus(name,r0,r1,y0,y1,a0=0,a1=360,role='structure',cx=0,cz=C):
 n=max(12,round((a1-a0)/4));angles=[math.radians(a0+(a1-a0)*i/n) for i in range(n+1)];m=n+1
 vs=[(cx+r*math.cos(a),y,cz+r*math.sin(a)) for y in (y0,y1) for r in (r0,r1) for a in angles]
 fs=[]
 for i in range(n):fs.extend([(i,i+1,2*m+i+1,2*m+i),(m+i,3*m+i,3*m+i+1,m+i+1),(i,m+i,m+i+1,i+1),(2*m+i,2*m+i+1,3*m+i+1,3*m+i)])
 if a1-a0<359.9:fs.extend([(0,2*m,3*m,m),(n,m+n,3*m+n,2*m+n)])
 return mesh(name,vs,fs,role)

def along_y(name,x,y,z,r,h,role='detail',n=24):
 o=cyl(name,0,0,0,r,h,role,n);o.matrix_world=Matrix.Translation((x,y,z))@Matrix.Rotation(math.pi/2,4,'X');return o

def radial_box(name,angle,r,y,w,length,thick,role='detail',cx=0,cz=C):
 a=math.radians(angle);o=box(name,(0,0,0),(w,thick,length),role)
 o.matrix_world=Matrix.Translation((cx+r*math.cos(a),y,cz+r*math.sin(a)))@Matrix.Rotation(math.pi/2-a,4,'Y');return o

def link(name,a,b,r=2,role='structure'):
 pts=[a,b];wire(name,pts,r,role)

def casting(name,profile,role='structure',yc=0):
 # Continuous rounded-rectangle sections, lofted into cast industrial housings.
 n=96;vs=[];fs=[]
 for z,rx,ry in profile:
  for k in range(n):
   a=tau*k/n;co=math.cos(a);si=math.sin(a)
   vs.append((rx*math.copysign(abs(co)**.65,co),yc+ry*math.copysign(abs(si)**.65,si),z))
 for j in range(len(profile)-1):
  for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 fs.extend([tuple(reversed(range(n))),tuple((len(profile)-1)*n+k for k in range(n))])
 return mesh(name,vs,fs,role)

def softbox(name,center,size,radius,role='structure'):
 o=box(name,center,size,role);mod=o.modifiers.new('Cast edge radii','BEVEL');mod.width=radius;mod.segments=6
 return o

def trim(name,z,rx,ry,yc=0):
 pts=[]
 for k in range(193):
  a=tau*k/192;co=math.cos(a);si=math.sin(a)
  pts.append((rx*math.copysign(abs(co)**.65,co),yc+ry*math.copysign(abs(si)**.65,si),z))
 wire(name,pts,.55,'detail')

# Streamlined cast pedestal: rolled skirt, recessed waist and a domed shoulder.
casting('streamlined pedestal',[(5,232,208),(8,247,220),(15,263,234),(23,270,240),(31,269,239),(38,261,231),(45,251,220),(53,232,202),(58,220,192)],yc=20)
casting('recessed pedestal foot',[(0,225,199),(4,231,205),(9,231,205)],'detail',yc=20)
trim('lower rolled bead',16,265,236,20);trim('upper skirt seam',36,265,235,20)
for x in (-203,203):
 for y in (-134,184):
  cyl('isolator',x,y,-9,17,14,'structure');cyl('isolator lockring',x,y,-4,21,4,'detail')
# Flush slide assembly lives within the upper casting, with a curved front fascia.
for x in (-105,105):
 softbox('service slide',(x,-18,69),(18,312,20),5)
 box('slide bearing strip',(x,-18,81),(7,290,2),'detail')
 for y in range(-147,121,40):cyl('slide countersink',x,y,82,2.8,1.5,'detail',12)
softbox('drawer fascia',(0,-177,66),(245,25,36),12)
softbox('fascia inset',(0,-191,66),(173,2,18),4,'detail')
# Rounded tubular pull, mounted at both ends.
wire('service handle',[(-62,-194,68),(-62,-205,68),(-55,-212,68),(55,-212,68),(62,-205,68),(62,-194,68)],2.4,'structure')
for x in (-95,95):along_y('fascia latch',x,-192,66,6,3,'detail',32)
# Broad crescent saddles rise from waisted cast necks rather than rectangular posts.
for y in (-55,159):
 casting('saddle pedestal',[(52,88,37),(57,86,36),(72,65,28),(87,52,24),(99,55,26),(112,67,29)],yc=y)
 annulus('cast crescent saddle',233,257,y-18,y+18,202,338,'structure')
 annulus('saddle inset rib',244,248,y-19,y-18,208,332,'detail')
 for a in (215,325):
  t=math.radians(a);along_y('saddle pivot cap',244*math.cos(t),y-21,C+244*math.sin(t),10,4,'detail',40)
# A small analog service panel on the sloping front shoulder.
softbox('instrument console',(-166,-93,65),(77,67,21),10)
for x in (-186,-150):
 cyl('dial bezel',x,-99,76,12,3,'detail',48)
 cyl('dial inner lip',x,-99,79,10,1,'detail',48)
 wire('dial needle',[(x-4,-104,80),(x+4,-94,80)],.45,'accent')
for x in (-184,-166,-148):cyl('service selector',x,-71,76,3.5,5,'detail',16)
# Short vents follow the upper shoulder rather than covering the whole base.
for x in range(126,202,9):
 wire('pedestal vent',[(x,94,59),(x,132,59)],1.0,'detail')
# Cutaway is intentional: the front and upper quadrant expose the internals.
annulus('vacuum shell',229,235,-94,194,100,382,'shell')
annulus('vacuum front flange',218,246,-109,-93,0,360,'structure')
annulus('rolled outer lip',244,249,-112,-105,0,360,'detail')
annulus('recessed inner lip',214,218,-113,-103,0,360,'detail')
annulus('vacuum rear flange',218,245,190,203,0,360,'structure')
annulus('50 K shield',199,203,-80,165,105,375,'shell')
annulus('4 K shield',170,174,-62,140,110,369,'shell')
annulus('100 mK shield',136,139,-47,108,114,361,'shell')
# Rear bulkhead stays a real closed wall, behind the optical distribution hub.
along_y('rear bulkhead',0,210,C,226,6,'shell',96)
for a in range(0,360,15):
 t=math.radians(a)
 along_y('flange washer',234*math.cos(t),-111,C+234*math.sin(t),5.2,1.2,'detail',20)
 along_y('flange screw',234*math.cos(t),-112.2,C+234*math.sin(t),3.2,3.5,'detail',6)
# Six suspended compute cassettes, each 1700 logical qubits (illustrative).
def cassette(prefix,angle,cx=0,cz=C,y=-81,r=78):
 radial_box(prefix+' carrier',angle,r,y,48,87,5,'accent',cx,cz)
 radial_box(prefix+' heat spreader',angle,r,y+5,54,92,4,'structure',cx,cz)
 radial_box(prefix+' processor tile',angle,r+6,y-4,30,38,4,'accent',cx,cz)
 radial_box(prefix+' optical termination',angle,r-31,y-5,32,11,8,'detail',cx,cz)
 a=math.radians(angle);normal=Vector((-math.sin(a),0,math.cos(a)));rad=Vector((math.cos(a),0,math.sin(a)))
 center=Vector((cx,y,cz))+rad*r
 for side in (-1,1):
  for k in range(9):
   p=center+normal*(side*20)+rad*(-31+k*7)+Vector((0,-5,0))
   o=box(prefix+' bond pad',p,(3,2,3),'detail')
   # Bond/tracing run terminating at the package edge, constrained to its board.
   end=center+normal*(side*15)+rad*(-15+k*3.8)+Vector((0,-6,0))
   wire(prefix+' trace',[tuple(p),tuple(p+rad*2),tuple(end)],.35,'fine')
 # Repeated fine resonator paths occupy the active tile face, not the casing.
 for lane in range(5):
  pts=[]
  for k in range(13):
   p=center+normal*(-10+lane*5)+rad*(-8+k*2.2)+Vector((0,-7,0))
   p+=normal*(1 if k%4<2 else -1)*1.1
   pts.append(tuple(p))
  wire(prefix+' resonator',pts,.2,'fine')
 for off in (-37,37):
  for side in (-1,1):
   p=center+rad*off+normal*(side*21)
   along_y(prefix+' mount',p.x,y-5,p.z,2.7,3,'detail',12)
 for side in (-1,1):
  radial_box(prefix+' latch',angle,r+47,y-5,8,7,11,'detail',cx+side*normal.x*18,cz+side*normal.z*18)

for idx in range(6):
 a=idx*60+30;cassette('cassette '+str(idx+1),a)
 # Warm control electronics ring, close to the module but on its own stage.
 radial_box('4 K controller carrier',a,153,-67,42,31,5,'structure')
 radial_box('4 K control ASIC',a,153,-72,24,17,5,'accent')
 for side in (-1,1):radial_box('controller decoupler',a+side*6,153,-73,4,15,3,'detail')
 # Tangential flexures suspend each stage with slender low-contact members.
 for rr in (144,183,211):
  t=math.radians(a+10);u=math.radians(a+16)
  link('thermal flexure',(rr*math.cos(t),-35,C+rr*math.sin(t)),((rr+12)*math.cos(u),22,C+(rr+12)*math.sin(u)),1.7)
 # Fibre passes through the rear hub, curves to its controller and forward to tile.
 for j in range(3):
  pts=[]
  for k in range(31):
   t=k/30;rr=35+(151-35)*t;theta=math.radians(a+j*.9)
   pts.append((rr*math.cos(theta),120-172*t,C+rr*math.sin(theta)))
  wire('controller optical bus',pts,.75,'cable')
  pts=[]
  for k in range(25):
   t=k/24;rr=143-94*t;theta=math.radians(a+j*.9)
   pts.append((rr*math.cos(theta),-78-10*math.sin(t*math.pi),C+rr*math.sin(theta)))
  wire('cold optical link',pts,.55,'accent')
# Central cold manifold with a six-port hexagonal service boss.
along_y('8 mK mixing manifold',0,-18,C,31,42,'structure',6)
along_y('manifold cover',0,-61,C,27,5,'detail',48)
for a in range(0,360,60):
 t=math.radians(a)
 along_y('manifold bolt',22*math.cos(t),-67,C+22*math.sin(t),2.5,3,'detail',6)
# Cryogenic engine sits off-axis with return tubes and a wound heat exchanger.
for x,z in ((124,560),(183,510)):
 cyl('pulse tube tower',x,111,z,25,72,'structure',48)
 cap=casting('domed cooler cap',[(z+69,25,25),(z+73,25,25),(z+80,21,21),(z+84,12,12),(z+85,1,1)],'structure',yc=111)
 cap.location.x=x
 for off in range(5,70,8):cyl('cooler fin',x,111,z+off,30,2,'detail',48)
 wire('cold supply',[(x,111,z),(x,111,z-34),(x-18,87,z-65),(35,37,C+35)],3,'structure')
for j in range(2):
 pts=[(68+18*math.cos(tau*k/24),48+18*math.sin(tau*k/24),C+54+k*.55+j*3) for k in range(150)]
 wire('counterflow exchanger',pts,1.2,'detail')
# Exterior service equipment: optical distribution, vacuum ports and a shielded bay.
softbox('optical bulkhead',(252,120,347),(45,91,138),17)
for z in (303,328,353,378):
 box('fibre coupler',(273,103,z),(12,18,12),'detail')
 wire('external patch lead',[(279,103,z),(301,103,z),(310,130,z-6),(310,178,z-6)],1,'accent')
 box('patch termination',(310,183,z-6),(9,12,7),'detail')
softbox('service electronics bay',(-241,106,285),(55,123,126),18)
for z in range(242,326,8):box('bay ventilation',(-267,106,z),(1,83,2),'detail')
# Rear piping returns beneath the capsule, clear of its removable front drawer.
for x in (-58,58):
 wire('vacuum return',[(x,205,C),(x,238,C),(x,252,140),(x,252,75)],4,'structure')
 for z in (145,220,290):box('pipe bracket',(x,246,z),(18,9,8),'detail')
anchors={'COMPUTE CASSETTES':(80,-89,397),'8 mK MANIFOLD':(0,-68,C),'4 K CONTROLLERS':(132,-74,426),'NESTED THERMAL SHIELDS':(-180,-50,450),'PULSE-TUBE COOLERS':(124,111,618),'OPTICAL INTERCONNECT':(279,103,378),'SERVICE CARRIAGE':(62,-212,68),'VACUUM ENCLOSURE':(-226,70,355)}
# Independent enlarged view of exactly the same cassette geometry.
cassette('REF cassette',90,cx=720,cz=70,y=0,r=0)
# Visible creases, boundaries, smooth contours and wires (hidden_line.py).
sys.path.insert(0,str(Path(__file__).resolve().parent));import hidden_line
meshes=hidden_line.collect(parts)
az=math.radians(29);el=math.radians(16);right=Vector((math.cos(az),math.sin(az),0));toward=Vector((math.sin(az)*math.cos(el),-math.cos(az)*math.cos(el),math.sin(el)));up=toward.cross(right)
def export(view):
 def xy(p):return [round(p.dot(right),4),round(-p.dot(up),4)]
 detail=view=='detail'
 paths=hidden_line.extract(meshes,wires,right,up,toward,
  draw=lambda name,role:role!='tube' and name.startswith('REF')==detail,
  draw_wire=lambda name:name.startswith('REF')==detail)
 data=dict(paths=paths,anchors={name:xy(Vector(p)) for name,p in anchors.items()})
 (OUT/(view+'.json')).write_text(json.dumps(data,separators=(',',':'))+'\n')
 print(view,len(paths),'visible paths',flush=True)
export('main');export('detail')
bpy.ops.object.camera_add(location=toward*1800+Vector((0,0,360)));cam=bpy.context.object;cam.rotation_euler=(-toward).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1050;bpy.context.scene.camera=cam
bpy.ops.wm.save_as_mainfile(filepath=str(STUDY/'radial-quantum.blend'))
sys.stdout.flush();os._exit(0)
