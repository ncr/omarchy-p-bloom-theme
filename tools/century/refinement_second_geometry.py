"""Second curated ten: serviceable mechanisms, not generic surface greebles."""
from .kit import *
from . import kit


def tidal_loom():
    # Matched cartridge hardware on both turbines; visible water-side wear parts.
    for x,key in ((-71,'B'),(71,'C')):
        with group(key):
            for y in (-18,14):
                ring('replaceable shroud lip',(x,y,61),44.5,1.5,2,(0,1,0),'detail')
                bolts((x,y-1,61),42.5,12,(0,-1,0),.7)
            for a in (45,135,225,315):
                q=math.radians(a)
                box('sacrificial anode',(x+43*math.cos(q),-1,61+43*math.sin(q)),(4,14,4),.8,'detail')
            ring('shaft labyrinth',(x,35,61),12,2,4,(0,1,0),'detail')
            tube('bearing sensor lead',[(x,39,65),(x,36,88),(x,31,109),(0,30,115)],.35,'detail')
            for z in (47,54,68,75):rod('generator cooling rib',(x-7,33,z),(x+7,33,z),.5,'detail')
    for x in (-10,10):
        cyl('junction gland',(x,13,109),3,5,'detail',(0,-1,0))
        tube('gland cable',[(x,8,109),(x,1,100),(x*4,24,105),(x*7.1,30,109)],.55,'cable')


def manta_foil():
    with group('B'):
        for y in (-12,12):
            flange('hinge keeper',(-53,y,20),9,(0,1 if y>0 else -1,0),2)
            rod('hinge clevis cheek',(-63,y,16),(-51,y,-2),1.6,'detail')
        for y in (-48,-24,24,48):
            tube('foil inspection seam',[(-61,y,-35),(-48,y,-33),(-36,y,-34)],.25,'detail')
        tube('strut instrumentation',[(-56,-4,27),(-57,-4,-27),(-44,-4,-34)],.25,'detail')
    with group('C'):
        for y in (-15,15):
            ring('duct replaceable lip',(80,y,8),20.5,1,2,(0,1,0),'detail')
            bolts((80,y-1,8),19,10,(0,-1,0),.55)
        for a in (30,150,270):
            with at((80,0,8),a,'Y'):
                rod('nozzle service tie',(17,-10,0),(17,14,0),.7,'detail')
    for side in (-1,1):
        sections=[(-70.4,2,3,0),(-49.92,20.16,13.65,0),(-12.8,24,19.5,2),(44.8,20.16,17.16,0),(61.44,5,6,-4)]
        for x in (-29.44,0,28.8):
            rx,rz,lift=profile_at(sections,x);pts=[]
            for i in range(21):
                t=.13+.54*i/20;yy=rx*max(.001,1-abs(t)**(2/.7))**(.7/2)
                pts.append((x,side*(yy+.50),68+lift+rz*t))
            g.wire('conformal window mullion',pts,.18,'detail')
        tube('deck rail',[(-84,side*25,59),(-62,side*28,60),(59,side*28,60),(74,side*25,59)],.65,'detail')
        for x in (-56,56):
            box('mooring cleat',(x,side*27,51),(8,3,3),.6,'detail')
    for x in (-88,85):
        box('deck service hatch',(x,0,54),(21,23,2),3,'detail')
        for y in (-8,8):cyl('hatch latch',(x,y,55),.8,1,'detail',n=6)


def memory_kiln():
    with group('B'):
        for z in range(89,143,5):
            # Mechanical graduations on focus screws, not floating data marks.
            for x in (-19,19):ring('focus scale',(x,9,z),1.8,.25,.5,role='detail')
        for z in (101,112):
            for a in range(0,360,30):
                q=math.radians(a);rod('focus knurl',(20*math.cos(q),20*math.sin(q),z),(20*math.cos(q),20*math.sin(q),z+3),.32,'detail')
        rod('encoder strip',(25,9,87),(25,9,146),.8,'detail')
        box('encoder readhead',(25,9,122),(5,7,9),1,'detail')
    with group('C'):
        for a in range(0,360,60):
            q=math.radians(a);x,y=31*math.cos(q),31*math.sin(q)
            # Alignment marks on the six actual plates.
            for dx in (-7,7):
                rod('plate fiducial',(x+dx-1,y-7,41.1),(x+dx+1,y-7,41.1),.18,'detail')
                rod('plate fiducial',(x+dx,y-8,41.1),(x+dx,y-6,41.1),.18,'detail')
            cyl('detent pocket',(45*math.cos(q),45*math.sin(q),39.2),1.1,.5,'detail',n=16)
        box('carousel index sensor',(48,0,42),(7,9,7),1,'detail')
        tube('index sensor lead',[(49,3,42),(56,8,32),(54,31,22)],.35,'detail')
    for x in (-54,54):
        for z in (22,142):ring('bridge column clamp',(x,31,z),5.5,1.5,5,role='detail')
    for x in (-64,-59,-54,-49):rod('source heat fin',(x,-15,83),(x,-15,111),.5,'detail')
    rod('guide drawer handle',(45,-44,27),(60,-44,27),.7,'detail')


def lunar_porch():
    with group('B'):
        for x in (-31,31):
            for z in (63,105):
                cyl('latch axle',(x,-30,z),2,4,'detail',(0,-1,0))
                rod('overcentre latch lever',(x,-31,z),(x*.73,-31,z+6),1,'detail')
                box('latch witness',(x,-29,z+7),(4,2,2),.3,'accent')
        tube('secondary seal',[(-21,-23,51),(-21,-23,116),(-15,-23,126),(15,-23,126),(21,-23,116),(21,-23,51),(-21,-23,51)],.4,'detail')
        for x in (-12,12):ring('test port',(x,-22,54),2.5,.6,3,(0,-1,0),'detail')
        tube('seal test manifold',[(-12,-26,54),(-12,-26,46),(12,-26,46),(12,-26,54)],.5,'detail')
    with group('C'):
        for y in (-64,-44,-24):rod('cross grate',( -36,y,16),(36,y,16),.6,'detail')
        for x in (-37,37):
            for y in (-65,-24):cyl('grate captive screw',(x,y,16),1,2,'detail',n=6)
        for x in (-22,22):box('drawer stop',(x,-74,4),(8,3,4),.6,'detail')
        tube('drawer gasket',[(-38,-72,8),(38,-72,8),(38,-16,8),(-38,-16,8),(-38,-72,8)],.45,'detail')
    for z in (42,57,72):
        ring('service quick coupling',(63,-45,z),4,1,3,(0,-1,0),'detail')
        box('coupling identity plate',(72,-45,z),(5,1,5),.3,'detail')
    for x in (-42,42):
        for z in (55,75,95):ring('handrail grip',(x,-61,z),2.5,.5,4,role='detail')


def fibre_braid():
    # Feed each yarn through its actual ceramic eye, then to the forming point.
    for wires in [g.wires,kit.GROUPS['B']['wires']]:
        wires[:]=[w for w in wires if not w[0].startswith('yarn lead')]
    with group('B'):
        for a in range(0,360,30):
            q=math.radians(a);x,z=49*math.cos(q),70+49*math.sin(q)
            tube('guided yarn',[(x,-20,z),(x*.83,-32,70+(z-70)*.83),(x*.13,-75,70+(z-70)*.13)],.2,'accent')
    kit.GROUPS['C']['parts'].extend((o,r) for o,r in g.parts if o.name.startswith('braided mandrel'))
    with group('B'):
        for a in range(0,360,30):
            q=math.radians(a);x,z=49*math.cos(q),70+49*math.sin(q)
            # Mirrored carrier groups feed clockwise and anticlockwise paths.
            ring('bobbin retaining washer',(x,-20.5,z),6.8,1,1,(0,-1,0),'detail')
            for yy in (-17,-13,-9,-5):ring('wound fibre',(x,yy,z),6.1,.25,.4,(0,1,0),'detail')
            rod('tension arm',(x,-24,z),(x*.83,-31,70+(z-70)*.83),.6,'detail')
            ring('ceramic eye',(x*.83,-32,70+(z-70)*.83),2,.5,1,(0,1,0),'detail')
        for a in range(0,360,15):
            q=math.radians(a);cyl('carrier track screw',(55*math.cos(q),-15,70+55*math.sin(q)),.7,1,'detail',(0,-1,0),6)
    # Replace original same-handed traces with a true pair of counterwound families.
    names=('braid trace',)
    g.wires[:]=[w for w in g.wires if not w[0].startswith(names)]
    for group_data in kit.GROUPS.values():group_data['wires'][:]=[w for w in group_data['wires'] if not w[0].startswith(names)]
    with group('C'):
        for hand in (-1,1):
            for phase in (0,math.pi):
                pts=[]
                for i in range(241):
                    a=hand*i*math.tau/80+phase;r=8.25+.22*math.sin(i*math.tau/40+phase+hand*math.pi/2)
                    pts.append((r*math.cos(a),-109+i*.24,70+r*math.sin(a)))
                g.wire('counterwound braid',pts,.12,'detail')
        for x in (-15,15):
            rod('chuck slide',(x,25,58),(x,25,82),.5,'detail')
        for a in range(0,360,30):
            with at((0,65,70),a,'Y'):rod('drive cooling fin',(16,0,0),(16,21,0),.5,'detail')


def quiet_stair():
    for side in (-1,1):
        for x,z,deckx,deckz in ((-65,17,-59,15.5),(63,60,58,57.5)):
            box('handrail tread bracket',(x,side*43,z-2),(12,12,4),1.2,'detail')
            rod('handrail bracket brace',(x,side*47,z),(deckx,side*36,deckz),1.4,'detail')
            for dx in (-3,3):cyl('handrail bracket bolt',(x+dx,side*40,z+.2),.7,.8,'detail',n=6)
    # Equal treads, repeatable supports and supported service components.
    with group('B'):
        for y in (-29,29):
            for x,z in ((-59,12),(-20,26),(19,40),(58,54)):
                for xx,zz in ((x,z-11),(x+21,z+5)):
                    ring('pivot dust washer',(xx,y-1,zz),4.6,.8,1,(0,-1,0),'detail')
                rod('paired link web',(x-1,y-3,z-9),(x+18,y-3,z+4),.5,'detail')
        rod('drive cross shaft',(66,-40,20),(66,35,20),3,'detail')
        for y in (-35,35):flange('shaft bearing',(66,y,20),7,(0,1,0),2)
    with group('C'):
        for y in (-29,-9,11,31):
            ring('sensor bezel',(-85.5,y,17),2.3,.5,1,(-1,0,0),'detail')
        box('contact safety edge',(-84,0,11),(3,75,3),1,'detail')
        rod('edge end retainer',(-85,-35,9),(-85,-35,15),.5,'detail')
    for x,z in ((-59,12),(-20,26),(19,40),(58,54)):
        rod('tread nose', (x-18,-39,z+3.7),(x-18,39,z+3.7),.6,'accent')
        for y in (-36,36):
            for xx in (-13,13):cyl('tread captive screw',(x+xx,y,z+3.7),.65,.6,'detail',n=6)
    box('release label recess',(64,-62,29),(18,1,10),1,'detail')
    rod('manual release lever',(63,-66,25),(69,-66,35),1,'detail')
    for x in (-44,77):
        for y in (-40,40):cyl('base anchor',(x,y,10.6),2,2,'detail',n=6)


def wind_kite():
    g.wires[:]=[w for w in g.wires if not w[0].startswith('traction tether')]
    tube('traction tether',[(0,8,177),(0,-10,110),(0,-11,65),(0,-11,46.3)],.35,'accent')
    with group('B'):
        # Level-wind carriage stays on the ground, clear of the drum.
        for z in (53,72):rod('fairlead guide',(-29,0,z),(29,0,z),1.4,'detail')
        for x in (-29,29):box('fairlead end support',(x,0,34),(5,8,80),1,'detail')
        box('levelwind traveller',(0,0,62),(13,8,25),2,'detail')
        rod('fairlead outrigger',(0,-3,62),(0,-9,62),1.5,'detail')
        ring('tether fairlead',(0,-11,63),4,1,3,(0,0,1),'detail')
        for x in range(-24,25,4):ring('guide screw turn',(x,0,53),2,.4,.7,(1,0,0),'detail')
        ring('drum brake disc',(-28,0,25),26,2,2,(1,0,0),'detail')
        box('brake caliper',(-29,-23,25),(9,10,19),2,'detail')
    with group('C'):
        with at((0,12,230),-8,'Y'):
            for x in (-80,-48,-16,16,48,80):
                for y in (-10,22):box('rib spar shoe',(x,y,0),(4,5,3),.6,'detail')
            for x in (-72,72):
                joint((x,9,-8),3,(0,1,0))
                rod('bridle hardpoint',(x,9,-8),(x,9,0),1.2,'detail')
            for x in (-91,91):
                tube('tip rib',[ (x,-10,-2),(x,3,4),(x,24,0)],.5,'detail')
    for x in (-48,52):
        box('anchor lug',(x,0,-7),(10,18,9),2,'detail')
        ring('anchor eye',(x,-10,-7),3,1,4,(0,1,0),'detail')


def seam_surgeon():
    # Open bearing frame: a solid cuboid hid the actual contact rollers in C.
    for parts in [g.parts,kit.GROUPS['C']['parts']]:
        parts[:]=[(o,r) for o,r in parts if not o.name.startswith('inspection shoe')]
    with group('C'):
        with at((0,0,65),67,'X'):
            for x in (-4,18):box('probe frame cheek',(x,-41,0),(3,15,23),1.2)
            box('probe rear bridge',(7,-47,0),(20,3,23),1.2)
            for x in (-4,18):
                for z in (-8,8):cyl('probe frame screw',(x,-33,z),.8,1,'detail',(0,1,0),6)
    with group('B'):
        for a in range(0,360,15):
            q=math.radians(a);rod('rail encoder tick',(11,46*math.cos(q),65+46*math.sin(q)),(11,48.5*math.cos(q),65+48.5*math.sin(q)),.3,'detail')
        with at((0,0,65),-36,'X'):
            ring('torch gas cup',(9,-28,0),3.5,.7,5,(0,1,0),'detail')
            tube('wire feed',[(4,-66,8),(4,-54,9),(9,-42,0),(9,-29,0)],.45,'cable')
            box('arc tracking head',(15,-36,0),(6,6,9),1,'detail')
            for x in (-3,15):cyl('carriage service screw',(x,-60,7),.9,2,'detail',(0,-1,0),6)
    with group('C'):
        with at((0,0,65),67,'X'):
            for x in (-2,16):
                rod('probe spring guide',(x,-48,0),(x,-33,0),.5,'detail')
                for y in range(-46,-34,2):ring('probe spring',(x,y,0),1.7,.4,.6,(0,1,0),'detail')
            tube('couplant feed',[(7,-56,7),(13,-47,8),(13,-33,0),(9,-31,0)],.5,'cable')
            ring('probe hose fitting',(7,-56,7),2,.5,3,(0,-1,0),'detail')
    for x in (-71,83):
        ring('pipe identity band',(x,0,65),32.2,.3,4,(1,0,0),'detail')
    for z in (17,29,41):ring('service manifold',(-45,32,z),3.5,1,3,(0,-1,0),'detail')


def queue_garden():
    with group('B'):
        for j in range(6):
            a=j*137;z=60+j*13
            with at((0,0,z),a):
                ring('leaf hinge washer',(6,-2,0),4.5,.6,1,(0,1,0),'detail')
                rod('leaf rib',(10,0,1),(42,0,15),.4,'detail')
                rod('event latch',(3,1,-8),(7,1,-2),.6,'detail')
        ring('stem index collar',(0,0,48),7,1,5,role='detail')
        for a in range(0,360,60):
            with at((0,0,50),a):box('index detent',(6,0,0),(3,2,4),.3,'detail')
        tube('event linkage',[(0,2,46),(3,2,70),(3,2,105),(2,2,140)],.35,'detail')
    with group('C'):
        for y in (-42,-50):
            for x in range(-14,15,7):ring('reader traction ring',(x,y,35),3.3,.5,1,(1,0,0),'detail')
        for x in (-13,13):
            cyl('board standoff',(x,-32,23),1.2,5,'detail')
        for x in range(-10,11,3):rod('ticket printed index',(x,-68,34.5),(x,-60,34.5),.2,'detail')
        tube('reader harness',[(0,-34,24),(13,-29,26),(13,-20,29),(0,-15,35)],.4,'cable')
    ring('pot service seam',(0,0,35),35.6,.4,1,role='detail')


def compliment_mill():
    with group('B'):
        for x in (-14,14):
            ring('inspection lens bezel',(x,-36,115),8.5,1,2,(0,1,0),'detail')
            for a in range(0,360,60):
                q=math.radians(a);cyl('lens rim screw',(x+7*math.cos(q),-37,115+7*math.sin(q)),.5,1,'detail',(0,-1,0),6)
        rod('focus synchronizer',(-14,7,119),(14,7,119),.8,'detail')
        for z in (91,95):ring('head swivel scale',(0,0,z),7,.5,1,role='detail')
    with group('C'):
        for x in (-20,-10,0,10,20):
            ring('paper traction ring',(x,-41,43),6.3,.5,1,(1,0,0),'detail')
        for x in (-25,25):
            rod('printer tension guide',(x,-28,48),(x,-40,48),.65,'detail')
            for y in range(-39,-28,2):ring('printer tension spring',(x,y,48),1.8,.4,.6,(0,1,0),'detail')
        for x in range(-14,15,4):
            rod('paper ruled receipt',(x,-55,36),(x,-62,34),.18,'detail')
    for x in range(-45,46,5):
        rod('inspection tray scale',(x,-129,14),(x,-125 if x%10 else -122,14),.22,'detail')
    for x,y in ((-38,-120),(38,-120),(-38,-82),(38,-82)):
        rod('tray fiducial',(x-2,y,14),(x+2,y,14),.25,'detail');rod('tray fiducial',(x,y-2,14),(x,y+2,14),.25,'detail')


SELECTED={2:tidal_loom,6:manta_foil,17:memory_kiln,18:lunar_porch,25:fibre_braid,
          38:quiet_stair,42:wind_kite,65:seam_surgeon,70:queue_garden,80:compliment_mill}

def enrich(entry):
    if entry['number'] in SELECTED:SELECTED[entry['number']]()
