"""b20 QUIET SCANNER: text, field notes and side diagrams.

Numbers are narrative and kept consistent:
- Field 0.07 T from a permanent magnet (no helium, no cooling plant);
  magnet and housings about 900 kg; runs from an ordinary 230 V socket at
  about 1.2 kW while scanning.
- Sound: gradient plates on elastomer mounts, slow gradient ramps; about
  55 dB(A) at the child's ear (declared design target), against about
  110 dB(A) inside a conventional tube scanner. 55 dB is quieter than
  ordinary conversation (~60 dB). 110 - 55 = 55 dB: roughly 1/300 000 of
  the sound intensity.
- A brain series of four sequences: 22 minutes including positioning.
- Pipeline (declared, illustrative): low-field signal is noisy; many short
  acquisitions are combined and a reconstruction model trained on paired
  scans produces the image a radiologist reads. No clinical claim is made.
"""

ENTRY = dict(
    id='b20', series='B20', number=220, slug='quiet-scanner', title='QUIET SCANNER',
    domain='paediatric imaging', category='serious', model='QS-3', palette='navy', seed=260120,
    purpose='SILENT OPEN MRI FOR CHILDREN',
    narrative=('An open, quiet scanner shaped like a hammock under a ceiling of stars. A child can '
               'lie still with a parent’s hand in theirs, without sedation, while the magnet '
               'listens for twenty minutes.'),
    enabled_by=[
        ('LOW-FIELD MRI', 'Permanent-magnet scanners light enough to wheel into a ward.'),
        ('SILENT GRADIENTS', 'Flat coils on soft mounts, switched gently instead of hammered.'),
        ('RECONSTRUCTION', 'Models that turn weak, noisy signal into a readable image.'),
    ],
    real_basis='Open low-field MRI, silent gradient coils, AI image reconstruction.',
    required_breakthroughs='Diagnostic image quality from quiet low-field magnets.',
    view_A='CRESCENT MAGNET, HAMMOCK AND STAR CANOPY',
    view_B='GRADIENT PLATE', view_B_note='FINGERPRINT WINDINGS / AXIAL LOOPS / SOFT MOUNTS',
    view_C='STAR CANOPY', view_C_note='SEEN FROM BELOW / FIBRE STARS / TWO CONSTELLATIONS / DAWN STRIP',
    service_year='2033',
    sources=['https://doi.org/10.1038/s41467-021-25441-6', 'https://doi.org/10.1002/mrm.28069'],
    source_scope='Real basis only: portable low-field MRI, acoustic noise reduction in gradient systems and learned image reconstruction. The scanner, its figures and the pipeline are an original concept, not a medical device.',
)

DOSSIER = dict(
    kind='one scan',
    fact=('Children often need sedation to lie still in a loud, narrow tube. Here the '
          'magnet is open on three sides and quieter than a conversation.'),
    rows=[('FIELD', '0.07 T / PERMANENT MAGNET'),
          ('SOUND AT THE EAR', 'ABOUT 55 dB(A)'),
          ('BRAIN SERIES', '22 MIN / FOUR SEQUENCES'),
          ('POWER', 'WALL SOCKET / 1.2 kW')],
    note="TWENTY-TWO MINUTES. NO SEDATION. HER FATHER'S HAND THE WHOLE TIME.",
    left=('QUIETER THAN A CONVERSATION', 'DECLARED SOUND LEVELS / dB(A) AT THE EAR',
          'Design target, not a measurement: every 10 dB is ten times less sound energy.'),
    right=('FROM A WHISPER OF SIGNAL', 'ILLUSTRATIVE PIPELINE / NOT A CLINICAL CLAIM',
           'Many short, noisy acquisitions are combined; a trained model rebuilds the image.'),
)

LEVELS = [('TUBE MRI', 110, 'GOLD'), ('BUSY STREET', 80, 'WHITE'), ('CONVERSATION', 60, 'WHITE'),
          ('THIS SCANNER', 55, 'ARC'), ('LIBRARY', 40, 'WHITE')]


def figure(s, side, x, y, w):
    from sheet import WHITE, ARC, GOLD
    from century.editorial import tx, arrow
    cols = {'GOLD': GOLD, 'WHITE': WHITE, 'ARC': ARC}
    if side == 'left':
        x0 = x + 104; x1 = x + w - 40
        X = lambda db: x0 + (x1 - x0) * db / 120
        for db in (0, 40, 80, 120):
            s.ln(X(db), y + 2, X(db), y + 118, .12, .4)
            tx(s, str(db), X(db), y + 132, 6.2, .6, align='c')
        for i, (lab, db, col) in enumerate(LEVELS):
            yy = y + 12 + i * 24
            c = cols[col]
            tx(s, lab, x + 96, yy + 3, 6.4, .85 if col != 'WHITE' else .66, align='r', color=c if col != 'WHITE' else WHITE)
            s.ln(X(0), yy, X(db), yy, .85 if col != 'WHITE' else .45, 3.2 if col != 'WHITE' else 2.2, color=c)
            tx(s, f'{db}', X(db) + 8, yy + 3, 6.2, .75)
    else:
        # Noisy samples -> reconstruction -> image, three small panels.
        import random
        rnd = random.Random(7)
        px, py, pw = x + 4, y + 18, 96
        s.rect(px, py, pw, pw, .5, .6)
        for k in range(150):
            u, v = rnd.random(), rnd.random()
            r = ((u - .5) ** 2 + (v - .5) ** 2) ** .5
            if rnd.random() < (.9 if r < .36 else .35):
                s.dot(px + 4 + u * (pw - 8), py + 4 + v * (pw - 8), .8, .6)
        tx(s, 'RAW SIGNAL', px + pw / 2, py - 7, 6.2, .7, align='c')
        arrow(s, (px + pw + 8, py + pw / 2), (px + pw + 44, py + pw / 2), ARC)
        bx = px + pw + 52
        s.rect(bx, py + 22, 108, 52, .8, .7, color=ARC)
        tx(s, 'COMBINE', bx + 54, py + 44, 6.4, .85, align='c')
        tx(s, 'RECONSTRUCT', bx + 54, py + 60, 6.4, .85, align='c')
        arrow(s, (bx + 116, py + pw / 2), (bx + 150, py + pw / 2), ARC)
        ix = bx + 158
        s.rect(ix, py, pw, pw, .5, .6)
        cx, cy = ix + pw / 2, py + pw / 2
        s.circ(cx, cy, 36, .85, .8)
        s.circ(cx, cy, 30, .5, .6)
        for k, r in enumerate((20, 14)):
            s.circ(cx + (2 if k else 0), cy + 2, r, .45, .55, color=GOLD)
        tx(s, 'READABLE IMAGE', cx, py - 7, 6.2, .7, align='c')
        tx(s, 'ABOUT 40 SHORT ACQUISITIONS', px, py + pw + 20, 6.2, .6)
