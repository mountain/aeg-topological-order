"""Phase-5 kernel compiler for fresh epsilon=-1 R(2,2) branches.

This does not solve the final system.  It keeps the exact two-parameter E torus,
quotients the complete F-linear weighted relations, substitutes the resulting
F-component parameters into every pentagon with four noninvertible external
inputs, and reports the exact polynomial kernel size/degree/term structure with
pentagon-entry provenance.

The first development gate is component 5 / chirality mask 0.  Later branches
must use the same compiler rather than branch-specific algebra.
"""
from __future__ import annotations

import argparse
from collections import Counter

import sympy as sp

import r22_epsminus_f_parametric as fp
from r22_scale_audit import M, f_class, pentagon_blocks
from r22_local_associator import pentagon


def gsym(c):
    a, b = c
    return sp.Rational(a.numerator, a.denominator) + sp.I * sp.Rational(b.numerator, b.denominator)


def lm_expr(lm, params):
    p, q = params
    return sp.cancel(gsym(lm.c) * p ** lm.ep * q ** lm.eq)


def final_cases():
    out = []
    for p in pentagon_blocks():
        if not all(x in M for x in p[:4]):
            continue
        registry, _mats, diff = pentagon(dict(zip("abcd", p[:4])), p[4])
        out.append((p, registry, diff))
    return out


FINAL_CASES = final_cases()


def parametric_f_data(cid, mask):
    scalar, ddata, params, emats, droot = fp.parametric_lower_data(cid, mask)
    uf, support, _degrees, n_eq = fp.build_f_system(scalar, ddata, params, emats)
    profile, _kvals = fp.root_condition_profile(uf)
    active = sorted(fp.active_roots(profile))
    if any(info["conditions"] for info in profile.values() if not info["forced"]):
        raise RuntimeError(("generic F stratum has conditional components", cid, mask))
    z = sp.symbols(f"z0:{len(active)}")
    zmap = {r: z[i] for i, r in enumerate(active)}
    active_set = set(active)
    fdata = {}
    for key, dim in fp.F_BLOCKS:
        base = fp.F_OFFSET[key]
        mat = sp.zeros(dim)
        for i in range(dim):
            for j in range(dim):
                r, w = uf.find(base + dim * i + j)
                if r in active_set and not profile[r]["forced"]:
                    mat[i, j] = sp.cancel(lm_expr(w, params) * zmap[r])
        fdata[key] = mat
    return scalar, ddata, params, emats, z, fdata, droot, support, n_eq


def registry_sub(registry, scalar, ddata, emats, fdata):
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
            sub[sym] = fdata[key][row, col]
        else:
            raise RuntimeError(("unexpected final-kernel dependency", key, cl))
    return sub


def canonical_poly(expr, variables, eparams):
    expr = sp.cancel(expr)
    num, den = sp.fraction(expr)
    if den.free_symbols - set(eparams):
        raise RuntimeError(("final denominator depends on F parameters", den))
    num = sp.expand(num)
    if num == 0:
        return None
    poly = sp.Poly(num, *variables, extension=sp.I)
    terms = poly.terms()

    # p,q are nonzero on the E-invertible torus, so remove only their common
    # monomial factor.  Do not divide by F-component variables.
    mins = [min(mon[k] for mon, _c in terms) for k in range(2)]
    if mins[0] or mins[1]:
        p, q = eparams
        num = sp.expand(num / (p ** mins[0] * q ** mins[1]))
        poly = sp.Poly(num, *variables, extension=sp.I)
        terms = poly.terms()

    lead = terms[0][1]
    norm = []
    for mon, c in terms:
        cc = sp.cancel(c / lead)
        norm.append((tuple(int(x) for x in mon), cc))
    return tuple(norm)


def poly_stats(key):
    degrees = [sum(mon) for mon, _c in key]
    fdegrees = [sum(mon[2:]) for mon, _c in key]
    return len(key), max(degrees), max(fdegrees)


def compile_branch(cid, mask):
    scalar, ddata, params, emats, z, fdata, droot, fsupport, fneq = parametric_f_data(cid, mask)
    variables = tuple(params) + tuple(z)
    unique = {}
    raw_nonzero = 0
    scalar_positions = 0
    denominator_profile = Counter()

    for p, registry, diff in FINAL_CASES:
        sub = registry_sub(registry, scalar, ddata, emats, fdata)
        value = diff.applyfunc(lambda e: sp.cancel(e.xreplace(sub)))
        scalar_positions += value.rows * value.cols
        for i in range(value.rows):
            for j in range(value.cols):
                e = value[i, j]
                if e == 0:
                    continue
                raw_nonzero += 1
                _num, den = sp.fraction(e)
                denominator_profile[str(sp.factor(den))] += 1
                key = canonical_poly(e, variables, params)
                if key is None:
                    continue
                unique.setdefault(key, (p[:5], (i, j)))

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
    for key, prov in sorted(unique.items(), key=lambda kv: (len(kv[0]), poly_stats(kv[0])[1], str(kv[1])))[:12]:
        examples.append({"terms": len(key), "degree": poly_stats(key)[1], "F_degree": poly_stats(key)[2], "provenance": prov, "poly": str(key)})

    out = {
        "component": cid,
        "mask": mask,
        "D_root_group": droot,
        "final_pentagon_blocks": len(FINAL_CASES),
        "final_scalar_positions": scalar_positions,
        "E_parameters": len(params),
        "F_linear_components": len(z),
        "kernel_variables": len(variables),
        "F_linear_equations_before_kernel": fneq,
        "F_linear_support": dict(fsupport),
        "raw_nonzero_final_entries": raw_nonzero,
        "unique_kernel_polynomials": len(unique),
        "term_count_profile": dict(term_profile),
        "total_degree_profile": dict(degree_profile),
        "F_degree_profile": dict(fdegree_profile),
        "constant_contradictions": len(constant_contradictions),
        "denominator_types": len(denominator_profile),
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
    print("RESULT: Phase-5 exact kernel compiled; no nonlinear solving attempted", flush=True)
    if result["constant_contradictions"]:
        print("WARNING: kernel already contains a nonzero constant equation", flush=True)


if __name__ == "__main__":
    main()
