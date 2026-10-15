"""LIBRARY BEACON: wheeled library trunk with solar wings and a mesh mast.

Units are centimetres. X along the trunk (left to right), Y depth (front is
-Y), Z up, ground at z = 0. The rugged trunk (104 x 62 x 34 cm base, 12 cm
lid) rides on two wheels and two feet. Its lid opens back 100 degrees and
carries two racks of twenty tablets standing like books; the server core sits
under a vented deck plate. Two solar wings (88 x 60 cm, 120 W each) unfold
from hinges along the top of the trunk's ends, held by folding struts; near
the equator they work almost flat. A three-section telescoping mast stands
in a yoke on the trunk's back, 2.05 m to the head, braced by the trunk and two
guy lines to stakes placed symmetrically either side.
"""
from ..kit import *
from .parts import loft

CW, CD, CH, LH = 104, 62, 34, 12
BASE_Z = 12
TOP = BASE_Z + CH
HINGE_Y = CD / 2
MAST = Vector((0, 58, 0))
HEAD = 205
GUY_Z = 180
ASPECT_AZ = 26
WING = 88
DIHEDRAL = 10


def rounded_rect(w, d, r, n=6):
    pts = []
    for cx, cy, a0 in ((w / 2 - r, d / 2 - r, 0), (-w / 2 + r, d / 2 - r, 90), (-w / 2 + r, -d / 2 + r, 180), (w / 2 - r, -d / 2 + r, 270)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def open_tray(name, c, w, d, h, r=6, wall=2.2, role='structure'):
    """Rounded open-top trunk body: real walls and floor, so the core is visible."""
    outer = rounded_rect(w, d, r); inner = rounded_rect(w - 2 * wall, d - 2 * wall, r - wall)
    m = len(outer); vs = []; fs = []
    cx, cy, cz = c
    for (x, y) in outer: vs.append((cx + x, cy + y, cz))
    for (x, y) in outer: vs.append((cx + x, cy + y, cz + h))
    for (x, y) in inner: vs.append((cx + x, cy + y, cz + h))
    for (x, y) in inner: vs.append((cx + x, cy + y, cz + wall))
    for k in range(m):
        k1 = (k + 1) % m
        fs.append((k, k1, m + k1, m + k))
        fs.append((m + k, m + k1, 2 * m + k1, 2 * m + k))
        fs.append((2 * m + k, 2 * m + k1, 3 * m + k1, 3 * m + k))
    fs.append(tuple(reversed(range(m))))
    fs.append(tuple(3 * m + k for k in range(m)))
    return g.mesh(name, vs, fs, role)


def solar_wing(side):
    """Panel hinged on the trunk end, 10 degrees of dihedral, folding strut below."""
    hx = side * (CW / 2 + 1.5); hz = TOP - 1.5
    with at((hx, 0, hz), -side * DIHEDRAL, 'Y'):
        x0 = side * 1.5; xm = side * (WING / 2 + 1.5)
        box('solar wing frame', (xm, 0, 0), (WING, 60, 3.4), 1.4)
        for i in range(1, 8):
            xx = x0 + side * WING * i / 8
            g.wire('cell seam', [(xx, -28, 1.75), (xx, 28, 1.75)], .08, 'shell')
        for j in range(1, 5):
            yy = -30 + 60 * j / 5
            g.wire('cell seam', [(x0 + side * 2, yy, 1.75), (x0 + side * (WING - 2), yy, 1.75)], .08, 'shell')
        box('junction box', (side * 14, 18, -2.8), (10, 7, 2.4), .8, 'detail')
        box('wing grip', (side * (WING + 2.5), 0, 0), (3, 16, 2.4), .8, 'detail')
        for y in (-22, 22):
            cyl('wing hinge', (0, y - 5, 0), 1.6, 10, 'structure', (0, 1, 0), 16)
    # Folding strut: trunk foot to the wing's underside at 55 cm, with a knuckle.
    q = math.radians(DIHEDRAL)
    for y in (-20, 20):
        a = Vector((side * (CW / 2 + 1), y, BASE_Z + 7))
        b = Vector((hx + side * 55 * math.cos(q), y, hz + 55 * math.sin(q) - 2))
        mid = a.lerp(b, .5) + Vector((side * 1.5, 0, -1))
        rod('wing strut', a, mid, 1.3, 'structure'); rod('wing strut', mid, b, 1.3, 'structure')
        cyl('strut knuckle', mid + Vector((0, -1.8, 0)), 1.9, 3.6, 'detail', (0, 1, 0), 16)
    tube('wing lead', [(side * 14 + hx, 18, hz - 4), (side * (CW / 2 - 2), 26, TOP - 8)], .5, 'cable')


def tablet_rack(x0, frame):
    """Twenty tablets standing in charging slots, like books on a shelf."""
    b = len(g.parts); w = len(g.wires)
    box('rack tray', (x0 + 17, -5, 13), (37, 11, 3.4), 1.4)
    for i in range(20):
        x = x0 + 1 + i * 1.75
        box('tablet', (x, -7, 25), (1.0, 12.4, 21), .4, 'detail' if i % 5 else 'structure')
        cyl('charge contact', (x, -7, 14.8), .3, .4, 'accent', (0, 0, 1), 8)
    rod('retaining bar', (x0 - 1.5, -14, 30), (x0 + 35.5, -14, 30), .6, 'detail')
    box('rack label card', (x0 + 17, -.7, 44), (16, 1, 6), .6, 'shell')
    transform(b, w, frame)


def build():
    views(B=(16, 70), C=(24, 12))
    # --- telescoping mast: three stepped sections, collars, clamp levers --------------------
    sections = [(4, 116, 4.4), (110, 158, 3.5), (152, HEAD - 6, 2.7)]
    for z0, z1, r in sections:
        cyl('mast section', MAST + Vector((0, 0, z0)), r, z1 - z0, 'structure', (0, 0, 1), 36)
    for (z0, z1, r), (_, _, r_next) in zip(sections, sections[1:]):
        ring('section collar', MAST + Vector((0, 0, z1 - 9)), r + 2.2, 2.2 + r - r_next, 9, (0, 0, 1))
        ring('collar lip', MAST + Vector((0, 0, z1 - 10)), r + 2.8, .8, 1.2, (0, 0, 1), 'detail')
        q = math.radians(ASPECT_AZ + 180)
        dx = Vector((math.cos(q), math.sin(q), 0))
        rod('clamp lever', MAST + dx * (r + 2.2) + Vector((0, 0, z1 - 4.5)), MAST + dx * (r + 7.5) + Vector((0, 0, z1 - 12)), 1.1, 'structure')
        box('lever pad', MAST + dx * (r + 7.8) + Vector((0, 0, z1 - 12.8)), (3, 3, 3), .8, 'accent')
    cyl('mast foot pad', MAST, 10, 4, 'structure', (0, 0, 1), 40)
    # Socket bracket: a cast yoke on the trunk's back carries the mast.
    for z in (BASE_Z + 7, TOP - 8):
        box('socket yoke arm', (0, (HINGE_Y + MAST.y) / 2, z), (16, MAST.y - HINGE_Y, 5), 1.6, 'structure')
        ring('socket clamp', MAST + Vector((0, 0, z - 4)), 6.6, 2.2, 8, (0, 0, 1))
    box('socket back plate', (0, HINGE_Y + 1.4, BASE_Z + 18), (26, 2.8, 26), 1.4, 'structure')
    for x in (-9, 9):
        for z in (BASE_Z + 9, BASE_Z + 27):
            cyl('plate bolt', (x, HINGE_Y + 2.8, z), 1, 1.2, 'detail', (0, 1, 0), 8)
    # Two guy lines to two stakes, symmetric about the mast as the viewer sees it.
    stakes = []
    top = MAST + Vector((0, 0, GUY_Z))
    q = math.radians(ASPECT_AZ)
    right = Vector((math.cos(q), math.sin(q), 0)); away = Vector((-math.sin(q), math.cos(q), 0))
    for side in (-1, 1):
        p = MAST + right * side * 128 + away * 40
        stakes.append(p)
        rod('ground stake', p + Vector((0, 0, -2)), p + Vector((0, 0, 12)), 1.1, 'structure')
        ring('stake eye', p + Vector((0, 0, 12)), 2.2, .7, .8, (1, 0, 0), 'detail')
        tube('guy line', [top.lerp(p + Vector((0, 0, 12)), .05), p + Vector((0, 0, 12))], .45, 'cable')
        box('line tensioner', top.lerp(p + Vector((0, 0, 12)), .86), (3, 3, 6), .8, 'detail')
    # --- C: mast head ---------------------------------------------------------------------
    with group('C'):
        cyl('upper mast section', MAST + Vector((0, 0, GUY_Z - 24)), 2.7, HEAD - 6 - GUY_Z + 24, 'structure', (0, 0, 1), 36)
        ring('guy ring', top, 5.2, 2.2, 3.2, (0, 0, 1))
        for p in stakes:
            tube('guy line lead', [top + (p + Vector((0, 0, 10)) - top).normalized() * 4, top.lerp(p + Vector((0, 0, 10)), .05)], .4, 'cable')
        hp = MAST + Vector((0, 0, HEAD - 6))
        cyl('head plate', hp, 17, 2.2, 'structure', (0, 0, 1), 56)
        ring('head clamp', hp + Vector((0, 0, -6)), 3, 1.4, 6, (0, 0, 1))
        for a in (90, 210, 330):
            q = math.radians(a); d = Vector((math.cos(q), math.sin(q), 0))
            c = hp + d * 13 + Vector((0, 0, 20))
            with at(c, a - 90, 'Z'):
                box('sector antenna', (0, 0, 0), (11, 4, 38), 1.6, 'structure')
                for z in (-12.6, -4.2, 4.2, 12.6):
                    box('radiating patch', (0, 2.05, z), (6, .3, 6), .3, 'shell')
                box('tilt bracket', (0, -3.6, -13), (4.4, 3.2, 5.6), .8, 'detail')
            rod('antenna arm', hp + d * 3 + Vector((0, 0, 2.2)), hp + d * 10.6 + Vector((0, 0, 7)), 1.2, 'detail')
        cyl('omni whip', hp + Vector((0, 0, 2.2)), .7, 40, 'structure', (0, 0, 1), 12)
        cyl('whip base', hp + Vector((0, 0, 1.8)), 1.6, 4.5, 'detail', (0, 0, 1), 16)
        box('mesh radio', hp + Vector((0, -6.4, -15)), (10, 5.6, 15), 1.6, 'structure')
        for z in (-20.5, -18.3, -16.1, -13.9, -11.7, -9.5):
            box('radio fin', hp + Vector((0, -9.5, z)), (9, .9, .7), .25, 'detail')
        cyl('status lamp', hp + Vector((0, -9.6, -5.6)), .9, .6, 'accent', (0, -1, 0), 12)
        tube('radio feed', [hp + Vector((0, -3.6, -22.6)), MAST + Vector((0, -2.1, GUY_Z - 8)), MAST + Vector((0, -2.1, GUY_Z - 24))], .45, 'cable')
    tube('mast feed cable', [MAST + Vector((0, -3.2, GUY_Z - 24)), MAST + Vector((0, -4.2, 150)), MAST + Vector((0, -5.2, 90)), MAST + Vector((0, -5.6, TOP)), (8, HINGE_Y + 3, TOP - 5)], .55, 'cable')
    # --- B: the trunk and its core -------------------------------------------------------------
    with group('B'):
        open_tray('trunk base shell', (0, 0, BASE_Z), CW, CD, CH)
        f = BASE_Z + 2.2
        # Rear: four LiFePO4 modules under busbars and the battery board; fanless server.
        for i in range(4):
            x = -44 + i * 11
            box('battery module', (x, 13, f + 9), (10, 26, 18), .9)
            for yy in (4, 22):
                cyl('module terminal', (x, yy, f + 18), 1.1, 1.6, 'accent', (0, 0, 1), 12)
        for yy in (4, 22):
            box('busbar', (-27.5, yy, f + 19.8), (36, 2, .7), .2, 'detail')
        box('battery management board', (-27.5, 13, f + 19.2), (30, 10, .9), .3, 'detail')
        box('server board', (26, 13, f + 1.6), (36, 26, 1.4), .3, 'structure')
        box('processor sink base', (21, 13, f + 3.6), (16, 16, 2.4), .6, 'structure')
        for x in range(14, 29, 2):
            box('sink fin', (x, 13, f + 8.4), (.7, 15, 7.4), .2, 'detail')
        for y in (3, 23):
            box('memory module', (37, y, f + 3.4), (11, 1.4, 3.8), .2, 'detail')
        for x in (0, 6):
            box('drive sled', (x, -9, f + 4.6), (4.6, 18, 9), .7, 'structure')
            cyl('sled pull tab', (x, -18.4, f + 7.4), 1.1, 1.2, 'accent', (0, -1, 0), 10)
        box('charge controller', (-30, -11, f + 6), (24, 16, 12), 1.4, 'structure')
        box('controller display', (-30, -19.2, f + 8.4), (11, .5, 5), .4, 'shell')
        for x in range(-38, -21, 3):
            cyl('terminal screw', (x, -11, f + 12.2), .7, .6, 'detail', (0, 0, 1), 8)
        box('tablet charge hub', (30, -13, f + 3), (32, 11, 6), 1, 'structure')
        for i in range(12):
            box('charge port', (17 + i * 2.4, -18.7, f + 3.6), (1.5, .6, 1), .2, 'accent')
        tube('lid harness', [(30, -9, f + 6), (33, 2, f + 14), (36, 24, TOP - 5), (36, HINGE_Y, TOP + 3)], 1.1, 'cable')
        tube('wing input', [(-50, -8, f + 14), (-44, -11, f + 11), (-38, -11, f + 12)], .6, 'cable')
        tube('battery feed', [(-27, 4, f + 20), (-29, -2, f + 15), (-30, -5, f + 12)], .6, 'cable')
    # Trunk furniture outside the core: corner guards, ribs, deck plate, latches.
    for x in (-CW / 2 + 5, CW / 2 - 5):
        for y in (-CD / 2 + 5, CD / 2 - 5):
            cyl('corner guard', (x, y, BASE_Z - .5), 6.6, CH + 1, 'structure', (0, 0, 1), 32)
    for z in (BASE_Z + 6, BASE_Z + 27):
        box('front rib', (0, -CD / 2 - .6, z), (CW - 26, 1.6, 2.6), .7, 'detail')
    # Label plate: school, unit number, and the month of the last update.
    box('label plate', (-22, -CD / 2 - .9, BASE_Z + 16.5), (30, 1.2, 12), 1, 'structure')
    for k, w in enumerate((22, 16, 19)):
        g.wire('label line', [(-22 - 11 + (22 - w) / 2 - 0 + 0, -CD / 2 - 1.6, BASE_Z + 20 - k * 3.3), (-22 - 11 + (22 - w) / 2 + w, -CD / 2 - 1.6, BASE_Z + 20 - k * 3.3)], .18, 'detail')
    for x in (-35.5, -8.5):
        cyl('plate rivet', (x, -CD / 2 - 1.6, BASE_Z + 16.5), .7, .6, 'detail', (0, -1, 0), 8)
    # Recessed front carry handle.
    box('handle recess', (22, -CD / 2 - .3, BASE_Z + 18), (26, 1, 9), 2, 'detail')
    loft('front carry handle', [(12, -CD / 2 - .6, BASE_Z + 19), (13.5, -CD / 2 - 4, BASE_Z + 19), (30.5, -CD / 2 - 4, BASE_Z + 19), (32, -CD / 2 - .6, BASE_Z + 19)], 1.3, 12, 'structure')
    box('deck plate', (0, 0, TOP - .7), (CW - 6, CD - 6, 1.6), 1.4, 'structure')
    for i in range(8):
        box('vent slot', (26, -16 + i * 4.2, TOP + .2), (28, 1.4, .5), .25, 'detail')
    for i in range(10):
        box('deck charge port', (-40 + i * 4, -22, TOP + .2), (2.4, 1.1, .5), .25, 'accent')
    cyl('power switch', (-4, -22, TOP + .1), 1.9, .9, 'detail', (0, 0, 1), 16)
    box('status window', (-26, 8, TOP + .1), (22, 10, .5), .7, 'shell')
    for x in (-30, 30):
        box('draw latch', (x, -CD / 2 - 1.4, TOP - 5), (9, 2.4, 7), 1, 'accent')
    loft('end carry handle', [(-CW / 2 - 1, -10, TOP - 12), (-CW / 2 - 5.5, -9, TOP - 12), (-CW / 2 - 5.5, 9, TOP - 12), (-CW / 2 - 1, 10, TOP - 12)], 1.2, 10, 'detail')
    for y in (-22, 22):
        cyl('trunk wheel', (CW / 2 - 3, y + (4 if y > 0 else -4), 8), 8, 5, 'structure', (0, 1 if y > 0 else -1, 0), 40)
        ring('wheel hub', (CW / 2 - 3, y + (9.4 if y > 0 else -9.4), 8), 3.6, 1.2, 1.2, (0, 1 if y > 0 else -1, 0), 'detail')
    for y in (-22, 22):
        box('rubber foot', (-CW / 2 + 12, y, BASE_Z - 3.5), (9, 9, 7), 1.6, 'detail')
    for y in (-9, 9):
        rod('pull handle tube', (CW / 2 + 1.2, y, BASE_Z + 5), (CW / 2 + 1.2, y, TOP - 3), 1.1, 'detail')
    loft('pull handle grip', [(CW / 2 + 1.2, -9, TOP - 3), (CW / 2 + 1.2, -7, TOP + 1), (CW / 2 + 1.2, 7, TOP + 1), (CW / 2 + 1.2, 9, TOP - 3)], 1.5, 12, 'structure')
    # Lid, opened 100 degrees about the rear hinge; racks in the lid's frame.
    lid = Matrix.Translation((0, HINGE_Y, TOP)) @ Matrix.Rotation(math.radians(-100), 4, 'X') @ Matrix.Translation((0, -HINGE_Y, -TOP))
    b = len(g.parts); w = len(g.wires)
    box('trunk lid shell', (0, 0, TOP + LH / 2), (CW, CD, LH), 6)
    for x in (-CW / 2 + 16, CW / 2 - 16):
        box('lid rib', (x, 0, TOP + LH + .4), (3.2, CD - 10, 1.4), .6, 'detail')
    transform(b, w, lid)
    for side in (-1, 1):
        cyl('lid hinge', (side * 34 - 7, HINGE_Y + 1, TOP - .8), 1.7, 14, 'structure', (1, 0, 0), 16)
        rod('lid stay', (side * 47, 18, TOP - 3), (side * 47, 34, TOP + 30), .8, 'detail')
    face = Matrix.Translation((0, HINGE_Y + 1.8, TOP)) @ Matrix.Rotation(math.radians(-10), 4, 'X')
    for x0 in (-42, 6):
        tablet_rack(x0, face)
    for side in (-1, 1):
        solar_wing(side)
    # --- anchors -----------------------------------------------------------------------------
    q = math.radians(210)
    mark('MESH MAST', MAST + Vector((17 * math.cos(q), 17 * math.sin(q), HEAD + 26)), '2.1 m / THREE SECTIONS / 200 m ACROSS THE SCHOOL')
    mark('TABLET RACKS', (-43, HINGE_Y - 4, TOP + 32), 'FORTY TABLETS / CHARGED EVERY NIGHT')
    qd = math.radians(DIHEDRAL)
    mark('SOLAR WINGS', (-(CW / 2 + 1.5) - (WING + 3) * math.cos(qd), -14, TOP - 1.5 + (WING + 3) * math.sin(qd) + 1.2), '2 x 120 W / UNFOLD IN A MINUTE')
    mark('SERVER CORE', (40, -24, TOP + .3), 'UNDER THE DECK / 2 x 4 TB MIRRORED / 9 W')
    mark('GUY LINES', top.lerp(stakes[1] + Vector((0, 0, 12)), .55), 'TWO STAKES / UP IN TEN MINUTES')
    mark('TRUNK WHEELS', (CW / 2 - 3, -31, 5), '46 kg / ONE PERSON PULLS IT ACROSS THE YARD')
    return ASPECT_AZ, 12
