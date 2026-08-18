"""Exact Phase-5 finite-stratum audit for component 5 masks 150 and 255.

The fresh sparse kernels show that the four component-5 chirality survivors form
an exact p/q phase square.  The already-closed masks 0 and 105 use q-side
relation z1*z8=-i*q^2*z0.  The remaining masks 150 and 255 instead have

    q^3 = (-1+i)/4,     z1*z8 = +i*q^2*z0,

while the p side distinguishes the two masks:

    mask 150: p^3=(1-i)/4, z2*z3=+i*p^2*z0,
    mask 255: p^3=(1+i)/4, z2*z3=-i*p^2*z0.

In both cases the fifth local relation is

    2*z0^2 + 4*z0 - 1 = 0.

This probe applies only these five exact relations, rebuilds the safely
localized affine closure on all 18 finite (p,q,z0) strata, and evaluates the
same seven low-support final-pentagon cells that resolved masks 0 and 105.
A branch is declared closed at this gate only by affine inconsistency or by a
nonzero Laurent monomial in the already-proved nonzero z1,z2 scale variables.
No Groebner basis or global nonlinear solve is used.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction

import sympy as sp

import r22_epsminus_f_parametric as fp
import r22_epsminus_final_kernel as fk
import r22_phase5_monomial_lift as ml
import r22_phase5_ratio_classes as rc

GZERO = (Fraction(0), Fraction(0))
GONE = (Fraction(1), Fraction(0))
I = (Fraction(0), Fraction(1))
NEG_I = (Fraction(0), Fraction(-1))

SQ3 = sp.sqrt(3)
SQ6 = sp.sqrt(6)
OMEGA = (-1 + sp.I * SQ3) / 2
ROOTS = {
    "positive": (SQ6 - 2) / 2,
    "negative": -(SQ6 + 2) / 2,
}
ZS = rc.ZS

REL = {
    150: {
        "P3": (Fraction(1, 4), Fraction(-1, 4)),
        "Q3": (Fraction(-1, 4), Fraction(1, 4)),
        "Z23": I,
        "Z18": I,
        "P0": -(1 + sp.I) / 2,
        "Q0": (1 + sp.I) / 2,
    },
    255: {
        "P3": (Fraction(1, 4), Fraction(1, 4)),
        "Q3": (Fraction(-1, 4), Fraction(1, 4)),
        "Z23": NEG_I,
        "Z18": I,
        "P0": -(1 - sp.I) / 2,
        "Q0": (1 + sp.I) / 2,
    },
}

TARGETS = (
    (("X", "X", "X", "X", "X"), (5, 2)),
    (("X", "X", "X", "X", "1"), (1, 3)),
    (("X", "X", "X", "X", "1"), (3, 1)),
    (("X", "X", "X", "X", "g"), (0, 0)),
    (("X", "X", "X", "X", "g"), (0, 1)),
    (("X", "X", "X", "X", "g"), (0, 2)),
    (("X", "X", "X", "X", "g"), (0, 3)),
)


def gpow(x, n):
    out = GONE
    for _ in range(n):
        out = fp.gmul(out, x)
    return out


def add_term(poly, mon, coeff):
    if fp.giszero(coeff):
        return
    v = fp.gadd(poly.get(mon, GZERO), coeff)
    if fp.giszero(v):
        poly.pop(mon, None)
    else:
        poly[mon] = v


def z0_remainder(n):
    a, b = Fraction(1), Fraction(0)
    for _ in range(n):
        a, b = b / 2, a - 2 * b
    return a, b


def reduce_monomial(mon, coeff, rel):
    e = list(mon)
    c = coeff

    # z2*z3 = rel[Z23] * p^2 * z0.
    k = min(e[4], e[5])
    if k:
        e[4] -= k
        e[5] -= k
        e[0] += 2 * k
        e[2] += k
        c = fp.gmul(c, gpow(rel["Z23"], k))

    # z1*z8 = rel[Z18] * q^2 * z0.
    k = min(e[3], e[10])
    if k:
        e[3] -= k
        e[10] -= k
        e[1] += 2 * k
        e[2] += k
        c = fp.gmul(c, gpow(rel["Z18"], k))

    kp, e[0] = divmod(e[0], 3)
    kq, e[1] = divmod(e[1], 3)
    if kp:
        c = fp.gmul(c, gpow(rel["P3"], kp))
    if kq:
        c = fp.gmul(c, gpow(rel["Q3"], kq))

    a, b = z0_remainder(e[2])
    base = list(e)
    base[2] = 0
    out = {}
    if a:
        add_term(out, tuple(base), fp.gmul(c, (a, Fraction(0))))
    if b:
        base[2] = 1
        add_term(out, tuple(base), fp.gmul(c, (b, Fraction(0))))
    return out


def key_to_poly(key):
    return {tuple(mon): ml.gfromkey(gc) for mon, gc in key}


def reduce_poly(key, rel):
    out = {}
    for mon, c in key_to_poly(key).items():
        fk.poly_add_scaled(out, reduce_monomial(mon, c, rel))
    return out


def compile_once(cid, mask):
    rel = REL[mask]
    _quotient, unique = ml.compile_unique(cid, mask)
    reduced = {key: reduce_poly(key, rel) for key in unique}
    by_prov = {prov: key for key, prov in unique.items()}
    missing = [p for p in TARGETS if p not in by_prov]
    if missing:
        raise RuntimeError(("missing target provenance", missing))
    return unique, reduced, by_prov


def product_substitution(p, q, t, rel):
    s23 = sp.I if rel["Z23"] == I else -sp.I
    s18 = sp.I if rel["Z18"] == I else -sp.I
    return {
        ZS[2]: s23 * p**2 * t / ZS[1],
        ZS[7]: s18 * q**2 * t / ZS[0],
    }


def substitute_closure(expr, exprs, p, q, t, rel):
    product = product_substitution(p, q, t, rel)
    subs = {ZS[j]: sp.cancel(rhs.subs(product)) for j, rhs in exprs.items()}
    subs.update(product)
    return sp.factor(sp.cancel(expr.subs(subs)))


def run_case(unique, reduced, by_prov, mask, a, b, root_name):
    rel = REL[mask]
    p = sp.expand(rel["P0"] * OMEGA**a)
    q = sp.expand(rel["Q0"] * OMEGA**b)
    t = ROOTS[root_name]

    affine, exprs = rc.affine_closure(unique, reduced, p, q, t)
    row = {
        "mask": mask,
        "a": a,
        "b": b,
        "ratio_class": (a - b) % 3,
        "root": root_name,
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
        rem = substitute_closure(expr, exprs, p, q, t, rel)
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


def audit_mask(cid, mask):
    if mask not in REL:
        raise ValueError(("supported masks", tuple(REL)))
    rel = REL[mask]
    # Exact root identities are checked before any branch analysis.
    if sp.expand(rel["P0"]**3 - (rc.gc_expr(rel["P3"]))) != 0:
        raise AssertionError((mask, "bad P0"))
    if sp.expand(rel["Q0"]**3 - (rc.gc_expr(rel["Q3"]))) != 0:
        raise AssertionError((mask, "bad Q0"))

    unique, reduced, by_prov = compile_once(cid, mask)
    rows = []
    rank_profile = Counter()
    for b in range(3):
        for a in range(3):
            for root in ("positive", "negative"):
                row = run_case(unique, reduced, by_prov, mask, a, b, root)
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
        "component": cid,
        "mask": mask,
        "relations": {
            "p3": str(rc.gc_expr(rel["P3"])),
            "q3": str(rc.gc_expr(rel["Q3"])),
            "z2z3_phase": "+i" if rel["Z23"] == I else "-i",
            "z1z8_phase": "+i" if rel["Z18"] == I else "-i",
            "z0": "2*z0^2+4*z0-1=0",
        },
        "total": len(rows),
        "closed_by_affine_or_7_targets": sum(bool(r["closed"]) for r in rows),
        "rank_profile": {str(k): v for k, v in rank_profile.items()},
        "survivors": survivors,
    }
    print("SUMMARY", summary, flush=True)
    if survivors:
        print("RESULT: mask", mask, "has finite branches surviving the first affine/local-cell gate", flush=True)
    else:
        print("RESULT: all 18 finite branches are excluded for mask", mask, flush=True)
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, choices=tuple(REL), action="append")
    args = ap.parse_args()
    masks = args.mask or [150, 255]
    summaries = [audit_mask(args.component, m) for m in masks]
    print("GLOBAL", {"masks": masks, "survivors": sum(len(s["survivors"]) for s in summaries)}, flush=True)


if __name__ == "__main__":
    main()
