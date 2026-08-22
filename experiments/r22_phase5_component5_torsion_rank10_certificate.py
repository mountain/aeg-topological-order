"""Exact rank-10 Phase-5 certificates for component 5 / mask 0 / D class 1.

The fresh finite census leaves eight rank-10 branches at
(a,b)=(1,1),(2,1),(1,2),(2,2), for both roots of z0.

After the class-1 affine quotient, four fixed local g-cells reduce, up to
nonzero branch scalars, to a small two-variable model in

    x = z19, y = z20.

The source remainders are recomputed for every branch and explicitly checked to
be proportional to the models below.  No conclusion is imported from the
historical D sheet.
"""
from __future__ import annotations

import argparse

import sympy as sp

import r22_phase5_component5_rest_audit as fa
import r22_phase5_component5_torsion_finite_audit as tf
import r22_phase5_ratio_classes as rc
import r22_phase5_torsion_sheet as ts

X = rc.ZS[18]  # z19
Y = rc.ZS[19]  # z20
SQ3 = sp.sqrt(3)
EXT = [sp.I, SQ3, sp.sqrt(6)]

G0 = (("X", "X", "X", "X", "g"), (0, 0))
G1 = (("X", "X", "X", "X", "g"), (0, 1))
G2 = (("X", "X", "X", "X", "g"), (0, 2))
G3 = (("X", "X", "X", "X", "g"), (0, 3))

# Universal rank-10 models on class 1 / mask 0.
M2 = 4*(1-sp.I)*X*Y - 4*(1+sp.I)*Y**2 - 1
M3 = 4*(1-sp.I)*X**2 + 4*(1+sp.I)*X*Y - sp.I

OFF_G0 = (X-Y)*(X + (1-2*sp.I)*Y)
OFF_G1 = (X+Y)*((2-sp.I)*X + sp.I*Y)

DIAG_G0_11 = (
    (SQ3+sp.I)*X**2
    + (2-2*SQ3*sp.I)*X*Y
    + (4-SQ3-sp.I)*Y**2
)
DIAG_G0_22 = (
    (SQ3-sp.I)*X**2
    + (-2-2*SQ3*sp.I)*X*Y
    + (-SQ3-4+sp.I)*Y**2
)


def monic(expr):
    p = sp.Poly(sp.expand(expr), X, Y, extension=EXT)
    if p.is_zero:
        raise AssertionError("unexpected zero polynomial")
    return sp.Poly(p.monic().as_expr(), X, Y, extension=EXT)


def assert_proportional(expr, model, label):
    if monic(expr) != monic(model):
        raise AssertionError((label, "not proportional", monic(expr).as_expr(), monic(model).as_expr()))


def remainder(reduced, by_prov, exprs, p, q, t, rel, prov):
    key = by_prov[prov]
    spoly = rc.specialize_reduced(reduced[key], p, q, t)
    expr = rc.zpoly_expr(spoly)
    return sp.factor(sp.cancel(fa.substitute_closure(expr, exprs, p, q, t, rel)))


def affine_case(unique, reduced, a, b, root):
    rel = fa.REL[0]
    p = sp.expand(rel["P0"] * fa.OMEGA**a)
    q = sp.expand(rel["Q0"] * fa.OMEGA**b)
    t = fa.ROOTS[root]
    affine, exprs = rc.affine_closure(unique, reduced, p, q, t)
    if exprs is None or not affine.get("consistent"):
        raise AssertionError((a, b, root, "expected consistent rank-10 branch", affine))
    if affine["rank"] != 10 or affine["free_dimension"] != 10 or affine["forced_zero"]:
        raise AssertionError((a, b, root, "unexpected affine profile", affine))
    return rel, p, q, t, affine, exprs


def certify(unique, reduced, by_prov, a, b, root):
    rel, p, q, t, affine, exprs = affine_case(unique, reduced, a, b, root)
    g0 = remainder(reduced, by_prov, exprs, p, q, t, rel, G0)
    g1 = remainder(reduced, by_prov, exprs, p, q, t, rel, G1)
    g2 = remainder(reduced, by_prov, exprs, p, q, t, rel, G2)
    g3 = remainder(reduced, by_prov, exprs, p, q, t, rel, G3)

    assert_proportional(g2, M2, (a,b,root,"G2"))
    assert_proportional(g3, M3, (a,b,root,"G3"))

    if (a,b) in {(2,1),(1,2)}:
        assert_proportional(g0, OFF_G0, (a,b,root,"G0"))
        assert_proportional(g1, OFF_G1, (a,b,root,"G1"))
        res = sp.factor(sp.resultant(OFF_G0, OFF_G1, X))
        if sp.expand(res + 48*Y**4) != 0:
            raise AssertionError((a,b,root,"unexpected resultant",res))
        if sp.expand(OFF_G0.subs(Y,0) - X**2) != 0:
            raise AssertionError((a,b,root,"offdiag y=0 followup failed"))
        if sp.expand(M2.subs({X:0,Y:0})) != -1:
            raise AssertionError((a,b,root,"G2 constant check failed"))
        cert = {
            "type":"three-cell-plus-resultant",
            "cells":(G0,G1,G2),
            "derived":"Res_x(G0,G1)=-48*y^4 => y=0 => x=0; G2=-1",
        }
    else:
        model = DIAG_G0_11 if (a,b)==(1,1) else DIAG_G0_22
        assert_proportional(g0, model, (a,b,root,"G0"))
        relation = sp.factor(M3 - sp.I*M2)
        target = 4*(1-sp.I)*(X-Y)*(X+Y)
        if sp.expand(relation-target) != 0:
            raise AssertionError((a,b,root,"unexpected sign relation",relation))
        if sp.expand(M2.subs({X:0,Y:0})) != -1:
            raise AssertionError((a,b,root,"origin check failed"))
        same = sp.simplify(model.subs(X,Y)/Y**2)
        opp = sp.simplify(model.subs(X,-Y)/Y**2)
        if same == 0 or opp == 0:
            raise AssertionError((a,b,root,"diagonal G0 coefficient vanished",same,opp))
        cert = {
            "type":"three-cell-sign-split",
            "cells":(G0,G2,G3),
            "derived":"G3-i*G2=4*(1-i)*(x-y)*(x+y); y!=0 from G2; G0 nonzero on both signs",
            "same_sign_G0_coefficient":str(same),
            "opposite_sign_G0_coefficient":str(opp),
        }

    return {
        "component":5,
        "mask":0,
        "D_amplitude_class":1,
        "a":a,"b":b,"root":root,
        "affine_rank":affine["rank"],
        "certificate":cert,
        "closed":True,
    }


def audit(cid=5):
    old = fa.REL.get(0)
    fa.REL[0] = tf.relation(0)
    try:
        with ts.second_sheet_provider():
            unique, reduced, by_prov = fa.compile_once(cid, 0)
            rows=[]
            for a,b in ((1,1),(2,1),(1,2),(2,2)):
                for root in ("positive","negative"):
                    row=certify(unique,reduced,by_prov,a,b,root)
                    rows.append(row)
                    print(row,flush=True)
    finally:
        if old is None:
            fa.REL.pop(0,None)
        else:
            fa.REL[0]=old

    if len(rows)!=8 or not all(r["closed"] for r in rows):
        raise AssertionError("rank-10 class-1 closure incomplete")
    types={t:sum(r["certificate"]["type"]==t for r in rows) for t in {r["certificate"]["type"] for r in rows}}
    summary={"component":cid,"mask":0,"D_amplitude_class":1,"closed":8,"total":8,"certificate_types":types}
    print("SUMMARY",summary,flush=True)
    print("RESULT: all eight component-5 mask-0 class-1 rank-10 strata are excluded",flush=True)
    return summary


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--component",type=int,default=5)
    args=ap.parse_args()
    audit(args.component)


if __name__=="__main__":
    main()
