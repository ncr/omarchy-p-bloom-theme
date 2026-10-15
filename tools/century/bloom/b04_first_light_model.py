"""FIRST LIGHT: school-owned robotic telescope under a dark sky.

Units are centimetres. Z up. A 3.2 m drum observatory; its clamshell dome
opens as two quarter-sphere shells that swing 95 degrees outward about
hinges on the rim and stand open like petals (horizon limit ~8 degrees). The outer skin of the shells is the solar
array: closed by day it charges the battery vault in the pier base.
Inside, an alt-azimuth fork carries a 0.5 m f/6.8 Serrurier truss
telescope pointing 50 degrees up. The camera train leaves through the
Nasmyth port in the right fork arm. A weather mast decides each night.
"""
from contextlib import contextmanager
from ..kit import *
from .parts import loft, sphere, dome, arc_tube, arc_points, frame_matrix

R = 160          # drum radius
H = 200          # drum height (rim)
SHELL = 158      # shell radius
OPEN = 95        # shell swing, degrees: petals stand open
ALT = 214        # altitude axis just above the dome centre: parks inside a closed dome
ELEV = 50        # telescope elevation, degrees
AZ = 58          # telescope azimuth from +X toward +Y, degrees


@contextmanager
def local(m):
    start = len(g.parts); wstart = len(g.wires)
    yield
    transform(start, wstart, m)


def shell(side):
    """Quarter-sphere shell, built about its hinge, then swung open."""
    hinge = (side * R, 0, H)
    a0, a1 = (-90, 90) if side > 0 else (90, 270)
    c = Vector((-side * R, 0, 0))
    with at(hinge, side * OPEN, 'Y'):
        dome('clamshell solar shell', c, SHELL, SHELL, 'structure', 48, 14, a0, a1)
        # Stiffening lip along the cut meridian, and the equator seat.
        # The lip runs over the top on both petals: ref turns with the side, so axis x ref is always +z
        # (with a fixed +y ref the left petal's lip hung below the seat and its rim read as a full circle).
        arc_tube('shell meridian lip', c + Vector((-side * 1.5, 0, 0)), (side, 0, 0), (0, side, 0), SHELL + 1.5, 3, 3, 0, 180, 'structure')
        arc_tube('shell seat ring', c, (0, 0, 1), (side, 0, 0), SHELL + 1.5, 3, 3, -90, 90, 'structure')
        # Thin-film solar tiles: meridian and latitude seams on the outer skin.
        for az in range(a0 + 18, a1, 18):
            q = math.radians(az)
            g.wire('solar tile seam', [c + (SHELL + .4) * Vector((math.cos(math.radians(t)) * math.cos(q), math.cos(math.radians(t)) * math.sin(q), math.sin(math.radians(t)))) for t in range(4, 88, 3)], .1, 'shell')
        for lat in (22, 44, 64):
            rr = (SHELL + .4) * math.cos(math.radians(lat)); zz = (SHELL + .4) * math.sin(math.radians(lat))
            g.wire('solar tile seam', [c + Vector((rr * math.cos(math.radians(az)), rr * math.sin(math.radians(az)), zz)) for az in range(a0 + 2, a1 - 1, 3)], .1, 'shell')
        # Inner stiffening ribs, seen on the petal that faces away.
        for az in range(a0 + 30, a1, 30):
            q = math.radians(az)
            g.wire('inner rib', [c + (SHELL - 1.2) * Vector((math.cos(math.radians(t)) * math.cos(q), math.cos(math.radians(t)) * math.sin(q), math.sin(math.radians(t)))) for t in range(3, 86, 3)], .5, 'detail')
        # Hinge knuckles on the rim.
        for y in (-110, -40, 40, 110):
            cyl('shell hinge knuckle', (0, y - 6, 0), 3.2, 12, 'detail', (0, 1, 0), 16)


def shell_point(side, az, lat, y=None, lift=0):
    """World point on an open shell (az/lat about its own centre, before swinging).
    If y is given, az is solved so the point lies at that y on the seat (lat 0)."""
    if y is not None:
        cx = math.sqrt(max(0, SHELL ** 2 - y * y)) * (1 if side > 0 else -1)
        rel = Vector((cx, y, 0))
    else:
        q = math.radians(az); t = math.radians(lat)
        rel = (SHELL + lift) * Vector((math.cos(t) * math.cos(q), math.cos(t) * math.sin(q), math.sin(t)))
    rel = rel + Vector((-side * R, 0, 0))
    return Matrix.Translation((side * R, 0, H)) @ Matrix.Rotation(math.radians(side * OPEN), 4, 'Y') @ rel


def fork_mount():
    """Alt-az fork in the mount frame: x along the altitude axis, z up, origin at the axis."""
    cyl('azimuth turntable', (0, 0, -90), 44, 14, 'structure')
    ring('azimuth drive ring', (0, 0, -77), 45.5, 3, 4, (0, 0, 1), 'accent')
    bolts((0, 0, -75.5), 40, 12, size=1.1)
    # Cast yoke: a shallow U whose arms taper up to the altitude bearings.
    hull('fork yoke', [(-64, 5, 6, 5), (-57, 15, 9, 2), (-40, 17, 8, 0), (40, 17, 8, 0), (57, 15, 9, 2), (64, 5, 6, 5)], 'X').matrix_world = Matrix.Translation((0, 0, -68))
    for side in (-1, 1):
        x = side * 56
        g.casting('fork arm', [(0, 8.5, 17), (22, 8, 15), (48, 7.5, 13), (62, 7.5, 13)], 'structure', 0)
        g.parts[-1][0].matrix_world = Matrix.Translation((x, 0, -66))
        g.trim('arm parting line', 0, 8.9, 14.4)
        g.wires[-1] = (g.wires[-1][0], [Matrix.Translation((x, 0, -30)) @ p_ for p_ in g.wires[-1][1]], g.wires[-1][2])
        cyl('altitude bearing housing', (x - side * 8, 0, 0), 20, 16, 'structure', (side, 0, 0))
        ring('altitude direct drive', (x + side * 8.5, 0, 0), 21, 3, 3, (side, 0, 0), 'accent')
        flange('bearing cover', (x + side * 11, 0, 0), 14, (side, 0, 0), 1.5)
        box('encoder read head', (x + side * 9, 0, -22), (5, 8, 5), 1, 'detail')
    # Cable wrap: a loose helix from the turntable up the left arm.
    pts = [Vector((-24 + 9 * math.cos(t / 2.6), -12 + 9 * math.sin(t / 2.6), -76 + t * 1.6)) for t in range(0, 26)]
    tube('cable wrap', pts + [Vector((-50, -12, -36)), Vector((-50, -14, -16))], .9, 'cable')


def telescope():
    """Optical tube in its own frame: z along the optical axis, x along the altitude axis."""
    cyl('mirror cell', (0, 0, -86), 34, 22, 'structure')
    flange('mirror cell flange', (0, 0, -64), 35, (0, 0, 1), 2)
    for a in (0, 120, 240):
        q = math.radians(a)
        ring('cell cooling fan', (17 * math.cos(q), 17 * math.sin(q), -88), 7, 1.2, 2, (0, 0, -1), 'detail')
    cyl('primary mirror', (0, 0, -62), 25, 4, 'accent', (0, 0, 1), 64)
    # Serrurier truss: four V pairs to the upper cage.
    for k in range(8):
        b = math.radians(45 * k); t = math.radians(45 * k + (22.5 if k % 2 == 0 else -22.5))
        rod('truss tube', (32 * math.cos(b), 32 * math.sin(b), 10), (32 * math.cos(t), 32 * math.sin(t), 92), 1.6)
    for z in (92, 110):
        ring('upper cage ring', (0, 0, z), 35, 3.5, 4, (0, 0, 1), 'structure')
    for k in range(8):
        a = math.radians(45 * k + 22.5)
        rod('cage stringer', (33.5 * math.cos(a), 33.5 * math.sin(a), 96), (33.5 * math.cos(a), 33.5 * math.sin(a), 110), 1.1, 'detail')
    cyl('secondary holder', (0, 0, 96), 10, 16, 'structure')
    for a in (45, 135, 225, 315):
        q = math.radians(a)
        box('spider vane', (22 * math.cos(q), 22 * math.sin(q), 104), (26, .8, 6), .2, 'detail').matrix_world = \
            Matrix.Translation((22 * math.cos(q), 22 * math.sin(q), 104)) @ Matrix.Rotation(q, 4, 'Z') @ Matrix.Translation((-22 * math.cos(q), -22 * math.sin(q), -104))
    ring('light baffle', (0, 0, 114), 36, 1.5, 14, (0, 0, 1), 'shell')


def camera_train():
    """Nasmyth port on +x (altitude axis) in the telescope frame."""
    x = 66
    cyl('derotator', (x + 5, 0, 0), 15, 8, 'structure', (1, 0, 0))
    ring('derotator scale', (x + 13, 0, 0), 15.5, 1.5, 1.5, (1, 0, 0), 'accent')
    cyl('focuser body', (x + 14, 0, 0), 9, 12, 'structure', (1, 0, 0))
    cyl('focus motor', (x + 20, 0, 12), 3.5, 8, 'detail', (0, 0, 1))
    box('focus motor gearbox', (x + 20, 0, 9.5), (7, 7, 4), 1, 'detail')
    cyl('filter wheel', (x + 27, 0, -4), 16, 5, 'structure', (1, 0, 0))
    for k in range(6):
        q = math.radians(60 * k + 30)
        ring('filter slot', (x + 32.2, 11 * math.cos(q), -4 + 11 * math.sin(q)), 3.4, .6, .5, (1, 0, 0), 'accent' if k == 1 else 'detail')
    box('CMOS camera body', (x + 44, 0, 0), (13, 22, 22), 3)
    for k in range(7):
        box('camera cooling fin', (x + 53 + 1.8 * k, 0, 0), (.8, 19, 19), .3, 'detail')
    ring('fan guard', (x + 66, 0, 0), 8, 1, 1.2, (1, 0, 0), 'detail')
    tube('USB and power', [(x + 44, 11, 5), (x + 40, 17, 12), (x + 26, 18, 16), (x + 14, 16, 12)], .7, 'cable')


def mast():
    base = Vector((-120, 150, 0))
    cyl('mast foot', base, 12, 6, 'structure')
    rod('weather mast', base, base + Vector((0, 0, 420)), 3.2)
    for z in (140, 280):
        ring('mast clamp', base + Vector((0, 0, z)), 4.4, 1.2, 3, (0, 0, 1), 'detail')
    top = base + Vector((0, 0, 420))
    rod('anemometer spindle', top, top + Vector((0, 0, 22)), 1.2, 'detail')
    for k in range(3):
        q = math.radians(120 * k + 20)
        tip = top + Vector((16 * math.cos(q), 16 * math.sin(q), 20))
        rod('anemometer arm', top + Vector((0, 0, 20)), tip, .6, 'detail')
        sphere('anemometer cup', tip, 4, 'structure', 16, 8)
    rod('vane arm', base + Vector((0, 0, 400)), base + Vector((-34, 0, 400)), 1.0, 'detail')
    rod('wind vane', base + Vector((-2, 0, 400)), base + Vector((26, 0, 400)), .9, 'detail')
    g.mesh('vane tail', [base + Vector((-34, 0, 394)), base + Vector((-48, 0, 391)), base + Vector((-48, 0, 411)), base + Vector((-34, 0, 406))], [(0, 1, 2, 3)], 'structure')
    # All-sky camera on a side arm: fisheye dome on a small box.
    arm = base + Vector((0, -26, 372))
    rod('sky camera arm', base + Vector((0, 0, 372)), arm, 1.2, 'detail')
    box('sky camera body', arm, (14, 14, 12), 2.5)
    sphere('all-sky dome', arm + Vector((0, 0, 7)), 6.5, 'accent', 24, 12)
    box('rain sensor', base + Vector((12, 0, 330)), (12, 3, 9), 1, 'detail').matrix_world = \
        Matrix.Translation(base + Vector((12, 0, 330))) @ Matrix.Rotation(math.radians(35), 4, 'Y') @ Matrix.Translation(-(base + Vector((12, 0, 330))))
    rod('rain sensor arm', base + Vector((0, 0, 330)), base + Vector((8, 0, 330)), .8, 'detail')
    tube('sensor cable', [base + Vector((3, -3, 360)), base + Vector((4, -4, 200)), base + Vector((4, -4, 30)), Vector((-110, 138, 8))], .6, 'cable')
    return top


def build():
    views(B=(-20, 16), C=(-38, 18))
    # --- drum -----------------------------------------------------------------
    box('concrete pad', (0, 0, -8), (370, 370, 16), 8)
    # Separate wall segments occlude each other (the exporter never hides an
    # object's own far edges), so the open drum reads as solid.
    for k in range(12):
        arc_tube('drum wall segment', (0, 0, 0), (0, 0, 1), (1, 0, 0), R, 5, H, 30 * k, 30 * k + 30, 'structure', 12)
    cyl('observing deck', (0, 0, 92), R - 5, 4, 'structure', n=96)
    ring('rim seat', (0, 0, H - 4), R + 3, 5, 6, (0, 0, 1), 'structure')
    ring('plinth band', (0, 0, 0), R + 2.5, 3, 14, (0, 0, 1), 'structure')
    for a in range(0, 360, 30):
        if -95 < ((a + 180) % 360) - 180 < -85 or a in (240, 300):
            continue
        q = math.radians(a)
        g.wire('wall panel seam', [(math.cos(q) * (R + .4), math.sin(q) * (R + .4), 16), (math.cos(q) * (R + .4), math.sin(q) * (R + .4), H - 6)], .12, 'detail')
    # Service door facing the path, with frame, lever handle, step and rail.
    dq = math.radians(-52)
    dn = Vector((math.cos(dq), math.sin(dq), 0)); dt = Vector((-math.sin(dq), math.cos(dq), 0))
    dp = dn * (R + 1.5)
    with local(frame_matrix(dp, dn, dt)):
        box('door leaf', (0, 95, 0), (80, 190, 3), 2)
        box('door frame head', (0, 192, 0), (92, 5, 4), 1, 'detail')
        for x in (-44, 44):
            box('door frame jamb', (x, 95, 0), (5, 194, 4), 1, 'detail')
        box('door lever', (28, 100, 3), (12, 2.4, 2.4), .8, 'accent')
        box('door vent', (0, 30, 2), (50, 18, 1.5), 1, 'detail')
        for k in range(4):
            box('vent louvre', (0, 24 + 4 * k, 2.8), (46, 1.2, 1), .3, 'detail')
    step = dn * (R + 32)
    box('entry step', step + Vector((0, 0, 8)), (60, 60, 16), 3)
    box('entry step', step + dn * 30 + Vector((0, 0, 0)), (60, 50, 4), 2, 'detail')
    rail_base = dp + dt * 58
    loft('hand rail', [rail_base + Vector((0, 0, 0)), rail_base + dn * 40 + Vector((0, 0, 0)), rail_base + dn * 40 + Vector((0, 0, 95)), rail_base + Vector((0, 0, 100))], 1.6, 10, 'structure', False)
    # Nameplate beside the door: the schools that own the telescope.
    with local(frame_matrix(dn * (R + 1) + Vector((0, 0, 0)), dn, dt)):
        box('owners plate', (-78, 150, 0), (46, 26, 1.2), 1.5, 'accent')
    # --- clamshell petals ---------------------------------------------------------
    for side in (-1, 1):
        shell(side)
        # Opening ram: from the wall bracket to the shell lip.
        for y in (-90, 90):
            a = Vector((side * (math.sqrt(R * R - y * y) + 3), y, 120)); b = shell_point(side, 0, 0, y, 0)
            u = (b - a).normalized()
            cyl('ram cylinder', a, 3, 40, 'structure', u, 20)
            rod('ram rod', a + u * 40, b, 1.4, 'detail')
            box('ram foot', a - u * 2, (8, 10, 7), 1.5, 'detail')
    # --- pier, fork, telescope ------------------------------------------------------
    cyl('pier', (0, 0, 0), 26, ALT - 88, 'structure', n=48)
    flange('pier head', (0, 0, ALT - 94), 30, (0, 0, 1), 4)
    phi = math.radians(AZ); el = math.radians(ELEV)
    a_axis = Vector((-math.sin(phi), math.cos(phi), 0))
    d = Vector((math.cos(el) * math.cos(phi), math.cos(el) * math.sin(phi), math.sin(el)))
    centre = Vector((0, 0, ALT))
    with group('B'):
        with local(frame_matrix(centre, (0, 0, 1), a_axis)):
            fork_mount()
    with local(frame_matrix(centre, d, a_axis)):
        telescope()
    with group('C'):
        with local(frame_matrix(centre, (0, 0, 1), a_axis)):
            camera_train()
        mark('CAMERA TRAIN', centre + a_axis * 110 + Vector((0, 0, 11.5)), 'NASMYTH PORT ON THE FORK ARM')
    with group('B'):
        # The trunnions and centre section belong to the mount study as well.
        with local(frame_matrix(centre, d, a_axis)):
            for side in (-1, 1):
                cyl('trunnion', (side * 36, 0, 0), 12, 10, 'structure', (side, 0, 0))
            cyl('centre section', (0, 0, -24), 36, 34, 'structure', (0, 0, 1), 64)
            for z in (-20, 6):
                ring('centre section band', (0, 0, z), 36.8, 1, 1.6, (0, 0, 1), 'detail')
    top = mast()
    mark('0.5 m TELESCOPE', centre + d * 112 + a_axis * 30, 'SERRURIER TRUSS / f/6.8 / 3.4 m FOCAL LENGTH')
    mark('WEATHER MAST', top + Vector((0, 0, 20)), 'WIND, CLOUD AND RAIN DECIDE EACH NIGHT')
    mark('SOLAR PETAL', shell_point(1, -20, 66, lift=1), 'THIN-FILM SKIN / CHARGES WHILE CLOSED BY DAY')
    mark('SERVICE DOOR', dp + dt * -30 + Vector((0, 0, 150)), 'ONE VISIT A YEAR / FIVE YEARS OF SPARES INSIDE')
    return 20, 24
