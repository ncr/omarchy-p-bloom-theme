"""SUN STILL: heliostat-fed multi-effect distillation tower with salt recovery.

Scale: 1 unit = 10 cm. Z = 0 is the ground. The tower is 36 m to the top of
the receiver crown: a 2 m plinth, fourteen 2 m effects stacked from z = 20
to z = 300, a cavity receiver and gallery above. The first (hottest, 70 C)
effect is at the top; the stack widens downward from 6 m to 9.6 m
because colder vapour at lower pressure needs more volume. A spiral stair
(1.2 m treads, handrail 1 m) climbs 3 turns to the gallery. Seventeen
of the 380 heliostats (4 x 4 m mirrors on 3 m pedestals) are drawn in the
front sector. At the base: seawater intake, hot-water store, freshwater
tank and the crystallisers and product shed of the salt recovery.
The mannequin is 1.75 m (17.5 units) and stands by the tower door.
"""
from ..kit import *
from .parts import loft, sphere, arc_tube, dome
from ..humans import human

N_EFF = 14
Z0, H_EFF = 20, 20
RECEIVER = Vector((0, 0, 322))
MIRROR = 40                     # 4 m square heliostat
FIELD = -66                     # azimuth of the field centre (deg)
SUN = Vector((.35, -.45, .82)).normalized()
B_EFFECTS = (6, 7, 8)


def r_at(z):
    """Tower radius: 48 at the plinth to 30 under the crown (linear)."""
    t = max(0, min(1, (z - Z0) / (N_EFF * H_EFF)))
    return 48 - 18 * t


def frustum(name, z0, z1, r0, r1, role='structure', n=72):
    vs = [(r0 * math.cos(T * j / n), r0 * math.sin(T * j / n), z0) for j in range(n)]
    vs += [(r1 * math.cos(T * j / n), r1 * math.sin(T * j / n), z1) for j in range(n)]
    fs = [(j, (j + 1) % n, n + (j + 1) % n, n + j) for j in range(n)]
    fs += [tuple(reversed(range(n))), tuple(range(n, 2 * n))]
    return g.mesh(name, vs, fs, role)


def effect_internals(k):
    """Horizontal-tube falling-film effect: spray bar, tube bundle, tray."""
    z0 = Z0 + k * H_EFF; r = r_at(z0 + H_EFF / 2) - 3
    cyl('effect floor', (0, 0, z0), r_at(z0) - 1.2, .8, 'detail')
    # Tube bundle: heating vapour from the effect above condenses inside.
    for i, zz in enumerate((z0 + 6, z0 + 8.4, z0 + 10.8)):
        for j in range(-4, 5):
            y = j * 2.6 + (1.3 if i % 2 else 0)
            half = math.sqrt(max(4, (r - 6) ** 2 - y * y))
            cyl('bundle tube', (-half, y, zz), .8, 2 * half, 'detail', (1, 0, 0), 10)
    for x in (-r * .55, r * .55):
        box('tube sheet', (x, 0, z0 + 8.4), (1.2, 24, 9), .4, 'structure')
    # Spray bar wets the outside of the tubes with brine.
    rod('brine spray bar', (-r + 5, 0, z0 + 14.5), (r - 5, 0, z0 + 14.5), .9, 'structure')
    for x in range(int(-r + 8), int(r - 7), 4):
        cyl('spray nozzle', (x, 0, z0 + 13.6), .45, 1, 'accent', (0, 0, -1), 8)
    # Distillate tray under the bundle, brine sump at the floor.
    ring('distillate tray', (0, 0, z0 + 2.4), r - 7, 1, 1.4)
    box('demister pad', (0, r - 5.5, z0 + 10), (22, 2.4, 10), .4, 'detail')
    for x in (-8, 0, 8):
        tube('demister seam', [(x, r - 6.8, z0 + 5.4), (x, r - 6.8, z0 + 14.6)], .1, 'shell')


def heliostat(p, drive_detail=False):
    p = Vector(p)
    top = p + Vector((0, 0, 30))
    to_rec = (RECEIVER - top).normalized()
    nrm = (to_rec + SUN).normalized()
    cyl('pedestal footing', p, 3.2, 2, 'structure', n=24)
    rod('pedestal', p + Vector((0, 0, 2)), top, 1.8)
    box('two-axis drive', top, (7, 7, 6), 1.4, 'structure')
    side = nrm.cross(Vector((0, 0, 1))).normalized()
    rod('torque tube', top - side * 17, top + side * 17, 1.1, 'detail')
    panel('heliostat mirror', top + nrm * 3.6, (MIRROR, MIRROR), nrm, 4, 4, 'shell')
    if drive_detail:
        cyl('azimuth ring', top + Vector((0, 0, -3.4)), 4.2, 1.2, 'detail', n=32)
        cyl('elevation gear', top + side * 3.6, 3, 1, 'detail', side, 24)
        box('drive motor', top + Vector((0, 0, -6)) - side * 3, (3, 3, 4), .8, 'detail')
        tube('drive cable', [top + Vector((0, 0, -8)), p + Vector((0, 0, 6)), p + Vector((0, 0, 2))], .25, 'cable')
    return top, nrm


def cleaning_robot(p, heading):
    p = Vector(p); f = Vector((math.cos(heading), math.sin(heading), 0)); s_ = Vector((-f.y, f.x, 0))
    box('robot chassis', p + Vector((0, 0, 5)), (16, 10, 5), 1.6)
    for a in (-1, 1):
        for b in (-1, 1):
            cyl('robot wheel', p + f * a * 5.5 + s_ * b * 5.6 + Vector((0, 0, 2.6)), 2.6, 1.6, 'detail', s_ * b, 20)
    cyl('rinse tank', p + Vector((0, 0, 7.5)) - f * 3, 3, 4, 'detail', n=20)
    rod('brush mast', p + Vector((0, 0, 7.5)) + f * 4, p + Vector((0, 0, 24)) + f * 4, .9)
    rod('brush boom', p + Vector((0, 0, 24)) + f * 4, p + Vector((0, 0, 24)) + f * 4 + s_ * 12, .8)
    cyl('rotary brush', p + Vector((0, 0, 24)) + f * 4 + s_ * 12 - f * 13, 1.6, 26, 'accent', f, 16)


def build():
    views(B=(14, 6), C=(40, 14))
    human(p=(16, -68, 0), scale=.028, angle=8)
    # --- plinth and the effect stack -----------------------------------------
    cyl('tower plinth', (0, 0, 0), 54, 20)
    ring('plinth cornice', (0, 0, 17), 55.6, 2.4, 3, role='detail')
    for k in range(N_EFF):
        z0 = Z0 + k * H_EFF
        role = 'structure'
        cm = group('B') if k in B_EFFECTS else None
        if cm:
            cm.__enter__()
        frustum('effect shell', z0, z0 + H_EFF, r_at(z0), r_at(z0 + H_EFF), role)
        if k in B_EFFECTS:
            arc_tube('cutaway back shell', (0, 0, z0), (0, 0, 1), (0, 1, 0), r_at(z0 + H_EFF) - 1.2, .8, H_EFF, -95, 95)
            effect_internals(k)
        if cm:
            cm.__exit__(None, None, None)
        ring('effect flange', (0, 0, z0 + H_EFF - 1), r_at(z0 + H_EFF) + 1.4, 2, 2, role='detail')
    uncover('B', 'effect shell')
    # --- crown: gallery, cavity receiver, cap ----------------------------------
    zc = Z0 + N_EFF * H_EFF
    ring('gallery deck', (0, 0, zc), 44, 16, 1.6)
    for k in range(20):
        q = T * k / 20
        rod('gallery stanchion', (43 * math.cos(q), 43 * math.sin(q), zc + 1.6), (43 * math.cos(q), 43 * math.sin(q), zc + 11.6), .6, 'detail')
    tube('gallery rail', [(43 * math.cos(T * k / 120), 43 * math.sin(T * k / 120), zc + 11.6) for k in range(121)], .6, 'structure')
    cyl('receiver drum', (0, 0, zc), 28, 32)
    # Cavity aperture faces the field (toward -y).
    with at((0, 0, 0), FIELD + 90):
        box('receiver aperture', (0, -27, zc + 17), (28, 3, 22), 2, 'accent')
        for x in (-10, -5, 0, 5, 10):
            tube('absorber tube', [(x, -28.7, zc + 7), (x, -28.7, zc + 27)], .3, 'accent')
    loft('receiver hood', [(0, 0, zc + 32), (0, 0, zc + 37), (0, 0, zc + 44)], lambda t: 31 - 22 * t * t, 48, 'structure', False)
    rod('lightning mast', (0, 0, zc + 44), (0, 0, zc + 64), .7, 'detail')
    # --- spiral stair: 3 turns from the plinth to the gallery ------------------
    turns = 3.0; n = 150; start = -100
    rail = []; inner = []
    for i in range(n + 1):
        t = i / n; z = Z0 + (zc - Z0) * t
        a = math.radians(start + 360 * turns * t)
        ri = r_at(z) + 1.5; ro = r_at(z) + 13
        u = Vector((math.cos(a), math.sin(a), 0))
        if i < n:
            g.box('stair tread', tuple(u * (ri + ro) / 2 + Vector((0, 0, z))), (11.5, 5, .8), 'detail').matrix_world = \
                Matrix.Translation(u * (ri + ro) / 2 + Vector((0, 0, z))) @ Matrix.Rotation(a, 4, 'Z') @ Matrix.Translation(-(u * (ri + ro) / 2 + Vector((0, 0, z))))
        rail.append(u * ro + Vector((0, 0, z + 10)))
        inner.append(u * ro + Vector((0, 0, z)))
        if i % 6 == 0:
            rod('stair stanchion', u * ro + Vector((0, 0, z)), u * ro + Vector((0, 0, z + 10)), .45, 'detail')
    tube('stair handrail', rail, .5, 'structure')
    tube('stair stringer', inner, .5, 'structure')
    # Door at the base, facing the field.
    box('tower door', (0, -53.8, 11.5), (10, 1.2, 21), .8, 'detail')
    box('door canopy', (0, -56.5, 23.2), (16, 6, 1.2), .4, 'detail')
    box('door handle', (3.4, -54.6, 11), (.6, .6, 3), .2, 'accent')
    # Risers and mains run inside the tower; only the ground connections show.
    # Hot-water store (16 h of night running) behind the tower.
    HS = (-128, 2)
    cyl('hot water store', (HS[0], HS[1], 0), 16, 46)
    loft('store roof', [(HS[0], HS[1], 46), (HS[0], HS[1], 50), (HS[0], HS[1], 53)], lambda t: 16.5 - 11 * t * t, 32, 'structure', False)
    for zz in (12, 24, 36):
        ring('store insulation band', (HS[0], HS[1], zz), 17.0, 1.0, 1.2, role='detail')
    box('store manway', (HS[0] + 6, HS[1] - 15.6, 9), (7, 1.4, 9), 1.2, 'detail')
    tube('store to tower', [(HS[0] + 16, HS[1], 8), (-80, 4, 8), (-52, 3, 8)], 1.1, 'cable')
    # Seawater intake from the shore and freshwater tank.
    tube('seawater intake', [(-190, -30, 4), (-120, -24, 4), (-70, -12, 4), (-40, -6, 6)], 1.6, 'structure')
    for x, y in ((-175, -29), (-140, -26), (-105, -21)):
        box('pipe sleeper', (x, y, 1.2), (4, 7, 2.4), .5, 'detail')
    cyl('freshwater tank', (-104, 84, 0), 22, 26)
    loft('tank roof', [(-104, 84, 26), (-104, 84, 29), (-104, 84, 31)], lambda t: 22.5 - 16 * t * t, 32, 'structure', False)
    tube('freshwater main', [(-40, 36, 5), (-64, 60, 5), (-84, 72, 5)], 1.2, 'cable')
    # --- salt recovery: two crystallisers, product shed with bagged salts ------
    for i, x in enumerate((86, 112)):
        c = Vector((x, 26 + i * 6, 0))
        for a in (0, 120, 240):
            q = math.radians(a)
            rod('crystalliser leg', c + Vector((9 * math.cos(q), 9 * math.sin(q), 0)), c + Vector((9 * math.cos(q), 9 * math.sin(q), 22)), .9)
        loft('crystalliser cone', [c + Vector((0, 0, 14)), c + Vector((0, 0, 20)), c + Vector((0, 0, 24))], lambda t: 2 + 9 * t ** .7, 32, 'structure', False)
        cyl('crystalliser body', c + Vector((0, 0, 24)), 11, 34)
        loft('crystalliser head', [c + Vector((0, 0, 58)), c + Vector((0, 0, 61)), c + Vector((0, 0, 63))], lambda t: 11 - 8 * t * t, 32, 'structure', False)
        ring('crystalliser band', c + Vector((0, 0, 40)), 11.3, .6, 1.2, role='detail')
    tube('brine to crystalliser', [(44, 16, 26), (64, 22, 34), (76, 26, 40)], .9, 'cable')
    # Open product shed: roof on six posts, pallets of 25 kg bags.
    sx, sy = 132, -36
    for dx in (-22, 22):
        for dy in (-14, 0, 14):
            rod('shed post', (sx + dx, sy + dy, 0), (sx + dx, sy + dy, 24), .8)
    box('shed roof', (sx, sy, 25), (52, 34, 1.4), .6, 'structure')
    for j in range(5):
        tube('roof rib', [(sx - 26 + 13 * j, sy - 17, 25.9), (sx - 26 + 13 * j, sy + 17, 25.9)], .1, 'shell')
    for i, (dx, dy) in enumerate(((-12, -6), (0, -6), (12, -6), (-12, 7), (0, 7))):
        box('pallet', (sx + dx, sy + dy, .8), (10, 10, 1.4), .3, 'detail')
        for lvl in range(3 if i % 2 == 0 else 2):
            for dd in (-2.4, 2.4):
                box('product bag', (sx + dx + dd, sy + dy, 2.6 + lvl * 2.6), (4.4, 9, 2.4), .9, 'detail' if i else 'accent')
    # --- heliostats: nearest two rows of the field -----------------------------
    front = []
    for r, angs in ((180, range(-40, 41, 16)), (236, range(-42, 43, 14)), (292, range(-42, 43, 12))):
        for a in angs:
            q = math.radians(FIELD + a)
            p = (r * math.cos(q), r * math.sin(q), 0)
            if a > 30:
                continue        # keep the salt shed readable behind the field
            if r == 180 and a in (-8, 8):
                front.append((a, p))
                continue
            heliostat(p)
    with group('C'):
        for a, p in front:
            top, nrm = heliostat(p, drive_detail=True)
            if a == 8:
                front_top = top
        q = math.radians(FIELD)
        cleaning_robot((156 * math.cos(q), 156 * math.sin(q), 0), q + math.pi / 2)
        mark('HELIOSTAT', front_top + Vector((0, 0, -14)), '4 × 4 m / 380 IN THE FIELD')
    # --- callouts ----------------------------------------------------------------
    mark('SOLAR RECEIVER', (28.7 * math.cos(math.radians(FIELD)), 28.7 * math.sin(math.radians(FIELD)), zc + 27), 'HEATS WATER TO 75 °C FOR THE TOP EFFECT')
    mark('EFFECT STACK', (-r_at(160) * .98, -r_at(160) * .2, 160), '2 m PER EFFECT / 6 TO 9.6 m ACROSS')
    mark('SPIRAL STAIR', (r_at(230) + 13, 0, 236), 'INSPECTION ON FOOT, THREE TURNS')
    mark('SALT RECOVERY', (123, 38, 44), 'CRYSTALLISERS AND PRODUCT SHED')
    mark('HOT WATER STORE', (-128 - 9, 2 - 13.4, 30), '16 h OF HEAT FOR THE NIGHT')
    mark('PLANT OPERATOR', (16, -70, 12), 'ONE OF SIX PEOPLE FROM TOWN WHO RUN IT')
    return 24, 26
