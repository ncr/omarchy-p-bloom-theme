"""REEF NURSERY: moored solar platform tending lattice trees of coral fragments.

Scale: 1 unit = 2 cm. Z = 0 is the waterline; the lagoon floor is at
z = -400 (8 m). A ring pontoon (6.6 m across the tube centres, 0.8 m tube)
carries a solid deck plate 0.5 m above calm water. Ten solar petals
(1.6 x 1.24 m, framed) form a raised canopy 2.4 m above the deck, tilted
10 degrees outward like an opening flower; the centre stays open for the
davit over the moon pool. Handrail 1.0 m. Three of the forty lattice trees
are drawn, close in: each hangs from a subsurface buoy 2 m down, with four
tiers of six arms; every arm carries two lines of two fragments (96 per
tree). A fragment tray (24 plugs) is being lowered from the davit.
"""
from ..kit import *
from .parts import loft, sphere, arc_tube

R_PONTOON = 165
R_TUBE = 20
DECK_Z = 21
TREE_R = 200
TREE_TOP = -100
TREES = [-135, -5, 110]           # azimuths (deg); -5 is the B tree


def torus(name, c, R, r, role='structure', n=120, m=20):
    c = Vector(c); vs = []; fs = []
    for i in range(n):
        a = T * i / n
        for j in range(m):
            b = T * j / m
            vs.append(c + Vector(((R + r * math.cos(b)) * math.cos(a), (R + r * math.cos(b)) * math.sin(a), r * math.sin(b))))
    for i in range(n):
        for j in range(m):
            fs.append((i * m + j, i * m + (j + 1) % m, ((i + 1) % n) * m + (j + 1) % m, ((i + 1) % n) * m + j))
    return g.mesh(name, vs, fs, role)


def circle(r, z, n=144, a0=0, a1=360):
    return [(r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), r * math.sin(math.radians(a0 + (a1 - a0) * k / n)), z) for k in range(n + 1)]


def fragment(p, s=1.0):
    """Branching coral colony hanging from its line: stalk and five arms, upturned."""
    p = Vector(p)
    organic_branch('coral fragment', [p, p + Vector((.3 * s, .2 * s, -2.4 * s)), p + Vector((.1 * s, .4 * s, -4.6 * s))], .9 * s, 'structure')
    for k, (dx, dy, h) in enumerate(((1, 0, 1.6), (-.6, .8, 2.4), (-.5, -.9, 3.0), (.4, -1, 3.8), (-.9, .1, 4.2))):
        q = p + Vector((0, 0, -h * s))
        organic_branch('coral branch', [q, q + Vector((dx * 2.2 * s, dy * 2.2 * s, .6 * s)), q + Vector((dx * 3.2 * s, dy * 3.2 * s, 2.4 * s)),
                                        q + Vector((dx * 3.6 * s, dy * 3.6 * s, 3.8 * s))], .55 * s, 'detail')


def tree(a_deg, tagged=False):
    from contextlib import nullcontext
    a = math.radians(a_deg)
    c = Vector((TREE_R * math.cos(a), TREE_R * math.sin(a), 0))
    top = c + Vector((0, 0, TREE_TOP)); H = 200; bottom = top + Vector((0, 0, -H))
    B = (lambda: group('B')) if tagged else nullcontext
    with B():
        sphere('subsurface buoy', top + Vector((0, 0, 17)), 15, 'structure', 36, 18)
        ring('buoy band', top + Vector((0, 0, 16.4)), 15.4, 1.2, 1.8, (0, 0, 1), 'detail')
        rod('buoy shackle', top + Vector((0, 0, 2.5)), top, .8, 'detail')
        rod('tree mast', top, top + Vector((0, 0, -108)), 2.6)
    rod('tree mast', top + Vector((0, 0, -108)), bottom, 2.6)
    ring('mast foot cap', bottom + Vector((0, 0, -1)), 3.4, 1, 2.2, (0, 0, 1), 'detail')
    for i, dz in enumerate((-24, -70, -116, -162)):
        z0 = top.z + dz
        with (B() if i < 2 else nullcontext()):
            cyl('arm clamp', Vector((c.x, c.y, z0 - 3.5)), 4.8, 7, 'structure', n=32)
            for j in range(6):
                q = math.radians(30 * (i % 2) + 60 * j + a_deg)
                u = Vector((math.cos(q), math.sin(q), 0))
                L = 66 - 6 * abs(i - 1.5)
                end = Vector((c.x, c.y, z0)) + u * L
                rod('branch arm', Vector((c.x, c.y, z0)), end, 1.4)
                ring('arm end cap', end, 2, .7, 1.4, u, 'detail')
                for f in (.55, .95):
                    hp = Vector((c.x, c.y, z0)) + u * (L * f)
                    tube('fragment line', [hp, hp + Vector((0, 0, -26))], .15, 'detail')
                    for k, dd in enumerate((-8, -20)):
                        fragment(hp + Vector((0, 0, dd)), 1.35 - .15 * k)
                if tagged and j == 0:
                    box('tier ID tag', Vector((c.x, c.y, z0)) + u * 10 + Vector((0, 0, 4)), (6, 1, 4), .4, 'accent')
    tube('tree anchor line', [bottom, Vector((c.x, c.y, -392))], .5, 'detail')
    box('tree anchor block', Vector((c.x, c.y, -396)), (24, 24, 9), 2)
    return c, top, bottom


def tray(p):
    """Outplanting tray: welded frame, ceramic plug grid, four-leg bridle."""
    p = Vector(p); W, D = 62, 42
    box('tray base plate', p, (W, D, 1.4), .6, 'shell')
    for sx in (-1, 1):
        rod('tray side rail', p + Vector((sx * W / 2, -D / 2, 1)), p + Vector((sx * W / 2, D / 2, 1)), 1.3)
    for sy in (-1, 1):
        rod('tray end rail', p + Vector((-W / 2, sy * D / 2, 1)), p + Vector((W / 2, sy * D / 2, 1)), 1.3)
    for x in (-W / 6, W / 6):
        rod('tray cross bar', p + Vector((x, -D / 2, 1)), p + Vector((x, D / 2, 1)), .8, 'detail')
    for i in range(6):
        for j in range(4):
            q = p + Vector((-W / 2 + W * (i + .5) / 6, -D / 2 + D * (j + .5) / 4, .7))
            cyl('ceramic plug', q, 2.6, 2.2, 'detail', n=20)
            organic_branch('plug fragment', [q + Vector((0, 0, 2.2)), q + Vector((.3, .2, 5)), q + Vector((.1, .4, 7.4))], .7, 'structure')
            for dx, dy in ((1, 0), (-.6, .8), (-.5, -.9)):
                organic_branch('plug branch', [q + Vector((0, 0, 4)), q + Vector((dx * 2, dy * 2, 5.6)), q + Vector((dx * 2.8, dy * 2.8, 7.6))], .45, 'detail')
    ring_c = p + Vector((0, 0, 34))
    ring('bridle ring', ring_c, 2.6, .9, 1.2, (0, 1, 0), 'structure')
    for sx in (-1, 1):
        for sy in (-1, 1):
            corner = p + Vector((sx * W / 2, sy * D / 2, 1.5))
            tube('bridle leg', [corner, ring_c + Vector((sx * 1.2, 0, -2))], .35, 'cable')
            cyl('bridle eye', corner, 1.2, 2.2, 'detail', n=12)
    box('reef destination tag', p + Vector((W / 2 + 2.2, 0, 1.5)), (1.2, 12, 6), .4, 'accent')
    return ring_c


def petal(ang):
    """Framed PV petal on a raked post, tilted 10 degrees outward."""
    tilt = math.radians(10)
    with at((0, 0, 0), ang):
        c = Vector((150, 0, DECK_Z + 128))
        nrm = Vector((-math.sin(tilt), 0, math.cos(tilt)))       # outer edge higher
        u = Vector((math.cos(tilt), 0, math.sin(tilt)))
        with at(c, -10, 'Y'):
            box('solar petal', (0, 0, 0), (80, 62, 1.6), .8, 'structure')
            for i in range(1, 5):
                tube('cell seam', [(-40 + 16 * i, -30, .9), (-40 + 16 * i, 30, .9)], .08, 'shell')
            for j in range(1, 4):
                tube('cell seam', [(-39, -31 + 15.5 * j, .9), (39, -31 + 15.5 * j, .9)], .08, 'shell')
            for sy in (-1, 1):
                rod('petal rail', (-40, sy * 31, -1.4), (40, sy * 31, -1.4), .9, 'detail')
        rod('petal post', (128, 0, DECK_Z + 2), c - u * 22 - nrm * 2.2, 1.6, 'structure')
        rod('petal strut', (128, 0, DECK_Z + 66), c + u * 24 - nrm * 2.2, 1.0, 'detail')
        rod('petal spar', c - u * 38 - nrm * 2.2, c + u * 38 - nrm * 2.2, .9, 'detail')


def build():
    views(B=(24, 10), C=(28, 38))
    # --- hull: pontoon ring and solid deck plate ------------------------------
    torus('ring pontoon', (0, 0, 0), R_PONTOON, R_TUBE)
    ring('deck plate', (0, 0, DECK_Z), 188, 128, 2.4)
    ring('deck fascia', (0, 0, DECK_Z - 5), 190, 2.4, 7.4)
    ring('moon pool coaming', (0, 0, -16), 60, 2.4, DECK_Z + 18.4)
    for k in range(20):
        q = T * k / 20
        tube('deck plate seam', [(62 * math.cos(q), 62 * math.sin(q), DECK_Z + 2.5), (187 * math.cos(q), 187 * math.sin(q), DECK_Z + 2.5)], .1, 'shell')
    # Waterline: where calm water meets the pontoon, and a wider swell ring.
    wr = R_PONTOON + math.sqrt(R_TUBE ** 2 - 4 ** 2)
    tube('waterline', circle(wr, -4, 200), .15, 'accent')
    tube('water surface', circle(262, -4, 220), .1, 'shell')
    # --- light handrail at 1.0 m, gate at the ladder ----------------------------
    gap = (-52, -28)
    pts = [(186 * math.cos(math.radians(d)), 186 * math.sin(math.radians(d)), DECK_Z + 52) for d in [gap[1] + (360 - (gap[1] - gap[0])) * k / 150 for k in range(151)]]
    tube('handrail', pts, .8, 'detail')
    for k in range(20):
        d = (360 * (k + .5) / 20 + 180) % 360 - 180
        if gap[0] - 4 < d < gap[1] + 4:
            continue
        q = math.radians(d)
        rod('rail stanchion', (186 * math.cos(q), 186 * math.sin(q), DECK_Z + 2.4), (186 * math.cos(q), 186 * math.sin(q), DECK_Z + 52), .8, 'detail')
    # --- raised solar canopy: ten framed petals ---------------------------------
    for k in range(10):
        petal(18 + 36 * k)
    # --- boarding ladder -------------------------------------------------------
    la = math.radians(-40)
    u = Vector((math.cos(la), math.sin(la), 0)); t_ = Vector((-math.sin(la), math.cos(la), 0))
    for s_ in (-1, 1):
        base = u * 189 + t_ * s_ * 12
        loft('ladder stile', [base + Vector((0, 0, DECK_Z + 50)), base + Vector((0, 0, DECK_Z + 2)), base + u * 12 + Vector((0, 0, -4)), base + u * 14 + Vector((0, 0, -64))], 1.1, 10)
    for k in range(5):
        z = -56 + 15 * k
        rod('ladder rung', u * 202 + t_ * -12 + Vector((0, 0, z)), u * 202 + t_ * 12 + Vector((0, 0, z)), .8, 'detail')
    # --- power cabinet on the deck under the canopy -------------------------------
    with at((0, 0, 0), 180):
        box('power cabinet', (152, 0, DECK_Z + 28), (34, 48, 52), 4)
        box('cabinet door', (134.6, 0, DECK_Z + 28), (1, 38, 42), 1.5, 'detail')
        box('cabinet handle', (133.6, -11, DECK_Z + 30), (1.2, 2, 9), .4, 'accent')
    # --- davit over the moon pool ----------------------------------------------
    post = Vector((0, 92, DECK_Z))
    cyl('davit base', post, 7, 5)
    bolts(post + Vector((0, 0, 5)), 5.4, 6, size=.8)
    rod('davit post', post, post + Vector((0, 0, 132)), 3.6)
    loft('davit boom', [post + Vector((0, 0, 130)), post + Vector((0, -32, 142)), (0, 6, DECK_Z + 128)], 2.8, 14, 'structure')
    cyl('sheave', (0, 3, DECK_Z + 125), 4, 2, 'detail', (1, 0, 0))
    cyl('winch drum', post + Vector((-4, 0, 56)), 5.8, 8, 'structure', (1, 0, 0))
    motor(post + Vector((4, 0, 56)), 4, 9, (1, 0, 0))
    with group('C'):
        rc = tray((0, 0, DECK_Z + 46))
    tube('lifting cable', [(0, 0, DECK_Z + 125), rc + Vector((0, 0, 2.6))], .4, 'cable')
    tube('winch cable', [post + Vector((0, -5.8, 56)), post + Vector((0, -3, 128)), (0, 3, DECK_Z + 129)], .4, 'cable')
    # --- moorings ---------------------------------------------------------------
    for ang in (0, 180):
        q = math.radians(ang)
        a0 = Vector(((R_PONTOON + 10) * math.cos(q), (R_PONTOON + 10) * math.sin(q), -12))
        a1 = Vector((300 * math.cos(q), 300 * math.sin(q), -392))
        tube('platform mooring', [a0, a0.lerp(a1, .5) + Vector((0, 0, -12)), a1], .5, 'detail')
        box('platform anchor', a1 + Vector((0, 0, -4)), (26, 26, 10), 2)
    # --- three lattice trees ------------------------------------------------------
    info = {a: tree(a, tagged=(a == -5)) for a in TREES}
    # --- callouts -------------------------------------------------------------------
    c, top, bottom = info[-5]
    q = math.radians(-5 + 90)
    mark('LATTICE TREE', Vector((c.x, c.y, TREE_TOP - 150)) + Vector((math.cos(q), math.sin(q), 0)) * 2, '3 OF 40 SHOWN / 96 FRAGMENTS EACH')
    ca, ta, ba = info[-135]
    mark('SUBSURFACE BUOY', ta + Vector((-10, -10, 17)), 'HOLDS EACH TREE 2 m DOWN, BELOW THE SWELL')
    mark('SEABED ANCHOR', Vector((ca.x + 10, ca.y - 10, -392)), 'VERTICAL LINES / NOTHING DRAGS ON THE REEF')
    q = math.radians(-18)
    mark('SOLAR CANOPY', (188 * math.cos(q), 188 * math.sin(q), DECK_Z + 135), '10 PETALS / 4 kW PEAK / 30 kWh STORE')
    mark('DAVIT', post + Vector((0, -3.6, 118)), 'LOWERS ONE TRAY OF 24 AT A TIME')
    q = math.radians(200)
    mark('WATERLINE', (wr * math.cos(q), wr * math.sin(q), -4), 'DECK 0.5 m ABOVE CALM WATER')
    return 20, 20
