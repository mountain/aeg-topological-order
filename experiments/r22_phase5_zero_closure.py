"""Exact raw-polynomial zero-product closure for Phase-5 z0=0 branches.

The four shortest final-pentagon binomials imply, under z0=0 and p*q!=0,

    z2*z3 = 0,
    z1*z8 = 0,

hence four initial zero patterns A/ZB/ZC/D.

IMPORTANT ORDER OF OPERATIONS
-----------------------------
Zero specialization is performed on the raw long-side minus short-side
pentagon polynomials *before* Laurent canonicalization and global deduplication.
This is exactly the order used by r22_phase5_zero_branch_probe.py.  It matters:
a previously attempted propagator specialized one representative from the
already deduplicated 219-polynomial kernel and produced spurious constant
constraints on mask 150 ZC.  Those results are intentionally superseded here.

At each node this script:

1. checks whether accumulated zeros kill a required F determinant;
2. specializes the current raw pentagon polynomials by newly forced zeros;
3. canonicalizes only after that specialization;
4. closes on a torus-only monomial (p,q are proved nonzero);
5. propagates any singleton monomial z_j^k=0;
6. if a singleton product monomial remains, branches exhaustively over its
   coordinate factors.

No Groebner basis, numerical solve, or division by an unknown F variable is
used.  Product branching is exact over a field because a monomial vanishes iff
at least one of its coordinate factors vanishes.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction

import r22_epsminus_f_parametric as fp
import r22_epsminus_final_kernel as fk


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


def compile_raw_final(cid, mask):
    """Compile all nonzero raw final-pentagon differences without canonicalizing."""
    quotient = fk.parametric_quotient_data(cid, mask)
    rows = []
    scalar_positions = 0
    for p in fk.FINAL_BLOCKS:
        labels = dict(zip("abcd", p[:4]))
        long_side, short_side = fk.pentagon_sparse(labels, p[4], quotient)
        dim = len(long_side)
        scalar_positions += dim * dim
        for i in range(dim):
            cols = set(long_side[i]) | set(short_side[i])
            for j in cols:
                diff = dict(long_side[i].get(j, {}))
                fk.poly_add_scaled(
                    diff,
                    short_side[i].get(j, {}),
                    (Fraction(-1), Fraction(0)),
                )
                if diff:
                    rows.append((diff, (p[:5], (i, j))))
    return quotient, rows, scalar_positions


def specialize_rows(rows, new_zero_z):
    """Specialize raw rows by additional z coordinates; never canonicalize here."""
    if not new_zero_z:
        return rows
    zero_indices = {2 + zi for zi in new_zero_z}
    out = []
    for poly, prov in rows:
        spec = {
            mon: coeff
            for mon, coeff in poly.items()
            if not any(mon[k] for k in zero_indices)
        }
        if spec:
            out.append((spec, prov))
    return out


def canonical_constraints(rows):
    """Canonicalize the already-specialized raw rows, matching zero_branch_probe."""
    unique = {}
    for poly, prov in rows:
        key, _floor = fk.canonical_poly(poly)
        if key is not None:
            unique.setdefault(key, prov)

    singletons = []
    term_profile = Counter()
    for key, prov in unique.items():
        term_profile[len(key)] += 1
        if len(key) != 1:
            continue
        mon, _gc = key[0]
        zsupport = tuple(zi for zi, e in enumerate(mon[2:]) if e)
        singletons.append({
            "provenance": prov,
            "z_support": zsupport,
            "z_powers": {zname(zi): mon[2 + zi] for zi in zsupport},
            "p_power": mon[0],
            "q_power": mon[1],
        })
    return singletons, len(unique), dict(term_profile)


def node_key(zeros):
    return tuple(sorted(zeros))


def close_search(raw_rows, active, determinants, initial_zeros, max_nodes=2048):
    stats = Counter()
    nodes = 0

    initial = frozenset(initial_zeros)
    initial_rows = specialize_rows(raw_rows, initial)

    def visit(zeros, rows, depth=0):
        nonlocal nodes
        zeros = frozenset(zeros)
        key = node_key(zeros)
        nodes += 1
        if nodes > max_nodes:
            raise RuntimeError(("zero-branch search exceeded node budget", max_nodes))
        stats["nodes"] += 1

        killed, survivor_counts = killed_determinants(active, determinants, zeros)
        if killed:
            stats["closed_F"] += 1
            return {
                "closed": True,
                "reason": "F_invertibility",
                "zero_z": key,
                "killed_blocks": killed,
                "min_surviving_det_terms": min(survivor_counts.values()),
                "depth": depth,
            }

        singleton_rows, unique_count, term_profile = canonical_constraints(rows)
        constants = [r for r in singleton_rows if not r["z_support"]]
        if constants:
            stats["closed_torus"] += 1
            return {
                "closed": True,
                "reason": "torus_monomial_contradiction",
                "zero_z": key,
                "certificate": constants[0],
                "unique_specialized_polynomials": unique_count,
                "term_profile": term_profile,
                "min_surviving_det_terms": min(survivor_counts.values()),
                "depth": depth,
            }

        forced_by_var = {}
        for row in singleton_rows:
            support = row["z_support"]
            if len(support) == 1:
                forced_by_var.setdefault(support[0], row)

        # Variables already in zeros cannot appear after exact specialization,
        # but keep the guard explicit for certificate readability.
        forced_by_var = {zi: row for zi, row in forced_by_var.items() if zi not in zeros}
        if forced_by_var:
            newvars = tuple(sorted(forced_by_var))
            child_rows = specialize_rows(rows, newvars)
            child = visit(zeros | set(newvars), child_rows, depth + 1)
            stats["forced_steps"] += 1
            return {
                "closed": child["closed"],
                "reason": "forced_singletons_then_" + child["reason"],
                "zero_z": key,
                "forced_zero": [
                    {
                        "variable": zname(zi),
                        "provenance": forced_by_var[zi]["provenance"],
                        "power": forced_by_var[zi]["z_powers"][zname(zi)],
                    }
                    for zi in newvars
                ],
                "unique_specialized_polynomials": unique_count,
                "child": child,
                "depth": depth,
            }

        products = [r for r in singleton_rows if len(r["z_support"]) >= 2]
        if not products:
            stats["open_stable"] += 1
            return {
                "closed": False,
                "reason": "stable_no_singleton_product_constraint",
                "zero_z": key,
                "unique_specialized_polynomials": unique_count,
                "term_profile": term_profile,
                "min_surviving_det_terms": min(survivor_counts.values()),
                "depth": depth,
            }

        products.sort(
            key=lambda r: (
                len(r["z_support"]),
                r["z_support"],
                str(r["provenance"]),
            )
        )
        chosen = products[0]
        children = []
        for zi in chosen["z_support"]:
            child_rows = specialize_rows(rows, (zi,))
            child = visit(zeros | {zi}, child_rows, depth + 1)
            children.append({"set_zero": zname(zi), "result": child})
        closed = all(c["result"]["closed"] for c in children)
        stats["product_branches"] += 1
        return {
            "closed": closed,
            "reason": "exhaustive_product_branch" if closed else "product_branch_has_survivor",
            "zero_z": key,
            "product_constraint": chosen,
            "unique_specialized_polynomials": unique_count,
            "children": children,
            "depth": depth,
        }

    result = visit(initial, initial_rows)
    return result, dict(stats)


def compact_chain(result, depth=0, limit=14):
    if depth >= limit:
        return {"reason": "depth_limit"}
    out = {
        "zero_z": result.get("zero_z"),
        "closed": result["closed"],
        "reason": result["reason"],
    }
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
            {
                "set_zero": c["set_zero"],
                "result": compact_chain(c["result"], depth + 1, limit),
            }
            for c in result["children"]
        ]
    return out


def audit(cid, mask, branches):
    quotient, raw_rows, scalar_positions = compile_raw_final(cid, mask)
    if quotient["F_components"] != 21:
        raise RuntimeError((
            "this closure probe currently expects 21 F components",
            cid,
            mask,
            quotient["F_components"],
        ))
    if len(raw_rows) != 50880 or scalar_positions != 56448:
        raise RuntimeError((
            "unexpected raw final-kernel size",
            len(raw_rows),
            scalar_positions,
        ))

    active, determinants = determinant_data(cid, mask)
    if len(active) != quotient["F_components"]:
        raise RuntimeError(("active-coordinate mismatch", len(active), quotient["F_components"]))

    out_rows = []
    for name in branches:
        result, stats = close_search(raw_rows, active, determinants, BASE_PATTERNS[name])
        row = {
            "component": cid,
            "mask": mask,
            "branch": name,
            "initial_zero_z": BASE_PATTERNS[name],
            "closed": result["closed"],
            "stats": stats,
            "certificate_tree": compact_chain(result),
        }
        out_rows.append(row)
        print(row, flush=True)

    summary = {
        "component": cid,
        "mask": mask,
        "raw_nonzero_final_entries": len(raw_rows),
        "branches": branches,
        "closed": sum(bool(r["closed"]) for r in out_rows),
        "total": len(out_rows),
        "survivors": [r["branch"] for r in out_rows if not r["closed"]],
    }
    print("SUMMARY", summary, flush=True)
    if summary["closed"] == summary["total"]:
        print(
            "RESULT: z0=0 is completely excluded by raw-before-canonical exact propagation for mask",
            mask,
            flush=True,
        )
    else:
        print(
            "RESULT: unresolved z0=0 branches remain for mask",
            mask,
            summary["survivors"],
            flush=True,
        )
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
