"""Ten manufacturing mechanisms with physically shared tool studies."""
from .kit import *


def glass_river():
    with group('B'):
        die=hull('heated die',[(15,25,18,50),(21,29,22,50),(45,29,22,50),(52,25,18,50)])
        for x in (22,29,36,43):hull_seam(die,x,'detail')
        box('glass exit slot',(53,0,50),(3,43,6),1,'accent')
        for y in (-24,24):rod('die tie',(13,y,39),(52,y,39),2,'detail')
        flange('feed neck',(13,0,50),20,(-1,0,0))
        mark('HEATED DIE',(43,-26,54),'CONTROLLED GLASS DRAW CHANNEL')
    with group('C'):
        for y in (-23,23):
            vessel('separate batch hopper',(-65,y,69),20,39)
            cyl('hopper gate',(-65,y,55),9,15,'detail');motor((-51,y,59),6,15,(1,0,0))
        rod('batch feed',(-64,-23,55),(-64,23,55),8)
        box('selector block',(-64,0,47),(29,29,23),5)
        mark('BATCH SELECTOR',(-65,-23,85),'KEEPS INCOMPATIBLE GLASSES APART')
    cyl('melting barrel',(-47,0,49),23,60,'structure',(1,0,0))
    for x in range(-43,11,9):ring('barrel heater',(x,0,49),25,2,4,(1,0,0),'detail')
    box('formed glass ribbon',(83,0,49),(61,39,3),1,'accent')
    for x in (67,83,100,114):
        cyl('draw roller',(x,-28,42),6,56,'detail',(0,1,0))
        for y in (-31,31):box('roller bearing',(x,y,37),(9,7,17),2,'detail')
    box('cast machine bed',(13,0,20),(233,84,16),12)
    for x in (-78,96):
        for y in (-30,30):rod('bed leg',(x,y,16),(x,y,0),4)
    mark('DRAW ROLLERS',(99,-22,43),'MATCHED SPEED / FLATNESS CONTROL')
    mark('MELTING BARREL',(-14,-24,50),'HOMOGENISED HOT GLASS')
    return 25,25


def road_mender():
    wheels(63,36,18);hull('road service chassis',[(-88,10,7,45),(-59,38,20,45),(48,38,20,45),(77,15,11,45)])
    with group('B'):
        box('seam shoe',(87,0,6),(43,36,9),6)
        for y in (-13,13):rod('shoe skid',(70,y,1),(108,y,1),1.5,'detail')
        rod('injector lance',(87,0,12),(87,0,33),4)
        ring('shoe swivel',(87,0,30),9,3,5)
        for y in (-16,16):rod('shoe arm',(50,y,39),(86,y,20),3)
        optics((98,-8,24),4,9,(0,0,-1))
        mark('SEAM SHOE',(90,-13,11),'CLEAN / FILL / FINISH IN ONE PASS')
    with group('C'):
        vessel('repair cartridge',(-24,0,66),25,55)
        flange('cartridge lid',(-24,0,121),27,depth=4)
        cyl('metering cylinder',(-24,0,49),8,20,'detail')
        motor((-12,-20,63),8,19,(1,0,0))
        tube('metering elbow',[(-23,0,60),(3,0,60),(12,-17,49)],2.5,'accent')
        mark('METERING CARTRIDGE',(-24,-25,92),'MATCHED MATERIAL / MEASURED DOSE')
    tube('heated feed',[(7,-26,61),(37,-35,51),(69,-26,35),(88,-7,27)],3,'cable')
    box('vacuum pod',(40,0,79),(36,55,39),8)
    for x in range(28,54,5):rod('pod vent',(x,-28,70),(x,-28,89),.6,'detail')
    optics((-79,-12,53),7,13,(-1,0,0));optics((-79,12,53),7,13,(-1,0,0))
    tube('suction duct',[(42,10,64),(60,26,45),(87,13,13)],4,'detail')
    mark('SEAM SCANNER',(-88,-12,54),'MAPS CRACK BEFORE MATERIAL DELIVERY')
    mark('VACUUM POD',(41,-27,82),'DEBRIS REMOVAL BEFORE BONDING')
    return 25,25


def fibre_braid():
    with group('B'):
        for y in (-9,9):ring('braider track',(0,y,70),58,7,5,(0,1,0))
        for a in range(0,360,30):
            q=math.radians(a);x,z=49*math.cos(q),70+49*math.sin(q)
            cyl('yarn carrier',(x,-19,z),6,20,'structure',(0,1,0))
            for yy in (-20,-2):ring('bobbin flange',(x,yy,z),8,1,2,(0,1,0),'detail')
            tube('yarn lead',[(x,-20,z),(x*.47,-45,70+(z-70)*.47),(x*.13,-75,70+(z-70)*.13)],.2,'accent')
        mark('CARRIER TRACK',(41,-13,104),'TWIN TRACK RINGS ON PEDESTALS')
    with group('C'):
        cyl('mandrel chuck',(0,30,70),22,31,'structure',(0,1,0))
        flange('chuck face',(0,27,70),25,(0,-1,0))
        for a in (0,120,240):
            q=math.radians(a);rod('chuck jaw',(7*math.cos(q),21,70+7*math.sin(q)),(19*math.cos(q),21,70+19*math.sin(q)),3,'detail')
        motor((0,62,70),16,30,(0,1,0))
        mark('MANDREL CHUCK',(0,24,91),'CENTRED REMOVABLE FORM')
    rod('braided mandrel',(0,-109,70),(0,35,70),8)
    for j in range(2):
        pts=[]
        for i in range(161):a=T*i/20+j*math.pi;pts.append((8.4*math.cos(a),-109+i*.24,70+8.4*math.sin(a)))
        g.wire('braid trace',pts,.18,'detail')
    box('cast braider base',(0,10,6),(152,196,13),12)
    for x in (-47,47):rod('track pedestal',(x,0,12),(x,0,39),5)
    box('chuck support',(0,69,38),(44,43,60),7)
    for y in (-85,-48):
        for x in (-17,17):rod('output guide',(x,y,12),(x,y,65),3)
        rod('guide roller',(-17,y,65),(17,y,65),4,'detail')
    mark('BRAIDED OUTPUT',(0,-99,70),'FOUR OUTPUT GUIDE POSTS')
    mark('CHUCK DRIVE',(0,82,71),'SYNCHRONISED FORM ADVANCE')
    return 34,25


def metal_orchard():
    with group('B'):
        vessel('melt crucible',(0,0,109),24,44)
        ring('atomizer throat',(0,0,104),18,6,6)
        for a in range(0,360,45):
            q=math.radians(a);rod('gas jet',(15*math.cos(q),15*math.sin(q),109),(7*math.cos(q),7*math.sin(q),102),1.5,'accent')
        flange('crucible lid',(0,0,153),27,depth=4)
        mark('ATOMIZER THROAT',(0,-16,106),'INERT GAS BREAKS VERIFIED MELT')
    with group('C'):
        for z in (17,32,47):
            ring('sieve cassette',(0,0,z),35,4,7)
            panel('sieve screen',(0,0,z+3),(43,43),nx=13,ny=13,role='shell')
        for x,y in ((31,0),(-15,27),(-15,-27)):rod('sieve tie',(x,y,12),(x,y,57),2,'detail')
        box('vibration motor',(39,0,31),(24,27,26),5);cyl('eccentric cover',(52,0,31),8,4,'detail',(1,0,0))
        mark('SIEVE CASSETTE',(25,-21,40),'SCREENED PARTICLE SIZE FRACTIONS')
    g.shell('sectioned settling chamber',41,59,106,20,215)
    for z in (58,106):flange('chamber ring',(0,0,z),44,depth=3)
    for a in (0,120,240):
        with at(angle=a):rod('tower leg',(37,0,103),(54,0,0),3);box('isolation foot',(54,0,0),(23,23,7),4)
    vessel('gas recovery vessel',(-72,18,6),19,98)
    tube('gas return',[(-72,-3,81),(-64,-14,120),(-16,-8,125)],2,'cable')
    box('powder drawer',(0,-36,8),(49,42,14),5)
    mark('GAS RECOVERY',(-72,-3,68),'CLOSED INERT ATMOSPHERE')
    mark('POWDER DRAWER',(0,-56,12),'SEALED SCREENED BATCH')
    return 27,24


def patch_arm():
    # Portable clamped articulated repair arm; shield is local, not a giant enclosure.
    with group('B'):
        with at((74,-4,73),-18,'Y'):
            cyl('deposition wrist',(0,0,0),13,22)
            flange('wrist coupling',(0,0,23),16,depth=3)
            cyl('nozzle body',(0,0,-17),7,18,'detail');rod('nozzle tip',(0,0,-27),(0,0,-17),2,'accent')
            optics((10,-9,-9),4,8,(0,0,-1))
            tube('wire guide',[(0,12,21),(9,15,5),(3,5,-21)],1,'cable')
        mark('DEPOSITION WRIST',(76,-8,66),'REPAIRS A LOCAL MISSING SURFACE')
    with group('C'):
        ring('shield rim',(74,-4,29),29,3,5)
        for a in range(0,360,45):
            q=math.radians(a);leaf('shield petal',(74+25*math.cos(q),-4+25*math.sin(q),32),(74+15*math.cos(q),-4+15*math.sin(q),53),16,'shell')
        tube('shield gas hose',[(96,5,35),(109,15,48),(101,32,67)],1.8,'cable')
        mark('LOCAL SHIELD',(91,-15,38),'SMALL INERT PROCESS ENVELOPE')
    box('workpiece',(13,0,0),(183,83,18),7)
    for x in (-69,-36):
        box('clamp jaw',(x,0,16),(21,49,13),4);rod('clamp screw',(x,-18,-10),(x,-18,31),3,'detail')
        ring('clamp wheel',(x,-18,33),10,2,2)
    cyl('arm base',(-53,4,25),20,21);joint((-53,0,61),10)
    rod('upper arm',(-53,4,49),(-29,4,113),6);joint((-29,-3,113),10)
    rod('forearm',(-29,4,113),(41,4,109),5);joint((41,-3,109),8)
    rod('wrist link',(41,4,109),(71,-4,96),4)
    tube('service bundle',[(-56,14,45),(-36,16,115),(8,17,127),(52,13,108),(73,8,98)],2,'cable')
    box('wire feed pack',(-71,31,55),(35,28,55),6)
    mark('CLAMP',(-67,-18,30),'REMOVABLE FIXTURE ON EXISTING PART')
    mark('ARM JOINT',(-29,-5,113),'LOCAL REPAIR PATH CONTROL')
    return 27,25


def ceramic_nest():
    with group('B'):
        vessel('paste reservoir',(0,0,135),17,32)
        cyl('extrusion screw',(0,0,102),9,33)
        motor((0,0,172),12,24)
        rod('ceramic nozzle',(0,0,91),(0,0,104),3,'accent')
        box('tool carriage',(0,12,126),(49,23,31),5)
        for x in (-19,19):cyl('carriage roller',(x,24,126),6,5,'detail',(0,1,0))
        mark('EXTRUSION HEAD',(0,-10,118),'METERED REFRACTORY PASTE')
    with group('C'):
        ring('heated cradle',(0,0,19),58,10,30)
        for z in (24,36,45):ring('cradle heater',(0,0,z),59,1,2,role='accent')
        cyl('build floor',(0,0,21),48,4,'detail')
        for a in range(0,360,60):
            q=math.radians(a);box('cradle standoff',(52*math.cos(q),52*math.sin(q),11),(11,11,16),3)
        mark('HEATED CRADLE',(36,-43,36),'GRADUAL DRYING / WALL SUPPORT')
    for x in (-67,67):truss((x,22,7),(x,22,172),10,8)
    for z in (121,147):rod('gantry rail',(-67,22,z),(67,22,z),3)
    box('bed',(0,0,3),(155,139,13),11)
    # Interlocking curved wall printed within the actual cradle.
    for z in range(26,79,4):ring('printed ceramic layer',(0,0,z),31,6,3,role='detail',start=20,end=315)
    tube('paste feed',[(0,0,165),(27,16,192),(61,24,176),(69,37,73)],2,'cable')
    box('service cabinet',(-91,31,47),(31,48,72),6)
    mark('CERAMIC PART',(18,-20,69),'LAYERED INTERLOCKING REFRACTORY')
    mark('GANTRY',(66,22,117),'TWO AXIS TOOL SUPPORT')
    return 25,24


def seam_surgeon():
    views(B=(64,25),C=(155,50))
    with group('B'):
        ring('orbital rail',(0,0,65),49,5,10,(1,0,0))
        with at((0,0,65),-36,'X'):
            box('orbital carriage',(6,-48,0),(31,20,26),4)
            for x in (-5,17):cyl('track wheel',(x,-43,0),7,5,'detail',(1,0,0))
            motor((7,-65,0),7,17,(0,1,0))
            rod('welding torch',(9,-44,0),(9,-27,0),3,'accent')
        mark('ORBITAL CARRIAGE',(8,-45,93),'CONTROLLED PASS AROUND THE JOINT')
    with group('C'):
        with at((0,0,65),67,'X'):
            box('inspection shoe',(7,-41,0),(26,15,23),4)
            for z in (-7,7):cyl('inspection roller',(-2,-33,z),3,18,'detail',(1,0,0))
            box('contact transducer',(7,-32,0),(12,4,6),1,'accent')
            for x in (-3,17):rod('roller bearing plate',(x,-40,-8),(x,-33,-8),1,'detail')
            optics((7,-53,0),5,12,(0,1,0))
            rod('shoe spring',(7,-53,-8),(7,-42,-8),1,'detail')
        mark('INSPECTION SHOE',(8,-16,27),'CHECKS THE COMPLETED SEAM')
    cyl('left pipe',(-81,0,65),32,81,'detail',(1,0,0));cyl('right pipe',(10,0,65),32,86,'detail',(1,0,0))
    for x in (-59,70):
        ring('pipe cradle',(x,0,65),36,4,8,(1,0,0),start=175,end=365)
        for y in (-22,22):rod('stand leg',(x,y,40),(x,y*1.6,0),3)
        box('stand foot',(x,0,-1),(31,93,7),5)
    box('service pod',(-45,53,30),(53,39,54),7)
    tube('weld service',[(-43,34,46),(-20,25,120),(3,-22,125),(8,-45,96)],2,'cable')
    mark('PIPE JOINT',(8,-32,65),'PREPARED BUTT JOINT / COMMON AXIS')
    mark('SERVICE POD',(-47,32,31),'POWER / GAS / REFUSAL LOG')
    return 30,24


def foam_forge():
    views(B=(35,-20))
    with group('B'):
        cyl('gas injector cover',(-58,0,79),12,45)
        cyl('injector metering stem',(-58,0,83),2.2,39,'detail')
        for z in (88,100,114):ring('injector distribution ring',(-58,0,z),8,1.5,2,role='detail')
        flange('injector flange',(-58,0,125),16,depth=4)
        for a in range(0,360,60):
            q=math.radians(a);rod('injector passage',(-58+7*math.cos(q),7*math.sin(q),85),(-58+4*math.cos(q),4*math.sin(q),73),1,'detail')
        tube('gas inlet',[(-46,0,109),(-32,10,117),(-28,26,117)],2,'accent')
        mark('GAS INJECTOR',(-58,-13,100),'CONTROLLED FOAM NUCLEATION')
    uncover('B','gas injector cover')
    with group('C'):
        for y in (-26,26):
            box('split mold half',(28,y,37),(78,25,48),6)
            for x in (-1,57):rod('mold alignment pin',(x,y-17,39),(x,y+17,39),2,'detail')
            for x in (0,20,40,58):box('mold rib',(x,y,65),(4,23,6),1,'detail')
        box('mold base',(28,0,8),(104,93,12),8)
        for x in (-18,74):ring('clamp wheel',(x,0,51),9,2,3)
        mark('SPLIT MOLD',(27,-32,58),'OPENED TO SHOW RIBBED CAVITY')
    vessel('melt furnace',(-58,0,18),29,57)
    with at((-58,0,0)):
        for z in (30,41,52,63):g.trim('conformal furnace heater',z,30.5,30.5)
    tube('heated transfer',[(-36,0,57),(-13,0,67),(8,0,55),(16,0,46)],5,'cable')
    for x in (-82,73):
        for y in (-40,40):rod('frame leg',(x,y,8),(x,y,-12),3)
    box('machine sill',(-9,0,0),(199,108,11),10)
    box('process console',(-88,-31,74),(25,29,42),5);g.dial(-88,-47,78,7)
    mark('MELT FURNACE',(-58,-29,49),'VERIFIED ALLOY / TEMPERATURE HOLD')
    mark('TRANSFER',(-13,0,66),'HEATED LOW TURBULENCE PATH')
    return 26,27


def thread_doctor():
    with group('B'):
        for x in (-28,28):rod('micro loom rail',(x,-34,58),(x,34,58),2)
        for y in (-34,34):box('cloth clamp',(0,y,58),(69,11,13),3)
        for x in range(-25,26,5):g.wire('warp strand',[(x,-29,59),(x,29,59)],.15,'shell')
        for y in range(-25,26,5):
            if -7<y<8:continue
            g.wire('weft strand',[(-25,y,59),(25,y,59)],.15,'shell')
        for side in (-1,1):rod('tension screw',(side*36,-31,59),(side*36,31,59),1.5,'detail')
        mark('MICRO LOOM',(3,-20,59),'INDIVIDUAL CROSSINGS UNDER TENSION')
    with group('C'):
        optics((0,0,125),17,34,(0,0,-1))
        ring('inspection light',(0,0,89),23,4,5,role='accent')
        box('optical shuttle',(0,14,121),(48,27,24),6)
        for x in (-19,19):cyl('shuttle roller',(x,29,121),5,5,'detail',(0,1,0))
        rod('repair needle',(9,-8,81),(9,-8,63),.65,'detail')
        tube('yarn feed',[(23,13,122),(26,0,105),(10,-8,83)],.5,'cable')
        mark('OPTICAL SHUTTLE',(0,-13,106),'MATCHES YARN BEFORE REWEAVING')
    with at((0,0,0)):
        g.casting('desk machine base',[(0,64,53),(8,71,57),(16,67,54),(22,56,45)])
    for x in (-48,48):rod('loom support',(x,21,18),(x,21,59),3)
    for x in (-55,55):rod('optical gantry',(x,35,19),(x,35,144),4)
    rod('shuttle rail',(-55,35,126),(55,35,126),3)
    cyl('replacement yarn spool',(-49,-22,34),14,35,'detail')
    for z in (31,69):flange('spool cheek',(-49,-22,z),16,depth=2)
    box('operator focus control',(48,-29,36),(26,31,22),5)
    mark('YARN SPOOL',(-49,-35,50),'MATCHED FIBRE AND COLOUR')
    mark('FOCUS CONTROL',(49,-45,41),'HUMAN APPROVES THE REPAIR PATCH')
    return 26,26


def brick_return():
    with group('B'):
        for x in (-29,29):
            box('compliant jaw',(x,0,72),(14,62,35),5)
            box('jaw pad',(x+(-7 if x>0 else 7),0,73),(4,51,26),2,'accent')
            rod('jaw slide',(x,0,48),(x,0,96),3,'detail')
        for y in (-20,20):rod('jaw cross slide',(-49,y,47),(49,y,47),3)
        motor((50,0,48),11,25,(1,0,0))
        mark('COMPLIANT JAW',(25,-25,77),'SUPPORTS BRICK WITHOUT EDGE CRUSHING')
    with group('C'):
        box('separator head',(0,0,117),(67,44,24),6)
        for x in (-23,-11,1,13,25):rod('vibration chisel',(x,0,91),(x,0,106),1.8,'detail')
        motor((0,0,131),14,24)
        for x in (-29,29):rod('head tie',(x,-15,102),(x,-15,136),1.5,'detail')
        mark('MORTAR SEPARATOR',(0,-19,113),'CONTROLLED VIBRATION / LOCAL RELEASE')
    for x in (-53,53):truss((x,22,0),(x,22,157),9,8)
    box('gantry crown',(0,22,156),(126,29,13),6)
    box('brick',(0,0,69),(40,54,24),2,'shell')
    for y in (-55,55):
        for x in range(-38,39,13):cyl('conveyor roller',(x,y-15,27),5,30,'detail',(0,1,0))
        for x in (-46,46):rod('conveyor rail',(x,y-21,21),(x,y+21,21),3)
    box('dust tray',(0,0,6),(98,85,13),7)
    tube('dust extraction',[(29,18,109),(54,42,95),(53,48,36)],5,'cable')
    box('dust separator',(70,46,35),(39,45,69),7)
    mark('REUSABLE BRICK',(0,-27,71),'INTACT CERAMIC / MORTAR REMOVED')
    mark('DUST TRAY',(0,-43,12),'SEPARATE RECOVERED MINERAL FRACTION')
    return 26,25
