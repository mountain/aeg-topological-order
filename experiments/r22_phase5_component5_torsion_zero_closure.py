"""Raw-before-canonical z0=0 closure for component 5 on D class 1.

This reuses the accepted exact zero-product search, but injects the second
physical D-amplitude sheet into the shared lower-data provider.  No finite
p^3/q^3 relation or z0 quadratic is used.  The purpose is solely to prove that
z0=0 is impossible before any division by z0 in the five-cell local model.
"""
from __future__ import annotations

import argparse

import r22_phase5_torsion_sheet as ts
import r22_phase5_zero_closure as zc


def audit(cid: int, mask: int):
    with ts.second_sheet_provider():
        out = zc.audit(cid, mask, list(zc.BASE_PATTERNS))
    out = dict(out)
    out["D_amplitude_class"] = 1
    if out["closed"] != out["total"] or out["survivors"]:
        raise AssertionError(("z0=0 second-sheet branch not fully closed", out))
    print("TORSION_SHEET_ZERO", out, flush=True)
    print(
        "RESULT: z0=0 is excluded on the second D sheet before any z0 localization",
        flush=True,
    )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, required=True)
    args = ap.parse_args()
    audit(args.component, args.mask)


if __name__ == "__main__":
    main()
