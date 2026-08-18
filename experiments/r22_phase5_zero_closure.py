"""Exact singleton/product propagation for Phase-5 z0=0 branches.

The four shortest final-pentagon binomials imply, under z0=0 and p*q!=0,

    z2*z3 = 0,
    z1*z8 = 0,

hence four initial zero patterns A/ZB/ZC/D.  Earlier probes inspected only one
hard-coded derived zero.  That is not chirality-uniform: masks 150 and 255 force
different next coordinates on their ZC branches.

This script instead derives every further zero from the specialized exact
219-polynomial kernel itself.  At each node it:

1. checks whether the accumulated zero pattern kills a required F determinant;
2. specializes every final-pentagon polynomial by the zero pattern;
3. closes on a surviving torus-only monomial (p,q are proved nonzero);
4. propagates any singleton monomial supported on one F variable, z_j^k=0;
5. for a singleton product monomial, branches exhaustively over its factors.

The search uses only exact zero-product logic and determinant monomial support.
It performs no Groebner computation, numerical solving, or division by an
unknown F variable.
"""
from __future__ import annotations

import argparse
from collections import Counter

import r22_epsminus_f_parametric as fp
import r22_phase5_monomial_lift as ml


BASE_PATTERNS = {
    "A": (0, 2, 1),
    "ZB": (0, 2, 8),
    "ZC": (0, 3, 1),
    "D": (0, 3, 8),
}


def zname(zi):
    return f"z{zi}"


def determinant_data(cid, mask):
    scalar, ddata, params, emats, _droot = fp.parametric_lower_data(cid, mask)
    uf, _support, _degrees, _n_eq = fp.build_f_system(scalar, ddata, params, emats)
    profile, _kvalues = fp.root_condition_profile(uf)
    active = sorted(fp.active_roots(profile))
    active_set = set(active)
    determinants = {}
    for key, _dim in fp.F_BLOCKS:
        desc = fp.block_descriptor(uf, profile, key, active_set)
        det = fp.determinant_generic(desc)
        if not det:
            raise RuntimeError(("generic required determinant vanished", cid, mask, key))
        determinants[key] = det
    return active, determinants


def killed_determinants(active, determinants, zeros):
    zero_roots = {active[zi] for zi in zeros}
    killed = []
    survivor_counts = {}
    for key, det in determinants.items():
        n = sum(1 for mon, _rexp in det if not any(r in zero_roots for r in mon))
        survivor_counts[key] = n
        if n == 0:
            killed.append(key)
    return killed, survivor_counts


def specialized_singletons(unique, zeros):
    """Return exact monomial equations left after setting the selected z's to 0."""
    rows = []
    for key, prov in unique.items():
        surviving = []
        for mon, gc in key:
            if any(mon[2 + zi] for zi in zeros):
                continue
            surviving.append((mon, gc))
        if len(surviving) != 1:
            continue
        mon, _gc = surviving[0]
        zsupport = tuple(zi for zi, e in enumerate(mon[2:]) if e)
        rows.append({
            "provenance": prov,
            "z_support": zsupport,
            "z_powers": {zname(zi): mon[2 + zi] for zi in zsupport},
            "p_power": mon[0],
            "q_power": mon[1],
        })
    return rows


def node_key(zeros):
    return tuple(sorted(zeros))


def close_search(unique, active, determinants, initial_zeros, max_nodes=2048):
    memo = {}
    stats = Counter()
    nodes = 0

    def visit(zeros):
        nonlocal nodes
        zeros = frozenset(zeros)
        key = node_key(zeros)
        if key in memo:
            return memo[key]
        nodes += 1
        if nodes > max_nodes:
            raise RuntimeError(("zero-branch search exceeded node budget", max_nodes))
        stats["nodes"] += 1

        killed, survivor_counts = killed_determinants(active, determinants, zeros)
        if killed:
            out = {
                "closed": True,
                "reason": "F_invertibility",
                "zero_z": key,
                "killed_blocks": killed,
                "min_surviving_det_terms": min(survivor_counts.values()),
            }
            stats["closed_F"] += 1
            memo[key] = out
            return out

        singleton_rows = specialized_singletons(unique, zeros)
        constants = [r for r in singleton_rows if not r["z_support"]]
        if constants:
            out = {
                "closed": True,
                "reason": "torus_monomial_contradiction",
                "zero_z": key,
                "certificate": constants[0],
                "min_surviving_det_terms": min(survivor_counts.values()),
            }
            stats["closed_torus"] += 1
            memo[key] = out
            return out

        forced_by_var = {}
        for row in singleton_rows:
            support = row["z_support"]
            if len(support) == 1:
                forced_by_var.setdefault(support[0], row)
        if forced_by_var:
            newvars = tuple(sorted(forced_by_var))
            child = visit(zeros | set(newvars))
            out = {
                "closed": child["closed"],
                "reason": "forced_singletons_then_" + child["reason"],
                "zero_z": key,
                "forced_zero": [
                    {"variable": zname(zi), "provenance": forced_by_var[zi]["provenance"], "power": forced_by_var[zi]["z_powers"][zname(zi)]}
                    for zi in newvars
                ],
                "child": child,
            }
            stats["forced_steps"] += 1
            memo[key] = out
            return out

        products = [r for r in singleton_rows if len(r["z_support"]) >= 2]
        if not products:
            out = {
                "closed": False,
                "reason": "stable_no_singleton_product_constraint",
                "zero_z": key,
                "min_surviving_det_terms": min(survivor_counts.values()),
            }
            stats["open_stable"] += 1
            memo[key] = out
            return out

        # Branch on the shortest exact product equation.  Product=0 is the union
        # of the coordinate-zero branches, so this branching is exhaustive.
        products.sort(key=lambda r: (len(r["z_support"]), r["z_support"], str(r["provenance"])))
        chosen = products[0]
        children = []
        for zi in chosen["z_support"]:
            child = visit(zeros | {zi})
            children.append({"set_zero": zname(zi), "result": child})
        closed = all(c["result"]["closed"] for c in children)
        out = {
            "closed": closed,
            "reason": "exhaustive_product_branch" if closed else "product_branch_has_survivor",
            "zero_z": key,
            "product_constraint": chosen,
            "children": children,
        }
        stats["product_branches"] += 1
        memo[key] = out
        return out

    result = visit(set(initial_zeros))
    return result, dict(stats)


def compact_chain(result, depth=0, limit=12):
    """Small human-readable certificate prefix without dumping the full tree."""
    if depth >= limit:
        return {"reason": "depth_limit"}
    out = {"zero_z": result.get("zero_z"), "closed": result["closed"], "reason": result["reason"]}
    if "killed_blocks" in result:
        out["killed_blocks"] = result["killed_blocks"]
    if "certificate" in result:
        out["certificate"] = result["certificate"]
    if "forced_zero" in result:
        out["forced_zero"] = result["forced_zero"]
        out["child"] = compact_chain(result["child"], depth + 1, limit)
    if "product_constraint" in result:
        out["product_constraint"] = result["product_constraint"]
        out["children"] = [
            {"set_zero": c["set_zero"], "result": compact_chain(c["result"], depth + 1, limit)}
            for c in result["children"]
        ]
    return out


def audit(cid, mask, branches):
    quotient, unique = ml.compile_unique(cid, mask)
    if quotient["F_components"] != 21:
        raise RuntimeError(("this closure probe currently expects 21 F components", cid, mask, quotient["F_components"]))
    active, determinants = determinant_data(cid, mask)
    if len(active) != quotient["F_components"]:
        raise RuntimeError(("active-coordinate mismatch", len(active), quotient["F_components"]))

    rows = []
    for name in branches:
        result, stats = close_search(unique, active, determinants, BASE_PATTERNS[name])
        row = {
            "component": cid,
            "mask": mask,
            "branch": name,
            "initial_zero_z": BASE_PATTERNS[name],
            "closed": result["closed"],
            "stats": stats,
            "certificate_tree": compact_chain(result),
        }
        rows.append(row)
        print(row, flush=True)

    summary = {
        "component": cid,
        "mask": mask,
        "branches": branches,
        "closed": sum(bool(r["closed"]) for r in rows),
        "total": len(rows),
        "survivors": [r["branch"] for r in rows if not r["closed"]],
    }
    print("SUMMARY", summary, flush=True)
    if summary["closed"] == summary["total"]:
        print("RESULT: z0=0 is completely excluded by exact zero-product propagation for mask", mask, flush=True)
    else:
        print("RESULT: unresolved z0=0 branches remain for mask", mask, summary["survivors"], flush=True)
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=5)
    ap.add_argument("--mask", type=int, required=True)
    ap.add_argument("--branch", choices=tuple(BASE_PATTERNS), action="append")
    args = ap.parse_args()
    branches = args.branch or list(BASE_PATTERNS)
    audit(args.component, args.mask, branches)


if __name__ == "__main__":
    main()
