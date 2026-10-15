"""Authored left-side explanatory studies; all keys live outside geometry."""
import math
from sheet import WHITE,ARC,GOLD,RED
from hardware3d.secondary_drawing import view


def tissue(s,lx):
    a=view(s,'cortical-tissue-section',lx,296,322,294)
    for key,num,side,y in [('SCALP','01',-1,189),('SKULL','02',-1,252),('MENINGES','03',-1,317),('IMPLANT','06',1,193),('CORTEX','04',1,351),('WHITE','05',1,409)]:
        x0,y0=a[key];x=lx+side*201
        s.poly([(x0,y0),(x-side*20,y-2),(x-side*8,y-2)],.46,.5,close=False)
        s.dot(x0,y0,1.2,.7);s.text(num,x,y,6.7,track=.04,a=.9,align='c')
    items=[('01','SCALP',-191,458),('02','SKULL',-191,477),('03','MENINGEAL ENVELOPE',-191,496),('04','CORTEX / I–VI',24,458),('05','WHITE MATTER',24,477),('06','IMPLANT + MESH',24,496)]
    if s.layer_mode:
        from right_aux_panels import compact_key
        compact_key(s,lx-191,458+s.type_growth(6.2),[(num,label,ARC if num=='06' else WHITE) for num,label,_,_ in items],3,lx+300,size=6.2,track=.06,lead=19)
    else:
        for num,label,dx,y in items:
            s.text(num,lx+dx,y,6.2,track=.06,a=.6)
            s.text(label,lx+dx+22,y,6.2,track=.06,a=.86,color=ARC if num=='06' else WHITE)
    s.view_label(lx,541,'B','IMPLANT SECTION','TISSUE DETAIL ENLARGED')


def dinner(s,lx):
    a=view(s,'truth-dinner-seating',lx,282,348,266)
    # Seat identifiers lead to chairs; totals never sit over dishes or furniture.
    labels=[(1,-199,302),(2,-85,171),(3,81,154),(4,198,245),(5,100,410),(6,-66,430)]
    for idx,dx,y in labels:
        x0,y0=a[f'S{idx}'];x=lx+dx
        vx,vy=x0-x,y0-(y-2.5);length=math.hypot(vx,vy)
        endpoint=(x+vx/length*9,y-2.5+vy/length*9)
        s.poly([(x0,y0),endpoint],.42,.45,close=False)
        s.dot(x0,y0,1.1,.65)
        s.text(f'{idx:02}',x,y,6.7,track=.04,a=.9,align='c',color=ARC if idx==1 else RED if idx==4 else WHITE)
    records=[('01','GRANDMOTHER',0,-194,462),('02','UNCLE',14,-194,482),('03','AUNT',9,-194,502),('04','HOST',22,23,462),('05','GUEST',17,23,482),('06','TEENAGER',11,23,502)]
    for num,name,count,dx,y in records:
        color=ARC if count==0 else RED if count>=20 else WHITE
        s.text(num,lx+dx,y,6.2,track=.06,a=.6)
        s.text(name,lx+dx+22,y,6.2,track=.08,a=.85)
        s.text(str(count),lx+dx+167,y,8,track=0,a=.95,align='r',bold=True,color=color)
    s.view_label(lx,546,'B','ONE DINNER','UNTRUTHS DETECTED, BY SEAT')
