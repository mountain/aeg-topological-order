"""Exact 18-stratum Phase-5 audit for component 5, D-amplitude class 1.

This gate consumes the five-cell source relations established by
r22_phase5_component5_torsion_local_relations.py and the independent raw
z0=0 closures.  It therefore works only after the legitimate localization
z0 != 0 has been proved for the requested mask.

The relation table below is the direct output of the fresh source-cell replay
on D class 1; no historical class-0 constants are imported.  In every mask the
fifth cell gives

    2*z0^2 + 4*z0 - 1 = 0,

while the p/q cube phases and the two product phases form the exact table
recorded in ``relation``.

The generic component-5 finite-stratum machinery is reused only as an algebraic
engine.  All 18 branches and all target-cell remainders are recomputed from the
class-1 kernel.
"""
from __future__ import annotations

import argparse
from fractions import Fraction

import sympy as sp

import r22_phase5_component5_rest_audit as fa
import r22_phase5_torsion_sheet as ts


def relation(mask: int):
    # Exact source-validated class-1 table.
    table = {
        0: {
            "P3": (Fraction(-1, 4), Fraction(1, 4)),
            "Q3": (Fraction(-1, 4), Fraction(-1, 4)),
            "Z23": fa.NEG_I,
            "Z18": fa.NEG_I,
            "P0": (1 + sp.I) / 2,
            "Q0": (1 - sp.I) / 2,
        },
        105: {
            "P3": (Fraction(-1, 4), Fraction(-1, 4)),
            "Q3": (Fraction(-1, 4), Fraction(-1, 4)),
            "Z23": fa.I,
            "Z18": fa.NEG_I,
            "P0": (1 - sp.I) / 2,
            "Q0": (1 - sp.I) / 2,
        },
        150: {
            "P3": (Fraction(-1, 4), Fraction(1, 4)),
            "Q3": (Fraction(-1, 4), Fraction(1, 4)),
            "Z23": fa.NEG_I,
            "Z18": fa.I,
            "P0": (1 + sp.I) / 2,
            "Q0": (1 + sp.I) / 2,
        },
        255: {
            "P3": (Fraction(-1, 4), Fraction(-1, 4)),
            "Q3": (Fraction(-1, 4), Fraction(1, 4)),
            "Z23": fa.I,
            "Z18": fa.I,
            "P0": (1 - sp.I) / 2,
            "Q0": (1 + sp.I) / 2,
        },
    }
    if mask not in table:
        raise ValueError(("mask has no source-validated class-1 relation table", mask))
    return table[mask]


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
