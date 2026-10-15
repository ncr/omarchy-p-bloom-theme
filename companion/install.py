#!/usr/bin/env python3
"""Install the optional p(bloom) Wallpapers companion in a user-local prefix."""
import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from wallpaper_uninstall import ICON_SIZES, MARKER, RUNTIME, remove  # noqa: E402


def desktop_quote(value):
    # Desktop Exec has its own escaping, distinct from shell quoting.
    value = str(value).replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`').replace('$', '\\$').replace('%', '%%')
    return '"' + value + '"'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--prefix', type=Path, default=Path.home()/'.local')
    ap.add_argument('--uninstall', action='store_true')
    ap.add_argument('--purge', action='store_true', help='With --uninstall: also delete the downloaded sets and the settings')
    ap.add_argument('--no-launch', action='store_true', help='Install without opening the app')
    args = ap.parse_args()
    prefix = args.prefix.expanduser().resolve()
    app = prefix/'share/p-bloom-wallpapers'
    launcher = prefix/'bin/p-bloom-wallpapers'
    desktop = prefix/'share/applications/p-bloom-wallpapers.desktop'
    # the app icon in the user's hicolor theme, one PNG per size (tools/make_icon.py)
    icons = [(prefix/f'share/icons/hicolor/{n}x{n}/apps/p-bloom-wallpapers.png', ROOT/f'companion/icons/p-bloom-wallpapers-{n}.png')
             for n in ICON_SIZES]
    local = prefix == (Path.home()/'.local').resolve()
    service = Path.home()/'.config/systemd/user/p-bloom-wallpapers-desktop.service'
    if local and service.exists() and MARKER not in service.read_text():
        ap.error(f'Refusing to replace an unrelated service: {service}')
    hook = Path.home()/'.config/omarchy/hooks/theme-set.d/p-bloom-wallpapers'
    if local and hook.exists() and MARKER not in hook.read_text():
        ap.error(f'Refusing to replace an unrelated hook: {hook}')
    if args.uninstall:
        if not (app/'install.json').is_file():
            ap.error('No companion installation recorded at this prefix')
        remove(prefix, purge=args.purge)
        print('Companion removed.' + (' Downloaded sets and settings deleted.' if args.purge else
              ' Downloaded sets and settings kept (--purge deletes them).') + ' The theme is unchanged.')
    else:
        try:
            import gi
            gi.require_version('Gtk', '4.0')
        except (ImportError, ValueError):
            ap.error('The gallery needs GTK 4 and python-gobject; on Omarchy run: omarchy pkg add python-gobject gtk4')
        if launcher.exists() and MARKER not in launcher.read_text():
            ap.error(f'Refusing to overwrite an unrelated executable: {launcher}')
        if desktop.exists() and 'StartupWMClass=p-bloom-wallpapers' not in desktop.read_text():
            ap.error(f'Refusing to overwrite an unrelated desktop entry: {desktop}')
        for directory in (app,launcher.parent,desktop.parent):directory.mkdir(parents=True,exist_ok=True)
        print('Installing p(bloom) Wallpapers, its application-menu entry and automatic format selection.', flush=True)
        for old in ('wallpaper_setup_ui.py', 'wallpaper-viewer.ini'):
            (app/old).unlink(missing_ok=True)
        for name in RUNTIME:
            shutil.copy2(ROOT/'tools'/name,app/name)
        launcher.write_text('#!/bin/sh\n'+MARKER+'\n'+
            'export PBLOOM_THEME_ROOT='+shlex.quote(str(ROOT))+'\n'+
            'exec '+shlex.quote(sys.executable)+' '+shlex.quote(str(app/'view_wallpapers.py'))+
            ' --collection finalized "$@"\n')
        launcher.chmod(0o755)
        for target, source in icons:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        desktop.write_text('[Desktop Entry]\nType=Application\nName=p(bloom) Wallpapers\n'
            'Comment=Browse the p(bloom) wallpaper collection\n'
            'Exec='+desktop_quote(launcher)+'\nIcon=p-bloom-wallpapers\n'
            'Terminal=false\nCategories=Graphics;Viewer;\nActions=Settings;\n'
            'Keywords=wallpaper;tapety;p-bloom;pbloom;bloom;blueprint;\nStartupWMClass=p-bloom-wallpapers\n'
            '\n[Desktop Action Settings]\nName=Wallpaper settings\n'
            'Exec='+desktop_quote(launcher)+' --configure\n')
        if local and shutil.which('omarchy'):
            hook_source = app/'p-bloom-wallpapers'
            hook_source.write_text('#!/bin/sh\n'+MARKER+'\n'
                '[ "$1" = p-bloom ] || exit 0\nexec '+shlex.quote(str(launcher))+' --sync-backgrounds\n')
            subprocess.run(['omarchy', 'hook', 'install', 'theme-set', str(hook_source)], check=True)
        if local:
            def unit_quote(value):
                return '"'+str(value).replace('\\','\\\\').replace('"','\\"').replace('%','%%')+'"'
            service.parent.mkdir(parents=True,exist_ok=True)
            service.write_text(MARKER+'\n[Unit]\nDescription=Automatic p(bloom) desktop wallpaper resolution\n'
                '\n[Service]\nType=simple\nExecStart=:'+
                ' '.join(unit_quote(x) for x in (sys.executable,app/'wallpaper_desktop.py','--root',ROOT))+
                '\nRestart=on-failure\nRestartSec=5\n'
                '\n[Install]\nWantedBy=default.target\n')
            subprocess.run(['systemctl','--user','daemon-reload'],check=True)
            subprocess.run(['systemctl','--user','enable',service.name],check=True)
            subprocess.run(['systemctl','--user','restart',service.name],check=True)
            print('Automatic desktop updates enabled (monitor checks every 10 seconds).')
        (app/'install.json').write_text(json.dumps({'theme_root':str(ROOT),'prefix':str(prefix),'version':6},indent=2)+'\n')
        print(f'Installed p(bloom) Wallpapers: {launcher}\nWallpaper source: {ROOT}')
    refresh = shutil.which('update-desktop-database')
    if refresh and desktop.parent.is_dir():
        subprocess.run([refresh,str(desktop.parent)],check=True)
    if not args.uninstall and not args.no_launch and local:
        if os.environ.get('WAYLAND_DISPLAY') or os.environ.get('DISPLAY'):
            log = app/'launch.log'
            with log.open('a') as stream:
                subprocess.Popen([str(launcher)], stdout=stream, stderr=stream, start_new_session=True)
            print('Opening p(bloom) Wallpapers. Resolution is selected automatically; a notification links to settings.')
        else:
            print('No graphical session detected. Open p(bloom) Wallpapers from the application menu later.')


if __name__ == '__main__':main()
