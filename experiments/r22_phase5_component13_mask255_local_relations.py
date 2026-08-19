"""Direct exact local-relation certificate for component 13 / chirality mask 255.

Run only after the mask-255 coordinate-stability gate.  This probe recompiles
the fresh Phase-5 kernel and validates five fixed short pentagon entries by
provenance.  Before any localization it derives

    z3^2 = 1/2.

Then, using z3 != 0, exact polynomial combinations give

    p^3 = (1-i)/4,
    q^3 = (-1+i)/4,
    z0*z4 = i*q^2*z3,
    z17*z18 = -i*p^2*z3.

Hence p,q,z3,z0,z4,z17,z18 are all nonzero.  No relation from masks
0/105/150 is imported and no Groebner/global nonlinear solve is used.
"""
from __future__ import annotations

import sympy as sp

import r22_phase5_monomial_lift as ml

P, Q = sp.symbols("p q")
ZS = sp.symbols("z0:21")
Z0, Z3, Z4, Z17, Z18 = ZS[0], ZS[3], ZS[4], ZS[17], ZS[18]
VARS = (P, Q) + ZS
EXT = [sp.I]

C = (1 + sp.I) / 4

P1 = (("X", "X", "X", "X", "X"), (0, 0))
P2 = (("X", "X", "X", "X", "X"), (0, 2))
P3 = (("X", "X", "X", "X", "Y"), (0, 18))
P4 = (("X", "X", "X", "X", "Y"), (18, 18))
P5 = (("X", "X", "X", "X", "1"), (0, 0))
PROVENANCE = (P1, P2, P3, P4, P5)

MODELS = {
    P1: Q**2 * Z3 + sp.I * Z0 * Z4,
    P2: Q * Z0 * Z4 + C * Z3,
    P3: P * Z17 * Z18 + C * Z3,
    P4: P**2 * Z3 - sp.I * Z17 * Z18,
    P5: P * Z17 * Z18 - Q * Z0 * Z4 + C * Z3**2 - C / 2,
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
    cid, mask = 13, 255
    _quotient, unique = ml.compile_unique(cid, mask)
    by_prov = {prov: key for key, prov in unique.items()}
    missing = [prov for prov in PROVENANCE if prov not in by_prov]
    if missing:
        raise AssertionError(("missing local provenance", missing))

    for prov in PROVENANCE:
        assert_proportional(kernel_expr(by_prov[prov]), MODELS[prov], prov)

    # P3-P2 supplies exactly p*z17*z18-q*z0*z4.  Therefore
    # P5-(P3-P2)=C*(z3^2-1/2), before any division.
    z3_residual = sp.expand(MODELS[P5] - (MODELS[P3] - MODELS[P2]))
    expected_z3 = sp.expand(C * (Z3**2 - sp.Rational(1, 2)))
    if sp.expand(z3_residual - expected_z3) != 0:
        raise AssertionError(("z3 residual", z3_residual, expected_z3))
    z3_quadratic = 2 * Z3**2 - 1

    # z3^2=1/2 proves z3 != 0.  Now exact polynomial combinations give
    # z3*(p^3+i*C)=0 and z3*(q^3-i*C)=0.
    p_combo = sp.expand(P * MODELS[P4] + sp.I * MODELS[P3])
    q_combo = sp.expand(Q * MODELS[P1] - sp.I * MODELS[P2])
    if sp.expand(p_combo - Z3 * (P**3 + sp.I * C)) != 0:
        raise AssertionError(("p cubic combination", p_combo))
    if sp.expand(q_combo - Z3 * (Q**3 - sp.I * C)) != 0:
        raise AssertionError(("q cubic combination", q_combo))

    p3 = sp.expand(-sp.I * C)
    q3 = sp.expand(sp.I * C)
    z0z4 = sp.I * Q**2 * Z3
    z17z18 = -sp.I * P**2 * Z3
    nonzero = ("p", "q", "z0", "z3", "z4", "z17", "z18")

    out = {
        "component": cid,
        "mask": mask,
        "unique_kernel_polynomials": len(unique),
        "p3": str(p3),
        "q3": str(q3),
        "z3_quadratic": str(z3_quadratic),
        "z0z4": str(z0z4),
        "z17z18": str(z17z18),
        "proved_nonzero": nonzero,
        "validated_provenance": PROVENANCE,
    }
    print(out, flush=True)
    print(
        "RESULT: component 13 / mask 255 local relations derived exactly; "
        "z3 is the finite scale variable",
        flush=True,
    )


if __name__ == "__main__":
    main()
