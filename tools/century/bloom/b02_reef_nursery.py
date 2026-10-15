"""b02 REEF NURSERY: text, field notes and side diagrams.

Numbers are narrative, kept consistent with the model notes:
40 trees x 96 fragments (4 tiers x 6 arms x 2 lines x 2) = 3 840 growing.
Grow-out 6 months -> 2 cycles a year. Each grown colony is cut into 4:
1 goes back on the tree, 3 go to the reef -> 3 840 x 3 x 2 = 23 040 a year.
Trays hold 24 -> 960 tray lifts a year, about 4 on a working day.
Solar: 10 petals x 2 m2 x 210 W/m2 = 4.2 kW peak; 30 kWh storage runs the winch,
lights, pumps and sensors through the night.
Heat screen: hold at the local maximum monthly mean (MMM) + 3 degC for
10 days after a 3-day ramp; colonies that stay pigmented become parents.
"""

ENTRY = dict(
    id='b02', series='B02', number=202, slug='reef-nursery', title='REEF NURSERY',
    domain='ocean', category='serious', model='RN-2', palette='violet', seed=260102,
    purpose='CORAL RESTORATION PLATFORM',
    narrative=('Grows heat-tolerant coral fragments on lattice trees moored around a solar '
               'platform, then lowers them in trays for divers to plant on bleached reefs. '
               'One platform returns about 23 000 fragments a year.'),
    enabled_by=[
        ('CORAL GARDENING', 'Fragments on mid-water trees reach planting size in months, as in today\'s nurseries.'),
        ('ASSISTED EVOLUTION', 'Research that selects and breeds corals for higher heat tolerance.'),
        ('MARINE SOLAR', 'Floating panels and batteries that run the winch, lights and sensors offshore.'),
    ],
    real_basis='Coral gardening on mid-water trees, assisted evolution of heat tolerance, solar marine platforms.',
    required_breakthroughs='Coral strains that stay heat-tolerant for decades without losing genetic diversity.',
    view_A='MOORED LATTICE-TREE NURSERY',
    view_B='LATTICE TREE', view_B_note='BUOY / TOP TWO OF FOUR TIERS / FRAGMENT LINES / ID TAGS',
    view_C='FRAGMENT TRAY', view_C_note='24 CERAMIC PLUGS / LIFTING BRIDLE / REEF TAG',
    service_year='2033',
    sources=['https://www.fisheries.noaa.gov/national/habitat-conservation/restoring-coral-reefs',
             'https://www.aims.gov.au/research/climate-change/assisted-evolution'],
    source_scope='Real basis only: coral tree nurseries, outplanting practice, heat-tolerance selection research. The platform, its output and every figure are an original concept.',
)

DOSSIER = dict(
    kind='nursery',
    fact=('Fragments are cut from survivors of the last heatwave. The nursery multiplies '
          'them; the divers choose where they go.'),
    rows=[('TRAY LIFTS', '960 A YEAR / 4 ON A WORKING DAY'),
          ('GROW-OUT', '6 MONTHS / 4 CUTS PER COLONY'),
          ('PONTOON RING', '6.6 m ACROSS / 8 m OF WATER BELOW'),
          ('PARENT GENOTYPES', '30 OR MORE PER SPECIES')],
    note='EVERY TRAY CARRIES THE NAME OF THE REEF IT RETURNS TO.',
    left=('FROM SURVIVOR TO REEF', 'ANNUAL CYCLE / DESIGN TARGETS',
          '3 840 growing × 3 outplanted cuts × 2 cycles = 23 040 fragments a year.'),
    right=('KEEP THE ONES THAT KEPT THEIR COLOUR', 'HEAT SCREEN / DESIGN SCHEDULE',
           'MMM is the home reef\'s maximum monthly mean temperature; the ramp takes three days.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        # Four stations: parent colony, tree, cut, tray -> reef. Icons are drawn.
        cy = y + 46
        # The first station's name is the widest: keep it inside the column.
        x0 = x + max(30, s.measure('SURVIVOR', 6.6, .08) / 2 + 2)
        xs = [x0 + (x + 360 - x0) * k / 3 for k in range(4)]

        def bush(cx, by, k=1.0, col=WHITE, a=.8):
            s.poly([(cx, by), (cx, by - 18 * k)], a, .8, close=False, color=col)
            for dx, h in ((-7, 13), (7, 12), (-3, 20), (4, 17)):
                s.poly([(cx, by - h * .45 * k), (cx + dx * k, by - h * k)], a, .7, close=False, color=col)
        # 1 parent colony on the reef
        bush(xs[0], cy + 14, 1.2, GOLD)
        s.ln(xs[0] - 20, cy + 14, xs[0] + 20, cy + 14, .5, .6)
        # 2 tree: mast, three tiers
        s.ln(xs[1], cy - 26, xs[1], cy + 20, .8, .8)
        s.circ(xs[1], cy - 31, 5, .75, .7)
        for k, yy in enumerate((cy - 16, cy - 2, cy + 12)):
            s.ln(xs[1] - 18, yy, xs[1] + 18, yy, .6, .6)
            for dx in (-18, 18):
                bush(xs[1] + dx, yy + 9, .4, ARC, .85)
        # 3 cut into four
        for k in range(4):
            bush(xs[2] - 18 + 12 * k, cy + 12, .55, ARC if k else GOLD, .85)
        # 4 tray of plugs
        s.rect(xs[3] - 26, cy + 4, 52, 10, .7, .6)
        for k in range(5):
            bush(xs[3] - 20 + 10 * k, cy + 4, .45, ARC, .85)
        for a_, b_ in zip(xs, xs[1:]):
            arrow(s, (a_ + 30, cy), (b_ - 30, cy), WHITE)
        # 1 of 4 cuts goes back on the tree.
        s.poly([(xs[2] - 18, cy + 26), (xs[2] - 18, cy + 34), (xs[1], cy + 34), (xs[1], cy + 26)], .55, .6, close=False, color=GOLD)
        s.poly([(xs[1] - 3, cy + 30), (xs[1], cy + 25), (xs[1] + 3, cy + 30)], .55, .6, close=False, color=GOLD)
        tx(s, '1 OF 4 REGROWS', (xs[1] + xs[2]) / 2 - 9, cy + 48, 6.4, .72, align='c', color=GOLD)
        labels = [('SURVIVOR', 'PARENT'), ('TREE', '3 840 / 6 MO'), ('CUT', '3 TO THE REEF'), ('TRAY', '24 PLUGS')]
        for xx, (a_, b_) in zip(xs, labels):
            tx(s, a_, xx, y + 4, 6.6, .85, align='c')
        for xx, (a_, b_) in zip(xs, labels):
            tx(s, b_, xx, cy + 70, 6.4, .66, align='c')
    else:
        # Design temperature schedule: 3 days ramp, 10 days hold, 3 days return.
        legend = max(s.measure(t_, 6.4, .08) for t_ in ('COLOUR KEPT', 'BLEACHED', 'RECOVERS'))
        px = x + 58; top = y + 8; h = 92
        pw = min(300, x + w - legend - 16 - 22 - px)
        days = 17
        X = lambda d: px + pw * d / days
        Y = lambda t: top + h * (1 - t / 4)          # t = degC above MMM, 0..4
        s.poly([(px, top - 4), (px, top + h), (px + pw, top + h)], .48, .55, close=False)
        for t in (1, 2, 3):
            s.ln(px, Y(t), px + pw, Y(t), .12, .4)
        s.text_mid('MMM', px - 8, Y(0), 6.4, .08, .6, align='r')
        s.text_mid('+3 °C', px - 8, Y(3), 6.4, .08, .8, align='r', color=GOLD)
        pts = [(X(0), Y(0)), (X(1), Y(0)), (X(4), Y(3)), (X(14), Y(3)), (X(16), Y(0)), (X(17), Y(0))]
        s.poly(pts, .85, .85, close=False, color=GOLD)
        for d in (1, 4, 14, 16):
            s.ln(X(d), top + h, X(d), top + h + 4, .45, .5)
        tx(s, 'RAMP', (X(1) + X(4)) / 2, Y(3) - 8, 6.2, .6, align='c')
        tx(s, 'HOLD 10 DAYS', (X(4) + X(14)) / 2, Y(3) - 8, 6.4, .78, align='c')
        tx(s, 'DAY', px + pw, top + h + 16, 6.2, .55, align='r')
        # Outcome markers: pigmented kept, pale not kept (symbols only, no counts).
        ox = px + pw + 22
        s.circ(ox + 5, top + 22, 5, .85, .8, color=ARC)
        s.circ(ox + 5, top + 22, 2.4, .6, .6, color=ARC)
        s.text_mid('COLOUR KEPT', ox + 16, top + 22, 6.4, .08, .8)
        tx(s, 'PARENT', ox + 16, top + 38, 6.2, .6)
        s.circ(ox + 5, top + 66, 5, .45, .6, dash=[1.5, 1.5])
        s.text_mid('BLEACHED', ox + 16, top + 66, 6.4, .08, .66)
        tx(s, 'RECOVERS', ox + 16, top + 82, 6.2, .55)
