"""Exact chirality-conjugation audit for component-5 Phase-5 quotients.

Test the known Phase-2 survivor pairings

    0   <-> 255
    105 <-> 150

without assuming that the pairing survives the later quotient construction.
For each pair, rebuild the complete Phase-4 parametric quotient and compare every
non-unit A--F associator entry under coefficientwise complex conjugation while
keeping p,q and the ordered active F coordinates z_j as formal coordinates.
Unit associators are omitted because the final compiler inserts their canonical
identity maps directly, independently of chirality.

If every lower associator entry is conjugate in this common coordinate system,
then every required F block is entrywise conjugate, hence its determinant and
invertibility locus are conjugate as well.  Since the Phase-5 pentagon compiler
uses only addition and multiplication of those entries, the complete final
kernel is then conjugate automatically.  We nevertheless compile the final 219
polynomial sets as an independent exact verification.

If the direct coordinate comparison fails, this probe reports the first lower
and final-kernel mismatches rather than declaring an equivalence.
"""
from __future__ import annotations

import argparse
from collections import Counter

import r22_epsminus_final_kernel as fk
import r22_phase5_monomial_lift as ml
from r22_scale_audit import ONE, f_blocks, f_class


def gconj(c):
    return c[0], -c[1]


def pconj(poly):
    return {m: gconj(c) for m, c in poly.items()}


def key_conj(key):
    out = []
    for mon, gc in key:
        (ar, ad), (br, bd) = gc
        out.append((mon, ((ar, ad), (-br, bd))))
    return tuple(out)


def lower_entry_audit(cid, left, right):
    ql = fk.parametric_quotient_data(cid, left)
    qr = fk.parametric_quotient_data(cid, right)
    meta = {
        "left_variables": ql["variables"],
        "right_variables": qr["variables"],
        "left_F_components": ql["F_components"],
        "right_F_components": qr["F_components"],
        "left_D_root_group": ql["droot"],
        "right_D_root_group": qr["droot"],
    }
    if ql["variables"] != qr["variables"]:
        return meta, False, [{"type": "variable-list", "left": ql["variables"], "right": qr["variables"]}]

    mismatches = []
    class_counts = Counter()
    total = 0
    f_total = 0
    f_mismatch = 0
    skipped_unit = 0
    for a, b, c, d, dim in f_blocks():
        if ONE in (a, b, c):
            skipped_unit += dim * dim
            continue
        key = (a, b, c, d)
        cl = f_class(key)
        if cl not in "ABCDEF":
            continue
        for row in range(dim):
            for col in range(dim):
                lhs = ql["lower_entry"](key, row, col)
                rhs = qr["lower_entry"](key, row, col)
                total += 1
                class_counts[cl] += 1
                if cl == "F":
                    f_total += 1
                if pconj(lhs) != rhs:
                    if cl == "F":
                        f_mismatch += 1
                    if len(mismatches) < 24:
                        mismatches.append({
                            "type": "lower-entry",
                            "class": cl,
                            "key": key,
                            "row": row,
                            "col": col,
                            "conjugate_left": pconj(lhs),
                            "right": rhs,
                        })
    meta.update({
        "lower_entries_checked": total,
        "unit_entries_skipped_as_canonical": skipped_unit,
        "class_counts": dict(class_counts),
        "required_F_entries_checked": f_total,
        "required_F_entry_mismatches": f_mismatch,
        "required_F_blocks_entrywise_conjugate": f_mismatch == 0,
    })
    return meta, not mismatches, mismatches


def kernel_audit(cid, left, right):
    _ql, ul = ml.compile_unique(cid, left)
    _qr, ur = ml.compile_unique(cid, right)
    sl = {key_conj(k) for k in ul}
    sr = set(ur)
    only_left = sl - sr
    only_right = sr - sl
    return {
        "left_unique": len(ul),
        "right_unique": len(ur),
        "conjugate_sets_equal": not only_left and not only_right,
        "only_conjugate_left": len(only_left),
        "only_right": len(only_right),
        "left_examples": [str(x) for x in list(only_left)[:4]],
        "right_examples": [str(x) for x in list(only_right)[:4]],
    }


def audit_pair(cid, left, right):
    lower_meta, lower_ok, lower_mismatches = lower_entry_audit(cid, left, right)
    kernel = kernel_audit(cid, left, right)
    verified = lower_ok and lower_meta["required_F_blocks_entrywise_conjugate"] and kernel["conjugate_sets_equal"]
    out = {
        "component": cid,
        "pair": (left, right),
        "coordinate_map": "identity on p,q,z_j; coefficientwise complex conjugation",
        "lower": lower_meta,
        "lower_conjugate": lower_ok,
        "lower_mismatch_examples": lower_mismatches,
        "kernel": kernel,
        "verified_full_phase5_conjugation": verified,
    }
    print(out, flush=True)
    if verified:
        print(
            "RESULT:", left, "<->", right,
            "is an exact full Phase-5 conjugation preserving required F invertibility",
            flush=True,
        )
    else:
        print(
            "RESULT:", left, "<->", right,
            "is NOT verified by the direct coordinatewise conjugation; derive a coordinate map or replay fresh",
            flush=True,
        )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    args = ap.parse_args()
    rows = [audit_pair(args.component, 0, 255), audit_pair(args.component, 105, 150)]
    print(
        "SUMMARY",
        {
            "verified": sum(bool(r["verified_full_phase5_conjugation"]) for r in rows),
            "total": len(rows),
        },
        flush=True,
    )


if __name__ == "__main__":
    main()
