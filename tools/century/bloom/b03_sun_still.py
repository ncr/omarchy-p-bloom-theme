"""b03 SUN STILL: text, field notes and side diagrams.

Numbers are narrative, kept consistent with the model notes:
Town of 4 000 x 120 L a day = 480 m3 of fresh water a day.
Zero liquid discharge: 500 t seawater a day (35 g salts per kg)
  = 480 t fresh water + 17.5 t salts + 2.5 t moisture left in wet product.
Salts 17.5 t: sodium chloride 13.6, magnesium salts 2.7, gypsum 0.6,
  potassium salts 0.4, other 0.2 (seawater proportions, rounded).
Heat: 14 effects, 70 -> 36 C, gained output ratio 12 -> 2 300 kJ/kg / 12
  = 0.19 MJ/kg x 480 000 kg = 92 GJ = 25.6 MWh of heat a day.
Field: 6.5 kWh/m2 a day direct sun x 0.65 field efficiency = 4.2 kWh/m2
  -> 6 100 m2 of mirror = 380 heliostats of 16 m2. A 16 h hot-water store
  keeps the stack running through the night.
"""

ENTRY = dict(
    id='b03', series='B03', number=203, slug='sun-still', title='SUN STILL',
    domain='water', category='serious', model='SS-14', palette='saffron', seed=260103,
    purpose='SOLAR DESALINATION TOWER',
    narrative=('Gives a coastal town of 4 000 its drinking water from the sea using only '
               'sunlight, and bags the salts as table salt, magnesium and gypsum instead '
               'of returning a brine plume to the bay.'),
    enabled_by=[
        ('DISTILLATION', 'Multi-effect stacks, as in coastal plants: each effect boils at a lower pressure than the one above.'),
        ('SOLAR THERMAL', 'Heliostat fields and tower receivers from concentrating solar power.'),
        ('MINERAL RECOVERY', 'Staged crystallisation that separates sodium, magnesium and calcium salts.'),
    ],
    real_basis='Multi-effect distillation, solar thermal collectors, mineral recovery from brine.',
    required_breakthroughs='Low-cost, scale-free evaporator surfaces that last many years in hot brine.',
    view_A='HELIOSTAT-FED DISTILLATION TOWER',
    view_B='EFFECT STACK', view_B_note='SHELL CUT AWAY / TUBE BUNDLES / SPRAY BARS / TRAYS',
    view_C='MIRROR ROW', view_C_note='TWO-AXIS DRIVES / CLEANING ROBOT',
    service_year='2036',
    sources=['https://www.iea-shc.org/', 'https://www.nrel.gov/csp/'],
    source_scope='Real basis only: multi-effect distillation, central-receiver solar thermal, brine mineral recovery. The tower, its output and every figure are an original concept.',
)

DOSSIER = dict(
    kind='still',
    fact=('The stack is widest at the bottom: colder vapour is thinner and needs more room. '
          'The tower stands 36 m to the top of the receiver crown.'),
    rows=[('FRESH WATER', '480 m³ A DAY / 120 L PER PERSON'),
          ('SEAWATER', '35 g OF SALTS PER kg'),
          ('DIRECT SUN', '6.5 kWh PER m² A DAY'),
          ('MIRROR FIELD', '6 100 m² / 25.6 MWh OF HEAT A DAY')],
    note='THE FIRST BAGS OF SALT WENT TO THE SCHOOL KITCHEN.',
    left=('ONE HEAT, FOURTEEN EFFECTS', 'MULTI-EFFECT CASCADE / DESIGN TEMPERATURES',
          'Vapour from each effect condenses in the tubes of the next and boils the brine there.'),
    right=('NOTHING GOES BACK AS BRINE', 'DAILY MASS BALANCE / t PER DAY / DESIGN VALUES',
           'Seawater 500 t = fresh water 480 t + salts 17.5 t + moisture in the bags 2.5 t.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        # Staircase of effects: 1, 2, 3 ... 14, each 2.6 C cooler than the last.
        # Each box reads "index  temperature" on one cap-centred line: the dim
        # effect number left, the temperature right, equal padding.
        shown = [1, 2, 3, None, 13, 14]
        temps = {k: f'{70 - (k - 1) * 34 / 13:.0f} °C' for k in shown if k}
        pad, gap = 5, 10
        nw = max(s.measure(str(k), 6.4, .08) for k in temps)
        bw = max(46, 2 * pad + nw + gap + max(s.measure(v, 6.4, .08) for v in temps.values()))
        bh, step = 20, bw + 11
        for i, k in enumerate(shown):
            bx = x + i * step; by = y + 8 + i * 16
            if k is None:
                for d in (-1, 0, 1):
                    s.dot(bx + bw / 2 + d * 9, by + bh / 2, 1.2, .7)
                continue
            s.rect(bx, by, bw, bh, .75, .7)
            s.text_mid(str(k), bx + pad, by + bh / 2, 6.4, .08, .45)
            s.text_mid(temps[k], bx + bw - pad, by + bh / 2, 6.4, .08, .8, align='r', color=GOLD if k == 1 else WHITE)
            if i + 1 < len(shown) and shown[i + 1]:
                arrow(s, (bx + bw, by + bh / 2), (bx + step, by + 16 + bh / 2 - 4), ARC)
        end = x + 5 * step + bw
        sx = x + bw / 2
        arrow(s, (sx, y - 12), (sx, y + 7), GOLD)
        s.text_mid('SUN HEAT', sx + 7, y - 3, 6.4, .08, .8, color=GOLD)
        s.text_mid('VAPOUR', x + step, y + 13, 6.2, .08, .7, color=ARC)
        tx(s, 'DISTILLATE', x, y + 122, 6.4, .7)
        s.ln(x, y + 110, end, y + 110, .5, .6)
        for i in range(6):
            if shown[i] is None:
                continue
            bx = x + i * step + bw / 2
            s.ln(bx, y + 8 + i * 16 + bh, bx, y + 110, .35, .5, dash=[2, 2])
        tx(s, 'GAINED OUTPUT RATIO 12', end, y + 122, 6.4, .8, align='r')
    else:
        # Stacked bar: 500 t seawater -> fresh water / salts / moisture, salts expanded.
        bx = x; bw = 400; scale = bw / 500.0
        by = y + 16
        s.rect(bx, by, bw, 14, .7, .7)
        tx(s, 'SEAWATER 500 t', bx, by - 6, 6.6, .85)
        by2 = y + 58
        parts = [('FRESH WATER', 480, ARC), ('SALTS', 17.5, GOLD), ('', 2.5, WHITE)]
        xx = bx
        for name, v, col in parts:
            ww = v * scale
            s.rect(xx, by2, ww, 14, .8, .7, color=col)
            xx += ww
        tx(s, 'FRESH WATER 480 t', bx, by2 - 6, 6.6, .85, color=ARC)
        arrow(s, (bx + bw / 2, by + 18), (bx + bw / 2, by2 - 12), WHITE)
        # Expanded salt breakdown (13.6 + 2.7 + 0.6 + 0.4 + 0.2 = 17.5 t).
        sx0 = bx + 480 * scale; ex0 = bx + 130; ew = 270
        s.ln(sx0, by2 + 14, ex0, y + 96, .35, .5, dash=[2, 2])
        s.ln(sx0 + 17.5 * scale, by2 + 14, ex0 + ew, y + 96, .35, .5, dash=[2, 2])
        salts = [('NaCl', 13.6), ('Mg', 2.7), ('GYPSUM', .6), ('K', .4), ('', .2)]
        xx = ex0
        for name, v in salts:
            ww = v / 17.5 * ew
            s.rect(xx, y + 96, ww, 12, .8, .65, color=GOLD)
            xx += ww
        if s.type_growth(6.2):
            # Enlarged type (composed profiles): one line from the left edge.
            tx(s, 'NaCl 13.6 / Mg 2.7 / GYPSUM 0.6 / K 0.4 / OTHER 0.2', bx, y + 122, 6.2, .8)
        else:
            tx(s, 'NaCl 13.6', ex0, y + 122, 6.4, .8)
            tx(s, 'Mg 2.7 / GYPSUM 0.6 / K 0.4 / OTHER 0.2', ex0 + ew, y + 122, 6.2, .7, align='r')
        s.text_mid('SALTS 17.5 t', ex0 - 8, y + 102, 6.6, .08, .85, align='r', color=GOLD)
