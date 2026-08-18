"""Constructive Phase-5 audit on the simplest exact component-5 stratum.

After the local certificate, choose the Gaussian-rational cube roots

    p = -(1+i)/2,    q = (1-i)/2,

and first take the positive z0 root

    z0 = (sqrt(6)-2)/2 = 1/(2+sqrt(6)).

The five proved local rewrite rules are applied first.  We then substitute this
exact stratum into every canonical final-kernel polynomial, leaving only
z1,...,z20.  The result is audited over Q(i,sqrt(6)) for term counts, variable
incidence, short equations, and variables that occur linearly.

This script does not claim or solve a categorification.  It is a constructive
structure probe and uses no Groebner basis.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque

import sympy as sp

import r22_phase5_local_rewrite as lr
import r22_phase5_monomial_lift as ml


P = -(sp.Integer(1) + sp.I) / 2
Q = (sp.Integer(1) - sp.I) / 2
Z0_POS = (sp.sqrt(6) - 2) / 2
Z0_NEG = -(sp.sqrt(6) + 2) / 2


def gc_expr(c):
    return sp.Rational(c[0].numerator, c[0].denominator) + sp.I * sp.Rational(c[1].numerator, c[1].denominator)


def specialize_reduced(poly, z0_value):
    """Substitute p,q,z0 after the five-relation exact reduction."""
    out = defaultdict(lambda: sp.Integer(0))
    for mon, c in poly.items():
        coeff = gc_expr(c) * P ** mon[0] * Q ** mon[1] * z0_value ** mon[2]
        zm = tuple(mon[3:])  # z1,...,z20
        out[zm] += coeff

    ans = {}
    for m, c in out.items():
        c = sp.expand(c)
        # nsimplify against sqrt(6) is deterministic here and keeps the field
        # representation compact without introducing floating arithmetic.
        c = sp.collect(c, sp.sqrt(6))
        if c != 0:
            ans[m] = c
    return ans


def normalize(poly):
    if not poly:
        return None
    mons = sorted(poly, reverse=True)
    lead = poly[mons[0]]
    return tuple((m, sp.cancel(poly[m] / lead)) for m in mons)


def variable_set(poly):
    return {j for m in poly for j, e in enumerate(m, start=1) if e}


def graph_components(nvars, polynomials):
    adj = {i: set() for i in range(1, nvars + 1)}
    used = set()
    for poly in polynomials:
        vs = sorted(variable_set(poly))
        used.update(vs)
        for i in vs:
            adj[i].update(j for j in vs if j != i)

    comps = []
    seen = set()
    for s in sorted(used):
        if s in seen:
            continue
        q = deque([s]); seen.add(s); comp = []
        while q:
            x = q.popleft(); comp.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); q.append(y)
        comps.append(tuple(sorted(comp)))
    unused = tuple(i for i in range(1, nvars + 1) if i not in used)
    return comps, unused


def linear_variables(poly):
    ans = []
    for j in variable_set(poly):
        k = j - 1
        exps = [m[k] for m in poly]
        if max(exps) <= 1 and 1 in exps and 0 in exps:
            ans.append(j)
    return tuple(ans)


def analyze(cid, mask, root_name):
    z0_value = Z0_POS if root_name == "positive" else Z0_NEG
    quotient, unique = ml.compile_unique(cid, mask)

    specialized = {}
    identically_zero = []
    term_profile = Counter()
    degree_profile = Counter()
    var_count_profile = Counter()
    linear_var_frequency = Counter()
    short = []
    constant_contradictions = []

    for key, prov in unique.items():
        reduced = lr.reduce_poly(key)
        poly = specialize_reduced(reduced, z0_value)
        if not poly:
            identically_zero.append(prov)
            continue
        nk = normalize(poly)
        specialized.setdefault(nk, prov)

    for key, prov in specialized.items():
        poly = dict(key)
        nt = len(key)
        deg = max(sum(m) for m, _c in key)
        vs = variable_set(poly)
        term_profile[nt] += 1
        degree_profile[deg] += 1
        var_count_profile[len(vs)] += 1
        for j in linear_variables(poly):
            linear_var_frequency[j] += 1
        if not vs:
            constant_contradictions.append((key, prov))

    for key, prov in sorted(specialized.items(), key=lambda kv: (len(kv[0]), max(sum(m) for m, _c in kv[0]), len(variable_set(dict(kv[0]))), str(kv[1])))[:32]:
        poly = dict(key)
        short.append({
            "terms": len(key),
            "degree": max(sum(m) for m, _c in key),
            "variables": sorted(variable_set(poly)),
            "linear_variables": list(linear_variables(poly)),
            "provenance": prov,
            "poly": str(key),
        })

    comps, unused = graph_components(20, [dict(k) for k in specialized])

    # On this chosen p,q root both product relations become the same constant.
    product_constant = sp.simplify(-z0_value / 2)
    out = {
        "component": cid,
        "mask": mask,
        "root": root_name,
        "p": str(P),
        "q": str(Q),
        "p_over_q": str(sp.simplify(P / Q)),
        "z0": str(z0_value),
        "z0_equals_inverse_FPdim": bool(sp.simplify(z0_value - 1 / (2 + sp.sqrt(6))) == 0) if root_name == "positive" else False,
        "z1z8_equals_z2z3": str(product_constant),
        "base_kernel_polynomials": len(unique),
        "identically_zero_after_five_relations_and_stratum": len(identically_zero),
        "unique_specialized_polynomials": len(specialized),
        "term_count_profile": dict(term_profile),
        "degree_profile": dict(degree_profile),
        "variable_count_profile": dict(var_count_profile),
        "constant_contradictions": len(constant_contradictions),
        "variable_incidence_components": comps,
        "unused_variables": unused,
        "linear_variable_frequency": dict(sorted(linear_var_frequency.items())),
        "shortest": short,
    }
    print(out, flush=True)
    if constant_contradictions:
        print("RESULT: exact stratum is excluded by a constant specialized equation", constant_contradictions[0][1], flush=True)
    else:
        print("RESULT: exact stratum survives structural specialization; continue constructive solving", flush=True)
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
