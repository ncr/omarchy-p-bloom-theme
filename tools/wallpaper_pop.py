#!/usr/bin/python
"""Super+O: fullscreen/float for the gallery, standard Omarchy pop elsewhere."""
import json
import os
import subprocess
import time


def query(kind):
    return json.loads(subprocess.check_output(['hyprctl', '-j', kind]))


def toggle(window):
    selector = json.dumps('address:' + window['address'])

    def dispatch(action, fields=''):
        subprocess.run(['hyprctl', 'dispatch',
                        f'hl.dsp.window.{action}({{ window = {selector}{fields} }})'],
                       check=True, stdout=subprocess.DEVNULL)

    if window['fullscreen']:
        dispatch('fullscreen', ', mode = "fullscreen"')
        # Allow the compositor's configure event to settle before resizing.
        for _ in range(20):
            current = next((w for w in query('clients') if w['address'] == window['address']), None)
            if current is None:
                return
            if not current['fullscreen']:
                break
            time.sleep(.025)
        else:
            raise RuntimeError('The viewer did not leave fullscreen')
        if not current['floating']:
            dispatch('float', ', action = "toggle"')
        monitor = next(m for m in query('monitors') if m['id'] == current['monitor'])
        width = min(1400, round(monitor['width'] / monitor['scale'] * .65))
        height = round(width * 2160 / 5120)
        dispatch('resize', f', x = {width}, y = {height}')
        dispatch('center')
        if not current['pinned']:
            dispatch('pin')
        dispatch('alter_zorder', ', mode = "top"')
    else:
        if window['pinned']:
            dispatch('pin')
        dispatch('fullscreen', ', mode = "fullscreen"')


def main():
    window = query('activewindow')
    if window.get('class') != 'p-bloom-wallpapers':
        os.execvp('omarchy-hyprland-window-pop', ['omarchy-hyprland-window-pop'])
    toggle(window)


if __name__ == '__main__':
    main()
