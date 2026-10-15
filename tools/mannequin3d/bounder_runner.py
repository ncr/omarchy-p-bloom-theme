"""An authored sprint pose and paired B-4 wearables on the shared dummy.

X is lateral, -Y forward, Z up. Each side uses the same limb lengths and
hardware dimensions; only rigid joint transforms differ.
"""
import math,sys
from pathlib import Path
from mathutils import Vector,Matrix


def pose_layout():
    torso=Matrix.Rotation(math.radians(12),4,'X')
    torso.translation=Vector((0,0,30))-torso@Vector((0,0,30))
    def step(origin,length,degrees):
        a=math.radians(degrees)
        return origin+Vector((0,-length*math.sin(a),-length*math.cos(a)))
    poses=[]
    for side,arm,forearm,thigh,calf in [(1,-43,47,62,12),(-1,40,130,-42,-132)]:
        sh=torso@Vector((side*78,0,239))
        el=step(sh,116,arm);wr=step(el,88,forearm)
        hip=torso@Vector((side*36,0,30))
        kn=step(hip,146,thigh);an=step(kn,140,calf)
        poses.append((side,sh,el,wr,hip,kn,an))
    return torso,poses


def foot_frame(ankle,knee,side):
    """Keep the plantar side opposite the shin, including a folded rear leg.

    An arbitrary absolute pitch can satisfy a right angle while mounting the
    whole boot upside down. Resolve that 180-degree ambiguity from the vector
    towards the knee, then add the selected plantar flexion for this phase.
    """
    proximal=Vector(knee)-Vector(ankle)
    shin_angle=math.atan2(-proximal.z,-proximal.y)
    pitch=shin_angle+math.pi/2+math.radians(17 if side==1 else 10)
    return Matrix.Translation(ankle)@Matrix.Rotation(pitch,4,'X')


def equip(dummy):
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'hardware3d'))
    import family_core as g
    g.parts=[];g.wires=[];g.anchors={}
    torso,poses=pose_layout()

    def transform_since(index,mat):
        for obj,_ in g.parts[index:]:obj.matrix_world=mat@obj.matrix_world

    # A wraparound pelvic harness and a compact vented lumbar power pack.
    i=len(g.parts)
    g.softbox('B4 belt back',(0,27,56),(101,14,25),5)
    for side in (-1,1):
        g.softbox('B4 belt flank',(side*47,0,56),(12,62,25),4)
        g.softbox('B4 pelvic brace',(side*47,0,37),(14,29,30),5)
    g.softbox('B4 front buckle',(0,-30,56),(32,11,21),4)
    g.softbox('B4 lumbar pack',(0,49,77),(77,34,65),10)
    for z in range(56,102,7):g.softbox('B4 pack cooling slot',(39,49,z),(1.5,20,2),.5)
    transform_since(i,torso)

    for side,sh,el,wr,hip,kn,an in poses:
        # The outer rail sits beyond the skin: hubs share anatomical joint axes.
        outward=Vector((side*29,0,0));h=hip+outward;k=kn+outward;a=an+outward
        for name,p,r,depth in [('hip drive',h,23,12),('knee cam',k,19,12),('ankle pivot',a,13,10)]:
            q=p+Vector((side*depth,0,0))
            g.beam('B4 '+name,p,q,r,'structure',48)
            g.beam('B4 '+name+' cap',q,q+Vector((side*2,0,0)),r*.7,'accent',40)
            for t in range(4):
                angle=math.tau*t/4
                off=Vector((0,r*.8*math.cos(angle),r*.8*math.sin(angle)))
                g.beam('B4 hub fastener',q+off,q+off+Vector((side*2.7,0,0)),1.5,'detail',8)
        for name,start,end in [('thigh',h,k),('shank',k,a)]:
            axis=(end-start).normalized();across=Vector((side,0,0));tangent=axis.cross(across).normalized()
            g.beam('B4 '+name+' load rail',start,end,4.3,'structure',12)
            for flank in (-1,1):
                offset=tangent*flank*14+across*4
                u=start.lerp(end,.20)+offset;v=start.lerp(end,.80)+offset
                g.beam('B4 muscle bundle',u,v,5.5,'structure',20)
                for n in (-1,0,1):
                    off=across*5.6+tangent*n*2
                    g.wire('B4 yarn rib',[u+off,v+off],.32,'accent')
                g.beam('B4 actuator clevis',start.lerp(end,.08),u,2.1)
                g.beam('B4 actuator clevis',v,start.lerp(end,.92),2.1)
            # Bands wrap around the actual limb, not the displaced external rail.
            bone0,bone1=(hip,kn) if name=='thigh' else (kn,an)
            centre=bone0.lerp(bone1,.36 if name=='thigh' else .57)
            radius=24 if name=='thigh' else 17
            for d in (-4,4):
                pts=[centre+axis*d+across*radius*math.cos(math.tau*j/64)+tangent*radius*math.sin(math.tau*j/64) for j in range(65)]
                g.wire('B4 neural cuff edge',pts,.7,'detail')
            g.beam('B4 cuff mount',centre+outward*.60,centre+outward,4)
        # Foot cradle and extruded C-spring use one identical local mesh per leg.
        fm=foot_frame(an,kn,side)
        i=len(g.parts)
        g.softbox('B4 boot cradle',(0,-13,-29),(42,66,7),3)
        # Profile is (forward, down), from heel clamp round the heel to the toe.
        control=[Vector(p) for p in [(0,19),(-66,40),(-45,90),(59,76)]]
        pts=[]
        for j in range(49):
            t=j/48;p=(1-t)**3*control[0]+3*(1-t)**2*t*control[1]+3*(1-t)*t*t*control[2]+t**3*control[3]
            pts.append(p)
        vs=[(x,-p.x,-p.y+off) for x in (-18,18) for off in (0,4) for p in pts]
        n=len(pts);faces=[]
        for j in range(n-1):
            faces += [(j,j+1,n+j+1,n+j),(2*n+j,3*n+j,3*n+j+1,2*n+j+1),(j,2*n+j,2*n+j+1,j+1),(n+j,n+j+1,3*n+j+1,3*n+j)]
        faces += [(0,n,3*n,2*n),(n-1,3*n-1,4*n-1,2*n-1)]
        g.mesh('B4 carbon return blade',vs,faces)
        g.softbox('B4 replaceable sole',(0,-43,-77),(39,43,6),2)
        for u in range(26,63,6):g.softbox('B4 sole tread',(0,-u,-80),(37,2,2),.5)
        transform_since(i,fm)
        # Regression guard: the blade belongs on the plantar side, away from
        # the shin. A 180-degree reversed mounting passed limb-length checks.
        shin=(kn-an).normalized()
        boot=next(o for o in dummy.objects if o.name==f'{side}foot')
        boot_normal=(boot.matrix_world.to_3x3()@Vector((0,0,-1))).normalized()
        for obj,_ in g.parts[i:]:
            normal=(obj.matrix_world.to_3x3()@Vector((0,0,-1))).normalized()
            assert normal.dot(shin)<-.75, f'Inverted B4 sole on side {side}: {obj.name}'
            assert (normal-boot_normal).length<1e-5, f'Boot/blade frame mismatch on side {side}'

    dummy.objects.extend(obj for obj,role in g.parts)
    dummy.detail.extend((name,points,.55,'seam') for name,points,role in g.wires)
