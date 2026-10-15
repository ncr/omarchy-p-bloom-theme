"""b13 GREEN FORGE: text, field notes and side diagrams.

Narrative numbers, kept consistent:
Ideal reduction  Fe2O3 + 3 H2 -> 2 Fe + 3 H2O, per tonne of iron:
  Fe2O3 = 1 000 x 159.7 / 111.7 = 1 430 kg; H2 = 1.5 x 17 905 mol x 2.016 g
  = 54 kg; H2O = 1.5 x 17 905 x 18.02 g = 484 kg; 1 430 + 54 = 1 000 + 484.
Practical: ~57 kg H2 per tonne of iron (excess gas is recycled), 50 kWh per
kg at the electrolyser -> 2.85 MWh; gas heater and compression ~0.15 MWh;
arc furnace ~0.55 MWh per tonne of liquid steel; total 3.55 MWh/t.
Mill: 1.0 Mt of steel a year ~ 1.0 Mt of iron at 8 000 h -> 125 t/h.
Hydrogen: 125 t/h x 57 kg = 7.1 t/h x 50 kWh/kg = 356 MW -> 360 MW of
electrolysers running on wind and hydropower, spheres buffer the lulls.
"""

ENTRY = dict(
    id='b13', series='B13', number=213, slug='green-forge', title='GREEN FORGE',
    domain='steelmaking', category='serious', model='GF-1', palette='emerald', seed=260113,
    purpose='HYDROGEN STEEL FURNACE',
    narrative=('Makes steel from iron ore pellets with hydrogen split from water by northern wind '
               'and river power. The furnace crews of the old coal works run it; the only plume '
               'over the town is water vapour.'),
    enabled_by=[
        ('DIRECT REDUCTION', 'Shaft furnaces that already reduce pellets with natural gas can run on hydrogen.'),
        ('ARC MELTING', 'Electric arc furnaces that melt sponge iron and scrap on electricity.'),
        ('LARGE ELECTROLYSERS', 'Alkaline and PEM stacks built by the hundred megawatts, fed by wind and hydropower.'),
    ],
    real_basis='Hydrogen direct reduction, electric arc furnaces and large electrolysers.',
    required_breakthroughs='Cheap, abundant clean hydrogen at steel-mill scale.',
    view_A='HYDROGEN DIRECT-REDUCTION PLANT',
    view_B='SHAFT FURNACE', view_B_note='SHELL CUT AWAY / BURDEN / BUSTLE MAIN / TUYERES',
    view_C='ELECTROLYSER STACK', view_C_note='CELLS / END PLATES / TIE RODS / H₂ AND O₂ MANIFOLDS',
    service_year='2031',
    sources=['https://www.midrex.com/technology/midrex-process/midrex-h2/',
             'https://www.iea.org/reports/iron-and-steel-technology-roadmap'],
    source_scope='Real basis only: hydrogen direct reduction, electric arc steelmaking and industrial electrolysis. The plant, its layout and every figure are an original concept.',
)

DOSSIER = dict(
    kind='melt shop',
    fact=('Coke never enters the shaft; the arc furnace still uses a little carbon for its '
          'electrodes and slag.'),
    rows=[('STEEL', '1 Mt A YEAR / 8 000 h RUNNING'),
          ('REDUCTION SHAFT', '7 m ACROSS / TOP AT 47 m'),
          ('HYDROGEN', '7.1 t AN HOUR'),
          ('ELECTROLYSERS', '360 MW / 50 kWh PER kg OF H₂')],
    note='THE NIGHT SHIFT STILL CALLS IT THE COAL WORKS.',
    left=('THE OXYGEN LEAVES AS WATER', 'IDEAL MASS BALANCE / PER TONNE OF IRON / PURE OXIDE',
          'Fe₂O₃ + 3 H₂ → 2 Fe + 3 H₂O; the plant adds ~3 kg of excess hydrogen, recycled.'),
    right=('FROM WIND TO STEEL', 'ELECTRICITY PER TONNE OF LIQUID STEEL / DESIGN VALUES',
           'Most of the energy goes into splitting water; melting is the smaller share.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow

    def cell(cx, cy, top, bottom, col=WHITE, ww=86):
        s.rect(cx - ww / 2, cy - 18, ww, 36, .7, .65, color=col)
        # Two lines, cap-centred about the middle of the box.
        s.text_mid(top, cx, cy - 7.5, 7, .08, .88, align='c', color=col)
        s.text_mid(bottom, cx, cy + 7.5, 6.4, .08, .7, align='c')
    if side == 'left':
        cy = y + 44
        cell(x + 50, cy, 'Fe₂O₃', '1 430 kg')
        s.text_mid('+', x + 103, cy, 9, .08, .8, align='c')
        cell(x + 156, cy, 'H₂', '54 kg', ARC)
        arrow(s, (x + 204, cy), (x + 236, cy), WHITE)
        cell(x + 286, cy, 'Fe', '1 000 kg', GOLD)
        s.text_mid('+', x + 338, cy, 9, .08, .8, align='c')
        cell(x + 390, cy, 'H₂O', '484 kg', ARC)
        # Balance bar: both sides 1 484 kg.
        yy = y + 102
        s.ln(x + 7, yy, x + 199, yy, .5, .6); s.ln(x + 243, yy, x + 433, yy, .5, .6)
        for xx in (x + 7, x + 199, x + 243, x + 433):
            s.ln(xx, yy - 4, xx, yy + 4, .5, .6)
        tx(s, 'IN  1 484 kg', x + 103, yy + 16, 6.6, .75, align='c')
        tx(s, 'OUT  1 484 kg', x + 338, yy + 16, 6.6, .75, align='c')
    else:
        stages = [('ELECTROLYSIS', 2.85, ARC, '57 kg H2'), ('HEAT + GAS', .15, WHITE, ''), ('ARC FURNACE', .55, GOLD, '1 t STEEL')]
        total = sum(v for _, v, _, _ in stages)
        bx = x; bw = 400; yy = y + 30
        tx(s, 'ELECTRICITY 3.55 MWh', bx, yy - 12, 6.8, .82)
        xx = bx
        for name, v, col, out in stages:
            ww = bw * v / total
            s.rect(xx, yy, ww, 18, .8, .7, fill=.14, color=col)
            xx += ww
        e_w = bw * 2.85 / total; h_w = bw * .15 / total
        tx(s, 'ELECTROLYSIS 2.85 MWh', bx, yy + 36, 6.5, .82, color=ARC)
        tx(s, '57 kg OF HYDROGEN', bx, yy + 50, 6.2, .62)
        hx = bx + e_w + h_w / 2
        s.ln(hx, yy - 7, hx, yy - 1, .35, .5)
        tx(s, 'HEAT + GAS 0.15 MWh', hx, yy - 12, 6.4, .75, align='c')
        tx(s, 'ARC FURNACE 0.55 MWh', bx + bw, yy + 36, 6.5, .82, align='r', color=GOLD)
        tx(s, 'WATER + WIND  →  HYDROGEN  →  SPONGE IRON  →  STEEL', bx, yy + 98, 6.4, .66)
