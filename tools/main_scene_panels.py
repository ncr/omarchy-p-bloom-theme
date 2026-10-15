"""Main-scene composition, with physical anchors and deterministic typography."""
import cairo,math
from sheet import WHITE,ARC,GOLD,RED
from hardware3d.family_drawing import data
from path_cleanup import points


def scene(s,name,cx,cy,width,height):
    d=data(name);pts=[p for path in d['paths'] for p in path['points']]
    x0=min(p[0] for p in pts);x1=max(p[0] for p in pts);y0=min(p[1] for p in pts);y1=max(p[1] for p in pts)
    k=min(width/(x1-x0),height/(y1-y0));ox=(x0+x1)/2;oy=(y0+y1)/2
    def point(p):return(cx+(p[0]-ox)*k,cy+(p[1]-oy)*k)
    for path in d['paths']:
        role=path['role'];a,w,col={'structure':(.86,.83,WHITE),'detail':(.65,.49,WHITE),'shell':(.38,.35,WHITE),'accent':(.8,.55,ARC),'cable':(.67,.48,GOLD)}.get(role,(.65,.5,WHITE))
        pts,closed=points(path)
        s.poly([point(p) for p in pts],a,w,close=closed,color=col)
    return {key:point(p) for key,p in d['anchors'].items()}


def callout(s,p,x,y,side,title,sub,color=WHITE):
    s.dot(*p,1.5,.85,color)
    s.poly([p,(x,y),(x+side*116,y)],.48,.5,close=False,color=color)
    align='r' if side<0 else 'l';tx=x+side*5
    s.text(title,tx,y-8,7.3,track=.17,a=.85,align=align,color=color)
    s.text(sub,tx,y+12,5.7,track=.065,a=.62,align=align)


def proxy(s,mx,my):
    a=scene(s,'proxy-main-scene',mx,my-14,558,644)
    # The omitted head remains a symbol, visibly above the physical capped neck.
    from human_figures import absent_head
    hx,hy=a['HEAD'];absent_head(s,hx,hy-57)
    # Bib text belongs to the actual projected plane, not a second guessed pose.
    p,u,v=[a[key] for key in ('BIB0','BIBX','BIBY')]
    s.c.save();s.c.transform(cairo.Matrix((u[0]-p[0])/62,(u[1]-p[1])/62,(v[0]-p[0])/50,(v[1]-p[1])/50,p[0],p[1]))
    if not s.type_growth(5.2):  # enlarged, it would not fit on the bib
        s.text('CITY 10K',31,12,5.2,track=.05,a=.85,align='c')
    s.text('114',31,39,24,track=.01,a=.95,align='c',bold=True)
    s.c.restore()
    # The leader dot sits in the bib's lower-left corner, clear of the digits
    # (on the number it read as "1i4").
    bib=(p[0]+(u[0]-p[0])*6/62+(v[0]-p[0])*45/50,p[1]+(u[1]-p[1])*6/62+(v[1]-p[1])*45/50)
    # A guide for blind and low-vision runners (story of 2026-09-27).
    info=[('HEAD',(hx,hy-57),'NONE FITTED'),
          ('RACE NUMBER',bib,'GUIDE BIB, SAME NUMBER AS ITS RUNNER'),
          ('CUE BAND',a['WATCH'],'CLIPS THE TETHER'),
          ('LEFT WRIST',a['WRIST'],"GRIP FOR THE RUNNER'S HAND"),
          ('CHEST',a['CHEST'],'CAMERAS AND LIDAR / READS 20 m AHEAD'),
          ('HAND',a['HAND'],'SIGNALS FASTER RUNNERS TO PASS'),
          ('RIGHT KNEE',a['KNEE'],"MATCHES THE RUNNER'S 172 STEPS A MINUTE"),
          ('FOOT',a['FOOT'],'FEELS ICE AND LOOSE STONES FIRST')]
    # The original sheets' callouts: each label at the height of its part.
    from hardware3d.family_drawing import callouts
    # The arm, hand and leg labels stay on the side of the limb they name, so no leader crosses the torso.
    sides={'HEAD':1,'CHEST':1,'FOOT':1,'RACE NUMBER':-1,'CUE BAND':-1,'LEFT WRIST':-1,'HAND':-1,'RIGHT KNEE':-1}
    callouts(s,{title:(p[0]-mx,p[1]-my) for title,p,_ in info},{title:sub for title,_,sub in info},mx,my,sides=sides)


def truth(s,mx,my):
    a=scene(s,'truth-main-scene',mx,my+7,720,683)
    for key,color in [('GRANDMOTHER',ARC),('HOST',RED)]:
        x,y=a[key];s.circ(x,y,19,.6,.6,color=color,dash=[3,4])
    info=[('LAMP','LAMP',-1,-322,'GLOWS RED FOR THREE SECONDS. NOT DIMMABLE.'),
          ('SWITCH','OFF SWITCH',1,-350,'NEW IN VERSION 2'),
          ('MICROPHONES','MICROPHONE RING',-1,-207,'HEARS THE HALF SECOND BEFORE "OF COURSE NOT"'),
          ('CAMERAS','THERMAL CAMERAS',1,-212,'NOSES COOL BY 0.4 °C WHEN THEIR OWNERS LIE'),
          ('GRANDMOTHER','SEAT 1, GRANDMOTHER',-1,-85,'NEVER SETS IT OFF. SAYS WHAT SHE THINKS.'),
          ('HOST','SEAT 4',1,-53,'"NO, I LOVE IT. I\'LL WEAR IT ALL THE TIME."'),
          ('DINNER','DINNER',-1,278,'THE SUBJECT OF 31 % OF ALL DETECTIONS'),
          ('DOG','DOG',1,294,'HAS NEVER SET IT OFF EITHER')]
    for key,title,side,dy,sub in info:callout(s,a[key],mx+side*370,my+dy,side,title,sub)
