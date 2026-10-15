"""MYCELIUM MASON: tracked arm printing a round hemp-mycelium house, segment by segment.

Units: centimetres. Z up. House centre at the origin.
The printer is a mason, not a gantry: it raises one 30-degree wall segment
to full height, then moves on, leaving vertical cold joints like racked
brickwork. Finished segments get growth-tent hoops and membrane while the
mycelium binds the hemp; the front of the house is still only its plinth,
so the interior, door and windows read through the gap.
Wall: outer radius 350, 30 thick, 240 high on a 20 cm stone plinth.
Print layers are 2 cm; every sixth layer line is drawn (12 cm).
"""
import math
from ..kit import *
from .parts import loft, arc_tube
from ..humans import human

R_OUT = 350
THICK = 30
R_MID = R_OUT - THICK / 2
PLINTH = 20
H = 240
SEG = 30
ARM_ANGLE = -5            # working segment centre, degrees
ARM_R = 575               # tracked base, from house centre


def polar(r, a, z=0):
    q = math.radians(a)
    return Vector((r * math.cos(q), r * math.sin(q), z))


def wall(name, a0, a1, z0, z1, layers=True, role='structure'):
    """One printed segment: annular sector, drawn layer lines on both faces."""
    arc_tube(name, (0, 0, z0), (0, 0, 1), (1, 0, 0), R_OUT, THICK, z1 - z0, a0, a1, role)
    if not layers:
        return
    z = PLINTH + 12
    while z < z1 - 3:
        if z > z0 + 3:
            for r in (R_OUT + .25, R_OUT - THICK - .25):
                n = max(6, int(abs(a1 - a0) / 2))
                tube('print layer', [polar(r, a0 + (a1 - a0) * k / n, z) for k in range(n + 1)], .12, 'detail')
        z += 12


def build():
    human('presence', .28, 60, tuple(polar(430, 262)))
    views(B=(60, 16), C=(80, 30))
    # --- plinth: the whole ring, stone on a gravel bed --------------------
    arc_tube('stone plinth', (0, 0, 0), (0, 0, 1), (1, 0, 0), R_OUT + 6, THICK + 12, PLINTH, 0, 360)
    # --- finished segments: 250 deg down to 10 deg ------------------------
    door = (140, 156)        # doorway sector
    windows = [(52, 64), (206, 218)]
    tent = (160, 250)
    starts = list(range(250, 10, -SEG))
    for a1 in starts:
        a0 = a1 - SEG
        pieces = [(a0, a1)]
        in_tent = a0 >= tent[0] - .1 and a1 <= tent[1] + .1
        with group('C') if in_tent else _null():
            # Split the segment around any opening that falls inside it.
            cuts = [o for o in [door] + windows if a0 <= o[0] and o[1] <= a1]
            edges = [a0]
            for o in cuts:
                edges += [o[0], o[1]]
            edges.append(a1)
            for k in range(0, len(edges), 2):
                if edges[k + 1] - edges[k] > .1:
                    wall('printed wall segment', edges[k], edges[k + 1], PLINTH, H + PLINTH)
            for o in cuts:
                if o == door:
                    wall('wall over lintel', o[0], o[1], 200 + PLINTH, H + PLINTH)
                    c = polar(R_MID, (o[0] + o[1]) / 2)
                    with at((c.x, c.y, 200 + PLINTH - 6), (o[0] + o[1]) / 2):
                        box('timber lintel', (0, 0, 0), (THICK + 6, 106, 12), 1.2, 'detail')
                    for a in o:
                        p = polar(R_MID, a)
                        with at((p.x, p.y, PLINTH), a):
                            box('door jamb', (0, 0, 100), (THICK + 2, 8, 200), .8, 'detail')
                else:
                    wall('wall under sill', o[0], o[1], PLINTH, 90 + PLINTH)
                    wall('wall over window', o[0], o[1], 170 + PLINTH, H + PLINTH)
                    c = polar(R_MID, (o[0] + o[1]) / 2)
                    with at((c.x, c.y, 130 + PLINTH), (o[0] + o[1]) / 2):
                        box('window frame', (0, 0, 0), (8, 70, 80), 1, 'accent')
                        box('window mullion', (-1, 0, 0), (6, 4, 76), .5, 'detail')
    # --- working segment: -20..10, raked to 150 cm -------------------------
    wall('working segment', -20, 10, PLINTH, 150 + PLINTH)
    wall('racked step', -20, -8, 150 + PLINTH, 150 + PLINTH + 0.01, layers=False)
    # --- growth tent over the first three printed segments ---------------
    with group('C'):
        hoops = [tent[0] + k * 10 for k in range(10)]
        rings = []
        for a in hoops:
            pts = []
            for k in range(17):
                t = math.pi * k / 16
                pts.append(polar(R_MID + 58 * math.cos(t), a, 285 * math.sin(t)))
            loft('tent hoop', pts, 1.4, 10, 'structure', False)
            rings.append(pts)
        # Membrane on the middle bays only: the ends stay open for air.
        vs = []; fs = []
        span = [pts[:10] for pts in rings[1:9]]      # outer side, ground to just past the ridge
        for i, pts in enumerate(span):
            for p in pts:
                vs.append(p + Vector((0, 0, 1.6)))
        m = len(span[0])
        for i in range(len(span) - 1):
            for k in range(m - 1):
                fs.append((i * m + k, i * m + k + 1, (i + 1) * m + k + 1, (i + 1) * m + k))
        g.mesh('growth membrane', vs, fs, 'shell')
        # Inner side rolled up for air and inspection: a roll along the hoops.
        roll = [rings[i][10] + Vector((0, 0, 3)) for i in range(1, 9)]
        loft('rolled-up side', roll, 4.5, 14, 'structure', False)
        for i in (2, 5, 8):
            tube('roll tie', [rings[i][10] + Vector((0, 0, 8)), rings[i][10] + Vector((0, 0, -2))], .4, 'detail')
        ridge = [polar(R_MID, a, 283) for a in range(tent[0], tent[0] + 91, 5)]
        tube('misting line', ridge, .8, 'accent')
        for a in hoops[1:-1]:
            cyl('mist nozzle', polar(R_MID, a + 5, 280), 1.4, 3, 'accent', (0, 0, -1), 12)
        box('humidity sensor', polar(R_MID + 40, tent[0] + 45, 150), (8, 8, 12), 1.5, 'detail')
        for a in (tent[0], tent[0] + 90):
            for side in (-1, 1):
                cyl('hoop ground peg', polar(R_MID + side * 58, a, -6), 1.6, 10, 'detail', (0, 0, 1), 12)
        mark('GROWTH TENT', polar(R_MID + 40, tent[0] + 55, 262), '6 DAYS AT 24 °C / 95 % HUMIDITY')
    # --- tracked printing arm ----------------------------------------------
    base = polar(ARM_R, ARM_ANGLE)
    yaw = ARM_ANGLE + 180
    def W(v):
        v = Vector(v); q = math.radians(yaw)
        return base + Vector((v.x * math.cos(q) - v.y * math.sin(q), v.x * math.sin(q) + v.y * math.cos(q), v.z))
    reach = ARM_R - R_MID       # local x of the nozzle
    tip_z = 150 + PLINTH
    with at(base, yaw):
        for side in (-1, 1):
            box('crawler track', (0, side * 48, 24), (190, 32, 44), 14)
            for x in (-78, 78):
                cyl('track sprocket', (x, side * 48 - 16, 24), 17, 32, 'detail', (0, 1, 0), 32)
            for x in (-40, 0, 40):
                cyl('track roller', (x, side * 48 - 17, 12), 7, 2, 'detail', (0, 1, 0), 20)
        box('undercarriage', (0, 0, 44), (120, 70, 16), 4)
        cyl('slew ring', (0, 0, 52), 46, 8, 'structure', (0, 0, 1), 64)
        box('turret body', (-10, 0, 90), (120, 84, 64), 12)
        # Hopper doubles as counterweight: hurd, water and spawn mixed on board.
        vs = []; fs = []
        for z, w, d in ((124, 44, 60), (196, 92, 104), (206, 92, 104)):
            vs += [Vector((-66 + sx * w / 2, sy * d / 2, z)) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        for i in range(2):
            for k in range(4):
                a = i * 4 + k; b = i * 4 + (k + 1) % 4
                fs.append((a, b, b + 4, a + 4))
        fs.append((3, 2, 1, 0)); fs.append((8, 9, 10, 11))
        g.mesh('hurd hopper', vs, fs, 'structure')
        for z in (150, 172):
            tube('hopper band', [Vector((-66 + sx * (44 + (z - 124) / 72 * 48) / 2 * 1.01, sy * (60 + (z - 124) / 72 * 44) / 2 * 1.01, z))
                                 for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1))], .35, 'detail')
        box('mixer', (-66, 0, 112), (54, 64, 22), 6, 'detail')
        motor((-66, 34, 112), 8, 10, (0, 1, 0))
        box('spawn tank', (-28, -44, 128), (22, 14, 30), 4, 'accent')
        box('control box', (-18, -46, 92), (40, 8, 30), 3, 'detail')
        for k in range(5):
            box('cooling slat', (-44 + k * 8, 43, 100), (4, 2, 28), .6, 'detail')
        # Boom and stick: tapered box-section members, hydraulic rams.
        pivot = Vector((34, 0, 118)); elbow = Vector((150, 0, 368)); wrist = Vector((reach, 0, tip_z + 72))
        loft('boom', [pivot, pivot.lerp(elbow, .5) + Vector((6, 0, 6)), elbow], lambda t: 15 - 5 * t, 18)
        loft('stick', [elbow, wrist], lambda t: 10 - 2.5 * t, 16)
        cyl('boom pin', pivot + Vector((0, -14, 0)), 7, 28, 'detail', (0, 1, 0), 24)
        cyl('elbow pin', elbow + Vector((0, -11, 0)), 6, 22, 'detail', (0, 1, 0), 24)
        rod('boom ram', (18, 0, 92), pivot.lerp(elbow, .45) + Vector((0, 0, -10)), 4.5, 'detail')
        rod('stick ram', pivot.lerp(elbow, .7) + Vector((-8, 0, 12)), elbow.lerp(wrist, .25) + Vector((0, 0, 12)), 3.5, 'detail')
        # Print hose from the turret along the boom to the head.
        tube('material hose', [(-40, 30, 112), (20, 22, 140), pivot.lerp(elbow, .5) + Vector((0, 18, 8)),
                               elbow + Vector((0, 16, 10)), wrist + Vector((-10, 14, 14)), wrist + Vector((0, 8, 4))], 2.4, 'cable')
    with group('B'):
        with at(base, yaw):
            hx = reach
            cyl('wrist rotator', (hx, 0, tip_z + 66), 10, 10, 'structure', (0, 0, 1), 36)
            flange('hose coupling', (hx, 0, tip_z + 76), 7, (0, 0, 1), 2)
            # Auger barrel with a service window onto the flight.
            arc_tube('auger barrel', (hx, 0, tip_z + 22), (0, 0, 1), (-.8, .45, 0), 9.5, 1.2, 44, 40, 320)
            pts = [Vector((hx + 6.5 * math.cos(t * .5), 6.5 * math.sin(t * .5), tip_z + 24 + t * 1.3)) for t in range(0, 31)]
            tube('auger flight', pts, .9, 'detail')
            cyl('auger shaft', (hx, 0, tip_z + 22), 2, 44, 'detail', (0, 0, 1), 16)
            loft('nozzle', [Vector((hx, 0, tip_z + 22)), Vector((hx, 0, tip_z + 10)), Vector((hx, 0, tip_z + 2))],
                 lambda t: 9.5 - 6 * t, 24, 'structure', False)
            ring('nozzle lip', (hx, 0, tip_z + 1), 3.8, 1.2, 1.6, (0, 0, 1), 'accent')
            # Inoculation injector: living spawn enters just above the nozzle.
            cyl('spawn cartridge', (hx + 6, -22, tip_z + 40), 5, 22, 'accent', (0, 0, 1), 24)
            tube('spawn line', [Vector((hx + 6, -22, tip_z + 40)), Vector((hx + 6, -16, tip_z + 28)), Vector((hx + 3, -7, tip_z + 18))], .8, 'accent')
            box('dosing pump', (hx + 6, -22, tip_z + 66), (12, 12, 10), 2, 'detail')
            rod('pump bracket', (hx + 6, -16, tip_z + 66), (hx + 2, -9, tip_z + 66), 1.2, 'detail')
            # Side trowels ride both faces of the fresh layer.
            for side in (-1, 1):
                box('side trowel', (hx + side * (THICK / 2 + 2), 0, tip_z - 3), (1.6, 22, 10), .5, 'structure')
                rod('trowel arm', (hx + side * (THICK / 2 + 2), 0, tip_z + 3), (hx + side * 9, 0, tip_z + 20), 1.2, 'detail')
            box('layer camera', (hx + 16, -18, tip_z + 30), (8, 8, 7), 1.2, 'detail')
            cyl('camera lens', (hx + 16, -18, tip_z + 26), 2, 1, 'accent', (0, 0, -1), 16)
    mark('PRINT HEAD', W((reach, -9.6, tip_z + 40)), '2 cm LAYERS / 0.5 m³ AN HOUR')
    mark('HOPPER AND MIXER', W((-66, -40, 180)), 'HEMP HURD, WATER AND LIVING SPAWN / MIXED ON BOARD')
    # --- marks --------------------------------------------------------------
    mark('COLD JOINT', polar(R_OUT - THICK - .5, 70, 130), 'ONE 30° SEGMENT AT A TIME / RACKED LIKE BRICKWORK')
    mark('DOORWAY', polar(R_OUT - THICK - .5, 148, 206 + PLINTH), 'TIMBER LINTEL / THE FAMILY CHOSE THE SIDE')
    mark('BUILDER', polar(430, 262, 110), 'CHECKS EVERY LAYER BY HAND')
    return 44, 40


class _null:
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False
