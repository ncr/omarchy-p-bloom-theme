#!/usr/bin/env python3
"""Preserve native before/after masters and publish the twelve-sheet review."""
import json,shutil,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'concepts/century/quality-redesign'
CHANGES={
'queue-garden':('An open crescent plinth, six exposed mechanical latches, an offset index train and separately readable ticket optics replace the potted ornament.','Six completion events remain the same fictional service log; no waiting-time prediction.'),
'coral-cradle':('A horseshoe nursery with removable radial cassettes, gentle circulation and a short gantry makes the cradle the main subject. The compliant transfer collar contacts fragment bases.','Original speculative restoration tool. Biological success is not inferred from the drawing.'),
'tidal-loom':('Staggered matched rotor cartridges now have swept triangulated supports, recoverable seabed shoes and a dedicated wet-service spine.','Same paired shrouded-rotor premise. The flow-power plot is still an ideal available-flux relation, not measured output.'),
'presence-rig':('The human stands on a spatial roller deck within swept load columns. A captive overhead reel, actual suit connections and replaceable floor cassette make the equipment tangible.','Shared mannequin limb lengths and sole contact retained. Sparse roller bays illustrate a much denser fictional production floor.'),
'sleep-cocoon':('A ribbed acoustic canopy, shaped side petals, isolated head support and rear air circuit wrap the existing measured occupant and pelvis linkage.','The authored seated pose is retained. No health outcome or dynamic recline validation is claimed.'),
'wind-kite':('A swept airfoil, canted tips, open structural wing bay and shaped ground winch give the airborne and ground systems comparable visual weight.','The tether is explicitly compressed for the system study; the force-length diagram remains an illustrative cycle.'),
'meeting-buoy':('An exposed chronometer and rack-driven semaphore replace the bare mast. Microphone capsules and the manual paddle stay physically distinct from the timing mechanism.','The same 60-minute fictional meeting log is retained. The flag still cannot mute anyone.'),
'manta-foil':('Twin wave-piercing hulls, a raised passenger salon and recessed boarding rails replace the blunt single hull. Retractable foil roots and axial guarded propulsors get their own studies.','Same harbour ferry and retractable-foil premise. Lift-ratio plot is an ideal relationship, not a hull-performance prediction.'),
'seam-surgeon':('Short pipe ends now provide context around the double orbital track. Preparation, filler-fed welding and trailing inspection form a visible tool train.','The twelve-sector inspection log is fictional and unchanged. Finishing a weld is still separate from accepting it.'),
'volumetric-stage':('A deep triangulated stage with seventeen articulated optical heads, service ladders, cooling and timing replaces the smooth arch. The luminous locus is restrained.','Original fictional performance targets retained; particle-response curve now explicitly labelled fictional. No photonics feasibility claim.'),
'aroma-organ':('The random orange-peel receptor matrix is gone. A spatial six-channel metering bank and an explicitly illustrative valve program explain the machine instead.','Six of 96 fictional hardware channels, not biological receptor measurements. Compact format also receives an explicit concept note.'),
'quiet-stair':('Four fixed-x treads now ride independent vertical screw guides. A same-scale sequence shows stair, level-low and level-high states; the manual release and edge sensor remain separate.','Endpoint kinematics checked. Authored concept, not a certified access lift, complete control system or collision simulation.')}


def main():
 entries=json.loads((OUT/'selected.json').read_text());font=ImageFont.truetype('/usr/share/fonts/gsfonts/NimbusSans-Regular.otf',23)
 for e in entries:
  e['change'],e['limits']=CHANGES[e['slug']];e['status']='quality-redesign / reviewed internally / awaiting user review'
  e['files']={}
  for fmt in ('wide','16-9'):
   stem=e['id']+'-'+e['slug']+'.webp'
   if e['origin']=='Century':source=ROOT/'concepts/century'/fmt/Path(e['source']).name
   else:source=OUT/'after'/('original-wide' if fmt=='wide' else 'original-16-9')/Path(e['source']).name
   dest=OUT/'after'/fmt/stem;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
   before=OUT/'before'/fmt/stem
   if not before.exists() and e['origin']=='Original' and fmt=='16-9':shutil.copy2(OUT/'before/original-16-9'/Path(e['source']).name,before)
   assert before.is_file()
   expected=(5120,2160) if fmt=='wide' else (5120,2880)
   e['files'][fmt]={}
   for state,p in [('before',before),('after',dest)]:
    with Image.open(p) as im:assert im.size==expected
    e['files'][fmt][state]={'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':list(expected)}
   preview=OUT/'previews';preview.mkdir(exist_ok=True)
   with Image.open(dest) as im:im.thumbnail((1200,675));im.save(preview/(e['id']+'-'+fmt+'.jpg'),quality=95)
   ch=675 if fmt=='wide' else 900;compare=Image.new('RGB',(1600,2*ch+64),(9,14,21));dr=ImageDraw.Draw(compare)
   for i,p in enumerate((before,dest)):
    with Image.open(p) as im:im.thumbnail((1600,ch));compare.paste(im,(0,32+i*(ch+32)))
    dr.text((14,4+i*(ch+32)),'BEFORE' if i==0 else 'AFTER',font=font,fill='#bfd1de')
   compare.save(OUT/(e['id']+'-'+fmt+'-compare.jpg'),quality=95)
 data={'wallpapers':entries,'scope':'Twelve below-cutoff redesigns; other 22 unchanged','status':'awaiting user review','pipeline':'Blender visible vectors / native Cairo / original typography','compact_before_note':'Original 3 compact before files were regenerated from unchanged source before edits.'}
 sources=['tools/century/quality_geometry.py','tools/century/build.py','tools/century/render.py','tools/century/exporter.py','tools/century/kit.py','tools/century/editorial.py','tools/century/editorial_second.py','tools/hardware3d/quality_scenes.py','tools/quality_panels.py','tools/leisure.py','tools/sheet.py','tools/starmap_study.py','tools/omarchy-logo.svg','tools/century/quality_review.py','tools/century/quality_review.html']
 data['source_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}
 data['scope_verification']=json.loads((OUT/'scope-verification.json').read_text()) if (OUT/'scope-verification.json').exists() else None
 (OUT/'review.json').write_text(json.dumps(data,indent=2)+'\n')
 html=(ROOT/'tools/century/quality_review.html').read_text();(OUT/'index.html').write_text(html.replace('/*DATA*/',json.dumps(data).replace('</','<\\/')))
 for fmt in ('wide','16-9'):
  hh=380 if fmt=='wide' else 506;im=Image.new('RGB',(1800,6*(hh+36)),(9,14,21));dr=ImageDraw.Draw(im)
  for i,e in enumerate(entries):
   with Image.open(OUT/'after'/fmt/(e['id']+'-'+e['slug']+'.webp')) as img:img.thumbnail((900,hh));im.paste(img,((i%2)*900,(i//2)*(hh+36)))
   dr.text(((i%2)*900+12,(i//2)*(hh+36)+hh+5),e['title'],font=font,fill='#c1d5df')
  im.save(OUT/('contact-'+fmt+'.jpg'),quality=95)
 print('Review ready: 12 sheets, 24 native after files, 24 before files, 24 comparisons.')
if __name__=='__main__':main()
