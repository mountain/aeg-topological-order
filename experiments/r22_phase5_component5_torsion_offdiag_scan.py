"""Local source-cell scan for component 5 / D class 1 rank-10 off-diagonal strata.

The full 219-equation residual scan exceeded the 10-minute guardrail before its
first sign branch completed.  This probe deliberately narrows the search to the
source-local row

    (X,X,X,X;g)_(0,j)

because all existing component-5 rank-drop certificates live in the neighboring
j=0,1,2,3 cells of this block.

For one fresh representative off-diagonal branch, (a,b)=(2,1), positive z0
root, we derive the exact affine quotient, impose only the already-established
relations

    z19=-z20,  z20=+/- i*sqrt(2)/4,

and inspect every nonzero source cell in row 0.  A candidate is accepted only if
it reduces to a nonzero Laurent monomial in the proved-nonzero scale variables
z1,z2 for BOTH exact signs.  No global nonlinear solve is used.
"""
from __future__ import annotations

import argparse
from fractions import Fraction

import sympy as sp

import r22_epsminus_final_kernel as fk
import r22_phase5_component5_rest_audit as fa
import r22_phase5_component5_torsion_finite_audit as tf
import r22_phase5_monomial_lift as ml
import r22_phase5_ratio_classes as rc
import r22_phase5_torsion_sheet as ts

X = rc.ZS[18]  # z19
Y = rc.ZS[19]  # z20
Z1 = rc.ZS[0]
Z2 = rc.ZS[1]
SQ2 = sp.sqrt(2)
SQ3 = sp.sqrt(3)
SQ6 = sp.sqrt(6)
EXT = [sp.I, SQ2, SQ3, SQ6]


def is_nonzero_scale_laurent(expr):
    expr = sp.cancel(expr)
    if expr == 0:
        return False
    num, den = sp.fraction(expr)
    if (num.free_symbols | den.free_symbols) - {Z1, Z2}:
        return False
    try:
        pn = sp.Poly(sp.expand(num), Z1, Z2, extension=EXT)
        pd = sp.Poly(sp.expand(den), Z1, Z2, extension=EXT)
    except Exception:
        return False
    return (
        not pn.is_zero
        and not pd.is_zero
        and len(pn.terms()) == 1
        and len(pd.terms()) == 1
    )


def source_remainder(key, reduced, exprs, p, q, t, rel):
    spoly = rc.specialize_reduced(reduced[key], p, q, t)
    expr = rc.zpoly_expr(spoly)
    return sp.factor(sp.cancel(fa.substitute_closure(expr, exprs, p, q, t, rel)))


def row0_keys(quotient, reduced):
    labels = {"a": "X", "b": "X", "c": "X", "d": "X"}
    long_side, short_side = fk.pentagon_sparse(labels, "g", quotient)
    if not long_side:
        raise AssertionError("empty (XXXX;g) block")
    i = 0
    rows = []
    cols = sorted(set(long_side[i]) | set(short_side[i]))
    for j in cols:
        diff = dict(long_side[i].get(j, {}))
        fk.poly_add_scaled(
            diff,
            short_side[i].get(j, {}),
            (Fraction(-1), Fraction(0)),
        )
        if not diff:
            continue
        key, _floor = fk.canonical_poly(diff)
        if key is None:
            continue
        if key not in reduced:
            raise AssertionError(("row-0 canonical key missing from full kernel", j))
        rows.append((j, key))
    return rows


def scan(cid: int, mask: int):
    if mask not in (105, 150, 255):
        raise ValueError("scan is intended for the remaining class-1 component-5 masks")

    old = fa.REL.get(mask)
    fa.REL[mask] = tf.relation(mask)
    try:
        with ts.second_sheet_provider():
            quotient, unique = ml.compile_unique(cid, mask)
            rel = fa.REL[mask]
            reduced = {key: fa.reduce_poly(key, rel) for key in unique}

            a, b, root = 2, 1, "positive"
            p = sp.expand(rel["P0"] * fa.OMEGA**a)
            q = sp.expand(rel["Q0"] * fa.OMEGA**b)
            t = fa.ROOTS[root]
            affine, exprs = rc.affine_closure(unique, reduced, p, q, t)
            if exprs is None or not affine.get("consistent"):
                raise AssertionError((mask, a, b, root, "expected consistent branch", affine))
            if affine["rank"] != 10 or affine["free_dimension"] != 10:
                raise AssertionError((mask, a, b, root, "unexpected affine profile", affine))

            local = row0_keys(quotient, reduced)
            sign_candidates = {}
            sign_exprs = {}
            for sign in (+1, -1):
                yval = sign * sp.I * SQ2 / 4
                rows = []
                emap = {}
                for j, key in local:
                    rem = source_remainder(key, reduced, exprs, p, q, t, rel)
                    rem2 = sp.factor(sp.cancel(rem.subs({X: -yval, Y: yval})))
                    if is_nonzero_scale_laurent(rem2):
                        prov = (("X", "X", "X", "X", "g"), (0, j))
                        rows.append((int(sp.count_ops(rem2)), len(str(rem2)), j, prov, rem2))
                        emap[j] = rem2
                rows.sort(key=lambda r: (r[0], r[1], r[2]))
                sign_candidates[sign] = {r[2] for r in rows}
                sign_exprs[sign] = emap
                print({
                    "component": cid,
                    "mask": mask,
                    "D_amplitude_class": 1,
                    "a": a,
                    "b": b,
                    "root": root,
                    "sign": sign,
                    "affine_rank": affine["rank"],
                    "row0_nonzero_cells": len(local),
                    "candidate_count": len(rows),
                    "best": [
                        {"provenance": r[3], "remainder": str(r[4]), "ops": r[0]}
                        for r in rows[:12]
                    ],
                }, flush=True)
    finally:
        if old is None:
            fa.REL.pop(mask, None)
        else:
            fa.REL[mask] = old

    common = sorted(set.intersection(*sign_candidates.values()))
    common_rows = []
    for j in common:
        ep = sign_exprs[+1][j]
        en = sign_exprs[-1][j]
        common_rows.append((
            max(int(sp.count_ops(ep)), int(sp.count_ops(en))),
            len(str(ep)) + len(str(en)),
            j,
            ep,
            en,
        ))
    common_rows.sort(key=lambda r: (r[0], r[1], r[2]))
    out = {
        "component": cid,
        "mask": mask,
        "D_amplitude_class": 1,
        "representative": (2, 1, "positive"),
        "common_sign_candidate_count": len(common_rows),
        "best_common": [
            {
                "provenance": (("X", "X", "X", "X", "g"), (0, r[2])),
                "positive_remainder": str(r[3]),
                "negative_remainder": str(r[4]),
                "max_ops": r[0],
            }
            for r in common_rows[:12]
        ],
    }
    print("SUMMARY", out, flush=True)
    if common_rows:
        print("RESULT: local row-0 source cells contain a two-sign obstruction candidate", flush=True)
    else:
        print("RESULT: no row-0 cell closes both signs on the representative branch", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=105)
    args = ap.parse_args()
    scan(args.component, args.mask)


if __name__ == "__main__":
    main()
