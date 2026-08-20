"""Source-validated Phase-5 local relations for component 13 / mask 255 / D class 1.

The verifier recompiles the final kernel on the second physical D-amplitude
sheet, locates five fixed final-pentagon cells by provenance, and checks their
raw exact Gaussian-rational polynomials.  The finite scale equation is derived
by polynomial addition before any localization or division by the scale.
"""
from __future__ import annotations

import sympy as sp

import r22_phase5_monomial_lift as ml
import r22_phase5_torsion_sheet as ts

CID = 13
MASK = 255

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

    s = z[3]
    uq, vq = z[0], z[4]
    up, vp = z[17], z[18]
    A = (1 + sp.I) / 4

    expected = {
        P1: q**2 * s - sp.I * uq * vq,
        P2: q * uq * vq + A * s,
        P3: p * up * vp + A * s,
        P4: p**2 * s - sp.I * up * vp,
        P5: p * up * vp - q * uq * vq + A * s**2 - A / 2,
    }
    for prov in PROVS:
        if sp.expand(expr[prov] - expected[prov]) != 0:
            raise AssertionError((prov, "source relation mismatch", expr[prov], expected[prov]))

    # Eliminate both product terms before any division by s.
    scale_combo = sp.factor(expr[P5] - expr[P3] + expr[P2])
    scale_target = sp.factor(A * (s**2 - sp.Rational(1, 2)))
    if sp.expand(scale_combo - scale_target) != 0:
        raise AssertionError(("scale combination mismatch", scale_combo, scale_target))

    # Once s^2=1/2, s!=0.  The following polynomial combinations then give
    # the two exact cubic phases.
    p_combo = sp.factor(p * expr[P4] + sp.I * expr[P3])
    p_target = sp.factor(s * (p**3 - (1 - sp.I) / 4))
    if sp.expand(p_combo - p_target) != 0:
        raise AssertionError(("p cube combination mismatch", p_combo, p_target))

    q_combo = sp.factor(q * expr[P1] + sp.I * expr[P2])
    q_target = sp.factor(s * (q**3 - (1 - sp.I) / 4))
    if sp.expand(q_combo - q_target) != 0:
        raise AssertionError(("q cube combination mismatch", q_combo, q_target))

    summary = {
        "component": CID,
        "mask": MASK,
        "D_amplitude_class": 1,
        "scale": "z3",
        "scale_equation": "z3^2=1/2",
        "p3": "(1-i)/4",
        "q3": "(1-i)/4",
        "q_product": "z0*z4=-i*q^2*z3",
        "p_product": "z17*z18=-i*p^2*z3",
        "source_cells": PROVS,
        "prelocalization_scale_combination": "P5-P3+P2=(1+i)*(z3^2-1/2)/4",
    }
    print("SUMMARY", summary, flush=True)
    print("RESULT: component 13 mask 255 class-1 five-cell local model is source-validated", flush=True)


if __name__ == "__main__":
    main()
