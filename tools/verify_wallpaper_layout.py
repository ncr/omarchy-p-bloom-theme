"""Audit glyph bounds against a render without text, before grain/bloom.

Grid/frame are the comparison baseline. Intentional identifiers inside their
own filled symbols are listed explicitly; no callout or legend is exempt.
Run from the repository root. Output includes every measured text string.
"""
import argparse,json,math,sys
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--size',default='5120x2160');ap.add_argument('--source',default='tools');ap.add_argument('--out',required=True);ap.add_argument('--style',default='starmap',choices=['starmap','original'])
ap.add_argument('--profile',help='audit a composed release profile (all 42 sheets) instead, e.g. 16x9-1080p')
ap.add_argument('--level',default='default',choices=['muted','default','vivid'],help='ground level (tools/ground_levels.py)');args=ap.parse_args()
sys.path.insert(0,str(Path('tools').resolve()));sys.path.insert(0,str(Path(args.source).resolve()))
from sheet import Sheet as _Sheet;_Sheet.ground_level=args.level
import ground_levels
if args.profile:
    # Composed profiles: same checks on final pixels (tools/aspect_layout.audit),
    # plus type floor, clipped labels and one A/B/C per placed view.
    import aspect_layout
    comp=aspect_layout.composition(args.profile);report=[]
    for item in aspect_layout.collection():
        r,_=aspect_layout.audit(item,comp);report.append(r)
        print(item['id'],'min',r['min_text_px'],'contrast',{k:v['ratio'] for k,v in r['contrast'].items()},'dropped',r['dropped'],'issues',r['issues'],flush=True)
    Path(args.out).write_text(json.dumps({'profile':args.profile,'level':args.level,'size':comp.size,'floor_px':comp.floor_px,'sheets':report},indent=2)+'\n')
    sys.exit(1 if any(r['issues'] for r in report) else 0)
import devices,foibles,leisure
from sheet import Sheet
from order import ORDER
size=tuple(map(int,args.size.split('x')));width,height=size
if abs(width/height-16/9)<.01:Sheet.side_inset=150
original_start=devices.start;original_leader=Sheet.leader;original_legend=Sheet.legend
labels=[];kind='text'
def text(self,t,x,y,size=8,track=.22,a=.7,align='l',bold=False,color=(.95,.965,.98),rot=0):
    size=self.readable_size(size)
    glyphs=self._glyphs(t,size);adv=self._advances(glyphs,bold)
    w=sum(adv)+track*size*(len(glyphs)-1)
    px=-{'l':0,'r':w,'c':w/2}[align];m=self.c.get_matrix();m.translate(x,y);m.rotate(math.radians(rot));pts=[]
    for (ch,fs,dy),aw in zip(glyphs,adv):
        self.c.set_font_size(fs);e=self.c.text_extents(ch)
        if e.width and e.height:
            pts += [m.transform_point(u,v) for u in (px+e.x_bearing,px+e.x_bearing+e.width) for v in (dy+e.y_bearing,dy+e.y_bearing+e.height)]
        px+=aw+track*size
    if getattr(self,'triptych',False):a=max(a,.60)
    if pts:labels.append({'text':t,'kind':kind,'ink':[*map(float,color),float(a)],'font_px':round(size*math.hypot(m.xy,m.yy),3),'box':[min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts),max(p[1] for p in pts)]})
    return w
def leader(self,*a,**kw):
    global kind
    before=kind;kind='callout';original_leader(self,*a,**kw);kind=before
def text_mid(self,t,x,y_mid,size=8,track=.22,a=.7,align='l',bold=False,color=(.95,.965,.98)):
    size=self.readable_size(size)
    # Sheet.text_mid draws centred single glyphs directly. Capture those too,
    # including the boxed A/B/C identifiers, at their actual ink coordinates.
    import cairo
    from sheet import FONT
    self.c.select_font_face(FONT,cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    self.c.set_font_size(size);cap=-self.c.text_extents('H').y_bearing
    if len(t)==1 and align=='c':
        e=self.c.text_extents(t)
        return text(self,t,x-(e.x_bearing+e.width/2),y_mid+cap/2,size,0,a,'l',bold,color)
    return text(self,t,x,y_mid+cap/2,size,track,a,align,bold,color)
def legend(self,*a,**kw):
    global kind
    before=kind;kind='legend';original_legend(self,*a,**kw);kind=before
def start(*a,**kw):
    s=original_start(*a,**kw);s.surface.flush()
    s._audit_base=np.frombuffer(s.surface.get_data(),np.uint8).reshape(height,width,4).copy()
    labels.clear();return s
Sheet.text=text;Sheet.text_mid=text_mid;Sheet.leader=leader;Sheet.legend=legend
devices.start=start;foibles.start=start;leisure.start=start
inside_own_symbol={
 'air-refinery':{'AIR','CONTACTOR','WATER','ELECTROLYSER','SUNLIGHT','RECEIVER','ENZYME BEDS','CATALYST BEDS','JET FUEL'},
 'truth-lamp':{'14','9','0','22','17','11'},
 'organ-foundry':{'1','2','3','4','5','6'},
 'proxy':{'114','CITY 10K'},
}
fns=dict(devices.SHEETS+foibles.SHEETS+leisure.SHEETS);report=[];main_titles={}
if args.style=='starmap':
    from starmap import install
    install()
for name,_ in ORDER:
    labels=[];s=fns[name](size);s.surface.flush()
    arr=np.frombuffer(s.surface.get_data(),np.uint8).reshape(height,width,4)
    mask=np.abs(arr[:,:,:3].astype(np.int16)-s._audit_base[:,:,:3].astype(np.int16)).max(axis=2)>5
    issues=[];intentional=[];out_of_bounds=[]
    for t in labels:
        x0,y0,x1,y1=t['box']
        if x0<0 or y0<0 or x1>width or y1>height:out_of_bounds.append(t)
        hits=int(mask[max(0,math.floor(y0)):min(height,math.ceil(y1)),max(0,math.floor(x0)):min(width,math.ceil(x1))].sum())
        if hits:
            item=dict(t,geometry_pixels=hits)
            if t['kind']=='text' and t['text'] in inside_own_symbol.get(name,set()):intentional.append(item)
            else:issues.append(item)
    pairs=[]
    for i,a in enumerate(labels):
        for b in labels[i+1:]:
            if a['box'][0]<b['box'][2] and a['box'][2]>b['box'][0] and a['box'][1]<b['box'][3] and a['box'][3]>b['box'][1]:pairs.append([a['text'],b['text']])
    view_counts={letter:sum(t['text']==letter for t in labels) for letter in 'ABC'}
    expected={'A':1,'B':int(s.wide),'C':int(s.wide)}
    view_issues=[f'{letter}: expected {count}, found {view_counts[letter]}' for letter,count in expected.items() if view_counts[letter]!=count]
    if getattr(s,'triptych',False):
        from triptych import audit_slots
        view_issues.extend(audit_slots(s,labels))
    notes=[t for t in labels if t['text'].startswith('FIELD NOTES / ')]
    if len(notes)!=1:view_issues.append(f'Expected one FIELD NOTES block, found {len(notes)}')
    from collection_layout import signature_box
    nx0,ny0,nx1,ny1=s.field_notes_bounds
    ex,ey,er=signature_box(s)
    if nx0<ex+er and nx1>ex-er and ny0<ey+er and ny1>ey-er:
        view_issues.append('Field notes collide with signature region')
    contrast=ground_levels.text_contrast(labels,ground_levels.bgra_rgb(s._bg,width,height),
        None if args.level=='default' else ground_levels.reference_ground(s))
    view_issues.extend(ground_levels.contrast_issues(contrast,getattr(s,'ground',None)))
    main_caption=next((labels[i+1]['text'] for i,t in enumerate(labels[:-1]) if t['text']=='A'),None)
    if main_caption:
        key=main_caption.casefold()
        if key in main_titles:view_issues.append(f'A caption duplicates {main_titles[key]}: {main_caption}')
        main_titles[key]=name
        if set(main_caption.upper().split()) & {'ASSEMBLY','CONFIGURATION','UNIT'}:
            view_issues.append(f'Generic A caption: {main_caption}')
    else:view_issues.append('A caption is missing')
    report.append({'name':name,'illustration_layout':s.illustration_layout,'section_layout':s.section_layout,'legend_top':s.legend_top,'field_notes_bounds':s.field_notes_bounds,'geometry_collisions':issues,'text_collisions':pairs,'out_of_bounds':out_of_bounds,'view_label_counts':view_counts,'view_label_issues':view_issues,'main_caption':main_caption,'contrast':ground_levels.summary(contrast),'intentional_symbol_fills':intentional,'texts':labels})
    print(name,'geometry:',[(t['text'],t['geometry_pixels']) for t in issues],'text:',pairs,'outside:',len(out_of_bounds),'views:',view_counts,'view issues:',view_issues,flush=True)
Path(args.out).write_text(json.dumps({'size':size,'level':args.level,'threshold':5,'sheets':report},indent=2)+'\n')
if any(s[k] for s in report for k in ('geometry_collisions','text_collisions','out_of_bounds','view_label_issues')):
    sys.exit(1)
