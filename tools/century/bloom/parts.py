"""Blender-side shape vocabulary for p(bloom). Adds forms the kit lacks:
airfoil surfaces, lofted tubes with a radius law, lumpy natural bodies,
finger-like segments and spheres. Every helper registers ordinary kit parts,
so hidden-line export, groups and transforms behave as in Century.
"""
import math
from mathutils import Vector, Matrix
from ..kit import g, T, curve, at, transform


def _frame(d):
    d = Vector(d).normalized()
    u = d.cross(Vector((0, 0, 1)))
    if u.length < .05:
        u = d.cross(Vector((0, 1, 0)))
    u.normalize()
    return d, u, d.cross(u)


def airfoil(n=28, t=.12, camber=.02):
    """Closed section, chord 0..1 along +x, thickness along +z (NACA-like)."""
    def yt(x):
        return 5 * t * (.2969 * math.sqrt(x) - .126 * x - .3516 * x * x + .2843 * x ** 3 - .1036 * x ** 4)
    xs = [(1 - math.cos(math.pi * k / (n - 1))) / 2 for k in range(n)]
    upper = [(x, camber * 4 * x * (1 - x) + yt(x)) for x in xs]
    lower = [(x, camber * 4 * x * (1 - x) - yt(x)) for x in xs[1:-1]]
    return upper[::-1] + lower


def wing(name, root, tip, c_root, c_tip, chord=(-1, 0, 0), up=(0, 0, 1), t=.12, camber=.02,
         stations=8, role='structure', t_tip=None, tip_round=True):
    """Lofted lifting surface. root/tip are leading-edge points; chord points aft."""
    root, tip = Vector(root), Vector(tip)
    cdir = Vector(chord).normalized(); upv = Vector(up).normalized()
    sec = airfoil(28, t, camber)
    vs = []; fs = []; m = len(sec)
    for j in range(stations + 1):
        s = j / stations
        le = root.lerp(tip, s)
        c = c_root + (c_tip - c_root) * s
        tt = 1.0
        if t_tip is not None:
            tt = 1 + (t_tip / t - 1) * s
        if tip_round and j == stations:
            c *= .96
        for x, z in sec:
            vs.append(le + cdir * (x * c) + upv * (z * c * tt))
    for j in range(stations):
        for k in range(m):
            a = j * m + k; b = j * m + (k + 1) % m
            fs.append((a, b, b + m, a + m))
    fs.append(tuple(range(m)))
    fs.append(tuple(stations * m + k for k in reversed(range(m))))
    return g.mesh(name, vs, fs, role)


def loft(name, points, radii, sides=18, role='structure', smooth=True):
    """Round tube along a path; radii is a function of t in [0,1] or a list."""
    pts = [Vector(v) for v in (curve(points, 10) if smooth and len(points) > 2 else points)]
    n = len(pts); vs = []; fs = []
    prev_u = None
    for i, p in enumerate(pts):
        tangent = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized()
        if prev_u is None:
            _, u, _ = _frame(tangent)
        else:
            u = (prev_u - tangent * prev_u.dot(tangent)).normalized()
        prev_u = u
        v = tangent.cross(u)
        t = i / (n - 1)
        if callable(radii):
            r = radii(t)
        elif isinstance(radii, (int, float)):
            r = radii
        else:
            r = radii[min(len(radii) - 1, int(t * (len(radii) - 1) + .5))]
        for j in range(sides):
            a = T * j / sides
            vs.append(p + r * (math.cos(a) * u + math.sin(a) * v))
    for i in range(n - 1):
        for j in range(sides):
            fs.append((i * sides + j, i * sides + (j + 1) % sides, (i + 1) * sides + (j + 1) % sides, (i + 1) * sides + j))
    fs.append(tuple(reversed(range(sides))))
    fs.append(tuple((n - 1) * sides + j for j in range(sides)))
    return g.mesh(name, vs, fs, role)


def sphere(name, p, r, role='structure', seg=32, rings=16, squash=(1, 1, 1)):
    vs = []; fs = []
    for i in range(1, rings):
        th = math.pi * i / rings
        for j in range(seg):
            ph = T * j / seg
            vs.append(Vector(p) + Vector((r * squash[0] * math.sin(th) * math.cos(ph),
                                          r * squash[1] * math.sin(th) * math.sin(ph),
                                          r * squash[2] * math.cos(th))))
    top = len(vs); vs.append(Vector(p) + Vector((0, 0, r * squash[2])))
    bot = len(vs); vs.append(Vector(p) - Vector((0, 0, r * squash[2])))
    for i in range(rings - 2):
        for j in range(seg):
            a = i * seg + j; b = i * seg + (j + 1) % seg
            fs.append((a, b, b + seg, a + seg))
    for j in range(seg):
        fs.append((top, (j + 1) % seg, j))
        fs.append((bot, (rings - 2) * seg + j, (rings - 2) * seg + (j + 1) % seg))
    return g.mesh(name, vs, fs, role)


def dome(name, p, r, h=None, role='structure', seg=48, rings=12, a0=0, a1=360, base_ring=True):
    """Spherical cap / hemisphere shell surface (open at the base), optional sector."""
    h = r if h is None else h
    vs = []; fs = []; full = a1 - a0 >= 359.9
    cols = seg if full else seg + 1
    for i in range(rings + 1):
        th = (math.pi / 2) * i / rings
        for j in range(cols):
            ph = math.radians(a0 + (a1 - a0) * j / seg)
            vs.append(Vector(p) + Vector((r * math.cos(th) * math.cos(ph), r * math.cos(th) * math.sin(ph), h * math.sin(th))))
    for i in range(rings):
        for j in range(seg):
            a = i * cols + j; b = i * cols + (j + 1) % cols
            fs.append((a, b, b + cols, a + cols))
    return g.mesh(name, vs, fs, role)


def lumpy(name, p, radius, seed=3, bumps=((1.0, 2, .10), (1.0, 4, .05), (1.0, 7, .025)),
          stretch=(1, 1, 1), seg=72, rings=36, role='structure'):
    """Irregular natural body (asteroid, boulder): deterministic low-order noise."""
    import random
    rnd = random.Random(seed)
    waves = []
    for amp, freq, depth in bumps:
        for _ in range(3):
            axis = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))).normalized()
            waves.append((axis, freq, depth * amp, rnd.uniform(0, T)))

    def rad(d):
        k = 1.0
        for axis, f, depth, ph in waves:
            k += depth * math.sin(f * d.dot(axis) * 2.2 + ph)
        return radius * k
    vs = []; fs = []
    for i in range(1, rings):
        th = math.pi * i / rings
        for j in range(seg):
            ph = T * j / seg
            d = Vector((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)))
            q = d * rad(d)
            vs.append(Vector(p) + Vector((q.x * stretch[0], q.y * stretch[1], q.z * stretch[2])))
    for d in (Vector((0, 0, 1)), Vector((0, 0, -1))):
        q = d * rad(d); vs.append(Vector(p) + Vector((q.x * stretch[0], q.y * stretch[1], q.z * stretch[2])))
    top, bot = len(vs) - 2, len(vs) - 1
    for i in range(rings - 2):
        for j in range(seg):
            a = i * seg + j; b = i * seg + (j + 1) % seg
            fs.append((a, b, b + seg, a + seg))
    for j in range(seg):
        fs.append((top, (j + 1) % seg, j))
        fs.append((bot, (rings - 2) * seg + j, (rings - 2) * seg + (j + 1) % seg))
    o = g.mesh(name, vs, fs, role)
    return o, rad


def surface_point(p, radius_fn, d, stretch=(1, 1, 1)):
    d = Vector(d).normalized(); q = d * radius_fn(d)
    return Vector(p) + Vector((q.x * stretch[0], q.y * stretch[1], q.z * stretch[2]))


def capsule_segment(name, a, b, r0, r1=None, role='structure', sides=20, flat=1.0, up=None):
    """Rounded finger-like segment between two joint centres (closed, domed ends).
    flat < 1 compresses the section along the frame's second axis (v);
    up fixes that axis (e.g. the palm normal) instead of the automatic frame."""
    a, b = Vector(a), Vector(b); r1 = r0 if r1 is None else r1
    d, u, v = _frame(b - a)
    if up is not None:
        v = (Vector(up) - d * Vector(up).dot(d)).normalized(); u = v.cross(d)
    L = (b - a).length; n = 6
    head = [(-r0 * math.cos(math.pi / 2 * k / n), max(.01, r0 * math.sin(math.pi / 2 * k / n))) for k in range(n + 1)]
    body = [(L * s, r0 + (r1 - r0) * s) for s in (.25, .5, .75)]
    tail = [(L + r1 * math.sin(math.pi / 2 * k / n), max(.01, r1 * math.cos(math.pi / 2 * k / n))) for k in range(n + 1)]
    prof = head + body + tail
    vs = []; fs = []
    for x, r in prof:
        for j in range(sides):
            ang = T * j / sides
            vs.append(a + d * x + r * (math.cos(ang) * u + flat * math.sin(ang) * v))
    m = len(prof)
    for i in range(m - 1):
        for j in range(sides):
            fs.append((i * sides + j, i * sides + (j + 1) % sides, (i + 1) * sides + (j + 1) % sides, (i + 1) * sides + j))
    fs.append(tuple(reversed(range(sides))))
    fs.append(tuple((m - 1) * sides + j for j in range(sides)))
    return g.mesh(name, vs, fs, role)


def polyline_ring(name, pts, r=.35, role='detail'):
    g.wire(name, [Vector(p) for p in pts], r, role)


def arc_points(c, r, a0, a1, axis_u=(1, 0, 0), axis_v=(0, 1, 0), n=48):
    c = Vector(c); u = Vector(axis_u); v = Vector(axis_v)
    return [c + r * (math.cos(math.radians(a0 + (a1 - a0) * k / n)) * u + math.sin(math.radians(a0 + (a1 - a0) * k / n)) * v) for k in range(n + 1)]


def frame_matrix(p, axis, ref):
    """4x4 with local Z along axis and local X toward ref (projected)."""
    z = Vector(axis).normalized(); x = Vector(ref)
    x = (x - z * x.dot(z)).normalized(); y = z.cross(x)
    m = Matrix((x, y, z)).transposed().to_4x4(); m.translation = Vector(p)
    return m


def arc_tube(name, p, axis, ref, r, thick, depth, a0=0, a1=360, role='structure', n=None):
    """Ring/tube sector whose angle 0 points toward ref: windows face where intended."""
    full = a1 - a0 >= 359.9
    n = n or max(16, round((a1 - a0) / 4)); cols = n if full else n + 1
    m = frame_matrix(p, axis, ref); vs = []; fs = []
    for z in (0, depth):
        for rr in (r - thick, r):
            for j in range(cols):
                a = math.radians(a0 + (a1 - a0) * j / n)
                vs.append(m @ Vector((rr * math.cos(a), rr * math.sin(a), z)))
    k = cols
    for j in range(n):
        j1 = (j + 1) % cols
        fs.extend([(j, j1, k + j1, k + j), (2 * k + j, 3 * k + j, 3 * k + j1, 2 * k + j1),
                   (j, 2 * k + j, 2 * k + j1, j1), (k + j, k + j1, 3 * k + j1, 3 * k + j)])
    if not full:
        fs.extend([(0, k, 3 * k, 2 * k), (n, n + 2 * k, n + 3 * k, n + k)])
    return g.mesh(name, vs, fs, role)


def proprotor(p, R, blades=3, axis=(0, 0, 1), pitch=14, root_chord=None, tip_chord=None, hub=None, phase=0, role='structure'):
    """Slender tapered blades with an elliptic spinner; blade plane normal to axis."""
    root_chord = root_chord or R * .16; tip_chord = tip_chord or R * .07; hub = hub or R * .1
    m = frame_matrix(p, axis, (1, 0, 0) if abs(Vector(axis).normalized().x) < .9 else (0, 1, 0))
    for k in range(blades):
        a = math.radians(phase) + T * k / blades
        radial = Vector((math.cos(a), math.sin(a), 0)); tang = Vector((-math.sin(a), math.cos(a), 0))
        q = math.radians(pitch)
        chord = (tang * math.cos(q) + Vector((0, 0, -1)) * math.sin(q)).normalized()
        up = radial.cross(chord).normalized()
        o = wing('proprotor blade', radial * hub - chord * root_chord * .3, radial * R - chord * tip_chord * .3,
                 root_chord, tip_chord, chord, up, t=.10, camber=.03, stations=8, role=role)
        o.matrix_world = m @ o.matrix_world
        c = cyl_local('blade root cuff', radial * hub * .9, R * .035, hub * .6, radial, 'detail')
        c.matrix_world = m @ c.matrix_world
    s_ = sphere('rotor spinner', (0, 0, 0), hub * 1.05, role, 24, 12, (1, 1, 1.5))
    s_.matrix_world = m @ s_.matrix_world


def cyl_local(name, p, r, h, axis, role='detail', n=20):
    o = g.cyl(name, 0, 0, 0, r, h, role, n)
    o.matrix_world = Matrix.Translation(Vector(p)) @ Vector(axis).to_track_quat('Z', 'Y').to_matrix().to_4x4()
    return o
