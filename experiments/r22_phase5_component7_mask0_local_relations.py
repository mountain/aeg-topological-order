"""Exact local source certificate for component 7 / chirality mask 0.

Run only after the coordinate-stability gate.  Recompile the fresh Phase-5
kernel and verify two fixed final-pentagon provenances:

    (XXXXX)_(0,0)    -> z0 = 0
    (XXXX;1)_(0,0)   -> z4^2 - 1/2 = 0

The second relation proves z4 != 0.  No component-5/13 relation is imported,
and no nonlinear solve is performed.
"""
from __future__ import annotations

import sympy as sp

import r22_phase5_monomial_lift as ml

CID = 7
MASK = 0
P1 = (("X", "X", "X", "X", "X"), (0, 0))
P2 = (("X", "X", "X", "X", "1"), (0, 0))
PROVENANCE = (P1, P2)

P, Q = sp.symbols("p q")
ZS = sp.symbols("z0:17")
Z0 = ZS[0]
Z4 = ZS[4]
VARS = (P, Q) + ZS


def coeff_expr(gc):
    (ar, ad), (br, bd) = gc
    return sp.Rational(ar, ad) + sp.I * sp.Rational(br, bd)


def kernel_expr(key):
    expr = sp.Integer(0)
    for mon, gc in key:
        term = coeff_expr(gc)
        for var, e in zip(VARS, mon):
            if e:
                term *= var ** e
        expr += term
    return sp.expand(expr)


def monic(expr):
    poly = sp.Poly(sp.expand(expr), *VARS, extension=[sp.I])
    if poly.is_zero:
        raise AssertionError("unexpected zero polynomial")
    return poly.monic()


def main():
    _quotient, unique = ml.compile_unique(CID, MASK)
    by_prov = {prov: key for key, prov in unique.items()}
    missing = [p for p in PROVENANCE if p not in by_prov]
    if missing:
        raise AssertionError(("missing provenance", missing))

    e1 = kernel_expr(by_prov[P1])
    e2 = kernel_expr(by_prov[P2])

    if monic(e1) != monic(Z0):
        raise AssertionError(("P1 is not proportional to z0", e1))
    if monic(e2) != monic(Z4**2 - sp.Rational(1, 2)):
        raise AssertionError(("P2 is not proportional to z4^2-1/2", e2))

    out = {
        "component": CID,
        "mask": MASK,
        "unique_kernel_polynomials": len(unique),
        "P1": str(e1),
        "P2": str(e2),
        "derived": ("z0=0", "z4^2=1/2", "z4!=0"),
        "validated_provenance": PROVENANCE,
    }
    print(out, flush=True)
    print(
        "RESULT: component 7 / mask 0 local source relations verified exactly; "
        "z0 is forced zero and z4 is a nonzero quadratic scale",
        flush=True,
    )


if __name__ == "__main__":
    main()
