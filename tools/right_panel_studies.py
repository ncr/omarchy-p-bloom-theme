"""Legible field records and a concept process flow sheet."""
from sheet import WHITE,ARC,GOLD,RED
from hardware3d.secondary_drawing import view


def truth(s,rx):
    left=rx-176;right=rx+176
    s.text('MOST DETECTED SENTENCES',left,125,8.3,a=.94,track=.16)
    s.text('SHARE OF ALL DETECTIONS',left,145,6,a=.6)
    rows=[("“IT'S DELICIOUS”",31),
          ('“WE SHOULD DO THIS MORE OFTEN”',22),
          ("“I'M FINE”",19),
          ('“NO, YOU CHOOSE”',11),
          ('“TRAFFIC WAS TERRIBLE”',9),
          ('“I WAS JUST ABOUT TO CALL YOU”',8)]
    for i,(line,value) in enumerate(rows):
        y=177+i*60
        s.text(line,left,y,9.4,track=.07,a=.96)
        s.text(f'{value} %',right,y+7,12.5,track=.03,a=.96,align='r',color=RED if i==0 else WHITE)
        by=y+28;length=352*value/35
        s.ln(left,by+4,right,by+4,.22,.45)
        s.rect(left,by,length,8,.72,.65,fill=.16,color=RED if i==0 else ARC)
        for v in range(5,value,5):
            x=left+352*v/35;s.ln(x,by,x,by+8,.4,.4)
    s.view_label(left,548,'C','FIELD DATA','11 000 DINNERS, BEFORE THE RETURNS BEGAN',align='l')


def refinery(s,rx):
    a=rx-97;b=rx+109
    # Enlarged type (composed profiles): names under a drawing move down by their growth, and the
    # second line of a two-line label keeps its leading. Zero in the masters.
    g=s.type_growth
    s.text('CARBON PATH',a,112,6.6,a=.82,align='c')
    s.text('HYDROGEN PATH',b,112,6.6,a=.82,align='c')
    s.text('AIR',a,148,7,a=.85,align='c')
    s.text('WATER',b,148,7,a=.85,align='c')
    view(s,'refinery-capture',a,192,106,66)
    view(s,'refinery-electrolysis',b,192,111,66)
    s.text('CONTACTOR',a,239+g(6.5),6.5,a=.83,align='c')
    s.text('ELECTROLYSER',b,239+g(6.5),6.5,a=.83,align='c')
    # Material streams bend around equipment captions rather than through them
    # (and clear the captions' enlarged width in the composed profiles).
    ca=min(a-69,a-s.measure('CONTACTOR',6.5)/2-10);cb=min(b-66,b-s.measure('ELECTROLYSER',6.5)/2-10)
    s.poly([(a-58,193),(ca,193),(ca,281),(a,281)],.8,.8,close=False,color=ARC)
    s.arrow(a,281,a,300,.8,.8,head=4,color=ARC)
    s.text('CO₂',a-58,272,7,a=.9,color=ARC)
    view(s,'refinery-enzyme',a,336,72,69)
    s.text('ENZYME BEDS',a+54,325,7,a=.9)
    s.text('CARBON FIXATION',a+54,341+g(5.8),5.8,a=.6)
    s.arrow(a,373,a,409,.8,.8,head=4,color=ARC)
    s.text('INTERMEDIATES',a+13,391,5.5,a=.67)
    view(s,'refinery-catalysis',a,443,77,67)
    s.text('CATALYST BEDS',a+54,447,7,a=.9)
    s.text('CHAIN BUILDING',a+54,463+g(5.8),5.8,a=.6)
    # H2 joins the synthesis feed, independently of the captured-carbon leg.
    s.poly([(b-58,194),(cb,194),(cb,267),(b+52,267),(b+52,401),(a,401)],.76,.8,close=False,color=ARC)
    s.arrow(a+38,401,a,401,.76,.8,head=4,color=ARC)
    s.text('H₂',b+37,293,7,a=.9,align='r',color=ARC)
    s.arrow(b+57,185,b+78,185,.55,.6,head=4)
    s.text('O₂',b+86,178,6,a=.65)
    s.arrow(a,480,a,512,.85,.9,head=4,color=GOLD)
    view(s,'refinery-product',a,537,95,57)
    s.text('JET FUEL',a+66,533,8,a=.95,color=GOLD)
    s.text('PRODUCT RECEIVER',a+66,550+g(5.7),5.7,a=.65)
    # Utilities never share the material pipeline. They remain schematic.
    s.ln(rx-189,156,rx-189,451,.5,.65,dash=[5,3],color=GOLD)
    for y,end in [(179,a-56),(330,a-42),(443,a-45)]:
        s.ln(rx-189,y,end,y,.5,.65,dash=[5,3],color=GOLD)
    s.poly([(rx-189,156),(rx-189,129),(b+74,129),(b+74,205),(b+58,205)],.5,.65,close=False,dash=[5,3],color=GOLD)
    # Key: each sample line keeps its full length and its gap to the word at every type size.
    ky=593+g(5.5);x=rx-179;L=32+4*g(5.5)
    s.ln(x,ky-3,x+L,ky-3,.65,.7,color=ARC)
    w=s.text('MATERIAL',x+L+8,ky,5.5,a=.75)
    x=max(rx-39,x+L+8+w+28)
    s.ln(x,ky-3,x+L,ky-3,.6,.65,dash=[5,3],color=GOLD)
    s.text('SOLAR HEAT / POWER',x+L+8,ky,5.5,a=.75)
    s.view_label(rx,622,'C','PROCESS','AIR AND WATER TO JET FUEL')
