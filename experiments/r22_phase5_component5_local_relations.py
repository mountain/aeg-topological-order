"""Exact source validation for the five component-5 Phase-5 local relations.

For masks 150 and 255 this probe does not assume the finite relations.  It
recompiles the exact final-pentagon kernel, locates the five short pentagon
entries by provenance, and verifies directly that the first four are
proportional to the claimed product/cube relations.  It then reduces the fifth
entry using only those four relations and the resulting p^3/q^3 constants and
checks that the residual polynomial is exactly proportional to

    2*z0^2 + 4*z0 - 1.

No z0 quadratic is used while deriving the z0 quadratic, and no division by an
unknown F variable is performed.
"""
from __future__ import annotations

import argparse

import sympy as sp

import r22_phase5_component5_rest_audit as fa
import r22_phase5_monomial_lift as ml
import r22_phase5_ratio_classes as rc


P, Q, T = sp.symbols("p q z0")
Z1, Z2, Z3, Z8 = sp.symbols("z1 z2 z3 z8")
VARS = (P, Q, T, Z1, Z2, Z3, Z8)
EXT = [sp.I]

P1 = (("X", "X", "X", "X", "X"), (0, 0))
P2 = (("X", "X", "X", "X", "X"), (0, 2))
P3 = (("X", "X", "X", "X", "Y"), (0, 18))
P4 = (("X", "X", "X", "X", "Y"), (18, 18))
P5 = (("X", "X", "X", "X", "1"), (0, 0))
PROVENANCE = (P1, P2, P3, P4, P5)


def coeff_expr(gc):
    return rc.gc_expr(ml.gfromkey(gc))


def project_expr(key):
    """Project one local kernel polynomial to its expected seven variables."""
    out = sp.Integer(0)
    for mon, gc in key:
        zexp = mon[3:]
        unexpected = tuple(zi for zi, e in enumerate(zexp) if e and zi not in {0, 1, 2, 7})
        if unexpected:
            raise AssertionError(("unexpected local F variables", unexpected, mon))
        term = coeff_expr(gc) * P ** mon[0] * Q ** mon[1] * T ** mon[2]
        term *= Z1 ** zexp[0]
        term *= Z2 ** zexp[1]
        term *= Z3 ** zexp[2]
        term *= Z8 ** zexp[7]
        out += term
    return sp.expand(out)


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


def reduce_p5(expr, alpha, beta, p3, q3):
    """Reduce P5 by z2*z3, z1*z8 and p^3/q^3, but NOT by any z0 relation."""
    poly = sp.Poly(sp.expand(expr), *VARS, extension=EXT)
    out = sp.Integer(0)
    for exps, coeff in poly.terms():
        ep, eq, et, e1, e2, e3, e8 = map(int, exps)

        k = min(e2, e3)
        if k:
            e2 -= k
            e3 -= k
            ep += 2 * k
            et += k
            coeff *= alpha ** k

        k = min(e1, e8)
        if k:
            e1 -= k
            e8 -= k
            eq += 2 * k
            et += k
            coeff *= beta ** k

        kp, ep = divmod(ep, 3)
        kq, eq = divmod(eq, 3)
        coeff *= p3 ** kp
        coeff *= q3 ** kq

        out += (
            coeff
            * P ** ep
            * Q ** eq
            * T ** et
            * Z1 ** e1
            * Z2 ** e2
            * Z3 ** e3
            * Z8 ** e8
        )
    return sp.expand(out)


def audit(cid, mask):
    if mask not in fa.REL:
        raise ValueError(("supported masks", tuple(fa.REL)))

    rel = fa.REL[mask]
    p3 = rc.gc_expr(rel["P3"])
    q3 = rc.gc_expr(rel["Q3"])
    alpha = rc.gc_expr(rel["Z23"])
    beta = rc.gc_expr(rel["Z18"])

    _quotient, unique = ml.compile_unique(cid, mask)
    by_prov = {prov: key for key, prov in unique.items()}
    missing = [prov for prov in PROVENANCE if prov not in by_prov]
    if missing:
        raise AssertionError((mask, "missing local provenance", missing))

    e1 = project_expr(by_prov[P1])
    e2 = project_expr(by_prov[P2])
    e3 = project_expr(by_prov[P3])
    e4 = project_expr(by_prov[P4])
    e5 = project_expr(by_prov[P5])

    # These four equations are equivalent, up to nonzero Gaussian scalars, to
    # z2*z3 = alpha*p^2*z0,
    # p*z2*z3 = alpha*p3*z0,
    # q*z1*z8 = beta*q3*z0,
    # z1*z8 = beta*q^2*z0.
    assert_proportional(e1, Z2 * Z3 - alpha * P ** 2 * T, (mask, "P1"))
    assert_proportional(e2, P * Z2 * Z3 - alpha * p3 * T, (mask, "P2"))
    assert_proportional(e3, Q * Z1 * Z8 - beta * q3 * T, (mask, "P3"))
    assert_proportional(e4, Z1 * Z8 - beta * Q ** 2 * T, (mask, "P4"))

    # Once z0 != 0 is proved, P1/P2 and P3/P4 give p^3=p3 and q^3=q3.
    # The fifth cell must then produce the z0 quadratic without assuming it.
    r5 = sp.factor(reduce_p5(e5, alpha, beta, p3, q3))
    if r5.free_symbols - {T}:
        raise AssertionError((mask, "P5 reduction retained unexpected variables", r5))
    target = 2 * T ** 2 + 4 * T - 1
    if sp.Poly(r5, T, extension=EXT).monic() != sp.Poly(target, T, extension=EXT).monic():
        raise AssertionError((mask, "P5 did not yield z0 quadratic", r5))

    out = {
        "component": cid,
        "mask": mask,
        "p3": str(p3),
        "q3": str(q3),
        "z2z3_phase": str(alpha),
        "z1z8_phase": str(beta),
        "p5_reduced": str(r5),
        "validated": True,
    }
    print(out, flush=True)
    print(
        "RESULT: five local relations validated directly from exact pentagon entries for mask",
        mask,
        flush=True,
    )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, choices=tuple(fa.REL), required=True)
    args = ap.parse_args()
    audit(args.component, args.mask)


if __name__ == "__main__":
    main()
