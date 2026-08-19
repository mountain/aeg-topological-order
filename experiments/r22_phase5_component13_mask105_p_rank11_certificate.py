"""One-cell exact certificates for the four p-side rank-11 finite strata of
component 13 / chirality mask 105.

Branches (a,b)=(1,0),(2,0), z0=+-sqrt(2)/2 have forced z7=z8=0.  Rebuild each
branch independently and check the fixed final-pentagon provenance

    (X,X,X,X;Y)_(1,0).

The branch is closed only if that residual entry is a nonzero exact scalar
times z3.  The mask-105 local-relation gate has already proved z3 != 0.
"""
from __future__ import annotations

import r22_phase5_component13_mask105_residual_scan as rs
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss

TARGET = (("X", "X", "X", "X", "Y"), (1, 0))
CASES = ((1, 0, 1), (1, 0, -1), (2, 0, 1), (2, 0, -1))


def certify(unique, a, b, sign):
    data = rs.build_branch(unique, a, b, sign)
    if data["free"] != (3, 4, 5, 6, 16, 19, 20):
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
    expected = (1, 0, 0, 0, 0, 0, 0)  # z3
    if mon != expected or ss.kiszero(coeff):
        raise AssertionError((a, b, sign, "target is not nonzero scalar*z3", mon, ss.kstr(coeff)))

    row = {
        "a": a,
        "b": b,
        "z0_sign": "+" if sign > 0 else "-",
        "provenance": TARGET,
        "residual": rs.poly_string(poly, data["free_names"]),
        "contradiction": "nonzero_scalar*z3=0 with proved z3!=0",
        "closed": True,
    }
    print(row, flush=True)
    return row


def main():
    _quotient, unique = ml.compile_unique(13, 105)
    rows = [certify(unique, *case) for case in CASES]
    if len(rows) != 4 or not all(r["closed"] for r in rows):
        raise AssertionError(rows)
    print("SUMMARY", {"closed": 4, "total": 4, "cell": TARGET}, flush=True)
    print("RESULT: all four component-13/mask-105 p-side rank-11 strata are excluded by one local cell", flush=True)


if __name__ == "__main__":
    main()
