"""Finite Phase-5 audit of the three p/q cube-root classes.

The local certificate gives

    p^3=(1-i)/4, q^3=-(1+i)/4, (p/q)^3=i,
    2*z0^2+4*z0-1=0,
    z1,z2,z3,z8 != 0.

Choose q=Q0=(1-i)/2 and p=P0*omega^k with

    P0=-(1+i)/2, omega^3=1, k=0,1,2.

For each ratio class and each z0 root, independently rebuild the safely
localized affine closure over Q(i,sqrt(3),sqrt(6)), then evaluate only three
already-diagnostic final pentagon entries:

    (X,X,X,X,X;X)_(5,2),
    (X,X,X,X;1)_(1,3),
    (X,X,X,X;1)_(3,1).

A target is an obstruction only when it reduces to a nonzero Laurent monomial
in the proved-nonzero scaling variables z1,z2 (constants included).  This is a
finite exact audit, not a global nonlinear solve.
"""
from __future__ import annotations

import argparse
from collections import Counter

import sympy as sp

import r22_phase5_linear_closure as lc
import r22_phase5_local_rewrite as lr
import r22_phase5_monomial_lift as ml


SQ3 = sp.sqrt(3)
SQ6 = sp.sqrt(6)
OMEGA = (-1 + sp.I * SQ3) / 2
P0 = -(1 + sp.I) / 2
Q0 = (1 - sp.I) / 2
Z0_ROOTS = {
    "positive": (SQ6 - 2) / 2,
    "negative": -(SQ6 + 2) / 2,
}
ZS = sp.symbols("z1:21")
NONZERO_SCALE = {ZS[0], ZS[1]}
TARGETS = (
    (("X", "X", "X", "X", "X"), (5, 2)),
    (("X", "X", "X", "X", "1"), (1, 3)),
    (("X", "X", "X", "X", "1"), (3, 1)),
)


def gc_expr(c):
    return sp.Rational(c[0].numerator, c[0].denominator) + sp.I * sp.Rational(c[1].numerator, c[1].denominator)


def specialize_reduced(poly, p, q, t):
    out = {}
    for mon, c in poly.items():
        coeff = gc_expr(c) * p ** mon[0] * q ** mon[1] * t ** mon[2]
        zm = tuple(mon[3:])
        out[zm] = out.get(zm, 0) + coeff
    return {
        m: sp.collect(sp.expand(c), (SQ3, SQ6))
        for m, c in out.items()
        if sp.expand(c) != 0
    }


def zpoly_expr(poly):
    expr = sp.Integer(0)
    for mon, c in poly.items():
        term = c
        for j, e in enumerate(mon):
            if e:
                term *= ZS[j] ** e
        expr += term
    return sp.expand(expr)


def compile_reduced_once(cid, mask):
    _quotient, unique = ml.compile_unique(cid, mask)
    reduced = {key: lr.reduce_poly(key) for key in unique}
    by_prov = {prov: key for key, prov in unique.items()}
    missing = [p for p in TARGETS if p not in by_prov]
    if missing:
        raise RuntimeError(("missing diagnostic target provenance", missing))
    return unique, reduced, by_prov


def affine_closure(unique, reduced, p, q, t):
    rows = []
    profile = Counter()
    for key, prov in unique.items():
        poly = specialize_reduced(reduced[key], p, q, t)
        if not poly:
            continue
        stripped = lc.strip_common_nonzero(poly)
        ar = lc.affine_row(stripped)
        if ar is None:
            continue
        a, b = ar
        if not any(c != 0 for c in a):
            if sp.simplify(b) != 0:
                raise RuntimeError(("localized affine contradiction", prov, b))
            continue
        support = tuple(i + 1 for i, c in enumerate(a) if c != 0)
        profile[len(support)] += 1
        rows.append(a + [b])

    aug = sp.Matrix(rows)
    A = aug[:, :20]
    rank_a = A.rank()
    rank_aug = aug.rank()
    if rank_a != rank_aug:
        return {
            "consistent": False,
            "rank": rank_a,
            "rank_aug": rank_aug,
            "rows": len(rows),
            "support_profile": dict(profile),
        }, None

    rref, pivots_all = aug.rref()
    pivots = tuple(j for j in pivots_all if j < 20)
    free = tuple(j for j in range(20) if j not in pivots)
    exprs = {}
    for row, j in enumerate(pivots):
        expr = rref[row, 20]
        for k in free:
            if rref[row, k] != 0:
                expr -= rref[row, k] * ZS[k]
        exprs[j] = sp.collect(sp.expand(expr), (SQ3, SQ6))

    meta = {
        "consistent": True,
        "rows": len(rows),
        "support_profile": dict(profile),
        "rank": rank_a,
        "free_dimension": 20 - rank_a,
        "pivots": tuple(j + 1 for j in pivots),
        "free": tuple(j + 1 for j in free),
        "forced_zero": tuple(j + 1 for j, e in exprs.items() if e == 0),
    }
    return meta, exprs


def substitute_closure(expr, exprs, p, q, t):
    # Product relations are valid because z1,z2,z3,z8 are already proved nonzero.
    product = {
        ZS[2]: sp.I * p ** 2 * t / ZS[1],
        ZS[7]: -sp.I * q ** 2 * t / ZS[0],
    }
    subs = {}
    for j, rhs in exprs.items():
        subs[ZS[j]] = sp.cancel(rhs.subs(product))
    subs.update(product)
    return sp.factor(sp.cancel(expr.subs(subs)))


def is_nonzero_scale_laurent(expr):
    expr = sp.cancel(expr)
    if expr == 0:
        return False
    num, den = sp.fraction(expr)
    if (num.free_symbols | den.free_symbols) - NONZERO_SCALE:
        return False
    try:
        pn = sp.Poly(sp.expand(num), ZS[0], ZS[1], extension=[sp.I, SQ3, SQ6])
        pd = sp.Poly(sp.expand(den), ZS[0], ZS[1], extension=[sp.I, SQ3, SQ6])
    except Exception:
        return False
    return len(pn.terms()) == 1 and len(pd.terms()) == 1 and not pn.is_zero and not pd.is_zero


def run_case(unique, reduced, by_prov, k, root_name):
    p = sp.expand(P0 * OMEGA ** k)
    q = Q0
    t = Z0_ROOTS[root_name]
    affine, exprs = affine_closure(unique, reduced, p, q, t)
    out = {
        "ratio_class": k,
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
    for prov in TARGETS:
        key = by_prov[prov]
        spoly = specialize_reduced(reduced[key], p, q, t)
        expr = zpoly_expr(spoly)
        rem = substitute_closure(expr, exprs, p, q, t)
        obstruction = is_nonzero_scale_laurent(rem)
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
    ap.add_argument("--ratio-class", type=int, action="append", choices=(0, 1, 2))
    ap.add_argument("--root", action="append", choices=("positive", "negative"))
    args = ap.parse_args()

    ks = args.ratio_class or [0, 1, 2]
    roots = args.root or ["positive", "negative"]
    unique, reduced, by_prov = compile_reduced_once(args.component, args.mask)
    rows = []
    for k in ks:
        for root in roots:
            row = run_case(unique, reduced, by_prov, k, root)
            rows.append(row)
            print(row, flush=True)
    print("SUMMARY", {"closed": sum(bool(r["closed"]) for r in rows), "total": len(rows)}, flush=True)


if __name__ == "__main__":
    main()
