"""Symbolic Fibonacci braiding from frozen F-data and generic hexagon coherence.

This is NOT a blind R reconstruction: the parent workstream has already been
exposed to a comparison source that contains explicit Fibonacci R-data.  The
script deliberately does not encode those constants.  It re-derives the
symbolic hexagon ideal from the already-frozen F-stage data and then compiles
small braid-group representations as F/R history transports.

Research labels:
- CLASSICAL: multiplicity-free hexagon equation, braid-group relations.
- REFORMULATION: permutation-enriched operation-history groupoid.
- COMPUTATIONAL-CLAIM: exact symbolic eliminations and matrix checks below.
"""

from __future__ import annotations

from itertools import permutations, product
from typing import Dict, List, Tuple

import sympy as sp

ONE = "1"
TAU = "t"
LABELS = (ONE, TAU)

# Frozen F-stage parameters.  The chosen unitary gauge satisfies
# alpha^2 + alpha - 1 = 0, s^2 = alpha, with alpha > 0.
alpha, s = sp.symbols("alpha s", nonzero=True)
r1, rt = sp.symbols("r1 rt", nonzero=True)


def fuse(a: str, b: str) -> Tuple[str, ...]:
    if a == ONE:
        return (b,)
    if b == ONE:
        return (a,)
    if a == TAU and b == TAU:
        return (ONE, TAU)
    raise ValueError((a, b))


def admissible_f(a: str, b: str, c: str, d: str, e: str, f: str) -> bool:
    return e in fuse(a, b) and d in fuse(e, c) and f in fuse(b, c) and d in fuse(a, f)


def f_symbol(a: str, b: str, c: str, d: str, e: str, f: str) -> sp.Expr:
    """Frozen Fibonacci F-data in the real symmetric unitary gauge."""
    if not admissible_f(a, b, c, d, e, f):
        return sp.Integer(0)
    if ONE in (a, b, c):
        return sp.Integer(1)
    if (a, b, c) != (TAU, TAU, TAU):
        raise ValueError((a, b, c, d, e, f))
    if d == ONE:
        return sp.Integer(1)  # g = 1 from the blind F-stage solve.
    if d == TAU:
        return {
            (ONE, ONE): alpha,
            (ONE, TAU): s,
            (TAU, ONE): s,
            (TAU, TAU): -alpha,
        }[(e, f)]
    raise ValueError(d)


def r_symbol(a: str, b: str, c: str) -> sp.Expr:
    """Unknown local exchange symbols, with vacuum braiding normalized to 1."""
    if c not in fuse(a, b):
        return sp.Integer(0)
    if ONE in (a, b):
        return sp.Integer(1)
    if (a, b) == (TAU, TAU):
        return r1 if c == ONE else rt
    raise ValueError((a, b, c))


def r_power(a: str, b: str, c: str, sign: int) -> sp.Expr:
    value = r_symbol(a, b, c)
    if value == 0:
        return sp.Integer(0)
    return value if sign == 1 else 1 / value


def hexagon_instances(sign: int = 1) -> List[Tuple[Tuple[str, ...], sp.Expr]]:
    """CLASSICAL: enumerate the multiplicity-free hexagon equation.

    Convention follows Aboumrad 2022, Eq. (2.3):

      (R^ac_e)^± F^{acb}_{d;eg} (R^bc_g)^±
        = sum_f F^{cab}_{d;ef} (R^{fc}_d)^± F^{abc}_{d;fg}.

    We return only nonzero polynomial numerators after clearing denominators.
    """
    if sign not in (1, -1):
        raise ValueError(sign)
    out: List[Tuple[Tuple[str, ...], sp.Expr]] = []
    for a, b, c, d, e, g in product(LABELS, repeat=6):
        lhs = r_power(a, c, e, sign) * f_symbol(a, c, b, d, e, g) * r_power(b, c, g, sign)
        rhs = sp.Integer(0)
        for f in LABELS:
            rhs += f_symbol(c, a, b, d, e, f) * r_power(f, c, d, sign) * f_symbol(a, b, c, d, f, g)
        diff = sp.factor(lhs - rhs)
        if diff == 0:
            continue
        numerator = sp.factor(sp.together(diff).as_numer_denom()[0])
        out.append(((a, b, c, d, e, g), numerator))
    return out


def hexagon_groebner() -> sp.GroebnerBasis:
    plus = [expr for _, expr in hexagon_instances(+1)]
    relations = plus + [alpha**2 + alpha - 1, s**2 - alpha]
    return sp.groebner(relations, r1, rt, s, alpha, order="lex")


def canonical_hexagon_relations() -> Tuple[sp.Expr, ...]:
    """COMPUTATIONAL-CLAIM: reduced symbolic R-family from the hexagons."""
    G = hexagon_groebner()
    expected = (
        alpha * rt + r1 + 1,
        alpha * rt + rt**2 + 1,
        -alpha + s**2,
        alpha**2 + alpha - 1,
    )
    assert tuple(G.polys[i].as_expr() for i in range(len(G.polys))) == expected
    # The negative hexagon is redundant modulo the positive hexagon ideal.
    for _, expr in hexagon_instances(-1):
        assert sp.factor(G.reduce(sp.expand(expr))[1]) == 0
    return expected


def cyclotomic_elimination() -> sp.Expr:
    """Eliminate alpha and identify the exchange phase polynomial."""
    z = sp.symbols("z")
    resultant = sp.factor(sp.resultant(alpha**2 + alpha - 1, z**2 + alpha * z + 1, alpha))
    assert sp.expand(resultant - sp.cyclotomic_poly(10, z)) == 0
    return resultant


def reducer() -> sp.GroebnerBasis:
    return sp.groebner(
        [
            alpha**2 + alpha - 1,
            s**2 - alpha,
            r1 - rt**2,
            rt**2 + alpha * rt + 1,
        ],
        r1,
        rt,
        s,
        alpha,
        order="lex",
    )


def reduce_matrix(matrix: sp.Matrix) -> sp.Matrix:
    G = reducer()
    return sp.Matrix(matrix.rows, matrix.cols, lambda i, j: sp.factor(G.reduce(sp.expand(matrix[i, j]))[1]))


def three_anyon_braids() -> Dict[str, Dict[str, sp.Matrix]]:
    """Compile B_3 generators on total-charge 1 and tau sectors."""
    F = sp.Matrix([[alpha, s], [s, -alpha]])
    D = sp.diag(r1, rt)

    # Total tau has basis indexed by the first-pair channel {1,tau}.
    sigma1_tau = D
    sigma2_tau = F * D * F  # F^{-1}=F modulo the frozen F relations.

    # Total 1 is one-dimensional; both adjacent pair channels are tau.
    sigma1_one = sp.Matrix([[rt]])
    sigma2_one = sp.Matrix([[rt]])

    return {
        ONE: {"sigma1": sigma1_one, "sigma2": sigma2_one},
        TAU: {"sigma1": sigma1_tau, "sigma2": sigma2_tau},
    }


def verify_b3() -> None:
    for sector in three_anyon_braids().values():
        x, y = sector["sigma1"], sector["sigma2"]
        assert reduce_matrix(x * y * x - y * x * y) == sp.zeros(x.rows)


def four_anyon_braids() -> Dict[str, Dict[str, sp.Matrix]]:
    """Compile B_4 generators in a left-associated fusion-path basis.

    total=1 basis: (e,f)=(1,t),(t,t)
    total=t basis: (e,f)=(1,t),(t,1),(t,t)
    where e is the first-pair channel and f the first-three channel.
    """
    F = sp.Matrix([[alpha, s], [s, -alpha]])
    D = sp.diag(r1, rt)
    block = F * D * F

    one_s1 = sp.diag(r1, rt)
    one_s2 = block
    one_s3 = sp.diag(r1, rt)

    tau_s1 = sp.diag(r1, rt, rt)

    tau_s2 = sp.zeros(3)
    # Nontrivial F block on states (1,t) and (t,t), plus scalar rt on (t,1).
    for i0, i in enumerate((0, 2)):
        for j0, j in enumerate((0, 2)):
            tau_s2[i, j] = block[i0, j0]
    tau_s2[1, 1] = rt

    tau_s3 = sp.zeros(3)
    # Scalar rt on (1,t), nontrivial block on (t,1),(t,t).
    tau_s3[0, 0] = rt
    for i0, i in enumerate((1, 2)):
        for j0, j in enumerate((1, 2)):
            tau_s3[i, j] = block[i0, j0]

    return {
        ONE: {"sigma1": one_s1, "sigma2": one_s2, "sigma3": one_s3},
        TAU: {"sigma1": tau_s1, "sigma2": tau_s2, "sigma3": tau_s3},
    }


def verify_b4() -> None:
    for sector in four_anyon_braids().values():
        s1, s2, s3 = sector["sigma1"], sector["sigma2"], sector["sigma3"]
        zero = sp.zeros(s1.rows)
        assert reduce_matrix(s1 * s2 * s1 - s2 * s1 * s2) == zero
        assert reduce_matrix(s2 * s3 * s2 - s3 * s2 * s3) == zero
        assert reduce_matrix(s1 * s3 - s3 * s1) == zero


def projective_spectral_invariant() -> sp.Expr:
    """Gauge-invariant eigenvalue ratio for exchanging identical tau anyons."""
    # r1/rt = rt because r1=rt^2.  Thus the projective ratio obeys Phi_10.
    return rt


def labelled_three_strand_groupoid_counts() -> Dict[str, int]:
    """REFORMULATION: count the smallest permutation-enriched history graph.

    Objects retain strand identities even though all three simple-object labels
    are tau.  There are two parenthesizations for each of 3! strand orders.
    F-edges preserve order; local R-edges exchange the sibling pair.  The graph
    is one 12-cycle.  After quotienting the strand identities by S_3, the two
    parenthesization objects remain, F is the connecting chart edge, and local
    exchanges become loops.  This is the combinatorial place where braid
    holonomy can survive while pure F coherence remains flat.
    """
    perms = list(permutations((1, 2, 3)))
    vertices = [(shape, p) for shape in ("L", "R") for p in perms]
    edges = set()

    def edge(u, v, kind):
        return (frozenset((u, v)), kind)

    for p in perms:
        edges.add(edge(("L", p), ("R", p), "F"))
        q = (p[1], p[0], p[2])
        edges.add(edge(("L", p), ("L", q), "R"))
        q = (p[0], p[2], p[1])
        edges.add(edge(("R", p), ("R", q), "R"))

    f_edges = sum(1 for _, kind in edges if kind == "F")
    r_edges = sum(1 for _, kind in edges if kind == "R")
    assert (len(vertices), len(edges), f_edges, r_edges) == (12, 12, 6, 6)

    # Every vertex has degree two and the graph is connected, hence a 12-cycle.
    adjacency = {v: set() for v in vertices}
    for pair, _ in edges:
        u, v = tuple(pair)
        adjacency[u].add(v)
        adjacency[v].add(u)
    assert all(len(nbrs) == 2 for nbrs in adjacency.values())
    seen = set()
    stack = [vertices[0]]
    while stack:
        v = stack.pop()
        if v in seen:
            continue
        seen.add(v)
        stack.extend(adjacency[v] - seen)
    assert len(seen) == 12

    return {
        "labelled_objects": 12,
        "labelled_F_edges": 6,
        "labelled_R_edges": 6,
        "labelled_cycle_length": 12,
        "quotient_parenthesization_objects": 2,
        "quotient_F_edges": 1,
        "quotient_R_loops": 2,
    }


def main() -> None:
    print("positive hexagon instances:", len(hexagon_instances(+1)))
    print("negative hexagon instances:", len(hexagon_instances(-1)))
    print("canonical Groebner relations:")
    for relation in canonical_hexagon_relations():
        print(" ", relation, "= 0")

    print("cyclotomic elimination:", cyclotomic_elimination())
    print("projective eigenvalue ratio:", projective_spectral_invariant())

    verify_b3()
    print("B3 relations: PASS")
    verify_b4()
    print("B4 relations: PASS")

    print("three-strand permutation-enriched history graph:")
    for key, value in labelled_three_strand_groupoid_counts().items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
