"""Short-relation scan for component 5 / D class 1 rank-10 off-diagonal strata.

Two broader searches have now been ruled out by exact gates:
- scanning all 219 residual equations is too expensive under the 10-minute guardrail;
- the eight nonzero source cells in row 0 of (XXXX;g) contain no direct
  two-sign Laurent-monomial obstruction on the representative branch.

This probe therefore scans only the shortest exact kernel relations: canonical
source equations with at most four monomial terms.  On one fresh representative
rank-10 off-diagonal branch, (a,b)=(2,1), positive z0 root, it imposes only the
already-derived exact consequences

    z19=-z20,  z20=+/- i*sqrt(2)/4,

and asks whether a short source equation becomes a nonzero Laurent monomial in
the proved-nonzero scale variables z1,z2 for both signs.

No Groebner basis or global nonlinear solve is used.
"""
from __future__ import annotations

import argparse

import sympy as sp

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


def scan(cid: int, mask: int, max_terms: int):
    if mask not in (105, 150, 255):
        raise ValueError("scan is intended for the remaining class-1 component-5 masks")

    old = fa.REL.get(mask)
    fa.REL[mask] = tf.relation(mask)
    try:
        with ts.second_sheet_provider():
            _quotient, unique = ml.compile_unique(cid, mask)
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

            short = [
                (len(key), str(prov), prov, key)
                for key, prov in unique.items()
                if len(key) <= max_terms
            ]
            short.sort(key=lambda row: (row[0], row[1]))
            print({
                "component": cid,
                "mask": mask,
                "D_amplitude_class": 1,
                "representative": (a, b, root),
                "max_terms": max_terms,
                "short_source_relations": len(short),
                "term_count_profile": {
                    n: sum(row[0] == n for row in short)
                    for n in sorted({row[0] for row in short})
                },
            }, flush=True)

            sign_candidates = {}
            sign_exprs = {}
            for sign in (+1, -1):
                yval = sign * sp.I * SQ2 / 4
                rows = []
                emap = {}
                for nterms, _pstr, prov, key in short:
                    rem = source_remainder(key, reduced, exprs, p, q, t, rel)
                    rem2 = sp.factor(sp.cancel(rem.subs({X: -yval, Y: yval})))
                    if is_nonzero_scale_laurent(rem2):
                        rows.append((int(sp.count_ops(rem2)), len(str(rem2)), nterms, str(prov), prov, rem2))
                        emap[prov] = rem2
                rows.sort(key=lambda r: (r[0], r[1], r[2], r[3]))
                sign_candidates[sign] = {r[4] for r in rows}
                sign_exprs[sign] = emap
                print({
                    "component": cid,
                    "mask": mask,
                    "D_amplitude_class": 1,
                    "a": a,
                    "b": b,
                    "root": root,
                    "sign": sign,
                    "candidate_count": len(rows),
                    "best": [
                        {
                            "provenance": r[4],
                            "kernel_terms": r[2],
                            "remainder": str(r[5]),
                            "ops": r[0],
                        }
                        for r in rows[:12]
                    ],
                }, flush=True)
    finally:
        if old is None:
            fa.REL.pop(mask, None)
        else:
            fa.REL[mask] = old

    common = sign_candidates[+1] & sign_candidates[-1]
    common_rows = []
    for prov in common:
        ep = sign_exprs[+1][prov]
        en = sign_exprs[-1][prov]
        common_rows.append((
            max(int(sp.count_ops(ep)), int(sp.count_ops(en))),
            len(str(ep)) + len(str(en)),
            str(prov),
            prov,
            ep,
            en,
        ))
    common_rows.sort(key=lambda r: (r[0], r[1], r[2]))
    out = {
        "component": cid,
        "mask": mask,
        "D_amplitude_class": 1,
        "representative": (2, 1, "positive"),
        "max_terms": max_terms,
        "common_sign_candidate_count": len(common_rows),
        "best_common": [
            {
                "provenance": r[3],
                "positive_remainder": str(r[4]),
                "negative_remainder": str(r[5]),
                "max_ops": r[0],
            }
            for r in common_rows[:12]
        ],
    }
    print("SUMMARY", out, flush=True)
    if common_rows:
        print("RESULT: a short source relation obstructs both exact signs on the representative branch", flush=True)
    else:
        print("RESULT: no <=max_terms source relation directly closes both signs on the representative branch", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=105)
    ap.add_argument("--max-terms", type=int, default=4)
    args = ap.parse_args()
    scan(args.component, args.mask, args.max_terms)


if __name__ == "__main__":
    main()
