"""Three-cell exact certificate for the representative rank-10 stratum
component 13 / chirality mask 0 / (a,b,z5-sign)=(1,1,+).

After the verified finite relations and affine RREF, let

    r = z17,  s = z18.

This probe checks only

    G0 = (X,X,X,X;g)_(0,0),
    G2 = (X,X,X,X;g)_(0,2),
    G3 = (X,X,X,X;g)_(0,3).

It verifies exactly that G2-G3 is a nonzero scalar times r^2-s^2.  Hence a
common zero has r=+s or r=-s.  On each sign slice G0 is a nonzero scalar times
s^2, so G0=0 forces s=0.  But G2 has a nonzero constant term on both sign
slices, contradicting G2=0 at s=0.

No global nonlinear solve or Groebner basis is used.
"""
from __future__ import annotations

import r22_phase5_component13_mask0_residual_scan as rs
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss

CASE = (1, 1, 1)
G0 = (("X", "X", "X", "X", "g"), (0, 0))
G2 = (("X", "X", "X", "X", "g"), (0, 2))
G3 = (("X", "X", "X", "X", "g"), (0, 3))


def target(data, prov):
    hits = []
    for key, provs in data["provenance"].items():
        if prov in provs:
            hits.append(data["residual"][key])
    if len(hits) != 1:
        raise AssertionError((prov, "residual multiplicity", len(hits)))
    return hits[0]


def restrict_sign(poly, rpos, spos, sign, nf):
    """Substitute r=sign*s; require no variable besides r,s occurs."""
    out = {}
    for mon, c in poly.items():
        for j, e in enumerate(mon):
            if e and j not in (rpos, spos):
                raise AssertionError(("unexpected variable in bivariate core", j, mon))
        degree = mon[rpos] + mon[spos]
        cc = c if sign > 0 or mon[rpos] % 2 == 0 else ss.kneg(c)
        old = out.get(degree, ss.K0)
        val = ss.kadd(old, cc)
        if ss.kiszero(val):
            out.pop(degree, None)
        else:
            out[degree] = val
    return out


def main():
    _quotient, unique = ml.compile_unique(13, 0)
    data = rs.build_branch(unique, *CASE)
    if data["free"] != (0, 9, 10, 11, 17, 18, 19, 20):
        raise AssertionError(("unexpected rank-10 free variables", data["free"]))

    names = data["free_names"]
    rpos = names.index("z17")
    spos = names.index("z18")
    g0 = target(data, G0)
    g2 = target(data, G2)
    g3 = target(data, G3)

    if rs.poly_support(g0) != (rpos, spos):
        raise AssertionError(("G0 support", rs.poly_support(g0)))
    if rs.poly_support(g2) != (rpos, spos) or rs.poly_support(g3) != (rpos, spos):
        raise AssertionError(("G2/G3 support", rs.poly_support(g2), rs.poly_support(g3)))

    diff = rs.padd(g2, rs.pscale(g3, ss.kneg(ss.K1)))
    mr = [0] * len(names)
    ms = [0] * len(names)
    mr[rpos] = 2
    ms[spos] = 2
    mr, ms = tuple(mr), tuple(ms)
    if set(diff) != {mr, ms}:
        raise AssertionError(("G2-G3 monomial support", diff))
    ar = diff[mr]
    ass = diff[ms]
    if ss.kiszero(ar) or not ss.kiszero(ss.kadd(ar, ass)):
        raise AssertionError(("G2-G3 is not A*(r^2-s^2)", ss.kstr(ar), ss.kstr(ass)))

    signs = []
    for sign in (1, -1):
        q0 = restrict_sign(g0, rpos, spos, sign, len(names))
        q2 = restrict_sign(g2, rpos, spos, sign, len(names))

        # G0|_{r=+-s} = H*s^2 with H != 0.
        if set(q0) != {2} or ss.kiszero(q0[2]):
            raise AssertionError(("G0 sign restriction", sign, {d:ss.kstr(c) for d,c in q0.items()}))

        # G2 has a nonzero constant term on either sign slice.  Therefore
        # s=0, forced by G0, contradicts G2 immediately.
        if 0 not in q2 or ss.kiszero(q2[0]):
            raise AssertionError(("G2 missing nonzero constant", sign, {d:ss.kstr(c) for d,c in q2.items()}))

        signs.append({
            "r_equals": "+s" if sign > 0 else "-s",
            "G0_s2_coefficient": ss.kstr(q0[2]),
            "G2_constant": ss.kstr(q2[0]),
            "closed": True,
        })

    out = {
        "branch": (1, 1, "+"),
        "cells": (G0, G2, G3),
        "G2_minus_G3_r2_coefficient": ss.kstr(ar),
        "sign_branches": signs,
        "closed": True,
    }
    print(out, flush=True)
    print("RESULT: representative component-13/mask-0 rank-10 branch is excluded by three local g-cells", flush=True)


if __name__ == "__main__":
    main()
