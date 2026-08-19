"""Direct exact local-relation certificate for component 13 / chirality mask 150.

This probe is intended to run only after the mask-150 coordinate-stability gate.
It recompiles the fresh Phase-5 kernel and validates five short pentagon entries
by provenance.  It derives, before any unsafe division,

    z6^2 = 1/2,
    p^3 = q^3 = (-1+i)/4,
    z0*z9 = -p^2*z6,
    z1*z7 = q^2*z6.

Hence p,q,z6,z0,z9,z1,z7 are all nonzero.
No mask-0/mask-105 relation is imported and no Groebner/global nonlinear solve
is used.
"""
from __future__ import annotations

import sympy as sp

import r22_phase5_monomial_lift as ml


P, Q = sp.symbols("p q")
ZS = sp.symbols("z0:21")
Z0, Z1, Z6, Z7, Z9 = ZS[0], ZS[1], ZS[6], ZS[7], ZS[9]
VARS = (P, Q) + ZS
EXT = [sp.I]

D = (1 - sp.I) / 4

P1 = (("X", "X", "X", "X", "X"), (0, 0))
P2 = (("X", "X", "X", "X", "X"), (0, 2))
P3 = (("X", "X", "X", "X", "Y"), (0, 18))
P4 = (("X", "X", "X", "X", "Y"), (18, 18))
P5 = (("X", "X", "X", "X", "1"), (0, 0))
PROVENANCE = (P1, P2, P3, P4, P5)

MODELS = {
    P1: P**2 * Z6 + Z0 * Z9,
    P2: P * Z0 * Z9 - D * Z6,
    P3: Q * Z1 * Z7 + D * Z6,
    P4: Q**2 * Z6 - Z1 * Z7,
    P5: P * Z0 * Z9 + Q * Z1 * Z7 + D * Z6**2 - D / 2,
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
    cid, mask = 13, 150
    _quotient, unique = ml.compile_unique(cid, mask)
    by_prov = {prov: key for key, prov in unique.items()}
    missing = [prov for prov in PROVENANCE if prov not in by_prov]
    if missing:
        raise AssertionError(("missing local provenance", missing))

    for prov in PROVENANCE:
        expr = kernel_expr(by_prov[prov])
        assert_proportional(expr, MODELS[prov], prov)

    # P2+P3 supplies exactly the two mixed terms of P5.  Therefore
    # P5-(P2+P3)=D*(z6^2-1/2), before localization.
    z6_residual = sp.expand(MODELS[P5] - (MODELS[P2] + MODELS[P3]))
    expected_z6 = sp.expand(D * (Z6**2 - sp.Rational(1, 2)))
    if sp.expand(z6_residual - expected_z6) != 0:
        raise AssertionError(("z6 residual", z6_residual, expected_z6))
    z6_quadratic = 2 * Z6**2 - 1

    # z6^2=1/2 proves z6 != 0.  Exact polynomial combinations then give
    # z6*(p^3+D)=0 and z6*(q^3+D)=0.
    p_combo = sp.expand(P * MODELS[P1] - MODELS[P2])
    q_combo = sp.expand(Q * MODELS[P4] + MODELS[P3])
    if sp.expand(p_combo - Z6 * (P**3 + D)) != 0:
        raise AssertionError(("p cubic combination", p_combo))
    if sp.expand(q_combo - Z6 * (Q**3 + D)) != 0:
        raise AssertionError(("q cubic combination", q_combo))

    p3 = sp.expand(-D)
    q3 = sp.expand(-D)
    z0z9 = -P**2 * Z6
    z1z7 = Q**2 * Z6
    nonzero = ("p", "q", "z0", "z1", "z6", "z7", "z9")

    out = {
        "component": cid,
        "mask": mask,
        "unique_kernel_polynomials": len(unique),
        "p3": str(p3),
        "q3": str(q3),
        "z6_quadratic": str(z6_quadratic),
        "z0z9": str(z0z9),
        "z1z7": str(z1z7),
        "proved_nonzero": nonzero,
        "validated_provenance": PROVENANCE,
    }
    print(out, flush=True)
    print(
        "RESULT: component 13 / mask 150 local relations derived exactly; "
        "z6 is the finite scale variable",
        flush=True,
    )


if __name__ == "__main__":
    main()
