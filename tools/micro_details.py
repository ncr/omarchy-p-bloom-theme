"""Authored microscopic detail studies; local randomness never alters poster data."""
import math,random
from sheet import WHITE,ARC,GOLD
from fidelity import contour
T=math.tau

def ribbon(s,pts,width=3,a=.8,color=WHITE):
 """Visible walls around a sampled centreline, with an opaque interior."""
 left=[];right=[]
 for i,(x,y) in enumerate(pts):
  p=pts[max(0,i-1)];q=pts[min(len(pts)-1,i+1)]
  dx,dy=q[0]-p[0],q[1]-p[1];ll=math.hypot(dx,dy) or 1
  w=width(i/(len(pts)-1)) if callable(width) else width
  left.append((x-dy/ll*w,y+dx/ll*w));right.append((x+dy/ll*w,y-dx/ll*w))
 c=s.c;c.new_path();c.move_to(*left[0])
 for p in left[1:]+right[::-1]:c.line_to(*p)
 c.close_path();s.knockout();s._ink(.015,color);c.fill()
 for edge in (left,right):
  s.poly(edge,a,.65,close=False,color=color)

def bezpts(a,b,c,d,n=40):
 return [((1-t)**3*a[0]+3*(1-t)**2*t*b[0]+3*(1-t)*t*t*c[0]+t**3*d[0],
          (1-t)**3*a[1]+3*(1-t)**2*t*b[1]+3*(1-t)*t*t*c[1]+t**3*d[1]) for t in [i/n for i in range(n+1)]]

def advance_legacy_rng(s,name):
 """Keep unrelated downstream charts byte-for-byte stable."""
 r=s.rng
 if name=='capillaries':
  for _ in range(40):r.uniform(-150,150);r.uniform(-150,150);r.uniform(7,11)
 elif name=='pellet':
  for _ in range(70):r.uniform(-104,104);r.uniform(-104,104);r.uniform(4,13)
  for _ in range(16):
   r.uniform(-80,80);r.uniform(-80,80);r.uniform(0,360)
   for j in range(14):r.uniform(-70,70)
 elif name=='leaf':
  for _ in range(49*22):r.uniform(-24,24);r.uniform(-18,18);r.uniform(0,180)
 elif name=='voxel':
  for _ in range(70):
   x,y=r.uniform(-170,170),r.uniform(-170,170)
   if abs(x)/22+abs(y)/10>=1.4:r.uniform(1.5,3)

def iso(x,y,z=0):
 return (x-y*.56, y*.42-z)
def local(s,x,y):
 s.c.save();s.c.translate(x,y)
def face(s,pts,a=.8,w=.75,color=WHITE):
 contour(s,[('M',*pts[0])]+[('L',*p) for p in pts[1:]],a=a,w=w,fill=.02,close=True,color=color)
def slab(s,cx,cy,z,w,d,h,color=WHITE):
 top=[iso(cx+xx,cy+yy,z+h) for xx,yy in [(-w/2,-d/2),(w/2,-d/2),(w/2,d/2),(-w/2,d/2)]]
 low=[iso(cx+xx,cy+yy,z) for xx,yy in [(-w/2,-d/2),(w/2,-d/2),(w/2,d/2),(-w/2,d/2)]]
 face(s,[top[1],low[1],low[2],top[2]],.62,.6)
 face(s,[top[2],low[2],low[3],top[3]],.72,.65)
 face(s,top,.85,.8,color)
 return top

def yarn(s,x,y):
 from hardware3d.secondary_drawing import view
 view(s,'micro-yarn',x,y,380,230,angle=math.radians(-22))

def pellet(s,x,y):
 rng=random.Random(752)
 # An oblique broken granule with connected porous walls.
 outer=[]
 for j in range(100):
  a=T*j/100;r=111+6*math.sin(a*5)+3*math.sin(a*9)
  outer.append((x+r*math.cos(a),y+r*.85*math.sin(a)))
 s.poly(outer,.9,1,fill=.025)
 for row in range(-3,4):
  for col in range(-3,4):
   px=col*32+(16 if row%2 else 0);py=row*29
   if px*px+(py/0.85)**2>88**2:continue
   rr=10+rng.random()*4;pts=[]
   for j in range(25):
    a=T*j/24;r=rr*(1+.13*math.sin(a*3+col))
    pts.append((x+px+r*math.cos(a),y+py+r*.76*math.sin(a)))
   s.poly(pts,.6,.55)
   s.poly([(xx+2,yy+4) for xx,yy in pts],.34,.4)
 # Tethered folded enzymes sit at pore mouths, with a legible attachment.
 for px,py,rot in [(-68,-40,.1),(-20,-62,1.2),(44,-39,.5),(62,21,2),(-1,7,.8),(-39,47,1.7),(22,63,2.4)]:
  s.ln(x+px,y+py,x+px+8,y+py+9,.65,.55,color=GOLD)
  pts=[]
  for j in range(65):
   a=T*j/64;r=8+2*math.cos(3*a)+1.2*math.sin(5*a)
   pts.append((x+px+8+r*math.cos(a+rot),y+py+12+r*.75*math.sin(a+rot)))
  s.poly(pts,.88,.8,fill=.025,color=ARC)
  s.bez((x+px+2,y+py+11),(x+px+11,y+py+3),(x+px+5,y+py+20),(x+px+16,y+py+14),.58,.45,color=ARC)
 # Visible fractured thickness along the granule's lower rim.
 s.poly([(xx+5,yy+9) for xx,yy in outer[2:49]],.48,.55,close=False)

def leaf(s,x,y):
 rng=random.Random(491)
 # Staggered, gently irregular cell walls; chloroplasts line the periphery
 # around a quiet central vacuole.
 for row in range(-2,3):
  for col in range(-2,3):
   cx=x+col*80+(38 if row%2 else 0);cy=y+row*68
   pts=[]
   for j in range(65):
    a=T*j/64
    rx=39*(1+.065*math.sin(a*3+col));ry=32*(1+.08*math.sin(a*4+row))
    pts.append((cx+rx*math.copysign(abs(math.cos(a))**.55,math.cos(a)),cy+ry*math.copysign(abs(math.sin(a))**.55,math.sin(a))))
   s.poly(pts,.78,.8)
   s.poly([(cx+(px-cx)*.91,cy+(py-cy)*.89) for px,py in pts],.4,.45)
   s.ellipse(cx+2,cy,20,15,a=.36,w=.45)
   for j in range(11):
    a=T*j/11+.08*rng.random();px=cx+29*math.cos(a);py=cy+23*math.sin(a)
    s.c.save();s.c.translate(px,py);s.c.rotate(a+math.pi/2)
    s.ellipse(0,0,5.8,3,a=.85,w=.65,color=ARC)
    for off in (-2,0,2):s.ln(off,-1.6,off,1.6,.55,.4,color=ARC)
    s.c.restore()
   s.ellipse(cx-14,cy+6,5,6,a=.63,w=.6)
   s.dot(cx-14,cy+6,1.1,.7)

def node(s,x,y):
 # Exploded recording node: a porous contact, dielectric window and routing
 # substrate, carried by one bent flexible strip instead of a crossed symbol.
 local(s,x,y+30)
 p=bezpts((-189,85),(-80,86),(-125,35),(-41,24));ribbon(s,p,13,.8)
 for off in (-7,-2,3,8):s.poly([(xx,yy+off) for xx,yy in p],.62,.5,close=False,color=GOLD)
 slab(s,0,0,-24,108,87,10)
 slab(s,0,0,15,94,76,5)
 # A window and precise routed traces on the middle layer.
 face(s,[iso(xx,yy,21) for xx,yy in [(-25,-19),(25,-19),(25,19),(-25,19)]],.65,.55,ARC)
 for sign in (-1,1):
  for k in range(6):
   pts=[iso(sign*51,-32+k*12,-13),iso(sign*34,-32+k*12,-13),iso(sign*28,-16+k*6,-13)]
   s.poly(pts,.7,.55,close=False,color=GOLD)
 # Raised recording contact with explicit porous surface.
 slab(s,0,0,63,64,54,8,ARC)
 for row in range(5):
  for col in range(6):
   xx=-25+col*10+(3 if row%2 else 0);yy=-20+row*10;px,py=iso(xx,yy,72)
   s.ellipse(px,py,1.8,.85,a=.67,w=.4)
 # Registration posts connect the exploded layers.
 for xx,yy in [(-43,-31),(43,-31),(-43,31),(43,31)]:
  a=iso(xx,yy,-25);b=iso(xx,yy,55)
  s.ln(*a,*b,.4,.5,dash=[3,3])
  s.ellipse(*iso(xx,yy,20),2,1,a=.72,w=.5)
 # One neighbouring axon drapes past the contact rather than a fourfold icon.
 ps=bezpts((162,-85),(89,-143),(111,-49),(27,-46))
 ribbon(s,ps,5,.62,WHITE)
 for j in (7,15,23,31):
  px,py=ps[j];s.ellipse(px,py,7,3,rot=35,a=.4,w=.5)
 s.c.restore()

def voxel(s,x,y):
 # Spatial optical setup: emitter ports, converging beam surfaces and a
 # suspended particle volume shown obliquely, without a central diamond.
 local(s,x,y+8)
 # Quiet back edges of the sampling volume.
 for z in (-41,41):
  ps=[iso(xx,yy,z) for xx,yy in [(-58,-50),(58,-50),(58,50),(-58,50),(-58,-50)]]
  s.poly(ps,.35,.5,close=False,dash=[3,4])
 for xx,yy in [(-58,-50),(58,-50),(-58,50),(58,50)]:
  s.ln(*iso(xx,yy,-41),*iso(xx,yy,41),.35,.5,dash=[3,4])
 # Two offset optical heads with lens stacks, beams meet inside the volume.
 for px,py,ang in [(-122,52,-.39),(74,-118,1.88)]:
  s.c.save();s.c.translate(px,py);s.c.rotate(ang)
  face(s,[(-27,-15),(-4,-15),(6,-9),(6,9),(-4,15),(-27,15)],.8,.8)
  for xx in (-5,1,7):s.ellipse(xx,0,3,11,a=.7,w=.65,color=ARC)
  for yy in (-6,0,6):s.ln(-24,yy,-14,yy,.45,.5)
  s.c.restore()
  vx,vy=-px,-py;ll=math.hypot(vx,vy);nx,ny=-vy/ll,vx/ll
  for sign in (-1,1):
   ps=bezpts((px+sign*nx*10,py+sign*ny*10),(px*.63+sign*nx*8,py*.63+sign*ny*8),(-sign*nx*5,-sign*ny*5),(-px*.65-sign*nx*20,-py*.65-sign*ny*20))
   s.poly(ps,.53,.6,close=False,color=ARC)
 # Depth-coded aerosol samples; only a compact irregular cluster glows.
 rng=random.Random(12081)
 for j in range(85):
  xx=rng.uniform(-52,52);yy=rng.uniform(-45,45);zz=rng.uniform(-36,36)
  px,py=iso(xx,yy,zz);s.dot(px,py,.7,.28)
 for xx,yy,zz in [(-9,-4,2),(-4,3,6),(1,1,0),(7,-2,-3),(3,7,3),(8,5,8),(-3,-7,-6)]:
  px,py=iso(xx,yy,zz);s.circ(px,py,2.6,.64,.55,color=ARC);s.dot(px,py,.9,.86,ARC)
 # Sampling-plane registration marks rather than decorative glow.
 for px,py in [iso(-58,50,-41),iso(58,50,-41)]:
  s.ln(px-5,py+6,px+5,py+6,.55,.55)
 s.c.restore()

def capillaries(s,x,y):
 # Organic planar vascular network: inset Voronoi tissue islands leave
 # connected channels, so junctions stay open instead of crossing like wires.
 rng=random.Random(1121);seeds=[]
 for _ in range(800):
  p=(rng.uniform(-190,190),rng.uniform(-190,190))
  if all(math.hypot(p[0]-q[0],p[1]-q[1])>43 for q in seeds):seeds.append(p)
  if len(seeds)==43:break
 for i,(px,py) in enumerate(seeds):
  poly=[(-210,-210),(210,-210),(210,210),(-210,210)]
  for j,(qx,qy) in enumerate(seeds):
   if i==j:continue
   nx,ny=qx-px,qy-py;limit=(qx*qx+qy*qy-px*px-py*py)/2;out=[]
   for u,v in zip(poly,poly[1:]+poly[:1]):
    du=u[0]*nx+u[1]*ny-limit;dv=v[0]*nx+v[1]*ny-limit
    if du<=0:out.append(u)
    if (du<=0)!=(dv<=0):
     t=du/(du-dv);out.append((u[0]+t*(v[0]-u[0]),u[1]+t*(v[1]-u[1])))
   poly=out
   if not poly:break
  if len(poly)<3:continue
  cx=sum(p[0] for p in poly)/len(poly);cy=sum(p[1] for p in poly)/len(poly)
  poly=[(x+cx+(u-cx)*.90,y+cy+(v-cy)*.90) for u,v in poly]
  c=s.c;c.new_path()
  for j,p in enumerate(poly):
   prev=poly[j-1];nxt=poly[(j+1)%len(poly)]
   aa=(p[0]*.76+prev[0]*.24,p[1]*.76+prev[1]*.24)
   bb=(p[0]*.76+nxt[0]*.24,p[1]*.76+nxt[1]*.24)
   if j==0:c.move_to(*aa)
   else:c.line_to(*aa)
   c.curve_to(p[0],p[1],p[0],p[1],bb[0],bb[1])
  c.close_path();s._stroke(.77,.72,None,ARC if cx<-35 else WHITE)
  if i%3==0:s.ellipse(x+cx,y+cy,5.5,3.7,rot=i*23,a=.25,w=.45)
