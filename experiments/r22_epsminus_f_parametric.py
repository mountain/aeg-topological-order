"""Phase-4 parametric F-linear filter over the exact two-parameter E torus.

Phase 3 proves that every deep epsilon=-1 branch has a two-dimensional exact E
solution space.  The 32 required E determinants are monomials: sixteen are a
nonzero constant times p^2 and sixteen a nonzero constant times q^2.  Thus the
E-invertible locus is p*q != 0.  The two parameters are NOT assumed to be gauge.

This script keeps them symbolic.  The F-linear pentagons have support one/two
in the 1312 F entries.  Their coefficients are checked to be Laurent monomials
in p,q with Gaussian-rational constants.  Weighted graph cycles then tell us
when an F weighted component may be nonzero.  Since coefficient ratios have
E-degree zero, every nontrivial cycle condition is

    unit * (p/q)^k = 1.

Hence E-ratio space splits into one generic stratum plus finitely many
root-of-unity strata.  For every stratum, each 8x8/10x10 F determinant is
computed exactly as a polynomial in the remaining independent F-component
parameters.  Finite ratio strata are evaluated in a cyclotomic ring, not by
floating point.

A branch passes Phase 4 iff at least one E-ratio stratum has all sixteen
required determinant polynomials nonzero.  Otherwise F coherence forces a
singular required associator for every invertible E solution.
"""
from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from functools import reduce

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
_nf = 0
for key, dim in F_BLOCKS:
    F_OFFSET[key] = _nf
    _nf += dim * dim
assert _nf == 1312
FVARS = sp.symbols("f0:1312")
FVAR_SET = set(FVARS)
FVAR_INDEX = {x: i for i, x in enumerate(FVARS)}


def fvar(key, row, col):
    dim = F_DIMS[key]
    return FVARS[F_OFFSET[key] + dim * row + col]


def build_f_cases():
    out = []
    for p in pentagon_blocks():
        if ONE in p[:4] or not layer_spec("F", p):
            continue
        registry, _mats, diff = pentagon(dict(zip("abcd", p[:4])), p[4])
        out.append((p, registry, diff))
    return out


F_CASES = build_f_cases()


def gaussian_pair(x):
    x = sp.expand(sp.cancel(x))
    a, b = x.as_real_imag()
    a = sp.cancel(a); b = sp.cancel(b)
    if a.free_symbols or b.free_symbols or not (a.is_Rational and b.is_Rational):
        raise RuntimeError(("not Gaussian rational", x, a, b))
    return Fraction(int(a.p), int(a.q)), Fraction(int(b.p), int(b.q))


def gadd(x, y):
    return x[0] + y[0], x[1] + y[1]


def gneg(x):
    return -x[0], -x[1]


def gmul(x, y):
    return x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def ginv(x):
    n = x[0] * x[0] + x[1] * x[1]
    if n == 0:
        raise ZeroDivisionError(x)
    return x[0] / n, -x[1] / n


def gdiv(x, y):
    return gmul(x, ginv(y))


def giszero(x):
    return x[0] == 0 and x[1] == 0


def gone():
    return Fraction(1), Fraction(0)


def gminusone():
    return Fraction(-1), Fraction(0)


def gphase(x):
    table = {
        (Fraction(1), Fraction(0)): 0,
        (Fraction(0), Fraction(1)): 1,
        (Fraction(-1), Fraction(0)): 2,
        (Fraction(0), Fraction(-1)): 3,
    }
    if x not in table:
        raise RuntimeError(("cycle constant is not a fourth-root unit", x))
    return table[x]


@dataclass(frozen=True)
class LM:
    c: tuple[Fraction, Fraction]
    ep: int = 0
    eq: int = 0

    def mul(self, other: "LM") -> "LM":
        return LM(gmul(self.c, other.c), self.ep + other.ep, self.eq + other.eq)

    def div(self, other: "LM") -> "LM":
        return LM(gdiv(self.c, other.c), self.ep - other.ep, self.eq - other.eq)

    def neg(self) -> "LM":
        return LM(gneg(self.c), self.ep, self.eq)

    def inv(self) -> "LM":
        return LM(ginv(self.c), -self.ep, -self.eq)


LM_ONE = LM(gone(), 0, 0)


def parse_laurent(expr, params):
    expr = sp.cancel(expr)
    num, den = sp.fraction(expr)

    def mono(x):
        poly = sp.Poly(sp.expand(x), *params)
        terms = poly.terms()
        if len(terms) != 1:
            return None
        powers, coeff = terms[0]
        return tuple(int(a) for a in powers), gaussian_pair(coeff)

    n = mono(num); d = mono(den)
    if n is None or d is None:
        raise RuntimeError(("non-monomial F coefficient over E torus", expr))
    npow, nc = n; dpow, dc = d
    if len(params) != 2:
        raise RuntimeError(("expected two E parameters", params))
    return LM(gdiv(nc, dc), npow[0] - dpow[0], npow[1] - dpow[1])


def parametric_lower_data(cid, mask):
    scalar, ddata, d_root_group = ef.exact_d_data(cid, mask)
    euf, esupport, _total, eneq, _prov = ef.build_weighted_system(scalar, ddata)
    roots, params, emats, dets = ef.parametric_blocks(euf)
    if len(roots) != 2:
        raise RuntimeError(("E nullity is not two", cid, mask, roots))
    det_profile = Counter()
    for key, det in dets.items():
        if det == 0:
            raise RuntimeError(("E determinant zero", cid, mask, key))
        poly = sp.Poly(sp.factor(det), *params)
        terms = poly.terms()
        if len(terms) != 1:
            raise RuntimeError(("E determinant nonmonomial", cid, mask, key, det))
        powers, coeff = terms[0]
        if coeff == 0:
            raise RuntimeError(("E determinant zero coefficient", cid, mask, key))
        det_profile[tuple(int(x) for x in powers)] += 1
    if det_profile != Counter({(2, 0): 16, (0, 2): 16}):
        raise RuntimeError(("unexpected E determinant torus profile", cid, mask, det_profile))
    return scalar, ddata, params, emats, d_root_group


def registry_sub_f(registry, scalar, ddata, emats):
    sub = {}
    for (meta, sym) in registry.symbols.items():
        key, row, col = meta
        cl = f_class(key)
        if cl in "ABC":
            sub[sym] = scalar[key]
        elif cl == "D":
            sub[sym] = ddata[key][row, col]
        elif cl == "E":
            sub[sym] = emats[key][row, col]
        elif cl == "F":
            sub[sym] = fvar(key, row, col)
        else:
            raise RuntimeError(("unexpected F dependency", key, cl))
    return sub


def linear_row(expr, params):
    coeffs = defaultdict(lambda: sp.Integer(0))
    const = sp.Integer(0)
    for term in sp.Add.make_args(sp.expand(expr)):
        fs = term.free_symbols & FVAR_SET
        if not fs:
            const += term
            continue
        if len(fs) != 1:
            raise RuntimeError(("nonlinear F term", term, fs))
        sym = next(iter(fs))
        coeffs[FVAR_INDEX[sym]] += term / sym
    const = sp.cancel(const)
    if const != 0:
        raise RuntimeError(("inhomogeneous F-linear equation", const, expr))
    out = {}
    for i, c in coeffs.items():
        c = sp.cancel(c)
        if c != 0:
            out[i] = parse_laurent(c, params)
    return out


class LaurentUF:
    """Weighted union-find with cycle conditions retained instead of forced generically."""
    def __init__(self, n):
        self.parent = list(range(n))
        self.weight = [LM_ONE for _ in range(n)]  # x_i = weight_i * x_root
        self.forced = [False] * n
        self.conditions = [[] for _ in range(n)]

    def find(self, x):
        if self.parent[x] == x:
            return x, self.weight[x]
        p = self.parent[x]
        r, wp = self.find(p)
        self.weight[x] = self.weight[x].mul(wp)
        self.parent[x] = r
        return r, self.weight[x]

    def force(self, x):
        r, _ = self.find(x)
        self.forced[r] = True

    def relation(self, i, a: LM, j, b: LM, provenance):
        ri, wi = self.find(i); rj, wj = self.find(j)
        if ri == rj:
            # a*wi + b*wj = 0  <=>  (-a*wi)/(b*wj) = 1.
            cond = a.mul(wi).neg().div(b.mul(wj))
            self.conditions[ri].append((cond, provenance))
            return
        q = a.mul(wi).neg().div(b.mul(wj))
        fi, fj = self.forced[ri], self.forced[rj]
        ci, cj = self.conditions[ri], self.conditions[rj]
        self.parent[rj] = ri
        self.weight[rj] = q
        self.forced[ri] = fi or fj
        self.conditions[ri] = ci + cj

    def canonicalize(self):
        for i in range(len(self.parent)):
            self.find(i)
        forced = defaultdict(bool)
        conds = defaultdict(list)
        for i in range(len(self.parent)):
            r, _ = self.find(i)
            forced[r] = forced[r] or self.forced[i]
        # Conditions were moved only at union roots; collect from every stored slot.
        for i, cs in enumerate(self.conditions):
            if not cs:
                continue
            r, _ = self.find(i)
            conds[r].extend(cs)
        for r in set(self.find(i)[0] for i in range(len(self.parent))):
            self.forced[r] = forced[r]
            self.conditions[r] = conds[r]


def build_f_system(scalar, ddata, params, emats):
    uf = LaurentUF(1312)
    support = Counter()
    coefficient_degrees = Counter()
    n_eq = 0
    for p, registry, diff in F_CASES:
        sub = registry_sub_f(registry, scalar, ddata, emats)
        value = diff.applyfunc(lambda e: e.xreplace(sub))
        for i in range(value.rows):
            for j in range(value.cols):
                e = value[i, j]
                if e == 0:
                    continue
                row = linear_row(e, params)
                if not row:
                    continue
                support[len(row)] += 1; n_eq += 1
                for lm in row.values():
                    coefficient_degrees[(lm.ep, lm.eq)] += 1
                prov = (p[:5], (i, j))
                if len(row) == 1:
                    (x, _a), = row.items(); uf.force(x)
                elif len(row) == 2:
                    (x, a), (y, b) = list(row.items()); uf.relation(x, a, y, b, prov)
                else:
                    raise RuntimeError(("F equation support > 2", prov, len(row)))
    uf.canonicalize()
    return uf, support, coefficient_degrees, n_eq


def normalized_condition(lm: LM):
    # Every F coefficient has one E factor, so relation weights and cycle
    # conditions must have total E degree zero.
    if lm.ep + lm.eq != 0:
        raise RuntimeError(("cycle condition depends on overall E scale", lm))
    k = lm.ep
    phase = gphase(lm.c)
    # condition i^phase * r^k = 1
    return k, phase


def root_condition_profile(uf):
    roots = sorted({uf.find(i)[0] for i in range(1312)})
    profile = {}
    k_values = []
    for r in roots:
        if uf.forced[r]:
            profile[r] = {"forced": True, "conditions": []}
            continue
        conds = []
        impossible = False
        for lm, prov in uf.conditions[r]:
            k, phase = normalized_condition(lm)
            if k == 0:
                if phase % 4:
                    impossible = True
                    conds.append((k, phase, prov))
                continue
            conds.append((k, phase, prov)); k_values.append(abs(k))
        profile[r] = {"forced": impossible, "conditions": conds}
    return profile, k_values


def lcm(values):
    ans = 1
    for v in values:
        ans = ans * v // math.gcd(ans, v)
    return ans


def candidate_modulus(k_values):
    return lcm([4] + [4 * k for k in k_values if k])


def active_roots(profile, u=None, L=None):
    active = []
    for r, info in profile.items():
        if info["forced"]:
            continue
        conds = info["conditions"]
        if u is None:
            # Generic ratio: only components with no nontrivial condition survive.
            if not conds:
                active.append(r)
            continue
        ok = True
        for k, phase, _prov in conds:
            if (k * u + phase * (L // 4)) % L != 0:
                ok = False; break
        if ok:
            active.append(r)
    return active


def entry_descriptor(uf, profile, index, active_set):
    r, w = uf.find(index)
    if r not in active_set:
        return None
    if w.ep + w.eq != 0:
        raise RuntimeError(("entry relation depends on overall E scale", index, w))
    return r, w.c, w.ep


def block_descriptor(uf, profile, key, active_set):
    dim = F_DIMS[key]; base = F_OFFSET[key]
    return [[entry_descriptor(uf, profile, base + dim * i + j, active_set) for j in range(dim)] for i in range(dim)]


def determinant_generic(mat):
    """Polynomial in independent F roots and Laurent r; exact Gaussian coefficients."""
    n = len(mat)
    dp = {0: {((), 0): gone()}}
    for i in range(n):
        nd = {}
        for mask, poly in dp.items():
            for j in range(n):
                if (mask >> j) & 1 or mat[i][j] is None:
                    continue
                root, gc, rk = mat[i][j]
                sign = -1 if ((mask >> (j + 1)).bit_count() & 1) else 1
                if sign < 0: gc = gneg(gc)
                q = nd.setdefault(mask | (1 << j), {})
                for (mon, rexp), c in poly.items():
                    mm = tuple(sorted(mon + (root,)))
                    key = (mm, rexp + rk)
                    v = gadd(q.get(key, (Fraction(0), Fraction(0))), gmul(c, gc))
                    if giszero(v): q.pop(key, None)
                    else: q[key] = v
        dp = {m: p for m, p in nd.items() if p}
        if not dp: return {}
    return dp.get((1 << n) - 1, {})


def cyclotomic_coeff_nonzero(terms, u, L):
    """terms: {r_exponent: Gaussian coefficient}; evaluate r=s^u, i=s^(L/4)."""
    s = sp.Symbol("s")
    expr = sp.Integer(0)
    for k, (a, b) in terms.items():
        ek = (u * k) % L
        if a:
            expr += sp.Rational(a.numerator, a.denominator) * s ** ek
        if b:
            expr += sp.Rational(b.numerator, b.denominator) * s ** ((ek + L // 4) % L)
    if expr == 0:
        return False
    phi = sp.Poly(sp.cyclotomic_poly(L, s), s, domain=sp.QQ)
    rem = sp.rem(sp.Poly(expr, s, domain=sp.QQ), phi)
    return not rem.is_zero


def determinant_finite_nonzero(mat, u, L):
    poly = determinant_generic(mat)
    if not poly:
        return False
    by_mon = defaultdict(dict)
    for (mon, rexp), c in poly.items():
        by_mon[mon][rexp] = gadd(by_mon[mon].get(rexp, (Fraction(0), Fraction(0))), c)
    return any(cyclotomic_coeff_nonzero(terms, u, L) for terms in by_mon.values())


def determinant_generic_nonzero(mat):
    return bool(determinant_generic(mat))


def analyze_branch(cid, mask):
    scalar, ddata, params, emats, droot = parametric_lower_data(cid, mask)
    uf, support, coefficient_degrees, n_eq = build_f_system(scalar, ddata, params, emats)
    profile, k_values = root_condition_profile(uf)
    roots = sorted(profile)
    generic_active = set(active_roots(profile))
    L = candidate_modulus(k_values)
    if L > 128:
        raise RuntimeError(("unexpectedly large E-ratio root-of-unity modulus", cid, mask, L, sorted(set(k_values))))

    strata = []
    # Generic E ratio.
    generic_bad = []
    for key, _dim in F_BLOCKS:
        if not determinant_generic_nonzero(block_descriptor(uf, profile, key, generic_active)):
            generic_bad.append(key)
    strata.append({"type": "generic", "active_F_components": len(generic_active), "bad_blocks": generic_bad})

    # Finite exceptional root-of-unity ratios.  Deduplicate identical u modulo L
    # only after determinant testing because coefficient phases depend on u.
    passing = []
    finite_summaries = Counter()
    for u in range(L):
        active = set(active_roots(profile, u=u, L=L))
        bad = []
        for key, _dim in F_BLOCKS:
            if not determinant_finite_nonzero(block_descriptor(uf, profile, key, active), u, L):
                bad.append(key)
        finite_summaries[(len(active), len(bad))] += 1
        if not bad:
            passing.append(u)

    if not generic_bad:
        passing_desc = ["generic"] + [f"zeta_{L}^{u}" for u in passing]
    else:
        passing_desc = [f"zeta_{L}^{u}" for u in passing]

    condition_counts = Counter()
    for info in profile.values():
        if info["forced"]: condition_counts["forced"] += 1
        elif info["conditions"]: condition_counts["conditional"] += 1
        else: condition_counts["free"] += 1

    out = {
        "component": cid,
        "mask": mask,
        "D_root_group": droot,
        "F_equations": n_eq,
        "F_support": dict(support),
        "F_coefficient_E_degrees": {str(k): v for k, v in coefficient_degrees.items()},
        "F_component_condition_profile": dict(condition_counts),
        "E_ratio_modulus": L,
        "generic_active_F_components": len(generic_active),
        "generic_bad_blocks": generic_bad,
        "finite_strata_profile": {str(k): v for k, v in finite_summaries.items()},
        "passing_E_ratio_strata": passing_desc,
        "status": "F_PASS" if passing_desc else "F_SINGULAR_FOR_ALL_E",
    }
    print(out, flush=True)
    return out


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
            result = analyze_branch(cid, mask)
            counts[result["status"]] += 1
    print("PARAMETRIC F status counts", dict(counts), flush=True)


if __name__ == "__main__":
    main()
