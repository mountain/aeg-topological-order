"""Three-cell exact certificates for all eight rank-10 finite strata of
component 13 / chirality mask 0.

The exact finite census leaves

    (a,b) in {(1,1),(2,1),(1,2),(2,2)}

for both signs of z5=sqrt(2)/2.  On every branch the affine quotient has free
variables

    z0,z9,z10,z11,z17,z18,z19,z20.

Set r=z17 and s=z18.  For each branch this script independently rebuilds the
residual quotient and checks the fixed local cells

    G0 = (X,X,X,X;g)_(0,0),
    G2 = (X,X,X,X;g)_(0,2),
    G3 = (X,X,X,X;g)_(0,3).

The accepted certificate form is:

1. G2-G3 = A*(r^2-s^2), A != 0;
2. hence r=+s or r=-s;
3. on each sign slice G0 = H*s^2 with H != 0, so s=0;
4. on each sign slice G2 has a nonzero constant term, contradicting G2=0.

Every branch is verified separately.  No global solve or Groebner basis is
used.
"""
from __future__ import annotations

import r22_phase5_component13_mask0_residual_scan as rs
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss

G0 = (("X", "X", "X", "X", "g"), (0, 0))
G2 = (("X", "X", "X", "X", "g"), (0, 2))
G3 = (("X", "X", "X", "X", "g"), (0, 3))
CASES = tuple(
    (a, b, sign)
    for (a, b) in ((1,1), (2,1), (1,2), (2,2))
    for sign in (1, -1)
)
EXPECTED_FREE = (0, 9, 10, 11, 17, 18, 19, 20)


def target(data, prov):
    hits = []
    for key, provs in data["provenance"].items():
        if prov in provs:
            hits.append(data["residual"][key])
    if len(hits) != 1:
        raise AssertionError((prov, "residual multiplicity", len(hits)))
    return hits[0]


def restrict_sign(poly, rpos, spos, sign):
    out = {}
    for mon, c in poly.items():
        for j, e in enumerate(mon):
            if e and j not in (rpos, spos):
                raise AssertionError(("unexpected variable in bivariate core", j, mon))
        degree = mon[rpos] + mon[spos]
        cc = c if sign > 0 or mon[rpos] % 2 == 0 else ss.kneg(c)
        val = ss.kadd(out.get(degree, ss.K0), cc)
        if ss.kiszero(val):
            out.pop(degree, None)
        else:
            out[degree] = val
    return out


def certify(unique, a, b, z5sign):
    data = rs.build_branch(unique, a, b, z5sign)
    if data["free"] != EXPECTED_FREE:
        raise AssertionError((a, b, z5sign, "unexpected free variables", data["free"]))

    names = data["free_names"]
    rpos = names.index("z17")
    spos = names.index("z18")
    g0 = target(data, G0)
    g2 = target(data, G2)
    g3 = target(data, G3)

    for label, poly in (("G0", g0), ("G2", g2), ("G3", g3)):
        if rs.poly_support(poly) != (rpos, spos):
            raise AssertionError((a, b, z5sign, label, "support", rs.poly_support(poly)))

    diff = rs.padd(g2, rs.pscale(g3, ss.kneg(ss.K1)))
    mr = [0] * len(names)
    ms = [0] * len(names)
    mr[rpos] = 2
    ms[spos] = 2
    mr, ms = tuple(mr), tuple(ms)
    if set(diff) != {mr, ms}:
        raise AssertionError((a, b, z5sign, "G2-G3 support", diff))
    ar = diff[mr]
    ass = diff[ms]
    if ss.kiszero(ar) or not ss.kiszero(ss.kadd(ar, ass)):
        raise AssertionError((a, b, z5sign, "G2-G3 not A*(r^2-s^2)", ss.kstr(ar), ss.kstr(ass)))

    sign_rows = []
    for rsign in (1, -1):
        q0 = restrict_sign(g0, rpos, spos, rsign)
        q2 = restrict_sign(g2, rpos, spos, rsign)
        if set(q0) != {2} or ss.kiszero(q0[2]):
            raise AssertionError((a, b, z5sign, rsign, "G0 sign restriction", {d:ss.kstr(c) for d,c in q0.items()}))
        if 0 not in q2 or ss.kiszero(q2[0]):
            raise AssertionError((a, b, z5sign, rsign, "G2 constant", {d:ss.kstr(c) for d,c in q2.items()}))
        sign_rows.append({
            "r_equals": "+s" if rsign > 0 else "-s",
            "G0_s2_coefficient": ss.kstr(q0[2]),
            "G2_constant": ss.kstr(q2[0]),
        })

    row = {
        "a": a,
        "b": b,
        "z5_sign": "+" if z5sign > 0 else "-",
        "cells": (G0, G2, G3),
        "G2_minus_G3_r2_coefficient": ss.kstr(ar),
        "sign_slices": sign_rows,
        "closed": True,
    }
    print(row, flush=True)
    return row


def main():
    _quotient, unique = ml.compile_unique(13, 0)
    rows = [certify(unique, *case) for case in CASES]
    if len(rows) != 8 or not all(r["closed"] for r in rows):
        raise AssertionError(rows)
    print("SUMMARY", {"closed": 8, "total": 8, "cells": (G0, G2, G3)}, flush=True)
    print("RESULT: all eight component-13/mask-0 rank-10 strata are excluded by the same three local g-cells", flush=True)


if __name__ == "__main__":
    main()
