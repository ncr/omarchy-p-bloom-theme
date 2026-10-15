"""QUIET SCANNER: open, silent low-field head MRI with a hammock bed under a canopy of stars.

Units: centimetres. X along the bed (head end +X), Y across (-Y is the open
front toward the viewer, the parent sits at +Y facing the child), Z up.
Like today's portable low-field scanners it images the head only. The magnet
is one smooth crescent: two flat arms whose inner faces are the pole faces
(lower face z = 48, upper face z = 88, a 40 cm gap around the head), joined
behind the head by a rounded back, standing on one plinth. The child lies in
a fabric hammock hung by straps from two slim end frames; the head rests on
a pillow cradle on the lower pole face. The gradient plate (B) sits inside
the upper arm. Above the head end an arched canopy on two slender posts
carries the fibre-optic stars (C); its front half is cut away in the
drawing so the magnet stays visible.
"""
from ..kit import *
from .parts import loft, sphere
import family_core as fc

HX = 70.0            # head / magnet axis station
LZ, UZ = 42.0, 94.0  # centre heights of the lower and upper arms (12 cm thick)


def se(a, rx, ry, e=.65):
    c, s_ = math.cos(a), math.sin(a)
    return rx * math.copysign(abs(c) ** e, c), ry * math.copysign(abs(s_) ** e, s_)


def band(name, path, width, thick, role='structure', n=28, u=(0, 1, 0)):
    """Loft along a path in a plane normal to u, rounded-rectangle section:
    'width' along u and 'thick' in the plane, both functions of t in [0, 1]."""
    pts = [Vector(p) for p in curve(path, 14)]
    vs = []; fs = []; m = len(pts)
    uu = Vector(u)
    for i, p in enumerate(pts):
        t = i / (m - 1)
        tg = (pts[min(i + 1, m - 1)] - pts[max(i - 1, 0)]).normalized()
        v = tg.cross(uu).normalized()
        w = width(t) / 2; th = thick(t) / 2
        for k in range(n):
            x_, y_ = se(T * k / n, w, th, .5)
            vs.append(p + uu * x_ + v * y_)
    for i in range(m - 1):
        for k in range(n):
            fs.append((i * n + k, i * n + (k + 1) % n, (i + 1) * n + (k + 1) % n, (i + 1) * n + k))
    fs.append(tuple(reversed(range(n)))); fs.append(tuple((m - 1) * n + k for k in range(n)))
    return g.mesh(name, vs, fs, role)


def end_round(t, e=.07):
    """Rounds the ends of a band: 1 in the middle, easing to .45 at t = 0 and 1."""
    d = max(0.0, (abs(2 * t - 1) - (1 - 2 * e)) / (2 * e))
    return .45 + .55 * math.sqrt(max(0.0, 1 - d * d))


def magnet():
    path = [(HX - 26, 0, LZ), (HX, 0, LZ), (HX + 24, 0, LZ + 1), (HX + 46, 0, LZ + 9), (HX + 56, 0, (LZ + UZ) / 2),
            (HX + 46, 0, UZ - 9), (HX + 24, 0, UZ - 1), (HX, 0, UZ), (HX - 26, 0, UZ)]
    band('crescent magnet', path,
         lambda t: (52 - 16 * math.sin(math.pi * t) ** 2) * end_round(t, .05),
         lambda t: (12 + 8 * math.sin(math.pi * t) ** 2) * end_round(t))
    # Pole faces: shallow rounded shoes on both inner faces, with an accent rim.
    for z0, z1, zr in ((LZ + 5.8, LZ + 8, LZ + 8.3), (UZ - 5.8, UZ - 8, UZ - 8.3)):
        with at((HX, 0, 0)):
            fc.casting('pole face', [(z0, 21, 19), (z1, 20, 18)])
        tube('pole face rim', [(HX + se(T * k / 120, 18.5, 16.5)[0], se(T * k / 120, 18.5, 16.5)[1], zr) for k in range(121)], .25, 'accent')
    # One plinth, rising in one piece under the back of the lower arm.
    with at((HX + 18, 0, 0)):
        fc.casting('magnet plinth', [(0, 44, 36), (2.5, 46, 38), (8, 46, 38), (11, 40, 33), (16, 24, 20), (LZ - 6, 18, 16), (LZ - 4, 20, 18)])
        fc.trim('plinth bead', 5.2, 46.6, 38.6)


def hammock(x0=-78, x1=38, zf=74, zh=60, sag=16, half=25, n=(56, 16)):
    """Fabric sling: gathered at the foot, on a padded spreader at the head;
    catenary sag along the length and edges curling up into a trough."""
    nx, ny = n; vs = []; fs = []

    def P(u, v):
        x = x0 + (x1 - x0) * u
        w = half * (math.sin(math.pi / 2 * min(1, u / .38)) ** .8 * .88 + .12)
        z = zf + (zh - zf) * u - sag * math.sin(math.pi * u) ** 1.2 + 7 * v * v * (w / half)
        return Vector((x, w * v, z))
    for i in range(nx + 1):
        for j in range(ny + 1):
            vs.append(P(i / nx, -1 + 2 * j / ny))
    for i in range(nx):
        for j in range(ny):
            a = i * (ny + 1) + j
            fs.append((a, a + 1, a + ny + 2, a + ny + 1))
    g.mesh('hammock sling', vs, fs, 'structure')
    for v in (-1, 1):
        tube('sling hem', [P(k / 80, v) for k in range(81)], .3, 'structure')
    for u in (.3, .55, .8):
        tube('sling seam', [P(u, -1 + 2 * k / 30) for k in range(31)], .12, 'detail')
    return P


def end_frame(x, top, legy=36, topy=26):
    """Slim inverted-U frame in the YZ plane standing on the rug."""
    pts = [(x, -legy, 0), (x, -legy + 2, top * .55), (x, -topy, top - 4), (x, -topy + 6, top), (x, topy - 6, top),
           (x, topy, top - 4), (x, legy - 2, top * .55), (x, legy, 0)]
    loft('end frame', pts, 1.6, 14)
    for y in (-legy, legy):
        cyl('frame foot', (x, y, 0), 4, 1.6, 'detail', (0, 0, 1), 24)


def canopy():
    """Arched star canopy over the head end: back half drawn, front cut away."""
    cy, cz, ry, rz = 6.0, 108.0, 52.0, 42.0
    xs = (-26.0, 96.0)

    def A(x, th, off=0.0):
        return Vector((x, cy + (ry + off) * math.cos(th), cz + (rz + off) * math.sin(th)))
    ths = [math.radians(8 + 100 * k / 40) for k in range(41)]
    vs = []; fs = []
    nx = 24
    for i, th in enumerate(ths):
        for j in range(nx + 1):
            vs.append(A(xs[0] + (xs[1] - xs[0]) * j / nx, th))
    for i in range(len(ths) - 1):
        for j in range(nx):
            a = i * (nx + 1) + j
            fs.append((a, a + nx + 1, a + nx + 2, a + 1))
    g.mesh('star canopy', vs, fs, 'structure')
    tube('canopy cut edge', [A(xs[0] + (xs[1] - xs[0]) * k / 40, ths[-1], .2) for k in range(41)], .35, 'structure')
    for x in xs:
        tube('canopy rib', [A(x, th, .3) for th in ths], .5, 'structure')
    # Two slender posts from the rug to the canopy foot.
    for x in xs:
        p = A(x, ths[0])
        loft('canopy post', [(x, p.y + 1, 0), (x, p.y, p.z * .6), (x, p.y - .4, p.z)], lambda t: 1.8 - .5 * t, 14)
        cyl('post foot', (x, p.y + 1, 0), 5, 1.6, 'detail', (0, 0, 1), 24)
    # Fibre-optic stars on the underside, and two constellations.
    import random
    rnd = random.Random(20)
    for k in range(46):
        x = rnd.uniform(xs[0] + 4, xs[1] - 4); th = math.radians(rnd.uniform(14, 100))
        sphere('fibre star', A(x, th, -.7), rnd.choice((.45, .6, .8)), 'accent', 8, 4)
    for pts in ([(-6, 30), (6, 38), (20, 36), (28, 46), (18, 56)], [(56, 62), (66, 54), (78, 58), (86, 70)]):
        P = [A(x, math.radians(d), -.8) for x, d in pts]
        for a, b in zip(P, P[1:]):
            tube('constellation line', [a, b], .1, 'detail')
        for p in P:
            sphere('constellation star', p, 1.0, 'accent', 10, 6)
    # Dawn light strip along the canopy foot, noise-sensing loops on the top.
    tube('dawn light strip', [A(xs[0] + 3 + (xs[1] - xs[0] - 6) * k / 30, math.radians(12), -.8) for k in range(31)], .35, 'cable')
    for xc in (10, 66):
        c = A(xc, math.radians(72), 1.0)
        tube('noise-sensing loop', [c + Vector((9 * math.cos(T * k / 48), 0, 0)) + (A(xc, math.radians(72 + 9 * math.sin(T * k / 48)), 1.0) - A(xc, math.radians(72), 1.0)) for k in range(49)], .3, 'cable')
    return A


def build():
    views(B=(24, -38), C=(20, -22))
    # Rug: the floor the frames, chair and plinth stand on.
    with at((18, 18, 0)):
        fc.casting('rug', [(0, 128, 80), (.8, 128, 80)])
        fc.trim('rug border', 1.0, 119, 72)
    magnet()
    # --- B: gradient plate inside the upper arm ------------------------------------
    with group('B'):
        zb = UZ - 3.0
        with at((HX, 0, 0)):
            fc.casting('gradient plate', [(zb - 1.2, 21, 19.5), (zb, 22.5, 21), (zb + 2.4, 22.5, 21), (zb + 3.4, 21, 19.5)])
        for cx in (-9, 9):
            pts = []
            for k in range(0, 721, 4):
                a = math.radians(k) * (1 if cx < 0 else -1); r = 1.4 + 6.8 * k / 720
                pts.append((HX + cx + r * math.cos(a), r * .9 * math.sin(a), zb - 1.3))
            tube('transverse gradient winding', pts, .08, 'cable')
        for r in (17.8, 19.3, 20.6):
            tube('axial gradient loop', [(HX + se(T * k / 120, r, r * .92)[0], se(T * k / 120, r, r * .92)[1], zb - 1.3) for k in range(121)], .08, 'accent')
        for k in range(6):
            a = T * (k + .5) / 6; x_, y_ = se(a, 25.2, 23.4)
            xi, yi = se(a, 21.6, 20.0)
            box('mount lug', (HX + (x_ + xi) / 2, (y_ + yi) / 2, zb + 1.2), (abs(x_ - xi) + 3, abs(y_ - yi) + 3, 2.2), .6, 'structure')
            cyl('damping mount', (HX + x_, y_, zb - .8), 1.5, 5.2, 'structure', (0, 0, 1), 20)
            ring('elastomer ring', (HX + x_, y_, zb + 1.2), 2.0, .55, 1.4, (0, 0, 1), 'accent')
        tube('coolant loop', [(HX - 19, 0, zb + 3.6), (HX - 19, 8, zb + 3.6), (HX - 12, 14, zb + 3.6), (HX + 12, 14, zb + 3.6), (HX + 19, 8, zb + 3.6), (HX + 19, 0, zb + 3.6)], .3, 'cable')
    # --- the hammock, its frames and straps ---------------------------------------
    P = hammock()
    end_frame(-96, 96)
    end_frame(30, 90)
    foot = P(0, 0)
    ring('gather ring', foot, 2.2, .5, .8, (1, 0, 0), 'accent')
    tube('foot strap', [foot, (-92, 0, 94)], .45, 'cable')
    rod('head spreader', P(1, -1) + Vector((0, -1.5, 0)), P(1, 1) + Vector((0, 1.5, 0)), 1.4)
    for v in (-1, 1):
        tube('head strap', [P(1, v) + Vector((0, 1.5 * v, 0)), (30, 20 * v, 90)], .45, 'cable')
    # Pillow cradle on the lower pole face, a hollow for the head.
    fc.softbox('pillow cradle', (HX - 4, 0, LZ + 11), (34, 30, 6), 2.8, 'structure')
    for v in (-1, 1):
        fc.softbox('cradle bolster', (HX - 4, v * 12, LZ + 15.5), (30, 6, 5), 2.4, 'structure')
    with group('C'):
        A = canopy()
    # Parent's chair at the head end, far side, facing the child.
    with at((2, 66, 0), 0):
        box('chair seat', (0, 0, 44), (46, 44, 7), 3)
        box('chair back', (0, 20, 72), (46, 6, 46), 3)
        for side in (-1, 1):
            box('chair arm', (side * 21, -2, 62), (5, 40, 4), 1.8)
            rod('chair arm post', (side * 21, -16, 47), (side * 21, -16, 60), 1.2)
        for sx in (-1, 1):
            for sy in (-1, 1):
                rod('chair leg', (sx * 18, sy * 17, 41), (sx * 20, sy * 19, 0), 1.6)
    loft('hand loop', [P(.82, 1), (32, 30, 58), (34, 33, 55), (36, 30, 58), P(.9, 1)], .6, 10, 'detail')
    mark('CRESCENT MAGNET', (HX + 57, -14, (LZ + UZ) / 2), 'ONE PERMANENT MAGNET / 0.07 T / NO HELIUM')
    mark('POLE FACES', (HX - 16, -14, LZ + 8.3), '40 cm APART / THE HEAD RESTS BETWEEN THEM')
    mark('STAR CANOPY', A(50, math.radians(40), -.8), 'FIBRE-OPTIC SKY ABOVE THE HEAD END')
    mark('HAMMOCK', P(.4, -1), '140 cm SLING / THE BODY STAYS OUTSIDE THE MAGNET')
    mark("PARENT'S CHAIR", (2 - 21, 64, 64), 'AT THE HEAD END / A HAND IN REACH')
    mark('END FRAMES', (-96, -36, 20), 'STRAPS, NOT RAILS / THE BED LIFTS OUT')
    return 22, 16
