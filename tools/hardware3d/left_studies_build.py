"""Spatial explanatory insets: an implant tissue section and a dinner seating study."""
import sys,os,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import family_core as g
from mathutils import Vector,Matrix
from bio_details_build import curve
T=math.tau


def tissue():
    g.reset()
    def fold(x,y=0):return 5*math.cos(x/26)+2*math.sin(y/22)
    def slab(name,lo,hi,role='structure',xmin=-100,xmax=100,ymin=0,ymax=72):
        n=64;vs=[]
        for y in (ymin,ymax):
            for z in (lo,hi):
                vs += [(xmin+(xmax-xmin)*j/n,y,z+fold(xmin+(xmax-xmin)*j/n,y)) for j in range(n+1)]
        m=n+1;fs=[]
        for j in range(n):
            fs += [(j,j+1,j+1+m,j+m),(j+2*m,j+3*m,j+3*m+1,j+2*m+1),(j,j+2*m,j+2*m+1,j+1),(j+m,j+m+1,j+3*m+1,j+3*m)]
        fs += [(0,m,3*m,2*m),(n,n+2*m,n+3*m,n+m)]
        g.mesh(name,vs,fs,role)
    slab('white matter block',0,23,'shell')
    slab('cortical grey matter',23,73)
    for z in (30,39,49,60,68):
        g.wire('laminar boundary',[(x,-.4,z+fold(x)) for x in range(-100,101,2)],.12,'shell')
    # Meningeal envelope: pia follows the tissue; arachnoid bridges above it.
    for z in (74,82,85):slab('meningeal membrane',z,z+.6,'detail')
    for x in range(-96,100,8):
        g.wire('subarachnoid trabecula',[(x,-.3,75+fold(x)),(x+2,-.3,81+fold(x+2))],.10,'shell')
    for xmin,xmax in [(-100,-35),(35,100)]:
        slab('cranial diploe',88,111,'detail',xmin,xmax)
        slab('outer compact bone',111,114,'structure',xmin,xmax)
        slab('inner compact bone',86,89,'structure',xmin,xmax)
        for x in range(xmin+3,xmax-2,7):
            for z in (94,102,108):
                g.wire('cancellous bone trabecula',[(x,-.4,z+fold(x)),(x+3,-.4,z+2+fold(x)),(x+5,-.4,z-1+fold(x))],.11,'shell')
        slab('scalp',115,126,'structure',xmin,xmax)
        for x in range(xmin+3,xmax-3,6):g.wire('scalp section hatching',[(x,-.3,117+fold(x)),(x+3,-.3,124+fold(x+3))],.1,'shell')
    # A half-open can seated in the local bone recess; skin is locally omitted.
    n=64;vs=[]
    for z in (91,113):
        vs += [(31*math.cos(math.pi*j/n),31*math.sin(math.pi*j/n)+2,z) for j in range(n+1)]
    fs=[tuple(reversed(range(n+1)))]
    for j in range(n):fs.append((j,j+1,j+n+2,j+n+1))
    g.mesh('sectioned titanium can',vs,fs)
    for z in (93,111,114):g.wire('can rim',[(31*math.cos(math.pi*j/n),31*math.sin(math.pi*j/n)+2,z) for j in range(n+1)],.18,'detail')
    for z in (97,100,103):g.softbox('acoustic layer',(0,15,z),(50,24,1.1),2,'detail')
    g.softbox('decoder die',(0,7,108),(19,11,4),1,'accent')
    for side in (-1,1):
        for y in range(3,13,2):g.wire('die bond',[(side*9,y,110),(side*14,y,106)],.1,'cable')
    # A compliant mesh on the exposed front plane; separated from tissue texture.
    for k in range(9):
        x=-80+k*20;endz=36+(k%3)*10+fold(x)
        g.wire('deployed electrode strand',curve([(k-4,1,94),((k-4)*3,-1,78),(x*.75,-1,68),(x,-1,endz)]),.18,'accent')
        g.along_y('recording contact',x,-1.5,endz,1.2,.5,'cable',16)
    # Cell morphology is illustrative, deliberately sampled rather than a cell census.
    for i,x in enumerate(range(-86,95,28)):
        z=43+(i%2)*14+fold(x);y=-.7
        g.wire('pyramidal soma',[(x-1.6,y,z-2),(x,y,z+3),(x+1.8,y,z-2),(x-1.6,y,z-2)],.10,'detail')
        g.wire('apical dendrite',curve([(x,y,z+3),(x+1,y,z+9),(x-1,y,z+16)]),.09,'shell')
        for side in (-1,1):
            g.wire('basal dendrite',curve([(x,y,z),(x+side*4,y,z-3),(x+side*7,y,z-2)]),.09,'shell')
            g.wire('dendritic arbor',[(x,y,z+9),(x+side*4,y,z+12),(x+side*6,y,z+16)],.08,'shell')
        g.wire('axon',curve([(x,y,z-2),(x+2,y,z-9),(x-1,y,19)]),.08,'shell')
    for x in range(-96,100,9):g.wire('white matter fascicle',curve([(x,-.5,3),(x+3,-.5,10),(x+2,-.5,20)]),.10,'shell')
    for key,p in [('SCALP',(-72,0,122)),('SKULL',(-76,0,102)),('MENINGES',(-76,0,80)),('CORTEX',(85,0,49)),('WHITE',(86,0,12)),('IMPLANT',(18,7,108))]:g.mark(key,p)
    g.export('cortical-tissue-section',24,23)


def ellipse(name,x,y,z,rx,ry,r=.12,role='detail'):
    g.wire(name,[(x+rx*math.cos(T*k/64),y+ry*math.sin(T*k/64),z) for k in range(65)],r,role)


def dinner():
    g.reset()
    # Boat-shaped top, tapered pedestal feet and a real thick edge.
    n=128;vs=[]
    for z in (40,44):
        for k in range(n):
            a=T*k/n;vs.append((108*math.copysign(abs(math.cos(a))**.65,math.cos(a)),48*math.sin(a),z))
    fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    fs += [(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
    g.mesh('dining tabletop',vs,fs)
    for x in (-57,57):
        g.softbox('table pedestal',(x,0,22),(9,24,38),3)
        g.softbox('pedestal foot',(x,0,3),(15,57,5),2,'detail')
    seats=[(-135,0,-math.pi/2),(-48,77,math.pi),(48,77,math.pi),(135,0,math.pi/2),(48,-77,0),(-48,-77,0)]
    for idx,(x,y,ang) in enumerate(seats,1):
        before=len(g.parts);startw=len(g.wires)
        g.softbox('chair cushion',(0,0,22),(30,29,5),4)
        g.softbox('chair back',(0,-13,38),(30,4,29),3)
        g.softbox('back inset',(0,-15.2,38),(22,.8,17),2,'detail')
        for xx in (-11,11):
            for yy in (-10,10):g.beam('chair leg',(xx*1.17,yy*1.18,0),(xx,yy,22),1.2,'detail')
        mat=Matrix.Translation((x,y,0))@Matrix.Rotation(ang,4,'Z')
        for o,role in g.parts[before:]:o.matrix_world=mat@o.matrix_world
        # The chair is geometry only; no local wires need transforming.
        assert len(g.wires)==startw
        direction=Vector((-math.sin(ang),math.cos(ang),0));px=x+direction.x*46;py=y+direction.y*46
        g.cyl('dinner plate',px,py,44.2,12,1,'detail',48)
        ellipse('plate well',px,py,45.3,8.4,8.4)
        # Cutlery placed tangentially beside each plate, aligned toward its sitter.
        tangent=Vector((-direction.y,direction.x,0))
        for side in (-1,1):
            c=Vector((px,py,45))+tangent*side*16
            a=c-direction*8;b=c+direction*8
            g.wire('cutlery stem',[a,b],.2,'detail')
            if side<0:
                for d in (-.7,0,.7):g.wire('fork tine',[b-direction*3+tangent*d,b+tangent*d],.10,'detail')
            else:g.wire('knife edge',[a+tangent*.8,b+tangent*.8,b],.13,'detail')
        cup=Vector((px,py,45))+direction*17+tangent*13
        g.cyl('glass foot',cup.x,cup.y,44.2,3,.6,'detail',24)
        g.cyl('glass stem',cup.x,cup.y,45,.5,5,'detail',16)
        ellipse('glass bowl rim',cup.x,cup.y,57,4,4)
        for side in (-1,1):g.wire('glass bowl wall',curve([(cup.x+side*4,cup.y,57),(cup.x+side*3,cup.y,52),(cup.x,cup.y,50)]),.1,'detail')
        g.mark(f'S{idx}',(x,y,39))
    g.softbox('serving platter',(0,0,45),(49,24,2),9,'detail')
    for x,y,r in [(-12,0,5),(1,3,5),(12,-2,4)]:
        g.ball('bread on platter',(x,y,48),(r,r*.65,3),'shell')
    # Low receiver on the table, visibly distinct from the serving dish.
    g.softbox('table event receiver',(0,-30,47),(23,9,5),2,'detail')
    for x in (-7,-3,1,5):g.wire('receiver indicator',[(x,-34.6,46),(x,-34.6,48)],.1,'accent')
    g.export('truth-dinner-seating',-18,56)


if __name__=='__main__':
    chosen=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['tissue','dinner']
    for name in chosen:globals()[name]()
    sys.stdout.flush();os._exit(0)
