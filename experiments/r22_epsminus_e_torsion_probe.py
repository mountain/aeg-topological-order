"""Exact Phase-3 E-layer probe for the second physical D-amplitude sheet.

The theorem audit found two gauge-inequivalent cross-D amplitude classes for
each deep epsilon-minus scalar/chirality branch.  Historical Phase-3 work used
only class 0.  This probe compares class 0 and class 1 on one branch using the
same complete E pentagon engine and exact determinant tests.

No numerical solving is used for the proof gate.  If an invertible E locus
exists, an explicit exact point is chosen only after every required E-block
determinant is proved to be a nonzero polynomial, and that point is substituted
back into all original E-layer pentagon entries.
"""
from __future__ import annotations

import argparse
from collections import Counter

import sympy as sp

import r22_epsminus_d_torsion_branch as tb
import r22_epsminus_e_filter as ef


def determinant_profile(dets, params):
    """Summarize exact E determinants in the current free-root coordinates."""
    profile = Counter()
    term_counts = Counter()
    for key, det in dets.items():
        if det == 0:
            profile[("ZERO", key)] += 1
            continue
        poly = sp.Poly(sp.expand(det), *params)
        terms = poly.terms()
        term_counts[len(terms)] += 1
        if len(terms) == 1:
            powers, coeff = terms[0]
            if coeff == 0:
                raise AssertionError(("zero determinant coefficient", key, det))
            profile[tuple(int(x) for x in powers)] += 1
        else:
            profile[("terms", len(terms))] += 1
    return dict(profile), dict(term_counts)


def solve(cid: int, mask: int, amplitude_class: int):
    scalar, ddata, droot, d_checked, d_exponents = tb.exact_d_data(
        cid, mask, amplitude_class
    )
    uf, support, total_entries, n_eq, provenance = ef.build_weighted_system(
        scalar, ddata
    )
    roots, params, _mats, dets = ef.parametric_blocks(uf)
    nullity = len(roots)
    rank = 128 - nullity
    zero_dets = [key for key, det in dets.items() if det == 0]
    det_profile, det_term_counts = determinant_profile(dets, params)

    result = {
        "component": cid,
        "mask": mask,
        "D_amplitude_class": amplitude_class,
        "D_root_group": droot,
        "D_verified_entries": d_checked,
        "D_exponent_profile": dict(Counter(int(x) % 8 for x in d_exponents)),
        "E_total_matrix_entries": total_entries,
        "E_equations": n_eq,
        "E_support": dict(support),
        "E_rank": rank,
        "E_nullity": nullity,
        "E_free_roots": tuple(roots),
        "E_zero_determinant_blocks": zero_dets,
        "E_determinant_monomial_profile": det_profile,
        "E_determinant_term_counts": det_term_counts,
    }

    if nullity == 0:
        result["status"] = "E_ZERO_ONLY"
        print(result, flush=True)
        return result

    if zero_dets:
        result["status"] = "E_SINGULAR"
        print(result, flush=True)
        return result

    root_values = ef.choose_root_values(
        roots, params, dets, seed=100000 * amplitude_class + cid * 1000 + mask
    )
    if root_values is None:
        raise RuntimeError((
            "all determinant polynomials are nonzero but no explicit invertible E point was found",
            cid,
            mask,
            amplitude_class,
            det_profile,
        ))
    edata = ef.root_values_to_edata(uf, roots, root_values)
    bad_blocks = [key for key, M in edata.items() if sp.cancel(M.det()) == 0]
    if bad_blocks:
        raise RuntimeError(("chosen E point is singular", cid, mask, amplitude_class, bad_blocks))
    checked, failures = ef.verify_e(scalar, ddata, edata)
    if failures:
        raise RuntimeError((
            "characteristic-zero E replay failed",
            cid,
            mask,
            amplitude_class,
            failures,
        ))

    result.update({
        "explicit_E_root_values": tuple(str(sp.simplify(x)) for x in root_values),
        "E_verified_matrix_entries": checked,
        "all_32_det_polynomials_nonzero": True,
        "status": "E_PASS",
    })
    print(result, flush=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    args = ap.parse_args()

    base = solve(args.component, args.mask, 0)
    torsion = solve(args.component, args.mask, 1)

    comparison = {
        "component": args.component,
        "mask": args.mask,
        "base_status": base["status"],
        "torsion_status": torsion["status"],
        "same_E_equation_count": base["E_equations"] == torsion["E_equations"],
        "same_E_support": base["E_support"] == torsion["E_support"],
        "same_E_rank": base["E_rank"] == torsion["E_rank"],
        "same_E_nullity": base["E_nullity"] == torsion["E_nullity"],
        "same_det_monomial_profile": (
            base["E_determinant_monomial_profile"]
            == torsion["E_determinant_monomial_profile"]
        ),
    }
    print("COMPARISON", comparison, flush=True)
    print(
        "RESULT: second-sheet E-layer fingerprint completed exactly; "
        "inspect torsion_status before advancing the branch census",
        flush=True,
    )


if __name__ == "__main__":
    main()
