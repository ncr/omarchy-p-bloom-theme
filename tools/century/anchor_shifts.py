"""Corrections for exported callout anchors that miss the part they name.

SHIFTS: (slug, view) -> {anchor name: (dx, dy)} in the exported drawing's own units (scaled with the view).
Keep each entry to the smallest move that lands the dot on the part, and say why in a comment.

SIDES: (slug, view) -> {anchor name: -1 or 1}, the label's column whatever the split by anchor x says:
where that split would send a leader across the machine, or where a shift moves a dot past a neighbour's x.

ROOM: (slug, view) -> {-1 or 1: design units}, how much lower than the standard (my + 160) that
column's labels may sit, where the part is low in the view and the column has clear space under it.
"""
SHIFTS = {
    ('quiet-stair','A'):{'VERTICAL CARRIAGES':(-39,-1)},  # c038: the front-left carriage's screw, nearest its label, not the second carriage deep in the frame
    ('seam-surgeon','A'):{'INSPECTION ARRAY':(-8,3)},  # c065: onto the inspection bogie's visible face below the pipe; the array itself sits behind the pipe in A
    ('sleep-cocoon','A'):{'RESTING WORKER':(3,29),'FOOT PLATFORM':(-34,-4)},  # c099: the chest, not beside the eye; the platform's near edge by its label
    ('reef-nursery','A'):{'SEABED ANCHOR':(-107,-64),'DAVIT':(1,39)},  # b02: the free far-left anchor block, not one behind a lattice tree; the davit post just above its winch, level with the label
    ('sun-still','A'):{'HELIOSTAT':(120,15)},  # b03: the right-hand front mirror, not the product-shed roof
    ('manta-foil','A'):{'RETRACTABLE FOILS':(6,26)},  # c006: the front hinged strut, not the hull side above it
    ('memory-kiln','A'):{'FOCUS OBJECTIVE':(-7,26)},  # c017: the objective's lower mount ring, so the leader passes under the pulse source
    ('fibre-braid','A'):{'MANDREL CHUCK':(-19,12)},  # c025: the chuck face inside the carrier ring, not a bobbin in front of it
    ('petal-eye','A'):{'SUN SHADE':(-3,-20)},  # c031: a sunshade petal, not the flat radiator panel
    ('light-sail','A'):{'MEMBRANE':(-158,-61)},  # c001: the left quadrant's film, so with CARGO SPINE gone MEMBRANE takes the left column and SAIL ROOT's leader stays off the hub
    ('key-concord','A'):{'WITHDRAWAL':(-11.5,-4.3)},  # c104: onto the knurled crown's rim, from the bolt end behind it; the leader then clears key two's bow
    ('volumetric-stage','A'):{'CLOCK DISTRIBUTION':(15,-11)},  # o12: onto the timing controller's front face, out of the truss clutter where the dot was lost
    ('green-forge','A'):{'ARC FURNACE':(2.1,4.1)},  # b13: the shell's lower left, so its label (ROOM) sits level with it under the spheres' feet and the control box
    ('wind-kite','A'):{'TRACTION WINCH':(-29.6,5.9),  # c042: the drum's near flange, so the leader stops there instead of running along the drum
                       'SWEPT SPAR':(53,-1.6)},       # c042: the spar's outer end at the canted tip, not mid-span through the ribs
    ('suture-loom','A'):{'OPEN SERVICE TRACK':(-12.6,28.3),  # c108: the horseshoe's top face on the near side; the export's point lay behind the left motor stack
                         'TEST MEMBRANE':(-40.2,2.3)},     # c108: the membrane's near corner, reached from the left (SIDES)
}

SIDES = {
    ('green-forge','A'):{'ARC FURNACE':-1,'SHAFT FURNACE':1},  # b13: both keep their columns; the furnace's new dot lies a little right of the shaft's
    ('suture-loom','A'):{'TEST MEMBRANE':-1,'DUAL NEEDLE GRIP':-1},  # c108: from the right the membrane's leader crossed the spool, the dancer post, the track and the arm; the grip stays left
}

ROOM = {
    ('green-forge','A'):{-1:115},  # b13: the arc furnace stands below the spheres; its label goes down to it, the legend is further left
}
