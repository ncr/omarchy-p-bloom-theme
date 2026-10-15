"""Field biology and cultivation equipment, including explicit living context."""
from .kit import *


def sprig(root,height=44,spread=22):
    x,y,z=root;organic_branch('plant stem',[(x,y,z),(x+2,y,z+height*.5),(x,y,z+height)],1.1,'structure')
    for j in range(3):
        zz=z+height*(.25+j*.23);side=-1 if j%2 else 1
        leaf('living leaf',(x,y,zz),(x+side*spread,y+side*5,zz+height*.22),spread*.65,'detail')


def seed_courier():
    # Low six-legged rover keeps its seed head below an arched protective chassis.
    with group('B'):
        cyl('seed indexing disc',(0,0,73),34,7)
        for a in range(0,360,30):
            q=math.radians(a);cyl('seed capsule',(25*math.cos(q),25*math.sin(q),81),4,9,'accent',n=20)
        ring('indexer guide',(0,0,72),37,2,14)
        motor((0,0,45),13,23)
        mark('SEED INDEXER',(21,-22,83),'TWELVE INDIVIDUAL CAPSULE POCKETS')
    with group('C'):
        cyl('soil dart guide',(31,0,20),7,35)
        rod('penetrating tip',(31,0,2),(31,0,23),3,'detail')
        flange('dart collar',(31,0,54),11,depth=3)
        for x in (20,42):rod('linear slide',(x,0,23),(x,0,64),1.5,'detail')
        box('dart carriage',(31,0,48),(30,18,10),3)
        tube('capsule chute',[(24,0,79),(32,0,69),(31,0,56)],3,'cable')
        mark('SOIL DART',(32,-6,29),'PLACES CAPSULE BELOW THE SURFACE')
    hull('protective cowling',[(-54,15,8,68),(-34,42,15,78),(34,42,15,78),(54,15,8,68)])
    # Cowling is split longitudinally to keep the indexer readable.
    ob=g.parts[-1][0];ob.location.y=47;ob.scale.y=.25
    for side in (-1,1):
        for x in (-45,0,45):
            hip=(x,side*33,59);knee=(x+8,side*64,38);foot=(x+14,side*74,0)
            rod('upper walker leg',hip,knee,3);joint(knee,5);rod('lower walker leg',knee,foot,2)
            box('walker foot',foot,(20,18,4),4)
    optics((-45,-14,69),9,17,(-1,0,0));optics((-43,14,70),5,14,(-1,0,0))
    panel('solar roof',(-10,10,104),(71,48),nx=7,ny=5)
    sprig((-74,36,0),40,20)
    mark('VISION',(-61,-14,69),'AVOIDS EXISTING PLANTS AND NESTS')
    mark('WALKER FOOT',(12,-74,2),'SMALL CONTACT PATCH / LOW LOAD')
    return 27,27


def pollen_steward():
    wheels(43,29,15);hull('greenhouse rover',[(-62,12,7,36),(-42,30,16,36),(40,30,16,36),(60,12,7,36)])
    rod('arm mast',(0,0,49),(0,0,106),5);joint((0,-5,106),10)
    rod('arm link',(0,0,106),(42,0,137),5);joint((42,-5,137),8)
    rod('wrist link',(42,0,137),(77,-7,124),4)
    with group('B'):
        gripper((79,-7,121),20,(0,0,-1))
        for a in range(0,360,60):
            q=math.radians(a);tube('soft flower brush',[(79+5*math.cos(q),-7+5*math.sin(q),99),(79+9*math.cos(q),-7+9*math.sin(q),91)],.55,'accent')
        optics((71,-17,115),4,9,(1,0,0))
        mark('SOFT POLLINATOR',(79,-8,98),'COMPLIANT FLOWER CONTACT')
    with group('C'):
        vessel('pollen reservoir',(-28,0,55),13,35)
        flange('sterile lid',(-28,0,90),16,depth=3)
        cyl('metering screw',(-28,0,44),6,12,'detail')
        box('meter drive',(-14,0,49),(16,19,15),3)
        tube('pollen feed',[(-28,-14,58),(-12,-23,83),(1,-14,105)],1,'cable')
        mark('POLLEN RESERVOIR',(-28,-14,76),'SMALL BATCH / CLEANABLE CHAMBER')
    tube('arm service line',[(1,-12,106),(22,-9,137),(43,-11,139),(75,-15,125)],1,'cable')
    sprig((86,6,0),83,25)
    for a in range(0,360,72):
        q=math.radians(a);leaf('flower petal',(86,6,84),(86+11*math.cos(q),6+11*math.sin(q),92),10,'shell')
    box('navigation chest',(-44,-5,60),(27,32,20),5);optics((-59,-5,60),6,9,(-1,0,0))
    mark('FLOWER',(86,6,90),'LIVING PLANT / TOOL TARGET')
    mark('NAVIGATION',(-64,-5,60),'ROW AND FLOWER LOCALISATION')
    return 26,22


def root_post():
    views(C=(26,-18))
    # A narrow planted instrument and articulated injection arm, no robot body.
    with group('B'):
        cyl('microdose barrel',(32,-4,33),6,42)
        rod('injection needle',(32,-4,-11),(32,-4,33),1.6,'detail')
        flange('meter collar',(32,-4,76),10,depth=3)
        cyl('syringe drive',(32,-4,80),8,19,'detail')
        tube('dose inlet',[(32,-4,79),(42,1,85),(44,13,89)],1,'accent')
        mark('MICRODOSE TIP',(32,-6,28),'DELIVERY BESIDE ACTIVE ROOTS')
    with group('C'):
        box('root scanner',(-28,0,13),(43,39,17),6)
        for x in (-43,-28,-13):
            rod('scanner tine',(x,0,6),(x,0,-20),2,'detail');ring('tine collar',(x,0,7),4,1,2)
        panel('sensor face',(-28,-20,14),(30,10),(0,-1,0),nx=6,ny=1,role='accent')
        for x in (-43,-13):cyl('housing fastener',(x,0,23),1.7,2,'detail',n=6)
        mark('ROOT SCANNER',(-30,-20,16),'LOCAL MOISTURE AND IMPEDANCE')
    cyl('service post',(0,16,0),10,147);ring('post collar',(0,16,101),13,2,8)
    vessel('dose cartridge',(0,16,101),17,48)
    rod('tool arm',(0,16,87),(32,-4,87),4);joint((0,10,87),7)
    panel('power canopy',(0,15,165),(80,55),nx=8,ny=5)
    tube('sensor tether',[(-28,0,27),(-17,11,35),(0,10,77)],.8,'cable')
    box('display pod',(0,2,63),(26,20,34),4)
    sprig((-57,35,0),124,32)
    mark('DOSE CARTRIDGE',(0,-2,128),'TREE SPECIFIC NUTRIENT BLEND')
    mark('POWER CANOPY',(24,5,166),'OFF GRID FIELD SERVICE')
    return 23,23


def mycelium_loom():
    with group('B'):
        box('breathable lower mold',(0,0,47),(138,91,7),7)
        for x in range(-58,60,12):
            for y in range(-33,34,11):cyl('mold breathing pore',(x,y,51),1.2,.7,'detail',n=12)
        for x in (-66,66):box('mold edge',(x,0,61),(5,91,29),2)
        for y in (-42,42):box('mold end',(0,y,61),(128,5,29),2)
        # A purposeful fibrous fill, clipped to the real mold volume.
        for i in range(18):
            x=-59+i*6.8;tube('cultivation fibre',[(x,-36,64),(x+2,-14,68),(x-2,13,66),(x,36,65)],.3,'shell')
        mark('BREATHABLE MOLD',(5,-34,63),'FIBRE GROWTH UNDER CONTROLLED AIRFLOW')
    with group('C'):
        box('drying plenum',(0,0,28),(144,98,27),8)
        for x in range(-57,58,9):rod('plenum diffuser slot',(x,-38,42),(x,38,42),.6,'detail')
        cyl('blower inlet',(0,51,29),17,17,'structure',(0,1,0))
        rotor((0,69,29),13,5,(0,1,0));ring('blower guard',(0,72,29),19,2,3,(0,1,0))
        mark('DRYING PLENUM',(0,52,29),'EVEN WARM AIR AFTER GROWTH')
    for x in (-61,61):
        for y in (-37,37):rod('bench leg',(x,y,20),(x,y,-12),3)
    for x in (-77,77):
        rod('lid strut',(x,33,59),(x,44,113),2)
    with at((0,44,110),65,'X'):
        box('raised inspection lid',(0,0,0),(146,95,5),7)
        for x in (-58,58):rod('lid rail',(x,-35,3),(x,35,3),1,'detail')
    box('environment controller',(95,0,49),(30,44,58),6);g.dial(95,-24,56,9)
    mark('LID',(0,45,119),'BREATHABLE ENVIRONMENT COVER')
    mark('CONTROLLER',(95,-23,54),'HUMIDITY AND TEMPERATURE SCHEDULE')
    return 26,29


def coral_cradle():
    with group('B'):
        gripper((-67,0,87),26,(0,0,-1))
        for side in (-1,1):
            box('soft silicone contact',(-67+side*9,0,57),(5,18,17),2,'accent')
        optics((-57,-13,80),4,8,(-1,0,0))
        joint((-67,0,95),7)
        mark('FRAGMENT GRIPPER',(-66,-7,61),'COMPLIANT CONTACT ON DEAD BASE')
    with group('C'):
        box('nursery tile',(32,0,9),(63,51,7),6)
        for x,y in ((14,-13),(43,-12),(29,15)):
            cyl('fragment socket',(x,y,14),6,7,'detail')
            organic_branch('coral primary branch',[(x,y,20),(x+2,y,37),(x-1,y+3,49)],1.7,'structure')
            for side in (-1,1):organic_branch('coral branch',[(x+1,y,34),(x+side*8,y+2,42),(x+side*11,y+4,49)],1,'detail')
        for x in (8,56):cyl('tile handling point',(x,0,14),2,3,'accent')
        mark('NURSERY TILE',(40,-11,19),'IDENTIFIED FRAGMENTS / OPEN FLOW')
    box('cradle deck',(0,0,1),(173,93,8),8)
    for x in (-69,69):
        for y in (-33,33):rod('cradle foot',(x,y,0),(x,y,-18),3)
    joint((-15,24,13),10);rod('arm lower',(-15,24,17),(-24,24,82),4);joint((-24,20,82),8)
    rod('arm upper',(-24,24,82),(-67,0,96),4)
    for side in (-1,1):
        ring('gentle circulation fan',(side*70,18,31),14,3,14,(0,1,0));rotor((side*70,23,31),10,5,(0,1,0))
    tube('service hose',[(-15,24,13),(-12,28,66),(-28,28,87),(-66,7,96)],1,'cable')
    mark('CURRENT FAN',(70,15,31),'LOW SHEAR WATER CIRCULATION')
    mark('TRANSFER ARM',(-26,24,82),'LIMITED FORCE POSITIONING')
    return 26,26


def spore_library():
    # Curved radial magazine with one real drawer extended for access.
    with group('B'):
        box('extended culture drawer',(-18,-72,48),(48,81,14),6)
        for x in (-31,-5):
            for y in (-92,-67,-42):
                cyl('culture well',(x,y,56),9,6,'structure');ring('sealed well lid',(x,y,62),9,.7,1,'Z' if False else (0,0,1),'accent')
        for x in (-40,4):rod('drawer rail',(x,-102,42),(x,7,42),2,'detail')
        box('drawer handle',(-18,-114,49),(24,7,7),2)
        mark('CULTURE DRAWER',(-19,-92,64),'SIX INDEPENDENTLY SEALED CULTURES')
    with group('C'):
        cyl('transfer lock',(61,-12,79),19,28,'structure',(0,-1,0))
        flange('sterile port',(61,-42,79),24,(0,-1,0),4)
        ring('interlock ring',(61,-49,79),20,2,3,(0,-1,0),'accent')
        for a in (0,120,240):
            q=math.radians(a);box('bayonet latch',(61+22*math.cos(q),-51,79+22*math.sin(q)),(7,7,9),2,'detail')
        mark('TRANSFER PORT',(61,-53,79),'INTERLOCKED STERILE ACCESS')
    with at((0,14,0)):
        g.casting('archive cabinet',[(0,64,39),(8,71,43),(115,71,43),(130,60,36)])
        for z in (10,127):g.trim('cabinet seam',z,70,43)
    # Drawer fronts are a façade on the actual near surface.
    for z in (28,77,102):
        box('culture drawer front',(-18,-31,z),(50,7,19),4)
        rod('drawer pull',(-31,-37,z),(-5,-37,z),1.6,'detail')
    box('climate service',(60,40,55),(32,42,83),6)
    for z in range(25,92,7):rod('service vent',(77,28,z),(77,55,z),.7,'detail')
    optics((0,-30,115),6,10)
    mark('CLIMATE SERVICE',(75,27,62),'PER DRAWER ENVIRONMENT CONTROL')
    mark('VERIFY HEAD',(0,-41,115),'CULTURE ID / NO UNKNOWN RETURNS')
    return 24,25


def canopy_weaver():
    # A saddle mounted to a visible tree trunk and an articulated cable handling head.
    with group('B'):
        ring('bark saddle',(0,0,58),27,4,44,role='structure',start=10,end=330)
        for a in (45,135,225,315):
            q=math.radians(a);box('soft bark pad',(22*math.cos(q),22*math.sin(q),79),(10,12,30),4,'detail')
        for z in (65,94):ring('saddle strap',(0,0,z),29,1,3,role='accent')
        joint((30,0,79),10)
        mark('BARK SADDLE',(-25,-7,79),'BROAD PADS / NO CLIMBING SPIKES')
    with group('C'):
        with at((86,0,117)):
            cyl('tension drum',(-13,0,0),13,26,'structure',(1,0,0))
            for x in (-16,16):flange('drum side',(x,0,0),16,(1,0,0),3)
            motor((19,0,0),8,18,(1,0,0))
            box('rope guide',(0,-18,0),(27,10,15),3)
            for x in (-9,9):cyl('guide roller',(x,-20,-5),3,10,'detail')
        mark('TENSION HEAD',(87,-16,119),'MEASURED SUPPORT CABLE TENSION')
    rod('positioning arm',(29,0,79),(58,0,113),4);joint((58,-5,113),8)
    rod('wrist arm',(58,0,113),(86,0,117),4)
    tube('support rope',[(86,-18,117),(116,-27,145),(140,-13,172)],.7,'accent')
    # Schematic woody context, explicitly drawn as a plant, not a second machine.
    hull('tree trunk',[(-9,16,16,0),(45,19,19,0),(115,15,15,0),(165,11,11,0)],'X')
    ob=g.parts[-1][0];ob.matrix_world=Matrix.Rotation(-math.pi/2,4,'Y')
    organic_branch('branch',[(0,0,126),(41,15,154),(79,24,181)],5,'detail')
    sprig((78,24,178),38,25)
    box('saddle power pack',(0,33,77),(38,24,44),5)
    optics((48,-12,107),5,10,(1,0,0))
    mark('VISION',(56,-12,107),'BRANCH AND CABLE CLEARANCE')
    mark('TREE',(0,0,143),'LIVING ANCHOR / LOAD LIMITED')
    return 25,22


def algae_ribbon():
    # Serpentine transparent film channels rather than a stack of generic tanks.
    with group('B'):
        for z in (26,49,72,95):
            box('transparent film channel',(0,0,z),(141,49,5),5,'shell')
            for y in (-20,20):rod('channel edge',(-66,y,z+3),(66,y,z+3),1,'structure')
            for x in range(-55,56,10):rod('film spacer',(x,-17,z+3),(x,17,z+3),.25,'accent')
        for i,z in enumerate((26,49,72)):
            x=68*(-1 if i%2 else 1);tube('channel return',[(x,0,z+3),(x*1.14,0,z+9),(x*1.14,0,z+17),(x,0,z+26)],3,'detail')
        mark('FILM CHANNEL',(25,-19,97),'THIN SUNLIT CULTURE FLOW')
    with group('C'):
        rod('gas header',(-51,36,26),(51,36,26),5)
        for x in range(-45,46,15):
            rod('exchange finger',(x,36,26),(x,36,87),2,'detail')
            for z in (42,59,76):ring('membrane sleeve',(x,36,z),3.5,1,8,role='accent')
        flange('gas connection',(55,36,26),8,(1,0,0))
        mark('EXCHANGE COMB',(30,36,63),'CONTROLLED GAS TRANSFER')
    for x in (-62,62):
        for y in (-23,23):rod('frame upright',(x,y,0),(x,y,114),2.5)
    box('harvest sump',(0,0,6),(134,62,13),8);pump((-87,4,13),.5)
    tube('circulation line',[(-86,4,26),(-94,10,85),(-70,0,99)],2,'cable')
    optics((88,-5,71),5,10,(-1,0,0));rod('sensor post',(85,0,0),(85,0,80),2)
    mark('HARVEST SUMP',(0,-30,8),'DRAINABLE CLEANING AND HARVEST')
    mark('OPTICAL SENSOR',(79,-5,71),'CULTURE DENSITY TREND')
    return 27,27


def soil_choir():
    # One hub, three physically different-height but same-pattern satellite probes.
    with group('B'):
        with at((-73,-18,0)):
            cyl('probe body',(0,0,0),7,68)
            for z in (5,27,49):ring('sensing electrode',(0,0,z),8,1,6,role='accent')
            cyl('probe cap',(0,0,69),11,9);flange('service cap',(0,0,79),12,depth=2)
            rod('probe tip',(0,0,-18),(0,0,0),2,'detail')
        mark('PROBE TINE',(-73,-25,31),'DEPTH RESOLVED MOISTURE AND CHEMISTRY')
    with group('C'):
        box('field hub',(13,5,93),(62,46,35),8)
        for x in (-9,35):cyl('sealed cable socket',(x,-19,89),4,5,'detail',(0,-1,0),24)
        optics((13,-22,95),5,9)
        panel('hub solar cover',(13,5,119),(83,62),nx=8,ny=6)
        for x in (-10,36):rod('cover stay',(x,5,109),(x,5,118),2,'detail')
        mark('FIELD HUB',(15,-21,99),'COMPARES LOCAL TRENDS')
    for x,y in ((66,-24),(-29,57)):
        cyl('satellite probe',(x,y,0),7,68)
        for z in (5,27,49):ring('sensing electrode',(x,y,z),8,1,6,role='accent')
        cyl('probe cap',(x,y,69),11,9)
        tube('probe cable',[(x,y,78),(x*.55,y*.5,84),(14,5,75)],.75,'cable')
    tube('probe cable',[(-73,-18,78),(-35,-10,84),(13,5,75)],.75,'cable')
    rod('hub mast',(13,5,0),(13,5,77),4)
    for a in (0,120,240):
        with at((13,5,0),a):rod('hub tripod',(0,0,40),(34,0,0),2);box('foot',(34,0,0),(20,17,4),3)
    sprig((65,40,0),58,23)
    mark('SATELLITE',(67,-24,58),'SAME CALIBRATION / ANOTHER PATCH')
    mark('LIVING CONTEXT',(66,40,37),'LOCAL ROOT ZONE / NO FIELD AVERAGE')
    return 26,26


def orchard_tender():
    wheels(69,40,18);hull('orchard carriage',[(-94,12,8,44),(-64,40,15,44),(61,40,15,44),(87,13,8,44)])
    rod('arm mast',(-44,4,56),(-44,4,108),6);joint((-44,-3,108),11)
    rod('upper picking arm',(-44,4,108),(6,4,154),6);joint((6,-3,154),9)
    rod('forearm',(6,4,154),(54,-4,140),4)
    with group('B'):
        gripper((56,-4,136),28,(0,0,-1))
        for side in (-1,1):leaf('soft fruit cup',(56+side*12,-4,117),(56+side*5,-4,101),17,'accent')
        optics((45,-18,130),4,9,(1,0,0));joint((55,-5,139),6)
        mark('SOFT GRIPPER',(56,-4,111),'SUPPORTS FRUIT BEFORE RELEASE')
    with group('C'):
        box('fruit tray',(29,0,69),(94,64,7),7)
        for x in (-10,68):box('tray side',(x,0,78),(4,64,18),2)
        for y in (-29,29):box('tray end',(29,y,78),(79,4,18),2)
        for x in (3,29,55):
            for y in (-14,14):
                ring('cushioned fruit nest',(x,y,75),10,2,4,role='detail')
                g.ball('picked fruit',(x,y,84),(8,8,8),'shell');rod('fruit stem',(x,y,91),(x+1,y,95),.6,'detail')
        mark('CUSHIONED TRAY',(30,-28,78),'SHALLOW INDIVIDUAL FRUIT NESTS')
    tube('arm service cable',[(-43,12,55),(-47,16,106),(5,13,160),(54,7,144)],1.2,'cable')
    box('vision head',(-71,0,75),(23,39,26),5)
    for y in (-11,11):optics((-83,y,75),6,10,(-1,0,0))
    sprig((98,31,0),118,25);g.ball('unpicked fruit',(90,30,110),(8,8,8),'shell')
    mark('VISION',(-91,-10,76),'RIPENESS AND BRANCH CLEARANCE')
    mark('ARM JOINT',(5,-5,154),'SLOW LOAD CONTROL NEAR CANOPY')
    return 26,23
