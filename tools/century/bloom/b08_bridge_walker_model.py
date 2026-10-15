"""BRIDGE WALKER: cable-riding robot laying a suspended footbridge, day five.

Scale: 1 unit = 5 cm. The bridge runs along X; towers at x = +-180 (18 m
span), deck 1.2 m wide (24 units), handrail rope 1.1 m (22 units) above
the planks. Deck sag 0.5 m; main cables (y = +-18) from 3.1 m tower tops
sag to 1.1 m above mid-deck (f = 2.5 m). Water 3.2 m below the crest.
Two landform banks at opposite corners of the view (crest, contours,
shoreline, boulders) carry the towers and the anchor blocks. The robot
(3 m over its magazine and lay arm, 60 units) straddles both main cables
at mid-span on four grooved sheaves; it lays transverse planks behind
itself (done from the near bank so far, bare cross-beams ahead) and pays
out the handrail rope from its spool. The inspector (1.75 m, 35 units)
stands on the near bank crest.
"""
from ..kit import *
from .parts import loft, sphere, arc_tube, lumpy
from ..humans import human

L = 180
ROBOT_X = 12
CY, RY, DW = 18, 13, 12       # main cable y, handrail rope y, deck half width
WATER = -64
SAG_DECK, CABLE_LOW, F = 10, 12, 50


def deck_z(x):
    return -SAG_DECK * (1 - (x / L) ** 2)


def cable_z(x):
    return CABLE_LOW + F * (x / L) ** 2


# Bank profile, left bank (mirrored for the right): distance from the
# river centre -> height. Plateau, crest at 228, slope to the water at 172.
PROF = [(252, 3), (205, 1), (170, 0), (158, -12), (142, -34), (128, -52), (116, WATER), (110, WATER - 6)]


def prof_z(d):
    for (d0, z0), (d1, z1) in zip(PROF, PROF[1:]):
        if d1 <= d <= d0:
            return z0 + (z1 - z0) * (d0 - d) / (d0 - d1)
    return PROF[0][1] if d > PROF[0][0] else PROF[-1][1]


def prof_d(z):
    """Inverse on the slope part (monotone from crest to water)."""
    k = next(i for i, (d, z) in enumerate(PROF) if z == 0)
    for (d0, z0), (d1, z1) in zip(PROF[k:], PROF[k + 1:]):
        if z1 <= z <= z0:
            return d0 + (d1 - d0) * (z0 - z) / (z0 - z1)
    return None


def wobble(y):
    return 7 * math.sin(y / 23.0) + 4 * math.sin(y / 9.0 + 1.3)


def ground_z(x, y):
    return prof_z(abs(x) - wobble(y))


def half_width(d):
    """Bank patch outline: widest at the water, tapering toward the back."""
    t = (252 - d) / (252 - 110)
    return 50 + 30 * math.sqrt(max(0, math.sin(math.pi * min(1, t))))


def bank(sign):
    ds = [252 - (252 - 110) * i / 40 for i in range(41)]
    nv = 24
    vs = []; fs = []
    for d in ds:
        w = half_width(d)
        for j in range(nv + 1):
            y = -w + 2 * w * j / nv
            vs.append((sign * (d + wobble(y)), y, prof_z(d)))
    m = nv + 1
    for i in range(len(ds) - 1):
        for j in range(nv):
            a = i * m + j
            fs.append((a, a + 1, a + m + 1, a + m) if sign < 0 else (a, a + m, a + m + 1, a + 1))
    # Invisible occluder: the exporter skips edges of 'tube'-role meshes, so the
    # ground hides what is behind it but is drawn only by its authored lines.
    g.mesh('river bank', vs, fs, 'detail')
    # Crest line and contours: y-dependent through the same wobble.
    def line_at(z, name, role, r=.12):
        d0 = prof_d(z)
        pts = []
        for k in range(41):
            wmax = half_width(d0)
            y = -wmax + 2 * wmax * k / 40
            pts.append((sign * (d0 + wobble(y)), y, z + .4))
        tube(name, pts, r, role)
    line_at(-.01, 'bank crest', 'structure', .2)
    for z in (-18, -36, -54):
        line_at(z, 'bank contour', 'shell')
    line_at(WATER, 'shoreline', 'detail', .15)
    # Fall-line hachures from the crest, longer where the slope is steep.
    dc = prof_d(-.01); dw = prof_d(WATER)
    for k in range(15):
        wmax = half_width(dc) * .92
        y = -wmax + 2 * wmax * (k + .5) / 15
        L_ = .55 if k % 2 else .32
        d1 = dc + (dw - dc) * L_
        tube('slope hachure', [(sign * (dc + wobble(y)), y, prof_z(dc) - .2), (sign * (d1 + wobble(y)), y, prof_z(d1) + .3)], .1, 'shell')
    # Plateau edge behind the anchors: a short broken ground line.
    for y0, y1 in ((-40, -12), (8, 36)):
        tube('ground line', [(sign * (236 + wobble(y)), y, prof_z(236) + .2) for y in [y0 + (y1 - y0) * k / 8 for k in range(9)]], .1, 'shell')
    # Boulders along the shoreline and one on the crest.
    for k, (dd, y, r) in enumerate(((114, -48, 7), (118, -18, 5), (113, 22, 8), (120, 50, 5.5), (174, 44, 6))):
        o, _ = lumpy('boulder', (sign * (dd + wobble(y)), y, prof_z(dd) + r * .35), r, seed=7 + k + (20 if sign > 0 else 0),
                     stretch=(1.1, 1, .7), seg=28, rings=14, role='detail')


def tower(xs):
    s_ = 1 if xs > 0 else -1
    for side in (-1, 1):
        gz = ground_z(xs + s_ * 6, side * 34)
        base = Vector((xs + s_ * 6, side * 34, gz)); top = Vector((xs, side * CY, cable_z(xs)))
        rod('tower leg', base, top, 3.0)
        box('tower footing', base + Vector((0, 0, -1)), (20, 20, 6), 1.6)
        box('cable saddle', top + Vector((0, 0, 2.6)), (11, 6, 5), 1.4, 'structure')
        cyl('saddle sheave', top + Vector((0, -3, 3.4)), 3.6, 6, 'detail', (0, 1, 0), 24)
    for z in (18, 46):
        t = (z) / (cable_z(xs))
        y = 34 + (CY - 34) * t
        rod('tower cross tie', (xs + s_ * 6 * (1 - t), -y, z), (xs + s_ * 6 * (1 - t), y, z), 1.8)
    for side in (-1, 1):
        rod('tower diagonal', (xs + s_ * 4.6, side * 30, 18), (xs + s_ * 2.4, -side * 24, 46), 1.2, 'detail')


def plank(x, role='structure'):
    z = deck_z(x)
    box('deck plank', (x, 0, z + 1.4), (4.6, 2 * DW, 1.2), .3, role)


def build():
    views(B=(-66, 24), C=(-52, 18))
    hx, hy = -202, -26
    human(p=(hx, hy, ground_z(hx, hy)), scale=.056, angle=-30)
    bank(-1); bank(1)
    # Water: long ripple lines along the current (the river runs along y).
    for x, y0, y1 in ((-86, -70, 30), (-40, -90, -10), (-4, -30, 70), (36, -80, 10), (76, -20, 64), (96, -70, -30)):
        tube('ripple', [(x + 3 * math.sin(k / 3), y0 + (y1 - y0) * k / 12, WATER) for k in range(13)], .1, 'shell')
    tower(-L); tower(L)
    for side in (-1, 1):
        tube('main cable', [(x, side * CY, cable_z(x)) for x in range(-L, L + 1, 4)], .9, 'structure')
        for xs in (-L, L):
            s_ = 1 if xs > 0 else -1
            ax = xs + s_ * 52; gz = ground_z(ax, side * 30)
            tube('backstay', [(xs, side * CY, cable_z(xs)), (ax - s_ * 3, side * 30, gz + 4)], .9, 'structure')
            box('anchor block', (ax, side * 31, gz + 1.5), (16, 14, 7), 1.2)
            cyl('anchor eye', (ax - s_ * 5, side * 30, gz + 4), 1.8, 3, 'detail', (0, 1, 0), 16)
    for x in range(-L + 20, L - 19, 20):
        dz = deck_z(x)
        rod('cross beam', (x, -DW - 3, dz), (x, DW + 3, dz), 1.2, 'structure')
        for side in (-1, 1):
            tube('suspender', [(x, side * CY, cable_z(x)), (x, side * (DW + 2.6), dz + .6)], .25, 'detail')
    for side in (-1, 1):
        tube('deck stringer', [(x, side * (DW - 3), deck_z(x) + .4) for x in range(-L + 12, L - 11, 12)], .5, 'detail')
    x = -L + 16; last = x
    while x < ROBOT_X - 58:
        if x > ROBOT_X - 76:
            with group('C'):
                plank(x)
        else:
            plank(x)
        last = x; x += 5.2
    for side in (-1, 1):
        tube('handrail rope', [(xx, side * RY, deck_z(xx) + 22) for xx in range(-L, int(last) + 1, 8)], .45, 'cable')
        for xx in range(-L + 20, int(last), 20):
            rod('handrail post', (xx, side * RY, deck_z(xx) + .6), (xx, side * RY, deck_z(xx) + 22), .5, 'detail')
    zc = robot(last)
    mark('CABLE CARRIAGE', (ROBOT_X + 30, -CY - 7, zc + 12), '3 m / RIDES THE CABLES IT HELPED STRING')
    mark('A-FRAME TOWER', (L + 3, -CY - 3, cable_z(L) - 10), '3.1 m / STEEL TUBE, BOLTED ON SITE')
    ax = -L - 52
    mark('ANCHOR BLOCK', (ax, -38, ground_z(ax, -31) + 5), 'PROOF-LOADED BEFORE THE DECK GOES ON')
    mark('INSPECTOR', (hx, hy - 3, ground_z(hx, hy) + 24), 'CHOSEN BY THE VILLAGE / SIGNS EACH ANCHOR')
    mark('FINISHED DECK', (-110, -DW - 1, deck_z(-110) + 2), '1.2 m WIDE / HANDRAIL AT 1.1 m')
    return -56, 34


def robot(last):
    """3 m carriage on the main cables; each group encloses its own transform."""
    x0 = ROBOT_X; zc = cable_z(x0)
    slope = math.degrees(math.atan(2 * F * x0 / L ** 2))
    M = Matrix.Translation((x0, 0, zc)) @ Matrix.Rotation(math.radians(-slope), 4, 'Y')
    frame = lambda: at((x0, 0, zc), -slope, 'Y')
    hx = -52
    dz_deck = deck_z(x0 + hx) - zc
    with frame():
        for side in (-1, 1):
            for dx in (-22, 22):
                cyl('cable sheave', (dx, side * CY - 3, 6.8), 6.8, 6, 'structure', (0, 1, 0), 44)
                cyl('sheave hub', (dx, side * CY - 3.6, 6.8), 2.2, 7.2, 'detail', (0, 1, 0), 20)
                ring('sheave rim', (dx, side * CY + 3.2, 6.8), 6.8, 1.2, .6, (0, 1, 0), 'detail')
                cyl('pinch roller', (dx, side * CY - 2, -3.8), 2.6, 4, 'detail', (0, 1, 0), 24)
                box('sheave fork', (dx, side * (CY + 4.8), 3.4), (11, 2.4, 18), 1, 'structure')
                motor((dx, side * (CY + 6.4), 6.8), 3.4, 7, (0, side, 0))
            rod('side beam', (-30, side * (CY + 6.2), 11), (30, side * (CY + 6.2), 11), 2.6)
        for dx in (-29, 29):
            rod('cross beam', (dx, -CY - 6.2, 11), (dx, CY + 6.2, 11), 2.6)
        box('battery case', (6, 0, 19), (14, 28, 10), 1.6)
        for k in range(4):
            box('battery rib', (6 - 5 + k * 3.4, -14.6, 19), (1, .8, 8), .3, 'detail')
        # Solar roof over the battery and spool: a flat slab on four posts.
        for dx in (-2, 30):
            for side in (-1, 1):
                rod('roof post', (dx, side * 16, 15), (dx, side * 16, 46), 1.1, 'structure')
        box('solar roof', (14, 0, 47.2), (40, 38, 1.8), .8, 'structure')
        for k in range(1, 5):
            tube('roof cell seam', [(-6 + 8 * k, -18.5, 48.3), (-6 + 8 * k, 18.5, 48.3)], .08, 'shell')
        box('status lamp', (32, 0, 49), (2.4, 2.4, 1.6), .5, 'accent')
    sx = 22
    with group('B'):
        with frame():
            cyl('spool drum', (sx, -11, 30), 5.8, 22, 'structure', (0, 1, 0), 44)
            for y in (-11, 11):
                cyl('spool flange', (sx, y - .6, 30), 9, 1.2, 'structure', (0, 1, 0), 48)
            for k in range(18):
                ring('rope wrap', (sx, -10 + k * 1.2, 30), 6.6, .5, .9, (0, 1, 0), 'cable')
            for y in (-13, 13):
                box('spool cheek', (sx, y, 25.5), (7, 1.4, 14), .5, 'structure')
            cyl('brake disc', (sx, 13.9, 30), 6.4, .6, 'accent', (0, 1, 0), 40)
            box('brake caliper', (sx + 5.4, 14.2, 32.8), (2.8, 2.6, 4), .4, 'detail')
            motor((sx, -24, 30), 3.2, 7, (0, 1, 0))
            rod('level-wind screw', (sx - 10, -12, 24.5), (sx - 10, 12, 24.5), .8, 'detail')
            for k in range(24):
                ring('screw thread', (sx - 10, -11.5 + k, 24.5), 1.2, .35, .35, (0, 1, 0), 'detail')
            box('wind guide', (sx - 10, 3, 26.5), (3.4, 3.4, 3.4), .6, 'accent')
            cyl('load cell pulley', (sx - 17, 3, 21.5), 2.6, 2.2, 'structure', (0, 1, 0), 24)
            box('load cell', (sx - 17, 3, 18), (2.2, 4.4, 2.6), .4, 'accent')
            tube('rope lead', [(sx - 4, 3, 30), (sx - 10, 3, 26.6), (sx - 17, 3, 24.1), (sx - 19.6, 3, 21.5)], .35, 'cable')
            box('spool frame', (sx, 0, 16.6), (16, 30, 2), .6, 'detail')
    top = dz_deck + 28
    with group('C'):
        with frame():
            box('chassis deck', (0, 0, 14), (60, 40, 2.6), 1)
            for k in range(14):
                box('magazine plank', (-14, 0, 17.4 + k * 1.5), (4.6, 2 * DW, 1.2), .3, 'detail')
            for dx in (-17.4, -10.6):
                for side in (-1, 1):
                    rod('magazine guide', (dx, side * 13, 15), (dx, side * 13, 40), .8, 'structure')
            box('magazine cap', (-14, 0, 40.6), (8.8, 29, 1.6), .5, 'structure')
            box('arm base bracket', (-31, 0, 12), (4.4, 22, 14), .8)
            for side in (-1, 1):
                y = side * 8.6
                for zb, zh in ((17, top), (8, top - 9)):
                    rod('parallel link', (-31, y, zb), (hx, y, zh), 1.4, 'structure')
                    cyl('link pin', (-31, y - 1.6, zb), 1.6, 3.2, 'detail', (0, 1, 0), 16)
                    cyl('link pin', (hx, y - 1.6, zh), 1.6, 3.2, 'detail', (0, 1, 0), 16)
            rod('actuator body', (-18, 0, 12), (-31, 0, 2), 1.7, 'structure')
            rod('actuator rod', (-31, 0, 2), (-40, 0, (8 + top - 9) / 2 - 1), .8, 'detail')
            for side in (-1, 1):
                rod('head post', (hx, side * 8.6, top + 1), (hx, side * 8.6, dz_deck + 8), 1.2, 'structure')
            rod('head tie', (hx, -8.6, top - 5), (hx, 8.6, top - 5), 1.0, 'detail')
            box('clamp beam', (hx - 1, 0, dz_deck + 6.8), (4.4, 2 * DW + 4, 2.6), .6)
            for side in (-1, 1):
                box('clamp jaw', (hx - 1, side * (DW + 1.3), dz_deck + 4.3), (5.4, 1.8, 5.6), .4, 'structure')
                cyl('jaw pad', (hx - 1, side * (DW + .3), dz_deck + 3.2), 1.2, .6, 'accent', (0, -side, 0), 12)
            box('held plank', (hx - 1, 0, dz_deck + 3.2), (4.6, 2 * DW, 1.2), .3, 'accent')
            rod('driver slide rail', (hx + 3.8, -DW, dz_deck + 11.5), (hx + 3.8, DW, dz_deck + 11.5), .7, 'detail')
            box('driver carriage', (hx + 3.8, 7, dz_deck + 11.5), (3.8, 4.4, 3.8), .6, 'structure')
            cyl('bolt driver', (hx + 3.8, 7, dz_deck + 9.6), 1.6, 5.4, 'structure', (0, 0, -1), 20)
            cyl('driver bit', (hx + 3.8, 7, dz_deck + 4.2), .5, 2.6, 'accent', (0, 0, -1), 12)
            box('deck camera', (hx + 4.4, -10, top - 2), (3.2, 2.8, 2.6), .5, 'detail')
            cyl('camera lens', (hx + 4.4, -11.6, top - 2.6), 1, .8, 'accent', (0, -1, -1), 12)
    mark('DECK LAYER', M @ Vector((hx - 1, -DW - 2.4, dz_deck + 4.3)), 'ONE PLANK EVERY 90 SECONDS')
    tube('rope to spool', [(last, -RY, deck_z(last) + 22), (x0 - 16, -8, zc + 22), (x0 + 4, -8, zc + 27)], .3, 'cable')
    return zc
