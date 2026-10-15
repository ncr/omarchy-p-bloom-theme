#!/usr/bin/env python3
"""Render the p(bloom) theme wallpapers into ../backgrounds.

    python3 tools/make_wallpapers.py                  # all sheets, 5120x2160
    python3 tools/make_wallpapers.py --size 5120x2880 # 16:9, the main branch
    python3 tools/make_wallpapers.py --size 2880x1920 --inset 0  # one exact screen
    python3 tools/make_wallpapers.py --only 3         # one sheet
    python3 tools/make_wallpapers.py --set classic    # the first set of sheets

Needs pycairo, numpy and Pillow, and the Nimbus Sans font (Arch: gsfonts).

Every subject here is made up for this theme. Nothing is traced or copied
from the game: only the drawing technique is borrowed — thin white line work
on slate, tick rings, leader lines, spaced capitals.

The current starmap treatment retains three columns in both native formats:
centred main drawing, side details and diagrams, legend bottom left and Field
Notes bottom right. The legacy original treatment keeps its old compact layout.
"""

import argparse
import os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", default="5120x2160")
    ap.add_argument("--only", type=int)
    ap.add_argument("--set", default="devices", choices=["devices", "classic"])
    ap.add_argument("--style", default="starmap", choices=["starmap", "original"],
                    help="accepted line treatment; original reproduces the clear-labels masters")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backgrounds"))
    ap.add_argument("--ext", default="webp", choices=["webp", "png", "jpg"])
    ap.add_argument("--inset", type=int, help="keep legend and emblem this many units from the sides; "
                    "default 150 for 16:9 (survives cropping to 16:10 and 3:2), else 0")
    args = ap.parse_args()
    if args.set == "classic":
        from classic import SHEETS
    else:
        import devices
        import foibles
        import leisure
        from order import ORDER
        drawn = dict(devices.SHEETS + leisure.SHEETS + foibles.SHEETS)
        SHEETS = [(f"{i:02d}-{name}", drawn[name]) for i, (name, _) in enumerate(ORDER, 1)]
        if args.style == "starmap":
            from starmap import install
            install()
    size = tuple(int(v) for v in args.size.lower().split("x"))
    from sheet import Sheet
    is_16_9 = abs(size[0] / size[1] - 16 / 9) < 0.01
    Sheet.side_inset = args.inset if args.inset is not None else (150 if is_16_9 else 0)
    os.makedirs(args.out, exist_ok=True)
    for i, (name, fn) in enumerate(SHEETS, 1):
        if args.only and args.only != i:
            continue
        sheet = fn(size)
        sheet.end_lines()
        path = os.path.join(args.out, f"{name}.{args.ext}")
        sheet.save(path)
        print(f"{path}  {os.path.getsize(path) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
