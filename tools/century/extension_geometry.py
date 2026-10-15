"""Eight new machines. Service views are actual subsets of their main models."""
from .kit import *
from . import kit
from .quality_geometry import gear


def ribs(p,size,count=9):
 for i in range(count):
  x=p[0]-size[0]/2+size[0]*(i+.5)/count
  box('cast cooling rib',(x,p[1],p[2]),(1.5,size[1],size[2]),.6,'detail')


def instrument(p,w=38,h=22):
 box('rounded instrument casting',p,(w,12,h),4)
 box('instrument bezel',(p[0],p[1]-7,p[2]),(w-5,2,h-5),2,'detail')
 for i in range(5):rod('engraved scale',(p[0]-w*.3+i*w*.15,p[1]-8,p[2]-3),(p[0]-w*.3+i*w*.15,p[1]-8,p[2]+3),.32,'accent')
 for x in (-w*.36,w*.36):cyl('face screw',(p[0]+x,p[1]-8,p[2]-h*.3),1.1,2,'detail',(0,-1,0),6)
 # Separate bezel, dial and service fasteners remain visible from the camera.
 for x in (-w*.36,w*.36):
  for z in (-h*.31,h*.31):
   cyl('bezel captive screw',(p[0]+x,p[1]-9,p[2]+z),.75,1.7,'detail',(0,-1,0),6)
 for xx in (-w*.22,w*.22):
  ring('instrument dial',(p[0]+xx,p[1]-9,p[2]),h*.22,1,1,(0,-1,0),'detail')
  rod('dial needle',(p[0]+xx,p[1]-11,p[2]),(p[0]+xx+h*.11,p[1]-11,p[2]+h*.1),.25,'accent')
 for i in range(5):box('case ventilation slot',(p[0]+w/2+.3,p[1]-3+i*1.5,p[2]),(1,.5,h*.35),.2,'detail')


def strip_recorder(p,w=48,h=27):
 # Housing behind the paper path; a stylus on a guide rod marks the strip at each contact.
 box('recorder housing',p,(w,12,h),4)
 rod('stylus guide',(p[0]-w*.42,p[1]-8,p[2]),(p[0]+w*.42,p[1]-8,p[2]),.6,'detail')
 box('marking stylus carriage',(p[0]-w*.12,p[1]-9,p[2]),(6,4,5),1.2,'accent')
 for x in (-w*.42,w*.42):
  for z in (-h*.36,h*.36):cyl('housing screw',(p[0]+x,p[1]-6.5,p[2]+z),1,1.2,'detail',(0,-1,0),6)


def sight_glass(p,h=36):
 # Vertical glass between two bosses, a float on the gas/liquid line and an engraved scale.
 for z in (0,h):box('sight glass boss',(p[0],p[1]+3,p[2]+z),(11,7,6),2)
 cyl('sight glass',(p[0],p[1],p[2]+3),2.6,h-6,'shell')
 for x in (-5,5):rod('glass guard',(p[0]+x,p[1]-1,p[2]+3),(p[0]+x,p[1]-1,p[2]+h-3),.6,'detail')
 cyl('level float',(p[0],p[1],p[2]+h*.55),3.1,3,'accent')
 box('level scale',(p[0]+8.5,p[1]+1,p[2]+h/2),(3,1.5,h-8),.5,'detail')
 for i in range(7):
  z=p[2]+6+i*(h-12)/6
  rod('level graduation',(p[0]+7,p[1]-.2,z),(p[0]+(10 if i%3==0 else 8.6),p[1]-.2,z),.22,'detail')


def dial_indicator(p,r=10):
 # One round dial with its stem and lifting cap: the reference head reads a single travel.
 cyl('dial indicator case',p,r,4,'structure',(0,-1,0))
 ring('indicator bezel',(p[0],p[1]-4,p[2]),r+.5,1.6,1.2,(0,-1,0))
 for i in range(20):
  a=math.tau*i/20;l=2.2 if i%5==0 else 1.2
  rod('dial graduation',(p[0]+(r-1.8)*math.cos(a),p[1]-4.4,p[2]+(r-1.8)*math.sin(a)),(p[0]+(r-1.8-l)*math.cos(a),p[1]-4.4,p[2]+(r-1.8-l)*math.sin(a)),.2,'detail')
 rod('indicator needle',(p[0],p[1]-4.8,p[2]),(p[0]+r*.62,p[1]-4.8,p[2]+r*.36),.35,'accent')
 cyl('needle hub',(p[0],p[1]-4.2,p[2]),1.2,.8,'detail',(0,-1,0),16)
 ring('revolution counter',(p[0],p[1]-4.3,p[2]+r*.45),r*.22,.4,.5,(0,-1,0),'detail')
 cyl('indicator stem',(p[0],p[1]-2,p[2]+r),1.7,6,'detail')
 cyl('lifting cap',(p[0],p[1]-2,p[2]+r+6),2.4,2,'detail')


def timing_unit(p,w=40,h=15):
 # Rack-mounted clock module: pull handles, a time display, a lock lamp and bayonet inputs.
 box('timing unit panel',p,(w,3,h),1.5)
 for x in (-w/2+2.5,w/2-2.5):
  box('pull handle',(p[0]+x,p[1]-4,p[2]),(2,1.6,h-3),.6,'detail')
  for z in (-h/2+3,h/2-3):rod('handle standoff',(p[0]+x,p[1]-1.5,p[2]+z),(p[0]+x,p[1]-4,p[2]+z),.5,'detail')
 box('time display window',(p[0]-4,p[1]-1.9,p[2]+3),(18,.8,5),.6,'accent')
 cyl('lock lamp',(p[0]+9,p[1]-1.6,p[2]+3),1.2,1.2,'detail',(0,-1,0),12)
 for x in (-11,0,11):
  cyl('timing connector',(p[0]+x,p[1]-1.5,p[2]-3.5),1.6,3,'detail',(0,-1,0))
  ring('bayonet collar',(p[0]+x,p[1]-4.5,p[2]-3.5),2.3,.6,1,(0,-1,0),'detail')


def reed_gauge(p,w=26,h=14,reeds=7):
 # Vibrating-reed frequency meter: graded reeds behind a window; the one in tune swings widest.
 box('reed gauge case',p,(w,4,h),2)
 box('reed window',(p[0],p[1]-2.2,p[2]-1),(w-6,.6,h-6),.8,'detail')
 for i in range(reeds):
  x=p[0]-(w-9)/2+i*(w-9)/(reeds-1);length=3+i*.55
  rod('tuned reed',(x,p[1]-2.8,p[2]-4.5),(x,p[1]-2.8,p[2]-4.5+length),.35,'detail')
  box('reed flag',(x,p[1]-3,p[2]-4.5+length),(1.3,.4,1),.2,'accent' if i==reeds//2 else 'detail')
  rod('frequency mark',(x,p[1]-2.6,p[2]+h/2-2.4),(x,p[1]-2.6,p[2]+h/2-1.2),.2,'detail')


def arc_scale(pivot,radius,a0,a1,y):
 # Tension scale swept round the dancer pivot; the arm's own tip is the pointer.
 pts=[(pivot[0]+radius*math.sin(math.radians(a0+(a1-a0)*i/24)),y,pivot[2]+radius*math.cos(math.radians(a0+(a1-a0)*i/24))) for i in range(25)]
 tube('tension scale arc',pts,.6,'detail')
 for i in range(7):
  a=math.radians(a0+(a1-a0)*i/6);l=3 if i%3==0 else 1.8
  rod('tension graduation',(pivot[0]+radius*math.sin(a),y,pivot[2]+radius*math.cos(a)),(pivot[0]+(radius+l)*math.sin(a),y,pivot[2]+(radius+l)*math.cos(a)),.25,'detail')
 for a in (a0,a1):rod('scale spoke',(pivot[0],y,pivot[2]),(pivot[0]+radius*math.sin(math.radians(a)),y,pivot[2]+radius*math.cos(math.radians(a))),.5,'detail')


def spring(a,b,r=5,turns=9):
 d=Vector(b)-Vector(a);axis=d.normalized();u=axis.cross(Vector((0,1,0)))
 if u.length<.1:u=axis.cross(Vector((1,0,0)))
 u.normalize();v=axis.cross(u)
 pts=[Vector(a)+d*(i/(turns*24))+r*(u*math.cos(T*i/24)+v*math.sin(T*i/24)) for i in range(turns*24+1)]
 g.wire('wound return spring',pts,.3,'detail')


def velvet_hammer():
 # Interrupted release ring: deliberately open for inspection, not a torus filler.
 views(B=(22,25),C=(32,33))
 for r in (91,104):ring('split carrier ring',(0,0,125),r,5,18,(0,-1,0),start=35,end=325)
 for a in range(45,326,35):
  x=98*math.cos(math.radians(a));z=125+98*math.sin(math.radians(a))
  joint((x,-23,z),6,(0,-1,0))
  rod('radial web',(x*.91,7,125+(z-125)*.91),(x*1.065,7,125+(z-125)*1.065),2,'detail')
 for i,a in enumerate((62,178,287)):
  with group('B') if i==0 else at():
   with at((96*math.cos(math.radians(a)),-17,125+96*math.sin(math.radians(a))),a-90,'Y'):
    box('load transfer saddle',(0,0,0),(43,30,18),6)
    for x in (-16,16):rod('cassette guide',(x,0,7),(x,0,42),2)
    ring('cam sector',(0,-5,25),15,5,8,(0,-1,0),start=15,end=270)
    joint((9,-17,30),4,(0,-1,0));rod('roller rocker',(9,-15,30),(20,-15,14),2)
    spring((-13,-18,10),(-13,-18,38),3,7)
    box('retaining jaw',(12,0,44),(22,16,9),3,'accent')
    cyl('release shaft',(0,-9,25),3,28,'detail',(0,1,0))
 with group('C'):
  strip_recorder((62,-12,57),48,27)
  box('event strip magazine',(87,0,58),(20,29,32),4)
  for z in (48,57,66):box('record slot',(88,-16,z),(13,2,3),.5,'detail')
  cyl('reset crown',(63,-15,35),5,5,'detail',(0,-1,0))
  # Paper feed and indexed spool expose the recorder's purpose.
  for x in (49,76):
   flange('paper roller bearing',(x,-20,51),5,(0,-1,0),2)
   cyl('paper roller',(x,-17,51),3,21,'detail',(0,1,0))
  for x in range(45,82,5):
   rod('time strip graduation',(x,-20,61),(x,-20,65 if x%10==0 else 63),.25,'detail')
  for z in range(47,72,4):box('spool case rib',(99,0,z),(2,23,1.5),.5,'detail')
  box('paper outlet',(60,-20,44),(25,3,5),1,'detail')
  box('event paper strip',(62.5,-18.7,57),(27,.5,17),.3,'shell')
 # The loom runs on to the ring, so it stays out of the recorder's detail view.
 tube('time-tag loom',[(60,0,47),(45,18,35),(5,20,30)],1)
 for a in (35,325):
  x=98*math.cos(math.radians(a));z=125+98*math.sin(math.radians(a))
  box('split end termination',(x,-8,z),(14,27,14),4)
  cyl('end witness',(x,-24,z),3,3,'detail',(0,-1,0),6)
 mark('TRANSFER CAM',(-90,-30,128),'THREE CASSETTES ROUND THE RING')
 mark('SPLIT RING',(-94,3,99),'TWIN CARRIERS, OPEN FOR INSPECTION')
 mark('RELEASE LOG',(68,-20,58),'PAPER STRIP, MARKED AT EACH CONTACT')
 mark('RETAINING JAW',(50,-18,210),'ONE JAW PER CASSETTE')
 return 27,22


def bubble_bailiff():
 views(B=(25,40),C=(-22,26))
 # Thick sinuous channel walls with an open service side.
 path=[(-105,0,45),(-75,0,48),(-48,0,78),(30,0,95),(65,0,125),(35,0,158),(-42,0,177),(-62,0,207),(-22,0,229),(82,0,229)]
 for dy in (-14,14):organic_branch('formed channel rail',[(x,dy,z) for x,y,z in path],5)
 for i in range(1,len(path)-1):
  x,y,z=path[i];rod('channel cross rib',(x,-14,z),(x,14,z),2,'detail')
 for x,z in ((-100,45),(82,229)):flange('liquid line union',(x,0,z),13,(1,0,0));cyl('flow stub',(x,0,z),7,20,'structure',(1,0,0))
 with group('B'):
  box('membrane cassette',(-20,5,99),(73,38,15),6)
  for y in (-13,-6,1,8,15):rod('wick support',(-51,y,109),(12,y,109),.8,'detail')
  for x in range(-47,15,8):rod('capillary channel',(x,-15,110),(x,19,110),.4,'accent')
  for x in (-48,9):cyl('cassette retainer',(x,-13,111),2,3,'detail',n=6)
  flange('vent plenum outlet',(-18,21,99),8,(0,1,0))
 with group('C'):
  vessel('gas buffer',(63,30,25),20,49)
  flange('trap outlet',(63,30,78),9)
  cyl('isolation valve stem',(63,30,86),4,20,'detail')
  ring('manual vent wheel',(63,30,103),15,3,4)
  for a in (0,120,240):rod('wheel spoke',(63,30,105),(63+12*math.cos(math.radians(a)),30+12*math.sin(math.radians(a)),105),1,'detail')
  sight_glass((63,6,31),36)
 tube('gas-only riser',[(-18,29,99),(3,46,100),(51,49,95),(63,30,78)],1.2)
 for x,z in ((-74,49),(55,120)):
  box('isolated saddle foot',(x,8,15),(34,48,10),5)
  rod('channel support',(x,8,20),(x,8,z),3)
  flange('saddle adjuster',(x,8,22),6)
  rod('saddle brace',(x,8,z),(x,0,z),4)
 # Repeated formed ribs follow the actual channel rather than a bounding box.
 for a,b in zip(path,path[1:]):
  for f in (.25,.5,.75):
   q=Vector(a).lerp(Vector(b),f)
   rod('channel retention strap',(q.x,-14,q.z),(q.x,14,q.z),.9,'detail')
 mark('LIQUID PATH',(-83,0,49),'OPEN SERVICE SIDE / COVER OMITTED')
 mark('WICK CASSETTE',(-20,-10,108),'GAS LEAVES BY THE VENT PLENUM')
 mark('GAS BUFFER',(63,25,58),'END OF THE GAS-ONLY RISER')
 mark('RETURN UNION',(82,0,229),'FLANGED OUTLET TO THE LOOP')
 return 27,18


def key_concord():
 views(B=(24,50),C=(-20,35))
 hull('waisted lock bed',[(-100,12,6,0),(-80,44,10,0),(0,32,10,0),(80,44,10,0),(100,12,6,0)])
 for x in (-64,64):
  cyl('equal authority barrel',(x,0,20),25,36)
  flange('barrel rim',(x,0,56),28)
  gear((x,0,63),23,20,axis=(0,0,1))
  box('key bow',(x,0,93),(30,9,24),8)
  rod('key shaft',(x,0,60),(x,0,88),3,'detail')
  for y in (-19,19):rod('carriage guide',(x-30,y,14),(x+30,y,14),2,'detail')
 with group('B'):
  box('coincidence yoke',(0,0,47),(46,28,12),5)
  for side in (-1,1):
   rod('equal-input lever',(side*17,0,52),(side*63,0,63),3)
   joint((side*17,-6,52),5,(0,1,0))
   box('blocking pawl',(side*10,-19,37),(9,12,16),2,'accent')
   spring((side*10,-20,26),(side*10,-20,41),2,6)
  cyl('coincidence pivot',(0,-18,47),5,36,'detail',(0,1,0))
 with group('C'):
  # Open casting exposes the bolt and return spring in A and C.
  for x in (-24,24):box('revocation side rail',(x,55,27),(6,64,22),3)
  for y in (27,83):box('revocation end bridge',(0,y,21),(50,8,12),3)
  box('witness bridge',(0,49,39),(45,8,7),2)
  for x in (-24,24):
   for y in (29,81):cyl('keeper fastener',(x,y,39),2,3,'detail',n=6)
  box('retractable bolt',(0,82,27),(21,48,12),3)
  for x in (-17,17):rod('return guide',(x,38,28),(x,88,28),2,'detail')
  spring((-17,43,28),(-17,76,28),4,8)
  cyl('manual return crown',(0,49,44),12,8,'detail')
  for a in range(0,360,45):rod('crown knurl',(10*math.cos(math.radians(a)),49+10*math.sin(math.radians(a)),44),(10*math.cos(math.radians(a)),49+10*math.sin(math.radians(a)),51),.6,'detail')
 rod('bolt transmission',(0,0,43),(0,54,43),4)
 for x in (-64,64):
  for z in (25,33,41):ring('barrel witness band',(x,0,z),25.3,.9,1,role='detail')
  for a in range(0,360,60):
   cyl('barrel mounting screw',(x+32*math.cos(math.radians(a)),32*math.sin(math.radians(a)),12),2,3,'detail',n=6)
  box('key identification inset',(x,-5,94),(17,1,11),3,'detail')
 mark('KEY ONE',(-64,0,89),'GEARED BARREL / ID INSET ON THE BOW')
 mark('KEY TWO',(64,0,89),'SAME PARTS, MIRRORED')
 mark('COINCIDENCE YOKE',(0,-10,50),'TWO SPRUNG PAWLS, ONE PIVOT')
 mark('WITHDRAWAL',(0,89,29),'KNURLED CROWN RETURNS THE BOLT')
 return 22,35


def metric_embassy():
 views(B=(28,33),C=(18,32))
 ring('open gauge carousel',(0,0,29),91,14,12,start=18,end=330)
 ring('carousel undercut',(0,0,17),82,6,10,start=18,end=330)
 for i,a in enumerate(range(40,330,40)):
  with at((73*math.cos(math.radians(a)),73*math.sin(math.radians(a)),42),a):
   with group('C') if i==0 else at():
    box('keyed adaptor shoe',(0,0,0),(26,30,8),4)
    cyl('coded connector',(0,0,5),10,20)
    ring('connector rim',(0,0,24),12,3,4)
    for j in range(5):cyl('contact pin',(5*math.cos(T*j/5),5*math.sin(T*j/5),27),.8,6,'detail',n=12)
    box('polarisation key',(10,0,17),(5,4,10),1,'accent')
    for z in (9,13,17):ring('thread crest',(0,0,z),10.6,.8,1,role='detail')
 gear((0,0,22),33,28,(0,0,1));cyl('carousel spindle',(0,0,0),12,46)
 for x,y in ((-62,-50),(63,-50),(0,70)):
  box('cast foot',(x,y,-8),(32,30,12),7)
  rod('carousel pedestal',(x,y,-2),(x,y,21),5)
  flange('pedestal collar',(x,y,0),9)
 # Actual radial spokes connect the index spindle to the interrupted rim.
 for a in (45,120,195,270):
  rod('carousel radial web',(25*math.cos(math.radians(a)),25*math.sin(math.radians(a)),23),(84*math.cos(math.radians(a)),84*math.sin(math.radians(a)),23),4,'detail')
 rod('scanner mast',(-92,24,5),(-92,24,139),7)
 organic_branch('arched measuring arm',[(-92,24,125),(-91,24,155),(-65,21,173),(-27,18,171),(9,8,150)],5)
 with group('B'):
  box('metrology head',(9,8,141),(48,31,27),8)
  for x in (-11,29):rod('probe slide',(x,8,126),(x,8,94),2,'detail')
  for x in (-11,29):box('three-wire jaw',(x,8,96),(13,20,7),2)
  for j in range(3):rod('reference wire',(-17+j*4,-1,99),(-17+j*4,17,99),.7,'accent')
  dial_indicator((9,-8,143),10)
 tube('probe return loom',[(9,27,145),(-50,45,160),(-105,43,80),(-80,38,15)],1)
 mark('REFERENCE HEAD',(9,-6,144),'HANGS FROM AN ARCHED ARM')
 mark('ADAPTOR LIBRARY',(50,48,60),'EIGHT KEYED SHOES ON THE RIM')
 mark('GAUGE CAROUSEL',(-79,-29,41),'INTERRUPTED RIM / THREE PEDESTALS')
 mark('DRIVE INDEX',(0,-8,25),'GEARED SPINDLE / FOUR RADIAL WEBS')
 return 28,28


def muon_customs():
 views(B=(23,24),C=(28,22))
 # Open-sided gantry. The absence of an emitter is intentional.
 for y in (-58,58):
  organic_branch('C frame casting',[(-118,y,30),(-139,y,42),(-144,y,92),(-144,y,224),(-130,y,265),(-97,y,280),(100,y,280)],9)
  box('stabilising shoe',(-127,y,12),(70,35,20),8)
 for z in (80,220):rod('gantry tie',(-145,-60,z),(-145,60,z),5)
 for level in (43,248):
  with group('B') if level==248 else at():
   for dz in (0,12):
    panel('tracking cassette',(0,0,level+dz),(207,119),nx=12,ny=4)
    for i in range(10):rod('scintillator strip',(-92+20*i,-53,level+dz+3),(-92+20*i,53,level+dz+3),1,'accent' if i%3==0 else 'detail')
    for x in (-109,109):box('readout spine',(x,0,level+dz),(9,122,9),2,'detail')
   for x in (-86,86):rod('drawer extraction bar',(x,-69,level+8),(x+15,-69,level+8),2,'detail')
 box('cargo pallet',(5,0,70),(160,102,14),5)
 box('sealed test crate',(10,0,122),(110,80,89),12,'shell')
 for x in (-36,55):box('cargo strap',(x,0,122),(4,83,92),1,'detail')
 with group('C'):
  box('coincidence clock rack',(-137,-82,137),(47,36,72),8)
  for z in (114,136,158):timing_unit((-137,-101.5,z),40,15)
  ribs((-137,-63,140),(34,5,57),8)
  tube('rack service pigtail',[(-124,-78,170),(-118,-74,181),(-107,-64,181)],1)
 tube('clock loom',[(-107,-64,181),(-108,-60,210),(-104,-61,250)],1)
 for y in (-58,58):
  for z in (43,253):rod('cassette attachment',(-145,y,z),(-104,y,z),4,'detail')
 for x in (-34,54):
  box('cargo strap buckle',(x,-43,131),(13,5,17),2,'detail')
  for z in (86,159):box('cargo edge protector',(10,-41,z),(93,3,6),2,'detail')
 box('manifest plate',(10,-44,128),(40,2,23),3,'detail')
 for i in range(6):rod('manifest code',(-3+i*5,-46,121),(-3+i*5,-46,135),.6,'detail')
 mark('UPPER TRACKER',(30,-40,262),'TWO PLANES, TEN STRIPS EACH')
 mark('LOWER TRACKER',(35,-40,46),'SAME PAIR, BELOW THE PALLET')
 mark('CLOCK RACK',(-137,-104,139),'THREE TIMING UNITS ON THE FRAME')
 mark('PASSIVE BAY',(-43,-40,95),'STRAPPED TEST CRATE / NO EMITTER')
 return 23,17


def resonance_tailor():
 views(B=(30,27),C=(-20,30))
 ring('split machine collar',(0,0,5),38,9,26,start=16,end=344)
 for x in (-38,38):box('clamp ear',(x,0,21),(22,27,13),4);cyl('clamp screw',(x,0,10),3,24,'detail')
 for x in (-57,57):rod('fork load spider',(0,9,30),(x,9,39),6)
 for i,(x,h) in enumerate(((-57,160),(0,205),(57,133))):
  with group('B') if i==1 else at():
   box('fork root',(x,9,44),(35,30,22),7)
   for dx in (-12,12):rod('parallel flexure',(x+dx,8,45),(x+dx,8,h),1.4,'detail')
   box('sliding mass',(x,8,h-24),(42,35,37),8)
   for y in (-12,28):box('mass cheek',(x,y,h-24),(45,4,28),2,'detail')
   cyl('tuning leadscrew',(x,8,51),2,h-37,'detail')
   for z in range(64,h,10):ring('screw witness',(x,8,z),2.9,.6,1,role='detail')
   reed_gauge((x,-16,h-24),26,14)
   spring((x,23,53),(x,23,h-45),4,9)
   box('end stop',(x,8,h+7),(31,19,8),3)
 with group('C'):
  box('locking bridge',(0,-35,53),(61,32,14),5)
  for x in (-22,22):cyl('lock screw',(x,-35,55),3,24,'detail');ring('lock knob',(x,-35,78),9,3,4)
  rod('crossed flexure one',(-25,-54,30),(25,-54,67),1,'accent')
  rod('crossed flexure two',(25,-52,30),(-25,-52,67),1,'accent')
  box('travel stop',(0,-35,63),(14,18,11),2,'detail')
  for x in (-25,25):
   for z in (30,67):
    rod('flexure anchorage',(x,-54,z),(x,-35,53),2,'detail')
    cyl('flexure clamp',(x,-56,z),2.5,3,'detail',(0,-1,0),6)
 mark('CENTRE MASS',(0,-10,181),'TALLEST BRANCH, OWN REED GAUGE')
 mark('SHORT BRANCH',(57,8,109),'SHORTEST FLEXURES OF THE THREE')
 mark('LOCK BRIDGE',(-22,-44,81),'TWO KNOBS ON THE CENTRE ROOT')
 mark('HOST CLAMP',(-24,-30,14),'SPLIT COLLAR, TWO SCREWS')
 return 27,21


def suture_loom():
 views(B=(18,39),C=(20,30))
 ring('open horseshoe',(0,0,42),91,12,15,start=12,end=327)
 ring('lower service track',(0,0,22),82,6,12,start=12,end=327)
 for a in (35,125,235,305):
  x=83*math.cos(math.radians(a));y=83*math.sin(math.radians(a));rod('track spacer',(x,y,23),(x,y,57),3)
 with group('B'):
  for side in (-1,1):
   motor((side*62,-16,53),11,24,(0,0,1))
   joint((side*52,-16,82),8,(0,0,1))
   rod('needle handoff arm',(side*52,-16,84),(side*12,-4,111),3)
   box('needle jaw',(side*10,-4,111),(12,14,9),3)
   for dx in (-3,3):rod('jaw finger',(side*10+dx,-4,112),(side*10+dx,6,119),.9,'detail')
  ring('test needle',(0,0,114),15,.8,1,(0,1,0),role='accent',start=12,end=168)
 with group('C'):
  cyl('thread spool',(61,57,60),21,31,'structure',(0,1,0))
  for y in (56,87):flange('spool cheek',(61,y,60),24,(0,1,0),3)
  for y in range(60,85,4):ring('wound thread',(61,y,60),21.3,.4,.6,(0,1,0),'detail')
  joint((31,70,82),6,(0,1,0));rod('dancer arm',(31,70,82),(22,70,103),2)
  spring((32,72,83),(47,72,102),2,6)
  arc_scale((31,70,82),28,-55,5,66)
  rod('dancer pointer',(22,69,103),(20.3,67,106.9),.4,'accent')
  box('spool bracket',(61,72,38),(52,38,8),4)
  rod('dancer pivot support',(31,70,40),(31,70,82),3)
  rod('spring return lug',(47,72,40),(47,72,102),1.5,'detail')
  rod('spool bearing pedestal',(61,73,38),(61,73,60),5)
 tube('tensioned thread',[(61,58,80),(24,70,104),(7,24,126),(0,0,127)],.35)
 panel('neutral test membrane',(0,5,89),(37,43),nx=5,ny=5,role='shell')
 for x in (-20,20):
  rod('membrane support',(x,63,50),(x,25,89),2,'detail')
  box('membrane clamp',(x,24,89),(6,12,7),2,'detail')
 for x,y in ((-68,43),(60,54),(-28,-72)):box('bench shoe',(x,y,5),(29,34,11),5);rod('bench stand',(x,y,10),(x,y,34),4)
 mark('DUAL NEEDLE GRIP',(-10,-4,114),'TWO MOTORISED ARMS, MIRRORED')
 mark('THREAD DANCER',(25,70,101),'SPRUNG ARM OVER A TENSION SCALE')
 mark('TEST MEMBRANE',(16,5,90),'CLAMPED BETWEEN TWO SUPPORTS')
 mark('OPEN SERVICE TRACK',(-78,0,49),'CLEANING ACCESS BUILT IN')
 return 28,32


def round_bowl():
 profile=[(-38,22),(-36,28),(-32,34),(-25,40),(-15,43),(10,43),(23,41),(27,38)]
 n=96;vs=[(r*math.cos(T*j/n),r*math.sin(T*j/n),z) for z,r in profile for j in range(n)]
 fs=[(i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j) for i in range(len(profile)-1) for j in range(n)]
 fs.extend([tuple(reversed(range(n))),tuple(range((len(profile)-1)*n,len(profile)*n))])
 g.mesh('spun galley bowl',vs,fs)


def spin_table():
 views(B=(18,32),C=(15,36))
 for x in (-66,66):
  organic_branch('swept cradle leg',[(x,-38,5),(x,-32,30),(x,-15,65),(math.copysign(78,x),0,128)],6)
  box('magnetic galley foot',(x,-38,4),(47,38,12),8)
 ring('fixed gimbal hoop',(0,0,128),78,6,10,(0,1,0),start=0,end=360)
 with group('B'):
  joint((-79,-3,128),19,(1,0,0))
  motor((-114,-3,128),17,30,(1,0,0))
  gear((-78,-4,128),28,26,(1,0,0))
  instrument((-104,-24,106),29,18)
  rod('torque arm',(-97,-3,112),(-66,-15,70),3,'detail')
 with at((0,0,128),-26,'X'):
  # Spun round bowl; unlike a pump housing it has a circular food cavity.
  round_bowl()
  for z,r in ((-24,40),(10,43),(23,41)):
   ring('bowl rolled seam',(0,0,z),r+1,1.3,2,role='detail')
  for x in (-1,1):
   rod('rotor trunnion',(x*40,0,0),(x*78,0,0),7)
   flange('trunnion retainer',(x*67,0,0),12,(x,0,0))
  ring('inner stir boundary',(0,0,13),36,2,4,role='detail')
  with group('C'):
   ring('lid seal',(0,0,27),45,4,5)
   cyl('spun lid',(0,0,30),45,8)
   ring('lid rolled rim',(0,0,37),46,2,2,role='detail')
   for a in (25,145,265):
    rod('lid pressed rib',(19*math.cos(math.radians(a)),19*math.sin(math.radians(a)),39),(35*math.cos(math.radians(a)),35*math.sin(math.radians(a)),39),.6,'detail')
   for a in (0,120,240):
    with at((41*math.cos(math.radians(a)),41*math.sin(math.radians(a)),34),a):
     box('lid latch',(0,0,0),(17,10,12),3);joint((3,0,3),3,(0,1,0))
   ring('lid grip',(0,0,40),15,3,8,(0,1,0),start=0,end=180)
   cyl('pressure equalisation port',(22,0,40),4,7,'detail')
  rod('balance outrigger',(0,0,-34),(0,0,-102),5)
  for z in (-78,-87,-96):cyl('trim counterweight',(0,0,z),19,7,'detail')
 tube('cradle service cable',[(-106,8,121),(-99,26,73),(-66,20,28),(-66,-26,10)],1)
 mark('SEALED VESSEL',(15,-40,142),'SPUN BOWL, THREE ROLLED SEAMS')
 mark('DRIVE BEARING',(-100,-3,130),'MOTOR OUTBOARD OF THE HOOP')
 mark('BALANCE MASS',(0,-35,46),'THREE TRIM WEIGHTS OPPOSITE THE LID')
 mark('LID INTERLOCK',(36,-14,162),'HALF-RING GRIP / PRESSED RIBS')
 return 24,22

BUILDERS={101:velvet_hammer,103:bubble_bailiff,104:key_concord,105:metric_embassy,106:muon_customs,107:resonance_tailor,108:suture_loom,110:spin_table}
