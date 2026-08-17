from __future__ import annotations

from collections import Counter, defaultdict

import sympy as sp

from r22_scale_audit import (
    M,
    ONE,
    f_blocks,
    f_class,
    layer_spec,
    pentagon_blocks,
    pentagon_deps,
)
from r22_local_associator import pentagon


def d_block_set():
    return {
        (a, b, c, d)
        for a, b, c, d, dim in f_blocks()
        if ONE not in (a, b, c) and f_class((a, b, c, d)) == "D"
    }


def singleton_d_cases():
    dset = d_block_set()
    out = []
    for p in pentagon_blocks():
        if ONE in p[:4] or not layer_spec("D", p):
            continue
        deps = pentagon_deps(*p[:5]) & dset
        if len(deps) == 1:
            out.append((p, next(iter(deps))))
    return out


def is_scalar_identity(mat: sp.Matrix) -> bool:
    if mat.rows != mat.cols:
        return False
    lam = mat[0, 0]
    return sp.simplify(mat - lam * sp.eye(mat.rows)) == sp.zeros(mat.rows)


def projective_involution_audit():
    """Verify the 24 first D-layer pentagons are local U^2=lambda I relations."""
    cases = singleton_d_cases()
    assert len(cases) == 24
    role_profile = Counter()
    by_underlying_space = defaultdict(list)

    for p, unknown_key in cases:
        labels = dict(zip("abcd", p[:4]))
        total = p[4]
        registry, mats, _ = pentagon(labels, total)

        unknown_symbols = {
            symbol
            for (key, _row, _col), symbol in registry.symbols.items()
            if key == unknown_key
        }
        containing = [
            i
            for i, mat in enumerate(mats)
            if any(symbol in mat.free_symbols for symbol in unknown_symbols)
        ]
        assert len(containing) == 2
        assert sp.simplify(mats[containing[0]] - mats[containing[1]]) == sp.zeros(2)
        assert all(
            is_scalar_identity(mat)
            for i, mat in enumerate(mats)
            if i not in containing
        )

        long_count = sum(i < 3 for i in containing)
        short_count = sum(i >= 3 for i in containing)
        role_profile[(long_count, short_count)] += 1

        a, b, c, d = unknown_key
        if a == "h":
            underlying = (b, c, d)
            position = "left"
        elif b == "h":
            underlying = (a, c, d)
            position = "middle"
        elif c == "h":
            underlying = (a, b, d)
            position = "right"
        else:
            raise AssertionError(unknown_key)
        by_underlying_space[underlying].append((position, unknown_key))

    assert role_profile == Counter({(2, 0): 16, (0, 2): 8})
    assert len(by_underlying_space) == 8
    assert all(
        {p for p, _ in rows} == {"left", "middle", "right"}
        for rows in by_underlying_space.values()
    )
    return role_profile, by_underlying_space


def epsilon_square_audit(obj: str):
    """The gauge-invariant middle stabilizer scalar epsilon_M satisfies epsilon_M^2=1."""
    assert obj in M
    registry, _mats, diff = pentagon(
        {"a": "h", "b": obj, "c": "h", "d": "h"}, obj
    )
    key = (("h", obj, "h", obj), 0, 0)
    eps = registry.symbols[key]
    expr = sp.factor(diff[0, 0])
    quotient = sp.factor(expr / (eps**2 - 1))
    assert quotient != 0 and sp.simplify(expr - quotient * (eps**2 - 1)) == 0
    return eps, quotient


def pair_relation_probe(m: str, n: str, out: str):
    """Extract which scalar controls pairwise projective commutation.

    For V_{mn}^out, the left/middle and left/right relations are controlled by
    epsilon_m = F^{h m h}_m; the middle/right relation is controlled by
    epsilon_n = F^{h n h}_n.
    """
    assert m in M and n in M and out in M
    cases = [
        ({"a": "h", "b": m, "c": "h", "d": n}, out, ("left", "middle")),
        ({"a": "h", "b": m, "c": n, "d": "h"}, out, ("left", "right")),
        ({"a": m, "b": "h", "c": n, "d": "h"}, out, ("middle", "right")),
    ]
    scalars = []
    for labels, total, pair in cases:
        registry, _mats, _diff = pentagon(labels, total)
        scalar_symbols = []
        for (key, r, c), sym in registry.symbols.items():
            if (
                key[0] == "h"
                and key[2] == "h"
                and key[1] in M
                and key[3] == key[1]
                and r == c == 0
            ):
                scalar_symbols.append((key, sym))
        assert len(scalar_symbols) == 1
        scalars.append((pair, scalar_symbols[0]))
    return scalars


def transport_orbits():
    """Pair-flip graph on the eight multiplicity-two spaces V_{MN}^P."""
    spaces = [(a, b, c) for a in M for b in M for c in M]

    def toggle(x):
        return "Y" if x == "X" else "X"

    adjacency = {}
    for a, b, c in spaces:
        adjacency[(a, b, c)] = {
            (toggle(a), b, toggle(c)),
            (a, toggle(b), toggle(c)),
            (toggle(a), toggle(b), c),
        }

    comps = []
    seen = set()
    for s in spaces:
        if s in seen:
            continue
        stack = [s]
        comp = set()
        while stack:
            u = stack.pop()
            if u in comp:
                continue
            comp.add(u)
            seen.add(u)
            stack.extend(adjacency[u] - comp)
        comps.append(comp)

    assert sorted(map(len, comps)) == [4, 4]
    assert all(
        len({sum(x == "Y" for x in s) % 2 for s in comp}) == 1
        for comp in comps
    )
    return comps


def main():
    role_profile, spaces = projective_involution_audit()
    print("D-layer singleton pentagons:", len(singleton_d_cases()))
    print("role profile (long occurrences, short occurrences):", dict(role_profile))
    print("multiplicity-two fusion spaces:", len(spaces))
    print("each carries three h-position matrices:", all(len(v) == 3 for v in spaces.values()))

    for obj in M:
        eps, quotient = epsilon_square_audit(obj)
        print(
            f"epsilon_{obj} = {eps}; pentagon gives epsilon_{obj}^2=1 "
            f"(nonzero factor {quotient})"
        )

    print("projective commutation probes for V_XX^X:")
    for pair, (key, sym) in pair_relation_probe("X", "X", "X"):
        print(" ", pair, "controlled by", key, "=", sym)
    print("projective commutation probes for V_XY^X:")
    for pair, (key, sym) in pair_relation_probe("X", "Y", "X"):
        print(" ", pair, "controlled by", key, "=", sym)

    comps = transport_orbits()
    print("pair-flip transport orbits among 8 multiplicity spaces:")
    for comp in comps:
        parity = sum(next(iter(comp)).count("Y") for _ in [0]) % 2
        print(" ", sorted(comp), "Y-parity=", parity)

    print("\ninterpretation")
    print("  After scalar normalization, each of the three stabilizer matrices on a 2D fusion space is a projective involution.")
    print("  Pair pentagons make them commute/anticommute with signs epsilon_X, epsilon_Y in {+1,-1}.")
    print("  Combined with r22_scalar_audit.py, epsilon_X=epsilon_Y, so only the commuting and Clifford regimes survive.")


if __name__ == "__main__":
    main()
