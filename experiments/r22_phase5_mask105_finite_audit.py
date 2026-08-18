"""Finite exact Phase-5 audit for component 5 / chirality mask 105.

Fresh local relations give

    p^3=(1+i)/4, q^3=-(1+i)/4,
    z2*z3=-i*p^2*z0, z1*z8=-i*q^2*z0,
    2*z0^2+4*z0-1=0,

with z1,z2,z3,z8 nonzero.  Hence

    p=P0*omega^a, q=Q0*omega^b, a,b in {0,1,2},
    z0=-1 +- sqrt(6)/2.

This probe rebuilds the safely localized affine closure independently on all 18
finite branches and evaluates seven local final-pentagon cells: the three cells
that were diagnostic for mask 0 plus the four adjacent (XXXX;g) cells that
closed its final rank-drop strata.  A cell is an obstruction only if its exact
remainder is a nonzero Laurent monomial in the already-proved nonzero z1,z2.
No Groebner basis or nonlinear solve is used.
"""
from __future__ import annotations

import argparse
from collections import Counter

import sympy as sp

import r22_phase5_mask105_local_rewrite as m105
import r22_phase5_monomial_lift as ml
import r22_phase5_ratio_classes as rc

SQ3 = sp.sqrt(3)
SQ6 = sp.sqrt(6)
OMEGA = (-1 + sp.I * SQ3) / 2
P0 = -(1 - sp.I) / 2
Q0 = (1 - sp.I) / 2
ROOTS = {
    "positive": (SQ6 - 2) / 2,
    "negative": -(SQ6 + 2) / 2,
}
ZS = rc.ZS

TARGETS = (
    (("X", "X", "X", "X", "X"), (5, 2)),
    (("X", "X", "X", "X", "1"), (1, 3)),
    (("X", "X", "X", "X", "1"), (3, 1)),
    (("X", "X", "X", "X", "g"), (0, 0)),
    (("X", "X", "X", "X", "g"), (0, 1)),
    (("X", "X", "X", "X", "g"), (0, 2)),
    (("X", "X", "X", "X", "g"), (0, 3)),
)


def compile_once(cid, mask):
    _quotient, unique = ml.compile_unique(cid, mask)
    reduced = {key: m105.reduce_poly(key) for key in unique}
    by_prov = {prov: key for key, prov in unique.items()}
    missing = [p for p in TARGETS if p not in by_prov]
    if missing:
        raise RuntimeError(("missing target provenance", missing))
    return unique, reduced, by_prov


def product_substitution(p, q, t):
    return {
        ZS[2]: -sp.I * p ** 2 * t / ZS[1],
        ZS[7]: -sp.I * q ** 2 * t / ZS[0],
    }


def substitute_closure(expr, exprs, p, q, t):
    product = product_substitution(p, q, t)
    subs = {ZS[j]: sp.cancel(rhs.subs(product)) for j, rhs in exprs.items()}
    subs.update(product)
    return sp.factor(sp.cancel(expr.subs(subs)))


def run_case(unique, reduced, by_prov, a, b, root_name):
    p = sp.expand(P0 * OMEGA ** a)
    q = sp.expand(Q0 * OMEGA ** b)
    t = ROOTS[root_name]

    affine, exprs = rc.affine_closure(unique, reduced, p, q, t)
    row = {
        "a": a,
        "b": b,
        "ratio_class": (a - b) % 3,
        "root": root_name,
        "p": str(p),
        "q": str(q),
        "affine": affine,
    }
    if exprs is None:
        row["closed"] = True
        row["reason"] = "affine_inconsistency"
        row["targets"] = []
        return row

    targets = []
    closed = False
    for prov in TARGETS:
        key = by_prov[prov]
        spoly = rc.specialize_reduced(reduced[key], p, q, t)
        expr = rc.zpoly_expr(spoly)
        rem = substitute_closure(expr, exprs, p, q, t)
        obstruction = rc.is_nonzero_scale_laurent(rem)
        targets.append({
            "provenance": prov,
            "remainder": str(rem),
            "nonzero_scale_laurent_obstruction": obstruction,
        })
        closed = closed or obstruction
    row["targets"] = targets
    row["closed"] = closed
    row["reason"] = "local_target" if closed else "survives_local_targets"
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=105)
    args = ap.parse_args()
    if args.mask != 105:
        raise ValueError("mask-105-specific probe")

    unique, reduced, by_prov = compile_once(args.component, args.mask)
    rows = []
    rank_profile = Counter()
    for b in range(3):
        for a in range(3):
            for root in ("positive", "negative"):
                row = run_case(unique, reduced, by_prov, a, b, root)
                rows.append(row)
                aff = row["affine"]
                if aff.get("consistent"):
                    rank_profile[(aff["rank"], aff["free_dimension"], tuple(aff["forced_zero"]))] += 1
                else:
                    rank_profile[("inconsistent",)] += 1
                print(row, flush=True)

    survivors = [
        {"a": r["a"], "b": r["b"], "ratio_class": r["ratio_class"], "root": r["root"], "affine": r["affine"]}
        for r in rows if not r["closed"]
    ]
    summary = {
        "total": len(rows),
        "closed_by_affine_or_7_targets": sum(bool(r["closed"]) for r in rows),
        "rank_profile": {str(k): v for k, v in rank_profile.items()},
        "survivors": survivors,
    }
    print("SUMMARY", summary, flush=True)
    if survivors:
        print("RESULT: mask 105 has finite branches surviving the first affine/local-cell gate", flush=True)
    else:
        print("RESULT: all 18 mask-105 finite branches are excluded by the affine/local-cell gate", flush=True)


if __name__ == "__main__":
    main()
