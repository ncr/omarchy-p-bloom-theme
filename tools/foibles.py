"""Three devices that say more about their owners than about engineering.

Same rules as the other sheets — a real job, plausible breakthroughs — but
the job exists only because people are the way they are.
"""

import math
import micro_details

from devices import centres, framing, start
from leisure import cuff, limb
from fidelity import enrich, seated, diner, dog, contour, hand, front_head
from sheet import ARC, GOLD, RED, WHITE, polar
from hardware3d.accessories import rounded, model as hardware_model


# ---------------------------------------------------------------------------
# Proxy
# ---------------------------------------------------------------------------

def proxy(size):
    s = start(size, "proxy", 1212)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    from main_scene_panels import proxy as draw_main_scene
    draw_main_scene(s,mx,my)
    s.end_main()

    # Story rewritten on 2026-09-27 (owner's request): a sincere guide robot
    # for blind and low-vision runners. The drawing is unchanged. Numbers are
    # narrative and agree with each other: 10 km at 6 min/km is about an hour;
    # 3 s of warning at that pace is about 8 m, inside the 20 m the sensors read.
    s.legend("PROXY", "MODEL PX-1   /   GUIDE FOR BLIND RUNNERS",
             "Runs beside a blind or low-vision runner on a short tether, calling the pace and warning "
             "of kerbs, turns and puddles.",
             [("ROBOTICS", "Legs that run on pavement, grass and stairs without missing a step."),
              ("PERCEPTION", "Sensing that tells kerbs, cyclists, ice and wet leaves apart in time to warn the runner."),
              ("HAPTICS", "Pulses that the runner feels in the hand before every turn, kerb or step."),
              ("SPEECH", "One quiet earbud: pace, distance and the next kerb, in as few words as possible, then silence.")],
             "2047")
    from triptych import auxiliary_panel, original_diagrams
    with auxiliary_panel(s, 'B', lx, rx):
        dx, dy = lx, 300
        s.detail_ring(dx, dy, 150)
        s.begin_clip_circle(dx, dy, 149)
        rounded(s,dx-80,dy-101,160,48,15,.95,1.0,.07)
        rounded(s,dx-65,dy-96,130,15,6,.75,.65,.03)
        s.ln(dx-57,dy-73,dx+57,dy-73,.5,.5)
        for xx in (dx-68,dx+68):
            s.circ(xx,dy-66,2,.8,.5)
        rounded(s,dx+80,dy-86,9,15,3,.8,.6)
        for side in (-1,1):
            rounded(s,dx+side*97-17,dy-91,34,23,7,.75,.65)
        s.ellipse(dx,dy-56,17,4,a=.85,w=.65,color=ARC)
        s.rect(dx - 16, dy - 58, 32, 6, 0.9, 0.6, fill=0.8, color=ARC)
        for off in (-8, 0, 8):
            s.ln(dx + off, dy - 52, dx + off * 2.4, dy - 6, 0.6, 0.5, dash=[2, 3], color=ARC)

        def skin():
            s.c.rectangle(dx - 160, dy - 50, 320, 22)
        s.hatch(skin, 3, 60, 0.35)
        s.rect(dx - 160, dy - 50, 320, 22, 0.8, 0.7)
        for k in range(-4, 5):
            x = dx + k * 34 + 12
            s.ln(x, dy - 28, x, dy - 50, 0.7, 0.5)
            s.circ(x, dy - 54, 2.2, 0.9, 0.5, fill=0.6, color=ARC)
        # Longitudinal section: a continuous double-wall pulse line with a
        # shallow pressure chamber directly below the watch sensor.
        for off,alpha,width in ((0,.88,.8),(3,.55,.5)):
            yy=dy-10+off
            contour(s,[("M",dx-160,yy),("L",dx-49,yy),
                ("C",dx-38,yy,dx-36,dy-22+off,dx-25,dy-22+off),
                ("L",dx+25,dy-22+off),
                ("C",dx+36,dy-22+off,dx+38,yy,dx+49,yy),
                ("L",dx+160,yy)],a=alpha,w=width,color=RED)
            s.ln(dx-160,dy+9-off,dx+160,dy+9-off,alpha,width,color=RED)
        for xx in (dx-70,dx+70):
            for shift in (-3,3):
                s.ln(xx+shift,dy-12,xx+shift,dy+11,.65,.55,color=RED)
        s.poly([(dx - 160 + k * 12, dy + 26 + (8 if k % 2 else 0)) for k in range(28)], 0.85, 0.7, close=False, color=GOLD)

        def core():
            s.c.rectangle(dx - 160, dy + 46, 320, 120)
        s.hatch(core, 6, 45, 0.3)
        s.ln(dx - 160, dy + 46, dx + 160, dy + 46, 0.9, 0.9)
        s.end_clip()
        for yy, lab in ((dy - 76, "CUE BAND"), (dy - 39, "SOFT GRIP SKIN"), (dy - 3, "HAPTIC LINE"), (dy + 30, "HEATER, 33 °C"), (dy + 90, "ALUMINIUM")):
            s.ln(dx + 154, yy, dx + 166, yy, 0.5, 0.5)
            s.text(lab, dx + 172, yy + 3, 6.5, a=0.6)
        s.view_label(dx, dy + 190, "B", "LEFT WRIST", "SECTION / WHERE THE TETHER HAND RESTS")
    with auxiliary_panel(s, 'C', lx, rx):
        from right_aux_panels import owner as owner_panel
        owner_panel(s,rx)
    from original_charts import draw as right_chart
    right_chart(s)
    original_diagrams(s)
    return s


# ---------------------------------------------------------------------------
# Greener
# ---------------------------------------------------------------------------

def gnome(s, x, g, lens=False):
    s.c.save();s.c.translate(x,g)
    contour(s,[("M",-15,0),("C",-18,-5,-12,-8,-10,-9),("L",-12,-21),
        ("C",-12,-30,-5,-34,0,-34),("C",8,-35,13,-26,13,-20),
        ("L",10,-8),("C",22,-5,18,0,14,0),("L",3,0),("L",0,-8),("L",-2,0)],w=.8,fill=.1,close=True)
    contour(s,[("M",-11,-37),("C",-8,-49,-1,-59,4,-63),
        ("C",3,-52,12,-46,11,-37),("C",5,-33,-5,-33,-11,-37)],w=.8,fill=.14,close=True)
    contour(s,[("M",-8,-29),("C",-10,-20,-3,-13,0,-12),
        ("C",7,-17,9,-21,7,-29)],a=.7,w=.65)
    s.ellipse(0,-31,3.4,4,a=.8,w=.55)
    for k in (-4,0,4):
        s.bez((k,-25),(k+2,-20),(k,-19),(0,-15),.4,.4)
    s.bez((-9,-23),(-14,-20),(-13,-16),(-9,-15),.7,.5)
    s.bez((10,-23),(15,-20),(14,-16),(10,-15),.7,.5)
    if lens:
        s.circ(-4,-32,2.2,.9,.4,color=ARC)
        s.dot(-4,-32,.8,.95,ARC)
    s.c.restore()


def mast(s, x, g, h, toward, color):
    """A periscope pole with a camera head looking over the fence."""
    for off in (-3, 3):
        s.ln(x + off, g, x + off, g - h, 0.9, 0.8)
    for k in range(1, int(h // 40)):
        s.ln(x - 3, g - k * 40, x + 3, g - k * 40, 0.5, 0.5)
    hx = x + toward * 26
    hardware_model(s,'greener-head',min(x-toward*10,hx+toward*18),g-h-22,54,32,flip=toward)
    s.circ(hx + toward * 16, g - h - 3, 5, .85, .65, color=color)
    return hx + toward * 16, g - h - 3


def greener(size):
    s = start(size, "greener", 1313)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    framing(s, mx, my - 20, 478, a0=200, thick=(150, 190), thin=(20, 55))
    from hardware3d.family_drawing import enabled as hardware_enabled, draw as draw_hardware
    if hardware_enabled('greener'):
        draw_hardware(s, 'greener', mx, my)
    else:
        g = my + 150

        # night sky
        s.circ(mx + 360, my - 370, 26, 0.9, 0.9, fill=0.10)
        s.arc(mx + 372, my - 376, 24, 120, 250, 0.6, 0.6)
        s.text("03:00", mx + 396, my - 366, 7, a=0.7)
        for k in range(14):
            s.cross(mx - 440 + s.rng.uniform(0, 760), my - 430 + s.rng.uniform(0, 150), 2.5, 0.5, 0.45)

        # ground, soil, the two buried antenna wires
        s.ln(mx - 470, g, mx + 470, g, 0.9, 1.0)
        for k in range(60):
            x, y = mx - 460 + s.rng.uniform(0, 920), g + s.rng.uniform(16, 150)
            s.ln(x, y, x + 5, y + 4, 0.25, 0.45)
        for x0, x1 in ((mx - 360, mx - 26), (mx + 26, mx + 440)):
            s.poly([(x, g + 46 + 7 * math.sin((x - x0) / 5.0)) for x in range(int(x0), int(x1), 2)], 0.85, 0.7, close=False, color=GOLD)

        # the owner's house and control box
        s.rect(mx - 470, g - 236, 84, 236, 0.9, 1.0, fill=0.05)
        s.poly([(mx - 470, g - 236), (mx - 470, g - 290), (mx - 372, g - 236)], 0.9, 1.0, fill=0.05)
        s.rect(mx - 450, g - 190, 40, 50, 0.7, 0.6, fill=0.12)
        rounded(s,mx - 386,g - 122,28,42,7,.95,.9,.04)
        s.arc(mx-372,g-99,8,190,350,.65,.55)
        s.dot(mx - 372, g - 108, 2.4, 0.95, ARC)
        s.poly([(mx - 372, g - 82), (mx - 372, g + 46), (mx - 360, g + 46)], 0.7, 0.6, close=False, dash=[4, 3], color=GOLD)

        # fence, raised twice
        s.rect(mx - 6, g - 184, 12, 184, 0.95, 1.2, fill=0.12)
        s.rect(mx - 5, g - 240, 10, 56, 0.8, 0.8, fill=0.06, dash=[5, 3])
        s.rect(mx - 4, g - 282, 8, 42, 0.65, 0.7, fill=0.04, dash=[3, 3])

        # both units, each measuring the other lawn
        lens1 = mast(s, mx - 64, g, 318, 1, ARC)
        for k in range(7):
            s.fade_ln(lens1[0], lens1[1], mx + 90 + k * 55, g - 8, 0.6, 0.05, 0.5, ARC)
        for cx_, cy_, r in ((mx + 60, g - 40, 40), (mx + 96, g - 70, 46), (mx + 50, g - 104, 38), (mx + 100, g - 130, 34), (mx + 70, g - 160, 28)):
            s.circ(cx_, cy_, r, 0.45, 0.6, dash=[4, 3])
        lens2 = mast(s, mx + 76, g, 336, -1, GOLD)
        for k in range(7):
            s.fade_ln(lens2[0], lens2[1], mx - 90 - k * 42, g - 8, 0.6, 0.05, 0.5, GOLD)

        # grass, both sides equally and unreasonably green
        x = mx - 384
        while x < mx + 466:
            if abs(x - mx) > 9:
                h = s.rng.uniform(14, 30)
                s.ln(x, g, x + s.rng.uniform(-5, 5), g - h, s.rng.uniform(0.55, 0.98), 0.8, color=ARC)
            x += 2.6
        gnome(s, mx - 180, g)
        gnome(s, mx + 300, g, lens=True)
        s.fade_ln(mx + 297, g - 31, mx + 40, g - 60, 0.5, 0.0, 0.5, GOLD)
        for sx_ in (mx - 300, mx - 140, mx + 200, mx + 400):
            s.ln(sx_, g, sx_, g - 9, 0.9, 0.9)
            s.ln(sx_ - 6, g - 9, sx_ + 6, g - 9, 0.9, 0.9)

        enrich(s, "greener", mx, my)

        s.leader(lens1[0] - 18, lens1[1] - 6, -150, -70, -120, "PERISCOPE CAMERA", "READS THE NEIGHBOUR'S GREEN BY STARLIGHT")
        s.leader(lens2[0] + 20, lens2[1] - 6, 150, -30, 120, "THE NEIGHBOUR'S UNIT", "BOUGHT THREE WEEKS LATER / 18 mm TALLER")
        s.leader(mx + 5, g - 262, 210, 0, 110, "FENCE", "RAISED TWICE, BY BOTH PARTIES")
        s.leader(mx - 372, g - 100, -30, -190, 30, "CONTROL BOX", "SET TO: NEIGHBOUR + 4 %")
        s.leader(mx - 180, g - 50, -30, -100, -70, "GNOME", "DECOY. CONTAINS NOTHING.")
        s.leader(mx + 310, g - 46, 60, -90, 100, "THEIR GNOME", "CONTAINS A SECOND CAMERA")
        s.leader(mx - 200, g + 46, -60, 90, -110, "ANTENNA WIRE", "TELLS THE GRASS HOW GREEN TO BE")
        s.leader(mx + 118, g - 96, 80, 190, 110, "SHRUB", "PLANTED TO HIDE THE MAST. HIDES NOTHING.")
    s.end_main()

    s.legend("GREENER", "MODEL G-4   /   COMPETITIVE LAWN SYSTEM",
             "Keeps the owner's lawn exactly four per cent greener than the neighbour's. It measures their grass "
             "over the fence at night and corrects its own by morning. Most neighbours respond by buying one.",
             [("SYNTHETIC BIOLOGY", "Grass whose chlorophyll is set by a gene switch that listens to a radio signal from a wire under the turf."),
              ("REMOTE SENSING", "A camera that reads the exact green of a lawn by starlight, over a fence, from nine metres."),
              ("GAME THEORY", "A proof that two units facing each other never settle. Marketing called it a feature and sold them in pairs."),
              ("PUBLIC LAW", "A legal limit on how green grass may be, first passed in 2061 after airline pilots reported glare.")],
             "2049")
    from triptych import auxiliary_panel, original_diagrams
    with auxiliary_panel(s, 'B', lx, rx):
        dx, dy = lx, 300
        s.detail_ring(dx, dy, 150)
        s.begin_clip_circle(dx, dy, 149)
        micro_details.leaf(s,dx,dy)
        micro_details.advance_legacy_rng(s,'leaf')
        s.end_clip()
        s.view_label(dx, dy + 190, "B", "LEAF CELLS", "CHLOROPLASTS PER CELL: 40 BEFORE, 310 NOW")
    with auxiliary_panel(s, 'C', lx, rx):
        from right_aux_panels import street
        street(s,rx)
    with auxiliary_panel(s, 'plot', lx, rx):
        x0, y0, w_, h_ = rx - 170, 640, 260, 110
        f1 = lambda t: min(0.84, 0.10 + 0.05 * math.exp(4.4 * t))
        s.chart(x0, y0, w_, h_, "GREEN OF BOTH LAWNS", f1, "YEARS, 0 – 12", "")
        s.poly([(x0 + w_ * i / 60, y0 + h_ * (1 - min(0.84, 0.10 + 0.05 * math.exp(4.4 * max(0, i / 60.0 - 0.03))) + 0.03)) for i in range(61)],
               0.8, 0.9, close=False, dash=[4, 3], color=GOLD)
        s.ln(x0, y0 + h_ * 0.16, x0 + w_, y0 + h_ * 0.16, 0.7, 0.6, dash=[2, 3], color=RED)
        s.text("LEGAL LIMIT", x0 + 6, y0 + h_ * 0.16 - 5, 6, a=0.9, color=RED)
    original_diagrams(s)
    return s


# ---------------------------------------------------------------------------
# Truth lamp
# ---------------------------------------------------------------------------

def truth_lamp(size):
    s = start(size, "truth-lamp", 1414)
    mx, my, lx, rx = centres(s)
    s.begin_main(mx, my)
    from main_scene_panels import truth as draw_main_scene
    draw_main_scene(s,mx,my)
    s.end_main()

    s.legend("TRUTH LAMP", "MODEL TL-1   /   LIE DETECTOR FOR THE DINING TABLE",
             "Hangs over the table and glows red for three seconds whenever someone says a thing they do not "
             "believe. It is right 97 % of the time. Most owners unplug it before dessert.",
             [("AFFECTIVE SCIENCE", "Reading a lie from voice, face and the temperature of the nose, at three metres, without touching anyone."),
              ("SIGNAL PROCESSING", "Telling six people apart while all of them talk at once, which at this table is always."),
              ("SOCIOLOGY", "The discovery, made with this lamp, that a family dinner runs on about forty small untruths an hour and stops without them."),
              ("PRODUCT DESIGN", "An off switch. Added in version 2, and the only change in version 2.")],
             "2046")
    from triptych import auxiliary_panel, original_diagrams
    with auxiliary_panel(s, 'B', lx, rx):
        from left_aux_panels import dinner
        dinner(s,lx)
    with auxiliary_panel(s, 'C', lx, rx):
        from right_panel_studies import truth as truth_field_data
        truth_field_data(s,rx)
    with auxiliary_panel(s, 'plot', lx, rx):
        s.chart(rx - 170, 600, 260, 150, "LAMPS STILL PLUGGED IN",
                lambda t: 0.04 + 0.92 * math.exp(-9 * t), "DAYS SINCE PURCHASE, 0 – 30", "")
    original_diagrams(s)
    return s


SHEETS = [
    ("proxy", proxy),
    ("greener", greener),
    ("truth-lamp", truth_lamp),
]
