"""System architecture and hierarchical material study for the TC-20."""
from hardware3d.secondary_drawing import view
from sheet import WHITE,ARC


def system(s,lx):
    tx=lx-65
    s.view_label(lx-175,105,'B','ELEVATOR SYSTEM','ANCHOR TO COUNTERWEIGHT / AXIS BROKEN',align='l')
    # Independent rail segments make the distance compression explicit.
    for a,b in [(196,244),(262,316),(368,398),(416,488)]:
        for dx in (-2,2):s.ln(tx+dx,a,tx+dx,b,.8,.7,color=ARC)
    for y in (252,407):
        for dy in (-3,3):s.poly([(tx-7,y+dy-3),(tx+7,y+dy+3)],.75,.75,close=False)
    view(s,'tether-counterweight',tx,168,47,68)
    view(s,'tether-geo-station',tx,342,143,70)
    view(s,'tether-ocean-anchor',tx,548,188,122)

    # Same TC-20 geometry as the main view, at a deliberately enlarged scale.
    view(s,'tether-climber',tx,451,37,55)
    s.ln(tx-34,474,tx-34,432,.65,.65,color=ARC)
    s.poly([(tx-37,438),(tx-34,432),(tx-31,438)],.65,.65,close=False,color=ARC)
    # Laser path is distinguished from the material tether.
    s.ln(tx+14,500,tx+5,477,.5,.6,dash=[3,3],color=ARC)

    for y,title,sub,end in [(168,'COUNTERWEIGHT','100 000 km',tx+28),
                            (342,'GEO TRANSFER','35 786 km',tx+77),
                            (451,'TC-20 / ASCENDING','LASER POWER FROM BELOW',tx+25),
                            (549,'OCEAN ANCHOR','EQUATOR / SEA LEVEL',tx+102)]:
        label=lx+60
        s.ln(end,y,label-10,y,.35,.5)
        s.text(title,label,y-7,6.5,a=.85)
        # Type held at the readable floor grows inside this scaled view; the second line keeps its leading.
        s.text(sub,label,y+10+.75*(s.readable_size(5.7)-5.7),5.7,a=.56)

    # Water datum and a few clipped surface wavelets ground the platform.
    s.ln(lx-180,613,lx+186,613,.4,.55)
    for x,y,length in [(-152,622,52),(-83,629,31),(-15,620,58),(74,628,42),(134,620,30)]:
        s.bez((lx+x,y),(lx+x+length*.3,y-2),(lx+x+length*.7,y+2),(lx+x+length,y),.27,.4)
    s.text('CO-ROTATING WITH EARTH',lx,653,5.8,a=.5,align='c')


def ribbon(s,rx):
    # A peeled material sample explains how flat ribbon is assembled from bundles.
    s.text('01 / RIBBON SECTION',rx-170,147,6.3,a=.78)
    view(s,'tether-ribbon-laminate',rx,265,348,192)
    if s.layer_mode:  # enlarged: start clear of the arrow head
        s.text('LONGITUDINAL LOAD',max(rx-18,rx+35-s.measure('LONGITUDINAL LOAD',5.8)/2),378,5.8,a=.68,color=ARC)
    else:s.text('LONGITUDINAL LOAD',rx+35,378,5.8,a=.68,align='c',color=ARC)
    s.ln(rx-110,386,rx-28,363,.65,.7,color=ARC)
    s.poly([(rx-36,362),(rx-28,363),(rx-34,368)],.65,.7,close=False,color=ARC)
    s.text('02 / ALIGNED CNT BUNDLE',rx-170,409,6.3,a=.78)
    view(s,'tether-cnt-bundle',rx-20,466,233,85)
    # Deliberately no fabricated nanometre bar: these are schematic scale levels.
    s.view_label(rx,549,'C','RIBBON ARCHITECTURE','THICKNESS EXAGGERATED')
