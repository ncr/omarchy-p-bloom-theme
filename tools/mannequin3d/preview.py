import cairo,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
for pose in ('presence','proxy','seated'):
 d=json.loads((ROOT/'tools/assets/mannequin3d'/f'{pose}.json').read_text());pts=[p for path in d['paths'] for p in path['points']];x0=min(p[0] for p in pts)-20;y0=min(p[1] for p in pts)-20;w=max(p[0] for p in pts)-x0+20;h=max(p[1] for p in pts)-y0+20
 s=cairo.ImageSurface(cairo.FORMAT_RGB24,int(w*2),int(h*2));c=cairo.Context(s);c.set_source_rgb(.08,.1,.12);c.paint();c.scale(2,2);c.translate(-x0,-y0)
 for path in d['paths']:
  c.set_source_rgb(*((.9,.72,.3) if path['kind']=='target' else (.8,.85,.9)));c.set_line_width(path['width']);c.move_to(*path['points'][0]);[c.line_to(*p) for p in path['points'][1:]];c.stroke()
 s.write_to_png(str(ROOT/'concepts/mannequin3d'/f'{pose}-lines.png'))
