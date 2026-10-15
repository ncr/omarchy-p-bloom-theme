"""FOG HARP: three standing wire harps on a coastal ridge, a cistern below.

Scale: 1 unit = 1 cm. X runs along the ridge, +Y toward the sea (the fog
comes from +Y), Z up. The crest bends gently away from the viewer; the
three panels are staggered along it but all face the same prevailing wind.

Harp: wire field 4 m wide under an S-curved neck that falls from a tall
pillar (7.8 / 7.3 / 6.8 m) to a 3.8 m post, so the wires step down in
length like harp strings. Mean wire height ~4.6 m -> 19.4 + 18.6 + 17.7
= 56 m2 of wire field. A U-gutter under the bottom tension bar, a bolted
spacing comb at 2.4 m, windward stays only. Real wires: 0.4 mm stainless
at 3.2 mm pitch -> 1 250 per harp; drawn one in 16 (every 5 cm).
Droplets drawn about twice real size. Each gutter drains at its east
end through a leaf screen and filter can; a collector runs down the lee
slope to a 16 m3 cistern (3.2 m across, 2 m deep) with a tap.
"""
from ..kit import *
from .parts import loft, sphere, arc_tube, lumpy
from ..humans import human

W = 200            # half width of the wire field
Z0, Z1 = 86, 566   # bottom tension bar, head beam (at the posts)
ARCH = 44          # head beam rise at mid-span
PANELS = (-470, 0, 470)
CIST = Vector((-520, -440, 0))


def crest_y(x):
    return .0006 * x * x


def ground_z(x, y):
    d = y - crest_y(x)
    if d >= 0:
        return -.55 * d
    d = -d
    return -.2 * d - .00011 * d * d


HS = 380           # short (east) post height of every harp
HEIGHTS = (780, 730, 680)   # tall pillar of each harp, stepping down the crest


def head_z(u, ht=660):
    """Harp neck: tall pillar (u=-1) down an S-curve to the short post (u=1)."""
    t = (u + 1) / 2
    return HS + (ht - HS) * (1 - t) ** 1.35 + 38 * math.sin(math.pi * t) ** 1.5


def trough(name, x0, x1, y, z, w=9, depth=9, t=.9, role='structure'):
    """U-gutter along x: a real profile (lips, floor), closed ends."""
    prof = []
    n = 12
    for k in range(n + 1):
        a = math.pi * k / n
        prof.append((-w * math.cos(a), -depth * math.sin(a)))
    inner = [(px * (w - t) / w, py * (depth - t) / depth) for px, py in prof]
    sec = prof + inner[::-1]
    vs = []; fs = []; m = len(sec)
    for x in (x0, x1):
        for py, pz in sec:
            vs.append((x, y + py, z + pz))
    for k in range(m):
        fs.append((k, (k + 1) % m, m + (k + 1) % m, m + k))
    fs.append(tuple(range(m))); fs.append(tuple(m + k for k in reversed(range(m))))
    return g.mesh(name, vs, fs, role)


def panel(cx, ht=660, b_patch=False, c_end=False):
    """One harp. b_patch: wires/comb around x in [cx-40, cx+40] go to group B.
    c_end: the gutter end section, outlet and filter can go to group C."""
    cy = crest_y(cx); base = ground_z(cx, cy)
    # Tall pillar (west) and short post (east): tapered lofts, cast feet.
    for s_ in (-1, 1):
        px = cx + s_ * (W + 12)
        top = head_z(s_, ht)
        r0, r1 = (13, 8) if s_ < 0 else (9, 6.5)
        loft('harp pillar' if s_ < 0 else 'harp post', [(px, cy, base - 6), (px, cy, base + top * .5), (px, cy, base + top + 10)],
             lambda t, r0=r0, r1=r1: r0 - (r0 - r1) * t, 22)
        box('post foot', (px, cy, base - 2), (2.8 * r0 + 6, 2.8 * r0 + 6, 12), 4)
        # Windward stays only: the fog wind pushes the harp toward the lee.
        a = Vector((px + s_ * 40, cy + 360, ground_z(px + s_ * 40, cy + 360) + 6))
        t_ = Vector((px, cy, base + top))
        tube('windward stay', [t_, a], .35, 'detail')
        box('stay anchor', a + Vector((0, 0, -4)), (18, 18, 8), 2, 'detail')
    # Pillar crown: a turned finial, the harp's visual anchor.
    px = cx - W - 12; tz = base + head_z(-1, ht) + 10
    ring('pillar collar', (px, cy, tz - 4), 10.5, 3, 4, (0, 0, 1), 'detail')
    sphere('pillar finial', (px, cy, tz + 9), 10, 'structure', 28, 14, (1, 1, 1.25))
    sphere('post cap', (cx + W + 12, cy, base + HS + 18), 7, 'structure', 24, 12)
    # Neck in three bolted segments (tapering 7.5 -> 5 cm radius).
    cuts = (-1, -1 / 3, 1 / 3, 1)
    for j in range(3):
        us = [cuts[j] + (cuts[j + 1] - cuts[j]) * k / 14 for k in range(15)]
        pts = [(cx + (W + 12) * u, cy, base + head_z(u, ht)) for u in us]
        r0 = 7.5 - 2.5 * (cuts[j] + 1) / 2; r1 = 7.5 - 2.5 * (cuts[j + 1] + 1) / 2
        with (group('B') if b_patch and j == 1 else _null()):
            loft('harp neck', pts, lambda t, r0=r0, r1=r1: r0 + (r1 - r0) * t, 18, 'structure', False)
            for uj in (cuts[j], cuts[j + 1]):
                if -1 < uj < 1:
                    rr = 7.5 - 2.5 * (uj + 1) / 2
                    ring('neck joint band', (cx + (W + 12) * uj - 1.5, cy, base + head_z(uj, ht)), rr + 1.2, 1.4, 3, (1, 0, 0), 'detail')
    rod('bottom tension bar', (cx - W - 12, cy, base + Z0), (cx + W + 12, cy, base + Z0), 2.6)
    for s in (-1, 1):
        cyl('bar tensioner', (cx + s * (W + 4), cy, base + Z0 - 5), 2.2, 10, 'detail', (0, 0, 1), 16)
    # Spacing comb: bolted segments of 80 cm, two flat bars clamping the wires.
    zc = base + 240
    for k in range(5):
        x0 = cx - W + k * 80; x1 = x0 + 80
        with _null():
            for dy in (-1.6, 1.6):
                box('comb segment', ((x0 + x1) / 2, cy + dy, zc), (78, 1.6, 4), .5, 'detail')
            for xb in range(int(x0) + 5, int(x1), 10):
                cyl('comb bolt', (xb, cy - 2.4, zc), .7, 4.8, 'detail', (0, 1, 0), 8)
    # Gutter in sections, falling 1 % to its east end; end section joins the outlet.
    gz0 = base + Z0 - 12
    trough('drip gutter', cx - W - 8, cx + W - 60, cy, gz0, 9, 9)
    with (group('C') if c_end else _null()):
        trough('gutter end section', cx + W - 60, cx + W + 22, cy, gz0 - .6, 9, 9)
        box('gutter joint strap', (cx + W - 60, cy, gz0 - 9.6), (4, 18.4, .8), .3, 'detail')
        rod('bottom tension bar end', (cx + W - 58, cy, base + Z0), (cx + W + 12, cy, base + Z0), 2.7, 'detail')
        ox = cx + W + 14
        oz = base + Z0 - 21.6
        cyl('gutter outlet', (ox, cy, oz - 6), 3.2, 7, 'structure', (0, 0, 1), 20)
        box('leaf screen', (ox, cy, gz0 - .4), (12, 17, .8), .3, 'accent')
        for xx in range(-5, 6, 2):
            rod('screen bar', (ox + xx, cy - 8, gz0), (ox + xx, cy + 8, gz0), .25, 'detail')
        cyl('filter can', (ox, cy, oz - 30), 7, 22, 'structure', (0, 0, 1), 28)
        ring('filter can lid', (ox, cy, oz - 9.5), 7.6, 1.2, 2.2, (0, 0, 1), 'detail')
        for zz in (-24, -16):
            ring('filter can band', (ox, cy, oz + zz), 7.4, .8, 1.2, (0, 0, 1), 'detail')
        box('can clamp handle', (ox, cy - 8.4, oz - 20), (3, 2, 10), .6, 'detail')
        loft('drop pipe', [(ox, cy, oz - 30), (ox, cy, base + 14), (ox, cy - 12, base + 6), (ox, cy - 24, base + 5)], 2.4, 14, 'structure')
        for s in (-1, 1):
            rod('gutter hanger', (cx + W - 30, cy + s * 9.4, base + Z0 + 1), (cx + W - 30, cy + s * 9.4, gz0 - 8), .8, 'detail')
    rod('gutter hanger', (cx - W + 30, cy - 9.4, base + Z0 + 1), (cx - W + 30, cy - 9.4, gz0 - 8), .8, 'detail')
    rod('gutter hanger', (cx - W + 30, cy + 9.4, base + Z0 + 1), (cx - W + 30, cy + 9.4, gz0 - 8), .8, 'detail')
    # Wires: drawn one in 16. Crimp sleeves at the bar; droplets bead and grow.
    n = 81
    for i in range(n):
        u = -1 + 2 * (i + .5) / n
        x = cx + W * u
        ztop = base + head_z(u * W / (W + 12), ht)
        cyl('crimp sleeve', (x, cy, base + Z0 + 2.4), .55, 4, 'detail', (0, 0, 1), 8)
        inb = b_patch and abs(u * W / (W + 12)) < 1 / 3 - .02
        # Every wire carries the same beading: small drops that grow as they
        # run down (positions from a fixed hash, not a visible pattern).
        def beads(z0, z1):
            out = []
            for k in range(int((z1 - z0) / 26)):
                hsh = math.sin(i * 12.9898 + k * 78.233 + cx * .017) * 43758.5453
                f = hsh - math.floor(hsh)
                if f < .38:
                    zz = z0 + (k + f) * 26
                    frac = (zz - (base + Z0)) / (ztop - base - Z0)
                    out.append((zz, .3 + .3 * (1 - frac) + (.3 if f < .05 else 0)))
            return out
        zt = ztop - 1.5            # wire ends at its pin through the neck
        zb = zt - 130              # B holds the top 1.3 m of its wires
        tube('harp wire', [(x, cy, base + Z0 + 2.6), (x, cy, zb)], .12, 'shell')
        for zz, r in beads(base + Z0 + 8, zb):
            sphere('droplet', (x, cy - .2, zz), r, 'accent', 10, 5)
        with (group('B') if inb else _null()):
            tube('harp wire', [(x, cy, zb), (x, cy, zt)], .12, 'shell')
            for zz, r in beads(zb, zt - 16):
                sphere('droplet', (x, cy - .2, zz), r, 'accent', 12, 6)
            # Tensioning pin through the neck, peg head on the lee side.
            cyl('tension pin', (x, cy + 5, zt), .75, 12, 'detail', (0, -1, 0), 10)
            box('pin head', (x, cy - 8.2, zt), (1.8, 1.6, 3.4), .4, 'detail')
    return cx + W + 14, cy, base


from contextlib import contextmanager


@contextmanager
def _null():
    yield


def ground():
    xs = [-1100 + 2200 * i / 60 for i in range(61)]
    ys = [-1100 + 1500 * j / 50 for j in range(51)]
    vs = [(x, y, ground_z(x, y)) for x in xs for y in ys]
    m = len(ys); fs = []
    for i in range(len(xs) - 1):
        for j in range(m - 1):
            a = i * m + j
            fs.append((a, a + m, a + m + 1, a + 1))
    # Occluder only: the exporter draws no edges of 'tube'-role meshes.
    g.mesh('ridge ground', vs, fs, 'tube')
    tube('ridge crest', [(x, crest_y(x), ground_z(x, crest_y(x)) + .5) for x in range(-760, 761, 20)], .3, 'structure')
    # Lee-slope contours, 1 m apart: inverse of the declared profile.
    for dz, span in ((-60, 700), (-130, 560), (-210, 420)):
        pts = []
        for x in range(-span, span + 1, 20):
            d = 0
            while -.2 * d - .00011 * d * d > dz:
                d += 2
            pts.append((x, crest_y(x) - d, dz + .4))
        tube('lee contour', pts, .2, 'shell')
    for dz in (-100,):
        pts = [(x, crest_y(x) + 100 / .55, dz + .4) for x in range(-640, 641, 20)]
        tube('seaward contour', pts, .2, 'shell')
    # Fall-line hachures under the crest.
    for x in range(-700, 701, 70):
        y0 = crest_y(x)
        tube('slope hachure', [(x, y0 - 8, ground_z(x, y0 - 8) + .4), (x, y0 - 120, ground_z(x, y0 - 120) + .4)], .15, 'shell')


def build():
    views(B=(-28, -14), C=(-40, 20))
    hx, hy = CIST.x + 190, CIST.y - 150
    human(p=(hx, hy, ground_z(hx, hy)), scale=.28, angle=-50)
    ground()
    outs = [panel(cx, HEIGHTS[k], b_patch=(k == 0), c_end=(k == 2)) for k, cx in enumerate(PANELS)]
    # Collector along the lee foot of the panels, then down to the cistern.
    col = []
    for ox, oy, oz in outs:
        col.append((ox, oy - 24, ground_z(ox, oy - 24) + 5))
    tube('collector pipe', col, 2.2, 'cable')
    path = [(outs[1][0], outs[1][1] - 24), (180, -150), (-120, -300), (CIST.x + 150, CIST.y + 30)]
    tube('main pipe', [(x, y, ground_z(x, y) + 5) for x, y in path], 2.4, 'cable')
    cistern()
    # Fog drifting in from the sea (implied, declared in the callout).
    for k, (z, y, x0, x1) in enumerate(((380, 260, -760, 100), (470, 330, -300, 700), (300, 420, -700, 600), (620, 480, -760, -100))):
        tube('fog drift line', [(x, y + 18 * math.sin(x / 140 + k), z + 10 * math.sin(x / 210 + 2 * k)) for x in range(x0, x1 + 1, 25)], .3, 'shell')
    cx = PANELS[0]; cy = crest_y(cx); b = ground_z(cx, cy)
    mark('WIRE HARP', (cx - 170, cy - 1, b + 470), '1 250 WIRES A HARP / DRAWN 1 IN 16')
    cx = PANELS[2]; cy = crest_y(cx); b = ground_z(cx, cy)
    mark('HARP NECK', (cx + 150, cy, b + head_z(150 / (W + 12), HEIGHTS[2]) + 6), 'SHORTER WIRES DOWNWIND / SAME TENSION')
    mark('FOG FROM THE SEA', (700, 330 + 18 * math.sin(700 / 140 + 1), 470 + 10 * math.sin(700 / 210 + 2)), 'GREY MORNINGS / 6 h ON A GOOD DAY')
    ox, oy, ob = outs[2]
    mark('GUTTER OUTLET', (ox, oy - 7, ob + Z0 - 45), 'LEAF SCREEN / FILTER CAN / 1 % FALL')
    mark('VILLAGE CISTERN', (CIST.x - 110, CIST.y - 100, ground_z(CIST.x - 110, CIST.y - 100) + 80), '16 000 L / SIXTY FOGGY MORNINGS')
    mark('HUMAN / MARISOL', (hx + 4, hy - 10, ground_z(hx, hy) + 45), 'FILLS THE FIRST JERRYCAN AT SEVEN')
    return -22, 14


def cistern():
    c = CIST; gz = ground_z(c.x, c.y)
    cyl('cistern wall', (c.x, c.y, gz - 10), 160, 70, 'structure', (0, 0, 1), 96)
    ring('cistern coping', (c.x, c.y, gz + 60), 164, 10, 6, (0, 0, 1), 'detail')
    loft('cistern lid', [(c.x, c.y, gz + 66), (c.x, c.y, gz + 88)], lambda t: 158 * math.cos(t * 1.25) ** .5 + 1, 64, 'structure', False)
    box('inspection hatch', (c.x + 40, c.y - 30, gz + 86), (46, 46, 6), 3, 'detail')
    cyl('air vent', (c.x - 50, c.y + 20, gz + 84), 4, 22, 'detail', (0, 0, 1), 16)
    sphere('vent cowl', (c.x - 50, c.y + 20, gz + 108), 6, 'detail', 16, 8)
    # Tap post on the lee side and a jerrycan under the spout.
    tx, ty = c.x + 120, c.y - 120
    tz = ground_z(tx, ty)
    loft('tap supply', [(c.x + 100, c.y - 100, gz + 8), (tx, ty, tz + 8), (tx, ty, tz + 90)], 2.2, 12, 'structure')
    box('tap plinth', (tx, ty, tz + 4), (40, 40, 10), 3)
    loft('tap spout', [(tx, ty, tz + 90), (tx + 10, ty - 10, tz + 92), (tx + 16, ty - 16, tz + 84)], 1.6, 12, 'structure')
    cyl('tap handle', (tx, ty, tz + 94), 4.5, 1.6, 'accent', (0, 0, 1), 20)
    box('jerrycan', (tx + 18, ty - 18, tz + 24), (34, 18, 40), 4)
    box('jerrycan grip', (tx + 18, ty - 18, tz + 48), (14, 5, 6), 1.5, 'detail')
