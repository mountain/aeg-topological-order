"""Phase-5 exact probe for the two surviving z0=0 branches.

The four shortest final pentagon equations imply that z0=0 splits into four
zero patterns.  Two are already excluded by required F-block invertibility.
This probe substitutes the two surviving patterns into all 96 final pentagons
and recompiles the exact sparse kernel.

The goal is local certificate discovery, not nonlinear solving.  For each branch
we report unique specialized equations, term/degree profiles, torus-monomial
contradictions, one-term equations that force additional F-component products
to vanish, and the shortest equations with exact pentagon-entry provenance.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction

import r22_epsminus_final_kernel as fk


SURVIVING_Z0_BRANCHES = {
    "ZB": (0, 2, 8),  # z0=z2=z8=0
    "ZC": (0, 3, 1),  # z0=z3=z1=0
}


def specialize_zero(poly, zero_var_indices):
    """Set selected variables to zero in a sparse nonnegative-exponent poly."""
    out = {}
    for mon, coeff in poly.items():
        if any(mon[k] for k in zero_var_indices):
            continue
        out[mon] = coeff
    return out


def compile_specialized(cid, mask, name, zero_z):
    quotient = fk.parametric_quotient_data(cid, mask)
    zero_var_indices = {2 + zi for zi in zero_z}

    unique = {}
    raw_nonzero = 0
    raw_surviving = 0
    for p in fk.FINAL_BLOCKS:
        labels = dict(zip("abcd", p[:4]))
        long_side, short_side = fk.pentagon_sparse(labels, p[4], quotient)
        dim = len(long_side)
        for i in range(dim):
            cols = set(long_side[i]) | set(short_side[i])
            for j in cols:
                diff = dict(long_side[i].get(j, {}))
                fk.poly_add_scaled(diff, short_side[i].get(j, {}), (Fraction(-1), Fraction(0)))
                if not diff:
                    continue
                raw_nonzero += 1
                spec = specialize_zero(diff, zero_var_indices)
                if not spec:
                    continue
                raw_surviving += 1
                key, _floor = fk.canonical_poly(spec)
                if key is not None:
                    unique.setdefault(key, (p[:5], (i, j)))

    term_profile = Counter()
    total_degree_profile = Counter()
    fdegree_profile = Counter()
    torus_monomial_contradictions = []
    singleton_zero_constraints = []
    torus_only = []

    for key, prov in unique.items():
        nt, deg, fdeg = fk.poly_stats(key)
        term_profile[nt] += 1
        total_degree_profile[deg] += 1
        fdegree_profile[fdeg] += 1

        if fdeg == 0:
            torus_only.append((key, prov))
            if nt == 1:
                # A nonzero Gaussian coefficient times p^a q^b cannot vanish
                # on the already-proved E torus p*q != 0.
                torus_monomial_contradictions.append((key, prov))
        elif nt == 1:
            singleton_zero_constraints.append((key, prov))

    shortest = []
    for key, prov in sorted(unique.items(), key=lambda kv: (len(kv[0]), fk.poly_stats(kv[0])[2], str(kv[1])))[:20]:
        nt, deg, fdeg = fk.poly_stats(key)
        shortest.append(
            {
                "terms": nt,
                "degree": deg,
                "F_degree": fdeg,
                "provenance": prov,
                "poly": str(key),
            }
        )

    out = {
        "branch": name,
        "zero_z": zero_z,
        "component": cid,
        "mask": mask,
        "kernel_variables_before_specialization": len(quotient["variables"]),
        "remaining_F_components": quotient["F_components"] - len(zero_z),
        "raw_nonzero_before_specialization": raw_nonzero,
        "raw_surviving_after_specialization": raw_surviving,
        "unique_specialized_polynomials": len(unique),
        "term_count_profile": dict(term_profile),
        "total_degree_profile": dict(total_degree_profile),
        "F_degree_profile": dict(fdegree_profile),
        "torus_only_equations": len(torus_only),
        "torus_monomial_contradictions": len(torus_monomial_contradictions),
        "singleton_zero_constraints": len(singleton_zero_constraints),
        "singleton_examples": [
            {"provenance": prov, "poly": str(key)}
            for key, prov in singleton_zero_constraints[:12]
        ],
        "shortest": shortest,
    }
    print(out, flush=True)
    if torus_monomial_contradictions:
        print("RESULT:", name, "is excluded by a torus-monomial final pentagon contradiction", flush=True)
    else:
        print("RESULT:", name, "survives direct zero specialization; continue local branching", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    ap.add_argument("--branch", choices=tuple(SURVIVING_Z0_BRANCHES), action="append")
    args = ap.parse_args()

    names = args.branch or list(SURVIVING_Z0_BRANCHES)
    for name in names:
        compile_specialized(args.component, args.mask, name, SURVIVING_Z0_BRANCHES[name])


if __name__ == "__main__":
    main()
