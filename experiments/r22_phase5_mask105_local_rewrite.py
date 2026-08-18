"""Exact five-relation local rewrite for component 5 / chirality mask 105.

Fresh Phase-5 replay gives z0 != 0 and the shortest final-pentagon cells imply

    p^3 = (1+i)/4,
    q^3 = -(1+i)/4,
    z2*z3 = -i*p^2*z0,
    z1*z8 = -i*q^2*z0,
    2*z0^2 + 4*z0 - 1 = 0.

This is deliberately separate from the frozen mask-0 rewrite: only the p-side
relations change sign/conjugation.  Apply these five identities to the fresh
219-polynomial mask-105 kernel, localizing only by the variables already proved
nonzero.  No Groebner basis or nonlinear solve is used.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations

import r22_epsminus_final_kernel as fk
import r22_epsminus_f_parametric as fp
import r22_phase5_monomial_lift as ml

GZERO = (Fraction(0), Fraction(0))
GONE = (Fraction(1), Fraction(0))
NEG_I = (Fraction(0), Fraction(-1))
P3 = (Fraction(1, 4), Fraction(1, 4))
Q3 = (Fraction(-1, 4), Fraction(-1, 4))


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


def reduce_monomial(mon, coeff):
    e = list(mon)
    c = coeff

    # mask 105: z2*z3 = -i*p^2*z0.
    k = min(e[4], e[5])
    if k:
        e[4] -= k
        e[5] -= k
        e[0] += 2 * k
        e[2] += k
        c = fp.gmul(c, gpow(NEG_I, k))

    # z1*z8 = -i*q^2*z0, unchanged from mask 0.
    k = min(e[3], e[10])
    if k:
        e[3] -= k
        e[10] -= k
        e[1] += 2 * k
        e[2] += k
        c = fp.gmul(c, gpow(NEG_I, k))

    kp, e[0] = divmod(e[0], 3)
    kq, e[1] = divmod(e[1], 3)
    if kp:
        c = fp.gmul(c, gpow(P3, kp))
    if kq:
        c = fp.gmul(c, gpow(Q3, kq))

    n0 = e[2]
    a, b = z0_remainder(n0)
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


def reduce_poly(key):
    out = {}
    for mon, c in key_to_poly(key).items():
        fk.poly_add_scaled(out, reduce_monomial(mon, c))
    return out


def localized_key(poly):
    if not poly:
        return None
    key, _floor = fk.canonical_poly(poly)
    if key is None:
        return None
    return ml.localized_equation(key)


def analyze(cid, mask):
    if mask != 105:
        raise ValueError("this probe is intentionally mask-105-specific")
    _quotient, unique = ml.compile_unique(cid, mask)

    reduced = {}
    zero_equations = []
    singleton_known = []
    singleton_unknown = []
    groups = defaultdict(list)
    term_profile = Counter()
    degree_profile = Counter()
    fdegree_profile = Counter()

    for key, prov in unique.items():
        loc = localized_key(reduce_poly(key))
        if loc is None:
            zero_equations.append(prov)
            continue
        reduced.setdefault(loc, prov)
        support = tuple(mon for mon, _c in loc)
        coeffs = tuple(c for _mon, c in loc)
        groups[support].append((coeffs, prov))
        nt = len(loc)
        term_profile[nt] += 1
        degree_profile[max(sum(m) for m, _c in loc)] += 1
        fdegree_profile[max(sum(m[2:]) for m, _c in loc)] += 1
        if nt == 1:
            mon = support[0]
            row = {"monomial": mon, "provenance": prov}
            if ml.monomial_known_nonzero(mon):
                singleton_known.append(row)
            else:
                row["unknown_variable_indices"] = sorted(
                    k for k, e in enumerate(mon) if e and k not in ml.KNOWN_NONZERO
                )
                singleton_unknown.append(row)

    direct = []
    forced = []
    rank_profile = Counter()
    for support, equations in groups.items():
        ncols = len(support)
        if not (1 <= ncols <= 4) or len(equations) < 2:
            continue
        rank_all = ml.rank_gaussian([row for row, _p in equations])
        rank_profile[(ncols, len(equations), rank_all)] += 1
        if rank_all < ncols:
            continue
        found = None
        for choose in range(ncols, min(4, len(equations)) + 1):
            for ids in combinations(range(len(equations)), choose):
                if ml.rank_gaussian([equations[i][0] for i in ids]) == ncols:
                    found = ids
                    break
            if found is not None:
                break
        if found is None:
            continue
        row = {
            "support_size": ncols,
            "equations_used": len(found),
            "support": support,
            "provenance": [equations[i][1] for i in found],
            "known_nonzero_columns": [
                j for j, mon in enumerate(support) if ml.monomial_known_nonzero(mon)
            ],
        }
        (direct if row["known_nonzero_columns"] else forced).append(row)

    out = {
        "component": cid,
        "mask": mask,
        "base_relations": {
            "p3": "(1+i)/4",
            "q3": "-(1+i)/4",
            "z2z3": "-i*p^2*z0",
            "z1z8": "-i*q^2*z0",
            "z0": "2*z0^2+4*z0-1=0",
        },
        "unique_kernel_polynomials": len(unique),
        "identically_reduced_to_zero": len(zero_equations),
        "unique_reduced_polynomials": len(reduced),
        "reduced_term_profile": dict(term_profile),
        "reduced_total_degree_profile": dict(degree_profile),
        "reduced_F_degree_profile": dict(fdegree_profile),
        "singleton_known_nonzero_contradictions": len(singleton_known),
        "singleton_unknown_constraints": len(singleton_unknown),
        "small_support_rank_profile": {str(k): v for k, v in sorted(rank_profile.items())},
        "direct_full_rank_contradictions": len(direct),
        "singleton_known_nonzero_examples": singleton_known[:12],
        "singleton_unknown_examples": singleton_unknown[:12],
        "direct_full_rank_examples": direct[:12],
        "forced_zero_examples": forced[:12],
    }
    print(out, flush=True)
    if singleton_known:
        print("RESULT: mask 105 five-relation rewrite gives a direct monomial contradiction", singleton_known[0], flush=True)
    elif direct:
        print("RESULT: mask 105 reduced monomial lift gives a <=4-entry contradiction", direct[0], flush=True)
    else:
        print("RESULT: mask 105 five-relation rewrite is locally consistent", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=105)
    args = ap.parse_args()
    analyze(args.component, args.mask)


if __name__ == "__main__":
    main()
