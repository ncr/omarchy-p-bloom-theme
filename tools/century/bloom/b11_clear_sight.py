"""b11 CLEAR SIGHT: text, field notes and side diagrams.

Numbers are narrative and kept consistent:
- Manual small-incision cataract surgery (MSICS) takes about 10 minutes;
  with cleaning and turnaround a slot is 12 minutes. One table, 08:00-12:00
  and 13:00-16:12 -> 4 h + 3.2 h = 7.2 h = 432 min / 12 = 36 eyes a day.
- A district visit lasts three weeks: 18 operating days x 36 = 648 eyes.
- Energy per day: air handler 1.5 kW x 10 h = 15 kWh, steam steriliser
  6 cycles x 1 kWh = 6 kWh, lights, microscope and cold store 3 kWh
  -> 24 kWh. Solar: roof 2.9 kWp + awning 2.4 kWp = 5.3 kWp x ~5 sun-hours
  = 26 kWh; 30 kWh battery bridges cloudy days.
- Lens power, SRK regression (illustrative): P = A - 2.5 L - 0.9 K with
  A = 118.4, L = 23.5 mm, K = 43.5 D -> P = 118.4 - 58.75 - 39.15 = 20.5 D.
"""

ENTRY = dict(
    id='b11', series='B11', number=211, slug='clear-sight', title='CLEAR SIGHT',
    domain='eye care', category='serious', model='CS-20', palette='copper', seed=260111,
    purpose='MOBILE CATARACT CLINIC',
    narrative=('A shipping-container operating room that restores sight in a single day. People '
               'walk in unable to see their grandchildren\'s faces and walk out able to; after three '
               'weeks the clinic moves to the next district.'),
    enabled_by=[
        ('SMALL-INCISION SURGERY', 'A ten-minute operation without stitches, at very low cost per eye.'),
        ('PORTABLE MICROSCOPY', 'Floor-stand surgical microscopes with LED light that pack for transport.'),
        ('CONTAINER CLINICS', 'Standard containers fitted as clean rooms, moved by any truck, train or ship.'),
    ],
    real_basis='Small-incision cataract surgery, portable surgical microscopes, container clinics.',
    required_breakthroughs='Sterile, fully self-contained operation for years in remote heat and dust.',
    view_A='FOLD-OUT CONTAINER EYE THEATRE',
    view_B='SURGICAL MICROSCOPE', view_B_note='FLOOR STAND / BALANCED BOOM / FOOT PEDAL',
    view_C='LENS BENCH', view_C_note='LENSES BY DIOPTRE / INJECTORS / STERILE CASSETTE',
    service_year='2030',
    sources=['https://www.who.int/news-room/fact-sheets/detail/blindness-and-visual-impairment',
             'https://doi.org/10.1016/j.ophtha.2006.10.019'],
    source_scope='Real basis only: cataract as a leading cause of blindness, MSICS outcomes, container clinics. The clinic, its layout and every figure are an original concept, not medical guidance.',
)

DOSSIER = dict(
    kind='district visit',
    fact=('Cataract is the most common cause of blindness and one of the most '
          'treatable. For most patients, the hard part is reaching a surgeon.'),
    rows=[('PER VISIT', '18 OPERATING DAYS / 648 EYES'),
          ('POWER', '5.3 kWp SOLAR / 30 kWh STORE'),
          ('DAILY LOAD', '24 kWh / AIR HANDLER 15 kWh'),
          ('STERILISER', '6 STEAM CYCLES A DAY')],
    note='SHE READ THE BUS NUMBER FROM ACROSS THE SQUARE.',
    left=('ONE TABLE, THIRTY-SIX EYES', 'OPERATING DAY / 12 MIN SLOTS / 08:00–16:12',
          'Ten minutes of surgery per slot; the rest is cleaning and the next patient settling in.'),
    right=('CHOOSING THE NEW LENS', 'EYE SECTION / SRK REGRESSION',
           'Measured eye length and corneal power give the lens; each box is set out the night before.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        # Time axis 07:30-16:30. Rows: biometry, surgery slots, recovery occupancy.
        x0 = x + 96; x1 = x + w - 8
        t0, t1 = 7.0, 16.5
        X = lambda h: x0 + (x1 - x0) * (h - t0) / (t1 - t0)
        slots = [8 + i * .2 for i in range(20)] + [13 + i * .2 for i in range(16)]
        # Row names cap-centred on their tracks (resting: the middle of its band).
        s.text_mid('MEASURE', x, y + 10, 6.6, .08, .76)
        s.text_mid('SURGERY', x, y + 42, 6.6, .08, .76)
        s.text_mid('RESTING', x, y + 79, 6.6, .08, .76)
        for yy in (y + 10, y + 42, y + 92):
            s.ln(x0, yy, x1, yy, .14, .4)
        for h in slots:
            # Biometry about an hour before surgery: one tick per patient.
            s.ln(X(h - 1), y + 4, X(h - 1), y + 16, .75, .6)
            s.poly([(X(h) + .6, y + 36), (X(h + 10 / 60), y + 36), (X(h + 10 / 60), y + 48), (X(h) + .6, y + 48)], .82, .55, close=True, color=ARC)
        # Patients resting after surgery (15 min to 75 min after the slot start):
        # a step curve computed from the same slots, maximum five at once.
        pts = []; unit = 5.2
        for k in range(0, 541):
            t = t0 + k / 60
            n = sum(1 for h in slots if h + .25 <= t < h + 1.25)
            pts.append((X(t), y + 92 - n * unit))
        s.poly(pts, .85, .75, close=False, color=GOLD)
        # The peak, named just under its plateau (clear of the surgery row above).
        s.text_mid('5 AT ONCE', X(10.7), y + 92 - 5 * unit + 9, 6.2, .08, .7, align='c')
        for h in (8, 10, 12, 14, 16):
            s.ln(X(h), y + 96, X(h), y + 101, .45, .5)
            tx(s, f'{h:02d}:00', X(h), y + 114, 6.4, .66, align='c')
        # LUNCH centred over the surgery row's gap, on the 36 EYES baseline.
        tx(s, 'LUNCH', (X(slots[19] + 10 / 60) + X(slots[20])) / 2, y + 29, 6.2, .6, align='c')
        tx(s, '36 EYES', x1, y + 29, 6.6, .85, align='r', color=ARC)
    else:
        # Eye section: cornea, anterior chamber, lens in its capsule, globe, retina.
        import math
        cx = x + 112; cy = y + 52; R = 46
        pts = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in range(28, 333, 4)]
        s.poly(pts, .7, .7, close=False)
        cor = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in (28, 332)]
        # Cornea: a steeper arc bulging to the right of the globe.
        c2 = [(cx + 35 + 24 * math.cos(math.radians(a)), cy + 26 * math.sin(math.radians(a)) * 1.02) for a in range(-62, 63, 4)]
        s.poly([cor[1]] + c2 + [cor[0]], .85, .75, close=False)
        # Replacement lens: optic and two haptics inside the capsular bag.
        lx = cx + 32
        s.poly([(lx + 7 * math.cos(math.radians(a)), cy + 15 * math.sin(math.radians(a))) for a in range(0, 361, 10)], .92, .8, close=True, color=ARC)
        for sgn in (-1, 1):
            s.poly([(lx, cy + sgn * 15), (lx - 3, cy + sgn * 22), (lx - 9, cy + sgn * 25)], .8, .6, close=False, color=ARC)
        # Axial length dimension: cornea to retina.
        s.ln(cx - R, cy + 58, cx + 64, cy + 58, .5, .55)
        for xx in (cx - R, cx + 64):
            s.ln(xx, cy + 53, xx, cy + 63, .5, .55)
        tx(s, 'L = 23.5 mm', cx + 9, cy + 76, 6.4, .75, align='c')
        tx(s, 'K = 43.5 D', cx + 64, cy - 36, 6.4, .75)
        s.text_mid('RETINA', cx - R - 8, cy, 6.2, .08, .6, align='r')
        # Formula block.
        fx = x + 262
        tx(s, 'P = A - 2.5 L - 0.9 K', fx, y + 30, 7, .85)
        tx(s, 'A = 118.4 (LENS CONSTANT)', fx, y + 52, 6.4, .66)
        tx(s, 'P = 118.4 - 58.75 - 39.15', fx, y + 74, 6.4, .66)
        tx(s, 'P = 20.5 D', fx, y + 98, 7.4, .9, color=ARC)
