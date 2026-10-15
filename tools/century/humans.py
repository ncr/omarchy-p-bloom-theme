"""Shared technical mannequin geometry, measured contacts and rigid posing."""
from .kit import *
import main_scenes_build as scene
CACHE={}

def human(pose='presence',scale=.28,angle=0,p=(0,0,0),arm_angle=0,only=None):
    # Capture calls the old builder which clears the scene: recipes invoke us first.
    if pose not in CACHE:CACHE[pose]=scene.capture(pose)
    template=CACHE[pose]
    g.reset()
    parts,details,joints=template
    selected=(parts,details,joints)
    if only:
        selected=([item for item in parts if item[0].startswith(tuple(only))],[item for item in details if item[0].startswith(tuple(only))],joints)
    bottom=min(v.z for n,vs,fs in selected[0] for v in vs)
    m=Matrix.Translation(Vector(p)+Vector((0,0,-bottom*scale)))@Matrix.Rotation(math.radians(angle),4,'Z')@Matrix.Scale(scale,4)
    scene.place(selected,m,'HUMAN',arm_angle=arm_angle)
    # Make the human a quieter context layer; outer shells remain fully closed.
    for i,(obj,role) in enumerate(g.parts):
        if role=='structure':g.parts[i]=(obj,'figure')
    def point(v):return m@Vector(v)
    pts={name:{key:point(j[key]) for key in ('a','b')} for name,j in joints.items()}
    if arm_angle:
        pivot=Vector(joints['1forearm']['a']);r=Matrix.Translation(pivot)@Matrix.Rotation(math.radians(arm_angle),4,'X')@Matrix.Translation(-pivot)
        pts['1forearm']={key:point(r@Vector(joints['1forearm'][key])) for key in ('a','b')}
    report={'shared_lengths':True,'pose':pose,'scale':scale,'bottom_before':bottom,'ground_after':p[2],
            'arm_angle':arm_angle,'only':only,'joint_points':{n:{k:list(v) for k,v in q.items()} for n,q in pts.items()}}
    path=ROOT/'concepts/century/qa'/f"{CURRENT['slug'] if CURRENT else 'human'}-pose.json"
    # CURRENT imported by value from kit; use module state rather than that alias.
    from . import kit
    path=ROOT/'concepts/century/qa'/(kit.CURRENT['slug']+'-pose.json');path.write_text(json.dumps(report,indent=2)+'\n')
    return pts,point
