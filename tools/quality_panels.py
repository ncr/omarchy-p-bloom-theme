"""Reviewable quality-pass drawings; deterministic paths, type and data labels."""
import json
from century.render import draw_view,ASSETS


def main_hardware(s,slug,mx,my):
    # Century geometry, the original sheets' callouts (hardware3d.family_drawing.callouts).
    entry={'slug':slug,'number':0}
    anchors=draw_view(s,entry,'A',mx,my-20,652,675)
    notes=json.loads((ASSETS/(slug+'-meta.json')).read_text())['notes']
    from hardware3d.family_drawing import callouts
    callouts(s,{key:(x-mx,y-my) for key,(x,y) in anchors.items()},notes,mx,my)


def component(s,slug,key,cx,cy,w,h):
    return draw_view(s,{'slug':slug,'number':0},key,cx,cy,w,h)


def aroma_detail(s,rx):
    component(s,'aroma-command','A',rx,313,350,270)
    s.view_label(rx,495,'C','ODOUR COMMAND PATH','METERING HARDWARE / SIX CHANNELS SHOWN')
