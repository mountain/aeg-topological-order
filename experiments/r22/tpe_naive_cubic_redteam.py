"""Red-team: why the standard TPE must NOT be coded as naive cubic invariance.

A tempting but incorrect shortcut is to identify the standard triangular-prism
system with invariance of the ordinary product trace under one linear map F:

    tr(a b c) ?= tr(F(a) F(b) F(c)).

On the normalized matrix-unit algebra End(X tensor X), this fake equation has
an explicit invertible diagonal solution, so equation count alone looks
misleadingly encouraging.  More decisively, the shortcut contradicts the
classical geometric behavior of the 90-degree string Fourier transform.

For the unit-channel projection p_1 and d=dim(X), graphical Fourier duality
switches identity and the Jones/unit-channel projection up to dimension:

    F(id) = d p_1,
    F(p_1) = d^{-1} id.

But tr(p_1^3)=1 while

    tr(F(p_1)^3) = d^{-3} tr(id) = d^{-1} != 1,

because tr(id_{X tensor X})=d^2.  Thus ordinary-product cubic invariance cannot
be the published TPE contraction.

This script keeps the false model only as a regression test.  Any future TPE
compiler that collapses the two pictorial products into one ordinary product
must fail this test.
"""

from __future__ import annotations

from itertools import product

import sympy as sp

from tpe_local_algebra import BASIS, SIMPLE_DIMS, triple_trace

D = SIMPLE_DIMS["X"]


def false_fourier_matrix() -> sp.Matrix:
    """An invertible fake solution of the naive same-product cubic equations."""
    U = sp.zeros(len(BASIS))
    for index, (q, _, _) in enumerate(BASIS):
        U[index, index] = sp.simplify(1 / SIMPLE_DIMS[q])
    return U


def false_cubic_rhs(U: sp.Matrix, a: int, b: int, c: int) -> sp.Expr:
    """The tempting but incorrect same-product contraction."""
    total = sp.Integer(0)
    for q in ("1", "h", "X", "Y"):
        m = 1 if q in ("1", "h") else 2
        def row(i: int, j: int) -> int:
            return BASIS.index((q, i, j))
        for i, j, k in product(range(m), repeat=3):
            total += (
                SIMPLE_DIMS[q]
                * U[row(i, j), a]
                * U[row(j, k), b]
                * U[row(k, i), c]
            )
    return sp.simplify(total)


def verify_fake_solution() -> None:
    U = false_fourier_matrix()
    assert sp.simplify(U.det()) != 0
    for a, b, c in product(range(len(BASIS)), repeat=3):
        lhs = triple_trace(BASIS[a], BASIS[b], BASIS[c])
        assert sp.simplify(false_cubic_rhs(U, a, b, c) - lhs) == 0


def verify_fourier_normalization_contradiction() -> None:
    # p_1=tau_(1,0,0) is an idempotent with categorical trace 1.
    p1 = BASIS.index(("1", 0, 0))
    assert triple_trace(BASIS[p1], BASIS[p1], BASIS[p1]) == 1

    trace_identity = sp.expand(D**2)
    rotated_value_under_naive_invariance = sp.simplify(trace_identity / D**3)
    assert rotated_value_under_naive_invariance == sp.simplify(1 / D)
    assert sp.simplify(rotated_value_under_naive_invariance - 1) != 0


def main() -> None:
    verify_fake_solution()
    verify_fourier_normalization_contradiction()
    print("naive same-product cubic model: explicit invertible fake solution PASS")
    print("classical SFT identity/projector normalization contradicts that model PASS")
    print("RESULT: preserve the two pictorial products in the real TPE compiler")


if __name__ == "__main__":
    main()
