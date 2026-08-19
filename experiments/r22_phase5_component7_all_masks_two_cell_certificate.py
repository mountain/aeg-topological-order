"""Unified exact two-cell Phase-5 obstruction for scalar component 7.

Recompile each surviving chirality mask independently, in the fixed serial order
0, 105, 150, 255.  For every mask verify the same two raw final-pentagon
provenances:

    (XXXXX)_(0,0)    -> z0
    (XXXX;1)_(0,0)   -> z0^2 - 1/2

Thus every chirality requires z0=0 and z0^2=1/2 simultaneously.  This file is
a component-level replay certificate; it does not replace the earlier
mask-specific fresh kernel and coordinate-stability audits.
"""
from __future__ import annotations

import sympy as sp
import r22_phase5_monomial_lift as ml

CID = 7
MASKS = (0, 105, 150, 255)
P1 = (("X", "X", "X", "X", "X"), (0, 0))
P2 = (("X", "X", "X", "X", "1"), (0, 0))
P, Q = sp.symbols("p q")
ZS = sp.symbols("z0:17")
Z0 = ZS[0]
VARS = (P, Q) + ZS


def coeff_expr(gc):
    (ar, ad), (br, bd) = gc
    return sp.Rational(ar, ad) + sp.I * sp.Rational(br, bd)


def expr_from_key(key):
    out = sp.Integer(0)
    for mon, gc in key:
        term = coeff_expr(gc)
        for var, exp in zip(VARS, mon):
            if exp:
                term *= var ** exp
        out += term
    return sp.expand(out)


def monic(expr):
    poly = sp.Poly(sp.expand(expr), *VARS, extension=[sp.I])
    if poly.is_zero:
        raise AssertionError("unexpected zero polynomial")
    return poly.monic()


def verify(mask):
    _quotient, unique = ml.compile_unique(CID, mask)
    if len(unique) != 147:
        raise AssertionError((mask, "unexpected kernel size", len(unique)))
    by_prov = {prov: key for key, prov in unique.items()}
    if P1 not in by_prov or P2 not in by_prov:
        raise AssertionError((mask, "missing fixed provenance"))
    e1 = expr_from_key(by_prov[P1])
    e2 = expr_from_key(by_prov[P2])
    if monic(e1) != monic(Z0):
        raise AssertionError((mask, "P1 mismatch", e1))
    if monic(e2) != monic(Z0**2 - sp.Rational(1, 2)):
        raise AssertionError((mask, "P2 mismatch", e2))
    contradiction = sp.expand((Z0**2 - sp.Rational(1, 2)).subs(Z0, 0))
    if contradiction != -sp.Rational(1, 2):
        raise AssertionError((mask, contradiction))
    row = {
        "component": CID,
        "mask": mask,
        "unique_kernel_polynomials": len(unique),
        "P1": str(e1),
        "P2": str(e2),
        "contradiction": str(contradiction),
        "closed": True,
    }
    print(row, flush=True)
    return row


def main():
    rows = []
    for mask in MASKS:
        rows.append(verify(mask))
    if not all(r["closed"] for r in rows):
        raise AssertionError(rows)
    print("SUMMARY", {"component": CID, "closed_masks": MASKS, "closed": 4, "total": 4}, flush=True)
    print("RESULT: scalar component 7 is excluded in all four chirality masks by the same two fixed final-pentagon cells", flush=True)


if __name__ == "__main__":
    main()
