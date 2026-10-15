#!/usr/bin/env python3
"""Render the release matrix: one complete 42-sheet set per profile.

    python3 tools/render_wallpaper_sets.py                      # every profile
    python3 tools/render_wallpaper_sets.py --profile 16x9-1080p --only o03,c087
    python3 tools/render_wallpaper_sets.py --jobs 3 --out dist/wallpaper-sets
    python3 tools/render_wallpaper_sets.py --level muted --level vivid   # the two extra grounds

Composed profiles use tools/aspect_layout.py; each sheet is audited on its
final pixels (type floor, text/geometry and text/text collisions, clipped
labels, A/B/C counts) and the report is written next to the images as
audit.json. The two accepted 5K masters are rendered by the direct renderer
and must reproduce the recorded catalog hashes byte for byte.

--level picks the ground intensity (tools/ground_levels.py). Default sets go
to <out>/<profile>/, the others to <out>/<profile>-<level>/ (the set id used
by the manifest, the archive and the companion). The audit includes the type
contrast check at every level.

Output is a build artefact (dist/ is not tracked). Package it with
tools/package_wallpaper_profiles.py.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from concurrent.futures import ProcessPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def master_hashes():
    """Recorded hashes of the accepted native masters."""
    data = json.loads((ROOT/'docs/collection/native-masters.json').read_text())['profiles']
    return {pid: {i: f['sha256'] for i, f in p['files'].items()} for pid, p in data.items()}


def set_id(profile, level):
    return profile if level == 'default' else f'{profile}-{level}'


def render_one(task):
    profile, level, item_id, out = task
    import aspect_layout as A
    from sheet import Sheet
    Sheet.ground_level = level
    items = {i['id']: i for i in A.collection()}
    item = items[item_id]
    path = Path(out)/set_id(profile, level)/item['filename']
    tmp = path.with_name('.'+path.name+'.tmp.webp')
    t = time.time()
    masters = {pid: size for pid, _, size in A.MASTERS}
    if profile in masters:
        size = masters[profile]
        Sheet.side_inset = 150 if abs(size[0]/size[1]-16/9) < .01 else 0
        s = item['render'](size)
        if item['family'] == 'original':
            s.end_lines()
        s.save(tmp, glow=item['glow'], grain=item['grain'])
        report = dict(id=item_id, size=list(size), template='native-master', blocks=['all'],
                      dropped=[], fallback=None, min_text_px=14.0, issues=[],
                      ground=getattr(s, 'ground', None), level=level)
    else:
        comp = A.composition(profile)
        report, s = A.audit(item, comp)
        s.save(tmp, glow=item['glow'], grain=item['grain'])
    tmp.replace(path)
    report.update(file=item['filename'], sha256=sha(path), bytes=path.stat().st_size,
                  seconds=round(time.time()-t, 2))
    return set_id(profile, level), report


def main():
    import aspect_layout as A
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ids = [p[0] for p in A.MATRIX] + [p[0] for p in A.MASTERS]
    ap.add_argument('--profile', action='append', choices=ids, help='repeatable; default all')
    ap.add_argument('--only', help='comma-separated sheet ids (o03,c087,...)')
    ap.add_argument('--out', type=Path, default=ROOT/'dist/wallpaper-sets')
    ap.add_argument('--jobs', type=int, default=2)
    ap.add_argument('--level', action='append', choices=['muted', 'default', 'vivid'],
                    help='ground intensity, repeatable; default: default')
    ap.add_argument('--accept-masters', action='store_true',
                    help='record new native-master hashes after an approved visual change '
                         '(palette, sheet numbers); normally they must reproduce exactly')
    args = ap.parse_args()
    levels = args.level or ['default']
    if args.accept_masters and levels != ['default']:
        ap.error('--accept-masters records the Default masters only')
    items = A.collection()
    only = set(args.only.split(',')) if args.only else None
    tasks = []
    sets = {}
    for level in levels:
        for pid in args.profile or ids:
            sid = set_id(pid, level)
            sets[sid] = (pid, level)
            (args.out/sid).mkdir(parents=True, exist_ok=True)
            tasks += [(pid, level, it['id'], str(args.out)) for it in items if not only or it['id'] in only]
    profiles = list(sets)
    reports = {pid: {} for pid in profiles}
    for pid in profiles:
        old = args.out/pid/'audit.json'
        if old.is_file() and only:
            reports[pid] = {r['id']: r for r in json.loads(old.read_text())['sheets']}
    expected = master_hashes()
    failed = 0
    with ProcessPoolExecutor(args.jobs) as pool:
        for pid, r in pool.map(render_one, tasks):
            if pid in expected and not args.accept_masters and expected[pid].get(r['id']) != r['sha256']:
                r['issues'].append('native master differs from the accepted file')
            reports[pid][r['id']] = r
            failed += bool(r['issues'])
            print(f"{pid:19} {r['id']:5} {r['seconds']:5.1f}s {r['bytes']/1e6:5.2f} MB min {r['min_text_px']:5.2f}px"
                  f" drop {','.join(r['dropped']) or '-'}{' [' + r['fallback'] + ']' if r['fallback'] else ''}"
                  f"{'  ISSUES ' + '; '.join(r['issues']) if r['issues'] else ''}", flush=True)
    if args.accept_masters:
        path = ROOT/'docs/collection/native-masters.json'
        data = json.loads(path.read_text())
        for pid in profiles:
            if pid in data['profiles']:
                current = [it['id'] for it in items]
                files = data['profiles'][pid]['files']
                for i, r in reports[pid].items():
                    files[i] = {'name': r['file'], 'sha256': r['sha256']}
                # Only the current collection; an old audit.json may still list retired sheets.
                data['profiles'][pid]['files'] = {i: files[i] for i in current if i in files}
        path.write_text(json.dumps(data, indent=1)+'\n')
    order = [it['id'] for it in items]
    for pid in profiles:
        sheets = [reports[pid][i] for i in order if i in reports[pid]]
        (args.out/pid/'audit.json').write_text(json.dumps(dict(
            profile=sets[pid][0], level=sets[pid][1], count=len(sheets),
            min_text_px=min(r['min_text_px'] for r in sheets),
            issues=sum(len(r['issues']) for r in sheets), sheets=sheets), indent=1)+'\n')
    print('SHEETS WITH ISSUES:', failed)
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
