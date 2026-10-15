#!/usr/bin/env python3
"""README hero: the name as on the music video's chorus card, then one wallpaper per beat of the song.

    python3 tools/make_readme_hero.py        # writes previews/hero.webp from the full 16:9 5K set in dist/wallpaper-release/

The card is set in Jost Light (SIL OFL, the film's accent face): "p(" and ")" in ice white, "bloom" in Pollen, on the
theme's navy, at the same proportion of the frame as the film's card. Fourteen sheets follow, spread over the ground
colours and ordered so that neighbours differ, each held for one beat of "Prepare to Walk" (0.4527 s).
"""
import colorsys
import json
from pathlib import Path
import subprocess
import tempfile
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'previews/hero.webp'
W, H, FPS, BEAT = 960, 540, 24, 0.4527
NAVY, WHITE, POLLEN = (7, 12, 20), (241, 245, 252), (245, 200, 67)
FONT = Path.home()/'.cache/p-bloom/jost-300.ttf'


def jost():
    if not FONT.is_file():
        css = urllib.request.urlopen('https://fonts.googleapis.com/css2?family=Jost:wght@300', timeout=30).read().decode()
        url = css.split('url(')[1].split(')')[0]
        FONT.parent.mkdir(parents=True, exist_ok=True)
        FONT.write_bytes(urllib.request.urlopen(url, timeout=30).read())
    return FONT


def card():
    target = (718-359)/1080*H              # the film's card: the name 359 px tall in 1080
    size = 10
    while True:
        f = ImageFont.truetype(str(jost()), size)
        b = f.getbbox('p(bloom)')
        if b[3]-b[1] >= target:
            break
        size += 1
    im = Image.new('RGB', (W, H), NAVY)
    d = ImageDraw.Draw(im)
    x, y = (W-f.getlength('p(bloom)'))/2, (H-(b[3]-b[1]))/2-b[1]
    for text, colour in (('p(', WHITE), ('bloom', POLLEN), (')', WHITE)):
        d.text((x, y), text, font=f, fill=colour)
        x += f.getlength(text)
    return im


def sheets():
    files = sorted((ROOT/'dist/wallpaper-release/16x9-2880p').glob('*.webp'))
    items = []
    for f in files:
        im = Image.open(f).convert('RGB')
        r, g, b = np.asarray(im.resize((64, 36))).reshape(-1, 3).mean(0)/255
        items.append((colorsys.rgb_to_hls(r, g, b)[0], f.name, im))
    items.sort(key=lambda x: x[0])
    pick = [items[i] for i in np.linspace(0, len(items)-1, 14).round().astype(int)]
    return [pick[i] for i in (0, 7, 3, 10, 5, 12, 1, 8, 4, 11, 6, 13, 2, 9)]


def main():
    frames, t = [], 0.0
    def hold(img, seconds):
        nonlocal t
        frames.extend([img]*(round((t+seconds)*FPS)-round(t*FPS)))
        t += seconds
    hold(card(), 3*BEAT)
    for _, _, im in sheets():
        hold(im.resize((W, H), Image.LANCZOS), BEAT)
    with tempfile.TemporaryDirectory() as work:
        for i, f in enumerate(frames):
            f.save(f'{work}/{i:04d}.png')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{work}/%04d.png', '-c:v', 'libwebp',
                        '-loop', '0', '-quality', '75', '-compression_level', '6', '-preset', 'picture', str(OUT)], check=True)
    print(OUT, len(frames), 'frames')


if __name__ == '__main__':
    main()
