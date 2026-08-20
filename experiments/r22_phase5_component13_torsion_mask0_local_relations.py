"""Source-validated Phase-5 local relations for component 13 / mask 0 / D class 1.

This verifier recompiles the final kernel on the second physical D-amplitude
sheet, locates five fixed pentagon cells by provenance, and checks their exact
Gaussian-rational polynomials.  The scale equation is obtained by the literal
polynomial combination P5-P2+P3, so no localization or division by the scale
variable is used before its nonzeroness is proved.

No Groebner basis or global nonlinear solve is used.
"""
from __future__ import annotations

from fractions import Fraction

import sympy as sp

import r22_phase5_monomial_lift as ml
import r22_phase5_torsion_sheet as ts

CID = 13
MASK = 0

P1 = (("X", "X", "X", "X", "X"), (0, 0))
P2 = (("X", "X", "X", "X", "X"), (0, 2))
P3 = (("X", "X", "X", "X", "Y"), (0, 18))
P4 = (("X", "X", "X", "X", "Y"), (18, 18))
P5 = (("X", "X", "X", "X", "1"), (0, 0))
PROVS = (P1, P2, P3, P4, P5)


def gc_expr(k):
    a, b = ml.gfromkey(k)
    return sp.Rational(a.numerator, a.denominator) + sp.I * sp.Rational(b.numerator, b.denominator)


def key_expr(key, symbols):
    out = sp.Integer(0)
    for mon, gc in key:
        term = gc_expr(gc)
        for x, e in zip(symbols, mon):
            if e:
                term *= x ** e
        out += term
    return sp.expand(out)


def main():
    with ts.second_sheet_provider():
        quotient, unique = ml.compile_unique(CID, MASK)

    names = quotient["variables"]
    if names != ("p", "q") + tuple(f"z{i}" for i in range(21)):
        raise AssertionError(("unexpected Phase-5 chart", names))
    symbols = sp.symbols("p q " + " ".join(f"z{i}" for i in range(21)))
    p, q = symbols[:2]
    z = symbols[2:]

    by_prov = {prov: key for key, prov in unique.items()}
    missing = [prov for prov in PROVS if prov not in by_prov]
    if missing:
        raise AssertionError(("missing source provenance", missing))

    expr = {prov: key_expr(by_prov[prov], symbols) for prov in PROVS}

    # Fresh class-1 chart discovered by the fingerprint gate.
    s = z[5]
    up, vp = z[0], z[6]
    uq, vq = z[12], z[16]
    A = (1 - sp.I) / 4

    expected = {
        P1: p**2 * s + sp.I * up * vp,
        P2: p * up * vp + A * s,
        P3: q * uq * vq + A * s,
        P4: q**2 * s + uq * vq,
        P5: p * up * vp - q * uq * vq + (-1 + sp.I) * s**2 / 4 + (1 - sp.I) / 8,
    }
    for prov in PROVS:
        if sp.expand(expr[prov] - expected[prov]) != 0:
            raise AssertionError((prov, "source relation mismatch", expr[prov], expected[prov]))

    # This combination eliminates both product terms without dividing by s.
    scale_combo = sp.factor(expr[P5] - expr[P2] + expr[P3])
    scale_target = sp.factor((1 - sp.I) * (1 - 2*s**2) / 8)
    if sp.expand(scale_combo - scale_target) != 0:
        raise AssertionError(("scale combination mismatch", scale_combo, scale_target))

    # Once s^2=1/2, s is nonzero; these combinations then give the cube phases.
    p_combo = sp.factor(p * expr[P1] - sp.I * expr[P2])
    p_target = sp.factor(s * (p**3 - (1 + sp.I)/4))
    if sp.expand(p_combo - p_target) != 0:
        raise AssertionError(("p cube combination mismatch", p_combo, p_target))

    q_combo = sp.factor(q * expr[P4] - expr[P3])
    q_target = sp.factor(s * (q**3 - (1 - sp.I)/4))
    if sp.expand(q_combo - q_target) != 0:
        raise AssertionError(("q cube combination mismatch", q_combo, q_target))

    summary = {
        "component": CID,
        "mask": MASK,
        "D_amplitude_class": 1,
        "scale": "z5",
        "p_product": "z0*z6 = i*p^2*z5",
        "q_product": "z12*z16 = -q^2*z5",
        "scale_equation": "z5^2 = 1/2",
        "p3": "(1+i)/4",
        "q3": "(1-i)/4",
        "source_cells": PROVS,
        "prelocalization_scale_combination": "P5-P2+P3 = (1-i)*(1-2*z5^2)/8",
    }
    print("SUMMARY", summary, flush=True)
    print("RESULT: component 13 mask 0 class-1 five-cell local model is source-validated", flush=True)


if __name__ == "__main__":
    main()
