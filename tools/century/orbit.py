"""Ten different orbital machines: deployed structures, vehicles and anchored tools."""
from .kit import *


def light_sail():
    # Four diamond membranes supported by extensible booms; compact cargo spine.
    with group('B'):
        ring('reefing drum housing',(0,0,-12),28,4,25)
        flange('hub flange',(0,0,13),31)
        for x,y in ((-12,-12),(-12,12),(12,-12),(12,12)):
            cyl('tension drum',(x,y,-5),8,17,'detail')
            for z in (-3,1,5,9):ring('wound line',(x,y,z),8.6,.5,.8,role='detail')
            bolts((x,y,13),5.5,4,size=.7)
        for a in range(0,360,90):
            with at(angle=a):
                joint((31,0,0),7,(0,1,0));motor((34,-11,-8),7,20,(0,1,0))
                box('boom root latch',(46,0,0),(23,13,15),3)
        mark('REEFING HUB',(0,-24,10),'HUB FLANGE / FOUR BOOM LATCHES')
    with group('C'):
        with at((43,0,0)):
            box('root clevis',(0,0,0),(22,27,10),3)
            for y in (-12,12):
                box('bearing cheek',(6,y,6),(20,4,19),2)
                cyl('roller bearing',(6,y,8),5,3,'detail',(0,1,0));bolts((6,y+3,8),3.5,4,(0,1,0),.6)
            cyl('deployment roller',(6,-10,8),4,20,'detail',(0,1,0))
            motor((-7,-18,0),6,13,(0,1,0),fins=False)  # fins this small hatch the roller in C
            rod('retaining pin',(-6,-17,8),(-6,17,8),2,'detail')
            for x in (-7,7):cyl('plate fastener',(x,0,6),1.6,2,'detail',n=6)
        mark('SAIL ROOT',(49,7,8),'MEMBRANE EDGE TENSIONER')
    truss((56,0,0),(185,0,0),8,10)
    box('end roller',(181,0,0),(16,21,11),3)
    for y in (-8,8):cyl('guide roller',(181,y,-8),4,16,'detail')
    tube('tension line',[(42,10,1),(99,17,4),(170,7,0)],.3,'accent')
    for a in (90,180,270):
        with at(angle=a):truss((42,0,0),(185,0,0),8,10)
    for a in range(0,360,90):
        with at(angle=a):
            pts=[(16,16,1),(173,6,0),(106,106,4),(6,173,0)]
            g.mesh('reflective sail membrane',pts,[(0,1,2,3)],'shell')
            g.wire('sail reinforced edge',pts+[pts[0]],.38,'structure')
            for j in range(1,12):
                t=j/12;g.wire('radial membrane weld',[(16+157*t,16-10*t,1-t),(6+100*t,173-67*t,4*t)],.09,'shell')
    with at((0,0,-60)):
        hull('cargo spindle',[(-74,3,3,0),(-61,16,14,0),(42,19,17,0),(68,10,10,0),(76,4,4,0)])
        for x in (-40,0,40):ring('payload cradle',(x,0,0),20,2,6,(1,0,0),'detail')
        for x in (-37,37):rod('cargo standoff',(x,0,13),(x*.35,0,48),3)
        optics((68,0,0),6,12,(1,0,0))
    # The cargo spindle hangs behind the membrane in A, so it carries no callout there.
    mark('MEMBRANE',(95,-90,3),'REPAIRABLE REFLECTIVE FILM')
    mark('TIP REEL',(185,0,0),'BOOM RETRACTION DRIVE')
    return 25,50


def ring_tender():
    # Three-finger docking tug wrapped around a genuinely open capture throat.
    with group('B'):
        ring('capture throat',(0,0,0),62,7,20,(0,1,0))
        ring('compliant seal',(0,-2,0),56,2,4,(0,1,0),'accent')
        for a in (30,150,270):
            with at(angle=a,axis='Y'):
                box('capture shoe',(56,0,0),(20,28,17),4)
                rod('jaw slide',(42,-12,0),(66,-12,0),3,'detail');motor((68,0,0),6,14,(-1,0,0))
        mark('CAPTURE RING',(0,-3,58),'SOFT CONTACT BEFORE HARD LATCH')
    with group('C'):
        with at((92,28,0),-15,'Z'):
            vessel('propellant pod',(0,0,-31),15,62)
            for z in (-30,28):
                for side in (-1,1):
                    ring('thruster nozzle',(0,side*18,z),8,2,9,(0,side,0));cyl('thruster chamber',(0,side*11,z),5,8,'detail',(0,side,0))
            box('valve island',(15,-10,0),(14,19,26),3)
        mark('THRUSTER POD',(94,7,28),'PAIRED TRANSLATION JETS')
    for x in (-92,92):
        if x<0:
            vessel('second propellant pod',(x,28,-31),15,62)
            for z in (-30,28):
                for side in (-1,1):
                    ring('thruster nozzle',(x,28+side*18,z),8,2,9,(0,side,0));cyl('thruster chamber',(x,28+side*11,z),5,8,'detail',(0,side,0))
        truss((x*.59,14,0),(x,28,0),12,3)
    hull('avionics dorsal fairing',[(-54,18,17,0),(-35,26,24,0),(35,26,24,0),(54,18,17,0)],'X')
    # Shift fairing above throat instead of occluding its opening.
    o=g.parts[-1][0];o.location.z=98;o.location.y=35
    for x in (-32,32):rod('dorsal bridge',(x,21,49),(x,35,82),4)
    optics((0,7,97),10,18,(0,-1,0));optics((23,8,97),5,12,(0,-1,0))
    radiator((-99,34,-56),(36,90));radiator((99,34,-56),(36,90))
    mark('RANGE FINDER',(0,-11,97),'FINAL APPROACH LIDAR')
    mark('RADIATOR',(-99,34,-56),'WASTE HEAT TO DEEP SPACE')
    return 23,21


def sweep_net():
    # Broad square catching aperture carried ahead of a small tug.
    with group('B'):
        for x in (-65,65):truss((x,-55,0),(x,55,0),7,7)
        for y in (-55,55):truss((-65,y,0),(65,y,0),7,8)
        for i in range(-5,6):
            tube('capture web X',[(-61,i*9,0),(0,i*9,-8),(61,i*9,0)],.25,'shell')
            tube('capture web Y',[(i*10,-51,0),(i*10,0,-8),(i*10,51,0)],.25,'shell')
        mark('CATCH WEB',(0,-20,-7),'SACRIFICIAL TENSION MESH')
    with group('C'):
        with at((65,-55,0)):
            motor((0,0,-17),9,27);flange('reel cheek',(0,0,13),16)
            for z in (-5,0,5):ring('cable turns',(0,0,z),12,1,2,role='detail')
            box('load cell',(16,0,4),(17,13,12),2)
        mark('CORNER REEL',(65,-55,10),'LOAD LIMITED PAYOUT')
    for x in (-65,65):
        for y in (-55,55):rod('capture boom',(x,y,-3),(x*.3,y*.3,-100),2)
    vessel('service bus',(0,0,-137),26,45)
    for x in (-1,1):panel('power wing',(x*66,0,-123),(54,70),nx=6,ny=6)
    optics((0,-25,-115),7,13)
    mark('SERVICE BUS',(0,-26,-117),'GUIDANCE AND DEORBIT PACKAGE')
    mark('POWER WING',(-65,0,-123),'FOLDING SOLAR ARRAY')
    return 28,40


def petal_eye():
    # Segmented primary mirror; radial service modules leave optical axis clear.
    with group('B'):
        cyl('mirror backplate',(0,0,0),69,8)
        for row in range(-2,3):
            for col in range(-2,3):
                x=col*24+(row%2)*12;y=row*21
                if x*x+y*y>57**2:continue
                o=cyl('hexagonal mirror',(x,y,10),13,3,'accent',n=6)
                o.matrix_world=o.matrix_world@Matrix.Rotation(math.pi/6,4,'Z')
                for a in (0,120,240):
                    q=math.radians(a);rod('mirror actuator',(x+8*math.cos(q),y+8*math.sin(q),4),(x+8*math.cos(q),y+8*math.sin(q),9),1,'detail')
        mark('PRIMARY MIRROR',(0,0,13),'19 HEXAGONAL SEGMENTS')
    with group('C'):
        for a in (30,150,270):
            q=math.radians(a);rod('secondary spider',(60*math.cos(q),60*math.sin(q),6),(11*math.cos(q),11*math.sin(q),91),1.5)
        ring('secondary cell',(0,0,91),15,3,7);bolts((0,0,99),11,6,size=1)
        optics((0,0,95),9,15,(0,0,-1))
        mark('SECONDARY',(0,0,99),'FOCUS STAGE AND STRAY-LIGHT BAFFLE')
    for a in range(0,360,60):
        with at(angle=a):
            leaf('deployable sun shade',(67,-19,-7),(132,0,-18),45,'shell');rod('shade hinge',(65,-16,-6),(65,16,-6),2)
    vessel('instrument barrel',(0,0,-85),31,75)
    for z in (-69,-39):ring('instrument bay',(0,0,z),34,2,3,role='detail')
    for x in (-1,1):radiator((x*85,0,-66),(53,100))
    mark('DETECTOR BAY',(0,-31,-45),'CRYOGENIC FOCAL PLANE')
    mark('SUN SHADE',(119,-16,-16),'SIX DEPLOYABLE PETALS')
    return 26,41


def wheelhouse():
    # Axial flywheel service spacecraft, two counterrotating drums with open yoke.
    with group('B'):
        for z in (0,28):
            ring('momentum flywheel',(0,0,z),57,11,16)
            for a in range(0,360,60):
                q=math.radians(a);rod('wheel spoke',(12*math.cos(q),12*math.sin(q),z+8),(48*math.cos(q),48*math.sin(q),z+8),3,'detail')
            cyl('magnetic hub',(0,0,z),14,16,'detail');bolts((0,0,z+17),10,6,size=1)
        rod('bearing axis',(0,0,-17),(0,0,59),5)
        mark('COUNTER ROTORS',(45,-25,36),'ANGULAR MOMENTUM EXCHANGE')
    with group('C'):
        motor((0,0,56),19,25)
        for x in (-38,38):rod('motor yoke',(x,0,50),(x,0,92),4)
        box('yoke crown',(0,0,91),(87,26,13),5)
        for x in (-29,29):joint((x,-13,91),7)
        mark('BEARING YOKE',(0,-13,92),'ACTIVE MAGNETIC SUSPENSION')
    for x in (-80,80):
        truss((x,0,-28),(x,0,91),12,6);rod('upper outrigger',(x,0,91),(35 if x>0 else -35,0,91),4)
    hull('service hull',[(-85,15,10,-39),(-65,29,20,-39),(65,29,20,-39),(85,15,10,-39)])
    for x in (-100,100):radiator((x,0,-36),(27,110))
    optics((0,-29,-38),9,13)
    mark('SERVICE BUS',(0,-32,-38),'STATION ATTITUDE INTERFACE')
    mark('COOLING LEAF',(100,0,-36),'BEARING HEAT REJECTION')
    return 27,28


def ice_mule():
    # Asymmetric lunar tank hauler, six wheels and a real tool-side crane.
    wheels(74,44,19);wheels(0,44,19)
    hull('rover sill',[(-102,24,8,39),(-78,43,14,39),(69,43,14,39),(93,24,8,39)])
    with group('B'):
        for x in (-35,25):
            vessel('insulated ice flask',(x,0,54),24,69)
            ring('flask retention strap',(x,0,83),26,2,4,'Z' if False else (0,0,1),'detail')
        tube('transfer hose',[(-35,-27,72),(-10,-36,62),(25,-27,72)],2,'accent')
        pump((62,0,55),.62)
        mark('ICE FLASK',(-35,-24,92),'VACUUM JACKET / SOLID CARGO')
    with group('C'):
        cyl('crane slew ring',(-82,25,49),13,12);bolts((-82,25,62),10,6,size=1)
        rod('crane lower arm',(-82,25,60),(-100,25,116),5);joint((-100,20,116),8)
        rod('crane jib',(-100,25,116),(-138,12,107),4)
        gripper((-139,12,100),20,(0,0,-1))
        rod('lift ram',(-91,18,71),(-100,18,111),2,'detail')
        mark('SAMPLE CRANE',(-137,12,106),'SEALED CANISTER HANDLING')
    rod('navigation mast',(81,0,46),(81,0,127),3)
    optics((81,-8,123),7,14);panel('mast solar visor',(81,0,140),(41,36),nx=5,ny=4)
    mark('NAVIGATION',(81,-20,123),'STEREO RANGE HEAD')
    mark('WHEEL BOGIE',(0,-56,19),'COMPLIANT METAL MESH TYRE')
    return 25,23


def shade_courier():
    views(B=(25,-28),C=(34,22))
    # Long cold-chain spacecraft shaded by three staggered circular parasols.
    with group('B'):
        for z,r in ((60,89),(68,80),(76,70)):
            cyl('radiation shield',(0,0,z),r,.8,'shell',n=96)
            ring('shield perimeter',(0,0,z),r,1,1,role='structure')
            for a in range(0,360,45):
                q=math.radians(a);rod('shield rib',(8*math.cos(q),8*math.sin(q),z-1),(r*math.cos(q),r*math.sin(q),z-1),.7,'detail')
        mark('SHADE STACK',(64,-30,77),'STAGGERED RADIATIVE BARRIERS')
    with group('C'):
        vessel('cold capsule',(0,0,-62),30,80)
        with at((0,0,-62)):
            for z in (16,40,64):g.trim('cold collar',z,31.5,31.5)
        for z in (-47,-24,-1):
            box('payload shelf',(0,0,z),(42,42,2),3,'detail')
            for x in (-12,12):
                for y in (-12,12):
                    cyl('sealed sample vial',(x,y,z+2),5,17,'detail')
                    ring('vial retention lip',(x,y,z+17),5.8,1,2,role='accent')
        for x in (-23,23):
            rod('payload vertical rail',(x,0,-51),(x,0,17),1.4,'detail')
        box('temperature logger',(0,-24,-27),(24,4,12),1.5,'detail')
        for x in (-7,0,7):cyl('logger indicator',(x,-27,-27),1,1,'accent',(0,-1,0))
        for a in (0,120,240):
            q=math.radians(a);tube('coolant return',[(32*math.cos(q),32*math.sin(q),-50),(38*math.cos(q),38*math.sin(q),-22),(32*math.cos(q),32*math.sin(q),10)],1)
        mark('COLD CAPSULE',(0,-31,-28),'PASSIVE THERMAL HOLD')
    uncover('C','cold capsule','conformal vessel seam')
    for x,y in ((42,0),(-21,36),(-21,-36)):rod('insulating suspension',(x,y,60),(x*.6,y*.6,16),2)
    truss((0,0,-132),(0,0,-66),17,6)
    cyl('electric engine',(0,0,-142),20,16);ring('ion optics',(0,0,-144),24,3,3);bolts((0,0,-145),20,12,size=1)
    for side in (-1,1):
        rod('solar deployment boom',(side*8,0,-115),(side*56,0,-115),2,'detail')
        joint((side*40,-5,-115),4,(0,1,0))
        panel('power blanket',(side*95,0,-115),(110,64),nx=11,ny=5)
    mark('ION DRIVE',(0,-18,-139),'LOW THRUST / LONG COAST')
    mark('POWER BLANKET',(94,0,-115),'HINGED SOLAR CELLS')
    return 21,24


def regolith_kite():
    # Surface-hopping excavator: rake mouth and shallow drum, no wheels.
    with group('B'):
        cyl('collection drum',(-46,0,30),27,92,'structure',(1,0,0))
        for x in (-45,45):flange('drum cheek',(x,0,30),29,(1,0,0),3)
        for a in range(0,360,45):
            q=math.radians(a);rod('scoop lip',(-43,27*math.cos(q),30+27*math.sin(q)),(43,27*math.cos(q),30+27*math.sin(q)),1.2,'detail')
        motor((48,0,30),12,24,(1,0,0))
        mark('SCOOP DRUM',(0,-26,27),'CONTROLLED TOOL REACTION')
    with group('C'):
        box('rake mouth',(0,-45,12),(100,19,9),3)
        for x in range(-45,46,9):rod('replaceable tooth',(x,-39,14),(x,-67,7),1.7)
        for x in (-39,39):rod('rake pivot',(x,-40,12),(x,-18,30),3)
        joint((-45,-19,30),6,(1,0,0));joint((42,-19,30),6,(1,0,0))
        mark('RAKE MOUTH',(0,-64,8),'PARTICLE SIZE CONTROL')
    hull('sample vault',[(-52,8,7,74),(-38,30,22,74),(38,30,22,74),(52,8,7,74)])
    for x in (-1,1):
        rod('landing leg',(x*36,15,63),(x*82,39,0),3)
        box('landing shoe',(x*82,39,0),(28,37,5),4)
        panel('power leaf',(x*98,18,66),(61,86),nx=7,ny=6)
    optics((0,-32,76),7,13)
    ring('lifting eye',(0,0,109),9,3,6,(0,1,0))
    for x in (-29,29):rod('vault lifting stay',(x,0,88),(0,0,108),2.5)
    tube('crane tether',[(0,2,117),(3,3,153),(6,4,182)],.55,'cable')
    mark('SAMPLE VAULT',(0,-28,77),'DUST SEALED TRANSFER BIN')
    mark('LANDING SHOE',(83,39,2),'LOW GRAVITY ANCHOR PAD')
    return 25,28


def comet_anchor():
    # Tripod feet and a central articulated penetrating screw.
    with group('B'):
        cyl('drill cartridge',(0,0,44),16,68)
        motor((0,0,113),21,31)
        rod('core shaft',(0,0,-25),(0,0,47),6)
        for j in range(8):
            pts=[]
            for t in range(33):
                a=T*t/32;pts.append((12*math.cos(a),12*math.sin(a),-22+j*8+t/4))
            tube('helical cutter flight',pts,.7,'detail')
        flange('core coupling',(0,0,40),19)
        mark('ANCHOR SCREW',(0,-12,12),'LOW TORQUE ICE PENETRATOR')
    with group('C'):
        for a in (0,120,240):
            with at(angle=a):
                rod('tripod link',(14,0,90),(70,0,4),4);rod('leg brace',(17,0,52),(63,0,15),2,'detail')
                box('landing pad',(73,0,1),(30,28,5),4)
                for y in (-8,8):rod('ice tooth',(78,y,0),(81,y,-8),1.5,'detail')
                joint((18,-4,90),7)
        mark('TOOTHED PAD',(75,0,2),'REACTION LOAD INTO SURFACE')
    ring('instrument shelf',(0,0,94),43,14,8)
    for a in range(0,360,90):
        with at(angle=a):box('instrument module',(33,0,109),(19,23,24),4)
    rod('telemetry mast',(22,0,119),(36,0,187),2)
    optics((36,-4,184),7,12);panel('high gain patch',(36,0,197),(30,29),nx=3,ny=3)
    mark('INSTRUMENT SHELF',(-31,-17,107),'CORE AND VOLATILE ANALYSIS')
    mark('TELEMETRY',(36,-16,184),'OPTICAL RELAY HEAD')
    return 27,24


def star_post():
    # A folded optical communication relay with a side aperture and dish.
    with group('B'):
        joint((0,0,45),23,(0,1,0))
        for x in (-31,31):rod('gimbal fork',(x,0,9),(x,0,58),5)
        optics((0,-10,56),30,65,(0,-1,0))
        for z in (38,75):rod('barrel stiffener',(-22,-17,z),(22,-17,z),1,'detail')
        mark('LASER TELESCOPE',(0,-76,56),'COHERENT OPTICAL LINK')
    with group('C'):
        with at((67,13,28),-25,'Y'):
            # Deep bowl generated by paraboloid rings and radial gores.
            vs=[];fs=[];n=64
            for j in range(10):
                r=4+j*3.3
                for k in range(n):a=T*k/n;vs.append((r*math.cos(a),r*math.sin(a),r*r/80))
            for j in range(9):
                for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
            g.mesh('acquisition dish',vs,fs);ring('dish rim',(0,0,14.2),34,1,1)
            for a in (0,120,240):
                q=math.radians(a);rod('feed tripod',(31*math.cos(q),31*math.sin(q),12),(0,0,38),.8,'detail')
            cyl('feed horn',(0,0,35),5,9,'accent')
        mark('ACQUISITION DISH',(75,13,49),'WIDE ANGLE RENDEZVOUS RADIO')
    hull('relay bus',[(-51,15,10,-15),(-35,29,22,-15),(35,29,22,-15),(51,15,10,-15)])
    for side in (-1,1):
        rod('panel hinge',(side*45,0,-15),(side*72,0,-15),3)
        panel('power wing',(side*122,0,-15),(93,121),nx=9,ny=10)
    radiator((0,44,-19),(71,23));optics((-30,-28,-13),6,12)
    mark('POWER WING',(-123,0,-15),'TWO AXIS SUN TRACKING')
    mark('STAR TRACKER',(-30,-40,-13),'INERTIAL POINTING REFERENCE')
    return 25,29
