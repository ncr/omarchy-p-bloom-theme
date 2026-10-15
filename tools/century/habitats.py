"""Deployable shelter, building components and civic infrastructure."""
from .kit import *


def storm_petal():
    with group('B'):
        for x in (-54,54):
            cyl('petal hinge',(x,-35,8),6,70,'structure',(0,1,0))
            for y in (-31,0,31):ring('hinge bearing',(x,y,8),8,2,5,(0,1,0),'detail')
            rod('opening ram',(x,0,7),(x*1.34,0,38),3,'detail')
            joint((x*1.34,-4,38),5)
        mark('PETAL HINGE',(-57,-21,9),'RIGID SHELL / CONTROLLED DEPLOYMENT')
    with group('C'):
        box('floor cassette',(0,0,0),(119,141,10),8)
        tube('floor perimeter seal',[(-51,-61,6),(51,-61,6),(51,61,6),(-51,61,6),(-51,-61,6)],1.2,'accent')
        for x in (-45,45):
            for y in (-48,48):box('floor latch',(x,y,8),(9,17,6),2,'detail')
        for y in range(-49,50,14):rod('floor seam',(-47,y,6),(47,y,6),.3,'shell')
        mark('FLOOR SEAL',(42,-61,7),'CONTINUOUS WEATHER BARRIER')
    # Two curved shell petals opened around the same floor, with shaped roof spine.
    for side in (-1,1):
        vs=[];fs=[]
        for j in range(15):
            t=j/14;x=side*(55+32*math.sin(t*math.pi*.55));z=8+90*t
            for y in (-65,65):vs.append((x,y,z))
        for j in range(14):fs.append((j*2,j*2+1,j*2+3,j*2+2))
        g.mesh('rigid shelter petal',vs,fs,'structure')
        for y in (-64,0,64):tube('petal rib',[(side*55,y,8),(side*75,y,54),(side*87,y,98)],1.3,'detail')
    truss((0,-66,117),(0,66,117),11,8)
    for y in (-66,66):
        rod('roof arch',(-86,y,99),(0,y,117),2);rod('roof arch',(0,y,117),(86,y,99),2)
        rod('end post',(0,y,8),(0,y,112),3)
    box('service spine',(0,53,37),(31,21,57),6)
    for x in (-39,39):box('ground shoe',(x,49,-10),(27,32,10),4)
    mark('ROOF SPINE',(0,0,118),'TRANSPORT AND WEATHER LOAD PATH')
    mark('SERVICE SPINE',(0,41,38),'HEAT / AIR / LOCAL POWER')
    return 25,24


def lunar_porch():
    # Rear-entry suit interface on an exterior porch; the clean boundary is explicit.
    with group('B'):
        box('suit dock backplate',(0,-11,85),(64,17,89),12)
        tube('suitport seal',[(-24,-22,49),(-24,-22,118),(-16,-22,129),(16,-22,129),(24,-22,118),(24,-22,49),(-24,-22,49)],1.5,'accent')
        for x in (-31,31):
            for z in (63,105):box('port latch',(x,-23,z),(9,11,18),3)
        ring('air connection',(-22,-25,77),6,2,4,(0,-1,0));ring('data connection',(22,-25,77),5,1,4,(0,-1,0),'detail')
        mark('SUIT DOCK',(0,-22,99),'FOUR LATCHES / AIR AND DATA LINES')
    with group('C'):
        box('dust grate',(0,-44,12),(87,67,8),5)
        for x in range(-34,35,7):rod('grate bar',(x,-71,17),(x,-17,17),.8,'detail')
        box('dust trap drawer',(0,-44,1),(81,59,13),5)
        rod('drawer handle',(-12,-77,4),(12,-77,4),1.5,'detail')
        for x in (-35,35):rod('drawer rail',(x,-69,3),(x,-19,3),1.2,'detail')
        mark('DUST TRAP',(0,-72,13),'GRATE UNDERFOOT / DRAWER BELOW')
    ring('habitat bulkhead',(0,12,81),78,10,19,(0,1,0))
    for a in range(0,360,30):
        q=math.radians(a);cyl('bulkhead bolt',(71*math.cos(q),10,81+71*math.sin(q)),2,4,'detail',(0,-1,0),6)
    # Both posts stand on the grate's edge, not beside it in the air.
    for x in (-42,42):rod('handrail',(x,-61,16),(x,-61,105),2);rod('handrail return',(x,-61,105),(x,-16,105),2)
    box('exterior utility chest',(63,-25,53),(29,38,61),7)
    tube('service umbilical',[(64,-15,83),(49,-28,116),(22,-25,99)],1.2,'cable')
    mark('BULKHEAD',(-63,12,119),'PRESSURE BOUNDARY / 12 BOLTS')
    mark('UTILITY CHEST',(63,-45,61),'SUIT PURGE AND SERVICE')
    return 25,20


def heat_window():
    with group('B'):
        # Three real layers staggered at an exposed top edge, not an invented heat map.
        for y in (-4,0,4):
            panel('optical laminate',(0,y,93),(94,132),(0,-1,0),nx=6,ny=8,role='shell')
        for x in (-49,49):rod('laminate edge',(x,0,24),(x,0,160),2)
        for z in (25,159):rod('laminate edge',(-49,0,z),(49,0,z),2)
        mark('OPTICAL LAMINATE',(13,-6,111),'DAYLIGHT AND HEAT TRANSFER LAYERS')
    with group('C'):
        box('edge actuator',(61,0,87),(19,27,69),5)
        motor((61,0,42),8,24)
        rod('edge drive screw',(61,0,68),(61,0,145),2,'detail')
        for z in (71,108,140):box('edge linkage',(53,0,z),(21,12,8),2,'detail')
        for z in (64,119):cyl('service fastener',(61,-15,z),1.5,2,'detail',(0,-1,0),6)
        mark('EDGE ACTUATOR',(62,-15,93),'LOCAL CONTROL / MANUAL RELEASE')
    for x in (-62,77):box('window jamb',(x,8,87),(13,41,174),5)
    for z in (0,175):box('window header',(7,8,z),(152,41,14),5)
    for x in (-57,72):
        for z in (20,151):box('wall anchor',(x,25,z),(21,12,9),2,'detail')
    box('interior sill',(5,-14,-7),(168,76,9),5)
    optics((-61,-14,123),4,7)
    mark('JAMB',(77,-11,62),'REPLACEABLE SERVICE EDGE')
    mark('DAYLIGHT SENSOR',(-61,-21,123),'MEASURES USEFUL INDOOR LIGHT')
    return 26,21


def quiet_stair():
    # Four equal steps with a single coherent parallel linkage under the deck.
    with group('B'):
        for y in (-29,29):
            for x,z in ((-59,12),(-20,26),(19,40),(58,54)):
                rod('step support link',(x,y,z-11),(x+21,y,z+5),3)
                joint((x,y,z-11),4,(0,1,0));joint((x+21,y,z+5),4,(0,1,0))
                rod('fixed anchor riser',(x,y,9),(x,y,z-11),2.3,'detail')
            rod('synchronising bar',(-59,y,1),(79,y,57),2,'detail')
        mark('STEP LINKAGE',(-18,-29,29),'PARALLEL MOTION / LEVEL PLATFORM MODE')
    with group('C'):
        box('leading edge sensor',(-80,-1,17),(7,71,8),2)
        for y in range(-29,30,10):cyl('edge sensing aperture',(-85,y,17),1.7,2,'accent',(-1,0,0),16)
        for y in (-32,32):box('edge bracket',(-77,y,15),(11,7,15),2,'detail')
        tube('sensor lead',[(-80,-31,18),(-66,-37,12),(-47,-37,9)],.6,'cable')
        mark('EDGE SENSOR',(-83,-17,17),'OCCUPANCY AND PINCH CLEARANCE')
    for x,z in ((-59,12),(-20,26),(19,40),(58,54)):
        box('equal stair tread',(x,0,z),(38,83,7),3)
        for xx in (-10,0,10):rod('tread grip',(x+xx,-35,z+4),(x+xx,35,z+4),.35,'detail')
    for y in (-47,47):
        rod('handrail',(-75,y,81),(80,y,136),2)
        for x,z in ((-65,17),(63,60)):rod('handrail post',(x,y,z),(x,y,z+70),2)
    box('drive plinth',(25,0,4),(164,108,13),7);motor((66,0,20),12,25,(0,1,0))
    box('manual release',(64,-53,26),(28,17,29),4)
    mark('TREAD',(20,-35,44),'SAME PUBLIC ROUTE FOR EVERY USER')
    mark('MANUAL RELEASE',(64,-63,29),'ACCESSIBLE SERVICE OVERRIDE')
    return 26,25


def air_root():
    with group('B'):
        ring('sorbent wheel',(0,0,86),41,4,18,(0,1,0))
        for a in range(0,360,30):
            q=math.radians(a);rod('sorbent sector rib',(7*math.cos(q),-1,86+7*math.sin(q)),(37*math.cos(q),-1,86+37*math.sin(q)),1,'detail')
        for rr in (15,25,34):ring('honeycomb layer',(0,0,86),rr,.7,14,(0,1,0),'shell')
        motor((0,19,86),11,25,(0,1,0));flange('wheel hub',(0,-3,86),10,(0,-1,0),3)
        mark('SORBENT WHEEL',(25,-4,102),'REPLACEABLE ADSORBENT SECTORS')
    with group('C'):
        box('flow plenum',(0,5,34),(100,61,39),10)
        for x in range(-38,39,9):rod('flow guide',(x,-27,22),(x,-27,47),.7,'detail')
        for x in (-45,45):cyl('access fastener',(x,-29,37),1.8,2,'detail',(0,-1,0),6)
        ring('outlet throat',(0,38,34),19,3,17,(0,1,0))
        rotor((0,45,34),15,5,(0,1,0))
        mark('FLOW PLENUM',(0,-27,36),'SEPARATE PARTICLE AND GAS STAGES')
    for x in (-53,53):
        box('service upright',(x,15,70),(10,28,120),4)
        box('living cartridge',(x*1.4,17,40),(30,44,64),6)
        from .biology import sprig
        sprig((x*1.4,17,74),38,19)
    box('service base',(0,9,3),(188,93,14),10)
    box('particle filter',(-68,-19,83),(32,12,45),4)
    for z in range(65,102,5):rod('filter pleat',(-81,-27,z),(-55,-27,z),.4,'detail')
    tube('plant return',[(-75,34,34),(-41,41,17),(0,35,17),(75,34,34)],2,'cable')
    mark('PARTICLE FILTER',(-68,-28,87),'FIRST STAGE / PULL OUT ACCESS')
    mark('LIVING CARTRIDGE',(76,-5,54),'BIOLOGICAL STAGE / SEPARATE SERVICE')
    return 25,24


def frost_house():
    views(C=(-50,26))
    with group('B'):
        for x in (-34,0,34):
            box('phase change cassette',(x,11,66),(27,43,86),6)
            for z in (32,61,90):rod('cassette cooling rib',(x-9,-12,z),(x+9,-12,z),.5,'detail')
            tube('cassette handle',[(x-8,4,112),(x-8,4,121),(x+8,4,121),(x+8,4,112)],1.2)
        mark('THERMAL CASSETTE',(1,-13,72),'REPLACEABLE PHASE CHANGE RESERVE')
    with group('C'):
        # Actual open door: continuous rectangular gasket, hinges and latch.
        with at((-64,-27,0),-110):
            box('insulated door',(56,0,67),(111,13,131),11)
            tube('door gasket',[(9,-8,10),(103,-8,10),(103,-8,122),(9,-8,122),(9,-8,10)],1.2,'accent')
            for x in (14,98):
                for z in (17,116):cyl('gasket retainer',(x,-9,z),1.2,1.4,'detail',(0,-1,0),6)
            box('inner thermal liner',(56,-8,67),(78,3,87),7,'detail')
            for z in (25,107):cyl('door hinge',(0,0,z),4,12,'detail')
            rod('door latch',(99,-11,50),(99,-11,82),2,'detail')
        mark('DOOR GASKET',(-17,-119,70),'CONTINUOUS MONITORED THERMAL SEAL')
    for x in (-63,63):box('insulated cabinet wall',(x,10,67),(15,83,139),10)
    for z in (0,135):box('cabinet end',(0,10,z),(127,83,14),8)
    box('rear thermal wall',(0,47,68),(115,13,126),8)
    for z in (24,55,87):box('medicine shelf',(0,-14,z),(110,31,3),2,'detail')
    for x in (-32,0,32):box('medicine box',(x,-17,35),(24,22,18),3,'shell')
    box('temperature monitor',(80,-4,89),(23,23,36),5)
    box('temperature display',(80,-17,95),(15,2,13),2,'accent')
    for x in (75,85):cyl('monitor control',(x,-18,82),2,2,'detail',(0,-1,0))
    for x in (-33,0,33):
        vessel('sealed payload vial',(x,-15,58),6,18)
        cyl('vial cap',(x,-15,76),5,3,'detail')
    for x in (-34,34):
        box('payload tray',(x,-14,91),(28,26,5),2,'detail')
        for xx in (-8,0,8):cyl('sample tube',(x+xx,-14,94),2.5,14,'detail')
    for x in (-47,47):box('isolation foot',(x,9,-13),(29,56,12),5)
    mark('MEDICINE SHELF',(1,-29,39),'MONITORED PAYLOAD / STORAGE STUDY')
    mark('MONITOR',(80,-16,94),'ALARM BEFORE RESERVE IS EXHAUSTED')
    return -28,25


def bridge_kit():
    def knuckle(x,y):
        joint((x,y,21),9,(0,1,0))
        for side in (-1,1):rod('truss knuckle clevis',(x+side*15,y,5),(x,y,21),3,'detail')
        bolts((x,y-9,21),6,6,(0,-1,0),1)
        box('clevis lower shoe',(x,y,2),(36,13,7),3)
    with group('B'):
        knuckle(-50,-37)
        mark('TRUSS KNUCKLE',(-50,-46,22),'CAPTIVE PIN / ALIGNED LOAD PATH')
    for x,y in ((50,-37),(-50,37),(50,37)):knuckle(x,y)
    with group('C'):
        box('deck locking cassette',(0,-3,34),(25,72,9),3)
        for y in (-28,28):
            rod('deck lock pin',(-12,y,34),(12,y,34),2,'detail')
            box('overcentre latch',(0,y,40),(13,9,7),2)
            cyl('latch pivot',(0,y-5,39),2,10,'detail',(0,1,0),16)
        for x in (-9,9):rod('deck seam',(x,-34,40),(x,34,40),.4,'detail')
        mark('DECK LOCK',(0,-26,42),'LINKS ADJACENT LOAD PANELS')
    for y in (-37,37):
        for x in (-125,-75,-25,25,75):
            rod('upper chord',(x,y,30),(x+50,y,30),3)
            rod('lower chord',(x,y,0),(x+50,y,0),3)
            rod('diagonal',(x,y,0),(x+25,y,29),1.8,'detail');rod('diagonal',(x+25,y,29),(x+50,y,0),1.8,'detail')
    for x in range(-111,113,25):
        box('bridge deck panel',(x,0,34),(23,89,5),2)
        for xx in (-7,0,7):rod('deck texture',(x+xx,-40,37),(x+xx,40,37),.25,'shell')
    for y in (-44,44):
        for x in (-113,-63,-13,37,87,113):rod('folding handrail post',(x,y,36),(x,y,71),1.2,'detail')
        rod('handrail',(-113,y,71),(113,y,71),1.2,'detail')
    for x in (-116,116):box('bank shoe',(x,0,-10),(41,111,11),6)
    mark('BANK SHOE',(114,-34,-5),'DISTRIBUTES LOAD INTO THE BANK')
    mark('DECK',(60,-23,38),'INTERLOCKING WALKING SURFACE')
    return 25,28


def sand_archive():
    with group('B'):
        cyl('access throat',(0,0,105),24,49)
        for z in (107,148):flange('throat flange',(0,0,z),28,depth=4)
        ring('dust labyrinth',(0,0,154),26,4,9)
        box('hatch lid',(0,0,166),(56,53,9),10)
        rod('hatch handle',(-12,0,175),(12,0,175),2,'detail')
        for x in (-24,24):box('hatch dog',(x,0,169),(9,17,7),2)
        mark('ACCESS THROAT',(0,-26,141),'REPLACEABLE DUST AND WATER BARRIER')
    with group('C'):
        box('archive drawer',(0,-48,35),(65,63,15),6)
        for x in (-23,0,23):
            box('record packet',(x,-47,47),(17,41,12),3,'detail')
            rod('packet binding',(x,-65,55),(x,-29,55),.5,'accent')
        for x in (-29,29):rod('drawer rail',(x,-80,28),(x,9,28),2,'detail')
        rod('drawer pull',(-14,-81,37),(14,-81,37),2)
        mark('ARCHIVE DRAWER',(1,-64,53),'READABLE RECORDS AND DECODING NOTES')
    g.shell('sectioned buried chamber',63,0,106,15,208)
    for z in (0,102):flange('chamber compression ring',(0,0,z),67,depth=5)
    for a in (30,90,150):
        q=math.radians(a);rod('chamber stiffener',(64*math.cos(q),64*math.sin(q),9),(64*math.cos(q),64*math.sin(q),96),2,'detail')
    for z in (18,65,85):box('archive rack',(0,13,z),(79,51,5),4)
    box('desiccant drawer',(37,4,78),(22,37,22),4)
    tube('manual hatch linkage',[(21,3,149),(32,13,131),(42,16,116)],1.2,'detail')
    mark('BURIED CHAMBER',(-48,29,76),'SECTIONED DRY STORAGE ENVELOPE')
    mark('DESICCANT',(39,-13,80),'PASSIVE HUMIDITY BUFFER')
    return 26,26


def floating_court():
    with group('B'):
        for x in (-38,38):
            box('platform joint cheek',(x,0,17),(18,21,19),4)
            rod('joint pin',(x,-17,17),(x,17,17),3,'detail')
            for y in (-15,15):ring('pin retainer',(x,y,17),5,1.5,2,(0,1,0),'detail')
            tube('flexible service bridge',[(x-11,5,22),(x,9,28),(x+11,5,22)],1,'cable')
        mark('PLATFORM JOINT',(-38,-14,20),'FLEXIBLE INTERPLATFORM CONNECTION')
    with group('C'):
        box('mooring cleat base',(84,-40,24),(30,25,5),3)
        for x in (76,92):rod('cleat post',(x,-40,26),(x,-40,35),2)
        rod('cleat horn',(67,-40,36),(101,-40,36),3)
        for x in (73,95):
            for y in (-47,-33):cyl('cleat bolt',(x,y,27),1.5,2,'detail',n=6)
        tube('mooring rope',[(83,-41,33),(98,-58,19),(123,-83,-10)],.8,'accent')
        mark('MOORING CLEAT',(84,-43,35),'RECOVERABLE SHORE ANCHOR')
    for x,y in ((-76,0),(0,0),(76,0),(0,76),(0,-76)):
        box('buoyant caisson',(x,y,4),(72,72,23),11)
        box('walking deck',(x,y,19),(74,74,5),5)
        for yy in range(-28,29,8):rod('deck board',(x-32,y+yy,22),(x+32,y+yy,22),.3,'shell')
    for x,y in ((-22,-22),(-22,22),(22,-22),(22,22)):rod('service canopy post',(x,y,22),(x,y,101),2.5)
    box('service core',(0,7,54),(34,24,63),7)
    for side in (-1,1):leaf('canopy wing',(0,0,104),(side*64,0,94),97,'shell')
    for x in (-78,78):box('public bench',(x,0,37),(42,19,9),4)
    mark('SERVICE CORE',(0,-6,61),'SHARED POWER AND COMMUNICATION')
    mark('CAISSON',(77,-30,7),'COMPARTMENTED BUOYANCY')
    return 28,32


def shade_orchard():
    with group('B'):
        for x in (-54,-18,18,54):
            joint((x,-32,110),6,(0,1,0))
            rod('louver axle',(x,-40,110),(x,40,110),2)
        rod('synchronising link',(-54,-42,112),(54,-42,112),1.8,'detail')
        motor((0,-46,109),8,19,(0,-1,0))
        for x in (-54,-18,18,54):rod('crank',(x,-42,110),(x+7,-42,118),1.5,'detail')
        mark('LOUVER PIVOT',(0,-52,111),'ONE CONTROLLED SHADING AXIS')
    with group('C'):
        box('rain channel',(0,49,104),(157,14,9),3)
        for x in (-63,63):box('gutter clip',(x,48,102),(8,21,14),2)
        tube('downpipe',[(67,49,101),(73,49,87),(73,49,10)],2.5,'cable')
        flange('downpipe cleanout',(73,49,8),5,depth=3)
        mark('RAIN CHANNEL',(44,49,105),'WATER TO A COVERED GROUND STORE')
    for x in (-72,72):
        for y in (-39,39):rod('canopy column',(x,y,0),(x,y,105),3);box('column foot',(x,y,0),(24,24,6),4)
    for y in (-40,40):rod('roof beam',(-77,y,105),(77,y,105),3)
    for x in (-54,-18,18,54):
        with at((x,0,111),22,'Y'):
            box('shading louver',(0,0,0),(29,85,3),3)
            for y in (-33,33):rod('louver stiffener',(-11,y,-2),(11,y,-2),.7,'detail')
    box('public bench',(0,20,19),(104,27,8),5)
    for x in (-37,37):rod('bench leg',(x,20,0),(x,20,17),2)
    optics((-71,-40,97),4,7)
    mark('LOUVER',(20,-9,115),'SUMMER SHADE / WINTER DAYLIGHT')
    mark('PEDESTRIAN SPACE',(0,6,22),'CLEAR ROUTE BELOW THE CANOPY')
    return 26,27
