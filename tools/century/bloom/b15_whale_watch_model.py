"""WHALE WATCH: moored acoustic buoy that listens for right whales.

Units are centimetres, z = 0 at the sea surface. Discus hull 260 cm across
(draft 70 cm, freeboard 40 cm), tripod mast to +430 with three 60 W solar
panels, lantern, radar reflector, satellite and AIS antennas. Mooring:
three-leg bridle to a swivel, riser with a subsurface float, a vertical
string of four hydrophones on elastic isolation, acoustic release and a
two-wheel rail anchor on the seabed. Depth is COMPRESSED: the seabed at
z = -1500 stands for a 60 m lane. The North Atlantic right whale is drawn
at true scale (14 m) relative to the buoy.
"""
from ..kit import *
from .parts import loft, sphere, wing, frame_matrix

SEABED = -1500


def revolve(name, prof, n=72, role='structure', c=(0, 0, 0)):
    """Surface of revolution about Z through a profile of (r, z) points."""
    vs = []; fs = []; m = len(prof)
    for r, z in prof:
        for k in range(n):
            a = T * k / n
            vs.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2] + z))
    for i in range(m - 1):
        for k in range(n):
            fs.append((i * n + k, i * n + (k + 1) % n, (i + 1) * n + (k + 1) % n, (i + 1) * n + k))
    if prof[0][0] > .01:
        fs.append(tuple(reversed(range(n))))
    if prof[-1][0] > .01:
        fs.append(tuple((m - 1) * n + k for k in range(n)))
    return g.mesh(name, vs, fs, role)


def circle(name, c, r, role='shell', n=96, z=None):
    c = Vector(c)
    tube(name, [c + Vector((r * math.cos(T * k / n), r * math.sin(T * k / n), 0)) for k in range(n + 1)], .4, role)


def hull_and_deck():
    revolve('discus hull', [(0, -78), (60, -74), (104, -60), (126, -34), (132, -8), (132, 22), (126, 34), (110, 40), (0, 40)])
    ring('fender', (0, 0, 0), 138, 8, 12, (0, 0, 1))
    ring('fender', (0, 0, -6), 138, 8, 0.1, (0, 0, 1), 'detail')
    # Painted waterline band on the hull, just below the fender.
    circle('waterline band', (0, 0, -10), 133, 'accent')
    box('battery well hatch', (30, -20, 41), (70, 56, 3), 4, 'detail')
    for x in (4, 56):
        box('hatch dog', (x, -50, 42.5), (6, 4, 3), 1, 'detail')
    for a in (30, 150, 270):
        q = math.radians(a)
        p = Vector((112 * math.cos(q), 112 * math.sin(q), 41))
        loft('lifting eye', [p + Vector((-5 * math.sin(q), 5 * math.cos(q), 0)), p + Vector((0, 0, 9)), p + Vector((5 * math.sin(q), -5 * math.cos(q), 0))], 1.8, 10)
    # Ballast keel and bridle pads under the hull.
    revolve('ballast keel', [(0, -140), (22, -136), (30, -110), (26, -80), (0, -78)])
    for a in (90, 210, 330):
        q = math.radians(a)
        box('bridle pad', (100 * math.cos(q), 100 * math.sin(q), -66), (16, 16, 10), 2, 'detail')


def mast():
    """Tripod mast with panels, lantern, reflector and antennas (group C)."""
    with group('C'):
        feet = [Vector((70 * math.cos(math.radians(a)), 70 * math.sin(math.radians(a)), 40)) for a in (90, 210, 330)]
        top = Vector((0, 0, 330))
        for f in feet:
            rod('mast leg', f, top + (f - Vector((0, 0, 40))) * .12, 3.2)
            box('leg foot', f + Vector((0, 0, 2)), (14, 14, 4), 1.5, 'detail')
        for z, k in ((140, .72), (240, .42)):
            pts = [Vector((0, 0, z)) + (f - Vector((0, 0, 40))) * k for f in feet]
            for a, b in zip(pts, pts[1:] + pts[:1]):
                rod('mast ring brace', a, b, 1.6, 'detail')
        # Three panels facing outward between the legs, 70 degrees from horizontal.
        for a in (30, 150, 270):
            q = math.radians(a)
            n = Vector((math.cos(q), math.sin(q), 0))
            c = Vector((0, 0, 188)) + n * 44
            m = frame_matrix(c, n * math.sin(math.radians(70)) + Vector((0, 0, math.cos(math.radians(70)))), (0, 0, 1))
            b = len(g.parts); w = len(g.wires)
            box('solar panel', (0, 0, 0), (74, 54, 3.5), 1.5)
            for k in range(1, 4):
                box('cell row', (-37 + k * 18.5, 0, 2), (.8, 50, .6), .2, 'detail')
            transform(b, w, m)
            rod('panel bracket', c - n * 4 + Vector((0, 0, -20)), Vector((0, 0, 170)) + n * 18, 1.4, 'detail')
        # Top platform: lantern, radar reflector, antennas.
        cyl('top plate', (0, 0, 330), 26, 4, 'structure', (0, 0, 1), 48)
        cyl('lantern base', (0, 0, 334), 9, 8, 'structure', (0, 0, 1), 32)
        revolve('lantern lens', [(0, 342), (8, 342), (9, 350), (8, 360), (0, 362)], 32, 'accent')
        cyl('lantern cap', (0, 0, 362), 7, 3, 'detail', (0, 0, 1), 24)
        # Octahedral radar reflector: three orthogonal plates on a short post.
        rc = Vector((-15, 10, 380))
        rod('reflector post', (-15, 10, 334), rc, 1.2, 'detail')
        for ax in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            size = [18, 18, 18]; size[[i for i, v in enumerate(ax) if v][0]] = .6
            box('reflector plate', rc + Vector((0, 0, 0)), tuple(size), .2, 'structure')
        rod('VHF whip', (16, -8, 334), (22, -12, 436), .6)
        cyl('whip base', (16, -8, 334), 2.2, 6, 'detail', (0, 0, 1), 16)
        revolve('satellite puck', [(0, 334), (7, 334), (6.5, 338), (0, 340)], 32, 'detail', (8, 16, 0))
        cyl('AIS antenna', (-18, -12, 334), 1.6, 34, 'structure', (0, 0, 1), 16)
        box('electronics box', (0, 0, 70), (40, 30, 26), 4)
        tube('mast harness', [(0, 12, 83), (8, 10, 150), (6, 6, 240), (4, 4, 328)], .8, 'cable')
    return top


def hydrophone_string(top_z, bottom_z):
    """Four hydrophones on elastic isolation, pressure housing, release (group B)."""
    with group('B'):
        z = top_z
        cyl('acoustic recorder housing', (0, 0, z - 70), 9, 70, 'structure', (0, 0, 1), 36)
        revolve('housing end cap', [(0, z), (9, z), (8, z + 4), (4, z + 7), (0, z + 7)], 36)
        for zz in (z - 60, z - 10):
            ring('housing clamp', (0, 0, zz), 10, 1.4, 3, (0, 0, 1), 'detail')
        loft('upper shackle', [(0, 0, z + 7), (0, 3, z + 13), (0, 0, z + 18)], 1.2, 10, 'detail')
        z -= 76
        for k in range(4):
            # Elastic isolation section: a coiled strain relief between hydrophones.
            pts = [Vector((3 * math.cos(t), 3 * math.sin(t), z - 26 * t / (6 * T))) for t in [T * 6 * j / 72 for j in range(73)]]
            tube('elastic isolation', pts, .6, 'cable')
            tube('electro-mechanical cable', [(4, 0, z), (4.5, 0, z - 13), (4, 0, z - 26)], .3, 'cable')
            z -= 26
            cyl('hydrophone element', (0, 0, z - 18), 3.8, 18, 'accent', (0, 0, 1), 28)
            for zz in (z - 1, z - 17):
                ring('guard ring', (0, 0, zz), 7, 1, 1.2, (0, 0, 1), 'detail')
            for a in (0, 120, 240):
                q = math.radians(a)
                rod('guard bar', (6.5 * math.cos(q), 6.5 * math.sin(q), z - 1), (6.5 * math.cos(q), 6.5 * math.sin(q), z - 17), .5, 'detail')
            z -= 18
        tube('lower line', [(0, 0, z), (0, 0, z - 40)], .6, 'cable')
        z -= 40
        # Acoustic release above the anchor: recovery without divers.
        cyl('acoustic release', (0, 0, z - 56), 6.5, 56, 'structure', (0, 0, 1), 32)
        revolve('release transducer', [(0, z), (6.5, z), (5, z + 5), (0, z + 7)], 32, 'detail')
        box('release hook', (0, 0, z - 62), (10, 4, 10), 1.5, 'detail')
        tube('anchor chain', [(0, 0, z - 66), (4, 0, z - 90), (0, 0, bottom_z + 40)], .8, 'cable')
        # Two stacked railway wheels: the usual sacrificial mooring anchor.
        for k in range(2):
            cyl('rail-wheel anchor', (0, 0, bottom_z + 17 * k), 42, 16, 'structure', (0, 0, 1), 48)
            ring('wheel flange', (0, 0, bottom_z + 17 * k), 46, 4, 3, (0, 0, 1), 'detail')
            cyl('wheel hub', (0, 0, bottom_z + 17 * k + 16), 12, 2, 'detail', (0, 0, 1), 24)
        rod('anchor eye', (0, 0, bottom_z + 34), (0, 0, bottom_z + 42), 2, 'detail')


# Right whale body, local frame: X forward (snout at +X), Y left, Z up; 14 m.
# Stations: (x, half-width above the centre line, half-width below, top z, bottom z).
# The head (x > 350) is a quarter of the length: a narrow arched rostrum on top
# and the broad bowed lower lips below.
WHALE = [(-700, 9, 9, 26, -6), (-620, 22, 22, 52, -30), (-500, 60, 62, 110, -80),
         (-330, 120, 126, 165, -140), (-120, 166, 174, 188, -178), (80, 176, 184, 190, -190),
         (260, 162, 176, 178, -188), (360, 126, 166, 150, -184), (450, 78, 158, 160, -186),
         (540, 54, 134, 164, -160), (620, 38, 104, 140, -112), (672, 24, 62, 100, -62),
         (708, 5, 10, 50, 18)]
WE = .94


def whale_section(x):
    from ..kit import profile_at
    ryt, ryb, zt = profile_at([w[:4] for w in WHALE], x)
    zb = profile_at([(w[0], w[4], 0, 0) for w in WHALE], x)[0]
    return ryt, ryb, zt, zb


def whale_surf(x, a, off=0.):
    ryt, ryb, zt, zb = whale_section(x)
    c, s_ = math.cos(a), math.sin(a)
    ry = ryb + (ryt - ryb) * (1 + s_) / 2 + off
    zc, rz = (zt + zb) / 2, (zt - zb) / 2 + off
    return Vector((x, ry * math.copysign(abs(c) ** WE, c), zc + rz * math.copysign(abs(s_) ** WE, s_)))


def whale_at_z(x, z, side, off=0.):
    """Surface point on one flank at height z."""
    ryt, ryb, zt, zb = whale_section(x)
    zc, rz = (zt + zb) / 2, (zt - zb) / 2
    u = max(-.985, min(.985, (z - zc) / rz))
    s_ = math.copysign(abs(u) ** (1 / WE), u)
    a = math.asin(s_)
    return whale_surf(x, a if side > 0 else math.pi - a, off)


def blade(name, root, span_v, chord_v, up_v, span, le_fn, c_fn, t, stations=18, role='structure'):
    """Lofted fin: airfoil sections along a span, planform given by functions of s."""
    from .parts import airfoil
    root, sv, cv, uv = Vector(root), Vector(span_v).normalized(), Vector(chord_v).normalized(), Vector(up_v).normalized()
    sec = airfoil(24, t, 0); m = len(sec); vs = []; fs = []
    for j in range(stations + 1):
        q = j / stations
        le = root + sv * span * q + cv * le_fn(q)
        c = max(2.5, c_fn(q))
        vs += [le + cv * (x * c) + uv * (z * c) for x, z in sec]
    for j in range(stations):
        for k in range(m):
            a_ = j * m + k; b_ = j * m + (k + 1) % m
            fs.append((a_, b_, b_ + m, a_ + m))
    fs += [tuple(range(m)), tuple(stations * m + k for k in reversed(range(m)))]
    return g.mesh(name, vs, fs, role)


def whale(p, heading, roll=0):
    """North Atlantic right whale, 14 m: no dorsal fin, arched rostrum, bowed
    lower lip, broad paddle flippers, wide notched flukes, callosities."""
    with at(p, heading):
        with at((0, 0, 0), roll, 'X'):
            n = 72; xs = []
            for w0, w1 in zip(WHALE, WHALE[1:]):
                xs += [w0[0] + (w1[0] - w0[0]) * j / 8 for j in range(8)]
            xs.append(WHALE[-1][0])
            vs = [whale_surf(x, T * k / n) for x in xs for k in range(n)]
            fs = [(i * n + k, i * n + (k + 1) % n, (i + 1) * n + (k + 1) % n, (i + 1) * n + k)
                  for i in range(len(xs) - 1) for k in range(n)]
            fs += [tuple(reversed(range(n))), tuple((len(xs) - 1) * n + k for k in range(n))]
            g.mesh('right whale body', vs, fs, 'structure')
            # Flukes: two swept lobes with a deep central notch and pointed tips.
            # Leading edge sweeps back; the trailing edge bulges aft between notch and tip.
            te = lambda q: 95 + 80 * q + 40 * math.sin(math.pi * q)
            le = lambda q: 170 * q ** 1.5
            for s_ in (-1, 1):
                blade('fluke lobe', (-628, s_ * 4, 11), (0, s_, -.04), (-1, 0, 0), (0, 0, 1), 290,
                      le, lambda q: te(q) - le(q), .11)
            # Broad paddle flippers, low behind the head, rounded tips.
            for s_ in (-1, 1):
                r = whale_at_z(330, -118, s_, -6)
                full = lambda q: 84 + 40 * q
                blade('pectoral flipper', r, (-.28, s_ * .62, -.73), (-.96, -s_ * .1, .25), (s_ * .15, .78, .6), 185,
                      lambda q: full(q) * (1 - math.sqrt(max(0., 1 - q ** 6))) / 2,
                      lambda q: full(q) * math.sqrt(max(0., 1 - q ** 6)), .2)
            # Mouth line on the surface: from the gape below the eye, arching high
            # over the bowed lower lip, down to the tip of the rostrum.
            for s_ in (-1, 1):
                pts = []
                for k in range(41):
                    t = k / 40; x = 392 + (704 - 392) * t
                    z = -52 + 84 * t + 100 * math.sin(math.pi * t) ** 1.1
                    pts.append(whale_at_z(x, z, s_, 1.2))
                tube('mouth line', pts, .45, 'detail')
                e = whale_at_z(404, -30, s_, .8)
                ring('eye', e, 4.5, 1.3, 1, (0, s_, 0), 'detail')
            for s_ in (-1, 1):
                ring('blowhole', whale_surf(380, math.pi / 2 + s_ * .12, .6), 3.5, 1.2, 1, (0, 0, 1), 'detail')
            # Callosities: the bonnet on the rostrum, a few along it, one above each eye.
            for x, a, r in ((672, 90, 9), (640, 96, 7), (600, 86, 6), (562, 94, 5)):
                sphere('callosity', whale_surf(x, math.radians(a), -r * .5), r, 'detail', 16, 8, (1.3, 1, .4))
            for s_ in (-1, 1):
                sphere('callosity', whale_at_z(418, -6, s_, -2), 6, 'detail', 16, 8, (1.3, .4, 1))


def build():
    views(B=(24, 8), C=(28, 12))
    hull_and_deck()
    top = mast()
    # Sea surface: a disc of water around the buoy (outline and two ripples).
    circle('sea surface', (0, 0, 0), 760, 'shell', 160)
    for r in (175, 225):
        circle('ripple', (0, 0, 0), r, 'shell', 96)
    # Bridle to a swivel, riser to a subsurface float, then the string.
    sw = Vector((0, 0, -230))
    for a in (90, 210, 330):
        q = math.radians(a)
        tube('bridle leg', [(100 * math.cos(q), 100 * math.sin(q), -70), sw], .7, 'cable')
    sphere('swivel', sw, 5, 'structure', 16, 8)
    fz = -900
    tube('riser', [sw, (18, 0, -520), (8, 0, fz + 44)], .8, 'cable')
    sphere('subsurface float', (0, 0, fz), 42, 'structure', 40, 20)
    ring('float band', (0, 0, fz - 2), 42.5, 2.5, 4, (0, 0, 1), 'detail')
    tube('lower riser', [(0, 0, fz - 42), (-10, 0, -1020), (0, 0, -1110)], .8, 'cable')
    hydrophone_string(-1110, SEABED)
    # Seabed patch with sand ripples.
    circle('seabed', (0, 0, SEABED), 420, 'shell', 120)
    for k, r in enumerate((150, 230, 310)):
        tube('sand ripple', [(r * math.cos(math.radians(a)), r * math.sin(math.radians(a)), SEABED) for a in range(200 + 8 * k, 300 - 6 * k, 4)], .3, 'shell')
    WX, WY, WZ, WH = -120, 720, -520, 14
    whale((WX, WY, WZ), WH, 18)
    mark('SOLAR MAST', (40, -18, 196), '3 x 60 W PANELS / LANTERN / SATELLITE LINK')
    mark('DISCUS HULL', (-136, 0, 4), '2.6 m / BATTERY WELL / WATERLINE MARKED')
    mark('SUBSURFACE FLOAT', (-42, 0, fz), 'KEEPS THE RISER SLACK / DEPTH COMPRESSED')
    mark('HYDROPHONE STRING', (8, 0, -1210), 'FOUR ELEMENTS / 10 Hz TO 2 kHz')
    mark('RAIL-WHEEL ANCHOR', (44, 0, SEABED + 20), 'RELEASED ON COMMAND FOR RECOVERY')
    q = math.radians(WH)
    mark('RIGHT WHALE', (WX - 640 * math.cos(q), WY - 640 * math.sin(q) - 60, WZ + 30), '14 m ADULT / CALLS AT 50 TO 250 Hz')
    return 28, 15
