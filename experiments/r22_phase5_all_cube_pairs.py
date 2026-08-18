"""Complete finite audit of all 3x3 cube-root pairs and both z0 roots.

This reuses the exact Phase-5 ratio-class machinery but does not assume a
simultaneous mu3 symmetry: the separate mod-3 grading audit found none that also
preserves all required F determinants.  Therefore every

    p=P0*omega^a, q=Q0*omega^b, a,b in {0,1,2}

is checked explicitly for both roots of 2*z0^2+4*z0-1=0.

The 219-polynomial kernel is compiled and locally rewritten once; each of the
18 finite branches independently rebuilds the safely localized affine closure
and evaluates the three diagnostic final pentagon cells.
"""
from __future__ import annotations

import argparse
import sympy as sp

import r22_phase5_ratio_classes as rc


def run_pair(unique, reduced, by_prov, a, b, root_name):
    p = sp.expand(rc.P0 * rc.OMEGA ** a)
    q = sp.expand(rc.Q0 * rc.OMEGA ** b)
    t = rc.Z0_ROOTS[root_name]
    affine, exprs = rc.affine_closure(unique, reduced, p, q, t)
    out = {
        "a": a,
        "b": b,
        "ratio_class": (a - b) % 3,
        "root": root_name,
        "p": str(p),
        "q": str(q),
        "p_over_q": str(sp.expand(p / q)),
        "affine": affine,
    }
    if exprs is None:
        out["closed"] = True
        out["reason"] = "affine_inconsistency"
        return out

    target_rows = []
    closed = False
    for prov in rc.TARGETS:
        key = by_prov[prov]
        spoly = rc.specialize_reduced(reduced[key], p, q, t)
        expr = rc.zpoly_expr(spoly)
        rem = rc.substitute_closure(expr, exprs, p, q, t)
        obstruction = rc.is_nonzero_scale_laurent(rem)
        target_rows.append({
            "provenance": prov,
            "remainder": str(rem),
            "nonzero_scale_laurent_obstruction": obstruction,
        })
        closed = closed or obstruction
    out["targets"] = target_rows
    out["closed"] = closed
    out["reason"] = "diagnostic_target" if closed else "survives_diagnostic_targets"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    ap.add_argument("--b", type=int, action="append", choices=(0, 1, 2))
    args = ap.parse_args()

    bs = args.b or [0, 1, 2]
    unique, reduced, by_prov = rc.compile_reduced_once(args.component, args.mask)
    rows = []
    for b in bs:
        for a in range(3):
            for root in ("positive", "negative"):
                row = run_pair(unique, reduced, by_prov, a, b, root)
                rows.append(row)
                print(row, flush=True)

    summary = {
        "closed": sum(bool(r["closed"]) for r in rows),
        "total": len(rows),
        "survivors": [
            {"a": r["a"], "b": r["b"], "ratio_class": r["ratio_class"], "root": r["root"]}
            for r in rows if not r["closed"]
        ],
    }
    print("SUMMARY", summary, flush=True)
    if not summary["survivors"]:
        print("RESULT: all explicitly audited cube-root pairs in the requested b-slices are excluded", flush=True)
    else:
        print("RESULT: some finite cube-root pairs survive the diagnostic cells", flush=True)


if __name__ == "__main__":
    main()
