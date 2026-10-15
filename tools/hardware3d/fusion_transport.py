"""FT-2: a crew wheel, long open spine and serviceable magnetic-drive assembly."""
import math
import family_core as g
from mathutils import Matrix
T=math.tau
Z=180

def ring(name,x,inner,outer,depth,role='structure',a0=0,a1=360):
 if inner==0 and a1-a0==360:return axial(name,x,depth,outer,role)
 o=g.annulus(name,inner,outer,-depth/2,depth/2,a0,a1,role,cz=0)
 o.matrix_world=Matrix.Translation((x,0,Z))@Matrix.Rotation(math.pi/2,4,'Z')
 return o

def axial(name,x,length,r,role='structure',y=0,z=Z):
 return g.beam(name,(x-length/2,y,z),(x+length/2,y,z),r,role,48)

def build():
 # Layered whipple shield, behind which the pressure module remains visible.
 for x,r in [(-361,71),(-353,73),(-345,68)]:ring('forward dust shield',x,0,r,2,'structure' if x==-361 else 'detail')
 g.ball('command pressure vessel',(-296,0,Z),(49,32,32),'structure')
 for x,r in [(-331,20),(-317,29),(-280,29),(-259,20)]:ring('pressure hull seam',x,r-1,r,1,'detail')
 for sign in (-1,1):
  g.softbox('forward sensor recess',(-316,sign*25,Z+16),(15,4,9),2,'accent')
 axial('forward docking collar',-270,24,18)
 # Rotation joint and an inhabited wheel, assembled from six pressure pods.
 ring('wheel bearing',-236,18,32,27)
 ring('crew wheel inner band',-236,85,92,22)
 ring('crew wheel outer band',-236,110,116,25)
 for k in range(6):
  a=T*k/6+.25;y,z=100*math.cos(a),Z+100*math.sin(a)
  g.beam('tapered spoke',(-236,27*math.cos(a),Z+27*math.sin(a)),(-236,87*math.cos(a),Z+87*math.sin(a)),4)
  # Pressure cabins and stepped external protection share one casting.
  g.ball('crew pressure cabin',(-236,y,z),(21,20,22))
  g.beam('radial hatch',(-236,y,z),(-236,119*math.cos(a),Z+119*math.sin(a)),7,'detail')
  for off in (-7,7):
   g.ball('cabin observation port',(-254,y+off*math.sin(a),z-off*math.cos(a)),(1.5,3,4),'accent')
  ring('wheel segment seam',-249,91,109,1,'detail',math.degrees(a)-17,math.degrees(a)+17)
 # Four-chord lattice spine gives scale and separates crew from hot machinery.
 for y,z in [(-15,Z-15),(15,Z-15),(15,Z+15),(-15,Z+15)]:
  g.beam('primary spine chord',(-204,y,z),(139,y,z),2.8)
 for x in range(-196,140,32):
  for y0,z0,y1,z1 in [(-15,Z-15,15,Z-15),(15,Z-15,15,Z+15),(15,Z+15,-15,Z+15),(-15,Z+15,-15,Z-15)]:
   g.beam('cross frame',(x,y0,z0),(x,y1,z1),1.6,'detail')
   g.beam('diagonal web',(x,y0,z0),(x+32,y1,z1),1.2,'detail')
 # Four slimmer propellant tanks, with supports and exposed feed valves.
 for k in range(4):
  a=T*k/4+math.pi/4;y,z=54*math.cos(a),Z+54*math.sin(a)
  g.ball('propellant vessel',(-131,y,z),(61,22,22))
  for x in (-168,-102):
   g.beam('tank mounting strut',(x,15*math.cos(a),Z+15*math.sin(a)),(x,y,z),3,'detail')
   # Encircling tank straps face the ship axis.
   o=ring('tank retaining strap',x,21,23,4,'detail');o.location.y+=y;o.location.z+=z-Z
  axial('tank service neck',-67,15,5,'detail',y,z)
  g.wire('propellant feed',[(-60,y,z),(-41,y,z),(-25,y*.35,Z+(z-Z)*.35),(168,y*.35,Z+(z-Z)*.35)],1.25,'cable')
 # Swept droplet radiator collectors form two unmistakable long wings.
 for sign in (-1,1):
  g.beam('radiator deployment boom',(-35,sign*17,Z),(2,sign*174,Z+11),4)
  g.beam('radiator emitter',(-35,sign*78,Z+7),(38,sign*221,Z+13),4,'structure')
  g.beam('radiator collector',(149,sign*60,Z-7),(201,sign*183,Z-2),6,'structure')
  g.beam('collector return boom',(150,0,Z),(201,sign*183,Z-2),3,'detail')
  for j in range(22):
   t=j/21;a=(-35+73*t,sign*(78+143*t),Z+7+6*t);b=(149+52*t,sign*(60+123*t),Z-7+5*t)
   pts=[]
   for q in range(29):
    u=q/28;pts.append((a[0]*(1-u)+b[0]*u,a[1]*(1-u)+b[1]*u,a[2]*(1-u)+b[2]*u+6*math.sin(math.pi*u)))
   g.wire('liquid tin stream',pts,.20,'radiator' if j%4 else 'cable')
  for t in (.15,.45,.75):
   y=sign*(78+143*t);x=-35+73*t
   g.ball('emitter metering block',(x,y,Z+10),(7,5,5),'detail')
 # A stepped radiation shield and narrow reactor neck.
 ring('shadow shield core',151,0,65,11)
 ring('shadow shield outer bevel',145,58,71,6)
 ring('shadow shield rear lip',159,47,61,4,'detail')
 axial('reactor feed neck',180,32,21)
 for a in [T*k/6 for k in range(6)]:
  g.beam('reactor cradle',(169,24*math.cos(a),Z+24*math.sin(a)),(320,44*math.cos(a),Z+44*math.sin(a)),3)
 # Partly open reactor enclosure: copper-like winding layers and service collars.
 axial('fusion vessel',235,80,26,'detail')
 for x,r in [(204,37),(222,42),(241,44),(261,42),(280,37)]:
  ring('superconducting field coil',x,r-6,r,9)
  for dx in (-2,0,2):ring('coil winding seam',x+dx,r-1,r+.2,.6,'detail')
 for k in range(4):
  a=T*k/4+.5;y,z=49*math.cos(a),Z+49*math.sin(a)
  g.softbox('reactor service pod',(235,y,z),(63,15,16),5,'detail')
 # Trumpet-like open magnetic nozzle, supported by swept vanes.
 for x,r in [(303,30),(321,37),(348,53),(378,75)]:
  ring('magnetic nozzle coil',x,r-5,r,7,'structure')
 for k in range(8):
  a=T*k/8
  pts=[(303,30*math.cos(a),Z+30*math.sin(a)),(329,40*math.cos(a),Z+40*math.sin(a)),(354,56*math.cos(a),Z+56*math.sin(a)),(378,75*math.cos(a),Z+75*math.sin(a))]
  g.wire('nozzle support vane',pts,1.4,'detail')
 # Annular service flanges, valves and a subtle central exhaust datum.
 ring('nozzle throat flange',296,22,35,5,'detail')
 for k in range(12):
  a=T*k/12;axial('flange stud',294,7,1.5,'detail',31*math.cos(a),Z+31*math.sin(a))
 g.wire('exhaust axis',[(303,0,Z),(405,0,Z)],.24,'fine')
 for lab,p in [('CREW RING',(-248,-100,Z+20)),('DUST SHIELD',(-361,-55,Z)),('PROPELLANT TANKS',(-125,-38,Z+38)),('DROPLET RADIATOR',(5,-154,Z+10)),('DROPLET COLLECTOR',(179,-134,Z-4)),('SHADOW SHIELD',(145,-58,Z+20)),('FUSION CORE',(241,-44,Z+5)),('MAGNETIC NOZZLE',(378,-62,Z+25))]:g.mark(lab,p)
 return (-32,29)
