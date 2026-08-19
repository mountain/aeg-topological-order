"""Exact F-invertibility gate for component 13 / chirality mask 255 rank-11 strata.

Finite census gives z7=z8=0 on p-side and z13=z14=0 on q-side.  Rebuild all
required Phase-4 F determinant polynomials and close a pattern here only if a
required determinant loses every monomial.  No nonlinear solving is used.
"""
from __future__ import annotations
import r22_epsminus_f_parametric as fp
CID=13; MASK=255
PATTERNS={"p-side-rank11":(7,8),"q-side-rank11":(13,14)}
def surviving_terms(det,zero_roots): return [(m,r) for m,r in det if not any(x in zero_roots for x in m)]
def main():
    scalar,ddata,params,emats,droot=fp.parametric_lower_data(CID,MASK)
    uf,support,_degrees,n_eq=fp.build_f_system(scalar,ddata,params,emats)
    profile,_=fp.root_condition_profile(uf); active=sorted(fp.active_roots(profile))
    if len(active)!=21: raise AssertionError(("expected 21 active",len(active)))
    if any(info["conditions"] for info in profile.values() if not info["forced"]): raise AssertionError("unexpected conditional component")
    aset=set(active); dets={}
    for key,_dim in fp.F_BLOCKS:
        desc=fp.block_descriptor(uf,profile,key,aset); det=fp.determinant_generic(desc)
        if not det: raise AssertionError(("generic determinant vanished",key))
        dets[key]=det
    rows=[]
    for name,pattern in PATTERNS.items():
        zero={active[j] for j in pattern}; killed=[]; prof={}
        for key,det in dets.items():
            surv=surviving_terms(det,zero); prof[key]={"terms":len(surv),"r_exponents":tuple(sorted({r for _m,r in surv}))}
            if not surv: killed.append(key)
        row={"type":name,"zero_z":pattern,"killed_required_blocks":tuple(killed),"min_surviving_terms":min(v["terms"] for v in prof.values()),"XXXX":prof[("X","X","X","X")]}
        print(row,flush=True); rows.append(row)
    summary={"component":CID,"mask":MASK,"D_root_group":droot,"F_linear_equations":n_eq,"F_linear_support":dict(support),"patterns":len(rows),"closed_by_invertibility":sum(bool(r["killed_required_blocks"]) for r in rows)}
    print("SUMMARY",summary,flush=True)
    print("RESULT:","both patterns violate F invertibility" if summary["closed_by_invertibility"]==2 else "at least one forced-zero stratum remains F-invertible",flush=True)
if __name__=="__main__": main()
