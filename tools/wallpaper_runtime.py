"""The app's own files: what the installer copies, and keeping that copy in step with the theme checkout.

The installed runtime is a copy of these files from the checkout's tools/ (so the app keeps working while the checkout
is updated). `omarchy theme update` only pulls the checkout, so the desktop service and the launcher compare the copy
with the checkout they were installed from and refresh it when it differs, then restart into the new code. Only the
files listed in RUNTIME are copied, and only from the theme root recorded at install time.
"""
import hashlib
from pathlib import Path
import runpy
import shutil
import time

RUNTIME = ('view_wallpapers.py', 'gallery.py', 'wallpaper_profiles.py', 'wallpaper_desktop.py', 'wallpaper_setup_cli.py',
           'settings_ui.py', 'wallpaper_uninstall.py', 'wallpaper_runtime.py')


def _digest(path):
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except OSError:
        return None


def wanted(root):
    """The runtime file list of the checkout (it may name files this copy doesn't know yet)."""
    try:
        names = runpy.run_path(str(Path(root)/'tools/wallpaper_runtime.py'))['RUNTIME']
    except Exception:  # an unreadable or partial checkout: keep what is installed
        return ()
    return tuple(n for n in names if isinstance(n, str) and n.endswith('.py') and n == Path(n).name)


def stale(app, root):
    """Names of runtime files whose installed copy differs from the checkout's."""
    tools = Path(root)/'tools'
    return [n for n in wanted(root) if (tools/n).is_file() and _digest(tools/n) != _digest(Path(app)/n)]


def settled(root, names, quiet=10):
    """No Git operation is running in the checkout and none of these files changed in the last `quiet` seconds, so a
    pull is not half-way (a mix of old and new files may not even import)."""
    root = Path(root)
    if (root/'.git/index.lock').exists():
        return False
    try:
        return all(time.time() - (root/'tools'/n).stat().st_mtime >= quiet for n in names)
    except OSError:
        return False


def refresh(app, root, quiet=10):
    """Copy the changed runtime files from the checkout into the app folder; each file is replaced atomically.
    Nothing is copied while the checkout is still changing; the next call picks it up."""
    app, tools = Path(app), Path(root)/'tools'
    names = stale(app, root)
    if not names or not settled(root, wanted(root), quiet):
        return []
    for name in names:
        tmp = app/f'.{name}.new'
        shutil.copy2(tools/name, tmp)
        tmp.replace(app/name)
    if names:
        shutil.rmtree(app/'__pycache__', ignore_errors=True)
    return names
