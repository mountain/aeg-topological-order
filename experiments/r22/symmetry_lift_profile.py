"""Finite residual kernel for the open R(2,2) categorification attack.

This file records a CONDITIONAL reduction, not a categorification theorem.

Let tau be the based-ring involution fixing the pointed V4 sector and swapping
X<->Y.  Previous exact calculations in this branch show that tau has a genuine
order-two lift as an autoequivalence of the pointed module M=<X,Y>.  The open
question is whether this pointed-module symmetry extends through M tensor M to
an order-two tensor autoequivalence of a hypothetical full categorification C.

The script measures the only tensorator blocks not already controlled by the
pointed/module layer and proves the finite consequences of a *strict-pointed*
lift, meaning that T|_P is the identity monoidal functor on
P = Vec^omega_{V4}.

COMPUTATIONAL-CLAIM:
  - MxM contains 16 nonzero tensorator multiplicity blocks / 40 raw matrix
    parameters;
  - tau pairs them into 8 block orbits / 20 representative raw parameters.

CONDITIONAL CLASSICAL CONSEQUENCE:
  If such a strict-pointed C2 tensor action exists, equivariantization has
  eight invertible objects and one noninvertible object rho of dimension
  4+2*sqrt(6), hence near-group level 8.  The invertible group is abelian:
  C2^3 for trivial action-coherence character and C4 x C2 for any nontrivial
  character.  Schopieray's categorifiability theorem excludes C2^3+8, so the
  only categorifiable strict-pointed target is C4 x C2 + 8.

The final Schopieray exclusion is a literature theorem and is NOT encoded as a
computer proof below; this script verifies only the finite group/dimension
part of the conditional reduction.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
from typing import Dict, Tuple

import sympy as sp

from fusion_ring import LABELS, NONINV, fusion, tau_permutation, permutation_as_map

TAU_MAP = permutation_as_map(tau_permutation())


def mm_tensorator_blocks() -> Tuple[Tuple[str, str, str, int], ...]:
    """Nonzero multiplicity blocks of T_2 on M tensor M."""
    blocks = []
    for a, b in product(NONINV, repeat=2):
        for c, multiplicity in fusion(a, b).items():
            ta, tb, tc = TAU_MAP[a], TAU_MAP[b], TAU_MAP[c]
            assert fusion(ta, tb).get(tc, 0) == multiplicity
            blocks.append((a, b, c, multiplicity))
    assert len(blocks) == 16
    assert sum(m * m for _, _, _, m in blocks) == 40
    return tuple(blocks)


def tau_block_orbits() -> Tuple[Tuple[Tuple[Tuple[str, str, str, int], ...], int], ...]:
    """Pair MxM tensorator blocks under tau; weight is raw GL(m) entries."""
    blocks = set(mm_tensorator_blocks())
    seen = set()
    orbits = []
    for key in sorted(blocks):
        if key in seen:
            continue
        a, b, c, m = key
        image = (TAU_MAP[a], TAU_MAP[b], TAU_MAP[c], m)
        assert image in blocks
        orbit = tuple(sorted({key, image}))
        seen.update(orbit)
        orbits.append((orbit, m * m))
    assert len(orbits) == 8
    assert sum(weight for _, weight in orbits) == 20
    assert all(len(orbit) == 2 for orbit, _ in orbits)
    return tuple(orbits)


# V4 written additively.
V4 = ((0, 0), (1, 0), (0, 1), (1, 1))
ZERO = (0, 0)
Elt = Tuple[int, int]
LiftElt = Tuple[Elt, int]  # second coordinate is exponent of i mod 4


def add(a: Elt, b: Elt) -> Elt:
    return (a[0] ^ b[0], a[1] ^ b[1])


def character(kind: Elt, a: Elt) -> int:
    """All Hom(V4,C2), represented by dot product mod 2."""
    return (kind[0] * a[0] + kind[1] * a[1]) & 1


def equivariant_invertibles(kind: Elt) -> Tuple[LiftElt, ...]:
    """Strict-pointed equivariant structures u with u^2=chi(g).

    Write u=i^r.  Then u^2=(-1)^r and r mod 2 equals the C2-valued
    character.  There are two choices for each pointed simple.
    """
    return tuple(
        (a, r)
        for a in V4
        for r in range(4)
        if (r & 1) == character(kind, a)
    )


def multiply(x: LiftElt, y: LiftElt) -> LiftElt:
    a, r = x
    b, s = y
    return (add(a, b), (r + s) % 4)


def element_order(kind: Elt, x: LiftElt) -> int:
    identity = (ZERO, 0)
    y = identity
    for n in range(1, 9):
        y = multiply(y, x)
        if y == identity:
            return n
    raise AssertionError("order > 8 in an 8-element group")


def strict_pointed_invertible_group(kind: Elt) -> Dict[str, object]:
    elems = equivariant_invertibles(kind)
    assert len(elems) == 8
    elem_set = set(elems)
    for x, y in product(elems, repeat=2):
        assert multiply(x, y) in elem_set
        assert multiply(x, y) == multiply(y, x)
    orders = Counter(element_order(kind, x) for x in elems)
    if kind == ZERO:
        assert orders == Counter({2: 7, 1: 1})
        group = "C2^3"
    else:
        assert orders == Counter({4: 4, 2: 3, 1: 1})
        group = "C4xC2"
    return {"character": kind, "group": group, "order_distribution": dict(orders)}


def near_group_dimension_check() -> Dict[str, sp.Expr]:
    d = sp.Integer(2) + sp.sqrt(6)
    rho = sp.expand(2 * d)
    source_global = sp.expand(4 + 2 * d**2)
    equiv_global = sp.expand(2 * source_global)

    # Unique noninvertible in equivariantization => rho^2 = sum_g g + ell*rho.
    ell = sp.simplify((rho**2 - 8) / rho)
    assert ell == 8
    assert sp.expand(equiv_global - (8 + rho**2)) == 0
    return {
        "FPdim_X": d,
        "FPdim_rho": rho,
        "source_global_dimension": source_global,
        "equivariantized_global_dimension": equiv_global,
        "near_group_level": ell,
    }


def main() -> None:
    print("MxM tensorator blocks")
    print("  blocks:", len(mm_tensorator_blocks()))
    print("  raw matrix parameters:", sum(m * m for _, _, _, m in mm_tensorator_blocks()))
    print("\ntau block orbits")
    for orbit, weight in tau_block_orbits():
        print(" ", orbit, "parameters=", weight)
    print("  representative raw parameters:", sum(w for _, w in tau_block_orbits()))

    print("\nstrict-pointed equivariantized invertible groups")
    for kind in V4:
        print(" ", strict_pointed_invertible_group(kind))

    print("\nnear-group dimension forcing")
    for key, value in near_group_dimension_check().items():
        print(f"  {key}: {value}")

    print("\nCONDITIONAL reduction:")
    print("  strict-pointed tau lift => C2^3+8 or C4xC2+8")
    print("  Schopieray excludes categorifiability of C2^3+8")
    print("  therefore any categorifiable strict-pointed lift targets C4xC2+8")


if __name__ == "__main__":
    main()
