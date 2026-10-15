#!/usr/bin/env python3
"""Package rendered wallpaper sets as per-file objects and write the manifest.

    tools/run_matrix.sh [o02,b13]                       # renders dist/wallpaper-sets/<set>/ (all, or a few sheets)
    python3 tools/package_wallpaper_profiles.py         # shipping copies + docs/collection/profiles.json
    python3 tools/publish_wallpaper_objects.py          # uploads the files R2 doesn't have yet, then verifies

Rendering keeps lossless, audited intermediates in dist/wallpaper-sets/. The
shipped files are re-encoded as lossy WebP (quality 90, method 6; owner's
decision for fast installs: text and thin lines are unchanged at close zoom,
only the finest grain is smoother) into dist/wallpaper-release/<set>/, only
when the lossless source is newer, so unchanged wallpapers keep their bytes.

Every shipped file is published once, under its own SHA-256, at
<objects_base><sha256>.webp (Cloudflare R2): content-addressed, immutable,
identical files stored once. Each profile has three packs in the manifest,
`packs` → muted / default / vivid, each a group of files (`objects`); the
companion downloads a pack file by file and reuses what it already has, so fixing one wallpaper means rendering that wallpaper in every
set, uploading only its new files and committing the manifest.

The theme itself ships only the starter: one wallpaper per background colour
(STARTER), from the Default pack of the default profile, copied into
backgrounds/ and listed as `starter` in the manifest, so the theme works right
after `omarchy theme install` without the companion app and its clone stays
small. The companion downloads the full set for the screen.

`files`, `archive` and `levels` in each profile are the frozen first release
(tar archives on the GitHub release wallpapers-v1), kept as they were for
companion apps from before per-file downloads.

Ground levels: sets rendered with `--level muted --level vivid` (folders
<profile>-muted/ and <profile>-vivid/) become the Muted and Vivid packs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
DEFAULT = '16x9-2880p'
OBJECTS_BASE = 'https://media.jacekbecela.com/p-bloom/'
QUALITY = dict(quality=90, method=6)
# The theme's own wallpapers: the best sheet of each of the ten background colours (palettes.json)
STARTER = ('o03', 'o09', 'o02', 'c087', 'b02', 'o01', 'c025', 'o13', 'b18', 'b21')


def encode(task):
    src, dst = task
    from PIL import Image
    tmp = dst.with_name('.'+dst.name+'.tmp')
    with Image.open(src) as im:
        im.convert('RGB').save(tmp, format='WEBP', **QUALITY)
    tmp.replace(dst)
    return dst


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    import aspect_layout as A
    from wallpaper_profiles import set_digest
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--sets', type=Path, default=ROOT/'dist/wallpaper-sets')
    ap.add_argument('--release', type=Path, default=ROOT/'dist/wallpaper-release')
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--default', default=DEFAULT)
    ap.add_argument('--allow-issues', action='store_true', help='package despite audit findings (not for release)')
    ap.add_argument('--levels', help='ground levels to package besides Default (default: muted,vivid when '
                                     'rendered; an empty string packages Default only)')
    args = ap.parse_args()
    cat = json.loads((ROOT/'docs/collection/catalog.json').read_text())
    ids = [e['id'] for e in cat['finalized']]
    names = {e['id']: Path(e['source']).name for e in cat['finalized']}
    rows = [(pid, fam, size, tpl) for pid, fam, size, tpl, _ in A.MATRIX] + \
           [(pid, fam, size, 'native-master') for pid, fam, size in A.MASTERS]
    rows.sort(key=lambda r: (['16:9', '16:10', '3:2', '4:3', '21:9', '32:9'].index(r[1]), r[2][0]*r[2][1]))
    profiles = []
    total = 0
    levels = [x for x in (args.levels.split(',') if args.levels else ('muted', 'vivid')) if x]
    # A set is a profile at one ground level; Default sets keep the plain id.
    sets = [pid for pid, *_ in rows]
    for level in levels:
        found = [f'{pid}-{level}' for pid, *_ in rows if (args.sets/f'{pid}-{level}'/'audit.json').is_file()]
        if found and len(found) != len(rows) and not args.allow_issues:
            sys.exit(f'{level}: rendered for {len(found)} of {len(rows)} profiles; render the rest or pass --levels')
        sets += found
    # Lossy shipping copies, re-encoded only when the lossless source is newer.
    from concurrent.futures import ProcessPoolExecutor
    tasks = []
    for sid in sets:
        (args.release/sid).mkdir(parents=True, exist_ok=True)
        for i in ids:
            src, dst = args.sets/sid/names[i], args.release/sid/names[i]
            if not dst.is_file() or dst.stat().st_mtime < src.stat().st_mtime:
                tasks.append((src, dst))
    with ProcessPoolExecutor(args.jobs) as pool:
        for n, _ in enumerate(pool.map(encode, tasks), 1):
            if n % 42 == 0:
                print(f'encoded {n}/{len(tasks)}', flush=True)

    def package(sid):
        """Audit check and the file list (`objects`) of one set."""
        folder = args.sets/sid
        audit = json.loads((folder/'audit.json').read_text())
        sheets = {r['id']: r for r in audit['sheets']}
        if [i for i in ids if i in sheets] != ids:
            sys.exit(f'{sid}: incomplete render ({len(sheets)} of {len(ids)})')
        if audit['issues'] and not args.allow_issues:
            sys.exit(f'{sid}: {audit["issues"]} audit findings; see {folder/"audit.json"}')
        files = []
        lossless = 0
        for i in ids:
            if sha(folder/names[i]) != sheets[i]['sha256']:
                sys.exit(f'{sid}/{names[i]}: changed since its audit')
            lossless += (folder/names[i]).stat().st_size
            path = args.release/sid/names[i]
            files.append(dict(id=i, name=path.name, sha256=sha(path), bytes=path.stat().st_size))
        size = sum(f['bytes'] for f in files)
        print(f'{sid:20} {size/1e6:7.1f} MB (lossless {lossless/1e6:6.1f} MB)'
              f'  min text {audit["min_text_px"]:.1f} px  {set_digest(files)[:12]}')
        return audit, files

    # the first release's archives and file lists, kept as they were for companion apps from before per-file
    # downloads (they read `files`, `archive` and `levels`)
    old = json.loads((ROOT/'docs/collection/profiles.json').read_text())
    legacy = {p['id']: p for p in old['profiles']}

    for pid, family, size, template in rows:
        packs = {}
        for level in ('muted', 'default', 'vivid'):
            sid = pid if level == 'default' else f'{pid}-{level}'
            if sid in sets:
                audit, files = package(sid)
                total += sum(f['bytes'] for f in files)
                packs[level] = dict(min_text_px=audit['min_text_px'], objects=files)
        frozen = {k: legacy[pid][k] for k in ('archive', 'files', 'levels') if k in legacy.get(pid, {})}
        entry = dict(
            id=pid, label=f'{family} · {size[0]} × {size[1]}', aspect=family, size=list(size),
            layout=template, floor_px=A.floor_px(*size) if template != 'native-master' else 14.0,
            min_text_px=packs['default']['min_text_px'], packs=packs, **frozen)
        profiles.append(entry)
    default = next(p for p in profiles if p['id'] == args.default)['packs']['default']
    grounds = json.loads((ROOT/'docs/collection/palettes.json').read_text())['assignment_42']
    if sorted(grounds[i] for i in STARTER) != sorted(set(grounds.values())):
        sys.exit('STARTER must hold one sheet of each background colour')
    starter = [f for f in default['objects'] if f['id'] in STARTER]
    # backgrounds/ holds exactly the starter.
    out = ROOT/'backgrounds'
    out.mkdir(exist_ok=True)
    wanted = {f['name'] for f in starter}
    for old in out.glob('*.webp'):
        if old.name not in wanted:
            sys.exit(f'Unexpected file in backgrounds/: {old.name}; resolve explicitly')
    for f in starter:
        dst = out/f['name']
        if not dst.is_file() or sha(dst) != f['sha256']:
            shutil.copyfile(args.release/args.default/f['name'], dst)
    manifest = dict(
        version=4, count=len(ids), default=args.default, objects_base=OBJECTS_BASE,
        starter=dict(profile=args.default, note='The wallpapers in backgrounds/: one per background colour, from '
                                               'the default profile\'s Default pack.', objects=starter),
        release=dict(note='Each profile has three packs (`packs`: muted, default, vivid), each a group of files '
                          '(`objects`); every file is published once at objects_base + sha256 + suffix '
                          '(content-addressed, immutable; tools/publish_wallpaper_objects.py). `files`, `archive` '
                          'and `levels` are the frozen first release (GitHub release wallpapers-v1 tar archives) '
                          'for companion apps from before per-file downloads.'),
        readability=dict(rule='floor_px = max(11, 14 * height / 2880)',
                         note='Smallest type on the native file after every transform. Lower resolutions '
                              'are composed more compactly and drop secondary blocks; type is never shrunk.'),
        encoding=dict(format='webp', lossless=False, **QUALITY,
                      note='Lossless intermediates are audited; shipped files are re-encoded.'),
        levels=dict(order=['muted', 'default', 'vivid'],
                    note='Background intensity (tools/ground_levels.py): one pack per level, '
                         'profile["packs"][level], installed in the folder <profile> (Default) or '
                         '<profile>-<level>/.'),
        profiles=profiles)
    (ROOT/'docs/collection/profiles.json').write_text(json.dumps(manifest, indent=1)+'\n')
    print(f'{len(profiles)} profiles, {total/1e9:.2f} GB in all sets; {len(starter)} starter wallpapers in backgrounds/')


if __name__ == '__main__':
    main()
