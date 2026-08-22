"""Complete terminal certificate for component 13 / mask 255 / D class 1.

The finite census is already source-validated.  This verifier rebuilds the
class-1 nonlinear kernel once, then closes all 18 finite strata:

* 2 affine-inconsistent branches;
* 4 p-rank11 branches by the fixed cell (XXXXX)_(5,2);
* 4 q-rank11 branches by the fixed cell (XXXX;Y)_(0,1);
* 8 rank10 branches by the fixed g-cells (0,3),(0,2),(0,1).

The historical modules are reused only for exact RREF/substitution and the
source-certificate algorithms.  Their finite-data module is replaced by the
class-1 census and the kernel is compiled under the second-sheet provider.
"""
from __future__ import annotations

import r22_phase5_component13_mask255_residual_scan as rs
import r22_phase5_component13_mask255_p_rank11_certificate as pc
import r22_phase5_component13_mask255_q_rank11_certificate as qc
import r22_phase5_component13_mask255_rank10_certificate as rc
import r22_phase5_component13_torsion_mask255_finite_census as fc
import r22_phase5_monomial_lift as ml
import r22_phase5_torsion_sheet as ts

AFFINE_CASES = ((0, 0, 1), (0, 0, -1))
P_CASES = ((1, 0, 1), (1, 0, -1), (2, 0, 1), (2, 0, -1))
Q_CASES = ((0, 1, 1), (0, 1, -1), (0, 2, 1), (0, 2, -1))
RANK10_CASES = tuple(
    (a, b, sign)
    for (a, b) in ((1, 1), (2, 1), (1, 2), (2, 2))
    for sign in (1, -1)
)


def main():
    # All downstream residual/certificate modules share this module object.
    rs.fc = fc
    with ts.second_sheet_provider():
        _q, unique = ml.compile_unique(13, 255)

    affine = []
    for case in AFFINE_CASES:
        row = fc.branch_census(unique, *case)
        if row["consistent"]:
            raise AssertionError(("expected affine inconsistency", case, row))
        affine.append(row)

    p_rows = [pc.certify(unique, *case) for case in P_CASES]
    q_rows = [qc.certify(unique, *case) for case in Q_CASES]
    rank10_rows = [rc.certify(unique, *case) for case in RANK10_CASES]

    if len(affine) != 2:
        raise AssertionError(affine)
    if len(p_rows) != 4 or not all(r["closed"] for r in p_rows):
        raise AssertionError(p_rows)
    if len(q_rows) != 4 or not all(r["closed"] for r in q_rows):
        raise AssertionError(q_rows)
    if len(rank10_rows) != 8 or not all(r["closed"] for r in rank10_rows):
        raise AssertionError(rank10_rows)

    summary = {
        "component": 13,
        "mask": 255,
        "D_amplitude_class": 1,
        "affine_inconsistent": 2,
        "p_rank11_closed": 4,
        "q_rank11_closed": 4,
        "rank10_closed": 8,
        "finite_total": 18,
        "terminal_cells": {
            "p": pc.TARGET,
            "q": qc.TARGET,
            "rank10": (rc.P1, rc.P2, rc.P3),
        },
    }
    print("SUMMARY", summary, flush=True)
    print("RESULT: component 13 mask 255 class-1 Phase-5 branch is CLOSED / EXACT", flush=True)


if __name__ == "__main__":
    main()
