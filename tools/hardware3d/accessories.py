"""Cast equipment outlines at the accepted anchors, independent of human poses."""
import math
from sheet import WHITE,ARC,GOLD
from hardware3d.family_drawing import data
from path_cleanup import trace

def rounded(s,x,y,w,h,r=7,a=.8,line=.7,fill=0,color=WHITE):
 r=min(r,w/2,h/2);c=s.c;c.new_path();c.move_to(x+r,y);c.line_to(x+w-r,y);c.arc(x+w-r,y+r,r,-math.pi/2,0);c.line_to(x+w,y+h-r);c.arc(x+w-r,y+h-r,r,0,math.pi/2);c.line_to(x+r,y+h);c.arc(x+r,y+h-r,r,math.pi/2,math.pi);c.line_to(x,y+r);c.arc(x+r,y+r,r,math.pi,math.pi*1.5);c.close_path()
 if fill:s._ink(fill,color);c.fill_preserve()
 s._stroke(a,line,None,color)

def model(s,name,x,y,w,h,flip=1):
 d=data(name);pts=[p for path in d['paths'] for p in path['points']];x0=min(p[0] for p in pts);x1=max(p[0] for p in pts);y0=min(p[1] for p in pts);y1=max(p[1] for p in pts)
 c=s.c;c.save();c.translate(x+(w if flip<0 else 0),y);c.scale(flip*w/(x1-x0),h/(y1-y0));c.translate(-x0,-y0)
 for path in d['paths']:
  trace(c,path)
  role=path['role'];s._stroke(.84 if role=='structure' else .56,.72 if role=='structure' else .4,None,ARC if role=='accent' else WHITE)
 c.restore()
