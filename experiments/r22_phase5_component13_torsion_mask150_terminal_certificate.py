"""Terminal exact closure for component 13 / mask 150 / D class 1.

Prerequisites are the independently source-validated local scale relations and
18-stratum finite census. This verifier recompiles the nonlinear kernel on the
second physical D sheet, then checks the complete terminal ledger:

  * two affine-inconsistent branches;
  * four p-side rank-11 branches by one fixed constant source cell;
  * four q-side rank-11 branches by one fixed constant source cell;
  * eight rank-10 branches by the same three fixed g-cells in r=z18,s=z20.

No Groebner basis, floating search, or branch-specific source-cell search is
used.
"""
from __future__ import annotations

from fractions import Fraction

import r22_phase5_component13_mask150_residual_scan as rs
import r22_phase5_component13_torsion_mask150_finite_census as fc
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss
import r22_phase5_torsion_sheet as ts

P = (("X", "X", "X", "X", "Y"), (1, 0))
Q = (("X", "X", "X", "X", "X"), (2, 5))
G0 = (("X", "X", "X", "X", "g"), (0, 0))
G2 = (("X", "X", "X", "X", "g"), (0, 2))
G3 = (("X", "X", "X", "X", "g"), (0, 3))
RANK11_FREE = (0, 1, 10, 11, 15, 16, 20)
RANK10_FREE = (0, 1, 10, 11, 15, 16, 18, 20)
P_CASES = tuple((a, 0, sign) for a in (1, 2) for sign in (1, -1))
Q_CASES = tuple((0, b, sign) for b in (1, 2) for sign in (1, -1))
R10_CASES = tuple((a, b, sign) for b in (1, 2) for a in (1, 2) for sign in (1, -1))


def find_by_prov(data, target):
    hits = []
    for key, provs in data["provenance"].items():
        if target in provs:
            hits.append(data["residual"][key])
    if len(hits) != 1:
        raise AssertionError((target, "residual multiplicity", len(hits)))
    return hits[0]


def certify_constant(unique, target, cases, side):
    rows = []
    for a, b, sign in cases:
        data = rs.build_branch(unique, a, b, sign)
        if data["free"] != RANK11_FREE:
            raise AssertionError((side, a, b, sign, "unexpected free", data["free"]))
        poly = find_by_prov(data, target)
        if len(poly) != 1:
            raise AssertionError((side, a, b, sign, "not singleton", rs.poly_string(poly, data["free_names"])))
        mon, coeff = next(iter(poly.items()))
        if mon != (0,) * len(RANK11_FREE) or ss.kiszero(coeff):
            raise AssertionError((side, a, b, sign, "not nonzero constant", mon, ss.kstr(coeff)))
        row = {
            "type": f"{side}-rank11-one-cell",
            "a": a, "b": b, "z6_sign": "+" if sign > 0 else "-",
            "provenance": target,
            "residual": rs.poly_string(poly, data["free_names"]),
            "closed": True,
        }
        print(row, flush=True)
        rows.append(row)
    return rows


def poly2(raw, rpos, spos):
    out = {}
    for mon, c in raw.items():
        if any(e for j, e in enumerate(mon) if j not in (rpos, spos)):
            raise AssertionError(("escaped two-variable core", mon))
        k = (mon[rpos], mon[spos])
        v = ss.kadd(out.get(k, ss.K0), c)
        if ss.kiszero(v):
            out.pop(k, None)
        else:
            out[k] = v
    return out


def certify_rank10(unique, a, b, sign):
    data = rs.build_branch(unique, a, b, sign)
    if data["free"] != RANK10_FREE:
        raise AssertionError((a, b, sign, "unexpected free", data["free"]))
    rpos = data["free"].index(18)
    spos = data["free"].index(20)
    e2 = poly2(find_by_prov(data, G2), rpos, spos)
    e3 = poly2(find_by_prov(data, G3), rpos, spos)
    e0 = poly2(find_by_prov(data, G0), rpos, spos)

    if set(e2) != {(0, 0), (0, 2), (1, 1)}:
        raise AssertionError((a, b, sign, "bad G2 support", e2))
    if set(e3) != {(0, 0), (1, 1), (2, 0)}:
        raise AssertionError((a, b, sign, "bad G3 support", e3))
    c2, c3 = e2[(0, 0)], e3[(0, 0)]
    if ss.kiszero(c2) or ss.kiszero(c3):
        raise AssertionError((a, b, sign, "zero anchor scale"))
    four = ss.kr(Fraction(4, 1))
    minus_four = ss.kr(Fraction(-4, 1))
    if ss.kdiv(e2[(1, 1)], c2) != four or ss.kdiv(e2[(0, 2)], c2) != minus_four:
        raise AssertionError((a, b, sign, "G2 normalized form failed"))
    if ss.kdiv(e3[(1, 1)], c3) != four or ss.kdiv(e3[(2, 0)], c3) != minus_four:
        raise AssertionError((a, b, sign, "G3 normalized form failed"))

    # Subtracting normalized anchors gives 4(r^2-s^2)=0.  If r=s,
    # normalized G2 is 1=0.  If r=-s, normalized G2 gives s^2=1/8.
    s2 = ss.kr(Fraction(1, 8))
    if set(e0) - {(2, 0), (1, 1), (0, 2)}:
        raise AssertionError((a, b, sign, "G0 unexpected support", e0))
    crr = e0.get((2, 0), ss.K0)
    crs = e0.get((1, 1), ss.K0)
    css = e0.get((0, 2), ss.K0)
    minus_coeff = ss.ksub(ss.kadd(crr, css), crs)
    minus_value = ss.kmul(minus_coeff, s2)
    if ss.kiszero(minus_value):
        raise AssertionError((a, b, sign, "r=-s slice survives G0", ss.kstr(minus_coeff)))

    row = {
        "type": "rank10-three-cell",
        "a": a, "b": b, "z6_sign": "+" if sign > 0 else "-",
        "core": "r=z18,s=z20",
        "cells": (G2, G3, G0),
        "normalized_anchors": ("1+4rs-4s^2", "1+4rs-4r^2"),
        "r_equals_s": "G2 -> 1=0",
        "r_equals_minus_s": "s^2=1/8",
        "G0_at_minus_slice": ss.kstr(minus_value),
        "closed": True,
    }
    print(row, flush=True)
    return row


def main():
    rs.fc = fc
    with ts.second_sheet_provider():
        _q, unique = ml.compile_unique(13, 150)

    affine = [fc.branch_census(unique, 0, 0, sign) for sign in (1, -1)]
    if not all(not row["consistent"] for row in affine):
        raise AssertionError(("expected two affine-inconsistent branches", affine))

    p_rows = certify_constant(unique, P, P_CASES, "p")
    q_rows = certify_constant(unique, Q, Q_CASES, "q")
    r_rows = [certify_rank10(unique, *case) for case in R10_CASES]
    summary = {
        "component": 13, "mask": 150, "D_amplitude_class": 1,
        "affine_inconsistent": len(affine),
        "p_rank11_closed": len(p_rows),
        "q_rank11_closed": len(q_rows),
        "rank10_closed": len(r_rows),
        "finite_total": len(affine) + len(p_rows) + len(q_rows) + len(r_rows),
        "terminal_cells": {"p": P, "q": Q, "rank10": (G2, G3, G0)},
    }
    if summary["finite_total"] != 18:
        raise AssertionError(summary)
    print("SUMMARY", summary, flush=True)
    print("RESULT: component 13 mask 150 class-1 Phase-5 branch is CLOSED / EXACT", flush=True)


if __name__ == "__main__":
    main()
