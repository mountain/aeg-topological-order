"""Exact two-variable probe for the component-13/mask-105 rank-10 representative.

For branch (a,b,z0-sign)=(1,1,+), the affine residual leaves a 17-equation core
supported only on r=z16 and s=z18.  This probe uses two fixed short residual
relations to derive two exact candidate (r,s) points, then searches the
remaining bivariate equations for a single short third relation that is
nonzero at both candidates.

This is finite exact elimination in K=Q(i,sqrt(2),sqrt(3)); no Groebner basis
or floating-point root search is used.
"""
from __future__ import annotations

import r22_phase5_component13_mask105_residual_scan as rs
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss

CID = 13
MASK = 105
BRANCH = (1, 1, 1)

# Residual provenance anchors seen in the representative scan.
P1 = (("X", "X", "X", "X", "g"), (0, 3))
P2 = (("X", "X", "X", "X", "g"), (0, 2))


def poly2(poly, rpos, spos):
    out = {}
    for mon, c in poly.items():
        if any(e for j, e in enumerate(mon) if j not in (rpos, spos)):
            return None
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
        if ss.kiszero(v): out.pop(m, None)
        else: out[m] = v
    return out


def eval2(poly, r, s):
    out = ss.K0
    for (er, es), c in poly.items():
        out = ss.kadd(out, ss.kmul(c, ss.kmul(ss.kpow(r, er), ss.kpow(s, es))))
    return out


def find_by_prov(data, target):
    hits = []
    for key, provs in data["provenance"].items():
        if target in provs:
            hits.append((key, data["residual"][key], tuple(provs)))
    if len(hits) != 1:
        raise AssertionError((target, "residual multiplicity", len(hits)))
    return hits[0]


def main():
    _q, unique = ml.compile_unique(CID, MASK)
    data = rs.build_branch(unique, *BRANCH)
    if data["free"] != (3, 4, 5, 6, 16, 18, 19, 20):
        raise AssertionError(("unexpected free variables", data["free"]))
    rpos = data["free"].index(16)
    spos = data["free"].index(18)

    k1, raw1, provs1 = find_by_prov(data, P1)
    k2, raw2, provs2 = find_by_prov(data, P2)
    e1 = poly2(raw1, rpos, spos)
    e2 = poly2(raw2, rpos, spos)
    if e1 is None or e2 is None:
        raise AssertionError("anchor equation escaped the r,s core")

    # E1+E2 must reduce to a*s+b*s^2 with a,b both nonzero.
    total = p2add(e1, e2)
    forbidden = {m: c for m, c in total.items() if m not in ((0, 1), (0, 2))}
    if forbidden:
        raise AssertionError(("E1+E2 has unexpected terms", forbidden))
    a = total.get((0, 1), ss.K0)
    b = total.get((0, 2), ss.K0)
    if ss.kiszero(a) or ss.kiszero(b):
        raise AssertionError(("degenerate s factor", ss.kstr(a), ss.kstr(b)))
    s_values = (ss.K0, ss.kneg(ss.kdiv(a, b)))

    # E1 is affine in r after each s specialization.  Solve exact candidate r.
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
                raise AssertionError(("E1 nonlinear in r", er, es))
        if ss.kiszero(c1):
            raise AssertionError(("E1 lost r coefficient", ss.kstr(s), ss.kstr(c0)))
        r = ss.kneg(ss.kdiv(c0, c1))
        if not ss.kiszero(eval2(e1, r, s)) or not ss.kiszero(eval2(e2, r, s)):
            raise AssertionError("candidate does not solve E1,E2")
        candidates.append((r, s))

    # Collect all exact residuals supported inside {r,s}; find the shortest
    # single equation that is nonzero on both E1/E2 candidate points.
    bivar = []
    for key, raw in data["residual"].items():
        p = poly2(raw, rpos, spos)
        if p is None or not p:
            continue
        vals = tuple(eval2(p, r, s) for r, s in candidates)
        provs = tuple(data["provenance"][key])
        bivar.append((len(p), max(sum(m) for m in p), key, p, vals, provs))
    bivar.sort(key=lambda x: (x[0], x[1], str(x[2])))

    third = None
    for item in bivar:
        _nt, _deg, key, p, vals, provs = item
        if key in (k1, k2):
            continue
        if all(not ss.kiszero(v) for v in vals):
            third = item
            break
    if third is None:
        raise AssertionError("no single bivariate residual excludes both candidates")

    nt, deg, _key, _p, vals, provs3 = third
    out = {
        "branch": (1, 1, "+"),
        "free": data["free"],
        "bivariate_equations": len(bivar),
        "anchors": (P1, P2),
        "E1_plus_E2": {
            "s_coefficient": ss.kstr(a),
            "s2_coefficient": ss.kstr(b),
            "derived": "s*(a+b*s)=0",
        },
        "candidates": [
            {"r": ss.kstr(r), "s": ss.kstr(s), "third_value": ss.kstr(v)}
            for (r, s), v in zip(candidates, vals)
        ],
        "third": {
            "terms": nt,
            "degree": deg,
            "provenance": provs3[:4],
        },
        "closed": True,
    }
    print(out, flush=True)
    print("RESULT: representative mask-105 rank-10 branch is excluded by a three-residual bivariate certificate", flush=True)


if __name__ == "__main__":
    main()
