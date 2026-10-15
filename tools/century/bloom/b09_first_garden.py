"""b09 FIRST GARDEN: text, field notes and side diagrams.

Numbers are narrative, kept consistent with the model and each other:
Vault 12 m x 7 m (radius 3.5 m) -> ~84 m2 floor. Growing area:
far rack 10 m x 0.6 m x 4 tiers = 24 m2 + near deep beds 10 m x 0.9 m x
2 tiers = 18 m2 -> 42 m2.
Crew of four: O2 need 0.84 kg per person per day -> 3.4 kg/day.
Crops return ~20 g O2 per m2 per day (good light) -> 0.84 kg/day,
about a quarter of the crew's need; photosynthesis takes 44/32 x 0.84 =
1.16 kg CO2 a day (~1.2 kg).
Fresh produce ~107 g per m2 per day (greens, dwarf tomatoes, potatoes)
-> ~4.5 kg/day; at ~250 kcal/kg that is ~1 100 kcal, about 10 % of the
crew's 4 x 2 800 kcal.
Transpiration ~3.3 L per m2 per day -> ~140 L/day, condensed and returned.
Cabin air 50 kPa with 30 % oxygen (partial pressure 15 kPa, close to a
2 700 m altitude on Earth). Lamps ~3 kW average, heat shed by the radiator.
"""

ENTRY = dict(
    id='b09', series='B09', number=209, slug='first-garden', title='FIRST GARDEN',
    domain='life support', category='serious', model='FG-1', palette='umber', seed=260109,
    purpose='MARTIAN GREENHOUSE',
    narrative=('An inflatable greenhouse beside the first base on Mars. Four crew grow their '
               'fresh food and a quarter of their oxygen in it, and on hard days they step '
               'inside, out of their suits, to smell wet soil.'),
    enabled_by=[
        ('INFLATABLE HABITATS', 'Woven restraint layers and gas bladders already proven in orbit and on the ground.'),
        ('LED HORTICULTURE', 'Lamps tuned to each crop, from lettuce to dwarf wheat, at a known energy per gram.'),
        ('CLOSED LOOPS', 'Water, carbon dioxide and nutrients cycled between people and plants.'),
    ],
    real_basis='Inflatable habitats, LED horticulture and closed-loop life support.',
    required_breakthroughs='Pressurised membranes that last for years on Mars, and farmable soil made from regolith.',
    view_A='INFLATABLE MARTIAN GREENHOUSE',
    view_B='GROW RACK', view_B_note='FOUR TIERS / LED BARS / DRIP MANIFOLD / PUMP',
    view_C='AIRLOCK', view_C_note='PRESSURE DOOR / EQUALISATION VALVE / BENCH',
    service_year='2044',
    sources=['https://www.nasa.gov/missions/station/iss-research/veggie/', 'https://ntrs.nasa.gov/citations/20100040573'],
    source_scope='Real basis only: plant growth units on the ISS (Veggie), inflatable module tests, bioregenerative life-support studies. The greenhouse, crew and all figures are an original concept.',
)

DOSSIER = dict(
    kind='harvest',
    fact=('The crops take the crew\'s carbon dioxide and give back oxygen, clean water '
          'and food. The greenhouse is part of life support, not a garden beside it.'),
    rows=[('GROWING AREA', '42 m² / RACKS AND DEEP BEDS'),
          ('CABIN AIR', '50 kPa / 30 % OXYGEN'),
          ('FRESH FOOD', '4.5 kg A DAY / 10 % OF CALORIES'),
          ('OXYGEN RETURNED', 'A QUARTER OF THE CREW\'S NEED')],
    note='SOL 212: THE FIRST TOMATO, CUT INTO FOUR.',
    left=('PEOPLE AND PLANTS, ONE LOOP', 'DECLARED DAILY FLOWS / CREW OF FOUR / 42 m² OF CROPS',
          'The base supplies the rest of the oxygen and food; the loop shares the load.'),
    right=('THE WALL, LAYER BY LAYER', 'MEMBRANE SECTION / DECLARED LAYERS / NOT TO SCALE',
           'The net carries the pressure; the clear layers let daylight reach the leaves.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    from century.extension_editorial import capsule
    if side == 'left':
        # Three stations and the declared flows between them.
        bx = [(x + 8, 'CREW', '4 PEOPLE'), (x + 170, 'CROPS', '42 m²'), (x + 330, 'CONDENSER', 'WATER')]
        by = y + 40; bw = 96; bh = 40
        for xx, a, b in bx:
            capsule(s, xx, by, bw, bh, 9, WHITE, .75)
            tx(s, a, xx + bw / 2, by + 17, 6.8, .9, align='c')
            tx(s, b, xx + bw / 2, by + 31, 6.4, .6, align='c')
        c0, c1, c2 = bx[0][0] + bw, bx[1][0], bx[1][0] + bw
        arrow(s, (c0 + 4, by + 10), (c1 - 4, by + 10), WHITE)
        tx(s, 'CO₂ 1.2 kg', (c0 + c1) / 2, by + 3, 6.4, .8, align='c')
        arrow(s, (c1 - 4, by + 30), (c0 + 4, by + 30), ARC)
        tx(s, 'O₂ 0.84 kg', (c0 + c1) / 2, by + 50, 6.4, .85, align='c', color=ARC)
        # Food goes back under the boxes.
        s.poly([(bx[1][0] + bw / 2, by + bh + 4), (bx[1][0] + bw / 2, by + bh + 26), (bx[0][0] + bw / 2, by + bh + 26)], .8, .8, close=False, color=GOLD)
        arrow(s, (bx[0][0] + bw / 2, by + bh + 26), (bx[0][0] + bw / 2, by + bh + 5), GOLD)
        tx(s, 'FOOD 4.5 kg FRESH', bx[0][0] + bw / 2 + 10, by + bh + 38, 6.4, .85, color=GOLD)
        # Transpired water: out to the condenser, back as irrigation.
        arrow(s, (c2 + 4, by + 10), (bx[2][0] - 4, by + 10), WHITE)
        arrow(s, (bx[2][0] - 4, by + 30), (c2 + 4, by + 30), WHITE)
        tx(s, 'VAPOUR', (c2 + bx[2][0]) / 2, by + 3, 6.2, .7, align='c')
        tx(s, '140 L', (c2 + bx[2][0]) / 2, by + 50, 6.4, .8, align='c')
        tx(s, 'PER DAY', x + 8, y + 12, 6.2, .55)
    else:
        layers = [('DUST-SHEDDING SKIN', .8, 5, None),
                  ('ABRASION AND UV LAYER', .5, 7, None),
                  ('WEBBING RESTRAINT NET', .9, 12, 'net'),
                  ('CLEAR INSULATING GAP', .3, 12, None),
                  ('GAS BLADDER, TWO PLIES', .85, 8, 'accent'),
                  ('INNER LINER', .5, 5, None)]
        x0 = x + 30; x1 = x + 210; yy = y + 14
        tx(s, 'OUTSIDE 0.6 kPa', x0, yy - 4, 6.4, .6)
        yy += 4
        for i, (name, a, h, kind) in enumerate(layers):
            s.ln(x0, yy, x1, yy, a * .7, .6)
            if kind == 'net':
                for k in range(0, 180, 14):
                    s.ln(x0 + k, yy + h, x0 + k + 7, yy, .45, .5)
                    s.ln(x0 + k + 7, yy, x0 + k + 14, yy + h, .45, .5)
            if kind == 'accent':
                s.ln(x0, yy + h / 2, x1, yy + h / 2, .7, .6, color=ARC)
            s.ln(x1, yy + h / 2, x1 + 14, yy + h / 2, .3, .5)
            tx(s, name, x1 + 20, yy + h / 2 + 3, 6.4, .8 if kind else .65, color=ARC if kind == 'accent' else WHITE)
            yy += h + 7
        s.ln(x0, yy, x1, yy, .5, .6)
        s.ln(x1, yy, x1 + 14, yy, .3, .5)
        tx(s, 'INSIDE 50 kPa', x1 + 20, yy + 3, 6.4, .75)
        for k in (60, 120, 180):
            arrow(s, (x0 + k - 30, yy + 10), (x0 + k - 30, yy - 22), GOLD)
