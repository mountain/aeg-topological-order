"""Exact affine closure on either Gaussian-rational Phase-5 z0 root.

Fix

    p=-(1+i)/2, q=(1-i)/2,

and choose either root of

    2*z0^2+4*z0-1=0.

The local certificate proves z1,z2,z3,z8 are nonzero. For every specialized
kernel polynomial, divide only by the common monomial in those four variables.
Whenever the residual equation is affine-linear in z1,...,z20, add it to one
exact linear system over Q(i,sqrt(6)).

This is safe localization plus ordinary Gaussian elimination, not a nonlinear
solver. Running both roots independently audits whether the affine formulas are
really one z0-parametric family rather than an artifact of the positive root.
"""
from __future__ import annotations

import argparse
from collections import Counter

import sympy as sp

import r22_phase5_exact_stratum as xs
import r22_phase5_local_rewrite as lr
import r22_phase5_monomial_lift as ml


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


def compile_specialized(cid, mask, z0_value):
    _quotient, unique = ml.compile_unique(cid, mask)
    rows = []
    provs = []
    profile = Counter()
    for key, prov in unique.items():
        reduced = lr.reduce_poly(key)
        poly = xs.specialize_reduced(reduced, z0_value)
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


def analyze(cid, mask, root_name):
    z0_value = xs.Z0_POS if root_name == "positive" else xs.Z0_NEG
    rows, provs, profile = compile_specialized(cid, mask, z0_value)
    aug = sp.Matrix(rows)
    A = aug[:, :20]
    rank_a = A.rank()
    rank_aug = aug.rank()
    if rank_a != rank_aug:
        raise RuntimeError(("linear closure inconsistent", root_name, rank_a, rank_aug))

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

    examples = [
        {"provenance": prov, "support": support}
        for prov, support in sorted(provs, key=lambda x: (len(x[1]), str(x[0])))[:24]
    ]

    # Compare the RREF output with the concise z0-parametric formulas inferred
    # from the positive root.  These equalities are assertions, not assumptions.
    q = xs.Q
    t = z0_value
    z20 = zs[19]
    expected = {
        6: sp.Integer(0),
        7: sp.Integer(0),
        9: sp.Integer(0),
        10: sp.Integer(0),
        13: sp.I * t - z20,
        14: -z20,
        15: -q * t,
        16: (-1 + sp.I) * z20 + sp.I * q * t,
        17: -q * t,
        18: (-1 + sp.I) * z20 + sp.I * q * t,
        19: z20 - sp.I * t,
    }
    formula_checks = {}
    for k, rhs in expected.items():
        ok = k in expressions and sp.simplify(expressions[k] - rhs) == 0
        formula_checks[f"z{k}"] = bool(ok)
    all_expected = all(formula_checks.values())

    out = {
        "component": cid,
        "mask": mask,
        "root": root_name,
        "z0": str(z0_value),
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
        "z0_parametric_formula_checks": formula_checks,
        "all_z0_parametric_formulas_verified": all_expected,
        "short_localized_cells": examples,
    }
    print(out, flush=True)
    if not all_expected:
        raise RuntimeError(("negative/positive affine family differs from expected z0-parametric form", root_name, formula_checks))
    print("RESULT: exact affine closure computed and z0-parametric formulas verified", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    ap.add_argument("--root", choices=("positive", "negative"), default="positive")
    args = ap.parse_args()
    analyze(args.component, args.mask, args.root)


if __name__ == "__main__":
    main()
