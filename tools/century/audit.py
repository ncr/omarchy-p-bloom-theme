#!/usr/bin/env python3
"""Independent glyph/geometry collision checks for both Century page formats."""
import sys,math,json,argparse,cairo
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from century.render import compose,CAT,OUT
from sheet import Sheet,FONT,WHITE
from century.registry import update
LABELS=[]
def text(self,t,x,y,size=8,track=.22,a=.7,align='l',bold=False,color=WHITE,rot=0):
    size=self.readable_size(size)
    self.c.select_font_face(FONT,cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    glyphs=self._glyphs(t,size);adv=self._advances(glyphs,bold);w=sum(adv)+track*size*(len(glyphs)-1)
    px=-{'l':0,'r':w,'c':w/2}[align];m=self.c.get_matrix();m.translate(x,y);m.rotate(math.radians(rot));pts=[]
    for (ch,fs,dy),aw in zip(glyphs,adv):
        self.c.set_font_size(fs);e=self.c.text_extents(ch)
        if e.width and e.height:pts.extend(m.transform_point(u,v) for u in (px+e.x_bearing,px+e.x_bearing+e.width) for v in (dy+e.y_bearing,dy+e.y_bearing+e.height))
        px+=aw+track*size
    if pts:LABELS.append({'text':t,'font_px':round(size*math.hypot(m.xy,m.yy),3),'box':[min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts),max(p[1] for p in pts)]})
    return w

def text_mid(self,t,x,y_mid,size=8,track=.22,a=.7,align='l',bold=False,color=WHITE):
    size=self.readable_size(size)
    self.c.select_font_face(FONT,cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    self.c.set_font_size(size);cap=-self.c.text_extents('H').y_bearing
    if len(t)==1 and align=='c':
        e=self.c.text_extents(t);return text(self,t,x-(e.x_bearing+e.width/2),y_mid+cap/2,size,0,a,'l',bold,color)
    return text(self,t,x,y_mid+cap/2,size,track,a,align,bold,color)

def baseline(s):
    s.surface.flush();w,h=s.px;s._audit_base=np.frombuffer(s.surface.get_data(),np.uint8).reshape(h,w,4).copy();LABELS.clear()

def audit(entry,fmt):
    size=(5120,2160) if fmt=='wide' else (5120,2880)
    s=compose(entry,size,baseline);w,h=size;s.surface.flush();arr=np.frombuffer(s.surface.get_data(),np.uint8).reshape(h,w,4)
    mask=np.abs(arr[:,:,:3].astype(np.int16)-s._audit_base[:,:,:3].astype(np.int16)).max(axis=2)>5
    collisions=[];outside=[];pairs=[]
    for t in LABELS:
        x0,y0,x1,y1=t['box']
        if x0<0 or y0<0 or x1>w or y1>h:outside.append(t)
        hits=int(mask[max(0,math.floor(y0)):min(h,math.ceil(y1)),max(0,math.floor(x0)):min(w,math.ceil(x1))].sum())
        if hits:collisions.append(dict(t,geometry_pixels=hits))
    for i,a in enumerate(LABELS):
        for b in LABELS[i+1:]:
            if a['box'][0]<b['box'][2] and a['box'][2]>b['box'][0] and a['box'][1]<b['box'][3] and a['box'][3]>b['box'][1]:pairs.append([a['text'],b['text']])
    counts={k:sum(t['text']==k for t in LABELS) for k in 'ABC'};expected={'A':1,'B':int(s.wide),'C':int(s.wide)}
    issues=[]
    if counts!=expected:issues.append({'expected':expected,'found':counts})
    if entry.get('curation',{}).get('status')!='rejected':
        from triptych import audit_slots,caption_y
        issues.extend(audit_slots(s,LABELS))
        for letter in 'BC':
            note=entry.get(f'view_{letter}_note')
            matches=[t for t in LABELS if t['text']==note] if note else []
            if len(matches)!=1:
                issues.append(f'{letter}: expected one authored detail note')
                continue
            label_index=next(i for i,t in enumerate(LABELS) if t['text']==letter)
            title=LABELS[label_index+1]
            # Same view_label layout as the original HALL PLAN reference.
            # Glyph bearings can move visible left edges by a native pixel.
            if abs(title['box'][0]-matches[0]['box'][0])>3:
                issues.append(f'{letter}: note is not aligned with its title')
            expected_top=(caption_y(s,'left' if letter=='B' else 'right')+9)*s.s
            if abs(matches[0]['box'][1]-expected_top)>3:
                issues.append(f'{letter}: note is detached from its title')
        stale=('COMPONENT STUDY / OBLIQUE','COVER REMOVED / SAME HARDWARE','SAME HARDWARE / SERVICE VIEW')
        if any(t['text'] in stale or '/ SPECULATIVE' in t['text'] for t in LABELS):
            issues.append('Legacy generic caption or inconsistent service suffix')
        notes=[t for t in LABELS if t['text'].startswith('FIELD NOTES / ')]
        if len(notes)!=1:issues.append(f'Expected one FIELD NOTES block, found {len(notes)}')
        from collection_layout import signature_box
        nx0,ny0,nx1,ny1=s.field_notes_bounds
        ex,ey,er=signature_box(s)
        if nx0<ex+er and nx1>ex-er and ny0<ey+er and ny1>ey-er:
            issues.append('Field notes collide with signature region')
    if entry['view_A'] not in [t['text'] for t in LABELS]:issues.append('A caption missing')
    result={'number':entry['number'],'slug':entry['slug'],'format':fmt,'size':list(size),'geometry_collisions':collisions,'text_collisions':pairs,'out_of_bounds':outside,'view_issues':issues,'illustration_layout':s.illustration_layout,'section_layout':s.section_layout,'legend_top':s.legend_top,'field_notes_bounds':s.field_notes_bounds,'text_count':len(LABELS),'texts':LABELS[:]}
    result['passed']=not any(result[k] for k in ('geometry_collisions','text_collisions','out_of_bounds','view_issues'))
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--ids',default='');p.add_argument('--domain');a=p.parse_args();ids={int(x) for x in a.ids.split(',') if x}
    oldtext,oldmid=Sheet.text,Sheet.text_mid;Sheet.text=text;Sheet.text_mid=text_mid
    entries=json.loads(CAT.read_text());reports=[]
    for entry in entries:
        if not entry.get('built') or (ids and entry['number'] not in ids) or (a.domain and entry['domain']!=a.domain):continue
        rr=[]
        for fmt in ('wide','16-9'):
            r=audit(entry,fmt);reports.append(r);rr.append(r)
            print(entry['number'],fmt,'PASS' if r['passed'] else 'FAIL',[(x['text'],x['geometry_pixels']) for x in r['geometry_collisions']],r['text_collisions'],flush=True)
        entry.setdefault('validation',{})['layout']={r['format']:r['passed'] for r in rr}
        (OUT/'qa'/f"{entry['number']:03d}-{entry['slug']}-layout.json").write_text(json.dumps(rr,indent=2)+'\n')
        update(entry['number'],{'validation':entry['validation']})
    Sheet.text,Sheet.text_mid=oldtext,oldmid
    return int(any(not r['passed'] for r in reports))
if __name__=='__main__':sys.exit(main())
