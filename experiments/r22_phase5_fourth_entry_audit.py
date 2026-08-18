"""Audit the fourth local pentagon entry on all final finite Phase-5 branches.

Previous exact reductions leave only cube pairs (2,1) and (1,2), either root of
2*z0^2+4*z0-1=0, and the two exact signs

    z20 = +/- i*sqrt(2)/4,  z19 = -z20.

This script compiles the Phase-5 kernel once, independently rebuilds the rank-10
affine closure for each cube/root branch, then evaluates only

    (X,X,X,X;g)_(0,1)

on each of the two z20 signs.  If the projected expression is a nonzero constant,
that finite branch is excluded.  No global nonlinear solve is performed.
"""
from __future__ import annotations

import argparse

import r22_phase5_local_rewrite as lr
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as s
import r22_phase5_rankdrop_second as second


TARGET = (("X", "X", "X", "X", "g"), (0, 1))
PAIRS = ((2, 1), (1, 2))


def run_branch(unique, reduced, by_prov, a, b, root_name, sign):
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
                return {
                    "cube_pair": (a, b), "root": root_name, "sign": sign,
                    "closed": True, "reason": "affine_inconsistency", "provenance": prov,
                }
            continue
        rows.append(ar)

    rr, pivots = s.rref(rows)
    if len(pivots) != 10:
        raise RuntimeError(("expected rank-10 branch", a, b, root_name, len(pivots)))
    zmaps, old_free = s.build_zmaps(rr, pivots, p, q, t)
    if old_free != (0, 1, 3, 4, 10, 11, 18, 19):
        raise RuntimeError(("unexpected free variables", a, b, root_name, old_free))

    key = by_prov[TARGET]
    lp = s.evaluate(specialized[key], zmaps, len(old_free))
    r = second.z20_value(sign)
    projected, new_free = second.project_lp(lp, old_free, r)
    if new_free != (0, 1, 3, 4, 10, 11):
        raise RuntimeError(("unexpected final variables", new_free))

    # Normalize only by the already-proved nonzero scale variables z1,z2.
    ck = s.canonical(projected, new_free)
    if ck is None:
        return {
            "cube_pair": (a, b), "ratio_class": (a-b) % 3,
            "root": root_name, "sign": sign,
            "z20": s.kstr(r), "z19": s.kstr(s.kneg(r)),
            "closed": False, "reason": "fourth_entry_vanishes", "remainder": "0",
        }

    supp = s.support(ck)
    constant = not supp
    rem = [(m, s.kstr(c)) for m, c in ck]
    return {
        "cube_pair": (a, b), "ratio_class": (a-b) % 3,
        "root": root_name, "sign": sign,
        "z20": s.kstr(r), "z19": s.kstr(s.kneg(r)),
        "closed": constant,
        "reason": "fourth_entry_nonzero_constant" if constant else "fourth_entry_has_residual_variables",
        "remainder": rem,
        "provenance": TARGET,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    args = ap.parse_args()

    _quotient, unique = ml.compile_unique(args.component, args.mask)
    reduced = {key: lr.reduce_poly(key) for key in unique}
    by_prov = {prov: key for key, prov in unique.items()}
    if TARGET not in by_prov:
        raise RuntimeError(("missing target", TARGET))

    rows = []
    for a, b in PAIRS:
        for root in ("positive", "negative"):
            for sign in (1, -1):
                row = run_branch(unique, reduced, by_prov, a, b, root, sign)
                rows.append(row)
                print(row, flush=True)

    survivors = [r for r in rows if not r["closed"]]
    print("SUMMARY", {
        "closed": len(rows) - len(survivors),
        "total": len(rows),
        "survivors": survivors,
    }, flush=True)
    if not survivors:
        print("RESULT: the fourth local pentagon entry excludes all eight final finite subbranches", flush=True)
    else:
        print("RESULT: some final finite subbranches survive the fourth-entry audit", flush=True)


if __name__ == "__main__":
    main()
