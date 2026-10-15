"""FIRST POSTCARD: a gram-scale probe on a mirror sail over a laser field.

Two scales in one drawing, declared on the sheet: the probe is ENLARGED
(the real sail is 4 m across, the chip 15 mm), the laser field is drawn in
true proportion to itself as a hex field of tiles standing for an array
3.5 km across. Units are arbitrary drawing units. The beam is drawn as a
light volume: cross-section rings along its axis and four faint edges.
Field: natural plateau (radius ~305, scarp 70 high, talus apron) with a hex
layout of flat hexagonal phased-array tiles (circumradius 24, pitch 54) on
short pedestals, all tilted to the beam axis; three service roads split it
into six blocks. Probe: shallow billowed sail (radius 170) with radial ribs
and a hair-thin rim; square chip (34 wide, enlarged) at the apex with a
camera, a laser-communication aperture and four photon thruster pods.
"""
from ..kit import *
from .parts import loft, sphere, dome, arc_tube

PITCH = 54
TILE = 24
FIELD_R = 262
SAIL_C = Vector((70, -200, 470))
SAIL_R = 170
BILLOW = 20
TILT = SAIL_C.normalized()                    # beam axis: tiles and sail share it
RAVINES = ()


def sail_frame():
    z = TILT; x = z.cross(Vector((0, 0, 1))).normalized(); y = z.cross(x)
    return x, y, z


def sail_point(r, a, lift=0.0):
    """Point on the billowed sail (convex away from the field) in world space."""
    x, y, z = sail_frame()
    h = BILLOW * (1 - (r / SAIL_R) ** 2) + lift
    return SAIL_C + x * (r * math.cos(a)) + y * (r * math.sin(a)) + z * h


def mesa_edge(a):
    r = 312 + 14 * math.sin(3 * a + .4) + 8 * math.sin(7 * a + 1.3)
    for deg, w in RAVINES:
        d = (math.degrees(a) - deg + 180) % 360 - 180
        r -= 20 * math.exp(-(d / (6 * w)) ** 2)
    return r


SCARP = 70


def mesa():
    """Natural plateau: flat top, steep scarp, talus apron; heavy crest, hachures."""
    na = 360; vs = []; fs = []
    rings = [(0, 0), (1.0, 0), (26, -SCARP), (92, -SCARP - 34)]
    for k, (off, z) in enumerate(rings):
        for j in range(na):
            a = T * j / na; R = mesa_edge(a)
            r = 0 if k == 0 else R + off - (1.0 if k == 1 else 0) + (0 if k < 2 else 4 * math.sin(5 * a + 1))
            vs.append((r * math.cos(a), r * math.sin(a), z))
    for i in range(len(rings) - 1):
        for j in range(na):
            p = i * na + j; q = i * na + (j + 1) % na
            fs.append((p, q, q + na, p + na))
    g.mesh('high plateau', vs, fs, 'structure')
    tube('plateau crest', [(mesa_edge(T * k / 720) * math.cos(T * k / 720), mesa_edge(T * k / 720) * math.sin(T * k / 720), .8) for k in range(721)], 1.0, 'structure')
    for j in range(0, 720, 3):
        a = math.radians(j / 2 + .4 * ((j * 37) % 5)); R = mesa_edge(a)
        f = .45 + .5 * ((j * 13) % 4) / 3
        tube('scarp hachure', [((R + 2) * math.cos(a), (R + 2) * math.sin(a), -2), ((R + 2 + 26 * f) * math.cos(a), (R + 2 + 26 * f) * math.sin(a), -2 - SCARP * f)], .22, 'shell')
    for j in range(0, 360, 7):
        a = math.radians(j + 2.3 * ((j * 7) % 3)); R = mesa_edge(a)
        tube('talus stroke', [((R + 34) * math.cos(a), (R + 34) * math.sin(a), -SCARP - 3), ((R + 60) * math.cos(a), (R + 60) * math.sin(a), -SCARP - 16)], .18, 'shell')


def hex_prism(name, R, h, role, z0=0.0):
    vs = [(R * math.cos(math.radians(30 + 60 * k)), R * math.sin(math.radians(30 + 60 * k)), z) for z in (z0, z0 + h) for k in range(6)]
    fs = [tuple(reversed(range(6))), tuple(range(6, 12))] + [(k, (k + 1) % 6, 6 + (k + 1) % 6, 6 + k) for k in range(6)]
    return g.mesh(name, vs, fs, role)


def hex_line(name, R, z, role, r=.3):
    pts = [(R * math.cos(math.radians(30 + 60 * k)), R * math.sin(math.radians(30 + 60 * k)), z) for k in range(7)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(name, p0, p1, r, role)


def tile(p, detail=False):
    """Flat hexagonal phased-array tile on a short pedestal, aimed along the beam."""
    b = len(g.parts); w = len(g.wires)
    box('tile footing', (0, 0, 1), (12, 12, 2), .8)
    cyl('tile pedestal', (0, 0, 2), 2.6, 8, 'structure', (0, 0, 1), 20)
    m = Vector((0, 0, 1)).rotation_difference(TILT).to_matrix().to_4x4(); m.translation = Vector((0, 0, 11))
    bb = len(g.parts); ww = len(g.wires)
    box('tilt yoke', (0, 0, -1.2), (8, 5, 2.4), .6, 'detail')
    hex_prism('phased-array tile', TILE, 2.6, 'structure')
    hex_line('emitting face', TILE * .82, 3.0, 'accent', .25)
    if detail:
        for k in range(7):
            q = math.radians(60 * k); rr = 0 if k == 6 else TILE * .5
            cyl('sub-aperture lens', (rr * math.cos(q), rr * math.sin(q), 2.7), 4.4, .8, 'accent', (0, 0, 1), 28)
        box('phase controller', (0, -TILE * .55, -3.2), (12, 7, 4), 1, 'detail')
        tube('fibre feed', [(0, -TILE * .55 - 3.5, -3.2), (0, -TILE * .55 - 7, -6), (0, -TILE * .55 - 8, -10)], .6, 'cable')
        for sgn in (-1, 1):
            tube('coolant line', [(sgn * TILE * .45, 0, -.2), (sgn * TILE * .45, 0, -4), (sgn * 3, 0, -9)], .7, 'cable')
    transform(bb, ww, m)
    transform(b, w, Matrix.Translation(p))


def hex_sites():
    n = int(FIELD_R / PITCH) + 2
    for q in range(-n, n + 1):
        for r in range(-n, n + 1):
            x = PITCH * (q + r / 2); y = PITCH * r * math.sqrt(3) / 2
            road = r == 0 or q == 0 or q + r == 0
            if math.hypot(x, y) <= FIELD_R and not road:
                yield Vector((x, y, 0))


def build():
    views(B=(30, 50), C=(-70, 18))
    mesa()
    sites = sorted(hex_sites(), key=lambda v: (v - Vector((60, -220, 0))).length)
    ctile = sites[0]
    for v in sites[1:]:
        tile(v)
    with group('C'):
        tile(ctile, detail=True)
    mark('LASER EMITTER', ctile + Vector((0, 0, 16)), 'ONE TILE OF MILLIONS / ALL KEPT IN PHASE')
    # Three service roads between the six blocks.
    for deg in (0, 60, 120):
        d = Vector((math.cos(math.radians(deg)), math.sin(math.radians(deg)), 0))
        n_ = Vector((-d.y, d.x, 0))
        for sgn in (-1, 1):
            tube('service road edge', [d * -FIELD_R * 1.05 + n_ * sgn * 9 + Vector((0, 0, .4)), d * FIELD_R * 1.05 + n_ * sgn * 9 + Vector((0, 0, .4))], .2, 'shell')
    x_, y_, z_ = sail_frame()
    # --- the beam as a light volume: rings along the axis, four faint edges ------
    yh = Vector((y_.x, y_.y, 0)).normalized()
    def beam(a, t):
        bot = (x_ * math.cos(a) + yh * math.sin(a)) * FIELD_R * .92 + Vector((0, 0, 34))
        top = sail_point(SAIL_R * .95, a, -1.5)
        return bot.lerp(top, t)
    for t in (.22, .44, .66, .86):
        tube('beam cross-section', [beam(T * k / 160, t) for k in range(161)], .2, 'accent')
    for a in (0, 90, 180, 270):
        q = math.radians(a + 12)
        tube('beam edge', [beam(q, .1), beam(q, .97)], .12, 'detail')
    # --- sail: billowed disc on the beam axis, ribs, hair-thin rim ---------------
    nr, na = 16, 120; vs = []; fs = []
    for i in range(nr + 1):
        for j in range(na):
            vs.append(sail_point(SAIL_R * i / nr, T * j / na))
    for i in range(nr):
        for j in range(na):
            p = i * na + j; q = i * na + (j + 1) % na
            fs.append((p, q, q + na, p + na))
    g.mesh('mirror sail', vs, fs, 'shell')
    tube('sail rim', [sail_point(SAIL_R, T * k / 200, .3) for k in range(201)], .2, 'detail')
    for k in range(12):
        a = T * k / 12 + T / 24
        tube('graphene rib', [sail_point(r, a, .4) for r in range(26, SAIL_R, 8)], .22, 'detail')
    # --- B: the chip at the apex (enlarged, in the sail frame) --------------------
    top = sail_point(0, 0, .4)
    m = Matrix((x_, y_, z_)).transposed().to_4x4(); m.translation = top
    with group('B'):
        bb = len(g.parts); ww = len(g.wires)
        box('probe chip', (0, 0, 1.6), (34, 34, 3.2), 1.2)
        box('chip die', (-7, -7, 3.6), (13, 13, .8), .3, 'detail')
        cyl('camera lens', (8, -8, 3.2), 4.6, 2.6, 'accent', (0, 0, 1), 32)
        cyl('laser comm aperture', (-8, 8, 3.2), 3.6, 3.2, 'accent', (0, 0, 1), 32)
        box('battery cell', (8, 8, 3.6), (10, 10, .8), .3, 'detail')
        for a in (45, 135, 225, 315):
            q = math.radians(a)
            box('photon thruster pod', (25 * math.cos(q), 25 * math.sin(q), 1.6), (7, 7, 3.2), 1.2)
            rod('pod strut', (17 * math.cos(q), 17 * math.sin(q), 1.6), (21.5 * math.cos(q), 21.5 * math.sin(q), 1.6), .7, 'detail')
        transform(bb, ww, m)
    mark('SAIL CHIP', top + z_ * 4, 'ONE GRAM / CAMERA, LASER, FOUR THRUSTERS')
    mark('MIRROR SAIL', sail_point(SAIL_R * .96, math.radians(200), 1), 'DRAWN ENLARGED / REALLY 4 m, THINNER THAN SOAP FILM')
    mark('BEAM', beam(math.radians(100), .55), '100 GW FOR THREE MINUTES')
    a = math.radians(-20)
    mark('LASER FIELD', Vector(((mesa_edge(a) + 40) * math.cos(a), (mesa_edge(a) + 40) * math.sin(a), -40)), '3.5 km ACROSS / ONE HIGH PLATEAU')
    return 30, 26
