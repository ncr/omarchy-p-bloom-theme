"""b07 FEELING HAND: text, field notes and side diagrams.

Numbers are narrative and consistent:
24 taxels per fingertip on a 2.5 mm pitch (a fingertip pad of about
10 x 15 mm), five fingertips = 120 taxels; plus palm sensors not counted.
Latency budget: sensing 5 ms + encoding 10 ms + stimulation 5 ms +
nerve conduction and perception 15 ms = 35 ms, inside a 40 ms target.
16 stimulation channels over three cuffs (median 8, ulnar 6, radial 2).
Grip range 0.5-60 N; a child's hand is held at about 3 N; a detected slip
raises the grip by 1 N and the rule settles back after 0.5 s.
Concept illustration; no clinical performance is claimed.
"""

ENTRY = dict(
    id='b07', series='B07', number=207, slug='feeling-hand', title='FEELING HAND',
    domain='prosthetics', category='serious', model='FH-5', palette='crimson', seed=260107,
    purpose='SENSORY PROSTHETIC HAND',
    narrative=('Returns the sense of touch. Pressure, texture and warmth at the fingertips reach '
               'the wearer as natural feeling in the missing hand, so a parent can hold a child\'s '
               'hand in a crowd without looking down at it.'),
    enabled_by=[
        ('TACTILE SKINS', 'Flexible sensor arrays that measure pressure, vibration and warmth at fingertip resolution.'),
        ('NERVE STIMULATION', 'Cuff electrodes on the remaining nerves that evoke touch felt in the missing fingers.'),
        ('OSSEOINTEGRATION', 'A titanium implant anchored in bone that carries the limb and its signal leads.'),
    ],
    real_basis='Tactile sensor skins, targeted nerve stimulation and osseointegration.',
    required_breakthroughs='Stable, natural-feeling sensory feedback over a lifetime of use.',
    view_A='SENSING HAND, READY TO HOLD',
    view_B='FINGERTIP SKIN', view_B_note='NAIL CAP / TAXELS ON FLEX CIRCUIT / COMPLIANT SKIN',
    view_C='NERVE INTERFACE', view_C_note='FEEDTHROUGH / THREADED FIXTURE / THREE CUFFS',
    service_year='2038',
    sources=['https://doi.org/10.1126/scitranslmed.3010081', 'https://doi.org/10.1056/NEJMoa1917537'],
    source_scope='Real basis only: research on sensory feedback via peripheral nerve stimulation and osseointegrated neuromusculoskeletal prostheses. The hand, figures and rules are an original concept, not a clinical device.',
)

DOSSIER = dict(
    kind='touch',
    fact=('Pressure, texture and warmth are measured at the fingertips and returned '
          'as feeling in the missing hand, so the wearer can hold on without watching.'),
    rows=[('TAXELS', '24 PER FINGERTIP / 2.5 mm PITCH'),
          ('FEEDBACK DELAY', 'UNDER 40 ms'),
          ('STIMULATION', '16 CHANNELS / 3 NERVES'),
          ("A CHILD'S HAND", 'HELD AT ABOUT 3 N')],
    note="HE HELD HIS SON'S HAND ALL THE WAY TO SCHOOL AND WATCHED THE ROAD.",
    left=('FROM FINGERTIP TO FEELING', 'SIGNAL PATH / DECLARED LATENCY BUDGET / ms',
          'Budget, not measurement: 5 + 10 + 5 + 15 = 35 ms, inside a 40 ms target.'),
    right=("HOLD, DON'T SQUEEZE", 'DECLARED GRIP RULE / SLIP ADDS 1 N FOR 0.5 s',
           'A rule for illustration, not a measured trace: slip is sensed as vibration.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        stages = [('TAXELS', 5), ('ENCODER', 10), ('STIMULATOR', 5), ('NERVE', 15)]
        step = (w - 70) / 4; yy = y + 26
        for i, (name, ms) in enumerate(stages):
            cx = x + 30 + i * step
            if name == 'TAXELS':
                for r in range(3):
                    for c in range(4):
                        s.circ(cx - 9 + c * 6, yy - 6 + r * 6, 1.6, .85, .6, color=ARC)
            elif name == 'ENCODER':
                # Pulse train: rate follows pressure (declared coding, not a recording).
                pts = [(cx - 16, yy + 6)]
                for k, xx in enumerate((-12, -6, -1, 3, 7, 10, 13)):
                    pts += [(cx + xx, yy + 6), (cx + xx, yy - 8), (cx + xx + 1.2, yy - 8), (cx + xx + 1.2, yy + 6)]
                pts.append((cx + 17, yy + 6))
                s.poly(pts, .8, .6, close=False, color=GOLD)
            elif name == 'STIMULATOR':
                s.rect(cx - 12, yy - 9, 24, 18, .85, .7)
                for k in range(3):
                    s.ln(cx - 7 + k * 7, yy - 4, cx - 7 + k * 7, yy + 4, .6, .6)
            else:
                s.circ(cx, yy, 9, .8, .7, color=ARC)
                s.circ(cx, yy, 5, .5, .5, color=ARC)
            tx(s, name, cx, yy + 25, 6.6, .8, align='c')
            if i < 3:
                arrow(s, (cx + 20, yy), (cx + step - 20, yy), ARC)
        tx(s, 'FELT', x + w - 6, yy + 3, 6.8, .85, align='r')
        # Latency bar, one segment per stage on a 40 ms scale.
        bx = x + 30; scale = (w - 60) / 40.0; by = y + 84
        xx = bx
        for (name, ms), col in zip(stages, (ARC, GOLD, WHITE, ARC)):
            s.rect(xx, by, ms * scale, 10, .8, .65, color=col)
            tx(s, str(ms), xx + ms * scale / 2, by + 24, 6.4, .7, align='c')
            xx += ms * scale
        s.ln(bx + 40 * scale, by - 6, bx + 40 * scale, by + 16, .6, .6, dash=[2, 3])
        tx(s, '40 ms', bx + 40 * scale, by - 10, 6.4, .7, align='c')
        tx(s, 'ms', x, by + 9, 6.4, .6)
    else:
        # Declared rule: hold 3 N; each sensed slip adds 1 N, released after 0.5 s.
        px = x + 34; pw = w - 60; ph = 96; py = y + 6
        for f in (0, 2, 4, 6):
            yy = py + ph * (1 - f / 6)
            s.ln(px, yy, px + pw, yy, .12 if f else .45, .45)
            tx(s, str(f), px - 8, yy + 3, 6.4, .6, align='r')
        tx(s, 'N', px - 8, py - 8, 6.4, .6, align='r')
        T_ = 4.0
        def X(t): return px + pw * t / T_
        def Y(f): return py + ph * (1 - f / 6)
        prof = [(0, 0), (.3, 0), (.6, 3), (1.4, 3), (1.4, 4), (1.9, 4), (1.9, 3), (2.6, 3), (2.6, 4), (3.1, 4), (3.1, 3), (4.0, 3)]
        s.poly([(X(t), Y(f)) for t, f in prof], .9, .8, close=False, color=GOLD)
        for t in (1.4, 2.6):
            s.poly([(X(t) - 5, Y(0) - 3), (X(t) - 3, Y(0) - 9), (X(t) - 1, Y(0) - 3), (X(t) + 1, Y(0) - 9), (X(t) + 3, Y(0) - 3)], .8, .6, close=False, color=ARC)
            tx(s, 'SLIP', X(t) + 7, Y(0) - 4, 6.2, .7, color=ARC)
        tx(s, 'HOLD 3 N', X(.7), Y(3) - 6, 6.4, .75)
        for t in (0, 1, 2, 3, 4):
            tx(s, str(t), X(t), py + ph + 13, 6.2, .6, align='c')
        tx(s, 's', px + pw + 10, py + ph + 13, 6.2, .6)
