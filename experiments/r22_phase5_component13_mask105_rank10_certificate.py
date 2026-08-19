"""Exact three-residual certificates for all eight component-13/mask-105 rank-10 strata.

Every branch is rebuilt independently.  The SAME three fixed residual
provenances are used on all branches:

    P1 = (X,X,X,X;g)_(0,3)
    P2 = (X,X,X,X;g)_(0,2)
    P3 = (X,X,X,X;g)_(0,0)

In the exact affine quotient, P1 and P2 lie in the r=z16,s=z18 core.  Their
sum must factor as s*(a+b*s) with a,b nonzero.  This gives two exact s values;
P1 is affine in r on each value and determines an exact candidate r.  P3 must
then evaluate nonzero at BOTH candidate points.

No branch may substitute a different third equation, and no Groebner basis or
floating-point root search is used.
"""
from __future__ import annotations

import r22_phase5_component13_mask105_rank10_bivariate_probe as bp
import r22_phase5_component13_mask105_residual_scan as rs
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss

CID = 13
MASK = 105
P1 = (("X", "X", "X", "X", "g"), (0, 3))
P2 = (("X", "X", "X", "X", "g"), (0, 2))
P3 = (("X", "X", "X", "X", "g"), (0, 0))
CASES = tuple(
    (a, b, sign)
    for b in (1, 2)
    for a in (1, 2)
    for sign in (1, -1)
)
EXPECTED_FREE = (3, 4, 5, 6, 16, 18, 19, 20)


def exact_poly_by_prov(data, target, rpos, spos):
    key, raw, provs = bp.find_by_prov(data, target)
    p = bp.poly2(raw, rpos, spos)
    if p is None or not p:
        raise AssertionError((target, "not a nonzero bivariate residual", provs))
    return key, p, provs


def certify(unique, aidx, bidx, sign):
    data = rs.build_branch(unique, aidx, bidx, sign)
    if data["free"] != EXPECTED_FREE:
        raise AssertionError((aidx, bidx, sign, "unexpected free variables", data["free"]))
    rpos = data["free"].index(16)
    spos = data["free"].index(18)

    k1, e1, _ = exact_poly_by_prov(data, P1, rpos, spos)
    k2, e2, _ = exact_poly_by_prov(data, P2, rpos, spos)
    _k3, e3, provs3 = exact_poly_by_prov(data, P3, rpos, spos)

    total = bp.p2add(e1, e2)
    forbidden = {m: c for m, c in total.items() if m not in ((0, 1), (0, 2))}
    if forbidden:
        raise AssertionError((aidx, bidx, sign, "P1+P2 unexpected terms", forbidden))
    aa = total.get((0, 1), ss.K0)
    bb = total.get((0, 2), ss.K0)
    if ss.kiszero(aa) or ss.kiszero(bb):
        raise AssertionError((aidx, bidx, sign, "degenerate s factor", ss.kstr(aa), ss.kstr(bb)))
    s_values = (ss.K0, ss.kneg(ss.kdiv(aa, bb)))

    candidates = []
    for s in s_values:
        c0 = ss.K0
        c1 = ss.K0
        for (er, es), c in e1.items():
            term = ss.kmul(c, ss.kpow(s, es))
            if er == 0:
                c0 = ss.kadd(c0, term)
            elif er == 1:
                c1 = ss.kadd(c1, term)
            else:
                raise AssertionError((aidx, bidx, sign, "P1 nonlinear in r", er, es))
        if ss.kiszero(c1):
            raise AssertionError((aidx, bidx, sign, "P1 lost r coefficient", ss.kstr(s)))
        r = ss.kneg(ss.kdiv(c0, c1))
        if not ss.kiszero(bp.eval2(e1, r, s)) or not ss.kiszero(bp.eval2(e2, r, s)):
            raise AssertionError((aidx, bidx, sign, "candidate fails anchors", ss.kstr(r), ss.kstr(s)))
        v3 = bp.eval2(e3, r, s)
        if ss.kiszero(v3):
            raise AssertionError((aidx, bidx, sign, "fixed P3 vanishes at candidate", ss.kstr(r), ss.kstr(s), provs3))
        candidates.append({"r": ss.kstr(r), "s": ss.kstr(s), "P3": ss.kstr(v3)})

    row = {
        "a": aidx,
        "b": bidx,
        "z0_sign": "+" if sign > 0 else "-",
        "anchors": (P1, P2),
        "third": P3,
        "factor": {"s": ss.kstr(aa), "s2": ss.kstr(bb)},
        "candidates": candidates,
        "closed": True,
    }
    print(row, flush=True)
    return row


def main():
    _q, unique = ml.compile_unique(CID, MASK)
    rows = [certify(unique, *case) for case in CASES]
    if len(rows) != 8 or not all(r["closed"] for r in rows):
        raise AssertionError(rows)
    print("SUMMARY", {"closed": 8, "total": 8, "cells": (P1, P2, P3)}, flush=True)
    print("RESULT: all eight component-13/mask-105 rank-10 strata are excluded by the same three residual cells", flush=True)


if __name__ == "__main__":
    main()
