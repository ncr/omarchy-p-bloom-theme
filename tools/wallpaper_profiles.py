"""Monitor selection and first-run setup for the optional wallpaper companion."""
import base64
import time
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def monitors():
    try:
        result = subprocess.run(['hyprctl', '-j', 'monitors'], capture_output=True,
                                text=True, check=True, timeout=3)
        return normalize_monitors(json.loads(result.stdout))
    except (OSError, ValueError, subprocess.SubprocessError):
        return []


def normalize_monitors(rows):
    out = []
    if not isinstance(rows, list):
        return out
    for row in rows:
        try:
            if row.get('disabled') or row.get('name') == 'FALLBACK':
                continue
            w, h, scale = int(row['width']), int(row['height']), float(row.get('scale', 1))
            if min(w, h, scale) <= 0 or not math.isfinite(scale):
                continue
            if int(row.get('transform', 0)) % 2:
                w, h = h, w
            out.append(dict(name=str(row['name']), width=w, height=h, scale=scale,
                            focused=bool(row.get('focused'))))
        except (KeyError, TypeError, ValueError, AttributeError, OverflowError):
            continue
    return out


RETRY_SECONDS = 900

# Background intensity: how strong the background colour is. Default is the
# design (and the only level bundled with the theme); Muted and Vivid are
# their own sets per screen profile (`levels` in profiles.json).
LEVELS = ('muted', 'default', 'vivid')
LEVEL_LABELS = {'muted': 'Muted', 'default': 'Default', 'vivid': 'Vivid'}
LEVEL_HINT = 'How strong the background colour is.'


def valid_level(level):
    return level if level in LEVELS else 'default'


def set_name(profile_id, level='default'):
    """Folder of one set: the profile id, plus the level unless Default."""
    return profile_id if level == 'default' else f'{profile_id}-{level}'


def object_url(base, item):
    """Each file is published once under its own SHA-256 (content-addressed): <objects_base><sha256><suffix>."""
    suffix = Path(_safe_name(item['name'])).suffix.lower()
    if suffix not in ('.webp', '.png', '.jpg', '.jpeg') or len(item['sha256']) != 64:
        raise ValueError(f"Invalid wallpaper object: {item['name']}")
    return f"{base}{item['sha256']}{suffix}"


def set_digest(files):
    """One SHA-256 for a set's file list: a set on disk is current when its marker holds the manifest's digest."""
    return hashlib.sha256(''.join(f"{f['sha256']}  {f['name']}\n" for f in files).encode()).hexdigest()


def data_dir():
    return Path(os.environ.get('XDG_DATA_HOME', Path.home()/'.local/share'))/'p-bloom-wallpapers'


def sets_dir():
    return data_dir()/'sets'


def _safe_name(name):
    if not isinstance(name, str) or not name or '/' in name or name.startswith('.') or name != Path(name).name:
        raise ValueError(f'Unsafe file name in wallpaper manifest: {name!r}')
    return name


def _at_level(profile, level):
    """The profile's pack at a background level, or None if it is not published.

    Each profile lists its packs under `packs`: Muted, Default and Vivid, each a group of files (`objects`) that is
    downloaded and installed together, into its own folder (set_name). Here `files` becomes that pack's list.
    `files`, `archive` and `levels` are the frozen first release, kept for apps from before per-file downloads.
    Only the bundled profile's Default pack ships in backgrounds/.
    """
    entry = (profile.get('packs') or {}).get(level)
    if not entry:
        return None
    if not isinstance(entry, dict) or not isinstance(entry.get('objects'), list):
        raise ValueError(f"Invalid {level} set in profile {profile['id']}")
    rest = {k: v for k, v in profile.items() if k not in ('packs', 'levels', 'bundled', 'archive', 'files')}
    return {**rest, 'min_text_px': entry.get('min_text_px', profile['min_text_px']), 'files': entry['objects'],
            'bundled': bool(profile.get('bundled')) and level == 'default'}


MARKER = '.set-sha256'
# Called while a set downloads and installs: progress(phase='download'|'install', done=bytes, total=bytes,
# label=..., level=...). The gallery's settings set it to show the download in its window.
progress = None
# The wallpaper sync() puts on the desktop instead of the current one (the gallery's Enter on another level)
desktop_choice = None
refreshed = None                                    # the wallpaper sync() last put on the desktop
pack = None                                         # (i, n) while fetch_packs() fetches the i-th of n sets


def _marker(folder):
    try:
        return (folder/MARKER).read_text().strip()
    except OSError:
        return None


def profiles(root, level='default'):
    """Every published profile at a background level.

    Bundled files live in the checkout's backgrounds/. Downloaded sets live in
    $XDG_DATA_HOME/p-bloom-wallpapers/sets/<profile>[-<level>]/. A profile is
    `local` when all of its files are present there. A profile that does not
    publish the requested level is offered at Default instead, marked
    `level_missing`; the resolution choice does not depend on the level.
    """
    root = Path(root)
    level = valid_level(level)
    manifest = json.loads((root/'docs/collection/profiles.json').read_text())
    ids = [x['id'] for x in json.loads((root/'docs/collection/catalog.json').read_text())['finalized']]
    out = []
    for base_profile in manifest['profiles']:
        _safe_name(base_profile['id'])
        profile = _at_level(base_profile, level)
        missing = profile is None
        if missing:
            profile = _at_level(base_profile, 'default')
        if profile is None:
            raise ValueError(f"Profile {base_profile['id']} publishes no Default pack")
        shown = 'default' if missing else level
        if [x['id'] for x in profile['files']] != ids:
            raise ValueError(f"Incomplete collection in profile {profile['id']}")
        names = [_safe_name(x['name']) for x in profile['files']]
        if len(set(names)) != len(names):
            raise ValueError('Duplicate wallpaper names in profile')
        if len(profile['size']) != 2 or min(profile['size']) <= 0:
            raise ValueError('Invalid profile dimensions')
        base = root/'backgrounds' if profile.get('bundled') else sets_dir()/set_name(profile['id'], shown)
        paths = [base/n for n in names]
        # A downloaded set counts only if it matches the file list this manifest names: after a theme update that
        # changes some wallpapers, the set is brought up to date (only the changed files are downloaded).
        current = profile.get('bundled') or _marker(base) == set_digest(profile['files'])
        out.append({**{k: v for k, v in profile.items() if k != 'levels'}, 'paths': paths,
                    'local': current and all(x.is_file() for x in paths), 'level': shown, 'level_missing': missing})
    if not any(p['local'] for p in out) and level == 'default':
        raise ValueError('No complete wallpaper set is installed. Reinstall from a complete checkout.')
    return manifest, out


def assess(profile, screens):
    """Physical pixel density for desktop cover, independent of UI scaling."""
    w, h = profile['size']
    paths = profile.get('paths', [])
    # Measure the files users actually have; for a set not downloaded yet,
    # use the byte counts recorded when it was packaged.
    if profile.get('local', True) and paths:
        total = sum(p.stat().st_size for p in paths)
    else:
        total = sum(f.get('bytes', 0) for f in profile['files']) or None
    count = len(profile['files']) if 'files' in profile else len(paths)
    rows = []
    for m in screens:
        fill = max(m['width']/w, m['height']/h)
        crop = max(0., 1 - (m['width']*m['height'])/(w*h*fill*fill))
        rows.append(dict(name=m['name'], width=m['width'], height=m['height'],
                         scale=m['scale'], factor=fill, crop=crop,
                         text_px=profile['min_text_px']*min(1., fill),
                         upscale=fill > 1.000001))
    return dict(profile=profile['id'], label=profile['label'], size=profile['size'],
                local=profile.get('local', True), level=profile.get('level', 'default'),
                total_bytes=total, file_count=count,
                average_bytes=total/count if total and count else None,
                displays=rows, upscale=any(r['upscale'] for r in rows))


def quality_score(option, preferred=None):
    rows = option['displays']
    if not rows:
        return (0, 0, 0, 0, 0, 0, option['profile'])
    # First avoid enlargement on ANY display. Then minimize worst cropping and
    # area-weighted cropping. Among equally suitable sets, prefer fewer bytes,
    # then fewer pixels. Focus changes must never alter the recommendation.
    worst_scale = max(1., max(r['factor'] for r in rows))
    relevant = [r for r in rows if r['name'] == preferred] if preferred else rows
    crop = max(r['crop'] for r in relevant)
    area = sum(r['width']*r['height'] for r in relevant)
    average = sum(r['crop']*r['width']*r['height'] for r in relevant)/area
    # Crops below half a percent are rounding between nominal proportions.
    return (option['upscale'], round(worst_scale, 6), round(max(0, crop-.005), 6), round(average, 6),
            option['total_bytes'] if option['total_bytes'] is not None else math.inf,
            option['size'][0]*option['size'][1], option['profile'])


def recommendation_reason(option, options):
    rows = option['displays']
    if not rows:
        return 'No monitors detected; the desktop will stay unchanged.'
    if option['upscale']:
        return f"No set is large enough; this needs the least enlargement ({max(r['factor'] for r in rows):.2f}×)."
    cheaper = sorted((o for o in options if o['total_bytes'] is not None and option['total_bytes'] is not None and o['total_bytes'] < option['total_bytes']), key=lambda o:o['total_bytes'])
    for other in cheaper:
        enlarged = [r for r in other['displays'] if r['upscale']]
        if enlarged:
            row = max(enlarged, key=lambda r:r['factor'])
            return f"The cheaper set needs {row['factor']:.2f}× enlargement on {row['name']}; this one does not."
        crop = max(r['crop'] for r in other['displays'])
        own_crop = max(r['crop'] for r in rows)
        if crop > own_crop + .01:
            return (f"The cheaper {other['label']} set crops {crop:.0%} of the image; " +
                    ('this set keeps the whole sheet.' if own_crop < .01 else f'this set limits cropping to {own_crop:.0%}.'))
    crop = max(r['crop'] for r in rows)
    if crop > .01:
        return f"Smallest set with the best available fit; mixed screen proportions still crop up to {crop:.0%}."
    return f"Smallest set that fits all {len(rows)} displays without enlargement or cropping."


def plan(root, requested='auto', monitor=None, detected=None, local_only=False, level='default'):
    level = valid_level(level)
    manifest, every = profiles(root, level)
    available = [p for p in every if p['local']] if local_only else every
    if not available:
        # Nothing installed at this level yet: the installed Default sets.
        return {**plan(root, requested, monitor, detected, True, 'default'), 'requested_level': level}
    detected = monitors() if detected is None else detected
    if monitor and monitor not in {m['name'] for m in detected}:
        raise ValueError(f'Monitor {monitor!r} is not connected')
    options = sorted([assess(p, detected) for p in available], key=lambda o: quality_score(o, monitor))
    default = next((p['id'] for p in available if p['id'] == manifest['default']), None) \
        or next(p['id'] for p in available if p['local'])
    recommended = options[0]['profile'] if detected else default
    recommended_option = next((o for o in options if o['profile']==recommended), options[0])
    ratio = recommended_option['size'][0]/recommended_option['size'][1]
    matching = [o for o in options if abs(o['size'][0]/o['size'][1]-ratio) < .000001]
    biggest = max(matching, key=lambda o:(o['size'][0]*o['size'][1], o['total_bytes'] or 0, o['profile']))['profile']
    choice = biggest if requested == 'biggest' else (requested if requested != 'auto' else recommended)
    profile = next((p for p in available if p['id'] == choice), None)
    if profile is None:
        if requested != 'auto' and requested != 'biggest':
            raise ValueError(f'Unavailable profile: {requested}')
        profile = next(p for p in available if p['id'] == default)
        recommended = profile['id']
    chosen = next(o for o in options if o['profile'] == profile['id'])
    warnings = []
    small = [r for r in chosen['displays'] if r['text_px'] < 10]
    if small:
        warnings.append(f"The smallest labels shrink to {min(r['text_px'] for r in small):.1f} screen pixels "
                        "on the largest downscale; a set for that screen is not published.")
    if not detected:
        warnings.append('Monitor detection is unavailable. Using the shipped default; desktop settings will stay unchanged.')
    if len(detected) > 1:
        warnings.append('One shared wallpaper is used on all monitors. The recommendation considers every connected display.')
    if profile['level_missing']:
        warnings.append(f"A {LEVEL_LABELS[level]} background is not published for the {profile['label']} set; "
                        "using its Default background.")
    return dict(profile=profile['id'], recommended=recommended, biggest=biggest,
                reason=recommendation_reason(recommended_option, options), options=options,
                label=profile['label'], size=profile['size'], count=len(profile['paths']),
                level=profile['level'], requested_level=level, set=set_name(profile['id'], profile['level']),
                local=profile['local'],
                screen=detected[0] if detected else None, monitors=detected, warnings=warnings,
                files=[str(p) for p in profile['paths']], hashes=[r['sha256'] for r in profile['files']])


def _manifest_profile(root, profile_id, level='default'):
    manifest, every = profiles(root, level)
    profile = next(p for p in every if p['id'] == profile_id)
    if profile['level_missing']:
        raise ValueError(f"No {LEVEL_LABELS[valid_level(level)]} background is published for {profile_id}")
    return manifest, profile


def _local_copy(root, item):
    """A file already on disk with this name and content (any installed set, or the bundled one), or None."""
    candidates = [root/'backgrounds'/item['name']]
    if sets_dir().is_dir():
        candidates += [d/item['name'] for d in sets_dir().iterdir() if d.is_dir() and not d.name.startswith('.')]
    for path in candidates:
        try:
            if path.is_file() and path.stat().st_size == item['bytes'] and \
                    hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']:
                return path
        except OSError:
            continue
    return None


def fetch(root, profile_id, opener=None, timeout=60, level='default', attempts=3, workers=4):
    """Install one set from its per-file objects, atomically.

    Files the set needs that are already on disk (an older copy of this set, another set, the bundled one) are
    reused when their SHA-256 matches; the rest are downloaded from the manifest's `objects_base`, each checked
    against its own hash (retried a few times), into a staging folder that replaces the set only when complete.
    A theme update that changes a few wallpapers therefore downloads only those files. Each level of a profile is
    its own folder (set_name).
    """
    import threading
    import urllib.request
    from concurrent.futures import ThreadPoolExecutor
    root = Path(root)
    manifest, profile = _manifest_profile(root, profile_id, level)
    if profile.get('bundled'):
        return sets_dir()
    base = manifest.get('objects_base')
    if not isinstance(base, str) or not base.startswith('https://') or not base.endswith('/'):
        raise ValueError('The wallpaper manifest names no download location')
    folder = set_name(profile_id, profile['level'])
    files = profile['files']
    target = sets_dir()/folder
    sets_dir().mkdir(parents=True, exist_ok=True)
    opener = opener or urllib.request.urlopen
    with tempfile.TemporaryDirectory(prefix='.download-', dir=sets_dir()) as work:
        work = Path(work)
        stage = work/folder
        stage.mkdir()
        needed = []
        for item in files:
            name = _safe_name(item['name'])
            local = _local_copy(root, item)
            if local:
                try:
                    os.link(local, stage/name)
                except OSError:
                    shutil.copyfile(local, stage/name)
            else:
                needed.append(item)
        total = sum(f['bytes'] for f in needed)
        state = dict(done=0)
        lock = threading.Lock()

        def report(phase):
            if progress:
                progress(phase=phase, done=state['done'], total=total, label=profile.get('label', profile_id),
                         level=profile['level'], **(dict(pack=pack[0], packs=pack[1]) if pack else {}))

        def get(item):
            url = object_url(base, item)
            for attempt in range(attempts):
                got = 0
                try:
                    request = urllib.request.Request(url, headers={'User-Agent': 'p-bloom-wallpapers'})
                    digest = hashlib.sha256()
                    tmp = stage/('.' + item['name'] + '.part')
                    with opener(request, timeout=timeout) as response, tmp.open('wb') as out:
                        while chunk := response.read(1 << 18):
                            got += len(chunk)
                            if got > item['bytes']:
                                raise ValueError(f"{item['name']} is larger than published")
                            digest.update(chunk)
                            out.write(chunk)
                            with lock:                  # one report at a time: they are lines on a pipe
                                state['done'] += len(chunk)
                                report('download')
                    if got != item['bytes'] or digest.hexdigest() != item['sha256']:
                        raise ValueError(f"{item['name']} failed its SHA-256 check")
                    tmp.replace(stage/item['name'])
                    return
                except (OSError, ValueError):
                    with lock:
                        state['done'] -= got
                    if attempt == attempts - 1:
                        raise
                    time.sleep(1 + attempt)

        report('download')
        with ThreadPoolExecutor(workers) as pool:
            list(pool.map(get, needed))
        report('install')
        missing = [f['name'] for f in files if not (stage/f['name']).is_file()]
        if missing:
            raise ValueError(f'{folder} is missing {len(missing)} wallpapers; nothing was installed')
        (stage/MARKER).write_text(set_digest(files) + '\n')
        if target.exists():
            os.replace(target, work/'previous')
        os.replace(stage, target)
    return target


def optimal_packs(root, screens, monitor=None):
    """The packs DOWNLOAD OPTIMAL fetches: the optimal set for all screens together (the one automatic selection uses;
    Omarchy shows one wallpaper on every monitor) at every intensity it is published at. A list of dicts: profile,
    level, set, label, bytes, local. (Sets for each monitor on its own wait for per-monitor wallpapers in Omarchy.)"""
    pid = plan(root, 'auto', monitor, screens)['profile']
    packs = []
    for lv in LEVELS:
        entry = next(x for x in profiles(root, lv)[1] if x['id'] == pid)
        if entry['level_missing']:
            continue
        packs.append(dict(profile=pid, level=lv, set=set_name(pid, lv), label=entry['label'],
                          bytes=0 if entry.get('bundled') else sum(f['bytes'] for f in entry['files']),
                          local=entry['local']))
    return packs


def fetch_packs(root, packs):
    """Download the packs that are not installed yet, one after another; the ones that fail are returned (with
    why), the rest stay installed."""
    global pack
    missing = [k for k in packs if not k['local']]
    failed = []
    for i, k in enumerate(missing):
        pack = (i + 1, len(missing))
        try:
            fetch(root, k['profile'], level=k['level'])
        except Exception as exc:  # network, disk, checksum or archive errors alike
            failed.append((k, f'{exc}'))
        finally:
            pack = None
    return failed


def prune(current, keep=3, pinned=()):
    """Keep the `keep` most recently used downloaded sets (docking back and
    forth should not re-download); `current` is marked as just used. Sets in
    `pinned` (DOWNLOAD OPTIMAL's) are kept besides them."""
    base = sets_dir()
    if not base.is_dir():
        return
    mark = base/current
    if mark.is_dir():
        os.utime(mark)
    sets = sorted((p for p in base.iterdir() if p.is_dir() and not p.is_symlink() and not p.name.startswith('.')
                   and p.name not in pinned), key=lambda p: p.stat().st_mtime, reverse=True)
    for path in sets[keep:]:
        shutil.rmtree(path)


def current_dir():
    # Omarchy itself uses this path, not XDG_STATE_HOME.
    return Path.home()/'.local/state/omarchy/current'


def active_theme(current):
    try:
        return (current/'theme.name').read_text().strip() == 'p-bloom'
    except OSError:
        return False


def setup_path():
    return Path(os.environ.get('XDG_STATE_HOME', Path.home()/'.local/state'))/'p-bloom-wallpapers/setup.json'


def read_setup():
    try:
        value = json.loads(setup_path().read_text())
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def save_setup(data):
    target = setup_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=target.parent, prefix='.setup-')
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(data, stream, indent=2)
            stream.write('\n')
        os.replace(name, target)
    finally:
        Path(name).unlink(missing_ok=True)


def announce(p, apply):
    from wallpaper_setup_cli import choose_profile
    return choose_profile(p, apply)


def refresh_desktop(target, current):
    subprocess.run(['omarchy','theme','bg','set',str(target)],check=True,timeout=15)
    # The shell ignores set(path) when the path is unchanged. Use its existing
    # theme-transition API with an uncached snapshot and the same final path.
    # The canonical link stays intact for Omarchy's next-background command.
    shell=shutil.which('omarchy-shell')
    if not shell:return
    def payload(name):
        path=current/'theme'/name
        return base64.b64encode(path.read_bytes() if path.is_file() else b'').decode()
    with tempfile.TemporaryDirectory(prefix='p-bloom-refresh-') as directory:
        snapshot=Path(directory)/target.name
        shutil.copyfile(target,snapshot)
        result=subprocess.run(['omarchy','shell','-q','background','themeTransition','',str(snapshot),str(target),
                               payload('colors.toml'),payload('shell.toml')],check=False,timeout=10)
        if result.returncode==0:time.sleep(3)


def sync(p, current=None):
    """Replace only this collection's files in Omarchy's disposable theme stage."""
    global refreshed
    current = current or current_dir()
    if not p['screen'] or not active_theme(current):
        return False
    theme = current/'theme'
    destination = theme/'backgrounds'
    # Never follow a theme stage symlink into a source checkout.
    if theme.is_symlink() or destination.is_symlink() or not destination.is_dir():
        raise ValueError('Expected a regular staged Omarchy backgrounds directory')
    sources = [Path(x) for x in p['files']]
    for src, digest in zip(sources, p['hashes'], strict=True):
        if hashlib.sha256(src.read_bytes()).hexdigest() != digest:
            raise ValueError(f'Wallpaper changed since packaging: {src.name}')
    selected = desktop_choice or (Path(os.readlink(current/'background')).name if (current/'background').is_symlink() else None)
    changed = False
    # Stage the whole set first so an out-of-space failure cannot leave half copied.
    with tempfile.TemporaryDirectory(prefix='.p-bloom-', dir=theme) as work:
        stage = Path(work)
        pending = []
        for src, digest in zip(sources, p['hashes'], strict=True):
            target = destination/src.name
            if target.exists() and not target.is_symlink() and hashlib.sha256(target.read_bytes()).hexdigest() == digest:
                continue
            shutil.copyfile(src, stage/src.name)
            pending.append(src.name)
        for name in pending:
            os.replace(stage/name, destination/name)
        changed = bool(pending)
    # Keep custom user wallpapers selected. Owned sheets always use stage paths,
    # so Omarchy's next-background operation can match its current-file list.
    if selected in {s.name for s in sources} and (changed or (current/'background').resolve() != (destination/selected).resolve()):
        refresh_desktop(destination/selected,current)
        refreshed = selected
    return changed


def notify_selection(p, desktop):
    notifier = shutil.which('omarchy-notification-send')
    fallback = shutil.which('notify-send')
    if not notifier and not fallback:
        return
    resolution=' × '.join(map(str,p['size']))
    title=('Optimal desktop wallpaper resolution applied' if p['profile']==p['recommended']
           else 'Desktop wallpaper resolution applied')
    title+=': '+resolution
    if p.get('level','default')!='default':
        title+=f" · {LEVEL_LABELS[p['level']]} background"
    if not desktop:
        return
    scope=''
    command=shutil.which('p-bloom-wallpapers')
    if notifier and command:
        args=[notifier,'--app-name','p(bloom) Wallpapers','-t','9000',title,
              scope+'Click to change settings.', '--exec',command,'--configure']
    else:
        args=[notifier or fallback,title,scope+'Settings: p-bloom-wallpapers --configure']
    try:
        subprocess.run(args,check=False,timeout=5,capture_output=True)
    except (OSError,subprocess.SubprocessError):
        pass  # A notification failure must never prevent the gallery opening.


def saved_level(previous, root):
    """The remembered background level (Default for new or foreign settings)."""
    if previous.get('version') != 6 or previous.get('root') != str(root):
        return 'default'
    return valid_level(previous.get('level', 'default'))


def initialize(root, p, requested='auto', monitor=None, configure=False, level=None):
    lock=setup_path().with_suffix('.lock')
    lock.parent.mkdir(parents=True,exist_ok=True)
    with lock.open('a') as handle:
        fcntl.flock(handle,fcntl.LOCK_EX)
        return _initialize(root,p,requested,monitor,configure,level)


def _fallback_plan(root, monitor, screens, level, previous):
    """An installed set to show while the chosen one cannot be downloaded.

    Keeps the set already on the desktop when it is still installed (same
    background level, same resolution); otherwise the best installed set at
    the requested level, otherwise the best installed Default set.
    """
    shown = previous.get('selected'), valid_level(previous.get('selected_level', 'default'))
    if shown[0]:
        _, every = profiles(root, shown[1])
        if any(p['id'] == shown[0] and p['local'] and p['level'] == shown[1] for p in every):
            return plan(root, shown[0], monitor, screens, local_only=True, level=shown[1])
    return plan(root, 'auto', monitor, screens, local_only=True, level=level)


def ensure_local(root, p, requested, monitor, previous):
    """Download the chosen set if needed; on any failure keep a local set.

    A failed download is not retried for RETRY_SECONDS (per set), so the
    10-second monitor watcher does not hammer the network while offline.
    """
    failed = dict(previous.get('failed') or {})
    if p['local'] or not p['screen']:
        return {**p, 'failed': failed}
    level = p.get('level', 'default')
    key = set_name(p['profile'], level)
    now = time.time()
    if now - failed.get(key, 0) >= RETRY_SECONDS:
        try:
            if level == 'default':
                fetch(root, p['profile'])
            else:
                fetch(root, p['profile'], level=level)
            failed.pop(key, None)
            return {**plan(root, requested, monitor, p['monitors'], level=p.get('requested_level', level)),
                    'failed': failed}
        except Exception as exc:  # network, disk, checksum or archive errors alike
            failed[key] = now
            reason = f'{exc}'
    else:
        reason = 'a recent download failed'
    fallback = _fallback_plan(root, monitor, p['monitors'], level, previous)
    what = p['label'] + ('' if level == 'default' else f', {LEVEL_LABELS[level]} background,')
    got = fallback['label'] + ('' if fallback['level'] == 'default' else f" ({LEVEL_LABELS[fallback['level']]})")
    fallback['warnings'].insert(0, f"The {what} set could not be downloaded ({reason}); "
                                   f"using the installed {got} set. It will be retried automatically.")
    return {**fallback, 'fallback': key, 'failed': failed}


def _initialize(root, p, requested='auto', monitor=None, configure=False, level=None):
    previous = read_setup()
    pinned = previous.get('pinned', [])
    level = valid_level(level or saved_level(previous, root))
    # Old chooser preferences migrate to automatic; only explicit new settings
    # can establish a manual override.
    if previous.get('version') != 6 or previous.get('root') != str(root):
        requested='auto'
    p = ensure_local(root, plan(root, requested, monitor, p['monitors'], level=level), requested, monitor, previous)
    desktop=bool(p['screen']) and active_theme(current_dir())
    if configure:
        # Sizes and "download" markers differ per level: give the settings
        # screen the resolution list of every level.
        by_level={lv:plan(root,requested,monitor,p['monitors'],level=lv)['options'] for lv in LEVELS}
        # the gallery's menu: the monitors, the set in use, and the optimal set's packs
        choice=announce({**p,'setting':requested,'setting_level':level,'options_by_level':by_level,
                         'optimal':plan(root,'auto',monitor,p['monitors'],level=level)['profile'],
                         'packs':optimal_packs(root,p['monitors'],monitor)}, desktop)
        if not choice:
            return None
        if isinstance(choice, str):
            choice = {'profile': choice, 'level': level}
        if (not isinstance(choice, dict) or choice.get('profile') not in {'auto',*(o['profile'] for o in p['options'])}
                or choice.get('level') not in LEVELS):
            raise ValueError('Invalid wallpaper setting')
        requested, level = choice['profile'], choice['level']
        failed_packs = []
        if choice.get('download') == 'optimal':
            packs = optimal_packs(root, p['monitors'], monitor)
            pinned = [k['set'] for k in packs]
            failed_packs = [f"The {k['label']} {LEVEL_LABELS[k['level']]} set could not be downloaded ({reason})."
                            for k, reason in fetch_packs(root, packs)]
        p=ensure_local(root,plan(root,requested,monitor,p['monitors'],level=level),requested,monitor,previous)
        p['warnings'] = failed_packs + p['warnings']
    updated=sync(p)
    shown = p.get('level', 'default')
    if p['screen']:
        changed=(previous.get('version')!=6 or previous.get('root')!=str(root)
                 or previous.get('selected')!=p['profile']
                 or previous.get('selected_level','default')!=shown
                 or (desktop and (updated or previous.get('desktop_selected')!=set_name(p['profile'], shown))))
        save_setup(dict(version=6,root=str(root),profile=requested,level=level,monitor=monitor,
                        selected=p['profile'],selected_level=shown,
                        desktop_selected=set_name(p['profile'], shown) if desktop else previous.get('desktop_selected'),
                        failed=p.get('failed',{}),pinned=pinned))
        if desktop and not p.get('fallback'):
            prune(set_name(p['profile'], shown), pinned=pinned)
        if changed:
            notify_selection(p,desktop)
    return p
