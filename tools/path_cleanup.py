"""Clean exported visible-line paths before Cairo draws them.

The Blender exporters (tools/century/exporter.py, tools/hardware3d/family_core.py)
write every visible mesh edge as its own short path. Drawn one by one with butt
caps and alpha, that produces three kinds of artefact:

* split joins: consecutive edges of one contour meet as separate strokes, so the
  corner has a notch outside and a doubled (brighter) wedge inside;
* overlapping duplicates: coincident edges of two touching parts, or an edge and
  a clipped remnant of itself, are stroked on top of each other;
* near-miss ends: the visibility test accepts points up to 0.35 model units behind
  an occluder and samples edges every 1.1 units, so a clipped edge can stop short
  of the contour it meets (gap) or poke slightly past it (overshoot), and a
  hidden edge can leave a short isolated fragment (stray).

clean() fixes this in model units, once per loaded view:

1. endpoints closer than ``eps`` become one node (exporter rounding noise);
2. collinear overlapping segments are merged: the stronger role (or, within
   one role, the earlier path) keeps the overlap; only white roles are merged
   across roles, coloured roles only with themselves;
3. free ends (a path end nobody else touches) within ``r`` of other geometry
   are snapped to it: to a node, to the segment its own direction runs into
   (gap), or back to the segment it just crossed (overshoot);
4. very short open fragments that touch nothing within ``r`` and have no
   parallel neighbour (dashes, hatching) are dropped (strays);
5. segments of one role are chained through their shared nodes into long
   polylines (straightest continuation first, never through a hairpin), so each
   contour is a single stroke with real line joins. Closed contours get
   ``closed: True`` and repeat their first point, so a renderer that ignores
   the flag still draws exactly the same polyline.

Thresholds are the smaller of a model-unit cap and a fraction of the view's
extent; the fraction keeps them below about 3 px at the 5K master scale in
views drawn at high magnification, where model units are large on paper.

Nothing moves outward: points only snap to existing geometry and the convex
hull points of the view are never moved or dropped, so every renderer fits
the view (also after a camera roll) to exactly the same frame as before.
"""
import math
from collections import defaultdict

# Style rank for merging overlaps (the later-drawn, stronger stroke survives).
RANK = {'structure': 6, 'plate': 6, 'figure': 5, 'outline': 5, 'detail': 3, 'grass': 3,
        'shell': 1}
WHITE_ROLES = set(RANK)

# Model-unit caps: below the exporter's own tolerances (0.35 ray acceptance,
# 1.1 sample spacing), so no modelled feature of that size is at risk.
EPS_UNITS = 0.004      # same point (bisection resolution 1.1/2**8)
DUP_UNITS = 0.02       # coincident lines
SNAP_UNITS = 0.30      # gap / overshoot / near node
STRAY_UNITS = 0.35     # longest fragment that may be treated as a stray
# Fractions of the view's largest extent (B/C views ~1000 px, A ~1900 px wide).
EPS_FRAC = 1.0e-4
DUP_FRAC = 2.5e-4
SNAP_FRAC = 2.5e-3
STRAY_FRAC = 4.0e-3
HAIRPIN_DEG = 25.0     # never chain through a turn sharper than this
PARALLEL_SIN = math.sin(math.radians(2.0))


def thresholds(extent):
    return dict(eps=min(EPS_UNITS, EPS_FRAC*extent), dup=min(DUP_UNITS, DUP_FRAC*extent),
                snap=min(SNAP_UNITS, SNAP_FRAC*extent), stray=min(STRAY_UNITS, STRAY_FRAC*extent))


def _role(p):
    return p.get('role', p.get('kind'))


class _Geometry:
    """Segments and nodes of one view, in model units."""

    def __init__(self, paths, key=_role):
        self.key = key
        pts = [q for p in paths for q in p['points']]
        self.x0 = min(x for x, y in pts); self.x1 = max(x for x, y in pts)
        self.y0 = min(y for x, y in pts); self.y1 = max(y for x, y in pts)
        self.extent = max(self.x1-self.x0, self.y1-self.y0, 1e-9)
        self.t = thresholds(self.extent)
        self.paths = paths
        # Segment list: [a, b, role, path index]; a/b are node ids.
        self.xy = []            # node coordinates
        self.seg = []
        eps = self.t['eps']
        cell = {}
        def node(q):
            q = (float(q[0]), float(q[1]))
            cx, cy = math.floor(q[0]/eps), math.floor(q[1]/eps)
            best = None
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for n in cell.get((cx+dx, cy+dy), ()):
                        d = math.dist(self.xy[n], q)
                        if d <= eps and (best is None or d < best[0]):
                            best = (d, n)
            if best:
                return best[1]
            self.xy.append(q)
            cell.setdefault((cx, cy), []).append(len(self.xy)-1)
            return len(self.xy)-1
        # Convex-hull points fix the view's frame at any roll or rotation a
        # renderer applies: they keep their exact coordinates and never move.
        self.hull = set()
        for q in _hull(pts):
            self.xy.append(q)
            n = len(self.xy)-1
            self.hull.add(n)
            cell.setdefault((math.floor(q[0]/eps), math.floor(q[1]/eps)), []).append(n)
        for i, p in enumerate(paths):
            ids = [node(q) for q in p['points']]
            for a, b in zip(ids, ids[1:]):
                if a != b:
                    self.seg.append([a, b, key(p), i])

    # -- helpers ---------------------------------------------------------

    def extreme(self, n):
        return n in self.hull

    def live(self):
        return [k for k, s in enumerate(self.seg) if s is not None]

    def index(self, cell):
        g = defaultdict(list)
        for k in self.live():
            a, b = self.xy[self.seg[k][0]], self.xy[self.seg[k][1]]
            for x in range(math.floor(min(a[0], b[0])/cell), math.floor(max(a[0], b[0])/cell)+1):
                for y in range(math.floor(min(a[1], b[1])/cell), math.floor(max(a[1], b[1])/cell)+1):
                    g[(x, y)].append(k)
        return g

    def near(self, g, cell, q, r):
        out = set()
        for x in range(math.floor((q[0]-r)/cell), math.floor((q[0]+r)/cell)+1):
            for y in range(math.floor((q[1]-r)/cell), math.floor((q[1]+r)/cell)+1):
                out.update(g.get((x, y), ()))
        return out

    def ends(self):
        """node -> list of (segment, which end)."""
        e = defaultdict(list)
        for k in self.live():
            e[self.seg[k][0]].append((k, 0))
            e[self.seg[k][1]].append((k, 1))
        return e


def _hull(pts):
    """Convex hull vertices (monotone chain), as float tuples."""
    P = sorted({(float(x), float(y)) for x, y in pts})
    if len(P) < 3:
        return P
    def half(seq):
        h = []
        for q in seq:
            while len(h) > 1 and ((h[-1][0]-h[-2][0])*(q[1]-h[-2][1])
                                  - (h[-1][1]-h[-2][1])*(q[0]-h[-2][0])) <= 0:
                h.pop()
            h.append(q)
        return h
    return half(P)[:-1] + half(P[::-1])[:-1]


def _closest(p, a, b):
    dx, dy = b[0]-a[0], b[1]-a[1]
    L2 = dx*dx+dy*dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0]-a[0])*dx+(p[1]-a[1])*dy)/L2))
    q = (a[0]+t*dx, a[1]+t*dy)
    return math.dist(p, q), t, q


def _cross(p, r, q, s):
    """Intersection parameters of p + t r and q + u s, or None if parallel."""
    den = r[0]*s[1]-r[1]*s[0]
    if abs(den) < 1e-15:
        return None
    w = (q[0]-p[0], q[1]-p[1])
    return (w[0]*s[1]-w[1]*s[0])/den, (w[0]*r[1]-w[1]*r[0])/den


# ---------------------------------------------------------------------------
# 2. overlapping duplicates
# ---------------------------------------------------------------------------

def _duplicates(G, apply):
    """Find (and optionally remove) collinear overlaps. Returns [(length, point, roles)]."""
    dup = G.t['dup']
    cell = max(G.t['snap']*4, G.extent/256)
    g = G.index(cell)
    seen = set()
    removed = defaultdict(list)     # loser segment -> [(t0, t1)]
    found = []
    for key, members in g.items():
        for i in range(len(members)):
            for j in range(i+1, len(members)):
                a, b = members[i], members[j]
                if (a, b) in seen:
                    continue
                seen.add((a, b))
                sa, sb = G.seg[a], G.seg[b]
                ra, rb = sa[2], sb[2]
                if ra != rb and not (ra in WHITE_ROLES and rb in WHITE_ROLES):
                    continue
                p0, p1 = G.xy[sa[0]], G.xy[sa[1]]
                q0, q1 = G.xy[sb[0]], G.xy[sb[1]]
                u = (p1[0]-p0[0], p1[1]-p0[1]); v = (q1[0]-q0[0], q1[1]-q0[1])
                lu, lv = math.hypot(*u), math.hypot(*v)
                if abs(u[0]*v[1]-u[1]*v[0]) > PARALLEL_SIN*lu*lv:
                    continue
                # Parameters of b's ends on a's line, and their offsets from it.
                def along(q): return ((q[0]-p0[0])*u[0]+(q[1]-p0[1])*u[1])/(lu*lu)
                t0, t1 = sorted((along(q0), along(q1)))
                lo, hi = max(0.0, t0), min(1.0, t1)
                if (hi-lo)*lu <= G.t['eps']:
                    continue
                # Offsets where the overlap begins and ends (b is straight).
                def at(t):
                    x, y = p0[0]+u[0]*t, p0[1]+u[1]*t
                    return _closest((x, y), q0, q1)[0]
                if at(lo) > dup or at(hi) > dup:
                    continue
                # Winner: stronger role, then the earlier path.
                ka = (RANK.get(ra, 4), -sa[3], -a); kb = (RANK.get(rb, 4), -sb[3], -b)
                if ka > kb:
                    loser, w_lo, w_hi = b, t0, t1
                    # Overlap interval in the loser's own parameter.
                    lp0, lp1 = q0, q1; lw = v; ll = lv
                    x0 = (p0[0]+u[0]*lo, p0[1]+u[1]*lo); x1 = (p0[0]+u[0]*hi, p0[1]+u[1]*hi)
                else:
                    loser = a
                    lp0, lp1 = p0, p1; lw = u; ll = lu
                    x0 = (p0[0]+u[0]*lo, p0[1]+u[1]*lo); x1 = (p0[0]+u[0]*hi, p0[1]+u[1]*hi)
                def own(q): return ((q[0]-lp0[0])*lw[0]+(q[1]-lp0[1])*lw[1])/(ll*ll)
                s0, s1 = sorted((own(x0), own(x1)))
                removed[loser].append((max(0.0, s0), min(1.0, s1)))
                found.append(((hi-lo)*lu, ((x0[0]+x1[0])/2, (x0[1]+x1[1])/2), (ra, rb)))
    if apply:
        for k, spans in removed.items():
            s = G.seg[k]
            if s is None:
                continue
            spans.sort()
            keep, cur = [], 0.0
            # The points that fix the view's frame stay drawn.
            spans = [(s0, s1) for s0, s1 in spans
                     if not ((s0 <= 0.0 and G.extreme(s[0])) or (s1 >= 1.0 and G.extreme(s[1])))]
            for s0, s1 in spans:
                if s0 > cur:
                    keep.append((cur, s0))
                cur = max(cur, s1)
            if cur < 1.0:
                keep.append((cur, 1.0))
            a, b = G.xy[s[0]], G.xy[s[1]]
            L = math.dist(a, b)
            G.seg[k] = None
            for t0, t1 in keep:
                if (t1-t0)*L <= G.t['eps']:
                    continue
                def pt(t, n0=s[0], n1=s[1]):
                    if t <= 0.0:
                        return n0
                    if t >= 1.0:
                        return n1
                    G.xy.append((a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t))
                    return len(G.xy)-1
                G.seg.append([pt(t0), pt(t1), s[2], s[3]])
    return found


# ---------------------------------------------------------------------------
# 3. near-miss ends
# ---------------------------------------------------------------------------

def _free_ends(G):
    e = G.ends()
    return e, sorted(n for n, lst in e.items() if len(lst) == 1)


def _near_miss(G, apply):
    """Free ends within snap distance of other geometry. Returns [(kind, dist, point)]."""
    r = G.t['snap']; eps = G.t['eps']
    cell = max(r*4, G.extent/256)
    g = G.index(cell)
    e, free = _free_ends(G)
    found = []
    moved = set()
    for n in free:
        if len(e.get(n, ())) != 1 or G.extreme(n):
            continue
        k, which = e[n][0]
        s = G.seg[k]
        if s is None:
            continue
        other = s[1-which]
        p = G.xy[n]; o = G.xy[other]
        L = math.dist(p, o)
        if L == 0:
            continue
        u = ((p[0]-o[0])/L, (p[1]-o[1])/L)          # outward direction
        best = None
        for j in G.near(g, cell, p, r):
            t = G.seg[j]
            if t is None or j == k:
                continue
            a, b = G.xy[t[0]], G.xy[t[1]]
            if n in (t[0], t[1]):
                continue
            # (a) a node of another segment
            for m in (t[0], t[1]):
                if m == other:
                    continue
                d = math.dist(p, G.xy[m])
                if eps < d <= r:
                    w = ((G.xy[m][0]-p[0])/d, (G.xy[m][1]-p[1])/d)
                    ahead = w[0]*u[0]+w[1]*u[1]
                    if d <= r/2 or ahead >= .5:
                        cand = (d, 'node', m, G.xy[m])
                        best = cand if best is None or cand[0] < best[0] else best
            # (b) gap: own direction runs into the segment within r
            x = _cross(p, u, a, (b[0]-a[0], b[1]-a[1]))
            if x is not None:
                tt, uu = x
                if 1e-9 < uu < 1-1e-9:
                    q = (a[0]+(b[0]-a[0])*uu, a[1]+(b[1]-a[1])*uu)
                    if eps < tt <= r:
                        cand = (tt, 'gap', None, q)
                        best = cand if best is None or cand[0] < best[0] else best
                    elif -min(r, L*.5) <= tt < -eps:
                        # (c) overshoot: the end already crossed it
                        cand = (-tt, 'overshoot', None, q)
                        best = cand if best is None or cand[0] < best[0] else best
            # a near-touch sideways (end almost on a segment)
            d, tpar, q = _closest(p, a, b)
            if eps < d <= r/3 and 1e-6 < tpar < 1-1e-6:
                cand = (d, 'touch', None, q)
                best = cand if best is None or cand[0] < best[0] else best
        if best is None:
            continue
        found.append((best[1], best[0], p))
        if apply and n not in moved:
            d, kind, m, q = best
            if kind == 'node':
                if m == other:
                    continue
                s[which] = m
                moved.add(m)
            else:
                G.xy[n] = q
            moved.add(n)
    return found


# ---------------------------------------------------------------------------
# 4. strays
# ---------------------------------------------------------------------------

def _strays(G, apply):
    """Short open fragments touching nothing. Returns [(length, point, n_segments)]."""
    r = G.t['snap']; limit = G.t['stray']
    parent = {}
    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for k in G.live():
        a, b = G.seg[k][:2]
        parent[find(a)] = find(b)
    comps = defaultdict(list)
    for k in G.live():
        comps[find(G.seg[k][0])].append(k)
    e = G.ends()
    cell = max(r*4, G.extent/256)
    g = G.index(cell)
    found = []
    for root, ks in comps.items():
        length = sum(math.dist(G.xy[G.seg[k][0]], G.xy[G.seg[k][1]]) for k in ks)
        if length > limit:
            continue
        nodes = {n for k in ks for n in G.seg[k][:2]}
        if not any(len(e[n]) == 1 for n in nodes):
            continue                                  # closed loop: a real detail
        if any(G.seg[k][2] not in WHITE_ROLES for k in ks):
            continue                                  # cables, accents: authored
        if any(G.extreme(n) for n in nodes):
            continue
        mine = set(ks)
        touching = False
        for k in ks:
            a, b = G.xy[G.seg[k][0]], G.xy[G.seg[k][1]]
            for j in G.near(g, cell, a, r) | G.near(g, cell, b, r):
                if j in mine or G.seg[j] is None:
                    continue
                c0, c1 = G.xy[G.seg[j][0]], G.xy[G.seg[j][1]]
                if _seg_dist(a, b, c0, c1) <= r:
                    touching = True
                    break
            if touching:
                break
        if touching or _patterned(G, g, cell, ks, max(length, r)*4):
            continue
        mid = G.xy[G.seg[ks[0]][0]]
        found.append((length, mid, len(ks)))
        if apply:
            for k in ks:
                G.seg[k] = None
    return found


def _patterned(G, g, cell, ks, radius):
    """True if a nearby segment runs parallel: a dash of a dashed line or one
    stroke of hatching, which are intended details, not strays."""
    nodes = [n for k in ks for n in G.seg[k][:2]]
    a = G.xy[nodes[0]]
    b = max((G.xy[n] for n in nodes), key=lambda q: math.dist(a, q))
    L = math.dist(a, b)
    if L == 0:
        return False
    u = ((b[0]-a[0])/L, (b[1]-a[1])/L)
    mid = ((a[0]+b[0])/2, (a[1]+b[1])/2)
    mine = set(ks)
    for j in G.near(g, cell, mid, radius):
        t = G.seg[j]
        if j in mine or t is None:
            continue
        c, d = G.xy[t[0]], G.xy[t[1]]
        M = math.dist(c, d)
        if M == 0 or _closest(mid, c, d)[0] > radius:
            continue
        if abs(u[0]*(d[1]-c[1])-u[1]*(d[0]-c[0]))/M < math.sin(math.radians(10)):
            return True
    return False


def _seg_dist(a, b, c, d):
    x = _cross(a, (b[0]-a[0], b[1]-a[1]), c, (d[0]-c[0], d[1]-c[1]))
    if x is not None and 0 <= x[0] <= 1 and 0 <= x[1] <= 1:
        return 0.0
    return min(_closest(a, c, d)[0], _closest(b, c, d)[0], _closest(c, a, b)[0], _closest(d, a, b)[0])


# ---------------------------------------------------------------------------
# 5. chaining
# ---------------------------------------------------------------------------

def _split_joins(G):
    """Nodes where exactly two separate paths of one role meet end to end."""
    e = G.ends()
    count = 0
    for n, lst in e.items():
        if len(lst) == 2:
            (k0, _), (k1, _) = lst
            s0, s1 = G.seg[k0], G.seg[k1]
            if s0[3] != s1[3] and s0[2] == s1[2]:
                count += 1
    return count


def _chain(G):
    e = G.ends()
    cos_hairpin = math.cos(math.radians(HAIRPIN_DEG))
    def direction(k, at):
        s = G.seg[k]
        a = G.xy[at]; b = G.xy[s[1] if s[0] == at else s[0]]
        L = math.dist(a, b) or 1.0
        return ((b[0]-a[0])/L, (b[1]-a[1])/L)
    # Pair the segments at every node: same role, straightest first.
    partner = {}
    for n, lst in e.items():
        if len(lst) < 2:
            continue
        pairs = []
        for i in range(len(lst)):
            for j in range(i+1, len(lst)):
                ki, kj = lst[i][0], lst[j][0]
                if G.seg[ki][2] != G.seg[kj][2] or ki == kj:
                    continue
                di, dj = direction(ki, n), direction(kj, n)
                c = di[0]*dj[0]+di[1]*dj[1]        # -1 = straight on
                if c > cos_hairpin:
                    continue                        # hairpin: keep the tip
                pairs.append((c, min(G.seg[ki][3], G.seg[kj][3]), ki, kj))
        pairs.sort()
        used = set()
        for c, _, ki, kj in pairs:
            if ki in used or kj in used:
                continue
            used.update((ki, kj))
            partner[(n, ki)] = kj
            partner[(n, kj)] = ki
    done = set()
    chains = []
    def walk(k, start):
        """Follow from node `start` through segment k."""
        nodes = [start]
        ks = []
        cur, at = k, start
        while cur is not None and cur not in done:
            done.add(cur)
            ks.append(cur)
            s = G.seg[cur]
            nxt = s[1] if s[0] == at else s[0]
            nodes.append(nxt)
            at = nxt
            cur = partner.get((at, cur))
        return nodes, ks
    live = G.live()
    # Open chains start where a segment has no partner.
    for k in live:
        if k in done:
            continue
        s = G.seg[k]
        for end in (s[0], s[1]):
            if (end, k) not in partner:
                nodes, ks = walk(k, end)
                chains.append((nodes, ks))
                break
    for k in live:                                  # the rest are closed loops
        if k in done:
            continue
        s = G.seg[k]
        nodes, ks = walk(k, s[0])
        chains.append((nodes, ks))
    out = []
    for nodes, ks in chains:
        first = min(G.seg[k][3] for k in ks)
        src = G.paths[first]
        p = {key: val for key, val in src.items() if key != 'points'}
        p['points'] = [[round(G.xy[n][0], 5), round(G.xy[n][1], 5)] for n in nodes]
        if len(nodes) > 3 and nodes[0] == nodes[-1]:
            p['closed'] = True
        out.append((first, min(ks), p))
    out.sort(key=lambda t: (t[0], t[1]))
    return [p for _, _, p in out]


def _purge(G):
    """Drop segments that snapping reduced to (almost) a point, and exact
    repeats of a segment between the same two nodes in the same colour."""
    seen = {}
    for k, s in enumerate(G.seg):
        if s is None:
            continue
        if s[0] == s[1] or math.dist(G.xy[s[0]], G.xy[s[1]]) <= G.t['eps']*.5:
            G.seg[k] = None
            continue
        colour = 'white' if s[2] in WHITE_ROLES else s[2]
        key = (min(s[0], s[1]), max(s[0], s[1]), colour)
        if key in seen:
            j = seen[key]
            keep, drop = (j, k) if RANK.get(G.seg[j][2], 4) >= RANK.get(s[2], 4) else (k, j)
            G.seg[drop] = None
            seen[key] = keep
        else:
            seen[key] = k


# ---------------------------------------------------------------------------
# public
# ---------------------------------------------------------------------------

def analyse(paths, key=_role):
    """Issue counts and locations of one view (nothing is changed)."""
    G = _Geometry(paths, key)
    dup = _duplicates(G, apply=False)
    near = _near_miss(G, apply=False)
    stray = _strays(G, apply=False)
    return dict(thresholds=G.t, extent=G.extent, paths=len(paths),
                split_joins=_split_joins(G), duplicates=dup, near_miss=near, strays=stray)


def clean(paths, key=_role):
    """Return cleaned paths (new list; input untouched)."""
    if not paths:
        return paths
    G = _Geometry(paths, key)
    for _ in range(3):
        # Snapping can expose new overlaps and merging new free ends.
        _purge(G)
        d = _duplicates(G, apply=True)
        _purge(G)
        n = _near_miss(G, apply=True)
        _purge(G)
        if not d and not n:
            break
    _purge(G)
    _duplicates(G, apply=True)
    _purge(G)
    _strays(G, apply=True)
    return _chain(G)


def clean_view(data, key=_role):
    """clean() the 'paths' of a loaded view dict in place and return it."""
    data['paths'] = clean(data['paths'], key)
    return data


_CACHE = {}


def load(path):
    """Read an exported view (JSON with 'paths') and return it cleaned.

    Cleaned geometry is cached per file and modification time; every call
    returns fresh dicts, so callers may transform points in place.
    """
    import json
    import os
    from pathlib import Path
    path = Path(path)
    stamp = (str(path.resolve()), os.stat(path).st_mtime_ns)
    if stamp not in _CACHE:
        data = json.loads(path.read_text())
        if os.environ.get('PBLOOM_RAW_PATHS') != '1':
            data['paths'] = clean(data['paths'])
        _CACHE[stamp] = data
    data = _CACHE[stamp]
    out = {k: v for k, v in data.items() if k != 'paths'}
    out['paths'] = [dict(p, points=[list(q) for q in p['points']]) for p in data['paths']]
    return out


def points(path):
    """Points to stroke and whether to close the stroke (closed contours
    repeat their first point; drawing that point again would leave a cap)."""
    pts = path['points']
    if path.get('closed') and len(pts) > 3 and pts[0] == pts[-1]:
        return pts[:-1], True
    return pts, False


def trace(c, path):
    """Add one path to a Cairo context (new path), closing closed contours."""
    pts, closed = points(path)
    c.new_path()
    c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    if closed:
        c.close_path()
