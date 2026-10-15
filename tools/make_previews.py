#!/usr/bin/env python3
"""Build the images the README shows, into ../previews.

    python3 tools/make_previews.py

palette.webp is drawn from colors.toml, so it cannot drift from the theme.
The wallpaper thumbnails are scaled-down copies of the full 16:9 5K set
(dist/wallpaper-release/16x9-2880p, made by tools/package_wallpaper_profiles.py);
backgrounds/ holds only the starter.
"""

import os
import json
import math
import re
import subprocess

from pathlib import Path
from PIL import Image

from sheet import Sheet

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "previews")

ROWS = [
    ("SURFACES", ["darker_background", "dark_background", "background", "lighter_background", "selection", "muted"]),
    ("TEXT AND SIGNAL", ["dark_foreground", "light_foreground", "foreground", "bright_foreground", "accent"]),
    ("NAMED COLOURS", ["red", "orange", "yellow", "green", "cyan", "blue", "magenta", "brown"]),
    ("BRIGHT VARIANTS", ["bright_red", "bright_yellow", "bright_green", "bright_cyan", "bright_blue", "bright_magenta"]),
]


def read_colors():
    text = open(os.path.join(ROOT, "colors.toml")).read()
    return {k: v for k, v in re.findall(r'^(\w+)\s*=\s*"(#[0-9a-fA-F]{6})"', text, re.M)}


def rgb(hex_):
    return tuple(int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5))


def palette_card(colors):
    s = Sheet(2592, 1080, seed=5)
    s.background()
    s.begin_lines()
    s.grid()
    s.frame(0, 14, code="NCR")
    s.diamond(97, 96, 5, 0.9, 0.8, fill=0.9)
    s.ln(110, 96, 700, 96, 0.35, 0.5)
    s.text("PALETTE", 92, 140, 30, track=0.30, a=0.95, bold=True)
    s.text("colors.toml", 92, 166, 9, track=0.34, a=0.6)
    chip_w, chip_h, gap = 280, 112, 24
    for r, (title, keys) in enumerate(ROWS):
        y = 232 + r * 196
        s.text(title, 92, y - 16, 10, a=0.6)
        for i, key in enumerate(keys):
            x = 92 + i * (chip_w + gap)
            s.rect(x, y, chip_w, chip_h, 0.55, 0.6, fill=1.0, color=rgb(colors[key]))
            s.rect(x, y, chip_w, chip_h, 0.35, 0.6)
            s.text(key.upper().replace("_", " "), x, y + chip_h + 22, 10.5, track=0.16, a=0.85)
            s.text(colors[key], x, y + chip_h + 40, 10.5, track=0.10, a=0.55)
    s.end_lines()
    # no bloom and no grain here: the chips must show the exact colours
    s.save(os.path.join(OUT, "palette.webp"), glow=0, grain=0.6)


def thumbnails():
    src = os.path.join(ROOT, "dist", "wallpaper-release", "16x9-2880p")
    for name in sorted(os.listdir(src)):
        if name.endswith(".webp"):
            subprocess.run(["magick", os.path.join(src, name), "-resize", "1600x", "-quality", "82",
                            "-define", "webp:method=6", os.path.join(OUT, name)], check=True)
    registry = Path(ROOT) / 'docs/collection/catalog.json'
    if registry.exists():
        files = [Path(e['source']).name for e in json.loads(registry.read_text())['finalized']]
        files = [f for f in files if os.path.isfile(os.path.join(src, f))]
    else:
        files = sorted(f for f in os.listdir(src) if re.match(r"\d{2,3}-.*\.webp$", f))
    with Image.open(os.path.join(src, files[0])) as image:
        cell_height = round(1200 * image.height / image.width)
    subprocess.run(["magick", "montage"] + [os.path.join(OUT, f) for f in files] +
                   ["-tile", f"3x{math.ceil(len(files)/3)}", "-geometry", f"1200x{cell_height}+8+8", "-background", "#0a0c10",
                    "-quality", "84", os.path.join(OUT, "wallpapers.webp")], check=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    palette_card(read_colors())
    thumbnails()
    for f in sorted(os.listdir(OUT)):
        print(f"{f}  {os.path.getsize(os.path.join(OUT, f)) / 1e3:.0f} kB")
