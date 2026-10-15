"""b08 BRIDGE WALKER: text, field notes and side diagrams.

Numbers are narrative, kept consistent with the model notes:
Span L = 18 m, cable sag f = 2.5 m, deck 1.2 m wide.
Design load w: crowd 4 kN/m2 x 1.2 m = 4.8 kN/m + deck and cables 0.6 kN/m
  = 5.4 kN/m. Horizontal cable pull H = w L^2 / (8 f) = 5.4 x 324 / 20
  = 87.5 kN, shared by two cables = 44 kN each. Tension at the tower
  T = H x sqrt(1 + (4 f / L)^2) = 44 x 1.14 = 50 kN per cable.
22 mm wire rope, minimum breaking force ~300 kN -> safety factor 6.
Deck: planks every 26 cm -> 69 planks; one plank every 90 s of laying.
Plan: day 1 anchors and towers, day 2 pilot line, day 3 main cables,
  day 4 suspenders and cross-beams, days 5-6 deck and handrail, then load test.
"""

ENTRY = dict(
    id='b08', series='B08', number=208, slug='bridge-walker', title='BRIDGE WALKER',
    domain='infrastructure', category='serious', model='BW-3', palette='emerald', seed=260108,
    purpose='FOOTBRIDGE-BUILDING ROBOT',
    narrative=('Crosses a river on its own work: strings two cables between the banks, then '
               'rides them to lay an 18 m footbridge in six days, so children can reach '
               'school through the rainy season.'),
    enabled_by=[
        ('CABLE ROBOTS', 'Machines that climb, clamp and position loads on wire rope.'),
        ('FOOTBRIDGE KITS', 'Proven suspended footbridge designs that villages already build and maintain.'),
        ('SITE SENSING', 'Probes and load cells that test each anchor before the deck goes on.'),
    ],
    real_basis='Cable robots, prefabricated suspended footbridges, locally sourced timber decks.',
    required_breakthroughs='Autonomous anchoring in unknown banks, with safety the community can verify itself.',
    view_A='SUSPENDED FOOTBRIDGE, DAY FIVE',
    view_B='CABLE SPOOL', view_B_note='HANDRAIL ROPE / LEVEL WIND / BRAKE / LOAD CELL',
    view_C='DECK LAYER', view_C_note='CLAMP ARM / HELD PLANK / BOLT DRIVER / CAMERA',
    service_year='2031',
    sources=['https://bridgestoprosperity.org/', 'https://www.nist.gov/el/intelligent-systems-division-73500/robocrane'],
    source_scope='Real basis only: community footbridge programmes, cable-driven robots, wire-rope design practice. The robot, the schedule and every figure are an original concept.',
)

DOSSIER = dict(
    kind='crossing',
    fact=('The robot rides the main cables it helped to string and bolts the deck down '
          'behind itself. Nobody crosses until the village has checked every anchor.'),
    rows=[('SPAN', '18 m / DECK 1.2 m WIDE'),
          ('BUILD TIME', '6 DAYS, BANK TO BANK'),
          ('DESIGN CROWD', '4 kN PER m² OF DECK'),
          ('MAIN CABLES', '2 x 22 mm / SAFETY FACTOR 6')],
    note='ON THE SEVENTH DAY THE CHILDREN WALKED TO SCHOOL WITH DRY FEET.',
    left=('SIX DAYS, BANK TO BANK', 'DECLARED BUILD PLAN / 18 m SPAN / DRY WEATHER',
          'The village digs the anchors; the robot does the work over the water.'),
    right=('HOW HARD THE CABLES PULL', 'PARABOLIC CABLE / UNIFORM LOAD / DESIGN VALUES',
           'H = w L² / 8f = 5.4 x 18² / (8 x 2.5) = 87.5 kN, shared by two cables.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        tasks = [('ANCHORS AND TOWERS', 0, 1, GOLD), ('PILOT LINE ACROSS', 1, 2, WHITE),
                 ('MAIN CABLES', 2, 3, WHITE), ('SUSPENDERS AND BEAMS', 3, 4, WHITE),
                 ('DECK AND HANDRAIL', 4, 6, ARC), ('LOAD TEST, SIGN-OFF', 6, 6.5, GOLD)]
        gx = x + 150; dw = 38
        for d in range(7):
            s.ln(gx + d * dw, y - 2, gx + d * dw, y + 108, .12, .4)
            tx(s, f'{d + 1}', gx + d * dw + dw / 2, y + 122, 6.4, .6, align='c')
        tx(s, 'DAY', gx - 10, y + 122, 6.2, .55, align='r')
        for i, (name, a, b, col) in enumerate(tasks):
            yy = y + 6 + i * 18
            tx(s, name, x, yy + 5, 6.4, .78)
            s.rect(gx + a * dw + 2, yy - 2, (b - a) * dw - 4, 8, .85, .7, color=col)
        s.ln(gx + 4 * dw + dw * .5, y - 6, gx + 4 * dw + dw * .5, y + 110, .6, .6, dash=[2, 2])
        tx(s, 'DRAWN', gx + 4 * dw + dw * .5 + 4, y - 6, 6, .6)
    else:
        # Parabola between two supports; span L and sag f marked; H at the ends.
        x0 = x + 60; x1 = x + 330; yt = y + 12; f = 52
        pts = [(x0 + (x1 - x0) * i / 60, yt + f * (1 - (2 * i / 60 - 1) ** 2)) for i in range(61)]
        s.poly(pts, .85, .85, close=False, color=GOLD)
        for xx in (x0, x1):
            s.ln(xx, yt - 4, xx, yt + 86, .6, .7)
        s.ln(x0, yt + 86, x1, yt + 86, .35, .5)
        for i in range(1, 12):
            xx = x0 + (x1 - x0) * i / 12
            arrow(s, (xx, yt + f * (1 - (2 * i / 12 - 1) ** 2) + 4), (xx, yt + f * (1 - (2 * i / 12 - 1) ** 2) + 16), WHITE)
        tx(s, 'w = 5.4 kN/m', (x0 + x1) / 2, yt + f + 30, 6.4, .75, align='c')
        mx = (x0 + x1) / 2
        s.ln(mx, yt, mx, yt + f, .5, .6, dash=[2, 2])
        s.ln(x0, yt, x1, yt, .2, .5, dash=[2, 2])
        tx(s, 'f = 2.5 m', mx + 6, yt + f / 2 + 3, 6.4, .8)
        tx(s, 'L = 18 m', mx, yt + 100, 6.4, .8, align='c')
        arrow(s, (x0 - 4, yt), (x0 - 40, yt), ARC)
        arrow(s, (x1 + 4, yt), (x1 + 40, yt), ARC)
        tx(s, 'H', x0 - 44, yt + 3, 6.8, .85, align='r', color=ARC)
        tx(s, 'H', x1 + 44, yt + 3, 6.8, .85, color=ARC)
        tx(s, '44 kN', x1 + 44, yt + 18, 6.4, .7)
        tx(s, 'PER CABLE', x1 + 44, yt + 31, 6.2, .6)
