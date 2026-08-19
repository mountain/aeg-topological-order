"""Exact sparse sign-specialized residual for component 5 / D class 1.

This is the D-class-1 counterpart of ``r22_phase5_rankdrop_second.py``.  It
reuses the exact sparse coefficient field

    K = Q(i, sqrt(2), sqrt(3))

and sparse Laurent arithmetic from ``r22_phase5_survivor_sparse.py``, but all
branch values, product phases and five-relation reductions come from the fresh
class-1 source table in ``r22_phase5_component5_torsion_finite_audit.py``.

For a rank-10 off-diagonal branch we impose only the already-derived local
consequences

    z19 = -z20,
    z20^2 = -1/8,

split the two exact signs z20 = +/- i*sqrt(2)/4, and project the complete 219
source equations to the remaining six Laurent variables

    z1,z2,z4,z5,z11,z12,

with only z1,z2 invertible.  The probe reports constant contradictions,
proved-nonzero scale monomials, singleton/univariate constraints and the
shortest residual relations.  No Groebner basis or global nonlinear solve is
used.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction

import r22_phase5_component5_rest_audit as fa
import r22_phase5_component5_torsion_finite_audit as tf
import r22_phase5_monomial_lift as ml
import r22_phase5_rankdrop_second as second
import r22_phase5_survivor_sparse as s
import r22_phase5_torsion_sheet as ts


def omega_k():
    # omega = -1/2 + (i/2)*sqrt(3)
    return (
        (((Fraction(-1, 2), Fraction(0)), s.G0)),
        (((Fraction(0), Fraction(1, 2)), s.G0)),
    )


def z0_value(root_name: str):
    # z0 = -1 +/- sqrt(6)/2.
    s6half = (s.Q20, (s.G0, (Fraction(1, 2), Fraction(0))))
    return s.kadd(s.kr(-1), s6half if root_name == "positive" else s.kneg(s6half))


def complex_k(a: Fraction, b: Fraction):
    return s.kg((a, b))


def base_values(mask: int):
    rel = tf.relation(mask)
    # Avoid SymPy conversion: source-validated P0/Q0 are always (1 +/- i)/2.
    table = {
        0: (complex_k(Fraction(1, 2), Fraction(1, 2)), complex_k(Fraction(1, 2), Fraction(-1, 2))),
        105: (complex_k(Fraction(1, 2), Fraction(-1, 2)), complex_k(Fraction(1, 2), Fraction(-1, 2))),
        150: (complex_k(Fraction(1, 2), Fraction(1, 2)), complex_k(Fraction(1, 2), Fraction(1, 2))),
        255: (complex_k(Fraction(1, 2), Fraction(-1, 2)), complex_k(Fraction(1, 2), Fraction(1, 2))),
    }
    if mask not in table:
        raise ValueError(mask)
    # Cross-check cube constants in exact K.
    p0, q0 = table[mask]
    if s.kstr(s.kpow(p0, 3)) != s.kstr(s.kg(rel["P3"])):
        raise AssertionError((mask, "P0 cube mismatch", s.kstr(s.kpow(p0, 3)), rel["P3"]))
    if s.kstr(s.kpow(q0, 3)) != s.kstr(s.kg(rel["Q3"])):
        raise AssertionError((mask, "Q0 cube mismatch", s.kstr(s.kpow(q0, 3)), rel["Q3"]))
    return p0, q0


def branch_values(mask: int, a: int, b: int, root_name: str):
    p0, q0 = base_values(mask)
    w = omega_k()
    return s.kmul(p0, s.kpow(w, a)), s.kmul(q0, s.kpow(w, b)), z0_value(root_name)


def phase_k(gphase):
    return s.kg(gphase)


def build_zmaps_class1(rr, pivots, p, q, t, rel):
    free = tuple(j for j in range(20) if j not in pivots)
    final_free = tuple(j for j in free if j not in (2, 7))
    pos = {j: k for k, j in enumerate(final_free)}
    n = len(final_free)

    def var(j):
        m = [0] * n
        m[pos[j]] = 1
        return {tuple(m): s.K1}

    maps = {j: var(j) for j in final_free}

    # Source-validated class-1 products:
    # z3 = Z23 * p^2 * z0 / z2
    # z8 = Z18 * q^2 * z0 / z1
    c3 = s.kmul(phase_k(rel["Z23"]), s.kmul(s.kpow(p, 2), t))
    c8 = s.kmul(phase_k(rel["Z18"]), s.kmul(s.kpow(q, 2), t))
    m3 = [0] * n
    m3[pos[1]] = -1
    m8 = [0] * n
    m8[pos[0]] = -1
    maps[2] = {tuple(m3): c3}
    maps[7] = {tuple(m8): c8}

    for row_i, j in enumerate(pivots):
        expr = s.lp_const(rr[row_i][20], n)
        for k in free:
            if s.kiszero(rr[row_i][k]):
                continue
            s.lp_add_scaled(expr, maps[k], s.kneg(rr[row_i][k]))
        maps[j] = expr

    if len(maps) != 20:
        raise RuntimeError(("incomplete z map", sorted(set(range(20)) - set(maps))))
    return maps, final_free


def analyze(cid: int, mask: int, a: int, b: int, root_name: str, sign: int):
    if (a, b) not in ((2, 1), (1, 2)):
        raise ValueError(("off-diagonal cube pair required", a, b))
    rel = tf.relation(mask)
    p, q, t = branch_values(mask, a, b, root_name)

    old_rel = fa.REL.get(mask)
    fa.REL[mask] = rel
    try:
        with ts.second_sheet_provider():
            _quotient, unique = ml.compile_unique(cid, mask)
    finally:
        if old_rel is None:
            fa.REL.pop(mask, None)
        else:
            fa.REL[mask] = old_rel

    reduced = {key: fa.reduce_poly(key, rel) for key in unique}
    specialized = {key: s.specialize(poly, p, q, t) for key, poly in reduced.items()}

    rows = []
    profile = Counter()
    for key, prov in unique.items():
        zpoly = s.strip_common_nonzero(specialized[key])
        ar = s.affine_row(zpoly)
        if ar is None:
            continue
        if all(s.kiszero(x) for x in ar[:20]):
            if not s.kiszero(ar[20]):
                raise RuntimeError(("localized affine contradiction", prov))
            continue
        profile[sum(1 for x in ar[:20] if not s.kiszero(x))] += 1
        rows.append(ar)

    rr, pivots = s.rref(rows)
    if len(pivots) != 10:
        raise RuntimeError(("expected rank 10", mask, a, b, root_name, len(pivots)))
    zmaps, old_free = build_zmaps_class1(rr, pivots, p, q, t, rel)
    expected = (0, 1, 3, 4, 10, 11, 18, 19)
    if old_free != expected:
        raise RuntimeError(("unexpected old free variables", old_free))

    r = second.z20_value(sign)
    if not s.kiszero(s.kadd(s.kmul(r, r), s.kr(Fraction(1, 8)))):
        raise RuntimeError(("bad z20 root", sign, s.kstr(r)))

    projected = {}
    new_free = None
    for j, poly in zmaps.items():
        pp, nf = second.project_lp(poly, old_free, r)
        if new_free is None:
            new_free = nf
        elif new_free != nf:
            raise RuntimeError("projection mismatch")
        projected[j] = pp
    if new_free != (0, 1, 3, 4, 10, 11):
        raise RuntimeError(("unexpected final variables", new_free))

    residual = {}
    vanished = 0
    for key, prov in unique.items():
        lp = s.evaluate(specialized[key], projected, len(new_free))
        ck = s.canonical(lp, new_free)
        if ck is None:
            vanished += 1
        else:
            residual.setdefault(ck, prov)

    term_profile = Counter()
    degree_profile = Counter()
    var_profile = Counter()
    contradictions = []
    scale_monomials = []
    singleton = []
    univariate = []
    pos = {j: k for k, j in enumerate(new_free)}
    scale_pos = {pos[0], pos[1]}

    for key, prov in residual.items():
        nt = len(key)
        deg = max(sum(mon) for mon, _ in key)
        supp = s.support(key)
        term_profile[nt] += 1
        degree_profile[deg] += 1
        var_profile[len(supp)] += 1
        if not supp:
            contradictions.append((key, prov))
        if nt == 1:
            mon, _c = key[0]
            if all(e == 0 or j in scale_pos for j, e in enumerate(mon)):
                scale_monomials.append((key, prov))
            else:
                singleton.append((key, prov))
        if len(supp) == 1:
            univariate.append((key, prov, next(iter(supp))))

    order = sorted(
        residual.items(),
        key=lambda kv: (
            len(s.support(kv[0])),
            len(kv[0]),
            max(sum(m) for m, _ in kv[0]),
            str(kv[1]),
        ),
    )
    examples = []
    for key, prov in order[:50]:
        examples.append({
            "variables": [f"z{new_free[j] + 1}" for j in sorted(s.support(key))],
            "terms": len(key),
            "degree": max(sum(m) for m, _ in key),
            "provenance": prov,
            "poly": [(m, s.kstr(c)) for m, c in key],
        })

    adj = {j: set() for j in range(len(new_free))}
    used = set()
    for key in residual:
        supp = s.support(key)
        used |= supp
        for x in supp:
            adj[x] |= supp - {x}
    comps = []
    seen = set()
    for start in range(len(new_free)):
        if start not in used or start in seen:
            continue
        dq = deque([start])
        seen.add(start)
        cc = []
        while dq:
            x = dq.popleft()
            cc.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    dq.append(y)
        comps.append(tuple(f"z{new_free[j] + 1}" for j in cc))

    out = {
        "component": cid,
        "mask": mask,
        "D_amplitude_class": 1,
        "cube_pair": (a, b),
        "root": root_name,
        "z20_sign": sign,
        "z20": s.kstr(r),
        "z19": s.kstr(s.kneg(r)),
        "field": "Q(i,sqrt(2),sqrt(3))",
        "affine_equations": len(rows),
        "affine_support_profile": dict(profile),
        "affine_rank": len(pivots),
        "final_variables": tuple(f"z{j + 1}" for j in new_free),
        "base_kernel_polynomials": len(unique),
        "vanished_after_projection": vanished,
        "unique_residual_polynomials": len(residual),
        "term_count_profile": dict(term_profile),
        "degree_profile": dict(degree_profile),
        "variable_count_profile": dict(var_profile),
        "constant_contradictions": len(contradictions),
        "proved_nonzero_scale_monomial_contradictions": len(scale_monomials),
        "singleton_unknown_constraints": len(singleton),
        "univariate_equations": len(univariate),
        "incidence_components": comps,
        "constant_examples": [prov for _key, prov in contradictions[:12]],
        "scale_monomial_examples": [prov for _key, prov in scale_monomials[:12]],
        "singleton_examples": [prov for _key, prov in singleton[:12]],
        "univariate_examples": [
            {
                "variable": f"z{new_free[j] + 1}",
                "provenance": prov,
                "poly": [(m, s.kstr(c)) for m, c in key],
            }
            for key, prov, j in univariate[:20]
        ],
        "shortest": examples,
    }
    print(out, flush=True)
    if contradictions:
        print("RESULT: class-1 sign residual contains a constant contradiction", contradictions[0][1], flush=True)
    elif scale_monomials:
        print("RESULT: class-1 sign residual kills a proved-nonzero scale monomial", scale_monomials[0][1], flush=True)
    else:
        print("RESULT: exact class-1 sign residual compiled; continue local elimination", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=105)
    ap.add_argument("--a", type=int, default=2, choices=(1, 2))
    ap.add_argument("--b", type=int, default=1, choices=(1, 2))
    ap.add_argument("--root", choices=("positive", "negative"), default="positive")
    ap.add_argument("--sign", type=int, choices=(-1, 1), default=1)
    args = ap.parse_args()
    analyze(args.component, args.mask, args.a, args.b, args.root, args.sign)


if __name__ == "__main__":
    main()
