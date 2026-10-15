"""Transport architectures: hydrofoil, tracked sled, cable cabin, modular freight."""
from .kit import *


def cabin(name,p,length=120,width=49,height=39):
    x,y,z=p
    with at(p):
        hull(name,[(-length*.55,2,3,0),(-length*.39,width*.42,height*.35,0),(-length*.1,width*.5,height*.5,2),(length*.35,width*.42,height*.44,0),(length*.48,5,6,-4)])
        # Conformal windows follow the actual loft rather than guessed ellipses.
        sections=[(-length*.55,2,3,0),(-length*.39,width*.42,height*.35,0),(-length*.1,width*.5,height*.5,2),(length*.35,width*.42,height*.44,0),(length*.48,5,6,-4)]
        def surface(x,t,side):
            rx,rz,lift=profile_at(sections,x)
            z=lift+rz*t;y=rx*max(.001,1-abs(t)**(2/.7))**(.7/2)
            return(x,side*(y+.48),z)
        for side in (-1,1):
            for left,right in ((-.32,-.14),(-.10,.10),(.14,.31)):
                corners=[(left,.13),(right,.13),(right,.67),(left,.67),(left,.13)];pts=[]
                for a,b in zip(corners,corners[1:]):
                    for k in range(17):
                        t=k/16;pts.append(surface(length*(a[0]+t*(b[0]-a[0])),a[1]+t*(b[1]-a[1]),side))
                g.wire('conformal glazing seal',pts,.09,'detail')
            pts=[surface(length*(-.34+.68*k/48),-.18,side) for k in range(49)]
            g.wire('lower cabin belt seam',pts,.08,'shell')


def manta_foil():
    hull('manta hull',[(-116,2,3,39),(-87,23,11,40),(-40,35,14,40),(60,34,15,40),(101,17,9,40),(115,2,3,40)])
    cabin('passenger cabin',(0,0,68),128,48,39)
    with group('B'):
        rod('foil strut',(-53,0,28),(-53,0,-35),5)
        joint((-53,-7,20),10)
        for side in (-1,1):leaf('retractable foil',(-53,0,-34),(-42,side*77,-34),25,'structure')
        rod('retraction ram',(-73,0,18),(-54,0,-17),2,'detail')
        flange('root bearing',(-53,-11,20),12,(0,-1,0),3)
        mark('FOIL ROOT',(-53,-12,18),'RETRACTS FOR SHALLOW DOCKS')
    with group('C'):
        ring('propulsor duct',(80,-14,8),20,3,29,(0,1,0))
        rotor((80,0,8),15,5,(0,1,0))
        motor((80,14,8),7,19,(0,1,0))
        for a in (0,120,240):
            q=math.radians(a);rod('motor stay',(80+17*math.cos(q),17,8+17*math.sin(q)),(80,28,8),1,'detail')
        mark('DUCTED PROPULSOR',(83,-16,9),'GUARDED LOW SPEED THRUST')
    rod('aft foil strut',(67,0,28),(67,0,-25),4)
    for side in (-1,1):leaf('aft control foil',(67,0,-25),(73,side*44,-25),18)
    for x in (-85,74):
        for side in (-1,1):rod('deck handrail',(x,side*25,47),(x,side*25,59),.8,'detail')
    rod('roof mast',(8,0,90),(8,0,113),1.5);optics((8,-4,108),4,8)
    mark('CABIN',(0,-24,69),'ENCLOSED HARBOUR PASSENGER SPACE')
    mark('AFT FOIL',(73,-36,-25),'PITCH TRIM AND RIDE CONTROL')
    return 28,20


def track(p,length=114,width=25,r=17):
    with at(p):
        for x in (-length*.35,0,length*.35):
            cyl('bogie wheel',(x,-width/2,r),r,width,'structure',(0,1,0));ring('wheel hub',(x,-width/2-2,r),r*.5,2,2,(0,1,0),'detail')
        for z in (0,2*r):
            for x in range(-int(length/2),int(length/2)+1,6):box('track shoe',(x,0,z),(4,width+5,3),1,'detail')
        for side in (-1,1):
            pts=[]
            for i in range(33):
                a=-math.pi/2+math.pi*i/32;pts.append((side*length*.35+side*r*math.cos(a),-width/2-1,r+r*math.sin(a)))
            g.wire('track end',pts,.8,'structure')
        rod('bogie suspension',(-length*.35,0,r),(length*.35,0,r),4)


def snow_thread():
    with group('B'):
        track((0,-42,0),129,32,18)
        for x in (-39,39):rod('bogie suspension',(x,-43,18),(x,-23,45),3,'detail')
        mark('TRACK BOGIE',(0,-60,19),'WIDE SHOES / SHARED GROUND LOAD')
    track((0,42,0),129,32,18)
    hull('snow carrier hull',[(-89,10,8,52),(-63,36,20,52),(64,36,20,52),(87,11,8,52)])
    with group('C'):
        rod('snow probe arm',(-69,0,46),(-109,0,20),3)
        box('probe skid',(-111,0,8),(35,42,7),6)
        for y in (-14,0,14):rod('probe electrode',(-120,y,5),(-108,y,5),1,'accent')
        joint((-71,-5,44),6);rod('probe spring',(-91,0,21),(-94,0,42),1,'detail')
        optics((-115,-5,19),4,8,(-1,0,0))
        mark('SNOW PROBE',(-116,-10,10),'MEASURES AHEAD OF THE LOAD')
    cabin('operator cabin',(-38,0,84),55,43,34)
    for x in (11,44):box('supply case',(x,0,88),(29,49,37),6)
    for y in (-30,30):rod('cargo rail',(-1,y,73),(63,y,73),2,'detail')
    tube('exhaust-free service conduit',[(55,30,47),(63,24,67),(59,12,84)],1.5,'cable')
    mark('SUPPLY CASE',(44,-26,91),'INSULATED FIELD PAYLOAD')
    mark('CABIN',(-45,-20,91),'LOW CENTRE OF MASS')
    return 27,23


def canyon_car():
    with group('B'):
        for y in (-17,17):
            for x in (-32,32):
                cyl('traction wheel',(x,y,150),13,7,'structure',(0,1,0));ring('wheel groove',(x,y-1,150),14,1,2,(0,1,0),'detail')
            rod('bogie spine',(-45,y,141),(45,y,141),3)
            motor((0,y,145),9,21,(1,0,0))
        for x in (-31,31):rod('wheel crosshead',(x,-24,141),(x,24,141),3)
        mark('TRACTION BOGIE',(31,-21,151),'PAIRED CABLE CONTACT')
    with group('C'):
        for y in (-12,12):rod('cabin hanger',(0,y,140),(0,y,76),4)
        joint((0,-17,137),10);joint((0,-17,79),11)
        rod('sway damper',(0,-12,127),(18,-12,89),2,'detail')
        box('hanger saddle',(0,0,74),(43,42,11),4)
        for x in (-15,15):cyl('saddle fastener',(x,0,80),2,3,'detail',n=6)
        mark('CABIN HANGER',(0,-14,108),'PENDULAR COMFORT / DAMPED SWAY')
    cabin('cable cabin',(0,0,42),123,63,63)
    for y in (-17,17):rod('support cable',(-103,y,163),(103,y,163),.8,'detail')
    for x in (-28,28):
        for y in (-29,29):rod('door seam',(x,y,23),(x,y,52),.55,'detail')
    box('cab floor',(0,0,11),(85,47,7),5)
    box('roof rescue hatch',(20,0,76),(25,28,3),3,'detail')
    mark('CABIN',(20,-31,42),'COMPACT VALLEY CROSSING')
    mark('SUPPORT CABLE',(-72,-17,163),'PAIRED FIXED TRACK ROPES')
    return 25,20


def rescue_fan():
    with group('B'):
        ring('lift duct',(-65,-43,109),34,5,19)
        rotor((-65,-43,117),27,7)
        for a in (0,120,240):
            q=math.radians(a);rod('motor bridge',(-65+28*math.cos(q),-43+28*math.sin(q),129),(-65,-43,130),1.5,'detail')
        motor((-65,-43,121),9,15)
        mark('LIFT DUCT',(-64,-43,130),'GUARDED ROTOR ABOVE OBSTACLES')
    for x,y in ((65,-43),(-65,43),(65,43)):
        ring('lift duct',(x,y,109),34,5,19);rotor((x,y,117),27,7);motor((x,y,121),9,15)
        for a in (0,120,240):
            q=math.radians(a);rod('motor bridge',(x+28*math.cos(q),y+28*math.sin(q),129),(x,y,130),1.5,'detail')
    with group('C'):
        hull('stretcher shell',[(-69,3,3,22),(-51,24,12,22),(49,24,12,22),(69,3,3,22)])
        for x in (-40,20):
            tube('patient restraint',[(x,-23,26),(x,-15,40),(x,15,40),(x,23,26)],1,'accent')
        for y in (-25,25):rod('stretcher handle',(-50,y,35),(50,y,35),1.5,'detail')
        box('head cushion',(-43,0,31),(24,27,9),4,'detail')
        mark('STRETCHER CRADLE',(0,-24,25),'PATIENT POD / NO FIGURE FITTED')
    hull('flight spine',[(-56,7,6,115),(-39,20,13,115),(39,20,13,115),(56,7,6,115)])
    for x in (-65,65):rod('rotor spar',(x,-43,114),(x,43,114),4)
    for y in (-20,20):rod('longitudinal spine',(-65,y,113),(65,y,113),3)
    for x in (-45,45):
        for y in (-18,18):rod('suspension line',(x,y,108),(x,y,38),.6,'detail')
    optics((0,-21,114),8,15)
    for x in (-83,83):rod('landing leg',(x,0,106),(x,0,49),3);box('landing foot',(x,0,47),(24,52,5),5)
    mark('RANGE HEAD',(0,-35,114),'LANDING SITE AND POD CLEARANCE')
    mark('SUSPENSION',(-45,-18,68),'LOWERED PATIENT CRADLE')
    return 27,25


def cargo_snake():
    # A gentle S-turn rather than three cloned cars on a rigid straight axis.
    poses=[((-86,14,0),-16),((0,0,0),0),((86,14,0),16)]
    with group('B'):
        joint((-43,7,28),10,(0,0,1));joint((43,7,28),10,(0,0,1))
        for x in (-43,43):
            rod('hitch drawbar',(x-12,7,28),(x+12,7,28),5)
            tube('hitch loom',[(x-11,-2,30),(x,1,37),(x+11,-2,30)],.8,'cable')
            bolts((x,7,39),6,6,size=1)
        mark('ARTICULATED HITCH',(-43,7,37),'POWER AND STEERING BETWEEN SEGMENTS')
    with group('C'):
        with at(*poses[1]):
            cyl('drive wheel',(-24,-29,14),14,9,'structure',(0,-1,0))
            flange('drive hub',(-24,-39,14),9,(0,-1,0),2)
            motor((-24,-17,14),8,15,(0,-1,0))
            rod('steering knuckle',(-24,-24,14),(-24,-24,31),2.5,'detail')
        mark('DRIVE CORNER',(-24,-39,14),'STEERED POWERED WHEEL')
    for i,(p,a) in enumerate(poses):
        with at(p,a):
            hull('cargo module',[(-38,7,7,36),(-28,27,16,36),(28,27,16,36),(38,7,7,36)])
            box('cargo enclosure',(0,0,64),(59,46,49),8)
            for x in (-24,24):
                for y in (-29,29):
                    if i==1 and x==-24 and y==-29:continue
                    side=1 if y>0 else -1
                    cyl('drive wheel',(x,y,14),14,9,'structure',(0,side,0))
                    flange('drive hub',(x,y+side*10,14),9,(0,side,0),2)
                    motor((x,y-side*12,14),8,15,(0,side,0))
                    rod('steering knuckle',(x,y-side*5,14),(x,y-side*5,31),2.5,'detail')
            for z in (49,78):tube('enclosure strap',[(-30,-21,z),(-30,21,z),(30,21,z),(30,-21,z)],.4,'detail')
    optics((-122,3,47),6,11,(-1,0,0));box('destination panel',(90,-10,87),(27,21,3),2,'accent')
    mark('CARGO POD',(1,-23,70),'ONE ADDRESS / INDEPENDENT LOAD')
    mark('ROUTE SENSOR',(-130,3,47),'SLOW SERVICE STREET NAVIGATION')
    return 29,28


def dune_skimmer():
    with group('B'):
        cyl('expanding wheel',(-56,-37,24),24,27,'structure',(0,-1,0))
        for y in (-39,-48,-57,-65):ring('wheel lamella',(-56,y,24),25,1,2,(0,1,0),'detail')
        flange('wheel drive hub',(-56,-67,24),14,(0,-1,0),3)
        for a in range(0,360,45):
            q=math.radians(a);rod('expansion spoke',(-56+8*math.cos(q),-69,24+8*math.sin(q)),(-56+20*math.cos(q),-65,24+20*math.sin(q)),1.2,'detail')
        mark('EXPANDING WHEEL',(-56,-68,24),'TELESCOPING SLEEVE, ALL FOUR')
    for x,y in ((56,-37),(-56,37),(56,37)):
        cyl('wide sand wheel',(x,y,24),24,27,'structure',(0,-1 if y<0 else 1,0));flange('wheel hub',(x,y+(-30 if y<0 else 30),24),14,(0,-1 if y<0 else 1,0),3)
        for dy in (2,11,20,28):ring('wheel lamella',(x,y+(-dy if y<0 else dy),24),25,1,2,(0,1,0),'detail')
        for a in range(0,360,45):
            q=math.radians(a);rod('expansion spoke',(x+8*math.cos(q),y+(-32 if y<0 else 32),24+8*math.sin(q)),(x+20*math.cos(q),y+(-28 if y<0 else 28),24+20*math.sin(q)),1.2,'detail')
    hull('sand rover body',[(-88,3,5,57),(-61,36,20,57),(49,36,20,57),(82,9,8,57)])
    cabin('crew canopy',(-22,0,85),70,42,32)
    with group('C'):
        for y in (-23,23):
            joint((38,y,80),6,(0,1,0));rod('shade hinge arm',(38,y,80),(44,y,132),2.5)
            rod('shade piston',(30,y,83),(42,y,121),1.5,'detail')
        rod('shade hinge',(44,-29,132),(44,29,132),3)
        for y in (-24,24):cyl('hinge pin',(44,y,132),4,5,'detail',(0,1,0))
        mark('SHADE HINGE',(43,-25,128),'FOLDS FLAT OVER THE PAYLOAD')
    panel('folding shade',(31,0,136),(120,99),nx=10,ny=6,role='shell')
    for x in (-21,83):rod('shade edge',(x,-47,136),(x,47,136),1,'detail')
    box('rear cargo',(43,0,90),(43,48,35),7)
    optics((-77,-11,65),6,10,(-1,0,0))
    mark('CREW CANOPY',(-25,-20,91),'SEALED AGAINST ABRASIVE SAND')
    mark('CARGO BAY',(50,-24,96),'SUPPLIES BELOW THE SHADE')
    return 25,22


def canal_thread():
    with group('B'):
        for x in (-7,7):box('coupler cheek',(x,0,17),(8,27,25),3)
        rod('coupler pin',(0,-20,17),(0,20,17),3,'detail');ring('pin retainer',(0,-21,17),6,2,2,(0,-1,0))
        for x in (-15,15):rod('coupler drawbar',(x,0,17),(x*2.2,0,17),4)
        tube('power bridge',[(-19,7,23),(0,15,30),(19,7,23)],1,'cable')
        mark('LOCKING COUPLER',(0,-13,20),'SEPARABLE POWER AND TOW CONNECTION')
    with group('C'):
        cyl('azimuth shaft',(132,0,-6),7,33)
        ring('propeller duct',(132,-13,-11),17,3,22,(0,1,0));rotor((132,-3,-11),12,4,(0,1,0))
        motor((132,0,29),11,21);flange('steering bearing',(132,0,27),15)
        mark('AZIMUTH DRIVE',(132,-16,-11),'ROTATES FOR DOCKING THRUST')
    for side in (-1,1):
        with at((side*76,0,0)):
            hull('cargo barge',[(-62,4,4,13),(-46,26,14,13),(46,26,14,13),(62,4,4,13)])
            box('cargo hatch',(0,0,34),(79,42,18),7)
            for x in (-32,32):
                for y in (-21,21):cyl('hatch dog',(x,y,44),2,3,'detail',n=6)
            for x in (-48,48):
                for y in (-15,15):rod('mooring cleat',(x,y-4,31),(x,y+4,31),1.5,'detail')
            for x in (-20,20):rod('hatch seam',(x,-20,44),(x,20,44),.4,'detail')
    box('navigation mast',(135,0,61),(17,19,28),4);rod('mast',(132,0,48),(132,0,85),1.5)
    optics((140,-9,68),4,8)
    mark('HATCH',(-70,-21,40),'SHALLOW NARROW CARGO HOLD')
    mark('DOCKING SENSOR',(140,-18,68),'SMALL URBAN QUAY APPROACH')
    return 27,27


def cliff_step():
    # Device on a prepared inclined rail: both clamps obey one physical load path.
    with group('B'):
        for z in (18,109):
            box('anchor clamp',(0,0,z),(47,31,22),5)
            for x in (-22,22):rod('clamp bolt',(x,-20,z),(x,18,z),2,'detail')
            for x in (-12,12):box('gripping tooth',(x,13,z),(12,8,16),2,'accent')
            motor((0,-17,z),8,20,(0,-1,0))
        mark('ANCHOR CLAMP',(0,-29,110),'LOCKED BEFORE LOAD TRANSFER')
    with group('C'):
        for x in (-17,17):
            cyl('transfer cylinder',(x,-3,38),6,51)
            rod('piston rod',(x,-3,85),(x,-3,103),3,'detail')
            joint((x,-7,36),5);joint((x,-7,104),5)
        box('load crosshead',(0,-3,63),(51,22,11),3)
        tube('cylinder equalisation',[(-17,-10,47),(0,-22,57),(17,-10,47)],1,'cable')
        mark('TRANSFER LINK',(16,-9,71),'ALTERNATING CLAMP LOAD CYCLE')
    for x in (-13,13):rod('prepared cliff rail',(x,23,-25),(x,23,171),4)
    for z in range(-10,166,22):rod('anchor rung',(-17,23,z),(17,23,z),3,'detail')
    for z in (0,150):
        for x in (-13,13):rod('rock fixing',(x,23,z),(x,43,z),3,'detail')
    box('cargo platform',(0,-53,36),(91,63,8),5)
    for x in (-36,36):rod('platform brace',(x,-74,33),(x*.3,-10,15),3)
    box('secured crate',(0,-56,65),(72,48,50),7)
    for x in (-23,23):tube('cargo strap',[(x,-79,45),(x,-79,93),(x,-33,93),(x,-33,45)],.7,'accent')
    mark('PREPARED RAIL',(13,23,142),'FIXED ANCHORS / INSPECTED ROUTE')
    mark('PAYLOAD',(0,-80,68),'LOAD REMAINS OVER THE CLAMP AXIS')
    return 26,24


def island_wing():
    with group('B'):
        for y in (-1,1):
            leaf('broad main wing',(-12,y*20,42),(23,y*129,39),86)
            rod('main spar',(-8,y*24,42),(18,y*118,42),3,'detail')
            for span in (48,76,103):rod('wing rib',(-20,y*span,40),(38,y*span,40),.6,'detail')
            box('wing box root',(-9,y*26,39),(59,17,13),4)
        mark('WING BOX',(8,-42,43),'BROAD LOW ASPECT RATIO LIFT SURFACE')
    with group('C'):
        for side in (-1,1):
            leaf('spray deflector',(-92,side*9,17),(-44,side*39,23),20,'detail')
            rod('deflector rail',(-86,side*14,19),(-46,side*35,24),1.2)
            for x in (-78,-58):box('deflector bracket',(x,side*(21 if x==-78 else 30),22),(9,6,8),2,'detail')
        mark('SPRAY DEFLECTOR',(-62,-28,23),'KEEPS WATER FROM INTAKES')
    hull('ground effect hull',[(-124,1,2,31),(-97,15,13,31),(-50,22,21,31),(64,20,18,31),(102,10,9,31),(123,1,2,31)])
    cabin('forward cabin',(-67,0,58),63,35,28)
    for side in (-1,1):
        with at((32,side*37,72),90,'Y'):
            ring('engine duct',(0,0,0),18,3,31);rotor((0,0,5),13,5);motor((0,0,17),6,19)
        rod('engine pylon',(28,side*20,46),(32,side*37,69),3)
        leaf('tailplane',(87,side*4,49),(108,side*54,56),34)
    leaf('tail fin',(74,0,41),(115,0,103),42)
    for x in (-24,35):tube('cargo door seam',[(x,-21,25),(x,-21,40),(x,-15,48)],.4,'detail')
    mark('CABIN',(-66,-17,65),'WATER PROXIMITY PILOTING')
    mark('LIFT ENGINE',(31,-37,73),'HIGH MOUNTED / SPRAY CLEARANCE')
    return 29,23


def rail_pod():
    with group('B'):
        for x in (-52,52):
            rod('wheel axle',(x,-31,14),(x,31,14),4)
            for y in (-31,31):
                cyl('rail wheel',(x,y,14),14,7,'structure',(0,1 if y>0 else -1,0));ring('wheel flange',(x,y,14),16,2,2,(0,1,0),'detail')
            motor((x,-7,21),10,28,(0,1,0))
            for y in (-23,23):rod('suspension',(x,y,15),(x+8,y,36),2,'detail')
        mark('WHEEL MODULE',(-51,-38,14),'STANDARD GAUGE RUNNING GEAR')
    with group('C'):
        box('coupling nose',(-95,0,35),(23,31,23),5)
        rod('coupler shank',(-110,0,34),(-78,0,34),5)
        ring('coupling collar',(-109,0,34),10,3,5,(-1,0,0));bolts((-115,0,34),7,6,(-1,0,0),1)
        for y in (-19,19):cyl('buffer',(-96,y,34),6,17,'detail',(-1,0,0))
        mark('COUPLING NOSE',(-110,-9,34),'AUTOMATIC MECHANICAL AND POWER LINK')
    hull('freight pod',[(-88,8,8,58),(-65,32,28,58),(62,32,28,58),(86,8,8,58)])
    for x in (-49,0,49):tube('cargo door outline',[(x,-31,42),(x,-31,68),(x,-21,82)],.5,'detail')
    for y in (-31,31):rod('rail',(-135,y,0),(130,y,0),2,'shell')
    for x in range(-119,120,23):box('rail sleeper',(x,0,-3),(10,98,5),1,'shell')
    for x in (-74,74):optics((x,-12,52),5,9,(-1 if x<0 else 1,0,0))
    box('roof service hatch',(22,0,89),(42,37,3),4,'detail')
    mark('CARGO DOOR',(0,-33,61),'SINGLE CONSIGNMENT SIDE ACCESS')
    mark('ROUTE SENSOR',(78,-12,52),'SIDING AND COUPLING APPROACH')
    return 27,23
