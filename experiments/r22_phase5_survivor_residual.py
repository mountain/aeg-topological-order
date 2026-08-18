"""Project one surviving finite Phase-5 stratum through its full affine closure.

The complete 3x3 cube-root audit leaves several branches that survive the first
three diagnostic cells.  For one selected (a,b,z0-root) branch this script:

1. compiles the 219 exact final-kernel polynomials once;
2. applies the five proved local rewrite identities;
3. substitutes the selected exact p,q,z0 values;
4. independently reconstructs the safely localized affine RREF;
5. substitutes all affine pivot expressions and the proved product relations
   for z3,z8;
6. clears only denominators in z1,z2, which are already proved nonzero;
7. reports the exact residual kernel over Q(i,sqrt(3),sqrt(6)).

No Groebner basis or nonlinear solving is used.  The development gate is the
first surviving branch a=b=1 with the positive z0 root.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque

import sympy as sp

import r22_phase5_ratio_classes as rc


FIELD_EXT = [sp.I, rc.SQ3, rc.SQ6]


def branch_values(a, b, root_name):
    p = sp.expand(rc.P0 * rc.OMEGA ** a)
    q = sp.expand(rc.Q0 * rc.OMEGA ** b)
    t = rc.Z0_ROOTS[root_name]
    return p, q, t


def build_substitution(exprs, p, q, t):
    # z1,z2,z3,z8 are known nonzero.  Product identities therefore solve z3,z8
    # without introducing any unproved localization.
    product = {
        rc.ZS[2]: sp.I * p ** 2 * t / rc.ZS[1],
        rc.ZS[7]: -sp.I * q ** 2 * t / rc.ZS[0],
    }
    subs = {}
    for j, rhs in exprs.items():
        subs[rc.ZS[j]] = sp.cancel(rhs.subs(product))
    subs.update(product)
    return subs


def canonical_residual(expr, free_symbols):
    expr = sp.cancel(expr)
    if expr == 0:
        return None
    num, den = sp.fraction(expr)
    # The only legal variable denominators are z1,z2, already proved nonzero.
    bad = den.free_symbols - {rc.ZS[0], rc.ZS[1]}
    if bad:
        raise RuntimeError(("unexpected residual denominator", den, sorted(map(str, bad))))
    num = sp.expand(num)
    if num == 0:
        return None
    poly = sp.Poly(num, *free_symbols, extension=FIELD_EXT)
    if poly.is_zero:
        return None
    monic = poly.monic()
    # Domain coefficients have a canonical exact string representation inside
    # one fixed algebraic extension; use it only as a hash key/report form.
    return tuple((tuple(int(x) for x in mon), str(coeff)) for mon, coeff in monic.terms())


def vars_in(key, free_symbols):
    return {free_symbols[j] for mon, _c in key for j, e in enumerate(mon) if e}


def incidence_components(keys, free_symbols):
    idx = {s: i for i, s in enumerate(free_symbols)}
    adj = {s: set() for s in free_symbols}
    used = set()
    for key in keys:
        vs = sorted(vars_in(key, free_symbols), key=lambda s: idx[s])
        used.update(vs)
        for x in vs:
            adj[x].update(y for y in vs if y != x)
    seen = set(); comps = []
    for s in free_symbols:
        if s not in used or s in seen:
            continue
        q = deque([s]); seen.add(s); comp = []
        while q:
            x = q.popleft(); comp.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); q.append(y)
        comps.append(tuple(str(x) for x in comp))
    return comps, tuple(str(s) for s in free_symbols if s not in used)


def is_known_nonzero_monomial(key, free_symbols):
    if len(key) != 1:
        return False
    mon, _c = key[0]
    for j, e in enumerate(mon):
        if e and free_symbols[j] not in {rc.ZS[0], rc.ZS[1]}:
            return False
    return True


def analyze(cid, mask, a, b, root_name):
    p, q, t = branch_values(a, b, root_name)
    unique, reduced, _by_prov = rc.compile_reduced_once(cid, mask)
    affine, exprs = rc.affine_closure(unique, reduced, p, q, t)
    if exprs is None:
        raise RuntimeError(("selected branch already affine-inconsistent", a, b, root_name, affine))

    subs = build_substitution(exprs, p, q, t)
    pivot_symbols = {rc.ZS[j] for j in exprs}
    eliminated_product = {rc.ZS[2], rc.ZS[7]}
    free_symbols = tuple(
        z for z in rc.ZS
        if z not in pivot_symbols and z not in eliminated_product
    )

    residual = {}
    vanished = []
    contradictions = []
    known_nonzero_monomials = []
    singleton_unknown = []
    term_profile = Counter()
    degree_profile = Counter()
    var_count_profile = Counter()

    for key, prov in unique.items():
        spoly = rc.specialize_reduced(reduced[key], p, q, t)
        if not spoly:
            vanished.append(prov)
            continue
        expr = rc.zpoly_expr(spoly)
        rem = sp.cancel(expr.subs(subs))
        ck = canonical_residual(rem, free_symbols)
        if ck is None:
            vanished.append(prov)
            continue
        residual.setdefault(ck, prov)

    shortest = []
    univariate = []
    for key, prov in residual.items():
        nt = len(key)
        deg = max(sum(mon) for mon, _c in key)
        vs = vars_in(key, free_symbols)
        term_profile[nt] += 1
        degree_profile[deg] += 1
        var_count_profile[len(vs)] += 1
        if not vs:
            contradictions.append((key, prov))
        if is_known_nonzero_monomial(key, free_symbols):
            known_nonzero_monomials.append((key, prov))
        elif nt == 1:
            singleton_unknown.append((key, prov))
        if len(vs) == 1:
            univariate.append((key, prov, next(iter(vs))))

    for key, prov in sorted(
        residual.items(),
        key=lambda kv: (
            len(vars_in(kv[0], free_symbols)),
            len(kv[0]),
            max(sum(mon) for mon, _c in kv[0]),
            str(kv[1]),
        ),
    )[:40]:
        shortest.append({
            "variables": sorted(str(x) for x in vars_in(key, free_symbols)),
            "terms": len(key),
            "degree": max(sum(mon) for mon, _c in key),
            "provenance": prov,
            "poly": str(key),
        })

    comps, unused = incidence_components(residual.keys(), free_symbols)
    out = {
        "component": cid,
        "mask": mask,
        "cube_pair": (a, b),
        "ratio_class": (a - b) % 3,
        "root": root_name,
        "p": str(p),
        "q": str(q),
        "z0": str(t),
        "affine": affine,
        "free_variables_after_affine_and_products": tuple(str(s) for s in free_symbols),
        "free_variable_count": len(free_symbols),
        "base_kernel_polynomials": len(unique),
        "vanished_after_projection": len(vanished),
        "unique_residual_polynomials": len(residual),
        "term_count_profile": dict(term_profile),
        "degree_profile": dict(degree_profile),
        "variable_count_profile": dict(var_count_profile),
        "constant_contradictions": len(contradictions),
        "proved_nonzero_monomial_contradictions": len(known_nonzero_monomials),
        "singleton_unknown_constraints": len(singleton_unknown),
        "univariate_equations": len(univariate),
        "incidence_components": comps,
        "unused_variables": unused,
        "univariate_examples": [
            {"variable": str(v), "provenance": prov, "poly": str(key)}
            for key, prov, v in univariate[:16]
        ],
        "singleton_unknown_examples": [
            {"provenance": prov, "poly": str(key)}
            for key, prov in singleton_unknown[:16]
        ],
        "shortest": shortest,
    }
    print(out, flush=True)
    if contradictions:
        print("RESULT: survivor projection contains a constant contradiction", contradictions[0][1], flush=True)
    elif known_nonzero_monomials:
        print("RESULT: survivor projection forces a proved-nonzero scaling monomial to vanish", known_nonzero_monomials[0][1], flush=True)
    else:
        print("RESULT: survivor residual kernel compiled; continue exact local reduction", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    ap.add_argument("--a", type=int, default=1, choices=(0, 1, 2))
    ap.add_argument("--b", type=int, default=1, choices=(0, 1, 2))
    ap.add_argument("--root", choices=("positive", "negative"), default="positive")
    args = ap.parse_args()
    analyze(args.component, args.mask, args.a, args.b, args.root)


if __name__ == "__main__":
    main()
