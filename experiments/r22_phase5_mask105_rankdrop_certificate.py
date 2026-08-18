"""Exact local certificate closing the eight rank-drop Phase-5 strata of
component 5 / chirality mask 105.

The finite audit leaves exactly

    (a,b) in {(1,1),(2,1),(1,2),(2,2)}

for both roots of 2*z0^2+4*z0-1=0.  Each has affine rank 10.  This script
rebuilds every branch independently and checks the three relevant final
pentagon cells

    G0 = (X,X,X,X;g)_(0,0),
    G2 = (X,X,X,X;g)_(0,2),
    G3 = (X,X,X,X;g)_(0,3).

For (2,1) and (1,2), G0 is a nonzero scalar times (z19-z20)^2, while G2 is a
nonzero scalar times 4*z19*z20-4*z20^2-1.  Thus G0=0 forces z19=z20 and G2
becomes -1=0.

For (1,1) and (2,2), G2 and G3 imply

    (z19-z20)(z19+z20)=0.

The z19=z20 branch again contradicts G2.  Hence z19=-z20; then G2 gives
z20^2=-1/8.  Substitution into G0 leaves a nonzero algebraic constant.

No Groebner basis or global solve is used.  The script verifies every claimed
proportionality and nonzero constant exactly over Q(i,sqrt(3),sqrt(6)).
"""
from __future__ import annotations

import argparse

import sympy as sp

import r22_phase5_mask105_finite_audit as fa
import r22_phase5_ratio_classes as rc


X = rc.ZS[18]   # z19
Y = rc.ZS[19]   # z20
SQ3 = sp.sqrt(3)
SQ6 = sp.sqrt(6)
EXT = [sp.I, SQ3, SQ6]

G0_PROV = (("X", "X", "X", "X", "g"), (0, 0))
G2_PROV = (("X", "X", "X", "X", "g"), (0, 2))
G3_PROV = (("X", "X", "X", "X", "g"), (0, 3))

G2_MODEL = 4*X*Y - 4*Y**2 - 1
G3_MODEL = 4*X**2 - 4*X*Y + 1
G0_OFFDIAG = (X - Y)**2
G0_11 = (SQ3 + sp.I)*(X**2 + Y**2) + 4*sp.I*X*Y
G0_22 = (SQ3 - sp.I)*(X**2 + Y**2) - 4*sp.I*X*Y


def monic(expr):
    p = sp.Poly(sp.expand(expr), X, Y, extension=EXT)
    if p.is_zero:
        raise AssertionError("unexpected zero polynomial")
    return sp.Poly(p.monic().as_expr(), X, Y, extension=EXT)


def assert_proportional(expr, model, label):
    a = monic(expr)
    b = monic(model)
    if a != b:
        raise AssertionError((label, "not proportional", a.as_expr(), b.as_expr()))


def target_remainder(reduced, by_prov, exprs, p, q, t, prov):
    key = by_prov[prov]
    spoly = rc.specialize_reduced(reduced[key], p, q, t)
    expr = rc.zpoly_expr(spoly)
    return sp.factor(sp.cancel(fa.substitute_closure(expr, exprs, p, q, t)))


def certify_case(unique, reduced, by_prov, a, b, root_name):
    p = sp.expand(fa.P0 * fa.OMEGA**a)
    q = sp.expand(fa.Q0 * fa.OMEGA**b)
    t = fa.ROOTS[root_name]
    affine, exprs = rc.affine_closure(unique, reduced, p, q, t)
    if exprs is None or not affine.get("consistent"):
        raise AssertionError((a, b, root_name, "expected consistent rank-drop affine closure", affine))
    if affine["rank"] != 10 or affine["free_dimension"] != 10:
        raise AssertionError((a, b, root_name, "unexpected affine rank", affine))

    g0 = target_remainder(reduced, by_prov, exprs, p, q, t, G0_PROV)
    g2 = target_remainder(reduced, by_prov, exprs, p, q, t, G2_PROV)
    g3 = target_remainder(reduced, by_prov, exprs, p, q, t, G3_PROV)

    assert_proportional(g2, G2_MODEL, (a, b, root_name, "G2"))
    assert_proportional(g3, G3_MODEL, (a, b, root_name, "G3"))

    if (a, b) in {(2, 1), (1, 2)}:
        assert_proportional(g0, G0_OFFDIAG, (a, b, root_name, "G0"))
        # G0=0 => X=Y over C.  G2 then is exactly -1.
        collapsed = sp.expand(G2_MODEL.subs(X, Y))
        if collapsed != -1:
            raise AssertionError((a, b, root_name, "off-diagonal collapse", collapsed))
        certificate = {
            "type": "two-cell",
            "cells": (G0_PROV, G2_PROV),
            "derived": "z19=z20, then -1=0",
        }
    else:
        model = G0_11 if (a, b) == (1, 1) else G0_22
        assert_proportional(g0, model, (a, b, root_name, "G0"))

        # G2+G3 = 4*(X-Y)*(X+Y).  The X=Y branch contradicts G2,
        # so any common zero must have X=-Y.
        factor_relation = sp.factor(G2_MODEL + G3_MODEL)
        if sp.expand(factor_relation - 4*(X-Y)*(X+Y)) != 0:
            raise AssertionError((a, b, root_name, "factor relation", factor_relation))
        same_branch = sp.expand(G2_MODEL.subs(X, Y))
        if same_branch != -1:
            raise AssertionError((a, b, root_name, "same-sign branch", same_branch))

        opposite = sp.expand(G2_MODEL.subs(X, -Y))
        if opposite != -8*Y**2 - 1:
            raise AssertionError((a, b, root_name, "opposite branch", opposite))

        # On X=-Y and 8*Y^2+1=0, G0 must still be nonzero.
        gy = sp.Poly(sp.expand(model.subs(X, -Y)), Y, extension=EXT)
        modulus = sp.Poly(8*Y**2 + 1, Y, extension=EXT)
        rem = gy.rem(modulus).as_expr()
        rem = sp.simplify(rem)
        if rem == 0:
            raise AssertionError((a, b, root_name, "G0 vanished on derived branch"))
        certificate = {
            "type": "three-cell",
            "cells": (G0_PROV, G2_PROV, G3_PROV),
            "derived": "z19=-z20, z20^2=-1/8",
            "final_nonzero_constant": str(rem),
        }

    out = {
        "a": a,
        "b": b,
        "root": root_name,
        "ratio_class": (a-b) % 3,
        "affine_rank": affine["rank"],
        "certificate": certificate,
        "g0": str(g0),
        "g2": str(g2),
        "g3": str(g3),
        "closed": True,
    }
    print(out, flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=105)
    args = ap.parse_args()
    if args.mask != 105:
        raise ValueError("mask-105-specific certificate")

    unique, reduced, by_prov = fa.compile_once(args.component, args.mask)
    rows = []
    for a, b in ((1,1), (2,1), (1,2), (2,2)):
        for root in ("positive", "negative"):
            rows.append(certify_case(unique, reduced, by_prov, a, b, root))

    if len(rows) != 8 or not all(r["closed"] for r in rows):
        raise AssertionError("not all eight rank-drop branches closed")
    print("SUMMARY", {"closed": 8, "total": 8, "two_cell": 4, "three_cell": 4}, flush=True)
    print("RESULT: all eight mask-105 rank-drop finite branches are excluded by <=3 local g-cells", flush=True)


if __name__ == "__main__":
    main()
