"""Exact Fibonacci Levin--Wen plaquette benchmark.

This file tests the next-stage question in the AEG x topological-order program:
does an explicit operation-history / DAG representation provide representation or
verification value beyond the standard categorical plaquette formula?

The implementation uses the already-frozen Fibonacci F-data from the F-stage.
No R-symbols are needed: the Levin--Wen plaquette operator is built entirely
from fusion data, F-symbols, and quantum dimensions.

Conventions
-----------
For the six-index tensor we use

    F^{a b e}_{c d f} := [F^{a b c}_d]_{e f}.

For an n-gon with fixed external legs a_k, old plaquette-edge labels i_k,
new labels i'_k, and inserted loop s, the local matrix element is

    (B_p^s)_{i',i}(a)
      = product_k F^{a_k i_{k-1} i_k}_{s i'_k i'_{k-1}}.

This is the self-dual Fibonacci specialization of the standard Levin--Wen
plaquette formula.

Research labels
---------------
CLASSICAL:
  - Fibonacci fusion grammar and frozen unitary F-data.
  - Levin--Wen plaquette formula and fusion algebra of loop insertions.
REFORMULATION:
  - cyclic local-factor / operation-history representation.
COMPUTATIONAL-CLAIM:
  - exhaustive exact checks and transfer-matrix scaling below.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
from typing import Dict, Iterable, List, Sequence, Tuple

import sympy as sp

ONE = "1"
TAU = "t"
LABELS = (ONE, TAU)

# Frozen F-stage gauge:
# alpha = phi^{-1}, q^2 = alpha, alpha^2 + alpha - 1 = 0.
alpha, q = sp.symbols("alpha q", nonzero=True)


def fuse(a: str, b: str) -> Tuple[str, ...]:
    if a == ONE:
        return (b,)
    if b == ONE:
        return (a,)
    if a == TAU and b == TAU:
        return (ONE, TAU)
    raise ValueError((a, b))


def admissible_f(a: str, b: str, c: str, d: str, e: str, f: str) -> bool:
    return e in fuse(a, b) and d in fuse(e, c) and f in fuse(b, c) and d in fuse(a, f)


def f_symbol(a: str, b: str, c: str, d: str, e: str, f: str) -> sp.Expr:
    """Frozen Fibonacci F^{abc}_d[e,f] in the real symmetric unitary gauge."""
    if not admissible_f(a, b, c, d, e, f):
        return sp.Integer(0)
    if ONE in (a, b, c):
        return sp.Integer(1)
    if (a, b, c) != (TAU, TAU, TAU):
        raise ValueError((a, b, c, d, e, f))
    if d == ONE:
        return sp.Integer(1)
    if d == TAU:
        return {
            (ONE, ONE): alpha,
            (ONE, TAU): q,
            (TAU, ONE): q,
            (TAU, TAU): -alpha,
        }[(e, f)]
    raise ValueError(d)


REDUCER = sp.groebner([q**2 - alpha, alpha**2 + alpha - 1], q, alpha, order="lex")


def zero_mod_f_relations(expr: sp.Expr) -> bool:
    numerator = sp.together(sp.expand(expr)).as_numer_denom()[0]
    remainder = REDUCER.reduce(sp.expand(numerator))[1]
    return sp.factor(remainder) == 0


def admissible_cycle(boundary: Sequence[str], inner: Sequence[str]) -> bool:
    """Vertex constraint: a_k x i_{k-1} -> i_k, cyclically."""
    n = len(boundary)
    return all(inner[k] in fuse(boundary[k], inner[(k - 1) % n]) for k in range(n))


def plaquette_basis(boundary: Sequence[str]) -> List[Tuple[str, ...]]:
    n = len(boundary)
    return [
        inner
        for inner in product(LABELS, repeat=n)
        if admissible_cycle(boundary, inner)
    ]


def local_plaquette_factor(
    external: str,
    old_prev: str,
    old_cur: str,
    inserted: str,
    new_prev: str,
    new_cur: str,
) -> sp.Expr:
    """F^{a old_prev old_cur}_{s new_cur new_prev}.

    Under F^{a b e}_{c d f} := [F^{a b c}_d]_{e f}, this is
    [F^{a,old_prev,s}_{new_cur}]_{old_cur,new_prev}.
    """
    return f_symbol(external, old_prev, inserted, new_cur, old_cur, new_prev)


def plaquette_matrix(
    boundary: Sequence[str], inserted: str
) -> Tuple[List[Tuple[str, ...]], sp.Matrix]:
    """Direct categorical baseline: materialize B_p^s from the local product."""
    basis = plaquette_basis(boundary)
    n = len(boundary)
    matrix = sp.zeros(len(basis))
    for row, new in enumerate(basis):
        for col, old in enumerate(basis):
            coeff = sp.Integer(1)
            for k, external in enumerate(boundary):
                coeff *= local_plaquette_factor(
                    external,
                    old[(k - 1) % n],
                    old[k],
                    inserted,
                    new[(k - 1) % n],
                    new[k],
                )
                if coeff == 0:
                    break
            matrix[row, col] = sp.factor(coeff)
    return basis, matrix


def verify_hexagonal_blocks() -> Dict[str, object]:
    """Exhaust all 2^6 external boundary sectors exactly."""
    dim_hist = Counter()
    nnz_by_dim: Dict[int, set[int]] = {}

    for boundary in product(LABELS, repeat=6):
        basis, b_one = plaquette_matrix(boundary, ONE)
        _, b_tau = plaquette_matrix(boundary, TAU)
        dim = len(basis)
        dim_hist[dim] += 1
        nnz = sum(1 for entry in b_tau if entry != 0)
        nnz_by_dim.setdefault(dim, set()).add(nnz)

        # Vacuum-loop insertion is identity.
        assert b_one == sp.eye(dim)

        # Local loop insertions represent the Fibonacci fusion algebra.
        # tau x tau = 1 + tau.
        assert all(
            zero_mod_f_relations(entry)
            for entry in b_tau * b_tau - b_one - b_tau
        )

        # Levin--Wen smooth-phase projector.
        phi = alpha + 1  # = alpha^{-1} modulo alpha^2 + alpha - 1
        projector = (b_one + phi * b_tau) / (1 + phi**2)
        assert all(
            zero_mod_f_relations(entry)
            for entry in projector * projector - projector
        )

    return {
        "boundary_blocks": 2**6,
        "dimension_histogram": dict(sorted(dim_hist.items())),
        "nnz_by_dimension": {k: sorted(v) for k, v in sorted(nnz_by_dim.items())},
    }


def basis_transfer_matrix() -> sp.Matrix:
    """All-tau external boundary: transitions of one cyclic inner label."""
    C = sp.zeros(2)
    for i, prev in enumerate(LABELS):
        for j, cur in enumerate(LABELS):
            C[i, j] = int(cur in fuse(TAU, prev))
    return C


PAIR_STATES = tuple(product(LABELS, repeat=2))


def entry_transfer_matrix() -> sp.Matrix:
    """All-tau boundary: transitions of (old_i,new_i) pair states.

    A closed length-n walk is exactly one nonzero matrix entry of B_p^tau.
    """
    A = sp.zeros(len(PAIR_STATES))
    for i, (old_prev, new_prev) in enumerate(PAIR_STATES):
        for j, (old_cur, new_cur) in enumerate(PAIR_STATES):
            coeff = local_plaquette_factor(
                TAU, old_prev, old_cur, TAU, new_prev, new_cur
            )
            A[i, j] = int(coeff != 0)
    return A


def all_tau_scaling(n: int) -> Dict[str, object]:
    C = basis_transfer_matrix()
    A = entry_transfer_matrix()
    dim = int(sp.trace(C**n))
    nnz = int(sp.trace(A**n))

    sqrt2 = sp.sqrt(2)
    closed_nnz = sp.expand(
        (-1) ** n + (1 + sqrt2) ** n + (1 - sqrt2) ** n
    )
    assert sp.simplify(nnz - closed_nnz) == 0

    return {
        "n": n,
        "dimension": dim,
        "nnz": nnz,
        "dense_entries": dim * dim,
        "density": float(nnz / (dim * dim)),
        "factor_nodes": n,
    }


def representation_benchmark(ns: Iterable[int] = range(3, 15)) -> List[Dict[str, object]]:
    """Compare materialized matrix size with the cyclic local-factor IR.

    The factorized representation is *not* claimed as AEG-specific: it is
    already visible in the standard Levin--Wen product formula and is a tensor
    network / factor graph with O(n) local nodes.
    """
    return [all_tau_scaling(n) for n in ns]


def verify_transfer_formulas() -> Dict[str, sp.Expr]:
    C = basis_transfer_matrix()
    A = entry_transfer_matrix()
    assert C == sp.Matrix([[0, 1], [1, 1]])
    assert A == sp.Matrix(
        [
            [0, 0, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 0, 1],
            [0, 1, 1, 1],
        ]
    )
    return {
        "basis_charpoly": sp.factor(C.charpoly().as_expr()),
        "entry_charpoly": sp.factor(A.charpoly().as_expr()),
    }


def main() -> None:
    print("hexagonal exhaustive validation")
    summary = verify_hexagonal_blocks()
    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\ntransfer matrices / characteristic polynomials")
    print("C =")
    print(basis_transfer_matrix())
    print("A =")
    print(entry_transfer_matrix())
    for key, value in verify_transfer_formulas().items():
        print(f"{key}: {value}")

    print("\nall-tau n-gon scaling")
    for row in representation_benchmark():
        print(row)


if __name__ == "__main__":
    main()
