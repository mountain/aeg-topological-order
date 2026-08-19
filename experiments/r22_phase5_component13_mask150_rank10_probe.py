"""Exact three-cell certificate probe for component 13 / mask 150 rank-10 representative.

For branch (a,b,z6-sign)=(1,1,+), the affine residual has a 17-equation core
supported only on r=z19 and s=z20.  This gate checks three fixed g-cell
residuals directly and derives the contradiction without Groebner/global solve.

The first two cells must have the exact common-factor forms

    B*(1/4 + r*s - s^2) = 0,
    B*(1/4 + r*s - r^2) = 0,

with B != 0.  Hence r^2=s^2.  If r=s, the first equation reduces to B/4=0.
If r=-s, the first equation gives s^2=1/8; the fixed third homogeneous
quadratic must then be nonzero on that slice.
"""
from __future__ import annotations

import r22_phase5_component13_mask150_residual_scan as rs
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss

CID = 13
MASK = 150
BRANCH = (1, 1, 1)
P1 = (("X", "X", "X", "X", "g"), (0, 3))
P2 = (("X", "X", "X", "X", "g"), (0, 2))
P3 = (("X", "X", "X", "X", "g"), (0, 0))


def find_by_prov(data, target):
    hits = []
    for key, provs in data["provenance"].items():
        if target in provs:
            hits.append(data["residual"][key])
    if len(hits) != 1:
        raise AssertionError((target, "residual multiplicity", len(hits)))
    return hits[0]


def poly2(raw, rpos, spos):
    out = {}
    for mon, c in raw.items():
        if any(e for j, e in enumerate(mon) if j not in (rpos, spos)):
            raise AssertionError(("escaped two-variable core", mon))
        k = (mon[rpos], mon[spos])
        v = ss.kadd(out.get(k, ss.K0), c)
        if ss.kiszero(v): out.pop(k, None)
        else: out[k] = v
    return out


def main():
    _q, unique = ml.compile_unique(CID, MASK)
    data = rs.build_branch(unique, *BRANCH)
    expected_free = (0, 1, 10, 11, 14, 15, 19, 20)
    if data["free"] != expected_free:
        raise AssertionError(("unexpected free variables", data["free"]))
    rpos = data["free"].index(19)
    spos = data["free"].index(20)

    e1 = poly2(find_by_prov(data, P1), rpos, spos)
    e2 = poly2(find_by_prov(data, P2), rpos, spos)
    e3 = poly2(find_by_prov(data, P3), rpos, spos)

    if set(e1) != {(0, 0), (0, 2), (1, 1)}:
        raise AssertionError(("bad P1 support", e1))
    if set(e2) != {(0, 0), (1, 1), (2, 0)}:
        raise AssertionError(("bad P2 support", e2))

    c1 = e1[(0, 0)]
    c2 = e2[(0, 0)]
    if ss.kiszero(c1) or c1 != c2:
        raise AssertionError(("anchor constants differ/vanish", ss.kstr(c1), ss.kstr(c2)))
    B = ss.kmul(ss.kr(4), c1)
    if ss.kiszero(B):
        raise AssertionError("B vanished")
    if e1[(1, 1)] != B or e1[(0, 2)] != ss.kneg(B):
        raise AssertionError(("P1 is not B*(1/4+rs-s^2)", e1))
    if e2[(1, 1)] != B or e2[(2, 0)] != ss.kneg(B):
        raise AssertionError(("P2 is not B*(1/4+rs-r^2)", e2))

    # P1-P2 gives B*(r^2-s^2)=0, hence r=+/-s over characteristic zero.
    # Slice r=s: P1 = B/4, already nonzero.
    plus_value = c1
    if ss.kiszero(plus_value):
        raise AssertionError("r=s slice unexpectedly survives")

    # Slice r=-s: P1 gives B*(1/4-2*s^2)=0 => s^2=1/8.
    s2 = ss.kr(__import__('fractions').Fraction(1, 8))

    # P3 must be a homogeneous quadratic C*r^2 + D*r*s + C*s^2.
    if set(e3) != {(2, 0), (1, 1), (0, 2)}:
        raise AssertionError(("bad P3 support", e3))
    C_r = e3[(2, 0)]
    C_s = e3[(0, 2)]
    D = e3[(1, 1)]
    if C_r != C_s:
        raise AssertionError(("P3 diagonal coefficients differ", ss.kstr(C_r), ss.kstr(C_s)))
    minus_coeff = ss.ksub(ss.kadd(C_r, C_s), D)  # r=-s
    minus_value = ss.kmul(minus_coeff, s2)
    if ss.kiszero(minus_coeff) or ss.kiszero(minus_value):
        raise AssertionError(("r=-s slice survives P3", ss.kstr(minus_coeff), ss.kstr(minus_value)))

    out = {
        "branch": (1, 1, "+"),
        "free": data["free"],
        "core": ("r=z19", "s=z20"),
        "cells": (P1, P2, P3),
        "B": ss.kstr(B),
        "P1_minus_P2": "B*(r^2-s^2)",
        "r_equals_s_P1": ss.kstr(plus_value),
        "r_equals_minus_s_s2": "1/8",
        "r_equals_minus_s_P3": ss.kstr(minus_value),
        "closed": True,
    }
    print(out, flush=True)
    print("RESULT: representative component-13/mask-150 rank-10 branch is excluded by three fixed g-cells", flush=True)


if __name__ == "__main__":
    main()
