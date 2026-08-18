from __future__ import annotations

import time
from collections import Counter
from functools import lru_cache

import sympy as sp

from r22_scale_audit import ONE, OBJECTS, N, f_blocks, f_class, pentagon_blocks, layer_spec
from r22_local_associator import (
    P0, P1, P2, P3, P4, enum_states, rotate_right, root_label,
    leafsets_state, subtree_at,
)

# Linear expression represented as (constant, {variable_id: integer coefficient}).
ZERO = (0, {})
ONE_L = (1, {})


def var(v):
    return (0, {v: 1})


def add(x, y):
    c = x[0] + y[0]
    d = dict(x[1])
    for k, v in y[1].items():
        d[k] = d.get(k, 0) + v
        if d[k] == 0:
            del d[k]
    return c, d


def mul(x, y):
    c1, d1 = x
    c2, d2 = y
    if d1 and d2:
        raise RuntimeError("nonlinear F-layer product")
    d = {}
    if c1:
        for k, v in d2.items():
            d[k] = d.get(k, 0) + c1 * v
    if c2:
        for k, v in d1.items():
            d[k] = d.get(k, 0) + c2 * v
    return c1 * c2, d


def matmul(A, B):
    nr = len(A)
    nk = len(B)
    nc = len(B[0])
    C = [[ZERO for _ in range(nc)] for _ in range(nr)]
    for i in range(nr):
        for k in range(nk):
            if A[i][k] == ZERO:
                continue
            for j in range(nc):
                if B[k][j] == ZERO:
                    continue
                C[i][j] = add(C[i][j], mul(A[i][k], B[k][j]))
    return C


def matsub(A, B):
    return [
        [
            add(A[i][j], (-B[i][j][0], {k: -v for k, v in B[i][j][1].items()}))
            for j in range(len(A[0]))
        ]
        for i in range(len(A))
    ]


Finfo = {
    (a, b, c, d): dim
    for a, b, c, d, dim in f_blocks()
    if ONE not in (a, b, c) and f_class((a, b, c, d)) == "F"
}

var_ids = {}
rev = []
for key, dim in sorted(Finfo.items()):
    for r in range(dim):
        for c in range(dim):
            var_ids[(key, r, c)] = len(rev)
            rev.append((key, r, c))


@lru_cache(None)
def block_bases(key):
    a, b, c, d = key
    src = []
    tgt = []
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


def coeff(a, b, c, d, e, alpha, beta, f, mu, nu):
    key = (a, b, c, d)
    src, tgt = block_bases(key)
    ci = src.index((e, alpha, beta))
    ri = tgt.index((f, mu, nu))
    if key in Finfo:
        return var(var_ids[(key, ri, ci)])
    # Reconnaissance branch: all lower A/B/C scalar data and D/E transports
    # are the compatible identity representatives.
    return ONE_L if ri == ci else ZERO


def leaves(node):
    if isinstance(node, str):
        return frozenset([node])
    return leaves(node[0]) | leaves(node[1])


def reassoc(source, path, total, leaf_labels):
    target = rotate_right(source, path)

    def sk(st):
        return tuple(sorted(st.items()))

    sb = sorted(enum_states(source, leaf_labels, total), key=sk)
    tb = sorted(enum_states(target, leaf_labels, total), key=sk)
    mat = [[ZERO for _ in sb] for _ in tb]

    pa = path + ("L", "L")
    pb = path + ("L", "R")
    pc = path + ("R",)
    pold = path + ("L",)
    pout = path
    pnew = path + ("R",)
    local = leaves(subtree_at(source, path))

    for j, ss in enumerate(sb):
        a = root_label(source, ss, leaf_labels, pa)
        b = root_label(source, ss, leaf_labels, pb)
        c = root_label(source, ss, leaf_labels, pc)
        e, alpha = ss[pold]
        d, beta = ss[pout]
        ssets = leafsets_state(source, ss)

        for i, ts in enumerate(tb):
            tsets = leafsets_state(target, ts)
            common = ssets.keys() & tsets.keys()
            if any(ssets[x] != tsets[x] for x in common if x != local):
                continue
            f, mu = ts[pnew]
            dd, nu = ts[pout]
            if dd != d:
                continue
            mat[i][j] = coeff(a, b, c, d, e, alpha, beta, f, mu, nu)

    return target, mat


def pent(labels, total):
    _, m01 = reassoc(P0, ("L",), total, labels)
    _, m12 = reassoc(P1, (), total, labels)
    _, m23 = reassoc(P2, ("R",), total, labels)
    _, m04 = reassoc(P0, (), total, labels)
    _, m43 = reassoc(P4, (), total, labels)
    return matsub(matmul(m23, matmul(m12, m01)), matmul(m43, m04))


def mod_rank(rows, p=1000003):
    basis = {}
    for rr in rows:
        r = {j: v % p for j, v in rr.items() if v % p}
        while r:
            q = max(r)
            if q not in basis:
                inv = pow(r[q], p - 2, p)
                r = {j: (v * inv) % p for j, v in r.items() if (v * inv) % p}
                basis[q] = r
                break
            fac = r[q]
            b = basis[q]
            for j, v in b.items():
                nv = (r.get(j, 0) - fac * v) % p
                if nv:
                    r[j] = nv
                else:
                    r.pop(j, None)
    return len(basis), basis


def main():
    t = time.time()
    rows = []
    cases = 0
    constants = []

    for p in pentagon_blocks():
        if ONE in p[:4] or not layer_spec("F", p):
            continue
        cases += 1
        D = pent(dict(zip("abcd", p[:4])), p[4])
        for row in D:
            for c, d in row:
                if c:
                    constants.append((p, c, d))
                if d:
                    rows.append(d)

    print(
        "Fvars", len(rev), "cases", cases, "rows", len(rows),
        "constant failures", len(constants), "build_sec", round(time.time() - t, 3)
    )
    print("support", Counter(len(r) for r in rows), "incident", len(set().union(*(set(r) for r in rows))))
    assert not constants

    for prime in (1000003, 1000033):
        t0 = time.time()
        rank, _ = mod_rank(rows, prime)
        print("rank_mod", prime, rank, "nullity", len(rev) - rank, "sec", round(time.time() - t0, 3))
        assert rank == 1167

    # Every equation is xi=xj on this lower trivial branch. Contract those
    # equalities and inspect the induced generic F blocks exactly.
    parent = list(range(len(rev)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)
        if a != b:
            parent[a] = b

    for r in rows:
        assert len(r) == 2 and sorted(r.values()) == [-1, 1]
        i, j = r.keys()
        union(i, j)

    comps = Counter(find(i) for i in range(len(rev)))
    print(
        "entry-equivalence components", len(comps),
        "size_distribution", Counter(comps.values())
    )
    assert len(comps) == 145
    assert Counter(comps.values()) == Counter({8: 128, 16: 16, 32: 1})

    root_symbol = {r: sp.Symbol(f"z{k}") for k, r in enumerate(sorted(comps))}
    ten_blocks = 0
    for key, dim in sorted(Finfo.items()):
        if dim != 10:
            continue
        ten_blocks += 1
        M = sp.zeros(dim)
        for i in range(dim):
            for j in range(dim):
                M[i, j] = root_symbol[find(var_ids[(key, i, j)])]
        # Exact rank defect: the 1- and h-intermediate paths are identified.
        assert M.row(0) == M.row(1)
        assert M.col(0) == M.col(1)
    assert ten_blocks == 8
    print("10x10 exact rank defect: rows 0,1 and columns 0,1 are identified in all 8 blocks")


if __name__ == "__main__":
    main()
