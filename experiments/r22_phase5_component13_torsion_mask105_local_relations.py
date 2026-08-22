"""Source-validated Phase-5 local relations for component 13 / mask 105 / D class 1."""
from __future__ import annotations

import sympy as sp

import r22_phase5_monomial_lift as ml
import r22_phase5_torsion_sheet as ts

CID=13
MASK=105
P1=(("X","X","X","X","X"),(0,0))
P2=(("X","X","X","X","X"),(0,2))
P3=(("X","X","X","X","Y"),(0,18))
P4=(("X","X","X","X","Y"),(18,18))
P5=(("X","X","X","X","1"),(0,0))
PROVS=(P1,P2,P3,P4,P5)


def gc_expr(k):
    a,b=ml.gfromkey(k)
    return sp.Rational(a.numerator,a.denominator)+sp.I*sp.Rational(b.numerator,b.denominator)


def key_expr(key,symbols):
    out=sp.Integer(0)
    for mon,gc in key:
        term=gc_expr(gc)
        for x,e in zip(symbols,mon):
            if e: term*=x**e
        out+=term
    return sp.expand(out)


def main():
    with ts.second_sheet_provider():
        quotient,unique=ml.compile_unique(CID,MASK)
    names=quotient["variables"]
    if names != ("p","q")+tuple(f"z{i}" for i in range(21)):
        raise AssertionError(("unexpected chart",names))
    symbols=sp.symbols("p q "+" ".join(f"z{i}" for i in range(21)))
    p,q=symbols[:2]; z=symbols[2:]
    by={prov:key for key,prov in unique.items()}
    missing=[x for x in PROVS if x not in by]
    if missing: raise AssertionError(("missing provenance",missing))
    e={prov:key_expr(by[prov],symbols) for prov in PROVS}
    s=z[0]; A=z[3]*z[10]; B=z[6]*z[9]
    expected={
        P1:p**2*s-sp.I*A,
        P2:p*A-(1+sp.I)*s/4,
        P3:q*B+(1-sp.I)*s/4,
        P4:q**2*s+B,
        P5:p*A+sp.I*q*B+(1+sp.I)*s**2/4-(1+sp.I)/8,
    }
    for prov in PROVS:
        if sp.expand(e[prov]-expected[prov])!=0:
            raise AssertionError((prov,e[prov],expected[prov]))

    scale=sp.factor(e[P5]-e[P2]-sp.I*e[P3])
    scale_target=sp.factor((1+sp.I)*(2*s**2-1)/8)
    if sp.expand(scale-scale_target)!=0:
        raise AssertionError(("scale combination",scale,scale_target))

    pcombo=sp.factor(p*e[P1]+sp.I*e[P2])
    ptarget=sp.factor(s*(p**3-(-1+sp.I)/4))
    if sp.expand(pcombo-ptarget)!=0:
        raise AssertionError(("p cube",pcombo,ptarget))

    qcombo=sp.factor(q*e[P4]-e[P3])
    qtarget=sp.factor(s*(q**3-(1-sp.I)/4))
    if sp.expand(qcombo-qtarget)!=0:
        raise AssertionError(("q cube",qcombo,qtarget))

    print("SUMMARY",{
        "component":CID,"mask":MASK,"D_amplitude_class":1,
        "scale":"z0","scale_equation":"z0^2=1/2",
        "p3":"(-1+i)/4","q3":"(1-i)/4",
        "p_product":"z3*z10=-i*p^2*z0",
        "q_product":"z6*z9=-q^2*z0",
        "source_cells":PROVS,
        "prelocalization_scale_combination":"P5-P2-i*P3=(1+i)*(2*z0^2-1)/8",
    },flush=True)
    print("RESULT: component 13 mask 105 class-1 five-cell local model is source-validated",flush=True)

if __name__=="__main__": main()
