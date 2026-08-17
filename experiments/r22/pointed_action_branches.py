"""Two pointed monoidal restriction branches for the R(2,2) involution.

Let P = Vec^omega_{V4}.  Any tensor autoequivalence T whose object action fixes
every pointed simple restricts to the identity group automorphism of V4.  Its
monoidal structure is therefore a normalized C^*-valued 2-cocycle, modulo
monoidal natural isomorphism.  H^2(V4,C^*) ~= C2, so there are exactly two
restriction classes.

This file represents them explicitly:

  eta_0(a,b) = +1,
  eta_1(a,b) = (-1)^(a_1 b_2).

The commutator bicharacter eta(b,a)/eta(a,b) is trivial for eta_0 and
nontrivial for eta_1.  Consequently, for any order-two categorical action
extending T, the group of invertible objects in the equivariantization is:

  - abelian in the trivial H^2 branch;
  - a nonabelian central extension of V4 by C2 in the nontrivial branch,
    hence D8 or Q8.

The precise D8/Q8 choice depends on the action-coherence character; only
nonabelianity is needed by the obstruction argument.

CLASSICAL: classification of identity-on-objects tensor autoequivalences of a
pointed category by H^2(G,C^*).
COMPUTATIONAL-CLAIM: finite commutator / extension checks below.
"""

from __future__ import annotations

from itertools import product
from typing import Dict, Tuple

V4 = tuple(product((0, 1), repeat=2))
ZERO = (0, 0)
Elt = Tuple[int, int]


def add(a: Elt, b: Elt) -> Elt:
    return (a[0] ^ b[0], a[1] ^ b[1])


def eta(branch: int, a: Elt, b: Elt) -> int:
    """Return +/-1 for the canonical representative of an H^2 class."""
    if branch == 0:
        return 1
    if branch == 1:
        return -1 if (a[0] * b[1]) & 1 else 1
    raise ValueError(branch)


def verify_2_cocycle(branch: int) -> None:
    for a, b, c in product(V4, repeat=3):
        assert eta(branch, a, b) * eta(branch, add(a, b), c) == eta(branch, b, c) * eta(branch, a, add(b, c))
    for a in V4:
        assert eta(branch, ZERO, a) == eta(branch, a, ZERO) == 1


def commutator(branch: int, a: Elt, b: Elt) -> int:
    return eta(branch, b, a) * eta(branch, a, b)  # inverse=same for +/-1


def commutator_table(branch: int) -> Dict[Tuple[Elt, Elt], int]:
    verify_2_cocycle(branch)
    return {(a, b): commutator(branch, a, b) for a, b in product(V4, repeat=2)}


def is_commutator_trivial(branch: int) -> bool:
    return all(value == 1 for value in commutator_table(branch).values())


def main() -> None:
    assert is_commutator_trivial(0)
    assert not is_commutator_trivial(1)
    witness = ((1, 0), (0, 1))
    assert commutator(1, *witness) == -1

    print("H^2(V4,C*) has two restriction branches: trivial / nontrivial")
    print("trivial branch commutator: trivial => abelian 8-invertible extension")
    print("nontrivial branch witness", witness, "commutator=", commutator(1, *witness))
    print("nontrivial branch => nonabelian central extension => D8 or Q8")
    print("literature level bound then excludes R(D8,8) and R(Q8,8)")


if __name__ == "__main__":
    main()
