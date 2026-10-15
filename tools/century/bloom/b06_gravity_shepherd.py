"""b06 GRAVITY SHEPHERD: text, field notes and side diagrams.

Numbers are narrative, kept consistent with the model and each other:
Asteroid 30 m across, bulk density 2 000 kg/m3 -> M = 2000 x 4/3 pi 15^3
= 2.8e7 kg (~28 000 t); a 30 m stony body is a city-scale airburst.
Craft ~100 t = 4.5 t dry + 0.3 t xenon + one 4.5 m boulder lifted from the
surface (4/3 pi 2.25^3 = 47.7 m3 x 2 000 kg/m3 = 95 t).
Hover d = 40 m centre to centre (the rock's 15 m radius + 25 m).
Pull on the asteroid: a = G m / d^2 = 6.674e-11 x 1e5 / 40^2 = 4.2e-9 m/s2.
Two years of hover (6.31e7 s): delta-v = a t = 0.26 m/s.
Ideal along-track drift, near-circular orbit: s = 1.5 a t^2 while towing
(25 000 km at year 2), then + 3 delta-v (t - 2 y): +150 000 km by year 8
-> ~175 000 km at the 2085 encounter, almost halfway to the Moon.
Station-keeping thrust: F = G M m / d^2 = 0.118 N along the line; engines
canted 36 deg (limb at asin(15/40) = 22 deg + 12 deg plume half-angle):
0.118 / cos 36 = 0.146 N, eight thrusters (two pods of four) x 18 mN.
Isp 3 000 s -> 5.0e-6 kg/s -> ~0.3 t of xenon in two years.
Power ~35 W per mN = 5.1 kW plus the bus. Wings 2 x 22 m x 6 m = 264 m2
x ~170 W/m2 = 45 kW at 1 AU, sized for the 2.2 AU aphelion: 45 / 2.2^2 = 9 kW.
"""
import math

ENTRY = dict(
    id='b06', series='B06', number=206, slug='gravity-shepherd', title='GRAVITY SHEPHERD',
    domain='planetary defence', category='serious', model='GS-2', palette='graphite', seed=260106,
    purpose='ASTEROID GRAVITY TRACTOR',
    narrative=('Hovers beside a 30 m asteroid for two years and moves it by gravity alone. In 2085 '
               'it passes Earth 175 000 km away, almost halfway to the Moon. Nothing touches '
               'the rock and nothing breaks off it.'),
    enabled_by=[
        ('ION PROPULSION', 'Gridded ion thrusters that run for years on a few hundred kilograms of xenon.'),
        ('TRACTOR STUDIES', 'Analyses showing that a hovering craft can tow an asteroid without contact.'),
        ('DART RESULTS', 'A measured change in an asteroid orbit and better models of rubble-pile bodies.'),
    ],
    real_basis='Ion propulsion, gravity-tractor studies and the DART results.',
    required_breakthroughs='Autonomous station-keeping for years beside an irregular, spinning body.',
    view_A='GRAVITY TRACTOR ON STATION',
    view_B='ION ENGINE CLUSTER', view_B_note='FOUR GIMBALLED THRUSTERS / PLATE / PPU / XENON VALVE',
    view_C='HOVER SENSORS', view_C_note='SCANNING LIDAR / ALTIMETERS / STEREO CAMERAS',
    service_year='2077',
    sources=['https://doi.org/10.1038/438177a', 'https://science.nasa.gov/mission/dart/'],
    source_scope='Real basis only: the gravity-tractor principle (Lu and Love, 2005), ion propulsion flight heritage, the DART deflection. The craft, the asteroid, the encounter and every figure are an original, idealised concept.',
)

DOSSIER = dict(
    kind='tow',
    fact=('The spacecraft never touches the rock. Its own mass pulls the asteroid, '
          'and its engines keep it from falling in.'),
    rows=[('HOVER DISTANCE', '40 m CENTRE TO CENTRE'),
          ('PULL ON THE ASTEROID', '4.2 x 10⁻⁹ m/s²'),
          ('TWO YEARS OF HOVER', 'DELTA-V 26 cm/s'),
          ('MISS DISTANCE, 2085', 'ABOUT 175 000 km')],
    note='IT WILL PASS IN 2085 AND KEEP GOING.',
    left=('AIM THE EXHAUST PAST THE ROCK', 'FORCE GEOMETRY / ANGLES FROM THE MODEL / NOT TO SCALE',
          'Useful thrust along the line is F cos 36°: about 19 % is spent keeping the rock clean.'),
    right=('A SMALL PULL, A LONG LEVER', 'IDEAL ALONG-TRACK DRIFT / NEAR-CIRCULAR ORBIT',
           'Towing: s = 1.5 a t². After: + 3 delta-v t. Real paths need full orbit models.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow, axes, curve
    if side == 'left':
        cx, cy, r = x + 50, y + 62, 26
        d = r * 40 / 15
        kx, ky = cx + d, cy
        pts = []
        for k in range(73):
            a = math.tau * k / 72
            pts.append((cx + r * math.cos(a) * (1 + .06 * math.sin(3 * a)), cy + r * math.sin(a) * (1 + .05 * math.cos(2 * a))))
        s.poly(pts, .7, .7, close=True)
        tx(s, 'ROCK', cx, cy + 3, 6.4, .55, align='c')
        # Limb tangents from the craft (dashed), plume axes and cones.
        lim = math.asin(15 / 40)
        for sg in (-1, 1):
            s.ln(kx, ky, kx - d * math.cos(lim) * math.cos(lim), ky + sg * d * math.cos(lim) * math.sin(lim), .35, .5, dash=[2, 3])
            for da, a_, wdt in ((0, .85, .8), (-12, .35, .5), (12, .35, .5)):
                q = math.radians(36 + da)
                L = 82
                s.ln(kx, ky, kx - L * math.cos(q), ky + sg * L * math.sin(q), a_, wdt, color=ARC if da == 0 else WHITE)
        # Forces on the craft: gravity toward the rock, resultant thrust away.
        arrow(s, (kx + 4, ky), (kx + 40, ky), GOLD)
        s.dot(kx, ky, 3.2, .95)
        tx(s, 'CRAFT', kx + 8, ky + 18, 6.4, .7)
        tx(s, 'NET THRUST', kx + 46, ky + 3, 6.4, .8, color=GOLD)
        lx = kx + 46
        tx(s, '36° CANT', lx, ky - 38, 6.6, .85, color=ARC)
        tx(s, '22° TO THE LIMB', lx, ky - 22, 6.4, .65)
        tx(s, 'PLUMES PASS BOTH SIDES', lx, ky + 30, 6.4, .65)
        # Hover distance as a dimension line under the geometry.
        dy = cy + 68
        s.ln(cx, dy, kx, dy, .5, .5)
        for xx in (cx, kx):
            s.ln(xx, dy - 4, xx, dy + 4, .5, .5)
        tx(s, '40 m', (cx + kx) / 2, dy - 4, 6.4, .8, align='c')
    else:
        ax = x + 34; aw = w - 68; ah = 92
        axes(s, ax, y, aw, ah, 'YEARS FROM THE START OF THE TOW', '200 000', '0')
        yr = 3.156e7; a = 4.17e-9; T = 2 * yr; dv = a * T; top = 2e8

        def drift(t):
            t *= yr
            return 1.5 * a * t * t if t <= T else 1.5 * a * T * T + 3 * dv * (t - T)
        curve(s, [(ax + aw * i / 240, y + ah * (1 - drift(8 * i / 240) / top)) for i in range(241)], GOLD)
        for t in (0, 2, 4, 6, 8):
            s.ln(ax + aw * t / 8, y + ah, ax + aw * t / 8, y + ah + 4, .45, .5)
            tx(s, str(t), ax + aw * t / 8, y + ah + 13, 6.6, .65, align='c')
        tx(s, 'km', ax - 9, y + 16, 6.2, .5, align='r')
        # Earth radius for scale: the drift passes it within the tow.
        ey = y + ah * (1 - 6.371e6 / top)
        s.ln(ax, ey, ax + aw, ey, .35, .5, dash=[2, 3])
        tx(s, 'EARTH RADIUS', ax + aw, ey - 4, 6.2, .6, align='r')
        mx = ax + aw * 2 / 8
        s.ln(mx, y, mx, y + ah, .35, .5, dash=[2, 3])
        tx(s, 'TOW ENDS', mx + 6, y + 10, 6.4, .75)
        fy = y + ah * (1 - drift(8) / top)
        s.dot(ax + aw, fy, 2.6, .95, color=ARC)
        tx(s, '175 000 km IN 2085', ax + aw, y + 40, 6.4, .85, align='r', color=ARC)
