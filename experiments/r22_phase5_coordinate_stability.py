"""Audit whether Phase-5 F-component coordinates are reproducible across hash seeds.

The current Phase-5 compiler names generic F-linear components by sorting the
weighted-union-find root integers.  A union-find root is an implementation
representative, not a mathematical invariant.  This probe runs fresh Python
processes with different PYTHONHASHSEED values and compares:

1. the partition of the 1312 F entries assigned to z0,z1,...;
2. the canonical polynomial at the fixed final-pentagon cell
   (X,X,X,X;1)_(0,0).

Any mismatch proves that hard-coded z_j coordinates are not reproducible and
must be replaced by canonical component anchors before accepting Phase-5
certificates that refer to named z_j variables.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys

import r22_epsminus_f_parametric as fp
import r22_epsminus_final_kernel as fk

TARGET_BLOCK = ("X", "X", "X", "X", "1")
TARGET_CELL = (0, 0)


def digest(x):
    return hashlib.sha256(repr(x).encode("utf-8")).hexdigest()


def root_partition(cid, mask):
    scalar, ddata, params, emats, _droot = fp.parametric_lower_data(cid, mask)
    uf, _support, _degrees, _n_eq = fp.build_f_system(scalar, ddata, params, emats)
    profile, _kvalues = fp.root_condition_profile(uf)
    active = sorted(fp.active_roots(profile))
    active_set = set(active)
    members = {r: [] for r in active}
    for i in range(1312):
        r, _w = uf.find(i)
        if r in active_set:
            members[r].append(i)
    return tuple(tuple(members[r]) for r in active)


def target_key(cid, mask):
    quotient = fk.parametric_quotient_data(cid, mask)
    for p in fk.FINAL_BLOCKS:
        if p[:5] != TARGET_BLOCK:
            continue
        labels = dict(zip("abcd", p[:4]))
        long_side, short_side = fk.pentagon_sparse(labels, p[4], quotient)
        i, j = TARGET_CELL
        diff = dict(long_side[i].get(j, {}))
        fk.poly_add_scaled(diff, short_side[i].get(j, {}), (-1, 0))
        key, floor = fk.canonical_poly(diff)
        return key, floor
    raise RuntimeError(("target block not found", TARGET_BLOCK))


def emit(cid, mask):
    partition = root_partition(cid, mask)
    key, floor = target_key(cid, mask)
    out = {
        "component": cid,
        "mask": mask,
        "partition_digest": digest(partition),
        "partition_prefix": [list(x[:8]) for x in partition[:8]],
        "target_digest": digest(key),
        "target_floor": floor,
        "target_key": repr(key),
    }
    print(json.dumps(out, sort_keys=True), flush=True)


def audit(cid, masks, seeds):
    rows = []
    script = os.path.abspath(__file__)
    for mask in masks:
        by_seed = []
        for seed in seeds:
            env = dict(os.environ)
            env["PYTHONHASHSEED"] = str(seed)
            proc = subprocess.run(
                [sys.executable, script, "--emit", "--component", str(cid), "--mask", str(mask)],
                check=True,
                text=True,
                capture_output=True,
                env=env,
            )
            line = proc.stdout.strip().splitlines()[-1]
            row = json.loads(line)
            row["seed"] = seed
            by_seed.append(row)
            print(row, flush=True)
        pset = {r["partition_digest"] for r in by_seed}
        tset = {r["target_digest"] for r in by_seed}
        summary = {
            "component": cid,
            "mask": mask,
            "seeds": seeds,
            "partition_variants": len(pset),
            "target_variants": len(tset),
            "stable": len(pset) == 1 and len(tset) == 1,
        }
        rows.append(summary)
        print("MASK", summary, flush=True)
    global_summary = {
        "component": cid,
        "masks": masks,
        "all_stable": all(r["stable"] for r in rows),
        "unstable_masks": [r["mask"] for r in rows if not r["stable"]],
    }
    print("SUMMARY", global_summary, flush=True)
    if global_summary["all_stable"]:
        print("RESULT: current z_j coordinates are stable across tested hash seeds", flush=True)
    else:
        print("RESULT: current z_j coordinates are NOT reproducible across tested hash seeds", flush=True)
    return global_summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, action="append")
    ap.add_argument("--seed", type=int, action="append")
    ap.add_argument("--emit", action="store_true")
    args = ap.parse_args()
    masks = args.mask or [0, 105, 150, 255]
    if args.emit:
        if len(masks) != 1:
            raise ValueError("--emit requires exactly one --mask")
        emit(args.component, masks[0])
        return
    audit(args.component, masks, args.seed or [1, 2, 17])


if __name__ == "__main__":
    main()
