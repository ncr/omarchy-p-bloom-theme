"""SR-1: a compact six-duct race aircraft, authored around its pilot capsule."""
import math
import family_core as g
from mathutils import Matrix
T=math.tau

def loft(name,stations,role='structure'):
 # Smooth longitudinal sections: y, half-width, belly z, crown z.
 samples=[]
 for i in range(len(stations)-1):
  a=stations[max(0,i-1)];b=stations[i];c=stations[i+1];d=stations[min(len(stations)-1,i+2)]
  for j in range(10):
   t=j/10
   samples.append(tuple(.5*((2*b[k])+(-a[k]+c[k])*t+(2*a[k]-5*b[k]+4*c[k]-d[k])*t*t+(-a[k]+3*b[k]-3*c[k]+d[k])*t*t*t) for k in range(4)))
 samples.append(stations[-1]);n=64;vs=[];fs=[]
 for y,w,lo,hi in samples:
  for k in range(n):
   a=T*k/n;vs.append((max(.3,w)*math.cos(a),y,(hi+lo)/2+(hi-lo)/2*math.sin(a)))
 for j in range(len(samples)-1):
  for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 fs.extend([tuple(reversed(range(n))),tuple((len(samples)-1)*n+k for k in range(n))])
 g.mesh(name,vs,fs,role)
 return samples

def build():
 hull=loft('monocoque safety capsule',[(-234,1,70,75),(-215,18,55,81),(-166,36,40,91),(-86,45,35,104),(12,42,38,99),(101,29,46,87),(190,17,61,79),(220,1,69,73)])
 # Canopy is a separate framed shell with a clear raised profile.
 glass=loft('canopy glazing',[(-151,1,91,93),(-131,24,92,116),(-73,33,98,151),(-15,29,98,155),(23,14,93,122),(31,1,96,99)],'shell')
 for sign in (-1,1):
  for angle,label in [(0,'canopy sill'),(.58,'glazing shoulder')]:
   pts=[]
   for y,w,lo,hi in glass:
    a=angle if sign>0 else math.pi-angle
    pts.append((w*math.cos(a),y,(hi+lo)/2+(hi-lo)/2*math.sin(a)+.5))
   g.wire(label,pts,.75 if angle==0 else .48,'structure' if angle==0 else 'detail')
 # Arch at the rear of the pilot's head, attached to both canopy sills.
 idx=min(range(len(glass)),key=lambda j:abs(glass[j][0]+9))
 y,w,lo,hi=glass[idx]
 g.wire('canopy rear arch',[(w*math.cos(T*k/100),y,(hi+lo)/2+(hi-lo)/2*math.sin(T*k/100)+.6) for k in range(51)],.85,'structure')
 # Long access seams follow the body, rather than being floating ornament.
 for side in (-1,1):
  for angle in (.18,-.44):
   pts=[(side*w*math.cos(angle),y,(hi+lo)/2+(hi-lo)/2*math.sin(angle)+.6) for y,w,lo,hi in hull[5:-5]]
   g.wire('shell longitudinal seam',pts,.45,'detail')
 # Paired replaceable energy cassettes form the underbody shoulders.
 for side in (-1,1):
  start=len(g.parts)
  loft('energy cassette',[(-48,1,38,48),(-25,12,29,58),(68,13,31,63),(127,6,43,66),(138,1,53,59)],'structure')
  for o,r in g.parts[start:]:o.location.x=side*38
  for y in (3,30,57,84):
   g.softbox('cassette latch',(side*49,y,47),(3,11,9),1.4,'detail')
 # Six differently sized ring motors on swept, faired folding wings.
 for row,(cy,cx,r,z) in enumerate([(-142,105,47,66),(7,154,54,62),(153,112,47,75)]):
  for side in (-1,1):
   x=side*cx
   # A tapered wing prism connects the chassis to each duct, with a true hinge.
   rooty=cy+(-25 if row==0 else 28);rootx=side*(31 if row!=1 else 42)
   vs=[(rootx,rooty-25,63),(rootx,rooty+28,63),(x-side*(r-1),cy+20,z),(x-side*(r-1),cy-19,z)]
   vs+= [(xx,yy,zz-10) for xx,yy,zz in vs]
   g.mesh('swept folding wing',vs,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)])
   g.beam('fold bearing',(side*(abs(rootx)+14),rooty-19,61),(side*(abs(rootx)+14),rooty+19,61),4,'detail')
   # Duct has a flared inlet, lip, motor band and narrower exit.
   for ri,ro,za,zb,role in [(r-5,r,z-8,z+8,'structure'),(r-4,r+2,z+8,z+12,'structure'),(r-6,r-3,z-13,z-8,'detail')]:
    o=g.annulus('rim motor duct',ri,ro,za,zb,role=role,cz=0)
    o.matrix_world=Matrix.Translation((x,cy,0))@Matrix.Rotation(math.pi/2,4,'X')
    # annulus local axial coordinate rotates to +z.
   for k in range(11):
    a=T*k/11;verts=[]
    for rad,da,zz in [(7,0,z+1),(r*.6,.10,z+3),(r-6,.28,z+1),(r-6,.40,z-1),(r*.6,.27,z-2),(7,.18,z)]:
     verts.append((x+rad*math.cos(a+da),cy+rad*math.sin(a+da),zz))
    g.mesh('swept fan blade',verts,[tuple(range(6))],'detail')
   g.cyl('rotor centre fairing',x,cy,z-5,7,10,'structure',24)
   for k in range(8):
    a=T*k/8
    g.cyl('ring fastener',x+(r-1)*math.cos(a),cy+(r-1)*math.sin(a),z+12,1.2,1.5,'detail',8)
   # External rim controller, cooling slots, all mirrored as one family.
   g.softbox('rim controller',(x,cy+r+2,z+1),(22,11,13),4,'detail')
   for off in (-6,0,6):g.wire('controller cooling slot',[(x+off,cy+r+8,z-2),(x+off,cy+r+8,z+5)],.4,'detail')
 # Twin canted stabilisers, swept and tapered rather than a generic box tail.
 for side in (-1,1):
  v=[(side*17,131,76),(side*18,202,74),(side*36,190,130),(side*32,170,135)]
  v+= [(xx+side*3,yy,zz) for xx,yy,zz in v]
  g.mesh('canted tail fin',v,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)])
  g.wire('rudder hinge',[(side*22,181,87),(side*33,184,125)],.4,'detail')
 # Short landing runners tuck under the energy pods.
 for side in (-1,1):
  for y in (-90,92):g.beam('landing link',(side*34,y,43),(side*46,y+9,18),3,'detail')
  g.wire('landing runner',[(side*46,-122,25),(side*46,-101,16),(side*46,111,16),(side*46,129,26)],3,'structure')
 # Exactly fourteen sensing windows grouped in recognisable arrays.
 for side in (-1,1):
  for y in (-194,-164,-116,-58,17,93,160):
   sample=min(hull,key=lambda p:abs(p[0]-y));yy,w,lo,hi=sample
   g.ball('sensing aperture',(side*(w+.8),yy,(lo+hi)/2),(2,3.2,2.5),'accent')
 g.mark('RIM-DRIVEN FAN',(-154,7,77));g.mark('CRASH CELL',(0,-72,151))
 g.mark('LITHIUM-AIR PACK',(49,57,47));g.mark('SENSING ARRAY',(23,-194,70))
 g.mark('FOLDING ARM',(66,35,61))
 return (31,34)
