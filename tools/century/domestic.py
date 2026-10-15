"""Deadpan domestic inventions: the joke is in the job, not random decoration."""
from .kit import *


def sock_oracle():
    with group('B'):
        ring('soft sorting drum',(0,0,77),42,5,45,(0,1,0))
        for a in range(0,360,45):
            q=math.radians(a);rod('compliant sorting rib',(34*math.cos(q),3,77+34*math.sin(q)),(34*math.cos(q),39,77+34*math.sin(q)),2,'detail')
        for y in (1,43):ring('drum rim',(0,y,77),44,2,4,(0,1,0),'detail')
        motor((0,45,77),14,27,(0,1,0));cyl('rear hub',(0,39,77),17,8,'detail',(0,1,0))
        mark('SORTING DRUM',(26,0,99),'GENTLE MOTION / CLEAN SOCKS ONLY')
    with group('C'):
        box('pairing gate',(0,-12,31),(74,49,9),6)
        for x in (-23,23):
            box('pairing pocket',(x,-25,23),(36,44,7),5)
            rod('gate hinge',(x-15,-2,35),(x+15,-2,35),1.8,'detail')
            motor((x,5,35),6,12,(0,1,0))
        box('diverter tongue',(0,-14,40),(8,31,13),3)
        mark('PAIRING GATE',(24,-35,28),'MATCHED PAIR / SEPARATE LONELY DRAWER')
    for x in (-47,47):box('cast drum cheek',(x,16,66),(13,57,110),9)
    box('machine foot',(0,8,6),(125,101,14),12)
    optics((-27,-7,114),6,12);optics((27,-7,114),6,12)
    box('unmatched drawer',(0,-3,12),(35,63,12),4)
    rod('drawer pull',(-9,-37,16),(9,-37,16),1.4,'detail')
    # A folded fabric pair with broad soft contours, no fictitious data pattern.
    for x in (-23,23):
        hull('folded sock',[(-12,5,2,0),(-7,11,4,0),(11,10,4,0),(15,4,2,0)])
        g.parts[-1][0].location=Vector((x,-31,29))
    mark('WEAVE CAMERA',(-27,-20,115),'OWNER / WEAVE / WEAR COMPARISON')
    mark('LONELY DRAWER',(0,-36,16),'THE OTHER SOCK IS STILL ELSEWHERE')
    return 25,25


def snooze_engine():
    with group('B'):
        ring('travelling chime',(0,0,84),30,4,7,(0,1,0))
        for x in (-14,0,14):
            rod('chime bar',(x,3,67),(x,3,96),2,'detail')
            ring('bar suspension',(x,3,99),3,1,2,(0,1,0),'detail')
        rod('striker',(0,-8,85),(17,-8,91),1.5,'accent')
        motor((0,6,84),7,13,(0,1,0))
        mark('TRAVELLING CHIME',(0,-5,105),'GENTLE AT FIRST / STILL AN ALARM')
    with group('C'):
        for x in (-37,37):
            cyl('drive foot wheel',(x,-15,16),16,11,'structure',(0,1,0))
            flange('drive hub',(x,-17,16),9,(0,-1,0),2)
            motor((x,0,16),9,16,(0,1,0))
            rod('compliant axle',(x,0,17),(x*.55,0,34),3,'detail')
        mark('DRIVE FOOT',(37,-19,16),'SMALL SLOW STEPS AWAY FROM BED')
    hull('clock body',[(-54,4,4,41),(-32,23,17,41),(32,23,17,41),(54,4,4,41)])
    for x in (-18,18):rod('chime yoke',(x,7,50),(x,7,71),3)
    box('light panel',(0,-24,44),(37,3,12),3,'accent')
    for x in (-13,0,13):cyl('light cell',(x,-27,44),2,1,'detail',(0,-1,0),16)
    optics((-46,-11,40),4,7,(-1,0,0))
    box('snooze paddle',(0,0,60),(27,19,5),4)
    mark('LIGHT PANEL',(0,-27,46),'STAGE ONE / BEFORE THE WALKING')
    mark('SNOOZE PADDLE',(0,-1,64),'MARKETING CALLS THIS WELLNESS')
    return 26,24


def advice_filter():
    views(C=(35,-28))
    with group('B'):
        ring('acoustic shutter',(0,0,69),36,4,10,(0,1,0))
        for x in range(-24,25,8):
            h=math.sqrt(max(1,29**2-x*x));box('shutter blade',(x,-3,69),(5,4,h*2),1,'detail')
            cyl('blade pivot',(x,-5,69+h),1.4,3,'accent',(0,-1,0),16)
        rod('shutter link',(-24,8,69),(24,8,69),1,'detail');motor((33,3,69),6,12,(0,1,0))
        mark('ACOUSTIC SHUTTER',(16,-7,81),'HOLDS THE REST OF THE SENTENCE')
    with group('C'):
        cyl('consent button',(0,-34,16),15,7)
        ring('button bezel',(0,-34,14),18,3,5)
        for a in range(0,360,90):
            q=math.radians(a);cyl('bezel screw',(16*math.cos(q),-34+16*math.sin(q),20),1,2,'detail',n=6)
        box('button switch',(0,-34,8),(20,21,10),3,'detail')
        for x in (-6,6):rod('switch terminal',(x,-34,3),(x,-34,-3),1.2,'accent')
        for y in (-41,-27):rod('switch mounting ear',(-13,y,9),(13,y,9),1.1,'detail')
        mark('CONSENT BUTTON',(0,-35,25),'PRESS ONLY IF YOU WANT THE REST')
    with at((0,15,66),90,'X'):
        vessel('speaker back',(0,0,-23),31,42)
    for x in (-26,26):rod('speaker stand',(x,11,41),(x*.72,11,13),3)
    box('desk base',(0,-4,3),(97,96,13),12)
    for x in (-20,0,20):cyl('room microphone',(x,23,29),3,8,'detail')
    box('processing chest',(0,28,20),(60,29,26),6)
    mark('MICROPHONE',(0,23,37),'LISTENS FOR UNSOLICITED ADVICE')
    mark('PROCESSOR',(0,13,23),'THE LISTENER REMAINS IN CHARGE')
    return 25,25


def later_anchor():
    with group('B'):
        box('timed latch',(41,-22,39),(21,25,31),5)
        rod('locking bolt',(29,-22,39),(57,-22,39),3,'detail')
        motor((41,-22,57),8,18)
        for x in (34,48):cyl('latch fastener',(x,-36,44),1.3,2,'detail',(0,-1,0),6)
        ring('manual override',(42,-38,31),5,1.5,2,(0,-1,0),'accent')
        mark('TIMED LATCH',(42,-36,44),'PHYSICAL DELAY / MANUAL OVERRIDE EXISTS')
    with group('C'):
        box('device drawer',(0,-42,26),(74,85,11),7)
        for x in (-32,32):rod('drawer slide',(x,-76,19),(x,23,19),2,'detail')
        box('padded cradle',(0,-42,34),(48,64,7),6,'detail')
        box('distracting device',(0,-42,41),(32,52,7),4,'shell')
        for x in (-26,26):box('cradle bumper',(x,-42,39),(7,43,12),3)
        mark('DEVICE CRADLE',(0,-54,45),'THE PHONE IS FINE / YOU ARE ELSEWHERE')
    for x in (-47,47):box('cast anchor cheek',(x,3,36),(16,87,57),10)
    box('anchor bridge',(0,12,69),(110,72,18),12)
    box('anchor plinth',(0,0,4),(122,103,13),12)
    g.dial(0,-26,70,13)
    rod('drawer handle',(-19,-89,30),(19,-89,30),2,'detail')
    for x in (-22,22):rod('handle stay',(x,-82,30),(x,-89,30),1.5,'detail')
    mark('TIMER',(0,-30,71),'READABLE REMAINING TIME')
    mark('DRAWER HANDLE',(0,-89,31),'OVERRIDE KEY IS IN ANOTHER ROOM')
    return 25,28


def pet_diplomat():
    views(C=(28,-24))
    with group('B'):
        box('gesture camera',(0,0,83),(48,28,27),7)
        for x in (-12,12):optics((x,-16,85),7,11)
        cyl('pan axis',(0,0,65),9,12);flange('pan bearing',(0,0,65),12,depth=2)
        for x in (-20,20):cyl('camera fastener',(x,-16,76),1.2,2,'detail',(0,-1,0),6)
        mark('GESTURE CAMERA',(0,-27,86),'POSTURE AND ROUTINE / NO MIND READING')
    with group('C'):
        box('request paddle',(31,-27,13),(36,33,9),8)
        rod('paddle hinge',(16,-12,12),(47,-12,12),2,'detail')
        for x in (19,43):cyl('hinge collar',(x,-12,12),3,5,'detail',(1,0,0))
        box('paddle load cell',(31,-27,5),(17,17,9),3)
        ring('paddle indicator',(31,-27,19),7,1,1,role='accent')
        mark('REQUEST PADDLE',(31,-30,20),'OPEN THE DOOR SO I CAN RECONSIDER')
    hull('interpreter pedestal',[(-39,7,6,35),(-24,23,21,35),(24,23,21,35),(39,7,6,35)])
    rod('camera neck',(0,0,53),(0,0,66),5)
    box('status panel',(0,-24,38),(39,3,15),4,'accent')
    for x in (-12,0,12):ring('status icon cell',(x,-27,38),3.5,.7,1,(0,-1,0),'detail')
    box('desk foot',(0,0,3),(79,59,10),10)
    tube('paddle lead',[(31,-10,7),(36,0,7),(22,8,12)],.8,'cable')
    # Low bowl gives scale and domestic context, not a fake humanoid pet.
    ring('water bowl',(-55,-23,0),20,3,10);cyl('bowl base',(-55,-23,0),18,1,'detail')
    mark('STATUS PANEL',(0,-28,39),'SUGGESTION / NOT A TRANSLATION')
    mark('WATER BOWL',(-54,-24,9),'CHECK THE OBVIOUS THINGS FIRST')
    return 25,26


def meeting_buoy():
    with group('B'):
        rod('flag mast',(0,0,34),(0,0,151),3)
        box('flag carriage',(0,0,111),(15,15,25),4)
        for z in (104,119):cyl('carriage roller',(0,-9,z),3,4,'detail',(0,-1,0))
        motor((0,0,27),10,23)
        tube('flag cable',[(4,1,46),(4,1,149),(-4,1,149),(-4,1,46)],.45,'cable')
        g.mesh('meeting flag',[(5,0,119),(51,0,119),(41,0,143),(5,0,143)],[(0,1,2,3)],'accent')
        mark('FLAG ACTUATOR',(0,-7,112),'RAISES AN OBSERVATION / NOT A BAN')
    with group('C'):
        ring('microphone crown',(0,0,25),27,5,9)
        for a in range(0,360,45):
            q=math.radians(a);cyl('room microphone',(24*math.cos(q),24*math.sin(q),34),2.5,4,'detail')
            ring('microphone mesh',(24*math.cos(q),24*math.sin(q),38),3,.5,1,role='accent')
        bolts((0,0,36),19,6,size=1)
        mark('ROOM MICROPHONE',(20,-14,36),'FORMAT DISCUSSION DETECTOR')
    with at((0,0,0)):g.base(43,36)
    box('status window',(0,-36,18),(37,3,9),3,'detail')
    for x in (-10,0,10):cyl('status light',(x,-39,18),1.8,1,'accent',(0,-1,0),16)
    box('reset paddle',(33,1,31),(17,24,5),3)
    mark('STATUS WINDOW',(0,-40,19),'THE MEETING IS ABOUT THE MEETING')
    mark('RESET PADDLE',(34,0,35),'NOT CONNECTED TO A MUTE BUTTON')
    return 25,22


def queue_garden():
    views(C=(24,32))
    with group('B'):
        rod('leaf register stem',(0,0,34),(0,0,145),4)
        for j in range(6):
            a=j*137;z=60+j*13
            with at((0,0,z),a):
                joint((6,0,0),4,(0,1,0));leaf('completed position leaf',(7,0,0),(45,0,17),22,'accent')
                rod('leaf opening link',(5,2,-5),(23,2,5),1,'detail')
        mark('LEAF REGISTER',(27,-16,110),'ONE LEAF FOR EACH COMPLETED POSITION')
    with group('C'):
        box('ticket reader',(0,-36,32),(47,34,33),7)
        box('ticket slot',(0,-55,35),(32,2,5),1,'accent')
        for y in (-42,-50):
            cyl('reader roller',(-17,y,32),3,34,'detail',(1,0,0))
            for x in (-19,19):box('roller bearing',(x,y,32),(4,7,8),1,'detail')
        box('reader board',(0,-35,23),(33,22,2),1,'detail')
        for x in (-9,0,9):box('reader component',(x,-35,25),(5,8,3),.5,'detail')
        optics((0,-43,43),4,7,(0,0,-1))
        box('ticket paper',(0,-65,34),(27,29,.7),.3,'shell')
        mark('TICKET READER',(0,-57,36),'ACTUAL PROGRESS / NO FIVE MINUTE PROMISE')
    uncover('C','ticket reader')
    vessel('register pot',(0,0,0),36,39)
    for z in (5,31):ring('pot trim',(0,0,z),38,1,2,role='detail')
    motor((0,0,42),12,15)
    for a in (0,120,240):
        q=math.radians(a);box('pot foot',(28*math.cos(q),28*math.sin(q),-4),(17,17,7),4)
    box('service hatch',(0,35,20),(32,7,24),4)
    mark('DRIVE ROOT',(0,-11,49),'PERSISTENT MECHANICAL POSITION MEMORY')
    mark('SERVICE HATCH',(0,39,23),'THE QUEUE SURVIVES A POWER CUT')
    return 25,24


def compliment_mill():
    with group('B'):
        box('observation head',(0,0,113),(53,33,31),8)
        for x in (-14,14):optics((x,-19,115),8,16)
        rod('head swivel',(0,0,86),(0,0,100),5)
        joint((0,0,88),9,(0,1,0))
        ring('inspection lamp',(0,-19,108),5,1,2,(0,-1,0),'accent')
        mark('OBSERVATION HEAD',(0,-35,116),'EXAMINES WHAT WAS ACTUALLY MADE')
    with group('C'):
        for y in (-27,-41):
            cyl('paper roller',(-23,y,40),6,46,'detail',(1,0,0))
            for x in (-26,26):box('roller bearing',(x,y,40),(5,15,15),2,'detail')
        for x in range(-21,22,3):box('thermal print element',(x,-34,47),(1.5,3,1.5),.3,'accent')
        box('print carriage',(0,-26,51),(56,19,15),4)
        rod('print rail',(-29,-25,51),(29,-25,51),1.5,'detail')
        motor((31,-25,48),6,14,(1,0,0))
        g.mesh('printed paper', [(-23,-34,43),(23,-34,43),(23,-72,32),(-23,-72,32)],[(0,1,2,3)],'shell')
        for y in (-48,-53,-58):rod('printed line',(-16,y,43+(y+34)*11/38),(16,y,43+(y+34)*11/38),.2,'detail')
        mark('PRINT MECHANISM',(0,-30,54),'ONE SPECIFIC DEFENSIBLE COMPLIMENT')
    with at((0,0,0)):g.casting('mill body',[(0,43,34),(8,49,39),(66,43,34),(78,27,25)])
    for z in (8,67):g.trim('cast body seam',z,45 if z==8 else 41,36 if z==8 else 32)
    box('work inspection tray',(0,-102,10),(111,72,7),8)
    # A small made object to inspect, rather than a decorative waveform.
    vessel('sample handmade cup',(9,-99,14),13,24);ring('cup handle',(24,-101,27),9,2,4,(0,1,0),'detail')
    box('evidence button',(35,-23,74),(16,17,5),3,'accent')
    mark('WORKPIECE',(10,-107,30),'THE OBJECT BEING PRAISED')
    mark('EVIDENCE BUTTON',(36,-24,78),'AMAZING IS NOT AN OBSERVATION')
    return 25,25


def crumb_pilot():
    with group('B'):
        for side in (-1,1):
            tube('edge whisker',[(-36,side*15,17),(-53,side*29,12),(-63,side*40,3)],.65,'accent')
            joint((-36,side*15,17),4,(0,0,1))
            box('whisker sensor',(-31,side*19,19),(12,9,11),3)
        mark('EDGE WHISKER',(-54,-30,11),'STOPS BEFORE THE TABLE EDGE')
    with group('C'):
        box('vacuum throat',(-24,0,4),(29,39,9),5)
        for y in range(-14,15,7):rod('throat guard',(-38,y,4),(-11,y,4),.7,'detail')
        cyl('suction impeller',(-8,0,14),12,10)
        rotor((-8,0,25),10,5);ring('fan collar',(-8,0,24),13,2,3)
        mark('VACUUM THROAT',(-25,-13,8),'CRUMBS TO A REMOVABLE HOPPER')
    hull('crumb rover',[(-44,3,3,22),(-29,23,16,22),(25,25,17,22),(44,4,4,22)])
    for x in (-18,24):
        for y in (-24,24):cyl('desk wheel',(x,y,9),9,6,'structure',(0,1 if y>0 else -1,0));ring('desk wheel hub',(x,y+(7 if y>0 else -7),9),4,1,1,(0,1,0),'detail')
    box('hopper lid',(17,0,40),(33,31,5),5)
    rod('hopper pull',(10,0,46),(25,0,46),1.5,'detail')
    optics((-36,-8,26),4,8,(-1,0,0));optics((-36,8,26),4,8,(-1,0,0))
    for x,y,r in ((-77,14,3),(-72,-6,2),(-65,8,2),(-91,2,4)):
        cyl('biscuit crumb',(x,y,0),r,2,'shell',n=6)
    mark('HOPPER',(17,0,45),'NO CRUMBS STORED IN THE SOFTWARE')
    mark('VISION',(-43,-9,27),'THE BISCUIT IS NOT WORTH THE FALL')
    return 25,27


def plant_alibi():
    from .biology import sprig
    with group('B'):
        rod('root probe',(-14,0,15),(-14,0,71),3)
        for z in (19,33,47):ring('root electrode',(-14,0,z),4,.6,4,role='accent')
        box('probe head',(-14,0,75),(16,13,15),4)
        for x in (-19,-9):cyl('probe screw',(x,-7,76),.8,1,'detail',(0,-1,0),6)
        mark('ROOT PROBE',(-15,-3,54),'MEASURED MOISTURE / NOT AN EXCUSE')
    with group('C'):
        cyl('water meter',(46,0,30),13,22)
        flange('meter lid',(46,0,53),16,depth=3)
        for side in (-1,1):flange('water port',(46+side*15,0,38),6,(side,0,0),3)
        ring('meter readout',(46,-14,43),6,1,2,(0,-1,0),'accent')
        pump((46,0,13),.3)
        mark('WATER METER',(46,-14,44),'RECORDS EVERY ACTUAL WATERING')
    vessel('plant pot',(0,0,0),33,49)
    ring('pot lip',(0,0,49),36,3,5)
    sprig((0,0,52),87,34);sprig((13,8,52),58,26)
    tube('watering tube',[(31,0,39),(27,3,61),(17,5,62),(10,4,55)],1.2,'cable')
    rod('light sensor stalk',(22,9,45),(32,9,111),1.7)
    box('light sensor',(32,9,113),(17,15,5),3,'accent')
    box('history recorder',(0,-31,31),(28,9,21),4)
    for x in (-8,0,8):cyl('history indicator',(x,-37,33),1.5,1,'detail',(0,-1,0),16)
    mark('LIGHT SENSOR',(31,8,117),'ACTUAL EXPOSURE / WINDOW INCLUDED')
    mark('HISTORY RECORDER',(0,-37,35),'CANNOT BE EDITED FROM THE WATERING CAN')
    return 25,25
