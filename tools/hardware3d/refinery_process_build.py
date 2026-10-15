"""Equipment symbols for the AR-1 concept flow sheet, projected from solids."""
import sys,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import family_core as g

g.reset()
for x in (-40,40):g.softbox('contactor end casting',(x,0,33),(8,37,59),4)
for z in (4,62):g.softbox('contactor beam',(0,0,z),(89,37,8),3)
for x in range(-32,38,7):g.softbox('sorbent lamella',(x,0,33),(2,31,49),.5)
g.beam('CO2 header',(-40,20,3),(40,20,3),4)
g.export('refinery-capture',25,20)

g.reset()
for x in (-43,43):g.softbox('electrolyser end plate',(x,0,22),(7,41,44),3)
for x in range(-36,40,7):g.softbox('cell plate',(x,0,22),(3,38,39),1)
for y in (-17,17):
 for z in (5,39):g.beam('tie rod',(-49,y,z),(49,y,z),1.5)
for y in (-12,12):g.beam('gas outlet',(46,y,26),(59,y,26),4,'accent')
g.export('refinery-electrolysis',25,20)

g.reset()
g.cyl('bed housing',0,0,4,24,65)
for z in (8,34,65):g.flange(0,0,z,28)
for z in (18,44):
 g.softbox('bed access',(0,-26,z+6),(19,8,13),4)
 g.dial(0,-32,z+6,4)
for x in (-17,17):g.beam('reactor foot',(x,0,-6),(x,0,6),3)
g.export('refinery-enzyme',27,18)

g.reset()
for x in (-19,19):
 g.cyl('catalyst cartridge',x,0,6,13,52)
 for z in (6,57):g.flange(x,0,z,16)
g.beam('feed manifold',(-23,0,68),(23,0,68),4)
for x in (-19,19):g.beam('cartridge feed',(x,0,61),(x,0,68),3)
g.beam('product header',(-19,0,0),(19,0,0),4)
g.export('refinery-catalysis',25,20)

g.reset()
g.beam('product receiver',(-36,0,22),(36,0,22),22,'structure',64)
for x in (-36,36):g.ball('dished end',(x,0,22),(6,22,22))
for x in (-23,23):g.softbox('tank saddle',(x,0,4),(8,39,9),3)
g.cyl('inspection neck',0,0,42,7,7);g.flange(0,0,49,10)
g.beam('fuel outlet',(30,-14,9),(30,-34,9),3,'accent')
g.export('refinery-product',25,20)
sys.stdout.flush();os._exit(0)
