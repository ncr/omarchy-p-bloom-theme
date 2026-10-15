"""Shared authored geometry and orthographic hidden-line export for the hardware family."""
import bpy, math, json, sys, os
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
import hidden_line
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'tools/assets/hardware-family';STUDY=ROOT/'concepts/retro-family'
parts=[];wires=[];anchors={};tau=math.tau;C=350
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


def reset():
 global parts,wires,anchors
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 parts=[];wires=[];anchors={}

def mark(label,p):anchors[label]=p

def beam(name,a,b,r,role='structure',sides=12):
 a,b=Vector(a),Vector(b);o=cyl(name,0,0,0,r,(b-a).length,role,sides)
 o.matrix_world=Matrix.Translation(a)@(b-a).to_track_quat('Z','Y').to_matrix().to_4x4();return o

def ball(name,p,scale,role='structure'):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,location=p)
 o=bpy.context.object;o.name=name;o.scale=scale;parts.append((o,role));return o

def base(rx=170,ry=110):
 casting('cast pedestal',[(0,rx*.88,ry*.88),(4,rx*.97,ry*.97),(12,rx,ry),(20,rx*.98,ry*.98),(29,rx*.90,ry*.90),(33,rx*.85,ry*.85)])
 trim('skirt bead',10,rx+1,ry+1)
 for x in (-rx*.7,rx*.7):
  for y in (-ry*.7,ry*.7):cyl('isolation foot',x,y,-8,10,9,'detail',24)

def flange(x,y,z,r):
 cyl('bolted flange',x,y,z,r,5,'structure',64)
 for k in range(12):
  a=tau*k/12;cyl('flange bolt',x+(r-6)*math.cos(a),y+(r-6)*math.sin(a),z+5,2,3,'detail',6)

def vents(x,y,z,n=9,w=40):
 for k in range(n):softbox('vent', (x,y,z+k*5),(w,2,1.5),.6,'detail')

def dial(x,y,z,r=10):
 along_y('dial bezel',x,y,z,r,3,'detail',40);along_y('dial face',x,y-3,z,r-2,1,'detail',40)
 wire('dial needle',[(x-3,y-4.3,z-4),(x+3,y-4.3,z+5)],.35,'accent')

def export(name,az=27,el=20):
 a,e=math.radians(az),math.radians(el);right=Vector((math.cos(a),math.sin(a),0));toward=Vector((math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)));up=toward.cross(right)
 def xy(p):return [round(p.dot(right),4),round(-p.dot(up),4)]
 # Exact visibility and continuous smooth contours: hidden_line.py.
 paths=hidden_line.extract(hidden_line.collect(parts),wires,right,up,toward)
 data=dict(paths=paths,anchors={label:xy(Vector(p)) for label,p in anchors.items()})
 (OUT/(name+'.json')).write_text(json.dumps(data,separators=(',',':'))+'\n')
 bpy.ops.object.camera_add(location=toward*1600+Vector((0,0,250)));cam=bpy.context.object;cam.rotation_euler=(-toward).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=900;bpy.context.scene.camera=cam
 bpy.ops.wm.save_as_mainfile(filepath=str(STUDY/(name+'.blend')))
 print(name,len(parts),'parts',len(paths),'paths',flush=True)
