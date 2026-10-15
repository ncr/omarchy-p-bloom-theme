"""CRATER EAR: a kilometre wire-mesh dish hung in a far-side lunar crater.

Units: 1 unit = 1 m. Crater: rim crest radius 700 m at z = +35, floor
radius 350 m at z = -300, terraced inner wall, outer apron to r ~ 1000.
Dish: paraboloid z = -270 + r^2 / (4 f), f = 250 m, radius 500 m (1 km),
so the rim of the mesh sits at z = -20 and the focus at z = -20. Mesh
every 40 cm in reality; drawn every 50 m radially and every 10 degrees.
24 anchor cables from the mesh rim to rim anchors at r = 735 m; three
tensioning climbers ride them. Receiver: a 96 m triangular platform with a
36 m cabin drum at the focus, on three cables from 130 m rim masts with
back-stays. Ejecta apron with broken rays and secondary craters out to an
irregular edge (~1.1 km radius). Lander with relay antenna
on the rim. Wall slopes stay below the 40-degree camera elevation so the
single terrain surface never needs to hide its own far edges.
"""
import random
from ..kit import *
from .parts import loft, sphere, lumpy

F = 250
Z0 = -270
RD = 500
RIM = 770
PYLONS = (90, 210, 330)
CLIMB = (255, 285, 345)
rnd = random.Random(21)
BUMPS = [(rnd.uniform(0, T), rnd.randint(3, 9), rnd.uniform(2, 7)) for _ in range(9)]


def profile(r):
    """Terraced crater profile z(r), metres."""
    pts = [(0, -300), (330, -300), (372, -262), (420, -252), (468, -200), (515, -190),
           (565, -135), (615, -125), (672, -48), (720, -36), (770, 35), (830, 20), (900, -4), (1010, -14), (1400, -22)]
    for (r0, z0), (r1, z1) in zip(pts, pts[1:]):
        if r <= r1:
            t = (r - r0) / (r1 - r0)
            t = t * t * (3 - 2 * t) if r0 >= 720 or r1 <= 330 else t
            return z0 + (z1 - z0) * t
    return pts[-1][1]


def height(r, a):
    z = profile(r)
    w = min(1, max(0, (r - 300) / 120)) * min(1, max(0, (1350 - r) / 260))
    for ph, k, amp in BUMPS:
        z += w * amp * math.sin(k * a + ph) * math.cos(r / 90 + ph)
    return z


def edge_radius(a):
    return 1010 + 60 * math.sin(3 * a + .7) + 34 * math.sin(5 * a + 1.9) + 18 * math.sin(11 * a + .3)


BANDS = (0, 330, 420, 515, 615, 720, 770, None)


def terrain():
    """Terrain as ring bands split at the terrace edges: each band occludes the
    others, and the band boundaries draw the terrace lines exactly."""
    na = 240
    for r0, r1 in zip(BANDS, BANDS[1:]):
        nr = 24 if r0 == 0 else 12
        vs = []; fs = []
        for i in range(nr + 1):
            for j in range(na):
                a = T * j / na
                ro = edge_radius(a) if r1 is None else r1
                r = r0 + (ro - r0) * i / nr
                vs.append((r * math.cos(a), r * math.sin(a), height(r, a)))
        for i in range(nr):
            for j in range(na):
                p = i * na + j; q = i * na + (j + 1) % na
                fs.append((p, q, q + na, p + na))
        g.mesh('crater terrain band', vs, fs, 'shell')


SECONDARIES = ((905, 205, 26), (950, 320, 18), (890, 20, 15), (930, 110, 22), (920, 262, 13), (975, 170, 11))


def ejecta():
    """Ejecta blanket: broken radial rays that thin out toward the edge."""
    for k in range(260):
        a = T * ((k * 0.61803) % 1)
        ray = abs(math.sin(4 * a + 1.1)) ** 3 + .35 * abs(math.sin(9 * a + .4))
        if ((k * 29) % 13) / 13 > ray:
            continue
        r0 = 880 + 60 * ((k * 37) % 7) / 7
        L = 40 + 110 * ray * ((k * 17) % 5) / 5
        r1 = min(r0 + L, edge_radius(a) - 25)
        if r1 - r0 < 15:
            continue
        pts = [(r * math.cos(a), r * math.sin(a), height(r, a) + .6) for r in (r0, (r0 + r1) / 2, r1)]
        tube('ejecta ray', pts, .2, 'shell')


def secondary(r, a_deg, rad):
    """Small secondary crater on the apron: broken raised rim, shaded inner wall."""
    a = math.radians(a_deg); c = Vector((r * math.cos(a), r * math.sin(a), 0))
    gap = (a_deg * 7) % 360
    pts = []
    for k in range(73):
        q = math.radians(gap + 30 + 300 * k / 72)
        rr = rad * (1 + .09 * math.sin(3 * q + a_deg) + .05 * math.sin(5 * q))
        x, y = c.x + rr * math.cos(q), c.y + rr * math.sin(q)
        pts.append((x, y, height(math.hypot(x, y), math.atan2(y, x)) + 1.0))
    tube('secondary crater rim', pts, .35, 'detail')
    for k in range(9):
        q = math.radians(a_deg + 110 + 14 * k)
        x0, y0 = c.x + rad * .92 * math.cos(q), c.y + rad * .92 * math.sin(q)
        x1, y1 = c.x + rad * .55 * math.cos(q), c.y + rad * .55 * math.sin(q)
        tube('crater wall hachure', [(x0, y0, height(math.hypot(x0, y0), math.atan2(y0, x0)) + .8),
                                      (x1, y1, height(math.hypot(x1, y1), math.atan2(y1, x1)) + .8)], .18, 'shell')


def contour(name, r, role='detail', lift=.6, a0=0, a1=T):
    pts = []
    for k in range(361):
        a = a0 + (a1 - a0) * k / 360
        pts.append((r * math.cos(a), r * math.sin(a), height(r, a) + lift))
    tube(name, pts, .5, role)


def hachures():
    """Fall-line hachures: short strokes down the steep bands, longer where steeper."""
    bands = ((332, 370, 1.5), (422, 466, 1.5), (517, 563, 1.5), (617, 670, 1.5), (722, 768, 1.5), (775, 860, 3.0))
    for r0, r1, step in bands:
        k = 0
        a_deg = 0.0
        while a_deg < 360:
            a = math.radians(a_deg)
            jit = ((k * 37) % 11) / 11
            ra = r0 + (r1 - r0) * .08 * jit
            rb = r1 - (r1 - r0) * (.15 + .35 * ((k * 53) % 7) / 7) if r0 < 770 else r0 + (r1 - r0) * (.35 + .5 * ((k * 29) % 5) / 5)
            pts = [(r * math.cos(a), r * math.sin(a), height(r, a) + .6) for r in (ra, (ra + rb) / 2, rb)]
            tube('fall-line hachure', pts, .2, 'shell')
            a_deg += step * (1 + .35 * jit); k += 1


def dish_z(r):
    return Z0 + r * r / (4 * F)


MAST = 130


def pylon(a_deg):
    """Tapered mast on the rim with a back-stay to a ground anchor."""
    a = math.radians(a_deg); er = Vector((math.cos(a), math.sin(a), 0))
    base = er * 800 + Vector((0, 0, height(800, a)))
    top = base + Vector((0, 0, MAST))
    box('mast footing', base + Vector((0, 0, 1)), (26, 26, 6), 2)
    loft('rim mast', [base + Vector((0, 0, 3)), top], lambda t: 9 - 6.5 * t, 20, 'structure', False)
    for h in (40, 80):
        ring('mast collar', base + Vector((0, 0, h)), 9 - 6.5 * h / MAST + 1.0, 1.2, 2.5, (0, 0, 1), 'detail')
    box('mast head', top + Vector((0, 0, 3)), (9, 9, 7), 1.5)
    stay = er * 900
    stay = stay + Vector((0, 0, height(900, a)))
    tube('back-stay', [top + Vector((0, 0, 2)), stay + Vector((0, 0, 2))], .6, 'cable')
    box('stay anchor', stay + Vector((0, 0, 1)), (12, 12, 5), 1.5)
    return top + Vector((0, 0, 4))


PLAT = 48


def cabin(p):
    """Receiver at the focus: triangular platform, cabin drum, feed looking down."""
    b = len(g.parts); w = len(g.wires)
    corners = [Vector((PLAT * math.cos(math.radians(a)), PLAT * math.sin(math.radians(a)), 20)) for a in PYLONS]
    for c0, c1 in zip(corners, corners[1:] + corners[:1]):
        loft('platform girder', [c0, c1], 2.2, 12, 'structure', False)
    for c in corners:
        box('winch pod', c + Vector((0, 0, 2.5)), (8, 8, 5), 1.2)
        cyl('winch drum', c + Vector((0, 0, 6)), 2.2, 4, 'detail', (0, 0, 1), 20)
        rod('hanger strut', c, (c.x * .3, c.y * .3, 14), 1.2)
    cyl('cabin drum', (0, 0, -14), 18, 28, 'structure', (0, 0, 1), 48)
    for z in (-14, 14):
        ring('cabin rim band', (0, 0, z - .8), 18.6, 1.2, 1.6, (0, 0, 1), 'detail')
    ring('cabin panel seam', (0, 0, 0), 18.1, .4, .4, (0, 0, 1), 'detail')
    # Feed: a flared horn and a crossed dipole cluster for 5-40 MHz.
    loft('feed horn', [(0, 0, -14), (0, 0, -22), (0, 0, -29)], lambda t: 6 + 9 * t * t, 32, 'accent', False)
    for a in range(0, 180, 45):
        q = math.radians(a)
        rod('crossed dipole arm', (-20 * math.cos(q), -20 * math.sin(q), -31), (20 * math.cos(q), 20 * math.sin(q), -31), .5, 'accent')
    for a in (30, 150, 270):
        q = math.radians(a); er = Vector((math.cos(q), math.sin(q), 0))
        box('radiator panel', er * 19, (1.4, 16, 20), .4, 'detail')
    box('electronics hatch', (0, -18, -2), (10, .5, 14), .6, 'detail')
    sphere('star tracker', (0, 0, 16), 2.4, 'detail', 16, 8)
    transform(b, w, Matrix.Translation(p))


def climber(p, d):
    """Tensioning robot riding an anchor cable (d = cable direction)."""
    d = Vector(d).normalized(); side = d.cross(Vector((0, 0, 1))).normalized(); up = side.cross(d)
    m = Matrix((d, side, up)).transposed().to_4x4(); m.translation = Vector(p)
    b = len(g.parts); w = len(g.wires)
    box('climber body', (0, 0, 2.2), (7, 3.4, 2.6), .7)
    for x in (-2.6, 2.6):
        for y in (-1.2, 1.2):
            cyl('drive sheave', (x, y, 0), 1.1, .6, 'detail', (0, 1 if y > 0 else -1, 0), 24)
    box('solar deck', (0, 0, 3.9), (6.2, 4.4, .25), .1, 'accent')
    rod('gripper arm', (-3.4, 0, 1.3), (-4.4, 0, 0), .35, 'detail')
    rod('gripper arm', (3.4, 0, 1.3), (4.4, 0, 0), .35, 'detail')
    transform(b, w, m)


def build():
    views(B=(24, 18), C=(-40, 28))
    terrain()
    contour('rim crest', RIM, 'structure', 1.0)
    ejecta()
    for r, a, rad in SECONDARIES:
        secondary(r, a, rad)
    hachures()
    # Boulders on the floor, the wall and the rim.
    for i, (r, a, s_) in enumerate(((150, 40, 14), (240, 150, 10), (300, 250, 12), (420, 20, 9),
                                     (520, 115, 11), (820, 190, 16), (860, 300, 12), (805, 60, 10),
                                     (940, 240, 13), (960, 80, 11), (935, 350, 15), (975, 140, 9))):
        q = math.radians(a)
        lumpy('boulder', (r * math.cos(q), r * math.sin(q), height(r, q) + s_ * .45), s_, seed=i + 3,
              stretch=(1, .9, .6), seg=24, rings=12)
    # Dish: mesh rings and radials, heavy rim cable.
    for r in range(50, RD, 50):
        tube('mesh ring', [(r * math.cos(T * k / 240), r * math.sin(T * k / 240), dish_z(r)) for k in range(241)], .3, 'accent')
    for k in range(36):
        a = T * k / 36
        tube('mesh radial', [(r * math.cos(a), r * math.sin(a), dish_z(r)) for r in range(25, RD + 1, 25)], .25, 'detail')
    loft('dish rim cable', [(RD * math.cos(T * k / 240), RD * math.sin(T * k / 240), dish_z(RD)) for k in range(241)], 1.6, 10, 'structure', False)
    # 24 anchor cables to the rim; anchor blocks sit on the crest.
    anchors = {}
    for k in range(24):
        a_deg = k * 15; a = math.radians(a_deg)
        er = Vector((math.cos(a), math.sin(a), 0))
        p0 = er * RD + Vector((0, 0, dish_z(RD)))
        p1 = er * 790 + Vector((0, 0, height(790, a) + 3))
        anchors[a_deg] = (p0, p1)
        tube('anchor cable', [p0, p1], .4, 'cable')
        if a_deg != CLIMB[0]:
            box('rim anchor block', p1 + Vector((0, 0, -1)), (9, 9, 6), 1.2)
    # Receiver cabin on three cables from the pylons.
    focus = Vector((0, 0, Z0 + F))
    with group('B'):
        cabin(focus)
    tops = [pylon(a) for a in PYLONS]
    for a, top in zip(PYLONS, tops):
        q = math.radians(a); er = Vector((math.cos(q), math.sin(q), 0))
        loft('cabin suspension cable', [top, focus + er * PLAT + Vector((0, 0, 25))], 1.0, 8, 'structure', False)
    mark('RECEIVER CABIN', focus + Vector((0, -18, -6)), 'HANGS AT THE FOCUS / 250 m ABOVE THE MESH')
    # Climbers on three anchor cables; C shows the first with its anchor.
    for i, a_deg in enumerate(CLIMB):
        p0, p1 = anchors[a_deg]
        grp = group('C') if i == 0 else None
        if grp:
            with grp:
                climber(p0.lerp(p1, .93), p1 - p0)
                a = math.radians(a_deg); er = Vector((math.cos(a), math.sin(a), 0)); et = Vector((-math.sin(a), math.cos(a), 0))
                box('rim anchor block', p1 + Vector((0, 0, -1.5)), (11, 10, 5), 1.2)
                for s_ in (-1, 1):
                    box('ballast bag', p1 + et * (8 * s_) + Vector((0, 0, -2)), (5, 5, 3), 1.4, 'detail')
                box('anchor tensioner', p1 + Vector((0, 0, 3.5)), (6, 5, 3), .8, 'detail')
                cyl('tensioner drum', p1 + Vector((-2.2, -2.8, 3.5)) , 1.3, 5.6, 'detail', tuple(et), 20)
                tube('anchor cable segment', [p0.lerp(p1, .86), p1], .4, 'cable')
            mark('ANCHOR CLIMBER', p0.lerp(p1, .93) + Vector((0, 0, 4)), 'WALKS THE CABLES / TRIMS THE MESH TO 1 cm')
        else:
            climber(p0.lerp(p1, .55), p1 - p0)
    # Lander with relay antenna on the rim, between two pylons.
    a = math.radians(150); er = Vector((math.cos(a), math.sin(a), 0))
    lp = er * 870 + Vector((0, 0, height(870, a)))
    with at(lp):
        cyl('lander body', (0, 0, 4), 5, 5, 'structure', (0, 0, 1), 8)
        for k in range(4):
            q = T * k / 4 + .4
            rod('lander leg', (4 * math.cos(q), 4 * math.sin(q), 5), (8 * math.cos(q), 8 * math.sin(q), 0), .45)
            cyl('footpad', (8 * math.cos(q), 8 * math.sin(q), -.3), 1.2, .5, 'detail', (0, 0, 1), 12)
        rod('relay mast', (0, 0, 9), (0, 0, 16), .4)
        loft('relay dish', [(0, 0, 15.5), (0, 0, 17.5)], lambda t: .6 + 3.4 * t, 32, 'accent', False)
        box('lander solar wing', (7, 0, 8), (8, 3, .3), .1, 'detail')
    mark('LANDER AND RELAY', lp + Vector((0, 0, 14)), 'PARKED ON THE CRATER RIM')
    mark('WIRE MESH DISH', Vector((300 * math.cos(math.radians(240)), 300 * math.sin(math.radians(240)), dish_z(300))),
         '1 km ACROSS / WIRES EVERY 40 cm')
    top = tops[0]
    mark('RIM MAST', top, 'THREE MASTS / 130 m / HOLD THE CABIN')
    mark('CRATER RIM', Vector((RIM * math.cos(math.radians(30)), RIM * math.sin(math.radians(30)), height(RIM, math.radians(30)) + 1)), '1.4 km ACROSS / 335 m DEEP')
    return 20, 50
