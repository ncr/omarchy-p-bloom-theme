"""Human-scale assistance equipment, with one shared technical mannequin."""
from .kit import *
from .humans import human


def load_fern():
    j,p=human()
    with group('B'):
        for side in (-1,1):
            hip=j[str(side)+'thigh']['a'];x=hip.x+side*6
            joint((x,hip.y,hip.z),5,(1,0,0));flange('hip retainer',(x+side*4,hip.y,hip.z),6,(side,0,0),2)
            rod('load strut',(x,hip.y,hip.z),(x,12,142),2.3)
            box('pelvis pad',(x,4,hip.z+4),(8,16,18),3,'detail')
        mark('HIP COUPLING',(18,0,91),'LOAD PATH OUTSIDE THE HIP')
    with group('C'):
        for side in (-1,1):
            box('spring cartridge',(side*13,17,123),(12,14,47),4)
            tube('load spring',[(side*13+4*math.cos(T*i/24),17+4*math.sin(T*i/24),104+38*i/192) for i in range(193)],.45,'detail')
            rod('spring rod',(side*13,17,100),(side*13,17,87),2,'accent')
            for z in (106,140):cyl('cartridge bolt',(side*13,9,z),1.2,2,'detail',(0,-1,0),6)
        mark('SPRING PACK',(13,20,127),'COMPLIANT SHOULDER LOAD TRANSFER')
    uncover('C','spring cartridge')
    for side in (-1,1):
        hip=j[str(side)+'thigh']['a'];kn=j[str(side)+'calf']['a'];an=j[str(side)+'calf']['b']
        off=Vector((side*8,5,0))
        rod('thigh load frame',hip+off,kn+off,2);joint(kn+off,4,(1,0,0));rod('calf load frame',kn+off,an+off,2)
        box('ground shoe',(an.x,an.y-4,1),(14,27,3),2,'detail')
        tube('shoulder strap',[(side*14,14,146),(side*18,6,157),(side*14,-12,145)],1.3,'detail')
    box('carried load',(0,33,132),(41,30,58),7)
    for z in (111,153):tube('load strap',[(-21,20,z),(-21,49,z),(21,49,z),(21,20,z)],.6,'accent')
    mark('CARRIED LOAD',(0,49,143),'WEIGHT THROUGH THE FRAME')
    mark('HUMAN WORKER',p((0,-26,307)),'STILL DOES THE ACTUAL WORK')
    return 39,15


def hand_stead():
    j,p=human(scale=.55,only=['1forearm','1wrist','1hand'])
    wr=j['1forearm']['b'];el=j['1forearm']['a'];axis=(wr-el).normalized()
    with group('B'):
        q=wr+Vector((0,-16,-8));ring('tool gimbal',q,15,3,8,(0,1,0))
        for x in (-12,12):cyl('gimbal pivot',q+Vector((x,-3,0)),3,6,'detail',(1,0,0))
        rod('tool cradle',q+Vector((-9,0,0)),q+Vector((9,0,0)),2,'detail')
        optics(q+Vector((0,-4,0)),4,18,(0,-1,0))
        rod('precision tool',q+Vector((0,-8,0)),q+Vector((0,-45,0)),2,'accent')
        mark('TOOL GIMBAL',q+Vector((0,-7,13)),'TWO AXIS DISTURBANCE COMPENSATION')
    with group('C'):
        q=wr.lerp(el,.47)
        ring('compliant forearm cuff',q,12,2,19,axis)
        for z in (-1,1):box('cuff pad',q+Vector((z*10,0,7)),(5,17,21),2,'detail')
        box('cuff latch',q+Vector((0,-15,4)),(13,7,18),3)
        for x in (-4,4):cyl('latch fastener',q+Vector((x,-19,4)),1.3,2,'detail',(0,-1,0),6)
        mark('COMPLIANT CUFF',q+Vector((0,-16,6)),'BROAD CONTACT / NO RIGID GRIP')
    q=wr.lerp(el,.5);rod('tool support',q+Vector((0,-15,0)),wr+Vector((0,-20,-8)),2.5)
    tube('actuator lead',[q+Vector((8,-12,0)),wr+Vector((10,-17,-2)),wr+Vector((0,-17,-8))],.65,'cable')
    box('control pod',q+Vector((0,12,6)),(17,13,24),4)
    mark('HUMAN HAND',wr+Vector((6,-2,-13)),'THE SKILL BELONGS TO THE PERSON')
    mark('CONTROL POD',q+Vector((0,18,6)),'LOCAL MOTION ESTIMATE')
    return 23,25


def breath_shell():
    j,p=human()
    with group('B'):
        for x in (-11,11):
            vessel('scrubber cartridge',(x,23,115),8,35)
            for z in (120,139):ring('cartridge lock',(x,23,z),9,1,3,role='detail')
            tube('scrubber return',[(x,23,150),(x,16,157),(x,10,159)],1.2,'cable')
        box('scrubber manifold',(0,23,111),(33,23,10),3)
        mark('SCRUBBER',(12,26,136),'REPLACEABLE MONITORED SORBENT')
    with group('C'):
        q=p((0,-29,300));box('breathing valve',q,(17,12,16),5)
        for x in (-8,8):flange('breathing hose port',q+Vector((x,0,0)),5,(1 if x>0 else -1,0,0),3)
        ring('valve diaphragm',q+Vector((0,-7,0)),6,1,2,(0,-1,0),'accent')
        for x in (-5,5):cyl('valve fastener',q+Vector((x,-7,5)),.8,1,'detail',(0,-1,0),6)
        mark('BREATHING VALVE',q+Vector((0,-9,0)),'INHALE AND EXHALE PATHS SEPARATED')
    for side in (-1,1):
        q=p((side*10,-29,300));tube('breathing hose',[q,(side*17,-11,166),(side*22,4,157),(side*11,23,150)],2,'cable')
        tube('pack harness',[(side*13,20,150),(side*19,3,156),(side*13,-12,136),(side*12,-10,110)],1.1,'detail')
    box('oxygen sensor pack',(0,33,139),(27,10,23),4)
    vessel('reserve gas',(0,29,87),8,24)
    mark('RESERVE GAS',(0,29,99),'ILLUSTRATIVE EMERGENCY RESERVE')
    mark('HUMAN INSIDE',p((0,-28,337)),'THE PERSON IS NOT A ROBOT')
    return 44,14


def stride_return():
    j,p=human()
    with group('B'):
        for side in (-1,1):
            an=j[str(side)+'calf']['b'];q=an+Vector((side*6,1,0))
            joint(q,4,(1,0,0));ring('ankle cam',q+Vector((side*4,0,0)),6,1.5,2,(side,0,0),'accent')
            rod('cam follower',q+Vector((0,0,5)),q+Vector((0,6,16)),1.3,'detail')
            box('sole plate',(an.x,an.y-4,1),(13,27,3),2)
        mark('ANKLE CAM',j['1calf']['b']+Vector((10,0,1)),'RETURN TIMING NEAR PUSH OFF')
    with group('C'):
        for side in (-1,1):
            an=j[str(side)+'calf']['b'];q=an+Vector((side*5,9,7))
            box('elastic cartridge',q+Vector((0,0,11)),(9,11,31),3)
            tube('ankle spring',[q+Vector((2.7*math.cos(T*i/24),2.7*math.sin(T*i/24),24*i/144)) for i in range(145)],.3,'detail')
            rod('spring return',q+Vector((0,0,-7)),q+Vector((0,0,1)),1.5,'accent')
            tube('calf strap',[q+Vector((-9,-6,23)),q+Vector((-8,-15,23)),q+Vector((7,-15,23)),q+Vector((9,-6,23))],.7,'detail')
        mark('ELASTIC CARTRIDGE',j['1calf']['b']+Vector((5,14,21)),'TUNED STORAGE / STAIRS BYPASS')
    uncover('C','elastic cartridge')
    for side in (-1,1):
        an=j[str(side)+'calf']['b'];kn=j[str(side)+'calf']['a']
        rod('calf frame',an+Vector((side*7,7,0)),kn+Vector((side*6,5,-4)),1.5)
        box('calf cuff',kn+Vector((0,6,-8)),(14,10,13),3,'detail')
    mark('CALF CUFF',j['1calf']['a']+Vector((0,8,-8)),'SPREADS CONTACT ABOVE THE ANKLE')
    mark('HUMAN WALKER',p((0,-26,313)),'ENERGY SAVED / WALKING STILL REQUIRED')
    return 29,15


def cold_mantle():
    j,p=human()
    with group('B'):
        for side in (-1,1):
            box('thermal vest panel',(side*9,-11,136),(15,4,32),4,'detail')
            for z in range(123,151,5):tube('microchannel',[(side*3,-14,z),(side*14,-14,z),(side*14,-14,z+2),(side*3,-14,z+2)],.25,'accent')
            tube('panel manifold',[(side*16,-13,120),(side*16,-13,152)],.7,'detail')
        mark('MICROCHANNEL PANEL',(13,-15,139),'LOCAL HEAT EXCHANGE AT THE VEST')
    with group('C'):
        vessel('thermal buffer',(0,26,111),13,37)
        flange('buffer lid',(0,26,148),15,depth=3)
        pump((0,26,107),.25)
        for x in (-7,7):tube('buffer hose',[(x,25,147),(x,14,155),(x,-2,151)],.8,'cable')
        mark('THERMAL BUFFER',(0,38,130),'SWAPPABLE PHASE CHANGE RESERVE')
    for side in (-1,1):
        tube('vest shoulder',[(side*12,21,147),(side*18,1,156),(side*12,-13,151)],1,'detail')
        tube('waist belt',[(side*2,-12,112),(side*14,-11,112),(side*16,9,112),(side*6,20,112)],.9,'detail')
    box('pump controller',(18,0,119),(8,13,16),3);optics((21,-7,122),2,3)
    mark('CONTROLLER',(21,-7,122),'LOCAL FLOW AND TEMPERATURE LIMITS')
    mark('HUMAN WORKER',p((0,-26,313)),'COOLS ONE PERSON / NOT THE WHOLE SITE')
    return 42,15


def reach_friend():
    # Forearms rotate rigidly about matched elbow pivots; head and feet stay neutral.
    j,p=human(arm_angle=-100)
    with group('B'):
        sh=j['1upper_arm']['a'];el=j['1upper_arm']['b'];wr=j['1forearm']['b']
        for a,b in ((sh,el),(el,wr)):
            off=Vector((7,5,0));rod('shoulder assist link',a+off,b+off,2.5)
        for q in (sh,el):joint(q+Vector((7,5,0)),4,(1,0,0))
        box('forearm support cuff',wr.lerp(el,.7)+Vector((1,5,0)),(12,9,15),3)
        mark('SHOULDER LINK',sh+Vector((8,5,0)),'TOOL WEIGHT INTO THE BACK FRAME')
    with group('C'):
        q=Vector((13,21,136));box('balance spring pack',q,(14,15,37),4)
        tube('balance spring',[q+Vector((4*math.cos(T*i/24),4*math.sin(T*i/24),-13+26*i/168)) for i in range(169)],.4,'detail')
        rod('spring takeoff',q+Vector((0,0,18)),(22,9,155),1.5,'accent')
        flange('spring adjustment',q+Vector((0,0,-21)),7,depth=3)
        mark('BALANCE SPRING',q+Vector((0,8,0)),'ADJUSTED TO TOOL MASS')
    uncover('C','balance spring pack')
    for side in (-1,1):tube('back frame',[(side*10,14,96),(side*12,16,138),(side*20,6,156)],1.8)
    wr=j['1forearm']['b'];q=wr+Vector((2,-7,0));box('held service tool',q,(9,23,12),3)
    rod('tool bit',q+Vector((0,-10,0)),q+Vector((0,-31,0)),1.5,'detail')
    mark('TOOL',q+Vector((0,-16,0)),'HUMAN STEERS THE WORK')
    mark('HUMAN TECHNICIAN',p((0,-26,313)),'STILL RESPONSIBLE FOR THE REPAIR')
    return 39,17


def balance_thread():
    j,p=human()
    with group('B'):
        for x in (-10,0,10):
            box('tactile tile',(x,-9,101),(8,7,13),2)
            for z in (98,104):cyl('haptic pad',(x,-13,z),2,.8,'accent',(0,-1,0),16)
            for dx in (-3,3):cyl('tile screw',(x+dx,-13,106),.6,.8,'detail',(0,-1,0),6)
        tube('front belt',[(-16,-8,102),(0,-11,102),(16,-8,102)],1,'detail')
        mark('TACTILE TILE',(0,-14,103),'DIRECTIONAL PRESSURE / EARS STAY FREE')
    with group('C'):
        q=Vector((0,-13,145));box('depth sensor',q,(20,10,12),3)
        for x in (-6,6):optics(q+Vector((x,-6,0)),3,4)
        box('sensor clip',q+Vector((0,5,0)),(13,5,16),2,'detail')
        for x in (-7,7):cyl('sensor fastener',q+Vector((x,-6,4)),.6,1,'detail',(0,-1,0),6)
        mark('DEPTH SENSOR',q+Vector((0,-11,0)),'NEARBY OBSTACLES AND ROUTE CUES')
    for side in (-1,1):
        tube('waist belt',[(side*15,-9,102),(side*17,5,102),(side*11,12,102),(0,13,102)],1,'detail')
        box('side tactile tile',(side*17,2,102),(6,12,13),2)
    box('belt processor',(0,17,103),(22,9,17),3)
    tube('sensor lead',[(0,-9,142),(13,-10,130),(13,-9,109)],.45,'cable')
    mark('BELT PROCESSOR',(0,22,104),'LOCAL MAP / NO AUDIO PROMPTS')
    mark('HUMAN USER',p((0,-26,313)),'THE PERSON CHOOSES WHERE TO GO')
    return 31,14


def dive_spine():
    views(C=(30,14))
    j,p=human()
    with group('B'):
        box('buoyancy valve',(14,24,149),(16,15,17),4)
        for side in (-1,1):flange('valve coupling',(14+side*9,24,149),4,(side,0,0),2)
        cyl('valve button',(14,24,159),4,3,'accent')
        tube('inflation tube',[(14,24,152),(21,10,159),(20,-9,153)],1.3,'cable')
        mark('BUOYANCY VALVE',(18,20,151),'ACCESSIBLE INFLATE AND DUMP')
    with group('C'):
        for side in (-1,1):
            box('quick release buckle',(side*12,-9,123),(9,6,13),2)
            box('release tab',(side*12,-14,123),(5,4,7),1,'accent')
            rod('buckle hinge',(side*12-4,-10,125),(side*12+4,-10,125),.7,'detail')
            for z in (118,128):cyl('buckle fastener',(side*12,-13,z),.7,1,'detail',(0,-1,0),6)
        mark('QUICK RELEASE',(12,-15,123),'CLEAR EMERGENCY ACCESS')
    for side in (-1,1):
        vessel('breathing cylinder',(side*11,26,102),9,47)
        for z in (112,140):ring('cylinder strap',(side*11,26,z),10,1,3,role='detail')
        tube('shoulder harness',[(side*11,24,146),(side*18,2,156),(side*12,-10,124)],1.5,'detail')
    q=p((0,-30,300));box('mouthpiece',q,(13,11,10),3)
    tube('breathing hose',[q,(18,-6,164),(17,21,150)],1.5,'cable')
    for side in (-1,1):
        an=j[str(side)+'calf']['b'];leaf('diver fin',an+Vector((0,-7,-7)),an+Vector((0,-40,-7)),19,'detail')
    mark('CYLINDER',(10,35,129),'CLOSE TO THE BODY CENTRELINE')
    mark('HUMAN DIVER',p((0,-28,332)),'ILLUSTRATIVE LIFE SUPPORT CONCEPT')
    return 45,14


def grip_print():
    views(B=(156,25),C=(18,20))
    j,p=human(scale=.8,only=['1forearm','1wrist','1hand'])
    wr=j['1forearm']['b'];el=j['1forearm']['a'];q=wr.lerp(el,.45)
    with group('B'):
        box('tendon differential',q+Vector((0,17,0)),(21,15,31),4)
        for z in (-8,8):
            cyl('differential pulley',q+Vector((0,26,z)),5,3,'detail',(0,1,0));ring('pulley rim',q+Vector((0,30,z)),6,1,2,(0,1,0),'accent')
        motor(q+Vector((0,16,18)),6,14)
        for side in (-1,1):tube('tendon path',[q+Vector((side*6,26,-10)),wr+Vector((side*6,14,-6)),wr+Vector((side*8,6,-22))],.45,'cable')
        mark('TENDON DIFFERENTIAL',q+Vector((0,28,0)),'SERVICEABLE COMPACT DRIVE')
    with group('C'):
        q2=wr+Vector((0,-6,-19));box('palm sensor pad',q2,(14,3,17),3,'accent')
        for x in (-5,0,5):
            for z in (-5,0,5):cyl('pressure cell',q2+Vector((x,-2,z)),.7,.4,'detail',(0,-1,0),12)
        tube('sensor edge',[q2+Vector((-7,-2,-8)),q2+Vector((-7,-2,8)),q2+Vector((7,-2,8)),q2+Vector((7,-2,-8))],.25,'detail')
        mark('PALM SENSOR',q2+Vector((0,-4,0)),'CONTACT PRESSURE / OBJECT SLIP')
    axis=(wr-el).normalized();ring('fitted forearm socket',wr.lerp(el,.75),17,2,21,axis)
    for side in (-1,1):rod('socket rail',wr.lerp(el,.8)+Vector((side*16,0,0)),wr+Vector((side*10,0,0)),1.5,'detail')
    mark('CUSTOM SOCKET',wr.lerp(el,.8)+Vector((17,0,0)),'INDIVIDUALLY FITTED INTERFACE')
    mark('HUMAN HAND STAND-IN',wr+Vector((0,4,-23)),'COMPACT SCHEMATIC / NOT A FINGER MODEL')
    return 27,26


def sleep_cocoon():
    j,p=human('seated',scale=.28,p=(0,0,0))
    hip=j['1thigh']['a'];kn=j['1calf']['a'];an=j['1calf']['b']
    with group('B'):
        q=p((0,7,319));ring('head cradle',q,12,3,6,(0,-1,0),start=20,end=340)
        for side in (-1,1):box('lateral head pad',q+Vector((side*10,-2,0)),(5,9,13),2,'detail')
        rod('headrest post',q+Vector((0,5,-8)),q+Vector((0,5,-34)),2)
        box('headrest adjuster',q+Vector((0,5,-28)),(13,9,13),3)
        mark('HEAD CRADLE',q+Vector((11,-3,0)),'SUPPORTS WITHOUT FORWARD NECK FLEXION')
    with group('C'):
        for side in (-1,1):
            x=side*17
            rod('seat parallelogram',(x,8,9),(x,-21,25),2.5)
            rod('seat parallelogram',(x,11,19),(x,-18,35),2.5)
            for y,z in ((8,9),(-21,25),(11,19),(-18,35)):joint((x,y,z),3,(1,0,0))
            rod('recline damper',(x,9,13),(x,-9,29),1.3,'detail')
            rod('lower linkage bracket',(x,8,0),(x,8,9),2.5)
            rod('fixed linkage knuckle',(x,8,9),(x,11,19),2.5)
            rod('seat linkage knuckle',(x,-21,25),(x,-18,35),2.5)
            rod('seat mounting post',(x,-18,35),(x,-18,hip.z-5),2.5)
        mark('SEAT LINKAGE',(17,-8,26),'SUPPORTED PELVIS THROUGH RECLINE')
    # Seated foot minimum is zero from measured template; pelvis contact is explicit.
    seat_z=min(v.z*.28 for n,vs,fs in __import__('century.humans',fromlist=['CACHE']).CACHE['seated'][0] if n=='pelvis' for v in vs)
    # Human() shifts the foot minimum; pelvis centre provides stable contact in this pose.
    seat_height=hip.z-2
    box('seat cushion',(0,-5,seat_height-2.5),(43,42,5),6,'detail')
    box('chair back',(0,13,seat_height+27),(44,7,55),5,'detail')
    box('foot platform',(0,an.y-5,-3),(47,36,6),5)
    for side in (-1,1):rod('footrest stay',(side*20,2,8),(side*20,an.y,-3),2)
    box('chair ground rail',(0,0,-5),(61,64,7),6)
    for side in (-1,1):
        wrist=j[str(side)+'forearm']['b'];rod('armrest',(side*23,12,wrist.z-4),(side*23,-55,wrist.z-4),2,'detail')
    mark('FOOT PLATFORM',(20,an.y-6,0),'BOTH FEET SUPPORTED')
    mark('RESTING WORKER',p((0,-26,313)),'SITS UPRIGHT; THE SEAT DOES THE HOLDING')
    return 36,17
