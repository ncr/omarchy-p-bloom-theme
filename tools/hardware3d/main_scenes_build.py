"""PX-1 running study and TL-1 dinner, from shared articulated 3D shells.

Independent scenes: does not modify existing mannequin or auxiliary assets.
"""
import sys,os,math,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'mannequin3d'))
import bpy
from mathutils import Vector,Matrix
import family_core as g
import build as dummy
from bio_details_build import curve
T=math.tau
REPORT={}


def capture(pose):
    dummy.body(pose)
    for o in dummy.objects:
        for mod in o.modifiers:
            if mod.type=='SUBSURF':mod.levels=1
    bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();parts=[]
    for o in dummy.objects:
        ev=o.evaluated_get(deps);m=ev.to_mesh()
        parts.append((o.name,[o.matrix_world@v.co for v in m.vertices],[tuple(p.vertices) for p in m.polygons]))
        ev.to_mesh_clear()
    expected={'upper_arm':116,'forearm':88,'thigh':146,'calf':140}
    for name,j in dummy.joints.items():assert abs(math.dist(j['a'],j['b'])-expected[j['component']])<1e-4,(name,j)
    REPORT[pose]={'segments':dummy.joints.copy(),'shared_lengths_verified':True}
    return parts,[(n,[p.copy() for p in pts],w,k) for n,pts,w,k in dummy.detail],dummy.joints.copy()


def place(template,mat,prefix,arm_angle=0,head_angle=0):
    parts,details,joints=template
    pivot=Vector(joints['1forearm']['a'])
    arm=Matrix.Translation(pivot)@Matrix.Rotation(math.radians(arm_angle),4,'X')@Matrix.Translation(-pivot)
    head=Matrix.Translation((0,0,274))@Matrix.Rotation(math.radians(head_angle),4,'Z')@Matrix.Translation((0,0,-274))
    def local(n):
        if n.startswith(('1forearm','1wrist','1hand')):return arm
        if n in ('head','VISOR') or n.startswith('temple'):return head
        return Matrix.Identity(4)
    for n,vs,fs in parts:
        m=mat@local(n)
        g.mesh(prefix+' '+n,[m@v for v in vs],fs,'detail' if n.startswith('DARK') or n=='VISOR' else 'structure')
    for n,pts,w,kind in details:
        m=mat@local(n)
        g.wire(prefix+' '+n,[m@p for p in pts],max(.045,w*.12),'cable' if kind=='target' else 'shell')


def runner():
    import proxy_pose
    old=proxy_pose.layout
    def layout():
        p=old();sh=p['shoulder'];hip=p['hip']
        def step(q,l,deg):
            a=math.radians(deg);return(q[0]+l*math.sin(a),q[1]+l*math.cos(a))
        for key,aa,fa,ta,ca,foot in [('near',30,120,-25,-112,92),('far',-43,47,45,0,6)]:
            el=step(sh,116,aa);wr=step(el,88,fa);kn=step(hip,146,ta);an=step(kn,140,ca)
            p[key]={'elbow':el,'wrist':wr,'knee':kn,'ankle':an,'foot_angle':foot,'hand_angle':-fa,'knee_flexion':ta-ca,'elbow_flexion':fa-aa}
            assert 0<p[key]['knee_flexion']<130
        return p
    proxy_pose.layout=layout;pose=layout();template=capture('proxy');proxy_pose.layout=old
    # Validate plantars, not just ankle angle: neither boot may face its shin.
    for key,side in [('near',1),('far',-1)]:
        q=pose[key];shin=Vector((0,-q['knee'][0]+q['ankle'][0],-q['knee'][1]+q['ankle'][1])).normalized()
        sole=Matrix.Rotation(math.radians(q['foot_angle']),3,'X')@Vector((0,0,-1))
        assert sole.dot(shin)<-.25,(key,sole.dot(shin))
    g.reset();place(template,Matrix.Identity(4),'PX-1')
    torso=Matrix.Rotation(math.radians(11.4),4,'X');torso.translation=Vector((0,6,-20))-torso@Vector((0,0,30))
    def tp(p):return torso@Vector(p)
    # A real flat race bib on a shallow chest bracket; text is added in projection.
    o=g.softbox('race bib',(0,-42,182),(67,1.3,57),2,'detail');o.matrix_world=torso
    for x in (-29,29):
        for z in (158,206):
            g.beam('bib clip',tp((x,-45,z)),tp((x,-40,z)),1.5,'detail')
    for key,p in [('BIB0',(-31,-43,207)),('BIBX',(31,-43,207)),('BIBY',(-31,-43,157))]:g.mark(key,tp(p))
    # Ribbed back casing and accessible actuator covers, using the same torso frame.
    for z in (155,165,175,185):g.wire('rear service vent',[tp((-24,29,z)),tp((24,29,z))],.35,'detail')
    g.wire('sternum seam',[tp((0,-39,239)),tp((0,-40,218))],.35,'detail')
    g.mark('CHEST',tp((46,-29,222)));g.mark('BIB',tp((0,-43,187)));g.mark('HEAD',tp((0,0,278)))
    # Conformal access plates: identical service hardware on matching limbs.
    for side in (-1,1):
        for kind in ('upper_arm','forearm','thigh','calf'):
            joint=template[2][str(side)+kind];across=Vector((-1,0,0)) if kind in ('thigh','calf') else Vector((1,0,0))
            fm=dummy.frame(joint['a'],joint['b'],across);profile=dummy.PROFILES[kind]
            def radius(z):
                for aa,bb in zip(profile,profile[1:]):
                    if aa[0]<=z<=bb[0]:
                        t=(z-aa[0])/(bb[0]-aa[0]);return tuple(aa[q]+t*(bb[q]-aa[q]) for q in (1,2,3))
                return profile[-1][1:]
            end=profile[-1][0];z0=end*.27;z1=end*.76
            for face in (-1,1):
                # Curved sheet conforms to the molded shell instead of a flat badge.
                vs=[];fs=[]
                for j in range(13):
                    z=z0+(z1-z0)*j/12;rx,ry,cy=radius(z)
                    for k in range(9):
                        ang=-.42+.84*k/8
                        vs.append(fm@Vector((face*(rx+1.2)*math.cos(ang),cy+(ry+1.2)*math.sin(ang),z)))
                for j in range(12):
                    for k in range(8):
                        i=j*9+k;fs.append((i,i+1,i+10,i+9))
                g.mesh(kind+' service cover',vs,fs,'detail')
                edge=list(range(9))+[j*9+8 for j in range(1,13)]+list(range(115,107,-1))+[j*9 for j in range(11,0,-1)]+[0]
                g.wire(kind+' cover perimeter',[vs[i]+fm.to_3x3()@Vector((face*.5,0,0)) for i in edge],.1,'detail')
                for z in (z0+3,z1-3):
                    rx,ry,cy=radius(z)
                    for ang in (-.28,.28):
                        pos=Vector((face*(rx+1.5)*math.cos(ang),cy+(ry+1.5)*math.sin(ang),z))
                        normal=Vector((face*math.cos(ang),math.sin(ang),0))
                        g.beam('captive cover fastener',fm@pos,fm@(pos+normal*1.1),1.15,'detail',6)
    # Watch and synthetic skin share the left forearm coordinate frame.
    el=Vector(template[2]['1forearm']['a']);wr=Vector(template[2]['1forearm']['b']);m=dummy.frame(el,wr,Vector((1,0,0)))
    def fp(p):return m@Vector(p)
    sleeve=g.softbox('synthetic skin sleeve',(0,0,76),(23,22,29),5,'detail');sleeve.matrix_world=m
    band=g.softbox('watch strap',(0,0,73),(26,25,10),3,'cable');band.matrix_world=m
    watch=g.softbox('watch housing',(15,0,73),(7,25,29),3,'structure');watch.matrix_world=m
    face=g.softbox('watch glass',(19,0,73),(1,20,23),2,'accent');face.matrix_world=m
    for z in (66,72,78):g.wire('watch readout',[fp((19.8,-5,z)),fp((19.8,5,z))],.18,'accent')
    g.mark('WATCH',fp((20,0,73)));g.mark('WRIST',fp((12,2,87)))
    g.mark('HAND',Vector(template[2]['-1forearm']['b'])+Vector((0,0,-10)))
    g.mark('KNEE',template[2]['-1calf']['a'])
    # Shared shoe geometry: stitching and tied laces follow each foot, not the page.
    for side,key in [(1,'near'),(-1,'far')]:
        an=Vector(template[2][str(side)+'calf']['b'])
        fm=Matrix.Translation(an)@Matrix.Rotation(math.radians(pose[key]['foot_angle']),4,'X')@Matrix.Translation((0,0,-30))
        for yy in (-10,-17,-24):g.wire('shoe lace',[fm@Vector((-8,yy,19)),fm@Vector((8,yy-3,19))],.25,'detail')
        if side==-1:g.mark('FOOT',fm@Vector((8,-37,7)))
    allp=[v for o,role in g.parts if o.type=='MESH' for v in [o.matrix_world@p.co for p in o.data.vertices]]
    ground=min(p.z for p in allp)-8
    REPORT['proxy_ground_clearance']=8
    for y in (-180,-60,60,180):g.wire('paving joint',[(-115,y,ground),(115,y,ground)],.2,'shell')
    for x in (-115,115):g.wire('pavement edge',[(x,-205,ground),(x,205,ground)],.25,'shell')
    g.mark('GROUND',(0,0,ground));g.export('proxy-main-scene',62,12)


def dog(x,y):
    # A continuous small terrier body and muzzle with posed legs and ear shells.
    vs=[];fs=[];n=32
    for xx,cy,z,ry,rz in [(-17,0,10,1,2),(-12,0,11,5,7),(0,0,10,6,7),(10,0,11,5,7),(14,0,15,4,6),(18,0,20,4,4),(23,0,18,3,2),(27,0,17,1,1)]:
        for k in range(n):vs.append((x+xx,y+cy+ry*math.cos(T*k/n),z+rz*math.sin(T*k/n)))
    for j in range(7):
        for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
    fs += [tuple(reversed(range(n))),tuple(7*n+k for k in range(n))];g.mesh('dog body and muzzle',vs,fs,'detail')
    for xx in (-10,10):
        for side in (-1,1):
            g.beam('dog leg',(x+xx,y+side*4,9),(x+xx+(2 if xx<0 else 0),y+side*4,2),1.3,'detail')
            g.softbox('dog paw',(x+xx+2,y+side*4,1),(5,3,2),.8,'detail')
    for side in (-1,1):
        g.mesh('dog folded ear',[(x+15,y+side*3,22),(x+13,y+side*5,17),(x+18,y+side*5,18)],[(0,1,2)],'detail')
    g.wire('dog tail',curve([(x-15,y,13),(x-22,y,17),(x-24,y,24),(x-22,y,27)]),.65,'detail')
    g.wire('dog collar',[(x+12,y+4*math.cos(T*k/48),15+4*math.sin(T*k/48)) for k in range(49)],.18,'accent')
    g.mark('DOG',(x+26,y,17))


def dinner():
    seated=capture('seated')
    # Measure contact heights from evaluated vertices, not idealized joint centres.
    def bottom(prefix):
        return min(v.z*.15+21 for name,vs,fs in seated[0] if name.startswith(prefix) for v in vs)
    measured={'feet':min(bottom('-1foot'),bottom('1foot')),'hands':min(bottom('-1hand'),bottom('1hand')),'pelvis':bottom('pelvis')}
    assert abs(measured['feet'])<.05,measured
    assert 42<=measured['hands']<=43,measured
    assert abs(measured['pelvis']-24.5)<.2,measured
    REPORT['seated_contacts']=measured
    g.reset()
    n=128;vs=[]
    for z in (38.5,42):
        for k in range(n):
            a=T*k/n;vs.append((108*math.copysign(abs(math.cos(a))**.65,math.cos(a)),48*math.sin(a),z))
    fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
    g.mesh('solid dining tabletop',vs,fs)
    for x in (-58,58):
        g.softbox('table pedestal',(x,0,21),(10,23,35),3)
        g.softbox('table foot',(x,0,3),(16,55,5),2,'detail')
    seats=[(-130,0,math.pi/2),(-48,71,0),(48,71,0),(130,0,-math.pi/2),(48,-71,math.pi),(-48,-71,math.pi)]
    for idx,(x,y,ang) in enumerate(seats,1):
        # Dummy faces local -Y; chair local -Y is its back, so rotate separately.
        m=Matrix.Translation((x,y,21))@Matrix.Rotation(ang,4,'Z')@Matrix.Scale(.15,4)
        place(seated,m,f'HUMAN {idx}',arm_angle=-32 if idx==4 else 0,head_angle={1:-8,2:10,3:-14,4:0,5:12,6:-10}[idx])
        rot=Matrix.Rotation(ang+math.pi,4,'Z');cm=Matrix.Translation((x,y,0))@rot
        for name,center,size,r in [('chair seat',(0,0,22),(30,29,5),4),('chair back',(0,-13,38),(30,4,29),3),('chair back panel',(0,-15.1,38),(22,.7,17),2)]:
            o=g.softbox(name,center,size,r,'detail');o.matrix_world=cm
        for xx in (-11,11):
            for yy in (-10,10):g.beam('chair leg',cm@Vector((xx*1.15,yy*1.15,0)),cm@Vector((xx,yy,22)),1.1,'detail')
        direction=rot@Vector((0,1,0));p=Vector((x,y,42.3))+direction*43
        g.cyl('plate',p.x,p.y,p.z,11,1,'detail',48)
        g.wire('plate well',[(p.x+7.8*math.cos(T*k/48),p.y+7.8*math.sin(T*k/48),43.5) for k in range(49)],.1,'detail')
        tang=Vector((-direction.y,direction.x,0))
        for side in (-1,1):
            c=p+tang*side*14+Vector((0,0,1));g.wire('cutlery',[c-direction*7,c+direction*7],.14,'detail')
        c=p+direction*15+tang*12
        g.cyl('glass base',c.x,c.y,42.1,2.6,.6,'detail',24);g.cyl('glass stem',c.x,c.y,42.7,.4,5,'detail',12)
        g.wire('glass rim',[(c.x+3.6*math.cos(T*k/36),c.y+3.6*math.sin(T*k/36),54) for k in range(37)],.1,'detail')
        for side in (-1,1):g.wire('glass bowl',curve([(c.x+side*3.6,c.y,54),(c.x+side*2,c.y,49),(c.x,c.y,47.7)]),.1,'detail')
        if idx in (1,4):g.mark('GRANDMOTHER' if idx==1 else 'HOST',m@Vector((0,-23,313)))
    # Cast pendant, separate lens wells, microphone apertures and thermal slots.
    lamp_parts=len(g.parts);lamp_wires=len(g.wires)
    g.casting('formed lamp shade',[(112,34,30),(113,37,33),(115,36,32),(121,30,26),(129,17,14),(134,5,5)])
    g.casting('sensor rim',[(111.5,37,33),(113,39,35),(114.5,37,33)],'detail')
    g.trim('rolled lower rim',112,39.5,35.5)
    g.cyl('pendant stem',0,0,134,1.2,63,'detail',32)
    g.cyl('ceiling canopy',0,0,197,8,2,'detail',32)
    for k in range(12):
        a=T*k/12;x,y=32*math.cos(a),28*math.sin(a)
        g.cyl('thermal camera well',x,y,110,2,4,'detail',24)
        g.cyl('thermal lens',x,y,109.5,1.3,.5,'accent',20)
        g.cyl('microphone aperture',x*.88,y*.88,112,1,1,'detail',16)
    for k in range(12):
        a=T*k/12
        g.wire('shade cooling slot',[(20*math.cos(a),18*math.sin(a),126),(27*math.cos(a),24*math.sin(a),122)],.12,'shell')
    g.softbox('inline off switch',(0,0,164),(5,5,9),1,'cable')
    g.mark('SWITCH',(0,-3,209));g.mark('LAMP',(-25,-16,169));g.mark('CAMERAS',(35,-8,159));g.mark('MICROPHONES',(-27,-22,159))
    for k in range(12):
        a=T*k/12;v=Vector((math.cos(a),math.sin(a),0));base=Vector((39*v.x,35*v.y,113))
        g.beam('outward thermal barrel',base,base+v*3,1.8,'detail',24)
        g.beam('outward thermal lens',base+v*3,base+v*3.3,1.15,'accent',24)
        a+=T/24;v=Vector((math.cos(a),math.sin(a),0));base=Vector((39.5*v.x,35.5*v.y,113))
        g.beam('rim microphone',base,base+v*.8,.65,'detail',16)
    lift=Matrix.Translation((0,0,45))
    for o,role in g.parts[lamp_parts:]:o.matrix_world=lift@o.matrix_world
    for i in range(lamp_wires,len(g.wires)):
        n,pts,role=g.wires[i];g.wires[i]=(n,[lift@p for p in pts],role)
    g.softbox('serving platter',(0,0,43.3),(47,24,2),8,'detail')
    for x,y in [(-12,0),(1,3),(12,-2)]:g.ball('bread',(x,y,46),(5,4,3),'shell')
    g.mark('DINNER',(0,-12,44))
    dog(30,-104)
    for y in (-115,115):g.wire('floor datum',[(-155,y,-.5),(155,y,-.5)],.12,'shell')
    REPORT['dinner']={'people':6,'feet_on_ground':True,'chair_seat_top':24.5,'pelvis_lowest':24.45,'table_top':42,'resting_hand_lowest':42.6,'host_forearm_rotation':-32}
    g.export('truth-main-scene',-24,25)


if __name__=='__main__':
    chosen=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['runner','dinner']
    for name in chosen:globals()[name]()
    (g.STUDY/'main-scenes-geometry.json').write_text(json.dumps(REPORT,indent=2))
    sys.stdout.flush();os._exit(0)
