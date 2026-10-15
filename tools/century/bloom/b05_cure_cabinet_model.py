"""CURE CABINET: bedside cell-therapy foundry on castors, curved door open.

Authored in centimetres, then scaled x2 (1 unit = 5 mm) so the editing
cartridge's millimetre features survive the hidden-line tolerance.
X to the right, Y depth (front is -Y), Z up, floor at z = 0.
The body is a rounded C-section shell (68 x 58 cm, 22-150 cm) whose front
sector is a curved door, hinged on the left edge and swung open 115 degrees.
Above it a closed crown carries the sloped console. Bays, top to bottom:
editing-cartridge carousel (114-148), rocking-bag bioreactor (66-114),
cold drawer and release-testing cytometer (22-66). On the right side the
sterile tube welder receives the bag of the patient's collected cells.
"""
from ..kit import *
from .parts import loft, sphere, arc_tube

S = 2.0
RX, RY, E = 34, 29, .55          # body half-width, half-depth, superellipse exponent
Z0, Z1 = 22, 150                 # C-shell height
WALL = 1.8
OPEN = (222, 318)                # door sector (front is 270 degrees)


def se(a, rx, ry):
    c, s_ = math.cos(a), math.sin(a)
    return (rx * math.copysign(abs(c) ** E, c), ry * math.copysign(abs(s_) ** E, s_))


def c_shell(name, a0, a1, z0, z1, role='structure', n=64):
    """Superellipse wall sector, extruded vertically, with real thickness."""
    vs = []; fs = []
    angles = [math.radians(a0 + (a1 - a0) * k / n) for k in range(n + 1)]
    m = n + 1
    for z in (z0, z1):
        for rx, ry in ((RX, RY), (RX - WALL, RY - WALL)):
            for a in angles:
                x, y = se(a, rx, ry); vs.append((x, y, z))
    # blocks: 0 outer-bottom, 1 inner-bottom, 2 outer-top, 3 inner-top
    for k in range(n):
        fs.append((k, k + 1, 2 * m + k + 1, 2 * m + k))                   # outer
        fs.append((m + k, 3 * m + k, 3 * m + k + 1, m + k + 1))            # inner
        fs.append((2 * m + k, 2 * m + k + 1, 3 * m + k + 1, 3 * m + k))    # top rim
        fs.append((k, m + k, m + k + 1, k + 1))                           # bottom rim
    fs.append((0, 2 * m, 3 * m, m)); fs.append((n, m + n, 3 * m + n, 2 * m + n))
    return g.mesh(name, vs, fs, role)


def plate(name, z, inset=2.4, t=1.2, role='structure', n=64):
    """Horizontal shelf matching the inner section."""
    vs = []; fs = []
    for zz in (z, z + t):
        for k in range(n):
            x, y = se(T * k / n, RX - WALL - inset, RY - WALL - inset); vs.append((x, y, zz))
    fs.append(tuple(reversed(range(n)))); fs.append(tuple(n + k for k in range(n)))
    for k in range(n):
        fs.append((k, (k + 1) % n, n + (k + 1) % n, n + k))
    return g.mesh(name, vs, fs, role)


def pillow(name, c, L, W, H, axis='X', role='structure'):
    sec = [(-L / 2, W * .12, H * .1, 0), (-L / 2 + L * .1, W * .45, H * .45, 0), (-L * .2, W * .5, H * .5, 0),
           (L * .2, W * .5, H * .5, 0), (L / 2 - L * .1, W * .45, H * .45, 0), (L / 2, W * .12, H * .1, 0)]
    with at(c):
        o = hull(name, sec, axis, role, .55)
    return o


def cartridge(c, featured=False):
    """Single-use editing cartridge, 8 x 3.4 x 12 cm, standing on edge."""
    x, y, z = c
    box('cartridge body', (x, y, z), (8, 3.4, 12), .6, 'structure')
    if not featured:
        return
    # Sealed foil top with six reagent wells; guide ribs; label and barcode on the face.
    box('foil seal', (x, y, z + 6.05), (7.2, 2.8, .1), .05, 'shell')
    for i in range(3):
        for j in range(2):
            ring('reagent well', (x - 2.4 + i * 2.4, y - .7 + j * 1.4, z + 5.4), .55, .18, .7, (0, 0, 1), 'detail')
    # Electroporation chamber: clear cuvette window with two electrode plates.
    box('electrode chamber window', (x + 1.6, y - 1.72, z - .6), (3.4, .1, 4.6), .3, 'accent')
    for dx in (-1.1, 1.1):
        box('electrode plate', (x + 1.6 + dx, y - 1.78, z - .6), (.3, .12, 4.0), .05, 'accent')
    # Moulded microfluidic channels, wells to chamber to outlet.
    for i, xx in enumerate((-2.4, 0, 2.4)):
        g.wire('fluid channel', [(x + xx, y - 1.76, z + 4.9), (x + xx, y - 1.76, z + 3.6), (x + .6 + i * .5, y - 1.76, z + 2.4), (x + .9 + i * .35, y - 1.76, z + 1.8)], .06, 'cable')
    g.wire('fluid channel', [(x + 1.6, y - 1.76, z - 3.0), (x + 1.6, y - 1.76, z - 4.4), (x - 2.6, y - 1.76, z - 4.4), (x - 2.6, y - 1.76, z - 5.4)], .06, 'cable')
    ring('outlet port', (x - 2.6, y, z - 6), .5, .2, .6, (0, 0, -1), 'detail')
    box('label panel', (x - 2.2, y - 1.72, z + .6), (2.8, .08, 5.4), .1, 'shell')
    for k in range(11):
        w = .06 if k % 3 else .14
        box('barcode bar', (x - 3.4 + k * .23, y - 1.76, z - 3.0), (w, .06, 1.8), .01, 'detail')
    for dz in (-4, 4):
        box('guide rib', (x + 4.1, y, z + dz), (.3, 1.6, 2.4), .1, 'detail')


def castor(x, y):
    cyl('swivel plate', (x, y, 12.5), 4.2, 1, 'detail', (0, 0, 1), 24)
    box('castor fork', (x, y + 1.5, 9), (4, 6, 6), .8, 'structure')
    cyl('castor wheel', (x - 1.6, y + 3, 5), 5, 3.2, 'structure', (1, 0, 0), 32)
    ring('wheel hub', (x + 1.7, y + 3, 5), 1.8, .6, .4, (1, 0, 0), 'detail')


def build():
    views(B=(24, 30), C=(28, 18))
    start = len(g.parts); wstart = len(g.wires)
    # --- body, crown, plinth ------------------------------------------------------
    c_shell('cabinet shell', OPEN[1] - 360, OPEN[0], Z0, Z1)
    box('plinth', (0, 0, 17), (RX * 2 - 3, RY * 2 - 3, 10), 4, 'structure')
    g.trim('bumper band', 17, RX - .6, RY - .6)
    crown = hull('crown', [(Z1, RX, RY, 0), (163, RX - .3, RY - .3, 0), (169, RX - 2.5, RY - 2.2, 0), (172.5, RX - 7, RY - 6, 0), (174.5, RX - 14, RY - 12, 0), (175.2, RX - 22, RY - 19, 0)], 'Y', 'structure', E)
    crown.matrix_world = Matrix.Rotation(math.radians(90), 4, 'X') @ crown.matrix_world
    for z in (Z1 + .2,):
        g.trim('crown seam', z, RX + .4, RY + .4)
    # Sloped console on the crown's front.
    with at((10, -RY + 1.2, 160), -18, 'X'):
        box('console bezel', (0, 0, 0), (26, 1.6, 12), 1.2, 'structure')
        box('console screen', (0, -.85, .3), (22, .2, 9), .6, 'accent')
    box('status light bar', (-17, -RY + 1.2, 158), (10, .8, 1.2), .4, 'accent')
    # Door: the front sector, hinged at its left edge, swung open.
    hx, hy = se(math.radians(OPEN[0]), RX, RY)
    b = len(g.parts); w = len(g.wires)
    c_shell('curved door', OPEN[0], OPEN[1], Z0 + 1, Z1 - 1)
    for z in (Z0 + 4, Z1 - 4):
        pts = [se(math.radians(OPEN[0] + (OPEN[1] - OPEN[0]) * k / 40), RX - WALL - .3, RY - WALL - .3) for k in range(41)]
        g.wire('door gasket', [(x, y, z) for x, y in pts], .35, 'accent')
    gx, gy = se(math.radians(300), RX + .8, RY + .8)
    loft('door handle', [(gx, gy, 80), (gx + .8, gy - 2.4, 82), (gx + .8, gy - 2.4, 104), (gx, gy, 106)], .8, 10, 'detail')
    for z in (40, 130):
        cyl('door hinge knuckle', (hx - .6, hy - .6, z - 4), 1.3, 8, 'detail', (0, 0, 1), 16)
    transform(b, w, Matrix.Translation((hx, hy, 0)) @ Matrix.Rotation(math.radians(-115), 4, 'Z') @ Matrix.Translation((-hx, -hy, 0)))
    # Shelves between bays.
    plate('lower shelf', 66)
    plate('upper shelf', 114)
    # --- top bay: cartridge carousel --------------------------------------------
    with group('C'):
        cartridge((0, -21, 124), featured=True)
    cyl('carousel turntable', (0, 4, 116), 21, 1.6, 'structure', (0, 0, 1), 64)
    cyl('carousel hub', (0, 4, 117.6), 5, 5, 'detail', (0, 0, 1), 32)
    for k in range(12):
        a = math.radians(270 + 30 * k)
        if k == 0:
            continue
        with at((15 * math.cos(a), 4 + 15 * math.sin(a), 0), math.degrees(a) - 90 + 90, 'Z'):
            cartridge((0, 0, 124))
    box('cartridge rail', (0, -18, 117.4), (9.4, 14, 1), .3, 'detail')
    # --- middle bay: rocking-bag bioreactor (B) -----------------------------------
    with group('B'):
        box('cradle base', (0, 2, 69), (40, 32, 3), 1.2, 'structure')
        for x in (-17, 17):
            box('rocker bearing block', (x, 2, 73), (4, 8, 6), 1, 'structure')
        cyl('rocker axle', (-19, 2, 75), 1.2, 38, 'detail', (1, 0, 0), 16)
        motor((20, 2, 75), 2.8, 5.5, (1, 0, 0))
        with at((0, 2, 77), 6, 'X'):
            box('rocking tray', (0, 0, 1), (46, 34, 1.6), 1.2, 'structure')
            for x in (-23, 23):
                box('tray lip', (x, 0, 2.6), (1.2, 34, 2), .4, 'detail')
            pillow('cell culture bag', (0, 0, 4.6), 38, 26, 5.2)
            for x in (-8, 0, 8):
                cyl('sensor spot', (x, -4, 7.2), 1.1, .3, 'accent', (0, 0, 1), 20)
            for y in (-7, 0, 7):
                cyl('bag port', (-19.6, y, 4.6), .6, 3.2, 'detail', (-1, 0, 0), 12)
        # Gas and media lines to the back-wall manifold; 0.2 um vent filter.
        box('gas manifold', (0, 23, 98), (24, 3, 9), 1, 'structure')
        for i, x in enumerate((-8, 0, 8)):
            cyl('manifold valve', (x, 21.2, 98), 1.3, 1.6, 'accent', (0, -1, 0), 16)
        tube('gas line', [(-22.5, -5, 80), (-26, 0, 84), (-24, 14, 94), (-8, 21, 98)], .5, 'cable')
        tube('media line', [(-22.5, 2, 80), (-25, 8, 86), (-18, 20, 96), (0, 21, 98)], .5, 'cable')
        tube('sample line', [(-22.5, 9, 80), (-23, 14, 84), (-10, 20, 92), (8, 21, 98)], .5, 'cable')
        cyl('vent filter', (14, 21, 104), 2.2, 5, 'structure', (0, 0, 1), 24)
        tube('vent line', [(14, 21, 109), (14, 21, 111), (10, 22, 111)], .4, 'cable')
        box('incubation heater', (0, 24.5, 84), (40, 1, 14), .5, 'detail')
        for x in range(-16, 17, 4):
            box('heater fin', (x, 23.8, 84), (.6, .8, 12), .2, 'detail')
    # --- lower bay: cold drawer and release-testing cytometer ----------------------
    with at((0, -16, 0)):
        box('cold drawer', (-15, 0, 38), (26, 44, 18), 1.2, 'structure')
        box('drawer front', (-15, -22.6, 38), (28, 2, 20), 1.4, 'structure')
        loft('drawer pull', [(-21, -23.6, 45), (-21, -25.4, 45.4), (-9, -25.4, 45.4), (-9, -23.6, 45)], .5, 8, 'detail')
        for i in range(4):
            for j in range(6):
                cyl('reagent vial', (-22 + i * 4.6, -16 + j * 4.2, 47.2), 1.3, 4.2, 'detail', (0, 0, 1), 16)
                cyl('vial cap', (-22 + i * 4.6, -16 + j * 4.2, 51.4), 1.4, 1, 'accent' if (i + j) % 5 == 0 else 'detail', (0, 0, 1), 16)
    box('cytometer', (15, 2, 42), (26, 36, 38), 2, 'structure')
    cyl('sample carousel', (15, -6, 61), 8, 1.4, 'structure', (0, 0, 1), 40)
    for k in range(10):
        a = T * k / 10
        cyl('sample tube', (15 + 6 * math.cos(a), -6 + 6 * math.sin(a), 62.4), .7, 3, 'detail', (0, 0, 1), 12)
    box('flow cell window', (15, -16.1, 50), (8, .3, 5), .4, 'accent')
    for z in range(28, 44, 3):
        box('cytometer vent', (15, -16.1, z), (18, .3, .8), .2, 'detail')
    # --- right side: sterile welder, bag hook, patient's collected cells ---------------
    box('welder recess', (RX + .2, -6, 108), (1.4, 20, 18), 1.2, 'detail')
    box('sterile tube welder', (RX + 3, -6, 108), (5, 14, 9), 1.2, 'structure')
    for dz in (-2.6, 2.6):
        box('welder jaw', (RX + 5.8, -6, 108 + dz), (1.2, 10, 1.6), .4, 'accent')
    rod('bag hook arm', (RX, 8, 150), (RX + 12, 8, 150), .9, 'structure')
    loft('bag hook', [(RX + 12, 8, 150), (RX + 13.6, 8, 148), (RX + 12.6, 8, 146)], .5, 8, 'detail', False)
    with at((RX + 12.6, 8, 133), 90, 'Y'):
        pillow("patient's cell bag", (0, 0, 0), 22, 13, 3.4)
    box('bag label', (RX + 14.4, 8, 131), (.2, 7, 5), .2, 'shell')
    ring('bag eyelet', (RX + 12.6, 8, 145), 1, .3, .5, (0, 1, 0), 'detail')
    tube('collection line', [(RX + 12.6, 8, 122), (RX + 11, 6, 116), (RX + 7, 0, 111.5), (RX + 5.6, -6, 110)], .45, 'cable')
    tube('transfer line', [(RX + 5.6, -6, 106), (RX + 3, -12, 100), (RX + .5, -14, 96)], .45, 'cable')
    # --- castors and push handle -----------------------------------------------------
    for x in (-24, 24):
        for y in (-19, 19):
            castor(x, y)
    for x in (-24, 24):
        loft('push handle', [(x, RY - 2, 96), (x, RY + 6, 98), (x * .95, RY + 7, 104)], 1.4, 12, 'structure')
    rod('push bar', (-23, RY + 7, 104), (23, RY + 7, 104), 1.6, 'structure')
    # --- anchors (authored in cm, scaled with the model) ---------------------------------
    mark('EDITING CARTRIDGE', (-4, -22.8, 127), 'ONE PATIENT / ONE SEALED CARTRIDGE')
    mark('BIOREACTOR BAY', (-19, -8, 83.5), 'ROCKING BAG / 1 L / 37 °C')
    mark('COLD DRAWER', (-26, -38.6, 42), '4 °C REAGENTS FOR ONE RUN')
    mark('RELEASE TESTING', (24, -16.3, 34), 'COUNT, IDENTITY, STERILITY / BEFORE RELEASE')
    mark('STERILE WELDER', (RX + 6.4, -6, 110.6), "JOINS THE PATIENT'S OWN CELLS / NO OPEN STEP")
    mark('CONSOLE', (21, -RY + .2, 162), 'ONE NURSE RUNS IT / 20 MIN A DAY')
    # Scale the whole scene and its anchors: 1 unit = 5 mm.
    m = Matrix.Scale(S, 4)
    transform(0, 0, m)
    # Group lists hold the pre-scale wire tuples (transform replaces g.wires entries).
    from .. import kit
    for grp in kit.GROUPS.values():
        grp['wires'] = [(n, [m @ Vector(p) for p in pts], r) for n, pts, r in grp['wires']]
    for k, v in list(g.anchors.items()):
        g.anchors[k] = m @ Vector(v)
    return 26, 18
