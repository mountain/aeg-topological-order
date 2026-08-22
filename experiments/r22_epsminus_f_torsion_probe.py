"""Exact parametric Phase-4 probe for the second physical D-amplitude sheet.

This is the Phase-4 analogue of r22_epsminus_e_torsion_probe.py.  It injects
D-amplitude class 1, rebuilds its exact two-parameter E torus, then compiles the
complete F-linear coherence system and checks simultaneous invertibility of all
sixteen required 8x8/10x10 F blocks on generic and finite E-ratio strata.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict

import sympy as sp

import r22_epsminus_d_torsion_branch as tb
import r22_epsminus_e_filter as ef
import r22_epsminus_f_parametric as fp


def second_sheet_lower_data(cid: int, mask: int):
    scalar, ddata, droot, d_checked, d_exponents = tb.exact_d_data(cid, mask, 1)
    euf, esupport, _total, eneq, _prov = ef.build_weighted_system(scalar, ddata)
    roots, params, emats, dets = ef.parametric_blocks(euf)

    zero_e_dets = [key for key, det in dets.items() if det == 0]
    if zero_e_dets:
        raise RuntimeError(("second-sheet E determinant vanished before Phase 4", cid, mask, zero_e_dets))
    if len(roots) != 2:
        raise RuntimeError(("second-sheet E nullity is not two", cid, mask, roots))

    e_det_profile = Counter()
    for key, det in dets.items():
        poly = sp.Poly(sp.expand(det), *params)
        terms = poly.terms()
        if len(terms) != 1:
            raise RuntimeError(("second-sheet E determinant nonmonomial", cid, mask, key, det))
        powers, coeff = terms[0]
        if coeff == 0:
            raise RuntimeError(("second-sheet E determinant zero coefficient", cid, mask, key))
        e_det_profile[tuple(int(x) for x in powers)] += 1

    return {
        "scalar": scalar,
        "ddata": ddata,
        "droot": droot,
        "d_checked": d_checked,
        "d_exponent_profile": dict(Counter(int(x) % 8 for x in d_exponents)),
        "e_support": dict(esupport),
        "e_equations": eneq,
        "e_roots": tuple(roots),
        "e_params": params,
        "emats": emats,
        "e_det_profile": dict(e_det_profile),
    }


def analyze(cid: int, mask: int):
    lower = second_sheet_lower_data(cid, mask)
    params = lower["e_params"]
    uf, support, coefficient_degrees, n_eq = fp.build_f_system(
        lower["scalar"], lower["ddata"], params, lower["emats"]
    )
    profile, k_values = fp.root_condition_profile(uf)
    generic_active = set(fp.active_roots(profile))
    L = fp.candidate_modulus(k_values)
    if L > 128:
        raise RuntimeError(("unexpected second-sheet E-ratio modulus", cid, mask, L, sorted(set(k_values))))

    generic_bad = []
    generic_det_terms = {}
    for key, _dim in fp.F_BLOCKS:
        desc = fp.block_descriptor(uf, profile, key, generic_active)
        det = fp.determinant_generic(desc)
        generic_det_terms[key] = len(det)
        if not det:
            generic_bad.append(key)

    passing = []
    finite_summaries = Counter()
    for u in range(L):
        active = set(fp.active_roots(profile, u=u, L=L))
        bad = []
        for key, _dim in fp.F_BLOCKS:
            if not fp.determinant_finite_nonzero(
                fp.block_descriptor(uf, profile, key, active), u, L
            ):
                bad.append(key)
        finite_summaries[(len(active), len(bad))] += 1
        if not bad:
            passing.append(u)

    condition_counts = Counter()
    for info in profile.values():
        if info["forced"]:
            condition_counts["forced"] += 1
        elif info["conditions"]:
            condition_counts["conditional"] += 1
        else:
            condition_counts["free"] += 1

    passing_desc = ([] if generic_bad else ["generic"]) + [f"zeta_{L}^{u}" for u in passing]
    result = {
        "component": cid,
        "mask": mask,
        "D_amplitude_class": 1,
        "D_root_group": lower["droot"],
        "D_verified_entries": lower["d_checked"],
        "D_exponent_profile": lower["d_exponent_profile"],
        "E_equations": lower["e_equations"],
        "E_support": lower["e_support"],
        "E_nullity": len(lower["e_roots"]),
        "E_determinant_monomial_profile": lower["e_det_profile"],
        "F_equations": n_eq,
        "F_support": dict(support),
        "F_coefficient_E_degrees": {str(k): v for k, v in coefficient_degrees.items()},
        "F_component_condition_profile": dict(condition_counts),
        "E_ratio_modulus": L,
        "generic_active_F_components": len(generic_active),
        "generic_bad_blocks": generic_bad,
        "generic_required_det_term_counts": {
            str(key): n for key, n in generic_det_terms.items()
        },
        "finite_strata_profile": {str(k): v for k, v in finite_summaries.items()},
        "passing_E_ratio_strata": passing_desc,
        "status": "F_PASS" if passing_desc else "F_SINGULAR_FOR_ALL_E",
    }
    print(result, flush=True)
    print(
        "RESULT: second-sheet representative Phase-4 fingerprint completed exactly; "
        "inspect status and weighted-component profile before branch propagation",
        flush=True,
    )
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    args = ap.parse_args()
    analyze(args.component, args.mask)


if __name__ == "__main__":
    main()
