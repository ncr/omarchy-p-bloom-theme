#!/usr/bin/env python3
"""Build a portable, offline review gallery with embedded metadata."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    data=json.loads((ROOT/'docs/century/catalog.json').read_text())
    public=[{k:e[k] for k in ('number','slug','title','domain','purpose','narrative','real_basis','required_breakthroughs','curation')} for e in data]
    template=(ROOT/'tools/century/gallery.html').read_text()
    if (ROOT/'concepts/century/refined-ten/index.html').exists():
        template=template.replace('<div class="controls">','<p><a href="refined-ten/">Dopracowana dziesiątka — porównanie przed / po ↗</a></p><div class="controls">')
    if (ROOT/'concepts/century/refined-next-ten/index.html').exists():
        template=template.replace('<div class="controls">','<p><a href="refined-next-ten/">Druga dopracowana dziesiątka — porównanie przed / po ↗</a></p><div class="controls">')
    template=template.replace('<div class="controls">','<p><a href="ranking/">All 34 finished wallpapers — proposed quality ranking ↗</a></p><div class="controls">')
    template=template.replace('<label>Szukaj', '<label>Wybór <select id="selection"><option value="retained">Zachowane 20</option><option value="rejected">Archiwum odrzuconych 80</option><option value="">Wszystkie 100</option></select></label><label>Szukaj')
    template=template.replace("e=>(!domain", "e=>(!$('selection').value||e.curation.status===$('selection').value)&&(!domain")
    template=template.replace("['search','domain','format']", "['search','domain','format','selection']")
    template=template.replace("meta.append(title,el('span',e.purpose))", "meta.append(title,el('span',e.purpose),el('span',e.curation.status==='rejected'?'ODRZUCONE / ARCHIWUM':'ZACHOWANE / PARTIA '+e.curation.batch))")
    template=template.replace("el('p',e.required_breakthroughs)", "el('p',e.required_breakthroughs),el('h3','DECYZJA KURATORSKA'),el('p',e.curation.reason)")
    (ROOT/'concepts/century/index.html').write_text(template.replace('/*CATALOG*/',json.dumps(public,ensure_ascii=False).replace('</','<\\/')))
    print('Gallery: 100 entries, two native formats, no network dependencies.')
if __name__=='__main__':main()
