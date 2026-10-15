"""b24 CAROUSEL LAMP: text, field notes and side diagrams.

Numbers are narrative, kept consistent with the model:
Deck 2.5 m across (rim radius 1.25 m). Rim speed held at 3.5 m/s ->
omega = 3.5 / 1.25 = 2.8 rad/s = 27 rpm (a common playground limit for
roundabouts is about 5 m/s at the rim; this one stays well below).
Step-up 1:21 -> flywheel at about 570-600 rpm.
Flywheel: steel disc, radius 0.30 m, 8 cm thick:
m = pi x 0.30^2 x 0.08 x 7850 = 178 kg ("180 kg");
I = 0.5 x 178 x 0.09 = 8.0 kg m2; at 600 rpm (62.8 rad/s)
E = 0.5 x 8.0 x 62.8^2 = 15.8 kJ; that keeps 80 W flowing ~3 minutes.
Play: break 30 min + lunch 45 min + after school 60 min = 135 min a day
at an average 80 W electrical: 40 + 60 + 80 = 180 Wh a day.
Light: reading room 4 x 6 W = 24 W, door lamp 8 W = 32 W; 5.5 h a
night = 176 Wh. Battery 1 kWh LiFePO4 in the lamp plinth: about five
evenings if nobody plays (e.g. a rainy week).
"""

ENTRY = dict(
    id='b24', series='B24', number=224, slug='carousel-lamp', title='CAROUSEL LAMP',
    domain='schools', category='serious', model='CL-6', palette='berry', seed=260124,
    purpose='PLAYGROUND ENERGY ROUNDABOUT',
    narrative=('A roundabout that keeps the energy of children playing at break time and '
               'gives it back at night as light for the school reading room. Every push '
               'turns a flywheel under the yard; the harder they push, the more light, never more speed.'),
    enabled_by=[
        ('PLAY ENERGY', 'Playground roundabouts that already turn small generators as children play.'),
        ('FLYWHEEL STORAGE', 'A spinning steel disc that smooths bursts of pushing into steady charge.'),
        ('LED LIGHTING', 'Lamps that light a reading room for an evening on a few tens of watts.'),
    ],
    real_basis='Flywheel and generator playgrounds, LED lighting and small batteries.',
    required_breakthroughs='Robust, safe mechanisms that survive a decade of enthusiastic use.',
    view_A='SCHOOLYARD ROUNDABOUT OVER ITS FLYWHEEL',
    view_B='FLYWHEEL HUB', view_B_note='CLUTCH / STEP-UP / FLYWHEEL / LIMITER / GENERATOR',
    view_C='LAMP POST', view_C_note='LED HEAD / CONTROLLER / BATTERY PLINTH / CONDUIT',
    service_year='2029',
    sources=['https://www.en-standard.eu/bs-en-1176-5-2019-playground-equipment-and-surfacing-roundabouts/'],
    source_scope='Real basis only: generator-driven play equipment, flywheel storage, LED lighting, roundabout safety standards. The machine, schedule and all figures are an original concept.',
)

DOSSIER = dict(
    kind='school day',
    fact=('A one-way clutch lets every push add to the flywheel and nothing pull back. '
          'Above a steady walking pace the limiter turns extra push into charge.'),
    rows=[('PLAY', '135 MIN A DAY / ABOUT 80 W'),
          ('STORED', '180 Wh A DAY / 1 kWh BATTERY'),
          ('LIGHT', '32 W / 5.5 HOURS A NIGHT'),
          ('RIM SPEED', 'HELD BELOW 3.5 m/s')],
    note='THE LIGHT THEY READ BY TONIGHT, THEY SPUN AT BREAK TIME.',
    left=('PLAY IN, LIGHT OUT', 'DECLARED DAILY BUDGET / Wh / ONE SCHOOL DAY',
          'Averages, not measurements: 80 W while in use; the battery covers a rainy week.'),
    right=('HARDER PUSHING, SAME SAFE SPEED', 'DECLARED LIMITER RULE / NOT A TEST RESULT',
           'Below 100 W the deck speeds up; above it, the eddy brake takes the extra as charge.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        bx = x + 96; scale = 300 / 200.0
        rows = [('PLAY', [('BREAK', 40, WHITE), ('LUNCH', 60, GOLD), ('AFTER SCHOOL', 80, WHITE)], '180 Wh'),
                ('LIGHT', [('READING ROOM 24 W', 132, ARC), ('LAMP', 44, WHITE)], '176 Wh')]
        for i, (label, parts, total) in enumerate(rows):
            yy = y + 24 + i * 52
            tx(s, label, x, yy + 4, 7)
            xx = bx
            for name, wh, col in parts:
                s.rect(xx, yy - 7, wh * scale, 14, .85, .7, color=col)
                tx(s, name, xx + 2, yy - 13, 6.2, .62)
                xx += wh * scale
            tx(s, total, xx + 8, yy + 4, 6.8, .8)
        axis = y + 116
        s.ln(bx, axis, bx + 300, axis, .45, .55)
        for v in (0, 50, 100, 150, 200):
            s.ln(bx + v * scale, axis, bx + v * scale, axis + 4, .45, .5)
            tx(s, str(v), bx + v * scale, axis + 14, 6.4, .6, align='c')
        tx(s, 'Wh', x, axis + 4, 6.6, .55)
    else:
        px = x + 40; pw = 300; ph = 100; py = y + 6
        def X(p): return px + pw * p / 300.0
        def Y(v): return py + ph * (1 - v / 5.0)
        for v in (0, 1, 2, 3, 4, 5):
            s.ln(px, Y(v), px + pw, Y(v), .12, .4)
        s.poly([(px, py), (px, py + ph), (px + pw, py + ph)], .5, .55, close=False)
        s.ln(px, Y(5), px + pw, Y(5), .55, .6, dash=[4, 4])
        tx(s, 'PLAYGROUND LIMIT 5 m/s', px + pw, Y(5) - 5, 6.2, .6, align='r')
        pts = []
        for k in range(61):
            p = 300 * k / 60
            pts.append((X(p), Y(3.5 * min(1.0, (p / 100.0)) ** .5 if p < 100 else 3.5)))
        s.poly(pts, .9, .85, close=False, color=ARC)
        tx(s, 'RIM SPEED', X(170), Y(3.5) - 12, 6.4, .8, color=ARC)
        s.ln(X(100), Y(0), X(100), Y(3.5), .4, .5, dash=[2, 3])
        s.poly([(X(100), Y(0)), (X(300), Y(0) - 70)], .85, .8, close=False, color=GOLD)
        tx(s, 'EXTRA CHARGE', X(300) + 6, Y(0) - 64, 6.4, .8, color=GOLD)
        tx(s, '5', px - 8, Y(5) + 3, 6.2, .55, align='r'); tx(s, '0', px - 8, Y(0) + 3, 6.2, .55, align='r')
        tx(s, 'm/s', px - 8, Y(2.5) + 3, 6.2, .55, align='r')
        for p in (0, 100, 200, 300):
            tx(s, str(p), X(p), py + ph + 13, 6.4, .6, align='c')
        tx(s, 'PUSH / W', px + pw, py + ph + 27, 6.4, .6, align='r')
