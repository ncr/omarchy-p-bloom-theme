"""Shared fabrication vocabulary, not a shared machine silhouette. Blender only."""
import math,sys,json,os
from pathlib import Path
from contextlib import contextmanager
import bpy
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/hardware3d'))
import family_core as g
from .exporter import export
from bio_details_build import curve
T=math.tau
GROUPS={};NOTES={};CURRENT=None;VIEW_ANGLES={}


def reset(entry):
    global GROUPS,NOTES,CURRENT,VIEW_ANGLES
    g.reset();GROUPS={};NOTES={};CURRENT=entry;VIEW_ANGLES={}
    g.OUT=ROOT/'tools/assets/century';g.OUT.mkdir(parents=True,exist_ok=True)
    g.STUDY=ROOT/'concepts/century/models';g.STUDY.mkdir(parents=True,exist_ok=True)


@contextmanager
def group(key):
    start=len(g.parts);wstart=len(g.wires)
    yield
    GROUPS.setdefault(key,{'parts':[],'wires':[]})
    GROUPS[key]['parts'].extend(g.parts[start:]);GROUPS[key]['wires'].extend(g.wires[wstart:])


def mark(name,p,detail):
    g.mark(name,p);NOTES[name]=detail


def box(name,p,size,r=3,role='structure'):
    return g.softbox(name,p,size,r,role)


def rod(name,a,b,r=2,role='structure'):
    return g.beam(name,a,b,r,role,16)


def tube(name,points,r=1.0,role='cable'):
    g.wire(name,curve(points),r,role)


def cyl(name,p,r,h,role='structure',axis=(0,0,1),n=48):
    o=g.cyl(name,0,0,0,r,h,role,n);o.matrix_world=Matrix.Translation(p)@Vector(axis).to_track_quat('Z','Y').to_matrix().to_4x4();return o


def ring(name,p,r,thick=2,depth=5,axis=(0,0,1),role='structure',start=0,end=360):
    n=max(16,round((end-start)/4));vs=[];fs=[]
    m=Matrix.Translation(p)@Vector(axis).to_track_quat('Z','Y').to_matrix().to_4x4()
    for z in (0,depth):
        for rr in (r-thick,r):
            vs.extend(m@Vector((rr*math.cos(math.radians(start+(end-start)*j/n)),rr*math.sin(math.radians(start+(end-start)*j/n)),z)) for j in range(n+1))
    k=n+1
    for j in range(n):fs.extend([(j,j+1,k+j+1,k+j),(2*k+j,3*k+j,3*k+j+1,2*k+j+1),(j,2*k+j,2*k+j+1,j+1),(k+j,k+j+1,3*k+j+1,3*k+j)])
    if end-start<359.9:fs.extend([(0,k,3*k,2*k),(n,n+2*k,n+3*k,n+k)])
    return g.mesh(name,vs,fs,role)


def bolts(p,r,count=8,axis=(0,0,1),size=1.4):
    m=Matrix.Translation(p)@Vector(axis).to_track_quat('Z','Y').to_matrix().to_4x4()
    for j in range(count):
        a=T*j/count;o=cyl('captive fastener',(r*math.cos(a),r*math.sin(a),0),size,size*1.2,'detail',n=6);o.matrix_world=m@o.matrix_world


def flange(name,p,r,axis=(0,0,1),depth=5):
    # Bolt centres belong to the material of the flange, never its open aperture.
    wall=min(6,max(.8,r*.22));depth=min(depth,max(.8,r*.28))
    ring(name,p,r,wall,depth,axis);m=Vector(p)+Vector(axis)*depth
    bolts(m,r-wall*.5,8 if r>=8 else 6,axis,min(1.5,wall*.23))


def joint(p,r=12,axis=(0,1,0)):
    depth=max(1.5,r*.62)
    cyl('pivot body',p,r,depth,'structure',axis)
    flange('retainer',Vector(p)+Vector(axis)*depth,r*1.08,axis,max(.8,r*.15))


def uncover(key,*prefixes):
    """Service view omits selected covers but reuses all remaining original geometry."""
    selected=GROUPS[key]
    selected['removed_covers']=list(prefixes)
    selected['parts']=[(o,r) for o,r in selected['parts'] if not o.name.startswith(prefixes)]
    selected['wires']=[w for w in selected['wires'] if not w[0].startswith(prefixes)]



def panel(name,p,size,axis=(0,0,1),nx=8,ny=5,role='detail'):
    w,h=size;m=Matrix.Translation(p)@Vector(axis).to_track_quat('Z','Y').to_matrix().to_4x4()
    before=len(g.parts);beforew=len(g.wires)
    box(name,(0,0,0),(w,h,2),1,'structure')
    for x in (-w/2+3,w/2-3):rod('panel edge',(x,-h/2,1),(x,h/2,1),.7,'detail')
    for i in range(1,nx):g.wire('panel seam',[(-w/2+w*i/nx,-h/2+3,1.2),(-w/2+w*i/nx,h/2-3,1.2)],.1,role)
    for i in range(1,ny):g.wire('panel cross seam',[(-w/2+3,-h/2+h*i/ny,1.2),(w/2-3,-h/2+h*i/ny,1.2)],.1,role)
    transform(before,beforew,m)


def transform(start,wstart,m):
    for o,role in g.parts[start:]:o.matrix_world=m@o.matrix_world
    for i in range(wstart,len(g.wires)):
        n,pts,role=g.wires[i];g.wires[i]=(n,[m@p for p in pts],role)


@contextmanager
def at(p=(0,0,0),angle=0,axis='Z'):
    start=len(g.parts);wstart=len(g.wires)
    yield
    transform(start,wstart,Matrix.Translation(p)@Matrix.Rotation(math.radians(angle),4,axis))


def profile_at(sections,pos):
    # Monotone cubic Hermite sections: smooth silhouettes without bulging overshoot.
    i=next((i for i in range(len(sections)-1) if pos<=sections[i+1][0]),len(sections)-2)
    a,b=sections[i],sections[i+1];h=b[0]-a[0];t=max(0,min(1,(pos-a[0])/h));out=[]
    for k in (1,2,3):
        ds=[(q[k]-p[k])/(q[0]-p[0]) for p,q in zip(sections,sections[1:])]
        slopes=[ds[0]]
        for d0,d1 in zip(ds,ds[1:]):
            slopes.append(0 if d0*d1<=0 else math.copysign(min(abs((d0+d1)/2),3*min(abs(d0),abs(d1))),d0))
        slopes.append(ds[-1]);v=(2*t**3-3*t*t+1)*a[k]+(t**3-2*t*t+t)*h*slopes[i]+(-2*t**3+3*t*t)*b[k]+(t**3-t*t)*h*slopes[i+1]
        out.append(v)
    return tuple(out)


def hull(name,sections,axis='X',role='structure',exponent=.7):
    n=64;vs=[];fs=[];samples=[]
    for a,b in zip(sections,sections[1:]):
        samples.extend(a[0]+(b[0]-a[0])*j/10 for j in range(10))
    samples.append(sections[-1][0])
    for pos in samples:
        rx,rz,lift=profile_at(sections,pos)
        for j in range(n):
            a=T*j/n;v=rx*math.copysign(abs(math.cos(a))**exponent,math.cos(a));z=lift+rz*math.copysign(abs(math.sin(a))**exponent,math.sin(a))
            vs.append((pos,v,z) if axis=='X' else (v,pos,z))
    for i in range(len(samples)-1):
        for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    fs += [tuple(reversed(range(n))),tuple((len(samples)-1)*n+j for j in range(n))]
    o=g.mesh(name,vs,fs,role);o['section_data']=json.dumps({'sections':sections,'axis':axis,'exponent':exponent});return o


def hull_seam(obj,station,role='detail'):
    d=json.loads(obj['section_data']);rx,rz,lift=profile_at(d['sections'],station);exp=d['exponent'];pts=[]
    for k in range(129):
        a=T*k/128;v=(rx+.38)*math.copysign(abs(math.cos(a))**exp,math.cos(a));z=lift+(rz+.38)*math.copysign(abs(math.sin(a))**exp,math.sin(a))
        pts.append(obj.matrix_world@Vector((station,v,z) if d['axis']=='X' else (v,station,z)))
    g.wire('conformal hull seam',pts,.07,role)


def organic_branch(name,points,radius=1.8,role='detail'):
    pts=[Vector(v) for v in curve(points)];vs=[];fs=[];n=12
    for i,p in enumerate(pts):
        tangent=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized()
        u=tangent.cross(Vector((0,0,1)))
        if u.length<.05:u=tangent.cross(Vector((0,1,0)))
        u.normalize();v=tangent.cross(u);r=radius*(1-.48*i/(len(pts)-1))
        for j in range(n):a=T*j/n;vs.append(p+r*(math.cos(a)*u+math.sin(a)*v))
    for i in range(len(pts)-1):
        for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    fs.extend([tuple(reversed(range(n))),tuple((len(pts)-1)*n+j for j in range(n))]);return g.mesh(name,vs,fs,role)


def vessel(name,p,r,h):
    with at(p):
        g.casting(name,[(0,r*.62,r*.62),(h*.08,r*.9,r*.9),(h*.2,r,r),(h*.8,r,r),(h*.92,r*.9,r*.9),(h,r*.62,r*.62)])
        # The shell is a rounded-square casting, not a circular cylinder.
        # Match its section so the seam cannot disappear inside the corners.
        for z in (h*.2,h*.8):g.trim('conformal vessel seam',z,r+.6,r+.6)
        flange('service neck',(0,0,h),r*.38)
        for side in (-1,1):rod('vessel saddle',(side*r*.7,0,-10),(side*r*.7,0,8),3,'detail')


def motor(p,r=16,length=35,axis=(0,0,1),fins=True):
    m=Matrix.Translation(p)@Vector(axis).to_track_quat('Z','Y').to_matrix().to_4x4()
    b=len(g.parts);w=len(g.wires)
    cyl('motor case',(0,0,0),r,length)
    for z in range(3,int(length-3),4) if fins else ():ring('cooling fin',(0,0,z),r+2,1.2,1.2,role='detail')
    flange('motor face',(0,0,length),r+2)
    cyl('output shaft',(0,0,length+3),r*.24,13,'detail')
    box('terminal housing',(r,0,length*.55),(9,13,16),2,'detail')
    transform(b,w,m)


def rotor(p,r=45,blades=5,axis=(0,0,1),twist=25):
    m=Matrix.Translation(p)@Vector(axis).to_track_quat('Z','Y').to_matrix().to_4x4();b=len(g.parts);w=len(g.wires)
    cyl('rotor hub',(0,0,-4),r*.19,12)
    for k in range(blades):
        vs=[];fs=[];a=T*k/blades
        for j in range(8):
            rr=r*(.18+.82*j/7);chord=r*(.24-.11*j/7);pitch=math.radians(twist)*(1-j/10)
            for t in (-1,1):
                tang=chord*t/2;vs.append((rr*math.cos(a)-tang*math.sin(a),rr*math.sin(a)+tang*math.cos(a),tang*math.sin(pitch)))
        for j in range(7):fs.append((2*j,2*j+1,2*j+3,2*j+2))
        g.mesh('twisted rotor blade',vs,fs)
    bolts((0,0,9),r*.12,6,size=1.0)
    transform(b,w,m)


def truss(a,b,width=15,steps=6):
    a,b=Vector(a),Vector(b);d=(b-a).normalized();u=d.cross(Vector((0,0,1)))
    if u.length<.1:u=Vector((1,0,0))
    u.normalize();v=d.cross(u)
    for off in (u+v,u-v,-u+v,-u-v):rod('truss longeron',a+off*width/2,b+off*width/2,1)
    for j in range(steps):
        p=a.lerp(b,j/steps);q=a.lerp(b,(j+1)/steps)
        for off in (u,-u):rod('diagonal brace',p+off*width/2+v*width/2,q+off*width/2-v*width/2,.65,'detail')


def pump(p=(0,0,0),scale=1):
    b=len(g.parts);w=len(g.wires)
    cyl('pump volute',(0,0,0),20,14)
    flange('pump cover',(0,0,14),21)
    cyl('suction throat',(0,0,17),8,15,'detail')
    rod('discharge',(15,0,7),(34,0,7),6)
    flange('discharge flange',(34,0,7),9,(1,0,0))
    motor((0,0,-31),12,29)
    transform(b,w,Matrix.Translation(p)@Matrix.Scale(scale,4))


def optics(p=(0,0,0),r=15,length=30,axis=(0,-1,0)):
    b=len(g.parts);w=len(g.wires)
    cyl('optical barrel',(0,0,0),r,length)
    for z in (3,length-8,length-2):ring('barrel retaining band',(0,0,z),r+1.5,1,2,role='detail')
    ring('lens hood',(0,0,length),r+2,2,6)
    cyl('lens',(0,0,length+1),r-2,.6,'accent')
    bolts((0,0,length+1),r-.7,6,size=.8)
    transform(b,w,Matrix.Translation(p)@Vector(axis).to_track_quat('Z','Y').to_matrix().to_4x4())


def radiator(p,size=(70,100),axis=(0,0,1)):
    panel('radiator face',p,size,axis,12,4,'shell')


def skid(w=180,d=120):
    for x in (-w/2,w/2):
        rod('skid rail',(x,-d/2,0),(x,d/2,0),4)
        for y in (-d*.35,d*.35):rod('skid strut',(x,y,0),(x*.8,y,17),3)
    for y in (-d*.35,d*.35):rod('cross bearer',(-w*.4,y,17),(w*.4,y,17),3,'detail')


def wheels(xspan=80,yspan=60,r=18):
    for x in sorted(set((-xspan,xspan))):
        for y in (-yspan,yspan):
            cyl('wheel',(x,y,r),r,10,'structure',(0,1 if y>0 else -1,0))
            ring('wheel hub',(x,y+(11 if y>0 else -11),r),r*.56,2,2,(0,1,0),'detail')
            rod('suspension',(x*.75,y*.75,r+13),(x,y,r),3,'detail')


def gripper(p,width=30,axis=(0,0,1)):
    b=len(g.parts);w=len(g.wires)
    box('gripper bridge',(0,0,0),(width+12,16,10),3)
    for side in (-1,1):
        rod('parallel jaw link',(side*width/2,0,3),(side*width/2,0,27),2,'detail')
        box('compliant jaw',(side*(width/2-3),0,27),(8,17,18),3,'detail')
        cyl('jaw pin',(side*width/2,-10,12),2,20,'detail',(0,1,0),16)
    cyl('wrist coupling',(0,0,-13),10,10,'detail')
    transform(b,w,Matrix.Translation(p)@Vector(axis).to_track_quat('Z','Y').to_matrix().to_4x4())


def leaf(name,root,tip,width,role='structure'):
    root,tip=Vector(root),Vector(tip);d=tip-root;u=d.cross(Vector((0,0,1)))
    if u.length<.1:u=Vector((1,0,0))
    u.normalize();vs=[];fs=[]
    for j in range(17):
        t=j/16;p=root+d*t+Vector((0,0,math.sin(math.pi*t)*width*.22));half=math.sin(math.pi*t)**.7*width/2
        for k in (-1,0,1):vs.append(p+u*half*k+Vector((0,0,-abs(k)*half*.10)))
    for j in range(16):
        for k in range(2):i=3*j+k;fs.append((i,i+1,i+4,i+3))
    g.mesh(name,vs,fs,role);g.wire(name+' spine',[vs[j*3+1]+Vector((0,0,.25)) for j in range(17)],.15,'detail')
    for j in range(2,15,2):
        for side in (-1,1):g.wire(name+' vein',[vs[j*3+1]+Vector((0,0,.3)),vs[(j+1)*3+(2 if side>0 else 0)]+Vector((0,0,.3))],.09,'shell')


def views(**angles):
    VIEW_ANGLES.update(angles)


def save(entry,az=25,el=25):
    assert len(g.parts)>20,(entry['slug'],'insufficient authored geometry')
    assert len(NOTES)>=4,(entry['slug'],'missing explanatory anchors')
    name=entry['slug'];allparts=g.parts[:];allwires=g.wires[:];allanchors=g.anchors.copy()
    export(name+'-A',az,el)
    meta={'slug':name,'notes':NOTES.copy(),'parts':len(allparts),'groups':{},'views':{}}
    for key,a,e in [('B',az-38,min(68,el+20)),('C',az+8,min(62,el+16))]:
        selected=GROUPS.get(key)
        assert selected and len(selected['parts'])>=5,(name,key,'missing detailed subassembly')
        g.parts=selected['parts'];g.wires=selected['wires'];g.anchors={}
        a,e=VIEW_ANGLES.get(key,(a,e))
        export(name+'-'+key,a,e);meta['groups'][key]={'parts':len(g.parts),'objects':[o.name for o,r in g.parts],'removed_covers':selected.get('removed_covers',[]),'camera':[a,e]}
    g.parts=allparts;g.wires=allwires;g.anchors=allanchors
    for key in 'ABC':
        path=g.OUT/(name+'-'+key+'.json');d=json.loads(path.read_text());pts=[p for item in d['paths'] for p in item['points']]
        assert pts and all(math.isfinite(x) for p in pts for x in p)
        meta['views'][key]={'paths':len(d['paths']),'file':str(path.relative_to(ROOT))}
    (g.OUT/(name+'-meta.json')).write_text(json.dumps(meta,indent=2)+'\n')
    return meta
