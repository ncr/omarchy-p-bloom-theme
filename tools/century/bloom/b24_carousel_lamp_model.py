"""CAROUSEL LAMP: a playground roundabout that charges the reading-room lights.

Units: centimetres. Z up, ground at z = 0, roundabout axis at the origin.
The schoolyard slab has its front corner cut away as a clean section,
so the concrete vault under the roundabout and the drive train in it show:
slewing bearing, one-way clutch, planetary step-up (1:21), a 180 kg steel
flywheel with an eddy-current speed limiter, and the generator on the floor.
A cable runs underground to a crook lamp post beside the reading-room door.
Roundabout: 2.5 m diameter deck, six arched handrails, six seats.
"""
import math
from ..kit import *
from .parts import loft, arc_tube, sphere, frame_matrix
from ..humans import human

DEPTH = 215
PIT = 84                            # outer radius of the vault ring
NOTCH = 230                         # the front corner of the yard is cut away to this
YARD = (-250, NOTCH, -NOTCH, 520)   # x0, x1, y0, y1 of the schoolyard slab
CORNER = 50                         # rounded yard corners
SAFETY = 205                        # rubber safety surface around the deck
ROOM = (-130, 110, 310, 470)        # reading-room walls: x0, x1, y0, y1
DOOR_X = 40
LAMP = Vector((150, 235, 0))


def revolve(name, profile, n=72, role='structure', centre=(0, 0, 0)):
    c = Vector(centre); vs = []; fs = []
    for r, z in profile:
        for j in range(n):
            a = math.tau * j / n
            vs.append(c + Vector((max(r, .01) * math.cos(a), max(r, .01) * math.sin(a), z)))
    m = len(profile)
    for i in range(m - 1):
        for j in range(n):
            fs.append((i * n + j, i * n + (j + 1) % n, (i + 1) * n + (j + 1) % n, (i + 1) * n + j))
    return g.mesh(name, vs, fs, role)


def yard_outline():
    """Rounded rectangle, anticlockwise, as a closed polygon."""
    x0, x1, y0, y1 = YARD; r = CORNER; pts = []
    for cx, cy, a0 in ((x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270)):
        for k in range(7):
            a = math.radians(a0 + 15 * k)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def ray(poly, theta):
    """Distance from the origin to the convex outline along theta."""
    d = (math.cos(theta), math.sin(theta)); best = 1e9
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        ex, ey = bx - ax, by - ay
        den = d[0] * ey - d[1] * ex
        if abs(den) < 1e-9:
            continue
        t = (ax * ey - ay * ex) / den
        u = (ax * d[1] - ay * d[0]) / den
        if t > 0 and -1e-6 <= u <= 1 + 1e-6:
            best = min(best, t)
    return best


def ground():
    """Schoolyard slab with its front corner cut away over the vault, as one surface."""
    poly = yard_outline()
    angles = set(math.radians(k * 2.5) for k in range(0, 109))
    for x, y in poly:
        a = math.atan2(y, x) % math.tau
        if a <= math.radians(270) + 1e-6:
            angles.add(a)
    angles = sorted(angles)
    n = len(angles)
    ins = [Vector((PIT * math.cos(a), PIT * math.sin(a), 0)) for a in angles]
    outs = [Vector((ray(poly, a) * math.cos(a), ray(poly, a) * math.sin(a), 0)) for a in angles]
    down = Vector((0, 0, DEPTH))
    vs = ins + outs + [p - down for p in outs] + [p - down for p in ins]
    fs = []
    for i in range(n - 1):
        fs.append((i, i + 1, n + i + 1, n + i))                    # paving
        fs.append((n + i, n + i + 1, 2 * n + i + 1, 2 * n + i))    # outer soil face
    fs.append((0, n, 2 * n, 3 * n))                                # section along +x
    fs.append((n - 1, 4 * n - 1, 3 * n - 1, 2 * n - 1))            # section along -y
    g.mesh('schoolyard', vs, fs, 'shell')
    # Kerb: a line just inside the edge of the paving.
    kerb = [Vector(((ray(poly, a) - 14) * math.cos(a), (ray(poly, a) - 14) * math.sin(a), .3)) for a in angles]
    tube('kerb', kerb, .35, 'detail')
    # Rubber safety surface around the deck, cut with the ground.
    tube('safety surface edge', [Vector((SAFETY * math.cos(a), SAFETY * math.sin(a), .3)) for a in angles if a <= math.radians(270)], .3, 'detail')
    # Section: straight cut faces with strata and hatching.
    for along, off in ((Vector((1, 0, 0)), Vector((0, -.3, 0))), (Vector((0, -1, 0)), Vector((.3, 0, 0)))):
        tube('paving layer', [along * PIT + Vector((0, 0, -12)) + off, along * NOTCH + Vector((0, 0, -12)) + off], .2, 'detail')
        tube('gravel bed', [along * PIT + Vector((0, 0, -40)) + off, along * NOTCH + Vector((0, 0, -40)) + off], .14, 'detail')
        for k in range(int((NOTCH - PIT - 6) / 18)):
            d = PIT + 6 + k * 18
            tube('section hatch', [along * d + Vector((0, 0, -44)) + off, along * min(NOTCH - 2, d + 30) + Vector((0, 0, -44 - 30 * min(1, (NOTCH - 2 - d) / 30))) + off], .08, 'shell')
        for k in range(int((NOTCH - PIT) / 18)):
            d = PIT + 6 + k * 18
            for z in (-90, -150):
                tube('section hatch', [along * d + Vector((0, 0, z)) + off, along * min(NOTCH - 2, d + 24) + Vector((0, 0, z - 24 * min(1, (NOTCH - 2 - d) / 24))) + off], .08, 'shell')


def roundabout():
    # Sculpted deck: gently domed top, rounded rim, recessed skirt.
    revolve('roundabout deck', [(0, 38), (60, 38.5), (112, 36.5), (122, 34), (125, 30), (122, 26),
                                (119, 20), (117, 8), (100, 8), (40, 8), (0, 8)])
    ring('deck tread ring', (0, 0, 36.2), 116, 1, .6, (0, 0, 1), 'detail')
    sphere('hub cap', (0, 0, 38), 20, 'structure', 40, 16, (1, 1, .55))
    for k in range(6):
        a = math.radians(k * 60 + 15)
        u = Vector((math.cos(a), math.sin(a), 0)); t = Vector((-math.sin(a), math.cos(a), 0))
        path = [u * 26 + Vector((0, 0, 38)), u * 32 + Vector((0, 0, 78)), u * 66 + Vector((0, 0, 104)),
                u * 102 + Vector((0, 0, 88)), u * 111 + Vector((0, 0, 37))]
        loft('arched handrail', path, 2.6, 14)
        loft('grab bar', [u * 66 + t * -14 + Vector((0, 0, 104)), u * 66 + t * 14 + Vector((0, 0, 104))], 1.8, 12, 'detail', False)
        s = Vector((math.cos(a + math.radians(30)), math.sin(a + math.radians(30)), 0))
        with at(s * 92 + Vector((0, 0, 41)), k * 60 + 45):
            box('seat pad', (0, 0, 0), (34, 42, 8), 3.5, 'detail')
    cyl('hub column', (0, 0, -6), 22, 14, 'structure', (0, 0, 1), 48)


def vault():
    arc_tube('vault ring', (0, 0, -190), (0, 0, 1), (1, 0, 0), PIT, 12, 190, 0, 270)
    arc_tube('vault floor', (0, 0, -202), (0, 0, 1), (1, 0, 0), PIT, PIT - .5, 12, 0, 270)
    with group('B'):
        cyl('slewing bearing', (0, 0, -18), 30, 12, 'structure', (0, 0, 1), 64)
        flange('bearing flange', (0, 0, -6), 30, (0, 0, 1), 3)
        cyl('drive shaft', (0, 0, -170), 5, 152, 'detail', (0, 0, 1), 24)
        cyl('one-way clutch', (0, 0, -58), 15, 14, 'structure', (0, 0, 1), 48)
        for z in (-55, -51, -47):
            ring('clutch rib', (0, 0, z), 16, 1, 1, (0, 0, 1), 'detail')
        cyl('planetary step-up', (0, 0, -104), 24, 28, 'structure', (0, 0, 1), 56)
        flange('gearbox input flange', (0, 0, -76), 24, (0, 0, 1), 2)
        flange('gearbox output flange', (0, 0, -104), 24, (0, 0, -1), 2)
        cyl('flywheel', (0, 0, -136), 30, 8, 'structure', (0, 0, 1), 72)
        ring('flywheel rim band', (0, 0, -136.5), 30.6, 1.2, 9, (0, 0, 1), 'detail')
        cyl('flywheel hub', (0, 0, -140), 9, 16, 'detail', (0, 0, 1), 32)
        # Eddy-current limiter: a caliper of magnets straddling the rim.
        a = math.radians(-45)
        with at((36 * math.cos(a), 36 * math.sin(a), -132), -45):
            box('limiter caliper', (0, 0, 0), (18, 16, 20), 2.5, 'accent')
            box('caliper gap', (-6, 0, 0), (10, 17, 9.5), .5, 'detail')
        cyl('generator', (0, 0, -186), 20, 30, 'structure', (0, 0, 1), 48)
        for z in (-181, -175, -169, -163):
            ring('generator fin', (0, 0, z), 21.5, 1.4, 1.2, (0, 0, 1), 'detail')
        box('terminal box', (22, 14, -168), (12, 14, 14), 2, 'detail')
        for q in (45, 135, 225, 315):
            b = math.radians(q)
            box('generator foot', (22 * math.cos(b), 22 * math.sin(b), -188), (10, 10, 4), 1, 'detail')
        tube('power cable', [Vector((26, 18, -164)), Vector((38, 34, -156)), Vector((48, 50, -150)),
                             Vector((56, 58, -148))], 1.4, 'cable')
        cyl('cable gland', (56, 58, -148), 3.2, 5, 'detail', (.7, .7, 0), 16)
    mark('FLYWHEEL VAULT', (30 * math.cos(math.radians(-60)), 30 * math.sin(math.radians(-60)), -132),
         '180 kg DISC / 600 rpm / 3 MINUTES OF RUN-ON')


def lamp():
    with group('C'):
        cyl('battery plinth', LAMP, 22, 72, 'structure', (0, 0, 1), 48)
        ring('plinth cap', LAMP + Vector((0, 0, 72)), 23, 3, 3, (0, 0, 1), 'detail')
        box('service door', LAMP + Vector((0, -21.5, 38)), (18, 2, 40), 1.5, 'detail')
        # Tapered pole with a crook that bends toward the door.
        top = LAMP + Vector((0, 0, 300))
        head = Vector((DOOR_X + 40, ROOM[2] - 50, 262))
        mid = (top + head) / 2
        path = [LAMP + Vector((0, 0, 72)), LAMP + Vector((0, 0, 220)), top, top + (head - top) * .15 + Vector((0, 0, 30)),
                mid + Vector((0, 0, 34)), head + (top - head) * .12 + Vector((0, 0, 14)), head + Vector((0, 0, 5))]
        loft('crook pole', path, lambda t: 6.2 - 3.0 * t, 18)
        box('charge controller', LAMP + Vector((0, -7.5, 150)), (18, 8, 26), 2, 'detail')
        tube('controller lead', [LAMP + Vector((0, -7, 137)), LAMP + Vector((0, -6.5, 110)), LAMP + Vector((0, -6, 80))], .6, 'cable')
        with at(head, 20):
            box('lamp head', (0, 0, 0), (46, 20, 9), 4, 'structure')
            box('led lens', (0, 0, -4.8), (36, 14, 1), .6, 'accent')
        loft('conduit elbow', [LAMP + Vector((40, -30, -20)), LAMP + Vector((40, -30, 4)), LAMP + Vector((22, -12, 8))], 2.2, 12, 'cable')
    mark('LAMP', head + Vector((-12, -4, -6)), '8 W LED / FROM DUSK UNTIL THE ROOM CLOSES')


def reading_room():
    """A small complete building: walls, gable roof, door with step, lit window."""
    x0, x1, y0, y1 = ROOM; wall_h = 225; ridge = 280; ov = 14
    box('reading-room walls', ((x0 + x1) / 2, (y0 + y1) / 2, wall_h / 2), (x1 - x0, y1 - y0, wall_h), 1.5, 'structure')
    ym = (y0 + y1) / 2; half = (y1 - y0) / 2; drop = ov * (ridge - wall_h) / half
    for yB in (y0 - ov, y1 + ov):
        vs = [Vector((x0 - ov, ym, ridge)), Vector((x1 + ov, ym, ridge)), Vector((x1 + ov, yB, wall_h - drop)), Vector((x0 - ov, yB, wall_h - drop))]
        vs += [v + Vector((0, 0, 7)) for v in vs]
        g.mesh('roof', vs, [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], 'structure')
    for x in (x0, x1):
        g.mesh('gable', [Vector((x, y0, wall_h)), Vector((x, y1, wall_h)), Vector((x, ym, ridge))], [(0, 1, 2)], 'structure')
    box('door frame', (DOOR_X, y0 - 1, 104), (96, 3, 208), 1, 'detail')
    box('door', (DOOR_X, y0 - 2, 102), (84, 2, 200), .8, 'detail')
    box('door handle', (DOOR_X - 30, y0 - 4, 102), (3, 3, 14), .8, 'detail')
    box('step', (DOOR_X, y0 - 20, 6), (124, 40, 12), 1.5, 'detail')
    wx = -70
    box('window frame', (wx, y0 - 1.5, 135), (90, 4, 90), 1.5, 'accent')
    box('window mullion', (wx, y0 - 3.5, 135), (4, 2, 84), .5, 'accent')
    box('window transom', (wx, y0 - 3.5, 150), (84, 2, 4), .5, 'accent')
    box('sill', (wx, y0 - 6, 87), (102, 12, 5), 1, 'detail')
    mark('READING ROOM', (x1 + .5, y0 + 60, 150), 'FOUR 6 W LED PANELS / TWENTY CHAIRS')


def build():
    human('presence', .28, 0, (DOOR_X + 20, ROOM[2] - 70, 0))
    views(B=(35, 12), C=(24, 12))
    ground()
    roundabout()
    vault()
    lamp()
    reading_room()
    mark('ROUNDABOUT DECK', (0, -118, 38), '2.5 m / RIM HELD BELOW 3.5 m/s')
    mark('TEACHER', (DOOR_X + 34, ROOM[2] - 70, 40), 'OPENS THE DOOR AT SEVEN')
    return 32, 34
