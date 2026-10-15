#!/usr/bin/env python3
"""Run the unchanged Century layout audit on p(bloom) sheets, both formats.

Checks glyph/geometry collisions, text overlaps, bounds, exactly one A/B/C,
caption notes attached to their views, readable type, one title, one field
notes block, one punch line, section spacing. Reports: concepts/bloom-ten/qa.
"""
import sys, json, argparse
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
from sheet import Sheet
import century.audit as base
from century.bloom import render as bloom_render
from century import bloom
QA = ROOT / 'concepts/bloom-ten/qa'


def main():
    p = argparse.ArgumentParser(); p.add_argument('--ids', default=''); a = p.parse_args()
    ids = [x for x in a.ids.split(',') if x]
    base.compose = bloom_render.compose
    oldtext, oldmid = Sheet.text, Sheet.text_mid
    Sheet.text = base.text; Sheet.text_mid = base.text_mid
    QA.mkdir(parents=True, exist_ok=True)
    failed = False; summary = {}
    try:
        for entry in bloom.entries(ids or None):
            if not (ROOT / 'tools/assets/century' / (entry['slug'] + '-meta.json')).exists():
                continue
            rr = []
            for fmt in ('wide', '16-9'):
                r = base.audit(entry, fmt); rr.append(r)
                label = '21x9' if fmt == 'wide' else '16x9'
                print(entry['id'], label, 'PASS' if r['passed'] else 'FAIL',
                      [(x['text'], x['geometry_pixels']) for x in r['geometry_collisions']],
                      r['text_collisions'], r['out_of_bounds'] and [t['text'] for t in r['out_of_bounds']],
                      r['view_issues'], flush=True)
                failed |= not r['passed']
                summary.setdefault(entry['id'], {})[label] = r['passed']
            (QA / f"{bloom.stem(entry)}-layout.json").write_text(json.dumps(rr, indent=2) + '\n')
    finally:
        Sheet.text, Sheet.text_mid = oldtext, oldmid
    path = QA / 'audit-summary.json'
    merged = json.loads(path.read_text()) if path.exists() else {}
    merged.update(summary)
    path.write_text(json.dumps(dict(sorted(merged.items())), indent=2) + '\n')
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
