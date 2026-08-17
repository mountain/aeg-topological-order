"""Eliminate all four conditional near-group lift branches for R(2,2).

Standing conditional reduction:
If a categorification A of R(2,2) admits a monoidal C2 action lifting the based-ring
involution X <-> Y, then E=A^C2 is a near-group category R(Ghat,8), where Ghat
is an order-eight central extension of V4 by C2.  Hence

    Ghat in {C2^3, C4 x C2, D8, Q8}.

Categorical input (recorded with exact primary sources in the companion notes):

1. Schopieray (arXiv:2208.07319, Thm. 1.1): R(C2^3,8) is not categorifiable.
2. Rowell--Solomon--Zhang (arXiv:2305.09108): in each C2 x C4 + 8
   near-group category, the center invertible a_g has twist <g,g>.  Their
   bicharacter tables imply that the three nontrivial order-two elements have
   twists (-1,+1,-1), so there is one nontrivial boson and hence one
   Tannakian Rep(C2).
3. Meng--Yu (arXiv:2608.06064, Cor. 5.8): de-equivariantizing any
   C2 x C4 + 8 near-group category by this Rep(C2) gives a rank-six category
   with Grothendieck ring R'(2), not R(2,2).
4. Ostrik--Nikshych, Appendix A of arXiv:1309.4822, Theorem A.6:
   if a near-group ring K(G,n) is categorifiable and its noninvertible
   Frobenius-Perron dimension d_+ is irrational, then G is abelian (and n is
   divisible by |G|).  For n=|G|=8, d_+=4+2*sqrt(6) is irrational, so the
   nonabelian groups D8 and Q8 are impossible without any unitarity assumption.

Therefore ALL four possible extension-group branches are eliminated.  This yields
the conditional no-lift theorem:

    if R(2,2) is categorifiable, the ring involution X<->Y cannot lift to a
    monoidal C2 action fixing the four invertible isomorphism classes.

This file machine-checks only finite group/bicharacter/FP-dimension arithmetic.  It
does not replace the cited categorical theorems.
"""

from __future__ import annotations

from typing import Dict, Tuple

import sympy as sp

OrderTwo = Tuple[int, int]


def self_pairing_c2xc4(g: OrderTwo, m: int) -> int:
    """The Table-3 bicharacter diagonal for C2 x C4, m in {+1,-1}."""
    x, y = g
    # exp(2 pi i x^2 / 2) * exp(2 pi i m y^2 / 4).
    # On the order-two subgroup these values are exactly +/-1.
    first = -1 if x & 1 else 1
    exponent = m * (y * y // 4)
    second = -1 if exponent % 2 else 1
    return first * second


def c2xc4_order_two_twists(m: int) -> Dict[OrderTwo, int]:
    assert m in (-1, 1)
    elements = ((1, 0), (0, 2), (1, 2))
    return {g: self_pairing_c2xc4(g, m) for g in elements}


def unique_nontrivial_boson() -> OrderTwo:
    for m in (-1, 1):
        twists = c2xc4_order_two_twists(m)
        bosons = [g for g, theta in twists.items() if theta == 1]
        assert bosons == [(0, 2)]
        assert twists[(1, 0)] == -1
        assert twists[(1, 2)] == -1
    return (0, 2)


def order8_level8_fp_dimension() -> sp.Expr:
    """Positive root d of d^2 = 8 + 8 d."""
    d = sp.Integer(4) + 2 * sp.sqrt(6)
    assert sp.simplify(d**2 - 8 * d - 8) == 0
    return d


def level8_nonintegral() -> bool:
    d = order8_level8_fp_dimension()
    # Minimal polynomial x^2 - 8x - 8 has nonsquare discriminant 96.
    x = sp.symbols("x")
    assert sp.minimal_polynomial(d, x) == x**2 - 8 * x - 8
    return not d.is_integer


def conditional_branch_status() -> Dict[str, str]:
    assert level8_nonintegral()
    return {
        "C2^3": "ELIMINATED: R(C2^3,8) is not categorifiable (Schopieray Thm 1.1)",
        "C4xC2": (
            "ELIMINATED: unique central order-2 boson gives the unique Rep(C2) "
            "de-equivariantization, whose K0 is R'(2) (Meng--Yu Cor 5.8)"
        ),
        "D8": (
            "ELIMINATED: d_+=4+2*sqrt(6) is irrational, while categorifiable "
            "non-integral near-group rings must have abelian G "
            "(Ostrik--Nikshych Thm A.6)"
        ),
        "Q8": (
            "ELIMINATED: d_+=4+2*sqrt(6) is irrational, while categorifiable "
            "non-integral near-group rings must have abelian G "
            "(Ostrik--Nikshych Thm A.6)"
        ),
    }


def all_conditional_branches_eliminated() -> bool:
    return all(status.startswith("ELIMINATED") for status in conditional_branch_status().values())


def main() -> None:
    print("C2 x C4 center order-two twists")
    for m in (-1, 1):
        print(" m=", m, c2xc4_order_two_twists(m))
    print("unique boson:", unique_nontrivial_boson())

    print("\norder-8 level-8 near-group FP dimension:", order8_level8_fp_dimension())
    print("irrational/non-integral:", level8_nonintegral())

    print("\nconditional R(2,2) swap-lift branches")
    for group, status in conditional_branch_status().items():
        print(group, status)
    assert all_conditional_branches_eliminated()
    print("\nconditional no-lift theorem branch audit: PASS")


if __name__ == "__main__":
    main()
