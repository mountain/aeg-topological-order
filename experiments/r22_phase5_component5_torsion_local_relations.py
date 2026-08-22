"""Fresh local Phase-5 relation derivation for component 5 on D class 1.

The historical component-5 closure used five short final-pentagon cells, but
the theorem audit found a second gauge-inequivalent D-amplitude sheet.  This
script does not import the historical p^3/q^3/product phases.  It recompiles the
class-1 kernel, reads the same five cells by provenance, derives the two product
relations and the p/q cube constants from their exact coefficients, and only
then reduces the fifth cell.

The z0=0 branch is not excluded here.  Cube constants are reported as the
consequence of these relations *conditional on z0 != 0*.  A separate raw-before-
canonical zero-branch gate must establish z0 != 0 before finite stratification.
"""
from __future__ import annotations

import argparse

import sympy as sp

import r22_phase5_component5_local_relations as old
import r22_phase5_monomial_lift as ml
import r22_phase5_torsion_sheet as ts


P, Q, T = old.P, old.Q, old.T
Z1, Z2, Z3, Z8 = old.Z1, old.Z2, old.Z3, old.Z8
VARS = old.VARS
EXT = old.EXT
PROVENANCE = old.PROVENANCE
P1, P2, P3, P4, P5 = PROVENANCE


def exact_coeff(expr, monomial):
    poly = sp.Poly(sp.expand(expr), *VARS, extension=EXT)
    return sp.cancel(poly.coeff_monomial(monomial))


def require_two_terms(expr, expected, label):
    poly = sp.Poly(sp.expand(expr), *VARS, extension=EXT)
    terms = poly.terms()
    if len(terms) != 2:
        raise AssertionError((label, "expected exactly two terms", expr, terms))
    got = {tuple(int(x) for x in powers) for powers, _coeff in terms}
    exp = {
        tuple(int(x) for x in sp.Poly(m, *VARS, extension=EXT).monoms()[0])
        for m in expected
    }
    if got != exp:
        raise AssertionError((label, "unexpected monomial support", got, exp, expr))


def derive(cid: int, mask: int):
    with ts.second_sheet_provider():
        quotient, unique = ml.compile_unique(cid, mask)

    if quotient["F_components"] != 21 or quotient["nvars"] != 23:
        raise AssertionError(("not a component-5-type quotient", cid, mask, quotient["F_components"], quotient["nvars"]))

    by_prov = {prov: key for key, prov in unique.items()}
    missing = [prov for prov in PROVENANCE if prov not in by_prov]
    if missing:
        raise AssertionError(("missing fixed local provenance", cid, mask, missing))

    e1 = old.project_expr(by_prov[P1])
    e2 = old.project_expr(by_prov[P2])
    e3 = old.project_expr(by_prov[P3])
    e4 = old.project_expr(by_prov[P4])
    e5 = old.project_expr(by_prov[P5])

    require_two_terms(e1, (P**2*T, Z2*Z3), "P1")
    require_two_terms(e2, (P*Z2*Z3, T), "P2")
    require_two_terms(e3, (Q*Z1*Z8, T), "P3")
    require_two_terms(e4, (Q**2*T, Z1*Z8), "P4")

    # P1: a p^2 z0 + b z2 z3 = 0 => z2 z3 = alpha p^2 z0.
    a1 = exact_coeff(e1, P**2*T)
    b1 = exact_coeff(e1, Z2*Z3)
    if a1 == 0 or b1 == 0:
        raise AssertionError(("degenerate P1", e1, a1, b1))
    alpha = sp.cancel(-a1 / b1)

    # P4: a q^2 z0 + b z1 z8 = 0 => z1 z8 = beta q^2 z0.
    a4 = exact_coeff(e4, Q**2*T)
    b4 = exact_coeff(e4, Z1*Z8)
    if a4 == 0 or b4 == 0:
        raise AssertionError(("degenerate P4", e4, a4, b4))
    beta = sp.cancel(-a4 / b4)

    # Conditional on z0 != 0, P2/P3 and the product relations determine p^3/q^3.
    c2 = exact_coeff(e2, P*Z2*Z3)
    d2 = exact_coeff(e2, T)
    c3 = exact_coeff(e3, Q*Z1*Z8)
    d3 = exact_coeff(e3, T)
    if 0 in (c2, d2, c3, d3):
        raise AssertionError(("degenerate cube relation", e2, e3))
    p3 = sp.cancel(-d2 / (c2 * alpha))
    q3 = sp.cancel(-d3 / (c3 * beta))

    reduced5 = sp.factor(old.reduce_p5(e5, alpha, beta, p3, q3))
    if reduced5.free_symbols - {T}:
        raise AssertionError(("P5 reduction retained unexpected variables", reduced5))
    p5poly = sp.Poly(reduced5, T, extension=EXT)
    if p5poly.is_zero:
        raise AssertionError("P5 vanished after only the four short relations")
    p5monic = sp.expand(p5poly.monic().as_expr())

    out = {
        "component": cid,
        "mask": mask,
        "D_amplitude_class": 1,
        "kernel_variables": quotient["nvars"],
        "F_components": quotient["F_components"],
        "unique_kernel_polynomials": len(unique),
        "P1": str(sp.factor(e1)),
        "P2": str(sp.factor(e2)),
        "P3": str(sp.factor(e3)),
        "P4": str(sp.factor(e4)),
        "P5": str(sp.factor(e5)),
        "z2z3_over_p2z0": str(alpha),
        "z1z8_over_q2z0": str(beta),
        "p3_if_z0_nonzero": str(p3),
        "q3_if_z0_nonzero": str(q3),
        "P5_reduced": str(reduced5),
        "P5_monic_in_z0": str(p5monic),
    }
    print(out, flush=True)
    print(
        "RESULT: class-1 component-5 five-cell local model derived from source provenance; "
        "z0 nonzero remains a separate proof gate",
        flush=True,
    )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, required=True)
    args = ap.parse_args()
    derive(args.component, args.mask)


if __name__ == "__main__":
    main()
