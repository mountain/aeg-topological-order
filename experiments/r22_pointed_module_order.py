"""Classify the order of the R(2,2) pointed-module swap in a finite cochain model.

This refines `r22_pointed_module_swap.py`.

For a hypothetical categorification, let

    P = Vec_{V4}^omega,
    M = <X,Y> ~= V4/<h>.

The pointed-module dual D=Fun_P(M,M) is a pointed category of dimension four.
Its invertible group K fits

    1 -> H^* ~= C2 -> K -> V4/H ~= C2 -> 1,

so K is either V4 or C4.  A module autoequivalence in the nontrivial quotient
coset swaps X and Y.  If one such swap squares to the identity module functor,
K=V4; otherwise every swap has order four and K=C4.

The exhaustive finite audit below shows, for every admissible sign-valued
pointed/module cochain representative:

    order-two swap exists
       iff omega(g,g,g) == omega(k,k,k),  k=gh.

In a pointed C2 subcategory, the restriction class in H^3(C2,C^x) is detected
by the second Frobenius--Schur indicator of its nontrivial invertible object.
Thus Meng--Yu Remark 3.9, nu_2(g)=nu_2(gh), selects precisely the split/V4
module-dual type.

The finite computation is a gauge sanity check for this cohomological statement;
the mathematical argument should be stated invariantly in the companion note.
"""

from __future__ import annotations

from itertools import product
from typing import Dict, Tuple

import numpy as np

from r22_pointed_module_swap import (
    G,
    NZ,
    Q,
    W_INDEX,
    W_VARS,
    C_INDEX,
    C_VARS,
    add,
    act,
    affine_solution,
    module_equation_matrices,
    sign_cohomology_basis,
    swap_equation_matrices_integer,
)


def all_swap_solutions(mu: np.ndarray) -> Tuple[np.ndarray, ...]:
    C, M = swap_equation_matrices_integer()
    rhs = (2 * (M @ mu)) % 4
    out = []
    for values in product(range(4), repeat=len(C_VARS)):
        y = np.array(values, dtype=int)
        if np.all((C @ y - rhs) % 4 == 0):
            out.append(y)
    assert out
    return tuple(out)


def swap_square_tensorator(y: np.ndarray) -> Dict[Tuple[Tuple[int, int], int], int]:
    """Tensorator phases of S^2, represented in Z/4.

    If c(g,q) is the module-functor tensorator of the swap S, then the square
    has tensorator c(g,Tq)c(g,q), since T^2 q=q.
    """
    return {
        (g, q): int((y[C_INDEX[(g, q ^ 1)]] + y[C_INDEX[(g, q)]]) % 4)
        for g in NZ
        for q in Q
    }


def square_is_module_naturally_trivial(y: np.ndarray) -> bool:
    """Check whether S^2 is module-naturally isomorphic to Id.

    A scalar natural transformation eta_q in fourth roots must satisfy

        eta_{g.q} / eta_q = c_{S^2}(g,q).

    Fourth roots suffice because the square tensorator is already Z/4-valued.
    """
    square = swap_square_tensorator(y)
    for z0, z1 in product(range(4), repeat=2):
        z = (z0, z1)
        if all(
            (z[act(g, q)] - z[q] - square[(g, q)]) % 4 == 0
            for g in NZ
            for q in Q
        ):
            return True
    return False


def omega_diagonal_sign(w: np.ndarray, x: Tuple[int, int]) -> int:
    """Sign of omega(x,x,x) for an order-two group element x."""
    return -1 if int(w[W_INDEX[(x, x, x)]]) else 1


def representative_profile() -> Tuple[Dict[str, object], ...]:
    quotient_basis = sign_cohomology_basis()
    M_mu, M_w = module_equation_matrices()

    rows = []
    for bits in product((0, 1), repeat=len(quotient_basis)):
        w = np.zeros(len(W_VARS), dtype=np.uint8)
        for bit, vector in zip(bits, quotient_basis):
            if bit:
                w ^= vector

        particular, null = affine_solution(M_mu, (M_w @ w) % 2)
        if particular is None:
            continue
        assert len(null) == 5

        order2_count = 0
        order4_count = 0
        for coefficients in product((0, 1), repeat=len(null)):
            mu = particular.copy()
            for bit, vector in zip(coefficients, null):
                if bit:
                    mu ^= vector

            has_order2_swap = any(
                square_is_module_naturally_trivial(y)
                for y in all_swap_solutions(mu)
            )
            if has_order2_swap:
                order2_count += 1
            else:
                order4_count += 1

        g = (1, 0)
        h = (0, 1)
        k = (1, 1)
        signs = {
            "g": omega_diagonal_sign(w, g),
            "h": omega_diagonal_sign(w, h),
            "k": omega_diagonal_sign(w, k),
        }
        assert signs["h"] == 1  # exactly the H=<h> admissibility condition here
        assert (order2_count, order4_count) in ((32, 0), (0, 32))
        split = order2_count == 32
        assert split == (signs["g"] == signs["k"])

        rows.append(
            {
                "sign_basis_bits": bits,
                "omega_diagonal_signs": signs,
                "module_associator_representatives": 32,
                "order2_swap_representatives": order2_count,
                "order4_only_representatives": order4_count,
                "module_dual_group": "V4" if split else "C4",
            }
        )

    assert len(rows) == 8
    assert sum(row["order2_swap_representatives"] for row in rows) == 128
    assert sum(row["order4_only_representatives"] for row in rows) == 128
    return tuple(rows)


def meng_yu_indicator_filter() -> Tuple[Dict[str, object], ...]:
    """Apply only the invariant equality nu_2(g)=nu_2(k) from Meng--Yu.

    In the pointed order-two subcategories, nu_2(x) detects the restriction
    class of omega to <x>, represented here by omega(x,x,x)=+/-1.
    """
    kept = tuple(
        row
        for row in representative_profile()
        if row["omega_diagonal_signs"]["g"] == row["omega_diagonal_signs"]["k"]
    )
    assert len(kept) == 4
    assert all(row["module_dual_group"] == "V4" for row in kept)
    return kept


def main() -> None:
    print("admissible sign-cochain representatives")
    for row in representative_profile():
        print(row)

    print("\nMeng--Yu indicator equality filter")
    for row in meng_yu_indicator_filter():
        print(row)

    print("\nConclusion: every representative compatible with nu2(g)=nu2(gh)")
    print("has an involutive pointed-module swap (module dual group V4).")


if __name__ == "__main__":
    main()
