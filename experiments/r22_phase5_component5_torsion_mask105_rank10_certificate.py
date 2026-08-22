"""Exact uniform rank-10 certificate for component 5 / mask 105 / D class 1.

The fresh 18-stratum census leaves exactly eight rank-10 branches

    (a,b) = (1,1), (2,1), (1,2), (2,2)

for both roots of 2*z0^2+4*z0-1=0.  This verifier compiles the class-1 kernel
once, rebuilds each rank-10 affine quotient independently, and validates the
fixed source cells

    G2 = (X,X,X,X;g)_(0,2),
    G3 = (X,X,X,X;g)_(0,3),
    H  = (X,X,X,X,X)_(2,23).

On every rank-10 branch, after affine substitution and normalization by only the
proved-nonzero scale variables z1,z2,

    G2 ~ 4*x*y - 4*y^2 - 1,
    G3 ~ 4*x^2 - 4*x*y + 1,

where x=z19 and y=z20.  Hence G2+G3=4*(x-y)*(x+y).  The slice x=y contradicts
G2 immediately, so x=-y and G2 gives y^2=-1/8.  Both exact signs

    y = +/- i*sqrt(2)/4

are then checked directly against H.  The certificate closes a branch only if
H becomes a nonzero constant on BOTH signs.

No Groebner basis or global nonlinear solve is used.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction

import r22_phase5_component5_rest_audit as fa
import r22_phase5_component5_torsion_finite_audit as tf
import r22_phase5_component5_torsion_sparse_residual as sr
import r22_phase5_monomial_lift as ml
import r22_phase5_rankdrop_second as second
import r22_phase5_survivor_sparse as s
import r22_phase5_torsion_sheet as ts

G2 = (("X", "X", "X", "X", "g"), (0, 2))
G3 = (("X", "X", "X", "X", "g"), (0, 3))
H = (("X", "X", "X", "X", "X"), (2, 23))
PAIRS = ((1, 1), (2, 1), (1, 2), (2, 2))
ROOTS = ("positive", "negative")
SIGNS = (1, -1)


def model_g2(old_free):
    pos = {j: k for k, j in enumerate(old_free)}
    n = len(old_free)
    px, py = pos[18], pos[19]
    z = (0,) * n
    mxy = list(z); mxy[px] = 1; mxy[py] = 1
    my2 = list(z); my2[py] = 2
    return {
        tuple(mxy): s.kr(4),
        tuple(my2): s.kr(-4),
        z: s.kr(-1),
    }


def model_g3(old_free):
    pos = {j: k for k, j in enumerate(old_free)}
    n = len(old_free)
    px, py = pos[18], pos[19]
    z = (0,) * n
    mx2 = list(z); mx2[px] = 2
    mxy = list(z); mxy[px] = 1; mxy[py] = 1
    return {
        tuple(mx2): s.kr(4),
        tuple(mxy): s.kr(-4),
        z: s.kr(1),
    }


def affine_quotient(unique, reduced, p, q, t, rel):
    specialized = {key: s.specialize(poly, p, q, t) for key, poly in reduced.items()}
    rows = []
    profile = Counter()
    for key, prov in unique.items():
        zpoly = s.strip_common_nonzero(specialized[key])
        ar = s.affine_row(zpoly)
        if ar is None:
            continue
        if all(s.kiszero(x) for x in ar[:20]):
            if not s.kiszero(ar[20]):
                raise AssertionError(("unexpected affine contradiction", prov))
            continue
        profile[sum(1 for x in ar[:20] if not s.kiszero(x))] += 1
        rows.append(ar)
    rr, pivots = s.rref(rows)
    if len(pivots) != 10:
        raise AssertionError(("expected rank 10", len(pivots)))
    zmaps, old_free = sr.build_zmaps_class1(rr, pivots, p, q, t, rel)
    expected = (0, 1, 3, 4, 10, 11, 18, 19)
    if old_free != expected:
        raise AssertionError(("unexpected final free variables", old_free))
    return specialized, pivots, old_free, zmaps, dict(profile)


def normalized_cell(key, specialized, zmaps, old_free):
    lp = s.evaluate(specialized[key], zmaps, len(old_free))
    ck = s.canonical(lp, old_free)
    if ck is None:
        raise AssertionError("source cell vanished unexpectedly")
    return ck


def constant_after_sign(key, specialized, zmaps, old_free, sign):
    lp = s.evaluate(specialized[key], zmaps, len(old_free))
    r = second.z20_value(sign)
    if not s.kiszero(s.kadd(s.kmul(r, r), s.kr(Fraction(1, 8)))):
        raise AssertionError(("bad sign root", sign, s.kstr(r)))
    projected, new_free = second.project_lp(lp, old_free, r)
    expected = (0, 1, 3, 4, 10, 11)
    if new_free != expected:
        raise AssertionError(("unexpected sign-projected free variables", new_free))
    ck = s.canonical(projected, new_free)
    if ck is None:
        raise AssertionError(("H vanished on sign", sign))
    if s.support(ck):
        raise AssertionError(("H retained variables on sign", sign, ck))
    if len(ck) != 1:
        raise AssertionError(("constant H has unexpected term count", sign, ck))
    return r, ck


def main():
    cid = 5
    mask = 105
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
    missing = [prov for prov in (G2, G3, H) if prov not in by_prov]
    if missing:
        raise AssertionError(("missing certificate provenance", missing))
    reduced = {key: fa.reduce_poly(key, rel) for key in unique}

    closed = 0
    rows = []
    for a, b in PAIRS:
        for root in ROOTS:
            p, q, t = sr.branch_values(mask, a, b, root)
            specialized, pivots, old_free, zmaps, profile = affine_quotient(unique, reduced, p, q, t, rel)

            g2 = normalized_cell(by_prov[G2], specialized, zmaps, old_free)
            g3 = normalized_cell(by_prov[G3], specialized, zmaps, old_free)
            mg2 = s.canonical(model_g2(old_free), old_free)
            mg3 = s.canonical(model_g3(old_free), old_free)
            if g2 != mg2:
                raise AssertionError((a, b, root, "G2 mismatch", g2, mg2))
            if g3 != mg3:
                raise AssertionError((a, b, root, "G3 mismatch", g3, mg3))

            sign_rows = []
            for sign in SIGNS:
                r, h = constant_after_sign(by_prov[H], specialized, zmaps, old_free, sign)
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
                "H": H,
                "signs": sign_rows,
                "closed": True,
            }
            rows.append(row)
            closed += 1
            print(row, flush=True)

    summary = {
        "component": cid,
        "mask": mask,
        "D_amplitude_class": 1,
        "rank10_closed": closed,
        "rank10_total": len(PAIRS) * len(ROOTS),
        "sign_subbranches_checked": len(rows) * len(SIGNS),
        "certificate_cells": (G2, G3, H),
    }
    print("SUMMARY", summary, flush=True)
    if closed != 8:
        raise AssertionError(("rank-10 closure incomplete", summary))
    print("RESULT: all eight mask-105 class-1 rank-10 strata are excluded by one fixed three-cell source family", flush=True)


if __name__ == "__main__":
    main()
