"""Exact 18-stratum Phase-5 audit for component 5, D-amplitude class 1.

This gate consumes the five-cell source relations established by
r22_phase5_component5_torsion_local_relations.py and the independent raw
z0=0 closure.  It therefore works on the legitimate localization z0 != 0.

For mask 0 the fresh class-1 relations are

    z2*z3 = -i*p^2*z0,
    z1*z8 = -i*q^2*z0,
    p^3 = (-1+i)/4,
    q^3 = (-1-i)/4,
    2*z0^2 + 4*z0 - 1 = 0.

The generic component-5 finite-stratum machinery is reused only as an algebraic
engine.  The historical class-0 relation constants are not imported.  All 18
branches and all target-cell remainders are recomputed from the class-1 kernel.
"""
from __future__ import annotations

import argparse
from fractions import Fraction

import sympy as sp

import r22_phase5_component5_rest_audit as fa
import r22_phase5_torsion_sheet as ts


def relation(mask: int):
    if mask != 0:
        raise ValueError(("only mask 0 is source-validated at this gate", mask))
    return {
        "P3": (Fraction(-1, 4), Fraction(1, 4)),
        "Q3": (Fraction(-1, 4), Fraction(-1, 4)),
        "Z23": fa.NEG_I,
        "Z18": fa.NEG_I,
        # Exact cube roots; multiplying by OMEGA^a/b enumerates all roots.
        "P0": (1 + sp.I) / 2,
        "Q0": (1 - sp.I) / 2,
    }


def audit(cid: int, mask: int):
    old = fa.REL.get(mask)
    fa.REL[mask] = relation(mask)
    try:
        with ts.second_sheet_provider():
            out = fa.audit_mask(cid, mask)
    finally:
        if old is None:
            fa.REL.pop(mask, None)
        else:
            fa.REL[mask] = old

    out = dict(out)
    out["D_amplitude_class"] = 1
    if out["total"] != 18:
        raise AssertionError(("finite branch census is not 18", out))
    print("TORSION_SHEET_FINITE", out, flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, default=0)
    args = ap.parse_args()
    audit(args.component, args.mask)


if __name__ == "__main__":
    main()
