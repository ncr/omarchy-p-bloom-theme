"""Common editorial grid for the 34 retained technical plates.

Design units are independent of native resolution. The notes and signature have
separate measured regions; illustration callouts must not enter the footer.
"""
from sheet import ARC, GOLD

# Explanatory metadata belongs to the dossier, not a second centre footer.
MAIN_CONTEXT = {
 'truth-lamp': ('HUMAN FAMILY / SCHEMATIC STAND-INS',
                'NO ROBOTS. JUST AWKWARD SILENCES.'),
}

# Punchline arithmetic: 900 N of thrust = the weight of 92 kg on Earth (o03);
# a ~5 kg head at 6 g weighs about 30 kg (o02).
ORIGINAL = {
 'quantum-simulator': ('ERRORS ALSO NEED MANAGEMENT', 'The wall draws six thousand watts for every microwatt the base stage removes.', ('ENCODE', 'CHECK', 'CORRECT'), 'THE ERROR BUDGET HAS REQUESTED A LARGER BUDGET.'),
 'sky-racer': ('PILOT STILL REQUIRED', 'Tilted thrust provides acceleration as well as lift. The pilot remains part of the payload.', ('LIFT', 'BANK', 'RECOVER'), "IN A 6 g TURN, THE PILOT'S HEAD WEIGHS ABOUT 30 kg."),
 'fusion-transport': ('HEAT MUST LEAVE THE SHIP', 'Propulsion and waste heat share a reactor: the exhaust carries 45 MW, the radiators most of the rest.', ('BURN', 'COAST', 'BRAKE'), 'ON EARTH, ITS FULL THRUST WOULD JUST LIFT ONE OF THE CREW.'),
 'greener': ('RELATIVE SUCCESS', 'The target follows the neighbour. A better lawn can therefore make this lawn temporarily worse.', ('SCAN', 'COMPARE', 'OUTGROW'), 'PEACE TREATY SOLD SEPARATELY.'),
 'cortical-mesh': ('CHANNELS ARE NOT THOUGHTS', 'Together the sites take 21 billion samples a second; the chip decodes them before anything leaves the skull.', ('SENSE', 'ENCODE', 'DECODE'), 'FIRST WORD BACK AFTER THE STROKE: “COFFEE.”'),
 'bounder': ('THE HUMAN IS THE PAYLOAD', 'At top speed the athlete covers 100 m in under six seconds.', ('LOAD', 'RELEASE', 'RECOVER'), 'GRAVITY HAS NOT SIGNED THE WAIVER.'),
 'air-refinery': ('CARBON IS NOT THE ENERGY SUPPLY', 'Nearly every carbon atom taken from the air leaves the tower in the fuel.', ('CAPTURE', 'CONVERT', 'REFINE'), 'FLIGHT 212 TO REYKJAVÍK RAN ON LAST TUESDAY’S AIR.'),
 'aroma-organ': ('A RECIPE IS NOT A RECEPTOR MAP', 'Smells are scored like music: each cue is a chord of base odorants, played on the valves.', ('METER', 'MIX', 'CLEAR'), 'CUE 12, GRANDMA’S KITCHEN: CINNAMON, THEN ONIONS.'),
 'tether-climber': ('THE BEAM PAYS FOR THE CLIMB', 'Two hours after leaving the sea, the climber passes the height of the space station.', ('ACQUIRE', 'GRIP', 'CLIMB'), 'PLEASE KEEP ALL PLANETS INSIDE THE VEHICLE.'),
 'truth-lamp': ('ACCURACY IS NOT DIPLOMACY', 'The lamp claims to detect disbelief, not objective truth. The dinner still requires an off switch.', ('LISTEN', 'INFER', 'REGRET'), 'DESSERT IS AN UNSUPERVISED LEARNING EVENT.'),
 'organ-foundry': ('PRINTED IS NOT READY', 'The printer places about 800 000 cells a second, then the kidney matures on the pump.', ('PRINT', 'PERFUSE', 'MATURE'), 'PLEASE DO NOT SELECT DRAFT QUALITY.'),
 'volumetric-stage': ('A VOLUME NEEDS A MEDIUM', 'The points of the image sit about 2 cm apart.', ('ADDRESS', 'EXCITE', 'REFRESH'), 'APPLAUSE IS NOT AN OPTICAL FEEDBACK LOOP.'),
 'proxy': ('THE RUNNER LEADS', 'Volunteer guides have diaries of their own. PX-1 is ready every morning, and the volunteers still come, now for the company.', ('WAKE', 'RUN', 'RETURN'), 'IN DECEMBER THE RUN STARTS IN THE DARK. THE LIDAR DOES NOT MIND.'),
 'presence-rig': ('THE FLOOR IS PART OF THE GAME', 'The player can cross a whole game world and never reach the edge of the floor.', ('TRACK', 'RESIST', 'RELEASE'), 'REALITY WILL RESUME AFTER THE NEXT CHECKPOINT.'),
}


def note_box(s):
    # Both triptych formats: notes under C, dedicated signature bay to the right.
    # The legacy non-triptych layout retains its compact fallback.
    return (s.W-670, s.H-264, 430) if s.wide else (242, 422, 425)


def signature_box(s):
    return (s.W-133, s.H-158, 78) if s.wide else (s.W-242, 910, 92)


def field_notes(s, d):
    x,y,w=note_box(s)
    def tx(t,xx,yy,size=7,a=.76,**kw):
        return s.text(t,xx,yy,size,track=.08,a=a,**kw)
    s.ln(x,y-12,x+w,y-12,.23,.5)
    tx('FIELD NOTES / '+d['kind'].upper(),x,y,6.5,.62)
    yy=y+21
    for line in s.wrap(d['fact'],w,8,.08):
        tx(line,x,yy,8,.85);yy+=12
    yy+=11
    for label,value in d['rows']:
        # Never shrink or truncate narrative facts to force them into the grid.
        assert s.measure(label,5.8,.08)+s.measure(value,5.8,.08)+18<w, (label,value)
        tx(label,x,yy,5.8,.53);tx(value,x+w,yy,5.8,.81,align='r');yy+=15
    context=MAIN_CONTEXT.get(s.subject,())
    if hasattr(s,'entry'):
        context=(s.entry['model']+' / '+s.entry['domain'].upper(),)
    s.main_context_notes=context
    if context:
        s.ln(x,yy-3,x+w,yy-3,.18,.45)
        yy+=12
        for note in context:
            for line in s.wrap(note,w,7,.08):
                tx(line,x,yy,7,.65);yy+=12
    bottom=yy
    assert bottom < s.H-72, (s.subject,bottom)
    s.field_notes_bounds=(x,y-12,x+w,bottom)


def original_notes(s):
    subject=getattr(s,'subject',None)
    if subject not in ORIGINAL:return
    import json
    from pathlib import Path
    title,fact,process,note=ORIGINAL[subject]
    rows=json.loads(Path(__file__).with_name('original_field_notes.json').read_text())[subject]
    field_notes(s,dict(kind='design targets',fact=fact,rows=rows,process=process))
    # A short editorial heading fills the compact column previously left blank.
    if not s.wide:
        s.text(title,242,362,9,track=.12,a=.83)
        s.text('DESIGN DOSSIER / PERFORMANCE TARGETS',242,385,5.8,track=.1,a=.48)
    from triptych import punchline
    punchline(s,note)
