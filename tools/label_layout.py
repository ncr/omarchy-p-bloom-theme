"""Reviewed callout offsets in design units; anchors and wording stay fixed.

Keep labels outside the drawn parts, including long second lines. Values are
relative to each authored leader elbow, before the main-view transform.
"""

LABEL_OFFSETS = {'quantum-simulator': {'PULSE-TUBE COOLER': (0, 32),
                       'CONTROL CHIPS': (90, 0),
                       'OPTICAL LINK': (90, 0),
                       'HEAT EXCHANGER': (90, 0),
                       'MIXING CHAMBER': (90, 0),
                       'MAGNETIC SHIELD': (90, 0),
                       'PROCESSOR STACK': (0, 8),
                       'CONTROL LINES': (0, 8)},
 'sky-racer': {'CRASH CELL': (0, 32), 'LITHIUM-AIR PACK': (24, 32)},
 'greener': {'ANTENNA WIRE': (-8, 24), 'SHRUB': (32, -16)},
 'cortical-mesh': {'MESH THREAD': (-88, 8), 'POWER COIL': (-112, 16)},
 'air-refinery': {'SOLAR RECEIVER': (-48, 0), 'ELECTROLYSER': (-112, -40)},
 'tether-climber': {'POWER BEAM': (-8, 0)},
 'truth-lamp': {'SEAT 4': (0, -8), 'DOG': (240, 10), 'DINNER': (0, 80)},
 'organ-foundry': {'VASCULAR TREE': (16, 0)},
 'volumetric-stage': {'BRIDGE': (104, 16), 'TOWER': (0, 16)},
 'proxy': {'WAVING HAND': (0, 8)},
 'presence-rig': {'INNER-EAR PADS': (190, 0),
                  'MUSCLE BAND': (152, 0),
                  'TACTILE SKIN': (136, 0)}}

# Additional clearance from the emblem when secondary views are omitted.
COMPACT_OFFSETS = {
    'aroma-organ': {'SCRUBBER': (-160, 48)},
    'volumetric-stage': {'HAZE UNIT': (0, -72)},
}
