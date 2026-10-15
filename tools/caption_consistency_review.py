#!/usr/bin/env python3
"""Native crops of the changed B/C captions and service-year row."""
import html
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'concepts/century/caption-consistency'


def main():
    review = json.loads((OUT / 'review.json').read_text())
    entries = sorted((e for e in review['wallpapers'] if e['id'].startswith('c')),
                     key=lambda e: (e['slug'] != 'seam-surgeon', e['id']))
    records, cards = [], []
    for e in entries:
        pairs = []
        for region, title in [('B', 'Left detail'), ('C', 'Right detail'),
                              ('service', 'Projected first service')]:
            paths = {}
            for fmt, height in [('wide', 1080), ('16-9', 1440)]:
                ex = height - 1080
                boxes = {
                    'B': (125, 445 + ex * .35, 675, 500 + ex * .35),
                    'C': (1890, 445 + ex * .35, 2440, 500 + ex * .35),
                    'service': (82, height - 112, 632, height - 76),
                }
                box = tuple(round(v * 2) for v in boxes[region])
                paths[fmt] = {}
                for state in ('before', 'after'):
                    dest = OUT / 'caption-crops' / fmt / f'{e["id"]}-{region}-{state}.jpg'
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    with Image.open(OUT / e['files'][fmt][state]) as im:
                        im.crop(box).save(dest, quality=97)
                    paths[fmt][state] = str(dest.relative_to(OUT))
            records.append(dict(wallpaper=e['id'], region=region, files=paths))
            figures = ''.join(
                '<figure><figcaption>' + state.upper() + '</figcaption><a href="' +
                paths['wide'][state] + '"><img loading="lazy" src="' +
                paths['wide'][state] + '" alt="' + html.escape(e['title'] + ' ' + region + ' ' + state) +
                '"></a></figure>' for state in ('before', 'after'))
            pairs.append('<h3>' + title + '</h3><div class="pair">' + figures + '</div>')
        cards.append('<article><h2>' + html.escape(e['title']) + '</h2>' + ''.join(pairs) + '</article>')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>p(bloom) / Caption consistency</title><style>
body{margin:0;padding:3vw;background:#0b121a;color:#d7e2e9;font:16px/1.5 system-ui}
h1{font-size:26px}h2{font-size:20px}h3{font-size:13px;font-weight:400;color:#a6bbc8}
p{color:#a6bbc8;max-width:900px}a{color:#b8d4df}article{margin:40px 0 70px}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}figure{margin:0}
figcaption{font-size:11px;color:#b9a374;letter-spacing:.12em}img{width:100%;display:block}
@media(max-width:1050px){.pair{grid-template-columns:1fr}}</style>
<h1>ONE CAPTION CONVENTION</h1><p>Twenty Century sheets now follow the original
HALL PLAN layout: letter, name and an aligned, device-specific detail note.
Projected service keeps the original year, without the inconsistent suffix.</p>
<p><a href="./">Full wallpaper comparison / both formats</a></p>'''
    (OUT / 'captions.html').write_text(page + ''.join(cards) + '</html>')
    (OUT / 'captions.json').write_text(json.dumps(records, indent=2) + '\n')
    print('20 sheets / 40 detail captions / 20 service rows / both native formats')


if __name__ == '__main__':
    main()
