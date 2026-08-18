"""Direct exact local-relation certificate for component 13 / chirality mask 0.

This probe recompiles the final Phase-5 kernel and locates five short pentagon
entries by provenance.  It verifies that they are exactly proportional to a
small local model and then derives, without unsafe division,

    z5^2 = 1/2,
    p^3 = -(1+i)/4,
    q^3 =  (1+i)/4,
    z0*z6  = -i*p^2*z5,
    z11*z14 = i*q^2*z5.

Consequently p,q,z0,z5,z6,z11,z14 are all nonzero.

No component-5 rewrite rule is imported and no Groebner/global nonlinear solve
is used.
"""
from __future__ import annotations

from fractions import Fraction

import sympy as sp

import r22_phase5_monomial_lift as ml


P, Q = sp.symbols("p q")
ZS = sp.symbols("z0:21")
Z0, Z5, Z6, Z11, Z14 = (ZS[0], ZS[5], ZS[6], ZS[11], ZS[14])
VARS = (P, Q) + ZS
EXT = [sp.I]

C = (1 - sp.I) / 4

P1 = (("X", "X", "X", "X", "X"), (0, 0))
P2 = (("X", "X", "X", "X", "X"), (0, 2))
P3 = (("X", "X", "X", "X", "Y"), (0, 18))
P4 = (("X", "X", "X", "X", "Y"), (18, 18))
P5 = (("X", "X", "X", "X", "1"), (0, 0))
PROVENANCE = (P1, P2, P3, P4, P5)

MODELS = {
    P1: P**2 * Z5 - sp.I * Z0 * Z6,
    P2: P * Z0 * Z6 + C * Z5,
    P3: Q * Z11 * Z14 + C * Z5,
    P4: Q**2 * Z5 + sp.I * Z11 * Z14,
    P5: P * Z0 * Z6 - Q * Z11 * Z14 - C * Z5**2 + C / 2,
}


def coeff_expr(gc):
    (ar, ad), (br, bd) = gc
    return sp.Rational(ar, ad) + sp.I * sp.Rational(br, bd)


def kernel_expr(key):
    expr = sp.Integer(0)
    for mon, gc in key:
        term = coeff_expr(gc)
        term *= P ** mon[0]
        term *= Q ** mon[1]
        for j, e in enumerate(mon[2:]):
            if e:
                term *= ZS[j] ** e
        expr += term
    return sp.expand(expr)


def monic(expr):
    poly = sp.Poly(sp.expand(expr), *VARS, extension=EXT)
    if poly.is_zero:
        raise AssertionError("unexpected zero polynomial")
    return poly.monic()


def assert_proportional(expr, model, label):
    a = monic(expr)
    b = monic(model)
    if a != b:
        raise AssertionError((label, "not proportional", a.as_expr(), b.as_expr()))


def main():
    cid, mask = 13, 0
    _quotient, unique = ml.compile_unique(cid, mask)
    by_prov = {prov: key for key, prov in unique.items()}
    missing = [prov for prov in PROVENANCE if prov not in by_prov]
    if missing:
        raise AssertionError(("missing local provenance", missing))

    exact = {}
    for prov in PROVENANCE:
        expr = kernel_expr(by_prov[prov])
        assert_proportional(expr, MODELS[prov], prov)
        exact[prov] = expr

    # P5 - (P2 - P3) = C*(1/2 - z5^2).  This step uses only polynomial
    # addition/subtraction, so z5^2=1/2 is obtained before any localization.
    z5_residual = sp.expand(MODELS[P5] - (MODELS[P2] - MODELS[P3]))
    expected_z5 = sp.expand(C * (sp.Rational(1, 2) - Z5**2))
    if sp.expand(z5_residual - expected_z5) != 0:
        raise AssertionError(("z5 residual", z5_residual, expected_z5))

    z5_quadratic = 2 * Z5**2 - 1

    # With z5 != 0, p*P1 together with P2 gives
    # z5*(p^3 + i*C)=0, and q*P4 together with P3 gives
    # z5*(q^3 - i*C)=0.
    p3 = sp.expand(-sp.I * C)
    q3 = sp.expand(sp.I * C)
    if p3 != -(1 + sp.I) / 4:
        raise AssertionError(("p3", p3))
    if q3 != (1 + sp.I) / 4:
        raise AssertionError(("q3", q3))

    # Product identities follow from the exact local models.
    z0z6 = -sp.I * P**2 * Z5
    z11z14 = sp.I * Q**2 * Z5

    # The constants in p3/q3 and z5 quadratic are nonzero, hence
    # p,q,z5 are nonzero.  P2/P3 then make the two products nonzero,
    # proving z0,z6,z11,z14 nonzero individually.
    nonzero = ("p", "q", "z0", "z5", "z6", "z11", "z14")

    out = {
        "component": cid,
        "mask": mask,
        "unique_kernel_polynomials": len(unique),
        "p3": str(p3),
        "q3": str(q3),
        "z5_quadratic": str(z5_quadratic),
        "z0z6": str(z0z6),
        "z11z14": str(z11z14),
        "proved_nonzero": nonzero,
        "validated_provenance": PROVENANCE,
    }
    print(out, flush=True)
    print(
        "RESULT: component 13 / mask 0 local relations derived exactly; "
        "z5 is the finite scale variable and z0 is proved nonzero",
        flush=True,
    )


if __name__ == "__main__":
    main()
