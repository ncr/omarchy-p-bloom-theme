"""STELLARATOR HEARTH: five-period stellarator power plant, cut open.

Units: 1 unit = 5 cm. Major radius R0 = 240 (12 m). The magnetic axis is
helical: R = R0 + D cos(N phi), Z = D sin(N phi), N = 5 field periods.
Plasma section: an ellipse (half-axes 38 x 18 units = 1.9 x 0.9 m) that
turns half a revolution per period (angle N phi / 2), the classic
rotating-ellipse stellarator. Fifty non-planar modular coils (ten per
period) sit on a winding surface 22 units outside the plasma and wobble
toroidally with the section angle, so every coil is twisted.
Plasma vessel: ten half-module shells (one per half period) with the front
sector removed; there the plasma boundary and three field lines show.
Cryostat: a torus shell of section radius 90 over the back half, in
30-degree segments with bolted joint rings, radial ports. A service
platform with railing runs outside the front; the standing person is
1.75 m = 35 units.
"""
from ..kit import *
from .parts import loft, sphere
from ..humans import human

N = 5
R0 = 240
D = 16
A1, A2 = 38, 18
GAP = 22
CUT = (250, 306)         # degrees: vessel removed, plasma shown (front)
OPEN = (262, 296)        # degrees: coils removed as well (the cutaway)
CRYO = (20, 160)         # degrees: cryostat shell present (back)
COILS = 50
KB = 34                  # the coil opened for view B (front-right, beside the cut)


def axis(phi):
    return Vector(((R0 + D * math.cos(N * phi)) * math.cos(phi), (R0 + D * math.cos(N * phi)) * math.sin(phi), D * math.sin(N * phi)))


def section(phi, theta, grow=0.0):
    """Point on the rotating-ellipse surface grown outward by `grow` units."""
    al = N * phi / 2
    u = (A1 + grow) * math.cos(theta); v = (A2 + grow) * math.sin(theta)
    dr = u * math.cos(al) - v * math.sin(al); dz = u * math.sin(al) + v * math.cos(al)
    er = Vector((math.cos(phi), math.sin(phi), 0))
    return axis(phi) + er * dr + Vector((0, 0, dz))


def surface(name, phi0, phi1, grow, role, nphi=None, nth=72):
    nphi = nphi or max(8, int(abs(phi1 - phi0) / math.radians(1.5)))
    vs = []; fs = []
    for i in range(nphi + 1):
        phi = phi0 + (phi1 - phi0) * i / nphi
        for j in range(nth):
            vs.append(section(phi, T * j / nth, grow))
    for i in range(nphi):
        for j in range(nth):
            a = i * nth + j; b = i * nth + (j + 1) % nth
            fs.append((a, b, b + nth, a + nth))
    return g.mesh(name, vs, fs, role)


def coil_curve(phi_k, theta, grow):
    """Non-planar coil centreline: toroidal wobble follows the section angle."""
    al = N * phi_k / 2
    wob = .045 * math.sin(theta - al) + .018 * math.sin(2 * theta)
    return section(phi_k + wob, theta, grow)


def ribbon(name, phi_k, grow=GAP, w=15.0, h=10.0, role='structure', th0=0, th1=T, n=120):
    """Closed (or partial) rectangular-section coil following coil_curve."""
    full = th1 - th0 >= T - 1e-6
    count = n if full else n + 1
    vs = []; fs = []
    for k in range(count):
        th = th0 + (th1 - th0) * k / n
        c = coil_curve(phi_k, th, grow)
        c2 = coil_curve(phi_k, th + 1e-3, grow)
        tang = (c2 - c).normalized()
        out = (c - section(phi_k, th, 0)).normalized()
        tor = tang.cross(out).normalized()
        out = tor.cross(tang).normalized()
        for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            vs.append(c + tor * (a * w / 2) + out * (b * h / 2))
    for k in range(count if full else count - 1):
        k2 = (k + 1) % count
        for q in range(4):
            fs.append((k * 4 + q, k * 4 + (q + 1) % 4, k2 * 4 + (q + 1) % 4, k2 * 4 + q))
    if not full:
        fs.append((0, 1, 2, 3)); fs.append(((count - 1) * 4 + 3, (count - 1) * 4 + 2, (count - 1) * 4 + 1, (count - 1) * 4))
    return g.mesh(name, vs, fs, role)


def torus_segment(name, phi0, phi1, r_sec, role='structure', n_sec=64, z=0):
    nphi = max(6, int((phi1 - phi0) / math.radians(2)))
    vs = []; fs = []
    for i in range(nphi + 1):
        phi = phi0 + (phi1 - phi0) * i / nphi
        er = Vector((math.cos(phi), math.sin(phi), 0))
        for j in range(n_sec):
            t = T * j / n_sec
            vs.append(er * (R0 + r_sec * math.cos(t)) + Vector((0, 0, z + r_sec * math.sin(t))))
    for i in range(nphi):
        for j in range(n_sec):
            a = i * n_sec + j; b = i * n_sec + (j + 1) % n_sec
            fs.append((a, b, b + n_sec, a + n_sec))
    return g.mesh(name, vs, fs, role)


def theta_bottom(phi, grow=7):
    best = None
    for j in range(360):
        th = T * j / 360
        z = section(phi, th, grow).z
        if best is None or z < best[0]:
            best = (z, th)
    return best[1]


def trough(name, phi0, phi1, grow, role, half=math.radians(96), nth=48):
    """Lower half of the vessel: an open trough under the plasma in the cutaway."""
    nphi = max(8, int(abs(phi1 - phi0) / math.radians(1.5)))
    vs = []; fs = []
    for i in range(nphi + 1):
        phi = phi0 + (phi1 - phi0) * i / nphi
        tb = theta_bottom(phi, grow)
        for j in range(nth + 1):
            vs.append(section(phi, tb - half + 2 * half * j / nth, grow))
    for i in range(nphi):
        for j in range(nth):
            a = i * (nth + 1) + j
            fs.append((a, a + 1, a + nth + 2, a + nth + 1))
    return g.mesh(name, vs, fs, role)


def in_range(deg, rng):
    d = (deg - rng[0]) % 360
    return d <= (rng[1] - rng[0]) % 360


def divertor_cassette(phi_deg):
    """Monoblock divertor module on the lower inboard wall of the cut sector."""
    phi = math.radians(phi_deg)
    th = theta_bottom(phi)
    base = section(phi, th, 6.2)
    out = (section(phi, th, 0) - base).normalized()      # heat face toward the plasma
    tor = Vector((-math.sin(phi), math.cos(phi), 0))
    along = tor.cross(out).normalized()
    m = Matrix((along, tor, out)).transposed().to_4x4(); m.translation = base
    b = len(g.parts); w = len(g.wires)
    box('divertor base plate', (0, 0, -1.2), (16, 26, 1.6), .5)
    for j in range(8):
        for i in range(3):
            # an open gap on every side and a hair above the plate, so each block keeps a closed
            # outline and neighbouring rounded corners never merge into forks
            box('tungsten monoblock', (-5 + i * 5, -10.5 + j * 3, .75), (4.2, 2.2, 2.2), .25, 'structure')
    for i in range(3):
        cyl('monoblock cooling tube', (-5 + i * 5, -14.6, .6), .7, 29.2, 'accent', (0, 1, 0), 16)
    for y in (-15.2, 15.2):
        box('water manifold', (0, y, -.2), (17, 2.2, 3.2), .6)
    transform(b, w, m)
    return base


def build():
    # The person first: the mannequin builder resets the scene.
    human(p=(40, -(R0 + 78), -104), scale=.056, angle=4)
    # --- plasma (cut sector) with three field lines ---------------------------
    c0, c1 = (math.radians(v) for v in (CUT[0] - 4, CUT[1] - 16))
    surface('plasma boundary', c0, c1, 0, 'accent', nth=64)
    for k, th0 in enumerate((0.4, 2.5, 4.6)):
        pts = []
        for i in range(160):
            phi = c0 + (c1 - c0) * i / 159
            # Rotational transform ~0.9 per turn: the line winds around the section.
            th = th0 + (phi - c0) * .9 * 5 / 2
            pts.append(section(phi, th, .35))
        tube('field line', pts, .12, 'accent')
    # --- plasma vessel in half-module shells, open over the cut ---------------
    for m_ in range(10):
        a0 = -8 + m_ * 36; a1 = a0 + 36
        for s0, s1 in ((a0, min(a1, CUT[0])), (max(a0, CUT[1]), a1)):
            if s1 - s0 > .5:
                surface('plasma vessel shell', math.radians(s0), math.radians(s1), 7, 'shell', nth=64)
    trough('plasma vessel floor', math.radians(CUT[0]), math.radians(CUT[1]), 7, 'shell')
    # --- fifty modular coils ----------------------------------------------------
    for k in range(COILS):
        deg = -8 + 360 * (k + .5) / COILS
        if in_range(deg % 360, (CRYO[0] + 6, CRYO[1] - 6)) or in_range(deg % 360, OPEN) or k == KB:
            continue
        ribbon('non-planar coil', math.radians(deg))
    # --- B: one coil opened to its winding pack ----------------------------------
    with group('B'):
        phB = math.radians(-8 + 360 * (KB + .5) / COILS)
        ribbon('coil casing', phB, th0=math.radians(40), th1=math.radians(330), w=15.4, h=10.4)
        for i, dh in enumerate((-3.6, -1.2, 1.2, 3.6)):
            ribbon('winding pack turn layer', phB, grow=GAP + dh, w=13.0, h=1.9, role='accent' if i % 2 else 'detail',
                   th0=math.radians(-40), th1=math.radians(52), n=40)
        for sgn in (-1, 1):
            pts = [coil_curve(phB, th, GAP) + (coil_curve(phB, th, GAP) - section(phB, th, 0)).normalized() * 6.8
                   + Vector((-math.sin(phB), math.cos(phB), 0)) * (sgn * 4.5)
                   for th in [math.radians(40 + 290 * i / 60) for i in range(61)]]
            tube('helium cooling line', pts, .5, 'cable')
        for th in (80, 150, 220, 290):
            q = coil_curve(phB, math.radians(th), GAP)
            out = (q - section(phB, math.radians(th), 0)).normalized()
            box('coil support lug', q + out * 8.5, (6, 6, 6), 1.2, 'detail')
        mark('TWISTED COILS', coil_curve(phB, math.radians(100), GAP + 5), 'FIFTY SHAPES / NO TWO NEIGHBOURS ALIKE')
    # --- C: divertor module in the open sector -----------------------------------
    with group('C'):
        divertor_cassette(CUT[1] - 7)
    # --- cryostat over the back half, in segments with joint rings ----------------
    RC = 92
    for s0 in range(CRYO[0], CRYO[1], 30):
        s1 = min(CRYO[1], s0 + 30)
        torus_segment('cryostat shell', math.radians(s0), math.radians(s1), RC, 'structure')
        phi = math.radians(s0)
        er = Vector((math.cos(phi), math.sin(phi), 0))
        pts = [er * (R0 + (RC + 1.2) * math.cos(T * j / 96)) + Vector((0, 0, (RC + 1.2) * math.sin(T * j / 96))) for j in range(97)]
        tube('cryostat joint ring', pts, .8, 'detail')
    # Radial ports with flanges on the cryostat.
    for deg in (38, 74, 110, 146):
        phi = math.radians(deg); er = Vector((math.cos(phi), math.sin(phi), 0))
        cyl('radial port', er * (R0 + RC - 6), 11, 40, 'structure', tuple(er))
        flange('port flange', er * (R0 + RC + 34), 13, tuple(er), 3)
    for deg in (56, 128):
        phi = math.radians(deg); er = Vector((math.cos(phi), math.sin(phi), 0))
        cyl('vertical port', er * R0 + Vector((0, 0, RC - 8)), 9, 34, 'structure', (0, 0, 1))
        flange('top flange', er * R0 + Vector((0, 0, RC + 26)), 11, (0, 0, 1), 3)
    # --- plinth, coil cradles, front walkway ----------------------------------------
    PZ = -104
    ring('machine plinth', (0, 0, PZ - 18), R0 + 96, 200, 18, (0, 0, 1))
    ring('plinth edge', (0, 0, PZ - .8), R0 + 94, 2, 1.2, (0, 0, 1), 'detail')
    for deg in range(0, 360, 36):
        phi = math.radians(deg); er = Vector((math.cos(phi), math.sin(phi), 0))
        if in_range(deg % 360, CRYO):
            box('cryostat saddle', er * R0 + Vector((0, 0, PZ + 7)), (46, 28, 16), 3)
            continue
        low = section(phi, theta_bottom(phi, GAP + 6), GAP + 6)
        box('coil cradle', Vector((low.x, low.y, (PZ + low.z) / 2)), (24, 24, low.z - PZ), 3)
    # Walkway on the plinth in front: railing on the outer edge, person for scale.
    pr = R0 + 90
    for zz in (PZ + 19, PZ + 38):
        tube('walkway rail', [(pr * math.cos(math.radians(d)), pr * math.sin(math.radians(d)), zz) for d in range(232, 309, 2)], .5, 'detail')
    for deg in range(232, 309, 6):
        phi = math.radians(deg)
        rod('railing post', (pr * math.cos(phi), pr * math.sin(phi), PZ), (pr * math.cos(phi), pr * math.sin(phi), PZ + 38), .5, 'detail')
    # --- annotations ---------------------------------------------------------------
    mark('PLASMA', section(math.radians(272), math.radians(60), 0), '3.8 × 1.8 m SECTION / THREE FIELD LINES SHOWN')
    mark('CRYOSTAT', Vector((math.cos(math.radians(30)), math.sin(math.radians(30)), 0)) * (R0 + RC * .75) + Vector((0, 0, RC * .66)), 'VACUUM JACKET / 30° SEGMENTS / RADIAL PORTS')
    mark('SERVICE WALKWAY', (40, -(R0 + 78), -104 + 36), 'PERSON FOR SCALE / 1.75 m')
    phc = math.radians(252); lowc = section(phc, theta_bottom(phc, GAP + 6), GAP + 6)
    mark('COIL CRADLE', Vector((lowc.x, lowc.y, (-104 + lowc.z) / 2)) + Vector((math.cos(phc), math.sin(phc), 0)) * 12, 'TEN CRADLES / 2 000 t OF COLD MAGNETS')
    ph_v = math.radians(CUT[0] + 8)
    mark('PLASMA VESSEL', section(ph_v, theta_bottom(ph_v) - math.radians(60), 7), 'TEN HALF-MODULES / BOLTED JOINTS')
    views(B=(-120, 30), C=(80, 35))
    return 18, 36
