"""Phase-5 local probe: which F-linear components are forced nonzero by invertibility?

For a generic Phase-4 quotient, compute each required F-block determinant as the
same exact sparse polynomial used by the Phase-4 audit.  The common monomial
factor of a determinant is safe to interpret: if z_j divides every determinant
monomial of any required block, invertibility of that block forces z_j != 0.

This is only a localization probe.  It does not solve any final pentagon.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict

import r22_epsminus_f_parametric as fp


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
    block_rows = []
    for key, dim in fp.F_BLOCKS:
        desc = fp.block_descriptor(uf, profile, key, active_set)
        det = fp.determinant_generic(desc)
        if not det:
            raise RuntimeError(("generic determinant vanished", cid, mask, key))

        mins = {}
        for r in active:
            mins[r] = min(mon.count(r) for mon, _rexp in det)
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
        "block_profiles": block_rows,
    }
    print(out, flush=True)

    if 0 in by_root:
        print("RESULT: F invertibility forces z0 != 0", flush=True)
    else:
        print("RESULT: z0 is not individually forced nonzero by a determinant monomial factor", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    args = ap.parse_args()
    probe(args.component, args.mask)


if __name__ == "__main__":
    main()
