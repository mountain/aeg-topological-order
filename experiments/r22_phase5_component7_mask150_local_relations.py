"""Exact two-cell source certificate for component 7 / chirality mask 150."""
from __future__ import annotations
import sympy as sp
import r22_phase5_monomial_lift as ml

CID, MASK = 7, 150
P1 = (("X","X","X","X","X"),(0,0))
P2 = (("X","X","X","X","1"),(0,0))
P,Q = sp.symbols("p q")
ZS = sp.symbols("z0:17")
Z0 = ZS[0]
VARS = (P,Q)+ZS

def ce(gc):
    (ar,ad),(br,bd)=gc
    return sp.Rational(ar,ad)+sp.I*sp.Rational(br,bd)

def expr(key):
    out=sp.Integer(0)
    for mon,gc in key:
        t=ce(gc)
        for v,e in zip(VARS,mon):
            if e:t*=v**e
        out+=t
    return sp.expand(out)

def monic(x):
    p=sp.Poly(sp.expand(x),*VARS,extension=[sp.I])
    if p.is_zero: raise AssertionError("zero")
    return p.monic()

def main():
    _q,u=ml.compile_unique(CID,MASK)
    bp={prov:key for key,prov in u.items()}
    e1,e2=expr(bp[P1]),expr(bp[P2])
    if monic(e1)!=monic(Z0): raise AssertionError(("P1",e1))
    if monic(e2)!=monic(Z0**2-sp.Rational(1,2)): raise AssertionError(("P2",e2))
    c=sp.expand((Z0**2-sp.Rational(1,2)).subs(Z0,0))
    if c!=-sp.Rational(1,2): raise AssertionError(c)
    print({"component":CID,"mask":MASK,"unique_kernel_polynomials":len(u),"P1":str(e1),"P2":str(e2),"contradiction":str(c),"closed":True},flush=True)
    print("RESULT: component 7 / mask 150 is excluded by two fixed final-pentagon cells",flush=True)
if __name__=="__main__": main()
