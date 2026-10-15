"""b12 WIND FREIGHTER: text, field notes and side diagrams.

Narrative numbers, kept consistent with the model notes:
Ship 150 m x 26 m, draught 8.5 m, about 14 000 t deadweight, 1 100 TEU
(about 400 on deck in the drawing, the rest in the holds). Three wings of
~1 000 m2 (50 m span, mean chord ~16 m + ~5.8 m flap).
Lift per wing at 12 m/s apparent wind, CL 1.85:
  0.5 x 1.225 x 12^2 x 1 000 x 1.85 = 163 kN; three wings ~ 490 kN.
Broad reach, apparent wind 110 deg off the bow, L/D = 8 (lift leans forward,
drag now points slightly forward too):
  thrust = L sin110 - D cos110 = 0.940 + 0.043 = 0.98 L
  side   = L cos110 + D sin110 = -0.342 + 0.117 = -0.22 L (to windward)
  Thrust ~ 0.98 x 490 = 480 kN.
Hull at 11 knots (5.66 m/s) needs ~2.7 MW effective, 2.7e6 / 5.66 = 477 kN:
  in that wind the wings alone hold 11 knots; over a year of crossings
  (lighter and headwind days included) they supply ~80 % of the energy.
Crossing Rotterdam - Halifax, 2 900 nm at 11 kn = 264 h = 11 days.
11 kn = 20.4 km/h, a cyclist's pace (the punchline).
Propulsion energy ~2.7 MW x 264 h = 713 MWh: wind 80 % (570 MWh),
  bio-methanol generator 17 % (121 MWh), battery 3 % (21 MWh, harbour and
  berthing, charged at the quay; pack 24 MWh).
"""
import math

ENTRY = dict(
    id='b12', series='B12', number=212, slug='wind-freighter', title='WIND FREIGHTER',
    domain='shipping', category='serious', model='WF-3', palette='teal', seed=260112,
    purpose='RIGID-WING CARGO SHIP',
    narrative=('Carries 1 100 containers from Rotterdam to Halifax in eleven days, four fifths of the '
               'way on wind. The wings trim themselves through the night watch; the crew of fourteen '
               'hears the sea instead of an engine.'),
    enabled_by=[
        ('RIGID WING SAILS', 'Two-element composite wings with slotted flaps, as proven on sailing cargo ships and racing yachts.'),
        ('WEATHER ROUTING', 'Forecast-driven routes that trade a few hours for a steady, useful wind.'),
        ('HARBOUR PROPULSION', 'Battery-electric pods for harbour and berthing, charged at the quay.'),
    ],
    real_basis='Rigid wing sails, rotor sails, weather routing and battery-electric harbour propulsion.',
    required_breakthroughs='Wing sails that survive decades of storms with little maintenance.',
    view_A='WING-SAILED CONTAINER FEEDER',
    view_B='WING SAIL SECTION', view_B_note='RIBS / SPAR CAPS / MAST / FLAP HINGE ARMS',
    view_C='TRIM ACTUATOR', view_C_note='GEAR RING / THREE DRIVES / FLAP RAM',
    service_year='2034',
    sources=['https://www.imo.org/en/OurWork/Environment/Pages/Wind-propulsion.aspx',
             'https://www.wind-ship.org/en/grid-home/'],
    source_scope='Real basis only: rigid and rotor wind-assist trials, weather routing and battery harbour propulsion. The ship, wings and every figure are an original concept.',
)

DOSSIER = dict(
    kind='crossing',
    fact=('At eleven knots the hull needs about 2.7 MW. On a broad reach in a fresh breeze '
          'the wings alone supply it.'),
    rows=[('LENGTH / BEAM', '150 m / 26 m'),
          ('DRAUGHT', '8.5 m / 14 000 t DEADWEIGHT'),
          ('WIND THRUST', '480 kN / 12 m/s APPARENT WIND'),
          ('CROSSING', '2 900 NAUTICAL MILES')],
    note="SHE CROSSES THE ATLANTIC AT A CYCLIST'S PACE.",
    left=('A WING PULLS FORWARD', 'ONE WING, PLAN VIEW / APPARENT WIND 110° / L / D = 8 / NORMALISED',
          'Thrust = L sin 110° − D cos 110° = 0.98 L; the hull and keel take the small side force.'),
    right=('ONE CROSSING, BY ENERGY SOURCE', 'DESIGN VALUES / 713 MWh OF PROPULSION',
           'The generator runs on bio-methanol; the battery pack holds 24 MWh.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        # Plan view, heading up the page; apparent wind 110 deg on the port side.
        cx, cy = x + 250, y + 78; q = .8
        hull = [(cx, cy - 44 * q), (cx + 7 * q, cy - 27 * q), (cx + 8 * q, cy + 30 * q), (cx + 5 * q, cy + 40 * q),
                (cx - 5 * q, cy + 40 * q), (cx - 8 * q, cy + 30 * q), (cx - 7 * q, cy - 27 * q)]
        s.poly(hull, .5, .6, close=True)
        s.text_mid('HEADING', cx + 14, cy + 30, 6.4, .08, .6)
        awa = math.radians(110)
        frm = (-math.sin(awa), -math.cos(awa))           # from the port side, slightly aft
        to = (-frm[0], -frm[1])
        for k in (-1, 0, 1):
            ox, oy = -to[1] * k * 10, to[0] * k * 10
            sx, sy = cx + frm[0] * 128 + ox, cy + frm[1] * 128 + oy
            arrow(s, (sx, sy), (sx + to[0] * 46, sy + to[1] * 46), WHITE)
        s.text_mid('APPARENT WIND', cx + frm[0] * 128 - 14, cy + frm[1] * 128, 6.4, .08, .66, align='r')
        lift = (to[1], -to[0])
        if lift[1] > 0:
            lift = (-lift[0], -lift[1])
        drag = (to[0] / 8, to[1] / 8)
        k = 70
        tip = (cx + k * lift[0], cy + k * lift[1])
        arrow(s, (cx, cy), tip, ARC)
        s.text_mid('LIFT', tip[0] - 8, tip[1], 6.6, .08, .85, align='r', color=ARC)
        dt = (cx + k * drag[0], cy + k * drag[1])
        arrow(s, (cx, cy), dt, WHITE)
        # Just below its short arrow, on HEADING's left edge.
        s.text_mid('DRAG', cx + 14, cy + 9, 6.4, .08, .66)
        res = (cx + k * (lift[0] + drag[0]), cy + k * (lift[1] + drag[1]))
        s.ln(tip[0], tip[1], res[0], res[1], .35, .5, dash=[2, 3])
        thrust = -(lift[1] + drag[1]); sideforce = lift[0] + drag[0]
        arrow(s, (cx + 34, cy), (cx + 34, res[1]), GOLD)
        s.ln(res[0], res[1], cx + 34, res[1], .35, .5, dash=[2, 3])
        # on one line with LIFT (centred on the lift tip), so the two force labels read as a pair
        s.text_mid(f'THRUST {thrust:.2f}', cx + 44, tip[1], 6.6, .08, .85, color=GOLD)
        tx(s, f'SIDE FORCE {abs(sideforce):.2f}', cx + 44, tip[1] + 17, 6.2, .62)
        tx(s, 'TO WINDWARD', cx + 44, tip[1] + 30, 6.2, .62)
    else:
        bx = x; bw = 400
        tx(s, 'THIS SHIP', bx, y + 8, 6.6, .75)
        yy = y + 16; xx = bx
        for frac, col, fill in ((.80, ARC, .16), (.17, GOLD, .16), (.03, WHITE, .10)):
            s.rect(xx, yy, bw * frac, 16, .8, .7, fill=fill, color=col); xx += bw * frac
        tx(s, 'WIND 570 MWh / 80 %', bx, yy + 32, 6.6, .85, color=ARC)
        tx(s, 'GENERATOR 121 MWh', bx + bw * .97, yy + 32, 6.4, .8, align='r', color=GOLD)
        tx(s, 'BATTERY 21 MWh', bx + bw, yy + 47, 6.4, .7, align='r')
        # Lifted a little so FUEL keeps clear of the caption with enlarged type.
        tx(s, 'SAME HULL, ENGINE ONLY', bx, y + 84, 6.6, .75)
        s.rect(bx, y + 92, bw, 16, .5, .7, fill=.05)
        tx(s, 'FUEL 713 MWh', bx, y + 124, 6.6, .75)
