#!/usr/bin/env python3
"""Write the human-readable catalogue from the reviewed source of truth."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 c=json.loads((ROOT/'docs/century/catalog.json').read_text())
 lines=['# Century — 100 autorskich koncepcji','','Każdy projekt ma własną historię, geometrię oraz podpis A. FOUNDATION opisuje realny punkt wyjścia; STILL NEEDED wskazuje spekulację. Przewidywane daty są fikcją.','']
 research=['# Podstawy i granice źródeł','','Źródła poniżej wspierają wybrane zasady fizyczne lub kierunki badań. Nie dokumentują naszych maszyn, geometrii, parametrów ani dat wdrożenia. Kształty są autorskie. Brak źródła przy koncepcji oznacza, że nie podajemy jej jako zweryfikowanego rozwiązania technicznego.','']
 for e in c:
  n=f"{e['number']:03d}";stem=n+'-'+e['slug'];lines += [f"## {n} · {e['title']}",'',f"**{e['purpose']}**",'',e['narrative'],'',f"- A: {e['view_A']}",f"- B: {e['view_B']}",f"- C: {e['view_C']}",f"- Realna podstawa: {e['real_basis']}",f"- Postulowany przełom: {e['required_breakthroughs']}",f"- Fikcyjna data pierwszego wdrożenia: {e['service_year']}",'',f"[Ultrawide](../../concepts/century/wide/{stem}.webp) · [16:9](../../concepts/century/16-9/{stem}.webp)",'']
  if e.get('curation'):
   decision=e['curation'];lines += [f"**Selekcja: {decision['status']} / partia {decision['batch'] or 'archiwum'}.** {decision['reason']}",'']
  research += [f"## {n} · {e['title']}",'',e['real_basis'],'',e['source_scope'],'']
  for i,url in enumerate(e['sources'],1):research.append(f'- [Źródło {i}]({url})')
  research += ['']
 (ROOT/'docs/century/CONCEPTS.md').write_text('\n'.join(lines))
 (ROOT/'docs/century/RESEARCH.md').write_text('\n'.join(research))
 print('Updated readable concepts and source scope.')
if __name__=='__main__':main()
