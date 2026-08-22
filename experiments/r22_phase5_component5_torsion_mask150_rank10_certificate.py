"""Exact uniform rank-10 certificate test for component 5 / mask 150 / D class 1.

The fresh 18-stratum census leaves exactly eight rank-10 branches at
(a,b)=(1,1),(2,1),(1,2),(2,2), for both roots of the z0 quadratic.
This verifier tests the same fixed source family that closed mask 105:

    G2 = (X,X,X,X;g)_(0,2),
    G3 = (X,X,X,X;g)_(0,3),
    H  = (X,X,X,X,X)_(2,23).

The first two cells are source-validated on every branch against

    G2 ~ 4*x*y - 4*y^2 - 1,
    G3 ~ 4*x^2 - 4*x*y + 1,

with x=z19,y=z20. Hence x=y is impossible and the only common-zero slice is
x=-y, y^2=-1/8. Both exact signs are then substituted directly into H.
Closure is accepted only when H is a nonzero constant on both signs for every
one of the eight rank-10 strata.

No Groebner basis or global nonlinear solve is used.
"""
from __future__ import annotations

import r22_phase5_component5_rest_audit as fa
import r22_phase5_component5_torsion_finite_audit as tf
import r22_phase5_component5_torsion_mask105_rank10_certificate as base
import r22_phase5_component5_torsion_sparse_residual as sr
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as s
import r22_phase5_torsion_sheet as ts

MASK = 150


def main():
    cid = 5
    mask = MASK
    rel = tf.relation(mask)

    old = fa.REL.get(mask)
    fa.REL[mask] = rel
    try:
        with ts.second_sheet_provider():
            _quotient, unique = ml.compile_unique(cid, mask)
    finally:
        if old is None:
            fa.REL.pop(mask, None)
        else:
            fa.REL[mask] = old

    by_prov = {prov: key for key, prov in unique.items()}
    missing = [prov for prov in (base.G2, base.G3, base.H) if prov not in by_prov]
    if missing:
        raise AssertionError(("missing certificate provenance", missing))
    reduced = {key: fa.reduce_poly(key, rel) for key in unique}

    rows = []
    for a, b in base.PAIRS:
        for root in base.ROOTS:
            p, q, t = sr.branch_values(mask, a, b, root)
            specialized, pivots, old_free, zmaps, profile = base.affine_quotient(
                unique, reduced, p, q, t, rel
            )

            g2 = base.normalized_cell(by_prov[base.G2], specialized, zmaps, old_free)
            g3 = base.normalized_cell(by_prov[base.G3], specialized, zmaps, old_free)
            mg2 = s.canonical(base.model_g2(old_free), old_free)
            mg3 = s.canonical(base.model_g3(old_free), old_free)
            if g2 != mg2:
                raise AssertionError((a, b, root, "G2 mismatch", g2, mg2))
            if g3 != mg3:
                raise AssertionError((a, b, root, "G3 mismatch", g3, mg3))

            sign_rows = []
            for sign in base.SIGNS:
                r, h = base.constant_after_sign(
                    by_prov[base.H], specialized, zmaps, old_free, sign
                )
                sign_rows.append({
                    "sign": sign,
                    "z20": s.kstr(r),
                    "z19": s.kstr(s.kneg(r)),
                    "H_normalized": [(m, s.kstr(c)) for m, c in h],
                    "closed": True,
                })

            row = {
                "component": cid,
                "mask": mask,
                "D_amplitude_class": 1,
                "cube_pair": (a, b),
                "root": root,
                "affine_rank": len(pivots),
                "affine_support_profile": profile,
                "G2": "4*x*y - 4*y^2 - 1",
                "G3": "4*x^2 - 4*x*y + 1",
                "derived": "x=-y, y^2=-1/8",
                "H": base.H,
                "signs": sign_rows,
                "closed": True,
            }
            rows.append(row)
            print(row, flush=True)

    summary = {
        "component": cid,
        "mask": mask,
        "D_amplitude_class": 1,
        "rank10_closed": len(rows),
        "rank10_total": 8,
        "sign_subbranches_checked": len(rows) * len(base.SIGNS),
        "certificate_cells": (base.G2, base.G3, base.H),
    }
    print("SUMMARY", summary, flush=True)
    if len(rows) != 8:
        raise AssertionError(("rank-10 closure incomplete", summary))
    print("RESULT: all eight mask-150 class-1 rank-10 strata are excluded by one fixed three-cell source family", flush=True)


if __name__ == "__main__":
    main()
