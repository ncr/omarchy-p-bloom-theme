"""HALF-MOON PLOUGH: a small electric tractor that digs demi-lune catchments.

Scale: 1 unit = 1 cm. The ground rises gently to +Y (upslope, 2 %). The
tractor drives along the contour toward -X; at each stop its rear
implement lowers and swings a crescent blade through half a turn, cutting
a basin 4 m across and throwing the soil downslope into a crescent bund.
The basin opens upslope, toward the run-off. Rows are 4 m apart on the
slope and staggered by half the 8 m spacing (313 half-moons a hectare).
Older rows, further up, already carry grass and a sapling in each basin.
Tractor 3.3 m long, 1.7 m wide, canopy at 2.1 m; rear wheels 1.2 m.
The farmer (1.75 m) walks beside it.
"""
from ..kit import *
from .parts import loft, sphere, arc_tube, lumpy
from ..humans import human
from contextlib import contextmanager

SLOPE = .02
HM_R = 200          # half-moon radius (4 m across)
PIVOT = Vector((400, 0, 0))    # implement slew axis, on a trailed frame behind the tractor


def gz(x, y):
    """2 % slope up to +Y, with gentle undulation away from the working area."""
    d = math.hypot(x - 150, y + 20)
    f = min(1.0, max(0.0, (d - 260) / 200)); f = f * f * (3 - 2 * f)
    return SLOPE * y + f * 1.6 * math.sin(x / 260 + .6)


@contextmanager
def _null():
    yield


def wheel(p, r, w, side, lugs=18):
    """Tyre with chevron lugs, rim and hub; axis along Y."""
    ax = (0, side, 0)
    cyl('tyre', Vector(p) - Vector((0, side * w / 2, 0)), r, w, 'structure', ax, 64)
    ring('rim', Vector(p) + Vector((0, side * (w / 2 + .1), 0)), r * .66, r * .1, 1.2, ax, 'detail')
    cyl('hub', Vector(p) + Vector((0, side * (w / 2), 0)), r * .2, 4, 'structure', ax, 24)
    bolts(Vector(p) + Vector((0, side * (w / 2 + 4), 0)), r * .13, 6, ax, 1.0)
    for k in range(lugs):
        a = math.tau * k / lugs
        rad = Vector((math.cos(a), 0, math.sin(a))); tan = Vector((-math.sin(a), 0, math.cos(a)))
        frame = Matrix((tan, Vector((0, 1, 0)), rad)).transposed().to_4x4()
        for half in (-1, 1):
            # Chevron: each half-lug angled toward the tread centre line.
            c = Vector(p) + rad * (r + 1.1) + Vector((0, half * w * .24, 0))
            o = g.softbox('tyre lug', (0, 0, 0), (r * .09, w * .44, 2.4), .5, 'detail')
            o.matrix_world = Matrix.Translation(c) @ frame @ Matrix.Rotation(math.radians(24 * half), 4, 'Z')


def tractor():
    # Chassis rail and belly battery case.
    box('chassis beam', (0, 0, 52), (300, 36, 16), 4)
    box('battery case', (-40, 0, 76), (150, 70, 46), 10)
    for x in (-100, -70, -40, -10, 20):
        box('battery rib', (x, 0, 99.5), (4, 72, 2), 1, 'detail')
    # Rounded hood over the motor; bolted service panel on each flank.
    hood = hull('hood', [(-150, 20, 20, 92), (-140, 30, 28, 92), (-100, 34, 30, 92), (-50, 34, 30, 94), (-30, 30, 28, 94)], 'X', 'structure', .55)
    hull_seam(hood, -100)
    for side in (-1, 1):
        box('side panel', (-90, side * 34.5, 90), (70, 1.2, 34), 3, 'detail')
        for x in (-120, -60):
            for z in (76, 104):
                cyl('panel bolt', (x, side * 35.4, z), 1, 1.2, 'detail', (0, side, 0), 8)
        box('headlamp', (-151, side * 22, 104), (4, 10, 7), 2, 'accent')
    box('grille', (-152, 0, 88), (2, 30, 22), 2, 'detail')
    for z in range(80, 98, 4):
        rod('grille bar', (-153.5, -13, z), (-153.5, 13, z), .6, 'detail')
    # Operator platform, seat, steering column and wheel.
    box('floor plate', (20, 0, 100), (80, 110, 3), 2)
    box('step', (20, -62, 64), (28, 18, 2.5), 1, 'detail')
    rod('step hanger', (10, -60, 64), (10, -55, 99), 1.2, 'detail')
    rod('step hanger', (30, -60, 64), (30, -55, 99), 1.2, 'detail')
    box('seat base', (45, 0, 118), (34, 40, 30), 5)
    box('seat pan', (47, 0, 136), (40, 46, 8), 4)
    box('seat back', (66, 0, 158), (8, 44, 40), 4)
    rod('steering column', (-12, 0, 102), (4, 0, 150), 2.4)
    ring('steering wheel', (4, 0, 150), 19, 2.6, 2.2, (.45, 0, 1), 'structure')
    rod('wheel spoke', (4, 0, 151), (4, -17, 151), 1, 'detail')
    rod('wheel spoke', (4, 0, 151), (4, 17, 151), 1, 'detail')
    # Fenders over the rear wheels.
    for side in (-1, 1):
        ring('rear fender', (70, side * 66, 60), 72, 3, 34, (0, side, 0), 'structure', 20, 175)
    # Roll-over frame with a solar canopy.
    for x in (-8, 92):
        for side in (-1, 1):
            rod('canopy post', (x, side * 52, 100), (x + (6 if x < 0 else -6), side * 48, 212), 3.2)
        rod('canopy bow', (x + (6 if x < 0 else -6), -48, 212), (x + (6 if x < 0 else -6), 48, 212), 3.2)
    box('solar canopy', (42, 0, 218), (128, 118, 4), 3)
    for k in range(1, 6):
        x = -22 + 128 * k / 6
        rod('cell seam', (x, -57, 220.4), (x, 57, 220.4), .35, 'detail')
    rod('cell seam', (-20, 0, 220.4), (104, 0, 220.4), .35, 'detail')
    # Wheels: big lugged rears, smaller fronts.
    for side in (-1, 1):
        wheel((70, side * 66, 60), 60, 34, side, 20)
        wheel((-110, side * 60, 40), 40, 22, side, 16)
    box('front axle beam', (-110, 0, 40), (16, 104, 12), 3)
    # Three-point hitch and PTO-free electric drive to the implement.
    for side in (-1, 1):
        rod('lower link', (150, side * 26, 50), (220, side * 34, 34), 2.6)
    rod('top link', (150, 0, 92), (222, 0, 74), 2.4)
    tube('implement power', [(140, 14, 70), (190, 18, 88), (240, 16, 62), (PIVOT.x - 30, 16, 66)], .9, 'cable')


def implement():
    """Slewing crescent blade: frame on the hitch, ring, swing arm, blade, ridger."""
    P = PIVOT
    with group('B'):
        # Trailed frame from the hitch: the pivot sits 3.3 m behind the rear axle,
        # clear of the half-moon it cuts.
        box('hitch head', (226, 0, 40), (14, 76, 18), 3)
        for side in (-1, 1):
            rod('tow beam', (230, side * 34, 44), (P.x - 26, side * 40, 58), 3.2)
        rod('tow cross brace', (300, -36, 50), (300, 36, 50), 2)
        box('implement frame', (P.x - 14, 0, 58), (26, 90, 12), 3)
        for side in (-1, 1):
            rod('frame upright', (P.x - 24, side * 34, 34), (P.x - 24, side * 34, 72), 2.4)
            # Depth skid wheels set how deep the blade cuts.
            cyl('depth skid wheel', (P.x - 24, side * 52, 16), 15, 7, 'structure', (0, side, 0), 40)
            rod('skid arm', (P.x - 24, side * 38, 50), (P.x - 24, side * 50, 16), 1.8)
        cyl('slewing ring', (P.x, 0, 48), 22, 8, 'structure', (0, 0, 1), 56)
        ring('slew gear', (P.x, 0, 56), 23.5, 3, 3, (0, 0, 1), 'detail')
        motor((P.x + 16, 20, 56), 6, 14, (0, 0, 1))
        # Swing arm, drawn two thirds of the way through its half turn.
        ang = math.radians(-58)
        d = Vector((math.cos(ang), math.sin(ang), 0))
        tip = P + d * (HM_R - 20) + Vector((0, 0, 22))
        rod('swing arm', P + Vector((0, 0, 52)), tip + Vector((0, 0, 20)), 4)
        rod('arm brace', P + Vector((0, 0, 40)), tip + Vector((0, 0, 8)), 2.2, 'detail')
        # Crescent blade: a curved plate following the basin rim, teeth below.
        pts = []; vs = []; fs = []
        for k in range(15):
            a = ang - .32 + .64 * k / 14
            q = P + Vector((math.cos(a), math.sin(a), 0)) * (HM_R - 16)
            for z in (-4, 26):
                vs.append(q + Vector((0, 0, z)))
        for k in range(14):
            fs.append((2 * k, 2 * k + 2, 2 * k + 3, 2 * k + 1))
        g.mesh('crescent blade', vs, fs, 'structure')
        for k in range(8):
            a = ang - .28 + .56 * k / 7
            q = P + Vector((math.cos(a), math.sin(a), 0)) * (HM_R - 16)
            box('blade tooth', q + Vector((0, 0, -7)), (5, 5, 8), 1, 'detail')
        # Ridger wing throws the soil outward into the bund.
        a = ang + .32
        q = P + Vector((math.cos(a), math.sin(a), 0)) * (HM_R - 16)
        g.mesh('ridger wing', [q + Vector((0, 0, -2)), q + Vector((math.cos(a), math.sin(a), 0)) * 30 + Vector((0, 0, 10)),
                               q + Vector((math.cos(a), math.sin(a), 0)) * 30 + Vector((0, 0, 34)), q + Vector((0, 0, 26))],
               [(0, 1, 2, 3)], 'structure')
        rod('blade mount', tip + Vector((0, 0, 20)), tip + Vector((0, 0, 4)), 3)
    with group('C'):
        # Seed hopper on the frame: a pinch of grass seed and one tree seed per basin.
        hp = Vector((P.x - 30, 0, 110))
        loft('seed hopper', [hp + Vector((0, 0, -26)), hp + Vector((0, 0, -12)), hp + Vector((0, 0, 14))],
             lambda t: 9 + 11 * t ** .7, 32)
        cyl('hopper lid', hp + Vector((0, 0, 14)), 21, 3, 'structure', (0, 0, 1), 40)
        rod('lid hinge', hp + Vector((-21, -8, 16)), hp + Vector((-21, 8, 16)), .8, 'detail')
        cyl('metering housing', hp + Vector((0, -8, -34)), 9, 16, 'structure', (0, 1, 0), 32)
        for k in range(10):
            a = math.tau * k / 10
            rod('fluted roller rib', hp + Vector((6.5 * math.cos(a), -9, -34 + 6.5 * math.sin(a))), hp + Vector((6.5 * math.cos(a), 9, -34 + 6.5 * math.sin(a))), .6, 'detail')
        motor(hp + Vector((0, 8, -34)), 4.5, 9, (0, 1, 0))
        loft('drop tube', [hp + Vector((0, 0, -43)), hp + Vector((14, 0, -70)), P + Vector((0, 0, 8))], 2.2, 16, 'cable')
        rod('hopper strut', hp + Vector((-16, -14, -26)), (P.x - 26, -30, 64), 1.6)
        rod('hopper strut', hp + Vector((-16, 14, -26)), (P.x - 26, 30, 64), 1.6)
    mark('CRESCENT BLADE', P + Vector((math.cos(math.radians(-70)), math.sin(math.radians(-70)), 0)) * (HM_R - 16) + Vector((0, 0, 12)), 'SWINGS HALF A TURN / 25 cm DEEP')
    mark('SEED HOPPER', Vector((P.x - 30 - 20, -6, 124)), 'GRASS SEED AND ONE TREE SEED PER BASIN')


def berm(name, cx, cy, span, R, w, h, role, fresh=False):
    """Crescent earth bund as one mesh: rounded section, tapered tips (a fresh cut ends full)."""
    prof = [(-.5, 0), (-.34, .45), (-.16, .88), (0, 1), (.18, .86), (.36, .42), (.5, 0)]
    n = 56
    vs = []; fs = []
    for k in range(n + 1):
        t = k / n
        a = math.pi + math.pi * span * t
        taper = math.sin(math.pi * min(t, .5 if fresh else t)) ** .45 if not fresh else math.sin(math.pi * min(t, .5)) ** .45
        taper = max(.08, taper)
        lump = 1 + .08 * math.sin(k * 1.9 + cx * .01)
        for u, v in prof:
            rr = R + u * w * (.6 + .4 * taper)
            x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
            vs.append((x, y, gz(x, y) - .6 + v * h * taper * lump))
    m = len(prof)
    for k in range(n):
        for j in range(m - 1):
            q = k * m + j
            fs.append((q, q + 1, q + m + 1, q + m))
    fs.append(tuple(range(m)))
    fs.append(tuple(n * m + j for j in reversed(range(m))))
    g.mesh(name, vs, fs, role)


def ground_line(name, pts, r, role):
    tube(name, [(x, y, gz(x, y) + .4) for x, y in pts], r, role)


def half_moon(cx, cy, age, current=False):
    """Basin opening upslope (+Y); crescent bund on the downslope side; the pit inside."""
    span = (302 - 180) / 180 if current else 1.0     # cut so far by the swinging blade
    W, Hb = 56, 24                                   # bund 56 cm wide, 24 cm high
    berm('earth bund', cx, cy, span, HM_R + 22, W, Hb, 'structure' if current else 'detail', fresh=current)
    # Pit outlines: the cut edge under the bund, a depth contour, the upslope lip.
    for rr, role, rad in ((HM_R - 12, 'detail', .9), (HM_R * .62, 'shell', .5)):
        ground_line('basin edge' if role == 'detail' else 'basin contour',
                    [(cx + rr * math.cos(math.pi + math.pi * span * k / 40), cy + rr * math.sin(math.pi + math.pi * span * k / 40)) for k in range(41)], rad, role)
    x1 = cx if current else cx + HM_R - 12
    ground_line('upslope lip', [(cx - HM_R + 12 + (x1 - cx + HM_R - 12) * k / 20, cy + 3 * math.sin(k * 1.3)) for k in range(21)], .45, 'shell')
    if age >= 1:
        # Grass back in the basin: tufts of blades on the pit floor.
        for k in range(11):
            a = math.pi * (1.1 + .8 * k / 10)
            rr = HM_R * (.3 + .45 * ((k * 5) % 4) / 3)
            bx, by = cx + rr * math.cos(a), cy + rr * math.sin(a)
            z0 = gz(bx, by)
            for j in range(5):
                b = -.6 + 1.2 * j / 4
                tube('grass blade', [(bx, by, z0), (bx + 4 * math.sin(b), by + 2 * b, z0 + 8), (bx + 9 * math.sin(b), by + 4 * b, z0 + 13)], .18, 'detail')
    if age >= 2:
        # Sapling where the water pools longest, near the bund.
        tx, ty = cx, cy - HM_R * .5
        z0 = gz(tx, ty)
        organic_branch('sapling trunk', [(tx, ty, z0), (tx + 2, ty, z0 + 50), (tx + 3, ty + 1, z0 + 96)], 2.2, 'structure')
        for k, (dz, a) in enumerate(((58, .3), (70, 2.4), (82, 4.3), (94, 1.2))):
            organic_branch('sapling branch', [(tx + 2, ty, z0 + dz), (tx + 2 + 16 * math.cos(a), ty + 16 * math.sin(a), z0 + dz + 10), (tx + 2 + 26 * math.cos(a), ty + 26 * math.sin(a), z0 + dz + 22)], .9, 'detail')
            for m in range(3):
                t = .5 + .25 * m
                lx, ly = tx + 2 + 26 * t * math.cos(a), ty + 26 * t * math.sin(a)
                leaf('acacia leaf', (lx, ly, z0 + dz + 22 * t), (lx + 8 * math.cos(a + .6), ly + 8 * math.sin(a + .6), z0 + dz + 22 * t + 2), 3.4, 'shell')
    if current:
        # Fresh spoil thrown out by the ridger, still loose beside the blade.
        for k, (deg, dr, r) in enumerate(((292, 34, 8), (286, 44, 6), (298, 48, 5.5), (280, 30, 7), (295, 60, 4.5), (275, 50, 5), (300, 28, 6.5))):
            a = math.radians(deg)
            x, y = cx + (HM_R + dr) * math.cos(a), cy + (HM_R + dr) * math.sin(a)
            lumpy('soil clod', (x, y, gz(x, y) + r * .3), r, seed=40 + k, stretch=(1.2, 1, .6), seg=20, rings=10, role='detail')


FIELD_C = Vector((330, 230, 0))


def field_r(a):
    return 1.0 + .07 * math.sin(3 * a + .4) + .04 * math.sin(7 * a + 2.2)


def ground():
    xs = [-900 + 2600 * i / 80 for i in range(81)]
    ys = [-800 + 2200 * j / 70 for j in range(71)]
    vs = [(x, y, gz(x, y) - .8) for x in xs for y in ys]
    m = len(ys); fs = []
    for i in range(len(xs) - 1):
        for j in range(m - 1):
            a = i * m + j
            fs.append((a, a + m, a + m + 1, a + 1))
    g.mesh('bare ground', vs, fs, 'tube')             # occluder only
    # Field edge: irregular, open at the back (upslope), like a surveyed patch.
    RX, RY = 620, 500
    def edge(a):
        f = field_r(a)
        return FIELD_C.x + RX * f * math.cos(a), FIELD_C.y + RY * f * math.sin(a)
    ground_line('field edge', [edge(math.radians(-196 + 212 * k / 150)) for k in range(151)], .7, 'detail')
    for k in range(22):
        a = math.radians(-190 + 200 * (k + .5) / 22)
        x1, y1 = edge(a)
        ln = .05 if k % 2 else .03
        x0, y0 = FIELD_C.x + (x1 - FIELD_C.x) * (1 - ln), FIELD_C.y + (y1 - FIELD_C.y) * (1 - ln)
        ground_line('edge hachure', [(x0, y0), (x1, y1)], .3, 'shell')
    # Contours across the slope, every 10 cm of height, clipped to the field.
    for zc in (-6, 2, 10):
        pts = []
        for k in range(81):
            x = FIELD_C.x - RX + 2 * RX * k / 80
            lo, hi = -900.0, 1300.0
            for _ in range(40):
                mid = (lo + hi) / 2
                if gz(x, mid) < zc:
                    lo = mid
                else:
                    hi = mid
            y = lo
            dx, dy = (x - FIELD_C.x) / RX, (y - FIELD_C.y) / RY
            inside = dx * dx + dy * dy < .82 * field_r(math.atan2(dy, dx)) ** 2
            if inside and not (abs(x - 160) < 300 and -260 < y < 180):
                pts.append((x, y))
            elif len(pts) > 3:
                ground_line('slope contour', pts, .35, 'shell'); pts = []
            else:
                pts = []
        if len(pts) > 3:
            ground_line('slope contour', pts, .35, 'shell')
    # Crusted bare ground: a few stones and short crack lines.
    for k, (x, y, r) in enumerate(((-150, -130, 9), (640, -170, 7), (840, 260, 10), (-200, 330, 8))):
        lumpy('stone', (x, y, gz(x, y) + r * .3), r, seed=70 + k, stretch=(1.2, 1, .6), seg=20, rings=10, role='detail')
    for k, (x, y, a) in enumerate(((-60, -210, .3), (560, -230, 1.9), (800, 120, .9), (-250, 120, 2.6))):
        ground_line('crust crack', [(x + 18 * m * math.cos(a + .4 * math.sin(m)), y + 18 * m * math.sin(a + .4 * math.sin(m))) for m in range(5)], .25, 'shell')


def build():
    views(B=(-30, 30), C=(-50, 20))
    hx, hy = -290, -10
    human(p=(hx, hy, gz(hx, hy)), scale=.28, angle=-55)
    ground()
    tractor()
    implement()
    # The basin being cut now; last season's two above it, staggered 4 m.
    half_moon(PIVOT.x, 0, 0, current=True)
    half_moon(PIVOT.x - 400, 400, 2)
    half_moon(PIVOT.x + 400, 400, 1)
    mark('ELECTRIC TRACTOR', (-150, -30, 100), '30 kWh / 20 kW / BOLTED PANELS, FIELD REPAIRS')
    mark('SOLAR CANOPY', (-22, -58, 218), 'SHADE FOR THE DRIVER / 300 W TOP-UP')
    mark('LAST SEASON\'S ROW', (PIVOT.x - 400, 400 - HM_R * .5, gz(PIVOT.x - 400, 400 - HM_R * .5) + 90), 'GRASS BACK / ACACIA IN EVERY BASIN')
    a = math.radians(292); x, y = PIVOT.x + (HM_R + 40) * math.cos(a), (HM_R + 40) * math.sin(a)
    mark('FRESH BUND', (x, y, gz(x, y) + 6), '56 cm WIDE / SOIL THROWN DOWNSLOPE')
    mark('HUMAN / AISSATA', (hx + 6, hy - 6, gz(hx, hy) + 110), 'WALKS THE ROWS AFTER THE FIRST RAIN')
    return -34, 34
