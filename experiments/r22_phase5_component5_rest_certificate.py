"""Exact local certificates for component-5 masks 150 and 255 rank-drop strata.

Both masks have the same finite-stratum census as the already-closed masks:
10 rank-11 branches are killed by the first diagnostic cells and 8 rank-10
branches remain at (a,b)=(1,1),(2,1),(1,2),(2,2), for both z0 roots.

Mask 150 reproduces the mask-105 local models:
- off diagonal cube pairs close with G0,G2;
- diagonal cube pairs close with G0,G2,G3.

Mask 255 has a different but equally short local geometry:
- off diagonal G0,G1 have resultant 48*y^4, so their common zero forces
  x=y=0, contradicting the nonzero constant in G2;
- diagonal i*G3-G2 = 4*(1+i)*(x-y)*(x+y); each sign branch makes G0 a
  nonzero scalar times y^2, while G2 excludes y=0.

No global solve or Groebner basis is used.
"""
from __future__ import annotations

import argparse

import sympy as sp

import r22_phase5_component5_rest_audit as fa
import r22_phase5_ratio_classes as rc

X = rc.ZS[18]  # z19
Y = rc.ZS[19]  # z20
SQ3 = sp.sqrt(3)
EXT = [sp.I, SQ3, sp.sqrt(6)]

G0 = (("X", "X", "X", "X", "g"), (0, 0))
G1 = (("X", "X", "X", "X", "g"), (0, 1))
G2 = (("X", "X", "X", "X", "g"), (0, 2))
G3 = (("X", "X", "X", "X", "g"), (0, 3))

M150_G2 = 4*X*Y - 4*Y**2 - 1
M150_G3 = 4*X**2 - 4*X*Y + 1
M150_OFF_G0 = (X - Y)**2
M150_G0_11 = (SQ3 + sp.I)*(X**2 + Y**2) + 4*sp.I*X*Y
M150_G0_22 = (SQ3 - sp.I)*(X**2 + Y**2) - 4*sp.I*X*Y

M255_G2 = 4*(1-sp.I)*X*Y + 4*(1+sp.I)*Y**2 + sp.I
M255_G3 = 4*(1-sp.I)*X**2 - 4*(1+sp.I)*X*Y + 1
M255_OFF_G0 = (X-Y)*(X + (1+2*sp.I)*Y)
M255_OFF_G1 = (X+Y)*((1-2*sp.I)*X - Y)
M255_G0_11 = (
    (SQ3 + sp.I)*X**2
    + (-2 + 2*SQ3*sp.I)*X*Y
    + (-SQ3 - 4 - sp.I)*Y**2
)
M255_G0_22 = (
    (SQ3 - sp.I)*X**2
    + (2 + 2*SQ3*sp.I)*X*Y
    + (-SQ3 + 4 + sp.I)*Y**2
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


def affine_case(unique, reduced, mask, a, b, root):
    rel = fa.REL[mask]
    p = sp.expand(rel["P0"] * fa.OMEGA**a)
    q = sp.expand(rel["Q0"] * fa.OMEGA**b)
    t = fa.ROOTS[root]
    affine, exprs = rc.affine_closure(unique, reduced, p, q, t)
    if exprs is None or not affine.get("consistent"):
        raise AssertionError((mask, a, b, root, "expected consistent rank-drop branch", affine))
    if affine["rank"] != 10 or affine["free_dimension"] != 10:
        raise AssertionError((mask, a, b, root, "unexpected affine profile", affine))
    return rel, p, q, t, affine, exprs


def certify_150(unique, reduced, by_prov, a, b, root):
    rel, p, q, t, affine, exprs = affine_case(unique, reduced, 150, a, b, root)
    g0 = remainder(reduced, by_prov, exprs, p, q, t, rel, G0)
    g2 = remainder(reduced, by_prov, exprs, p, q, t, rel, G2)
    g3 = remainder(reduced, by_prov, exprs, p, q, t, rel, G3)
    assert_proportional(g2, M150_G2, (150,a,b,root,"G2"))
    assert_proportional(g3, M150_G3, (150,a,b,root,"G3"))

    if (a,b) in {(2,1),(1,2)}:
        assert_proportional(g0, M150_OFF_G0, (150,a,b,root,"G0"))
        if sp.expand(M150_G2.subs(X,Y)) != -1:
            raise AssertionError("mask150 offdiag collapse failed")
        cert = {"type":"two-cell", "cells":(G0,G2), "derived":"x=y, then -1=0"}
    else:
        model = M150_G0_11 if (a,b)==(1,1) else M150_G0_22
        assert_proportional(g0, model, (150,a,b,root,"G0"))
        relation = sp.factor(M150_G2 + M150_G3)
        if sp.expand(relation - 4*(X-Y)*(X+Y)) != 0:
            raise AssertionError(("mask150 sign relation", relation))
        if sp.expand(M150_G2.subs(X,Y)) != -1:
            raise AssertionError("mask150 x=y branch should contradict G2")
        opp = sp.expand(M150_G2.subs(X,-Y))
        if opp != -8*Y**2-1:
            raise AssertionError(("mask150 x=-y relation", opp))
        gy = sp.Poly(sp.expand(model.subs(X,-Y)), Y, extension=EXT)
        modulus = sp.Poly(8*Y**2+1, Y, extension=EXT)
        final = sp.simplify(gy.rem(modulus).as_expr())
        if final == 0:
            raise AssertionError((150,a,b,root,"G0 vanished on x=-y branch"))
        cert = {"type":"three-cell", "cells":(G0,G2,G3), "derived":"x=-y, y^2=-1/8", "final":str(final)}

    return {"mask":150,"a":a,"b":b,"root":root,"affine_rank":affine["rank"],"certificate":cert,"closed":True}


def certify_255(unique, reduced, by_prov, a, b, root):
    rel, p, q, t, affine, exprs = affine_case(unique, reduced, 255, a, b, root)
    g0 = remainder(reduced, by_prov, exprs, p, q, t, rel, G0)
    g1 = remainder(reduced, by_prov, exprs, p, q, t, rel, G1)
    g2 = remainder(reduced, by_prov, exprs, p, q, t, rel, G2)
    g3 = remainder(reduced, by_prov, exprs, p, q, t, rel, G3)
    assert_proportional(g2, M255_G2, (255,a,b,root,"G2"))
    assert_proportional(g3, M255_G3, (255,a,b,root,"G3"))

    if (a,b) in {(2,1),(1,2)}:
        assert_proportional(g0, M255_OFF_G0, (255,a,b,root,"G0"))
        assert_proportional(g1, M255_OFF_G1, (255,a,b,root,"G1"))
        res = sp.factor(sp.resultant(M255_OFF_G0, M255_OFF_G1, X))
        if sp.expand(res - 48*Y**4) != 0:
            raise AssertionError((255,a,b,root,"unexpected offdiag resultant",res))
        if sp.expand(M255_OFF_G0.subs(Y,0)) != X**2:
            raise AssertionError("mask255 resultant follow-up failed")
        if sp.expand(M255_G2.subs({X:0,Y:0})) != sp.I:
            raise AssertionError("mask255 G2 constant check failed")
        cert = {"type":"three-cell", "cells":(G0,G1,G2), "derived":"Res_x(G0,G1)=48*y^4 => y=0 => x=0; G2=i"}
    else:
        model = M255_G0_11 if (a,b)==(1,1) else M255_G0_22
        assert_proportional(g0, model, (255,a,b,root,"G0"))
        relation = sp.factor(sp.I*M255_G3 - M255_G2)
        target = 4*(1+sp.I)*(X-Y)*(X+Y)
        if sp.expand(relation-target) != 0:
            raise AssertionError((255,a,b,root,"unexpected diagonal sign relation",relation))
        # G2(0,0)=i proves y cannot vanish on either x=+/-y branch.
        if sp.expand(M255_G2.subs({X:0,Y:0})) != sp.I:
            raise AssertionError("mask255 y-nonzero check failed")
        same_coeff = sp.simplify(model.subs(X,Y)/Y**2)
        opp_coeff = sp.simplify(model.subs(X,-Y)/Y**2)
        if same_coeff == 0 or opp_coeff == 0:
            raise AssertionError((255,a,b,root,"G0 coefficient vanished",same_coeff,opp_coeff))
        cert = {
            "type":"three-cell",
            "cells":(G0,G2,G3),
            "derived":"i*G3-G2=4*(1+i)*(x-y)*(x+y); G0 nonzero on both signs",
            "same_sign_G0_coefficient":str(same_coeff),
            "opposite_sign_G0_coefficient":str(opp_coeff),
        }

    return {"mask":255,"a":a,"b":b,"root":root,"affine_rank":affine["rank"],"certificate":cert,"closed":True}


def audit_mask(cid, mask):
    unique, reduced, by_prov = fa.compile_once(cid, mask)
    rows=[]
    for a,b in ((1,1),(2,1),(1,2),(2,2)):
        for root in ("positive","negative"):
            row = certify_150(unique,reduced,by_prov,a,b,root) if mask==150 else certify_255(unique,reduced,by_prov,a,b,root)
            rows.append(row)
            print(row, flush=True)
    if len(rows)!=8 or not all(r["closed"] for r in rows):
        raise AssertionError((mask,"rank-drop closure incomplete"))
    summary={"component":cid,"mask":mask,"closed":8,"total":8,"certificate_types":{t:sum(r["certificate"]["type"]==t for r in rows) for t in {r["certificate"]["type"] for r in rows}}}
    print("SUMMARY",summary,flush=True)
    print("RESULT: all eight rank-drop finite branches are excluded for mask",mask,flush=True)
    return summary


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--component",type=int,default=5)
    ap.add_argument("--mask",type=int,choices=(150,255),action="append")
    args=ap.parse_args()
    masks=args.mask or [150,255]
    rows=[audit_mask(args.component,m) for m in masks]
    print("GLOBAL",{"masks":masks,"closed":sum(r["closed"] for r in rows),"total":sum(r["total"] for r in rows)},flush=True)


if __name__=="__main__":
    main()
