"""ICE STUPA: a winter-built cone of ice that waters a mountain village in spring.

Scale: 1 unit = 10 cm. The cone stands on the valley floor at the origin,
30 m tall and 18 m across (radius 90 units, flaring to ~11 m at the foot), built by spraying stream
water from a riser at its apex through the winter nights. A feed pipe
comes down the slope from an intake on the stream, 60 m above the base,
so the mountain supplies the pressure. Terraced barley fields step down
toward the viewer on the right; a melt channel runs to them from the foot
of the cone. One person stands at the valve pit (1.75 m = 17.5 units).
Cone volume: 1/3 pi 9^2 30 = 2 545 m3 of ice x 0.917 -> about 2.3 million L.
"""
from ..kit import *
from .parts import loft, sphere, arc_tube, lumpy
from ..humans import human

H = 300            # cone height
R0 = 90            # base radius
PIT = Vector((-124, -62, 0))
BANDS = (74, 146, 218)     # growth ledges: one per long cold spell
FRONT = math.radians(-110) # azimuth facing the camera (A view az -20)


def soft(v, k=40.0):
    return k * math.log1p(math.exp(v / k))


def ground_z(x, y):
    """Flat pad round the cone; the slope rises behind and to the left, falls to the front."""
    d = math.hypot(x, y)
    f = min(1.0, max(0.0, (d - 135) / 90)); f = f * f * (3 - 2 * f)
    up = .5 * soft(y - 130) + .15 * soft(-x - 200)
    down = -.14 * soft(-y - 110)
    return f * (up + down)


def cone_r(z, a):
    """Irregular cone: gentle lumps, a refrozen flare at the foot, a lip at every growth ledge."""
    t = max(0.0, z) / H
    base = R0 * (1 - t) ** .92 * (1 + .05 * math.sin(math.pi * t))
    lump = 1 + .03 * math.sin(2 * a + 1.1 + 3 * t) + .018 * math.sin(5 * a + .4 - 4 * t) + .012 * math.sin(3 * a + 7 * t + 2)
    u = max(0.0, (.15 - t) / .15)
    skirt = 1 + .24 * u * u
    r = base * lump * skirt
    for k, zb in enumerate(BANDS):
        d = zb - z
        amp = 4.0 * (1 - t) * (.75 + .25 * math.sin(3 * a + k * 1.7))
        if 0 <= d < 14:
            r += amp * (1 - d / 14) ** 2           # drapery thickening to the lip
        elif -3 < d < 0:
            r += amp * (1 + d / 3)                 # sloped top: no shelf seen from above
    return max(1.4, r)


def on_cone(z, a, k=1.006):
    r = cone_r(z, a) * k
    return (r * math.cos(a), r * math.sin(a), z)


def cone():
    zs = sorted(set([H * i / 80 for i in range(81)] + [zb + o for zb in BANDS for o in (-.02, .75, 1.5, 2.25, 3.0)]))
    na = 180
    vs = []; fs = []
    for z in zs:
        for j in range(na):
            a = math.tau * j / na
            r = cone_r(z, a)
            vs.append((r * math.cos(a), r * math.sin(a), z if z > 0 else -3))
    nz = len(zs) - 1
    for i in range(nz):
        for j in range(na):
            a = i * na + j; b = i * na + (j + 1) % na
            fs.append((a, b, b + na, a + na))
    fs.append(tuple(reversed(range(na))))
    fs.append(tuple(nz * na + j for j in range(na)))
    g.mesh('ice cone', vs, fs, 'structure')
    # Where the ice meets the ground (the far half is hidden by the cone).
    tube('cone foot', [(cone_r(0, a) * math.cos(a), cone_r(0, a) * math.sin(a), .4) for a in [math.tau * k / 240 for k in range(241)]], .7, 'structure')
    # Growth ledges on the camera side only (surface lines stay off the limbs).
    span = [FRONT + math.radians(-62 + 124 * k / 90) for k in range(91)]
    for zb in BANDS:
        tube('growth ledge', [on_cone(zb - .3, a, 1.004) for a in span], .45, 'detail')
    # Icicle fringe under the two lower ledges.
    for n_, zb in enumerate(BANDS[:2]):
        for k in range(-56, 57, 4):
            a = FRONT + math.radians(k + 2 * n_)
            x, y, z = on_cone(zb - .3, a, 1.004)
            ln = 3 + 6 * (((k + 60) * 7 + n_ * 3) % 11) / 10
            tube('icicle', [(x, y, z), (x * 1.001, y * 1.001, z - ln)], .22, 'shell')
    # Drip-curtain ribs on the front face, each from a ledge down toward the next.
    for k, (deg, zb, ln) in enumerate(((-38, 182, 46), (-22, 122, 52), (-8, 182, 40), (6, 62, 44), (18, 122, 56), (30, 62, 40), (44, 182, 34))):
        a0 = FRONT + math.radians(deg)
        tube('drip rib', [on_cone(z, a0 + .015 * math.sin(z / 9 + k)) for z in [zb - 15 - ln * m / 16 for m in range(17)]], .3, 'detail')
    # Shade on the lee side: short fall-line strokes, well inside the right limb.
    for k in range(26):
        deg = 52 + 18 * ((k * 7) % 13) / 12
        z0 = 14 + 230 * ((k * 5) % 26) / 26
        a = FRONT + math.radians(deg)
        ln = 10 + 12 * ((k * 3) % 5) / 4
        if any(0 < zb - z0 < 16 for zb in BANDS):
            continue
        tube('shade stroke', [on_cone(z, a) for z in (z0, z0 - ln * .5, z0 - ln)], .18, 'shell')


def ground():
    xs = [-900 + 1700 * i / 85 for i in range(86)]
    ys = [-700 + 1500 * j / 75 for j in range(76)]
    vs = [(x, y, ground_z(x, y)) for x in xs for y in ys]
    m = len(ys); fs = []
    for i in range(len(xs) - 1):
        for j in range(m - 1):
            a = i * m + j
            fs.append((a, a + m, a + m + 1, a + 1))
    g.mesh('valley ground', vs, fs, 'tube')           # occluder only
    # Near edge of the valley floor: an irregular open patch like a surveyed plot.
    def edge_r(a):
        return 188 + 12 * math.sin(3 * a + .7) + 6 * math.sin(7 * a + 2.1)
    pts = []
    for k in range(121):
        a = math.radians(-205 + 222 * k / 120)
        r = edge_r(a)
        pts.append((r * math.cos(a), -10 + r * math.sin(a), ground_z(r * math.cos(a), -10 + r * math.sin(a)) + .4))
    tube('valley floor edge', pts, .45, 'detail')
    # Short fall-line hachures just inside the front edge: the floor drops away.
    for k in range(17):
        a = math.radians(-195 + 200 * (k + .5) / 17)
        r = edge_r(a)
        r0 = r - (16 if k % 2 else 9)
        tube('edge hachure', [(rr * math.cos(a), -10 + rr * math.sin(a), ground_z(rr * math.cos(a), -10 + rr * math.sin(a)) + .4) for rr in (r0, r - 2)], .2, 'shell')
    # A few boulders on the floor.
    for k, (x, y, r) in enumerate(((-160, -95, 6), (150, -120, 5), (178, 30, 7), (-170, 90, 5.5))):
        lumpy('boulder', (x, y, ground_z(x, y) + r * .35), r, seed=31 + k, stretch=(1.1, 1, .7), seg=24, rings=12, role='detail')


def riser_and_fountain():
    top = Vector((0, 0, H + 24))
    with group('B'):
        # Riser head: pipe out of the apex ice, freeze valve, swivel nozzle.
        loft('riser pipe', [(0, 0, H - 6), (0, 0, H + 14)], 1.1, 20)
        cyl('freeze valve body', (0, 0, H + 2), 2.4, 6, 'structure', (0, 0, 1), 24)
        box('valve actuator', (0, -3.2, H + 5), (3.2, 2.4, 3.4), .5, 'detail')
        tube('valve drain line', [(0, 2.4, H + 3), (2, 5, H + 1), (3, 8, H - 6)], .35, 'cable')
        cyl('swivel collar', (0, 0, H + 14), 1.8, 3, 'detail', (0, 0, 1), 20)
        cyl('nozzle hub', (0, 0, H + 17), 2.4, 3.4, 'structure', (0, 0, 1), 24)
        for k in range(3):
            a = math.tau * k / 3 + .4
            d = Vector((math.cos(a), math.sin(a), 0))
            rod('nozzle arm', top + Vector((0, 0, -5.4)) + d * 1.8, top + Vector((0, 0, -4.4)) + d * 9, .45, 'structure')
            cyl('nozzle tip', top + Vector((0, 0, -4.4)) + d * 9, .7, 1.6, 'accent', tuple(d + Vector((0, 0, .5))), 12)
        rod('spray deflector stem', (0, 0, H + 20.4), (0, 0, H + 24), .35, 'detail')
        cyl('spray deflector', (0, 0, H + 24), 3.2, .5, 'detail', (0, 0, 1), 24)
        # Spray: a small crown of five short arcs; the droplets freeze as they fall.
        for k in range(5):
            a = math.tau * k / 5 + .4
            d = Vector((math.cos(a), math.sin(a), 0))
            pts = []
            for m in range(16):
                t = m / 15
                rr = 9 + 24 * t
                pts.append(Vector((rr * d.x, rr * d.y, H + 20 + 9 * t - 30 * t * t)))
            tube('spray arc', pts, .14, 'detail')
    mark('SPRAY FOUNTAIN', (0, -9, H + 17), 'RUNS ON COLD NIGHTS / FREEZES IN THE AIR')


def feed_pipe():
    """Pipe down the slope from the intake (60 m above, off the drawing) to the valve pit."""
    path = [(-138, 196), (-150, 140), (-158, 84), (-162, 30), (-160, -22), (-152, -58), (PIT.x - 24, PIT.y)]
    pts = [(x, y, ground_z(x, y) + 1.6) for x, y in path]
    tube('feed pipe', pts, 1.2, 'cable')
    for k in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[k], path[k + 1]
        for f in (.25, .75):
            x = x0 + (x1 - x0) * f; y = y0 + (y1 - y0) * f
            z = ground_z(x, y)
            rod('route marker', (x, y - 6, z), (x, y - 6, z + 9), .45, 'detail')
            box('marker plate', (x, y - 6.4, z + 8.4), (3, .6, 2), .2, 'accent')
    x, y = path[2]
    mark('FEED PIPE', (x, y, ground_z(x, y) + 2), 'FROM THE STREAM INTAKE, 60 m ABOVE / BURIED')
    # Valve pit at the foot of the cone: walls in four slabs, lid lifted aside.
    c = PIT
    with group('C'):
        for nm, dx, dy, sx, sy in (('pit wall near', 0, -9, 20, 2), ('pit wall', 0, 9, 20, 2), ('pit wall near', -9, 0, 2, 16), ('pit wall', 9, 0, 2, 16)):
            box(nm, (c.x + dx, c.y + dy, -3), (sx, sy, 14), .6)
        box('pit floor', (c.x, c.y, -9.6), (18, 18, 1.2), .4, 'detail')
        # Pipe in from uphill, isolation valve with wheel, drain-back valve, riser out.
        loft('pipe in', [(c.x - 24, c.y, 0), (c.x - 10, c.y, -4), (c.x - 5, c.y, -4)], 1.2, 16, 'cable')
        cyl('isolation valve', (c.x - 5, c.y, -4), 2.4, 5, 'structure', (1, 0, 0), 24)
        rod('valve stem', (c.x - 2.5, c.y, -1.6), (c.x - 2.5, c.y, 3), .35, 'detail')
        cyl('valve wheel', (c.x - 2.5, c.y, 3), 3.2, .6, 'accent', (0, 0, 1), 24)
        for k in range(4):
            a = math.tau * k / 4
            rod('wheel spoke', (c.x - 2.5, c.y, 3.3), (c.x - 2.5 + 3 * math.cos(a), c.y + 3 * math.sin(a), 3.3), .2, 'detail')
        loft('pit pipe', [(c.x, c.y, -4), (c.x + 4, c.y, -4)], 1.2, 16, 'structure')
        box('drain-back valve', (c.x + 5, c.y, -4), (4, 4, 4.4), .6, 'structure')
        loft('drain line', [(c.x + 5, c.y + 2, -6), (c.x + 5, c.y + 6, -8.4), (c.x + 5, c.y + 12, -9)], .5, 12, 'cable')
        cyl('pressure gauge', (c.x + 1, c.y - 2.2, -1.2), 1.6, 1, 'structure', (0, -1, 0), 24)
        rod('gauge needle', (c.x + 1, c.y - 3.4, -1.2), (c.x + 1.8, c.y - 3.4, -.3), .12, 'accent')
        loft('riser leg', [(c.x + 7, c.y, -4), (c.x + 9, c.y, -4), (c.x + 14, c.y + 4, 2)], 1.2, 16, 'structure')
        box('lifted pit lid', (c.x + 22, c.y + 4, 1.4), (20, 16, 1.2), .5, 'detail')
    uncover('C', 'pit wall near')
    # The riser continues under the ice from the pit to the apex (hidden).
    tube('riser under the ice', [(c.x + 14, c.y + 4, -2), (-60, -25, -2), (0, 0, 20), (0, 0, H - 6)], 1.1, 'cable')
    mark('VALVE PIT', (c.x + 22, c.y - 4, 2.5), 'DRAINS THE RISER WHEN THE SPRAY STOPS')


def terraces():
    """Three stone-walled barley terraces stepping down toward the viewer."""
    for k in range(3):
        rr = 124 + 24 * k
        a0, a1 = -2.25, -.85
        pts = []
        for m in range(41):
            a = a0 + (a1 - a0) * m / 40
            x, y = rr * math.cos(a), -10 + rr * math.sin(a)
            pts.append((x, y, ground_z(x, y) + 2.4))
        loft('terrace wall', pts, 2.4, 10)
        for f in (.33, .66):
            r2 = rr - 24 * f
            fp = []
            for m in range(31):
                a = a0 + .08 + (a1 - a0 - .16) * m / 30
                x, y = r2 * math.cos(a), -10 + r2 * math.sin(a)
                fp.append((x, y, ground_z(x, y) + .5))
            tube('furrow', fp, .2, 'shell')
    # Melt channel: from the gate at the cone foot straight down the terraces.
    ch = [(r * math.cos(-1.0), r * math.sin(-1.0)) for r in (116, 134, 152, 170, 184)]
    for dx in (-3, 3):
        tube('melt channel edge', [(x + dx, y, ground_z(x, y) + 1) for x, y in ch], .35, 'detail')
    box('channel gate', (ch[0][0], ch[0][1], ground_z(*ch[0]) + 3), (10, 4, 6), .8, 'accent')
    mark('MELT CHANNEL', (ch[3][0] + 4, ch[3][1], ground_z(*ch[3]) + 1), 'OPENED IN APRIL / GATE AT THE CONE FOOT')
    a = -2.1; x, y = 172 * math.cos(a), -10 + 172 * math.sin(a)
    mark('BARLEY TERRACES', (x, y, ground_z(x, y) + 4), '1 ha SOWN WHILE THE STREAMS ARE STILL FROZEN')


def prayer_flags():
    """One string from the riser to a pole on the terrace edge, as in Ladakh."""
    a = Vector((0, -3, H + 9)); pole = Vector((172, -10, 0))
    pole.z = ground_z(pole.x, pole.y)
    rod('flag pole', pole, pole + Vector((0, 0, 60)), 1.1, 'structure')
    b = pole + Vector((0, 0, 58))
    pts = []
    for k in range(41):
        t = k / 40
        p = a.lerp(b, t); p.z -= 38 * 4 * t * (1 - t)
        pts.append(p)
    tube('flag line', pts, .25, 'detail')
    for k in range(3, 38, 2):
        p = pts[k]; q = pts[k + 1]
        d = (q - p).normalized()
        g.mesh('prayer flag', [p, p + d * 3.2, p + d * 3.2 + Vector((0, 0, -4.2)), p + Vector((0, 0, -4.2))], [(0, 1, 2, 3)], 'detail')


def build():
    views(B=(-24, 6), C=(-30, 52))
    hx, hy = PIT.x - 14, PIT.y - 30
    human(p=(hx, hy, ground_z(hx, hy)), scale=.028, angle=-35)
    ground()
    cone()
    riser_and_fountain()
    feed_pipe()
    terraces()
    prayer_flags()
    a = math.pi * 1.2
    mark('ICE CONE', (cone_r(110, a) * math.cos(a), cone_r(110, a) * math.sin(a), 109), '30 m TALL / ABOUT 2.3 MILLION L OF WATER')
    return -20, 14
