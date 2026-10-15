"""Energy machines with distinct flows: momentum, heat, wind, waves and salt."""
from .kit import *


def tidal_loom():
    # Open bridge lets marine life pass between independently removable turbines.
    with group('B'):
        ring('rotor shroud',(-71,-17,61),44,5,31,(0,1,0))
        rotor((-71,-3,61),36,5,(0,1,0))
        motor((-71,5,61),11,33,(0,1,0))
        for a in (0,120,240):
            q=math.radians(a);rod('generator stay',(-71+38*math.cos(q),20,61+38*math.sin(q)),(-71,34,61),2)
        mark('ROTOR',(-71,-9,61),'REMOVABLE GENERATOR CARTRIDGE')
    with group('C'):
        ring('guide frame',(71,-17,61),44,5,31,(0,1,0))
        for a in range(0,360,60):
            with at((71,-18,61),a,'Y'):
                leaf('guide vane',(12,0,0),(39,0,0),14,'detail')
        flange('hub collar',(71,-18,61),13,(0,1,0))
        mark('GUIDE VANES',(105,-18,70),'REVERSING FLOW / SOFT LEADING EDGE')
    for a in range(0,360,60):
        with at((-71,-18,61),a,'Y'):leaf('guide vane',(12,0,0),(39,0,0),14,'detail')
    for a in (0,120,240):
        q=math.radians(a);rod('generator stay',(71+38*math.cos(q),20,61+38*math.sin(q)),(71,34,61),2)
    rotor((71,4,61),36,5,(0,1,0));motor((71,11,61),11,31,(0,1,0))
    for x in (-71,71):
        for y in (-24,32):rod('support leg',(x,y,35),(x*1.2,y*1.3,0),4)
        box('seabed foot',(x*1.2,0,0),(34,99,8),7)
    truss((-71,30,108),(71,30,108),13,8)
    box('wet junction',(0,30,109),(37,31,24),6)
    tube('power conduit',[(-71,38,61),(-47,42,107),(0,37,112),(48,42,107),(71,38,61)],2,'accent')
    mark('BRIDGE',(0,30,111),'CLEAR CENTRAL TRANSIT CORRIDOR')
    mark('FOOT',(86,-28,2),'RECOVERABLE BALLAST ANCHOR')
    return 24,25


def inertia_bank():
    # Two staggered vacuum vessels, cutaway rotor in front and closed rear store.
    with group('B'):
        for z in (25,48,71):
            ring('composite rotor',(0,0,z),39,12,14)
            for a in range(0,360,60):
                q=math.radians(a);rod('rotor spoke',(8*math.cos(q),8*math.sin(q),z+7),(30*math.cos(q),30*math.sin(q),z+7),2.3,'detail')
        rod('rotor shaft',(0,0,12),(0,0,112),6)
        mark('ROTOR STACK',(32,-21,73),'COUNTER ROTATING STORAGE PAIR')
    with group('C'):
        for z in (12,97):
            ring('bearing stator',(0,0,z),20,5,11);bolts((0,0,z+12),17,8,size=1)
            for a in range(0,360,90):
                q=math.radians(a);box('magnetic pole',(24*math.cos(q),24*math.sin(q),z+5),(9,9,12),1,'detail')
        for x,y in ((29,29),(-29,29),(-29,-29),(29,-29)):rod('bearing cage tie',(x,y,9),(x,y,115),2,'detail')
        mark('BEARING CAGE',(-24,-24,103),'CONTACTLESS SUPPORT / TOUCHDOWN RING')
    g.shell('sectioned vacuum shell',48,9,112,30,210)
    for z in (7,113):flange('pressure flange',(0,0,z),50,depth=5)
    vessel('second vacuum store',(105,31,8),46,114)
    for x,y in ((0,0),(105,31)):
        for dx in (-34,34):box('isolation shoe',(x+dx,y,-1),(19,77,14),4)
    box('inverter cabinet',(100,-42,46),(51,25,79),7)
    for z in range(16,79,7):rod('inverter cooling rib',(78,-57,z),(122,-57,z),.7,'detail')
    tube('bus conduit',[(37,-21,24),(70,-40,17),(83,-44,19)],2,'accent')
    mark('INVERTER',(100,-56,47),'DC BUS POWER INTERFACE')
    mark('VACUUM VESSEL',(105,-13,94),'FRAGMENT CONTAINMENT SHELL')
    return 26,25


def ember_vault():
    views(C=(46,24))
    # Brick-like storage cassettes inside a curved, opened refractory enclosure.
    with group('B'):
        for z in (22,45,68,91):
            for x in (-32,0,32):
                box('ceramic heat block',(x,0,z),(28,61,19),3,'structure')
                for y in (-18,0,18):cyl('heat passage',(x,y,z+9.7),3.2,.5,'accent',n=20)
        mark('CERAMIC CORE',(-31,-31,69),'REPLACEABLE RESISTIVE HEAT BRICKS')
    with group('C'):
        for x in (-33,-11,11,33):
            tube('exchanger hairpin',[(x,42,23),(x,66,26),(x,69,87),(x,42,94)],2.2,'detail')
        for z in (23,94):rod('exchanger header',(-44,42,z),(44,42,z),6)
        for x in (-44,44):flange('header connection',(x,42,23),9,(1,0,0))
        for z in range(34,86,8):box('transfer fin',(0,61,z),(84,23,1.2),.4,'detail')
        mark('EXCHANGER',(35,63,59),'SEALED USEFUL HEAT CIRCUIT')
    for x in (-57,57):
        hull('insulated curved cheek',[(-39,5,5,8),(-28,11,49,58),(28,11,49,58),(39,5,5,8)],'Y')
        g.parts[-1][0].location.x=x
    box('refractory plinth',(0,12,5),(128,123,16),9)
    box('refractory crown',(0,12,119),(126,119,17),10)
    for x in (-54,54):
        rod('front tie', (x,-43,15),(x,-43,111),3)
        bolts((x,-43,121),4,4,size=1)
    box('control pod',(63,-46,71),(30,23,45),5);g.dial(63,-59,77,8)
    for x in (57,69):cyl('control key',(x,-60,59),2,2,'accent',(0,-1,0))
    mark('INSULATION',(-57,-12,72),'MULTILAYER REFRACTORY SHELL')
    mark('CONTROL POD',(65,-60,73),'LIMITS TEMPERATURE AND CHARGE RATE')
    return 26,22


def mantle_needle():
    # Drill rig on four rock shoes; the drill crown is deliberately visible below deck.
    with group('B'):
        cyl('crown body',(0,0,12),24,27)
        ring('annular cutter',(0,0,5),27,5,10)
        for a in range(0,360,30):
            q=math.radians(a);cyl('cutter insert',(24*math.cos(q),24*math.sin(q),3),3,6,'accent',n=6)
            tube('flushing passage',[(18*math.cos(q),18*math.sin(q),36),(21*math.cos(q),21*math.sin(q),21)],1,'detail')
        mark('DRILL CROWN',(19,-18,13),'ELECTRIC ASSIST / ANNULAR CUT')
    with group('C'):
        ring('return manifold',(0,0,145),24,10,14)
        for x in (-1,1):
            rod('return elbow',(x*22,0,151),(x*43,0,151),5)
            flange('return coupling',(x*43,0,151),9,(x,0,0))
            cyl('isolation valve',(x*33,0,157),6,12,'detail');ring('valve handwheel',(x*33,0,170),9,1.5,2,role='detail')
        bolts((0,0,161),19,10,size=1.2)
        mark('RETURN MANIFOLD',(24,0,151),'SEALED SUPPLY AND RETURN')
    rod('drill stem',(0,0,38),(0,0,145),11)
    for x in (-40,40):truss((x,18,35),(x,18,195),11,8)
    box('crown carriage',(0,16,191),(98,31,18),5);motor((0,0,165),17,36)
    for x in (-68,68):
        for y in (-45,45):
            rod('outrigger',(x*.58,y*.4,59),(x,y,6),5);box('rock shoe',(x,y,3),(33,38,8),5)
    box('service deck',(0,21,53),(117,81,9),5)
    for y in (55,64,73):rod('hose rack',(-57,y,69),(57,y,69),2,'detail')
    tube('return hose',[(43,0,151),(69,20,140),(65,45,88),(58,66,69)],3,'accent')
    mark('FEED TOWER',(-40,18,116),'CONSTANT THRUST DRILL FEED')
    mark('ROCK SHOE',(68,-45,7),'LOAD DISTRIBUTION PAD')
    return 28,22


def wind_kite():
    views(C=(24,52))
    # Wing occupies upper half, one thin physical tether connects to ground drum.
    with group('B'):
        cyl('tether drum',(-22,0,25),24,44,'structure',(1,0,0))
        for x in (-24,24):flange('drum flange',(x,0,25),29,(1,0,0),3)
        for x in range(-18,20,3):ring('tether winding',(x,0,25),24.5,.5,1,(1,0,0),'detail')
        motor((30,0,25),14,30,(1,0,0))
        for x in (-34,30):box('drum bearing',(x,0,12),(15,37,27),4)
        mark('TETHER DRUM',(0,-24,27),'TRACTION POWER TAKEOFF')
    box('winch skid',(7,0,-3),(131,74,12),8)
    for x in (-43,48):
        for y in (-30,30):rod('ground screw',(x,y,-3),(x,y,-17),3,'detail')
    with group('C'):
        with at((0,12,230),-8,'Y'):
            truss((-103,0,0),(103,0,0),10,16)
            for x in range(-96,97,16):
                tube('wing rib',[(x,-11,-2),(x,-5,5),(x,10,7),(x,26,0)],.7,'detail')
            for x in (-80,0,80):box('spar joiner',(x,0,0),(14,17,16),2)
        mark('WING SPAR',(30,12,234),'LOAD PATH TO BRIDLE ROOTS')
    # Light membrane between leading and trailing edges; readable sweep.
    with at((0,12,230),-8,'Y'):
        g.mesh('kite skin',[(-112,0,0),(-87,34,0),(0,22,7),(87,34,0),(112,0,0),(0,-17,5)],[(0,1,2,3,4,5)],'shell')
        g.wire('wing perimeter',[(-112,0,0),(-87,34,0),(0,22,7),(87,34,0),(112,0,0),(0,-17,5),(-112,0,0)],.6,'structure')
    for x in (-73,73):tube('bridle',[(x,21,220),(0,8,177)],.35,'detail')
    tube('traction tether',[(0,8,177),(3,7,104),(0,0,50)],.35,'accent')
    optics((47,-20,19),6,14)
    mark('BRIDLE',(0,8,177),'DIFFERENTIAL STEERING LINES')
    mark('TRACKER',(47,-35,19),'WING POSITION AND WIND ESTIMATE')
    return 25,32


def salt_delta():
    # Alternating membrane channels inside a tied pressure stack, two separated feeds.
    with group('B'):
        for x in range(-43,45,7):
            box('membrane cassette',(x,0,58),(4,58,77),4)
            for y in (-23,23):cyl('manifold port',(x-2,y,84),4,4,'accent',(1,0,0))
        for x in (-51,51):box('clamping platen',(x,0,58),(11,72,91),7)
        for y in (-30,30):
            for z in (23,93):rod('tie rod',(-60,y,z),(60,y,z),2,'detail')
        mark('MEMBRANE STACK',(5,-30,63),'ALTERNATING SELECTIVE LAYERS')
    with group('C'):
        for y in (-19,19):
            rod('feed header',(-57,y,18),(57,y,18),7)
            for x in range(-42,43,14):rod('channel riser',(x,y,18),(x,y,30),2,'detail')
            flange('feed flange',(-60,y,18),11,(-1,0,0));flange('return flange',(59,y,18),11,(1,0,0))
        box('flow separation block',(-69,0,24),(19,67,35),4)
        mark('FLOW DISTRIBUTOR',(-69,-22,24),'FRESH AND SALT STREAMS STAY SEPARATE')
    skid(145,94)
    for side in (-1,1):
        pump((side*97,0,24),.6)
        tube('feed elbow',[(side*96,0,40),(side*85,side*19,42),(side*68,side*19,20)],2,'cable')
    box('electrical cabinet',(37,48,58),(45,27,56),6)
    for z in range(38,76,6):rod('cabinet vent',(21,63,z),(53,63,z),.5,'detail')
    mark('FEED PUMP',(-99,-4,37),'LOW PRESSURE CIRCULATION')
    mark('POWER TERMINAL',(39,48,81),'STACK OUTPUT CONDITIONING')
    return 26,27


def sun_fold():
    # Radial dish made of individually articulated mirror leaves.
    def facet_actuator():
        with at((55,0,83),-28,'Y'):
            joint((0,0,0),7);rod('facet strut',(0,0,0),(44,0,0),3)
            rod('actuator barrel',(3,-7,-13),(29,-7,-10),3,'detail')
            rod('actuator rod',(27,-7,-10),(45,-7,-2),1.3,'detail')
            for x in (3,44):joint((x,-7,-8),3,(0,1,0))
            box('facet carrier',(31,0,4),(41,24,5),2)
    with group('B'):facet_actuator()
    mark('FACET ACTUATOR',(73,-7,89),'FAIL SAFE STOW POSITION')
    for angle in range(45,360,45):
        with at(angle=angle):facet_actuator()
    for a in range(0,360,45):
        with at(angle=a):
            leaf('mirror leaf',(20,-5,79),(114,0,111),47,'accent')
            rod('mirror back rib',(21,0,76),(107,0,105),2,'detail')
            joint((21,-5,77),5)
    with group('C'):
        vessel('thermal receiver',(0,0,133),14,31)
        for z in range(139,159,4):ring('absorber fin',(0,0,z),16,1,1,role='detail')
        for x in (-7,7):tube('receiver return',[(x,0,163),(x,16,167),(x,24,145)],1.5,'cable')
        flange('receiver aperture',(0,0,132),17,(0,0,-1))
        mark('RECEIVER',(0,-16,147),'SMALL FOCAL HEAT RECEIVER')
    for a in (0,120,240):
        q=math.radians(a);rod('receiver tripod',(65*math.cos(q),65*math.sin(q),83),(11*math.cos(q),11*math.sin(q),136),1.5)
    cyl('pedestal',(0,0,9),15,66);joint((0,0,77),18)
    for a in (0,120,240):
        with at(angle=a):rod('foot brace',(0,0,22),(50,0,0),4);box('pavement shoe',(50,0,0),(27,22,5),4)
    box('charging pedestal',(42,-39,19),(29,24,40),6)
    mark('SLEW HEAD',(0,-17,77),'TWO AXIS SOLAR TRACKING')
    mark('CHARGING POST',(43,-51,27),'PUBLIC COURT INTERFACE')
    return 24,29


def pulse_reef():
    # Long anchored spar and annular floating collar, with exposed generator slot.
    with group('B'):
        rod('translator shaft',(0,0,32),(0,0,163),7)
        for z in range(50,151,10):ring('magnet ring',(0,0,z),15,7,6,role='accent')
        for x in (-24,24):rod('generator guide',(x,0,41),(x,0,159),2,'detail')
        for z in (41,159):box('guide crosshead',(0,0,z),(62,28,10),3)
        mark('TRANSLATOR',(12,0,105),'RELATIVE HEAVE DRIVES THE GENERATOR')
    with group('C'):
        cyl('mooring swivel',(0,0,-35),15,26)
        flange('swivel cap',(0,0,-8),18)
        ring('anchor eye',(0,-4,-43),13,4,8,(0,1,0))
        for z in (-29,-22):ring('swivel bearing',(0,0,z),17,1,3,role='detail')
        mark('MOORING SWIVEL',(0,-10,-32),'TORSION ISOLATION AT THE ANCHOR')
    ring('float collar',(0,0,67),63,31,32)
    for z in (67,98):ring('float rub rail',(0,0,z),65,2,3,role='detail')
    for a in range(0,360,60):
        with at(angle=a):rod('float spoke',(23,0,81),(36,0,81),4);box('access hatch',(49,0,101),(20,15,3),3,'detail')
    cyl('lower ballast spar',(0,0,-5),19,62)
    rod('beacon mast',(0,0,165),(0,0,207),2);optics((0,-5,199),5,8)
    for side in (-1,1):panel('beacon solar panel',(side*19,0,183),(25,25),nx=3,ny=3)
    mark('FLOAT COLLAR',(43,-42,84),'ANNULAR BUOY / SEA SURFACE')
    mark('BALLAST SPAR',(0,-19,27),'SUBMERGED REACTION MASS')
    return 27,24


def night_cell():
    views(C=(34,-27))
    # Flat faceted cold plate lifted clear of ground heat, tiny sensor load beneath.
    with group('B'):
        for x in (-35,35):
            panel('selective sky radiator',(x,0,71),(65,111),nx=5,ny=7,role='shell')
            for y in (-46,46):box('laminate clamp',(x,y,72),(54,4,3),1,'detail')
        for y in (-54,54):rod('radiator frame',(-71,y,71),(71,y,71),2)
        mark('RADIATOR',(31,-23,73),'SELECTIVE INFRARED EMISSION')
    with group('C'):
        box('cold spreader',(0,0,65),(64,47,5),2)
        for x in (-21,0,21):
            box('thermoelectric tile',(x,0,58),(17,33,9),2,'accent')
            for z in range(36,54,4):box('warm fin',(x,0,z),(20,43,1.2),.3,'detail')
        box('warm collector',(0,0,32),(73,52,5),3)
        mark('THERMAL BRIDGE',(0,-18,58),'SMALL TEMPERATURE DIFFERENCE')
    for x in (-58,58):
        for y in (-44,44):rod('insulated leg',(x,y,70),(x*1.16,y*1.16,0),2.5);box('ground foot',(x*1.16,y*1.16,0),(21,24,4),3)
    box('sensor logger',(43,-33,22),(34,23,34),5)
    optics((43,-45,27),4,7)
    rod('logger aerial',(48,-29,38),(48,-29,104),.8,'detail')
    tube('signal cable',[(0,10,32),(18,20,19),(35,-20,19)],.65,'cable')
    mark('LOGGER',(44,-45,21),'LOW POWER FIELD TELEMETRY')
    mark('SUPPORT',(68,-52,4),'THERMAL ISOLATION FROM GROUND')
    return 28,29


def district_heart():
    # Two large loops joined by compressor and a deliberately open service bridge.
    with group('B'):
        cyl('compressor shell',(-47,0,23),27,60)
        flange('compressor cover',(-47,0,84),29)
        for z in range(31,80,6):ring('shell cooling band',(-47,0,z),28,1,2,role='detail')
        motor((-47,0,91),20,30)
        tube('discharge elbow',[(-25,0,77),(-9,0,82),(-8,22,93)],4,'cable')
        mark('COMPRESSOR',(-47,-28,61),'VARIABLE SPEED REFRIGERANT SCROLL')
    with group('C'):
        for x in (-9,14,37,60):
            cyl('valve body',(x,-39,53),7,17,'structure',(0,1,0))
            cyl('valve spindle',(x,-30,60),3,15,'detail');ring('valve wheel',(x,-30,76),8,1.5,2,role='accent')
            rod('valve drop',(x,-30,51),(x,-30,28),3,'detail')
        for z in (29,53):rod('valve header',(-16,-30,z),(68,-30,z),4)
        for x in (-17,69):flange('service connection',(x,-30,29),8,(1,0,0))
        mark('VALVE BRIDGE',(26,-37,55),'REVERSIBLE FLOW ROUTING')
    for x in (34,83):
        for y in range(-3,43,5):box('plate exchanger',(x,y,61),(35,2,83),3,'detail')
        for y in (-7,47):box('pressure platen',(x,y,61),(42,6,91),5)
        for z in (32,91):
            for xx in (x-16,x+16):rod('exchanger tie',(xx,-12,z),(xx,52,z),1.5,'detail')
    skid(191,131)
    for z in (32,92):tube('loop pipe',[(-47,18,z),(0,65,z),(87,62,z),(101,48,z)],3,'cable')
    box('service controller',(-70,-29,96),(30,21,38),5)
    mark('DISTRICT LOOP',(85,48,82),'HOT WATER PLATE EXCHANGER')
    mark('CONTROLLER',(-70,-42,99),'DEMAND AND DEFROST COORDINATION')
    return 28,23
