"""SKY WHALE: solar-electric rigid airship that winches medicine down to islands.

Units: 1 unit = 25 cm. X forward (nose +X), Y to port, Z up; the landing
terrace of the island is z = 0, the sea is z = -48 (12 m below the terrace).
Hull: 120 m long (480 units), 27 m diameter (R = 54), a body of revolution
with a whale-like profile: a full, rounded forward third (fullest 26 % aft
of the nose) and a long taper into the X tail; about 38 000 m3 inside,
36 000 m3 of it in gas cells. The keel of the faired gondola hovers 26 m
(z = 104) above the terrace; the crate is half-way down. Four tilting
ducted props on outriggers, solar skin on the upper hull.
"""
from ..kit import *
from .parts import wing, loft, sphere, arc_tube, proprotor, frame_matrix, lumpy

L = 480.0
NOSE = 220.0
R = 54.0
BAY_X = 44.0
KEEL = 104.0
SEA = -48.0


def radius(x):
    """Hull radius at station x: blunt, full forward third, long taper aft."""
    t = (NOSE - x) / L
    if t <= 0 or t >= 1:
        return 0.0
    a, b = .36, 1.0
    tm = a / (a + b)
    fmax = tm ** a * (1 - tm) ** b
    return R * (t ** a * (1 - t) ** b) / fmax


def gondola_z(x, rz):
    """Centre height of the faired gondola section at x (half sunk into the belly)."""
    return ZC - radius(x) * .9 - rz * .25


ZC = KEEL + radius(BAY_X) * .9 + 10 * .25 + 10      # gondola keel (rz = 10) at KEEL


def surf(x, ang, off=0.0):
    """Point on the hull surface; ang = 0 at the top, positive toward +Y."""
    r = radius(x) + off
    return Vector((x, r * math.sin(ang), ZC + r * math.cos(ang)))


def hull_mesh():
    xs = []
    n = 90
    for k in range(n + 1):
        t = (1 - math.cos(math.pi * k / n)) / 2           # denser at nose and tail
        xs.append(NOSE - L * t)
    seg = 72; vs = []; fs = []
    rows = []
    for i, x in enumerate(xs):
        r = radius(x)
        if i in (0, len(xs) - 1):
            vs.append(Vector((x, 0, ZC))); rows.append([len(vs) - 1]); continue
        row = []
        for j in range(seg):
            a = T * j / seg
            vs.append(Vector((x, r * math.sin(a), ZC + r * math.cos(a)))); row.append(len(vs) - 1)
        rows.append(row)
    for i in range(len(rows) - 1):
        A, B = rows[i], rows[i + 1]
        if len(A) == 1:
            for j in range(seg):
                fs.append((A[0], B[(j + 1) % seg], B[j]))
        elif len(B) == 1:
            for j in range(seg):
                fs.append((A[j], A[(j + 1) % seg], B[0]))
        else:
            for j in range(seg):
                fs.append((A[j], A[(j + 1) % seg], B[(j + 1) % seg], B[j]))
    g.mesh('rigid hull', vs, fs, 'structure')


def hull_lines():
    # Main ring frames: a few clean surface lines.
    for x in range(-200, 200, 48):
        if radius(x) < 10:
            continue
        tube('ring frame', [surf(x, T * k / 144, .25) for k in range(145)], .14, 'detail')
    # Gores: six long meridians, clear of the solar skin.
    for deg in (35, 90, 140, -35, -90, -140):
        a = math.radians(deg)
        pts = [surf(x, a, .25) for x in [NOSE - 8 - k * (L - 60) / 120 for k in range(121)]]
        tube('envelope gore', pts, .1, 'detail')
    # Solar skin: panels on the upper hull between frames, +-24 degrees of the top.
    for x0 in range(-152, 160, 48):
        x1 = x0 + 44
        for a0, a1 in ((-24, -2), (2, 24)):
            A0, A1 = math.radians(a0), math.radians(a1)
            edge = ([surf(x0 + 2, A0 + (A1 - A0) * k / 12, .35) for k in range(13)] +
                    [surf(x0 + 2 + (x1 - x0 - 4) * k / 12, A1, .35) for k in range(1, 13)] +
                    [surf(x1 - 2, A1 - (A1 - A0) * k / 12, .35) for k in range(1, 13)] +
                    [surf(x1 - 2 - (x1 - x0 - 4) * k / 12, A0, .35) for k in range(1, 13)])
            tube('solar skin panel', edge, .12, 'accent')


def gondola():
    """Keel gondola faired into the belly: crew cabin forward, cargo bay aft."""
    secs = []
    for x, rx, rz in ((128, 1.5, 1.5), (122, 6, 5), (108, 10, 9), (80, 11, 10), (40, 11, 10), (12, 9, 8), (-8, 5, 4), (-20, 1.5, 1.5)):
        secs.append((x, rx, rz, gondola_z(x, rz)))
    secs.reverse()
    o = hull('keel gondola', secs, 'X', 'structure', .8)
    hull_seam(o, 64)
    # Cabin windows along the forward flank, following the fairing.
    for x in range(96, 118, 5):
        zc = gondola_z(x, 9) + 1
        box('cabin window', (x, -9.6, zc), (3.2, .6, 2.6), .6, 'accent')
    return secs


def ducted_prop(p, side, tilt, name='vectoring'):
    """Ducted prop on a hull outrigger. p: hub centre. tilt: degrees nose-down."""
    with at(p, tilt, 'Y'):
        arc_tube(name + ' duct', (-5, 0, 0), (1, 0, 0), (0, 0, 1), 11.5, 1.8, 10)
        ring(name + ' duct lip', (4.2, 0, 0), 11.8, .6, .8, (1, 0, 0), 'detail')
        hull('prop motor pod', [(-9, 1, 1, 0), (-6, 3.4, 3.4, 0), (3, 3.6, 3.6, 0), (6, 2.4, 2.4, 0)], 'X')
        proprotor((2.5, 0, 0), 9.4, 5, (1, 0, 0), 22, root_chord=2.4, tip_chord=1.4, hub=1.6, phase=18 * side)
        for a in (45, 135, 225, 315):
            q = math.radians(a)
            rod('duct stator', (-3, 3.4 * math.cos(q), 3.4 * math.sin(q)), (-3, 9.8 * math.cos(q), 9.8 * math.sin(q)), .45, 'detail')
        cyl('tilt bearing', (-2, -side * 11.5, 0), 2.2, 2, 'detail', (0, -side, 0))


def outrigger(x, side, tilt, grp=None):
    r = radius(x)
    root = surf(x, side * math.radians(105), -.5)
    hub = Vector((x, side * (r + 20), root.z - 2))
    # Aerofoil outrigger strut from the hull frame to the prop tilt bearing.
    wing('outrigger strut', root + Vector((3, 0, 0)), hub + Vector((3, -side * 11.5, 0)), 8, 6,
         (-1, 0, 0), (0, 0, 1), t=.16, camber=0, stations=4)
    ducted_prop(hub, side, tilt)
    return hub


IC = (46.0, 14.0)
IRX, IRY = 150.0, 100.0


def rim(th):
    return 1 + .10 * math.sin(2 * th + .7) + .06 * math.sin(5 * th + 1.9) + .03 * math.sin(9 * th + .3)


def smooth(a, b, x):
    u = min(1, max(0, (x - a) / (b - a)))
    return u * u * (3 - 2 * u)


def land_z(s, th):
    """Terraced headland: flat landing terrace, two field terraces, sea cliff,
    and a crest rising behind the village (the +Y side)."""
    z = 0.0
    z -= 12 * smooth(.40, .50, s)
    z -= 12 * smooth(.58, .68, s)
    z -= (-24 - SEA) * smooth(.74, 1.0, s) ** 1.3
    back = max(0.0, math.cos(th - math.radians(55))) ** 2.4
    z += 30 * back * math.exp(-((s - .66) / .12) ** 2) * smooth(.44, .56, s)
    return z


def land_p(s, th, dz=0.0):
    k = rim(th)
    return Vector((IC[0] + s * IRX * k * math.cos(th), IC[1] + s * IRY * k * math.sin(th), land_z(s, th) + dz))


def island():
    na, ns = 160, 44
    vs = [Vector((IC[0], IC[1], 0))]; fs = []
    for i in range(1, ns + 1):
        for j in range(na):
            vs.append(land_p(i / ns, T * j / na))
    for j in range(na):
        fs.append((0, 1 + j, 1 + (j + 1) % na))
    for i in range(ns - 1):
        for j in range(na):
            a0 = 1 + i * na
            fs.append((a0 + j, a0 + na + j, a0 + na + (j + 1) % na, a0 + (j + 1) % na))
    g.mesh('headland', vs, fs, 'structure')
    # Landing terrace edge: a clean flat ring.
    tube('terrace edge', [land_p(.40, T * k / 200, .35) for k in range(201)], .3, 'structure')
    # Field terrace rims on the seaward side, where the crest does not rise.
    for s_ in (.58, .74):
        seg = []
        for k in range(201):
            th = T * k / 200
            if math.cos(th - math.radians(55)) < .35:
                seg.append(land_p(s_, th, .35))
            elif len(seg) > 1:
                tube('field terrace rim', seg, .22, 'structure'); seg = []
            else:
                seg = []
        if len(seg) > 1:
            tube('field terrace rim', seg, .22, 'structure')
    # Crest line: the highest point along each bearing behind the village.
    crest = []
    for k in range(0, 61):
        th = math.radians(5 + 100 * k / 60)
        best = max((land_z(i / 200, th), i / 200) for i in range(84, 190))
        crest.append((th, best[1]))
    tube('headland crest', [land_p(s_, th, .5) for th, s_ in crest], .4, 'structure')
    # Fall lines from the crest down to the sea and down to the terrace.
    for k in range(3, 58, 4):
        th, sc = crest[k]
        tube('slope hachure', [land_p(sc + .02, th, .4), land_p(sc + .02 + (.22 if k % 8 == 3 else .14), th, .4)], .14, 'detail')
    # Rocks along the seaward shore.
    for k, (deg, r) in enumerate(((212, 7), (236, 5), (262, 9), (291, 6), (318, 8), (338, 5))):
        th = math.radians(deg); p = land_p(1.02, th); p.z = SEA + r * .3
        lumpy('shore rock', p, r, seed=31 + k, stretch=(1.2, 1, .7), seg=28, rings=14)
    # Swell line offshore, seaward side only.
    tube('swell line', [land_p(1.14, math.radians(a)) + Vector((0, 0, SEA - land_z(1.14, math.radians(a)))) for a in range(190, 355, 3)], .15, 'detail')


def village():
    """Landing patch, four houses, a clinic water tank on the flat terrace."""
    lp = Vector((BAY_X + 9, 0, .3))
    tube('landing ring', [lp + Vector((14 * math.cos(T * k / 72), 14 * math.sin(T * k / 72), 0)) for k in range(73)], .4, 'accent')
    for d in ((1, 0), (0, 1)):
        tube('landing cross', [lp + Vector((-7 * d[0], -7 * d[1], 0)), lp + Vector((7 * d[0], 7 * d[1], 0))], .35, 'accent')
    for (hx, hy, ang) in ((88, 34, 14), (62, 48, -8), (12, 42, 30), (0, 16, 6)):
        with at((hx, hy, 0), ang):
            box('house walls', (0, 0, 7), (24, 16, 14), .6)
            vs = [(-12.8, -8.8, 14), (12.8, -8.8, 14), (12.8, 8.8, 14), (-12.8, 8.8, 14), (-12.8, 0, 21), (12.8, 0, 21)]
            g.mesh('house roof', vs, [(0, 1, 5, 4), (3, 4, 5, 2), (0, 4, 3), (1, 2, 5), (0, 3, 2, 1)], 'structure')
            box('house door', (5, -8.2, 3.8), (3.4, .5, 7.2), .3, 'detail')
            box('house window', (-5, -8.2, 8), (3.4, .5, 3), .3, 'detail')
    cyl('clinic water tank', (72, 18, 0), 5, 10, 'structure', (0, 0, 1), 36)
    tube('terrace path', [(66, 12, .3), (60, 6, .3), (55, 2, .3)], .25, 'detail')


def build():
    from ..humans import human
    # The nurse waiting on the landing patch: one standing figure (1.75 m = 7 units).
    human('presence', .0112, -35, (BAY_X - 8, -18, 0))
    views(B=(28, 16), C=(58, 14))
    hull_mesh()
    hull_lines()
    secs = gondola()
    # X tail: four fins at 45 degrees, root on the tapering hull.
    for k in range(4):
        a = math.radians(45 + 90 * k)
        x_le = -176
        root = surf(x_le, a, -2); tipd = Vector((0, math.sin(a), math.cos(a)))
        tip = root + tipd * 46 + Vector((-34, 0, 0))
        up = Vector((1, 0, 0)).cross(tipd).normalized()
        wing('x-tail fin', root, tip, 64, 30, (-1, 0, 0), up, t=.17, camber=0, stations=6)
        wing('fin rudder', root + Vector((-54, 0, 0)) + tipd * 2, tip + Vector((-24, 0, 0)) - tipd * 2, 10, 7, (-1, 0, 0), up, t=.06, camber=0, stations=4, role='detail')
    # Nose cone battens and mooring cone.
    for k in range(8):
        a = T * k / 8
        tube('nose batten', [surf(NOSE - .6, a, .3), surf(NOSE - 3, a, .3), surf(NOSE - 12, a, .3), surf(NOSE - 26, a, .3)], .15, 'detail')
    sphere('mooring cone', (NOSE + .8, 0, ZC), 2.4, 'detail', 20, 10)
    # Props: front pair tilted for hover-hold, aft pair on the C group.
    for side in (-1, 1):
        outrigger(96, side, 18)
    with group('C'):
        hub_c = outrigger(-120, -1, 0)
    outrigger(-120, 1, 0)
    # --- B: cargo bay winch (gondola shell not in this group) -------------------
    gz = gondola_z(BAY_X, 10)                     # gondola centre height at the bay
    bay_floor = gz - 10 * .8
    with group('B'):
        wz = gz + 3.5
        cyl('winch drum', (BAY_X, -6, wz), 4.2, 12, 'structure', (0, 1, 0), 48)
        for yy in range(-5, 6, 1):
            ring('cable wrap', (BAY_X, yy, wz), 4.45, .35, .6, (0, 1, 0), 'detail')
        for yy in (-6.6, 6.0):
            cyl('drum flange', (BAY_X, yy, wz), 5.6, .6, 'structure', (0, 1, 0), 48)
        for yy in (-6.6, 6.0):
            box('winch pedestal', (BAY_X, yy, wz - 4.4), (8, 1.1, 4.2), .4)
        rod('level wind screw', (BAY_X - 6.5, -6, wz + 5), (BAY_X - 6.5, 6, wz + 5), .45, 'detail')
        box('level wind carriage', (BAY_X - 6.5, 1.5, wz + 5), (2.2, 2.4, 2.2), .5, 'accent')
        motor((BAY_X, 7.2, wz), 3, 6, (0, 1, 0))
        cyl('brake disc', (BAY_X, -8.2, wz), 4.6, .6, 'accent', (0, -1, 0), 40)
        box('brake caliper', (BAY_X + 3.6, -8.4, wz + 2.4), (2.4, 1.6, 2.6), .5, 'detail')
        box('winch frame', (BAY_X + 2, 0, wz - 7), (22, 18, 1.4), .6)
        cyl('bay sheave', (BAY_X + 7, 0, bay_floor + 3), 2.2, 1.2, 'structure', (0, 1, 0), 32)
        box('load cell', (BAY_X + 7, 0, bay_floor + 6.2), (2.4, 2.4, 2.4), .5, 'detail')
        tube('winch cable', [(BAY_X + 3.8, 0, wz - 2), (BAY_X + 8.8, 0, bay_floor + 3.5), (BAY_X + 9.2, 0, bay_floor - 7)], .25, 'cable')
        # Bay doors swung down; the hook and sling spreader just below them.
        for side in (-1, 1):
            with at((BAY_X + 7, side * 5.6, bay_floor), -side * 58, 'X'):
                box('bay door', (0, 0, -3.8), (18, .8, 7.6), .5)
                for xx in (-8, 8):
                    cyl('door hinge', (xx, 0, 0), .8, 3, 'detail', (1, 0, 0), 12)
        loft('crate hook', [(BAY_X + 9.2, 0, bay_floor - 7), (BAY_X + 9.2, 0, bay_floor - 10), (BAY_X + 7.6, 0, bay_floor - 11.5), (BAY_X + 6.6, 0, bay_floor - 10)], .55, 10, 'accent')
        sphere('hook swivel', (BAY_X + 9.2, 0, bay_floor - 6.5), .9, 'detail', 14, 8)
    # Cable to the crate being lowered, the crate and its four-leg sling.
    cz = 66
    tube('lowering cable', [(BAY_X + 9.2, 0, bay_floor - 11), (BAY_X + 9.2, 0, cz + 10)], .2, 'cable')
    for dx, dy in ((-2.4, -2.4), (2.4, -2.4), (2.4, 2.4), (-2.4, 2.4)):
        tube('crate sling', [(BAY_X + 9.2, 0, cz + 10), (BAY_X + 9.2 + dx, dy, cz + 4.8)], .12, 'cable')
    box('medical crate', (BAY_X + 9.2, 0, cz + 2.4), (5.2, 5.2, 4.8), .4)
    box('crate label', (BAY_X + 9.2, -2.7, cz + 2.8), (2.6, .3, 1.6), .2, 'accent')
    island()
    village()
    mark('SOLAR SKIN', surf(118, math.radians(-14), .4), '2 400 m² ON THE UPPER HULL')
    mark('HELIUM CELLS', surf(150, math.radians(-112), .3), '36 000 m³ IN 14 CELLS')
    fa = math.radians(315); froot = surf(-176, fa, -2); ftd = Vector((0, math.sin(fa), math.cos(fa)))
    mark('X TAIL', froot + ftd * 30 + Vector((-34, 0, 0)), 'FOUR FINS / ANY THREE CAN STEER')
    ra = radius(-120); rroot = surf(-120, -math.radians(105), -.5)
    mark('TILTING PROPS', Vector((-120, -(ra + 20), rroot.z - 2 + 11.6)), 'HOLD POSITION IN A 30 km/h WIND')
    mark('MEDICAL CRATE', (BAY_X + 9.2, -2.7, cz + 2.4), '40 m OF WINCH CABLE / ONE TONNE A LIFT')
    mark('LANDING PATCH', (BAY_X - 8, -18, 3), 'THE NURSE WAITS / 30 m OF FLAT TERRACE')
    return 50, 22
