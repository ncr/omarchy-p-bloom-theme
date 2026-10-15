"""Tether system hardware and hierarchical CNT ribbon, authored review geometry."""
import sys,os,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import family_core as g
from mathutils import Vector

def anchor():
    g.reset()
    for x in (-66,66):
        g.softbox('semi-submersible pontoon',(x,0,-27),(32,152,26),12)
        for y in (-45,45):g.cyl('buoyancy column',x,y,-27,10,51)
    g.softbox('rounded platform deck',(0,0,25),(181,139,12),10)
    for x in (-79,79):
        for y in range(-56,57,28):g.beam('rail stanchion',(x,y,31),(x,y,44),1)
        g.beam('deck handrail',(x,-56,44),(x,56,44),1)
    for x in (-17,17):
        for y in (-15,15):
            g.beam('anchor gantry leg',(x*1.4,y*1.6,31),(x,y,101),3)
        g.beam('gantry bracing',(x,-20,45),(x,15,88),1.6)
    g.softbox('tether guide head',(0,0,102),(49,39,17),5)
    g.box('tether through guide',(0,0,122),(12,2,25),'accent')
    for y in (-14,14):g.beam('traction guide roller',(-15,y,95),(15,y,95),6)
    g.softbox('plant cabin',(-57,12,45),(39,48,30),6)
    for z in range(36,58,4):g.wire('cabin vents',[(-78,-6,z),(-78,26,z)],.45,'detail')
    g.cyl('laser mount',49,-24,31,14,9)
    g.beam('beam telescope',(49,-24,42),(37,-17,77),10)
    g.beam('telescope rim',(37,-17,77),(36,-16.4,80),11,'accent')
    g.cyl('service radome foot',54,38,31,9,7)
    g.ball('radome',(54,38,44),(13,13,11))
    for x in (-44,0,44):g.wire('deck panel joint',[(x,-63,31.2),(x,63,31.2)],.4,'detail')
    g.export('tether-ocean-anchor',27,22)

def station():
    g.reset()
    for x in (-32,32):
        g.beam('pressurised service module',(x,-18,0),(x,19,0),11)
        g.beam('module hatch',(x,-21,0),(x,-18,0),8,'accent')
        g.beam('connecting tunnel',(x,0,0),(x*.2,0,0),5)
        for y in (-10,10):g.beam('transfer cradle',(x,y,-12),(0,y,-19),1.8)
    g.softbox('central ribbon guide',(0,0,0),(13,18,46),3)
    g.box('continuous ribbon',(0,0,0),(5,1,90),'accent')
    for sign in (-1,1):
        g.beam('array boom',(sign*32,0,0),(sign*72,0,0),1.8)
        g.box('solar wing',(sign*67,0,0),(36,48,1))
        for x in range(52,84,6):g.wire('solar cell columns',[(sign*x,-24,1),(sign*x,24,1)],.25,'fine')
        for y in range(-18,24,6):g.wire('solar cell rows',[(sign*49,y,1),(sign*85,y,1)],.25,'fine')
    g.export('tether-geo-station',23,20)

def counterweight():
    g.reset()
    for x in (-21,21):
        for y in (-14,14):g.beam('counterweight truss chord',(x,y,-39),(x,y,39),1.5)
    for z in (-38,-13,13,38):
        for x in (-21,21):g.beam('cross brace',(x,-14,z),(x,14,z+24 if z<38 else z),1)
    for z in (-25,0,25):g.softbox('ballast cassette',(0,0,z),(35,24,18),4)
    g.beam('tether termination',(0,0,-61),(0,0,-38),3,'accent')
    for sign in (-1,1):g.beam('trim thruster',(sign*22,0,27),(sign*31,0,27),4)
    g.export('tether-counterweight',27,20)

def ribbon():
    g.reset()
    # Three peeled sheet strata. Thickness and separation are exaggerated.
    for layer in range(3):
        length=245-layer*29;z0=layer*8
        def point(x,y):
            t=max(0,(x-5)/(length/2-5))
            return Vector((x,y,z0+(layer*17)*t*t))
        n=45;vs=[]
        for dz in (0,2.5):
            for y in (-49,49):
                for j in range(n+1):
                    p=point(-length/2+length*j/n,y);p.z+=dz;vs.append(p)
        m=n+1;faces=[]
        for j in range(n):faces.extend([(j,j+1,m+j+1,m+j),(2*m+j,3*m+j,3*m+j+1,2*m+j+1),(j,2*m+j,2*m+j+1,j+1),(m+j,m+j+1,3*m+j+1,3*m+j)])
        faces.extend([(0,m,3*m,2*m),(n,2*m+n,3*m+n,m+n)])
        g.mesh('CNT sheet stratum',vs,faces)
        for y in range(-45,49,6):
            pts=[]
            for j in range(n+1):
                x=-length/2+length*j/n;p=point(x,y+.4*math.sin(x/26+y));p.z+=2.8;pts.append(p)
            g.wire('aligned bundle texture',pts,.22,'detail')
        # Interrupted end face exposes the aligned longitudinal sub-bundles.
        for y in range(-45,49,6):
            p=point(-length/2,y)+Vector((0,0,1.2))
            g.beam('bundle end',p-Vector((1,0,0)),p,1.05,'detail',12)
    g.export('tether-ribbon-laminate',-33,26)

def bundle():
    g.reset()
    # A handful of hollow tubes stand for a much larger aligned CNT bundle.
    # Separate tubular walls avoid depicting solid rods or graphene sheets.
    for row in range(3):
        for col in range(5-row):
            y=(col-(4-row)/2)*9;z=row*7.8
            length=103+((col*7+row*11)%19)
            n=40;vs=[]
            for x in (-length/2,length/2):
                for r in (2.5,3.4):
                    for k in range(n):vs.append((x,y+r*math.cos(math.tau*k/n),z+r*math.sin(math.tau*k/n)))
            fs=[]
            for k in range(n):
                j=(k+1)%n;fs.extend([(k,j,2*n+j,2*n+k),(n+k,3*n+k,3*n+j,n+j),(k,n+k,n+j,j),(2*n+k,2*n+j,3*n+j,3*n+k)])
            g.mesh('hollow CNT',vs,fs,'accent' if row==2 else 'structure')
    g.export('tether-cnt-bundle',-38,24)

for build in (anchor,station,counterweight,ribbon,bundle):build()
sys.stdout.flush();os._exit(0)
