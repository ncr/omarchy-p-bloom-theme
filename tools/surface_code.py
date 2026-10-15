"""Rotated planar surface-code patch; d^2 data and d^2-1 check ancillas.

Reference: Bausch et al., Nature 635, 834–840 (2024), Fig. 1.
https://www.nature.com/articles/s41586-024-08148-8
Boundary convention: X checks on top/bottom, Z checks on left/right.
"""
from sheet import WHITE,ARC,GOLD

def patch(d=11):
 checks=[]
 for j in range(d-1):
  for i in range(d-1):
   checks.append(('X' if (i+j)%2==0 else 'Z',(i+.5,j+.5),
                  [(i,j),(i+1,j),(i+1,j+1),(i,j+1)]))
 for i in range(d-1):
  if i%2==1:checks.append(('X',(i+.5,-.5),[(i,0),(i+1,0)]))
  if i%2==0:checks.append(('X',(i+.5,d-.5),[(i,d-1),(i+1,d-1)]))
 for j in range(d-1):
  if j%2==0:checks.append(('Z',(-.5,j+.5),[(0,j),(0,j+1)]))
  if j%2==1:checks.append(('Z',(d-.5,j+.5),[(d-1,j),(d-1,j+1)]))
 return checks

def marker(s,x,y,kind,r=2.1):
 if kind=='X':s.poly([(x,y-r),(x+r,y),(x,y+r),(x-r,y)],.86,.6,color=ARC)
 else:s.rect(x-r,y-r,r*2,r*2,.78,.55)

def draw(s,lx):
 d=11;step=20;gx=lx-174;gy=174
 def pos(p):return gx+p[0]*step,gy+p[1]*step
 checks=patch(d)
 for kind,centre,support in checks:
  pts=[pos(p) for p in support]
  if len(pts)==2:pts.append(pos(centre))
  s.poly(pts,.27,.45,fill=.045 if kind=='X' else .015,color=ARC if kind=='X' else WHITE)
  cx,cy=pos(centre)
  for p in support:s.ln(cx,cy,*pos(p),.23,.4,color=ARC if kind=='X' else WHITE)
  marker(s,cx,cy,kind)
 # Z_L follows a horizontal row for this boundary convention.
 yy=gy+5*step
 s.ln(gx,yy,gx+10*step,yy,.8,1.05,color=GOLD)
 for j in range(d):
  for i in range(d):s.dot(*pos((i,j)),1.8,.91)
 s.text('Zₗ',gx+10*step+10,yy+3,7,a=.85,color=GOLD)
 # Enlarged weight-four X stabilizer, isolated from the full patch.
 cx,cy=lx+126,269;lead=14
 if s.layer_mode:
  # Enlarged type: the inset moves right until its widest line clears the patch and Zₗ.
  w=max(s.measure('4 DATA + 1 ANCILLA',5.4),s.measure('XXXX PARITY',5.8),s.measure('X CHECK',7))
  cx=min(max(cx,gx+10*step+10+s.measure('Zₗ',7)+14+w/2),lx+316-w/2)
  lead=max(14,s.readable_size(5.8)*1.3)
 s.text('X CHECK',cx,cy-49,7,a=.8,align='c',color=ARC)
 for dx,dy in [(-25,-25),(25,-25),(25,25),(-25,25)]:
  s.ln(cx,cy,cx+dx,cy+dy,.55,.65,color=ARC)
  s.dot(cx+dx,cy+dy,3,.9)
 marker(s,cx,cy,'X',4)
 s.text('4 DATA + 1 ANCILLA',cx,cy+45+s.type_growth(5.4),5.4,a=.65,align='c')
 s.text('XXXX PARITY',cx,cy+45+s.type_growth(5.4)+lead,5.8,a=.65,align='c',color=ARC)
 hx,hy=pos((6,4))
 s.rect(hx-2,hy-2,step+4,step+4,.66,.75,color=GOLD)
 s.poly([(hx+step+3,hy+1),(lx+62,214),(cx-30,cy-32)],.42,.5,close=False,dash=[3,3])
 # Separate legend explains symbols without writing over the circuit.
 ky=420
 if s.layer_mode:
  # Enlarged type: each word keeps a fixed gap to its marker and to the next marker.
  ky+=s.type_growth(6);x=lx-168;f=s.readable_size(6);near,far=3+.9*f,2.4*f
  s.dot(x,ky-3,2,.9);x=x+near+s.text('DATA',x+near,ky,6,a=.75)+far
  marker(s,x,ky-3,'X',2.6);x=x+near+s.text('X CHECK',x+near,ky,6,a=.75,color=ARC)+far
  marker(s,x,ky-3,'Z',2.6);s.text('Z CHECK',x+near,ky,6,a=.75)
  s.text('Zₗ / LOGICAL Z OPERATOR',lx-174,ky+22+s.type_growth(6),6,a=.7,color=GOLD)
 else:
  s.dot(lx-168,417,2,.9);s.text('DATA',lx-158,420,6,a=.75)
  marker(s,lx-82,417,'X',2.6);s.text('X CHECK',lx-71,420,6,a=.75,color=ARC)
  marker(s,lx+32,417,'Z',2.6);s.text('Z CHECK',lx+43,420,6,a=.75)
  s.text('Zₗ / LOGICAL Z OPERATOR',lx-174,442,6,a=.7,color=GOLD)
 s.view_label(lx,474,'B','ONE LOGICAL QUBIT','121 DATA + 120 ANCILLAS / DISTANCE 11')
