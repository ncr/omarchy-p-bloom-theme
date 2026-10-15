"""b04 FIRST LIGHT: text, field notes and side diagrams.

Numbers are narrative, kept consistent with the model notes:
0.5 m mirror at f/6.8 -> 3.4 m focal length. 3.76 um pixels ->
206265 x 3.76e-6 / 3.4 = 0.23 arcsec per pixel; Saturn's globe (~18 arcsec)
spans ~80 px, the rings (~40 arcsec) ~175 px.
Planet capture: 60 s at 100 frames/s = 6 000 frames; keep the sharpest 10 %
= 600 -> ideal random-noise gain root(600) = 24.
Dark hours at the site ~8.5 h (20:00-04:30); a booking is a 10 min slot
including the slew -> ~50 bookings a night; ~280 clear nights -> ~14 000
images a year, shared by the 120 owning schools.
Power: ~10 m2 of thin-film skin on the dome x ~180 W/m2 = 1.8 kW peak,
~9 kWh on a clear day; night load ~0.5 kW x 10 h + ~2 kWh by day;
30 kWh battery vault = about four nights without sun.
"""

ENTRY = dict(
    id='b04', series='B04', number=204, slug='first-light', title='FIRST LIGHT',
    domain='astronomy', category='serious', model='FL-5', palette='emerald', seed=260104,
    purpose='SCHOOL-OWNED ROBOTIC TELESCOPE',
    narrative='Lets any child book a slot on a real telescope under a dark sky.',
    enabled_by=[
        ('ROBOTIC OBSERVATORIES', 'Mounts, domes and weather stations that open, point and close with nobody on site.'),
        ('REMOTE SCHEDULING', 'A booking queue that fits each request into a clear, dark ten-minute slot.'),
        ('CMOS CAMERAS', 'Fast, low-noise sensors that record a hundred frames a second of a planet.'),
    ],
    real_basis='Robotic observatories, remote scheduling and CMOS astronomy cameras.',
    required_breakthroughs='Maintenance-free operation for years at a remote dark-sky site.',
    view_A='CLAMSHELL SCHOOL OBSERVATORY',
    view_B='FORK MOUNT', view_B_note='DIRECT-DRIVE ALTITUDE AND AZIMUTH / CABLE WRAP',
    view_C='CAMERA TRAIN', view_C_note='DEROTATOR / FOCUSER / FILTER WHEEL / CMOS',
    service_year='2031',
    sources=['https://lco.global/observatory/', 'https://www.faulkes-telescope.com/'],
    source_scope='Real basis only: networked robotic telescopes already serve schools; lucky imaging and stacking are standard practice. The observatory, its site, owners and all figures are an original concept.',
)

DOSSIER = dict(
    kind='night',
    fact=('Each planet picture is built from six thousand short frames. The sharpest '
          'tenth are aligned and stacked while the child who booked them sleeps.'),
    rows=[('NIGHT POWER', '30 kWh / FOUR NIGHTS WITHOUT SUN'),
          ('SATURN ON THE SENSOR', 'GLOBE 80 px / RINGS 175 px'),
          ('BOOKINGS', '50 A NIGHT / 14 000 A YEAR'),
          ('OWNERS', '120 SCHOOLS / FIVE CONTINENTS')],
    note='AMARA, 9, KISUMU. SATURN. TUESDAY, 21:10.',
    left=('ONE NIGHT, MANY SCHOOLS', 'SITE TIME / 5 OF 50 BOOKINGS',
          'The queue only books targets more than 30° above the horizon.'),
    right=('MORE FRAMES, STEADIER RINGS', 'IDEAL STACKING / SNR = SNR1 × ROOT N',
           'Each doubling of the stack raises the signal-to-noise ratio by about 40 %.'),
)

BOOKINGS = [  # (school / target, site time in hours after 20:00, slot index)
    ('KISUMU / SATURN', 1 + 10 / 60),
    ('CUSCO / THE MOON', 0.5),
    ('HANOI / JUPITER', 3 + 50 / 60),
    ('OAXACA / OMEGA CENTAURI', 5 + 20 / 60),
    ('LEEDS / ORION NEBULA', 6 + 40 / 60),
]


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, axes, curve
    if side == 'left':
        t0 = x + 150; tw = w - 162; hours = 8.5
        px = lambda h: t0 + tw * h / hours
        # All fifty ten-minute slots of the night; the five examples in accent.
        chosen = {int(h * 6) for _, h in BOOKINGS}
        for k in range(51):
            h = k / 6
            if h > hours:
                break
            s.rect(px(h) + .6, y + 2, tw / 51 - 1.2, 8, .9 if k in chosen else .28, .5, color=ARC if k in chosen else WHITE)
        s.text_mid('SLOTS', x, y + 6, 6.6, .08, .6)
        for i, (label, h) in enumerate(BOOKINGS):
            ly = y + 28 + i * 18
            s.text_mid(label, x, ly, 6.6, .08, .78)
            # Enlarged type (composed profiles): the guide line starts after the label.
            start = max(t0, x + s.measure(label, 6.6, .08) + 6) if s.type_growth(6.6) else t0
            s.ln(start, ly, t0 + tw, ly, .14, .4)
            s.dot(px(h) + tw / 102, ly, 2.6, .95, color=ARC)
            hh = (20 + int(h)) % 24; mm = round((h - int(h)) * 60)
            tx(s, f'{hh:02d}:{mm:02d}', px(h) + tw / 102 + (6 if h < 7 else -6), ly - 5, 6.4, .7, align='l' if h < 7 else 'r')
        # Time axis kept clear of the caption below, also with enlarged type.
        for h, lab in ((0, '20:00'), (2, '22:00'), (4, '00:00'), (6, '02:00'), (8, '04:00')):
            s.ln(px(h), y + 112, px(h), y + 116, .45, .5)
            tx(s, lab, px(h), y + 127, 6.4, .6, align='c')
        s.ln(t0, y + 112, t0 + tw, y + 112, .4, .5)
    else:
        ax = x + 26; aw = w - 60; ah = 92
        axes(s, ax, y, aw, ah, 'FRAMES STACKED / N', '30', '0')
        curve(s, [(ax + aw * i / 150, y + ah * (1 - (900 * i / 150) ** .5 / 30)) for i in range(151)], GOLD)
        for n in (1, 100, 400, 900):
            s.ln(ax + aw * n / 900, y + ah, ax + aw * n / 900, y + ah + 4, .45, .5)
            tx(s, str(n), ax + aw * n / 900, y + ah + 13 + s.type_growth(6.6), 6.6, .65, align='c')
        n = 600; kx = ax + aw * n / 900; ky = y + ah * (1 - n ** .5 / 30)
        s.ln(kx, ky, kx, y + ah, .35, .5, dash=[2, 3])
        s.dot(kx, ky, 2.8, .95, color=ARC)
        if s.type_growth(6.6):
            # Enlarged type: below the curve, right of the kept point, between grid lines.
            tx(s, '600 KEPT / ×24', kx + 8, y + ah * 0.46, 6.6, .85, align='l', color=ARC)
        else:
            tx(s, '600 KEPT / ×24', kx - 8, ky - 9, 6.6, .85, align='r', color=ARC)
        tx(s, 'SNR / SNR1', ax - 9, y - 8, 6.2, .55, align='l')
