"""Exact theorem-level audit of epsilon-minus cross-D amplitudes modulo gauge.

Phase 1 fixes one Pauli/Clifford chirality on each of the eight multiplicity-two
fusion spaces V_{MN}^P.  The 48 cross-D blocks are then projectively fixed, up
to one nonzero scalar amplitude t_j per block.  The complete D pentagons give
168 binomial equations in these 48 amplitudes.

A previous closure step produced and exactly replayed one root-of-unity witness
for each surviving (scalar component, chirality) branch.  Existence of one
witness is not enough for a non-categorifiability theorem: inequivalent
amplitude solutions could in principle lead to additional E/F branches.

For a fixed inhomogeneous solution t, the ratio u=t'/t of two solutions obeys
all homogeneous character equations defined by the integer exponent matrix A.
Thus the homogeneous solution group has character lattice

    Z^48 / rowspan(A).

A manifest connected residual gauge torus comes from scalar basis changes on
the eight multiplicity-two fusion spaces.  This script constructs its 48 x 8
endpoint-incidence matrix B directly from the source/target fusion paths and
checks A*B=0.

The first theorem-audit run discovered that the connected dimensions match but
Smith(A) contains two factors 2.  Therefore the purpose of this version is to
diagnose that discrete torsion *across all 16 deep branches* rather than abort
on the first one.  A later audit must determine whether the resulting Z2^2 is
removed by disconnected residual gauge/Pauli normalizer transformations or is
a genuine fourfold D-amplitude branch split.
"""
from __future__ import annotations

from collections import defaultdict

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

import r22_epsminus_d_amplitude as da
import r22_epsminus_d_trace as tr
from r22_scale_audit import N, OBJECTS


def multiplicity_two_endpoints(key):
    """Return (source_space, target_space) for one 2x2 cross-D F block."""
    a, b, c, d = key
    source = []
    target = []

    for e in OBJECTS:
        n1, n2 = N(a, b, e), N(e, c, d)
        if not n1 or not n2:
            continue
        if n1 == 2 and n2 == 1:
            source.append((a, b, e))
        elif n1 == 1 and n2 == 2:
            source.append((e, c, d))
        elif n1 * n2 != 1:
            raise AssertionError(("unexpected source multiplicity pattern", key, e, n1, n2))

    for f in OBJECTS:
        n1, n2 = N(b, c, f), N(a, f, d)
        if not n1 or not n2:
            continue
        if n1 == 2 and n2 == 1:
            target.append((b, c, f))
        elif n1 == 1 and n2 == 2:
            target.append((a, f, d))
        elif n1 * n2 != 1:
            raise AssertionError(("unexpected target multiplicity pattern", key, f, n1, n2))

    if len(source) != 1 or len(target) != 1:
        raise AssertionError(("cross-D block does not have unique 2D endpoints", key, source, target))
    if source[0] not in tr.SPACE_INDEX or target[0] not in tr.SPACE_INDEX:
        raise AssertionError(("endpoint outside multiplicity-two X/Y spaces", key, source, target))
    return source[0], target[0]


def residual_gauge_matrix():
    B = sp.zeros(len(tr.CROSS_KEYS), len(tr.SPACES))
    edges = []
    for key in tr.CROSS_KEYS:
        i = tr.T_INDEX[key]
        source, target = multiplicity_two_endpoints(key)
        B[i, tr.SPACE_INDEX[source]] += 1
        B[i, tr.SPACE_INDEX[target]] -= 1
        edges.append((source, target))

    adjacency = {s: set() for s in tr.SPACES}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    comps = []
    seen = set()
    for s in tr.SPACES:
        if s in seen:
            continue
        stack = [s]
        comp = set()
        while stack:
            u = stack.pop()
            if u in comp:
                continue
            comp.add(u)
            seen.add(u)
            stack.extend(adjacency[u] - comp)
        comps.append(comp)
    return B, tuple(sorted((tuple(sorted(c)) for c in comps), key=str))


def exponent_rows(ratios):
    rows = []
    for key in sorted(ratios):
        row = [0] * len(tr.CROSS_KEYS)
        for i, power in key:
            row[i] = int(power)
        rows.append(tuple(row))
    if len(rows) != 168:
        raise AssertionError(("unexpected D ratio count", len(rows)))
    return tuple(rows)


def gf2_rank(rows):
    packed = []
    for row in rows:
        bits = 0
        for j, x in enumerate(row):
            if x & 1:
                bits |= 1 << j
        if bits:
            packed.append(bits)
    rank = 0
    for col in range(len(tr.CROSS_KEYS)):
        pivot = next((i for i in range(rank, len(packed)) if (packed[i] >> col) & 1), None)
        if pivot is None:
            continue
        packed[rank], packed[pivot] = packed[pivot], packed[rank]
        for i in range(len(packed)):
            if i != rank and ((packed[i] >> col) & 1):
                packed[i] ^= packed[rank]
        rank += 1
    return rank


def smith_profile(rows):
    A = sp.Matrix(rows)
    S = smith_normal_form(A, domain=ZZ)
    diag = [
        abs(int(S[i, i]))
        for i in range(min(S.shape))
        if S[i, i] != 0
    ]
    torsion = [d for d in diag if d != 1]
    return A, diag, torsion


def main():
    B, components = residual_gauge_matrix()
    gauge_rank = B.rank()
    component_sizes = sorted(len(c) for c in components)
    print({
        "cross_D_amplitudes": len(tr.CROSS_KEYS),
        "multiplicity_two_spaces": len(tr.SPACES),
        "transport_component_sizes": component_sizes,
        "connected_residual_gauge_rank": gauge_rank,
        "connected_residual_gauge_kernel_dimension": len(tr.SPACES) - gauge_rank,
    }, flush=True)
    if component_sizes != [4, 4] or gauge_rank != 6:
        raise AssertionError(("unexpected residual gauge graph", components, gauge_rank))

    profile_cache = {}
    matrix_variants = defaultdict(list)
    branches = []

    for cid in da.FRONTIER_COMPONENTS:
        for mask in da.SURVIVOR_MASKS:
            ratios, _source, _shapes, _seeds, _nonzero = da.collect_ratio_constraints(cid, mask)
            rows = exponent_rows(ratios)
            matrix_variants[rows].append((cid, mask))

            if rows not in profile_cache:
                A, diag, torsion = smith_profile(rows)
                profile_cache[rows] = {
                    "A": A,
                    "rank": len(diag),
                    "mod2_rank": gf2_rank(rows),
                    "smith_nonzero": diag,
                    "torsion": torsion,
                    "free_dimension": len(tr.CROSS_KEYS) - len(diag),
                    "gauge_in_kernel": A * B == sp.zeros(A.rows, B.cols),
                }

            p = profile_cache[rows]
            connected_exhaustive = (
                p["gauge_in_kernel"]
                and p["free_dimension"] == gauge_rank
            )
            disconnected_classes = 1
            for d in p["torsion"]:
                disconnected_classes *= d
            row = {
                "component": cid,
                "mask": mask,
                "ratio_constraints": len(ratios),
                "amplitude_variables": len(tr.CROSS_KEYS),
                "exponent_rank_Q": p["rank"],
                "exponent_rank_F2": p["mod2_rank"],
                "homogeneous_connected_dimension": p["free_dimension"],
                "smith_torsion": p["torsion"],
                "homogeneous_connected_components": disconnected_classes,
                "connected_residual_gauge_rank": gauge_rank,
                "connected_gauge_in_kernel": p["gauge_in_kernel"],
                "connected_part_exhausted_by_gauge": connected_exhaustive,
                "full_mod_gauge_completeness_pending": disconnected_classes != 1,
            }
            print(row, flush=True)
            if not connected_exhaustive:
                raise AssertionError(("connected D-amplitude quotient still has moduli", row))
            branches.append(row)

    variants = []
    for rows, ids in matrix_variants.items():
        p = profile_cache[rows]
        variants.append({
            "branches": ids,
            "rank_Q": p["rank"],
            "rank_F2": p["mod2_rank"],
            "smith_torsion": p["torsion"],
            "smith_nonzero": p["smith_nonzero"],
        })

    print({
        "distinct_exponent_matrix_variants": len(matrix_variants),
        "variant_branch_counts": sorted(len(v) for v in matrix_variants.values()),
        "variants": variants,
        "total_branches": len(branches),
    }, flush=True)
    if len(branches) != 16:
        raise AssertionError(len(branches))

    torsion_profiles = {tuple(b["smith_torsion"]) for b in branches}
    if torsion_profiles != {(2, 2)}:
        raise AssertionError(("unexpected/nonuniform D torsion profile", torsion_profiles))

    print(
        "RESULT: connected D-amplitude freedom is exactly residual gauge, but a uniform Z2 x Z2 discrete quotient remains to be audited",
        flush=True,
    )


if __name__ == "__main__":
    main()
