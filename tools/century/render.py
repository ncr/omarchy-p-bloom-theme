#!/usr/bin/env python3
"""Native-size Century sheets. All lettering remains deterministic Cairo type."""
import sys,json,math,time,argparse,os
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from sheet import Sheet,WHITE,ARC,GOLD
from starmap_study import StudySheet
from PIL import Image
from century.registry import update
ASSETS=ROOT/'tools/assets/century';CAT=ROOT/'docs/century/catalog.json';OUT=ROOT/'concepts/century'

class CenturySheet(StudySheet):
    def primary_focus(self,gx,gy):
        shift=max(0,self.H-1080)*.35
        return self.role=='main' and abs(gx-self.cx)<215 and 240+shift<gy<600+shift
    def end_main(self):
        x,y=self._main_origin
        self.c.restore();self.role='secondary'
        self.clear_caption_rail(self.entry['view_A'])
        self.view_label(self.cx,88,'A',self.entry['view_A'])
        self.finish_main()
    def frame(self,sheet_no,total=100,code='NCR'):
        # Shared physical frame, three-digit collection numbering in the text layer.
        old=self.text
        def number_text(t,*a,**kw):
            if t==f'{code}-{sheet_no:02d}':t=f'{code}-{sheet_no:03d}'
            if t==f'SHEET {sheet_no:02d} / {total:02d}':t=f'SHEET {sheet_no:03d} / {total:03d}'
            return old(t,*a,**kw)
        self.text=number_text
        try:super().frame(sheet_no,total,code)
        finally:self.text=old


def draw_view(s,entry,key,cx,cy,width,height):
    from path_cleanup import load,points
    d=load(ASSETS/(entry['slug']+'-'+key+'.json'))
    # An authored camera roll presents elongated service rails diagonally,
    # without changing their geometry or shrinking their useful details.
    roll=math.radians(entry.get('view_'+key+'_roll',0))
    def turn(v):return [v[0]*math.cos(roll)-v[1]*math.sin(roll),v[0]*math.sin(roll)+v[1]*math.cos(roll)]
    if roll:
        for path in d['paths']:path['points']=[turn(v) for v in path['points']]
        d['anchors']={k:turn(v) for k,v in d.get('anchors',{}).items()}
    pts=[p for path in d['paths'] for p in path['points']]
    x0=min(x for x,y in pts);x1=max(x for x,y in pts);y0=min(y for x,y in pts);y1=max(y for x,y in pts)
    k=min(width/(x1-x0),height/(y1-y0));ox=(x0+x1)/2;oy=(y0+y1)/2
    def p(v):return(cx+(v[0]-ox)*k,cy+(v[1]-oy)*k)
    styles={'structure':(.89,.85,WHITE),'detail':(.69,.47,WHITE),'shell':(.48,.36,WHITE),
            'accent':(.86,.62,ARC),'cable':(.64,.47,GOLD),'figure':(.90,.80,WHITE)}
    from century.editorial import DATA
    from century.editorial_second import DATA as SECOND
    if entry['number'] in DATA or entry['number'] in SECOND or entry['number']>100:
        styles['detail']=(.79,.54,WHITE)
        styles['shell']=(.52,.38,WHITE)
    drawn=[]
    for path in d['paths']:
        a,w,col=styles.get(path['role'],(.56,.45,WHITE))
        pts,closed=points(path)
        s.poly([p(v) for v in pts],a,w,close=closed,color=col)
        drawn.append([p(v) for v in pts]+([p(pts[0])] if closed else []))
    if key=='A':s._view_A_paths,s._view_A_centre=drawn,cy
    # per-sheet corrections where an exported anchor misses the part it names (century/anchor_shifts.py)
    from century.anchor_shifts import SHIFTS
    shift=SHIFTS.get((entry['slug'],key),{})
    return {name:(lambda q,d=shift.get(name,(0,0)):(q[0]+d[0]*k,q[1]+d[1]*k))(p(v)) for name,v in d.get('anchors',{}).items()}


def callouts(s,entry,anchors,mx,my):
    notes=json.loads((ASSETS/(entry['slug']+'-meta.json')).read_text())['notes']
    order=sorted(anchors,key=lambda key:anchors[key][0]);n=len(order)//2
    # per-sheet column choices and extra room at the bottom (century/anchor_shifts.py)
    from century.anchor_shifts import SIDES,ROOM
    sides=SIDES.get((entry['slug'],'A'),{});room=ROOM.get((entry['slug'],'A'),{})
    columns=([k for k in order[:n] if sides.get(k,-1)<0]+[k for k in order[n:] if sides.get(k,1)<0],
             [k for k in order[:n] if sides.get(k,-1)>0]+[k for k in order[n:] if sides.get(k,1)>0])
    for side,keys in ((-1,columns[0]),(1,columns[1])):
        keys.sort(key=lambda key:anchors[key][1])
        # labels stay in their column but sit as close to the height of what they name as the spacing allows,
        # so leaders run short and nearly level instead of reaching across the drawing to fixed slots
        top,bottom,gap=my-260,my+160+room.get(side,0),82
        ys=[min(bottom,max(top,anchors[key][1])) for key in keys]
        for i in range(1,len(ys)):ys[i]=max(ys[i],ys[i-1]+gap)
        if ys and ys[-1]>bottom:
            ys[-1]=bottom
            for i in range(len(ys)-2,-1,-1):ys[i]=min(ys[i],ys[i+1]-gap)
        # where a label at its part's height would sit on the drawing, this side keeps the even slots
        def on_drawing(i,key):
            x0=mx+side*374+side*5;w=max(103,max([s.measure(key,7.3,.14)]+[s.measure(l,6,.035) for l in s.wrap(notes[key],227,6,.035)] if notes.get(key) else [0]))
            bx0,bx1=sorted((x0-side*6,x0+side*(w+6)));by0,by1=ys[i]-22,ys[i]+16+12*len(s.wrap(notes[key],227,6,.035) if notes.get(key) else [])
            # (the faint centre mark of the main view runs across the label columns too)
            if by0<=getattr(s,'_view_A_centre',-1e9)<=by1:return True
            for path in getattr(s,'_view_A_paths',[]):
                for (ax,ay),(cx_,cy_) in zip(path,path[1:]):
                    n=max(1,int(math.hypot(cx_-ax,cy_-ay)/4))
                    if any(bx0<=ax+(cx_-ax)*t/n<=bx1 and by0<=ay+(cy_-ay)*t/n<=by1 for t in range(n+1)):return True
            return False
        # a label that would sit on the drawing moves to the nearest clear height between its neighbours;
        # only if none exists does this side fall back to the even slots
        for i,key in enumerate(keys):
            if not on_drawing(i,key):continue
            lo=ys[i-1]+gap if i else top; hi=ys[i+1]-gap if i+1<len(ys) else bottom
            here=ys[i]
            for d in sorted(range(-240,241,8),key=abs):
                if lo<=here+d<=hi:
                    ys[i]=here+d
                    if not on_drawing(i,key):break
            else:
                ys[i]=here
        if any(on_drawing(i,key) for i,key in enumerate(keys)):
            ys=[top+i*(bottom-top)/max(1,len(keys)-1) for i in range(len(keys))]
        slot=lambda i,key,side=side,ys=ys:(mx+side*374,ys[i])
        from hardware3d.family_drawing import uncrossed
        keys=uncrossed(keys,anchors,slot)
        for i,key in enumerate(keys):
            x,y=slot(i,key)
            px,py=anchors[key]
            align='r' if side<0 else 'l';tx=x+side*5
            lines=s.wrap(notes[key],227,6,.035) if notes.get(key) else []
            # the rule under the name runs as far as the longest of the name and its lines
            rule=max(103,5+max([s.measure(key,7.3,.14)]+[s.measure(line,6,.035) for line in lines]))
            s.dot(px,py,1.35,.85)
            s.poly([(px,py),(x,y),(x+side*rule,y)],.4,.43,close=False)
            s.text(key,tx,y-8,7.3,track=.14,a=.85,align=align)
            # Enlarged type in composed profiles needs proportional leading.
            lead=max(10,s.readable_size(6)*1.32) if s.layer_mode else 10
            for j,line in enumerate(lines):s.text(line,tx,y+13+j*lead,6,track=.035,a=.62,align=align)


def compose(entry,size=(5120,2160),audit_hook=None):
    Sheet.side_inset=150 if size[0]/size[1]<2 else 0
    s=CenturySheet(*size,seed=entry['seed']);s.entry=entry;s.subject=entry['slug'];s.set_palette(entry['palette'])
    s.background();s.begin_lines();s.grid();s.frame(entry['number'],entry.get('series_total',100))
    if audit_hook:audit_hook(s)
    mx,my=s.cx-70,505
    s.begin_main(mx,my)
    anchors=draw_view(s,entry,'A',mx,my-15,660,665)
    callouts(s,entry,anchors,mx,my)
    s.end_main()
    if s.wide:
        from triptych import extra,caption_y,measured_illustration
        ex=extra(s);lx=390;rx=s.W-405
        with measured_illustration(s,'left'):
            draw_view(s,entry,'B',lx,241+ex*.225,370,290+ex*.25)
        s.view_label(lx,caption_y(s,'left'),'B',entry['view_B'],entry.get('view_B_note'))
        with measured_illustration(s,'right'):
            draw_view(s,entry,'C',rx,241+ex*.225,370,290+ex*.25)
        s.view_label(rx,caption_y(s,'right'),'C',entry['view_C'],entry.get('view_C_note'))
    # Three named disciplines, as on the b-sheets; real_basis stays in the catalog as their source record.
    head=[tuple(x) for x in entry['enabled_by']] if 'enabled_by' in entry else [('FOUNDATION',entry['real_basis'])]
    enabled=head+[('STILL NEEDED',entry['required_breakthroughs'])]
    for tag,_ in enabled:
        # Tags sit at +20 in the 160-unit label column; composed profiles widen that column themselves.
        width=20+s.measure(tag,6.5)
        assert s.layer_mode or width<152,(entry['number'],'legend tag too long for its column',tag,round(width,1))
    s.legend(entry['title'],entry['purpose'],entry['narrative'],enabled,entry['service_year'])
    from century.editorial import draw as draw_editorial
    draw_editorial(s,entry)
    from century.editorial_second import draw as draw_second
    draw_second(s,entry)
    from century.extension_editorial import draw as draw_extension
    draw_extension(s,entry)
    s.end_lines()
    return s


def main():
    p=argparse.ArgumentParser();p.add_argument('--ids',default='');p.add_argument('--domain');p.add_argument('--format',choices=['wide','16-9','both'],default='both');p.add_argument('--force',action='store_true');p.add_argument('--maintenance',action='store_true',help='Explicit later revision; bypass the one-night production deadline');a=p.parse_args()
    ids={int(x) for x in a.ids.split(',') if x};entries=json.loads(CAT.read_text())
    for entry in entries:
        if not ids and entry.get('curation',{}).get('status')=='rejected':continue
        if ids and entry['number'] not in ids:continue
        if a.domain and entry['domain']!=a.domain:continue
        if not entry.get('built'):continue
        for fmt,size in [('wide',(5120,2160)),('16-9',(5120,2880))]:
            if a.format not in (fmt,'both'):continue
            file=OUT/fmt/f"{entry['number']:03d}-{entry['slug']}.webp"
            if file.exists() and not a.force:continue
            if not a.maintenance and datetime.now(timezone.utc)>=datetime(2026,9,25,6,tzinfo=timezone.utc):print('DEADLINE',flush=True);return
            t=time.time();s=compose(entry,size)
            temporary=file.with_name('.'+file.stem+f'.{os.getpid()}.webp')
            s.save(temporary,glow=.15,grain=1.8);temporary.replace(file)
            im=Image.open(file);im.thumbnail((1600,900));im.save(OUT/'previews'/f"{entry['number']:03d}-{entry['slug']}-{fmt}.jpg",quality=92)
            entry.setdefault('rendered',{})[fmt]={'file':str(file.relative_to(ROOT)),'size':list(size),'seconds':round(time.time()-t,2)}
            entry['status']='rendered' if len(entry['rendered'])==2 else 'partially-rendered'
            update(entry['number'],{'rendered':entry['rendered'],'status':entry['status']})
            print('RENDERED',entry['number'],fmt,round(time.time()-t,2),flush=True)
if __name__=='__main__':main()
