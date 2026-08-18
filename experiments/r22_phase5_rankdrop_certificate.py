"""Audit a three-entry obstruction certificate on all Phase-5 rank-drop branches.

After the finite cube-root audit, eight component-5/mask-0 branches remain.  On
one representative, the shortest residual equations come from

    (X,X,X,X;g)_(0,0), (X,X,X,X;g)_(0,2), (X,X,X,X;g)_(0,3)

and involve only z19,z20.  This script replays those same three entries on all
eight rank-drop branches using the exact sparse coefficient field
Q(i,sqrt(2),sqrt(3)).

For equations of the exact forms

    F0 = g*x^2 + h*x*y + k*y^2 = 0,
    F2 = a*x*y + b*y^2 + c = 0,
    F3 = d*x^2 + e*x*y + f = 0,

with x=z19, y=z20 and a,d nonzero, put Y=y^2.  F2 and F3 give

    x*y = U*Y + V,
    x^2 = P*Y + Q.

F0 then gives one affine equation A*Y+B=0.  If A!=0, substitute
Y0=-B/A into the universal identity

    (x*y)^2 = x^2*y^2.

A nonzero exact remainder proves the three pentagon entries have no common
solution.  This is a tiny hand-auditable elimination, not a Groebner basis.
"""
from __future__ import annotations

import argparse

import r22_phase5_local_rewrite as lr
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as s


TARGETS = (
    (("X", "X", "X", "X", "g"), (0, 0)),
    (("X", "X", "X", "X", "g"), (0, 2)),
    (("X", "X", "X", "X", "g"), (0, 3)),
)
SURVIVOR_PAIRS = ((1, 1), (2, 1), (1, 2), (2, 2))


def coeff(poly, ex, ey):
    return poly.get((ex, ey), s.K0)


def to_bivariate(poly, final_free):
    pos = {j: k for k, j in enumerate(final_free)}
    px, py = pos[18], pos[19]  # z19,z20, zero-based z indices
    out = {}
    for mon, c in poly.items():
        if any(e and j not in (px, py) for j, e in enumerate(mon)):
            raise RuntimeError(("target is not z19/z20-local", final_free, mon))
        key = (mon[px], mon[py])
        v = s.kadd(out.get(key, s.K0), c)
        if s.kiszero(v):
            out.pop(key, None)
        else:
            out[key] = v
    return out


def expected_shape(poly, allowed, label):
    bad = set(poly) - set(allowed)
    if bad:
        raise RuntimeError(("unexpected target shape", label, sorted(poly), sorted(bad)))


def branch_certificate(unique, reduced, by_prov, a, b, root_name):
    p, q, t = s.branch_values(a, b, root_name)
    specialized = {key: s.specialize(poly, p, q, t) for key, poly in reduced.items()}

    rows = []
    for key, prov in unique.items():
        zpoly = s.strip_common_nonzero(specialized[key])
        ar = s.affine_row(zpoly)
        if ar is None:
            continue
        if all(s.kiszero(x) for x in ar[:20]):
            if not s.kiszero(ar[20]):
                return {"closed": True, "reason": "affine_inconsistency", "provenance": prov}
            continue
        rows.append(ar)

    rr, pivots = s.rref(rows)
    if len(pivots) != 10:
        raise RuntimeError(("expected rank-drop affine rank 10", a, b, root_name, len(pivots)))
    zmaps, final_free = s.build_zmaps(rr, pivots, p, q, t)
    if tuple(j + 1 for j in final_free) != (1, 2, 4, 5, 11, 12, 19, 20):
        raise RuntimeError(("unexpected final free variables", a, b, root_name, final_free))

    polys = []
    for prov in TARGETS:
        key = by_prov[prov]
        lp = s.evaluate(specialized[key], zmaps, len(final_free))
        polys.append(to_bivariate(lp, final_free))

    f0, f2, f3 = polys
    expected_shape(f0, {(2, 0), (1, 1), (0, 2)}, "F0")
    expected_shape(f2, {(1, 1), (0, 2), (0, 0)}, "F2")
    expected_shape(f3, {(2, 0), (1, 1), (0, 0)}, "F3")

    g, h, k = coeff(f0, 2, 0), coeff(f0, 1, 1), coeff(f0, 0, 2)
    aa, bb, cc = coeff(f2, 1, 1), coeff(f2, 0, 2), coeff(f2, 0, 0)
    d, e, ff = coeff(f3, 2, 0), coeff(f3, 1, 1), coeff(f3, 0, 0)
    if s.kiszero(aa) or s.kiszero(d):
        raise RuntimeError(("degenerate solve coefficient", a, b, root_name))

    # xy = U Y + V.
    U = s.kdiv(s.kneg(bb), aa)
    V = s.kdiv(s.kneg(cc), aa)

    # x^2 = P Y + Q.
    P = s.kdiv(s.kneg(s.kmul(e, U)), d)
    Q = s.kdiv(s.kneg(s.kadd(s.kmul(e, V), ff)), d)

    # F0 -> A Y + B = 0.
    A = s.kadd(s.kadd(s.kmul(g, P), s.kmul(h, U)), k)
    B = s.kadd(s.kmul(g, Q), s.kmul(h, V))
    if s.kiszero(A):
        closed = not s.kiszero(B)
        return {
            "cube_pair": (a, b), "root": root_name, "closed": closed,
            "reason": "F0_constant" if closed else "F0_redundant",
            "A": s.kstr(A), "B": s.kstr(B),
        }

    Y0 = s.kdiv(s.kneg(B), A)

    # H(Y) = (U Y + V)^2 - (P Y + Q)Y.
    c2 = s.ksub(s.kmul(U, U), P)
    c1 = s.ksub(s.kmul(s.kr(2), s.kmul(U, V)), Q)
    c0 = s.kmul(V, V)
    H = s.kadd(s.kadd(s.kmul(c2, s.kmul(Y0, Y0)), s.kmul(c1, Y0)), c0)
    closed = not s.kiszero(H)

    return {
        "cube_pair": (a, b),
        "ratio_class": (a - b) % 3,
        "root": root_name,
        "affine_rank": len(pivots),
        "closed": closed,
        "reason": "three_entry_identity_contradiction" if closed else "three_entry_test_survives",
        "U": s.kstr(U), "V": s.kstr(V),
        "P": s.kstr(P), "Q": s.kstr(Q),
        "A": s.kstr(A), "B": s.kstr(B),
        "Y0": s.kstr(Y0),
        "identity_remainder": s.kstr(H),
        "targets": TARGETS,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    args = ap.parse_args()

    _quotient, unique = ml.compile_unique(args.component, args.mask)
    reduced = {key: lr.reduce_poly(key) for key in unique}
    by_prov = {prov: key for key, prov in unique.items()}
    missing = [p for p in TARGETS if p not in by_prov]
    if missing:
        raise RuntimeError(("missing target provenance", missing))

    rows = []
    for a, b in SURVIVOR_PAIRS:
        for root in ("positive", "negative"):
            row = branch_certificate(unique, reduced, by_prov, a, b, root)
            rows.append(row)
            print(row, flush=True)

    survivors = [r for r in rows if not r.get("closed")]
    print("SUMMARY", {"closed": len(rows) - len(survivors), "total": len(rows), "survivors": survivors}, flush=True)
    if not survivors:
        print("RESULT: the same three final pentagon entries exclude all eight rank-drop finite branches", flush=True)
    else:
        print("RESULT: some rank-drop branches survive the three-entry certificate", flush=True)


if __name__ == "__main__":
    main()
