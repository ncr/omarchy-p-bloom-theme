"""Hidden-line extraction shared by the Blender exporters (Blender only).

Used by century/exporter.py (Century, p(bloom), the quality scenes),
hardware3d/family_core.py (the hardware family and its studies) and
hardware3d/radial.py (quantum simulator). The drawing style is unchanged: the
same camera basis and projection, the same roles, and the same features are
lines:

* boundary edges of open surfaces;
* creases (adjacent face normals below ``CREASE_DOT``) with a front face;
* the outline of smooth surfaces: every smooth edge between a front-facing and
  a back-facing face (the exact outline of the faceted surface, so every view
  keeps its frame);
* wire centrelines.

What changed against the first exporters (in Git history):

Visibility. The old test accepted any point whose first ray hit belonged to the
same object, so every hidden edge of a concave part was drawn (the inner end
face of a split collar, the far rims inside rings and hoods), accepted hits up
to 0.35 units in front of other objects (edges just under a skin leaked), and
sampled every 1.1 units with 8 bisections, so clipped ends stopped short or
poked past. Now a point is visible when no face lies in front of it by more
than ``DEPTH_TOL``; only the faces around its own edge (sharing a vertex) and
grazing hits on its own surface within one face size are ignored. Samples are
spaced at a fixed fraction of the drawn extent (under half a pixel on the 5K
master) and every change of visibility is bisected to 1e-7 of that, so a line
ends exactly where something passes in front of it.

Topology. Vertices of one mesh are welded, so the closing seam of a lathed
ring, hood or loft is no longer a pair of boundary edges drawn across the part.
Windings are made consistent and closed parts face outward (an airfoil rib
with inward caps counted its visible side as back-facing). The rim of a flat
n-gon cap is one loop, drawn whole or not at all. Drawn edges are chained into
polylines through vertices where exactly two meet.

Added 2026-10-03 (gaps left on the hardware family's originals):

Loft rings. A crease continues along its edge loop, through vertices where
four quads meet, while the dihedral stays below ``WEAK_DOT``. A cast ring
whose angle wanders around ``CREASE_DOT`` (the widest girth of Air Refinery's
pedestal, a little flatter on its long sides) otherwise stops in the middle
of a face, as the cap rims did before the n-gon rule.

Wires on a surface. A wire is drawn as its centreline, so its tube does not
hide the lines of a part it runs along (most of its length within
``MOUNT_GAP`` of that part's skin, beyond its own radius): a seam, trim or
sill lying near an outline cut gaps into it with nothing drawn in them (the
Sky Racer's nose, the skirt bead under both pedestals). Tubes still hide
every other part, and every part still hides the wire.
"""
import math
from mathutils import Vector
from mathutils.bvhtree import BVHTree

CREASE_DOT = .75        # unchanged: dihedral cos below this is a drawn crease
WEAK_DOT = .9           # a crease continues along its edge loop while the cos stays below this
MOUNT_GAP = 2.5         # model units beyond its radius: a wire this close runs along a part
MOUNT_SHARE = .8        # ... for at least this share of its length
FRONT_EPS = 1e-6        # unchanged: facing counts as front above this
DEPTH_TOL = 0.03        # model units; coplanar contact of touching parts
GRAZE = 0.12            # |n . view| below this: a grazing hit on a curved surface
WELD = 1e-4             # model units; coincident vertices of one mesh (seams)
STEP_FRAC = 1/3200      # sample spacing as a fraction of the drawn extent
BISECT = 24
FAR = 4000.0


def collect(parts):
    """Evaluated world-space meshes of (object, role) parts: [(name, role, verts, faces)]."""
    import bpy
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    out = []
    for o, role in parts:
        eo = o.evaluated_get(deps)
        m = eo.to_mesh()
        v = [o.matrix_world @ p.co for p in m.vertices]
        f = [list(p.vertices) for p in m.polygons]
        out.append((o.name, role, v, f))
        eo.to_mesh_clear()
    return out


def _weld(verts, faces):
    index = {}
    remap = []
    vs = []
    for p in verts:
        key = (round(p.x/WELD), round(p.y/WELD), round(p.z/WELD))
        i = index.get(key)
        if i is None:
            i = index[key] = len(vs)
            vs.append(Vector(p))
        remap.append(i)
    fs = []
    for face in faces:
        f = []
        for i in face:
            j = remap[i]
            if not f or f[-1] != j:
                f.append(j)
        while len(f) > 1 and f[0] == f[-1]:
            f.pop()
        if len(set(f)) < 3:
            continue
        fs.append(f)
    return vs, fs


def _orient(vs, fs):
    """Consistent outward winding. Authored meshes sometimes mix windings (an
    extruded airfoil whose caps face inward while its sides face out); the
    old exporter hid that by never occluding an object with itself. Faces are
    made consistent across every manifold edge, then each closed component is
    turned outward by the sign of its volume. Open components keep the
    winding of their first face."""
    edge_faces = {}
    for fi, f in enumerate(fs):
        for a, b in zip(f, f[1:]+f[:1]):
            edge_faces.setdefault((a, b) if a < b else (b, a), []).append(fi)
    flip = [None]*len(fs)
    out = [list(f) for f in fs]
    for seed in range(len(fs)):
        if flip[seed] is not None:
            continue
        flip[seed] = False
        comp = [seed]
        stack = [seed]
        closed = True
        while stack:
            fi = stack.pop()
            f = out[fi]
            for a, b in zip(f, f[1:]+f[:1]):
                e = (a, b) if a < b else (b, a)
                ff = edge_faces[e]
                if len(ff) != 2:
                    closed = False
                    continue
                g = ff[0] if ff[1] == fi else ff[1]
                if g == fi or flip[g] is not None:
                    continue
                h = out[g]
                same = any(x == a and y == b for x, y in zip(h, h[1:]+h[:1]))
                flip[g] = same
                if same:
                    out[g] = h[::-1]
                comp.append(g)
                stack.append(g)
        if closed:
            vol = 0.0
            for fi in comp:
                f = out[fi]
                p0 = vs[f[0]]
                for j in range(1, len(f)-1):
                    vol += p0.dot(vs[f[j]].cross(vs[f[j+1]]))
            if vol < 0:
                for fi in comp:
                    out[fi] = out[fi][::-1]
    return out


def _newell(vs, f):
    n = Vector((0.0, 0.0, 0.0))
    for a, b in zip(f, f[1:]+f[:1]):
        p, q = vs[a], vs[b]
        n.x += (p.y-q.y)*(p.z+q.z)
        n.y += (p.z-q.z)*(p.x+q.x)
        n.z += (p.x-q.x)*(p.y+q.y)
    return n


class _Mesh:
    """One welded, consistently wound mesh with face normals and edge adjacency."""

    def __init__(self, name, role, verts, faces, toward):
        self.name, self.role = name, role
        vs, fs = _weld(verts, faces)
        fs = _orient(vs, fs)
        self.v = vs
        self.f = []
        self.n = []
        for f in fs:
            nn = _newell(vs, f)
            if nn.length < 1e-12:
                continue
            self.f.append(f)
            self.n.append(nn.normalized())
        self.edges = {}
        for fi, f in enumerate(self.f):
            for a, b in zip(f, f[1:]+f[:1]):
                self.edges.setdefault((a, b) if a < b else (b, a), []).append(fi)
        self.vfaces = [[] for _ in vs]
        for fi, f in enumerate(self.f):
            for i in f:
                self.vfaces[i].append(fi)
        self.smooth = set()
        for e, ff in self.edges.items():
            if len(ff) == 2 and self.n[ff[0]].dot(self.n[ff[1]]) >= CREASE_DOT:
                self.smooth.add(e)
        # An n-gon (more than four corners) is a flat cap: its rim is one edge
        # loop and is either drawn whole or not at all, by majority of its
        # dihedrals. Otherwise, where a loft meets the cap near CREASE_DOT, the
        # rim drops out in pieces wherever the dihedral wanders across it.
        for f in self.f:
            if len(f) <= 4:
                continue
            rim = [(a, b) if a < b else (b, a) for a, b in zip(f, f[1:]+f[:1])]
            rim = [e for e in rim if len(self.edges[e]) == 2]
            if not rim:
                continue
            if 2*sum(e not in self.smooth for e in rim) >= len(rim):
                self.smooth.difference_update(rim)
            else:
                self.smooth.update(rim)
        self._continue_creases()
        self.front = [n.dot(toward) > FRONT_EPS for n in self.n]

    def _continue_creases(self):
        """Creases continue along their edge loop (see the module notes)."""
        at = {}
        for e in self.edges:
            for i in e:
                at.setdefault(i, []).append(e)
        def regular(i):
            fs = self.vfaces[i]
            return len(at[i]) == 4 and len(fs) == 4 and all(len(self.f[fi]) == 4 for fi in fs)
        def weak(e):
            ff = self.edges[e]
            return len(ff) == 2 and self.n[ff[0]].dot(self.n[ff[1]]) < WEAK_DOT
        seeds = [e for e, ff in self.edges.items() if len(ff) == 2 and e not in self.smooth]
        for seed in seeds:
            for v in seed:
                e = seed
                while regular(v):
                    nxt = [x for x in at[v] if not set(self.edges[x]) & set(self.edges[e])]
                    if len(nxt) != 1 or nxt[0] not in self.smooth or not weak(nxt[0]):
                        break
                    e = nxt[0]
                    self.smooth.discard(e)
                    v = e[0] if e[1] == v else e[1]

    def drawn_edges(self):
        out = []
        for (a, b), ff in self.edges.items():
            front = [self.front[fi] for fi in ff]
            if len(ff) == 1:
                ok = True                       # open surface: both sides show
            elif (a, b) in self.smooth:
                ok = front[0] != front[1]       # outline of a smooth surface
            else:
                ok = any(front)                 # crease (or non-manifold edge)
            if ok:
                out.append((a, b))
        return out


class HiddenLines:
    def __init__(self, meshes, right, up, toward):
        """meshes: [(name, role, world verts, faces)] of every occluding part."""
        self.right, self.up, self.toward = right, up, toward
        self.meshes = [_Mesh(n, r, v, f, toward) for n, r, v, f in meshes]
        vv, ff = [], []
        self.base = []                            # global face offset per mesh
        self.byname = {}
        self.owner = []
        self.gn = []
        for mi, m in enumerate(self.meshes):
            off = len(vv)
            self.base.append(len(ff))
            vv.extend(m.v)
            ff.extend([tuple(off+i for i in f) for f in m.f])
            self.owner.extend([mi]*len(m.f))
            self.gn.extend(m.n)
            self.byname.setdefault(m.name, []).append(mi)
        self.bvh = BVHTree.FromPolygons(vv, ff, all_triangles=False) if ff else None
        self.skip = frozenset()                   # tube faces that may not hide the current mesh
        self.mounted = {}                         # mesh index -> faces of wires along it
        self.paths = []
        self.scale([True]*len(self.meshes), [])

    def scale(self, drawn, wires):
        """Sample spacing from the extent of what this view draws."""
        pts = [v for m, d in zip(self.meshes, drawn) if d for v in m.v]
        pts += [Vector(p) for _, ps, _ in wires for p in ps]
        xs = [v.dot(self.right) for v in pts] or [0.0]
        ys = [v.dot(self.up) for v in pts] or [0.0]
        self.extent = max(max(xs)-min(xs), max(ys)-min(ys), 1.0)
        self.step = self.extent*STEP_FRAC

    def mount(self, wires):
        """Tubes of wires that run along a part (see the module notes) stop hiding its lines."""
        def seg_dist(p, a, b):
            ab = b-a
            t = 0.0 if ab.length_squared == 0 else max(0.0, min(1.0, (p-a).dot(ab)/ab.length_squared))
            return (p-(a+ab*t)).length
        trees = {}
        for name, pts, _ in wires:
            pts = [Vector(p) for p in pts]
            tubes = [mi for mi in self.byname.get(name, ()) if self.meshes[mi].role == 'tube']
            if len(pts) < 2 or not tubes:
                continue
            radius = sorted(min(seg_dist(v, a, b) for a, b in zip(pts, pts[1:]))
                            for mi in tubes for v in self.meshes[mi].v)
            reach = radius[len(radius)//2] + MOUNT_GAP
            samples = []
            for a, b in zip(pts, pts[1:]):
                n = max(1, math.ceil((b-a).length/self.step/8))
                samples += [a.lerp(b, j/n) for j in range(n)]
            samples.append(pts[-1])
            lo = Vector((min(p.x for p in samples), min(p.y for p in samples), min(p.z for p in samples)))-Vector((reach,)*3)
            hi = Vector((max(p.x for p in samples), max(p.y for p in samples), max(p.z for p in samples)))+Vector((reach,)*3)
            faces = {self.base[mi]+fi for mi in tubes for fi in range(len(self.meshes[mi].f))}
            for hi_ in range(len(self.meshes)):
                m = self.meshes[hi_]
                if m.role == 'tube' or not m.f or hi_ in tubes:
                    continue
                if any(max(v[k] for v in m.v) < lo[k] or min(v[k] for v in m.v) > hi[k] for k in range(3)):
                    continue
                if hi_ not in trees:
                    trees[hi_] = BVHTree.FromPolygons(m.v, m.f, all_triangles=False)
                near = sum(1 for p in samples if trees[hi_].find_nearest(p, reach)[0] is not None)
                if near >= MOUNT_SHARE*len(samples):
                    self.mounted.setdefault(hi_, set()).update(faces)

    def xy(self, p):
        return [round(p.dot(self.right), 4), round(-p.dot(self.up), 4)]

    def visible(self, p, local, own=None, size=0.0):
        """No face in front of p, ignoring the global face ids in `local` and
        grazing hits on mesh `own` within `size` of p."""
        if self.bvh is None:
            return True
        t = self.toward
        origin = p + t*FAR
        for _ in range(96):
            loc, nrm, fi, dist = self.bvh.ray_cast(origin, -t, FAR*2)
            if loc is None or (loc-p).dot(t) <= DEPTH_TOL:
                return True                       # nothing, or the hit is at/behind p
            if fi in local or fi in self.skip or (own is not None and self.owner[fi] == own
                               and abs(self.gn[fi].dot(t)) < GRAZE and (loc-p).length < size):
                origin = loc - t*1e-4
                continue
            self.last_hit = fi                    # for diagnostics
            return False
        return True

    def trace(self, name, role, pts, locals_, own=None, sizes=None):
        """Append the visible parts of polyline pts (segment k tested with locals_[k])."""
        chain = []
        def flush():
            nonlocal chain
            if len(chain) > 1:
                self.paths.append(dict(name=name, points=chain, role=role))
            chain = []
        prev = None
        state = False
        for k, (a, b) in enumerate(zip(pts, pts[1:])):
            local = locals_[k]
            size = sizes[k] if sizes else 0.0
            n = max(1, math.ceil((b-a).length/self.step))
            prev_u = 0.0                          # prev (if any) is this segment's start
            for j in range(0 if k == 0 else 1, n+1):
                u = j/n
                p = a.lerp(b, u)
                vis = self.visible(p, local, own, size)
                if prev is not None and vis != state:
                    lo, hi = prev_u, u
                    for _ in range(BISECT):
                        mid = (lo+hi)*.5
                        if self.visible(a.lerp(b, mid), local, own, size) == state:
                            lo = mid
                        else:
                            hi = mid
                    q = self.xy(a.lerp(b, (lo+hi)*.5))
                    if state:
                        chain.append(q)
                        flush()
                    else:
                        chain = [q]
                if vis and (j == 0 or j == n):   # samples inside a straight segment add nothing
                    q = self.xy(p)
                    if not chain or chain[-1] != q:
                        chain.append(q)
                prev, prev_u, state = p, u, vis
        flush()

    def _ring(self, mi, verts):
        m, base = self.meshes[mi], self.base[mi]
        return {base+fi for vi in verts for fi in m.vfaces[vi]}

    def mesh_lines(self, mi):
        """Drawn edges of one mesh, chained through vertices where exactly two
        meet, clipped by exact visibility."""
        m = self.meshes[mi]
        v = m.v
        drawn = m.drawn_edges()
        at = {}
        for k, (a, b) in enumerate(drawn):
            at.setdefault(a, []).append(k)
            at.setdefault(b, []).append(k)
        used = [False]*len(drawn)
        def walk(k, node):
            vs, ks = [node], []
            while k is not None and not used[k]:
                used[k] = True
                a, b = drawn[k]
                node = b if a == node else a
                vs.append(node)
                ks.append(k)
                nxt = [x for x in at[node] if not used[x]]
                k = nxt[0] if len(at[node]) == 2 and nxt else None
            return vs, ks
        chains = []
        for k, (a, b) in enumerate(drawn):        # open chains start at an end
            if used[k]:
                continue
            for end in (a, b):
                if len(at[end]) != 2:
                    chains.append(walk(k, end))
                    break
        for k, (a, b) in enumerate(drawn):        # the rest are closed loops
            if not used[k]:
                chains.append(walk(k, a))
        def size(e):
            return max((v[x]-v[y]).length for fi in m.edges[e]
                       for f in (m.f[fi],) for x, y in zip(f, f[1:]+f[:1]))
        self.skip = frozenset(self.mounted.get(mi, ()))
        for vs, ks in chains:
            self.trace(m.name, m.role, [v[i] for i in vs],
                       [self._ring(mi, drawn[k]) for k in ks], own=mi,
                       sizes=[size(drawn[k]) for k in ks])
        self.skip = frozenset()

    def wire(self, name, pts, role):
        own = set()
        for mi in self.byname.get(name, ()):
            b = self.base[mi]
            own.update(range(b, b+len(self.meshes[mi].f)))
        self.trace(name, role, [Vector(p) for p in pts], [own]*(len(pts)-1))


def extract(meshes, wires, right, up, toward, draw=lambda name, role: role != 'tube',
            draw_wire=lambda name: True):
    """Visible paths [{name, points, role}] of meshes and wires in the view basis."""
    H = HiddenLines(meshes, right, up, toward)
    H.scale([draw(m.name, m.role) for m in H.meshes], [w for w in wires if draw_wire(w[0])])
    H.mount(wires)
    for mi, m in enumerate(H.meshes):
        if draw(m.name, m.role):
            H.mesh_lines(mi)
    for name, pts, role in wires:
        if draw_wire(name):
            H.wire(name, pts, role)
    return H.paths
