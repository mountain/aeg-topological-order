"""Pointed-cohomology and module-symmetry analysis for the open R(2,2) ring.

Purpose
-------
For any categorification C of R(2,2), its pointed subcategory is
P = Vec_{V4}^omega and the additive noninvertible sector M=<X,Y> is a
transitive P-module category with stabilizer H=<h>.  Meng--Yu prove
nu_2(h)=+1 and nu_2(g)=nu_2(gh)=+/-1.

This script performs two finite exact calculations.

1. It enumerates normalized {+/-1}-valued 3-cocycles on V4 and quotients them
   by C^*-coboundaries (implemented using fourth-root exponents).  The eight
   H^3(V4,C^*) classes are distinguished exactly by their restrictions to the
   three order-two subgroups.  Meng--Yu's indicator constraints leave only
   two classes: (+,+,+) and (-,+,-).  They are the pullbacks of the two
   H^3(V4/H,C^*) classes.

2. For each of these two canonical pointed associators, it constructs the
   transitive twisted G-set X=G/H and enumerates its module autoequivalences
   using the explicit Galindo--Plavnik 1-cell equation.  In both cases the
   module-autoequivalence group is C2 x C2, and the nontrivial G-set
   automorphism swapping the two cosets has an order-two module lift.

Consequences
------------
CLASSICAL/COMPUTATIONAL-CLAIM: the based-ring involution X<->Y is not
obstructed at the pointed-module level.  Any remaining obstruction to a
Z2 tensor symmetry lies in extending this module symmetry across the
noninvertible multiplication M tensor M and the full associator.

This is not yet a proof that R(2,2) is categorifiable or non-categorifiable.
"""

from __future__ import annotations

from itertools import product
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

G = ((0, 0), (1, 0), (0, 1), (1, 1))
E = (0, 0)
g = (1, 0)
h = (0, 1)
k = (1, 1)
NONZERO = tuple(x for x in G if x != E)
XSET = (0, 1)  # G/H, where H=<h>; quotient coordinate is the first bit.

Elt = Tuple[int, int]


def add(a: Elt, b: Elt) -> Elt:
    return (a[0] ^ b[0], a[1] ^ b[1])


def q(a: Elt) -> int:
    return a[0]


def act(a: Elt, x: int) -> int:
    return q(a) ^ x


# ---------------------------------------------------------------------------
# Normalized bar cohomology: H^3(V4,C^*) and restriction indicators.
# ---------------------------------------------------------------------------


def normalized_tuples(n: int) -> Tuple[Tuple[Elt, ...], ...]:
    return tuple(product(NONZERO, repeat=n))


BASES = {n: normalized_tuples(n) for n in (2, 3, 4)}
INDEX = {n: {t: i for i, t in enumerate(BASES[n])} for n in BASES}


def delta_matrix(n: int, modulus: int) -> np.ndarray:
    """Normalized bar differential C^n -> C^{n+1}, additive exponents."""
    rows, cols = BASES[n + 1], BASES[n]
    out = np.zeros((len(rows), len(cols)), dtype=np.int64)
    for row, args in enumerate(rows):
        terms = [args[1:]]
        terms += [args[:i] + (add(args[i], args[i + 1]),) + args[i + 2 :] for i in range(n)]
        terms += [args[:-1]]
        coeffs = [1] + [(-1) ** (i + 1) for i in range(n)] + [(-1) ** (n + 1)]
        for term, coeff in zip(terms, coeffs):
            if E in term:  # normalized cochains vanish if an argument is identity
                continue
            out[row, INDEX[n][term]] += coeff
    return out % modulus


def gf2_rref(matrix: np.ndarray) -> Tuple[np.ndarray, Tuple[int, ...]]:
    a = (matrix.copy() % 2).astype(np.uint8)
    m, n = a.shape
    pivots: List[int] = []
    row = 0
    for col in range(n):
        pivot = next((r for r in range(row, m) if a[r, col]), None)
        if pivot is None:
            continue
        if pivot != row:
            a[[row, pivot]] = a[[pivot, row]]
        for r in range(m):
            if r != row and a[r, col]:
                a[r] ^= a[row]
        pivots.append(col)
        row += 1
        if row == m:
            break
    return a, tuple(pivots)


def gf2_nullspace(matrix: np.ndarray) -> Tuple[np.ndarray, ...]:
    rref, pivots = gf2_rref(matrix)
    free = [c for c in range(matrix.shape[1]) if c not in pivots]
    basis = []
    for free_col in free:
        v = np.zeros(matrix.shape[1], dtype=np.uint8)
        v[free_col] = 1
        for row, pivot in enumerate(pivots):
            if rref[row, free_col]:
                v[pivot] = 1
        basis.append(v)
    return tuple(basis)


def gf2_span(basis: Sequence[np.ndarray], dimension: int) -> Tuple[np.ndarray, ...]:
    out = []
    for bits in product((0, 1), repeat=len(basis)):
        v = np.zeros(dimension, dtype=np.uint8)
        for bit, b in zip(bits, basis):
            if bit:
                v ^= b
        out.append(v)
    # Deduplicate potentially dependent generating sets.
    unique = {bytes(v): v for v in out}
    return tuple(unique.values())


def pm_one_cocycle_classes_mod_pm_coboundary() -> Tuple[Tuple[np.ndarray, ...], ...]:
    d2 = delta_matrix(2, 2)
    d3 = delta_matrix(3, 2)
    z3 = gf2_span(gf2_nullspace(d3), d3.shape[1])
    b3 = gf2_span(tuple(d2[:, j].astype(np.uint8) for j in range(d2.shape[1])), d2.shape[0])
    assert len(z3) == 512
    assert len(b3) == 32

    remaining = {bytes(v) for v in z3}
    classes = []
    while remaining:
        rep = np.frombuffer(min(remaining), dtype=np.uint8).copy()
        cls_bytes = {bytes(rep ^ b) for b in b3}
        classes.append(tuple(np.frombuffer(x, dtype=np.uint8).copy() for x in cls_bytes))
        remaining.difference_update(cls_bytes)
    assert len(classes) == 16  # H^3(V4,C2), before allowing C^* coboundaries.
    return tuple(classes)


def z4_two_coboundary_image() -> set[Tuple[int, ...]]:
    d2 = delta_matrix(2, 4)
    image = set()
    for coeffs in product(range(4), repeat=d2.shape[1]):
        value = (d2 @ np.asarray(coeffs, dtype=np.int64)) % 4
        image.add(tuple(int(x) for x in value))
    assert len(image) == 2048
    return image


def cstar_equiv(a: np.ndarray, b: np.ndarray, image_z4: set[Tuple[int, ...]]) -> bool:
    # +/-1 exponents are 0 or 2 in Z/4.  A C^*-coboundary may require i-valued
    # 2-cochains, so quotient by the full Z/4 coboundary image, not only +/-1.
    diff = 2 * (a ^ b).astype(np.int64)
    return tuple(int(x % 4) for x in diff) in image_z4


def h3_cstar_classes() -> Tuple[np.ndarray, ...]:
    c2_classes = pm_one_cocycle_classes_mod_pm_coboundary()
    reps = [cls[0] for cls in c2_classes]
    image_z4 = z4_two_coboundary_image()
    remaining = set(range(len(reps)))
    cstar_classes = []
    while remaining:
        i = min(remaining)
        same = {j for j in remaining if cstar_equiv(reps[i], reps[j], image_z4)}
        cstar_classes.append(reps[i])
        remaining.difference_update(same)
    assert len(cstar_classes) == 8
    return tuple(cstar_classes)


def eval_pm(cocycle: np.ndarray, a: Elt, b: Elt, c: Elt) -> int:
    """Return +1/-1 for a normalized +/-1-valued cocycle."""
    if E in (a, b, c):
        return 1
    exponent = int(cocycle[INDEX[3][(a, b, c)]])
    return -1 if exponent else 1


def restriction_triples() -> Dict[Tuple[int, int, int], np.ndarray]:
    out = {}
    for cocycle in h3_cstar_classes():
        triple = (eval_pm(cocycle, g, g, g), eval_pm(cocycle, h, h, h), eval_pm(cocycle, k, k, k))
        assert triple not in out
        out[triple] = cocycle
    assert len(out) == 8
    return out


# ---------------------------------------------------------------------------
# Canonical representatives after Meng--Yu's indicator reduction.
# ---------------------------------------------------------------------------


def omega_exponent(p: int, a: Elt, b: Elt, c: Elt) -> int:
    """Z/4 exponent of pullback of the C2 3-cocycle (-1)^(p abc)."""
    return (2 * p * q(a) * q(b) * q(c)) % 4


def alpha_exponent(p: int, a: Elt, b: Elt, x: int) -> int:
    """Twist for the transitive G-set G/H, realized as the regular Q=C2 module."""
    return (2 * p * q(a) * q(b) * x) % 4


def verify_twisted_module_pentagon(p: int) -> None:
    # alpha(a,b;c.x) alpha(ab,c;x)
    # = omega(a,b,c) alpha(b,c;x) alpha(a,bc;x)
    for a, b, c, x in product(G, G, G, XSET):
        lhs = (alpha_exponent(p, a, b, act(c, x)) + alpha_exponent(p, add(a, b), c, x)) % 4
        rhs = (
            omega_exponent(p, a, b, c)
            + alpha_exponent(p, b, c, x)
            + alpha_exponent(p, a, add(b, c), x)
        ) % 4
        assert lhs == rhs


# ---------------------------------------------------------------------------
# Explicit module autoequivalences of M(G/H,alpha).
# ---------------------------------------------------------------------------

BETA_KEYS = tuple(product(NONZERO, XSET))
BETA_INDEX = {key: i for i, key in enumerate(BETA_KEYS)}
Beta = Tuple[int, ...]  # Z/4 exponents of fourth roots of unity.


def beta_value(beta: Beta, a: Elt, x: int) -> int:
    return 0 if a == E else beta[BETA_INDEX[(a, x)]]


def beta_solutions(p: int, shift: int) -> Tuple[Beta, ...]:
    """Solve the Galindo--Plavnik 1-cell equation for L(x)=x+shift."""
    out = []
    for beta in product(range(4), repeat=len(BETA_KEYS)):
        valid = True
        for sigma, tau, x in product(G, G, XSET):
            lhs = (
                beta_value(beta, tau, x)
                - beta_value(beta, add(sigma, tau), x)
                + beta_value(beta, sigma, act(tau, x))
            ) % 4
            rhs = (
                alpha_exponent(p, sigma, tau, x ^ shift)
                - alpha_exponent(p, sigma, tau, x)
            ) % 4
            if lhs != rhs:
                valid = False
                break
        if valid:
            out.append(tuple(int(v) for v in beta))
    assert len(out) == 8
    return tuple(out)


def beta_equivalent(a: Beta, b: Beta) -> bool:
    """2-cell equivalence for two module 1-cells with the same underlying map."""
    for theta in product(range(4), repeat=2):
        if all(
            (beta_value(b, sigma, x) - beta_value(a, sigma, x)) % 4
            == (theta[x] - theta[act(sigma, x)]) % 4
            for sigma, x in product(G, XSET)
        ):
            return True
    return False


def beta_classes(p: int, shift: int) -> Tuple[Tuple[Beta, ...], ...]:
    solutions = beta_solutions(p, shift)
    remaining = set(range(len(solutions)))
    classes = []
    while remaining:
        i = min(remaining)
        same = {j for j in remaining if beta_equivalent(solutions[i], solutions[j])}
        classes.append(tuple(solutions[j] for j in sorted(same)))
        remaining.difference_update(same)
    assert len(classes) == 2
    assert all(len(c) == 4 for c in classes)
    return tuple(classes)


def all_module_functor_classes(p: int) -> Tuple[Tuple[int, Tuple[Beta, ...]], ...]:
    return tuple((shift, cls) for shift in XSET for cls in beta_classes(p, shift))


def compose_functors(second: Tuple[int, Beta], first: Tuple[int, Beta]) -> Tuple[int, Beta]:
    """Composition (second after first), using pullback of second's beta by first."""
    s2, b2 = second
    s1, b1 = first
    values = []
    for sigma, x in BETA_KEYS:
        values.append((beta_value(b2, sigma, x ^ s1) + beta_value(b1, sigma, x)) % 4)
    return s1 ^ s2, tuple(values)


def functor_class_index(p: int, item: Tuple[int, Beta]) -> int:
    shift, beta = item
    for i, (candidate_shift, cls) in enumerate(all_module_functor_classes(p)):
        if candidate_shift == shift and any(beta_equivalent(beta, representative) for representative in cls):
            return i
    raise AssertionError("module-functor class not found")


def module_autoequivalence_orders(p: int) -> Tuple[int, ...]:
    classes = all_module_functor_classes(p)
    reps = [(shift, cls[0]) for shift, cls in classes]
    table = []
    for left in reps:
        table.append(tuple(functor_class_index(p, compose_functors(left, right)) for right in reps))

    identity = next(
        i for i in range(4)
        if all(table[i][j] == j and table[j][i] == j for j in range(4))
    )
    orders = []
    for i in range(4):
        current = identity
        for n in range(1, 9):
            current = table[i][current]
            if current == identity:
                orders.append(n)
                break
    assert sorted(orders) == [1, 2, 2, 2]  # C2 x C2, not C4.

    swap_classes = [i for i, (shift, _) in enumerate(classes) if shift == 1]
    assert len(swap_classes) == 2
    assert all(orders[i] == 2 for i in swap_classes)
    return tuple(orders)


def main() -> None:
    triples = restriction_triples()
    print("H^3(V4,C*) restriction triples:")
    for triple in sorted(triples):
        print(" ", triple)
    assert set(triples) == set(product((1, -1), repeat=3))

    meng_yu_allowed = ((1, 1, 1), (-1, 1, -1))
    print("\nMeng--Yu allowed pointed classes for R(2,2):", meng_yu_allowed)
    assert all(t in triples for t in meng_yu_allowed)

    for p, triple in ((0, (1, 1, 1)), (1, (-1, 1, -1))):
        verify_twisted_module_pentagon(p)
        orders = module_autoequivalence_orders(p)
        print(f"\np={p}, restriction triple={triple}")
        print("  twisted module pentagon: PASS")
        print("  module autoequivalence group orders:", orders)
        print("  conclusion: Aut_P(M) ~= C2 x C2; an involutive coset-swap lift exists")


if __name__ == "__main__":
    main()
