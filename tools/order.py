"""The order of the sheets, and the colour mood of each one.

Omarchy cycles backgrounds by file name, so this list is the order people see.
It is arranged by hand: neighbours are far apart in hue, so every switch
changes how the desktop feels, and the serious sheets, the playful ones and the
three jokes take turns. The first sheet is the one a new user sees; it sits
closest to the theme's own navy.

The file name prefix comes from the position here; to reorder, move a line.
The "NCR-126" printed on a sheet is its permanent number from
docs/collection/ncr-registry.json and never follows the position.
"""

# (sheet, palette from sheet.PALETTES)
# Greener (04) and Truth Lamp (10) left the collection on 2026-09-27; they
# stay here so every other original keeps its position, id and file name.
# docs/collection/catalog.json decides what is in the collection.
ORDER = [
    ("quantum-simulator", "teal"),
    ("sky-racer", "cobalt"),
    ("fusion-transport", "crimson"),
    ("greener", "emerald"),
    ("cortical-mesh", "violet"),
    ("bounder", "graphite"),
    ("air-refinery", "saffron"),
    ("aroma-organ", "crimson"),
    ("tether-climber", "emerald"),
    ("truth-lamp", "saffron"),
    ("organ-foundry", "teal"),
    ("volumetric-stage", "cobalt"),
    ("proxy", "saffron"),
    ("presence-rig", "copper"),
]

TOTAL = len(ORDER)


def number(sheet):
    """The permanent NCR number printed on the sheet (docs/collection/ncr-registry.json).

    It is not the list position: reordering ORDER changes file names and the
    desktop sequence, never a sheet's identity.
    """
    import json, os
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'collection', 'ncr-registry.json')
    with open(path) as f:
        return json.load(f)['originals'][sheet]


def palette(sheet):
    return dict(ORDER)[sheet]
