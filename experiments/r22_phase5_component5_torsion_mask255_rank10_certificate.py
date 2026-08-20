"""Exact rank-10 Phase-5 certificates for component 5 / mask 255 / D class 1.

The fresh class-1 finite census leaves exactly eight rank-10 strata at
(a,b)=(1,1),(2,1),(1,2),(2,2), for both roots of the z0 quadratic.
This verifier recompiles the second D sheet and validates four fixed source
cells in the residual variables x=z19, y=z20.

Common models (up to nonzero branch scalars):

    C = (4-4i)xy + (4+4i)y^2 + i,
    D = (4-4i)x^2 - (4+4i)xy + 1.

For off-diagonal cube pairs, G0 and G1 factor and have resultant -48*y^4,
forcing x=y=0, which contradicts C(0,0)=i.

For diagonal cube pairs, C-iD=-4(1+i)(x-y)(x+y).  The two sign slices are
x=y with y^2=-i/8 and x=-y with y^2=-1/8; source cell G0 has a nonzero
y^2 coefficient on both slices.

No Groebner basis, numerical solve, or imported class-0 branch verdict is used.
"""
from __future__ import annotations

import sympy as sp

import r22_phase5_component5_rest_audit as fa
import r22_phase5_component5_torsion_finite_audit as tf
import r22_phase5_ratio_classes as rc
import r22_phase5_torsion_sheet as ts

X = rc.ZS[18]
Y = rc.ZS[19]
SQ3 = sp.sqrt(3)
EXT = [sp.I, SQ3, sp.sqrt(6)]

G0 = (("X", "X", "X", "X", "g"), (0, 0))
G1 = (("X", "X", "X", "X", "g"), (0, 1))
G2 = (("X", "X", "X", "X", "g"), (0, 2))
G3 = (("X", "X", "X", "X", "g"), (0, 3))

C = (4-4*sp.I)*X*Y + (4+4*sp.I)*Y**2 + sp.I
D = (4-4*sp.I)*X**2 - (4+4*sp.I)*X*Y + 1

OFF_G0 = (X+Y)*(X+(-1+2*sp.I)*Y)
OFF_G1 = (X-Y)*((2-sp.I)*X-sp.I*Y)

DIAG_G0_11 = (
    (SQ3+sp.I)*X**2
    + (-2+2*SQ3*sp.I)*X*Y
    + (4-SQ3-sp.I)*Y**2
)
DIAG_G0_22 = (
    (SQ3-sp.I)*X**2
    + (2+2*SQ3*sp.I)*X*Y
    + (-4-SQ3+sp.I)*Y**2
)

PAIRS = ((1,1),(2,1),(1,2),(2,2))
ROOTS = ("positive","negative")


def monic(expr):
    p = sp.Poly(sp.expand(expr), X, Y, extension=EXT)
    if p.is_zero:
        raise AssertionError("unexpected zero polynomial")
    return sp.Poly(p.monic().as_expr(), X, Y, extension=EXT)


def assert_proportional(expr, model, label):
    pe = monic(expr)
    pm = monic(model)
    if pe != pm:
        raise AssertionError((label, "not proportional", pe.as_expr(), pm.as_expr()))


def remainder(reduced, by_prov, exprs, p, q, t, rel, prov):
    key = by_prov[prov]
    spoly = rc.specialize_reduced(reduced[key], p, q, t)
    expr = rc.zpoly_expr(spoly)
    return sp.factor(sp.cancel(fa.substitute_closure(expr, exprs, p, q, t, rel)))


def affine_case(unique, reduced, a, b, root):
    rel = fa.REL[255]
    p = sp.expand(rel["P0"] * fa.OMEGA**a)
    q = sp.expand(rel["Q0"] * fa.OMEGA**b)
    t = fa.ROOTS[root]
    affine, exprs = rc.affine_closure(unique, reduced, p, q, t)
    if exprs is None or not affine.get("consistent"):
        raise AssertionError((a,b,root,"expected consistent rank-10 branch",affine))
    if affine["rank"] != 10 or affine["free_dimension"] != 10 or affine["forced_zero"]:
        raise AssertionError((a,b,root,"unexpected affine profile",affine))
    return rel,p,q,t,affine,exprs


def certify(unique, reduced, by_prov, a, b, root):
    rel,p,q,t,affine,exprs = affine_case(unique,reduced,a,b,root)
    g0 = remainder(reduced,by_prov,exprs,p,q,t,rel,G0)
    g1 = remainder(reduced,by_prov,exprs,p,q,t,rel,G1)
    g2 = remainder(reduced,by_prov,exprs,p,q,t,rel,G2)
    g3 = remainder(reduced,by_prov,exprs,p,q,t,rel,G3)

    assert_proportional(g2,C,(a,b,root,"G2"))
    assert_proportional(g3,D,(a,b,root,"G3"))

    if (a,b) in {(2,1),(1,2)}:
        assert_proportional(g0,OFF_G0,(a,b,root,"G0"))
        assert_proportional(g1,OFF_G1,(a,b,root,"G1"))
        res = sp.factor(sp.resultant(OFF_G0,OFF_G1,X))
        if sp.expand(res + 48*Y**4) != 0:
            raise AssertionError((a,b,root,"unexpected resultant",res))
        if sp.expand(OFF_G0.subs(Y,0)-X**2) != 0:
            raise AssertionError((a,b,root,"y=0 followup failed"))
        if sp.expand(C.subs({X:0,Y:0})) != sp.I:
            raise AssertionError((a,b,root,"C origin check failed"))
        cert = {
            "type":"three-cell-resultant",
            "cells":(G0,G1,G2),
            "derived":"Res_x(G0,G1)=-48*y^4 => y=0 => x=0; G2=i",
        }
    else:
        model = DIAG_G0_11 if (a,b)==(1,1) else DIAG_G0_22
        assert_proportional(g0,model,(a,b,root,"G0"))
        relation = sp.factor(C-sp.I*D)
        target = -4*(1+sp.I)*(X-Y)*(X+Y)
        if sp.expand(relation-target) != 0:
            raise AssertionError((a,b,root,"unexpected sign relation",relation))

        same_c = sp.factor(C.subs(X,Y))
        opp_c = sp.factor(C.subs(X,-Y))
        if sp.expand(same_c-(8*Y**2+sp.I)) != 0:
            raise AssertionError((a,b,root,"x=y C relation",same_c))
        if sp.expand(opp_c-sp.I*(8*Y**2+1)) != 0:
            raise AssertionError((a,b,root,"x=-y C relation",opp_c))

        same_coeff = sp.simplify(model.subs(X,Y)/Y**2)
        opp_coeff = sp.simplify(model.subs(X,-Y)/Y**2)
        if same_coeff == 0 or opp_coeff == 0:
            raise AssertionError((a,b,root,"G0 sign coefficient vanished",same_coeff,opp_coeff))
        same_value = sp.simplify(same_coeff * (-sp.I/8))
        opp_value = sp.simplify(opp_coeff * (-sp.Rational(1,8)))
        if same_value == 0 or opp_value == 0:
            raise AssertionError((a,b,root,"G0 sign value vanished",same_value,opp_value))
        cert = {
            "type":"three-cell-sign-split",
            "cells":(G0,G2,G3),
            "derived":"G2-i*G3=-4*(1+i)*(x-y)*(x+y)",
            "x_eq_y_y2":"-i/8",
            "x_eq_minus_y_y2":"-1/8",
            "G0_on_x_eq_y":str(same_value),
            "G0_on_x_eq_minus_y":str(opp_value),
        }

    return {
        "component":5,
        "mask":255,
        "D_amplitude_class":1,
        "a":a,"b":b,"root":root,
        "affine_rank":affine["rank"],
        "certificate":cert,
        "closed":True,
    }


def main():
    cid=5
    mask=255
    rel=tf.relation(mask)
    old=fa.REL.get(mask)
    fa.REL[mask]=rel
    try:
        with ts.second_sheet_provider():
            unique,reduced,by_prov=fa.compile_once(cid,mask)
            missing=[p for p in (G0,G1,G2,G3) if p not in by_prov]
            if missing:
                raise AssertionError(("missing certificate provenance",missing))
            rows=[]
            for a,b in PAIRS:
                for root in ROOTS:
                    row=certify(unique,reduced,by_prov,a,b,root)
                    rows.append(row)
                    print(row,flush=True)
    finally:
        if old is None:
            fa.REL.pop(mask,None)
        else:
            fa.REL[mask]=old

    if len(rows)!=8 or not all(r["closed"] for r in rows):
        raise AssertionError("mask255 rank-10 closure incomplete")
    types={t:sum(r["certificate"]["type"]==t for r in rows) for t in {r["certificate"]["type"] for r in rows}}
    summary={"component":5,"mask":255,"D_amplitude_class":1,"closed":8,"total":8,"certificate_types":types}
    print("SUMMARY",summary,flush=True)
    print("RESULT: all eight mask-255 class-1 rank-10 strata are excluded by fixed local source certificates",flush=True)


if __name__=="__main__":
    main()
