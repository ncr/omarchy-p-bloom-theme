"""Right-column charts of the original sheets, in the Century side-figure schema.

Heading, grey subtitle, chart, one-sentence caption, all on one left edge and
with the type sizes and chart strokes of the Bloom and Century figures. The
curves keep the originals' shapes; values only where the sheet states them.
"""
import math
from sheet import WHITE, ARC
from century.editorial import tx, header, curve

AX, AW, AH = 26, 380, 92   # chart inset, width and height inside the 440 column


def _frame(s, title, scope, foot, body):
    from triptych import diagram_y, register_section
    x, w = s.W - 650, 440
    y = diagram_y(s, 'right', 187)
    header(s, dict(title=title, scope=scope), x, y, w)
    body(s, x, y + 39)
    tx(s, foot, x, y + 184, 7, .67)
    register_section(s, 'right', y - 16, y + 187)
    s.diagram_slots = getattr(s, 'diagram_slots', set()) | {'right'}


def _xaxis(s, x, y, xlabel, ticks):
    ax = x + AX
    for t, label in ticks:
        s.ln(ax + AW * t, y + AH, ax + AW * t, y + AH + 4, .45, .5)
        tx(s, label, ax + AW * t, y + AH + 13 + s.type_growth(6.6), 6.6, .65, align='c')
    tx(s, xlabel, ax + AW, y + AH + 27, 7, .55, align='r')


def _chart(s, x, y, fn, xlabel, ticks, unit='', n=150):
    ax = x + AX
    for t in (0, .25, .5, .75, 1):
        s.ln(ax, y + AH * t, ax + AW, y + AH * t, .13, .4)
    s.poly([(ax, y), (ax, y + AH), (ax + AW, y + AH)], .48, .55, close=False)
    if unit:
        tx(s, unit, ax - 9, y - 8, 6.2, .55)
    curve(s, [(ax + AW * i / n, y + AH * (1 - fn(i / n))) for i in range(n + 1)], ARC)
    _xaxis(s, x, y, xlabel, ticks)
    return ax


def quantum_simulator(s):
    def body(s, x, y):
        _chart(s, x, y, lambda t: .03 + .93 * math.exp(-4.2 * t), 'CODE DISTANCE / d',
               [(0, '3'), (12 / 22, '15'), (1, '25')])
    _frame(s, 'LOGICAL ERROR RATE', 'IDEAL SURFACE CODE / BELOW THRESHOLD',
           'Below threshold, each step in code distance cuts errors by the same factor.', body)


def sky_racer(s):
    def body(s, x, y):
        _chart(s, x, y, lambda t: .55 + .22 * math.sin(t * 17) * math.cos(t * 5) + .15 * math.sin(t * 7 + 1),
               'GATE', [(0, '1'), (.5, '5'), (1, '9')], 'km/h')
    _frame(s, 'SPEED OVER ONE LAP', 'ONE LAP / NINE GATES',
           'The racer slows for the tight gates and speeds up between them.', body)


def fusion_transport(s):
    def speed(t):
        up = 1 / (1 + math.exp(-(t - .16) * 30))
        down = 1 / (1 + math.exp((t - .84) * 30))
        return .08 + .84 * up * down

    def body(s, x, y):
        _chart(s, x, y, speed, 'DAY', [(0, '0'), (1 / 3, '25'), (2 / 3, '50'), (1, '75')], 'km/s')
    _frame(s, 'SPEED RELATIVE TO THE SUN', 'EARTH TO MARS / THRUST, COAST, BRAKE',
           'About two weeks of thrust, a long coast, then two weeks of braking.', body)


def cortical_mesh(s):
    def body(s, x, y):
        ax = x + AX; pitch = AH / 14
        # The legacy random stream is consumed in its original order and count.
        for row in range(14):
            yy = y + row * pitch + 1
            col = ARC if row == 5 else WHITE
            rate = s.rng.uniform(6, 30)
            t = 0.0
            while True:
                t += s.rng.expovariate(1 / rate)
                if t > 260:
                    break
                xx = ax + AW * t / 260
                s.ln(xx, yy, xx, yy + pitch - 2.2, .8, .6, color=col)
        s.ln(ax, y + AH, ax + AW, y + AH, .48, .55)
        _xaxis(s, x, y, 'TIME / ms', [(0, '0'), (.5, '250'), (1, '500')])
    _frame(s, 'UNIT ACTIVITY', '14 CHANNELS / SPIKE RASTER',
           'Each tick is one spike; each row is one channel.', body)


def bounder(s):
    def force(t):
        u = (t * 2.5) % 1.0
        return .04 + (.9 * math.sin(math.pi * u / .34) if u < .34 else 0.0)

    def body(s, x, y):
        _chart(s, x, y, force, 'STRIDES', [(0, '0'), (.4, '1'), (.8, '2')], 'kN', n=300)
    _frame(s, 'FORCE ON THE GROUND', 'ONE LEG / SPRINTING',
           'Ground contact takes about a third of each stride; the rest is flight.', body)


def air_refinery(s):
    def body(s, x, y):
        _chart(s, x, y, lambda t: .05 + .88 * math.exp(-(((t - .52) / .2) ** 2)), 'HOUR',
               [(0, '0'), (.25, '6'), (.5, '12'), (.75, '18'), (1, '24')], 't/h')
    _frame(s, 'FUEL OUTPUT OVER ONE DAY', 'ONE CLEAR DAY / HOURLY OUTPUT',
           'Output follows the sun on the mirror field and peaks just after midday.', body)


def aroma_organ(s):
    def body(s, x, y):
        ax = x + 44; aw = AX + AW - 44
        starts = (.10, .20, .05, .42, .32, .63); durations = (.32, .42, .18, .31, .52, .19)
        for i, (a, d) in enumerate(zip(starts, durations)):
            yy = y + 4 + i * 17.6
            tx(s, 'V' + str(i + 1).zfill(2), x, yy + 2.5, 7, .7)
            s.ln(ax, yy, ax + aw, yy, .13, .45)
            s.ln(ax + aw * a, yy, ax + aw * (a + d), yy, .82, 2, color=ARC)
        tx(s, 'TIME', x + AX + AW, y + AH + 27, 7, .55, align='r')
    _frame(s, 'VALVE PROGRAM', 'SIX VALVES / ONE CUE',
           'A recipe sets when each valve opens and for how long.', body)


def organ_foundry(s):
    def body(s, x, y):
        _chart(s, x, y, lambda t: .05 + .9 / (1 + math.exp(-(t - .55) * 11)), 'DAY',
               [(0, '0'), (1 / 3, '7'), (2 / 3, '14'), (1, '21')], 'ml/min')
    _frame(s, 'FILTRATION RATE', 'MATURING KIDNEY / ON THE PUMP',
           'Filtration rises as the printed vessels open, then levels off.', body)


def volumetric_stage(s):
    def body(s, x, y):
        _chart(s, x, y, lambda t: .04 + .92 * math.exp(-(((t - .5) / .045) ** 2)),
               'DISTANCE FROM THE CROSSING / mm', [(0, '−5'), (.5, '0'), (1, '5')], n=300)
    _frame(s, 'LIGHT FROM ONE PARTICLE', 'ACROSS THE BEAM CROSSING',
           'The glowing spot is under a millimetre wide.', body)


def proxy(s):
    def body(s, x, y):
        ax = _chart(s, x, y, lambda t: .30 + .62 * (1 - math.exp(-3.2 * t)), 'MONTHS WITH PX-1',
                    [(0, '0'), (.5, '6'), (1, '12')])
        s.poly([(ax + AW * i / 60, y + AH * (1 - (.30 - .22 * (i / 60) ** .8))) for i in range(61)],
               .8, .9, close=False, dash=[4, 3])
        # Each line named beside itself, inside a clear grid band: the rising
        # line above its early climb, the dashed one above its late tail.
        tx(s, 'RUNS WHEN THEY CHOOSE', ax + 8, y + 14, 6.6, .9, color=ARC)
        tx(s, 'RUNS CANCELLED, NO GUIDE', ax + AW - 4, y + 64, 6.6, .7, align='r')
    _frame(s, 'RUNS PER WEEK', "ONE RUNNER'S YEAR",
           'Most of the gain comes in the first six months.', body)


def presence_rig(s):
    def body(s, x, y):
        _chart(s, x, y, lambda t: .06 + .8 / (1 + math.exp(-(t - .3) * 24)) - .35 / (1 + math.exp(-(t - .75) * 30)),
               'TIME / s', [(0, '0'), (.5, '1'), (1, '2')], 'N·m')
    _frame(s, 'ARM RESISTANCE, PUSHING A DOOR', 'ELBOW TORQUE / ONE PUSH',
           'Resistance builds against the closed door and eases once it starts to swing.', body)


CHARTS = {
    'quantum-simulator': quantum_simulator,
    'sky-racer': sky_racer,
    'fusion-transport': fusion_transport,
    'cortical-mesh': cortical_mesh,
    'bounder': bounder,
    'air-refinery': air_refinery,
    'aroma-organ': aroma_organ,
    'organ-foundry': organ_foundry,
    'volumetric-stage': volumetric_stage,
    'proxy': proxy,
    'presence-rig': presence_rig,
}


def draw(s):
    CHARTS[s.subject](s)
