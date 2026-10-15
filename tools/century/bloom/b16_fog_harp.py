"""b16 FOG HARP: text, field notes and side diagrams.

Numbers are narrative, kept consistent with the model notes:
Three harps, wire fields 19.4 + 18.6 + 17.7 = 56 m2 (4 m wide, mean wire
height ~4.6 m under the S-curved neck).
Declared yield on a good fog morning: 0.8 L per m2 per fog hour x 6 h
  -> 56 x 0.8 x 6 = 269 L, "about 270 L".
Cistern 3.2 m across x 2 m deep = 16 m3 = 16 000 L = 60 such mornings.
Drinking and cooking at 5 L per person a day -> 270 / 5 = 54 people.
Wires 0.4 mm at 3.2 mm pitch -> 4 000 / 3.2 = 1 250 per harp, 3 750 in all.
Vertical wires versus mesh: on mesh, drops hang at crossings and are torn
off by the same wind that brings them; on vertical wires they merge and
slide straight down (after published fog-harp tests: about twice the
yield of standard mesh in light fog; stated as a design assumption here).
"""
import math

ENTRY = dict(
    id='b16', series='B16', number=216, slug='fog-harp', title='FOG HARP',
    domain='water', category='serious', model='FH-3', palette='periwinkle', seed=260116,
    purpose='FOG-WATER COLLECTOR',
    narrative=('Three harps of fine vertical wire stand on the coastal ridge and comb drinking '
               'water out of the passing fog. On a grey morning they fill the village cistern '
               'with about 270 litres, enough for fifty people to drink and cook.'),
    enabled_by=[
        ('FOG COLLECTION', 'Fog nets already water coastal villages in Chile, Peru and Morocco.'),
        ('FOG HARPS', 'Vertical wires shed droplets faster than mesh and clog less.'),
        ('GRAVITY WATER', 'Gutters, filter cans and a buried pipe; no pump, no power.'),
    ],
    real_basis='Fog nets, fog harps (vertical wire collectors outperform mesh).',
    required_breakthroughs='Coatings that keep shedding droplets after years of salt and dust.',
    view_A='WIRE HARPS ON THE COASTAL RIDGE',
    view_B='WIRE ARRAY', view_B_note='NECK SEGMENT / TENSION PINS / BEADING DROPS',
    view_C='DRIP GUTTER', view_C_note='END SECTION / LEAF SCREEN / FILTER CAN / DROP PIPE',
    service_year='2030',
    sources=['https://doi.org/10.1021/acsami.7b17488', 'https://www.fogquest.org/'],
    source_scope='Real basis only: fog-net programmes and published fog-harp tests. The harps, the village and every figure are an original concept.',
)

DOSSIER = dict(
    kind='fog morning',
    fact=('Fog is a cloud touching the ground. The wind pushes its droplets through the '
          'harp; a few catch on each wire, merge, and run down into the gutter.'),
    rows=[('WIRE FIELD', '3 HARPS / 56 m²'),
          ('GOOD FOG MORNING', '6 h / ABOUT 270 L'),
          ('WIRES', '0.4 mm AT 3.2 mm PITCH'),
          ('CISTERN', '16 000 L / SIXTY MORNINGS')],
    note='BY SEVEN THE FOG HAD LIFTED AND THE TAP WAS RUNNING.',
    left=('WHY WIRES, NOT MESH', 'SCHEMATIC / AFTER PUBLISHED FOG-HARP TESTS',
          'On mesh, drops hang at the crossings and the wind takes them back; on wire they run down.'),
    right=('ONE GREY MORNING', 'DECLARED RATE / 0.8 L PER m² PER FOG HOUR / 56 m²',
           'Litres in the cistern = 56 m² x 0.8 x fog hours; clear mornings add nothing.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        # Mesh panel: drops pinned at crossings, some blown off downwind.
        mx, my, ms = x + 20, y + 4, 96
        for k in range(6):
            s.ln(mx + k * ms / 5, my, mx + k * ms / 5, my + ms, .45, .6)
            s.ln(mx, my + k * ms / 5, mx + ms, my + k * ms / 5, .45, .6)
        for i, j in ((1, 1), (3, 1), (2, 2), (4, 3), (1, 4), (3, 4)):
            s.circ(mx + i * ms / 5, my + j * ms / 5, 3.2, .85, .7, color=ARC)
        for yy in (my + 30, my + 70):
            arrow(s, (mx + ms + 6, yy), (mx + ms + 34, yy - 6), WHITE)
            s.circ(mx + ms + 40, yy - 7, 2.4, .7, .6, color=ARC)
        tx(s, 'MESH', mx, my + ms + 18, 6.8)
        tx(s, 'BLOWN OFF', mx + ms + 14, my + 18, 6.2, .62)
        # Wire array: drops merge and slide into the gutter.
        wx = x + 250
        for k in range(6):
            s.ln(wx + k * 18, my, wx + k * 18, my + ms - 10, .55, .6)
        for k, (dy, r) in enumerate(((12, 2.2), (34, 2.8), (58, 3.4), (80, 4.0))):
            for c in range(0, 6, 2 if k % 2 else 3):
                s.circ(wx + c * 18, my + dy, r, .85, .7, color=ARC)
        arrow(s, (wx + 36 + 8, my + 38), (wx + 36 + 8, my + 76), ARC)
        s.poly([(wx - 8, my + ms - 6), (wx - 4, my + ms + 4), (wx + 94, my + ms + 4), (wx + 98, my + ms - 6)], .6, .7, close=False)
        tx(s, 'WIRE', wx, my + ms + 18, 6.8)
        tx(s, 'INTO THE GUTTER', wx + 106, my + ms + 2, 6.2, .62)
    else:
        # Cumulative litres through one declared morning of fog.
        px, py, pw, ph = x + 40, y + 6, 330, 100
        s.poly([(px, py), (px, py + ph), (px + pw, py + ph)], .5, .6, close=False)
        hours = ['04', '05', '06', '07', '08', '09', '10', '11', '12']
        fog0, fog1 = 1, 7                 # fog from 05:00 to 11:00
        for i, h in enumerate(hours):
            xx = px + pw * i / 8
            s.ln(xx, py + ph, xx, py + ph + 4, .45, .5)
            tx(s, h, xx, py + ph + 15, 6.4, .62, align='c')
        s.rect(px + pw * fog0 / 8, py, pw * (fog1 - fog0) / 8, ph, .18, .5, dash=[3, 3])
        tx(s, 'FOG', px + pw * (fog0 + fog1) / 16, py - 5, 6.4, .7, align='c')
        top = 300.0
        def yv(litres): return py + ph * (1 - litres / top)
        pts = []
        for k in range(81):
            t = 8 * k / 80
            litres = 56 * .8 * max(0, min(t, fog1) - fog0)
            pts.append((px + pw * t / 8, yv(litres)))
        s.poly(pts, .85, .8, close=False, color=GOLD)
        s.ln(px - 4, yv(269), px + pw, yv(269), .2, .5, dash=[2, 3])
        tx(s, '270 L', px - 8, yv(269) + 3, 6.6, .8, align='r')
        tx(s, '0', px - 8, py + ph + 3, 6.4, .6, align='r')
        tx(s, 'HOUR', px + pw + 10, py + ph + 3, 6.2, .55)
        tx(s, 'MARISOL, 07:00', px + pw * 3 / 8 + 6, yv(56 * .8 * 2) + 18, 6.4, .75)
        s.dot(px + pw * 3 / 8, yv(56 * .8 * 2), 2.4, .9, color=ARC)
