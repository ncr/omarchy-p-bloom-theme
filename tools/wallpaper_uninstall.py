"""Remove the p(bloom) Wallpapers companion.

Used by `companion/install.py --uninstall`, and by the desktop service when the theme itself is gone (Omarchy's
Remove > Theme deletes the theme's folder and has no hook for it), so removing the theme removes its app too. It lives
with the app's runtime files because the theme checkout may no longer exist when it runs.

Only files the companion wrote are removed: each is recognised by MARKER or by its window class. Downloaded sets and
the settings stay unless `purge` is set.
"""
import os
from pathlib import Path
import shutil
import subprocess

from wallpaper_runtime import RUNTIME

MARKER = '# p(bloom) Wallpapers companion'
ICON_SIZES = (16, 24, 32, 48, 64, 128, 256, 512)
SERVICE = 'p-bloom-wallpapers-desktop.service'


def paths(prefix):
    prefix = Path(prefix)
    return dict(
        app=prefix/'share/p-bloom-wallpapers',
        launcher=prefix/'bin/p-bloom-wallpapers',
        desktop=prefix/'share/applications/p-bloom-wallpapers.desktop',
        icons=[prefix/f'share/icons/hicolor/{n}x{n}/apps/p-bloom-wallpapers.png' for n in ICON_SIZES],
        service=Path.home()/'.config/systemd/user'/SERVICE,
        hook=Path.home()/'.config/omarchy/hooks/theme-set.d/p-bloom-wallpapers',
        local=Path(prefix).resolve() == (Path.home()/'.local').resolve(),
    )


def owned(path, mark=MARKER):
    try:
        return path.is_file() and mark in path.read_text()
    except (OSError, UnicodeDecodeError):
        return False


def remove(prefix, purge=False, from_service=False):
    """Remove the app, its menu entry, icons, hook and desktop service; with `purge`, also the downloaded sets and the
    settings. From the service itself it is disabled without being stopped, and the caller exits afterwards."""
    p = paths(prefix)
    if owned(p['launcher']):
        p['launcher'].unlink()
    if owned(p['desktop'], 'StartupWMClass=p-bloom-wallpapers'):
        p['desktop'].unlink()
    for icon in p['icons']:
        icon.unlink(missing_ok=True)
    if p['local'] and owned(p['hook']):
        p['hook'].unlink()
    app = p['app']
    for name in (*RUNTIME, 'wallpaper_setup_ui.py', 'wallpaper-viewer.ini', 'install.json', 'p-bloom-wallpapers', 'launch.log'):
        (app/name).unlink(missing_ok=True)
    shutil.rmtree(app/'__pycache__', ignore_errors=True)
    if purge:
        data = Path(os.environ.get('XDG_DATA_HOME', Path.home()/'.local/share'))/'p-bloom-wallpapers'
        state = Path(os.environ.get('XDG_STATE_HOME', Path.home()/'.local/state'))/'p-bloom-wallpapers'
        shutil.rmtree(data/'sets', ignore_errors=True)
        shutil.rmtree(state, ignore_errors=True)
    if app.is_dir() and not any(app.iterdir()):
        app.rmdir()
    refresh = shutil.which('update-desktop-database')
    if refresh and p['desktop'].parent.is_dir():
        subprocess.run([refresh, str(p['desktop'].parent)], check=False)
    # the service last: stopping it from inside would end this process half-way
    if p['local'] and owned(p['service']):
        systemctl = ['systemctl', '--user']
        subprocess.run([*systemctl, 'disable', *(() if from_service else ('--now',)), SERVICE], check=False)
        p['service'].unlink()
        subprocess.run([*systemctl, 'daemon-reload'], check=False)


def notify(title, body):
    for tool in ('omarchy-notification-send', 'notify-send'):
        if shutil.which(tool):
            subprocess.run([tool, '--app-name', 'p(bloom) Wallpapers', title, body], check=False)
            return
