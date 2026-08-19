"""Exact finite-stratum affine census for component 13 / chirality mask 255.

Run only after the independently verified local relations

    z3^2 = 1/2,
    p^3 = (1-i)/4,
    q^3 = (-1+i)/4,
    z0*z4 = i*q^2*z3,
    z17*z18 = -i*p^2*z3,

and hence p,q,z0,z3,z4,z17,z18 != 0.

Enumerate all 3*3*2 exact (p,q,z3) choices, eliminate z4 and z18 through the
proved-nonzero product relations, strip only common Laurent factors in the
proved-nonzero scale variables z0,z17, and compute the exact affine rank
profile over K=Q(i,sqrt(2),sqrt(3)).  No prior chirality rank split is assumed.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction

import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss

CID = 13
MASK = 255
KEEP_Z = tuple(j for j in range(21) if j not in (3, 4, 18))
POS = {j: k for k, j in enumerate(KEEP_Z)}
NVARS = len(KEEP_Z)
NONZERO_SCALE_POS = (POS[0], POS[17])
KI = ss.kg((Fraction(0), Fraction(1)))


def branch_values(a, b, sign):
    # ((-1-i)/2)^3=(1-i)/4 and ((1+i)/2)^3=(-1+i)/4.
    p0 = ss.kg((Fraction(-1, 2), Fraction(-1, 2)))
    q0 = ss.kg((Fraction(1, 2), Fraction(1, 2)))
    omega = (
        (((Fraction(-1, 2), Fraction(0)), ss.G0)),
        (((Fraction(0), Fraction(1, 2)), ss.G0)),
    )
    s2half = ((ss.G0, (Fraction(1, 2), Fraction(0))), ss.Q20)
    t = s2half if sign > 0 else ss.kneg(s2half)
    return ss.kmul(p0, ss.kpow(omega, a)), ss.kmul(q0, ss.kpow(omega, b)), t


def add_term(poly, mon, coeff):
    if ss.kiszero(coeff): return
    v = ss.kadd(poly.get(mon, ss.K0), coeff)
    if ss.kiszero(v): poly.pop(mon, None)
    else: poly[mon] = v


def specialize_key(key, p, q, t):
    out = {}
    A = ss.kmul(KI, ss.kmul(ss.kpow(q, 2), t))       # z0*z4
    B = ss.kneg(ss.kmul(KI, ss.kmul(ss.kpow(p, 2), t)))  # z17*z18
    for mon, gc in key:
        c = ss.kg(ml.gfromkey(gc))
        c = ss.kmul(c, ss.kpow(p, mon[0]))
        c = ss.kmul(c, ss.kpow(q, mon[1]))
        f = list(mon[2:])
        if f[3]: c = ss.kmul(c, ss.kpow(t, f[3]))
        if f[4]: c = ss.kmul(c, ss.kpow(A, f[4]))
        if f[18]: c = ss.kmul(c, ss.kpow(B, f[18]))
        exps = []
        for j in KEEP_Z:
            e = f[j]
            if j == 0: e -= f[4]      # z4=A/z0
            elif j == 17: e -= f[18]  # z18=B/z17
            exps.append(e)
        add_term(out, tuple(exps), c)
    return out


def strip_nonzero_laurent(poly):
    if not poly: return {}
    mins = {k: min(mon[k] for mon in poly) for k in NONZERO_SCALE_POS}
    out = {}
    for mon, c in poly.items():
        mm = list(mon)
        for k, m in mins.items(): mm[k] -= m
        if any(e < 0 for e in mm):
            raise AssertionError(("unexpected negative exponent", mon, mins, tuple(mm)))
        add_term(out, tuple(mm), c)
    return out


def affine_row(poly):
    coeff = [ss.K0] * NVARS
    const = ss.K0
    for mon, c in poly.items():
        deg = sum(mon)
        if deg == 0:
            const = ss.kadd(const, c); continue
        if deg != 1: return None
        j = next(k for k, e in enumerate(mon) if e)
        if mon[j] != 1: return None
        coeff[j] = ss.kadd(coeff[j], c)
    return coeff + [ss.kneg(const)]


def rref(rows):
    a = [list(r) for r in rows]
    rank = 0; pivots = []
    for col in range(NVARS):
        p = next((i for i in range(rank, len(a)) if not ss.kiszero(a[i][col])), None)
        if p is None: continue
        a[rank], a[p] = a[p], a[rank]
        inv = ss.kinv(a[rank][col])
        a[rank] = [ss.kmul(x, inv) for x in a[rank]]
        for i in range(len(a)):
            if i == rank or ss.kiszero(a[i][col]): continue
            q = a[i][col]
            a[i] = [ss.ksub(x, ss.kmul(q, y)) for x, y in zip(a[i], a[rank])]
        pivots.append(col); rank += 1
    for row in a:
        if all(ss.kiszero(x) for x in row[:NVARS]) and not ss.kiszero(row[NVARS]):
            return a, tuple(pivots), False
    return a, tuple(pivots), True


def branch_census(unique, a, b, sign):
    p, q, t = branch_values(a, b, sign)
    affine=[]; support=Counter(); normalized=[]; constants=[]
    for key, prov in unique.items():
        poly=strip_nonzero_laurent(specialize_key(key,p,q,t))
        if not poly: continue
        normalized.append((poly,prov))
        if len(poly)==1:
            mon,c=next(iter(poly.items()))
            if sum(mon)==0 and not ss.kiszero(c): constants.append(prov)
        row=affine_row(poly)
        if row is not None:
            support[sum(not ss.kiszero(x) for x in row[:NVARS])] += 1
            affine.append(row)
    rr,pivots,consistent=rref(affine)
    free=tuple(j for j in range(NVARS) if j not in pivots)
    forced=[]
    if consistent:
        for i,j in enumerate(pivots):
            if ss.kiszero(rr[i][NVARS]) and all(ss.kiszero(rr[i][k]) for k in free):
                forced.append(KEEP_Z[j])
    out={
        "a":a,"b":b,"sign":"+" if sign>0 else "-",
        "constant_contradictions":len(constants),
        "affine_rows":len(affine),"affine_support_profile":dict(support),
        "consistent":consistent,"rank":len(pivots),"free_dimension":NVARS-len(pivots),
        "pivot_z":tuple(KEEP_Z[j] for j in pivots),
        "free_z":tuple(KEEP_Z[j] for j in free),
        "forced_zero_z":tuple(forced),"normalized_polynomials":len(normalized),
    }
    print(out,flush=True); return out


def main():
    ptarget=ss.kg((Fraction(1,4),Fraction(-1,4)))
    qtarget=ss.kg((Fraction(-1,4),Fraction(1,4)))
    for a in range(3):
        for b in range(3):
            for sign in (1,-1):
                p,q,t=branch_values(a,b,sign)
                if ss.kpow(p,3)!=ptarget or ss.kpow(q,3)!=qtarget:
                    raise AssertionError((a,b,sign,"bad cubic",ss.kstr(ss.kpow(p,3)),ss.kstr(ss.kpow(q,3))))
                if ss.ksub(ss.kmul(t,t),ss.kr(Fraction(1,2)))!=ss.K0:
                    raise AssertionError((a,b,sign,"bad z3 root"))
    _q,unique=ml.compile_unique(CID,MASK)
    rows=[branch_census(unique,a,b,sign) for b in range(3) for a in range(3) for sign in (1,-1)]
    profile=Counter((r["consistent"],r["rank"],r["free_dimension"],r["forced_zero_z"],r["constant_contradictions"]) for r in rows)
    summary={"component":CID,"mask":MASK,"finite_branches":len(rows),"unknown_F_variables_after_local_products":NVARS,"rank_profile":{str(k):v for k,v in profile.items()}}
    print("SUMMARY",summary,flush=True)
    print("RESULT: component 13 / mask 255 finite affine census completed",flush=True)

if __name__=="__main__": main()
