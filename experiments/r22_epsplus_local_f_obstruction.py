"""Independent exact obstruction for all epsilon=+1 scalar components of R(2,2).

The script uses only the R(2,2) fusion grammar, frozen canonical scalar-component
representatives, the commuting-character projective D gluing rule, two local
pentagons containing the stabilizer h, and exact determinant arithmetic.

It does not use cross-D amplitudes, E-layer associators, numerical solving, or
final four-noninvertible pentagons.

For each of the eight epsilon=+1 scalar components it enumerates the complete
52 x 52 projectively admissible character-sheet gluings on the two parity K4
history graphs and proves det(F^{XXX}_X) is the zero polynomial for every one.
"""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import product

ONE = "1"
G = ("1", "g", "h", "k")
M = ("X", "Y")
OBJECTS = G + M


def gmul(a, b):
    if a == ONE:
        return b
    if b == ONE:
        return a
    if a == b:
        return ONE
    return {
        frozenset(("g", "h")): "k",
        frozenset(("g", "k")): "h",
        frozenset(("h", "k")): "g",
    }[frozenset((a, b))]


def act(g, x):
    return x if g in (ONE, "h") else ("Y" if x == "X" else "X")


def fuse(a, b):
    if a in G and b in G:
        return {gmul(a, b): 1}
    if a in G and b in M:
        return {act(a, b): 1}
    if b in G and a in M:
        return {act(b, a): 1}
    if a == b == "X" or a == b == "Y":
        return {"1": 1, "h": 1, "X": 2, "Y": 2}
    if a in M and b in M:
        return {"g": 1, "k": 1, "X": 2, "Y": 2}
    raise ValueError((a, b))


def N(a, b, c):
    return fuse(a, b).get(c, 0)


def f_dim(key):
    a, b, c, d = key
    dl = sum(N(a, b, e) * N(e, c, d) for e in OBJECTS)
    dr = sum(N(b, c, f) * N(a, f, d) for f in OBJECTS)
    assert dl == dr
    return dl


def f_class(key):
    a, b, c, d = key
    nm = sum(x in M for x in (a, b, c))
    om = d in M
    return {
        (0, False): "A", (1, True): "B", (2, False): "C",
        (2, True): "D", (3, False): "E", (3, True): "F",
    }[(nm, om)]


SC_KEYS = sorted(
    (a, b, c, d)
    for a, b, c, d in product(OBJECTS, repeat=4)
    if ONE not in (a, b, c) and f_dim((a, b, c, d)) == 1
    and f_class((a, b, c, d)) in "ABC"
)
SC_INDEX = {k: i for i, k in enumerate(SC_KEYS)}
assert len(SC_KEYS) == 153

# Canonical representatives from the complete C* scalar-gauge quotient.
COMPONENT_REPS = [
    0,
    8375186228175,
    28475633175795,
    33500744912700,
    245290391601051373745507362430976,
    245290391601051373753882548659151,
    245290391601051373773982995606771,
    245290391601051373779008107343676,
    7500369583939335664664731354947763724618117171,
    7500369583939335664664731354947772099804345340,
    7500369583939335664664731354947792200251292864,
    7500369583939335664664731354947797225363029775,
    7500369583939580955056330045138267797157924915,
    7500369583939580955056330045138276172344153084,
    7500369583939580955056330045138296272791100608,
    7500369583939580955056330045138301297902837519,
]
EPS_INDEX = SC_INDEX[("h", "X", "h", "X")]
EPS_PLUS = [i for i, r in enumerate(COMPONENT_REPS) if ((r >> EPS_INDEX) & 1) == 0]
assert EPS_PLUS == [0, 1, 2, 3, 8, 9, 10, 11]

P0 = ((("a", "b"), "c"), "d")
P1 = (("a", ("b", "c")), "d")
P2 = ("a", (("b", "c"), "d"))
P4 = (("a", "b"), ("c", "d"))


def subtree_at(tree, path):
    n = tree
    for s in path:
        n = n[0] if s == "L" else n[1]
    return n


def leaves(node):
    return frozenset([node]) if isinstance(node, str) else leaves(node[0]) | leaves(node[1])


def rotate_right(tree, path=()):
    if not path:
        ab, c = tree
        a, b = ab
        return (a, (b, c))
    h, *t = path
    return (rotate_right(tree[0], tuple(t)), tree[1]) if h == "L" else (tree[0], rotate_right(tree[1], tuple(t)))


def enum_states(tree, leaf_labels, total=None):
    def rec(node, path):
        if isinstance(node, str):
            return [(leaf_labels[node], {})]
        out = []
        for la, sa in rec(node[0], path + ("L",)):
            for lb, sb in rec(node[1], path + ("R",)):
                for c, mult in fuse(la, lb).items():
                    for idx in range(mult):
                        st = dict(sa); st.update(sb); st[path] = (c, idx)
                        out.append((c, st))
        return out
    vals = rec(tree, ())
    if total is not None:
        vals = [(r, s) for r, s in vals if r == total]
    return [s for _, s in vals]


def root_label(tree, state, leaf_labels, path):
    n = subtree_at(tree, path)
    return leaf_labels[n] if isinstance(n, str) else state[path][0]


def leafsets_state(tree, state):
    out = {}
    def walk(node, path):
        if isinstance(node, str):
            return frozenset([node])
        s = walk(node[0], path + ("L",)) | walk(node[1], path + ("R",))
        out[s] = state[path]
        return s
    walk(tree, ())
    return out


@lru_cache(None)
def block_bases(key):
    a, b, c, d = key
    src, tgt = [], []
    for e in OBJECTS:
        for alpha in range(N(a, b, e)):
            for beta in range(N(e, c, d)):
                src.append((e, alpha, beta))
    for f in OBJECTS:
        for mu in range(N(b, c, f)):
            for nu in range(N(a, f, d)):
                tgt.append((f, mu, nu))
    assert len(src) == len(tgt)
    return tuple(src), tuple(tgt)


def strict_unit_entry(a, b, c, d, e, alpha, beta, f, mu, nu):
    if a == ONE:
        return int(e == b and alpha == 0 and f == d and nu == 0 and mu == beta)
    if b == ONE:
        return int(e == a and alpha == 0 and f == c and mu == 0 and nu == beta)
    if c == ONE:
        return int(e == d and beta == 0 and f == b and mu == 0 and nu == alpha)
    return None


def reassoc_desc(source, path, total, leaf_labels):
    target = rotate_right(source, path)
    sk = lambda st: tuple(sorted(st.items()))
    sb = sorted(enum_states(source, leaf_labels, total), key=sk)
    tb = sorted(enum_states(target, leaf_labels, total), key=sk)
    mat = [[0 for _ in sb] for _ in tb]
    pa, pb, pc = path + ("L", "L"), path + ("L", "R"), path + ("R",)
    pold, pout, pnew = path + ("L",), path, path + ("R",)
    local = leaves(subtree_at(source, path))
    for j, ss in enumerate(sb):
        a = root_label(source, ss, leaf_labels, pa)
        b = root_label(source, ss, leaf_labels, pb)
        c = root_label(source, ss, leaf_labels, pc)
        e, alpha = ss[pold]; d, beta = ss[pout]
        ssets = leafsets_state(source, ss)
        for i, ts in enumerate(tb):
            tsets = leafsets_state(target, ts)
            common = ssets.keys() & tsets.keys()
            if any(ssets[x] != tsets[x] for x in common if x != local):
                continue
            f, mu = ts[pnew]; dd, nu = ts[pout]
            if dd != d:
                continue
            u = strict_unit_entry(a, b, c, d, e, alpha, beta, f, mu, nu)
            if u is not None:
                mat[i][j] = u
            else:
                src, tgt = block_bases((a, b, c, d))
                ci = src.index((e, alpha, beta)); ri = tgt.index((f, mu, nu))
                mat[i][j] = ((a, b, c, d), ri, ci)
    return mat


TARGET = ("X", "X", "X", "X")
LOCAL_CASES = []
for external in (("X", "h", "X", "X"), ("X", "X", "X", "h")):
    labels = dict(zip("abcd", external))
    LOCAL_CASES.append((external, [
        reassoc_desc(P0, ("L",), "X", labels),
        reassoc_desc(P1, (), "X", labels),
        reassoc_desc(P2, ("R",), "X", labels),
        reassoc_desc(P0, (), "X", labels),
        reassoc_desc(P4, (), "X", labels),
    ]))


def flip(x):
    return "Y" if x == "X" else "X"


def edge_of(key):
    a, b, c, d = key
    if a in ("g", "k"):
        return ((flip(b), c, d), (b, c, flip(d)))
    if b in ("g", "k"):
        return ((flip(a), c, d), (a, flip(c), d))
    if c in ("g", "k"):
        return ((a, b, flip(d)), (a, flip(b), d))
    raise ValueError(key)


def parity(v):
    return sum(x == "Y" for x in v) % 2

D_KEYS = [
    (a, b, c, d)
    for a, b, c, d in product(OBJECTS, repeat=4)
    if ONE not in (a, b, c) and f_dim((a, b, c, d)) == 2
    and f_class((a, b, c, d)) == "D"
]
D_CROSS = [k for k in D_KEYS if "h" not in k[:3]]
D_SEED = set(k for k in D_KEYS if "h" in k[:3])
UND = {}
for k in D_CROSS:
    u, v = edge_of(k); und = tuple(sorted((u, v)))
    pos = next(i for i, x in enumerate(k[:3]) if x in ("g", "k"))
    vis = tuple(i for i in range(3) if i != pos)
    if und in UND:
        assert UND[und] == vis
    else:
        UND[und] = vis

PAIRS = [(a, b) for a in range(8) for b in range(a, 8)]

def cbits(ch):
    return tuple((ch >> i) & 1 for i in range(3))

def restr(ch, vis):
    b = cbits(ch)
    return tuple(b[i] for i in vis)

def compatible(p, q, vis):
    return sorted(restr(x, vis) for x in p) == sorted(restr(x, vis) for x in q)

def enumerate_parity(q):
    V = sorted({x for e in UND for x in e if parity(x) == q})
    edges = [(u, v, vis) for (u, v), vis in UND.items() if parity(u) == q]
    assert len(V) == 4 and len(edges) == 6
    nbr = {v: [] for v in V}
    for u, v, vis in edges:
        nbr[u].append((v, vis)); nbr[v].append((u, vis))
    sols = []
    def rec(i, A):
        if i == len(V):
            sols.append(dict(A)); return
        v = V[i]
        for pp in PAIRS:
            if all(u not in A or compatible(pp, A[u], vis) for u, vis in nbr[v]):
                A[v] = pp; rec(i + 1, A); A.pop(v)
    rec(0, {})
    assert len(sols) == 52
    return sols

GLUING0 = enumerate_parity(0)
GLUING1 = enumerate_parity(1)

PZERO = {}
PONE = {0: 1}
def padd(a, b, sign=1):
    d = dict(a)
    for m, c in b.items():
        v = d.get(m, 0) + sign * c
        if v: d[m] = v
        else: d.pop(m, None)
    return d

def pmul(a, b):
    d = {}
    for m, c in a.items():
        for n, e in b.items():
            d[m ^ n] = d.get(m ^ n, 0) + c * e
    return {m: c for m, c in d.items() if c}

def pconst(c):
    return {} if c == 0 else {0: int(c)}

seed_token = {}; seed_rev = []
def stoken(space, pos, sheet):
    k = (space, pos, sheet)
    if k not in seed_token:
        seed_token[k] = len(seed_rev); seed_rev.append(k)
    return {1 << seed_token[k]: 1}

ZERO = (PZERO, {})
def econst(c): return (pconst(c), {})
def evar(i): return (PZERO, {i: PONE})
def eadd(x, y, sign=1):
    c = padd(x[0], y[0], sign); d = {k: dict(v) for k, v in x[1].items()}
    for k, v in y[1].items():
        d[k] = padd(d.get(k, PZERO), v, sign)
        if not d[k]: d.pop(k, None)
    return c, d

def emul(x, y):
    c1, d1 = x; c2, d2 = y
    if d1 and d2: raise RuntimeError("nonlinear local-F product")
    d = {}
    if c1:
        for k, v in d2.items(): d[k] = padd(d.get(k, PZERO), pmul(c1, v))
    if c2:
        for k, v in d1.items(): d[k] = padd(d.get(k, PZERO), pmul(c2, v))
    return pmul(c1, c2), d

def matmul(A, B):
    C = [[ZERO for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for k in range(len(B)):
            if not A[i][k][0] and not A[i][k][1]: continue
            for j in range(len(B[0])):
                if B[k][j][0] or B[k][j][1]: C[i][j] = eadd(C[i][j], emul(A[i][k], B[k][j]))
    return C

def matsub(A, B):
    return [[eadd(A[i][j], B[i][j], -1) for j in range(len(A[0]))] for i in range(len(A))]

def seed_space_pos(key):
    a, b, c, d = key
    if a == "h": return (b, c, d), 0
    if b == "h": return (a, c, d), 1
    if c == "h": return (a, b, d), 2
    raise ValueError(key)


def compile_component(cid):
    bits = COMPONENT_REPS[cid]
    scalars = {k: (-1 if ((bits >> SC_INDEX[k]) & 1) else 1) for k in SC_KEYS}
    def block(key):
        if key in scalars:
            return [[econst(scalars[key])]]
        if key in D_SEED:
            spc, pos = seed_space_pos(key)
            return [[(stoken(spc, pos, 0), {}), ZERO], [ZERO, (stoken(spc, pos, 1), {})]]
        if key == TARGET:
            return [[evar(10 * i + j) for j in range(10)] for i in range(10)]
        raise RuntimeError(("unexpected local block", key, f_dim(key)))
    def eval_desc(desc):
        out = []
        for row in desc:
            rr = []
            for x in row:
                if isinstance(x, int): rr.append(econst(x))
                else:
                    key, i, j = x; rr.append(block(key)[i][j])
            out.append(rr)
        return out
    templates = []
    for meta, ds in LOCAL_CASES:
        m01, m12, m23, m04, m43 = [eval_desc(d) for d in ds]
        R = matsub(matmul(m23, matmul(m12, m01)), matmul(m43, m04))
        for i, row in enumerate(R):
            for j, (c, d) in enumerate(row):
                if c: raise RuntimeError(("constant obstruction before seed eval", meta, i, j, c))
                if d: templates.append((meta, i, j, d))
    return templates


def peval(P, signbits):
    return sum(c * (-1 if ((m & signbits).bit_count() & 1) else 1) for m, c in P.items())

def eval_rows(templates, assignment):
    sb = 0
    for t, (spc, pos, sheet) in enumerate(seed_rev):
        ch = assignment[spc][sheet]
        if (ch >> pos) & 1: sb |= 1 << t
    rows = []
    for _meta, _i, _j, d in templates:
        r = {}
        for v, P in d.items():
            c = peval(P, sb)
            if c: r[v] = int(c)
        if r: rows.append(r)
    return rows


class WeightedUF:
    def __init__(self, n):
        self.p = list(range(n)); self.w = [Fraction(1) for _ in range(n)]; self.forced = [False] * n
    def find(self, x):
        if self.p[x] == x: return x, self.w[x]
        p = self.p[x]; r, wp = self.find(p); self.w[x] *= wp; self.p[x] = r
        return r, self.w[x]
    def force(self, x):
        r, _ = self.find(x); self.forced[r] = True
    def relation(self, i, a, j, b):
        ri, wi = self.find(i); rj, wj = self.find(j)
        if ri == rj:
            if a * wi + b * wj != 0: self.forced[ri] = True
            return
        q = -(Fraction(a) * wi) / (Fraction(b) * wj)
        fi, fj = self.forced[ri], self.forced[rj]
        self.p[rj] = ri; self.w[rj] = q; self.forced[ri] = fi or fj
    def forced_roots(self):
        out = set()
        for i in range(len(self.p)):
            r, _ = self.find(i)
            if self.forced[r]: out.add(r)
        return out


def analyze_rows(rows):
    uf = WeightedUF(100)
    for r in rows:
        if len(r) == 1:
            (i, _a), = r.items(); uf.force(i)
        elif len(r) == 2:
            (i, a), (j, b) = list(r.items()); uf.relation(i, a, j, b)
        else:
            raise RuntimeError(("local equation support", len(r), r))
    return uf, uf.forced_roots()


def determinant_polynomial(rows):
    uf, forced = analyze_rows(rows)
    mat = []
    for i in range(10):
        rr = []
        for j in range(10):
            r, w = uf.find(10 * i + j)
            rr.append(None if r in forced else (r, w))
        mat.append(rr)
    dp = {0: {(): Fraction(1)}}
    for i in range(10):
        nd = {}
        for mask, poly in dp.items():
            for j in range(10):
                if (mask >> j) & 1 or mat[i][j] is None: continue
                r, w = mat[i][j]
                sign = -1 if ((mask >> (j + 1)).bit_count() & 1) else 1
                q = nd.setdefault(mask | (1 << j), {})
                fac = sign * w
                for mon, c in poly.items():
                    mm = tuple(sorted(mon + (r,)))
                    v = q.get(mm, Fraction(0)) + fac * c
                    if v: q[mm] = v
                    else: q.pop(mm, None)
        dp = nd
        if not dp: return {}
    return dp.get((1 << 10) - 1, {})


def main():
    total = 0
    for cid in EPS_PLUS:
        templates = compile_component(cid)
        bad = []
        for A0 in GLUING0:
            for A1 in GLUING1:
                det = determinant_polynomial(eval_rows(templates, {**A0, **A1}))
                if det: bad.append(det)
                total += 1
        print("component", cid, "branches", 2704, "nonzero determinant polynomials", len(bad))
        assert not bad
    print("TOTAL exact branches", total)
    print("RESULT: all epsilon=+1 branches force det(F^{XXX}_X) == 0")
    assert total == 21632


if __name__ == "__main__":
    main()
