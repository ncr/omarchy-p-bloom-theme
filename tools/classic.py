"""The first set of sheets: generic spacecraft and machinery.

Not shipped in backgrounds/ any more; render it with
    python3 tools/make_wallpapers.py --set classic
These sheets use the older layout, with the title block at the bottom left and
no emblem.
"""

import math

import cairo

from sheet import ARC, GOLD, WHITE, Sheet, polar

TOTAL = 6


def start(size, no, seed):
    s = Sheet(size[0], size[1], seed=seed)
    s.background()
    s.begin_lines()
    s.grid()
    s.frame(no, TOTAL)
    return s


# ---------------------------------------------------------------------------
# 01  Ring station: plan view, edge-on elevation, enlarged detail
# ---------------------------------------------------------------------------

def ring_station(size):
    s = start(size, 1, 11)
    cx, cy = s.cx, s.cy - 10

    # construction circles and the degree ring
    s.circ(cx, cy, 500, 0.10, 0.5)
    s.circ(cx, cy, 452, 0.22, 0.5, dash=[2, 5])
    s.circ(cx, cy, 418, 0.30, 0.5)
    s.ticks(cx, cy, 418, 360, 5, 0.30, 0.45, major=10, major_len=11)
    for d in range(0, 360, 30):
        if d % 180 == 0:
            continue
        x, y = polar(cx, cy, 440, d)
        s.text(f"{d:03d}", x, y + 3, 6.5, a=0.5, align="c")
    s.arc(cx, cy, 476, 200, 252, 0.75, 2.2)
    s.arc(cx, cy, 476, 258, 262, 0.75, 2.2)
    s.arc(cx, cy, 476, 20, 64, 0.45, 1.2)
    s.arc(cx, cy, 486, 96, 170, 0.25, 0.6, dash=[10, 4, 2, 4])
    s.ln(cx - 560, cy, cx + 560, cy, 0.16, 0.5, dash=[18, 4, 3, 4])
    s.ln(cx, cy - 520, cx, cy + 520, 0.16, 0.5, dash=[18, 4, 3, 4])

    # habitat ring: two walls, 36 compartments, every sixth one hatched
    for r, a, w in ((288, 0.45, 0.6), (300, 0.9, 1.1), (338, 0.9, 1.1), (350, 0.45, 0.6)):
        s.circ(cx, cy, r, a, w)
    s.circ(cx, cy, 319, 0.18, 0.5, dash=[1.5, 4])
    for i in range(36):
        d = i * 10 + 5
        x1, y1 = polar(cx, cy, 300, d)
        x2, y2 = polar(cx, cy, 338, d)
        s.ln(x1, y1, x2, y2, 0.5, 0.5)
    for i in range(0, 36, 6):
        a0, a1 = i * 10 + 5, i * 10 + 15

        def seg(a0=a0, a1=a1):
            s.c.new_sub_path()
            s.c.arc(cx, cy, 338, math.radians(a0), math.radians(a1))
            s.c.arc_negative(cx, cy, 300, math.radians(a1), math.radians(a0))
            s.c.close_path()
        s.hatch(seg, 4, 45 + a0, 0.4)
        s.band(cx, cy, 300, 338, a0, a1, 0.0, 0.1, fill=0.06)

    # spokes: six twin tubes with a lift car on each
    for i in range(6):
        d = i * 60 + 30
        for off in (-5, 5):
            ox, oy = polar(0, 0, off, d + 90)
            x1, y1 = polar(cx, cy, 58, d)
            x2, y2 = polar(cx, cy, 288, d)
            s.ln(x1 + ox, y1 + oy, x2 + ox, y2 + oy, 0.7, 0.7)
        for k in range(8):
            r = 80 + k * 26
            ox, oy = polar(0, 0, 5, d + 90)
            x, y = polar(cx, cy, r, d)
            s.ln(x - ox, y - oy, x + ox, y + oy, 0.35, 0.45)
        x, y = polar(cx, cy, 150 + i * 17, d)
        s.c.save()
        s.c.translate(x, y)
        s.c.rotate(math.radians(d))
        s.rect(-9, -8, 18, 16, 0.9, 0.8, fill=0.12)
        s.c.restore()

    # hub
    s.circ(cx, cy, 58, 0.9, 1.0, fill=0.05)
    s.circ(cx, cy, 46, 0.4, 0.5)
    s.poly([polar(cx, cy, 34, 60 * k) for k in range(6)], 0.8, 0.8)
    s.circ(cx, cy, 14, 0.9, 0.8)
    s.ticks(cx, cy, 46, 48, 5, 0.4, 0.45)
    s.cross(cx, cy, 7, 0.9, 0.6)

    # docking arms on the vertical axis
    for sgn in (-1, 1):
        y0 = cy + sgn * 350
        s.rect(cx - 7, min(y0, y0 + sgn * 34), 14, 34, 0.8, 0.7)
        s.rect(cx - 17, min(y0 + sgn * 34, y0 + sgn * 52), 34, 18, 0.9, 0.8, fill=0.08)
        s.poly([(cx - 11, y0 + sgn * 52), (cx + 11, y0 + sgn * 52), (cx + 6, y0 + sgn * 62), (cx - 6, y0 + sgn * 62)], 0.7, 0.6)

    # collector wings on the horizontal axis
    for sgn in (-1, 1):
        x0 = cx + sgn * 350
        s.ln(x0, cy - 3, x0 + sgn * 300, cy - 3, 0.7, 0.6)
        s.ln(x0, cy + 3, x0 + sgn * 300, cy + 3, 0.7, 0.6)
        for k in range(5):
            px = x0 + sgn * (26 + k * 55)
            left = min(px, px + sgn * 46)
            for top in (cy - 78, cy + 14):
                s.rect(left, top, 46, 64, 0.75, 0.6, fill=0.04)
                for q in range(1, 4):
                    s.ln(left, top + q * 16, left + 46, top + q * 16, 0.28, 0.4)
                s.ln(left + 23, top, left + 23, top + 64, 0.28, 0.4)
        s.diamond(x0 + sgn * 308, cy, 5, 0.9, 0.7, fill=0.5, color=ARC)

    # callouts
    x, y = polar(cx, cy, 338, 310)
    s.leader(x, y, 70, -92, 120, "HABITAT RING", "36 COMPARTMENTS / 0.92 G")
    x, y = polar(cx, cy, 201, 210)
    s.leader(x, y, -150, -170, -110, "LIFT CAR", "TWIN TUBE / 6 OFF")
    s.leader(cx + 30, cy + 30, 120, 150, 110, "HUB", "ZERO-G BAY")
    s.leader(cx + 17, cy + 395, 120, 40, 120, "DOCKING ARM", "AXIAL / 2 OFF")
    s.dim(cx - 350, cy + 520, cx + 350, cy + 520, "Ø 1 400 M", a=0.4)
    s.ln(cx - 350, cy, cx - 350, cy + 526, 0.12, 0.4)
    s.ln(cx + 350, cy, cx + 350, cy + 526, 0.12, 0.4)

    s.title_block(92, s.H - 150, "RING STATION", "TYPE R-7   /   PLAN · ELEVATION · DETAIL",
                  ("GENERAL ARRANGEMENT", "ALL DIMENSIONS IN METRES", "REV 04"))
    s.view_label(cx + 470, cy + 470, "A", "PLAN", "SCALE 1 : 2 400", align="l")
    if not s.wide:
        return s

    # elevation, left
    ex, ey = s.cx - 960, cy - 40
    s.ln(ex - 250, ey, ex + 250, ey, 0.16, 0.5, dash=[18, 4, 3, 4])
    s.ln(ex, ey - 200, ex, ey + 200, 0.16, 0.5, dash=[18, 4, 3, 4])
    for sgn in (-1, 1):
        s.rect(min(ex + sgn * 152, ex + sgn * 176), ey - 13, 24, 26, 0.9, 0.9, fill=0.06)
        s.ln(ex + sgn * 26, ey - 4, ex + sgn * 152, ey - 4, 0.6, 0.6)
        s.ln(ex + sgn * 26, ey + 4, ex + sgn * 152, ey + 4, 0.6, 0.6)
        s.ln(ex + sgn * 176, ey, ex + sgn * 236, ey, 0.5, 0.6)
    s.rect(ex - 176, ey - 9, 352, 18, 0.35, 0.5)
    s.rect(ex - 26, ey - 86, 52, 172, 0.9, 1.0, fill=0.05)
    for k in range(-3, 4):
        s.ln(ex - 26, ey + k * 22, ex + 26, ey + k * 22, 0.3, 0.45)
    for sgn in (-1, 1):
        yb = ey + sgn * 86
        s.poly([(ex - 18, yb), (ex + 18, yb), (ex + 9, yb + sgn * 30), (ex - 9, yb + sgn * 30)], 0.8, 0.7)
        s.rect(ex - 12, min(yb + sgn * 30, yb + sgn * 44), 24, 14, 0.8, 0.7)
        s.ln(ex, yb + sgn * 44, ex, yb + sgn * 120, 0.5, 0.5)
        s.circ(ex, yb + sgn * 126, 6, 0.7, 0.6)
    s.dim(ex + 215, ey - 86, ex + 215, ey + 86, "310 M", a=0.4)
    s.view_label(ex, ey + 250, "B", "ELEVATION", "SCALE 1 : 4 800")

    # detail, right
    dx, dy = s.cx + 940, cy - 60
    s.circ(dx, dy, 150, 0.8, 0.9)
    s.ticks(dx, dy, 150, 72, 4, 0.35, 0.45, major=6, major_len=8)

    def clipc():
        s.c.new_sub_path()
        s.c.arc(dx, dy, 149, 0, 2 * math.pi)
    s.c.save()
    clipc()
    s.c.clip()
    ocx, ocy = dx - 80, dy + 1230
    for r, a, w in ((1150, 0.45, 0.6), (1190, 0.95, 1.3), (1320, 0.95, 1.3), (1360, 0.45, 0.6)):
        s.circ(ocx, ocy, r, a, w)
    s.circ(ocx, ocy, 1255, 0.25, 0.5, dash=[2, 5])
    for k in range(-6, 8):
        d = 270 + k * 3.2
        x1, y1 = polar(ocx, ocy, 1190, d)
        x2, y2 = polar(ocx, ocy, 1320, d)
        s.ln(x1, y1, x2, y2, 0.6, 0.6)
        if k % 2 == 0:
            x3, y3 = polar(ocx, ocy, 1232, d + 1.6)
            s.rect(x3 - 12, y3 - 9, 24, 18, 0.5, 0.5)

    def seg2():
        s.c.new_sub_path()
        s.c.arc(ocx, ocy, 1320, math.radians(270), math.radians(273.2))
        s.c.arc_negative(ocx, ocy, 1190, math.radians(273.2), math.radians(270))
        s.c.close_path()
    s.hatch(seg2, 5, 45, 0.4)
    s.c.restore()
    x, y = polar(cx, cy, 352, 335)
    ex2, ey2 = polar(dx, dy, 150, 172)
    s.ln(x, y, ex2, ey2, 0.22, 0.5, dash=[3, 4])
    s.circ(x - 9, y + 4, 16, 0.6, 0.6)
    s.view_label(dx, dy + 190, "C", "DETAIL", "SCALE 1 : 600")
    s.table(dx - 105, dy + 250, [
        ("RADIUS", "700 M"), ("SPIN", "1.08 RPM"), ("SEGMENTS", "36"),
        ("SPOKES", "6 × TWIN"), ("CREW", "4 200"), ("MASS", "2.1 × 10⁹ KG"),
    ])

    return s


# ---------------------------------------------------------------------------
# 02  Transfer orbit: two circular orbits and the half-ellipse between them
# ---------------------------------------------------------------------------

def transfer_orbit(size):
    s = start(size, 2, 22)
    px, py = s.cx - 40, s.cy - 5
    r1, r2 = 150, 420
    a_ = (r1 + r2) / 2
    c_ = a_ - r1
    b_ = math.sqrt(a_ * a_ - c_ * c_)
    lead = 44.2

    # reference rings
    s.circ(px, py, 520, 0.08, 0.5)
    s.circ(px, py, 478, 0.28, 0.5)
    s.ticks(px, py, 478, 180, 4, 0.3, 0.45, major=5, major_len=9)
    s.arc(px, py, 500, 98, 148, 0.7, 2.0)
    s.arc(px, py, 500, 152, 155, 0.7, 2.0)
    s.arc(px, py, 500, 300, 338, 0.4, 1.0)
    s.ln(px - 640, py, px + 640, py, 0.2, 0.5, dash=[18, 4, 3, 4])
    s.ln(px, py - 525, px, py + 525, 0.12, 0.5, dash=[18, 4, 3, 4])

    # a third, inclined orbit for depth
    s.ellipse(px + 30, py, 600, 205, rot=-17, a=0.2, w=0.5, dash=[2, 5])
    for d in (-17, 163):
        x, y = polar(px + 30, py, 600, d)
        s.rect(x - 4, y - 4, 8, 8, 0.6, 0.6)
    x, y = polar(px + 30, py, 600, -17)
    s.text("NODE 2", x + 12, y + 3, 6.5, a=0.45)

    # the two circular orbits
    s.circ(px, py, r1, 0.55, 0.7, dash=[6, 4])
    s.circ(px, py, r2, 0.4, 0.6)
    s.arc(px, py, r2, -180, -lead, 0.9, 1.5)

    # transfer ellipse: flown half solid, the rest dashed
    ex = px - c_
    s.ellipse(ex, py, a_, b_, a0=180, a1=360, a=0.95, w=1.4, color=ARC)
    s.ellipse(ex, py, a_, b_, a0=0, a1=180, a=0.35, w=0.6, dash=[3, 5])
    for t in range(200, 360, 20):
        t_ = math.radians(t)
        x, y = ex + a_ * math.cos(t_), py + b_ * math.sin(t_)
        nx, ny = b_ * math.cos(t_), a_ * math.sin(t_)
        n = math.hypot(nx, ny)
        s.ln(x - 5 * nx / n, y - 5 * ny / n, x + 5 * nx / n, y + 5 * ny / n, 0.8, 0.6, color=ARC)

    # primary body
    s.circ(px, py, 38, 0.95, 1.1, fill=0.06)

    def night():
        s.c.new_sub_path()
        s.c.arc(px, py, 38, math.radians(-60), math.radians(120))
        s.c.close_path()
    s.hatch(night, 3.5, 30, 0.4)
    s.ellipse(px, py, 38, 11, rot=-30, a0=0, a1=180, a=0.5, w=0.5)
    s.ln(*polar(px, py, 58, -120), *polar(px, py, 58, 60), 0.5, 0.5, dash=[8, 3, 2, 3])
    s.circ(px, py, 62, 0.25, 0.5, dash=[1.5, 3])

    # departure and arrival
    dxp, dyp = px + r1, py
    axp, ayp = px - r2, py
    s.diamond(dxp, dyp, 6, 0.95, 0.8, fill=0.9, color=GOLD)
    s.arrow(dxp, dyp - 10, dxp, dyp - 84, 0.9, 0.9, color=GOLD)
    s.diamond(axp, ayp, 6, 0.95, 0.8, fill=0.9, color=ARC)
    s.arrow(axp, ayp + 10, axp, ayp + 66, 0.9, 0.9, color=ARC)
    s.circ(axp, ayp, 15, 0.7, 0.6, dash=[3, 3])

    # target body at departure, and the lead angle
    tx, ty = polar(px, py, r2, -lead)
    s.circ(tx, ty, 10, 0.95, 1.0, fill=0.15)
    s.circ(tx, ty, 26, 0.35, 0.5)
    s.dot(*polar(tx, ty, 26, 200), 1.8, 0.9)
    s.ln(px, py, tx, ty, 0.3, 0.5, dash=[4, 4])
    s.arc(px, py, 96, -lead, 0, 0.8, 0.7)
    lx, ly = polar(px, py, 112, -lead / 2)
    s.text("44.2°", lx, ly + 3, 7.5, a=0.85)

    s.leader(dxp + 5, dyp - 50, 60, -40, 110, "BURN 01", "ΔV 2.94 KM/S  /  T+000 D")
    s.leader(axp - 4, ayp + 44, -50, 50, -120, "BURN 02", "ΔV 2.65 KM/S  /  T+259 D")
    s.leader(tx + 8, ty - 6, 60, -50, 120, "TARGET AT DEPARTURE", "LEAD ANGLE 44.2°")
    x, y = polar(px, py, r1, 130)
    s.leader(x, y, -40, 70, -100, "PARKING ORBIT", "R 1.00")
    x, y = ex + a_ * math.cos(math.radians(250)), py + b_ * math.sin(math.radians(250))
    s.leader(x, y, -50, -60, -110, "TRANSFER ARC", "A 1.90  /  E 0.474")
    s.text("R 2.80", px + r2 + 10, py - 7, 6.5, a=0.5)
    s.text("R 1.00", px + r1 + 12, py + 14, 6.5, a=0.5)

    s.title_block(92, s.H - 150, "TRANSFER ORBIT", "TRAJECTORY T-12   /   TWO-BURN MINIMUM ENERGY",
                  ("ECLIPTIC PLANE PROJECTION", "DISTANCES IN PARKING-ORBIT RADII", "REV 02"))
    if not s.wide:
        return s

    # speed along the arc, from the vis-viva equation
    def speed(t):
        ang = math.pi * t
        r = a_ * (1 - (c_ / a_) ** 2) / (1 + (c_ / a_) * math.cos(ang))
        v = math.sqrt(2 / r - 1 / a_)
        v0 = math.sqrt(2 / r1 - 1 / a_)
        return 0.08 + 0.84 * v / v0
    s.chart(s.cx - 1130, s.cy - 250, 330, 170, "SPEED ALONG ARC", speed, "TRUE ANOMALY 0 – 180°", "KM/S")
    s.table(s.cx - 1130, s.cy + 10, [
        ("DEPART", "T+000 D"), ("ARRIVE", "T+259 D"), ("ΔV TOTAL", "5.59 KM/S"),
        ("PERIAPSIS", "1.00"), ("APOAPSIS", "2.80"), ("WINDOW", "EVERY 780 D"),
    ])

    # further orbits running off the right edge
    for r, a, w, dash in ((700, 0.3, 0.6, None), (760, 0.16, 0.5, [2, 5]), (930, 0.22, 0.5, None)):
        s.arc(px, py, r, -28, 28, a, w, dash)
    s.ticks(px, py, 930, 41, 5, 0.3, 0.45, major=5, major_len=10, a0=-20, a1=20)
    bx, by = polar(px, py, 700, 11)
    s.circ(bx, by, 7, 0.9, 0.9, fill=0.12)
    s.circ(bx, by, 18, 0.3, 0.5)
    s.leader(bx + 6, by + 5, 40, 50, 110, "OUTER BODY", "NOT TO SCALE")
    s.view_label(s.cx + 880, s.cy - 300, "B", "OUTER SYSTEM", "R 4.6 – 6.2", align="l")
    return s


# ---------------------------------------------------------------------------
# 03  Confinement reactor: vertical section through the torus
# ---------------------------------------------------------------------------

def d_path(s, cx, cy, sign, x_in, x_out, h):
    """Add a D-shaped outline to the context: straight inner leg, bulging outer side."""
    X = (x_out - 0.25 * x_in) / 0.75
    s.c.move_to(cx + sign * x_in, cy - h)
    s.c.line_to(cx + sign * x_in, cy + h)
    s.c.curve_to(cx + sign * X, cy + h, cx + sign * X, cy - h, cx + sign * x_in, cy - h)
    s.c.close_path()


def reactor(size):
    s = start(size, 3, 33)
    cx, cy = s.cx, s.cy - 20

    # framing arcs
    for a0, a1 in ((150, 210), (-30, 30)):
        s.arc(cx, cy, 560, a0, a1, 0.3, 0.5)
        s.ticks(cx, cy, 560, 61, 4, 0.3, 0.45, major=5, major_len=9, a0=a0, a1=a1)
    s.arc(cx, cy, 582, 156, 176, 0.7, 2.0)
    s.arc(cx, cy, 582, 4, 14, 0.7, 2.0)
    s.ln(cx, cy - 470, cx, cy + 470, 0.3, 0.5, dash=[18, 4, 3, 4])
    s.ln(cx - 640, cy, cx + 640, cy, 0.14, 0.5, dash=[18, 4, 3, 4])

    # cryostat: chamfered double shell
    for k, a, w in ((0, 0.8, 1.0), (8, 0.35, 0.5)):
        X, Y, ch = 500 - k, 390 - k, 70
        s.poly([(cx - X + ch, cy - Y), (cx + X - ch, cy - Y), (cx + X, cy - Y + ch), (cx + X, cy + Y - ch),
                (cx + X - ch, cy + Y), (cx - X + ch, cy + Y), (cx - X, cy + Y - ch), (cx - X, cy - Y + ch)], a, w)

    # floor and supports
    s.ln(cx - 620, cy + 420, cx + 620, cy + 420, 0.7, 0.8)
    for k in range(-31, 31):
        s.ln(cx + k * 20, cy + 420, cx + k * 20 - 10, cy + 432, 0.3, 0.45)
    for x in (-380, -240, 240, 380):
        s.rect(cx + x - 9, cy + 390, 18, 30, 0.7, 0.6, fill=0.06)

    for sign in (-1, 1):
        # field coil: hatched band between two D outlines
        def coil(sign=sign):
            d_path(s, cx, cy, sign, 62, 408, 306)
            d_path(s, cx, cy, sign, 92, 372, 270)
        s.c.save()
        s.c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        s.hatch(coil, 5, 45 * sign, 0.35)
        s.c.restore()
        for dims, a, w in (((62, 408, 306), 0.95, 1.2), ((92, 372, 270), 0.95, 1.0),
                           ((106, 352, 252), 0.6, 0.6), ((114, 342, 243), 0.6, 0.6),
                           ((130, 322, 224), 0.85, 0.8)):
            d_path(s, cx, cy, sign, *dims)
            s._stroke(a, w, None, WHITE)
        d_path(s, cx, cy, sign, 114, 342, 243)
        s._ink(0.05, WHITE)
        s.c.fill()
        # blanket modules between vessel and first wall
        for k in range(-6, 7):
            yy = cy + k * 32
            s.ln(cx + sign * 114, yy, cx + sign * 130, yy, 0.45, 0.45)

        # flux surfaces
        R0, kappa, delta = 224, 1.72, 0.42
        for i, am in enumerate((10, 24, 38, 52, 66, 80)):
            pts = []
            for q in range(0, 361, 4):
                t = math.radians(q)
                x = R0 + am * math.cos(t + delta * math.sin(t))
                y = kappa * am * math.sin(t)
                pts.append((cx + sign * x, cy + y))
            s.poly(pts, 0.35 + 0.1 * i, 0.6 if i < 5 else 1.2, color=ARC, fill=0.03)
        s.cross(cx + sign * R0, cy, 6, 0.9, 0.6, color=ARC)
        # exhaust target under the plasma
        s.poly([(cx + sign * 160, cy + 196), (cx + sign * 190, cy + 214), (cx + sign * 206, cy + 186),
                (cx + sign * 224, cy + 214), (cx + sign * 262, cy + 190)], 0.85, 0.9, close=False)

        # ring coils outside the field coil
        for x, y in ((150, -346), (330, -292), (442, -130), (442, 130), (330, 292), (150, 346)):
            bx, by = cx + sign * x - 17, cy + y - 17
            s.rect(bx, by, 34, 34, 0.9, 0.8, fill=0.06)
            s.ln(bx, by, bx + 34, by + 34, 0.4, 0.45)
            s.ln(bx + 34, by, bx, by + 34, 0.4, 0.45)

        # midplane port through the cryostat
        x0, x1 = cx + sign * 408, cx + sign * 600
        s.ln(x0, cy - 20, x1, cy - 20, 0.8, 0.7)
        s.ln(x0, cy + 20, x1, cy + 20, 0.8, 0.7)
        for fx in (500, 520, 600):
            s.ln(cx + sign * fx, cy - 28, cx + sign * fx, cy + 28, 0.8, 0.8)

    # central column: stacked windings
    s.rect(cx - 46, cy - 300, 92, 600, 0.95, 1.1, fill=0.05)
    for k in range(1, 6):
        s.ln(cx - 46, cy - 300 + k * 100, cx + 46, cy - 300 + k * 100, 0.8, 0.7)
    yy = cy - 296
    while yy < cy + 300:
        s.ln(cx - 40, yy, cx - 8, yy, 0.25, 0.4)
        s.ln(cx + 8, yy, cx + 40, yy, 0.25, 0.4)
        yy += 6

    s.leader(cx + 224, cy - 60, 250, -330, 120, "PLASMA", "FLUX SURFACES / Q 1 – 3")
    s.leader(cx - 388, cy - 120, -170, -200, -110, "FIELD COIL", "18 OFF / 11.8 T")
    s.leader(cx - 30, cy + 250, -330, 210, -110, "CENTRAL COLUMN", "6 MODULES")
    s.leader(cx + 442, cy + 130, 120, 110, 100, "RING COIL", "6 PAIRS")
    s.leader(cx + 224, cy + 210, 190, 250, 110, "EXHAUST TARGET", "10 MW / M²")
    s.leader(cx - 560, cy - 20, -40, -70, -100, "HEATING PORT", "33 MW")
    s.dim(cx, cy - 430, cx + 224, cy - 430, "R 6.20 M", a=0.45)
    s.dim(cx + 650, cy - 306, cx + 650, cy + 306, "13.4 M", a=0.4)

    s.title_block(92, s.H - 150, "CONFINEMENT REACTOR", "UNIT C-3   /   VERTICAL SECTION A–A",
                  ("MAGNETIC CONFINEMENT, D-SHAPED CROSS-SECTION", "ALL DIMENSIONS IN METRES", "REV 07"))
    if not s.wide:
        return s

    # plan view, left
    qx, qy = s.cx - 990, cy - 50
    for r, a, w, dash in ((34, 0.9, 0.9, None), (56, 0.5, 0.5, None), (96, 0.5, 0.5, None),
                          (198, 0.5, 0.5, None), (236, 0.8, 0.9, None), (244, 0.35, 0.5, None)):
        s.circ(qx, qy, r, a, w, dash)
    s.circ(qx, qy, 148, 0.9, 1.0, dash=[5, 3], color=ARC)
    for k in range(18):
        s.band(qx, qy, 46, 210, k * 20 - 3, k * 20 + 3, 0.7, 0.6, fill=0.06)
    s.ln(qx - 264, qy, qx + 264, qy, 0.6, 0.6, dash=[18, 4, 3, 4])
    for sign in (-1, 1):
        s.arrow(qx + sign * 264, qy, qx + sign * 264, qy - 26, 0.8, 0.7)
        s.text("A", qx + sign * 264, qy - 34, 9, track=0, a=0.9, align="c", bold=True)
    s.view_label(qx, qy + 300, "B", "PLAN", "SCALE 1 : 400")

    # right: profile chart and figures
    s.chart(s.cx + 800, cy - 260, 330, 170, "PRESSURE PROFILE",
            lambda t: 0.06 + 0.86 * (1 - t * t) ** 1.6 + (0.08 * math.exp(-((t - 0.93) / 0.04) ** 2)),
            "MINOR RADIUS 0 – 2.0 M", "KPA")
    s.table(s.cx + 800, cy + 0, [
        ("MAJOR R", "6.20 M"), ("MINOR R", "2.00 M"), ("FIELD", "5.3 T ON AXIS"),
        ("CURRENT", "15 MA"), ("VOLUME", "840 M³"), ("OUTPUT", "500 MW"), ("PULSE", "400 S"),
    ])
    return s


# ---------------------------------------------------------------------------
# 04  Survey probe: side elevation, antenna plan, truss detail
# ---------------------------------------------------------------------------

def truss(s, x1, y1, x2, y2, depth=10, bay=20, a=0.7):
    """Two chords with a zigzag between them."""
    L = math.hypot(x2 - x1, y2 - y1)
    s.c.save()
    s.c.translate(x1, y1)
    s.c.rotate(math.atan2(y2 - y1, x2 - x1))
    s.ln(0, -depth / 2, L, -depth / 2, a, 0.7)
    s.ln(0, depth / 2, L, depth / 2, a, 0.7)
    n = max(1, int(L // bay))
    step = L / n
    for i in range(n):
        s.ln(i * step, depth / 2 if i % 2 else -depth / 2, (i + 1) * step, -depth / 2 if i % 2 else depth / 2, a * 0.6, 0.45)
        s.ln(i * step, -depth / 2, i * step, depth / 2, a * 0.6, 0.45)
    s.ln(L, -depth / 2, L, depth / 2, a * 0.6, 0.45)
    s.c.restore()


def probe(size):
    s = start(size, 4, 44)
    cx, cy = s.cx + 40, s.cy + 30

    s.ln(cx, cy - 470, cx, cy + 330, 0.22, 0.5, dash=[18, 4, 3, 4])
    s.circ(cx, cy - 60, 430, 0.10, 0.5)
    s.arc(cx, cy - 60, 430, 205, 335, 0.3, 0.5)
    s.ticks(cx, cy - 60, 430, 66, 4, 0.3, 0.45, major=5, major_len=9, a0=205, a1=335)
    s.arc(cx, cy - 60, 452, 212, 250, 0.7, 2.0)
    s.arc(cx, cy - 60, 452, 254, 257, 0.7, 2.0)

    # beam cone above the antenna
    apex = (cx, cy - 262)
    for sgn in (-1, 1):
        s.fade_ln(apex[0], apex[1], apex[0] + sgn * 70, apex[1] - 230, 0.6, 0.0, 0.6, ARC)
    for r in (70, 130, 190):
        s.arc(apex[0], apex[1], r, -107, -73, 0.5 - r / 500, 0.6, color=ARC)

    # dish
    hw, rim_y, vert_y = 236, cy - 150, cy - 56

    def dish_y(x, off=0.0):
        return vert_y + off - (vert_y - rim_y) * (x / hw) ** 2
    s.poly([(cx + x, dish_y(x)) for x in range(-hw, hw + 1, 4)], 0.95, 1.3, close=False)
    s.poly([(cx + x, dish_y(x, 7)) for x in range(-hw + 8, hw - 7, 4)], 0.5, 0.5, close=False)
    for x in range(-200, 201, 50):
        s.ln(cx + x, dish_y(x), cx + x, dish_y(x, 7), 0.5, 0.45)
    s.ln(cx - hw, rim_y, cx + hw, rim_y, 0.2, 0.45, dash=[2, 4])
    for sgn in (-1, 1):
        s.ln(cx + sgn * 210, dish_y(210), cx + sgn * 12, apex[1] + 8, 0.7, 0.6)
        s.ln(cx + sgn * 70, dish_y(70, 7), cx + sgn * 56, cy - 10, 0.7, 0.6)
        s.ln(cx + sgn * 150, dish_y(150, 7), cx + sgn * 70, cy - 4, 0.5, 0.5)
    s.ellipse(cx, apex[1] + 8, 24, 6, a=0.9, w=0.9)
    s.poly([(cx - 7, vert_y), (cx - 13, vert_y - 34), (cx + 13, vert_y - 34), (cx + 7, vert_y)], 0.85, 0.7)

    # bus
    s.poly([(cx - 78, cy - 10), (cx + 78, cy - 10), (cx + 78, cy + 96), (cx - 78, cy + 96)], 0.95, 1.2, fill=0.05)
    for x in (-26, 26):
        s.ln(cx + x, cy - 10, cx + x, cy + 96, 0.5, 0.5)
    s.circ(cx, cy + 43, 40, 0.4, 0.5, dash=[4, 3])
    for k in range(8):
        s.ln(cx + 34, cy + 4 + k * 11, cx + 70, cy + 4 + k * 11, 0.45, 0.45)
    for sx, sy in ((-78, -10), (78, -10), (-78, 96), (78, 96)):
        sgn = 1 if sx > 0 else -1
        s.poly([(cx + sx, cy + sy - 5), (cx + sx + sgn * 12, cy + sy - 9), (cx + sx + sgn * 12, cy + sy + 9), (cx + sx, cy + sy + 5)], 0.7, 0.6)

    # engine bell
    for sgn in (-1, 1):
        s.bez((cx + sgn * 16, cy + 110), (cx + sgn * 22, cy + 140), (cx + sgn * 40, cy + 160), (cx + sgn * 48, cy + 186), 0.9, 0.9)
    s.rect(cx - 16, cy + 96, 32, 14, 0.8, 0.7)
    s.ln(cx - 48, cy + 186, cx + 48, cy + 186, 0.9, 0.9)
    for k in range(1, 4):
        s.ln(cx - 18 - k * 8, cy + 118 + k * 17, cx + 18 + k * 8, cy + 118 + k * 17, 0.3, 0.45)

    # long boom, left, with two field sensors
    truss(s, cx - 78, cy + 30, cx - 660, cy + 30)
    for x in (cx - 400, cx - 694):
        s.rect(x, cy + 21, 34, 18, 0.9, 0.8, fill=0.1)
    # instrument platform, right
    truss(s, cx + 78, cy + 20, cx + 330, cy + 20)
    s.rect(cx + 330, cy - 24, 96, 88, 0.95, 1.0, fill=0.05)
    s.rect(cx + 426, cy - 14, 60, 22, 0.85, 0.7)
    s.ellipse(cx + 486, cy - 3, 4, 11, a=0.85, w=0.7)
    s.rect(cx + 426, cy + 24, 40, 16, 0.85, 0.7)
    s.ellipse(cx + 466, cy + 32, 3, 8, a=0.85, w=0.7)
    s.rect(cx + 352, cy - 52, 30, 28, 0.7, 0.6)
    s.arc(cx + 378, cy + 20, 140, -22, 22, 0.35, 0.5, dash=[3, 3])
    # power unit on a slanted boom
    x1, y1, x2, y2 = cx + 78, cy + 86, cx + 290, cy + 222
    truss(s, x1, y1, x2, y2, depth=8, bay=18)
    s.c.save()
    s.c.translate(x2, y2)
    s.c.rotate(math.atan2(y2 - y1, x2 - x1))
    s.rect(0, -15, 150, 30, 0.95, 1.0, fill=0.06)
    for k in range(1, 15):
        s.ln(k * 10, -26, k * 10, 26, 0.6, 0.5)
    s.rect(150, -8, 12, 16, 0.8, 0.7)
    s.c.restore()
    # wire antennas
    for ex_, ey_ in ((cx - 400, cy + 330), (cx - 250, cy + 380)):
        s.ln(cx - 70, cy + 96, ex_, ey_, 0.6, 0.5)
        s.dot(ex_, ey_, 1.8, 0.8)

    s.leader(cx - 170, dish_y(-170), -150, -130, -120, "HIGH-GAIN ANTENNA", "Ø 3.8 M / X AND KA BAND")
    s.leader(cx + 8, apex[1] + 6, 150, -60, 120, "SUBREFLECTOR", None)
    s.leader(cx - 560, cy + 24, -30, -110, -110, "FIELD SENSOR BOOM", "11.6 M / 2 SENSORS")
    s.leader(cx + 456, cy - 14, 70, -110, 120, "INSTRUMENT PLATFORM", "2-AXIS SCAN")
    s.leader(cx + 374, cy + 276, 90, 60, 120, "POWER UNIT", "RADIOISOTOPE / 420 W")
    s.leader(cx + 40, cy + 170, 70, 90, 110, "MAIN ENGINE", "445 N")
    s.leader(cx - 235, cy + 213, -90, -60, -110, "WIRE ANTENNA", "10 M / 2 OFF")
    s.dim(cx - 694, cy + 440, cx + 486, cy + 440, "23.6 M", a=0.4)
    s.ln(cx - 694, cy + 44, cx - 694, cy + 446, 0.12, 0.4)
    s.ln(cx + 486, cy + 44, cx + 486, cy + 446, 0.12, 0.4)

    s.title_block(92, s.H - 150, "SURVEY PROBE", "CLASS S-2   /   ELEVATION · ANTENNA PLAN · DETAIL",
                  ("CRUISE CONFIGURATION, BOOMS DEPLOYED", "ALL DIMENSIONS IN METRES", "REV 03"))
    if not s.wide:
        return s

    # antenna plan, right
    qx, qy = s.cx + 960, s.cy - 110
    for r, a, w, dash in ((170, 0.95, 1.2, None), (163, 0.45, 0.5, None), (112, 0.4, 0.5, None),
                          (56, 0.4, 0.5, [3, 3]), (17, 0.9, 0.9, None)):
        s.circ(qx, qy, r, a, w, dash)
    for k in range(24):
        s.ln(*polar(qx, qy, 17, k * 15), *polar(qx, qy, 163, k * 15), 0.3, 0.45)
    for d in (90, 210, 330):
        s.ln(*polar(qx, qy, 150, d), *polar(qx, qy, 17, d), 0.9, 0.9)
    s.poly([polar(qx, qy, 60, 36 * k + 18) for k in range(10)], 0.45, 0.5, dash=[4, 3])
    s.ticks(qx, qy, 176, 72, 4, 0.3, 0.45, major=6, major_len=8)
    s.view_label(qx, qy + 225, "B", "ANTENNA PLAN", "SCALE 1 : 40")
    s.table(qx - 105, qy + 285, [
        ("DRY MASS", "815 KG"), ("PROPELLANT", "1 120 KG"), ("POWER", "420 W"),
        ("DATA RATE", "115 KBIT/S"), ("DESIGN LIFE", "20 YEARS"),
    ])

    # truss detail, left
    dx, dy = s.cx - 980, s.cy - 190
    s.circ(dx, dy, 130, 0.8, 0.9)
    s.ticks(dx, dy, 130, 72, 4, 0.35, 0.45, major=6, major_len=8)
    s.c.save()
    s.c.new_sub_path()
    s.c.arc(dx, dy, 129, 0, 2 * math.pi)
    s.c.clip()
    for yy in (dy - 40, dy + 40):
        s.ln(dx - 140, yy - 3, dx + 140, yy - 3, 0.9, 0.9)
        s.ln(dx - 140, yy + 3, dx + 140, yy + 3, 0.9, 0.9)
    for k in range(-2, 3):
        x = dx + k * 80
        s.ln(x, dy - 37, x, dy + 37, 0.7, 0.7)
        s.ln(x, dy - 37 if k % 2 else dy + 37, x + 80, dy + 37 if k % 2 else dy - 37, 0.7, 0.7)
        for yy in (dy - 40, dy + 40):
            s.circ(x, yy, 7, 0.95, 0.9, fill=0.2)
    s.c.restore()
    s.ln(dx + 92, dy + 92, cx - 520, cy + 22, 0.22, 0.5, dash=[3, 4])
    s.circ(cx - 520, cy + 30, 16, 0.6, 0.6)
    s.view_label(dx, dy + 170, "C", "BOOM JOINT", "SCALE 1 : 4")
    return s


# ---------------------------------------------------------------------------
# 05  Ion drive: section along the axis, grid face
# ---------------------------------------------------------------------------

def ion_drive(size):
    s = start(size, 5, 55)
    cx, cy = s.cx - 60, s.cy - 10

    s.ln(cx - 720, cy, cx + 1100, cy, 0.3, 0.5, dash=[18, 4, 3, 4])
    gx = cx + 150  # face of the last grid

    # exhaust beam
    for k in range(-11, 12):
        s.fade_ln(gx, cy + k * 9.5, gx + 760, cy + k * 9.5 + k * 24, 0.75 - abs(k) * 0.03, 0.0, 0.6, ARC)
    for sgn in (-1, 1):
        s.ln(gx, cy + sgn * 108, gx + 700, cy + sgn * 108 + sgn * 290, 0.3, 0.5, dash=[6, 4])
    for r, lab in ((220, "0.5 M"), (440, "1.0 M"), (660, "1.5 M")):
        s.arc(gx - 250, cy, r + 250, -21, 21, 0.3, 0.5)
        x, y = polar(gx - 250, cy, r + 250, -22.5)
        s.text(lab, x, y, 6.5, a=0.45, align="c")

    # tank: capsule with a double wall
    tl, tr, rad = cx - 660, cx - 340, 100
    for k, a, w in ((0, 0.95, 1.2), (7, 0.5, 0.5)):
        r = rad - k
        s.c.new_sub_path()
        s.c.arc(tl + rad, cy, r, math.radians(90), math.radians(270))
        s.c.arc(tr - rad, cy, r, math.radians(270), math.radians(90))
        s.c.close_path()
        if k == 0:
            s._ink(0.04, WHITE)
            s.c.fill_preserve()
        s._stroke(a, w, None, WHITE)
    s.ellipse((tl + tr) / 2, cy, 120, 70, a=0.35, w=0.5, dash=[4, 3])
    for x in (tl + rad, (tl + tr) / 2, tr - rad):
        s.ln(x, cy - rad + 7, x, cy + rad - 7, 0.35, 0.5)
    for sgn in (-1, 1):
        s.rect(tl + 120, cy + sgn * rad - (12 if sgn < 0 else 0), 80, 12, 0.7, 0.6)

    # feed line with a valve and a regulator
    s.ln(tr, cy - 4, cx - 200, cy - 4, 0.8, 0.6)
    s.ln(tr, cy + 4, cx - 200, cy + 4, 0.8, 0.6)
    vx = cx - 300
    s.poly([(vx - 12, cy - 10), (vx + 12, cy + 10), (vx + 12, cy - 10), (vx - 12, cy + 10)], 0.9, 0.7, fill=0.12)
    s.ln(vx, cy, vx, cy - 22, 0.8, 0.6)
    s.rect(vx - 8, cy - 30, 16, 8, 0.8, 0.6)
    s.rect(cx - 262, cy - 13, 34, 26, 0.9, 0.8, fill=0.08)

    # gimbal ring
    for sgn in (-1, 1):
        s.rect(cx - 236, cy + sgn * 150 - 10, 20, 20, 0.7, 0.6)
        s.circ(cx - 226, cy + sgn * 150, 5, 0.9, 0.7)
        s.ln(cx - 226, cy + sgn * 140, cx - 226, cy + sgn * 40, 0.4, 0.5, dash=[4, 3])

    # discharge chamber: hatched walls and back plate
    x0, x1, ri, ro = cx - 200, cx + 118, 110, 125
    for top in (cy - ro, cy + ri):
        def wall(top=top):
            s.c.rectangle(x0, top, x1 - x0, ro - ri)
        s.hatch(wall, 4.5, 45, 0.4)
        s.rect(x0, top, x1 - x0, ro - ri, 0.95, 1.0)

    def back():
        s.c.rectangle(x0, cy - ri, 15, 2 * ri)
    s.hatch(back, 4.5, -45, 0.4)
    s.rect(x0, cy - ri, 15, 2 * ri, 0.95, 1.0)
    s.rect(x0 + 15, cy - 9, 64, 18, 0.9, 0.8, fill=0.1)
    s.poly([(x0 + 79, cy - 9), (x0 + 92, cy - 4), (x0 + 92, cy + 4), (x0 + 79, cy + 9)], 0.9, 0.8)
    s.rect(x0 + 15, cy - 16, 26, 32, 0.6, 0.5)

    # magnet rings and the field between them
    mags = (x0 + 8, x0 + 138, x0 + 268)
    for sgn in (-1, 1):
        for mx in mags:
            top = cy + sgn * (ro + 4) - (28 if sgn < 0 else 0)
            s.rect(mx, top, 44, 28, 0.9, 0.8, fill=0.06)
            s.ln(mx, top, mx + 44, top + 28, 0.4, 0.45)
            s.ln(mx + 44, top, mx, top + 28, 0.4, 0.45)
        for a_, b_ in zip(mags, mags[1:]):
            for depth, al in ((40, 0.55), (62, 0.4), (84, 0.25)):
                y0 = cy + sgn * ri
                s.bez((a_ + 22, y0), (a_ + 22, y0 - sgn * depth * 1.3), (b_ + 22, y0 - sgn * depth * 1.3), (b_ + 22, y0),
                      al, 0.55, color=ARC)

    # grids
    for i, (x, a, w) in enumerate(((x1 + 8, 0.95, 1.6), (x1 + 20, 0.95, 1.6), (x1 + 32, 0.7, 1.2))):
        s.ln(x, cy - ri + 2, x, cy + ri - 2, a, w, dash=[5, 2.5])
    for sgn in (-1, 1):
        top = cy + sgn * ri - (0 if sgn > 0 else 34)
        s.rect(x1, top, 44, 34, 0.9, 0.8, fill=0.08)
    # outer shroud
    for sgn in (-1, 1):
        s.poly([(tr - 30, cy + sgn * 96), (cx - 250, cy + sgn * 176), (x1 + 20, cy + sgn * 176),
                (x1 + 56, cy + sgn * 150)], 0.6, 0.6, close=False)
        s.ln(cx - 250, cy + sgn * 170, x1 + 20, cy + sgn * 170, 0.25, 0.45, dash=[2, 3])

    # neutraliser above the beam
    s.c.save()
    s.c.translate(x1 + 70, cy - 196)
    s.c.rotate(math.radians(35))
    s.rect(-40, -8, 60, 16, 0.9, 0.8, fill=0.1)
    s.poly([(20, -8), (32, -3), (32, 3), (20, 8)], 0.9, 0.8)
    s.c.restore()
    s.bez((x1 + 96, cy - 178), (x1 + 130, cy - 150), (x1 + 170, cy - 110), (x1 + 260, cy - 60), 0.55, 0.6, dash=[2, 3], color=GOLD)

    s.leader((tl + tr) / 2 - 40, cy - 60, -60, -130, -120, "PROPELLANT TANK", "XENON / 1 450 KG")
    s.leader(vx, cy - 26, 20, -150, 110, "LATCH VALVE", None)
    s.leader(x0 + 50, cy + 6, -30, 210, -110, "CATHODE", "HOLLOW / 13 A")
    s.leader(mags[1] + 22, cy - ro - 20, 110, -175, 120, "MAGNET RING", "3 OFF / 0.01 T AT GRID")
    s.leader(x1 + 20, cy + 60, 60, 190, 120, "GRID SET", "SCREEN · ACCEL · DECEL")
    s.leader(x1 + 62, cy - 200, 50, -50, 120, "NEUTRALISER", "ELECTRON RETURN")
    s.leader(gx + 380, cy + 80, 60, 200, 120, "ION BEAM", "1 800 V / 15° HALF ANGLE")
    s.dim(x0, cy - 250, x1 + 44, cy - 250, "362 MM", a=0.45)
    s.ln(x0, cy - ro, x0, cy - 256, 0.12, 0.4)
    s.ln(x1 + 44, cy - ri - 34, x1 + 44, cy - 256, 0.12, 0.4)
    s.dim(tl, cy + 270, x1 + 44, cy + 270, "1 568 MM", a=0.4)
    s.ln(tl, cy, tl, cy + 276, 0.12, 0.4)
    s.ln(x1 + 44, cy + ri + 34, x1 + 44, cy + 276, 0.12, 0.4)

    s.title_block(92, s.H - 150, "ION DRIVE", "MODEL E-40   /   AXIAL SECTION · GRID FACE",
                  ("GRIDDED ELECTROSTATIC THRUSTER", "ALL DIMENSIONS IN MILLIMETRES", "REV 05"))
    if not s.wide:
        return s

    # grid face, left
    qx, qy = s.cx - 1000, s.cy - 170
    s.circ(qx, qy, 150, 0.9, 1.1)
    s.circ(qx, qy, 134, 0.5, 0.5)
    s.circ(qx, qy, 122, 0.9, 0.9, fill=0.04)
    for k in range(12):
        x, y = polar(qx, qy, 142, k * 30)
        s.circ(x, y, 3.2, 0.85, 0.6)
    s.c.save()
    s.c.new_sub_path()
    s.c.arc(qx, qy, 120, 0, 2 * math.pi)
    s.c.clip()
    pitch = 7.5
    row = 0
    y = qy - 126
    while y < qy + 126:
        x = qx - 126 + (pitch / 2 if row % 2 else 0)
        while x < qx + 126:
            s.c.new_sub_path()
            s.c.arc(x, y, 1.5, 0, 2 * math.pi)
            x += pitch
        y += pitch * 0.866
        row += 1
    s._ink(0.55, WHITE)
    s.c.fill()
    s.c.restore()
    s.cross(qx, qy, 160, 0.18, 0.45)
    s.view_label(qx, qy + 200, "B", "GRID FACE", "Ø 220 MM / 14 800 APERTURES")

    s.table(s.cx + 880, s.cy + 250, [
        ("THRUST", "236 MN"), ("SPECIFIC IMP.", "4 100 S"), ("INPUT POWER", "6.9 KW"),
        ("BEAM VOLTAGE", "1 800 V"), ("EFFICIENCY", "68 %"), ("LIFE", "50 000 H"),
    ], key_w=104)
    return s


# ---------------------------------------------------------------------------
# 06  Datum figure: a quiet sheet, polygons inscribed in one circle
# ---------------------------------------------------------------------------

def datum(size):
    s = start(size, 6, 66)
    cx, cy = s.cx + 420, s.cy - 10
    R = 340

    s.ln(60, cy, s.W - 60, cy, 0.2, 0.5, dash=[18, 4, 3, 4])
    s.ln(cx, cy - 500, cx, cy + 500, 0.2, 0.5, dash=[18, 4, 3, 4])
    s.circ(cx, cy, R, 0.9, 1.1)
    s.circ(cx, cy, R + 40, 0.22, 0.5, dash=[2, 5])
    s.circ(cx, cy, R + 72, 0.3, 0.5)
    s.ticks(cx, cy, R + 72, 360, 5, 0.3, 0.45, major=10, major_len=11)
    s.circ(cx, cy, R + 150, 0.08, 0.5)
    s.arc(cx, cy, R + 120, 190, 250, 0.75, 2.2)
    s.arc(cx, cy, R + 120, 255, 259, 0.75, 2.2)
    s.arc(cx, cy, R + 120, 30, 62, 0.4, 1.0)

    for n, a in ((3, 0.85), (4, 0.55), (5, 0.42), (6, 0.34), (8, 0.24), (12, 0.16)):
        pts = [polar(cx, cy, R, -90 + 360 * k / n) for k in range(n)]
        s.poly(pts, a, 0.9 if n == 3 else 0.55, fill=0.02 if n == 3 else 0.0,
               color=ARC if n == 3 else WHITE)
    hexp = [polar(cx, cy, R, -90 + 60 * k) for k in range(6)]
    for i in range(6):
        for j in range(i + 2, 6):
            if (i, j) != (0, 5):
                s.ln(*hexp[i], *hexp[j], 0.14, 0.45)
    s.circ(cx, cy, R / 2, 0.5, 0.6)
    s.circ(cx, cy, R / 2 * 0.5, 0.3, 0.5, dash=[3, 3])
    for k, p in enumerate(hexp):
        s.diamond(p[0], p[1], 4.5, 0.95, 0.7, fill=0.9)
        lx, ly = polar(cx, cy, R + 22, -90 + 60 * k)
        s.text(f"P{k + 1:02d}", lx, ly + 3, 6.5, a=0.55, align="c")
    s.cross(cx, cy, 9, 0.9, 0.6)
    s.circ(cx, cy, 4, 0.9, 0.7)
    s.leader(*polar(cx, cy, R / 2, 140), -260, 200, -110, "INSCRIBED CIRCLE", "R / 2")
    s.dim(cx, cy + R + 130, cx + R, cy + R + 130, "R 1.000", a=0.4)

    s.title_block(92, s.H - 150, "DATUM FIGURE", "REFERENCE D-0   /   REGULAR POLYGONS, N = 3 · 4 · 5 · 6 · 8 · 12",
                  ("COMMON CIRCUMCIRCLE", "UNIT RADIUS", "REV 01"))
    return s


SHEETS = [
    ("01-ring-station", ring_station),
    ("02-transfer-orbit", transfer_orbit),
    ("03-confinement-reactor", reactor),
    ("04-survey-probe", probe),
    ("05-ion-drive", ion_drive),
    ("06-datum-figure", datum),
]
