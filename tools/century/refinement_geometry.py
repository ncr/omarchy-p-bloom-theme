"""Purpose-built service details for the first ten editorial revisions.

Added in the original coordinate frames; B/C and A share the same objects.
No changes to the authored human rig or to the other ninety machines.
"""
from .kit import *


def loom(points):
    for d in (-.65,.65):tube('paired service loom',[(x+d,y,z) for x,y,z in points],.28,'detail')


def light_sail():
    views(C=(-45,38))
    with group('B'):
        for a in range(0,360,90):
            with at(angle=a):
                box('tension encoder',(23,-8,18),(8,6,5),1,'detail')
                loom([(23,-8,20),(18,-8,24),(0,-8,24),(0,0,14)])
                ring('reel thrust washer',(12,12,12),7,1,1,role='accent')
        cyl('hub harness manifold',(0,0,14),7,12,'detail');bolts((0,0,27),4,4,size=.55)
    with group('C'):
        for y in (-12,12):
            ring('roller dust seal',(49,y,8),5.4,.7,1,(0,1,0),'accent')
            ring('pin safety keeper',(37,y*1.3,8),2.8,.6,1,(0,1,0),'detail')
        loom([(36,-19,1),(32,-22,1),(26,-21,7),(22,-15,14)])


def sock_oracle():
    with group('B'):
        # Perforated drum end, lint screen and service flange.
        for a in range(0,360,15):
            q=math.radians(a);cyl('drum ventilation eye',(38*math.cos(q),-1,77+38*math.sin(q)),1.5,1,'detail',(0,-1,0),16)
        for x in (-18,18):rod('drum front spoke',(x*.25,-2,77),(x,-2,77+side_height(x)),1,'detail')
        box('optical encoder tab',(33,40,107),(10,9,5),1,'detail')
    with group('C'):
        for x in (-23,23):
            for dx in (-12,12):
                box('pocket guide rail',(x+dx,-25,28),(2,34,3),.5,'detail')
            for y in (-34,-26,-18):rod('anti-snag roller',(x-10,y,29),(x+10,y,29),1,'detail')
            loom([(x,6,39),(x,14,42),(0,14,42),(0,8,45)])
    uncover('C','pairing gate')


def side_height(x):return 28 if x>0 else -28


def advice_filter():
    with group('B'):
        for x in range(-24,25,8):
            h=math.sqrt(29**2-x*x)
            rod('blade crank',(x,9,69),(x+3,9,72),.6,'detail')
            ring('pivot felt washer',(x,-5.8,69+h),2,.5,.6,(0,-1,0),'detail')
        loom([(33,6,74),(36,14,75),(18,17,73),(12,17,62)])
    with group('C'):
        for x in (-8,8):
            rod('switch spring guide',(x,-34,8),(x,-34,16),.7,'detail')
            for z in (9,11,13):ring('switch return spring',(x,-34,z),1.9,.4,.7,role='detail')
    for x in (-22,-11,0,11,22):box('processor ventilation',(x,43,23),(5,1.5,12),.5,'detail')


def petal_eye():
    with group('B'):
        for a in range(0,360,30):
            with at(angle=a):
                rod('radial backplane rib',(13,0,-1),(61,0,-1),1.2,'detail')
                box('edge metrology head',(66,0,10),(5,9,5),1,'detail')
                bolts((62,0,9),2,3,size=.4)
    with group('C'):
        for a in (30,150,270):
            with at(angle=a):
                cyl('focus actuator',(11,0,86),2,9,'detail')
                loom([(11,0,91),(15,0,84),(41,0,43),(58,0,12)])
        for z in (100,102,104):ring('stray light knife edge',(0,0,z),13,1,1,role='detail')
    for x in (-1,1):
        tube('cryogenic supply',[(x*28,0,-49),(x*38,0,-49),(x*43,0,-66),(x*65,0,-66)],1,'accent')


def coral_cradle():
    with group('B'):
        for side in (-1,1):
            box('contact force sensor',(-67+side*10,-10,62),(4,2,10),.7,'detail')
            loom([(-67+side*10,-11,65),(-67+side*10,-9,77),(-67,-7,91)])
        ring('wrist splash collar',(-67,0,92),8,1.5,2,role='detail')
    with group('C'):
        for x,y in ((14,-13),(43,-12),(29,15)):
            ring('removable socket collar',(x,y,18),7,1,2,role='accent')
            box('fragment identity tab',(x,y-8,16),(8,3,1),.4,'detail')
        for y in (-19,-9,1,11,21):
            for x in (5,59):cyl('flow perforation',(x,y,13),1.2,.8,'detail',n=12)
    for side in (-1,1):
        for a in range(0,360,45):
            q=math.radians(a);rod('fan intake guard',(side*70+4*math.cos(q),17,31+4*math.sin(q)),(side*70+11*math.cos(q),17,31+11*math.sin(q)),.5,'detail')
    for x in (-60,-40,-20,0,20,40,60):box('deck drainage slit',(x,-30,5.5),(11,2,1),.3,'detail')


def dune_skimmer():
    for x in (-56,56):
        for y in (-37,37):
            # All four wheels receive the same tread and telescoping sleeve.
            key='B' if (x,y)==(-56,-37) else 'wheels'
            with group(key):
                side=1 if y>0 else -1
                for a in range(0,360,20):
                    q=math.radians(a)
                    rod('sand grouser',(x+24.4*math.cos(q),y+side*2,24+24.4*math.sin(q)),(x+24.4*math.cos(q),y+side*26,24+24.4*math.sin(q)),.8,'detail')
                ring('hub dust seal',(x,y+side*34,24),9,1,1,(0,side,0),'accent')
    with group('C'):
        for y in (-23,23):
            loom([(38,y,81),(42,y,93),(46,y,117),(44,y,130)])
            for t in (.4,.5,.6):
                q=Vector((30,y,83)).lerp(Vector((42,y,121)),t)
                ring('piston bellows',q,2.4,.4,1,(12,0,38),'detail')
    for y in (-25,25):
        tube('cargo tie rail',[(25,y,103),(25,y,111),(61,y,111),(61,y,103)],1,'detail')
    for z in (87,92,97):box('cargo cooling louvre',(50,-24.5,z),(22,1.4,1.7),.4,'detail')


def meeting_buoy():
    with group('B'):
        for z in range(51,146,8):ring('mast index band',(0,0,z),3.5,.5,.7,role='detail')
        for z in (48,146):box('travel limit switch',(-5,1,z),(4,5,7),1,'detail')
        loom([(-5,0,49),(-7,3,46),(-7,3,24),(0,3,21)])
        for z in (124,137):ring('flag eyelet',(6,-1,z),1.2,.4,1,(0,1,0),'detail')
    with group('C'):
        for a in range(0,360,45):
            with at(angle=a):
                box('preamplifier capsule',(21,0,22),(7,5,4),1,'detail')
                loom([(24,0,31),(21,0,29),(21,0,24)])
        ring('shielded signal bus',(0,0,22),17,1,1,role='accent')


def neutrino_bell():
    views(B=(-135,30))
    with group('B'):
        for x in (-8,0,8):
            box('readout front-end IC',(x,-17,73),(5,9,1.5),.4,'detail')
            for dx in (-3,3):
                for y in (-20,-17,-14):rod('IC lead',(x+dx,y,72),(x+dx*1.2,y,72),.18,'detail')
        for x in (-9,9):cyl('board standoff',(x,-20,64),1.3,6,'detail')
    with group('C'):
        for a in range(0,360,60):
            with at(angle=a):
                ring('emitter gasket',(13,0,127),3.8,.6,1,(1,0,0),'detail')
        for z in (143,146,149):ring('cable strain relief',(0,0,z),3,1,1,role='detail')
    for z in (84,96):
        for a in range(0,360,45):
            q=math.radians(a);box('digitizer package',(15*math.cos(q),15*math.sin(q),z+1),(6,4,2),.5,'detail')
    for a in range(0,360,60):
        q=math.radians(a);rod('board support column',(22*math.cos(q),22*math.sin(q),78),(22*math.cos(q),22*math.sin(q),99),.9,'detail')


def sleep_cocoon():
    with group('C'):
        for side in (-1,1):
            for y,z in ((8,9),(-21,25),(11,19),(-18,35)):
                ring('link bearing washer',(side*17+3,y,z),2.5,.6,.6,(1,0,0),'accent')
            loom([(side*17,8,3),(side*20,8,10),(side*20,-10,24),(side*17,-18,34)])
            box('recline stop block',(side*17,6,5),(7,8,4),1,'detail')
    # Rig is untouched. Only ground frame accessories, safely clear of the body.
    for x in (-23,23):
        for y in (-24,24):cyl('floor isolator',(x,y,-10),4,2,'detail')
    box('service pack',(0,22,8),(25,16,13),3,'detail')
    for x in (-8,-4,0,4,8):box('pack ventilation',(x,30.2,9),(1.5,1,7),.3,'detail')


def plant_alibi():
    with group('B'):
        for z in range(22,66,5):ring('probe scale tick',(-14,0,z),3.3,.4,.5,role='detail')
        loom([(-14,0,81),(-14,8,85),(-23,10,70),(-23,7,48)])
    with group('C'):
        for a in range(0,360,60):
            with at((46,0,0),a):
                rod('meter tie rod',(10,0,31),(10,0,52),.7,'detail')
                cyl('meter tie nut',(10,0,52),1.4,1,'detail',n=6)
        ring('meter sight rim',(46,-15,43),4.6,.5,1,(0,-1,0),'detail')
    for x in (-11,11):
        for z in (24,38):cyl('recorder security screw',(x,-37, z),.9,1,'detail',(0,-1,0),6)
    tube('probe harness',[(-23,7,48),(-27,-12,42),(-18,-31,31),(-13,-34,31)],.5,'detail')


SELECTED={1:light_sail,10:sock_oracle,30:advice_filter,31:petal_eye,44:coral_cradle,
          56:dune_skimmer,60:meeting_buoy,87:neutrino_bell,99:sleep_cocoon,100:plant_alibi}


def enrich(entry):
    if entry['number'] in SELECTED:SELECTED[entry['number']]()
