"""Phase-5 local invertibility probe for the generic F-linear quotient.

The probe first identifies common monomial factors of required F determinants.
It then tests a concrete local branch forced by the four shortest final
pentagon equations.  If z0=0, those binomials imply

    z2*z3 = 0,    z1*z8 = 0,

so only four zero-pattern branches remain.  We test each branch by exact support
restriction of every required determinant polynomial.  A determinant is killed
iff no monomial survives after the indicated z variables are set to zero.

No nonlinear solving or Groebner computation is used.
"""
from __future__ import annotations

import argparse
from collections import defaultdict

import r22_epsminus_f_parametric as fp


def surviving_terms(det, zero_roots):
    return sum(1 for (mon, _rexp) in det if not any(r in zero_roots for r in mon))


def probe(cid, mask):
    scalar, ddata, params, emats, droot = fp.parametric_lower_data(cid, mask)
    uf, support, _degrees, n_eq = fp.build_f_system(scalar, ddata, params, emats)
    profile, k_values = fp.root_condition_profile(uf)
    active = sorted(fp.active_roots(profile))
    active_set = set(active)
    zindex = {r: i for i, r in enumerate(active)}

    conditional = [r for r, info in profile.items() if not info["forced"] and info["conditions"]]
    forced = [r for r, info in profile.items() if info["forced"]]

    by_root = defaultdict(list)
    determinants = {}
    block_rows = []
    for key, dim in fp.F_BLOCKS:
        desc = fp.block_descriptor(uf, profile, key, active_set)
        det = fp.determinant_generic(desc)
        if not det:
            raise RuntimeError(("generic determinant vanished", cid, mask, key))
        determinants[key] = det

        mins = {r: min(mon.count(r) for mon, _rexp in det) for r in active}
        common = {zindex[r]: m for r, m in mins.items() if m > 0}
        for zi, power in common.items():
            by_root[zi].append((key, power))

        root_support = sorted({zindex[r] for mon, _rexp in det for r in set(mon) if r in zindex})
        r_exponents = sorted({rexp for _mon, rexp in det})
        block_rows.append(
            {
                "block": key,
                "dim": dim,
                "det_terms": len(det),
                "common_z_factors": common,
                "z_support": root_support,
                "r_exponents": r_exponents,
            }
        )

    mandatory = sorted(by_root)

    # The four exact two-term final pentagon equations printed by the Phase-5
    # compiler imply these branches under z0=0:
    #   z2*z3=0 and z1*z8=0.
    zero_patterns = [
        (0, 2, 1),
        (0, 2, 8),
        (0, 3, 1),
        (0, 3, 8),
    ]
    branch_tests = []
    for pattern in zero_patterns:
        zero_roots = {active[zi] for zi in pattern}
        survivors = {key: surviving_terms(det, zero_roots) for key, det in determinants.items()}
        killed = [key for key, n in survivors.items() if n == 0]
        branch_tests.append(
            {
                "zero_z": pattern,
                "killed_blocks": killed,
                "XXXX_surviving_det_terms": survivors[("X", "X", "X", "X")],
                "min_surviving_det_terms": min(survivors.values()),
            }
        )

    z0_branch_excluded = all(row["killed_blocks"] for row in branch_tests)
    out = {
        "component": cid,
        "mask": mask,
        "D_root_group": droot,
        "F_linear_equations": n_eq,
        "F_linear_support": dict(support),
        "active_components": len(active),
        "conditional_components": len(conditional),
        "forced_zero_components": len(forced),
        "E_ratio_condition_modulus": fp.candidate_modulus(k_values),
        "mandatory_nonzero_z": mandatory,
        "mandatory_by_block": {f"z{zi}": rows for zi, rows in sorted(by_root.items())},
        "z0_zero_branch_tests": branch_tests,
        "z0_zero_branch_excluded_by_binomials_plus_invertibility": z0_branch_excluded,
        "block_profiles": block_rows,
    }
    print(out, flush=True)

    if z0_branch_excluded:
        print("RESULT: four binomial pentagon entries plus F invertibility force z0 != 0", flush=True)
    elif 0 in by_root:
        print("RESULT: F invertibility alone forces z0 != 0", flush=True)
    else:
        print("RESULT: current local data do not yet force z0 != 0", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    args = ap.parse_args()
    probe(args.component, args.mask)


if __name__ == "__main__":
    main()
