"""Second exact reduction of the four surviving component-5/mask-0 Phase-5 branches.

The three-entry (XXXX;g) certificate leaves only cube pairs (2,1) and (1,2),
for either z0 root, and on each of them proves

    z19 = -z20,
    z20^2 = -1/8.

Since sqrt(-1/8)=i*sqrt(2)/4 already lies in K=Q(i,sqrt(2),sqrt(3)), split
z20 into the two exact signs and project the full 219-polynomial kernel to the
remaining six Laurent variables

    z1,z2,z4,z5,z11,z12,

with only z1,z2 inverted.  Report short equations and direct contradictions;
perform no Groebner computation or global nonlinear solve.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction

import r22_phase5_local_rewrite as lr
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as s


def z20_value(sign):
    # sign * i*sqrt(2)/4 in K = Q(i,sqrt(2),sqrt(3)).
    return ((s.G0, (Fraction(0), Fraction(sign, 4))), s.Q20)


def project_lp(poly, old_free, r):
    pos = {j: k for k, j in enumerate(old_free)}
    p19, p20 = pos[18], pos[19]
    new_free = tuple(j for j in old_free if j not in (18, 19))
    keep = [pos[j] for j in new_free]
    out = {}
    minus_r = s.kneg(r)
    for mon, c in poly.items():
        if mon[p19] < 0 or mon[p20] < 0:
            raise RuntimeError(("unexpected z19/z20 Laurent denominator", mon))
        cc = s.kmul(c, s.kmul(s.kpow(minus_r, mon[p19]), s.kpow(r, mon[p20])))
        mm = tuple(mon[k] for k in keep)
        v = s.kadd(out.get(mm, s.K0), cc)
        if s.kiszero(v):
            out.pop(mm, None)
        else:
            out[mm] = v
    return out, new_free


def analyze(cid, mask, a, b, root_name, sign):
    if (a, b) not in ((2, 1), (1, 2)):
        raise RuntimeError(("not a surviving cube pair", a, b))
    p, q, t = s.branch_values(a, b, root_name)
    _quotient, unique = ml.compile_unique(cid, mask)
    reduced = {key: lr.reduce_poly(key) for key in unique}
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
        raise RuntimeError(("expected rank 10", a, b, root_name, len(pivots)))
    zmaps, old_free = s.build_zmaps(rr, pivots, p, q, t)
    expected = (0, 1, 3, 4, 10, 11, 18, 19)
    if old_free != expected:
        raise RuntimeError(("unexpected old free variables", old_free))

    r = z20_value(sign)
    projected = {}
    new_free = None
    for j, poly in zmaps.items():
        pp, nf = project_lp(poly, old_free, r)
        if new_free is None:
            new_free = nf
        elif new_free != nf:
            raise RuntimeError("projection mismatch")
        projected[j] = pp
    if new_free != (0, 1, 3, 4, 10, 11):
        raise RuntimeError(("unexpected final variables", new_free))

    # Independently assert the three-entry consequences inside the field.
    if not s.kiszero(s.kadd(s.kmul(r, r), s.kr(Fraction(1, 8)))):
        raise RuntimeError(("bad z20 root", sign, s.kstr(r)))

    residual = {}
    vanished = 0
    for key, prov in unique.items():
        lp = s.evaluate(specialized[key], projected, len(new_free))
        ck = s.canonical(lp, new_free)
        if ck is None:
            vanished += 1
        else:
            residual.setdefault(ck, prov)

    term_profile = Counter(); degree_profile = Counter(); var_profile = Counter()
    contradictions = []; scale_monomials = []; singleton = []; univariate = []
    pos = {j: k for k, j in enumerate(new_free)}
    scale_pos = {pos[0], pos[1]}
    for key, prov in residual.items():
        nt = len(key)
        deg = max(sum(mon) for mon, _ in key)
        supp = s.support(key)
        term_profile[nt] += 1; degree_profile[deg] += 1; var_profile[len(supp)] += 1
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
        key=lambda kv: (len(s.support(kv[0])), len(kv[0]), max(sum(m) for m, _ in kv[0]), str(kv[1])),
    )
    examples = []
    for key, prov in order[:40]:
        examples.append({
            "variables": [f"z{new_free[j]+1}" for j in sorted(s.support(key))],
            "terms": len(key),
            "degree": max(sum(m) for m, _ in key),
            "provenance": prov,
            "poly": [(m, s.kstr(c)) for m, c in key],
        })

    adj = {j: set() for j in range(len(new_free))}; used = set()
    for key in residual:
        supp = s.support(key); used |= supp
        for x in supp: adj[x] |= supp - {x}
    comps = []; seen = set()
    for start in range(len(new_free)):
        if start not in used or start in seen: continue
        dq = deque([start]); seen.add(start); cc = []
        while dq:
            x = dq.popleft(); cc.append(x)
            for y in adj[x]:
                if y not in seen: seen.add(y); dq.append(y)
        comps.append(tuple(f"z{new_free[j]+1}" for j in cc))

    out = {
        "component": cid, "mask": mask, "cube_pair": (a, b), "root": root_name,
        "z20_sign": sign, "z20": s.kstr(r), "z19": s.kstr(s.kneg(r)),
        "affine_rank": len(pivots),
        "final_variables": tuple(f"z{j+1}" for j in new_free),
        "base_kernel_polynomials": len(unique), "vanished_after_projection": vanished,
        "unique_residual_polynomials": len(residual),
        "term_count_profile": dict(term_profile), "degree_profile": dict(degree_profile),
        "variable_count_profile": dict(var_profile),
        "constant_contradictions": len(contradictions),
        "proved_nonzero_scale_monomial_contradictions": len(scale_monomials),
        "singleton_unknown_constraints": len(singleton), "univariate_equations": len(univariate),
        "incidence_components": comps,
        "constant_examples": [p for _k, p in contradictions[:8]],
        "scale_monomial_examples": [p for _k, p in scale_monomials[:8]],
        "singleton_examples": [p for _k, p in singleton[:12]],
        "univariate_examples": [
            {"variable": f"z{new_free[j]+1}", "provenance": prov, "poly": [(m, s.kstr(c)) for m, c in key]}
            for key, prov, j in univariate[:16]
        ],
        "shortest": examples,
    }
    print(out, flush=True)
    if contradictions:
        print("RESULT: second reduction contains a constant contradiction", contradictions[0][1], flush=True)
    elif scale_monomials:
        print("RESULT: second reduction kills a proved-nonzero scale monomial", scale_monomials[0][1], flush=True)
    else:
        print("RESULT: second exact finite reduction compiled; continue local elimination", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    ap.add_argument("--a", type=int, default=2, choices=(1, 2))
    ap.add_argument("--b", type=int, default=1, choices=(1, 2))
    ap.add_argument("--root", choices=("positive", "negative"), default="positive")
    ap.add_argument("--sign", type=int, choices=(-1, 1), default=1)
    args = ap.parse_args()
    analyze(args.component, args.mask, args.a, args.b, args.root, args.sign)


if __name__ == "__main__":
    main()
