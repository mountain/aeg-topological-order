"""Representative residual-source probe for component 13 / mask 0 / D class 1.

The fresh finite census has established the exact 2+4+4+8 affine split.  This
probe recompiles the second-sheet kernel once and inspects fixed historical
provenance positions on one representative of each surviving stratum.  It is a
reconnaissance gate only: no historical polynomial or certificate is assumed.
"""
from __future__ import annotations

import r22_phase5_component13_mask0_residual_scan as rs
import r22_phase5_component13_torsion_mask0_finite_census as fc
import r22_phase5_monomial_lift as ml
import r22_phase5_torsion_sheet as ts

P_TARGET = (("X", "X", "X", "X", "Y"), (1, 0))
Q_TARGET = (("X", "X", "X", "X", "X"), (5, 2))
G0 = (("X", "X", "X", "X", "g"), (0, 0))
G1 = (("X", "X", "X", "X", "g"), (0, 1))
G2 = (("X", "X", "X", "X", "g"), (0, 2))
G3 = (("X", "X", "X", "X", "g"), (0, 3))
TARGETS = (P_TARGET, Q_TARGET, G0, G1, G2, G3)
CASES = (
    ("p-rank11", 1, 0, 1),
    ("q-rank11", 0, 1, 1),
    ("rank10", 1, 1, 1),
)


def target(data, prov):
    hits = []
    for key, provs in data["provenance"].items():
        if prov in provs:
            hits.append(data["residual"][key])
    if len(hits) != 1:
        return None
    return hits[0]


def main():
    # Reuse the accepted residual-substitution engine, but replace its finite
    # chart by the class-1 chart proved in the preceding gate.
    rs.fc = fc
    with ts.second_sheet_provider():
        _quotient, unique = ml.compile_unique(13, 0)

    for label, a, b, sign in CASES:
        data = rs.build_branch(unique, a, b, sign)
        rows = []
        for prov in TARGETS:
            poly = target(data, prov)
            rows.append({
                "provenance": prov,
                "present": poly is not None,
                "support": () if poly is None else tuple(data["free_names"][j] for j in rs.poly_support(poly)),
                "poly": None if poly is None else rs.poly_string(poly, data["free_names"]),
            })

        shortest = sorted(
            data["residual"].items(),
            key=lambda kv: (len(kv[1]), len(rs.poly_support(kv[1])), rs.poly_degree(kv[1]), str(kv[0])),
        )[:12]
        short_rows = [{
            "terms": len(poly),
            "degree": rs.poly_degree(poly),
            "support": tuple(data["free_names"][j] for j in rs.poly_support(poly)),
            "poly": rs.poly_string(poly, data["free_names"]),
            "provenance": tuple(data["provenance"][key][:3]),
        } for key, poly in shortest]

        print({
            "stratum": label,
            "branch": (a, b, "+" if sign > 0 else "-"),
            "free": data["free"],
            "free_names": data["free_names"],
            "targets": rows,
            "shortest": short_rows,
        }, flush=True)

    print("RESULT: class-1 component-13/mask-0 representative residual source probe completed", flush=True)


if __name__ == "__main__":
    main()
