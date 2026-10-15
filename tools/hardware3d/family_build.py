"""Ten individually authored devices sharing a retro-industrial construction language."""
import sys,os,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import family_core as g
from mathutils import Vector,Matrix
T=math.tau

def rotor(x,y,z,r=61):
 o=g.annulus('rolled fan duct',r-7,r,0,20,role='structure',cz=0)
 o.matrix_world=Matrix.Translation((x,y,z))@Matrix.Rotation(math.pi/2,4,'X')
 g.cyl('fan hub',x,y,z-5,9,20,'structure',32)
 for k in range(7):
  a=k*T/7;vs=[]
  for rr,ang in [(10,a),(r*.6,a+.12),(r-9,a+.42),(r-9,a+.65),(r*.5,a+.37),(10,a+.35)]:vs.append((x+rr*math.cos(ang),y+rr*math.sin(ang),z+8))
  g.mesh('swept rotor blade',vs,[tuple(range(6))],'detail')
 for k in range(12):
  a=k*T/12;g.cyl('duct rivet',x+(r-3)*math.cos(a),y+(r-3)*math.sin(a),z+20,1.3,1,'detail',8)

def sky_racer():
 from sky_racer import build
 return build()

def organ_foundry():
 # A sterile, rounded incubator with its door removed and perfusion equipment below.
 g.base(174,132)
 for x in (-150,150):g.softbox('cast column',(x,40,223),(32,45,370),13)
 g.softbox('curved crown',(0,40,407),(318,116,46),20)
 g.softbox('rear sterile wall',(0,99,248),(279,12,271),6,'shell')
 g.softbox('chamber floor',(0,15,101),(286,190,25),12)
 for x in (-103,103):g.beam('Z guide',(x,58,125),(x,58,377),5,'detail')
 for z in (128,374):g.softbox('guide bridge',(0,58,z),(223,23,16),6)
 g.softbox('moving gantry',(0,24,303),(229,30,23),8)
 for x in (-97,97):g.beam('gantry slide',(x,58,303),(x,-55,303),4,'detail')
 g.softbox('print carriage',(10,-25,301),(53,39,28),8)
 for x in (-7,0,7,14,21,28):g.cyl('ink nozzle',x,-25,268,1.8,21,'detail',12)
 for i in range(6):
  x=-110+i*44;g.cyl('cell vial',x,30,434,14,43,'structure',40);g.cyl('vial cap',x,30,477,16,6,'detail',40)
  g.wire('ink line',[(x,29,435),(x,4,397),(x*.6,-4,345),(i*6-5,-25,318)],1.4,'cable')
 g.cyl('perfusion dish',0,0,119,76,17,'structure',64)
 # Kidney form with a lobed profile, authored rather than a generic sphere.
 vs=[];n=72
 for z,sc in [(139,.58),(145,.85),(157,1),(172,.86),(181,.5)]:
  for k in range(n):
   a=T*k/n;rx=(43-14*math.exp(-((a-math.pi)/.55)**2))*sc;vs.append((rx*math.cos(a),rx*1.4*math.sin(a),z))
 fs=[(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(4) for k in range(n)]
 g.mesh('printed kidney',vs,fs,'accent')
 for k in range(9):
  a=T*k/9;g.wire('vascular branch',[(0,0,181),(18*math.cos(a),22*math.sin(a),178),(32*math.cos(a),43*math.sin(a),164)],.6,'fine')
 g.softbox('perfusion console',(-92,-78,71),(75,65,56),17);g.dial(-100,-112,76,12)
 g.cyl('oxygenator',101,-62,44,22,49);g.flange(101,-62,93,25)
 for x in (-85,92):g.wire('perfusion tube',[(x,-71,93),(x,-76,130),(34 if x>0 else -34,-22,147)],2,'cable')
 for x in (-16,-5,6,17):g.softbox('metabolite sensor',(x,-79,83),(7,12,13),2,'accent')
 for lab,p in [('PRINT HEAD',(10,-25,283)),('CELL CARTRIDGES',(-66,30,460)),('PRINT FRONT',(24,-28,171)),('VASCULAR TREE',(0,0,181)),('PERFUSION PUMP',(-92,-90,76)),('OXYGENATOR',(101,-62,74)),('METABOLITE SENSORS',(5,-79,83))]:g.mark(lab,p)
 return (26,19)

def air_refinery():
 # Art-deco process tower, flanked by heat collectors and streamlined tank pods.
 g.base(195,121)
 g.casting('tapered process column',[(31,71,62),(55,74,64),(110,64,54),(350,51,48),(465,58,51),(477,63,54)])
 for z in (106,171,236,301,366,440):
  # 63, not 61: the column's rounded-square corners reach 61.5 at 236 and 61.0 at 445 and cut the bands' front rims
  g.flange(0,0,z,74 if z<180 else 63)
  g.dial(0,-58,z+23,9)
  for side in (-1,1):g.softbox('catalyst access cover',(side*28,-54,z+26),(25,11,25),6,'detail')
 g.softbox('contactor crown',(0,0,510),(295,134,60),26)
 for x in (-94,0,94):rotor(x,0,543,39)
 for x in range(-126,135,10):g.wire('sorbent lamella',[(x,-66,493),(x,-66,526)],.8,'detail')
 for x in (-123,123):
  g.ball('fuel tank',(x,12,106),(41,65,69));g.flange(x,12,163,19)
 g.softbox('electrolyser',(106,-60,53),(68,52,38),11);g.vents(106,-87,42,5,41)
 g.softbox('solar receiver',(-89,42,318),(39,42,83),11,'accent')
 for k in range(5):
  x=-150+k*75;g.beam('heliostat stalk',(x,-156,0),(x,-156,37),2,'detail')
  o=g.softbox('heliostat mirror',(x,-156,49),(55,36,3),2,'shell');o.rotation_euler.x=.4
 for lab,p in [('AIR CONTACTOR',(0,-67,512)),('ENZYME BEDS',(28,-57,390)),('CATALYST BEDS',(28,-57,263)),('SOLAR RECEIVER',(-89,22,318)),('MIRROR FIELD',(-75,-156,49)),('ELECTROLYSER',(106,-80,53)),('PRODUCT TANKS',(123,12,117))]:g.mark(lab,p)
 return (27,17)

def aroma_organ():
 # A countertop scent instrument: domed cartridge carousel and a front mixing bay.
 g.base(174,133)
 g.cyl('cartridge tray',0,0,45,146,10,'structure',96)
 # Exactly 96 vials: three concentric rings of 24, 32 and 40.
 for radius,n in [(72,24),(104,32),(134,40)]:
  for k in range(n):
   a=T*k/n;x,y=radius*math.cos(a),radius*math.sin(a)
   g.cyl('odorant vial',x,y,57,5,43,'detail',12);g.cyl('metering cap',x,y,100,6,4,'detail',12)
 g.casting('cutaway canopy',[(106,155,140),(111,155,140),(123,144,130),(150,122,109),(167,77,69),(173,31,28)],'shell',yc=0)
 # Only rear half of canopy remains, genuinely cut geometry instead of transparency.
 canopy=g.parts[-1][0];keep=[]
 for poly in canopy.data.polygons:
  if all(canopy.data.vertices[i].co.y>=0 for i in poly.vertices):keep.append(tuple(poly.vertices))
 v=[tuple(p.co) for p in canopy.data.vertices];new=g.bpy.data.meshes.new('rear hood');new.from_pydata(v,[],keep);new.update();canopy.data=new
 g.cyl('valve hub',0,0,51,44,28,'structure',64)
 for k in range(16):
  a=T*k/16;g.wire('capillary manifold',[(70*math.cos(a),70*math.sin(a),65),(45*math.cos(a),45*math.sin(a),68),(12*math.cos(a),12*math.sin(a),77)],.5,'cable')
 g.softbox('mixing chip',(0,-42,84),(33,30,9),5,'accent')
 g.softbox('front instrument panel',(0,-124,59),(129,32,44),14)
 for x in (-37,37):g.dial(x,-141,63,13)
 g.softbox('scrubber cartridge',(107,-56,74),(39,73,51),13);g.vents(107,-94,55,7,25)
 rotor(-97,-53,111,25)
 g.wire('heated outlet',[(0,-43,89),(0,-77,105),(0,-110,147),(0,-136,151)],6,'structure')
 g.along_y('outlet rim',0,-136,151,10,7,'detail',32)
 for lab,p in [('BASE ODORANT',(-104,0,85)),('VALVE RING',(39,-13,73)),('MANIFOLD',(-28,-28,72)),('MIXING CHIP',(0,-42,89)),('HEATED OUTLET',(0,-142,151)),('CLEARING FAN',(-97,-53,120)),('SCRUBBER',(107,-56,97))]:g.mark(lab,p)
 return (23,40)

def cortical_mesh():
 # A cutaway implanted capsule feeding a fine expandable neural lace.
 g.cyl('titanium implant',0,0,29,67,9,'structure',96)
 g.annulus('capsule lip',60,68,0,5,role='structure',cz=0).matrix_world=Matrix.Translation((0,0,37))@Matrix.Rotation(math.pi/2,4,'X')
 for k in range(5):g.cyl('acoustic transducer layer',0,0,40+k*2,53-k,1,'detail',72)
 g.softbox('decoder die',(0,-13,53),(34,25,6),4,'accent')
 for side in (-1,1):
  for k in range(12):g.softbox('die bond',(side*20,-25+k*2,53),(5,1,1),.4,'detail')
 # Elastic lace with individual nodes, open and legible against its curled edge.
 for col in range(13):
  x=-108+col*18;pts=[]
  for row in range(11):
   y=-92-row*17;z=24+10*math.sin(col*.38)+9*math.sin(row*.45);pts.append((x,y,z))
   g.cyl('neural recording node',x,y,z,1.6,.9,'accent',12)
  g.wire('neural lace strand',pts,.38,'cable')
 for row in range(11):
  pts=[(-108+col*18,-92-row*17,24+10*math.sin(col*.38)+9*math.sin(row*.45)) for col in range(13)]
  g.wire('lace crosslink',pts,.27,'fine')
 for x in range(-90,91,15):g.wire('fanout ribbon',[(x,-92,26),(x*.3,-67,33),(x*.2,-26,51)],.5,'cable')
 g.along_y('insertion collar',0,-66,32,5,13,'structure',40)
 g.mark('MESH THREAD',(-90,-210,26));g.mark('RECORDING SITE',(18,-160,40));g.mark('DECODER CHIP',(0,-13,57));g.mark('POWER COIL',(35,12,45));g.mark('INSERTION PORT',(0,-75,32));g.mark('SEALED CAN',(-60,0,33))
 return (18,53)

def tether_climber():
 # Streamlined elevator cargo car around a continuous central ribbon.
 g.softbox('cargo rear shell',(0,82,230),(221,32,293),15,'structure')
 for side in (-1,1):
  g.softbox('cargo side casting',(side*100,24,230),(21,129,293),10,'structure')
 for z in (89,371):
  g.softbox('cargo end casting',(0,24,z),(210,129,18),8,'structure')
 # Open front service bay reveals traction hardware, cargo stays behind it.
 for x in (-101,101):g.beam('external rail',(x,-59,72),(x,-59,390),5)
 for x in (-60,60):
  for z in (134,197,260,323):
   g.along_y('traction roller',x,-82,z,27,22,'structure',48)
   g.along_y('roller hub',x,-105,z,11,4,'accent',24)
   for a in range(0,360,60):
    t=math.radians(a);g.along_y('hub screw',x+18*math.cos(t),-106,z+18*math.sin(t),1.6,2,'detail',6)
 g.box('tether ribbon',(0,-97,245),(54,1.5,542),'accent')
 for i in range(3):
  for x in (-49,49):g.softbox('cargo cassette',(x,28,140+i*87),(83,108,76),13,'detail')
 g.ball('debris fairing',(0,25,395),(119,80,61),'structure')
 for sign in (-1,1):
  g.softbox('radiator wing',(sign*166,10,246),(92,9,203),15)
  for z in range(158,338,13):g.wire('radiator channel',[(sign*129,3,z),(sign*204,3,z)],.55,'detail')
 g.casting('laser collector',[(18,138,119),(24,148,130),(31,144,126),(44,119,99)],'structure')
 for x in range(-100,101,12):g.wire('receiver cell line',[(x,-70,45),(x,70,45)],.4,'fine')
 for x in (-80,80):g.beam('collector strut',(x,30,44),(x,30,91),6)
 for lab,p in [('RIBBON',(0,-97,470)),('DEBRIS SHIELD',(0,-34,425)),('CARGO POD',(98,15,250)),('TRACTION DRIVE',(60,-108,260)),('RADIATOR',(184,3,246)),('LASER RECEIVER',(0,-95,31)),('POWER BEAM',(0,0,18))]:g.mark(lab,p)
 return (27,16)

def fusion_transport():
 from fusion_transport import build
 return build()

def volumetric_stage():
 # A sculpted proscenium with articulated optical heads and an open luminous volume.
 g.base(258,167)
 for x in (-226,226):
  g.casting('tower footing',[(32,34,44),(38,37,47),(60,27,32),(90,20,24)],yc=67).location.x=x
  g.softbox('projector tower',(x,67,237),(35,43,314),16)
  for z in (147,224,301):
   g.softbox('optical head',(x,-1,z),(34,44,27),12)
   g.along_y('emitter lens',x,-25,z,9,4,'accent',32)
   g.beam('head arm',(x,67,z),(x,11,z),6,'detail')
 g.softbox('overhead bridge',(0,67,403),(482,48,33),16)
 for i in range(7):
  x=-180+i*60;g.ball('gimbal head',(x,51,377),(15,16,17),'structure');g.cyl('downward emitter',x,51,353,9,9,'accent',24)
 # Sparse, quiet iso-contours describe the projected light volume.
 for k in range(4):
  pts=[]
  for j in range(161):
   t=T*j/160;pts.append((116*math.sin(t),-18+61*math.sin(2*t),220+83*math.cos(t)+(k-1.5)*3.2))
  g.wire('luminous image',pts,.12,'hologram')
 g.softbox('haze console',(-171,-97,68),(72,56,57),17);g.vents(-171,-126,48,8,43)
 for x in (141,167,193):g.dial(x,-129,55,7)
 for lab,p in [('EMITTER HEAD',(-226,-25,224)),('TOWER',(226,67,285)),('BRIDGE',(60,51,377)),('IMAGE VOLUME',(0,-18,302)),('VOXEL',(115,-18,220)),('HAZE UNIT',(-171,-126,67))]:g.mark(lab,p)
 return (23,19)

def bounder():
 # Unoccupied single-leg wearable, shown with joint housings and flexible spring.
 hip=Vector((0,0,455));knee=Vector((64,-4,265));ankle=Vector((6,-8,86))
 g.softbox('waist pack',(-68,32,477),(62,37,99),19);g.vents(-68,12,444,11,39)
 g.softbox('hip belt',(0,33,471),(121,24,36),14)
 for label,p,r in [('hip drive',hip,31),('knee cam',knee,26),('ankle bearing',ankle,18)]:
  g.along_y(label,p.x,p.y,p.z,r,23,'structure',64);g.along_y(label+' cover',p.x,p.y-24,p.z,r*.69,3,'accent',48)
 for a,b in [(hip,knee),(knee,ankle)]:
  g.beam('tapered frame',a,b,9)
  for side in (-1,1):
   off=Vector((side*27,7,0));start=a.lerp(b,.19)+off;end=a.lerp(b,.81)+off
   g.beam('actuator housing',start,end,9,'structure',24)
   for j in range(5):g.wire('muscle fibre',[tuple(start+Vector((j-2,-10,0))),tuple(end+Vector((j-2,-10,0)))],.5,'accent')
   g.beam('actuator link',a,start,2,'detail');g.beam('actuator link',end,b,2,'detail')
 for t in (.32,.7):
  p=hip.lerp(knee,t);g.softbox('neural cuff',(p.x,p.y+8,p.z),(89,25,23),10)
  for x in range(-32,33,8):g.ball('cuff contact',(p.x+x,p.y-6,p.z),(1.5,1,1.5),'accent')
 # Extruded swept spring blade, with visible thickness and a formed sole.
 vs=[];n=64
 for y in (-19,5):
  for off in (0,7):
   for i in range(n+1):
    t=i/n;x=(1-t)**3*6+3*(1-t)**2*t*(-113)+3*(1-t)*t*t*(-59)+t**3*113;z=(1-t)**3*80+3*(1-t)**2*t*29+3*(1-t)*t*t*8+t**3*13
    vs.append((x,y,z+off))
 m=n+1;fs=[]
 for i in range(n):fs.extend([(i,i+1,m+i+1,m+i),(2*m+i,3*m+i,3*m+i+1,2*m+i+1),(i,2*m+i,2*m+i+1,i+1),(m+i,m+i+1,3*m+i+1,3*m+i)])
 g.mesh('carbon spring blade',vs,fs,'structure');g.softbox('replaceable sole',(87,-7,8),(63,34,9),4)
 for lab,p in [('PACK',(-68,12,476)),('HIP DRIVE',(0,-25,455)),('NERVE-SIGNAL CUFF',(21,-6,394)),('MUSCLE BUNDLE',(47,-7,348)),('KNEE CAM',(64,-29,265)),('ANKLE PIVOT',(6,-33,86)),('SPRING BLADE',(-40,-19,28)),('SOLE',(96,-24,9))]:g.mark(lab,p)
 return (23,13)

def greener():
 # Two adjacent garden plots, viewed obliquely; a cutaway exposes buried loops.
 for side in (-1,1):
  g.softbox('soil section',(side*133,0,-12),(254,235,24),8,'shell')
  for row in range(5):
   for col in range(7):
    x=side*(29+col*34);y=-99+row*46;z=1
    if any((x-gx)**2+(y-gy)**2<31**2 for gx,gy in [(-145,-71),(179,-52)]):continue
    # Three curved blades form a legible tuft; clear soil separates each clump.
    for dx,dy,h in [(-7,-1,15),(1,2,20),(8,3,13)]:
     pts=[(x+dx*t*t,y+dy*t,z+h*t) for t in [j/8 for j in range(9)]]
     g.wire('grass blade',pts,.35,'grass')
  pts=[]
  for j in range(81):
   a=T*j/80;pts.append((side*133+106*math.cos(a),91*math.sin(a),-22))
  g.wire('buried antenna loop',pts,.8,'cable')
 # Fence in depth, with successive height extensions and bolted straps.
 for y in (-107,0,107):
  g.softbox('fence post',(0,y,97),(12,12,194),3)
  for z in (135,177):
   g.softbox('extension strap',(8,y,z),(3,19,26),2,'detail')
   for zz in (z-8,z+8):g.beam('strap bolt',(7,y,zz),(12,y,zz),1.8,'detail')
 for z in (43,112,157,184):g.softbox('fence rail',(0,0,z),(9,228,10),2,'detail')
 for y in range(-100,110,20):g.softbox('fence paling',(0,y,74),(8,15,140),3,'detail')
 # Shared telescopic mast and cast optical head, opposing orientations.
 for side,h in [(-1,244),(1,262)]:
  x=side*63;y=side*37
  g.softbox('mast footing',(x,y,9),(38,38,18),8)
  for z,r,hh in [(18,8,99),(117,6.5,77),(194,5,h-194)]:
   g.cyl('telescopic mast',x,y,z,r,hh)
   g.cyl('locking collar',x,y,z,r+2,7,'detail')
  g.softbox('camera housing',(x,y,h+11),(43,28,27),9)
  # Lens points across the fence.
  g.beam('lens barrel',(x-side*21,y,h+11),(x-side*32,y,h+11),10)
  g.beam('objective',(x-side*32,y,h+11),(x-side*34,y,h+11),7,'accent')
  g.cyl('pan bearing',x,y,h-4,11,6,'detail')
  for zz in (h+5,h+10,h+15):g.wire('camera louvre',[(x-11,y+15,zz),(x+11,y+15,zz)],.4,'detail')
  for k in range(3):
   g.wire('sensing ray',[(x-side*35,y,h+11),(-side*(140+k*35),-65+k*50,3)],.15,'fine')
 g.softbox('control enclosure',(-204,58,45),(65,38,85),14)
 g.along_y('control dial',-204,36,61,17,5,'detail',48)
 g.along_y('dial centre',-204,30,61,3,3,'accent')
 g.wire('dial pointer',[(-204,29,61),(-195,29,70)],.5,'detail')
 g.vents(-204,37,16,5,36)
 g.wire('control conduit',[(-204,60,3),(-204,60,-22),(-133,80,-22)],1,'cable')
 # Molded garden figurines: cap, nose, beard, folded arms and separate boots.
 for x,y in [(-145,-71),(179,-52)]:
  g.ball('gnome coat',(x,y,29),(19,14,24),'figure')
  for dx in (-10,10):
   g.softbox('gnome boot',(x+dx,y-7,6),(17,26,12),5,'figure')
  g.ball('gnome face',(x,y-1,58),(13,12,14),'figure')
  # A tapered beard, with quiet grooves on its front surface.
  vs=[]
  for z,rx,ry,cy in [(29,2,2,y-14),(39,10,5,y-14),(52,13,7,y-11)]:
   vs.extend((x+rx*math.cos(T*j/40),cy+ry*math.sin(T*j/40),z) for j in range(40))
  fs=[(k*40+j,k*40+(j+1)%40,(k+1)*40+(j+1)%40,(k+1)*40+j) for k in range(2) for j in range(40)]
  g.mesh('gnome beard',vs,fs,'figure')
  for dx in (-6,0,6):
   g.wire('beard groove',[(x+dx,y-18,49),(x+dx*.7,y-19,41),(x+dx*.2,y-16,32)],.3,'detail')
  for dx in (-17,17):
   g.ball('gnome sleeve',(x+dx,y-2,37),(6,9,13),'figure')
   g.ball('gnome mitten',(x+dx*.8,y-10,30),(5,5,6),'figure')
  vs=[(x+16*math.cos(T*j/48),y+14*math.sin(T*j/48),64) for j in range(48)]+[(x+8,y+2,102)]
  g.mesh('gnome pointed cap',vs,[(j,(j+1)%48,48) for j in range(48)],'figure')
  g.wire('cap rolled brim',[(x+16.5*math.cos(T*j/64),y+14.5*math.sin(T*j/64),64) for j in range(65)],.7,'figure')
  g.ball('gnome nose',(x,y-14,57),(5,6,5),'figure')
  if x>0:g.along_y('concealed camera',x-6,y-12,61,3,3,'accent',24)
 for x,y,z,r in [(104,58,27,25),(127,61,44,25),(108,61,68,20),(119,63,90,16)]:
  g.ball('shrub envelope',(x,y,z),(r,r*.8,r),'shell')
 for lab,p in [('PERISCOPE CAMERA',(-40,-37,255)),("THE NEIGHBOUR'S UNIT",(42,37,273)),('FENCE',(0,-98,184)),('CONTROL BOX',(-204,28,61)),('GNOME',(-145,-71,82)),('THEIR GNOME',(173,-67,61)),('ANTENNA WIRE',(-169,-86,-22)),('SHRUB',(119,63,90))]:g.mark(lab,p)
 return (30,24)

BUILDERS={'greener':greener,'sky-racer':sky_racer,'organ-foundry':organ_foundry,'air-refinery':air_refinery,'aroma-organ':aroma_organ,'cortical-mesh':cortical_mesh,'tether-climber':tether_climber,'fusion-transport':fusion_transport,'volumetric-stage':volumetric_stage,'bounder':bounder}
if __name__=='__main__':
 for name,fn in BUILDERS.items():
  if os.environ.get('HARDWARE_ONLY') and name!=os.environ['HARDWARE_ONLY']:continue
  g.reset();az,el=fn();g.export(name,az,el)
 sys.stdout.flush();os._exit(0)
