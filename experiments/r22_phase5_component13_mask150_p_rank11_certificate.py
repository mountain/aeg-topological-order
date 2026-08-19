"""One-cell exact certificates for the four p-side rank-11 finite strata of
component 13 / chirality mask 150.

After the independently verified mask-150 local relations and finite affine
census, the branches

    (a,b)=(1,0),(2,0),  z6=+-sqrt(2)/2

have forced z2=z8=0 while required F determinants remain generically nonzero.
This gate rebuilds each branch independently and checks the fixed final-pentagon
provenance

    (X,X,X,X;Y)_(1,0)

in the complete affine residual quotient.  A branch is closed here only if that
entry is an exact nonzero constant.  No alternative provenance is searched and
no Groebner/global nonlinear solve is used.
"""
from __future__ import annotations

import r22_phase5_component13_mask150_residual_scan as rs
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss

TARGET = (("X", "X", "X", "X", "Y"), (1, 0))
CASES = ((1, 0, 1), (1, 0, -1), (2, 0, 1), (2, 0, -1))
EXPECTED_FREE = (0, 1, 10, 11, 14, 15, 20)


def certify(unique, a, b, sign):
    data = rs.build_branch(unique, a, b, sign)
    if data["free"] != EXPECTED_FREE:
        raise AssertionError((a, b, sign, "unexpected free variables", data["free"]))

    hits = []
    for key, provs in data["provenance"].items():
        if TARGET in provs:
            hits.append(data["residual"][key])
    if len(hits) != 1:
        raise AssertionError((a, b, sign, "target residual multiplicity", len(hits)))

    poly = hits[0]
    if len(poly) != 1:
        raise AssertionError((a, b, sign, "target is not singleton", rs.poly_string(poly, data["free_names"])))
    mon, coeff = next(iter(poly.items()))
    if mon != (0,) * len(EXPECTED_FREE) or ss.kiszero(coeff):
        raise AssertionError((a, b, sign, "target is not nonzero constant", mon, ss.kstr(coeff)))

    row = {
        "a": a,
        "b": b,
        "z6_sign": "+" if sign > 0 else "-",
        "provenance": TARGET,
        "residual": rs.poly_string(poly, data["free_names"]),
        "contradiction": "nonzero_constant=0",
        "closed": True,
    }
    print(row, flush=True)
    return row


def main():
    _quotient, unique = ml.compile_unique(13, 150)
    rows = [certify(unique, *case) for case in CASES]
    if len(rows) != 4 or not all(r["closed"] for r in rows):
        raise AssertionError(rows)
    print("SUMMARY", {"closed": 4, "total": 4, "cell": TARGET}, flush=True)
    print("RESULT: all four component-13/mask-150 p-side rank-11 strata are excluded by one constant local cell", flush=True)


if __name__ == "__main__":
    main()
