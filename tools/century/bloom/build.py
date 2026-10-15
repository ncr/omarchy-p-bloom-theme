"""Blender runner for the p(bloom) series. Reuses the Century kit and exporter.

blender -b --factory-startup --python-exit-code 1 --python tools/century/bloom/build.py -- --ids b01,b02

No deadline guard: this series is an explicit, later production. Models are
saved to concepts/bloom-ten/models; visible paths to tools/assets/century.
"""
import sys, os, json, importlib, time
from pathlib import Path
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
from century import kit
from century import bloom
STATUS = ROOT / 'concepts/bloom-ten/qa'


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--ids', default='')
    p.add_argument('--angles', default='', help='exploration only: az,el;az,el ... exports A-<i> variants, no B/C')
    args = p.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    ids = [x for x in args.ids.split(',') if x]
    failed = False
    for entry in bloom.entries(ids or None):
        t = time.time()
        print('BUILD', entry['id'], entry['slug'], flush=True)
        try:
            model = importlib.import_module('century.bloom.' + entry['module'] + '_model')
            kit.reset(entry)
            kit.g.STUDY = ROOT / 'concepts/bloom-ten/models'
            kit.g.STUDY.mkdir(parents=True, exist_ok=True)
            az, el = model.build()
            if args.angles:
                from century.exporter import export
                kit.g.OUT = Path('/tmp/bloom/probes'); kit.g.STUDY = Path('/tmp/bloom/probes')
                kit.g.OUT.mkdir(parents=True, exist_ok=True)
                for i, pair in enumerate(args.angles.split(';')):
                    a_, e_ = (float(v) for v in pair.split(','))
                    export(entry['slug'] + f'-probe{i}', a_, e_)
                continue
            meta = kit.save(entry, az, el)
        except Exception:
            import traceback
            traceback.print_exc()
            failed = True
            continue
        record = {'at': datetime.now(timezone.utc).isoformat(), 'seconds': round(time.time() - t, 2),
                  'parts': meta['parts'], 'views': meta['views'], 'groups': meta['groups']}
        STATUS.mkdir(parents=True, exist_ok=True)
        (STATUS / f"{bloom.stem(entry)}-build.json").write_text(json.dumps(record, indent=2) + '\n')
        print('BUILT', entry['slug'], record['seconds'], 's', meta['parts'], 'parts', flush=True)
    sys.stdout.flush()
    os._exit(1 if failed else 0)


if __name__ == '__main__':
    main()
