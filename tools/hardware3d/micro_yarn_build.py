"""Five solid twisted filaments wound into a larger actuator coil."""
import sys,os,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import family_core as g
from mathutils import Vector
g.reset();T=math.tau
for strand in range(5):
 centres=[];n=780;m=10
 for j in range(n+1):
  t=-3.2*T+j/n*6.4*T;p=Vector((10.8*t,46*math.cos(t),46*math.sin(t)))
  normal=Vector((0,math.cos(t),math.sin(t)));tangent=Vector((10.8,-46*math.sin(t),46*math.cos(t))).normalized()
  binormal=tangent.cross(normal);phase=4*t+strand*T/5
  centres.append(p+normal*(6*math.cos(phase))+binormal*(6*math.sin(phase)))
 verts=[]
 for j,p in enumerate(centres):
  tangent=(centres[min(n,j+1)]-centres[max(0,j-1)]).normalized()
  u=tangent.cross(Vector((0,0,1))).normalized();v=tangent.cross(u).normalized()
  for k in range(m):verts.append(tuple(p+2.4*(u*math.cos(T*k/m)+v*math.sin(T*k/m))))
 faces=[]
 for j in range(n):
  for k in range(m):faces.append((j*m+k,j*m+(k+1)%m,(j+1)*m+(k+1)%m,(j+1)*m+k))
 faces.extend([tuple(reversed(range(m))),tuple(n*m+k for k in range(m))])
 g.mesh('twisted filament',verts,faces,'accent' if strand==0 else 'structure')
g.export('micro-yarn',0,23)
sys.stdout.flush();os._exit(0)
