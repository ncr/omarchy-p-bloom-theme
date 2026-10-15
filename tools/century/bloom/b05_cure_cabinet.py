"""b05 CURE CABINET: text, field notes and side diagrams.

Numbers are narrative and kept consistent:
day 0 collection on the ward (about 1 x 10^9 T cells in the bag), activation;
day 1 editing in the sealed cartridge (electroporation of the editor);
days 1-6 expansion in a 1 L rocking bag at 37 C up to about 1 x 10^9 cells
(roughly 1 x 10^6 per mL), of which a dose of 2 x 10^8 is formulated;
days 6-7 release testing (count, identity, sterility) and return.
Collected on a Monday, returned the next Monday: seven days.
Nurse time about 20 minutes a day (loading, checks, sign-off).
This is a concept illustration, not a clinical device or protocol.
"""

ENTRY = dict(
    id='b05', series='B05', number=205, slug='cure-cabinet', title='CURE CABINET',
    domain='medicine', category='serious', model='CC-7', palette='berry', seed=260105,
    purpose='BEDSIDE CELL-THERAPY FOUNDRY',
    narrative=('Prepares a personalised cell therapy from a patient\'s own cells in about a week, '
               'inside the hospital that treats them. Nothing is shipped to a distant plant; '
               'the cells are grown down the corridor and return to the same ward.'),
    enabled_by=[
        ('CLOSED PROCESSING', 'Automated, sealed cell-processing systems that need no open cleanroom step.'),
        ('GENE EDITING', 'CRISPR editors delivered into T cells by electroporation in a single-use cartridge.'),
        ('CAR-T MANUFACTURE', 'Established methods to activate, expand and dose a patient\'s own T cells.'),
    ],
    real_basis='Closed automated cell processing, CRISPR editing and CAR-T manufacturing.',
    required_breakthroughs='Fully automated, validated editing and release testing at the bedside.',
    view_A='WARD CELL FOUNDRY, DOOR OPEN',
    view_B='BIOREACTOR BAY', view_B_note='SHELL OMITTED / ROCKING TRAY / BAG / GAS LINES',
    view_C='EDITING CARTRIDGE', view_C_note='REAGENT WELLS / ELECTRODE CHAMBER / BARCODE',
    service_year='2036',
    sources=['https://www.fda.gov/vaccines-blood-biologics/cellular-gene-therapy-products/approved-cellular-and-gene-therapy-products',
             'https://doi.org/10.1038/s41591-021-01436-0'],
    source_scope='Real basis only: closed automated cell processing, point-of-care CAR-T studies, CRISPR editing. The cabinet, its schedule and all figures are an original concept, not a clinical device.',
)

DOSSIER = dict(
    kind='one patient',
    fact=('The cells never leave the ward. Every line is welded closed, '
          'so the cabinet needs no cleanroom around it.'),
    rows=[('CELLS TO DOSE', 'ABOUT 7 DAYS'),
          ('DOSE', '2 × 10⁸ EDITED T CELLS'),
          ('BIOREACTOR', '1 L ROCKING BAG / 37 °C'),
          ('OPEN STEPS', 'NONE / WELDED LINES ONLY')],
    note='COLLECTED ON A MONDAY. RETURNED, READY, THE NEXT MONDAY.',
    left=('ONE WEEK, ONE PATIENT', 'DECLARED SCHEDULE / DAYS 0-7 / NOT A PROTOCOL',
          'Illustrative schedule; real processes vary by product and by patient.'),
    right=('NOTHING IS OPENED', 'CLOSED FLUID PATH / SCHEMATIC / NOT TO SCALE',
           'Each joint is a sterile weld; test samples leave through a sealed port.'),
)


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx
    if side == 'left':
        # Gantt of the declared week: day ticks, one bar per step.
        bx = x + 112; bw = w - 130; day = bw / 7
        steps = [('COLLECT', 0, .35, ARC), ('ACTIVATE', .2, 1.0, WHITE), ('EDIT', 1.0, 1.4, ARC),
                 ('EXPAND', 1.4, 6.0, WHITE), ('TEST', 6.0, 6.8, GOLD), ('RETURN', 6.8, 7.0, ARC)]
        for i, (name, a, b, col) in enumerate(steps):
            yy = y + 6 + i * 17
            tx(s, name, x, yy + 4, 6.6, .78)
            s.ln(bx, yy, bx + bw, yy, .12, .4)
            s.rect(bx + a * day, yy - 4, max(3, (b - a) * day), 8, .85, .7, color=col)
        for d in range(8):
            xx = bx + d * day
            s.ln(xx, y + 108, xx, y + 112, .4, .5)
            tx(s, str(d), xx, y + 123, 6.4, .65, align='c')
        tx(s, 'DAY', x, y + 123, 6.4, .6)
    else:
        # Closed loop: patient -> weld -> cartridge -> bag -> test -> dose -> weld -> patient.
        nodes = [('WARD', x + 30), ('CARTRIDGE', x + 125), ('BAG', x + 220), ('DOSE', x + 318), ('WARD', x + 405)]
        yy = y + 42
        for i, (name, cx) in enumerate(nodes):
            if name == 'WARD':
                # Hospital bed: headboard, mattress, pillow, two legs.
                s.ln(cx - 17, yy - 12, cx - 17, yy + 11, .85, .75)
                s.rect(cx - 17, yy - 2, 34, 7, .85, .75)
                s.rect(cx - 14, yy - 7, 9, 5, .6, .6)
                s.ln(cx - 14, yy + 5, cx - 14, yy + 11, .7, .7); s.ln(cx + 15, yy + 5, cx + 15, yy + 11, .7, .7)
            elif name == 'CARTRIDGE':
                s.rect(cx - 10, yy - 14, 20, 28, .85, .75, color=ARC)
                s.rect(cx - 5, yy - 4, 10, 12, .6, .6, color=ARC)
            elif name == 'BAG':
                s.poly([(cx - 22, yy), (cx - 14, yy - 11), (cx + 14, yy - 11), (cx + 22, yy), (cx + 14, yy + 11), (cx - 14, yy + 11)], .85, .75, close=True)
            else:
                s.poly([(cx - 9, yy - 14), (cx + 9, yy - 14), (cx + 11, yy + 12), (cx - 11, yy + 12)], .85, .75, close=True, color=ARC)
            tx(s, name, cx, yy + 32, 6.6, .8, align='c')
        # Tube runs with weld marks (small diamonds) at each joint.
        for (a, ax), (b, bx_) in zip(nodes, nodes[1:]):
            x0 = ax + (19 if a == 'WARD' else 24 if a == 'BAG' else 13)
            x1 = bx_ - (19 if b == 'WARD' else 24 if b == 'BAG' else 13)
            s.ln(x0, yy, x1, yy, .6, .7, color=GOLD)
            mx = (x0 + x1) / 2
            s.diamond(mx, yy, 3.4, .9, .7, color=GOLD)
        # Sealed sample port from the bag to the cytometer.
        s.poly([(x + 236, yy + 9), (x + 250, yy + 24), (x + 250, yy + 62)], .5, .6, close=False, color=GOLD)
        s.diamond(x + 250, yy + 48, 3.4, .9, .7, color=GOLD)
        s.rect(x + 226, yy + 62, 48, 18, .8, .7)
        tx(s, 'TEST', x + 282, yy + 75, 6.6, .8)
        s.diamond(x + 20, yy + 85, 3.4, .9, .7, color=GOLD)
        tx(s, 'STERILE WELD', x + 30, yy + 88, 6.4, .7)
