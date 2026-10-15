"""New hardware for existing human/story compositions; pose geometry is untouched."""
import sys,os,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import family_core as g
T=math.tau
# A formed pendant housing with rolled rim and real concentric sensor pockets.
g.reset()
g.casting('pendant reflector',[(0,117,103),(4,124,109),(11,123,108),(17,115,100),(32,97,84),(56,63,53),(70,34,27),(75,18,16)],'structure')
for z,rx,ry in [(5,126,111),(13,121,106),(25,105,92)]:g.trim('reflector bead',z,rx,ry)
g.cyl('stem collar',0,0,76,15,10,'detail',48)
for k in range(12):
 a=T*k/12;x,y=103*math.cos(a),90*math.sin(a)
 g.cyl('thermal camera',x,y,-4,5,7,'accent',20)
 g.cyl('microphone aperture',x*.9,y*.9,0,2,3,'detail',12)
g.export('truth-lamp-head',0,8)
# Rounded articulated optical head: a compact periscope rather than a box.
g.reset();g.softbox('camera shell',(0,0,20),(51,27,26),10)
g.along_y('lens hood',0,-16,20,10,10,'structure',40);g.along_y('lens',0,-27,20,7,2,'accent',40)
g.cyl('pan pivot',0,0,0,8,9,'detail',32)
for x in (-14,-7,0,7,14):g.wire('head cooling slot',[(x,11,18),(x,11,25)],.5,'detail')
g.export('greener-head',50,12)
sys.stdout.flush();os._exit(0)
