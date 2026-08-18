"""Exact sparse residual compiler for the Phase-5 rank-drop finite strata.

This is the non-SymPy counterpart of r22_phase5_survivor_residual.py.  The
surviving cube-root branches have a small exact coefficient field

    K = Q(i, sqrt(2), sqrt(3)),

and an affine closure of rank 10.  Rather than expanding 219 residual equations
with generic SymPy algebraic expressions, this script performs all coefficient
arithmetic directly in K and all variable arithmetic as sparse Laurent
polynomials.

Only z1,z2 are inverted, because z1,z2,z3,z8 are already proved nonzero and the
product identities eliminate z3,z8.  No Groebner basis or nonlinear solve is
performed.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction

import r22_phase5_local_rewrite as lr
import r22_phase5_monomial_lift as ml


# ---------------------------------------------------------------------------
# Exact coefficient field K = Q(i, sqrt(2), sqrt(3)).
#
# G  = Q(i):                 (a,b) = a+b*i
# Q2 = Q(i,sqrt(2)):         (a,b) = a+b*sqrt(2), a,b in G
# K  = Q(i,sqrt(2),sqrt(3)): (a,b) = a+b*sqrt(3), a,b in Q2
# ---------------------------------------------------------------------------

G0 = (Fraction(0), Fraction(0))
G1 = (Fraction(1), Fraction(0))
GI = (Fraction(0), Fraction(1))
Q20 = (G0, G0)
Q21 = (G1, G0)
K0 = (Q20, Q20)
K1 = (Q21, Q20)


def gadd(x, y): return (x[0] + y[0], x[1] + y[1])
def gneg(x): return (-x[0], -x[1])
def gsub(x, y): return gadd(x, gneg(y))
def gmul(x, y): return (x[0]*y[0] - x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def giszero(x): return x == G0

def ginv(x):
    n = x[0]*x[0] + x[1]*x[1]
    if n == 0: raise ZeroDivisionError(x)
    return (x[0]/n, -x[1]/n)

def gdiv(x, y): return gmul(x, ginv(y))


def q2add(x, y): return (gadd(x[0], y[0]), gadd(x[1], y[1]))
def q2neg(x): return (gneg(x[0]), gneg(x[1]))
def q2sub(x, y): return q2add(x, q2neg(y))
def q2mul(x, y):
    return (
        gadd(gmul(x[0], y[0]), (lambda z: (2*z[0], 2*z[1]))(gmul(x[1], y[1]))),
        gadd(gmul(x[0], y[1]), gmul(x[1], y[0])),
    )
def q2iszero(x): return x == Q20

def q2inv(x):
    den = gsub(gmul(x[0], x[0]), (lambda z: (2*z[0], 2*z[1]))(gmul(x[1], x[1])))
    if giszero(den): raise ZeroDivisionError(x)
    return (gdiv(x[0], den), gdiv(gneg(x[1]), den))

def q2div(x, y): return q2mul(x, q2inv(y))


def kadd(x, y): return (q2add(x[0], y[0]), q2add(x[1], y[1]))
def kneg(x): return (q2neg(x[0]), q2neg(x[1]))
def ksub(x, y): return kadd(x, kneg(y))
def kmul(x, y):
    three_bd = q2mul(x[1], y[1])
    three_bd = (
        (3*three_bd[0][0], 3*three_bd[0][1]),
        (3*three_bd[1][0], 3*three_bd[1][1]),
    )
    return (
        q2add(q2mul(x[0], y[0]), three_bd),
        q2add(q2mul(x[0], y[1]), q2mul(x[1], y[0])),
    )
def kiszero(x): return x == K0

def kinv(x):
    b2 = q2mul(x[1], x[1])
    three_b2 = (
        (3*b2[0][0], 3*b2[0][1]),
        (3*b2[1][0], 3*b2[1][1]),
    )
    den = q2sub(q2mul(x[0], x[0]), three_b2)
    if q2iszero(den): raise ZeroDivisionError(x)
    return (q2div(x[0], den), q2div(q2neg(x[1]), den))

def kdiv(x, y): return kmul(x, kinv(y))

def kpow(x, n):
    if n < 0: return kpow(kinv(x), -n)
    out = K1
    base = x
    while n:
        if n & 1: out = kmul(out, base)
        base = kmul(base, base)
        n >>= 1
    return out


def kg(g): return ((g, G0), Q20)
def kr(x): return kg((Fraction(x), Fraction(0)))


def branch_values(a, b, root_name):
    p0 = kg((Fraction(-1,2), Fraction(-1,2)))
    q0 = kg((Fraction(1,2), Fraction(-1,2)))
    # omega = -1/2 + (i/2)*sqrt(3)
    omega = (
        (( (Fraction(-1,2), Fraction(0)), G0 )),
        (( (Fraction(0), Fraction(1,2)), G0 )),
    )
    # sqrt(6)/2 = (sqrt(2)/2)*sqrt(3)
    s6half = (Q20, (G0, (Fraction(1,2), Fraction(0))))
    t = kadd(kr(-1), s6half if root_name == "positive" else kneg(s6half))
    return kmul(p0, kpow(omega, a)), kmul(q0, kpow(omega, b)), t


def kstr(x):
    vals = [
        x[0][0][0], x[0][0][1], x[0][1][0], x[0][1][1],
        x[1][0][0], x[1][0][1], x[1][1][0], x[1][1][1],
    ]
    names = ["1", "i", "s2", "i*s2", "s3", "i*s3", "s6", "i*s6"]
    parts = [f"({v})*{n}" for v, n in zip(vals, names) if v]
    return "0" if not parts else "+".join(parts)


# ---------------------------------------------------------------------------
# Sparse z-polynomials and affine closure.
# ---------------------------------------------------------------------------

PROVED_NONZERO_Z = (0, 1, 2, 7)  # z1,z2,z3,z8, zero-based


def specialize(poly, p, q, t):
    out = {}
    for mon, gc in poly.items():
        c = kg(gc)
        c = kmul(c, kpow(p, mon[0]))
        c = kmul(c, kpow(q, mon[1]))
        c = kmul(c, kpow(t, mon[2]))
        zm = tuple(mon[3:])
        v = kadd(out.get(zm, K0), c)
        if kiszero(v): out.pop(zm, None)
        else: out[zm] = v
    return out


def strip_common_nonzero(poly):
    if not poly: return {}
    mins = {j: min(m[j] for m in poly) for j in PROVED_NONZERO_Z}
    out = {}
    for mon, c in poly.items():
        mm = list(mon)
        for j, v in mins.items(): mm[j] -= v
        out[tuple(mm)] = c
    return out


def affine_row(poly):
    coeff = [K0] * 20
    const = K0
    for mon, c in poly.items():
        deg = sum(mon)
        if deg == 0:
            const = kadd(const, c)
            continue
        if deg != 1: return None
        j = next(k for k, e in enumerate(mon) if e)
        if mon[j] != 1: return None
        coeff[j] = kadd(coeff[j], c)
    return coeff + [kneg(const)]


def rref(rows):
    a = [list(r) for r in rows]
    rank = 0
    pivots = []
    for col in range(20):
        p = next((i for i in range(rank, len(a)) if not kiszero(a[i][col])), None)
        if p is None: continue
        a[rank], a[p] = a[p], a[rank]
        inv = kinv(a[rank][col])
        a[rank] = [kmul(x, inv) for x in a[rank]]
        for i in range(len(a)):
            if i == rank or kiszero(a[i][col]): continue
            q = a[i][col]
            a[i] = [ksub(x, kmul(q, y)) for x, y in zip(a[i], a[rank])]
        pivots.append(col)
        rank += 1
    for row in a:
        if all(kiszero(x) for x in row[:20]) and not kiszero(row[20]):
            raise RuntimeError("affine closure inconsistent")
    return a, tuple(pivots)


# ---------------------------------------------------------------------------
# Sparse Laurent polynomials in the final free variables.
# ---------------------------------------------------------------------------

def lp_add_scaled(dst, src, scale=K1):
    for m, c in src.items():
        v = kadd(dst.get(m, K0), kmul(scale, c))
        if kiszero(v): dst.pop(m, None)
        else: dst[m] = v
    return dst


def lp_mul(a, b):
    if not a or not b: return {}
    out = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(x+y for x,y in zip(ma,mb))
            v = kadd(out.get(m, K0), kmul(ca, cb))
            if kiszero(v): out.pop(m, None)
            else: out[m] = v
    return out


def lp_pow(a, n, nvars):
    out = {(0,)*nvars: K1}
    for _ in range(n): out = lp_mul(out, a)
    return out


def lp_const(c, nvars):
    return {} if kiszero(c) else {(0,)*nvars: c}


def build_zmaps(rr, pivots, p, q, t):
    free = tuple(j for j in range(20) if j not in pivots)
    final_free = tuple(j for j in free if j not in (2,7))
    pos = {j:k for k,j in enumerate(final_free)}
    n = len(final_free)

    def var(j):
        m = [0]*n; m[pos[j]] = 1
        return {tuple(m): K1}

    maps = {}
    for j in final_free: maps[j] = var(j)

    # z3 = i*p^2*t/z2, z8 = -i*q^2*t/z1
    c3 = kmul(kg(GI), kmul(kpow(p,2), t))
    c8 = kneg(kmul(kg(GI), kmul(kpow(q,2), t)))
    m3 = [0]*n; m3[pos[1]] = -1
    m8 = [0]*n; m8[pos[0]] = -1
    maps[2] = {tuple(m3): c3}
    maps[7] = {tuple(m8): c8}

    # Each RREF pivot is affine in the free variables only.
    for row_i, j in enumerate(pivots):
        expr = lp_const(rr[row_i][20], n)
        for k in free:
            if kiszero(rr[row_i][k]): continue
            lp_add_scaled(expr, maps[k], kneg(rr[row_i][k]))
        maps[j] = expr

    if len(maps) != 20:
        raise RuntimeError(("incomplete z map", sorted(set(range(20))-set(maps))))
    return maps, final_free


def evaluate(poly, zmaps, nvars):
    out = {}
    for mon, c in poly.items():
        term = lp_const(c, nvars)
        for j, e in enumerate(mon):
            if e: term = lp_mul(term, lp_pow(zmaps[j], e, nvars))
            if not term: break
        lp_add_scaled(out, term)
    return out


def canonical(poly, final_free):
    if not poly: return None
    # Only z1,z2 may be divided out.  They are final_free positions 0,1 in all
    # branches studied here, but use the index map rather than assume ordering.
    pos = {j:k for k,j in enumerate(final_free)}
    shift = [0]*len(final_free)
    for j in (0,1):
        k = pos[j]
        shift[k] = min(m[k] for m in poly)
    shifted = {}
    for mon, c in poly.items():
        mm = tuple(e-shift[k] if k in (pos[0],pos[1]) else e for k,e in enumerate(mon))
        if any(e < 0 for k,e in enumerate(mm) if k not in (pos[0],pos[1])):
            raise RuntimeError(("unexpected non-scale Laurent exponent", mm))
        shifted[mm] = c
    lead_mon = max(shifted)
    lead = shifted[lead_mon]
    return tuple((m, kdiv(shifted[m], lead)) for m in sorted(shifted, reverse=True))


def support(key):
    return {j for mon,_c in key for j,e in enumerate(mon) if e}


def analyze(cid, mask, a, b, root_name):
    p, q, t = branch_values(a,b,root_name)
    _quotient, unique = ml.compile_unique(cid, mask)
    reduced = {key: lr.reduce_poly(key) for key in unique}
    specialized = {key: specialize(poly,p,q,t) for key,poly in reduced.items()}

    rows = []
    profile = Counter()
    for key, prov in unique.items():
        zpoly = strip_common_nonzero(specialized[key])
        ar = affine_row(zpoly)
        if ar is None: continue
        if all(kiszero(x) for x in ar[:20]):
            if not kiszero(ar[20]): raise RuntimeError(("localized affine contradiction",prov))
            continue
        s = sum(1 for x in ar[:20] if not kiszero(x))
        profile[s] += 1
        rows.append(ar)

    rr, pivots = rref(rows)
    zmaps, final_free = build_zmaps(rr,pivots,p,q,t)
    n = len(final_free)

    residual = {}
    vanished = 0
    for key, prov in unique.items():
        lp = evaluate(specialized[key], zmaps, n)
        ck = canonical(lp, final_free)
        if ck is None:
            vanished += 1
        else:
            residual.setdefault(ck, prov)

    term_profile = Counter(); degree_profile = Counter(); var_profile = Counter()
    contradictions = []; scale_monomials = []; singleton = []; univariate = []
    pos = {j:k for k,j in enumerate(final_free)}
    scale_pos = {pos[0],pos[1]}
    for key,prov in residual.items():
        nt = len(key); deg = max(sum(mon) for mon,_ in key); supp = support(key)
        term_profile[nt] += 1; degree_profile[deg] += 1; var_profile[len(supp)] += 1
        if not supp: contradictions.append((key,prov))
        if nt == 1:
            mon,_ = key[0]
            if all(e == 0 or j in scale_pos for j,e in enumerate(mon)):
                scale_monomials.append((key,prov))
            else:
                singleton.append((key,prov))
        if len(supp)==1: univariate.append((key,prov,next(iter(supp))))

    order = sorted(residual.items(), key=lambda kv:(len(support(kv[0])),len(kv[0]),max(sum(m) for m,_ in kv[0]),str(kv[1])))
    examples=[]
    for key,prov in order[:40]:
        examples.append({
            "variables": [f"z{final_free[j]+1}" for j in sorted(support(key))],
            "terms": len(key),
            "degree": max(sum(m) for m,_ in key),
            "provenance": prov,
            "poly": [(m,kstr(c)) for m,c in key],
        })

    # Incidence components.
    adj={j:set() for j in range(n)}; used=set()
    for key in residual:
        s=support(key); used|=s
        for x in s: adj[x]|=(s-{x})
    comps=[]; seen=set()
    for s in range(n):
        if s not in used or s in seen: continue
        dq=deque([s]); seen.add(s); cc=[]
        while dq:
            x=dq.popleft(); cc.append(x)
            for y in adj[x]:
                if y not in seen: seen.add(y); dq.append(y)
        comps.append(tuple(f"z{final_free[j]+1}" for j in cc))

    out={
        "component":cid,"mask":mask,"cube_pair":(a,b),"root":root_name,
        "field":"Q(i,sqrt(2),sqrt(3))",
        "affine_equations":len(rows),"affine_support_profile":dict(profile),
        "affine_rank":len(pivots),"affine_free_dimension":20-len(pivots),
        "pivot_variables":tuple(j+1 for j in pivots),
        "final_free_variables":tuple(f"z{j+1}" for j in final_free),
        "final_free_count":n,
        "base_kernel_polynomials":len(unique),"vanished_after_projection":vanished,
        "unique_residual_polynomials":len(residual),
        "term_count_profile":dict(term_profile),"degree_profile":dict(degree_profile),
        "variable_count_profile":dict(var_profile),
        "constant_contradictions":len(contradictions),
        "proved_nonzero_scale_monomial_contradictions":len(scale_monomials),
        "singleton_unknown_constraints":len(singleton),"univariate_equations":len(univariate),
        "incidence_components":comps,"shortest":examples,
    }
    print(out,flush=True)
    if contradictions:
        print("RESULT: rank-drop residual contains constant contradiction",contradictions[0][1],flush=True)
    elif scale_monomials:
        print("RESULT: rank-drop residual kills proved-nonzero scale monomial",scale_monomials[0][1],flush=True)
    else:
        print("RESULT: exact sparse rank-drop residual compiled; continue local reduction",flush=True)
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--component",type=int,default=5)
    ap.add_argument("--mask",type=int,default=0)
    ap.add_argument("--a",type=int,default=1,choices=(0,1,2))
    ap.add_argument("--b",type=int,default=1,choices=(0,1,2))
    ap.add_argument("--root",choices=("positive","negative"),default="positive")
    args=ap.parse_args()
    analyze(args.component,args.mask,args.a,args.b,args.root)

if __name__=="__main__": main()
