"""Sparse Phase-5 kernel compiler for fresh epsilon=-1 R(2,2) branches.

This compiler works directly in the Phase-4 quotient.  It keeps the exact
E-torus parameters p,q, represents every lower associator entry as a Gaussian-
rational Laurent monomial, represents every active F entry as that monomial
times one independent F-component parameter z_j, and contracts the final
four-noninvertible pentagons without first materializing generic SymPy F-symbol
matrices.

The output is only a structural audit of the exact nonlinear kernel: variable
count, raw nonzero equations, unique normalized Laurent polynomials, degree and
term profiles, and pentagon-entry provenance.  It deliberately performs no
Groebner computation and no nonlinear solving.
"""
from __future__ import annotations

import argparse
import time
from collections import Counter
from fractions import Fraction

import sympy as sp

import r22_epsminus_f_parametric as fp
from r22_local_associator import (
    P0,
    P1,
    P2,
    P4,
    enum_states,
    leafsets_state,
    root_label,
    rotate_right,
    subtree_at,
)
from r22_scale_audit import M, N, OBJECTS, ONE, f_class, pentagon_blocks


GZERO = (Fraction(0), Fraction(0))
GONE = (Fraction(1), Fraction(0))


def monomial(coeff, exponents):
    if fp.giszero(coeff):
        return {}
    return {tuple(int(x) for x in exponents): coeff}


def poly_add_scaled(dst, src, scale=GONE):
    for m, c in src.items():
        v = fp.gadd(dst.get(m, GZERO), fp.gmul(scale, c))
        if fp.giszero(v):
            dst.pop(m, None)
        else:
            dst[m] = v
    return dst


def poly_mul(a, b):
    if not a or not b:
        return {}
    out = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(x + y for x, y in zip(ma, mb))
            v = fp.gadd(out.get(m, GZERO), fp.gmul(ca, cb))
            if fp.giszero(v):
                out.pop(m, None)
            else:
                out[m] = v
    return out


def matmul(a, b):
    """Sparse exact matrix product; matrices are row -> {column: polynomial}."""
    out = [dict() for _ in range(len(a))]
    for i, row in enumerate(a):
        for k, aik in row.items():
            if k >= len(b):
                raise RuntimeError(("matrix shape mismatch", i, k, len(b)))
            for j, bkj in b[k].items():
                prod = poly_mul(aik, bkj)
                if not prod:
                    continue
                cell = out[i].setdefault(j, {})
                poly_add_scaled(cell, prod)
                if not cell:
                    out[i].pop(j, None)
    return out


def final_blocks():
    return [p for p in pentagon_blocks() if all(x in M for x in p[:4])]


FINAL_BLOCKS = final_blocks()


def sympy_laurent_monomial(expr, params, nvars):
    """Convert an exact lower-layer SymPy monomial into sparse Laurent form."""
    expr = sp.cancel(expr)
    if expr == 0:
        return {}
    num, den = sp.fraction(expr)

    def one_term(x):
        poly = sp.Poly(sp.expand(x), *params)
        terms = poly.terms()
        if len(terms) != 1:
            raise RuntimeError(("expected Laurent monomial", expr, x, terms[:4]))
        powers, coeff = terms[0]
        return tuple(int(a) for a in powers), fp.gaussian_pair(coeff)

    npow, nc = one_term(num)
    dpow, dc = one_term(den)
    exponents = [0] * nvars
    exponents[0] = npow[0] - dpow[0]
    exponents[1] = npow[1] - dpow[1]
    return monomial(fp.gdiv(nc, dc), exponents)


def parametric_quotient_data(cid, mask):
    t0 = time.perf_counter()
    scalar, ddata, params, emats, droot = fp.parametric_lower_data(cid, mask)
    uf, support, _degrees, n_eq = fp.build_f_system(scalar, ddata, params, emats)
    profile, _kvals = fp.root_condition_profile(uf)
    active = sorted(fp.active_roots(profile))
    if any(info["conditions"] for info in profile.values() if not info["forced"]):
        raise RuntimeError(("generic F stratum has conditional components", cid, mask))

    nvars = 2 + len(active)
    root_index = {r: i for i, r in enumerate(active)}
    active_set = set(active)
    fdata = {}
    for key, dim in fp.F_BLOCKS:
        base = fp.F_OFFSET[key]
        for i in range(dim):
            for j in range(dim):
                r, w = uf.find(base + dim * i + j)
                if r not in active_set or profile[r]["forced"]:
                    fdata[(key, i, j)] = {}
                    continue
                exponents = [0] * nvars
                exponents[0] = int(w.ep)
                exponents[1] = int(w.eq)
                exponents[2 + root_index[r]] = 1
                fdata[(key, i, j)] = monomial(w.c, exponents)

    lower_cache = {}

    def lower_entry(key, row, col):
        ck = (key, row, col)
        if ck in lower_cache:
            return lower_cache[ck]
        cl = f_class(key)
        if cl in "ABC":
            value = sympy_laurent_monomial(scalar[key], params, nvars)
        elif cl == "D":
            value = sympy_laurent_monomial(ddata[key][row, col], params, nvars)
        elif cl == "E":
            value = sympy_laurent_monomial(emats[key][row, col], params, nvars)
        elif cl == "F":
            value = fdata[ck]
        else:
            raise RuntimeError(("unexpected final-kernel dependency", key, cl))
        lower_cache[ck] = value
        return value

    return {
        "params": params,
        "variables": ("p", "q") + tuple(f"z{i}" for i in range(len(active))),
        "nvars": nvars,
        "droot": droot,
        "F_support": support,
        "F_equations": n_eq,
        "F_components": len(active),
        "lower_entry": lower_entry,
        "lower_seconds": time.perf_counter() - t0,
    }


_BASIS_INDEX_CACHE = {}


def basis_indices(key):
    if key in _BASIS_INDEX_CACHE:
        return _BASIS_INDEX_CACHE[key]
    a, b, c, d = key
    src = []
    for e in OBJECTS:
        for alpha in range(N(a, b, e)):
            for beta in range(N(e, c, d)):
                src.append((e, alpha, beta))
    tgt = []
    for f in OBJECTS:
        for mu in range(N(b, c, f)):
            for nu in range(N(a, f, d)):
                tgt.append((f, mu, nu))
    if len(src) != len(tgt):
        raise RuntimeError(("associator basis mismatch", key, len(src), len(tgt)))
    ans = ({x: i for i, x in enumerate(src)}, {x: i for i, x in enumerate(tgt)})
    _BASIS_INDEX_CACHE[key] = ans
    return ans


def one_poly(nvars):
    return monomial(GONE, (0,) * nvars)


def associator_entry(a, b, c, d, e, alpha, beta, f, mu, nu, quotient):
    nvars = quotient["nvars"]
    if a == ONE:
        ok = e == b and alpha == 0 and f == d and nu == 0 and mu == beta
        return one_poly(nvars) if ok else {}
    if b == ONE:
        ok = e == a and alpha == 0 and f == c and mu == 0 and nu == beta
        return one_poly(nvars) if ok else {}
    if c == ONE:
        ok = e == d and beta == 0 and f == b and mu == 0 and nu == alpha
        return one_poly(nvars) if ok else {}

    key = (a, b, c, d)
    src_index, tgt_index = basis_indices(key)
    try:
        col = src_index[(e, alpha, beta)]
        row = tgt_index[(f, mu, nu)]
    except KeyError as exc:
        raise RuntimeError(("associator basis lookup failed", key, exc.args[0])) from exc
    return quotient["lower_entry"](key, row, col)


def leaves(node):
    if isinstance(node, str):
        return frozenset([node])
    return leaves(node[0]) | leaves(node[1])


def reassoc_sparse(source, path, total, leaf_labels, quotient):
    target = rotate_right(source, path)

    def sortkey(st):
        return tuple(sorted(st.items()))

    sb = sorted(enum_states(source, leaf_labels, total), key=sortkey)
    tb = sorted(enum_states(target, leaf_labels, total), key=sortkey)
    rows = [dict() for _ in tb]

    pa = path + ("L", "L")
    pb = path + ("L", "R")
    pc = path + ("R",)
    pold = path + ("L",)
    pout = path
    pnew = path + ("R",)
    local_leafset = leaves(subtree_at(source, path))

    target_sets = [leafsets_state(target, ts) for ts in tb]
    for j, ss in enumerate(sb):
        a = root_label(source, ss, leaf_labels, pa)
        b = root_label(source, ss, leaf_labels, pb)
        c = root_label(source, ss, leaf_labels, pc)
        e, alpha = ss[pold]
        d, beta = ss[pout]
        ssets = leafsets_state(source, ss)

        for i, ts in enumerate(tb):
            tsets = target_sets[i]
            common = ssets.keys() & tsets.keys()
            if any(ssets[x] != tsets[x] for x in common if x != local_leafset):
                continue
            f, mu = ts[pnew]
            dd, nu = ts[pout]
            if dd != d:
                continue
            value = associator_entry(a, b, c, d, e, alpha, beta, f, mu, nu, quotient)
            if value:
                rows[i][j] = value

    return target, rows


def pentagon_sparse(labels, total, quotient):
    _, m01 = reassoc_sparse(P0, ("L",), total, labels, quotient)
    _, m12 = reassoc_sparse(P1, (), total, labels, quotient)
    _, m23 = reassoc_sparse(P2, ("R",), total, labels, quotient)
    _, m04 = reassoc_sparse(P0, (), total, labels, quotient)
    _, m43 = reassoc_sparse(P4, (), total, labels, quotient)
    long_side = matmul(matmul(m23, m12), m01)
    short_side = matmul(m43, m04)
    return long_side, short_side


def gaussian_key(c):
    return (
        (c[0].numerator, c[0].denominator),
        (c[1].numerator, c[1].denominator),
    )


def canonical_poly(poly):
    if not poly:
        return None, None
    mins = [min(mon[k] for mon in poly) for k in range(2)]
    shifted = {}
    for mon, c in poly.items():
        mm = list(mon)
        mm[0] -= mins[0]
        mm[1] -= mins[1]
        shifted[tuple(mm)] = c

    mons = sorted(shifted, reverse=True)
    lead = shifted[mons[0]]
    key = tuple((m, gaussian_key(fp.gdiv(shifted[m], lead))) for m in mons)
    return key, tuple(mins)


def poly_stats(key):
    degrees = [sum(mon) for mon, _c in key]
    fdegrees = [sum(mon[2:]) for mon, _c in key]
    return len(key), max(degrees), max(fdegrees)


def compile_branch(cid, mask):
    t0 = time.perf_counter()
    quotient = parametric_quotient_data(cid, mask)
    unique = {}
    raw_nonzero = 0
    scalar_positions = 0
    laurent_floor_profile = Counter()
    block_dim_profile = Counter()

    for bi, p in enumerate(FINAL_BLOCKS, 1):
        labels = dict(zip("abcd", p[:4]))
        long_side, short_side = pentagon_sparse(labels, p[4], quotient)
        dim = len(long_side)
        scalar_positions += dim * dim
        block_dim_profile[dim] += 1

        for i in range(dim):
            cols = set(long_side[i]) | set(short_side[i])
            for j in cols:
                diff = dict(long_side[i].get(j, {}))
                poly_add_scaled(diff, short_side[i].get(j, {}), (Fraction(-1), Fraction(0)))
                if not diff:
                    continue
                raw_nonzero += 1
                key, floor = canonical_poly(diff)
                if key is None:
                    continue
                laurent_floor_profile[floor] += 1
                unique.setdefault(key, (p[:5], (i, j)))

        if bi % 8 == 0 or bi == len(FINAL_BLOCKS):
            print(
                "progress",
                bi,
                "/",
                len(FINAL_BLOCKS),
                "raw",
                raw_nonzero,
                "unique",
                len(unique),
                flush=True,
            )

    term_profile = Counter()
    degree_profile = Counter()
    fdegree_profile = Counter()
    constant_contradictions = []
    for key, prov in unique.items():
        nt, deg, fdeg = poly_stats(key)
        term_profile[nt] += 1
        degree_profile[deg] += 1
        fdegree_profile[fdeg] += 1
        if deg == 0:
            constant_contradictions.append((key, prov))

    examples = []
    order = sorted(unique.items(), key=lambda kv: (len(kv[0]), poly_stats(kv[0])[1], str(kv[1])))
    for key, prov in order[:12]:
        nt, deg, fdeg = poly_stats(key)
        examples.append(
            {
                "terms": nt,
                "degree": deg,
                "F_degree": fdeg,
                "provenance": prov,
                "poly": str(key),
            }
        )

    out = {
        "component": cid,
        "mask": mask,
        "compiler": "sparse-gaussian-laurent",
        "D_root_group": quotient["droot"],
        "final_pentagon_blocks": len(FINAL_BLOCKS),
        "final_block_dimension_profile": dict(block_dim_profile),
        "final_scalar_positions": scalar_positions,
        "E_parameters": 2,
        "F_linear_components": quotient["F_components"],
        "kernel_variables": len(quotient["variables"]),
        "kernel_variable_names": quotient["variables"],
        "F_linear_equations_before_kernel": quotient["F_equations"],
        "F_linear_support": dict(quotient["F_support"]),
        "raw_nonzero_final_entries": raw_nonzero,
        "unique_kernel_polynomials": len(unique),
        "term_count_profile": dict(term_profile),
        "total_degree_profile": dict(degree_profile),
        "F_degree_profile": dict(fdegree_profile),
        "max_total_degree": max(degree_profile, default=0),
        "max_F_degree": max(fdegree_profile, default=0),
        "constant_contradictions": len(constant_contradictions),
        "laurent_floor_profile": {str(k): v for k, v in laurent_floor_profile.items()},
        "lower_quotient_seconds": round(quotient["lower_seconds"], 3),
        "total_seconds": round(time.perf_counter() - t0, 3),
        "examples": examples,
    }
    print(out, flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    args = ap.parse_args()
    result = compile_branch(args.component, args.mask)
    print("RESULT: Phase-5 exact sparse kernel compiled; no nonlinear solving attempted", flush=True)
    if result["constant_contradictions"]:
        print("WARNING: kernel already contains a nonzero torus-localized constant equation", flush=True)


if __name__ == "__main__":
    main()
