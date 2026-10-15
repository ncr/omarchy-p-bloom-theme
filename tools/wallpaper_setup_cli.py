"""Optional wallpaper settings (background level, resolution); normal launches never open this TUI."""
import argparse
import curses
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile


LEVELS = ('muted', 'default', 'vivid')
LEVEL_LABELS = {'muted': 'Muted', 'default': 'Default', 'vivid': 'Vivid'}
LEVEL_HINT = 'How strong the background colour is.'
# lines a --configure or --level run sends the gallery on stdout (PBLOOM_SETTINGS_PIPE): the plan for its menu,
# a download's progress, and the files of the set it ends with
PIPE_PREFIX = 'p-bloom-settings-plan '
PROGRESS_PREFIX = 'p-bloom-progress '
FILES_PREFIX = 'p-bloom-files '


def settings(plan, level=None):
    """Resolution rows; sizes and download markers are those of `level`."""
    options=(plan.get('options_by_level') or {}).get(level) or plan['options']
    def size(o):return ' × '.join(map(str,o['size']))
    best=next((o for o in options if o['profile']==plan.get('profile')),None)
    # Automatic says that it follows the optimal set and names it; the same set is marked in the list
    rows=[('auto','Automatic · Optimal set'+(f' ({size(best)})' if best else ''))]
    for o in options:
        mb=f"{o['total_bytes']/1_000_000:.1f} MB" if o.get('total_bytes') is not None else 'Size unknown'
        # sizes right-aligned, so "download" lines up down the list
        width=max(len(f"{x['total_bytes']/1_000_000:.1f} MB") if x.get('total_bytes') is not None else 12 for x in options)
        rows.append((o['profile'],size(o)+' / '+mb.rjust(width)+(' · optimal' if o is best else '')+('' if o.get('local',True) else ' · download')))
    return rows


def level_line(level):
    """The three-way background choice on one line, the current one bracketed."""
    return '   '.join(f'[ {LEVEL_LABELS[k]} ]' if k == level else f'  {LEVEL_LABELS[k]}  ' for k in LEVELS)


def valid(value, plan):
    return (isinstance(value, dict) and value.get('level') in LEVELS
            and value.get('profile') in {'auto',*(o['profile'] for o in plan['options'])})


def tui(screen,plan,apply):
    try:curses.curs_set(0)
    except curses.error:pass
    screen.keypad(True)
    level=plan.get('setting_level','default')
    if level not in LEVELS:level='default'
    rows=settings(plan,level)
    selected=next((i for i,(key,_) in enumerate(rows) if key==plan.get('setting','auto')),0)
    while True:
        rows=settings(plan,level)
        screen.erase()
        h,w=screen.getmaxyx()
        left=max(1,(w-66)//2)
        top=max(0,(h-min(len(rows)+12,h))//2)
        def put(y,text,style=0):
            if 0<=y<h-1:
                try:screen.addstr(y,left,text[:max(0,w-left-1)],style)
                except curses.error:pass
        put(top,'P(BLOOM) / WALLPAPER SETTINGS',curses.A_BOLD)
        put(top+2,'INTENSITY',curses.A_BOLD)
        put(top+3,level_line(level),curses.A_BOLD)
        put(top+4,LEVEL_HINT)
        put(top+6,'RESOLUTION',curses.A_BOLD)
        # one row per line; a list taller than the window scrolls with the selection and says what is hidden
        count=max(1,h-top-12)
        start=0 if len(rows)<=count else min(max(0,selected-count+1+(selected<len(rows)-1)),len(rows)-count)
        if start:put(top+7,f'  ↑ {start} more')
        for j,(key,label) in enumerate(rows[start:start+count]):
            i=start+j
            style=curses.A_BOLD|(curses.A_REVERSE if i==selected else 0)
            put(top+8+j,('▶ ' if i==selected else '  ')+label,style)
        if start+count<len(rows):put(top+8+count,f'  ↓ {len(rows)-start-count} more')
        put(h-2,'←→ Intensity   ↑↓ Resolution   ENTER Save   ESC Cancel',curses.A_BOLD)
        screen.refresh()
        key=screen.get_wch()
        if key in (curses.KEY_DOWN,'j','\t'):selected=(selected+1)%len(rows)
        elif key in (curses.KEY_UP,'k'):selected=(selected-1)%len(rows)
        elif key in (curses.KEY_LEFT,'h'):level=LEVELS[max(0,LEVELS.index(level)-1)]
        elif key in (curses.KEY_RIGHT,'l'):level=LEVELS[min(2,LEVELS.index(level)+1)]
        elif key in ('\n','\r',curses.KEY_ENTER):return {'profile':rows[selected][0],'level':level}
        elif key in ('\x1b','q','Q'):return None


def prompt(plan,apply):
    if sys.stdin.isatty() and sys.stdout.isatty() and os.environ.get('TERM')!='dumb':
        try:return curses.wrapper(tui,plan,apply)
        except KeyboardInterrupt:return None
    level=plan.get('setting_level','default')
    if level not in LEVELS:level='default'
    print('P(BLOOM) / WALLPAPER SETTINGS')
    print('Intensity: '+LEVEL_HINT)
    for i,k in enumerate(LEVELS,1):print(f"{i}. {LEVEL_LABELS[k]}"+(' (current)' if k==level else ''))
    try:
        while True:
            value=input(f'Number, Enter={LEVEL_LABELS[level]}, q=cancel: ').strip().lower()
            if value=='q':return None
            if value=='':break
            if value in ('1','2','3'):level=LEVELS[int(value)-1];break
        print('Resolution:')
        rows=settings(plan,level)
        for i,(_,label) in enumerate(rows,1):print(f'{i}. {label}')
        while True:
            value=input('Number, Enter=automatic, q=cancel: ').strip().lower()
            if value=='q':return None
            if value=='':return {'profile':'auto','level':level}
            if value.isdecimal() and 1<=int(value)<=len(rows):return {'profile':rows[int(value)-1][0],'level':level}
    except (KeyboardInterrupt,EOFError):return None


def choose_profile(plan, apply):
    """Ask for the settings: {'profile': 'auto' or a set id, 'level': a LEVELS name}, or None."""
    # the gallery's menu: the plan goes out as one line on stdout, the choice comes back as one line on stdin
    if os.environ.get('PBLOOM_SETTINGS_PIPE'):
        print(PIPE_PREFIX + json.dumps(plan), flush=True)
        try:
            value = json.loads(sys.stdin.readline() or 'null')
        except ValueError:
            value = None
        return value if valid(value, plan) else None
    if sys.stdin.isatty() and sys.stdout.isatty():
        return prompt(plan, apply)
    foot = shutil.which('foot')
    terminal = shutil.which('xdg-terminal-exec')
    if not (foot or terminal) or not (os.environ.get('WAYLAND_DISPLAY') or os.environ.get('DISPLAY')):
        raise ValueError('Run p-bloom-wallpapers --configure in a terminal to review the optimal wallpaper set.')
    with tempfile.TemporaryDirectory(prefix='p-bloom-setup-') as directory:
        request, result = Path(directory)/'request.json', Path(directory)/'result.json'
        request.write_text(json.dumps({'plan':plan, 'apply':apply}))
        command = [sys.executable, str(Path(__file__).resolve()), '--request', str(request), '--result', str(result)]
        if foot:
            launcher = [foot, '--fullscreen', '--font=monospace:size=20',
                        '--title=p(bloom) Wallpapers setup', '--app-id=p-bloom-wallpapers-setup']
        else:
            launcher = [terminal, '--title=p(bloom) Wallpapers setup', '--app-id=p-bloom-wallpapers-setup']
        subprocess.run([*launcher, *command], check=False)
        if not result.is_file():
            return None
        value = json.loads(result.read_text())
        return value if valid(value, plan) else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request', type=Path, required=True)
    parser.add_argument('--result', type=Path, required=True)
    args = parser.parse_args()
    def cancel(*_):
        raise KeyboardInterrupt
    signal.signal(signal.SIGHUP, cancel)
    signal.signal(signal.SIGTERM, cancel)
    value = None
    try:
        request = json.loads(args.request.read_text())
        value = prompt(request['plan'], request['apply'])
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        args.result.write_text(json.dumps(value))


if __name__ == '__main__':
    main()
