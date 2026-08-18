"""Cheap exact residual scan for one surviving finite Phase-5 stratum.

This is the replacement for full algebraic-number canonicalization of the
8-variable residual kernel.  It keeps every equation tied to its provenance and
uses SymPy's EX coefficient domain only to separate monomials from exact radical
coefficients.  No global monic normalization and no cross-equation deduplication
is attempted.

For the selected branch it:
  * reuses the five exact local rewrite identities;
  * independently rebuilds the safe affine closure;
  * substitutes the affine pivots plus the proved z3/z8 product relations;
  * clears only denominators in the already-proved nonzero z1,z2;
  * scans all 219 equations for constant contradictions, proved-nonzero
    monomials, singleton zero constraints, low term count and low variable
    support.

This is exact certificate discovery, not a nonlinear solver.
"""
from __future__ import annotations

import argparse
from collections import Counter

import sympy as sp

import r22_phase5_ratio_classes as rc


def branch_values(a, b, root_name):
    return (
        sp.expand(rc.P0 * rc.OMEGA ** a),
        sp.expand(rc.Q0 * rc.OMEGA ** b),
        rc.Z0_ROOTS[root_name],
    )


def build_substitution(exprs, p, q, t):
    product = {
        rc.ZS[2]: sp.I * p ** 2 * t / rc.ZS[1],
        rc.ZS[7]: -sp.I * q ** 2 * t / rc.ZS[0],
    }
    subs = {rc.ZS[j]: rhs.subs(product) for j, rhs in exprs.items()}
    subs.update(product)
    return subs


def clear_legal_denominator(expr):
    expr = sp.together(expr)
    num, den = sp.fraction(expr)
    bad = den.free_symbols - {rc.ZS[0], rc.ZS[1]}
    if bad:
        raise RuntimeError(("unexpected residual denominator", den, sorted(map(str, bad))))
    return sp.expand(num)


def exact_nonzero(x):
    return sp.simplify(x) != 0


def scan(cid, mask, a, b, root_name):
    p, q, t = branch_values(a, b, root_name)
    unique, reduced, _by_prov = rc.compile_reduced_once(cid, mask)
    affine, exprs = rc.affine_closure(unique, reduced, p, q, t)
    if exprs is None:
        raise RuntimeError(("selected branch affine-inconsistent", a, b, root_name, affine))

    subs = build_substitution(exprs, p, q, t)
    pivot_symbols = {rc.ZS[j] for j in exprs}
    free_symbols = tuple(
        z for z in rc.ZS
        if z not in pivot_symbols and z not in {rc.ZS[2], rc.ZS[7]}
    )
    known_nonzero = {rc.ZS[0], rc.ZS[1]}

    term_profile = Counter()
    degree_profile = Counter()
    var_profile = Counter()
    vanished = 0
    constants = []
    known_nonzero_monomials = []
    singleton_unknown = []
    univariate = []
    records = []

    for key, prov in unique.items():
        spoly = rc.specialize_reduced(reduced[key], p, q, t)
        if not spoly:
            vanished += 1
            continue
        expr = rc.zpoly_expr(spoly)
        num = clear_legal_denominator(expr.subs(subs))
        if num == 0:
            vanished += 1
            continue

        poly = sp.Poly(num, *free_symbols, domain="EX")
        terms = []
        for mon, coeff in poly.terms():
            cc = sp.simplify(coeff)
            if cc != 0:
                terms.append((tuple(int(x) for x in mon), cc))
        if not terms:
            vanished += 1
            continue

        nt = len(terms)
        deg = max(sum(mon) for mon, _c in terms)
        used_idx = sorted({j for mon, _c in terms for j, e in enumerate(mon) if e})
        used = tuple(free_symbols[j] for j in used_idx)
        term_profile[nt] += 1
        degree_profile[deg] += 1
        var_profile[len(used)] += 1

        rec = {
            "provenance": prov,
            "terms": nt,
            "degree": deg,
            "variables": tuple(str(x) for x in used),
            "poly": tuple((mon, str(c)) for mon, c in terms),
        }
        records.append(rec)

        if not used:
            coeffs = [c for _m, c in terms]
            if any(exact_nonzero(c) for c in coeffs):
                constants.append(rec)
            continue

        if nt == 1:
            mon, coeff = terms[0]
            if exact_nonzero(coeff):
                vars_in_mon = {free_symbols[j] for j, e in enumerate(mon) if e}
                if vars_in_mon <= known_nonzero:
                    known_nonzero_monomials.append(rec)
                else:
                    singleton_unknown.append(rec)

        if len(used) == 1:
            univariate.append(rec)

    records.sort(key=lambda r: (len(r["variables"]), r["terms"], r["degree"], str(r["provenance"])))
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
        "equations_scanned": len(unique),
        "vanished_after_projection": vanished,
        "surviving_equations": len(records),
        "term_count_profile": dict(term_profile),
        "degree_profile": dict(degree_profile),
        "variable_count_profile": dict(var_profile),
        "constant_contradictions": len(constants),
        "proved_nonzero_monomial_contradictions": len(known_nonzero_monomials),
        "singleton_unknown_constraints": len(singleton_unknown),
        "univariate_equations": len(univariate),
        "constant_examples": constants[:8],
        "proved_nonzero_monomial_examples": known_nonzero_monomials[:8],
        "singleton_unknown_examples": singleton_unknown[:12],
        "univariate_examples": univariate[:16],
        "shortest": records[:40],
    }
    print(out, flush=True)
    if constants:
        print("RESULT: survivor scan finds a constant contradiction", constants[0]["provenance"], flush=True)
    elif known_nonzero_monomials:
        print("RESULT: survivor scan forces a proved-nonzero monomial to vanish", known_nonzero_monomials[0]["provenance"], flush=True)
    else:
        print("RESULT: survivor scan is locally consistent; inspect shortest residual equations", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    ap.add_argument("--a", type=int, default=1, choices=(0, 1, 2))
    ap.add_argument("--b", type=int, default=1, choices=(0, 1, 2))
    ap.add_argument("--root", choices=("positive", "negative"), default="positive")
    args = ap.parse_args()
    scan(args.component, args.mask, args.a, args.b, args.root)


if __name__ == "__main__":
    main()
