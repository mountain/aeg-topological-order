"""Direct exact local-relation certificate for component 13 / chirality mask 105.

This probe recompiles the fresh Phase-5 kernel and validates five short
pentagon entries by provenance.  It derives, without unsafe division,

    z0^2 = 1/2,
    p^3 = (1-i)/4,
    q^3 = (1-i)/4,
    z3*z10 = -i*p^2*z0,
    z6*z9  = -q^2*z0.

The quadratic is derived first, so z0 != 0 is established before using it to
cancel the z0 factor in the p^3/q^3 consequences.  No mask-0 relation is
imported and no Groebner/global nonlinear solve is used.
"""
from __future__ import annotations

import sympy as sp

import r22_phase5_monomial_lift as ml


P, Q = sp.symbols("p q")
ZS = sp.symbols("z0:21")
Z0, Z3, Z6, Z9, Z10 = ZS[0], ZS[3], ZS[6], ZS[9], ZS[10]
VARS = (P, Q) + ZS
EXT = [sp.I]

C = (1 + sp.I) / 4
D = (1 - sp.I) / 4

P1 = (("X", "X", "X", "X", "X"), (0, 0))
P2 = (("X", "X", "X", "X", "X"), (0, 2))
P3 = (("X", "X", "X", "X", "Y"), (0, 18))
P4 = (("X", "X", "X", "X", "Y"), (18, 18))
P5 = (("X", "X", "X", "X", "1"), (0, 0))
PROVENANCE = (P1, P2, P3, P4, P5)

MODELS = {
    P1: P**2 * Z0 - sp.I * Z3 * Z10,
    P2: P * Z3 * Z10 + C * Z0,
    P3: Q * Z6 * Z9 + D * Z0,
    P4: Q**2 * Z0 + Z6 * Z9,
    P5: P * Z3 * Z10 - sp.I * Q * Z6 * Z9 - C * Z0**2 + C / 2,
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
    cid, mask = 13, 105
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

    # P2 - i*P3 contains exactly the first two terms of P5.  Therefore
    # P5 - (P2 - i*P3) = C*(1/2-z0^2), before any localization.
    z0_residual = sp.expand(MODELS[P5] - (MODELS[P2] - sp.I * MODELS[P3]))
    expected_z0 = sp.expand(C * (sp.Rational(1, 2) - Z0**2))
    if sp.expand(z0_residual - expected_z0) != 0:
        raise AssertionError(("z0 residual", z0_residual, expected_z0))

    z0_quadratic = 2 * Z0**2 - 1

    # z0^2=1/2 proves z0 != 0.  Polynomial combinations then give
    #   p*P1 + i*P2 = z0*(p^3-D),
    #   q*P4 - P3   = z0*(q^3-D).
    p_combo = sp.expand(P * MODELS[P1] + sp.I * MODELS[P2])
    q_combo = sp.expand(Q * MODELS[P4] - MODELS[P3])
    if sp.expand(p_combo - Z0 * (P**3 - D)) != 0:
        raise AssertionError(("p cubic combination", p_combo))
    if sp.expand(q_combo - Z0 * (Q**3 - D)) != 0:
        raise AssertionError(("q cubic combination", q_combo))

    p3 = sp.expand(D)
    q3 = sp.expand(D)

    z3z10 = -sp.I * P**2 * Z0
    z6z9 = -Q**2 * Z0

    # p,q,z0 are nonzero from their nonzero cubic/quadratic constants.  The
    # product identities then prove z3,z10,z6,z9 nonzero individually.
    nonzero = ("p", "q", "z0", "z3", "z6", "z9", "z10")

    out = {
        "component": cid,
        "mask": mask,
        "unique_kernel_polynomials": len(unique),
        "p3": str(p3),
        "q3": str(q3),
        "z0_quadratic": str(z0_quadratic),
        "z3z10": str(z3z10),
        "z6z9": str(z6z9),
        "proved_nonzero": nonzero,
        "validated_provenance": PROVENANCE,
    }
    print(out, flush=True)
    print(
        "RESULT: component 13 / mask 105 local relations derived exactly; "
        "z0 is the finite scale variable",
        flush=True,
    )


if __name__ == "__main__":
    main()
