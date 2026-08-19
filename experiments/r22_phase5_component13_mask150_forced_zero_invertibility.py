"""Exact F-invertibility gate for component 13 / chirality mask 150 rank-11 strata.

The exact finite census yields two forced-zero types:

    z2=z8=0    on (a,b)=(1,0),(2,0), both z6 signs;
    z12=z16=0  on (a,b)=(0,1),(0,2), both z6 signs.

Rebuild the Phase-4 weighted F quotient and all sixteen required 8x8/10x10
determinant polynomials.  A zero pattern closes a stratum here only if at
least one required determinant loses every monomial after specialization.

No nonlinear solving or additional final-pentagon equation is used.
"""
from __future__ import annotations

import r22_epsminus_f_parametric as fp

CID = 13
MASK = 150
PATTERNS = {
    "p-side-rank11": (2, 8),
    "q-side-rank11": (12, 16),
}


def surviving_terms(det, zero_roots):
    return [(mon, rexp) for mon, rexp in det if not any(r in zero_roots for r in mon)]


def main():
    scalar, ddata, params, emats, droot = fp.parametric_lower_data(CID, MASK)
    uf, support, _degrees, n_eq = fp.build_f_system(scalar, ddata, params, emats)
    profile, _kvalues = fp.root_condition_profile(uf)
    active = sorted(fp.active_roots(profile))
    if len(active) != 21:
        raise AssertionError(("expected 21 active F components", len(active)))
    if any(info["conditions"] for info in profile.values() if not info["forced"]):
        raise AssertionError("unexpected conditional F component")
    active_set = set(active)

    determinants = {}
    for key, _dim in fp.F_BLOCKS:
        desc = fp.block_descriptor(uf, profile, key, active_set)
        det = fp.determinant_generic(desc)
        if not det:
            raise AssertionError(("generic determinant vanished", key))
        determinants[key] = det

    rows = []
    for name, pattern in PATTERNS.items():
        zero_roots = {active[j] for j in pattern}
        killed = []
        surviving_profile = {}
        for key, det in determinants.items():
            surv = surviving_terms(det, zero_roots)
            surviving_profile[key] = {
                "terms": len(surv),
                "r_exponents": tuple(sorted({rexp for _mon, rexp in surv})),
            }
            if not surv:
                killed.append(key)
        row = {
            "type": name,
            "zero_z": pattern,
            "killed_required_blocks": tuple(killed),
            "min_surviving_terms": min(v["terms"] for v in surviving_profile.values()),
            "XXXX": surviving_profile[("X", "X", "X", "X")],
        }
        print(row, flush=True)
        rows.append(row)

    summary = {
        "component": CID,
        "mask": MASK,
        "D_root_group": droot,
        "F_linear_equations": n_eq,
        "F_linear_support": dict(support),
        "patterns": len(rows),
        "closed_by_invertibility": sum(bool(r["killed_required_blocks"]) for r in rows),
    }
    print("SUMMARY", summary, flush=True)
    if summary["closed_by_invertibility"] == len(rows):
        print("RESULT: both mask-150 rank-11 forced-zero strata violate required F invertibility", flush=True)
    else:
        print("RESULT: at least one mask-150 forced-zero stratum remains F-invertible at determinant-polynomial level", flush=True)


if __name__ == "__main__":
    main()
