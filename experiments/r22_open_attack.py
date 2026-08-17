"""Open-problem attack on the unresolved fusion ring R(2,2).

This experiment is deliberately different from the earlier Fibonacci benchmarks:
the target is not to reconstruct known data more efficiently, but to reduce a
categorification problem that Meng--Yu (arXiv:2608.06064, 2026) explicitly
leave open.

Research labels used in this file:
- CLASSICAL: standard fusion-ring/equivariantization facts.
- COMPUTATIONAL-CLAIM: finite counts verified by this script.
- CANDIDATE-NEW: project-specific reductions not claimed as literature theorems.
- CONJECTURE: hypotheses still requiring a categorical proof or construction.

The central conditional reduction is:

    if a categorification A of R(2,2) admits a monoidal C2-action which
    fixes 1,g,h,gh and swaps X,Y, then A^C2 has a near-group fusion ring
    R(Ghat, 8), where Ghat is a central extension

        1 -> C2 -> Ghat -> C2 x C2 -> 1.

At ring level this follows from

    (X+Y)^2 = 2(1+g+h+gh) + 8(X+Y).

The hard problem is therefore not this ring identity but the existence and
coherence of the monoidal lift of the swap symmetry, and the extension class
of Ghat.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
from typing import Callable, Dict, Iterable, Mapping, Tuple

import sympy as sp

Obj = str
Fusion = Counter[Obj]

OBJECTS: Tuple[Obj, ...] = ("1", "g", "h", "k", "X", "Y")
INVERTIBLES: Tuple[Obj, ...] = ("1", "g", "h", "k")
NONINVERTIBLES: Tuple[Obj, ...] = ("X", "Y")

_V4 = {"1": (0, 0), "g": (1, 0), "h": (0, 1), "k": (1, 1)}
_FROM_V4 = {value: key for key, value in _V4.items()}


def v4_mul(a: Obj, b: Obj) -> Obj:
    x, y = _V4[a]
    u, v = _V4[b]
    return _FROM_V4[(x ^ u, y ^ v)]


def fusion_R(m: int, n: int, a: Obj, b: Obj) -> Fusion:
    """CLASSICAL: the self-dual rank-6 V4-quadratic fusion ring R(m,n)."""
    if a in INVERTIBLES and b in INVERTIBLES:
        return Counter({v4_mul(a, b): 1})

    if a in INVERTIBLES and b in NONINVERTIBLES:
        q, z = a, b
    elif b in INVERTIBLES and a in NONINVERTIBLES:
        q, z = b, a
    else:
        q = z = None

    if q is not None:
        # Stabilizer of each noninvertible is <h>; g and k swap X,Y.
        if q in ("g", "k"):
            return Counter({"Y" if z == "X" else "X": 1})
        return Counter({z: 1})

    if a == b and a in NONINVERTIBLES:
        return Counter({"1": 1, "h": 1, "X": m, "Y": n})

    if {a, b} == {"X", "Y"}:
        return Counter({"g": 1, "k": 1, "X": n, "Y": m})

    raise ValueError((a, b))


def fusion_Rprime(m: int, a: Obj, b: Obj) -> Fusion:
    """CLASSICAL: the non-self-dual unresolved comparison family R'(m)."""
    if a in INVERTIBLES and b in INVERTIBLES:
        return Counter({v4_mul(a, b): 1})

    if a in INVERTIBLES and b in NONINVERTIBLES:
        q, z = a, b
    elif b in INVERTIBLES and a in NONINVERTIBLES:
        q, z = b, a
    else:
        q = z = None

    if q is not None:
        if q in ("g", "k"):
            return Counter({"Y" if z == "X" else "X": 1})
        return Counter({z: 1})

    if a == b and a in NONINVERTIBLES:
        return Counter({"g": 1, "k": 1, "X": m, "Y": m})

    if {a, b} == {"X", "Y"}:
        return Counter({"1": 1, "h": 1, "X": m, "Y": m})

    raise ValueError((a, b))


def multiply_linear(
    fusion: Callable[[Obj, Obj], Fusion], left: Mapping[Obj, int], right: Mapping[Obj, int]
) -> Fusion:
    out: Fusion = Counter()
    for a, ca in left.items():
        for b, cb in right.items():
            for c, multiplicity in fusion(a, b).items():
                out[c] += ca * cb * multiplicity
    return +out


def verify_associativity(fusion: Callable[[Obj, Obj], Fusion]) -> None:
    for a, b, c in product(OBJECTS, repeat=3):
        left = multiply_linear(fusion, fusion(a, b), Counter({c: 1}))
        right = multiply_linear(fusion, Counter({a: 1}), fusion(b, c))
        assert left == right, (a, b, c, left, right)


def N(fusion: Callable[[Obj, Obj], Fusion], a: Obj, b: Obj, c: Obj) -> int:
    return fusion(a, b).get(c, 0)


def associator_profile(fusion: Callable[[Obj, Obj], Fusion]) -> Dict[str, object]:
    """COMPUTATIONAL-CLAIM: raw F-block dimensions before symmetry/gauge reduction."""
    histogram: Counter[int] = Counter()
    raw_matrix_entries = 0
    blocks = 0

    for a, b, c, d in product(OBJECTS, repeat=4):
        left_dim = sum(N(fusion, a, b, e) * N(fusion, e, c, d) for e in OBJECTS)
        right_dim = sum(N(fusion, b, c, f) * N(fusion, a, f, d) for f in OBJECTS)
        assert left_dim == right_dim
        if left_dim:
            blocks += 1
            histogram[left_dim] += 1
            raw_matrix_entries += left_dim * left_dim

    return {
        "nonzero_F_blocks": blocks,
        "raw_F_matrix_entries": raw_matrix_entries,
        "block_dimension_histogram": dict(sorted(histogram.items())),
    }


def fusion_space_gauge_profile(fusion: Callable[[Obj, Obj], Fusion]) -> Dict[str, object]:
    """Count GL(N_ab^c) dimensions, with strict-unit spaces excluded separately."""
    all_dimension = 0
    strict_unit_reduced = 0
    histogram: Counter[int] = Counter()

    for a, b, c in product(OBJECTS, repeat=3):
        multiplicity = N(fusion, a, b, c)
        if not multiplicity:
            continue
        histogram[multiplicity] += 1
        all_dimension += multiplicity * multiplicity
        if a != "1" and b != "1":
            strict_unit_reduced += multiplicity * multiplicity

    return {
        "all_GL_parameter_dimension": all_dimension,
        "strict_unit_reduced_dimension": strict_unit_reduced,
        "fusion_multiplicity_histogram": dict(sorted(histogram.items())),
    }


def pentagon_profile(fusion: Callable[[Obj, Obj], Fusion]) -> Dict[str, object]:
    """COMPUTATIONAL-CLAIM: naive matrix sizes for all four-input pentagons.

    This is intentionally only a difficulty profile, not the solver that the
    project ultimately wants to use.  The whole point of the open attack is to
    avoid treating all these scalar entries as unrelated equations.
    """
    histogram: Counter[int] = Counter()
    blocks = 0
    scalar_equalities = 0

    for a, b, c, d, target in product(OBJECTS, repeat=5):
        dim_left_comb = sum(
            N(fusion, a, b, x) * N(fusion, x, c, y) * N(fusion, y, d, target)
            for x, y in product(OBJECTS, repeat=2)
        )
        dim_right_comb = sum(
            N(fusion, c, d, z) * N(fusion, b, z, y) * N(fusion, a, y, target)
            for z, y in product(OBJECTS, repeat=2)
        )
        assert dim_left_comb == dim_right_comb
        if dim_left_comb:
            blocks += 1
            histogram[dim_left_comb] += 1
            scalar_equalities += dim_left_comb * dim_left_comb

    return {
        "nonzero_pentagon_blocks": blocks,
        "naive_scalar_matrix_equalities": scalar_equalities,
        "pentagon_dimension_histogram": dict(sorted(histogram.items())),
    }


def fp_dimensions_R(m: int, n: int) -> Dict[str, sp.Expr]:
    """CLASSICAL: FP dimension of the two noninvertibles and global dimension."""
    s = sp.Integer(m + n)
    d = sp.simplify((s + sp.sqrt(s * s + 8)) / 2)
    global_dim = sp.simplify(4 + 2 * d**2)
    return {"d_X=d_Y": d, "global_dimension": global_dim}


def swap_automorphism_R22(obj: Obj) -> Obj:
    return {"X": "Y", "Y": "X"}.get(obj, obj)


def verify_R22_swap_ring_automorphism() -> None:
    fusion = lambda a, b: fusion_R(2, 2, a, b)
    for a, b in product(OBJECTS, repeat=2):
        source = fusion(a, b)
        mapped_source = Counter({swap_automorphism_R22(c): k for c, k in source.items()})
        target = fusion(swap_automorphism_R22(a), swap_automorphism_R22(b))
        assert mapped_source == target, (a, b, mapped_source, target)


def R22_orbit_square() -> Fusion:
    """COMPUTATIONAL-CLAIM: square of the formal orbit object X+Y."""
    fusion = lambda a, b: fusion_R(2, 2, a, b)
    orbit = Counter({"X": 1, "Y": 1})
    return multiply_linear(fusion, orbit, orbit)


# ----- central extensions of V4 by C2 ------------------------------------

V = ((0, 0), (1, 0), (0, 1), (1, 1))
ZERO = (0, 0)


def vadd(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    return (a[0] ^ b[0], a[1] ^ b[1])


def normalized_c2_2cocycles() -> Tuple[Dict[Tuple[Tuple[int, int], Tuple[int, int]], int], ...]:
    """Enumerate normalized beta: V4 x V4 -> C2 satisfying delta beta=0."""
    variable_pairs = tuple((a, b) for a in V for b in V if a != ZERO and b != ZERO)
    result = []
    for values in product((0, 1), repeat=len(variable_pairs)):
        beta = dict(zip(variable_pairs, values))

        def B(a: Tuple[int, int], b: Tuple[int, int]) -> int:
            if a == ZERO or b == ZERO:
                return 0
            return beta[(a, b)]

        if all(
            (B(b, c) ^ B(vadd(a, b), c) ^ B(a, vadd(b, c)) ^ B(a, b)) == 0
            for a, b, c in product(V, repeat=3)
        ):
            result.append(beta)
    return tuple(result)


def extension_type(beta: Mapping[Tuple[Tuple[int, int], Tuple[int, int]], int]) -> str:
    """Classify the order-8 central extension by elementary group invariants."""
    elements = tuple((a, eps) for a in V for eps in (0, 1))
    identity = (ZERO, 0)

    def B(a: Tuple[int, int], b: Tuple[int, int]) -> int:
        if a == ZERO or b == ZERO:
            return 0
        return beta[(a, b)]

    def mul(x, y):
        a, eps = x
        b, eta = y
        return (vadd(a, b), eps ^ eta ^ B(a, b))

    def order(x) -> int:
        current = identity
        for n in range(1, 9):
            current = mul(current, x)
            if current == identity:
                return n
        raise AssertionError(x)

    orders = Counter(order(x) for x in elements)
    commutative = all(mul(x, y) == mul(y, x) for x, y in product(elements, repeat=2))

    signature = (commutative, tuple(sorted(orders.items())))
    lookup = {
        (True, ((1, 1), (2, 7))): "C2^3",
        (True, ((1, 1), (2, 3), (4, 4))): "C4xC2",
        (False, ((1, 1), (2, 5), (4, 2))): "D8",
        (False, ((1, 1), (2, 1), (4, 6))): "Q8",
    }
    assert signature in lookup, signature
    return lookup[signature]


def central_extension_profile() -> Dict[str, int]:
    """COMPUTATIONAL-CLAIM: cocycle representatives before quotient by coboundaries."""
    return dict(sorted(Counter(extension_type(beta) for beta in normalized_c2_2cocycles()).items()))


def verify_conditional_neargroup_ring() -> Dict[str, object]:
    """CANDIDATE-NEW reduction target at the Grothendieck-ring level.

    If the swap ring automorphism lifts to a monoidal C2 action, equivariantization
    has eight invertibles (two lifts of each fixed V4 object) and one orbit simple
    rho whose forgetful object is X+Y.  Cyclic symmetry then forces every
    invertible to occur once in rho^2; the orbit-square identity fixes the
    remaining coefficient to 8.

    This function checks all purely ring-theoretic numerics.  It deliberately
    does NOT claim that the monoidal action exists.
    """
    orbit_square = R22_orbit_square()
    expected = Counter({"1": 2, "g": 2, "h": 2, "k": 2, "X": 8, "Y": 8})
    assert orbit_square == expected

    d = fp_dimensions_R(2, 2)["d_X=d_Y"]
    rho_dim = sp.simplify(2 * d)
    assert sp.simplify(rho_dim**2 - 8 * rho_dim - 8) == 0

    return {
        "forgetful_rho_square": dict(orbit_square),
        "rho_FP_dimension": rho_dim,
        "near_group_order": 8,
        "near_group_level": 8,
        "possible_central_extension_groups": ("C2^3", "C4xC2", "D8", "Q8"),
    }


def unresolved_difficulty_table() -> Dict[str, Dict[str, object]]:
    r22 = lambda a, b: fusion_R(2, 2, a, b)
    r44 = lambda a, b: fusion_R(4, 4, a, b)
    rp4 = lambda a, b: fusion_Rprime(4, a, b)
    return {
        "R(2,2)": {
            **associator_profile(r22),
            **fusion_space_gauge_profile(r22),
            **pentagon_profile(r22),
        },
        "R(4,4)": {
            **associator_profile(r44),
            **fusion_space_gauge_profile(r44),
            **pentagon_profile(r44),
        },
        "R'(4)": {
            **associator_profile(rp4),
            **fusion_space_gauge_profile(rp4),
            **pentagon_profile(rp4),
        },
    }


def main() -> None:
    r22 = lambda a, b: fusion_R(2, 2, a, b)
    r44 = lambda a, b: fusion_R(4, 4, a, b)
    rp4 = lambda a, b: fusion_Rprime(4, a, b)
    for fusion in (r22, r44, rp4):
        verify_associativity(fusion)

    verify_R22_swap_ring_automorphism()

    print("unresolved difficulty table")
    for name, data in unresolved_difficulty_table().items():
        print(name)
        for key, value in data.items():
            print(" ", key, value)

    print("\nR(2,2) FP dimensions")
    for key, value in fp_dimensions_R(2, 2).items():
        print(" ", key, "=", value)

    print("\nR(2,2) swap automorphism: PASS")
    print("(X+Y)^2 =", dict(R22_orbit_square()))

    print("\nconditional equivariantization -> near-group")
    for key, value in verify_conditional_neargroup_ring().items():
        print(" ", key, value)

    print("\nnormalized C2-valued 2-cocycle extension profile")
    print(central_extension_profile())


if __name__ == "__main__":
    main()
