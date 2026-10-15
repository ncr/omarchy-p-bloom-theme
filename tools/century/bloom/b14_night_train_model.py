"""NIGHT TRAIN: cab-end electric sleeper carriage on track, side opened.

Units are centimetres. X along the track (cab nose at +X), Y across
(camera side -Y), Z up from the top of rail. Standard gauge: wheel
centres at y = +/-75. Body: superellipse section, half-width 145,
half-height 150 about z = 270 (floor 125, roof 420). A 630 cm segment
of the body is built as a thick-walled shell open on the corridor side,
exposing three compartments (two berths each). Bogies at x = -900 and
+800 (motor bogie under the cab). Single-arm pantograph on the roof,
overhead contact line with a messenger wire above.
"""
from ..kit import *
from .parts import loft, sphere, frame_matrix

E = .42                  # superellipse exponent of the body section
RY, RZ, ZC = 145, 150, 270
CUT = (-100, 530)        # opened body segment
BOGIES = (-900, 800)
X_TAIL, X_BODY_END, X_NOSE = -1250, 980, 1310


def sec(a, ry=RY, rz=RZ, zc=ZC):
    c, s = math.cos(a), math.sin(a)
    return (ry * math.copysign(abs(c) ** E, c), zc + rz * math.copysign(abs(s) ** E, s))


def open_shell(x0, x1, a_from, a_to, wall=6, n=72):
    """Body segment as a real wall: outer and inner skins over an arc of the
    section (angles in degrees, counter-clockwise), closed at the cut edges
    and at both ends, so the cut shows the wall thickness."""
    angs = [math.radians(a_from + (a_to - a_from) * k / n) for k in range(n + 1)]
    outer = [sec(a) for a in angs]
    inner = [sec(a, RY - wall, RZ - wall) for a in angs]
    vs = []
    for x in (x0, x1):
        vs += [(x, y, z) for y, z in outer] + [(x, y, z) for y, z in inner]
    m = n + 1; o0, i0, o1, i1 = 0, m, 2 * m, 3 * m
    fs = []
    for k in range(n):
        fs.append((o0 + k, o0 + k + 1, o1 + k + 1, o1 + k))
        fs.append((i0 + k, i1 + k, i1 + k + 1, i0 + k + 1))
        fs.append((o0 + k, i0 + k, i0 + k + 1, o0 + k + 1))
        fs.append((o1 + k, o1 + k + 1, i1 + k + 1, i1 + k))
    for a, b in ((0, 0), (n, n)):
        fs.append((o0 + a, o1 + a, i1 + a, i0 + a))
    return g.mesh('opened body shell', vs, fs, 'structure')


def window_row(x0, x1, pitch, w, h, zc, y=-RY - .6, role='detail'):
    n = int((x1 - x0) // pitch)
    for i in range(n):
        x = x0 + pitch * (i + .5)
        box('side window', (x, y, zc), (w, 1.4, h), 5, role)


def body():
    sections = lambda x0, x1: [(x0, RY, RZ, ZC), (x1, RY, RZ, ZC)]
    tail = hull('carbody', sections(X_TAIL, CUT[0]), 'X', 'structure', E)
    front = hull('carbody', [(CUT[1], RY, RZ, ZC), (X_BODY_END, RY, RZ, ZC), (1080, RY - 2, RZ - 4, ZC - 2),
                             (1170, RY - 10, RZ - 22, ZC - 14), (1235, RY - 32, RZ - 58, ZC - 40),
                             (1280, RY - 70, RZ - 96, ZC - 62), (X_NOSE, 26, 24, 186)], 'X', 'structure', E)
    for st in (-1000, -600, 700):
        hull_seam(tail if st < 0 else front, st)
    # Opened segment: shell from 212 deg round to 424 deg (= 64): the roof and the
    # corridor side are cut away; the berth-side wall and the floor remain.
    open_shell(CUT[0], CUT[1], 212, 424)
    # Corridor-side window band and berth-side windows on the closed segments.
    window_row(X_TAIL + 260, CUT[0] - 20, 210, 150, 62, 262)
    window_row(CUT[1] + 20, 900, 210, 150, 62, 262)
    # Two livery lines along the flank (under the windows and at the cantrail),
    # stopping at the door and at the opened segment.
    for z in (214, 318):
        a = math.asin(max(-1, min(1, ((abs(z - ZC) / RZ) ** (1 / E))))) * (1 if z > ZC else -1)
        y = -RY * abs(math.cos(a)) ** E - .9
        for xa, xb in ((X_TAIL + 175, CUT[0] - 4), (CUT[1] + 4, 1120)):
            tube('livery line', [(xa, y, z), (xb, y, z)], .2, 'detail')
    # Entrance at the tail: plug door, steps, grab poles (human scale).
    dx = X_TAIL + 120
    box('entrance door', (dx, -RY - .8, 232), (92, 1.6, 206), 6, 'detail')
    box('door window', (dx, -RY - 1.8, 290), (54, 1.2, 60), 4, 'detail')
    for k, z in enumerate((96, 62)):
        box('boarding step', (dx, -RY - 14 - 12 * k, z), (96, 24, 4), 1.5)
    for x in (dx - 58, dx + 58):
        loft('grab pole', [(x, -RY - 4, 150), (x, -RY - 8, 160), (x, -RY - 8, 300), (x, -RY - 4, 310)], 1.5, 10, 'detail')
    # Cab: windscreen following the nose surface, headlights, coupler cover.
    from ..kit import profile_at
    nose = [(CUT[1], RY, RZ, ZC), (X_BODY_END, RY, RZ, ZC), (1080, RY - 2, RZ - 4, ZC - 2),
            (1170, RY - 10, RZ - 22, ZC - 14), (1235, RY - 32, RZ - 58, ZC - 40),
            (1280, RY - 70, RZ - 96, ZC - 62), (X_NOSE, 26, 24, 186)]

    def on_nose(x, a, lift=.8):
        ry, rz, zc = profile_at(nose, x)
        c, s = math.cos(a), math.sin(a)
        return Vector((x, (ry + lift) * math.copysign(abs(c) ** E, c), zc + (rz + lift) * math.copysign(abs(s) ** E, s)))
    loop = [on_nose(1150, math.radians(a)) for a in range(40, 141, 5)]
    loop += [on_nose(1150 + 104 * t / 10, math.radians(140)) for t in range(1, 11)]
    loop += [on_nose(1254, math.radians(a)) for a in range(140, 39, -5)]
    loop += [on_nose(1254 - 104 * t / 10, math.radians(40)) for t in range(1, 11)]
    tube('windscreen', loop, .3, 'accent')
    tube('wiper', [on_nose(1210, math.radians(70), 1.2), on_nose(1236, math.radians(95), 1.2)], .25, 'detail')
    for a in (205, 335):
        p = on_nose(1268, math.radians(a), .6)
        cyl('headlight', p, 7, 1.6, 'accent', (1, -.2 if a < 270 else .2, -.3), 24)
    cyl('coupler cover', (X_NOSE - 2, 0, 170), 16, 6, 'detail', (1, 0, 0), 32)
    loft('nose skirt', [(1200, -120, 104), (1290, -60, 112), (1305, 0, 116), (1290, 60, 112), (1200, 120, 104)], 2.5, 12, 'structure')
    # Gangway at the tail: bellows frame.
    for k in range(5):
        box('gangway bellows', (X_TAIL - 4 - k * 4, 0, 260), (3, 130 - k * 2, 250 - k * 2), 10, 'detail')
    box('gangway face plate', (X_TAIL - 26, 0, 260), (4, 124, 240), 10)


def roof_gear():
    # HVAC module and breaker; single-arm pantograph above the cab bogie.
    box('roof HVAC unit', (-640, 0, 434), (360, 170, 30), 10)
    for k in range(7):
        box('HVAC grille bar', (-760 + k * 40, -86, 434), (22, 1.2, 18), .6, 'detail')
    box('roof well', (720, 0, 421), (340, 150, 4), 4, 'detail')
    px = 700
    for x in (px - 70, px + 70):
        for y in (-50, 50):
            cyl('post insulator', (x, y, 424), 5, 16, 'structure', (0, 0, 1), 16)
            for z in (428, 432, 436):
                ring('insulator shed', (x, y, z), 7, 2, 1, (0, 0, 1), 'detail')
    box('pantograph base frame', (px, 0, 442), (170, 120, 6), 2)
    pivot = Vector((px + 60, 0, 448))
    knee = Vector((px - 70, 0, 520))
    head = Vector((px + 20, 0, 588))
    for y in (-18, 18):
        loft('lower arm', [pivot + Vector((0, y, 0)), knee + Vector((0, y * .4, 0))], 2.6 if y < 0 else 2.2, 12)
    loft('upper arm', [knee, head], 2.0, 12)
    rod('lower operating rod', pivot + Vector((-10, 0, -2)), knee + Vector((10, 0, -8)), .9, 'detail')
    rod('upper guide rod', knee + Vector((8, 0, 6)), head + Vector((-6, 0, -4)), .6, 'detail')
    cyl('lift cylinder', pivot + Vector((-40, -30, -4)), 4, 34, 'detail', (1, 0, .35), 16)
    # Collector head: two carbon strips across the track, curved horns.
    for dx in (-12, 12):
        box('carbon strip', head + Vector((dx, 0, 6)), (6, 150, 3), 1, 'accent')
    box('pan head frame', head + Vector((0, 0, 1)), (34, 12, 4), 1.5)
    for s_ in (-1, 1):
        loft('pan horn', [head + Vector((0, s_ * 75, 6)), head + Vector((0, s_ * 95, 0)), head + Vector((0, s_ * 104, -14))], 1.4, 10)
        rod('head spring box', head + Vector((0, s_ * 40, 1)), head + Vector((0, s_ * 40, 6)), 2, 'detail')
    tube('roof high-voltage line', [pivot + Vector((0, 0, -6)), (px + 120, 0, 426), (px + 240, 0, 424)], 1.1, 'cable')
    return head


def catenary(head):
    z = head.z + 7.5
    tube('contact wire', [(X_TAIL - 60, 0, z), (X_NOSE + 60, 0, z)], .5, 'shell')
    tube('messenger wire', [(X_TAIL - 60, 0, z + 118), (X_NOSE + 60, 0, z + 92)], .5, 'shell')
    for x in range(-1200, 1300, 360):
        t = (x - (X_TAIL - 200)) / (X_NOSE + 240 - X_TAIL + 200)
        tube('dropper', [(x, 0, z), (x, 0, z + 120 - 30 * t)], .3, 'shell')


def track():
    x0, x1 = X_TAIL - 90, X_NOSE + 170
    for y in (-75, 75):
        box('rail', ((x0 + x1) / 2, y, -8.5), (x1 - x0, 7, 17), 1)
        box('rail foot', ((x0 + x1) / 2, y, -16), (x1 - x0, 15, 2), .5, 'detail')
    for x in range(int(x0) + 20, int(x1) - 10, 64):
        box('sleeper', (x, 0, -27), (26, 260, 20), 3, 'detail')


def wheelset(x, motor=False):
    for y in (-75, 75):
        cyl('wheel', (x, y - 7 * (1 if y > 0 else -1) * 0, 46), 46, 14, 'structure', (0, 1 if y > 0 else -1, 0), 48)
        ring('wheel flange', (x, y - (1 if y > 0 else -1) * 1, 46), 50, 4, 2, (0, 1 if y > 0 else -1, 0), 'detail')
        ring('wheel web', (x, y + (15 if y > 0 else -15), 46), 30, 1.5, 1, (0, 1 if y > 0 else -1, 0), 'detail')
    cyl('axle', (x, -104, 46), 8, 208, 'structure', (0, 1, 0), 24)
    for y in (-104, 104):
        box('axle box', (x, y + (6 if y > 0 else -6), 46), (30, 18, 26), 4)
        # Primary suspension: coil spring from axle box to frame.
        pts = [Vector((x + 8 * math.cos(t), y + (6 if y > 0 else -6) + 8 * math.sin(t), 59 + 16 * t / (5 * T))) for t in [T * 5 * k / 90 for k in range(91)]]
        tube('primary coil', pts, .9, 'structure')
    for y in (-38, 38):
        cyl('brake disc', (x, y - 2, 46), 32, 4, 'structure', (0, 1, 0), 40)
        ring('disc vent ring', (x, y + (2.2 if y > 0 else -2.2), 46), 24, 1, .6, (0, 1, 0), 'detail')
        box('brake caliper', (x + 28, y, 58), (14, 12, 16), 2, 'detail')
    if motor:
        cyl('traction motor', (x - 70, -60, 50), 26, 90, 'structure', (0, 1, 0), 36)
        for k in range(1, 8):
            ring('motor cooling rib', (x - 70, -60 + k * 11, 50), 27.5, 1.5, 2, (0, 1, 0), 'detail')
        box('gearbox', (x - 30, 42, 46), (70, 18, 40), 8)


def bogie(x, motor):
    for y in (-105, 105):
        with at((0, y, 0)):
            hull('bogie side frame', [(x - 170, 8, 9, 78), (x - 120, 9, 12, 76), (x - 60, 10, 9, 66), (x + 60, 10, 9, 66),
                                      (x + 120, 9, 12, 76), (x + 170, 8, 9, 78)], 'X', 'structure', .6)
        # Secondary suspension: air spring bellows between frame and body.
        for k, (r, z) in enumerate(((22, 78), (26, 88), (24, 98), (20, 108))):
            ring('air spring bellows', (x, y, z), r, 5, 8, (0, 0, 1), 'detail' if k % 2 else 'structure')
        cyl('air spring top plate', (x, y, 114), 23, 4, 'detail', (0, 0, 1), 32)
        # Active lateral damper, frame to body.
        rod('active damper', (x + 40, y, 76), (x + 110, y * .85, 114), 2.2, 'detail')
        cyl('damper actuator', (x + 40, y, 76), 4.2, 30, 'detail', (70, -15 * (1 if y > 0 else -1), 38), 16)
    for dx in (-30, 30):
        box('transom', (x + dx, 0, 64), (16, 200, 16), 3)
    for dx in (-125, 125):
        wheelset(x + dx, motor and dx > 0)


SECTION = 100            # partitions shown cut at this height above the floor


def partitions(x0, cut=True):
    fl = 125; ph = SECTION if cut else 250
    box('compartment partition', (x0 + 2, 41, fl + ph / 2), (5, 186, ph), 1.2)
    for xa, xb in ((x0 + 4, x0 + 56), (x0 + 142, x0 + 208)):
        box('corridor partition', ((xa + xb) / 2, -52, fl + ph / 2), (xb - xa, 5, ph), 1.2)


def compartment(x0, cut=True):
    """Two-berth compartment on the far side, corridor on the near side.
    Berths run along the outer wall: lower berth, window, upper berth."""
    fl = 125; yw = 134              # floor, inner face of the outer wall
    box('wall lining', (x0 + 106, yw + 2.5, fl + 128), (206, 2, 250), 2, 'shell')
    yb = yw - 38
    for z, lab in ((fl + 46, 'lower'), (fl + 160, 'upper')):
        box('berth frame', (x0 + 106, yb, z - 5), (192, 76, 8), 2)
        box('mattress', (x0 + 106, yb, z + 4), (186, 72, 12), 5)
        box('pillow', (x0 + 186, yb, z + 14), (26, 50, 9), 4, 'detail')
        box('folded duvet', (x0 + 40, yb, z + 13), (40, 62, 7), 3, 'detail')
        for x in (x0 + 16, x0 + 196):
            box('berth bracket', (x, yw - 3, z - 16), (4, 6, 26), 1, 'detail')
        if lab == 'upper':
            rod('berth guard rail', (x0 + 30, yb - 38, z + 26), (x0 + 170, yb - 38, z + 26), 1.2, 'detail')
            for x in (x0 + 30, x0 + 170):
                rod('rail upright', (x, yb - 38, z + 8), (x, yb - 38, z + 26), 1, 'detail')
        else:
            box('berth plinth', (x0 + 106, yb, fl + 20), (186, 70, 40), 3, 'detail')
    # Window between the berths, blind half drawn.
    box('window frame', (x0 + 106, yw + 1, fl + 118), (150, 3, 62), 8)
    box('window reveal', (x0 + 106, yw - .5, fl + 118), (138, 1, 50), 6, 'detail')
    box('roller blind', (x0 + 106, yw - 3, fl + 136), (140, 2, 22), 3, 'detail')
    # Ladder at the head end, washbasin cabinet by the corridor, lamps, luggage shelf.
    for y in (yb - 44, yb - 44 - 34):
        rod('ladder rail', (x0 + 24, y, fl), (x0 + 30, y, fl + 176), 1.4)
    for k in range(5):
        z = fl + 30 + k * 30
        rod('ladder rung', (x0 + 24 + k * 1.1, yb - 44, z), (x0 + 24 + k * 1.1, yb - 78, z), 1)
    box('basin cabinet', (x0 + 176, -26, fl + 42), (50, 40, 84), 4)
    cyl('washbasin', (x0 + 176, -26, fl + 80), 13, 6, 'detail', (0, 0, 1), 32)
    loft('basin tap', [(x0 + 196, -26, fl + 84), (x0 + 196, -26, fl + 98), (x0 + 186, -26, fl + 98)], 1, 8, 'detail', False)
    for z in (fl + 74, fl + 188):
        cyl('reading lamp', (x0 + 190, yw - 2, z), 4, 5, 'accent', (0, -1, 0), 20)
    box('luggage shelf', (x0 + 106, yw - 20, fl + 236), (192, 40, 4), 1.5)
    for k in range(1, 7):
        rod('shelf bar', (x0 + 10 + k * 27, yw - 38, fl + 240), (x0 + 10 + k * 27, yw - 2, fl + 240), .8, 'detail')
    box('shelf lip', (x0 + 106, yw - 40, fl + 241), (192, 2, 6), .8, 'detail')


def build():
    views(B=(22, 24), C=(32, 30))
    body()
    head = roof_gear()
    catenary(head)
    track()
    # Underframe equipment between the bogies.
    for x, w, name in ((-560, 220, 'converter case'), (-280, 180, 'battery case'), (80, 240, 'water and waste tanks'), (420, 160, 'brake control')):
        box(name, (x, 0, 88), (w, 210, 50), 6)
        for k in range(1, int(w // 40)):
            box('case rib', (x - w / 2 + k * 40, -105.6, 88), (3, 1.4, 42), .5, 'detail')
    box('corridor floor', (sum(CUT) / 2, 0, 122), (CUT[1] - CUT[0], 2 * RY - 16, 6), 1, 'detail')
    with group('B'):
        compartment(CUT[0] + 210)
    compartment(CUT[0])
    compartment(CUT[0] + 420)
    for k in range(3):
        partitions(CUT[0] + 210 * k)
    box('compartment partition', (CUT[1] - 3, 41, 125 + SECTION / 2), (5, 186, SECTION), 1.2)
    for x in BOGIES:
        if x > 0:
            with group('C'):
                bogie(x, True)
        else:
            bogie(x, False)
    mark('PANTOGRAPH', (head.x + 10, -60, head.z + 4), '15 kV AC / 3 kV DC / 1.5 kV DC')
    mark('SLEEPING COMPARTMENTS', (CUT[0] + 316, 60, 297), 'TEN PER CARRIAGE / TWO BERTHS EACH')
    mark('MOTOR BOGIE', (800 + 125, -115, 46), 'ACTIVE AIR SPRINGS / QUIET OVER POINTS')
    mark('CAB', (1205, -60, 330), 'THE CARRIAGE DRIVES ITSELF AT THE HEAD OR MID-TRAIN')
    mark('BOARDING STEP', (X_TAIL + 120, -RY - 26, 62), 'LEVEL WITH A 55 cm PLATFORM')
    mark('OVERHEAD LINE', (X_TAIL - 30, 0, head.z + 7.5), 'THREE SUPPLY SYSTEMS, NO LOCOMOTIVE CHANGE')
    return 60, 34
