"""Exact two-cell source certificate for component 7 / chirality mask 105.

Freshly recompile mask 105 and verify the same two fixed final-pentagon
provenances independently of mask 0:

    (XXXXX)_(0,0)    -> z0 = 0
    (XXXX;1)_(0,0)   -> z0^2 - 1/2 = 0

Together they give -1/2=0. No result from mask 0 is imported as a premise.
"""
from __future__ import annotations

import sympy as sp
import r22_phase5_monomial_lift as ml

CID = 7
MASK = 105
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
        for var, e in zip(VARS, mon):
            if e:
                term *= var ** e
        out += term
    return sp.expand(out)


def monic(expr):
    p = sp.Poly(sp.expand(expr), *VARS, extension=[sp.I])
    if p.is_zero:
        raise AssertionError("unexpected zero polynomial")
    return p.monic()


def main():
    _q, unique = ml.compile_unique(CID, MASK)
    by_prov = {prov: key for key, prov in unique.items()}
    for prov in (P1, P2):
        if prov not in by_prov:
            raise AssertionError(("missing provenance", prov))
    e1 = expr_from_key(by_prov[P1])
    e2 = expr_from_key(by_prov[P2])
    if monic(e1) != monic(Z0):
        raise AssertionError(("P1 mismatch", e1))
    if monic(e2) != monic(Z0**2 - sp.Rational(1,2)):
        raise AssertionError(("P2 mismatch", e2))
    contradiction = sp.expand((Z0**2-sp.Rational(1,2)).subs(Z0,0))
    if contradiction != -sp.Rational(1,2):
        raise AssertionError(contradiction)
    print({
        "component": CID,
        "mask": MASK,
        "unique_kernel_polynomials": len(unique),
        "P1": str(e1),
        "P2": str(e2),
        "contradiction": str(contradiction),
        "closed": True,
    }, flush=True)
    print("RESULT: component 7 / mask 105 is excluded by two fixed final-pentagon cells", flush=True)


if __name__ == "__main__":
    main()
