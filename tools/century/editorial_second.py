"""Second ten: individual plots, mechanism diagrams and fictional service records."""
import math
import cairo
from sheet import WHITE,ARC,GOLD,FONT
from collection_layout import note_box
from .editorial import tx,arrow,header,axes,curve,dossier

DATA={
2:dict(title='THE TIDE DOES NOT TAKE REQUESTS',kind='current',scope='KINETIC FLUX / FIXED AREA AND DENSITY',
 fact='Tides are highly predictable, so the grid knows long in advance when this machine will deliver power.',
 note='THE MOON HAS DECLINED YOUR SLA.',process=('CURRENT','ROTOR','GRID'),
 rows=[('SLACK WATER','NO FLOW POWER'),('FISH','NOT A FUEL SOURCE')],foot='P / P₀ = |v / v₀|³: twice the current carries eight times the power.'),
6:dict(title='THE HULL WOULD LIKE SOME SPACE',kind='foil',scope='IDEAL LIFT RATIO / FIXED AREA, DENSITY AND CL',
 fact='Lifted clear, the hulls stop pushing water aside, which is where most of the energy saving comes from.',
 note='SEASICKNESS HAS NOT ACCEPTED THE PATCH.',process=('ACCELERATE','TRIM','RETRACT'),
 rows=[('HULL FORM','WAVE-PIERCING'),('LOOKOUT','MAST CAMERA ABOVE THE SALON')],foot='L / L₀ = (v / v₀)²: twice the speed, four times the lift.'),
17:dict(title='TWO BITS IN EVERY MARK',kind='archive',scope='CELL MAP / FOUR ORIENTATIONS',
 fact='Every plate is read back and verified before it is stored.',
 note='README INCLUDED. CIVILISATION NOT INCLUDED.',process=('WRITE','VERIFY','DECODE'),
 rows=[('READBACK','POLARISED LIGHT')],foot='Read along each row, every angle gives one bit pair.'),
18:dict(title='DUST HAS NO CABIN PRIVILEGES',kind='suitport',scope='CONTAMINATION BOUNDARY / SCHEMATIC',
 fact='Every entry starts with docking: the suit\'s back hatch seals to the port before anyone opens it.',
 note='PLEASE WIPE YOUR PLANET BEFORE ENTERING.',process=('DOCK','CHECK','ENTER'),
 rows=[('QUICK COUPLINGS','THREE, EACH WITH AN ID PLATE'),('EMERGENCY','SEPARATE EGRESS')],foot='The suit stays outside; only the person comes in.'),
25:dict(title='DIRECTION IS A MATERIAL PROPERTY',kind='braid',scope='IDEAL HELIX / FIXED CARRIER TANGENTIAL SPEED',
 fact='A braided tube has no seam: every yarn runs unbroken from one end to the other.',
 note='UNLIKE THE COMMITTEE, THE FIBRES HAVE DIRECTION.',process=('TENSION','CROSS','TAKE UP'),
 rows=[('CARRIERS','SIX EACH WAY ROUND')],foot='tan θ = vₜ / vₐ, θ from the mandrel axis: slow the mandrel and the fibres turn towards the hoop.'),
38:dict(title='ACCESS IS NOT A SIDE QUEST',kind='access',scope='INTERLOCK SEQUENCE / FOUR TREADS, THREE STATES',
 fact='As a stair it is just a stair: nothing moves until someone asks for the platform.',
 note='CLAUDE CALLED THIS LABEL LOAD-BEARING. THE LATCH DISAGREES.',process=('LEVEL','LOCK','LIFT'),
 rows=[('LIFT SCREWS','8, ONE MOTOR EACH'),('HANDRAILS','FIXED, BOTH SIDES'),('EXIT','HIGH LANDING')],foot='All three states drawn at the same scale.'),
42:dict(title='YOU ALSO HAVE TO REEL IT BACK',kind='kite',scope='TETHER FORCE / PAID-OUT LENGTH CYCLE',
 fact='On a tether it reaches the stronger winds higher up, with far less material than a tower.',
 note='PLEASE DO NOT HOLD THE STRING.',process=('REEL OUT','DEPOWER','REEL IN'),
 rows=[('WORK','LOOP AREA'),('RETURN','CONSUMES ENERGY'),('NET ELECTRIC','AFTER LOSSES')],foot='Reeling in at low tension costs less than reeling out earns.'),
65:dict(title='A CIRCLE IS NOT A CERTIFICATE',kind='weld',scope='INSPECTION LOG / TWELVE SECTORS',
 fact='The torch passes over, beside and under the pipe; gravity pulls the weld pool differently in each, so every sector has its own settings.',
 note='THE DEADLINE IS NOT A WELDING PARAMETER.',process=('PREPARE','WELD','INSPECT'),
 rows=[('TORCH PATH','ONE FULL ORBIT'),('RECORD','EVERY SECTOR'),('RELEASE','AFTER REVIEW')],foot='One orbit; every sector is judged on its own.'),
70:dict(title='FIVE MINUTES, SINCE LAST TUESDAY',kind='queue',scope='FICTIONAL EVENT LOG / SIX COMPLETED POSITIONS',
 fact='Each leaf records a completed position. It does not predict when your turn will arrive.',
 note='PLEASE HOLD. YOUR PATIENCE IS IMPORTANT TO US.',process=('TICKET','EVENT','LEAF'),
 rows=[('LEAVES','6 COMPLETIONS'),('CLOCK','NOT A FORECAST'),('ESTIMATE','INSUFFICIENT EVIDENCE')],foot='Events at 2, 5, 9, 14, 20, 27 min; not queue performance.'),
80:dict(title='AMAZING HAS FAILED INSPECTION',kind='praise',scope='FICTIONAL REVIEW LOG / TWELVE CANDIDATES',
 fact='A defensible compliment needs an observation. Enthusiasm is not a measurement.',
 note='FLATTERY CARTRIDGE: EMPTY BY DESIGN.',process=('INSPECT','CITE','PRINT'),
 rows=[('SPECIFIC','3 APPROVED'),('GENERIC','7 REJECTED'),('UNSUPPORTED','2 REJECTED')],foot='Example receipt: Your three mounting holes are aligned.')
}


def cap(s,size):
    """Cap height of a label as drawn, enlarged type of composed profiles included."""
    c=s.c;c.save();c.select_font_face(FONT,cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(s.readable_size(size));h=-c.text_extents('H').y_bearing;c.restore()
    return h


def mid(s,t,x,y,size=7,a=.76,**kw):
    """tx() centred on its capitals at y: optical centring beside a mark or inside a box."""
    return s.text_mid(t,x,y,size,track=.08,a=a,**kw)


def below(s,t,x,y,size=7,a=.76,gap=6,**kw):
    """tx() whose capitals start gap units under y, however large the type grows."""
    return mid(s,t,x,y+gap+cap(s,size)/2,size,a,**kw)


def ticks_under(s,px,y,pw,ticks,xlabel=None):
    """Tick marks and centred values under an x axis at y (the c001 convention).

    The axis name hangs under the values, so enlarged type never stacks into them;
    pass it here and an empty name to axes().
    """
    for t,label in ticks:
        s.ln(px+pw*t,y,px+pw*t,y+4,.45,.5)
        below(s,label,px+pw*t,y+4,7,.65,gap=5,align='c')
    if xlabel:below(s,xlabel,px+pw,y+9+cap(s,7),7,.55,gap=6,align='r')


def plot(s,d,x,y,w):
    header(s,d,x,y,w);y+=40;h=97;k=d['kind'];px=x+26;pw=w-28
    if k in ('current','foil','braid'):
        pw=w-38  # the last tick value stays inside the column
        axes(s,px,y,pw,h,'','90°' if k=='braid' else '1.0' if k=='current' else '4.0')
        points=[]
        for i in range(121):
            t=i/120
            if k=='current':value=abs(2*t-1)**3
            elif k=='foil':value=(2*t)**2/4
            else:value=math.atan2(1,.25+3.75*t)/(math.pi/2)
            points.append((px+pw*t,y+h*(1-value)))
        curve(s,points)
        ticks=[(0,'−1'),(.5,'0'),(1,'+1')] if k=='current' else [(0,'0'),(.5,'1'),(1,'2')] if k=='foil' else [(0,'0.25'),(.2,'1'),(.467,'2'),(1,'4')]
        ticks_under(s,px,y+h,pw,ticks,{'current':'CURRENT / v₀','foil':'SPEED / v₀','braid':'AXIAL SPEED / vₜ'}[k])
    elif k=='archive':
        # Four symbolic orientations, laid on four real-looking indexed rows.
        # The key draws the same glyphs as the plate, one per row, in its own column.
        def cell(xx,yy,code):
            a=code*math.pi/4
            s.circ(xx,yy,5,.22,.35)
            s.ln(xx-4*math.cos(a),yy-4*math.sin(a),xx+4*math.cos(a),yy+4*math.sin(a),.8,.9,color=ARC)
        top=y+8;key=x+300
        for row in range(4):
            yy=top+20+row*22
            mid(s,str(row+1),x,yy,6,.5)
            for col in range(9):cell(x+44+col*24,yy,(row*5+col*3)%4)
            cell(key+5,yy,row);mid(s,format(row,'02b'),key+20,yy,7,.8)
        tx(s,'ORIENTATION',key,top,6,.6)
        tx(s,'READING KEY TRAVELS WITH THE PLATE',x,y+119,6,.5)
    elif k=='suitport':
        boundary=x+238
        s.ln(boundary,y+4,boundary,y+102,.65,.7)
        s.ln(boundary+5,y+4,boundary+5,y+102,.32,.4)
        # The two sides are named at the wall they share, on one baseline.
        tx(s,'EXTERIOR',boundary-12,y+8,6,.65,align='r');tx(s,'CABIN',boundary+17,y+8,6,.65)
        # Dust samples stop before the pressure boundary; occupants pass a tested interface.
        for dx,dy in ((12,25),(51,47),(88,32),(136,68),(38,77),(111,85),(172,38)):
            s.diamond(x+dx,y+dy,2,.55,.5,color=GOLD)
        s.poly([(boundary-35,y+29),(boundary-14,y+29),(boundary-14,y+77),(boundary-35,y+77)],.7,.6,close=False)
        below(s,'DUSTY SUIT',boundary-14,y+77,6,.62,gap=8,align='r')
        arrow(s,(boundary-8,y+53),(x+w-29,y+53),ARC)
        tx(s,'REAR ENTRY',(boundary+5+x+w-29)/2,y+53-8,6,.6,align='c')
        below(s,'TESTED SEAL',boundary+2.5,y+102,6,.66,gap=8,align='c')
    elif k=='access':
        # Elevation of the exact model's four fixed-x, independently driven treads.
        # Three states, common scale. No fictitious diagonal four-bar mechanism.
        for n,(name,heights) in enumerate((('01 / STAIR',[16,33,50,67]),('02 / LEVEL LOW',[16]*4),('03 / LEVEL HIGH',[67]*4))):
            xx=x+n*151;floor=y+86
            for j,z in enumerate(heights):
                left=xx+j*28;top=floor-z*.82
                s.poly([(left,top),(left+27,top),(left+27,top+4),(left,top+4)],.8,.7,close=True)
                s.ln(left+13,top+5,left+13,floor,.3,.5)
            s.ln(xx,floor+2,xx+111,floor+2,.28,.5)
            tx(s,name,xx,y+106,5.7,.73)
            if n<2:arrow(s,(xx+116,y+48),(xx+139,y+48),ARC)
        tx(s,'EMPTY TO LEVEL / LOCK TREADS / THEN PLATFORM LIFT',x,y+127,5.7,.55)
    elif k=='kite':
        axes(s,px,y,pw,h,'PAID-OUT LENGTH / NORMALISED')
        # Strokes on the .75 and .25 grid lines; each label centred in the free
        # grid band beyond its stroke, clear of every line.
        a=(px+pw*.13,y+h*.25);b=(px+pw*.87,y+h*.25);c=(b[0],y+h*.75);d0=(a[0],c[1])
        s.poly([a,b,c,d0],.7,.6,close=True,color=GOLD)
        arrow(s,a,b,ARC);arrow(s,c,d0,WHITE)
        mid(s,'HIGH TENSION / REEL OUT',px+pw/2,y+h*.125,6,.72,align='c')
        mid(s,'LOW TENSION / RETURN',px+pw/2,y+h*.875,6,.65,align='c')
    elif k=='weld':
        cx=x+91;cy=y+54;r=43
        for j in range(12):
            col=ARC if j<9 else GOLD
            pts=[(cx+r*math.cos(math.radians(-90+j*30+a)),cy+r*math.sin(math.radians(-90+j*30+a))) for a in range(3,28,3)]
            s.poly(pts,.8,2.1 if j==11 else 1,close=False,color=col)
            if j==11:
                a=math.radians(-90+j*30+15);xx=cx+r*math.cos(a);yy=cy+r*math.sin(a)
                s.ln(xx-3,yy-3,xx+3,yy+3,.8,.6);s.ln(xx+3,yy-3,xx-3,yy+3,.8,.6)
        # Count and unit as one group, centred on the ring by their capitals.
        c12,cu=cap(s,11),cap(s,5.5);top=cy-(c12+6+cu)/2
        mid(s,'12',cx,top+c12/2,11,.8,align='c');mid(s,'SECTORS',cx,top+c12+6+cu/2,5.5,.5,align='c')
        # Legend: stroke, label, count in a tabular column right beside the labels.
        rows=(('ACCEPT',9),('HOLD',2),('REWORK',1))
        lx=x+208;nx=lx+max(s.measure(label,6.5,.08) for label,_ in rows)+14+s.measure('0',7,.08)
        for i,(label,count) in enumerate(rows):
            yy=cy+(i-1)*30
            if i==2:  # drawn as the rework sector: heavier stroke and a cross
                s.ln(x+170,yy,x+193,yy,.8,2.1,color=GOLD)
                s.ln(x+178.5,yy-3,x+184.5,yy+3,.8,.6);s.ln(x+184.5,yy-3,x+178.5,yy+3,.8,.6)
            else:s.ln(x+170,yy,x+193,yy,.8,1,color=ARC if i==0 else GOLD)
            mid(s,label,lx,yy,6.5,.72);mid(s,str(count),nx,yy,7,.8,align='r')
    elif k=='queue':
        axes(s,px,y,pw,h,'ELAPSED MINUTES','6','0');pts=[(px,y+h)]
        for i,t in enumerate((2,5,9,14,20,27)):
            xx=px+pw*t/30;pts.extend([(xx,y+h*(1-i/6)),(xx,y+h*(1-(i+1)/6))])
        pts.append((px+pw,y));curve(s,pts,ARC)
        for t in (0,10,20,30):tx(s,str(t),px+pw*t/30,y+h+9+.72*s.type_growth(5.5),5.5,.6,align='c')
    elif k=='praise':
        for i,(label,v) in enumerate((('SPECIFIC',3),('GENERIC',7),('UNSUPPORTED',2))):
            yy=y+18+i*32;tx(s,label,x,yy,6.3,.7)
            for j in range(7):
                xx=x+132+j*30
                if j<v:s.ln(xx,yy-3,xx+17,yy-3,.85,3,color=ARC if i==0 else GOLD)
                else:s.ln(xx,yy-3,xx+17,yy-3,.17,.6)
            tx(s,str(v),x+w,yy,7,.8,align='r')
    tx(s,d['foot'],x,y+145,5.9,.6)


def draw(s,entry):
    d=DATA.get(entry['number'])
    if not d:return
    from triptych import extra, diagram, punchline, diagram_y, register_section
    with s.layer('section'):
        y=diagram_y(s,'left',187)
        plot(s,d,140,y,440)
        register_section(s,'left',y-16,y+187)
        s.diagram_slots={'left'}
        diagram(s,'right')
        dossier(s,d,*note_box(s))
        punchline(s,d['note'])
