"""Ten authored mini-dossiers: physics, explicit fictional logs, and dry humour.

Plots are computed from documented equations or declared fictional counts.
No random curves, no fabricated measurements presented as research.
Coordinates remain in the sheet's deterministic type/line layer.
"""
import math
from sheet import WHITE,ARC,GOLD
from collection_layout import note_box

DATA={
1:dict(title='THRUST FALLS AS THE SAIL TURNS',kind='sail',scope='IDEAL MIRROR / NORMAL FORCE / NORMALISED',
    fact='Photons carry momentum. Solar wind is not the engine.',
    note='REEFING: FOUR DRUMS, NO SHOUTING.',
    process=('PHOTONS','MEMBRANE','THRUST'),
    rows=[('PROPELLANT','NONE CARRIED'),('REFUELLING','STAR INCLUDED'),('SAIL','FOUR WELDED QUADRANTS')],
    foot='P / P₀ = cos²(angle) / constant illumination'),
10:dict(title='THE UNPAIRED CASE FILE',kind='sock',scope='FICTIONAL SORTING LOG / 100 SOCKS',
    fact='A visual match is not proof that the other sock exists.',
    note='WARRANTY EXCLUDES PARALLEL UNIVERSES.',
    process=('WEAVE','OWNER','PAIR?'),
    rows=[('MATCHED','84 SOCKS / 42 PAIRS'),('UNRESOLVED','16 INDIVIDUALS'),('PORTAL FOUND','0')],
    foot='Unresolved: 9 solitary / 5 worn / 2 disputed'),
30:dict(title='CONSENT IS THE SIGNAL',kind='advice',scope='SCRIPTED EXAMPLE / NOT A SPEECH BENCHMARK',
    fact='The shutter gates this speaker. Your uncle is still audible.',
    note='EXPERTISE DOES NOT BYPASS THE BUTTON.',
    process=('DETECT','HOLD','ASK'),
    rows=[('DEFAULT','CLOSED'),('RELEASE','LISTENER REQUEST'),('SENIORITY','NOT AN INPUT')],
    foot='Buffered audio expires; it does not become a podcast.'),
31:dict(title='COLLECT PHOTONS, NOT OPINIONS',kind='mirror',scope='IDEAL APERTURE / FIXED SHAPE / AREA RATIO',
    fact='Warm things glow in the infrared, mirrors included; the sunshade keeps this one cold enough not to blind itself.',
    note='ALIEN NEIGHBOURS: STILL NOT CONFIRMED.',
    process=('ALIGN','PHASE','INTEGRATE'),
    rows=[('ACTUATORS','THREE PER SEGMENT / 57 IN ALL'),('DIGITAL ZOOM','NOT A BIGGER MIRROR')],
    foot='A / A₀ = (D / D₀)²: twice the diameter, four times the light.'),
44:dict(title='GROWN HERE, PLANTED THERE',kind='coral',scope='RESTORATION WORKFLOW / TIME NOT TO SCALE',
    fact='Nursery-grown coral can be outplanted. Habitat still matters.',
    note='DOES NOT PATCH THE OCEAN OPERATING SYSTEM.',
    process=('HOLD','NURSE','OUTPLANT'),
    rows=[('FRAGMENTS','TWO PER CASSETTE'),('NURSERY TIME','MONTHS, NOT MINUTES'),('SUCCESS','REQUIRES FOLLOW-UP')],
    foot='Fragments branch in the nursery, then go back to the reef.'),
56:dict(title='SPREAD THE LOAD',kind='sand',scope='MEAN CONTACT PRESSURE / FIXED WHEEL LOAD',
    fact='A wheel that sinks keeps climbing out of its own rut; on soft sand that is most of the rolling resistance.',
    note='FOUR-WHEEL DRIVE. ZERO-WHEEL JUDGEMENT.',
    process=('SENSE','WIDEN','RECHECK'),
    rows=[('MODEL','p = F / A'),('WIDTH','NARROW ON FIRM GROUND'),('SHADE','DEPLOY WHEN PARKED')],
    foot='Pressure falls as the contact area grows.'),
60:dict(title='THIS COULD HAVE BEEN A FLAG',kind='meeting',scope='FICTIONAL MEETING LOG / 60 MINUTES',
    fact='Elapsed time is measurable. Whether this helped is another question.',
    note='THE FLAG HAS BEEN INVITED TO A FOLLOW-UP.',
    process=('LISTEN','CLASSIFY','RAISE'),
    rows=[('DECISIONS','9 MINUTES'),('FORMAT DEBATE','33 MINUTES'),('NEXT MEETING','18 MINUTES')],
    foot='Mutually exclusive labels; no productivity claim.'),
87:dict(title='AN EXTREMELY QUIET DOORBELL',kind='neutrino',scope='DETECTION CHAIN / NEUTRINO TO SENSOR',
    fact='A photomultiplier turns a single photon into a pulse of millions of electrons.',
    note='IF IT RINGS OFTEN, CHECK THE DARK CURRENT.',
    process=('LIGHT','PHOTOELECTRON','TIME TAG'),
    rows=[('MEDIUM','WATER OR ICE'),('SHIELDING','ROCK OVERBURDEN'),('BACKGROUND','ALSO GETS A VOTE')],
    foot='Only the charged particle leaves a trail of light; the neutrino stays dark.'),
99:dict(title='SUPPORT, REST, RELEASE',kind='rest',scope='ONE REST CYCLE / SEQUENCE OF STATES',
    fact='Release works at any recline angle; the occupant never waits for the seat.',
    note='PRODUCTIVITY MODE: TEMPORARILY UNINSTALLED.',
    process=('SUPPORT','REST','RELEASE'),
    rows=[('WAKE-UP','OCCUPANT DECIDES'),('SLEEP SCORE','NOT COLLECTED')],
    foot='The seat keeps its support until the release is complete.'),
100:dict(title='THE OWNER SAID THEY WATERED IT',kind='plant',scope='FICTIONAL CASE LOG / SEVEN DAYS',
    fact='A watering claim and a flow-meter event are different records.',
    note='THE FERN HAS REQUESTED LEGAL REPRESENTATION.',
    process=('METER','TIMESTAMP','RETAIN'),
    rows=[('CLAIMED','7 WATERINGS'),('RECORDED','2 EVENTS'),('BLAMED','THE PLANT')],
    foot='Meter events do not prove root uptake or plant health.')
}


def tx(s,t,x,y,size=7,a=.76,**kw):return s.text(t,x,y,size,track=.08,a=a,**kw)


def arrow(s,a,b,color=WHITE):
    s.ln(*a,*b,.5,.55,color=color)
    angle=math.atan2(b[1]-a[1],b[0]-a[0]);r=4
    s.poly([(b[0]-r*math.cos(angle-.45),b[1]-r*math.sin(angle-.45)),b,(b[0]-r*math.cos(angle+.45),b[1]-r*math.sin(angle+.45))],.55,.55,close=False,color=color)


def header(s,d,x,y,w):
    tx(s,d['title'],x,y,8,.89)
    tx(s,d['scope'],x,y+17,5.8,.48)
    s.ln(x,y-16,x+w,y-16,.20,.45)


def axes(s,x,y,w,h,xlabel,ytop='1.0',ybottom='0'):
    for t in (0,.25,.5,.75,1):s.ln(x,y+h*t,x+w,y+h*t,.13,.4)
    s.poly([(x,y),(x,y+h),(x+w,y+h)],.48,.55,close=False)
    tx(s,ytop,x-9,y+4,6,.5,align='r');tx(s,ybottom,x-9,y+h,6,.5,align='r')
    tx(s,xlabel,x+w,y+h+27,7,.55,align='r')


def curve(s,points,color=GOLD):s.poly(points,.8,.8,close=False,color=color)


def plot(s,d,x,y,w):
    header(s,d,x,y,w);y+=40;kind=d['kind'];h=97
    if kind in ('sail','mirror','sand'):
        from .editorial_second import ticks_under
        px=x+26;pw=w-38  # the last tick value stays inside the column
        xlabel={'sail':'INCIDENCE / DEGREES','mirror':'DIAMETER / D₀','sand':'CONTACT AREA / A₀'}[kind]
        axes(s,px,y,pw,h,'','4.0' if kind=='mirror' else '1.0','0')
        if kind=='sail':
            points=[(px+pw*i/90,y+h*(1-math.cos(math.radians(i))**2)) for i in range(91)]
            ticks=[(0,'0'),(1/3,'30'),(2/3,'60'),(1,'90')]
        elif kind=='mirror':
            points=[(px+pw*i/100,y+h*(1-(.5+1.5*i/100)**2/4)) for i in range(101)]
            ticks=[(0,'0.5'),(1/3,'1.0'),(2/3,'1.5'),(1,'2.0')]
        else:
            points=[(px+pw*i/100,y+h*(1-1/(1+3*i/100))) for i in range(101)]
            ticks=[(0,'1'),(1/3,'2'),(2/3,'3'),(1,'4')]
        curve(s,points)
        # Axis name hangs under the values, so enlarged type never stacks into them.
        ticks_under(s,px,y+h,pw,ticks,xlabel)
    elif kind in ('sock','meeting'):
        values=[('MATCHED',84),('SOLITARY',9),('WORN',5),('DISPUTED',2)] if kind=='sock' else [('DECISIONS',9),('FORMAT DEBATE',33),('NEXT MEETING',18)]
        maxv=100 if kind=='sock' else 60;barx=x+126;bw=w-173
        if s.layer_mode:
            # Enlarged value labels need the end of the bar track clear.
            unit=' socks' if kind=='sock' else ' min'
            bw=min(bw,w-126-14-max(s.measure(str(v)+unit,6.5,.08) for _,v in values))
        for i,(label,value) in enumerate(values):
            yy=y+7+i*29
            tx(s,label,x,yy,6.3,.72)
            s.ln(barx,yy-3,barx+bw,yy-3,.17,3.2)
            s.ln(barx,yy-3,barx+bw*value/maxv,yy-3,.86,3.2,color=ARC if i==0 else GOLD)
            tx(s,str(value)+(' socks' if kind=='sock' else ' min'),x+w,yy,6.5,.8,align='r')
    elif kind in ('advice','rest'):
        labels=['PHRASE BUFFER','ASK BUTTON','SPEAKER GATE'] if kind=='advice' else ['SEAT SUPPORT','REST WINDOW','RELEASE']
        starts=[.05,.48,.50] if kind=='advice' else [.02,.21,.87]
        ends=[.50,.53,.89] if kind=='advice' else [.94,.83,.94]
        px=x+123;pw=w-130
        for i,label in enumerate(labels):
            yy=y+13+i*29;s.text_mid(label,x,yy-6,6.2,track=.08,a=.68)  # centred on its trace
            s.ln(px,yy,px+pw,yy,.2,.4)
            points=[(px,yy),(px+pw*starts[i],yy),(px+pw*starts[i],yy-12),(px+pw*ends[i],yy-12),(px+pw*ends[i],yy),(px+pw,yy)]
            curve(s,points,ARC if i==0 else GOLD)
        tx(s,'SEQUENCE →',x+w,y+108,6,.48,align='r')
    elif kind=='plant':
        tx(s,'OWNER CLAIM',x,y+20,6.3);tx(s,'FLOW METER',x,y+57,6.3)
        px=x+122;pw=w-137
        for i in range(7):
            xx=px+i*pw/6
            s.circ(xx,y+17,3,.7,.6)
            if i in (1,5):s.dot(xx,y+54,3,.9,color=ARC)
            else:s.ln(xx-3,y+54,xx+3,y+54,.38,.6)
            tx(s,str(i+1),xx,y+85,6,.6,align='c')
        tx(s,'DAY',x+w,y+109,6,.48,align='r')
    elif kind=='coral':
        for i,label in enumerate(('FRAGMENT','NURSERY','REEF')):
            xx=x+55+i*(w-110)/2
            # Attachment puck, branching fragment, and a flow-through substrate.
            s.poly([(xx-27,y+69),(xx,y+60),(xx+27,y+69),(xx,y+78)],.6,.6,close=True)
            for j in range(1 if i==0 else 3):
                bx=xx+(j-(0 if i==0 else 1))*12
                s.poly([(bx,y+63),(bx-2,y+46),(bx+1,y+31)],.75,.75,close=False)
                s.poly([(bx-1,y+48),(bx-8,y+40),(bx-9,y+32)],.56,.55,close=False)
            tx(s,label,xx,y+99,6.3,.77,align='c')
            if i<2:arrow(s,(xx+35,y+52),(xx+(w-110)/2-34,y+52),ARC)
        tx(s,'RECORD IDENTITY → FOLLOW SURVIVAL',x,y+124,5.8,.48)
    elif kind=='neutrino':
        # Charged secondary emits light; neutrino travels to an interaction vertex.
        yy=y+62;vertex=x+92;tip=x+w-32
        s.ln(x,yy,vertex,yy,.42,.6,dash=[3,4]);s.dot(vertex,yy,2,.85)
        arrow(s,(vertex,yy),(tip,yy),WHITE)
        # Each name sits just beside what it names: the incoming line, the vertex,
        # the outgoing track, and the three light paths with their sensors.
        tx(s,'NEUTRINO',x,yy-7,6,.62)
        tx(s,'INTERACTION',vertex,yy+13,6,.5,align='c')
        tx(s,'CHARGED SECONDARY',tip,yy+13,6,.7,align='r')
        for dx in (30,76,122):
            end=(vertex+dx+32,yy-31);arrow(s,(vertex+dx,yy),end,ARC)
            s.circ(*end,5,.48,.55)
        tx(s,'CHERENKOV LIGHT → SENSORS',vertex+(30+122+32+5)/2,yy-45,6,.67,align='c')
    tx(s,d['foot'],x,y+145,5.9,.6)


def dossier(s,d,x,y,w):
    from collection_layout import field_notes
    field_notes(s,d)


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
