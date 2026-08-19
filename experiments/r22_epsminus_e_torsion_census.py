"""Complete exact Phase-3 census for the second physical D-amplitude sheet."""
from __future__ import annotations

from collections import Counter, defaultdict

import r22_epsminus_d_amplitude as da
import r22_epsminus_e_torsion_probe as probe


def fingerprint(row):
    return (
        row["E_equations"],
        tuple(sorted(row["E_support"].items())),
        row["E_rank"],
        row["E_nullity"],
        tuple(sorted((str(k), v) for k, v in row["E_determinant_monomial_profile"].items())),
        tuple(sorted(row["E_determinant_term_counts"].items())),
    )


def main():
    rows = []
    variants = defaultdict(list)
    statuses = Counter()

    for cid in da.FRONTIER_COMPONENTS:
        for mask in da.SURVIVOR_MASKS:
            row = probe.solve(cid, mask, 1)
            rows.append(row)
            statuses[row["status"]] += 1
            variants[fingerprint(row)].append((cid, mask))

    if len(rows) != 16:
        raise AssertionError(("incomplete second-sheet E census", len(rows)))

    print("SUMMARY", {
        "D_amplitude_class": 1,
        "branches": len(rows),
        "statuses": dict(statuses),
        "fingerprint_variants": len(variants),
        "variant_branch_counts": sorted(len(v) for v in variants.values()),
    }, flush=True)
    for i, (fp, branches) in enumerate(variants.items()):
        print("VARIANT", i, {"fingerprint": fp, "branches": branches}, flush=True)

    if statuses == Counter({"E_PASS": 16}):
        print(
            "RESULT: all 16 second-sheet deep branches retain an exact invertible two-parameter E locus",
            flush=True,
        )
    else:
        print(
            "RESULT: the second D sheet splits at the E layer; inspect the exact status census above",
            flush=True,
        )


if __name__ == "__main__":
    main()
