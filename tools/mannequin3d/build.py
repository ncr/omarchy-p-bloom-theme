"""Blender-only, authored articulated crash dummy -> occlusion-tested vector paths.
Run: blender -b --factory-startup -t 4 --python tools/mannequin3d/build.py
World: X lateral, -Y anterior, Z superior. Units are blueprint design units.
No generated raster is traced. Both sides instantiate identical shell meshes.
"""
import bpy, math, json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'tools/assets/mannequin3d';OUT.mkdir(parents=True,exist_ok=True)
STUDY=ROOT/'concepts/mannequin3d';STUDY.mkdir(parents=True,exist_ok=True)
TAU=math.tau
# Profiles: axial position, lateral half-width, anterior/posterior half-depth,
# anterior offset. Subdivision creates a continuous molded surface.
PROFILES={
 'upper_arm':[(0,10,10,0),(8,17,18,-1),(22,22,21,-2),(48,21,20,-2),(76,17,16,0),(102,13,13,0),(116,10,10,0)],
 'forearm':[(0,10,10,0),(10,14,14,0),(28,16,15,-1),(51,14,12,-1),(76,10,9,0),(88,8,8,0)],
 'thigh':[(0,13,14,0),(14,21,22,-1),(33,23,24,-2),(63,21,22,-2),(102,17,18,-1),(133,13,14,0),(146,11,12,0)],
 'calf':[(0,11,12,0),(15,15,16,1),(43,14,18,2),(70,12,16,2),(104,9,12,1),(126,7,9,0),(140,6,7,0)],
 'torso':[(125,38,25,-3),(132,44,30,-4),(158,46,31,-4),(185,49,34,-5),(208,61,35,-4),(237,63,31,-1),(241,59,29,-1)],
 'pelvis':[(23,12,14,0),(29,44,18,0),(44,46,19,0),(51,30,17,0),(57,12,12,0)],
 'head':[(274,12,14,0),(280,19,20,0),(290,23,23,0),(325,24,23,0),(341,20,19,1),(349,10,12,1),(351,2,3,1)],
 'hand':[(0,7,5,0),(5,7,5,0),(10,11,6,-1),(13,12,6,-1),(33,12,6,-1),(38,10,5,-1),(40,10,5,-1)],
 'foot':[(0,17,30,-13),(2,18,31,-13),(6,18,31,-13),(10,17,30,-13),(16,14,24,-8),(25,8,10,0),(30,8,9,0)]}
objects=[];detail=[];joints={}

def loft(name,profile):
 n=40;vs=[];fs=[]
 for z,rx,ry,cy in profile:
  for k in range(n):
   a=TAU*k/n
   # Rounded rectangular sections, with planar palms, toes and soles.
   exponent=.45 if name in ('hand','foot','thumb') else 1
   cs=math.cos(a);sn=math.sin(a)
   vs.append((rx*math.copysign(abs(cs)**exponent,cs),cy+ry*math.copysign(abs(sn)**exponent,sn),z))
 for j in range(len(profile)-1):
  for k in range(n):fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 fs += [tuple(reversed(range(n))),tuple((len(profile)-1)*n+k for k in range(n))]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vs,[],fs);mesh.update()
 # Preserve planar end rims: subdividing large cap ngons otherwise creates
 # scalloped grazing contours at shell junctions and shoe soles.
 crease=mesh.attributes.new('crease_edge','FLOAT','EDGE')
 last=(len(profile)-1)*n
 for edge in mesh.edges:
  a,b=edge.vertices
  if (a<n and b<n) or (a>=last and b>=last):crease.data[edge.index].value=1.0
 return mesh
TEMPLATES={name:loft(name,p) for name,p in PROFILES.items()}
# One continuous wraparound sensor visor, inset within the smooth skull.
visor_vertices=[];visor_faces=[]
for z,rx,ry in [(281,15,22),(289,21,25),(313,23,26),(335,20,23),(342,13,19)]:
 for k in range(25):
  a=math.pi+.12+(math.pi-.24)*k/24
  visor_vertices.append((rx*math.cos(a),ry*math.sin(a)-2,z))
for j in range(4):
 for k in range(24):visor_faces.append((j*25+k,j*25+k+1,(j+1)*25+k+1,(j+1)*25+k))
visor_mesh=bpy.data.meshes.new('Visor');visor_mesh.from_pydata(visor_vertices,[],visor_faces);visor_mesh.update()

def obj(name,mesh,matrix):
 o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.matrix_world=matrix
 sub=o.modifiers.new('Molded surface','SUBSURF');sub.levels=2;sub.render_levels=2
 for f in mesh.polygons:f.use_smooth=True
 objects.append(o);return o

def frame(a,b,across=Vector((1,0,0))):
 z=(Vector(b)-Vector(a)).normalized();x=Vector(across);x=(x-z*x.dot(z)).normalized();y=z.cross(x)
 m=Matrix((x,y,z)).transposed().to_4x4();m.translation=Vector(a);return m

def curve(name,pts,weight=.45,kind='seam'):
 detail.append((name,[Vector(p) for p in pts],weight,kind))

def ring(name,center,axis,radius,kind='seam'):
 n=Vector(axis).normalized();u=n.cross(Vector((0,0,1)))
 if u.length<.01:u=n.cross(Vector((0,1,0)))
 u.normalize();v=n.cross(u);c=Vector(center)
 curve(name,[c+radius*(u*math.cos(TAU*i/96)+v*math.sin(TAU*i/96)) for i in range(97)],.5,kind)
 if kind=='target':
  curve(name+'.cross-a',[c-u*radius,c+u*radius],.45,kind)
  curve(name+'.cross-b',[c-v*radius,c+v*radius],.45,kind)

def sphere(name,p,r):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=r,location=p)
 o=bpy.context.object;o.name=name;objects.append(o)
 for f in o.data.polygons:f.use_smooth=True
 return o

def segment(name,kind,a,b,across):
 a,b=Vector(a),Vector(b);m=frame(a,b,across);obj(name,TEMPLATES[kind],m)
 # Actual parting and access seams on the SAME 3-D molded shell.
 pr=PROFILES[kind]
 for index in (1,len(pr)-2):
  z,rx,ry,cy=pr[index];curve(name+'.socket', [m@Vector((rx*1.005*math.cos(TAU*k/96),cy+ry*1.005*math.sin(TAU*k/96),z)) for k in range(97)])
 for angle in (-math.pi/2,math.pi/2,0):
  pts=[m@Vector((rx*math.cos(angle),cy+ry*math.sin(angle),z)) for z,rx,ry,cy in pr[1:-1]]
  curve(name+'.mold-seam',pts,.32)
 joints[name]={'a':list(a),'b':list(b),'length':(a-b).length,'component':kind}
 return m

def joint(name,p,r,axis):
 sphere(name,p,r)
 n=Vector(axis).normalized();c=Vector(p)+n*(r*.94)
 ring(name+'.cap',c,n,r*.68);ring(name+'.target',Vector(p)+n*(r+.03),n,r*.48,'target')

def hand(name,wrist,elbow,across,side,thumb_out=False):
 wrist=Vector(wrist);direction=(wrist-Vector(elbow)).normalized();m=frame(wrist,wrist+direction,across)
 obj(name,TEMPLATES['hand'],m)
 # Compact thumb wedge: same palm frame, mirrored only across the hand.
 obj(name+'.thumb',loft('thumb',[(8,4,4,0),(10,5,4,0),(20,5,4,-1),(25,3,3,-1)]),m@Matrix.Translation(((side if thumb_out else -side)*11,0,0)))
 curve(name+'.cuff',[m@Vector((8*math.cos(TAU*k/64),7*math.sin(TAU*k/64),6)) for k in range(65)])

def body(pose):
 global objects,detail,joints
 objects=[];detail=[];joints={}
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 sideview=pose in ('proxy','seated','bounder');across=Vector((1,0,0))
 if pose=='bounder':
  from bounder_runner import pose_layout
  torso,poses=pose_layout()
 elif pose=='proxy':
  from proxy_pose import layout
  proxy=layout()
  def cv(point,lateral):return Vector((lateral,-point[0],-point[1]))
  poses=[]
  for side,key in ((-1,'far'),(1,'near')):
   p=proxy[key]
   poses.append((side,cv(proxy['shoulder'],side*82),cv(p['elbow'],side*82),cv(p['wrist'],side*82),cv(proxy['hip'],side*36),cv(p['knee'],side*36),cv(p['ankle'],side*36)))
  torso=Matrix.Rotation(math.radians(11.4),4,'X');torso.translation=Vector((0,6,-20))-torso@Vector((0,0,30))
 elif pose in ('seated','diner'):
  torso=Matrix.Identity(4);poses=[]
  for side in (-1,1):
   sh=Vector((side*82,0,236));el=sh+Vector((0,-math.sqrt(116**2-86**2),-86));wr=el+Vector((0,-88,0))
   hip=Vector((side*36,0,30));kn=hip+Vector((0,-146,0));an=kn+Vector((0,0,-140))
   poses.append((side,sh,el,wr,hip,kn,an))
 else:
  torso=Matrix.Identity(4);poses=[]
  for side in (-1,1):
   sh=Vector((side*82,0,236));el=sh+Vector((side*32,0,-math.sqrt(116**2-32**2)));wr=el+Vector((side*18,0,-math.sqrt(88**2-18**2)))
   hip=Vector((side*36,0,30));kn=hip+Vector((side*14,0,-math.sqrt(146**2-14**2)));an=kn+Vector((side*2,0,-math.sqrt(140**2-2**2)))
   poses.append((side,sh,el,wr,hip,kn,an))
 for part in ('torso','pelvis'):
  obj(part,TEMPLATES[part],torso)
 # Short chest shell over a black rib housing, narrow spine, exposed hip drives.
 obj('DARK abdomen',loft('Abdominal drive',[(84,22,19,0),(91,36,26,-1),(112,42,29,-2),(133,40,26,-3)]),torso)
 obj('DARK collar',loft('Shoulder yoke',[(237,66,27,0),(241,74,26,0),(248,69,24,0),(254,34,19,0),(256,25,17,0)]),torso)
 obj('neck coupling',loft('Neck coupling',[(252,13,12,0),(255,14,12,0),(271,12,11,0),(278,12,11,0)]),torso)
 obj('DARK spine',loft('Spine actuator',[(51,9,10,0),(60,12,11,0),(76,10,10,0),(89,12,12,0)]),torso)
 for sign in (-1,1):
  obj('DARK hip drive',loft('Hip drive',[(5,10,15,0),(13,17,22,0),(40,17,22,0),(55,10,16,0)]),torso@Matrix.Translation((sign*38,0,0)))
 for z in (63,72,81):ring('spine coupling',torso@Vector((0,0,z)),(0,0,1),12)

 if pose!='proxy':
  obj('head',TEMPLATES['head'],torso)
  obj('VISOR',visor_mesh,torso)
 # Torso parting lines, clavicles, sternum and pelvic service cover.
 for part,index in [('torso',1),('torso',-2),('pelvis',2)]:
  z,rx,ry,cy=PROFILES[part][index]
  curve(part+'.seam',[torso@Vector((rx*math.cos(TAU*k/120),cy+ry*math.sin(TAU*k/120),z)) for k in range(121)],.5)
 for sign in (-1,1):
  curve('chest panel', [torso@Vector((sign*x,y,z)) for x,y,z in [(53,-26,232),(54,-33,211),(43,-34,195),(36,-31,160),(34,-29,136)]],.45)
  curve('pectoral break',[torso@Vector((sign*x,y,z)) for x,y,z in [(0,-36,205),(21,-36,205),(43,-34,199),(54,-31,193)]],.4)
 # Optical targets placed on the physical shell (front or lateral).
 if not sideview:
  ring('sternum',torso@Vector((0,-39,222)),(0,-1,0),6,'target')
 else:
  if pose!='proxy':ring('temple',torso@Vector((24.5,0,312)),(1,0,0),8,'target')
 for side,sh,el,wr,hip,kn,an in poses:
  for kind,a,b in [('upper_arm',sh,el),('forearm',el,wr),('thigh',hip,kn),('calf',kn,an)]:
   # The descending leg frame reverses local front/back. Restore the intended
   # anterior thigh / posterior calf offset in the running side elevation.
   shell_across=-across if pose=='proxy' and kind in ('thigh','calf') else across
   segment(str(side)+kind,kind,a,b,shell_across)
  axis=(side,0,0) if sideview else (0,-1,0)
  for nm,p,r in [('shoulder',sh,15),('elbow',el,11),('wrist',wr,8),('hip',hip,17),('knee',kn,14),('ankle',an,8)]:joint(str(side)+nm,p,r,axis)
  hand(str(side)+'hand',wr,el,across,side,thumb_out=pose=='presence')
  footmat=Matrix.Translation(an-Vector((0,0,30)))
  if pose=='bounder':
   from bounder_runner import foot_frame
   footmat=foot_frame(an,kn,side)@Matrix.Translation((0,0,-30))
  elif pose=='proxy':
   angle=proxy['near' if side==1 else 'far']['foot_angle']
   footmat=Matrix.Translation(an)@Matrix.Rotation(math.radians(angle),4,'X')@Matrix.Translation((0,0,-30))
  obj(str(side)+'foot',TEMPLATES['foot'],footmat)
  curve(str(side)+'sole',[footmat@Vector((18*math.copysign(abs(math.cos(TAU*k/96))**.45,math.cos(TAU*k/96)),-13+31*math.copysign(abs(math.sin(TAU*k/96))**.45,math.sin(TAU*k/96)),4)) for k in range(97)],.5)
 # A bone skeleton records the articulation for further posing in Blender.
 arm=bpy.data.armatures.new('Dummy joints');rig=bpy.data.objects.new('Pose skeleton',arm);bpy.context.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True)
 bpy.ops.object.mode_set(mode='EDIT')
 trunk=arm.edit_bones.new('trunk');trunk.head=torso@Vector((0,0,30));trunk.tail=torso@Vector((0,0,259))
 for name,j in joints.items():
  bone=arm.edit_bones.new(name);bone.head=j['a'];bone.tail=j['b'];bone.parent=trunk
 for side,sh,el,wr,hip,kn,an in poses:
  prefix=str(side)
  arm.edit_bones[prefix+'forearm'].parent=arm.edit_bones[prefix+'upper_arm']
  arm.edit_bones[prefix+'calf'].parent=arm.edit_bones[prefix+'thigh']
  for suffix,a,b,parent in [('hand',wr,wr+(wr-el).normalized()*42,'forearm'),('foot',an,an+Vector((0,-45,-20)),'calf')]:
   bone=arm.edit_bones.new(prefix+suffix);bone.head=a;bone.tail=b;bone.parent=arm.edit_bones[prefix+parent]
 bpy.ops.object.mode_set(mode='OBJECT');rig.hide_render=True
 for o in objects:
  bone_name='trunk'
  for side in ('-1','1'):
   if o.name.startswith(side):
    stem=o.name[len(side):].split('.')[0]
    part={'shoulder':'upper_arm','elbow':'upper_arm','wrist':'forearm','hip':'thigh','knee':'thigh','ankle':'calf'}.get(stem,stem)
    if side+part in arm.bones:bone_name=side+part
  group=o.vertex_groups.new(name=bone_name);group.add(list(range(len(o.data.vertices))),1,'REPLACE')
  modifier=o.modifiers.new('Rigid casting articulation','ARMATURE');modifier.object=rig
 return sideview


def project(pose):
 sideview=body(pose)
 if pose=='bounder':
  from bounder_runner import equip
  equip(sys.modules[__name__])
 bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
 verts=[];faces=[];meshes=[];face_owners=[]
 for o in objects:
  eo=o.evaluated_get(deps);mesh=eo.to_mesh();v=[o.matrix_world@p.co for p in mesh.vertices];f=[tuple(p.vertices) for p in mesh.polygons]
  face_owners.extend([o.name]*len(f))
  offset=len(verts);verts.extend(v);faces.extend([tuple(offset+i for i in p) for p in f]);meshes.append((o.name,v,f));eo.to_mesh_clear()
 bvh=BVHTree.FromPolygons(verts,faces,all_triangles=False)
 toward=Vector((1,0,0)) if sideview else Vector((0,-1,0))
 if pose=='bounder':toward=Vector((1,-.22,0)).normalized()
 runner_right=toward.cross(Vector((0,0,1)))
 # Fit the fixed front view to the existing roller-floor contact, preserving scale.
 if pose=='presence':scale=.96;dy=246+min(v.z for v in verts)*scale
 elif pose in ('seated','diner'):scale=346/(304-min(v.z for v in verts));dy=304*scale
 else:scale=1;dy=0
 def xy(p):return [round((p.dot(runner_right) if pose=='bounder' else (-p.y if sideview else p.x))*scale,3),round(-p.z*scale+dy,3)]
 def visible(p,owner=None,tolerance=.8):
  hit=bvh.ray_cast(p+toward*2000,-toward,2001)
  if hit[0] is None:return True
  # A faceted silhouette must not clip against its own subdivided shell.
  if owner is not None and face_owners[hit[2]]==owner:return True
  return (hit[0]-p).length<tolerance
 paths=[];fills=[];panels=[];dark_faces=[]
 def store(name,points,width,kind):
  def seen(p):return visible(p,name if kind=='outline' else None,3.5 if kind=='target' else .8)
  def boundary(a,b,state):
   # Locate the actual visibility boundary instead of stopping one sample short.
   for _ in range(12):
    mid=(a+b)*.5
    if seen(mid)==state:a=mid
    else:b=mid
   return (a+b)*.5
  chains=[];chain=[];previous=None;previous_state=False
  for p in points:
   state=seen(p)
   if previous is not None and state!=previous_state:
    q=xy(boundary(previous,p,previous_state))
    if previous_state:
     chain.append(q)
     if len(chain)>1:chains.append(chain)
     chain=[]
    else:chain=[q]
   if state:chain.append(xy(p))
   previous=p;previous_state=state
  if len(chain)>1:chains.append(chain)
  # A closed source contour can straddle the traversal start; join that seam.
  if len(chains)>1 and (points[0]-points[-1]).length<1e-4 and seen(points[0]):
   chains=[chains[-1]+chains[0][1:]]+chains[1:-1]
  for chain in chains:paths.append({'name':name,'points':chain,'width':width,'kind':kind})
 for name,v,f in meshes:
  if name.startswith('DARK') or name=='pelvis':
   for poly in f:
    center=sum((v[i] for i in poly),Vector())/len(poly)
    normal=(v[poly[1]]-v[poly[0]]).cross(v[poly[2]]-v[poly[0]])
    if normal.dot(toward)>0 and visible(center):dark_faces.append([xy(v[i]) for i in poly])
  edges={}
  for poly in f:
   a,b,c=(v[i] for i in poly[:3]);normal=(b-a).cross(c-a);front=normal.dot(toward)>normal.length*1e-5
   for i,j in zip(poly,poly[1:]+poly[:1]):edges.setdefault(tuple(sorted((i,j))),[]).append(front)
  silhouette=[e for e,sides in edges.items() if len(sides)==1 or any(sides)!=all(sides)]
  adjacent={}
  for a,b in silhouette:adjacent.setdefault(a,[]).append(b);adjacent.setdefault(b,[]).append(a)
  unused=set(silhouette)
  while unused:
   a,b=unused.pop();ids=[a,b]
   while True:
    nexts=[j for j in adjacent[ids[-1]] if tuple(sorted((ids[-1],j))) in unused]
    if not nexts:break
    j=nexts[0];unused.remove(tuple(sorted((ids[-1],j))));ids.append(j)
   points=[]
   for a,b in zip(ids,ids[1:]):
    length=(v[a]-v[b]).length;n=max(1,math.ceil(length/1.5));points.extend(v[a].lerp(v[b],k/n) for k in range(n))
   points.append(v[ids[-1]])
   if ids[0]==ids[-1]:
    fills.append([xy(p) for p in points])
    if name=='VISOR':panels.append([xy(p) for p in points])
   store(name,points,.8,'outline')
 for name,pts,w,kind in detail:
  smooth=[]
  for a,b in zip(pts,pts[1:]):smooth.extend(a.lerp(b,k/max(1,math.ceil((a-b).length))) for k in range(max(1,math.ceil((a-b).length))))
  smooth.append(pts[-1]);store(name,smooth,w,kind)
 # Bound contour simplification in projection units, never smoothing targets.
 def simplify(points,epsilon):
  if len(points)<3:return points
  a=Vector(points[0]);b=Vector(points[-1]);delta=b-a
  distances=[]
  for p in points[1:-1]:
   q=Vector(p);t=max(0,min(1,(q-a).dot(delta)/delta.length_squared)) if delta.length_squared else 0
   distances.append((q-a-delta*t).length)
  maximum=max(distances);i=distances.index(maximum)+1
  if maximum<=epsilon:return [points[0],points[-1]]
  return simplify(points[:i+1],epsilon)[:-1]+simplify(points[i:],epsilon)
 cleaned=[]
 for path in paths:
  if path['kind']!='target':
   path['points']=simplify(path['points'],.12 if path['kind']=='outline' else .1)
   length=sum(math.dist(a,b) for a,b in zip(path['points'],path['points'][1:]))
   if length<3.5:continue
  cleaned.append(path)
 paths=cleaned
 data={'pose':pose,'source':'Authored 3D molded crash dummy, orthographic BVH hidden-line projection','scale':scale,'dy':dy,'joints':joints,'paths':paths,'fills':fills,'panels':panels,'dark_faces':dark_faces}
 (OUT/(pose+'.json')).write_text(json.dumps(data,separators=(',',':'))+'\n')
 # Scene retained for inspection in 3D, with orthographic camera matching output.
 bpy.ops.object.camera_add(location=toward*1800+Vector((0,0,30)));cam=bpy.context.object;cam.rotation_euler=(-toward).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=750;bpy.context.scene.camera=cam
 bpy.ops.wm.save_as_mainfile(filepath=str(STUDY/(pose+'.blend')))
 print(pose,'paths',len(paths),'vertices',len(verts),flush=True)
if __name__=='__main__':
 import sys,os
 poses=os.environ.get('MANNEQUIN_ONLY','presence,proxy,seated,diner').split(',')
 for pose in poses:project(pose)
 sys.stdout.flush();os._exit(0)
