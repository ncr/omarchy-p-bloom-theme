"""FEELING HAND: sensory prosthetic hand, wrist and short socket.

Authored in millimetres, exported at 1 unit = 0.5 mm. Built in a palm frame (distal +Y, dorsal +Z, thumb on
-X: a right hand), then posed with the palm turned up and toward the viewer,
fingers in a relaxed open cradle, thumb opposed with a 55-60 mm opening,
the width of a small child's hand.

Adult proportions: knuckle width 84 mm, wrist to middle fingertip 185 mm.
Phalanges (mm) index 42/25/19 (1 : 0.6 : 0.45), middle 46/29/20,
ring 43/27/19, little 34/21/17; thumb 44 (metacarpal) / 32 / 25.
Flexion MCP 22-34, PIP 32-44, DIP 16-20 degrees; fingers fanned 7 to -12.

A shows the external device only: hand, wrist rotator, a short socket
ending in a section cut, and the abutment stub. The fingertip section (B)
and the implanted nerve interface (C) are separate parts of the same model,
exported only in their own views.
"""
from ..kit import *
from ..kit import profile_at
from .parts import capsule_segment, loft, sphere, arc_tube
from mathutils import Matrix as M

E = .72
FINGERS = {
    #          MCP (palm frame)    spread  lengths        radii              flexion MCP, PIP, DIP
    'index':  ((-26, 96, 1), 7, (42, 25, 19), (9.2, 8.4, 7.6), (22, 32, 16)),
    'middle': ((-8, 101, 2), 1, (46, 29, 20), (9.6, 8.8, 7.9), (26, 36, 17)),
    'ring':   ((10, 98, 1), -5, (43, 27, 19), (9.1, 8.3, 7.5), (30, 40, 18)),
    'little': ((26, 89, -1), -12, (34, 21, 17), (8.1, 7.4, 6.8), (34, 44, 20)),
}
THUMB = [(-22, 18, -10), (-47, 47, -28), (-55, 74, -42), (-51, 94, -52)]
THUMB_R = (13.5, 11, 9.6)
PALM = [(-6, 27, 14, 0), (10, 31, 15, 0), (45, 38, 15.5, -1), (80, 42, 14.5, 0), (95, 41, 12, 1), (103, 36, 8.5, 2), (106, 29, 5, 2)]
SOCKET = [(-22, 26.5, 24.5, 0), (-46, 29, 26.5, 0), (-70, 31, 28, 0)]
PALMAR = (0, -.55, .83)          # palm faces up and toward the viewer
REACH = (1, 0, .45)              # wrist-to-fingers direction in the world
PROBE = None
SCALE = 2.0                      # export units: 1 unit = 0.5 mm


def sec_pt(sections, y, ang, off=0, exp=E):
    rx, rz, lift = profile_at(sections, y)
    c, s_ = math.cos(ang), math.sin(ang)
    return Vector((rx * math.copysign(abs(c) ** exp, c) + off * c, y, lift + rz * math.copysign(abs(s_) ** exp, s_) + off * s_))


def chain(mcp, spread, lengths, flex):
    rs = M.Rotation(math.radians(spread), 3, 'Z')
    pts = [Vector(mcp)]; frames = []; phi = 0
    for L, f in zip(lengths, flex):
        phi += f
        rx = M.Rotation(math.radians(-phi), 3, 'X')
        frames.append((rs @ rx @ Vector((0, 1, 0)), rs @ rx @ Vector((0, 0, 1)), rs @ Vector((1, 0, 0))))
        pts.append(pts[-1] + frames[-1][0] * L)
    return pts, frames


def palm_inside(p):
    """Is a palm-frame point inside the palm hull (superellipse loft along Y)?"""
    if not (PALM[0][0] < p.y < PALM[-1][0]):
        return False
    rx, rz, lift = profile_at(PALM, p.y)
    return abs(p.x / rx) ** (2 / E) + abs((p.z - lift) / rz) ** (2 / E) < 1


def sweep(name, joints, radii, u_axis, flat=.86, n_ang=64, steps=16, dome_rings=10):
    """One continuous shell along a smooth centreline through the joints.

    A single mesh per finger: no overlapping segments, so the contour stays
    continuous around every bend. Radius follows the per-segment radii with a
    slight bulge at each joint; the tip closes with a real rounded dome.
    Returns (rings, centreline, frames) for seams, pins and junction curves.
    """
    from bio_details_build import curve as spline
    P = [Vector(p) for p in joints]
    cl = [Vector(p) for p in spline(P, steps)]
    seg_len = [(P[i + 1] - P[i]).length for i in range(len(P) - 1)]
    cum = [0]
    for L in seg_len:
        cum.append(cum[-1] + L)
    s_acc = [0]
    for i in range(1, len(cl)):
        s_acc.append(s_acc[-1] + (cl[i] - cl[i - 1]).length)
    total = s_acc[-1]; scale = cum[-1] / total

    def radius(sv):
        s_ = sv * scale
        for i in range(len(seg_len)):
            if s_ <= cum[i + 1] or i == len(seg_len) - 1:
                t = min(1, max(0, (s_ - cum[i]) / seg_len[i]))
                r = radii[i] + (radii[i + 1] - radii[i]) * t
                break
        for cj in cum[1:-1]:
            r += .35 * math.exp(-((s_ - cj) / 3.2) ** 2)
        return r
    u = Vector(u_axis).normalized()
    rings = []; frames = []
    for i, c in enumerate(cl):
        d = (cl[min(i + 1, len(cl) - 1)] - cl[max(i - 1, 0)]).normalized()
        uu = (u - d * u.dot(d)).normalized(); vv = uu.cross(d)
        r = radius(s_acc[i])
        rings.append([c + r * (math.cos(T * j / n_ang) * uu + flat * math.sin(T * j / n_ang) * vv) for j in range(n_ang)])
        frames.append((c, d, uu, vv, r))
    c, d, uu, vv, r = frames[-1]
    for k in range(1, dome_rings):
        th = (math.pi / 2) * k / dome_rings
        rings.append([c + d * r * math.sin(th) + r * math.cos(th) * (math.cos(T * j / n_ang) * uu + flat * math.sin(T * j / n_ang) * vv) for j in range(n_ang)])
    apex = c + d * r
    vs = [p for ring in rings for p in ring] + [apex]
    fs = []; m = len(rings)
    for i in range(m - 1):
        for j in range(n_ang):
            fs.append((i * n_ang + j, i * n_ang + (j + 1) % n_ang, (i + 1) * n_ang + (j + 1) % n_ang, (i + 1) * n_ang + j))
    fs.append(tuple(reversed(range(n_ang))))
    ap = len(vs) - 1
    for j in range(n_ang):
        fs.append(((m - 1) * n_ang + j, (m - 1) * n_ang + (j + 1) % n_ang, ap))
    g.mesh(name, vs, fs, 'structure')
    return frames, flat


def junction(name, frames, flat, inside, n_ang=96):
    """Draw where a swept shell enters another body: the intersection curve."""
    pts = []
    for j in range(n_ang + 1):
        a = T * j / n_ang
        prev = None
        for c, d, uu, vv, r in frames:
            q = c + r * (math.cos(a) * uu + flat * math.sin(a) * vv)
            ins = inside(q)
            if prev is not None and prev[1] and not ins:
                lo, hi = prev[0], (c, d, uu, vv, r)
                for _ in range(12):
                    mid = tuple(x.lerp(y, .5) if isinstance(x, Vector) else (x + y) / 2 for x, y in zip(lo, hi))
                    mq = mid[0] + mid[4] * (math.cos(a) * mid[2] + flat * math.sin(a) * mid[3])
                    if inside(mq):
                        lo = mid
                    else:
                        hi = mid
                pts.append(hi[0] + hi[4] * 1.004 * (math.cos(a) * hi[2] + flat * math.sin(a) * hi[3]))
                break
            prev = ((c, d, uu, vv, r), ins)
    if len(pts) > 8:
        g.wire(name, pts, .08, 'structure')


def surface_ring_at(frames, flat, sv_index, off=.06, name='joint seam', role='detail'):
    c, d, uu, vv, r = frames[sv_index]
    g.wire(name, [c + (r + off) * (math.cos(T * j / 96) * uu + flat * math.sin(T * j / 96) * vv) for j in range(97)], .07, role)


def pin(frames, flat, k, side, rho=3.2):
    """Joint axle pin drawn conformally on the lateral face."""
    c, d, uu, vv, r = frames[k]
    pts = []
    for j in range(49):
        t = T * j / 48
        x = rho * math.cos(t); phi = (rho * math.sin(t)) / r
        ang = (0 if side > 0 else math.pi) + (phi if side > 0 else -phi)
        pts.append(c + d * x + (r + .06) * (math.cos(ang) * uu + flat * math.sin(ang) * vv))
    g.wire('joint pin', pts, .07, 'detail')


def nearest(frames, p):
    return min(range(len(frames)), key=lambda i: (frames[i][0] - Vector(p)).length)


def pad_outline(name, frames, flat, tip_back=11.5, half_len=3.6, half_ang=36):
    """Sensor pad: conformal outline on the palmar face, inside the contour."""
    s_acc = [0]
    for i in range(1, len(frames)):
        s_acc.append(s_acc[-1] + (frames[i][0] - frames[i - 1][0]).length)
    target = s_acc[-1] - tip_back
    pts = []
    for j in range(73):
        t = T * j / 72
        sv = target + half_len * math.cos(t)
        k = min(range(len(s_acc)), key=lambda i: abs(s_acc[i] - sv))
        c, d, uu, vv, r = frames[k]
        ang = math.radians(-90 + half_ang * math.sin(t))
        pts.append(c + d * (sv - s_acc[k]) + (r + .06) * (math.cos(ang) * uu + flat * math.sin(ang) * vv))
    g.wire(name, pts, .07, 'accent')
    k = min(range(len(s_acc)), key=lambda i: abs(s_acc[i] - target))
    c, d, uu, vv, r = frames[k]
    return c + (r * flat + .4) * (-vv)


def finger(name, spec):
    mcp, spread, lengths, radii, flex = spec
    pts, frames_ = chain(mcp, spread, lengths, flex)
    base = pts[0] - frames_[0][0] * 12          # starts inside the palm
    tip = pts[3] - frames_[2][0] * radii[2] * .9
    fr, flat = sweep(name + ' finger shell', [base, pts[0], pts[1], pts[2], tip],
                     (radii[0] * 1.02, radii[0], radii[1], radii[2], radii[2] * .9), frames_[0][2])
    junction(name + ' palm junction', fr, flat, palm_inside)
    for k in (1, 2):
        i = nearest(fr, pts[k])
        surface_ring_at(fr, flat, i, name='joint seam')
        for side in (-1, 1):
            pin(fr, flat, i, side, FINGERS[name][3][k - 1] * .36)
    return pts, frames_, pad_outline(name + ' fingertip pad', fr, flat, radii[2] * 1.45)


def fingertip_section(spec):
    """B: the index fingertip cut on its mid-plane. Same position as in A."""
    mcp, spread, lengths, radii, flex = spec
    pts, frames = chain(mcp, spread, lengths, flex)
    d, up, ax = frames[2]
    v = (up - d * up.dot(d)).normalized(); u = v.cross(d)
    a = pts[2]; L = lengths[2]; R = radii[2] * 1.02

    def ring_pt(x, rad, ang):
        return a + d * x + rad * (math.cos(ang) * u + math.sin(ang) * v)

    def dome(x, rmax):                 # rounded tip: radius falls to zero at x = L
        t = (x - (L - rmax)) / rmax
        return rmax if t <= 0 else rmax * math.sqrt(max(0, 1 - t * t))

    def half_layer(name, rin, rout, x0, x1, a0, a1, role, n=40, m=28):
        """Revolved layer between two radius laws, over an angle sector, capped."""
        xs = [x0 + (x1 - x0) * k / n for k in range(n + 1)]
        angs = [math.radians(a0 + (a1 - a0) * j / m) for j in range(m + 1)]
        vs = []
        for x in xs:
            for rr in (rin(x), rout(x)):
                for ang in angs:
                    vs.append(ring_pt(x, rr, ang))
        fs = []; W_ = m + 1
        def idx(i, layer, j): return (i * 2 + layer) * W_ + j
        for i in range(n):
            for j in range(m):
                fs.append((idx(i, 1, j), idx(i, 1, j + 1), idx(i + 1, 1, j + 1), idx(i + 1, 1, j)))
                fs.append((idx(i, 0, j), idx(i + 1, 0, j), idx(i + 1, 0, j + 1), idx(i, 0, j + 1)))
            for j in (0, m):
                fs.append((idx(i, 0, j), idx(i, 1, j), idx(i + 1, 1, j), idx(i + 1, 0, j)))
        for i in (0, n):
            for j in range(m):
                fs.append((idx(i, 0, j), idx(i, 0, j + 1), idx(i, 1, j + 1), idx(i, 1, j)))
        return g.mesh(name, vs, fs, role)

    xc = L - 2.6

    def core(x):                       # structural core with its own rounded tip
        t = (x - (xc - 4.6)) / 4.6
        return 4.6 if t <= 0 else 4.6 * math.sqrt(max(0, 1 - t * t))
    half_layer('distal bone core', lambda x: 0.001, core, 0, xc, -90, 90, 'structure', 44, 28)
    # Flex circuit: a thin palmar layer on the core, taxels printed on it.
    half_layer('flex circuit', lambda x: core(x) + .15, lambda x: core(x) + .55, 3, L - 5.2, -90, -30, 'cable')
    for k in range(5):
        x = 4.5 + k * 2.5
        for ang in (-90, -72, -54):
            p = ring_pt(x, core(x) + .95, math.radians(ang))
            sphere('taxel', p, .42, 'accent', 12, 6)
    p = ring_pt(L - 6.2, core(L - 6.2) + .8, math.radians(-70))
    sphere('temperature sensor', p, .75, 'accent', 14, 8)
    # Compliant skin: thicker on the pad, thinner over the back; tip closed.
    skin_in = lambda x: core(x) + 1.2 if core(x) > .1 else 0.001
    half_layer('compliant skin', skin_in, lambda x: dome(x, R), 0, L, -90, 90, 'structure', 44, 32)
    # Nail cap: a stiff dorsal plate over the distal two thirds.
    half_layer('nail cap', lambda x: dome(x, R) + .1, lambda x: dome(x, R) + 1.5, L * .28, L - 2.4, 38, 90, 'structure')
    return pts, frames, (a, d, u, v, L, R)


def build():
    views(B=(0, 0), C=(20, 10))
    # --- palm, thenar, parting lines ------------------------------------------------------
    palm = hull('palm shell', PALM, 'Y', 'structure', E)
    g.wire('dorsal cover seam', [sec_pt(PALM, 34, math.radians(a), .3) for a in range(20, 161, 4)], .2, 'detail')
    for x in (-23, -7, 9, 24):
        y0, y1 = 50, 76
        z0 = sec_pt(PALM, y0, math.acos(max(-1, min(1, x / 40)))).z; z1 = sec_pt(PALM, y1, math.acos(max(-1, min(1, x / 41)))).z
        capsule_segment('finger drive housing', (x, y0, z0 - 1.2), (x, y1, z1 - 1.2), 4.4, 4.2, 'structure', 18, .5, (0, 0, 1))
    # --- fingers and thumb: one continuous shell each ------------------------------------------
    pads = {}
    for name, spec in FINGERS.items():
        pads[name] = finger(name, spec)[2]
    tb = [Vector(p) for p in THUMB]
    tbase = Vector((-4, 8, 0))                # thumb root tapers from inside the palm
    ttip = tb[3] - (tb[3] - tb[2]).normalized() * THUMB_R[2] * .9
    tu = (tb[2] - tb[1]).cross(Vector((0, 0, -1))).normalized()
    tfr, tflat = sweep('thumb shell', [tbase, tb[0], tb[1], tb[2], ttip], (3, 14.5, THUMB_R[0] * .86, THUMB_R[1], THUMB_R[2] * .9), tu)
    junction('thumb palm junction', tfr, tflat, palm_inside)
    for p in (tb[1], tb[2]):
        i = nearest(tfr, p)
        surface_ring_at(tfr, tflat, i, name='joint seam')
        for side in (-1, 1):
            pin(tfr, tflat, i, side, 3.8)
    thumb_pad = pad_outline('thumb pad', tfr, tflat, THUMB_R[2] * 1.45)
    # --- wrist and short socket -------------------------------------------------------------------
    cyl('wrist rotator', (0, -22, 0), 25.5, 16, 'structure', (0, 1, 0), 72)
    ring('rotator bearing band', (0, -15, 0), 26.6, 1.4, 3, (0, 1, 0), 'detail')
    cyl('release button', (-25.6, -12, 7), 3, 1.4, 'accent', (-1, 0, 0), 20)
    sock = hull('socket shell', SOCKET, 'Y', 'structure', .8)
    hull_seam(sock, -30)
    # Clean section cut at the end of the drawing: the shell wall is 3 mm.
    rx, rz, lift = profile_at(SOCKET, -70)
    g.wire('section cut, inner wall', [Vector(((rx - 3) * math.copysign(abs(math.cos(a)) ** .8, math.cos(a)), -70.6, lift + (rz - 3) * math.copysign(abs(math.sin(a)) ** .8, math.sin(a)))) for a in [T * k / 96 for k in range(97)]], .3, 'accent')
    for i in range(3):
        cyl('status light', (-8 + i * 8, -52, profile_at(SOCKET, -52)[1] + .1), 1.4, .8, 'accent', (0, 0, 1), 12)
    cyl('abutment stub', (0, -71, 0), 6.5, 14, 'structure', (0, -1, 0), 36)
    ring('abutment collar', (0, -82, 0), 9, 2.4, 2.5, (0, -1, 0), 'detail')
    # --- B: fingertip in section (not exported in A) -------------------------------------------------
    with group('B'):
        ip, ifr, (fa, fd, fu, fv, fL, fR) = fingertip_section(FINGERS['index'])
    # --- C: implanted interface, axial exploded (not exported in A) ---------------------------------
    with group('C'):
        cyl('abutment', (0, -140, 0), 6.5, 26, 'structure', (0, -1, 0), 36)
        ring('abutment collar', (0, -164, 0), 9.5, 3, 3, (0, -1, 0))
        cyl('feedthrough', (0, -136, 0), 7.4, 4, 'structure', (0, -1, 0), 36)
        for a in (90, 210, 330):
            q = math.radians(a)
            cyl('feedthrough pin', (3.6 * math.cos(q), -132, 3.6 * math.sin(q)), .9, 4, 'accent', (0, 1, 0), 12)
        cyl('fixture', (0, -167, 0), 5.4, 72, 'structure', (0, -1, 0), 36)
        for k in range(20):
            ring('fixture thread', (0, -172 - k * 3.2, 0), 6.3, .9, 1.2, (0, -1, 0), 'detail')
        box('lead exit port', (0, -182, 6.8), (6, 8, 3), 1, 'detail')
        for (x, z), label in [((-26, -10), 'median'), ((22, -16), 'ulnar'), ((6, 24), 'radial')]:
            loft(label + ' nerve', [(x * .8, -150, z * .8), (x, -194, z), (x * 1.08, -224, z * 1.06), (x * 1.14, -246, z * 1.1)], lambda t: 3.4 - .9 * t, 20, 'shell')
            c = Vector((x * 1.02, -216, z * 1.03))
            arc_tube('cuff electrode', c + Vector((0, 5, 0)), (0, -1, 0), (x, 0, z), 4.9, 1.2, 10, 30, 330, 'accent')
            box('cuff connector', c + Vector((x, 0, z)).normalized() * 6.2, (3, 6, 3), .8, 'detail')
            tube('lead wire', [(0, -182, 8.2), (x * .4, -190, z * .4 + 4), c + Vector((x, 0, z)).normalized() * 7.8 + Vector((0, 3, 0))], .55, 'cable')
    # --- anchors (visible in A) ----------------------------------------------------------------------
    pts, fr = chain(*[FINGERS['index'][k] for k in (0, 1, 2, 4)])
    d, up, ax = fr[2]; v = (up - d * up.dot(d)).normalized()
    r2 = FINGERS['index'][3][2]
    mark('FINGERTIP PADS', pads['index'], '24 TAXELS EACH / PRESSURE, TEXTURE, WARMTH')
    mark('OPPOSED THUMB', thumb_pad, 'OPENS 58 mm / THE WIDTH OF A SMALL HAND')
    mark('WRIST ROTATOR', (-25.6, -14, 8), '300° ROTATION / QUICK RELEASE')
    mark('SOCKET', sec_pt(SOCKET, -58, math.radians(100), .3), 'BATTERY AND 16-CHANNEL STIMULATOR INSIDE')
    mark('ABUTMENT STUB', (6.5, -78, 0), 'TITANIUM / CARRIES LOAD AND SIGNALS')
    # --- pose: palm frame -> world, then keep B and C out of A --------------------------------------
    Y = Vector(REACH).normalized()
    Z = -Vector(PALMAR); Z = (Z - Y * Z.dot(Y)).normalized()
    X = Y.cross(Z)
    W = Matrix.Scale(SCALE, 4) @ Matrix((X, Y, Z)).transposed().to_4x4()
    transform(0, 0, W)
    from .. import kit
    for grp in kit.GROUPS.values():
        grp['wires'] = [(n, [W @ Vector(p) for p in pts_], r) for n, pts_, r in grp['wires']]
    for k, v_ in list(g.anchors.items()):
        g.anchors[k] = W @ Vector(v_)
    # Joint-barrel callout on the index finger's middle joint, on the pin ring
    # facing the right-hand callout column, so its leader crosses no finger.
    az = math.radians(PROBE[0] if PROBE else -15)
    screen_right = Vector((math.cos(az), math.sin(az), 0))
    ip_, ifr_ = chain(*[FINGERS['index'][k] for k in (0, 1, 2, 4)])
    rr = FINGERS['index'][3][0] * .98
    cands = [W @ (ip_[1] + ifr_[1][2].normalized() * s_ * (rr + .7)) for s_ in (-1, 1)]
    g.anchors['JOINT BARRELS'] = max(cands, key=lambda c: c.dot(screen_right))
    NOTES_ = __import__('century.kit', fromlist=['NOTES']).NOTES
    NOTES_['JOINT BARRELS'] = 'ONE DRIVE PER FINGER / 14 JOINTS'
    hidden = {id(o) for key in 'BC' for o, r in kit.GROUPS[key]['parts']}
    hidden_wires = {n for key in 'BC' for n, p, r in kit.GROUPS[key]['wires']}
    g.parts[:] = [(o, r) for o, r in g.parts if id(o) not in hidden]
    g.wires[:] = [w for w in g.wires if w[0] not in hidden_wires]
    # B camera: square to the section plane, a little from the tip and palm side.
    fu_w = (W.to_3x3() @ fu).normalized(); fd_w = (W.to_3x3() @ fd).normalized(); fv_w = (W.to_3x3() @ fv).normalized()
    t = (-fu_w * .88 + fd_w * .3 - fv_w * .36).normalized()
    views(B=(math.degrees(math.atan2(t.x, -t.y)), math.degrees(math.asin(max(-1, min(1, t.z))))))
    return PROBE or (-15, 18)
