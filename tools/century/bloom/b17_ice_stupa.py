"""b17 ICE STUPA: text, field notes and side diagrams.

Numbers are narrative, kept consistent with the model notes:
Cone 30 m tall, 18 m across: V = 1/3 pi 9^2 30 = 2 545 m3 of ice
  x 0.917 -> about 2 330 t, "about 2.3 million litres" of water.
Winter feed: 2 L/s, sprayed through 12 cold hours a night for 90 nights
  = 2 x 43 200 x 90 = 7.8 million L; about a third freezes onto the cone
  (7.8 x 0.3 = 2.3 million L), the rest runs back to the stream.
Head: intake 60 m above the valve pit -> P = rho g h = 1 000 x 9.81 x 60
  = 5.9 bar at the pit; at the nozzle, 30 m higher, 30 m -> 2.9 bar.
Spring melt over 45 days in April and May: 2.3 million / 45 = 51 000 L a
  day; at 5 mm of water a day that waters 51 / 0.005 = 10 200 m2, ~1 ha.
"""

ENTRY = dict(
    id='b17', series='B17', number=217, slug='ice-stupa', title='ICE STUPA',
    domain='water', category='serious', model='IS-2', palette='teal', seed=260117,
    purpose='ARTIFICIAL GLACIER BUILDER',
    narrative=('On winter nights it sprays stream water into the cold air, and a cone of ice '
               'grows 30 m tall. In spring it melts slowly and waters a mountain village\'s '
               'barley while the streams above are still frozen.'),
    enabled_by=[
        ('ICE STUPAS', 'Ladakh villages have built them since 2014 with pipes and local labour.'),
        ('GRAVITY HEAD', 'An intake 60 m up the slope gives the fountain its pressure; no pump.'),
        ('FREEZE CONTROL', 'A valve that drains the riser whenever the spray stops.'),
    ],
    real_basis='Ladakh ice stupas, gravity-fed pipes, spray freezing.',
    required_breakthroughs='Placement and shape control that keeps the cone melting exactly when crops need it.',
    view_A='WINTER ICE CONE ABOVE THE FIELDS',
    view_B='SPRAY FOUNTAIN', view_B_note='FREEZE VALVE / SWIVEL NOZZLES / DEFLECTOR',
    view_C='FEED PIPE', view_C_note='VALVE PIT / NEAR WALLS OMITTED / GAUGE / DRAIN-BACK',
    service_year='2029',
    sources=['https://icestupa.org/', 'https://doi.org/10.3389/feart.2021.736478'],
    source_scope='Real basis only: Ladakh ice-stupa projects and published studies of their melt. The machine, the village and every figure are an original concept.',
)

DOSSIER = dict(
    kind='winter to spring',
    fact=('Water sprayed into air at minus fifteen freezes as it falls. A cone has little '
          'surface for its volume, so the ice keeps into spring.'),
    rows=[('HEIGHT', '30 m / 18 m ACROSS'),
          ('ICE STORED', 'ABOUT 2.3 MILLION L'),
          ('HEAD AT THE PIT', '60 m / 5.9 bar'),
          ('SPRING MELT', '51 000 L A DAY / 45 DAYS')],
    note='ON 20 APRIL TSERING SOWED HER BARLEY. THE STREAM ABOVE WAS STILL ICE.',
    left=('THE MOUNTAIN IS THE PUMP', 'HYDROSTATIC HEAD / P = RHO g h / NO FLOW LOSSES',
          'Pressure falls by 0.98 bar for every 10 m the water climbs; 2.9 bar is left for the spray.'),
    right=('WATER HELD FROM WINTER TO SPRING', 'ILLUSTRATIVE YEAR / DECLARED SHAPES, NOT A RECORD',
           'The cone gives its water in April and May, before the glacier melt reaches the stream.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        # Elevation schematic: intake, slope, pit, riser; pressure bars.
        gx, gy, sc = x + 30, y + 118, 1.7        # 1 m = 1.7 units vertically
        def zy(m): return gy - m * sc
        s.poly([(gx, zy(60)), (gx + 70, zy(52)), (gx + 150, zy(26)), (gx + 205, zy(0)), (gx + 250, zy(0))], .5, .6, close=False)
        s.poly([(gx + 205, zy(0)), (gx + 228, zy(0)), (gx + 228, zy(30))], .8, .8, close=False, color=GOLD)
        s.poly([(gx + 216, zy(0)), (gx + 228, zy(30)), (gx + 240, zy(0))], .35, .5, close=False)
        s.circ(gx, zy(60), 3, .9, .7, color=ARC)
        s.circ(gx + 205, zy(0), 3, .9, .7, color=ARC)
        s.circ(gx + 228, zy(30), 3, .9, .7, color=ARC)
        tx(s, 'INTAKE 60 m', gx + 8, zy(60) - 6, 6.4, .75)
        tx(s, 'PIT 0 m', gx + 150, zy(0) + 14, 6.4, .75)
        tx(s, 'NOZZLE 30 m', gx + 236, zy(30) - 4, 6.4, .75)
        # Pressure bars on the right: 5.9 and 3.4 bar.
        bx = x + 330
        for k, (label, bar) in enumerate((('PIT', 5.9), ('NOZZLE', 2.9))):
            yy = y + 30 + k * 40
            tx(s, label, bx, yy - 4, 6.4, .7)
            s.ln(bx, yy + 6, bx + 100, yy + 6, .18, 3)
            s.ln(bx, yy + 6, bx + 100 * bar / 6, yy + 6, .85, 3, color=ARC if k else GOLD)
            tx(s, f'{bar} bar', bx + 104, yy + 9, 6.4, .8)
    else:
        px, py, pw, ph = x + 40, y + 8, 330, 96
        months = ['NOV', 'DEC', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL']
        s.poly([(px, py), (px, py + ph), (px + pw, py + ph)], .5, .6, close=False)
        for i, m in enumerate(months):
            xx = px + pw * (i + .5) / 9
            tx(s, m, xx, py + ph + 14, 6.4, .62, align='c')
        # Shade April-May: the cone waters the fields.
        s.rect(px + pw * 5 / 9, py, pw * 2 / 9, ph, .2, .5, dash=[3, 3])
        tx(s, 'SOWING', px + pw * 6 / 9, py - 5, 6.4, .72, align='c')
        # Ice held (declared): grows Nov-Feb, holds in March, melts Apr-May.
        def ice(t):
            if t < 4: return t / 4
            if t < 5: return 1
            if t < 7: return 1 - (t - 5) / 2
            return 0
        # Stream flow (declared): low under ice until June's glacier melt.
        def flow(t):
            return .12 + .78 * max(0, min(1, (t - 6.8) / 1.6)) ** 1.5
        s.poly([(px + pw * t / 9, py + ph * (1 - .95 * ice(t))) for t in [9 * k / 90 for k in range(91)]], .85, .85, close=False, color=ARC)
        s.poly([(px + pw * t / 9, py + ph * (1 - flow(t))) for t in [9 * k / 90 for k in range(91)]], .7, .7, close=False, color=GOLD, dash=[4, 3])
        tx(s, 'ICE IN THE CONE', px + pw * 1.2 / 9, py + 18, 6.4, .8, color=ARC)
        tx(s, 'STREAM', px + pw * 8.95 / 9, py + 6, 6.4, .8, color=GOLD, align='r')
