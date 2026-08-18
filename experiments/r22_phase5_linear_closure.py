"""Exact linear closure on the positive constructive Phase-5 stratum.

Start from the specialized component-5/mask-0 kernel with

    p=-(1+i)/2, q=(1-i)/2, z0=1/(2+sqrt(6)).

The local certificate proves z1,z2,z3,z8 are nonzero.  For each specialized
kernel polynomial, divide only by the common monomial in those four variables.
Whenever the residual equation is affine-linear in z1,...,z20, add it to one
exact linear system over Q(i,sqrt(6)).

This is safe localization plus ordinary Gaussian elimination, not a nonlinear
solver.  The output gives rank, free variables and exact pivot expressions.
"""
from __future__ import annotations

import argparse
from collections import Counter

import sympy as sp

import r22_phase5_exact_stratum as xs
import r22_phase5_local_rewrite as lr
import r22_phase5_monomial_lift as ml


# z-indices are 1..20; tuple positions are 0..19.
PROVED_NONZERO_Z = (1, 2, 3, 8)


def strip_common_nonzero(poly):
    if not poly:
        return {}
    mins = {}
    for j in PROVED_NONZERO_Z:
        k = j - 1
        mins[k] = min(mon[k] for mon in poly)
    out = {}
    for mon, c in poly.items():
        mm = list(mon)
        for k, m in mins.items():
            mm[k] -= m
        out[tuple(mm)] = c
    return out


def affine_row(poly):
    coeff = [sp.Integer(0)] * 20
    const = sp.Integer(0)
    for mon, c in poly.items():
        deg = sum(mon)
        if deg == 0:
            const += c
            continue
        if deg != 1:
            return None
        j = next((k for k, e in enumerate(mon) if e), None)
        if j is None or mon[j] != 1:
            return None
        coeff[j] += c
    coeff = [sp.collect(sp.expand(c), sp.sqrt(6)) for c in coeff]
    const = sp.collect(sp.expand(const), sp.sqrt(6))
    return coeff, -const


def compile_specialized(cid, mask):
    _quotient, unique = ml.compile_unique(cid, mask)
    rows = []
    provs = []
    profile = Counter()
    for key, prov in unique.items():
        reduced = lr.reduce_poly(key)
        poly = xs.specialize_reduced(reduced, xs.Z0_POS)
        if not poly:
            continue
        stripped = strip_common_nonzero(poly)
        ar = affine_row(stripped)
        if ar is None:
            continue
        a, b = ar
        if not any(c != 0 for c in a):
            if b != 0:
                raise RuntimeError(("localized affine contradiction", prov, stripped, b))
            continue
        support = tuple(i + 1 for i, c in enumerate(a) if c != 0)
        profile[len(support)] += 1
        rows.append(a + [b])
        provs.append((prov, support))
    return rows, provs, profile


def analyze(cid, mask):
    rows, provs, profile = compile_specialized(cid, mask)
    aug = sp.Matrix(rows)
    A = aug[:, :20]
    b = aug[:, 20]
    rank_a = A.rank()
    rank_aug = aug.rank()
    if rank_a != rank_aug:
        raise RuntimeError(("linear closure inconsistent", rank_a, rank_aug))

    rref, pivots_all = aug.rref()
    pivots = tuple(p for p in pivots_all if p < 20)
    free = tuple(j for j in range(20) if j not in pivots)
    zs = sp.symbols("z1:21")

    expressions = {}
    forced_zero = []
    forced_constants = {}
    for row, p in enumerate(pivots):
        expr = rref[row, 20]
        for j in free:
            if rref[row, j] != 0:
                expr -= rref[row, j] * zs[j]
        expr = sp.collect(sp.expand(expr), sp.sqrt(6))
        expressions[p + 1] = expr
        if not (expr.free_symbols & set(zs)):
            if expr == 0:
                forced_zero.append(p + 1)
            else:
                forced_constants[p + 1] = str(expr)

    # Keep provenance of the shortest localized linear cells.  The RREF itself
    # may combine many rows, so these are orientation aids, not a certificate
    # of minimality.
    examples = [
        {"provenance": prov, "support": support}
        for prov, support in sorted(provs, key=lambda x: (len(x[1]), str(x[0])))[:24]
    ]

    out = {
        "component": cid,
        "mask": mask,
        "field": "Q(i,sqrt(6))",
        "localized_by_nonzero_z": PROVED_NONZERO_Z,
        "affine_equations": len(rows),
        "affine_support_profile": dict(profile),
        "rank": rank_a,
        "free_dimension": 20 - rank_a,
        "pivot_variables": tuple(p + 1 for p in pivots),
        "free_variables": tuple(j + 1 for j in free),
        "forced_zero_variables": tuple(forced_zero),
        "forced_constant_variables": forced_constants,
        "pivot_expressions": {f"z{k}": str(v) for k, v in expressions.items()},
        "short_localized_cells": examples,
    }
    print(out, flush=True)
    print("RESULT: exact affine closure computed; nonlinear remainder may now be expressed in the free variables", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    args = ap.parse_args()
    analyze(args.component, args.mask)


if __name__ == "__main__":
    main()
