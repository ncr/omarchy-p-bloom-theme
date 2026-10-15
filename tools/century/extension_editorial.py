"""Sixteen subject-specific figures: declared idealisations, never synthetic data."""
import math
from sheet import WHITE,ARC,GOLD
from .editorial import tx,arrow,header,axes,curve
from .editorial_second import mid,below,ticks_under,cap
from collection_layout import field_notes
from triptych import diagram_y,register_section,punchline

DATA={
101:dict(kind='release',fact='Stored bolt strain still has to go somewhere; the cam decides where.',rows=[('PRELOAD','TRANSFER BEFORE RELEASE'),('RING GAP','70°'),('SHOCK','REQUIRES MEASUREMENT')],note='THE RECORDER CAN BE RESET. THE PAYLOAD CANNOT.',left=('HAND OVER THE LOAD FIRST','RELEASE STATES / TIME NOT TO SCALE'),right=('THE RECORD IS NOT THE EVENT','RECORDER STRIP / FOUR CONTACTS')),
103:dict(kind='capillarity',fact='Coolant carries dissolved air, which comes out as bubbles wherever the loop warms up or its pressure drops.',rows=[('SURFACE','MATCHED TO COOLANT'),('GAS INVENTORY','BUFFERED BEFORE VENT'),('GRAVITY','NOT THE SEPARATOR')],note='ALL BUBBLES MUST DECLARE THEIR INTENTIONS.',left=('SMALL PORES, LARGE CONSEQUENCES','IDEAL CAPILLARY PRESSURE / FIXED WETTING'),right=('KEEP THE INTERFACE WET','MEMBRANE CROSS-SECTION / NOT TO SCALE')),
104:dict(kind='consent',fact='A witness window shows where the bolt is.',rows=[('SENIORITY','NO BYPASS'),('EMERGENCY','SEPARATE PROCEDURE')],note='THE SECOND KEY IS ON HOLIDAY UNTIL MONDAY.',left=('AUTHORITY DOES NOT ADD UP','BOOLEAN PERMISSION TABLE / NO MASTER INPUT'),right=('CONSENT HAS AN EXPIRY','SCRIPTED WITHDRAWAL / BEFORE BOLT RELEASE')),
105:dict(kind='metrology',fact='Pitch and diameter can identify a thread. Neither establishes voltage, pressure rating or polarity.',rows=[('MECHANICAL','MEASURE BEFORE MATING'),('ELECTRICAL','SEPARATE VERIFICATION'),('ADAPTOR','AFTER A FULL MATCH')],note='THE GAUGES HAVE CERTIFICATES. THE VISITORS HAVE CONFIDENCE.',left=('SAME DIAMETER, WRONG CONVERSATION','TWO THREAD PROFILES / SIDE BY SIDE'),right=('PASS IS A SMALLER SET','ACCEPTANCE REGISTER / EXAMPLE COUNTS')),
106:dict(kind='scattering',fact='Heavy elements such as lead and uranium deflect muons the most, so dense shielding stands out instead of hiding.',rows=[('SOURCE','NATURAL COSMIC MUONS'),('MEASURED','INCOMING / OUTGOING TRACK'),('DENSITY MAP','RECONSTRUCTION REQUIRED')],note='TWO TRACKERS, THREE CLOCKS, NO DOG.',left=('A BEND LEAVES A CLUE','ONE MUON THROUGH TWO TRACKER PAIRS'),right=('THE SKY SETS THE SAMPLE SIZE','POISSON COUNT UNCERTAINTY / 1 / √N')),
107:dict(kind='resonance',fact='A tuned absorber works near its chosen frequency. A changed host or load can detune it.',rows=[('TUNING','MEASURE, MOVE, LOCK'),('MODEL','f = √(k / m) / 2π'),('BANDS','THREE, ONE PER BRANCH')],note='GOOD VIBRATIONS ARE STILL VIBRATIONS.',left=('MORE MASS, LOWER NOTE','IDEAL NATURAL FREQUENCY / FIXED STIFFNESS'),right=('THE HOST AND ITS UNINVITED GUEST','TWO COUPLED OSCILLATORS / LUMPED MODEL')),
108:dict(kind='handoff',fact='A curved needle is driven by turning it along its own arc, so after each pass it has to change hands.',rows=[('SUBSTRATE','TEST MEMBRANE'),('HOLD','AT LEAST ONE GRIPPER'),('THREAD','SPOOL, DANCER, NEEDLE')],note='KNOTS SHOULD BE IN THE THREAD, NOT THE PLAN.',left=('DO NOT DROP THE NEEDLE','GRIPPER STATES / ONE HANDOFF'),right=('SLACK NEEDS SOMEWHERE TO GO','DANCER GEOMETRY / THREAD RESERVE')),
110:dict(kind='rotation',fact='When the bowl stops, the soup floats again.',rows=[('MODEL','a = ω²r'),('LID','OPEN ONLY WHEN STOPPED'),('HUMANS','NOT AN INGREDIENT')],note='SPIN THE BOWL BY HAND AND THE COOK SPINS THE OTHER WAY.',left=('DOUBLE THE SPEED, FOUR TIMES THE MESS','IDEAL RADIAL ACCELERATION / FIXED RADIUS'),right=('BALANCE IS PART OF THE RECIPE','STATIC FIRST-MOMENT BALANCE / IDEAL PAIR')),
}

def capsule(s,x,y,w,h,r=7,color=WHITE,a=.7):
 pts=[]
 for cx,cy,a0 in ((x+w-r,y+r,-90),(x+w-r,y+h-r,0),(x+r,y+h-r,90),(x+r,y+r,180)):
  pts.extend((cx+r*math.cos(math.radians(a0+j*90/8)),cy+r*math.sin(math.radians(a0+j*90/8))) for j in range(9))
 s.poly(pts,a,.65,close=True,color=color)

def waveform(s,x,y,w,h,fn,xlabel,top='1',ticks=()):
 axes(s,x+25,y,w-35,h,'',top)
 curve(s,[(x+25+(w-35)*i/120,y+h*(1-fn(i/120))) for i in range(121)],ARC)
 ticks_under(s,x+25,y+h,w-35,ticks,xlabel)

def trace_rows(s,x,y,labels,states,w=440):
 """Three discrete contact records with explicit disjoint row captions.

 Each caption is centred on its trace (between its low and high level).
 Returns the x of a state column's left edge.
 """
 left=x+128;step=(w-128)/len(states[0])
 for r,(label,row) in enumerate(zip(labels,states)):
  yy=y+13+r*31;mid(s,label,x,yy-5,7)
  s.ln(left,yy+9,x+w,yy+9,.18,.4)
  pts=[]
  for j,on in enumerate(row):
   if j:pts.append((left+j*step,yy-(10 if row[j-1] else 0)))
   pts.extend([(left+j*step,yy-(10 if on else 0)),(left+(j+1)*step,yy-(10 if on else 0))])
  curve(s,pts,ARC if r!=2 else GOLD)
 return lambda a,b=None:left+(a+(a if b is None else b)+1)/2*step


def figure(s,n,side,x,y,w):
 d=DATA[n];title,scope=d[side];header(s,dict(title=title,scope=scope),x,y,w)
 body=y+39;foot=''
 if side=='left':
  if n==101:
   col=trace_rows(s,x,body,('PRIMARY HOLD','TRANSFER CAM','JAW OPEN'),((1,1,0,0,0),(0,1,1,1,0),(0,0,0,1,1)))
   # Each phase is named under the states it spans.
   for label,a,b in (('HOLD',0,0),('HANDOFF',1,1),('RELEASE',3,4)):tx(s,label,col(a,b),body+113,align='c')
   foot='The cam takes the load before the jaw opens.'
  elif n==103:
   waveform(s,x,body,w,91,lambda t:1/(1+3*t),'PORE RADIUS / r₀','1',((0,'1'),(1/3,'2'),(1,'4')))
   foot='Pressure ratio = r₀ / r; surface tension and angle fixed.'
  elif n==104:
   # Inputs centred under their headings; the result column hangs from its heading.
   heads=(('KEY ONE',x),('KEY TWO',x+150),('PERMISSION',x+300))
   for label,hx in heads:tx(s,label,hx,body)
   c1,c2=(hx+s.measure(label,7,.08)/2 for label,hx in heads[:2]);px=heads[2][1]
   for i,(a,b) in enumerate(((0,0),(0,1),(1,0),(1,1))):
    yy=body+23+i*23
    # Tabular digits: centred on their advance, so 0 and 1 share one axis.
    base=yy+cap(s,7)/2;tx(s,str(a),c1,base,align='c');tx(s,str(b),c2,base,align='c')
    s.circ(px+3,yy,3,.8,.7,color=ARC if a*b else WHITE)
    mid(s,'RELEASE' if a*b else 'HOLD',px+14,yy,color=ARC if a*b else WHITE)
   foot='Equal inputs. Neither key can impersonate the other.'
  elif n==105:
   for j,pitch in enumerate((24,38)):
    yy=body+22+j*55;capsule(s,x+24,yy-15,310,31,7)
    # Rounded thread crests; straight flanks are physical geometry.
    pts=[]
    for k in range(113):
     xx=x+32+k*2.6;v=(xx-x-32)/pitch
     zz=7*math.cos(math.tau*v)
     pts.append((xx,yy+zz))
    curve(s,pts,WHITE);mid(s,'PITCH '+('p' if j==0 else '1.6p'),x+351,yy+.5)
   foot='Nominal diameter agrees; axial engagement does not.'
  elif n==106:
   for yy in (body+6,body+24,body+92,body+110):capsule(s,x+47,yy,280,5,2,a=.5)
   capsule(s,x+144,body+40,88,40,9,a=.35)
   # One muon: in straight, bent at the cargo, out on the bent line; the dashed line is where it would have gone.
   s.ln(x+189,body+59,x+232,body+125,.38,.6,dash=[3,4])
   s.poly([(x+146,body-2),(x+189,body+59),(x+165,body+125)],.85,.9,close=False,color=ARC)
   tx(s,'MEASURED',x+157,body+128,6,.7,align='r');tx(s,'STRAIGHT ON',x+240,body+128,6,.5)
   # Each label centred on what it names: a detector pair, the cargo.
   mid(s,'IN',x+344,body+17.5);mid(s,'CARGO',x+344,body+60);mid(s,'OUT',x+344,body+103.5)
   foot='Where the two tracks meet marks the scattering point.'
  elif n==107:
   waveform(s,x,body,w,91,lambda t:1/math.sqrt(1+3*t),'MOVING MASS / m₀','1',((0,'1'),(1/3,'2'),(1,'4')))
   foot='Frequency ratio = √(m₀ / m); one ideal branch.'
  elif n==108:
   col=trace_rows(s,x,body,('LEFT GRIP','RIGHT GRIP','NEEDLE HELD'),((1,1,0,0,1),(0,1,1,1,1),(1,1,1,1,1)))
   for label,a,b in (('HOLD',0,0),('OVERLAP',1,1),('TRANSFER',2,3)):tx(s,label,col(a,b),body+113,align='c')
   foot='Both grippers hold at once before either lets go.'
  elif n==110:
   waveform(s,x,body,w,91,lambda t:t*t,'ANGULAR SPEED / ω₀','4',((0,'0'),(.5,'1'),(1,'2')))
   foot='a / a₀ = (ω / ω₀)² at the same radius.'
 else:
  if n==101:
   for i,(label,start,end) in enumerate((('ARM',0,3),('CAM',1,4),('JAW',3,5),('CLEAR',4,5))):
    yy=body+8+i*27;mid(s,label,x,yy-1);step=(w-95)/5
    for j in range(6):s.ln(x+95+j*step,yy-10,x+95+j*step,yy+9,.16,.5)
    capsule(s,x+95+start*step,yy-5,(end-start)*step,8,3,ARC)
   foot='Each contact overlaps the next, so the load is never dropped.'
  elif n==103:
   capsule(s,x+30,body+28,320,62,15)
   for xx in range(70,320,25):
    s.ln(x+xx,body+31,x+xx,body+88,.35,.7)
    s.circ(x+xx-7,body+59,2,.7,.6,color=ARC)
   for xx,r in ((80,10),(155,13),(245,9)):s.circ(x+xx,body+12,r,.72,.7,color=GOLD)
   arrow(s,(x+10,body+114),(x+345,body+114),ARC)
   mid(s,'GAS',x+370,body+12);mid(s,'WET PORE',x+370,body+59);mid(s,'LIQUID',x+370,body+114)
   foot='Gas is excluded below bubble point; fouling changes behaviour.'
  elif n==104:
   col=trace_rows(s,x,body,('KEY ONE','KEY TWO','PERMISSION'),((1,1,1,1,1),(0,1,1,0,0),(0,1,1,0,0)))
   # Centred under the falling edge it names.
   tx(s,'SECOND KEY WITHDRAWN',col(3)-(col(4)-col(3))/2,body+113,align='c')
   foot='Pre-release permission falls when either input is removed.'
  elif n==105:
   for i,(label,count) in enumerate((('ARRIVED',12),('THREAD FIT',8),('FULL MATCH',3))):
    yy=body+13+i*38;mid(s,label,x,yy)
    for j in range(12):
     xx=x+145+j*22;capsule(s,xx,yy-8,12,16,4,ARC if j<count else WHITE,.8 if j<count else .18)
   foot='Five fit the thread and still fail the full match.'
  elif n==106:
   waveform(s,x,body,w,91,lambda t:1/math.sqrt(1+99*t),'DETECTED COUNT / N','1',((0,'1'),(.24,'25'),(1,'100')))
   foot='A hundred muons give a tenth of the noise of one.'
  elif n==107:
   s.ln(x+30,body+100,x+390,body+100,.5,.6)
   capsule(s,x+87,body+29,130,58,12)
   capsule(s,x+292,body+43,61,30,8,color=ARC)
   for start,end,yy in ((x+28,x+87,body+58),(x+217,x+292,body+58)):
    pts=[(start,yy)]+[(start+(end-start)*i/80,yy+6*math.sin(i*math.tau/16)) for i in range(81)]
    curve(s,pts,WHITE)
   # Names on one baseline above the bodies; each body carries its own mass and stiffness.
   tx(s,'HOST MASS',x+152,body+19,align='c');tx(s,'ABSORBER',x+322.5,body+19,align='c')
   mid(s,'M, K',x+152,body+58,align='c');mid(s,'m, k',x+322.5,body+58,align='c')
   foot='Tuned right, the absorber moves so the host does not have to.'
  elif n==108:
   b=body+8  # clear of the scope line, like the other figures
   for xx in (80,340):s.circ(x+xx,b+15,12,.7,.7)
   s.circ(x+210,b+83,15,.75,.7,color=ARC)
   s.poly([(x+68,b+15),(x+197,b+83),(x+223,b+83),(x+352,b+15)],.7,.7,close=False,color=GOLD)
   arrow(s,(x+210,b+35),(x+210,b+61),ARC)
   tx(s,'SUPPLY',x+80,b-5,align='c');tx(s,'NEEDLE',x+340,b-5,align='c')
   tx(s,'MOVING DANCER / TWO THREAD LEGS',x+210,body+122,align='c')
   foot='For parallel legs, reserve change is twice dancer travel.'
  elif n==110:
   # The heavier mass sits nearer the pivot: r₁ / r₂ = m₂ / m₁ (block areas 43 × 42 and 29 × 28).
   s.ln(x+136,body+70,x+384,body+70,.65,1)
   s.circ(x+224,body+70,10,.8,.8)
   capsule(s,x+144.5,body+49,43,42,8,color=GOLD)
   capsule(s,x+338,body+56,29,28,6,color=ARC)
   arrow(s,(x+215,body+100),(x+168,body+100));arrow(s,(x+233,body+100),(x+351,body+100))
   # Paired labels share a baseline; each radius is named under its own arrow.
   tx(s,'m₁',x+166,body+40,align='c');tx(s,'m₂',x+352.5,body+40,align='c')
   tx(s,'r₁',x+191.5,body+116,align='c');tx(s,'r₂',x+292,body+116,align='c')
   foot='m₁ × r₁ = m₂ × r₂; real rotor also needs dynamic balance.'
 tx(s,foot,x,y+184,7,.67)


def draw(s,entry):
 n=entry['number'];d=DATA.get(n)
 if not d:return
 with s.layer('section'):
  for side,x in (('left',140),('right',s.W-650)):
   y=diagram_y(s,side,187);figure(s,n,side,x,y,440);register_section(s,side,y-16,y+187)
  s.diagram_slots={'left','right'}
  field_notes(s,d);punchline(s,d['note'])
