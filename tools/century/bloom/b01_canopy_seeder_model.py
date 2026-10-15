"""CANOPY SEEDER: electric tandem-wing tilt-rotor that plants one seed pod per m2.

Units are centimetres. X forward, Y to port, Z up. A slim fuselage carries two
wings of equal span: a shoulder front wing and a rear wing on a swept fin.
Four tip nacelles tilt 12 degrees forward of vertical for the slow planting
pass. The seed magazine (four species canisters, revolver cluster) hangs at
the centre of gravity between the wings; its selector feeds a single
pneumatic pod injector whose muzzle stays above the skid line.
Mass budget behind the field notes: 55 kg = 25 airframe + 19 battery
(4.7 kWh) + 10.8 kg pods (2 400 x 4.5 g).
"""
from ..kit import *
from .parts import wing, loft, sphere, arc_tube, proprotor

TILT = 12
SPAN = 120
R = 45
POD_R = .9
MAG = Vector((-24, 0, -32))     # magazine cluster centre
FRONT = (58, 17)                # leading-edge x, z of the front wing root
REAR = (-96, 47)


def nacelle(x, y, z, side, phase):
    """Tip nacelle in its own frame: axis +Z, pivot at the wing tip."""
    with at((x, y, z), TILT, 'Y'):
        body = hull('tilt nacelle', [(-27, 3.5, 3.5, 0), (-20, 8.5, 8.5, 0), (4, 9.6, 9.6, 0),
                                      (19, 8.6, 8.6, 0), (25, 5, 5, 0)], 'Y')
        body.matrix_world = Matrix.Rotation(math.radians(90), 4, 'X') @ body.matrix_world
        for zz in (-12, -8, -4):
            ring('motor cooling band', (0, 0, zz), 9.1, .6, 1.1, (0, 0, 1), 'detail')
        ring('nacelle seam', (0, 0, 6), 9.9, .5, .8, (0, 0, 1), 'detail')
        proprotor((0, 0, 28), R, 3, (0, 0, 1), 14, phase=phase)
        cyl('tilt bearing', (0, -side * 8.5, 0), 4.8, 3, 'detail', (0, -side, 0))
        bolts((0, -side * 11.5, 0), 3.4, 6, (0, -side, 0), .55)


def canister(p, outward):
    """Species canister with a sight slot facing outward from the cluster."""
    L = 74
    start = Vector(p) - Vector((L / 2, 0, 0))
    arc_tube('species canister', start, (1, 0, 0), outward, 4.4, .7, L, 20, 340)
    for xx in (-L / 2 - 1.2, L / 2):
        arc_tube('canister end ring', Vector(p) + Vector((xx, 0, 0)), (1, 0, 0), outward, 5.0, 1.3, 1.6)
    cyl('species cap', Vector(p) + Vector((L / 2 + 1.6, 0, 0)), 4.7, 2.6, 'accent', (1, 0, 0), 24)
    c = Vector(p) + Vector((L / 2 + 4.2, 0, 0))
    loft('loading handle', [c + Vector((0, -2.6, 0)), c + Vector((3.2, -2.6, 0)), c + Vector((3.2, 2.6, 0)), c + Vector((0, 2.6, 0))], .45, 8, 'detail', False)
    # Pods fill the tube; only the layer behind the sight slot is modelled
    # (the rest is hidden by the wall and would not reach the export).
    out = Vector(outward); out = (out - Vector((1, 0, 0)) * out.x).normalized()
    side = Vector((1, 0, 0)).cross(out)
    step = 2 * POD_R + .15
    for k in range(int((L - 6) / step)):
        for j, ang in enumerate((-32, 0, 32)):
            a = math.radians(ang)
            off = (out * math.cos(a) + side * math.sin(a)) * 2.55
            sphere('seed pod', Vector(p) + Vector((-L / 2 + 3 + k * step + (step / 2 if j == 1 else 0), 0, 0)) + off, POD_R, 'detail', 10, 6)


def build():
    views(B=(34, -24), C=(20, -8))
    # --- airframe -----------------------------------------------------------
    fus = hull('fuselage', [(-128, 3, 4, 17), (-112, 9, 10, 13), (-80, 17, 18, 6), (-30, 22, 21, 1),
                            (30, 23, 21, 0), (70, 19, 19, -1), (94, 11, 12, -3), (107, 3.5, 4.5, -4)], 'X')
    for st in (-80, 70):
        hull_seam(fus, st)
    # Battery bay between the wings: top hatch, latches, two carry handles.
    box('battery hatch', (-22, 0, 21.6), (46, 26, 1.6), 3, 'detail')
    for x in (-36, -8):
        loft('hatch carry handle', [(x - 6, 0, 22.2), (x - 5, 0, 27), (x + 5, 0, 27), (x + 6, 0, 22.2)], .9, 10, 'detail')
    for y in (-8, 8):
        box('hatch latch', (-46, y, 22.2), (4, 3.5, 1.4), .5, 'accent')
    # Front wing (shoulder) and rear wing on a swept fin; equal span, slight dihedral.
    fx, fz = FRONT; rx, rz = REAR
    for side in (-1, 1):
        wing('front wing', (fx + 4, side * 8, fz), (fx - 1, side * SPAN, fz + 4), 40, 29, t=.15, stations=10)
        wing('front spar cap', (fx - 7, side * 20, fz + 3.1), (fx - 9, side * (SPAN - 10), fz + 6.6), 1.2, 1.2, t=.5, camber=0, stations=2, role='detail')
        wing('front flaperon', (fx - 29, side * 40, fz + 1), (fx - 23, side * (SPAN - 8), fz + 4), 8, 6, t=.06, camber=0, stations=4, role='detail')
        wing('rear wing', (rx + 4, side * 3, rz), (rx - 1, side * SPAN, rz + 4), 40, 29, t=.14, stations=10)
        wing('rear spar cap', (rx - 7, side * 16, rz + 3.0), (rx - 9, side * (SPAN - 10), rz + 6.5), 1.2, 1.2, t=.5, camber=0, stations=2, role='detail')
        wing('rear elevon', (rx - 29, side * 30, rz + 1), (rx - 23, side * (SPAN - 8), rz + 4), 8, 6, t=.06, camber=0, stations=4, role='detail')
    root = Vector((-86, 0, 12)); tip = Vector((-96, 0, 47.5))
    wing('swept fin', root, tip, 38, 31, (-1, 0, 0), (0, 1, 0), t=.11, camber=0, stations=6)
    box('front wing saddle', (fx - 14, 0, fz + 1.5), (44, 18, 7), 3.5)
    # Fold joints at mid-span: a chordwise seam over the upper skin and a
    # latch fairing at the trailing edge. The aircraft travels folded.
    from .parts import airfoil
    for side in (-1, 1):
        for (lx, lz) in ((fx, fz), (rx, rz)):
            f = 64 / SPAN
            y = side * 64; le = Vector((lx + 4 - 5 * f, y, lz + 4 * f)); c = 40 - 11 * f
            upper = [(x, z) for x, z in airfoil(28, .15 if lx == fx else .14, .02) if z >= 0]
            tube('wing fold seam', [le + Vector((-x * c, 0, z * c + .25)) for x, z in upper], .12, 'detail')
            box('fold latch fairing', le + Vector((-c + 3, 0, 1.2)), (7, 4, 2.4), 1, 'detail')
    # Four tilt nacelles: pivots at the wing tips (quarter chord).
    for i, (x, z) in enumerate(((fx - 8, fz + 4), (rx - 8, rz + 4))):
        for side in (-1, 1):
            nacelle(x, side * (SPAN + 7), z, side, 20 + 40 * i + (30 if side > 0 else 0))
    # Twin skids with sprung legs; the magazine hangs between them.
    for side in (-1, 1):
        y = side * 34
        loft('landing skid', [(-100, y, -72), (32, y, -72), (46, y, -69), (52, y, -62)], 2.3, 14)
        for x in (-70, 20):
            loft('skid leg', [(x, side * 15, -16), (x, side * 26, -40), (x, y, -71)], lambda t: 3.4 - 1.2 * t, 14)
    # Nose sensors: lidar sphere in a chin collar, downward multispectral camera.
    ring('lidar collar', (88, 0, -16), 7.4, 1.8, 2.6, (0, 0, 1))
    sphere('terrain lidar dome', (88, 0, -16), 6.4, 'accent', 32, 16)
    box('multispectral camera', (70, 0, -21), (10, 8, 6), 1.6, 'detail')
    cyl('camera lens', (70, 0, -24), 2.2, 1.2, 'accent', (0, 0, -1), 20)
    rod('pitot boom', (104, 0, -3), (124, 0, -3), .55, 'detail')
    # --- B: seed magazine ------------------------------------------------------
    with group('B'):
        offs = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        for a, b in offs:
            canister(MAG + Vector((0, a * 5.5, b * 5.5)), (0, a, b))
        for x in (-20, 24):
            ring('cluster clamp band', MAG + Vector((x, 0, 0)), 12.0, 1.7, 3, (1, 0, 0))
            rod('magazine hanger', MAG + Vector((x + 1.5, 0, 11.6)), (MAG.x + x + 1.5, 0, -19), 1.5)
        box('quick-release beam', (MAG.x + 2, 0, -20), (62, 6, 3), 1.2, 'detail')
        # Rotary selector at the aft end: one port per species, one outlet.
        sel = MAG + Vector((-45, 0, 0))
        cyl('selector drum', sel, 12.5, 8, 'structure', (1, 0, 0))
        flange('selector cover', sel, 12.5, (-1, 0, 0), 1.5)
        for a, b in offs:
            tube('species feed', [MAG + Vector((-37.5, a * 5.5, b * 5.5)), MAG + Vector((-39.5, a * 4.5, b * 4.5)), sel + Vector((8, a * 3.2, b * 3.2))], .9, 'cable')
        motor(sel + Vector((4, 12.5, 0)), 4, 8, (0, 1, 0))
        box('selector encoder', sel + Vector((4, -13.5, 3)), (5, 3, 6), 1, 'detail')
        mark('SEED MAGAZINE', MAG + Vector((-30, -8.6, -6.5)), 'FOUR SPECIES / 2 400 PODS / RELOADED BY HAND')
    # --- C: pod injector ------------------------------------------------------
    with group('C'):
        sel = MAG + Vector((-45, 0, 0))
        ax = Vector((sel.x - 16, 0, 0))            # injector axis, aft of the selector
        tee = ax + Vector((0, 0, -48))
        cyl('breech tee', tee + Vector((0, 0, -4)), 4.4, 8, 'structure', (0, 0, 1), 36)
        flange('breech cap', tee + Vector((0, 0, 4)), 4.6, (0, 0, 1), 1.2)
        # Feed elbow from the selector outlet into the side of the breech.
        loft('feed elbow', [sel + Vector((-4, 0, -9)), sel + Vector((-9, 0, -13)), tee + Vector((3.8, 0, 1.5))], 1.5, 14, 'structure')
        # Fast valve on top of the breech; the air charge sets the planting depth.
        box('fast air valve', tee + Vector((0, 0, 9.5)), (7, 7, 6), 1.4, 'detail')
        cyl('valve coil', tee + Vector((0, -3.5, 9.5)), 2.2, 2.6, 'accent', (0, -1, 0), 20)
        res = ax + Vector((-16, 0, -44))
        sphere('air reservoir', res, 6.6, 'structure', 32, 16)
        ring('reservoir strap', res + Vector((0, 0, 0)), 6.9, .9, 1.4, (1, 0, 0), 'detail')
        rod('reservoir cradle arm', res + Vector((5.5, 0, -2)), tee + Vector((-4.2, 0, -2)), 1.0)
        box('compressor', res + Vector((-10, 0, 3)), (7, 8, 10), 1.8, 'detail')
        for zz in (-.5, 2, 4.5, 7):
            box('compressor fin', res + Vector((-10, 0, zz)), (8.2, 9.2, .5), .2, 'detail')
        loft('charge line', [res + Vector((4.8, 0, 4.6)), res + Vector((9, 0, 9)), tee + Vector((-3.5, 0, 9.5))], .8, 10, 'cable')
        # Charge gauge on the line, dial facing the service side.
        gp = res + Vector((10, -1, 9.5))
        cyl('charge gauge body', gp, 2.6, 2, 'structure', (0, -1, 0), 32)
        rod('gauge stem', gp + Vector((0, -1, -2.4)), res + Vector((9.3, 0, 8.6)), .5, 'detail')
        ring('gauge bezel', gp + Vector((0, -2, 0)), 2.8, .5, .6, (0, -1, 0), 'detail')
        rod('gauge needle', gp + Vector((0, -2.3, 0)), gp + Vector((1.3, -2.3, 1.6)), .18, 'accent')
        # Barrel: sight slot at the breech shows the chambered pod.
        arc_tube('injector barrel', tee + Vector((0, 0, -4)), (0, 0, -1), (0, -1, 0), 2.6, .6, 8, 38, 322)
        ring('slot end band', tee + Vector((0, 0, -12.5)), 3.2, .8, 1.2, (0, 0, 1), 'detail')
        cyl('barrel', tee + Vector((0, 0, -12)), 2.6, 7, 'structure', (0, 0, -1), 28)
        loft('muzzle shroud', [tee + Vector((0, 0, -18.5)), tee + Vector((0, 0, -21)), tee + Vector((0, 0, -22.5))], lambda t: 2.9 + 1.7 * t * t, 28, 'accent', False)
        sphere('chambered pod', tee + Vector((0, 0, -8)), POD_R * 1.1, 'accent', 16, 8)
        sphere('next pod', tee + Vector((1.8, 0, 1.5)), POD_R * 1.05, 'detail', 14, 8)
        # Downward rangefinder: fires only above the mapped spot.
        box('rangefinder', tee + Vector((8, 0, -8)), (5, 5, 8), 1.2, 'detail')
        cyl('rangefinder window', tee + Vector((8, 0, -12.2)), 1.5, .8, 'accent', (0, 0, -1), 16)
        box('rangefinder bracket', tee + Vector((5, 0, -4)), (6, 3, 2), .6, 'detail')
        mark('POD INJECTOR', tee + Vector((0, -2.8, -8)), 'PLANTS 30 mm DEEP, UNDER THE WATER-REPELLENT CRUST')
    mark('TERRAIN LIDAR', (89, -5.5, -17), '5 cm GRID / SLOPE, ASH AND SOIL MOISTURE')
    q = math.radians(TILT)
    mark('TILTING PROPROTOR', (fx - 8 + 28 * math.sin(q), SPAN + 7, fz + 4 + 28 * math.cos(q)), 'HOVERS TO PLANT / TILTS FORWARD TO CRUISE')
    mark('TILT NACELLE', (rx - 8 + 6 * math.sin(q) - 7, -(SPAN + 7), rz + 4 - 6), '2.8 kW EACH / ANY THREE CAN LAND IT')
    mark('WING FOLD', (fx - 9, 64, fz + 5.5), 'FOLDS AT MID-SPAN / TRAVELS IN A PICKUP BED')
    return 30, 32
