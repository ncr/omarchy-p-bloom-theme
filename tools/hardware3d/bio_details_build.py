"""Authored biological detail studies, not measured anatomy or implant designs.

blender -b --factory-startup -t 4 --python tools/hardware3d/bio_details_build.py
"""
import math, sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mathutils import Vector
import family_core as g
from right_aux_build import tube
TAU=math.tau


def curve(points, steps=18):
    p=[Vector(v) for v in points]; pad=[p[0]]+p+[p[-1]]; out=[]
    for j in range(len(p)-1):
        a,b,c,d=pad[j:j+4]
        for k in range(steps):
            t=k/steps
            out.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
    return out+[p[-1]]


def kidney():
    g.reset()
    def outline(t,k=1,z=22):
        # Asymmetric poles and a real hilar concavity.
        x=66*math.cos(t)-40*math.exp(-(math.sin(t)/.35)**2)*max(0,math.cos(t))**5
        return Vector((x*k,107*math.sin(t)*k*(1+.055*math.cos(t-.5)),z))
    n=192; vs=[]
    rings=[(.79,-16),(.93,-10),(1,4),(1,22)]
    for scale,z in rings:vs.extend(outline(TAU*j/n,scale,z) for j in range(n))
    fs=[]
    for layer in range(3):
        for j in range(n):fs.append((layer*n+j,layer*n+(j+1)%n,(layer+1)*n+(j+1)%n,(layer+1)*n+j))
    fs.extend([tuple(reversed(range(n))),tuple(3*n+j for j in range(n))])
    g.mesh('renal cut face and capsule',vs,fs,'shell')
    g.wire('continuous cut-face boundary',[outline(TAU*j/n,1.003,22.7) for j in range(n+1)],.10,'structure')
    for k in (1,.972):g.wire('capsule',[outline(TAU*j/n,k,22.4) for j in range(n+1)],.16,'detail')
    # A scalloped corticomedullary boundary, following the lobe bases.
    g.wire('corticomedullary interface',[outline(math.radians(35+290*j/180),.79+.012*math.cos(j*.24),23.2) for j in range(181)],.10,'shell')
    # Different papilla positions and three major calyces prevent a rotor layout.
    lobes=[(53,.22,(22,37,24)),(92,.22,(0,43,24)),(135,.24,(-15,31,24)),
           (179,.25,(-25,3,24)),(221,.24,(-17,-27,24)),(263,.22,(1,-43,24)),(307,.21,(23,-33,24))]
    hubs=[Vector((19,26,25)),Vector((4,0,25)),Vector((20,-26,25))]
    for idx,(deg,spread,tip) in enumerate(lobes):
        t=math.radians(deg); tip=Vector(tip); base=outline(t,.77,24)
        left=outline(t-spread,.77,24);right=outline(t+spread,.77,24)
        u=(right-left).normalized(); axis=(base-tip).normalized()
        # Broad curved base, rounded papilla, gently convex sides.
        contour=curve([tip-u*2,left*.55+tip*.45-u*1,left,base,right,right*.55+tip*.45+u*1,tip+u*2,tip-u*2])
        g.wire('medullary lobe',contour,.23,'detail')
        # Convergent tubules, each stopping at its own papillary exit.
        for j in range(12):
            f=(j+.5)/12; end=outline(t-spread+2*spread*f,.765,24.5)
            start=tip+axis*4+u*((f-.5)*5)
            mid=start.lerp(end,.52)+u*(math.sin(f*math.pi)*1.8)
            g.wire('medullary tubule bundle',curve([start,mid,end]),.10,'shell')
        hub=hubs[0 if idx<2 else 1 if idx<5 else 2]
        # Minor calyx cup wraps around a papilla instead of ending in a point.
        mouth=tip+axis*3
        cup=curve([mouth-u*4.3,tip-axis*4-u*3,tip-axis*6,tip-axis*4+u*3,mouth+u*4.3])
        g.wire('minor calyx lip',cup,.3,'cable')
        tube('minor collecting branch',[hub,hub.lerp(tip,.6)-axis*3,tip-axis*5],1.9,'cable')
        # Arcuate vessel and repeated cortical units; enlarged for legibility.
        arc=[outline(t-spread+2*spread*j/24,.81,25) for j in range(25)]
        tube('arcuate artery',[arc[j] for j in (0,6,12,18,24)],.65,'accent')
        for j in range(6):
            ang=t-spread*.92+spread*1.84*j/5
            a=outline(ang,.815,25);b=outline(ang+.009,.932,25)
            g.wire('cortical radial artery',curve([a,a.lerp(b,.5)+Vector((.6,0,0)),b]),.17,'accent')
            for sign in (-1,1):
                c=outline(ang+sign*.021,.90 if sign<0 else .94,25)
                stem=a.lerp(b,.50 if sign<0 else .77)
                g.wire('afferent branch',curve([stem,(stem+c)/2,c]),.12,'accent')
                # Selected corpuscles are symbolic, not an exhaustive nephron map.
                g.wire('renal corpuscle',[c+Vector((1.15*math.cos(TAU*k/24),1.4*math.sin(TAU*k/24),.1)) for k in range(25)],.1,'detail')
                g.wire('cortical convoluted tubule',[c+Vector((sign*(1.6+q*.22),math.sin(q*1.15)*1.3,.15)) for q in range(15)],.09,'shell')
    root=Vector((26,4,28))
    tube('renal artery',[(64,9,30),(48,9,30),root],2.8,'accent')
    # Segmental branching in the sinus, then interlobar routes between lobes.
    for deg,hub in [(29,hubs[0]),(73,hubs[0]),(114,hubs[0]),(157,hubs[1]),(200,hubs[1]),(241,hubs[2]),(286,hubs[2]),(331,hubs[2])]:
        end=outline(math.radians(deg),.815,26)
        start=hub+Vector((0,0,3)); mid=start.lerp(end,.58)
        tube('interlobar vessel',[root,start,mid,end],.85,'accent')
    pelvis=Vector((28,-8,24))
    for h in hubs:tube('major calyx',[pelvis,pelvis.lerp(h,.5)+Vector((2,0,0)),h],3.2,'cable')
    tube('ureter',[pelvis,(41,-24,21),(50,-51,14),(58,-86,4)],3.4,'cable')
    for z,k in [(-8,.948),(-3,.973),(3,1.001),(9,1.003),(15,1.003)]:
        g.wire('printed tissue strata',[outline(TAU*j/n,k,z) for j in range(n+1)],.10,'shell')
    g.mark('CORTEX',outline(math.radians(142),.9,25))
    g.mark('MEDULLA',(-32,-45,25));g.mark('SUPPLY',(60,9,30));g.mark('DRAIN',(58,-86,4))
    g.export('foundry-renal-section',-24,56)


def rounded(w,h,r,z,cx=0,cy=0):
    pts=[]
    for x,y,start in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
        for k in range(17):
            a=math.radians(start+90*k/16)
            pts.append(Vector((cx+x+r*math.cos(a),cy+y+r*math.sin(a),z)))
    return pts


def film(name,w,h,r,z,thick,hole=None,role='structure'):
    outer=rounded(w,h,r,z); n=len(outer)
    if hole:
        inner=rounded(*hole,z);vs=outer+inner+[p+Vector((0,0,thick)) for p in outer+inner];fs=[]
        for j in range(n):
            k=(j+1)%n
            fs.extend([(j,k,k+n,j+n),(j+2*n,j+3*n,k+3*n,k+2*n),(j,k,k+2*n,j+2*n),(j+n,j+3*n,k+3*n,k+n)])
    else:
        vs=outer+[p+Vector((0,0,thick)) for p in outer];fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]
        for j in range(n):fs.append((j,(j+1)%n,(j+1)%n+n,j+n))
    g.mesh(name,vs,fs,role)


def node():
    g.reset()
    # Drawing units are illustrative; vertical separation exaggerates film thickness.
    film('compliant carrier',116,86,22,0,1.6)
    film('patterned metallization carrier',106,76,18,31,1.1)
    film('passivation window',100,72,17,63,1.2,(49,35,10))
    film('porous recording contact',45,31,9,94,1.1)
    # A serpentine mesh tether, with a real continuous curved ribbon surface.
    def ribbon(t,v):
        return Vector((-49-98*t,13*math.sin(TAU*t*.8)+v,-.5+10*t*t))
    n=120;vs=[ribbon(i/n,v) for i in range(n+1) for v in (-12,12)];fs=[]
    for i in range(n):fs.append((2*i,2*i+2,2*i+3,2*i+1))
    g.mesh('flexible routing tail',vs,fs)
    for v in (-10,10):g.wire('ribbon edge reinforcement',[ribbon(i/n,v)+Vector((0,0,.2)) for i in range(n+1)],.17,'detail')
    for v in (-6,-2,2,6):
        g.wire('serpentine conductor',[ribbon(i/n,v)+Vector((0,0,.3)) for i in range(n+1)],.18,'cable')
    # Eight independent conductors: nested fanout lanes, no decorative shorts.
    # The large centre contact is shown lifted above its actual landing.
    for j in range(8):
        yy=-24+j*6.8; end_y=-10+j*2.8
        pts=[(-49,yy,32.3),(-35-j*.6,yy,32.3),(-24-j*.6,end_y,32.3),(-16,end_y,32.3)]
        g.wire('isolated fanout lane',pts,.14,'cable')
    film('recording bond',33,25,6,32.35,.25,role='accent')
    for y in (-8,-3,2,7):
        g.wire('contact landing finger',[(-17,y,32.8),(-9,y,32.8)],.16,'cable')
    # Nested guard electrode follows three sides of the sensing region.
    for d in (0,3):
        g.wire('guard conductor',[(-17,19+d,32.6),(24+d,19+d,32.6),(31+d,12+d,32.6),(31+d,-14-d,32.6),(24+d,-21-d,32.6),(-17,-21-d,32.6)],.13,'cable')
    # Open serpentine tethers on the opposite side make the mesh context visible.
    for side in (-1,1):
        path=[(49,side*17,1),(65,side*22,2),(73,side*34,6),(85,side*38,11),(96,side*31,15)]
        cc=curve(path)
        left=[];right=[]
        for j,p in enumerate(cc):
            tangent=(cc[min(j+1,len(cc)-1)]-cc[max(0,j-1)]).normalized()
            u=Vector((-tangent.y,tangent.x,0)).normalized()*3
            left.append(p-u);right.append(p+u)
        vs=left+right;n=len(left)
        g.mesh('open mesh tether',vs,[(j,j+1,j+1+n,j+n) for j in range(n-1)])
        g.wire('tether conductor',[p+Vector((0,0,.2)) for p in cc],.14,'cable')
    # Bond perimeter stitching and via lands on the metal layer.
    for sign in (-1,1):
        for j in range(9):
            x=-29+j*7.2;y=sign*29
            g.wire('via land',[Vector((x+1.0*math.cos(TAU*k/20),y+1.0*math.sin(TAU*k/20),32.3)) for k in range(21)],.13,'detail')
    # Irregular but repeatable pore openings suggest deposited electrode texture.
    for row in range(6):
        for col in range(9):
            x=-16+col*4+(row%2)*1.2;y=-9+row*3.6
            if abs(x)>17 and abs(y)>7:continue
            r=.7+.17*math.sin(row*13+col*7)
            g.wire('porous contact opening',[(x+r*(1+.12*math.sin(k*2.1))*math.cos(TAU*k/18),y+r*.76*math.sin(TAU*k/18),95.25) for k in range(19)],.1,'detail')
    # Fine witness axes distinguish the exploded components from a physical stack.
    for x,y in [(-36,-22),(36,22)]:
        for z in range(4,91,6):g.wire('exploded alignment',[(x,y,z),(x,y,z+2.6)],.08,'shell')
    # Base relief slots are sparse and follow the membrane edge.
    for sign in (-1,1):
        for j in range(7):
            x=-27+j*9
            g.wire('strain relief slot',curve([(x-2,sign*30,1.9),(x,sign*33,1.9),(x+3,sign*30,1.9)]),.12,'detail')
    g.mark('CONTACT',(18,0,95));g.mark('WINDOW',(48,7,64));g.mark('ROUTING',(48,-15,32));g.mark('CARRIER',(42,-30,2))
    g.export('cortical-node-exploded',-27,34)


if __name__=='__main__':
    chosen=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['kidney','node']
    for name in chosen:globals()[name]()
    sys.stdout.flush();os._exit(0)
