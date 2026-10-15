#!/usr/bin/env python3
"""Validate the completed collection and write portable review documentation."""
import json,hashlib,math,sys
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from century.registry import update
CAT=ROOT/'docs/century/catalog.json';OUT=ROOT/'concepts/century';ASSETS=ROOT/'tools/assets/century'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    c=json.loads(CAT.read_text());assert len(c)==100 and {e['number'] for e in c}==set(range(1,101))
    for k in ('slug','title','view_A','recipe'):assert len({e[k] for e in c})==100,k
    old={p.stem.split('-',1)[-1] for p in (ROOT/'backgrounds').glob('*.webp')}
    assert not old.intersection(e['slug'] for e in c),'An old wallpaper was counted as new'
    visual=json.loads((OUT/'qa/visual-review.json').read_text())
    assert set(visual['reviewed_numbers'])==set(range(1,101))
    assert visual['last_export_review']=='complete','Final render review is not yet recorded'
    records=[];all_a=[];total=0
    for e in c:
        stem=f"{e['number']:03d}-{e['slug']}";r={'number':e['number'],'slug':e['slug'],'title':e['title'],'files':{},'views':{},'review_status':e.get('curation',{}).get('review','ready-for-user-review'),'curation':e.get('curation',{})}
        audit=json.loads((OUT/'qa'/f'{stem}-layout.json').read_text())
        assert len(audit)==2 and all(a['passed'] for a in audit),stem
        for fmt,size in [('wide',(5120,2160)),('16-9',(5120,2880))]:
            a=next(a for a in audit if a['format']==fmt);assert a['size']==list(size),'Audit must run at native resolution'
            texts=[t['text'] for t in a['texts']]
            assert e['title'] in texts and e['view_A'] in texts
            if fmt=='wide':assert e['view_B'] in texts and e['view_C'] in texts
            path=OUT/fmt/(stem+'.webp')
            with Image.open(path) as im:assert im.format=='WEBP' and im.size==size;im.load()
            views=[ASSETS/(e['slug']+'-'+k+'.json') for k in 'ABC']
            assert path.stat().st_mtime>=max(p.stat().st_mtime for p in views),'Stale render: '+str(path)
            n=path.stat().st_size;total+=n
            r['files'][fmt]={'path':str(path.relative_to(ROOT)),'size':list(size),'bytes':n,'sha256':digest(path)}
        for k in 'ABC':
            path=ASSETS/(e['slug']+'-'+k+'.json');data=json.loads(path.read_text());assert len(data['paths'])>=10
            assert all(math.isfinite(x) for p in data['paths'] for v in p['points'] for x in v)
            r['views'][k]={'path':str(path.relative_to(ROOT)),'sha256':digest(path),'paths':len(data['paths'])}
            assert (OUT/'models'/(e['slug']+'-'+k+'.blend')).stat().st_size>10000
        all_a.append(r['views']['A']['sha256'])
        if e['domain']=='wearables':
            pose=json.loads((OUT/'qa'/(e['slug']+'-pose.json')).read_text());j=pose['joint_points'];lengths={n:math.dist(q['a'],q['b']) for n,q in j.items()}
            for limb,base in [('upper_arm',116),('forearm',88),('thigh',146),('calf',140)]:
                assert abs(lengths['1'+limb]-lengths['-1'+limb])<1e-3,(stem,limb)
                assert abs(lengths['1'+limb]-base*pose['scale'])<1e-3
            for side in ('1','-1'):
                assert math.dist(j[side+'upper_arm']['b'],j[side+'forearm']['a'])<1e-3
                assert math.dist(j[side+'thigh']['b'],j[side+'calf']['a'])<1e-3
            r['pose_checks']={'paired_segment_lengths':True,'continuous_elbows_and_knees':True,'lengths':lengths,'scope':'Illustrative rig geometry; no biomechanics simulation or clinical validation.'}
        records.append(r)
        update(e['number'],{'status':'ready-for-review','validation':{'layout':{'wide':True,'16-9':True},'files':True,'visual_review':'agent-reviewed / awaiting user opinion'}})
    assert len(set(all_a))==100,'Duplicate main geometry'
    source_paths=list((ROOT/'tools/century').glob('*.py'))+[ROOT/'tools/century/gallery.html',ROOT/'tools/century/ranking.html',ROOT/'tools/century/quality_review.html',ROOT/'tools/century/foundations.txt']
    source_paths += [ROOT/p for p in ['tools/sheet.py','tools/collection_layout.py','tools/original_field_notes.json','tools/starmap_study.py','tools/omarchy-logo.svg','tools/hardware3d/family_core.py','tools/hardware3d/main_scenes_build.py','tools/hardware3d/bio_details_build.py','tools/mannequin3d/build.py']]
    source_paths.extend([ROOT/'tools/triptych.py',ROOT/'tools/subject_diagrams.py'])
    manifest={'created_at':datetime.now(timezone.utc).isoformat(),'count':100,'native_files':200,'total_bytes':total,'formats':{'wide':[5120,2160],'16-9':[5120,2880]},'pipeline':'Authored Blender geometry → BVH visible paths → Cairo typography and original SVG → native raster + grain','font':'Nimbus Sans','font_file_sha256':digest(Path('/usr/share/fonts/gsfonts/NimbusSans-Regular.otf')),'source_sha256':{str(p.relative_to(ROOT)):digest(p) for p in source_paths},'catalog_sha256':digest(CAT),'wallpapers':records,'limitations':['Speculative illustrations, not manufacturing drawings.','Curated selection: twenty retained, eighty rejected and archived. Nine retained Century sheets have a new quality redesign awaiting user review; their prior refinements were approved. Collection membership unchanged.','Primary sources describe selected physical principles, not these invented machines.']}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (ROOT/'docs/century/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'PACKAGE PASS: 100 unique concepts, 300 vector views, 200 native files, 200 layout audits. {total/1e9:.2f} GB')
if __name__=='__main__':main()
