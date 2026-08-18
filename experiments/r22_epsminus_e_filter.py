"""Phase-3 E-layer filter for fresh epsilon=-1 R(2,2) survivors.

Consumes the explicit exact D-amplitude witnesses from
r22_epsminus_d_amplitude.py.  For every requested (scalar component, chirality)
branch it constructs the complete corrected 32-block E system, including vacuum
output 1, solves the homogeneous characteristic-zero linear equations, checks
that every required 2x2 E-block has a nonzero determinant polynomial on the
nullspace, chooses one exact simultaneous-invertible point, and substitutes it
back into every E-layer pentagon.
"""
from __future__ import annotations

import argparse
import random
from collections import Counter
from itertools import product

import sympy as sp

import r22_epsminus_d_amplitude as da
import r22_epsminus_d_trace as tr
from r22_scale_audit import ONE, OBJECTS, f_blocks, f_class, layer_spec, pentagon_blocks
from r22_local_associator import pentagon


E_KEYS = sorted(
    (a, b, c, d)
    for a, b, c, d, dim in f_blocks()
    if ONE not in (a, b, c) and dim == 2 and f_class((a, b, c, d)) == "E"
)
assert len(E_KEYS) == 32
E_INDEX = {k: i for i, k in enumerate(E_KEYS)}
EVARS = sp.symbols("e0:128")


def evar(key, row, col):
    return EVARS[4 * E_INDEX[key] + 2 * row + col]


def build_e_cases():
    out = []
    for p in pentagon_blocks():
        if ONE in p[:4] or not layer_spec("E", p):
            continue
        registry, _mats, diff = pentagon(dict(zip("abcd", p[:4])), p[4])
        out.append((p, registry, diff))
    return out


E_CASES = build_e_cases()


def exact_d_data(cid: int, mask: int):
    ratios, _source, shapes, seeds, _ = da.collect_ratio_constraints(cid, mask)
    exponents, _profile = da.solve_root_amplitudes(ratios, require_mu4=True)
    root_group = "mu4"
    if exponents is None:
        exponents, _profile = da.solve_root_amplitudes(ratios, require_mu4=False)
        root_group = "mu8"
    if exponents is None:
        raise RuntimeError(("D-amplitude witness missing", cid, mask))
    checked, failures = da.verify_characteristic_zero(cid, mask, exponents, shapes, seeds)
    if failures:
        raise RuntimeError(("D replay failed before E", cid, mask, failures))

    ddata = dict(seeds)
    for key, T in shapes.items():
        ddata[key] = da.amplitude_value(exponents[tr.T_INDEX[key]]) * T
    return tr.scalar_assignment(cid), ddata, root_group


def registry_sub_e(registry, scalar, ddata, edata=None):
    sub = {}
    for (meta, sym) in registry.symbols.items():
        key, row, col = meta
        cl = f_class(key)
        if cl in "ABC":
            sub[sym] = scalar[key]
        elif cl == "D":
            sub[sym] = ddata[key][row, col]
        elif cl == "E":
            if edata is None:
                sub[sym] = evar(key, row, col)
            else:
                sub[sym] = edata[key][row, col]
        else:
            raise RuntimeError(("unexpected E-layer dependency", key, cl))
    return sub


def build_linear_system(scalar, ddata):
    equations = []
    total_entries = 0
    support = Counter()
    for _p, registry, diff in E_CASES:
        sub = registry_sub_e(registry, scalar, ddata)
        value = diff.applyfunc(lambda e: sp.expand(e.xreplace(sub)))
        total_entries += value.rows * value.cols
        for e in value:
            if e == 0:
                continue
            poly = sp.Poly(e, *EVARS)
            support[len(poly.terms())] += 1
            equations.append(e)
    A, b = sp.linear_eq_to_matrix(equations, EVARS)
    if b != sp.zeros(len(equations), 1):
        raise RuntimeError("E system unexpectedly inhomogeneous")
    return A, support, total_entries, len(equations)


def nullspace_block_matrix(ns, key, params):
    M = sp.zeros(2)
    base = 4 * E_INDEX[key]
    for k, v in enumerate(ns):
        for r in range(2):
            for c in range(2):
                M[r, c] += params[k] * v[base + 2 * r + c]
    return M.applyfunc(sp.cancel)


def determinant_polynomials(ns):
    params = sp.symbols(f"p0:{len(ns)}")
    dets = {}
    for key in E_KEYS:
        M = nullspace_block_matrix(ns, key, params)
        det = sp.factor(sp.expand(M.det()))
        dets[key] = det
    return params, dets


def choose_invertible_point(ns, params, dets, seed):
    if any(d == 0 for d in dets.values()):
        return None
    candidates = []
    candidates.append([sp.Integer(1)] * len(ns))
    for k in range(min(len(ns), 8)):
        x = [sp.Integer(1)] * len(ns)
        x[k] = sp.Integer(2)
        candidates.append(x)
    rng = random.Random(seed)
    for _ in range(512):
        candidates.append([sp.Integer(rng.choice([-3, -2, -1, 1, 2, 3])) for _ in ns])

    for vals in candidates:
        sub = dict(zip(params, vals))
        if all(sp.simplify(d.xreplace(sub)) != 0 for d in dets.values()):
            vec = sp.zeros(128, 1)
            for a, v in zip(vals, ns):
                vec += a * v
            return [sp.cancel(x) for x in vec]
    return None


def vector_to_edata(vec):
    out = {}
    for key in E_KEYS:
        i = 4 * E_INDEX[key]
        out[key] = sp.Matrix([[vec[i], vec[i + 1]], [vec[i + 2], vec[i + 3]]])
    return out


def verify_e(scalar, ddata, edata):
    checked = 0
    failures = []
    for p, registry, diff in E_CASES:
        sub = registry_sub_e(registry, scalar, ddata, edata)
        value = diff.applyfunc(lambda e: sp.simplify(e.xreplace(sub)))
        checked += value.rows * value.cols
        for i in range(value.rows):
            for j in range(value.cols):
                if value[i, j] != 0:
                    failures.append((p[:5], (i, j), value[i, j]))
                    if len(failures) >= 5:
                        return checked, failures
    return checked, failures


def solve_branch(cid: int, mask: int):
    scalar, ddata, d_root_group = exact_d_data(cid, mask)
    A, support, total_entries, n_eq = build_linear_system(scalar, ddata)
    ns = A.nullspace()
    rank = A.cols - len(ns)
    if not ns:
        result = {
            "component": cid, "mask": mask, "D": d_root_group,
            "E_rank": rank, "E_nullity": 0, "equations": n_eq,
            "support": dict(support), "status": "E_ZERO_ONLY",
        }
        print(result, flush=True)
        return result, None

    params, dets = determinant_polynomials(ns)
    zero_dets = [k for k, d in dets.items() if d == 0]
    if zero_dets:
        result = {
            "component": cid, "mask": mask, "D": d_root_group,
            "E_rank": rank, "E_nullity": len(ns), "equations": n_eq,
            "support": dict(support), "zero_determinant_blocks": zero_dets,
            "status": "E_SINGULAR",
        }
        print(result, flush=True)
        return result, None

    vec = choose_invertible_point(ns, params, dets, seed=cid * 1000 + mask)
    if vec is None:
        raise RuntimeError(("could not find explicit E point although determinants are nonzero polynomials", cid, mask, len(ns)))
    edata = vector_to_edata(vec)
    bad_blocks = [k for k, M in edata.items() if sp.simplify(M.det()) == 0]
    if bad_blocks:
        raise RuntimeError(("chosen E point singular", cid, mask, bad_blocks))
    checked, failures = verify_e(scalar, ddata, edata)
    if failures:
        raise RuntimeError(("E characteristic-zero replay failed", cid, mask, failures))

    result = {
        "component": cid, "mask": mask, "D": d_root_group,
        "E_rank": rank, "E_nullity": len(ns), "equations": n_eq,
        "support": dict(support), "all_32_det_polynomials_nonzero": True,
        "verified_matrix_entries": checked, "status": "E_PASS",
    }
    print(result, flush=True)
    return result, (scalar, ddata, edata)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, action="append")
    ap.add_argument("--mask", type=int, action="append")
    args = ap.parse_args()
    components = tuple(args.component) if args.component else da.FRONTIER_COMPONENTS
    masks = tuple(args.mask) if args.mask else da.SURVIVOR_MASKS

    counts = Counter()
    for cid in components:
        for mask in masks:
            result, _data = solve_branch(cid, mask)
            counts[result["status"]] += 1
    print("E status counts", dict(counts), flush=True)


if __name__ == "__main__":
    main()
