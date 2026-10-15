#!/usr/bin/env python3
"""Write docs/bloom/catalog.json from the per-machine modules and QA records.

The modules are the source of truth for text; this file is the readable
registry (id, texts, views, notes, files, build/audit status).
"""
import sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
from century import bloom

OUT = ROOT / 'docs/bloom/catalog.json'
QA = ROOT / 'concepts/bloom-ten/qa'


def main():
    summary = json.loads((QA / 'audit-summary.json').read_text()) if (QA / 'audit-summary.json').exists() else {}
    rows = []
    for e in bloom.entries():
        mod = bloom.module(e['module'])
        stem = bloom.stem(e)
        meta = ROOT / 'tools/assets/century' / (e['slug'] + '-meta.json')
        build = QA / f'{stem}-build.json'
        row = {k: v for k, v in e.items() if k not in ('module',)}
        row['stamp'] = f"NCR-{e['ncr']:03d}"
        row['field_notes'] = {k: mod.DOSSIER[k] for k in ('kind', 'fact', 'rows', 'note')}
        row['diagrams'] = {side: dict(zip(('title', 'scope', 'foot'), mod.DOSSIER[side])) for side in ('left', 'right')}
        row['callouts'] = json.loads(meta.read_text())['notes'] if meta.exists() else {}
        row['source_files'] = [f'tools/century/bloom/{e["module"]}.py', f'tools/century/bloom/{e["module"]}_model.py',
                               'tools/century/bloom/parts.py', 'tools/century/kit.py', 'tools/century/bloom/render.py']
        row['files'] = {fmt: f'concepts/bloom-ten/{fmt}/{stem}.webp' for fmt in ('16x9', '21x9')
                        if (ROOT / f'concepts/bloom-ten/{fmt}/{stem}.webp').exists()}
        if build.exists():
            b = json.loads(build.read_text())
            row['built'] = {'at': b['at'], 'parts': b['parts'], 'cameras': {k: v['camera'] for k, v in b['groups'].items()}}
        row['layout_audit'] = summary.get(e['id'])
        rows.append(row)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n')
    print(OUT, len(rows), 'entries')


if __name__ == '__main__':
    main()
