"""First exact extension of an epsilon=-1 scalar branch through the D layer.

This does not solve categorifiability. It freezes one concrete sign-valued
A/B/C scalar solution, installs Pauli/Clifford representatives on the 24
stabilizer D seeds, verifies their local pentagons, and proves that each of the
remaining 48 D blocks has a one-dimensional local intertwiner space with an
invertible representative.
"""
from __future__ import annotations

from collections import Counter, defaultdict

import sympy as sp

from r22_scale_audit import ONE, M, f_class, pentagon_blocks, layer_spec, pentagon_deps
from r22_scalar_audit import build_scalar_system
from r22_local_associator import pentagon
from r22_d_layer_probe import d_block_set, singleton_d_cases


def gf2_sign_solution():
    keys, idx, A, _ = build_scalar_system()
    n = len(keys)
    rows = []
    for i in range(A.rows):
        bits = 0
        for j in range(A.cols):
            if int(A[i, j]) & 1:
                bits |= 1 << j
        rows.append([bits, 0])
    # Force epsilon_X=-1; epsilon_Y then follows from scalar pentagons.
    rows.append([1 << idx[("h", "X", "h", "X")], 1])

    r = 0
    pivots = []
    for c in range(n):
        p = next((i for i in range(r, len(rows)) if (rows[i][0] >> c) & 1), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and ((rows[i][0] >> c) & 1):
                rows[i][0] ^= rows[r][0]
                rows[i][1] ^= rows[r][1]
        pivots.append(c)
        r += 1

    for bits, rhs in rows:
        if bits == 0 and rhs:
            raise RuntimeError("inconsistent GF(2) scalar branch")

    x = 0
    # Set free bits to zero; RREF then gives one concrete representative.
    for i, c in enumerate(pivots):
        if rows[i][1]:
            x |= 1 << c

    assign = {k: (-1 if (x >> i) & 1 else 1) for i, k in enumerate(keys)}
    assert assign[("h", "X", "h", "X")] == -1
    assert assign[("h", "Y", "h", "Y")] == -1

    for i in range(A.rows):
        value = 1
        for j in range(A.cols):
            power = int(A[i, j])
            if power:
                value *= assign[keys[j]] ** power
        assert value == 1
    return assign


PX = sp.Matrix([[0, 1], [1, 0]])
PZ = sp.diag(1, -1)
PY = sp.Matrix([[0, -sp.I], [sp.I, 0]])


def underlying_h_space(key):
    a, b, c, d = key
    if a == "h":
        return (b, c, d), "L"
    if b == "h":
        return (a, c, d), "M"
    if c == "h":
        return (a, b, d), "R"
    raise KeyError(key)


def pauli_seed_assignment(chirality=None):
    if chirality is None:
        chirality = {(a, b, d): 1 for a in M for b in M for d in M}
    D = d_block_set()
    H = {k for k in D if "h" in k[:3]}
    assert len(H) == 24
    out = {}
    for key in H:
        u, pos = underlying_h_space(key)
        out[key] = {"L": PX, "M": PZ, "R": chirality[u] * PY}[pos]
    return out


def substitute_registry(registry, scalar, known_d, target=None):
    sub = {}
    target_symbols = []
    for (meta, sym) in registry.symbols.items():
        key, row, col = meta
        cl = f_class(key)
        if cl in "ABC":
            sub[sym] = scalar[key]
        elif cl == "D":
            if key in known_d:
                sub[sym] = known_d[key][row, col]
            elif key == target:
                target_symbols.append(sym)
            else:
                raise RuntimeError(("unexpected unknown D block", key, target))
        else:
            raise RuntimeError((key, cl))
    return sub, sorted(set(target_symbols), key=str)


def verify_seed_pentagons(scalar, seeds):
    for p, target in singleton_d_cases():
        registry, _mats, diff = pentagon(dict(zip("abcd", p[:4])), p[4])
        sub, _ = substitute_registry(registry, scalar, {target: seeds[target]})
        value = sp.simplify(diff.subs(sub))
        assert value == sp.zeros(*value.shape)

    for m in M:
        for n in M:
            for out in M:
                cases = [
                    ({"a": "h", "b": m, "c": "h", "d": n}, out),
                    ({"a": "h", "b": m, "c": n, "d": "h"}, out),
                    ({"a": m, "b": "h", "c": n, "d": "h"}, out),
                ]
                for labels, total in cases:
                    registry, _mats, diff = pentagon(labels, total)
                    sub, _ = substitute_registry(registry, scalar, seeds)
                    value = sp.simplify(diff.subs(sub))
                    assert value == sp.zeros(*value.shape)


def propagate_projective_d(scalar, seeds):
    D = d_block_set()
    H = set(seeds)
    by = defaultdict(list)
    for p in pentagon_blocks():
        if ONE in p[:4] or not layer_spec("D", p):
            continue
        deps = pentagon_deps(*p[:5]) & D
        rem = deps - H
        if len(rem) == 1:
            by[next(iter(rem))].append(p)
    assert set(by) == D - H

    forms = {}
    nullity = Counter()
    invertible = Counter()

    for target, ps in by.items():
        equations = []
        symbols = set()
        symbol_pos = {}
        for p in ps:
            registry, _mats, diff = pentagon(dict(zip("abcd", p[:4])), p[4])
            sub, tv = substitute_registry(registry, scalar, seeds, target)
            symbols.update(tv)
            for (meta, sym) in registry.symbols.items():
                key, row, col = meta
                if key == target:
                    symbol_pos[sym] = (row, col)
            value = diff.subs(sub)
            equations.extend(sp.expand(e) for e in value if e != 0)

        symbols = sorted(symbols, key=str)
        assert len(symbols) == 4
        A, b = sp.linear_eq_to_matrix(equations, symbols)
        assert b == sp.zeros(len(equations), 1)
        ns = A.nullspace()
        nullity[len(ns)] += 1
        assert len(ns) == 1

        T = sp.zeros(2)
        for sym, val in zip(symbols, ns[0]):
            T[symbol_pos[sym]] = sp.simplify(val)
        forms[target] = T
        invertible[sp.simplify(T.det()) != 0] += 1

    assert nullity == Counter({1: 48})
    assert invertible == Counter({True: 48})
    return forms


def main():
    scalar = gf2_sign_solution()
    print("scalar minus signs", sum(v == -1 for v in scalar.values()))
    print("epsilon_X", scalar[("h", "X", "h", "X")])
    print("epsilon_Y", scalar[("h", "Y", "h", "Y")])

    seeds = pauli_seed_assignment()
    verify_seed_pentagons(scalar, seeds)
    print("24 Pauli stabilizer seeds and pair pentagons: PASS")

    forms = propagate_projective_d(scalar, seeds)
    print("remaining D projective intertwiners", len(forms))
    print("all nullity=1 and invertible: PASS")


if __name__ == "__main__":
    main()
