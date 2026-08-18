"""Exact adjacent-plaquette commutation benchmark for Fibonacci Levin--Wen.

The patch consists of two hexagons sharing one edge. It has:
- 11 internal lattice edges,
- 8 fixed dangling/external legs,
- 10 trivalent vertices.

For each of the 2^8 external-label assignments, the script:
1. enumerates the complete admissible internal-edge Hilbert-space block;
2. constructs the left and right B_p^tau operators from local F factors;
3. multiplies the two sparse operators in both orders;
4. verifies exact equality in Q[q]/(q^4 + q^2 - 1).

The quotient polynomial follows from the frozen F-stage relations
q^2 = alpha and alpha^2 + alpha - 1 = 0.

Research labels:
- CLASSICAL: adjacent Levin--Wen plaquette operators commute.
- REFORMULATION: compare the two operator products as competing rewrite histories.
- COMPUTATIONAL-CLAIM: exhaustive exact verification on all 256 external sectors.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product
from typing import Dict, List, Mapping, Sequence, Tuple

ONE = "1"
TAU = "t"
LABELS = (ONE, TAU)

# Exact coefficient ring K = Q[q]/(q^4 + q^2 - 1).
# Integer tuples are enough for all products/sums in this finite benchmark.
Elt = Tuple[int, int, int, int]
ZERO: Elt = (0, 0, 0, 0)
UNIT: Elt = (1, 0, 0, 0)
Q: Elt = (0, 1, 0, 0)
ALPHA: Elt = (0, 0, 1, 0)
NEG_ALPHA: Elt = (0, 0, -1, 0)


def add(x: Elt, y: Elt) -> Elt:
    return tuple(a + b for a, b in zip(x, y))  # type: ignore[return-value]


def mul(x: Elt, y: Elt) -> Elt:
    """Multiply modulo q^4 + q^2 - 1."""
    coeff = [0] * 7
    for i, a in enumerate(x):
        if a:
            for j, b in enumerate(y):
                if b:
                    coeff[i + j] += a * b
    # q^d = q^(d-4) - q^(d-2), d >= 4.
    for degree in range(6, 3, -1):
        c = coeff[degree]
        if c:
            coeff[degree] = 0
            coeff[degree - 4] += c
            coeff[degree - 2] -= c
    return tuple(coeff[:4])  # type: ignore[return-value]


def fuse(a: str, b: str) -> Tuple[str, ...]:
    if a == ONE:
        return (b,)
    if b == ONE:
        return (a,)
    if a == TAU and b == TAU:
        return (ONE, TAU)
    raise ValueError((a, b))


def triple_allowed(a: str, b: str, c: str) -> bool:
    return c in fuse(a, b)


def f_symbol(a: str, b: str, c: str, d: str, e: str, f: str) -> Elt:
    """Frozen F^{abc}_d[e,f] in exact q-polynomial form."""
    admissible = (
        e in fuse(a, b)
        and d in fuse(e, c)
        and f in fuse(b, c)
        and d in fuse(a, f)
    )
    if not admissible:
        return ZERO
    if ONE in (a, b, c):
        return UNIT
    if d == ONE:
        return UNIT
    return {
        (ONE, ONE): ALPHA,
        (ONE, TAU): Q,
        (TAU, ONE): Q,
        (TAU, TAU): NEG_ALPHA,
    }[(e, f)]


# Two hexagons share AB.
#
# Left:  A-B-C-D-E-F-A
# Right: B-A-G-H-I-J-B
#
# C,D,E,F,G,H,I,J carry the eight fixed dangling legs.
INTERNAL = ("AB", "BC", "CD", "DE", "EF", "FA", "AG", "GH", "HI", "IJ", "JB")
INDEX = {edge: i for i, edge in enumerate(INTERNAL)}
DANGLES = ("c", "d", "e", "f", "g", "h", "i", "j")

VERTICES = {
    "A": ("AB", "FA", "AG"),
    "B": ("AB", "BC", "JB"),
    "C": ("BC", "CD", "c"),
    "D": ("CD", "DE", "d"),
    "E": ("DE", "EF", "e"),
    "F": ("EF", "FA", "f"),
    "G": ("AG", "GH", "g"),
    "H": ("GH", "HI", "h"),
    "I": ("HI", "IJ", "i"),
    "J": ("IJ", "JB", "j"),
}

# The edge list stores the "current" cyclic edge at each vertex; the previous
# edge is the preceding list item.
LEFT_EDGES = ("BC", "CD", "DE", "EF", "FA", "AB")
LEFT_EXTERNAL = ("JB", "c", "d", "e", "f", "AG")

RIGHT_EDGES = ("AG", "GH", "HI", "IJ", "JB", "AB")
RIGHT_EXTERNAL = ("FA", "g", "h", "i", "j", "BC")

State = Tuple[str, ...]
SparseOp = Dict[Tuple[int, int], Elt]


def state_map(state: State, external: Mapping[str, str]) -> Dict[str, str]:
    out = {edge: state[INDEX[edge]] for edge in INTERNAL}
    out.update(external)
    return out


def admissible_basis(external: Mapping[str, str]) -> List[State]:
    result: List[State] = []
    for labels in product(LABELS, repeat=len(INTERNAL)):
        values = state_map(labels, external)
        if all(
            triple_allowed(*(values[edge] for edge in incident))
            for incident in VERTICES.values()
        ):
            result.append(labels)
    return result


def local_factor(
    external: str,
    old_prev: str,
    old_cur: str,
    inserted: str,
    new_prev: str,
    new_cur: str,
) -> Elt:
    # F^{a old_prev old_cur}_{s new_cur new_prev}
    # = [F^{a,old_prev,s}_{new_cur}]_{old_cur,new_prev}.
    return f_symbol(external, old_prev, inserted, new_cur, old_cur, new_prev)


def plaquette_operator(
    basis: Sequence[State],
    external: Mapping[str, str],
    face_edges: Sequence[str],
    face_external: Sequence[str],
    inserted: str = TAU,
) -> SparseOp:
    positions = [INDEX[edge] for edge in face_edges]
    position = {state: i for i, state in enumerate(basis)}
    operator: SparseOp = {}

    for col, old_state in enumerate(basis):
        old = state_map(old_state, external)
        for new_values in product(LABELS, repeat=6):
            trial = list(old_state)
            for p, value in zip(positions, new_values):
                trial[p] = value
            new_state = tuple(trial)
            row = position.get(new_state)
            if row is None:
                continue

            new = state_map(new_state, external)
            coeff = UNIT
            for k, (cur_edge, external_edge) in enumerate(
                zip(face_edges, face_external)
            ):
                prev_edge = face_edges[(k - 1) % 6]
                coeff = mul(
                    coeff,
                    local_factor(
                        old[external_edge],
                        old[prev_edge],
                        old[cur_edge],
                        inserted,
                        new[prev_edge],
                        new[cur_edge],
                    ),
                )
                if coeff == ZERO:
                    break
            if coeff != ZERO:
                operator[(row, col)] = coeff

    return operator


def compose(left: SparseOp, right: SparseOp) -> Tuple[SparseOp, int]:
    """Sparse exact composition left @ right and scalar multiplication count."""
    left_by_mid: Dict[int, List[Tuple[int, Elt]]] = defaultdict(list)
    right_by_mid: Dict[int, List[Tuple[int, Elt]]] = defaultdict(list)
    for (row, mid), value in left.items():
        left_by_mid[mid].append((row, value))
    for (mid, col), value in right.items():
        right_by_mid[mid].append((col, value))

    result: Dict[Tuple[int, int], Elt] = defaultdict(lambda: ZERO)
    multiplication_count = 0
    for mid in left_by_mid.keys() & right_by_mid.keys():
        multiplication_count += len(left_by_mid[mid]) * len(right_by_mid[mid])
        for row, a in left_by_mid[mid]:
            for col, b in right_by_mid[mid]:
                result[(row, col)] = add(result[(row, col)], mul(a, b))

    return (
        {key: value for key, value in result.items() if value != ZERO},
        multiplication_count,
    )


def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def verify_all_external_sectors() -> Dict[str, object]:
    dimension_by_tau_count: Dict[int, set[int]] = defaultdict(set)
    dimension_histogram = Counter()
    failures = []
    max_record = None

    for dangling_labels in product(LABELS, repeat=len(DANGLES)):
        external = dict(zip(DANGLES, dangling_labels))
        basis = admissible_basis(external)
        dim = len(basis)
        tau_count = dangling_labels.count(TAU)

        dimension_by_tau_count[tau_count].add(dim)
        dimension_histogram[dim] += 1
        assert dim == 5 * fibonacci(tau_count + 1)

        left = plaquette_operator(basis, external, LEFT_EDGES, LEFT_EXTERNAL)
        right = plaquette_operator(basis, external, RIGHT_EDGES, RIGHT_EXTERNAL)

        lr, lr_mults = compose(left, right)
        rl, rl_mults = compose(right, left)
        if lr != rl:
            failures.append(dangling_labels)

        record = {
            "tau_external": tau_count,
            "dimension": dim,
            "left_nnz": len(left),
            "right_nnz": len(right),
            "product_nnz": len(lr),
            "left_right_scalar_mults": lr_mults,
            "right_left_scalar_mults": rl_mults,
            "external": dangling_labels,
        }
        if max_record is None or dim > max_record["dimension"]:
            max_record = record

    assert not failures
    assert all(len(values) == 1 for values in dimension_by_tau_count.values())

    return {
        "verified_external_sectors": 2 ** len(DANGLES),
        "dimension_by_tau_count": {
            k: next(iter(v)) for k, v in sorted(dimension_by_tau_count.items())
        },
        "dimension_histogram": dict(sorted(dimension_histogram.items())),
        "max_sector": max_record,
        "failures": len(failures),
    }


def main() -> None:
    # Ring sanity checks.
    assert mul(Q, Q) == ALPHA
    assert mul(ALPHA, ALPHA) == (1, 0, -1, 0)

    summary = verify_all_external_sectors()
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
