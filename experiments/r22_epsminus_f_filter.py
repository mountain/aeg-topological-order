"""Phase-4 F-linear weighted-component filter for fresh epsilon=-1 R(2,2).

Only branches that pass the complete E-layer filter are processed.  Lower A--E
data are frozen at one explicit exact simultaneous-invertible E point.  The
three-noninvertible / noninvertible-output pentagons are then linear in the 1312
entries of the sixteen large F blocks.

The linear system is solved as an exact support-1/support-2 weighted graph.
Each required 8x8 or 10x10 determinant is computed as a characteristic-zero
polynomial in the remaining weighted-component parameters by subset DP.  A
branch is rejected only if some required determinant polynomial is identically
zero.  If all are nonzero, the script also finds one explicit simultaneous-
invertible exact F point and replays every F-linear pentagon.
"""
from __future__ import annotations

import argparse
import random
from collections import Counter, defaultdict

import sympy as sp

import r22_epsminus_d_amplitude as da
import r22_epsminus_e_filter as ef
from r22_scale_audit import ONE, f_blocks, f_class, layer_spec, pentagon_blocks
from r22_local_associator import pentagon


F_BLOCKS = sorted(
    ((a, b, c, d), dim)
    for a, b, c, d, dim in f_blocks()
    if ONE not in (a, b, c) and f_class((a, b, c, d)) == "F"
)
assert len(F_BLOCKS) == 16
F_DIMS = {k: d for k, d in F_BLOCKS}
F_OFFSET = {}
_n = 0
for k, d in F_BLOCKS:
    F_OFFSET[k] = _n
    _n += d * d
assert _n == 1312
FVARS = sp.symbols("f0:1312")
FVAR_SET = set(FVARS)
FVAR_INDEX = {x: i for i, x in enumerate(FVARS)}


def fvar(key, row, col):
    d = F_DIMS[key]
    return FVARS[F_OFFSET[key] + d * row + col]


def build_f_cases():
    out = []
    for p in pentagon_blocks():
        if ONE in p[:4] or not layer_spec("F", p):
            continue
        registry, _mats, diff = pentagon(dict(zip("abcd", p[:4])), p[4])
        out.append((p, registry, diff))
    return out


F_CASES = build_f_cases()


def registry_sub_f(registry, scalar, ddata, edata, fdata=None):
    sub = {}
    for (meta, sym) in registry.symbols.items():
        key, row, col = meta
        cl = f_class(key)
        if cl in "ABC":
            sub[sym] = scalar[key]
        elif cl == "D":
            sub[sym] = ddata[key][row, col]
        elif cl == "E":
            sub[sym] = edata[key][row, col]
        elif cl == "F":
            sub[sym] = fvar(key, row, col) if fdata is None else fdata[key][row, col]
        else:
            raise RuntimeError(("unexpected F-layer dependency", key, cl))
    return sub


def linear_row(expr):
    coeffs = defaultdict(lambda: sp.Integer(0))
    const = sp.Integer(0)
    for term in sp.Add.make_args(sp.expand(expr)):
        fs = term.free_symbols & FVAR_SET
        if not fs:
            const += term
            continue
        if len(fs) != 1:
            raise RuntimeError(("nonlinear F-linear term", term, fs))
        sym = next(iter(fs))
        c = sp.cancel(term / sym)
        if c.free_symbols:
            raise RuntimeError(("unexpected symbolic F coefficient", c, c.free_symbols))
        coeffs[FVAR_INDEX[sym]] += c
    const = sp.cancel(const)
    coeffs = {i: sp.cancel(c) for i, c in coeffs.items() if sp.cancel(c) != 0}
    return const, coeffs


class WeightedUF:
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
        q = sp.cancel(-(a * wi) / (b * wj))
        fi, fj = self.forced[ri], self.forced[rj]
        self.parent[rj] = ri
        self.weight[rj] = q
        self.forced[ri] = fi or fj

    def canonicalize(self):
        for i in range(len(self.parent)):
            self.find(i)
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


def build_weighted_system(scalar, ddata, edata):
    uf = WeightedUF(1312)
    support = Counter()
    n_eq = 0
    total_entries = 0
    provenance = {}
    for p, registry, diff in F_CASES:
        sub = registry_sub_f(registry, scalar, ddata, edata)
        value = diff.applyfunc(lambda e: e.xreplace(sub))
        total_entries += value.rows * value.cols
        for i in range(value.rows):
            for j in range(value.cols):
                e = value[i, j]
                if e == 0:
                    continue
                const, row = linear_row(e)
                if const != 0:
                    raise RuntimeError(("inhomogeneous F-linear equation", p[:5], (i, j), const, row))
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
                    raise RuntimeError(("F-linear support > 2", p[:5], (i, j), len(row), row))
    uf.canonicalize()
    return uf, support, total_entries, n_eq, provenance


def entry_descriptor(uf, index, ridx):
    r, w = uf.find(index)
    if uf.forced[r]:
        return None
    return ridx[r], sp.cancel(w)


def block_descriptors(uf, key, ridx):
    d = F_DIMS[key]
    base = F_OFFSET[key]
    return [[entry_descriptor(uf, base + d * i + j, ridx) for j in range(d)] for i in range(d)]


def determinant_polynomial(mat):
    """Exact determinant polynomial: monomial tuple -> SymPy coefficient."""
    n = len(mat)
    dp = {0: {(): sp.Integer(1)}}
    for i in range(n):
        nd = {}
        for mask, poly in dp.items():
            for j in range(n):
                if (mask >> j) & 1 or mat[i][j] is None:
                    continue
                root, w = mat[i][j]
                sign = -1 if ((mask >> (j + 1)).bit_count() & 1) else 1
                q = nd.setdefault(mask | (1 << j), {})
                fac = sp.cancel(sign * w)
                for mon, c in poly.items():
                    mm = tuple(sorted(mon + (root,)))
                    v = sp.cancel(q.get(mm, sp.Integer(0)) + fac * c)
                    if v != 0:
                        q[mm] = v
                    else:
                        q.pop(mm, None)
        dp = {m: p for m, p in nd.items() if p}
        if not dp:
            return {}
    return dp.get((1 << n) - 1, {})


def evaluate_poly(poly, values):
    ans = sp.Integer(0)
    for mon, c in poly.items():
        v = c
        for r in mon:
            v *= values[r]
        ans += v
    return sp.cancel(ans)


def choose_root_values(roots, dets, seed):
    candidates = [{r: sp.Integer(1) for r in roots}]
    rng = random.Random(seed)
    for _ in range(512):
        candidates.append({r: sp.Integer(rng.choice([-3, -2, -1, 1, 2, 3])) for r in roots})
    for vals in candidates:
        if all(evaluate_poly(poly, vals) != 0 for poly in dets.values()):
            return vals
    return None


def roots_to_fdata(uf, roots, values):
    out = {}
    for key, d in F_BLOCKS:
        base = F_OFFSET[key]
        M = sp.zeros(d)
        for i in range(d):
            for j in range(d):
                r, w = uf.find(base + d * i + j)
                M[i, j] = 0 if uf.forced[r] else sp.cancel(w * values[r])
        out[key] = M
    return out


def verify_f(scalar, ddata, edata, fdata):
    checked = 0
    failures = []
    for p, registry, diff in F_CASES:
        sub = registry_sub_f(registry, scalar, ddata, edata, fdata)
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
    eresult, edata_pack = ef.solve_branch(cid, mask)
    if edata_pack is None:
        result = {"component": cid, "mask": mask, "status": "SKIP_" + eresult["status"]}
        print(result, flush=True)
        return result, None
    scalar, ddata, edata = edata_pack

    uf, support, total_entries, n_eq, provenance = build_weighted_system(scalar, ddata, edata)
    roots = uf.free_roots()
    ridx = {r: k for k, r in enumerate(roots)}
    forced_roots = sorted({uf.find(i)[0] for i in range(1312) if uf.forced[uf.find(i)[0]]})

    dets = {}
    zero_blocks = []
    for key, _d in F_BLOCKS:
        poly = determinant_polynomial(block_descriptors(uf, key, ridx))
        dets[key] = poly
        if not poly:
            zero_blocks.append(key)

    if zero_blocks:
        result = {
            "component": cid, "mask": mask,
            "F_free_components": len(roots), "F_forced_zero_components": len(forced_roots),
            "equations": n_eq, "support": dict(support),
            "zero_determinant_blocks": zero_blocks,
            "status": "F_SINGULAR",
        }
        print(result, flush=True)
        return result, None

    values = choose_root_values(roots, dets, seed=cid * 1000 + mask)
    if values is None:
        raise RuntimeError(("no explicit simultaneous F-invertible point found", cid, mask, len(roots)))
    fdata = roots_to_fdata(uf, roots, values)
    bad = [key for key, M in fdata.items() if sp.simplify(M.det()) == 0]
    if bad:
        raise RuntimeError(("chosen F point singular", cid, mask, bad))
    checked, failures = verify_f(scalar, ddata, edata, fdata)
    if failures:
        raise RuntimeError(("F-linear characteristic-zero replay failed", cid, mask, failures))

    result = {
        "component": cid, "mask": mask,
        "F_free_components": len(roots), "F_forced_zero_components": len(forced_roots),
        "equations": n_eq, "support": dict(support),
        "all_16_det_polynomials_nonzero": True,
        "verified_matrix_entries": checked,
        "status": "F_PASS",
    }
    print(result, flush=True)
    return result, (scalar, ddata, edata, uf, roots, fdata)


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
    print("F status counts", dict(counts), flush=True)


if __name__ == "__main__":
    main()
