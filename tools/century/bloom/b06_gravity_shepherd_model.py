"""GRAVITY SHEPHERD: gravity tractor hovering beside a 30 m asteroid.

Units: 1 unit = 20 cm. Asteroid radius ~75 u (15 m), centre at the origin.
The craft hovers with its bus 200 u (40 m) from the centre along DIR.
Craft frame: z points away from the asteroid (along DIR), x along the
solar wings, y completes the frame. From the rock outward: hover-sensor
plate, a thrust frame with two outrigger pods (two gridded thrusters each,
canted 36 deg so the plumes pass either side of the rock: asin(15/40) =
22 deg + 12 deg plume half-angle), the octagonal bus with xenon tank and two
radiators, two 22 m roll-out wings, and at the far end a three-arm cradle
holding one 4.5 m boulder (~95 t) lifted from the asteroid.
"""
from contextlib import contextmanager
from ..kit import *
from .parts import loft, sphere, lumpy, surface_point, arc_tube, frame_matrix

AST_R = 75
DIST = 200
DIR = Vector((.80, -.12, .60)).normalized()
CANT = 36
STRETCH = (1.25, 1.0, .85)
SUN = Vector((.55, -.55, .63)).normalized()
LIFT = []


@contextmanager
def local(m):
    start = len(g.parts); wstart = len(g.wires)
    yield
    transform(start, wstart, m)


def surface_frame(rad, d):
    d = Vector(d).normalized()
    p = surface_point((0, 0, 0), rad, d, STRETCH)
    # Numerical normal from two nearby surface points.
    u = d.cross(Vector((0, 0, 1)))
    if u.length < .1:
        u = d.cross(Vector((1, 0, 0)))
    u.normalize(); v = d.cross(u)
    a = surface_point((0, 0, 0), rad, d + u * .01, STRETCH) - p
    b = surface_point((0, 0, 0), rad, d + v * .01, STRETCH) - p
    n = a.cross(b).normalized()
    if n.dot(p) < 0:
        n = -n
    return p, n, u, v


def crater(rad, d, r_ang, lip, role='detail'):
    """Raised crater lip following the surface: a closed tube on a small circle."""
    d = Vector(d).normalized()
    _, _, u, v = surface_frame(rad, d)
    pts = []
    for k in range(49):
        t = math.tau * k / 48
        q = (d * math.cos(r_ang) + (u * math.cos(t) + v * math.sin(t)) * math.sin(r_ang)).normalized()
        p, n, _, _ = surface_frame(rad, q)
        pts.append(p + n * lip * .45)
    loft('crater lip', pts, lip, 10, role, False)


def asteroid():
    body, rad = lumpy('asteroid', (0, 0, 0), AST_R, seed=11,
                      bumps=((1.0, 2, .075), (1.0, 3, .022)), stretch=STRETCH, seg=128, rings=64)
    # Craters with raised lips at several sizes, on the hemisphere toward the viewer.
    for d, ang, lip in [((-.25, -.9, .3), .34, 1.3), ((.3, -.85, -.25), .22, 1.0), ((-.7, -.6, -.15), .18, .9),
                        ((.05, -.6, .78), .15, .8), ((-.55, -.65, .5), .11, .7), ((.55, -.7, .25), .10, .6),
                        ((-.1, -.98, -.25), .08, .55), ((-.35, -.85, -.5), .07, .5), ((.2, -.95, .05), .06, .45),
                        ((-.85, -.35, .35), .09, .6), ((.4, -.6, -.62), .08, .55), ((-.45, -.88, -.1), .05, .4)]:
        crater(rad, d, ang, lip)
    # Fresh pit where the ballast boulder was lifted: sharp accent lip.
    crater(rad, (.62, -.62, .42), .2, 1.2, 'accent')
    LIFT[:] = [surface_frame(rad, (.62, -.62, .42))[0]]
    # A ridge crest running over the upper shoulder.
    ridge = []
    for k in range(25):
        t = k / 24
        q = Vector((-.9 + 1.3 * t, -.55 + .1 * math.sin(3 * t), .55 + .25 * math.sin(math.pi * t))).normalized()
        p, n, _, _ = surface_frame(rad, q)
        ridge.append(p + n * .6)
    loft('ridge crest', ridge, .35, 6, 'detail')
    # Terminator: the day-night line, drawn light.
    a = SUN.cross(Vector((0, 0, 1))).normalized(); b = SUN.cross(a)
    term = []
    for k in range(121):
        t = math.tau * k / 120
        p, n, _, _ = surface_frame(rad, a * math.cos(t) + b * math.sin(t))
        term.append(p + n * .4)
    g.wire('terminator', term, .15, 'shell')
    # Scattered boulders.
    import random
    rnd = random.Random(5)
    for i in range(22):
        d = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, -.25), rnd.uniform(-.8, .9))).normalized()
        r = rnd.uniform(1.0, 2.6)
        p, n, _, _ = surface_frame(rad, d)
        lumpy('boulder', p + n * r * .45, r, seed=90 + i, bumps=((1.0, 2, .12),), seg=16, rings=8)
    return rad


def octagon_prism(name, levels, role='structure'):
    """Octagonal body: levels are (z, across-flats radius)."""
    vs = []; fs = []
    for z, r in levels:
        rr = r / math.cos(math.pi / 8)
        vs.extend((rr * math.cos(math.pi / 8 + k * math.pi / 4), rr * math.sin(math.pi / 8 + k * math.pi / 4), z) for k in range(8))
    for i in range(len(levels) - 1):
        for k in range(8):
            fs.append((i * 8 + k, i * 8 + (k + 1) % 8, (i + 1) * 8 + (k + 1) % 8, (i + 1) * 8 + k))
    fs.append(tuple(reversed(range(8)))); fs.append(tuple((len(levels) - 1) * 8 + k for k in range(8)))
    return g.mesh(name, vs, fs, role)


def ion_thruster(p, axis, ref, k=.72):
    """One gridded ion thruster in a two-axis gimbal (built along +z, placed)."""
    with local(frame_matrix(p, axis, ref) @ Matrix.Scale(k, 4)):
        cyl('discharge chamber', (0, 0, -8), 5, 8, 'structure', (0, 0, 1), 40)
        ring('grid mount ring', (0, 0, 0), 5.8, 1.2, 1.2, (0, 0, 1), 'structure')
        for r in (1.5, 2.9, 4.3):
            ring('ion optics aperture band', (0, 0, 1), r, .25, .2, (0, 0, 1), 'accent')
        cyl('neutraliser', (5.6, 0, -2), .8, 3, 'detail', (0, 0, 1), 12)
        arc_tube('gimbal ring', (0, 0, -5.6), (0, 1, 0), (1, 0, 0), 7.2, .9, 1.4, 0, 360, 'detail', 36)
        for sd in (-1, 1):
            cyl('gimbal pivot', (sd * 6.9, -.7, -5.6), 1, 1.8, 'detail', (1, 0, 0), 12)
        cyl('gimbal actuator', (0, 6.9, -9), .8, 4, 'detail', (0, 0, 1), 10)


def outrigger(side):
    q = math.radians(CANT)
    out = Vector((side * math.sin(q), 0, -math.cos(q)))
    root = Vector((side * 12, 0, -14))
    tip = Vector((side * 36, 0, -24))
    for dy in (-4, 4):
        rod('outrigger longeron', root + Vector((0, dy, 3)), tip + Vector((0, dy, 3)), .8)
        rod('outrigger longeron', root + Vector((0, dy, -3)), tip + Vector((0, dy, -3)), .8)
    for k in range(4):
        a = root.lerp(tip, k / 4); b = root.lerp(tip, (k + 1) / 4)
        rod('outrigger brace', a + Vector((0, -4, 3)), b + Vector((0, -4, -3)), .45, 'detail')
        rod('outrigger brace', a + Vector((0, 4, 3)), b + Vector((0, 4, -3)), .45, 'detail')
    tube('xenon feed', [(0, -3, -20), root + Vector((0, -3, -1)), tip + Vector((0, -3, -2))], .45, 'cable')
    return tip, out


def engine_pod(tip, out):
    """Common mounting plate, four gimballed thrusters, PPU and feed valve."""
    plate = tip + out * 2
    with local(frame_matrix(plate, out, (0, 1, 0))):
        box('thruster mounting plate', (0, 0, 0), (24, 24, 2.2), 1)
        for x in (-11, 11):
            box('plate stiffener', (x, 0, -1.8), (1.6, 24, 1.6), .3, 'detail')
        box('power processing unit', (0, -4, -5.5), (16, 10, 6), 1)
        for x in (-5, -1.7, 1.7, 5):
            box('PPU fin', (x, -4, -9.2), (.8, 10, 1.6), .2, 'detail')
        cyl('xenon flow valve', (7, 7, -3.5), 2, 3, 'structure', (0, 0, 1), 20)
        tube('valve manifold', [(7, 7, -1.5), (6, 6, -.5), (-6, 6, -.5), (-6, -6, -.5), (6, -6, -.5)], .35, 'cable')
    ref = (0, 1, 0)
    fr = frame_matrix(plate, out, ref)
    for x in (-6, 6):
        for y in (-6, 6):
            ion_thruster(fr @ Vector((x, y, 6.2)), out, ref)
    return plate


def build():
    views(C=(-62, -34))
    rad = asteroid()
    W = Vector((-DIR.z, 0, DIR.x)).normalized()
    centre = DIR * DIST
    craft = frame_matrix(centre, DIR, W)
    with local(craft):
        # Octagonal bus, 6 m across flats, chamfered ends, three frame bands.
        octagon_prism('spacecraft bus', [(-13, 12), (-11.5, 15), (11.5, 15), (13, 12)])
        for z in (-6, 0, 6):
            octagon_prism('bus frame band', [(z - .5, 15.35), (z + .5, 15.35)], 'detail')
        # Radiators on the two faces normal to y: edge-on to the Sun, seen face-on here.
        for sd in (-1, 1):
            box('radiator arm', (0, sd * 17, 6), (3, 5, 2), .6, 'detail')
            box('deployed radiator', (0, sd * 30, 2), (22, 22, 1.2), .5)
            for k in range(-4, 5):
                g.wire('radiator heat pipe', [(k * 2.2, sd * 19.5, 2.8 * sd * 0 + 2.7), (k * 2.2, sd * 40.5, 2.7)], .08, 'detail')
        # Wing yokes and roll-out wings.
        for sd in (-1, 1):
            L = 110; Wd = 30; x0 = sd * 18
            box('wing yoke', (sd * 16, 0, 4), (5, 9, 8), 1.5)
            cyl('wing root drum', (x0, -Wd / 2 - 1, 4), 3.2, Wd + 2, 'structure', (0, 1, 0), 24)
            for y in (-Wd / 2, Wd / 2):
                loft('wing edge boom', [(x0, y, 4), (x0 + sd * L, y, 4)], 1.0, 10)
            box('wing tip spreader', (x0 + sd * L, 0, 4), (2.6, Wd + 2, 2.2), .6)
            g.mesh('solar blanket', [(x0, -Wd / 2 + 1, 3.6), (x0 + sd * L, -Wd / 2 + 1, 3.6), (x0 + sd * L, Wd / 2 - 1, 3.6), (x0, Wd / 2 - 1, 3.6)], [(0, 1, 2, 3)], 'shell')
            for k in range(1, 12):
                xx = x0 + sd * L * k / 12
                g.wire('cell string gap', [(xx, -Wd / 2 + 1, 3.7), (xx, Wd / 2 - 1, 3.7)], .08, 'shell')
            g.wire('blanket centreline', [(x0, 0, 3.7), (x0 + sd * L, 0, 3.7)], .08, 'shell')
        cyl('high-gain antenna mast', (0, -15, -8), 1, 7, 'detail', (0, -1, 0), 12)
        ring('high-gain dish', (0, -22, -8), 6.5, 6.3, 2.2, (0, -1, 0), 'structure')
        # Cradle: ring on the bus top, three curved arms gripping the boulder.
        cz = 36
        ring('cradle ring', (0, 0, 13), 11, 2.4, 3, (0, 0, 1), 'structure')
        lumpy('captured boulder', (0, 0, cz), 11.25, seed=73, bumps=((1.0, 2, .12), (1.0, 3, .05)), seg=40, rings=20)
        for k in range(3):
            a = math.radians(120 * k + 30); c, s_ = math.cos(a), math.sin(a)
            loft('cradle arm', [(10 * c, 10 * s_, 15), (15 * c, 15 * s_, 24), (15.5 * c, 15.5 * s_, 36), (11 * c, 11 * s_, 46), (5 * c, 5 * s_, 49)], lambda t: 1.8 - .8 * t, 12)
            cyl('arm knuckle', (15 * c, 15 * s_, 24), 2.2, 3, 'detail', (-s_, c, 0), 16)
            box('grip pad', (5.5 * c, 5.5 * s_, 48.4), (6, 6, 1.6), .6, 'accent')
    # Thrust frame: a cross-beam carrying both outriggers.
    with local(craft):
        box('thrust frame', (0, 0, -15), (30, 12, 3), 1)
        sphere('xenon tank', (0, 0, -21), 6, 'structure', 28, 14)
        ring('tank girth band', (0, 0, -21.3), 6.2, .6, .8, (0, 0, 1), 'detail')
        tip_l, out_l = outrigger(1)
        engine_pod(tip_l, out_l)
        tip_r, out_r = outrigger(-1)
    with group('B'), local(craft):
        engine_pod(tip_r, out_r)
    # B camera: from the exhaust side of the right pod, 56 degrees off its axis.
    rot = craft.to_3x3()
    ow = (rot @ out_r).normalized(); yw = (rot @ Vector((0, 1, 0))).normalized()
    xw = ow.cross(yw).normalized()
    tw = (ow * math.cos(math.radians(56)) + (yw * .8 + xw * .6).normalized() * math.sin(math.radians(56))).normalized()
    views(B=(math.degrees(math.atan2(tw.x, -tw.y)), math.degrees(math.asin(tw.z))))
    with group('C'), local(craft):
        for k in range(3):
            q = math.radians(120 * k + 30)
            rod('sensor truss', (5 * math.cos(q), 5 * math.sin(q), -26), (7 * math.cos(q), 7 * math.sin(q), -37), .7)
        cyl('sensor plate', (0, 0, -39), 11, 2.2, 'structure', (0, 0, 1), 48)
        ring('plate rim', (0, 0, -39.4), 11.4, .8, 1, (0, 0, 1), 'detail')
        cyl('scanning lidar', (-4.5, 0, -39), 3.2, 5, 'structure', (0, 0, -1), 32)
        cyl('lidar head', (-4.5, 0, -44), 2.7, 2.6, 'structure', (0, 0, -1), 32)
        box('lidar window', (-4.5, -2.6, -45.3), (3.2, .4, 1.6), .2, 'accent')
        for x, y in ((4.5, -5.5), (6.5, 3.5)):
            cyl('laser altimeter', (x, y, -39), 1.5, 4.5, 'structure', (0, 0, -1), 20)
            ring('altimeter hood', (x, y, -43.5), 1.8, .4, 1.4, (0, 0, -1), 'detail')
            cyl('altimeter lens', (x, y, -43.4), 1.1, .3, 'accent', (0, 0, -1), 16)
        for y in (-3.5, 7):
            box('stereo camera', (1, y, -40.6), (3.4, 3, 3.2), .5, 'structure')
            cyl('camera barrel', (1, y, -42.2), 1.1, 2, 'structure', (0, 0, -1), 16)
            ring('camera hood', (1, y, -44.2), 1.5, .35, 1, (0, 0, -1), 'accent')
        box('star tracker', (-8, 8, -32), (4, 4, 5), .6, 'structure')
        ring('star tracker baffle', (-8, 10.2, -32), 1.9, .3, 4.5, (0, 1, 0), 'detail')
        tube('sensor harness', [(0, 1.5, -37.2), (0, 3, -31), (0, 2.5, -24)], .45, 'cable')
    wtip = centre + W * (18 + 110)
    mark('ROLL-OUT SOLAR WING', wtip, '2 x 22 m / 45 kW AT 1 AU, 9 kW AT APHELION')
    mark('BALLAST BOULDER', centre + DIR * 49, '95 t LIFTED FROM THE ASTEROID ITSELF')
    mark('CANTED ION ENGINES', craft @ Vector((-40, 0, -30)), 'PLUMES PASS THE ROCK ON BOTH SIDES')
    mark('HOVER SENSORS', craft @ Vector((-4.5, 0, -46.5)), 'HOLDS 40 m FROM THE CENTRE FOR TWO YEARS')
    mark('RADIATOR', craft @ Vector((10, -40, 2)), 'SHEDS THE ENGINE ELECTRONICS HEAT')
    mark('TARGET ASTEROID', surface_point((0, 0, 0), rad, (-.95, -.3, .05), STRETCH), '30 m ACROSS / 28 000 t / RUBBLE AND ROCK')
    mark('LIFT SITE', LIFT[0], 'WHERE THE BALLAST CAME FROM')
    return 40, 22
