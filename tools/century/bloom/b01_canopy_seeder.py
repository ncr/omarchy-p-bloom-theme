"""b01 CANOPY SEEDER: text, field notes and side diagrams.

Numbers are narrative, kept consistent with the model notes:
2 400 pods x 4.5 g = 10.8 kg; one pod per m2 -> 0.24 ha per sortie;
one pod per second at 1 m/s over a 1 m row -> 40 min of planting;
38 min sortie + 12 min reload -> 9 sorties a day -> 2.2 ha per aircraft,
six aircraft -> 13 ha a day. Hover power ~7.4 kW (55 kg, two 1.24 m rotors,
figure of merit 0.7) -> 4.7 kWh battery for a 38 min sortie.
"""
import math

ENTRY = dict(
    id='b01', series='B01', number=201, slug='canopy-seeder', title='CANOPY SEEDER',
    domain='reforestation', category='serious', model='CS-4', palette='moss', seed=260101,
    purpose='AERIAL REFORESTATION DRONE',
    narrative=('Replants a burned hillside with one mapped seed pod per square metre, choosing '
               'the species for each patch of slope and moisture. Six aircraft plant thirteen '
               'hectares a day; volunteers from the valley load the magazines.'),
    enabled_by=[
        ('TERRAIN MAPPING', 'Lidar and multispectral cameras that map slope, ash and soil moisture to a 5 cm grid.'),
        ('TILT-ROTOR FLIGHT', 'Electric proprotors that hover to plant and tilt forward to cruise between plots.'),
        ('SEED COATINGS', 'Clay-and-fibre pods carrying seed, mycorrhizal spores and a wetting agent.'),
    ],
    real_basis='Tilt-rotor drones, lidar terrain mapping and seed pods with mycorrhizal coatings.',
    required_breakthroughs='Pods that germinate reliably on degraded, water-repellent burned soil.',
    view_A='TILT-ROTOR SEEDING AIRCRAFT',
    view_B='SEED MAGAZINE', view_B_note='FOUR SPECIES CANISTERS / ROTARY SELECTOR',
    view_C='POD INJECTOR', view_C_note='CHARGE SETS DEPTH / CHAMBERED POD / SHROUD',
    service_year='2032',
    sources=['https://www.fs.usda.gov/research/treesearch/', 'https://doi.org/10.1016/j.foreco.2021.119174'],
    source_scope='Real basis only: aerial seeding trials, post-fire soil water repellency, mycorrhizal inoculation. The aircraft, pod and all figures are an original concept.',
)

DOSSIER = dict(
    kind='sortie',
    fact=('Burned soil can shed water for months. The injector places each pod beneath '
          'that crust, where rain can still reach the seed.'),
    rows=[('PODS PER SORTIE', '2 400 / 0.24 ha'),
          ('PLANTING PACE', '1 POD EVERY SECOND AT 1 m/s'),
          ('PAYLOAD', '10.8 kg / 4.5 g PER POD'),
          ('FLEET DAY', '6 AIRCRAFT / 13 ha')],
    note='THE LAST ROW BY THE ROAD WAS PLANTED BY THE SCHOOL.',
    left=('A SPECIES FOR EVERY SQUARE METRE', 'ILLUSTRATIVE PLOT / 12 x 6 m / RULE: MAPPED MOISTURE',
          'Species follow the moisture map: pine on the dry spur, oak mid-slope, alder in the gully.'),
    right=('PLANTED UNDER THE CRUST', 'SOIL SECTION / DEPTHS IN mm / NOT TO SCALE',
           'Repellent layer depth varies by fire and soil; the air charge is set per plot.'),
)


def moisture(i, j):
    """Declared field for the illustrative plot: a gully running down the slope."""
    x = i / 11; y = j / 5
    gully = math.exp(-((x - .62 - .12 * y) / .16) ** 2)
    return .25 + .55 * gully + .18 * y   # wetter downslope (y) and in the gully


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    if side == 'left':
        cell = 22; gx = x + 20; gy = y + 2
        # Contours of the declared field, then one symbol per square metre.
        for i in range(12):
            for j in range(6):
                m = moisture(i, j)
                cx = gx + i * cell + cell / 2; cy = gy + j * cell + cell / 2
                if m < .42:      # pine: dry spur
                    s.poly([(cx, cy - 5), (cx + 4.5, cy + 3.5), (cx - 4.5, cy + 3.5)], .78, .65, close=True, color=GOLD)
                elif m < .62:    # oak: mid-slope
                    s.circ(cx, cy, 3.8, .8, .65, color=WHITE)
                else:            # alder: gully
                    s.poly([(cx, cy - 4.5), (cx + 4.5, cy), (cx, cy + 4.5), (cx - 4.5, cy)], .85, .7, close=True, color=ARC)
        s.rect(gx, gy, cell * 12, cell * 6, .35, .5)
        for i in range(1, 12):
            s.ln(gx + i * cell, gy, gx + i * cell, gy + cell * 6, .1, .4)
        for j in range(1, 6):
            s.ln(gx, gy + j * cell, gx + cell * 12, gy + j * cell, .1, .4)
        arrow(s, (gx - 10, gy + 8), (gx - 10, gy + cell * 6 - 6), WHITE)
        lx = gx + cell * 12 + 22
        s.poly([(lx + 5, gy + 10), (lx + 9.5, gy + 18.5), (lx + .5, gy + 18.5)], .78, .65, close=True, color=GOLD)
        tx(s, 'PINE / DRY', lx + 18, gy + 19, 6.6)
        s.circ(lx + 5, gy + 50, 3.8, .8, .65)
        tx(s, 'OAK / MID', lx + 18, gy + 54, 6.6)
        s.poly([(lx + 5, gy + 81), (lx + 9.5, gy + 85.5), (lx + 5, gy + 90), (lx + .5, gy + 85.5)], .85, .7, close=True, color=ARC)
        tx(s, 'ALDER / WET', lx + 18, gy + 89, 6.6)
        tx(s, '1 SQUARE = 1 m²', lx, gy + 126, 6.2, .6)
    else:
        # Soil section: ash, water-repellent layer, mineral soil; pod at 30 mm.
        x0 = x + 18; x1 = x + 300; top = y + 26
        depth = lambda mm: top + mm * 2.2
        s.ln(x0, top, x1, top, .75, .8)
        s.ln(x0, depth(8), x1, depth(8), .45, .6)
        s.ln(x0, depth(22), x1, depth(22), .45, .6)
        for k in range(0, 282, 9):
            s.ln(x0 + k, depth(22), min(x1, x0 + k + 16), depth(8), .22, .5)
        tx(s, 'ASH', x1 + 14, depth(4) + 3, 6.6)
        tx(s, 'WATER-REPELLENT', x1 + 14, depth(15) + 3, 6.6, .8, color=GOLD)
        tx(s, 'MINERAL SOIL', x1 + 14, depth(34) + 3, 6.6)
        # Rain runs off the crust at left; only the injection channel lets it down.
        for xx in (x0 + 26, x0 + 52, x0 + 78):
            arrow(s, (xx, top - 22), (xx, top - 2), WHITE)
        arrow(s, (x0 + 92, top - 5), (x0 + 132, top - 5), WHITE)
        tx(s, 'RUNS OFF', x0 + 140, top - 2, 6.4, .66)
        px = x0 + 236
        for xx in (px - 24, px, px + 24):
            arrow(s, (xx, top - 22), (xx, top - 2), WHITE)
        s.ln(px, top, px, depth(27), .55, .7, dash=[2, 3])
        arrow(s, (px - 6, depth(3)), (px - 6, depth(25)), ARC)
        s.circ(px, depth(30), 6.5, .9, .8, color=ARC)
        s.circ(px, depth(30), 3.6, .6, .55, color=ARC)
        s.ln(px + 9, depth(30), px + 22, depth(30), .4, .5)
        tx(s, 'POD AT 30 mm', px - 12, depth(30) + 3, 6.6, .8, align='r')
