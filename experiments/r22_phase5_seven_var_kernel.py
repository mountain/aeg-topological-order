"""Project the constructive Phase-5 branch to its seven-variable Laurent kernel.

On the positive exact stratum, the affine closure gives

  z6=z7=z9=z10=0,
  z15=z17=-q*z0,
  z14=-z20,
  z13=i*z0-z20,
  z16=z18=(-1+i)*z20+i*q*z0,
  z19=z20-i*z0.

The proved product relations give

  z3=(-z0/2)/z2,   z8=(-z0/2)/z1,

with z1,z2 nonzero.  Substitute all of this into every specialized final-kernel
polynomial.  After clearing only powers of the known-nonzero z1,z2, report the
exact residual kernel in

  Q(i,sqrt(6))[z1,z2,z4,z5,z11,z12,z20].

No Groebner basis or nonlinear solve is attempted.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque

import sympy as sp

import r22_phase5_exact_stratum as xs
import r22_phase5_local_rewrite as lr
import r22_phase5_monomial_lift as ml


u, v, a, b, c, d, h = sp.symbols("u v a b c d h")
VARS = (u, v, a, b, c, d, h)
T = xs.Z0_POS
K = -T / 2
C = -xs.Q * T

SUB = {
    1: u,
    2: v,
    3: K / v,
    4: a,
    5: b,
    6: sp.Integer(0),
    7: sp.Integer(0),
    8: K / u,
    9: sp.Integer(0),
    10: sp.Integer(0),
    11: c,
    12: d,
    13: sp.I * T - h,
    14: -h,
    15: C,
    16: (-1 + sp.I) * h + sp.I * xs.Q * T,
    17: C,
    18: (-1 + sp.I) * h + sp.I * xs.Q * T,
    19: h - sp.I * T,
    20: h,
}


def poly_expr(poly):
    expr = sp.Integer(0)
    for mon, coeff in poly.items():
        term = coeff
        for j, e in enumerate(mon, start=1):
            if e:
                term *= SUB[j] ** e
        expr += term
    return sp.expand(expr)


def canonical(expr):
    expr = sp.cancel(expr)
    if expr == 0:
        return None
    num, den = sp.fraction(expr)
    # All variable denominators arise only from the proved nonzero u,v.
    bad = den.free_symbols - {u, v}
    if bad:
        raise RuntimeError(("unexpected residual denominator", den, bad))
    num = sp.expand(num)
    if num == 0:
        return None
    p = sp.Poly(num, *VARS, extension=[sp.I, sp.sqrt(6)])
    terms = p.terms()
    lead = terms[0][1]
    key = []
    for mon, coeff in terms:
        cc = sp.cancel(coeff.as_expr() / lead.as_expr()) if hasattr(coeff, "as_expr") else sp.cancel(coeff / lead)
        key.append((tuple(int(x) for x in mon), sp.collect(sp.expand(cc), sp.sqrt(6))))
    return tuple(key)


def vars_in(key):
    return {j for mon, _c in key for j, e in enumerate(mon) if e}


def incidence_components(keys):
    adj = {j: set() for j in range(7)}
    used = set()
    for key in keys:
        vs = sorted(vars_in(key)); used.update(vs)
        for x in vs:
            adj[x].update(y for y in vs if y != x)
    seen = set(); comps = []
    for s in sorted(used):
        if s in seen: continue
        q = deque([s]); seen.add(s); comp = []
        while q:
            x = q.popleft(); comp.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); q.append(y)
        comps.append(tuple(VARS[j].name for j in sorted(comp)))
    return comps


def analyze(cid, mask):
    _quotient, unique = ml.compile_unique(cid, mask)
    residual = {}
    vanished = []
    contradictions = []
    term_profile = Counter()
    degree_profile = Counter()
    var_profile = Counter()
    univariate = []
    shortest = []

    for key, prov in unique.items():
        reduced = lr.reduce_poly(key)
        spoly = xs.specialize_reduced(reduced, T)
        if not spoly:
            vanished.append(prov); continue
        expr = poly_expr(spoly)
        ck = canonical(expr)
        if ck is None:
            vanished.append(prov); continue
        residual.setdefault(ck, prov)

    for key, prov in residual.items():
        nt = len(key)
        deg = max(sum(mon) for mon, _c in key)
        vs = vars_in(key)
        term_profile[nt] += 1
        degree_profile[deg] += 1
        var_profile[len(vs)] += 1
        if not vs:
            contradictions.append((key, prov))
        if len(vs) == 1:
            univariate.append((key, prov, next(iter(vs))))

    for key, prov in sorted(residual.items(), key=lambda kv: (len(vars_in(kv[0])), len(kv[0]), max(sum(m) for m, _c in kv[0]), str(kv[1])))[:40]:
        shortest.append({
            "variables": [VARS[j].name for j in sorted(vars_in(key))],
            "terms": len(key),
            "degree": max(sum(mon) for mon, _c in key),
            "provenance": prov,
            "poly": str(key),
        })

    out = {
        "component": cid,
        "mask": mask,
        "field": "Q(i,sqrt(6))",
        "variables": tuple(x.name for x in VARS),
        "nonzero_variables": ("u", "v"),
        "base_kernel_polynomials": len(unique),
        "vanished_after_projection": len(vanished),
        "unique_residual_polynomials": len(residual),
        "term_count_profile": dict(term_profile),
        "degree_profile": dict(degree_profile),
        "variable_count_profile": dict(var_profile),
        "constant_contradictions": len(contradictions),
        "univariate_equations": len(univariate),
        "univariate_examples": [
            {"variable": VARS[j].name, "provenance": prov, "poly": str(key)}
            for key, prov, j in univariate[:16]
        ],
        "incidence_components": incidence_components(residual.keys()),
        "shortest": shortest,
    }
    print(out, flush=True)
    if contradictions:
        print("RESULT: seven-variable projection contains a constant contradiction", contradictions[0][1], flush=True)
    else:
        print("RESULT: seven-variable exact Laurent kernel compiled; continue constructive reduction", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    args = ap.parse_args()
    analyze(args.component, args.mask)


if __name__ == "__main__":
    main()
