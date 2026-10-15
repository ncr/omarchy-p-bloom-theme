"""Three authored auxiliary scenes; export real occlusion-tested vector lines.

blender -b --factory-startup -t 4 --python tools/hardware3d/right_aux_build.py
"""
import sys, os, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import family_core as g
import bpy
from mathutils import Vector, Matrix


def tube(name,points,radius,role='accent'):
    """Smooth branched-organ channels, exported as walls rather than centrelines."""
    knots=[Vector(p) for p in points];pad=[knots[0]]+knots+[knots[-1]];path=[]
    for j in range(len(knots)-1):
        a,b,c,d=pad[j:j+4]
        for k in range(16):
            t=k/16
            path.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
    path.append(knots[-1]);vs=[];fs=[];n=16
    for j,p in enumerate(path):
        tangent=(path[min(j+1,len(path)-1)]-path[max(0,j-1)]).normalized()
        u=tangent.cross(Vector((0,0,1))).normalized();v=tangent.cross(u)
        r=radius*(1-.22*j/(len(path)-1))
        for k in range(n):vs.append(p+r*(u*math.cos(math.tau*k/n)+v*math.sin(math.tau*k/n)))
    for j in range(len(path)-1):
        for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
    fs.extend([tuple(reversed(range(n))),tuple((len(path)-1)*n+k for k in range(n))])
    return g.mesh(name,vs,fs,role)


def owner():
    g.reset()
    # The same molded stand-in as the other human illustrations, lying supine.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'mannequin3d'))
    import build as dummy
    dummy.body('presence')
    matrix=Matrix(((0,0,-.25,0),(.25,0,0,0),(0,-.25,0,42),(0,0,0,1)))
    deps=bpy.context.evaluated_depsgraph_get()
    # Only the visible head/neck/shoulders; everything else is beneath the duvet.
    for o in dummy.objects:
        if o.name not in ('head','VISOR','neck coupling','DARK collar','torso'):
            continue
        ev=o.evaluated_get(deps);me=ev.to_mesh()
        lift=9 if o.name in ('head','VISOR','neck coupling') else 7
        verts=[matrix @ o.matrix_world @ v.co + Vector((0,0,lift)) for v in me.vertices]
        faces=[tuple(p.vertices) for p in me.polygons]
        g.mesh('owner '+o.name,verts,faces,'detail' if o.name=='VISOR' else 'structure')
        ev.to_mesh_clear()
    for o in dummy.objects:
        bpy.data.objects.remove(o,do_unlink=True)
    g.softbox('low cast bed frame',(0,0,15),(214,107,14),8)
    g.softbox('mattress',(0,0,28),(202,99,16),7)
    for x in (-79,79):
        for y in (-36,36):g.cyl('recessed bed foot',x,y,0,5,12)
    g.softbox('headboard',(-109,0,40),(9,110,75),6)
    g.softbox('headboard inset',(-103.8,0,46),(1,87,41),.4,'detail')
    g.softbox('pillow',(-79,0,38),(40,64,13),6)
    # Continuous draped surface with a body-shaped rise, not a flat rectangle.
    def duvet(x,y):
        body=21*math.exp(-((x+20)/56)**2-(y/28)**4)
        legs=5*math.exp(-((x-50)/30)**2)*(math.exp(-((y-12)/12)**2)+math.exp(-((y+12)/12)**2))
        drape=14*max(0,(abs(y)-36)/18)**1.3
        fold=1.5*math.sin(x/17+y/13)*math.exp(-((abs(y)-34)/19)**2)
        return (x,y,39+body+legs-drape+fold)
    nx,ny=52,38;vs=[];fs=[]
    for i in range(nx+1):
        for j in range(ny+1):vs.append(duvet(-55+153*i/nx,-55+110*j/ny))
    for i in range(nx):
        for j in range(ny):
            k=i*(ny+1)+j;fs.append((k,k+1,k+ny+2,k+ny+1))
    g.mesh('duvet',vs,fs)
    for x in (-53,-48,95):g.wire('stitched transverse hem',[Vector(duvet(x,-55+110*j/80))+Vector((0,0,.18)) for j in range(81)],.12,'detail')
    for y in (-53,-48,48,53):g.wire('stitched side hem',[Vector(duvet(-55+153*j/100,y))+Vector((0,0,.18)) for j in range(101)],.12,'detail')
    for yy in (-34,-19,19,34):
        g.wire('draped fold',[Vector(duvet(-39+128*j/90,yy+3*math.sin(j/22)))+Vector((0,0,.2)) for j in range(91)],.14,'detail')
    # Bedside receiver has a cradle, a separate screen and actual controls.
    g.softbox('nightstand',(-73,-88,18),(52,43,34),5)
    g.softbox('nightstand drawer',(-72,-110,19),(40,1,21),.3,'detail')
    g.beam('drawer pull',(-79,-112,23),(-65,-112,23),.9)
    g.softbox('phone cradle',(-73,-89,38),(28,21,5),2)
    g.softbox('receiver shell',(-73,-87,53),(24,6,32),2)
    g.softbox('receiver screen',(-73,-90.4,55),(19,.5,22),.5,'accent')
    for x in (-79,-73,-67):g.ball('receiver button',(x,-90.8,43),(1,1,1),'detail')
    g.mark('HUMAN',(-81,0,56));g.mark('RECEIVER',(-73,-91,58))
    g.export('proxy-sleeping-owner',32,47)


def course():
    g.reset()
    def p(t):
        return Vector((151*math.cos(t)+37*math.sin(2*t),95*math.sin(t)+14*math.cos(3*t),105+75*math.sin(t+.45)))
    # Gates are normal to the local flight path, not marks in the page plane.
    for j in range(9):
        t=math.tau*j/9
        c=p(t);normal=(p(t+.001)-p(t-.001)).normalized()
        u=normal.cross(Vector((0,0,1))).normalized();v=normal.cross(u)
        mat=Matrix((u,v,normal)).transposed().to_4x4();mat.translation=c
        # A thin structural hoop plus small orthogonal equipment pods.
        for off in (-1.5,1.5):
            g.wire('gate rim', [c+u*18*math.cos(a)+v*18*math.sin(a)+normal*off for a in [math.tau*k/96 for k in range(97)]],.65,'cable' if j==0 else 'structure')
        for k in range(4):
            a=math.tau*k/4;position=c+(u*math.cos(a)+v*math.sin(a))*18
            o=g.softbox('gate beacon', (0,0,0),(5,5,6),.7,'detail')
            o.matrix_world=Matrix.Translation(position) @ mat.to_3x3().to_4x4()
        # Height witnesses terminate at unobtrusive ground registration crosses.
        for z in range(0,max(1,int(c.z-19)),7):
            g.wire('altitude witness',[(c.x,c.y,z),(c.x,c.y,min(z+3,c.z-19))],.13,'shell')
        for dx,dy in ((4,0),(0,4)):
            g.wire('ground datum',[(c.x-dx,c.y-dy,0),(c.x+dx,c.y+dy,0)],.2,'shell')
        g.mark(f'G{j+1}',c)
    # Broken trajectory keeps the spatial illustration light and readable.
    for k in range(112):
        a=math.tau*k/112;b=a+math.tau/112*.67
        g.wire('flight trajectory',[p(a+(b-a)*i/5) for i in range(6)],.28,'accent')
    for k in range(9):
        t=math.tau*(k+.47)/9;c=p(t);n=(p(t+.01)-p(t-.01)).normalized();u=n.cross(Vector((0,0,1))).normalized()
        g.wire('course direction',[c-n*5+u*2,c,c-n*5-u*2],.28,'accent')
    # A few projected ground contours establish a datum without another oval.
    for y in (-110,-55,0,55,110):g.wire('survey grid',[(-182,y,0),(182,y,0)],.1,'shell')
    for x in (-180,-90,0,90,180):g.wire('survey grid',[(x,-111,0),(x,111,0)],.1,'shell')
    g.export('sky-racer-course',-19,38)


def kidney():
    from bio_details_build import kidney as build_kidney
    build_kidney()


if __name__=='__main__':
    chosen=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['owner','course','kidney']
    for name in chosen:globals()[name]()
    sys.stdout.flush();os._exit(0)
