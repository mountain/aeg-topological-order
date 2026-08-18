"""Phase-3 E-layer filter for fresh epsilon=-1 R(2,2) survivors.

Consumes explicit exact D-amplitude witnesses from r22_epsminus_d_amplitude.py.
The complete corrected 32-block E system is homogeneous and, after lower-layer
substitution, consists of support-one/support-two linear equations.  We solve it
as an exact weighted-component graph rather than materializing a dense
1280-by-128 SymPy matrix.

For every branch the script:
  * constructs all E-layer pentagons, including vacuum output 1;
  * contracts exact weighted entry identifications;
  * determines the E nullity from free weighted components;
  * proves whether every required 2x2 E determinant is a nonzero polynomial on
    that nullspace;
  * chooses an explicit simultaneous-invertible exact point when possible;
  * substitutes the point back into every original E-layer pentagon.
"""
from __future__ import annotations

import argparse
import random
from collections import Counter, defaultdict

import sympy as sp

import r22_epsminus_d_amplitude as da
import r22_epsminus_d_trace as tr
from r22_scale_audit import ONE, f_blocks, f_class, layer_spec, pentagon_blocks
from r22_local_associator import pentagon


E_KEYS = sorted(
    (a, b, c, d)
    for a, b, c, d, dim in f_blocks()
    if ONE not in (a, b, c) and dim == 2 and f_class((a, b, c, d)) == "E"
)
assert len(E_KEYS) == 32
E_INDEX = {k: i for i, k in enumerate(E_KEYS)}
EVARS = sp.symbols("e0:128")
EVAR_SET = set(EVARS)
EVAR_INDEX = {x: i for i, x in enumerate(EVARS)}


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
            sub[sym] = evar(key, row, col) if edata is None else edata[key][row, col]
        else:
            raise RuntimeError(("unexpected E-layer dependency", key, cl))
    return sub


def linear_row(expr):
    coeffs = defaultdict(lambda: sp.Integer(0))
    const = sp.Integer(0)
    for term in sp.Add.make_args(sp.expand(expr)):
        fs = term.free_symbols & EVAR_SET
        if not fs:
            const += term
            continue
        if len(fs) != 1:
            raise RuntimeError(("nonlinear E term", term, fs))
        sym = next(iter(fs))
        c = sp.cancel(term / sym)
        if c.free_symbols:
            raise RuntimeError(("unexpected symbolic E coefficient", c, c.free_symbols))
        coeffs[EVAR_INDEX[sym]] += c
    const = sp.cancel(const)
    coeffs = {i: sp.cancel(c) for i, c in coeffs.items() if sp.cancel(c) != 0}
    return const, coeffs


class WeightedUF:
    """Exact homogeneous linear solver for support-1/support-2 equations.

    find(i) returns (root, w) with x_i = w * x_root.
    A forced root denotes x_root = 0.
    """
    def __init__(self, n):
        self.parent = list(range(n))
        self.weight = [sp.Integer(1) for _ in range(n)]
        self.forced = [False] * n

    def find(self, x):
        if self.parent[x] == x:
            return x, self.weight[x]
        p = self.parent[x]
        r, wp = self.find(p)
        self.weight[x] = sp.cancel(self.weight[x] * wp)
        self.parent[x] = r
        return r, self.weight[x]

    def force(self, x):
        r, _ = self.find(x)
        self.forced[r] = True

    def relation(self, i, a, j, b):
        ri, wi = self.find(i)
        rj, wj = self.find(j)
        if ri == rj:
            if sp.cancel(a * wi + b * wj) != 0:
                self.forced[ri] = True
            return
        # a*wi*R_i + b*wj*R_j = 0 => R_j = q R_i.
        q = sp.cancel(-(a * wi) / (b * wj))
        fi, fj = self.forced[ri], self.forced[rj]
        self.parent[rj] = ri
        self.weight[rj] = q
        self.forced[ri] = fi or fj

    def canonicalize(self):
        for i in range(len(self.parent)):
            self.find(i)
        # A forced child may have been merged after its flag was set; fold flags.
        flags = defaultdict(bool)
        for i in range(len(self.parent)):
            r, _ = self.find(i)
            flags[r] = flags[r] or self.forced[i]
        for r, f in flags.items():
            self.forced[r] = f

    def free_roots(self):
        self.canonicalize()
        roots = sorted({self.find(i)[0] for i in range(len(self.parent))})
        return [r for r in roots if not self.forced[r]]


def build_weighted_system(scalar, ddata):
    uf = WeightedUF(128)
    support = Counter()
    total_entries = 0
    n_eq = 0
    provenance = {}
    for p, registry, diff in E_CASES:
        sub = registry_sub_e(registry, scalar, ddata)
        value = diff.applyfunc(lambda e: e.xreplace(sub))
        total_entries += value.rows * value.cols
        for i in range(value.rows):
            for j in range(value.cols):
                e = value[i, j]
                if e == 0:
                    continue
                const, row = linear_row(e)
                if const != 0:
                    raise RuntimeError(("inhomogeneous E equation", p[:5], (i, j), const, row))
                if not row:
                    continue
                support[len(row)] += 1
                n_eq += 1
                provenance.setdefault(len(row), (p[:5], (i, j), row))
                if len(row) == 1:
                    (x, _a), = row.items()
                    uf.force(x)
                elif len(row) == 2:
                    (x, a), (y, b) = list(row.items())
                    uf.relation(x, a, y, b)
                else:
                    raise RuntimeError(("E equation support > 2", p[:5], (i, j), len(row), row))
    uf.canonicalize()
    return uf, support, total_entries, n_eq, provenance


def parametric_blocks(uf):
    roots = uf.free_roots()
    ridx = {r: i for i, r in enumerate(roots)}
    params = sp.symbols(f"p0:{len(roots)}")
    mats = {}
    dets = {}
    for key in E_KEYS:
        vals = []
        base = 4 * E_INDEX[key]
        for q in range(4):
            r, w = uf.find(base + q)
            vals.append(sp.Integer(0) if uf.forced[r] else sp.cancel(w * params[ridx[r]]))
        M = sp.Matrix([[vals[0], vals[1]], [vals[2], vals[3]]])
        mats[key] = M
        dets[key] = sp.factor(sp.expand(M.det()))
    return roots, params, mats, dets


def choose_root_values(roots, params, dets, seed):
    if any(d == 0 for d in dets.values()):
        return None
    candidates = [[sp.Integer(1)] * len(roots)]
    for k in range(min(len(roots), 8)):
        x = [sp.Integer(1)] * len(roots)
        x[k] = sp.Integer(2)
        candidates.append(x)
    rng = random.Random(seed)
    for _ in range(256):
        candidates.append([sp.Integer(rng.choice([-3, -2, -1, 1, 2, 3])) for _ in roots])
    for vals in candidates:
        sub = dict(zip(params, vals))
        if all(sp.cancel(d.xreplace(sub)) != 0 for d in dets.values()):
            return vals
    return None


def root_values_to_edata(uf, roots, root_values):
    ridx = {r: i for i, r in enumerate(roots)}
    out = {}
    for key in E_KEYS:
        vals = []
        base = 4 * E_INDEX[key]
        for q in range(4):
            r, w = uf.find(base + q)
            vals.append(sp.Integer(0) if uf.forced[r] else sp.cancel(w * root_values[ridx[r]]))
        out[key] = sp.Matrix([[vals[0], vals[1]], [vals[2], vals[3]]])
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
    uf, support, total_entries, n_eq, provenance = build_weighted_system(scalar, ddata)
    roots, params, _mats, dets = parametric_blocks(uf)
    nullity = len(roots)
    rank = 128 - nullity

    if nullity == 0:
        result = {
            "component": cid, "mask": mask, "D": d_root_group,
            "E_rank": 128, "E_nullity": 0, "equations": n_eq,
            "support": dict(support), "status": "E_ZERO_ONLY",
        }
        print(result, flush=True)
        return result, None

    zero_dets = [k for k, d in dets.items() if d == 0]
    if zero_dets:
        result = {
            "component": cid, "mask": mask, "D": d_root_group,
            "E_rank": rank, "E_nullity": nullity, "equations": n_eq,
            "support": dict(support), "zero_determinant_blocks": zero_dets,
            "status": "E_SINGULAR",
        }
        print(result, flush=True)
        return result, None

    root_values = choose_root_values(roots, params, dets, seed=cid * 1000 + mask)
    if root_values is None:
        raise RuntimeError(("could not find explicit E point", cid, mask, nullity))
    edata = root_values_to_edata(uf, roots, root_values)
    bad_blocks = [k for k, M in edata.items() if sp.cancel(M.det()) == 0]
    if bad_blocks:
        raise RuntimeError(("chosen E point singular", cid, mask, bad_blocks))
    checked, failures = verify_e(scalar, ddata, edata)
    if failures:
        raise RuntimeError(("E characteristic-zero replay failed", cid, mask, failures))

    result = {
        "component": cid, "mask": mask, "D": d_root_group,
        "E_rank": rank, "E_nullity": nullity, "equations": n_eq,
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
