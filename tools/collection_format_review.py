#!/usr/bin/env python3
"""Freeze the 34-sheet formatting revision, check it, and optionally publish masters."""
import argparse,hashlib,json,shutil,os
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'concepts/century/format-unification'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')

def main():
    global OUT
    ap=argparse.ArgumentParser();ap.add_argument('--publish',action='store_true')
    ap.add_argument('--revision',choices=['format-unification','triptych','individual-diagrams','retro-diagrams','caption-consistency','single-caption','readable-retro','quiet-footer','vertical-rhythm','attached-captions'],default='format-unification');args=ap.parse_args()
    OUT=ROOT/'concepts/century'/args.revision
    baseline=json.loads((OUT/'baseline.json').read_text());entries=[];checks=[]
    for fmt in ('wide','16-9'):
        report=json.loads((OUT/f'layout-original-{fmt}.json').read_text())
        for s in report['sheets']:
            assert not any(s[k] for k in ('geometry_collisions','text_collisions','out_of_bounds','view_label_issues')),s['name']
            checks.append(dict(id=s['name'],format=fmt,passed=True))
    for e in baseline:
        original=e['id'].startswith('o');name=Path(e['source']).name;slug=name.split('-',1)[1][:-5]
        item=dict(e,slug=slug,files={})
        item['change']=('Field Notes now include all five original specification rows, a device-specific explanation, process rail and dry service aside. Centred A caption and a separate, smaller Omarchy signature.' if original else 'Existing Field Notes moved into the shared right footer, aligned with the technical column. A smaller, separate Omarchy signature gives the dossier room to breathe.')
        item['limits']='Illustration geometry and narrative figures retained. This is a layout revision, not a new quality ranking.'
        if args.revision=='triptych':
            item['format_revision']='triptych-2026-09-25'
            item['change']='Complete three-column composition in both formats: detail and diagram on each side, title lower left, Field Notes lower right. A moves above the main drawing; the Easter egg sits quietly at the exact bottom centre.'
        if args.revision=='individual-diagrams':
            from subject_diagrams import FIGURES
            item['format_revision']='individual-diagrams-2026-09-25'
            item['change']=FIGURES[slug][1]+'. '+FIGURES[slug][3]
            item['limits']='Individual explanatory diagram replaces the repeated two-input/two-output block. Main artwork, narrative and three-column layout retained.'
        if args.revision=='retro-diagrams':
            from subject_diagrams import RETRO_REFINED
            item['format_revision']='retro-diagrams-2026-09-25'
            item['change']=RETRO_REFINED.get(slug,'Retained: precise scientific geometry or an already curved figure.')
            item['limits']='Schematic presentation retained. Shape and material language refined; narrative, typography and main hardware retained.'
        if args.revision=='caption-consistency':
            item['format_revision']='caption-consistency-2026-09-25'
            item['change']=('Reference caption layout retained.' if original else 'B and C now use a specific device note directly beneath and aligned with the name. Projected service shows the year without the inconsistent SPECULATIVE suffix.')
            item['limits']='Typography and editorial consistency only; illustration geometry and original service years retained.'
        if args.revision=='single-caption':
            item['format_revision']='single-caption-2026-09-25'
            item['change']=('Removed the redundant illustration heading; the B/C caption below owns the view name.' if not original or slug in ('greener','sky-racer','cortical-mesh','truth-lamp','organ-foundry','proxy') else 'Reference layout retained; no redundant illustration heading.')
            item['limits']='Only duplicate headings removed; device geometry, annotations, data and lower captions retained.'
        if args.revision=='readable-retro':
            item['format_revision']='readable-retro-2026-09-25'
            item['change']='Readable typography: 14 native pixel minimum after fitting, stronger text contrast and adjusted label spacing.'
            focus={'fusion-transport':'Larger crew-ring axial detail.','volumetric-stage':'Address planes on a shaped instrument cradle.','quiet-stair':'Working-face service rail with exposed contacts, detailed latch and a load-bearing editorial aside.','seam-surgeon':'Machined weld coupon and a contact inspection shoe.','plant-alibi':'Layered basin, branching roots, flow-meter bezel and drain.'}
            item['change']+=' '+focus.get(slug,'Existing illustration retained.')
            item['limits']='Technical paths and planes stay precise. Conceptual hardware remains illustrative; typography uses the original font.'
        if args.revision=='quiet-footer':
            item['format_revision']='quiet-footer-2026-09-25'
            item['change']='Loose main-view annotations moved into Field Notes; the bottom centre keeps one Easter egg.' if not original or slug in ('truth-lamp','proxy','quantum-simulator') else 'Reviewed: existing part callouts remain attached to the drawing.'
            item['limits']='All wording, narrative, artwork and existing 14-pixel typography floor retained. No changes to collection membership.'
        if args.revision in ('vertical-rhythm','attached-captions'):
            item['format_revision']=args.revision+'-2026-09-25'
            item['change']='B/C captions follow the actual drawn contours, including component annotations, with a short measured gap. Each illustration and its caption form one group, separate from the following study.'
            item['limits']='Artwork scale, wording, minimum type size, main illustration and Field Notes content retained.'
        if not original:
            rr=json.loads((ROOT/'concepts/century/qa'/name.replace('.webp','-layout.json')).read_text())
            assert all(r['passed'] for r in rr),e['id']
            checks.extend(dict(id=e['id'],format=r['format'],passed=r['passed']) for r in rr)
        for fmt,size in [('wide',(5120,2160)),('16-9',(5120,2880))]:
            source=OUT/'after'/('original-'+fmt)/name if original else ROOT/'concepts/century'/fmt/name
            dest=OUT/'after'/fmt/(e['id']+'-'+slug+'.webp');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
            with Image.open(dest) as im:
                assert im.size==size
                im.thumbnail((1280,720));p=OUT/'previews'/f"{e['id']}-{fmt}.jpg";p.parent.mkdir(exist_ok=True);im.save(p,quality=95)
            before=e['before'] if fmt=='wide' else e['compact_before']
            item['files'][fmt]={'after':str(dest.relative_to(OUT)),'before':str((ROOT/before).relative_to(OUT)) if before else None,'size':size,'sha256':digest(dest)}
            item['files'][fmt]['changed']=bool(before and digest(ROOT/before)!=digest(dest))
            if before and args.revision not in ('retro-diagrams','caption-consistency','single-caption','quiet-footer'):assert item['files'][fmt]['changed'],e['id']
        entries.append(item)
    archive=json.loads((OUT/'archive-hashes.json').read_text())
    assert all(digest(ROOT/p)==h for p,h in archive.items()),'Rejected archive changed'
    assert len(checks)==68
    sources=['tools/collection_layout.py','tools/original_field_notes.json','tools/sheet.py','tools/devices.py','tools/leisure.py','tools/foibles.py','tools/century/editorial.py','tools/century/editorial_second.py','tools/omarchy-logo.svg']
    sources+=['tools/triptych.py','tools/starmap_study.py','tools/quality_panels.py','tools/century/render.py']
    sources.append('tools/subject_diagrams.py')
    if args.revision=='single-caption':sources+=['tools/left_aux_panels.py','tools/right_aux_panels.py','tools/century/audit.py']
    if args.revision=='caption-consistency':sources+=['docs/century/catalog.json','tools/century/audit.py']
    if args.revision=='readable-retro':sources+=['docs/century/catalog.json','tools/assets/century/quiet-stair-A.json','tools/assets/century/quiet-stair-B.json','tools/assets/century/quiet-stair-C.json','tools/assets/century/quiet-stair-meta.json','tools/century/quality_geometry.py','tools/century/editorial.py','tools/right_aux_panels.py','tools/fusion_transit.py','tools/verify_wallpaper_layout.py','tools/century/audit.py']
    if args.revision=='quiet-footer':sources+=['tools/main_scene_panels.py','tools/hardware3d/radial_drawing.py','tools/century/audit.py']
    if args.revision in ('vertical-rhythm','attached-captions'):sources+=['tools/century/audit.py','tools/verify_wallpaper_layout.py']
    if args.revision=='attached-captions':sources.append('tools/hardware3d/secondary_drawing.py')
    data=dict(revision=args.revision,wallpapers=entries,count=34,formats=2,validation=checks,rejected_archive_unchanged=len(archive),source_sha256={p:digest(ROOT/p) for p in sources})
    dump(OUT/'review.json',data)
    html=(ROOT/'tools/collection_format_review.html').read_text()
    if args.revision in ('triptych','individual-diagrams','retro-diagrams','caption-consistency','single-caption'):
        html=html.replace('P(BLOOM) / COLLECTION FORMAT','P(BLOOM) / THREE-COLUMN COMPOSITION')
        html=html.replace('All 34 retained wallpapers, now with one editorial grid: Field Notes, centred main captions and a separate Omarchy signature. Illustration geometry and the original narrative figures are retained.','All 34 wallpapers now contain the complete composition: two details, two diagrams, title, Field Notes, original signature and a quiet, centred Easter egg. A sits above the main illustration. Both formats retain every section.')
        html=html.replace('Before / after compares the actual previous masters. Eleven original sheets had no current 16:9 master; comparison is unavailable for those compact views. This layout pass does not change the quality ranking.','Before / after compares all 68 actual previous masters. B toggles the revision, including in fullscreen. This composition pass preserves the narrative facts and collection membership.')
    if args.revision=='individual-diagrams':
        html=html.replace('P(BLOOM) / THREE-COLUMN COMPOSITION','P(BLOOM) / INDIVIDUAL DIAGRAMS').replace('All 34 wallpapers now contain the complete composition: two details, two diagrams, title, Field Notes, original signature and a quiet, centred Easter egg. A sits above the main illustration. Both formats retain every section.','35 independently drawn explanatory figures replace the repeated flowchart across all 34 wallpapers. Weld sections, optical paths, sampling records and mechanisms each have their own composition. The three-column layout and narrative are retained.')
    if args.revision=='retro-diagrams':
        html=html.replace('P(BLOOM) / THREE-COLUMN COMPOSITION','P(BLOOM) / RETRO-FUTURE DIAGRAMS').replace('All 34 wallpapers now contain the complete composition: two details, two diagrams, title, Field Notes, original signature and a quiet, centred Easter egg. A sits above the main illustration. Both formats retain every section.','26 schematic figures receive shaped castings, swept cables, helical springs and softer material contours. Nine figures keep their precise scientific geometry or existing curves. Compare against the previous individual-diagrams revision.')
    if args.revision=='single-caption':
        html=html.replace('P(BLOOM) / THREE-COLUMN COMPOSITION','P(BLOOM) / ONE CAPTION PER VIEW').replace('All 34 wallpapers now contain the complete composition: two details, two diagrams, title, Field Notes, original signature and a quiet, centred Easter egg. A sits above the main illustration. Both formats retain every section.','The lower B/C caption now owns the name of each side view. Duplicate upper headings were removed from twenty Century sheets and seven panels on six original sheets. Component labels, data headings, geometry and narrative are retained.').replace('<div class="controls">','<p><a href="panels.html">Compare the affected side panels</a></p><div class="controls">')
    if args.revision=='caption-consistency':
        html=html.replace('P(BLOOM) / THREE-COLUMN COMPOSITION','P(BLOOM) / CAPTION CONSISTENCY').replace('All 34 wallpapers now contain the complete composition: two details, two diagrams, title, Field Notes, original signature and a quiet, centred Easter egg. A sits above the main illustration. Both formats retain every section.','The twenty Century sheets now follow the original caption convention: boxed letter, view name, and an aligned, device-specific subtitle. All projected service dates show the year consistently. Geometry and original narrative facts are retained.').replace('<div class="controls">','<p><a href="captions.html">Compare caption and service-date details</a></p><div class="controls">')
    if args.revision in ('individual-diagrams','retro-diagrams'):
        html=html.replace('<div class="controls">','<p><a href="fragments.html">Compare the diagram fragments side by side</a></p><div class="controls">')
    if args.revision=='readable-retro':
        html=html.replace('P(BLOOM) / COLLECTION FORMAT','P(BLOOM) / READABLE RETRO FUTURE')
        html=html.replace('All 34 retained wallpapers, now with one editorial grid: Field Notes, centred main captions and a separate Omarchy signature. Illustration geometry and the original narrative figures are retained.','All 34 sheets receive a 14-native-pixel text floor and stronger text contrast. Five sheets also receive enlarged, reoriented or detailed auxiliary illustrations. The Quiet Stair Easter egg is now demonstrably load-bearing.')
        html=html.replace('Before / after compares the actual previous masters. Eleven original sheets had no current 16:9 master; comparison is unavailable for those compact views. This layout pass does not change the quality ranking.','Before / after uses the actual single-caption masters in both formats. Main illustrations retain their geometry except the detailed Quiet Stair safety rail.')
        html=html.replace('<div class="controls">','<p><a href="fragments.html">Compare the six illustration changes and typography</a></p><div class="controls">')
    if args.revision=='quiet-footer':
        html=html.replace('P(BLOOM) / COLLECTION FORMAT','P(BLOOM) / A QUIETER CENTRE')
        html=html.replace('All 34 retained wallpapers, now with one editorial grid: Field Notes, centred main captions and a separate Omarchy signature. Illustration geometry and the original narrative figures are retained.','All 34 sheets reviewed. Twenty-three had loose captions below the main artwork; these now belong to Field Notes. Part callouts remain by their parts, and the centre footer has one Easter egg.')
        html=html.replace('Before / after compares the actual previous masters. Eleven original sheets had no current 16:9 master; comparison is unavailable for those compact views. This layout pass does not change the quality ranking.','Both formats compare the actual readable-retro masters. All wording and illustration geometry are retained.')
        html=html.replace('<div class="controls">','<p><a href="footers.html">Compare the relocated annotations</a></p><div class="controls">')
    if args.revision in ('vertical-rhythm','attached-captions'):
        html=html.replace('P(BLOOM) / COLLECTION FORMAT','P(BLOOM) / VERTICAL HIERARCHY')
        html=html.replace('All 34 retained wallpapers, now with one editorial grid: Field Notes, centred main captions and a separate Omarchy signature. Illustration geometry and the original narrative figures are retained.','All 34 sheets: closer illustration/caption groups, section dividers above study headings, and measured clearance before the legend and Field Notes. Main artwork, wording and readable typography remain intact.')
        html=html.replace('Before / after compares the actual previous masters. Eleven original sheets had no current 16:9 master; comparison is unavailable for those compact views. This layout pass does not change the quality ranking.','Both native formats compare against the frozen previous masters. Checks include actual vector ink bounds, caption attachment, vertical section gaps, collisions and type size.')
        html=html.replace('<div class="controls">','<p><a href="columns.html">Compare the vertical hierarchy of the side columns</a></p><div class="controls">')
    (OUT/'index.html').write_text(html.replace('/*DATA*/',json.dumps(data,ensure_ascii=False).replace('</','<\\/')))
    font=ImageFont.truetype('/usr/share/fonts/gsfonts/NimbusSans-Regular.otf',21)
    for fmt in ('wide','16-9'):
        hh=270 if fmt=='wide' else 360
        for batch in range(4):
            subset=entries[batch*9:(batch+1)*9];canvas=Image.new('RGB',(1920,((len(subset)+2)//3)*(hh+34)),'#101720');dr=ImageDraw.Draw(canvas)
            for i,e in enumerate(subset):
                with Image.open(OUT/e['files'][fmt]['after']) as im:
                    im.thumbnail((640,hh));x=i%3*640;y=i//3*(hh+34);canvas.paste(im,(x,y));dr.text((x+9,y+hh+4),e['id']+' / '+e['title'],font=font,fill='#d1dce4')
            canvas.save(OUT/f'contact-{fmt}-{batch+1}.jpg',quality=95)
    if args.publish:
        for e in entries:
            if e['id'].startswith('o'):
                for fmt in ('wide','16-9'):
                    dest=ROOT/e['source'];dest=dest if fmt=='wide' else dest.parent/'16-9'/dest.name
                    dest.parent.mkdir(exist_ok=True);temp=dest.with_suffix('.format.tmp');shutil.copy2(OUT/e['files'][fmt]['after'],temp);temp.replace(dest)
        for filename,key in [('docs/collection/catalog.json','finalized'),('docs/collection/quality-ranking.json','wallpapers')]:
            p=ROOT/filename;d=json.loads(p.read_text())
            for e in d[key]:
                e.setdefault('pre_format_sha256',e['sha256'])
                if args.revision=='triptych':e.setdefault('pre_triptych_sha256',e['sha256'])
                e['sha256']=digest(ROOT/e['source']);e['format_revision']=args.revision+'-2026-09-25'
            dump(p,d)
    print(f'34 sheets / 68 native masters / 68 layout checks passed / {len(archive)} rejected masters unchanged / published={args.publish}')
if __name__=='__main__':main()
