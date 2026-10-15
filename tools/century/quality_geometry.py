"""Second architecture pass: purpose-built replacements, not detail overlays.

All component views are subsets of the same scene. Quiet Stair additionally
exports two explicit states from one set of vertical carriage coordinates.
"""
from contextlib import nullcontext
from .kit import *
from . import kit


def rail_arc(name,p,r,a0,a1,axis=(0,0,1),thick=2,depth=3,role='structure'):
    ring(name,p,r,thick,depth,axis,role,a0,a1)


def gear(p,r=16,teeth=20,axis=(0,1,0)):
    with at():
        b=len(g.parts);w=len(g.wires)
        ring('index wheel rim',(0,0,0),r,3,3)
        cyl('index hub',(0,0,-2),r*.25,7,'detail')
        for a in range(0,360,60):
            q=math.radians(a);rod('wheel spoke',(0,0,1),(r*.85*math.cos(q),r*.85*math.sin(q),1),1,'detail')
        for i in range(teeth):
            a=T*i/teeth
            with at((r*math.cos(a),r*math.sin(a),1.5),i*360/teeth):box('index tooth',(0,0,0),(3,2.3,3),.3,'detail')
        transform(b,w,Matrix.Translation(p)@Vector(axis).to_track_quat('Z','Y').to_matrix().to_4x4())


def foot(p,width=24):
    box('isolating shoe',p,(width,width*1.7,6),3)
    cyl('shoe adjuster',Vector(p)+Vector((0,0,3)),3,7,'detail')


def queue_garden():
    views(B=(14,18),C=(35,54))
    # Six physical latches store six events; an offset gear train is exposed.
    with group('B'):
        for z in (50,77,104,131,158,185):
            ring('indexed stem collar',(0,8,z),9,3,7)
            box('latch pawl',(-12,8,z+3),(12,6,5),1,'detail')
            rod('latch spring',(-16,8,z),(-16,8,z+11),.5,'cable')
        for x in (-6,6):rod('register guide',(x,8,40),(x,8,200),1.5)
        for i in range(6):
            z=54+i*27;angle=18+i*137.5
            with at((0,8,z),angle):
                joint((8,0,3),4)
                rod('leaf rocker',(8,0,3),(31,0,12),1.8)
                rod('pushrod',(4,3,-8),(24,3,9),.7,'cable')
                leaf('completion leaf',(21,0,8),(65,0,28),27,'structure')
                box('rocker travel stop',(12,0,-1),(5,8,4),.6,'detail')
        mark('LEAF MEMORY',(-12,8,160),'SIX LATCHES / SIX ACTUAL COMPLETIONS')
    with group('C'):
        with at((42,-24,18),-12):
            box('reader bed',(0,0,0),(40,46,7),4)
            for y in (-14,10):
                cyl('paper roller',(-18,y,7),3,36,'detail',(1,0,0));flange('roller bearing',(-19,y,7),5,(-1,0,0),1)
            box('ticket ribbon',(0,-28,7),(28,32,.8),.3,'shell')
            optics((0,8,27),5,15,(0,0,-1))
            for x in (-18,18):rod('reader yoke',(x,10,2),(x,10,27),1.5)
            rod('optics bridge',(-18,10,27),(18,10,27),2)
            motor((22,10,7),5,13,(1,0,0))
        mark('TICKET OPTICS',(44,-16,40),'EVENT INPUT / NOT A TIME ESTIMATE')
    # Open crescent plinth instead of a featureless flower pot.
    rail_arc('sculpted plinth',(0,8,0),48,15,320,thick=16,depth=12)
    rail_arc('plinth edge',(0,8,13),46,15,320,thick=2,depth=2,role='detail')
    for p in ((-33,-13,-5),(22,43,-5),(32,-29,-5)):foot(p,16)
    with at((-28,-7,32)):
        for y in (-3,7):box('gear bearing cheek',(0,y,0),(48,3,39),5,'detail')
        gear((0,-6,0),20,28,(0,-1,0));gear((26,-6,13),11,16,(0,-1,0))
        motor((26,7,13),8,21,(0,1,0))
    tube('index transfer',[(-3,2,45),(-3,2,59),(0,8,62)],1.4,'cable')
    for z in (68,122,176):rod('spine brace',(-23,22,z-15),(0,8,z),1,'detail')
    tube('curved service spine',[(-29,26,11),(-27,24,80),(-22,21,156),(-9,12,201)],3)
    mark('INDEX TRAIN',(-31,-14,32),'ONE COMPLETED POSITION / ONE DETENT')
    mark('RELEASE KEY',(-2,18,45),'RESET REQUIRES A NEW TICKET')
    return 27,23


def coral_cradle():
    views(B=(30,25),C=(18,48))
    # Open horseshoe nursery, removable cassettes and a compliant transfer saddle.
    rail_arc('nursery backbone',(0,0,8),77,12,322,thick=8,depth=10)
    rail_arc('circulation header',(0,0,24),81,12,322,thick=2,depth=3,role='detail')
    with group('C'):
        for i,a in enumerate((25,82,139,196,253)):
            with at((0,0,0),a):
                box('nursery cassette',(51,0,21),(39,32,6),5)
                for x in (40,59):
                    for y in (-8,8):
                        ring('fragment collet',(x,y,25),4,1,5,role='detail')
                        if (i+int(x))%2:
                            organic_branch('live fragment',[(x,y,30),(x+1,y,43),(x+4,y+1,53)],1.3,'structure')
                            for side in (-1,1):organic_branch('coral offshoot',[(x+1,y,40),(x+side*6,y+2,45),(x+side*8,y+3,48)],.7,'detail')
                for y in (-13,13):rod('cassette guide',(31,y,17),(72,y,17),1.5,'detail')
                box('cassette ID tab',(73,0,24),(6,13,3),1,'accent')
        mark('NURSERY CASSETTES',(51,8,24),'FOUR COLLETS EACH / LIFT OUT WHOLE')
    with group('B'):
        with at((0,-32,70)):
            ring('compliant transfer collar',(0,0,0),16,4,9)
            for a in (0,120,240):
                with at((0,0,0),a):
                    rod('flexure finger',(11,0,0),(7,0,-17),1,'detail')
                    box('soft base contact',(7,0,-19),(5,8,9),2,'accent')
            optics((0,0,32),6,20,(0,0,-1))
            for x in (-18,18):rod('camera support',(x,0,5),(x,0,35),1.3)
            box('camera bridge',(0,0,34),(40,13,7),2)
            box('transfer slide',(0,7,38),(33,22,10),3)
        mark('TRANSFER COLLAR',(-14,-40,70),'THREE CONTACTS / RIDES THE GANTRY')
    for x in (-53,53):
        rod('service arch leg',(x,37,17),(x,37,114),3)
        rod('gantry rail',(x,37,113),(x,-45,113),2)
    for y in (-34,-22):rod('cross slide',(-53,y,111),(53,y,111),2)
    motor((-58,-28,110),8,19,(-1,0,0))
    tube('head loom',[(-60,38,25),(-59,39,105),(-27,-28,122),(0,-28,109)],1.2,'cable')
    with at((0,76,27),90,'X'):
        ring('low shear duct',(0,0,0),20,3,29);rotor((0,0,11),15,5);motor((0,0,27),6,16)
    for a in (40,160,280):
        q=math.radians(a);rod('cradle leg',(68*math.cos(q),68*math.sin(q),8),(88*math.cos(q),88*math.sin(q),-15),3);foot((88*math.cos(q),88*math.sin(q),-18),20)
    mark('CIRCULATION',(0,66,27),'DUCTED ROTOR / NO SEALED TANK')
    mark('GANTRY',(-54,-25,114),'LIMITED FORCE TRANSFER / SHORT REACH')
    return 29,34


def tidal_loom():
    views(B=(18,26),C=(37,26))
    # Paired cartridges on a triangulated, swept support. Service spine is asymmetric.
    centres=[(-73,-5,73),(68,15,98)]
    for i,(x,y,z) in enumerate(centres):
        # B is one rotor cartridge; C is the wet-service saddle, not the second, matched cartridge.
        with (group('B') if i==0 else nullcontext()):
            ring('flow shroud',(x,y-18,z),43,4,34,(0,1,0))
            for yy in (y-18,y+14):ring('shroud lip',(x,yy,z),45,2,3,(0,1,0),'detail')
            rotor((x,y-3,z),36,5,(0,1,0),19)
            motor((x,y+6,z),10,34,(0,1,0))
            flange('generator extraction flange',(x,y+39,z),13,(0,1,0))
            for a in (0,120,240):
                q=math.radians(a);rod('stator stay',(x+39*math.cos(q),y+16,z+39*math.sin(q)),(x,y+30,z),2)
            for a in range(0,360,60):
                with at((x,y-16,z),a,'Y'):leaf('reversing guide vane',(17,0,0),(39,0,0),11,'detail')
            for a in (35,145,265):
                q=math.radians(a);box('removable cartridge latch',(x+43*math.cos(q),y+9,z+43*math.sin(q)),(7,13,8),2,'detail')
    for p in ((-113,42,5),(110,58,5),(15,-57,5)):
        cyl('seabed suction shoe',p,20,8);ring('shoe flange',Vector(p)+Vector((0,0,8)),22,3,3)
        bolts(Vector(p)+Vector((0,0,12)),20,8,size=1)
    for p,q in [((-113,42,17),(-73,29,111)),((110,58,17),(68,48,135)),((15,-57,17),(-73,15,38)),((15,-57,17),(68,35,58))]:truss(p,q,10,5)
    truss((-75,36,118),(69,55,143),13,10)
    with group('C'):
        box('wet service saddle',(33,58,148),(48,27,20),6)
        for i in range(5):cyl('wet mate socket',(15+i*8,43,148),2.4,8,'accent',(0,-1,0))
    tube('power collection',[(-73,44,73),(-83,51,113),(27,65,146),(68,57,98)],2,'cable')
    with group('C'):
        rod('recovery mast',(47,62,149),(47,62,180),3)
        ring('recovery eye',(47,62,189),9,3,6,(0,1,0))
        # Wet-mate face: a collar round every socket, two guide posts for the ROV and clamp bolts on the lid.
        for i in range(5):ring('socket collar',(15+i*8,44,148),3.6,.9,2,(0,-1,0),'detail')
        for x in (11,55):rod('rov guide post',(x,45,141),(x,36,141),1.2,'detail')
        for x in (16,26,36):
            for y in (49,67):cyl('lid clamp bolt',(x,y,158),1.1,1.6,'detail',n=6)
        flange('mast flange',(47,62,158),6.5,depth=2.5)
    mark('REMOVABLE ROTOR',(-73,-23,73),'MATCHED GENERATOR CARTRIDGES')
    mark('WET SERVICE SPINE',(34,42,149),'ONE RECOVERY SIDE / DRY-DECK MAINTENANCE')
    mark('BALLAST SHOE',(15,-57,14),'RECOVERABLE SEABED CONNECTION')
    mark('TRANSIT CORRIDOR',(-2,20,72),'NO CROSS BRACE THROUGH CENTRAL GAP')
    return 21,25


def manta_foil():
    from .mobility import cabin
    views(B=(44,15),C=(125,20))
    # Long wave-piercing bows support a shorter raised passenger bridge.
    for side in (-1,1):
        with at((0,side*30,0)):
            o=hull('wave piercing demi-hull',[(-140,1,1,33),(-108,9,12,33),(-55,12,17,35),(58,10,13,36),(104,6,8,39),(113,2,3,41)])
            for x in (-81,5,68):hull_seam(o,x)
    hull('wing deck',[(-92,4,2,52),(-60,39,7,53),(45,40,7,55),(84,20,4,53),(98,2,2,51)])
    cabin('swept passenger salon',(-7,0,75),134,61,36)
    for side in (-1,1):
        with at((0,side*34,0)):
            tube('boarding rail',[(26,0,59),(27,0,68),(62,0,68),(66,0,60)],.65,'detail')
            for x in (32,45,58):rod('rail stanchion',(x,0,59),(x,0,68),.5,'detail')
            box('boarding landing',(62,0,58),(27,17,3),3,'detail')
            for x in (54,60,66):rod('landing grip',(x,-6,60),(x,6,60),.35,'detail')
    with group('B'):
        # Paired hinged struts and a true spanwise lifting foil.
        for side in (-1,1):
            y=side*31
            joint((-45,y,35),8,(0,1,0))
            rod('retracting foil strut',(-45,y,34),(-32,y,-30),3)
            rod('foil retraction ram',(-62,y,44),(-42,y,16),2,'detail')
            flange('root lock',(-45,y-7,35),10,(0,-1,0),2)
        for side in (-1,1):leaf('main hydrofoil',(-32,0,-30),(-17,side*75,-28),24)
        rod('foil spar',(-25,-69,-29),(-25,69,-29),1.2,'detail')
        mark('RETRACTABLE FOILS',(-43,-37,32),'TWO HINGED STRUTS / ONE SPANWISE FOIL')
    with group('C'):
        for side in (-1,1):
            y=side*28
            rod('aft control strut',(65,y,33),(71,y,-14),3)
            ring('axial propulsor duct',(69,y,-17),12,2,23,(1,0,0))
            rotor((74,y,-17),9,5,(1,0,0));motor((81,y,-17),4,13,(1,0,0))
            for a in (0,120,240):
                q=math.radians(a);rod('propulsor stator',(91,y+10*math.cos(q),-17+10*math.sin(q)),(88,y,-17),.6,'detail')
            leaf('aft trim foil',(71,y,-12),(76,side*56,-11),15)
        mark('TWIN PROPULSORS',(86,-28,-16),'AXIAL THRUST / GUARDED AT LOW SPEED')
    box('roof service spine',(18,0,96),(39,19,6),4)
    for x in range(3,34,5):rod('roof cooling slot',(x,-7,100),(x,7,100),.4,'detail')
    rod('navigation mast',(39,0,99),(48,0,124),1.2);optics((47,-3,122),4,8)
    for side in (-1,1):cyl('navigation light',(-70,side*26,76),2,3,'accent',(0,side,0))
    mark('PASSENGER BRIDGE',(-13,-30,78),'RAISED SALON / RECESSED SIDE BOARDING')
    mark('FINE ENTRY BOW',(-108,-30,36),'SLENDER WATERLINE / WIDE DECK ABOVE')
    return 24,21


def seam_surgeon():
    views(B=(52,22),C=(155,50))
    # Short cut pipe ends provide scale; the double orbital track is the subject.
    for x in (-26,4):ring('short pipe context',(x,0,68),31,2,24,(1,0,0),'shell')
    for x in (-7,12):
        ring('split orbital track',(x,0,68),53,5,5,(1,0,0))
        for a in range(0,360,30):
            q=math.radians(a);cyl('track cap screw',(x+5,50*math.cos(q),68+50*math.sin(q)),1.2,2,'detail',(1,0,0),6)
    for a in (30,150,270):
        q=math.radians(a);rod('track spacer',(-7,49*math.cos(q),68+49*math.sin(q)),(16,49*math.cos(q),68+49*math.sin(q)),2)
    for z in (15,121):
        box('split rail latch',(4,-3,z),(32,14,9),2)
        cyl('latch pin',(-14,-3,z),2,36,'detail',(1,0,0))
    with group('B'):
        with at((0,0,68),-18,'X'):
            box('orbital tool saddle',(3,-54,0),(38,15,35),4)
            for x in (-7,15):
                for z in (-12,12):cyl('vee guide wheel',(x,-49,z),5,5,'detail',(1,0,0))
            rod('torch feed rail',(0,-64,-18),(0,-64,18),2,'detail')
            box('torch carriage',(0,-65,2),(15,11,16),2)
            rod('torch throat',(0,-60,2),(0,-32,2),2.5,'accent')
            ring('torch ceramic nozzle',(0,-35,2),4,1,5,(0,1,0),'detail')
            motor((11,-68,7),8,23,(0,1,0))
            # Visible wire reel and guided feed, not a mysterious trailing cable.
            cyl('filler wire spool',(-19,-65,21),13,9,'detail',(1,0,0))
            for x in (-20,-10):ring('spool flange',(x,-65,21),14,2,1,(1,0,0))
            tube('filler guide',[(-13,-75,24),(-4,-79,11),(0,-46,4)],.6,'cable')
        mark('WELD TRAIN',(-8,-55,96),'ORBIT / FEED / FILLER / SHIELD GAS')
    with group('C'):
        with at((0,0,68),119,'X'):
            box('inspection bogie',(3,-49,0),(36,14,31),3)
            for x in (-8,15):
                for z in (-10,10):cyl('inspection contact wheel',(x,-39,z),4,5,'detail',(1,0,0))
            box('inspection array',(3,-33,0),(23,4,12),1,'accent')
            for x in (-5,0,5,10):rod('array division',(x,-35,-5),(x,-35,5),.2,'detail')
            for z in (-9,9):rod('compliant probe link',(3,-45,z),(3,-34,z),1,'detail')
            optics((3,-55,0),6,15,(0,1,0))
            box('shoe junction',(23,-45,0),(9,12,18),2,'detail')
        mark('INSPECTION ARRAY',(-10,26,20),'SEGMENTED ARRAY ON CONTACT WHEELS')
    uncover('B','orbital tool saddle')
    uncover('C','inspection bogie')
    with at((0,0,68),215,'X'):
        box('preparation carriage',(3,-52,0),(31,17,24),3)
        motor((2,-67,0),7,22,(0,1,0))
        cyl('preparation brush',(-6,-34,0),7,17,'detail',(1,0,0))
        for x in range(-5,10,3):ring('brush lamella',(x,-34,0),7,.5,1,(1,0,0),'shell')
    for x in (-15,20):
        for y in (-33,33):rod('collar shoe',(x,y,29),(x,y*1.7,1),2.5)
    box('gas power cassette',(51,32,37),(32,41,65),7)
    for z in range(14,64,6):rod('power cooling slot',(68,19,z),(68,44,z),.5,'detail')
    # Over the top of the outer track, never across the bore.
    tube('torch service',[(51,13,50),(55,40,110),(30,10,138),(5,-45,126),(-2,-70,85)],1.3,'cable')
    mark('PREPARATION HEAD',(3,34,103),'CLEAN FIRST / THEN CONTROLLED WELD PASS')
    mark('SPLIT TRACK',(14,52,64),'CLAMP AROUND THE JOINT / NO PIPE REMOVAL')
    return 48,24


def meeting_buoy():
    views(B=(17,22),C=(15,50))
    # A tabletop semaphore chronometer with a visible clockwork time comparator.
    with group('B'):
        for x in (-21,21):rod('semaphore upright',(x,7,20),(x,7,149),2)
        for z in (41,99,148):box('upright bridge',(0,7,z),(51,16,8),3)
        rod('flag rack',(0,5,44),(0,5,174),3,'detail')
        for z in range(48,153,6):box('rack tooth',(4,4,z),(3,3,3),.4,'detail')
        gear((15,-4,92),11,20,(0,-1,0))
        motor((15,13,92),8,17,(0,1,0))
        for z in (64,123):
            for x in (-6,6):cyl('flag rack guide',(x,0,z),4,8,'detail',(0,1,0))
        # Rigid, tapered enamel semaphore flag; retains the original visual joke.
        g.mesh('raised signal flag',[(2,5,163),(63,5,163),(49,5,190),(2,5,190)],[(0,1,2,3)],'accent')
        g.wire('flag border',[(2,4.8,163),(63,4.8,163),(49,4.8,190),(2,4.8,190),(2,4.8,163)],.3,'detail')
        mark('SEMAPHORE RACK',(6,4,125),'FORMAT TIME EXCEEDS SUBJECT TIME')
    with group('C'):
        rail_arc('microphone perimeter',(0,0,23),42,195,345,thick=5,depth=9)
        for a in (205,237,269,301,333):
            q=math.radians(a);x,y=40*math.cos(q),40*math.sin(q)
            cyl('microphone capsule',(x,y,33),4,7,'detail')
            ring('capsule mesh',(x,y,40),4,1,1,role='accent')
            for off in (-2,0,2):rod('mesh slit',(x-2,y+off,41),(x+2,y+off,41),.15,'detail')
        box('classifier board',(0,-14,25),(44,20,2),1,'detail')
        for x in (-14,0,14):box('board package',(x,-14,28),(8,11,4),1,'detail')
        mark('MICROPHONE ARRAY',(0,-41,38),'LISTENS TO THE ROOM / MUTES NOBODY')
    hull('chronometer pedestal',[(-57,4,3,8),(-43,32,10,11),(31,39,11,11),(56,13,5,8)])
    for x,y in ((-37,-20),(32,-25),(25,27)):foot((x,y,-1),15)
    # Upright differential clock face, partial bezel leaves gears visible.
    rail_arc('clockwork bezel',(-3,-8,72),37,15,335,(0,-1,0),4,4)
    for x,z,r in ((-16,68,16),(12,75,12),(1,52,10)):
        gear((x,-12,z),r,24,(0,-1,0))
    cyl('time pointer spindle',(-3,-17,72),2,3,'accent',(0,-1,0))
    rod('elapsed time pointer',(-3,-20,72),(-19,-20,95),.65,'accent')
    for a in range(0,360,30):
        q=math.radians(a);rod('clock index',(-3+32*math.cos(q),-14,72+32*math.sin(q)),(-3+35*math.cos(q),-14,72+35*math.sin(q)),.4,'detail')
    box('reset paddle',(49,-3,28),(22,30,7),3)
    for x in (-11,0,11):cyl('status jewel',(x,-35,14),2,2,'accent',(0,-1,0))
    mark('TIME COMPARATOR',(-16,-17,69),'ELAPSED TIME / NO PRODUCTIVITY SCORE')
    mark('RESET PADDLE',(51,-3,32),'ANOTHER MEETING IS NOT A RESET')
    return 25,22


def wind_kite():
    views(B=(-28,58),C=(14,62))
    # Airfoil shell with an exposed starboard wing bay; short illustrated tether.
    with group('C'):
        for side in (-1,1):
            for u in (20,40,60,80,100,119):
                x=side*u;yy=14+.20*u;zz=155+.08*u;ch=48-.21*u
                pts=[(x,yy-ch*.48,zz),(x,yy-ch*.34,zz+5),(x,yy+ch*.12,zz+6),(x,yy+ch*.5,zz),(x,yy-ch*.48,zz)]
                vs=[(x+off,y,z) for off in (-.6,.6) for _,y,z in pts[:4]]
                g.mesh('airfoil rib',vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'detail')
            organic_branch('wing spar',[(side*9,16,156),(side*69,29,162),(side*126,42,170)],2,'structure')
            organic_branch('trailing spar',[(side*9,40,157),(side*68,47,164),(side*126,53,170)],1.2,'structure')
        for side in (-1,1):
            for u in (20,40,60,80,100):
                rod('wing bay diagonal',(side*u,14+.20*u,157+.08*u),(side*(u+19),14+.20*(u+19)+12,157+.08*(u+19)),.65,'detail')
        for x in (-24,24):box('bridle hardpoint',(x,22,151),(16,12,9),2)
        mark('SWEPT SPAR',(67,30,163),'SWEEPS BACK TO CANTED TIPS')
    for side in (-1,1):
        # Same geometry on both sides; near/starboard inspection opening is physical.
        for band in range(6):
            if side==1 and band in (1,2,3):continue
            vs=[]
            for u in (band*21,(band+1)*21):
                yy=14+.20*u;zz=155+.08*u;ch=48-.21*u
                for f,h in ((-.48,0),(-.34,5),(.12,6),(.5,0)):
                    vs.append((side*u,yy+ch*f,zz+h))
            g.mesh('wing skin panel',vs,[(0,1,5,4),(1,2,6,5),(2,3,7,6)],'shell')
        leaf('canted wingtip',(side*120,44,165),(side*136,57,198),24)
        box('trim servo',(side*78,45,167),(15,10,5),2,'detail')
        rod('flap linkage',(side*78,45,166),(side*80,51,164),.5,'cable')
    hull('flight control keel',[(-17,2,2,152),(-5,9,9,154),(37,8,7,154),(63,1,1,154)],'Y')
    for x in (-24,24):tube('bridle',[(x,22,149),(0,8,115)],.3,'detail')
    tube('traction tether',[(0,8,115),(-4,-1,92),(-15,-9,62)],.45,'accent')
    with group('B'):
        with at((-14,-15,31),-12):
            cyl('traction drum',(-25,0,0),23,50,'structure',(1,0,0))
            for x in (-29,25):flange('drum flange',(x,0,0),28,(1,0,0),3)
            for x in range(-21,23,3):ring('tether winding',(x,0,0),23.5,.5,1,(1,0,0),'detail')
            for x in (-31,31):box('bearing saddle',(x,0,-13),(12,32,26),4)
            motor((35,0,0),13,32,(1,0,0))
            for x in (-25,25):rod('level wind rail',(x,-33,19),(x,33,19),1.5,'detail')
            rod('traversing screw',(-28,-26,19),(28,-26,19),2,'detail')
            ring('tether fairlead',(-3,-26,22),5,1.5,4,(0,1,0))
        mark('TRACTION WINCH',(-12,-33,33),'GENERATOR AND RETURN DRIVE')
    for side in (-1,1):
        rod('outrigger',(-10,0,2),(side*82,-44,-7),3)
        foot((side*82,-44,-10),22)
    foot((-2,51,-10),22)
    truss((-51,19,3),(33,19,3),12,6)
    box('power interface',(42,36,18),(33,28,35),6)
    for z in range(7,33,5):rod('inverter fin',(60,25,z),(60,45,z),.6,'detail')
    optics((-47,-26,36),6,13,(0,-1,.25))
    mark('TRACKING HEAD',(-47,-38,40),'GROUND OPTICS / FOLLOWS THE WING')
    mark('BRIDLE',(0,8,115),'TWO LINES SHARE THE PULL')
    return 24,29


def sleep_cocoon():
    # Keep the measured shared occupant and four-bar, replace the chair silhouette.
    from .wearables import sleep_cocoon as seated
    seated()
    canopy_start=len(g.parts);canopy_wire_start=len(g.wires)
    # Five shaped ribs wrap behind the back and over the head, open at the face.
    for x in (-31,-16,0,16,31):
        organic_branch('cocoon structural rib',[(x,19,11),(x,28,43),(x,26,82),(x,19,106),(x,-3,118),(x,-24,115)],1.5,'structure')
    # Side shell petals create a purposeful cocoon without hiding the human.
    for side in (-1,1):
        vs=[]
        for y,z,w in ((21,10,25),(29,35,31),(29,68,34),(23,99,34),(0,116,28),(-25,113,25)):
            vs.extend([(side*w,y,z),(side*(w+9),y-12,z-3)])
        g.mesh('acoustic side petal',vs,[(i,i+1,i+3,i+2) for i in range(0,10,2)],'structure')
        tube('petal rolled rim',[vs[i] for i in range(1,12,2)],.5,'detail')
        for z in (32,57,82):
            box('shell isolation mount',(side*28,25,z),(6,11,9),2,'detail')
        cyl('canopy hinge',(side*33,20,95),7,5,'detail',(side,0,0))
        flange('canopy hinge cap',(side*38,20,95),8,(side,0,0),2)
    # Perforated crown bridges the ribs above the occupant; no face occlusion.
    for x in range(-27,28,6):rod('crown acoustic slat',(x,1,117),(x,-20,116),.6,'detail')
    box('air cassette',(0,33,62),(30,12,49),5)
    for z in range(45,83,6):rod('return vent',(-10,40,z),(10,40,z),.5,'detail')
    for side in (-1,1):
        tube('low speed air duct',[(side*10,35,77),(side*22,26,103),(side*20,-8,115)],1.2,'cable')
        rod('skid',(side*32,29,-6),(side*32,-44,-6),3)
    # Crown clearance measured from the actual head mesh, not guessed from joint Z.
    transform(canopy_start,canopy_wire_start,Matrix.Diagonal((1,1,1.36,1)))
    from .humans import CACHE
    head_top=max(v.z for name,vs,fs in CACHE['seated'][0] if name=='head' for v in vs)
    bottom=min(v.z for name,vs,fs in CACHE['seated'][0] for v in vs)
    head_world=(head_top-bottom)*.28
    assert 113*1.36 > head_world+7, (head_world,'insufficient canopy clearance')
    # Use the actual cradle in B and add its crown linkage, not an unrelated part.
    with group('B'):
        for side in (-1,1):
            rod('headrest height rail',(side*14,17,93),(side*14,17,124),1.2,'detail')
            box('headrest lock',(side*14,16,107),(7,6,10),2,'detail')
        tube('release loop',[(-11,23,83),(-11,28,69),(11,28,69),(11,23,83)],.7,'accent')
    # Existing four explanatory anchors retain their actual rig coordinates.
    return 31,19


def stair_height(index,mode):
    """Fixed x; separate vertical screws. Empty treads level before occupancy."""
    if mode=='stairs':return 16+index*17
    if mode=='low':return 16
    if mode=='high':return 67
    raise ValueError(mode)


def stair_treads(mode,detail=True):
    for i in range(4):
        x=-66+i*44;z=stair_height(i,mode)
        box('level tread '+str(i),(x,0,z),(43,84,6),3)
        for xx in (-12,0,12):rod('anti slip rib',(x+xx,-37,z+3.1),(x+xx,37,z+3.1),.35,'detail')
        if detail:
            for y in (-46,46):
                box('tread carriage',(x,y,z-4),(32,12,13),3,'detail')
                for xx in (-10,10):cyl('carriage roller',(x+xx,y-7,z-3),3,3,'detail',(0,-1,0))
                # Two nested blade guards retract into a fixed side sill.
                box('riser guard',(x+21,0,z-8),(1.3,77,9),.4,'shell')


def quiet_stair():
    views(B=(22,22),C=(-64,26))
    stair_treads('stairs')
    for y in (-56,56):
        # Shaped outboard sills house four independent screw axes.
        hull('side drive sill',[(-100,4,3,5),(-88,11,10,8),(80,11,10,8),(99,4,3,5)],'X').location.y=y
        for i in range(4):
            x=-66+44*i
            with group('B' if y<0 and i==1 else 'axes'):
                for xx in (-13,13):rod('vertical guide',(x+xx,y,11),(x+xx,y,78),1.8)
                rod('lift screw',(x,y,11),(x,y,78),1.8,'detail')
                for z in range(13,78,4):ring('screw thread',(x,y,z),2.3,.6,.7,role='detail')
                box('top bearing bridge',(x,y,81),(33,16,8),3)
                motor((x,y,-13),7,21)
                z=stair_height(i,'stairs')
                box('travelling nut',(x,y,z),(10,12,12),2,'detail')
                rod('tread load bridge',(x,y,z-3),(x,y*.8,z-3),3)
                for z0 in (13,70):box('end stop',(x+16,y,z0),(5,8,7),1,'accent')
    with group('C'):
        # Same safety rail as the main machine, now facing the working side.
        box('edge carrier extrusion',(-87,0,17),(7,84,9),1.8)
        box('edge removable elastomer lip',(-93,0,17),(4,80,10),2,'accent')
        for y in range(-33,34,11):
            box('contact cell saddle',(-91,y,17),(3,8,7),1,'detail')
            box('moving contact pad',(-93,y,17),(1,5,5),.7,'accent')
            for z in (14.6,19.4):
                rod('compliant contact leaf',(-90,y-3,z),(-94,y+2,z),.32,'detail')
            cyl('cell retainer',(-93,y+3,17),.7,1,'detail',(-1,0,0),8)
        for y in (-42,42):
            box('end seal',(-90,y,17),(10,3,11),1.5)
            box('edge mounting ear',(-84,y,13),(10,7,9),1.6)
            cyl('mounting fastener',(-90,y,12),1.2,2,'detail',(-1,0,0),6)
        tube('edge return bus',[(-91,-37,13),(-91,36,13)],.4,'cable')
        cyl('sealed cable gland',(-88,-46,17),2.2,6,'detail',(0,-1,0),20)
        for y in (-48,-50,-52):ring('gland grip',(-88,y,17),2.4,.5,.6,(0,-1,0),'detail')
        tube('edge loom',[(-88,-53,17),(-88,-58,14),(-78,-60,12),(-66,-51,12)],.5,'cable')
    uncover('C','edge removable elastomer lip')
    for y in (-66,66):
        for x in (-91,91):rod('fixed handrail post',(x,y,10),(x,y,128),2)
        organic_branch('fixed handrail',[(-91,y,117),(-91,y,130),(91,y,130),(91,y,117)],2,'structure')
        for i in range(3):rod('side infill',(-91+i*60,y,76),(-31+i*60,y,76),.6,'shell')
    for x,side in ((-91,1),(91,-1)):
        for z in (88,125):
            cyl('entry gate hinge',(x,-66,z),3,6,'detail')
            rod('folded gate rail',(x,-66,z),(x+side*66,-66,z),1.2)
        rod('gate return',(x+side*66,-66,88),(x+side*66,-66,125),1.2)
        box('gate interlock',(x,-64,83),(9,9,11),2,'accent')
    box('controller',(103,28,38),(27,35,59),6)
    for z in range(18,60,7):rod('controller vent',(118,19,z),(118,38,z),.5,'detail')
    box('manual release',(112,-7,46),(18,16,22),3,'detail')
    for y in (-53,53):
        for x in (-91,91):foot((x,y,-19),20)
    mark('VERTICAL CARRIAGES',(-22,-56,36),'FIXED TREAD X / INDEPENDENT Z AXES')
    mark('LEVEL DECK',(22,-18,50),'TREADS LEVEL INTO ONE DECK')
    mark('SAFETY EDGE',(-90,-20,17),'INHIBITS MOVEMENT WHEN OBSTRUCTED')
    mark('MANUAL RELEASE',(118,-9,46),'SERVICE OVERRIDE / MODE LOCK FIRST')
    # Numerical endpoints deliberately checked independently of the visible drawing.
    report={'equation':'stairs z_i=16+17*i; level-low z_i=16; level-high z_i=67',
      'fixed_tread_centres':[-66,-22,22,66],'tread_width':43,'gap':1,
      'states':{m:[stair_height(i,m) for i in range(4)] for m in ('stairs','low','high')},
      'sequence':['empty stair','level to low deck','occupy locked deck','lift whole level deck','exit at high landing'],
      'limitation':'Authored kinematic concept; not a certified public-access lift or collision simulation.'}
    assert len(set(report['states']['low']))==len(set(report['states']['high']))==1
    (ROOT/'concepts/century/qa/quiet-stair-kinematics.json').write_text(json.dumps(report,indent=2)+'\n')
    return 27,28


BUILDERS={2:tidal_loom,6:manta_foil,38:quiet_stair,42:wind_kite,44:coral_cradle,
          60:meeting_buoy,65:seam_surgeon,70:queue_garden,99:sleep_cocoon}
