"""One-cell exact certificates for the four p-side rank-11 finite strata of
component 13 / chirality mask 0.

After the exact finite relations and affine RREF, the branches

    (a,b)=(1,0),(2,0),  z5=+-sqrt(2)/2

have forced z12=z13=0.  This script rebuilds each branch independently and
checks the single final-pentagon provenance

    (X,X,X,X;Y)_(1,0)

in the full residual quotient.  The branch is closed only if that entry is a
nonzero exact scalar times z0.  The local-relation gate has already proved
z0 != 0, so such an equation is an immediate contradiction.
"""
from __future__ import annotations

import r22_phase5_component13_mask0_residual_scan as rs
import r22_phase5_monomial_lift as ml
import r22_phase5_survivor_sparse as ss

TARGET = (("X", "X", "X", "X", "Y"), (1, 0))
CASES = ((1, 0, 1), (1, 0, -1), (2, 0, 1), (2, 0, -1))


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
    expected = (1, 0, 0, 0, 0, 0, 0)  # z0
    if mon != expected or ss.kiszero(coeff):
        raise AssertionError((a, b, sign, "target is not nonzero scalar*z0", mon, ss.kstr(coeff)))

    row = {
        "a": a,
        "b": b,
        "z5_sign": "+" if sign > 0 else "-",
        "provenance": TARGET,
        "residual": rs.poly_string(poly, data["free_names"]),
        "contradiction": "nonzero_scalar*z0=0 with proved z0!=0",
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
    print("RESULT: all four component-13/mask-0 p-side rank-11 strata are excluded by one local cell", flush=True)


if __name__ == "__main__":
    main()
