"""Terminal Phase-5 certificates for component 13 / mask 0 / D class 1.

Prerequisites are the source-validated five-cell local model and the fresh exact
18-branch census.  This verifier recompiles the second-sheet kernel and closes:

* 4 p-side rank-11 branches with (XXXX;Y)_(1,0) = c*z0, c != 0;
* 4 q-side rank-11 branches with (XXXXX)_(5,2) = c*z12, c != 0;
* 8 rank-10 branches with the fixed g-cells G0,G2,G3 on the bivariate core
  r=z18, s=z19.

The rank-10 certificate checks G2-G3=A*(r^2-s^2), A!=0; on r=+/-s,
G0 is a nonzero scalar times s^2, hence s=0, while G2 has a nonzero constant.
No global solve or Groebner basis is used.
"""
from __future__ import annotations

import r22_phase5_component13_mask0_residual_scan as rs
import r22_phase5_component13_torsion_mask0_finite_census as fc
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss
import r22_phase5_torsion_sheet as ts

P_TARGET = (("X", "X", "X", "X", "Y"), (1, 0))
Q_TARGET = (("X", "X", "X", "X", "X"), (5, 2))
G0 = (("X", "X", "X", "X", "g"), (0, 0))
G2 = (("X", "X", "X", "X", "g"), (0, 2))
G3 = (("X", "X", "X", "X", "g"), (0, 3))

P_CASES = tuple((a, 0, sign) for a in (1, 2) for sign in (1, -1))
Q_CASES = tuple((0, b, sign) for b in (1, 2) for sign in (1, -1))
RANK10_CASES = tuple(
    (a, b, sign)
    for (a, b) in ((1, 1), (2, 1), (1, 2), (2, 2))
    for sign in (1, -1)
)
EXPECTED_RANK11_FREE = (0, 10, 11, 12, 15, 19, 20)
EXPECTED_RANK10_FREE = (0, 10, 11, 12, 15, 18, 19, 20)


def target(data, prov):
    hits = []
    for key, provs in data["provenance"].items():
        if prov in provs:
            hits.append(data["residual"][key])
    if len(hits) != 1:
        raise AssertionError((prov, "residual multiplicity", len(hits)))
    return hits[0]


def singleton_nonzero_scale(data, prov, expected_name):
    poly = target(data, prov)
    if len(poly) != 1:
        raise AssertionError((prov, "not singleton", rs.poly_string(poly, data["free_names"])))
    mon, coeff = next(iter(poly.items()))
    pos = data["free_names"].index(expected_name)
    expected = [0] * len(data["free_names"])
    expected[pos] = 1
    if mon != tuple(expected) or ss.kiszero(coeff):
        raise AssertionError((prov, expected_name, mon, ss.kstr(coeff)))
    return poly


def restrict_sign(poly, rpos, spos, sign):
    """Restrict r=sign*s and collect by total s degree."""
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


def certify_p(unique, a, b, sign):
    data = rs.build_branch(unique, a, b, sign)
    if data["free"] != EXPECTED_RANK11_FREE:
        raise AssertionError(("p", a, b, sign, data["free"]))
    poly = singleton_nonzero_scale(data, P_TARGET, "z0")
    row = {
        "type": "p-rank11-one-cell",
        "a": a, "b": b, "z5_sign": "+" if sign > 0 else "-",
        "provenance": P_TARGET,
        "residual": rs.poly_string(poly, data["free_names"]),
        "contradiction": "c*z0=0 with c!=0 and proved z0!=0",
        "closed": True,
    }
    print(row, flush=True)
    return row


def certify_q(unique, a, b, sign):
    data = rs.build_branch(unique, a, b, sign)
    if data["free"] != EXPECTED_RANK11_FREE:
        raise AssertionError(("q", a, b, sign, data["free"]))
    poly = singleton_nonzero_scale(data, Q_TARGET, "z12")
    row = {
        "type": "q-rank11-one-cell",
        "a": a, "b": b, "z5_sign": "+" if sign > 0 else "-",
        "provenance": Q_TARGET,
        "residual": rs.poly_string(poly, data["free_names"]),
        "contradiction": "c*z12=0 with c!=0 and proved z12!=0",
        "closed": True,
    }
    print(row, flush=True)
    return row


def certify_rank10(unique, a, b, sign):
    data = rs.build_branch(unique, a, b, sign)
    if data["free"] != EXPECTED_RANK10_FREE:
        raise AssertionError(("rank10", a, b, sign, data["free"]))
    names = data["free_names"]
    rpos = names.index("z18")
    spos = names.index("z19")
    g0 = target(data, G0)
    g2 = target(data, G2)
    g3 = target(data, G3)

    for label, poly in (("G0", g0), ("G2", g2), ("G3", g3)):
        if rs.poly_support(poly) != (rpos, spos):
            raise AssertionError((a, b, sign, label, "support", rs.poly_support(poly), names))

    diff = rs.padd(g2, rs.pscale(g3, ss.kneg(ss.K1)))
    mr = [0] * len(names); mr[rpos] = 2
    ms = [0] * len(names); ms[spos] = 2
    mr, ms = tuple(mr), tuple(ms)
    if set(diff) != {mr, ms}:
        raise AssertionError((a, b, sign, "G2-G3 support", diff))
    ar, ass = diff[mr], diff[ms]
    if ss.kiszero(ar) or not ss.kiszero(ss.kadd(ar, ass)):
        raise AssertionError((a, b, sign, "not A*(r^2-s^2)", ss.kstr(ar), ss.kstr(ass)))

    slices = []
    for rsign in (1, -1):
        q0 = restrict_sign(g0, rpos, spos, rsign)
        q2 = restrict_sign(g2, rpos, spos, rsign)
        if set(q0) != {2} or ss.kiszero(q0[2]):
            raise AssertionError((a, b, sign, rsign, "G0 slice", {d:ss.kstr(c) for d,c in q0.items()}))
        if 0 not in q2 or ss.kiszero(q2[0]):
            raise AssertionError((a, b, sign, rsign, "G2 constant", {d:ss.kstr(c) for d,c in q2.items()}))
        slices.append({
            "r_equals": "+s" if rsign > 0 else "-s",
            "G0_s2_coefficient": ss.kstr(q0[2]),
            "G2_constant": ss.kstr(q2[0]),
        })

    row = {
        "type": "rank10-three-cell",
        "a": a, "b": b, "z5_sign": "+" if sign > 0 else "-",
        "core": "r=z18,s=z19",
        "cells": (G0, G2, G3),
        "G2_minus_G3_r2_coefficient": ss.kstr(ar),
        "slices": slices,
        "closed": True,
    }
    print(row, flush=True)
    return row


def main():
    rs.fc = fc
    with ts.second_sheet_provider():
        _quotient, unique = ml.compile_unique(13, 0)

    p_rows = [certify_p(unique, *case) for case in P_CASES]
    q_rows = [certify_q(unique, *case) for case in Q_CASES]
    r_rows = [certify_rank10(unique, *case) for case in RANK10_CASES]
    if not (len(p_rows) == 4 and len(q_rows) == 4 and len(r_rows) == 8):
        raise AssertionError("terminal branch count mismatch")
    if not all(r["closed"] for r in p_rows + q_rows + r_rows):
        raise AssertionError("terminal closure incomplete")

    summary = {
        "component": 13,
        "mask": 0,
        "D_amplitude_class": 1,
        "affine_inconsistent": 2,
        "p_rank11_closed": 4,
        "q_rank11_closed": 4,
        "rank10_closed": 8,
        "finite_total": 18,
        "terminal_cells": {"p": P_TARGET, "q": Q_TARGET, "rank10": (G0, G2, G3)},
    }
    print("SUMMARY", summary, flush=True)
    print("RESULT: component 13 mask 0 class-1 Phase-5 branch is CLOSED / EXACT", flush=True)


if __name__ == "__main__":
    main()
