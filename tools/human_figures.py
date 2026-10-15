"""Continuous human-factors envelopes for the wearable equipment plates."""
import math
from fidelity import contour, front_head, optical_target, bolt
from sheet import WHITE, ARC, GOLD
from hardware3d.accessories import rounded


def absent_head(s,x,y):
    """Dashed head envelope and a cancellation stroke above a capped mount."""
    s.c.save();s.c.translate(x,y)
    c=s.c
    c.move_to(0,23)
    c.curve_to(-15,23,-23,9,-23,-8)
    c.curve_to(-23,-26,-14,-34,0,-34)
    c.curve_to(14,-34,23,-26,23,-8)
    c.curve_to(23,9,15,23,0,23)
    s._stroke(.64,.75,[4,3],WHITE)
    s.ln(-28,27,28,-38,.85,.9)
    # Symbol only. The physical neck is part of proxy_body's connected shell.
    s.c.restore()


def muscle_sleeve(s,p1,p2,r1,r2):
    """A longitudinal textile actuator with curved retaining cuffs."""
    dx,dy=p2[0]-p1[0],p2[1]-p1[1]
    length=math.hypot(dx,dy)
    s.c.save();s.c.translate(*p1);s.c.rotate(math.atan2(dy,dx)-math.pi/2)
    for k in range(5):
        x=(k-2)*2.5
        s.bez((x,length*.24),(x+2,length*.40),(x+1,length*.60),(x,length*.76),.43,.42,color=ARC)
    for t in (.22,.77):
        y=length*t;r=(r1*(1-t)+r2*t)*.93
        contour(s,[("M",-r,y),("C",-r*.4,y+4,r*.4,y+4,r,y),
            ("L",r,y+5),("C",r*.4,y+9,-r*.4,y+9,-r,y+5)],
            a=.65,w=.6,fill=.025,close=True,color=ARC)
        s.rect(r-4,y+1,5,4,.68,.4,fill=.09,color=ARC)
    s.c.restore()


def dummy_joint(s,p,r=12,target=False,a=.8):
    """Recessed load-cell cover and exposed steel pin, without gear ornament."""
    x,y=p
    s.circ(x,y,r,a,.7,fill=.025)
    s.arc(x,y,r-3,25,155,a*.55,.5)
    s.arc(x,y,r-3,205,335,a*.55,.5)
    if target:optical_target(s,x,y,r*.52)
    else:
        s.circ(x,y,r*.35,a*.8,.5)
        s.ln(x-r*.2,y,x+r*.2,y,a*.8,.4)


def dummy_segment(s,p1,p2,r1,r2,j1,j2,a=.8):
    """Moulded limb with recessed end sockets and a removable side cover."""
    dx,dy=p2[0]-p1[0],p2[1]-p1[1];length=math.hypot(dx,dy)
    s.c.save();s.c.translate(*p1);s.c.rotate(math.atan2(dy,dx)-math.pi/2)
    start,end=j1*.8,length-j2*.8
    # The narrow central member bridges each shell to the joint centre.
    s.rect(-4,0,8,length,a*.48,.45,fill=.008)
    contour(s,[("M",-r1*.77,start),
        ("C",-r1*1.07,start+16,-r1*1.05,length*.33,-r2*1.1,end-19),
        ("C",-r2*1.03,end-9,-r2,end-3,-r2*.8,end),
        ("C",-r2*.4,end+2,r2*.4,end+2,r2*.8,end),
        ("C",r2,end-3,r2*1.03,end-9,r2*1.1,end-19),
        ("C",r1*.98,length*.33,r1*1.02,start+16,r1*.77,start),
        ("C",r1*.4,start-2,-r1*.4,start-2,-r1*.77,start)],
        a=a,w=.8,fill=.02,close=True)
    s.bez((-r1*.72,start+6),(-r1*.3,start+9),(r1*.3,start+9),(r1*.72,start+6),a*.6,.5)
    s.bez((-r2*.74,end-5),(-r2*.3,end-2),(r2*.3,end-2),(r2*.74,end-5),a*.6,.5)
    s.bez((r1*.5,start+14),(r1*.7,length*.34),(r2*.53,end-23),(r2*.45,end-13),a*.43,.45)
    for x,y in ((r1*.5,start+15),(r2*.45,end-13)):bolt(s,x,y,1.45,a*.66)
    s.c.restore()


def dummy_foot(s,p,side=1,angle=0,a=.78):
    """One rigid 72 x 29 shoe; only rotation/reflection may differ by side."""
    x,y=p;s.c.save();s.c.translate(x,y);s.c.scale(side,1)
    s.c.rotate(math.radians(angle))
    contour(s,[("M",-10,-1),("L",10,-1),
        ("C",13,8,20,15,37,18),("C",49,20,58,21,58,25),
        ("L",58,28),("L",-12,28),("C",-14,26,-14,17,-12,11),("L",-10,-1)],
        a=a,w=.8,fill=.025,close=True)
    s.ln(-11,24,57,24,a*.6,.5)
    s.bez((1,9),(12,11),(23,17),(35,18),a*.45,.45)
    for x in (12,18,24):s.ln(x,15,x+2,19,a*.5,.45)
    dummy_joint(s,(0,0),8,False,a)
    s.c.restore()


def dummy_hand(s,p,angle=0,side=1,a=.78):
    """Rigid moulded hand envelope, grouped fingers and an integral thumb.

    The origin is the wrist pivot. Every instance shares this unscaled path;
    a mirrored casting or a different wrist angle does not alter its size.
    """
    s.c.save();s.c.translate(*p);s.c.rotate(math.radians(angle));s.c.scale(side,1)
    # A short metal spigot overlaps the wrist pivot and the moulded cuff.
    s.rect(-5,-2,10,12,a*.65,.5,fill=.025)
    contour(s,[("M",-7,7),("L",7,7),
        ("C",8,12,11,15,11,22),("L",10,33),
        ("C",10,37,7,39,3,39),("L",-3,38),
        ("C",-7,38,-9,35,-9,31),("L",-9,26),
        ("C",-13,28,-17,26,-16,22),
        ("C",-15,17,-10,14,-9,11),("L",-7,7)],
        a=a,w=.75,fill=.022,close=True)
    s.bez((-8,12),(-3,14),(3,14),(8,12),a*.55,.5)
    # One mould seam, without individual digits or anatomical palm creases.
    s.bez((7,19),(8,26),(7,33),(3,35),a*.35,.4)
    s.c.restore()


def dummy_foot_front(s,p,side=1,a=.78):
    """Front elevation of the shoe, with slight outward toe splay.

    The sole is 26 units below the ankle, at the roller crowns in Presence
    Rig. Both sides use the same casting, reflected across the body axis.
    """
    s.c.save();s.c.translate(*p);s.c.scale(side,1)
    contour(s,[("M",-9,-1),("L",9,-1),
        ("C",10,7,13,11,17,17),("L",20,21),
        ("C",22,24,20,26,17,26),("L",-14,26),
        ("C",-18,26,-19,23,-17,20),("L",-13,12),
        ("C",-11,8,-10,4,-9,-1)],a=a,w=.8,fill=.025,close=True)
    s.bez((-16,22),(-7,24),(9,24),(19,22),a*.6,.5)
    s.bez((-10,12),(-4,15),(6,15),(12,12),a*.45,.45)
    for y in (8,11):s.ln(-4,y,6,y,a*.5,.45)
    dummy_joint(s,(0,0),8,False,a)
    s.c.restore()


def paired_joint(root,tip,length1,length2,hint):
    """Two rigid links; choose the joint solution nearest the authored pose."""
    dx,dy=tip[0]-root[0],tip[1]-root[1];d=math.hypot(dx,dy)
    assert abs(length1-length2)<=d<=length1+length2
    along=(length1**2-length2**2+d*d)/(2*d)
    height=math.sqrt(max(0,length1**2-along**2))
    center=(root[0]+dx*along/d,root[1]+dy*along/d)
    candidates=[(center[0]-sign*dy*height/d,center[1]+sign*dx*height/d) for sign in (-1,1)]
    return min(candidates,key=lambda p:math.dist(p,hint))


# One component definition per type, used by BOTH sides of the running dummy.
# length, proximal radius, distal radius, proximal joint, distal joint
PROXY_PARTS={'upper_arm':(116,21,14,16,11),'forearm':(88,16,10,11,8),
             'thigh':(146,31,22,18,15),'calf':(140,23,12,15,8)}


def proxy_pose():
    from mannequin3d.proxy_pose import layout
    return layout()


def presence_body(s,mx,my):
    """One orthographic projection of the shared 3D test-dummy castings."""
    from projected_dummy import draw, geometry
    draw(s,'presence',mx,my)
    data=geometry('presence');scale=data['scale'];dy=data['dy']
    # The wearable apparatus remains authored vector geometry, on top of the dummy.
    s.c.save();s.c.translate(mx,my+dy);s.c.scale(scale,scale)
    contour(s,[("M",-31,-316),("C",-17,-321,17,-321,31,-316),
        ("L",29,-300),("C",17,-296,-17,-296,-29,-300)],
        a=.86,w=.8,fill=0,close=True,color=ARC)
    for sign in (-1,1):
        s.rect(sign*34-3,-302,6,14,.75,.55,fill=.2,color=GOLD)
        s.bez((sign*36,-288),(sign*34,-274),(sign*34,-263),(sign*45,-253),.4,.5)
    contour(s,[("M",-21,-214),("L",21,-214),("L",24,-208),("L",24,-164),
        ("L",18,-158),("L",-18,-158),("L",-24,-164),("L",-24,-208)],
        a=.72,w=.65,fill=.028,close=True)
    rounded(s,-15,-203,30,29,6,.72,.55,color=ARC)
    for x in (-9,0,9):s.circ(x,-166,1.4,.7,.4,color=GOLD)
    for sign in (-1,1):
        for kind,r1,r2 in [('upper_arm',21,14),('forearm',16,10),('thigh',23,14),('calf',15,8)]:
            j=data['joints'][str(sign)+kind]
            a,b=j['a'],j['b']
            muscle_sleeve(s,(a[0],-a[2]),(b[0],-b[2]),r1,r2)
    s.c.restore()


def proxy_body(s,mx,my):
    """Running pose of the same 3D castings; head intentionally absent."""
    from projected_dummy import draw
    from leisure import cuff
    draw(s,'proxy',mx,my)
    pose=proxy_pose();e,w=pose['near']['elbow'],pose['near']['wrist']
    s.c.save();s.c.translate(mx,my)
    cuff(s,e,w,.52,.98,14,fill=.10,color=ARC)
    # Cast watch case aligned with the already approved wrist orientation.
    angle=math.atan2(w[1]-e[1],w[0]-e[0])
    s.c.save();s.c.translate(e[0]+(w[0]-e[0])*.78,e[1]+(w[1]-e[1])*.78);s.c.rotate(angle)
    rounded(s,-10,-18,20,36,6,.92,.7,.035,GOLD)
    rounded(s,-6,-12,12,24,4,.8,.5,color=ARC)
    s.circ(12,0,2.4,.8,.5,color=GOLD);s.c.restore()
    for r in (20,28,36):s.arc(pose['far']['wrist'][0]-9,pose['far']['wrist'][1]+8,r,140,220,.4,.5)
    s.c.restore()
