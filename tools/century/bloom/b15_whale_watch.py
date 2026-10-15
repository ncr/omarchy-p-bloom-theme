"""b15 WHALE WATCH: text, field notes and side diagrams.

Numbers are narrative and kept consistent:
- North Atlantic right whale up-call: about 50-250 Hz, one second long;
  heard by the buoy to about 15 km in ordinary sea states.
- Alert chain (declared): call at t = 0; classified on the buoy and sent
  by satellite, confirmed by t = 5 min; broadcast to ships within 30 km
  (AIS text and VHF) by t = 8 min; a ship at 16 kn reaches 10 kn by
  t = 20 min.
- Power: 3 x 60 W panels = 180 W; average load 12 W (recorder and
  detector 3 W, satellite 2 W, AIS 5 W, lantern 2 W) = 288 Wh a day;
  a 2 kWh battery covers about seven sunless days.
- Speed and risk, illustrative logistic: P(v) = 1 / (1 + exp(-(v - 12) / 2.3))
  for the chance that a strike at v knots is lethal: P(10) = 0.30,
  P(18) = 0.93. Shape after published strike studies; not a fitted model.
"""
import math

ENTRY = dict(
    id='b15', series='B15', number=215, slug='whale-watch', title='WHALE WATCH',
    domain='ocean', category='serious', model='WW-4', palette='teal', seed=260115, view_B_roll=-40,
    purpose='ACOUSTIC WHALE BUOY',
    narrative=('Listens for right whales in the shipping lanes off Cape Cod and asks nearby ships '
               'to slow to ten knots within twenty minutes of a call, so the whales and the ships '
               'can share the water.'),
    enabled_by=[
        ('PASSIVE ACOUSTICS', 'Hydrophones and onboard detectors that recognise the calls of each species.'),
        ('SATELLITE LINKS', 'Low-power messages that reach ships and harbour pilots within minutes.'),
        ('SLOW ZONES', 'Seasonal speed programmes that ships already follow when whales are near.'),
    ],
    real_basis='Passive acoustic monitoring, real-time detection buoys, vessel speed programmes.',
    required_breakthroughs='Reliable detection of every species in noisy water, and every ship listening.',
    view_A='MOORED LISTENING BUOY IN A SHIPPING LANE',
    view_B='HYDROPHONE STRING', view_B_note='FOUR HYDROPHONES / ISOLATION / RELEASE / ANCHOR',
    view_C='SOLAR MAST', view_C_note='PANELS / LANTERN / RADAR REFLECTOR / ANTENNAS',
    service_year='2028',
    sources=['https://www.fisheries.noaa.gov/species/north-atlantic-right-whale',
             'https://doi.org/10.1111/j.1748-7692.2006.00098.x'],
    source_scope='Real basis only: right whale call bands, near-real-time acoustic buoys, vessel speed rules and strike studies. The buoy, timings and risk curve are an original, illustrative concept.',
)

DOSSIER = dict(
    kind='shipping lane',
    fact=('Right whales call often and low. A ship slowed to ten knots gives a whale time '
          'to move, and is far less likely to kill one it strikes.'),
    rows=[('LISTENING', '4 HYDROPHONES / 10 Hz TO 2 kHz'),
          ('RIGHT WHALE CALL', '50 TO 250 Hz / HEARD TO 15 km'),
          ('ALERT', 'SHIPS WITHIN 30 km / 20 MIN'),
          ('POWER', '180 W SOLAR / 2 kWh / 12 W AVERAGE')],
    note='TUESDAY 04:12: TWO RIGHT WHALES HEARD, SEVEN SHIPS SLOWED.',
    left=('FROM A CALL TO A SLOWER SHIP', 'DECLARED SEQUENCE / MINUTES AFTER THE CALL',
          'One ship shown; every ship within 30 km receives the same message.'),
    right=('SLOWER IS SAFER', 'ILLUSTRATIVE LOGISTIC / SHAPE AFTER STRIKE STUDIES',
           'P = 1 / (1 + e^-((v - 12) / 2.3)); a strike is still to be avoided at any speed.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        x0 = x + 70; x1 = x + w - 10
        X = lambda t: x0 + (x1 - x0) * t / 25
        # Events on the time axis.
        ev = [(0, 'HEAR'), (5, 'CHECK'), (8, 'ALERT'), (20, 'SLOW')]
        for t, lab in ev:
            s.ln(X(t), y + 12, X(t), y + 92, .22, .5, dash=[2, 3])
            s.dot(X(t), y + 12, 2.4, .9, color=ARC)
            tx(s, lab, X(t), y + 3, 6.4, .8, align='c')
        # Ship speed trace (declared): 16 kn until the alert, easing to 10 kn by t = 20.
        Y = lambda v: y + 92 - (v - 6) * 5.6
        pts = []
        for k in range(0, 251):
            t = k / 10
            if t < 8: v = 16
            elif t < 20:
                u = (t - 8) / 12; v = 16 - 6 * (3 * u * u - 2 * u ** 3)
            else: v = 10
            pts.append((X(t), Y(v)))
        s.poly(pts, .88, .85, close=False, color=GOLD)
        for v in (10, 16):
            tx(s, f'{v} kn', x0 - 8, Y(v) + 3, 6.4, .7, align='r')
            s.ln(x0, Y(v), x1, Y(v), .1, .4)
        s.ln(x0, y + 92, x1, y + 92, .45, .55)
        for t in (0, 5, 10, 15, 20, 25):
            s.ln(X(t), y + 92, X(t), y + 96, .45, .5)
            tx(s, str(t), X(t), y + 108, 6.4, .64, align='c')
        tx(s, 'MIN', x1, y + 122, 6.2, .55, align='r')
        tx(s, 'SHIP SPEED', x, y + 50, 6.2, .6)
    else:
        x0 = x + 40; x1 = x + w - 60; y0 = y + 4; y1 = y + 96
        X = lambda v: x0 + (x1 - x0) * (v - 4) / 18
        Y = lambda p: y1 - (y1 - y0) * p
        P = lambda v: 1 / (1 + math.exp(-(v - 12) / 2.3))
        for p in (.25, .5, .75, 1):
            s.ln(x0, Y(p), x1, Y(p), .1, .4)
        s.poly([(x0, y0), (x0, y1), (x1, y1)], .45, .55, close=False)
        s.poly([(X(4 + 18 * k / 120), Y(P(4 + 18 * k / 120))) for k in range(121)], .88, .85, close=False, color=GOLD)
        for v, col in ((10, ARC), (18, WHITE)):
            s.ln(X(v), y1, X(v), Y(P(v)), .5, .6, dash=[2, 3])
            s.dot(X(v), Y(P(v)), 2.6, .95, color=col)
            tx(s, f'{v} kn  {P(v):.2f}', X(v) + 7, Y(P(v)) + 13, 6.4, .8)
        tx(s, '1', x0 - 7, y0 + 4, 6.2, .6, align='r')
        tx(s, '0', x0 - 7, y1 + 2, 6.2, .6, align='r')
        for v in (4, 10, 16, 22):
            s.ln(X(v), y1, X(v), y1 + 4, .45, .5)
            tx(s, str(v), X(v), y1 + 16, 6.4, .64, align='c')
        tx(s, 'KNOTS', x1 + 52, y1 + 16, 6.2, .55, align='r')
        tx(s, 'LETHAL IF STRUCK', x0 + 6, y0 - 2, 6.2, .6)
