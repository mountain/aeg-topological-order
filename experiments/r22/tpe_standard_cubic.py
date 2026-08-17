"""Standard cubic triangular-prism subsystem for the R(2,2) X-sector.

This file turns the exact local matrix-unit algebra from tpe_local_algebra.py
into the structural cubic system described by the standard-prism TPE
localization.

Notation
--------
Let I_a = tau_a be the normalized I-shaped matrix-unit basis of
A=End(X tensor X).  Write the rotated H-shaped basis element as

    H_a = sum_r d_{q(r)} U[r,a] I_r,

where r=(q,i,j) runs through the ten matrix units and the factor d_q is the
resolution-of-identity normalization.  Then the triangular-prism trace has the
cubic form

    tr(I_a I_b I_c)
      = sum_q d_q sum_{i,j,k}
          U[(q,i,j),a] U[(q,j,k),b] U[(q,k,i),c].

Up to transpose/orientation convention for the SFT indices, this is the exact
matrix-unit contraction underlying the n^3 standard-prism equations.  The
cycle orientation does not affect the main negative result below.

NEGATIVE COMPUTATIONAL BENCHMARK
--------------------------------
The standard X-only cubic subsystem has an explicit invertible fake solution:

    U[r,a] = delta[r,a] / d_{q(r)}.

Indeed the corresponding H_a equals I_a exactly, so every prism trace identity
is tautological.  The script verifies all 10^3 ordered equations symbolically
over Q(sqrt(6)).

Thus equation count (340 C3-orbits for 100 variables) is misleading: the
standard shell alone cannot obstruct R(2,2).  A useful localization must add
constraints that remember the *geometric 90-degree rotation*, such as
unit-channel/identity Fourier normalization or a next shell of prism equations
coupling the X-sector to other object labels.

AUDIT BOUNDARY
--------------
The exact tensor contraction follows from the published resolution-of-identity
normalization and the standard-prism description.  Before using a nontrivial
Groebner inconsistency as a theorem, the remaining orientation/pivotal
conventions must still be checked against a known category.  The explicit
diagonal fake solution is insensitive to transpose conventions and therefore
is a robust negative result for the isolated standard shell.
"""

from __future__ import annotations

from itertools import product
from typing import Dict, Iterable, Tuple

import sympy as sp

from tpe_local_algebra import BASIS, SIMPLE_DIMS, cyclic_orbits, triple_trace

N = len(BASIS)
assert N == 10


def row(simple: str, i: int, j: int) -> int:
    return BASIS.index((simple, i, j))


def block_indices(simple: str) -> Tuple[int, ...]:
    return tuple(index for index, (q, _, _) in enumerate(BASIS) if q == simple)


def cubic_rhs(U: sp.Matrix, a: int, b: int, c: int) -> sp.Expr:
    total = sp.Integer(0)
    for q in ("1", "h", "X", "Y"):
        indices = block_indices(q)
        # Recover the multiplicity m_q from the matrix-unit block size m_q^2.
        multiplicity = int(sp.sqrt(len(indices)))
        assert multiplicity * multiplicity == len(indices)
        for i, j, k in product(range(multiplicity), repeat=3):
            total += (
                SIMPLE_DIMS[q]
                * U[row(q, i, j), a]
                * U[row(q, j, k), b]
                * U[row(q, k, i), c]
            )
    return sp.expand(total)


def cubic_equation(U: sp.Matrix, a: int, b: int, c: int) -> sp.Expr:
    lhs = triple_trace(BASIS[a], BASIS[b], BASIS[c])
    return sp.factor(sp.expand(cubic_rhs(U, a, b, c) - lhs))


def symbolic_matrix() -> sp.Matrix:
    variables = sp.symbols(f"u0:{N*N}")
    return sp.Matrix(N, N, variables)


def diagonal_fake_solution() -> sp.Matrix:
    U = sp.zeros(N)
    for index, (q, _, _) in enumerate(BASIS):
        U[index, index] = sp.simplify(1 / SIMPLE_DIMS[q])
    assert sp.simplify(U.det()) != 0
    return U


def verify_diagonal_fake_solution() -> None:
    U = diagonal_fake_solution()
    for a, b, c in product(range(N), repeat=3):
        assert sp.simplify(cubic_equation(U, a, b, c)) == 0


def representative_equations(U: sp.Matrix) -> Tuple[Tuple[Tuple[int, int, int], sp.Expr], ...]:
    """One equation per cyclic orbit; exact orbit count is 340."""
    out = []
    for orbit, _ in cyclic_orbits():
        representative = min(orbit)
        eq = cubic_equation(U, *representative)
        # Cyclic trace and cyclic matrix contraction should agree exactly.
        for triple in orbit:
            assert sp.simplify(cubic_equation(U, *triple) - eq) == 0
        out.append((representative, eq))
    assert len(out) == 340
    return tuple(out)


def equation_degree_profile() -> Dict[int, int]:
    U = symbolic_matrix()
    profile: Dict[int, int] = {}
    for _, eq in representative_equations(U):
        degree = int(sp.Poly(eq, *list(U)).total_degree())
        profile[degree] = profile.get(degree, 0) + 1
    # Nonzero known-side equations contain a cubic term plus a constant; the
    # total polynomial degree remains 3 for all representatives.
    assert profile == {3: 340}
    return profile


def main() -> None:
    print("R(2,2) standard X-only TPE cubic subsystem")
    print("  variables:", N * N)
    print("  ordered equations:", N ** 3)
    print("  C3 representatives:", len(cyclic_orbits()))
    print("  degree profile:", equation_degree_profile())

    verify_diagonal_fake_solution()
    U = diagonal_fake_solution()
    print("\nexplicit invertible fake solution")
    print("  det(U) =", sp.factor(U.det()))
    print("  all 1000 ordered cubic equations: PASS")
    print("\nNEGATIVE BENCHMARK:")
    print("  the isolated standard shell cannot decide categorifiability")
    print("  next shell must encode genuine 90-degree Fourier geometry")


if __name__ == "__main__":
    main()
