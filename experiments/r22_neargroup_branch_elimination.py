"""Eliminate two of the four conditional near-group lift branches for R(2,2).

Mathematical input (recorded with exact sources in the companion note):

1. Schopieray (arXiv:2208.07319, Thm. 1.1): the near-group ring
   R(C2^3, 8) is not categorifiable.
2. Rowell--Solomon--Zhang (arXiv:2305.09108): for every one of the four
   C2 x C4 + 8 near-group categories, the invertibles a_g in the Drinfeld
   center have twist <g,g>, with the tabulated bicharacters m=+/-1.
   Hence among the three nontrivial order-two elements, (0,2) is the unique
   boson while (1,0),(1,2) are fermions.
3. Meng--Yu (arXiv:2608.06064, Cor. 5.8): de-equivariantizing *any*
   C2 x C4 + 8 near-group category by Rep(C2) gives a rank-six category
   with Grothendieck ring R'(2).

Therefore, under the conditional swap-lift proposition, the C2^3 and
C4 x C2 branches cannot produce R(2,2).  The only remaining extension
GROUP TYPES are D8 and Q8.

This file machine-checks only the finite group/bicharacter arithmetic.  It does
not replace the cited categorical theorems.
"""

from __future__ import annotations

from typing import Dict, Tuple

OrderTwo = Tuple[int, int]


def self_pairing_c2xc4(g: OrderTwo, m: int) -> complex:
    """The Table-3 bicharacter diagonal for C2 x C4, m in {+1,-1}."""
    x, y = g
    # exp(2 pi i x^2 / 2) * exp(2 pi i m y^2 / 4).
    # We keep exact +/-1 arithmetic on the order-two subgroup.
    first = -1 if x & 1 else 1
    second = -1 if ((m * (y * y // 4)) & 1) else 1
    return first * second


def c2xc4_order_two_twists(m: int) -> Dict[OrderTwo, int]:
    assert m in (-1, 1)
    elements = ((1, 0), (0, 2), (1, 2))
    return {g: int(self_pairing_c2xc4(g, m)) for g in elements}


def unique_nontrivial_boson() -> OrderTwo:
    for m in (-1, 1):
        twists = c2xc4_order_two_twists(m)
        bosons = [g for g, theta in twists.items() if theta == 1]
        assert bosons == [(0, 2)]
        assert twists[(1, 0)] == -1
        assert twists[(1, 2)] == -1
    return (0, 2)


def conditional_branch_status() -> Dict[str, str]:
    return {
        "C2^3": "ELIMINATED: R(C2^3,8) is not categorifiable (Schopieray Thm 1.1)",
        "C4xC2": (
            "ELIMINATED: unique central order-2 boson gives the unique Rep(C2) "
            "de-equivariantization, whose K0 is R'(2) (Meng--Yu Cor 5.8)"
        ),
        "D8": "OPEN in the pseudo-unitary setting",
        "Q8": "OPEN in the pseudo-unitary setting",
    }


def main() -> None:
    print("C2 x C4 center order-two twists")
    for m in (-1, 1):
        print(" m=", m, c2xc4_order_two_twists(m))
    print("unique boson:", unique_nontrivial_boson())

    print("\nconditional R(2,2) swap-lift branches")
    for group, status in conditional_branch_status().items():
        print(group, status)


if __name__ == "__main__":
    main()
