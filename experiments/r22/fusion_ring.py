"""Exact and numerical reconnaissance for the open fusion ring R(2,2).

CLASSICAL: the fusion rules are Meng--Yu's self-dual V4-quadratic rules
R(m,n), specialized to m=n=2.
COMPUTATIONAL-CLAIM: this script verifies associativity, computes exact FP
data, enumerates based-ring automorphisms, and measures the raw associator
block profile.
REFORMULATION: isolate the involution tau swapping X<->Y while fixing V4 as
the candidate symmetry whose categorical lift would turn the open rank-6
problem into an order-8 near-group problem after equivariantization.

NumPy stores and inspects the finite integer fusion tensor and is used only for
floating-point spectral reconnaissance. SymPy is the source of truth for
characteristic polynomials and algebraic-number identities.
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations, product
from typing import Dict, Tuple

import numpy as np
import sympy as sp

LABELS = ("1", "g", "h", "k", "X", "Y")
UNIT = "1"
INV = ("1", "g", "h", "k")
NONINV = ("X", "Y")
I = {x: i for i, x in enumerate(LABELS)}


def build_fusion_tensor() -> np.ndarray:
    N = np.zeros((6, 6, 6), dtype=np.int64)
    v4 = {
        ("1", "1"): "1", ("1", "g"): "g", ("1", "h"): "h", ("1", "k"): "k",
        ("g", "1"): "g", ("h", "1"): "h", ("k", "1"): "k",
        ("g", "g"): "1", ("h", "h"): "1", ("k", "k"): "1",
        ("g", "h"): "k", ("h", "g"): "k",
        ("g", "k"): "h", ("k", "g"): "h",
        ("h", "k"): "g", ("k", "h"): "g",
    }
    for a, b in product(INV, repeat=2):
        N[I[a], I[b], I[v4[a, b]]] = 1

    def act(a: str, z: str) -> str:
        if a in ("1", "h"):
            return z
        return "Y" if z == "X" else "X"

    for a in INV:
        for z in NONINV:
            out = act(a, z)
            N[I[a], I[z], I[out]] = 1
            N[I[z], I[a], I[out]] = 1

    # X^2 = Y^2 = 1 + h + 2X + 2Y.
    for z in NONINV:
        for out, mult in (("1", 1), ("h", 1), ("X", 2), ("Y", 2)):
            N[I[z], I[z], I[out]] = mult

    # XY = YX = g + k + 2X + 2Y.
    for a, b in (("X", "Y"), ("Y", "X")):
        for out, mult in (("g", 1), ("k", 1), ("X", 2), ("Y", 2)):
            N[I[a], I[b], I[out]] = mult
    return N


N = build_fusion_tensor()


def fusion(a: str, b: str) -> Dict[str, int]:
    return {c: int(N[I[a], I[b], I[c]]) for c in LABELS if N[I[a], I[b], I[c]]}


def verify_associativity() -> None:
    for a, b, c, d in product(range(6), repeat=4):
        lhs = sum(int(N[a, b, e]) * int(N[e, c, d]) for e in range(6))
        rhs = sum(int(N[b, c, f]) * int(N[a, f, d]) for f in range(6))
        assert lhs == rhs, (a, b, c, d, lhs, rhs)


def fusion_matrix(a: str) -> sp.Matrix:
    ia = I[a]
    return sp.Matrix([[int(N[ia, j, k]) for k in range(6)] for j in range(6)])


def exact_fp_data() -> Dict[str, sp.Expr]:
    lam = sp.Symbol("lambda")
    charpoly = sp.factor(fusion_matrix("X").charpoly(lam).as_expr())
    expected = lam**2 * (lam**2 - 2) * (lam**2 - 4 * lam - 2)
    assert sp.expand(charpoly - expected) == 0

    d = sp.Integer(2) + sp.sqrt(6)
    assert sp.expand(d**2 - 4 * d - 2) == 0
    global_dim = sp.simplify(4 + 2 * d**2)
    assert global_dim == 24 + 8 * sp.sqrt(6)

    # Conditional Z2 equivariantization: the free orbit {X,Y} becomes rho.
    D = sp.expand(2 * d)
    equiv_dim = sp.expand(2 * global_dim)
    assert D == 4 + 2 * sp.sqrt(6)
    assert sp.expand(D**2 - 8 * D - 8) == 0
    assert sp.expand(equiv_dim - (8 + D**2)) == 0
    return {
        "charpoly_X": charpoly,
        "FPdim_X": d,
        "global_dimension": global_dim,
        "lifted_noninvertible_dimension": D,
        "equivariantized_global_dimension": equiv_dim,
    }


def numerical_probe() -> Dict[str, float]:
    vals = np.linalg.eigvals(np.asarray(fusion_matrix("X"), dtype=float))
    rho = float(np.max(np.abs(vals)))
    exact = float(sp.N(2 + sp.sqrt(6), 16))
    assert abs(rho - exact) < 1e-12
    return {"spectral_radius_X": rho, "exact_float": exact}


def is_based_ring_automorphism(perm: Tuple[int, ...]) -> bool:
    if perm[I[UNIT]] != I[UNIT]:
        return False
    return all(
        int(N[a, b, c]) == int(N[perm[a], perm[b], perm[c]])
        for a, b, c in product(range(6), repeat=3)
    )


def based_ring_automorphisms() -> Tuple[Tuple[int, ...], ...]:
    autos = tuple(p for p in permutations(range(6)) if is_based_ring_automorphism(p))
    assert len(autos) == 4
    return autos


def permutation_as_map(perm: Tuple[int, ...]) -> Dict[str, str]:
    return {LABELS[i]: LABELS[perm[i]] for i in range(6)}


def tau_permutation() -> Tuple[int, ...]:
    target = {"1": "1", "g": "g", "h": "h", "k": "k", "X": "Y", "Y": "X"}
    for p in based_ring_automorphisms():
        if permutation_as_map(p) == target:
            return p
    raise AssertionError("tau not found")


def associator_block_dimension(a: int, b: int, c: int, d: int) -> int:
    source = sum(int(N[a, b, e]) * int(N[e, c, d]) for e in range(6))
    target = sum(int(N[b, c, f]) * int(N[a, f, d]) for f in range(6))
    assert source == target
    return source


def associator_profile(strict_unit: bool = False) -> Dict[str, object]:
    dist: Counter[int] = Counter()
    entries = blocks = 0
    for a, b, c, d in product(range(6), repeat=4):
        if strict_unit and I[UNIT] in (a, b, c):
            continue
        n = associator_block_dimension(a, b, c, d)
        if n:
            blocks += 1
            dist[n] += 1
            entries += n * n
    return {"blocks": blocks, "raw_matrix_entries": entries, "dimension_distribution": dict(dist)}


def vertex_gauge_profile(strict_unit: bool = False) -> Dict[str, object]:
    dist: Counter[int] = Counter()
    parameters = spaces = 0
    for a, b, c in product(range(6), repeat=3):
        if strict_unit and I[UNIT] in (a, b):
            continue
        n = int(N[a, b, c])
        if n:
            spaces += 1
            dist[n] += 1
            parameters += n * n
    return {"fusion_spaces": spaces, "GL_raw_parameters": parameters, "multiplicity_distribution": dict(dist)}


def tau_orbit_profile() -> Dict[str, object]:
    """Count strict-unit associator blocks modulo tau, conditionally on a lift.

    This is only a ring-level orbit count. It must not be used as a categorical
    quotient unless a monoidal lift of tau has been constructed or forced.
    """
    tau = tau_permutation()
    seen = set()
    orbit_sizes: Counter[int] = Counter()
    fixed_dims: Counter[int] = Counter()
    representative_entries = representatives = 0
    for a, b, c, d in product(range(6), repeat=4):
        if I[UNIT] in (a, b, c):
            continue
        n = associator_block_dimension(a, b, c, d)
        if not n:
            continue
        key = (a, b, c, d)
        if key in seen:
            continue
        image = tuple(tau[x] for x in key)
        orbit = {key, image}
        seen.update(orbit)
        orbit_sizes[len(orbit)] += 1
        representatives += 1
        representative_entries += n * n
        if len(orbit) == 1:
            fixed_dims[n] += 1

    assert fixed_dims == Counter({1: 27})
    assert representatives == 150
    assert representative_entries == 954
    return {
        "block_orbit_sizes": dict(orbit_sizes),
        "representative_blocks": representatives,
        "representative_raw_entries": representative_entries,
        "fixed_block_dimensions": dict(fixed_dims),
    }


def main() -> None:
    verify_associativity()
    print("R(2,2) fusion ring: associative PASS")
    print("X^2 =", fusion("X", "X"))
    print("XY  =", fusion("X", "Y"))
    print("\nexact FP data")
    for key, value in exact_fp_data().items():
        print(f"  {key}: {value}")
    print("\nnumerical reconnaissance")
    for key, value in numerical_probe().items():
        print(f"  {key}: {value:.15g}")
    print("\nbased-ring automorphisms")
    for p in based_ring_automorphisms():
        print(" ", permutation_as_map(p))
    print("\nassociator profile")
    print("  all:", associator_profile(False))
    print("  strict unit:", associator_profile(True))
    print("  vertex gauge all:", vertex_gauge_profile(False))
    print("  vertex gauge strict unit:", vertex_gauge_profile(True))
    print("  conditional tau orbit profile:", tau_orbit_profile())


if __name__ == "__main__":
    main()
