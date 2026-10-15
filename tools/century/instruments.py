"""Measurement architectures; illustrations of principles, never fabricated data plots."""
from .kit import *


def tripod(p=(0,0,0),height=70,radius=48):
    with at(p):
        cyl('tripod head',(0,0,height),16,8)
        for a in (0,120,240):
            with at(angle=a):
                rod('tripod leg',(11,0,height),(radius,0,0),3)
                rod('leg brace',(5,0,height*.35),(radius*.7,0,height*.25),1.2,'detail')
                box('adjustable foot',(radius,0,0),(19,19,5),3)


def hush_field():
    with group('B'):
        with at((-44,0,100),-12,'Z'):
            box('acoustic source tile',(0,0,0),(54,19,63),8)
            for x in (-14,14):
                for z in (-18,8):
                    ring('driver surround',(x,-11,z),10,2,2,(0,-1,0));cyl('driver diaphragm',(x,-13,z),7,.6,'accent',(0,-1,0),32)
            for x in (-22,22):cyl('mount screw',(x,-12,25),1.5,2,'detail',(0,-1,0),6)
        mark('SOURCE TILE',(-44,-13,100),'INDEPENDENTLY AIMED ACOUSTIC SOURCES')
    for x,a in ((17,0),(77,12)):
        with at((x,0,100),a,'Z'):
            box('source tile',(0,0,0),(54,19,63),8)
            for xx in (-14,14):
                for z in (-18,8):ring('driver surround',(xx,-11,z),10,2,2,(0,-1,0))
    with group('C'):
        rod('microphone stem',(-94,-18,0),(-94,-18,116),2)
        for a in (0,120,240):
            q=math.radians(a);p=(-94+23*math.cos(q),-18+23*math.sin(q),127)
            rod('microphone branch',(-94,-18,104),p,1)
            cyl('microphone capsule',p,3,7,'detail');ring('capsule mesh',Vector(p)+Vector((0,0,7)),3.5,.6,1,role='accent')
        box('microphone foot',(-94,-18,0),(31,29,6),4)
        mark('MICROPHONE TREE',(-94,-18,112),'LOCAL ERROR MEASUREMENTS')
    rod('source beam',(-70,8,63),(101,8,63),3)
    for x in (-46,77):tripod((x,9,0),60,29)
    box('adaptive controller',(13,16,20),(60,39,30),6)
    tube('tile bus',[(-45,11,78),(-21,25,62),(18,25,61),(77,11,78)],1,'cable')
    tube('microphone lead',[(-94,-18,6),(-61,-28,2),(14,3,7)],.8,'cable')
    mark('CONTROLLER',(13,-4,26),'LIMITS THE QUIET ZONE TO A MAPPED AREA')
    mark('AIMING BEAM',(76,8,65),'SOURCE ORIENTATION / NO SOUND DOME')
    return 23,22


def memory_kiln():
    with group('B'):
        optics((0,0,124),18,41,(0,0,-1))
        for z in (96,108):ring('objective focus band',(0,0,z),20,1,3,role='detail')
        box('objective carriage',(0,17,120),(51,25,34),5)
        for x in (-19,19):rod('focus screw',(x,9,87),(x,9,148),1.5,'detail')
        ring('objective illumination',(0,0,80),24,3,3,role='accent')
        mark('FOCUS OBJECTIVE',(0,-19,108),'ONE LENS WRITES AND READS')
    with group('C'):
        cyl('plate carousel',(0,0,33),48,6)
        for a in range(0,360,60):
            q=math.radians(a);x,y=31*math.cos(q),31*math.sin(q)
            box('glass archive plate',(x,y,40.2),(19,19,1.5),1,'accent')
            for dx in (-10,10):box('plate latch',(x+dx,y,42),(3,9,3),.7,'detail')
        flange('carousel bearing',(0,0,23),19);motor((0,0,3),12,19)
        mark('PLATE CAROUSEL',(27,-16,41),'SIX PLATES ON ONE TURNTABLE')
    with at((0,0,-9)):g.base(75,58)
    for x in (-54,54):rod('optical bridge column',(x,31,15),(x,31,153),4)
    box('optical bridge',(0,31,153),(132,33,15),7)
    box('pulse source',(-56,8,94),(27,46,56),6)
    tube('optical fibre',[(-54,0,123),(-37,18,162),(0,16,159),(1,16,139)],.7,'cable')
    box('decoding guide drawer',(52,-25,27),(41,34,12),4)
    for z in (24,27,30):box('archive guide leaf',(55,-35,z),(30,30,1),.2,'shell')
    mark('PULSE SOURCE',(-56,-16,103),'FIBRE-FED TO THE OPTICAL BRIDGE')
    mark('DECODING GUIDE',(53,-39,30),'THREE LEAVES IN A BASE DRAWER')
    return 26,26


def quasar_clock():
    with group('B'):
        box('trap vacuum chamber',(-24,0,61),(43,43,43),7)
        for axis in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1)):
            p=Vector((-24,0,61))+Vector(axis)*23
            cyl('vacuum optical port',p,12,12,'structure',axis);flange('viewport flange',p+Vector(axis)*13,16,axis,3)
            cyl('viewport',p+Vector(axis)*17,10,.5,'accent',axis)
        mark('TRAP CHAMBER',(-24,-37,61),'ULTRACOLD ATOMS IN A VACUUM')
    with group('C'):
        box('laser optical bench',(43,20,33),(76,74,6),5)
        for x,y in ((17,0),(48,0),(68,24),(37,41)):
            rod('optic post',(x,y,37),(x,y,52),2,'detail');optics((x,y,52),6,9,(1,0,0))
        box('laser cavity',(37,16,45),(33,17,16),3)
        for y in (12,19):rod('laser rail',(22,y,55),(51,y,55),.7,'detail')
        tube('fibre link',[(21,0,53),(4,-11,71),(-24,-38,62)],.6,'cable')
        mark('LASER BENCH',(48,0,56),'STABILISED OPTICAL REFERENCE')
    box('transport tray',(4,6,11),(175,126,20),12)
    for x in (-67,74):
        for y in (-44,54):cyl('isolation mount',(x,y,-3),9,16,'detail')
    for x in (-81,88):tube('carry handle',[(x,-17,9),(x*1.12,-17,22),(x*1.12,27,22),(x,27,9)],2)
    box('vacuum pump',(-47,43,38),(35,31,35),6)
    tube('pump connection',[(-48,27,38),(-46,10,35),(-24,0,34)],2,'detail')
    box('control front',(4,-51,31),(91,15,24),5)
    mark('VACUUM PUMP',(-47,44,52),'MAINTAINS THE TRAP ENVIRONMENT')
    mark('ISOLATION MOUNT',(74,-44,5),'RECOVERABLE REFERENCE AFTER TRAVEL')
    return 26,28


def stone_listener():
    with group('B'):
        box('contact shoe',(-46,-30,12),(38,31,21),6)
        cyl('contact transducer',(-46,-30,24),12,8,'detail')
        for x in (-60,-32):cyl('coupling adjuster',(x,-30,25),3,9,'detail',n=6)
        box('compliant interface',(-46,-30,0),(32,26,3),2,'accent')
        tube('shoe handle',[(-60,-30,28),(-60,-30,40),(-32,-30,40),(-32,-30,28)],1.5)
        mark('CONTACT SHOE',(-46,-31,24),'CONTROLLED CONTACT ON MASONRY')
    with group('C'):
        box('phased receiver',(37,0,15),(71,49,23),7)
        for x in (-1,0,1):
            for y in (-1,1):cyl('receiver element',(37+x*21,y*13,28),7,4,'accent')
        for x in (5,69):cyl('clamp screw',(x,0,28),2,4,'detail',n=6)
        tube('receiver grip',[(8,20,24),(8,20,41),(67,20,41),(67,20,24)],1.5)
        mark('PHASED RECEIVER',(38,-15,28),'MULTIPLE ACOUSTIC TRAVEL PATHS')
    for x,y in ((-43,38),(16,57)):
        box('secondary contact',(x,y,12),(32,27,21),6);cyl('transducer',(x,y,24),10,7,'detail')
        tube('contact cable',[(x,y,32),(x-4,y+13,43),(-5,21,64)],.8,'cable')
    tripod((-8,16,0),59,29);box('field computer',(-8,16,75),(47,35,25),6)
    tube('source cable',[(-46,-30,32),(-41,-10,50),(-8,3,66)],.8,'cable')
    tube('receiver cable',[(39,20,26),(28,39,51),(-8,29,68)],.8,'cable')
    for x in (-74,-24,26,76):box('masonry course',(x,18,-12),(47,113,19),3,'shell')
    mark('FIELD COMPUTER',(-8,-3,78),'INVERSION WITH UNCERTAINTY')
    mark('MASONRY',(51,-30,-5),'EXISTING STRUCTURE / NO DRILLING')
    return 25,31


def dark_bloom():
    with group('B'):
        cyl('filter wheel',(0,0,111),28,5)
        for a in range(0,360,60):
            q=math.radians(a);x,y=18*math.cos(q),18*math.sin(q)
            ring('filter cell',(x,y,117),7,1.5,2);cyl('spectral filter',(x,y,117),5.5,.5,'accent')
        motor((0,0,84),11,23);ring('wheel guard',(0,0,110),31,2,8)
        mark('FILTER WHEEL',(14,-14,118),'REGISTERED SPECTRAL PASSBANDS')
    with group('C'):
        cyl('cold finger',(0,0,51),7,30,'detail')
        box('detector cold stage',(0,0,82),(25,25,5),2,'accent')
        for z in (54,61,68):ring('thermal shield',(0,0,z),15,2,3,role='detail')
        cyl('cooler body',(0,0,27),16,23)
        for x in (-16,16):rod('cooler mount',(x,-7,26),(x,7,26),2)
        mark('COLD FINGER',(0,-9,69),'LOW NOISE DETECTOR SUPPORT')
    for a in range(0,360,60):
        q=math.radians(a);p=Vector((43*math.cos(q),43*math.sin(q),99));axis=Vector((math.cos(q)*.5,math.sin(q)*.5,.87))
        optics(p,12,31,axis);rod('optical branch',(0,0,91),p,3)
        tube('channel fibre',[p,p+Vector((0,0,-19)),(0,0,78)],.5,'cable')
    tripod((0,0,-19),50,50)
    box('logger',(-31,17,25),(33,26,32),5)
    mark('APERTURE',(45,-24,121),'PASSIVE OBSERVATION / NO ILLUMINATION')
    mark('LOGGER',(-31,3,25),'REGISTERED CHANNEL COMPARISON')
    return 24,26


def gravity_pencil():
    with group('B'):
        box('atom source chamber',(0,0,131),(38,38,37),6)
        for axis in ((1,0,0),(-1,0,0),(0,-1,0),(0,1,0)):
            p=Vector((0,0,131))+Vector(axis)*21;flange('source viewport',p,13,axis,4);cyl('window',p+Vector(axis)*5,8,.7,'accent',axis)
        cyl('source oven',(0,25,132),8,25,'detail',(0,1,0))
        mark('ATOM SOURCE',(0,-24,132),'LASER COOLED ATOMIC CLOUD')
    with group('C'):
        with at(angle=-35):
            rod('isolation leg',(12,0,61),(57,0,0),4)
            cyl('levelling foot',(57,0,0),11,8)
            for z in (12,16,20,24):ring('isolation bellows',(48,0,z),6,1,2,role='detail')
            rod('adjusting spindle',(57,0,9),(57,0,24),2,'detail')
            ring('levelling wheel',(57,0,24),7,1,2)
        mark('ISOLATION LEG',(45,-32,11),'VIBRATION AND TILT CONTROL')
    for a in (85,205):
        with at(angle=a):rod('tripod leg',(12,0,61),(57,0,0),4);cyl('foot',(57,0,0),11,8)
    cyl('interferometer tube',(0,0,51),17,61)
    for z in (53,108):flange('vacuum coupling',(0,0,z),21,depth=4)
    for z in (66,91):ring('magnetic shield band',(0,0,z),20,1,5,role='detail')
    box('reference mirror stage',(0,0,43),(40,40,9),5)
    box('laser controller',(39,29,88),(32,38,55),6)
    tube('optical lead',[(39,8,93),(24,-1,116),(0,-25,132)],.6,'cable')
    mark('FALL TUBE',(0,-18,81),'INTERFEROMETRIC GRAVITY MEASUREMENT')
    mark('MIRROR STAGE',(0,-21,44),'MECHANICAL REFERENCE UNDER THE CLOUD')
    return 26,23


def spectrum_harp():
    with group('B'):
        box('grating carriage',(0,0,40),(37,37,13),5)
        with at((0,0,53),23,'Y'):
            box('diffraction grating',(0,0,0),(27,3,29),2,'accent')
            for x in range(-11,12,2):rod('grating ruling',(x,-2,-12),(x,-2,12),.13,'shell')
        cyl('grating rotary stage',(0,0,28),24,6);bolts((0,0,35),19,8,size=1)
        motor((0,24,31),7,18,(0,1,0))
        mark('GRATING CARRIAGE',(0,-4,56),'ANGLE SELECTED SPECTRAL DISPERSION')
    with group('C'):
        cyl('sample cell',(-53,-26,48),12,27,'structure',(1,0,0))
        for x in (-55,-25):flange('cell window',(x,-26,48),15,(1,0,0),3)
        for x in (-48,-31):cyl('fluid port',(x,-26,59),3,9,'detail')
        for y in (-37,-15):rod('cell foot',(-39,y,22),(-39,y,44),2)
        mark('SAMPLE CELL',(-39,-37,50),'SMALL SEALED OPTICAL SAMPLE')
    box('optical bed',(0,0,13),(158,117,17),11)
    for x,y,angle in ((-43,28,25),(48,28,-25),(51,-30,90)):
        with at((x,y,48),angle):
            rod('optic mount',(0,0,-26),(0,0,0),3)
            box('fold mirror',(0,0,0),(21,3,25),2,'detail')
            for xx in (-8,8):cyl('adjuster',(xx,4,-6),2,7,'detail',(0,1,0),16)
    optics((62,-30,48),10,23,(-1,0,0))
    tube('carry bow',[(-80,0,8),(-85,0,80),(85,0,80),(80,0,8)],2.5)
    box('detector electronics',(51,-28,30),(39,39,16),4)
    mark('FOLD MIRROR',(48,28,52),'COMPACT OPTICAL PATH')
    mark('DETECTOR',(58,-30,49),'CALIBRATED INTENSITY READOUT')
    return 26,30


def fault_lantern():
    with group('B'):
        box('shearography camera',(0,0,107),(69,43,41),8)
        for x in (-16,16):optics((x,-24,107),11,22)
        for x in (-29,29):cyl('front captive screw',(x,-23,121),1.6,2,'detail',(0,-1,0),6)
        rod('camera gimbal',(-41,0,105),(41,0,105),4)
        joint((-41,-4,105),8)
        mark('SHEAROGRAPHY HEAD',(0,-43,110),'COMPARES SURFACE MOTION UNDER LOAD')
    with group('C'):
        box('reference stage',(56,8,91),(29,28,9),4)
        rod('mirror post',(56,8,95),(56,8,117),2)
        ring('reference mirror',(56,5,120),12,2,5,(0,-1,0));cyl('mirror face',(56,-1,120),10,.4,'accent',(0,-1,0))
        for x in (47,65):rod('fine adjuster',(x,10,109),(x,10,124),1,'detail')
        mark('REFERENCE MIRROR',(57,-2,120),'STABLE INTERFEROMETRIC REFERENCE')
    tripod((0,0,0),74,58)
    for x in (-41,41):rod('camera yoke',(x,0,81),(x,0,105),3)
    box('laser source',(-47,23,92),(31,34,31),5)
    tube('fibre link',[(-46,5,98),(-32,-3,135),(15,8,137),(21,16,124)],.7,'cable')
    box('field controller',(0,33,39),(57,32,26),6)
    for x in (-21,21):rod('controller mount',(x,18,49),(x,0,72),2)
    mark('LASER SOURCE',(-47,5,100),'COHERENT ILLUMINATION')
    mark('FIELD CONTROLLER',(0,15,42),'REFERENCE / LOADED PAIR COMPARISON')
    return 25,23


def neutrino_bell():
    views(B=(10,-25))
    # Open section of a pressure housing reveals many photon sensors on one cage.
    with group('B'):
        p=Vector((0,-27,59));axis=Vector((0,-.7,-.7))
        optics(p,14,25,axis)
        box('sensor readout',(0,-16,66),(23,19,13),3,'detail')
        for x in (-7,7):tube('sensor lead',[(x,-22,70),(x,-11,88),(x,0,97)],.4,'cable')
        mark('PHOTON SENSOR',(0,-46,42),'REGISTERS LIGHT FROM DETECTOR MEDIUM')
    with group('C'):
        cyl('calibration head',(0,0,120),14,16)
        for a in range(0,360,60):
            q=math.radians(a);cyl('calibration emitter',(13*math.cos(q),13*math.sin(q),127),3,4,'accent',(math.cos(q),math.sin(q),0),16)
        flange('cable penetrator',(0,0,138),17,depth=3)
        tube('calibration feed',[(0,0,143),(0,0,157),(15,0,161),(23,0,150)],1.4,'cable')
        mark('CALIBRATION FEED',(0,-12,129),'FED THROUGH A TOP PENETRATOR')
    for a in (60,120,180,240,300):
        q=math.radians(a);p=Vector((27*math.sin(q),-27*math.cos(q),59));axis=Vector((math.sin(q)*.7,-math.cos(q)*.7,-.7))
        optics(p,14,25,axis);rod('sensor cage stay',(0,0,98),p,2,'detail')
    for a in (0,120,240):
        q=math.radians(a);optics((20*math.cos(q),20*math.sin(q),89),11,19,(math.cos(q)*.8,math.sin(q)*.8,.6))
    for z,r in ((32,30),(65,48),(106,36)):ring('housing datum',(0,0,z),r,1,2,role='shell')
    # One sectioned transparent dome; no opaque sphere hiding all the sensors.
    g.shell('pressure housing section',51,45,101,25,190,'shell')
    ring('equatorial clamp',(0,0,69),53,2,6);bolts((0,0,76),50,16,size=1)
    for z in (83,95):cyl('readout board',(0,0,z),25,1,'detail')
    mark('READOUT',(0,-21,97),'TIME TAGGED LOW LIGHT SIGNALS')
    mark('PRESSURE HOUSING',(44,14,76),'SECTIONED SENSOR MODULE / MEDIUM OMITTED')
    return 25,24


def echo_cartographer():
    with group('B'):
        joint((0,0,78),17,(0,0,1))
        for x in (-24,24):rod('sensor fork',(x,0,77),(x,0,112),3)
        box('sensor head',(0,0,106),(42,35,31),7)
        for x in (-11,11):optics((x,-19,107),7,12)
        for x in (-15,0,15):cyl('acoustic receiver',(x,-20,95),3.5,4,'accent',(0,-1,0),24)
        mark('SENSOR GIMBAL',(0,-31,107),'LIGHT AND ACOUSTIC RANGE CHANNELS')
    with group('C'):
        cyl('retractable wheel',(-44,-33,19),19,11,'structure',(0,-1,0))
        flange('wheel hub',(-44,-45,19),10,(0,-1,0),3)
        rod('wheel swing arm',(-44,-33,19),(-23,-27,47),4)
        joint((-23,-30,47),7);rod('deployment ram',(-12,-28,48),(-36,-32,25),2,'detail')
        mark('RETRACTABLE WHEEL',(-44,-46,20),'NARROW MODE FOR TIGHT PASSAGES')
    for x,y in ((44,-33),(-44,33),(44,33)):
        cyl('wheel',(x,y,19),19,11,'structure',(0,-1 if y<0 else 1,0));rod('swing arm',(x,y,19),(x*.55,y*.82,47),4)
        flange('wheel hub',(x,y+(-12 if y<0 else 12),19),10,(0,-1 if y<0 else 1,0),3)
        joint((x*.55,y*.9,47),7);rod('deployment ram',(x*.27,y*.85,48),(x*.82,y*.97,25),2,'detail')
    hull('survey rover',[(-67,8,7,48),(-44,28,19,48),(44,28,19,48),(67,8,7,48)])
    for x in (-42,42):box('service lid',(x,0,67),(23,31,4),4,'detail')
    tube('rescue handle',[(-29,21,62),(-29,26,76),(29,26,76),(29,21,62)],2)
    cyl('tether reel',(48,6,70),12,17,'detail',(1,0,0))
    tube('recovery tether',[(63,6,73),(76,15,54),(81,36,21)],.6,'cable')
    mark('RECOVERY REEL',(63,6,72),'PHYSICAL RETURN OPTION')
    mark('SERVICE LID',(-43,0,69),'BATTERY AND MAP STORAGE')
    return 25,24
