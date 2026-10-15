"""Spatial replacements for Presence Rig and Volumetric Stage.
Reuses the Century fabrication/export vocabulary and the shared mannequin.
"""
import sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from century.kit import *
from century import kit
from century.humans import human


def presence():
    joints,point=human('presence',scale=.32,p=(0,-10,20))
    views(B=(26,36),C=(26,31))
    # Shared mannequin's sole minima are exactly on the powered floor at z=20.
    ring('floor perimeter',(0,0,8),141,7,10)
    cyl('roller deck',(0,0,9),133,7,'shell',n=96)
    for row in range(-7,8):
        for col in range(-7,8):
            x=col*16;y=row*16
            if x*x+y*y>124**2:continue
            # Representative roller bays; total device count stays in the legend.
            cyl('floor roller',(x-4,y,17),3,8,'detail',(1,0,0),12)
    for angle in (0,120,240):
        with at((0,0,0),angle):
            box('floor support foot',(117,0,0),(41,37,12),6)
            for x in (112,124):cyl('foot leveller',(x,0,-7),4,8,'detail')
    with group('B'):
        # A real replaceable bay in the front-left service opening.
        with at((-75,-75,12),-20):
            box('roller cartridge pan',(0,0,-6),(32,32,5),3)
            for x in (-10,0,10):
                cyl('cartridge roller',(x-3,-8,5),3,6,'structure',(1,0,0),20)
                cyl('cartridge roller',(x-3,2,5),3,6,'structure',(1,0,0),20)
                cyl('cartridge roller',(x-3,12,5),3,6,'structure',(1,0,0),20)
            for y in (-9,2,12):rod('roller shaft',(-14,y,5),(14,y,5),.6,'detail')
            for x in (-12,12):box('roller bearing rail',(x,2,2),(3,29,7),1,'detail')
            motor((0,12,-1),4,10,(0,1,0))
            box('bay connector',(0,17,-5),(13,6,5),1,'accent')
        mark('ROLLER CASSETTE',(-75,-85,17),'9 ROLLERS, ONE MOTOR')
    # Rear crescent backbone supports an actual bearing and captive tether reel.
    for side in (-1,1):
        x=side*87
        organic_branch('swept load column',[(x,58,14),(x*1.04,64,72),(x*.82,66,156),(x*.52,47,217),(x*.25,22,233)],4,'structure')
        organic_branch('rear column brace',[(x,84,14),(x*.95,85,82),(x*.65,71,171),(x*.25,25,235)],2,'structure')
        for z,f in ((62,1.02),(109,.95),(156,.82)):
            rod('column diagonal',(x*f,64,z),(x*(f-.12),77,z+29),1.3,'detail')
        box('column shoe',(x,67,16),(29,35,20),5)
        for y in (54,79):cyl('shoe fastener',(x,y,27),2,3,'detail',n=6)
    rod('crown bearing bridge',(-24,22,233),(24,22,233),4)
    with group('C'):
        ring('tether azimuth bearing',(0,17,231),19,5,6)
        cyl('tether reel',(-10,15,223),10,20,'structure',(1,0,0))
        for x in (-12,12):flange('reel cheek',(x,15,223),12,(1,0,0),2)
        motor((15,15,223),6,14,(1,0,0))
        box('release clevis',(0,13,207),(15,14,12),2)
        rod('release pin',(-11,13,206),(11,13,206),1.3,'accent')
        ring('manual pull eye',(-16,13,206),5,1.2,2,(1,0,0),'accent')
    # Tether ends on the shoulder harness, never into empty air.
    shoulder=point((0,17,245))
    tube('safety tether',[(0,13,207),tuple(shoulder+Vector((0,6,15))),tuple(shoulder)],.8,'cable')
    for side in (-1,1):
        tube('shoulder restraint',[point((side*47,13,225)),point((side*46,1,253)),point((side*37,-29,218))],1.1,'detail')
        elbow=joints[str(side)+'forearm']['a'];wrist=joints[str(side)+'forearm']['b']
        d=(wrist-elbow).normalized();q=elbow.lerp(wrist,.24)
        ring('forearm force cuff',q,5.8,1.2,6,d)
        tube('suit service line',[tuple(q+Vector((0,5,0))),tuple(elbow+Vector((0,5,5))),tuple(point((side*45,15,222)))],.35,'cable')
    # A shallow headset follows the shared head coordinates, never a black mask.
    box('headset optics',point((0,-28,302)),(17,4,8),2,'detail')
    for side in (-1,1):
        q=point((side*25,2,299))
        cyl('inner ear contact',q,2.8,2,'accent',(side,0,0))
        tube('headset temple',[point((side*20,-24,302)),point((side*26,-5,303)),point((side*25,4,301))],.4,'detail')
    box('suit interface cabinet',(114,35,58),(26,40,72),6)
    for z in range(30,89,7):rod('cabinet cooling rib',(128,21,z),(128,47,z),.6,'detail')
    tube('cabinet loom',[(107,28,81),(78,48,127),tuple(shoulder)],1,'cable')
    optics((-52,64,141),7,16,(.35,-1,-.15))
    mark('HUMAN PLAYER',point((0,-30,200)),'SUIT RESISTS OR ASSISTS EVERY JOINT')
    mark('CAPTIVE TETHER',(0,15,224),'SAFETY LINE TO THE SHOULDERS')
    mark('SUIT INTERFACE',(116,14,61),'TACTILE AND MUSCLE BAND CONTROL')
    mark('SIGHT AND SOUND',point((0,-28,311)),'HEADSET / INNER-EAR INTERFACE')
    mark('POWERED FLOOR',(83,-61,20),'DRIVEN ROLLER FIELD')
    return 22,18


def stage():
    views(B=(0,90),C=(30,25))
    # Stage depth, open trusses, physical light paths and service access.
    box('performance deck',(0,0,5),(263,145,10),15)
    for y in (-68,68):rod('deck edge',(-116,y,12),(116,y,12),1.1,'detail')
    for x in (-118,118):
        for y in (-39,47):
            box('tower shoe',(x,y,15),(31,34,15),6)
            truss((x,y,23),(x*.9,y+10,189),12,9)
        rod('upper tower tie',(x*.9,-29,189),(x*.9,57,189),3)
        for z in (50,94,138,182):rod('tower cross tie',(x,-29,z),(x,57,z),1.8,'detail')
    truss((-108,36,202),(108,36,202),17,16)
    truss((-108,-18,202),(108,-18,202),10,16)
    for x in range(-105,106,30):rod('bridge depth tie',(x,-18,202),(x,36,202),1.5)
    def emitter(p,axis):
        with at(p):
            box('emitter carrier',(0,3,0),(17,14,12),3)
            joint((0,-5,0),7,(1,0,0))
            optics((0,-7,0),6,15,axis)
            for x in (-10,10):rod('gimbal cheek',(x,2,0),(x,-7,0),1.2,'detail')
            box('beam controller',(0,8,4),(13,7,8),2,'detail')
    with group('C'):
        emitter((-104,-27,119),(.8,-.2,0))
    for x in (-104,104):
        for z in (43,81,119,157,192):
            if x==-104 and z==119:continue
            emitter((x,-27,z),(-math.copysign(.8,x),-.2,0))
    for x in (-84,-56,-28,0,28,56,84):emitter((x,4,190),(0,0,-1))
    # Side service ladders, behind emitters; seventeen heads in total.
    for side in (-1,1):
        x=side*122
        for y in (44,57):rod('service ladder rail',(x,y,22),(x,y,191),.8,'detail')
        for z in range(28,190,9):rod('ladder rung',(x,44,z),(x,57,z),.7,'detail')
        tube('tower cooling manifold',[(x,63,22),(x,66,184),(side*104,48,208)],1.4,'cable')
    with group('B'):
        # B intentionally includes the whole physical machine: actual overhead plan.
        pass
    box('haze service console',(-77,44,31),(44,32,37),8)
    for y in range(33,57,5):rod('haze console vent',(-99,y,23),(-99,y,41),.5,'detail')
    for x in (-80,-40,0,40,80):
        box('deck haze emitter',(x,-51,15),(21,10,6),2)
        for xx in (-5,0,5):cyl('haze nozzle',(x+xx,-51,19),1.2,2,'detail')
    box('timing controller',(85,47,33),(32,31,42),5)
    for x in (76,85,94):optics((x,30,38),2.8,4)
    # Quiet projected knot: sparse white/teal isocontours, no hard luminous field.
    for k in (-1,0,1):
        pts=[]
        for i in range(221):
            t=T*i/220;pts.append((39*(math.sin(t)+.65*math.sin(2*t)),-14+22*math.cos(t),105+37*math.cos(2*t)+k*.9))
        g.wire('illustrative luminous locus',pts,.06,'shell')
    mark('OPTICAL HEAD',(-98,-29,119),'INFRARED EMITTER')
    mark('SERVICE BRIDGE',(38,36,205),'7 HEADS POINTING DOWN')
    mark('IMAGE VOLUME',(45,-14,122),'40 × 22 × 18 m')
    mark('HAZE CIRCUIT',(-79,33,43),'FEEDS 5 DECK EMITTERS')
    mark('CLOCK DISTRIBUTION',(85,29,40),'KEEPS EVERY HEAD IN STEP')
    kit.GROUPS['B']={'parts':g.parts[:],'wires':g.wires[:]}
    return 24,22


def aroma_command():
    # Six representative channels in a fictional 96-channel metering bank.
    for i in range(6):
        x=-50+i*20
        with group('B'):
            cyl('odorant socket',(x,6,41),6,17,'structure')
            ring('socket seal',(x,6,58),7,1.4,2)
            cyl('metering valve',(x,6,23),5,14,'detail')
            for z in (27,32):ring('valve collar',(x,6,z),5.8,1,1,role='detail')
            box('valve coil connector',(x,-1,30),(7,6,7),1,'accent')
            rod('dosing capillary',(x,6,22),(x,6,13),.7,'cable')
        tube('metered flow',[(x,6,13),(x,-8,9),(x*.12,-20,9)],.6,'detail')
    with group('C'):
        box('mixing die',(0,-20,7),(23,18,5),2)
        for i in range(6):rod('mixer channel',(-8+i*3,-26,10),(-8+i*3,-14,10),.3,'accent')
        rod('outlet tube',(0,-29,8),(0,-47,8),2)
        ring('heated outlet',(0,-47,8),5,2,9,(0,-1,0))
        for y in (-42,-38,-34):ring('heater band',(0,y,8),3,.7,1,(0,1,0),'detail')
    box('carrier manifold',(0,8,17),(126,25,8),4)
    for x in (-63,63):
        box('bank mounting ear',(x,8,19),(9,37,6),2)
        for y in (-5,20):cyl('mount fastener',(x,y,23),1.6,2,'detail',n=6)
    tube('carrier gas inlet',[(-75,8,15),(-69,8,15),(-65,8,16)],2,'cable')
    flange('carrier union',(-75,8,15),5,(-1,0,0),2)
    for key,p in [('METER',(-30,6,29)),('MIX',(0,-20,9)),('CARRIER',(-74,8,16)),('OUTLET',(0,-50,8))]:mark(key,p,'FICTIONAL HARDWARE / NOT RECEPTOR DATA')
    return 25,33


if __name__=='__main__':
    for slug,fn in [('presence-rig',presence),('volumetric-stage',stage),('aroma-command',aroma_command)]:
        entry={'slug':slug,'number':0};kit.reset(entry);az,el=fn();kit.save(entry,az,el)
    sys.stdout.flush();os._exit(0)
