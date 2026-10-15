"""Five more devices, this time for fun: racing, shows, games, smell, athletics.

Same rules as devices.py: a real job, breakthroughs that have not happened
yet, plausible within about fifty years. Nothing here saves the world.
"""

import math
import micro_details
from hardware3d.secondary_drawing import view as hardware_view
from hardware3d.accessories import rounded as cast_outline

from devices import centres, framing, start, truss
from fidelity import enrich, contour, hand, front_head, anatomical_segment, joint_chain
from sheet import ARC, GOLD, WHITE, polar
from hardware3d.accessories import rounded


# ---------------------------------------------------------------------------
# Sky racer
# ---------------------------------------------------------------------------

def sky_racer(size):
    s = start(size, "sky-racer", 707)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my, 478, a0=100, thick=(205, 250), thin=(330, 372))
    from hardware3d.family_drawing import enabled as hardware_enabled, draw as draw_hardware
    if hardware_enabled('sky-racer'):
        draw_hardware(s, 'sky-racer', mx, my)
        c = s.c
    else:
        c = s.c

        # the envelope the flight computer keeps clear
        s.circ(mx, my, 440, 0.4, 0.6, dash=[5, 4], color=ARC)
        fans = [(sgn * fx, fy, r) for fx, fy, r in ((215, -185, 88), (305, 15, 98), (215, 215, 88)) for sgn in (-1, 1)]
        sensors = [(0, -196, -90), (0, 186, 90)] + [(fx + math.copysign(r, fx), fy, 0 if fx > 0 else 180) for fx, fy, r in fans]
        for ox, oy, d in sensors:
            for spread in (-16, 0, 16):
                s.fade_ln(mx + ox, my + oy, *polar(mx + ox, my + oy, 130, d + spread), 0.5, 0.0, 0.5, ARC)
            s.dot(mx + ox, my + oy, 2.4, 0.95, ARC)

        # arms
        for fx, fy, r in fans:
            sgn = 1 if fx > 0 else -1
            p1 = (mx + sgn * 44, my + fy * 0.35)
            ang = math.atan2(my + fy - p1[1], mx + fx - p1[0])
            p2 = (mx + fx - r * math.cos(ang), my + fy - r * math.sin(ang))
            nx, ny = -math.sin(ang) * 5, math.cos(ang) * 5
            for k in (-1, 1):
                s.ln(p1[0] + k * nx, p1[1] + k * ny, p2[0] + k * nx, p2[1] + k * ny, 0.85, 0.8)
            mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
            s.circ(mid[0], mid[1], 6, 0.8, 0.6, fill=0.2)

        # ducted fans, rim-driven
        for i, (fx, fy, r) in enumerate(fans):
            x, y = mx + fx, my + fy
            s.circ(x, y, r, 0.95, 1.3, fill=0.04)
            s.circ(x, y, r - 9, 0.5, 0.5)
            s.circ(x, y, r - 4.5, 0.85, 1.8, dash=[6, 3], color=ARC)
            turn = 1 if i % 2 else -1
            for k in range(7):
                d = k * 360 / 7 + i * 13
                # Both edges of an aerofoil, with a tapered root and swept tip.
                c.move_to(*polar(x,y,15,d))
                c.curve_to(*polar(x,y,r*.45,d+turn*10), *polar(x,y,r*.75,d+turn*26), *polar(x,y,r-10,d+turn*40))
                c.line_to(*polar(x,y,r-10,d+turn*49))
                c.curve_to(*polar(x,y,r*.72,d+turn*46), *polar(x,y,r*.38,d+turn*35), *polar(x,y,15,d+turn*22))
                c.close_path()
                s._ink(.10,WHITE); c.fill_preserve(); s._stroke(.72,.7,None,WHITE)
                s.bez(polar(x,y,22,d+turn*10), polar(x,y,r*.45,d+turn*24), polar(x,y,r*.75,d+turn*38),
                      polar(x,y,r-16,d+turn*44),.35,.4)
            for k in range(3):
                s.ln(*polar(x, y, 15, k * 120 + 30), *polar(x, y, r - 9, k * 120 + 30), 0.3, 0.45, dash=[3, 3])
            s.circ(x, y, 15, 0.95, 0.9, fill=0.18)
            a0 = 200 if turn > 0 else 340
            s.arc(x, y, r + 10, min(a0, a0 + turn * 50), max(a0, a0 + turn * 50), 0.6, 0.6)
            tip = polar(x, y, r + 10, a0 + turn * 50)
            back = polar(x, y, r + 10, a0 + turn * 44)
            s.arrow(back[0], back[1], tip[0], tip[1], 0.7, 0.5, head=6)

        # pod: teardrop, nose up
        def pod(k=1.0):
            c.move_to(mx, my - 196 * k)
            c.curve_to(mx + 58 * k, my - 150 * k, mx + 60 * k, my - 20 * k, mx + 42 * k, my + 84 * k)
            c.curve_to(mx + 30 * k, my + 136 * k, mx + 10 * k, my + 176 * k, mx, my + 186 * k)
            c.curve_to(mx - 10 * k, my + 176 * k, mx - 30 * k, my + 136 * k, mx - 42 * k, my + 84 * k)
            c.curve_to(mx - 60 * k, my - 20 * k, mx - 58 * k, my - 150 * k, mx, my - 196 * k)
            c.close_path()
        pod()
        s._ink(0.07, WHITE)
        c.fill_preserve()
        s._stroke(0.95, 1.3, None, WHITE)
        c.save()
        c.translate(0, -my * 0.0)
        pod(0.62)
        c.restore()
        s._stroke(0.6, 0.6, None, WHITE)
        s.ellipse(mx, my - 40, 40, 96, a=0.5, w=0.6, dash=[4, 3], color=ARC)
        s.circ(mx, my - 64, 15, 0.9, 0.9, fill=0.2)
        s.rect(mx - 17, my - 44, 34, 58, 0.6, 0.5)
        for sgn in (-1, 1):
            s.rect(mx + sgn * 24 - 7, my + 10, 14, 120, 0.6, 0.5, dash=[4, 3], color=GOLD)
            s.ln(mx + sgn * 64, my - 120, mx + sgn * 64, my + 150, 0.3, 0.5, dash=[8, 4])

        enrich(s, "sky-racer", mx, my)

        s.leader(mx + 305 + 60, my + 15 - 60, 100, -150, 110, "RIM-DRIVEN FAN", "6 OFF / 95 kW EACH")
        s.leader(mx + 26, my - 100, 150, -250, 120, "CRASH CELL", "PILOT, SEAT AND HARNESS")
        s.leader(mx + 24, my + 100, 330, 130, 110, "LITHIUM-AIR PACK", "1 100 Wh PER kg")
        s.leader(mx, my - 196, -150, -150, -120, "SENSING ARRAY", "14 HEADS / SEES 200 m")
        s.leader(mx - 150, my + 140, -190, 160, -110, "FOLDING ARM", None)
        s.dim(mx - 403, my + 440, mx + 403, my + 440, "SPAN 4.6 m", a=0.4, label_shift=80, label_offset=-16)
    s.end_main()

    s.legend("SKY RACER", "CLASS SR-1   /   ONE-SEAT ELECTRIC RACING COPTER",
             "A racing aircraft for one pilot, flown through courses of gates in the air. "
             "The pilot steers; the machine refuses to hit a gate, the ground or another racer.",
             [("ELECTROCHEMISTRY", "Lithium-air cells that store four times today's best per kilogram and survive a thousand fast charges."),
              ("MOTOR DESIGN", "Fan motors built into the duct rim and wound with carbon nanotube wire, 25 kW for every kilogram."),
              ("AUTONOMY", "A flight computer that tracks every racer and gate a thousand times a second and overrides the pilot only in the last metre."),
              ("MATERIALS SCIENCE", "Airframes woven from nanotube fibre, half the mass of carbon composite, that fold around the cockpit instead of shattering.")],
             "2052")
    from triptych import auxiliary_panel, original_diagrams
    with auxiliary_panel(s, 'B', lx, rx):
        anchors=hardware_view(s,'sky-racer-cutaway',lx,285,410,250)
        # Enlarged type (composed profiles): the flight computer's label drops below the hull,
        # clear of the crash cell's. The crash cell keeps the name it has in view A.
        fc=(lx-170,387+s.type_growth(6)) if s.layer_mode else (lx-180,190)
        for label,tx,ty in [('FLIGHT COMPUTER',*fc),('CRASH CELL',lx-15,170),('CELL BAY',lx+110,387+s.type_growth(6))]:
            ax,ay=anchors[label]
            s.poly([(ax,ay),(tx,ty-10 if ay<ty else ty+9)],.45,.5,close=False)
            s.dot(ax,ay,1.4,.7)
            s.text(label,tx,ty,6,a=.75,align='c')
        s.view_label(lx,470,'B','LONGITUDINAL CUTAWAY','COCKPIT + CELL BAY / OUTBOARD DRIVES OMITTED')
    with auxiliary_panel(s, 'C', lx, rx):
        from right_aux_panels import course as course_panel
        course_panel(s,rx)
    from original_charts import draw as right_chart
    right_chart(s)
    original_diagrams(s)
    return s


# ---------------------------------------------------------------------------
# Volumetric stage
# ---------------------------------------------------------------------------

def volumetric_stage(size):
    s = start(size, "volumetric-stage", 808)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my - 30, 480, a0=30, thick=(200, 240), thin=(305, 345))
    from hardware3d.family_drawing import enabled as hardware_enabled, draw as draw_hardware
    if hardware_enabled('volumetric-stage'):
        from quality_panels import main_hardware
        main_hardware(s, 'volumetric-stage', mx, my)
        c = s.c
    else:
        deck = my + 250

        # deck, towers, bridge
        s.rect(mx - 450, deck, 900, 16, 0.95, 1.1, fill=0.10)
        for sgn in (-1, 1):
            truss(s, mx + sgn * 412, deck, mx + sgn * 412, my - 344, depth=30, bay=30, a=0.8)
        truss(s, mx - 427, my - 357, mx + 427, my - 357, depth=26, bay=26, a=0.8)
        heads = []
        for sgn in (-1, 1):
            for k in range(5):
                y = my - 290 + k * 112
                x = mx + sgn * 397
                s.poly([(x, y - 9), (x - sgn * 24, y - 5), (x - sgn * 24, y + 5), (x, y + 9)], 0.95, 0.8, fill=0.2)
                heads.append((x - sgn * 24, y))
        for k in range(7):
            x = mx - 300 + k * 100
            s.poly([(x - 9, my - 344), (x - 5, my - 322), (x + 5, my - 322), (x + 9, my - 344)], 0.95, 0.8, fill=0.2)
            heads.append((x, my - 322))
        for k in range(9):
            x = mx - 320 + k * 80
            s.rect(x - 12, deck - 12, 24, 12, 0.9, 0.7, fill=0.12)
            for off in (-7, 0, 7):
                s.fade_ln(x, deck - 12, x + off * 2.2, deck - 80, 0.28, 0.0, 0.5)

        # the volume the image lives in
        s.rect(mx - 336, my - 296, 672, 516, 0.35, 0.5, dash=[6, 4])
        for cx_, cy_ in ((mx - 336, my - 296), (mx + 336, my - 296), (mx - 336, my + 220), (mx + 336, my + 220)):
            s.cross(cx_, cy_, 7, 0.8, 0.7)

        # the image: a trefoil knot of light, drawn as voxels
        tilt = math.radians(72)
        pts = []
        n = 1700
        for i in range(n):
            t = 2 * math.pi * i / n
            for _ in range(4):
                X = (math.sin(t) + 2 * math.sin(2 * t)) / 2.0 + s.rng.gauss(0, 0.035)
                Y = (math.cos(t) - 2 * math.cos(2 * t)) / 2.0 + s.rng.gauss(0, 0.035)
                Z = -0.55 * math.sin(3 * t) + s.rng.gauss(0, 0.035)
                depth = Y * math.cos(tilt) - Z * math.sin(tilt)
                up = Y * math.sin(tilt) + Z * math.cos(tilt)
                pts.append((depth, mx + 150 * X, my - 20 - 150 * up))
        pts.sort()
        for depth, x, y in pts:
            near = min(1.0, max(0.0, (depth + 1.3) / 2.6))
            s.dot(x, y, 0.7 + 1.2 * near, 0.2 + 0.75 * near, WHITE if s.rng.random() < 0.12 else ARC)
        lit = [pts[900], pts[3300], pts[5600]]
        for (hx, hy), (_, vx, vy) in zip((heads[1], heads[6], heads[12], heads[3], heads[8], heads[14]), lit + lit):
            s.ln(hx, hy, vx, vy, 0.22, 0.45, dash=[2, 4])
        right = max(pts, key=lambda p: p[1])

        # audience, seen from behind
        for row in range(3):
            for k in range(40 - row):
                x = mx - 380 + k * 19.5 + row * 9.7
                s.circ(x, deck + 50 + row * 22, 5.5, 0.4 - row * 0.08, 0.5, fill=0.05)

        enrich(s, "volumetric-stage", mx, my)

        s.leader(heads[0][0] + 10, heads[0][1], -150, -90, -120, "EMITTER HEAD", "INFRARED / STEERED ON A CHIP")
        s.leader(mx - 427, my - 100, -60, 60, -100, "TOWER", "24 m")
        s.leader(mx + 100, my - 357, 140, -60, 120, "BRIDGE", "7 HEADS POINTING DOWN")
        s.leader(mx + 336, my - 120, 120, -40, 110, "IMAGE VOLUME", "40 × 22 × 18 m")
        s.leader(right[1], right[2], 46, -80, 46, "VOXEL", None)
        s.leader(mx + 240, deck - 8, 250, 70, 110, "HAZE UNIT", "LIGHT-CONVERTING PARTICLES")
        s.dim(mx - 336, my - 420, mx + 336, my - 420, "40 m", a=0.4, label_shift=70)
        s.ln(mx - 336, my - 296, mx - 336, my - 426, 0.1, 0.4)
        s.ln(mx + 336, my - 296, mx + 336, my - 426, 0.1, 0.4)
    s.end_main()

    s.legend("VOLUMETRIC STAGE", "MODEL VS-40   /   MOVING 3D IMAGES IN OPEN AIR",
             "Fills the air above a stage with images that keep their depth from every seat, "
             "for concerts, theatre and sport replays.",
             [("PHOTONICS", "Haze particles that turn infrared into visible light a thousand times better than today's, and only where two beams cross."),
              ("OPTICAL CHIPS", "Beam steering on a chip, with no moving parts, that aims at two billion points sixty times a second."),
              ("AEROSOL SCIENCE", "A haze proven harmless to breathe for hours and cleared from the hall air within a minute."),
              ("COMPUTER GRAPHICS", "Rendering a whole volume at once instead of one camera view, live, from performers on stage.")],
             "2060")
    from triptych import auxiliary_panel, original_diagrams
    with auxiliary_panel(s, 'B', lx, rx):
        from quality_panels import component
        component(s,'volumetric-stage','B',lx,190,250,120)
        for k in range(9):
            r = 96 + k * 20
            for a0, a1 in ((24, 68), (74, 106), (112, 156)):
                s.arc(lx, 214, r, a0, a1, 0.75 - k * 0.05, 0.9 if k == 0 else 0.6)
        s.view_label(lx, 520, "B", "HALL PLAN", "STAGE AND SEATING ARCS")
    with auxiliary_panel(s, 'C', lx, rx):
        qx, qy = rx, 330
        s.detail_ring(qx, qy, 170)
        s.begin_clip_circle(qx, qy, 169)
        micro_details.voxel(s,qx,qy)
        micro_details.advance_legacy_rng(s,'voxel')
        s.end_clip()
        s.ln(qx - 120, qy + 188, qx - 60, qy + 188, 0.9, 1.0)
        s.text("1 mm", qx - 90, qy + 180, 6.5, a=0.8, align="c")
        s.view_label(qx, qy + 210, "C", "ONE VOXEL", "TWO BEAMS, ONE CROSSING")
    from original_charts import draw as right_chart
    right_chart(s)
    original_diagrams(s)
    return s


# ---------------------------------------------------------------------------
# Presence rig
# ---------------------------------------------------------------------------

def limb(s, p1, p2, r1, r2, a=0.9, w=1.0, fill=0.05, dash=None):
    """A curved tapered shell with a longitudinal construction seam."""
    dx, dy = p2[0]-p1[0], p2[1]-p1[1]
    length = math.hypot(dx, dy)
    if not length:
        return
    nx, ny = -dy/length, dx/length
    def point(f, r):
        return p1[0]+dx*f+nx*r, p1[1]+dy*f+ny*r
    c = s.c
    c.move_to(*point(0,r1))
    c.curve_to(*point(.26,r1*1.12), *point(.72,r2*1.12), *point(1,r2))
    c.curve_to(*point(1.06,r2*.45), *point(1.06,-r2*.45), *point(1,-r2))
    c.curve_to(*point(.72,-r2*1.12), *point(.26,-r1*1.12), *point(0,-r1))
    c.curve_to(*point(-.04,-r1*.4), *point(-.04,r1*.4), *point(0,r1))
    c.close_path()
    s._ink(fill, WHITE); c.fill_preserve()
    s._stroke(a,w,dash,WHITE)
    s.bez(point(.1,r1*.62),point(.3,r1*.75),point(.7,r2*.75),point(.9,r2*.62),a*.4,w*.5,dash=dash)


def cuff(s, p1, p2, f0, f1, half, a=0.9, fill=0.3, color=ARC):
    """A band across a limb, from fraction f0 to f1 of its length."""
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    nx, ny = -math.sin(ang) * half, math.cos(ang) * half
    a_ = (p1[0] + (p2[0] - p1[0]) * f0, p1[1] + (p2[1] - p1[1]) * f0)
    b_ = (p1[0] + (p2[0] - p1[0]) * f1, p1[1] + (p2[1] - p1[1]) * f1)
    s.poly([(a_[0] + nx, a_[1] + ny), (b_[0] + nx, b_[1] + ny), (b_[0] - nx, b_[1] - ny), (a_[0] - nx, a_[1] - ny)],
           a, 0.6, True, fill, None, color)


def presence_rig(size):
    s = start(size, "presence-rig", 909)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my - 30, 478, a0=20, thick=(195, 235), thin=(300, 340))
    from quality_panels import main_hardware
    main_hardware(s,'presence-rig',mx,my)
    s.end_main()

    s.legend("PRESENCE RIG", "MODEL PR-2   /   SUIT AND FLOOR FOR FULL-BODY GAMES",
             "Lets a player walk, climb and fight inside a game and feel it: weight in the arms, wind on the "
             "skin, the lurch of a fall. The floor slides under the feet, so a living room is enough.",
             [("SOFT ROBOTICS", "Woven polymer muscle fibres, as strong as real muscle and silent, thin enough to wear as clothing."),
              ("NEUROSCIENCE", "Small currents behind the ear that make the balance organ feel acceleration, which ends motion sickness in virtual worlds."),
              ("MICROSYSTEMS", "Printed tactile sheets of independently moving points that survive sweat and washing."),
              ("COMPUTING", "Real-time simulation of touch, cloth and impact.")],
             "2057")
    from triptych import auxiliary_panel, original_diagrams
    with auxiliary_panel(s, 'B', lx, rx):
        from quality_panels import component
        component(s,'presence-rig','B',lx,310,330,290)
        s.view_label(lx,510,'B','ROLLER CASSETTE','DRIVE / SHAFTS / REPLACEABLE FLOOR BAY')
    with auxiliary_panel(s, 'C', lx, rx):
        component(s,'presence-rig','C',rx,310,330,290)
        s.view_label(rx,510,'C','CAPTIVE TETHER REEL','AZIMUTH BEARING / MANUAL RELEASE')
    from original_charts import draw as right_chart
    right_chart(s)
    original_diagrams(s)
    return s


# ---------------------------------------------------------------------------
# Aroma organ
# ---------------------------------------------------------------------------

def aroma_organ(size):
    s = start(size, "aroma-organ", 1010)
    mx, my, lx, rx = centres(s)
    my -= 30
    s.begin_main(mx, my)
    framing(s, mx, my, 478, a0=200, thick=(140, 175), thin=(10, 50))
    from hardware3d.family_drawing import enabled as hardware_enabled, draw as draw_hardware
    if hardware_enabled('aroma-organ'):
        draw_hardware(s, 'aroma-organ', mx, my)
        c = s.c
    else:

        s.circ(mx, my, 388, 0.95, 1.3, fill=0.03)
        s.circ(mx, my, 398, 0.4, 0.5)
        active = {3, 11, 12, 27, 40, 41, 58, 66, 79, 80, 91}
        for i in range(96):
            outer = i % 2 == 0
            r_c, r_b = (338, 13) if outer else (292, 11)
            d = i * 3.75
            x, y = polar(mx, my, r_c, d)
            on = i in active
            s.ln(*polar(mx, my, r_c - r_b, d), *polar(mx, my, 152, d), 0.85 if on else 0.13, 0.7 if on else 0.4, color=ARC if on else WHITE)
            s.circ(x, y, r_b, 0.9, 0.8, fill=0.5 if on else 0.05, color=ARC if on else WHITE)
            s.arc(x, y, r_b - 4, d + 90, d + 90 + 200 + (i * 37) % 120, 0.5, 0.5)
            vx, vy = polar(mx, my, 250, d)
            s.c.save()
            s.c.translate(vx, vy)
            s.c.rotate(math.radians(d))
            s.rect(-5, -2.5, 10, 5, 0.9, 0.5, fill=0.9 if on else 0.1, color=ARC if on else WHITE)
            s.c.restore()
        s.circ(mx, my, 250, 0.2, 0.45, dash=[1.5, 4])
        s.circ(mx, my, 152, 0.9, 0.9)
        s.circ(mx, my, 144, 0.4, 0.5)

        # mixing chip with a serpentine channel
        s.rect(mx - 84, my - 84, 168, 168, 0.95, 1.1, fill=0.08)
        for k in range(8):
            d = k * 45 + 22.5
            s.ln(*polar(mx, my, 144, d), *polar(mx, my, 100, d), 0.8, 0.7, color=ARC)
        pts = []
        for row in range(9):
            y = my - 68 + row * 17
            xs = (mx - 68, mx + 68) if row % 2 == 0 else (mx + 68, mx - 68)
            pts += [(xs[0], y), (xs[1], y)]
        s.poly(pts, 0.8, 0.8, close=False, color=ARC)
        s.circ(mx, my, 34, 0.9, 0.9, dash=[4, 3], color=GOLD)
        s.circ(mx, my, 22, 0.95, 1.1, fill=0.35)
        s.circ(mx, my, 9, 0.9, 0.7)

        # clearing fan and scrubber, below
        s.rect(mx - 130, my + 384, 260, 84, 0.95, 1.1, fill=0.05)
        fx, fy = mx - 70, my + 428
        s.circ(fx, fy, 32, 0.9, 0.9)
        for k in range(6):
            s.bez(polar(fx, fy, 6, k * 60), polar(fx, fy, 16, k * 60 + 12), polar(fx, fy, 26, k * 60 + 30), polar(fx, fy, 30, k * 60 + 48), 0.7, 0.7)
        s.circ(fx, fy, 6, 0.9, 0.7, fill=0.3)

        def scrub():
            s.c.rectangle(mx - 10, my + 398, 120, 56)
        s.hatch(scrub, 5, 45, 0.45, color=GOLD)
        s.hatch(scrub, 5, -45, 0.45, color=GOLD)
        s.rect(mx - 10, my + 398, 120, 56, 0.9, 0.8, color=GOLD)
        s.arrow(mx - 170, my + 428, mx - 134, my + 428, 0.7, 0.7, head=6)
        s.arrow(mx + 134, my + 428, mx + 176, my + 428, 0.7, 0.7, head=6)

        enrich(s, "aroma-organ", mx, my)

        s.leader(*polar(mx, my, 338, 12 * 3.75), 120, 60, 110, "BASE ODORANT", "6 MONTHS PER CARTRIDGE")
        s.leader(*polar(mx, my, 250, 300), 260, -70, 110, "VALVE RING", None)
        s.leader(*polar(mx, my, 152, 330), 330, -40, 110, "MANIFOLD", None)
        s.leader(mx + 60, my + 60, 380, 130, 110, "MIXING CHIP", "NEW BLEND 12 TIMES A SECOND")
        s.leader(mx - 16, my - 16, -330, -300, -110, "HEATED OUTLET", "TO THE NOSE PIECE OR THE ROOM DUCT")
        s.leader(fx - 20, fy + 10, -190, 30, -110, "CLEARING FAN", None)
        s.leader(mx + 100, my + 440, 170, 30, 110, "SCRUBBER", None)
        s.dim(mx - 388, my - 440, mx + 388, my - 440, "Ø 310 mm", a=0.4, label_shift=70)
    if not s.wide:
        s.text('METERED ODORANTS / NOT A VALIDATED PERCEPTION MODEL',mx+28,my+394,6.2,track=.08,a=.62)
    s.end_main()

    s.legend("AROMA ORGAN", "MODEL AO-96   /   SMELL AND FLAVOUR ON CUE",
             "Plays smells the way a speaker plays sound. For cinema, games and kitchens.",
             [("SENSORY BIOLOGY", "A full map from the 400 human smell receptors to what people say they smell, so any odour can be written down as a recipe."),
              ("CHEMISTRY", "A palette of safe base odorants that covers nearly the whole map, the way three colours cover sight."),
              ("MICROFLUIDICS", "Valves and a mixer small enough to meter picolitre doses."),
              ("CATALYSIS", "A room-temperature catalyst that destroys the last smell before the next scene.")],
             "2050")
    from triptych import auxiliary_panel, original_diagrams
    with auxiliary_panel(s, 'B', lx, rx):
        hardware_view(s,'aroma-organ-section',lx,292,382,285)
        from hardware3d.secondary_drawing import fitted_size
        _,view_h=fitted_size('aroma-organ-section',382,285)
        datum_y=292+view_h/2+8
        s.ln(lx-195,datum_y,lx+195,datum_y,.25,.5,dash=[12,4,2,4])
        s.view_label(lx, 470, "B", "CUTAWAY", "CARTRIDGES, MIXER, HEATED OUTLET, FAN")
    with auxiliary_panel(s, 'C', lx, rx):
        from quality_panels import aroma_detail
        aroma_detail(s,rx)
    from original_charts import draw as right_chart
    right_chart(s)
    original_diagrams(s)

    return s


# ---------------------------------------------------------------------------
# Bounder
# ---------------------------------------------------------------------------

def spindle(s, p1, p2, off, width, color=ARC):
    """A muscle bundle beside a limb: a lens shape, hatched along its length."""
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    nx, ny = -math.sin(ang), math.cos(ang)
    a_ = (p1[0] + (p2[0] - p1[0]) * 0.12 + nx * off, p1[1] + (p2[1] - p1[1]) * 0.12 + ny * off)
    b_ = (p1[0] + (p2[0] - p1[0]) * 0.88 + nx * off, p1[1] + (p2[1] - p1[1]) * 0.88 + ny * off)

    def ctrl(f, k):
        return (a_[0] + (b_[0] - a_[0]) * f + nx * width * k, a_[1] + (b_[1] - a_[1]) * f + ny * width * k)
    for k in (-1.0, -0.5, 0.0, 0.5, 1.0):
        s.bez(a_, ctrl(0.3, k), ctrl(0.7, k), b_, 0.9 if abs(k) == 1 else 0.45, 0.9 if abs(k) == 1 else 0.5, color=color)
    return a_, b_


def bounder(size):
    s = start(size, "bounder", 1111)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my - 30, 478, a0=330, thick=(190, 232), thin=(120, 160))
    from hardware3d.family_drawing import enabled as hardware_enabled, draw as draw_hardware
    if hardware_enabled('bounder'):
        draw_hardware(s, 'bounder', mx, my)
        c = s.c
    else:
        g = my + 330
        H, K, A = (mx - 10, my - 250), (mx + 84, my - 36), (mx + 18, my + 172)
        T = (mx + 124, g - 6)

        s.ln(mx - 430, g, mx + 430, g, 0.8, 0.9)
        for k in range(-21, 22):
            s.ln(mx + k * 20, g, mx + k * 20 - 9, g + 11, 0.3, 0.45)

        # The wearer's anatomical envelope remains subordinate to the mechanism.
        anatomical_segment(s, H, K, 48, 27, "thigh", a=.3, w=.55, ghost=True)
        anatomical_segment(s, K, A, 27, 14, "calf", a=.3, w=.55, ghost=True)
        joint_chain(s, [H, K, A])
        s.poly([(A[0] - 28, A[1] + 4), (A[0] + 74, A[1] + 34), (A[0] + 80, A[1] + 52), (A[0] - 28, A[1] + 52)], 0.3, 0.6, dash=[5, 4])
        s.poly([(mx - 86, my - 330), (mx - 74, my - 450)], 0.3, 0.6, close=False, dash=[5, 4])
        s.poly([(mx + 70, my - 330), (mx + 78, my - 450)], 0.3, 0.6, close=False, dash=[5, 4])

        # belt and pack
        s.rect(mx - 96, my - 332, 176, 58, 0.95, 1.1, fill=0.07)
        s.rect(mx - 168, my - 356, 68, 118, 0.95, 1.1, fill=0.06)
        for k in range(1, 6):
            s.ln(mx - 162, my - 356 + k * 19, mx - 106, my - 356 + k * 19, 0.4, 0.45)
        s.rect(mx - 158, my - 350, 20, 10, 0.9, 0.5, fill=0.8, color=ARC)
        s.bez((mx - 134, my - 356), (mx - 130, my - 420), (mx - 90, my - 440), (mx - 76, my - 450), 0.4, 0.6, dash=[5, 4])

        # frame, muscles, joints
        limb(s, H, K, 13, 11, fill=0.07)
        limb(s, K, A, 11, 9, fill=0.07)
        f1 = spindle(s, H, K, 36, 13)
        f2 = spindle(s, H, K, -36, 13)
        f3 = spindle(s, K, A, 30, 11)
        for a_, b_ in (f1, f2):
            s.ln(a_[0], a_[1], H[0], H[1] + 10, 0.6, 0.5, color=ARC)
            s.ln(b_[0], b_[1], K[0], K[1] - 6, 0.6, 0.5, color=ARC)
        s.ln(f3[0][0], f3[0][1], K[0], K[1] + 8, 0.6, 0.5, color=ARC)
        s.ln(f3[1][0], f3[1][1], A[0], A[1] - 6, 0.6, 0.5, color=ARC)
        cuff(s, H, K, 0.30, 0.40, 58, fill=0.10)
        ang = math.atan2(K[1] - H[1], K[0] - H[0])
        for k in range(-5, 6):
            bx = H[0] + (K[0] - H[0]) * 0.35 - math.sin(ang) * k * 10
            by = H[1] + (K[1] - H[1]) * 0.35 + math.cos(ang) * k * 10
            s.dot(bx, by, 1.6, 0.95, GOLD)
        s.circ(H[0], H[1], 33, 0.95, 1.2, fill=0.10)
        s.circ(H[0], H[1], 23, 0.9, 1.6, dash=[5, 3], color=ARC)
        s.dot(H[0], H[1], 4, 0.95)
        s.circ(K[0], K[1], 27, 0.95, 1.2, fill=0.10)
        s.circ(K[0], K[1], 45, 0.5, 0.6, dash=[4, 3])
        s.dot(K[0], K[1], 4, 0.95)
        s.circ(A[0], A[1], 20, 0.95, 1.1, fill=0.10)
        s.dot(A[0], A[1], 3, 0.95)

        # spring blade
        s.bez((A[0] - 4, A[1] + 18), (mx - 116, my + 236), (mx - 44, g - 2), T, 0.95, 1.3)
        s.bez((A[0] + 10, A[1] + 22), (mx - 94, my + 244), (mx - 34, g - 14), (T[0] - 4, T[1] - 10), 0.95, 1.3)
        s.ln(T[0], T[1], T[0] - 4, T[1] - 10, 0.95, 1.2)
        s.rect(T[0] - 46, g - 6, 60, 6, 0.9, 0.7, fill=0.5)
        for k in range(1, 8):
            s.ln(T[0] - 46 + k * 7.5, g - 6, T[0] - 46 + k * 7.5, g, 0.4, 0.4)

        enrich(s, "bounder", mx, my)

        s.leader(mx - 134, my - 300, -130, -60, -110, "PACK", "CELLS AND CONTROLLER / 2.2 kg")
        s.leader(H[0] + 22, H[1] - 10, 230, -80, 110, "HIP DRIVE", None)
        s.leader(f1[0][0] * 0.5 + f1[1][0] * 0.5 - 12, f1[0][1] * 0.5 + f1[1][1] * 0.5 + 6, -230, 10, -110, "NERVE-SIGNAL CUFF",
                 "READS THE COMMAND 60 ms EARLY")
        s.leader(f2[0][0] * 0.4 + f2[1][0] * 0.6, f2[0][1] * 0.4 + f2[1][1] * 0.6, 200, -30, 110, "MUSCLE BUNDLE", "3 PER LEG")
        s.leader(K[0] + 40, K[1] + 20, 150, 30, 100, "KNEE CAM", "VARIABLE LEVERAGE")
        s.leader(A[0] - 16, A[1] + 10, -220, -10, -110, "ANKLE PIVOT", None)
        s.leader(mx - 58, my + 262, -190, 20, -110, "SPRING BLADE", "RETURNS 96 % OF THE LANDING")
        s.leader(T[0] - 10, g - 3, 170, -50, 110, "SOLE", "SPIKED OR FLAT")
        s.dim(mx + 440, g, mx + 440, my - 332, "1.18 m", a=0.4)
        s.dim(mx - 330, g + 44, T[0], g + 44, "STRIDE 5.8 m", a=0.4)
    s.end_main()

    s.legend("BOUNDER", "MODEL B-4   /   POWERED LEGS FOR AUGMENTED ATHLETICS",
             "Lets a runner sprint and jump beyond any unaided athlete. "
             "The legs follow the athlete's own nerve signals, so the athlete still does the running.",
             [("MATERIALS SCIENCE", "Artificial muscle spun from carbon nanotube yarn: forty times the power of human muscle per kilogram, good for a hundred million strokes."),
              ("NEURAL ENGINEERING", "Sensors on the skin that read the nerve command to a muscle before it moves, with no implant."),
              ("BIOMECHANICS", "Control that keeps the load on knees and spine below what an unaided sprinter takes."),
              ("COMPOSITES", "Spring blades that give back almost all of each landing for a million cycles without cracking.")],
             "2064")
    from triptych import auxiliary_panel, original_diagrams
    with auxiliary_panel(s, 'B', lx, rx):
        from bounder_wearing import draw as draw_bounder_wearing
        draw_bounder_wearing(s,lx)
    with auxiliary_panel(s, 'C', lx, rx):
        qx, qy = rx, 330
        s.detail_ring(qx, qy, 170)
        s.begin_clip_circle(qx, qy, 169)
        micro_details.yarn(s,qx,qy)
        micro_details.advance_legacy_rng(s,'yarn')
        s.end_clip()
        s.ln(qx - 120, qy + 188, qx - 60, qy + 188, 0.9, 1.0)
        s.text("50 µm", qx - 90, qy + 180, 6.5, a=0.8, align="c")
        s.view_label(qx, qy + 210, "C", "MUSCLE YARN", "TWISTED, THEN COILED / SHORTENS WHEN CHARGED")
    from original_charts import draw as right_chart
    right_chart(s)
    original_diagrams(s)
    return s


SHEETS = [
    ("sky-racer", sky_racer),
    ("volumetric-stage", volumetric_stage),
    ("presence-rig", presence_rig),
    ("aroma-organ", aroma_organ),
    ("bounder", bounder),
]
