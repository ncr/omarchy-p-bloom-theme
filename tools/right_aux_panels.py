"""Right-side spatial studies, with labels kept outside the drawing envelope."""
from sheet import WHITE, ARC, GOLD
from hardware3d.secondary_drawing import view


def compact_key(s,x,y,rows,per_col,limit,size=6.3,track=.07,lead=18):
    """Enlarged type (composed profiles): a numbered key with fixed gutters.

    rows are (number, label, colour) down the columns, per_col to a column. The gap from a number
    to its word and between the columns stays the same at every size; when two columns would
    run past limit, the key stacks in one."""
    off=s.measure('00',size,.06)+12
    lead=max(lead,s.readable_size(size)*1.55)
    cols=[rows[i:i+per_col] for i in range(0,len(rows),per_col)]
    widths=[off+max(s.measure(label,size,track) for _,label,_ in col) for col in cols]
    if x+sum(widths)+24*(len(cols)-1)>limit:
        cols=[rows];widths=[max(widths)]
    xx=x
    for col,w in zip(cols,widths):
        for i,(num,label,color) in enumerate(col):
            s.text(num,xx,y+i*lead,size,track=.06,a=.6)
            s.text(label,xx+off,y+i*lead,size,track=track,a=.86,color=color)
        xx+=w+24


def owner(s,rx):
    a=view(s,'proxy-sleeping-owner',rx,321,347,268)
    # Proxy's guide-runner story: the runner wakes; PX-1 has charged by the bed.
    cy=166
    if s.layer_mode:
        # Enlarged type: when the route line would run into the runner's label, the clock group
        # rises until the route sits clear above it.
        if rx-174+s.measure('HUMAN RUNNER',7,.09)+14>rx+169-s.measure('10.0 km / ROUTE LOADED',7,.07):
            cy=min(cy,170-.75*s.readable_size(7)-.5*s.readable_size(7)-18)
    s.text('05:40',rx+169,cy,18,track=.04,a=.9,align='r')
    s.text('10.0 km / ROUTE LOADED',rx+169,cy+18,7,track=.07,a=.85,align='r',color=ARC)
    s.text('HUMAN RUNNER',rx-174,170,7,track=.09,a=.85)
    x,y=a['HUMAN']
    g=s.type_growth(7)
    s.poly([(rx-145,179+g),(rx-145,192+g),(x,y)],.4,.5,close=False)
    s.dot(x,y,1.2,.65)
    s.text('PX-1 CHARGES BY THE BED; OUT AT 06:00',rx,480,6.4,a=.6,track=.11,align='c')
    s.view_label(rx,540,'C','THE RUNNER','AT HOME, BEFORE THE RUN')


def course(s,rx):
    a=view(s,'sky-racer-course',rx,318,348,314)
    # Number labels follow the projection but sit off each physical gate.
    offsets={1:(24,-18),2:(-8,-26),3:(-9,-24),4:(-15,-22),5:(-24,-5),6:(-24,14),7:(-10,28),8:(14,24),9:(90,-18)}
    for j in range(1,10):
        x,y=a[f'G{j}'];dx,dy=offsets[j]
        if dy>=24:dy+=.72*s.type_growth(7)  # enlarged numbers below a gate grow towards it
        s.text(f'{j:02}',x+dx,y+dy,7,track=.04,a=.9,align='c',color=ARC if j==1 else WHITE)
    # START / FINISH reads on from the accent 01, beside the gate it names.
    x,y=a['G1'];dx,dy=offsets[1]
    s.text('START / FINISH',x+dx+s.measure('01',7,.04)/2+6,y+dy,6.1,track=.08,a=.8,color=ARC)
    s.view_label(rx,548,'C','COURSE','9 GATES / 2.4 km / 30 – 180 m ABOVE GROUND')


def kidney(s,rx):
    a=view(s,'foundry-renal-section',rx,318,292,298)
    # Numbered leaders terminate in dedicated side gutters. The key below is
    # physically separate, so captions never sit on vessels or tissue hatching.
    for key,num,tx,ty in [('CORTEX','01',rx-170,210),('MEDULLA','02',rx-170,376),('SUPPLY','03',rx+170,261),('DRAIN','04',rx+170,444)]:
        x,y=a[key];side=-1 if tx<rx else 1
        s.poly([(x,y),(tx-side*17,ty-2),(tx-side*8,ty-2)],.48,.5,close=False)
        s.dot(x,y,1.3,.7)
        s.text(num,tx,ty,6.7,track=.05,a=.9,align='c')
    rows=[('01','CORTEX',WHITE),('02','MEDULLARY PYRAMIDS',WHITE),('03','VASCULAR SUPPLY',ARC),('04','COLLECTING SYSTEM',GOLD)]
    if s.layer_mode:
        compact_key(s,rx-171,490+s.type_growth(6.3),rows,2,rx+280)
    else:
        for (num,label,color),(x,y) in zip(rows,[(rx-171,490),(rx-171,508),(rx+8,490),(rx+8,508)]):
            s.text(num,x,y,6.3,track=.06,a=.6)
            s.text(label,x+21,y,6.3,track=.07,a=.86,color=color)
    s.view_label(rx,548,'C','RENAL SECTION','CORONAL CUTAWAY / AS PRINTED')


def node(s,rx):
    a=view(s,'cortical-node-exploded',rx-17,312,298,286)
    for key,num,ty in [('CONTACT','01',194),('WINDOW','02',267),('ROUTING','03',345),('CARRIER','04',422)]:
        x,y=a[key];tx=rx+169
        s.poly([(x,y),(tx-22,ty-2),(tx-8,ty-2)],.48,.5,close=False)
        s.dot(x,y,1.2,.7)
        s.text(num,tx,ty,6.7,track=.05,a=.9,align='c')
    # Numbered down the columns, like every other key in the collection.
    rows=[('01','POROUS CONTACT',WHITE),('02','PASSIVATION WINDOW',WHITE),('03','METAL ROUTING',GOLD),('04','FLEXIBLE CARRIER',WHITE)]
    if s.layer_mode:
        compact_key(s,rx-171,480+s.type_growth(6.3),rows,2,rx+280)
    else:
        x2=max(rx+8,rx-171+21+s.measure('PASSIVATION WINDOW',6.3,.07)+14)
        for (num,label,color),(x,y) in zip(rows,[(rx-171,480),(rx-171,498),(x2,480),(x2,498)]):
            s.text(num,x,y,6.3,track=.06,a=.6)
            s.text(label,x+21,y,6.3,track=.07,a=.86,color=color)
    s.view_label(rx,540,'C','ONE NODE','EXPLODED FILMS / THICKNESS EXAGGERATED')


def street(s,rx):
    a=view(s,'greener-street',rx,324,348,324)
    for no in (2,6,10,14,3,7,11,15):
        x,y=a[f'N{no}'];dy=-12 if no%2==0 else 14
        s.text(str(no),x,y+dy,7,track=.06,a=.9,align='c',color=GOLD if no==14 else WHITE)
    s.text('14 / FIRST INSTALLATION',rx-174,518,6.2,track=.07,a=.8,color=GOLD)
    s.text('7 / LAWN PAVED OVER',rx+12,518,6.2,track=.07,a=.8)
    s.view_label(rx,552,'C','THE STREET, YEAR SIX','No. 14 BOUGHT THE FIRST ONE. No. 7 PAVED THE LAWN.')
