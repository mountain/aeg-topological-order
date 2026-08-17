"""Exact local algebra for a TPE attack on the open ring R(2,2).

This file deliberately stops one step before generating triangular-prism
polynomials.  Its purpose is to build, exactly and auditably, the local
algebroid data that the TPE localization of Liu--Palcoux--Ren--Vercleyen uses.

For the self-dual noninvertible simple X of R(2,2),

    X tensor X = 1 + h + 2 X + 2 Y.

Hence

    End(X tensor X) ~= C + C + M_2(C) + M_2(C)

as a semisimple algebra and has dimension n=10.  In the normalized I-shaped
basis of matrix units, the multiplication rule is the one used in the TPE
paper:

    tau_(c,i,j) tau_(c',k,l)
      = delta_(c,c') delta_(j,k) d_c^{-1} tau_(c,i,l),
    tr(tau_(c,i,j)) = delta_(i,j).

The string Fourier transform on this space therefore has n^2=100 local matrix
entries.  The TPE paper explains that the standard-prism localization gives
n^3 configurations, roughly n^3/3 after C3 rotation.

COMPUTATIONAL-CLAIM:
  * n = 10;
  * the 1000 ordered triples of I-basis elements split into exactly 340 C3
    orbits (10 fixed triples and 330 length-three orbits);
  * only 18 ordered triples have nonzero categorical trace of their product;
    these form 10 C3 orbits;
  * the nonzero values are 1 for the 1,h blocks and d_X^{-2}=5/2-sqrt(6)
    for the X,Y M2 blocks;
  * F^{XXX}_d block dimensions are 2,2,2,2,10,8 for
    d=1,g,h,k,X,Y respectively.

IMPORTANT AUDIT BOUNDARY:
The trilinear trace tensor computed here is certainly the known matrix-unit
algebra side used by TPE localization, but this script does NOT yet assert a
specific index-level polynomial contraction for Theorem 4.21.  The graphical
I/H-to-SFT dictionary must be matched to the paper before turning the 340
orbits into equations.  In particular, do not yet advertise "330 zero TPEs"
as a theorem; what is proved here is "330 zero orbits in the candidate known
I-basis trace tensor".
"""

from __future__ import annotations

from collections import Counter
from itertools import product
from typing import Dict, Iterable, Optional, Tuple

import sympy as sp

from fusion_ring import LABELS, fusion

ONE = "1"
X = "X"
Y = "Y"
H = "h"

D = sp.Integer(2) + sp.sqrt(6)
SIMPLE_DIMS: Dict[str, sp.Expr] = {
    "1": sp.Integer(1),
    "g": sp.Integer(1),
    "h": sp.Integer(1),
    "k": sp.Integer(1),
    "X": D,
    "Y": D,
}

# Multiplicities in X tensor X.
XX_MULTIPLICITIES = fusion(X, X)
assert XX_MULTIPLICITIES == {"1": 1, "h": 1, "X": 2, "Y": 2}

MatrixUnit = Tuple[str, int, int]
Triple = Tuple[int, int, int]


def i_basis() -> Tuple[MatrixUnit, ...]:
    basis = []
    for simple in ("1", "h", "X", "Y"):
        multiplicity = XX_MULTIPLICITIES[simple]
        for i in range(multiplicity):
            for j in range(multiplicity):
                basis.append((simple, i, j))
    assert len(basis) == 10
    return tuple(basis)


BASIS = i_basis()


def multiply_matrix_units(a: MatrixUnit, b: MatrixUnit) -> Tuple[Optional[MatrixUnit], sp.Expr]:
    c, i, j = a
    c2, k, ell = b
    if c != c2 or j != k:
        return None, sp.Integer(0)
    return (c, i, ell), sp.simplify(1 / SIMPLE_DIMS[c])


def categorical_trace(a: MatrixUnit) -> sp.Expr:
    _, i, j = a
    return sp.Integer(1) if i == j else sp.Integer(0)


def triple_trace(a: MatrixUnit, b: MatrixUnit, c: MatrixUnit) -> sp.Expr:
    ab, first = multiply_matrix_units(a, b)
    if first == 0 or ab is None:
        return sp.Integer(0)
    abc, second = multiply_matrix_units(ab, c)
    if second == 0 or abc is None:
        return sp.Integer(0)
    return sp.simplify(first * second * categorical_trace(abc))


def trace_tensor_nonzero_entries() -> Tuple[Tuple[Triple, sp.Expr], ...]:
    out = []
    for indices in product(range(len(BASIS)), repeat=3):
        value = sp.simplify(triple_trace(*(BASIS[i] for i in indices)))
        if value != 0:
            out.append((indices, value))
    assert len(out) == 18
    values = Counter(sp.sstr(value) for _, value in out)
    assert values == Counter({sp.sstr(sp.Rational(5, 2) - sp.sqrt(6)): 16, "1": 2})
    return tuple(out)


def rotate(triple: Triple) -> Triple:
    a, b, c = triple
    return (b, c, a)


def cyclic_orbits() -> Tuple[Tuple[Tuple[Triple, ...], sp.Expr], ...]:
    seen = set()
    out = []
    for triple in product(range(len(BASIS)), repeat=3):
        if triple in seen:
            continue
        orbit_set = {triple, rotate(triple), rotate(rotate(triple))}
        seen.update(orbit_set)
        values = {
            sp.simplify(triple_trace(*(BASIS[i] for i in item)))
            for item in orbit_set
        }
        assert len(values) == 1  # cyclicity of the categorical trace
        out.append((tuple(sorted(orbit_set)), next(iter(values))))

    assert len(out) == 340
    orbit_sizes = Counter(len(orbit) for orbit, _ in out)
    assert orbit_sizes == Counter({3: 330, 1: 10})

    nonzero = [(orbit, value) for orbit, value in out if value != 0]
    assert len(nonzero) == 10
    nonzero_values = Counter(sp.sstr(value) for _, value in nonzero)
    assert nonzero_values == Counter({sp.sstr(sp.Rational(5, 2) - sp.sqrt(6)): 8, "1": 2})
    return tuple(out)


def fusion_coefficient(a: str, b: str, c: str) -> int:
    return int(fusion(a, b).get(c, 0))


def associator_block_dimension(a: str, b: str, c: str, out: str) -> int:
    left = sum(
        fusion_coefficient(a, b, e) * fusion_coefficient(e, c, out)
        for e in LABELS
    )
    right = sum(
        fusion_coefficient(b, c, f) * fusion_coefficient(a, f, out)
        for f in LABELS
    )
    assert left == right
    return left


def f_xxx_profile() -> Dict[str, int]:
    profile = {out: associator_block_dimension(X, X, X, out) for out in LABELS}
    assert profile == {"1": 2, "g": 2, "h": 2, "k": 2, "X": 10, "Y": 8}
    return profile


def local_summary() -> Dict[str, object]:
    orbits = cyclic_orbits()
    nonzero_orbits = sum(1 for _, value in orbits if value != 0)
    return {
        "End_X2_dimension": len(BASIS),
        "SFT_unknown_entries": len(BASIS) ** 2,
        "ordered_standard_triples": len(BASIS) ** 3,
        "C3_orbits": len(orbits),
        "nonzero_ordered_trace_entries": len(trace_tensor_nonzero_entries()),
        "nonzero_trace_orbits": nonzero_orbits,
        "zero_trace_orbits": len(orbits) - nonzero_orbits,
        "F_XXX_block_dimensions": f_xxx_profile(),
    }


def main() -> None:
    print("R(2,2) local TPE algebra")
    print("  X^2 =", XX_MULTIPLICITIES)
    print("  d_X =", D)
    print("  I-basis:")
    for index, item in enumerate(BASIS):
        print(f"    {index}: {item}")

    print("\nsummary")
    for key, value in local_summary().items():
        print(f"  {key}: {value}")

    print("\nnonzero trilinear trace entries")
    for indices, value in trace_tensor_nonzero_entries():
        print(" ", indices, "=", value)

    print("\nAUDIT BOUNDARY:")
    print("  The 10-dimensional I-basis algebra is exact.")
    print("  The index-level standard-TPE polynomial dictionary is still pending.")


if __name__ == "__main__":
    main()
