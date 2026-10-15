#!/usr/bin/env python3
"""Review sheets for the three ground levels (Muted / Default / Vivid).

    python3 tools/render_wallpaper_sets.py --profile 16x9-1080p \
        --level muted --level default --level vivid --out concepts/ground-levels/sets --jobs 12
    python3 tools/ground_level_review.py

Reads the rendered 1920x1080 sets and their audits and writes, into
concepts/ground-levels/:

  contact-muted.jpg, contact-default.jpg, contact-vivid.jpg
      all 42 sheets of one level, in collection order
  grounds-side-by-side.jpg
      the 13 grounds, one representative sheet each, Muted | Default | Vivid
  contrast.json, contrast.md
      lowest measured label contrast per ground x level (white type and
      accents), from the per-label audit on final pixels
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ('muted', 'default', 'vivid')
FONT = '/usr/share/fonts/gsfonts/NimbusSans-Regular.otf'


def font(size):
    try:
        return ImageFont.truetype(FONT, size)
    except OSError:
        return ImageFont.load_default()


def set_dir(sets, profile, level):
    return sets/(profile if level == 'default' else f'{profile}-{level}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--sets', type=Path, default=ROOT/'concepts/ground-levels/sets')
    ap.add_argument('--profile', default='16x9-1080p')
    ap.add_argument('--out', type=Path, default=ROOT/'concepts/ground-levels')
    args = ap.parse_args()
    cat = json.loads((ROOT/'docs/collection/catalog.json').read_text())['finalized']
    palettes = json.loads((ROOT/'docs/collection/palettes.json').read_text())
    grounds = palettes['assignment_42']
    audits = {lv: {r['id']: r for r in json.loads((set_dir(args.sets, args.profile, lv)/'audit.json').read_text())['sheets']}
              for lv in LEVELS}
    names = {e['id']: Path(e['source']).name for e in cat}
    titles = {e['id']: e['title'] for e in cat}
    args.out.mkdir(parents=True, exist_ok=True)

    # One contact sheet per level: 6 x 7 thumbnails.
    tw, th, label, cols = 560, 315, 30, 6
    for lv in LEVELS:
        rows = -(-len(cat) // cols)
        sheet = Image.new('RGB', (cols*tw + (cols+1)*12, 70 + rows*(th+label+12)), (12, 13, 16))
        d = ImageDraw.Draw(sheet)
        d.text((12, 18), f'p(bloom) ground level: {lv.upper()}  ·  {args.profile}  ·  42 sheets in collection order',
               fill=(225, 230, 238), font=font(28))
        for n, e in enumerate(cat):
            x, y = 12 + (n % cols)*(tw+12), 70 + (n // cols)*(th+label+12)
            with Image.open(set_dir(args.sets, args.profile, lv)/names[e['id']]) as im:
                sheet.paste(im.convert('RGB').resize((tw, th), Image.Resampling.LANCZOS), (x, y))
            c = audits[lv][e['id']].get('contrast', {})
            text = c.get('text', {}).get('ratio', 0)
            acc = c.get('accent', {}).get('ratio', 0)
            d.text((x, y+th+5), f"{n+1:02d} {titles[e['id']]} · {grounds[e['id']]} · text {text:.1f} acc {acc:.1f}",
                   fill=(200, 206, 216), font=font(17))
        sheet.save(args.out/f'contact-{lv}.jpg', quality=92)

    # The 13 grounds side by side: first sheet of each ground in collection order.
    order = list(palettes['palettes'])
    reps = {}
    for e in cat:
        reps.setdefault(grounds[e['id']], e['id'])
    tw, th = 960, 540
    sheet = Image.new('RGB', (3*tw + 4*12 + 190, 60 + len(order)*(th+12)), (12, 13, 16))
    d = ImageDraw.Draw(sheet)
    for k, lv in enumerate(LEVELS):
        d.text((190 + 12 + k*(tw+12), 16), lv.upper(), fill=(225, 230, 238), font=font(30))
    for r, g in enumerate(order):
        y = 60 + r*(th+12)
        i = reps[g]
        d.text((12, y+8), g, fill=(225, 230, 238), font=font(28))
        d.text((12, y+44), titles[i].title(), fill=(170, 176, 186), font=font(18))
        for k, lv in enumerate(LEVELS):
            with Image.open(set_dir(args.sets, args.profile, lv)/names[i]) as im:
                sheet.paste(im.convert('RGB').resize((tw, th), Image.Resampling.LANCZOS), (190 + 12 + k*(tw+12), y))
    sheet.save(args.out/'grounds-side-by-side.jpg', quality=92)

    # Lowest label contrast per ground x level.
    table = {}
    for lv in LEVELS:
        for i, r in audits[lv].items():
            row = table.setdefault(grounds[i], {}).setdefault(lv, {'text': None, 'accent': None, 'issues': 0})
            for role in ('text', 'accent'):
                v = r.get('contrast', {}).get(role, {}).get('ratio')
                if v is not None and (row[role] is None or v < row[role]):
                    row[role] = v
            row['issues'] += sum('contrast' in x for x in r['issues'])
    (args.out/'contrast.json').write_text(json.dumps(table, indent=1)+'\n')
    lines = ['| ground | ' + ' | '.join(f'{lv} text / accent' for lv in LEVELS) + ' |',
             '|---|' + '---|'*len(LEVELS)]
    for g in order:
        cells = [f"{table[g][lv]['text']:.2f} / {table[g][lv]['accent']:.2f}"
                 + (f" ({table[g][lv]['issues']} issues)" if table[g][lv]['issues'] else '') for lv in LEVELS]
        lines.append(f'| {g} | ' + ' | '.join(cells) + ' |')
    (args.out/'contrast.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
