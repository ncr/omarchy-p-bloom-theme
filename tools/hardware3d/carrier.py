"""Illustration-only carrier PCB, shared by KiCad and the Blender assembly."""
from pathlib import Path
import json,pcbnew as k
ROOT=Path(__file__).resolve().parents[2];out=ROOT/'tools/assets/hardware3d'
out.mkdir(parents=True,exist_ok=True)
board=k.BOARD();board.SetCopperLayerCount(2)
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
for a,b in [((-48,-34),(48,-34)),((48,-34),(48,34)),((48,34),(-48,34)),((-48,34),(-48,-34))]:
 e=k.PCB_SHAPE();e.SetShape(k.SHAPE_T_SEGMENT);e.SetStart(v(*a));e.SetEnd(v(*b));e.SetLayer(k.Edge_Cuts);e.SetWidth(k.FromMM(.15));board.Add(e)
parts=[];pads=[];tracks=[]
for i,(x,y) in enumerate([(-24,-12),(0,-12),(24,-12),(-24,12),(0,12),(24,12)]):
 parts.append(dict(x=x,y=y,w=12,h=12,height=3,kind='package'))
 fp=k.FOOTPRINT(board);fp.SetReference('U'+str(i+1));fp.SetValue('ILLUSTRATIVE_TILE');fp.SetPosition(v(x,y));board.Add(fp)
 for side in (-1,1):
  for n in range(8):
   px=x-4.9+n*1.4;py=y+side*7
   pad=k.PAD(fp);pad.SetNumber(str(len(pads)+1));pad.SetAttribute(k.PAD_ATTRIB_SMD);pad.SetShape(k.PAD_SHAPE_RECT);pad.SetSize(v(.8,2));pad.SetPosition(v(px,py));layers=k.LSET();layers.AddLayer(k.F_Cu);pad.SetLayerSet(layers);fp.Add(pad);pads.append([px,py,.8,2])
 for side in (-1,1):
  for n in range(3):parts.append(dict(x=x+side*9,y=y-3+n*3,w=2,h=1,height=1,kind='passive'))
for side in (-1,1):
 parts.append(dict(x=side*42,y=0,w=6,h=48,height=5,kind='connector'))
 for n in range(20):
  y=-23+n*2.4;tracks.append([[side*39,y],[side*34,y],[side*30,y*.55]])
for line in tracks:
 for a,b in zip(line,line[1:]):
  tr=k.PCB_TRACK(board);tr.SetStart(v(*a));tr.SetEnd(v(*b));tr.SetWidth(k.FromMM(.22));tr.SetLayer(k.F_Cu);board.Add(tr)
# Fabrication-layer component envelopes share dimensions with the 3-D blocks.
for p in parts:
 x,y,w,h=p['x'],p['y'],p['w'],p['h']
 for a,b in [((x-w/2,y-h/2),(x+w/2,y-h/2)),((x+w/2,y-h/2),(x+w/2,y+h/2)),((x+w/2,y+h/2),(x-w/2,y+h/2)),((x-w/2,y+h/2),(x-w/2,y-h/2))]:
  e=k.PCB_SHAPE();e.SetShape(k.SHAPE_T_SEGMENT);e.SetStart(v(*a));e.SetEnd(v(*b));e.SetLayer(k.F_Fab);e.SetWidth(k.FromMM(.12));board.Add(e)
k.SaveBoard(str(out/'carrier.kicad_pcb'),board)
(out/'carrier.json').write_text(json.dumps(dict(size=[96,68],parts=parts,pads=pads,tracks=tracks),indent=2)+'\n')
print('KiCad illustration carrier and shared geometry written.')
