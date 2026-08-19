"""Exact theorem-level audit of epsilon-minus cross-D amplitudes modulo gauge.

Phase 1 fixes one Pauli/Clifford chirality on each of the eight multiplicity-two
fusion spaces V_{MN}^P.  The 48 cross-D blocks are then projectively fixed, up
to one nonzero scalar amplitude t_j per block.  The complete D pentagons give
168 binomial equations in these 48 amplitudes.

A previous closure step produced and exactly replayed one root-of-unity witness
for each surviving (scalar component, chirality) branch.  Existence of one
witness is not enough for a non-categorifiability theorem: inequivalent
amplitude solutions could in principle lead to additional E/F branches.

This script audits the *entire* homogeneous amplitude solution group.  For a
fixed inhomogeneous solution t, the ratio u=t'/t of two solutions satisfies

    prod_j u_j**A[r,j] = 1

for the integer exponent matrix A of all 168 binomial D constraints.  Hence the
homogeneous solution group is the diagonal algebraic group with character
lattice Z^48 / rowspan(A).

There is also a manifest residual trivalent gauge torus: multiply the basis of
each of the eight 2D fusion spaces V_{MN}^P by a scalar.  Scalar conjugation
leaves every Pauli seed matrix unchanged.  A cross-D F block maps between one
multiplicity-two source fusion space and one multiplicity-two target fusion
space, so its amplitude changes by the endpoint scalar ratio.  The resulting
48 x 8 incidence matrix B is constructed directly from the fusion paths, not
hard-coded.

The theorem-completeness criterion is:

1. A*B = 0, so the residual gauge orbit lies in the homogeneous D solution;
2. Smith(A) has no nontrivial torsion, so that solution group is connected;
3. dim ker(A) = rank(B).

Then the connected residual-gauge image is a closed subtorus of the connected
homogeneous solution group with the same dimension, hence they are equal.
Therefore every nonzero D-amplitude solution is gauge-equivalent to the exact
witness already used by the downstream E/F/Phase-5 analysis.
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
    """Return (source_space, target_space) for one 2x2 cross-D F block.

    For F^{abc}_d the source basis is
        V_ab^e tensor V_ec^d,
    while the target basis is
        V_bc^f tensor V_af^d.
    A cross-D block has exactly one multiplicity-two trivalent factor on each
    side.  We extract those factors directly from fusion multiplicities.
    """
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
    """48 x 8 endpoint-incidence map for scalar basis gauges on 2D spaces."""
    B = sp.zeros(len(tr.CROSS_KEYS), len(tr.SPACES))
    edges = []
    for key in tr.CROSS_KEYS:
        i = tr.T_INDEX[key]
        source, target = multiplicity_two_endpoints(key)
        # Convention is immaterial up to replacing all endpoint parameters by
        # inverses; this is source/target as read from the F-symbol basis.
        B[i, tr.SPACE_INDEX[source]] += 1
        B[i, tr.SPACE_INDEX[target]] -= 1
        edges.append((source, target))

    # The underlying transport graph should be exactly two connected K4s.
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
        "residual_gauge_rank": gauge_rank,
        "residual_gauge_kernel_dimension": len(tr.SPACES) - gauge_rank,
    }, flush=True)

    if component_sizes != [4, 4] or gauge_rank != 6:
        raise AssertionError(("unexpected residual gauge graph", components, gauge_rank))

    profile_cache = {}
    matrix_variants = defaultdict(list)
    complete = []

    for cid in da.FRONTIER_COMPONENTS:
        for mask in da.SURVIVOR_MASKS:
            ratios, _source, _shapes, _seeds, _nonzero = da.collect_ratio_constraints(cid, mask)
            rows = exponent_rows(ratios)
            matrix_variants[rows].append((cid, mask))

            if rows not in profile_cache:
                A, diag, torsion = smith_profile(rows)
                gauge_residual = A * B
                gauge_in_kernel = gauge_residual == sp.zeros(A.rows, B.cols)
                rank = len(diag)
                free_dimension = len(tr.CROSS_KEYS) - rank
                profile_cache[rows] = {
                    "A": A,
                    "rank": rank,
                    "smith_nonzero": diag,
                    "torsion": torsion,
                    "free_dimension": free_dimension,
                    "gauge_in_kernel": gauge_in_kernel,
                }

            p = profile_cache[rows]
            row = {
                "component": cid,
                "mask": mask,
                "ratio_constraints": len(ratios),
                "amplitude_variables": len(tr.CROSS_KEYS),
                "exponent_rank": p["rank"],
                "homogeneous_dimension": p["free_dimension"],
                "smith_torsion": p["torsion"],
                "residual_gauge_rank": gauge_rank,
                "gauge_in_kernel": p["gauge_in_kernel"],
                "complete_mod_gauge": (
                    p["gauge_in_kernel"]
                    and not p["torsion"]
                    and p["free_dimension"] == gauge_rank
                ),
            }
            print(row, flush=True)
            if not row["complete_mod_gauge"]:
                raise AssertionError(("D-amplitude mod-gauge completeness failed", row, p["smith_nonzero"]))
            complete.append((cid, mask))

    print({
        "distinct_exponent_matrix_variants": len(matrix_variants),
        "variant_branch_counts": sorted(len(v) for v in matrix_variants.values()),
        "complete_branches": complete,
        "total": len(complete),
    }, flush=True)
    if len(complete) != 16:
        raise AssertionError(complete)

    print(
        "RESULT: every nonzero D-amplitude solution on every deep chirality survivor "
        "is gauge-equivalent to the exact witness used downstream",
        flush=True,
    )


if __name__ == "__main__":
    main()
