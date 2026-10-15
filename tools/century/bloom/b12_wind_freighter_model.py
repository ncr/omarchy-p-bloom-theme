"""WIND FREIGHTER: 150 m container ship driven mostly by three rigid wing sails.

Units: 1 unit = 0.5 m. X from the transom (0) to the stem (300), Y to port,
Z up from the design waterline (0). Beam 26 m (52 u), draught 8.5 m (17 u),
freeboard 7 m (14 u) rising to 9.5 m at the forecastle.
Three two-element wings on slewing towers at x = 95, 165, 235: wing root at
20 m above the waterline (above four-high deck stacks), span 50 m, chord
18 -> 14 m main element plus a 6.5 -> 5 m slotted flap (~1 000 m2 each).
All three are trimmed for an apparent wind 110 degrees on the port side (broad reach).
Deckhouse aft (four decks + bridge), freefall lifeboat on the stern ramp.
"""
from ..kit import *
from .parts import wing, loft, sphere, arc_tube, airfoil

L = 300
MASTS = (95, 165, 235)
ROOT_Z = 40
SPAN_Z = 100
SPLIT_Z = 58                     # lower wing panel / upper wing panel joint
TRIM = 278                       # chord direction (LE -> TE): apparent wind 110 deg on the port side
FLAP = 17                        # flap deflection, degrees


def stations():
    # x, deck half-beam, waterline half-beam, depth below WL, deck height
    return [(0, 23, 21, 7, 14), (8, 25, 24, 13, 14), (40, 26, 26, 17, 14), (215, 26, 26, 17, 14.2),
            (250, 25, 23.5, 16.5, 15), (272, 21, 15, 15, 16.5), (287, 14, 6.5, 12.5, 18),
            (296, 6, 2, 9, 19), (300, 1.2, .6, 6, 19.4)]


def section(B, Bw, D, H, n=14, box=.35):
    """Port deck edge -> side -> bilge -> keel -> starboard, then deck back."""
    pts = [(B, H)]
    for j in range(n + 1):
        ph = math.pi * j / n
        c = math.cos(ph); s_ = math.sin(ph)
        pts.append((Bw * math.copysign(abs(c) ** box, c), -D * abs(s_) ** box))
    pts.append((-B, H))
    for j in range(1, 6):
        yy = -B + 2 * B * j / 6
        pts.append((yy, H + .5 * (1 - (yy / max(B, 1e-3)) ** 2)))
    return pts


def ship_hull():
    st = stations(); rows = []
    xs = []
    for a, b in zip(st, st[1:]):
        k = 8 if b[0] - a[0] > 20 else 4
        xs.extend(a[0] + (b[0] - a[0]) * j / k for j in range(k))
    xs.append(st[-1][0])

    def at_x(x):
        for a, b in zip(st, st[1:]):
            if a[0] <= x <= b[0]:
                t = (x - a[0]) / (b[0] - a[0]); t = t * t * (3 - 2 * t)
                return [a[i] + (b[i] - a[i]) * t for i in range(1, 5)]
        return list(st[-1][1:])
    vs = []; fs = []
    for x in xs:
        B, Bw, D, H = at_x(x)
        box_ = .35 if x < 240 else .35 + .45 * (x - 240) / 60
        rows.append([(x, y, z) for y, z in section(B, Bw, D, H, box=box_)])
    m = len(rows[0])
    for r in rows:
        vs.extend(r)
    for i in range(len(rows) - 1):
        for j in range(m):
            fs.append((i * m + j, i * m + (j + 1) % m, (i + 1) * m + (j + 1) % m, (i + 1) * m + j))
    fs.append(tuple(reversed(range(m))))
    fs.append(tuple((len(rows) - 1) * m + j for j in range(m)))
    g.mesh('hull', vs, fs, 'structure')
    # Waterline and boot-top as lines on the skin.
    for z, role, name in ((0, 'accent', 'design waterline'), (-3, 'detail', 'boot-top line')):
        port = []; stbd = []
        for x in xs:
            B, Bw, D, H = at_x(x)
            if z == 0:
                w = Bw
            else:
                box_ = .35 if x < 240 else .35 + .45 * (x - 240) / 60
                f = abs(z) / D
                w = Bw * max(0, 1 - f ** (1 / box_)) ** box_ if f < 1 else 0
            port.append(Vector((x, w + .15, z))); stbd.append(Vector((x, -w - .15, z)))
        g.wire(name, port, .12, role); g.wire(name, stbd, .12, role)
    return at_x


def deck_rail(at_x, x0, x1, side):
    pts = []; x = x0
    while x <= x1:
        B, Bw, D, H = at_x(x)
        pts.append((x, side * (B - .6), H + 2.4))
        if int(x) % 8 == 0:
            rod('rail stanchion', (x, side * (B - .6), H), (x, side * (B - .6), H + 2.4), .18, 'detail')
        x += 2
    g.wire('deck railing', [Vector(p) for p in pts], .14, 'detail')


def containers(at_x, x0, x1, tiers, rows=9):
    """Deck stacks: 20 ft = 12.2 u, 40 ft = 24.4 u, 2.44 m wide, 2.6 m high."""
    w = 4.88; h = 5.2; x = x0
    H = at_x((x0 + x1) / 2)[3] + 1.5
    box('hatch cover', ((x0 + x1) / 2, 0, H - .75), (x1 - x0 + 2, rows * w + 2, 1.5), .6)
    lengths = []
    while x + 12.2 <= x1 + .01:
        L40 = x + 24.4 <= x1 + .01
        lengths.append((x, 24.4 if L40 else 12.2)); x += 24.4 if L40 else 12.2
    for i in range(rows):
        y = -rows * w / 2 + w * (i + .5)
        for t in range(tiers):
            for xa, ln in lengths:
                g.box('container', (xa + ln / 2, y, H + h * (t + .5)), (ln - .3, w - .25, h - .2), 'detail')


def wing_rib(name, le, d, n, c, t, z, thick=.5, role='structure'):
    sec = airfoil(24, t, 0)
    vs = []
    for zz in (z, z + thick):
        for x, y in sec:
            p = le + d * (x * c) + n * (y * c)
            vs.append(Vector((p.x, p.y, zz)))
    m = len(sec)
    fs = [tuple(range(m)), tuple(m + j for j in reversed(range(m)))]
    for j in range(m):
        fs.append((j, (j + 1) % m, m + (j + 1) % m, m + j))
    return g.mesh(name, vs, fs, role)


def wing_geometry(xm, index, lower_group=None):
    d = Vector((math.cos(math.radians(TRIM)), math.sin(math.radians(TRIM)), 0))
    n = Vector((-d.y, d.x, 0))
    q = math.radians(FLAP)
    dfl = (d * math.cos(q) + n * math.sin(q)).normalized(); nfl = Vector((-dfl.y, dfl.x, 0))
    mast = Vector((xm, 0, 0))

    def chord(z):   # main-element chord in units, linear taper
        return 36 - 8 * (z - ROOT_Z) / SPAN_Z

    def le(z):
        return mast - d * (.3 * chord(z)) + Vector((0, 0, z))

    def fle(z):
        c = chord(z)
        return le(z) + d * (c * .93) + n * (-.02 * c)

    def fch(z):
        return 13 - 3 * (z - ROOT_Z) / SPAN_Z
    parts = {}
    lower = [ROOT_Z, SPLIT_Z]; upper = [SPLIT_Z, ROOT_Z + SPAN_Z]
    from contextlib import nullcontext
    for key, (z0, z1) in (('lower', lower), ('upper', upper)):
        with (group(lower_group) if (lower_group and key == 'lower') else nullcontext()):
            parts[key] = [
                wing('wing skin main', le(z0), le(z1), chord(z0), chord(z1), d, n, t=.16, camber=0, stations=6, tip_round=False),
                wing('wing skin flap', fle(z0), fle(z1), fch(z0), fch(z1), dfl, nfl, t=.12, camber=0, stations=6, tip_round=False),
            ]
    # Tip fairing and panel seams on the upper skin.
    wing('wing tip cap', le(ROOT_Z + SPAN_Z), le(ROOT_Z + SPAN_Z + 1.4), chord(ROOT_Z + SPAN_Z), chord(ROOT_Z + SPAN_Z) * .92, d, n, t=.12, camber=0, stations=2, role='detail')
    for z in (78, 98, 118):
        c = chord(z); pts = []
        for x, y in airfoil(28, .16, 0):
            p = le(z) + d * (x * c) + n * (y * c * 1.04)
            pts.append(p)
        g.wire('wing panel seam', pts + [pts[0]], .1, 'detail')
    return d, n, dfl, nfl, le, fle, chord, fch


def gear_motor(p, r=1.3, h=6.5):
    """Small vertical trim drive: can, flange, brake disc, pinion."""
    p = Vector(p)
    cyl('drive motor can', p, r, h, 'structure', (0, 0, 1), 28)
    ring('drive cooling band', p + Vector((0, 0, h * .35)), r + .25, .3, .5, (0, 0, 1), 'detail')
    ring('drive cooling band', p + Vector((0, 0, h * .6)), r + .25, .3, .5, (0, 0, 1), 'detail')
    cyl('drive brake', p + Vector((0, 0, -1.2)), r * .85, 1.2, 'detail', (0, 0, 1), 24)
    cyl('drive flange', p + Vector((0, 0, h)), r + .6, .5, 'detail', (0, 0, 1), 28)
    box('drive terminal box', p + Vector((r + .6, 0, h * .45)), (1.2, 1.6, 2), .3, 'detail')


def tower_head(xm):
    with at((xm, 0, 0)):
        g.casting('slewing tower head', [(ROOT_Z - 12, 4.9, 4.9), (ROOT_Z - 5, 4.8, 4.8), (ROOT_Z - 3.6, 6.4, 6.4), (ROOT_Z - 3.2, 6.2, 6.2)])
        g.trim('tower head seam', ROOT_Z - 9, 5.0, 5.0)


def tower(xm, H):
    with at((xm, 0, 0)):
        g.casting('slewing tower', [(H, 6.2, 6.2), (H + 3, 5.8, 5.8), (ROOT_Z - 12, 4.9, 4.9)])
        g.trim('tower seam', H + 12, 5.5, 5.5)
        # Ladder inside a cage on the service side of the tower (crew scale).
        for zz in range(int(H) + 2, ROOT_Z - 6, 2):
            rod('tower ladder rung', (-2, -5.4, zz), (2, -5.4, zz), .12, 'detail')
        for x in (-2, 2):
            rod('tower ladder rail', (x, -5.4, H + 1), (x, -5.4, ROOT_Z - 6), .16, 'detail')


def build():
    views(B=(98, 50), C=(30, 40))
    at_x = ship_hull()
    # Forecastle, windlass, mooring bitts, anchor hawse.
    B, Bw, D, H = at_x(282)
    edge = []
    for k in range(25):
        x = 262 + 38 * k / 24
        Bx, _, _, Hx = at_x(min(x, 300))
        edge.append((x, Bx, Hx))
    ring_pts = [(x, b_ - .3, h) for x, b_, h in edge] + [(x, -(b_ - .3), h) for x, b_, h in reversed(edge)]
    vs = [Vector(p) for p in ring_pts] + [Vector((x, y, z + 3.2)) for x, y, z in ring_pts]
    m = len(ring_pts)
    fs = [(j, j + 1, m + j + 1, m + j) for j in range(m - 1)]
    g.mesh('forecastle bulwark', vs, fs, 'structure')
    g.wire('bulwark capping', [Vector((x, y, z + 3.2)) for x, y, z in ring_pts], .25, 'detail')
    for side in (-1, 1):
        cyl('windlass drum', (280, side * 7, 21), 2.2, 4, 'detail', (0, side, 0), 24)
        cyl('mooring bitt', (270, side * 16, 18), 1, 3, 'detail')
        arc_tube('anchor hawse', (289, side * 11.8, 12.5), (0, side, .25), (1, 0, 0), 2.1, .5, .8)
    # Deckhouse aft: four decks, bridge with wings, radar mast, exhaust uptake.
    Hd = at_x(30)[3]
    box('deckhouse', (27, 0, Hd + 12), (26, 38, 24), 1.2)
    for z in (6, 12, 18):
        g.wire('deck line', [Vector((40.3, -19, Hd + z)), Vector((40.3, 19, Hd + z))], .12, 'detail')
    box('navigation bridge', (29, 0, Hd + 27), (18, 52, 6), 1.2)
    for yy in range(-22, 23, 4):
        g.box('bridge window', (38.2, yy, Hd + 27.6), (.2, 3, 2.4), 'detail')
    box('bridge roof', (29, 0, Hd + 30.4), (19, 53, .8), .3, 'detail')
    rod('radar mast', (24, 0, Hd + 30.8), (24, 0, Hd + 38), .5)
    box('radar scanner', (24, 0, Hd + 38.5), (1.2, 9, .8), .3, 'detail')
    box('generator uptake', (17, 0, Hd + 29), (5, 7, 10), 1.4)
    # Freefall lifeboat on the stern ramp.
    with at((6, 0, Hd + 7), -28, 'Y'):
        hull('freefall lifeboat', [(-8, .4, .6, 0), (-6, 2.4, 2.4, 0), (4, 2.6, 2.6, 0), (8, 1, 1.2, 0)], 'X')
    for side in (-1, 1):
        rod('lifeboat ramp rail', (0, side * 2.2, Hd + 1), (14, side * 2.2, Hd + 9), .35)
    # Stowed accommodation ladder along the port side, below the deckhouse.
    Bd = at_x(52)[0]
    with at((52, -Bd - .7, Hd - 4.5), 0, 'Z'):
        box('accommodation ladder', (0, 0, 0), (22, .6, 3.4), .3, 'structure')
        for x in range(-10, 11, 2):
            rod('ladder step', (x, -.4, -1.4), (x, -.4, 1.4), .12, 'detail')
        for x in (-11, 11):
            rod('ladder davit arm', (x, 0, 1.7), (x, .6, 4.8), .3, 'detail')
    for side in (-1, 1):
        deck_rail(at_x, 4, 268, side)
    # Deck cargo between the wing towers.
    for x0, x1, tiers in ((48, 87, 4), (104, 157, 4), (174, 227, 3), (243, 268, 2)):
        containers(at_x, x0, x1, tiers)
    # Wing sails: towers, two-element wings.
    for i, xm in enumerate(MASTS):
        H = at_x(xm)[3]
        tower(xm, H)
        tower_head(xm)
        d, n, dfl, nfl, le, fle, chord, fch = wing_geometry(xm, i, 'B' if i == 0 else None)
        if i == 0:
            with group('B'):
                # Inside the lower panel: ribs, spar caps, stringers, mast, hinge arms.
                for z in (ROOT_Z + .1, 49, SPLIT_Z - .6):
                    wing_rib('wing rib main', le(z), d, n, chord(z), .16, z)
                    wing_rib('wing rib flap', fle(z), dfl, nfl, fch(z), .12, z)
                cyl('wing mast', Vector((xm, 0, ROOT_Z - 1)), 2.4, SPLIT_Z - ROOT_Z + 1, 'structure', (0, 0, 1), 32)

                def yt(f, t=.16):
                    return 5 * t * (.2969 * math.sqrt(f) - .126 * f - .3516 * f * f + .2843 * f ** 3 - .1036 * f ** 4)
                for f, r in ((.03, .5), (.12, .45), (.3, .7), (.5, .4), (.7, .4), (.9, .35)):
                    for s_ in ((-1, 1) if f > .05 else (0,)):
                        a0 = le(ROOT_Z) + d * (f * chord(ROOT_Z)) + n * (s_ * max(0, yt(f) * chord(ROOT_Z) - r - .5))
                        b0 = le(SPLIT_Z) + d * (f * chord(SPLIT_Z)) + n * (s_ * max(0, yt(f) * chord(SPLIT_Z) - r - .5))
                        rod('spar cap' if f == .3 else 'skin stringer', a0, b0, r, 'detail')
                for f in (.3, .7):
                    for s_ in (-1, 1):
                        a0 = le(ROOT_Z) + d * (f * chord(ROOT_Z)) + n * (s_ * yt(f, .12) * fch(ROOT_Z) * 0) + (fle(ROOT_Z) - le(ROOT_Z)) + dfl * (f * fch(ROOT_Z)) - d * (f * chord(ROOT_Z))
                        b0 = fle(SPLIT_Z) + dfl * (f * fch(SPLIT_Z))
                        rod('flap stringer', a0 + nfl * (s_ * max(0, yt(f, .12) * fch(ROOT_Z) - .8)), b0 + nfl * (s_ * max(0, yt(f, .12) * fch(SPLIT_Z) - .8)), .3, 'detail')
                for z in (ROOT_Z + 4, SPLIT_Z - 4):
                    a0 = le(z) + d * (chord(z) * .96); b0 = fle(z) + dfl * 1.5
                    rod('flap hinge arm', a0, b0, .5, 'accent')
            zt = ROOT_Z + SPAN_Z - .2
            mark('SLOTTED FLAP', fle(zt) + dfl * (fch(zt) * .55), 'ADDS CAMBER IN LIGHT AIR / FEATHERS FLAT IN A STORM')
        if i == 1:
            with group('C'):
                c = Vector((xm, 0, ROOT_Z - 3))
                ring('slewing bearing outer race', c, 8.2, 1.8, 2.4, (0, 0, 1))
                ring('slewing bearing inner race', c + Vector((0, 0, 2.4)), 6.6, 1.6, 1.4, (0, 0, 1), 'detail')
                ring('drive gear ring', c + Vector((0, 0, -1.4)), 6.2, 1.1, 1.4, (0, 0, 1), 'accent')
                for k in range(48):
                    a = T * k / 48
                    with at(c + Vector((4.9 * math.cos(a), 4.9 * math.sin(a), -.7)), math.degrees(a)):
                        g.box('gear tooth', (0, 0, 0), (.6, .5, 1.3), 'detail')
                for a in (20, 140, 260):
                    a = math.radians(a); pm = c + Vector((3.3 * math.cos(a), 3.3 * math.sin(a), -9.5))
                    gear_motor(pm)
                    cyl('drive pinion', pm + Vector((0, 0, 7.8)), 1.25, 1.3, 'accent', (0, 0, 1), 18)
                box('bearing cover', c + Vector((0, 0, -4)), (13, 13, 5), 1.5, 'shell')
                cyl('wing root plate', c + Vector((0, 0, 3.8)), 7.2, .6, 'structure', (0, 0, 1), 48)
                z = ROOT_Z + .2
                wing_rib('wing root rib main', le(z), d, n, chord(z), .16, z)
                wing_rib('wing root rib flap', fle(z), dfl, nfl, fch(z), .12, z)
                za = ROOT_Z + 2.2
                a0 = le(za) + d * (chord(za) * .72); b0 = fle(za) + dfl * 2.5
                a0 = Vector((a0.x, a0.y, za)); b0 = Vector((b0.x, b0.y, za))
                cyl('flap actuator body', a0, .9, (b0 - a0).length * .55, 'structure', b0 - a0, 20)
                rod('flap actuator rod', a0 + (b0 - a0) * .55, b0, .4, 'accent')
                box('flap horn', b0, (2, 2, 1.6), .5, 'detail')
                box('actuator bracket', a0 - (b0 - a0).normalized() * .6, (2, 2, 1.6), .5, 'detail')
                mark('TRIM DRIVE', c + Vector((0, -8.2, 0)), 'TURNS EACH WING 360 DEGREES ON ITS MAST')
    uncover('B', 'wing skin')
    uncover('C', 'bearing cover', 'wing root plate')
    xc = MASTS[2]
    mark('WING SAIL', Vector((xc, 0, 0)) + Vector((math.cos(math.radians(TRIM)), math.sin(math.radians(TRIM)), 0)) * (-.3 * 28) + Vector((0, 0, ROOT_Z + SPAN_Z)), 'THREE WINGS / 1 000 m² EACH / 50 m SPAN')
    mark('BRIDGE', (38.2, -26, at_x(30)[3] + 27.6), 'ON A FOUR-DECK HOUSE AFT')
    mark('ACCOMMODATION LADDER', (46, -at_x(46)[0] - 1.1, at_x(46)[3] - 4.5), 'PILOT AND CREW BOARD HERE / STOWED AT SEA')
    mark('DECK STACKS', (260, -22.4, at_x(260)[3] + 7), 'FOUR-HIGH / ABOUT 400 ON DECK')
    return 50, 16
