"""b19 SKY WHALE: text, field notes and side diagrams.

Numbers are narrative and kept consistent with the model notes:
- Hull 120 m x 27 m, a body of revolution: integrating pi r(x)^2 over the
  model's profile gives about 38 000 m3; gas cells hold 36 000 m3 of helium.
- Gross lift ~1.0 kg per m3 at sea level -> 36 t. Budget (declared):
  hull and frames 11.0 t, envelope and cells 5.0, solar skin 2.0,
  motors and props 2.4, batteries 3.6, crew and systems 1.5 = 25.5 t empty;
  payload 8.0 t; reserve and water ballast 2.5 t. Total 36.0 t.
- Cruise 70 km/h: drag ~7.6 kN -> ~150 kW at the props, ~210 kW electric.
  Solar skin 2 400 m2 x 200 W/m2 = 480 kW peak, ~250 kW through a clear
  day; batteries 4 MWh carry the evening legs.
- Delivery loop (declared): Bissau base -> Bubaque -> Orango -> Uno ->
  Caravela -> base: 390 km at 70 km/h = 5 h 35 min flying, plus four
  hovers of about 25 min = about 7 h 15 min, a daylight round.
- Winch: 40 m of cable; the keel hovers 26 m above the terrace; one tonne a lift, lowering at
  0.5 m/s = 1 min.
- Holding position: four 90 kW tilting ducted props hold station in a
  30 km/h wind.
"""

ENTRY = dict(
    id='b19', series='B19', number=219, slug='sky-whale', title='SKY WHALE',
    domain='medical logistics', category='serious', model='SW-2', palette='saffron', seed=260119,
    purpose='MEDICAL CARGO AIRSHIP',
    narrative=('Carries vaccines, insulin and spare parts to the Bijagos islands, where there is no '
               'runway. It stops overhead, holds still in the wind and winches each crate down to '
               'the nurse waiting on the terrace.'),
    enabled_by=[
        ('RIGID AIRSHIPS', 'Light carbon frames and helium cells, as in the airships flying again today.'),
        ('SOLAR SKIN', 'Thin-film panels on the upper hull that fly the ship through the day.'),
        ('VECTORED THRUST', 'Tilting ducted props that hold the ship still while the crate goes down.'),
    ],
    real_basis='Modern rigid airships, helium lift, solar-electric propulsion.',
    required_breakthroughs='Safe all-weather ground handling without large ground crews.',
    view_A='ISLAND DELIVERY IN HOVER',
    view_B='CARGO WINCH', view_B_note='GONDOLA SHELL OMITTED / DRUM / LEVEL WIND / BRAKE / HOOK',
    view_C='VECTORING PROP', view_C_note='DUCT / FIVE BLADES / STATORS / TILT BEARING / STRUT',
    service_year='2034',
    sources=['https://www.hybridairvehicles.com/', 'https://doi.org/10.2514/1.C034380'],
    source_scope='Real basis only: helium lift, rigid airship structure, solar-electric propulsion and vectored-thrust station keeping. The ship, route and all figures are an original concept.',
)

DOSSIER = dict(
    kind='delivery round',
    fact=('The ship never lands. It holds still overhead while the winch lowers each crate, '
          'so an island needs a clear terrace and a person to sign, not a runway.'),
    rows=[('HULL', '120 m / 36 000 m³ HELIUM'),
          ('PAYLOAD', '8 t / ONE TONNE A LIFT'),
          ('CRUISE', '70 km/h ON SUNLIGHT'),
          ('ROUND', '4 ISLANDS / 390 km / 7 h')],
    note='THE CLINIC ON ORANGO HAS NOT RUN OUT OF INSULIN SINCE MARCH.',
    left=('WHAT THE HELIUM CARRIES', 'DECLARED MASS BUDGET / 36 t GROSS LIFT',
          'About 1.0 kg of lift per m³ of helium at sea level; less on hot afternoons.'),
    right=('ONE DAYLIGHT ROUND', 'ILLUSTRATIVE ROUTE / FLYING TIME + HOVERS',
           '390 km at 70 km/h plus four hovers of about 25 minutes: home before dark.'),
)

BUDGET = [('HULL', 11.0), ('ENVELOPE', 5.0), ('SOLAR', 2.0), ('PROPS', 2.4), ('BATTERY', 3.6),
          ('CREW', 1.5), ('PAYLOAD', 8.0), ('RESERVE', 2.5)]


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        x0 = x + 8; x1 = x + w - 8; top = y + 36; h = 20
        total = sum(v for _, v in BUDGET)
        X = lambda t: x0 + (x1 - x0) * t / total
        t = 0
        for i, (lab, v) in enumerate(BUDGET):
            col = GOLD if lab == 'PAYLOAD' else (ARC if lab == 'RESERVE' else WHITE)
            a = .85 if lab in ('PAYLOAD', 'RESERVE') else .55
            s.rect(X(t), top, X(t + v) - X(t), h, a, .7, color=col)
            if lab == 'PAYLOAD':
                for k in range(1, 9):
                    s.ln(X(t) + (X(t + v) - X(t)) * k / 9, top + 3, X(t) + (X(t + v) - X(t)) * k / 9, top + h - 3, .35, .5, color=GOLD)
            yy = top - 8 if i % 2 == 0 else top + h + 16
            tx(s, lab, (X(t) + X(t + v)) / 2, yy, 6.2, .72, align='c')
            tx(s, f'{v:g}', (X(t) + X(t + v)) / 2, top + h / 2 + 3, 6.2, .8, align='c')
            t += v
        # Brackets: empty ship vs what it can carry.
        empty = sum(v for lab, v in BUDGET[:6])
        by = top + h + 40
        s.poly([(X(0), by - 5), (X(0), by), (X(empty), by), (X(empty), by - 5)], .5, .6, close=False)
        tx(s, 'EMPTY SHIP 25.5 t', (X(0) + X(empty)) / 2, by + 16, 6.6, .8, align='c')
        s.poly([(X(empty), by - 5), (X(empty), by), (X(total), by), (X(total), by - 5)], .7, .6, close=False, color=GOLD)
        tx(s, 'CARGO + RESERVE 10.5 t', (X(empty) + X(total)) / 2, by + 16, 6.6, .85, align='c', color=GOLD)
    else:
        # A schematic loop of islands: stop circles, legs with flying minutes.
        pts = [('BASE', x + 30, y + 92), ('BUBAQUE', x + 128, y + 30), ('ORANGO', x + 238, y + 16),
               ('UNO', x + 336, y + 50), ('CARAVELA', x + 300, y + 112)]
        legs = [(0, 1, '1 h 05', 1), (1, 2, '0 h 55', 1), (2, 3, '1 h 00', 1), (3, 4, '0 h 45', -1.6), (4, 0, '1 h 50', 1)]
        for a, b, lab, sd in legs:
            (_, ax, ay), (_, bx, by) = pts[a], pts[b]
            d = ((bx - ax) ** 2 + (by - ay) ** 2) ** .5
            ux, uy = (bx - ax) / d, (by - ay) / d
            arrow(s, (ax + ux * 10, ay + uy * 10), (bx - ux * 10, by - uy * 10), ARC)
            mx, my = (ax + bx) / 2, (ay + by) / 2
            tx(s, lab, mx - uy * 11 * sd, my + ux * 11 * sd + 3, 6.2, .7, align='c')
        for i, (name, px, py) in enumerate(pts):
            if i == 0:
                s.rect(px - 6, py - 6, 12, 12, .9, .8)
            else:
                s.circ(px, py, 6, .9, .8, color=GOLD)
                s.circ(px, py, 2, .9, .6, color=GOLD)
            tx(s, name, px, py + 20 if py > y + 60 else py - 11, 6.4, .8, align='c')
        tx(s, '25 MIN HOVER AT EACH STOP', x + w - 4, y + 2, 6.2, .6, align='r')
