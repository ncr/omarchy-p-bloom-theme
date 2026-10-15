"""Bounder's sprint application view, projected from one equipped 3-D dummy."""
from projected_dummy import geometry,draw as draw_dummy
from sheet import ARC,WHITE


def draw(s,lx):
    d=geometry('bounder')
    points=[p for path in d['paths'] for p in path['points']]
    x0=min(x for x,y in points);x1=max(x for x,y in points)
    y0=min(y for x,y in points);y1=max(y for x,y in points)
    scale=min(355/(x1-x0),345/(y1-y0))
    ox=lx-(x0+x1)*scale/2;oy=300-(y0+y1)*scale/2
    draw_dummy(s,'bounder',ox,oy,scale=scale,stroke_scale=.7/scale)
    # Both blades clear the ground: this is a sprint flight phase, not a stance.
    ground=494
    s.ln(lx-180,ground,lx+185,ground,.42,.55)
    for u in range(-175,185,12):s.ln(lx+u,ground,lx+u-6,ground+7,.25,.4)
    y=101
    if s.layer_mode and s.measure('HUMAN ATHLETE*',6.7)+s.measure('B-4 / PAIRED ASSIST',6.2)+14>360:
        y-=s.readable_size(6.7)*.72+7  # enlarged type: stack the two labels
    s.text('HUMAN ATHLETE*',lx-180,y,6.7,a=.8)
    s.text('B-4 / PAIRED ASSIST',lx+180,101,6.2,a=.72,align='r',color=ARC)
    s.ln(lx+90,117,lx+177,117,.55,.65)
    s.poly([(lx+170,114),(lx+177,117),(lx+170,120)],.55,.65,close=False)
    s.view_label(lx,527,'B','ASSISTED SPRINT','FLIGHT PHASE / B-4 WORN ON BOTH LEGS')
    s.text('* HUMAN INSIDE. NO AUTOPILOT.',lx,563,5.8,a=.62,align='c')
