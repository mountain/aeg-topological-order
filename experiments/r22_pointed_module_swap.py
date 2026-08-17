"""Localize the R(2,2) X<->Y obstruction beyond the pointed-module layer.

The pointed subcategory of a hypothetical categorification is Vec_{V4}^omega.
The two noninvertibles form the transitive two-point module category with
stabilizer H=<h>.  This script studies the module associator and the module
functor swapping the two cosets in a finite sign-cochain model.

Important subtlety:
- restricting all tensorators to +/-1 creates a false obstruction for half of
  the sign representatives;
- allowing fourth roots of unity removes it in every admissible case.

The computation is intended as an exact finite sanity check for the classical
module-category expectation, not as a replacement for the general
classification theorem.

Research conclusion:
    ring swap -> pointed-module swap
but, by the conditional no-lift theorem in note 11,
    pointed-module swap -/-> tensor swap.
Hence any categorification must place the obstruction in the mixed
M x M multiplication/associator coherence.
"""

from __future__ import annotations

from itertools import product
from typing import Dict, List, Sequence, Tuple

import numpy as np

G = ((0, 0), (1, 0), (0, 1), (1, 1))
ZERO = (0, 0)
NZ = tuple(g for g in G if g != ZERO)
Q = (0, 1)  # V4/<h>, where the first coordinate is the coset coordinate.


def add(a, b):
    return (a[0] ^ b[0], a[1] ^ b[1])


def act(g, q: int) -> int:
    return q ^ g[0]


def gf2_rref(A, b=None):
    A = np.array(A, dtype=np.uint8) % 2
    if b is None:
        M = A.copy()
    else:
        b = np.array(b, dtype=np.uint8).reshape(-1, 1) % 2
        M = np.concatenate([A, b], axis=1)

    rows, cols = A.shape
    pivots: List[int] = []
    for col in range(cols):
        candidates = np.where(M[len(pivots):, col] == 1)[0]
        if not len(candidates):
            continue
        pivot_row = len(pivots) + int(candidates[0])
        M[[len(pivots), pivot_row]] = M[[pivot_row, len(pivots)]]
        for r in range(rows):
            if r != len(pivots) and M[r, col]:
                M[r] ^= M[len(pivots)]
        pivots.append(col)
        if len(pivots) == rows:
            break

    inconsistent = False
    if b is not None:
        inconsistent = any(
            not M[r, :cols].any() and M[r, cols]
            for r in range(len(pivots), rows)
        )
    return M, pivots, inconsistent


def gf2_nullspace(A):
    A = np.array(A, dtype=np.uint8) % 2
    R, pivots, _ = gf2_rref(A)
    free = [j for j in range(A.shape[1]) if j not in pivots]
    basis = []
    for f in free:
        x = np.zeros(A.shape[1], dtype=np.uint8)
        x[f] = 1
        for i, p in reversed(list(enumerate(pivots))):
            x[p] = sum(int(R[i, j]) * int(x[j]) for j in free) % 2
        basis.append(x)
    return np.array(basis, dtype=np.uint8), len(pivots)


def gf2_rank(vectors: Sequence[np.ndarray]) -> int:
    if not vectors:
        return 0
    _, pivots, _ = gf2_rref(np.array(vectors, dtype=np.uint8))
    return len(pivots)


def affine_solution(A, b):
    R, pivots, inconsistent = gf2_rref(A, b)
    if inconsistent:
        return None, None
    cols = np.array(A).shape[1]
    particular = np.zeros(cols, dtype=np.uint8)
    for i, p in enumerate(pivots):
        particular[p] = R[i, cols]
    null, _ = gf2_nullspace(A)
    return particular, null


# ----- normalized sign-valued pointed 3-cocycles ------------------------

W_VARS = tuple((a, b, c) for a in NZ for b in NZ for c in NZ)
W_INDEX = {v: i for i, v in enumerate(W_VARS)}
T_VARS = tuple((a, b) for a in NZ for b in NZ)
T_INDEX = {v: i for i, v in enumerate(T_VARS)}


def pointed_cocycle_matrix():
    rows = []
    for a, b, c, d in product(G, repeat=4):
        row = np.zeros(len(W_VARS), dtype=np.uint8)
        terms = (
            (b, c, d),
            (add(a, b), c, d),
            (a, add(b, c), d),
            (a, b, add(c, d)),
            (a, b, c),
        )
        for term in terms:
            if ZERO not in term:
                row[W_INDEX[term]] ^= 1
        rows.append(row)
    return np.array(rows, dtype=np.uint8)


def sign_coboundary_matrix():
    D = np.zeros((len(W_VARS), len(T_VARS)), dtype=np.uint8)
    for triple, row_index in W_INDEX.items():
        a, b, c = triple
        for term in ((b, c), (add(a, b), c), (a, add(b, c)), (a, b)):
            if ZERO not in term:
                D[row_index, T_INDEX[term]] ^= 1
    return D


def sign_cohomology_basis():
    Z_basis, _ = gf2_nullspace(pointed_cocycle_matrix())
    D = sign_coboundary_matrix()

    boundary_basis: List[np.ndarray] = []
    for j in range(D.shape[1]):
        v = D[:, j]
        if gf2_rank(boundary_basis + [v]) > gf2_rank(boundary_basis):
            boundary_basis.append(v)

    quotient_basis: List[np.ndarray] = []
    span = list(boundary_basis)
    for v in Z_basis:
        if gf2_rank(span + [v]) > gf2_rank(span):
            quotient_basis.append(v)
            span.append(v)

    # This is SIGN-cochain cohomology.  It is intentionally not identified
    # with H^3(V4,C^x), because allowing fourth-root coboundaries merges some
    # sign representatives.
    assert len(Z_basis) == 9
    assert len(boundary_basis) == 5
    assert len(quotient_basis) == 4
    return quotient_basis


# ----- two-point module associators -------------------------------------

MU_VARS = tuple((g, h, q) for g in NZ for h in NZ for q in Q)
MU_INDEX = {v: i for i, v in enumerate(MU_VARS)}


def module_equation_matrices():
    mu_rows = []
    w_rows = []
    for g, h, k, q in product(G, G, G, Q):
        mr = np.zeros(len(MU_VARS), dtype=np.uint8)
        # omega(g,h,k) mu(gh,k,q) mu(g,h,k.q)
        # = mu(g,hk,q) mu(h,k,q)
        terms = (
            (add(g, h), k, q),
            (g, h, act(k, q)),
            (g, add(h, k), q),
            (h, k, q),
        )
        for term in terms:
            a, b, _ = term
            if a != ZERO and b != ZERO:
                mr[MU_INDEX[term]] ^= 1

        wr = np.zeros(len(W_VARS), dtype=np.uint8)
        if g != ZERO and h != ZERO and k != ZERO:
            wr[W_INDEX[(g, h, k)]] = 1
        mu_rows.append(mr)
        w_rows.append(wr)
    return np.array(mu_rows), np.array(w_rows)


# ----- module functor swapping the two cosets ---------------------------

C_VARS = tuple((g, q) for g in NZ for q in Q)
C_INDEX = {v: i for i, v in enumerate(C_VARS)}


def swap_equation_matrices_integer():
    """Integer phase equations for c(g,q) in R/Z.

    Module-functor coherence is

      mu(g,h,q) c(g,h.q) c(h,q)
        = c(gh,q) mu(g,h,Tq),

    where T(q)=q+1 swaps the two cosets.

    If mu is sign-valued, multiplying phases by four turns the RHS into 0 or 2
    modulo 4.  Searching c in fourth roots is therefore exact for this finite
    sign model.
    """
    C = []
    M = []
    for g, h, q in product(G, G, Q):
        row = np.zeros(len(C_VARS), dtype=int)
        for term, coefficient in (
            ((g, act(h, q)), 1),
            ((h, q), 1),
            ((add(g, h), q), -1),
        ):
            gg, _ = term
            if gg != ZERO:
                row[C_INDEX[term]] += coefficient

        mu_row = np.zeros(len(MU_VARS), dtype=int)
        for term, coefficient in (
            ((g, h, q ^ 1), 1),
            ((g, h, q), -1),
        ):
            gg, hh, _ = term
            if gg != ZERO and hh != ZERO:
                mu_row[MU_INDEX[term]] += coefficient
        C.append(row)
        M.append(mu_row)
    return np.array(C, dtype=int), np.array(M, dtype=int)


def swap_fourth_root_solution(mu: np.ndarray):
    C, M = swap_equation_matrices_integer()
    rhs = (2 * (M @ mu)) % 4
    for values in product(range(4), repeat=len(C_VARS)):
        y = np.array(values, dtype=int)
        if np.all((C @ y - rhs) % 4 == 0):
            return y
    return None


def exhaustive_sign_model_profile() -> Dict[str, object]:
    quotient_basis = sign_cohomology_basis()
    M_mu, M_w = module_equation_matrices()

    admissible_sign_classes = 0
    module_representatives = 0
    swap_success = 0
    needs_nonreal_fourth_root = 0

    for bits in product((0, 1), repeat=len(quotient_basis)):
        w = np.zeros(len(W_VARS), dtype=np.uint8)
        for bit, vector in zip(bits, quotient_basis):
            if bit:
                w ^= vector

        particular, null = affine_solution(M_mu, (M_w @ w) % 2)
        if particular is None:
            continue
        admissible_sign_classes += 1
        assert len(null) == 5

        for coefficients in product((0, 1), repeat=len(null)):
            mu = particular.copy()
            for bit, vector in zip(coefficients, null):
                if bit:
                    mu ^= vector
            module_representatives += 1

            y = swap_fourth_root_solution(mu)
            assert y is not None
            swap_success += 1
            if any(int(v) % 2 for v in y):
                needs_nonreal_fourth_root += 1

    assert admissible_sign_classes == 8
    assert module_representatives == 8 * 32
    assert swap_success == module_representatives

    return {
        "sign_3cocycle_quotient_classes": 16,
        "admissible_two_point_sign_classes": admissible_sign_classes,
        "sign_module_associator_representatives_tested": module_representatives,
        "swap_module_functor_successes": swap_success,
        "representatives_whose_first_found_swap_uses_plus_minus_i": needs_nonreal_fourth_root,
    }


def main() -> None:
    profile = exhaustive_sign_model_profile()
    for key, value in profile.items():
        print(key, value)
    print("pointed-module swap finite sign/fourth-root audit: PASS")


if __name__ == "__main__":
    main()
