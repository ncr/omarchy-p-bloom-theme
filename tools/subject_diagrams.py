"""Individually composed explanatory figures; no universal input/output stencil.

Every registered figure owns its geometry. Shared helpers only draw strokes,
arrowheads and type. Examples and cutaways are expressly illustrative.
"""
import math
from sheet import WHITE, ARC, GOLD

FIGURES={}
# Scope of the retro-future pass. The remaining nine figures intentionally keep
# exact event grids, optical rays, section planes and existing curved geometry.
RETRO_REFINED={
    'fusion-transport':'Radiused radiator cassettes, folded rims and a bent thermal circuit.',
    'greener':'Soft lawn boundaries and curved grass strokes.',
    'cortical-mesh':'Rounded sample-record cells; signal traces and sample positions retained.',
    'bounder':'Spring blade in three states, drawn with its thickness and ankle socket.',
    'aroma-organ':'Capped dosing cartridges and swept capillary bends.',
    'tether-climber':'A rounded emitter housing; beam geometry retained.',
    'organ-foundry':'Radiused tissue section and gently branching perfusion channels.',
    'proxy':'Cue band on the tether wrist: double-rimmed case, control crown and ribbed straps.',
    'presence-rig':'Curved contact soles; force vectors and contact grid retained.',
    'tidal-loom':'Swept rotor blades, mounting feet and a thin shroud rim.',
    'manta-foil':'Continuous foil contour and smooth flow lines around a separate trim flap.',
    'sock-oracle':'Curved heels and toes on all three textile specimens.',
    'lunar-porch':'Radiused docking castings and a bezel around the leak-test gauge.',
    'fibre-braid':'Rounded carriers on the existing counter-rotating paths.',
    'advice-filter':'Double-rimmed grille, curved shutter ends and a rounded lever grip.',
    'petal-eye':'Radiused segment edges and helical actuator springs.',
    'quiet-stair':'Shaped latch castings, replaceable bearing insert, pinned rocker and swept release cable.',
    'wind-kite':'Smooth wing sections with bridle attachments following wing attitude.',
    'coral-cradle':'Organic fragment contour and radiused support clips.',
    'dune-skimmer':'Rounded tread contact footprints; tread pattern retained.',
    'meeting-buoy':'Swept follower rod and a helical spring; cam drop retained.',
    'seam-surgeon':'Radiused coupon ends, deposited bead and contact inspection shoe; V-root and rays retained.',
    'queue-garden':'Curved pawl and leaf with a helical return spring; ratchet teeth retained.',
    'compliment-mill':'Radiused mounting plate and corner fasteners; receipt edge retained.',
    'sleep-cocoon':'Soft pad contours, swept support rail and manual-release cable.',
    'plant-alibi':'Double-walled basin, drainage media, branching roots and serviceable flow-meter bezel.',
}
def figure(key,title,scope,foot):
    def register(fn):
        FIGURES[key]=(fn,title,scope,foot)
        return fn
    return register

class Pen:
    def __init__(self,s):self.s=s
    def l(self,x,y,u,v,a=.65,w=.65,col=WHITE,dash=None):self.s.ln(x,y,u,v,a,w,color=col,dash=dash)
    def p(self,pts,a=.7,w=.7,col=WHITE,close=False):self.s.poly(pts,a,w,color=col,close=close)
    def r(self,pts,a=.7,w=.7,col=WHITE,close=False,r=6):
        """Explicit tangent bends for castings and tubes, never data or rays.

        Radius is a trim distance, clipped to each adjacent segment. Sampling
        the quadratic corners through poly keeps the ordinary geometry audit.
        Endpoints and straight mating faces remain in their authored positions.
        """
        pts=list(pts)
        if close and pts[-1]==pts[0]:pts.pop()
        out=[]
        for i,b in enumerate(pts):
            if not close and i in (0,len(pts)-1):out.append(b);continue
            a0=pts[(i-1)%len(pts)];c=pts[(i+1)%len(pts)]
            d0=math.dist(a0,b);d1=math.dist(b,c)
            if min(d0,d1)<1e-8:out.append(b);continue
            trim=min(r[i] if isinstance(r,(tuple,list)) else r,d0*.45,d1*.45)
            u=tuple(b[j]+(a0[j]-b[j])*trim/d0 for j in (0,1))
            v=tuple(b[j]+(c[j]-b[j])*trim/d1 for j in (0,1))
            out.append(u)
            for k in range(1,13):
                t=k/12
                out.append(tuple((1-t)**2*u[j]+2*(1-t)*t*b[j]+t*t*v[j] for j in (0,1)))
        self.p(out,a,w,col,close)
    def screw(self,x,y,r=2):
        self.c(x,y,r,.4,.45);self.l(x-r*.55,y+r*.55,x+r*.55,y-r*.55,.4,.45)
    def c(self,x,y,r,a=.65,w=.65,col=WHITE):self.s.circ(x,y,r,a,w,color=col)
    def e(self,x,y,rx,ry,a=.6,col=WHITE):self.s.ellipse(x,y,rx,ry,a=a,w=.65,color=col)
    def t(self,text,x,y,size=6,a=.68,align='l',col=WHITE):self.s.text(text,x,y,size,track=.065,a=a,align=align,color=col)
    def a(self,x,y,u,v,col=ARC):
        self.l(x,y,u,v,.65,.65,col)
        ang=math.atan2(v-y,u-x)
        self.p([(u-4*math.cos(ang-.45),v-4*math.sin(ang-.45)),(u,v),(u-4*math.cos(ang+.45),v-4*math.sin(ang+.45))],col=col)
    def ticks(self,x,y,n,dx):
        for i in range(n):self.l(x+i*dx,y-3,x+i*dx,y+3,.35,.45)
    def coil(self,x,y,w,h,n=7):
        # Projected helical wire with return arcs, not the resistor zigzag.
        lead=min(7,w*.16);span=w-2*lead;pitch=span/n
        pts=[(x+lead+span*t+pitch*.65*math.sin(t*n*math.tau),
              y-h*.5*math.cos(t*n*math.tau)) for t in [i/(n*32) for i in range(n*32+1)]]
        self.r([(x,y),(x+lead*.4,y),pts[0]],r=2)
        self.p(pts)
        self.r([pts[-1],(x+w-lead*.4,y),(x+w,y)],r=2)

@figure('quantum-simulator','ERRORS LEAVE A TRAIL','SYNDROME HISTORY / FIVE CHECKS, EIGHT ROUNDS','Each error lights two detection events; the decoder pairs them up.')
def quantum(p):
    for i in range(5):
        y=57+i*20;p.l(25,y,340,y,.22,.4);p.t('s'+'₀₁₂₃₄'[i],4,y+2,5.5)
    for j in range(8):
        x=40+j*41;p.l(x,49,x,143,.15,.4)
        for i in range(5):p.c(x,57+i*20,1.3,.35,.4)
    for x,y in [(81,77),(163,97),(245,117),(327,77)]:p.c(x,y,4,.9,.9,ARC)
    p.p([(81,77),(122,77),(122,97),(163,97)],col=ARC)
    p.p([(245,117),(286,117),(286,77),(327,77)],col=GOLD)
    p.a(40,152,328,152);p.t('SUCCESSIVE CHECK ROUNDS',184,166,5.5,align='c')

@figure('sky-racer','BANKING SPENDS LIFT','THRUST DIRECTION / THREE ATTITUDES','Banked 25°, the fans keep 91 % of their thrust for lift.')
def sky(p):
    for n,(a,label) in enumerate([(0,'HOLD'),(-25,'BANK'),(12,'RECOVER')]):
        x=65+n*155;y=112;ang=math.radians(a)
        p.l(x,52,x,143,.24,.5,dash=[2,3]);p.l(x-44,y+30,x+44,y+30,.25,.5)
        for off in (-30,30):
            xx=x+off*math.cos(ang);yy=y+off*math.sin(ang)
            p.p([(xx-17*math.cos(ang),yy-17*math.sin(ang)),(xx+17*math.cos(ang),yy+17*math.sin(ang))],w=1.3)
            p.e(xx,yy,14,4,.35)
        p.l(x-30*math.cos(ang),y-30*math.sin(ang),x+30*math.cos(ang),y+30*math.sin(ang))
        p.a(x,y,x+53*math.sin(ang),y-53*math.cos(ang))
        p.c(x,y,4);p.t(label,x,166,6,align='c')

@figure('fusion-transport','THE OTHER EXHAUST','RADIATOR CIRCUIT / ONE LOOP, FOUR BANKS','Heat leaves through radiator area as well as the magnetic nozzle.')
def fusion(p):
    p.r([(24,115),(24,65),(90,65),(90,115),(24,115)],close=True)
    for x in range(35,86,10):p.l(x,70,x,109,.4)
    p.r([(18,74),(18,58),(96,58),(96,74)],.35,.5,r=7)
    p.r([(18,106),(18,123),(96,123),(96,106)],.35,.5,r=7)
    # One closed circuit: out along the top of the banks, back along the bottom into the hot loop.
    p.t('HOT LOOP',55,153,6,align='c');p.a(90,76,135,76)
    p.r([(135,76),(150,76),(150,61),(386,61),(386,134),(150,134),(150,111),(135,111)],col=ARC)
    for n in range(4):
        x=170+n*55;p.r([(x,72),(x+36,72),(x+36,120),(x,120)],close=True)
        for dy in range(79,118,8):p.l(x+3,dy,x+33,dy,.28,.5)
        for xx in (x+5,x+31):p.screw(xx,76,1.25);p.screw(xx,116,1.25)
        p.a(x+18,66,x+18,42,GOLD)
    p.a(135,111,92,111);p.t('RADIATION TO SPACE',275,153,6,align='c')

@figure('greener','THE PROPERTY LINE IS THE SENSOR','TWO GARDENS / FICTIONAL COMPARISON PATCHES','The neighbour can move the target without entering your garden.')
def greener(p):
    p.r([(24,69),(177,49),(198,135),(47,153)],close=True)
    p.r([(239,48),(399,70),(377,153),(221,131)],close=True)
    for i in range(10):
        x=191+i*2;p.l(x,46+i*10,x+20,51+i*10,.7,.7)
    for row in range(4):
        for col in range(7):
            x=52+col*18+row*4;y=80+row*15
            p.r([(x-3,y),(x,y-6),(x+2,y+1)],.45,.5)
            x+=202;p.r([(x-3,y),(x,y-10),(x+3,y+1)],.6,.6,col=ARC)
    p.c(117,102,13);p.c(117,102,5);p.a(133,99,257,95)
    p.t('OWN LAWN',96,171,6,align='c');p.t('INCONVENIENT NEIGHBOUR',324,171,6,align='c')

@figure('cortical-mesh','SAMPLES FIRST, SENTENCES LATER','CHANNEL SAMPLING / THREE CHANNELS, FIVE SAMPLES','The decoder chip reads speech and movement from the whole record.')
def cortical(p):
    for row in range(3):
        y=61+row*31;p.t('CH '+str(row+1),0,y+3,5.5)
        pts=[(49+i*2.1,y+8*math.sin(i*.14+row)*math.exp(-((i-45)/37)**2)) for i in range(96)]
        p.p(pts,.65,.65)
        for i in (12,32,52,72,92):
            x,yv=pts[i];p.c(x,yv,2.4,.8,.6,ARC)
    p.a(265,94,300,94)
    for row in range(3):
        for j in range(6):
            x=321+j*17;y=52+row*30;p.r([(x,y),(x+11,y),(x+11,y+16),(x,y+16)],.45,.5,close=True)
            p.l(x+3,y+4,x+8,y+12,.7,.7,col=ARC if (j+row)%3 else WHITE)
    p.t('TIME-SLICED RECORD',366,150,5.8,align='c')

@figure('bounder','LOAD BEFORE LAUNCH','SPRING BLADE / THREE MOMENTS OF ONE STEP','Landing bends the blade; push-off straightens it and lifts the runner.')
def bounder(p):
    # The B-4 spring blade (view A): a C-curve from the ankle socket down to a
    # forward toe. Landing presses the socket down and tightens the curve;
    # push-off rolls the blade onto its toe as it springs back.
    def blade(x,top,bend,roll):
        ground=140;toe=(x+44,ground)
        def bez(a,b,c,d,n=24):
            return [tuple((1-t)**3*a[j]+3*(1-t)**2*t*b[j]+3*(1-t)*t*t*c[j]+t**3*d[j] for j in (0,1)) for t in [i/n for i in range(n+1)]]
        spine=bez((x,top+18),(x-bend,top+32),(x-bend-4,ground),(x+6,ground))+[(x+30,ground),toe]
        def turn(q):  # roll about the toe tip
            c,s_=math.cos(roll),math.sin(roll);dx,dy=q[0]-toe[0],q[1]-toe[1]
            return (toe[0]+dx*c-dy*s_,toe[1]+dx*s_+dy*c)
        spine=[turn(q) for q in spine]
        # Blade thickness: a second edge offset along the normal, closed at both ends.
        inner=[]
        for i,q in enumerate(spine):
            a_,b_=spine[max(0,i-1)],spine[min(len(spine)-1,i+1)]
            dx,dy=b_[0]-a_[0],b_[1]-a_[1];n=math.hypot(dx,dy) or 1
            inner.append((q[0]-dy/n*3.2,q[1]+dx/n*3.2))
        p.p(spine+inner[::-1],.85,.8,close=True)
        sx,sy=turn((x,top+14))
        p.r([(sx-8,sy),(sx-8,sy-16),(sx+8,sy-16),(sx+8,sy)],.75,.75,close=True,r=3)
        p.l(sx,sy,*turn((x,top+18)),.75,.75)
        p.l(sx,sy-16,sx,sy-26,.6,.9)
        return sx,sy-26
    for i,(label,top,bend,roll) in enumerate([('UNLOADED',58,36,0),('LANDING',76,44,0),('PUSH-OFF',62,38,.16)]):
        x=58+i*142
        p.l(x-40,140,x+70,140,.36,.5)
        tx,ty=blade(x,top,bend,roll)
        p.t(label,x+10,166,5.8,align='c')
        if i==1:p.a(tx+20,ty-18,tx+20,ty-2)
        if i==2:p.a(tx+20,ty-2,tx+20,ty-18)
    # The unloaded socket height carried across, so the drop on landing reads.
    p.l(22,46,410,46,.22,.45,dash=[2,3])

@figure('air-refinery','CARBON HAS TO COME FROM SOMEWHERE','ATOM INVENTORY / CO₂ IN, CARBON CHAIN OUT','The air supplies the carbon; sunlight supplies the energy to link it.')
def air(p):
    for y in (71,119):
        p.c(36,y,8);p.c(66,y,7,.85,.7,ARC);p.c(96,y,8);p.l(44,y-2,59,y-2);p.l(44,y+2,59,y+2);p.l(73,y-2,88,y-2);p.l(73,y+2,88,y+2)
    p.t('CAPTURED CO₂',66,157,6,align='c')
    p.a(140,95,238,95);p.p([(165,57),(186,57),(177,70),(199,70),(181,87)],col=GOLD)
    p.t('ENERGY',210,52,5.5)
    chain=[(268+i*32,93+(-10 if i%2 else 10)) for i in range(5)]
    for a,b in zip(chain,chain[1:]):p.l(*a,*b,.7,.9)
    for x,y in chain:
        p.c(x,y,5,.8,.7,ARC)
        for dy in (-18,18):p.l(x,y+(6 if dy>0 else -6),x,y+dy,.45,.6);p.c(x,y+dy*1.3,2,.5,.5)
    p.t('CARBON BACKBONE',331,157,6,align='c')

@figure('aroma-organ','THE MIX HAS A MEMORY','CAPILLARY MANIFOLD / FIVE DOSES AND A PURGE','A previous recipe must leave before the next one arrives.')
def aroma(p):
    for i in range(5):
        x=28+i*57;p.r([(x,48),(x+18,48),(x+18,72),(x,72)],close=True)
        p.l(x+9,72,x+9,89);p.p([(x+2,89),(x+16,97),(x+2,105),(x+2,89)],.6,.55)
        p.l(x+9,105,x+9,122);p.c(x+9,57,2,.45,.5)
        p.l(x+3,51,x+15,51,.4,.55);p.l(x+4,68,x+14,68,.4,.55)
    p.r([(24,122),(284,122),(319,100),(346,100)],col=ARC)
    p.r([(24,132),(287,132),(322,111),(346,111)])
    for i in range(6):p.l(354+i*10,96-i*2,354+i*10,115+i*2,.45,.5,col=ARC)
    p.r([(214,132),(214,151),(296,151)],col=GOLD);p.a(296,151,335,151,GOLD)
    p.t('CARRIER + METERED DOSES',24,147+p.s.type_growth(5.8),5.8);p.t('PURGE',362,155,5.8)

@figure('tether-climber','POWER HAS A FOOTPRINT','BEAM, RECEIVER AND RIBBON','The receiver turns the beam into power; the rollers turn power into climb.')
def tether(p):
    p.r([(23,132),(53,132),(45,115),(32,115)],close=True)
    p.p([(37,115),(163,55),(265,55),(42,115)],.45,.55,col=ARC)
    p.l(168,55,263,55,.8,1.4)
    for i in range(9):p.l(175+i*10,49,175+i*10,62,.5,.55)
    for x in (297,306):p.l(x,43,x,148,.65,1)
    for y in (74,119):
        p.c(285,y,12);p.c(318,y,12);p.l(263,y,273,y,.6,.8)
    p.a(350,136,350,59);p.t('UP',369,93,6)
    p.t('BEAM',118,107);p.t('RECEIVER',215.5,42,5.8,align='c');p.t('RIBBON CONTACT',302,166,5.8,align='c')

@figure('tether-ribbon','MANY FIBRES MAKE A RIBBON','STAGGERED FIBRE ENDS / NINE BUNDLES','Each break is bridged by the unbroken bundles beside it.')
def ribbon(p):
    for row in range(9):
        y=56+row*11;cut=124+(row*47)%182
        p.l(34,y,cut-7,y,.6,.7,col=ARC if row%3==0 else WHITE)
        p.l(cut+8,y,394,y,.6,.7,col=ARC if row%3==0 else WHITE)
        p.l(cut-6,y-2,cut-1,y+2,.5,.6);p.l(cut+2,y-2,cut+7,y+2,.5,.6)
    for x in (81,221,353):
        p.p([(x,49),(x-7,45),(x+23,45),(x+16,49)],.45,.55)
        p.l(x+8,148,x+8,153,.3,.45)
    # the arrows stop short of the label at every type size
    g=max(75,p.s.measure('BUNDLES / OFFSET JOINTS',5.5,.065)/2+10)
    p.a(35,162,212-g,162);p.a(390,162,212+g,162)
    p.t('BUNDLES / OFFSET JOINTS',212,164.5+.5*p.s.type_growth(5.5),5.5,align='c')

@figure('truth-lamp','A DELAY BEFORE THE DAMAGE','SCRIPTED DINNER EVENT / NOT A DETECTION BENCHMARK','Three seconds between the claim and the social consequences.')
def truth(p):
    for y,label in [(62,'PHRASE'),(105,'DOUBT'),(148,'LAMP')]:p.t(label,0,y+3,5.8);p.l(75,y,425,y,.2,.4)
    wave=[(82+i*2,62+10*math.sin(i*.72)*math.sin(math.pi*i/65)) for i in range(66)];p.p(wave)
    p.p([(97,105),(139,105),(154,93),(175,101),(196,96),(213,105)],col=GOLD)
    p.l(215,45,215,155,.28,.5,dash=[2,3]);p.l(355,45,355,155,.28,.5,dash=[2,3])
    p.p([(78,148),(355,148),(355,131),(423,131)],col=ARC,w=1)
    p.l(219,78,351,78,.45,.55);p.ticks(219,78,2,132);p.t('3 s',285,72,6,align='c')
    p.t('THE RED LIGHT IS NOT A PROOF',263,173,5.7,align='c')

@figure('organ-foundry','KEEP THE INTERIOR FED','PERFUSION SECTION / TWO BRANCHING CHANNELS','Channels feed the cells that lie too deep to be reached from the surface.')
def organ(p):
    p.r([(23,64),(331,49),(404,85),(404,137),(84,151),(23,123)],close=True)
    p.r([(26,65),(84,93),(401,85)],.4,.55,r=10);p.l(84,93,84,148,.4,.55)
    for y in (105,122):
        p.r([(95,y),(166,y-3),(219,y-11),(302,y-13),(387,y-10)],.8,1,col=ARC)
        for x in (137,185,241,285,336):
            p.r([(x,y-2),(x+8,y-17),(x+29,y-23)],.5,.55)
    for x in range(104,380,18):
        p.c(x,137-(x%3)*3,2,.3,.4)
    p.a(3,114,29,114);p.a(405,111,435,111)
    p.t('SUPPLY',3,166,5.8);p.t('DISTRIBUTED CHANNELS',226,166,5.8,align='c');p.t('RETURN',435,166,5.8,align='r')

@figure('volumetric-stage','A POINT NEEDS AN ADDRESS','THREE SELECTED PLANES / ONE VOXEL','Row, column and depth name one point in the haze.')
def stage(p):
    # Addressing volume on an instrument cradle. The selected planes remain
    # straight: rounding optical coordinates would misrepresent the diagram.
    c=(200,88);u=(92,14);v=(-66,18);z=(0,-32)
    def pt(a,b,d):return(c[0]+a*u[0]+b*v[0]+d*z[0],c[1]+a*u[1]+b*v[1]+d*z[1])
    # Cast base in axonometric projection; narrow secondary rim and mounting feet.
    base=[pt(a,b,-1.05) for a,b in ((-1,-1),(1,-1),(1,1),(-1,1))]
    p.r(base,.75,.8,close=True,r=6)
    p.r([(x,y+5) for x,y in base],.4,.5,close=True,r=6)
    for a,b in ((-1,1),(1,1),(1,-1)):
        x,y=pt(a,b,-1.05);p.e(x,y+8,5,2,.5)
    for i,j,col in ((0,1,WHITE),(0,2,ARC),(1,2,GOLD)):
        axes=[u,v,z];aa,bb=axes[i],axes[j]
        corners=[(c[0]+a*aa[0]+b*bb[0],c[1]+a*aa[1]+b*bb[1]) for a,b in ((-1,-1),(1,-1),(1,1),(-1,1))]
        p.p(corners,.5,.6,col=col,close=True)
        # Sparse address graduations and dashed centre traces, not invented data.
        for t in (-.6,-.2,.2,.6):
            x,y=c[0]+t*aa[0]-bb[0],c[1]+t*aa[1]-bb[1]
            p.l(x,y,x+bb[0]*.09,y+bb[1]*.09,.5,.5,col=col)
        p.l(c[0]-aa[0],c[1]-aa[1],c[0]+aa[0],c[1]+aa[1],.3,.45,col=col,dash=[2,4])
    p.c(*c,4,.95,1,ARC);p.c(*c,8,.35,.45,ARC)
    p.r([(218,99),(320,99),(338,90),(360,90)],.4,.5,r=5)
    p.t('SELECTED',365,85,7);p.t('VOXEL',365,99,7)
    p.t('ROW',36,95,7,align='r');p.t('DEPTH',102,47,7,align='r');p.t('COLUMN',272,43,7)


@figure('proxy','A KERB, THREE SECONDS AHEAD','CUE PATH / SENSORS TO HAND','Two pulses in the hand, one word in the ear. The runner takes the step.')
def proxy(p):
    p.r([(23,64),(113,64),(132,80),(132,135),(23,135)],close=True)
    p.p([(113,64),(113,80),(132,80)],.4,.5)
    for i in range(16):p.l(35+i*5,99,35+i*5,119,.6,.5+(i%3)*.4)
    p.t('PX-1',35,86,7)
    p.r([(177,47),(219,47),(219,69),(177,69)],close=True);p.r([(177,121),(219,121),(219,149),(177,149)],close=True)
    p.r([(168,70),(227,70),(227,120),(168,120)],close=True,r=13)
    p.r([(172,74),(223,74),(223,116),(172,116)],.4,.45,close=True,r=10)
    p.r([(228,88),(233,88),(233,101),(228,101)],.55,.6,r=3)
    for y in (53,61,128,136,143):p.l(184,y,212,y,.3,.4)
    p.p([(178,95),(187,95),(192,84),(197,106),(203,91),(216,95)],col=ARC)
    p.a(137,95,162,95);p.a(235,95,286,95)
    p.r([(302,57),(398,57),(412,70),(412,143),(302,143)],close=True)
    p.t('KERB AHEAD',315,77,6);p.t('3 s / 8 m',315,101,10);p.t('STEP UP',315,125,6,col=ARC)
    p.t('CHEST SENSORS',73,166,6,align='c');p.t('CUE BAND',198,166,6,align='c');p.t("RUNNER'S HAND",356,166,6,align='c')

@figure('presence-rig','WHERE THE FLOOR PUSHES BACK','CONTACT PATCH / TWO SOLES, ONE STEP','The rollers push back where the foot lands and carry the step to the centre.')
def presence(p):
    # The contact grid is centred in the column.
    p.s.c.save();p.s.c.translate(49,0)
    try:presence_patch(p)
    finally:p.s.c.restore()

def presence_patch(p):
    for x in range(55,290,25):p.l(x,49,x,147,.2,.4)
    for y in range(49,149,20):p.l(55,y,287,y,.2,.4)
    for x,dy in [(116,0),(220,-10)]:
        p.r([(x-17,75+dy),(x-10,62+dy),(x+12,62+dy),(x+21,83+dy),(x+15,133+dy),(x-15,133+dy)],close=True,r=11)
        for y in range(88,130,10):p.l(x-11,y+dy,x+13,y+dy,.4,.5)
    p.p([(116,98),(142,111),(181,92),(220,87)],col=ARC);p.c(181,92,4,.9,.8,ARC)
    p.a(181,92,180,44);p.a(181,92,271,116)
    p.t('CENTRE-OF-PRESSURE PATH',171,166,5.5,align='c')

@figure('light-sail','LIGHT TURNS, THE SAIL REACTS','REFLECTION GEOMETRY / LOCAL MEMBRANE SECTION','Angle in equals angle out; the push follows the dashed normal.')
def sail(p):
    # A 45° membrane (lit face x = y + 125): light from the left leaves straight down,
    # angle in equals angle out, and the push acts along the normal (1, -1), away from the light.
    p.p([(173,48),(269,144),(275,138),(179,42)],close=True)
    for i in range(6):t=14+i*21.5;p.l(173+t*.7071+1,48+t*.7071-1,173+t*.7071+5,48+t*.7071-5,.35,.5)
    p.l(151,166,221,96,.3,.5,dash=[3,3])
    for i in range(3):
        y=70+i*20;x=y+125;p.a(26,y,x,y);p.a(x,y,x,152)
    p.a(227,90,281,36,GOLD)
    p.t('INCIDENT',44,60,6);p.t('REFLECTED',215,167,6,align='c');p.t('SAIL FORCE',289,36,6)

@figure('tidal-loom','THE FLOW COMES BACK','REVERSING CURRENT / ONE ROTOR, TWO TIDES','Same seabed mounting; the direction of the water changes.')
def tidal(p):
    for i in range(2):
        x=104+i*234;cy=93;p.c(x,cy,40,.4);p.c(x,cy,9,.8,.8)
        for a in (0,120,240):
            a=math.radians(a+i*25);pts=[]
            for r,t in [(10,0),(37,.17),(43,.42),(16,.32)]:pts.append((x+r*math.cos(a+t),cy+r*math.sin(a+t)))
            p.r(pts,.7,.7,col=ARC if i else WHITE,close=True)
        p.r([(x-9,cy+40),(x-14,cy+58),(x+14,cy+58),(x+9,cy+40)],close=True)
        p.c(x,cy,44,.23,.45)
        for off in (-8,8):p.screw(x+off,cy+52,1.5)
        if i:p.a(x+54,cy-37,x-53,cy-37)
        else:p.a(x-53,cy-37,x+54,cy-37)
        p.t('RETURN' if i else 'FLOOD',x,166,6,align='c')
    p.l(184,93,255,93,.3,.55,dash=[3,4]);p.t('SLACK',219.5,113,5.8,align='c')

@figure('manta-foil','TRIM THE FOIL, KEEP THE HULL LEVEL','FOIL SECTION / ONE STRUT, ONE FLAP','Lowering the trim flap adds lift; raising it lets the hull settle.')
def manta(p):
    p.r([(46,112),(73,98),(119,94),(180,99),(268,115),(243,121),(142,124),(75,122)],close=True,r=(24,24,24,24,0,24,24,24))
    p.c(268,115,4);p.r([(271,112),(348,128),(331,134),(272,120)],col=ARC,close=True,r=24)
    p.l(116,96,116,49,.7,2);p.l(126,96,126,49,.7,2)
    for dy in (-26,31):p.r([(24,112+dy),(95,102+dy),(184,108+dy),(290,119+dy),(413,120+dy)],.4,.55,col=ARC)
    p.l(12,42,425,42,.3,.6);p.a(178,87,178,54,GOLD)
    if p.s.layer_mode:  # enlarged type: label the strut from its open side
        p.t('STRUT',108,55,5.8,align='r');p.t('HINGED TRIM',348,163+.72*p.s.type_growth(5.8),5.8,align='c')
    else:p.t('STRUT',149,55,5.8);p.t('HINGED TRIM',348,163,5.8,align='c')

@figure('sock-oracle','MATCH THE WEAVE, NOT THE EXCUSE','THREE SPECIMENS / FICTIONAL PAIRING EXAMPLE','A similar stripe does not establish ownership or a missing mate.')
def socks(p):
    for i in range(3):
        x=41+i*142
        p.r([(x,52),(x+38,52),(x+36,110),(x+62,129),(x+55,145),(x+22,144),(x-3,122)],close=True,r=13)
        for y in (60,65,71):p.l(x+3,y,x+34,y,.5,.6)
        for j in range(5):
            y=84+j*7;p.l(x+5,y,x+29,y+(0 if i<2 else 6),.6,.5,col=ARC if i<2 else GOLD)
        p.t(('PAIR / L','PAIR / R','UNRESOLVED')[i],x+25,168,5.8,align='c')
    p.p([(69,152),(69,157),(211,157),(211,152)],.55,.6,col=ARC)

@figure('memory-kiln','FOCUS BELOW THE SURFACE','OPTICAL READBACK / EXPLODED GLASS PLANES','The reading optics must find the written layer and orientation.')
def memory(p):
    for j in range(4):
        y=85+j*16;p.p([(70,y),(245,y-31),(358,y-8),(184,y+26)],.35,.6,close=True)
        for k in range(5):p.l(157+k*23,y+6-k*4,160+k*23,y+9-k*4,.6,.8,col=ARC)
    f=110  # focus point, inside the second plane
    p.e(181,42,32,7);p.l(149,42,189,f,.5,.65,col=GOLD);p.l(213,42,189,f,.5,.65,col=GOLD)
    p.c(189,f,4,.9,.8,ARC);p.a(196,f,385,65)
    p.t('FOCUS',103,44,5.8);p.t('READBACK',378,50,5.8,align='c');p.t('DEPTH-SELECTED LAYER',214,171,5.8,align='c')

@figure('lunar-porch','THE SEAL GETS ITS OWN TEST','DOCKING LIP / TWO SEALS AND A TEST PORT','A leak-check port samples the space between the seals.')
def lunar(p):
    p.r([(29,64),(176,64),(176,89),(202,89),(202,130),(29,130)],close=True)
    p.r([(237,64),(406,64),(406,130),(221,130),(221,106),(237,106)],close=True)
    for x in range(42,165,14):p.l(x,70,x-9,84,.3,.5);p.l(x,111,x-9,126,.3,.5)
    for x in range(256,398,14):p.l(x,69,x-9,85,.3,.5);p.l(x,111,x-9,126,.3,.5)
    for y in (96,121):p.c(211,y,7,.85,1,ARC)
    p.r([(213,110),(213,45),(318,45)],.7,.7,col=GOLD);p.c(330,45,9);p.l(330,45,334,39,.7,.7)
    p.c(330,45,11.5,.35,.45)
    for a in (160,200,240,280,320):
        t=math.radians(a);p.l(330+6*math.cos(t),45+6*math.sin(t),330+7.5*math.cos(t),45+7.5*math.sin(t),.45,.45)
    p.t('SUIT SIDE',115.5,155,6,align='c');p.t('CABIN SIDE',313.5,155,6,align='c');p.t('TEST PORT',353,47,5.7)

@figure('fibre-braid','THE CARRIERS HAVE RIGHT OF WAY','COUNTER-ROTATING PATHS / TOPOLOGICAL STUDY','Opposite handedness requires crossing paths with scheduled clearance.')
def fibre(p):
    for side in (-1,1):
        pts=[(222+150*math.cos(t),102+48*math.sin(t)*math.cos(t)*side) for t in [i*math.tau/160 for i in range(161)]]
        p.p(pts,.6,.7,col=ARC if side>0 else WHITE)
    for i in range(10):
        a=i*math.tau/10;x=222+150*math.cos(a);y=102+48*math.sin(a)*math.cos(a)
        p.r([(x-4,y-4),(x+4,y-4),(x+4,y+4),(x-4,y+4)],.8,.6,close=True)
    p.c(222,102,15,.65,.7,GOLD);p.l(222,82,222,49,.35,.5)
    p.t('CROSSING CLEARANCE',222,42,5.8,align='c');p.t('TWO CARRIER FAMILIES',222,152,5.8,align='c')

@figure('advice-filter','THE SHUTTER DOES THE INTERRUPTING','MECHANICAL SPEAKER GATE / TWO POSITIONS','The release belongs to the listener, not the louder speaker.')
def advice(p):
    for i in range(2):
        x=91+i*234;p.r([(x-45,57),(x+45,57),(x+45,141),(x-45,141)],close=True)
        for j in range(5):
            y=65+j*16;p.r([(x-40,y),(x+40,y+(9 if i else 0)),(x+40,y+12),(x-40,y+12)],.65,.6,close=True)
        p.c(x+56,101,5);p.l(x+56,101,x+74,77 if i else 101,.8,1)
        p.r([(x-49,54),(x+49,54),(x+49,144),(x-49,144)],.32,.5,close=True,r=9)
        for xx in (x-44,x+44):
            for yy in (59,139):p.screw(xx,yy,1.4)
        p.c(x+74,77 if i else 101,2.5,.6,.7)
        p.t('RELEASED' if i else 'HELD CLOSED',x,165,5.8,align='c')
    p.a(172,104,241,104);p.t('ASK',207,88,6,align='c')

@figure('petal-eye','ONE WAVEFRONT, MANY ADJUSTMENTS','SEGMENT PISTON / SIDE SECTION','Segments share a target wavefront.')
def petal(p):
    for i,off in enumerate((14,-7,5)):
        x=51+i*91;p.r([(x,98+off),(x+63,98+off),(x+63,104+off),(x,104+off)],close=True)
        p.l(x+31,104+off,x+31,147,.65,1);p.coil(x+18,136,27,8,4)
        p.l(x+10,150,x+53,150,.6,1)
        p.a(x+31,94+off,372,61,ARC)
    p.l(33,90,314,90,.45,.55,dash=[3,3]);p.c(377,59,5,.8,.8,ARC)
    p.t('COMMON FOCUS',377,42,5.8,align='c');p.t('INDEPENDENT PISTON ADJUSTMENT',173.5,166,5.8,align='c')

@figure('quiet-stair','THE DECK MUST STAY LOCKED','LATCH SECTION / MANUAL RELEASE ACCESS','The latch carries the hold; the release remains accessible.')
def quiet(p):
    # Shaped latch castings, replaceable bearing insert and pinned release rocker.
    p.r([(23,119),(114,119),(145,109),(153,83),(180,83),(187,98),(187,147),(23,147)],.85,.9,close=True,r=10)
    p.r([(32,128),(115,128),(156,119),(177,126),(177,138),(32,138)],.4,.55,close=True,r=7)
    p.r([(196,76),(349,76),(362,84),(356,98),(222,98),(222,131),(196,137)],.85,.9,close=True,r=9)
    p.r([(226,84),(344,84),(348,91),(226,91)],.4,.5,close=True,r=3)
    p.r([(125,93),(165,60),(211,64),(215,72),(197,88),(161,92),(139,108)],.9,.9,close=True,col=ARC,r=7)
    p.c(132,101,10,.85,.85);p.c(132,101,5,.65,.55);p.screw(132,101,2.2)
    p.r([(175,85),(187,85),(187,109),(179,113)],.65,.6,close=True,r=2)
    for y in (91,97,103):p.l(178,y,184,y+3,.4,.45)
    p.coil(66,93,48,12,6);p.r([(44,93),(56,93),(66,93)],r=3);p.l(114,93,122,98)
    p.screw(42,134,2);p.screw(167,132,2);p.screw(335,87,2)
    p.r([(168,65),(251,45),(372,45),(397,62)],.7,.8,col=GOLD,r=15)
    p.r([(386,64),(399,58),(407,71),(394,77)],.8,.8,close=True,r=5)
    p.l(226,116,284,116,.4,.45);p.t('BEARING FACE',291,119,7)
    # Each name beside its part: the spring over its coil, the pull above its tab.
    p.t('PULL TO RELEASE',392,36,7,align='c');p.t('RETURN SPRING',90,78,7,align='c')


@figure('wind-kite','DEPOWER FOR THE RETURN','WING SECTION / TETHER LOAD DIRECTION','The return stroke changes wing attitude, not the sign of the wind.')
def wind(p):
    for i,ang in enumerate((-.2,.52)):
        x=111+i*226;y=86
        pts=[(-67,1),(-45,-13),(-8,-16),(28,-10),(72,4),(20,9),(-43,8)]
        p.r([(x+u*math.cos(ang)-v*math.sin(ang),y+u*math.sin(ang)+v*math.cos(ang)) for u,v in pts],.75,.8,close=True,col=ARC if i==0 else WHITE,r=24)
        # Bridle pickups follow the rotated lower wing surface.
        pickups=[(x+u*math.cos(ang)-v*math.sin(ang),y+u*math.sin(ang)+v*math.cos(ang)) for u,v in ((-27,8.25),(28,8.2))]
        p.p([pickups[0],(x,y+60),pickups[1]],.45,.6)
        p.a(x,y+60,x+23,y+75)
        p.t('POWERED' if i==0 else 'DEPOWERED',x,43,6,align='c')
    p.t('BRIDLE LOAD',142,164,5.8)  # beside the first section's tether arrow

@figure('coral-cradle','HOLD THE BASE, LEAVE ROOM TO GROW','ATTACHMENT SECTION / ONE BRANCHING FRAGMENT','Hardware contacts the dead base; living tissue stays clear.')
def coral(p):
    p.r([(91,134),(142,119),(272,119),(319,135),(266,151),(141,151)],close=True)
    p.p([(142,119),(142,141),(265,141),(272,119)],.5,.6)
    p.r([(177,126),(172,105),(187,92),(181,69),(190,54),(198,80),(211,88),(227,73),(233,49),(241,65),(236,89),(222,105),(228,126)],.85,.9,close=True)
    p.l(197,113,201,91,.35,.5);p.l(202,96,218,94,.35,.5)
    for x in (146,260):p.r([(x-9,105),(x+9,105),(x+9,129),(x-9,129)],.65,.7,close=True)
    p.l(166,91,124,63,.35,.5);p.t('CLEARANCE',56,58,5.8)
    p.l(231,124,354,110,.35,.5);p.t('BASE ONLY',365,109,5.8)
    p.t('FLOW-THROUGH SUPPORT',205,166,5.8,align='c')

@figure('dune-skimmer','THE FOOTPRINT IS ADJUSTABLE','TREAD CONTACT / TWO GEOMETRIC WIDTHS','The same wheel load spread over twice the tread width.')
def dune(p):
    for i,w in enumerate((64,128)):
        x=104+i*224;p.r([(x-w/2,56),(x+w/2,56),(x+w/2,144),(x-w/2,144)],close=True,r=10)
        for j in range(8):
            y=63+j*10;p.p([(x-w/2+5,y+4),(x-3,y),(x-3,y+5)],.7,.75,col=ARC)
            p.p([(x+3,y+5),(x+3,y),(x+w/2-5,y+4)],.7,.75)
        p.l(x-w/2,153,x+w/2,153,.35,.5);p.ticks(x-w/2,153,2,w)
        p.t('NARROW' if i==0 else 'WIDENED',x,168,6,align='c')
    p.a(175,102,238,102)

@figure('meeting-buoy','PROCEDURAL ESCALATION','CAM AND FLAG FOLLOWER / CONCEPT SECTION','When the cam runs out of patience, the flag goes up.')
def meeting(p):
    pts=[]
    for i in range(101):
        a=i*math.tau/100;r=42+14*(i/100);pts.append((113+r*math.cos(a),108+r*math.sin(a)))
    p.p(pts,.75,.8,close=True);p.c(113,108,10);p.c(113,108,4)
    for i in range(12):
        a=i*math.tau/12;p.l(113+32*math.cos(a),108+32*math.sin(a),113+37*math.cos(a),108+37*math.sin(a),.35,.55)
    p.c(121,47,7,.8,.8,ARC);p.r([(121,40),(121,34),(288,34),(288,141)],.75,.9)
    p.p([(288,53),(364,64),(288,85)],.8,.8,col=ARC,close=True)
    p.coil(263,114,51,10,6);p.l(252,126,324,126,.45,.7)
    p.t('ELAPSED AGENDA',104,175,5.8,align='c');p.t('RAISED OBJECTION',331,166,5.8,align='c')

@figure('seam-surgeon','LOOK INSIDE THE JOINT','WELD SECTION / ANGLED PROBE PATHS','A completed seam can still contain a reason to hold the part.')
def seam(p):
    # Machined coupon ends, a true V-root and deposited bead; rays stay straight.
    p.r([(20,100),(174,100),(204,136),(212,136),(243,100),(420,100),(420,151),(20,151)],.85,.9,close=True,r=[7,0,0,0,0,7,7,7])
    p.r([(174,100),(185,96),(202,98),(216,94),(232,96),(243,100)],.9,.85,r=5)
    for x in range(35,163,12):p.l(x,106,x-7,145,.3,.5)
    for x in range(271,410,12):p.l(x,106,x-7,145,.3,.5)
    p.l(30,146,196,146,.4,.45);p.l(222,146,410,146,.4,.45)
    for y in (110,119,128):p.r([(184+(y-110)*.5,y),(207,y-3),(232-(y-110)*.5,y)],.55,.55,r=8)
    # Inspection shoe in contact with the coupon; shell, wedge and cable socket.
    p.r([(281,74),(315,62),(335,83),(329,100),(279,100),(275,88)],.85,.9,close=True,r=5)
    p.r([(286,77),(311,69),(322,81),(318,88),(283,88)],.5,.5,close=True,r=3)
    p.l(281,97,328,97,.7,.75,col=ARC)
    for x in (291,297,303,309):p.l(x,75-(x-291)*.28,x+6,83-(x-291)*.1,.5,.5)
    p.r([(305,65),(300,49),(273,43),(254,50),(242,48)],.65,.75,r=12)
    p.screw(281,86,1.7);p.screw(327,85,1.7)
    for dx in (0,8,16):p.p([(292+dx,98),(242+dx,146),(203+dx*.25,116)],.65,.6,col=ARC)
    p.r([(198,116),(204,112),(211,115)],.95,1,col=GOLD,r=1)
    p.a(339,59,402,59);p.t('SCAN',370,47,7,align='c')
    # Each part named beside it: the bead on the crown, a fusion face of the V, the root under it.
    p.t('BEAD',208,84,7,align='c')
    p.l(166,86,187,114,.35,.5);p.t('FUSION FACE',160,88,7,align='r')
    p.l(208,139,208,156,.35,.5);p.t('ROOT',208,167,7,align='c')


@figure('queue-garden','ONE CLICK, ONE COMPLETED TURN','RATCHET AND PAWL / LEAF RECORD MECHANISM','The leaf latches an event; it does not forecast the next one.')
def queue(p):
    pts=[]
    for i in range(16):
        a=i*math.tau/16
        for da,r in [(0,45),(.23,54),(.34,45)]:pts.append((130+r*math.cos(a+da),107+r*math.sin(a+da)))
    p.p(pts,.8,.8,close=True);p.c(130,107,13);p.c(130,107,4)
    p.c(218,65,7);p.r([(213,60),(173,65),(155,82),(168,92),(186,77),(218,70)],.8,.8,close=True,col=ARC)
    p.l(225,65,231,63);p.coil(231,63,59,13,6);p.l(290,63,311,63)
    p.l(144,108,336,108,.65,1);p.r([(337,108),(376,79),(411,85),(382,110),(337,108)],.75,.75,close=True,r=16)
    p.l(337,108,397,88,.35,.5)
    p.t('EVENT LATCH',117,175,5.8,align='c');p.t('RETAINED LEAF POSITION',339,150,5.8,align='c')

@figure('compliment-mill','PLEASE ATTACH THE EVIDENCE','MOUNTING-HOLE CHECK / FICTIONAL RECEIPT','Your three mounting holes are aligned. Specific praise survives.')
def compliment(p):
    p.r([(24,68),(237,68),(237,129),(24,129)],close=True)
    for x in (31,230):
        for y in (75,122):p.screw(x,y,1.5)
    for x in (61,130,199):p.c(x,99,12);p.c(x,99,4,.45,.55)
    p.l(36,99,224,99,.25,.45,dash=[3,4])
    for x in (61,130,199):p.l(x,54,x,62,.35,.5)
    p.l(61,54,199,54,.45,.5);p.t('COMMON AXIS',131,43,5.8,align='c')
    p.a(248,99,284,99)
    p.p([(302,53),(421,53),(421,147),(411,143),(400,148),(389,143),(378,148),(367,143),(356,148),(345,143),(334,148),(323,143),(312,148),(302,143)],.7,.7,close=True)
    p.t('OBSERVED',314,73,6);p.t('3 HOLES',314,96,7);p.t('ALIGNED',314,117,7,col=ARC)
    p.t('RECEIPT WITH A REASON',218,174,5.8,align='c')

@figure('neutrino-bell','DO THE CLOCKS AGREE?','SENSOR HITS / THREE TUBES ON ONE CLOCK','Coincidence is timing evidence; background can also coincide.')
def neutrino(p):
    for i,events in enumerate(((62,178,202,333),(104,183,288),(44,189,254,361))):
        y=61+i*35;p.s.text_mid('PMT '+str(i+1),0,y,5.5,track=.065,a=.68);p.l(53,y,426,y,.3,.5)
        for x in events:p.p([(x+53,y),(x+53,y-14),(x+55,y)],.75,.75,col=ARC if 170<x<205 else WHITE)
    p.p([(224,39),(224,152),(264,152),(264,39)],.5,.55,col=GOLD)
    p.t('COINCIDENCE WINDOW',244,166,5.8,align='c')

@figure('sleep-cocoon','SUPPORTS BEFORE SCORES','ARTICULATED SUPPORT SECTION / RECLINED','Three separate supports and one manual release.')
def sleep(p):
    p.r([(34,89),(94,78),(167,106),(236,105),(312,129),(395,109)],.8,1.4)
    for x,y in [(67,84),(201,106),(356,119)]:
        p.l(x,y+3,x,y+35,.65,1);p.r([(x-15,y+35),(x+15,y+35),(x+15,y+40),(x-15,y+40)],close=True)
    p.r([(30,73),(91,64),(99,75),(36,85)],.75,.7,close=True)
    p.r([(170,92),(232,91),(236,102),(167,103)],.75,.7,close=True)
    p.r([(316,115),(390,95),(395,106),(312,125)],.75,.7,close=True)
    p.r([(51,148),(128,156),(260,153),(409,145)],.45,.6,col=GOLD);p.c(416,145,6,.8,.7,GOLD)
    p.t('HEAD',65,51,6,align='c');p.t('PELVIS',202,75,6,align='c');p.t('FEET',355,88,6,align='c')

@figure('plant-alibi','THE METER IS NOT THE ROOT','IRRIGATION SECTION / ILLUSTRATIVE WETTING FRONT','Recorded flow does not prove root uptake or plant health.')
def plant(p):
    # Double-walled ceramic basin; the section distinguishes media and drainage.
    p.r([(111,75),(339,75),(316,147),(139,147)],.85,.9,close=True,r=12)
    p.r([(122,80),(329,80),(309,139),(147,139)],.45,.55,close=True,r=9)
    p.r([(107,74),(107,66),(344,66),(344,74)],.65,.7,r=4)
    p.l(131,88,322,88,.4,.5);p.l(145,130,310,130,.35,.45)
    for x in range(151,307,13):p.e(x,135,3.3,1.5,.4)
    for x in (173,215,258):
        p.r([(x,84),(x+5,96),(x+2,112),(x-6,126)],.75,.85,r=9)
        for dx,dy in ((-1,0),(1,7)):
            p.r([(x+3,97+dy),(x+dx*12,108+dy),(x+dx*19,121+dy)],.5,.55,r=7)
            p.r([(x+dx*12,109+dy),(x+dx*22,111+dy),(x+dx*26,119+dy)],.35,.4,r=5)
    # Flow meter with service bezel, scale, couplings and a swept feed.
    p.r([(24,55),(111,55),(140,69),(150,78)],.8,.9,col=ARC,r=10)
    for x in (43,99):p.r([(x,51),(x+5,51),(x+5,59),(x,59)],.65,.55,close=True,r=1)
    p.c(73,55,15,.8,.7);p.c(73,55,11.5,.45,.45)
    for a in range(205,341,27):
        t=math.radians(a);p.l(73+9*math.cos(t),55+9*math.sin(t),73+12*math.cos(t),55+12*math.sin(t),.5,.5)
    p.l(73,55,80,47,.9,.8);p.c(73,55,1.3,.8)
    for i in range(9):p.c(140+i*18,93+(i%3)*6,1.5,.55,.5,ARC)
    p.r([(149,89),(174,116),(236,126),(303,111)],.55,.65,col=ARC,r=12)
    p.r([(291,145),(291,157),(358,157)],.6,.65,r=5)
    p.r([(286,143),(296,143),(296,149),(286,149)],.65,.6,close=True,r=1)
    p.t('FLOW EVENT',34,33,7);p.t('ROOT ZONE',217,173,7,align='c');p.t('DRAIN',374,160,7)



def draw(s,side):
    key='tether-ribbon' if s.subject=='tether-climber' and side=='right' else s.subject
    fn,title,scope,foot=FIGURES[key]
    x=140 if side=='left' else s.W-650
    from triptych import diagram_y,register_section
    lines=s.wrap(foot,440,5.8,.065)
    foot_y=186
    lead=9
    if s.layer_mode:  # enlarged type: proportional leading, foot moves down
        foot_y+=1.3*s.type_growth(5.8);lead=max(9,s.readable_size(5.8)*1.3)
    height=foot_y+(len(lines)-1)*lead+2
    y=diagram_y(s,side,height)
    s.c.save();s.c.translate(x,y)
    try:
        p=Pen(s);p.t(title,0,0,7.3,.8);p.t(scope,0,17,5.4,.48)
        p.l(0,-16,440,-16,.19,.45);fn(p)
        for i,line in enumerate(lines):p.t(line,0,foot_y+i*lead,5.8,.55)
    finally:s.c.restore()
    register_section(s,side,y-16,y+height)
    s.diagram_slots=getattr(s,'diagram_slots',set())|{side}
    s.individual_diagrams=getattr(s,'individual_diagrams',[])+[key]
