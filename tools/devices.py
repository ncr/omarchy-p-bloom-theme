"""Six devices that do not exist yet.

Each one has a real job and rests on breakthroughs that have not happened but
could within about fifty years. The legend on each sheet names the device,
says what it does, and lists what had to be discovered first.
"""

import math
import micro_details
from hardware3d.secondary_drawing import view as hardware_view

import cairo

import order
from fidelity import enrich
from sheet import ARC, GOLD, SUN, WHITE, Sheet, polar



def start(size, sheet, seed):
    """Open a sheet: palette, background, grid and frame. The number printed on
    the sheet comes from its place in order.ORDER."""
    s = Sheet(size[0], size[1], seed=seed)
    s.subject = sheet
    s.set_palette(order.palette(sheet))
    s.background()
    s.begin_lines()
    s.grid()
    # Permanent NCR number (126-139), three digits like Century, no total.
    s.frame(order.number(sheet), None)
    return s


def centres(s):
    """Main drawing centre, left column centre x, right column centre x."""
    return s.cx - 120, s.cy - 25, s.cx - 920, s.cx + 850


def framing(s, x, y, r, a0=150, thick=(200, 252), thin=(20, 64)):
    """Quiet view registration and datum axes, without decorative dial scales.

    The old angular arguments remain accepted by existing sheet definitions.
    They no longer imply an angular measurement around an unrelated subject.
    """
    for sx in (-1, 1):
        for sy in (-1, 1):
            xx, yy = x + sx*r, y + sy*r
            s.ln(xx-sx*13, yy, xx, yy, .20, .5)
            s.ln(xx, yy-sy*13, xx, yy, .20, .5)
    s.ln(x-r-20, y, x+r+20, y, .11, .4, dash=[20,4,2,4])
    s.datum_y = y  # the horizontal datum runs under the callout columns; their text keeps off it
    # The drawing datum stops before the shared A-caption rail.
    s.ln(x, y-r-12, x, min(y+r+12, 884), .11, .4, dash=[20,4,2,4])


def tree(s, x, y, ang, length, depth, spread=28, shrink=0.74, a=0.9, w=1.0, color=ARC, keep=None):
    """Branching vessel tree. keep(x, y) can veto segments, e.g. above the print front."""
    x2, y2 = polar(x, y, length, ang)
    if keep is None or keep(x2, y2):
        s.ln(x, y, x2, y2, a, w, color=color)
    if depth > 0:
        jitter = s.rng.uniform(-8, 8)
        for sgn in (-1, 1):
            tree(s, x2, y2, ang + sgn * spread + jitter, length * shrink, depth - 1, spread, shrink,
                 a * 0.86, max(0.4, w * 0.8), color, keep)


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


# ---------------------------------------------------------------------------
# Organ foundry
# ---------------------------------------------------------------------------

def bean(cx, cy, R, stretch=1.3, notch=0.30):
    pts = []
    for q in range(0, 360, 3):
        r = R * (1 - notch * math.exp(-(((q - 180) / 40.0) ** 2)))
        pts.append((cx + r * math.cos(math.radians(q)), cy + stretch * r * math.sin(math.radians(q))))
    return pts


def organ_foundry(size):
    s = start(size, "organ-foundry", 101)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my - 30, 470)
    from hardware3d.family_drawing import enabled as hardware_enabled, draw as draw_hardware
    if hardware_enabled('organ-foundry'):
        draw_hardware(s, 'organ-foundry', mx, my)
        c = s.c
    else:

        # cartridge housing
        s.rect(mx - 210, my - 410, 420, 84, 0.9, 1.0, fill=0.04)
        for k in range(6):
            x = mx - 150 + k * 60
            s.rect(x - 16, my - 400, 32, 62, 0.8, 0.7, fill=0.05)
            s.rect(x - 7, my - 338, 14, 8, 0.7, 0.6)
            level = my - 392 + 8 * ((k * 5) % 6)
            s.ln(x - 16, level, x + 16, level, 0.6, 0.5, color=ARC)
            s.text(f"{k + 1}", x, my - 345, 6, track=0, a=0.6, align="c")

        # glass chamber, double wall
        def rounded(x, y, w_, h_, r):
            c = s.c
            c.new_sub_path()
            c.arc(x + w_ - r, y + r, r, -math.pi / 2, 0)
            c.arc(x + w_ - r, y + h_ - r, r, 0, math.pi / 2)
            c.arc(x + r, y + h_ - r, r, math.pi / 2, math.pi)
            c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
            c.close_path()
        rounded(mx - 195, my - 322, 390, 446, 26)
        s._ink(0.035, WHITE)
        s.c.fill_preserve()
        s._stroke(0.95, 1.2, None, WHITE)
        rounded(mx - 187, my - 314, 374, 430, 20)
        s._stroke(0.4, 0.5, None, WHITE)

        # gantry and print head
        for yy in (my - 286, my - 278):
            s.ln(mx - 186, yy, mx + 186, yy, 0.8, 0.7)
        for k in range(-9, 10):
            s.ln(mx + k * 20, my - 286, mx + k * 20, my - 278, 0.3, 0.4)
        s.rect(mx + 8, my - 298, 76, 32, 0.95, 0.9, fill=0.1)
        s.rect(mx + 24, my - 266, 44, 30, 0.9, 0.8, fill=0.06)
        oy, R, front = my - 66, 108, my - 118
        for k in range(3):
            s.ln(mx + 34 + k * 12, my - 236, mx + 34 + k * 12, front - 3, 0.85, 0.6)
        s.ln(mx - 160, front, mx + 160, front, 0.35, 0.5, dash=[3, 3], color=ARC)

        # the organ: printed below the front, still to come above it
        outline = bean(mx + 20, oy, R)
        s.c.save()
        s.c.rectangle(mx - 200, front, 400, 400)
        s.c.clip()
        s.poly(outline, 0.95, 1.2, fill=0.05)

        def organ_path():
            s.c.move_to(*outline[0])
            for p in outline[1:]:
                s.c.line_to(*p)
            s.c.close_path()
        s.hatch(organ_path, 4, 0, 0.16, 0.4)
        inner = bean(mx + 26, oy, R * 0.62, notch=0.42)
        s.poly(inner, 0.4, 0.5, dash=[3, 3])
        s.c.restore()
        s.c.save()
        s.c.rectangle(mx - 200, my - 320, 400, front - (my - 320))
        s.c.clip()
        s.poly(outline, 0.4, 0.6, dash=[4, 4])
        s.c.restore()
        hx = mx + 20 - R * 0.7
        keep = lambda x, y: y > front + 2
        tree(s, hx, oy - 4, -14, 46, 6, keep=keep)
        tree(s, hx, oy + 10, 16, 44, 5, a=0.5, w=0.8, color=WHITE, keep=keep)

        # lines from the organ to the base
        s.poly([(hx, oy - 4), (mx - 230, oy - 4), (mx - 230, my + 218), (mx - 216, my + 218)], 0.9, 1.0, close=False, color=ARC)
        s.poly([(hx, oy + 10), (mx - 246, oy + 10), (mx - 246, my + 250), (mx + 150, my + 250), (mx + 150, my + 240)], 0.55, 0.7, close=False)
        for yy in (oy - 4, oy + 10):
            s.rect(mx - 201, yy - 5, 12, 10, 0.8, 0.6, fill=0.2)

        # build plate
        s.rect(mx - 130, my + 78, 260, 12, 0.9, 0.8, fill=0.1)
        s.rect(mx - 18, my + 90, 36, 34, 0.7, 0.6)

        # base unit
        s.rect(mx - 120, my + 124, 240, 18, 0.8, 0.7)
        s.rect(mx - 262, my + 142, 524, 150, 0.95, 1.1, fill=0.04)
        s.circ(mx - 190, my + 218, 26, 0.95, 1.0, fill=0.06)
        s.poly([polar(mx - 190, my + 218, 15, d) for d in (0, 120, 240)], 0.9, 0.7, fill=0.3)
        s.ln(mx - 164, my + 218, mx - 132, my + 218, 0.9, 1.0, color=ARC)
        s.rect(mx - 132, my + 186, 92, 64, 0.9, 0.8, fill=0.05)
        s.poly([(mx - 124 + k * 9.5, my + (196 if k % 2 else 240)) for k in range(9)], 0.7, 0.6, close=False, color=ARC)
        s.ln(mx - 40, my + 218, mx - 22, my + 218, 0.9, 1.0, color=ARC)
        for k in range(3):
            x = mx - 22 + k * 50
            s.rect(x, my + 166, 36, 92, 0.85, 0.7, fill=0.05)
            s.ln(x, my + 190 + k * 14, x + 36, my + 190 + k * 14, 0.6, 0.5, color=ARC)
        s.rect(mx + 150, my + 176, 84, 64, 0.9, 0.8, fill=0.06)
        s.poly([(mx + 158 + k * 4, my + 208 + 14 * math.sin(k * 0.9) * math.exp(-((k - 9) / 6.0) ** 2)) for k in range(18)],
               0.9, 0.7, close=False, color=ARC)
        for k in range(4):
            s.circ(mx + 164 + k * 18, my + 228, 3, 0.8, 0.5, fill=0.5 if k < 3 else 0)
        for x in (mx - 240, mx + 210):
            s.poly([(x, my + 292), (x + 30, my + 292), (x + 24, my + 308), (x + 6, my + 308)], 0.7, 0.6)
        s.ln(mx - 420, my + 308, mx + 420, my + 308, 0.6, 0.7)

        enrich(s, "organ-foundry", mx, my)

        s.leader(mx + 46, my - 252, 232, -92, 110, "PRINT HEAD", "6 BIO-INKS / 10 µm VOXEL")
        s.leader(mx - 150, my - 372, -150, -36, -120, "CELL CARTRIDGES", "GROWN FROM THE PATIENT'S SKIN")
        s.leader(mx + 20 + R * 0.93, front + 6, 190, -50, 110, "PRINT FRONT", "LAYER 1 212 OF 2 900")
        s.leader(mx + 44, oy + 24, 250, 52, 120, "VASCULAR TREE", "ARTERY TO 10 µm CAPILLARY")
        s.leader(mx - 190, my + 218, -150, 64, -110, "PERFUSION PUMP", "PULSATILE / 72 bpm")
        s.leader(mx - 86, my + 246, -60, 112, -110, "OXYGENATOR", None)
        s.leader(mx + 196, my + 200, 120, 60, 100, "METABOLITE SENSORS", "4 ANALYTES / 1 Hz")
        s.dim(mx + 300, my - 322, mx + 300, my + 124, "620 mm", a=0.4)
    s.end_main()

    s.legend("ORGAN FOUNDRY", "MODEL OF-3   /   PERFUSION BIOPRINTER",
             "Prints a kidney from the patient's own cells and matures it until it filters blood. "
             "No donor, no waiting list, no immune suppression.",
             [("TISSUE ENGINEERING", "Printed capillary networks that stay open under blood flow."),
              ("CELL BIOLOGY", "Skin cells reprogrammed reliably into all 26 cell types of a kidney."),
              ("DEVELOPMENTAL BIOLOGY", "Chemical gradients that make printed cells assemble themselves into working nephrons."),
              ("BIOSENSING", "In-line sensors that steer nutrients and oxygen hour by hour as the tissue grows.")],
             "2068")
    from triptych import auxiliary_panel, original_diagrams
    with auxiliary_panel(s, 'B', lx, rx):
        dx, dy = lx, 300
        s.detail_ring(dx, dy, 150)
        s.begin_clip_circle(dx, dy, 149)
        micro_details.capillaries(s,dx,dy)
        micro_details.advance_legacy_rng(s,'capillaries')
        s.end_clip()
        s.view_label(dx, dy + 190, "B", "CAPILLARY BED", "SCALE 200 : 1")
    from original_charts import draw as right_chart
    right_chart(s)
    with auxiliary_panel(s, 'C', lx, rx):
        from right_aux_panels import kidney as kidney_panel
        kidney_panel(s,rx)
    original_diagrams(s)
    return s


# ---------------------------------------------------------------------------
# Quantum simulator
# ---------------------------------------------------------------------------

def quantum_simulator(size):
    s = start(size, "quantum-simulator", 202)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my - 20, 480, a0=300, thick=(160, 205), thin=(330, 368))

    import os
    hardware_mode = os.environ.get('PBLOOM_HARDWARE_STUDY', 'radial' if os.environ.get('PBLOOM_HARDWARE_SET', 'retro') == 'retro' else '')
    hardware_study = hardware_mode in ('1', 'radial')
    radial_study = hardware_mode == 'radial'
    if hardware_study:
        if radial_study:
            from hardware3d.radial_drawing import main as hardware_main
        else:
            from hardware3d.drawing import main as hardware_main
        hardware_main(s, mx, my)
    else:
        plates = [(-390, 230, "300 K"), (-300, 210, "50 K"), (-205, 186, "4 K"),
                  (-115, 160, "800 mK"), (-35, 140, "100 mK"), (45, 124, "8 mK")]

        # support frame and floor
        s.ln(mx - 420, my + 405, mx + 420, my + 405, 0.6, 0.7)
        for sgn in (-1, 1):
            s.rect(mx + sgn * 330 - 8, my - 396, 16, 801, 0.7, 0.6, fill=0.04)
            s.ln(mx + sgn * 230, my - 390, mx + sgn * 322, my - 390, 0.8, 0.8)
            s.ln(mx + sgn * 236, my - 330, mx + sgn * 322, my - 384, 0.5, 0.5)

        # outer vacuum can and the nested shields
        c = s.c
        c.new_sub_path()
        c.move_to(mx - 238, my - 385)
        c.line_to(mx - 238, my + 330)
        c.arc_negative(mx - 208, my + 330, 30, math.pi, math.pi / 2)
        c.line_to(mx + 208, my + 360)
        c.arc_negative(mx + 208, my + 330, 30, math.pi / 2, 0)
        c.line_to(mx + 238, my - 385)
        s._stroke(0.9, 1.1, None, WHITE)
        for (yo, hw, _), yb, a, dash in zip(plates[1:4], (335, 312, 288), (0.55, 0.45, 0.4), (None, None, [4, 3])):
            s.poly([(mx - hw + 6, my + yo), (mx - hw + 6, my + yb), (mx + hw - 6, my + yb), (mx + hw - 6, my + yo)],
                   a, 0.6, close=False, dash=dash)

        # cooler head and its two tubes
        s.rect(mx + 96, my - 470, 100, 62, 0.9, 0.9, fill=0.06)
        for k in range(5):
            s.ln(mx + 104, my - 460 + k * 11, mx + 188, my - 460 + k * 11, 0.3, 0.4)
        for x in (mx + 112, mx + 158):
            s.rect(x, my - 408, 22, 200, 0.6, 0.5, dash=[4, 3])
        for x in (mx - 170, mx - 110, mx - 50):
            s.rect(x, my - 412, 30, 17, 0.8, 0.6)

        # plates, rods, control lines
        for i, (yo, hw, label) in enumerate(plates):
            y = my + yo
            if i < len(plates) - 1:
                nyo, nhw, _ = plates[i + 1]
                for fx in (-1, -0.42, 0.42, 1):
                    x = mx + fx * (nhw - 14)
                    s.rect(x - 2.5, y + 5, 5, nyo - yo - 10, 0.6, 0.5)
            s.rect(mx - hw, y - 5, 2 * hw, 10, 0.95, 1.0, fill=0.14)
        for k in range(11):
            x = mx - 112 + k * 9
            s.ln(x, my - 385, x, my + 40, 0.55, 0.45)
            for yo, _, _ in plates[1:]:
                s.rect(x - 2.2, my + yo + 7, 4.4, 8, 0.8, 0.4, fill=0.5)
        for k in range(6):
            s.rect(mx - 176 + k * 9 if k < 3 else mx + 60 + k * 9, my - 218, 7, 7, 0.9, 0.5, fill=0.7, color=ARC)

        # optical fibres
        for k in range(5):
            x = mx + 22 + k * 7
            s.ln(x, my - 385, x, my + 20, 0.8, 0.55, color=ARC)
            s.bez((x, my + 20), (x, my + 46), (mx - 40 + k * 7, my + 40), (mx - 40 + k * 7, my + 66), 0.8, 0.55, color=ARC)

        # still, heat exchanger, mixing chamber
        s.rect(mx + 74, my - 109, 60, 28, 0.85, 0.7, fill=0.06)
        s.poly([(mx + 104 + 13 * math.sin(q * 0.9), my - 80 + q * 1.1) for q in range(0, 37)], 0.8, 0.6, close=False)
        s.rect(mx + 70, my + 50, 50, 40, 0.9, 0.8, fill=0.1)

        # processor stack inside its magnetic shield
        s.rect(mx - 96, my + 58, 160, 200, 0.95, 1.1, fill=0.04)
        s.rect(mx - 89, my + 65, 146, 186, 0.45, 0.5)
        s.ln(mx + 44, my + 72, mx + 44, my + 244, 0.6, 0.6)
        for k in range(6):
            y = my + 84 + k * 28
            s.rect(mx - 78, y, 118, 10, 0.9, 0.7, fill=0.12)
            for q in range(5):
                s.rect(mx - 70 + q * 22, y - 5, 12, 5, 0.9, 0.4, fill=0.8, color=ARC)

        # temperature scale
        sx = mx - 520
        s.ln(sx, my - 395, sx, my + 50, 0.5, 0.6)
        s.text("STAGE", sx - 8, my - 425, 6.5, a=0.5, align="r")
        s.text("TEMPERATURE", sx - 8, my - 412, 6.5, a=0.5, align="r")
        for yo, hw, label in plates:
            s.ln(sx, my + yo, sx + 10, my + yo, 0.8, 0.7)
            s.ln(sx + 14, my + yo, mx - hw - 6, my + yo, 0.14, 0.4, dash=[2, 4])
            s.text(label, sx - 8, my + yo + 3, 7.5, a=0.85, align="r")
        for k in range(45):
            s.ln(sx, my - 395 + k * 10, sx + 4, my - 395 + k * 10, 0.3, 0.4)

        enrich(s, "quantum-simulator", mx, my)

        s.leader(mx + 150, my - 440, 130, -30, 110, "PULSE-TUBE COOLER", "NO LIQUID HELIUM TO REFILL")
        s.leader(mx + 69, my - 212, 250, -60, 120, "CONTROL CHIPS", "AT 4 K, BESIDE THE WIRING")
        s.leader(mx + 50, my - 150, 270, 20, 120, "OPTICAL LINK", "TO NEIGHBOUR CRYOSTATS")
        s.leader(mx + 116, my - 60, 210, 20, 110, "HEAT EXCHANGER", None)
        s.leader(mx + 120, my + 70, 210, 0, 110, "MIXING CHAMBER", "HELIUM-3 IN HELIUM-4")
        s.leader(mx + 64, my + 150, 260, 20, 110, "MAGNETIC SHIELD", None)
        s.leader(mx - 60, my + 172, -330, 80, -120, "PROCESSOR STACK", "6 TILES × 1 700 LOGICAL QUBITS")
        s.leader(mx - 80, my - 260, -290, -30, -90, "CONTROL LINES", None)
    s.end_main()

    s.legend("QUANTUM SIMULATOR", "MODEL QS-10K   /   FAULT-TOLERANT SUPERCONDUCTING COMPUTER",
             "Computes exactly how molecules and materials behave. Used to design catalysts, drugs and "
             "battery chemistries that no classical computer can model.",
             [("QUANTUM PHYSICS", "Error-corrected qubits that hold their state for hours instead of milliseconds."),
              ("MATERIALS SCIENCE", "Superconducting circuits with a hundred times fewer atomic defects than today's."),
              ("CRYOGENIC ELECTRONICS", "Control chips that work inside the cryostat and replace two million cables."),
              ("PHOTONICS", "Optical links that entangle qubits in separate cryostats into one machine.")],
             "2058")
    from triptych import auxiliary_panel, original_diagrams
    with auxiliary_panel(s, 'B', lx, rx):
        from surface_code import draw as draw_surface_code
        draw_surface_code(s,lx)
    from original_charts import draw as right_chart
    right_chart(s)
    with auxiliary_panel(s, 'C', lx, rx):
        if hardware_study:
            if radial_study:
                from hardware3d.radial_drawing import detail as hardware_detail
            else:
                from hardware3d.drawing import detail as hardware_detail
            hardware_detail(s, rx, 330)
        else:
            # coldest plate, plan, right
            qx, qy = rx, 330
            s.detail_ring(qx, qy, 170)
            s.circ(qx, qy, 150, 0.95, 1.1, fill=0.04)
            for k in range(12):
                s.circ(*polar(qx, qy, 122, k * 30), 9, 0.8, 0.6)
            for k in range(4):
                x, y = polar(qx, qy, 136, 45 + k * 90)
                s.circ(x, y, 5, 0.9, 0.7, fill=0.5)
            s.rect(qx - 58, qy - 58, 116, 116, 0.7, 0.6, dash=[4, 3])
            for i in range(-3, 4):
                for j in range(-3, 4):
                    if abs(i) + abs(j) <= 4:
                        s.circ(qx + i * 15 + (7.5 if j % 2 else 0), qy + j * 13, 3, 0.9, 0.5, color=ARC)
            s.view_label(qx, qy + 210, "C", "8 mK PLATE", "PLAN / FIBRE AND LINE PORTS")
    original_diagrams(s)
    return s


# ---------------------------------------------------------------------------
# Tether climber
# ---------------------------------------------------------------------------

def tether_climber(size):
    s = start(size, "tether-climber", 303)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my - 30, 470, a0=20, thick=(195, 240), thin=(300, 345))
    from hardware3d.family_drawing import enabled as hardware_enabled, draw as draw_hardware
    if hardware_enabled('tether-climber'):
        parts = draw_hardware(s, 'tether-climber', mx, my)
        c = s.c
        # The power beam comes up from the ground station into the receiver's underside.
        # (parts holds the dot on the beam, 80 units under the exported anchor on the receiver plate);
        # each line starts at the plate's lower rim and fades towards the ground station
        px, py = parts['POWER BEAM']
        by = py - 80
        for k in range(-4, 5):
            top = by + 52 - 20 * (k / 4) ** 2
            s.fade_ln(px + k * 30, top, px + k * 10, by + 230, 0.5 - abs(k) * 0.04, 0.0, 0.5, ARC)
    else:

        # power beam from below
        for k in range(-6, 7):
            s.fade_ln(mx + k * 60, my + 274, mx + k * 14, my + 560, 0.6 - abs(k) * 0.04, 0.0, 0.6, ARC)

        # ribbon
        for off, a in ((-6, 0.85), (6, 0.85), (0, 0.2)):
            s.ln(mx + off, my - 640, mx + off, my + 700, a, 0.7 if off else 0.4)
        for k in range(-32, 35):
            s.ln(mx - 6, my + k * 20, mx + 6, my + k * 20 + 6, 0.25, 0.4)

        # debris shield
        for sgn in (-1, 1):
            s.poly([(mx + sgn * 9, my - 400), (mx + sgn * 96, my - 292), (mx + sgn * 9, my - 292)], 0.9, 0.9, fill=0.06)
            s.ln(mx + sgn * 9, my - 292, mx + sgn * 60, my - 278, 0.5, 0.5)

        # cargo pod with six containers
        for sgn in (-1, 1):
            x0 = mx + 10 if sgn > 0 else mx - 110
            s.rect(x0, my - 278, 100, 166, 0.95, 1.1, fill=0.05)
            for k in range(3):
                s.rect(x0 + 10, my - 268 + k * 52, 80, 42, 0.7, 0.6, fill=0.05)
                s.ln(x0 + 10, my - 268 + k * 52, x0 + 90, my - 226 + k * 52, 0.25, 0.4)
        for sgn in (-1, 1):
            s.ln(mx + sgn * 60, my - 112, mx + sgn * 90, my - 100, 0.6, 0.6)
            s.ln(mx + sgn * 20, my - 112, mx + sgn * 40, my - 100, 0.6, 0.6)

        # traction drive: four roller pairs
        s.rect(mx - 132, my - 100, 264, 252, 0.95, 1.1, fill=0.04)
        for yo in (-66, -6, 54, 114):
            for sgn in (-1, 1):
                x, y = mx + sgn * 31, my + yo
                s.circ(x, y, 24, 0.95, 1.0, fill=0.08)
                s.circ(x, y, 8, 0.8, 0.6)
                for d in range(0, 360, 60):
                    s.ln(*polar(x, y, 8, d + yo), *polar(x, y, 24, d + yo), 0.4, 0.45)
                hx = x + sgn * 26
                s.rect(min(hx, hx + sgn * 58), y - 14, 58, 28, 0.85, 0.7, fill=0.05)
                for q in range(1, 7):
                    s.ln(hx + sgn * q * 8, y - 14, hx + sgn * q * 8, y + 14, 0.3, 0.4)

        # radiators
        for sgn in (-1, 1):
            x0 = mx + sgn * 176
            left = min(x0, x0 + sgn * 44)
            s.rect(left, my - 96, 44, 244, 0.9, 0.8, fill=0.04)
            for k in range(1, 30):
                s.ln(left, my - 96 + k * 8.2, left + 44, my - 96 + k * 8.2, 0.3, 0.4)
            for yo in (-60, 110):
                s.ln(mx + sgn * 132, my + yo, x0, my + yo, 0.7, 0.6)

        # receiver disc, facing down
        s.poly([(mx - 392, my + 256), (mx + 392, my + 256), (mx + 380, my + 274), (mx - 380, my + 274)], 0.95, 1.1, fill=0.10)
        for k in range(-19, 20):
            s.ln(mx + k * 20, my + 274, mx + k * 20, my + 280, 0.6, 0.45, color=ARC)
        for sgn in (-1, 1):
            s.ln(mx + sgn * 132, my + 152, mx + sgn * 372, my + 256, 0.8, 0.7)
            s.ln(mx + sgn * 80, my + 152, mx + sgn * 200, my + 256, 0.6, 0.6)
            s.ln(mx + sgn * 132, my + 100, mx + sgn * 372, my + 256, 0.35, 0.5)

        # altitude scale
        sx = mx - 520
        s.ln(sx, my - 380, sx, my + 300, 0.5, 0.6)
        for k in range(35):
            s.ln(sx, my + 300 - k * 20, sx + (9 if k % 5 == 0 else 4), my + 300 - k * 20, 0.5 if k % 5 == 0 else 0.3, 0.45)
        for frac, lab in ((0, "0"), (0.333, "12 000"), (0.667, "24 000"), (1, "36 000 km")):
            s.text(lab, sx - 8, my + 300 - 680 * frac + 3, 7, a=0.7, align="r")
        ya = my + 300 - 680 * 0.344
        s.diamond(sx, ya, 6, 0.95, 0.8, fill=0.9, color=ARC)
        s.text("ALT 12 400 km", sx + 14, ya + 3, 7, a=0.9, color=ARC)
        s.text("ALTITUDE", sx - 8, my - 400, 6.5, a=0.5, align="r")

        enrich(s, "tether-climber", mx, my)

        s.leader(mx - 6, my - 440, -140, 30, -110, "RIBBON", "1 m WIDE / 12 µm THICK")
        s.leader(mx + 56, my - 340, 200, -50, 110, "DEBRIS SHIELD", None)
        s.leader(mx + 110, my - 200, 170, -30, 110, "CARGO POD", "6 CONTAINERS")
        s.leader(mx + 46, my - 6, 250, 0, 110, "TRACTION DRIVE", "8 ROLLERS")
        s.leader(mx + 210, my + 100, 90, 60, 110, "RADIATOR", None)
        s.leader(mx - 300, my + 264, -60, 90, -110, "LASER RECEIVER", "TUNED TO ONE WAVELENGTH")
        s.leader(mx - 22, my + 420, -170, 40, -110, "POWER BEAM", None)
    s.end_main()

    s.legend("TETHER CLIMBER", "MODEL TC-20   /   SPACE ELEVATOR CARGO CAR",
             "Climbs a ribbon from an ocean platform to geostationary orbit on beamed laser "
             "power. Puts cargo in orbit without rockets, at the price of air freight.",
             [("MATERIALS SCIENCE", "Carbon nanotube ribbon spun by the kilometre with no weak points, forty times stronger than steel cable."),
              ("PHOTONICS", "Megawatt lasers with adaptive optics that hold a beam on a moving receiver through the atmosphere."),
              ("PHOTOVOLTAICS", "Cells that turn more than half of the laser light into electricity."),
              ("ORBIT CONTROL", "Tracking of every object above 1 cm, and a ribbon that can be steered out of its way.")],
             "2075")
    from triptych import auxiliary_panel, original_diagrams
    from tether_details import system as tether_system, ribbon as tether_ribbon
    with auxiliary_panel(s, 'B', lx, rx):
        tether_system(s,lx)
    with auxiliary_panel(s, 'C', lx, rx):
        tether_ribbon(s,rx)
    original_diagrams(s)
    return s


# ---------------------------------------------------------------------------
# Cortical mesh
# ---------------------------------------------------------------------------

def cortical_mesh(size):
    s = start(size, "cortical-mesh", 404)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my, 478, a0=110, thick=(250, 300), thin=(40, 80))
    from hardware3d.family_drawing import enabled as hardware_enabled, draw as draw_hardware
    if hardware_enabled('cortical-mesh'):
        draw_hardware(s, 'cortical-mesh', mx, my)
        c = s.c
    else:

        # the web: radial threads joined by rings
        N = 48
        ends = []
        for i in range(N):
            ends.append(340 + 70 * math.sin(i * 0.9) + 30 * math.sin(i * 2.3 + 1) + s.rng.uniform(-14, 14))
        rings = [118 + k * 38 for k in range(9)]

        def node(i, r):
            d = 360 * i / N
            return polar(mx, my, r * (1 + 0.012 * math.sin(math.radians(d * 5 + r))), d + 2.2 * math.sin(r / 50.0 + i))
        for i in range(N):
            pts = [polar(mx, my, 78, 360 * i / N)] + [node(i, r) for r in rings if r <= ends[i]]
            pts.append(node(i, ends[i]))
            s.poly(pts, 0.6, 0.5, close=False)
            s.dot(*pts[-1], 2.0, 0.9)
        for r in rings:
            run = []
            for i in range(N + 1):
                j = i % N
                if r <= ends[j]:
                    run.append(node(j, r))
                else:
                    if len(run) > 1:
                        s.poly(run, 0.4, 0.45, close=False)
                    run = []
            if len(run) > 1:
                s.poly(run, 0.4, 0.45, close=False)
        count = 0
        for i in range(N):
            for r in rings:
                if r <= ends[i]:
                    count += 1
                    x, y = node(i, r)
                    if count % 7 == 0:
                        s.circ(x, y, 3.4, 0.95, 0.7, fill=0.5, color=ARC)
                    else:
                        s.dot(x, y, 1.3, 0.85)

        # the can in the middle
        s.circ(mx, my, 78, 0.95, 1.2, fill=0.07)
        s.ticks(mx, my, 70, 48, 8, 0.6, 0.5)
        s.circ(mx, my, 70, 0.5, 0.5)
        for r in (62, 58, 54):
            s.circ(mx, my, r, 0.85, 0.7, color=ARC)
        s.rect(mx - 26, my - 26, 52, 52, 0.95, 0.9, fill=0.14)
        for k in range(-3, 4):
            for sgn in (-1, 1):
                s.ln(mx + k * 7, my + sgn * 26, mx + k * 7, my + sgn * 33, 0.7, 0.5)
                s.ln(mx + sgn * 26, my + k * 7, mx + sgn * 33, my + k * 7, 0.7, 0.5)
        px, py = polar(mx, my, 92, 140)
        s.circ(px, py, 9, 0.9, 0.8)
        s.cross(px, py, 13, 0.5, 0.45)

        x, y = node(18, rings[5])
        enrich(s, "cortical-mesh", mx, my)

        s.leader(x, y, -170, 90, -110, "MESH THREAD", "POLYMER AND GOLD / 1 µm THICK")
        x, y = node(3, rings[6])
        s.leader(x, y, 150, -60, 110, "RECORDING SITE", "ONE PER NEURON-SIZED NODE")
        s.leader(mx + 18, my - 12, 330, -330, 110, "DECODER CHIP", None)
        s.leader(*polar(mx, my, 58, 200), -300, -250, -110, "POWER COIL", "DRIVEN BY ULTRASOUND")
        s.leader(px, py, -290, 170, -110, "INSERTION PORT", "Ø 2 mm")
        s.leader(mx - 60, my + 50, -260, 330, -110, "SEALED CAN", "TITANIUM / Ø 18 mm")
        s.dim(mx - 462, my + 400, mx - 462, my - 400, "Ø 64 mm UNFOLDED", a=0.4, label_shift=90)
    s.end_main()

    s.legend("CORTICAL MESH", "MODEL CM-6   /   IMPLANTED NEURAL INTERFACE",
             "Reads and writes the activity of a million neurons. Gives back sight, speech and movement "
             "after injury or stroke. Unfolds through a small opening in the skull.",
             [("BIOELECTRONICS", "Electrode mesh as soft as brain tissue, so no scar forms around it and signals last for decades."),
              ("NEUROSCIENCE", "A worked-out code for how groups of neurons represent images, words and intended movement."),
              ("CHIP DESIGN", "Decoding every channel inside the implant on too little power to warm the tissue."),
              ("ACOUSTICS", "Power and data sent through intact bone by focused ultrasound, with no wire through the skin.")],
             "2062")
    from triptych import auxiliary_panel, original_diagrams
    with auxiliary_panel(s, 'B', lx, rx):
        from left_aux_panels import tissue
        tissue(s,lx)
        # Preserve the legacy RNG stream used by the existing activity raster.
        for _ in range(22):s.rng.uniform(-6,6)
        for _ in range(13):s.rng.uniform(-10,10)
    from original_charts import draw as right_chart
    right_chart(s)
    with auxiliary_panel(s, 'C', lx, rx):
        from right_aux_panels import node
        node(s,rx)
    original_diagrams(s)
    return s


# ---------------------------------------------------------------------------
# Fusion transport
# ---------------------------------------------------------------------------

def fusion_transport(size):
    s = start(size, "fusion-transport", 505)
    mx, my, lx, rx = centres(s)
    my -= 10
    s.begin_main(mx + 80, my)
    from hardware3d.family_drawing import enabled as hardware_enabled, draw as draw_hardware
    if hardware_enabled('fusion-transport'):
        framing(s, mx, my - 30, 476)
        draw_hardware(s, 'fusion-transport', mx, my)
    else:
        x0 = mx - 560
        s.ln(x0 - 60, my, mx + 1330, my, 0.2, 0.5, dash=[18, 4, 3, 4])

        # exhaust
        for k in range(-8, 9):
            s.fade_ln(mx + 716, my + k * 6, mx + 1400, my + k * 6 + k * 17, 0.75 - abs(k) * 0.05, 0.0, 0.6, ARC)

        # bow shield, command module
        s.rect(x0, my - 62, 10, 124, 0.95, 1.0, fill=0.25)
        s.poly([(x0 + 10, my - 50), (x0 + 62, my - 24), (x0 + 62, my + 24), (x0 + 10, my + 50)], 0.8, 0.7)
        s.rect(x0 + 62, my - 36, 108, 72, 0.95, 1.1, fill=0.05)
        for k in range(5):
            s.rect(x0 + 74 + k * 18, my - 22, 9, 6, 0.8, 0.5, fill=0.4)
        s.ln(x0 + 62, my + 8, x0 + 170, my + 8, 0.4, 0.5)

        # crew ring, seen edge-on
        s.rect(x0 + 170, my - 30, 70, 60, 0.9, 0.9, fill=0.06)
        s.rect(x0 + 188, my - 176, 34, 352, 0.95, 1.2, fill=0.07)
        s.ln(x0 + 205, my - 176, x0 + 205, my + 176, 0.35, 0.5, dash=[4, 3])
        for k in range(-8, 9):
            s.ln(x0 + 188, my + k * 20, x0 + 222, my + k * 20, 0.3, 0.4)
        s.ellipse(x0 + 205, my - 200, 34, 9, a0=150, a1=390, a=0.7, w=0.7)
        s.arrow(x0 + 236, my - 196, x0 + 232, my - 191, 0.8, 0.6, head=6)

        # spine and tanks
        truss(s, x0 + 240, my, mx + 330, my, depth=26, bay=26)
        for k in range(3):
            for sgn in (-1, 1):
                tx, ty = x0 + 310 + k * 104, my + sgn * 62
                s.circ(tx, ty, 47, 0.95, 1.1, fill=0.05)
                s.ellipse(tx, ty, 47, 13, a=0.35, w=0.5)
                s.ellipse(tx, ty, 13, 47, a=0.35, w=0.5)
                s.rect(tx - 5, my + sgn * 13 - (2 if sgn < 0 else 0), 10, 2, 0.8, 0.6)

        # droplet radiators
        xa, xb = mx - 70, mx + 300
        for sgn in (-1, 1):
            apex = (mx + 115, my + sgn * 345)
            s.rect(xa, my + sgn * 13 - (8 if sgn < 0 else 0), xb - xa, 8, 0.9, 0.8, fill=0.15)
            for k in range(38):
                x = xa + 4 + k * (xb - xa - 8) / 37
                s.ln(x, my + sgn * 21, apex[0] + (k - 18.5) * 0.5, apex[1] - sgn * 8, 0.32, 0.4, dash=[1.2, 2.6], color=ARC)
            s.ln(xa, my + sgn * 21, apex[0] - 12, apex[1], 0.8, 0.7)
            s.ln(xb, my + sgn * 21, apex[0] + 12, apex[1], 0.8, 0.7)
            s.rect(apex[0] - 14, apex[1] - 7, 28, 14, 0.95, 0.9, fill=0.2)
            s.ln(apex[0], apex[1] - sgn * 7, apex[0], my + sgn * 21, 0.3, 0.45, dash=[6, 3])

        # shield, power conversion, reactor
        def shield():
            s.c.rectangle(mx + 330, my - 74, 16, 148)
        s.hatch(shield, 4, 45, 0.45)
        s.rect(mx + 330, my - 74, 16, 148, 0.95, 1.0)
        s.rect(mx + 346, my - 40, 54, 80, 0.9, 0.8, fill=0.06)
        for k in range(1, 5):
            s.ln(mx + 346 + k * 11, my - 40, mx + 346 + k * 11, my + 40, 0.3, 0.4)
        s.rect(mx + 400, my - 46, 210, 92, 0.95, 1.2, fill=0.04)
        for k in range(7):
            for sgn in (-1, 1):
                bx, by = mx + 412 + k * 28, my + sgn * 50 - (26 if sgn < 0 else 0)
                s.rect(bx, by, 16, 26, 0.9, 0.7, fill=0.08)
                s.ln(bx, by, bx + 16, by + 26, 0.4, 0.4)
                s.ln(bx + 16, by, bx, by + 26, 0.4, 0.4)
        for i, (rx_, ry_) in enumerate(((86, 32), (66, 24), (46, 16), (24, 8))):
            s.ellipse(mx + 505, my, rx_, ry_, a=0.5 + 0.14 * i, w=0.6 if i else 1.1, color=ARC)
        s.cross(mx + 505, my, 5, 0.9, 0.6, color=ARC)

        # magnetic nozzle
        for sgn in (-1, 1):
            s.bez((mx + 610, my + sgn * 46), (mx + 650, my + sgn * 50), (mx + 690, my + sgn * 90), (mx + 724, my + sgn * 140), 0.95, 1.1)
            s.rect(mx + 626, my + sgn * 64 - (30 if sgn < 0 else 0), 22, 30, 0.9, 0.8, fill=0.1)
            s.rect(mx + 668, my + sgn * 98 - (30 if sgn < 0 else 0), 22, 30, 0.9, 0.8, fill=0.1)
            for q, al in ((0.35, 0.5), (0.65, 0.35)):
                s.bez((mx + 610, my + sgn * 40 * q), (mx + 680, my + sgn * 44 * q), (mx + 730, my + sgn * 120 * q),
                      (mx + 800, my + sgn * 230 * q), al, 0.5, color=ARC)

        enrich(s, "fusion-transport", mx, my)

        s.leader(x0 + 205, my - 176, -40, -70, -100, "CREW RING", "0.4 g AT 2 rpm")
        s.leader(x0 + 5, my + 62, 40, 110, 100, "DUST SHIELD", None)
        s.leader(x0 + 414, my + 106, 30, 120, 110, "PROPELLANT TANKS", "DEUTERIUM AND HELIUM-3")
        s.leader(mx + 40, my - 190, -110, -90, -120, "DROPLET RADIATOR", "LIQUID TIN / 25 MW")
        s.leader(mx + 115, my + 345, 60, 40, 110, "DROPLET COLLECTOR", None)
        s.leader(mx + 338, my - 74, 40, -150, 110, "SHADOW SHIELD", None)
        s.leader(mx + 505, my + 22, -30, 170, -110, "FUSION CORE", "FIELD-REVERSED PLASMA")
        s.leader(mx + 690, my - 124, 50, -90, 110, "MAGNETIC NOZZLE", None)
        s.dim(x0, my - 420, mx + 724, my - 420, "184 m", a=0.4)
        s.ln(x0, my - 62, x0, my - 426, 0.1, 0.4)
        s.ln(mx + 724, my - 140, mx + 724, my - 426, 0.1, 0.4)
    s.end_main()

    s.legend("FUSION TRANSPORT", "CLASS FT-2   /   DIRECT FUSION DRIVE",
             "Takes a crew to Mars in 75 days instead of eight and a half months, which cuts their radiation dose and "
             "bone loss by two thirds. One reactor both drives the ship and powers it.",
             [("PLASMA PHYSICS", "A stable, self-contained plasma ring hot enough to burn deuterium with helium-3, a reaction that releases few neutrons."),
              ("SUPERCONDUCTIVITY", "20-tesla magnet coils wound from high-temperature superconductor, light enough to launch."),
              ("THERMAL ENGINEERING", "Radiators made of free-flying droplets of liquid metal, a tenth of the mass of solid panels."),
              ("SPACE RESOURCES", "A steady supply of helium-3, bred in reactors on Earth or sieved from lunar soil.")],
             "2072")
    from triptych import auxiliary_panel, original_diagrams
    with auxiliary_panel(s, 'B', lx, rx):
        from fusion_transit import draw as draw_transit
        draw_transit(s,lx)
    from original_charts import draw as right_chart
    right_chart(s)
    with auxiliary_panel(s, 'C', lx, rx):
        qx, qy = rx + 40, 255
        hardware_view(s,'fusion-transport-front',qx,qy,520,355)
        from hardware3d.secondary_drawing import fitted_size
        _,view_h=fitted_size('fusion-transport-front',520,355)
        s.ln(qx-195,qy,qx+195,qy,.2,.5,dash=[12,4,2,4])
        s.ln(qx,qy-view_h/2-8,qx,qy+view_h/2+8,.2,.5,dash=[12,4,2,4])
        s.view_label(qx, qy - 225, "C", "CREW RING / AXIAL SECTION", "DUST SHIELD OMITTED")
    original_diagrams(s)
    return s


# ---------------------------------------------------------------------------
# Air refinery
# ---------------------------------------------------------------------------

def air_refinery(size):
    s = start(size, "air-refinery", 606)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my - 30, 476, a0=95, thick=(225, 262), thin=(330, 372))
    from hardware3d.family_drawing import enabled as hardware_enabled, draw as draw_hardware
    if hardware_enabled('air-refinery'):
        draw_hardware(s, 'air-refinery', mx, my)
        c = s.c
    else:
        g = my + 330

        # ground
        s.ln(mx - 480, g, mx + 450, g, 0.8, 0.9)
        for k in range(-24, 23):
            s.ln(mx + k * 20, g, mx + k * 20 - 9, g + 11, 0.3, 0.45)
        s.ln(mx - 480, g + 26, mx - 130, g + 26, 0.5, 0.6, dash=[5, 3], color=ARC)
        s.ln(mx - 130, g + 26, mx - 130, g, 0.5, 0.6, dash=[5, 3], color=ARC)
        s.text("WATER", mx - 470, g + 42, 6.5, a=0.6, color=ARC)

        # mirror field and its rays
        target_l, target_r = (mx - 62, my - 178), (mx + 62, my - 178)
        field = [(mx - 450 + k * 40, target_l) for k in range(7)] + [(mx + 352 + k * 40, target_r) for k in range(3)]
        for hx, tgt in field:
            s.ln(hx, g, hx, g - 22, 0.8, 0.7)
            tilt = math.degrees(math.atan2(tgt[1] - (g - 22), tgt[0] - hx)) / 2 - 45
            x1, y1 = polar(hx, g - 22, 17, tilt)
            x2, y2 = polar(hx, g - 22, 17, tilt + 180)
            s.ln(x1, y1, x2, y2, 0.95, 1.4)
            s.ln(hx, g - 22, tgt[0], tgt[1], 0.3, 0.45, dash=[2, 4], color=GOLD)
            s.fade_ln(hx, g - 22, hx + (30 if hx < mx else -30), g - 140, 0.3, 0.0, 0.45, GOLD)

        # tower shaft, in section
        for sgn in (-1, 1):
            def wall(sgn=sgn):
                s.c.rectangle(mx + sgn * 50 - (12 if sgn < 0 else 0), my - 240, 12, g - (my - 240))
            s.hatch(wall, 4.5, 45 * sgn, 0.4)
            s.rect(mx + sgn * 50 - (12 if sgn < 0 else 0), my - 240, 12, g - (my - 240), 0.95, 1.0)
            s.rect(mx + sgn * 62 - (0 if sgn > 0 else 10), my - 196, 10, 36, 0.95, 0.8, fill=0.5, color=GOLD)
        for k in range(7):
            y = my - 206 + k * 72
            col = ARC if k < 3 else WHITE

            def bed(y=y):
                s.c.rectangle(mx - 50, y, 100, 30)
            s.hatch(bed, 5, 45, 0.5, color=col)
            s.hatch(bed, 5, -45, 0.5, color=col)
            s.rect(mx - 50, y, 100, 30, 0.9, 0.8, color=col)
            if k < 6:
                s.arrow(mx, y + 38, mx, y + 64, 0.6, 0.6, head=5)
        s.poly([(mx - 150, g), (mx - 108, my + 252), (mx - 62, my + 252)], 0.8, 0.8, close=False)
        s.poly([(mx + 150, g), (mx + 108, my + 252), (mx + 62, my + 252)], 0.8, 0.8, close=False)

        # air contactor on top
        s.poly([(mx - 62, my - 240), (mx - 120, my - 252), (mx + 120, my - 252), (mx + 62, my - 240)], 0.8, 0.7)
        s.rect(mx - 224, my - 362, 448, 110, 0.95, 1.2, fill=0.04)
        for k in range(1, 37):
            s.ln(mx - 224 + k * 12.1, my - 356, mx - 224 + k * 12.1, my - 258, 0.35, 0.45)
        s.ln(mx - 224, my - 307, mx + 224, my - 307, 0.6, 0.6)
        for fx in (-144, 0, 144):
            s.rect(mx + fx - 46, my - 394, 92, 32, 0.9, 0.8, fill=0.06)
            s.ellipse(mx + fx, my - 378, 38, 9, a=0.8, w=0.6)
            s.ln(mx + fx - 38, my - 378, mx + fx + 38, my - 378, 0.4, 0.4)
            s.arrow(mx + fx, my - 402, mx + fx, my - 440, 0.6, 0.7, head=6)
        for sgn in (-1, 1):
            for yo in (-336, -280):
                s.arrow(mx + sgn * 330, my + yo, mx + sgn * 238, my + yo, 0.8, 0.8, head=7, color=ARC)
        s.text("AIR IN, 415 ppm CO₂", mx - 340, my - 300, 6.5, a=0.8, align="r", color=ARC)
        s.text("AIR OUT, 120 ppm", mx + 60, my - 446, 6.5, a=0.6)

        # electrolyser, left of the tower
        s.rect(mx - 172, g - 70, 84, 70, 0.95, 1.0, fill=0.05)
        for k in range(1, 12):
            s.ln(mx - 172 + k * 7, g - 62, mx - 172 + k * 7, g - 8, 0.4, 0.45)
        s.poly([(mx - 88, g - 40), (mx - 62, g - 40)], 0.9, 1.0, close=False, color=ARC)

        # product tanks, right of the tower
        for tx, r in ((mx + 176, 46), (mx + 280, 38)):
            ty = g - 16 - r
            s.circ(tx, ty, r, 0.95, 1.1, fill=0.05)
            s.ellipse(tx, ty, r, r * 0.28, a=0.35, w=0.5)
            for sgn in (-1, 1):
                s.ln(tx + sgn * r * 0.7, ty + r * 0.7, tx + sgn * r * 0.8, g, 0.7, 0.6)
        s.poly([(mx + 62, g - 30), (mx + 118, g - 30), (mx + 118, g - 62), (mx + 130, g - 62)], 0.9, 0.9, close=False, color=GOLD)
        s.ln(mx + 222, g - 62, mx + 242, g - 54, 0.8, 0.7, color=GOLD)

        enrich(s, "air-refinery", mx, my)

        s.leader(mx + 160, my - 330, 150, -70, 120, "AIR CONTACTOR", "SORBENT PANELS / RELEASE AT 60 °C")
        s.leader(mx + 30, my - 120, 250, -40, 120, "ENZYME BEDS", "CO₂ TO FORMATE")
        s.leader(mx + 30, my + 98, 250, -30, 120, "CATALYST BEDS", "FORMATE AND H₂ TO C₈ – C₁₆ CHAINS")
        s.leader(mx - 67, my - 178, -190, -60, -120, "SOLAR RECEIVER", "PROCESS HEAT AT 250 °C")
        s.leader(mx - 330, g - 24, -30, -130, -80, "MIRROR FIELD", None)
        s.leader(mx - 130, g - 70, -80, -90, -100, "ELECTROLYSER", "WATER TO H₂ AND O₂")
        s.leader(mx + 280, g - 92, 70, -100, 110, "PRODUCT TANKS", None)
        s.dim(mx - 300, g, mx - 300, my - 394, "118 m", a=0.4, label_shift=40)
    s.end_main()

    s.legend("AIR REFINERY", "UNIT AR-1   /   CARBON DIOXIDE TO JET FUEL",
             "Makes jet fuel from air, water and sunlight. One tower fixes as much CO₂ as two\u00a0million "
             "trees and turns it into fuel.",
             [("SYNTHETIC BIOLOGY", "Designed carbon-fixing enzymes, twenty times faster than the one plants use, that keep working outside a cell."),
              ("CATALYSIS", "Catalysts that build long fuel molecules from CO₂ and hydrogen in one pass, without precious metals."),
              ("MATERIALS SCIENCE", "Sorbents that pull CO₂ out of open air and let it go again with gentle heat, for a quarter of today's energy."),
              ("ELECTROCHEMISTRY", "Electrolysers that split water at 95 % efficiency with iron and nickel in place of iridium.")],
             "2055")
    from triptych import auxiliary_panel, original_diagrams
    with auxiliary_panel(s, 'B', lx, rx):
        dx, dy = lx, 300
        s.detail_ring(dx, dy, 150)
        s.begin_clip_circle(dx,dy,149)
        micro_details.pellet(s,dx,dy)
        s.end_clip()
        s.ln(dx-110,dy+168,dx-50,dy+168,.9,1)
        s.text('200 nm',dx-80,dy+160,6.5,a=.8,align='c')
        micro_details.advance_legacy_rng(s,'pellet')
        s.view_label(dx, dy + 190, "B", "BED PELLET", "ENZYMES FIXED IN POROUS SILICA")
    from original_charts import draw as right_chart
    right_chart(s)
    with auxiliary_panel(s, 'C', lx, rx):
        from right_panel_studies import refinery as refinery_process
        refinery_process(s,rx)
    original_diagrams(s)
    return s


SHEETS = [
    ("organ-foundry", organ_foundry),
    ("quantum-simulator", quantum_simulator),
    ("tether-climber", tether_climber),
    ("cortical-mesh", cortical_mesh),
    ("fusion-transport", fusion_transport),
    ("air-refinery", air_refinery),
]
