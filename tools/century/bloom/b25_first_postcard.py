"""b25 FIRST POSTCARD: text, field notes and side diagrams.

Numbers (narrative, idealised, consistent with each other):
Sail 4 m across, 1 g; chip 1 g -> 2 g in flight.
Laser array 100 GW, perfect reflection: F = 2 P / c = 2 x 1e11 / 3e8
= 667 N -> a = 667 / 0.002 = 3.3e5 m/s2 (about 34 000 g).
0.2 c = 6.0e7 m/s -> push time t = 6.0e7 / 3.3e5 = 180 s (3 minutes);
distance during the push 0.5 a t^2 = 5.4e9 m (5.4 million km).
Focus: spot 2.44 lambda d / D with lambda = 1.06 um, d = 5.4e9 m, spot 4 m
-> D = 2.44 x 1.06e-6 x 5.4e9 / 4 = 3.5 km: the array is 3.5 km across.
Energy per launch 100 GW x 180 s = 1.8e13 J = 5 GWh.
Proxima Centauri 4.24 light years: 4.24 / 0.2 = 21.2 years out; the photo
comes back at light speed in 4.24 years -> 25.4 years after launch.
Launch 2050 -> arrival 2071, photograph on Earth 2075.
A child of seven at launch is 32 when the picture arrives.
"""
import math

ENTRY = dict(
    id='b25', series='B25', number=225, slug='first-postcard', title='FIRST POSTCARD',
    domain='interstellar', category='serious', model='FP-1', palette='sage', seed=260125,
    purpose='INTERSTELLAR LIGHT-SAIL PROBE',
    narrative=('A one-gram chip on a mirror sail, pushed for three minutes by a field of lasers on '
               'Earth, reaches the nearest star in 21 years and sends home the first photograph '
               'of another world.'),
    enabled_by=[
        ('LIGHT SAILS', 'Thin reflective sails that have already flown in space, such as LightSail 2.'),
        ('PHASED LASERS', 'Arrays of fibre lasers held in phase so they act as one very large beam.'),
        ('GRAM PROBES', 'Chip-scale spacecraft with a camera, a radio and power on a few grams.'),
    ],
    real_basis='Breakthrough Starshot studies, phased laser arrays and ultralight sails.',
    required_breakthroughs='Sails that survive minutes of intense laser light at a fifth of light speed.',
    view_A='SAIL PROBE OVER ITS LASER FIELD',
    view_B='SAIL CHIP', view_B_note='CAMERA / LASER LINK / BATTERY / THRUSTER PODS',
    view_C='LASER EMITTER', view_C_note='SEVEN LENSES / TILT YOKE / FIBRE FEED / COOLANT',
    view_A_fit=(720, 700),
    service_year='2050',
    sources=['https://breakthroughinitiatives.org/initiative/3', 'https://doi.org/10.1016/j.actaastro.2016.06.025'],
    source_scope='Real basis only: the Breakthrough Starshot concept and its sail and laser studies. The probe, the field, the drawing (probe enlarged, not to scale) and every figure are an original, idealised concept.',
)

DOSSIER = dict(
    kind='launch',
    fact=('Light carries momentum. Reflected, a hundred gigawatts pushes with about 667 newtons: '
          'enough to throw two grams to a fifth of light speed.'),
    rows=[('IN FLIGHT', '2 g / SAIL 4 m ACROSS'),
          ('PUSH', '100 GW FOR 3 MINUTES'),
          ('CRUISE', '0.2 c / PROXIMA IN 21 YEARS'),
          ('PHOTOGRAPH HOME', '2075 / 4.24 YEARS AT LIGHT SPEED')],
    note='SHE WATCHED THE LAUNCH AT SEVEN AND SAW THE PHOTOGRAPH AT THIRTY-TWO.',
    left=('THE LONG WAY HOME', 'DECLARED MISSION / 4.24 LIGHT YEARS / 0.2 c',
          '4.24 ly / 0.2 c = 21.2 years out; the picture takes 4.24 years to come back.'),
    right=('THREE MINUTES OF LIGHT', 'IDEAL REFLECTION / F = 2P / c / m = 2 g',
           'F = 2 x 100 GW / c = 667 N on 2 g: 0.2 c after about 180 s.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow, axes, curve
    if side == 'left':
        x0, x1 = x + 10, x + 400
        k = (x1 - x0) / 26.0
        yy = y + 50
        s.rect(x0, yy - 7, 21.2 * k, 14, .85, .8, color=ARC)
        s.rect(x0 + 21.2 * k, yy - 7, 4.24 * k, 14, .85, .8, color=GOLD)
        for t, label in ((0, '2050'), (21.2, '2071'), (25.44, '2075')):
            xx = x0 + t * k
            s.ln(xx, yy - 16, xx, yy + 16, .6, .6)
            tx(s, label, xx, yy + 30, 6.6, .8, align='l' if t == 0 else ('c' if t < 25 else 'r'))
        tx(s, 'LAUNCH', x0, yy - 24, 6.2, .7)
        tx(s, 'ARRIVAL', x0 + 21.2 * k - 5, yy - 24, 6.2, .7, align='r')
        tx(s, 'PHOTO ON EARTH', x1, yy + 50, 6.2, .75, align='r')
        tx(s, 'PROBE AT 0.2 c', x0 + 8, yy + 3, 6.4, .9, color=ARC)
        tx(s, 'LIGHT', x0 + 21.2 * k + 7, yy + 3, 6.4, .9, color=GOLD)
        for t in range(0, 26, 5):
            s.ln(x0 + t * k, yy + 9, x0 + t * k, yy + 12, .35, .5)
        tx(s, 'YEARS FROM LAUNCH, 0 TO 25', x0, yy + 80, 6.2, .55)
    else:
        px, py, pw, ph = x + 30, y + 4, 300, 96
        axes(s, px, py, pw, ph, 'SECONDS', '0.2 c', '0')
        tmax = 240
        X = lambda t: px + pw * t / tmax
        Y = lambda v: py + ph * (1 - v / .2)
        pts = [(X(t), Y(min(.2, .2 * t / 180))) for t in range(0, tmax + 1, 4)]
        curve(s, pts, ARC)
        s.ln(X(180), py, X(180), py + ph, .35, .5, dash=[2, 3], color=GOLD)
        tx(s, 'LASERS OFF', X(180) + 6, py + ph - 8, 6.2, .8, color=GOLD)
        for t in (0, 60, 120, 180, 240):
            tx(s, str(t), X(t), py + ph + 13, 6.2, .6, align='c')
        tx(s, 'a = 34 000 g', px + 20, py + 18, 6.4, .8)
