"""Phase-5 local invertibility probe for the generic F-linear quotient.

The probe identifies common monomial factors of required F determinants and
then tests zero patterns forced by short final-pentagon equations.  A required
determinant is killed under a zero pattern iff no determinant monomial survives
after those F-component variables are set to zero.

No nonlinear solving or Groebner computation is used.
"""
from __future__ import annotations

import argparse
from collections import defaultdict

import r22_epsminus_f_parametric as fp


def surviving_terms(det, zero_roots):
    return sum(1 for (mon, _rexp) in det if not any(r in zero_roots for r in mon))


def test_pattern(active, determinants, name, pattern):
    zero_roots = {active[zi] for zi in pattern}
    survivors = {key: surviving_terms(det, zero_roots) for key, det in determinants.items()}
    killed = [key for key, n in survivors.items() if n == 0]
    return {
        "name": name,
        "zero_z": pattern,
        "killed_blocks": killed,
        "XXXX_surviving_det_terms": survivors[("X", "X", "X", "X")],
        "min_surviving_det_terms": min(survivors.values()),
    }


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

    # Four binomial equations under z0=0 give z2*z3=0 and z1*z8=0.
    base_patterns = [
        ("A", (0, 2, 1)),
        ("ZB", (0, 2, 8)),
        ("ZC", (0, 3, 1)),
        ("D", (0, 3, 8)),
    ]
    branch_tests = [test_pattern(active, determinants, name, pattern) for name, pattern in base_patterns]

    # Fresh exact specialization of ZC yields the single final-pentagon equation
    # z4=0 from (X,X,X,X;Y) entry (3,27).  Test that derived branch directly.
    derived_tests = [
        test_pattern(active, determinants, "ZC+z4", (0, 3, 1, 4)),
    ]

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
        "derived_zero_branch_tests": derived_tests,
        "block_profiles": block_rows,
    }
    print(out, flush=True)

    zc4 = derived_tests[0]
    if zc4["killed_blocks"]:
        print("RESULT: ZC plus its exact singleton z4=0 violates required F invertibility", flush=True)
    else:
        print("RESULT: ZC+z4 remains F-invertible at determinant-polynomial level", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    args = ap.parse_args()
    probe(args.component, args.mask)


if __name__ == "__main__":
    main()
