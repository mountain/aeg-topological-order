"""Exact three-cell certificate probe for component 13 / mask 255 rank-10 representative.

For branch (a,b,z3-sign)=(1,1,+), the affine residual contains an 18-equation
subsystem supported only on r=z19 and s=z20.  This gate checks only three fixed
final-pentagon g-cells:

    P1=(XXXX;g)_(0,3), P2=(XXXX;g)_(0,2), P3=(XXXX;g)_(0,1).

P1 and P2 must have the exact shapes

    C + A*s^2 + B*r*s = 0,
    C + A*r^2 + B*r*s = 0,

with A != 0.  Thus r^2=s^2 and r=+/-s.  On each slice P1 fixes s^2 exactly;
the fixed homogeneous quadratic P3 must then evaluate to a nonzero exact field
element.  No Groebner/global nonlinear solve is used.
"""
from __future__ import annotations

import r22_phase5_component13_mask255_residual_scan as rs
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss

CID=13; MASK=255; BRANCH=(1,1,1)
P1=(("X","X","X","X","g"),(0,3))
P2=(("X","X","X","X","g"),(0,2))
P3=(("X","X","X","X","g"),(0,1))
EXPECTED_FREE=(0,5,6,9,10,17,19,20)

def find_by_prov(data,target):
    hits=[]
    for k,ps in data['provenance'].items():
        if target in ps:hits.append(data['residual'][k])
    if len(hits)!=1:raise AssertionError((target,'residual multiplicity',len(hits)))
    return hits[0]

def poly2(raw,rpos,spos):
    out={}
    for mon,c in raw.items():
        if any(e for j,e in enumerate(mon) if j not in (rpos,spos)):
            raise AssertionError(('escaped core',mon))
        k=(mon[rpos],mon[spos]); v=ss.kadd(out.get(k,ss.K0),c)
        if ss.kiszero(v):out.pop(k,None)
        else:out[k]=v
    return out

def main():
    _q,u=ml.compile_unique(CID,MASK); data=rs.build_branch(u,*BRANCH)
    if data['free']!=EXPECTED_FREE:raise AssertionError(('unexpected free',data['free']))
    rpos=data['free'].index(19); spos=data['free'].index(20)
    e1=poly2(find_by_prov(data,P1),rpos,spos)
    e2=poly2(find_by_prov(data,P2),rpos,spos)
    e3=poly2(find_by_prov(data,P3),rpos,spos)
    if set(e1)!={(0,0),(0,2),(1,1)}:raise AssertionError(('bad P1 support',e1))
    if set(e2)!={(0,0),(2,0),(1,1)}:raise AssertionError(('bad P2 support',e2))
    C=e1[(0,0)]; A=e1[(0,2)]; B=e1[(1,1)]
    if ss.kiszero(A):raise AssertionError('A vanished')
    if e2[(0,0)]!=C or e2[(2,0)]!=A or e2[(1,1)]!=B:
        raise AssertionError(('P1/P2 coefficient symmetry failed',e1,e2))
    if set(e3)!={(2,0),(1,1),(0,2)}:raise AssertionError(('bad P3 support',e3))

    rows=[]
    for eps,label in ((ss.K1,'r=s'),(ss.kneg(ss.K1),'r=-s')):
        denom=ss.kadd(A,ss.kmul(eps,B))
        if ss.kiszero(denom):raise AssertionError((label,'anchor denominator vanished'))
        s2=ss.kdiv(ss.kneg(C),denom)
        third_coeff=ss.kadd(ss.kadd(e3[(2,0)],ss.kmul(eps,e3[(1,1)])),e3[(0,2)])
        value=ss.kmul(third_coeff,s2)
        if ss.kiszero(value):raise AssertionError((label,'P3 vanishes',ss.kstr(s2),ss.kstr(third_coeff)))
        rows.append({'slice':label,'s2':ss.kstr(s2),'P3':ss.kstr(value)})

    out={'branch':(1,1,'+'),'free':data['free'],'core':('r=z19','s=z20'),'cells':(P1,P2,P3),'difference':'A*(s^2-r^2)','slices':rows,'closed':True}
    print(out,flush=True)
    print('RESULT: representative component-13/mask-255 rank-10 branch is excluded by three fixed g-cells',flush=True)
if __name__=='__main__':main()
