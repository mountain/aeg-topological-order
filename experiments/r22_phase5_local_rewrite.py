"""Phase-5 exact local rewrite after the z0 certificate.

Use only the five short relations already proved in the local certificate:

    p^3 = (1-i)/4,
    q^3 = -(1+i)/4,
    z2*z3 = i*p^2*z0,
    z1*z8 = -i*q^2*z0,
    z0^2 = 1/2 - 2*z0.

These are oriented as exact rewrite rules and applied to every one of the 219
canonical final-kernel polynomials.  The probe reports the reduced term profile,
constant/singleton contradictions, and a second small-support monomial-lift
search.  It is deliberately not a Groebner computation: every rewrite is one
explicit identity with recorded pentagon provenance in note 25.
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
I = (Fraction(0), Fraction(1))
NEG_I = (Fraction(0), Fraction(-1))
P3 = (Fraction(1, 4), Fraction(-1, 4))
Q3 = (Fraction(-1, 4), Fraction(-1, 4))


def gpow(x, n):
    ans = GONE
    for _ in range(n):
        ans = fp.gmul(ans, x)
    return ans


def add_term(poly, mon, coeff):
    if fp.giszero(coeff):
        return
    old = poly.get(mon, GZERO)
    new = fp.gadd(old, coeff)
    if fp.giszero(new):
        poly.pop(mon, None)
    else:
        poly[mon] = new


def z0_remainder(n):
    """Return a,b with z0^n = a + b*z0 modulo 2*z0^2+4*z0-1."""
    a = Fraction(1)
    b = Fraction(0)
    for _ in range(n):
        a, b = b / 2, a - 2 * b
    return a, b


def reduce_monomial(mon, coeff):
    e = list(mon)
    c = coeff

    # z2*z3 = i*p^2*z0.
    k = min(e[4], e[5])
    if k:
        e[4] -= k
        e[5] -= k
        e[0] += 2 * k
        e[2] += k
        c = fp.gmul(c, gpow(I, k))

    # z1*z8 = -i*q^2*z0.
    k = min(e[3], e[10])
    if k:
        e[3] -= k
        e[10] -= k
        e[1] += 2 * k
        e[2] += k
        c = fp.gmul(c, gpow(NEG_I, k))

    # p^3 and q^3 are constants.
    kp, e[0] = divmod(e[0], 3)
    kq, e[1] = divmod(e[1], 3)
    if kp:
        c = fp.gmul(c, gpow(P3, kp))
    if kq:
        c = fp.gmul(c, gpow(Q3, kq))

    # Reduce z0 to degree <= 1.  This is the only rewrite that branches one
    # monomial into a sum of at most two monomials.
    n0 = e[2]
    a, b = z0_remainder(n0)
    out = {}
    base = list(e)
    base[2] = 0
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
        piece = reduce_monomial(mon, c)
        fk.poly_add_scaled(out, piece)
    return out


def localized_key(poly):
    if not poly:
        return None
    key, _floor = fk.canonical_poly(poly)
    if key is None:
        return None
    return ml.localized_equation(key)


def analyze(cid, mask):
    quotient, unique = ml.compile_unique(cid, mask)

    reduced = {}
    zero_equations = []
    singleton_known_nonzero = []
    singleton_unknown = []
    term_profile = Counter()
    degree_profile = Counter()
    fdegree_profile = Counter()

    groups = defaultdict(list)

    for key, prov in unique.items():
        poly = reduce_poly(key)
        if not poly:
            zero_equations.append(prov)
            continue
        loc = localized_key(poly)
        if loc is None:
            zero_equations.append(prov)
            continue

        support = tuple(mon for mon, _c in loc)
        coeffs = tuple(c for _mon, c in loc)
        groups[support].append((coeffs, prov))
        reduced.setdefault(loc, prov)

        nt = len(loc)
        deg = max(sum(m) for m, _c in loc)
        fdeg = max(sum(m[2:]) for m, _c in loc)
        term_profile[nt] += 1
        degree_profile[deg] += 1
        fdegree_profile[fdeg] += 1

        if nt == 1:
            mon = support[0]
            row = {"monomial": mon, "provenance": prov}
            if ml.monomial_known_nonzero(mon):
                singleton_known_nonzero.append(row)
            else:
                unknown = sorted(k for k, e in enumerate(mon) if e and k not in ml.KNOWN_NONZERO)
                row["unknown_variable_indices"] = unknown
                singleton_unknown.append(row)

    full_rank = []
    direct = []
    forced = []
    rank_profile = Counter()
    for support, equations in groups.items():
        ncols = len(support)
        if not (1 <= ncols <= 4) or len(equations) < 2:
            continue
        rank_all = ml.rank_gaussian([row for row, _prov in equations])
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
            "known_nonzero_columns": [j for j, mon in enumerate(support) if ml.monomial_known_nonzero(mon)],
        }
        full_rank.append(row)
        if row["known_nonzero_columns"]:
            direct.append(row)
        else:
            forced.append(row)

    out = {
        "component": cid,
        "mask": mask,
        "base_relations": 5,
        "unique_kernel_polynomials": len(unique),
        "identically_reduced_to_zero": len(zero_equations),
        "unique_reduced_polynomials": len(reduced),
        "reduced_term_profile": dict(term_profile),
        "reduced_total_degree_profile": dict(degree_profile),
        "reduced_F_degree_profile": dict(fdegree_profile),
        "singleton_known_nonzero_contradictions": len(singleton_known_nonzero),
        "singleton_unknown_constraints": len(singleton_unknown),
        "small_support_rank_profile": {str(k): v for k, v in sorted(rank_profile.items())},
        "full_rank_small_support_groups": len(full_rank),
        "direct_full_rank_contradictions": len(direct),
        "singleton_known_nonzero_examples": singleton_known_nonzero[:12],
        "singleton_unknown_examples": singleton_unknown[:12],
        "direct_full_rank_examples": direct[:12],
        "forced_zero_examples": forced[:12],
    }
    print(out, flush=True)
    if singleton_known_nonzero:
        print("RESULT: local five-relation rewrite produces a direct monomial contradiction", singleton_known_nonzero[0], flush=True)
    elif direct:
        print("RESULT: reduced monomial lift produces a <=4-entry full-rank contradiction", direct[0], flush=True)
    else:
        print("RESULT: five-relation rewrite is consistent at this local linearized gate", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    args = ap.parse_args()
    analyze(args.component, args.mask)


if __name__ == "__main__":
    main()
