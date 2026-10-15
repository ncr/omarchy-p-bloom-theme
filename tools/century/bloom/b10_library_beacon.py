"""b10 LIBRARY BEACON: text, field notes and side diagrams.

Numbers are narrative, kept consistent with the model notes:
panels 2 x 120 W; 4.5 peak-sun hours x 240 W x 0.8 system = 864 Wh a day.
Use: 40 tablets x 15 Wh recharge = 600 Wh; server 9 W + mesh radios 1 W
(average over 24 h) = 10 W x 24 h = 240 Wh; total 840 Wh, margin ~20 Wh.
Battery 2.4 kWh LiFePO4 (24 V, 100 Ah): 2 400 / 840 = 2.9 school days
without sun; server and mesh alone 2 400 / 240 = 10 days.
Library 1.3 TB (encyclopedia in three languages with images 0.4 TB, course
videos 0.7 TB, regional maps and books 0.2 TB) on 2 x 4 TB mirrored drives.
Trunk 46 kg including the 22 kg battery, on two wheels.
"""

ENTRY = dict(
    id='b10', series='B10', number=210, slug='library-beacon', title='LIBRARY BEACON',
    domain='education', category='serious', model='LB-40', palette='periwinkle', seed=260110,
    purpose='OFFLINE SOLAR LIBRARY',
    narrative=('Brings an encyclopedia, three years of courses and the region\'s maps to a school '
               'with no internet: one solar trunk, one mast, forty tablets. New books arrive once '
               'a month on a drive carried by the district nurse.'),
    enabled_by=[
        ('OFFLINE CONTENT', 'Compressed encyclopedias, course videos and maps served from local drives, no internet link.'),
        ('MESH NETWORKING', 'Low-power Wi-Fi mesh radios that reach every classroom and the teachers\' houses from one mast.'),
        ('SOLAR STORAGE', 'Folding panels and a lithium iron phosphate battery sized for three sunless school days.'),
    ],
    real_basis='Offline content servers, mesh Wi-Fi and solar storage.',
    required_breakthroughs='Content and devices that stay repairable and current for a decade without connectivity.',
    view_A='SCHOOLYARD LIBRARY TRUNK AND MAST',
    view_B='SERVER CORE', view_B_note='DECK PLATE OMITTED / DRIVES / BATTERY / HEAT SINK',
    view_C='MESH MAST', view_C_note='SECTOR ANTENNAS / RADIO / GUY RING',
    service_year='2029',
    sources=['https://www.kiwix.org/', 'https://www.internet-in-a-box.org/', 'https://learningequality.org/kolibri/'],
    source_scope='Real basis only: offline content servers, community mesh networks, solar storage. The trunk, mast, numbers and routine are an original concept.',
)

DOSSIER = dict(
    kind='school day',
    fact=('Nothing here needs the internet. The library is served from the trunk; '
          'only the monthly update travels, by road.'),
    rows=[('LIBRARY', '1.3 TB / MIRRORED ON TWO DRIVES'),
          ('TABLETS', '40 / 15 Wh EACH A DAY'),
          ('SUN', '240 W OF PANELS / 860 Wh A DAY'),
          ('RESERVE', '2.4 kWh / THREE CLOUDY DAYS')],
    note='THE TEACHER RAISES THE MAST BEFORE THE FIRST BELL.',
    left=('A DAY OF SUN FOR A DAY OF LESSONS', 'DECLARED DAILY BUDGET / Wh / CLEAR DAY',
          'Budget, not measurement: 4.5 sun hours at 80 % system efficiency.'),
    right=('THE LIBRARY UPDATES BY ROAD', 'ONE MONTHLY CYCLE / DECLARED ROUTINE',
           'Requests go back on the same drive; no pupil names leave the school.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        # Two stacked bars on one Wh scale, then the battery reserve.
        bx = x + 110; scale = 290 / 900.0
        def bar(yy, parts, label):
            tx(s, label, x, yy + 4, 6.8)
            xx = bx
            for value, name, col in parts:
                ww = value * scale
                s.rect(xx, yy - 6, ww, 12, .8, .7, color=col)
                tx(s, name, xx + ww / 2, yy - 12, 6.2, .72, align='c')
                xx += ww
            return xx
        end = bar(y + 18, [(864, '864 Wh', ARC)], 'PANELS IN')
        bar(y + 58, [(600, 'TABLETS 600', GOLD), (240, 'CORE + MESH 240', WHITE)], 'USED')
        s.ln(end, y + 6, end, y + 70, .35, .5, dash=[2, 3])
        tx(s, '+24', end + 6, y + 62, 6.4, .7)
        for v in (0, 300, 600, 900):
            s.ln(bx + v * scale, y + 80, bx + v * scale, y + 84, .4, .5)
            tx(s, str(v), bx + v * scale, y + 95, 6.2, .6, align='c')
        # Reserve: 2 400 Wh = three school days of 840 Wh.
        tx(s, 'RESERVE', x, y + 124, 6.8)
        for d in range(3):
            s.rect(bx + d * 97, y + 112, 93, 14, .7, .6, color=ARC)
            tx(s, f'DAY {d + 1}', bx + d * 97 + 46, y + 123, 6.2, .75, align='c')
    else:
        # Monthly cycle: curators -> sealed drive -> nurse's visit -> case -> tablets.
        nodes = [('CURATORS', 'CITY LIBRARY'), ('DRIVE', '4 TB / SEALED'), ('NURSE', 'MONTHLY VISIT'),
                 ('TRUNK', 'SYNC 40 MIN'), ('TABLETS', '40 PUPILS')]
        step = (w - 40) / 4; yy = y + 40
        for i, (a, b) in enumerate(nodes):
            cx = x + 20 + i * step
            if a == 'DRIVE':
                s.rect(cx - 13, yy - 9, 26, 18, .85, .75, color=GOLD)
                s.ln(cx - 7, yy, cx + 7, yy, .5, .5, color=GOLD)
            elif a == 'TRUNK':
                s.rect(cx - 15, yy - 8, 30, 16, .85, .75)
                s.ln(cx, yy - 8, cx, yy - 26, .7, .7); s.circ(cx, yy - 28, 2.4, .8, .6, color=ARC)
            elif a == 'TABLETS':
                for k in range(4):
                    s.rect(cx - 12 + k * 6, yy - 10, 4, 20, .75, .6)
            elif a == 'CURATORS':
                # Library building: pediment, three columns, step.
                s.poly([(cx - 14, yy - 5), (cx, yy - 14), (cx + 14, yy - 5)], .8, .7, close=True)
                for dx in (-9, 0, 9):
                    s.ln(cx + dx, yy - 4, cx + dx, yy + 8, .7, .7)
                s.ln(cx - 15, yy + 10, cx + 15, yy + 10, .8, .7)
            else:
                # The nurse's bag carries the drive between visits.
                s.rect(cx - 13, yy - 7, 26, 17, .85, .75, color=ARC)
                s.poly([(cx - 6, yy - 7), (cx - 6, yy - 12), (cx + 6, yy - 12), (cx + 6, yy - 7)], .7, .7, close=False, color=ARC)
                s.ln(cx - 4, yy + 1.5, cx + 4, yy + 1.5, .8, .8, color=ARC); s.ln(cx, yy - 2.5, cx, yy + 5.5, .8, .8, color=ARC)
            tx(s, a, cx, yy + 28, 6.8, .85, align='c')
            tx(s, b, cx, yy + 42, 6.2, .6, align='c')
            if i < 4:
                arrow(s, (cx + 18, yy), (cx + step - 18, yy), ARC)
        # Return leg: requests and repair notes ride back on the same drive.
        x0 = x + 20 + 3 * step; x1 = x + 20 + step
        s.poly([(x0, yy + 56), (x0, yy + 66), (x1, yy + 66)], .45, .55, close=False, color=GOLD)
        arrow(s, (x1, yy + 66), (x1, yy + 55), GOLD)
        tx(s, 'REQUESTS AND REPAIR NOTES, SAME DRIVE', (x0 + x1) / 2, yy + 84, 6.2, .7, align='c')
