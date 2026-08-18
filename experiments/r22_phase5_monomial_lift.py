"""Phase-5 monomial-relation lift for short contradiction certificates.

The exact final kernel is nonlinear in p,q,z_j, but linear in the finite set of
monomials that actually occur.  This probe lifts those monomials to temporary
linear coordinates and searches for tiny groups of pentagon equations with the
same support whose Gaussian-rational coefficient matrix has full column rank.

This is only a necessary-condition test in relation space.  It uses no Groebner
basis and no nonlinear solving.  A full-rank support group is useful because it
forces every monomial in that support to vanish.  If one of those monomials is
already known nonzero from the exact local certificate, the selected pentagon
entries form an immediate contradiction certificate.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations

import r22_epsminus_final_kernel as fk
import r22_epsminus_f_parametric as fp


# Proven in notes/25-r22-phase5-z0-certificate.md.
# Variable indices in the Phase-5 kernel are p,q,z0,z1,...,z20.
KNOWN_NONZERO = frozenset({0, 1, 2, 3, 4, 5, 10})


def gfromkey(k):
    (ar, ad), (br, bd) = k
    return Fraction(ar, ad), Fraction(br, bd)


def gneg(x):
    return -x[0], -x[1]


def gsub(x, y):
    return fp.gadd(x, gneg(y))


def compile_unique(cid, mask):
    quotient = fk.parametric_quotient_data(cid, mask)
    unique = {}
    for p in fk.FINAL_BLOCKS:
        labels = dict(zip("abcd", p[:4]))
        long_side, short_side = fk.pentagon_sparse(labels, p[4], quotient)
        for i in range(len(long_side)):
            cols = set(long_side[i]) | set(short_side[i])
            for j in cols:
                diff = dict(long_side[i].get(j, {}))
                fk.poly_add_scaled(diff, short_side[i].get(j, {}), (Fraction(-1), Fraction(0)))
                if not diff:
                    continue
                key, _floor = fk.canonical_poly(diff)
                if key is not None:
                    unique.setdefault(key, (p[:5], (i, j)))
    return quotient, unique


def localized_equation(key):
    """Remove only common factors already proved nonzero."""
    terms = [(tuple(mon), gfromkey(gc)) for mon, gc in key]
    mins = {}
    for k in KNOWN_NONZERO:
        mins[k] = min(mon[k] for mon, _c in terms)
    out = []
    for mon, c in terms:
        mm = list(mon)
        for k, m in mins.items():
            mm[k] -= m
        out.append((tuple(mm), c))
    out.sort(reverse=True)
    return tuple(out)


def monomial_known_nonzero(mon):
    # p and q are included in KNOWN_NONZERO.  Any z variable outside the
    # localized set makes the monomial's nonzeroness unknown.
    return all(e == 0 or k in KNOWN_NONZERO for k, e in enumerate(mon))


def rank_gaussian(rows):
    if not rows:
        return 0
    a = [list(r) for r in rows]
    nr, nc = len(a), len(a[0])
    rank = 0
    for c in range(nc):
        pivot = next((r for r in range(rank, nr) if not fp.giszero(a[r][c])), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = fp.ginv(a[rank][c])
        a[rank] = [fp.gmul(x, inv) for x in a[rank]]
        for r in range(nr):
            if r == rank or fp.giszero(a[r][c]):
                continue
            q = a[r][c]
            a[r] = [gsub(x, fp.gmul(q, y)) for x, y in zip(a[r], a[rank])]
        rank += 1
        if rank == nr:
            break
    return rank


def analyze(cid, mask):
    quotient, unique = compile_unique(cid, mask)

    groups = defaultdict(list)
    localized_singletons = []
    for key, prov in unique.items():
        eq = localized_equation(key)
        support = tuple(mon for mon, _c in eq)
        coeff = tuple(c for _mon, c in eq)
        groups[support].append((coeff, prov))
        if len(support) == 1:
            localized_singletons.append((support[0], prov))

    profile = Counter()
    full_rank_groups = []
    direct_contradictions = []
    forced_zero_groups = []

    for support, equations in groups.items():
        ncols = len(support)
        neqs = len(equations)
        profile[(ncols, neqs)] += 1
        if ncols == 0 or ncols > 4 or neqs < ncols:
            continue

        # Search the smallest possible exact certificate inside this support.
        found = None
        for choose in range(1, min(4, neqs) + 1):
            if choose < ncols:
                continue
            for ids in combinations(range(neqs), choose):
                rows = [equations[i][0] for i in ids]
                if rank_gaussian(rows) == ncols:
                    found = ids
                    break
            if found is not None:
                break
        if found is None:
            continue

        provs = [equations[i][1] for i in found]
        nonzero_cols = [j for j, mon in enumerate(support) if monomial_known_nonzero(mon)]
        row = {
            "support_size": ncols,
            "equations_used": len(found),
            "support": support,
            "provenance": provs,
            "known_nonzero_columns": nonzero_cols,
        }
        full_rank_groups.append(row)
        if nonzero_cols:
            direct_contradictions.append(row)
        else:
            forced_zero_groups.append(row)

    out = {
        "component": cid,
        "mask": mask,
        "kernel_variables": quotient["nvars"],
        "unique_kernel_polynomials": len(unique),
        "known_nonzero_variable_indices": sorted(KNOWN_NONZERO),
        "localized_singletons": len(localized_singletons),
        "support_group_profile": {str(k): v for k, v in sorted(profile.items())},
        "full_rank_small_support_groups": len(full_rank_groups),
        "direct_known_nonzero_contradictions": len(direct_contradictions),
        "forced_zero_groups": len(forced_zero_groups),
        "direct_examples": direct_contradictions[:12],
        "forced_zero_examples": forced_zero_groups[:12],
    }
    print(out, flush=True)
    if direct_contradictions:
        best = min(direct_contradictions, key=lambda x: (x["equations_used"], x["support_size"], str(x["provenance"])))
        print("RESULT: monomial lift found a local full-rank contradiction", best, flush=True)
    else:
        print("RESULT: no direct <=4-entry contradiction from identical small monomial supports", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    args = ap.parse_args()
    analyze(args.component, args.mask)


if __name__ == "__main__":
    main()
