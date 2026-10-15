"""GREEN FORGE: hydrogen direct-reduction shaft furnace with its arc furnace.

Units: 1 unit = 0.5 m. Z up from grade. The hero is the shaft furnace at the
origin: 7 m reduction-zone inner diameter (shell r 7.5 u), top at 47 m, in a
four-column steel frame (15 x 15 m) with platforms, handrails and a stair.
Around it: the inclined charging gallery (pellets to the top hopper), the
electric gas heater and bustle main (hot hydrogen at ~900 C), the enclosed
hot-DRI conveyor to a 150 t electric arc furnace, two hydrogen spheres and
the open electrolyser hall (two rows of six stacks). The top gas leaves as
steam through the scrubber and the slender stack.
Group B: the furnace shell sector facing the B camera is omitted to show
lining, pellet burden, gas paths, bustle tuyeres and cooling cone.
Group C: one electrolyser stack on its service skid in front of the hall.
"""
from ..kit import *
from .parts import loft, sphere, arc_tube, dome

CUT = (20, 110)          # shell sector (degrees) omitted in B, faces +Y/-X


def revolve(name, profile, a0=0, a1=360, n=None, role='structure', c=(0, 0, 0)):
    """Surface of revolution about Z through c: profile [(z, r)], optional sector."""
    full = a1 - a0 >= 359.9
    n = n or max(12, round((a1 - a0) / 5)); cols = n if full else n + 1
    vs = []; fs = []
    for z, r in profile:
        for j in range(cols):
            a = math.radians(a0 + (a1 - a0) * j / n)
            vs.append(Vector((c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2] + z)))
    for i in range(len(profile) - 1):
        for j in range(n):
            a = i * cols + j; b = i * cols + (j + 1) % cols
            fs.append((a, b, b + cols, a + cols))
    return g.mesh(name, vs, fs, role)


SHELL = [(18, 2.2), (21, 2.6), (24, 4.2), (30, 5.8), (34, 6.2), (44, 6.2), (48, 7.0), (52, 7.5),
         (80, 7.5), (86, 6.6), (90, 5.2), (93, 3.4), (94.5, 2.2)]


def handrail(pts, h=2.2, post=4):
    pts = [Vector(p) for p in pts]
    g.wire('handrail', [p + Vector((0, 0, h)) for p in pts], .12, 'detail')
    g.wire('knee rail', [p + Vector((0, 0, h * .5)) for p in pts], .08, 'detail')
    for a, b in zip(pts, pts[1:]):
        k = max(1, int((b - a).length / post))
        for j in range(k):
            q = a.lerp(b, j / k)
            rod('handrail post', q, q + Vector((0, 0, h)), .12, 'detail')


def platform(z, half=15, hole=8.4):
    """Square grating ring around the vessel: four strips, toe plates, handrail."""
    w = half - hole
    for sx, sy, lx, ly in ((0, half - w / 2, 2 * half, w), (0, -half + w / 2, 2 * half, w),
                           (half - w / 2, 0, w, 2 * hole), (-half + w / 2, 0, w, 2 * hole)):
        box('platform grating', (sx, sy, z), (lx, ly, .5), .15, 'detail')
    handrail([(-half, -half, z + .25), (half, -half, z + .25), (half, half, z + .25), (-half, half, z + .25), (-half, -half, z + .25)])


def stair(x, y0, z0, z1, direction=1):
    """Straight flight along Y at x: stringers, treads every 0.2 m of rise."""
    run = (z1 - z0) * 1.25
    a = Vector((x, y0, z0)); b = Vector((x, y0 + direction * run, z1))
    for dx in (-1.6, 1.6):
        rod('stair stringer', a + Vector((dx, 0, 0)), b + Vector((dx, 0, 0)), .22, 'structure')
        g.wire('stair handrail', [a + Vector((dx, 0, 2)), b + Vector((dx, 0, 2))], .1, 'detail')
    steps = int((z1 - z0) / .8)
    for k in range(1, steps):
        q = a.lerp(b, k / steps)
        rod('stair tread', q + Vector((-1.6, 0, 0)), q + Vector((1.6, 0, 0)), .12, 'detail')


def electrolyser_stack(p, cells=24, pitch=.45, detailed_role='detail'):
    """Alkaline stack along X: end plates, cells, tie rods, three manifolds."""
    p = Vector(p); L = cells * pitch
    for sx in (-1, 1):
        box('stack end plate', p + Vector((sx * (L / 2 + .6), 0, 0)), (1.2, 5.2, 5.2), .4, 'structure')
    for k in range(cells):
        x = -L / 2 + pitch * (k + .5)
        g.box('electrolyser cell frame', p + Vector((x, 0, 0)), (pitch * .72, 4.4, 4.4), detailed_role)
    for yy in (-2.3, 2.3):
        for zz in (-2.3, 2.3):
            rod('stack tie rod', p + Vector((-L / 2 - 1.6, yy, zz)), p + Vector((L / 2 + 1.6, yy, zz)), .16, 'detail')
            for sx in (-1, 1):
                cyl('tie rod nut', p + Vector((sx * (L / 2 + 1.25), yy, zz)), .32, .35, 'detail', (sx, 0, 0), 6)
    for yy, role, name in ((-1.2, 'accent', 'hydrogen manifold'), (0, 'cable', 'oxygen manifold'), (1.2, 'detail', 'water feed manifold')):
        rod(name, p + Vector((-L / 2 - .6, yy, 2.9)), p + Vector((L / 2 + .6, yy, 2.9)), .32, role)
        rod(name + ' riser', p + Vector((L / 2 + .6, yy, 2.9)), p + Vector((L / 2 + .6, yy, 5.2)), .32, role)
    return L


def build():
    views(B=(160, 26), C=(28, 26))
    # --- hero: shaft furnace in its frame -------------------------------------
    LOW = [p for p in SHELL if p[0] <= 44]; HIGH = [p for p in SHELL if p[0] >= 44]
    revolve('furnace lower shell', LOW)
    cyl('burden feeder', (0, 0, 16), 2.6, 2.2, 'structure', (0, 0, 1), 32)
    cyl('discharge seal leg', (0, 0, 10), 1.4, 6, 'structure', (0, 0, 1), 24)
    ring('shell stiffener', (0, 0, 34), 6.6, .6, .8, (0, 0, 1), 'detail')
    with group('B'):
        a0, a1 = CUT
        revolve('furnace shell', HIGH, a1, a0 + 360)
        revolve('furnace shell cut sector', HIGH, a0, a1)
        # Refractory lining and the pellet burden, visible where the sector is omitted.
        lining = [(z, r - 1.1) for z, r in HIGH[:-2]]
        revolve('refractory lining', lining, a1, a0 + 360, role='detail')
        import random
        rnd = random.Random(1313)
        for k in range(260):
            z = rnd.uniform(46, 85)
            r_in = next(r for zz, r in reversed(lining) if zz <= z) if z >= lining[0][0] else lining[0][1]
            a = rnd.uniform(0, T)
            rr = (r_in - .6) * math.sqrt(rnd.uniform(.02, 1))
            sphere('ore pellet', (rr * math.cos(a), rr * math.sin(a), z), .42, 'detail', 12, 6)
        # Burden stock line: pellets enter at the top as a cone.
        revolve('burden stock line', [(86, 0.3), (84, 5.4)], role='detail')
        # Hot hydrogen rises from the tuyeres through the descending burden.
        for k, a in enumerate((a0 + 18, a0 + 45, a0 + 72)):
            q = math.radians(a)
            pts = [(6.2 * math.cos(q), 6.2 * math.sin(q), 55), (4.5 * math.cos(q + .15), 4.5 * math.sin(q + .15), 64),
                   (3.0 * math.cos(q + .3), 3.0 * math.sin(q + .3), 75), (2.0 * math.cos(q + .45), 2.0 * math.sin(q + .45), 84)]
            tube('reducing gas path', pts, .2, 'accent')
        # Floor of the section: where the burden enters the cooling zone.
        revolve('section floor', [(44.2, 0), (44.2, 5.1)], a0, a1, role='detail')
        # Bustle main and tuyere downcomers (hot hydrogen at ~900 C).
        loft('bustle main', [(11 * math.cos(T * k / 48), 11 * math.sin(T * k / 48), 56) for k in range(49)], 1.5, 16, 'structure', False)
        for k in range(12):
            a = T * (k + .5) / 12
            loft('tuyere downcomer', [(11 * math.cos(a), 11 * math.sin(a), 54.6), (8.6 * math.cos(a), 8.6 * math.sin(a), 53.5), (7.6 * math.cos(a), 7.6 * math.sin(a), 53.5)], .55, 10, 'detail', False)
        for z in (48, 66, 80):
            arc_tube('shell stiffener', (0, 0, z), (0, 0, 1), (1, 0, 0), 7.9, .6, .8, a1 + 1, a0 + 359, 'detail')
        mark('BUSTLE MAIN', (12.4 * math.cos(math.radians(330)), 12.4 * math.sin(math.radians(330)), 56), 'HOT HYDROGEN AT 900 °C / TWELVE TUYERES')
    # Top: seal legs, charging hopper, top-gas off-takes.
    cyl('top cone', (0, 0, 94.5), 2.2, 3, 'structure', (0, 0, 1), 32)
    revolve('charging hopper', [(97.5, 1.6), (101, 5.2), (104, 5.4)], role='structure')
    ring('hopper rim', (0, 0, 104), 5.6, .6, .6, (0, 0, 1), 'detail')
    for a in (150, 330):
        q = math.radians(a)
        loft('top gas off-take', [(4.2 * math.cos(q), 4.2 * math.sin(q), 91), (8 * math.cos(q), 8 * math.sin(q), 96), (13 * math.cos(q), 13 * math.sin(q), 96)], 1.3, 16, 'structure')
    loft('top gas main', [(13 * math.cos(math.radians(150)), 13 * math.sin(math.radians(150)), 96), (-20, 12, 96), (-26, 14, 90), (-27, 15, 80)], 1.6, 16, 'structure')
    # Scrubber (top gas is mostly steam; water is condensed and returned) and stack.
    revolve('top gas scrubber', [(0, 3.8), (60, 3.8), (66, 2.4), (72, 1.2)], c=(-27, 15, 0))
    for z in (12, 30, 48):
        ring('scrubber band', (-27, 15, z), 4.0, .5, .7, (0, 0, 1), 'detail')
    revolve('vapour stack', [(0, 2.0), (118, 1.5)], c=(-36, 6, 0))
    for z in (40, 80, 116):
        ring('stack band', (-36, 6, z), 1.8 - z * .003, .4, .6, (0, 0, 1), 'detail')
    loft('scrubber to stack', [(-27, 15, 70), (-31, 11, 72), (-35, 7, 72)], 1.1, 14, 'structure')
    # Frame: four columns, cross bracing, platforms, stair.
    for x in (-15, 15):
        for y in (-15, 15):
            rod('frame column', (x, y, 0), (x, y, 100), .9, 'structure')
    for z0, z1 in ((0, 34), (34, 56), (56, 84), (84, 100)):
        for x0, y0, x1, y1 in ((-15, 15, 15, 15), (15, -15, 15, 15)):
            rod('frame bracing', (x0, y0, z0), (x1, y1, z1), .35, 'detail')
            rod('frame bracing', (x1, y1, z0), (x0, y0, z1), .35, 'detail')
    for z in (34, 56, 84):
        platform(z)
    platform(100, hole=6)
    stair(18.5, -15, 0, 17, 1); stair(18.5, 6, 17, 34, -1)
    # Ground-level control room with a door (human scale: 2.1 m door).
    box('control room', (8, -26, 3.2), (14, 8, 6.4), .6, 'structure')
    box('control room door', (3, -30.05, 2.1), (2, .1, 4.2), .1, 'detail')
    for x in (7, 10.5, 14):
        box('control room window', (x, -30.05, 4), (2.4, .1, 1.6), .1, 'detail')
    # Charging gallery: pellets rise on a covered belt to the hopper.
    a = Vector((84, 22, 4)); b = Vector((5, 2, 104))
    truss(a, b, 5, 22)
    for t, h in ((.22, None), (.5, None), (.76, None)):
        q = a.lerp(b, t)
        for s_ in (-1, 1):
            rod('gallery trestle leg', (q.x + s_ * 3, q.y + s_ * 1, 0), (q.x, q.y, q.z - 3), .8, 'structure')
    box('pellet transfer house', (87, 23, 5), (10, 9, 10), .6, 'structure')
    # Electric gas heater and hot hydrogen line to the bustle.
    box('electric gas heater', (-24, -18, 12), (9, 9, 24), 1, 'structure')
    for z in (4, 10, 16, 22):
        box('heater bus bar', (-19.4, -18, z), (.4, 6, .6), .1, 'detail')
    loft('hot hydrogen line', [(-24, -18, 24.5), (-24, -18, 40), (-14, -10, 52), (-7.8, -7.8, 56)], 1.1, 14, 'structure')
    # Enclosed hot-DRI conveyor to the arc furnace roof.
    loft('hot DRI conveyor', [(0, 0, 14), (0, 0, 9), (14, -14, 20), (34, -34, 22)], 1.4, 16, 'structure')
    # Arc furnace: shell on rockers, water-cooled roof, three electrodes on arms.
    E = Vector((40, -40, 0))
    revolve('arc furnace shell', [(6, 6.4), (8, 7.4), (14, 7.4), (15, 7.8)], c=E)
    revolve('arc furnace roof', [(15, 7.6), (16.5, 7.0), (18, 4.5), (18.5, 2.4)], c=E)
    for s_ in (-1, 1):
        arc_tube('tilting rocker', E + Vector((0, s_ * 5 - .7, 7)), (0, 1, 0), (0, 0, -1), 7, 1.2, 1.4, -62, 62)
        box('rocker rail', E + Vector((0, s_ * 5.6, .5)), (18, 2, 1), .3, 'detail')
    for k in range(3):
        q = T * k / 3 + .5
        p = E + Vector((2.2 * math.cos(q), 2.2 * math.sin(q), 0))
        cyl('graphite electrode', p + Vector((0, 0, 18)), .75, 14, 'structure', (0, 0, 1), 20)
        rod('electrode arm', p + Vector((0, 0, 28)), E + Vector((13, 0, 28 + k * 1.5)), .6, 'structure')
        box('electrode clamp', p + Vector((0, 0, 28)), (2.2, 2.2, 1.6), .4, 'detail')
    rod('electrode mast', E + Vector((13, 0, 0)), E + Vector((13, 0, 32)), 1.2, 'structure')
    box('furnace transformer', E + Vector((22, 4, 4)), (8, 10, 8), .6, 'structure')
    box('tapping spout', E + Vector((-9, 0, 9)), (5, 2, 1), .4, 'detail')
    # Hydrogen spheres on legs, pipe rack to the heater.
    for c in (Vector((-42, -24, 13)), Vector((-27, -37, 13))):
        sphere('hydrogen sphere', c, 8, 'structure', 48, 24)
        ring('sphere equator band', c, 8.1, .5, .8, (0, 0, 1), 'detail')
        for k in range(8):
            q = T * k / 8
            rod('sphere leg', c + Vector((8 * math.cos(q), 8 * math.sin(q), 0)), c + Vector((8 * math.cos(q), 8 * math.sin(q), -13)), .5, 'structure')
        loft('sphere stair', [c + Vector((6, -6, -13)), c + Vector((8.6, -1, -5)), c + Vector((7, 4.5, 3)), c + Vector((3.5, 6, 7))], .18, 8, 'detail')
    loft('hydrogen rack', [(-36, -32, 6), (-30, -24, 6), (-24, -18, 6)], .7, 12, 'accent')
    # Electrolyser hall: open portal frames, a light roof, two rows of stacks.
    H0 = Vector((24, 58, 0))
    for i in range(5):
        x = H0.x + i * 12
        for y in (-12, 12):
            rod('hall column', (x, H0.y + y, 0), (x, H0.y + y, 14), .6, 'structure')
        rod('hall rafter', (x, H0.y - 12, 14), (x, H0.y, 17), .5, 'structure')
        rod('hall rafter', (x, H0.y + 12, 14), (x, H0.y, 17), .5, 'structure')
    for y, z in ((-12, 14), (0, 17), (12, 14)):
        rod('hall purlin', (H0.x, H0.y + y, z), (H0.x + 48, H0.y + y, z), .35, 'detail')
    for i in range(4):
        for row in (-6, 6):
            electrolyser_stack(H0 + Vector((6 + i * 10.5 - 4, row, 3.2)))
    for row in (-6, 6):
        loft('hydrogen header', [H0 + Vector((-2, row - 1.2, 9)), H0 + Vector((46, row - 1.2, 9))], .45, 10, 'accent', False)
    loft('hydrogen to spheres', [H0 + Vector((-2, -7.2, 9)), (0, 36, 9), (-34, 22, 8), (-48, -4, 7), (-44, -18, 6)], .6, 12, 'accent')
    # --- C: one stack on its service skid in front of the hall ----------------
    with group('C'):
        S = Vector((44, 34, 0))
        box('service skid', S + Vector((0, 0, .6)), (18, 8, 1.2), .3, 'structure')
        for sx in (-7, 7):
            cyl('skid castor', S + Vector((sx, -3, 0)), .6, .6, 'detail', (0, 1, 0), 16)
            cyl('skid castor', S + Vector((sx, 3, 0)), .6, .6, 'detail', (0, 1, 0), 16)
        for sx in (-5, 5):
            box('stack cradle', S + Vector((sx, 0, 2.2)), (1.4, 6, 2), .3, 'detail')
        electrolyser_stack(S + Vector((0, 0, 5.8)))
        for yy, role in ((-1.2, 'accent'), (0, 'cable'), (1.2, 'detail')):
            cyl('manifold flange', S + Vector((5.95, yy, 11)), .6, .3, role, (0, 0, 1), 16)
        box('stack nameplate', S + Vector((0, -2.25, 2.4 + 5.8 - 3.8)), (3, .1, 1.2), .1, 'detail')
        mark('ELECTROLYSER STACK', S + Vector((-6.2, -2.6, 6)), '24 CELLS SHOWN / 12 STACKS IN TWO ROWS')
    uncover('B', 'furnace shell cut sector')
    mark('SHAFT FURNACE', (7.5 * math.cos(math.radians(318)), 7.5 * math.sin(math.radians(318)), 74), 'PELLETS DOWN, HYDROGEN UP / 125 t OF IRON AN HOUR')
    mark('CHARGING GALLERY', tuple(a.lerp(b, .38) + Vector((0, -2.5, 2.5))), 'PELLETS RISE 50 m TO THE HOPPER')
    mark('ARC FURNACE', tuple(E + Vector((-5.3, -5.3, 11))), '150 t HEATS / FED HOT BY A CLOSED CONVEYOR')
    mark('HYDROGEN SPHERES', (-43, -32, 13), 'BUFFER FOR WINDLESS HOURS')
    mark('VAPOUR STACK', (-36, 4.4, 110), 'TOP GAS, AFTER THE SCRUBBER')
    return 36, 20
