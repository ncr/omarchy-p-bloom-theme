#!/usr/bin/env python3
"""Upload the wallpaper files the manifest names and R2 doesn't have yet, then verify them.

    python3 tools/publish_wallpaper_objects.py            # upload what is missing, verify uploads and a sample
    python3 tools/publish_wallpaper_objects.py --dry-run  # only report what would be uploaded
    python3 tools/publish_wallpaper_objects.py --check o02,b13   # also download every file of these sheets

Every file of every pack in docs/collection/profiles.json (`packs` → `objects`) is stored once under its SHA-256 at
<objects_base><sha256>.webp (bucket `media`, key `p-bloom/<sha256>.webp`; Wrangler must be logged in). Files are taken
from dist/wallpaper-release/<set>/ (tools/package_wallpaper_profiles.py) and checked against the manifest before
upload. Objects never change, so they are served as immutable; a fix publishes new objects, never replaces old ones.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
BUCKET_PREFIX = 'media/p-bloom/'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def objects(manifest):
    """sha256 -> (set folder, file name, bytes, sheet id), each object once."""
    out = {}
    for p in manifest['profiles']:
        for level, pack in p['packs'].items():
            sid = p['id'] if level == 'default' else f"{p['id']}-{level}"
            for f in pack['objects']:
                out.setdefault(f['sha256'], (sid, f['name'], f['bytes'], f['id']))
    return out


def head(url):
    # A query of its own: Cloudflare caches a 404 for the plain URL, which the companions would then get after upload.
    request = urllib.request.Request(f'{url}?check={time.time_ns()}', method='HEAD',
                                     headers={'User-Agent': 'p-bloom-publish'})
    try:
        with urllib.request.urlopen(request, timeout=30) as r:
            return int(r.headers.get('Content-Length', -1))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def fetch_digest(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'p-bloom-publish'})
    with urllib.request.urlopen(request, timeout=120) as r:
        return hashlib.sha256(r.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--release', type=Path, default=ROOT/'dist/wallpaper-release')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--jobs', type=int, default=6)
    ap.add_argument('--sample', type=int, default=20, help='objects already online to re-download and check')
    ap.add_argument('--check', default='', help='sheet ids whose files are all re-downloaded and checked')
    args = ap.parse_args()
    args.release = args.release.resolve()
    manifest = json.loads((ROOT/'docs/collection/profiles.json').read_text())
    base = manifest['objects_base']
    todo = objects(manifest)
    for digest, (sid, name, size, _) in todo.items():
        path = args.release/sid/name
        if not path.is_file() or path.stat().st_size != size or sha(path) != digest:
            sys.exit(f'{sid}/{name}: the local file does not match the manifest; package again')

    def present(item):
        digest, (sid, name, size, _) = item
        return digest, head(f'{base}{digest}{Path(name).suffix}') == size

    with ThreadPoolExecutor(args.jobs) as pool:
        online = dict(pool.map(present, todo.items()))
    missing = [d for d in todo if not online[d]]
    print(f'{len(todo)} objects in the manifest, {len(todo) - len(missing)} online, {len(missing)} to upload '
          f'({sum(todo[d][2] for d in missing)/1e6:.1f} MB)', flush=True)
    if args.dry_run:
        return

    def upload(digest):
        sid, name, *_ = todo[digest]
        key = f'{BUCKET_PREFIX}{digest}{Path(name).suffix}'
        subprocess.run(['nice', '-n', '18', 'npx', '--yes', 'wrangler@4', 'r2', 'object', 'put', key,
                        '--file', str(args.release/sid/name), '--content-type', 'image/webp',
                        '--cache-control', 'public, max-age=31536000, immutable', '--remote'],
                       check=True, capture_output=True, text=True, cwd=args.release)   # Wrangler's .wrangler/ there
        return digest

    with ThreadPoolExecutor(args.jobs) as pool:
        for n, _ in enumerate(pool.map(upload, missing), 1):
            if n % 50 == 0 or n == len(missing):
                print(f'uploaded {n}/{len(missing)}', flush=True)
    sheets = set(filter(None, args.check.split(',')))
    check = missing + random.sample([d for d in todo if online[d]], min(args.sample, len(todo) - len(missing)))
    check = list(dict.fromkeys(check + [d for d in todo if todo[d][3] in sheets]))

    def verify(digest):
        return digest, fetch_digest(f'{base}{digest}{Path(todo[digest][1]).suffix}') == digest

    with ThreadPoolExecutor(args.jobs) as pool:
        bad = [d for d, ok in pool.map(verify, check) if not ok]
    if bad:
        sys.exit(f'{len(bad)} objects do not match after upload: {bad[:5]}')
    print(f'verified {len(check)} objects by downloading them')


if __name__ == '__main__':
    main()
