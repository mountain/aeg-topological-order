"""Component-level exact Phase-4 census for D-amplitude class 1.

Run one deep scalar component at a time to preserve the 10-minute research-job
guardrail.  Each mask is rebuilt independently through D class 1, the complete
E torus, F-linear coherence, and exact required-F determinant strata.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict

import r22_epsminus_d_amplitude as da
import r22_epsminus_f_torsion_probe as probe


def fingerprint(row):
    return (
        row["F_equations"],
        tuple(sorted(row["F_support"].items())),
        tuple(sorted(row["F_component_condition_profile"].items())),
        row["E_ratio_modulus"],
        row["generic_active_F_components"],
        tuple(row["generic_bad_blocks"]),
        tuple(sorted(row["finite_strata_profile"].items())),
        tuple(row["passing_E_ratio_strata"]),
        tuple(sorted(row["generic_required_det_term_counts"].values())),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, required=True)
    args = ap.parse_args()
    cid = args.component
    if cid not in da.FRONTIER_COMPONENTS:
        raise SystemExit(f"component {cid} not in deep frontier {da.FRONTIER_COMPONENTS}")

    rows = []
    variants = defaultdict(list)
    statuses = Counter()
    for mask in da.SURVIVOR_MASKS:
        row = probe.analyze(cid, mask)
        rows.append(row)
        statuses[row["status"]] += 1
        variants[fingerprint(row)].append(mask)

    if len(rows) != 4:
        raise AssertionError(("incomplete component Phase-4 census", cid, len(rows)))

    print("SUMMARY", {
        "component": cid,
        "D_amplitude_class": 1,
        "masks": list(da.SURVIVOR_MASKS),
        "statuses": dict(statuses),
        "fingerprint_variants": len(variants),
        "variant_mask_counts": sorted(len(v) for v in variants.values()),
    }, flush=True)
    for i, (fp, masks) in enumerate(variants.items()):
        print("VARIANT", i, {"fingerprint": fp, "masks": masks}, flush=True)

    if statuses == Counter({"F_PASS": 4}):
        print(
            f"RESULT: component {cid} second D sheet passes parametric Phase 4 on all four chirality masks",
            flush=True,
        )
    else:
        print(
            f"RESULT: component {cid} second D sheet splits or closes at Phase 4; inspect census",
            flush=True,
        )


if __name__ == "__main__":
    main()
