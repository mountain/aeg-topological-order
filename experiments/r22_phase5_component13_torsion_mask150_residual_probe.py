"""Representative residual-source probe for component 13 / mask 150 / D class 1.

The finite census is already exact. This probe does not claim closure. It
rebuilds one p-rank11 branch, one q-rank11 branch and one rank10 branch on the
second D sheet, then reports fixed provenance cells that historically carried
short terminal certificates. The class-0 residual engine is reused only as an
algebraic RREF/substitution implementation: its finite-data module is replaced
process-locally by the class-1 census module, and the nonlinear kernel is
compiled under the class-1 lower-data provider.
"""
from __future__ import annotations

import r22_phase5_component13_mask150_residual_scan as rs
import r22_phase5_component13_torsion_mask150_finite_census as fc
import r22_phase5_monomial_lift as ml
import r22_phase5_torsion_sheet as ts

P = (("X", "X", "X", "X", "Y"), (1, 0))
Q = (("X", "X", "X", "X", "X"), (2, 5))
G = tuple((("X", "X", "X", "X", "g"), (0, j)) for j in range(4))
CASES = (
    ("p-rank11", 1, 0, 1),
    ("q-rank11", 0, 1, 1),
    ("rank10", 1, 1, 1),
)


def hits(data, target):
    out = []
    for key, provs in data["provenance"].items():
        if target in provs:
            poly = data["residual"][key]
            out.append({
                "support": tuple(data["free_names"][j] for j in rs.poly_support(poly)),
                "poly": rs.poly_string(poly, data["free_names"]),
                "provenance_aliases": tuple(provs[:4]),
            })
    return out


def main():
    rs.fc = fc
    with ts.second_sheet_provider():
        _q, unique = ml.compile_unique(13, 150)

    for label, a, b, sign in CASES:
        data = rs.build_branch(unique, a, b, sign)
        row = {
            "stratum": label,
            "branch": (a, b, "+" if sign > 0 else "-"),
            "free": data["free"],
            "free_names": data["free_names"],
            "p_cell": hits(data, P),
            "q_cell": hits(data, Q),
            "g_cells": {str(g): hits(data, g) for g in G},
        }
        print(row, flush=True)

    print("RESULT: class-1 component-13/mask-150 representative residual probe completed", flush=True)


if __name__ == "__main__":
    main()
