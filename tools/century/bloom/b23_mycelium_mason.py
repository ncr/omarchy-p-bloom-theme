"""b23 MYCELIUM MASON: text, field notes and side diagrams.

Numbers are narrative, kept consistent with the model:
Round house, outer diameter 7.0 m, wall 0.30 m thick, 2.4 m high.
Wall volume = pi x (3.5^2 - 3.2^2) x 2.4 = pi x 2.01 x 2.4 = 15.2 m3;
door (0.9 x 2.0 x 0.3 = 0.54) and two windows (2 x 0.7 x 0.8 x 0.3 = 0.34)
leave about 14.3 -> "14 m3". Floor inside: pi x 3.2^2 = 32 m2.
Print rate 0.5 m3 an hour -> 28 h, three ten-hour days (day 0-3).
Twelve segments of 30 degrees; about 2.3 h each.
Growth in tents: 6 days at 24 C, 95 % relative humidity (day 3-9).
Drying with fans and sun: 3 days (day 9-12); drying stops the mycelium,
the wall is then inert. Lime plaster: 2 days (day 12-14).
Dry wall density ~250 kg/m3 -> 14 x 250 = 3.5 t of hurd and mycelium.
A hectare of hemp gives ~8 t of dry stalks, ~5 t of hurd -> one house
from well under a hectare (0.7 ha) of one season's hemp.
End of life: shredded and composted in about 12 weeks.
"""

ENTRY = dict(
    id='b23', series='B23', number=223, slug='mycelium-mason', title='MYCELIUM MASON',
    domain='housing', category='serious', model='MM-2', palette='moss', seed=260123,
    purpose='GROWN-HOUSE PRINTER',
    narrative=('Prints the walls of a small round house from hemp and living mycelium, one '
               'segment at a time. Under the tents the fibres grow into one solid wall in six '
               'days; when the house is no longer needed, it goes back to the soil.'),
    enabled_by=[
        ('MYCELIUM COMPOSITES', 'Fungal mycelium grown through plant fibre into light, solid blocks and panels.'),
        ('ROBOTIC PRINTING', 'Tracked arms and cranes that lay house walls layer by layer from a pumped mix.'),
        ('HEMP BUILDING', 'Hemp-lime walls that already insulate and breathe in thousands of homes.'),
    ],
    real_basis='Mycelium composites, construction 3D printing and hemp-lime walls.',
    required_breakthroughs='Load-bearing grown materials certified for homes.',
    view_A='TRACKED ARM RAISING A GROWN HOUSE',
    view_B='PRINT HEAD', view_B_note='AUGER / SPAWN INJECTOR / SIDE TROWELS / NOZZLE',
    view_C='GROWTH TENT', view_C_note='HOOPS / MEMBRANE / MISTING LINE / PRINTED WALL',
    service_year='2033',
    sources=['https://www.nature.com/articles/s41598-017-17482-x', 'https://www.3dwasp.com/en/3d-printed-house-gaia/'],
    source_scope='Real basis only: mycelium-bound composites, printed earth and hemp houses, hemp-lime construction. The printer, schedule and all figures are an original concept.',
)

DOSSIER = dict(
    kind='one house',
    fact=('The printed mix is hemp hurd, water and living spawn. In the tent the mycelium '
          'binds the fibres into one wall; drying then stops it growing.'),
    rows=[('WALLS', '14 m³ / 30 cm THICK / 2.4 m HIGH'),
          ('PRINTING', '3 DAYS / 0.5 m³ AN HOUR'),
          ('GROWING', '6 DAYS AT 24 °C / 95 % HUMIDITY'),
          ('END OF LIFE', 'SHREDDED, COMPOSTED IN 12 WEEKS')],
    note='THE CHILDREN PRESSED THEIR HANDPRINTS INTO THE LAST LAYER BY THE DOOR.',
    left=('TWO WEEKS FROM FIELD TO HOME', 'DECLARED SCHEDULE / DAYS / ONE HOUSE',
          'The walls are solid after the tent week; drying stops the growth for good.'),
    right=('IT COMES FROM A FIELD, IT GOES BACK TO ONE', 'DECLARED MATERIAL LOOP / ONE HOUSE / DRY MASS',
           'About 0.7 ha of one season\'s hemp; the grown wall weighs 3.5 t dry.'),
)


def figure(s, side, x, y, w):
    import math
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        # Gantt on a 0-14 day axis; the tent week is the accent bar.
        bx = x + 108; bw = 300; day = bw / 14
        rows = [('PRINT', 0, 3, WHITE), ('GROW IN TENTS', 3, 9, ARC), ('DRY', 9, 12, GOLD), ('LIME FINISH', 12, 14, WHITE)]
        for i, (label, a, b, col) in enumerate(rows):
            yy = y + 10 + i * 24
            tx(s, label, x, yy + 3, 6.8)
            s.ln(bx, yy, bx + bw, yy, .14, .4)
            s.rect(bx + a * day, yy - 6, (b - a) * day, 12, .85, .7, color=col)
        axis = y + 108
        s.ln(bx, axis, bx + bw, axis, .45, .55)
        for d in range(0, 15, 1):
            s.ln(bx + d * day, axis, bx + d * day, axis + (5 if d % 7 == 0 else 3), .45, .5)
        for d in (0, 3, 7, 9, 12, 14):
            tx(s, str(d), bx + d * day, axis + 15, 6.6, .65, align='c')
        tx(s, 'DAY', x, axis + 4, 6.6, .55)
    else:
        # Four stations on a loop: field, hurd, wall, soil.
        cx = x + 215; cy = y + 60; rx = 130; ry = 46
        pts = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in range(0, 361, 4)]
        s.poly(pts, .28, .6, close=False)
        nodes = [(180, 'FIELD', '0.7 ha OF HEMP'), (270, 'HURD', '3.5 t DRY'),
                 (0, 'WALL', '14 m³ / DECADES'), (90, 'SOIL', '12 WEEKS')]
        for a, name, val in nodes:
            px = cx + rx * math.cos(math.radians(a)); py = cy + ry * math.sin(math.radians(a))
            s.circ(px, py, 5.5, .9, .8, color=ARC if name == 'WALL' else WHITE)
            if a == 180:
                tx(s, name, px - 12, py - 2, 7, .85, align='r'); tx(s, val, px - 12, py + 11, 6.4, .62, align='r')
            elif a == 0:
                tx(s, name, px + 12, py - 2, 7, .85); tx(s, val, px + 12, py + 11, 6.4, .62)
            elif a == 270:
                tx(s, name + ' / ' + val, px, py - 12, 6.8, .8, align='c')
            else:
                tx(s, name + ' / ' + val, px, py + 20, 6.8, .8, align='c')
        # Direction of travel: clockwise, field -> hurd -> wall -> soil.
        for a in (225, 315, 45, 135):
            p0 = (cx + rx * math.cos(math.radians(a - 6)), cy + ry * math.sin(math.radians(a - 6)))
            p1 = (cx + rx * math.cos(math.radians(a + 6)), cy + ry * math.sin(math.radians(a + 6)))
            arrow(s, p0, p1, GOLD)
