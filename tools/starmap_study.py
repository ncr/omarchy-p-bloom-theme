#!/usr/bin/env python3
"""Isolated Truth Lamp art-direction study. Does not change the default renderer.

Run: python3 tools/starmap_study.py
The accepted clear-labels master is the reference, at native 5120x2160.
"""
from contextlib import contextmanager
from pathlib import Path
import hashlib,json,math
import cairo
from PIL import Image,ImageDraw,ImageFont
import devices,foibles
from sheet import Sheet,WHITE,ARC

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'concepts/starmap-study'

class StudySheet(Sheet):
    triptych = True
    def __init__(self,*a,**kw):
        self.role='plain'
        self.text_manifest=[]
        super().__init__(*a,**kw)

    @contextmanager
    def layer(self,role):
        old=self.role;self.role=role
        try:yield
        finally:self.role=old

    def text(self,*a,**kw):
        self.text_manifest.append((a,kw))
        with self.layer('plain'):return super().text(*a,**kw)

    def text_mid(self,*a,**kw):
        with self.layer('plain'):return super().text_mid(*a,**kw)

    def grid(self,*a,**kw):
        with self.layer('grid'):return super().grid(*a,**kw)

    def frame(self,*a,**kw):
        with self.layer('frame'):return super().frame(*a,**kw)

    def begin_main(self,*a,**kw):
        super().begin_main(*a,**kw);self.role='main'

    def end_main(self):
        super().end_main();self.role='secondary'

    def leader(self,*a,**kw):
        with self.layer('callout'):return super().leader(*a,**kw)

    def legend(self,*a,**kw):
        with self.layer('plain'):return super().legend(*a,**kw)

    def emblem(self,*a,**kw):
        with self.layer('emblem'):return super().emblem(*a,**kw)

    def _ink(self,a,color):
        # Text always uses the plain role. The .95 white SVG wordmark stays exact.
        if self.role=='grid':a*=.28
        elif self.role=='frame':a*=.65
        elif self.role=='emblem' and a<.95:a*=.42
        elif self.role in ('main','figure','secondary') and a<.3:a*=.7
        super()._ink(a,color)

    @staticmethod
    def density(x,y):
        # Spatially correlated ink attenuation, not distorted coordinates.
        v=(math.sin(x/79+y/143)+.65*math.sin(x/23-y/61+1.7)
           +.35*math.sin(x/7.3+y/13.1)) / 2
        return .18+.82*((v+1)/2)**.6

    def primary_focus(self,gx,gy):
        mx,my=self.cx,self.cy-25+max(0,self.H-1080)*.35
        return self.role=='main' and abs(gx-mx)<145 and my-260<gy<my-150

    def _stroke(self,a,w,dash,color):
        if self.role=='plain':return super()._stroke(a,w,dash,color)
        c=self.c
        x0,y0,x1,y1=c.path_extents()
        px,py=c.user_to_device((x0+x1)/2,(y0+y1)/2)
        gx,gy=px/self.s,py/self.s
        primary=self.primary_focus(gx,gy)
        if self.role=='emblem':factor=.42
        elif self.role=='callout':factor=.7
        elif self.role in ('grid','frame'):factor=1 # _ink handles these
        elif self.role=='section':factor=1
        elif primary:factor=1.05 if a>=.7 else .9
        elif self.role=='figure':factor=.87 if a>=.65 else .62
        elif self.role=='secondary':factor=.76 if a>=.65 else .52
        else:factor=.78 if a>=.7 else (.58 if a>=.4 else .38)
        alpha=min(.98,a*factor)
        textured=(self.role in ('main','figure','secondary','section') and a<.65)
        if textured and abs(x1-x0)+abs(y1-y0)>2:
            grad=cairo.LinearGradient(x0,y0,x1 if x1!=x0 else x0+.01,y1)
            for i in range(17):
                t=i/16;x=x0+(x1-x0)*t;y=y0+(y1-y0)*t
                ux,uy=c.user_to_device(x,y)
                grad.add_color_stop_rgba(t,*color,alpha*self.density(ux/self.s,uy/self.s))
            c.set_source(grad)
        else:self._ink(alpha,color)
        c.set_line_width(w);c.set_dash(dash or []);c.stroke();c.set_dash([])

    def fade_ln(self,x1,y1,x2,y2,a0=.7,a1=0,w=.6,color=WHITE):
        return super().fade_ln(x1,y1,x2,y2,a0*.7,a1*.7,w,color)


def section_study(s,mx,my):
    with s.layer('section'):
        # A compact field-volume study immediately below the emitter array.
        # It ends above the heads and stays away from every callout.
        for k in range(8):
            y=my-148+k*5.2;hw=117+k*7.8
            s.bez((mx-hw,y),(mx-hw*.5,y+8+k*.65),
                  (mx+hw*.5,y+8+k*.65),(mx+hw,y),.22,.32,color=ARC)


def install_study(sheet_class=StudySheet):
    devices.Sheet=sheet_class
    original_enrich=foibles.enrich
    def enrich(s,name,mx,my):
        original_enrich(s,name,mx,my)
        if name=='truth-lamp':section_study(s,mx,my)
    foibles.enrich=enrich
    for name in ('seated','diner','dog'):
        original=getattr(foibles,name)
        def wrapped(s,*a,_draw=original,**kw):
            with s.layer('figure'):return _draw(s,*a,**kw)
        setattr(foibles,name,wrapped)


def main():
    (OUT/'native').mkdir(parents=True,exist_ok=True)
    # Capture the unchanged layout/text before installing the experiment.
    calls=[];original_text=Sheet.text
    def capture(self,*a,**kw):
        calls.append((a,kw));return original_text(self,*a,**kw)
    Sheet.text=capture
    baseline=foibles.truth_lamp((5120,2160))
    Sheet.text=original_text
    baseline.end_lines();baseline.save(OUT/'native/before.png')
    accepted=ROOT/'concepts/clear-labels/native/10-truth-lamp.png'
    assert (OUT/'native/before.png').read_bytes()==accepted.read_bytes(),'Baseline differs from accepted master'
    install_study()
    studied=foibles.truth_lamp((5120,2160))
    # Immutable strings/colors avoid comparing mutable shared palette containers.
    assert repr(calls)==repr(studied.text_manifest),'Text or text placement changed'
    studied.end_lines();studied.save(OUT/'native/after.png')
    font=ImageFont.truetype('/usr/share/fonts/gsfonts/NimbusSans-Regular.otf',25)
    panel=Image.new('RGB',(2048,1824),(12,16,22));d=ImageDraw.Draw(panel)
    detail=Image.new('RGB',(1800,1130),(12,16,22));dd=ImageDraw.Draw(detail)
    for i,(file,label) in enumerate((('before.png','PRZED — ZAAKCEPTOWANA WERSJA'),('after.png','PO — PROBA WARSTW I KRESKI'))):
        with Image.open(OUT/'native'/file) as im:
            thumb=im.resize((2048,864),Image.Resampling.LANCZOS)
            thumb.save(OUT/file)
            d.text((24,i*912+11),label,font=font,fill='#d9e1e9');panel.paste(thumb,(0,i*912+48))
            dd.text((i*900+20,14),label.split(' — ')[0],font=font,fill='#d9e1e9')
            detail.paste(im.crop((1880,460,2780,1540)),(i*900,50))
    panel.save(OUT/'before-after.jpg',quality=96,subsampling=0)
    detail.save(OUT/'detail-before-after.png')
    report={'resolution':[5120,2160],'baseline_byte_identical':True,'all_text_calls_and_positions_unchanged':True,
            'text_calls':len(calls),'seed':studied.seed,
            'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (OUT/'native').glob('*.png')}}
    (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
