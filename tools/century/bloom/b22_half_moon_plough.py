"""b22 HALF-MOON PLOUGH: text, field notes and side diagrams.

Numbers are narrative, kept consistent with the model notes:
Half-moon 4 m across, 25 cm deep at the centre; bund on the downslope side.
Layout: 8 m apart along the contour, rows 4 m apart, staggered by 4 m
  -> 32 m2 per half-moon -> 10 000 / 32 = 313 per hectare.
A 20 mm storm on each 32 m2 share = 32 x 0.020 m = 0.64 m3 = up to 640 L
  held in the basin instead of running off the crusted ground.
Pace: one half-moon every 40 s including the move -> 313 x 40 s = 3.5 h,
  "a hectare in a morning". By hand, one person digs about five a day.
Energy: about 6 kW average over 3.5 h = 21 kWh of a 30 kWh battery
  -> one hectare on one charge. Canopy panel 1.5 m2 -> ~300 W top-up.
"""

ENTRY = dict(
    id='b22', series='B22', number=222, slug='half-moon-plough', title='HALF-MOON PLOUGH',
    domain='land', category='serious', model='HP-4', palette='crimson', seed=260122,
    purpose='DRYLAND REGREENING TRACTOR',
    narrative=('Digs half-moon basins across bare Sahel ground, a hectare in a morning, and '
               'drops grass seed and one tree seed into each. The next rain soaks in instead '
               'of running off; grass and young trees return within two seasons.'),
    enabled_by=[
        ('DEMI-LUNES', 'Hand-dug half-moons already regreen farms in Niger and Burkina Faso.'),
        ('SMALL E-TRACTORS', 'Battery tractors charged from village solar, not diesel.'),
        ('DIRECT SEEDING', 'Local grass and acacia seed placed where the water pools.'),
    ],
    real_basis='Demi-lune water harvesting, the Great Green Wall, electric tractors.',
    required_breakthroughs='Cheap machines that farmers can repair themselves in the field.',
    view_A='HALF-MOON BASINS ON A SAHEL SLOPE',
    view_B='CRESCENT BLADE', view_B_note='SLEWING RING / SWING ARM / TOOTHED BLADE / DEPTH SKIDS',
    view_C='SEED HOPPER', view_C_note='FLUTED METERING ROLLER / DROP TUBE TO THE BASIN',
    service_year='2030',
    sources=['https://www.wocat.net/', 'https://www.unccd.int/our-work/ggwi'],
    source_scope='Real basis only: demi-lune water harvesting and regreening programmes. The tractor, the implement and every figure are an original concept.',
)

DOSSIER = dict(
    kind='first rain',
    fact=('Crusted ground sheds most of a storm. A half-moon catches the water running '
          'down the slope and holds it long enough to soak into the root zone.'),
    rows=[('HALF-MOONS', '313 A HECTARE / 4 m ACROSS'),
          ('PACE', 'ONE EVERY 40 s / 1 ha A MORNING'),
          ('RAIN HELD', 'UP TO 640 L IN A 20 mm STORM'),
          ('BATTERY', '30 kWh / ONE HECTARE A CHARGE')],
    note='AFTER THE FIRST RAIN AISSATA FOUND WATER STANDING IN EVERY BASIN.',
    left=('SHAPED TO HOLD THE RAIN', 'SECTION DOWN THE SLOPE / NOT TO SCALE',
          'The bund stands downslope; the open side faces the run-off coming down the hill.'),
    right=('STAGGERED, SO LITTLE ESCAPES', 'PLAN / 8 m ALONG THE CONTOUR / ROWS 4 m APART',
           'Water that slips between two basins meets the next row; 32 m² each, 313 a hectare.'),
)


def figure(s, side, x, y, w):
    import math
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        # Section: slope falls to the right; basin cut, bund downslope.
        x0, x1 = x + 10, x + 400
        def gy(xx): return y + 40 + (xx - x0) * .12
        pit0, pit1 = x + 170, x + 290
        pts = [(x0, gy(x0)), (pit0, gy(pit0))]
        for k in range(21):
            t = k / 20
            xx = pit0 + (pit1 - pit0) * t
            pts.append((xx, gy(xx) + 26 * math.sin(math.pi * t) ** .8))
        bund = [(pit1 + 30 * k / 10, gy(pit1 + 30 * k / 10) - 16 * math.sin(math.pi * k / 10)) for k in range(11)]
        s.poly(pts + bund + [(x1, gy(x1))], .8, .8, close=False)
        # Water pooled in the basin; infiltration below it.
        wl = gy(pit0) + 10
        s.ln(pit0 + 18, wl, pit1 - 4, wl, .8, .8, color=ARC)
        for xx in (pit0 + 40, pit0 + 70, pit0 + 100):
            arrow(s, (xx, wl + 22), (xx, wl + 52), ARC)
        for xx in (x0 + 20, x0 + 70, x0 + 120):
            arrow(s, (xx, gy(xx) - 10), (xx + 34, gy(xx + 34) - 8), WHITE)
        tx(s, 'RUN-OFF', x0 + 10, gy(x0) - 18, 6.4, .7)
        tx(s, 'BUND', pit1 + 8, gy(pit1) - 24, 6.4, .7)
        tx(s, 'SOAKS IN', pit0 + 110, wl + 50, 6.4, .75, color=ARC)
        tx(s, '25 cm', pit0 + 10, wl + 14, 6.2, .6, align='r')
    else:
        # Plan: three staggered rows of crescents, flow arrows downhill (down the page).
        R = 20
        def crescent(cx, cy, a=.85):
            pts = [(cx + R * math.cos(t), cy + R * .8 * math.sin(t)) for t in [math.pi * k / 20 for k in range(21)]]
            s.poly(pts, a, .9, close=False)
        rows = [(y + 18, (x + 50, x + 150, x + 250)), (y + 58, (x + 100, x + 200, x + 300)), (y + 98, (x + 50, x + 150, x + 250))]
        for cy, xs in rows:
            for cx in xs:
                crescent(cx, cy)
        # Water passing between two basins of row 1 is caught by row 2.
        arrow(s, (x + 100, y - 4), (x + 100, y + 44), ARC)
        arrow(s, (x + 200, y - 4), (x + 200, y + 44), ARC)
        s.ln(x + 50 - R, y + 124, x + 150 - R, y + 124, .45, .5)
        tx(s, '8 m', x + 100 - R, y + 136, 6.4, .7, align='c')
        s.ln(x + 330, y + 18, x + 330, y + 58, .45, .5)
        tx(s, '4 m', x + 338, y + 42, 6.4, .7)
        tx(s, 'DOWNHILL', x + 360, y + 110, 6.4, .6)
        arrow(s, (x + 372, y + 70), (x + 372, y + 98), WHITE)
