"""Validate physical shared parts across poses, independent of raster output."""
import json,math
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'assets/mannequin3d'
expected={'upper_arm':116,'forearm':88,'thigh':146,'calf':140}
for pose in ('presence','proxy','seated','diner','bounder'):
 d=json.loads((root/(pose+'.json')).read_text())
 for name,j in d['joints'].items():
  actual=math.dist(j['a'],j['b']);assert abs(actual-expected[j['component']])<.0001,(pose,name,actual)
 for path in d['paths']:
  assert len(path['points'])>=2
  assert all(math.isfinite(v) for p in path['points'] for v in p)
 assert d['fills'],pose
 print(pose,': matched left/right rigid component lengths, finite visible paths')
