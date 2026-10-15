"""A small architectural axonometric for Greener's neighbourhood arms race."""
import math,sys,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import family_core as g
from mathutils import Vector


def house(x,y,front,variant):
    # One consistent neighbourhood kit, with pitched standing-seam roofs.
    w=50;d=38;h=28
    g.softbox('rendered house walls',(x,y,h/2),(w,d,h),1.3)
    g.box('foundation',(x,y,1),(w+3,d+3,2),'detail')
    ridge=y+front*4
    vs=[(x+xx,y+yy,zz) for xx,yy,zz in [(-28,-22,h),(-28,front*4,h+13),(-28,22,h),(28,-22,h),(28,front*4,h+13),(28,22,h)]]
    g.mesh('pitched folded roof',vs,[(0,1,4,3),(1,2,5,4),(0,2,1),(3,4,5)])
    for xx in range(-24,26,7):
        g.wire('standing roof seam',[(x+xx,y-22,h+.2),(x+xx,ridge,h+13.2),(x+xx,y+22,h+.2)],.1,'shell')
    # Recessed front door, porch and two multi-light windows, all on the facade.
    fy=y+front*(d/2+.15)
    g.box('door frame',(x+12,fy,11),(10,.7,22),'detail')
    g.box('recessed door',(x+12,fy+front*.5,10.5),(7,.3,19),'shell')
    g.box('entrance steps',(x+12,fy+front*4,1.5),(14,8,3),'detail')
    g.box('door canopy',(x+12,fy+front*3,24),(16,8,1.2),'detail')
    for wx in (-15,-3):
        g.box('window reveal',(x+wx,fy,16),(9,.8,12),'detail')
        g.wire('window mullion',[(x+wx,fy+front*.6,10),(x+wx,fy+front*.6,22)],.10,'shell')
        g.wire('window sill',[(x+wx-5,fy+front*.7,10),(x+wx+5,fy+front*.7,10)],.12,'detail')
    # Side window and drainpipe lend depth without ornamental greebles.
    g.box('side window',(x+25.1,y,16),(.5,12,10),'detail')
    g.wire('rainwater downpipe',[(x+25.8,y-17,28),(x+26.8,y-17,25),(x+26.8,y-17,2)],.18,'detail')
    g.box('chimney',(x-13,y-8,37),(7,7,16),'detail')
    g.box('chimney cap',(x-13,y-8,45),(9,9,1.5),'detail')


def mast(x,y,first=False):
    h=21 if first else 24
    g.cyl('mast base',x,y,0,2.5,3,'detail',16)
    g.cyl('periscope',x,y,3,.85,h,'detail',12)
    g.softbox('optical head',(x,y,h+4),(6,4,4),1.3,'cable' if first else 'detail')
    g.along_y('camera lens',x,y-2,h+4,1.25,1,'accent',16)


def build():
    g.reset()
    # Eight lots, preserving the original street numbers and story.
    g.box('street cutaway',(0,0,-3),(337,342,6),'shell')
    g.box('road bed',(0,0,.15),(337,43,.3),'shell')
    for y in (-24,24):
        g.box('kerb',(0,y,1),(337,3,2),'detail')
        g.box('footway',(0,y+(5 if y>0 else -5),.4),(337,7,.8),'shell')
        for x in range(-162,164,14):g.wire('pavement joint',[(x,y,1),(x,y+(8 if y>0 else -8),1)],.08,'shell')
    for x in range(-162,165,20):g.wire('road centre dash',[(x,0,.7),(x+9,0,.7)],.10,'detail')
    for row in (0,1):
        side=1 if row==0 else -1;front=-side
        for k in range(4):
            no=2+k*4 if row==0 else 3+k*4
            x=-123+k*82; y=side*126; first=no==14;paved=no==7
            house(x,y,front,k)
            # Lot divisions are low fences, keeping the lawn visible.
            for xx in (x-38,x+38):
                for yy in (side*38,side*83,side*166):g.box('boundary post',(xx,yy,5),(1.5,1.5,10),'detail')
                for z in (3,8):g.wire('boundary rail',[(xx,side*38,z),(xx,side*166,z)],.12,'shell')
            g.wire('rear plot line',[(x-38,side*168,.4),(x+38,side*168,.4)],.10,'shell')
            # Front path reaches the same door as the house geometry.
            for xx in (x+6,x+18):g.wire('entrance path',[(xx,side*34,.6),(xx,side*103,.6)],.12,'detail')
            for yy in range(39,104,11):g.wire('path slab joint',[(x+6,side*yy,.6),(x+18,side*yy,.6)],.10,'shell')
            # A front strip remains open, with a break for the entry path.
            for xa,xb in [(x-37,x+5),(x+19,x+37)]:
                g.wire('low garden boundary',[(xa,side*35,4),(xb,side*35,4)],.16,'detail')
            if paved:
                # Staggered orthogonal paving is immediately distinct from turf.
                for yy in range(40,102,8):
                    g.wire('paving bed joint',[(x-34,side*yy,1),(x+4,side*yy,1)],.12,'detail')
                    for xx in range(-34+(4 if (yy//8)%2 else 0),5,12):
                        g.wire('paving cross joint',[(x+xx,side*yy,1),(x+xx,side*min(yy+8,103),1)],.10,'shell')
                for yy in range(40,102,8):g.wire('side paving',[(x+20,side*yy,1),(x+34,side*yy,1)],.10,'shell')
            else:
                # Individual bent blades at separated planting points, not hatch fill.
                for r in range(8):
                    for c in range(6):
                        xx=x-31+c*6.1+(r%2)*1.4;yy=side*(41+r*8)
                        for dx,dy,h in [(-1.2,.4,2.3),(.1,-.2,3.4),(1.2,.3,2.7)]:
                            g.wire('turf blade',[(xx+dx*t*t,yy+dy*t,1+h*t) for t in (0,.25,.5,.75,1)],.06,'fine')
                for r in range(7):
                    xx=x+26;yy=side*(43+r*9)
                    g.wire('side turf tuft',[(xx-1,yy,3),(xx,yy,1),(xx+1.3,yy,4)],.06,'fine')
                mast(x-27,side*86,first)
                g.box('wall controller',(x-21,y+front*20,7),(5,2,7),'cable' if first else 'detail')
            if first:
                # The founder's plot is picked out by its boundary, not a colour block.
                g.wire('first installation boundary',[(x-39,side*34,1),(x-39,side*169,1),(x+39,side*169,1),(x+39,side*34,1)],.14,'cable')
            # Labels are outside the projected scene, on separate gutters.
            g.mark(f'N{no}',(x,side*171,45 if row==0 else -3))
    for x in (-150,10,150):
        for y in (-22,22):
            g.box('storm drain',(x,y,.9),(8,2,.3),'detail')
            for xx in (-2,0,2):g.wire('drain slot',[(x+xx,y-1,1.2),(x+xx,y+1,1.2)],.06,'shell')
    g.export('greener-street',-12,58)


if __name__=='__main__':
    build();sys.stdout.flush();os._exit(0)
