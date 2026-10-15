"""Water collection, treatment and transport; each mechanism keeps its own silhouette."""
from .kit import *


def dew_crown():
    with group('B'):
        with at(angle=-45):
            leaf('condensing leaf',(17,0,91),(102,0,135),44,'accent')
            tube('leaf drainage spine',[(17,0,89),(48,0,103),(99,0,132)],.7,'detail')
            for x in (35,55,75):
                for side in (-1,1):tube('capillary groove',[(x+10,side*14,103+(x-35)*.5),(x,0,97+(x-35)*.5)],.2,'shell')
            joint((21,-4,94),5);rod('leaf stay',(15,0,73),(52,0,108),2)
        mark('CONDENSING LEAF',(58,-58,121),'TEXTURED RADIATIVE SURFACE')
    for a in (15,75,135,195,255):
        with at(angle=a):
            leaf('condensing leaf',(17,0,91),(102,0,135),44,'accent');rod('leaf stay',(15,0,73),(52,0,108),2)
    with group('C'):
        ring('collection lip',(0,0,93),24,3,8)
        hull('collection funnel',[(-12,7,7,0),(0,24,24,0)],'X')
        # Orient funnel to vertical throat without independent projection tricks.
        o=g.parts[-1][0];o.matrix_world=Matrix.Translation((0,0,83))@Matrix.Rotation(-math.pi/2,4,'Y')
        cyl('filter cartridge',(0,0,52),11,24)
        for z in (56,72):flange('filter cap',(0,0,z),13,depth=2)
        tube('filtered drop',[(0,0,53),(0,0,36),(0,-12,24)],2,'cable')
        mark('COLLECTION THROAT',(0,-12,68),'SCREEN BEFORE STORAGE')
    for a in (0,120,240):
        with at(angle=a):rod('mast leg',(16,0,89),(42,0,0),3);box('ground plate',(42,0,0),(25,20,4),3)
    vessel('water cistern',(0,0,2),24,32)
    cyl('draw off spout',(0,-29,14),4,13,'detail',(0,-1,0))
    mark('CISTERN',(0,-23,21),'COVERED DRINKING WATER RESERVE')
    mark('MAST',(28,0,43),'FOLDS DOWN FOR SERVICE')
    return 24,25


def river_sieve():
    for y in (-56,56):
        hull('flotation pontoon',[(-101,2,2,13),(-84,16,16,13),(78,16,16,13),(101,4,4,13)])
        g.parts[-1][0].location.y=y
    for x in (-67,67):rod('deck bearer',(x,-60,31),(x,60,31),4)
    box('service deck',(0,0,36),(161,117,5),5)
    with group('B'):
        cyl('membrane drum',(-46,0,63),25,91,'structure',(1,0,0))
        for x in (-48,47):flange('drum end',(x,0,63),28,(1,0,0),3)
        for x in range(-40,42,9):ring('membrane support hoop',(x,0,63),26,1,2,(1,0,0),'detail')
        for y in (-1,1):rod('drum support',(-28,y*22,46),(32,y*22,46),3,'detail')
        motor((50,0,63),12,22,(1,0,0))
        mark('MEMBRANE DRUM',(-5,-25,65),'CROSS FLOW FILTRATION MODULE')
    with group('C'):
        pump((-59,-36,48),.6)
        rod('backwash header',(-59,-36,59),(38,-36,59),4)
        for x in (-25,10,36):
            cyl('backwash valve',(x,-36,63),5,9,'detail');ring('valve wheel',(x,-36,74),7,1,2,role='accent')
        flange('inlet coupling',(-77,-36,49),8,(-1,0,0))
        mark('BACKWASH VALVE',(9,-36,75),'REVERSE CLEANING PULSE')
    for x in (-76,76):rod('handrail post',(x,49,38),(x,49,71),1.5,'detail')
    rod('handrail',(-76,49,71),(76,49,71),1.5,'detail')
    tube('inlet hose',[(-70,-39,43),(-91,-47,31),(-106,-55,0)],3,'cable')
    box('control chest',(58,35,58),(39,30,36),6)
    mark('PONTOON',(28,-57,17),'SHALLOW DRAFT SERVICE RAFT')
    mark('CONTROL CHEST',(58,19,64),'FILTER PRESSURE AND WATER QUALITY')
    return 26,25


def brine_garden():
    with group('B'):
        for x in (-33,0,33):
            box('ion separation cassette',(x,14,82),(24,54,75),5)
            for z in range(52,114,9):rod('membrane support',(x-9,-14,z),(x+9,-14,z),.7,'detail')
            for y in (-8,34):cyl('cassette port',(x,y,122),4,9,'accent')
        box('cassette carrier',(0,14,40),(119,65,9),5)
        mark('ION CASSETTES',(0,-15,83),'SELECTIVE RECOVERY STAGES')
    with group('C'):
        for z in (10,28):
            box('precipitation pan',(0,-42,z),(111,59,5),5)
            for x in (-53,53):box('tray lip',(x,-42,z+5),(4,59,10),1,'detail')
            for y in (-69,-15):box('tray end',(0,y,z+5),(106,4,10),1,'detail')
            for x in (-36,-12,12,36):rod('settling baffle',(x,-65,z+6),(x,-19,z+6),1,'detail')
        for x in (-51,51):rod('tray upright',(x,-14,4),(x,-14,45),2)
        mark('SETTLING TRAY',(23,-52,34),'SEPARATE MINERAL FRACTIONS')
    for side in (-1,1):
        vessel('reagent vessel',(side*78,18,11),16,49)
        tube('metered reagent',[(side*78,-1,45),(side*66,-15,64),(side*40,-8,119)],1.4,'cable')
        pump((side*73,-32,14),.42)
    skid(195,126)
    rod('overflow return',(-50,47,38),(52,47,38),5)
    mark('REAGENT VESSEL',(-79,2,38),'CONTROLLED PRECIPITATION CHEMISTRY')
    mark('RETURN HEADER',(42,47,39),'RESIDUAL BRINE TO CLOSED PROCESS')
    return 26,26


def ice_stitcher():
    for y in (-39,39):
        tube('curved sled runner',[(-93,y,9),(-78,y,0),(73,y,0),(94,y,12)],3)
        for x in (-58,55):rod('sled stay',(x,y,2),(x,y*.75,22),3)
    hull('water tank',[(-56,12,12,48),(-40,30,27,48),(34,30,27,48),(56,12,12,48)])
    with group('B'):
        box('freeze shoe',(88,0,6),(48,50,10),7)
        for x in range(71,108,6):rod('shoe microchannel',(x,-20,12),(x,20,12),.6,'accent')
        for y in (-15,15):rod('shoe link',(42,y,25),(88,y,18),2.5);joint((88,y,18),4)
        tube('shoe cooling tube',[(70,-20,14),(106,-20,14),(106,20,14),(70,20,14)],1.2,'detail')
        mark('FREEZE SHOE',(90,-17,12),'LAYERED ICE REPAIR HEAD')
    with group('C'):
        pump((-71,0,25),.55)
        for x in (-83,-60):cyl('metering valve',(x,0,46),5,11,'detail')
        box('flow sensor',(-58,-14,38),(15,18,16),2)
        tube('metering return',[(-76,0,47),(-61,-15,49),(-49,-17,46)],1.4,'accent')
        mark('METERING PUMP',(-72,-10,34),'SMALL DOSES / NO OPEN FLOODING')
    tube('delivery hose',[(-61,-12,31),(-20,-35,26),(57,-29,26),(87,-16,17)],2,'cable')
    for x in (-32,29):ring('tank strap',(x,0,48),31,1.5,5,(1,0,0),'detail')
    for y in (-29,29):rod('push handle',(30,y,21),(54,y,86),2)
    rod('handle grip',(54,-29,86),(54,29,86),2)
    mark('WATER TANK',(0,-30,50),'INSULATED PROCESS WATER')
    mark('PUSH HANDLE',(54,-16,86),'GLOVED OPERATOR ACCESS')
    return 26,26


def flood_lung():
    # Elevated pump with a large flexible suction throat and external hose reel.
    with group('B'):
        ring('impeller bell',(0,0,25),38,5,26)
        rotor((0,0,31),31,6)
        motor((0,0,62),19,40)
        for a in (0,120,240):
            q=math.radians(a);rod('motor support',(33*math.cos(q),33*math.sin(q),51),(14*math.cos(q),14*math.sin(q),65),2)
        mark('IMPELLER BELL',(0,-32,38),'LOW HEAD / HIGH VOLUME FLOW')
    with group('C'):
        rod('discharge elbow',(28,0,47),(64,0,47),12)
        flange('quick coupling',(64,0,47),18,(1,0,0),7)
        for y in (-18,18):
            rod('cam lock',(66,y,40),(77,y,59),2,'detail');joint((65,y,45),4,(0,1,0))
        ring('gasket seat',(72,0,47),14,2,2,(1,0,0),'accent')
        mark('HOSE COUPLING',(71,-13,48),'TWIN CAM LOCK / CAPTIVE SEAL')
    for a in (0,120,240):
        with at(angle=a):rod('elevating leg',(28,0,59),(65,0,-29),4);box('mud plate',(65,0,-31),(39,34,5),5)
    ring('suction cage',(0,0,-27),32,2,47)
    for a in range(0,360,30):
        q=math.radians(a);rod('debris bar',(31*math.cos(q),31*math.sin(q),-24),(31*math.cos(q),31*math.sin(q),19),1,'detail')
    for x in (-1,1):tube('lift handle',[(x*22,-15,83),(x*35,-15,110),(x*35,15,110),(x*22,15,83)],2)
    box('power module',(-53,29,58),(32,38,53),6)
    mark('SUCTION CAGE',(0,-31,-9),'COARSE DEBRIS SCREEN')
    mark('POWER MODULE',(-53,8,64),'SEALED MOTOR DRIVE')
    return 25,22


def mist_spire():
    with group('B'):
        panel('fog fibre mesh',(0,0,119),(99,79),(0,-1,0),nx=16,ny=13,role='shell')
        for x in (-49,49):rod('mesh tension post',(x,0,79),(x,0,162),2.5)
        for z in (79,161):rod('mesh beam',(-49,0,z),(49,0,z),2.5)
        for x in (-36,-12,12,36):tube('drip fibre',[(x,-2,160),(x+2,-3,120),(x,-2,81)],.2,'accent')
        mark('FIBRE PANEL',(10,-2,126),'POROUS DROPLET INTERCEPTION')
    with group('C'):
        box('drip gutter',(0,0,74),(113,17,8),3)
        for x in (-50,50):box('gutter bracket',(x,2,72),(8,23,18),2)
        rod('gutter outlet',(37,0,70),(37,0,55),4)
        flange('gutter union',(37,0,53),7)
        tube('downpipe elbow',[(37,0,55),(37,7,45),(13,12,33)],2.5,'cable')
        mark('GUTTER JOINT',(37,-5,62),'SEALED DRAIN TO CISTERN')
    for x in (-49,49):truss((x,6,0),(x,6,80),7,5)
    for x in (-1,1):
        with at((x*66,15,114),x*22,'Z'):panel('wing mesh',(0,0,0),(31,72),(0,-1,0),nx=6,ny=12,role='shell')
        rod('guy wire',(x*48,6,153),(x*95,42,0),.45,'detail');box('guy anchor',(x*95,42,0),(21,25,4),3)
    vessel('covered cistern',(0,20,0),27,38)
    mark('CISTERN',(0,-8,25),'COVERED COLLECTION RESERVE')
    mark('GUY WIRE',(-75,26,62),'WIND LOAD TO GROUND ANCHOR')
    return 20,20


def well_warden():
    with group('B'):
        rod('sensor mandrel',(0,0,13),(0,0,133),5)
        for z in (22,55,88,119):
            cyl('sensor capsule',(0,0,z),10,17)
            for dz in (2,13):ring('capsule seal',(0,0,z+dz),11,1,2,role='detail')
            for a in range(0,360,60):
                q=math.radians(a);cyl('sensor port',(8*math.cos(q),8*math.sin(q),z+8),2,3,'accent',(math.cos(q),math.sin(q),0),16)
        mark('SENSOR STRING',(0,-10,83),'DEPTH RESOLVED WATER MONITORING')
    with group('C'):
        flange('well cap',(0,0,150),28)
        cyl('cable gland',(0,0,155),10,14,'detail',n=6)
        ring('gland nut',(0,0,168),12,3,5)
        for x in (-19,19):rod('cap handle',(x,-7,156),(x,7,156),2,'detail')
        tube('cable loop',[(0,0,174),(9,12,188),(29,16,188),(40,18,174)],1,'cable')
        mark('CABLE SEAL',(0,-9,168),'REMOVABLE PRESSURE CAP')
    # Half casing exposes the sensor string; this is a physical cutaway view.
    g.shell('sectioned well casing',24,0,150,35,205)
    box('wellhead pad',(0,0,-3),(87,87,7),6)
    rod('logger mast',(55,20,0),(55,20,150),3)
    box('logger cabinet',(55,19,131),(37,28,42),6)
    panel('power canopy',(55,20,162),(72,58),nx=8,ny=6)
    mark('LOGGER',(55,4,137),'TREND STORAGE / REMOTE ALARM')
    mark('CASING',(20,10,46),'SECTIONED OBSERVATION WELL')
    return 26,23


def blue_loop():
    with group('B'):
        for x in (-33,0,33):
            cyl('biofilm cartridge',(x,11,25),12,66)
            for z in range(31,88,6):ring('biofilm support',(x,11,z),12.5,.7,1,role='detail')
            flange('cartridge cap',(x,11,92),15,depth=3)
            rod('feed riser',(x,11,97),(x,11,108),3)
        rod('cartridge header',(-40,11,108),(40,11,108),5)
        mark('BIOFILM CARTRIDGE',(-31,-2,62),'FIRST STAGE ORGANIC LOAD REMOVAL')
    with group('C'):
        box('diverter body',(60,-20,53),(31,44,42),6)
        for z in (42,64):
            for side in (-1,1):flange('diverter port',(60+side*18,-20,z),7,(side,0,0),3)
        cyl('diverter actuator',(60,-20,76),12,21)
        for y in (-31,-9):cyl('inspection screw',(60,y,98),2,2,'detail',n=6)
        mark('DIVERTER',(61,-42,54),'REUSE SUPPLY IS A SEPARATE LINE')
    vessel('buffer tank',(-73,15,7),23,72)
    box('curved service plinth',(0,10,6),(209,88,13),9)
    for x in (-56,47):rod('protective frame',(x,37,13),(x,37,120),2.5)
    rod('frame crown',(-56,37,120),(47,37,120),2.5)
    pump((16,-35,15),.5)
    tube('filter feed',[(-73,-9,48),(-61,-23,30),(14,-27,26)],2,'cable')
    tube('clean return',[(36,11,108),(58,11,114),(66,-15,99)],1.8,'accent')
    mark('BUFFER TANK',(-73,-9,44),'GREYWATER INPUT / NO POTABLE CLAIM')
    mark('CIRCULATION PUMP',(16,-43,26),'CONTROLLED FILTER RECIRCULATION')
    return 26,25


def silt_heron():
    # Four symmetric articulated legs; sampled foot and actual core share the model.
    with group('B'):
        cyl('core barrel',(0,-25,4),8,78)
        ring('core mouth',(0,-25,3),9,1.2,4)
        motor((0,-25,84),13,25)
        for z in (23,62):flange('core guide',(0,-25,z),12,depth=3)
        rod('barrel slide',(17,-25,20),(17,-25,103),2,'detail')
        mark('CORE BARREL',(0,-33,47),'SHORT UNDISTURBED SEDIMENT SAMPLE')
    with group('C'):
        box('broad sediment foot',(-69,-50,0),(44,47,5),8)
        for x in (-83,-69,-55):rod('foot stiffener',(x,-67,3),(x,-33,3),.7,'detail')
        joint((-69,-50,8),7);rod('ankle neck',(-69,-50,8),(-63,-44,23),3)
        mark('BROAD FOOT',(-68,-57,3),'LOW PRESSURE ON SOFT MUD')
    hull('instrument body',[(-40,12,9,88),(-24,30,19,88),(24,30,19,88),(40,12,9,88)])
    for x in (-1,1):
        for y in (-1,1):
            hip=(x*25,y*18,81);knee=(x*64,y*41,49);ankle=(x*69,y*50,8)
            rod('upper leg',hip,knee,4);joint(knee,7);rod('lower leg',knee,ankle,3)
            if (x,y)!=(-1,-1):box('broad sediment foot',(x*69,y*50,0),(44,47,5),8);joint(ankle,7)
            tube('leg cable',[hip,(x*66,y*45,51),(x*71,y*50,18)],.65,'cable')
    optics((0,-31,91),7,13);panel('dorsal power panel',(0,0,117),(70,60),nx=7,ny=6)
    mark('NAVIGATION',(0,-44,91),'REED ROOT AVOIDANCE')
    mark('LEG JOINT',(64,-41,49),'QUASI STATIC SUPPORT GAIT')
    return 24,22


def cloud_cistern():
    # Long lifting envelope with a genuinely suspended tank cradle and winch deck.
    envelope=hull('lifting envelope',[(-144,2,2,145),(-121,25,30,145),(-70,43,47,145),(43,45,49,145),(111,26,31,145),(147,2,2,145)])
    for x,r in ((-92,36),(-36,45),(31,45),(90,35)):
        hull_seam(envelope,x,'shell')
    with group('B'):
        for x in (-43,29):
            vessel('water transport tank',(x,0,14),23,58)
            for y in (-20,20):rod('cradle hoop',(x-23,y,16),(x+23,y,16),2)
        for y in (-26,26):rod('cradle sill',(-72,y,8),(63,y,8),3)
        for x in (-69,61):rod('cradle crossmember',(x,-29,8),(x,29,8),3)
        mark('TANK CRADLE',(26,-23,44),'SWAPPABLE WATER PAYLOADS')
    with group('C'):
        cyl('lowering drum',(-17,0,81),12,34,'structure',(1,0,0))
        for x in (-20,19):flange('drum cheek',(x,0,81),16,(1,0,0),3)
        motor((23,0,81),9,19,(1,0,0))
        for x in (-24,21):box('winch bearing',(x,0,75),(8,28,23),3)
        box('winch deck',(0,0,68),(90,55,6),4)
        mark('LOWERING WINCH',(0,-12,83),'LOAD TRANSFER ON PREPARED PAD')
    for x in (-67,58):
        for y in (-24,24):rod('suspension cable',(x,y,116),(x,y,13),.7,'detail')
    for side in (-1,1):
        with at((75,side*58,124)):
            ring('vector thruster',(0,-6,0),15,3,16,(0,1,0));rotor((0,0,0),11,4,(0,1,0))
        rod('thruster pylon',(77,side*33,130),(75,side*58,124),3)
    for side in (-1,1):leaf('tail fin',(111,side*12,147),(141,side*57,153),34,'shell')
    mark('VECTOR THRUSTER',(75,-64,124),'LOW SPEED STATION KEEPING')
    mark('ENVELOPE',(-51,-42,158),'BUOYANT LIFT / WEATHER LIMITED')
    return 23,18
