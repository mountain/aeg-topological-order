"""Terminal exact Phase-5 certificate for component 13 / mask 105 / D class 1.

Prerequisites are the source-validated finite relations and the fresh 18-stratum
census.  The full ledger is checked here:

  * 2 affine-inconsistent strata;
  * 4 p-rank11 strata, one fixed source cell -> c*z3=0;
  * 4 q-rank11 strata, one fixed source cell -> c*z6=0;
  * 8 rank10 strata in the r=z17,s=z18 core, using the same fixed three
    provenance cells G3,G2,G0 on every branch.

No Groebner basis, numerical root search or global nonlinear solve is used.
"""
from __future__ import annotations

import r22_phase5_component13_mask105_residual_scan as rs
import r22_phase5_component13_torsion_mask105_finite_census as fc
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss
import r22_phase5_torsion_sheet as ts

P_CELL = (("X", "X", "X", "X", "Y"), (1, 0))
Q_CELL = (("X", "X", "X", "X", "X"), (5, 2))
G3 = (("X", "X", "X", "X", "g"), (0, 3))
G2 = (("X", "X", "X", "X", "g"), (0, 2))
G0 = (("X", "X", "X", "X", "g"), (0, 0))
RANK11_FREE = (3, 4, 5, 6, 17, 19, 20)
RANK10_FREE = (3, 4, 5, 6, 17, 18, 19, 20)


def target(data, prov):
    hits = []
    for key, provs in data["provenance"].items():
        if prov in provs:
            hits.append(data["residual"][key])
    if len(hits) != 1:
        raise AssertionError((prov, "residual multiplicity", len(hits)))
    return hits[0]


def singleton_in(data, prov, zname):
    poly = target(data, prov)
    if len(poly) != 1:
        raise AssertionError((prov, "not singleton", rs.poly_string(poly, data["free_names"])))
    mon, coeff = next(iter(poly.items()))
    pos = data["free_names"].index(zname)
    expected = [0] * len(data["free_names"])
    expected[pos] = 1
    if mon != tuple(expected) or ss.kiszero(coeff):
        raise AssertionError((prov, zname, mon, ss.kstr(coeff)))
    return coeff, poly


def poly2(poly, rpos, spos):
    out = {}
    for mon, c in poly.items():
        if any(e and j not in (rpos, spos) for j, e in enumerate(mon)):
            raise AssertionError(("not bivariate", mon))
        key = (mon[rpos], mon[spos])
        v = ss.kadd(out.get(key, ss.K0), c)
        if ss.kiszero(v):
            out.pop(key, None)
        else:
            out[key] = v
    return out


def p2add(a, b):
    out = dict(a)
    for m, c in b.items():
        v = ss.kadd(out.get(m, ss.K0), c)
        if ss.kiszero(v):
            out.pop(m, None)
        else:
            out[m] = v
    return out


def eval2(poly, r, s):
    out = ss.K0
    for (er, es), c in poly.items():
        term = ss.kmul(c, ss.kmul(ss.kpow(r, er), ss.kpow(s, es)))
        out = ss.kadd(out, term)
    return out


def certify_rank10(unique, a, b, sign):
    data = rs.build_branch(unique, a, b, sign)
    if data["free"] != RANK10_FREE:
        raise AssertionError((a, b, sign, "unexpected free", data["free"]))
    names = data["free_names"]
    rpos = names.index("z17")
    spos = names.index("z18")

    e1 = poly2(target(data, G3), rpos, spos)
    e2 = poly2(target(data, G2), rpos, spos)
    e3 = poly2(target(data, G0), rpos, spos)

    total = p2add(e1, e2)
    forbidden = {m: c for m, c in total.items() if m not in ((0, 1), (0, 2))}
    if forbidden:
        raise AssertionError((a, b, sign, "G3+G2 unexpected terms", forbidden))
    aa = total.get((0, 1), ss.K0)
    bb = total.get((0, 2), ss.K0)
    if ss.kiszero(aa) or ss.kiszero(bb):
        raise AssertionError((a, b, sign, "degenerate s factor", ss.kstr(aa), ss.kstr(bb)))

    candidates = []
    for s in (ss.K0, ss.kneg(ss.kdiv(aa, bb))):
        c0 = ss.K0
        c1 = ss.K0
        for (er, es), c in e1.items():
            term = ss.kmul(c, ss.kpow(s, es))
            if er == 0:
                c0 = ss.kadd(c0, term)
            elif er == 1:
                c1 = ss.kadd(c1, term)
            else:
                raise AssertionError((a, b, sign, "G3 nonlinear in r", er, es))
        if ss.kiszero(c1):
            raise AssertionError((a, b, sign, "G3 lost r coefficient", ss.kstr(s)))
        r = ss.kneg(ss.kdiv(c0, c1))
        if not ss.kiszero(eval2(e1, r, s)) or not ss.kiszero(eval2(e2, r, s)):
            raise AssertionError((a, b, sign, "anchor candidate mismatch", ss.kstr(r), ss.kstr(s)))
        v3 = eval2(e3, r, s)
        if ss.kiszero(v3):
            raise AssertionError((a, b, sign, "G0 vanishes at candidate", ss.kstr(r), ss.kstr(s)))
        candidates.append({"r": ss.kstr(r), "s": ss.kstr(s), "G0": ss.kstr(v3)})

    row = {
        "type": "rank10-three-cell",
        "a": a,
        "b": b,
        "z0_sign": "+" if sign > 0 else "-",
        "core": "r=z17,s=z18",
        "anchors": (G3, G2),
        "third": G0,
        "s_factor": {"s": ss.kstr(aa), "s2": ss.kstr(bb)},
        "candidates": candidates,
        "closed": True,
    }
    print(row, flush=True)
    return row


def main():
    rs.fc = fc
    with ts.second_sheet_provider():
        _q, unique = ml.compile_unique(13, 105)

    inconsistent = []
    for sign in (1, -1):
        row = fc.branch_census(unique, 0, 0, sign)
        if row["consistent"]:
            raise AssertionError(("expected affine inconsistency", sign, row))
        inconsistent.append(row)

    p_rows = []
    for a in (1, 2):
        for sign in (1, -1):
            data = rs.build_branch(unique, a, 0, sign)
            if data["free"] != RANK11_FREE:
                raise AssertionError((a, 0, sign, "unexpected p free", data["free"]))
            coeff, poly = singleton_in(data, P_CELL, "z3")
            row = {
                "type": "p-rank11-one-cell", "a": a, "b": 0,
                "z0_sign": "+" if sign > 0 else "-", "provenance": P_CELL,
                "residual": rs.poly_string(poly, data["free_names"]),
                "coefficient": ss.kstr(coeff), "closed": True,
            }
            print(row, flush=True)
            p_rows.append(row)

    q_rows = []
    for b in (1, 2):
        for sign in (1, -1):
            data = rs.build_branch(unique, 0, b, sign)
            if data["free"] != RANK11_FREE:
                raise AssertionError((0, b, sign, "unexpected q free", data["free"]))
            coeff, poly = singleton_in(data, Q_CELL, "z6")
            row = {
                "type": "q-rank11-one-cell", "a": 0, "b": b,
                "z0_sign": "+" if sign > 0 else "-", "provenance": Q_CELL,
                "residual": rs.poly_string(poly, data["free_names"]),
                "coefficient": ss.kstr(coeff), "closed": True,
            }
            print(row, flush=True)
            q_rows.append(row)

    rank10 = [
        certify_rank10(unique, a, b, sign)
        for b in (1, 2)
        for a in (1, 2)
        for sign in (1, -1)
    ]

    summary = {
        "component": 13,
        "mask": 105,
        "D_amplitude_class": 1,
        "affine_inconsistent": len(inconsistent),
        "p_rank11_closed": len(p_rows),
        "q_rank11_closed": len(q_rows),
        "rank10_closed": len(rank10),
        "finite_total": len(inconsistent) + len(p_rows) + len(q_rows) + len(rank10),
        "terminal_cells": {"p": P_CELL, "q": Q_CELL, "rank10": (G3, G2, G0)},
    }
    if summary["finite_total"] != 18 or not all(r["closed"] for r in p_rows + q_rows + rank10):
        raise AssertionError(summary)
    print("SUMMARY", summary, flush=True)
    print("RESULT: component 13 mask 105 class-1 Phase-5 branch is CLOSED / EXACT", flush=True)


if __name__ == "__main__":
    main()
