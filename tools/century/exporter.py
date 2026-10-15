"""Century hidden-line export: visible creases, boundaries, smooth contours and wires.

The line extraction is shared with the hardware family (tools/hardware3d/hidden_line.py).
"""
import bpy,math,json
from mathutils import Vector
import family_core as g
import hidden_line

def export(name,az=27,el=20):
 parts,wires,anchors,OUT,STUDY=g.parts,g.wires,g.anchors,g.OUT,g.STUDY
 a,e=math.radians(az),math.radians(el);right=Vector((math.cos(a),math.sin(a),0));toward=Vector((math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)));up=toward.cross(right)
 def xy(p):return [round(p.dot(right),4),round(-p.dot(up),4)]
 # Exact visibility and continuous smooth contours: tools/hardware3d/hidden_line.py.
 paths=hidden_line.extract(hidden_line.collect(parts),wires,right,up,toward)
 data=dict(paths=paths,anchors={label:xy(Vector(p)) for label,p in anchors.items()})
 (OUT/(name+'.json')).write_text(json.dumps(data,separators=(',',':'))+'\n')
 bpy.ops.object.camera_add(location=toward*1600+Vector((0,0,250)));cam=bpy.context.object;cam.rotation_euler=(-toward).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=900;bpy.context.scene.camera=cam
 bpy.ops.wm.save_as_mainfile(filepath=str(STUDY/(name+'.blend')))
 print(name,len(parts),'parts',len(paths),'paths',flush=True)
