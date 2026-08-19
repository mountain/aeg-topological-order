"""Exact residual-kernel scan for one finite component-13/mask-0 stratum.

This is deliberately a *single-branch* gate.  It starts from the already
verified finite relations and affine closure, substitutes the full exact RREF
into all 219 Phase-5 kernel relations, and reports the resulting low-dimensional
residual polynomial system.

No global solve or Groebner basis is attempted.  The goal is only to expose the
shortest equations and variable-incidence structure for local certificates.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict

import r22_phase5_component13_mask0_finite_census as fc
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss


def pzero(n):
    return {}


def pconst(c, n):
    return {} if ss.kiszero(c) else {(0,) * n: c}


def pvar(j, n):
    m = [0] * n
    m[j] = 1
    return {tuple(m): ss.K1}


def padd(a, b):
    out = dict(a)
    for m, c in b.items():
        v = ss.kadd(out.get(m, ss.K0), c)
        if ss.kiszero(v):
            out.pop(m, None)
        else:
            out[m] = v
    return out


def pscale(a, c):
    if ss.kiszero(c):
        return {}
    return {m: ss.kmul(v, c) for m, v in a.items() if not ss.kiszero(ss.kmul(v, c))}


def pmul(a, b):
    if not a or not b:
        return {}
    out = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(x + y for x, y in zip(ma, mb))
            c = ss.kmul(ca, cb)
            v = ss.kadd(out.get(m, ss.K0), c)
            if ss.kiszero(v):
                out.pop(m, None)
            else:
                out[m] = v
    return out


def ppow(a, e, n):
    out = pconst(ss.K1, n)
    base = a
    while e:
        if e & 1:
            out = pmul(out, base)
        base = pmul(base, base)
        e >>= 1
    return out


def canonical(poly):
    if not poly:
        return ()
    lead = min(poly)
    inv = ss.kinv(poly[lead])
    rows = []
    for mon in sorted(poly):
        c = ss.kmul(poly[mon], inv)
        if not ss.kiszero(c):
            rows.append((mon, c))
    return tuple(rows)


def poly_degree(poly):
    return max((sum(m) for m in poly), default=0)


def poly_support(poly):
    return tuple(sorted({j for m in poly for j, e in enumerate(m) if e}))


def poly_string(poly, names):
    if not poly:
        return "0"
    parts = []
    for mon in sorted(poly):
        c = poly[mon]
        factors = []
        for j, e in enumerate(mon):
            if e == 1:
                factors.append(names[j])
            elif e:
                factors.append(f"{names[j]}^{e}")
        term = "*".join(factors) if factors else "1"
        parts.append(f"({ss.kstr(c)})*{term}")
    return " + ".join(parts)


def build_branch(unique, a, b, sign):
    p, q, t = fc.branch_values(a, b, sign)
    normalized = []
    affine = []
    for key, prov in unique.items():
        poly = fc.strip_nonzero_laurent(fc.specialize_key(key, p, q, t))
        if not poly:
            continue
        normalized.append((poly, prov))
        row = fc.affine_row(poly)
        if row is not None:
            affine.append(row)

    rr, pivots, consistent = fc.rref(affine)
    if not consistent:
        raise AssertionError((a, b, sign, "representative is affine-inconsistent"))
    free = tuple(j for j in range(fc.NVARS) if j not in pivots)
    free_names = tuple(f"z{fc.KEEP_Z[j]}" for j in free)
    nf = len(free)
    free_pos = {j: k for k, j in enumerate(free)}

    subst = {}
    for j in free:
        subst[j] = pvar(free_pos[j], nf)
    for i, j in enumerate(pivots):
        expr = pconst(rr[i][fc.NVARS], nf)
        for k in free:
            if ss.kiszero(rr[i][k]):
                continue
            expr = padd(expr, pscale(subst[k], ss.kneg(rr[i][k])))
        subst[j] = expr

    residual = {}
    provenance = defaultdict(list)
    raw_nonzero = 0
    for poly, prov in normalized:
        out = {}
        for mon, coeff in poly.items():
            term = pconst(coeff, nf)
            for j, e in enumerate(mon):
                if e:
                    term = pmul(term, ppow(subst[j], e, nf))
                    if not term:
                        break
            out = padd(out, term)
        if not out:
            continue
        raw_nonzero += 1
        key = canonical(out)
        residual.setdefault(key, out)
        provenance[key].append(prov)

    return {
        "a": a,
        "b": b,
        "sign": sign,
        "affine_rows": len(affine),
        "pivots": tuple(fc.KEEP_Z[j] for j in pivots),
        "free": tuple(fc.KEEP_Z[j] for j in free),
        "free_names": free_names,
        "normalized": len(normalized),
        "raw_residual_nonzero": raw_nonzero,
        "residual": residual,
        "provenance": provenance,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, choices=(0,1,2), required=True)
    ap.add_argument("--b", type=int, choices=(0,1,2), required=True)
    ap.add_argument("--sign", choices=("+", "-"), required=True)
    args = ap.parse_args()
    sign = 1 if args.sign == "+" else -1

    _quotient, unique = ml.compile_unique(fc.CID, fc.MASK)
    data = build_branch(unique, args.a, args.b, sign)
    residual = data["residual"]
    names = data["free_names"]

    term_profile = Counter(len(poly) for poly in residual.values())
    degree_profile = Counter(poly_degree(poly) for poly in residual.values())
    varcount_profile = Counter(len(poly_support(poly)) for poly in residual.values())
    constant = []
    univariate = []
    by_support = Counter()
    for key, poly in residual.items():
        supp = poly_support(poly)
        by_support[supp] += 1
        if not supp:
            constant.append((key, poly))
        if len(supp) == 1:
            univariate.append((key, poly))

    shortest = sorted(
        residual.items(),
        key=lambda kv: (len(kv[1]), len(poly_support(kv[1])), poly_degree(kv[1]), str(kv[0])),
    )[:30]
    rows = []
    for key, poly in shortest:
        rows.append({
            "terms": len(poly),
            "degree": poly_degree(poly),
            "support": tuple(names[j] for j in poly_support(poly)),
            "poly": poly_string(poly, names),
            "provenance": tuple(data["provenance"][key][:4]),
        })

    summary = {
        "component": fc.CID,
        "mask": fc.MASK,
        "branch": (args.a, args.b, args.sign),
        "affine_rows": data["affine_rows"],
        "pivots": data["pivots"],
        "free": data["free"],
        "free_names": names,
        "normalized_kernel_polynomials": data["normalized"],
        "raw_residual_nonzero": data["raw_residual_nonzero"],
        "unique_residual_polynomials": len(residual),
        "term_profile": dict(term_profile),
        "degree_profile": dict(degree_profile),
        "variable_count_profile": dict(varcount_profile),
        "constant_contradictions": len(constant),
        "univariate_equations": len(univariate),
        "support_profile_top": [
            (tuple(names[j] for j in s), n)
            for s, n in sorted(by_support.items(), key=lambda kv: (len(kv[0]), -kv[1], kv[0]))[:20]
        ],
        "shortest": rows,
    }
    print(summary, flush=True)
    if constant:
        print("RESULT: representative residual has an exact constant contradiction", flush=True)
    else:
        print("RESULT: representative residual compiled; inspect shortest local relation core", flush=True)


if __name__ == "__main__":
    main()
