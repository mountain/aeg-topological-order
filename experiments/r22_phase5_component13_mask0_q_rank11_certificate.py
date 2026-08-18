"""One-cell exact certificates for the four q-side rank-11 finite strata of
component 13 / chirality mask 0.

The finite census leaves

    (a,b)=(0,1),(0,2),  z5=+-sqrt(2)/2

with affine rank 11 and forced z7=z8=0.  This script rebuilds each branch
independently and checks the fixed final-pentagon provenance

    (X,X,X,X;X)_(5,2).

A branch is closed only if that residual is a nonzero exact scalar times z11.
The local-relation gate has already proved z11 != 0, so the resulting equation
is an immediate contradiction.
"""
from __future__ import annotations

import r22_phase5_component13_mask0_residual_scan as rs
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss

TARGET = (("X", "X", "X", "X", "X"), (5, 2))
CASES = ((0, 1, 1), (0, 1, -1), (0, 2, 1), (0, 2, -1))


def certify(unique, a, b, sign):
    data = rs.build_branch(unique, a, b, sign)
    if data["free"] != (0, 9, 10, 11, 18, 19, 20):
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
    expected = (0, 0, 0, 1, 0, 0, 0)  # z11
    if mon != expected or ss.kiszero(coeff):
        raise AssertionError((a, b, sign, "target is not nonzero scalar*z11", mon, ss.kstr(coeff)))

    row = {
        "a": a,
        "b": b,
        "z5_sign": "+" if sign > 0 else "-",
        "provenance": TARGET,
        "residual": rs.poly_string(poly, data["free_names"]),
        "contradiction": "nonzero_scalar*z11=0 with proved z11!=0",
        "closed": True,
    }
    print(row, flush=True)
    return row


def main():
    _quotient, unique = ml.compile_unique(13, 0)
    rows = [certify(unique, *case) for case in CASES]
    if len(rows) != 4 or not all(r["closed"] for r in rows):
        raise AssertionError(rows)
    print("SUMMARY", {"closed": 4, "total": 4, "cell": TARGET}, flush=True)
    print("RESULT: all four component-13/mask-0 q-side rank-11 strata are excluded by one local cell", flush=True)


if __name__ == "__main__":
    main()
