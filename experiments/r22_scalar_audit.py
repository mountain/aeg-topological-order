"""Exact multiplicative-pentagon audit for the scalar A/B/C layers of R(2,2).

The scalar associators are nonzero C* variables, so one-dimensional pentagons
become monomial equations. Their exponent matrix provides a cheap exact audit
of continuous gauge freedom and discrete components before any large F-symbol
solver is attempted.
"""
from __future__ import annotations

from itertools import product
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

from r22_scale_audit import (
    ONE, OBJECTS, f_blocks, f_class, fuse, N, pentagon_blocks, pentagon_deps
)
from r22_local_associator import pentagon


def build_scalar_system():
    keys = sorted(
        (a, b, c, d)
        for a, b, c, d, dim in f_blocks()
        if ONE not in (a, b, c) and dim == 1 and f_class((a, b, c, d)) in "ABC"
    )
    assert len(keys) == 153
    idx = {k: i for i, k in enumerate(keys)}
    rows = []
    examples = []

    def side_vector(mats, positions, registry):
        v = [0] * len(keys)
        for pos in positions:
            e = sp.factor(mats[pos][0, 0])
            if e == 1:
                continue
            found = False
            for (meta, sym) in registry.symbols.items():
                if sym == e:
                    key = meta[0]
                    if key in idx:
                        v[idx[key]] += 1
                        found = True
                        break
            if not found and e.free_symbols:
                raise RuntimeError((e, e.free_symbols))
        return v

    for p in pentagon_blocks():
        a, b, c, d, z, dim = p
        if dim != 1 or ONE in (a, b, c, d):
            continue
        deps = pentagon_deps(a, b, c, d, z)
        if any(k not in idx for k in deps if ONE not in k[:3]):
            continue
        registry, mats, _ = pentagon(dict(zip("abcd", (a, b, c, d))), z)
        lv = side_vector(mats, (0, 1, 2), registry)
        rv = side_vector(mats, (3, 4), registry)
        row = [x - y for x, y in zip(lv, rv)]
        if any(row):
            rows.append(row)
            examples.append(p)

    A = sp.Matrix(rows)
    assert A.shape == (729, 153)
    return keys, idx, A, examples


def build_scalar_gauge(keys):
    triples = []
    for a, b in product(OBJECTS, repeat=2):
        for c, mult in fuse(a, b).items():
            if a != ONE and b != ONE and mult == 1:
                triples.append((a, b, c))
    gidx = {t: i for i, t in enumerate(triples)}
    G = sp.zeros(len(keys), len(triples))

    def paths(key):
        a, b, c, d = key
        left = [e for e in OBJECTS if N(a, b, e) == 1 and N(e, c, d) == 1]
        right = [f for f in OBJECTS if N(b, c, f) == 1 and N(a, f, d) == 1]
        assert len(left) == len(right) == 1
        return left[0], right[0]

    for i, key in enumerate(keys):
        a, b, c, d = key
        e, f = paths(key)
        for t, s in [
            ((a, b, e), 1),
            ((e, c, d), 1),
            ((b, c, f), -1),
            ((a, f, d), -1),
        ]:
            if t in gidx:
                G[i, gidx[t]] += s
    return triples, G


def torsion_invariants(A):
    S = smith_normal_form(A, domain=ZZ)
    return [
        abs(int(S[i, i]))
        for i in range(min(S.shape))
        if S[i, i] not in (0, 1, -1)
    ]


def epsilon_equality_witness(keys, idx, A, examples):
    """Return an integral two-pentagon witness for epsilon_X/epsilon_Y = 1."""
    target = sp.zeros(len(keys), 1)
    target[idx[("h", "X", "h", "X")]] = 1
    target[idx[("h", "Y", "h", "Y")]] = -1
    _, piv = A.T.rref()
    R = A[list(piv), :]
    coeff = R.T.gauss_jordan_solve(target)[0]
    assert all(x.q == 1 for x in coeff)
    terms = []
    for j, c in enumerate(coeff):
        if c:
            terms.append((int(c), examples[piv[j]]))
    assert len(terms) == 2
    return terms


def main():
    keys, idx, A, examples = build_scalar_system()
    triples, G = build_scalar_gauge(keys)
    assert A * G == sp.zeros(A.rows, G.cols)

    rank = A.rank()
    grank = G.rank()
    tors = torsion_invariants(A)
    print("scalar variables", len(keys))
    print("monomial pentagons", A.rows)
    print("equation rank", rank, "kernel dimension", len(keys) - rank)
    print("gauge variables", len(triples), "effective gauge rank", grank)
    print("continuous quotient dimension", len(keys) - rank - grank)
    print("Smith torsion", tors)
    print("epsilon equality witness", epsilon_equality_witness(keys, idx, A, examples))

    assert (len(keys) - rank - grank) == 0
    assert tors == [2, 2, 2, 2]


if __name__ == "__main__":
    main()
