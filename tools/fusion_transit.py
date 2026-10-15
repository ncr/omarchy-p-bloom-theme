"""Earth to Mars: the FT-2 arc (thrust, coast, brake in 75 days) against a chemical transfer ellipse (259 days)."""
import math
from sheet import WHITE,ARC,GOLD,SUN,polar

def draw(s,lx):
 cx,cy=lx-20,305
 s.dot(cx,cy,4.4,.9,SUN);s.circ(cx,cy,10,.5,.65,color=SUN)
 for r in (96,146):
  s.circ(cx,cy,r,.48,.65)
  for a in range(0,360,10):
   p=polar(cx,cy,r-2,a);q=polar(cx,cy,r+(4 if a%30==0 else 1),a)
   s.ln(*p,*q,.32,.45)
 # A half-ellipse tangent to the two circular reference orbits.
 theta=math.radians(150);ux,uy=math.cos(theta),math.sin(theta);vx,vy=-uy,ux
 a,b=121,math.sqrt(121**2-25**2)
 coast=[]
 for j in range(121):
  t=math.pi*j/120
  xx=-25+a*math.cos(t);yy=b*math.sin(t)
  coast.append((cx+ux*xx+vx*yy,cy+uy*xx+vy*yy))
 s.poly(coast,.55,.7,close=False,dash=[4,4])
 e=coast[0];m=polar(cx,cy,146,62);end=coast[-1]
 p1=(e[0]-27,e[1]+54);p2=(m[0]-58,m[1]+29)
 s.bez(e,p1,p2,m,.9,1.0,color=ARC)
 def trajectory(t):
  return ((1-t)**3*e[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t*t*p2[0]+t**3*m[0],
          (1-t)**3*e[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t*t*p2[1]+t**3*m[1])
 for t in (.23,.49,.74):
  p=trajectory(t);s.circ(*p,2,.75,.55,color=ARC)
 for t in (.34,.83):
  p=trajectory(t);q=trajectory(t+.025);s.arrow(*p,*q,.8,.65,head=4,color=ARC)
 s.circ(*e,5,.9,.8,fill=.1)
 s.circ(*m,4,.9,.8,fill=.1,color=ARC)
 s.circ(*end,3.5,.5,.6)
 s.ln(cx,cy,*e,.23,.5,dash=[2,4]);s.ln(cx,cy,*m,.23,.5,dash=[2,4])
 # A small spacecraft marker tangent to the powered path.
 p=trajectory(.58);q=trajectory(.59);ang=math.atan2(q[1]-p[1],q[0]-p[0])
 s.c.save();s.c.translate(*p);s.c.rotate(ang)
 s.poly([(-6,-2),(5,0),(-6,2),(-3,0)],.85,.65,color=ARC)
 s.c.restore()
 s.text('EARTH / DEPARTURE',lx-187,cy+18,5.8,a=.75,align='r')
 s.poly([e,(lx-179,cy+43),(lx-179,cy+25)],.38,.5,close=False)
 s.text('MARS / ARRIVAL',m[0]+10,m[1]+12+s.type_growth(5.8),5.8,a=.75)  # enlarged type grows away from the marker
 # Each leader runs from its label to the path it names.
 s.text('FT-2 / 75 d',lx-138,477,6.5,a=.85,color=ARC)
 s.ln(lx-110,465,*trajectory(.3),.45,.5,color=ARC)
 s.text('CHEMICAL / 259 d',lx-203,153,6,a=.55)
 s.ln(lx-150,159,*coast[55],.3,.5)
 s.view_label(lx,520,'B','TRANSIT','EARTH TO MARS / TWO TRANSFERS')
