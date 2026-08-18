from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product

import numpy as np
import sympy as sp

ONE = "1"
G = ("1", "g", "h", "k")  # k = gh
M = ("X", "Y")
OBJECTS = G + M


def gmul(a: str, b: str) -> str:
    if a == ONE:
        return b
    if b == ONE:
        return a
    if a == b:
        return ONE
    table = {
        frozenset(("g", "h")): "k",
        frozenset(("g", "k")): "h",
        frozenset(("h", "k")): "g",
    }
    return table[frozenset((a, b))]


def act(g: str, x: str) -> str:
    # h is the stabilizer of the noninvertible orbit; g,k exchange X,Y.
    if g in (ONE, "h"):
        return x
    return "Y" if x == "X" else "X"


def fuse(a: str, b: str) -> dict[str, int]:
    """Meng--Yu R(2,2) fusion ring."""
    if a in G and b in G:
        return {gmul(a, b): 1}
    if a in G and b in M:
        return {act(a, b): 1}
    if b in G and a in M:
        return {act(b, a): 1}
    if a == b == "X" or a == b == "Y":
        return {"1": 1, "h": 1, "X": 2, "Y": 2}
    if a in M and b in M:
        # XY = g X^2 because Y=gX and the ring is commutative.
        return {"g": 1, "k": 1, "X": 2, "Y": 2}
    raise ValueError((a, b))


def N(a: str, b: str, c: str) -> int:
    return fuse(a, b).get(c, 0)


def verify_ring() -> None:
    for a, b, c in product(OBJECTS, repeat=3):
        left = defaultdict(int)
        right = defaultdict(int)
        for x, nx in fuse(a, b).items():
            for y, ny in fuse(x, c).items():
                left[y] += nx * ny
        for x, nx in fuse(b, c).items():
            for y, ny in fuse(a, x).items():
                right[y] += nx * ny
        assert dict(left) == dict(right), (a, b, c, left, right)


def fusion_matrix(a: str) -> sp.Matrix:
    mat = sp.zeros(len(OBJECTS))
    for j, b in enumerate(OBJECTS):
        for c, mult in fuse(a, b).items():
            mat[OBJECTS.index(c), j] = mult
    return mat


def f_blocks() -> list[tuple[str, str, str, str, int]]:
    out = []
    for a, b, c, d in product(OBJECTS, repeat=4):
        dim_l = sum(N(a, b, e) * N(e, c, d) for e in OBJECTS)
        dim_r = sum(N(b, c, f) * N(a, f, d) for f in OBJECTS)
        assert dim_l == dim_r
        if dim_l:
            out.append((a, b, c, d, dim_l))
    return out


def pentagon_blocks() -> list[tuple[str, str, str, str, str, int]]:
    out = []
    for a, b, c, d, z in product(OBJECTS, repeat=5):
        dim = 0
        for x in OBJECTS:
            for y in OBJECTS:
                dim += N(a, b, x) * N(x, c, y) * N(y, d, z)
        if dim:
            out.append((a, b, c, d, z, dim))
    return out


def f_class(key: tuple[str, str, str, str]) -> str:
    a, b, c, d = key
    n_m = sum(x in M for x in (a, b, c))
    out_m = d in M
    classes = {
        (0, False): "A",  # pointed
        (1, True): "B",   # module/action scalar
        (2, False): "C",  # pair -> invertible scalar
        (2, True): "D",   # pair -> noninvertible, 2x2
        (3, False): "E",  # triple -> invertible, 2x2
        (3, True): "F",   # triple -> noninvertible, 8x8/10x10
    }
    return classes[(n_m, out_m)]


def support(a: str, b: str) -> list[str]:
    return list(fuse(a, b))


def pentagon_roles(a: str, b: str, c: str, d: str, z: str):
    """Block types occurring in the five associator positions of a pentagon."""
    roles = {r: set() for r in ("L1", "L2", "L3", "S1", "S2")}

    for x in support(a, b):
        for y in support(x, c):
            if N(y, d, z):
                roles["L1"].add((a, b, c, y))

    for f in support(b, c):
        if any(N(a, f, y) * N(y, d, z) for y in OBJECTS):
            roles["L2"].add((a, f, d, z))

    for f in support(b, c):
        for y in support(f, d):
            if N(a, y, z):
                roles["L3"].add((b, c, d, y))

    for x in support(a, b):
        if any(N(x, c, y) * N(y, d, z) for y in OBJECTS):
            roles["S1"].add((x, c, d, z))

    for r in support(c, d):
        if any(N(a, b, x) * N(x, r, z) for x in OBJECTS):
            roles["S2"].add((a, b, r, z))

    return roles


def pentagon_deps(a: str, b: str, c: str, d: str, z: str) -> set[tuple[str, str, str, str]]:
    roles = pentagon_roles(a, b, c, d, z)
    ans = set()
    for s in roles.values():
        ans |= s
    return ans


def layer_spec(layer: str, p: tuple[str, str, str, str, str, int]) -> bool:
    a, b, c, d, z, _ = p
    n_m = sum(x in M for x in (a, b, c, d))
    if layer == "A":
        return n_m == 0
    if layer == "B":
        return n_m == 1
    if layer == "C":
        return n_m == 2 and z in G
    if layer == "D":
        return n_m == 2 and z in M
    if layer == "E":
        return n_m == 3 and z in G
    if layer == "F":
        return n_m == 3 and z in M
    raise ValueError(layer)


def bootstrap(blockset, equations, seeds=()):
    known = set(seeds)
    rounds = []
    while True:
        new = set()
        for deps in equations:
            rem = deps - known
            if len(rem) == 1:
                new |= rem
        new -= known
        if not new:
            return known, rounds
        known |= new
        rounds.append(len(new))


def scalar_gauge_audit(nonunit_blocks):
    triples = []
    for a, b in product(OBJECTS, repeat=2):
        for c, mult in fuse(a, b).items():
            if a != ONE and b != ONE:
                triples.append((a, b, c, mult))

    scalar_gauges = [(a, b, c) for a, b, c, mult in triples if mult == 1]
    idx = {g: i for i, g in enumerate(scalar_gauges)}

    def unique_paths(key):
        a, b, c, d = key
        left = [e for e in OBJECTS if N(a, b, e) == 1 and N(e, c, d) == 1]
        right = [f for f in OBJECTS if N(b, c, f) == 1 and N(a, f, d) == 1]
        assert len(left) == len(right) == 1
        return left[0], right[0]

    def row(key):
        a, b, c, d = key
        e, f = unique_paths(key)
        v = [0] * len(scalar_gauges)
        for t, sign in [
            ((a, b, e), +1),
            ((e, c, d), +1),
            ((b, c, f), -1),
            ((a, f, d), -1),
        ]:
            if t in idx:
                v[idx[t]] += sign
        return v

    by_class = defaultdict(list)
    for a, b, c, d, dim in nonunit_blocks:
        if dim == 1 and f_class((a, b, c, d)) in "ABC":
            by_class[f_class((a, b, c, d))].append((a, b, c, d))

    matrices = {}
    running = []
    for cl in "ABC":
        running += sorted(by_class[cl])
        matrices[cl] = sp.Matrix([row(k) for k in running])

    seed_b = ("g", "X", "g", "X")
    seed_c = ("X", "g", "X", "g")
    rb = sp.Matrix([row(seed_b)])
    rc = sp.Matrix([row(seed_c)])
    null_a = matrices["A"].nullspace()
    null_ab = matrices["B"].nullspace()
    b_movable = any((rb * v)[0] != 0 for v in null_a)
    c_movable = any((rc * v)[0] != 0 for v in null_ab)

    gauge_dim = sum(mult * mult for *_, mult in triples)
    return {
        "gauge_blocks": Counter(mult for *_, mult in triples),
        "gauge_dimension": gauge_dim,
        "scalar_gauge_count": len(scalar_gauges),
        "rank_A": matrices["A"].rank(),
        "rank_AB": matrices["B"].rank(),
        "rank_ABC": matrices["C"].rank(),
        "seed_B_gauge_fixable_after_A": b_movable,
        "seed_C_gauge_fixable_after_AB": c_movable,
        "seed_B": seed_b,
        "seed_C": seed_c,
    }


def main() -> None:
    verify_ring()

    nx = fusion_matrix("X")
    d = sp.Integer(2) + sp.sqrt(6)
    global_dim = sp.simplify(4 + 2 * d**2)
    np_eigs = np.linalg.eigvals(np.array(nx.tolist(), dtype=float))
    np_radius = max(abs(np_eigs))
    assert abs(np_radius - float(d)) < 1e-10

    print("R(2,2) exact FP data")
    print("  charpoly(N_X) =", sp.factor(nx.charpoly().as_expr()))
    print("  FPdim(X) =", d)
    print("  FPdim(C) =", global_dim)
    print("  numpy spectral radius cross-check =", np_radius)

    triples = []
    for a, b in product(OBJECTS, repeat=2):
        for c, mult in fuse(a, b).items():
            triples.append((a, b, c, mult))
    print("\nfusion spaces")
    print("  nonzero triples =", len(triples), Counter(t[-1] for t in triples))

    fb = f_blocks()
    nonunit_fb = [x for x in fb if ONE not in x[:3]]
    print("\nF-block scale")
    print("  all blocks =", len(fb), Counter(x[-1] for x in fb))
    print("  all scalar entries =", sum(x[-1] ** 2 for x in fb))
    print("  strict-unit nontrivial blocks =", len(nonunit_fb), Counter(x[-1] for x in nonunit_fb))
    print("  strict-unit nontrivial scalar entries =", sum(x[-1] ** 2 for x in nonunit_fb))

    layer_blocks = {cl: set() for cl in "ABCDEF"}
    layer_entries = Counter()
    layer_dims = {cl: Counter() for cl in "ABCDEF"}
    for a, b, c, d0, dim in nonunit_fb:
        cl = f_class((a, b, c, d0))
        layer_blocks[cl].add((a, b, c, d0))
        layer_entries[cl] += dim * dim
        layer_dims[cl][dim] += 1
    print("\nlayered F-blocks")
    for cl in "ABCDEF":
        print(f"  {cl}: blocks={len(layer_blocks[cl])}, entries={layer_entries[cl]}, dims={dict(layer_dims[cl])}")

    pb = pentagon_blocks()
    nonunit_pb = [x for x in pb if ONE not in x[:4]]
    print("\npentagon scale")
    print("  all blocks =", len(pb), Counter(x[-1] for x in pb), "scalar_eqs=", sum(x[-1] ** 2 for x in pb))
    print("  nonunit external blocks =", len(nonunit_pb), Counter(x[-1] for x in nonunit_pb), "scalar_eqs=", sum(x[-1] ** 2 for x in nonunit_pb))

    all_unknown = set((a, b, c, d0) for a, b, c, d0, _ in nonunit_fb)
    eqs = []
    for p in nonunit_pb:
        deps = pentagon_deps(*p[:5]) & all_unknown
        eqs.append((p, deps))

    print("\nlocalization / block-dependency bootstrap")
    bootstrap_data = {}
    for cl in "ABCDEF":
        layer_eqs = [deps & layer_blocks[cl] for p, deps in eqs if layer_spec(cl, p)]
        singleton_cover = {next(iter(x)) for x in layer_eqs if len(x) == 1}
        known, rounds = bootstrap(layer_blocks[cl], layer_eqs)
        bootstrap_data[cl] = (layer_eqs, known, rounds)
        print(
            f"  {cl}: direct_singleton_cover={len(singleton_cover)}/{len(layer_blocks[cl])}, "
            f"bootstrap={len(known)}/{len(layer_blocks[cl])}, rounds={rounds}, "
            f"same-layer dependency sizes={dict(Counter(len(x) for x in layer_eqs))}"
        )

    seed_b = ("g", "X", "g", "X")
    seed_c = ("X", "g", "X", "g")
    for cl, seed in (("B", seed_b), ("C", seed_c)):
        layer_eqs = bootstrap_data[cl][0]
        known, rounds = bootstrap(layer_blocks[cl], layer_eqs, seeds=(seed,))
        assert len(known) == len(layer_blocks[cl])
        print(f"  {cl} + one seed {seed}: closes all {len(known)} blocks in rounds {rounds}")

    long_roles = {"L1", "L2", "L3"}
    short_roles = {"S1", "S2"}
    for cl in ("D", "E", "F"):
        profiles = Counter()
        for p, deps in eqs:
            if not layer_spec(cl, p):
                continue
            same = deps & layer_blocks[cl]
            if len(same) != 1:
                continue
            u = next(iter(same))
            roles = pentagon_roles(*p[:5])
            names = tuple(r for r, s0 in roles.items() if u in s0)
            profile = (sum(r in long_roles for r in names), sum(r in short_roles for r in names))
            profiles[profile] += 1
        print(f"  {cl} singleton role profile (long,short) = {dict(profiles)}")

    gauge = scalar_gauge_audit(nonunit_fb)
    print("\ngauge audit")
    for k, v in gauge.items():
        print(" ", k, "=", v)

    print("\nattackability verdict")
    print("  raw global nonlinear solve: REJECT (1881 entries / 76185 scalar equations)")
    print("  layered solve: PASS TO NEXT STAGE")
    print("  reason: B,C need only gauge-fixable scalar seeds at block level; D starts with local 2x2 quadratic blocks;")
    print("          E and F blocks are exposed by linear singleton pentagons once lower layers are fixed.")
    print("  remaining hard test: solve the D-layer branch structure and check the 4-noninvertible pentagons.")


if __name__ == "__main__":
    main()
