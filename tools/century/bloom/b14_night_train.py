"""b14 NIGHT TRAIN: text, field notes and side diagrams.

Numbers are narrative and kept consistent:
- Route Warsaw - Poznan - Berlin - Hanover - Amsterdam, about 1 220 km.
  Timetable (declared): Warsaw 20:10, Poznan 22:35 (300 km), Berlin 01:10
  (570 km), Hanover 03:40 (855 km), Amsterdam 07:50 (1 220 km).
  11 h 40 min, average 105 km/h; top speed 200 km/h where the line allows.
- Carriage: 10 compartments x 2 berths = 20 berths. Train of 12 carriages
  plus seats: about 300 travellers.
- Energy per traveller (illustrative): train 22 kWh per km x 1 220 km =
  26 840 kWh / 300 = 89 kWh of electricity. Flight of 1 100 km at 2.4 L of
  jet fuel per 100 passenger-km = 26.4 L x 9.8 kWh/L = 259 kWh of fuel.
- Supply systems on this route: 3 kV DC (Poland), 15 kV AC (Germany),
  1.5 kV DC (Netherlands).
"""

ENTRY = dict(
    id='b14', series='B14', number=214, slug='night-train', title='NIGHT TRAIN',
    domain='rail', category='serious', model='NT-10', palette='violet', seed=260114, view_A_fit=(740, 720),
    purpose='ELECTRIC SLEEPER CARRIAGE',
    narrative=('You fall asleep in Warsaw and wake up in Amsterdam, rested, having crossed three '
               'countries on electric power and without an airport. Each carriage has ten '
               'compartments and its own motors.'),
    enabled_by=[
        ('MODERN SLEEPERS', 'Night services with private compartments, washbasins and well-sprung carriages.'),
        ('ELECTRIFIED RAIL', 'Multi-system traction that runs under each country\'s overhead supply.'),
        ('ACTIVE SUSPENSION', 'Controlled air springs and dampers that keep a berth still over points.'),
    ],
    real_basis='Modern sleeper services, electrified rail, active suspension.',
    required_breakthroughs='Quiet, fast, affordable night networks across borders.',
    view_A='CAB-END SLEEPER CARRIAGE',
    view_B='SLEEPING COMPARTMENT', view_B_note='TWO BERTHS / LADDER / BASIN / LUGGAGE RACK',
    view_C='BOGIE', view_C_note='WHEELSETS / COIL AND AIR SPRINGS / DISCS / MOTOR',
    service_year='2029',
    sources=['https://www.nightjet.com/en/', 'https://www.era.europa.eu/'],
    source_scope='Real basis only: current European night services, multi-system electric traction, active secondary suspension. The carriage, timetable and energy figures are an original concept.',
)

DOSSIER = dict(
    kind='overnight',
    fact=('The train is timed for sleep, not speed: it runs gently through the small '
          'hours and arrives in time for breakfast.'),
    rows=[('BERTHS', '20 PER CARRIAGE / 10 COMPARTMENTS'),
          ('OVERNIGHT', '1 220 km / 11 h 40 min'),
          ('SUPPLY', '3 kV DC / 15 kV AC / 1.5 kV DC'),
          ('ENERGY', '89 kWh PER TRAVELLER')],
    note='SHE FELL ASLEEP IN WARSAW AND WOKE UP TO CANALS.',
    left=('TIMED FOR SLEEP', 'DECLARED TIMETABLE / DISTANCE AGAINST TIME',
          'The line flattens after midnight: slower running, longer stops, a quieter ride.'),
    right=('ENERGY FOR ONE TRAVELLER', 'ILLUSTRATIVE / WARSAW - AMSTERDAM / STATED ASSUMPTIONS',
           'Train: 22 kWh per km, 300 travellers. Flight: 2.4 L of fuel per 100 passenger-km.'),
)

STOPS = [('WARSAW', 20 + 10 / 60, 0), ('POZNAN', 22 + 35 / 60, 300), ('BERLIN', 25 + 10 / 60, 570),
         ('HANOVER', 27 + 40 / 60, 855), ('AMSTERDAM', 31 + 50 / 60, 1220)]


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        x0 = x + 92; x1 = x + w - 6; y0 = y + 6; y1 = y + 104
        t0, t1 = 20, 32
        X = lambda h: x0 + (x1 - x0) * (h - t0) / (t1 - t0)
        Y = lambda km: y1 - (y1 - y0) * km / 1220
        # Lights-low window 23:00-06:30.
        for k in range(0, int(X(30.5) - X(23)), 6):
            s.ln(X(23) + k, y0, X(23) + k, y1, .09, .5)
        tx(s, 'LIGHTS LOW', (X(23) + X(30.5)) / 2, y0 - 4, 6.2, .6, align='c')
        s.poly([(x0, y0), (x0, y1), (x1, y1)], .45, .55, close=False)
        pts = []
        for i, (name, h, km) in enumerate(STOPS):
            dwell = 0 if i in (0, len(STOPS) - 1) else 8 / 60
            pts += [(X(h), Y(km)), (X(h + dwell), Y(km))]
            s.dot(X(h), Y(km), 2.2, .9, color=ARC)
            tx(s, name, x0 - 8, Y(km) + 3, 6.2, .72, align='r')
            s.ln(x0, Y(km), X(h), Y(km), .12, .4)
        s.poly(pts, .9, .85, close=False, color=ARC)
        for h, lab in ((20, '20:00'), (24, '00:00'), (28, '04:00'), (32, '08:00')):
            s.ln(X(h), y1, X(h), y1 + 4, .45, .5)
            tx(s, lab, X(h), y1 + 16, 6.4, .66, align='c')
    else:
        # Two horizontal bars on one scale, values and energy carrier stated.
        bx = x + 120; bw = w - 175; scale = bw / 280
        rows = [('TRAIN', 89, 'ELECTRICITY', ARC), ('FLIGHT', 259, 'JET FUEL', GOLD)]
        for i, (lab, v, carrier, col) in enumerate(rows):
            yy = y + 22 + i * 44
            tx(s, lab, x, yy + 4, 7, .8)
            tx(s, carrier, x, yy + 18, 6.2, .55)
            s.ln(bx, yy, bx + bw, yy, .14, 5)
            s.ln(bx, yy, bx + v * scale, yy, .88, 5, color=col)
            tx(s, f'{v} kWh', bx + bw + 8, yy + 3, 6.8, .85)
        for v in (0, 100, 200):
            s.ln(bx + v * scale, y + 100, bx + v * scale, y + 105, .45, .5)
            tx(s, str(v), bx + v * scale, y + 118, 6.4, .62, align='c')
        tx(s, 'kWh', bx + bw, y + 118, 6.4, .62, align='r')
