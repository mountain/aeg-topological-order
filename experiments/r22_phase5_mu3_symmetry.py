"""Exact mod-3 grading audit for simultaneous cube-root choices in Phase 5.

The finite local relations fix p^3 and q^3, leaving three cube-root choices for
p and three for q.  We ask whether simultaneous multiplication

    p -> omega*p, q -> omega*q, omega^3=1,

extends to a diagonal omega-action on the 21 independent F-linear components
z_j that preserves BOTH

1. every exact final-kernel polynomial, and
2. every required F-block determinant polynomial.

This is a linear problem over F_3.  For every polynomial/determinant, differences
of exponent vectors must have zero weight.  We fix w_p=w_q=1 and solve for the
z_j weights.  If consistent, the resulting action is an exact symmetry of the
Phase-4 quotient and final coherence: E entries all acquire the same omega
factor, F-linear connected components may be independently rescaled, final
polynomials are weight-homogeneous, and required determinants scale by a single
nonzero omega power.
"""
from __future__ import annotations

import argparse
from collections import Counter

import r22_epsminus_f_parametric as fp
import r22_phase5_monomial_lift as ml


MOD = 3


def add_homogeneity_rows(rows, monomials):
    mons = list(monomials)
    if len(mons) <= 1:
        return
    base = mons[0]
    for m in mons[1:]:
        rows.append(tuple((a - b) % MOD for a, b in zip(m, base)))


def solve_mod3(rows, nvars, fixes):
    aug = [list(r) + [0] for r in rows]
    for j, value in fixes.items():
        row = [0] * nvars
        row[j] = 1
        aug.append(row + [value % MOD])

    rank = 0
    pivots = []
    for c in range(nvars):
        p = next((i for i in range(rank, len(aug)) if aug[i][c] % MOD), None)
        if p is None:
            continue
        aug[rank], aug[p] = aug[p], aug[rank]
        inv = 1 if aug[rank][c] % MOD == 1 else 2
        aug[rank] = [(x * inv) % MOD for x in aug[rank]]
        for i in range(len(aug)):
            if i == rank or aug[i][c] % MOD == 0:
                continue
            q = aug[i][c] % MOD
            aug[i] = [(x - q * y) % MOD for x, y in zip(aug[i], aug[rank])]
        pivots.append(c)
        rank += 1

    for row in aug:
        if all(x % MOD == 0 for x in row[:nvars]) and row[nvars] % MOD:
            return None, {"rank": rank, "pivots": tuple(pivots), "inconsistent": True}

    sol = [0] * nvars
    for i, c in enumerate(pivots):
        sol[c] = aug[i][nvars] % MOD
    free = tuple(j for j in range(nvars) if j not in pivots)
    return tuple(sol), {"rank": rank, "pivots": tuple(pivots), "free": free, "inconsistent": False}


def weight(mon, w):
    return sum(a * b for a, b in zip(mon, w)) % MOD


def analyze(cid, mask):
    _quotient, unique = ml.compile_unique(cid, mask)
    nvars = len(next(iter(unique))[0][0]) if False else 23
    # The branch under study has exactly p,q plus 21 F components.
    if nvars != 23:
        raise RuntimeError(nvars)

    rows = []
    final_profile = Counter()
    for key in unique:
        mons = [tuple(mon) for mon, _gc in key]
        final_profile[len(mons)] += 1
        add_homogeneity_rows(rows, mons)
    n_final_rows = len(rows)

    # Rebuild the generic Phase-4 F quotient to get exact determinant monomials.
    scalar, ddata, params, emats, _droot = fp.parametric_lower_data(cid, mask)
    uf, _support, _degrees, _neq = fp.build_f_system(scalar, ddata, params, emats)
    profile, _kvals = fp.root_condition_profile(uf)
    active = sorted(fp.active_roots(profile))
    if len(active) != 21:
        raise RuntimeError(("expected 21 active F components", len(active)))
    active_set = set(active)
    zindex = {r: i for i, r in enumerate(active)}

    determinant_profiles = []
    for block, dim in fp.F_BLOCKS:
        det = fp.determinant_generic(fp.block_descriptor(uf, profile, block, active_set))
        if not det:
            raise RuntimeError(("required determinant vanished before symmetry audit", block))
        exps = []
        for (root_mon, _r_exp), _c in det.items():
            v = [0] * 23
            for r in root_mon:
                v[2 + zindex[r]] += 1
            exps.append(tuple(x % MOD for x in v))
        before = len(rows)
        add_homogeneity_rows(rows, exps)
        determinant_profiles.append({"block": block, "dim": dim, "terms": len(det), "grading_rows": len(rows) - before})
    n_det_rows = len(rows) - n_final_rows

    w, meta = solve_mod3(rows, 23, {0: 1, 1: 1})
    out = {
        "component": cid,
        "mask": mask,
        "field": "F_3",
        "variables": ("p", "q") + tuple(f"z{i}" for i in range(21)),
        "final_polynomials": len(unique),
        "final_term_profile": dict(final_profile),
        "final_grading_rows": n_final_rows,
        "determinant_grading_rows": n_det_rows,
        "linear_system": meta,
        "simultaneous_mu3_symmetry_exists": w is not None,
        "weights": w,
        "determinant_profiles": determinant_profiles,
    }

    if w is not None:
        # Independent exact verification against the solved weight vector.
        bad_final = []
        for key, prov in unique.items():
            ws = {weight(tuple(mon), w) for mon, _gc in key}
            if len(ws) != 1:
                bad_final.append((prov, sorted(ws)))
        bad_det = []
        det_weights = {}
        for block, _dim in fp.F_BLOCKS:
            det = fp.determinant_generic(fp.block_descriptor(uf, profile, block, active_set))
            ws = set()
            for (root_mon, _r_exp), _c in det.items():
                v = [0] * 23
                for r in root_mon:
                    v[2 + zindex[r]] += 1
                ws.add(weight(tuple(v), w))
            det_weights[str(block)] = sorted(ws)
            if len(ws) != 1:
                bad_det.append((block, sorted(ws)))
        out["bad_final_polynomials"] = bad_final
        out["bad_required_determinants"] = bad_det
        out["required_determinant_weights"] = det_weights
        out["verified"] = not bad_final and not bad_det and w[0] == w[1] == 1
    else:
        out["verified"] = False

    print(out, flush=True)
    if out["verified"]:
        print("RESULT: simultaneous mu3 cube-root choices are exactly equivalent by a diagonal Phase-5 grading symmetry", flush=True)
    else:
        print("RESULT: no verified simultaneous mu3 symmetry; remaining cube-root pairs must be audited separately", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    args = ap.parse_args()
    analyze(args.component, args.mask)


if __name__ == "__main__":
    main()
