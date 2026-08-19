"""Exact three-cell certificates for all eight component-13/mask-150 rank-10 strata.

Each branch is rebuilt independently.  The same three fixed final-pentagon
cells are required:

    P1=(XXXX;g)_(0,3), P2=(XXXX;g)_(0,2), P3=(XXXX;g)_(0,0).

P1 and P2 are checked only up to their own nonzero scalar factors; after
normalization each must be

    1 + 4*r*s - 4*s^2 = 0,
    1 + 4*r*s - 4*r^2 = 0,

for r=z19,s=z20.  Thus r=+-s.  The r=s slice contradicts P1 immediately;
on r=-s, P1 gives s^2=1/8 and P3 must evaluate to a nonzero exact element.
No branch-specific alternative cell is allowed.
"""
from __future__ import annotations

from fractions import Fraction

import r22_phase5_component13_mask150_residual_scan as rs
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss

CID = 13
MASK = 150
P1 = (("X", "X", "X", "X", "g"), (0, 3))
P2 = (("X", "X", "X", "X", "g"), (0, 2))
P3 = (("X", "X", "X", "X", "g"), (0, 0))
CASES = tuple((a, b, sign) for (a, b) in ((1,1),(2,1),(1,2),(2,2)) for sign in (1,-1))
EXPECTED_FREE = (0, 1, 10, 11, 14, 15, 19, 20)


def find_by_prov(data, target):
    hits=[]
    for key,provs in data["provenance"].items():
        if target in provs:
            hits.append(data["residual"][key])
    if len(hits)!=1:
        raise AssertionError((target,"residual multiplicity",len(hits)))
    return hits[0]


def poly2(raw,rpos,spos):
    out={}
    for mon,c in raw.items():
        if any(e for j,e in enumerate(mon) if j not in (rpos,spos)):
            raise AssertionError(("escaped two-variable core",mon))
        k=(mon[rpos],mon[spos])
        v=ss.kadd(out.get(k,ss.K0),c)
        if ss.kiszero(v): out.pop(k,None)
        else: out[k]=v
    return out


def certify(unique,a,b,sign):
    data=rs.build_branch(unique,a,b,sign)
    if data["free"]!=EXPECTED_FREE:
        raise AssertionError((a,b,sign,"unexpected free",data["free"]))
    rpos=data["free"].index(19); spos=data["free"].index(20)
    e1=poly2(find_by_prov(data,P1),rpos,spos)
    e2=poly2(find_by_prov(data,P2),rpos,spos)
    e3=poly2(find_by_prov(data,P3),rpos,spos)

    if set(e1)!={(0,0),(0,2),(1,1)}:
        raise AssertionError((a,b,sign,"bad P1 support",e1))
    if set(e2)!={(0,0),(1,1),(2,0)}:
        raise AssertionError((a,b,sign,"bad P2 support",e2))
    c1=e1[(0,0)]; c2=e2[(0,0)]
    if ss.kiszero(c1) or ss.kiszero(c2):
        raise AssertionError((a,b,sign,"zero anchor scale"))
    four=ss.kr(Fraction(4,1)); minus_four=ss.kr(Fraction(-4,1))
    # scale-invariant normalized forms.
    if ss.kdiv(e1[(1,1)],c1)!=four or ss.kdiv(e1[(0,2)],c1)!=minus_four:
        raise AssertionError((a,b,sign,"P1 normalized form failed"))
    if ss.kdiv(e2[(1,1)],c2)!=four or ss.kdiv(e2[(2,0)],c2)!=minus_four:
        raise AssertionError((a,b,sign,"P2 normalized form failed"))

    # r=s -> normalized P1 is 1=0.
    plus_value=ss.K1
    # r=-s -> normalized P1 gives s^2=1/8.
    s2=ss.kr(Fraction(1,8))
    if set(e3)-{(2,0),(1,1),(0,2)}:
        raise AssertionError((a,b,sign,"P3 unexpected support",e3))
    Crr=e3.get((2,0),ss.K0); Crs=e3.get((1,1),ss.K0); Css=e3.get((0,2),ss.K0)
    minus_coeff=ss.ksub(ss.kadd(Crr,Css),Crs)
    minus_value=ss.kmul(minus_coeff,s2)
    if ss.kiszero(minus_value):
        raise AssertionError((a,b,sign,"r=-s slice survives P3",ss.kstr(minus_coeff)))

    row={
        "a":a,"b":b,"z6_sign":"+" if sign>0 else "-",
        "cells":(P1,P2,P3),
        "normalized_anchors":("1+4rs-4s^2","1+4rs-4r^2"),
        "r_equals_s":"P1 -> 1=0",
        "r_equals_minus_s":"s^2=1/8",
        "P3_at_minus_slice":ss.kstr(minus_value),
        "closed":True,
    }
    print(row,flush=True); return row


def main():
    _q,unique=ml.compile_unique(CID,MASK)
    rows=[certify(unique,*case) for case in CASES]
    if len(rows)!=8 or not all(r["closed"] for r in rows):
        raise AssertionError(rows)
    print("SUMMARY",{"closed":8,"total":8,"cells":(P1,P2,P3)},flush=True)
    print("RESULT: all eight component-13/mask-150 rank-10 strata are excluded by the same three fixed g-cells",flush=True)

if __name__=="__main__": main()
