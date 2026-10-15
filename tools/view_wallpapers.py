#!/usr/bin/env python3
"""p(bloom) Wallpapers: the full-screen gallery (tools/gallery.py), its settings and the desktop service entry points."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import threading

ROOT = Path(os.environ.get('PBLOOM_THEME_ROOT', Path(__file__).resolve().parents[1])).resolve()
DEVELOPMENT = ROOT / 'concepts/development'
EXTENSIONS = {'.webp', '.png', '.jpg', '.jpeg'}


def collection(directory):
    """Only numbered wallpaper masters (01-, 001-, b01-), never crops or thumbnails."""
    return sorted(p for p in directory.iterdir()
                  if p.is_file() and p.suffix.lower() in EXTENSIONS
                  and re.match(r'^(\d{2,3}|b\d{2})-', p.name))


def finalized_collection():
    """Use the retained registry; a clean checkout shows the complete shipped set.

    The generated ranking gallery is optional and is not a runtime dependency.
    Rejected Century studies are never discovered by scanning render folders.
    """
    registry = ROOT / 'docs/collection/catalog.json'
    if not registry.exists():
        return collection(ROOT / 'backgrounds')
    files = []
    for entry in json.loads(registry.read_text())['finalized']:
        source = (ROOT / entry['source']).resolve()
        if not source.is_relative_to(ROOT):
            raise ValueError('Collection source must be inside the theme checkout')
        if not source.is_file():
            source = ROOT / 'backgrounds' / source.name
        if source.is_file():
            files.append(source)
    return files


def select(files, query):
    if query is None:
        return files[0]
    if query.isdecimal():
        matches = [p for p in files if p.name.split('-')[0].isdecimal() and int(p.name.split('-')[0]) == int(query)]
    else:
        matches = [p for p in files if query.casefold() in p.name.casefold()]
    if len(matches) != 1:
        raise ValueError(f'Expected one wallpaper for {query!r}; found {len(matches)}. Use --list.')
    return matches[0]


def display_name(path):
    """09-tether-climber.webp -> Tether Climber"""
    stem = Path(path).stem
    return stem.split('-', 1)[-1].replace('-', ' ').title()


def notify(title, body=''):
    sender = shutil.which('omarchy-notification-send') or shutil.which('notify-send')
    if sender:
        # a short confirmation: without -t Omarchy keeps a notification until it is dismissed
        args = ([sender, '--app-name', 'p(bloom) Wallpapers', '-t', '4000', title, body] if 'omarchy' in sender
                else [sender, '-t', '4000', title, body])
        subprocess.run(args, check=False, capture_output=True, timeout=5)


def set_desktop(path):
    """Show one wallpaper on the desktop, from p(bloom)'s staged backgrounds (so Omarchy's next-background keeps working)."""
    import wallpaper_profiles as wp
    current = wp.current_dir()
    if not wp.active_theme(current):
        notify('p(bloom) is not the active theme', 'Choose p(bloom) in Omarchy\'s theme menu, then press Enter again.')
        return
    target = current/'theme/backgrounds'/Path(path).name
    if not target.is_file():
        notify('This wallpaper is not on the desktop set yet', 'Its set is still downloading; try again in a moment.')
        return
    wp.refresh_desktop(target, current)
    notify(f'Desktop wallpaper: {display_name(path)}')


def follow_checkout():
    """The installed app is a copy of the checkout's tools/; after `omarchy theme update` it refreshes itself from the
    checkout it was installed from (PBLOOM_THEME_ROOT, set by the launcher) and restarts into the new code."""
    here = Path(__file__).resolve().parent
    if 'PBLOOM_THEME_ROOT' not in os.environ or here == ROOT/'tools':
        return
    try:
        import wallpaper_runtime
        if wallpaper_runtime.refresh(here, ROOT):
            os.execv(sys.executable, [sys.executable, str(here/'view_wallpapers.py'), *sys.argv[1:]])
    except (ImportError, OSError):
        return


def main():
    follow_checkout()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('start', nargs='?', help='Wallpaper number or name, e.g. 9 or tether')
    ap.add_argument('--collection', choices=['development', 'finalized'], default='development',
                    help='Finalized reads the retained collection, with shipped backgrounds as fallback')
    ap.add_argument('--dir', type=Path, help='View a different render directory')
    ap.add_argument('--render', action='store_true', help='Regenerate the development set before opening')
    ap.add_argument('--list', action='store_true', help='List the selected collection and exit')
    ap.add_argument('--configure', action='store_true', help='Change wallpaper settings: background level and resolution')
    ap.add_argument('--monitor', help="Prefer this monitor's proportions; assess resolution on all monitors")
    ap.add_argument('--show-plan', action='store_true', help='Print automatic setup as JSON without changing anything')
    ap.add_argument('--sync-backgrounds', action='store_true', help='Automatically match the p(bloom) desktop to connected monitors without opening the viewer')
    ap.add_argument('--set-desktop', type=Path, metavar='FILE', help='Make this wallpaper the desktop background (the gallery\'s Enter key)')
    ap.add_argument('--print-files', action='store_true', help='With --configure or --level: print the chosen set as JSON instead of opening the gallery (the gallery\'s S and ↑ ↓ keys)')
    ap.add_argument('--level', choices=['muted', 'default', 'vivid'], help='With --print-files: the set at this background level, downloaded if needed; changes no setting (the gallery\'s ↑ ↓)')
    ap.add_argument('--save-level', choices=['muted', 'default', 'vivid'], help='Save the background level, keeping the resolution setting (the gallery\'s Enter on another level)')
    args = ap.parse_args()
    if args.set_desktop and not args.save_level:
        set_desktop(args.set_desktop)
        return
    directory = args.dir.expanduser().resolve() if args.dir else DEVELOPMENT
    if args.render and args.collection == 'finalized':
        ap.error('Render sources separately; --render only supports the development collection')
    if args.render:
        subprocess.run([sys.executable, str(ROOT/'tools/make_wallpapers.py'),
                        '--out', str(directory)], check=True)
    # A fresh checkout can still browse the shipped set without rendering.
    if args.dir is None and not directory.is_dir():
        directory = ROOT / 'backgrounds'
    try:
        retained = args.collection == 'finalized' and args.dir is None
        profile_plan = None
        if retained and (ROOT/'docs/collection/profiles.json').is_file():
            import wallpaper_profiles as wp
            previous = wp.read_setup()
            requested = previous.get('profile','auto') if previous.get('version')==6 and previous.get('root')==str(ROOT) else 'auto'
            level = wp.saved_level(previous, ROOT)
            if requested != 'auto':
                _, available = wp.profiles(ROOT)
                if requested not in {p['id'] for p in available}:
                    requested = 'auto'
            monitor = args.monitor or previous.get('monitor')
            detected = wp.monitors()
            # A remembered external screen may be unplugged; explicit CLI typos
            # remain errors, but normal launches fall back to a connected screen.
            if monitor and not args.monitor and monitor not in {m['name'] for m in detected}:
                monitor = None
            # --list is read-only: it shows installed files and downloads nothing.
            profile_plan = wp.plan(ROOT, requested, monitor, detected, local_only=args.list, level=level)
            if args.show_plan:
                print(json.dumps(profile_plan, indent=2))
                return
            if args.sync_backgrounds:
                wp.initialize(ROOT, profile_plan, requested, monitor)
                return
            files = [Path(p) for p in profile_plan['files']]
        else:
            if args.configure or args.monitor or args.show_plan or args.sync_backgrounds:
                ap.error('Monitor profiles require the packaged finalized collection')
            files = finalized_collection() if retained else collection(directory)
        if not files:
            raise ValueError(f'No numbered wallpapers in {directory}')
        if retained and args.start and args.start.isdecimal():
            index = int(args.start) - 1
            if not 0 <= index < len(files):
                raise ValueError(f'Wallpaper position must be between 1 and {len(files)}')
            first = files[index]
        else:
            first = select(files, args.start)
    except (OSError, ValueError) as exc:
        ap.error(str(exc))
    if args.list:
        if profile_plan:
            # Status on stderr; stdout stays one path per line.
            shown = wp.LEVEL_LABELS[profile_plan.get('level', 'default')]
            wanted = wp.LEVEL_LABELS[profile_plan.get('requested_level', 'default')]
            note = '' if shown == wanted else f' ({wanted} not installed yet)'
            print(f"p(bloom): {profile_plan['label']}, {shown} background{note}, "
                  f"{'automatic' if requested == 'auto' else 'manual'} resolution", file=sys.stderr)
        print('\n'.join(str(p) for p in files))
        return
    try:
        import gallery
    except (ImportError, ValueError) as exc:
        ap.error(f'The gallery needs GTK 4 and python-gobject (part of Omarchy): {exc}')
    # in a graphical session, settings are the gallery's menu: --configure opens the gallery with the menu showing
    in_gallery = bool(profile_plan) and args.configure and not args.print_files and graphical()
    if profile_plan:
        try:
            import wallpaper_setup_cli as cli
            if os.environ.get('PBLOOM_SETTINGS_PIPE'):

                def report(**info):
                    try:
                        print(cli.PROGRESS_PREFIX + json.dumps(info), flush=True)
                    except OSError:                      # the gallery closed: the download goes on
                        wp.progress = None
                wp.progress = report
            if args.level and args.print_files:
                # only for viewing: no setting, desktop or notification changes
                shown = wp.ensure_local(ROOT, wp.plan(ROOT, requested, monitor, detected, level=args.level),
                                        requested, monitor, previous)
                print(cli.FILES_PREFIX + json.dumps({'files': shown['files'], 'level': shown.get('level', 'default')}),
                      flush=True)
                return
            if args.save_level:
                wp.notify_selection = lambda *_: None            # Enter's own notification names the wallpaper
                if args.set_desktop:
                    wp.desktop_choice = args.set_desktop.name   # the level's set goes on with this wallpaper showing
            chosen_plan = wp.initialize(ROOT, profile_plan, requested, monitor, args.configure and not in_gallery,
                                        level=args.save_level)
            if not chosen_plan:
                return
            if args.save_level and args.set_desktop:
                if wp.refreshed == args.set_desktop.name:
                    notify(f'Desktop wallpaper: {display_name(args.set_desktop)}')
                else:
                    set_desktop(args.set_desktop)               # p(bloom) not active, or the set still downloading
            if args.print_files:
                try:
                    print(cli.FILES_PREFIX + json.dumps({'files': [str(f) for f in chosen_plan['files']],
                                                         'level': chosen_plan.get('level', 'default')}), flush=True)
                except OSError:
                    pass
                return
            # Preserve the selected sheet when an optimal format changes.
            files = [Path(p) for p in chosen_plan['files']]
            first = next((p for p in files if p.name == first.name), files[0])
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            ap.error(str(exc))
    gallery.run(files, first,
                set_desktop=enter if profile_plan else None,
                settings=open_settings if profile_plan else None,
                open_settings=in_gallery,
                level=(chosen_plan.get('level', 'default') if profile_plan else None),
                change_level=change_level if profile_plan else None)


def graphical():
    return bool(os.environ.get('WAYLAND_DISPLAY') or os.environ.get('DISPLAY'))


def run_job(view, args, target=None):
    """Run the companion for the gallery: `--configure` (the settings menu) or `--level` (↑ ↓), with --print-files.

    It hands its plan to the gallery's menu on stdout and takes the choice back on stdin, reports a download's
    progress, which the gallery shows in its middle, and ends with the files of the set it chose; the gallery then
    switches to them at the same wallpaper."""
    from gi.repository import GLib
    import settings_ui
    import wallpaper_setup_cli as cli
    view.settings_busy = True
    command = [sys.executable, str(Path(__file__).resolve()), '--collection', 'finalized',
               view.files[view.index].name, *args, '--print-files']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
                               env={**os.environ, 'PBLOOM_SETTINGS_PIPE': '1'})

    def answer(value):
        view.set_status('UPDATING WALLPAPERS' if value else None)
        try:
            process.stdin.write(json.dumps(value) + '\n')
            process.stdin.close()
        except OSError:
            pass

    def finish(result):
        view.show_progress(None)
        view.set_status(None)
        view.settings_busy = False
        if result:
            view.replace(result['files'], result.get('level'))
            if not target:                                 # settings saved (not a level only looked at)
                view.saved_level = result.get('level')
        if target and view.level_wanted != target:
            change_level(view, view.level_wanted)          # ↑ ↓ pressed again while this set was fetched
        else:
            view.level_wanted = view.level                 # the level in use (not the one asked for, if it failed)

    def wait():
        result = None
        for line in process.stdout:
            try:
                if line.startswith(cli.PIPE_PREFIX):
                    plan = json.loads(line[len(cli.PIPE_PREFIX):])
                    GLib.idle_add(view.set_status, None)
                    GLib.idle_add(view.show_menu, settings_ui.Menu(plan), answer)
                elif line.startswith(cli.PROGRESS_PREFIX):
                    GLib.idle_add(view.show_progress, json.loads(line[len(cli.PROGRESS_PREFIX):]))
                elif line.startswith(cli.FILES_PREFIX):
                    result = json.loads(line[len(cli.FILES_PREFIX):])
            except ValueError:
                pass
        if process.wait() != 0:
            result = None
        GLib.idle_add(finish, result)
    threading.Thread(target=wait, daemon=True).start()


def open_settings(view):
    """The gallery's S key: the settings menu in the gallery's own window, over the dimmed wallpaper."""
    if getattr(view, 'settings_busy', False):
        return
    view.set_status('OPENING SETTINGS')
    run_job(view, ['--configure'])


def change_level(view, level):
    """The gallery's ↑ ↓: the same wallpapers at another background level, only in the gallery (Enter makes it the
    desktop's); a set that is not installed yet is downloaded first. Presses while one is under way are taken up
    when it ends."""
    if getattr(view, 'settings_busy', False):
        return
    run_job(view, ['--level', level], target=level)


def enter(view, path):
    """The gallery's Enter: this wallpaper on the desktop, at the level shown. Another level than the saved one is
    saved first, which puts its set on the desktop with this wallpaper showing."""
    if getattr(view, 'settings_busy', False):
        return
    if view.level and view.level != getattr(view, 'saved_level', view.level):
        run_job(view, ['--save-level', view.level, '--set-desktop', str(path)])
    else:
        threading.Thread(target=set_desktop, args=(path,), daemon=True).start()

if __name__ == '__main__':
    main()
