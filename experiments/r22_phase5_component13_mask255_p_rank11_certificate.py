"""One-cell exact certificates for all four p-side rank-11 strata of component 13 / mask 255."""
from __future__ import annotations
import r22_phase5_component13_mask255_residual_scan as rs
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss
TARGET=(("X","X","X","X","X"),(5,2))
CASES=((1,0,1),(1,0,-1),(2,0,1),(2,0,-1))
EXPECTED_FREE=(0,5,6,9,10,17,20)
def certify(unique,a,b,sign):
    data=rs.build_branch(unique,a,b,sign)
    if data['free']!=EXPECTED_FREE:raise AssertionError((a,b,sign,'unexpected free',data['free']))
    hits=[]
    for k,ps in data['provenance'].items():
        if TARGET in ps:hits.append(data['residual'][k])
    if len(hits)!=1:raise AssertionError((a,b,sign,'target multiplicity',len(hits)))
    p=hits[0]
    if len(p)!=1:raise AssertionError((a,b,sign,'not singleton',rs.poly_string(p,data['free_names'])))
    mon,c=next(iter(p.items()))
    if mon!=(0,)*len(EXPECTED_FREE) or ss.kiszero(c):raise AssertionError((a,b,sign,'not nonzero constant',mon,ss.kstr(c)))
    row={'a':a,'b':b,'z3_sign':'+' if sign>0 else '-','provenance':TARGET,'residual':rs.poly_string(p,data['free_names']),'closed':True}
    print(row,flush=True);return row
def main():
    _q,u=ml.compile_unique(13,255); rows=[certify(u,*x) for x in CASES]
    if not all(r['closed'] for r in rows):raise AssertionError(rows)
    print('SUMMARY',{'closed':4,'total':4,'cell':TARGET},flush=True)
    print('RESULT: all four component-13/mask-255 p-side rank-11 strata are excluded by one constant local cell',flush=True)
if __name__=='__main__':main()
