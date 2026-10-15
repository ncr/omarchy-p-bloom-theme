"""CLEAR SIGHT: a 20 ft shipping container fitted as a cataract theatre.

Units are centimetres. X along the container (doors at +X), Y across
(the opened long side faces -Y), Z up; ground at z = 0, container floor
underside on four levelling jacks at z = 30. ISO 20 ft: 606 x 244 x 259.
The -Y side panel is lifted into a solar awning; a fold-out grating deck
with rails and steps serves as the shaded waiting area. Behind a sealed
glazed clean-room wall: operating table, floor-stand microscope (B) and
the lens bench on the far-wall counter (C). HEPA air handler on the roof.
"""
from ..kit import *
from .parts import loft, sphere, wing

L, WD, H = 606, 244, 259
Z0 = 30                      # container underside
FL = Z0 + 15                 # floor surface
TOP = Z0 + H
X0, X1 = -L / 2, L / 2
YN, YF = -WD / 2, WD / 2     # near (open) side, far side
OPEN = (-222, 222)           # opening in the near wall
AW = 40                      # awning angle above horizontal, degrees


def frame():
    for x in (X0 + 8, X1 - 8):
        for y in (YN + 8, YF - 8):
            box('corner post', (x, y, Z0 + H / 2), (16, 16, H), 1.5)
            for z in (Z0 + 6, TOP - 6):
                box('corner casting', (x, y, z), (18, 17, 12), 1.2)
                cyl('casting aperture', (x, y - 8.6 if y < 0 else y + 8.6, z), 2.6, .6, 'detail', (0, -1 if y < 0 else 1, 0), 16)
    for y in (YN + 8, YF - 8):
        box('bottom side rail', (0, y, Z0 + 8), (L - 36, 12, 16), 1.5)
        box('top side rail', (0, y, TOP - 7), (L - 36, 12, 14), 1.5)
    for x in (X0 + 8, X1 - 8):
        box('bottom end rail', (x, 0, Z0 + 8), (12, WD - 34, 16), 1.5)
        box('top end rail', (x, 0, TOP - 7), (12, WD - 34, 14), 1.5)


def corrugated_panel(x0, x1, y, z0, z1, pitch=27.6, depth=3.6):
    """Near-side wall section: flat skin with trapezoid ribs as raised bands."""
    box('side wall skin', ((x0 + x1) / 2, y + 1, (z0 + z1) / 2), (x1 - x0, 2, z1 - z0), .5)
    n = int((x1 - x0) / pitch)
    for i in range(n):
        x = x0 + pitch * (i + .5) + ((x1 - x0) - n * pitch) / 2
        box('corrugation rib', (x, y - depth / 2, (z0 + z1) / 2), (pitch * .42, depth, z1 - z0 - 2), .6, 'detail')


def doors():
    """ISO end doors at +X: two leaves, vertical ribs, four lock bars, hinges."""
    x = X1 + 1
    for side in (-1, 1):
        yc = side * 59
        box('door leaf', (x, yc, Z0 + H / 2), (3, 116, H - 30), 1, 'structure')
        for k in range(4):
            box('door rib', (x + 1.8, yc - 42 + k * 28, Z0 + H / 2), (1.8, 11, H - 44), .5, 'detail')
        for yy in (yc - 20 * side, yc + 30 * side):
            yb = yy
            cyl('lock bar', (x + 4.2, yb, Z0 + 18), 1.6, H - 36, 'structure', (0, 0, 1), 12)
            for z in (Z0 + 16, TOP - 16):
                box('cam keeper', (x + 4, yb, z), (5, 6, 6), 1, 'detail')
            box('lock handle', (x + 5.6, yb + side * 8, Z0 + 110), (2.4, 18, 3.4), 1, 'accent')
            box('handle retainer', (x + 5, yb + side * 16, Z0 + 110), (3, 4, 8), .8, 'detail')
        for z in (Z0 + 40, Z0 + 100, Z0 + 160, Z0 + 220):
            box('door hinge', (x + 2.5, side * 112, z), (5, 7, 9), 1, 'detail')


def roof():
    box('roof skin', (0, 0, TOP + 1), (L - 36, WD - 34, 2), .5)
    for i in range(20):
        x = X0 + 30 + i * 28.5
        box('roof corrugation', (x, 0, TOP + 2.8), (12, WD - 40, 1.4), .5, 'detail')
    # HEPA air handler at the -X end, fan on top, louvred intake on the near face.
    with group('AHU'):
        cx = X0 + 82
        box('air handler casing', (cx, 8, TOP + 26), (132, 176, 46), 8)
        box('casing plinth', (cx, 8, TOP + 3.5), (140, 184, 3), 1, 'detail')
        for k in range(10):
            box('intake louvre', (cx - 49.5 + k * 11, -80.6, TOP + 26), (8, 2.4, 28), .5, 'detail')
        box('louvre frame', (cx, -80.4, TOP + 26), (122, 1.2, 34), .8, 'detail')
        cyl('fan shroud', (cx + 20, 34, TOP + 49), 24, 7, 'structure', (0, 0, 1), 48)
        for a in range(0, 180, 30):
            q = math.radians(a)
            rod('fan guard', (cx + 20 - 21 * math.cos(q), 34 - 21 * math.sin(q), TOP + 56.4), (cx + 20 + 21 * math.cos(q), 34 + 21 * math.sin(q), TOP + 56.4), .5, 'detail')
        ring('fan guard rim', (cx + 20, 34, TOP + 55.6), 23, 1.6, 1.4)
        cyl('fan hub', (cx + 20, 34, TOP + 55), 5, 2, 'detail', (0, 0, 1), 24)
        # Supply duct drops through the roof into the ceiling diffuser.
        cyl('supply duct', (cx + 40, -30, TOP - 14), 11, 17, 'structure', (0, 0, 1), 32)
    # Roof solar array on low tilt frames (the rest of the roof).
    for i in range(3):
        x = X0 + 180 + i * 128
        with at((x, 4, TOP + 16), -8, 'X'):
            box('roof solar module', (0, 0, 0), (118, 196, 4), 1.5)
            for k in range(1, 6):
                box('cell string', (-59 + k * 19.6, 0, 2.5), (.8, 192, .8), .2, 'detail')
            box('module frame bar', (0, 0, 2.5), (116, .8, .8), .2, 'detail')
        for y in (-80, 88):
            rod('solar stand', (x, y, TOP + 2), (x, y, TOP + 16 + (y / 196) * 2 * 8 * .17), 1.6, 'detail')


def awning():
    """The near side panel, lifted about its top hinge and clad in PV."""
    depth = 225; x0, x1 = OPEN
    q = math.radians(AW)
    hinge = Vector((0, YN - 2, TOP - 4))
    out = Vector((0, -math.cos(q), math.sin(q)))
    up = Vector((0, math.sin(q), math.cos(q)))
    c = hinge + out * depth / 2
    # Build in a local frame then place: X along the container, Y outward.
    m = Matrix.Translation(c) @ Matrix(((1, 0, 0, 0), (0, out.y, up.y, 0), (0, out.z, up.z, 0), (0, 0, 0, 1)))
    b = len(g.parts); w = len(g.wires)
    box('awning panel', (0, 0, 0), (x1 - x0 + 8, depth, 6), 2)
    for k in range(4):
        xx = x0 + (x1 - x0) * (k + .5) / 4
        box('awning PV module', (xx, 0, 3.8), ((x1 - x0) / 4 - 8, depth - 16, 1.6), 1)
        for j in range(1, 5):
            box('awning cell string', (xx, -depth / 2 + 8 + j * (depth - 16) / 5, 4.9), ((x1 - x0) / 4 - 12, .7, .5), .2, 'detail')
    box('awning edge beam', (0, depth / 2 - 3, -5), (x1 - x0 + 8, 6, 8), 1.5)
    # Glass-glass bifacial modules: the cell strings read from beneath too.
    for k in range(4):
        xx = x0 + (x1 - x0) * (k + .5) / 4
        for j in range(1, 5):
            box('underside cell string', (xx, -depth / 2 + 8 + j * (depth - 16) / 5, -3.4), ((x1 - x0) / 4 - 12, .7, .5), .2, 'detail')
    for yy in (-depth / 4, depth / 4):
        box('awning purlin', (0, yy, -5.5), (x1 - x0 - 10, 5, 5), 1)
    for k in range(5):
        box('awning rafter', (x0 + (x1 - x0) * k / 4, 0, -4.5), (4, depth - 8, 3), .8, 'detail')
    transform(b, w, m)
    for x in (x0 + 20, x1 - 20):
        cyl('awning hinge knuckle', hinge + Vector((x - 14, 0, 0)), 2.6, 28, 'detail', (1, 0, 0), 16)
    # Two gas struts from the corner-post region to the awning's outer beam.
    tip_ = hinge + out * (depth - 12) - up * 6
    for x in (x0 + 30, x1 - 30):
        a = Vector((x, YN - 3, FL + 150)); bpt = Vector((x, tip_.y, tip_.z))
        rod('awning strut', a, bpt, 2.2)
        cyl('strut cylinder', a, 3.4, (bpt - a).length * .45, 'structure', tuple((bpt - a).normalized()), 16)
    return hinge, out, depth


def deck():
    """Fold-out grating deck with rails and steps: the shaded waiting area."""
    x0, x1 = OPEN; d = 170; yo = YN - d
    box('deck grating', (0, YN - d / 2, FL - 3), (x1 - x0, d, 6), 1)
    for i in range(1, 16):
        x = x0 + (x1 - x0) * i / 16
        box('grating bar', (x, YN - d / 2, FL + .55), (1.2, d - 6, .9), .2, 'detail')
    box('deck hinge beam', (0, YN - 3, FL - 6), (x1 - x0, 6, 8), 1)
    box('deck edge beam', (0, yo + 3, FL - 7), (x1 - x0, 6, 10), 1)
    for x in (x0 + 10, 0, x1 - 10):
        box('deck leg', (x, yo + 10, (FL - 8) / 2), (7, 7, FL - 8), 1.2)
        box('leg foot plate', (x, yo + 10, 1), (18, 18, 2), .6, 'detail')
        cyl('leg screw', (x, yo + 10, FL - 26), 1.6, 12, 'detail', (0, 0, 1), 10)
    # Guard rail along the outer edge and the +X end; opening for the steps at -X.
    rail_z = FL + 100
    posts = [x0 + 90 + i * (x1 - x0 - 100) / 4 for i in range(5)]
    for x in posts:
        rod('rail post', (x, yo + 4, FL), (x, yo + 4, rail_z), 1.6)
    loft('top rail', [(x0 + 90, yo + 4, rail_z), (x1 - 4, yo + 4, rail_z), (x1 - 4, YN - 6, rail_z)], 1.9, 12, 'structure', False)
    loft('knee rail', [(x0 + 90, yo + 4, FL + 50), (x1 - 4, yo + 4, FL + 50), (x1 - 4, YN - 6, FL + 50)], 1.2, 10, 'detail', False)
    rod('end rail post', (x1 - 4, YN - 6, FL), (x1 - 4, YN - 6, rail_z), 1.6)
    # Three steps down at the -X end, with a hand rail on the open side.
    steps = []
    for k in range(3):
        z = FL - (k + 1) * 11.25 - 0
        x = x0 - 18 - k * 28
        box('step tread', (x, yo + 55, z), (28, 110, 4), 1)
        steps.append((x, z))
    for y in (yo, yo + 110):
        loft('stair stringer', [(x0 + 2, y, FL - 4), (x0 - 18 - 3 * 28, y, 2)], 1.8, 10, 'structure', False)
    loft('stair hand rail', [(x0 + 90, yo + 4, rail_z), (x0 - 4, yo + 4, rail_z), (x0 - 100, yo + 4, rail_z - 42)], 1.9, 12, 'structure')
    for x in (x0 - 4, x0 - 70):
        z = FL if x > x0 - 10 else 12
        rod('stair rail post', (x, yo + 4, z), (x, yo + 4, rail_z - (0 if x > x0 - 10 else 31)), 1.5)
    # Waiting bench near the steps, facing out from the shade.
    bx = x0 + 70
    box('bench seat', (bx, yo + 45, FL + 44), (120, 38, 5), 2)
    box('bench back', (bx, yo + 64, FL + 70), (120, 4, 30), 2)
    for x in (bx - 52, bx + 52):
        box('bench frame', (x, yo + 50, FL + 22), (4, 36, 44), 1.2, 'detail')
    return yo


def glazing():
    """Sealed clean-room glazing set back in the opening; sliding door at +X."""
    x0, x1 = OPEN; y = YN + 10
    box('glazing sill', (0, y, FL + 4), (x1 - x0, 8, 8), 1)
    box('glazing head', (0, y, TOP - 26), (x1 - x0, 8, 10), 1)
    mull = [x0, x0 + 110, x0 + 220, x0 + 330, x1]
    for x in mull:
        box('glazing mullion', (x, y, (FL + TOP - 22) / 2), (6, 8, TOP - 22 - FL), .8)
    # Sliding door leaf in the last bay: frame, pull handle.
    dx = (x0 + 330 + x1) / 2
    for zz in (FL + 8, FL + 210):
        box('door leaf rail', (dx, y - 6, zz), (98, 3, 5), .6, 'detail')
    for xx in (dx - 47, dx + 47):
        box('door leaf stile', (xx, y - 6, FL + 109), (5, 3, 204), .6, 'detail')
    box('door pull', (dx - 38, y - 9, FL + 105), (3, 3, 36), 1, 'accent')
    # Reflection glints: short diagonals on the panes (shell weight).
    for x in (x0 + 55, x0 + 165, x0 + 275):
        tube('glass glint', [(x - 20, y - 4.5, FL + 190), (x + 12, y - 4.5, FL + 222)], .1, 'shell')
        tube('glass glint', [(x - 8, y - 4.5, FL + 184), (x + 16, y - 4.5, FL + 208)], .1, 'shell')


def theatre():
    # Far wall lining, ceiling light, partition to the anteroom at +X.
    box('far wall lining', (0, YF - 14, (FL + TOP) / 2), (L - 40, 3, TOP - FL - 16), 1, 'shell')
    box('anteroom partition', (170, 20, (FL + TOP) / 2), (4, 180, TOP - FL - 18), 1)
    box('partition door', (170, 40, FL + 100), (5, 80, 200), 1, 'detail')
    box('scrub sink', (200, 90, FL + 88), (48, 36, 10), 3, 'detail')
    loft('scrub tap', [(200, 104, FL + 93), (200, 104, FL + 110), (200, 94, FL + 110)], .8, 8, 'detail', False)
    # Operating light: arm from the ceiling, domed head over the table.
    rod('light drop', (-60, 20, TOP - 16), (-60, 20, TOP - 60), 2.4)
    rod('light arm', (-60, 20, TOP - 60), (-30, 0, TOP - 72), 2)
    sphere('light head', (-30, 0, TOP - 80), 22, 'structure', 36, 12, (1, 1, .32))
    ring('light rim', (-30, 0, TOP - 83), 22.5, 1.5, 1.6, (0, 0, 1), 'detail')
    box('HEPA diffuser', (-40, 20, TOP - 18), (120, 110, 5), 1, 'detail')
    # Operating table: column base, top, headrest, arm board.
    tx = -30
    box('table base', (tx, 10, FL + 5), (70, 44, 10), 3)
    cyl('table column', (tx, 10, FL + 10), 11, 58, 'structure', (0, 0, 1), 28)
    box('table top', (tx, 10, FL + 72), (178, 56, 9), 4)
    box('table cushion', (tx, 10, FL + 78.5), (172, 52, 5), 2.5, 'detail')
    box('headrest', (tx - 99, 10, FL + 80), (24, 26, 6), 3)
    box('arm board', (tx + 20, -26, FL + 74), (50, 16, 3), 1.5, 'detail')
    # Surgeon's stool at the head end.
    cyl('stool seat', (tx - 140, 40, FL + 58), 20, 7, 'structure', (0, 0, 1), 28)
    cyl('stool column', (tx - 140, 40, FL + 12), 3.4, 46, 'detail', (0, 0, 1), 12)
    for a in range(0, 360, 72):
        q = math.radians(a)
        rod('stool foot', (tx - 140, 40, FL + 10), (tx - 140 + 22 * math.cos(q), 40 + 22 * math.sin(q), FL + 3), 1.4, 'detail')
    # Instrument trolley.
    box('instrument trolley', (tx + 110, -20, FL + 82), (60, 40, 4), 1.5)
    for x in (tx + 84, tx + 136):
        for y in (-36, -4):
            rod('trolley leg', (x, y, FL + 5), (x, y, FL + 80), 1.1, 'detail')


def microscope():
    """Floor-stand surgical microscope at the head of the table (group B)."""
    with group('B'):
        bx, by = -205, -42
        # Five-leg base on castors.
        cyl('stand hub', (bx, by, FL + 8), 12, 10, 'structure', (0, 0, 1), 32)
        for a in range(0, 360, 72):
            q = math.radians(a + 18)
            e = Vector((bx + 42 * math.cos(q), by + 42 * math.sin(q), FL + 7))
            rod('base leg', (bx, by, FL + 12), e, 2.6)
            cyl('castor', e - Vector((0, 0, 6)), 3.2, 3, 'detail', (math.sin(q), -math.cos(q), 0), 16)
        cyl('column', (bx, by, FL + 18), 6.5, 140, 'structure', (0, 0, 1), 32)
        box('electronics housing', (bx, by, FL + 70), (22, 18, 42), 3)
        cyl('column head', (bx, by, FL + 158), 9, 10, 'structure', (0, 0, 1), 32)
        # Balanced boom: horizontal arm with counterweight, drop arm to the head.
        a0 = Vector((bx, by, FL + 166)); a1 = Vector((bx + 82, by + 50, FL + 170))
        loft('boom arm', [a0 - (a1 - a0).normalized() * 34, a0, a1], 4.2, 18)
        cyl('counterweight', a0 - (a1 - a0).normalized() * 46, 9, 22, 'structure', tuple((a1 - a0).normalized()), 28)
        joint(a1 + Vector((0, 0, 0)), 6, (0, 0, 1))
        drop = a1 + Vector((6, 4, -38))
        loft('carrier arm', [a1, a1 + Vector((4, 2, -14)), drop], 3.2, 16)
        # Optics carrier: objective, LED ring, binocular head with eyepieces.
        oc = drop + Vector((0, 0, -10))
        cyl('objective body', oc + Vector((0, 0, -4)), 8, 14, 'structure', (0, 0, 1), 32)
        ring('LED ring', oc + Vector((0, 0, -5)), 8.6, 1.4, 1.2, (0, 0, 1), 'accent')
        box('optics carrier', oc + Vector((-4, 0, 13)), (22, 16, 12), 3)
        box('binocular body', oc + Vector((-14, 0, 19)), (12, 16, 9), 2.5)
        for s_ in (-1, 1):
            e0 = oc + Vector((-18, s_ * 4, 22)); e1 = oc + Vector((-33, s_ * 4, 32))
            loft('eyepiece tube', [e0, e1], 2.7, 16, 'structure', False)
            ring('eye cup', e1, 3.1, 1.0, 2.4, tuple((e1 - e0).normalized()), 'detail')
        for s_ in (-1, 1):
            loft('steering handle', [oc + Vector((0, s_ * 8, 4)), oc + Vector((0, s_ * 15, 3)), oc + Vector((0, s_ * 15, -5))], 1.4, 10, 'detail')
        # Foot pedal and its cable.
        fp = Vector((bx + 70, by + 26, FL + 4))
        box('foot pedal', fp, (28, 22, 6), 3)
        box('pedal rocker', fp + Vector((2, 0, 4)), (18, 14, 2), 1.2, 'accent')
        tube('pedal cable', [fp + Vector((-14, 0, 2)), (bx + 30, by + 10, FL + 1), (bx + 6, by, FL + 14)], .6, 'cable')


def lens_bench():
    """Far-wall counter with the lens tray, injectors and sterile cassette (group C)."""
    cx, cy, cz = 80, YF - 44, FL + 90
    box('counter cabinet', (cx, cy + 4, cz - 45), (146, 48, 86), 3, 'detail')
    for x in (cx - 36, cx + 36):
        box('drawer front', (x, cy - 20.5, cz - 20), (68, 1.5, 20), 1, 'detail')
        box('drawer pull', (x, cy - 22, cz - 16), (18, 1.6, 2), .6, 'detail')
    with group('C'):
        cx, cy, cz = 80, YF - 44, FL + 90
        box('counter top', (cx, cy, cz), (150, 56, 4), 1.5)
        # Lens tray: five dioptre rows, six boxes each.
        tx0, ty0 = cx - 60, cy - 18
        box('lens tray', (tx0 + 33, ty0 + 17, cz + 3.5), (76, 42, 3), 1.2)
        for r in range(5):
            for k in range(6):
                p = Vector((tx0 + 6 + k * 11.6, ty0 + 3 + r * 7.2, cz + 6.2))
                box('lens box', p, (10.4, 6.2, 2.4), .6, 'detail')
                if (r + k) % 3 == 0:
                    ring('optic', p + Vector((0, 0, 1.3)), 1.6, .35, .4, (0, 0, 1), 'accent')
                    for s_ in (-1, 1):
                        tube('haptic', [p + Vector((s_ * 1.6, 0, 1.6)), p + Vector((s_ * 2.8, s_ * 1.2, 1.6)), p + Vector((s_ * 3.4, s_ * 2.6, 1.6))], .08, 'accent')
        # Injector cartridges in a rack.
        rx = cx + 22
        box('injector rack', (rx + 14, cy - 12, cz + 4), (34, 14, 4), 1)
        for k in range(5):
            x = rx + k * 7
            cyl('injector barrel', (x, cy - 12, cz + 6), 1.6, 15, 'structure', (0, 0, 1), 14)
            cyl('plunger', (x, cy - 12, cz + 21), .7, 5, 'detail', (0, 0, 1), 8)
        # Sterilisation cassette: perforated lid, latches.
        sx = cx + 48
        box('sterile cassette', (sx, cy + 6, cz + 7), (30, 22, 10), 2)
        for i in range(4):
            for j in range(3):
                cyl('vent perforation', (sx - 10.5 + i * 7, cy - 1 + j * 7, cz + 12.1), .9, .3, 'detail', (0, 0, 1), 10)
        for x in (sx - 13, sx + 13):
            box('cassette latch', (x, cy - 5.4, cz + 9), (3, 1.4, 4), .4, 'accent')
        # Biometry printout clip: each lens chosen before surgery.
        box('record clip', (cx + 60, cy - 20, cz + 3), (14, 18, 1.2), .4, 'detail')


def jacks():
    for x in (X0 + 8, X1 - 8):
        for y in (YN + 8, YF - 8):
            box('jack pad', (x, y, 1.5), (30, 30, 3), 1)
            cyl('jack screw', (x, y, 3), 3.4, Z0 - 3, 'structure', (0, 0, 1), 16)
            cyl('jack body', (x, y, 3), 6, 14, 'structure', (0, 0, 1), 24)
            rod('jack crank', (x, y, 14), (x + (14 if x > 0 else -14), y, 14), 1, 'detail')


def build():
    views(B=(-38, 12), C=(14, 62))
    frame()
    doors()
    roof()
    # Near wall: corrugated end pieces either side of the opening; far wall skin.
    corrugated_panel(X0 + 16, OPEN[0], YN + 1, Z0 + 16, TOP - 14)
    corrugated_panel(OPEN[1], X1 - 16, YN + 1, Z0 + 16, TOP - 14)
    box('far side wall', (0, YF - 2, Z0 + H / 2), (L - 32, 2, H - 30), .5, 'shell')
    box('end wall', (X0 + 1, 0, Z0 + H / 2), (2, WD - 32, H - 30), .5, 'shell')
    box('floor', (0, 0, FL - 4), (L - 32, WD - 30, 8), 1)
    hinge, out, depth = awning()
    yo = deck()
    glazing()
    theatre()
    microscope()
    lens_bench()
    jacks()
    # Service connections: shore power and water at the -X end.
    box('shore power box', (X0 + 40, YN - 3, Z0 + 60), (26, 6, 34), 2, 'detail')
    tube('shore cable', [(X0 + 40, YN - 6, Z0 + 43), (X0 + 20, YN - 30, 10), (X0 - 40, YN - 60, 1)], .9, 'cable')
    q = math.radians(AW)
    mark('SOLAR AWNING', hinge + out * (depth * .55) + Vector((OPEN[0] + 60, 0, 6)), 'BIFACIAL 2.4 kWp / SHADES THE WAITING DECK')
    mark('CLEAN AIR', (X0 + 40, -82, TOP + 40), 'HEPA / 20 AIR CHANGES AN HOUR')
    mark('WAITING DECK', (OPEN[0] + 20, yo + 40, FL + 47), 'SHADED / STEPS AND RAILS FOR OLDER PATIENTS')
    mark('SEALED THEATRE', (OPEN[0] + 165, YN + 6, FL + 150), 'GLAZED / FAMILIES WAIT WITHIN SIGHT')
    mark('ISO 20 ft BODY', (X1 + 6, -30, Z0 + 180), '6.06 × 2.44 × 2.59 m')
    mark('LEVELLING JACK', (X1 - 8, YN + 8, 12), 'SET UP ON ROUGH GROUND IN AN HOUR')
    return 36, 24
