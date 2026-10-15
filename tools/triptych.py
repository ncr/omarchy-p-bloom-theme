"""Shared three-column anatomy, authored auxiliary fitting, and explanatory diagrams."""
from contextlib import contextmanager
import cairo
import math
from sheet import WHITE, ARC
from collection_layout import ORIGINAL


def extra(s):return max(0,s.H-1080)


def caption_y(s,side=None):
    if side in getattr(s,'illustration_layout',{}):
        return s.illustration_layout[side]['caption_y']
    return 411+extra(s)*.35


@contextmanager
def measured_illustration(s,side):
    """Measure actual vector ink, including component annotations, not its slot.

    Recording keeps the existing vector geometry/scale. Text bounds are also
    measured explicitly so text-free collision audits use the same caption Y.
    """
    old=s.c;oldtext=s.text;record=cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA,None)
    c=cairo.Context(record);c.set_matrix(old.get_matrix())
    c.set_line_cap(old.get_line_cap());c.set_line_join(old.get_line_join())
    c.set_font_face(old.get_font_face());c.set_font_options(old.get_font_options())
    s.c=c;bounds=[]
    def text(t,x,y,size=8,track=.22,a=.7,align='l',bold=False,color=WHITE,rot=0):
        fs=s.readable_size(size);glyphs=s._glyphs(t,fs);adv=s._advances(glyphs,bold)
        w=sum(adv)+track*fs*(len(glyphs)-1);px=-{'l':0,'r':w,'c':w/2}[align]
        m=s.c.get_matrix();m.translate(x,y);m.rotate(math.radians(rot))
        for (ch,z,dy),aw in zip(glyphs,adv):
            s.c.set_font_size(z);e=s.c.text_extents(ch)
            if e.width and e.height:
                bounds.extend(m.transform_point(u,v) for u in (px+e.x_bearing,px+e.x_bearing+e.width) for v in (dy+e.y_bearing,dy+e.y_bearing+e.height))
            px+=aw+track*fs
        return oldtext(t,x,y,size,track,a,align,bold,color,rot)
    s.text=text
    try:yield
    finally:
        s.text=oldtext;s.c=old
        x,y,w,h=record.ink_extents();bounds.extend(((x,y),(x+w,y+h)))
        bottom=max(p[1] for p in bounds)/s.s
        if not hasattr(s,'illustration_layout'):s.illustration_layout={}
        s.illustration_layout[side]={'ink_bounds':[min(p[0] for p in bounds)/s.s,min(p[1] for p in bounds)/s.s,max(p[0] for p in bounds)/s.s,bottom], 'caption_y':bottom+30}
        old.save();old.identity_matrix();old.set_source_surface(record,0,0);old.paint();old.restore()


def diagram_y(s,side,height=188):
    if side=='right':return 552+extra(s)*.63
    # The legend's actual typeset height determines the lower breathing room.
    return min(546+extra(s)*.63,s.legend_top-40-height)


def register_section(s,side,top,bottom):
    if not hasattr(s,'section_layout'):s.section_layout={}
    s.section_layout[side]={'divider':top,'bottom':bottom}


def punchline(s,text):
    # Easter egg, anchored to the physical centre rather than illustration centre.
    s.text(text,s.W/2,s.H-84,6.3,track=.06,a=.40,align='c',color=WHITE)
    s.punchline_text=text
    s.punchline_anchor=(s.W/2,s.H-84)


def audit_slots(s,labels):
    """Check required content against text captured by the native layout audit."""
    issues=[]
    small=[t['text'] for t in labels if t.get('font_px',14)<13.99]
    if small:issues.append({'unreadable_type':small})
    title=getattr(s,'legend_title',None)
    if not title or sum(t['text']==title for t in labels)!=1:
        issues.append('The wallpaper title must occur once, in the lower-left legend')
    if getattr(s,'diagram_slots',set())!={'left','right'}:
        issues.append('Both side columns require a diagram')
    # Loose main-view context is collected beneath the Field Notes rows.
    for note in getattr(s,'main_context_notes',()):
        found=[t for t in labels if t['text']==note]
        if len(found)!=1:
            issues.append('Expected one dossier context line: '+note)
        elif found[0]['box'][0] < (s.W-670)*s.s-2:
            issues.append('Main-view context must stay in the right dossier: '+note)
    punch=getattr(s,'punchline_text',None)
    if not punch or sum(t['text']==punch for t in labels)!=1:
        issues.append('Expected exactly one Easter egg')
    if getattr(s,'punchline_anchor',None)!=(s.W/2,s.H-84):
        issues.append('Easter egg must sit at the bottom centre')
    for letter in 'ABC':
        if sum(t['text']==letter for t in labels)!=1:
            issues.append(f'Expected one {letter} view in both formats')
    for side,box in getattr(s,'section_layout',{}).items():
        gap=box['divider']-(caption_y(s,side)+16)
        footer=s.legend_top if side=='left' else s.field_notes_bounds[1]
        if gap<30:issues.append(f'{side}: caption/next-section gap is {gap:.1f}')
        if footer-box['bottom']<38:issues.append(f'{side}: diagram/footer gap is {footer-box["bottom"]:.1f}')
        ink=getattr(s,'illustration_layout',{}).get(side)
        if not ink:issues.append(f'{side}: missing actual illustration bounds')
        else:
            own_gap=ink['caption_y']-11-ink['ink_bounds'][3]
            if not 18<=own_gap<=24:issues.append(f'{side}: detached caption, ink gap {own_gap:.1f}')
            if gap<own_gap*2:issues.append(f'{side}: caption is not grouped with its own illustration')
    if set(getattr(s,'section_layout',{}))!={'left','right'}:
        issues.append('Both column spacing measurements are required')
    return issues


def diagram(s,side):
    from subject_diagrams import draw
    draw(s,side)


@contextmanager
def auxiliary_panel(s,slot,lx,rx):
    """Fit original authored vector helpers into a shared side-view envelope.

    The caption is moved out of the scaled drawing, keeping its typography
    identical to new Century views. No raster clipping or text erasure.
    """
    ex=extra(s);old_label=s.view_label;captions=[]
    if slot=='B':
        source=(lx-290,115,lx+320,555)
        if s.subject=='tether-climber':source=(lx-220,130,lx+250,665)
        if s.subject=='bounder':source=(lx-260,115,lx+290,630)
        target=(110,96+ex*.10,670,386+ex*.35)
    elif slot=='C':
        source=(rx-275,115,rx+300,555)
        if s.subject=='fusion-transport':source=(rx-260,70,rx+340,440)
        if s.subject=='air-refinery':source=(rx-270,140,rx+270,620)
        target=(s.W-680,96+ex*.10,s.W-130,386+ex*.35)
    else:
        source=(rx-225,565,rx+225,805)
        target=(s.W-650,542+ex*.63,s.W-160,758+ex*.75)
    x0,y0,x1,y1=source;a,b,c,d=target
    k=min((c-a)/(x1-x0),(d-b)/(y1-y0))
    s.c.save();s.c.translate((a+c)/2,(b+d)/2);s.c.scale(k,k);s.c.translate(-(x0+x1)/2,-(y0+y1)/2)
    def capture(x,y,letter,name,scale=None,align='c'):
        captions.append((letter,name,scale))
    if slot!='plot':s.view_label=capture
    try:
        if slot=='plot':yield
        else:
            with measured_illustration(s,'left' if slot=='B' else 'right'):yield
    finally:
        s.view_label=old_label;s.c.restore()
    if captions:
        for letter,name,scale in captions:
            old_label((a+c)/2,caption_y(s,'left' if slot=='B' else 'right'),letter,name,scale)
    if slot=='plot':
        s.diagram_slots=getattr(s,'diagram_slots',set())|{'right'}
        s.ln(a,b-46,c,b-46,.19,.45)
        register_section(s,'right',b-46,d)


def original_diagrams(s):
    diagram(s,'left')
    if s.subject=='tether-climber':diagram(s,'right')
