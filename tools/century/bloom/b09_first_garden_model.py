"""FIRST GARDEN: inflatable greenhouse beside the first Mars base.

Units are centimetres. X along the vault, Y across (-Y toward the viewer),
Z up. A 12 m barrel vault of radius 3.5 m with quarter-sphere ends; nine
inflated ribs outside a two-layer membrane (restraint net + bladder).
A 12 m... section to show two rows of four-tier
grow racks, the aisle and one crew member standing in shirtsleeves.
A rigid airlock at +X, a radiator at -X, regolith bags along the base.
Growing area: far row 10 m x 0.6 m x 4 tiers = 24 m2, near row of deep
beds 10 m x 0.9 m x 2 tiers = 18 m2 -> 42 m2.
"""
from contextlib import contextmanager
from ..kit import *
from .parts import loft, sphere, arc_tube, frame_matrix

R = 350          # vault radius
HALF = 500       # half length of the cylindrical part
CUT_X = (-470, 230)
CUT_PHI = (8, 128)   # degrees from the near ground line over the top


@contextmanager
def local(m):
    start = len(g.parts); wstart = len(g.wires)
    yield
    transform(start, wstart, m)


def vault_surface(name, r, role, cut=True):
    """Barrel surface p = (x, -r cos phi, r sin phi); omit the section window."""
    xs = [-HALF + 2 * HALF * i / 48 for i in range(49)]
    phis = [180 * j / 60 for j in range(61)]
    vs = []; fs = []; idx = {}
    for i, x in enumerate(xs):
        for j, ph in enumerate(phis):
            q = math.radians(ph)
            idx[i, j] = len(vs); vs.append((x, -r * math.cos(q), r * math.sin(q)))
    for i in range(48):
        for j in range(60):
            xm = (xs[i] + xs[i + 1]) / 2; pm = (phis[j] + phis[j + 1]) / 2
            if cut and CUT_X[0] < xm < CUT_X[1] and CUT_PHI[0] < pm < CUT_PHI[1]:
                continue
            fs.append((idx[i, j], idx[i + 1, j], idx[i + 1, j + 1], idx[i, j + 1]))
    return g.mesh(name, vs, fs, role)


def end_cap(name, sign, r, role):
    """Quarter sphere closing the vault at x = sign * HALF."""
    vs = []; fs = []; n = 30; m = 12
    for i in range(m + 1):
        t = (math.pi / 2) * i / m          # 0 at the vault joint, 90 at the pole
        for j in range(n + 1):
            ph = math.pi * j / n
            vs.append((sign * (HALF + r * math.sin(t)), -r * math.cos(t) * math.cos(ph), r * math.cos(t) * math.sin(ph)))
    for i in range(m):
        for j in range(n):
            a = i * (n + 1) + j
            fs.append((a, a + 1, a + n + 2, a + n + 1))
    return g.mesh(name, vs, fs, role)


def rack(y, x0, x1, side, tiers=(38, 92, 146, 200), top=252, depth=60, tray_h=8):
    """Rack row along x; one module per 120 cm."""
    mods = int((x1 - x0) / 120)
    for k in range(mods + 1):
        x = x0 + k * 120
        for dy in (-30, 30):
            rod('rack post', (x, y + dy * depth / 60, 0), (x, y + dy * depth / 60, top), 1.6)
        rod('rack top rail', (x, y - depth / 2, top), (x, y + depth / 2, top), 1.4, 'detail')
    for dy in (-depth / 2, depth / 2):
        rod('rack top rail', (x0, y + dy, top), (x1, y + dy, top), 1.4, 'detail')
    for z in tiers:
        box('grow tray', ((x0 + x1) / 2, y, z), (x1 - x0, depth, tray_h), 1.5)
        box('LED bar', ((x0 + x1) / 2, y, z + 44), (x1 - x0 - 10, 8, 2.4), .8, 'accent')
    for x in (x0 - 4, x1 + 4):
        tube('nutrient riser', [(x, y + side * 26, 20), (x, y + side * 26, 206)], 1.2, 'cable')


def plants(y, x0, x1, seed, tiers=(38, 92, 146, 200)):
    import random
    rnd = random.Random(seed)
    for z in tiers:
        x = x0 + 16
        while x < x1 - 12:
            base = Vector((x, y + rnd.uniform(-8, 8), z + 4))
            h = rnd.uniform(12, 20)
            for k in range(3):
                a = math.radians(120 * k + rnd.uniform(0, 60))
                leaf('crop leaf', base, base + Vector((h * .8 * math.cos(a), h * .8 * math.sin(a), h * .75)), h * .55, 'detail')
            x += rnd.uniform(34, 42)


def bags(y, x0, x1, z, h=18, stagger=0, role='structure'):
    x = x0 + stagger
    while x + 56 <= x1:
        box('regolith bag', (x + 28, y, z + h / 2), (56, 38, h), 7, role)
        x += 60


def build():
    from ..humans import human
    human('presence', .28, 0, (-75, 10, 12))
    views(B=(20, 14), C=(-34, 16))
    # --- envelope ------------------------------------------------------------------
    vault_surface('restraint net', R, 'structure')
    vault_surface('gas bladder', R - 6, 'shell')
    for sign in (-1, 1):
        end_cap('restraint end cap', sign, R, 'structure')
    # Inflated ribs: nine arcs outside the net, stopping at the ground.
    for k in range(9):
        x = -HALF + 2 * HALF * k / 8
        arc_tube('inflated rib', (x - 7, 0, 0), (1, 0, 0), (0, 1, 0), R + 16, 16, 14, 0, 180, 'structure', 60)
    # Restraint net: longitudinal straps between the ribs (visible lines on the skin).
    for ph in range(10, 180, 14):
        q = math.radians(ph)
        pts = [(x, -(R + .8) * math.cos(q), (R + .8) * math.sin(q)) for x in range(-HALF, HALF + 1, 50)]
        seg = []
        for p_ in pts:
            inside = CUT_X[0] < p_[0] < CUT_X[1] and CUT_PHI[0] < ph < CUT_PHI[1]
            if inside:
                if len(seg) > 1:
                    g.wire('restraint strap', seg, .3, 'detail')
                seg = []
            else:
                seg.append(p_)
        if len(seg) > 1:
            g.wire('restraint strap', seg, .3, 'detail')
    # Section edge: a cut through both layers, drawn as a clean frame.
    x0, x1 = CUT_X; p0, p1 = (math.radians(v) for v in CUT_PHI)
    for x in (x0, x1):
        g.wire('section edge', [(x, -(R + 2) * math.cos(math.radians(ph)), (R + 2) * math.sin(math.radians(ph))) for ph in range(CUT_PHI[0], CUT_PHI[1] + 1, 2)], .6, 'accent')
    # --- floor and racks -----------------------------------------------------------
    box('floor deck', (0, 0, 6), (2 * HALF - 20, 640, 12), 4)
    rack(185, -480, 240, 1)
    plants(185, -480, 240, 3)
    with group('B'):
        # One two-module section of the far row, with its tank, pump and drip manifold.
        rack(185, 240, 480, 1)
        plants(185, 240, 480, 11)
        for z in (38, 92, 146, 200):
            tube('drip manifold', [(244, 212, z + 7), (476, 212, z + 7)], .8, 'cable')
            for x in range(262, 470, 36):
                tube('drip line', [(x, 212, z + 7), (x, 206, z + 9)], .3, 'cable')
        cyl('nutrient tank', (530, 185, 12), 26, 70, 'structure', (0, 0, 1), 36)
        ring('tank band', (530, 185, 50), 26.8, 1, 1.6, (0, 0, 1), 'detail')
        motor((530, 152, 40), 7, 14, (0, -1, 0))
        tube('nutrient supply', [(530, 159, 30), (500, 196, 24), (484, 211, 22)], 1.2, 'cable')
        box('light driver', (360, 185, 232), (90, 30, 10), 2, 'detail')
    mark('GROW RACKS', (-150, 155, 150), 'RACKS AND DEEP BEDS / 42 m² OF CROPS')
    # Near row: two tiers of deep beds (potatoes), low enough to see the aisle.
    rack(-170, -480, 480, -1, tiers=(30, 84), top=132, depth=90, tray_h=16)
    plants(-170, -480, 480, 7, tiers=(38, 92))
    # --- side vestibule airlock (near side, +X) ---------------------------------------
    AX = 360
    frame = frame_matrix((AX, -R + 40, 118), (0, -1, 0), (1, 0, 0))   # local z outward, y up
    with group('C'), local(frame):
        ring('docking collar', (0, 0, 0), 106, 10, 34, (0, 0, 1), 'structure')
        # Open hull in segments (they occlude each other) and an end bulkhead
        # whose doorway is really open.
        for k in range(8):
            arc_tube('vestibule hull segment', (0, 0, 30), (0, 0, 1), (1, 0, 0), 98, 4, 180, 45 * k, 45 * k + 45, 'structure', 12)
        for z in (80, 150):
            ring('hull frame', (0, 0, z), 100, 3, 4, (0, 0, 1), 'detail')
        arc_tube('door bulkhead', (0, 0, 208), (0, 0, 1), (1, 0, 0), 98, 22, 4, 0, 360, 'structure', 64)
        ring('door frame', (0, 0, 212), 78, 6, 6, (0, 0, 1), 'structure')
        box('vestibule floor', (0, -70, 115), (150, 6, 170), 1.5, 'detail')
        # Outer pressure door, swung 100 degrees outward on its hinge.
        hinge = Vector((76, 0, 218))
        with at(hinge, 100, 'Y'):
            cyl('pressure door', Vector((-76, 0, 0)), 70, 9, 'structure', (0, 0, 1), 56)
            ring('door seal', Vector((-76, 0, -.6)), 66, 3, 1, (0, 0, -1), 'accent')
            cyl('door porthole', Vector((-76, 32, 9)), 14, 1.5, 'accent', (0, 0, 1), 32)
            ring('porthole bezel', Vector((-76, 32, 9.6)), 16, 3, 2, (0, 0, 1), 'detail')
            ring('handwheel', Vector((-76, -12, 11)), 19, 2.4, 2.4, (0, 0, 1), 'structure')
            for k in range(3):
                a = math.radians(120 * k + 90)
                rod('handwheel spoke', (-76, -12, 12), (-76 + 17 * math.cos(a), -12 + 17 * math.sin(a), 12), 1, 'detail')
        for dy in (-44, 36):
            cyl('door hinge', hinge + Vector((0, dy, 0)), 5, 16, 'structure', (0, 1, 0), 24)
        # Equalisation valve and gauge beside the frame.
        cyl('equalisation valve', (-88, 70, 206), 7, 12, 'structure', (0, 0, 1), 24)
        ring('valve handle', (-88, 70, 219), 9, 1.4, 1.4, (0, 0, 1), 'accent')
        box('pressure gauge', (-92, 44, 212), (12, 12, 4), 2, 'detail')
        # Bench and suit hooks on the inner +X wall, seen through the doorway.
        box('vestibule bench', (62, -44, 115), (30, 8, 130), 2)
        for z in (70, 160):
            box('bench leg', (62, -58, z), (26, 26, 6), 1, 'detail')
        for z in (70, 105, 140, 175):
            loft('suit hook', [(84, 58, z), (74, 58, z), (72, 50, z)], 1.2, 8, 'detail')
        box('entry ramp', (0, -114, 290), (140, 8, 150), 2)
        for z in (245, 290, 335):
            box('ramp tread', (0, -109, z), (136, 2, 6), .5, 'detail')
    mark('AIRLOCK', frame @ Vector((-100, 40, 120)), 'SIDE VESTIBULE / OUTER DOOR OPEN')
    # --- radiator on its own stand (-X) and berm ------------------------------------
    rx = -HALF - R - 70
    rframe = frame_matrix((rx, -150, 0), (0, -1, 0), (1, 0, 0))
    with local(rframe):
        with at((0, 190, 0), -14, 'X'):
            box('radiator panel', (0, 0, 0), (300, 170, 3), 1.5)
            for x in (-150, 150):
                box('panel edge rail', (x, 0, 1.5), (5, 172, 5), 1, 'detail')
            for yy in (-85, 85):
                loft('coolant header', [(-152, yy, 3), (152, yy, 3)], 3, 12, 'structure', False)
            for k in range(1, 15):
                g.wire('heat pipe', [(-150 + 300 * k / 15, -82, 2.2), (-150 + 300 * k / 15, 82, 2.2)], .15, 'detail')
        for x in (-120, 120):
            rod('stand leg', (x, 0, -40), (x, 105, 8), 3)
            rod('stand leg', (x, 0, 40), (x, 105, 8), 3)
            box('stand foot', (x, 3, 0), (24, 6, 100), 2, 'detail')
            rod('stand post', (x, 105, 8), (x, 110, 18), 2.4)
        rod('stand cross brace', (-120, 60, 18), (120, 60, 18), 2)
    tube('coolant loop', [rframe @ Vector((150, 110, 0)), (-HALF - R + 10, -60, 20), (-HALF - R + 60, -60, 60)], 2, 'cable')
    tube('base power line', [(-HALF - R - 20, 220, 8), (-HALF - 200, 420, 4), (-HALF - 360, 600, 2)], 1.6, 'cable')
    for layer, (z, st) in enumerate(((0, 0), (18, 30))):
        bags(-R - 26, -HALF - 30, AX - 130, z, 18, st)
        bags(-R - 26, AX + 130, HALF + 20, z, 18, st)
    bags(R + 26, -HALF - 30, HALF + 20, 0, 18, 0)
    mark('REGOLITH BERM', (-HALF + 90, -R - 45, 30), 'BAGS OF LOCAL SOIL / SHADE AND WIND ANCHOR')
    mark('INFLATED RIB', (-HALF + 150 - 7, -(R + 16) * math.cos(math.radians(62)), (R + 16) * math.sin(math.radians(62))), 'ONE OF NINE / HOLDS THE SHAPE IF THE AIR IS LET OUT')
    mark('CREW MEMBER', (-75, -6, 176), 'SHIRTSLEEVES / 50 kPa, 30 % OXYGEN')
    mark('RADIATOR', rframe @ Vector((-150, 250, 0)), 'SHEDS 3 kW OF LAMP HEAT')
    return 20, 28
