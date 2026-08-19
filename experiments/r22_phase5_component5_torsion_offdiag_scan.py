"""Exact residual-cell scan for component 5 / D class 1 rank-10 off-diagonal strata.

The finite census for mask 105 leaves the off-diagonal cube pairs
(a,b)=(2,1),(1,2), for both roots of the z0 quadratic.  The four neighboring
g-cells imply, on these branches,

    x=z19=-z20=-y,   y^2=-1/8.

This probe does not solve the residual nonlinear system.  It substitutes only
those already-derived exact relations into every source-provenance equation in
the 219-polynomial kernel and searches for a remaining equation that becomes a
nonzero Laurent monomial in the proved-nonzero scale variables z1,z2.

Both exact signs y=+/- i*sqrt(2)/4 are audited separately.  A provenance common
to all eight sign/root/cube subbranches is the preferred next local certificate.
"""
from __future__ import annotations

import argparse
from collections import defaultdict

import sympy as sp

import r22_phase5_component5_rest_audit as fa
import r22_phase5_component5_torsion_finite_audit as tf
import r22_phase5_ratio_classes as rc
import r22_phase5_torsion_sheet as ts

X = rc.ZS[18]  # z19
Y = rc.ZS[19]  # z20
Z1 = rc.ZS[0]
Z2 = rc.ZS[1]
SQ2 = sp.sqrt(2)
SQ3 = sp.sqrt(3)
SQ6 = sp.sqrt(6)
EXT = [sp.I, SQ2, SQ3, SQ6]


def is_nonzero_scale_laurent(expr):
    expr = sp.cancel(expr)
    if expr == 0:
        return False
    num, den = sp.fraction(expr)
    if (num.free_symbols | den.free_symbols) - {Z1, Z2}:
        return False
    try:
        pn = sp.Poly(sp.expand(num), Z1, Z2, extension=EXT)
        pd = sp.Poly(sp.expand(den), Z1, Z2, extension=EXT)
    except Exception:
        return False
    return (
        not pn.is_zero
        and not pd.is_zero
        and len(pn.terms()) == 1
        and len(pd.terms()) == 1
    )


def branch_data(unique, reduced, mask, a, b, root):
    rel = fa.REL[mask]
    p = sp.expand(rel["P0"] * fa.OMEGA**a)
    q = sp.expand(rel["Q0"] * fa.OMEGA**b)
    t = fa.ROOTS[root]
    affine, exprs = rc.affine_closure(unique, reduced, p, q, t)
    if exprs is None or not affine.get("consistent"):
        raise AssertionError((mask, a, b, root, "expected consistent branch", affine))
    if affine["rank"] != 10 or affine["free_dimension"] != 10:
        raise AssertionError((mask, a, b, root, "unexpected affine profile", affine))
    return rel, p, q, t, affine, exprs


def source_remainder(key, reduced, exprs, p, q, t, rel):
    spoly = rc.specialize_reduced(reduced[key], p, q, t)
    expr = rc.zpoly_expr(spoly)
    return sp.factor(sp.cancel(fa.substitute_closure(expr, exprs, p, q, t, rel)))


def scan(cid: int, mask: int):
    if mask not in (105, 150, 255):
        raise ValueError("scan is intended for the remaining class-1 component-5 masks")

    old = fa.REL.get(mask)
    fa.REL[mask] = tf.relation(mask)
    branch_candidates = {}
    branch_exprs = {}
    try:
        with ts.second_sheet_provider():
            unique, reduced, _by_prov = fa.compile_once(cid, mask)
            for a, b in ((2, 1), (1, 2)):
                for root in ("positive", "negative"):
                    rel, p, q, t, affine, exprs = branch_data(unique, reduced, mask, a, b, root)
                    for sign in (+1, -1):
                        yval = sign * sp.I * SQ2 / 4
                        key_branch = (a, b, root, sign)
                        rows = []
                        emap = {}
                        for key, prov in unique.items():
                            rem = source_remainder(key, reduced, exprs, p, q, t, rel)
                            rem2 = sp.factor(sp.cancel(rem.subs({X: -yval, Y: yval})))
                            if is_nonzero_scale_laurent(rem2):
                                complexity = int(sp.count_ops(rem2))
                                rows.append((complexity, len(str(rem2)), str(prov), prov, rem2))
                                emap[prov] = rem2
                        rows.sort(key=lambda r: (r[0], r[1], r[2]))
                        branch_candidates[key_branch] = {r[3] for r in rows}
                        branch_exprs[key_branch] = emap
                        print({
                            "mask": mask,
                            "a": a,
                            "b": b,
                            "root": root,
                            "sign": sign,
                            "affine_rank": affine["rank"],
                            "candidate_count": len(rows),
                            "best": [
                                {"provenance": r[3], "remainder": str(r[4]), "ops": r[0]}
                                for r in rows[:8]
                            ],
                        }, flush=True)
    finally:
        if old is None:
            fa.REL.pop(mask, None)
        else:
            fa.REL[mask] = old

    common = set.intersection(*branch_candidates.values()) if branch_candidates else set()
    common_rows = []
    for prov in common:
        expr_list = [branch_exprs[b][prov] for b in sorted(branch_exprs)]
        common_rows.append((
            max(int(sp.count_ops(e)) for e in expr_list),
            sum(len(str(e)) for e in expr_list),
            str(prov),
            prov,
            tuple(str(e) for e in expr_list),
        ))
    common_rows.sort(key=lambda r: (r[0], r[1], r[2]))
    out = {
        "component": cid,
        "mask": mask,
        "D_amplitude_class": 1,
        "sign_subbranches": len(branch_candidates),
        "common_provenance_count": len(common_rows),
        "best_common": [
            {"provenance": r[3], "remainders": r[4], "max_ops": r[0]}
            for r in common_rows[:12]
        ],
    }
    print("SUMMARY", out, flush=True)
    if common_rows:
        print("RESULT: found source provenance obstructing every off-diagonal sign subbranch", flush=True)
    else:
        print("RESULT: no single common source cell; use branchwise candidates or a larger local relation set", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=105)
    args = ap.parse_args()
    scan(args.component, args.mask)


if __name__ == "__main__":
    main()
