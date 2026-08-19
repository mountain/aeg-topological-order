"""Theorem-level audit of the 16 canonical scalar A/B/C components of R(2,2).

The scalar pentagons define an algebraic subgroup of (C*)^153.  The connected
trivalent-gauge image has the same dimension as the identity component of that
solution group.  Smith torsion of the scalar exponent matrix is (2,2,2,2), so
the quotient has exactly 16 connected components.

The historical source of one superseded epsilon-minus claim was an incomplete
sign-only treatment of complex gauge: an i-valued gauge can induce additional
sign changes that are invisible in the naive mod-2 column span of the gauge
matrix.  This verifier therefore tests the hard-coded COMPONENT_REPS against
the full C* gauge torus using an integer Smith decomposition of the gauge map.

If D = S G T is a Smith decomposition of the integer gauge matrix G, then a
sign vector b (the point b/2 in additive phase coordinates) lies in the full
complex gauge image iff every coordinate of S*b beyond rank(G) is even.  The
nonzero Smith factors in the first rank(G) coordinates impose no restriction
because multiplication by a nonzero integer is surjective on C*.
"""
from __future__ import annotations

from math import prod

import sympy as sp
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

import r22_scalar_audit as sa
from r22_epsplus_local_f_obstruction import COMPONENT_REPS, EPS_PLUS, SC_INDEX


def bit_vector(bits: int, n: int) -> sp.Matrix:
    if bits >> n:
        raise AssertionError(("representative has bits outside scalar inventory", bits.bit_length(), n))
    return sp.Matrix([(bits >> j) & 1 for j in range(n)])


def is_sign_solution(A: sp.Matrix, b: sp.Matrix) -> bool:
    # (-1)^b satisfies every monomial equation iff A*b is even entrywise.
    return all(int(x) % 2 == 0 for x in A * b)


def gauge_smith_left_transform(G: sp.Matrix):
    dm = DomainMatrix.from_Matrix(G).convert_to(ZZ)
    D, S, _T = smith_normal_decomp(dm)
    Dm = D.to_Matrix()
    Sm = S.to_Matrix()
    rank = G.rank()
    nonzero = [abs(int(Dm[i, i])) for i in range(min(Dm.shape)) if Dm[i, i] != 0]
    if len(nonzero) != rank:
        raise AssertionError(("gauge Smith/rank mismatch", rank, nonzero))
    return Sm, rank, nonzero


def in_full_complex_gauge_image(sign_vector: sp.Matrix, S: sp.Matrix, rank: int) -> bool:
    """Whether (-1)^sign_vector lies in the connected C* gauge image."""
    transformed = S * sign_vector
    return all(int(transformed[i]) % 2 == 0 for i in range(rank, transformed.rows))


def main():
    keys, idx, A, _examples = sa.build_scalar_system()
    triples, G = sa.build_scalar_gauge(keys)

    if A * G != sp.zeros(A.rows, G.cols):
        raise AssertionError("gauge image does not lie in scalar-pentagon kernel")

    rank_a = A.rank()
    rank_g = G.rank()
    torsion = sa.torsion_invariants(A)
    connected_solution_dim = len(keys) - rank_a
    quotient_dim = connected_solution_dim - rank_g
    component_count = prod(torsion)

    print({
        "scalar_variables": len(keys),
        "monomial_pentagons": A.rows,
        "scalar_rank": rank_a,
        "connected_solution_dimension": connected_solution_dim,
        "gauge_variables": len(triples),
        "effective_gauge_rank": rank_g,
        "continuous_quotient_dimension": quotient_dim,
        "smith_torsion": torsion,
        "component_count": component_count,
    }, flush=True)

    if (len(keys), A.rows, rank_a, rank_g, quotient_dim) != (153, 729, 129, 24, 0):
        raise AssertionError("unexpected scalar/gauge dimensions")
    if torsion != [2, 2, 2, 2] or component_count != 16:
        raise AssertionError(("unexpected scalar component group", torsion, component_count))

    # Full complex gauge image, not the naive sign-only image.
    Sg, gauge_rank, gauge_smith = gauge_smith_left_transform(G)
    if gauge_rank != 24:
        raise AssertionError(("unexpected gauge rank", gauge_rank))
    print({"gauge_smith_nonzero": gauge_smith}, flush=True)

    reps = list(COMPONENT_REPS)
    if len(reps) != 16 or len(set(reps)) != 16:
        raise AssertionError(("bad representative count", len(reps), len(set(reps))))

    vectors = [bit_vector(bits, len(keys)) for bits in reps]
    for cid, b in enumerate(vectors):
        if not is_sign_solution(A, b):
            raise AssertionError(("canonical representative is not a scalar solution", cid))

    # Two sign representatives lie in the same connected/gauge component iff
    # their ratio sign vector is a point of the full complex gauge torus.
    collisions = []
    for i in range(len(vectors)):
        for j in range(i):
            diff = vectors[i] + vectors[j]
            diff = diff.applyfunc(lambda x: int(x) & 1)
            if in_full_complex_gauge_image(diff, Sg, gauge_rank):
                collisions.append((j, i))
    if collisions:
        raise AssertionError(("canonical reps collide under full C* gauge", collisions))

    # There are exactly 16 components and we have 16 pairwise distinct points,
    # hence the representative list is exhaustive.
    if len(vectors) != component_count:
        raise AssertionError(("representatives do not exhaust components", len(vectors), component_count))

    eps_index = idx[("h", "X", "h", "X")]
    eps_plus = [cid for cid, bits in enumerate(reps) if ((bits >> eps_index) & 1) == 0]
    eps_minus = [cid for cid, bits in enumerate(reps) if ((bits >> eps_index) & 1) == 1]
    expected_plus = [0, 1, 2, 3, 8, 9, 10, 11]
    expected_minus = [4, 5, 6, 7, 12, 13, 14, 15]
    if eps_plus != expected_plus or eps_minus != expected_minus:
        raise AssertionError(("epsilon partition mismatch", eps_plus, eps_minus))
    if list(EPS_PLUS) != expected_plus or SC_INDEX[("h", "X", "h", "X")] != eps_index:
        raise AssertionError("consumer epsilon indexing disagrees with scalar audit")

    print({
        "canonical_representatives": len(reps),
        "pairwise_full_Cstar_gauge_distinct": True,
        "exhaustive": True,
        "epsilon_plus": eps_plus,
        "epsilon_minus": eps_minus,
    }, flush=True)
    print("RESULT: the 16 COMPONENT_REPS are a complete full-C* gauge component inventory", flush=True)


if __name__ == "__main__":
    main()
